r"""How each circuit in the Manual is run, written down as data (#466).

The Course's problems are records: a `.cir` entry says which analysis, which
rounding, which cards, so an app link, a check and a notebook can all read
it. The Manual is prose with circuits embedded, and its `field 9 Circuit
Description` fences say none of that -- the analysis is a sentence beside
the circuit, and the answer is a hand-typed `::: result` panel that nothing
compared with the solver until `check_manual_results.py` did.

This file is the missing record. It holds **only what the chapters leave
unsaid**: the analysis, omega, the nodes a tool is given, which panels
belong to which run. Everything else is read from the chapters themselves
so it cannot drift from them:

  * the circuits, from the fences;
  * the Define block of the symbols chapter, from its `field 9 Define` fence;
  * the printed answers, from the `::: result` panels;
  * the words around them, from the paragraphs before a fence and before a
    run's first panel.

Three guards keep the table honest, all in `check_manual_results.py`:
each run names its fence by the fence's first line, so a fence that has
moved or been rewritten fails; a panel that no run claims fails, so a new
result panel cannot be added to a chapter without a line here; and a run
that claims more panels than its chapter has fails.

`RUNS` is in the order the Manual is read. A fence with two runs (the
symbols chapter's Define, the coupling chapter's reversed coil) has two
entries with the same `fence`.
"""
from __future__ import annotations

import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(HERE)
SRC = os.path.join(DOCS, "src")

FENCE = re.compile(
    r"^```field\s+9\s+Circuit Description\s*$\n(.*?)^```\s*$", re.M | re.S)
DEFINE_FENCE = re.compile(
    r"^```field\s+9\s+Define\s*$\n(.*?)^```\s*$", re.M | re.S)
PANEL = re.compile(r"^::: result ([^\n]*)\n(.*?)\n:::[ \t]*$", re.M | re.S)

# One entry per run.
#   chapter  the file's stem in Documentation/src
#   fence    which circuit fence of that chapter, counting from 1
#   first    the fence's first line, so a moved or rewritten fence fails
#   how      the call: dc, ac, fd, tr, or one of the Find equivalent tools
#            th (Thevenin / Norton), er (resistance / impedance), port
#   panels   how many of the chapter's result panels this run prints, taken
#            in order from where the previous run left off
#   omega    for ac
#   nodes    for th, er and port
#   kind     for port: the parameter family
#   define   True: the chapter's Define fence applies as conditions
#   replace  {old line: new line}: the same circuit written another way
#   aside    a sentence for the notebook alone, where a run needs one the
#            chapter does not give (a fragment that has no source)
RUNS = [
    dict(chapter="21-manual-grammar", fence=1, first="e1,1,0,12",
         how="dc", panels=0),
    dict(chapter="21-manual-grammar", fence=2, first="e1,1,0,vs",
         how="dc", panels=0),
    dict(chapter="21-manual-grammar", fence=3, first="rp,1,0,[1'k,2'k,2'k]",
         how="dc", panels=0,
         aside="This fence shows the bracket notation on its own, so with no "
               "source in the circuit every answer is zero. The Manual's "
               "parallel-shorthand example, further on, puts the same "
               "element across a 9 V source."),
    dict(chapter="21-manual-grammar", fence=4, first="e,1,0,10",
         how="dc", panels=0),
    dict(chapter="22-manual-answers", fence=1, first="e1,1,0,12",
         how="dc", panels=3),
    dict(chapter="23-manual-symbols", fence=1, first="e,1,0,vs",
         how="dc", panels=1),
    dict(chapter="23-manual-symbols", fence=1, first="e,1,0,vs",
         how="dc", panels=1, define=True),
    dict(chapter="24-manual-dc", fence=1, first="j,0,1,3'm",
         how="dc", panels=1),
    dict(chapter="24-manual-dc", fence=2, first="e,1,0,9",
         how="dc", panels=1),
    dict(chapter="25-manual-equivalents", fence=1, first="r1,1,2,100",
         how="er", nodes=("1", "0"), panels=1),
    dict(chapter="25-manual-equivalents", fence=2, first="e,1,0,20",
         how="th", nodes=("2", "0"), panels=4),
    dict(chapter="26-manual-opamps", fence=1, first="e,1,0,2",
         how="dc", panels=1),
    dict(chapter="26-manual-opamps", fence=2, first="e,1,0,2",
         how="dc", panels=1),
    dict(chapter="27-manual-transients", fence=1, first="e,1,0,10",
         how="tr", panels=1),
    dict(chapter="27-manual-transients", fence=2, first="e,1,0,10",
         how="tr", panels=1),
    dict(chapter="27-manual-transients", fence=3, first="r,1,0,1'k",
         how="tr", panels=1),
    dict(chapter="28-manual-ac", fence=1, first="e,1,0,10",
         how="ac", omega=1000, panels=2),
    dict(chapter="28-manual-ac", fence=2, first="e,1,0,10",
         how="ac", omega=1000, panels=1),
    dict(chapter="29-manual-coupling", fence=1, first="e,1,0,10",
         how="ac", omega=1000, panels=1),
    dict(chapter="29-manual-coupling", fence=1, first="e,1,0,10",
         how="ac", omega=1000, panels=1,
         replace={"l2,2,0,0.03": "l2,0,2,0.03"}),
    dict(chapter="29-manual-coupling", fence=2, first="e,1,0,120",
         how="dc", panels=2),
    dict(chapter="30-manual-frequency", fence=1, first="e,1,0,vs",
         how="fd", panels=1),
    dict(chapter="31-manual-twoports", fence=1, first="ra,1,2,10",
         how="port", nodes=("1", "3"), kind="z", panels=4),
    dict(chapter="31-manual-twoports", fence=2, first="e,1,0,10",
         how="dc", panels=0),
]

_FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def chapter_path(stem: str) -> str:
    return os.path.join(SRC, stem + ".md")


def read_chapter(stem: str) -> str:
    with open(chapter_path(stem), encoding="utf-8") as fh:
        return fh.read()


def front_matter(text: str) -> dict:
    """`id` and `title` from a chapter's front matter -- all this needs."""
    m = _FRONT.match(text)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        k, _, v = line.partition(":")
        if k.strip() in ("id", "title"):
            out[k.strip()] = v.strip()
    return out


def chapter_titles() -> dict:
    """{chapter id: title} for every Manual chapter, for `{{ref:...}}`."""
    out = {}
    for path in glob.glob(os.path.join(SRC, "*-manual-*.md")):
        with open(path, encoding="utf-8") as fh:
            fm = front_matter(fh.read())
        if "id" in fm:
            out[fm["id"]] = fm.get("title", fm["id"])
    return out


def fences(text: str) -> list:
    return list(FENCE.finditer(text))


def panels_after(text: str, fence_match, all_fences: list) -> list:
    """The result panels between a fence and the next one:
    [(label, latex, start, end)]."""
    i = all_fences.index(fence_match)
    stop = all_fences[i + 1].start() if i + 1 < len(all_fences) else len(text)
    return [(m.group(1).strip(), m.group(2).strip(), m.start(), m.end())
            for m in PANEL.finditer(text, fence_match.end(), stop)]


def heading_before(text: str, pos: int) -> str:
    """The nearest `## ` heading above `pos`, or ''."""
    found = ""
    for m in re.finditer(r"^#{2,3} (.+)$", text[:pos], re.M):
        found = m.group(1).strip()
    return found


def paragraph_before(text: str, pos: int) -> str:
    """The paragraph that ends at `pos`, or '' if it is a fence, a panel
    or a list -- prose only."""
    chunk = text[:pos].rstrip()
    para = chunk.rsplit("\n\n", 1)[-1].strip()
    if not para or para.startswith(("```", ":::", "|", "#", "1.", "-")):
        return ""
    if para.endswith((":::", "```")):
        return ""
    return para


