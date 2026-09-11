---
id: nr12-sampler
kind: back
title: Select problems from Nilsson & Riedel 12ed
versions: [9]
updated: 2026-09-12
summary: >
  Forty-three worked examples from *Electric Circuits*, each described in
  Symbulator and checked against the answer the book prints. DC, AC, TR and FD,
  with Expert Mode and symbolic answers where they earn their place.
---

Nilsson and Riedel's *Electric Circuits* is the book a great many
engineers learned this material from, and its worked examples are unusually
well suited to showing what Symbulator is for: each one states a circuit,
states a question, and then prints the answer. That last part is what makes
this chapter checkable rather than merely illustrative — **every answer below
was compared against the number the book prints**, and the page says so
example by example.

The selection is deliberate. These are not the easiest problems in the book;
they are the ones where the distance between *describing a circuit* and
*solving it by hand* is widest — a delta that has to be transformed, a
supermesh, a dependent source whose controlling current is three steps away, a
transformer whose secondary floats, a switch that opens twice. The book meets
each with a method. Symbulator meets all of them with the same six words:
describe the circuit, choose an analysis.

::: note What this chapter is not
It is not a solutions manual, and it will not teach you circuit analysis.
Every example here is worked in full in the book itself, and the book's
derivation is the part worth reading — {{ref:lesson-dc}} onward is where
Symbulator is taught. This is a demonstration, aimed at someone who already
knows the material and wants to see what the software does with it.

The circuits are reproduced from *Electric Circuits*, 12th edition, by
James W. Nilsson and Susan A. Riedel (Pearson), and are the authors' and
publisher's property. For the purpose of teaching students how to use
Symbulator, these diagrams are reproduced under the principle of fair use. No
copyright infringement is intended.
:::

## How to read an entry {#nr12-how}

Each entry gives the book's question, the book's own figure, the Symbulator
description, the analysis to choose, and the answers. Where an answer is a
number it is quoted in prose, and the sentence says that it is the book's
number too. Where an answer is an *expression* — a function of *t*, a
transfer function in *s*, a formula in the circuit's own symbols — it is shown
in a results panel exactly as the app prints it.

Four things recur, and they are the reason these particular examples were
chosen:

- **A dependent source is a value, not a device.** Write `8*ir3` in a source's
  value field and the controlling current is named; there is no constraint
  equation to write and none to get wrong.
- **The case is never chosen by anyone.** Overdamped, critically damped and
  underdamped are the same three lines with different numbers, and the algebra
  decides which one comes out.
- **A symbol left in the circuit stays in the answer.** That is how a design
  problem gets checked, how a transfer function appears without being asked
  for, and how one run answers all three parts of a question.
- **{{card:Expert Mode}} turns a question inside out.** When the thing you know
  is an answer and the thing you want is a component value, state the answer as
  an equation and name the component as the unknown.

### Every circuit is in the app already {#nr12-entries}

Nothing here has to be typed. All forty-three circuits ship with Symbulator as
a built-in example book — open {{card:Built-in Examples}} and pick
*Nilsson & Riedel 12ed* from the list of books; the entries are named for the
example each one comes from, and each arrives with its note, its picture, its
settings, its Expert Mode fields and the analysis it wants already set.

Pick one, press {{btn:Run Symbulator}}, and the answers below are what you get.
{{ref:input-files}} explains what an entry remembers and how to save your own.

## Direct current — DC {#nr12-dc}

Sixteen resistive problems, and the running theme is that the book's
*method* — node voltages, mesh currents, source transformations, superposition,
a delta-to-wye — is a way of getting an answer by hand, not a property of the
answer. Symbulator is told the circuit and never told the method. Two of these
run in {{card:Expert Mode}}, and two are two-port problems.

::: problem NR12's Example 3.7

**Using Voltage Division and Current Division to Solve a Circuit.**

Use current division to find the current $i_o$ and use voltage division to find the voltage $v_o$ for the circuit in Fig. 3.22.

::: figure assets/circuit/nr12-ex3-7.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 3.7
:::

::: answer
A one-line answer to a problem the book solves with two division formulas: the whole circuit is solved at once, and the source's own `r_j` is the 6 Ω equivalent resistance the book works out by hand.

```field 9 Circuit Description
j,0,1,8
r1,1,2,36
r2,2,0,44
r3,1,0,10
r4,1,3,40
r5,3,4,10
r6,4,0,30
r7,1,0,24
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_r7` = {{o:2}} A, `v_r6` = {{o:18}} V, `v_r7` = {{o:48}} V and `r_j` = {{o:6}} Ω — the same answers the book prints.

:::
:::

::: problem NR12's Example 3.10

**Using a Wheatstone Bridge to Measure Resistance.**

For the Wheatstone bridge in Fig. 3.30, {{var:R_3}} can be varied from 10 Ω to 2 kΩ. What range of resistor values can this bridge measure?

::: figure assets/circuit/nr12-ex3-10.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 3.10
:::

::: answer
Balance is a statement about an answer — no current in the detector — so it is written as an equation and the unknown is a resistor. The answer comes back as the symbolic `4*r3`, and the range 40 Ω to 8 kΩ is that one line read twice.

```field 9 Circuit Description
e,1,0,vs
r1,1,a,1'k
r2,1,b,4'k
rg,a,b,500
r3,a,0,r3
rx,b,0,rx
```

```field 9 Add equation(s)
i_rg = 0
```

```field 9 Add unknown(s)
rx
```

Set {{ui:Analysis}} to *DC — direct current*. This one needs {{ui:Enable Expert Mode}} ticked in the {{card:Expert Mode}} box; the equations and unknowns go in the fields it reveals.

::: result rx
rx = 4 r_{3}
:::

:::
:::

::: problem NR12's Example 3.11

**Applying a Delta-to-Wye Transform.**

Find the current and power supplied by the 40 V source in the circuit shown in Fig. 3.35.

::: figure assets/circuit/nr12-ex3-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 3.11
:::

::: answer
The book needs a delta-to-wye transform to reduce this bridge. Symbulator needs nothing: the bridge is six lines, and `r_e` reports the 80 Ω the transform was for.

