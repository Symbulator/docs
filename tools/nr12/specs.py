import sys
import os

# --- paths, resolved from this file rather than hardcoded -------------------
# tools/nr12 -> tools -> Documentation -> the project root.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
DOCS = os.path.join(_ROOT, "Documentation")
EXAMPLES = os.path.join(_ROOT, "Application", "v9", "repos", "server", "examples")
PDF = os.path.join(_ROOT, "Other", "NR12.pdf")
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
# -*- coding: utf-8 -*-
"""Every selected Nilsson & Riedel 12e example, modelled for Symbulator.

Fields
  num        the book's example number
  title      the book's example title (not shown; the runner prints it)
  ask        the statement, as the book words the question
  page       PDF page the example starts on
  fig        (page, figure-number) for the schematic crop
  desc       the Symbulator circuit description (colon form)
  domain     dc | ac | tr | fd      kind: circuit (default) | th | port
  expect     book answer -> Symbulator answer name  ("@expr" = evaluate an expression)
  booknames  answer name -> the book's own symbol, set beside the answer
  hide       answers the runner verifies but the page shows another way
  shows      the paragraph above the run: how we describe the circuit and
             what the settings mean -- no result, no method
  pre        first runs, each {text, desc, tag, expect, booknames, note}: the
             circuit before the switch moves, run in DC for an initial condition
  parts      (letter, text) -- a lettered part answered in prose, after the results
  evals      Evaluate steps after the results: {text, expr, at, unit, expect, book}
  after      what follows from the answers, after everything else

Roberto's rules (12 Sep 2026), applied to every entry:
  1. no book title;  2. the paragraph compares nothing with the book's method
  and states no result;  3. only what the question asks is reported;
  4. explain as to someone who does not know;  5. what follows from an answer
  comes after it;  6. nothing from thin air -- a value not in the problem
  statement is found on the page, by a run or by arithmetic shown in full;
  7. what the statement, the diagram or circuit theory gives is stated as
  fact; every decision of ours -- a name, a node, a symbol left open, the
  order of a source's nodes -- is stated as a choice, in the first person
  plural ("we name the galvanometer `rg`"), never as "is".

Prose conventions (gen.polish applies the house typography):
  * the book's own symbols go in $maths$ -- $i_o$, $v_C(t)$, $0.2 + j0.5$ --
    which polish() leaves alone and cir_entry() unwraps for the .cir note;
  * an app name goes in `code`;
  * an arithmetic minus in prose is U+2212 (−), never " - ", which becomes an
    em dash; an intended dash is written as one (—).
"""
SPECS = []

SPECS += [
dict(num="3.7", title="Using Voltage Division and Current Division to Solve a Circuit",
     ask="Use current division to find the current $i_o$ and use voltage division to find "
         "the voltage $v_o$ for the circuit in Fig. 3.22.",
     page=95, fig=(95, "3.22"), domain="dc",
     desc="j,0,1,8:r1,1,2,36:r2,2,0,44:r3,1,0,10:r4,1,3,40:r5,3,4,10:r6,4,0,30:r7,1,0,24",
     expect={"i_r7": 2, "v_r6": 18},
     booknames={"i_r7": "i_o", "v_r6": "v_o"},
     shows="We describe the circuit as it is drawn, naming the current source `j` and the "
           "resistors `r1` to `r7`, with the bottom rail as ground. Symbulator solves the "
           "whole circuit at once and both answers are among the results."),

dict(num="3.11", title="Applying a Delta-to-Wye Transform",
     ask="Find the current and power supplied by the 40 V source in the circuit shown in Fig. 3.35.",
     page=103, fig=(103, "3.35"), domain="dc",
     desc="e,1,0,40:r1,1,2,5:r2,2,3,100:r3,2,4,125:r4,3,4,25:r5,3,0,40:r6,4,0,37.5",
     expect={"@-i_e": 0.5, "@-p_e": 20},
     shownames={"@-i_e": "-i_e", "@-p_e": "-p_e"},
     shows="We write the bridge as it is drawn, naming the source `e` and the six "
           "resistors `r1` to `r6`, each between the two nodes it joins, with the source's "
           "lower end as ground; nothing has to be simplified first. One thing to know "
           "when reading the results: Symbulator reports the current through a source and "
           "the power it *consumes*, both counted into the source, whereas the question "
           "asks what the source *supplies*. The two differ only in sign, so the answers "
           "to the question are the negatives of `i_e` and `p_e`, which we type into "
           "{{card:Evaluate}} as `-i_e` and `-p_e`."),

dict(num="4.4", title="Using the Node-Voltage Method with Dependent Sources",
     ask="Use the node-voltage method to find the power dissipated in the 5 Ω resistor "
         "in the circuit shown in Fig. 4.10.",
     page=125, fig=(125, "4.10"), domain="dc",
     desc="e,1,0,20:r1,1,2,2:r2,2,0,20:r3,2,3,5:r4,3,0,10:r5,3,4,2:e2,4,0,8*ir3",
     expect={"p_r3": 7.2},
     shows="The circuit has a dependent voltage source, whose value is eight times the "
           "current $i_\\phi$ through the 5 Ω resistor. In Symbulator a dependent source "
           "needs no special element: it is a source whose value names another result. "
           "We name the 5 Ω resistor `r3`, so its current is `ir3`, and we write the "
           "dependent source as `e2` with the value `8*ir3`; we number the nodes 1 to 4 "
           "from the source rightward, with the bottom rail as ground. The power the "
           "question asks for is then the power consumed by `r3`."),

dict(num="4.7", title="Using the Mesh-Current Method with Dependent Sources",
     ask="Use the mesh-current method to find the power dissipated in the 4 Ω resistor "
         "in the circuit shown in Fig. 4.23.",
     page=133, fig=(133, "4.23"), domain="dc",
     desc="e,1,0,50:r1,1,3,1:r2,1,2,5:r3,2,3,4:r4,2,0,20:e2,3,0,15*ir4",
     expect={"p_r3": 16},
     shows="Again a dependent voltage source, this time worth fifteen times the current "
           "$i_\\phi$ in the 20 Ω resistor. We name that resistor `r4`, so its current is "
           "`ir4` and we write the source as `e2` with the value `15*ir4`; the 4 Ω "
           "resistor whose power is asked for we name `r3`."),

dict(num="4.21", title="Calculating the Condition for Maximum Power Transfer",
     ask="a) For the circuit shown in Fig. 4.65, find the value of $R_L$ that results in "
         "maximum power being transferred to $R_L$. b) Calculate the maximum power that can "
         "be delivered to $R_L$.",
     page=153, fig=(153, "4.65"), kind="th", n1="2", n2="0", domain="dc",
     desc="e,1,0,360:r1,1,2,30:r2,2,0,150",
     expect={"z": 25, "pmax": 900},
     booknames={"z": "R_L", "pmax": "p_{max}"},
     shows="The circuit to the left of $R_L$ is a source and two resistors. We describe "
           "those three and leave $R_L$ out, because the question is about what to connect "
           "at its terminals, and we call those terminals node **2** and ground. The "
           "{{card:Find equivalent}} card with *Thévenin / Norton* chosen and the two "
           "terminals named reduces the circuit to its Thévenin equivalent, and reports "
           "with it the load that would draw the most power from those terminals and how "
           "much that power is. By the maximum power theorem that load equals the Thévenin "
           "resistance, which the card reports as `z`; the power it reports as `pmax`."),
]

