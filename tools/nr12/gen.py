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
UNIT_WORD = {"V": "V", "A": "A", "W": "W", "VA": "VA", "S": "S", "H": "H", "s": "s",
             "\\Omega": "\u03a9", "": ""}


def tidy(txt):
    """A number as the card prints it, minus the trailing zeros a fixed digit
    count leaves: `3.20000` reads `3.2`, `-3000.0 - 4000.0j` reads
    `-3000 - 4000j`. The digits are unchanged, only their padding."""
    return re.sub(r"(-?\d+\.\d*?)0+(?=$|[^\d.])",
                  lambda m: m.group(1).rstrip("."), txt)


#: a problem's own variable written bare -- R1, V0, h11 -- outside code and maths
_VAR = re.compile(r"\b([A-Za-z])(\d{1,2})\b")
#: the spans polish() must not touch: `code` and $maths$
_KEEP = re.compile(r"`[^`]*`|\$[^$]*\$")


def _subscripts(chunk):
    return _VAR.sub(lambda m: "{{var:%s_%s}}" % (m.group(1), m.group(2)), chunk)


def _house(chunk):
    """The typography applied to one stretch of ordinary prose."""
    out = _subscripts(chunk)
    out = re.sub(r"(?<= )-(?= )", "—", out)          # " - " -> em dash
    out = out.replace(">=", "≥").replace("<=", "≤")
    out = re.sub(r"\bThevenin\b", "Thévenin", out)
    out = re.sub(r"(\d)\s*kilohms?\b", r"\1 kΩ", out, flags=re.I)
    # "ohm" after a number is a unit and becomes the sign; the bare word --
    # "in ohms", "given in ohms" -- stays a word, since "in Ω" is not English.
    out = re.sub(r"(\d)\s*ohms?\b", r"\1 Ω", out, flags=re.I)
    out = re.sub(r"(\d)\s*uF\b", r"\1 µF", out)
    out = re.sub(r"(\d)\s*uS\b", r"\1 µS", out)
    out = re.sub(r"(\d)\s*uH\b", r"\1 µH", out)
    return out


def polish(txt):
    """House typography: em dashes, ohms, micro, the accent on Thevenin, and a
    problem's own variables set as variables (#261) -- but never inside a code
    span or a maths span, where `ir3` and $i_L$ mean what they say.

    Every rule skips the kept spans, not only the variable one: the em-dash
    rule used to run over the whole string afterwards and turned the minus
    signs inside Example 5.3's $v_o = -4v_a - v_b - 5v_c$ into dashes."""
    parts, last = [], 0
    for m in _KEEP.finditer(txt):
        parts.append(_house(txt[last:m.start()]))
        parts.append(m.group(0))
        last = m.end()
    parts.append(_house(txt[last:]))
    return "".join(parts)


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
            bits.append("Leave **omega** in the {{ui:\u03c9 \u2014 angular frequency}} box; "
                        "nothing here depends on the frequency")
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
        if k in s.get("hide", ()):      # verified by the runner, shown elsewhere
            continue
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
            if k.startswith("@"):
                s.setdefault("_evalkeys", {})[shown] = k
            numeric.append((shown, fmt.plain_value(got), unit, polar_of(s, got),
                            s.get("booknames", {}).get(k)))
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


def evaluated_blocks(s, numeric):
    """Rule 11 and 12 (Roberto, 13 Sep 2026): an answer the reader gets by
    typing an expression into Evaluate is shown as that step -- the
    expression in the Evaluate box, as typed, and what the card gives --
    never as if the run had returned it. Returns the lines, and the
    numeric items that are plain results and stay in the returns sentence."""
    direct, lines = [], []
    first = True
    for item in numeric:
        name, val, unit, pol, book = item
        key = s.get("_evalkeys", {}).get(name)
        if key is None:
            direct.append(item)
            continue
        typed = key[1:].replace(" ", "")
        lines.append(("Then we type `%s` into {{card:Evaluate}}:" if first else
                      "Likewise `%s`:") % typed)
        first = False
        lines.append("")
        lines.append("```field 9 Evaluate")
        lines.append(typed)
        lines.append("```")
        lines.append("")
        u = UNIT_WORD.get(unit, unit)
        aside = [x for x in (pol, ("the book's $%s$" % book) if book else "") if x]
        lines.append("It gives {{o:%s}}%s%s." % (val, (" " + u) if u else "",
                     (" (%s)" % ", ".join(aside)) if aside else ""))
        lines.append("")
    return direct, lines