```field 9 Circuit Description
e,1,0,40
r1,1,2,5
r2,2,3,100
r3,2,4,125
r4,3,4,25
r5,3,0,40
r6,4,0,37.5
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `-i_e` = {{o:0.5}} A, `-p_e` = {{o:20}} W and `r_e` = {{o:80}} Ω — the same answers the book prints.

:::
:::

::: problem NR12's Example 4.4

**Using the Node-Voltage Method with Dependent Sources.**

Use the node-voltage method to find the power dissipated in the 5 Ω resistor in the circuit shown in Fig. 4.10.

::: figure assets/circuit/nr12-ex4-4.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.4
:::

::: answer
A dependent source is written by naming another answer in its value — `8*ir3` — so no constraint equation has to be written by hand.

```field 9 Circuit Description
e,1,0,20
r1,1,2,2
r2,2,0,20
r3,2,3,5
r4,3,0,10
r5,3,4,2
e2,4,0,8*ir3
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `v_2` = {{o:16}} V, `v_3` = {{o:10}} V, `i_r3` = {{o:1.2}} A and `p_r3` = {{o:7.2}} W — the same answers the book prints.

:::
:::

::: problem NR12's Example 4.7

**Using the Mesh-Current Method with Dependent Sources.**

Use the mesh-current method to find the power dissipated in the 4 Ω resistor in the circuit shown in Fig. 4.23.

::: figure assets/circuit/nr12-ex4-7.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.7
:::

::: answer
The same circuit the book solves with three mesh equations and a constraint. Symbulator is told the circuit, not the method.

```field 9 Circuit Description
e,1,0,50
r1,1,3,1
r2,1,2,5
r3,2,3,4
r4,2,0,20
e2,3,0,15*ir4
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_r4` = {{o:1.6}} A, `i_r3` = {{o:2}} A and `p_r3` = {{o:16}} W — the same answers the book prints.

:::
:::

::: problem NR12's Example 4.8

**A Special Case in the Mesh-Current Method.**

Use the mesh-current method to find branch currents $i_a$, $i_b$ and $i_c$ in the circuit for Example 4.3, repeated here as Fig. 4.25.

::: figure assets/circuit/nr12-ex4-8.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.8
:::

::: answer
The book's 'special case' is a current source shared by no other mesh, which needs a rule of its own. Symbulator has no meshes, so there is no special case.

```field 9 Circuit Description
e,1,0,50
r1,1,2,5
r2,2,0,10
r3,2,0,40
j,0,2,3
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_r1` = {{o:2}} A, `i_r2` = {{o:4}} A, `i_r3` = {{o:1}} A and `v_2` = {{o:40}} V — the same answers the book prints.

:::
:::

::: problem NR12's Example 4.13

**Using Special Source Transformation Techniques.**

a) Use source transformations to find the voltage $v_o$ in the circuit shown in Fig. 4.42. b) Find the power developed by the 250 V voltage source. c) Find the power developed by the 8 A current source.

::: figure assets/circuit/nr12-ex4-13.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.13
:::

::: answer
Four source transformations in the book; one description here. The resistors the book has to put back before it can find the powers were never taken out.

```field 9 Circuit Description
e,1,0,250
r1,1,0,125
r2,1,2,25
j,2,9,8
r3,9,0,10
r4,2,0,100
r5,2,3,5
r6,3,0,15
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `v_r4` = {{o:20}} V, `-i_e` = {{o:11.2}} A, `-p_e` = {{o:2800}} W and `-p_j` = {{o:480}} W — the same answers the book prints.

:::
:::

::: problem NR12's Example 4.21

**Calculating the Condition for Maximum Power Transfer.**

a) For the circuit shown in Fig. 4.65, find the value of $R_L$ that results in maximum power being transferred to $R_L$. b) Calculate the maximum power that can be delivered to $R_L$.

::: figure assets/circuit/nr12-ex4-21.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.21
:::

::: answer
The Thévenin tool answers all three parts at once: `z` is the load for maximum transfer and `pmax` is the power it takes.

```field 9 Circuit Description
e,1,0,360
r1,1,2,30
r2,2,0,150
```

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **2** and **0**.

Symbulator returns `vth` = {{o:300}} V, `z` = {{o:25}} Ω and `pmax` = {{o:900}} W — the same answers the book prints.

:::
:::

::: problem NR12's Example 4.23

**Using Superposition to Solve a Circuit with Dependent Sources.**

Use the principle of superposition to find $v_o$ in the circuit shown in Fig. 4.71.

::: figure assets/circuit/nr12-ex4-23.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.23
:::

::: answer
Superposition is a method for getting an answer by hand, not a property of the answer. Two dependent sources and two independent ones, solved once.

```field 9 Circuit Description
e,1,c,10
r1,1,a,5
r2,a,c,20
r3,b,0,10
j1,0,b,5
j2,b,a,0.4*vr3
e2,0,c,2*ir1
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `v_r2` = {{o:24}} V, `v_r3` = {{o:10}} V and `i_r1` = {{o:-2.8}} A — the same answers the book prints.

:::
:::

::: problem NR12's Example 5.1

**Analyzing an Op Amp Circuit.**

The op amp in the circuit shown in Fig. 5.7 is ideal. a) Calculate $v_o$ if $v_a$ = 1 V and $v_b$ = 0 V. b) Repeat for $v_a$ = 1 V and $v_b$ = 2 V. c) If $v_a$ = 1.5 V, specify the range of $v_b$ that avoids amplifier saturation.

::: figure assets/circuit/nr12-ex5-1.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.1
:::

::: answer
An ideal op amp does not know its supplies exist — it will report an output of 200 V as readily as 2 V — so saturation is a question you ask of the answer rather than something the solve enforces. Leave both inputs symbolic and one run gives the formula every part is then read off.

```field 9 Circuit Description
ea,1,0,va
r1,1,2,25'k
r2,2,3,100'k
eb,4,0,vb
o,4,2,3
```

Set {{ui:Analysis}} to *DC — direct current*.

::: result voltage at node 3
v_{3} = - 4 va + 5 vb\,\mathrm{V}
:::

**a)** With {{var:v_a}} = 1 V and {{var:v_b}} = 0 V the formula gives {{var:v_o}} = 5(0) − 4(1) = {{o:-4}} V. That is inside the supplies, so the op amp is in its linear region and -4 V is the answer.

**b)** With {{var:v_a}} = 1 V and {{var:v_b}} = 2 V, {{var:v_o}} = 5(2) − 4(1) = {{o:6}} V. Inside the supplies again, so the op amp is still linear.

