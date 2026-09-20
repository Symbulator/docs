r"""Every circuit in the Manual must parse, and most must solve.

The Course's 297 worked problems are taken from printed textbooks and
every answer is checked against the book's own (`check_against_originals.py`).
The Manual's examples are invented, so they have no external answer to be
checked against -- which means the only thing standing between a reader and
a wrong circuit is whoever typed it.

This closes most of that gap. For every ```field 9 Circuit Description
fence in a `book: manual` chapter:

  * it must **parse** -- `parse_circuit` does grammar, field counts, names,
    brackets and topology, so a typo in a description cannot reach a reader;
  * unless the fence is listed in `FRAGMENTS` below, it must be a complete
    circuit, so an illustrative snippet is a deliberate, named exception
    rather than a silent one;
  * it is then **solved**, and the answers printed, so the `::: result`
    panels on the page can be read against what the app actually returns.

**What this does not do**, stated plainly because a checker that is trusted
for more than it does is worse than none: it does not compare the printed
`::: result` LaTeX against the solve. A result panel is hand-written -- that
is how TR5's Example 4.5 printed a wrong subscript for as long as it existed
(#370). **`check_manual_results.py` does that**, since #466: it reads every
panel back into an expression and compares it with the package and with the
app, using `manual_runs.py`'s record of how each circuit is run, which this
check cannot have because the chapters do not say. `--show` here still
prints the answers next to the panels for a person to read.

    py tools/check_manual_examples.py
    py tools/check_manual_examples.py --show

Exit status is 1 if anything failed to parse or solve.
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
APP = os.path.normpath(os.path.join(
    ROOT, "..", "Application", "v9", "repos", "server"))

if not os.path.isdir(APP):
    raise SystemExit(
        f"check_manual_examples: {APP} is missing. This tool solves each\n"
        "example through the app's own symbulator_ui, so the application\n"
        "tree must sit beside Documentation -- see the top-level CLAUDE.md.")
sys.path.insert(0, APP)

import symbulator_ui                                        # noqa: E402
from symbulator.elements import parse_circuit, CircuitError  # noqa: E402

# A fence that is deliberately not a whole circuit, with the reason. Keep
# this list short: in a manual, a runnable example is better documentation
# than a snippet, so an entry here should have to justify itself.
FRAGMENTS: dict[str, str] = {}

FENCE = re.compile(
    r"^```field\s+9\s+Circuit Description\s*$\n(.*?)^```\s*$",
    re.M | re.S)
RESULT = re.compile(r"^::: result\s*$\n(.*?)^:::\s*$", re.M | re.S)


def manual_chapters() -> list[str]:
    out = []
    for f in sorted(os.listdir(SRC)):
        if not f.endswith(".md"):
            continue
        head = open(os.path.join(SRC, f), encoding="utf-8").read(1200)
        if re.search(r"^book:\s*manual\s*$", head, re.M):
            out.append(f)
    return out


def solve(desc: str, domain: str = "dc", omega: str = ""):
    return symbulator_ui.solve_ui(desc, domain, omega, None, "solve",
                                  "", "", "z", None, None, None)


def main() -> int:
    show = "--show" in sys.argv
    files = manual_chapters()
    if not files:
        print("check_manual_examples: no chapters carry `book: manual` yet")
        return 0

    fences = failed = solved = 0
    problems: list[str] = []

    for f in files:
        text = open(os.path.join(SRC, f), encoding="utf-8").read()
        blocks = list(FENCE.finditer(text))
        print(f"\n{f}  --  {len(blocks)} circuit(s)")
        for m in blocks:
            fences += 1
            desc = m.group(1).strip()
            one = desc.replace("\n", ":")
            line = text[:m.start()].count("\n") + 1
            key = f"{f}:{line}"

            try:
                els = parse_circuit(desc)
            except CircuitError as e:
                if key in FRAGMENTS:
                    print(f"  {line:>5}  fragment  ({FRAGMENTS[key]})")
                    continue
                failed += 1
                problems.append(f"{key}: does not parse -- {e}")
                print(f"  {line:>5}  PARSE FAILED  {e}")
                continue

            # A page's circuit belongs to whatever analysis that page is
            # about, and the page says so in prose the checker cannot
            # read. Solving everything in DC therefore failed the
            # coupling example honestly and wrongly: in DC an inductor is
            # a short, so a source across one is a real contradiction --
            # of a circuit that is correct in AC, which is where the page
            # runs it. The claim worth making is that the description is
            # a solvable circuit in *some* domain.
            for dom, om in (("dc", ""), ("ac", "1000"), ("fd", ""),
                            ("tr", "")):
                out = solve(one, dom, om)
                if out.get("ok"):
                    break
            if not out.get("ok"):
                failed += 1
                problems.append(f"{key}: solves in no domain -- "
                                f"{out.get('error')}")
                print(f"  {line:>5}  SOLVE FAILED  {out.get('error')}")
                continue

            solved += 1
            note = "" if dom == "dc" else f"  ({dom})"
            print(f"  {line:>5}  ok  {len(els)} elements{note}")
            if show:
                for row in out.get("elements") or []:
                    for it in row["items"]:
                        print(f"          {row['name']:<6}{it['label']:<20}"
                              f"{it['plain']}")
                # The page's own panels, for reading against the above.
                tail = text[m.end(): m.end() + 1400]
                for r in RESULT.finditer(tail):
                    print(f"          page prints: {r.group(1).strip()}")

    print(f"\ncircuits {fences}, solved {solved}, failed {failed}")
    for p in problems:
        print("  " + p)
    print("note: this proves each circuit parses and solves; the printed "
          "result panels are compared by tools/check_manual_results.py.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
