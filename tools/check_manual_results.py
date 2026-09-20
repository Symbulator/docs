r"""Every printed answer in the Manual against the solver (#466).

    py tools\check_manual_results.py
    py tools\check_manual_results.py --package-only
    py tools\check_manual_results.py --prove-red

`check_manual_examples.py` proves every Manual circuit parses and solves.
It says, in its own words, what it does not do: compare the `::: result`
panels with what the solver returns, and a panel is hand-written LaTeX that
nothing checked -- which is how TR5's Example 4.5 printed a wrong subscript
for as long as it existed (#370). This does it.

For each run in `manual_runs.RUNS`, it takes the run's circuit from the
chapter, runs it, and for each of the run's panels reads the panel back
into a SymPy expression and compares it with the answer the panel names,
from **two independent sources**:

  * the package -- the very call the notebook shows, executed, then
    `evaluate()`; and
  * the app -- the circuit posted to the real `/api/solve`, then the real
    `/api/evaluate`, which is what a reader sees.

A panel must match both, and the two must agree with each other, since the
solver's API is not the app (#425).

**How two answers are compared.** A panel printed with decimals was rounded
to those places, so its tolerance is half of the last: `0.0621` stands for
anything within 0.00005. An exact panel must simplify to the same
expression, and failing that must agree numerically -- at sample points of
several sizes, because `e^(-1000 t)` at t = 1 is 1e-435 for any time
constant and would make a wrong one look right.

`--prove-red` damages every panel two ways -- adds one, and halves the
exponent of a decaying term -- and must report both. A check nobody has
seen fail is not a guard.

Exit status is 1 on any disagreement, and on a table that no longer matches
the chapters.
"""
from __future__ import annotations

import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(HERE)
ROOT = os.path.dirname(DOCS)
SOLVER = os.path.join(ROOT, "Application", "v9", "repos", "solver")
SERVER = os.path.join(ROOT, "Application", "v9", "repos", "server")

for tree in (SOLVER, SERVER):
    if not os.path.isdir(tree):
        raise SystemExit(
            f"check_manual_results: {tree} is missing. This checks the "
            "Manual against the solver and the app, so both trees must sit "
            "beside Documentation -- see the top-level CLAUDE.md.")
sys.path.insert(0, HERE)
sys.path.insert(0, SERVER)
sys.path.insert(0, SOLVER)          # first: the working tree's symbulator

import manual_runs as mr                                    # noqa: E402

# functions an answer can hold; every other identifier is a plain symbol
_FUNCS = {"exp", "sin", "cos", "sqrt", "log", "Abs", "re", "im", "I", "pi"}


def _as_expr(sp, value):
    """`value` as an expression whose symbols are plain -- the solver's `t`
    carries an assumption a panel's does not, and they must meet."""
    text = str(value)
    text = re.sub(r"(?<![\w.])(\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)j(?![\w])",
                  r"\1*I", text)
    text = text.replace("∞", "oo")
    names = {n: sp.Symbol(n) for n in set(re.findall(r"[^\W\d]\w*", text))
             if n not in _FUNCS and n != "oo"}
    return sp.sympify(text, locals=names)


def agree(sp, want, got, places):
    """'' when `got` is what a panel printing `want` stands for, else why not.

    `places` is the panel's decimal places (None = exact)."""
    want, got = _as_expr(sp, want), _as_expr(sp, got)
    symbols = sorted(want.free_symbols | got.free_symbols, key=str)
    if places is None:
        try:
            if sp.simplify(want - got) == 0:
                return ""
        except Exception:                                   # noqa: BLE001
            pass
        tol = 1e-9
    else:
        tol = 0.51 * 10.0 ** (-places)
    rng = random.Random(466)
    scales = (0.7, 1.3, 7e-4, 1.7e-3, 3.1)
    for _ in range(1 if not symbols else 12):
        at = {s: sp.Float(rng.choice(scales) * rng.uniform(0.9, 1.1))
              for s in symbols}
        a, b = (complex(sp.N(x.subs(at))) for x in (want, got))
        # exact: relative to the size of the answer; rounded: absolute,
        # half a unit in the last printed place
        limit = tol * max(1.0, abs(a)) if places is None else tol
        if abs(a - b) > limit:
            return f"panel {want}, solver {got}"
    return ""


