#!/usr/bin/env python3
"""Draw chapter 13's Gain Example 1, the one figure with no artwork.

Every other cited figure is real: 220 practice scans, 26 screens, and 67
circuits imported from the archive. This one is Roberto's own example, so
there was nothing to import and it stayed a placeholder.

The circuit is the one the lesson already describes:

    es,3,0,1      1 V source, node 3 to ground
    rs,3,1,2      2 ohm in series, node 3 to node 1
    yp,1,2        the two-port, input at node 1, output at node 2
    rl,2,0,20     20 ohm load, node 2 to ground

Drawn to the same proportions as the imported figures -- around 1200 by
500 -- so it does not stand out on the page beside them. Resistors are
zigzags rather than IEC boxes, matching Alexander & Sadiku, which is
where most of the surrounding figures come from.

    python tools/draw_gain_example_1.py

Writes assets/circuit/gain-example-1.png, replacing the placeholder.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
from matplotlib.patches import Circle, FancyArrow, Rectangle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "circuit", "gain-example-1.png")

INK = "#1b2a41"
LW = 2.2
FS = 15


def wire(ax, *points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, color=INK, lw=LW, solid_capstyle="round", zorder=2)


def resistor(ax, x0, y0, x1, y1, label, above=True):
    """A zigzag resistor between two points, horizontal or vertical."""
    horizontal = abs(x1 - x0) > abs(y1 - y0)
    length = (x1 - x0) if horizontal else (y1 - y0)
    lead = length * 0.22
    body = length - 2 * lead
    n, amp = 6, 0.16

    pts = []
    if horizontal:
        wire(ax, (x0, y0), (x0 + lead, y0))
        wire(ax, (x1 - lead, y1), (x1, y1))
        step = body / n
        for i in range(n + 1):
            x = x0 + lead + i * step
            off = 0 if i in (0, n) else (amp if i % 2 else -amp)
            pts.append((x, y0 + off))
    else:
        wire(ax, (x0, y0), (x0, y0 + lead))
        wire(ax, (x1, y1 - lead), (x1, y1))
        step = body / n
        for i in range(n + 1):
            y = y0 + lead + i * step
            off = 0 if i in (0, n) else (amp if i % 2 else -amp)
            pts.append((x0 + off, y))
    wire(ax, *pts)

    if horizontal:
        ax.text((x0 + x1) / 2, y0 + (0.34 if above else -0.42), label,
                ha="center", va="bottom" if above else "top",
                fontsize=FS, color=INK)
    else:
        ax.text(x0 + 0.38, (y0 + y1) / 2, label, ha="left", va="center",
                fontsize=FS, color=INK)


def source(ax, x, y0, y1, label):
    """An independent voltage source: a circle with + and - inside."""
    cy = (y0 + y1) / 2
    r = 0.42
    wire(ax, (x, y0), (x, cy - r))
    wire(ax, (x, cy + r), (x, y1))
    ax.add_patch(Circle((x, cy), r, fill=False, ec=INK, lw=LW, zorder=3))
    ax.text(x, cy + 0.17, "+", ha="center", va="center",
            fontsize=FS + 2, color=INK, zorder=4)
    ax.text(x, cy - 0.19, "−", ha="center", va="center",
            fontsize=FS + 2, color=INK, zorder=4)
    ax.text(x - 0.62, cy, label, ha="right", va="center",
            fontsize=FS, color=INK)


def ground(ax, x, y):
    wire(ax, (x, y), (x, y - 0.34))
    for i, half in enumerate((0.42, 0.26, 0.11)):
        yy = y - 0.34 - i * 0.16
        ax.plot([x - half, x + half], [yy, yy], color=INK,
                lw=LW, solid_capstyle="round", zorder=2)


def node(ax, x, y, name, dx=0.0, dy=0.34):
    ax.add_patch(Circle((x, y), 0.075, fc=INK, ec=INK, zorder=5))
    ax.text(x + dx, y + dy, name, ha="center", va="bottom",
            fontsize=FS, color=INK, fontweight="bold")


def main():
    fig, ax = plt.subplots(figsize=(12.6, 5.8), dpi=100)
    ax.set_xlim(0, 12.6)
    ax.set_ylim(-0.55, 5.45)
    ax.axis("off")

    top, bot = 4.0, 1.0

    # ---- source branch, node 3 ------------------------------------------
    source(ax, 1.2, bot, top, "$V_s = 1$ V")
    wire(ax, (1.2, top), (2.4, top))
    node(ax, 2.4, top, "3")

    # ---- series resistance, into node 1 ---------------------------------
    resistor(ax, 2.4, top, 4.7, top, r"$R_s = 2\ \Omega$")
    node(ax, 4.7, top, "1")

    # ---- the two-port ----------------------------------------------------
    #
    # All four terminals leave the box's *sides*, not its bottom. Running
    # the lower pair straight down from the bottom edge closes a rectangle
    # against the return rail, and that reads as a component rather than
    # as two leads.
    bx0, bx1 = 6.2, 9.6
    by0, by1 = 1.85, top + 0.55
    low = 2.45                       # height of the lower pair of terminals
    ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0,
                           fill=False, ec=INK, lw=LW, zorder=3))
    wire(ax, (4.7, top), (bx0, top))
    wire(ax, (bx1, top), (10.9, top))
    wire(ax, (bx0, low), (5.65, low), (5.65, bot))
    wire(ax, (bx1, low), (10.15, low), (10.15, bot))

    # The box carries only its name. The four parameters sit under the
    # whole diagram instead: inside, they crowd the box and force it wider
    # than the circuit wants to be.
    mid = (bx0 + bx1) / 2
    ax.text(mid, (by0 + by1) / 2, "two-port", ha="center", va="center",
            fontsize=FS + 1, color=INK)

    # ---- load, node 2 ----------------------------------------------------
    node(ax, 10.9, top, "2")
    resistor(ax, 10.9, top, 10.9, bot, r"$R_L = 20\ \Omega$")

    # ---- the common return, and the ground ------------------------------
    wire(ax, (1.2, bot), (10.9, bot))
    ground(ax, 3.4, bot)
    ax.text(3.4 - 0.72, bot - 0.52, "0", ha="right", va="center",
            fontsize=FS, color=INK, fontweight="bold")

    # ---- Z_in, looking into the input port, clear of the box ------------
    zx = 5.45
    ax.add_patch(FancyArrow(zx, top - 0.95, 0.0, 0.70, width=0.012,
                            head_width=0.17, head_length=0.20,
                            length_includes_head=True, color=INK, zorder=4))
    ax.text(zx, top - 1.12, "$Z_{in}$", ha="center", va="top",
            fontsize=FS, color=INK)

    # ---- the two-port's parameters, under the whole diagram -------------
    ax.text(6.3, -0.22,
            "$y_{11} = 0.4$        $y_{12} = -0.002$        "
            "$y_{21} = -5$        $y_{22} = 0.04$",
            ha="center", va="center", fontsize=FS, color=INK)

    fig.savefig(OUT, dpi=100, bbox_inches="tight", facecolor="white",
                pad_inches=0.18)
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
