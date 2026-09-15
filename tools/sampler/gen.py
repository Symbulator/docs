# -*- coding: utf-8 -*-
"""Build the sampler chapter body and its .cir input file from the verified specs."""
import sys, os, re, io
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import sympy as sp
import runner, specs, fmt, titles

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

MENU = {"dc": "*DC \u2014 direct current*", "ac": "*AC \u2014 alternating current*",
        "tr": "*TR \u2014 transient / time domain*",
        "fd": "*FD \u2014 complex frequency domain*"}
GROUP = {"dc": ("dc", "Direct current"), "tr": ("tr", "Transients"),
         "ac": ("ac", "Sinusoidal steady state"), "fd": ("fd", "The s domain")}
ORDER = ["dc", "tr", "ac", "fd"]
UNIT_WORD = {"V": "V", "A": "A", "W": "W", "VA": "VA", "S": "S", "H": "H", "s": "s",
             "\\Omega": "\u03a9", "": ""}


#: rule 32: the prefixes the app's *Use SI prefixes in answers* setting prints,
#: and what each multiplies by. The card writes micro as `u`; the page as µ.
SI_FACTOR = {"": 1, "k": 10**3, "M": 10**6, "G": 10**9,
             "m": sp.Rational(1, 10**3), "u": sp.Rational(1, 10**6),
             "\u00b5": sp.Rational(1, 10**6), "n": sp.Rational(1, 10**9),
             "p": sp.Rational(1, 10**12)}


def si_split(plain):
    """A card's SI reading, `(-484.6 - 230.3j) mV` or `-74.76 m`, as
    (number, prefix, unit); the prefix is empty when the card used none."""
    m = re.match(r"^\(?(?P<num>[^()]+?)\)?\s*(?P<pfx>[kMGmu\u00b5np])?"
                 r"(?P<unit>VA|var|V|A|W|\u03a9|S|F|H)?$", plain.strip())
    if not m or not m.group("pfx"):
        return plain.strip(), "", (m.group("unit") or "") if m else ""
    return m.group("num").strip(), m.group("pfx"), m.group("unit") or ""


def si_card(s):
    """{answer name: plain}, as the cards print them with SI prefixes on."""
    if "_sicard" not in s:
        digits, approx = shown_digits(s)
        shown = runner.app_display(s, digits=digits, approx=approx, si=True)
        s["_sicard"] = {k: v.get("plain", "") for k, v in shown.items()}
    return s["_sicard"]


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
    practice, ch, n, letter = fmt.parse_num(s["num"])
    return (ch, n, practice, letter)


def figname(num):
    return fmt.figname(num)


def base_num(num):
    return fmt.base_num(num)


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


DIGITS = 4      # Roberto, 13 Sep 2026: n = 3 or 4 unless the book asks for more


def digits_of(s):
    """The figures a problem's values are printed at: 4 unless the book
    prints more, in which case the book's own count (`digits=`)."""
    return int(s.get("digits", DIGITS))


def _integral(e):
    """True when an expression has no number in it but integers, so exact
    and approx print it alike."""
    e = sp.sympify(e)
    return not e.atoms(sp.Float) and all(a.is_Integer for a in e.atoms(sp.Number))


#: a number inside a rendered answer, scientific notation included
_NUMBER_IN = re.compile(r"\d+\.\d+(?:[eE][-+]?\d+)?|\d+(?:[eE][-+]?\d+)?")


def _canon(text):
    """A rendered answer with every number written one way, so that two
    printings of the same answer compare equal whatever notation they
    used -- `2.2e+6` and `2200000.0` are one number."""
    return _NUMBER_IN.sub(lambda m: repr(float(m.group(0))), text or "")


def _same_but_for_notation(a, b):
    """True when two renderings of an answer differ only in how their
    numbers are written, not in what they say."""
    return _canon(a) == _canon(b)


def _symbolic_text(plain):
    """True when a card's answer is an expression rather than a number.
    Unparseable counts as an expression: a number always parses."""
    try:
        return bool(sp.sympify(plain.replace("j", "*I")).free_symbols)
    except Exception:                                         # noqa: BLE001
        return True


