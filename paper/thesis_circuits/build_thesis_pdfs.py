"""Build the variant editions of the 2001 thesis.

Since #365 the Book itself carries the thesis's figures (see
`illustrate_book.py`), so the *canonical* build -- plain `xelatex
the_symbulator_book.tex` -- is the illustrated edition that the site
serves as `book.pdf`. This script builds the two editions that differ
from it:

    variant   figures                     circuit descriptions
    -------   -------------------------   --------------------------
    antony    the 2001 Word scans         converted to Symbulator 9
    compare   drawn by the v9 engine      as the thesis wrote them

Both start from the canonical chapters and change one axis each, so
neither can drift from the Book's own text.

Run `carve_png.py` first (the scans) and, for `compare`, `render_v9.py`
(the drawings); neither output is committed.

    py build_thesis_pdfs.py [variant ...]      (default: both)
"""
import io
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.dirname(HERE)
BOOK_TEX = os.path.join(PAPER, "the_symbulator_book.tex")
BOOK_DIR = os.path.join(PAPER, "book")
BOOK_FIGS = os.path.join(PAPER, "book_figures")
OUT_ROOT = os.path.join(PAPER, "build_thesis")

sys.path.insert(0, HERE)
from parse_book import parse                             # noqa: E402
from to_v9 import convert                                # noqa: E402

PROBLEM = re.compile(r"\\problem\{(\d{3})\}")
ENTRY_BLOCK = re.compile(r"\\begin\{entry\}\s*\n(.*?)\n\\end\{entry\}", re.S)
FIGURE = re.compile(
    r"\n?% figures added [^\n]*\n\\begin\{figure\}.*?\\end\{figure\}\n",
    re.S)
INCLUDE = re.compile(r"\\includegraphics\[[^\]]*\]\{book_figures/([^}]+)\}")

VARIANTS = {
    "antony":  dict(figures="word", descriptions="v9"),
    "compare": dict(figures="v9",   descriptions="original"),
}

NOTE = {
    "antony": r"""
\chapter*{About this printing}
\addcontentsline{toc}{chapter}{About this printing}
This printing carries the circuit figures of the 2001 thesis, as the
published edition does, and in addition every circuit description has
been converted from the notation of Symbulator~Q to that of
Symbulator~9: one element per line, the row padding dropped, the
square-root glyph spelled \texttt{sqrt}, and a two-port's parameters
written in the description rather than stored in calculator variables
beforehand. The narrative is the 2001 text and still describes the
calculator of its day, so where it says \code{sq\char`\\dc} the
description printed beneath it is the modern one. Five problems have no
figure because the thesis says they have none, and two circuits
(Problems 066 and 074) are worked without a simulation at all.

Prepared for Antony Garc\'ia, to be read as a source of circuits rather
than as the book: the published edition is at
\texttt{learn.symbulator.com/book.pdf}.
""",
    "compare": r"""
\chapter*{About this printing}
\addcontentsline{toc}{chapter}{About this printing}
In this printing every circuit is drawn afresh by the schematic engine of
Symbulator~9, from the thesis's own description of it, in place of the
2001 figure. The text and the circuit descriptions are unchanged. It is
meant to be read beside the published edition, which carries the original
figures: the two show the same circuits, drawn twenty-five years apart.
""",
}


def v9_descriptions():
    """problem number -> its description in version 9 notation."""
    out = {}
    for p in parse():
        if not p["netlists"]:
            continue
        tool, desc, rest = p["netlists"][0]
        c = convert(tool, desc, rest, stores=p.get("stores"))
        if c["desc"]:
            out[p["num"]] = c["desc"]
    return out


def rewrite_entries(body, v9):
    def one(m):
        sq = re.search(r'sq\\(\w+)\("([^"]*)"', m.group(1))
        if not sq or not v9:
            return m.group(0)
        return "\\begin{entry}\n" + v9 + "\n\\end{entry}"
    return ENTRY_BLOCK.sub(one, body)


