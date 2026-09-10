"""Put the thesis's figures into the Book itself, permanently.

The Book is the English edition of the 2001 thesis, and until now it
carried no figures at all -- deliberately, and its own Note on this
Edition said so. Roberto's decision of 10 Sep 2026 reverses that: the
figures are recovered from the original Word chapters and printed where
the text refers to them.

This edits the *source*, not a copy. Uploading a rebuilt PDF alone would
have been undone by the next `xelatex the_symbulator_book.tex`, since
`build.py` copies `paper/the_symbulator_book.pdf` to the site as
`book.pdf` -- the generated-files-are-not-source trap.

Idempotent: it refuses to run twice.

    py illustrate_book.py
"""
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.dirname(HERE)
BOOK_TEX = os.path.join(PAPER, "the_symbulator_book.tex")
BOOK_DIR = os.path.join(PAPER, "book")
FIG_DIR = os.path.join(PAPER, "book_figures")

sys.path.insert(0, HERE)
from build_thesis_pdfs import (english_caption, figure_index,   # noqa: E402
                               tex_width, PROBLEM, STATEMENT_END)

MARKER = "% figures added 10 Sep 2026"

OLD_NOTE = """Three editorial notes. First, the figures of the original---TI-89
screen captures and circuit drawings---are not reproduced in this
edition; every problem's circuit is fully defined by the circuit
description given in its solution, and the original figures survive
in the archived thesis."""

NEW_NOTE = """Three editorial notes. First, the figures of the original---TI-89
screen captures and circuit drawings---are reproduced in this edition.
They were recovered in 2026 from the original Word chapters of the
thesis, where they had lain embedded since 2001, and each is printed
with the problem whose circuit it shows. Earlier printings of this
translation carried none, on the reasoning that every problem's circuit
is fully defined by the circuit description given in its solution; that
is true, and the figures are still worth having. Five problems have no
figure because the thesis itself says they have none."""


def main():
    main_tex = io.open(BOOK_TEX, encoding="utf-8").read()
    if MARKER in main_tex:
        raise SystemExit("already illustrated -- nothing to do")

    figs = figure_index()
    os.makedirs(FIG_DIR, exist_ok=True)

    # ---- the figure files, into the repository ----------------------
    placed, unknown = {}, []
    for num, items in sorted(figs.items()):
        for k, (cap, pic) in enumerate(items):
            src = pic["file"]
            if not os.path.isabs(src):
                src = os.path.join(HERE, src)
            dest = f"p{num}_{k}.png"
            shutil.copyfile(src, os.path.join(FIG_DIR, dest))
            eng = english_caption(cap["text"])
            if eng is None:
                unknown.append((num, cap["text"]))
                eng = f"Figure for Problem {num}"
            placed.setdefault(num, []).append(
                (dest, tex_width(pic["size"][0]), eng))

    # ---- the chapters ------------------------------------------------
    touched = 0
    for fn in sorted(os.listdir(BOOK_DIR)):
        if not fn.endswith(".tex"):
            continue
        path = os.path.join(BOOK_DIR, fn)
        text = io.open(path, encoding="utf-8").read()
        if MARKER in text:
            continue
        new = inject(text, placed)
        if new != text:
            io.open(path, "w", encoding="utf-8").write(new)
            touched += 1

    # ---- the main file ------------------------------------------------
    if main_tex.count(OLD_NOTE) != 1:
        raise SystemExit("the editorial note is not as expected; stopping "
                         "rather than leaving the book contradicting itself")
    main_tex = main_tex.replace(OLD_NOTE, NEW_NOTE, 1)
    main_tex = main_tex.replace(
        r"\usepackage{booktabs}",
        MARKER + "\n\\usepackage{graphicx}\n\\usepackage{caption}\n"
        "\\usepackage{booktabs}", 1)
    io.open(BOOK_TEX, "w", encoding="utf-8").write(main_tex)

    total = sum(len(v) for v in placed.values())
    print(f"{total} figures into {FIG_DIR}")
    print(f"{touched} chapter file(s) edited; editorial note rewritten")
    for num, text in unknown:
        print(f"  ! {num}: caption not recognised: {text[:60]}")
    return 0


def inject(text, placed):
    marks = list(PROBLEM.finditer(text))
    if not marks:
        return text
    pieces, last = [], 0
    for k, m in enumerate(marks):
        num = m.group(1)
        end = marks[k + 1].start() if k + 1 < len(marks) else len(text)
        body = text[m.start():end]
        block = ""
        for dest, w_mm, caption in placed.get(num, []):
            block += (f"\n{MARKER}\n\\begin{{figure}}[!ht]\n\\centering\n"
                      f"\\includegraphics[width={w_mm:.0f}mm]"
                      f"{{book_figures/{dest}}}\n"
                      f"\\caption*{{{caption}}}\n\\end{{figure}}\n")
        if block:
            m2 = STATEMENT_END.search(body)
            body = (body[:m2.end()] + block + "\n" + body[m2.end():]
                    if m2 else body + block)
        pieces.append(text[last:m.start()])
        pieces.append(body)
        last = end
    pieces.append(text[last:])
    return "".join(pieces)


if __name__ == "__main__":
    sys.exit(main())
