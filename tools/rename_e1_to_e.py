#!/usr/bin/env python3
"""Version 9's lone voltage source is `e`, not `e1`.

`e` is Euler's number on both calculators, so a source could not be called
that and every circuit with one source called it `e1`. Version 9 has no such
collision -- the banned list is derived and comes to two names, neither of
them `e` -- so the `1` in `e1` now means nothing at all.

Only circuits where `e1` is the *only* source of its kind are renamed. A
circuit with `e1` and `e2` is numbering two sources, which is meaningful and
stays, exactly as `ra0` and `raa` stay in chapter 9.

Versions 7 and 8 are untouched: their calculators have the real restriction.
So the rename reaches only what a version 9 reader sees -- the `field 9`
panels, the `::: only 9` blocks and the `{{v9|...}}` halves of a span. Any
mention left in prose that all three versions read is reported instead of
changed, because there the two spellings have to be split by hand.

    py tools/rename_e1_to_e.py           # report
    py tools/rename_e1_to_e.py --write   # apply
"""
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")

PANEL = re.compile(r"^```field 9 Circuit Description\s*$")
FIELD = re.compile(r"^```field 9\b")
FENCE = re.compile(r"^```")

#: `e1` itself and every answer version 9 derives from it. `re1` is left out
#: on purpose: a resistor of that name already exists in chapter 3, put there
#: to dodge SymPy's `re`, and the two would be indistinguishable.
NAMES = {"e1": "e", "ie1": "ie", "ve1": "ve", "pe1": "pe", "se1": "se",
         "ze1": "ze", "ape1": "ape"}
TOKEN = re.compile(r"(?<![\w])(" + "|".join(sorted(NAMES, key=len, reverse=True))
                   + r")(?![\w])")


def swap(text):
    return TOKEN.sub(lambda m: NAMES[m.group(0)], text)


def sole_e(body):
    """True if this panel's only source named e-something is `e1`."""
    names = [b.split(",")[0].strip() for b in body if b.strip()]
    return [n for n in names if n.startswith("e")] == ["e1"]


def regions(lines):
    """(start, end, sole) for each stretch governed by one circuit panel."""
    starts = [i for i, ln in enumerate(lines) if PANEL.match(ln)]
    out = []
    for k, i in enumerate(starts):
        j = i + 1
        body = []
        while j < len(lines) and not FENCE.match(lines[j]):
            body.append(lines[j])
            j += 1
        end = starts[k + 1] if k + 1 < len(starts) else len(lines)
        out.append((i, end, sole_e(body)))
    return out


def rewrite_region(lines, start, end, report):
    """Rename inside everything a version 9 reader sees. Returns a count."""
    changed = 0
    i, in_only9 = start, 0
    depth9 = None
    while i < end:
        line = lines[i]
        if FENCE.match(line):
            keep = bool(FIELD.match(line))
            i += 1
            while i < end and not FENCE.match(lines[i]):
                if keep:
                    new = swap(lines[i])
                    if new != lines[i]:
                        lines[i], changed = new, changed + 1
                i += 1
            i += 1
            continue
        if re.match(r"^::: only 9\s*$", line):
            in_only9 += 1
            depth9 = in_only9
        elif line.startswith(":::") and depth9 and line.strip() == ":::":
            depth9 = None
        elif re.match(r"^::: only [78]", line):
            depth9 = None
        if depth9:
            new = swap(line)
        else:
            # Outside a version 9 block only the {{v9|...}} half may move.
            new = re.sub(r"\{\{(v9|!v7,8|!v8,7)\|([^}]*)\}\}",
                         lambda m: "{{%s|%s}}" % (m.group(1), swap(m.group(2))),
                         line)
            if new == line and TOKEN.search(line) and not line.startswith("```"):
                report.append((i + 1, line.strip()))
        if new != line:
            lines[i], changed = new, changed + 1
        i += 1
    return changed


def main():
    write = "--write" in sys.argv
    total = 0
    left = []
    for path in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        lines = io.open(path, encoding="utf-8").read().split("\n")
        report = []
        changed = 0
        for start, end, sole in regions(lines):
            if sole:
                changed += rewrite_region(lines, start, end, report)
        if changed:
            print("  %-28s %4d line(s)" % (os.path.basename(path), changed))
            total += changed
        for line_no, text in report:
            left.append("%s:%d  %s" % (os.path.basename(path), line_no, text))
        if changed and write:
            io.open(path, "w", encoding="utf-8",
                    newline="\n").write("\n".join(lines))
    if left:
        print("\n%d line(s) mention e1 where all three versions read them --"
              " split these by hand:" % len(left))
        for item in left[:60]:
            print("   " + item)
        if len(left) > 60:
            print("   ... and %d more" % (len(left) - 60))
    print("\n%d line(s) renamed%s" % (total, " -- written" if write else ""))
    if not write:
        print("dry run -- pass --write to apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
