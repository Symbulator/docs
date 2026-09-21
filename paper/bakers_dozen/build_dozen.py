"""A Baker's Dozen (#464): twelve solved examples from the documentation
and a bonus, laid out as HTML and printed to paper/the_bakers_dozen.pdf
by Microsoft Edge. build.py ships that PDF as learn.symbulator.com/dozen.pdf.

    py paper\\bakers_dozen\\build_dozen.py

The circuit descriptions are read from the app tree's built-in examples,
so they cannot drift from what the links open. The answers are written
out below as LaTeX; they were checked against the app on 16 Sep 2026, and
an entry that changes wants them checked again.

Before changing or rebuilding anything, read README.md beside this file
(the brief, the reasons for each pick, the reserves) and run
check_dozen.py, which fails if an entry has moved in its .cir book.
"""
import html, io, os, re, shutil, subprocess, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(os.path.dirname(HERE))
ROOT = os.path.dirname(DOCS)
EX = os.path.join(ROOT, "Application", "v9", "repos", "server", "examples")
ASSETS = os.path.join(DOCS, "assets")
OUT = os.path.join(DOCS, "paper", "the_bakers_dozen.pdf")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
APP = "https://symbulator.pythonanywhere.com/"


def entry(book, n):
    """The n-th entry of a book: its circuit lines, exactly as the app has them."""
    text = io.open(os.path.join(EX, book + ".cir"), encoding="utf-8").read()
    blocks, cur = [], None
    for line in text.splitlines():
        if line.startswith("["):
            cur = []
            blocks.append(cur)
            continue
        if cur is None or not line.strip() or line.startswith("#"):
            continue
        if re.match(r"^[a-z_0-9]+:\s", line):
            continue
        cur.append(line)
    return "\n".join(blocks[n - 1])


def uri(path):
    return "file:///" + os.path.join(ASSETS, path).replace("\\", "/")


