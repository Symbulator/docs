import sys
import os
# -*- coding: utf-8 -*-
"""Formatting helpers shared by the page generator."""
import re
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

UNIT = {"v": "V", "i": "A", "p": "W", "r": "\\Omega", "z": "\\Omega",
        "s": "VA", "ap": "W"}

def elements(desc):
    """Element names in a description, in order."""
    out = []
    for line in re.split(r"[:\n]", desc):
        line = line.strip()
        if not line or ":" in line.split(",")[0]: continue
        nm = line.split(",")[0].strip()
        if nm and re.match(r"^[A-Za-z][A-Za-z0-9_]*$", nm): out.append(nm)
    return out

def label_for(key, desc, spec):
    """The small label a result panel carries, in the app's own words."""
    if spec.get("labels", {}).get(key): return spec["labels"][key]
    key = key.lstrip("@")
    if key in ("vth",):  return "Thevenin voltage"
    if key in ("ino",):  return "Norton current"
    if key == "z":       return "Thevenin impedance"
    if key == "pmax":    return "maximum power"
    if key in ("11", "12", "21", "22"):
        return "%s parameter z%s" % ("open-circuit", key)
    m = re.match(r"^(ap|[vipzrs])_(.+)$", key)
    if not m: return key
    kind, name = m.group(1), m.group(2)
    els = elements(desc)
    is_el = name in els
    if kind == "v":
        return ("voltage drop across %s" % name) if is_el else ("voltage at node %s" % name)
    if kind == "i":  return "current through %s" % name
    if kind == "p":  return "power consumed by %s" % name
    if kind == "ap": return "average power in %s" % name
    if kind == "s":  return "complex power in %s" % name
    if kind == "r":  return "resistance seen by %s" % name
    if kind == "z":  return "impedance seen by %s" % name
    return key

def unit_for(key, spec):
    if spec.get("units", {}).get(key) is not None: return spec["units"][key]
    if key.startswith("@"):
        # an expression over answers: take the unit of the first answer in it
        m = re.search(r"\b(ap|[vipzrs])_", key)
        return UNIT.get(m.group(1), "") if m else ""
    if key in ("vth",): return "V"
    if key in ("ino",): return "A"
    if key == "z":      return "\\Omega"
    if key == "pmax":   return "W"
    if key in ("11", "12", "21", "22"):
        return "\\Omega" if spec.get("ptype") == "z" else ""
    m = re.match(r"^(ap|[vipzrs])_", key)
    return UNIT.get(m.group(1), "") if m else ""

def tex_name(key, spec):
    """The answer's name, set the way the app prints it."""
    if spec.get("texnames", {}).get(key): return spec["texnames"][key]
    key = key.lstrip("@")
    if key == "vth": return "V_{Th}"
    if key == "ino": return "I_{N}"
    if key == "z":   return "Z_{Th}"
    if key == "pmax": return "p_{max}"
    if key in ("11", "12", "21", "22"): return "z_{%s}" % key
    m = re.match(r"^(ap|[vipzrs])_(.+)$", key)
    if not m: return sp.latex(sp.Symbol(key))
    return "%s_{%s}" % (m.group(1), m.group(2).replace("_", ""))

def tex_value(val, digits=6):
    """A SymPy answer as LaTeX, rounded the way the app's Rounding setting would."""
    e = sp.sympify(val)
    if not e.free_symbols: return sp.latex(_round(e, digits))
    e = e.replace(lambda x: x.is_Float, lambda x: _r1(x, digits))
    return sp.latex(e)


def _round(e, digits=6):
    """Round a number, real or complex, keeping a tidy Rational tidy."""
    e = sp.sympify(e)
    if e.is_Rational and abs(e.p) < 10**6 and abs(e.q) < 10**4: return e
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
    if x.is_Rational and abs(x.p) < 10**6 and abs(x.q) < 10**4: return x
    try:
        r = round_sig(x, digits)
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
    if e.free_symbols: return sp.sstr(_round(e, digits))
    re_, im_ = sp.re(e), sp.im(e)
    if im_ == 0: return _dec(_r1(re_, digits))
    im_txt = _dec(_r1(abs(im_), digits))
    if im_txt == "1": im_txt = ""
    if re_ == 0:                       # a pure imaginary reads -4j, not 0 - 4j
        return ("-" if im_ < 0 else "") + im_txt + "j"
    sign = "+" if im_ >= 0 else "-"
    return "%s %s %sj" % (_dec(_r1(re_, digits)), sign, im_txt)


def _dec(x):
    """A rounded SymPy number as a plain decimal string, no exponent noise."""
    if x.is_Integer: return str(int(x))
    if x.is_Rational and abs(x.q) <= 10000:
        f = float(x)
        if abs(f - round(f)) < 1e-12: return str(int(round(f)))
        return ("%.6g" % f)
    try:
        return ("%.6g" % float(x))
    except Exception:
        pass
    txt = sp.sstr(x)
    return txt.rstrip("0").rstrip(".") if "." in txt else txt