def numeric_sentence(numeric):
    """The numeric answers, as one plain sentence.

    It used to end "-- the same answers the book prints", forty-three times.
    The claim is made once instead, in the chapter's *How to read an entry*,
    and an entry whose answer needs a word about it (a sign, a rounding)
    says so in its own paragraph."""
    if not numeric:
        return ""
    parts = []
    for name, val, unit, pol, book in numeric:
        u = UNIT_WORD.get(unit, unit)
        # a shown name is code unless it is a phrase -- "the sum of all eight"
        prose = " " in name and "_" not in name
        shown = name if prose else "`%s`" % name
        txt = "%s = {{o:%s}}%s" % (shown, val, (" " + u) if u else "")
        # the answer is named against the book's own symbol *here*, beside
        # the value, and not in the paragraph above the run: a reader meets
        # an answer where the simulation finds it (Roberto, 12 Sep 2026)
        aside = [x for x in (pol, ("the book's $%s$" % book) if book else "") if x]
        if aside:
            txt += " (%s)" % ", ".join(aside)
        parts.append(txt)
    body = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]
    return "Symbulator returns " + body + "."


def render(s, vals):
    num = s["num"]
    L = ["::: problem %s" % titles.short_title(num), ""]
    # The book's own title ("Using Voltage Division and Current Division to
    # Solve a Circuit") is not shown: it names the book's method, which is
    # not how the reader will solve the problem (Roberto, 12 Sep 2026).
    L.append(polish(s["ask"]))
    L.append("")
    L.append("::: figure assets/circuit/%s" % figname(num))
    L.append("Nilsson & Riedel, 12th edition \u2014 the circuit for Example %s"
             % base_num(num))
    L.append(":::")
    L.append("")
    L.append("::: answer")
    # A first run, when the problem needs one: the circuit before the switch
    # moves, run in DC for the initial condition the main run then carries in
    # a fifth field. Nothing arrives from thin air -- a value that is not in
    # the problem statement is found on the page (Roberto, 12 Sep 2026).
    # The app links follow the Course's rule (Roberto, 12 Sep 2026): a
    # problem's first run links from the head, under the title, and only a
    # *later* run gets a placed link beside its own description. So a
    # one-run problem carries no applink at all, and a two-run problem
    # places the second.
    runs = 0
    for pre in s.get("pre", []):
        L.append(polish(pre["text"]))
        L.append("")
        L.append("```field 9 Circuit Description")
        L.extend(split_desc(pre["desc"]))
        L.append("```")
        L.append("")
        if runs:
            L.append("::: applink %s" % entry_name(s, pre["tag"]))
            L.append(":::")
            L.append("")
        runs += 1
        L.append(settings_line(pre_spec(s, pre)))
        L.append("")
        _panels, numeric = answer_blocks(pre_spec(s, pre), pre_values(s, pre))
        L.append(numeric_sentence(numeric))
        L.append("")
    L.append(polish(s["shows"]))
    L.append("")
    L.append("```field 9 Circuit Description")
    L.extend(split_desc(s["desc"]))
    L.append("```")
    L.append("")
    if runs:
        L.append("::: applink %s" % entry_name(s, main_tag(s)))
        L.append(":::")
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
    # a panel's answer is named against the book's symbol in a sentence
    # under the panels, the way a numeric answer is named beside its value
    named = [(k, s["booknames"][k]) for k in s["expect"]
             if k in s.get("booknames", {}) and k not in s.get("hide", ())
             and sp.sympify(vals.get(k, 0) if not k.startswith("@") else 0).free_symbols]
    if panels and named:
        bits = ["`%s` is the book's $%s$" % (s.get("shownames", {}).get(k, k), b)
                for k, b in named]
        L.append(("Here " if len(bits) > 1 else "") + (
            bits[0] if len(bits) == 1 else ", ".join(bits[:-1]) + " and " + bits[-1]) + ".")
        L.append("")
    direct, eval_lines = evaluated_blocks(s, numeric)
    sent = numeric_sentence(direct)
    if sent:
        L.append(sent)
        L.append("")
    L.extend(eval_lines)
    # Lettered parts that are read straight off the panel come before the
    # steps that answer the later parts (14.6: (a)-(c) from the transfer
    # function, then (d) in the Solve card) -- rule 14, the session's order.
    if s.get("parts_first"):
        for letter, text in s.get("parts", []):
            L.append("**%s)** %s" % (letter, polish(text)))
            L.append("")
    # An Evaluate step: a value the question wants at one instant or for
    # one set of inputs, read off the answer the way the Course does it --
    # the answer's name in the Evaluate box and the conditions in
    # Conditions (Lesson 6, Example 4.15). Computed by the real app's
    # evaluate_ui, so the page prints what the card prints.
    for ev in s.get("evals", []):
        L.append(polish(ev["text"]))
        L.append("")
        L.append("```field 9 Evaluate")
        L.append(ev["expr"])
        L.append("```")
        L.append("")
        conds = ["%s = %s" % (k, v) for k, v in ev.get("at", {}).items()]
        if conds:
            L.append("```field 9 Conditions")
            L.extend(conds)
            L.append("```")
            L.append("")
        got = runner.app_evaluate(s, ev["expr"], conds)
        num, val = runner.number_of(got)
        unit = UNIT_WORD.get(ev.get("unit", ""), ev.get("unit", ""))
        if ev.get("expect") is not None:
            assert runner.close(val, ev["expect"], 0.006), \
                "Evaluate %s at %s: got %s, book says %s" % (ev["expr"], ev.get("at"), got, ev["expect"])
        L.append("It gives {{o:%s}}%s%s." % (tidy(num), (" " + unit) if unit else "",
                 (" (the book's $%s$)" % ev["book"]) if ev.get("book") else ""))
        L.append("")
    # Solve card runs (Roberto, 13 Sep 2026: "my approach with Solve, which
    # is more representative of the exploratory way a student would
    # follow"). Each is shown with its own boxes and its own answer, read
    # from the real app's solveq_ui on the values the page holds. The
    # first run's fields travel in the problem's head entry; a later run
    # is an entry of its own, linked beside its boxes.
    if s.get("solveq"):
        values = runner.app_values(s)
        for i, sq in enumerate(s["solveq"]):
            # A later run that only changes one box shows that box alone
            # and is not an entry of its own (Roberto, 13 Sep 2026: "just
            # mention to the student what to change in the Conditions").
            boxes = sq.get("boxes", ("equations", "unknowns", "conditions"))
            L.append(polish(sq["text"]))
            L.append("")
            if "equations" in boxes:
                L.append("```field 9 Equation(s) to solve in terms of the results")
                L.extend(sq["equations"])
                L.append("```")
                L.append("")
            if "unknowns" in boxes:
                L.append("```field 9 Unknown(s) to solve for")
                L.append(", ".join(sq.get("unknowns", [])))
                L.append("```")
                L.append("")
            if "conditions" in boxes and sq.get("conditions"):
                L.append("```field 9 Conditions")
                L.extend(sq["conditions"])
                L.append("```")
                L.append("")
            if i and sq.get("entry", True):
                L.append("::: applink %s" % entry_name(s, sq["tag"]))
                L.append(":::")
                L.append("")
            if "press" in sq:
                L.append(polish(sq["press"]))
            else:
                L.append(("Tick {{ui:real solutions only}} and press {{btn:Solve equations}}."
                          if sq.get("real_only", True) else "Press {{btn:Solve equations}}."))
            L.append("")
            got, _r = runner.app_solveq(s, sq, values)
            sols = _r.get("solutions") or []
            units = sq.get("unit", "")

            def one(k, plain):
                u = units.get(k, "") if isinstance(units, dict) else units
                u = UNIT_WORD.get(u, u)
                shown = tidy(runner.number_of(plain)[0])
                txt = "`%s` = {{o:%s}}%s" % (k, shown, (" " + u) if u else "")
                if sq.get("book", {}).get(k):
                    txt += " (the book's $%s$)" % sq["book"][k]
                return txt
            for k in sq["expect"]:
                assert k in got, "Solve card run %d of %s did not return %s: %s" % (i + 1, s["num"], k, got)
            if len(sols) > 1:
                # several roots: the card lists them as solution 1 of n, 2 of n
                items = ["`%s` = {{o:%s}}" % (v["name"], tidy(runner.number_of(v["plain"])[0]))
                         for sol in sols for v in sol]
                L.append("The card returns %d solutions, %s." % (len(sols), " and ".join(items)))
            else:
                parts = [one(k, got[k]) for k in sq["expect"]]
                L.append("The card returns " + (parts[0] if len(parts) == 1 else
                         ", ".join(parts[:-1]) + " and " + parts[-1]) + ".")
            L.append("")
    # A problem with lettered parts gets each one answered, separately. The
    # page used to state the formula and leave (b) and (c) to the reader,
    # which is not answering the question (Roberto, 12 Sep 2026).
    for letter, text in ([] if s.get("parts_first") else s.get("parts", [])):
        L.append("**%s)** %s" % (letter, polish(text)))
        L.append("")
    # `after`: what follows from the answers -- a range read off a formula, a
    # value at t = 0 -- which belongs after the run, not in the paragraph
    # above it (Roberto, 12 Sep 2026: no results before the student finds them)
    if s.get("after"):
        L.append(polish(s["after"]))
        L.append("")
    L.append(":::")
    L.append(":::")
    return "\n".join(L)


