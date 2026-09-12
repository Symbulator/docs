# -*- coding: utf-8 -*-
"""Build the sampler chapter body and its .cir input file from the verified specs."""
import sys, os, re, io
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import sympy as sp
import runner, specs, fmt, titles

# --- paths, resolved from this file rather than hardcoded -------------------
# tools/nr12 -> tools -> Documentation -> the project root.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
DOCS = os.path.join(_ROOT, "Documentation")
EXAMPLES = os.path.join(_ROOT, "Application", "v9", "repos", "server", "examples")
PDF = os.path.join(_ROOT, "Other", "NR12.pdf")
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

MENU = {"dc": "*DC \u2014 direct current*", "ac": "*AC \u2014 alternating current*",
        "tr": "*TR \u2014 transient / time domain*",
        "fd": "*FD \u2014 complex frequency domain*"}
GROUP = {"dc": ("dc", "Direct current"), "tr": ("tr", "Transients"),
         "ac": ("ac", "Sinusoidal steady state"), "fd": ("fd", "The s domain")}
ORDER = ["dc", "tr", "ac", "fd"]
UNIT_WORD = {"V": "V", "A": "A", "W": "W", "VA": "VA", "S": "S",
             "\\Omega": "\u03a9", "": ""}


#: a problem's own variable written bare -- R1, V0, h11 -- outside code and maths
_VAR = re.compile(r"\b([A-Za-z])(\d{1,2})\b")
#: the spans polish() must not touch: `code` and $maths$
_KEEP = re.compile(r"`[^`]*`|\$[^$]*\$")


def _subscripts(chunk):
    return _VAR.sub(lambda m: "{{var:%s_%s}}" % (m.group(1), m.group(2)), chunk)


def polish(txt):
    """House typography: em dashes, ohms, micro, the accent on Thevenin, and a
    problem's own variables set as variables (#261) -- but never inside a code
    span or a maths span, where `ir3` and $i_L$ mean what they say."""
    out = txt
    parts, last = [], 0
    for m in _KEEP.finditer(out):
        parts.append(_subscripts(out[last:m.start()]))
        parts.append(m.group(0))
        last = m.end()
    parts.append(_subscripts(out[last:]))
    out = "".join(parts)
    out = re.sub(r"(?<= )-(?= )", "—", out)          # " - " -> em dash
    out = out.replace(">=", "≥").replace("<=", "≤")
    out = re.sub(r"\bThevenin\b", "Thévenin", out)
    out = re.sub(r"(\d)\s*kilohms?\b", r"\1 kΩ", out, flags=re.I)
    out = re.sub(r"\bkilohms?\b", "kΩ", out, flags=re.I)
    out = re.sub(r"(\d)\s*ohms?\b", r"\1 Ω", out, flags=re.I)
    out = re.sub(r"\bohms?\b", "Ω", out, flags=re.I)
    out = re.sub(r"(\d)\s*uF\b", r"\1 µF", out)
    out = re.sub(r"(\d)\s*uS\b", r"\1 µS", out)
    out = re.sub(r"(\d)\s*uH\b", r"\1 µH", out)
    return out


def sortkey(s):
    m = re.match(r"(\d+)\.(\d+)([a-z]?)", s["num"])
    return (int(m.group(1)), int(m.group(2)), m.group(3))


def figname(num):
    m = re.match(r"(\d+)\.(\d+)", num)
    return "nr12-ex%s-%s.jpg" % (m.group(1), m.group(2))


def base_num(num):
    return re.match(r"(\d+\.\d+)", num).group(1)


def split_desc(desc):
    """Colon form -> one element per line, keeping bracketed groups whole."""
    out, buf, depth = [], "", 0
    for ch in desc:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        if ch == ":" and depth == 0:
            out.append(buf.strip())
            buf = ""
        else:
            buf += ch
    if buf.strip():
        out.append(buf.strip())
    return [x for x in out if x]


