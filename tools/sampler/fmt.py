import sys
import os
# -*- coding: utf-8 -*-
"""Formatting helpers shared by the page generator."""
import re
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

UNIT = {"v": "V", "i": "A", "p": "W", "r": "\\Omega", "z": "\\Omega",
        "s": "VA", "ap": "W", "q": "var"}

#: a problem number: `2.10` an example, `p2.10` a practice problem, either
#: with a letter for a second entry on the same problem (`5.3c`, `7.11a`)
_NUM = re.compile(r"^(p?)(\d+)\.(\d+)([a-z]?)$")


def parse_num(num):
    """(practice?, chapter, number, letter) of a problem number."""
    m = _NUM.match(num)
    assert m, "not a problem number: %r" % num
    return m.group(1) == "p", int(m.group(2)), int(m.group(3)), m.group(4)


def base_num(num):
    """`2.10` of `p2.10a`: the number the book prints."""
    _p, ch, n, _l = parse_num(num)
    return "%d.%d" % (ch, n)


def num_label(num):
    """What the book calls the problem: *Example* or *Practice Problem*."""
    return "Practice Problem" if parse_num(num)[0] else "Example"


def figname(num):
    """The figure file a problem shows, shared by its lettered entries."""
    practice, ch, n, _l = parse_num(num)
    return book.FIGNAME % ("pp" if practice else "ex", ch, n)


def elements(desc):
    """Element names in a description, in order."""
    out = []
    for line in re.split(r"[:\n]", desc):
        line = line.strip()
        if not line or ":" in line.split(",")[0]: continue
        nm = line.split(",")[0].strip()
        if nm and re.match(r"^[A-Za-z][A-Za-z0-9_]*$", nm): out.append(nm)
    return out

# The Find equivalent card's answers, as the card itself names, labels and
# typesets them (symbulator_ui._TOOL_LABELS and the template's TEXNAME).
# The runner keys the equivalent as `z`, th()'s own attribute; the page
# never shows that key (Roberto, 13 Sep 2026: "the card never reports the
# equivalent resistance as z. Even in AC, it is reported as zeq. But in
# DC, it is req.").
TOOL_LABELS = {"vth": "Thevenin voltage", "ino": "Norton current",
               "req": "equivalent resistance", "zeq": "equivalent impedance",
               "pmax": "maximum deliverable power"}
TOOL_TEX = {"vth": "v_{th}", "ino": "i_{no}", "req": "R_{eq}", "zeq": "Z_{eq}",
            "pmax": "p_{max}"}


def tool_name(key, spec):
    """The name the card prints for a Find equivalent answer, or None
    when the key is not one of the card's."""
    key = key.lstrip("@")
    if key == "z":
        return "req" if spec.get("domain", "dc") == "dc" else "zeq"
    return key if key in TOOL_LABELS else None


def shown_name(key, spec):
    """The name an answer is called in prose: the spec's own spelling,
    the card's name for a tool answer, else the key."""
    if spec.get("shownames", {}).get(key): return spec["shownames"][key]
    return tool_name(key, spec) or (key[1:] if key.startswith("@") else key)


def label_for(key, desc, spec):
    """The small label a result panel carries, in the app's own words."""
    if spec.get("labels", {}).get(key): return spec["labels"][key]
    tn = tool_name(key, spec)
    if tn: return TOOL_LABELS[tn]
    key = key.lstrip("@")
    if key in ("11", "12", "21", "22"):
        return "%s parameter z%s" % ("open-circuit", key)
    m = re.match(r"^(ap|[vipqzrs])_(.+)$", key)
    if not m: return key
    kind, name = m.group(1), m.group(2)
    els = elements(desc)
    is_el = name in els
    if kind == "v":
        return ("voltage drop across %s" % name) if is_el else ("voltage at node %s" % name)
    if kind == "i":  return "current through %s" % name
    if kind == "p":  return ("average (real) power consumed by %s" if spec.get("domain") == "ac"
                             else "power consumed by %s") % name
    if kind == "ap": return "average (real) power in %s" % name
    if kind == "q":  return "reactive power in %s" % name
    if kind == "s":  return "complex power in %s" % name
    if kind == "r":  return "resistance seen by %s" % name
    if kind == "z":  return "impedance seen by %s" % name
    return key

def unit_for(key, spec):
    if spec.get("units", {}).get(key) is not None: return spec["units"][key]
    if key.startswith("@"):
        # an expression over answers: take the unit of the first answer in it
        m = re.search(r"\b(ap|[vipqzrs])_", key)
        return UNIT.get(m.group(1), "") if m else ""
    if key in ("vth",): return "V"
    if key in ("ino",): return "A"
    if key == "z":      return "\\Omega"
    if key == "pmax":   return "W"
    if key in ("11", "12", "21", "22"):
        return "\\Omega" if spec.get("ptype") == "z" else ""
    m = re.match(r"^(ap|[vipqzrs])_", key)
    return UNIT.get(m.group(1), "") if m else ""