def main_tag(s):
    """The parenthetical of the main run's entry: (DC), (Th\u00e9venin), (TR, Expert Mode)."""
    dom, kind = s.get("domain", "dc"), s.get("kind", "circuit")
    tag = {"dc": "DC", "ac": "AC", "tr": "TR", "fd": "FD"}[dom]
    if kind == "th":
        tag = "Th\u00e9venin"
    if kind == "port":
        tag = "%s parameters" % s["ptype"]
    if s.get("equations"):
        tag += ", Expert Mode"
    return tag


def entry_name(s, tag):
    # The name is the page's problem title plus a parenthetical saying which
    # run this is -- the shape app_links' stage 4 claims. parse_book cuts a
    # name at 80 characters, so this must stay short.
    name = "%s (%s)" % (titles.short_title(s["num"]), tag)
    assert len(name) <= 80, "entry name too long, parse_book would cut it: " + name
    return name


def pre_spec(s, pre):
    """A first run as a spec of its own: a plain DC circuit, the problem's
    question, and the book names it carries."""
    return dict(num=s["num"], desc=pre["desc"], domain=pre.get("domain", "dc"),
                expect=pre["expect"], booknames=pre.get("booknames", {}),
                shownames=pre.get("shownames", {}), units=pre.get("units", {}))


