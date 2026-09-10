"""Draw every thesis circuit with the version 9 schematic engine.

This is version 3's artwork. Drawing does not require solving, so a
circuit the solver refuses may still draw -- the census is taken here
separately rather than assumed from the solve census.
"""
import os
import sys

import symbulator as sb

from parse_book import parse
from to_v9 import convert

OUT = "v9_svg"


def main():
    os.makedirs(OUT, exist_ok=True)
    drawn, failed, skipped = [], [], []
    for p in parse():
        num = p["num"]
        if not p["netlists"]:
            skipped.append((num, "no netlist in the Book"))
            continue
        tool, desc, rest = p["netlists"][0]
        c = convert(tool, desc, rest, stores=p.get('stores'))
        if c["analysis"] is None:
            skipped.append((num, c["notes"][0]))
            continue
        try:
            svg = sb.to_svg(c["desc"])
        except Exception as exc:
            failed.append((num, f"{type(exc).__name__}: {exc}"))
            continue
        path = os.path.join(OUT, f"p{num}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg)
        drawn.append(num)
    print(f"drawn {len(drawn)}, failed {len(failed)}, skipped {len(skipped)}")
    for num, why in failed:
        print(f"  FAILED {num}: {why[:96]}")
    for num, why in skipped:
        print(f"  skipped {num}: {why[:70]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
