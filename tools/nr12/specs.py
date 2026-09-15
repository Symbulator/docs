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
  expect     book answer -> Symbulator answer name  ("@expr" = an Evaluate step,
             shown as its box; the runner verifies it all the same)
  booknames  answer name -> the book's own symbol, set beside the answer
  hide       answers the runner verifies but the page shows another way
  shows      the paragraph above the run: what the thing in the figure is
             and what is asked, then how we describe it -- no result
  pre        first runs, each {text, desc, tag, expect, booknames, note}: the
             circuit before the switch moves, run in DC for an initial condition
  evals      Evaluate steps after the results: {text, expr, at, unit, expect, book}
  solveq     Solve card runs after the results: {tag, text, equations,
             unknowns, conditions, real_only, expect, unit, book, entry, boxes,
             press, note}
  parts      (letter, text) -- a lettered part concluded in prose, after the steps
  after      what follows from the answers, last of all

Roberto's fifteen rules (12-13 Sep 2026), all applied; the list is in
README.md. In short: no book title; no comparison with the book's method
and no result above the run; only what is asked; explained as to someone
who does not know; what follows an answer comes after it; nothing from thin
air; fact or choice, in the first person plural; open with the thing, not
the trick; the problem's names where it gives them, ours declared; the
ordinary route before the expert one; every value produced by a step the
reader can perform; exactly what is typed, in its box; one answer per value
asked; one job per paragraph, in the session's order; the book's words for
the things and the app's labels for the controls.

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
     ask="Find the current $i_o$ and the voltage $v_o$ for the circuit in the figure.",
     page=95, fig=(95, "3.22"), domain="dc",
     desc="j,0,1,8:r1,1,2,36:r2,2,0,44:r3,1,0,10:r4,1,3,40:r5,3,4,10:r6,4,0,30:r7,1,0,24",
     expect={"i_r7": 2, "v_r6": 18},
     booknames={"i_r7": "i_o", "v_r6": "v_o"},
     shows="The circuit consists of a current source feeding a ladder of seven "
           "resistors. The question wants the current in one branch, $i_o$ in the 24 Ω "
           "resistor, and the voltage across another, $v_o$ across the 30 Ω. We "
           "describe the circuit as it is drawn, naming the source `j` and the "
           "resistors `r1` to `r7` from left to right, and taking the bottom rail as "
           "ground, so $i_o$ is the current through `r7` and $v_o$ the voltage across "
           "`r6`. One run in DC returns every current and voltage in the circuit, "
           "those two among them."),

dict(num="3.11", title="Applying a Delta-to-Wye Transform",
     ask="Find a) the current and b) the power supplied by the 40 V source in the circuit shown in the figure.",
     page=103, fig=(103, "3.35"), domain="dc",
     desc="e,1,0,40:r1,1,2,5:r2,2,3,100:r3,2,4,125:r4,3,4,25:r5,3,0,40:r6,4,0,37.5",
     expect={"@-p_e": 20, "@-i_e": 0.5},
     shownames={"@-i_e": "-i_e", "@-p_e": "-p_e"},
     letters={"@-i_e": "a"},
     evals=[dict(text="**b)** The power it supplies is read off its card:", keys=["@-p_e"])],
     booknames={"@-i_e": "i", "@-p_e": "p"},
     delivered=["@-p_e"],
     shows="The circuit is a bridge: five resistors in a diamond with a sixth across "
           "the middle, fed by one source. The question wants what that source "
           "delivers, its current and its power. We write the bridge as it is drawn, "
           "naming the source `e` and the six resistors `r1` to `r6`.",
     interpret="The source's card reports the power it delivers as `-pe`, which is the "
           "power the question asks for. Its current it reports *into* the source, the "
           "same way as for every other element, so the current it supplies is the "
           "negative of that, which we read with a minus sign in the {{card:Evaluate}} "
           "card."),

dict(num="4.4", title="Using the Node-Voltage Method with Dependent Sources",
     ask="Find the power dissipated in the 5 Ω resistor in the circuit shown in the figure.",
     page=125, fig=(125, "4.10"), domain="dc",
     desc="e1,1,0,20:r1,1,2,2:r2,2,0,20:r3,2,3,5:r4,3,0,10:r5,3,4,2:e2,4,0,8*ir3",
     expect={"p_r3": 7.2},
     booknames={"p_r3": "p"},
     shows="The circuit is resistive, with a dependent voltage source at its far end. "
           "Its value is eight times $i_\\phi$, the current through the 5 Ω resistor, "
           "and the question wants the power that resistor dissipates. In Symbulator a "
           "dependent source needs no special element. It is a source whose value "
           "names another answer. We name the 5 Ω resistor `r3`, so its current is "
           "`ir3`, and write the dependent source as `e2` with the value `8*ir3`. We "
           "number the nodes 1 to 4 from the source rightward, with the bottom rail as "
           "ground. The power asked for is then `pr3`, the power consumed by `r3`."),

dict(num="4.7", title="Using the Mesh-Current Method with Dependent Sources",
     ask="Find the power dissipated in the 4 Ω resistor in the circuit shown in the figure.",
     page=133, fig=(133, "4.23"), domain="dc",
     desc="e1,1,0,50:r1,1,3,1:r2,1,2,5:r3,2,3,4:r4,2,0,20:e2,3,0,15*ir4",
     expect={"p_r3": 16},
     booknames={"p_r3": "p"},
     shows="The circuit again has a dependent voltage source, this time worth fifteen "
           "times $i_\\phi$, the current in the 20 Ω resistor, and again the question "
           "wants one resistor's power, the 4 Ω's. We name the 20 Ω `r4`, so its "
           "current is `ir4` and the source `e2` has the value `15*ir4`. The 4 Ω we "
           "name `r3`, and its power is `pr3`. We number the nodes 1 to 3 with the "
           "bottom rail as ground."),

dict(num="4.21", title="Calculating the Condition for Maximum Power Transfer",
     ask="a) For the circuit shown in the figure, find the value of $R_L$ that results in "
         "maximum power being transferred to $R_L$. b) Calculate the maximum power that can "
         "be delivered to $R_L$.",
     page=153, fig=(153, "4.65"), kind="th", n1="2", n2="0", domain="dc",
     desc="e,1,0,360:r1,1,2,30:r2,2,0,150",
     expect={"z": 25, "pmax": 900},
     letters={"z": "a", "pmax": "b"},
     booknames={"z": "R_L", "pmax": "p_{max}"},
     shows="The circuit consists of a source and two resistors with a load $R_L$ "
           "connected across the second, and the question is which load draws the most "
           "power from those terminals, and how much. That is a question about the "
           "circuit *seen from* the load, so we describe the source and the two "
           "resistors and leave $R_L$ out, calling its terminals node **2** and "
           "ground. The {{card:Find equivalent}} card, with *Thévenin / Norton* chosen "
           "and those two terminals named, reduces the circuit to its Thévenin "
           "equivalent and reports beside it the load that would draw the most power "
           "and how much that is: by the maximum power theorem that load equals the "
           "Thévenin resistance, which the card reports as `req`, and the power it "
           "reports as `pmax`."),
]

