#!/usr/bin/env python
"""Every result panel in the built chapter says what the app's card says (#443).

Roberto, 14 Sep 2026, on Example 13.6: *"says it uses approx but the answers
it shows are exact."* It was not one entry. The page rendered a symbolic
answer through a rounding of its own, so all 34 of them, across 21 entries,
differed from what the reader sees on screen -- `60` for the card's `60.0`,
`10000` for its `1.0 \\cdot 10^{4}`, and a different term order in every
transient answer.

`gen.py` now prints the card's own LaTeX, so the two agree by construction.
This checks it anyway, from the other end: it reads the BUILT
chapter (`book.CHAPTER`), pulls every `::: result` panel out of it, and asks
the real app what that answer's card shows at the Rounding the entry's own
`.cir` records. A panel and a card that disagree are a finding.

It is the artefact that is measured, not the generator: a panel typed by
hand, or a `gen.py` that starts rounding again, both fail here.

    py Documentation\\tools\\<book>\\check_card_truth.py
    py Documentation\\tools\\<book>\\check_card_truth.py --prove-red

`--prove-red` rounds one panel in the file it reads and expects the check to
FAIL: a guard nobody has watched fail is not a guard.
"""
import argparse
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import sympy as sp                                            # noqa: E402
import runner, specs, gen, fmt, titles                        # noqa: E402

import book                                                   # noqa: E402
CHAPTER = os.path.join(runner.DOCS, "src", book.CHAPTER)

#: "::: result <label>\n<body>\n:::" inside one problem
_PANEL = re.compile(r"^::: result ([^\n]*)\n(.+?)\n:::", re.M | re.S)
#: "::: problem NR12's Example 5.3 part c" -- a heading, which is `titles`'
#: own, not the spec's number: 7.11a and 7.11b are "7.11 to 35 ms" and
#: "7.11 after 35 ms", and a spec is matched to its heading through titles.
_PROBLEM = re.compile(r"^::: problem (.+?)\s*$", re.M)


def panels_by_entry(text):
    """{problem heading: [(label, body), ...]} from the built chapter."""
    marks = [(m.start(), m.group(1)) for m in _PROBLEM.finditer(text)]
    out = {}
    for i, (start, head) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        out[head] = [(m.group(1).strip(), m.group(2).strip())
                     for m in _PANEL.finditer(text[start:end])]
    return out


def wanted(spec):
    """[(label, body)] the app's cards justify for this spec, in page order."""
    digits, approx = gen.shown_digits(spec)
    shown = runner.app_display(spec, digits=digits, approx=approx)
    _r, vals = runner.run_one(spec)
    out = []
    for k in spec["expect"]:
        if k in spec.get("hide", ()):
            continue
        if k.startswith("@"):
            try:
                got = sp.sympify(k[1:], locals=dict(vals))
            except Exception:                                 # noqa: BLE001
                continue
        else:
            got = vals.get(k)
        if got is None or not sp.sympify(got).free_symbols:
            continue
        if k.startswith("@"):
            card = runner.app_evaluate_display(spec, k[1:], digits=digits,
                                               approx=approx)
        else:
            card = shown.get(fmt.tool_name(k, spec) or k)
            if card is None:
                continue
        tex = gen._CARD_UNIT.sub("", card["latex"]).strip()
        unit = fmt.unit_for(k, spec)
        body = "%s = %s" % (fmt.tex_name(k, spec), tex)
        if unit:
            body += "\\," + (unit if unit == "\\Omega" else "\\mathrm{%s}" % unit)
        out.append((fmt.label_for(k, spec["desc"], spec), body))
    return out


def main(prove_red=False):
    text = io.open(CHAPTER, encoding="utf-8").read()
    if prove_red:
        # round one panel the way the old generator did
        text, n = re.subn(r"\\frac\{480\.0\}\{s \+ 10000\.0\}",
                          r"\\frac{480}{s + 10000}", text, count=1)
        assert n == 1, ("prove-red found no panel to damage -- 13.6's Thevenin "
                        "voltage is not in the chapter as expected")
        print("prove-red: 13.6's Thevenin voltage rounded in the text read")

    built = panels_by_entry(text)
    bad, checked = [], 0
    for spec in specs.SPECS:
        want = wanted(spec)
        if not want:
            continue
        have = built.get(titles.short_title(spec["num"]), [])
        have_bodies = [b for _l, b in have]
        for label, body in want:
            checked += 1
            if body not in have_bodies:
                bad.append((spec["num"], label, body,
                            "; ".join(have_bodies) or "(no panel)"))

    for num, label, body, have in bad:
        print("XX %-7s %s" % (num, label))
        print("      page:  %s" % have[:150])
        print("      card:  %s" % body[:150])
    print("\n--- %d panel(s) checked, %d disagreeing ---" % (checked, len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--prove-red", action="store_true")
    args = ap.parse_args()
    code = main(args.prove_red)
    if args.prove_red:
        print("prove-red: the check %s, as it should"
              % ("FAILED" if code else "PASSED -- THE GUARD IS BLIND"))
        sys.exit(0 if code else 1)
    sys.exit(code)
