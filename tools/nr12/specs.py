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
  num      the book's example number
  title    the book's example title
  ask      the statement, as the book words the question
  page     PDF page the example starts on
  fig      (page, figure-number) for the schematic crop
  desc     the Symbulator circuit description (colon form)
  domain   dc | ac | tr | fd      kind: circuit (default) | th | port
  expect   book answer -> Symbulator answer name  ("@expr" = evaluate an expression)
  shows    what the entry is in the sampler for
  parts    (letter, text) -- a lettered part answered in prose, after the results

Prose conventions (gen.polish applies the house typography to `ask`, `shows`
and `parts`):
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
     shows="Symbulator solves the whole circuit at once and both answers are among the "
           "results."),

dict(num="3.11", title="Applying a Delta-to-Wye Transform",
     ask="Find the current and power supplied by the 40 V source in the circuit shown in Fig. 3.35.",
     page=103, fig=(103, "3.35"), domain="dc",
     desc="e,1,0,40:r1,1,2,5:r2,2,3,100:r3,2,4,125:r4,3,4,25:r5,3,0,40:r6,4,0,37.5",
     expect={"@-i_e": 0.5, "@-p_e": 20, "r_e": 80},
     shownames={"@-i_e": "-i_e", "@-p_e": "-p_e"},
     shows="Series and parallel steps cannot reduce this bridge, so the book converts one "
           "delta of resistors to a wye first and then collapses what is left to a single "
           "80 Ω. Symbulator takes the six resistors as they stand. One thing to read "
           "carefully: the book asks for the current and power the source *supplies*, and "
           "Symbulator reports what every element *consumes*, so the book's two answers are "
           "the negatives of `i_e` and `p_e` — 0.5 A and 20 W. The 80 Ω the transform was "
           "for is reported as `r_e`, the resistance seen by the source."),

dict(num="4.4", title="Using the Node-Voltage Method with Dependent Sources",
     ask="Use the node-voltage method to find the power dissipated in the 5 Ω resistor "
         "in the circuit shown in Fig. 4.10.",
     page=125, fig=(125, "4.10"), domain="dc",
     desc="e,1,0,20:r1,1,2,2:r2,2,0,20:r3,2,3,5:r4,3,0,10:r5,3,4,2:e2,4,0,8*ir3",
     expect={"v_2": 16, "v_3": 10, "i_r3": 1.2, "p_r3": 7.2},
     shows="The dependent source here is a voltage source worth eight times a current "
           "elsewhere in the circuit. The book writes two node equations, finds it has three "
           "unknowns, and adds a constraint equation expressing the controlling current in "
           "terms of the node voltages. In Symbulator the controlling current is simply "
           "named: `e2` is worth `8*ir3`, where `ir3` is the current through the 5 Ω "
           "resistor, and there is no constraint equation to write or to get wrong. The "
           "power the book asks for is `p_r3`."),

dict(num="4.7", title="Using the Mesh-Current Method with Dependent Sources",
     ask="Use the mesh-current method to find the power dissipated in the 4 Ω resistor "
         "in the circuit shown in Fig. 4.23.",
     page=133, fig=(133, "4.23"), domain="dc",
     desc="e,1,0,50:r1,1,3,1:r2,1,2,5:r3,2,3,4:r4,2,0,20:e2,3,0,15*ir4",
     expect={"i_r4": 1.6, "i_r3": 2, "p_r3": 16},
     shows="The same idea with mesh currents: the book writes two mesh equations and a "
           "third for the dependent source's controlling current, expressed as a difference "
           "of mesh currents. The description is the six lines it would be without the "
           "dependent source, except that `e2` is worth `15*ir4`. Symbulator is told the "
           "circuit and never the method, so nothing here says *mesh*. The power in the "
           "4 Ω resistor is `p_r3`."),

dict(num="4.21", title="Calculating the Condition for Maximum Power Transfer",
     ask="a) For the circuit shown in Fig. 4.65, find the value of $R_L$ that results in "
         "maximum power being transferred to $R_L$. b) Calculate the maximum power that can "
         "be delivered to $R_L$.",
     page=153, fig=(153, "4.65"), kind="th", n1="2", n2="0", domain="dc",
     desc="e,1,0,360:r1,1,2,30:r2,2,0,150",
     expect={"vth": 300, "z": 25, "pmax": 900},
     shows="The book finds the Thévenin equivalent at the load's terminals, because the "
           "load that draws the most power is the one equal to the Thévenin resistance, and "
           "the maximum is then $V_{Th}^2 / 4R_{Th}$. The Thévenin tool does the same in "
           "one run: `z` is the Thévenin resistance and so the load for part (a), and "
           "`pmax` is the power that load draws, part (b). The book's part (c), which asks "
           "what fraction of the source's power reaches that load, is one more DC run with "
           "`rl,2,0,25` added to the description: 900 W of 2520 W, or 35.7%."),
]

