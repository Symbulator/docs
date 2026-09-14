# -*- coding: utf-8 -*-
"""Run every spec through Symbulator and compare with the book's printed answer."""
import sys, io, os, re, cmath, importlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import sympy as sp
import symbulator as S

# --- paths, resolved from this file rather than hardcoded -------------------
# tools/<book> -> tools -> Documentation -> the project root. This file
# lives in tools/sampler and runs through the shim of the same name in
# each book's folder, so __file__ -- and so _HERE -- is that folder.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
DOCS = os.path.join(_ROOT, "Documentation")
EXAMPLES = os.path.join(_ROOT, "Application", "v9", "repos", "server", "examples")
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import book                                                   # noqa: E402
PDF = os.path.join(_ROOT, "Other", book.PDF)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

def _num(x):
    """SymPy expr -> complex, via its decimal string (see _round_expr note)."""
    if isinstance(x, (int, float, complex)): return complex(x)
    e = sp.sympify(x)
    e = sp.N(e, 18)
    return complex(sp.re(e), sp.im(e))

def _auto_ts(expr, n=7):
    """Sample points spanning the expression's own scale, from its exponents."""
    rates = []
    for e in expr.atoms(sp.exp):
        a = e.args[0]
        for x in a.free_symbols:
            c = a.coeff(x)
            try: c = abs(complex(sp.N(c)))
            except Exception: continue
            if c > 0: rates.append(c)
    if not rates: return [0.0, 0.1, 1.0, 10.0]
    r = max(rates)
    return [k / r for k in (0.0, 0.05, 0.2, 0.5, 1.0, 2.0, 4.0)][:n]

def close_at(got, want, tol, ts, var="t"):
    """Compare two expressions in t (or s) numerically at sample points -- the
    book prints a rounded closed form, so symbolic equality is too strict."""
    L = {"t": S.t, "s": S.s}
    g, w = sp.sympify(got, locals=L), sp.sympify(want, locals=L)
    x = L.get(var, sp.Symbol(var))
    for tv in ts:
        gv, wv = complex(sp.N(g.subs(x, tv), 18)), complex(sp.N(w.subs(x, tv), 18))
        scale = max(abs(wv), 1e-30)
        if abs(gv - wv) > tol * scale and abs(gv - wv) > 1e-12:
            return False, "at %s=%g got %.6g want %.6g" % (var, tv, gv.real, wv.real)
    return True, ""

def close(got, want, tol):
    if isinstance(want, str):                       # symbolic equality
        # sympify with Symbulator's own t and s: a plain sympify would make a
        # *different* t (theirs is declared nonnegative) and nothing cancels.
        # And with the answer's own symbols by name: `rf` on its own is
        # SymPy's rising factorial, not the feedback resistor.
        L = {"t": S.t, "s": S.s}
        g = sp.sympify(got, locals=L)
        L.update({str(x): x for x in getattr(g, "free_symbols", ())})
        w = sp.sympify(want, locals=L)
        d = sp.simplify(sp.expand(g - w))
        if d == 0: return True
        if not d.free_symbols:
            return abs(complex(sp.N(d))) < 1e-9
        # a float residue, or a rounded coefficient in the book's printed form:
        # settle it by sampling both over the expression's own time scale.
        # pick the variable to sample over from the expression itself
        free = sorted(d.free_symbols, key=lambda x: x.name)
        var = "t" if any(x.name == "t" for x in free) else (
              "s" if any(x.name == "s" for x in free) else free[0].name)
        ts = _auto_ts(g - w) if var == "t" else [0.5, 1.0, 3.0, 10.0, 100.0, 3000.0]
        good, _why = close_at(g, w, max(tol, 1e-6), ts, var)
        return good
    g, w = _num(got), _num(want)
    if abs(w) < 1e-12: return abs(g) <= max(tol, 1e-9)
    return abs(g - w) <= tol * abs(w)

