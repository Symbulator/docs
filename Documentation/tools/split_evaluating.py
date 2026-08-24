"""Version 9 does not evaluate an answer to read it -- it is on the page.

"Evaluating `pr2` gets the power consumed..." describes the calculator,
where you ask for a variable and it prints. In the web interface the value
is already shown, so the sentence becomes "`pr2` is the power consumed...".

Versions 7 and 8 keep the original wording, so each sentence is split
rather than rewritten. Lines that already carry a brace command are left
for a human: a version span closes at the first `}}` it meets, so wrapping
one around another silently truncates it.

Usage:
    python tools/split_evaluating.py            # report
    python tools/split_evaluating.py --write    # apply
"""
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "src")

# "Evaluating `x` gets", "Evaluating `x` we find", "Evaluating `x` gives us".
# Longest alternatives first: with "gives" ahead of "gives us", the "us" is
# left stranded and the sentence comes out as "`vo` is us the output".
LEAD = re.compile(r"\bEvaluating\s+(`[^`]+`)\s+"
                  r"(gets us|gives us|we find|we get|gets|gives)\b")


def split_phrase(text: str) -> str:
    """Split only the phrase, never the whole line.

    Most of these sentences carry a `{{o:...}}` value further along, and a
    version span closes at the first `}}` it meets -- so wrapping the line
    would swallow half of it. Wrapping just the words that differ leaves
    the value, the units and any subscript exactly where they were.
    """
    def one(m):
        name, verb = m.group(1), m.group(2)
        old = f"Evaluating {name} {verb}"
        new = f"{name} is"
        return f"{{{{v7,8|{old}}}}}{{{{v9|{new}}}}}"

    # Deliberately only the leading phrase. A sentence listing several
    # answers -- "`ir1` gets 17.5 mA, `ir2` gets 1.4 mA" -- needs the
    # same treatment on each, and doing that by pattern kept either
    # missing the later ones or wrapping the first a second time. Those
    # are reported and left; there are three and a person can read them.
    return LEAD.sub(one, text)


def main():
    write = "--write" in sys.argv
    done = skipped = 0
    for path in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        name = os.path.basename(path)
        lines = io.open(path, encoding="utf-8").read().split("\n")
        changed = False
        for i, line in enumerate(lines):
            if not LEAD.search(line):
                continue
            # A calculator array call is not something version 9 has
            # an equivalent for, so it needs rewriting rather than
            # splitting -- and its braces would break the span.
            # A calculator array call has no version 9 equivalent, so it
            # needs rewriting rather than splitting.
            if "approx(" in line:
                skipped += 1
                print(f"  {name}:{i + 1}  calculator array, left alone")
                print(f"      {line.strip()[:104]}")
                continue
            if "{{v7" in line or "{{v9" in line or "{{!v" in line:
                skipped += 1
                print(f"  {name}:{i + 1}  already version-split, left alone")
                print(f"      {line.strip()[:104]}")
                continue
            nine = split_phrase(line)
            if nine == line:
                continue
            lines[i] = nine
            done += 1
            changed = True
            print(f"  {name}:{i + 1}")
            print(f"      {nine.strip()[:150]}")
        if changed and write:
            io.open(path, "w", encoding="utf-8",
                    newline="\n").write("\n".join(lines))
    print(f"\n{done} split, {skipped} need a human")
    if done and not write:
        print("dry run -- pass --write to apply")


main()
