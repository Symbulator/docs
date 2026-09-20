r"""The Manual's worked circuits as an executed Jupyter notebook (#466).

    py tools\build_manual_notebook.py

Writes Application/v9/repos/solver/notebooks/books/Manual.ipynb. The Manual
is prose with circuits embedded, not a book of `.cir` entries, so what this
reads is `manual_runs.RUNS` (how each circuit is run, the one thing the
chapters leave unsaid) and the chapters themselves:

  * every circuit is read from its fence, never retyped;
  * the words around it -- the paragraph before the circuit and the one
    before the answer -- are the Manual's own, with its brace commands
    turned into plain markdown;
  * the answers the Manual prints are shown under each run, as the panels
    have them, to read beside what the cell computes.

Each run is the call `manual_runs.call_source` gives, and that is also what
`check_manual_results.py` executes when it compares every printed answer
with the solver and the app -- so what this notebook shows is what was
checked. Run that first: this refuses to build if the table and the
chapters disagree, and stops on any cell that raises.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(HERE)
ROOT = os.path.dirname(DOCS)
NOTEBOOKS = os.path.join(ROOT, "Application", "v9", "repos", "solver",
                         "notebooks")
LEARN = "https://learn.symbulator.com/"

if not os.path.isfile(os.path.join(NOTEBOOKS, "build_books.py")):
    raise SystemExit(
        f"build_manual_notebook: {NOTEBOOKS}\\build_books.py is missing. The\n"
        "notebook is built with the solver repository's generator, so\n"
        "Application/v9/repos/solver must sit beside Documentation's\n"
        "sibling folder, Application -- see the top-level CLAUDE.md.")

sys.path.insert(0, HERE)
sys.path.insert(0, NOTEBOOKS)
import manual_runs as mr                                    # noqa: E402
import build_books as bb                                    # noqa: E402

md, code = bb.md, bb.code


def build() -> str:
    runs = mr.resolve()
    ids = {r["chapter"]: mr.front_matter(r["text"])["id"] for r in runs}
    circuits = len({(r["chapter"], r["fence"]) for r in runs})
    cells = [md(
        "# The Symbulator Manual, run\n\n"
        "The Manual at https://learn.symbulator.com/9/ explains how "
        "Symbulator works, one chapter at a time, with small invented "
        f"circuits to make each point. This notebook runs all {circuits} of "
        "them with the `symbulator` package.\n\n"
        "Every circuit is read from the Manual's own chapters and not "
        "retyped, and the words around each are the Manual's. Under each "
        "run the answers the Manual prints are shown, to read beside what "
        "the cell computes; the Manual's build compares every one of them "
        "with the solver and with the app.\n\n"
        "The Manual's chapters take a run as a sequence of choices in the "
        "app -- an analysis, a frequency, two nodes. Here each is the "
        "call that makes it, with the same answers.\n\n"
        f"The Manual as a PDF: {LEARN}symbulator-manual.pdf\n\n"
        "If you are on Colab, run the first cell.")]
    cells += bb.setup_cells()

    last_chapter, seen, shown_circuit, n_circuit = None, set(), {}, 0
    c_no = r_no = 0
    for run in runs:
        stem, fence = run["chapter"], run["fence"]
        if stem != last_chapter:
            cells.append(md(f"## {run['title']}\n\n"
                            f"[Read the chapter]({LEARN}9/{ids[stem]})"))
            last_chapter = stem
        key = (stem, fence)
        first_of_fence = key not in seen
        if first_of_fence:
            seen.add(key)
            n_circuit += 1
            head = run["heading"] or run["title"]
            text = f"### {n_circuit}. {head}"
            if run["intro"]:
                text += f"\n\n{run['intro']}"
            cells.append(md(text))
        if first_of_fence or shown_circuit.get(key) != run["circuit"]:
            c_no += 1
            shown_circuit[key] = run["circuit"]
            cells.append(code(
                f"c{c_no} = '''\n{run['circuit']}\n'''"
                + (f"\ndraw(c{c_no})" if bb.drawable(run["circuit"]) else "")))
        r_no += 1
        r = f"r{r_no}"
        note = [run["lead"]] if run["lead"] else []
        if run.get("aside"):
            note.append(f"*{run['aside']}*")
        if run["define"]:
            note.append("The Define card, one per line:\n\n```\n"
                        + "\n".join(run["define"]) + "\n```\n\nIn the "
                        "package a Define is a condition -- the calculator's "
                        "`|` -- applied to the whole system.")
        if note:
            cells.append(md("\n\n".join(note)))
        cells.append(code(mr.call_source(run, f"c{c_no}", r) + f"\n{r}"))
        printed = []
        for label, tex in run["panels"]:
            name = mr.tex_name(tex.partition("=")[0])
            cells.append(code(
                mr.answer_source(run, r, name, run["circuit"])))
            printed.append(f"**{label}**\n\n$${tex}$$")
        if printed:
            cells.append(md("**The Manual prints**\n\n" + "\n\n".join(printed)))
    cells.append(md(
        "## Where next\n\n"
        f"* The Manual: {LEARN}9/\n"
        f"* The Manual as a PDF: {LEARN}symbulator-manual.pdf\n"
        "* The Course's problems, one notebook per book, and *A Baker's "
        "Dozen*, are beside this file."))
    out = bb.execute_and_write(cells, "Manual")
    n_code = sum(1 for c in cells if c.cell_type == "code")
    return (f"wrote {out}: {circuits} circuits, {len(runs)} runs, "
            f"{len(cells)} cells, {n_code} code cells, all executed")


if __name__ == "__main__":
    print(build())