def is_exact(s):
    """Rule 24, as rule 29 settled it (Roberto, 13 and 14 Sep 2026): True
    when the Rounding setting changes nothing the page shows, so the reader
    is told to set nothing and the entry says `rounding: exact`.

    Every answer the page prints is rendered by the real app twice, at the
    problem's digits and at exact, and compared with the numbers written
    one way -- so `1.0e+4` against `10000.0` is not a difference, while
    `1/(500*pi**2)` against `0.0002026` is. Cached on the spec, since it
    runs the app."""
    if "_exact" in s:
        return s["_exact"]
    n = digits_of(s)
    ok = n <= DIGITS
    # An AC entry's cards carry a polar form for every complex answer, and
    # a magnitude and an angle are decimal whatever the answer is, so
    # exact would print them to full precision (10.8, 14 Sep 2026).
    if s.get("domain") == "ac":
        ok = False
    if ok:
        at_n = runner.app_display(s, digits=n, approx=True)
        at_0 = runner.app_display(s, digits=0, approx=False)
        for k in s["expect"]:
            if k in s.get("hide", ()):
                continue
            if k.startswith("@"):
                pair = (runner.app_evaluate(s, k[1:], digits=n, approx=True),
                        runner.app_evaluate(s, k[1:], digits=0, approx=False))
            else:
                name = fmt.tool_name(k, s) or k
                if name not in at_n:
                    continue
                pair = (at_n[name]["plain"], at_0[name]["plain"])
            if not _same_but_for_notation(*pair):
                ok = False
                break
    if ok and s.get("evals"):
        for ev in s["evals"]:
            if "expr" not in ev:
                continue
            conds = ["%s = %s" % (k, v) for k, v in ev.get("at", {}).items()]
            if not _same_but_for_notation(
                    runner.app_evaluate(s, ev["expr"], conds, digits=n),
                    runner.app_evaluate(s, ev["expr"], conds, digits=0,
                                        approx=False)):
                ok = False
                break
    if ok and s.get("solveq"):
        for sq in s["solveq"]:
            at_n, _r = runner.app_solveq(s, sq, digits=n)
            at_0, _r = runner.app_solveq(s, sq, digits=0, approx=False)
            if set(at_n) != set(at_0) or any(
                    not _same_but_for_notation(at_n[k], at_0[k]) for k in at_n):
                ok = False
                break
    # a By-Hand Equations step's unknowns are printed too, and read the same
    # way: at the problem's digits against exact
    if ok and s.get("byhand"):
        bh = s["byhand"]
        _r, m_n = runner.app_byhand(s, bh, digits=n, approx=True)
        _r, m_0 = runner.app_byhand(s, bh, digits=0, approx=False)
        a_n = {a["name"]: str(a["value"]) for a in m_n["answers"]}
        a_0 = {a["name"]: str(a["value"]) for a in m_0["answers"]}
        if any(not _same_but_for_notation(a_n[k], a_0[k]) for k in bh["expect"]):
            ok = False
    s["_exact"] = ok
    return ok


def rounding_told(s):
    """What the reader is told to set: *approx to n digits* for n up to 4,
    *approx (full precision)* above it -- an n of 5 or 7 "comes across as
    clairvoyant" (Roberto, 13 Sep 2026); the page still prints the
    book's figures, and the reader will know why. Returns the .cir
    `rounding:` value."""
    if is_exact(s):
        return "exact"
    d = digits_of(s)
    return str(d) if d <= DIGITS else "approx"


def told_digits(s):
    """The Rounding the reader is told, as the pair `solve_ui` takes.
    *exact* is the app's default and is digits 0 with approx off."""
    told = rounding_told(s)
    if told == "exact":
        return 0, False
    if told == "approx":
        return 0, True
    return int(told), True


def shown_digits(s, part=None):
    """The Rounding a value is PRINTED at, as the pair `solve_ui` takes.

    The same as `told_digits` except under *approx (full precision)*,
    where the card prints every digit it has and the page prints the
    book's figures instead -- rule 19, Roberto, 13 Sep 2026: "show as many
    as the book; the reader will know why", restated 15 Sep 2026 when
    AS7's Example 5.1 printed -1.9999698252048888 for the book's
    -1.9999699. `part` is an Evaluate or Solve step that may carry its
    own `digits`, for an answer the book prints to a different precision
    from the rest of the problem (5.1's current, at 5)."""
    told = rounding_told(s)
    if told == "approx":
        return (part or {}).get("digits") or digits_of(s), True
    return told_digits(s)


#: a unit the card appends to a value's LaTeX, which the page adds itself
_CARD_UNIT = re.compile(r"\\,(?:\\mathrm\{[^}]*\}|\\Omega|var)\s*$")