SPECS += [
dict(num="4.8", title="A Special Case in the Mesh-Current Method",
     ask="Use the mesh-current method to find branch currents $i_a$, $i_b$ and $i_c$ "
         "in the circuit for Example 4.3, repeated here as Fig. 4.25.",
     page=134, fig=(134, "4.25"), domain="dc",
     desc="e,1,0,50:r1,1,2,5:r2,2,0,10:r3,2,0,40:j,0,2,3",
     expect={"i_r1": 2, "i_r2": 4, "i_r3": 1, "v_2": 40},
     shows="The book's special case is a current source in a branch shared by two meshes, "
           "whose voltage is unknown, so no KVL equation can be written around either mesh "
           "alone. The book's answer is the *supermesh*: merge the two meshes, write KVL "
           "around the outside of the pair, and add the constraint the source imposes. "
           "Symbulator has no meshes, so there is no special case: the current source `j` "
           "is one more line. The book's three branch currents are `i_r1`, `i_r2` and "
           "`i_r3`."),

dict(num="4.13", title="Using Special Source Transformation Techniques",
     ask="a) Use source transformations to find the voltage $v_o$ in the circuit shown in "
         "Fig. 4.42. b) Find the power developed by the 250 V voltage source. "
         "c) Find the power developed by the 8 A current source.",
     page=143, fig=(143, "4.42"), domain="dc",
     desc="e,1,0,250:r1,1,0,125:r2,1,2,25:j,2,9,8:r3,9,0,10:r4,2,0,100:r5,2,3,5:r6,3,0,15",
     expect={"v_r4": 20, "@-i_e": 11.2, "@-p_e": 2800, "@-p_j": 480},
     shownames={"@-i_e": "-i_e", "@-p_e": "-p_e", "@-p_j": "-p_j"},
     shows="The *special* techniques are two: a resistor in parallel with a voltage source, "
           "and one in series with a current source, have no effect on the rest of the "
           "circuit, so the book removes them, transforms the sources that remain, and finds "
           "$v_o$ from a single loop. Then it has to put those resistors back, because they "
           "do affect what the sources deliver, which is parts (b) and (c). Symbulator "
           "solves the circuit as drawn, so nothing is removed and nothing has to be "
           "restored. The book's $v_o$ is `v_r4`; the powers *developed* by the two sources "
           "are the negatives of what Symbulator reports them consuming, `-p_e` and `-p_j`, "
           "and `-i_e` is the current the 250 V source delivers."),

dict(num="4.23", title="Using Superposition to Solve a Circuit with Dependent Sources",
     ask="Use the principle of superposition to find $v_o$ in the circuit shown in Fig. 4.71.",
     page=156, fig=(156, "4.71"), domain="dc",
     desc="e,1,c,10:r1,1,a,5:r2,a,c,20:r3,b,0,10:j1,0,b,5:j2,b,a,0.4*vr3:e2,0,c,2*ir1",
     expect={"v_r2": 24, "v_r3": 10, "i_r1": -2.8},
     shows="Superposition is a way of getting an answer by hand — solve once for each "
           "independent source with the others switched off, then add — and it is not a "
           "property of the answer. Symbulator never uses it. The two dependent sources, "
           "`j2` worth `0.4*vr3` and `e2` worth `2*ir1`, stay in the circuit throughout, "
           "exactly as they must in each of the book's two partial solutions, and the two "
           "independent sources are solved together. The book's $v_o$ is `v_r2`."),

dict(num="5.1", title="Analyzing an Op Amp Circuit",
     ask="The op amp in the circuit shown in Fig. 5.7 is ideal. a) Calculate $v_o$ if "
         "$v_a$ = 1 V and $v_b$ = 0 V. b) Repeat (a) for $v_a$ = 1 V and $v_b$ = 2 V. "
         "c) If $v_a$ = 1.5 V, specify the range of $v_b$ that avoids amplifier saturation.",
     page=181, fig=(181, "5.7"), domain="dc",
     desc="ea,1,0,va:r1,1,2,25'k:r2,2,3,100'k:eb,4,0,vb:o,4,2,3",
     expect={"v_3": "5*vb - 4*va"},
     parts=[
      ("a", "With {{var:v_a}} = 1 V and {{var:v_b}} = 0 V the formula gives "
            "{{var:v_o}} = 5(0) − 4(1) = {{o:-4}} V. That is inside the ±10 V "
            "supplies, so the op amp is in its linear region and −4 V is the "
            "answer."),
      ("b", "With {{var:v_a}} = 1 V and {{var:v_b}} = 2 V, {{var:v_o}} = "
            "5(2) − 4(1) = {{o:6}} V. Inside the supplies again, so the op "
            "amp is still linear."),
      ("c", "With {{var:v_a}} = 1.5 V the formula becomes {{var:v_o}} = "
            "5{{var:v_b}} − 6. The op amp stays linear while that lies "
            "between the rails, so Symbulator is asked the question directly: "
            "put `v_3 = 10` in {{card:Expert Mode}} with `vb` as the "
            "unknown, then again with `v_3 = -10`. The rails are reached at "
            "{{var:v_b}} = {{o:3.2}} V and {{var:v_b}} = {{o:-0.8}} V, so "
            "the range is {{o:-0.8}} V ≤ {{var:v_b}} ≤ {{o:3.2}} V."),
     ],
     shows="An ideal op amp does not know its supplies exist. Symbulator's `o` element "
           "reports whatever output the inputs demand, 200 V as readily as 2 V, so "
           "saturation is a question you ask of the answer rather than something the solve "
           "enforces. With both inputs left as the symbols `va` and `vb`, one run returns "
           "the output as a formula, and each part of the question is read off it; the "
           "supplies in the figure are ±10 V, which is what part (c) checks against."),
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
     parts=[
      ("a", "The summing-amplifier formula is {{var:v_o}} = "
            "−({{var:R_f}}/{{var:R_a}}){{var:v_a}} − "
            "({{var:R_f}}/{{var:R_b}}){{var:v_b}} − "
            "({{var:R_f}}/{{var:R_c}}){{var:v_c}}, so with a 20 kΩ "
            "feedback resistor the three input resistors are "
            "{{var:R_a}} = 20k/4 = {{o:5}} kΩ, {{var:R_b}} = 20k/1 = "
            "{{o:20}} kΩ and {{var:R_c}} = 20k/5 = {{o:4}} kΩ. "
            "Running that circuit returns the very formula the design was "
            "asked to hit, which is the check."),
      ("b", "With {{var:v_a}} = 2 V and {{var:v_c}} = −1 V the output "
            "collapses to {{var:v_o}} = −{{var:v_b}} − 3. Asking "
            "{{card:Expert Mode}} for the {{var:v_b}} that puts `v_4` on "
            "each rail gives {{o:9}} V at −12 V and {{o:-15}} V at +12 V, so "
            "the op amp stays linear for {{o:-15}} V ≤ {{var:v_b}} "
            "≤ {{o:9}} V."),
     ],
     shows="A design problem, so the run is a check rather than a solve. The book's "
           "summing-amplifier formula gives each input resistor from its gain and the "
           "feedback resistor; the circuit built from those values is then run with its "
           "three inputs as symbols, and the output comes back as exactly the formula the "
           "design was asked to produce. Part (b) asks for the range of one input that keeps "
           "the output between the ±12 V rails, which is a question for {{card:Expert Mode}}: "
           "set the output equal to a rail and ask for the input."),

