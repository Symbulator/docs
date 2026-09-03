#!/usr/bin/env python3
"""Carry the imported practice problems into Symbulator 9.

    py tools/add_v9_practice.py              # dry run: report, change nothing
    py tools/add_v9_practice.py --apply      # do it
    py tools/add_v9_practice.py --apply --only 03-lesson-sources.md

The practice sections were imported for the calculator versions and sit
inside `::: only 7,8`, so a version 9 reader sees none of them. Two changes
put them back:

1.  **Unwrap** the `::: only 7,8` that hides a whole practice section.
2.  **Add a `field 9` panel** beside every calculator fence that is a plain
    circuit description, showing the same circuit the way version 9 wants
    it typed -- one element per line, in the Circuit description box.

What it deliberately does NOT do is rewrite prose. A sentence like "press
Enter and evaluate ir1" is wrong for version 9, but rewriting 200 of them
mechanically would produce 200 bad sentences. Instead every such line is
reported, chapter by chapter, so they can be fixed by hand or in a later
pass.

Safe to re-run: a fence that already has a `field 9` block after it is left
alone, and an already-unwrapped section is skipped.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_calls

SRC = Path(__file__).resolve().parent.parent / "src"

# s\dc("..."), s\ac("...", 60), s\ex("..."), s\tr(...), s\fd(...)
CALL_RE = re.compile(r'^s\\(dc|ac|ex|fd|tr)\("([^"]*)"(.*)\)\s*$')

FENCE_OPEN = re.compile(r"^```(\w+)?\s*([\d,]*)\s*(.*?)\s*$")

# Prose that plainly speaks to a calculator and will read as nonsense in the
# version 9 build once the section is unwrapped.
CALC_PROSE = re.compile(
    r"\b(press enter|press ENTER|hit enter|evaluate\s+[a-z]+\d|"
    r"\bapprox\(|when done|first level variables|"
    r"\bDelVar\b|the calculator|your calculator|s\\)", re.I)


EN_DASH = "–"


def split_elements(desc: str) -> list[str]:
    """Split a circuit description on its top-level colons.

    Colons inside brackets or parentheses belong to a nested construct --
    pr(...) and the [r,r] shorthand -- and are not element separators.

    The en dash becomes an ASCII minus on the way through. Thirteen of these
    descriptions write a negative value as `j01,0,1,-8` with U+2013, which is
    correct for the calculators -- the TI-89 has a separate negation key and
    the source represents it faithfully -- and is refused outright by
    Symbulator 9: "Circuit description contains characters that aren't used
    in Symbulator syntax." Only the version 9 panel is converted; the
    calculator fences above it keep their en dash untouched."""
    desc = desc.replace(EN_DASH, "-")
    out, depth, cur = [], 0, ""
    for ch in desc:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == ":" and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [e.strip() for e in out if e.strip()]


def convert(text: str, unwrap: bool = False) -> tuple[str, dict]:
    """Return the new text and a report of what changed."""
    lines = text.split("\n")
    out: list[str] = []
    stats = {"panels": 0, "unwrapped": 0, "skipped_existing": 0,
             "has_old_v9": 0, "skipped_odd": [], "prose": []}

    # --- pass 1: unwrap `::: only 7,8` that wraps a whole practice section --
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == "::: practice":
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].strip() == "::: only 7,8":
                # find its matching close: the last ::: before the practice
                # block's own close. Count directive depth from here.
                depth = 1
                k = j + 1
                close = None
                while k < len(lines):
                    s = lines[k].strip()
                    if s.startswith("::: "):
                        depth += 1
                    elif s == ":::":
                        depth -= 1
                        if depth == 0:
                            close = k
                            break
                    k += 1
                if close is not None and unwrap:
                    del lines[close]
                    del lines[j]
                    stats["unwrapped"] += 1
                    continue
        i += 1

    # --- pass 2: a field 9 panel beside every plain description fence ------
    i = 0
    while i < len(lines):
        line = lines[i]
        m = FENCE_OPEN.match(line)
        if not (m and m.group(1) == "sym" and m.group(2) in ("7", "8")):
            out.append(line)
            i += 1
            continue

        # gather the fence
        body, j = [], i + 1
        while j < len(lines) and not lines[j].startswith("```"):
            body.append(lines[j])
            j += 1
        out.append(line)
        out.extend(body)
        if j < len(lines):
            out.append(lines[j])
        i = j + 1

        if m.group(2) != "8":
            continue                      # only act after the 8 of a 7/8 pair

        # Already dealt with? Two ways that can be true, and both mean hands
        # off.
        #
        # A `field` fence after this one is a panel someone already wrote.
        #
        # A `sym 9` fence is the previous author's Python version of the same
        # instruction. Adding a panel in front of it would leave the chapter
        # saying two different things -- type this into a box, and also call
        # this function. Those fences are wrong and have to go, but replacing
        # them is a judgement about what the surrounding prose should now say,
        # which is the chapter rewrite's job, not a script's.
        nxt = i
        while nxt < len(lines) and not lines[nxt].strip():
            nxt += 1
        if nxt < len(lines) and lines[nxt].startswith("```field"):
            stats["skipped_existing"] += 1
            continue
        if nxt < len(lines) and lines[nxt].startswith("```sym 9"):
            stats["has_old_v9"] += 1
            continue

        # A call may be wrapped across several lines for width; join it back
        # before matching, since the line breaks are typography, not syntax.
        joined = " ".join(l.strip() for l in body if l.strip())
        joined = joined.replace(", ", ",") if joined.count('"') >= 2 else joined
        produced = v9_calls.convert(joined)
        if produced is None:
            if joined.startswith("s\\"):
                stats["skipped_odd"].append(joined[:70])
            continue
        out.extend(produced)
        stats["panels"] += 1

    new = "\n".join(out)

    # --- pass 3: report prose that will now reach a version 9 reader -------
    #
    # Only prose counts. A calculator command inside a ```sym 7 or ```sym 8
    # fence is not a problem: those fences are dropped from the version 9
    # build. What matters is the sentences around them, which are shared.
    in_practice = False
    fence_ver: str | None = None          # None when not inside a fence
    only9 = 0                             # depth inside a ::: only 9 block
    for n, line in enumerate(new.split("\n"), 1):
        stripped = line.strip()
        if stripped == "::: practice":
            in_practice = True
        if line.startswith("```"):
            if fence_ver is None:
                m = FENCE_OPEN.match(line)
                fence_ver = (m.group(2) if m else "") or "all"
            else:
                fence_ver = None
            continue
        if fence_ver is not None:
            continue                      # inside a fence: not prose
        # Text inside `::: only 9` is version 9 text already. It is allowed to
        # mention the calculators -- often it must, to say what it replaces --
        # so flagging it is noise. Doing so produced 21 false positives against
        # prose this very script had written.
        if only9:
            if stripped.startswith("::: "):
                only9 += 1
            elif stripped == ":::":
                only9 -= 1
            continue
        if stripped == "::: only 9":
            only9 = 1
            continue
        if in_practice and CALC_PROSE.search(strip_calc_branches(line)):
            stats["prose"].append((n, stripped[:88]))
    return new, stats


def strip_calc_branches(line: str) -> str:
    """Drop the {{v7|...}}, {{v8|...}} and {{v7,8|...}} halves of a line.

    A passage that has already been made version-aware is done, and its
    calculator branch is *supposed* to say "evaluate `vr3`" -- that is the
    calculator's instruction and it stays. Only what a version 9 reader will
    actually see should be searched, or every fixed line stays on the
    worklist forever, which is how four already-fixed passages in lesson 1
    were reported as outstanding."""
    out, i = [], 0
    while i < len(line):
        m = re.compile(r"\{\{v(?:7|8|7,8)\|").match(line, i)
        if not m:
            out.append(line[i])
            i += 1
            continue
        depth, j = 1, m.end()
        while j < len(line) - 1 and depth:
            if line[j:j + 2] == "{{":
                depth += 1; j += 2; continue
            if line[j:j + 2] == "}}":
                depth -= 1; j += 2; continue
            j += 1
        i = j
    return "".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true",
                    help="write the changes (default is a dry run)")
    ap.add_argument("--unwrap", action="store_true",
                    help="ALSO reveal the practice section to version 9. Only "
                         "do this for a chapter whose prose has been fixed: "
                         "unwrapping first is how 566 sentences telling a "
                         "browser user to press Enter reach the live site.")
    ap.add_argument("--worklist", metavar="FILE",
                    help="write the flagged prose lines to a file, to work through")
    ap.add_argument("--only", metavar="FILE",
                    help="just this one file, e.g. 03-lesson-sources.md")
    ap.add_argument("--prose", action="store_true",
                    help="list every calculator-flavoured line, not just a count")
    args = ap.parse_args()

    files = sorted(SRC.glob("*.md"))
    if args.only:
        files = [f for f in files if f.name == args.only]
        if not files:
            sys.exit(f"No such file in src/: {args.only}")

    tot = {"panels": 0, "unwrapped": 0, "existing": 0, "odd": 0, "prose": 0}
    worklist: list[str] = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        if "::: practice" not in text:
            continue
        new, st = convert(text, unwrap=args.unwrap)
        if new == text and not st["prose"]:
            continue
        print(f"\n{f.name}")
        print(f"  practice sections unwrapped for v9 : {st['unwrapped']}")
        print(f"  field 9 panels added               : {st['panels']}")
        if st["skipped_existing"]:
            print(f"  already had a panel                : {st['skipped_existing']}")
        if st["has_old_v9"]:
            print(f"  left for the chapter rewrite       : {st['has_old_v9']}"
                  f"  (an old ```sym 9 fence sits there)")
        if st["skipped_odd"]:
            print(f"  calculator calls not converted     : {len(st['skipped_odd'])}")
            for frag in st["skipped_odd"][:4]:
                print(f"      {frag}")
        if st["prose"]:
            print(f"  prose lines needing a human        : {len(st['prose'])}")
            if args.prose:
                for n, line in st["prose"]:
                    print(f"      {n:5}  {line}")
        tot["panels"] += st["panels"]; tot["unwrapped"] += st["unwrapped"]
        tot["existing"] += st["skipped_existing"]; tot["odd"] += len(st["skipped_odd"])
        tot["prose"] += len(st["prose"])
        if st["prose"]:
            worklist.append(f"\n## {f.name}  ({len(st['prose'])} lines)\n")
            for n, line in st["prose"]:
                worklist.append(f"{n:6}  {line}")
        if args.apply:
            f.write_text(new, encoding="utf-8", newline="\n")

    if args.worklist and worklist:
        header = ("# Practice-problem prose that still speaks to a calculator\n"
                  "#\n"
                  "# Each line below sits inside a practice section and says\n"
                  "# something a Symbulator 9 reader cannot do: press Enter,\n"
                  "# evaluate a variable, wait for Done. Fix these BEFORE\n"
                  "# running --unwrap on that chapter, or they go live.\n"
                  "#\n"
                  "# Line numbers are as of this run and shift as you edit.\n")
        Path(args.worklist).write_text(
            header + "\n".join(worklist) + "\n", encoding="utf-8", newline="\n")
        print(f"\nworklist written to {args.worklist}")

    print(f"\n{'APPLIED' if args.apply else 'DRY RUN'} — "
          f"{tot['panels']} panel(s), {tot['unwrapped']} section(s) unwrapped, "
          f"{tot['existing']} already done, {tot['odd']} call(s) left alone, "
          f"{tot['prose']} prose line(s) flagged")
    if not args.apply:
        print("Nothing was written. Re-run with --apply.")
    else:
        print("Now run:  py build.py --check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