SPECS += [
dict(num="4.8", title="A Special Case in the Mesh-Current Method",
     ask="Use the mesh-current method to find branch currents $i_a$, $i_b$ and $i_c$ "
         "in the circuit for Example 4.3, repeated here as Fig. 4.25.",
     page=134, fig=(134, "4.25"), domain="dc",
     desc="e,1,0,50:r1,1,2,5:r2,2,0,10:r3,2,0,40:j,0,2,3",
     expect={"i_r1": 2, "i_r2": 4, "i_r3": 1},
     booknames={"i_r1": "i_a", "i_r2": "i_b", "i_r3": "i_c"},
     shows="A voltage source, three resistors and a current source. We name them `e`, "
           "`r1` to `r3` and `j`, and take the bottom rail as ground. A current source is "
           "written like a voltage source — name, two nodes, value — and its current "
           "flows through it from the first node to the second, so we write the 3 A "
           "source, whose arrow points up from the bottom rail into node 2, as `j,0,2,3`. "
           "The three branch currents the question names are the currents through the "
           "three resistors, each counted in the direction of the figure's arrow, which is "
           "the order we write each resistor's nodes in."),

dict(num="4.13", title="Using Special Source Transformation Techniques",
     ask="a) Use source transformations to find the voltage $v_o$ in the circuit shown in "
         "Fig. 4.42. b) Find the power developed by the 250 V voltage source. "
         "c) Find the power developed by the 8 A current source.",
     page=143, fig=(143, "4.42"), domain="dc",
     desc="e,1,0,250:r1,1,0,125:r2,1,2,25:j,2,9,8:r3,9,0,10:r4,2,0,100:r5,2,3,5:r6,3,0,15",
     expect={"v_r4": 20, "@-p_e": 2800, "@-p_j": 480},
     shownames={"@-p_e": "-p_e", "@-p_j": "-p_j"},
     booknames={"v_r4": "v_o"},
     shows="We write every element as it stands in the figure, the 125 Ω across the "
           "source and the 10 Ω under the current source included, naming the resistors "
           "`r1` to `r6` from left to right. The current source's arrow points down, from "
           "node 2 towards the 10 Ω, so we write its nodes in that order, `j,2,9,8`, "
           "calling the node between the source and the resistor **9**. The *power "
           "developed* by a source is the power it supplies, and Symbulator reports the "
           "power each element consumes, so parts (b) and (c) are the negatives of `p_e` "
           "and `p_j`, which we type into {{card:Evaluate}} as `-p_e` and `-p_j`. The "
           "question's $v_o$ is the voltage across the 100 Ω, `r4`."),

dict(num="4.23", title="Using Superposition to Solve a Circuit with Dependent Sources",
     ask="Use the principle of superposition to find $v_o$ in the circuit shown in Fig. 4.71.",
     page=156, fig=(156, "4.71"), domain="dc",
     desc="e,1,c,10:r1,1,a,5:r2,a,c,20:r3,b,0,10:j1,0,b,5:j2,b,a,0.4*vr3:e2,0,c,2*ir1",
     expect={"v_r2": 24},
     booknames={"v_r2": "v_o"},
     shows="Two independent sources and two dependent ones. We name the 5 Ω resistor "
           "`r1`, the 20 Ω `r2` and the 10 Ω `r3`. The dependent current source is worth "
           "$0.4v_\\Delta$, and $v_\\Delta$ is the voltage across the 10 Ω, so we write its "
           "value as `0.4*vr3`; the dependent voltage source is worth $2i_\\Delta$, and "
           "$i_\\Delta$ is the current through the 5 Ω, so we write its value as `2*ir1`. "
           "We write each source's nodes in the order its arrow or its polarity marks "
           "give, and we take the bottom-right node as ground. The question's $v_o$ is "
           "the voltage across the 20 Ω, `r2`."),

dict(num="5.1", title="Analyzing an Op Amp Circuit",
     ask="The op amp in the circuit shown in Fig. 5.7 is ideal. a) Calculate $v_o$ if "
         "$v_a$ = 1 V and $v_b$ = 0 V. b) Repeat (a) for $v_a$ = 1 V and $v_b$ = 2 V. "
         "c) If $v_a$ = 1.5 V, specify the range of $v_b$ that avoids amplifier saturation.",
     page=181, fig=(181, "5.7"), domain="dc",
     desc="ea,1,0,va:r1,1,2,25'k:r2,2,3,100'k:eb,4,0,vb:o,4,2,3",
     expect={"v_3": "5*vb - 4*va"},
     booknames={"v_3": "v_o"},
     parts=[
      ("a", "With {{var:v_a}} = 1 V and {{var:v_b}} = 0 V the formula gives "
            "{{var:v_o}} = 5(0) − 4(1) = {{o:-4}} V. That is inside the ±10 V "
            "supplies, so the op amp is in its linear region and −4 V is the "
            "answer."),
      ("b", "With {{var:v_a}} = 1 V and {{var:v_b}} = 2 V, {{var:v_o}} = "
            "5(2) − 4(1) = {{o:6}} V. Inside the supplies again, so the op "
            "amp is still linear."),
      ("c", "With {{var:v_a}} = 1.5 V the formula becomes {{var:v_o}} = "
            "5{{var:v_b}} − 6. The op amp stays linear while that lies between "
            "the rails: 5{{var:v_b}} − 6 = 10 gives {{var:v_b}} = {{o:3.2}} V, "
            "and 5{{var:v_b}} − 6 = −10 gives {{var:v_b}} = {{o:-0.8}} V, so "
            "the range is {{o:-0.8}} V ≤ {{var:v_b}} ≤ {{o:3.2}} V."),
     ],
     shows="An ideal op amp is the element `o`, whose three nodes are its non-inverting "
           "input, its inverting input and its output, in that order. We choose to write "
           "the circuit's two inputs as voltage sources with the symbolic values `va` and "
           "`vb` rather than the numbers in the question, so that a single run returns "
           "the output as a formula in both and each part can be read off it afterwards; "
           "we name those sources `ea` and `eb`, the two resistors `r1` and `r2`, and "
           "number the nodes from the $v_a$ input. Symbulator's ideal op amp has no "
           "supplies: it reports whatever output the inputs demand, so whether the "
           "amplifier is saturated is checked afterwards against the ±10 V supplies in "
           "the figure."),
]

SPECS += [
dict(num="5.3", title="Designing a Summing Amplifier",
     ask="a) Design a summing amplifier whose output voltage is "
         "$v_o = -4v_a - v_b - 5v_c$, using an ideal op amp with ±12 V power supplies "
         "and a 20 kΩ feedback resistor. b) Suppose $v_a$ = 2 V and $v_c$ = $-$1 V. "
         "What range of input voltages for $v_b$ allows the op amp to remain linear?",
     page=185, fig=(185, "5.12"), domain="dc",
     desc="ea,1,0,va:eb,2,0,vb:ec,3,0,vc:r1,1,n,5'k:r2,2,n,20'k:r3,3,n,4'k:rf,n,4,20'k:o,0,n,4",
     expect={"v_4": "-4*va - vb - 5*vc"},
     booknames={"v_4": "v_o"},
     parts=[
      ("a", "The run returns exactly the formula the design was asked for, which is "
            "the check that the resistor values are right."),
      ("b", "With {{var:v_a}} = 2 V and {{var:v_c}} = −1 V the formula becomes "
            "{{var:v_o}} = −4(2) − {{var:v_b}} − 5(−1) = −{{var:v_b}} − 3. The "
            "output reaches the −12 V rail when −{{var:v_b}} − 3 = −12, at "
            "{{var:v_b}} = {{o:9}} V, and the +12 V rail when −{{var:v_b}} − 3 = 12, "
            "at {{var:v_b}} = {{o:-15}} V. So the op amp stays linear for "
            "{{o:-15}} V ≤ {{var:v_b}} ≤ {{o:9}} V."),
     ],
     shows="The output of a summing amplifier with feedback resistor $R_f$ and input "
           "resistors $R_a$, $R_b$ and $R_c$ is $v_o = -(R_f/R_a)v_a - (R_f/R_b)v_b - "
           "(R_f/R_c)v_c$. The question fixes $R_f$ at 20 kΩ and asks for gains of 4, 1 "
           "and 5, so the input resistors are $R_a$ = 20/4 = 5 kΩ, $R_b$ = 20/1 = 20 kΩ "
           "and $R_c$ = 20/5 = 4 kΩ. That is the design, and the run is its check. We "
           "describe the circuit with those four resistors, naming them `r1`, `r2`, `r3` "
           "and `rf`; we write the three inputs as sources `ea`, `eb` and `ec` with the "
           "symbolic values `va`, `vb` and `vc`, so that the output comes back as a "
           "formula; and we write the op amp `o` with its non-inverting input at ground, "
           "its inverting input at a node we call **n**, and its output at node **4**."),

dict(num="5.3c", title="Designing a Summing Amplifier - part (c), in Expert Mode",
     ask="c) Suppose $v_a$ = 2 V, $v_b$ = 3 V and $v_c$ = $-$1 V. Using the input resistor "
         "values found in part (a), how large can the feedback resistor be before the op amp "
         "saturates?",
     page=185, fig=(185, "5.12"), domain="dc",
     desc="ea,1,0,2:eb,2,0,3:ec,3,0,-1:r1,1,n,5'k:r2,2,n,20'k:r3,3,n,4'k:rf,n,4,rf:o,0,n,4",
     equations=["v_4 = -12"], unknowns=["rf"],
     expect={"rf": 40000}, units={"rf": "\\Omega"},
     booknames={"rf": "R_f"},
     parts=[
      ("c", "So the feedback resistor can be as large as {{o:40}} kΩ. Any larger and "
            "the output would have to go beyond −12 V, which it cannot: the op amp "
            "saturates."),
     ],
     shows="Part (c) keeps the input resistors found in part (a) but asks a different "
           "kind of question. The inputs are now the numbers 2 V, 3 V and −1 V, and the "
           "unknown is the feedback resistor. With these inputs the summing amplifier's "
           "output is negative, so the rail it can reach is −12 V, and the largest "
           "feedback resistor is the one that puts the output exactly there. In Symbulator "
           "that is a question for {{card:Expert Mode}}: we write the feedback resistor "
           "as the symbol `rf` instead of a number, we write the output at the rail as "
           "the equation `v_4 = -12`, and we name `rf` as the unknown to solve for."),

dict(num="5.5", title="Designing a Difference Amplifier",
     ask="a) Design a difference amplifier that amplifies the difference between two input "
         "voltages by a gain of 8, using an ideal op amp and ±8 V power supplies. "
         "b) Suppose $v_a$ = 1 V. What range of $v_b$ keeps the op amp linear?",
     page=189, fig=(189, "5.16"), domain="dc",
     desc="ea,1,0,va:eb,2,0,vb:ra,1,n,1.5'k:rb,n,3,12'k:rc,2,p,1.5'k:rd,p,0,12'k:o,p,n,3",
     expect={"v_3": "8*vb - 8*va"},
     booknames={"v_3": "v_o"},
     parts=[
      ("a", "The run returns exactly 8({{var:v_b}} − {{var:v_a}}), the gain the design "
            "was asked for."),
      ("b", "With {{var:v_a}} = 1 V the output is {{var:v_o}} = 8{{var:v_b}} − 8, "
            "which reaches +8 V when 8{{var:v_b}} − 8 = 8, at {{var:v_b}} = {{o:2}} V, "
            "and −8 V when 8{{var:v_b}} − 8 = −8, at {{var:v_b}} = {{o:0}} V. So the op "
            "amp remains in its linear region for {{o:0}} V ≤ {{var:v_b}} ≤ "
            "{{o:2}} V."),
     ],
     shows="A difference amplifier's output is $v_o = (R_b/R_a)(v_b - v_a)$, provided the "
           "four resistors satisfy $R_a/R_b = R_c/R_d$. A gain of 8 therefore needs $R_b$ "
           "eight times $R_a$ and $R_d$ eight times $R_c$; one choice, the book's, is "
           "$R_a$ = $R_c$ = 1.5 kΩ and $R_b$ = $R_d$ = 12 kΩ. We describe the circuit "
           "with those values, naming the resistors `ra` to `rd` after the book's, and "
           "we write the two inputs as sources with the symbolic values `va` and `vb`, "
           "so that the output comes back as a formula; the run checks the design."),

dict(num="5.7", title="Analyzing a Noninverting-Amplifier Circuit Using a Realistic Op Amp Model",
     ask="Analyze the noninverting amplifier of Example 5.4 using the realistic op amp model, "
         "with open-loop gain $A$ = 50,000, input resistance $R_i$ = 100 kΩ and output "
         "resistance $R_o$ = 7.5 kΩ; there is no load resistance at the output. Find the "
         "gain $v_o/v_g$.",
     page=195, fig=(195, "5.21"), domain="dc",
     desc="eg,1,0,vg:rg,1,p,1'k:ri,p,n,100'k:rs,n,0,2'k:rf,n,3,10'k:ro,4,3,7.5'k:"
          "ea,4,0,50000*(vp-vn)",
     shownames={"@v_3/vg": "v_3/vg"}, units={"@v_3/vg": ""},
     booknames={"@v_3/vg": "v_o/v_g"},
     expect={"@v_3/vg": 5.9988}, tol=2e-5,
     shows="The realistic op amp in the figure is not the `o` element but three ordinary "
           "ones: the input resistance $R_i$ between the two inputs, the output resistance "
           "$R_o$ in series with the output, and a dependent voltage source whose value is "
           "the open-loop gain times the voltage between the inputs, $A(v_p - v_n)$. We "
           "call the two input nodes **p** and **n**, write the input resistance as `ri` "
           "between them, the output resistance as `ro`, and the dependent source as `ea` "
           "with the value `50000*(vp-vn)`. We leave the source as the symbol `vg`, so "
           "that the output voltage comes back as a multiple of `vg`; the gain asked for "
           "is that multiple, which we type into {{card:Evaluate}} as `v_3/vg`."),

dict(num="7.1", title="Determining the Natural Response of an RL Circuit",
     ask="The switch in the circuit shown in Fig. 7.6 has been closed for a long time before "
         "it is opened at $t$ = 0. Find a) $i_L(t)$ for $t$ ≥ 0, b) $i_o(t)$ for "
         "$t$ ≥ 0+, c) $v_o(t)$ for $t$ ≥ 0+.",
     page=250, fig=(250, "7.6"), domain="tr",
     pre=[dict(
        text="There are two intervals. Before $t$ = 0 the switch has been closed for a long "
             "time, so any transient has died away and every current is steady; in a steady "
             "circuit an inductor carries its current with no voltage across it, which is "
             "to say it behaves as a wire. So we describe the circuit as it stands before "
             "the switch opens — the 20 A source, the 0.1 Ω resistor, the inductor and the "
             "three resistors beyond it — and run it in DC to find the inductor's current. "
             "We name the source `j`, the inductor `l` and the resistors `r0` to `r3`, and "
             "we write the inductor with no fifth field, since nothing about its past is "
             "being told:",
        desc="j,0,1,20:r0,1,0,0.1:l,1,0,2:r1,1,2,2:r2,2,0,10:r3,2,0,40",
        tag="DC, before the switch opens",
        expect={"i_l": 20}, booknames={"i_l": "i_L(0)"},
        note="This is the circuit before the switch opens, run in DC to find the "
             "inductor's current, which the next entry takes as its initial condition.")],
     desc="l,1,0,2,20:r1,1,2,2:r2,2,0,10:r3,2,0,40",
     expect={"i_l": "20*exp(-5*t)", "i_r3": "-4*exp(-5*t)", "v_2": "-160*exp(-5*t)"},
     booknames={"i_l": "i_L", "i_r3": "i_o", "v_2": "v_o"},
     shows="Opening the switch disconnects the source and the 0.1 Ω resistor, and leaves "
           "the inductor to release its energy through the three resistors. That is the "
           "circuit for the second interval, $t$ ≥ 0, and we describe it with the same "
           "names, dropping `j` and `r0`. The inductor now starts with the 20 A just "
           "found, which we write into its line as a fifth field, after the inductance. "
           "We set the analysis to TR, and the answers come back as functions of $t$."),
]

