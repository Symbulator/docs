#!/usr/bin/env python3
"""Answers that disagree between version 9 and versions 7 and 8.

The circuits and the questions are the same in all three versions, so the
answers have to be too. Where they are not, a passage was rewritten and the
rewrite changed a number -- which is the thing to examine.

Two things that are not disagreements, and are filtered out:

*   Precision. 1.357 and 1.36 are the same answer, so two numbers match
    when they agree to the *lesser* of the two precisions -- -6.34 matches
    a printed -6.3, and 6.809 matches 6.81.
*   Subscripts. The 11 in z11 is a parameter name, not a value, so a digit
    run glued to a letter is skipped.

    py tools/check_answer_parity.py            # every chapter
    py tools/check_answer_parity.py 09         # one chapter

Reported per problem:

    only in 7/8    the printed answer has a number version 9 never shows
    only in 9      version 9 shows a number the printed answer does not

Both directions matter. The first is an answer that went missing in the
rewrite; the second is the shape of a silent correction.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")

#: Minus is written three ways in this book: ASCII -, en dash, and the
#: real minus sign. All three count.
MINUS = "-–−"

#: A number as either version writes one: 6.809ᴇ0, 1e-6, .0588, –2. --
#: but never the digits of a subscript such as z11 or v_2.
NUM = re.compile(
    r"(?<![A-Za-z0-9_])[" + MINUS + r"]?"
    r"(?:\d+(?:\.\d+)?|\.\d+)"
    r"(?:[eEᴇ][" + MINUS + r"]?\d+)?")

FENCE = re.compile(r"^```([^\n]*)\n(.*?)^```", re.M | re.S)
ANSWER9 = re.compile(r"\{\{o:(.*?)\}\}", re.S)

#: Power factor direction is an answer too, and a flipped word is exactly
#: the shape a silent correction takes.
WORDS = ("leading", "lagging")


def parse(tok: str):
    """(value, significant figures), or None if the token isn't a number."""
    plain = tok.replace("–", "-").replace("−", "-")
    plain = plain.replace("ᴇ", "e")
    try:
        v = float(plain)
    except ValueError:
        return None
    digits = re.sub(r"[-+.]|[eE].*$", "", plain).lstrip("0")
    return v, max(1, len(digits))


def numbers(text: str):
    out = []
    for tok in NUM.findall(text):
        got = parse(tok)
        if got:
            out.append(got)
    return out


def same(a, b) -> bool:
    """Two answers agreeing to the lesser of their two precisions."""
    (va, pa), (vb, pb) = a, b
    p = max(1, min(pa, pb))
    return f"{va:.{p}g}" == f"{vb:.{p}g}"


def unmatched(these, those):
    """Values in `these` that nothing in `those` matches."""
    out = []
    for a in these:
        if not any(same(a, b) for b in those):
            out.append(a[0])
    return sorted(set(out))


def segments(text: str):
    marks = [(m.start(), m.group(1).strip())
             for m in re.finditer(r"^::: problem (.*)$", text, re.M)]
    marks += [(m.start(), m.group(1).strip())
              for m in re.finditer(r"^## (.*)$", text, re.M)]
    marks.sort()
    for i, (pos, title) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        yield title, text[pos:end]


def split_versions(body: str):
    old, new = [], []
    for info, block in FENCE.findall(body):
        kind = info.split()
        if not kind or kind[0] != "out":
            continue
        vers = "".join(kind[1:])
        if any(v in vers for v in "78"):
            old += numbers(block)
        elif "9" in vers:
            new += numbers(block)
    for m in ANSWER9.finditer(body):
        new += numbers(m.group(1))
    return old, new


def words_of(body: str):
    old_words, new_words = set(), set()
    for info, block in FENCE.findall(body):
        kind = info.split()
        if kind and kind[0] == "out" and any(v in "".join(kind[1:])
                                             for v in "78"):
            old_words |= {w for w in WORDS if w in block.lower()}
    for chunk in re.findall(r"^::: only 9$(.*?)^:::$", body, re.M | re.S):
        new_words |= {w for w in WORDS if w in chunk.lower()}
    return old_words, new_words


def check(only: str = ""):
    findings = []
    for path in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        name = os.path.basename(path)
        if only and not name.startswith(only):
            continue
        text = open(path, encoding="utf-8").read()
        for title, body in segments(text):
            old, new = split_versions(body)
            if not old or not new:
                continue
            gone, added = unmatched(old, new), unmatched(new, old)
            ow, nw = words_of(body)
            flip = bool(ow and nw and ow != nw)
            if gone or added or flip:
                findings.append((name, title, gone, added, ow, nw, flip))
    return findings


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    found = check(sys.argv[1] if len(sys.argv) > 1 else "")
    for name, title, gone, added, ow, nw, flip in found:
        print(f"\n{name}  --  {title}")
        if gone:
            print("    only in 7/8:  " +
                  ", ".join(f"{v:g}" for v in gone))
        if added:
            print("    only in 9:    " +
                  ", ".join(f"{v:g}" for v in added))
        if flip:
            print(f"    WORD FLIP:    7/8 say {'/'.join(sorted(ow))}, "
                  f"9 says {'/'.join(sorted(nw))}")
    print(f"\n\n{len(found)} problem(s) where the versions disagree")