def run_one(sp_):
    """Returns (Result-like, values dict)."""
    kind = sp_.get("kind", "circuit")
    d, dom = sp_["desc"], sp_.get("domain", "dc")
    kw = {}
    for k in ("equations", "unknowns", "conditions"):
        if sp_.get(k): kw[k] = sp_[k]
    if sp_.get("params"): kw["params"] = sp_["params"]
    if kind == "th":
        r = S.th(d, sp_["n1"], sp_["n2"], domain=dom,
                 omega=sp_.get("omega"), use_rms=sp_.get("rms", False), **kw)
        return r, {"vth": r.vth, "ino": r.ino, "z": r.z, "pmax": r.pmax}
    if kind == "er":
        r = S.er(d, sp_["n1"], sp_["n2"], domain=dom, omega=sp_.get("omega"), **kw)
        return r, {"z": r}
    if kind == "port":
        r = S.port(d, sp_["n1"], sp_["n2"], sp_["ptype"], domain=dom,
                   omega=sp_.get("omega"), **kw)
        return r, dict(r)
    if dom == "dc":   r = S.dc(d, **kw)
    elif dom == "ac": r = S.ac(d, sp_["omega"], use_rms=sp_.get("rms", False), **kw)
    elif dom == "fd": r = S.fd(d, **kw)
    elif dom == "tr":
        if sp_.get("vars"): kw["variables"] = sp_["vars"]
        r = S.tr(d, **kw)
    else: raise ValueError(dom)
    return r, dict(r.values)

SERVER = os.path.join(_ROOT, "Application", "v9", "repos", "server")


def app_values(s, digits=6, approx=True):
    """The circuit's answers as the page holds them -- `values`, keyed by
    name, from the real app's `solve_ui` -- which is what the Solve card
    is fed. Imported from the app tree, as build.py --check does."""
    if SERVER not in sys.path:
        sys.path.insert(0, SERVER)
    import symbulator_ui as ui
    w = s.get("omega")
    omega = ("omega" if (w is None or isinstance(w, sp.Symbol)) else str(sp.sympify(w))) \
        if s.get("domain") == "ac" else ""
    r = ui.solve_ui(s["desc"], s.get("domain", "dc"), omega, [], "solve", "", "", "z",
                    list(s.get("equations", [])), list(s.get("unknowns", [])), [],
                    digits=digits, approx=approx, units=True, use_rms=bool(s.get("rms")))
    assert r.get("ok"), r
    return r["values"]


def app_display(s, digits=6, approx=True):
    """What the app's CARDS show for a circuit: {answer name: {plain, latex}},
    keyed the way the page names an answer -- `v_2`, `i_l1`, and a Find
    equivalent answer by the card's own name, `vth`, `zeq`, `pmax`.

    `app_values` is the substitution dictionary the Evaluate card is fed and
    ignores the Rounding setting; this is the rendered answer the reader
    actually sees, which is what the page must reproduce (#443)."""
    if SERVER not in sys.path:
        sys.path.insert(0, SERVER)
    import symbulator_ui as ui
    w = s.get("omega")
    omega = ("omega" if (w is None or isinstance(w, sp.Symbol)) else str(sp.sympify(w))) \
        if s.get("domain") == "ac" else ""
    kind = s.get("kind", "circuit")
    tool = kind if kind in ("th", "er", "port") else "solve"
    r = ui.solve_ui(s["desc"], s.get("domain", "dc"), omega, [], tool,
                    s.get("n1", ""), s.get("n2", ""), s.get("ptype", "z"),
                    list(s.get("equations", [])), list(s.get("unknowns", [])), [],
                    digits=digits, approx=approx, units=True,
                    use_rms=bool(s.get("rms")))
    assert r.get("ok"), r.get("error")
    out = {}
    for n in r.get("nodes", []):
        out["v_%s" % n["node"]] = n
    for el in r.get("elements", []):
        for it in el.get("items", []):
            out["%s_%s" % (it["sym"], el["name"])] = it
    for it in r.get("extras", []) or []:
        if isinstance(it, dict) and "name" in it:
            out[it["name"]] = it
    return out


