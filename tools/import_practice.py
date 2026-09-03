#!/usr/bin/env python3
"""
Convert a practice-problem .docx into the documentation's own markup.

The Word files carry real semantic styles, and this reads them rather than
guessing from appearance:

    Heading 2            the practice section title
    Heading 3            a group heading within it
    Heading 4            one problem
    CalcType             a line you type into the calculator   -> ```sym
    CalcTypeFree         the same, set full width              -> ```sym
    Calc-in-text (run)   something you type, inline            -> `code`
    Calc-out-text (run)  a value the software returned         -> {{o:...}}
    subscript/superscript runs                                 -> {{sub:}} {{sup:}}

Images are copied into assets/practice/ and named after the problem.

    python3 tools/import_practice.py lesson1.docx --version 7
    python3 tools/import_practice.py lesson1.docx --version 7 \
            --into src/01-lesson-dc.md

Without --into it prints the markup for you to inspect. With --into it
replaces that chapter's ::: practice block, keeping a .bak of the original.
"""

from __future__ import annotations

import argparse
import os
import re
import unicodedata
import shutil
import sys
import zipfile
from xml.etree import ElementTree as ET

try:
    from PIL import Image
except ImportError:                                   # figures kept as-is
    Image = None

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Word keeps the original scan resolution, which is far more than either output
# needs: at the width these print, 1100px is already about 400 dpi.
MAX_WIDTH = 1100
CODE_STYLES = {"CalcType", "CalcTypeFree"}
IN_RUN = "Calc-in-textChar"
OUT_RUN = "Calc-out-textChar"


# ---------------------------------------------------------------- reading --

# The OMML-to-markup renderer, borrowed rather than copied. It was
# written for restore_practice_answers.py, which put back the 57 answers
# this importer had dropped; keeping one copy means a fix to either
# reaches both. Safe to import: that module guards its own main.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from restore_practice_answers import render as render_omml  # noqa: E402


def paragraph_items(p):
    """(kind, element) for a paragraph's runs and equations, in order.

    Word stores an equation as an <m:oMath> subtree, not as a run of text.
    A walk that looks only for <w:r> therefore steps straight over it --
    silently, because the sentence introducing the answer is ordinary text
    and comes through fine. That is how 57 answers went missing, and why
    chapter 6 carried a bare `{ , , }`.

    Runs *inside* an equation are skipped: the equation is rendered whole,
    and picking its pieces up again would print them twice.
    """
    maths = list(p.iter(M + "oMath"))
    inside = {id(el) for m in maths for el in m.iter() if el is not m}
    emitted = set()
    for el in p.iter():
        if el.tag == M + "oMath":
            if id(el) not in emitted and id(el) not in inside:
                emitted.add(id(el))
                yield "math", el
        elif el.tag == W + "r" and id(el) not in inside:
            yield "run", el


def load(path):
    with zipfile.ZipFile(path) as z:
        doc = ET.fromstring(z.read("word/document.xml"))
        rels = ET.fromstring(z.read("word/_rels/document.xml.rels"))
        media = {n: z.read(n) for n in z.namelist() if n.startswith("word/media/")}
    target = {r.get("Id"): r.get("Target") for r in rels}
    return doc, target, media


def paragraphs(body):
    """Top-level paragraphs, in order, descending into tables but not into
    the copies Word keeps inside drawing fallbacks."""
    for child in body:
        if child.tag == f"{W}p":
            yield child
        elif child.tag == f"{W}tbl":
            for cell in child.iter(f"{W}tc"):
                for p in cell.findall(f"{W}p"):
                    yield p


# Word's invisible hyphens and breaks, which carry no <w:t> of their own
HYPHENS = {"\u00ad": "-", "\u2011": "-", "\u2010": "-", "\u2212": "-"}

