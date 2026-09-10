"""Build the three illustrated editions of the 2001 thesis.

The Book (../the_symbulator_book.tex + ../book/ch*.tex) is the English
translation of the thesis, and it has never carried a single figure --
zero \\includegraphics across all thirteen files -- while its text says
"shown in the figure" throughout. The figures exist: they are embedded in
the original Word chapters, and `carve_png.py` recovers them.

Three editions, differing in two axes only:

    variant   figures                     circuit descriptions
    -------   -------------------------   --------------------------
    antony    the 2001 Word scans         converted to Symbulator 9
    landing   the 2001 Word scans         as the thesis wrote them
    compare   drawn by the v9 engine      as the thesis wrote them

`landing` is the one that replaces book.pdf on the site. `compare` puts
the version 9 schematic engine's drawing where the 2001 scan would be, so
the two can be read against each other.

    py build_thesis_pdfs.py [variant ...]      (default: all three)
"""
import io
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.dirname(HERE)                       # Documentation/paper
BOOK_TEX = os.path.join(PAPER, "the_symbulator_book.tex")
BOOK_DIR = os.path.join(PAPER, "book")
OUT_ROOT = os.path.join(PAPER, "build_thesis")

sys.path.insert(0, HERE)
from pair_figures import all_chapters, pair          # noqa: E402
from parse_book import parse                         # noqa: E402
from to_v9 import convert                            # noqa: E402

PROBLEM = re.compile(r"\\problem\{(\d{3})\}")
STATEMENT_END = re.compile(r"(\\emph\{Problem:.*?\}\s*?\n)\s*?\n", re.S)
ENTRY_BLOCK = re.compile(r"\\begin\{entry\}\s*\n(.*?)\n\\end\{entry\}", re.S)

#: The thesis has six caption shapes in all; each is translated, and an
#: unrecognised one is reported rather than guessed at.
CAPTIONS = [
    (re.compile(r"^Circuitosimplificadoparael[Pp]roblemaN.{0,3}?(\d{3})$"),
     "Simplified circuit for Problem {n}"),
    (re.compile(r"^Circuitoparael[Pp]roblemaN.{0,3}?(\d{3})$"),
     "Circuit for Problem {n}"),
    (re.compile(r"^Gr.ficasolicitadaporlapregunta([cd])\)del[Pp]roblemaN.{0,3}?(\d{3})$"),
     "Graph requested by part ({a}) of Problem {n}"),
    (re.compile(r"^Ordendel[Pp]roblemaN.{0,3}?(\d{3}),enlaTI-89$"),
     "The command for Problem {n}, on the TI-89"),
]

VARIANTS = {
    "antony":  dict(figures="word", descriptions="v9"),
    "landing": dict(figures="word", descriptions="original"),
    "compare": dict(figures="v9",   descriptions="original"),
}

NOTE = {
    "antony": r"""
\section*{Note on this edition}
This edition carries the circuit figures of the 2001 thesis, recovered
from the original Word chapters, and every circuit description has been
converted from the notation of Symbulator~Q to that of Symbulator~9.
The narrative is the 2001 text and still describes the calculator of its
day; where it says \code{sq\char`\\dc}, the description printed beneath
it is the modern one. Prepared for Antony Garc\'ia.
""",
    "landing": r"""
\section*{Note on this edition}
This edition adds the circuit figures of the 2001 thesis, recovered from
the original Word chapters. Earlier printings of this translation carried
none, although the text refers to them throughout. Nothing else has been
changed: the circuit descriptions are as the thesis wrote them, in the
notation of Symbulator~Q.
""",
    "compare": r"""
\section*{Note on this edition}
In this edition every circuit is drawn afresh by the schematic engine of
Symbulator~9, from the thesis's own description of it, in place of the
2001 figure. The text and the circuit descriptions are unchanged. It is
meant to be read beside the edition that carries the original figures:
the two show the same circuits, drawn twenty-five years apart.
""",
}


def english_caption(text):
    for rx, tmpl in CAPTIONS:
        m = rx.match(text)
        if m:
            g = m.groups()
            if len(g) == 2:
                return tmpl.format(a=g[0], n=g[1])
            return tmpl.format(n=g[0])
    return None


def figure_index():
    """problem number -> [(caption text, picture dict), ...] in order."""
    figs = {}
    for stem in all_chapters():
        _pairs, problems, _left = pair(stem)
        for num, cap, pic in problems:
            if pic is not None:
                figs.setdefault(num, []).append((cap, pic))
    return figs


def tex_width(px, cap_mm=150.0, mm_per_px=0.34):
    """A scan is small and low-resolution; printed at its nominal size it
    is unreadable, so it is enlarged to a fixed millimetres-per-pixel and
    then capped at the text width."""
    return min(px * mm_per_px, cap_mm)