SPECS += [
dict(num="4.8", title="A Special Case in the Mesh-Current Method",
     ask="Find the branch currents $i_a$, $i_b$ and $i_c$ in the circuit for Example 4.3, "
         "repeated here in the figure.",
     page=134, fig=(134, "4.25"), domain="dc",
     desc="e,1,0,50:r1,1,2,5:r2,2,0,10:r3,2,0,40:j,0,2,3",
     expect={"i_r1": 2, "i_r2": 4, "i_r3": 1},
     booknames={"i_r1": "i_a", "i_r2": "i_b", "i_r3": "i_c"},
     shows="The circuit consists of a voltage source and a current source feeding "
           "three resistors, and the question wants the current in each of the three "
           "branches. We name the sources `e` and `j` and the resistors `r1` to `r3`, "
           "and take the bottom rail as ground. A current source is written like a "
           "voltage source, name, two nodes, value, and its current flows through it "
           "from the first node to the second. The 3 A source's arrow points up from "
           "the bottom rail into node 2, so we write it `j,0,2,3`. We write each "
           "resistor's nodes in the direction of the figure's arrow, so that its "
           "current is counted as the book counts it: $i_a$ is `ir1`, $i_b$ is `ir2` "
           "and $i_c$ is `ir3`."),

dict(num="4.13", title="Using Special Source Transformation Techniques",
     ask="a) Find the voltage $v_o$ in the circuit shown in the figure. b) Find the power "
         "developed by the 250 V voltage source. "
         "c) Find the power developed by the 8 A current source.",
     page=143, fig=(143, "4.42"), domain="dc",
     desc="e,1,0,250:r1,1,0,125:r2,1,2,25:j,2,9,8:r3,9,0,10:r4,2,0,100:r5,2,3,5:r6,3,0,15",
     expect={"v_r4": 20, "@-p_e": 2800, "@-p_j": 480},
     shownames={"@-p_e": "-p_e", "@-p_j": "-p_j"},
     letters={"v_r4": "a", "@-p_e": "b", "@-p_j": "c"},
     booknames={"v_r4": "v_o", "@-p_e": "p_{250\\,V}", "@-p_j": "p_{8\\,A}"},
     shows="The circuit consists of two sources, one of voltage and one of current, "
           "and six resistors. The question wants the voltage across the 100 Ω, and "
           "the power each source develops. We write every element as it stands in the "
           "figure, the 125 Ω across the voltage source and the 10 Ω under the "
           "current source included, naming the resistors `r1` to `r6` from left to "
           "right and the sources `e` and `j`. The current source's arrow points down, "
           "from node 2 towards the 10 Ω, so we write its nodes in that order, "
           "`j,2,9,8`, calling the node between the source and the resistor **9**. "
           "$v_o$ is the voltage across `r4`.",
     delivered=["@-p_e", "@-p_j"],
     interpret="The power a source *develops* is what it delivers, which each source's "
           "card reports as `-pe` and `-pj`."),

dict(num="4.23", title="Using Superposition to Solve a Circuit with Dependent Sources",
     ask="Find $v_o$ in the circuit shown in the figure.",
     page=156, fig=(156, "4.71"), domain="dc",
     desc="e1,1,c,10:r1,1,a,5:r2,a,c,20:r3,b,0,10:j1,0,b,5:j2,b,a,0.4*vr3:e2,0,c,2*ir1",
     expect={"v_r2": 24},
     booknames={"v_r2": "v_o"},
     shows="The circuit consists of two independent sources, two dependent ones and "
           "three resistors, and the question wants the voltage across the 20 Ω. We "
           "name the 5 Ω resistor `r1`, the 20 Ω `r2` and the 10 Ω `r3`. The dependent "
           "current source is worth $0.4v_\\Delta$, and $v_\\Delta$ is the voltage "
           "across the 10 Ω, so we write its value as `0.4*vr3`. The dependent voltage "
           "source is worth $2i_\\Delta$, and $i_\\Delta$ is the current through the 5 "
           "Ω, so we write its value as `2*ir1`. We write each source's nodes in the "
           "order its arrow or its polarity marks give, name the three inner nodes "
           "**a**, **b** and **c**, and take the bottom-right node as ground. $v_o$ is "
           "the voltage across `r2`."),

dict(num="5.1", title="Analyzing an Op Amp Circuit",
     ask="The op amp in the circuit shown in the figure is ideal. a) Calculate $v_o$ if "
         "$v_a$ = 1 V and $v_b$ = 0 V. b) Repeat (a) for $v_a$ = 1 V and $v_b$ = 2 V. "
         "c) If $v_a$ = 1.5 V, specify the range of $v_b$ that avoids amplifier saturation.",
     page=181, fig=(181, "5.7"), domain="dc",
     desc="ea,1,0,va:r1,1,2,25'k:r2,2,3,100'k:eb,4,0,vb:o,4,2,3",
     expect={"v_3": "5*vb - 4*va"},
     booknames={"v_3": "v_o"},
     evals=[
      dict(text="Part (a) is that formula at $v_a$ = 1 V and $v_b$ = 0 V. We type the "
                "output's name into {{card:Evaluate}} and the two values into its "
                "{{ui:Conditions}} box:",
           expr="v_3", at={"va": 1, "vb": 0}, unit="V", expect=-4, book="v_o"),
      dict(text="Part (b) changes only the second condition:",
           expr="v_3", at={"va": 1, "vb": 2}, unit="V", expect=6, book="v_o"),
     ],
     solveq=[
      dict(tag="DC, Solve at the +10 V rail",
           text="Part (c) asks where saturation begins. The op amp is linear while its "
                "output lies between the supply rails, which the figure gives as ±10 V, so "
                "the question is which $v_b$ puts the output exactly on a rail. That is a "
                "question for the {{card:Solve}} card: the output on the upper rail is the "
                "equation, $v_b$ the unknown, and $v_a$ = 1.5 V a condition:",
           equations=["v_3=10"], unknowns=["vb"], conditions=["va=1.5"],
           real_only=True, expect={"vb": 3.2}, unit="V", book={"vb": "v_b"}),
      dict(tag="DC, Solve at the -10 V rail", entry=False, boxes=("equations",),
           text="For the lower rail we keep the unknown and the condition and change only "
                "the equation:",
           press="Then press {{btn:Solve equations}} again.",
           equations=["v_3=-10"], unknowns=["vb"], conditions=["va=1.5"],
           real_only=True, expect={"vb": -0.8}, unit="V", book={"vb": "v_b"}),
     ],
     parts=[
      ("a", "So {{var:v_o}} = {{o:-4}} V, inside the ±10 V supplies: the op amp is in "
            "its linear region and that is the answer."),
      ("b", "Now {{var:v_o}} = {{o:6}} V, which is inside the supplies again."),
      ("c", "The output reaches +10 V at {{var:v_b}} = {{o:3.2}} V and −10 V at "
            "{{var:v_b}} = {{o:-0.8}} V, so the op amp avoids saturation for "
            "{{o:-0.8}} V ≤ {{var:v_b}} ≤ {{o:3.2}} V."),
     ],
     shows="The circuit is an op amp with two inputs, $v_a$ into the inverting side "
           "through a 25 kΩ resistor and $v_b$ straight into the non-inverting side, "
           "with a 100 kΩ feedback resistor. The question wants the output for two "
           "pairs of input values, and then the range of one input that keeps the "
           "amplifier out of saturation. An ideal op amp is the element `o`, whose "
           "three nodes are its non-inverting input, its inverting input and its "
           "output, in that order. We choose to write the two inputs as voltage "
           "sources with the symbolic values `va` and `vb` rather than the numbers in "
           "the question, so that one run returns the output as a formula in both, and "
           "each part can then be asked of that formula. We name the sources `ea` and "
           "`eb`, the resistors `r1` and `r2`, and number the nodes from the $v_a$ "
           "input, the output being node **3**. Symbulator's ideal op amp has no "
           "supplies, so it reports whatever output the inputs demand. Whether that "
           "output is within the ±10 V supplies of the figure is something we check "
           "afterwards."),
]

SPECS += [
dict(num="5.3", title="Designing a Summing Amplifier",
     ask="a) You have designed a summing amplifier, as per the problem's specifications. "
         "Verify that its output voltage is $v_o = -4v_a - v_b - 5v_c$, using an ideal "
         "op amp with ±12 V power supplies and a 20 kΩ feedback resistor. b) Suppose "
         "$v_a$ = 2 V and $v_c$ = $-$1 V. "
         "What range of input voltages for $v_b$ allows the op amp to remain linear?",
     page=185, fig=(185, "5.12"), domain="dc",
     desc="ea,1,0,va:eb,2,0,vb:ec,3,0,vc:r1,1,n,5'k:r2,2,n,20'k:r3,3,n,4'k:rf,n,4,20'k:o,0,n,4",
     expect={"v_4": "-4*va - vb - 5*vc"},
     booknames={"v_4": "v_o"},
     solveq=[
      dict(tag="DC, Solve at the -12 V rail",
           text="Part (b) fixes two of the inputs and asks for the range of the third "
                "that keeps the output between the ±12 V rails. In the {{card:Solve}} card "
                "we put the output on the lower rail as the equation, name $v_b$ as the "
                "unknown, and give the two fixed inputs as conditions:",
           equations=["v_4=-12"], unknowns=["vb"], conditions=["va=2", "vc=-1"],
           real_only=True, expect={"vb": 9}, unit="V", book={"vb": "v_b"}),
      dict(tag="DC, Solve at the +12 V rail", entry=False, boxes=("equations",),
           text="For the upper rail we change only the equation:",
           press="Then press {{btn:Solve equations}} again.",
           equations=["v_4=12"], unknowns=["vb"], conditions=["va=2", "vc=-1"],
           real_only=True, expect={"vb": -15}, unit="V", book={"vb": "v_b"}),
     ],
     parts=[
      ("a", "The run returns exactly the formula the design was to produce, which "
            "verifies the three resistor values."),
      ("b", "The output sits on the −12 V rail at {{var:v_b}} = {{o:9}} V and on the "
            "+12 V rail at {{var:v_b}} = {{o:-15}} V, so the op amp remains linear for "
            "{{o:-15}} V ≤ {{var:v_b}} ≤ {{o:9}} V."),
     ],
     shows="The circuit is a summing amplifier, which adds several input voltages, "
           "each with its own gain, and inverts the sum. The question asks us to "
           "verify a design made for the gains given, then to find the range of one "
           "input that keeps it linear. The output of a summing amplifier with "
           "feedback resistor $R_f$ and input resistors $R_a$, $R_b$ and $R_c$ is $v_o "
           "= -(R_f/R_a)v_a - (R_f/R_b)v_b - (R_f/R_c)v_c$, so with $R_f$ fixed at 20 "
           "kΩ the gains of 4, 1 and 5 want $R_a$ = 20/4 = 5 kΩ, $R_b$ = 20/1 = 20 kΩ "
           "and $R_c$ = 20/5 = 4 kΩ. That is the design, and the run checks it. We "
           "describe the circuit with those four resistors, which we name `r1`, `r2`, "
           "`r3` and `rf`. We write the three inputs as sources `ea`, `eb` and `ec` "
           "with the symbolic values `va`, `vb` and `vc`, so that the output comes "
           "back as a formula, and we write the op amp `o` with its non-inverting "
           "input at ground, its inverting input at a node we call **n**, and its "
           "output at node **4**."),

dict(num="5.3c", title="Designing a Summing Amplifier - part (c), in Expert Mode",
     ask="c) Suppose $v_a$ = 2 V, $v_b$ = 3 V and $v_c$ = $-$1 V. Using the input resistor "
         "values found in part (a), how large can the feedback resistor be before the op amp "
         "saturates?",
     page=185, fig=(185, "5.12"), domain="dc",
     desc="ea,1,0,2:eb,2,0,3:ec,3,0,-1:r1,1,n,5'k:r2,2,n,20'k:r3,3,n,4'k:rf,n,4,rf:o,0,n,4",
     expect={"v_4": "-3*rf/10000"},
     booknames={"v_4": "v_o"},
     solveq=[
      dict(tag="DC, Solve for rf",
           text="The output is negative for any feedback resistor, so the rail it can "
                "reach is −12 V, and the largest feedback resistor is the one that puts "
                "the output exactly there. In the {{card:Solve}} card that is one equation "
                "and one unknown:",
           equations=["v_4=-12"], unknowns=["rf"], conditions=[],
           real_only=True, expect={"rf": 40000}, unit="\\Omega", book={"rf": "R_f"}),
     ],
     parts=[
      ("c", "So the feedback resistor can be as large as {{o:40000}} Ω, 40 kΩ. Any larger "
            "and the output would have to go beyond −12 V, which it cannot: the op amp "
            "saturates."),
     ],
     shows="The circuit is the same summing amplifier with the three inputs now given "
           "as numbers, and the question is turned round: not the output for a given "
           "feedback resistor, but the largest feedback resistor for which the output "
           "stays within the rails. We describe the circuit as in part (a), the inputs "
           "as sources of 2, 3 and −1 V, and leave the feedback resistor as the "
           "symbol `rf` instead of a number, so that the run returns the output as a "
           "formula in `rf`."),

dict(num="5.5", title="Designing a Difference Amplifier",
     ask="a) You have designed a difference amplifier, as per the problem's "
         "specifications. Verify that it amplifies the difference between two input "
         "voltages by a gain of 8, using an ideal op amp and ±8 V power supplies. "
         "b) Suppose $v_a$ = 1 V. What range of $v_b$ keeps the op amp linear?",
     page=189, fig=(189, "5.16"), domain="dc",
     desc="ea,1,0,va:eb,2,0,vb:ra,1,n,1.5'k:rb,n,3,12'k:rc,2,p,1.5'k:rd,p,0,12'k:o,p,n,3",
     expect={"v_3": "8*vb - 8*va"},
     booknames={"v_3": "v_o"},
     solveq=[
      dict(tag="DC, Solve at the +8 V rail",
           text="Part (b) fixes $v_a$ and asks for the range of $v_b$ that keeps the "
                "output between the ±8 V rails. In the {{card:Solve}} card, the output on "
                "the upper rail is the equation, $v_b$ the unknown and $v_a$ = 1 V a "
                "condition:",
           equations=["v_3=8"], unknowns=["vb"], conditions=["va=1"],
           real_only=True, expect={"vb": 2}, unit="V", book={"vb": "v_b"}),
      dict(tag="DC, Solve at the -8 V rail", entry=False, boxes=("equations",),
           text="For the lower rail we change only the equation:",
           press="Then press {{btn:Solve equations}} again.",
           equations=["v_3=-8"], unknowns=["vb"], conditions=["va=1"],
           real_only=True, expect={"vb": 0}, unit="V", book={"vb": "v_b"}),
     ],
     parts=[
      ("a", "The run returns exactly 8({{var:v_b}} − {{var:v_a}}), the gain the design "
            "was to produce, which verifies it."),
      ("b", "The output reaches +8 V at {{var:v_b}} = {{o:2}} V and −8 V at "
            "{{var:v_b}} = {{o:0}} V, so the op amp remains linear for "
            "{{o:0}} V ≤ {{var:v_b}} ≤ {{o:2}} V."),
     ],
     shows="The circuit is a difference amplifier, which amplifies the difference "
           "between its two inputs. The question asks us to verify a design made for a "
           "gain of 8, then to find the range of one input that keeps it linear. Its "
           "output is $v_o = (R_b/R_a)(v_b - v_a)$, provided the four resistors "
           "satisfy $R_a/R_b = R_c/R_d$, so a gain of 8 needs $R_b$ eight times $R_a$ "
           "and $R_d$ eight times $R_c$. One choice, the book's, is $R_a$ = $R_c$ = "
           "1.5 kΩ and $R_b$ = $R_d$ = 12 kΩ. We describe the circuit with those "
           "values, naming the resistors `ra` to `rd` after the book's, write the two "
           "inputs as sources with the symbolic values `va` and `vb` so that the "
           "output comes back as a formula, and call the op amp's two input nodes "
           "**p** and **n** and its output node **3**. The run checks the design."),

dict(num="5.7", digits=5, title="Analyzing a Noninverting-Amplifier Circuit Using a Realistic Op Amp Model",
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
     shows="The circuit is a noninverting amplifier built not round an ideal op amp "
           "but round a realistic model of one: a dependent voltage source with a "
           "large but finite gain, an input resistance between its two inputs, and an "
           "output resistance in series with its output. The question wants the gain "
           "of the whole amplifier, output over source. We write the model as those "
           "three ordinary elements. We call the op amp's two input nodes **p** and "
           "**n**, write the input resistance as `ri` between them, the output "
           "resistance as `ro`, and the dependent source as `ea` with the value "
           "`50000*(vp-vn)`, the open-loop gain times the voltage between the inputs, "
           "$A(v_p - v_n)$. The other three resistors are `rg`, `rs` and `rf`. We "
           "leave the source as the symbol `vg`, so that the output comes back as a "
           "multiple of it. The gain is that multiple, which we will read in the "
           "{{card:Evaluate}} card."),

dict(num="7.1", title="Determining the Natural Response of an RL Circuit",
     ask="The switch in the circuit shown in the figure has been closed for a long time before "
         "it is opened at $t$ = 0. Find a) $i_L(t)$ for $t$ ≥ 0, b) $i_o(t)$ for "
         "$t$ ≥ 0+, c) $v_o(t)$ for $t$ ≥ 0+.",
     page=250, fig=(250, "7.6"), domain="tr",
     pre=[dict(
        text="The circuit consists of an inductor that has been fed by a current "
             "source for a long time, and a switch that then cuts the source off and "
             "leaves the inductor to discharge through three resistors. The question "
             "wants the inductor's current and two other quantities afterwards, as "
             "functions of time. There are two intervals, and two runs. Before $t$ = 0 "
             "the switch has been closed for a long time, so any transient has died "
             "away and every current is steady. In a steady circuit an inductor "
             "carries its current with no voltage across it, which is to say it "
             "behaves as a wire. The full current of the source, 20 A, would run "
             "through it, and should be the initial condition of the inductor. To "
             "verify this intuition, we can run a DC simulation. Describe the circuit "
             "as it stands before the switch opens, the 20 A source, the 0.1 Ω "
             "resistor, the inductor and the three resistors beyond it, and run it for "
             "the inductor's current. We name the source `j`, the inductor `l` and "
             "the resistors `r0` to `r3`, and write the inductor with no fifth field, "
             "since nothing about its past is being told:",
        desc="j,0,1,20:r0,1,0,0.1:l,1,0,2:r1,1,2,2:r2,2,0,10:r3,2,0,40",
        tag="DC, before the switch opens",
        expect={"i_l": 20}, booknames={"i_l": "i_L(0)"},
        note="This is the circuit before the switch opens, run in DC to find the "
             "inductor's current, which the next entry takes as its initial condition.")],
     desc="l,1,0,2,20:r1,1,2,2:r2,2,0,10:r3,2,0,40",
     expect={"i_l": "20*exp(-5*t)", "i_r3": "-4*exp(-5*t)", "v_2": "-160*exp(-5*t)"},
     letters={"i_l": "a", "i_r3": "b", "v_2": "c"},
     booknames={"i_l": "i_L", "i_r3": "i_o", "v_2": "v_o"},
     shows="Opening the switch disconnects the source and the 0.1 Ω resistor and leaves "
           "the inductor to release its energy through the three resistors. That is the "
           "circuit for the second interval, $t$ ≥ 0, and we describe it with the same "
           "names, dropping `j` and `r0`. The inductor now starts with the 20 A just "
           "found, which we write into its line as a fifth field, after the inductance. "
           "The answers come back as functions of $t$: "
           "$i_L$ is the current through `l`, $i_o$ the current through `r3`, and $v_o$ "
           "the voltage at node 2."),
]