# Each run: (label, book, entry, lesson key for the link, settings, results)
# Results are LaTeX, checked against the app on 16 Sep 2026.
P = [
 dict(
  title="AS7's Example 3.4", tag="Supernodes around a dependent source",
  where="Alexander & Sadiku sampler", img="circuit/as7-ex3-4.jpg",
  question="Find the node voltages in the circuit of the figure.",
  why="Two voltage sources float between non-reference nodes, and one of them "
      "is worth three times the drop across a resistor. By hand that is two "
      "supernodes and a constraint equation. Here it is eight lines typed as "
      "they are drawn.",
  runs=[("DC", "Alexander_Sadiku", 2, "as7", "Analysis: DC. Rounding: approx.",
         [r"v_{1} = 26.667\ \mathrm{V}", r"v_{2} = 6.6667\ \mathrm{V}",
          r"v_{3} = 173.33\ \mathrm{V}", r"v_{4} = -46.667\ \mathrm{V}"])]),
 dict(
  title="NR12's Example 5.7", tag="A realistic op amp model",
  where="Nilsson & Riedel sampler", img="circuit/nr12-ex5-7.jpg",
  question=r"Analyze the noninverting amplifier using the realistic op amp model, "
           r"with open-loop gain $A$ = 50,000, input resistance $R_i$ = 100 kΩ and "
           r"output resistance $R_o$ = 7.5 kΩ. Find the gain $v_o/v_g$.",
  why="The model is a dependent source with a finite "
      "gain, an input resistance and an output resistance, written as three "
      "ordinary elements. The source stays a symbol, so the gain is read "
      "straight off the answer.",
  runs=[("DC", "Nilsson_Riedel", 14, "nr12",
         "Analysis: DC. Rounding: approx. Evaluate: v_3/vg.",
         [r"v_{3}/v_{g} = 5.9988"])]),
 dict(
  title="Bo2's Example 3.3", tag="Two op amps, every conductance a symbol",
  where="Course, Lesson 5 (Operational Amplifiers)",
  img="practice/bo2s-example-3-3-cascade-37.jpg",
  question=r"Find $v_o$ in terms of the conductances and the applied voltage $v_S$.",
  why="There is not a single number in the circuit. The answer is the gain as "
      "a formula, and its shape explains the circuit: a difference of "
      "conductances over a difference of conductances.",
  runs=[("DC", "Lesson_05b", 14, "5b", "Analysis: DC. Rounding: exact.",
         [r"v_{o} = \dfrac{(g_{1} - g_{2})\,v_{s}}{g_{3} - g_{4}}"])]),
 dict(
  title="AS7's Problem 9.73", tag="Eight impedances that will not reduce",
  where="Course, Lesson 7 (AC)", img="circuit/as7p0973.png",
  question="Determine the equivalent impedance for the circuit.",
  why="No two of these impedances are in series or in parallel, so by hand "
      "the circuit needs a delta-wye transformation. Find equivalent does it "
      "in one run.",
  runs=[("AC", "Lesson_07", 6, "7",
         "Analysis: Find equivalent, Resistance / impedance, between nodes 1 and 0, in AC. "
         "ω = 1 (any value gives the same answer, every impedance being in ohms). "
         "Rounding: 4 digits.",
         [r"Z_{eq} = 0.3794 + 1.46\,\mathrm{j}\ \Omega"])]),
 dict(
  title="AS7's Example 10.14", tag="Phasors with a dependent source",
  where="Course, Lesson 7 (AC)", img="circuit/as7e1014.png",
  question=r"Find $V_1$ and $V_2$ in the circuit.",
  why="Nine elements, three sources, one of them controlled by the voltage "
      "across a capacitor, and complex impedances on every branch. Nodal "
      "analysis by hand means complex algebra in two unknowns.",
  runs=[("AC", "Lesson_07", 10, "7", "Analysis: AC, ω = 1 (any value gives the same answer, every impedance "
         "being in ohms). Rounding: 4 digits. Show AC answers as polar phasors.",
         [r"V_{1} = 2.708\angle{-56.73^\circ}\ \mathrm{V}",
          r"V_{2} = 6.914\angle{-80.70^\circ}\ \mathrm{V}"])]),
 dict(
  title="AS7's Example 12.11", tag="Three-phase wye-delta with line impedances",
  where="Course, Lesson 9 (Three-Phase)", img="circuit/as7e1211.png",
  question=r"For the balanced Y-Δ circuit, find the line current $I_{aA}$, the "
           r"phase voltage $V_{AB}$ and the phase current $I_{AC}$. The source "
           r"frequency is 60 Hz.",
  why="The textbook converts the delta to a wye and works a single-phase "
      "equivalent. Symbulator needs neither: the three sources, the three "
      "lines and the delta go in as drawn.",
  runs=[("AC", "Lesson_09", 6, "9",
         "Analysis: AC, ω = 120π (60 Hz). Rounding: 4 digits. Polar phasors. "
         "Evaluate: vna2-vnb2.",
         [r"I_{aA} = i_{raa} = 2.350\angle{-36.20^\circ}\ \mathrm{A}",
          r"V_{AB} = v_{na2}-v_{nb2} = 169.9\angle{30.81^\circ}\ \mathrm{V}",
          r"I_{AC} = i_{rac} = 1.357\angle{-66.20^\circ}\ \mathrm{A}"])]),
 dict(
  title="AS7's Practice Problem 13.13", tag="Coupled coils in a tangle",
  where="Alexander & Sadiku sampler", img="circuit/as7-pp13-13.jpg",
  question=r"Find $i_o$ in the circuit of the figure.",
  why="Two coils coupled by k = 0.4, dots at opposite ends, a third coil, and a "
      "capacitor hung from the node the coupled coils share. The coupling is "
      "one line naming the two coils.",
  runs=[("AC", "Alexander_Sadiku", 48, "as7",
         "Analysis: AC, ω = 4. Rounding: 4 digits. Polar phasors.",
         [r"i_{o} = i_{r8} = 2.011\angle{68.51^\circ}\ \mathrm{A}"])]),
 dict(
  title="NR11's switched RLC with coupled coils", tag="A transient across a coupling",
  where="Course, Lesson 10 (Coupling)", img="circuit/sym_nr11_coupled_capacitor.png",
  question=r"A 48 V source feeds a 10 mF capacitor, a 4 Ω resistor and a 0.8 H coil "
           r"in series. A switch across the capacitor has been closed a long time "
           r"and opens at t = 0. The coil is coupled, M = 0.8 H, to a 1.6 H coil "
           r"across a 20 Ω resistor. Find $v_o$, the voltage across the 20 Ω, for t > 0.",
  why="A second-order primary talking to a first-order secondary through a "
      "mutual inductance. The answer carries both natural responses, an "
      "oscillation at 10 rad/s and a decay at 25 per second.",
  runs=[("DC, t < 0", "Lesson_10", 17, "10", "Analysis: DC.",
         [r"i_{l1} = 12\ \mathrm{A}", r"i_{l2} = 0\ \mathrm{A}"]),
        ("TR, t > 0", "Lesson_10", 18, "10", "Analysis: TR. Rounding: 4 digits. Evaluate: v4-v5.",
         [r"v_{o} = e^{-5t}\left(60\cos 10t - 120\sin 10t\right) - 60\,e^{-25t}\ \mathrm{V}"])]),
 dict(
  title="Bo2's Drill Exercise 6.6", tag="Two capacitors around an op amp",
  where="Course, Lesson 6 (Transients)",
  img="practice/bo2s-drill-exercise-6-6-op-amp-37.jpg",
  question=r"In the circuit, suppose that $v_S(t) = 2 - 2u(t)$ V. Find $v_o(t)$ for t ≥ 0.",
  why="An active second-order circuit whose two poles land in the same place. "
      "The repeated pole shows as the t in the answer, which no hand-picked "
      "solution form has to anticipate.",
  runs=[("DC, t < 0", "Lesson_06d", 7, "6d", "Analysis: DC.",
         [r"v_{ca} = 0\ \mathrm{V}", r"v_{cb} = 4\ \mathrm{V}"]),
        ("TR, t > 0", "Lesson_06d", 8, "6d", "Analysis: TR.",
         [r"v_{o} = (-4t-4)\,e^{-t}\ \mathrm{V}"])]),
 dict(
  title="Prof. Boulet's exam problem", tag="The switch, the ladder and the damped sine",
  where="Course, Lesson 6 (Transients)", img="practice/a-more-complex-problem-44.png",
  question=r"The circuit comes from the circuits analysis class of Professor Eliane "
           r"Boulet de Cabrera, at Universidad Tecnológica de Panamá. Find $v_1$ and $v$.",
  why="Two capacitors with their own initial conditions, and after the switch a "
      "current source that is itself a damped sinusoid. The answer holds two "
      "natural modes and a forced response. The TI calculator took 78 seconds "
      "and version 9 takes about one.",
  runs=[("DC, t < 0", "Lesson_06d", 18, "6d", "Analysis: DC. Rounding: exact.",
         [r"v_{ca} = 9\ \mathrm{V}", r"v_{cb} = 9/4\ \mathrm{V}"]),
        ("TR, t > 0", "Lesson_06d", 19, "6d",
         "Analysis: TR. Limit the results to v1, v2.",
         [r"\begin{aligned} v_{1} &= \left(\tfrac{5\sqrt{3}}{17}-\tfrac{20}{17}\right)e^{-t}\cos 2t"
          r" - \left(\tfrac{20\sqrt{3}}{17}+\tfrac{5}{17}\right)e^{-t}\sin 2t \\"
          r" &\quad + \left(\tfrac{80\sqrt{3}}{17}+\tfrac{193}{34}\right)e^{-t/2}"
          r" + \left(\tfrac{9}{2}-5\sqrt{3}\right)e^{-t}\ \mathrm{V}\end{aligned}",
          r"\begin{aligned} v_{2} &= -\left(\tfrac{245\sqrt{3}}{34}+\tfrac{20}{17}\right)e^{-t}\cos 2t"
          r" + \left(\tfrac{245}{34}-\tfrac{20\sqrt{3}}{17}\right)e^{-t}\sin 2t \\"
          r" &\quad + \left(\tfrac{80\sqrt{3}}{17}+\tfrac{193}{34}\right)e^{-t/2}"
          r" + \left(\tfrac{5\sqrt{3}}{2}-\tfrac{9}{4}\right)e^{-t}\ \mathrm{V}\end{aligned}"])]),
 dict(
  title="AS7's Problem 19.2", tag="A two-port with no ground",
  where="Course, Lesson 13 (Two-Ports)", img="circuit/as7-prob19-2.jpg",
  img2="circuit/sym_as7_p1902.png",
  cap2="The same circuit as Symbulator draws it. The tool takes f as the reference.",
  question="Determine the impedance parameters of the ladder: four 1 Ω resistors "
           "in the upper rail, four in the lower, three 1 Ω rungs.",
  why="Eleven resistors and no node 0 anywhere. Each port is written as its "
      "pair of terminals, so the lower rail stays in the circuit instead of "
      "being shorted to ground.",
  runs=[("DC", "Lesson_13", 14, "13",
         "Analysis: Find equivalent, Two-port parameters, z, between [a,f] and [e,j]. "
         "Rounding: 4 digits.",
         [r"z_{11} = z_{22} = 41/15 = 2.733\ \Omega",
          r"z_{12} = z_{21} = 1/15 = 0.06667\ \Omega"])]),
 dict(
  title="NR12's Example 18.6", tag="Two amplifiers known only by their h parameters",
  where="Nilsson & Riedel sampler", img="circuit/nr12-ex18-6.jpg",
  question=r"Two identical amplifiers are connected in cascade. Each is described by "
           r"its h parameters: $h_{11}$ = 1000 Ω, $h_{12}$ = 0.0015, $h_{21}$ = 100, "
           r"$h_{22}$ = 100 µS. The source has 500 Ω of internal resistance and the "
           r"load is 10 kΩ. Find the voltage gain $V_2/V_g$.",
  why="Each amplifier is a single element carrying its four parameters, and "
      "the cascade is two lines sharing a node. No matrix products, no "
      "conversions between parameter sets.",
  runs=[("DC", "Nilsson_Riedel", 16, "nr12",
         "Analysis: DC. Rounding: approx. Evaluate: v_c/vg.",
         [r"V_{2}/V_{g} = v_{c}/v_{g} = 33333.33"])]),
]