def swap_figures(body, num, drawn):
    """Replace the problem's Word scans with the v9 drawing: the first
    include becomes the drawing, any further ones are dropped."""
    if num not in drawn:
        return FIGURE.sub("", body)
    seen = {"n": 0}

    def one(m):
        seen["n"] += 1
        if seen["n"] > 1:
            return ""
        return m.group(0).replace(
            m.group(0)[m.group(0).index("\\includegraphics"):
                       m.group(0).index("}\n\\caption") + 1],
            "\\includegraphics[width=120mm]{figs/%s}" % drawn[num])
    return FIGURE.sub(one, body)


def build(name):
    cfg = VARIANTS[name]
    out = os.path.join(OUT_ROOT, name)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(os.path.join(out, "book"), exist_ok=True)

    if cfg["figures"] == "word":
        shutil.copytree(BOOK_FIGS, os.path.join(out, "book_figures"))
        drawn = {}
    else:
        figs = os.path.join(out, "figs")
        os.makedirs(figs, exist_ok=True)
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPDF
        sys.path.insert(0, PAPER)
        from render_exemplars import flatten_for_svglib, register_fonts
        register_fonts()
        drawn = {}
        for fn in sorted(os.listdir(os.path.join(HERE, "v9_svg"))):
            num = fn[1:4]
            svg = io.open(os.path.join(HERE, "v9_svg", fn),
                          encoding="utf-8").read()
            flat = os.path.join(figs, "_f.svg")
            io.open(flat, "w", encoding="utf-8").write(
                flatten_for_svglib(svg))
            renderPDF.drawToFile(svg2rlg(flat), os.path.join(figs, num + ".pdf"))
            os.remove(flat)
            drawn[num] = num + ".pdf"

    v9 = v9_descriptions() if cfg["descriptions"] == "v9" else {}

    for fn in sorted(os.listdir(BOOK_DIR)):
        if not fn.endswith(".tex"):
            continue
        text = io.open(os.path.join(BOOK_DIR, fn), encoding="utf-8").read()
        marks = list(PROBLEM.finditer(text))
        if marks:
            pieces, last = [], 0
            for k, m in enumerate(marks):
                num = m.group(1)
                end = (marks[k + 1].start() if k + 1 < len(marks)
                       else len(text))
                body = text[m.start():end]
                if cfg["descriptions"] == "v9":
                    body = rewrite_entries(body, v9.get(num))
                if cfg["figures"] == "v9":
                    body = swap_figures(body, num, drawn)
                pieces.append(text[last:m.start()])
                pieces.append(body)
                last = end
            pieces.append(text[last:])
            text = "".join(pieces)
        elif cfg["figures"] == "v9":
            text = FIGURE.sub("", text)
        io.open(os.path.join(out, "book", fn), "w",
                encoding="utf-8").write(text)

    main = io.open(BOOK_TEX, encoding="utf-8").read()
    main = main.replace(r"\input{book/ch01}",
                        NOTE[name].strip() + "\n\n" + r"\input{book/ch01}", 1)
    io.open(os.path.join(out, "main.tex"), "w", encoding="utf-8").write(main)
    return out


def run_xelatex(out):
    for i in range(2):
        r = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error",
             "main.tex"], cwd=out, capture_output=True, text=True,
            errors="replace")
        if r.returncode != 0:
            print("\n".join(r.stdout.strip().splitlines()[-20:]))
            return None
    pdf = os.path.join(out, "main.pdf")
    return pdf if os.path.exists(pdf) else None


def main():
    for name in (sys.argv[1:] or list(VARIANTS)):
        print(f"=== {name} ===")
        out = build(name)
        pdf = run_xelatex(out)
        print(f"  {pdf}  {os.path.getsize(pdf):,} bytes" if pdf
              else "  no PDF produced")
    return 0


if __name__ == "__main__":
    sys.exit(main())