SPECS += [
dict(num="7.3", title="Determining the Natural Response of an RC Circuit",
     ask="The switch in the circuit shown in Fig. 7.15 has been in position x for a long "
         "time. At $t$ = 0 it moves instantaneously to position y. Find a) $v_C(t)$ for "
         "$t$ ≥ 0, b) $v_o(t)$ for $t$ ≥ 0+, and c) $i_o(t)$ for $t$ ≥ 0+.",
     page=256, fig=(256, "7.15"), domain="tr",
     pre=[dict(
        text="Two intervals again. At position x the capacitor has been connected to the "
             "100 V source through the 10 kΩ resistor for a long time, and a capacitor in a "
             "steady circuit carries no current, so nothing flows in the 10 kΩ and the "
             "capacitor sits at the voltage of the source. We describe that circuit — the "
             "source, the 10 kΩ, which we name `r0`, and the capacitor, written without a "
             "fifth field — and run it in DC to find the capacitor's voltage:",
        desc="e,1,0,100:r0,1,2,10'k:c,2,0,0.5'u",
        tag="DC, before the switch moves",
        expect={"v_2": 100}, booknames={"v_2": "v_C(0)"},
        note="This is the circuit at position x, before the switch moves, run in DC to "
             "find the capacitor's voltage, which the next entry takes as its initial "
             "condition.")],
     desc="c,1,0,0.5'u,100:r1,1,2,32'k:r2,2,0,240'k:r3,2,0,60'k",
     expect={"v_1": "100*exp(-25*t)", "v_2": "60*exp(-25*t)",
             "i_r3": "0.001*exp(-25*t)"},
     booknames={"v_1": "v_C", "v_2": "v_o", "i_r3": "i_o"},
     shows="At position y the capacitor is connected instead to the 32 kΩ resistor and "
           "the two beyond it, and discharges through them. We describe that second "
           "circuit with the 100 V just found as the capacitor's fifth field, naming the "
           "three resistors `r1` to `r3` and the capacitor's node **1**, and set the "
           "analysis to TR."),

dict(num="7.5", title="Determining the Step Response of an RL Circuit",
     ask="The switch in the circuit shown in Fig. 7.21 has been in position a for a long "
         "time. At $t$ = 0 it moves from position a to position b. The switch is a "
         "make-before-break type, so the inductor current is continuous. a) Find the "
         "expression for $i(t)$ for $t$ ≥ 0. b) What is the initial voltage across the "
         "inductor just after the switch has been moved to position b?",
     page=260, fig=(260, "7.21"), domain="tr",
     pre=[dict(
        text="With the switch at position a, the inductor has been in parallel with the "
             "10 Ω resistor and the 8 A source for a long time. In that steady state the "
             "inductor is a wire, so the whole 8 A flows through it and none through the "
             "resistor. The direction matters: the source's arrow points down through the "
             "source, so its current comes up through the inductor, against the book's "
             "arrow for $i$. We write the source as `j,1,0,8`, its current flowing from "
             "node 1 down to ground, and the inductor as `l,1,0,0.2`, so that its current "
             "is counted downward like the book's $i$; a DC run then gives the current "
             "with its sign:",
        desc="j,1,0,8:r,1,0,10:l,1,0,0.2",
        tag="DC, at position a",
        expect={"i_l": -8}, booknames={"i_l": "i(0)"},
        note="This is the circuit at position a, before the switch moves, run in DC to "
             "find the inductor's current, which the next entry takes as its initial "
             "condition.")],
     desc="e,1,0,24:r1,1,2,2:l,2,0,0.2,-8",
     expect={"i_l": "12 - 20*exp(-10*t)", "v_2": "40*exp(-10*t)"},
     booknames={"i_l": "i"}, hide=["v_2"],
     evals=[dict(
        text="Part (b) asks for the voltage across the inductor the instant after the "
             "switch has moved. The inductor is between node 2 and ground, so its voltage "
             "is `v_2`, and we read its value at $t$ = 0 with {{card:Evaluate}}:",
        expr="v_2", at={"t": 0}, unit="V", expect=40, book="v(0^+)")],
     shows="Moving the switch to b connects the inductor, through the 2 Ω resistor, to "
           "the 24 V source instead. Because the switch is make-before-break, the "
           "inductor's current does not jump at the switching: it starts at the −8 A just "
           "found. We describe the second circuit with that −8 as the inductor's fifth "
           "field, sign included, naming the source `e` and the resistor `r1`, and set "
           "the analysis to TR."),

dict(num="7.10", title="Determining the Step Response of a Circuit with Magnetically Coupled Coils",
     ask="There is no energy stored in the circuit in Fig. 7.37 at the time the switch is "
         "closed. Find the solutions for $i_o$, $v_o$, $i_1$ and $i_2$.",
     page=271, fig=(271, "7.37"), domain="tr",
     desc="e,1,0,120:r1,1,2,7.5:l1,2,0,3:l2,2,0,15:m,l1,l2,6",
     expect={"i_r1": "16 - 16*exp(-5*t)", "v_2": "120*exp(-5*t)",
             "i_l1": "24 - 24*exp(-5*t)", "i_l2": "-8 + 8*exp(-5*t)"},
     booknames={"i_r1": "i_o", "v_2": "v_o", "i_l1": "i_1", "i_l2": "i_2"},
     shows="Two coils wound on one core, both fed from the same node. We write each coil "
           "as an inductor line of its own, `l1` and `l2`, and the coupling between them "
           "as the `m` line, which names the two coils and their mutual inductance, 6 H. "
           "No energy is stored, so we write neither inductor with a fifth field. The "
           "switch closing at $t$ = 0 needs no element: in TR a source with a plain "
           "numerical value is a step that begins at $t$ = 0, which is exactly what "
           "closing the switch on the 120 V source does. We name the source `e` and the "
           "resistor `r1`, and set the analysis to TR."),

dict(num="7.11a", title="Analyzing an RL Circuit That Has Sequential Switching (0 to 35 ms)",
     ask="The two switches in the circuit shown in Fig. 7.39 have been closed for a long "
         "time. At $t$ = 0 switch 1 is opened; then, 35 ms later, switch 2 is opened. "
         "a) Find $i_L(t)$ for 0 ≤ $t$ ≤ 35 ms.",
     page=273, fig=(273, "7.39"), domain="tr",
     pre=[dict(
        text="Three intervals this time, and three runs. In the first, both switches have "
             "been closed for a long time, the circuit is steady, and the inductor is a wire "
             "in parallel with the 18 Ω resistor. We describe the whole circuit — the 60 V "
             "source, the 4 Ω, 12 Ω, 6 Ω and 3 Ω resistors, the inductor and the 18 Ω — "
             "naming each resistor after its value, and run it in DC for the inductor's "
             "current:",
        desc="e,1,0,60:r4,1,2,4:r12,2,0,12:r6,2,0,6:r3,2,3,3:l,3,0,0.15:r18,3,0,18",
        tag="DC, both switches closed",
        expect={"i_l": 6}, booknames={"i_l": "i_L(0)"},
        note="This is the circuit with both switches closed, run in DC to find the "
             "inductor's current, which the next entry takes as its initial condition.")],
     desc="r6,2,0,6:r3,2,3,3:l,3,0,0.15,6:r18,3,0,18",
     expect={"i_l": "6*exp(-40*t)"},
     booknames={"i_l": "i_L"},
     evals=[dict(
        text="This run holds until switch 2 opens at 35 ms, and the inductor's current at "
             "that instant is where the third interval starts. We read it from the answer "
             "with {{card:Evaluate}}, giving the instant in seconds:",
        expr="i_l", at={"t": 0.035}, unit="A", expect=1.48, book="i_L(35\\,\\mathrm{ms})")],
     shows="In the second interval switch 1 has opened, which disconnects the 60 V source "
           "and the 4 Ω and 12 Ω resistors. We describe what remains — the 6 Ω, the 3 Ω, "
           "the inductor and the 18 Ω, with the same names — and give the inductor the 6 A "
           "just found as its fifth field. We set the analysis to TR."),

dict(num="7.11b", title="Analyzing an RL Circuit That Has Sequential Switching (after 35 ms)",
     ask="b) Find $i_L(t)$ for $t$ ≥ 35 ms. (Time is measured from the second switching.)",
     page=273, fig=(273, "7.39"), domain="tr",
     desc="r6,2,0,6:r3,2,3,3:l,3,0,0.15,6*exp(-1.4)",
     expect={"i_l": "6*exp(-1.4)*exp(-60*t)"},
     booknames={"i_l": "i_L"},
     shows="In the third interval switch 2 has opened too, removing the 18 Ω resistor, so "
           "the inductor now discharges through the 3 Ω and 6 Ω alone. We describe that "
           "circuit with the 18 Ω dropped, and give the inductor as its fifth field the "
           "current found at the end of the previous entry, $6e^{-40 \\times 0.035} = "
           "6e^{-1.4}$, about 1.48 A; we write it as the expression `6*exp(-1.4)`, which "
           "is exact. We measure time from the second switching, as the book does, so this "
           "run's $t$ = 0 is the instant switch 2 opens. The analysis is TR."),

dict(num="7.13", title="Finding the Unbounded Response in an RC Circuit",
     ask="a) When the switch is closed in the circuit shown in Fig. 7.45, the voltage on the "
         "capacitor is 10 V. Find the expression for $v_o$ for $t$ ≥ 0. b) Assume that the "
         "capacitor short-circuits when its terminal voltage reaches 150 V. How many "
         "milliseconds elapse before the capacitor short-circuits?",
     page=277, fig=(277, "7.45"), domain="tr",
     desc="c,1,0,5'u,10:r1,1,0,10'k:r2,1,0,20'k:j,0,1,7*ir2",
     expect={"v_1": "10*exp(40*t)"},
     booknames={"v_1": "v_o"},
     after="The exponent is positive, so the voltage grows instead of decaying: the "
           "dependent source feeds the capacitor faster than the resistors drain it. "
           "Part (b) is read off the answer: $10e^{40t}$ = 150 when $e^{40t}$ = 15, that "
           "is when $t = (\\ln 15)/40$ = {{o:0.0677}} s, so the capacitor short-circuits "
           "after {{o:67.7}} ms.",
     shows="The capacitor's 10 V is given in the question, and we write it into the "
           "capacitor's fifth field. The dependent current source is worth seven times "
           "the current $i_\\Delta$ in the 20 kΩ resistor; we name that resistor `r2`, so "
           "the source's value is `7*ir2`, and since its arrow points up into node 1 we "
           "write it as `j,0,1,7*ir2`. We set the analysis to TR."),

dict(num="8.2", title="Finding the Overdamped Natural Response of a Parallel RLC Circuit",
     ask="For the circuit in Fig. 8.6, $v(0^+)$ = 12 V and $i_L(0^+)$ = 30 mA. Find the "
         "expression for $v(t)$. (Example 8.3 asks the same circuit for its three branch "
         "currents.)",
     page=306, fig=(306, "8.6"), domain="tr",
     desc="c,1,0,0.2'u,12:l,1,0,50'm,0.03:r,1,0,200",
     expect={"v_1": "-14*exp(-5000*t) + 26*exp(-20000*t)",
             "i_r": "-0.07*exp(-5000*t) + 0.13*exp(-20000*t)",
             "i_l": "0.056*exp(-5000*t) - 0.026*exp(-20000*t)"},
     booknames={"v_1": "v", "i_r": "i_R", "i_l": "i_L"},
     shows="A capacitor, an inductor and a resistor in parallel. We write each as a line "
           "between node 1 and ground, naming them `c`, `l` and `r`, and put the two "
           "initial conditions the question gives in the fifth fields: 12 V on the "
           "capacitor and 30 mA, written 0.03, on the inductor. There is no source; the "
           "run is the circuit releasing the energy it holds. We set the analysis to TR."),

dict(num="8.4", title="Finding the Underdamped Natural Response of a Parallel RLC Circuit",
     ask="In the circuit shown in Fig. 8.8, $V_0$ = 0 and $I_0$ = $-$12.25 mA. Calculate "
         "the voltage response for $t$ ≥ 0.",
     page=310, fig=(310, "8.8"), domain="tr", at_t=[1e-4, 5e-4, 1e-3, 3e-3],
     desc="c,1,0,125'n,0:l,1,0,8,-0.01225:r,1,0,20'k",
     expect={"v_1": "100*exp(-200*t)*sin(979.80*t)"}, tol=3e-4,
     booknames={"v_1": "v"},
     after="The book prints the amplitude as 100 and the frequency of the sine as 979.80, "
           "both rounded; at six digits the run shows 100.021 and 979.796 for the same "
           "expression.",
     shows="The same three elements in parallel, and we describe them the same way. "
           "$V_0$ = 0 goes in the capacitor's fifth field and $I_0$ = −12.25 mA in the "
           "inductor's, written −0.01225 with the sign the question gives it. We set the "
           "analysis to TR."),

dict(num="8.11", title="Finding the Natural Response of a Series RLC Circuit",
     ask="The 0.1 µF capacitor in the circuit shown in Fig. 8.17 is charged to 100 V. At "
         "$t$ = 0 the capacitor is discharged through a series combination of a 100 mH "
         "inductor and a 560 Ω resistor. a) Find $i(t)$ for $t$ ≥ 0. b) Find $v_C(t)$ for "
         "$t$ ≥ 0.",
     page=328, fig=(328, "8.17"), domain="tr",
     desc="c,1,0,0.1'u,100:l,2,1,0.1:r,2,0,560",
     expect={"i_l": "-0.1042*exp(-2800*t)*sin(9600*t)",
             "v_1": "(100*cos(9600*t) + 29.17*sin(9600*t))*exp(-2800*t)"},
     at_t=[3e-5, 1e-4, 3e-4], tol=1e-3,
     booknames={"i_l": "i", "v_1": "v_C"},
     shows="We write the charged capacitor as the capacitor line with 100 V as its fifth "
           "field, and the inductor and the resistor after it round the loop, naming the "
           "three `c`, `l` and `r`. We write the inductor's nodes as 2 then 1 on purpose, "
           "so that its current is counted in the direction of the book's arrow for $i$; "
           "written the other way round the answer would come back with its sign "
           "reversed. The capacitor's voltage $v_C$ is then the voltage at node 1. We set "
           "the analysis to TR."),

dict(num="8.12", title="Finding the Step Response of a Series RLC Circuit",
     ask="No energy is stored in the 100 mH inductor or the 0.4 µF capacitor when the switch "
         "in the circuit shown in Fig. 8.18 is closed. Find $v_C(t)$ for $t$ ≥ 0.",
     page=328, fig=(328, "8.18"), domain="tr",
     desc="e,1,0,48:l,1,2,0.1:r,2,3,1250:c,3,0,0.4'u",
     expect={"v_3": "48 + 16*exp(-10000*t) - 64*exp(-2500*t)"},
     booknames={"v_3": "v_C"},
     shows="A single loop: the 48 V source, which in TR is a step beginning at $t$ = 0 "
           "and so stands for the switch closing, then the inductor, the resistor and the "
           "capacitor. We write them in that order, numbering the nodes 1 to 3 round the "
           "loop; neither the inductor nor the capacitor stores energy, so we write both "
           "without a fifth field. $v_C$ is then the voltage at node 3, the capacitor's "
           "upper end. We set the analysis to TR."),
]