dict(num="5.3c", title="Designing a Summing Amplifier - part (c), in Expert Mode",
     ask="c) Suppose $v_a$ = 2 V, $v_b$ = 3 V and $v_c$ = $-$1 V. Using the input resistor "
         "values found in part (a), how large can the feedback resistor be before the op amp "
         "saturates?",
     page=185, fig=(185, "5.12"), domain="dc",
     desc="ea,1,0,2:eb,2,0,3:ec,3,0,-1:r1,1,n,5'k:r2,2,n,20'k:r3,3,n,4'k:rf,n,4,rf:o,0,n,4",
     equations=["v_4 = -12"], unknowns=["rf"],
     expect={"rf": 40000}, units={"rf": "\\Omega"},
     parts=[
      ("c", "With {{var:v_a}} = 2 V, {{var:v_b}} = 3 V and {{var:v_c}} = "
            "−1 V the three input currents sum to a positive number, so the "
            "output swings negative and it is the −12 V rail that is reached "
            "first. Leave the feedback resistor as the symbol `rf`, put "
            "`v_4 = -12` in {{card:Expert Mode}} and name `rf` the unknown: "
            "the answer is {{o:40}} kΩ. Any larger and the op amp "
            "saturates."),
     ],
     shows="Part (c) turns the same circuit into a different kind of question. The inputs "
           "are now numbers, the feedback resistor is the unknown, and what is known is an "
           "answer: the output sits on the −12 V rail. That is what {{card:Expert Mode}} is "
           "for — `v_4 = -12` is the equation, `rf` the unknown, and the solve returns the "
           "resistor. It is one of two examples on this page whose answer is a component "
           "value; the Wheatstone bridge above is the other."),

dict(num="5.5", title="Designing a Difference Amplifier",
     ask="a) Design a difference amplifier that amplifies the difference between two input "
         "voltages by a gain of 8, using an ideal op amp and ±8 V power supplies. "
         "b) Suppose $v_a$ = 1 V. What range of $v_b$ keeps the op amp linear?",
     page=189, fig=(189, "5.16"), domain="dc",
     desc="ea,1,0,va:eb,2,0,vb:ra,1,n,1.5'k:rb,n,3,12'k:rc,2,p,1.5'k:rd,p,0,12'k:o,p,n,3",
     expect={"v_3": "8*vb - 8*va"},
     parts=[
      ("a", "The simplified difference-amplifier formula is {{var:v_o}} = "
            "({{var:R_b}}/{{var:R_a}})({{var:v_b}} − {{var:v_a}}), so a gain "
            "of 8 wants two resistors in the ratio 8: "
            "{{var:R_a}} = {{var:R_c}} = {{o:1.5}} kΩ and "
            "{{var:R_b}} = {{var:R_d}} = {{o:12}} kΩ. The formula also "
            "requires {{var:R_a}}/{{var:R_b}} = {{var:R_c}}/{{var:R_d}}, "
            "which those four satisfy. The run returns exactly "
            "8({{var:v_b}} − {{var:v_a}})."),
      ("b", "With {{var:v_a}} = 1 V the output is {{var:v_o}} = "
            "8{{var:v_b}} − 8, which reaches +8 V at {{var:v_b}} = {{o:2}} V "
            "and −8 V at {{var:v_b}} = {{o:0}} V. So the op amp remains in "
            "its linear region for {{o:0}} V ≤ {{var:v_b}} ≤ "
            "{{o:2}} V."),
     ],
     shows="A difference amplifier with a gain of 8 needs two resistor ratios to be equal, "
           "and the book picks 1.5 kΩ and 12 kΩ. Run with both inputs as symbols, the "
           "circuit returns exactly $8(v_b - v_a)$, which confirms the design; part (b)'s "
           "range then follows from that one line by setting the output to each ±8 V rail "
           "in turn."),

dict(num="5.7", title="Analyzing a Noninverting-Amplifier Circuit Using a Realistic Op Amp Model",
     ask="Analyze the noninverting amplifier of Example 5.4 using the realistic op amp model, "
         "with open-loop gain $A$ = 50,000, input resistance $R_i$ = 100 kΩ and output "
         "resistance $R_o$ = 7.5 kΩ; there is no load resistance at the output. Find the "
         "gain $v_o/v_g$.",
     page=195, fig=(195, "5.21"), domain="dc",
     desc="eg,1,0,vg:rg,1,p,1'k:ri,p,n,100'k:rs,n,0,2'k:rf,n,3,10'k:ro,4,3,7.5'k:"
          "ea,4,0,50000*(vp-vn)",
     shownames={"@v_3/vg": "v_3/vg"}, units={"@v_3/vg": ""},
     expect={"@v_3/vg": 5.9988}, tol=2e-5,
     shows="There is no `o` element here. The book's realistic op amp model is a dependent "
           "voltage source with a gain of 50,000, an input resistance between its two "
           "inputs and an output resistance in series with its output, and that is what the "
           "description says: `ea` is worth `50000*(vp-vn)`, `ri` sits between nodes **p** "
           "and **n**, and `ro` is at the output. The gain, the output node's voltage divided "
           "by the symbolic source, comes out as 5.9988 against the 6 an ideal op amp would "
           "give — and that small shortfall is the whole point of the example."),

dict(num="7.1", title="Determining the Natural Response of an RL Circuit",
     ask="The switch in the circuit shown in Fig. 7.6 has been closed for a long time before "
         "it is opened at $t$ = 0. Find a) $i_L(t)$ for $t$ ≥ 0, b) $i_o(t)$ for "
         "$t$ ≥ 0+, c) $v_o(t)$ for $t$ ≥ 0+.",
     page=250, fig=(250, "7.6"), domain="tr",
     desc="l,1,0,2,20:r1,1,2,2:r2,2,0,10:r3,2,0,40",
     expect={"i_l": "20*exp(-5*t)", "i_r3": "-4*exp(-5*t)", "v_2": "-160*exp(-5*t)"},
     shows="A switched circuit is two circuits, and two runs. With the switch closed for a "
           "long time the inductor is a short across the 20 A source, and a DC run of that "
           "circuit gives its current, 20 A. That number goes into the inductor's fifth "
           "field, its initial current, and the circuit that exists once the switch has "
           "opened is run in TR. No time constant is ever computed. The book's $i_L$ is "
           "`i_l`, its $i_o$ the current through `r3`, and its $v_o$ the voltage at node 2."),
]