def card_latex(s):
    """{answer name: LaTeX}, as the app's cards typeset them at the setting
    this entry tells the reader, with the card's unit stripped (the page
    appends its own). Cached on the spec, since it runs the app."""
    if "_cardtex" not in s:
        digits, approx = shown_digits(s)
        shown = runner.app_display(s, digits=digits, approx=approx)
        s["_cardtex"] = {k: _CARD_UNIT.sub("", v.get("latex", "")).strip()
                         for k, v in shown.items()}
    return s["_cardtex"]


def settings_line(s):
    kind, dom = s.get("kind", "circuit"), s.get("domain", "dc")
    bits = []
    if kind == "th":
        bits.append("Open {{card:Find equivalent}}, choose *Th\u00e9venin / Norton*, and "
                    "give the two terminals **%s** and **%s**" % (s["n1"], s["n2"]))
        if dom != "dc":
            bits.append("Set {{ui:Analysis}} to %s" % MENU[dom])
    elif kind == "er":
        bits.append("Open {{card:Find equivalent}}, choose *Resistance / impedance*, "
                    "and give the two terminals **%s** and **%s**" % (s["n1"], s["n2"]))
        if dom != "dc":
            bits.append("Set {{ui:Analysis}} to %s" % MENU[dom])
    elif kind == "port":
        bits.append("Open {{card:Find equivalent}}, choose *Two-port parameters*, kind "
                    "**%s**, with the ports at **%s** and **%s**"
                    % (s["ptype"], s["n1"], s["n2"]))
        if dom != "dc":
            bits.append("Set {{ui:Analysis}} to %s" % MENU[dom])
    else:
        bits.append("Set {{ui:Analysis}} to %s" % MENU[dom])
    if dom == "ac":
        w = s.get("omega")
        if w is None or isinstance(w, sp.Symbol):
            bits.append("Leave **omega** in the {{ui:\u03c9 \u2014 angular frequency}} box, "
                        "since nothing here depends on the frequency")
        else:
            bits.append("Put **%s** in the {{ui:\u03c9 \u2014 angular frequency}} box"
                        % fmt.plain_value(sp.sympify(w)))
    if s.get("rms"):
        bits.append("Tick {{ui:RMS phasors}} in {{card:Settings}}, since the book's source "
                    "is given in rms")
    if s.get("si"):
        # rule 32: the book prints these answers with SI prefixes
        bits.append("Tick {{ui:Use SI prefixes in answers}} in {{card:Settings}}")
    told = rounding_told(s)
    if told == "exact":
        pass                            # rule 24: the default shows what the page shows
    elif told == "approx":
        bits.append("Set {{ui:Rounding}} in {{card:Settings}} to *approx (full precision)*")
    else:
        bits.append("Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with "
                    "**n** = %d" % digits_of(s))
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
            # #443: the card's own typesetting, not a second rounding of our
            # own -- the two disagreed on every symbolic answer in the
            # chapter (`60` against `60.0`, `10000` against `1.0 \cdot 10^{4}`,
            # and a different term order in the transient answers).
            if k.startswith("@"):
                # not an answer of the run but an expression over them --
                # a transfer function, a gain -- which the reader reads in
                # the Evaluate card, so it is printed as that card prints it
                digits, approx = shown_digits(s)
                got = runner.app_evaluate_display(s, k[1:], digits=digits,
                                                  approx=approx)
                tex = _CARD_UNIT.sub("", got["latex"]).strip()
            else:
                tex = card_latex(s).get(fmt.tool_name(k, s) or k)
            assert tex, "%s: the card shows no %s" % (s["num"], k)
            body = "%s = %s" % (fmt.tex_name(k, s), tex)
            if unit:
                body += "\\," + (unit if unit == "\\Omega" else "\\mathrm{%s}" % unit)
            panels.append("::: result %s\n%s\n:::" % (lbl, body))
        else:
            shown = fmt.shown_name(k, s)
            if k.startswith("@"):
                s.setdefault("_evalkeys", {})[shown] = k
            value, pol = fmt.plain_value(got, digits_of(s)), polar_of(s, got)
            if s.get("si") and not k.startswith("@"):
                # rule 32: where the book prints a prefix the page prints the
                # card's own SI reading, and the angle form in the same unit
                num, pfx, _u = si_split(si_card(s).get(fmt.tool_name(k, s) or k, ""))
                if pfx:
                    value = tidy(num)
                    unit = ("\u00b5" if pfx == "u" else pfx) + UNIT_WORD.get(unit, unit)
                    pol = polar_of(s, sp.sympify(got) / SI_FACTOR[pfx])
            numeric.append((shown, value, unit, pol, s.get("booknames", {}).get(k)))
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
    p = S.polar(e, digits_of(s))
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
        if key is None or key in s.get("delivered", ()):
            # #434: a source's card shows its delivered power as `-pe`, so
            # that answer is read straight off the card, no Evaluate step
            direct.append(item)
            continue
        typed = key[1:].replace(" ", "")
        label = part_letters(s).get(name)
        if label:
            # rule 31: the step answers a lettered part, and says which
            lines.append("%s We type `%s` into {{card:Evaluate}}:" % (label, typed))
        else:
            lines.append(("Then we type `%s` into {{card:Evaluate}}:" if first else
                          "Likewise `%s`:") % typed)
        first = False
        lines.append("")
        lines.append("```field 9 Evaluate")
        lines.append(typed)
        lines.append("```")
        lines.append("")
        u = UNIT_WORD.get(unit, unit)
        aside = [x for x in (pol, book_aside(name, book)) if x]
        lines.append("It gives {{o:%s}}%s%s." % (val, (" " + u) if u else "",
                     (" (%s)" % ", ".join(aside)) if aside else ""))
        lines.append("")
    return direct, lines


