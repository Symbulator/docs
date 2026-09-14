# -*- coding: utf-8 -*-
"""Crop each selected problem's schematic out of the book's PDF into the docs assets."""
import sys, os, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import figlib, specs, fmt
from PIL import Image

# --- paths, resolved from this file rather than hardcoded -------------------
# tools/<book> -> tools -> Documentation -> the project root. This file
# lives in tools/sampler and runs through the shim of the same name in
# each book's folder, so __file__ -- and so _HERE -- is that folder.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
DOCS = os.path.join(_ROOT, "Documentation")
EXAMPLES = os.path.join(_ROOT, "Application", "v9", "repos", "server", "examples")
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import book                                                   # noqa: E402
PDF = os.path.join(_ROOT, "Other", book.PDF)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

OUT = os.path.join(DOCS, "assets", "circuit")
MAXW = 1000
done, rows = {}, []
for sp in specs.SPECS:
    name = fmt.figname(sp["num"])
    pg, fn = sp["fig"]
    if name in done:
        rows.append((sp["num"], name, "(shared with %s)" % done[name])); continue
    path = os.path.join(OUT, name)
    # a spec may give the crop itself, in PDF points on the figure's page,
    # where the caption-and-ink detector picks the wrong box
    box, cap = figlib.save(pg, fn, path, dpi=300, rect=sp.get("figrect"))
    if box is None:
        print("!! MISS", sp["num"], pg, fn); continue
    im = Image.open(path)
    if im.width > MAXW:
        im = im.resize((MAXW, int(im.height * MAXW / im.width)), Image.LANCZOS)
        im.save(path, "JPEG", quality=90, optimize=True)
    done[name] = sp["num"]
    rows.append((sp["num"], name, "%dx%d  %dKB  Fig %s p%d" %
                 (im.width, im.height, os.path.getsize(path)//1024, fn, pg)))
for n, f, info in rows: print("%-7s %-18s %s" % (n, f, info))
print("\n%d files written, %d entries" % (len(done), len(rows)))
