#!/usr/bin/env python3
"""Sentences that promise something the reader is then not shown.

"Below is how I describe this one:" followed by the calculator fences is
fine for versions 7 and 8 and empty for version 9, which never renders
them. Roberto found one that way in section 9.2: the description looked
missing, because the panel supplying it had been placed further down the
page, after the observations that discuss it.

The check reads the built pages rather than the source, because the
question is what a reader of *that version* is actually shown. A promise
is a paragraph ending in a colon. It is satisfied by a block that can
answer it -- a panel, a code block, a list, a figure, a table -- or by a
following paragraph that carries the answer inline, as `{{o:...}}` does.
Prose that merely carries on talking does not satisfy it.

    py tools/check_dangling_promises.py          # every built version
    py tools/check_dangling_promises.py 9        # just version 9
"""
import glob
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build", "web", "content")

#: Blocks that answer a promise by themselves.
SATISFIES = ("pre", "table", "ul", "ol", "figure", "div", "aside")

#: The subset that can answer a promise *through* an intervening sentence.
#: A figure is deliberately not one of them: "the answer is: ... as you can
#: see in the book's answer below:" is how a missing answer reads, and
#: letting a figure reach back past a sentence hides exactly that.
SATISFIES_VIA = ("pre", "table", "ul", "ol", "div", "aside")

#: A paragraph answers one only if it actually carries a value or a name:
#: an {{o:}} answer span, code such as a field name or an expression, or
#: set maths -- an answer that is an expression is set as maths and lands in
#: a paragraph of its own, which is what made this check unusable before.
INLINE_ANSWER = re.compile(r'<span class="(?:ans|math)"|<code')

#: A colon that introduces something, rather than punctuating a clause.
PROMISE = re.compile(r"[A-Za-z0-9`*_)\]]\s*:\s*$")

#: The longest run of letters an *expression* ever has. `cos`, `sin`, `e`,
#: `t`, `vc`, `il`, `r1` -- three. Every sentence in the book has a longer
#: word than that, so this tells an answer set apart from prose without
#: needing the source to mark it up.
WORDY = re.compile(r"[A-Za-z]{4,}")


def is_expression(text: str) -> bool:
    """A paragraph that is an answer rather than a sentence about one."""
    return (bool(text) and not WORDY.search(text)
            and bool(re.search(r"[0-9/*+=(){}]", text)))


def blocks_of(page: str):
    return re.findall(r"<(p|pre|table|ul|ol|figure|div|aside)\b[^>]*>(.*?)</\1>",
                      page, re.S)


def check(version: str = "") -> list[str]:
    problems = []
    for path in sorted(glob.glob(os.path.join(BUILD, "v*", "*.html"))):
        v = os.path.basename(os.path.dirname(path)).lstrip("v")
        if version and v != version:
            continue
        name = os.path.basename(path)
        blocks = blocks_of(open(path, encoding="utf-8").read())
        for i, (tag, body) in enumerate(blocks):
            if tag != "p":
                continue
            text = html.unescape(re.sub(r"<[^>]+>", "", body)).strip()
            if not text or not PROMISE.search(text):
                continue
            nxt_tag, nxt_body = blocks[i + 1] if i + 1 < len(blocks) else ("", "")
            if nxt_tag in SATISFIES:
                continue
            if nxt_tag == "p" and INLINE_ANSWER.search(nxt_body):
                continue
            if nxt_tag == "p" and is_expression(
                    html.unescape(re.sub(r"<[^>]+>", "", nxt_body)).strip()):
                continue
            # One sentence may stand between a promise and its answer --
            # "...reads:" / "With polar phasors on, each one reads:" / the
            # list. Chain through it, but only to a block that is itself an
            # answer rather than a picture.
            if nxt_tag == "p":
                nxt_text = html.unescape(re.sub(r"<[^>]+>", "", nxt_body)).strip()
                after_tag = blocks[i + 2][0] if i + 2 < len(blocks) else ""
                if PROMISE.search(nxt_text) and after_tag in SATISFIES_VIA:
                    continue
            problems.append(f'v{v} {name}: "{text[-64:]}"')
    return problems


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    found = check(sys.argv[1] if len(sys.argv) > 1 else "")
    for p in found:
        print("  " + p)
    print(f"\n{len(found)} promise(s) with nothing to answer them")
    sys.exit(1 if found else 0)
