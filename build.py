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
import app_links  # noqa: E402  (#224: the app link on every worked problem)

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
BUILD = os.path.join(ROOT, "build")
ASSETS = os.path.join(ROOT, "assets")

# ---- figure sizes (#153) --------------------------------------------------
# tools/figure_sizes.json, written by tools/measure_figures.py, records the
# pixel size of every figure scan and the estimated height in pixels of the
# label text inside it. A figure is rendered at the width that puts that
# label text at target_mm -- the size of the body text -- capped at the
# line; the same proportion goes to the web as a percentage of the column.
# The scans' own pixel sizes are meaningless (most were resampled to a
# uniform 1100 px in 2023), which is why the old fixed 72%-of-the-line rule
# printed some labels at half the body size and others at triple.
FIGSIZES_PATH = os.path.join(ROOT, "tools", "figure_sizes.json")
try:
    with open(FIGSIZES_PATH, encoding="utf-8") as _fh:
        _FIGSIZES = json.load(_fh)
except FileNotFoundError:
    _FIGSIZES = {"target_mm": 3.4, "line_mm": 156.0,
                 "overrides": {}, "measured": {}}

FIG_LINE_MM = float(_FIGSIZES.get("line_mm", 156.0))
#: The desktop reading column in CSS pixels: --measure is 34rem in
#: web/assets/style.css at the 16px root. A figure's measured width in mm
#: becomes a pixel width at this column's scale (#256), so the labels
#: inside it are the same height on every screen -- a phone included --
#: instead of shrinking with the column as a percentage did.
MEASURE_PX = 544.0

#: #171: the most a problem may demand before it starts -- the title and
#: three lines or so. Above that it stops protecting a title and starts
#: throwing away the foot of the page.
PROBLEM_NEED_MAX = 34.0

#: #172: where a circuit may go. "h" first so it stays where it was
#: written whenever it fits; "t" for the top of the page it lands on.
#: Never "b" or "p" -- a circuit that sank to the foot of the page, or
#: to a page of its own, would be reached before the words that set it
#: up. "!" tells LaTeX to ignore its own fullness quotas, which are
#: tuned for journal figures, not for a circuit per worked problem.
FIGURE_FLOAT = "!ht"


def figure_size_mm(ref: str):
    """(width_mm, height_mm) to render a figure at, or (None, None).

    None means the manifest knows nothing about the file -- the renderers
    fall back to the old 72%-of-the-line rule, and a fresh run of
    tools/measure_figures.py is due.
    """
    rel = ref[len("assets/"):] if ref.startswith("assets/") else ref
    m = _FIGSIZES["measured"].get(rel)
    ov = _FIGSIZES["overrides"].get(rel)
    if ov is not None:
        w_mm = min(float(ov), FIG_LINE_MM)
        if m and m.get("w"):
            return (w_mm, w_mm * m["h"] / m["w"])
        return (w_mm, None)
    if not m or not m.get("text_px"):
        return (None, None)
    w_mm = min(m["w"] * float(_FIGSIZES["target_mm"]) / m["text_px"],
               FIG_LINE_MM)
    return (w_mm, w_mm * m["h"] / m["w"])

# The shared banner lockup's one source, in the app repository -- a
# sibling tree of this one (see the top-level CLAUDE.md for the
# layout). It lives there rather than here because the app's build
# inlines a copy it cannot fetch, and moving the source into that repo
# pins the lockup and the check to the same commit (#75).
SHARED_BANNER = os.path.normpath(os.path.join(
    ROOT, "..", "Application", "v9", "repos", "local", "banner.css"))


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


def title_for(ch, v) -> str:
    """A chapter's title for version v (#270, 6 Sep 2026). The title is
    front matter -- one string for all three versions -- but Lesson 2's
    must say *expert mode* in 7 and 8 and *Expert Mode* in 9, so it may
    carry the same version spans the body does: `{{v7,8|expert
    mode}}{{v9|Expert Mode}}`, or `{{!v7|...}}`. Only version spans are
    resolved; a title is printed raw everywhere (the h1, the sidebar's
    toc.json, the search index, the PDF's \\lesson and running foot),
    so no other markup belongs in one -- bold included."""
    def pick(m):
        neg, vers = m.group(1), [int(x) for x in m.group(2).split(",")]
        hit = v in vers
        return m.group(3) if hit != bool(neg) else ""
    return re.sub(r"\{\{(!?)v([\d,]+)\|([^}]*)\}\}", pick, ch.title)


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
              "answer", "practice", "only", "not", "web", "pdf", "address",
              "result"}

#: The label a ::: result panel shows over an answer, from the name in
#: front of it (#276) -- the app's own words, from _ELEMENT_KEYS and
#: _TOOL_LABELS in repos/server/symbulator_ui.py. The directive's argument
#: overrides it: `::: result node voltage`.
#: With the element named (Roberto, 6 Sep 2026 -- a departure from the
#: app, whose card shows the element once as a heading the reader of a
#: single panel cannot see): "current through r3", "voltage drop in c",
#: "power consumed by r1", "resistance seen by e".
RESULT_LABELS = {"i": "current through {}", "v": "voltage drop in {}",
                 "p": "power consumed by {}", "r": "resistance seen by {}",
                 "z": "impedance seen by {}", "s": "complex power in {}"}
RESULT_SPECIAL = {"v_{th}": "Thévenin voltage", "i_{no}": "Norton current",
                  "R_{eq}": "equivalent resistance",
                  "Z_{eq}": "equivalent impedance",
                  "p_{max}": "maximum deliverable power"}


def result_label(text: str, arg: str) -> str:
    """The label for a result panel: the argument if given, else derived
    from the name before the `=`; empty when there is no name."""
    if arg.strip():
        return arg.strip()
    m = re.match(r"\s*([A-Za-z]_\{[^}]*\})\s*&?=", text)
    if not m:
        return ""
    name = m.group(1)
    if name in RESULT_SPECIAL:
        return RESULT_SPECIAL[name]
    elem = re.sub(r"[\\{}]", "", name[3:-1])      # the subscript, plain
    return RESULT_LABELS.get(name[0], "").format(elem).strip()