SPECS += [
dict(num="7.3", title="Determining the Natural Response of an RC Circuit",
     ask="The switch in the circuit shown in the figure has been in position x for a long "
         "time. At $t$ = 0 it moves instantaneously to position y. Find a) $v_C(t)$ for "
         "$t$ ≥ 0, b) $v_o(t)$ for $t$ ≥ 0+, and c) $i_o(t)$ for $t$ ≥ 0+.",
     page=256, fig=(256, "7.15"), domain="tr",
     pre=[dict(
        text="The circuit consists of a capacitor charged from one source, then "
             "switched over to a set of resistors to discharge. The question wants its "
             "voltage and two other quantities after the switch moves. There are two "
             "intervals, and two runs. At position x the capacitor has been connected "
             "to the 100 V source through the 10 kΩ resistor for a long time, and a "
             "capacitor in a steady circuit carries no current, so nothing flows in "
             "the 10 kΩ and the capacitor sits at the voltage of the source, 100 V, "
             "which would be its initial condition for the next interval. To confirm "
             "that intuition, we describe that circuit, the source, the 10 kΩ, which "
             "we name `r0`, and the capacitor, written without a fifth field, and run "
             "it in DC to find the capacitor's voltage:",
        desc="e,1,0,100:r0,1,2,10'k:c,2,0,0.5'u",
        tag="DC, before the switch moves",
        expect={"v_2": 100}, booknames={"v_2": "v_C(0)"},
        note="This is the circuit at position x, before the switch moves, run in DC to "
             "find the capacitor's voltage, which the next entry takes as its initial "
             "condition.")],
     desc="c,1,0,0.5'u,100:r1,1,2,32'k:r2,2,0,240'k:r3,2,0,60'k",
     expect={"v_1": "100*exp(-25*t)", "v_2": "60*exp(-25*t)",
             "i_r3": "0.001*exp(-25*t)"},
     letters={"v_1": "a", "v_2": "b", "i_r3": "c"},
     booknames={"v_1": "v_C", "v_2": "v_o", "i_r3": "i_o"},
     shows="At position y the capacitor is connected instead to the 32 kΩ resistor and "
           "the two beyond it, and discharges through them. We describe that second "
           "circuit with the 100 V just found as the capacitor's fifth field, naming the "
           "three resistors `r1` to `r3` and the capacitor's node **1**, and set the "
           "analysis to TR. $v_C$ is the voltage at node 1, $v_o$ the voltage at node 2, "
           "and $i_o$ the current through `r3`."),

dict(num="7.5", title="Determining the Step Response of an RL Circuit",
     ask="The switch in the circuit shown in the figure has been in position a for a long "
         "time. At $t$ = 0 it moves from position a to position b. The switch is a "
         "make-before-break type, so the inductor current is continuous. a) Find the "
         "expression for $i(t)$ for $t$ ≥ 0. b) What is the initial voltage across the "
         "inductor just after the switch has been moved to position b?",
     page=260, fig=(260, "7.21"), domain="tr",
     pre=[dict(
        text="The circuit consists of an inductor that has been carrying a current "
             "from one source and is switched, without a break, onto another. The "
             "question wants its current afterwards and the voltage across it the "
             "instant after the switch moves. There are two intervals, and two runs. "
             "With the switch at position a, the inductor has been in parallel with "
             "the 10 Ω resistor and the 8 A source for a long time, so the circuit is "
             "steady. The inductor behaves as a wire, so the whole 8 A would flow "
             "through it and none through the resistor, and that, with its sign, "
             "should be its initial condition. To verify this intuition, we can run a "
             "DC simulation. The direction matters: the source's arrow points down "
             "through the source, so its current comes up through the inductor, "
             "against the book's arrow for $i$. We write the source as `j,1,0,8`, its "
             "current flowing from node 1 down to ground, and the inductor as "
             "`l,1,0,0.2`, so that its current is counted downward like the book's "
             "$i$. A DC run then gives the current with its sign:",
        desc="j,1,0,8:r,1,0,10:l,1,0,0.2",
        tag="DC, at position a",
        expect={"i_l": -8}, booknames={"i_l": "i(0)"},
        note="This is the circuit at position a, before the switch moves, run in DC to "
             "find the inductor's current, which the next entry takes as its initial "
             "condition.")],
     desc="e,1,0,24:r1,1,2,2:l,2,0,0.2,-8",
     expect={"i_l": "12 - 20*exp(-10*t)", "v_2": "40*exp(-10*t)"},
     letters={"i_l": "a"},
     booknames={"i_l": "i"}, hide=["v_2"],
     evals=[dict(
        text="**b)** The inductor is between node 2 and ground, so the voltage across it is "
             "`v_2`, and we read its value the instant after the switch has moved, at "
             "$t$ = 0, with {{card:Evaluate}}:",
        expr="v_2", at={"t": 0}, unit="V", expect=40, book="v(0^+)")],
     shows="Moving the switch to b connects the inductor, through the 2 Ω resistor, to "
           "the 24 V source instead. Because the switch is make-before-break, the "
           "inductor's current does not jump at the switching: it starts at the −8 A just "
           "found. We describe the second circuit with that −8 as the inductor's fifth "
           "field, sign included, naming the source `e` and the resistor `r1`, and set "
           "the analysis to TR. $i$ is the current through `l`."),

dict(num="7.10", title="Determining the Step Response of a Circuit with Magnetically Coupled Coils",
     ask="There is no energy stored in the circuit in the figure at the time the switch is "
         "closed. Find the solutions for $i_o$, $v_o$, $i_1$ and $i_2$.",
     page=271, fig=(271, "7.37"), domain="tr",
     desc="e,1,0,120:r1,1,2,7.5:l1,2,0,3:l2,2,0,15:m,l1,l2,6",
     expect={"i_r1": "16 - 16*exp(-5*t)", "v_2": "120*exp(-5*t)",
             "i_l1": "24 - 24*exp(-5*t)", "i_l2": "-8 + 8*exp(-5*t)"},
     booknames={"i_r1": "i_o", "v_2": "v_o", "i_l1": "i_1", "i_l2": "i_2"},
     shows="The circuit consists of two coils wound on one core, both fed from the "
           "same node through one resistor, and a switch that connects the source at "
           "$t$ = 0. The question wants the source's current, the voltage across the "
           "coils and the current in each, all as functions of time. We write each "
           "coil as an inductor line of its own, `l1` and `l2`, and the coupling "
           "between them as the `m` line, which names the two coils and their mutual "
           "inductance, 6 H. No energy is stored, so we write neither inductor with a "
           "fifth field. The switch closing at $t$ = 0 needs no element: in TR a "
           "source with a plain numerical value is a step that begins at $t$ = 0, "
           "which is exactly what closing the switch on the 120 V source does. We name "
           "the source `e` and the resistor `r1`, and set the analysis to TR. $i_o$ "
           "is the current through `r1`, $v_o$ the voltage at node 2, and $i_1$ and "
           "$i_2$ the currents through `l1` and `l2`."),

dict(num="7.11a", title="Analyzing an RL Circuit That Has Sequential Switching (0 to 35 ms)",
     ask="The two switches in the circuit shown in the figure have been closed for a long "
         "time. At $t$ = 0 switch 1 is opened; then, 35 ms later, switch 2 is opened. "
         "a) Find $i_L(t)$ for 0 ≤ $t$ ≤ 35 ms.",
     page=273, fig=(273, "7.39"), domain="tr",
     pre=[dict(
        text="The circuit has an inductor and two switches that open one after the "
             "other. The question wants the inductor's current between the two "
             "openings. There are three intervals this time, and three runs. In the "
             "first, both switches have been closed for a long time and the circuit is "
             "steady. We describe the whole circuit, the 60 V source, the 4 Ω, 12 Ω, "
             "6 Ω and 3 Ω resistors, the inductor and the 18 Ω, naming each resistor "
             "after its value, and run it in DC for the inductor's current:",
        desc="e,1,0,60:r4,1,2,4:r12,2,0,12:r6,2,0,6:r3,2,3,3:l,3,0,0.15:r18,3,0,18",
        tag="DC, both switches closed",
        expect={"i_l": 6}, booknames={"i_l": "i_L(0)"},
        note="This is the circuit with both switches closed, run in DC to find the "
             "inductor's current, which the next entry takes as its initial condition.")],
     desc="r6,2,0,6:r3,2,3,3:l,3,0,0.15,6:r18,3,0,18",
     expect={"i_l": "6*exp(-40*t)"},
     letters={"i_l": "a"},
     booknames={"i_l": "i_L"},
     evals=[dict(
        text="This run holds until switch 2 opens at 35 ms, and the inductor's current at "
             "that instant is where the third interval starts. We read it from the answer "
             "with {{card:Evaluate}}, giving the instant in seconds:",
        expr="i_l", at={"t": 0.035}, unit="A", expect=1.48, book="i_L(35\\,\\mathrm{ms})")],
     shows="In the second interval switch 1 has opened, which disconnects the 60 V source "
           "and the 4 Ω and 12 Ω resistors. We describe what remains, the 6 Ω, the 3 Ω, "
           "the inductor and the 18 Ω, with the same names, and give the inductor the 6 A "
           "just found as its fifth field. $i_L$ is the "
           "current through `l`."),

dict(num="7.11b", title="Analyzing an RL Circuit That Has Sequential Switching (after 35 ms)",
     ask="b) Find $i_L(t)$ for $t$ ≥ 35 ms. (Time is measured from the second switching.)",
     page=273, fig=(273, "7.39"), domain="tr",
     desc="r6,2,0,6:r3,2,3,3:l,3,0,0.15,6*exp(-1.4)",
     expect={"i_l": "6*exp(-1.4)*exp(-60*t)"},
     letters={"i_l": "b"},
     booknames={"i_l": "i_L"},
     shows="This is the third interval of the same problem: switch 2 has opened too, "
           "removing the 18 Ω resistor, so the inductor now discharges through the 3 Ω "
           "and 6 Ω alone, and the question wants its current from that moment on. We "
           "describe that circuit with the 18 Ω dropped, and give the inductor as its "
           "fifth field the current found at the end of the previous entry, $6e^{-40 "
           "\\times 0.035} = 6e^{-1.4}$, about 1.48 A. We write it as the expression "
           "`6*exp(-1.4)`, which is exact. We measure time from the second switching, "
           "as the book does, so this run's $t$ = 0 is the instant switch 2 opens. The "
           "analysis is TR."),

dict(num="7.13", title="Finding the Unbounded Response in an RC Circuit",
     ask="a) When the switch is closed in the circuit shown in the figure, the voltage on the "
         "capacitor is 10 V. Find the expression for $v_o$ for $t$ ≥ 0. b) Assume that the "
         "capacitor short-circuits when its terminal voltage reaches 150 V. How many "
         "milliseconds elapse before the capacitor short-circuits?",
     page=277, fig=(277, "7.45"), domain="tr",
     desc="c,1,0,5'u,10:r1,1,0,10'k:r2,1,0,20'k:j,0,1,7*ir2",
     expect={"v_1": "10*exp(40*t)"},
     letters={"v_1": "a"},
     booknames={"v_1": "v_o"},
     solveq=[dict(
        tag="TR, Solve for the time to 150 V",
        text="The exponent is positive, so the voltage grows instead of decaying: the "
             "dependent source feeds the capacitor faster than the resistors drain it."
             "\n\n**b)** The time it takes to reach 150 V is a question for the "
             "{{card:Solve}} card, with the time as the unknown:",
        equations=["v_1=150"], unknowns=["t"], conditions=[],
        real_only=True, expect={"t": 0.0677}, unit="s", book={"t": "t"})],
     after="So the capacitor short-circuits after {{o:67.7}} ms.",
     shows="The circuit consists of a charged capacitor across two resistors and a "
           "dependent current source whose value is seven times the current in one of "
           "the resistors. The question wants the capacitor's voltage as a function of "
           "time, and then how long it takes to reach 150 V. The 10 V on the "
           "capacitor is given, and we write it into the capacitor's fifth field. We "
           "name the 20 kΩ resistor `r2`, so its current is `ir2` and the dependent "
           "source's value is `7*ir2`. The source's arrow points up into node 1, so we "
           "write it `j,0,1,7*ir2`. We set the analysis to TR. $v_o$ is the voltage "
           "at node 1."),

dict(num="8.2", title="Finding the Overdamped Natural Response of a Parallel RLC Circuit",
     ask="For the circuit in the figure, $v(0^+)$ = 12 V and $i_L(0^+)$ = 30 mA. Find the "
         "expression for $v(t)$. (Example 8.3 asks the same circuit for its three branch "
         "currents.)",
     page=306, fig=(306, "8.6"), domain="tr",
     desc="c,1,0,0.2'u,12:l,1,0,50'm,0.03:r,1,0,200",
     expect={"v_1": "-14*exp(-5000*t) + 26*exp(-20000*t)",
             "i_r": "-0.07*exp(-5000*t) + 0.13*exp(-20000*t)",
             "i_l": "0.056*exp(-5000*t) - 0.026*exp(-20000*t)"},
     booknames={"v_1": "v", "i_r": "i_R", "i_l": "i_L"},
     shows="The circuit consists of a capacitor, an inductor and a resistor in "
           "parallel with no source, holding an initial voltage and an initial "
           "current. The question wants the voltage across the three as a function of "
           "time, and the following example wants the three branch currents. We write "
           "each element as a line between node 1 and ground, naming them `c`, `l` and "
           "`r`, and put the two initial conditions the question gives in the fifth "
           "fields: 12 V on the capacitor and 30 mA, written 0.03, on the inductor. "
           "The run is the circuit releasing the energy it holds. $v$ is the voltage "
           "at node 1, and $i_R$ and $i_L$ the currents through `r` and `l`."),

dict(num="8.4", title="Finding the Underdamped Natural Response of a Parallel RLC Circuit",
     ask="In the circuit shown in the figure, $V_0$ = 0 and $I_0$ = $-$12.25 mA. Calculate "
         "the voltage response for $t$ ≥ 0.",
     page=310, fig=(310, "8.8"), domain="tr", at_t=[1e-4, 5e-4, 1e-3, 3e-3],
     desc="c,1,0,125'n,0:l,1,0,8,-0.01225:r,1,0,20'k",
     expect={"v_1": "100*exp(-200*t)*sin(979.80*t)"}, tol=3e-4,
     booknames={"v_1": "v"},
     digits=5,
     after="The book prints the amplitude as 100 and the frequency of the sine as "
           "979.80, both rounded. To the same figures the run gives 100.02 and 979.80.",
     shows="The circuit is the same three elements in parallel with different values, "
           "an initial current in the inductor and none on the capacitor. The question "
           "wants the voltage across them as a function of time. We describe them as "
           "before: $V_0$ = 0 goes in the capacitor's fifth field and $I_0$ = −12.25 "
           "mA in the inductor's, written −0.01225 with the sign the question gives "
           "it. We set the analysis to TR. $v$ is the voltage at node 1."),

dict(num="8.11", title="Finding the Natural Response of a Series RLC Circuit",
     ask="The 0.1 µF capacitor in the circuit shown in the figure is charged to 100 V. At "
         "$t$ = 0 the capacitor is discharged through a series combination of a 100 mH "
         "inductor and a 560 Ω resistor. a) Find $i(t)$ for $t$ ≥ 0. b) Find $v_C(t)$ for "
         "$t$ ≥ 0.",
     page=328, fig=(328, "8.17"), domain="tr",
     desc="c,1,0,0.1'u,100:l,2,1,0.1:r,2,0,560",
     expect={"i_l": "-0.1042*exp(-2800*t)*sin(9600*t)",
             "v_1": "(100*cos(9600*t) + 29.17*sin(9600*t))*exp(-2800*t)"},
     at_t=[3e-5, 1e-4, 3e-4], tol=1e-3,
     letters={"i_l": "a", "v_1": "b"},
     booknames={"i_l": "i", "v_1": "v_C"},
     shows="The circuit is a charged capacitor discharging round a loop through an "
           "inductor and a resistor. The question wants the loop current and the "
           "capacitor's voltage as functions of time. We write the capacitor with 100 "
           "V as its fifth field, and the inductor and the resistor after it round the "
           "loop, naming the three `c`, `l` and `r`. We write the inductor's nodes as "
           "2 then 1 on purpose, so that its current is counted in the direction of "
           "the book's arrow for $i$. Written the other way round, the answer would "
           "come back with its sign reversed. We set the analysis to TR. $i$ is the "
           "current through `l` and $v_C$ the voltage at node 1."),

dict(num="8.12", title="Finding the Step Response of a Series RLC Circuit",
     ask="No energy is stored in the 100 mH inductor or the 0.4 µF capacitor when the switch "
         "in the circuit shown in the figure is closed. Find $v_C(t)$ for $t$ ≥ 0.",
     page=328, fig=(328, "8.18"), domain="tr",
     desc="e,1,0,48:l,1,2,0.1:r,2,3,1250:c,3,0,0.4'u",
     expect={"v_3": "48 + 16*exp(-10000*t) - 64*exp(-2500*t)"},
     booknames={"v_3": "v_C"},
     shows="The circuit is a source switched at $t$ = 0 onto a loop of an inductor, a "
           "resistor and a capacitor, none of them holding any energy. The question "
           "wants the capacitor's voltage as a function of time. In TR a source with a "
           "plain numerical value is a step beginning at $t$ = 0, which is what the "
           "switch closing does, so the switch needs no element. We write the 48 V "
           "source and then the three elements in order round the loop, numbering the "
           "nodes 1 to 3, and write the inductor and the capacitor without a fifth "
           "field, since neither stores energy. We set the analysis to TR. $v_C$ is "
           "the voltage at node 3, the capacitor's upper end."),
]

