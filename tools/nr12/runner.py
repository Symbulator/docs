# -*- coding: utf-8 -*-
"""Run every spec through Symbulator and compare with the book's printed answer."""
import sys, io, os, re, cmath, importlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import sympy as sp
import symbulator as S

# --- paths, resolved from this file rather than hardcoded -------------------
# tools/nr12 -> tools -> Documentation -> the project root.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
DOCS = os.path.join(_ROOT, "Documentation")
EXAMPLES = os.path.join(_ROOT, "Application", "v9", "repos", "server", "examples")
PDF = os.path.join(_ROOT, "Other", "NR12.pdf")
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