#: The two output media. `::: web` / `::: pdf` blocks and `{{web|...}}` /
#: `{{pdf|...}}` spans show in one of them only; a pass that is not
#: rendering (labels, --check) sees both.
MEDIA = ("web", "pdf")

BS = chr(92)      # a LaTeX escape, spelled out so no editor eats it
NL = chr(10)      # a real newline in the emitted .tex

HEADING_RE = re.compile(r"^(#{2,3})\s+(.*?)(?:\s*\{#([\w-]+)\})?\s*$")
# ```field 9 Circuit description  -- lang, versions, then a free-text
# name for the interface field the reader types into. Only `field` uses
# the third part; for the others a stray word is a parse error rather
# than silent text.
FENCE_RE = re.compile(r"^```(\w+)?\s*([\d,]*)\s*(.*?)\s*$")
DIRECTIVE_RE = re.compile(r"^:::\s*(\w+)?\s*(.*)$")
ULI_RE = re.compile(r"^[-*]\s+(.*)$")
#: A pipe table, GitHub style, and the `|---|---|` rule under its header.
#: A row is only a row if the rule is on the line below the first one, so a
#: paragraph that happens to start with a pipe is still a paragraph.
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_RULE_RE = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
#: A quotation. `>` alone separates its paragraphs, as in Markdown.
QUOTE_RE = re.compile(r"^>\s?(.*)$")
#: An em dash or an en dash: how an attribution opens. Either is accepted,
#: because both are what people actually type.
QUOTE_DASHES = "\u2014\u2013"
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


def split_row(line: str) -> list:
    """One table row into its cells.

    An escaped pipe is a literal pipe rather than a cell boundary, which
    this book needs more than most: the calculator's "with" operator is a
    pipe, and it is discussed in the text."""
    body = line.strip().strip("|")
    parts = re.split(r"(?<!\\)\|", body)
    return [c.replace("\\|", "|").strip() for c in parts]


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
            if name == "result":            # #276: the body is LaTeX, kept raw
                node = Node(name, arg=arg, text="\n".join(l for l in inner if l.strip()))
            else:
                node = Node(name, arg=arg, children=parse_blocks(inner, path, depth + 1))
            out.append(node)
            i = i + 1 + consumed
            continue

        # table
        if (TABLE_ROW_RE.match(line) and i + 1 < len(lines)
                and TABLE_RULE_RE.match(lines[i + 1])):
            head = split_row(line)
            rows, j = [], i + 2
            while j < len(lines) and TABLE_ROW_RE.match(lines[j]):
                row = split_row(lines[j])
                if len(row) != len(head):
                    raise SourceError(
                        f"{path}: this table row has {len(row)} cell(s) "
                        f"where the header has {len(head)}:\n  "
                        f"{lines[j].strip()}\n"
                        f"  A cell holding a pipe has to write it as \\|.")
                rows.append(row)
                j += 1
            out.append(Node("table", meta={"head": head, "rows": rows}))
            i = j
            continue

        # quotation
        if QUOTE_RE.match(line):
            buf, j = [], i
            while j < len(lines) and QUOTE_RE.match(lines[j]):
                buf.append(QUOTE_RE.match(lines[j]).group(1))
                j += 1
            out.append(Node("quote", children=parse_blocks(buf, path, depth)))
            i = j
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
                or OLI_RE.match(lines[j]) or QUOTE_RE.match(lines[j])
                or (TABLE_ROW_RE.match(lines[j]) and j + 1 < len(lines)
                    and TABLE_RULE_RE.match(lines[j + 1]))):
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

# `\*` is a literal asterisk -- the multiplication sign in an answer the
# software gave back, as in **{.904\*vs,10952.}**. Until 2 Sep 2026 there
# was no escape at all: the interior `*` broke the `**...**` match, the
# stars then re-paired themselves across the rest of the paragraph, and
# the sentence rendered with scrambled italics and a stray `*` left over.
# Eleven lines across four lessons were doing this and nobody had looked.
#
# The escape set is deliberately just `*` and `\` -- NOT a general `\.`.
# A backslash is ordinary content here: the calculator's own namespace is
# written `s\dc`, `s\tr`, `s\rms`, and a general escape would eat those.
#
# Hence the atom `(?:\\[*\\]|[^*])`, in that order and not the other way
# round. The escape alternative goes first so `\*` is swallowed whole and
# its star cannot close the span; `[^*]` then still admits a *lone*
# backslash, which is what keeps **s\bode** bold. Writing the atom as
# `(?:[^*\\]|\\[*\\])` looks equivalent and is not -- it bans ordinary
# backslashes from emphasis entirely, and silently un-bolded every
# `**s\...**` in the book. Only a diff of the built pages showed it.
#
# One level of nesting each way (#263, 5 Sep 2026): an italic span may
# hold `**...**` runs -- *"**symb**olic sim**ulator**"* in the
# Introduction -- and a bold span may hold `*...*` runs -- `**Tick *real
# solutions only*.**` in Lesson 11. Each body admits a whole group of the
# other kind as one atom, so the inner stars cannot close the outer span;
# the body is then parsed again and the group becomes a node inside.
# The inner group is the plain form, so the nesting stops at one level.
# Strong is still tried first at any position, so a plain `**bold**`
# never reads as an italic that happens to start with a star. A side
# effect: `***x***`, which used to print a stray star and then bold, now
# reads as bold inside italic; no source writes it. Before this rule the
# Introduction's line rendered as five italic runs with no bold, and the
# Lesson 11 bullet as two stray stars and two fragments of italic -- the
# span closed at the first inner star and the stars re-paired down the
# rest of the paragraph.
INLINE_RE = re.compile(
    r"(?P<esc>\\[*\\])"
    r"|(?P<brace>\{\{(?:[^{}]|\{[^{}]*\})*\}\})"
    r"|(?P<code>`[^`]+`)"
    r"|(?P<math>\$[^$]+\$)"
    r"|(?P<link>\[[^\]]+\]\([^)]+\))"
    r"|(?P<strong>\*\*(?:\\[*\\]|\*(?:\\[*\\]|[^*])+\*|[^*])+\*\*)"
    r"|(?P<em>\*(?:\\[*\\]|\*\*(?:\\[*\\]|[^*])+\*\*|[^*])+\*)"
)