BONUS = dict(
  title="A freebie, on the house", tag="One dependent source of each kind",
  where="Course, Lesson 3 (Sources), as the Showing-off Problem",
  img="practice/the-showing-off-problem-expert-4.png",
  question=r"Find positive values for $V_s$ and $I_s$ that will result in 80 W "
           r"delivered by the VCCS and 0 W dissipated in the CCVS.",
  why="Invented by Roberto Perez-Franco in 2013 to show off. A VCCS, a CCVS, a CCCS and a VCVS woven "
      "through seven resistors, and the question runs backwards, from powers "
      "to sources. The two power conditions are quadratic, so four solutions "
      "fit, and the conditions pick the positive one. The answers also show "
      "why the CCVS dissipates nothing: its controlling current is exactly zero.",
  runs=[("DC, Expert Mode", "Lesson_03", 49, "3",
         "Analysis: DC. Rounding: 4 digits. Expert Mode: equations pjd1 = -80 and "
         "ped2 = 0, unknowns vs, is, conditions vs > 0 and is > 0.",
         [r"v_{s} = 17.61\ \mathrm{V}", r"i_{s} = 0.3973\ \mathrm{A}",
          r"i_{r5} = 0\ \mathrm{A}"])])


def esc(s):
    """Escape text but keep $...$ maths for KaTeX."""
    return html.escape(s, quote=False)