**c)** With {{var:v_a}} = 1.5 V the formula becomes {{var:v_o}} = 5{{var:v_b}} − 6. The op amp stays linear while that lies between the rails, so Symbulator is asked the question directly — put `v_3 = 10` in {{card:Expert Mode}} with `vb` as the unknown, then again with `v_3 = -10`. The rails are reached at {{var:v_b}} = {{o:3.2}} V and {{var:v_b}} = {{o:-0.8}} V, so the range is {{o:-0.8}} V ≤ {{var:v_b}} ≤ {{o:3.2}} V.

:::
:::

::: problem NR12's Example 5.3

**Designing a Summing Amplifier.**

a) Design a summing amplifier whose output voltage is $v_o = -4v_a — v_b — 5v_c$, using an ideal op amp with ±12 V power supplies and a 20 kΩ feedback resistor. b) Suppose $v_a$ = 2 V and $v_c$ = $-$1 V. What range of input voltages for $v_b$ allows the op amp to remain linear?

::: figure assets/circuit/nr12-ex5-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.3
:::

::: answer
The design is checked in one run: the answer comes back as the very formula the problem asked the designer to hit.

```field 9 Circuit Description
ea,1,0,va
eb,2,0,vb
ec,3,0,vc
r1,1,n,5'k
r2,2,n,20'k
r3,3,n,4'k
rf,n,4,20'k
o,0,n,4
```

Set {{ui:Analysis}} to *DC — direct current*.

::: result voltage at node 4
v_{4} = - 4 va - vb - 5 vc\,\mathrm{V}
:::

**a)** The summing-amplifier formula is {{var:v_o}} = -({{var:R_f}}/{{var:R_a}}){{var:v_a}} — ({{var:R_f}}/{{var:R_b}}){{var:v_b}} — ({{var:R_f}}/{{var:R_c}}){{var:v_c}}, so with a 20 kΩ feedback resistor the three input resistors are {{var:R_a}} = 20k/4 = {{o:5}} kΩ, {{var:R_b}} = 20k/1 = {{o:20}} kΩ and {{var:R_c}} = 20k/5 = {{o:4}} kΩ. Running that circuit returns the very formula the design was asked to hit, which is the check.

**b)** With {{var:v_a}} = 2 V and {{var:v_c}} = -1 V the output collapses to {{var:v_o}} = -{{var:v_b}} − 3. Asking {{card:Expert Mode}} for the {{var:v_b}} that puts `v_4` on each rail gives {{o:9}} V at -12 V and {{o:-15}} V at +12 V, so the op amp stays linear for {{o:-15}} V ≤ {{var:v_b}} ≤ {{o:9}} V.

:::
:::

::: problem NR12's Example 5.3 part c

**Designing a Summing Amplifier — part (c), in Expert Mode.**

c) Suppose $v_a$ = 2 V, $v_b$ = 3 V and $v_c$ = $-$1 V. Using the input resistor values found in part (a), how large can the feedback resistor be before the op amp saturates?

::: figure assets/circuit/nr12-ex5-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.3
:::

::: answer
An unknown that is a component value, not an answer: name the saturation voltage as an equation and ask for the resistor. This is what Expert Mode is for.

```field 9 Circuit Description
ea,1,0,2
eb,2,0,3
ec,3,0,-1
r1,1,n,5'k
r2,2,n,20'k
r3,3,n,4'k
rf,n,4,rf
o,0,n,4
```

```field 9 Add equation(s)
v_4 = -12
```

```field 9 Add unknown(s)
rf
```

Set {{ui:Analysis}} to *DC — direct current*. This one needs {{ui:Enable Expert Mode}} ticked in the {{card:Expert Mode}} box; the equations and unknowns go in the fields it reveals.

Symbulator returns `rf` = {{o:40000}} — the same answers the book prints.

**c)** With {{var:v_a}} = 2 V, {{var:v_b}} = 3 V and {{var:v_c}} = -1 V the three input currents sum to a positive number, so the output swings negative and it is the -12 V rail that is reached first. Leave the feedback resistor as the symbol `rf`, put `v_4 = -12` in {{card:Expert Mode}} and name `rf` the unknown: the answer is {{o:40}} kΩ. Any larger and the op amp saturates.

:::
:::

::: problem NR12's Example 5.5

**Designing a Difference Amplifier.**

a) Design a difference amplifier that amplifies the difference between two input voltages by a gain of 8, using an ideal op amp and ±8 V power supplies. b) Suppose $v_a$ = 1 V. What range of $v_b$ keeps the op amp linear?

::: figure assets/circuit/nr12-ex5-5.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.5
:::

::: answer
The gain-of-8 design returns exactly 8(vb — va), and part (b)'s range follows from that one line.

```field 9 Circuit Description
ea,1,0,va
eb,2,0,vb
ra,1,n,1.5'k
rb,n,3,12'k
rc,2,p,1.5'k
rd,p,0,12'k
o,p,n,3
```

Set {{ui:Analysis}} to *DC — direct current*.

::: result voltage at node 3
v_{3} = - 8 va + 8 vb\,\mathrm{V}
:::

**a)** The simplified difference-amplifier formula is {{var:v_o}} = ({{var:R_b}}/{{var:R_a}})({{var:v_b}} − {{var:v_a}}), so a gain of 8 wants two resistors in the ratio 8: {{var:R_a}} = {{var:R_c}} = {{o:1.5}} kΩ and {{var:R_b}} = {{var:R_d}} = {{o:12}} kΩ. The formula also requires {{var:R_a}}/{{var:R_b}} = {{var:R_c}}/{{var:R_d}}, which those four satisfy. The run returns exactly 8({{var:v_b}} − {{var:v_a}}).

**b)** With {{var:v_a}} = 1 V the output is {{var:v_o}} = 8{{var:v_b}} − 8, which reaches +8 V at {{var:v_b}} = {{o:2}} V and -8 V at {{var:v_b}} = {{o:0}} V. So the op amp remains in its linear region for {{o:0}} V ≤ {{var:v_b}} ≤ {{o:2}} V.

:::
:::

::: problem NR12's Example 5.7

**Analyzing a Noninverting-Amplifier Circuit Using a Realistic Op Amp Model.**

Analyze the noninverting amplifier of Example 5.4 using the realistic op amp model: open-loop gain $A$ = 50,000, input resistance $R_i$ = 100 kΩ, output resistance $R_o$ = 7.5 kΩ. Find $v_o/v_g$.

::: figure assets/circuit/nr12-ex5-7.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.7
:::