def same_name(app, book):
    """True when the app's name and the book's symbol are one name in two
    typesettings -- `z11` and `z_{11}`, `vb` and `v_b`, `t` and `t` -- so
    naming the book's beside the value would be redundant (rule 22)."""
    if not app or not book:
        return False
    strip = lambda x: re.sub(r"[\s_{}$\\]", "", x).lower()
    return strip(app) == strip(book)


def book_aside(app, book):
    """The "the book's $…$" aside, or nothing when the names agree."""
    return ("the book's $%s$" % book) if book and not same_name(app, book) else ""


def part_label(s, letter):
    """A part's letter in bold, in the book's own style: *(a)* where the
    ask writes (a), *a)* where it writes a) (rule 31)."""
    # the first letter decides: NR12's 5.1 writes a) and then "Repeat (a)"
    first = re.search(r"(?:^|[\s:])(\()?[a-h]\)(?=\s)", s["ask"])
    style = "(%s)" if first and first.group(1) else "%s)"
    return "**" + style % letter + "**"


def part_letters(s):
    """Shown answer name -> the bold letter of the part it answers."""
    return {fmt.shown_name(k, s): part_label(s, v) for k, v in s.get("letters", {}).items()}


def check_letters(s, text):
    """Rule 31's guard: an ask with two or more lettered parts has every
    one of them labelled on the page, in bold, where it is answered."""
    asked = re.findall(r"(?:^|[\s:(])\(?([a-h])\)(?=\s)", s["ask"])
    if len(set(asked)) < 2:
        return
    missing = [a for a in asked if part_label(s, a) not in text]
    assert not missing, "%s: the ask letters %s but the page never labels %s" % (
        s["num"], asked, missing)


def numeric_sentence(numeric, letters=None):
    """The numeric answers, as one plain sentence.

    It used to end "-- the same answers the book prints", forty-three times.
    The claim is made once instead, in the chapter's *How to read an entry*,
    and an entry whose answer needs a word about it (a sign, a rounding)
    says so in its own paragraph."""
    if not numeric:
        return ""
    return "Symbulator returns " + numeric_body(numeric, letters) + "."


def grouped_sentences(s, direct):
    """The returns sentence, or several of them: a spec's `groups` splits
    the plain results into sentences of their own, each with its own lead
    -- *For part (a), the three impedances' cards read ...* -- so a
    question with lettered parts answers each in turn (10.8, Roberto,
    14 Sep 2026). An answer in no group keeps the default *Symbulator
    returns ...* sentence, after the groups."""
    out, taken = [], set()
    for lead, keys in s.get("groups", []):
        names = [fmt.shown_name(k, s) for k in keys]
        items = [it for it in direct if it[0] in names]
        missing = set(names) - {it[0] for it in items}
        assert not missing, "group %r names answers the page does not show: %s" % (
            lead, sorted(missing))
        taken.update(names)
        if items:
            out.append(lead + " " + numeric_body(items) + ".")
    for ev in s.get("evals", []):
        if "keys" in ev:
            taken.update(fmt.shown_name(k, s) for k in ev["keys"])
    rest = [it for it in direct if it[0] not in taken]
    if rest:
        out.append(numeric_sentence(rest, part_letters(s)))
    return out