SPECS += [
dict(num="7.3", title="Determining the Natural Response of an RC Circuit",
     ask="The switch in the circuit shown in Fig. 7.15 has been in position x for a long "
         "time. At $t$ = 0 it moves instantaneously to position y. Find a) $v_C(t)$ for "
         "$t$ ≥ 0, b) $v_o(t)$ for $t$ ≥ 0+, and c) $i_o(t)$ for $t$ ≥ 0+.",
     page=256, fig=(256, "7.15"), domain="tr",
     desc="c,1,0,0.5'u,100:r1,1,2,32'k:r2,2,0,240'k:r3,2,0,60'k",
     expect={"v_1": "100*exp(-25*t)", "v_2": "60*exp(-25*t)",
             "i_r3": "0.001*exp(-25*t)"},
     shows="The RC twin of the example above. Before the switch moves the capacitor has "
           "charged to the 100 V of the source, and that is the fifth field of the `c` "
           "line; the three answers come back as functions of $t$ sharing the one time "
           "constant, 40 ms, that the book computes from the equivalent resistance. The "
           "book's $v_C$ is the voltage at node 1, its $v_o$ the voltage at node 2 and its "
           "$i_o$ the current through `r3`."),

dict(num="7.5", title="Determining the Step Response of an RL Circuit",
     ask="The switch in the circuit shown in Fig. 7.21 has been in position a for a long "
         "time. At $t$ = 0 it moves from position a to position b. The switch is a "
         "make-before-break type, so the inductor current is continuous. a) Find the "
         "expression for $i(t)$ for $t$ ≥ 0. b) What is the initial voltage across the "
         "inductor just after the switch has been moved to position b?",
     page=260, fig=(260, "7.21"), domain="tr",
     desc="e,1,0,24:r1,1,2,2:l,2,0,0.2,-8",
     expect={"i_l": "12 - 20*exp(-10*t)", "v_2": "40*exp(-10*t)"},
     shows="A step response whose starting current is neither zero nor in the direction "
           "the step will drive it: before the switch moves, the 8 A source was pushing "
           "current through the inductor the other way, so the inductor's fifth field reads "
           "−8. The book's point that the switch is make-before-break is what makes the "
           "inductor current continuous across the switching, and so what makes it "
           "meaningful to give an initial current at all. Part (b), the inductor voltage "
           "just after the switch moves, is `v_2` at $t$ = 0: 40 V."),

dict(num="7.10", title="Determining the Step Response of a Circuit with Magnetically Coupled Coils",
     ask="There is no energy stored in the circuit in Fig. 7.37 at the time the switch is "
         "closed. Find the solutions for $i_o$, $v_o$, $i_1$ and $i_2$.",
     page=271, fig=(271, "7.37"), domain="tr",
     desc="e,1,0,120:r1,1,2,7.5:l1,2,0,3:l2,2,0,15:m,l1,l2,6",
     expect={"i_r1": "16 - 16*exp(-5*t)", "v_2": "120*exp(-5*t)",
             "i_l1": "24 - 24*exp(-5*t)", "i_l2": "-8 + 8*exp(-5*t)"},
     shows="Two coils on one core, both fed from the same node. The book replaces the "
           "coupled pair by a single equivalent inductance of 1.5 H, solves the RL circuit "
           "that leaves, and then works back to the two coil currents through the "
           "coupled-coil voltage equations. Here the coupling is the one `m` line, naming "
           "the two coils and their mutual inductance, and the two coil currents come back "
           "on their own beside the total. The book's $i_o$ is `i_r1`, its $v_o$ the voltage "
           "at node 2, and $i_1$ and $i_2$ are the currents through `l1` and `l2`."),

dict(num="7.11a", title="Analyzing an RL Circuit That Has Sequential Switching (0 to 35 ms)",
     ask="The two switches in the circuit shown in Fig. 7.39 have been closed for a long "
         "time. At $t$ = 0 switch 1 is opened; then, 35 ms later, switch 2 is opened. "
         "a) Find $i_L(t)$ for 0 ≤ $t$ ≤ 35 ms.",
     page=273, fig=(273, "7.39"), domain="tr",
     desc="r6,2,0,6:r3,2,3,3:l,3,0,0.15,6:r18,3,0,18",
     expect={"i_l": "6*exp(-40*t)"},
     shows="Sequential switching is not a new kind of problem, only more runs. A DC run of "
           "the circuit with both switches closed gives the inductor current before anything "
           "happens, 6 A, and that is the fifth field here. The description is the circuit "
           "that exists after switch 1 has opened, and its answer holds until switch 2 opens "
           "at 35 ms."),

dict(num="7.11b", title="Analyzing an RL Circuit That Has Sequential Switching (after 35 ms)",
     ask="b) Find $i_L(t)$ for $t$ ≥ 35 ms. (Time is measured from the second switching.)",
     page=273, fig=(273, "7.39"), domain="tr",
     desc="r6,2,0,6:r3,2,3,3:l,3,0,0.15,1.47961",
     expect={"i_l": "1.47961*exp(-60*t)"},
     shows="The third run. Switch 2 has removed the 18 Ω resistor, so the inductor now "
           "sees the 6 Ω and 3 Ω in series, 9 Ω, and the time constant changes. Its "
           "starting current is whatever the previous run left at 35 ms — `6*exp(-40*0.035)`, "
           "1.48 A — and time is measured from the second switching, as the book measures "
           "it too."),

dict(num="7.13", title="Finding the Unbounded Response in an RC Circuit",
     ask="a) When the switch is closed in the circuit shown in Fig. 7.45, the voltage on the "
         "capacitor is 10 V. Find the expression for $v_o$ for $t$ ≥ 0. b) Assume that the "
         "capacitor short-circuits when its terminal voltage reaches 150 V. How many "
         "milliseconds elapse before the capacitor short-circuits?",
     page=277, fig=(277, "7.45"), domain="tr",
     desc="c,1,0,5'u,10:r1,1,0,10'k:r2,1,0,20'k:j,0,1,7*ir2",
     expect={"v_1": "10*exp(40*t)"},
     shows="A dependent current source makes the resistance the capacitor sees negative, "
           "−5 kΩ, so the voltage grows instead of decaying. The book finds that Thévenin "
           "resistance first and then solves a differential equation whose exponent turns "
           "out positive. Here nothing has to be told the case is different: the dependent "
           "source is `7*ir2`, and the exponent comes back positive of its own accord. Part "
           "(b) is read off the answer — $10e^{40t}$ reaches 150 V when $40t = \\ln 15$, "
           "at 67.7 ms."),

dict(num="8.2", title="Finding the Overdamped Natural Response of a Parallel RLC Circuit",
     ask="For the circuit in Fig. 8.6, $v(0^+)$ = 12 V and $i_L(0^+)$ = 30 mA. Find the "
         "expression for $v(t)$. (Example 8.3 asks the same circuit for its three branch "
         "currents.)",
     page=306, fig=(306, "8.6"), domain="tr",
     desc="c,1,0,0.2'u,12:l,1,0,50'm,0.03:r,1,0,200",
     expect={"v_1": "-14*exp(-5000*t) + 26*exp(-20000*t)",
             "i_r": "-0.07*exp(-5000*t) + 0.13*exp(-20000*t)",
             "i_l": "0.056*exp(-5000*t) - 0.026*exp(-20000*t)"},
     shows="The book's parallel RLC has three cases — overdamped, critically damped, "
           "underdamped — and three solution forms, so it compares $\\alpha$ with "
           "$\\omega_0$ to pick one before it can write anything down. Symbulator writes "
           "nothing down: the three elements with their two initial conditions are run in "
           "TR, and the two real exponents of the overdamped case come out of the algebra. "
           "Example 8.3's branch currents are in the same run — `i_r` and `i_l` below, and "
           "`i_c` in the app."),

dict(num="8.4", title="Finding the Underdamped Natural Response of a Parallel RLC Circuit",
     ask="In the circuit shown in Fig. 8.8, $V_0$ = 0 and $I_0$ = $-$12.25 mA. Calculate "
         "the voltage response for $t$ ≥ 0.",
     page=310, fig=(310, "8.8"), domain="tr", at_t=[1e-4, 5e-4, 1e-3, 3e-3],
     desc="c,1,0,125'n,0:l,1,0,8,-0.01225:r,1,0,20'k",
     expect={"v_1": "100*exp(-200*t)*sin(979.80*t)"}, tol=3e-4,
     shows="The same three lines with different values, and the underdamped case comes "
           "out: a damped sine, with the damping in the exponent and the damped frequency "
           "in the argument. The book needs a different row of its table and a different "
           "pair of constants to fit; the description does not change shape at all. The "
           "book prints the amplitude as 100 and the frequency as 979.80, both rounded; "
           "the app's answer, at six digits, shows 100.021 and 979.796 for the same "
           "expression."),

dict(num="8.11", title="Finding the Natural Response of a Series RLC Circuit",
     ask="The 0.1 µF capacitor in the circuit shown in Fig. 8.17 is charged to 100 V. At "
         "$t$ = 0 the capacitor is discharged through a series combination of a 100 mH "
         "inductor and a 560 Ω resistor. a) Find $i(t)$ for $t$ ≥ 0. b) Find $v_C(t)$ for "
         "$t$ ≥ 0.",
     page=328, fig=(328, "8.17"), domain="tr",
     desc="c,1,0,0.1'u,100:l,2,1,0.1:r,2,0,560",
     expect={"i_l": "-0.1042*exp(-2800*t)*sin(9600*t)"}, at_t=[3e-5, 1e-4, 3e-4], tol=1e-3,
     shows="Series rather than parallel, and again no case is chosen by anyone: the "
           "capacitor discharges through the inductor and resistor and the underdamped form "
           "arrives. One detail of the description is deliberate. The inductor's nodes are "
           "written 2 then 1 so that `i_l` is measured in the direction of the book's arrow "
           "for $i$; written the other way round, the answer comes back with the opposite "
           "sign. Part (b), $v_C$, is the voltage at node 1."),

dict(num="8.12", title="Finding the Step Response of a Series RLC Circuit",
     ask="No energy is stored in the 100 mH inductor or the 0.4 µF capacitor when the switch "
         "in the circuit shown in Fig. 8.18 is closed. Find $v_C(t)$ for $t$ ≥ 0.",
     page=328, fig=(328, "8.18"), domain="tr",
     desc="e,1,0,48:l,1,2,0.1:r,2,3,1250:c,3,0,0.4'u",
     expect={"v_3": "48 + 16*exp(-10000*t) - 64*exp(-2500*t)"},
     shows="A step into a series RLC with no stored energy. The book finds the two roots, "
           "recognises the overdamped form, and fits its two constants to the initial "
           "conditions; here the final value of 48 V, the two roots and both coefficients "
           "arrive together in one expression. The book's $v_C$ is the voltage at node 3."),
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
     shows="Henries and farads go in as the book gives them, and the frequency goes in the "
           "{{ui:ω — angular frequency}} box; the solver turns the 40 µH into $+j8$ Ω and "
           "the 1 µF into $-j5$ Ω at "
           "200,000 rad/s, which is the book's part (a), the frequency-domain equivalent "
           "circuit. The book's $V$ is `v_1` and its $I$ the current through `r2`, and "
           "part (e) is a matter of reading each phasor as an amplitude and an angle, which "
           "the app prints beside the rectangular form: 40 V at −36.87° and 4 A at −90°."),