def parse_inline(text: str) -> list[Node]:
    out, pos = [], 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            out.append(Node("text", text=text[pos:m.start()]))
        kind = m.lastgroup
        s = m.group()
        if kind == "esc":
            out.append(Node("text", text=s[1]))
        elif kind == "brace":
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


_ANSWER_MATH_CACHE: dict = {}


def answer_math(text: str):
    """LaTeX for an `{{o:...}}` value that is a symbolic expression, or None.

    An answer the software gave back is quoted verbatim in the source --
    `i*exp(-t/(c*r))/c` -- and until 27 Aug 2026 rendered as that plain
    text. When the value parses to a SymPy expression that actually
    contains symbols, it is typeset as mathematics instead (KaTeX on the
    web, math mode in the PDFs); a bare number, a braced pair like
    {4.77,7.18}, or anything else that does not parse keeps the plain
    `.ans` treatment it always had. The source text is untouched either
    way, so `tools/check_against_originals.py` and the verify harness
    keep reading the value exactly as printed."""
    if text in _ANSWER_MATH_CACHE:
        return _ANSWER_MATH_CACHE[text]
    result = None
    if re.search(r"[a-zA-Z]", text) and not re.search(r"[{}\\]", text):
        try:
            import sympy as sp
            expr = sp.sympify(text)
            if getattr(expr, "free_symbols", None):
                result = sp.latex(expr)
        except Exception:                                     # noqa: BLE001
            result = None
    _ANSWER_MATH_CACHE[text] = result
    return result


def parse_brace(inner: str) -> Node:
    if inner.startswith("i:"):
        return Node("index", text=inner[2:].strip())
    if inner.startswith("t:"):
        return Node("term", text=inner[2:].strip())
    if inner.startswith("ref:"):
        return Node("ref", text=inner[4:].strip())
    if inner.startswith("o:"):          # an answer the software gave back
        return Node("answer_span", text=inner[2:].strip())
    if inner.startswith("var:"):        # a problem's own variable (#261)
        return Node("var", text=inner[4:].strip())
    if inner.startswith("sub:"):
        return Node("sub", text=inner[4:].strip())
    if inner.startswith("sup:"):
        return Node("sup", text=inner[4:].strip())
    m = re.match(r"^(web|pdf)\|(.*)$", inner, re.S)
    if m:                               # {{web|...}} / {{pdf|...}}
        return Node("mspan", arg=m.group(1), children=parse_inline(m.group(2)))
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
            name = f"Lesson {number}" if number else title_for(ch, v)
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


