"""Turn one calculator call into the Symbulator 9 blocks that replace it.

Imported by add_v9_practice.py. Kept separate because the mapping from a
calculator call to a set of interface actions is the whole idea, and it
deserves to be readable on its own.

Every function here returns a list of markdown lines, or None when the call
is not one it can handle -- in which case the caller leaves the fence alone
rather than guessing.
"""

from __future__ import annotations

import re

EN_DASH = "–"

# s\dc("desc")            s\ac("desc",1000)       s\tr("desc"):{vc,ic}
CALL = re.compile(
    r'^s\\(?P<fn>dc|ac|ex|fd|tr)\('
    r'"(?P<desc>[^"]*)"'
    r'(?P<rest>[^)]*)\)'
    r'(?::(?P<sel>.+))?$')

# s\th("desc",2,0)  or  s\th(cir,2,0)
TH = re.compile(
    r'^s\\th\('
    r'(?:"(?P<desc>[^"]*)"|(?P<var>\w+))'
    r'\s*,\s*(?P<n1>[\w]+)\s*,\s*(?P<n2>[\w]+)\s*\)'
    r'(?::(?P<sel>.+))?$')

ONLY = re.compile(r'^s\\only\(\s*"?(?P<vars>[^")]*)"?\s*\)$')

DOMAIN = {
    "dc": ("*DC — direct current*", None),
    "ac": ("*AC — alternating current*", "omega"),
    "fd": ("*FD — complex frequency domain*", None),
    "tr": ("*TR — transient / time domain*", None),
}

# A selector item that is a bare answer name -- vr1, ir3, v2, pmax -- rather
# than an expression to be worked out.
BARE = re.compile(r"^[a-z]+[a-z0-9_]*$", re.I)


def split_elements(desc: str) -> list[str]:
    """Split a description on its top-level colons, ASCII-ing the minus.

    The en dash is correct for the calculators, which have a separate
    negation key, and is refused by Symbulator 9 as a character outside its
    syntax. Only the version 9 panel is converted."""
    desc = desc.replace(EN_DASH, "-")
    out, depth, cur = [], 0, ""
    for ch in desc:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == ":" and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [e.strip() for e in out if e.strip()]


def _panel(desc: str) -> list[str]:
    return ["```field 9 Circuit description"] + split_elements(desc) + ["```"]


def _selector_lines(sel: str) -> list[str]:
    """What to do with the `:{a,b,c}` tail of a calculator call.

    A bare answer name is something to read off the Results section. Anything
    with arithmetic in it has to be worked out, which is the Evaluate card's
    job."""
    sel = sel.strip().replace(EN_DASH, "-")

    # `:approx({ir1,ir2,ir3})` -- approx is the calculator's "give me that as
    # a decimal", which in version 9 is the Rounding menu, not something you
    # type. Unwrap it before splitting, or its inner commas split the call
    # apart and produce nonsense like `approx({ir1` as an expression to
    # evaluate. That is exactly what happened to 22 panels on 24 Aug 2026.
    approx = False
    while True:
        m = re.match(r"^approx\((.*)\)$", sel, re.S)
        if not m:
            break
        sel, approx = m.group(1).strip(), True

    sel = sel.strip().strip("{}")
    items = [s.strip() for s in sel.split(",") if s.strip()]
    if not items:
        return []
    names = [i for i in items if BARE.match(i)]
    exprs = [i for i in items if not BARE.match(i)]

    out: list[str] = []
    if names:
        shown = ", ".join(f"`{n}`" for n in names[:-1])
        shown = f"{shown} and `{names[-1]}`" if shown else f"`{names[-1]}`"
        verb = "are" if len(names) > 1 else "is"
        out.append(f"The answer{'s' if len(names) > 1 else ''} you want "
                   f"{verb} {shown}, in **Results**.")
    if exprs:
        if names:
            out.append("")
        out.append("Ask **Evaluate** for:")
        out.append("")
        out.append("```field 9 Evaluate")
        out.extend(exprs)
        out.append("```")
    if approx:
        out.append("")
        out.append("The calculator versions wrap this in `approx` to get a "
                   "decimal. Version 9 does that through **Rounding** "
                   "instead — *approximate to n significant digits* with "
                   "**n** = 3 is a good setting for this one.")
    return out


def convert_call(body: str) -> list[str] | None:
    """A dc/ac/ex/fd/tr call, with or without a result selector."""
    m = CALL.match(body.strip())
    if not m:
        return None
    fn, desc, rest, sel = (m.group("fn"), m.group("desc"),
                           m.group("rest") or "", m.group("sel"))
    lines = _panel(desc)

    label, extra = DOMAIN[fn if fn != "ex" else "dc"]
    notes: list[str] = []
    if fn != "dc":
        notes.append(f"Set **Analysis** to {label}.")
    arg = rest.strip().lstrip(",").strip()
    if fn == "ac" and arg:
        notes.append(f"The frequency box takes **{arg}**.")
    if fn == "ex":
        notes.append("This one needs **Enable Expert Mode** ticked in "
                     "**Settings**; the equations and unknowns go in the "
                     "boxes it reveals.")
    inner: list[str] = []
    if notes:
        inner.append(" ".join(notes))
    if sel:
        if inner:
            inner.append("")
        inner += _selector_lines(sel)
    if inner:
        lines += ["", "::: only 9"] + inner + [":::"]
    return lines


def convert_th(body: str) -> list[str] | None:
    """s\\th(desc, n1, n2) -- the Find equivalent tool."""
    m = TH.match(body.strip())
    if not m:
        return None
    desc, n1, n2, sel = (m.group("desc"), m.group("n1"),
                         m.group("n2"), m.group("sel"))
    lines: list[str] = []
    if desc:
        lines += _panel(desc)
        lines.append("")
    inner = [
        "Set **Type of analysis** to *Find equivalent* and **Type of "
        "equivalent** to *Thévenin / Norton*. Two node boxes appear: put "
        f"**{n1}** in the first and **{n2}** in the second — the pair of "
        "terminals you are looking into.",
    ]
    if sel:
        inner.append("")
        inner += _selector_lines(sel)
    lines += ["::: only 9"] + inner + [":::"]
    return lines


def convert_only(body: str) -> list[str] | None:
    """s\\only(...) -- limiting which answers get computed."""
    m = ONLY.match(body.strip())
    if not m:
        return None
    names = [v.strip() for v in m.group("vars").split(",") if v.strip()]
    if not names:
        return None
    listed = ", ".join(names)
    return [
        "",
        "::: only 9",
        "This is optional: Symbulator 9 solves quickly enough that limiting "
        "the results rarely saves you anything worth having. If you want to "
        "anyway, tick **Do you want to limit the results to save time?** in "
        f"**Settings** and list `{listed}` in the box beside it.",
        ":::",
    ]


def convert(body: str) -> list[str] | None:
    """Try each shape in turn."""
    for fn in (convert_th, convert_call, convert_only):
        out = fn(body)
        if out:
            return out
    return None
