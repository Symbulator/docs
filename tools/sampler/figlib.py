import sys
import os
# -*- coding: utf-8 -*-
"""Find and crop a labelled figure ('Figure 4.10 ...') out of the book's PDF."""
import re, pymupdf

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

_doc = None
def doc():
    global _doc
    if _doc is None: _doc = pymupdf.open(PDF)
    return _doc

CAP = re.compile(book.CAPTION_RE)

def captions(pageno):
    p = doc()[pageno-1]
    out = []
    for b in p.get_text("blocks"):
        t = b[4].replace("\xa0", " ").strip()
        m = CAP.match(t)
        if m:
            out.append(("%s.%s" % (m.group(1), m.group(2)),
                        pymupdf.Rect(b[:4]), re.sub(r"\s+", " ", t)))
    return out

def _drawings(p):
    out = []
    for d in p.get_drawings():
        r = pymupdf.Rect(d["rect"])
        if r.width < 0.2 and r.height < 0.2: continue
        if r.width > 545 or r.height > 620: continue       # page furniture
        # a wide, short filled band is a section/equation box, not circuit ink
        out.append(r)
    for img in p.get_image_info():
        out.append(pymupdf.Rect(img["bbox"]))
    return out

def _texts(p):
    out = []
    for b in p.get_text("blocks"):
        t = b[4].replace("\xa0", " ").strip()
        if not t: continue
        out.append((pymupdf.Rect(b[:4]), t))
    return out

def figure_rect(pageno, fignum, gap=24, xpad=16, maxh=380):
    p = doc()[pageno-1]
    caps = [c for c in captions(pageno) if c[0] == fignum]
    if not caps: return None, None
    _, crect, ctext = caps[0]
    cx0, cx1 = crect.x0 - xpad, crect.x1 + xpad
    floor = 0.0
    for fn, r, _t in captions(pageno):
        if r.y1 <= crect.y0 - 1 and not (r.x1 < cx0 or r.x0 > cx1):
            floor = max(floor, r.y1)
    # 1. cluster vector ink upward from the caption
    ink = []
    for r in _drawings(p):
        if r.y1 > crect.y0 + 2 or r.y0 < floor - 0.5: continue
        cxm = (r.x0 + r.x1) / 2
        if cxm < cx0 - 6 or cxm > cx1 + 6: continue
        ink.append(r)
    if not ink: return None, ctext
    ink.sort(key=lambda r: -r.y1)
    box = pymupdf.Rect(ink[0])
    for r in ink[1:]:
        if box.y0 - r.y1 > gap: break
        if (r | box).height > maxh: break
        box |= r
    # 2. pull in short text labels that touch the ink cluster
    grow = pymupdf.Rect(box.x0-16, box.y0-14, box.x1+16, box.y1+8)
    for r, t in _texts(p):
        if len(t) > 90 or t == ctext: continue
        if r.y1 > crect.y0 + 2 or r.y0 < floor - 0.5: continue
        if r.intersects(grow):
            nb = box | r
            if nb.height <= maxh + 26 and nb.width <= 560: box = nb
    return box, ctext

def save(pageno, fignum, path, dpi=400, pad=7, rect=None):
    p = doc()[pageno-1]
    if rect is not None: box, ctext = pymupdf.Rect(rect), None
    else: box, ctext = figure_rect(pageno, fignum)
    if box is None: return None, ctext
    box = pymupdf.Rect(box.x0-pad, box.y0-pad, box.x1+pad, box.y1+pad) & p.rect
    pix = p.get_pixmap(clip=box, dpi=dpi, colorspace=pymupdf.csRGB)
    if path.lower().endswith((".jpg", ".jpeg")):
        from PIL import Image
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        bg = Image.new("RGB", im.size, "white"); bg.paste(im)
        bg.save(path, "JPEG", quality=92, optimize=True)
    else:
        pix.save(path)
    return box, ctext
