def zig_h(x1, x2, y):
    m = (x1 + x2) / 2; w = 30; n = 6; s = w / n
    pts = [(x1, y), (m - w/2, y)]
    for k in range(n):
        pts.append((m - w/2 + s*(k+0.5), y + (-6 if k % 2 == 0 else 6)))
    pts += [(m + w/2, y), (x2, y)]
    return pts
def zig_v(x, y1, y2):
    return [(px, py) for (py, px) in [(p[0], p[1]) for p in [(q[0], x + (q[1]-0)) for q in []]]]
def path(pts):
    return '<polyline fill="none" stroke="#1c2330" stroke-width="1.6" stroke-linejoin="round" points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) + '"/>'
X = [40, 150, 260, 370, 480]; YT, YB = 40, 160
out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 200" width="120mm">',
       '<style>text{font-family:"IBM Plex Sans",sans-serif;font-size:12px;fill:#1c2330}.n{fill:#2f5fa8;font-weight:600}</style>']
for y, names in ((YT, "abcde"), (YB, "fghij")):
    for i in range(4):
        out.append(path(zig_h(X[i], X[i+1], y)))
        out.append(f'<text x="{(X[i]+X[i+1])/2}" y="{y-12 if y==YT else y+22}" text-anchor="middle">1 Ω</text>')
    for i, nm in enumerate(names):
        if i in (0, 4):
            out.append(f'<circle cx="{X[i]}" cy="{y}" r="4" fill="#fff" stroke="#1c2330" stroke-width="1.6"/>')
            out.append(f'<text class="n" x="{X[i] + (-12 if i == 0 else 12)}" y="{y+4}" text-anchor="middle">{nm}</text>')
        else:
            out.append(f'<circle cx="{X[i]}" cy="{y}" r="2.6" fill="#1c2330"/>')
            out.append(f'<text class="n" x="{X[i]+8}" y="{y + (-8 if y == YT else 16)}">{nm}</text>')
for i in (1, 2, 3):
    x = X[i]; m = (YT+YB)/2; w = 30; n = 6; s = w/n
    pts = [(x, YT), (x, m - w/2)] + [(x + (6 if k % 2 == 0 else -6), m - w/2 + s*(k+0.5)) for k in range(n)] + [(x, m + w/2), (x, YB)]
    out.append(path(pts))
    out.append(f'<text x="{x+12}" y="{m+4}">1 Ω</text>')
out.append('</svg>')
open("ladder.svg", "w", encoding="utf-8").write("\n".join(out))
