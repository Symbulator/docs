#!/usr/bin/env python3
"""Remove generated version 9 panels so they can be regenerated.

    py tools/undo_v9_panels.py --damaged        # dry run
    py tools/undo_v9_panels.py --damaged --apply

A generated region is a ```field 9 ... ``` panel, optionally followed by a
`::: only 9` block, sitting immediately after a ```sym 8 fence. This removes
whole regions so add_v9_practice.py can produce them again from the
calculator call above -- which is the only safe way to fix a converter bug
after the fact, because the panels carry no record of what produced them.

--damaged limits it to regions that look wrong: an Evaluate panel containing
`approx(`, or unbalanced brackets. Without it, every generated region goes,
which is the nuclear option and wants a dry run first.

Hand-written panels are not safe from this. Regions written by hand during
the chapter rewrites are indistinguishable from generated ones, so check the
dry run before applying.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"


def looks_damaged(region: list[str]) -> bool:
    joined = " ".join(region)
    if "approx(" in joined:
        return True
    if joined.count("(") != joined.count(")"):
        return True
    if joined.count("{") != joined.count("}"):
        return True
    return False


def strip_regions(text: str, damaged_only: bool) -> tuple[str, int, list]:
    lines = text.split("\n")
    out: list[str] = []
    removed, samples = 0, []
    i = 0
    while i < len(lines):
        out.append(lines[i])
        if not lines[i].startswith("```sym 8"):
            i += 1
            continue
        # copy the fence body and its close
        i += 1
        while i < len(lines) and not lines[i].startswith("```"):
            out.append(lines[i]); i += 1
        if i < len(lines):
            out.append(lines[i]); i += 1

        start = i
        region: list[str] = []
        j = i
        while j < len(lines) and not lines[j].strip():
            j += 1
        if not (j < len(lines) and lines[j].startswith("```field 9")):
            continue
        # the panel
        region += lines[i:j + 1]
        j += 1
        while j < len(lines) and not lines[j].startswith("```"):
            region.append(lines[j]); j += 1
        if j < len(lines):
            region.append(lines[j]); j += 1
        # an optional ::: only 9 block right after
        k = j
        while k < len(lines) and not lines[k].strip():
            k += 1
        if k < len(lines) and lines[k].strip() == "::: only 9":
            region += lines[j:k + 1]
            k += 1
            depth = 1
            while k < len(lines) and depth:
                region.append(lines[k])
                t = lines[k].strip()
                if t.startswith("::: "):
                    depth += 1
                elif t == ":::":
                    depth -= 1
                k += 1
            j = k

        if damaged_only and not looks_damaged(region):
            continue                       # keep it: copy through untouched
        removed += 1
        samples.append((start + 1, region[:6]))
        i = j                              # skip the region entirely
    return "\n".join(out), removed, samples


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--damaged", action="store_true",
                    help="only regions that look wrong (recommended)")
    ap.add_argument("--only", metavar="FILE")
    args = ap.parse_args()

    files = sorted(SRC.glob("*.md"))
    if args.only:
        files = [f for f in files if f.name == args.only]
    total = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        new, n, samples = strip_regions(text, args.damaged)
        if not n:
            continue
        total += n
        print(f"\n{f.name}: {n} region(s)")
        for line_no, head in samples[:3]:
            print(f"  at line {line_no}:")
            for h in head:
                print(f"      {h}")
        if args.apply:
            f.write_text(new, encoding="utf-8", newline="\n")
    print(f"\n{'REMOVED' if args.apply else 'WOULD REMOVE'} {total} region(s)")
    if not args.apply:
        print("Nothing written. Re-run with --apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
