"""Translate calculator syntax left inside version 9 panels.

The rewrite turned calculator calls into panels showing what a reader types
into the web interface, but a value copied across verbatim can still be
written the way the TI-89 reads it. The calculator infers a multiplication
between `2` and `ir3`; version 9 does not, and answers "invalid decimal
literal". The reader following that panel gets an error, not a circuit --
and nothing in the docs build can see it, because the docs build does not
know what the app accepts.

Every rule below was checked against the running app before being written
here (see VERIFIED-v9-api.md):

    2ir3        -> 2*ir3          implicit multiplication
    .2v1        -> .2*v1          the same, before an answer name
    e^(-4t)     -> exp(-4*t)      the calculator's power-of-e notation
    u(t)        -> Heaviside(t)   unit step
    d(t)        -> DiracDelta(t)  impulse  (written with a Greek delta)
    30 degrees  -> 30*pi/180      the degree sign is not in the charset
    beta, gamma                   Greek letters are not in the charset

Nothing is trusted: each panel is solved before and after, and a rewrite is
kept only if it turns a panel that failed into one that reads. Panels this
cannot fix are listed for a human -- renaming an element is a judgement
call, not a substitution.

Usage:
    python tools/fix_v9_panels.py            # report what it would change
    python tools/fix_v9_panels.py --write    # apply
"""
import glob
import io
import os
import re
import sys

sys.path.insert(0, r"C:\Users\perez\Claude Code\Application\v9\repos\server")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import symbulator_ui as ui                                    # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
OPEN = re.compile(r"^```field 9 Circuit Description\s*$")

GREEK = {
    "\u03b1": "alpha", "\u03b2": "beta", "\u03b3": "gamma",
    "\u03b4": "delta", "\u03c9": "w", "\u03bc": "u", "\u00b5": "u",
    "\u03c4": "tau", "\u03c6": "phi", "\u03b8": "theta",
}


def translate(value: str) -> str:
    """One value field, rewritten into what version 9 reads."""
    v = value

    # The calculator's e^(x). Do this before inserting multiplications, so
    # the `10` in `10e^(-t)` meets `exp` rather than a bare `e`.
    v = re.sub(r"(?<![A-Za-z_.])e\^", "exp", v)
    v = re.sub(r"\bexp(?!\()", "exp", v)

    # Step and impulse. `u` is also the micro prefix, but only ever after
    # a quote ("1'u"), so a bare u( cannot be confused with it.
    v = re.sub(r"(?<![\w.])u\s*\(", "Heaviside(", v)
    v = re.sub(r"(?<![\w.])\u03b4\s*\(", "DiracDelta(", v)

    # Degrees, before the Greek pass so the sign is still recognisable.
    v = re.sub(r"(\d+(?:\.\d+)?)\s*\u00b0", r"(\1*pi/180)", v)

    for greek, name in GREEK.items():
        v = v.replace(greek, name)

    # Implicit multiplication: a number against a name, a closing bracket
    # against either. Never after a quote -- that is an SI suffix (1'k).
    v = re.sub(r"(?<!')(\d)(?=[A-Za-z_])", r"\1*", v)
    v = re.sub(r"\)(?=[A-Za-z0-9_(])", ")*", v)
    v = re.sub(r"(?<=[A-Za-z0-9_)])\(", "*(", v)

    # The last rule would also break a genuine call, so put those back.
    for fn in ("exp", "Heaviside", "DiracDelta", "sin", "cos", "tan", "log",
               "ln", "sqrt", "pr", "abs", "Abs", "re", "im", "arg", "sign"):
        v = v.replace(fn + "*(", fn + "(")
    return v


def rewrite(desc_lines: list) -> list:
    """A whole panel: translate the value fields, leave names and nodes."""
    out = []
    for line in desc_lines:
        if not line.strip():
            out.append(line)
            continue
        parts = line.split(",")
        if len(parts) < 4:
            out.append(line)                 # a short (name,n1,n2) has none
            continue
        head, values = parts[:3], parts[3:]
        out.append(",".join(head + [translate(v) for v in values]))
    return out


def reads(desc: str) -> bool:
    """Does any analysis read this circuit?"""
    for domain, omega in (("dc", ""), ("ac", "1000"), ("tr", "")):
        try:
            if ui._validate(desc, domain, omega, None):
                continue
            r = ui.solve_ui(desc, domain, omega, None, "solve", "", "", "z",
                            [], [], [], digits=0, si=False, units=True)
            if r.get("ok"):
                return True
        except Exception:                                     # noqa: BLE001
            continue
    return False


def main():
    write = "--write" in sys.argv
    fixed = unfixable = 0

    for path in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        name = os.path.basename(path)
        lines = io.open(path, encoding="utf-8").read().split("\n")
        changed = False
        i = 0
        while i < len(lines):
            if not OPEN.match(lines[i]):
                i += 1
                continue
            start = i + 1
            j = start
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            body = lines[start:j]
            desc = ":".join(b.strip() for b in body if b.strip())
            if desc and not reads(desc):
                new_body = rewrite(body)
                new_desc = ":".join(b.strip() for b in new_body if b.strip())
                if not reads(new_desc):
                    # Some panels need both passes: the syntax translated
                    # AND a value symbol renamed off a Python/SymPy name.
                    from rename_v9_symbols import apply as rename
                    new_body = [rename(b) for b in new_body]
                    new_desc = ":".join(b.strip() for b in new_body
                                        if b.strip())
                if new_desc != desc and reads(new_desc):
                    fixed += 1
                    changed = True
                    print(f"  {name}:{start}")
                    print(f"      -  {desc[:92]}")
                    print(f"      +  {new_desc[:92]}")
                    lines[start:j] = new_body
                else:
                    unfixable += 1
                    print(f"  {name}:{start}  NEEDS A HUMAN")
                    print(f"      {desc[:92]}")
            i = j + 1
        if changed and write:
            io.open(path, "w", encoding="utf-8",
                    newline="\n").write("\n".join(lines))

    print(f"\n{fixed} panel(s) fixed, {unfixable} need a human")
    if fixed and not write:
        print("dry run -- pass --write to apply")


main()