_INDEX = re.compile(r"\{\{i:[^}]*\}\}")
_REF = re.compile(r"\{\{ref:([^}]*)\}\}")
_WRAP = re.compile(r"\{\{(ui|card|btn|tool|o|var|k|key):((?:[^{}]|\n)*?)\}\}")


def clean(text: str, titles: dict) -> str:
    """The Manual's brace commands turned into plain markdown for a
    notebook: index marks dropped, a cross-reference named by its chapter's
    title, a control or card set in bold, an answer or a variable as code."""
    text = _INDEX.sub("", text)
    text = _REF.sub(lambda m: f"*{titles.get(m.group(1), m.group(1))}*", text)

    def wrap(m):
        kind, body = m.group(1), " ".join(m.group(2).split())
        return f"`{body}`" if kind in ("o", "var", "k", "key") else f"**{body}**"

    return _WRAP.sub(wrap, text).strip()


def resolve():
    """Every run with what it reads from its chapter, in order:

        dict(run, text, fence_match, circuit, panels=[(label, latex)],
             heading, intro, lead, title, define)

    Raises SystemExit naming the run when the table and the chapters
    disagree: a fence whose first line is not `first`, a run that claims
    more panels than are left, a panel no run claims, a Define fence that
    is missing."""
    titles = chapter_titles()
    cache, used, out = {}, {}, []
    for run in RUNS:
        stem = run["chapter"]
        if stem not in cache:
            text = read_chapter(stem)
            cache[stem] = (text, fences(text))
        text, allf = cache[stem]
        where = f"{stem} fence {run['fence']}"
        if run["fence"] > len(allf):
            raise SystemExit(f"manual_runs: {where} does not exist "
                             f"({len(allf)} fences there)")
        fm = allf[run["fence"] - 1]
        circuit = fm.group(1).strip()
        if circuit.splitlines()[0].strip() != run["first"]:
            raise SystemExit(
                f"manual_runs: {where} now starts "
                f"{circuit.splitlines()[0]!r}, the table says "
                f"{run['first']!r} -- the chapter moved or the fence was "
                "rewritten; fix RUNS.")
        if run.get("replace"):
            for old, new in run["replace"].items():
                if old not in circuit:
                    raise SystemExit(f"manual_runs: {where}: the line {old!r} "
                                     "to replace is not in the circuit")
                circuit = circuit.replace(old, new)
        pan = panels_after(text, fm, allf)
        key = (stem, run["fence"])
        took = used.get(key, 0)
        mine = pan[took:took + run["panels"]]
        if len(mine) != run["panels"]:
            raise SystemExit(f"manual_runs: {where}: the run claims "
                             f"{run['panels']} panel(s) after {took} already "
                             f"taken, and the chapter has {len(pan)}")
        used[key] = took + run["panels"]
        define = None
        if run.get("define"):
            dm = DEFINE_FENCE.search(text)
            if not dm:
                raise SystemExit(f"manual_runs: {where}: no `field 9 Define` "
                                 "fence in the chapter")
            define = [ln.strip() for ln in dm.group(1).strip().splitlines()
                      if ln.strip()]
        lead_pos = mine[0][2] if mine else None
        out.append(dict(
            run, text=text, circuit=circuit, define=define,
            panels=[(a, b) for a, b, _s, _e in mine],
            title=front_matter(text).get("title", stem),
            heading=heading_before(text, fm.start()),
            intro=clean(paragraph_before(text, fm.start()), titles),
            lead=clean(paragraph_before(text, lead_pos), titles)
            if lead_pos is not None else ""))
    # a panel nobody claimed
    for (stem, n), took in used.items():
        text, allf = cache[stem]
        have = len(panels_after(text, allf[n - 1], allf))
        if took != have:
            raise SystemExit(f"manual_runs: {stem} fence {n} has {have} "
                             f"result panel(s) and the table claims {took} -- "
                             "add the run for the new one to RUNS")
    return out


