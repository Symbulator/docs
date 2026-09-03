"""Render the monograph's exemplar circuits with the v9 schematic
engine, and convert each SVG to PDF for inclusion in the appendix.

The circuits are **not** written out here. They are read from the app's
own example book, `repos/server/examples/The_Monograph.cir`, which is
where the reader meets them: the same seven entries, drawn by the same
drawer, so the appendix and the app cannot show different circuits or
spell the same circuit two ways. They did briefly -- this file kept its
own copy, and when Roberto restated the showcase's controls in the book
on 1 Sep 2026 (`0.2vr7` rather than `0.2*v_r7`) the copy here stayed as
it was. A second copy of anything is a second thing to keep right.

    py render_exemplars.py

Needs the app tree beside this one (both paths below), plus svglib and
reportlab, neither of which the solver depends on.
"""
import os
import re
import sys

SOLVER = r"C:\Users\perez\Claude Code\Application\v9\repos\solver"
SERVER = r"C:\Users\perez\Claude Code\Application\v9\repos\server"
for path in (SOLVER, SERVER):
    if not os.path.isdir(path):
        raise SystemExit(
            "no app tree at %s -- this script renders the appendix's\n"
            "circuits with the live schematic engine and reads them from\n"
            "the app's example book, so both have to be present." % path)
    sys.path.insert(0, path)

from symbulator.schematic import to_svg          # noqa: E402
from circuitbook import parse_book               # noqa: E402
from svglib.svglib import svg2rlg                # noqa: E402
from reportlab.graphics import renderPDF         # noqa: E402


