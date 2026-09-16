#!/usr/bin/env python
"""The Symbulator timeline, written once and rendered into both books.

The dates live in `paper/timeline.tsv` and nowhere else. This script
writes them into the two places that print them, each between its own
markers:

  * `src/99-credits.md`, as a pipe table inside *Who made Symbulator*;
  * `paper/symbulator_monograph.tex`, as a booktabs table closing
    chapter 1, *A history of Symbulator*.

    py Documentation\\tools\\gen_timeline.py            # write both
    py Documentation\\tools\\gen_timeline.py --check    # verify both

`--check` is what `build.py --check` runs. It exists because a table of
twenty dates restated in a second file goes stale -- this project has
recorded that failure three times -- so editing the `.tsv` without
regenerating fails the build instead of shipping two books that
disagree.

Roberto is the source (16 Sep 2026): the table carries no provenance
column and links no documents.
"""
import argparse
import io
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent
TSV = DOCS / "paper" / "timeline.tsv"
CREDITS = DOCS / "src" / "99-credits.md"
MONOGRAPH = DOCS / "paper" / "symbulator_monograph.tex"

MD_HEADING = "### A timeline"
TEX_BEGIN, TEX_END = "% TIMELINE:BEGIN", "% TIMELINE:END"

# The docs markup has no comment syntax -- every line of a chapter is
# content -- so a `<!-- TIMELINE:BEGIN -->` marker renders on the page as
# visible text (it did, for one build). The markdown region is therefore
# delimited by its own heading and the next one, which are real content.
# LaTeX does have comments, so the monograph keeps its markers.
MD_REGION = re.compile(
    r"(?m)^" + re.escape(MD_HEADING) + r"\s*?\n(.*?)(?=^#{2,3} )", re.S)


def rows():
    out = []
    for n, line in enumerate(io.open(TSV, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            sys.exit(f"{TSV}:{n}: expected two tab-separated fields, got {len(parts)}")
        out.append((parts[0].strip(), parts[1].strip()))
    if not out:
        sys.exit(f"{TSV}: no rows")
    return out


def markdown(rs):
    lines = ["| Date | Event |", "|---|---|"]
    lines += [f"| **{d}** | {e} |" for d, e in rs]
    return "\n".join(lines)


def tex_escape(s):
    s = s.replace("\\", "\\textbackslash{}")
    for ch in "&%$#_{}":
        s = s.replace(ch, "\\" + ch)
    return s


def latex(rs):
    lines = [
        r"\begin{table}[htbp]",
        r"\caption{The dates.}",
        r"\label{tab:timeline}",
        r"\centering",
        r"\begin{tabular}{@{}l>{\raggedright\arraybackslash}p{9.2cm}@{}}",
        r"\toprule",
        r"Date & Event \\",
        r"\midrule",
    ]
    lines += [f"{tex_escape(d)} & {tex_escape(e)} \\\\" for d, e in rs]
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    return "\n".join(lines)


def region(path, text):
    """The span of `text` the table owns, as a match, plus what it should hold."""
    if path is CREDITS:
        return MD_REGION.search(text), "md"
    pat = re.compile(re.escape(TEX_BEGIN) + r"(.*?)" + re.escape(TEX_END), re.S)
    return pat.search(text), "tex"


def splice(path, body, check):
    text = io.open(path, encoding="utf-8").read()
    m, kind = region(path, text)
    if not m:
        where = (f"no `{MD_HEADING}` heading followed by another heading"
                 if kind == "md" else f"no {TEX_BEGIN} / {TEX_END} markers")
        sys.exit(f"{path}: {where}")
    want = "\n" + body + "\n\n"
    if m.group(1) == want:
        print(f"  ok   {path.name}")
        return False
    if check:
        print(f"  BAD  {path.name}: the table does not match {TSV.name}")
        return True
    io.open(path, "w", encoding="utf-8", newline="\n").write(
        text[: m.start(1)] + want + text[m.end(1):])
    print(f"  wrote {path.name}")
    return False


def check_timeline():
    """Return a list of problems, for `build.py --check`.

    Reports when either book's table has drifted from `timeline.tsv` --
    an edit to the dates that was never regenerated.
    """
    problems = []
    try:
        rs = rows()
    except SystemExit as e:
        return [f"timeline: {e}"]
    for path, body in ((CREDITS, markdown(rs)), (MONOGRAPH, latex(rs))):
        text = io.open(path, encoding="utf-8").read()
        m, kind = region(path, text)
        if not m:
            problems.append(f"{path.name}: the timeline's place is missing "
                            + (f"(`{MD_HEADING}`)" if kind == "md"
                               else f"({TEX_BEGIN} / {TEX_END})"))
        elif m.group(1) != "\n" + body + "\n\n":
            problems.append(
                f"{path.name}: the timeline table does not match {TSV.name} -- "
                f"run `py Documentation\\tools\\gen_timeline.py`")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify both books match the .tsv; do not write")
    args = ap.parse_args()
    rs = rows()
    print(f"timeline: {len(rs)} rows from {TSV.name}")
    bad = splice(CREDITS, markdown(rs), args.check)
    bad |= splice(MONOGRAPH, latex(rs), args.check)
    if bad:
        print("\nRun `py Documentation\\tools\\gen_timeline.py` to regenerate.")
        sys.exit(1)


if __name__ == "__main__":
    main()
