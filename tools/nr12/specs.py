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
"""
SPECS = []

SPECS += [
dict(num="3.7", title="Using Voltage Division and Current Division to Solve a Circuit",
     ask="Use current division to find the current $i_o$ and use voltage division to find "
         "the voltage $v_o$ for the circuit in Fig. 3.22.",
     page=95, fig=(95, "3.22"), domain="dc",
     desc="j,0,1,8:r1,1,2,36:r2,2,0,44:r3,1,0,10:r4,1,3,40:r5,3,4,10:r6,4,0,30:r7,1,0,24",
     expect={"i_r7": 2, "v_r6": 18, "v_r7": 48, "r_j": 6},
     shows="A one-line answer to a problem the book solves with two division formulas: "
           "the whole circuit is solved at once, and the source's own `r_j` is the 6 Ohm "
           "equivalent resistance the book works out by hand."),

dict(num="3.11", title="Applying a Delta-to-Wye Transform",
     ask="Find the current and power supplied by the 40 V source in the circuit shown in Fig. 3.35.",
     page=103, fig=(103, "3.35"), domain="dc",
     desc="e,1,0,40:r1,1,2,5:r2,2,3,100:r3,2,4,125:r4,3,4,25:r5,3,0,40:r6,4,0,37.5",
     expect={"@-i_e": 0.5, "@-p_e": 20, "r_e": 80},
     shownames={"@-i_e": "-i_e", "@-p_e": "-p_e"},
     shows="The book needs a delta-to-wye transform to reduce this bridge. Symbulator needs "
           "nothing: the bridge is six lines, and `r_e` reports the 80 Ohm the transform was for."),

dict(num="4.4", title="Using the Node-Voltage Method with Dependent Sources",
     ask="Use the node-voltage method to find the power dissipated in the 5 Ohm resistor "
         "in the circuit shown in Fig. 4.10.",
     page=125, fig=(125, "4.10"), domain="dc",
     desc="e,1,0,20:r1,1,2,2:r2,2,0,20:r3,2,3,5:r4,3,0,10:r5,3,4,2:e2,4,0,8*ir3",
     expect={"v_2": 16, "v_3": 10, "i_r3": 1.2, "p_r3": 7.2},
     shows="A dependent source is written by naming another answer in its value - "
           "`8*ir3` - so no constraint equation has to be written by hand."),

dict(num="4.7", title="Using the Mesh-Current Method with Dependent Sources",
     ask="Use the mesh-current method to find the power dissipated in the 4 Ohm resistor "
         "in the circuit shown in Fig. 4.23.",
     page=133, fig=(133, "4.23"), domain="dc",
     desc="e,1,0,50:r1,1,3,1:r2,1,2,5:r3,2,3,4:r4,2,0,20:e2,3,0,15*ir4",
     expect={"i_r4": 1.6, "i_r3": 2, "p_r3": 16},
     shows="The same circuit the book solves with three mesh equations and a constraint. "
           "Symbulator is told the circuit, not the method."),

dict(num="4.21", title="Calculating the Condition for Maximum Power Transfer",
     ask="a) For the circuit shown in Fig. 4.65, find the value of $R_L$ that results in "
         "maximum power being transferred to $R_L$. b) Calculate the maximum power that can "
         "be delivered to $R_L$.",
     page=153, fig=(153, "4.65"), kind="th", n1="2", n2="0", domain="dc",
     desc="e,1,0,360:r1,1,2,30:r2,2,0,150",
     expect={"vth": 300, "z": 25, "pmax": 900},
     shows="The Thevenin tool answers all three parts at once: `z` is the load for maximum "
           "transfer and `pmax` is the power it takes."),
]

SPECS += [
dict(num="4.8", title="A Special Case in the Mesh-Current Method",
     ask="Use the mesh-current method to find branch currents $i_a$, $i_b$ and $i_c$ "
         "in the circuit for Example 4.3, repeated here as Fig. 4.25.",
     page=134, fig=(134, "4.25"), domain="dc",
     desc="e,1,0,50:r1,1,2,5:r2,2,0,10:r3,2,0,40:j,0,2,3",
     expect={"i_r1": 2, "i_r2": 4, "i_r3": 1, "v_2": 40},
     shows="The book's 'special case' is a current source shared by no other mesh, which "
           "needs a rule of its own. Symbulator has no meshes, so there is no special case."),

dict(num="4.13", title="Using Special Source Transformation Techniques",
     ask="a) Use source transformations to find the voltage $v_o$ in the circuit shown in "
         "Fig. 4.42. b) Find the power developed by the 250 V voltage source. "
         "c) Find the power developed by the 8 A current source.",
     page=143, fig=(143, "4.42"), domain="dc",
     desc="e,1,0,250:r1,1,0,125:r2,1,2,25:j,2,9,8:r3,9,0,10:r4,2,0,100:r5,2,3,5:r6,3,0,15",
     expect={"v_r4": 20, "@-i_e": 11.2, "@-p_e": 2800, "@-p_j": 480},
     shownames={"@-i_e": "-i_e", "@-p_e": "-p_e", "@-p_j": "-p_j"},
     shows="Four source transformations in the book; one description here. The resistors the "
           "book has to put back before it can find the powers were never taken out."),

dict(num="4.23", title="Using Superposition to Solve a Circuit with Dependent Sources",
     ask="Use the principle of superposition to find $v_o$ in the circuit shown in Fig. 4.71.",
     page=156, fig=(156, "4.71"), domain="dc",
     desc="e,1,c,10:r1,1,a,5:r2,a,c,20:r3,b,0,10:j1,0,b,5:j2,b,a,0.4*vr3:e2,0,c,2*ir1",
     expect={"v_r2": 24, "v_r3": 10, "i_r1": -2.8},
     shows="Superposition is a method for getting an answer by hand, not a property of the "
           "answer. Two dependent sources and two independent ones, solved once."),

dict(num="5.1", title="Analyzing an Op Amp Circuit",
     ask="The op amp in the circuit shown in Fig. 5.7 is ideal. a) Calculate $v_o$ if "
         "$v_a$ = 1 V and $v_b$ = 0 V. b) Repeat for $v_a$ = 1 V and $v_b$ = 2 V. "
         "c) If $v_a$ = 1.5 V, specify the range of $v_b$ that avoids amplifier saturation.",
     page=181, fig=(181, "5.7"), domain="dc",
     desc="ea,1,0,va:r1,1,2,25'k:r2,2,3,100'k:eb,4,0,vb:o,4,2,3",
     expect={"v_3": "5*vb - 4*va"},
     parts=[
      ("a", "With {{var:v_a}} = 1 V and {{var:v_b}} = 0 V the formula gives "
            "{{var:v_o}} = 5(0) − 4(1) = {{o:-4}} V. That is inside the "
            "supplies, so the op amp is in its linear region and -4 V is the "
            "answer."),
      ("b", "With {{var:v_a}} = 1 V and {{var:v_b}} = 2 V, {{var:v_o}} = "
            "5(2) − 4(1) = {{o:6}} V. Inside the supplies again, so the op "
            "amp is still linear."),
      ("c", "With {{var:v_a}} = 1.5 V the formula becomes {{var:v_o}} = "
            "5{{var:v_b}} − 6. The op amp stays linear while that lies "
            "between the rails, so Symbulator is asked the question directly "
            "- put `v_3 = 10` in {{card:Expert Mode}} with `vb` as the "
            "unknown, then again with `v_3 = -10`. The rails are reached at "
            "{{var:v_b}} = {{o:3.2}} V and {{var:v_b}} = {{o:-0.8}} V, so "
            "the range is {{o:-0.8}} V \u2264 {{var:v_b}} \u2264 {{o:3.2}} V."),
     ],
     shows="An ideal op amp does not know its supplies exist - it will report an output of "
           "200 V as readily as 2 V - so saturation is a question you ask of the answer "
           "rather than something the solve enforces. Leave both inputs symbolic and one "
           "run gives the formula every part is then read off."),
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
            "-({{var:R_f}}/{{var:R_a}}){{var:v_a}} - "
            "({{var:R_f}}/{{var:R_b}}){{var:v_b}} - "
            "({{var:R_f}}/{{var:R_c}}){{var:v_c}}, so with a 20 k\u03a9 "
            "feedback resistor the three input resistors are "
            "{{var:R_a}} = 20k/4 = {{o:5}} k\u03a9, {{var:R_b}} = 20k/1 = "
            "{{o:20}} k\u03a9 and {{var:R_c}} = 20k/5 = {{o:4}} k\u03a9. "
            "Running that circuit returns the very formula the design was "
            "asked to hit, which is the check."),
      ("b", "With {{var:v_a}} = 2 V and {{var:v_c}} = -1 V the output "
            "collapses to {{var:v_o}} = -{{var:v_b}} − 3. Asking "
            "{{card:Expert Mode}} for the {{var:v_b}} that puts `v_4` on "
            "each rail gives {{o:9}} V at -12 V and {{o:-15}} V at +12 V, so "
            "the op amp stays linear for {{o:-15}} V \u2264 {{var:v_b}} "
            "\u2264 {{o:9}} V."),
     ],
     shows="The design is checked in one run: the answer comes back as the very formula the "
           "problem asked the designer to hit."),

dict(num="5.3c", title="Designing a Summing Amplifier - part (c), in Expert Mode",
     ask="c) Suppose $v_a$ = 2 V, $v_b$ = 3 V and $v_c$ = $-$1 V. Using the input resistor "
         "values found in part (a), how large can the feedback resistor be before the op amp "
         "saturates?",
     page=185, fig=(185, "5.12"), domain="dc",
     desc="ea,1,0,2:eb,2,0,3:ec,3,0,-1:r1,1,n,5'k:r2,2,n,20'k:r3,3,n,4'k:rf,n,4,rf:o,0,n,4",
     equations=["v_4 = -12"], unknowns=["rf"],
     expect={"rf": 40000},
     parts=[
      ("c", "With {{var:v_a}} = 2 V, {{var:v_b}} = 3 V and {{var:v_c}} = "
            "-1 V the three input currents sum to a positive number, so the "
            "output swings negative and it is the -12 V rail that is reached "
            "first. Leave the feedback resistor as the symbol `rf`, put "
            "`v_4 = -12` in {{card:Expert Mode}} and name `rf` the unknown: "
            "the answer is {{o:40}} k\u03a9. Any larger and the op amp "
            "saturates."),
     ],
     shows="An unknown that is a component value, not an answer: name the saturation voltage "
           "as an equation and ask for the resistor. This is what Expert Mode is for."),

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
            "{{var:R_a}} = {{var:R_c}} = {{o:1.5}} k\u03a9 and "
            "{{var:R_b}} = {{var:R_d}} = {{o:12}} k\u03a9. The formula also "
            "requires {{var:R_a}}/{{var:R_b}} = {{var:R_c}}/{{var:R_d}}, "
            "which those four satisfy. The run returns exactly "
            "8({{var:v_b}} − {{var:v_a}})."),
      ("b", "With {{var:v_a}} = 1 V the output is {{var:v_o}} = "
            "8{{var:v_b}} − 8, which reaches +8 V at {{var:v_b}} = {{o:2}} V "
            "and -8 V at {{var:v_b}} = {{o:0}} V. So the op amp remains in "
            "its linear region for {{o:0}} V \u2264 {{var:v_b}} \u2264 "
            "{{o:2}} V."),
     ],
     shows="The gain-of-8 design returns exactly 8(vb - va), and part (b)'s range follows "
           "from that one line."),

dict(num="5.7", title="Analyzing a Noninverting-Amplifier Circuit Using a Realistic Op Amp Model",
     ask="Analyze the noninverting amplifier of Example 5.4 using the realistic op amp model: "
         "open-loop gain $A$ = 50,000, input resistance $R_i$ = 100 kΩ, output "
         "resistance $R_o$ = 7.5 kΩ. Find $v_o/v_g$.",
     page=195, fig=(195, "5.21"), domain="dc",
     desc="eg,1,0,vg:rg,1,p,1'k:ri,p,n,100'k:rs,n,0,2'k:rf,n,3,10'k:ro,4,3,7.5'k:"
          "ea,4,0,50000*(vp-vn)",
     shownames={"@v_3/vg": "v_3/vg"}, units={"@v_3/vg": ""},
     expect={"@v_3/vg": 5.9988}, tol=2e-5,
     shows="No `o` element at all: the realistic op amp is a dependent source with its own "
           "input and output resistances, and the finite-gain answer 5.9988 falls out against "
           "the ideal 6."),

dict(num="7.1", title="Determining the Natural Response of an RL Circuit",
     ask="The switch in the circuit shown in Fig. 7.6 has been closed for a long time before "
         "it is opened at $t$ = 0. Find a) $i_L(t)$ for *t* ≥ 0, b) $i_o(t)$ for "
         "*t* ≥ 0+, c) $v_o(t)$ for *t* ≥ 0+.",
     page=250, fig=(250, "7.6"), domain="tr",
     desc="l,1,0,2,20:r1,1,2,2:r2,2,0,10:r3,2,0,40",
     expect={"i_l": "20*exp(-5*t)", "i_r3": "-4*exp(-5*t)", "v_2": "-160*exp(-5*t)"},
     shows="A switched circuit is two runs: a DC pass for the initial current, then TR with "
           "that number in the inductor's fifth field. No time constant is ever computed."),
]

SPECS += [
dict(num="7.3", title="Determining the Natural Response of an RC Circuit",
     ask="The switch has been in position x for a long time. At t = 0 it moves "
         "instantaneously to position y. Find a) vC(t), b) vo(t) and c) io(t).",
     page=256, fig=(256, "7.15"), domain="tr",
     desc="c,1,0,0.5'u,100:r1,1,2,32'k:r2,2,0,240'k:r3,2,0,60'k",
     expect={"v_1": "100*exp(-25*t)", "v_2": "60*exp(-25*t)",
             "i_r3": "0.001*exp(-25*t)"},
     shows="The capacitor's starting voltage goes in its fifth field and the answers come "
           "back as functions of t. No time constant is computed anywhere."),

dict(num="7.5", title="Determining the Step Response of an RL Circuit",
     ask="The switch has been in position a for a long time. At t = 0 it moves from a to b. "
         "a) Find i(t) for t >= 0. b) What is the initial voltage across the inductor just "
         "after the switch has been moved?",
     page=260, fig=(260, "7.21"), domain="tr",
     desc="e,1,0,24:r1,1,2,2:l,2,0,0.2,-8",
     expect={"i_l": "12 - 20*exp(-10*t)", "v_2": "40*exp(-10*t)"},
     shows="A step response with a non-zero, negative starting current - the inductor was "
           "carrying the 8 A source the other way. Part (b) is the answer at t = 0."),

dict(num="7.10", title="Determining the Step Response of a Circuit with Magnetically Coupled Coils",
     ask="There is no energy stored in the circuit at the time the switch is closed. "
         "Find the solutions for io, vo, i1 and i2.",
     page=271, fig=(271, "7.37"), domain="tr",
     desc="e,1,0,120:r1,1,2,7.5:l1,2,0,3:l2,2,0,15:m,l1,l2,6",
     expect={"i_r1": "16 - 16*exp(-5*t)", "v_2": "120*exp(-5*t)",
             "i_l1": "24 - 24*exp(-5*t)", "i_l2": "-8 + 8*exp(-5*t)"},
     shows="The book replaces the coupled pair with one 1.5 H equivalent and then works back "
           "to i1 and i2 through KVL. The m element is one line, and both coil currents come "
           "back on their own."),

dict(num="7.11a", title="Analyzing an RL Circuit That Has Sequential Switching (0 to 35 ms)",
     ask="Both switches have been closed for a long time. At t = 0 switch 1 is opened; "
         "35 ms later switch 2 is opened. a) Find iL(t) for 0 <= t <= 35 ms.",
     page=273, fig=(273, "7.39"), domain="tr",
     desc="r6,2,0,6:r3,2,3,3:l,3,0,0.15,6:r18,3,0,18",
     expect={"i_l": "6*exp(-40*t)"},
     shows="Sequential switching is just more runs. A DC pass on the t < 0 circuit gives "
           "iL(0) = 6 A, which is the number that goes in the inductor's fifth field here."),

dict(num="7.11b", title="Analyzing an RL Circuit That Has Sequential Switching (after 35 ms)",
     ask="b) Find iL for t >= 35 ms. (Time is measured from the second switching.)",
     page=273, fig=(273, "7.39"), domain="tr",
     desc="r6,2,0,6:r3,2,3,3:l,3,0,0.15,1.47961",
     expect={"i_l": "1.47961*exp(-60*t)"},
     shows="The third run: switch 2 has dropped the 18 ohm, so the inductor now sees 9 ohm "
           "and the starting current is what the second run left at 35 ms."),

dict(num="7.13", title="Finding the Unbounded Response in an RC Circuit",
     ask="a) When the switch is closed at t = 0, find vo(t). The Thevenin resistance seen by "
         "the capacitor is negative, so the response grows without bound.",
     page=277, fig=(277, "7.45"), domain="tr",
     desc="c,1,0,5'u,10:r1,1,0,10'k:r2,1,0,20'k:j,0,1,7*ir2",
     expect={"v_1": "10*exp(40*t)"},
     shows="A dependent source makes the Thevenin resistance -5 kilohm, and the exponent "
           "comes back positive. Nothing had to be told that this case was different."),

dict(num="8.2", title="Finding the Overdamped Natural Response of a Parallel RLC Circuit",
     ask="For the circuit in Fig. 8.6, v(0+) = 12 V and iL(0+) = 30 mA. Find the expression "
         "for v(t). (Example 8.3 then asks for the three branch currents.)",
     page=306, fig=(306, "8.6"), domain="tr",
     desc="c,1,0,0.2'u,12:l,1,0,50'm,0.03:r,1,0,200",
     expect={"v_1": "-14*exp(-5000*t) + 26*exp(-20000*t)",
             "i_r": "-0.07*exp(-5000*t) + 0.13*exp(-20000*t)",
             "i_l": "0.056*exp(-5000*t) - 0.026*exp(-20000*t)"},
     shows="Overdamped, and nothing had to say so: the book compares alpha with omega-nought "
           "and picks a solution form. Example 8.3's branch currents are in the same run."),

dict(num="8.4", title="Finding the Underdamped Natural Response of a Parallel RLC Circuit",
     ask="In the circuit shown, V0 = 0 and I0 = -12.25 mA. Calculate the voltage response "
         "for t >= 0.",
     page=310, fig=(310, "8.8"), domain="tr", at_t=[1e-4, 5e-4, 1e-3, 3e-3],
     desc="c,1,0,125'n,0:l,1,0,8,-0.01225:r,1,0,20'k",
     expect={"v_1": "100*exp(-200*t)*sin(979.80*t)"}, tol=3e-4,
     shows="The same three lines give the underdamped case, damped sine and all. The book "
           "needs a different table row; the description does not change."),

dict(num="8.11", title="Finding the Natural Response of a Series RLC Circuit",
     ask="The 0.1 uF capacitor is charged to 100 V. At t = 0 it is discharged through a "
         "series combination of a 100 mH inductor and a 560 ohm resistor. a) Find i(t). "
         "b) Find vC(t).",
     page=328, fig=(328, "8.17"), domain="tr",
     desc="c,1,0,0.1'u,100:l,2,1,0.1:r,2,0,560",
     expect={"i_l": "-0.1042*exp(-2800*t)*sin(9600*t)"}, at_t=[3e-5, 1e-4, 3e-4], tol=1e-3,
     shows="Series rather than parallel, and again the case is not chosen by anyone. The "
           "inductor's node order is written to match the book's mesh arrow."),

dict(num="8.12", title="Finding the Step Response of a Series RLC Circuit",
     ask="No energy is stored in the 100 mH inductor or the 0.4 uF capacitor when the switch "
         "is closed. Find vC(t) for t >= 0.",
     page=328, fig=(328, "8.18"), domain="tr",
     desc="e,1,0,48:l,1,2,0.1:r,2,3,1250:c,3,0,0.4'u",
     expect={"v_3": "48 + 16*exp(-10000*t) - 64*exp(-2500*t)"},
     shows="A step response on a series RLC: the final value, the two roots and both "
           "coefficients arrive together in one expression."),
]

import sympy as _sp
W = _sp.Symbol("omega")

SPECS += [
dict(num="9.9", title="Combining Impedances in Series and in Parallel",
     ask="The sinusoidal current source produces is = 8 cos 200,000t A. b) Find the "
         "equivalent admittance to the right of the source. c) Find the phasor voltage V. "
         "d) Find the phasor current I. e) Find the steady-state expressions for v and i.",
     page=363, fig=(363, "9.20"), domain="ac", omega=200000,
     desc="j,0,1,8:r1,1,0,10:r2,1,2,6:l,2,0,40'u:c,1,0,1'u",
     expect={"v_1": 32 - 24j, "i_r2": -4j},
     shows="Henries and farads go in as they are given: the solver turns them into j8 and "
           "-j5 at the stated frequency. V comes back 40 at -36.87 degrees and I 4 at -90."),

dict(num="9.10", title="Using a Delta-to-Wye Transform in the Frequency Domain",
     ask="Use a delta-to-wye impedance transformation to find I0, I1, I2, I3, I4, I5, "
         "V1 and V2 in the circuit in Fig. 9.23.",
     page=365, fig=(365, "9.23"), domain="ac", omega=W,
     desc="e,a,0,120:r1,a,b,-4j:r2,a,c,63.2+2.4j:r3,b,c,10:r4,b,0,20+60j:r5,c,0,-20j",
     shownames={"@-i_e": "-i_e"},
     expect={"@-i_e": 2.4 + 3.2j, "i_r1": 2 + _sp.Rational(8, 3) * 1j,
             "i_r3": _sp.Rational(4, 3) + 4.266666666666667j,
             "i_r4": _sp.Rational(2, 3) - 1.6j, "i_r5": _sp.Rational(26, 15) + 4.8j,
             "v_b": _sp.Rational(328, 3) + 8j, "v_c": 96 - _sp.Rational(104, 3) * 1j},
     shows="Impedances go in as ohms, complex ones included, so the frequency never has to "
           "be known. Eight answers the book gets by transforming and working back."),

dict(num="9.12", title="Finding a Thevenin Equivalent in the Frequency Domain",
     ask="Find the Thevenin equivalent circuit with respect to terminals a,b for the "
         "circuit shown in Fig. 9.32.",
     page=368, fig=(368, "9.32"), kind="th", n1="9", n2="0", domain="ac", omega=W,
     desc="e,1,0,120:r1,1,2,12:r2,2,0,60:r3,2,9,-40j:e2,3,0,10*v2:r4,3,9,120",
     expect={"vth": 784 - 288j, "z": 91.2 - 38.4j},
     shows="A dependent source means the Thevenin resistance cannot be found by inspection; "
           "the book needs a test source. The tool returns both numbers."),

dict(num="9.14", title="Using the Mesh-Current Method in the Frequency Domain",
     ask="Use the mesh-current method to find the voltages V1, V2 and V3 in the circuit "
         "shown in Fig. 9.39.",
     page=372, fig=(372, "9.39"), domain="ac", omega=W,
     desc="e,1,0,150:r1,1,2,1:r2,2,a,2j:r3,a,c,12:r4,c,0,-16j:r5,a,4,1:r6,4,b,3j:"
          "e2,b,0,39*ir3",
     shownames={"@v_1-v_a": "v_1 - v_a", "@v_a-v_b": "v_a - v_b"},
     expect={"@v_1-v_a": 78 - 104j, "v_a": 72 + 104j, "@v_a-v_b": 150 - 130j,
             "i_r3": -2 + 6j},
     shows="Two mesh equations and a constraint in the book. Here the controlling current "
           "is just the name of the answer it is, written into the dependent source's value."),

dict(num="9.15", title="Analyzing a Linear Transformer in the Frequency Domain",
     ask="A linear transformer has R1 = 200 ohm, R2 = 100 ohm, L1 = 9 H, L2 = 4 H, k = 0.5, "
         "and couples an 800 ohm + 1 uF load to a 300 V (rms) source of internal impedance "
         "500 + j100 at 400 rad/s. g) Calculate the Thevenin equivalent with respect to the "
         "terminals of the load.",
     page=375, fig=(376, "9.42"), kind="th", n1="c", n2="d", domain="ac", omega=W, rms=True,
     desc="e,1,0,300:r1,1,2,500:r2,2,a,100j:r3,a,p,200:r4,p,0,3600j:m,r4,r5,1200j:"
          "r5,q,d,1600j:r6,q,c,100",
     expect={"vth": 93.9351 + 17.7715j, "z": 171.086 + 1224.2595j}, tol=1e-4,
     shows="The primary is grounded and the secondary is not: its foot is node **d**, a "
           "name like any other. Nothing conducts from one winding to the other, so the "
           "secondary's absolute potentials are undefined - its currents and its voltage "
           "differences are not - and Symbulator says so in a note, measuring that side "
           "against d. Self-impedance, reflected impedance and the scaling factor are "
           "three of the book's seven parts; name the load's two terminals and the tool "
           "answers the last outright."),
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
     shows="Every element reports its own complex power, so part (a) and part (b) are one "
           "run. Part (c) - the balance the book checks by hand - is the sum of the s "
           "answers, and it is exactly zero."),

dict(num="10.12", title="Finding Maximum Power Transfer in a Circuit with an Ideal Transformer",
     ask="The variable resistor is adjusted until maximum average power is delivered to RL. "
         "a) What is the value of RL in ohms? b) What is the maximum average power delivered "
         "to RL?",
     page=423, fig=(423, "10.25"), kind="th", n1="a", n2="0", domain="ac", omega=W, rms=True,
     desc="e,1,0,840:r60,1,p,60:t,[p,x],[x,a],[4,1]:r20,x,0,20",
     expect={"vth": -210, "z": 35, "pmax": 315},
     shows="An ideal transformer whose windings share a node, so both ports are written as "
           "bracketed terminal pairs. The book works the constraint equations twice, once "
           "open-circuit and once short-circuit; the tool returns -210 V, 35 ohm and 315 W."),

dict(num="11.1", title="Analyzing a Wye-Wye Circuit",
     ask="A balanced, positive-sequence Y-connected generator with internal impedance "
         "0.2 + j0.5 ohm per phase and internal voltage 120 V per phase feeds a balanced "
         "Y-connected load of 39 + j28 ohm per phase over a line of 0.8 + j1.5 ohm per "
         "phase. b) Calculate the three line currents. c) Calculate the phase voltages at "
         "the load. d) Calculate the line voltages at the load. e) Calculate the phase "
         "voltages at the generator terminals.",
     page=446, fig=(446, "11.10"), domain="ac", omega=W,
     desc="ea,ga,0,120:eb,gb,0,120*exp(-2j*pi/3):ec,gc,0,120*exp(2j*pi/3):"
          "rga,ga,a,0.2+0.5j:rgb,gb,b,0.2+0.5j:rgc,gc,c,0.2+0.5j:"
          "rla,a,pa,0.8+1.5j:rlb,b,pb,0.8+1.5j:rlc,c,pc,0.8+1.5j:"
          "rfa,pa,nn,39+28j:rfb,pb,nn,39+28j:rfc,pc,nn,39+28j",
     shownames={"@Abs(v_pa-v_nn)": "|v_pa - v_nn|", "@Abs(v_pa-v_pb)": "|v_pa - v_pb|",
                "@Abs(v_a)": "|v_a|"},
     expect={"i_rla": 1.92 - 1.44j, "@Abs(v_pa-v_nn)": 115.22, "@Abs(v_pa-v_pb)": 199.58,
             "@Abs(v_a)": 118.90, "v_nn": 0},
     shows="There is no three-phase mode and none is needed. The whole circuit goes in - "
           "three sources carrying their phase in the value - rather than the single-phase "
           "equivalent the book has to construct first. The neutral comes back at exactly "
           "zero, which is the balance, measured rather than assumed."),
]

SPECS += [
dict(num="13.2", title="The Natural Response of an RC Circuit",
     ask="The switch has been in position x for a long time; at t = 0 it moves to y. "
         "Use the Laplace transform method to find vo(t). (The same circuit as Example 7.3, "
         "worked in the s domain.)",
     page=515, fig=(515, "13.11"), domain="fd",
     desc="c,1,0,0.5'u,100:r1,1,2,32'k:r2,2,0,240'k:r3,2,0,60'k",
     expect={"v_1": "100/(s + 25)", "v_2": "60/(s + 25)"},
     shows="The same description as Example 7.3 with FD chosen instead of TR: the answers "
           "come back as transforms rather than as functions of t. One circuit, two domains, "
           "no re-typing."),

dict(num="13.3", title="The Step Response of an RLC Circuit",
     ask="The initial current in the inductor is 29 mA and the initial voltage across the "
         "capacitor is 50 V. Use the Laplace transform method to find v(t) for t >= 0.",
     page=515, fig=(515, "13.13"), domain="fd",
     desc="j,0,1,0.024/s:c,1,0,25'n,50:l,1,0,25'm,0.029:r,1,0,500",
     expect={"v_1": "(50*s - 200000)/(s**2 + 80000*s + 1600000000)"},
     shows="The book combines three parallel impedances and adds three current sources, two "
           "of them standing for the initial conditions. Here the initial conditions are the "
           "fifth field of c and l, and V(s) is the answer."),

dict(num="13.5", title="Analyzing a Circuit with Multiple Meshes",
     ask="The circuit has no initial stored energy. At t = 0 the switch closes. Use Laplace "
         "methods to find i1(t) and i2(t) for t >= 0.",
     page=519, fig=(519, "13.17"), domain="tr",
     desc="e,1,0,336:l1,1,2,8.4:r1,2,0,42:l2,2,3,10:r2,3,0,48",
     expect={"i_l1": "15 - 14*exp(-2*t) - exp(-12*t)",
             "i_l2": "7 - 8.4*exp(-2*t) + 1.4*exp(-12*t)"},
     shows="Two coupled mesh equations, a partial-fraction expansion and two inverse "
           "transforms in the book. Choosing TR does all of it and prints i1 and i2."),

dict(num="13.6", title="Creating a Thevenin Equivalent in the s Domain",
     ask="Find the Thevenin equivalent with respect to terminals a,b for the circuit shown "
         "in Fig. 13.20.",
     page=521, fig=(521, "13.20"), kind="th", n1="a", n2="0", domain="fd",
     desc="e,1,0,480/s:r1,1,2,20:l,2,0,0.002:r2,2,a,60",
     expect={"vth": "480/(s + 10000)", "z": "80*(s + 7500)/(s + 10000)"},
     shows="The Thevenin tool works in the s domain too, so the equivalent comes back as a "
           "pair of rational functions rather than a pair of numbers."),

dict(num="13.7", title="Analyzing a Circuit with Mutual Inductance",
     ask="The make-before-break switch has been in position a for a long time. At t = 0 it "
         "moves instantaneously to position b. Use Laplace methods to find i2(t) for t >= 0.",
     page=523, fig=(523, "13.23"), domain="tr",
     desc="r3,0,p,3:l1,p,0,2,5:m,l1,l2,2:l2,q,d,8,0:r2b,q,c,2:r10,c,d,10",
     expect={"i_l2": "1.25*exp(-t) - 1.25*exp(-3*t)",
             "i_l1": "2.5*exp(-t) + 2.5*exp(-3*t)"},
     shows="The book replaces the coupled coils with a T-equivalent and adds two voltage "
           "sources for the initial currents. Here the coupling is one m line and the "
           "initial currents are fifth fields. The secondary is an island, and Symbulator "
           "says so in a note rather than refusing the circuit."),

dict(num="13.9", title="Deriving the Transfer Function of a Circuit",
     ask="Derive the transfer function H(s) = Vo/Vg for the circuit in Fig. 13.31.",
     page=527, fig=(527, "13.31"), domain="fd",
     desc="e,1,0,vg:r1,1,2,1000:r2,2,3,250:l,3,0,50'm:c,2,0,1'u",
     expect={"@v_2/vg": "1000*(s + 5000)/(s**2 + 6000*s + 25000000)"},
     labels={"@v_2/vg": "transfer function"},
     texnames={"@v_2/vg": "H(s) = \\dfrac{v_{2}}{v_{g}}"},
     units={"@v_2/vg": ""},
     shows="Nothing is labelled 'transfer function' because nothing needs to be: leave the "
           "source as a symbol, run FD, and divide. The poles and zeros are then the "
           "expression's own."),

dict(num="13.13", title="A Series Inductor Circuit with an Impulsive Response",
     ask="The switch has been closed for a long time and opens at t = 0. Find vo(t).",
     page=541, fig=(541, "13.50"), domain="tr",
     desc="e,1,0,100:r1,1,2,10:l1,2,3,3,10:r2,3,4,15:l2,4,0,2,0",
     expect={"v_3": "12*DiracDelta(t) + 60 + 10*exp(-5*t)",
             "i_l1": "4 + 2*exp(-5*t)"},
     shows="Opening the switch forces two inductors carrying different currents into series, "
           "so the voltage has to contain an impulse. The answer says DiracDelta(t) - the "
           "current jumps from 10 A to 6 A, and the algebra is what noticed."),
]

SPECS += [
dict(num="3.10", title="Using a Wheatstone Bridge to Measure Resistance",
     ask="For the Wheatstone bridge in Fig. 3.30, R3 can be varied from 10 ohm to 2 kilohm. "
         "What range of resistor values can this bridge measure?",
     page=101, fig=(101, "3.30"), domain="dc",
     desc="e,1,0,vs:r1,1,a,1'k:r2,1,b,4'k:rg,a,b,500:r3,a,0,r3:rx,b,0,rx",
     equations=["i_rg = 0"], unknowns=["rx"],
     expect={"rx": "4*r3"},
     shows="Balance is a statement about an answer - no current in the detector - so it is "
           "written as an equation and the unknown is a resistor. The answer comes back as "
           "the symbolic `4*r3`, and the range 40 ohm to 8 kilohm is that one line read twice."),

dict(num="14.6", title="Designing a Parallel RLC Bandpass Filter",
     ask="a) Show that the RLC circuit in Fig. 14.22 is a bandpass filter by deriving an "
         "expression for the transfer function H(s). b) Compute the centre frequency. "
         "c) Calculate the cutoff frequencies, the bandwidth and Q. d) Compute R and L for a "
         "centre frequency of 5 kHz and a bandwidth of 200 Hz, using a 5 uF capacitor.",
     page=581, fig=(581, "14.22"), domain="fd",
     desc="e,1,0,vi:rr,1,2,R:c,2,0,C:l,2,0,L",
     expect={"@v_2/vi": "(s/(C*R))/(s**2 + s/(C*R) + 1/(L*C))"},
     labels={"@v_2/vi": "transfer function"},
     texnames={"@v_2/vi": "H(s) = \\dfrac{v_{2}}{v_{i}}"},
     units={"@v_2/vi": ""},
     shows="Nothing in Symbulator is filter-shaped. Leave R, L and C as symbols, run FD, and "
           "the standard bandpass form appears - from which the centre frequency, the "
           "bandwidth and part (d)'s R = 159.2 ohm and L = 202.6 uH are ordinary algebra."),

dict(num="18.1", title="Finding the z Parameters of a Two-Port Circuit",
     ask="Find the z parameters for the circuit shown in Fig. 18.3.",
     page=724, fig=(724, "18.3"), kind="port", n1="1", n2="2", ptype="z", domain="dc",
     desc="r5,1,2,5:r20,1,0,20:r15,2,0,15",
     expect={"11": 10, "12": 7.5, "21": 7.5, "22": 9.375},
     shows="Four separate open-circuit measurements in the book - two of them with a source "
           "moved to the other port. One run here, and z12 = z21 because the network is "
           "reciprocal, which is a result rather than an assumption."),

dict(num="18.6", title="Analyzing Cascaded Two-Port Circuits",
     ask="Two identical amplifiers are connected in cascade. Each is described by its h "
         "parameters: h11 = 1000 ohm, h12 = 0.0015, h21 = 100, h22 = 100 uS. The source has "
         "500 ohm of internal resistance and the load is 10 kilohm. Find the voltage gain "
         "V2/Vg.",
     page=738, fig=(738, "18.14"), domain="dc",
     desc="e,1,0,vg:rs,1,a,500:h1,a,b,[1000,0.0015,100,0.0001]:"
          "h2,b,c,[1000,0.0015,100,0.0001]:rl,c,0,10'k",
     shownames={"@v_c/vg": "v_c/vg"}, units={"@v_c/vg": ""},
     expect={"@v_c/vg": 33333.33},
     shows="The book converts h to a, multiplies the two transmission matrices, then reads a "
           "gain formula out of Table 18.3. Here the two blocks are two lines of circuit "
           "wired end to end, and the gain is a division."),
]