def numeric_body(numeric, letters=None):
    """`name` = value unit (asides), joined with commas and a final *and*.
    An answer to a lettered part carries its letter in front, and the
    lettered answers come first, in the question's order (rule 31)."""
    letters = letters or {}
    numeric = sorted(numeric, key=lambda it: (it[0] not in letters, letters.get(it[0], "")))
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
        aside = [x for x in (pol, book_aside(name, book)) if x]
        if aside:
            txt += " (%s)" % ", ".join(aside)
        if name in letters:
            txt = letters[name] + " " + txt
        parts.append(txt)
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


def render(s, vals):
    num = s["num"]
    L = ["::: problem %s" % titles.short_title(num), ""]
    # The book's own title ("Using Voltage Division and Current Division to
    # Solve a Circuit") is not shown: it names the book's method, which is
    # not how the reader will solve the problem (Roberto, 12 Sep 2026).
    L.append(polish(s["ask"]))
    L.append("")
    # A spec with `nofig` shows no figure: the book prints none for the
    # circuit as stated (9.15 has only its frequency-domain equivalent),
    # and the words are enough (Roberto, 13 Sep 2026).
    if not s.get("nofig"):
        L.append("::: figure assets/circuit/%s" % figname(num))
        L.append("%s \u2014 the circuit for %s %s"
                 % (book.CREDIT, fmt.num_label(num), base_num(num)))
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
    # Rule 16 (Roberto, 13 Sep 2026): a consideration about how to read the
    # results -- a sign convention, a note the solver will print, which
    # answer is which -- comes after the sentence that runs the simulation,
    # not in the paragraph that describes the circuit.
    if s.get("interpret"):
        L.append(polish(s["interpret"]))
        L.append("")
    panels, numeric = answer_blocks(s, vals)
    for p in panels:
        L.append(p)
        L.append("")
    # a panel's answer is named against the book's symbol in a sentence
    # under the panels, the way a numeric answer is named beside its value
    named = [(k, s["booknames"][k]) for k in s["expect"]
             if k in s.get("booknames", {}) and k not in s.get("hide", ())
             and not same_name(fmt.shown_name(k, s), s["booknames"][k])
             and sp.sympify(vals.get(k, 0) if not k.startswith("@") else 0).free_symbols]
    lettered = [k for k in s["expect"] if k in s.get("letters", {})
                and k not in s.get("hide", ())
                and (k.startswith("@") or sp.sympify(vals.get(k, 0)).free_symbols)]
    if panels and lettered:
        # rule 31: a panel that answers a lettered part says which, in the
        # question's order -- "**a)** is `i_l` and **b)** is `i_r3` (the book's $i_o$)"
        bits = []
        for k in sorted(lettered, key=lambda k: s["letters"][k]):
            name = fmt.shown_name(k, s)
            b = s.get("booknames", {}).get(k)
            what = ("the %s above" % fmt.label_for(k, s["desc"], s)) if k.startswith("@") else "`%s`" % name
            if b and not k.startswith("@") and not same_name(name, b):
                what += " (the book's $%s$)" % b
            bits.append("%s is %s" % (part_label(s, s["letters"][k]), what))
        L.append((bits[0] if len(bits) == 1 else ", ".join(bits[:-1]) + " and " + bits[-1]) + ".")
        L.append("")
        named = [(k, b) for k, b in named if k not in lettered]
    if panels and named:
        bits = ["`%s` is the book's $%s$" % (fmt.shown_name(k, s), b)
                for k, b in named]
        L.append(("Here " if len(bits) > 1 else "") + (
            bits[0] if len(bits) == 1 else ", ".join(bits[:-1]) + " and " + bits[-1]) + ".")
        L.append("")
    direct, eval_lines = evaluated_blocks(s, numeric)
    for sent in grouped_sentences(s, direct):
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
        if "card" in ev:
            # A row read straight off an element's card -- a source's power
            # factor (AS7's 11.14, Roberto, 15 Sep 2026: the card already
            # shows it, so no Mini-Tools step). `card` is (row, element), the
            # value comes from the real app's card and is checked against the
            # spec's `expect`, so the page cannot print what the card does not.
            row, element = ev["card"]
            digits, approx = shown_digits(s)
            plain = runner.app_display(s, digits=digits, approx=approx).get(
                "%s_%s" % (row, element), {}).get("plain", "")
            assert plain == ev["expect"], "%s: card row %s of %s reads %r, not %r" % (
                s["num"], row, element, plain, ev["expect"])
            L.append(polish(ev["text"]) + " {{o:%s}}." % plain)
            L.append("")
            continue
        if "keys" in ev:
            # A lettered part answered straight off the run, placed here
            # so the parts keep the question's order among the Evaluate
            # steps (11.1, Roberto, 14 Sep 2026: each question answered
            # separately, showing what is evaluated and what is returned).
            names = [fmt.shown_name(k, s) for k in ev["keys"]]
            items = [it for it in direct if it[0] in names]
            assert len(items) == len(names), (s["num"], ev["keys"])
            # no keys: a part answered in words alone, kept in its place
            # among the others (19.17's output impedance, the next entry's)
            L.append(polish(ev["text"]) + (" " + numeric_body(items) + "." if items else ""))
            L.append("")
            continue
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
        digits, approx = shown_digits(s, ev)
        card = runner.app_evaluate_display(s, ev["expr"], conds, digits=digits,
                                           approx=approx, si=bool(s.get("si")))
        got = card["plain"]
        pfx = ""
        if s.get("si"):
            # rule 32: the card prints `199.99799 u`; the number is read in
            # its prefix, and the prefix joins the unit
            num_si, pfx, _u = si_split(got)
            if pfx:
                got = num_si
        # `number_of` reads a LEADING number and cannot be asked about an
        # expression: on "(50.0 - 2200000.0*t)*exp(...)" it takes "(50.0"
        # and raises. So the shape of the answer is settled first, and a
        # symbolic one is compared whole.
        symbolic = _symbolic_text(got)
        num, val = ("", None) if symbolic else runner.number_of(got)
        unit = UNIT_WORD.get(ev.get("unit", ""), ev.get("unit", ""))
        if pfx:
            val = val * SI_FACTOR[pfx]
            unit = ("\u00b5" if pfx == "u" else pfx) + unit
        if ev.get("expect") is not None:
            want = ev["expect"]
            assert runner.close(got if symbolic else val, want, 0.006), \
                "Evaluate %s at %s: got %s, book says %s" % (ev["expr"], ev.get("at"), got, want)
        if symbolic:
            # An expression, shown the way every other expression answer on
            # the page is shown: a result panel carrying the card's own
            # typesetting (#443).
            tex = _CARD_UNIT.sub("", card["latex"]).strip()
            body = "%s = %s" % (ev["texname"], tex)
            if ev.get("unit"):
                u = ev["unit"]
                body += "\\," + (u if u == "\\Omega" else "\\mathrm{%s}" % u)
            L.append("It gives:")
            L.append("")
            L.append("::: result %s" % ev["label"])
            L.append(body)
            L.append(":::")
            L.append("")
            continue
        # an AC answer also reads as an amplitude and an angle, from the
        # exact value rather than the printed one, so the last digit is
        # the book's (199.58, not the 199.57 a rounded rectangular gives)
        aside = []
        if s.get("domain") == "ac" and not ev.get("at"):
            try:
                pol = polar_of(s, sp.sympify(ev["expr"], locals=dict(vals)))
            except Exception:
                pol = ""
            if pol:
                aside.append(pol)
        if ev.get("book") and not same_name(ev["expr"], ev["book"]):
            aside.append("the book's $%s$" % ev["book"])
        L.append("It gives {{o:%s}}%s%s." % (tidy(num), (" " + unit) if unit else "",
                 (" (%s)" % ", ".join(aside)) if aside else ""))
        L.append("")
    # A By-Hand Equations step: the card's system, as it writes it, and its
    # unknowns read against the book's names. `book` maps an unknown to the
    # book's symbol, `opposite` lists the ones that run the other way.
    bh = s.get("byhand")
    if bh:
        digits, approx = told_digits(s)
        _r, m = runner.app_byhand(s, bh, digits=digits or 4, approx=approx)
        label = {"mesh": "Mesh analysis", "nodal": "Nodal analysis"}[bh["method"]]
        if m.get("technique"):
            label += {"mesh": " (with supermeshes)", "nodal": " (with supernodes)"}[bh["method"]]
        L.append(polish(bh["text"]))
        L.append("")
        press = "Press {{btn:Write the equations}} in the {{card:By-Hand Equations}} card"
        if _r.get("both"):
            press += ", and choose *%s* in its {{ui:Method}} menu" % label
        L.append(press + ". It writes the system:")
        L.append("")
        L.append("$$")
        L.append("\\begin{aligned}")
        L.append(" \\\\\n".join(row["latex"].replace("=", "&=", 1) for row in m["rows"]))
        L.append("\\end{aligned}")
        L.append("$$")
        L.append("")
        items = []
        answers = {a["name"]: a for a in m["answers"]}
        for k in bh["expect"]:
            val = answers[k]["value"]
            txt = "`%s` = {{o:%s}}%s" % (k, tidy(val), (" " + bh["unit"]) if bh.get("unit") else "")
            book_sym = bh.get("book", {}).get(k)
            if book_sym:
                txt += (" (the opposite of the book's $%s$)" if k in bh.get("opposite", ())
                        else " (the book's $%s$)") % book_sym
            items.append(txt)
        L.append("The card returns " + (items[0] if len(items) == 1 else
                 ", ".join(items[:-1]) + " and " + items[-1]) + ".")
        L.append("")
    # A Mini-Tools step (#445): the tool chosen, the value typed into its
    # box, and what the card answers, read from the real app's
    # mini_tool_ui on the values the page holds. `rows` names what to
    # quote: [(row key, the words before it)], as the card prints them.
    for mt in s.get("minitool", []):
        L.append(polish(mt["text"]))
        L.append("")
        L.append("```field 9 Value")
        L.extend(mt["args"])
        L.append("```")
        L.append("")
        L.append("Press {{btn:Run}}.")
        L.append("")
        digits, approx = told_digits(s)
        got = runner.app_minitool(s, mt, digits=digits or 4, approx=True)
        # a one-value tool (pf, aa) replies with `plain` alone, read as row "value"
        rows = {r["key"]: r["plain"] for r in
                (got.get("rows") or [{"key": "value", "plain": got["plain"]}])}
        for k, want in mt["expect"].items():
            assert rows.get(k) == want, "%s: %s gives %s %r, the spec says %r" % (
                s["num"], mt["tool"], k, rows.get(k), want)
        bits = []
        for k, words in mt["say"]:
            values = [v.strip() for v in rows[k].split(",")]
            shown = ["{{o:%s}}" % v for v in values]
            bits.append("%s %s" % (words, shown[0] if len(shown) == 1 else
                                   ", ".join(shown[:-1]) + " and " + shown[-1]))
        L.append("The card returns " + (bits[0] if len(bits) == 1 else
                 ", ".join(bits[:-1]) + ", and " + bits[-1]) + ".")
        L.append("")
    # Solve card runs (Roberto, 13 Sep 2026: "my approach with Solve, which
    # is more representative of the exploratory way a student would
    # follow"). Each is shown with its own boxes and its own answer, read
    # from the real app's solveq_ui on the values the page holds. The
    # first run's fields travel in the problem's head entry; a later run
    # is an entry of its own, linked beside its boxes.
    if s.get("solveq"):
        values = runner.app_values(s, digits=told_digits(s)[0],
                                   approx=told_digits(s)[1])
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
                # #435: the tick is on by default in DC and TR and off in AC
                # and FD, so the line names it only when the run wants it
                # the other way.
                default_on = s.get("domain", "dc") in ("dc", "tr")
                want = sq.get("real_only", True)
                if want == default_on:
                    L.append("Press {{btn:Solve equations}}.")
                elif want:
                    L.append("Tick {{ui:real solutions only}} and press {{btn:Solve equations}}.")
                else:
                    L.append("Untick {{ui:real solutions only}} and press {{btn:Solve equations}}.")
            L.append("")
            got, _r = runner.app_solveq(s, sq, values, digits=shown_digits(s, sq)[0],
                                        approx=shown_digits(s, sq)[1])
            sols = _r.get("solutions") or []
            units = sq.get("unit", "")

            def one(k, plain):
                u = units.get(k, "") if isinstance(units, dict) else units
                u = UNIT_WORD.get(u, u)
                assert not _symbolic_text(plain), (
                    "%s: the Solve card answers %s with an expression, %r, "
                    "which this line would print as its leading number"
                    % (s["num"], k, plain))
                shown = tidy(runner.number_of(plain)[0])
                txt = "`%s` = {{o:%s}}%s" % (k, shown, (" " + u) if u else "")
                if sq.get("book", {}).get(k) and not same_name(k, sq["book"][k]):
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
    check_letters(s, "\n".join(L))
    L.append(":::")
    L.append(":::")
    return "\n".join(L)