dict(num="9.10", title="Using a Delta-to-Wye Transform in the Frequency Domain",
     ask="Use a delta-to-wye impedance transformation to find $I_0$, $I_1$, $I_2$, $I_3$, "
         "$I_4$, $I_5$, $V_1$ and $V_2$ in the circuit in Fig. 9.23.",
     page=365, fig=(365, "9.23"), domain="ac", omega=W,
     desc="e,a,0,120:r1,a,b,-4j:r2,a,c,63.2+2.4j:r3,b,c,10:r4,b,0,20+60j:r5,c,0,-20j",
     shownames={"@-i_e": "-i_e"},
     expect={"@-i_e": 2.4 + 3.2j, "i_r1": 2 + _sp.Rational(8, 3) * 1j,
             "i_r3": _sp.Rational(4, 3) + 4.266666666666667j,
             "i_r4": _sp.Rational(2, 3) - 1.6j, "i_r5": _sp.Rational(26, 15) + 4.8j,
             "v_b": _sp.Rational(328, 3) + 8j, "v_c": 96 - _sp.Rational(104, 3) * 1j},
     shows="Every impedance in this circuit is already in ohms, several of them complex, "
           "so they go in exactly as written — `-4j`, `63.2+2.4j`, `20+60j` — and the "
           "frequency never has to be known. The book has to transform a delta to a wye to "
           "reduce the circuit, and then work its way back out to the eight quantities "
           "asked for. The book's $I_0$ is the source current, `-i_e`; its $I_1$ to $I_5$ "
           "are the currents through `r1` to `r5`; and $V_1$ and $V_2$ are the voltages at "
           "nodes **b** and **c**."),