def tex_name(key, spec):
    """The answer's name, set the way the app prints it."""
    if spec.get("texnames", {}).get(key): return spec["texnames"][key]
    tn = tool_name(key, spec)
    if tn: return TOOL_TEX[tn]
    key = key.lstrip("@")
    if key in ("11", "12", "21", "22"): return "z_{%s}" % key
    m = re.match(r"^(ap|[vipqzrs])_(.+)$", key)
    if not m: return sp.latex(sp.Symbol(key))
    return "%s_{%s}" % (m.group(1), m.group(2).replace("_", ""))

def _approx_plain(e):
    """A number at *approx (full precision)*, as the app prints it: the
    shortest decimal that round-trips (symbulator_ui._approx_format)."""
    if e.is_Integer: return str(e)
    val = complex(e)
    if abs(val.imag) < 1e-30: return repr(val.real)
    re_t, im_t = repr(val.real), repr(abs(val.imag))
    if abs(val.real) < 1e-30: return ("-" if val.imag < 0 else "") + im_t + "j"
    return "%s %s %sj" % (re_t, "-" if val.imag < 0 else "+", im_t)


def tex_value(val, digits=6):
    """A SymPy answer as LaTeX, rounded the way the app's Rounding setting would."""
    e = sp.sympify(val)
    if not digits:                      # approx (full precision), as the app
        return sp.latex(sp.N(e))
    if not e.free_symbols: return sp.latex(_round(e, digits))
    e = e.replace(lambda x: x.is_Float, lambda x: _r1(x, digits))
    return sp.latex(e)


def _round(e, digits=6):
    """Round a number, real or complex, keeping a tidy Rational tidy."""
    e = sp.sympify(e)
    if e.is_Integer: return e
    try:
        re_, im_ = sp.re(e), sp.im(e)
    except Exception:
        return e
    if im_ == 0: return _r1(re_, digits)
    return _r1(re_, digits) + sp.I * _r1(im_, digits)


def _r1(x, digits=6):
    """One real number, rounded in decimal.

    round_sig() takes a SymPy expression, not a Python float -- hand it a
    float and it returns it untouched, silently. See #318.
    """
    from symbulator._display import round_sig
    x = sp.sympify(x)
    if x == 0: return sp.Integer(0)
    if x.is_Integer: return x
    try:
        r = round_sig(x, digits)
        # round_sig returns a Float carrying only `digits` of *binary*
        # precision, so float(r) and "%.6g" print its noise -- 2.66699
        # for 2.667. Read it back through its decimal string (#391).
        r = sp.Float(sp.sstr(r), 15)
    except Exception:
        return x
    # `r == int(r)` is False for a rounded Float: it carries only `digits` of
    # precision, so SymPy will not call it equal to the exact integer. Compare
    # through Python's float instead.
    try:
        rf = float(r)
        if rf == int(rf) and abs(rf) < 10**12: return sp.Integer(int(rf))
    except Exception:
        pass
    return r


def plain_value(val, digits=6):
    """A number as the page's prose reads it -- for {{o:...}} spans."""
    e = sp.sympify(val)
    if not digits:
        return sp.sstr(sp.N(e)) if e.free_symbols else _approx_plain(e)
    if e.free_symbols: return sp.sstr(_round(e, digits))
    re_, im_ = sp.re(e), sp.im(e)
    if im_ == 0: return _dec(_r1(re_, digits), digits)
    im_txt = _dec(_r1(abs(im_), digits), digits)
    if im_txt == "1": im_txt = ""
    if re_ == 0:                       # a pure imaginary reads -4j, not 0 - 4j
        return ("-" if im_ < 0 else "") + im_txt + "j"
    sign = "+" if im_ >= 0 else "-"
    return "%s %s %sj" % (_dec(_r1(re_, digits), digits), sign, im_txt)


def _dec(x, digits=6):
    """A rounded SymPy number as a plain decimal string at `digits`
    significant figures, written out in full -- no exponent, no binary
    noise, no trailing zeros: 33333.33 at 7, 0.0002026 at 4."""
    import math
    if x.is_Integer: return str(int(x))
    try:
        f = float(x)
    except Exception:
        txt = sp.sstr(x)
        return txt.rstrip("0").rstrip(".") if "." in txt else txt
    if f == 0: return "0"
    if abs(f - round(f)) < 1e-9 * max(1.0, abs(f)): return str(int(round(f)))
    exp = math.floor(math.log10(abs(f)))
    txt = "%.*f" % (max(digits - 1 - exp, 0), f)
    return txt.rstrip("0").rstrip(".") if "." in txt else txt
