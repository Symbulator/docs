"""Fail if any PDF page carries text that does not actually render.

Born 29 Aug 2026: the A4 rebuild shipped four pages of the v9 book whose
text was painted white -- a breakable tcolorbox whose end coincided with a
page break leaked its fill colour (colback=white) into the ambient colour,
and every page after it that never issued its own \\color was blank while
its text layer was intact. Lessons 9 and 10 opened with invisible titles
and the credits went white from p255 to the end. XeLaTeX exits 0 for this;
the log is clean; only rendering shows it. Hence this check: render every
page at low resolution (pdftoppm, shipped with MiKTeX) and compare the ink
on the page against the length of its extracted text. A page with plenty
of text and almost no ink is invisible text, whatever the cause.

The class-level guard against the known leak is in symbulator.cls (the
\\color{ink} re-assertions after every box and at every chapter start);
this check is what proves the guard held, on every build, against causes
nobody has met yet.

Usage: check_white_text(pdf_path) -> list of bad page numbers, or run
  python tools/check_white_text.py build/pdf/symbulator-v9.pdf ...
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile


def check_white_text(pdf):
    """Page numbers (1-based) whose text layer far exceeds their ink."""
    try:
        import numpy as np
        from PIL import Image
        from pypdf import PdfReader
    except ImportError as e:                            # pragma: no cover
        print(f"check_white_text: SKIPPED ({e}); install pypdf, pillow, "
              f"numpy to enable it", file=sys.stderr)
        return []
    if not shutil.which("pdftoppm"):                    # pragma: no cover
        print("check_white_text: SKIPPED (no pdftoppm on PATH)",
              file=sys.stderr)
        return []
    reader = PdfReader(pdf)
    bad = []
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdftoppm", "-r", "20", "-gray", "-png", pdf,
                        os.path.join(td, "p")], check=True)
        for f in sorted(glob.glob(os.path.join(td, "p*.png"))):
            n = int(os.path.splitext(os.path.basename(f))[0][1:].lstrip("-"))
            img = np.asarray(Image.open(f).convert("L"))
            ink = int((img < 200).sum())
            try:
                txt = reader.pages[n - 1].extract_text() or ""
            except Exception:                           # noqa: BLE001
                txt = ""
            # A contents page defeats the ratio below honestly: its dot
            # leaders are hundreds of characters of text layer and almost
            # no ink, so a *sparse* contents page -- the last one, mostly
            # blank -- reads as a page of unpainted text. That refused the
            # Manual's PDF on a page that renders perfectly (#393). A
            # leader is not prose; collapse a run of three or more dots
            # before measuring. Narrowed here rather than by loosening the
            # threshold, which would blunt the guard on every page to fix
            # it on one.
            prose = re.sub(r"(?:\.\s*){3,}", " ", txt)
            # 20 dpi ink pixels run ~1-3x the character count on a normal
            # page; a page of text under 0.15x is not being painted.
            if len(prose) > 300 and ink < 0.15 * len(prose):
                bad.append(n)
    return bad


def main():
    failed = False
    for pdf in sys.argv[1:]:
        bad = check_white_text(pdf)
        name = os.path.basename(pdf)
        if bad:
            failed = True
            print(f"check_white_text: {name}: INVISIBLE TEXT on "
                  f"page(s) {bad}")
        else:
            print(f"check_white_text: {name}: clean")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