def main_tag(s):
    """The parenthetical of the main run's entry: (DC), (Th\u00e9venin), (TR, Expert Mode)."""
    if s.get("tag"):
        return s["tag"]              # a spec that names its own run (10.6)
    dom, kind = s.get("domain", "dc"), s.get("kind", "circuit")
    tag = {"dc": "DC", "ac": "AC", "tr": "TR", "fd": "FD"}[dom]
    if kind == "th":
        tag = "Th\u00e9venin"
    if kind == "er":
        tag = "equivalent"
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
                shownames=pre.get("shownames", {}), units=pre.get("units", {}),
                digits=digits_of(s),
                # a first run may be AC at a frequency of its own -- one
                # of a superposition's runs, AS7's Example 10.6
                omega=pre.get("omega"), rms=pre.get("rms", False))


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
    if kind in ("th", "er"):
        L += ["tool: %s" % kind, "n1: %s" % s["n1"], "n2: %s" % s["n2"]]
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
        # a problem whose first runs are not "before the switch" says what
        # its own last run is (a superposition's third source, 10.6)
        L.append("note: %s" % s.get("cir_note",
                 "This is the circuit after the switch has moved; its initial "
                 "condition comes from the entry before it."))
    if not s.get("nofig"):
        L.append("image: https://learn.symbulator.com/assets/circuit/%s" % figname(num))
    L.append("rounding: %s" % rounding_told(s))
    L.append("si: %s" % ("yes" if s.get("si") else "no"))
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
    if not s.get("nofig"):
        L.append("image: https://learn.symbulator.com/assets/circuit/%s" % figname(s["num"]))
    L.append("rounding: %s" % rounding_told(s))
    L.append("si: %s" % ("yes" if s.get("si") else "no"))
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
    if pre.get("domain") == "ac":
        w = pre.get("omega")
        L.append("omega: %s" % ("omega" if (w is None or isinstance(w, sp.Symbol))
                                else fmt.plain_value(sp.sympify(w))))
    L.append("note: %s" % ask)
    L.append("note: %s" % pre["note"])
    if not s.get("nofig"):
        L.append("image: https://learn.symbulator.com/assets/circuit/%s" % figname(s["num"]))
    # the first run is classified on its own, as its page line is (rule 24)
    L.append("rounding: %s" % rounding_told(pre_spec(s, pre)))
    L.append("si: no")
    L.append("units: yes")
    if pre.get("domain") == "ac":
        L.append("rms: %s" % ("yes" if pre.get("rms") else "no"))
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
           "title: %s" % book.CIR_TITLE, ""]
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
    io.open(os.path.join(EXAMPLES, book.CIR_FILE), "w",
            encoding="utf-8", newline="\n").write("\n".join(cir).rstrip() + "\n")
    body = []
    for grp in ORDER:
        gid, gname = GROUP[grp]
        body.append("## %s \u2014 %s {#%s-%s}" % (gname, grp.upper(), book.ANCHOR, gid))
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
    words = {n: w for n, w in enumerate(
        "Zero One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve "
        "Thirteen Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen Twenty "
        "Twenty-one Twenty-two Twenty-three Twenty-four Twenty-five".split())}
    for g in ORDER:
        n = sum(1 for s in rows if s.get("domain", "dc") == g)
        intro = io.open(os.path.join(_HERE, "intro_%s.md" % g),
                        encoding="utf-8").read().strip()
        assert intro.startswith(words.get(n, "%d " % n)), \
            "the %s intro says a different count from the %d specs it introduces" % (g, n)
        text = text.replace("@@INTRO_%s@@" % g.upper(), intro)
    text = re.sub(r"\n{4,}", "\n\n\n", text).rstrip() + "\n"
    out = os.path.join(DOCS, "src", book.CHAPTER)
    io.open(out, "w", encoding="utf-8", newline="\n").write(text)
    counts = {g: sum(1 for s in rows if s.get("domain", "dc") == g) for g in ORDER}
    print("entries:", len(rows), "| by mode:", counts)
    print("chapter ->", out, "|", len(text.splitlines()), "lines")


main()