def damaged(tex_rhs: str, how: str):
    """The panel's answer made wrong, for --prove-red: as a SymPy
    expression, or None when this kind of damage does not apply to it.
    `add` adds one to what the panel says; `halve` halves the rate of a
    decaying exponential, the mistake a small sample of t would miss."""
    want = mr.tex_expr(tex_rhs)
    if how == "add":
        return want + 1
    if how == "halve" and re.search(r"e\^\{-(\d+)", tex_rhs):
        return mr.tex_expr(re.sub(
            r"e\^\{-(\d+)", lambda m: "e^{-%d" % (int(m.group(1)) // 2),
            tex_rhs))
    return None


def run_checks(package_only: bool = False, prove: bool = False) -> tuple:
    """(problems, runs, panels, compared, caught): the whole check, with
    nothing printed, so `build.py --check` can run it and report in its
    own voice. `package_only` skips the app, which is 110 seconds of the
    two minutes; `prove` damages each panel instead of reading it as
    printed. Raises SystemExit, naming the run, when `manual_runs.RUNS` and
    the chapters no longer agree."""
    import warnings
    warnings.filterwarnings("ignore")
    import sympy as sp

    package_only = package_only or prove
    runs = mr.resolve()

    ns: dict = {}
    exec("import sympy as sp\nfrom symbulator import (dc, ac, fd, tr, th, "
         "er, port, evaluate)", ns)

    client = None
    if not package_only:
        os.chdir(SERVER)
        import app as flask_app
        client = flask_app.app.test_client()

    problems, compared, caught = [], 0, 0
    for n, run in enumerate(runs, 1):
        where = f"[{n}] {run['chapter']} fence {run['fence']} ({run['how']})"
        circuit = run["circuit"].strip()
        ns["c"] = circuit
        try:
            exec(mr.call_source(run, "c", "r"), ns)
        except Exception as exc:                            # noqa: BLE001
            problems.append(f"{where}: the run raises -- "
                            f"{str(exc).splitlines()[0][:110]}")
            continue
        app_values = None
        if client is not None:
            app_values, err = app_solve(client, run, circuit)
            if err:
                problems.append(f"{where}: the app refuses it -- {err}")
                continue
        for label, tex in run["panels"]:
            lhs, _eq, rhs = tex.partition("=")
            name = mr.tex_name(lhs)
            places = mr.panel_decimals(rhs)
            compared += 1
            try:
                if prove:
                    attempts = [(k, damaged(rhs, k)) for k in ("add", "halve")]
                else:
                    attempts = [("as printed", mr.tex_expr(rhs))]
            except SystemExit as exc:
                problems.append(f"{where}: {label}: {exc}")
                continue
            for kind, want in attempts:
                if want is None:
                    continue
                # the same cell the notebook shows: a TR or FD drop is a
                # difference of node voltages, anything else is evaluate()
                pkg = eval(mr.answer_source(run, "r", name, circuit), ns)
                why = agree(sp, want, pkg, places)
                if why and prove:
                    caught += 1
                elif why:
                    problems.append(f"{where}: {label} ({name}) differs "
                                    f"from the package -- {why}")
                if client is not None and not prove:
                    got = app_evaluate(client, run, app_values, name)
                    if got.startswith("ERROR"):
                        problems.append(f"{where}: {label}: the app's "
                                        f"Evaluate refuses {name!r} -- {got}")
                        continue
                    why = agree(sp, want, got, places)
                    if why:
                        problems.append(f"{where}: {label} ({name}) differs "
                                        f"from the app -- {why}")
                    if agree(sp, pkg, got, None):
                        problems.append(f"{where}: {label} ({name}): the "
                                        f"package says {pkg}, the app {got}")
    n_panels = sum(len(r["panels"]) for r in runs)
    return problems, runs, n_panels, compared, caught


def main() -> int:
    prove = "--prove-red" in sys.argv
    package_only = "--package-only" in sys.argv or prove
    problems, runs, n_panels, compared, caught = run_checks(
        package_only=package_only, prove=prove)
    print(f"{len(runs)} runs, {n_panels} panels, {compared} compared"
          + ("" if package_only else " against the package and the app"))
    for p in problems:
        print("  **", p)
    if prove:
        need = 2 * n_panels - sum(
            1 for r in runs for _l, t in r["panels"]
            if not re.search(r"e\^\{-(\d+)", t.partition("=")[2]))
        print(f"prove-red: {caught} of {need} damaged panels caught",
              "-- RED, as it should be" if caught == need and not problems
              else "-- THIS CHECK CANNOT FAIL")
        return 0 if caught == need and not problems else 1
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


def app_solve(client, run: dict, circuit: str):
    """(values, error) from the real /api/solve for the run."""
    how = run["how"]
    payload = {
        "desc": circuit, "domain": "dc" if how in ("th", "er", "port")
        else how, "omega": str(run.get("omega", "")),
        "tool": how if how in ("th", "er", "port") else "solve",
        "n1": (run.get("nodes") or ("", ""))[0],
        "n2": (run.get("nodes") or ("", ""))[1],
        "kind": run.get("kind", "z"),
        "defines": run.get("define") or [],
        "units": False, "equations": [], "unknowns": "", "conditions": [],
    }
    got = client.post("/api/solve", json=payload).get_json()
    if not got.get("ok"):
        return None, got.get("error")
    return got.get("values") or {}, None


def app_evaluate(client, run: dict, values: dict, name: str) -> str:
    """The app's Evaluate card on `name`, as the plain text it returns."""
    got = client.post("/api/evaluate", json={
        "expr": name, "values": values,
        "domain": "dc" if run["how"] in ("th", "er", "port") else run["how"],
        "units": False, "defines": run.get("define") or []}).get_json()
    return got.get("plain") if got.get("ok") else f"ERROR {got.get('error')}"


if __name__ == "__main__":
    sys.exit(main())