import sympy as _sp
W = _sp.Symbol("omega")

SPECS += [
dict(num="9.9", title="Combining Impedances in Series and in Parallel",
     ask="The sinusoidal current source in the circuit shown in the figure produces the "
         "current $i_s$ = 8 cos 200,000$t$ A. b) Find the equivalent admittance to the right "
         "of the current source. c) Find the phasor voltage $v$. d) Find the phasor current "
         "$i$. e) Find the steady-state expressions for $v$ and $i$.",
     page=363, fig=(363, "9.20"), domain="ac", omega=200000,
     desc="j,0,1,8:r1,1,0,10:r2,1,2,6:l,2,0,40'u:c,1,0,1'u",
     expect={"v_1": 32 - 24j, "i_r2": -4j},
     booknames={"v_1": "v", "i_r2": "i"},
     evals=[dict(
        text="**b)** Symbulator reports the impedance seen by each source, here `z_j`, "
             "and the admittance the source sees is its reciprocal, so we type into "
             "{{card:Evaluate}}:",
        expr="1/z_j", unit="S", expect=0.16 + 0.12j, book="Y"),
        dict(text="**c)** and **d)** are read off the run:", keys=["v_1", "i_r2"])],
     after="**e)** The steady-state expressions are the two phasors written back as functions of time at the source's "
           "frequency, which is circuit theory rather than a run: $v$ = 40 cos(200,000$t$ "
           "− 36.87°) V and $i$ = 4 cos(200,000$t$ − 90°) A.",
     shows="The circuit consists of a sinusoidal current source at 200,000 rad/s "
           "feeding a resistor, a capacitor, and a branch of a resistor and an "
           "inductor. The question wants the admittance the source sees, the voltage "
           "across it and the current in the inductive branch as phasors, and those "
           "two as functions of time. The inductor and the capacitor are given as an "
           "inductance and a capacitance, and we write them as they are, `l,2,0,40'u` "
           "and `c,1,0,1'u`, putting the source's frequency, 200,000 rad/s, in the "
           "{{ui:ω — angular frequency}} box. The conversion to impedances is done "
           "inside the solver, so part (a), constructing the frequency-domain "
           "equivalent circuit, is out of scope for Symbulator and has been skipped. "
           "We write the current source as `j,0,1,8`, its arrow pointing up into node "
           "1, with its 8 A as the amplitude, which is what the book's phasors carry "
           "too, and name the resistors `r1` and `r2`. In AC each answer is a phasor, "
           "printed both as a complex number and as an amplitude with an angle: $v$ is "
           "the voltage at node 1 and $i$ the current through `r2`."),

dict(num="9.10", title="Using a Delta-to-Wye Transform in the Frequency Domain",
     ask="Find $I_0$, $I_1$, $I_2$, $I_3$, $I_4$, $I_5$, $V_1$ and $V_2$ in the circuit "
         "in the figure.",
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
     shows="The circuit is a bridge of five impedances fed by one source, every "
           "impedance given in ohms and several of them complex. The question wants "
           "the current in every branch and the voltage at two nodes. We write each "
           "impedance exactly as given, `-4j`, `63.2+2.4j`, `20+60j`, as a resistor "
           "with a complex value, naming the five `r1` to `r5` in the order of the "
           "book's $I_1$ to $I_5$, and we write each one's nodes in the direction of "
           "the figure's arrow, so that its current is counted as the book counts it. "
           "We keep the figure's letters for the nodes, with **d** as ground, so $V_1$ "
           "and $V_2$ are the voltages at **b** and **c**.",
     interpret="The source current $I_0$ leaves the source's positive terminal, which is "
           "the opposite of how Symbulator counts a source's current, so we read it with "
           "a minus sign in the {{card:Evaluate}} card."),

dict(num="9.12", title="Finding a Thevenin Equivalent in the Frequency Domain",
     ask="Find the Thevenin equivalent circuit with respect to terminals a,b for the "
         "circuit shown in the figure.",
     page=368, fig=(368, "9.32"), kind="th", n1="a", n2="0", domain="ac", omega=W,
     desc="e1,1,0,120:r1,1,2,12:r2,2,0,60:r3,2,a,-40j:e2,3,0,10*v2:r4,3,a,120",
     expect={"vth": 784 - 288j, "z": 91.2 - 38.4j},
     booknames={"vth": "V_{Th}", "z": "Z_{Th}"},
     shows="This is an AC circuit with a dependent source inside it, and the question "
           "wants its Thévenin equivalent, a voltage and an impedance, seen from two "
           "terminals. The dependent voltage source is worth ten times $V_x$, the "
           "voltage across the 60 Ω resistor. We name that resistor `r2` and place it "
           "between node 2 and ground, so that $V_x$ is the voltage at node 2 and the "
           "source's value is `10*v2`. The figure names the terminals a and b. "
           "Terminal b is the bottom rail, which we take as ground, so we keep **a** "
           "as the top terminal's node and name **a** and **0** to the {{card:Find "
           "equivalent}} card with *Thévenin / Norton* chosen, which returns the "
           "equivalent's voltage and impedance. A dependent source in the circuit is "
           "no obstacle to it."),

dict(num="9.14", title="Using the Mesh-Current Method in the Frequency Domain",
     ask="Find the voltages $V_1$, $V_2$ and $V_3$ in the circuit shown in the figure.",
     page=372, fig=(372, "9.39"), domain="ac", omega=W,
     desc="e1,a,0,150:r1,a,b,1+2j:r2,b,0,12-16j:r3,b,c,1+3j:e2,c,0,39*ir2",
     expect={"v_r1": 78 - 104j, "v_r2": 72 + 104j, "v_r3": 150 - 130j},
     booknames={"v_r1": "V_1", "v_r2": "V_2", "v_r3": "V_3"},
     shows="This is an AC circuit of two loops with a dependent voltage source in the "
           "far one, worth 39 times $I_x$, the current down through the middle branch. "
           "The question wants three voltages, each marked across a pair of "
           "impedances in series: $V_1$ across the 1 Ω and j2 Ω on the left, $V_2$ "
           "across the 12 Ω and −j16 Ω in the middle, $V_3$ across the 1 Ω and j3 Ω on "
           "the right. Nothing else connects inside a pair, so we write each pair as "
           "one impedance, `r1` worth `1+2j`, `r2` worth `12-16j` and `r3` worth "
           "`1+3j`, and each voltage asked is then that element's own drop. $I_x$ is "
           "the current through `r2`, so the dependent source's value is `39*ir2`. We "
           "name the source's top node **a**, the top of the middle branch **b** and "
           "the dependent source's top **c**."),

dict(num="9.15", title="Analyzing a Linear Transformer in the Frequency Domain",
     ask="A linear transformer has $R_1$ = 200 Ω, $R_2$ = 100 Ω, $L_1$ = 9 H, $L_2$ = 4 H "
         "and $k$ = 0.5, and couples a load of an 800 Ω resistor in series with a 1 µF "
         "capacitor to a 300 V (rms) source of internal impedance $500 + j100$ Ω at "
         "400 rad/s. g) Calculate the Thevenin equivalent with respect to the terminals of "
         "the load impedance.",
     page=375, fig=(376, "9.42"), nofig=True, kind="th", n1="c", n2="0", domain="ac", omega=400, rms=True,
     desc="e,1,0,300:r1,1,2,500:r2,2,a,100j:r3,a,p,200:l1,p,0,9:m,l1,l2,k=0.5:"
          "l2,q,0,4:r6,q,c,100",
     expect={"vth": 93.9351 + 17.7715j, "z": 171.086 + 1224.2595j}, tol=1e-4,
     booknames={"vth": "V_{Th}", "z": "Z_{Th}"},
     shows="The circuit consists of a linear transformer, two coupled coils each with "
           "its own winding resistance, between a source with an internal impedance "
           "and a load. The question wants the Thévenin equivalent seen from the "
           "load's terminals. Of the book's seven parts, (a) to (f) are the steps of "
           "its own method -- the frequency-domain equivalent circuit, the two "
           "self-impedances, the reflected impedance, its scaling factor and the "
           "impedance looking into the primary -- and are skipped. Only (g) asks about "
           "the circuit itself. The coils are given as inductances, so we write them "
           "as they are, `l1,p,0,9` and `l2,q,0,4`, and put the frequency, 400 rad/s, "
           "in the {{ui:ω — angular frequency}} box. The coupling the book gives as "
           "$k$, and the `m` line takes it as it is, `m,l1,l2,k=0.5`, naming the two "
           "coils. The mutual inductance is worked out inside. The winding resistances "
           "$R_1$ and $R_2$ we name `r3` and `r6`, and the source's internal "
           "impedance, given in ohms, `r1` and `r2`. We leave the load out, because "
           "the question asks for the equivalent seen from its terminals: we call the "
           "top one node **c** and take the bottom one as ground -- nothing conducts "
           "between the two windings, so joining their bottoms changes no current -- "
           "and name **c** and **0** to the {{card:Find equivalent}} card with "
           "*Thévenin / Norton* chosen."),
]