::: answer
No `o` element at all: the realistic op amp is a dependent source with its own input and output resistances, and the finite-gain answer 5.9988 falls out against the ideal 6.

```field 9 Circuit Description
eg,1,0,vg
rg,1,p,1'k
ri,p,n,100'k
rs,n,0,2'k
rf,n,3,10'k
ro,4,3,7.5'k
ea,4,0,50000*(vp-vn)
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `v_3/vg` = {{o:5.9988}} — the same answers the book prints.

:::
:::

::: problem NR12's Example 18.1

**Finding the z Parameters of a Two-Port Circuit.**

Find the z parameters for the circuit shown in Fig. 18.3.

::: figure assets/circuit/nr12-ex18-1.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 18.1
:::

::: answer
Four separate open-circuit measurements in the book — two of them with a source moved to the other port. One run here, and {{var:z_12}} = {{var:z_21}} because the network is reciprocal, which is a result rather than an assumption.

```field 9 Circuit Description
r5,1,2,5
r20,1,0,20
r15,2,0,15
```

Open {{card:Find equivalent}}, choose *Two-port parameters*, kind **z**, with the ports at **1** and **2**.

Symbulator returns `11` = {{o:10}} Ω, `12` = {{o:7.5}} Ω, `21` = {{o:7.5}} Ω and `22` = {{o:9.375}} Ω — the same answers the book prints.

:::
:::

::: problem NR12's Example 18.6

**Analyzing Cascaded Two-Port Circuits.**

Two identical amplifiers are connected in cascade. Each is described by its h parameters: {{var:h_11}} = 1000 Ω, {{var:h_12}} = 0.0015, {{var:h_21}} = 100, {{var:h_22}} = 100 µS. The source has 500 Ω of internal resistance and the load is 10 kΩ. Find the voltage gain {{var:V_2}}/Vg.

::: figure assets/circuit/nr12-ex18-6.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 18.6
:::

::: answer
The book converts h to a, multiplies the two transmission matrices, then reads a gain formula out of Table 18.3. Here the two blocks are two lines of circuit wired end to end, and the gain is a division.

```field 9 Circuit Description
e,1,0,vg
rs,1,a,500
h1,a,b,[1000,0.0015,100,0.0001]
h2,b,c,[1000,0.0015,100,0.0001]
rl,c,0,10'k
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `v_c/vg` = {{o:33333.3}} — the same answers the book prints.

:::
:::

## Transients — TR {#nr12-tr}

Fourteen transient problems. The pattern is always the same and always
the one you would follow by hand: run the *t* < 0 circuit in DC to read the
capacitor voltages and inductor currents, put those numbers in the fifth field
of the `c` and `l` lines, and run the *t* ≥ 0 circuit in TR. No time constant
is ever computed, no solution form is ever selected, and a sequential-switching
problem is simply one more run.

::: problem NR12's Example 7.1

**Determining the Natural Response of an RL Circuit.**

The switch in the circuit shown in Fig. 7.6 has been closed for a long time before it is opened at $t$ = 0. Find a) $i_L(t)$ for *t* ≥ 0, b) $i_o(t)$ for *t* ≥ 0+, c) $v_o(t)$ for *t* ≥ 0+.

::: figure assets/circuit/nr12-ex7-1.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.1
:::

::: answer
A switched circuit is two runs: a DC pass for the initial current, then TR with that number in the inductor's fifth field. No time constant is ever computed.

```field 9 Circuit Description
l,1,0,2,20
r1,1,2,2
r2,2,0,10
r3,2,0,40
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through l
i_{l} = 20 e^{- 5 t}\,\mathrm{A}
:::

::: result current through r3
i_{r3} = - 4 e^{- 5 t}\,\mathrm{A}
:::

::: result voltage at node 2
v_{2} = - 160 e^{- 5 t}\,\mathrm{V}
:::

:::
:::

::: problem NR12's Example 7.3

**Determining the Natural Response of an RC Circuit.**

The switch has been in position x for a long time. At t = 0 it moves instantaneously to position y. Find a) vC(t), b) vo(t) and c) io(t).

::: figure assets/circuit/nr12-ex7-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.3
:::

::: answer
The capacitor's starting voltage goes in its fifth field and the answers come back as functions of t. No time constant is computed anywhere.

```field 9 Circuit Description
c,1,0,0.5'u,100
r1,1,2,32'k
r2,2,0,240'k
r3,2,0,60'k
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result voltage at node 1
v_{1} = 100 e^{- 25 t}\,\mathrm{V}
:::

::: result voltage at node 2
v_{2} = 60 e^{- 25 t}\,\mathrm{V}
:::

::: result current through r3
i_{r3} = 0.001 e^{- 25 t}\,\mathrm{A}
:::

:::
:::

::: problem NR12's Example 7.5

**Determining the Step Response of an RL Circuit.**

The switch has been in position a for a long time. At t = 0 it moves from a to b. a) Find i(t) for t ≥ 0. b) What is the initial voltage across the inductor just after the switch has been moved?

::: figure assets/circuit/nr12-ex7-5.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.5
:::

::: answer
A step response with a non-zero, negative starting current — the inductor was carrying the 8 A source the other way. Part (b) is the answer at t = 0.

```field 9 Circuit Description
e,1,0,24
r1,1,2,2
l,2,0,0.2,-8
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through l
i_{l} = 12 - 20 e^{- 10 t}\,\mathrm{A}
:::

::: result voltage at node 2
v_{2} = 40 e^{- 10 t}\,\mathrm{V}
:::

:::
:::

::: problem NR12's Example 7.10

**Determining the Step Response of a Circuit with Magnetically Coupled Coils.**

There is no energy stored in the circuit at the time the switch is closed. Find the solutions for io, vo, {{var:i_1}} and {{var:i_2}}.

::: figure assets/circuit/nr12-ex7-10.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.10
:::

::: answer
The book replaces the coupled pair with one 1.5 H equivalent and then works back to {{var:i_1}} and {{var:i_2}} through KVL. The m element is one line, and both coil currents come back on their own.

```field 9 Circuit Description
e,1,0,120
r1,1,2,7.5
l1,2,0,3
l2,2,0,15
m,l1,l2,6
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through r1
i_{r1} = 16 - 16 e^{- 5 t}\,\mathrm{A}
:::

::: result voltage at node 2
v_{2} = 120 e^{- 5 t}\,\mathrm{V}
:::

::: result current through l1
i_{l1} = 24 - 24 e^{- 5 t}\,\mathrm{A}
:::

