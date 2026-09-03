#!/usr/bin/env python3
"""
Stand-in figures for the prototype.

The real documentation uses Roberto's scanned schematics. Until those are
converted, this draws the two circuits used in the sample lesson, writing
each one as both .svg (for the website) and .pdf (for the PDFs) so that the
build has something real to place. Run once:

    python3 tools/make_demo_figures.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "circuit")
INK, ACC = "#16181A", "#B7791F"


def new_axes(w=6.4, h=3.4):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_axis_off()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.6)
    return fig, ax


def wire(ax, pts):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=INK, lw=1.6, solid_capstyle="round", zorder=1)


def resistor(ax, x, y, label, value, vertical=False):
    if vertical:
        ax.add_patch(Rectangle((x - 0.28, y - 0.62), 0.56, 1.24, fc="white",
                               ec=INK, lw=1.6, zorder=2))
        ax.text(x + 0.45, y + 0.16, label, fontsize=10, style="italic", color=INK)
        ax.text(x + 0.45, y - 0.42, value, fontsize=10, color=INK)
    else:
        ax.add_patch(Rectangle((x - 0.62, y - 0.28), 1.24, 0.56, fc="white",
                               ec=INK, lw=1.6, zorder=2))
        ax.text(x - 0.5, y + 0.45, label, fontsize=10, style="italic", color=INK)
        ax.text(x + 0.05, y + 0.45, value, fontsize=10, color=INK)


def source(ax, x, y, label, value):
    ax.add_patch(plt.Circle((x, y), 0.52, fc="white", ec=INK, lw=1.6, zorder=2))
    ax.text(x, y + 0.14, "+", ha="center", fontsize=11, color=INK, zorder=3)
    ax.text(x, y - 0.36, "\u2212", ha="center", fontsize=11, color=INK, zorder=3)
    ax.text(x - 1.5, y + 0.12, label, fontsize=10, style="italic", color=INK)
    ax.text(x - 1.5, y - 0.42, value, fontsize=10, color=INK)


def ground(ax, x, y):
    for i, w in enumerate((0.44, 0.28, 0.13)):
        ax.plot([x - w, x + w], [y - 0.16 * i, y - 0.16 * i], color=INK, lw=1.6)


def node(ax, x, y, name):
    ax.plot([x], [y], "o", ms=5, color=ACC, zorder=4)
    ax.text(x + 0.12, y + 0.22, name, fontsize=10, color=ACC, weight="bold")


def series_circuit(path, labelled):
    fig, ax = new_axes()
    wire(ax, [(1.2, 1.0), (1.2, 4.4), (3.0, 4.4)])
    wire(ax, [(4.2, 4.4), (6.0, 4.4)])
    wire(ax, [(7.2, 4.4), (8.6, 4.4), (8.6, 3.2)])
    wire(ax, [(8.6, 2.0), (8.6, 1.0), (1.2, 1.0)])
    source(ax, 1.2, 2.7, "E", "36 V")
    wire(ax, [(1.2, 3.22), (1.2, 4.4)])
    wire(ax, [(1.2, 1.0), (1.2, 2.18)])
    resistor(ax, 3.6, 4.4, "R1", "1 k\u03a9")
    resistor(ax, 6.6, 4.4, "R2", "3 k\u03a9")
    resistor(ax, 8.6, 2.6, "R3", "2 k\u03a9", vertical=True)
    ground(ax, 4.9, 1.0)
    if labelled:
        node(ax, 1.2, 4.4, "1")
        node(ax, 5.1, 4.4, "2")
        node(ax, 8.6, 4.4, "3")
        node(ax, 4.9, 1.0, "0")
    for ext in ("svg", "pdf"):
        fig.savefig(f"{path}.{ext}", bbox_inches="tight", transparent=True)
    plt.close(fig)


def divider_circuit(path):
    fig, ax = new_axes()
    wire(ax, [(1.4, 1.0), (1.4, 4.4), (3.2, 4.4)])
    wire(ax, [(4.4, 4.4), (7.4, 4.4), (7.4, 3.3)])
    wire(ax, [(7.4, 2.1), (7.4, 1.0), (1.4, 1.0)])
    source(ax, 1.4, 2.7, "V", "")
    wire(ax, [(1.4, 3.22), (1.4, 4.4)])
    wire(ax, [(1.4, 1.0), (1.4, 2.18)])
    resistor(ax, 3.8, 4.4, "R1", "")
    resistor(ax, 7.4, 2.7, "R2", "", vertical=True)
    ground(ax, 4.4, 1.0)
    node(ax, 1.4, 4.4, "a")
    node(ax, 7.4, 4.4, "c")
    node(ax, 4.4, 1.0, "0")
    for ext in ("svg", "pdf"):
        fig.savefig(f"{path}.{ext}", bbox_inches="tight", transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    series_circuit(os.path.join(OUT, "b11e0507"), labelled=False)
    series_circuit(os.path.join(OUT, "b11e0507b"), labelled=True)
    divider_circuit(os.path.join(OUT, "as5f0229"))
    print("wrote figures to", OUT)
