#!/usr/bin/env python3
"""Put back the practice answers that were Word equations.

`tools/import_practice.py` reads runs of text. An answer Roberto set as a
Word equation is not a run of text, so it was dropped -- silently, because
the sentence promising it came through fine. The result is dozens of places
where a reader is told "we get the expression below" and shown nothing, and
the 27 literal `{ , , }` in chapter 6, which are the same loss where he
happened to type the braces around it.

This reads the equations out of the .docx and writes them back, anchored on
the paragraph that introduces each one. An answer whose anchor cannot be
found unambiguously is reported and left alone.

    py tools/restore_practice_answers.py           # report
    py tools/restore_practice_answers.py --write   # apply
"""
import glob
import io
import os
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
PRACTICE = (r"C:\Users\perez\OneDrive\_High Archive\_High Archive - Personal"
            r"\Documents\Roberto\Creaciones\Symbulator\Websites\2023 Website"
            r"\practice\7")

#: How much of the introducing sentence has to match, in letters and digits.
ANCHOR = 40


# ------------------------------------------------------- the Word equations --

def _kid(node, name):
    return node.find(M + name)


def _parens(s):
    s = s.strip()
    if re.fullmatch(r"-?[\w.]+", s) or re.fullmatch(r"-?\([^()]*\)", s):
        return s
    return "(%s)" % s


def render(node):
    """One OMML subtree, in the documentation's own markup."""
    tag = node.tag.split("}")[-1]
    if tag == "t":
        return (node.text or "").replace("\u00ad", "-").replace("\u2212", "-")
    if tag == "sSup":
        return "%s{{sup:%s}}" % (render(_kid(node, "e")),
                                 render(_kid(node, "sup")).strip())
    if tag == "sSub":
        return "%s{{sub:%s}}" % (render(_kid(node, "e")),
                                 render(_kid(node, "sub")).strip())
    if tag == "f":
        return "%s/%s" % (_parens(render(_kid(node, "num"))),
                          _parens(render(_kid(node, "den"))))
    if tag == "d":
        return "(%s)" % "".join(render(e) for e in node.findall(M + "e"))
    if tag in ("rPr", "ctrlPr", "sSupPr", "sSubPr", "fPr", "dPr", "radPr"):
        return ""
    # A fraction followed by anything has to be bracketed: Word sets it over
    # two lines, and one line has to say the same thing.
    parts = [(c.tag.split("}")[-1], render(c)) for c in node]
    out = []
    for i, (tag2, text) in enumerate(parts):
        nxt = next((s.strip() for _, s in parts[i + 1:] if s.strip()), "")
        if tag2 == "f" and (nxt[:1].isalnum() or nxt[:1] == "("):
            text = "(%s)" % text
        out.append(text)
    return "".join(out)


def paragraphs(path):
    """(style, text, [equations]) for every paragraph, in order."""
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    for para in root.iter(W + "p"):
        ppr = para.find(W + "pPr")
        style = ""
        if ppr is not None:
            st = ppr.find(W + "pStyle")
            if st is not None:
                style = st.get(W + "val") or ""
        text = "".join(t.text or "" for t in para.iter(W + "t")).strip()
        eqs = [re.sub(r"\s+", " ", render(m)).strip()
               for m in para.iter(M + "oMath")]
        yield style, text, [e for e in eqs if e]


def wanted():
    """(problem, sentence before, sentence after, [equations]) per equation.

    Both neighbours, because Roberto writes it either way round: "Evaluating
    vo we get:" ahead of the answer, or "which is correct, as can be seen..."
    behind it. Only one of the two survives in the sources often enough to
    anchor on."""
    out = []
    for path in sorted(glob.glob(os.path.join(PRACTICE, "*.docx"))):
        title, anchor, pending = None, "", []
        paras = list(paragraphs(path))
        for style, text, eqs in paras:
            if style == "Heading4":
                for item in pending:
                    out.append(item + ("",))
                pending = []
                title, anchor = text, ""
                continue
            if text and style not in ("CalcType", "CalcTypeFree"):
                for item in pending:
                    out.append(item + (text,))
                pending = []
            if eqs and title:
                pending.append((title, anchor, eqs))
            if text and style not in ("CalcType", "CalcTypeFree"):
                anchor = text
        for item in pending:
            out.append(item + ("",))
    return out


