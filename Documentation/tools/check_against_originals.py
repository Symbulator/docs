#!/usr/bin/env python3
"""Every printed answer, checked against Roberto's 2023 pages.

The current sources were converted from two hand-written HTML pages --
docs-page7.html and docs-page8.html -- and the conversion merged the two
into single ```out 7,8``` blocks. That merge is lossless only where the
two pages agreed. Where they did not, one version's answer was silently
given to both: AS7's Example 12.11 printed 1.36 angle -6.2 in page 7 and
the corrected -66.2 in page 8, and the merge reinstated the typo.

This checks the other direction -- that every answer now in src/ is one
the originals actually printed.

    py tools/check_against_originals.py [path to the 2023 Website folder]

Reported:

    not found     an out block whose text is in neither original
    v7 only       matches page 7 but not page 8 -- check page 8 didn't
                  correct it, as it did for 12.11
"""
import glob
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")

DEFAULT_ORIGINALS = os.path.join(
    os.path.expanduser("~"),
    "OneDrive", "_High Archive", "_High Archive - Personal", "Documents",
    "Roberto", "Creaciones", "Symbulator", "Websites", "2023 Website")

FENCE = re.compile(r"^```([^\n]*)\n(.*?)^```", re.M | re.S)


def flatten(text: str) -> str:
    """One long line, with the book's three minus signs made one."""
    text = text.replace("–", "-").replace("−", "-")
    # The originals write 16122.*𝐢 where the sources write 16122.𝐢, and
    # neither spelling is more correct than the other.
    text = text.replace("*", "")
    # The originals join code lines with colons where the sources
    # use newlines, and a description separates elements the same
    # way, so colons carry no information once whitespace is gone.
    text = text.replace(":", "")
    return re.sub(r"\s+", "", text)


def page_text(path: str) -> str:
    raw = open(path, encoding="utf-8", errors="replace").read()
    return flatten(html.unescape(re.sub(r"<[^>]+>", " ", raw)))


def check(folder: str):
    pages = {}
    for v in ("7", "8"):
        p = os.path.join(folder, f"docs-page{v}.html")
        if not os.path.exists(p):
            print(f"cannot find {p}")
            return None
        pages[v] = page_text(p)

    rows, ok = [], 0
    for path in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        name = os.path.basename(path)
        text = open(path, encoding="utf-8").read()
        for info, block in FENCE.findall(text):
            kind = info.split()
            # Answers only. Code blocks were tried and abandoned: the
            # originals interleave code with prose and the conversion
            # regrouped it, so a line-by-line comparison reports
            # hundreds of differences that are reformatting, not
            # drift -- noise that would bury the real findings.
            if not kind or kind[0] != "out":
                continue
            vers = "".join(kind[1:])
            # Line by line: the originals interleave code fragments with
            # prose, so a whole block rarely appears contiguously even when
            # every line of it is verbatim.
            for line in block.splitlines():
                needle = flatten(line)
                if len(needle) < 6:
                    continue
                for v in ("7", "8"):
                    if v not in vers:
                        continue
                    if needle in pages[v]:
                        ok += 1
                    else:
                        rows.append((name, v, kind[0], line.strip()))
    return ok, rows


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    folder = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ORIGINALS
    got = check(folder)
    if got is None:
        sys.exit(2)
    ok, rows = got

    by_kind = {}
    for name, v, kind, block in rows:
        by_kind.setdefault(kind, []).append((name, v, block))

    for kind in ("sym", "out"):
        got_rows = by_kind.get(kind, [])
        if not got_rows:
            continue
        label = ("CODE BLOCKS" if kind == "sym" else "PRINTED ANSWERS")
        print()
        print(f"{label} NOT FOUND IN THAT VERSION'S OWN PAGE"
              f"  ({len(got_rows)})")
        print("=" * 68)
        for name, v, block in got_rows:
            first = block.splitlines()[0] if block.splitlines() else ""
            print(f"  v{v}  {name:26} {first[:80]}")

    print()
    print(f"{ok} block(s) verified against the originals, "
          f"{len(rows)} not found")
    sys.exit(1 if rows else 0)