def walk(blocks: list[Node], v: int, medium: str | None = None):
    """Yield blocks visible in version v, flattening only/not wrappers.

    `medium` is "web" or "pdf" while rendering; a `::: web` or `::: pdf`
    block is flattened when it matches and dropped when it does not. With
    no medium (labels, --check) both are kept, so an anchor defined in
    either is known everywhere."""
    for b in blocks:
        if b.kind in MEDIA:
            if medium is None or medium == b.kind:
                yield from walk(b.children, v, medium)
            continue
        if b.kind in ("only", "not"):
            if keep(b, v):
                yield from walk(b.children, v, medium)
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
        # #224. Version 9 is the only one with an app to open a problem
        # in, so the books are read only when they can be used -- a v7
        # build does not reach into the app tree at all.
        self.books = app_links.load_books() if version == 9 else {}
        self.entries: list = []      # the entries of each problem, in order
        self.problem_no = 0          # which problem the renderer is on
        self.problem_ids: set = set()
        self.medium = "web"

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
            ltx = answer_math(n.text)
            if ltx:
                return f'<span class="ans ans-math">\\({ltx}\\)</span>'
            return f'<span class="ans">{html.escape(n.text)}</span>'
        if n.kind == "var":
            # #261: a variable the problem itself names -- I_s, v_o, R_L --
            # as distinct from the name Symbulator files the answer under
            # (`ir3`, in code). Bold italic, Roberto's choice of 5 Sep 2026;
            # `_` starts a subscript, so {{var:I_s}} is I with s below.
            base, _, sb = n.text.partition("_")
            sb = f'<sub>{html.escape(sb)}</sub>' if sb else ""
            # <em class="var">, weight 600 in style.css (#271): the site
            # loads Plex Serif's italic 600 cut for it, so the browser no
            # longer fakes a bold italic by slanting the semibold roman.
            return f'<em class="var">{html.escape(base)}{sb}</em>'
        if n.kind == "sub":
            return f'<sub>{html.escape(n.text)}</sub>'
        if n.kind == "sup":
            return f'<sup>{html.escape(n.text)}</sup>'
        if n.kind == "vspan":
            hit = self.v in n.meta["versions"]
            show = (not hit) if n.arg == "!" else hit
            return "".join(self.inode(c) for c in n.children) if show else ""
        if n.kind == "mspan":
            return ("".join(self.inode(c) for c in n.children)
                    if n.arg == self.medium else "")
        return ""

    # -- blocks ----------------------------------------------------------
    def blocks(self, blocks: list[Node]) -> str:
        return "\n".join(self.block(b) for b in walk(blocks, self.v, self.medium))

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
        if k == "table":
            # A blank header row means the table has no header -- see
            # chapter 13's gain answers, which are a label against a value.
            head = ("" if not any(c.strip() for c in b.meta["head"]) else
                    "<thead><tr>"
                    + "".join(f"<th>{self.inline(c)}</th>"
                              for c in b.meta["head"])
                    + "</tr></thead>")
            body = "".join(
                "<tr>" + "".join(f"<td>{self.inline(c)}</td>" for c in row)
                + "</tr>" for row in b.meta["rows"])
            # Wrapped, because a wide table has to scroll inside its own
            # column rather than widen the page. The measure is the point of
            # this layout, and a table is the one block that will not
            # respect it on its own.
            return (f'<div class="table-wrap"><table>{head}'
                    f'<tbody>{body}</tbody></table></div>')
        if k == "quote":
            # The attribution is a paragraph starting with a dash. Detected
            # rather than marked up, so the source stays ordinary Markdown --
            # which is what someone writing a quotation types anyway, without
            # having to be told a rule.
            parts = []
            for child in walk(b.children, self.v, self.medium):
                if child.kind == "para" and child.text.lstrip()[:1] in QUOTE_DASHES:
                    parts.append(f'<p class="quote-by">'
                                 f'{self.inline(child.text)}</p>')
                else:
                    parts.append(self.block(child))
            return "<blockquote>" + "".join(parts) + "</blockquote>"
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
            # A ```text fence is neither typed nor returned -- it is a
            # listing, such as the contents of a .cir file. Labelling it
            # "returns" would say it came out of Symbulator, which is the
            # one thing it did not do. So it gets no label at all.
            if b.meta["lang"] == "text":
                return f'<div class="code plain"><pre><code>{body}</code></pre></div>'
            cls = "sym" if b.meta["lang"] == "sym" else "out"
            label = "type" if cls == "sym" else "returns"
            return (f'<div class="code {cls}"><span class="code-label">{label}'
                    f'</span><pre><code>{body}</code></pre></div>')
        if k == "result":
            # #276: a card answer as the app shows it -- the label over the
            # typeset answer, on the returned-output panel (.code.out's
            # colours, so it follows the page's mode like every panel).
            label = html.escape(result_label(b.text, b.arg))
            lab = f'<span class="code-label">{label}</span>' if label else ""
            return (f'<div class="code result">{lab}'
                    f'<div class="mathblock">\\[{html.escape(b.text)}\\]</div></div>')
        if k == "address":
            # #259: an address to share, on a line of its own, centred, on
            # the input panel's tint. The argument is the URL as it should
            # be read (no scheme); the link target adds https:// unless a
            # scheme is already there. Escaped verbatim, not run through
            # inline(): a URL wants no curly quotes and no emphasis.
            text = b.arg.strip()
            href = text if re.match(r"^[a-z][a-z0-9+.-]*://", text) else "https://" + text
            return (f'<p class="address"><a href="{html.escape(href)}">'
                    f'{html.escape(text)}</a></p>')
        if k in ("tip", "note", "warning", "danger"):
            title = (f'<p class="callout-title">{self.inline(b.arg)}</p>'
                     if b.arg else "")
            return (f'<aside class="callout {k}">{callout_head(k)}'
                    f'{title}{self.blocks(b.children)}</aside>')
        if k == "figure":
            cap = self.blocks(b.children)
            # #153 measured the width in mm that puts a figure's labels at
            # body-text size; #256 turns it into pixels at the desktop
            # column's scale rather than a share of whatever column the
            # reader has. On a desktop that is the same width as before;
            # on a phone the figure keeps its size and the column, not the
            # figure, gives way -- capped at 100% so nothing overflows.
            w_mm, _h = figure_size_mm(b.arg)
            style = (f' style="width:min(100%,{w_mm * MEASURE_PX / FIG_LINE_MM:.0f}px)"'
                     if w_mm else "")
            return (f'<figure><img src="{html.escape(site_path(b.arg))}"'
                    f' alt=""{style}>'
                    f'<figcaption>{cap}</figcaption></figure>')
        if k == "problem":
            pid, links = self.problem_furniture(b)
            return (f'<section class="problem"{pid}><p class="problem-title">'
                    f'{self.inline(b.arg)}</p>{links}'
                    f'{self.blocks(b.children)}</section>')
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

    def problem_furniture(self, b: Node) -> tuple[str, str]:
        """#224: a worked problem's anchor, and its links into the app.

        Two anchors, doing different jobs. The section gets one built
        from its title, so every problem can be linked to -- including
        the fifteen the app has no entry for. Each *entry* gets one of
        its own, `e-6a-3`, on the link that opens it: the split view is
        handed ?lesson=6a&entry=3 and has to scroll the left pane to the
        matching place, and deriving `#e-6a-3` from the query costs it no
        lookup table. An entry anchor has to sit on the link rather than
        on the section, because a problem is often several entries -- a
        DC pass for the initial condition, then the TR -- and only one of
        them could own the section.

        The links go after the title paragraph, never inside it:
        SEARCH_PROBLEM reads that paragraph to label a search hit, and
        putting them in would rename every hit in the book.
        """
        n, self.problem_no = self.problem_no, self.problem_no + 1
        # From the source title, not the rendered one: inline() turns the
        # apostrophe in "Bo2's" into &#x27;, and slugifying that gives
        # prob-bo2x27s-example-51. slugify already drops version spans.
        base = slugify(b.arg)
        pid = f"prob-{base}"
        i = 2
        while pid in self.problem_ids:
            pid, i = f"prob-{base}-{i}", i + 1
        self.problem_ids.add(pid)
        entries = self.entries[n] if n < len(self.entries) else []
        if not entries:
            return f' id="{pid}"', ""
        rows = []
        for e in entries:
            label = app_links.entry_label(e, b.arg) if len(entries) > 1 else ""
            tag = (f'<span class="applink-tag">{html.escape(label)}</span>'
                   if label else "")
            rows.append(
                f'<span class="applink-row">{tag}'
                f'<a class="applink" id="{e.anchor}" href="{html.escape(e.app_href)}"'
                f' target="_blank" rel="noopener"'
                f' data-lesson="{e.lesson}" data-entry="{e.index}">'
                f'Open in app ↗</a>'
                f'<a class="splitlink" href="{html.escape(e.split_href)}">'
                f'Open in split view</a></span>')
        return f' id="{pid}"', f'<p class="problem-links">{"".join(rows)}</p>'

    def chapter(self, ch: Chapter, number, present: bool) -> str:
        self.chapter_id, self.chapter_no, self.section_no = ch.id, number, 0
        # #224. Resolved for the whole chapter up front, because an entry
        # is claimed by one problem and which problem that is depends on
        # the ones around it. Both walks are walk(blocks, v), so the order
        # here is the order the renderer will meet them in.
        self.problem_no, self.problem_ids, self.entries = 0, set(), []
        if self.v == 9 and present and ch.id in app_links.CHAPTER_BOOKS:
            self.entries = app_links.resolve_chapter(
                ch.id, app_links.chapter_problems(ch, self.v), self.books)
        # An eyebrow is the small line above a chapter title -- "Lesson 3".
        # A chapter with no number has nothing useful to put there, and
        # falling back to the title printed it twice: "Introduction /
        # Introduction", "Roll the credits / Roll the credits", on the
        # chapter page, in the sidebar and on the home page cards.
        eyebrow = f"Lesson {number}" if number else ""
        parts = ['<header class="chapter-head">']
        if eyebrow:
            parts.append(f'<p class="eyebrow">{html.escape(eyebrow)}</p>')
        parts.append(f'<h1>{html.escape(title_for(ch, self.v))}</h1>')
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
          # IBM Plex (mono and serif alike) has no Greek: β, γ and both
          # mus -- U+03BC and the micro sign U+00B5 -- rendered as tofu
          # boxes in every code block that names a transistor gain (#156,
          # 29 Aug 2026). The XeLaTeX log's "Missing character" lines are
          # the authority on this list; check them after adding glyphs.
          "β": r"\ensuremath{\beta}", "γ": r"\ensuremath{\gamma}",
          "μ": r"\ensuremath{\mu}", "µ": r"\ensuremath{\mu}",
          # Plex Serif has superscript four but not superscript minus.
          "⁻": r"\textsuperscript{-}",
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
        #: how many tcolorboxes deep we are. A float cannot leave one.
        self.boxdepth = 0
        self.medium = "pdf"

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
            ltx = answer_math(n.text)
            if ltx:
                return r"\ansmath{" + ltx + "}"
            return r"\ans{" + tex_escape(n.text) + "}"
        if n.kind == "var":                  # #261, see the HTML side
            base, _, sb = n.text.partition("_")
            sb = r"\textsubscript{" + tex_escape(sb) + "}" if sb else ""
            return r"\symvar{" + tex_escape(base) + sb + "}"   # #271
        if n.kind == "sub":
            return r"\textsubscript{" + tex_escape(n.text) + "}"
        if n.kind == "sup":
            return r"\textsuperscript{" + tex_escape(n.text) + "}"
        if n.kind == "vspan":
            hit = self.v in n.meta["versions"]
            show = (not hit) if n.arg == "!" else hit
            return "".join(self.inode(c) for c in n.children) if show else ""
        if n.kind == "mspan":
            return ("".join(self.inode(c) for c in n.children)
                    if n.arg == self.medium else "")
        return ""

    def blocks(self, blocks: list[Node]) -> str:
        return "\n\n".join(x for x in (self.block(b)
                                       for b in walk(blocks, self.v, self.medium)) if x)

    def _problem_need(self, b: Node) -> float:
        """Millimetres a problem needs before it is worth starting.

        Enough for the rule, the title and the opening lines of the
        statement -- no more. #152 used to add the first figure's height
        too, and cap the demand at 170mm; that is what emptied the foot
        of one page in six, because a problem whose circuit would not fit
        moved wholesale and left everything it had been standing on
        behind. The circuits float now (#172), so they no longer need to
        be reserved for, and the demand is back to what it is for: a
        title must not be the last thing on a page. Estimates are rough
        -- a paragraph line is guessed from its character count.
        """
        need = 11.0                          # the rule, the title, the air
        for child in list(walk(b.children, self.v, self.medium))[:4]:
            if child.kind == "para":
                need += 6.0 * max(1, round(len(child.text) / 90))
            else:
                break
        return min(need, PROBLEM_NEED_MAX)

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
        if k == "table":
            # tabularx, so the last column takes up the slack and wraps.
            # The tables in this book are a short key against a long line
            # of prose, which a plain tabular runs off the page with.
            cols = len(b.meta["head"])
            # @{} at both ends so the table lines up with the text
            # block instead of sitting a column-gap inside it.
            spec = "@{}" + ("l" * (cols - 1) + "X" if cols > 1 else "X") + "@{}"
            rows = [" & ".join(self.inline(c) for c in row)
                    for row in b.meta["rows"]]
            nl = " " + BS * 2 + NL
            if any(c.strip() for c in b.meta["head"]):
                header = (" & ".join(self.inline(c) for c in b.meta["head"])
                          + nl + BS + "midrule" + NL)
            else:
                header = ""
            return (BS + "begin{tabularx}{" + BS + "linewidth}{" + spec
                    + "}" + NL + BS + "toprule" + NL + header
                    + nl.join(rows) + nl
                    + BS + "bottomrule" + NL + BS + "end{tabularx}")
        if k == "quote":
            parts = []
            for child in walk(b.children, self.v, self.medium):
                if (child.kind == "para"
                        and child.text.lstrip()[:1] in QUOTE_DASHES):
                    parts.append(BS + "quoteby{"
                                 + self.inline(child.text) + "}")
                else:
                    parts.append(self.block(child))
            return (BS + "begin{symquote}" + NL + NL.join(parts)
                    + NL + BS + "end{symquote}")
        if k == "code":
            # A field is typed input with the field's name over it (#277,
            # Roberto, 6 Sep 2026 -- until then the PDF set it as plain
            # typed input, the sentence above naming the field): symfield
            # in the class, symtype's box with a label line.
            env = ("symtype" if b.meta["lang"] == "sym" else
                   "symfield" if b.meta["lang"] == "field" else
                   "symlisting" if b.meta["lang"] == "text" else "symout")
            head = ("" if env != "symfield"
                    else "{" + tex_escape(b.meta.get("field") or "") + "}")
            def _listing_line(line):
                # A blank line still has to be a line. These are joined with
                # \\, and \\ after nothing at all is "There's no line here
                # to end" -- which is how the .cir example in the
                # introduction, the first fence in the book with a blank
                # line in it, stopped the PDF build.
                if not line.strip():
                    return BS + "mbox{}"
                # A line starting with "[" would be read as \\'s optional
                # argument, so it is fenced off with an empty group.
                return (("{}" + tex_code(line))
                        if line.lstrip().startswith("[") else tex_code(line))

            lines = (BS * 2 + NL).join(
                _listing_line(l) for l in b.text.split(chr(10)))
            return f"\\begin{{{env}}}{head}\n{lines}\n\\end{{{env}}}"
        if k == "result":                    # #276, the PDF side
            label = tex_escape(result_label(b.text, b.arg))
            return (f"\\begin{{symresult}}{{{label}}}\n\\[{b.text}\\]\n"
                    f"\\end{{symresult}}")
        if k == "address":
            # #259, the PDF side: \symaddress in symbulator.cls. The
            # target escapes what hyperref reads specially, the way the
            # inline link does; the printed text goes through tex_escape.
            text = b.arg.strip()
            href = text if re.match(r"^[a-z][a-z0-9+.-]*://", text) else "https://" + text
            href = href.replace("%", r"\%").replace("#", r"\#")
            return f"\\symaddress{{{href}}}{{{tex_escape(text, prose=False)}}}"
        if k in ("tip", "note", "warning", "danger"):
            title = self.inline(b.arg) if b.arg else ""
            self.boxdepth += 1               # no floats in here (#172)
            body = self.blocks(b.children)
            self.boxdepth -= 1
            return (f"\\begin{{callout{k}}}{{{title}}}\n"
                    f"{body}\n\\end{{callout{k}}}")
        if k == "figure":
            src = (b.arg if b.arg.lower().endswith((".png", ".jpg", ".jpeg"))
                   else os.path.splitext(b.arg)[0])
            cap = self.blocks(b.children)
            # #153: measured width, capped at \linewidth by \symfig; the
            # fallback is the old 72% rule for a file the manifest has
            # not met yet.
            w_mm, _h = figure_size_mm(b.arg)
            img = (f"\\symfig{{{w_mm:.1f}}}{{{src}}}" if w_mm
                   else f"\\includegraphics[width=\\figwidth]{{{src}}}")
            if self.boxdepth:
                # Inside a callout, which is a tcolorbox: LaTeX will not
                # let a float out of a box, so this one stays put.
                return ("\\begin{symfigure}\n"
                        f"{img}\n"
                        f"\\caption{{{cap}}}\n\\end{{symfigure}}")
            return (f"\\begin{{figure}}[{FIGURE_FLOAT}]\\centering\n"
                    f"{img}\n"
                    f"\\caption{{{cap}}}\n\\end{{figure}}")
        if k == "problem":
            # #171: a problem's title must not be the last thing on a
            # page. The plain \\needspace, not the starred
            # \\Needspace*: the starred one fills out the page it breaks
            # from, which only moves the blank from the foot to the middle.
            return (f"\\needspace{{{self._problem_need(b):.0f}mm}}\n"
                    f"\\begin{{problem}}{{{self.inline(b.arg)}}}\n"
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
            head.append(f"\\lesson{{{number}}}{{{tex_escape(title_for(ch, self.v))}}}")
        else:
            head.append(f"\\frontchapter{{{tex_escape(title_for(ch, self.v))}}}")
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


#: Sections of the built page, for the sidebar search. One entry per `##`
#: heading, plus one for whatever comes before the first -- so a hit can be
#: linked to the anchor the reader wants, not just the page.
SEARCH_SPLIT = re.compile(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', re.S)


def plain(html_text: str) -> str:
    """The words of a rendered page, with the markup taken out."""
    text = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", html_text)
    # #224's app links are furniture, not words. Left in, "Open in app"
    # would be part of the searchable text of 265 problems, so a search
    # for "app" would return most of the book.
    text = re.sub(r'(?is)<p class="problem-links">.*?</p>', " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


#: A worked problem inside a section. Not an anchor -- problems have no id --
#: but the name a reader recognises, so a hit lands as "AS7's Example 12.10"
#: rather than as "Further wye-wye problems".
SEARCH_PROBLEM = re.compile(r'<p class="problem-title">(.*?)</p>', re.S)


def search_entries(chapter_id: str, title: str, body: str) -> list[dict]:
    """Entries for one built chapter: one per section, split again at each
    worked problem so a hit can name the problem it is in."""
    out = []

    def add(anchor, heading, raw):
        pos, label = 0, ""
        for m in SEARCH_PROBLEM.finditer(raw):
            chunk = plain(raw[pos:m.start()])
            if chunk:
                out.append({"p": chapter_id, "c": title, "a": anchor,
                            "s": heading, "q": label, "t": chunk})
            label = plain(m.group(1))
            pos = m.end()
        chunk = plain(raw[pos:])
        if chunk:
            out.append({"p": chapter_id, "c": title, "a": anchor,
                        "s": heading, "q": label, "t": chunk})

    pos, anchor, heading = 0, "", ""
    for m in SEARCH_SPLIT.finditer(body):
        add(anchor, heading, body[pos:m.start()])
        anchor, heading = m.group(1), plain(m.group(2))
        pos = m.end()
    add(anchor, heading, body[pos:])
    return out


def build_web(book: Book, versions: list[int]):
    outroot = os.path.join(BUILD, "web")
    for v in versions:
        vdir = os.path.join(outroot, "content", f"v{v}")
        os.makedirs(vdir, exist_ok=True)
        r = HtmlRenderer(book, v)
        toc, search = [], []
        for ch, number, present in book.for_version(v):
            body = r.chapter(ch, number, present)
            open(os.path.join(vdir, ch.id + ".html"), "w",
                 encoding="utf-8").write(body)
            if present:
                search += search_entries(ch.id, title_for(ch, v), body)
            sections = []
            if present:
                n = 0
                for b in walk(ch.blocks, v, "web"):
                    if b.kind == "heading" and b.meta["level"] == 2:
                        n += 1
                        sections.append({"anchor": b.meta["anchor"],
                                         "title": re.sub(r"\{\{[^}]*\}\}", "", b.text),
                                         "number": f"{number}.{n}" if number else ""})
            toc.append({"id": ch.id, "title": title_for(ch, v),
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
        # The search index is per version, because the search is: a reader
        # of version 8 must not be shown a hit that only exists in 9.
        json.dump(search, open(os.path.join(vdir, "search.json"), "w",
                               encoding="utf-8"), ensure_ascii=False,
                  separators=(",", ":"))
    # copy the PHP front end and static assets next to the content
    # `split` is #224's shell: a real directory, so it needs no .htaccess
    # rule -- the rewrite there only claims ^[789], and DirectoryIndex
    # serves /split/ on its own.
    for name in ("index.php", ".htaccess", "favicon.ico", "assets", "split"):
        s, d = os.path.join(ROOT, "web", name), os.path.join(outroot, name)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    # #224. The split view has to turn ?lesson=6a into a chapter to open
    # its left pane on, and #226 needs the other direction: the ribbon's
    # "Split View" link carries ?page=lesson-transient, and the app pane
    # opens on that chapter's first book. Written from CHAPTER_BOOKS
    # rather than restated in the shell, so that the map the links are
    # generated from and the map the shell reads them back with are the
    # same one.
    #
    # Both directions are written out rather than one being inverted in
    # the page, because JavaScript does not keep an object's key order
    # for keys that look like array indices: {"1":…,"10":…,"4a":…} comes
    # back as 1, 10, 4a, so "the chapter's first book" would silently be
    # the wrong one for Lesson 1 against Lesson 10.
    json.dump({"lessons": {key: cid
                           for cid, keys in app_links.CHAPTER_BOOKS.items()
                           for key in keys},
               "chapters": {cid: keys[0]
                            for cid, keys in app_links.CHAPTER_BOOKS.items()
                            if keys}},
              open(os.path.join(outroot, "split", "lessons.json"), "w",
                   encoding="utf-8"), indent=1)
    # The banner is shared with symbulator.com and the app. Its one
    # source is banner.css in the app's repository (Application/v9/repos/
    # local -- moved there Aug 2026 so the app build, which inlines a
    # copy it cannot fetch, guards against a file in its own commit);
    # this build copies the same file in rather than duplicating it
    # inside style.css.
    if not os.path.isfile(SHARED_BANNER):
        raise SystemExit(
            f"build.py: {SHARED_BANNER} is missing. The shared banner "
            "lockup lives in the app repository (Application/v9/repos/local, "
            "a sibling tree's grandchild of Documentation -- see the "
            "top-level CLAUDE.md); without it this site cannot build its "
            "header.")
    shutil.copy2(SHARED_BANNER, os.path.join(outroot, "assets", "banner.css"))
    # The monograph (paper/symbulator_monograph.pdf, tracked in this
    # repository) ships beside the three tutorial PDFs, under the same
    # hyphenated naming its shelf-mates use. The ribbon and footer of
    # index.php link it on every version, and the landing page links
    # the same URL.
    monograph = os.path.join(ROOT, "paper", "symbulator_monograph.pdf")
    if not os.path.isfile(monograph):
        raise SystemExit(
            f"build.py: {monograph} is missing. Build it with xelatex in "
            "Documentation/paper/ (twice, for the TOC), or the site would "
            "ship a dead link.")
    shutil.copy2(monograph, os.path.join(outroot, "monograph.pdf"))
    # The Symbulator Book (paper/the_symbulator_book.pdf) -- the
    # completed English edition of the 2001 thesis -- ships beside the
    # monograph, and the landing page links both.
    symbook = os.path.join(ROOT, "paper", "the_symbulator_book.pdf")
    if not os.path.isfile(symbook):
        raise SystemExit(
            f"build.py: {symbook} is missing. Build it with xelatex in "
            "Documentation/paper/ (twice, for the TOC), or the site would "
            "ship a dead link.")
    shutil.copy2(symbook, os.path.join(outroot, "book.pdf"))
    if os.path.isdir(ASSETS):
        shutil.copytree(ASSETS, os.path.join(outroot, "assets"),
                        dirs_exist_ok=True)
    json.dump({"versions": {str(k): val for k, val in book.meta["versions"].items()},
               "title": book.meta["title"], "subtitle": book.meta["subtitle"]},
              open(os.path.join(outroot, "content", "book.json"), "w",
                   encoding="utf-8"), indent=1)
    print(f"web:  {outroot}")


def build_tex(book: Book, versions: list[int], run_pdf=True) -> list[int]:
    """Write the .tex for each version and, unless asked not to, compile
    it. Returns the versions whose PDF did not get built, so the caller
    can fail the run rather than exiting 0 with nothing to show."""
    failed: list[int] = []
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
            if not compile_pdf(texdir, f"symbulator-v{v}", pdfdir):
                failed.append(v)

    if failed:
        missing = ", ".join(f"v{v}" for v in failed)
        print(f"\nNO PDF PRODUCED for {missing}. Anything already in "
              f"{os.path.join(BUILD, 'pdf')} is from an earlier run and is "
              f"NOT this build.", file=sys.stderr)

    # index.php links /symbulator-v7.pdf and friends, so they belong at the
    # document root -- which is build/web, the folder the deploy uploads.
    # Without this they stayed in build/pdf and no rebuild ever reached the
    # site. Only what was built this run is copied: a failed version must
    # not silently promote the previous build's PDF.
    webdir = os.path.join(BUILD, "web")
    if run_pdf and os.path.isdir(webdir):
        for v in versions:
            if v in failed:
                continue
            built = os.path.join(pdfdir, f"symbulator-v{v}.pdf")
            if os.path.isfile(built):
                shutil.copy2(built, os.path.join(webdir,
                                                 f"symbulator-v{v}.pdf"))
                print(f"web:  {os.path.join(webdir, f'symbulator-v{v}.pdf')}")

    return failed


def compile_pdf(texdir: str, stem: str, pdfdir: str) -> bool:
    """Build one PDF. Returns True only if a PDF was actually written.

    The return value is load-bearing: this used to print xelatex's error
    and return None, which nothing checked, so a run where every pass
    ended in "No pages of output" still exited 0 and left the previous
    build's PDFs sitting in build/pdf looking like the result."""
    env = dict(os.environ, TEXINPUTS=f".:{texdir}:")
    for i in range(3):
        # encoding is explicit because text=True would decode through the
        # Windows code page: xelatex writes UTF-8, cp1252 cannot represent
        # byte 0x90, and the reader thread died mid-log rather than
        # reporting anything useful.
        p = subprocess.run(["xelatex", "-interaction=nonstopmode",
                            "-halt-on-error", stem + ".tex"],
                           cwd=texdir, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=env)
        if p.returncode != 0:
            log = "\n".join(l for l in p.stdout.split("\n")
                            if l.startswith("!") or "l." == l[:2])[-2500:]
            print(f"xelatex failed on {stem} (pass {i+1}):\n{log}", file=sys.stderr)
            tail = p.stdout[-2500:]
            print(tail, file=sys.stderr)
            return False
        if i == 0:
            subprocess.run(["makeindex", "-q", stem + ".idx"], cwd=texdir,
                           capture_output=True)
    # xelatex can exit 0 and still write nothing -- a missing font ends in
    # "No pages of output" without a non-zero status. Check for the file
    # rather than trusting the exit code.
    built = os.path.join(texdir, stem + ".pdf")
    if not os.path.isfile(built):
        print(f"xelatex produced no {stem}.pdf (see "
              f"{os.path.join(texdir, stem + '.log')})", file=sys.stderr)
        return False
    # A clean exit is not a visible book: the 29 Aug 2026 A4 build shipped
    # pages whose text was painted white (a tcolorbox colour leak) with a
    # clean log. Render-and-compare catches invisible text whatever its
    # cause; see tools/check_white_text.py.
    from check_white_text import check_white_text
    bad = check_white_text(built)
    if bad:
        print(f"{stem}.pdf has INVISIBLE TEXT on page(s) {bad} -- "
              f"see tools/check_white_text.py", file=sys.stderr)
        return False
    shutil.copy2(built, os.path.join(pdfdir, stem + ".pdf"))
    print(f"pdf:  {os.path.join(pdfdir, stem + '.pdf')}")
    return True


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
    # The sidebar search is three pieces in three files with nothing else
    # tying them together -- the index this file writes, the markup and
    # script in web/index.php, and the rules in web/assets/style.css.
    problems.extend(check_search(versions))

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


def check_search(versions: list[int]) -> list[str]:
    """The search (#87) is written here and consumed there; keep them in step.

    Nothing else would notice a rename. The index is emitted by build_web
    into content/v<N>/search.json; web/index.php fetches that exact path and
    fills two elements by id; web/assets/style.css styles them. Break any one
    of those and the box still renders and simply never finds anything --
    which is the failure this catches. Where a build already exists, the
    index is also checked for covering every chapter of its version, so a
    half-written index is not mistaken for a working one."""
    out = []
    php = os.path.join(ROOT, "web", "index.php")
    css = os.path.join(ROOT, "web", "assets", "style.css")
    php_text = open(php, encoding="utf-8").read() if os.path.isfile(php) else ""
    css_text = open(css, encoding="utf-8").read() if os.path.isfile(css) else ""
    for needle, where in (('/content/v' + "' + version + '" + '/search.json', php),
                          ('id="docsearch"', php),
                          ('id="docsearch-results"', php),
                          ('id="docsearch-status"', php)):
        if needle not in php_text:
            out.append(f"search: {os.path.basename(where)} no longer has "
                       f"{needle!r} -- the sidebar search cannot work")
    for needle in (".docsearch", ".docsearch-results", ".docsearch-snip"):
        if needle not in css_text:
            out.append(f"search: style.css has no {needle} rule")

    for v in versions:
        built = os.path.join(BUILD, "web", "content", f"v{v}", "search.json")
        toc = os.path.join(BUILD, "web", "content", f"v{v}", "toc.json")
        if not (os.path.isfile(built) and os.path.isfile(toc)):
            continue                      # nothing built yet; nothing to check
        entries = json.load(open(built, encoding="utf-8"))
        pages = {e.get("p") for e in entries}
        for ch in json.load(open(toc, encoding="utf-8"))["chapters"]:
            if ch["present"] and ch["id"] not in pages:
                out.append(f"search: v{v}'s index has nothing for "
                           f"{ch['id']} -- rebuild before deploying")
    return out


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
    opener = re.compile(r"\{\{(?:v(?:7|8|9|7,8|7,9|8,9)|web|pdf)\|")
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
    """The banner is one file -- banner.css in the app repository
    (Application/v9/repos/local) -- imported by this site and copied
    verbatim into landing/. The landing page has no build step, so its
    copy can silently fall behind -- which is exactly how the lockup
    drifted before it was centralised. Compare them and complain
    loudly."""
    copy = os.path.join(ROOT, "landing", "assets", "banner.css")
    if not os.path.isfile(SHARED_BANNER):
        return [f"banner: the canonical banner.css is missing at "
                f"{SHARED_BANNER} -- the app repository "
                "(Application/v9/repos/local) must sit beside "
                "Documentation's own sibling folder, Application; "
                "see the top-level CLAUDE.md"]
    if not os.path.isfile(copy):
        return ["banner: landing/assets/banner.css is missing -- copy "
                "the canonical banner.css there so symbulator.com matches"]
    if open(SHARED_BANNER, encoding="utf-8").read() != \
            open(copy, encoding="utf-8").read():
        return ["banner: landing/assets/banner.css has drifted from the "
                f"canonical {SHARED_BANNER} -- copy it across"]
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
        if build_tex(book, versions, run_pdf=not a.tex_only):
            sys.exit(1)


if __name__ == "__main__":
    main()