::: result current through l2
i_{l2} = -8 + 8 e^{- 5 t}\,\mathrm{A}
:::

:::
:::

::: problem NR12's Example 7.11 to 35 ms

**Analyzing an RL Circuit That Has Sequential Switching (0 to 35 ms).**

Both switches have been closed for a long time. At t = 0 switch 1 is opened; 35 ms later switch 2 is opened. a) Find iL(t) for 0 ≤ t ≤ 35 ms.

::: figure assets/circuit/nr12-ex7-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.11
:::

::: answer
Sequential switching is just more runs. A DC pass on the t < 0 circuit gives iL(0) = 6 A, which is the number that goes in the inductor's fifth field here.

```field 9 Circuit Description
r6,2,0,6
r3,2,3,3
l,3,0,0.15,6
r18,3,0,18
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through l
i_{l} = 6 e^{- 40 t}\,\mathrm{A}
:::

:::
:::

::: problem NR12's Example 7.11 after 35 ms

**Analyzing an RL Circuit That Has Sequential Switching (after 35 ms).**

b) Find iL for t ≥ 35 ms. (Time is measured from the second switching.)

::: figure assets/circuit/nr12-ex7-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.11
:::

::: answer
The third run: switch 2 has dropped the 18 Ω, so the inductor now sees 9 Ω and the starting current is what the second run left at 35 ms.

```field 9 Circuit Description
r6,2,0,6
r3,2,3,3
l,3,0,0.15,1.47961
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through l
i_{l} = 1.47961 e^{- 60 t}\,\mathrm{A}
:::

:::
:::

::: problem NR12's Example 7.13

**Finding the Unbounded Response in an RC Circuit.**

a) When the switch is closed at t = 0, find vo(t). The Thévenin resistance seen by the capacitor is negative, so the response grows without bound.

::: figure assets/circuit/nr12-ex7-13.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.13
:::

::: answer
A dependent source makes the Thévenin resistance -5 kΩ, and the exponent comes back positive. Nothing had to be told that this case was different.

```field 9 Circuit Description
c,1,0,5'u,10
r1,1,0,10'k
r2,1,0,20'k
j,0,1,7*ir2
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result voltage at node 1
v_{1} = 10 e^{40 t}\,\mathrm{V}
:::

:::
:::

::: problem NR12's Example 8.2

**Finding the Overdamped Natural Response of a Parallel RLC Circuit.**

For the circuit in Fig. 8.6, v(0+) = 12 V and iL(0+) = 30 mA. Find the expression for v(t). (Example 8.3 then asks for the three branch currents.)

::: figure assets/circuit/nr12-ex8-2.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.2
:::

::: answer
Overdamped, and nothing had to say so: the book compares alpha with omega-nought and picks a solution form. Example 8.3's branch currents are in the same run.

```field 9 Circuit Description
c,1,0,0.2'u,12
l,1,0,50'm,0.03
r,1,0,200
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result voltage at node 1
v_{1} = - 14 e^{- 5000 t} + 26 e^{- 20000 t}\,\mathrm{V}
:::

::: result current through r
i_{r} = - 0.07 e^{- 5000 t} + 0.13 e^{- 20000 t}\,\mathrm{A}
:::

::: result current through l
i_{l} = 0.056 e^{- 5000 t} - 0.026 e^{- 20000 t}\,\mathrm{A}
:::

:::
:::

::: problem NR12's Example 8.4

**Finding the Underdamped Natural Response of a Parallel RLC Circuit.**

In the circuit shown, {{var:V_0}} = 0 and {{var:I_0}} = -12.25 mA. Calculate the voltage response for t ≥ 0.

::: figure assets/circuit/nr12-ex8-4.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.4
:::

::: answer
The same three lines give the underdamped case, damped sine and all. The book needs a different table row; the description does not change.

```field 9 Circuit Description
c,1,0,125'n,0
l,1,0,8,-0.01225
r,1,0,20'k
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result voltage at node 1
v_{1} = 100.021 e^{- 200 t} \sin{\left(979.796 t \right)}\,\mathrm{V}
:::

:::
:::

::: problem NR12's Example 8.11

**Finding the Natural Response of a Series RLC Circuit.**

The 0.1 µF capacitor is charged to 100 V. At t = 0 it is discharged through a series combination of a 100 mH inductor and a 560 Ω resistor. a) Find i(t). b) Find vC(t).

::: figure assets/circuit/nr12-ex8-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.11
:::

::: answer
Series rather than parallel, and again the case is not chosen by anyone. The inductor's node order is written to match the book's mesh arrow.

```field 9 Circuit Description
c,1,0,0.1'u,100
l,2,1,0.1
r,2,0,560
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through l
i_{l} = - 0.104167 e^{- 2800 t} \sin{\left(9600 t \right)}\,\mathrm{A}
:::

:::
:::

::: problem NR12's Example 8.12

**Finding the Step Response of a Series RLC Circuit.**

No energy is stored in the 100 mH inductor or the 0.4 µF capacitor when the switch is closed. Find vC(t) for t ≥ 0.

::: figure assets/circuit/nr12-ex8-12.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.12
:::

::: answer
A step response on a series RLC: the final value, the two roots and both coefficients arrive together in one expression.

```field 9 Circuit Description
e,1,0,48
l,1,2,0.1
r,2,3,1250
c,3,0,0.4'u
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result voltage at node 3
v_{3} = 48 - 64 e^{- 2500 t} + 16 e^{- 10000 t}\,\mathrm{V}
:::

:::
:::

::: problem NR12's Example 13.5

**Analyzing a Circuit with Multiple Meshes.**

The circuit has no initial stored energy. At t = 0 the switch closes. Use Laplace methods to find {{var:i_1}}(t) and {{var:i_2}}(t) for t ≥ 0.

::: figure assets/circuit/nr12-ex13-5.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.5
:::

::: answer
Two coupled mesh equations, a partial-fraction expansion and two inverse transforms in the book. Choosing TR does all of it and prints {{var:i_1}} and {{var:i_2}}.

```field 9 Circuit Description
e,1,0,336
l1,1,2,8.4
r1,2,0,42
l2,2,3,10
r2,3,0,48
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through l1
i_{l1} = 15 - 14 e^{- 2 t} - e^{- 12 t}\,\mathrm{A}
:::

::: result current through l2
i_{l2} = 7 - 8.4 e^{- 2 t} + 1.4 e^{- 12 t}\,\mathrm{A}
:::