import sympy as _sp
W = _sp.Symbol("omega")

SPECS += [
dict(num="9.9", title="Combining Impedances in Series and in Parallel",
     ask="The sinusoidal current source in the circuit shown in Fig. 9.20 produces the "
         "current $i_s$ = 8 cos 200,000$t$ A. b) Find the equivalent admittance to the right "
         "of the current source. c) Find the phasor voltage $V$. d) Find the phasor current "
         "$I$. e) Find the steady-state expressions for $v$ and $i$.",
     page=363, fig=(363, "9.20"), domain="ac", omega=200000,
     desc="j,0,1,8:r1,1,0,10:r2,1,2,6:l,2,0,40'u:c,1,0,1'u",
     expect={"v_1": 32 - 24j, "i_r2": -4j},
     booknames={"v_1": "V", "i_r2": "I"},
     evals=[dict(
        text="Part (b) asks for the admittance the source sees. Symbulator reports the "
             "impedance seen by each source, here `z_j`, and an admittance is the "
             "reciprocal of an impedance, so we type into {{card:Evaluate}}:",
        expr="1/z_j", unit="S", expect=0.16 + 0.12j, book="Y")],
     after="Part (e) is the two phasors written back as functions of time at the source's "
           "frequency: $v$ = 40 cos(200,000$t$ − 36.87°) V and $i$ = 4 cos(200,000$t$ − "
           "90°) A.",
     shows="The inductor and the capacitor are given as an inductance and a capacitance, "
           "and we write them as they are, `l,2,0,40'u` and `c,1,0,1'u`, putting the "
           "source's frequency, 200,000 rad/s, in the {{ui:ω — angular frequency}} box; "
           "the conversion to impedances is done inside the solver. We write the current "
           "source as `j,0,1,8`, its arrow pointing up into node 1, with its 8 A as the "
           "amplitude, which is what the book's phasors carry too, and we name the "
           "resistors `r1` and `r2`. We set the analysis to AC, and each answer is a "
           "phasor, printed both as a complex number and as an amplitude with an angle."),

dict(num="9.10", title="Using a Delta-to-Wye Transform in the Frequency Domain",
     ask="Use a delta-to-wye impedance transformation to find $I_0$, $I_1$, $I_2$, $I_3$, "
         "$I_4$, $I_5$, $V_1$ and $V_2$ in the circuit in Fig. 9.23.",
     page=365, fig=(365, "9.23"), domain="ac", omega=W,
     desc="e,a,0,120:r1,a,b,-4j:r2,a,c,63.2+2.4j:r3,b,c,10:r4,b,0,20+60j:r5,c,0,-20j",
     shownames={"@-i_e": "-i_e"},
     expect={"@-i_e": 2.4 + 3.2j, "i_r1": 2 + _sp.Rational(8, 3) * 1j,
             "i_r2": 0.4 + _sp.Rational(8, 15) * 1j,
             "i_r3": _sp.Rational(4, 3) + 4.266666666666667j,
             "i_r4": _sp.Rational(2, 3) - 1.6j, "i_r5": _sp.Rational(26, 15) + 4.8j,
             "v_b": _sp.Rational(328, 3) + 8j, "v_c": 96 - _sp.Rational(104, 3) * 1j},
     booknames={"@-i_e": "I_0", "i_r1": "I_1", "i_r2": "I_2", "i_r3": "I_3",
                "i_r4": "I_4", "i_r5": "I_5", "v_b": "V_1", "v_c": "V_2"},
     shows="Every impedance in this circuit is given in ohms, some purely reactive and "
           "some complex. We write each exactly as given — `-4j`, `63.2+2.4j`, `20+60j` — "
           "as a resistor with a complex value, naming the five `r1` to `r5` in the order "
           "of the book's $I_1$ to $I_5$, and we write each one's nodes in the direction "
           "of the figure's arrow, so that its current is counted as the book counts it. "
           "Nothing depends on the frequency, so we leave **omega** as a symbol in the "
           "{{ui:ω — angular frequency}} box. We keep the figure's letters for the nodes, "
           "with **d** as ground, so $V_1$ and $V_2$ are the voltages at **b** and **c**. "
           "The source current $I_0$ leaves the source's positive terminal, which is the "
           "opposite of how Symbulator counts a source's current, so it is `-i_e`, which "
           "we type into {{card:Evaluate}}. We set the analysis to AC."),

dict(num="9.12", title="Finding a Thevenin Equivalent in the Frequency Domain",
     ask="Find the Thevenin equivalent circuit with respect to terminals a,b for the "
         "circuit shown in Fig. 9.32.",
     page=368, fig=(368, "9.32"), kind="th", n1="9", n2="0", domain="ac", omega=W,
     desc="e,1,0,120:r1,1,2,12:r2,2,0,60:r3,2,9,-40j:e2,3,0,10*v2:r4,3,9,120",
     expect={"vth": 784 - 288j, "z": 91.2 - 38.4j},
     booknames={"vth": "V_{Th}", "z": "Z_{Th}"},
     shows="The dependent voltage source is worth ten times $V_x$, the voltage across the "
           "60 Ω resistor. We name that resistor `r2` and place it between node 2 and "
           "ground, so that $V_x$ is the voltage at node 2 and we can write the source's "
           "value as `10*v2`. We call the question's terminals a and b nodes **9** and "
           "**0**, and name them to the {{card:Find equivalent}} card with "
           "*Thévenin / Norton* chosen, which returns the equivalent's voltage and "
           "impedance; a dependent source in the circuit is no obstacle to it. The "
           "impedances are in ohms and nothing depends on the frequency, so we leave "
           "**omega** as a symbol. We set the analysis to AC."),

dict(num="9.14", title="Using the Mesh-Current Method in the Frequency Domain",
     ask="Use the mesh-current method to find the voltages $V_1$, $V_2$ and $V_3$ in the "
         "circuit shown in Fig. 9.39.",
     page=372, fig=(372, "9.39"), domain="ac", omega=W,
     desc="e,1,0,150:r1,1,2,1:r2,2,a,2j:r3,a,c,12:r4,c,0,-16j:r5,a,4,1:r6,4,b,3j:"
          "e2,b,0,39*ir3",
     shownames={"@v_1-v_a": "v_1 - v_a", "@v_a-v_b": "v_a - v_b"},
     expect={"@v_1-v_a": 78 - 104j, "v_a": 72 + 104j, "@v_a-v_b": 150 - 130j},
     booknames={"@v_1-v_a": "V_1", "v_a": "V_2", "@v_a-v_b": "V_3"},
     shows="The dependent source is worth 39 times $I_x$, the current down through the "
           "middle branch, the 12 Ω and −j16 Ω in series. We name the 12 Ω `r3`, so its "
           "current is `ir3` and we write the source's value as `39*ir3`; we name the "
           "other impedances `r1` to `r6`, and call the top of the middle branch node "
           "**a**, the far side of the −j16 Ω node **c** and the dependent source's top "
           "node **b**. The three voltages asked for are marked across three parts of the "
           "circuit in the figure: $V_1$ across the 1 Ω and j2 Ω on the left, which is the "
           "difference between the voltages at node 1 and node **a**; $V_2$ across the "
           "middle branch, which is the voltage at node **a** itself; and $V_3$ across the "
           "1 Ω and j3 Ω on the right, the difference between nodes **a** and **b**. We "
           "type the two differences into {{card:Evaluate}} as `v_1 - v_a` and "
           "`v_a - v_b`. Nothing depends on the frequency, so we leave **omega** as a "
           "symbol; we set the analysis to AC."),

dict(num="9.15", title="Analyzing a Linear Transformer in the Frequency Domain",
     ask="A linear transformer has $R_1$ = 200 Ω, $R_2$ = 100 Ω, $L_1$ = 9 H, $L_2$ = 4 H "
         "and $k$ = 0.5, and couples a load of an 800 Ω resistor in series with a 1 µF "
         "capacitor to a 300 V (rms) source of internal impedance $500 + j100$ Ω at "
         "400 rad/s. g) Calculate the Thevenin equivalent with respect to the terminals of "
         "the load impedance.",
     page=375, fig=(376, "9.42"), kind="th", n1="c", n2="d", domain="ac", omega=W, rms=True,
     desc="e,1,0,300:r1,1,2,500:r2,2,a,100j:r3,a,p,200:r4,p,0,3600j:m,r4,r5,1200j:"
          "r5,q,d,1600j:r6,q,c,100",
     expect={"vth": 93.9351 + 17.7715j, "z": 171.086 + 1224.2595j}, tol=1e-4,
     booknames={"vth": "V_{Th}", "z": "Z_{Th}"},
     shows="The transformer's two coils are given as inductances, and the frequency is "
           "given, so we work out their impedances first: $j\\omega L_1$ = $j$400 × 9 = "
           "$j$3600 Ω and $j\\omega L_2$ = $j$400 × 4 = $j$1600 Ω. The coupling is set by "
           "$k$: the mutual inductance is $M = k\\sqrt{L_1 L_2}$ = 0.5 × 6 = 3 H, so "
           "$j\\omega M$ = $j$1200 Ω. We then write each coil as an impedance, `r4` and "
           "`r5`, and the coupling between them as the `m` line naming the two and their "
           "mutual impedance, `m,r4,r5,1200j`; we name the winding resistances $R_1$ and "
           "$R_2$ `r3` and `r6`, and the source's internal impedance `r1` and `r2`. We "
           "leave the load out, because the question asks for the equivalent seen from "
           "its terminals, which we call nodes **c** and **d** and name to the "
           "{{card:Find equivalent}} card with *Thévenin / Norton* chosen. Two things "
           "about the secondary side. It is not connected to ground anywhere — nothing "
           "conducts between the two windings — so its bottom is simply the node we have "
           "called **d**, and Symbulator says in a note that it has measured that side's "
           "voltages against **d**; the currents, the voltage differences and the "
           "equivalent are unaffected. And the source is given in rms, so we tick "
           "{{ui:RMS phasors}} in {{card:Settings}}. Every value is in ohms already, so we "
           "leave **omega** as a symbol; we set the analysis to AC."),
]