SPECS += [
dict(num="10.8", title="Balancing Power Delivered with Power Absorbed in an AC Circuit",
     ask="a) Calculate the total average and reactive power delivered to each impedance in "
         "the circuit shown in the figure. b) Calculate the average and reactive powers "
         "associated with each source. c) Verify that the average power delivered equals the "
         "average power absorbed, and likewise for the reactive power.",
     page=417, fig=(417, "10.18"), domain="ac", omega=W,
     desc="e1,a,0,150:r1,a,b,1+2j:r2,b,0,12-16j:r3,b,c,1+3j:e2,c,0,39*ir2",
     # Roberto, 14 Sep 2026: now that every card reads the real and the
     # reactive power, (a) and (b) are read as p and q off the cards, and
     # the two halves of (c) are the sum of all p and the sum of all q.
     expect={"p_r1": 1690, "q_r1": 3380, "p_r2": 240, "q_r2": -320,
             "p_r3": 1970, "q_r3": 5910,
             "@-p_e1": -1950, "@-q_e1": 3900, "@-p_e2": 5850, "@-q_e2": 5070,
             "@p_e1+p_e2+p_r1+p_r2+p_r3": 0, "@q_e1+q_e2+q_r1+q_r2+q_r3": 0},
     # the two sums are verified by the runner and shown as Evaluate steps
     hide=["@p_e1+p_e2+p_r1+p_r2+p_r3", "@q_e1+q_e2+q_r1+q_r2+q_r3"],
     booknames={"p_r1": "P_1", "q_r1": "Q_1", "p_r2": "P_2", "q_r2": "Q_2",
                "p_r3": "P_3", "q_r3": "Q_3"},
     delivered=["@-p_e1", "@-q_e1", "@-p_e2", "@-q_e2"],
     groups=[("**a)** The three impedances\' cards read",
              ["p_r1", "q_r1", "p_r2", "q_r2", "p_r3", "q_r3"]),
             ("**b)** The two sources\' cards read",
              ["@-p_e1", "@-q_e1", "@-p_e2", "@-q_e2"])],
     shows="This entry takes the circuit of Example 9.14, which we describe the same "
           "way, and asks a question about power: how much average and reactive power "
           "each of its three impedances takes, how much each source supplies, and "
           "whether what is delivered balances what is absorbed. One run answers all "
           "three parts.",
     interpret="Every card of an AC run carries two power rows, *average (real) "
               "power*, the answer `p`, and *reactive power*, the answer `q`. On an "
               "impedance they read *consumed*, and each impedance in the figure is "
               "one element of our description, so part (a) is read straight off the "
               "three cards. On a source they read *delivered*, `-p` and `-q`, the "
               "negatives of the `p` and `q` answers, so part (b) is read off the two "
               "source cards the same way. For part (c), if every watt delivered is "
               "absorbed somewhere, the five `p` answers add to zero, and likewise the "
               "five `q`, which makes two sums in the {{card:Evaluate}} card.",
     evals=[dict(text="**c)** We type the sum of the five `p` answers into "
                      "{{card:Evaluate}}:",
                 expr="p_e1+p_e2+p_r1+p_r2+p_r3", expect=0, unit="W"),
            dict(text="Then we do the same with the five `q`:",
                 expr="q_e1+q_e2+q_r1+q_r2+q_r3", expect=0, unit="var")],
     after="A negative reading is the same power the other way: the $12 - j16$ Ω "
           "impedance\'s `q_r2` = \u2212320 var means it delivers 320 var, and the "
           "independent source\'s `-p_e1` = \u22121950 W means it absorbs 1950 W. Both "
           "sums being zero, the average power delivered equals the average power "
           "absorbed, and the reactive power likewise."),

dict(num="10.12", title="Finding Maximum Power Transfer in a Circuit with an Ideal Transformer",
     ask="The variable resistor in the circuit in the figure is adjusted until maximum "
         "average power is delivered to $R_L$. a) What is the value of $R_L$ in ohms? "
         "b) What is the maximum average power delivered to $R_L$?",
     page=423, fig=(423, "10.25"), kind="th", n1="a", n2="0", domain="ac", omega=W, rms=True,
     desc="e,1,0,840:r60,1,p,60:t,[p,x],[a,x],[-4,1]:r20,x,0,20",
     expect={"z": 35, "pmax": 315},
     letters={"z": "a", "pmax": "b"},
     booknames={"z": "R_L", "pmax": "p_{max}"},
     shows="The circuit consists of a source feeding a load through an ideal "
           "transformer whose windings share a node. The question wants the load that "
           "draws the most average power and how much that is. An ideal transformer is "
           "the element `t`. Because its primary and secondary here share a node, we "
           "write each winding as a bracketed pair of terminals, top node then bottom, "
           "`[p,x]` for the primary and `[a,x]` for the secondary, followed by the "
           "turns. The dots sit at opposite ends of the two windings, the primary's at "
           "the top and the secondary's at the bottom, and that polarity is a minus "
           "sign on one of the turn counts, so we write the ratio as `[-4,1]`. We name "
           "the two resistors after their values, `r60` and `r20`. The same "
           "transformer can also be written with the secondary's pair the other way "
           "round and the sign dropped, `t,[p,x],[x,a],[4,1]`, since reversing a pair "
           "reverses its polarity too, and the answers are the same. We leave the load "
           "$R_L$ out of the description and name its terminals, node **a** and "
           "ground, to the {{card:Find equivalent}} card with *Thévenin / Norton* "
           "chosen, which reports the load that would draw the most average power from "
           "those terminals and how much: by the maximum power theorem that load is "
           "the Thévenin impedance, reported as `zeq`, and the power is `pmax`."),

dict(num="11.1", digits=5, title="Analyzing a Wye-Wye Circuit",
     ask="A balanced, positive-sequence Y-connected generator with an internal impedance of "
         "$0.2 + j0.5$ Ω per phase and an internal voltage of 120 V per phase feeds a "
         "balanced Y-connected load of $39 + j28$ Ω per phase over a line of $0.8 + j1.5$ Ω "
         "per phase; the a-phase internal voltage is the reference. b) Calculate the three "
         "line currents. c) Calculate the phase voltages at the load. d) Calculate the line "
         "voltages at the load. e) Calculate the phase voltages at the generator terminals. "
         "f) Calculate the line voltages at the generator terminals. g) Repeat for a "
         "negative phase sequence.",
     page=446, fig=(446, "11.10"), domain="ac", omega=W,
     desc="ea,ga,0,(120∠0°):eb,gb,0,(120∠-120°):ec,gc,0,(120∠120°):"
          "rga,ga,a,0.2+0.5j:rgb,gb,b,0.2+0.5j:rgc,gc,c,0.2+0.5j:"
          "rla,a,pa,0.8+1.5j:rlb,b,pb,0.8+1.5j:rlc,c,pc,0.8+1.5j:"
          "rfa,pa,nn,39+28j:rfb,pb,nn,39+28j:rfc,pc,nn,39+28j",
     # Roberto, 14 Sep 2026: each part answered separately, under its
     # letter, showing what is evaluated and what Symbulator returns. The
     # nine differences are verified by the runner (hidden here) and shown
     # as the Evaluate steps below; the six read-off answers are placed
     # among them by the `keys` steps so the parts keep the book's order.
     expect={"i_rla": 1.92 - 1.44j,
             "i_rlb": -2.2071 - 0.94276j,
             "i_rlc": 0.28708 + 2.3828j,
             "v_a": 118.9 - 0.66406j,
             "v_b": -60.024 - 102.64j,
             "v_c": -58.874 + 103.3j,
             "@v_pa-v_nn": 115.2 - 2.3929j,
             "@v_pb-v_nn": -59.67 - 98.565j,
             "@v_pc-v_nn": -55.525 + 100.96j,
             "@v_pa-v_pb": 174.88 + 96.179j,
             "@v_pb-v_pc": -4.1449 - 199.54j,
             "@v_pc-v_pa": -170.73 + 103.36j,
             "@v_a-v_b": 178.92 + 101.97j,
             "@v_b-v_c": -1.1502 - 205.94j,
             "@v_c-v_a": -177.77 + 103.96j},
     hide=["@v_pa-v_nn", "@v_pb-v_nn", "@v_pc-v_nn", "@v_pa-v_pb", "@v_pb-v_pc", "@v_pc-v_pa", "@v_a-v_b", "@v_b-v_c", "@v_c-v_a"],
     booknames={"i_rla": "I_{aA}",
                "i_rlb": "I_{bB}",
                "i_rlc": "I_{cC}",
                "v_a": "V_{an}",
                "v_b": "V_{bn}",
                "v_c": "V_{cn}"},
     evals=[dict(text="**b)** The three line currents are the currents through the line "
                      "impedances `rla`, `rlb` and `rlc`, read off their cards:",
                 keys=["i_rla", "i_rlb", "i_rlc"]),
            dict(text="**c)** The phase voltages at the load are the voltages of its three nodes above its neutral **nn**. We type `v_pa-v_nn` into {{card:Evaluate}}:",
                 expr="v_pa-v_nn", expect=115.2 - 2.3929j, unit="V", book="V_{AN}"),
            dict(text="Likewise `v_pb-v_nn`:",
                 expr="v_pb-v_nn", expect=-59.67 - 98.565j, unit="V", book="V_{BN}"),
            dict(text="And `v_pc-v_nn`:",
                 expr="v_pc-v_nn", expect=-55.525 + 100.96j, unit="V", book="V_{CN}"),
            dict(text="**d)** The line voltages at the load are the differences between pairs of its nodes. We type `v_pa-v_pb`:",
                 expr="v_pa-v_pb", expect=174.88 + 96.179j, unit="V", book="V_{AB}"),
            dict(text="Likewise `v_pb-v_pc`:",
                 expr="v_pb-v_pc", expect=-4.1449 - 199.54j, unit="V", book="V_{BC}"),
            dict(text="And `v_pc-v_pa`:",
                 expr="v_pc-v_pa", expect=-170.73 + 103.36j, unit="V", book="V_{CA}"),
            dict(text="**e)** The phase voltages at the generator's terminals are the voltages "
                      "at nodes **a**, **b** and **c**, read off the run:",
                 keys=["v_a", "v_b", "v_c"]),
            dict(text="**f)** The line voltages at the generator's terminals are the differences between those three. We type `v_a-v_b`:",
                 expr="v_a-v_b", expect=178.92 + 101.97j, unit="V", book="V_{ab}"),
            dict(text="Likewise `v_b-v_c`:",
                 expr="v_b-v_c", expect=-1.1502 - 205.94j, unit="V", book="V_{bc}"),
            dict(text="And `v_c-v_a`:",
                 expr="v_c-v_a", expect=-177.77 + 103.96j, unit="V", book="V_{ca}")],
     shows="The circuit consists of a three-phase generator, a three-phase line and a "
           "three-phase load, all Y-connected and all balanced. The question wants the "
           "three line currents and the phase and line voltages at the load and at the "
           "generator, first for a positive phase sequence and then for a negative one. "
           "We describe the whole circuit, one phase at a time. There are three sources "
           "at the generator's internal nodes, which we call **ga**, **gb** and **gc**, "
           "each written as a phasor, its magnitude and its angle in degrees: "
           "`(120∠0°)`, `(120∠-120°)` and `(120∠120°)`. Then come the generator's, the "
           "line's and the load's impedance in each phase, all in ohms, which we name "
           "`rga`, `rla` and `rfa` for the a phase and likewise for b and c. We take the "
           "generator's neutral as ground and call the load's neutral **nn**. The "
           "generator's terminals we call **a**, **b** and **c** and the load's **pa**, "
           "**pb** and **pc**.",
     interpret="Every quantity the question asks for is the current through one element, "
               "the voltage at one node or the difference between two node voltages, so "
               "each part is read off the run or typed into the {{card:Evaluate}} card. "
               "The book prints each answer as a phasor, and the same value in that form "
               "follows each answer in parentheses.",
     after="**g)** A negative phase sequence is the same description with the angles of "
           "`eb` and `ec` exchanged, `(120∠120°)` and `(120∠-120°)`. Running it "
           "returns the same fifteen answers with every b-phase value and c-phase value "
           "exchanged, and the line voltages now lag the phase voltages by 30° instead "
           "of leading them."),
]