# -------------------------------------------------------------- the sources --

def key(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def chapters():
    """{path: [lines]} for every chapter."""
    return {p: io.open(p, encoding="utf-8").read().split("\n")
            for p in sorted(glob.glob(os.path.join(SRC, "*.md")))}


def problem_span(lines, title):
    """(first, last) line indices of one `::: problem` body, or None."""
    want = key(title)
    start = None
    for i, line in enumerate(lines):
        m = re.match(r"^::: problem (.+)$", line)
        if not m:
            continue
        if start is not None:
            return start, i
        if key(m.group(1)) == want:
            start = i
    return (start, len(lines)) if start is not None else None


def paragraph_span(lines, first, last, anchor):
    """(first line, last line) of the paragraph matching `anchor`, or None."""
    want = key(anchor)[:ANCHOR]
    if len(want) < 20:
        return None
    i, hits = first, []
    while i < last:
        if lines[i].startswith("```"):                  # skip a code fence
            i += 1
            while i < last and not lines[i].startswith("```"):
                i += 1
            i += 1
            continue
        if not lines[i].strip() or lines[i].startswith(":::"):
            i += 1
            continue
        j = i
        while (j + 1 < last and lines[j + 1].strip()
               and not lines[j + 1].startswith("```")
               and not lines[j + 1].startswith(":::")):
            j += 1
        if want in key(" ".join(lines[i:j + 1])):
            hits.append((i, j))
        i = j + 1
    return hits[0] if len(hits) == 1 else None


def main():
    write = "--write" in sys.argv
    books = chapters()
    done = skipped = 0
    edits = {}                                       # path -> [(after, text)]
    for title, anchor, eqs, follows in wanted():
        target = None
        for path, lines in books.items():
            span = problem_span(lines, title)
            if span:
                target = (path, lines, span)
                break
        if not target:
            skipped += len(eqs)
            print("  no such problem: %s" % title)
            continue
        path, lines, (first, last) = target
        body = key("\n".join(lines[first:last]))
        missing = [e for e in eqs if key(e) not in body]
        if not missing:
            continue
        span = paragraph_span(lines, first, last, anchor)
        at = span[1] if span else None
        if at is None:                      # try the sentence after instead
            span = paragraph_span(lines, first, last, follows)
            at = span[0] - 1 if span else None
        if at is None:
            skipped += len(missing)
            print("  %s  %s" % (os.path.basename(path), title))
            print("      no single anchor for: %r / %r"
                  % (anchor[:56], follows[:56]))
            for eq in missing:
                print("      unplaced: %s" % eq)
            continue
        text = (missing[0] if len(missing) == 1
                else "{ " + " , ".join(missing) + " }")
        edits.setdefault(path, []).append((at, text))
        done += 1
        print("  %s:%d  %s" % (os.path.basename(path), at + 1, title))
        print("      + %s" % text)

    if write:
        for path, items in edits.items():
            lines = books[path]
            grouped = {}
            for at, text in items:            # two answers can share one
                grouped.setdefault(at, []).append(text)   # introduction
            for at in sorted(grouped, reverse=True):
                block = []
                for text in grouped[at]:
                    block += ["", text]
                lines[at + 1:at + 1] = block
            io.open(path, "w", encoding="utf-8",
                    newline="\n").write("\n".join(lines))
        print("\n%d restored, %d left alone -- written" % (done, skipped))
    else:
        print("\n%d to restore, %d left alone" % (done, skipped))
        print("dry run -- pass --write to apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