def app_minitool(s, mt, values=None, digits=6, approx=True):
    """One Mini-Tools step of a spec, through the real app's `mini_tool_ui`
    on the values the page holds: the tool's reply, `rows` and all."""
    if SERVER not in sys.path:
        sys.path.insert(0, SERVER)
    import symbulator_ui as ui
    values = values if values is not None else app_values(s, digits, approx)
    r = ui.mini_tool_ui(mt["tool"], list(mt["args"]), values, digits or 6)
    assert r.get("ok"), r
    return r


def app_byhand(s, bh, digits=6, approx=True):
    """The By-Hand Equations card for a spec, through the real app's
    `byhand_ui`: the chosen method's rows, loops and answers."""
    if SERVER not in sys.path:
        sys.path.insert(0, SERVER)
    import symbulator_ui as ui
    w = s.get("omega")
    omega = ("omega" if (w is None or isinstance(w, sp.Symbol)) else str(sp.sympify(w))) \
        if s.get("domain") == "ac" else ""
    r = ui.byhand_ui(s["desc"], s.get("domain", "dc"), omega, bh["method"],
                     digits=digits, units=True, approx=approx)
    assert r.get("ok"), r
    m = r["methods"][bh["method"]]
    assert m.get("supported"), (s["num"], m.get("reason"))
    assert m.get("verdict") == "agrees", (s["num"], m.get("verdict"), m.get("message"))
    # The card's answers arrive exact and the page rounds them to the
    # Rounding setting as it typesets them (#359), so a reading at n digits
    # is the app's own rounding applied here.
    if approx and digits:
        for a in m["answers"]:
            a["value"] = str(ui._round_expr(sp.sympify(a["value"]), digits))
    return r, m


def app_solveq(s, sq, values=None, digits=6, approx=True):
    """One Solve-card run of a spec, through the real app's `solveq_ui`:
    {name: plain} of the first solution, and the raw reply."""
    if SERVER not in sys.path:
        sys.path.insert(0, SERVER)
    import symbulator_ui as ui
    values = values if values is not None else app_values(s, digits, approx)
    r = ui.solveq_ui(list(sq["equations"]), list(sq.get("unknowns", [])), values,
                     digits=digits, approx=approx, units=True,
                     real_only=sq.get("real_only", True),
                     conditions=list(sq.get("conditions", [])),
                     domain=s.get("domain", "dc"))
    assert r.get("ok"), r
    sols = r.get("solutions") or []
    return ({v["name"]: v["plain"] for v in sols[0]} if sols else {}), r


def number_of(plain):
    """The number in a card's plain string, and its SymPy value: `0.16 + 0.12j`
    and `-3000.0 - 4000.0j` are one number each, not a number and some
    words, and a trailing unit (`40 Ω`, `2.5 mA`) is dropped."""
    txt = plain.strip()
    m = re.match(r"^(-?[\d.]+(?:[eE][-+]?\d+)?(?:\s*[-+]\s*[\d.]+(?:[eE][-+]?\d+)?j)?j?)", txt)
    num = m.group(1) if m else txt.split()[0]
    return num, sp.sympify(num.replace("j", "*I"))


def app_evaluate_display(s, expr, conditions=(), values=None, digits=6,
                         approx=True):
    """One Evaluate-card step as the card renders it: {plain, latex}."""
    if SERVER not in sys.path:
        sys.path.insert(0, SERVER)
    import symbulator_ui as ui
    values = values if values is not None else app_values(s, digits, approx)
    r = ui.evaluate_ui(expr, values, digits=digits, approx=approx,
                       domain=s.get("domain", "dc"),
                       conditions=list(conditions) or None)
    assert r.get("ok"), r
    return r