def build_variant(name, log):
    cfg = VARIANTS[name]
    out = os.path.join(OUT_ROOT, name)
    figs_dir = os.path.join(out, "figs")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(figs_dir, exist_ok=True)

    figs = figure_index()
    probs = {p["num"]: p for p in parse()}

    # ---- figures on disk -------------------------------------------
    placed = {}
    if cfg["figures"] == "word":
        for num, items in figs.items():
            for k, (cap, pic) in enumerate(items):
                dest = f"p{num}_{k}.png"
                shutil.copyfile(os.path.join(HERE, pic["file"])
                                if not os.path.isabs(pic["file"])
                                else pic["file"],
                                os.path.join(figs_dir, dest))
                eng = english_caption(cap["text"])
                if eng is None:
                    log.append(f"  ! {num}: caption not recognised: "
                               f"{cap['text'][:60]}")
                    eng = f"Figure for Problem {num}"
                placed.setdefault(num, []).append(
                    (dest, tex_width(pic["size"][0]), eng))
    else:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPDF
        for num in sorted(probs):
            src = os.path.join(HERE, "v9_svg", f"p{num}.svg")
            if not os.path.exists(src):
                continue
            drawing = svg2rlg(src)
            dest = f"p{num}.pdf"
            renderPDF.drawToFile(drawing, os.path.join(figs_dir, dest))
            w_mm = min(drawing.width * 25.4 / 72.0 * 1.15, 150.0)
            placed[num] = [(dest, w_mm,
                            f"Circuit for Problem {num}, drawn by "
                            f"Symbulator 9")]

    # ---- chapters ---------------------------------------------------
    os.makedirs(os.path.join(out, "book"), exist_ok=True)
    for fn in sorted(os.listdir(BOOK_DIR)):
        if not fn.endswith(".tex"):
            continue
        text = io.open(os.path.join(BOOK_DIR, fn), encoding="utf-8").read()
        text = inject(text, placed, probs, cfg, log)
        io.open(os.path.join(out, "book", fn), "w",
                encoding="utf-8").write(text)

    # ---- main file --------------------------------------------------
    main = io.open(BOOK_TEX, encoding="utf-8").read()
    main = main.replace(
        r"\usepackage{booktabs}",
        "\\usepackage{graphicx}\n\\usepackage{caption}\n"
        "\\usepackage{booktabs}", 1)
    main = main.replace(r"\input{book/ch01}",
                        NOTE[name].strip() + "\n\n" + r"\input{book/ch01}", 1)
    io.open(os.path.join(out, "main.tex"), "w", encoding="utf-8").write(main)
    return out


def inject(text, placed, probs, cfg, log):
    """Put each problem's figures after its statement, and -- for the
    `antony` variant -- print its description in version 9 notation."""
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
            block += (f"\n\\begin{{figure}}[!ht]\n\\centering\n"
                      f"\\includegraphics[width={w_mm:.0f}mm]{{figs/{dest}}}\n"
                      f"\\caption*{{{caption}}}\n\\end{{figure}}\n")
        if block:
            m2 = STATEMENT_END.search(body)
            if m2:
                body = body[:m2.end()] + block + "\n" + body[m2.end():]
            else:
                body = body + block
                log.append(f"  ! {num}: no statement found; figure appended")

        if cfg["descriptions"] == "v9":
            body = rewrite_entries(body, probs.get(num), log, num)

        pieces.append(text[last:m.start()])
        pieces.append(body)
        last = end
    pieces.append(text[last:])
    return "".join(pieces)


def rewrite_entries(body, prob, log, num):
    """Replace a `sq\\tool("...")` entry with the version 9 description."""
    if prob is None:
        return body

    def one(m):
        inner = m.group(1)
        sq = re.search(r'sq\\(\w+)\("([^"]*)"([^)]*)\)', inner)
        if not sq:
            return m.group(0)
        c = convert(sq.group(1), sq.group(2), sq.group(3),
                    stores=prob.get("stores"))
        if not c["desc"]:
            return m.group(0)
        head = f"% Symbulator 9 -- analysis: {c['analysis']}"
        if c["args"]:
            head += f", at {c['args']}"
        return ("\\begin{entry}\n" + c["desc"] + "\n\\end{entry}")

    return ENTRY_BLOCK.sub(one, body)


def run_xelatex(out, log):
    for i in range(2):
        r = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error",
             "main.tex"],
            cwd=out, capture_output=True, text=True, errors="replace")
        if r.returncode != 0:
            tail = "\n".join(r.stdout.strip().splitlines()[-25:])
            log.append(f"  ** xelatex failed on pass {i + 1}:\n{tail}")
            return None
    pdf = os.path.join(out, "main.pdf")
    return pdf if os.path.exists(pdf) else None


def main():
    want = sys.argv[1:] or list(VARIANTS)
    os.makedirs(OUT_ROOT, exist_ok=True)
    for name in want:
        log = []
        print(f"=== {name} ===")
        out = build_variant(name, log)
        pdf = run_xelatex(out, log)
        for line in log:
            print(line)
        if pdf:
            print(f"  {pdf}  {os.path.getsize(pdf):,} bytes")
        else:
            print("  no PDF produced")
    return 0


if __name__ == "__main__":
    sys.exit(main())