def _escape(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;"))

OUT = r"C:\Users\perez\Claude Code\Documentation\paper\figures"
BOOK = os.path.join(SERVER, "examples", "The_Monograph.cir")

# Figure name -> the entry in The_Monograph.cir it is drawn from. The
# figure names are what `symbulator_monograph.tex` includes, so they
# stay put; the entry names are the book's own, and a rename on either
# side fails this script loudly rather than quietly rendering the wrong
# circuit.
EXEMPLARS = {
    # 5.1 The two-stage amplifier of 1999 (thesis Problem 87)
    "ex_amplifier": "The two-stage amplifier of 1999",
    # 5.2 The 2013 showcase
    "ex_showcase2013": "One of each: the 2013 showcase",
    # 5.3 Boulet, t<0 and t>0
    "ex_boulet_before": "Prof. Boulet's switching transient (DC, t < 0)",
    "ex_boulet_after": "Prof. Boulet's switching transient (TR, t > 0)",
    # 5.4 Three-phase wye-delta with line impedances
    "ex_threephase": "Three-phase wye-delta with line impedances",
    # 5.5 The ideal transformer, symbolically
    "ex_transformer": "The ideal transformer, symbolically",
    # 5.6 Coupled coils with initial conditions
    "ex_coupledcoils": "Coupled coils with initial conditions",
    # 5.7 Two op-amps, all symbols
    "ex_twoopamps": "Two op-amps, all symbols",
}


def descriptions():
    """Figure name -> circuit description, straight out of the book."""
    with open(BOOK, encoding="utf-8") as f:
        circuits, warnings, _title = parse_book(f.read())
    if warnings:
        raise SystemExit("the example book does not parse cleanly: %s"
                         % "; ".join(warnings))
    by_name = {c["name"]: c["desc"] for c in circuits}
    out = {}
    for figure, entry in EXEMPLARS.items():
        if entry not in by_name:
            raise SystemExit(
                "no entry %r in %s -- it was renamed or removed, and the\n"
                "appendix figure %s cannot be drawn without it."
                % (entry, BOOK, figure))
        out[figure] = by_name[entry].replace("\n", ":")
    return out


# The label font, and the two runs a label can be built from. `.sub`
# and the sloped quantity letters arrived with #212 and #213; svglib
# reads neither a <style> block nor a class, so both have to become
# attributes on the tspan before it will see them.
LABEL_PT = 13.0
SUB_SCALE = 0.72


# The label face. Helvetica is a Type 1 font in WinAnsi: it has no
# omega, no pi and no angle sign, and reportlab draws what it cannot
# encode as nothing at all. The appendix had been printing resistances
# as "10 |" since the figures were first generated (28 Aug 2026) -- not
# a styling blemish but a wrong unit, on every exemplar with a resistor
# in it, and invisible in the SVG, where all four characters were
# correct the whole time. Found on 1 Sep 2026 by looking at a rendered
# page. (Adobe's Symbol font has all three glyphs and is a standard
# face, but svglib will not honour a per-tspan `font-family` switch, so
# splitting the runs out into Symbol drew blanks instead of bars: no
# better.) A real Unicode TTF, embedded, is the fix.
DEJAVU = "DejaVuSans"
# style -> the face name svglib registered it under, filled in by
# `register_fonts` and read by everything that measures or draws text.
FACES = {}
_FONT_DIRS = []
try:                                            # matplotlib ships it
    import matplotlib
    _FONT_DIRS.append(os.path.join(os.path.dirname(matplotlib.__file__),
                                   "mpl-data", "fonts", "ttf"))
except ImportError:
    pass
_FONT_DIRS += [r"C:\Windows\Fonts",
               "/usr/share/fonts/truetype/dejavu",
               "/usr/local/share/fonts"]


def register_fonts():
    """Embed DejaVu Sans, upright and oblique, for the labels.

    Through `svglib.register_font`, not reportlab's `registerFont`.
    Registering with reportlab alone does nothing here: svglib keeps its
    own map from an SVG `font-family` to a reportlab face, and a family
    it does not know falls back to Helvetica -- silently, and with the
    omegas still missing, which is what the first attempt at this fix
    produced. The style is registered as part of the mapping too, so a
    `font-style="italic"` run picks the oblique on its own.

    Nothing else in this tree needs a font registered, so a missing
    face is a hard stop with the reason rather than a fall back to
    Helvetica -- which is exactly how the missing omegas shipped."""
    from svglib.svglib import register_font
    faces = [("normal", "DejaVuSans.ttf"),
             ("italic", "DejaVuSans-Oblique.ttf")]
    for style, filename in faces:
        for d in _FONT_DIRS:
            path = os.path.join(d, filename)
            if os.path.exists(path):
                # svglib names the face itself -- the oblique comes back
                # as `DejaVuSans-Italic`, not the file's own name -- and
                # that is the name reportlab knows it by, so it is the
                # one to measure with and the one to write into the
                # markup. Taking the returned name rather than guessing
                # it is the whole point of reading the return value.
                FACES[style] = register_font(
                    DEJAVU, font_path=path, style=style)[0]
                break
        else:
            raise SystemExit(
                "cannot find %s. The appendix's labels carry omega, pi "
                "and the angle sign, which the built-in Type 1 faces "
                "cannot encode; DejaVu Sans can. It ships with "
                "matplotlib, or install it and put it on one of: %s"
                % (filename, ", ".join(_FONT_DIRS)))
    return FACES


_TEXT_RE = re.compile(
    r'<text class="lbl" x="(?P<x>[-\d.]+)" y="(?P<y>[-\d.]+)" '
    r'text-anchor="(?P<anchor>\w+)">(?P<inner>.*?)</text>')
_TSPAN_RE = re.compile(
    r'<tspan(?P<attrs>[^>]*)>(?P<txt>[^<]*)</tspan>')


def _runs(inner):
    """[(text, font, size, dy)] for one label, dy relative to the run
    before it -- which is how the drawer writes them (`_Canvas.runs`)."""
    out = []
    for m in _TSPAN_RE.finditer(inner):
        attrs, txt = m.group("attrs"), m.group("txt")
        size = LABEL_PT * SUB_SCALE if 'class="sub"' in attrs else LABEL_PT
        font = FACES["italic" if "italic" in attrs else "normal"]
        dy = re.search(r'dy="([-\d.]+)"', attrs)
        out.append((txt, font, size, float(dy.group(1)) if dy else 0.0))
    return out


def _unescape(t):
    return (t.replace("&lt;", "<").replace("&gt;", ">")
             .replace("&quot;", '"').replace("&amp;", "&"))


def _lay_out_labels(svg: str) -> str:
    """Turn every label into one `<text>` per run, placed absolutely.

    svglib lays out a multi-run `<text>` itself, and it gets it wrong
    here: with DejaVu embedded, `J` and its subscript `D1` came out on
    top of each other while `R` and its `5` were fine -- the advance it
    used was not the advance it drew with. Rather than find out which
    metric it was reading, the arithmetic is done here, against the
    same reportlab faces the page is drawn in, and every run is handed
    to svglib already positioned with `text-anchor="start"`.

    The label's own anchor is honoured by measuring the whole label
    first; `dy` accumulates, because each run's shift is relative to
    the one before it."""
    from reportlab.pdfbase.pdfmetrics import stringWidth

    def place(m):
        x, y = float(m.group("x")), float(m.group("y"))
        runs = _runs(m.group("inner"))
        if not runs:
            return ""
        texts = [_unescape(t) for t, _f, _s, _dy in runs]
        widths = [stringWidth(t, f, s)
                  for t, (_txt, f, s, _dy) in zip(texts, runs)]
        # What is drawn is the run without its outer spaces, because
        # the renderer strips those anyway -- svglib's whitespace
        # handling is Unicode-aware, so a no-break space does not
        # survive either. The spaces still count toward the cursor, and
        # a run's *leading* space is added to its own x, so ` = ` and
        # `  (couples ` land exactly where their width says: the
        # caption read `M=  1H(couples  L1and  L2)` until they did.
        leads = [stringWidth(t[:len(t) - len(t.lstrip())], f, s)
                 for t, (_txt, f, s, _dy) in zip(texts, runs)]
        total = sum(widths)
        if m.group("anchor") == "middle":
            cursor = x - total / 2.0
        elif m.group("anchor") == "end":
            cursor = x - total
        else:
            cursor = x
        out, shift = [], 0.0
        for (_txt, font, size, dy), txt, w, lead in zip(
                runs, texts, widths, leads):
            shift += dy
            drawn = txt.strip()
            if drawn:
                out.append(
                    '<text x="%.3f" y="%.3f" font-family="%s" '
                    'font-size="%g" fill="#000000" stroke="none" '
                    'text-anchor="start">%s</text>'
                    % (cursor + lead, y + shift, font, size, _escape(drawn)))
            cursor += w
        return "".join(out)

    return _TEXT_RE.sub(place, svg)


def flatten_for_svglib(svg: str) -> str:
    """svglib ignores inheritable attributes on the root <svg> and the
    <style> block, so push them inline: wrap the content in a <g>
    carrying the stroke defaults and resolve currentColor to black.

    The labels do not survive that on their own -- the stylesheet is
    what made a subscript small, and svglib's own run layout puts the
    subscript in the wrong place even once it is -- so they are laid
    out here instead, absolutely, by `_lay_out_labels`."""
    svg = svg.replace('stroke="currentColor"', 'stroke="#000000"')
    svg = re.sub(r"<style>.*?</style>", "", svg, flags=re.S)
    svg = _lay_out_labels(svg)
    m = re.match(r"(<svg[^>]*>)(.*)(</svg>)", svg, flags=re.S)
    head, body, tail = m.groups()
    wrap = ('<g fill="none" stroke="#000000" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round">')
    return head + wrap + body + "</g>" + tail


def main():
    register_fonts()
    os.makedirs(OUT, exist_ok=True)
    for name, desc in descriptions().items():
        svg = to_svg(desc)
        svg_path = os.path.join(OUT, name + ".svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg)
        flat_path = os.path.join(OUT, name + "_flat.svg")
        with open(flat_path, "w", encoding="utf-8") as f:
            f.write(flatten_for_svglib(svg))
        drawing = svg2rlg(flat_path)
        pdf_path = os.path.join(OUT, name + ".pdf")
        renderPDF.drawToFile(drawing, pdf_path)
        os.remove(flat_path)
        print("%s: svg %d chars -> %d B pdf"
              % (name, len(svg), os.path.getsize(pdf_path)))


if __name__ == "__main__":
    main()