# ---------------------------------------------------------------------------
# The run as a package call, and a panel as a name and a value
# ---------------------------------------------------------------------------

def call_source(run: dict, c: str, r: str) -> str:
    """The run as the package call a person would type, with the circuit in
    variable `c` and the result bound to `r`. The notebook shows this text
    and the check executes it, so what is checked is what is shown."""
    how = run["how"]
    conds = run.get("define")
    extra = f", conditions={conds!r}" if conds else ""
    if how in ("dc", "fd", "tr"):
        return f"{r} = {how}({c}{extra})"
    if how == "ac":
        return f"{r} = ac({c}, omega={run['omega']}{extra})"
    n1, n2 = run["nodes"]
    if how == "th":
        return f"{r} = th({c}, {n1!r}, {n2!r}, domain='dc')"
    if how == "er":
        return f"{r} = er({c}, {n1!r}, {n2!r}, domain='dc')"
    if how == "port":
        return f"{r} = port({c}, {n1!r}, {n2!r}, {run['kind']!r}, domain='dc')"
    raise SystemExit(f"manual_runs: unknown how={how!r}")


def answers_expr(run: dict, r: str) -> str:
    """What evaluate() is handed for the run's result: the result itself,
    or for er(), which returns one expression, that expression under the
    name the Find equivalent card gives it."""
    return f"{{'req': {r}}}" if run["how"] == "er" else r


def tex_name(lhs: str) -> str:
    """A panel's left side as the name Evaluate reads: `v_{r2}` is `vr2`,
    `R_{eq}` is `req`, `-s_{e}` is `-se`. Lowercase, as the app writes an
    answer; Evaluate would find it either way."""
    return re.sub(r"[{}_\s]", "", lhs).lower()


def _fractions(s: str) -> str:
    pat = re.compile(r"\\d?frac\{([^{}]*)\}\{([^{}]*)\}")
    while pat.search(s):
        s = pat.sub(r"((\1)/(\2))", s)
    return s


def tex_expr(rhs: str):
    r"""A panel's right side as a SymPy expression, or SystemExit naming the
    LaTeX it could not read. It reads what the Manual's panels use -- a
    fraction, a power of e, a thin space for a product, `\text{j}` for the
    imaginary unit -- and refuses anything else, so a new kind of panel is
    seen instead of misread. Units are dropped."""
    import sympy as sp
    from sympy.parsing.sympy_parser import (
        parse_expr, standard_transformations, implicit_multiplication)

    s = rhs.strip()
    s = re.sub(r"\\[, ]*\\mathrm\{[^{}]*\}\s*$", "", s)      # \,\mathrm{V}
    s = re.sub(r"\\[, ]*\\Omega\s*$", "", s)                   # \,\Omega
    s = s.replace(r"\text{j}", "*I")
    s = _fractions(s)
    s = re.sub(r"e\^\{([^{}]*)\}", r"exp(\1)", s)
    s = re.sub(r"\^\{([^{}]*)\}", r"**(\1)", s)
    s = re.sub(r"\^(\w)", r"**\1", s)
    s = s.replace(r"\,", "*")
    s = s.replace("{", "(").replace("}", ")")
    if "\\" in s:
        raise SystemExit(f"manual_runs: cannot read the LaTeX {rhs!r} "
                         f"(left {s!r}); teach tex_expr the construct")
    names = {n: sp.Symbol(n) for n in set(re.findall(r"[A-Za-z_]\w*", s))
             if n not in ("exp", "I")}
    names["exp"] = sp.exp
    names["I"] = sp.I
    return parse_expr(s, local_dict=names, transformations=(
        standard_transformations + (implicit_multiplication,)))


def panel_decimals(rhs: str):
    """The fewest decimal places any number in a panel is printed with, or
    None when every number in it is exact. A panel that prints `0.0621`
    was rounded to four places; its tolerance is half of the last."""
    places = [len(m.group(1)) for m in re.finditer(r"\d\.(\d+)", rhs)]
    return min(places) if places else None
