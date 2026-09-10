"""Word scan beside v9 rendering, per problem.

Two independent things are checked at once. If the engine's drawing of
the converted netlist shows the same circuit as the 2001 scan, then the
netlist conversion is right *and* the scan is paired to the right
problem. A pairing error shows up as two obviously different circuits.
"""
import base64
import html
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pair_figures import all_chapters, pair                # noqa: E402
from parse_book import parse                               # noqa: E402
from to_v9 import convert                                  # noqa: E402

OUT = "compare_sheet.html"


def uri(path):
    with open(path, "rb") as fh:
        return "data:image/png;base64," + base64.b64encode(fh.read()).decode()


def main():
    figs = {}
    for stem in all_chapters():
        _p, problems, _l = pair(stem)
        for num, cap, pic in problems:
            if pic is not None:
                figs.setdefault(num, []).append((cap, pic))

    rows = []
    for p in parse():
        num = p["num"]
        v9 = ""
        if p["netlists"]:
            tool, desc, rest = p["netlists"][0]
            v9 = convert(tool, desc, rest, stores=p.get('stores'))["desc"]

        left = ""
        for cap, pic in figs.get(num, []):
            left += (f'<figure><img src="{uri(pic["file"])}">'
                     f'<figcaption>2001 &middot; Fig {html.escape(cap["fig"])}'
                     f'</figcaption></figure>')
        if not left:
            left = '<div class="miss">no 2001 figure paired</div>'

        svg_path = os.path.join("v9_svg", f"p{num}.svg")
        if os.path.exists(svg_path):
            svg = io.open(svg_path, encoding="utf-8").read()
            right = f'<figure><div class="svg">{svg}</div>' \
                    f'<figcaption>version 9 engine</figcaption></figure>'
        else:
            right = '<div class="miss">not drawn</div>'

        rows.append(
            f'<section><h2>Problem {num}</h2>'
            f'<div class="a">{left}</div><div class="b">{right}</div>'
            f'<pre>{html.escape(v9) or "(no netlist)"}</pre></section>')

    doc = f"""<!doctype html><meta charset="utf-8">
<title>2001 scan vs version 9 drawing</title>
<style>
 body{{font:14px system-ui;margin:0;padding:20px;background:#f6f7f9;color:#111}}
 section{{background:#fff;border:1px solid #dcdfe4;border-radius:8px;
   padding:12px 14px;margin:0 0 12px;display:grid;
   grid-template-columns:1fr 1fr 260px;gap:10px 16px;align-items:start}}
 h2{{grid-column:1/4;margin:0 0 4px;font-size:15px}}
 img{{max-width:100%;border:1px solid #ccc;background:#fff}}
 .svg svg{{max-width:100%;height:auto}}
 figcaption{{font-size:11px;color:#666}}
 pre{{margin:0;background:#f2f3f5;padding:8px;border-radius:6px;
   font:11px ui-monospace,monospace;white-space:pre-wrap}}
 .miss{{color:#b00020;font-weight:600;font-size:12px}}
</style>
<h1>2001 scan vs version 9 drawing</h1>
{''.join(rows)}"""
    io.open(OUT, "w", encoding="utf-8").write(doc)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