def page(p, label):
    out = [f'<section class="problem">',
           f'<div class="kicker">{label}</div>',
           f'<h2>{esc(p["title"])}</h2>',
           f'<div class="tag">{esc(p["tag"])}</div>',
           f'<div class="where">{esc(p["where"])}</div>',
           f'<p class="question">{esc(p["question"])}</p>',
           (f'<figure>{open(os.path.join(HERE, p["img"][4:]), encoding="utf-8").read()}</figure>' if p["img"].startswith("SVG:") else f'<figure><img src="{uri(p["img"])}"></figure>'),
           (f'<figure><img src="{uri(p["img2"])}"><figcaption>{esc(p["cap2"])}</figcaption></figure>' if p.get("img2") else ""),
           f'<p class="why"><b>Why it is here.</b> {esc(p["why"])}</p>']
    two = len(p["runs"]) > 1
    out.append(f'<div class="runs{" two" if two else ""}">')
    for lab, book, n, key, settings, results in p["runs"]:
        link = f"{APP}?lesson={key}&amp;entry={n}"
        out.append('<div class="run">')
        out.append(f'<div class="runhead">{esc(lab)}</div>')
        out.append(f'<pre>{esc(entry(book, n))}</pre>')
        out.append(f'<div class="settings">{esc(settings)}</div>')
        for r in results:
            out.append(f'<div class="result">$${r}$$</div>')
        out.append(f'<div class="link"><a href="{link}">{link}</a></div>')
        out.append('</div>')
    out.append('</div></section>')
    return "\n".join(out)


