"""Render the monograph's exemplar circuits with the v9 schematic
engine, and convert each SVG to PDF for inclusion in the appendix."""
import os
import sys

sys.path.insert(0, r"C:\Users\perez\Claude Code\Symbulator\repos\solver")
from symbulator.schematic import to_svg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

OUT = r"C:\Users\perez\Claude Code\Sym Docum\Documentation\paper\figures"
os.makedirs(OUT, exist_ok=True)

EXEMPLARS = {
    # 5.1 The two-stage amplifier of 1999 (thesis Problem 87)
    "ex_amplifier": (
        "e1,5,0,vg:r1,5,1,150:r2,1,0,1'k:cc1,1,0,100'p:cc2,1,2,3'p:"
        "jd1,2,0,0.05*v_1:r3,2,0,2'k:r4,2,3,100:r5,3,0,1'k:"
        "cc3,3,0,100'p:cc4,3,4,3'p:jd2,4,0,0.05*v_3:r6,4,0,2'k"),
    # 5.2 The 2013 showcase
    "ex_showcase2013": (
        "es,e,0,vs:js,0,d,is:r1,e,m,10:r2,a,e,20:r3,m,0,30:r4,b,m,40:"
        "r5,n,m,50:r6,c,d,60:r7,n,d,70:jd1,a,b,0.2*v_r7:"
        "ed2,c,b,0.1*i_r5:jd3,n,c,2*i_r1:ed4,0,n,0.7*v_r6"),
    # 5.3 Boulet, t<0 circuit
    "ex_boulet_before": (
        "e,s,0,18:r8,s,a,8:c1,a,0,1/6:r12,a,0,12:r18,a,b,18:"
        "r6,b,0,6:c2,b,0,1/3"),
    # 5.3 Boulet, t>0 circuit
    "ex_boulet_after": (
        "c1,a,0,1/6,9:r12,a,0,12:r18,a,b,18:r6,b,0,6:c2,b,0,1/3,9/4:"
        "js,0,b,10*e^(-t)*sin(2*t+30*pi/180)"),
    # 5.4 Three-phase wye-delta with line impedances
    "ex_threephase": (
        "ea1,na1,0,100:eb1,nb1,0,(100<-120):ec1,nc1,0,(100<120):"
        "raa,na1,na2,1:rbb,nb1,nb2,1:rcc,nc1,nc2,1:"
        "rac,na2,nc2,100+24*pi*j:rcb,nc2,nb2,100+24*pi*j:"
        "rba,nb2,na2,100+24*pi*j"),
    # 5.5 The ideal transformer, symbolically
    "ex_transformer": "t,2,3,1,n:r2,3,4,z2:e2,4,0,vs2",
    # 5.6 Coupled coils with initial conditions
    "ex_coupledcoils": "l1,1,0,2,1:r1,1,0,3:l2,2,0,2:r2,2,0,3:m,l1,l2,1",
    # 5.7 Two op-amps, all symbols
    "ex_twoopamps": (
        "e,1,0,vs:r12,1,2,1/g1:r14,1,4,1/g2:r23,2,3,1/g:r34,3,4,1/g:"
        "r2o,2,o,1/g4:r4o,4,o,1/g3:o1,0,2,3:o2,0,4,o"),
}

import re


def flatten_for_svglib(svg: str) -> str:
    """svglib ignores inheritable attributes on the root <svg> and the
    <style> block, so push them inline: wrap the content in a <g>
    carrying the stroke defaults, resolve currentColor to black, and
    expand the .lbl class into explicit text attributes."""
    svg = svg.replace('stroke="currentColor"', 'stroke="#000000"')
    svg = re.sub(r"<style>.*?</style>", "", svg, flags=re.S)
    svg = svg.replace(
        'class="lbl"',
        'font-family="Helvetica" font-size="13" fill="#000000" stroke="none"')
    m = re.match(r"(<svg[^>]*>)(.*)(</svg>)", svg, flags=re.S)
    head, body, tail = m.groups()
    wrap = ('<g fill="none" stroke="#000000" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round">')
    return head + wrap + body + "</g>" + tail


for name, desc in EXEMPLARS.items():
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
    print(f"{name}: svg {len(svg)} chars -> {os.path.getsize(pdf_path)} B pdf")