dict(num="9.12", title="Finding a Thevenin Equivalent in the Frequency Domain",
     ask="Find the Thevenin equivalent circuit with respect to terminals a,b for the "
         "circuit shown in Fig. 9.32.",
     page=368, fig=(368, "9.32"), kind="th", n1="9", n2="0", domain="ac", omega=W,
     desc="e,1,0,120:r1,1,2,12:r2,2,0,60:r3,2,9,-40j:e2,3,0,10*v2:r4,3,9,120",
     expect={"vth": 784 - 288j, "z": 91.2 - 38.4j},
     shows="A Thévenin equivalent with a dependent source inside it. The impedance cannot "
           "be found by inspection, because a dependent source cannot be switched off, so "
           "the book applies a test source at the terminals and works out the ratio. The "
           "Thévenin tool handles it as it handles every other circuit, and returns the "
           "voltage and the impedance together. The book's terminals a and b are nodes "
           "**9** and **0**."),

dict(num="9.14", title="Using the Mesh-Current Method in the Frequency Domain",
     ask="Use the mesh-current method to find the voltages $V_1$, $V_2$ and $V_3$ in the "
         "circuit shown in Fig. 9.39.",
     page=372, fig=(372, "9.39"), domain="ac", omega=W,
     desc="e,1,0,150:r1,1,2,1:r2,2,a,2j:r3,a,c,12:r4,c,0,-16j:r5,a,4,1:r6,4,b,3j:"
          "e2,b,0,39*ir3",
     shownames={"@v_1-v_a": "v_1 - v_a", "@v_a-v_b": "v_a - v_b"},
     expect={"@v_1-v_a": 78 - 104j, "v_a": 72 + 104j, "@v_a-v_b": 150 - 130j,
             "i_r3": -2 + 6j},
     shows="The frequency-domain counterpart of Example 4.7 above: two mesh equations, a "
           "dependent source, and a constraint defining its controlling current as a "
           "difference of mesh currents. As in DC, the controlling current is simply named — "
           "`e2` is worth `39*ir3` — and no constraint appears. The book's $V_1$, $V_2$ and "
           "$V_3$ are the drops across three impedances rather than node voltages, so two of "
           "them are printed as differences between node voltages, and the third is the "
           "voltage at node **a** itself."),

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
     shows="The book's question has seven lettered parts, and (b) to (f) — the two "
           "self-impedances, the reflected impedance, its scaling factor, the impedance seen "
           "at the primary — are the steps of its method for reaching (g). Name the load's "
           "two terminals, **c** and **d**, and the Thévenin tool answers (g) outright. Two "
           "details of the description matter. The coils are written as impedances at the "
           "given 400 rad/s — $j3600$, $j1600$ and the mutual $j1200$ — so the coupling "
           "line reads `m,r4,r5,1200j`, with the coupled pair named as `r` elements. And "
           "the secondary is not grounded: its foot is node **d**, a name like any other, "
           "and nothing conducts between the two windings. Symbulator says so in a note and "
           "measures that side against **d**, which leaves its currents, its voltage "
           "differences and the Thévenin equivalent all unaffected. The source is given in "
           "rms, so {{ui:RMS phasors}} is ticked."),
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
     shows="The circuit of Example 9.14, asked a different question. Every element reports "
           "its complex power, `s_r1`, `s_e` and so on, whose real part is the average power "
           "and whose imaginary part the reactive power, so parts (a) and (b) are one run. "
           "Each of the book's impedances is a pair of elements here — its $1 + j2$ Ω is "
           "`r1` and `r2` — so each is the sum of two `s` answers. Part (c), the balance the "
           "book verifies by adding up its own figures, is the sum of all eight, and it is "
           "exactly zero."),

dict(num="10.12", title="Finding Maximum Power Transfer in a Circuit with an Ideal Transformer",
     ask="The variable resistor in the circuit in Fig. 10.25 is adjusted until maximum "
         "average power is delivered to $R_L$. a) What is the value of $R_L$ in ohms? "
         "b) What is the maximum average power delivered to $R_L$?",
     page=423, fig=(423, "10.25"), kind="th", n1="a", n2="0", domain="ac", omega=W, rms=True,
     desc="e,1,0,840:r60,1,p,60:t,[p,x],[x,a],[4,1]:r20,x,0,20",
     expect={"vth": -210, "z": 35, "pmax": 315},
     shows="An ideal transformer whose primary and secondary share a node, which is why "
           "its two ports are written as bracketed terminal pairs, `[p,x]` and `[x,a]`, "
           "with the turns ratio `[4,1]` after them. The book has to work the transformer's "
           "constraint equations twice, once with the load terminals open for the Thévenin "
           "voltage and once shorted for the Norton current, before it can divide one by "
           "the other. The Thévenin tool returns both, and the maximum average power in the "
           "same run: the book's $R_L$ is `z` and the answer to (b) is `pmax`. The source is "
           "given in rms, so {{ui:RMS phasors}} is ticked."),

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
             "@Abs(v_a)": 118.90, "v_nn": 0},
     shows="There is no three-phase mode, and none is needed. The book's part (a) builds a "
           "single-phase equivalent — one generator, one line, one load — because a "
           "balanced circuit can be solved one phase at a time, the other two following by "
           "shifting the angle. Symbulator takes the whole circuit: three sources whose "
           "values carry their phase, `120*exp(-2j*pi/3)` for the b-phase, and three of each "
           "impedance. Every quantity the book derives by shifting is then simply another "
           "answer in the run, and the neutral comes back at exactly zero volts — the "
           "balance the single-phase method assumes, here measured. The book's line current "
           "$I_{aA}$ is `i_rla`; its load phase voltage $V_{AN}$ is the difference between "
           "nodes **pa** and **nn**, its line voltage $V_{AB}$ the difference between **pa** "
           "and **pb**, and its generator phase voltage $V_{An}$ the voltage at node **a**. "
           "Only the magnitudes are quoted for the last three, as the book quotes them."),
]

