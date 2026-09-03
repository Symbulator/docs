#!/usr/bin/env python3
"""
Derive the Symbulator 8 variant of every practice-problem command from the
Symbulator 7 one, and gate the imported problems so version 9 does not show
problems whose code has not been translated yet.

The practice documents are shared between versions 7 and 8 — they are the same
files, byte for byte — so the prose, the schematics and the answers need no
duplication. Only the commands differ, and only in narrow, known ways:

    unary minus  ->  the Nspire's negate sign (–)
    s\\rms        ->  userms

Everything else is left alone. Every line that changes is reported, so the
translation can be checked rather than trusted.

    python3 tools/derive_v8.py --report          # show what would change
    python3 tools/derive_v8.py --apply           # write it
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")

NEGATE = "\u2013"          # the character version 8's documentation uses

# a minus is a *negate* when nothing can be subtracted from what precedes it
UNARY_MINUS = re.compile(r'(?<=[(,{:=+*/^\s"])-|^-')

FENCE = re.compile(r"```sym 7\n(.*?)\n```", re.S)
INLINE = re.compile(r"`([^`\n]+)`")

V9_NOTE = """::: only 9
::: note These problems are still in calculator notation
The solved problems below were written for the calculator versions, and their
commands have not been translated to Symbulator 9 yet. The circuits and the
answers are the same; only the way you ask for them differs. Until they are
converted, read them alongside {{ref:introduction}} and translate as you go.
:::
:::
"""


def to_v8(line: str) -> str:
    out = UNARY_MINUS.sub(NEGATE, line)
    out = out.replace("s\\rms", "userms")
    return out


def practice_span(text: str):
    """Where the chapter's practice block starts and ends.

    A chapter may have several practice blocks, and they are not always the
    last thing in the file, so find the matching close by counting depth
    rather than assuming it runs to the end.
    """
    lines = text.split("\n")
    start_line = next((i for i, l in enumerate(lines)
                       if l.startswith("::: practice")), None)
    if start_line is None:
        return None
    depth = 0
    for i in range(start_line, len(lines)):
        line = lines[i].strip()
        if line == ":::":
            depth -= 1
            if depth == 0:
                start = sum(len(l) + 1 for l in lines[:start_line])
                end = sum(len(l) + 1 for l in lines[:i + 1])
                return start, end
        elif line.startswith(":::"):
            depth += 1
    return None


def process(path: str, apply: bool):
    text = open(path, encoding="utf-8").read()
    span = practice_span(text)
    if span is None:
        return 0, 0, []
    start, end = span
    head, block, tail = text[:start], text[start:end], text[end:]

    if "::: only 7,8" in block:
        return 0, 0, ["already processed"]

    changes, added = [], 0

    def twin(m):
        nonlocal added
        v7 = m.group(1)
        v8 = "\n".join(to_v8(l) for l in v7.split("\n"))
        added += 1
        if v8 != v7:
            for a, b in zip(v7.split("\n"), v8.split("\n")):
                if a != b:
                    changes.append((a, b))
        return f"```sym 7\n{v7}\n```\n```sym 8\n{v8}\n```"

    block = FENCE.sub(twin, block)

    # inline references need the same treatment, or a version 8 reader is told
    # to evaluate -pe while the command right below it says –pe
    def inline_twin(m):
        v7 = m.group(1)
        if "{{" in v7:                       # already version-tagged
            return m.group(0)
        v8 = to_v8(v7)
        if v8 == v7:
            return m.group(0)
        changes.append((v7, v8))
        return "{{v7|`" + v7 + "`}}{{v8|`" + v8 + "`}}"

    parts, out = block.split("```"), []
    for i, part in enumerate(parts):
        out.append(part if i % 2 else INLINE.sub(inline_twin, part))
    block = "```".join(out)

    # gate the whole thing: versions 7 and 8 see the problems, version 9 a note
    lines = block.split("\n")
    opener = lines[0]                                   # '::: practice ...'
    body = "\n".join(lines[1:]).rstrip()
    if body.endswith(":::"):
        body = body[:-3].rstrip()
    block = (f"{opener}\n\n::: only 7,8\n{body}\n:::\n\n{V9_NOTE}:::\n")

    if apply:
        shutil.copy2(path, path + ".bak")
        open(path, "w", encoding="utf-8").write(head + block + tail)
    return added, len(changes), changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("chapters", nargs="*")
    a = ap.parse_args()
    if not (a.apply or a.report):
        a.report = True

    files = a.chapters or sorted(
        os.path.join(SRC, f) for f in os.listdir(SRC)
        if f.endswith(".md") and "TODO" not in
        open(os.path.join(SRC, f), encoding="utf-8").read())

    total_cmds = total_changed = 0
    for path in files:
        added, changed, changes = process(path, a.apply)
        if not added and not changes:
            continue
        name = os.path.basename(path)
        if changes and changes[0] == "already processed":
            print(f"{name}: already processed, skipped")
            continue
        total_cmds += added
        total_changed += changed
        print(f"\n{name}: {added} commands, {changed} lines differ in v8")
        seen = set()
        for v7, v8 in changes:
            if v7 in seen:
                continue
            seen.add(v7)
            print(f"    7  {v7}")
            print(f"    8  {v8}")
    print(f"\n{total_cmds} commands, {total_changed} lines changed"
          + ("" if a.apply else "  (nothing written; pass --apply)"))


if __name__ == "__main__":
    main()
