# -*- coding: utf-8 -*-
"""Crop each selected example's schematic out of NR12.pdf into the docs assets."""
import sys, os, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import figlib, specs
from PIL import Image

# --- paths, resolved from this file rather than hardcoded -------------------
# tools/nr12 -> tools -> Documentation -> the project root.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
DOCS = os.path.join(_ROOT, "Documentation")
EXAMPLES = os.path.join(_ROOT, "Application", "v9", "repos", "server", "examples")
PDF = os.path.join(_ROOT, "Other", "NR12.pdf")
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

OUT = os.path.join(DOCS, "assets", "circuit")
MAXW = 1000
done, rows = {}, []
for sp in specs.SPECS:
    base = re.match(r"(\d+)\.(\d+)", sp["num"])
    name = "nr12-ex%s-%s.jpg" % (base.group(1), base.group(2))
    pg, fn = sp["fig"]
    if name in done:
        rows.append((sp["num"], name, "(shared with %s)" % done[name])); continue
    path = os.path.join(OUT, name)
    box, cap = figlib.save(pg, fn, path, dpi=300)
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