SPECS += [
dict(num="13.2", title="The Natural Response of an RC Circuit",
     ask="The circuit in Fig. 13.11 was analyzed in Example 7.3 using first-order circuit "
         "analysis techniques. Use the Laplace transform method to find $v_o(t)$ for "
         "$t$ ≥ 0+.",
     page=515, fig=(515, "13.11"), domain="fd",
     desc="c,1,0,0.5'u,100:r1,1,2,32'k:r2,2,0,240'k:r3,2,0,60'k",
     expect={"v_1": "100/(s + 25)", "v_2": "60/(s + 25)"},
     shows="The same description as Example 7.3 in the TR section, with FD chosen instead "
           "of TR — which is what the book does too, revisiting the circuit with the Laplace "
           "transform. The answers come back as transforms, functions of $s$ with the "
           "initial condition already inside them: `v_2` is the book's $V_o(s)$, one inverse "
           "transform away from the $60e^{-25t}$ it printed the first time. One circuit, two "
           "domains, nothing retyped."),

dict(num="13.3", title="The Step Response of an RLC Circuit",
     ask="Consider the circuit in Fig. 13.13, where the initial current in the inductor is "
         "29 mA and the initial voltage across the capacitor is 50 V. This circuit was "
         "analyzed in Example 8.10 using second-order circuit analysis techniques. Use the "
         "Laplace transform method to find $v(t)$ for $t$ ≥ 0.",
     page=515, fig=(515, "13.13"), domain="fd",
     desc="j,0,1,0.024/s:c,1,0,25'n,50:l,1,0,25'm,0.029:r,1,0,500",
     expect={"v_1": "(50*s - 200000)/(s**2 + 80000*s + 1600000000)"},
     shows="The book draws the $s$-domain circuit with three impedances in parallel and "
           "three current sources: the real one, and one each standing for the inductor's "
           "initial current and the capacitor's initial voltage. Here the initial conditions "
           "are the fifth fields of `c` and `l`, exactly as in TR, and the source is written "
           "as its own transform — the 24 mA step is `0.024/s`. The book's $V(s)$ is the "
           "voltage at node 1, which the book then inverts by hand into a damped response; "
           "choose TR instead and that inversion is done for you."),

dict(num="13.5", title="Analyzing a Circuit with Multiple Meshes",
     ask="The circuit in Fig. 13.17 has no initial stored energy. At $t$ = 0 the switch "
         "closes. Use Laplace methods to find $i_1(t)$ and $i_2(t)$ for $t$ ≥ 0.",
     page=519, fig=(519, "13.17"), domain="tr",
     desc="e,1,0,336:l1,1,2,8.4:r1,2,0,42:l2,2,3,10:r2,3,0,48",
     expect={"i_l1": "15 - 14*exp(-2*t) - exp(-12*t)",
             "i_l2": "7 - 8.4*exp(-2*t) + 1.4*exp(-12*t)"},
     shows="A Laplace-chapter problem, run in TR. The book writes two mesh equations in "
           "$s$, solves them, expands each answer in partial fractions and inverts both. TR "
           "does all of that in the same order and prints $i_1(t)$ and $i_2(t)$, which are "
           "the currents through the two inductors. Choose FD instead and the same run stops "
           "before the inversion, with the two transforms the book has half-way through."),

dict(num="13.6", title="Creating a Thevenin Equivalent in the s Domain",
     ask="The circuit in Fig. 13.20 has no initial stored energy, and at $t$ = 0 the switch "
         "closes. Find the Thevenin equivalent for the circuit to the left of the terminals "
         "a and b in the s domain, using Laplace methods.",
     page=521, fig=(521, "13.20"), kind="th", n1="a", n2="0", domain="fd",
     desc="e,1,0,480/s:r1,1,2,20:l,2,0,0.002:r2,2,a,60",
     expect={"vth": "480/(s + 10000)", "z": "80*(s + 7500)/(s + 10000)"},
     shows="The Thévenin tool works in the $s$ domain as well, so the equivalent comes back "
           "as a pair of rational functions of $s$ rather than a pair of numbers: `vth` is "
           "the transform of the open-circuit voltage and `z` the impedance. The source is "
           "written as the transform of its step, `480/s`. The book goes on to connect the "
           "capacitor to the equivalent and find its current; that second step is one more "
           "run, in TR, with the capacitor in place."),

dict(num="13.7", title="Analyzing a Circuit with Mutual Inductance",
     ask="The make-before-break switch in the circuit in Fig. 13.23 has been in position a "
         "for a long time. At $t$ = 0 it moves instantaneously to position b. Use Laplace "
         "methods to find $i_2(t)$ for $t$ ≥ 0.",
     page=523, fig=(523, "13.23"), domain="tr",
     desc="r3,0,p,3:l1,p,0,2,5:m,l1,l2,2:l2,q,d,8,0:r2b,q,c,2:r10,c,d,10",
     expect={"i_l2": "1.25*exp(-t) - 1.25*exp(-3*t)",
             "i_l1": "2.5*exp(-t) + 2.5*exp(-3*t)"},
     shows="Also from the Laplace chapter. The book replaces the coupled coils by a "
           "T-equivalent of three inductors and adds a voltage source for each initial "
           "current before it can write mesh equations in $s$. Here the coupling is the one "
           "`m` line and the initial currents are fifth fields: 5 A in the primary, which is "
           "what the DC circuit before the switch moved had established, and 0 in the "
           "secondary. The secondary is an island — nothing conducts between the two "
           "windings — and Symbulator says so in a note and refers its voltages to node "
           "**d**, rather than refusing the circuit. The book's $i_2$ is the current through "
           "`l2`."),

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
     shows="Nothing in the app is labelled *transfer function*, because nothing needs to "
           "be. Leave the source as the symbol `vg`, run FD, and the voltage at node 2 comes "
           "back as a function of $s$ with `vg` in it; dividing by `vg` is the transfer "
           "function, part (a). Part (b), the poles and zeros, are the roots of that "
           "expression's denominator and numerator: poles at $s = -3000 \\pm j4000$ and a "
           "zero at $s = -5000$, the book's values."),