# Word's autocorrect turns the calculator's straight quotes into curly ones.
# A curly quote is never valid input, so inside a command they are always wrong.
STRAIGHTEN = {"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"'}


def normalise(text: str) -> str:
    for bad, good in HYPHENS.items():
        text = text.replace(bad, good)
    return text


def run_text(r) -> str:
    """The text of a run, including the hyphens and breaks Word stores as
    elements rather than as characters."""
    out = []
    for node in r:
        if node.tag == f"{W}t":
            out.append(node.text or "")
        elif node.tag == f"{W}noBreakHyphen":
            out.append("-")
        elif node.tag == f"{W}tab":
            out.append(" ")
        elif node.tag in (f"{W}br", f"{W}cr"):
            out.append("\n")
    return normalise("".join(out))


def raw_text(p):
    return "".join(run_text(r) for r in p.iter(f"{W}r"))


def pstyle(p):
    node = p.find(f"{W}pPr/{W}pStyle")
    return node.get(f"{W}val") if node is not None else ""


def run_style(r):
    node = r.find(f"{W}rPr/{W}rStyle")
    return node.get(f"{W}val") if node is not None else ""


def vert_align(r):
    node = r.find(f"{W}rPr/{W}vertAlign")
    return node.get(f"{W}val") if node is not None else ""


def is_bold(r):
    return r.find(f"{W}rPr/{W}b") is not None


def is_italic(r):
    return r.find(f"{W}rPr/{W}i") is not None


def images_in(p, target):
    """Relationship ids of every image anchored in this paragraph."""
    out = []
    for blip in p.iter(f"{A}blip"):
        rid = blip.get(f"{R}embed")
        if rid and rid in target:
            out.append(target[rid])
    return out


# --------------------------------------------------------------- markup ----

def escape(text: str) -> str:
    """Neutralise characters the documentation markup would otherwise eat."""
    return text.replace("{{", "{ {").replace("*", r"\*")


def runs_to_markup(p) -> str:
    """Walk a paragraph's runs, merging neighbours that share a style."""
    pieces, prev, buf = [], None, ""

    def flush():
        nonlocal buf, prev
        if not buf:
            return
        text = buf
        if prev == IN_RUN:
            pieces.append(f"`{text}`")
        elif prev == OUT_RUN:
            pieces.append("{{o:" + text + "}}")
        elif prev == "sub":
            pieces.append("{{sub:" + text + "}}")
        elif prev == "sup":
            pieces.append("{{sup:" + text + "}}")
        elif prev == "b":
            pieces.append(f"**{escape(text)}**")
        elif prev == "i":
            pieces.append(f"*{escape(text)}*")
        else:
            pieces.append(escape(text))
        buf = ""

    for kind_, r in paragraph_items(p):
        if kind_ == "math":
            # An equation is one whole thing, so it interrupts whatever run
            # style was accumulating rather than joining it.
            flush()
            prev = None
            rendered = re.sub(r"\s+", " ", render_omml(r)).strip()
            if rendered:
                pieces.append(rendered)
            continue
        text = run_text(r)
        if not text:
            continue
        style = run_style(r)
        if not text.strip():
            kind = prev if prev in (None, "") else ""
        else:
            kind = None
        kind = kind if kind is not None else (style if style in (IN_RUN, OUT_RUN)
                else {"subscript": "sub", "superscript": "sup"}.get(vert_align(r))
                or ("b" if is_bold(r) and text.strip(".,;:()-")
                    else "i" if is_italic(r) else ""))
        if not text.strip():
            kind = ""
        if kind != prev:
            flush()
            prev = kind
        buf += text
    flush()
    return re.sub(r"[ \t]+", " ", "".join(pieces)).strip()


def wrap(text: str, width: int = 78, indent: str = "") -> str:
    words, lines, line = text.split(" "), [], indent
    for w in words:
        if len(line) + len(w) + 1 > width and line.strip():
            lines.append(line.rstrip())
            line = indent + w + " "
        else:
            line += w + " "
    if line.strip():
        lines.append(line.rstrip())
    return "\n".join(lines)


def shrink(path: str):
    """Downscale an oversized figure in place. Line art stays lossless."""
    if Image is None:
        return
    try:
        with Image.open(path) as im:
            if im.width <= MAX_WIDTH:
                return
            height = round(im.height * MAX_WIDTH / im.width)
            out = im.convert("RGB") if im.mode in ("P", "RGBA") else im.copy()
            out = out.resize((MAX_WIDTH, height), Image.LANCZOS)
            if path.lower().endswith(".png"):
                out.save(path, "PNG", optimize=True)
            else:
                out.save(path, "JPEG", quality=88, optimize=True,
                         progressive=True)
    except Exception as exc:                          # never fail the import
        print(f"  could not resize {os.path.basename(path)}: {exc}",
              file=sys.stderr)


def _ascii(s: str) -> str:
    r"""Fold accents away: "Thevenin" from "Thévenin".

    Python's \w is Unicode-aware, so the obvious slugify keeps "e-acute"
    and the name reaches a filename. That survives fine over SFTP, but it
    did not survive a ZIP unpacked by cPanel's extractor, which wrote the
    UTF-8 bytes out through a legacy code page and left junk twins of six
    figures on the live server. Slugs are ASCII from here on.
    """
    return "".join(c for c in unicodedata.normalize("NFKD", s)
                   if not unicodedata.combining(c))


def slugify(text: str) -> str:
    text = _ascii(text)
    text = re.sub(r"[^\w\s.-]", "", text, flags=re.ASCII).strip().lower()
    return re.sub(r"[\s_.]+", "-", text)


# -------------------------------------------------------------- converting --

def convert(path, version, media_dir, media_rel):
    doc, target, media = load(path)
    body = doc.find(f"{W}body")
    os.makedirs(media_dir, exist_ok=True)

    out, title, problem, fig_n = [], "", None, 0
    saved, seen, notes, fixed = {}, {}, [], {}

    def close_problem():
        if problem is not None:
            out.append(":::\n")

    for p in paragraphs(body):
        style = pstyle(p)
        text = runs_to_markup(p)
        pics = images_in(p, target)

        if style == "Heading2":
            title = re.sub(r"[`*]", "", text)
            continue

        if style == "Heading3":
            close_problem()
            problem = None
            out.append(f"### {re.sub(r'[`*]', '', text)}\n")
            continue

        if style == "Heading4":
            close_problem()
            seen.clear()
            problem = text
            out.append(f"::: problem {text}\n")
            continue

        if pics:
            for rel in pics:
                fig_n += 1
                data = media.get("word/" + rel)
                if data is None:
                    continue
                ext = os.path.splitext(rel)[1].lower().replace(".jpeg", ".jpg")
                name = f"{slugify(problem or title)}-{fig_n}{ext}"
                dest = os.path.join(media_dir, name)
                with open(dest, "wb") as fh:
                    fh.write(data)
                shrink(dest)
                saved[name] = os.path.getsize(dest)
                caption = "" if problem else title
                out.append(f"::: figure {media_rel}/{name}\n"
                           f"{caption}\n:::\n")
            if not text:
                continue

        if not text:
            continue

        # the same sentence twice in a row is nearly always a leftover in the
        # Word file; report it rather than quietly keeping both
        key = re.sub(r"\W+", " ", text).strip().lower()
        if len(key) > 15:
            if key in seen:
                notes.append(f"repeated text under {problem or title!r}: "
                             f"{text[:60]!r}")
            seen[key] = True

        if style in CODE_STYLES:
            code = raw_text(p)
            for curly, straight in STRAIGHTEN.items():
                if curly in code:
                    fixed[curly] = fixed.get(curly, 0) + code.count(curly)
                    code = code.replace(curly, straight)
            body_lines = "\n".join(l.strip() for l in code.split("\n")
                                    if l.strip())
            out.append(f"```sym {version}\n{body_lines}\n```\n")
            continue

        if style == "ListParagraph":
            out.append(f"- {text}")
            continue

        out.append(wrap(text) + "\n")

    close_problem()

    # tidy: blank line between blocks, single blank line runs
    body_text = "\n".join(out)
    body_text = re.sub(r"\n{3,}", "\n\n", body_text)
    body_text = re.sub(r"(?m)^(- .*)\n\n(?=- )", r"\1\n", body_text)
    body_text = re.sub(r"(?m)^(- .*)\n(?!- |\n)", r"\1\n\n", body_text)
    for curly, n in fixed.items():
        notes.append(f"straightened {n} curly {curly!r} inside commands "
                     f"(Word autocorrect; the calculator needs a straight one)")
    return title, body_text, saved, notes


def splice(chapter_path, title, body):
    """Replace the chapter's ::: practice block with the imported one."""
    src = open(chapter_path, encoding="utf-8").read()
    start = src.find("::: practice")
    if start == -1:
        raise SystemExit(f"{chapter_path}: no '::: practice' block to replace")
    # find the matching close: the practice block is the last thing in the file
    block = (f"::: practice {title}".rstrip() +
             f"\n\n{body.strip()}\n:::\n")
    shutil.copy2(chapter_path, chapter_path + ".bak")
    open(chapter_path, "w", encoding="utf-8").write(src[:start] + block)
    print(f"spliced into {chapter_path} (previous version kept as .bak)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("docx")
    ap.add_argument("--version", default="7",
                    help="which Symbulator version this file's code is for")
    ap.add_argument("--into", help="chapter file whose practice block to replace")
    ap.add_argument("--title", default="",
                    help="heading for the practice block; the chapter's own "
                         "section heading usually says it already")
    ap.add_argument("--media-dir", default=os.path.join(ROOT, "assets", "practice"))
    ap.add_argument("--media-rel", default="assets/practice")
    a = ap.parse_args()

    title, body, saved, notes = convert(a.docx, a.version, a.media_dir,
                                        a.media_rel)
    print(f"{title}: {len(saved)} figures written to {a.media_dir}",
          file=sys.stderr)
    for n in notes:
        print("  check: " + n, file=sys.stderr)
    if a.into:
        splice(a.into, a.title, body)
    else:
        print(body)


if __name__ == "__main__":
    main()
