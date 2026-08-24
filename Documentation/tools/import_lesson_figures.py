#!/usr/bin/env python3
"""Replace the stand-in lesson figures with the originals from the 2023 site.

    py tools/import_lesson_figures.py                 # dry run
    py tools/import_lesson_figures.py --apply
    py tools/import_lesson_figures.py --apply --skip 01-lesson-dc.md

`assets/circuit/*.svg` are stand-ins drawn by tools/make_demo_figures.py --
line art with no annotations. The real figures, scanned from the textbooks
with the node numbers written on them in blue, are in the 2023 website
archive, which is not part of this tree.

The two use the same coding scheme with different kind letters: b11e0507
here is b11ex0507 there, as7p0937 is as7pr0937, as5f0229 is as5fi0229. So
matching is on book + figure number + trailing letter, with the kind letters
treated as compatible when one is a prefix of the other. All 26 match.

What it does:
  * copies the original in as assets/circuit/<docs stem>.<jpg|png>
  * rewrites `::: figure assets/circuit/<stem>.svg` to the new extension

What it does not do: delete the stand-ins. They become unreferenced, and
removing them is a separate decision -- run it, look at the result, then
delete if you are happy.

The build already understands raster figures: check_figures() skips the
.pdf-pair requirement for them, and the LaTeX emitter keeps the extension
rather than dropping it, so print gets the same image rather than the
leftover stand-in .pdf.
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CIRCUIT = ROOT / "assets" / "circuit"
SRC = ROOT / "src"
ARCHIVE = Path(
    r"C:\Users\perez\OneDrive\_High Archive\_High Archive - Personal"
    r"\Documents\Roberto\Creaciones\Symbulator\Websites\2023 Website\circuit")

CODE = re.compile(r"^(?P<book>[a-z]+\d*?)(?P<kind>[a-z]+)(?P<num>\d{3,})(?P<tail>[a-z]?)$")


def parse(stem: str):
    m = CODE.match(stem.lower())
    if not m:
        return None
    d = m.groupdict()
    return d["book"], d["kind"], d["num"].lstrip("0") or "0", d["tail"]


def build_index() -> dict:
    index: dict = {}
    if not ARCHIVE.is_dir():
        sys.exit(f"The 2023 archive is not where this script expects it:\n"
                 f"  {ARCHIVE}\n"
                 f"Point ARCHIVE at it, or mount the drive.")
    for f in ARCHIVE.iterdir():
        if not f.is_file() or f.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        p = parse(f.stem)
        if p:
            index.setdefault((p[0], p[2], p[3]), []).append((p[1], f))
    return index


def match(stem: str, index: dict):
    p = parse(stem)
    if not p:
        return None
    book, kind, num, tail = p
    cands = index.get((book, num, tail), [])
    compat = [(k, f) for k, f in cands if k.startswith(kind) or kind.startswith(k)]
    pick = compat or cands
    return pick[0][1] if len(pick) == 1 else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--skip", action="append", default=[],
                    metavar="FILE", help="a src file to leave alone")
    args = ap.parse_args()

    index = build_index()
    stems = sorted({Path(f).stem for f in glob.glob(str(CIRCUIT / "*.svg"))})

    copied, unmatched = [], []
    for stem in stems:
        orig = match(stem, index)
        if orig is None:
            unmatched.append(stem)
            continue
        dest = CIRCUIT / (stem + orig.suffix.lower())
        copied.append((stem, orig, dest))
        if args.apply:
            shutil.copy2(orig, dest)

    print(f"{len(copied)} figure(s) matched, {len(unmatched)} not")
    for stem, orig, dest in copied:
        print(f"   {stem:14} <- {orig.name:20} -> {dest.name}")
    for stem in unmatched:
        print(f"   {stem:14} NOT FOUND in the archive")

    # --- rewrite the references -------------------------------------------
    ext = {stem: dest.suffix for stem, _, dest in copied}
    touched = 0
    for md in sorted(SRC.glob("*.md")):
        if md.name in args.skip:
            continue
        text = md.read_text(encoding="utf-8")
        new = text
        for stem, suffix in ext.items():
            new = new.replace(f"assets/circuit/{stem}.svg",
                              f"assets/circuit/{stem}{suffix}")
        if new != text:
            touched += 1
            n = sum(text.count(f"assets/circuit/{s}.svg") for s in ext)
            print(f"   {md.name}: {n} reference(s) repointed")
            if args.apply:
                md.write_text(new, encoding="utf-8", newline="\n")

    if args.skip:
        print(f"\nskipped: {', '.join(args.skip)}")
        for name in args.skip:
            p = SRC / name
            if not p.is_file():
                continue
            left = [s for s in ext if f"assets/circuit/{s}.svg" in p.read_text(encoding="utf-8")]
            for s in left:
                print(f"   {name} still points at assets/circuit/{s}.svg "
                      f"-- change to {s}{ext[s]}")

    print(f"\n{'APPLIED' if args.apply else 'DRY RUN'}: "
          f"{len(copied)} image(s), {touched} chapter(s)")
    if not args.apply:
        print("Nothing written. Re-run with --apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
