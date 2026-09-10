"""Carve embedded PNGs out of a Word 97 .doc Data stream.

A PNG runs from the 8-byte signature to the end of the IEND chunk, so the
extent is exact and no guessing is involved -- each carved blob is then
re-opened with PIL, which fails loudly on a bad carve.
"""
import os
import sys

import olefile

try:
    from PIL import Image
except ImportError:
    Image = None

SIG = b"\x89PNG\r\n\x1a\n"
IEND = b"IEND\xae\x42\x60\x82"

THESIS = (r"C:\Users\perez\Claude Symbulator\Documentation\paper"
          r"\references\2000_thesis")


def carve(doc_path, out_dir=None):
    f = olefile.OleFileIO(doc_path)
    if not f.exists("Data"):
        return []
    data = f.openstream("Data").read()
    out, i, n = [], 0, 0
    while True:
        i = data.find(SIG, i)
        if i < 0:
            break
        j = data.find(IEND, i)
        if j < 0:
            break
        blob = data[i:j + len(IEND)]
        n += 1
        size = None
        if Image is not None:
            import io as _io
            try:
                im = Image.open(_io.BytesIO(blob))
                im.load()
                size = im.size
            except Exception as exc:                       # bad carve
                size = f"UNREADABLE {exc}"
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            stem = os.path.splitext(os.path.basename(doc_path))[0]
            p = os.path.join(out_dir, f"{stem}_{n:02d}.png")
            open(p, "wb").write(blob)
        out.append((n, len(blob), size))
        i = j
    return out


if __name__ == "__main__":
    docs = sys.argv[1:] or ["02_cap_02.doc"]
    for d in docs:
        path = os.path.join(THESIS, d)
        res = carve(path)
        print(f"== {d}: {len(res)} PNG(s)")
        for n, ln, size in res[:40]:
            print(f"   {n:02d}  {ln:>8} b  {size}")