def app_evaluate(s, expr, conditions=(), values=None, digits=6, approx=True):
    """One Evaluate-card step of a spec, through the real app's
    `evaluate_ui`: the plain string the card shows."""
    if SERVER not in sys.path:
        sys.path.insert(0, SERVER)
    import symbulator_ui as ui
    values = values if values is not None else app_values(s, digits, approx)
    r = ui.evaluate_ui(expr, values, digits=digits, approx=approx,
                       domain=s.get("domain", "dc"), conditions=list(conditions) or None)
    assert r.get("ok"), r
    return r["plain"]


def check(specs, only=None, verbose=True):
    """Every spec, every first run a spec carries in `pre`, and every Solve
    card run it carries in `solveq`, solved and compared with the book. A
    first run is checked as a spec of its own, so the initial condition the
    main run carries is proved to be what the circuit before the switch
    actually gives; a Solve card run goes through the real app's `solveq_ui`
    on the values the page holds, so what the page prints for it is what
    the card prints."""
    expanded = []
    for s in specs:
        for i, pre in enumerate(s.get("pre", [])):
            expanded.append(dict(num="%s pre%d" % (s["num"], i + 1), title="first run",
                                 desc=pre["desc"], domain=pre.get("domain", "dc"),
                                 expect=pre["expect"]))
        expanded.append(s)
    bad, ok = _check(expanded, only, verbose, summary=False)
    # By-Hand Equations steps: the card's unknowns, exact, against the book
    for s in specs:
        if only and s["num"] not in only: continue
        bh = s.get("byhand")
        if not bh: continue
        _r, m = app_byhand(s, bh, digits=0, approx=False)
        got = {a["name"]: a["value"] for a in m["answers"]}
        fails = []
        for k, want in bh["expect"].items():
            try:
                good = k in got and close(sp.sympify(got[k]), want, s.get("tol", 0.006))
            except Exception as e:
                good = False
            if not good:
                fails.append((k, "got %r  want %r" % (got.get(k), want)))
        if fails:
            bad.append(("%s byhand" % s["num"], fails))
            print("XX %-6s By-Hand Equations" % s["num"])
            for k, msg_ in fails: print("        %-10s %s" % (k, msg_))
        else:
            ok += 1
            if verbose: print("ok %-6s By-Hand Equations" % s["num"])
    # Mini-Tools steps (#445): each row the page quotes, as the card prints it
    for s in specs:
        if only and s["num"] not in only: continue
        for i, mt in enumerate(s.get("minitool", [])):
            label = "%s minitool%d" % (s["num"], i + 1)
            got = app_minitool(s, mt, digits=4)
            # a one-value tool (pf, aa) replies with `plain` alone, read as row "value"
            rows = {r["key"]: r["plain"] for r in
                    (got.get("rows") or [{"key": "value", "plain": got["plain"]}])}
            fails = [(k, "got %r  want %r" % (rows.get(k), w))
                     for k, w in mt["expect"].items() if rows.get(k) != w]
            if fails:
                bad.append((label, fails))
                print("XX %-6s Mini-Tools step %d" % (s["num"], i + 1))
                for k, m in fails: print("        %-10s %s" % (k, m))
            else:
                ok += 1
                if verbose: print("ok %-6s Mini-Tools step %d" % (s["num"], i + 1))
    for s in specs:
        if only and s["num"] not in only: continue
        if not s.get("solveq"): continue
        values = app_values(s)
        for i, sq in enumerate(s.get("solveq", [])):
            label = "%s solveq%d" % (s["num"], i + 1)
            got, _r = app_solveq(s, sq, values)
            fails = []
            allsols = _r.get("solutions") or []
            for key, want in sq["expect"].items():
                if key not in got:
                    fails.append((key, "MISSING (have %s)" % sorted(got))); continue
                if isinstance(want, (list, tuple)):
                    # several roots: every one the book prints must be among the card's
                    plains = [v["plain"] for sol in allsols for v in sol if v["name"] == key]
                    for w in want:
                        try:
                            hit = any(close(number_of(p)[1], w, s.get("tol", 0.006)) for p in plains)
                        except Exception as e:
                            fails.append((key, "CMP %s" % e)); hit = True
                        if not hit:
                            fails.append((key, "root %s not among %s" % (w, plains)))
                    continue
                try:
                    good = close(number_of(got[key])[1], want, s.get("tol", 0.006))
                except Exception as e:
                    fails.append((key, "CMP %s (got %r)" % (e, got[key]))); continue
                if not good:
                    fails.append((key, "got %s  want %s" % (got[key], want)))
            if fails:
                bad.append((label, fails))
                print("XX %-6s Solve card run %d" % (s["num"], i + 1))
                for k, m in fails: print("        %-10s %s" % (k, m))
            else:
                ok += 1
                if verbose: print("ok %-6s Solve card run %d" % (s["num"], i + 1))
    print("\n--- %d ok, %d bad ---" % (ok, len(bad)))
    return bad


