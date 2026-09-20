r"""Every Python cell in the Manual, run, and every output compared (#317).

    py tools\check_manual_python.py
    py tools\check_manual_python.py --prove-red

`check_manual_results.py` compares the Manual's circuits and their printed
answers; this does the same for the chapter about the package, whose examples
are Python in `sym 9` fences with their outputs in the `out` fences that follow.
A printed output that nothing ran is what let the toolbox chapter say `r.v2`
for months, which raises `AttributeError`: the first thing this found.

Each Manual chapter with `sym 9` fences is run **as a notebook is**: in one
IPython shell, cell by cell, in order, so a later cell may use what an earlier
one bound, cell magics included. After each `sym 9` cell the next `out` fence
must equal what the cell's last expression prints, as a notebook's plain-text
output would. A `text` fence is a listing, not a cell, and is not run -- the
`pip` line and the Colab install cell are those.

`--prove-red` damages the chapter three ways -- one printed output made wrong,
one cell made to ask for an answer that is not there, one output made
different -- and each must be reported. A check nobody has seen fail is not a
guard.

Exit status is 1 on any disagreement.
"""
from __future__ import annotations

import contextlib
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(HERE)
ROOT = os.path.dirname(DOCS)
SOLVER = os.path.join(ROOT, "Application", "v9", "repos", "solver")
SRC = os.path.join(DOCS, "src")

if not os.path.isdir(SOLVER):
    raise SystemExit(
        f"check_manual_python: {SOLVER} is missing. This runs the Manual's "
        "Python against the solver tree, which must sit beside Documentation "
        "-- see the top-level CLAUDE.md.")
sys.path.insert(0, SOLVER)          # first: the working tree's symbulator
os.environ.setdefault("MPLBACKEND", "Agg")

FENCE = re.compile(r"^```(sym 9|out|text)[ \t]*\n(.*?)^```[ \t]*$",
                   re.M | re.S)


def chapters() -> list:
    """The Manual chapters that hold Python cells."""
    out = []
    for path in sorted(glob.glob(os.path.join(SRC, "*-manual-*.md"))):
        with open(path, encoding="utf-8") as fh:
            if "```sym 9" in fh.read():
                out.append(path)
    return out


def check_text(text: str, name: str) -> tuple:
    """(problems, cells run, outputs compared) for one chapter's text."""
    from IPython.core.interactiveshell import InteractiveShell

    InteractiveShell.clear_instance()
    shell = InteractiveShell.instance()
    problems, cells, compared = [], 0, 0
    last, last_line, ran_ok = None, 0, False
    for m in FENCE.finditer(text):
        kind, body = m.group(1), m.group(2)
        line = text[:m.start()].count("\n") + 2
        if kind == "sym 9":
            cells += 1
            sink = io.StringIO()
            with contextlib.redirect_stdout(sink), \
                    contextlib.redirect_stderr(sink):
                result = shell.run_cell(body, store_history=False)
            err = result.error_before_exec or result.error_in_exec
            if err is not None:
                problems.append(f"{name}:{line}: the cell raises "
                                f"{type(err).__name__}: "
                                f"{str(err).splitlines()[0][:100]}")
                ran_ok, last = False, None
            else:
                ran_ok, last, last_line = True, result.result, line
        elif kind == "out":
            compared += 1
            if not ran_ok:
                problems.append(f"{name}:{line}: an output with no cell "
                                "before it that ran")
                continue
            want, got = body.strip(), repr(last)
            if got != want:
                problems.append(f"{name}:{line}: the cell at line {last_line} "
                                f"prints {got!r}, the chapter says {want!r}")
    return problems, cells, compared


def run_checks(prove: bool = False) -> tuple:
    """(problems, cells, outputs, caught). Nothing is printed, so
    `build.py --check` can run it in its own voice."""
    problems, cells, compared, caught = [], 0, 0, 0
    for path in chapters():
        name = os.path.basename(path)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        if not prove:
            p, c, o = check_text(text, name)
            problems += p
            cells += c
            compared += o
            continue
        # damage the chapter three ways; each must come back as a problem
        damages = []
        m = re.search(r"```out\n(.*?)\n```", text, re.S)
        damages.append(("an output made wrong",
                        text[:m.start(1)] + m.group(1) + " + 1" + text[m.end(1):]))
        damages.append(("a cell asking for an answer that is not there",
                        text.replace('res["v2"]', 'res["v99"]', 1)))
        n = list(re.finditer(r"```out\n(.*?)\n```", text, re.S))[1]
        damages.append(("a second output different",
                        text[:n.start(1)] + "(0, 0, 0)" + text[n.end(1):]))
        for label, damaged in damages:
            found, _c, _o = check_text(damaged, name)
            if found:
                caught += 1
            else:
                problems.append(f"{name}: damage not caught -- {label}")
        cells += 1
    return problems, cells, compared, caught


def main() -> int:
    prove = "--prove-red" in sys.argv
    problems, cells, compared, caught = run_checks(prove=prove)
    if prove:
        print(f"prove-red: {caught} of 3 damages caught",
              "-- RED, as it should be" if caught == 3 and not problems
              else "-- THIS CHECK CANNOT FAIL")
        for p in problems:
            print("  **", p)
        return 0 if caught == 3 and not problems else 1
    print(f"{len(chapters())} chapter(s), {cells} cells run, "
          f"{compared} outputs compared")
    for p in problems:
        print("  **", p)
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