dict(num="13.13", title="A Series Inductor Circuit with an Impulsive Response",
     ask="The switch in the circuit shown in Fig. 13.50 has been closed for a long time. At "
         "$t$ = 0 it opens. Use Laplace methods to find the output voltage $v_o$ and the "
         "current in the 3 H inductor, $i_1$.",
     page=541, fig=(541, "13.50"), domain="tr",
     desc="e,1,0,100:r1,1,2,10:l1,2,3,3,10:r2,3,4,15:l2,4,0,2,0",
     expect={"v_3": "12*DiracDelta(t) + 60 + 10*exp(-5*t)",
             "i_l1": "4 + 2*exp(-5*t)"},
     shows="Opening the switch puts two inductors that were carrying different currents — "
           "10 A and none — into series, and since an inductor's current cannot jump, the "
           "voltage across them has to contain an impulse. The answer says so: "
           "`DiracDelta(t)` is the impulse, and its weight of 12 is what it takes to bring "
           "the 2 H inductor from 0 to the 6 A the pair settle on. The book's $v_o$ is the "
           "voltage at node 3 and its $i_1$ the current through `l1`."),
]

SPECS += [
dict(num="3.10", title="Using a Wheatstone Bridge to Measure Resistance",
     ask="For the Wheatstone bridge in Fig. 3.30, $R_3$ can be varied from 10 Ω to 2 kΩ. "
         "What range of resistor values can this bridge measure?",
     page=101, fig=(101, "3.30"), domain="dc",
     desc="e,1,0,vs:r1,1,a,1'k:r2,1,b,4'k:rg,a,b,500:r3,a,0,r3:rx,b,0,rx",
     equations=["i_rg = 0"], unknowns=["rx"],
     expect={"rx": "4*r3"},
     shows="A Wheatstone bridge measures a resistance nobody knows, $R_x$, by comparing it "
           "with resistances that are known. The adjustable resistor $R_3$ is turned until "
           "the detector between the two arms of the bridge — here the 500 Ω resistor `rg` — "
           "carries no current, and at that setting the unknown can be read off the others. "
           "So the circuit is described with two resistances left as symbols rather than "
           "numbers, `r3` for the adjustable one and `rx` for the unknown; the source is a "
           "symbol too, `vs`, because its value plays no part at balance. The balance "
           "condition itself, *no current through the detector*, is not a value that can be "
           "typed into any element, so it is given to Symbulator as an equation in "
           "{{card:Expert Mode}}, `i_rg = 0`, with `rx` named as the unknown to solve for.",
     after="That formula answers the question. The bridge reads four times whatever "
           "{{var:R_3}} is set to, so with {{var:R_3}} at its lowest, 10 Ω, the bridge reads "
           "{{o:40}} Ω, and at its highest, 2 kΩ, it reads {{o:8}} kΩ: the range of "
           "resistances this bridge can measure is 40 Ω to 8 kΩ."),

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
     shows="A filter is a circuit with a name, and nothing in the app is filter-shaped. "
           "Leave $R$, $L$ and $C$ as symbols, run FD, and the ratio of output to input is "
           "the standard bandpass form the book derives in part (a): a first-order numerator "
           "over a second-order denominator, from which the centre frequency "
           "$\\omega_0 = 1/\\sqrt{LC}$ and the bandwidth $\\beta = 1/RC$ are read off. "
           "Parts (b) to (d) are then ordinary algebra on that expression; for a 5 kHz "
           "centre and a 200 Hz bandwidth with a 5 µF capacitor the book's design values "
           "are $R$ = 159.2 Ω and $L$ = 202.6 µH."),

dict(num="18.1", title="Finding the z Parameters of a Two-Port Circuit",
     ask="Find the z parameters for the circuit shown in Fig. 18.3.",
     page=724, fig=(724, "18.3"), kind="port", n1="1", n2="2", ptype="z", domain="dc",
     desc="r5,1,2,5:r20,1,0,20:r15,2,0,15",
     expect={"11": 10, "12": 7.5, "21": 7.5, "22": 9.375},
     shownames={"11": "z11", "12": "z12", "21": "z21", "22": "z22"},
     shows="The book takes four open-circuit measurements — two with a source at port 1 "
           "and the other port open, two with the source moved to port 2 — and reads one "
           "z parameter from each. The two-port tool makes all four in one run and names "
           "them `z11` to `z22`. Note that `z12` = `z21`, as it must for a network of "
           "resistors, which is reciprocal: that equality is a result here, not an "
           "assumption."),

dict(num="18.6", title="Analyzing Cascaded Two-Port Circuits",
     ask="Two identical amplifiers are connected in cascade. Each is described by its h "
         "parameters: $h_{11}$ = 1000 Ω, $h_{12}$ = 0.0015, $h_{21}$ = 100, $h_{22}$ = "
         "100 µS. The source has 500 Ω of internal resistance and the load is 10 kΩ. Find "
         "the voltage gain $V_2/V_g$.",
     page=738, fig=(738, "18.14"), domain="dc",
     desc="e,1,0,vg:rs,1,a,500:h1,a,b,[1000,0.0015,100,0.0001]:"
          "h2,b,c,[1000,0.0015,100,0.0001]:rl,c,0,10'k",
     shownames={"@v_c/vg": "v_c/vg"}, units={"@v_c/vg": ""},
     expect={"@v_c/vg": 33333.33},
     shows="The book converts each amplifier's h parameters into a parameters, multiplies "
           "the two transmission matrices for the cascade, and reads the voltage gain out of "
           "a table of formulas. Symbulator's `h` element takes the four parameters as a "
           "bracketed term, so the cascade is two such lines wired end to end between the "
           "source resistance and the load, and the gain is the output node's voltage "
           "divided by the symbolic source — `v_c/vg`, a large number, and the book's."),
]