:::
:::

::: problem NR12's Example 13.7

**Analyzing a Circuit with Mutual Inductance.**

The make-before-break switch has been in position a for a long time. At t = 0 it moves instantaneously to position b. Use Laplace methods to find {{var:i_2}}(t) for t ≥ 0.

::: figure assets/circuit/nr12-ex13-7.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.7
:::

::: answer
The book replaces the coupled coils with a T-equivalent and adds two voltage sources for the initial currents. Here the coupling is one m line and the initial currents are fifth fields. The secondary is an island, and Symbulator says so in a note rather than refusing the circuit.

```field 9 Circuit Description
r3,0,p,3
l1,p,0,2,5
m,l1,l2,2
l2,q,d,8,0
r2b,q,c,2
r10,c,d,10
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through l2
i_{l2} = \frac{\left(5 e^{2 t} - 5\right) e^{- 3 t}}{4}\,\mathrm{A}
:::

::: result current through l1
i_{l1} = \frac{5 \left(e^{2 t} + 1\right) e^{- 3 t}}{2}\,\mathrm{A}
:::

:::
:::

::: problem NR12's Example 13.13

**A Series Inductor Circuit with an Impulsive Response.**

The switch has been closed for a long time and opens at t = 0. Find vo(t).

::: figure assets/circuit/nr12-ex13-13.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.13
:::

::: answer
Opening the switch forces two inductors carrying different currents into series, so the voltage has to contain an impulse. The answer says DiracDelta(t) — the current jumps from 10 A to 6 A, and the algebra is what noticed.

```field 9 Circuit Description
e,1,0,100
r1,1,2,10
l1,2,3,3,10
r2,3,4,15
l2,4,0,2,0
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result voltage at node 3
v_{3} = 12 \delta\left(t\right) + 60 + 10 e^{- 5 t}\,\mathrm{V}
:::

::: result current through l1
i_{l1} = 4 + 2 e^{- 5 t}\,\mathrm{A}
:::

:::
:::

## Sinusoidal steady state — AC {#nr12-ac}

Eight problems in the sinusoidal steady state. Impedances given in
ohms go in as they are written, complex ones included, and then the frequency
never enters — which is why several of these leave **omega** as a symbol.
Where the book gives henries and farads instead, the frequency goes in the
{{ui:ω — angular frequency}} box and the conversion is the solver's.

::: problem NR12's Example 9.9

**Combining Impedances in Series and in Parallel.**

The sinusoidal current source produces is = 8 cos 200,000t A. b) Find the equivalent admittance to the right of the source. c) Find the phasor voltage V. d) Find the phasor current I. e) Find the steady-state expressions for v and i.

::: figure assets/circuit/nr12-ex9-9.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.9
:::

::: answer
Henries and farads go in as they are given: the solver turns them into {{var:j_8}} and -{{var:j_5}} at the stated frequency. V comes back 40 at -36.87 degrees and I 4 at -90.

```field 9 Circuit Description
j,0,1,8
r1,1,0,10
r2,1,2,6
l,2,0,40'u
c,1,0,1'u
```

Set {{ui:Analysis}} to *AC — alternating current*. Put **200000** in the {{ui:ω — angular frequency}} box.

Symbulator returns `v_1` = {{o:32 - 24j}} V ({{o:40.00}}∠{{o:-36.87}}°) and `i_r2` = {{o:-4j}} A ({{o:4.000}}∠{{o:-90.00}}°) — the same answers the book prints.

:::
:::

::: problem NR12's Example 9.10

**Using a Delta-to-Wye Transform in the Frequency Domain.**

Use a delta-to-wye impedance transformation to find {{var:I_0}}, {{var:I_1}}, {{var:I_2}}, {{var:I_3}}, {{var:I_4}}, {{var:I_5}}, {{var:V_1}} and {{var:V_2}} in the circuit in Fig. 9.23.

::: figure assets/circuit/nr12-ex9-10.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.10
:::

::: answer
Impedances go in as Ω, complex ones included, so the frequency never has to be known. Eight answers the book gets by transforming and working back.

```field 9 Circuit Description
e,a,0,120
r1,a,b,-4j
r2,a,c,63.2+2.4j
r3,b,c,10
r4,b,0,20+60j
r5,c,0,-20j
```

Set {{ui:Analysis}} to *AC — alternating current*. Every impedance is given in ohms, so the frequency never enters: leave **omega** in the {{ui:ω — angular frequency}} box.

Symbulator returns `-i_e` = {{o:2.4 + 3.2j}} A ({{o:4.000}}∠{{o:53.13}}°), `i_r1` = {{o:2 + 2.66667j}} A ({{o:3.333}}∠{{o:53.13}}°), `i_r3` = {{o:1.33333 + 4.26667j}} A ({{o:4.470}}∠{{o:72.65}}°), `i_r4` = {{o:0.666667 - 1.6j}} A ({{o:1.733}}∠{{o:-67.38}}°), `i_r5` = {{o:1.73333 + 4.8j}} A ({{o:5.103}}∠{{o:70.14}}°), `v_b` = {{o:109.333 + 8j}} V ({{o:109.6}}∠{{o:4.185}}°) and `v_c` = {{o:96 - 34.6667j}} V ({{o:102.1}}∠{{o:-19.86}}°) — the same answers the book prints.

:::
:::

::: problem NR12's Example 9.12

**Finding a Thévenin Equivalent in the Frequency Domain.**

Find the Thévenin equivalent circuit with respect to terminals a,b for the circuit shown in Fig. 9.32.

::: figure assets/circuit/nr12-ex9-12.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.12
:::

::: answer
A dependent source means the Thévenin resistance cannot be found by inspection; the book needs a test source. The tool returns both numbers.

```field 9 Circuit Description
e,1,0,120
r1,1,2,12
r2,2,0,60
r3,2,9,-40j
e2,3,0,10*v2
r4,3,9,120
```

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **9** and **0**. Set {{ui:Analysis}} to *AC — alternating current*. Every impedance is given in ohms, so the frequency never enters: leave **omega** in the {{ui:ω — angular frequency}} box.

Symbulator returns `vth` = {{o:784 - 288j}} V ({{o:835.2}}∠{{o:-20.17}}°) and `z` = {{o:91.2 - 38.4j}} Ω ({{o:98.95}}∠{{o:-22.83}}°) — the same answers the book prints.

:::
:::

::: problem NR12's Example 9.14