SPECS += [
dict(num="10.8", title="Balancing Power Delivered with Power Absorbed in an AC Circuit",
     ask="a) Calculate the total average and reactive power delivered to each impedance in "
         "the circuit shown in Fig. 10.18. b) Calculate the average and reactive powers "
         "associated with each source. c) Verify that the average power delivered equals the "
         "average power absorbed, and likewise for the reactive power.",
     page=417, fig=(417, "10.18"), domain="ac", omega=W,
     desc="e,1,0,150:r1,1,2,1:r2,2,a,2j:r3,a,c,12:r4,c,0,-16j:r5,a,4,1:r6,4,b,3j:"
          "e2,b,0,39*ir3",
     expect={"@s_r1+s_r2": 1690 + 3380j, "@s_r3+s_r4": 240 - 320j,
             "@s_r5+s_r6": 1970 + 5910j, "s_e": 1950 - 3900j, "s_e2": -5850 - 5070j,
             "@s_e+s_e2+s_r1+s_r2+s_r3+s_r4+s_r5+s_r6": 0},
     shownames={"@s_r1+s_r2": "s_r1 + s_r2", "@s_r3+s_r4": "s_r3 + s_r4",
                "@s_r5+s_r6": "s_r5 + s_r6",
                "@s_e+s_e2+s_r1+s_r2+s_r3+s_r4+s_r5+s_r6": "the sum of all eight"},
     shows="The circuit of Example 9.14, which we describe the same way, asked a "
           "different question. Symbulator reports every element's complex power as `s_` "
           "followed by the element's name: its real part is the average power and its "
           "imaginary part the reactive power, so parts (a) and (b) are all read from one "
           "run. Each impedance in the figure is two elements in our description, a "
           "resistor and a reactance in series, so the power delivered to the impedance "
           "is the sum of their two `s` answers, which we type into {{card:Evaluate}} as "
           "`s_r1 + s_r2`. The balance of part (c) is the sum of all eight, typed the "
           "same way. Nothing depends on the frequency, so we leave **omega** as a symbol; "
           "we set the analysis to AC."),

dict(num="10.12", title="Finding Maximum Power Transfer in a Circuit with an Ideal Transformer",
     ask="The variable resistor in the circuit in Fig. 10.25 is adjusted until maximum "
         "average power is delivered to $R_L$. a) What is the value of $R_L$ in ohms? "
         "b) What is the maximum average power delivered to $R_L$?",
     page=423, fig=(423, "10.25"), kind="th", n1="a", n2="0", domain="ac", omega=W, rms=True,
     desc="e,1,0,840:r60,1,p,60:t,[p,x],[x,a],[4,1]:r20,x,0,20",
     expect={"z": 35, "pmax": 315},
     booknames={"z": "R_L", "pmax": "p_{max}"},
     shows="An ideal transformer is the element `t`. Its primary and secondary here share "
           "a node, so we write each winding as a bracketed pair of terminals, `[p,x]` for "
           "the primary and `[x,a]` for the secondary, followed by the turns ratio `[4,1]`; "
           "we name the two resistors after their values, `r60` and `r20`. We leave the "
           "load $R_L$ out of the description and name its terminals, node **a** and "
           "ground, to the {{card:Find equivalent}} card with *Thévenin / Norton* chosen, "
           "which reports the load that would draw the most average power from those "
           "terminals and how much. By the maximum power theorem that load is the "
           "Thévenin impedance, reported as `z`, and the power is `pmax`. The source is "
           "given as 840 V rms, so we tick {{ui:RMS phasors}} in {{card:Settings}}; there "
           "is no reactance anywhere, so we leave **omega** as a symbol. We set the "
           "analysis to AC."),

dict(num="11.1", title="Analyzing a Wye-Wye Circuit",
     ask="A balanced, positive-sequence Y-connected generator with an internal impedance of "
         "$0.2 + j0.5$ Ω per phase and an internal voltage of 120 V per phase feeds a "
         "balanced Y-connected load of $39 + j28$ Ω per phase over a line of $0.8 + j1.5$ Ω "
         "per phase; the a-phase internal voltage is the reference. b) Calculate the three "
         "line currents. c) Calculate the phase voltages at the load. d) Calculate the line "
         "voltages at the load. e) Calculate the phase voltages at the generator terminals.",
     page=446, fig=(446, "11.10"), domain="ac", omega=W,
     desc="ea,ga,0,120:eb,gb,0,120*exp(-2j*pi/3):ec,gc,0,120*exp(2j*pi/3):"
          "rga,ga,a,0.2+0.5j:rgb,gb,b,0.2+0.5j:rgc,gc,c,0.2+0.5j:"
          "rla,a,pa,0.8+1.5j:rlb,b,pb,0.8+1.5j:rlc,c,pc,0.8+1.5j:"
          "rfa,pa,nn,39+28j:rfb,pb,nn,39+28j:rfc,pc,nn,39+28j",
     shownames={"@Abs(v_pa-v_nn)": "|v_pa - v_nn|", "@Abs(v_pa-v_pb)": "|v_pa - v_pb|",
                "@Abs(v_a)": "|v_a|"},
     expect={"i_rla": 1.92 - 1.44j, "@Abs(v_pa-v_nn)": 115.22, "@Abs(v_pa-v_pb)": 199.58,
             "@Abs(v_a)": 118.90},
     booknames={"i_rla": "I_{aA}", "@Abs(v_pa-v_nn)": "|V_{AN}|",
                "@Abs(v_pa-v_pb)": "|V_{AB}|", "@Abs(v_a)": "|V_{An}|"},
     after="The question asks for all three phases of each quantity. In a balanced "
           "circuit the b and c phases carry the same magnitudes as the a phase, at "
           "−120° and +120° from it, and the run's `i_rlb` and `i_rlc`, `v_pb` and "
           "`v_pc` bear that out.",
     shows="We describe the whole three-phase circuit, one phase at a time: three "
           "sources at the generator's internal nodes, which we call **ga**, **gb** and "
           "**gc**, each carrying its phase in its value — `120*exp(-2j*pi/3)` is 120 V "
           "at −120° — then the generator's, the line's and the load's impedance in each "
           "phase, all in ohms, which we name `rga`, `rla` and `rfa` for the a phase and "
           "likewise for b and c. We take the generator's neutral as ground and call the "
           "load's neutral **nn**; we call the generator's terminals **a**, **b** and "
           "**c** and the load's **pa**, **pb** and **pc**. Nothing depends on the "
           "frequency, so we leave **omega** as a symbol. The question's quantities are "
           "then ordinary results: the a-phase line current $I_{aA}$ is the current "
           "through the line impedance `rla`; the phase voltage at the load, $V_{AN}$, is "
           "the voltage between **pa** and **nn**; the line voltage $V_{AB}$ is the "
           "voltage between **pa** and **pb**; and the phase voltage at the generator's "
           "terminal, $V_{An}$, is the voltage at node **a**. We type each difference "
           "into {{card:Evaluate}} as `v_pa - v_nn`, and its magnitude as "
           "`Abs(v_pa - v_nn)`, since the book quotes the voltages by magnitude. We set "
           "the analysis to AC."),
]