SPECS += [
dict(num="13.2", title="The Natural Response of an RC Circuit",
     ask="The circuit in the figure is the circuit of Example 7.3. Find $v_o(t)$ for "
         "$t$ ≥ 0+.",
     page=515, fig=(515, "13.11"), domain="fd",
     pre=[dict(
        text="This is the circuit of Example 7.3, a capacitor charged from one source "
             "and switched over to a set of resistors, asked again with the answer "
             "wanted as a Laplace transform. Its first interval is the same: before "
             "the switch moves the capacitor has sat across the 100 V source through "
             "the 10 kΩ for a long time, so the circuit is steady. We describe that "
             "circuit as before and run it in DC for the capacitor's voltage:",
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
     evals=[dict(text="The question asks for $v_o(t)$, and the run has given its "
                      "transform. Inverting it is the third step, and ours to take: "
                      "`s2t` turns a function of $s$ back into a function of $t$, "
                      "and we give it the answer just read.",
                 expr="s2t(v_2)", expect="60*exp(-25*t)", unit="V",
                 label="the voltage at node 2, back in the time domain",
                 texname="v_{o}(t)")],
     after="That is what Example 7.3 reached in a single TR run, which transforms, "
           "solves and inverts out of sight. Here the halves are separate and "
           "visible. FD does what the book does down to its $V_o(s)$, and `s2t` does "
           "the inversion the book performs with a table of transforms.",
     shows="The second interval is the same description as Example 7.3's second run, "
           "with the 100 V in the capacitor's fifth field. The analysis is the one "
           "difference. This chapter of the book works every problem by the Laplace "
           "method, which transforms the circuit into the $s$ domain, solves it "
           "there and inverts the result, so we set the analysis to FD. FD does the "
           "first two of those, returning each answer as a function of $s$ with the "
           "initial condition already inside it. $V_o(s)$ is the voltage at node 2."),

dict(num="13.3", title="The Step Response of an RLC Circuit",
     ask="Consider the circuit in the figure, where the initial current in the inductor is "
         "29 mA and the initial voltage across the capacitor is 50 V. Find $v(t)$ for "
         "$t$ ≥ 0.",
     page=515, fig=(515, "13.13"), domain="fd",
     desc="j,0,1,{24'm*u(t)}:c,1,0,25'n,50:l,1,0,25'm,0.029:r,1,0,500",
     expect={"v_1": "(50*s - 200000)/(s**2 + 80000*s + 1600000000)"},
     booknames={"v_1": "V(s)"},
     evals=[dict(text="The question asks for $v(t)$. `s2t` inverts a function of $s$ "
                      "back into a function of $t$, so we give it the answer just "
                      "read.",
                 expr="s2t(v_1)", expect="(50 - 2200000*t)*exp(-40000*t)", unit="V",
                 label="the voltage at node 1, back in the time domain",
                 texname="v(t)")],
     after="The book arrives at the same expression by a partial fraction expansion "
           "and a table of transforms, its last two steps. The same description run "
           "in TR returns it in one go, the solver transforming and inverting out of "
           "sight.",
     shows="The circuit is a parallel RLC circuit holding an initial current and an "
           "initial voltage, with a constant current source switched on at $t$ = 0. "
           "The question wants the voltage across it, and the book works it by the "
           "Laplace method. A constant source switched on at $t$ = 0 is a step, "
           "$24u(t)$ mA, so we type it as a function of time inside curly brackets, "
           "`{24'm*u(t)}`, and FD converts it to the $s$ domain. We put the two initial conditions the question gives in the "
           "fifth fields of the capacitor and the inductor, 50 V and 29 mA written "
           "0.029, and name the four elements `j`, `c`, `l` and `r`. We set the "
           "analysis to FD, which returns the transform $V(s)$ of the voltage asked "
           "for, the voltage at node 1."),

dict(num="13.5", title="Analyzing a Circuit with Multiple Meshes",
     ask="The circuit in the figure has no initial stored energy. At $t$ = 0 the switch "
         "closes. Find $i_1(t)$ and $i_2(t)$ for $t$ ≥ 0.",
     page=519, fig=(519, "13.17"), domain="tr",
     desc="e,1,0,336:l1,1,2,8.4:r1,2,0,42:l2,2,3,10:r2,3,0,48",
     expect={"i_l1": "15 - 14*exp(-2*t) - exp(-12*t)",
             "i_l2": "7 - 8.4*exp(-2*t) + 1.4*exp(-12*t)"},
     booknames={"i_l1": "i_1", "i_l2": "i_2"},
     shows="The circuit consists of two loops sharing a resistor, each with an "
           "inductor, switched onto a source at $t$ = 0 with no energy stored. The "
           "question wants the two loop currents as functions of time. No energy is "
           "stored, so we write the two inductors without fifth fields, and the switch "
           "closing at $t$ = 0 onto the 336 V source needs no element of its own: in "
           "TR a numerical source value is a step that begins at $t$ = 0. We name the "
           "inductors `l1` and `l2` after the book's $i_1$ and $i_2$, which are the "
           "currents through them, and the resistors `r1` and `r2`. TR returns the two "
           "currents as functions of $t$. The Laplace transform and its inversion "
           "happen inside the solver."),

dict(num="13.6", title="Creating a Thevenin Equivalent in the s Domain",
     ask="The circuit in the figure has no initial stored energy, and at $t$ = 0 the switch "
         "closes. Find the Thevenin equivalent for the circuit to the left of the terminals "
         "a and b in the s domain.",
     page=521, fig=(521, "13.20"), kind="th", n1="a", n2="0", domain="fd",
     desc="e,1,0,480/s:r1,1,2,20:l,2,0,0.002:r2,2,a,60",
     expect={"vth": "480/(s + 10000)", "z": "80*(s + 7500)/(s + 10000)"},
     booknames={"vth": "V_{Th}", "z": "Z_{Th}"},
     shows="The circuit is a source switched at $t$ = 0 onto two resistors and an "
           "inductor, and the question wants the Thévenin equivalent of that part of "
           "the circuit, seen from two terminals, as functions of $s$. The 480 V "
           "source switched on at $t$ = 0 is a step, whose transform is $480/s$, so we "
           "write its value as `480/s`. We call the terminals a and b node **a** and "
           "ground, and name them to the {{card:Find equivalent}} card with *Thévenin "
           "/ Norton* chosen. The card works in FD as it does in DC and AC, and "
           "returns the equivalent's voltage and impedance as functions of $s$. We "
           "leave out the capacitor to the right of the terminals, since the question "
           "asks for the equivalent seen from them."),

dict(num="13.7", title="Analyzing a Circuit with Mutual Inductance",
     ask="The make-before-break switch in the circuit in the figure has been in position a "
         "for a long time. At $t$ = 0 it moves instantaneously to position b. Find $i_2(t)$ "
         "for $t$ ≥ 0.",
     page=523, fig=(523, "13.23"), domain="tr",
     pre=[dict(
        text="The circuit consists of two coupled coils, the primary fed from a source "
             "through a switch and the secondary closed on two resistors. The switch "
             "takes the source out at $t$ = 0, and the question wants the secondary's "
             "current afterwards. There are two intervals, and two runs. With the "
             "switch at position a the primary side has been steady for a long time. "
             "We describe the whole circuit, naming the resistors after their values, "
             "`r9`, `r3`, `r2b` and `r10`, the coils `l1` and `l2`, and the coupling "
             "as the `m` line with their mutual inductance, 2 H. We call the "
             "secondary's top **q** and the node between its two resistors **c**, and "
             "take its bottom as ground -- nothing conducts between the two windings, "
             "so joining their bottoms changes no current. A DC run gives both "
             "currents:",
        desc="e,1,0,60:r9,1,a,9:r3,a,p,3:l1,p,0,2:m,l1,l2,2:l2,q,0,8:r2b,q,c,2:r10,c,0,10",
        tag="DC, at position a",
        expect={"i_l1": 5, "i_l2": 0}, booknames={"i_l1": "i_1(0)", "i_l2": "i_2(0)"},
        note="This is the circuit at position a, before the switch moves, run in DC to "
             "find the two coil currents, which the next entry takes as its initial "
             "conditions.")],
     desc="r3,0,p,3:l1,p,0,2,5:m,l1,l2,2:l2,q,0,8,0:r2b,q,c,2:r10,c,0,10",
     expect={"i_l2": "1.25*exp(-t) - 1.25*exp(-3*t)"},
     booknames={"i_l2": "i_2"},
     shows="At $t$ = 0 the switch moves to b, which takes the source and the 9 Ω out and "
           "closes the primary on the 3 Ω alone. We describe that circuit with the same "
           "names and the two currents just found as the coils' fifth fields, 5 and 0. "
           "$i_2$ is the current through `l2`."),

dict(num="13.9", title="Deriving the Transfer Function of a Circuit",
     ask="The voltage source $v_g$ drives the circuit shown in the figure. The output signal "
         "is the voltage across the capacitor, $v_o$. a) Find the transfer function for this "
         "circuit. b) Calculate the numerical values for the poles and zeros of the transfer "
         "function.",
     page=527, fig=(527, "13.31"), domain="fd",
     desc="e,1,0,vg:r1,1,2,1000:r2,2,3,250:l,3,0,50'm:c,2,0,1'u",
     expect={"@v_2/vg": "1000*(s + 5000)/(s**2 + 6000*s + 25000000)"},
     letters={"@v_2/vg": "a"},
     labels={"@v_2/vg": "transfer function"},
     texnames={"@v_2/vg": "H(s) = \\dfrac{v_{2}}{v_{g}}"},
     units={"@v_2/vg": ""},
     minitool=[
      dict(tool="pz", args=["v2/vg"],
           text="**b)** The poles of a transfer "
                "function are the values of $s$ that make its denominator zero, and "
                "the zeros are the values that make its numerator zero. The "
                "{{card:Mini-Tools}} card finds both at once: we choose *pz \u2014 "
                "poles and zeros* in its {{ui:Tool}} menu and give it the transfer "
                "function.",
           expect={"poles": "-3000 - 4000j, -3000 + 4000j", "zeros": "-5000"},
           say=[("poles", "the poles"), ("zeros", "the zero")]),
     ],
     after="So the transfer function has poles at $s = -3000 \\pm j4000$ and a zero at "
           "$s = -5000$. The card cancels any factor the numerator and the denominator "
           "share before it reads the roots, so a pole and a zero at the same place "
           "are not reported.",
     shows="The circuit consists of a source driving a resistor, a capacitor and an "
           "inductive branch, with the capacitor's voltage as the output. The question "
           "wants the transfer function from source to output, and its poles and "
           "zeros. A transfer function is the ratio of an output to the input that "
           "produced it, as functions of $s$, so we leave the source as the symbol "
           "`vg`, so that the output comes back as a multiple of it. We number the "
           "nodes from the source, so the output, the capacitor's voltage, is the "
           "voltage at node 2, and the transfer function is that voltage divided by "
           "`vg`, which we will read in the {{card:Evaluate}} card."),

dict(num="13.13", title="A Series Inductor Circuit with an Impulsive Response",
     ask="The switch in the circuit shown in the figure has been closed for a long time. At "
         "$t$ = 0 it opens. Find the output voltage $v_o$ and the current in the 3 H "
         "inductor, $i_1$.",
     page=541, fig=(541, "13.50"), domain="tr",
     pre=[dict(
        text="The circuit consists of two inductors, one carrying a current from a "
             "source and the other idle behind a closed switch that shorts it out. "
             "Opening the switch at $t$ = 0 forces the two into series, and the "
             "question wants the voltage across the second and the current in the "
             "first afterwards. There are two intervals, and two runs. While the "
             "switch is closed it joins the junction after $L_1$ to the bottom rail, "
             "and the circuit has been steady for a long time. We describe that "
             "circuit and run it in DC for the two inductor currents. We write the "
             "closed switch by giving both its ends the same node, ground, and name "
             "the inductors `l1` and `l2` after the book's $L_1$ and $L_2$:",
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
           "carry the same current from then on. An inductor's current cannot jump "
           "without an impulse of voltage across it, and the weight of this one, 12, "
           "is what it takes to bring $L_2$'s current from 0 to the 6 A the pair "
           "settle on.",
     shows="Opening the switch removes that wire, so the two inductors are now in series "
           "with the 15 Ω between them. We describe that circuit with the 10 A and 0 just "
           "found as their fifth fields, numbering the nodes 1 to 4 from the source. "
           "$v_o$ is the voltage at node 3, the top of the 15 Ω "
           "and $L_2$, and $i_1$ the current through `l1`."),
]

SPECS += [
dict(num="3.10", title="Using a Wheatstone Bridge to Measure Resistance",
     ask="For the Wheatstone bridge in the figure, $R_3$ can be varied from 10 Ω to 2 kΩ. "
         "What range of resistor values can this bridge measure?",
     page=101, fig=(101, "3.30"), domain="dc",
     desc="e,1,0,V_s:r1,1,a,1'k:r2,1,b,4'k:sg,a,b:r3,a,0,R_3:rx,b,0,R_x",
     expect={},
     solveq=[
      dict(tag="DC, Solve at R_3 = 10",
           text="With the results on screen, we open the {{card:Solve}} card under "
                "them and ask the question the way the bridge is used. The balance "
                "condition, no current through the galvanometer, is the equation "
                "`isg=0`. The resistance we want is the unknown, `R_x`. The setting of "
                "the dial is a condition, first at its lowest, 10 Ω:",
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
     shows="A Wheatstone bridge measures a resistance nobody knows, $R_x$, by "
           "comparing it with resistances that are known. The adjustable resistor "
           "$R_3$ is turned until the galvanometer between the two arms of the bridge "
           "carries no current, and at that setting the unknown can be read off the "
           "others. So we describe the circuit with the two resistances the question "
           "leaves open as symbols rather than numbers, which we name `R_3` for the "
           "adjustable one and `R_x` for the unknown, after the book's. We name the "
           "two known resistors `r1` and `r2`, and call the two arms' midpoints **a** "
           "and **b**. We describe the galvanometer as a short circuit, the element "
           "`s`, which we name `sg`: the figure gives it no resistance, and what we "
           "will need from it is its current, which a short reports as `isg`. We leave "
           "the source as a symbol too, `V_s`, since its value plays no part at "
           "balance. We run this as it stands, in DC, and every answer comes back as a "
           "formula in the three symbols."),

dict(num="14.6", title="Designing a Parallel RLC Bandpass Filter",
     ask="a) Show that the RLC circuit in the figure is a bandpass filter by deriving an "
         "expression for the transfer function $H(s)$. b) Compute the centre frequency. "
         "c) Calculate the cutoff frequencies, the bandwidth and $Q$. d) Compute $R$ and $L$ "
         "for a centre frequency of 5 kHz and a bandwidth of 200 Hz, using a 5 µF capacitor.",
     page=581, fig=(581, "14.22"), domain="fd",
     desc="e,1,0,vi:rr,1,2,R:c,2,0,C:l,2,0,L",
     expect={"@v_2/vi": "(s/(C*R))/(s**2 + s/(C*R) + 1/(L*C))"},
     labels={"@v_2/vi": "transfer function"},
     texnames={"@v_2/vi": "H(s) = \\dfrac{v_{2}}{v_{i}}"},
     units={"@v_2/vi": ""},
     solveq=[dict(
        tag="FD, Solve for R and L",
        text="**d)** The question gives the centre frequency, the bandwidth and the "
             "capacitor and asks for $R$ and $L$. Those are two equations in two unknowns, which the "
             "{{card:Solve}} card takes as they stand: $\\omega_0 = 1/\\sqrt{LC}$ at "
             "2π × 5000 rad/s and $\\beta = 1/RC$ at 2π × 200 rad/s, with the capacitor as "
             "a condition:",
        equations=["1/sqrt(L*C)=2*pi*5000", "1/(R*C)=2*pi*200"], unknowns=["L", "R"],
        conditions=["C=5'u"], real_only=True,
        expect={"L": 0.0002026, "R": 159.2}, unit={"L": "H", "R": "\\Omega"},
        book={"L": "L", "R": "R"})],
     after="That is $L$ = 202.6 µH and $R$ = 159.2 Ω.",
     parts_first=True,
     parts=[
      ("a", "Dividing numerator and denominator by $RLC$ puts the transfer function in "
            "the standard form $H(s) = \\dfrac{s/RC}{s^2 + s/RC + 1/LC}$: a first-order "
            "numerator in $s$ over a second-order denominator, which is the shape of a "
            "bandpass filter."),
      ("b", "The centre frequency is the $\\omega_0$ of that denominator, "
            "$\\omega_0 = 1/\\sqrt{LC}$."),
      ("c", "The bandwidth is the coefficient of $s$ in the denominator, $\\beta = "
            "1/RC$. The cutoff frequencies are $\\omega_{c} = \\mp\\beta/2 + "
            "\\sqrt{(\\beta/2)^2 + \\omega_0^2}$, and $Q = \\omega_0/\\beta$."),
     ],
     shows="The circuit consists of a series resistor feeding a parallel inductor and "
           "capacitor, with the voltage across the pair as the output. The question "
           "wants its transfer function shown to be a bandpass, its centre frequency, "
           "bandwidth and $Q$ in general, and then the resistor and inductor for a "
           "given centre frequency and bandwidth. Nothing in the question is a number "
           "until part (d), so we leave the three elements as the symbols `R`, `L` and "
           "`C` and the source as `vi`, naming the resistor `rr` to keep its name "
           "apart from its value. We set the analysis to FD. The transfer function is "
           "the output voltage, at node 2, divided by the input, which we will read in "
           "the {{card:Evaluate}} card, and it comes back in terms of the three "
           "symbols."),

dict(num="18.1", title="Finding the z Parameters of a Two-Port Circuit",
     ask="Find the z parameters for the circuit shown in the figure.",
     page=724, fig=(724, "18.3"), kind="port", n1="1", n2="2", ptype="z", domain="dc",
     desc="r5,1,2,5:r20,1,0,20:r15,2,0,15",
     expect={"11": 10, "12": 7.5, "21": 7.5, "22": 9.375},
     shownames={"11": "z11", "12": "z12", "21": "z21", "22": "z22"},
     booknames={"11": "z_{11}", "12": "z_{12}", "21": "z_{21}", "22": "z_{22}"},
     shows="The circuit is a T of three resistors seen as a two-port, and the question "
           "wants its z parameters: the four numbers that relate the two port "
           "voltages to the two port currents. We take port 1 as node **1** with "
           "ground and port 2 as node **2** with ground, write the three resistors "
           "between those nodes, naming each after its value, and name the two ports "
           "to the {{card:Find equivalent}} card with *Two-port parameters* chosen and "
           "the kind set to **z**. It returns the four parameters, named `z11` to "
           "`z22`."),

dict(num="18.6", digits=7, title="Analyzing Cascaded Two-Port Circuits",
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
     shows="The circuit consists of two identical amplifiers, each known only by its "
           "four h parameters, one feeding the other between a source with an internal "
           "resistance and a load. The question wants the voltage gain of the pair. A "
           "two-port known only by its parameters is an element of its own. Since "
           "these are h parameters we use the element `h`, and write the four values "
           "after the two nodes as a bracketed term, `[1000,0.0015,100,0.0001]`, the "
           "100 µS written as 0.0001. We write the two amplifiers as two such lines, "
           "`h1` and `h2`, sharing a node we call **b**, between the source's 500 Ω "
           "and the 10 kΩ load. We leave the source as the symbol `vg`, so that the "
           "output comes back as a multiple of it, and the gain is that multiple, "
           "which we will read in the {{card:Evaluate}} card."),
]