def pre_values(s, pre):
    _r, vals = runner.run_one(pre_spec(s, pre))
    return vals


def cir_entry(s):
    num, dom = s["num"], s.get("domain", "dc")
    kind = s.get("kind", "circuit")
    name = entry_name(s, main_tag(s))
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
    # the first Solve card run rides in the head entry, as Roberto's own
    # file had it; later runs are entries of their own (cir_solveq_entry)
    if s.get("solveq"):
        L.extend(solveq_fields(s["solveq"][0]))
    ask = re.sub(r"\s+", " ", s["ask"]).strip()
    # the note is plain text in a .cir, so unwrap the page's inline maths,
    # and a braced subscript with it: $h_{11}$ reads as h_11 in a note
    ask = re.sub(r"\$([^$]*)\$", r"\1", ask)
    ask = re.sub(r"_\{([^}]*)\}", r"_\1", ask)
    L.append("note: %s" % ask)      # the question alone; the book's title names its method
    if s.get("pre"):
        L.append("note: This is the circuit after the switch has moved; its initial "
                 "condition comes from the entry before it.")
    L.append("image: https://learn.symbulator.com/assets/circuit/%s" % figname(num))
    L.append("rounding: 6")
    L.append("si: no")
    L.append("units: yes")
    if dom == "ac":
        L.append("rms: %s" % ("yes" if s.get("rms") else "no"))
        L.append("polar: yes")
    L.append("")
    return "\n".join(L)