SPECS += [
dict(num="13.2", title="The Natural Response of an RC Circuit",
     ask="The circuit in Fig. 13.11 was analyzed in Example 7.3 using first-order circuit "
         "analysis techniques. Use the Laplace transform method to find $v_o(t)$ for "
         "$t$ ≥ 0+.",
     page=515, fig=(515, "13.11"), domain="fd",
     pre=[dict(
        text="The circuit is Example 7.3's, and so is its first interval: before the switch "
             "moves the capacitor has sat across the 100 V source through the 10 kΩ for a "
             "long time, carrying no current. We describe that circuit as before and run it "
             "in DC for the capacitor's voltage:",
        desc="e,1,0,100:r0,1,2,10'k:c,2,0,0.5'u",
        tag="DC, before the switch moves",
        expect={"v_2": 100}, booknames={"v_2": "v_C(0)"},
        note="This is the circuit at position x, before the switch moves, run in DC to "
             "find the capacitor's voltage, which the next entry takes as its initial "
             "condition.")],
     desc="c,1,0,0.5'u,100:r1,1,2,32'k:r2,2,0,240'k:r3,2,0,60'k",
     expect={"v_1": "100/(s + 25)", "v_2": "60/(s + 25)"},
     hide=["v_1"],
     booknames={"v_2": "V_o(s)"},
     after="That is the transform of the answer Example 7.3 found in the time domain, "
           "$60e^{-25t}$: FD returns the transform, TR its inverse, for the same "
           "description.",
     shows="The second interval is the same description as Example 7.3's second run, the "
           "100 V in the capacitor's fifth field, with one difference: we set the analysis "
           "to FD instead of TR. FD returns each answer as a function of $s$, the Laplace "
           "transform of the answer in time, with the initial condition already inside it."),

dict(num="13.3", title="The Step Response of an RLC Circuit",
     ask="Consider the circuit in Fig. 13.13, where the initial current in the inductor is "
         "29 mA and the initial voltage across the capacitor is 50 V. This circuit was "
         "analyzed in Example 8.10 using second-order circuit analysis techniques. Use the "
         "Laplace transform method to find $v(t)$ for $t$ ≥ 0.",
     page=515, fig=(515, "13.13"), domain="fd",
     desc="j,0,1,0.024/s:c,1,0,25'n,50:l,1,0,25'm,0.029:r,1,0,500",
     expect={"v_1": "(50*s - 200000)/(s**2 + 80000*s + 1600000000)"},
     booknames={"v_1": "V(s)"},
     shows="The 24 mA source is a constant current switched on at $t$ = 0. In the $s$ "
           "domain a constant $I$ switched on at $t$ = 0 has the transform $I/s$, so we "
           "write the source's value as `0.024/s`. We put the two initial conditions the "
           "question gives in the fifth fields of the capacitor and the inductor, 50 V and "
           "29 mA written 0.029, and name the four elements `j`, `c`, `l` and `r`. We set "
           "the analysis to FD, and the answer is the transform $V(s)$ of the voltage the "
           "question asks for; the book inverts it into $v(t)$ by hand, and choosing TR "
           "instead would do that inversion in the same run."),

dict(num="13.5", title="Analyzing a Circuit with Multiple Meshes",
     ask="The circuit in Fig. 13.17 has no initial stored energy. At $t$ = 0 the switch "
         "closes. Use Laplace methods to find $i_1(t)$ and $i_2(t)$ for $t$ ≥ 0.",
     page=519, fig=(519, "13.17"), domain="tr",
     desc="e,1,0,336:l1,1,2,8.4:r1,2,0,42:l2,2,3,10:r2,3,0,48",
     expect={"i_l1": "15 - 14*exp(-2*t) - exp(-12*t)",
             "i_l2": "7 - 8.4*exp(-2*t) + 1.4*exp(-12*t)"},
     booknames={"i_l1": "i_1", "i_l2": "i_2"},
     shows="No energy is stored, so we write the two inductors without fifth fields, and "
           "the switch closing at $t$ = 0 onto the 336 V source needs no element of its "
           "own: in TR a numerical source value is a step that begins at $t$ = 0. We name "
           "the inductors `l1` and `l2` after the book's $i_1$ and $i_2$, which are the "
           "currents through them, and the resistors `r1` and `r2`. The question comes "
           "from the book's Laplace chapter, but we set the analysis to TR, which returns "
           "the two currents as functions of $t$; the transform and its inversion happen "
           "inside the solver."),

dict(num="13.6", title="Creating a Thevenin Equivalent in the s Domain",
     ask="The circuit in Fig. 13.20 has no initial stored energy, and at $t$ = 0 the switch "
         "closes. Find the Thevenin equivalent for the circuit to the left of the terminals "
         "a and b in the s domain, using Laplace methods.",
     page=521, fig=(521, "13.20"), kind="th", n1="a", n2="0", domain="fd",
     desc="e,1,0,480/s:r1,1,2,20:l,2,0,0.002:r2,2,a,60",
     expect={"vth": "480/(s + 10000)", "z": "80*(s + 7500)/(s + 10000)"},
     booknames={"vth": "V_{Th}", "z": "Z_{Th}"},
     shows="The 480 V source switched on at $t$ = 0 is a step, whose transform is "
           "$480/s$, so we write its value as `480/s`. We call the terminals a and b node "
           "**a** and ground, and name them to the {{card:Find equivalent}} card with "
           "*Thévenin / Norton* chosen; the card works in FD as it does in DC and AC, and "
           "returns the equivalent's voltage and impedance as functions of $s$. We leave "
           "out the capacitor to the right of the terminals, since the question asks for "
           "the equivalent seen from them."),

dict(num="13.7", title="Analyzing a Circuit with Mutual Inductance",
     ask="The make-before-break switch in the circuit in Fig. 13.23 has been in position a "
         "for a long time. At $t$ = 0 it moves instantaneously to position b. Use Laplace "
         "methods to find $i_2(t)$ for $t$ ≥ 0.",
     page=523, fig=(523, "13.23"), domain="tr",
     pre=[dict(
        text="Two intervals. With the switch at position a the primary side has been "
             "steady for a long time: the 60 V source drives a constant current through the "
             "9 Ω, the 3 Ω and the 2 H coil, which in a steady circuit is a wire. The "
             "secondary has no source of its own, and a constant current in the primary "
             "induces nothing in it, so its current is zero. We describe the whole circuit, "
             "naming the resistors after their values, `r9`, `r3`, `r2b` and `r10`, the "
             "coils `l1` and `l2`, and the coupling as the `m` line with their mutual "
             "inductance, 2 H; we call the secondary's nodes **q**, **c** and **d**. A DC "
             "run gives both currents; it also notes that the secondary has no path to "
             "ground, which is true of the figure and changes nothing:",
        desc="e,1,0,60:r9,1,a,9:r3,a,p,3:l1,p,0,2:m,l1,l2,2:l2,q,d,8:r2b,q,c,2:r10,c,d,10",
        tag="DC, at position a",
        expect={"i_l1": 5, "i_l2": 0}, booknames={"i_l1": "i_1(0)", "i_l2": "i_2(0)"},
        note="This is the circuit at position a, before the switch moves, run in DC to "
             "find the two coil currents, which the next entry takes as its initial "
             "conditions.")],
     desc="r3,0,p,3:l1,p,0,2,5:m,l1,l2,2:l2,q,d,8,0:r2b,q,c,2:r10,c,d,10",
     expect={"i_l2": "1.25*exp(-t) - 1.25*exp(-3*t)"},
     booknames={"i_l2": "i_2"},
     shows="At $t$ = 0 the switch moves to b, which takes the source and the 9 Ω out and "
           "closes the primary on the 3 Ω alone. We describe that circuit with the same "
           "names and the two currents just found as the coils' fifth fields, 5 and 0. "
           "The secondary is still not connected to ground, so its bottom is simply the "
           "node we called **d**, and Symbulator again notes that it measures that side's "
           "voltages against **d**; the currents are unaffected. We set the analysis to "
           "TR, and $i_2$ is the current through `l2`."),

dict(num="13.9", title="Deriving the Transfer Function of a Circuit",
     ask="The voltage source $v_g$ drives the circuit shown in Fig. 13.31. The output signal "
         "is the voltage across the capacitor, $v_o$. a) Find the transfer function for this "
         "circuit. b) Calculate the numerical values for the poles and zeros of the transfer "
         "function.",
     page=527, fig=(527, "13.31"), domain="fd",
     desc="e,1,0,vg:r1,1,2,1000:r2,2,3,250:l,3,0,50'm:c,2,0,1'u",
     expect={"@v_2/vg": "1000*(s + 5000)/(s**2 + 6000*s + 25000000)"},
     labels={"@v_2/vg": "transfer function"},
     texnames={"@v_2/vg": "H(s) = \\dfrac{v_{2}}{v_{g}}"},
     units={"@v_2/vg": ""},
     after="Part (b): the poles are the roots of the denominator, $s^2 + 6000s + "
           "25{,}000{,}000 = 0$, which are $s = -3000 \\pm j4000$; the zero is the root of "
           "the numerator, $s = -5000$.",
     shows="A transfer function is the ratio of an output to the input that produced it, "
           "as functions of $s$. We therefore leave the source as the symbol `vg`, so that "
           "the output comes back as a multiple of it, and set the analysis to FD. We "
           "number the nodes from the source, so the output, the capacitor's voltage, is "
           "the voltage at node 2, and the transfer function is `v_2/vg`, which we type "
           "into {{card:Evaluate}}."),

dict(num="13.13", title="A Series Inductor Circuit with an Impulsive Response",
     ask="The switch in the circuit shown in Fig. 13.50 has been closed for a long time. At "
         "$t$ = 0 it opens. Use Laplace methods to find the output voltage $v_o$ and the "
         "current in the 3 H inductor, $i_1$.",
     page=541, fig=(541, "13.50"), domain="tr",
     pre=[dict(
        text="Two intervals. While the switch is closed it is a wire from the junction after "
             "$L_1$ down to the bottom rail, so the circuit that has been steady for a long "
             "time is the 100 V source, the 10 Ω and $L_1$ in a loop through that wire, "
             "with the 15 Ω and $L_2$ hanging across a short circuit and carrying nothing. "
             "We describe that circuit and run it in DC for the two inductor currents; we "
             "write the closed switch by giving both its ends the same node, ground, and "
             "name the inductors `l1` and `l2` after the book's $L_1$ and $L_2$:",
        desc="e,1,0,100:r1,1,2,10:l1,2,0,3:r2,0,4,15:l2,4,0,2",
        tag="DC, switch closed",
        expect={"i_l1": 10, "i_l2": 0}, booknames={"i_l1": "i_1(0)", "i_l2": "i_2(0)"},
        note="This is the circuit with the switch closed, run in DC to find the two "
             "inductor currents, which the next entry takes as its initial conditions.")],
     desc="e,1,0,100:r1,1,2,10:l1,2,3,3,10:r2,3,4,15:l2,4,0,2,0",
     expect={"v_3": "12*DiracDelta(t) + 60 + 10*exp(-5*t)",
             "i_l1": "4 + 2*exp(-5*t)"},
     booknames={"v_3": "v_o", "i_l1": "i_1"},
     after="The $\\delta(t)$ in $v_o$ is an impulse. Opening the switch puts the two "
           "inductors in series, one carrying 10 A and the other none, and they must "
           "carry the same current from then on; an inductor's current cannot jump without "
           "an impulse of voltage across it, and the weight of this one, 12, is what it "
           "takes to bring $L_2$'s current from 0 to the 6 A the pair settle on.",
     shows="Opening the switch removes that wire, so the two inductors are now in series "
           "with the 15 Ω between them. We describe that circuit with the 10 A and 0 just "
           "found as their fifth fields, numbering the nodes 1 to 4 from the source. The "
           "output voltage $v_o$ is then the voltage at node 3, the top of the 15 Ω and "
           "$L_2$, and $i_1$ is the current through `l1`. We set the analysis to TR."),
]

