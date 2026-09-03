#!/usr/bin/env python3
"""
Draw a labelled placeholder for every figure the source refers to but which
does not exist yet, so the build stays green while the real schematics are
being prepared.

Always writes .svg (web) and .pdf (print). When the source refers to a raster
figure -- the imported practice problems all cite .jpg -- it writes that file
too, because the web build emits the referenced path verbatim and would
otherwise still 404 on it.

    python3 tools/make_placeholders.py

Delete a placeholder and drop the real artwork in its place; this script never
overwrites a file it did not create (it checks for the marker comment, which
is embedded in the SVG/PDF metadata and in the JPEG's comment segment).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import build as B                                            # noqa: E402

import matplotlib                                            # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                              # noqa: E402

MARKER = "symbulator-placeholder"


def wanted(book):
    out = []
    for ch in book.chapters:
        for b in B._all_blocks(ch.blocks):
            if b.kind == "figure":
                out.append((ch.id, b.arg, "".join(
                    n.text for n in B.parse_inline(
                        " ".join(c.text for c in b.children if c.kind == "para")))))
    return out


def draw(path, caption, chapter):
    fig, ax = plt.subplots(figsize=(6.0, 2.6))
    ax.set_axis_off()
    ax.add_patch(plt.Rectangle((0.01, 0.02), 0.98, 0.96, fill=False,
                               ec="#B7791F", lw=1.4, ls=(0, (6, 4))))
    ax.text(0.5, 0.62, caption or os.path.basename(path), ha="center",
            fontsize=12, color="#16181A")
    ax.text(0.5, 0.36, "figure to be supplied", ha="center", fontsize=9,
            color="#B7791F", style="italic")
    ax.text(0.5, 0.16, os.path.basename(path), ha="center", fontsize=7.5,
            color="#78848D", family="monospace")
    base, ext = os.path.splitext(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(base + ".svg", bbox_inches="tight", transparent=True,
                metadata={"Title": MARKER})
    fig.savefig(base + ".pdf", bbox_inches="tight", transparent=True,
                metadata={"Title": MARKER})
    # A raster reference needs the raster itself: build.py emits the figure
    # path exactly as the source wrote it, so a .jpg citation is only
    # satisfied by a .jpg on disk. No transparency here -- JPEG has no alpha
    # channel, and an unfilled one comes out black.
    if ext.lower() in (".jpg", ".jpeg", ".png"):
        pil_kwargs = {"comment": MARKER} if ext.lower() != ".png" else None
        fig.savefig(path, bbox_inches="tight", transparent=False,
                    facecolor="white",
                    **({"pil_kwargs": pil_kwargs} if pil_kwargs else
                       {"metadata": {"Software": MARKER}}))
    plt.close(fig)


def is_placeholder(path):
    """True if this file is one of ours. The marker sits in the SVG's
    metadata, the PDF's /Title and the JPEG's comment segment, all of which
    fall inside the first few kilobytes, so one text-ish read covers every
    format we write."""
    try:
        with open(path, "rb") as fh:
            return MARKER.encode() in fh.read(8192)
    except OSError:
        return False


if __name__ == "__main__":
    book = B.load_book()
    made = 0
    for chapter, rel, caption in wanted(book):
        path = os.path.join(B.ROOT, rel)
        if os.path.isfile(path) and not is_placeholder(path):
            continue
        draw(path, re.sub(r"\s+", " ", caption).strip(), chapter)
        made += 1
    print(f"placeholders: {made} drawn or refreshed")