def settings_line(s):
    kind, dom = s.get("kind", "circuit"), s.get("domain", "dc")
    bits = []
    if kind == "th":
        bits.append("Open {{card:Find equivalent}}, choose *Th\u00e9venin / Norton*, and "
                    "give the two terminals **%s** and **%s**" % (s["n1"], s["n2"]))
        if dom != "dc":
            bits.append("Set {{ui:Analysis}} to %s" % MENU[dom])
    elif kind == "port":
        bits.append("Open {{card:Find equivalent}}, choose *Two-port parameters*, kind "
                    "**%s**, with the ports at **%s** and **%s**"
                    % (s["ptype"], s["n1"], s["n2"]))
    else:
        bits.append("Set {{ui:Analysis}} to %s" % MENU[dom])
    if dom == "ac":
        w = s.get("omega")
        if w is None or isinstance(w, sp.Symbol):
            bits.append("Every impedance is given in ohms, so the frequency never enters: "
                        "leave **omega** in the {{ui:\u03c9 \u2014 angular frequency}} box")
        else:
            bits.append("Put **%s** in the {{ui:\u03c9 \u2014 angular frequency}} box"
                        % fmt.plain_value(sp.sympify(w)))
    if s.get("rms"):
        bits.append("Tick {{ui:RMS phasors}} in {{card:Settings}}, since the book's source "
                    "is given in rms")
    return ". ".join(bits) + "."


def answer_blocks(s, vals):
    """Result panels for answers that are expressions, prose for the numbers."""
    panels, numeric = [], []
    for k in s["expect"]:
        if k.startswith("@"):
            try:
                got = sp.sympify(k[1:], locals=dict(vals))
            except Exception:
                continue
        else:
            got = vals.get(k)
        if got is None:
            continue
        lbl = fmt.label_for(k, s["desc"], s)
        unit = fmt.unit_for(k, s)
        if sp.sympify(got).free_symbols:
            body = "%s = %s" % (fmt.tex_name(k, s), fmt.tex_value(got))
            if unit:
                body += "\\," + (unit if unit == "\\Omega" else "\\mathrm{%s}" % unit)
            panels.append("::: result %s\n%s\n:::" % (lbl, body))
        else:
            shown = s.get("shownames", {}).get(k, k[1:] if k.startswith("@") else k)
            numeric.append((shown, fmt.plain_value(got), unit, polar_of(s, got)))
    return panels, numeric


def polar_of(s, val):
    """An AC answer also reads as an amplitude and angle, which is how the book
    states most of them. Only worth printing when there is an angle to print."""
    if s.get("domain") != "ac":
        return ""
    e = sp.sympify(val)
    if e.free_symbols or sp.im(e) == 0:
        return ""
    import symbulator as S
    p = S.polar(e, 4)
    mag = str(p.magnitude).rstrip(".")      # polar() prints "1236." at 4 digits
    return "{{o:%s}}\u2220{{o:%s}}\u00b0" % (mag, str(p.angle).rstrip("."))


def numeric_sentence(numeric):
    if not numeric:
        return ""
    parts = []
    for name, val, unit, pol in numeric:
        u = UNIT_WORD.get(unit, unit)
        txt = "`%s` = {{o:%s}}%s" % (name, val, (" " + u) if u else "")
        if pol:
            txt += " (%s)" % pol
        parts.append(txt)
    body = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]
    return "Symbulator returns " + body + " \u2014 the same answers the book prints."


def render(s, vals):
    num = s["num"]
    L = ["::: problem %s" % titles.short_title(num), ""]
    # the book's own title for the example, which used to be in the heading:
    # it has to leave, because the heading is now the key app_links joins on.
    L.append("**%s.**" % polish(s["title"]))
    L.append("")
    L.append(polish(s["ask"]))
    L.append("")
    L.append("::: figure assets/circuit/%s" % figname(num))
    L.append("Nilsson & Riedel, 12th edition \u2014 the circuit for Example %s"
             % base_num(num))
    L.append(":::")
    L.append("")
    L.append("::: answer")
    L.append(polish(s["shows"]))
    L.append("")
    L.append("```field 9 Circuit Description")
    L.extend(split_desc(s["desc"]))
    L.append("```")
    L.append("")
    if s.get("equations"):
        L.append("```field 9 Add equation(s)")
        L.extend(s["equations"])
        L.append("```")
        L.append("")
    if s.get("unknowns"):
        L.append("```field 9 Add unknown(s)")
        L.append(", ".join(s["unknowns"]))
        L.append("```")
        L.append("")
    extra = (" This one needs {{ui:Enable Expert Mode}} ticked in the {{card:Expert Mode}} "
             "box; the equations and unknowns go in the fields it reveals."
             if s.get("equations") else "")
    L.append(settings_line(s) + extra)
    L.append("")
    panels, numeric = answer_blocks(s, vals)
    for p in panels:
        L.append(p)
        L.append("")
    sent = numeric_sentence(numeric)
    if sent:
        L.append(sent)
        L.append("")
    # A problem with lettered parts gets each one answered, separately. The
    # page used to state the formula and leave (b) and (c) to the reader,
    # which is not answering the question (Roberto, 12 Sep 2026).
    for letter, text in s.get("parts", []):
        L.append("**%s)** %s" % (letter, polish(text)))
        L.append("")
    L.append(":::")
    L.append(":::")
    return "\n".join(L)


