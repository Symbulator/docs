"""Pair each carved image with its caption, by walking both sequences.

Word keeps pictures in the Data stream in document order and the .txt
extraction keeps captions in document order, so the two sequences agree.
They are not the same length -- some pictures carry no caption -- so
matching on counts alone shifts everything after the first extra picture.

What makes the walk safe is that the two kinds are distinguishable on
both sides:

  * a picture is a calculator *screen* (1-bit, and 59 of the 60 are
    exactly 160x100 plus a 2px frame) or a *drawing* (palette);
  * a caption names a screen ("Pantalla hogar", "Herramienta thevenin")
    or a circuit ("Circuito para el Problema N 001").

So a drawing caption takes the next drawing and a screen caption takes
the next screen. A caption that runs out of pictures of its kind, or a
picture left over at the end, is reported instead of being absorbed.
"""
import hashlib
import io
import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from carve_png import carve, THESIS                      # noqa: E402

#: Captions are matched against the chapter text with **all whitespace
#: removed**. The .doc extraction leaves long runs spaced out character by
#: character ("F i g u r a 4 1 ."), and a matcher written against the
#: spaced form silently finds nothing there -- which is how Problem 025's
#: figure came to be reported as absent when it is in the file (Roberto
#: asked why, 10 Sep 2026). Stripping whitespace first cannot be fooled by
#: the damage, because the damage is only ever added whitespace.
CAP = re.compile(r"Figura(\d{1,3})\.([^.]{0,90}?)\.")
PROB = re.compile(r"[Pp]roblemaN.{0,3}?(\d{3})")
#: Written without spaces: caption_kind() is fed the whitespace-stripped
#: text (see CAP above), so a multi-word marker like "tipo de" can never
#: match in its spaced form. Getting that wrong reads a calculator screen
#: as a circuit, and the screen then eats a drawing's slot and shifts
#: every figure after it in the chapter.
SCREEN_WORDS = ("pantalla", "herramienta", "entorno", "tipodered",
                "tipodeanalisis", "tipodeanálisis", "men", "editor",
                "ventana", "barra", "enlati-89", "enlati89")

PNG_DIR = "thesis_png"


def caption_kind(text):
    """A caption names a circuit drawing or a calculator screen.

    Listing the screen words was the wrong way round: they are open-ended
    ("Grafica solicitada...", "La exponencial se expande...", "Tipo de
    red...") and every one missed turns a screen into a drawing that then
    eats a circuit's slot. The circuit captions are the closed set -- the
    thesis calls a circuit figure "Circuito para el Problema N NNN", or
    "Circuito simplificado para..." -- so key on that and treat the rest
    as screens."""
    return "drawing" if "circuito" in text.lower() else "screen"


def chapter_captions(stem):
    raw = io.open(os.path.join(THESIS, stem + ".txt"),
                  encoding="utf-8", errors="replace").read()
    t = re.sub(r"\s+", "", raw)
    out, seen = [], set()
    for num, text in CAP.findall(t):
        key = (num, text.strip())
        if key in seen:                     # a caption echoed in the text
            continue
        seen.add(key)
        m = PROB.search(text)
        out.append(dict(fig=num, text=text.strip(), kind=caption_kind(text),
                        problem=m.group(1) if m else None))
    return out


def chapter_pictures(stem):
    """The chapter's pictures in document order, with a picture that
    merely repeats the one before it dropped.

    Word embeds a picture once per *appearance*, so a figure shown twice
    -- chapter 5's Figure 36 is in the file twice, byte for byte --
    arrives as two pictures under one caption. Left in, the repeat eats
    the next caption's slot and every figure after it in the chapter is
    one too early: that is what put Problem 020's circuit under Problem
    021 (Roberto, 10 Sep 2026, reading the comparison sheet). Identity is
    tested by hash, so this collapses a genuine repeat and never two
    figures that merely look alike."""
    out, last_hash = [], None
    for n, _ln, size in carve(os.path.join(THESIS, stem + ".doc")):
        if isinstance(size, str):
            continue
        p = os.path.join(PNG_DIR, f"{stem}_{n:02d}.png")
        digest = hashlib.sha256(open(p, "rb").read()).hexdigest()
        if digest == last_hash:
            continue                      # the same figure, shown again
        last_hash = digest
        im = Image.open(p)
        out.append(dict(n=n, file=p, size=im.size,
                        kind="screen" if im.mode == "1" else "drawing"))
    return out


def pair(stem):
    caps = chapter_captions(stem)
    pics = chapter_pictures(stem)
    queues = {"screen": [p for p in pics if p["kind"] == "screen"],
              "drawing": [p for p in pics if p["kind"] == "drawing"]}
    idx = {"screen": 0, "drawing": 0}
    pairs, problems = [], []
    for c in caps:
        q, i = queues[c["kind"]], idx[c["kind"]]
        pic = q[i] if i < len(q) else None
        idx[c["kind"]] += 1
        pairs.append((c, pic))
        if c["problem"]:
            problems.append((c["problem"], c, pic))
    leftovers = {k: len(queues[k]) - idx[k] for k in queues}
    return pairs, problems, leftovers


def all_chapters():
    stems = [os.path.splitext(d)[0] for d in sorted(os.listdir(THESIS))
             if d.endswith(".doc")]
    return [s for s in stems if os.path.exists(os.path.join(THESIS, s + ".txt"))
            and s != "00_paginas_iniciales"]


if __name__ == "__main__":
    total_probs = 0
    print(f"{'chapter':16} {'caps':>5} {'pics':>5} {'problems':>9} "
          f"{'unmatched caps':>15} {'left-over pics':>15}")
    for stem in all_chapters():
        pairs, problems, leftovers = pair(stem)
        missing = sum(1 for _c, p in pairs if p is None)
        left = sum(leftovers.values())
        total_probs += len(problems)
        flag = "" if (missing == 0 and left == 0) else "   <--"
        print(f"{stem:16} {len(pairs):>5} "
              f"{len(chapter_pictures(stem)):>5} {len(problems):>9} "
              f"{missing:>15} {left:>15}{flag}")
    print(f"\nproblem figures paired: {total_probs}")
