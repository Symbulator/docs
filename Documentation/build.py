#!/usr/bin/env python3
"""
Symbulator documentation builder.

Reads the single source tree described in SPEC.md and emits, for each
version of the software:

  build/tex/symbulator-v<N>.tex  ->  build/pdf/symbulator-v<N>.pdf
  build/web/content/v<N>/*.html  +  toc.json   (included by web/index.php)

Usage:  python3 build.py [--web] [--pdf] [--versions 7,8,9]
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import unicodedata
import shutil
import subprocess
import sys
from dataclasses import dataclass, field

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
from check_palette import check_palette  # noqa: E402  (needs sys.path set first)
from stamp_assets import check_asset_stamps  # noqa: E402
from check_control_chars import check_control_chars  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
BUILD = os.path.join(ROOT, "build")
ASSETS = os.path.join(ROOT, "assets")


# Every URL this build writes into the site is root-absolute.
#
# learn.symbulator.com serves the same index.php at /?v=9&p=lesson-dc and at
# the pretty /9/lesson-dc. A relative "assets/style.css" resolves against the
# second as /9/assets/style.css and 404s -- which is how the site shipped
# with no stylesheet, no logo and no figures on every pretty URL while the
# query form looked perfect. Root-absolute paths resolve identically under
# both, so there is one right answer rather than one per URL shape.
#
# The site therefore only works at a document root. That is already true of
# symbulator.com's landing page, and is stated in the deploy notes.

def site_path(ref: str) -> str:
    """An in-site asset reference, made root-absolute. External URLs and
    anything already absolute are returned untouched."""
    if ref.startswith(("http://", "https://", "//", "/", "data:", "#")):
        return ref
    return "/" + ref


def page_url(v, p: str = "") -> str:
    """A link to a chapter: /9/lesson-dc. Mirrors url() in web/index.php,
    including its fallback -- .htaccess only rewrites [789] and a
    lowercase-alnum-hyphen slug, so anything else takes the query form
    rather than 404ing."""
    import re as _re
    if not _re.fullmatch(r"[789]", str(v)) or (p and not _re.fullmatch(r"[a-z0-9-]+", p)):
        return f"/?v={v}" + (f"&amp;p={p}" if p else "")
    return f"/{v}/" + p


# --------------------------------------------------------------------------
# AST
# --------------------------------------------------------------------------

@dataclass
class Node:
    kind: str
    text: str = ""
    arg: str = ""
    children: list = field(default_factory=list)
    meta: dict = field(default_factory=dict)


@dataclass
class Chapter:
    id: str
    title: str
    kind: str = "lesson"
    versions: list = field(default_factory=lambda: [7, 8, 9])
    absent_note: str = ""
    updated: str = ""
    summary: str = ""
    blocks: list = field(default_factory=list)


class SourceError(Exception):
    pass


# --------------------------------------------------------------------------
# Block parser
# --------------------------------------------------------------------------

DIRECTIVES = {"tip", "note", "warning", "danger", "figure", "problem",
              "answer", "practice", "only", "not"}

HEADING_RE = re.compile(r"^(#{2,3})\s+(.*?)(?:\s*\{#([\w-]+)\})?\s*$")
# ```field 9 Circuit description  -- lang, versions, then a free-text
# name for the interface field the reader types into. Only `field` uses
# the third part; for the others a stray word is a parse error rather
# than silent text.
FENCE_RE = re.compile(r"^```(\w+)?\s*([\d,]*)\s*(.*?)\s*$")
DIRECTIVE_RE = re.compile(r"^:::\s*(\w+)?\s*(.*)$")
ULI_RE = re.compile(r"^[-*]\s+(.*)$")
OLI_RE = re.compile(r"^\d+[.)]\s+(.*)$")


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


def slugify(s: str) -> str:
    s = re.sub(r"\{\{[^}]*\}\}", "", s)
    s = _ascii(s)
    s = re.sub(r"[^\w\s-]", "", s, flags=re.ASCII).strip().lower()
    return re.sub(r"[\s_]+", "-", s) or "section"


def parse_chapter(path: str) -> Chapter:
    raw = open(path, encoding="utf-8").read()
    if not raw.startswith("---"):
        raise SourceError(f"{path}: missing YAML front matter")
    _, fm, body = raw.split("---", 2)
    meta = yaml.safe_load(fm) or {}
    ch = Chapter(
        id=meta.get("id") or os.path.splitext(os.path.basename(path))[0],
        title=meta.get("title", "Untitled"),
        kind=meta.get("kind", "lesson"),
        versions=meta.get("versions", [7, 8, 9]),
        absent_note=(meta.get("absent_note") or "").strip(),
        updated=str(meta.get("updated", "")),
        summary=(meta.get("summary") or "").strip(),
    )
    lines = body.split("\n")
    ch.blocks = parse_blocks(lines, path)
    return ch


def parse_blocks(lines: list[str], path: str, depth: int = 0) -> list[Node]:
    """Consume `lines` (mutated) until exhausted or a closing ':::' at depth>0."""
    out: list[Node] = []
    i = 0
    while i < len(lines):
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        # closing markers are consumed by collect_directive; any left is an error
        if line.strip() == ":::":
            raise SourceError(f"{path}: stray ':::' (unbalanced directive)")

        # heading
        m = HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            anchor = m.group(3) or slugify(title)
            out.append(Node("heading", text=title, meta={"level": level,
                                                         "anchor": anchor}))
            i += 1
            continue

        # code fence
        m = FENCE_RE.match(line)
        if m and m.group(1) in ("sym", "out", "field", "text", None):
            lang = m.group(1) or "text"
            vers = [int(v) for v in m.group(2).split(",") if v] or None
            name = m.group(3) or ""
            if name and lang != "field":
                raise SourceError(
                    f"{line!r}: only a ```field fence takes a name after the "
                    f"version. Did you mean ```field?")
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].startswith("```"):
                buf.append(lines[j])
                j += 1
            out.append(Node("code", text="\n".join(buf),
                            meta={"lang": lang, "versions": vers,
                                  "field": name}))
            i = j + 1
            continue

        # directive
        m = DIRECTIVE_RE.match(line)
        if m and m.group(1) in DIRECTIVES:
            name, arg = m.group(1), m.group(2).strip()
            inner, consumed = collect_directive(lines[i + 1:], path, depth + 1)
            node = Node(name, arg=arg, children=parse_blocks(inner, path, depth + 1))
            out.append(node)
            i = i + 1 + consumed
            continue

        # list
        if ULI_RE.match(line) or OLI_RE.match(line):
            ordered = bool(OLI_RE.match(line))
            items, j = [], i
            while j < len(lines):
                mm = OLI_RE.match(lines[j]) if ordered else ULI_RE.match(lines[j])
                if not mm:
                    if lines[j].startswith("  ") and items:      # continuation
                        items[-1] += " " + lines[j].strip()
                        j += 1
                        continue
                    break
                items.append(mm.group(1).strip())
                j += 1
            out.append(Node("list", meta={"ordered": ordered, "items": items}))
            i = j
            continue

        # display maths
        if line.strip() == "$$":
            j = i + 1
            buf = []
            while j < len(lines) and lines[j].strip() != "$$":
                buf.append(lines[j])
                j += 1
            out.append(Node("mathblock", text="\n".join(buf)))
            i = j + 1
            continue

        # paragraph
        buf = []
        j = i
        while j < len(lines) and lines[j].strip() and not (
                HEADING_RE.match(lines[j]) or lines[j].startswith("```")
                or lines[j].startswith(":::") or ULI_RE.match(lines[j])
                or OLI_RE.match(lines[j])):
            buf.append(lines[j].strip())
            j += 1
        out.append(Node("para", text=" ".join(buf)))
        i = j
    return out


def collect_directive(rest: list[str], path: str, depth: int):
    """Return (inner_lines, lines_consumed_including_closing_marker)."""
    inner, level, k = [], 1, 0
    while k < len(rest):
        line = rest[k]
        m = DIRECTIVE_RE.match(line)
        if line.strip() == ":::":
            level -= 1
            if level == 0:
                return inner, k + 1
            inner.append(line)
        elif m and m.group(1) in DIRECTIVES:
            level += 1
            inner.append(line)
        else:
            inner.append(line)
        k += 1
    raise SourceError(f"{path}: unclosed ':::' directive")


# --------------------------------------------------------------------------
# Inline parser
# --------------------------------------------------------------------------

INLINE_RE = re.compile(
    r"(?P<brace>\{\{(?:[^{}]|\{[^{}]*\})*\}\})"
    r"|(?P<code>`[^`]+`)"
    r"|(?P<math>\$[^$]+\$)"
    r"|(?P<link>\[[^\]]+\]\([^)]+\))"
    r"|(?P<strong>\*\*[^*]+\*\*)"
    r"|(?P<em>\*[^*]+\*)"
)


def parse_inline(text: str) -> list[Node]:
    out, pos = [], 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            out.append(Node("text", text=text[pos:m.start()]))
        kind = m.lastgroup
        s = m.group()
        if kind == "brace":
            out.append(parse_brace(s[2:-2]))
        elif kind == "code":
            out.append(Node("icode", text=s[1:-1]))
        elif kind == "math":
            out.append(Node("imath", text=s[1:-1]))
        elif kind == "link":
            label, url = re.match(r"\[([^\]]+)\]\(([^)]+)\)", s).groups()
            out.append(Node("link", text=label, arg=url,
                            children=parse_inline(label)))
        elif kind == "strong":
            out.append(Node("strong", children=parse_inline(s[2:-2])))
        elif kind == "em":
            out.append(Node("em", children=parse_inline(s[1:-1])))
        pos = m.end()
    if pos < len(text):
        out.append(Node("text", text=text[pos:]))
    return out


def parse_brace(inner: str) -> Node:
    if inner.startswith("i:"):
        return Node("index", text=inner[2:].strip())
    if inner.startswith("t:"):
        return Node("term", text=inner[2:].strip())
    if inner.startswith("ref:"):
        return Node("ref", text=inner[4:].strip())
    if inner.startswith("o:"):          # an answer the software gave back
        return Node("answer_span", text=inner[2:].strip())
    if inner.startswith("sub:"):
        return Node("sub", text=inner[4:].strip())
    if inner.startswith("sup:"):
        return Node("sup", text=inner[4:].strip())
    m = re.match(r"^(!?)v([\d,]+)\|(.*)$", inner, re.S)
    if m:
        neg, vers, body = m.groups()
        return Node("vspan", arg=neg,
                    meta={"versions": [int(v) for v in vers.split(",")]},
                    children=parse_inline(body))
    return Node("text", text="{{" + inner + "}}")


# --------------------------------------------------------------------------
# Version resolution / numbering
# --------------------------------------------------------------------------

class Book:
    def __init__(self, meta: dict, chapters: list[Chapter]):
        self.meta = meta
        self.chapters = chapters

    def for_version(self, v: int):
        """Chapters present in version v, with display numbers assigned."""
        out, n = [], 0
        for ch in self.chapters:
            present = v in ch.versions
            if not present and not ch.absent_note:
                continue
            number = None
            if ch.kind == "lesson":
                n += 1
                number = n
            out.append((ch, number, present))
        return out

    def labels(self, v: int) -> dict:
        """id -> (display name, chapter id, anchor) for cross-references."""
        lab = {}
        for ch, number, present in self.for_version(v):
            name = f"Lesson {number}" if number else ch.title
            lab[ch.id] = (name, ch.id, "")
            if not present:
                continue
            sect = 0
            for b in walk(ch.blocks, v):
                if b.kind == "heading" and b.meta["level"] == 2:
                    sect += 1
                    disp = (f"section {number}.{sect}" if number
                            else f"“{b.text}”")
                    lab[b.meta["anchor"]] = (disp, ch.id, b.meta["anchor"])
        return lab


def keep(node: Node, v: int) -> bool:
    if node.kind == "only":
        return v in [int(x) for x in node.arg.replace(" ", "").split(",") if x]
    if node.kind == "not":
        return v not in [int(x) for x in node.arg.replace(" ", "").split(",") if x]
    if node.kind == "code":
        vers = node.meta.get("versions")
        return vers is None or v in vers
    return True


def walk(blocks: list[Node], v: int):
    """Yield blocks visible in version v, flattening only/not wrappers."""
    for b in blocks:
        if b.kind in ("only", "not"):
            if keep(b, v):
                yield from walk(b.children, v)
            continue
        if not keep(b, v):
            continue
        yield b


# --------------------------------------------------------------------------
# Callout furniture
# --------------------------------------------------------------------------
# Each callout carries an icon *and* a word, so the four kinds stay
# distinguishable in greyscale, in print, and for a colour-blind reader.
# Drawn as inline SVG (stroked in currentColor, so the CSS accent applies).

CALLOUT_LABELS = {"tip": "Tip", "note": "Note", "warning": "Warning",
                  "danger": "Caution", "absent": "Not in this version"}

CALLOUT_ICONS = {
    # lightbulb
    "tip": '<circle cx="8" cy="6.4" r="3.9"/><path d="M6 12.4h4M6.7 14.4h2.6"/>',
    # circled i
    "note": '<circle cx="8" cy="8" r="6.2"/><path d="M8 7.2v4"/>'
            '<circle cx="8" cy="4.6" r=".85" fill="currentColor" stroke="none"/>',
    # triangle with a bang
    "warning": '<path d="M8 1.9 15 13.9H1z"/><path d="M8 6.3v3.5"/>'
               '<circle cx="8" cy="11.9" r=".85" fill="currentColor" stroke="none"/>',
    # octagon with a bang
    "danger": '<path d="M5.5 1.6h5L14.4 5.5v5l-3.9 3.9h-5L1.6 10.5v-5z"/>'
              '<path d="M8 4.7v4.2"/>'
              '<circle cx="8" cy="11.5" r=".85" fill="currentColor" stroke="none"/>',
    # circle with a bar
    "absent": '<circle cx="8" cy="8" r="6.2"/><path d="M4.8 8h6.4"/>',
}


def callout_head(kind: str) -> str:
    """The icon-plus-word strip that opens every callout."""
    return (f'<p class="callout-kind">'
            f'<svg class="callout-icon" viewBox="0 0 16 16" aria-hidden="true" '
            f'fill="none" stroke="currentColor" stroke-width="1.3" '
            f'stroke-linejoin="round" stroke-linecap="round">'
            f'{CALLOUT_ICONS[kind]}</svg>'
            f'<span>{CALLOUT_LABELS[kind]}</span></p>')


# --------------------------------------------------------------------------
# HTML emitter
# --------------------------------------------------------------------------

class HtmlRenderer:
    def __init__(self, book: Book, version: int):
        self.book, self.v = book, version
        self.terms = book.meta.get("terms", {})
        self.labels = book.labels(version)
        self.index: dict[str, list[str]] = {}
        self.chapter_id = ""
        self.section_no = 0
        self.chapter_no = None

    # -- inline ----------------------------------------------------------
    def inline(self, text: str) -> str:
        return "".join(self.inode(n) for n in parse_inline(text))

    def inode(self, n: Node) -> str:
        if n.kind == "text":
            return html.escape(n.text)
        if n.kind == "icode":
            return f'<code>{html.escape(n.text)}</code>'
        if n.kind == "imath":
            return f'<span class="math">\\({html.escape(n.text)}\\)</span>'
        if n.kind == "strong":
            return "<strong>" + "".join(self.inode(c) for c in n.children) + "</strong>"
        if n.kind == "em":
            return "<em>" + "".join(self.inode(c) for c in n.children) + "</em>"
        if n.kind == "link":
            return (f'<a href="{html.escape(n.arg)}">'
                    + "".join(self.inode(c) for c in n.children) + "</a>")
        if n.kind == "term":
            return html.escape(str(self.terms.get(n.text, {}).get(self.v, n.text)))
        if n.kind == "index":
            anchor = "ix-" + slugify(n.text) + f"-{len(self.index.get(n.text, []))}"
            self.index.setdefault(n.text, []).append(f"{self.chapter_id}#{anchor}")
            return f'<span class="ix" id="{anchor}"></span>'
        if n.kind == "ref":
            name, cid, anchor = self.labels.get(n.text, (n.text, "", ""))
            href = page_url(self.v, cid) + (f"#{anchor}" if anchor else "")
            return f'<a class="xref" href="{href}">{html.escape(name)}</a>'
        if n.kind == "answer_span":
            return f'<span class="ans">{html.escape(n.text)}</span>'
        if n.kind == "sub":
            return f'<sub>{html.escape(n.text)}</sub>'
        if n.kind == "sup":
            return f'<sup>{html.escape(n.text)}</sup>'
        if n.kind == "vspan":
            hit = self.v in n.meta["versions"]
            show = (not hit) if n.arg == "!" else hit
            return "".join(self.inode(c) for c in n.children) if show else ""
        return ""

    # -- blocks ----------------------------------------------------------
    def blocks(self, blocks: list[Node]) -> str:
        return "\n".join(self.block(b) for b in walk(blocks, self.v))

    def block(self, b: Node) -> str:
        k = b.kind
        if k == "para":
            return f"<p>{self.inline(b.text)}</p>"
        if k == "heading":
            if b.meta["level"] == 2:
                self.section_no += 1
                num = (f'<span class="secno">{self.chapter_no}.{self.section_no}</span>'
                       if self.chapter_no else "")
                return (f'<h2 id="{b.meta["anchor"]}">{num}'
                        f'{self.inline(b.text)}</h2>')
            return f'<h3 id="{b.meta["anchor"]}">{self.inline(b.text)}</h3>'
        if k == "list":
            tag = "ol" if b.meta["ordered"] else "ul"
            items = "".join(f"<li>{self.inline(i)}</li>" for i in b.meta["items"])
            return f"<{tag}>{items}</{tag}>"
        if k == "code":
            body = "\n".join(html.escape(l) for l in b.text.split("\n"))
            if b.meta["lang"] == "field":
                # What the reader types into a named field of the Symbulator 9
                # interface. Version 9 has no command line -- everything is
                # entered into a labelled box -- so the label is part of the
                # instruction, and the panel is drawn to resemble that box.
                name = html.escape(b.meta.get("field") or "")
                return (f'<div class="code field">'
                        f'<span class="code-label">{name}</span>'
                        f'<pre><code>{body}</code></pre></div>')
            cls = "sym" if b.meta["lang"] == "sym" else "out"
            label = "type" if cls == "sym" else "returns"
            return (f'<div class="code {cls}"><span class="code-label">{label}'
                    f'</span><pre><code>{body}</code></pre></div>')
        if k in ("tip", "note", "warning", "danger"):
            title = (f'<p class="callout-title">{self.inline(b.arg)}</p>'
                     if b.arg else "")
            return (f'<aside class="callout {k}">{callout_head(k)}'
                    f'{title}{self.blocks(b.children)}</aside>')
        if k == "figure":
            cap = self.blocks(b.children)
            return (f'<figure><img src="{html.escape(site_path(b.arg))}" alt="">'
                    f'<figcaption>{cap}</figcaption></figure>')
        if k == "problem":
            return (f'<section class="problem"><p class="problem-title">'
                    f'{self.inline(b.arg)}</p>{self.blocks(b.children)}</section>')
        if k == "answer":
            return (f'<div class="answer"><p class="answer-title">Solution</p>'
                    f'{self.blocks(b.children)}</div>')
        if k == "practice":
            head = (f'<h3 class="practice-title">{self.inline(b.arg)}</h3>'
                    if b.arg else "")
            return (f'<section class="practice">{head}'
                    f'{self.blocks(b.children)}</section>')
        if k == "mathblock":
            return f'<div class="mathblock">\\[{html.escape(b.text)}\\]</div>'
        return ""

    def chapter(self, ch: Chapter, number, present: bool) -> str:
        self.chapter_id, self.chapter_no, self.section_no = ch.id, number, 0
        # An eyebrow is the small line above a chapter title -- "Lesson 3".
        # A chapter with no number has nothing useful to put there, and
        # falling back to the title printed it twice: "Introduction /
        # Introduction", "Roll the credits / Roll the credits", on the
        # chapter page, in the sidebar and on the home page cards.
        eyebrow = f"Lesson {number}" if number else ""
        parts = ['<header class="chapter-head">']
        if eyebrow:
            parts.append(f'<p class="eyebrow">{html.escape(eyebrow)}</p>')
        parts.append(f'<h1>{html.escape(ch.title)}</h1>')
        if ch.summary:
            parts.append(f'<p class="lede">{self.inline(ch.summary)}</p>')
        if ch.updated:
            parts.append(f'<p class="updated">Last updated {html.escape(ch.updated)}</p>')
        parts.append("</header>")
        if not present:
            parts.append(f'<aside class="callout absent">'
                         f'{callout_head("absent")}'
                         f'<p>{self.inline(ch.absent_note)}</p></aside>')
        else:
            parts.append(self.blocks(ch.blocks))
        return "\n".join(parts)


# --------------------------------------------------------------------------
# LaTeX emitter
# --------------------------------------------------------------------------

TEX_ESCAPE = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
              "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
              "^": r"\textasciicircum{}", "\\": r"\textbackslash{}"}

# glyphs that the mono font may not carry
GLYPHS = {"\U0001d422": r"\textbf{i}", "∠": r"\ensuremath{\angle}",
          "δ": r"\ensuremath{\delta}", "ω": r"\ensuremath{\omega}",
          "π": r"\ensuremath{\pi}", "Ω": r"\ensuremath{\Omega}",
          "Δ": r"\ensuremath{\Delta}", "≤": r"\ensuremath{\le}",
          "→": r"\ensuremath{\rightarrow}", "ᴇ": r"\textsc{e}",
          "º": r"\textordmasculine{}", "°": r"\textdegree{}",
          }

# curly punctuation: converted in prose, left alone inside code, where the
# distinction between the negate sign and the minus sign matters
PROSE_GLYPHS = {"–": "--", "—": "---", "’": "'", "‘": "`",
                "“": "``", "”": "''"}


def _smart_quotes(s: str) -> str:
    """Turn straight double quotes into an alternating open/close pair."""
    out, open_next = [], True
    for c in s:
        if c == '"':
            out.append("``" if open_next else "''")
            open_next = not open_next
        else:
            out.append(c)
    return "".join(out)


def tex_escape(s: str, prose: bool = True) -> str:
    if prose:
        s = _smart_quotes(s)
    out = []
    for c in s:
        if prose and c in PROSE_GLYPHS:
            out.append(PROSE_GLYPHS[c])
        elif c in GLYPHS:
            out.append(GLYPHS[c])
        elif c in TEX_ESCAPE:
            out.append(TEX_ESCAPE[c])
        else:
            out.append(c)
    return "".join(out)


def tex_code(s: str) -> str:
    """Escape a line of calculator input and allow breaks at separators."""
    out = tex_escape(s, prose=False)
    out = out.replace(":", ":\\allowbreak{}").replace(",", ",\\allowbreak{}")
    return out


class TexRenderer:
    def __init__(self, book: Book, version: int):
        self.book, self.v = book, version
        self.terms = book.meta.get("terms", {})
        self.labels = book.labels(version)
        self.chapter_no = None

    def inline(self, text: str) -> str:
        return "".join(self.inode(n) for n in parse_inline(text))

    def inode(self, n: Node) -> str:
        if n.kind == "text":
            return tex_escape(n.text)
        if n.kind == "icode":
            return r"\symcode{" + tex_code(n.text) + "}"
        if n.kind == "imath":
            return f"${n.text}$"
        if n.kind == "strong":
            return r"\textbf{" + "".join(self.inode(c) for c in n.children) + "}"
        if n.kind == "em":
            return r"\emph{" + "".join(self.inode(c) for c in n.children) + "}"
        if n.kind == "link":
            label = "".join(self.inode(c) for c in n.children)
            return r"\href{" + n.arg.replace("%", r"\%") + "}{" + label + "}"
        if n.kind == "term":
            return tex_escape(str(self.terms.get(n.text, {}).get(self.v, n.text)))
        if n.kind == "index":
            return r"\index{" + tex_escape(n.text) + "}"
        if n.kind == "ref":
            name, cid, anchor = self.labels.get(n.text, (n.text, "", ""))
            target = anchor or cid
            return (tex_escape(name) + r"~(page~\pageref{lbl:" + target + "})")
        if n.kind == "answer_span":
            return r"\ans{" + tex_escape(n.text) + "}"
        if n.kind == "sub":
            return r"\textsubscript{" + tex_escape(n.text) + "}"
        if n.kind == "sup":
            return r"\textsuperscript{" + tex_escape(n.text) + "}"
        if n.kind == "vspan":
            hit = self.v in n.meta["versions"]
            show = (not hit) if n.arg == "!" else hit
            return "".join(self.inode(c) for c in n.children) if show else ""
        return ""

    def blocks(self, blocks: list[Node]) -> str:
        return "\n\n".join(x for x in (self.block(b)
                                       for b in walk(blocks, self.v)) if x)

    def block(self, b: Node) -> str:
        k = b.kind
        if k == "para":
            return self.inline(b.text)
        if k == "heading":
            cmd = "section" if b.meta["level"] == 2 else "subsection"
            return (f"\\{cmd}{{{self.inline(b.text)}}}"
                    f"\\label{{lbl:{b.meta['anchor']}}}")
        if k == "list":
            env = "enumerate" if b.meta["ordered"] else "itemize"
            items = "\n".join(r"\item " + self.inline(i) for i in b.meta["items"])
            return f"\\begin{{{env}}}\n{items}\n\\end{{{env}}}"
        if k == "code":
            # In print there is no interface to imitate, so a field is set as
            # typed input like any other. The sentence above it names the
            # field anyway.
            env = ("symtype" if b.meta["lang"] in ("sym", "field")
                   else "symout")
            # a line starting with "[" would be read as \\'s optional argument
            lines = "\\\\\n".join(
                ("{}" + tex_code(l)) if l.lstrip().startswith("[")
                else tex_code(l)
                for l in b.text.split("\n"))
            return f"\\begin{{{env}}}\n{lines}\n\\end{{{env}}}"
        if k in ("tip", "note", "warning", "danger"):
            title = self.inline(b.arg) if b.arg else ""
            return (f"\\begin{{callout{k}}}{{{title}}}\n"
                    f"{self.blocks(b.children)}\n\\end{{callout{k}}}")
        if k == "figure":
            src = (b.arg if b.arg.lower().endswith((".png", ".jpg", ".jpeg"))
                   else os.path.splitext(b.arg)[0])
            cap = self.blocks(b.children)
            return ("\\begin{symfigure}\n"
                    f"\\includegraphics[width=\\figwidth]{{{src}}}\n"
                    f"\\caption{{{cap}}}\n\\end{{symfigure}}")
        if k == "problem":
            return (f"\\begin{{problem}}{{{self.inline(b.arg)}}}\n"
                    f"{self.blocks(b.children)}\n\\end{{problem}}")
        if k == "answer":
            return (f"\\begin{{solution}}\n{self.blocks(b.children)}\n"
                    f"\\end{{solution}}")
        if k == "practice":
            head = (f"\\practiceheading{{{self.inline(b.arg)}}}\n\n"
                    if b.arg else "\\practicerule\n\n")
            return head + self.blocks(b.children)
        if k == "mathblock":
            return f"\\[{b.text}\\]"
        return ""

    def chapter(self, ch: Chapter, number, present: bool) -> str:
        self.chapter_no = number
        head = []
        if number:
            head.append(f"\\lesson{{{number}}}{{{tex_escape(ch.title)}}}")
        else:
            head.append(f"\\frontchapter{{{tex_escape(ch.title)}}}")
        head.append(f"\\label{{lbl:{ch.id}}}")
        if ch.summary:
            head.append(f"\\chaptersummary{{{self.inline(ch.summary)}}}")
        if not present:
            head.append(f"\\begin{{calloutnote}}{{Not in this version}}\n"
                        f"{self.inline(ch.absent_note)}\n\\end{{calloutnote}}")
        else:
            head.append(self.blocks(ch.blocks))
        return "\n\n".join(head)


# --------------------------------------------------------------------------
# Drivers
# --------------------------------------------------------------------------

def load_book() -> Book:
    meta = yaml.safe_load(open(os.path.join(ROOT, "book.yaml"), encoding="utf-8"))
    chapters = [parse_chapter(os.path.join(SRC, f)) for f in meta["chapters"]]
    return Book(meta, chapters)


def build_web(book: Book, versions: list[int]):
    outroot = os.path.join(BUILD, "web")
    for v in versions:
        vdir = os.path.join(outroot, "content", f"v{v}")
        os.makedirs(vdir, exist_ok=True)
        r = HtmlRenderer(book, v)
        toc = []
        for ch, number, present in book.for_version(v):
            body = r.chapter(ch, number, present)
            open(os.path.join(vdir, ch.id + ".html"), "w",
                 encoding="utf-8").write(body)
            sections = []
            if present:
                n = 0
                for b in walk(ch.blocks, v):
                    if b.kind == "heading" and b.meta["level"] == 2:
                        n += 1
                        sections.append({"anchor": b.meta["anchor"],
                                         "title": re.sub(r"\{\{[^}]*\}\}", "", b.text),
                                         "number": f"{number}.{n}" if number else ""})
            toc.append({"id": ch.id, "title": ch.title,
                        # Empty, not the title -- see the note above. Every
                        # consumer of toc.json must skip an empty eyebrow.
                        "eyebrow": f"Lesson {number}" if number else "",
                        "number": number,
                        # Rendered, not raw: the chapter opener runs the
                        # summary through inline() (see HtmlRenderer.chapter),
                        # and the cards on the home page need the same or the
                        # reader sees the literal *asterisks* of the source.
                        "summary": r.inline(ch.summary),
                        "present": present, "sections": sections})
        meta = {"version": v, "chapters": toc,
                "index": {k: sorted(set(vals)) for k, vals in sorted(r.index.items())},
                **{k: val for k, val in book.meta["versions"][v].items()}}
        json.dump(meta, open(os.path.join(vdir, "toc.json"), "w",
                             encoding="utf-8"), indent=1)
    # copy the PHP front end and static assets next to the content
    for name in ("index.php", ".htaccess", "favicon.ico", "assets"):
        s, d = os.path.join(ROOT, "web", name), os.path.join(outroot, name)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    # The banner is shared with symbulator.com and the app; design/banner.css
    # is its one source, copied in rather than duplicated inside style.css.
    shutil.copy2(os.path.join(ROOT, "design", "banner.css"),
                 os.path.join(outroot, "assets", "banner.css"))
    if os.path.isdir(ASSETS):
        shutil.copytree(ASSETS, os.path.join(outroot, "assets"),
                        dirs_exist_ok=True)
    json.dump({"versions": {str(k): val for k, val in book.meta["versions"].items()},
               "title": book.meta["title"], "subtitle": book.meta["subtitle"]},
              open(os.path.join(outroot, "content", "book.json"), "w",
                   encoding="utf-8"), indent=1)
    print(f"web:  {outroot}")


def build_tex(book: Book, versions: list[int], run_pdf=True):
    texdir = os.path.join(BUILD, "tex")
    pdfdir = os.path.join(BUILD, "pdf")
    os.makedirs(texdir, exist_ok=True)
    os.makedirs(pdfdir, exist_ok=True)
    shutil.copy2(os.path.join(ROOT, "tex", "symbulator.cls"), texdir)
    if os.path.isdir(ASSETS):
        shutil.copytree(ASSETS, os.path.join(texdir, "assets"), dirs_exist_ok=True)

    for v in versions:
        vm = book.meta["versions"][v]
        r = TexRenderer(book, v)
        body = "\n\n\\clearpage\n\n".join(
            r.chapter(ch, n, p) for ch, n, p in book.for_version(v))
        doc = "\n".join([
            r"\documentclass{symbulator}",
            f"\\booktitle{{{tex_escape(book.meta['title'])}}}",
            f"\\booksubtitle{{{tex_escape(book.meta['subtitle'])}}}",
            f"\\bookversion{{{tex_escape(vm['name'])}}}",
            f"\\bookplatform{{{tex_escape(vm['platform'])}}}",
            f"\\bookauthor{{{tex_escape(book.meta['author'])}}}",
            r"\begin{document}",
            r"\maketitlepage",
            r"\tableofcontents",
            body,
            r"\printtheindex",
            r"\end{document}", ""])
        texpath = os.path.join(texdir, f"symbulator-v{v}.tex")
        open(texpath, "w", encoding="utf-8").write(doc)
        print(f"tex:  {texpath}")
        if run_pdf:
            compile_pdf(texdir, f"symbulator-v{v}", pdfdir)


def compile_pdf(texdir: str, stem: str, pdfdir: str):
    env = dict(os.environ, TEXINPUTS=f".:{texdir}:")
    for i in range(3):
        p = subprocess.run(["xelatex", "-interaction=nonstopmode",
                            "-halt-on-error", stem + ".tex"],
                           cwd=texdir, capture_output=True, text=True, env=env)
        if p.returncode != 0:
            log = "\n".join(l for l in p.stdout.split("\n")
                            if l.startswith("!") or "l." == l[:2])[-2500:]
            print(f"xelatex failed on {stem} (pass {i+1}):\n{log}", file=sys.stderr)
            tail = p.stdout[-2500:]
            print(tail, file=sys.stderr)
            return
        if i == 0:
            subprocess.run(["makeindex", "-q", stem + ".idx"], cwd=texdir,
                           capture_output=True)
    shutil.copy2(os.path.join(texdir, stem + ".pdf"),
                 os.path.join(pdfdir, stem + ".pdf"))
    print(f"pdf:  {os.path.join(pdfdir, stem + '.pdf')}")


def check(book: Book, versions: list[int], verbose: bool = False) -> int:
    """Validate the source tree. Returns the number of problems found."""
    problems: list[str] = []
    known_versions = set(book.meta["versions"].keys())
    terms = book.meta.get("terms", {})

    for v in versions:
        labels = book.labels(v)
        for ch, _number, present in book.for_version(v):
            if not present:
                continue
            for b in walk(ch.blocks, v):
                _check_block(b, v, ch, labels, terms, known_versions, problems)

    # design/tokens.json, web/assets/style.css and tex/symbulator.cls each
    # hard-code their own copy of the palette with no shared source, so a
    # colour changed in one silently drifts from the other two -- see
    # tools/check_palette.py for the full explanation.
    problems.extend(check_palette())
    problems.extend(check_shared_banner())
    # The landing page has no build step, so nothing else would
    # notice that a changed stylesheet still carries its old stamp
    # and will not reach anyone who has visited before.
    problems.extend(check_asset_stamps())
    # A heredoc-eaten backslash is invisible in an editor and
    # survives every other check; chapter 9 shipped with one.
    problems.extend(check_control_chars())
    problems.extend(check_nested_version_spans())
    problems.extend(check_buried_v9())

    missing: list[str] = []
    # figures need a pair: .svg for the web, .pdf for print
    for ch in book.chapters:
        for b in _all_blocks(ch.blocks):
            if b.kind != "figure":
                continue
            web = os.path.join(ROOT, b.arg)
            print_file = os.path.splitext(web)[0] + ".pdf"
            if not os.path.isfile(web):
                missing.append(f"{ch.id}: figure not found: {b.arg}")
            elif web.lower().endswith((".png", ".jpg", ".jpeg")):
                pass      # a raster figure is used as-is by both outputs
            elif not os.path.isfile(print_file):
                missing.append(f"{ch.id}: no print version of {b.arg} "
                               f"(expected {os.path.basename(print_file)})")
        for v in ch.versions:
            if str(v) not in known_versions and v not in known_versions:
                problems.append(f"{ch.id}: unknown version {v} in front matter")

    for p in problems:
        print("  " + p, file=sys.stderr)
    if verbose:
        for m in missing:
            print("  " + m, file=sys.stderr)
    tail = f", {len(missing)} figure(s) still to supply" if missing else ""
    print((f"check: {len(problems)} problem(s)" if problems else "check: clean")
          + tail)
    return len(problems)


def check_buried_v9() -> list[str]:
    """Version 9 content inside an `::: only 7,8` block never renders.

    The outer directive drops the whole subtree from the version 9 build, so
    a ```field 9 panel or a `::: only 9` block nested inside one is dead: it
    is in the source, it survives every other check, and the reader sees
    nothing. Four of them were written that way on 24 Aug 2026 by a script
    that inserted panels after a ```sym 8 fence without looking at what
    directive it was standing in.

    Panels inside a `::: practice` section are exempt. Those sections are
    still wrapped for version 9 on purpose, chapter by chapter, and their
    panels are meant to lie dormant until the section is unwrapped."""
    import glob as _glob
    directive = re.compile(r"^:::\s*(\w+)?\s*(.*)$")
    out = []
    for path in sorted(_glob.glob(os.path.join(SRC, "*.md"))):
        stack, in_fence = [], False
        for n, line in enumerate(open(path, encoding="utf-8"), 1):
            line = line.rstrip(chr(10))
            t = line.strip()
            if line.startswith("```"):
                if (not in_fence and line.startswith("```field 9")
                        and not any(d.startswith("practice") for d in stack)
                        and any(d.startswith(("only 7", "only 8")) for d in stack)):
                    out.append(f"{os.path.basename(path)}:{n}: a ```field 9 "
                               f"panel is inside an ::: only 7,8 block, so "
                               f"version 9 never sees it")
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if t == ":::":
                if stack:
                    stack.pop()
                continue
            m = directive.match(t)
            if m and m.group(1):
                name = (m.group(1) + " " + (m.group(2) or "")).strip()
                if (name.startswith("only 9")
                        and not any(d.startswith("practice") for d in stack)
                        and any(d.startswith(("only 7", "only 8")) for d in stack)):
                    out.append(f"{os.path.basename(path)}:{n}: an ::: only 9 "
                               f"block is inside an ::: only 7,8 block, so "
                               f"version 9 never sees it")
                stack.append(name)
    return out


def check_nested_version_spans() -> list[str]:
    """A {{v7,8|...}} span must not contain another {{...}}.

    The inline parser closes a version span at the first `}}` it meets, so a
    nested `{{o:...}}` or `{{sub:x}}` ends it early and the remainder leaks
    into the page as literal markup -- `{{v7,8|The calculator returns` and all.
    It renders, it builds, it passes every other check, and it is visible only
    if someone reads that paragraph on that one version.

    Found on 24 Aug 2026 in three passages, all written the same day. Use
    `::: only 7,8` and `::: only 9` blocks instead when either half needs
    inline markup of its own."""
    import glob as _glob
    opener = re.compile(r"\{\{v(?:7|8|9|7,8|7,9|8,9)\|")
    out = []
    for path in sorted(_glob.glob(os.path.join(SRC, "*.md"))):
        # Whole file, not line by line: a version span routinely wraps across
        # a line break, and six of these hid from an earlier per-line version
        # of this check for exactly that reason.
        text = open(path, encoding="utf-8").read()
        for m in opener.finditer(text):
            rest = text[m.end():]
            close = rest.find("}}")
            inner = rest if close == -1 else rest[:close]
            if "{{" in inner:
                line_no = text.count(chr(10), 0, m.start()) + 1
                out.append(
                    f"{os.path.basename(path)}:{line_no}: a version span "
                    f"contains nested {{{{...}}}} markup, which closes it "
                    f"early -- use ::: only blocks instead")
    return out


def check_shared_banner() -> list[str]:
    """The banner is one file, design/banner.css, imported by this site and
    copied verbatim into landing/. The landing page has no build step, so its
    copy can silently fall behind -- which is exactly how the lockup drifted
    before it was centralised. Compare them and complain loudly."""
    canon = os.path.join(ROOT, "design", "banner.css")
    copy = os.path.join(ROOT, "landing", "assets", "banner.css")
    if not os.path.isfile(copy):
        return ["banner: landing/assets/banner.css is missing -- copy "
                "design/banner.css there so symbulator.com matches"]
    if open(canon, encoding="utf-8").read() != open(copy, encoding="utf-8").read():
        return ["banner: landing/assets/banner.css has drifted from "
                "design/banner.css -- run "
                "cp design/banner.css landing/assets/banner.css"]
    return []


def _all_blocks(blocks: list[Node]):
    for b in blocks:
        yield b
        yield from _all_blocks(b.children)


def _check_block(b: Node, v, ch, labels, terms, known_versions, problems):
    texts = [b.text, b.arg] + [i for i in b.meta.get("items", [])]
    if b.kind == "code":
        vers = b.meta.get("versions") or []
        for cv in vers:
            if str(cv) not in known_versions and cv not in known_versions:
                problems.append(f"{ch.id}: code fence tagged unknown version {cv}")
        if b.meta.get("lang") == "field" and not b.meta.get("field"):
            problems.append(
                f"{ch.id}: a ```field fence must name the field, e.g. "
                f"```field 9 Circuit description -- the name is the "
                f"instruction, not decoration")
        return
    for t in texts:
        for n in parse_inline(t or ""):
            _check_inline(n, v, ch, labels, terms, known_versions, problems)
    for c in b.children:
        _check_block(c, v, ch, labels, terms, known_versions, problems)


def _check_inline(n: Node, v, ch, labels, terms, known_versions, problems):
    if n.kind == "ref" and n.text not in labels:
        problems.append(f"{ch.id}: cross-reference to unknown label "
                        f"'{n.text}' (v{v})")
    if n.kind == "term":
        if n.text not in terms:
            problems.append(f"{ch.id}: unknown term '{n.text}' "
                            f"— add it to book.yaml")
        elif v not in terms[n.text]:
            problems.append(f"{ch.id}: term '{n.text}' has no value for v{v}")
    if n.kind == "vspan":
        for sv in n.meta["versions"]:
            if str(sv) not in known_versions and sv not in known_versions:
                problems.append(f"{ch.id}: inline span for unknown version {sv}")
    for c in n.children:
        _check_inline(c, v, ch, labels, terms, known_versions, problems)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--web", action="store_true")
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--tex-only", action="store_true")
    ap.add_argument("--check", action="store_true",
                    help="validate the source and stop")
    ap.add_argument("--versions", default="7,8,9")
    a = ap.parse_args()
    versions = [int(x) for x in a.versions.split(",")]
    book = load_book()
    if a.check:
        sys.exit(1 if check(book, versions, verbose=True) else 0)
    if check(book, versions):
        print("build continuing despite the problems above", file=sys.stderr)
    do_all = not (a.web or a.pdf or a.tex_only)
    if a.web or do_all:
        build_web(book, versions)
    if a.pdf or a.tex_only or do_all:
        build_tex(book, versions, run_pdf=not a.tex_only)


if __name__ == "__main__":
    main()
