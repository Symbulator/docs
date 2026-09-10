"""Check each built edition for what it is supposed to differ in.

Written after a first version that could not fail: it counted raster
images (so the vector-drawn `compare` edition reported zero) and searched
the whole document for "sq\\" (so every edition reported the old notation,
since entries with no quoted description are left alone in all three).
Each check below is keyed to one problem and one property, and the
expected answers differ between editions -- so a check that comes back
the same everywhere is itself the bug.
"""
import os
import re

from pypdf import PdfReader

ROOT = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "build_thesis")

EXPECT = {                    # edition -> (figures, problem-001 notation)
    "landing": ("word scans", "Q"),
    "antony":  ("word scans", "v9"),
    "compare": ("v9 drawings", "Q"),
}


def figure_count(reader):
    """Raster images *and* vector forms: the Word scans are PNGs, the
    version 9 drawings are vector PDFs, and only counting one kind makes
    the other edition look empty."""
    raster = forms = 0
    for page in reader.pages:
        try:
            raster += len(page.images)
        except Exception:
            pass
        try:
            xo = page["/Resources"]["/XObject"].get_object()
            forms += sum(1 for k in xo
                         if xo[k].get_object().get("/Subtype") == "/Form")
        except Exception:
            pass
    return raster, forms


def notation_of_001(tex_dir):
    """Read the generated source for Problem 001's entry: the Q form is
    one `sq\\dc("...")` line, the version 9 form is one element per line."""
    p = os.path.join(tex_dir, "book", "ch02.tex")
    t = open(p, encoding="utf-8").read()
    i = t.find("\\problem{001}")
    j = t.find("\\problem{002}")
    m = re.search(r"\\begin\{entry\}(.*?)\\end\{entry\}", t[i:j], re.S)
    if not m:
        return "none"
    body = m.group(1).strip()
    if body.startswith("sq\\"):
        return "Q"
    if re.match(r"^j1,0,1,3\.1\s*\nr1,1,0,2\s*\n", body):
        return "v9"
    return "other: " + body[:40]


print(f"{'edition':9} {'pages':>6} {'raster':>7} {'vector':>7}  "
      f"{'001 notation':>13}   verdict")
for name, (want_figs, want_note) in EXPECT.items():
    p = os.path.join(ROOT, name, "main.pdf")
    if not os.path.exists(p):
        print(f"{name:9} NOT BUILT")
        continue
    r = PdfReader(p)
    raster, forms = figure_count(r)
    note = notation_of_001(os.path.join(ROOT, name))
    if want_figs == "word scans":
        figs_ok = raster >= 90
    else:
        figs_ok = forms >= 80
    ok = figs_ok and note == want_note
    print(f"{name:9} {len(r.pages):>6} {raster:>7} {forms:>7}  "
          f"{note:>13}   {'ok' if ok else '** WRONG'}")