**Using the Mesh-Current Method in the Frequency Domain.**

Use the mesh-current method to find the voltages {{var:V_1}}, {{var:V_2}} and {{var:V_3}} in the circuit shown in Fig. 9.39.

::: figure assets/circuit/nr12-ex9-14.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.14
:::

::: answer
Two mesh equations and a constraint in the book. Here the controlling current is just the name of the answer it is, written into the dependent source's value.

```field 9 Circuit Description
e,1,0,150
r1,1,2,1
r2,2,a,2j
r3,a,c,12
r4,c,0,-16j
r5,a,4,1
r6,4,b,3j
e2,b,0,39*ir3
```

Set {{ui:Analysis}} to *AC — alternating current*. Every impedance is given in ohms, so the frequency never enters: leave **omega** in the {{ui:ω — angular frequency}} box.

Symbulator returns `v_1 - v_a` = {{o:78 - 104j}} V ({{o:130.0}}∠{{o:-53.13}}°), `v_a` = {{o:72 + 104j}} V ({{o:126.5}}∠{{o:55.30}}°), `v_a - v_b` = {{o:150 - 130j}} V ({{o:198.5}}∠{{o:-40.91}}°) and `i_r3` = {{o:-2 + 6j}} A ({{o:6.325}}∠{{o:108.4}}°) — the same answers the book prints.

:::
:::

::: problem NR12's Example 9.15

**Analyzing a Linear Transformer in the Frequency Domain.**

A linear transformer has {{var:R_1}} = 200 Ω, {{var:R_2}} = 100 Ω, {{var:L_1}} = 9 H, {{var:L_2}} = 4 H, k = 0.5, and couples an 800 Ω + 1 µF load to a 300 V (rms) source of internal impedance 500 + j100 at 400 rad/s. g) Calculate the Thévenin equivalent with respect to the terminals of the load.

::: figure assets/circuit/nr12-ex9-15.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.15
:::

::: answer
The primary is grounded and the secondary is not: its foot is node **d**, a name like any other. Nothing conducts from one winding to the other, so the secondary's absolute potentials are undefined — its currents and its voltage differences are not — and Symbulator says so in a note, measuring that side against d. Self-impedance, reflected impedance and the scaling factor are three of the book's seven parts; name the load's two terminals and the tool answers the last outright.

```field 9 Circuit Description
e,1,0,300
r1,1,2,500
r2,2,a,100j
r3,a,p,200
r4,p,0,3600j
m,r4,r5,1200j
r5,q,d,1600j
r6,q,c,100
```

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **c** and **d**. Set {{ui:Analysis}} to *AC — alternating current*. Every impedance is given in ohms, so the frequency never enters: leave **omega** in the {{ui:ω — angular frequency}} box. Tick {{ui:RMS phasors}} in {{card:Settings}}, since the book's source is given in rms.

Symbulator returns `vth` = {{o:93.9351 + 17.7715j}} V ({{o:95.60}}∠{{o:10.71}}°) and `z` = {{o:171.086 + 1224.26j}} Ω ({{o:1236}}∠{{o:82.04}}°) — the same answers the book prints.

:::
:::

::: problem NR12's Example 10.8

**Balancing Power Delivered with Power Absorbed in an AC Circuit.**

a) Calculate the total average and reactive power delivered to each impedance in the circuit shown in Fig. 10.18. b) Calculate the average and reactive powers associated with each source. c) Verify that the average power delivered equals the average power absorbed, and likewise for the reactive power.

::: figure assets/circuit/nr12-ex10-8.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 10.8
:::

::: answer
Every element reports its own complex power, so part (a) and part (b) are one run. Part (c) — the balance the book checks by hand — is the sum of the s answers, and it is exactly zero.

```field 9 Circuit Description
e,1,0,150
r1,1,2,1
r2,2,a,2j
r3,a,c,12
r4,c,0,-16j
r5,a,4,1
r6,4,b,3j
e2,b,0,39*ir3
```

Set {{ui:Analysis}} to *AC — alternating current*. Every impedance is given in ohms, so the frequency never enters: leave **omega** in the {{ui:ω — angular frequency}} box.

Symbulator returns `s_r1 + s_r2` = {{o:1690 + 3380j}} VA ({{o:3779}}∠{{o:63.43}}°), `s_r3 + s_r4` = {{o:240 - 320j}} VA ({{o:400.0}}∠{{o:-53.13}}°), `s_r5 + s_r6` = {{o:1970 + 5910j}} VA ({{o:6230}}∠{{o:71.57}}°), `s_e` = {{o:1950 - 3900j}} VA ({{o:4360}}∠{{o:-63.43}}°), `s_e2` = {{o:-5850 - 5070j}} VA ({{o:7741}}∠{{o:-139.1}}°) and `the sum of all eight` = {{o:0}} VA — the same answers the book prints.

:::
:::

::: problem NR12's Example 10.12

**Finding Maximum Power Transfer in a Circuit with an Ideal Transformer.**

The variable resistor is adjusted until maximum average power is delivered to RL. a) What is the value of RL in Ω? b) What is the maximum average power delivered to RL?

::: figure assets/circuit/nr12-ex10-12.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 10.12
:::

::: answer
An ideal transformer whose windings share a node, so both ports are written as bracketed terminal pairs. The book works the constraint equations twice, once open-circuit and once short-circuit; the tool returns -210 V, 35 Ω and 315 W.

```field 9 Circuit Description
e,1,0,840
r60,1,p,60
t,[p,x],[x,a],[4,1]
r20,x,0,20
```

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **a** and **0**. Set {{ui:Analysis}} to *AC — alternating current*. Every impedance is given in ohms, so the frequency never enters: leave **omega** in the {{ui:ω — angular frequency}} box. Tick {{ui:RMS phasors}} in {{card:Settings}}, since the book's source is given in rms.

Symbulator returns `vth` = {{o:-210}} V, `z` = {{o:35}} Ω and `pmax` = {{o:315}} W — the same answers the book prints.

:::
:::

::: problem NR12's Example 11.1

**Analyzing a Wye-Wye Circuit.**

A balanced, positive-sequence Y-connected generator with internal impedance 0.2 + {{var:j_0}}.5 Ω per phase and internal voltage 120 V per phase feeds a balanced Y-connected load of 39 + {{var:j_28}} Ω per phase over a line of 0.8 + {{var:j_1}}.5 Ω per phase. b) Calculate the three line currents. c) Calculate the phase voltages at the load. d) Calculate the line voltages at the load. e) Calculate the phase voltages at the generator terminals.