SPECS += [
dict(num="3.10", title="Using a Wheatstone Bridge to Measure Resistance",
     ask="For the Wheatstone bridge in Fig. 3.30, $R_3$ can be varied from 10 Ω to 2 kΩ. "
         "What range of resistor values can this bridge measure?",
     page=101, fig=(101, "3.30"), domain="dc",
     desc="e,1,0,V_s:r1,1,a,1'k:r2,1,b,4'k:sg,a,b:r3,a,0,R_3:rx,b,0,R_x",
     expect={},
     solveq=[
      dict(tag="DC, Solve at R_3 = 10",
           text="With the results on screen, we open the {{card:Solve}} card under them "
                "and ask the question the way the bridge is used. The balance condition, "
                "no current through the galvanometer, is the equation `isg=0`; the "
                "resistance we want is the unknown, `R_x`; and the setting of the dial is "
                "a condition, first at its lowest, 10 Ω:",
           equations=["isg=0"], unknowns=["R_x"], conditions=["R_3=10"],
           real_only=True, expect={"R_x": 40}, unit="\\Omega", book={"R_x": "R_x"}),
      dict(tag="DC, Solve at R_3 = 2k", entry=False, boxes=("conditions",),
           text="For the other end of the dial we keep the equation and the unknown as "
                "they are and change only the condition, to the highest setting, 2 kΩ, "
                "written with the usual shorthand:",
           press="Then press {{btn:Solve equations}} again.",
           equations=["isg=0"], unknowns=["R_x"], conditions=["R_3=2'k"],
           real_only=True, expect={"R_x": 8000}, unit="\\Omega", book={"R_x": "R_x"}),
     ],
     after="So the smallest resistance the bridge can measure is {{o:40}} Ω and the "
           "largest {{o:8000}} Ω: its range is 40 Ω to 8 kΩ.",
     shows="A Wheatstone bridge measures a resistance nobody knows, $R_x$, by comparing it "
           "with resistances that are known. The adjustable resistor $R_3$ is turned until "
           "the galvanometer between the two arms of the bridge carries no current, and at "
           "that setting the unknown can be read off the others. So we describe the "
           "circuit with the two resistances the question leaves open as symbols rather "
           "than numbers, which we name `R_3` for the adjustable one and `R_x` for the "
           "unknown, after the book's; we name the two known resistors `r1` and `r2`, and "
           "call the two arms' midpoints **a** and **b**. We describe the galvanometer as "
           "a short circuit, the element `s`, which we name `sg`: the figure gives it no "
           "resistance, and what we will need from it is its current, which a short "
           "reports as `isg`. We leave the source as a symbol too, `V_s`, since its value "
           "plays no part at balance. We run this as it stands, in DC, and every answer "
           "comes back as a formula in the three symbols."),

dict(num="14.6", title="Designing a Parallel RLC Bandpass Filter",
     ask="a) Show that the RLC circuit in Fig. 14.22 is a bandpass filter by deriving an "
         "expression for the transfer function $H(s)$. b) Compute the centre frequency. "
         "c) Calculate the cutoff frequencies, the bandwidth and $Q$. d) Compute $R$ and $L$ "
         "for a centre frequency of 5 kHz and a bandwidth of 200 Hz, using a 5 µF capacitor.",
     page=581, fig=(581, "14.22"), domain="fd",
     desc="e,1,0,vi:rr,1,2,R:c,2,0,C:l,2,0,L",
     expect={"@v_2/vi": "(s/(C*R))/(s**2 + s/(C*R) + 1/(L*C))"},
     labels={"@v_2/vi": "transfer function"},
     texnames={"@v_2/vi": "H(s) = \\dfrac{v_{2}}{v_{i}}"},
     units={"@v_2/vi": ""},
     after="Dividing numerator and denominator by $RLC$ puts it in the standard form "
           "$H(s) = \\dfrac{s/RC}{s^2 + s/RC + 1/LC}$, which is a bandpass, part (a). "
           "Part (b): the centre frequency is $\\omega_0 = 1/\\sqrt{LC}$. Part (c): the "
           "bandwidth is $\\beta = 1/RC$, the cutoff frequencies are $\\omega_{c} = "
           "\\mp\\beta/2 + \\sqrt{(\\beta/2)^2 + \\omega_0^2}$, and $Q = \\omega_0/\\beta$. "
           "Part (d): with $C$ = 5 µF, a centre frequency of 5 kHz is $\\omega_0$ = "
           "2π × 5000 rad/s, so $L = 1/(\\omega_0^2 C)$ = {{o:202.6}} µH, and a bandwidth of "
           "200 Hz is $\\beta$ = 2π × 200 rad/s, so $R = 1/(\\beta C)$ = {{o:159.2}} Ω.",
     shows="Nothing in this question is a number until part (d), so we leave the three "
           "elements as the symbols `R`, `L` and `C` and the source as `vi`, naming the "
           "resistor `rr` to keep its name apart from its value; we set the analysis to "
           "FD, and the transfer function is the output voltage, at node 2, divided by the "
           "input, which we type into {{card:Evaluate}} as `v_2/vi`. The run returns it in "
           "terms of the three symbols, and parts (a) to (d) are read off that one "
           "expression."),

dict(num="18.1", title="Finding the z Parameters of a Two-Port Circuit",
     ask="Find the z parameters for the circuit shown in Fig. 18.3.",
     page=724, fig=(724, "18.3"), kind="port", n1="1", n2="2", ptype="z", domain="dc",
     desc="r5,1,2,5:r20,1,0,20:r15,2,0,15",
     expect={"11": 10, "12": 7.5, "21": 7.5, "22": 9.375},
     shownames={"11": "z11", "12": "z12", "21": "z21", "22": "z22"},
     booknames={"11": "z_{11}", "12": "z_{12}", "21": "z_{21}", "22": "z_{22}"},
     shows="A two-port is a circuit seen from two pairs of terminals, and its z parameters "
           "are the four numbers that relate the two voltages to the two currents at those "
           "pairs. We take port 1 as node **1** with ground and port 2 as node **2** with "
           "ground, write the three resistors between those nodes, naming each after its "
           "value, and name the two ports to the {{card:Find equivalent}} card with "
           "*Two-port parameters* chosen and the kind set to **z**; it returns the four "
           "parameters, named `z11` to `z22`."),

dict(num="18.6", title="Analyzing Cascaded Two-Port Circuits",
     ask="Two identical amplifiers are connected in cascade. Each is described by its h "
         "parameters: $h_{11}$ = 1000 Ω, $h_{12}$ = 0.0015, $h_{21}$ = 100, $h_{22}$ = "
         "100 µS. The source has 500 Ω of internal resistance and the load is 10 kΩ. Find "
         "the voltage gain $V_2/V_g$.",
     page=738, fig=(738, "18.14"), domain="dc",
     desc="e,1,0,vg:rs,1,a,500:h1,a,b,[1000,0.0015,100,0.0001]:"
          "h2,b,c,[1000,0.0015,100,0.0001]:rl,c,0,10'k",
     shownames={"@v_c/vg": "v_c/vg"}, units={"@v_c/vg": ""},
     booknames={"@v_c/vg": "V_2/V_g"},
     expect={"@v_c/vg": 33333.33},
     shows="A two-port that is known only by its parameters is an element of its own. "
           "Since these are h parameters we use the element `h`, and write the four values "
           "after the two nodes as a bracketed term, `[1000,0.0015,100,0.0001]`, the "
           "100 µS written as 0.0001. We write the two amplifiers in cascade as two such "
           "lines, `h1` and `h2`, sharing a node we call **b**, between the source's 500 Ω "
           "and the 10 kΩ load; we leave the source as the symbol `vg`, so that the "
           "output comes back as a multiple of it, and the gain asked for is that "
           "multiple, which we type into {{card:Evaluate}} as `v_c/vg`."),
]