def main():
    toc = "".join(
        f'<li><span class="n">{i}</span><span class="t">{esc(p["title"])}</span>'
        f'<span class="g">{esc(p["tag"])}</span></li>' for i, p in enumerate(P, 1))
    toc += (f'<li class="bonus"><span class="n">★</span><span class="t">{esc(BONUS["title"])}</span>'
            f'<span class="g">{esc(BONUS["tag"])}</span></li>')
    body = [f"""
<section class="cover">
  <div class="logochip"><img class="logo" src="file:///{DOCS.replace(chr(92), '/')}/web/assets/logo.png"></div>
  <div class="brand">Symbulator 9</div>
  <h1>A Baker's Dozen</h1>
  <p class="sub">Twelve solved examples from the documentation, and a bonus</p>
  <p class="intro">Each of these circuits looks like an afternoon's work by hand.
  Symbulator solves each one in a single run, or in two when a switch splits
  the problem into intervals. No two of them make the same point. Every
  description below is the one in the app's built-in examples, and every answer was
  checked against the app on 16 September 2026. The link under each run opens
  the entry in the online app.</p>
  <ol class="toc">{toc}</ol>
</section>"""]
    for i, p in enumerate(P, 1):
        body.append(page(p, f"Sample {i} of 12"))
    body.append(page(BONUS, "Bonus"))
    doc = f"""<!doctype html><html><head><meta charset="utf-8">
<title>A Baker's Dozen</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<style>{io.open(os.path.join(HERE, 'style.css'), encoding='utf-8').read()}</style>
</head><body>
{''.join(body)}
<script>
document.addEventListener("DOMContentLoaded", function () {{
  renderMathInElement(document.body, {{delimiters: [
    {{left: "$$", right: "$$", display: true}},
    {{left: "$", right: "$", display: false}}], throwOnError: true}});
  document.body.setAttribute("data-ready", "1");
}});
</script>
</body></html>"""
    tmp = tempfile.mkdtemp(prefix="bakers_dozen_")
    page_path = os.path.join(tmp, "bakers.html")
    io.open(page_path, "w", encoding="utf-8").write(doc)
    if os.path.exists(OUT):
        os.remove(OUT)
    # Edge prints the page. The virtual-time budget lets the web fonts
    # and KaTeX (both fetched from their CDNs) finish before the print.
    subprocess.run([EDGE, "--headless=new", "--disable-gpu",
                    "--no-pdf-header-footer",
                    f"--user-data-dir={os.path.join(tmp, 'profile')}",
                    "--virtual-time-budget=25000",
                    f"--print-to-pdf={OUT}",
                    "file:///" + page_path.replace("\\", "/")], check=True)
    # msedge.exe can hand the job to a child and return before the PDF
    # lands, so wait for the file to appear and stop growing.
    last = -1
    for _ in range(120):
        size = os.path.getsize(OUT) if os.path.isfile(OUT) else -1
        if size > 0 and size == last:
            break
        last = size
        time.sleep(1)
    if not os.path.isfile(OUT):
        raise SystemExit("build_dozen.py: Edge produced no PDF.")
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT):,} bytes)")


if __name__ == "__main__":
    main()