::: figure assets/circuit/nr12-ex11-1.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 11.1
:::

::: answer
There is no three-phase mode and none is needed. The whole circuit goes in — three sources carrying their phase in the value — rather than the single-phase equivalent the book has to construct first. The neutral comes back at exactly zero, which is the balance, measured rather than assumed.

```field 9 Circuit Description
ea,ga,0,120
eb,gb,0,120*exp(-2j*pi/3)
ec,gc,0,120*exp(2j*pi/3)
rga,ga,a,0.2+0.5j
rgb,gb,b,0.2+0.5j
rgc,gc,c,0.2+0.5j
rla,a,pa,0.8+1.5j
rlb,b,pb,0.8+1.5j
rlc,c,pc,0.8+1.5j
rfa,pa,nn,39+28j
rfb,pb,nn,39+28j
rfc,pc,nn,39+28j
```

Set {{ui:Analysis}} to *AC — alternating current*. Every impedance is given in ohms, so the frequency never enters: leave **omega** in the {{ui:ω — angular frequency}} box.

Symbulator returns `i_rla` = {{o:1.92 - 1.44j}} A ({{o:2.400}}∠{{o:-36.87}}°), `|v_pa - v_nn|` = {{o:115.225}} V, `|v_pa - v_pb|` = {{o:199.576}} V, `|v_a|` = {{o:118.898}} V and `v_nn` = {{o:0}} V — the same answers the book prints.

:::
:::

## The s domain — FD {#nr12-fd}

Five problems in the *s* domain. FD returns every answer as a function
of *s*, initial conditions included, which makes a transfer function nothing
more than the answer with the source left as a symbol. Nothing on this page is
labelled *filter* or *transfer function*, because nothing needs to be.

::: problem NR12's Example 13.2

**The Natural Response of an RC Circuit.**

The switch has been in position x for a long time; at t = 0 it moves to y. Use the Laplace transform method to find vo(t). (The same circuit as Example 7.3, worked in the s domain.)

::: figure assets/circuit/nr12-ex13-2.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.2
:::

::: answer
The same description as Example 7.3 with FD chosen instead of TR: the answers come back as transforms rather than as functions of t. One circuit, two domains, no re-typing.

```field 9 Circuit Description
c,1,0,0.5'u,100
r1,1,2,32'k
r2,2,0,240'k
r3,2,0,60'k
```

Set {{ui:Analysis}} to *FD — complex frequency domain*.

::: result voltage at node 1
v_{1} = \frac{100}{s + 25}\,\mathrm{V}
:::

::: result voltage at node 2
v_{2} = \frac{60}{s + 25}\,\mathrm{V}
:::

:::
:::

::: problem NR12's Example 13.3

**The Step Response of an RLC Circuit.**

The initial current in the inductor is 29 mA and the initial voltage across the capacitor is 50 V. Use the Laplace transform method to find v(t) for t ≥ 0.

::: figure assets/circuit/nr12-ex13-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.3
:::

::: answer
The book combines three parallel impedances and adds three current sources, two of them standing for the initial conditions. Here the initial conditions are the fifth field of c and l, and V(s) is the answer.

```field 9 Circuit Description
j,0,1,0.024/s
c,1,0,25'n,50
l,1,0,25'm,0.029
r,1,0,500
```

Set {{ui:Analysis}} to *FD — complex frequency domain*.

::: result voltage at node 1
v_{1} = \frac{50 s - 200000}{s^{2} + 80000 s + 1600000000}\,\mathrm{V}
:::

:::
:::

::: problem NR12's Example 13.6

**Creating a Thévenin Equivalent in the s Domain.**

Find the Thévenin equivalent with respect to terminals a,b for the circuit shown in Fig. 13.20.

::: figure assets/circuit/nr12-ex13-6.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.6
:::

::: answer
The Thévenin tool works in the s domain too, so the equivalent comes back as a pair of rational functions rather than a pair of numbers.

```field 9 Circuit Description
e,1,0,480/s
r1,1,2,20
l,2,0,0.002
r2,2,a,60
```

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **a** and **0**. Set {{ui:Analysis}} to *FD — complex frequency domain*.

::: result Thevenin voltage
V_{Th} = \frac{480}{s + 10000}\,\mathrm{V}
:::

::: result Thevenin impedance
Z_{Th} = \frac{80 s + 600000}{s + 10000}\,\Omega
:::

:::
:::

::: problem NR12's Example 13.9

**Deriving the Transfer Function of a Circuit.**

Derive the transfer function H(s) = Vo/Vg for the circuit in Fig. 13.31.

::: figure assets/circuit/nr12-ex13-9.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.9
:::

::: answer
Nothing is labelled 'transfer function' because nothing needs to be: leave the source as a symbol, run FD, and divide. The poles and zeros are then the expression's own.

```field 9 Circuit Description
e,1,0,vg
r1,1,2,1000
r2,2,3,250
l,3,0,50'm
c,2,0,1'u
```

Set {{ui:Analysis}} to *FD — complex frequency domain*.

::: result transfer function
H(s) = \dfrac{v_{2}}{v_{g}} = \frac{1000 \left(s + 5000\right)}{s^{2} + 6000 s + 25000000}
:::

:::
:::

::: problem NR12's Example 14.6

**Designing a Parallel RLC Bandpass Filter.**

a) Show that the RLC circuit in Fig. 14.22 is a bandpass filter by deriving an expression for the transfer function H(s). b) Compute the centre frequency. c) Calculate the cutoff frequencies, the bandwidth and Q. d) Compute R and L for a centre frequency of 5 kHz and a bandwidth of 200 Hz, using a 5 µF capacitor.

::: figure assets/circuit/nr12-ex14-6.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 14.6
:::

::: answer
Nothing in Symbulator is filter-shaped. Leave R, L and C as symbols, run FD, and the standard bandpass form appears — from which the centre frequency, the bandwidth and part (d)'s R = 159.2 Ω and L = 202.6 µH are ordinary algebra.

```field 9 Circuit Description
e,1,0,vi
rr,1,2,R
c,2,0,C
l,2,0,L
```

Set {{ui:Analysis}} to *FD — complex frequency domain*.

::: result transfer function
H(s) = \dfrac{v_{2}}{v_{i}} = \frac{L s}{C L R s^{2} + L s + R}
:::

:::
:::
