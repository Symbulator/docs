"""Build a contact sheet: every problem, its paired figure, its caption
and its v9 netlist, side by side, so a wrong pairing is visible at a
glance instead of being trusted."""
import base64
import html
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pair_figures import all_chapters, pair                # noqa: E402
from parse_book import parse                               # noqa: E402
from to_v9 import convert                                  # noqa: E402

OUT = "contact_sheet.html"


def data_uri(path):
    with open(path, "rb") as fh:
        return "data:image/png;base64," + base64.b64encode(fh.read()).decode()


def main():
    # problem number -> (caption, picture)
    figs = {}
    for stem in all_chapters():
        _pairs, problems, _left = pair(stem)
        for num, cap, pic in problems:
            figs.setdefault(num, []).append((stem, cap, pic))

    probs = {p["num"]: p for p in parse()}
    rows = []
    for num in sorted(probs):
        p = probs[num]
        entries = figs.get(num, [])
        v9 = ""
        if p["netlists"]:
            tool, desc, rest = p["netlists"][0]
            c = convert(tool, desc, rest, stores=p.get('stores'))
            v9 = c["desc"]
        imgs = ""
        for _stem, cap, pic in entries:
            if pic is None:
                imgs += '<div class="miss">caption with no picture</div>'
                continue
            imgs += (f'<figure><img src="{data_uri(pic["file"])}">'
                     f'<figcaption>Fig {html.escape(cap["fig"])} &middot; '
                     f'{html.escape(os.path.basename(pic["file"]))} &middot; '
                     f'{pic["size"][0]}&times;{pic["size"][1]}</figcaption>'
                     f'</figure>')
        if not entries:
            imgs = '<div class="miss">no figure paired</div>'
        rows.append(
            f'<section><h2>Problem {num}</h2>'
            f'<p class="stmt">{html.escape(p["statement"])[:400]}</p>'
            f'<div class="figs">{imgs}</div>'
            f'<pre>{html.escape(v9) or "(no netlist)"}</pre></section>')

    doc = f"""<!doctype html><meta charset="utf-8">
<title>Thesis figure pairing</title>
<style>
 body{{font:14px system-ui;margin:0;padding:24px;background:#f6f7f9;color:#111}}
 h1{{font-size:20px}}
 section{{background:#fff;border:1px solid #dcdfe4;border-radius:8px;
   padding:14px 16px;margin:0 0 14px;display:grid;
   grid-template-columns:1fr 320px;gap:12px 18px;align-items:start}}
 h2{{grid-column:1/3;margin:0;font-size:15px}}
 .stmt{{margin:0;color:#333}}
 pre{{grid-column:1;margin:0;background:#f2f3f5;padding:8px;border-radius:6px;
   font:12px ui-monospace,monospace;white-space:pre-wrap}}
 .figs{{grid-column:2;grid-row:2/4}}
 figure{{margin:0 0 8px}}
 img{{max-width:100%;border:1px solid #ccc;background:#fff}}
 figcaption{{font-size:11px;color:#666;margin-top:2px}}
 .miss{{color:#b00020;font-weight:600;font-size:12px}}
</style>
<h1>2001 thesis — figure pairing, {len(rows)} problems</h1>
{''.join(rows)}"""
    io.open(OUT, "w", encoding="utf-8").write(doc)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")
    print("problems with no figure:",
          [n for n in sorted(probs) if n not in figs])


if __name__ == "__main__":
    main()
