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

#230 (3 Sep 2026) widened it from the prose to **the code that builds the
prose**, because that is where the next one was hiding. build.py's plain()
carried a regex reading <(script|style)BS...</SOH> -- literal bytes 8 and 1
where a word boundary and a backreference had been written -- so its
script/style stripping could never match anything and never had. It was
harmless only because no chapter contains a script tag. The checker that
would have caught it was looking at src/ alone: it had the same blind spot
as the bug, which is the reason to scan the tools too.
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
    # The prose, and the code that renders it. A build script is exactly
    # as vulnerable to a heredoc eating an escape as a chapter is, and
    # rather more quietly: a mangled regex still compiles and simply
    # stops matching (#230).
    # The notes files too (#380). Two `\a` escapes had been sitting
    # in NEXT_DOCS.md as BEL since they were written, because the
    # scan stopped at `src/`: the blind spot this checker exists to
    # warn about, in its own tree.
    targets = (sorted(glob.glob(os.path.join(ROOT, "src", "*.md")))
               + [os.path.join(ROOT, "build.py")]
               + sorted(glob.glob(os.path.join(ROOT, "*.md")))
               + sorted(glob.glob(os.path.join(ROOT, "tools", "*.py"))))
    for path in targets:
        if not os.path.isfile(path):
            continue
        text = io.open(path, encoding="utf-8", newline="").read()
        # CRLF is a line ending, not a control character in the content:
        # these files are edited on Windows and many are stored with it.
        # Collapsing the pair first keeps a *lone* CR a finding, which is
        # what chr(13) meant when only the prose was scanned.
        text = text.replace("\r\n", "\n")
        name = os.path.relpath(path, ROOT).replace(os.sep, "/")
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
