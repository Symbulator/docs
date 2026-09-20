"""A Baker's Dozen as an executed Jupyter notebook (#466).

    py paper\\bakers_dozen\\build_dozen_ipynb.py

Writes Application/v9/repos/solver/notebooks/books/Bakers_Dozen.ipynb: the
same thirteen problems as the PDF, each with its question, picture and
*why it is here*, then every run as the package call a person would type,
executed, with the answers the booklet prints beside what the notebook
computes.

Like `build_dozen_tex.py` it reads `P` and `BONUS` from `build_dozen.py`,
so the PDF, the LaTeX and the notebook cannot disagree about which
problems there are, what is asked, or what the booklet prints. The
circuits are not typed here either: each run names its book and position,
and the entry is read from the app's own `.cir` file by
`notebooks/build_books.py`, whose cell builders this reuses -- which is why
a notebook cell here is the same call the other twenty-two notebooks make
for the same entry.

Read README.md beside this file before changing the selection, and run
check_dozen.py first: this refuses to build if an entry has moved (the
same EXPECT table) and stops on any cell that raises.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(os.path.dirname(HERE))
ROOT = os.path.dirname(DOCS)
NOTEBOOKS = os.path.join(ROOT, "Application", "v9", "repos", "solver",
                         "notebooks")
APP = "https://symbulator.pythonanywhere.com/"
ASSETS = "https://learn.symbulator.com/assets/"

if not os.path.isfile(os.path.join(NOTEBOOKS, "build_books.py")):
    raise SystemExit(
        f"build_dozen_ipynb: {NOTEBOOKS}\\build_books.py is missing. The\n"
        "notebook is built with the solver repository's generator, so\n"
        "Application/v9/repos/solver must sit beside Documentation's\n"
        "sibling folder, Application -- see the top-level CLAUDE.md.")

sys.path.insert(0, HERE)
sys.path.insert(0, NOTEBOOKS)
import build_dozen as bd                                    # noqa: E402
import check_dozen as cd                                    # noqa: E402
import build_books as bb                                    # noqa: E402
import circuitbook                                          # noqa: E402  (bb put the app tree on the path)

md, code = bb.md, bb.code


def entry_for(book: str, n: int) -> dict:
    """Entry `n` of `book`, refusing one that is not the entry the booklet
    was written about (check_dozen's EXPECT pins each position to a title)."""
    path = os.path.join(bb.EXAMPLES, book + ".cir")
    entries = bb.parse_book(io.open(path, encoding="utf-8").read())[0]
    e = entries[n - 1]
    want = cd.EXPECT[(book, n)].strip()[:circuitbook.MAX_NAME_LEN]
    if e["name"] != want:
        raise SystemExit(f"ENTRY MOVED: {book} #{n} is now {e['name']!r}, "
                         f"the booklet was written about {want!r}. "
                         "Fix its position in build_dozen.py and "
                         "check_dozen.py, then run check_dozen.py.")
    return e


def picture(p: dict, e: dict) -> str:
    """The problem's picture as a URL learn serves. The booklet's own
    figure for the ladder is a local SVG with no web copy, so that one
    problem shows the entry's picture, which is the chapter's."""
    if p["img"].startswith("SVG:"):
        return (e.get("image") or "").split(" [")[0].strip()
    return ASSETS + p["img"]


def polar_cell(e: dict, book: str, n: int, r: str, cards: list) -> str:
    """The answers the booklet prints as phasors, as the app's *polar*
    setting shows them. The entry says polar; the names are the ones
    check_dozen watches, and an Evaluate expression is read the same way."""
    items = [f"{name!r}: polar({r}[{name!r}])"
             for name in cd.WATCH[(book, n)]]
    for src in cards:
        if src.startswith("evaluate("):
            items.append(f"{e['evaluate']!r}: polar({src})")
    return "{" + ", ".join(items) + "}"


def problem_cells(p: dict, label: str, first_run: int) -> tuple:
    """(cells, number of runs used) for one problem."""
    runs = p["runs"]
    e0 = entry_for(runs[0][1], runs[0][2])
    head = [f"## {label}: {p['title']}", f"**{p['tag']}**",
            f"*{p['where']}*", p["question"]]
    pic = picture(p, e0)
    if pic:
        head.append(f"![The circuit of {p['title']}]({pic})")
    head.append(f"**Why it is here.** {p['why']}")
    cells = [md("\n\n".join(head))]
    for k, (lab, book, n, key, settings, printed) in enumerate(runs):
        e = entry_for(book, n)
        c, r = f"c{first_run + k}", f"r{first_run + k}"
        link = f"{APP}?lesson={key}&entry={n}"
        sub = [f"### {lab}" if len(runs) > 1 else "", f"*{settings}*",
               f"[Open this run in the app]({link})"]
        cells.append(md("\n\n".join(s for s in sub if s)))
        cells.append(code(f"{c} = '''\n{e['desc'].strip()}\n'''"
                          + (f"\ndraw({c})" if bb.drawable(e["desc"]) else "")))
        run_src = bb.run_cell(e, c, r)
        # The booklet states the frequency on the settings line (the entry
        # may leave omega a symbol), so the cell runs at the stated one.
        om = cd.stated_omega(settings)
        if om and e.get("domain") == "ac":
            arg = f"omega={om!r}" if "pi" in om else f"omega={om}"
            run_src = re.sub(r"omega=[^,)\n]+", arg, run_src)
        cells.append(code(run_src))
        plot = bb.plot_cell(e, c)
        if plot:
            cells.append(code(plot))
        card_srcs = bb.card_cells(e, r)
        # Two of the booklet's runs print a ratio (`Evaluate: v_3/vg`) that
        # the settings line asks for and the entry does not carry, since the
        # entry's own Evaluate box is empty. The notebook asks for it too.
        m = re.search(r"Evaluate: (.+?)\.(?:\s|$)", settings)
        if m and not e.get("evaluate"):
            card_srcs.append(f"evaluate({r}, {m.group(1)!r})")
        cells += [code(src) for src in card_srcs]
        if e.get("polar") and cd.WATCH[(book, n)]:
            cells.append(code(polar_cell(e, book, n, r, card_srcs)))
        shown = "\n\n".join(f"$${x}$$" for x in printed)
        cells.append(md(f"**The booklet prints**\n\n{shown}"))
    return cells, len(runs)


def build() -> str:
    problems = bd.P + [bd.BONUS]
    toc = "\n".join(f"{i}. **{p['title']}** — {p['tag']}"
                    for i, p in enumerate(bd.P, 1))
    toc += f"\n\n★ **{bd.BONUS['title']}** — {bd.BONUS['tag']}"
    cells = [md(
        "# A Baker's Dozen\n\n"
        "Twelve solved examples from the Symbulator 9 documentation, and a "
        "bonus. Each of these circuits looks like an afternoon's work by "
        "hand. Symbulator solves each one in a single run, or in two when a "
        "switch splits the problem into intervals, and no two of them make "
        "the same point.\n\n"
        "This is the notebook of the booklet at "
        "https://learn.symbulator.com/dozen.pdf. Every description below is "
        "the one in the app's built-in examples, read from the app's own "
        "file and not retyped, and each run is the `symbulator` call that "
        "solves it. Under each run the answers the booklet prints are "
        "shown, to read beside what the cell computes. Where the booklet "
        "shows a rounded decimal the cell shows the exact value, and "
        "`rounded()` or `polar()` gives the same digits.\n\n"
        f"{toc}\n\nIf you are on Colab, run the first cell.")]
    cells += bb.setup_cells()
    used = 1
    for i, p in enumerate(bd.P, 1):
        more, k = problem_cells(p, f"Sample {i} of 12", used)
        cells += more
        used += k
    more, k = problem_cells(bd.BONUS, "Bonus", used)
    cells += more
    cells.append(md(
        "## Where next\n\n"
        "* The booklet: https://learn.symbulator.com/dozen.pdf\n"
        f"* Every run above opens in the app: {APP}\n"
        "* The rest of the built-in examples as notebooks, one per book, "
        "are beside this file."))
    out = bb.execute_and_write(cells, "Bakers_Dozen")
    n_code = sum(1 for c in cells if c.cell_type == "code")
    return (f"wrote {out}: {len(problems)} problems, {len(cells)} cells, "
            f"{n_code} code cells, all executed")


if __name__ == "__main__":
    print(build())