def solveq_fields(sq):
    """A Solve card run as .cir fields, the keys the app's own export writes."""
    L = ["solve_equations: %s" % eq for eq in sq["equations"]]
    if sq.get("unknowns"):
        L.append("solve_unknowns: %s" % ", ".join(sq["unknowns"]))
    L.extend("solve_conditions: %s" % c for c in sq.get("conditions", []))
    if sq.get("real_only", True):
        L.append("solve_real_only: yes")
    return L


def cir_solveq_entry(s, sq):
    """A later Solve card run as an entry of its own, just after the main
    one: the same circuit, the Solve card filled for this run."""
    dom = s.get("domain", "dc")
    ask = re.sub(r"\s+", " ", s["ask"]).strip()
    ask = re.sub(r"\$([^$]*)\$", r"\1", ask)
    ask = re.sub(r"_\{([^}]*)\}", r"_\1", ask)
    L = ["[%s]" % entry_name(s, sq["tag"]), ""]
    L.extend(split_desc(s["desc"]))
    L.append("")
    L.append("analysis: %s" % dom)
    L.extend(solveq_fields(sq))
    L.append("note: %s" % ask)
    L.append("note: %s" % sq["note"])
    L.append("image: https://learn.symbulator.com/assets/circuit/%s" % figname(s["num"]))
    L.append("rounding: 6")
    L.append("si: no")
    L.append("units: yes")
    L.append("")
    return "\n".join(L)


def cir_pre_entry(s, pre):
    """A first run as an entry of its own, just before the main one."""
    ask = re.sub(r"\s+", " ", s["ask"]).strip()
    ask = re.sub(r"\$([^$]*)\$", r"\1", ask)
    ask = re.sub(r"_\{([^}]*)\}", r"_\1", ask)
    L = ["[%s]" % entry_name(s, pre["tag"]), ""]
    L.extend(split_desc(pre["desc"]))
    L.append("")
    L.append("analysis: %s" % pre.get("domain", "dc"))
    L.append("note: %s" % ask)
    L.append("note: %s" % pre["note"])
    L.append("image: https://learn.symbulator.com/assets/circuit/%s" % figname(s["num"]))
    L.append("rounding: 6")
    L.append("si: no")
    L.append("units: yes")
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
                for pre in s.get("pre", []):
                    cir.append(cir_pre_entry(s, pre))
                cir.append(cir_entry(s))
                for sq in s.get("solveq", [])[1:]:
                    if sq.get("entry", True):
                        cir.append(cir_solveq_entry(s, sq))
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
    # The chapter's own prose is markdown beside this file, hand-editable:
    # chapter_head.md is everything before the first section (front matter,
    # opening, "How to read an entry"), and intro_<mode>.md is the paragraph
    # under each section heading. Roberto edits those; gen.py only assembles.
    head = io.open(os.path.join(_HERE, "chapter_head.md"), encoding="utf-8").read()
    text = head.rstrip("\n") + "\n\n" + "\n".join(body)
    # Each section's intro opens with its count in words. Counts restated in
    # prose go stale (root CLAUDE.md, "A number restated in a second file"),
    # so the intro is checked against the specs it introduces.
    words = {5: "Five", 8: "Eight", 14: "Fourteen", 16: "Sixteen"}
    for g in ORDER:
        n = sum(1 for s in rows if s.get("domain", "dc") == g)
        intro = io.open(os.path.join(_HERE, "intro_%s.md" % g),
                        encoding="utf-8").read().strip()
        assert intro.startswith(words.get(n, "%d " % n)), \
            "the %s intro says a different count from the %d specs it introduces" % (g, n)
        text = text.replace("@@INTRO_%s@@" % g.upper(), intro)
    text = re.sub(r"\n{4,}", "\n\n\n", text).rstrip() + "\n"
    out = os.path.join(DOCS, "src", "98-nr12-sampler.md")
    io.open(out, "w", encoding="utf-8", newline="\n").write(text)
    counts = {g: sum(1 for s in rows if s.get("domain", "dc") == g) for g in ORDER}
    print("entries:", len(rows), "| by mode:", counts)
    print("chapter ->", out, "|", len(text.splitlines()), "lines")


main()