def _check(specs, only=None, verbose=True, summary=True):
    bad, ok = [], 0
    for s in specs:
        if only and s["num"].split(" ")[0] not in only: continue
        tol = s.get("tol", 0.006)
        try:
            r, vals = run_one(s)
        except Exception as e:
            bad.append((s["num"], "RAISED %s: %s" % (type(e).__name__, e))); 
            print("XX %-6s RAISED %s: %s" % (s["num"], type(e).__name__, str(e)[:160])); continue
        if s.get("subs"):
            vals = {k: (sp.sympify(v).subs(s["subs"]) if not isinstance(v, (int, float)) else v)
                    for k, v in vals.items()}
        fails = []
        for key, want in s["expect"].items():
            if key.startswith("@"):                    # arbitrary sympy expression
                expr = key[1:]
                try: got = sp.sympify(expr, locals={k: v for k, v in vals.items()})
                except Exception as e: fails.append((key, "EVAL %s" % e)); continue
            elif key in vals: got = vals[key]
            else: fails.append((key, "MISSING (have %d keys)" % len(vals))); continue
            if s.get("at_t") and isinstance(want, str):
                good, why = close_at(got, want, tol, s["at_t"], s.get("at_var", "t"))
                if not good: fails.append((key, why))
                continue
            try:
                if not close(got, want, tol):
                    fails.append((key, "got %s  want %s" % (sp.nsimplify(got, rational=False) if 0 else _fmt(got), _fmt(want))))
            except Exception as e:
                fails.append((key, "CMP %s (got %r)" % (e, got)))
        if fails:
            bad.append((s["num"], fails))
            print("XX %-6s %s" % (s["num"], s.get("title","")[:44]))
            for k, m in fails: print("        %-10s %s" % (k, m))
        else:
            ok += 1
            if verbose: print("ok %-6s %s" % (s["num"], s.get("title","")[:60]))
    if not summary:
        return bad, ok
    print("\n--- %d ok, %d bad ---" % (ok, len(bad)))
    return bad

def _fmt(x):
    try:
        c = _num(x)
        if abs(c.imag) < 1e-9: return "%.6g" % c.real
        return "%.6g%+.6gj" % (c.real, c.imag)
    except Exception: return str(x)

def dump(spec, keys=None, digits=6):
    r, vals = run_one(spec)
    print("### %s  %s" % (spec["num"], spec.get("title","")))
    for k in sorted(vals, key=lambda z: (z.split("_")[0], z)):
        if keys and not any(k == q or k.startswith(q) for q in keys): continue
        v = vals[k]
        try: print("  %-12s %s   ~ %s" % (k, v, _fmt(v)))
        except Exception: print("  %-12s %s" % (k, v))
    return r, vals
