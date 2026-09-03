"""Run every version 9 Circuit Description panel through the real app.

The rewrite converts calculator calls into panels showing what a reader
types into the web interface. A panel that was copied across verbatim can
still carry calculator-only syntax -- `.2v1` for a dependent source is the
clearest case: the calculator reads the implicit multiplication, version 9
refuses it. Nothing in the docs build can catch that, because the docs
build does not know what the app accepts. So ask the app.

Reports only; it does not edit.
"""
import glob
import io
import os
import re
import sys

sys.path.insert(0, r"C:\Users\perez\Claude Code\Application\v9\repos\server")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import symbulator_ui as ui                                    # noqa: E402

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "src")
OPEN = re.compile(r"^```field 9 Circuit Description\s*$")


def panels(path):
    """(line number, description) for each circuit panel in a file."""
    lines = io.open(path, encoding="utf-8").read().split("\n")
    i = 0
    while i < len(lines):
        if OPEN.match(lines[i]):
            body, j = [], i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                body.append(lines[j])
                j += 1
            yield i + 1, ":".join(b.strip() for b in body if b.strip())
            i = j
        i += 1


def main():
    bad = ok = 0
    for path in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        name = os.path.basename(path)
        for line, desc in panels(path):
            if not desc:
                continue
            # A single element is an illustration of the syntax, not a
            # circuit -- "m1,l1,l2,1.5" shown to explain the fields. No
            # real circuit has one element, so it cannot be solved and
            # was never meant to be.
            if desc.count(":") == 0:
                continue
            # Symbolic circuits legitimately carry free symbols, so a
            # solve is not the test -- only whether the input is READ.
            # The panel does not say which analysis the reader picks, so
            # try each. If any domain reads the circuit, the panel is fine;
            # only a description no analysis can read is a real fault.
            attempts, err = [], None
            for domain, omega in (("dc", ""), ("ac", "1000"), ("tr", "")):
                try:
                    refused = ui._validate(desc, domain, omega, None)
                    if refused:
                        attempts.append(refused)
                        continue
                    r = ui.solve_ui(desc, domain, omega, None, "solve", "",
                                    "", "z", [], [], [], digits=0, si=False,
                                    units=True)
                    if r.get("ok"):
                        attempts = []
                        break
                    msg = str(r.get("error", "?"))
                    # A circuit that reads but will not solve is not a
                    # documentation fault -- chapter 4's "Tricky" example
                    # fails on purpose, and the lesson is that failure.
                    if "Could not solve the system" in msg:
                        attempts = []
                        break
                    attempts.append(msg)
                except Exception as exc:                      # noqa: BLE001
                    attempts.append(f"{type(exc).__name__}: {exc}")
            if attempts:
                err = attempts[0]
            if err:
                bad += 1
                print(f"  {name}:{line}\n      {desc[:96]}\n      -> {err[:150]}")
            else:
                ok += 1
    print(f"\n{ok} panel(s) read cleanly, {bad} refused")


main()
