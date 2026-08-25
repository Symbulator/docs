"""No raw control characters in the documentation source.

A shell heredoc expands backslash escapes, so text written through one can
arrive with a literal BEL where `s\\ac` was meant, or a form feed where
`\\frac` was. The result is invisible in most editors, survives every other
check, and renders as a missing command: `s\\aa(irab)` became `sa(irab)` on
the live site and stayed that way.

It was found twice on 25 Aug 2026 -- once fresh in chapter 7, once already
published in chapter 9's delta-delta section and chapter 7's LaTeX. Nothing
in this documentation has any business containing a control character, so
the rule is simply that there are none.
"""
import glob
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: Tab and newline are legitimate; nothing else below 0x20 is.
ALLOWED = {"\n", "\t"}

#: The likely intended spelling, for a message that says what to do.
LIKELY = {7: r"\a  (as in s\ac or s\aa)", 8: r"\b", 12: r"\f  (as in \frac)",
          11: r"\v", 13: r"\r  (a stray carriage return)"}


def check_control_chars() -> list[str]:
    problems = []
    for path in sorted(glob.glob(os.path.join(ROOT, "src", "*.md"))):
        text = io.open(path, encoding="utf-8", newline="").read()
        name = os.path.basename(path)
        for i, ch in enumerate(text):
            if ord(ch) < 32 and ch not in ALLOWED:
                line = text[:i].count("\n") + 1
                guess = LIKELY.get(ord(ch), "a backslash escape")
                problems.append(
                    f"{name}:{line}: control character chr({ord(ch)}) -- "
                    f"almost certainly {guess} eaten by a shell heredoc")
    return problems


if __name__ == "__main__":
    import sys

    found = check_control_chars()
    for p in found:
        print("  " + p)
    if found:
        sys.exit(1)
    print("no control characters in src/")