def cir_entry(s):
    num, dom = s["num"], s.get("domain", "dc")
    kind = s.get("kind", "circuit")
    tag = {"dc": "DC", "ac": "AC", "tr": "TR", "fd": "FD"}[dom]
    if kind == "th":
        tag = "Th\u00e9venin"
    if kind == "port":
        tag = "%s parameters" % s["ptype"]
    if s.get("equations"):
        tag += ", Expert Mode"
    # The name is the page's problem title plus a parenthetical saying which
    # run this is -- the shape app_links' stage 4 claims. parse_book cuts a
    # name at 80 characters, so this must stay short.
    name = "%s (%s)" % (titles.short_title(num), tag)
    assert len(name) <= 80, "entry name too long, parse_book would cut it: " + name
    L = ["[%s]" % name, ""]
    L.extend(split_desc(s["desc"]))
    L.append("")
    L.append("analysis: %s" % dom)
    if kind == "th":
        L += ["tool: th", "n1: %s" % s["n1"], "n2: %s" % s["n2"]]
    if kind == "port":
        L += ["tool: port", "kind: %s" % s["ptype"],
              "n1: %s" % s["n1"], "n2: %s" % s["n2"]]
    if dom == "ac":
        w = s.get("omega")
        L.append("omega: %s" % ("omega" if (w is None or isinstance(w, sp.Symbol))
                                else fmt.plain_value(sp.sympify(w))))
    for eq in s.get("equations", []):
        L.append("equations: %s" % eq)
    if s.get("unknowns"):
        L.append("unknowns: %s" % ", ".join(s["unknowns"]))
    ask = re.sub(r"\s+", " ", s["ask"]).strip()
    # the note is plain text in a .cir, so unwrap the page's inline maths
    ask = re.sub(r"\$([^$]*)\$", r"\1", ask)
    L.append("note: %s. %s" % (s["title"], ask))
    L.append("image: https://learn.symbulator.com/assets/circuit/%s" % figname(num))
    L.append("rounding: 6")
    L.append("si: no")
    L.append("units: yes")
    if dom == "ac":
        L.append("rms: %s" % ("yes" if s.get("rms") else "no"))
        L.append("polar: yes")
    L.append("")
    return "\n".join(L)


def main():
    rows = sorted(specs.SPECS, key=sortkey)
    solved = {}
    for s in rows:
        _r, vals = runner.run_one(s)
        solved[s["num"]] = vals
    cir = ["# Symbulator circuit book", "",
           "title: Problems from Nilsson & Riedel 12ed", ""]
    for grp in ORDER:
        for s in rows:
            if s.get("domain", "dc") == grp:
                cir.append(cir_entry(s))
    # The book ships with the app: repos/server/examples is the source, and
    # build_local.py generates the repos/local copy from it.
    io.open(os.path.join(EXAMPLES, "Nilsson_Riedel.cir"), "w",
            encoding="utf-8", newline="\n").write("\n".join(cir).rstrip() + "\n")
    body = []
    for grp in ORDER:
        gid, gname = GROUP[grp]
        body.append("## %s \u2014 %s {#nr12-%s}" % (gname, grp.upper(), gid))
        body.append("")
        body.append("@@INTRO_%s@@" % grp.upper())
        body.append("")
        for s in rows:
            if s.get("domain", "dc") == grp:
                body.append(render(s, solved[s["num"]]))
                body.append("")
    import chapter_parts as CP
    text = CP.FRONT + "\n" + CP.OPENING + "\n" + "\n".join(body)
    for g in ORDER:
        text = text.replace("@@INTRO_%s@@" % g.upper(), CP.INTROS[g.upper()].strip())
    text = re.sub(r"\n{4,}", "\n\n\n", text).rstrip() + "\n"
    out = os.path.join(DOCS, "src", "98-nr12-sampler.md")
    io.open(out, "w", encoding="utf-8", newline="\n").write(text)
    counts = {g: sum(1 for s in rows if s.get("domain", "dc") == g) for g in ORDER}
    print("entries:", len(rows), "| by mode:", counts)
    print("chapter ->", out, "|", len(text.splitlines()), "lines")


main()
