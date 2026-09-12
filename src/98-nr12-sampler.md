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

Here is a selection of problems from *Electric Circuits*, 12th edition, by
James W. Nilsson and Susan A. Riedel (Pearson). These are not the easiest
problems in the book, but they are well suited to showing what Symbulator
can do, since they are the ones where the distance between *describing a
circuit* and *solving it by hand* is widest.

::: note What this chapter is not
This is not a solutions manual, and it will not teach you circuit analysis.
Every example here is worked in full in the book itself, and the book's
derivation is the part worth reading. This is a demonstration, aimed at someone who already
knows the material and wants to see how the software deals with it.
:::

The problems and diagrams are reproduced for the purpose of teaching students how to use
Symbulator, under the principle of fair use. No copyright infringement is intended.

## How to read an entry {#nr12-how}

Each entry gives the book's question, the book's own figure, the Symbulator
description, the analysis to choose, and the answers. Every value on the page,
in a panel or in a sentence, was compared with the answer the book prints, and
they agree. Where the two are written differently — the book rounds an amplitude, or asks for the current a source *supplies*
where Symbulator reports what it *consumes* — the entry's paragraph says so.

The names are the app's own. `i_r3` is the current through the element called
`r3`, `v_2` the voltage at node 2, `p_e` the power consumed by the source called
`e`, and `v_r6` the voltage across `r6`. The book names its quantities
differently — $i_o$, $v_o$, $V_{Th}$ — so each entry says which of the app's
answers is which of the book's.

### Every circuit is in the app already {#nr12-entries}

Nothing here has to be typed. All forty-three circuits ship with Symbulator as
a built-in example book — open {{card:Built-in Examples}} and pick
*Nilsson & Riedel 12ed* from the list of books; the entries are named for the
example each one comes from, and each arrives with its note, its picture, its
settings, its Expert Mode fields and the analysis it wants already set.

Pick one, press {{btn:Run Symbulator}}, and the answers below are what you get.
{{ref:input-files}} explains what an entry remembers and how to save your own.

## Direct current — DC {#nr12-dc}

Sixteen resistive problems. The running theme is that the book's
*method* — node voltages, mesh currents, source transformations, superposition,
a delta-to-wye transform — is a way of getting an answer by hand, not a property
of the answer. Symbulator is told the circuit and never told the method, so the
same kind of description serves whichever chapter a problem came from. Five of
these are op-amp problems with lettered parts, two run in {{card:Expert Mode}},
and the last two are two-port problems from the book's final chapter.

::: problem NR12's Example 3.7

Use current division to find the current $i_o$ and use voltage division to find the voltage $v_o$ for the circuit in Fig. 3.22.

::: figure assets/circuit/nr12-ex3-7.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 3.7
:::

::: answer
The book applies two division formulas, one for the current and one for the voltage, after first reducing the circuit to find the equivalent resistance the source sees. Symbulator solves the whole circuit at once and both answers are among the results.

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

Symbulator returns `i_r7` = {{o:2}} A (the book's $i_o$) and `v_r6` = {{o:18}} V (the book's $v_o$).

:::
:::

::: problem NR12's Example 3.10

For the Wheatstone bridge in Fig. 3.30, $R_3$ can be varied from 10 Ω to 2 kΩ. What range of resistor values can this bridge measure?

::: figure assets/circuit/nr12-ex3-10.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 3.10
:::

::: answer
Balance is a statement about an answer — no current in the detector, `rg` — rather than a value the reader supplies, so it goes into {{card:Expert Mode}} as the equation `i_rg = 0`, and the unknown is the resistor being measured. The source is left as the symbol `vs`, because the balance does not depend on it, and the answer comes back symbolic too: `rx = 4*r3`. The book's range is that one line read at each end of the dial — 10 Ω to 2 kΩ gives 40 Ω to 8 kΩ.

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

Find the current and power supplied by the 40 V source in the circuit shown in Fig. 3.35.

::: figure assets/circuit/nr12-ex3-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 3.11
:::

::: answer
Series and parallel steps cannot reduce this bridge, so the book converts one delta of resistors to a wye first and then collapses what is left to a single 80 Ω. Symbulator takes the six resistors as they stand. One thing to read carefully: the book asks for the current and power the source *supplies*, and Symbulator reports what every element *consumes*, so the book's two answers are the negatives of `i_e` and `p_e` — 0.5 A and 20 W. The 80 Ω the transform was for is reported as `r_e`, the resistance seen by the source.

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

Symbulator returns `-i_e` = {{o:0.5}} A, `-p_e` = {{o:20}} W and `r_e` = {{o:80}} Ω.

:::
:::

::: problem NR12's Example 4.4

Use the node-voltage method to find the power dissipated in the 5 Ω resistor in the circuit shown in Fig. 4.10.

::: figure assets/circuit/nr12-ex4-4.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.4
:::

::: answer
The dependent source here is a voltage source worth eight times a current elsewhere in the circuit. The book writes two node equations, finds it has three unknowns, and adds a constraint equation expressing the controlling current in terms of the node voltages. In Symbulator the controlling current is simply named: `e2` is worth `8*ir3`, where `ir3` is the current through the 5 Ω resistor, and there is no constraint equation to write or to get wrong. The power the book asks for is `p_r3`.

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

Symbulator returns `v_2` = {{o:16}} V, `v_3` = {{o:10}} V, `i_r3` = {{o:1.2}} A and `p_r3` = {{o:7.2}} W.

:::
:::

::: problem NR12's Example 4.7

Use the mesh-current method to find the power dissipated in the 4 Ω resistor in the circuit shown in Fig. 4.23.

::: figure assets/circuit/nr12-ex4-7.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.7
:::

::: answer
The same idea with mesh currents: the book writes two mesh equations and a third for the dependent source's controlling current, expressed as a difference of mesh currents. The description is the six lines it would be without the dependent source, except that `e2` is worth `15*ir4`. Symbulator is told the circuit and never the method, so nothing here says *mesh*. The power in the 4 Ω resistor is `p_r3`.

```field 9 Circuit Description
e,1,0,50
r1,1,3,1
r2,1,2,5
r3,2,3,4
r4,2,0,20
e2,3,0,15*ir4
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_r4` = {{o:1.6}} A, `i_r3` = {{o:2}} A and `p_r3` = {{o:16}} W.

:::
:::

::: problem NR12's Example 4.8

Use the mesh-current method to find branch currents $i_a$, $i_b$ and $i_c$ in the circuit for Example 4.3, repeated here as Fig. 4.25.

::: figure assets/circuit/nr12-ex4-8.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.8
:::

::: answer
The book's special case is a current source in a branch shared by two meshes, whose voltage is unknown, so no KVL equation can be written around either mesh alone. The book's answer is the *supermesh*: merge the two meshes, write KVL around the outside of the pair, and add the constraint the source imposes. Symbulator has no meshes, so there is no special case: the current source `j` is one more line. The book's three branch currents are `i_r1`, `i_r2` and `i_r3`.

```field 9 Circuit Description
e,1,0,50
r1,1,2,5
r2,2,0,10
r3,2,0,40
j,0,2,3
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_r1` = {{o:2}} A, `i_r2` = {{o:4}} A, `i_r3` = {{o:1}} A and `v_2` = {{o:40}} V.

:::
:::

::: problem NR12's Example 4.13

a) Use source transformations to find the voltage $v_o$ in the circuit shown in Fig. 4.42. b) Find the power developed by the 250 V voltage source. c) Find the power developed by the 8 A current source.

::: figure assets/circuit/nr12-ex4-13.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.13
:::

::: answer
The *special* techniques are two: a resistor in parallel with a voltage source, and one in series with a current source, have no effect on the rest of the circuit, so the book removes them, transforms the sources that remain, and finds $v_o$ from a single loop. Then it has to put those resistors back, because they do affect what the sources deliver, which is parts (b) and (c). Symbulator solves the circuit as drawn, so nothing is removed and nothing has to be restored. The book's $v_o$ is `v_r4`; the powers *developed* by the two sources are the negatives of what Symbulator reports them consuming, `-p_e` and `-p_j`, and `-i_e` is the current the 250 V source delivers.

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

Symbulator returns `v_r4` = {{o:20}} V, `-i_e` = {{o:11.2}} A, `-p_e` = {{o:2800}} W and `-p_j` = {{o:480}} W.

:::
:::

::: problem NR12's Example 4.21

a) For the circuit shown in Fig. 4.65, find the value of $R_L$ that results in maximum power being transferred to $R_L$. b) Calculate the maximum power that can be delivered to $R_L$.

::: figure assets/circuit/nr12-ex4-21.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.21
:::

::: answer
The book finds the Thévenin equivalent at the load's terminals, because the load that draws the most power is the one equal to the Thévenin resistance, and the maximum is then $V_{Th}^2 / 4R_{Th}$. The Thévenin tool does the same in one run: `z` is the Thévenin resistance and so the load for part (a), and `pmax` is the power that load draws, part (b). The book's part (c), which asks what fraction of the source's power reaches that load, is one more DC run with `rl,2,0,25` added to the description: 900 W of 2520 W, or 35.7%.

```field 9 Circuit Description
e,1,0,360
r1,1,2,30
r2,2,0,150
```

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **2** and **0**.

Symbulator returns `vth` = {{o:300}} V, `z` = {{o:25}} Ω and `pmax` = {{o:900}} W.

:::
:::

::: problem NR12's Example 4.23

Use the principle of superposition to find $v_o$ in the circuit shown in Fig. 4.71.

::: figure assets/circuit/nr12-ex4-23.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.23
:::

::: answer
Superposition is a way of getting an answer by hand — solve once for each independent source with the others switched off, then add — and it is not a property of the answer. Symbulator never uses it. The two dependent sources, `j2` worth `0.4*vr3` and `e2` worth `2*ir1`, stay in the circuit throughout, exactly as they must in each of the book's two partial solutions, and the two independent sources are solved together. The book's $v_o$ is `v_r2`.

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

Symbulator returns `v_r2` = {{o:24}} V, `v_r3` = {{o:10}} V and `i_r1` = {{o:-2.8}} A.

:::
:::

::: problem NR12's Example 5.1

The op amp in the circuit shown in Fig. 5.7 is ideal. a) Calculate $v_o$ if $v_a$ = 1 V and $v_b$ = 0 V. b) Repeat (a) for $v_a$ = 1 V and $v_b$ = 2 V. c) If $v_a$ = 1.5 V, specify the range of $v_b$ that avoids amplifier saturation.

::: figure assets/circuit/nr12-ex5-1.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.1
:::

::: answer
An ideal op amp does not know its supplies exist. Symbulator's `o` element reports whatever output the inputs demand, 200 V as readily as 2 V, so saturation is a question you ask of the answer rather than something the solve enforces. With both inputs left as the symbols `va` and `vb`, one run returns the output as a formula, and each part of the question is read off it; the supplies in the figure are ±10 V, which is what part (c) checks against.

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

**a)** With {{var:v_a}} = 1 V and {{var:v_b}} = 0 V the formula gives {{var:v_o}} = 5(0) − 4(1) = {{o:-4}} V. That is inside the ±10 V supplies, so the op amp is in its linear region and −4 V is the answer.

**b)** With {{var:v_a}} = 1 V and {{var:v_b}} = 2 V, {{var:v_o}} = 5(2) − 4(1) = {{o:6}} V. Inside the supplies again, so the op amp is still linear.

**c)** With {{var:v_a}} = 1.5 V the formula becomes {{var:v_o}} = 5{{var:v_b}} − 6. The op amp stays linear while that lies between the rails, so Symbulator is asked the question directly: put `v_3 = 10` in {{card:Expert Mode}} with `vb` as the unknown, then again with `v_3 = -10`. The rails are reached at {{var:v_b}} = {{o:3.2}} V and {{var:v_b}} = {{o:-0.8}} V, so the range is {{o:-0.8}} V ≤ {{var:v_b}} ≤ {{o:3.2}} V.

:::
:::

::: problem NR12's Example 5.3

a) Design a summing amplifier whose output voltage is $v_o = -4v_a - v_b - 5v_c$, using an ideal op amp with ±12 V power supplies and a 20 kΩ feedback resistor. b) Suppose $v_a$ = 2 V and $v_c$ = $-$1 V. What range of input voltages for $v_b$ allows the op amp to remain linear?

::: figure assets/circuit/nr12-ex5-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.3
:::

::: answer
A design problem, so the run is a check rather than a solve. The book's summing-amplifier formula gives each input resistor from its gain and the feedback resistor; the circuit built from those values is then run with its three inputs as symbols, and the output comes back as exactly the formula the design was asked to produce. Part (b) asks for the range of one input that keeps the output between the ±12 V rails, which is a question for {{card:Expert Mode}}: set the output equal to a rail and ask for the input.

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

**a)** The summing-amplifier formula is {{var:v_o}} = −({{var:R_f}}/{{var:R_a}}){{var:v_a}} − ({{var:R_f}}/{{var:R_b}}){{var:v_b}} − ({{var:R_f}}/{{var:R_c}}){{var:v_c}}, so with a 20 kΩ feedback resistor the three input resistors are {{var:R_a}} = 20k/4 = {{o:5}} kΩ, {{var:R_b}} = 20k/1 = {{o:20}} kΩ and {{var:R_c}} = 20k/5 = {{o:4}} kΩ. Running that circuit returns the very formula the design was asked to hit, which is the check.

**b)** With {{var:v_a}} = 2 V and {{var:v_c}} = −1 V the output collapses to {{var:v_o}} = −{{var:v_b}} − 3. Asking {{card:Expert Mode}} for the {{var:v_b}} that puts `v_4` on each rail gives {{o:9}} V at −12 V and {{o:-15}} V at +12 V, so the op amp stays linear for {{o:-15}} V ≤ {{var:v_b}} ≤ {{o:9}} V.

:::
:::

::: problem NR12's Example 5.3 part c

c) Suppose $v_a$ = 2 V, $v_b$ = 3 V and $v_c$ = $-$1 V. Using the input resistor values found in part (a), how large can the feedback resistor be before the op amp saturates?

::: figure assets/circuit/nr12-ex5-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.3
:::

::: answer
Part (c) turns the same circuit into a different kind of question. The inputs are now numbers, the feedback resistor is the unknown, and what is known is an answer: the output sits on the −12 V rail. That is what {{card:Expert Mode}} is for — `v_4 = -12` is the equation, `rf` the unknown, and the solve returns the resistor. It is one of two examples on this page whose answer is a component value; the Wheatstone bridge above is the other.

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

Symbulator returns `rf` = {{o:40000}} Ω.

**c)** With {{var:v_a}} = 2 V, {{var:v_b}} = 3 V and {{var:v_c}} = −1 V the three input currents sum to a positive number, so the output swings negative and it is the −12 V rail that is reached first. Leave the feedback resistor as the symbol `rf`, put `v_4 = -12` in {{card:Expert Mode}} and name `rf` the unknown: the answer is {{o:40}} kΩ. Any larger and the op amp saturates.

:::
:::

::: problem NR12's Example 5.5

a) Design a difference amplifier that amplifies the difference between two input voltages by a gain of 8, using an ideal op amp and ±8 V power supplies. b) Suppose $v_a$ = 1 V. What range of $v_b$ keeps the op amp linear?

::: figure assets/circuit/nr12-ex5-5.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.5
:::

::: answer
A difference amplifier with a gain of 8 needs two resistor ratios to be equal, and the book picks 1.5 kΩ and 12 kΩ. Run with both inputs as symbols, the circuit returns exactly $8(v_b - v_a)$, which confirms the design; part (b)'s range then follows from that one line by setting the output to each ±8 V rail in turn.

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

**b)** With {{var:v_a}} = 1 V the output is {{var:v_o}} = 8{{var:v_b}} − 8, which reaches +8 V at {{var:v_b}} = {{o:2}} V and −8 V at {{var:v_b}} = {{o:0}} V. So the op amp remains in its linear region for {{o:0}} V ≤ {{var:v_b}} ≤ {{o:2}} V.

:::
:::

::: problem NR12's Example 5.7

Analyze the noninverting amplifier of Example 5.4 using the realistic op amp model, with open-loop gain $A$ = 50,000, input resistance $R_i$ = 100 kΩ and output resistance $R_o$ = 7.5 kΩ; there is no load resistance at the output. Find the gain $v_o/v_g$.

::: figure assets/circuit/nr12-ex5-7.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.7
:::

::: answer
There is no `o` element here. The book's realistic op amp model is a dependent voltage source with a gain of 50,000, an input resistance between its two inputs and an output resistance in series with its output, and that is what the description says: `ea` is worth `50000*(vp-vn)`, `ri` sits between nodes **p** and **n**, and `ro` is at the output. The gain, the output node's voltage divided by the symbolic source, comes out as 5.9988 against the 6 an ideal op amp would give — and that small shortfall is the whole point of the example.

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

Symbulator returns `v_3/vg` = {{o:5.9988}}.

:::
:::

::: problem NR12's Example 18.1

Find the z parameters for the circuit shown in Fig. 18.3.

::: figure assets/circuit/nr12-ex18-1.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 18.1
:::

::: answer
The book takes four open-circuit measurements — two with a source at port 1 and the other port open, two with the source moved to port 2 — and reads one z parameter from each. The two-port tool makes all four in one run and names them `z11` to `z22`. Note that `z12` = `z21`, as it must for a network of resistors, which is reciprocal: that equality is a result here, not an assumption.

```field 9 Circuit Description
r5,1,2,5
r20,1,0,20
r15,2,0,15
```

Open {{card:Find equivalent}}, choose *Two-port parameters*, kind **z**, with the ports at **1** and **2**.

Symbulator returns `z11` = {{o:10}} Ω, `z12` = {{o:7.5}} Ω, `z21` = {{o:7.5}} Ω and `z22` = {{o:9.375}} Ω.

:::
:::

::: problem NR12's Example 18.6

Two identical amplifiers are connected in cascade. Each is described by its h parameters: $h_{11}$ = 1000 Ω, $h_{12}$ = 0.0015, $h_{21}$ = 100, $h_{22}$ = 100 µS. The source has 500 Ω of internal resistance and the load is 10 kΩ. Find the voltage gain $V_2/V_g$.

::: figure assets/circuit/nr12-ex18-6.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 18.6
:::

::: answer
The book converts each amplifier's h parameters into a parameters, multiplies the two transmission matrices for the cascade, and reads the voltage gain out of a table of formulas. Symbulator's `h` element takes the four parameters as a bracketed term, so the cascade is two such lines wired end to end between the source resistance and the load, and the gain is the output node's voltage divided by the symbolic source — `v_c/vg`, a large number, and the book's.

```field 9 Circuit Description
e,1,0,vg
rs,1,a,500
h1,a,b,[1000,0.0015,100,0.0001]
h2,b,c,[1000,0.0015,100,0.0001]
rl,c,0,10'k
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `v_c/vg` = {{o:33333.3}}.

:::
:::

## Transients — TR {#nr12-tr}

Fourteen transient problems, three of them from the book's Laplace
chapter. The pattern is the one you would follow by hand: run the circuit as it
was before the switch moved in DC, read off the capacitor voltages and inductor
currents, put those numbers in the fifth field of the `c` and `l` lines, and run
the circuit as it is afterwards in TR. No time constant is computed, no solution
form is selected, and sequential switching is simply one more run. The
Laplace-chapter problems are no different: TR transforms, solves and inverts,
so what the book does in $s$ the solver does out of sight.

::: problem NR12's Example 7.1

The switch in the circuit shown in Fig. 7.6 has been closed for a long time before it is opened at $t$ = 0. Find a) $i_L(t)$ for $t$ ≥ 0, b) $i_o(t)$ for $t$ ≥ 0+, c) $v_o(t)$ for $t$ ≥ 0+.

::: figure assets/circuit/nr12-ex7-1.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.1
:::

::: answer
A switched circuit is two circuits, and two runs. With the switch closed for a long time the inductor is a short across the 20 A source, and a DC run of that circuit gives its current, 20 A. That number goes into the inductor's fifth field, its initial current, and the circuit that exists once the switch has opened is run in TR. No time constant is ever computed. The book's $i_L$ is `i_l`, its $i_o$ the current through `r3`, and its $v_o$ the voltage at node 2.

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

The switch in the circuit shown in Fig. 7.15 has been in position x for a long time. At $t$ = 0 it moves instantaneously to position y. Find a) $v_C(t)$ for $t$ ≥ 0, b) $v_o(t)$ for $t$ ≥ 0+, and c) $i_o(t)$ for $t$ ≥ 0+.

::: figure assets/circuit/nr12-ex7-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.3
:::

::: answer
The RC twin of the example above. Before the switch moves the capacitor has charged to the 100 V of the source, and that is the fifth field of the `c` line; the three answers come back as functions of $t$ sharing the one time constant, 40 ms, that the book computes from the equivalent resistance. The book's $v_C$ is the voltage at node 1, its $v_o$ the voltage at node 2 and its $i_o$ the current through `r3`.

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

The switch in the circuit shown in Fig. 7.21 has been in position a for a long time. At $t$ = 0 it moves from position a to position b. The switch is a make-before-break type, so the inductor current is continuous. a) Find the expression for $i(t)$ for $t$ ≥ 0. b) What is the initial voltage across the inductor just after the switch has been moved to position b?

::: figure assets/circuit/nr12-ex7-5.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.5
:::

::: answer
A step response whose starting current is neither zero nor in the direction the step will drive it: before the switch moves, the 8 A source was pushing current through the inductor the other way, so the inductor's fifth field reads −8. The book's point that the switch is make-before-break is what makes the inductor current continuous across the switching, and so what makes it meaningful to give an initial current at all. Part (b), the inductor voltage just after the switch moves, is `v_2` at $t$ = 0: 40 V.

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

There is no energy stored in the circuit in Fig. 7.37 at the time the switch is closed. Find the solutions for $i_o$, $v_o$, $i_1$ and $i_2$.

::: figure assets/circuit/nr12-ex7-10.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.10
:::

::: answer
Two coils on one core, both fed from the same node. The book replaces the coupled pair by a single equivalent inductance of 1.5 H, solves the RL circuit that leaves, and then works back to the two coil currents through the coupled-coil voltage equations. Here the coupling is the one `m` line, naming the two coils and their mutual inductance, and the two coil currents come back on their own beside the total. The book's $i_o$ is `i_r1`, its $v_o$ the voltage at node 2, and $i_1$ and $i_2$ are the currents through `l1` and `l2`.

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

The two switches in the circuit shown in Fig. 7.39 have been closed for a long time. At $t$ = 0 switch 1 is opened; then, 35 ms later, switch 2 is opened. a) Find $i_L(t)$ for 0 ≤ $t$ ≤ 35 ms.

::: figure assets/circuit/nr12-ex7-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.11
:::

::: answer
Sequential switching is not a new kind of problem, only more runs. A DC run of the circuit with both switches closed gives the inductor current before anything happens, 6 A, and that is the fifth field here. The description is the circuit that exists after switch 1 has opened, and its answer holds until switch 2 opens at 35 ms.

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

b) Find $i_L(t)$ for $t$ ≥ 35 ms. (Time is measured from the second switching.)

::: figure assets/circuit/nr12-ex7-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.11
:::

::: answer
The third run. Switch 2 has removed the 18 Ω resistor, so the inductor now sees the 6 Ω and 3 Ω in series, 9 Ω, and the time constant changes. Its starting current is whatever the previous run left at 35 ms — `6*exp(-40*0.035)`, 1.48 A — and time is measured from the second switching, as the book measures it too.

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

a) When the switch is closed in the circuit shown in Fig. 7.45, the voltage on the capacitor is 10 V. Find the expression for $v_o$ for $t$ ≥ 0. b) Assume that the capacitor short-circuits when its terminal voltage reaches 150 V. How many milliseconds elapse before the capacitor short-circuits?

::: figure assets/circuit/nr12-ex7-13.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.13
:::

::: answer
A dependent current source makes the resistance the capacitor sees negative, −5 kΩ, so the voltage grows instead of decaying. The book finds that Thévenin resistance first and then solves a differential equation whose exponent turns out positive. Here nothing has to be told the case is different: the dependent source is `7*ir2`, and the exponent comes back positive of its own accord. Part (b) is read off the answer — $10e^{40t}$ reaches 150 V when $40t = \ln 15$, at 67.7 ms.

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

For the circuit in Fig. 8.6, $v(0^+)$ = 12 V and $i_L(0^+)$ = 30 mA. Find the expression for $v(t)$. (Example 8.3 asks the same circuit for its three branch currents.)

::: figure assets/circuit/nr12-ex8-2.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.2
:::

::: answer
The book's parallel RLC has three cases — overdamped, critically damped, underdamped — and three solution forms, so it compares $\alpha$ with $\omega_0$ to pick one before it can write anything down. Symbulator writes nothing down: the three elements with their two initial conditions are run in TR, and the two real exponents of the overdamped case come out of the algebra. Example 8.3's branch currents are in the same run — `i_r` and `i_l` below, and `i_c` in the app.

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

In the circuit shown in Fig. 8.8, $V_0$ = 0 and $I_0$ = $-$12.25 mA. Calculate the voltage response for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex8-4.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.4
:::

::: answer
The same three lines with different values, and the underdamped case comes out: a damped sine, with the damping in the exponent and the damped frequency in the argument. The book needs a different row of its table and a different pair of constants to fit; the description does not change shape at all. The book prints the amplitude as 100 and the frequency as 979.80, both rounded; the app's answer, at six digits, shows 100.021 and 979.796 for the same expression.

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

The 0.1 µF capacitor in the circuit shown in Fig. 8.17 is charged to 100 V. At $t$ = 0 the capacitor is discharged through a series combination of a 100 mH inductor and a 560 Ω resistor. a) Find $i(t)$ for $t$ ≥ 0. b) Find $v_C(t)$ for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex8-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.11
:::

::: answer
Series rather than parallel, and again no case is chosen by anyone: the capacitor discharges through the inductor and resistor and the underdamped form arrives. One detail of the description is deliberate. The inductor's nodes are written 2 then 1 so that `i_l` is measured in the direction of the book's arrow for $i$; written the other way round, the answer comes back with the opposite sign. Part (b), $v_C$, is the voltage at node 1.

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

No energy is stored in the 100 mH inductor or the 0.4 µF capacitor when the switch in the circuit shown in Fig. 8.18 is closed. Find $v_C(t)$ for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex8-12.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.12
:::

::: answer
A step into a series RLC with no stored energy. The book finds the two roots, recognises the overdamped form, and fits its two constants to the initial conditions; here the final value of 48 V, the two roots and both coefficients arrive together in one expression. The book's $v_C$ is the voltage at node 3.

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

The circuit in Fig. 13.17 has no initial stored energy. At $t$ = 0 the switch closes. Use Laplace methods to find $i_1(t)$ and $i_2(t)$ for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex13-5.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.5
:::

::: answer
A Laplace-chapter problem, run in TR. The book writes two mesh equations in $s$, solves them, expands each answer in partial fractions and inverts both. TR does all of that in the same order and prints $i_1(t)$ and $i_2(t)$, which are the currents through the two inductors. Choose FD instead and the same run stops before the inversion, with the two transforms the book has half-way through.

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

The make-before-break switch in the circuit in Fig. 13.23 has been in position a for a long time. At $t$ = 0 it moves instantaneously to position b. Use Laplace methods to find $i_2(t)$ for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex13-7.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.7
:::

::: answer
Also from the Laplace chapter. The book replaces the coupled coils by a T-equivalent of three inductors and adds a voltage source for each initial current before it can write mesh equations in $s$. Here the coupling is the one `m` line and the initial currents are fifth fields: 5 A in the primary, which is what the DC circuit before the switch moved had established, and 0 in the secondary. The secondary is an island — nothing conducts between the two windings — and Symbulator says so in a note and refers its voltages to node **d**, rather than refusing the circuit. The book's $i_2$ is the current through `l2`.

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

The switch in the circuit shown in Fig. 13.50 has been closed for a long time. At $t$ = 0 it opens. Use Laplace methods to find the output voltage $v_o$ and the current in the 3 H inductor, $i_1$.

::: figure assets/circuit/nr12-ex13-13.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.13
:::

::: answer
Opening the switch puts two inductors that were carrying different currents — 10 A and none — into series, and since an inductor's current cannot jump, the voltage across them has to contain an impulse. The answer says so: `DiracDelta(t)` is the impulse, and its weight of 12 is what it takes to bring the 2 H inductor from 0 to the 6 A the pair settle on. The book's $v_o$ is the voltage at node 3 and its $i_1$ the current through `l1`.

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

Eight problems in the sinusoidal steady state. Where the book gives
its impedances in ohms they go in as written, complex ones included, and the
frequency never enters: **omega** is left as a symbol in the
{{ui:ω — angular frequency}} box and nothing depends on it. Where the book gives
henries and farads instead, the frequency goes in that box and the conversion to
impedance is the solver's. Two of the eight state their source in rms, and say
so in {{card:Settings}}.

::: problem NR12's Example 9.9

The sinusoidal current source in the circuit shown in Fig. 9.20 produces the current $i_s$ = 8 cos 200,000$t$ A. b) Find the equivalent admittance to the right of the current source. c) Find the phasor voltage $V$. d) Find the phasor current $I$. e) Find the steady-state expressions for $v$ and $i$.

::: figure assets/circuit/nr12-ex9-9.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.9
:::

::: answer
Henries and farads go in as the book gives them, and the frequency goes in the {{ui:ω — angular frequency}} box; the solver turns the 40 µH into $+j8$ Ω and the 1 µF into $-j5$ Ω at 200,000 rad/s, which is the book's part (a), the frequency-domain equivalent circuit. The book's $V$ is `v_1` and its $I$ the current through `r2`, and part (e) is a matter of reading each phasor as an amplitude and an angle, which the app prints beside the rectangular form: 40 V at −36.87° and 4 A at −90°.

```field 9 Circuit Description
j,0,1,8
r1,1,0,10
r2,1,2,6
l,2,0,40'u
c,1,0,1'u
```

Set {{ui:Analysis}} to *AC — alternating current*. Put **200000** in the {{ui:ω — angular frequency}} box.

Symbulator returns `v_1` = {{o:32 - 24j}} V ({{o:40.00}}∠{{o:-36.87}}°) and `i_r2` = {{o:-4j}} A ({{o:4.000}}∠{{o:-90.00}}°).

:::
:::

::: problem NR12's Example 9.10

Use a delta-to-wye impedance transformation to find $I_0$, $I_1$, $I_2$, $I_3$, $I_4$, $I_5$, $V_1$ and $V_2$ in the circuit in Fig. 9.23.

::: figure assets/circuit/nr12-ex9-10.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.10
:::

::: answer
Every impedance in this circuit is already in ohms, several of them complex, so they go in exactly as written — `-4j`, `63.2+2.4j`, `20+60j` — and the frequency never has to be known. The book has to transform a delta to a wye to reduce the circuit, and then work its way back out to the eight quantities asked for. The book's $I_0$ is the source current, `-i_e`; its $I_1$ to $I_5$ are the currents through `r1` to `r5`; and $V_1$ and $V_2$ are the voltages at nodes **b** and **c**.

```field 9 Circuit Description
e,a,0,120
r1,a,b,-4j
r2,a,c,63.2+2.4j
r3,b,c,10
r4,b,0,20+60j
r5,c,0,-20j
```

Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box; nothing here depends on the frequency.

Symbulator returns `-i_e` = {{o:2.4 + 3.2j}} A ({{o:4.000}}∠{{o:53.13}}°), `i_r1` = {{o:2 + 2.66667j}} A ({{o:3.333}}∠{{o:53.13}}°), `i_r3` = {{o:1.33333 + 4.26667j}} A ({{o:4.470}}∠{{o:72.65}}°), `i_r4` = {{o:0.666667 - 1.6j}} A ({{o:1.733}}∠{{o:-67.38}}°), `i_r5` = {{o:1.73333 + 4.8j}} A ({{o:5.103}}∠{{o:70.14}}°), `v_b` = {{o:109.333 + 8j}} V ({{o:109.6}}∠{{o:4.185}}°) and `v_c` = {{o:96 - 34.6667j}} V ({{o:102.1}}∠{{o:-19.86}}°).

:::
:::

::: problem NR12's Example 9.12

Find the Thévenin equivalent circuit with respect to terminals a,b for the circuit shown in Fig. 9.32.

::: figure assets/circuit/nr12-ex9-12.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.12
:::

::: answer
A Thévenin equivalent with a dependent source inside it. The impedance cannot be found by inspection, because a dependent source cannot be switched off, so the book applies a test source at the terminals and works out the ratio. The Thévenin tool handles it as it handles every other circuit, and returns the voltage and the impedance together. The book's terminals a and b are nodes **9** and **0**.

```field 9 Circuit Description
e,1,0,120
r1,1,2,12
r2,2,0,60
r3,2,9,-40j
e2,3,0,10*v2
r4,3,9,120
```

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **9** and **0**. Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box; nothing here depends on the frequency.

Symbulator returns `vth` = {{o:784 - 288j}} V ({{o:835.2}}∠{{o:-20.17}}°) and `z` = {{o:91.2 - 38.4j}} Ω ({{o:98.95}}∠{{o:-22.83}}°).

:::
:::

::: problem NR12's Example 9.14

Use the mesh-current method to find the voltages $V_1$, $V_2$ and $V_3$ in the circuit shown in Fig. 9.39.

::: figure assets/circuit/nr12-ex9-14.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.14
:::

::: answer
The frequency-domain counterpart of Example 4.7 above: two mesh equations, a dependent source, and a constraint defining its controlling current as a difference of mesh currents. As in DC, the controlling current is simply named — `e2` is worth `39*ir3` — and no constraint appears. The book's $V_1$, $V_2$ and $V_3$ are the drops across three impedances rather than node voltages, so two of them are printed as differences between node voltages, and the third is the voltage at node **a** itself.

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

Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box; nothing here depends on the frequency.

Symbulator returns `v_1 - v_a` = {{o:78 - 104j}} V ({{o:130.0}}∠{{o:-53.13}}°), `v_a` = {{o:72 + 104j}} V ({{o:126.5}}∠{{o:55.30}}°), `v_a - v_b` = {{o:150 - 130j}} V ({{o:198.5}}∠{{o:-40.91}}°) and `i_r3` = {{o:-2 + 6j}} A ({{o:6.325}}∠{{o:108.4}}°).

:::
:::

::: problem NR12's Example 9.15

A linear transformer has $R_1$ = 200 Ω, $R_2$ = 100 Ω, $L_1$ = 9 H, $L_2$ = 4 H and $k$ = 0.5, and couples a load of an 800 Ω resistor in series with a 1 µF capacitor to a 300 V (rms) source of internal impedance $500 + j100$ Ω at 400 rad/s. g) Calculate the Thévenin equivalent with respect to the terminals of the load impedance.

::: figure assets/circuit/nr12-ex9-15.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.15
:::

::: answer
The book's question has seven lettered parts, and (b) to (f) — the two self-impedances, the reflected impedance, its scaling factor, the impedance seen at the primary — are the steps of its method for reaching (g). Name the load's two terminals, **c** and **d**, and the Thévenin tool answers (g) outright. Two details of the description matter. The coils are written as impedances at the given 400 rad/s — $j3600$, $j1600$ and the mutual $j1200$ — so the coupling line reads `m,r4,r5,1200j`, with the coupled pair named as `r` elements. And the secondary is not grounded: its foot is node **d**, a name like any other, and nothing conducts between the two windings. Symbulator says so in a note and measures that side against **d**, which leaves its currents, its voltage differences and the Thévenin equivalent all unaffected. The source is given in rms, so {{ui:RMS phasors}} is ticked.

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

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **c** and **d**. Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box; nothing here depends on the frequency. Tick {{ui:RMS phasors}} in {{card:Settings}}, since the book's source is given in rms.

Symbulator returns `vth` = {{o:93.9351 + 17.7715j}} V ({{o:95.60}}∠{{o:10.71}}°) and `z` = {{o:171.086 + 1224.26j}} Ω ({{o:1236}}∠{{o:82.04}}°).

:::
:::

::: problem NR12's Example 10.8

a) Calculate the total average and reactive power delivered to each impedance in the circuit shown in Fig. 10.18. b) Calculate the average and reactive powers associated with each source. c) Verify that the average power delivered equals the average power absorbed, and likewise for the reactive power.

::: figure assets/circuit/nr12-ex10-8.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 10.8
:::

::: answer
The circuit of Example 9.14, asked a different question. Every element reports its complex power, `s_r1`, `s_e` and so on, whose real part is the average power and whose imaginary part the reactive power, so parts (a) and (b) are one run. Each of the book's impedances is a pair of elements here — its $1 + j2$ Ω is `r1` and `r2` — so each is the sum of two `s` answers. Part (c), the balance the book verifies by adding up its own figures, is the sum of all eight, and it is exactly zero.

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

Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box; nothing here depends on the frequency.

Symbulator returns `s_r1 + s_r2` = {{o:1690 + 3380j}} VA ({{o:3779}}∠{{o:63.43}}°), `s_r3 + s_r4` = {{o:240 - 320j}} VA ({{o:400.0}}∠{{o:-53.13}}°), `s_r5 + s_r6` = {{o:1970 + 5910j}} VA ({{o:6230}}∠{{o:71.57}}°), `s_e` = {{o:1950 - 3900j}} VA ({{o:4360}}∠{{o:-63.43}}°), `s_e2` = {{o:-5850 - 5070j}} VA ({{o:7741}}∠{{o:-139.1}}°) and the sum of all eight = {{o:0}} VA.

:::
:::

::: problem NR12's Example 10.12

The variable resistor in the circuit in Fig. 10.25 is adjusted until maximum average power is delivered to $R_L$. a) What is the value of $R_L$ in ohms? b) What is the maximum average power delivered to $R_L$?

::: figure assets/circuit/nr12-ex10-12.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 10.12
:::

::: answer
An ideal transformer whose primary and secondary share a node, which is why its two ports are written as bracketed terminal pairs, `[p,x]` and `[x,a]`, with the turns ratio `[4,1]` after them. The book has to work the transformer's constraint equations twice, once with the load terminals open for the Thévenin voltage and once shorted for the Norton current, before it can divide one by the other. The Thévenin tool returns both, and the maximum average power in the same run: the book's $R_L$ is `z` and the answer to (b) is `pmax`. The source is given in rms, so {{ui:RMS phasors}} is ticked.

```field 9 Circuit Description
e,1,0,840
r60,1,p,60
t,[p,x],[x,a],[4,1]
r20,x,0,20
```

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **a** and **0**. Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box; nothing here depends on the frequency. Tick {{ui:RMS phasors}} in {{card:Settings}}, since the book's source is given in rms.

Symbulator returns `vth` = {{o:-210}} V, `z` = {{o:35}} Ω and `pmax` = {{o:315}} W.

:::
:::

::: problem NR12's Example 11.1

A balanced, positive-sequence Y-connected generator with an internal impedance of $0.2 + j0.5$ Ω per phase and an internal voltage of 120 V per phase feeds a balanced Y-connected load of $39 + j28$ Ω per phase over a line of $0.8 + j1.5$ Ω per phase; the a-phase internal voltage is the reference. b) Calculate the three line currents. c) Calculate the phase voltages at the load. d) Calculate the line voltages at the load. e) Calculate the phase voltages at the generator terminals.

::: figure assets/circuit/nr12-ex11-1.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 11.1
:::

::: answer
There is no three-phase mode, and none is needed. The book's part (a) builds a single-phase equivalent — one generator, one line, one load — because a balanced circuit can be solved one phase at a time, the other two following by shifting the angle. Symbulator takes the whole circuit: three sources whose values carry their phase, `120*exp(-2j*pi/3)` for the b-phase, and three of each impedance. Every quantity the book derives by shifting is then simply another answer in the run, and the neutral comes back at exactly zero volts — the balance the single-phase method assumes, here measured. The book's line current $I_{aA}$ is `i_rla`; its load phase voltage $V_{AN}$ is the difference between nodes **pa** and **nn**, its line voltage $V_{AB}$ the difference between **pa** and **pb**, and its generator phase voltage $V_{An}$ the voltage at node **a**. Only the magnitudes are quoted for the last three, as the book quotes them.

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

Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box; nothing here depends on the frequency.

Symbulator returns `i_rla` = {{o:1.92 - 1.44j}} A ({{o:2.400}}∠{{o:-36.87}}°), `|v_pa - v_nn|` = {{o:115.225}} V, `|v_pa - v_pb|` = {{o:199.576}} V, `|v_a|` = {{o:118.898}} V and `v_nn` = {{o:0}} V.

:::
:::

## The s domain — FD {#nr12-fd}

Five problems in the $s$ domain. FD returns every answer as a
function of $s$, initial conditions included, so a transfer function is nothing
more than the answer with the source left as a symbol — two of these are exactly
that. Nothing on this page is labelled *filter* or *transfer function*, because
nothing needs to be. The book's other Laplace-chapter examples, the ones it
inverts back into time, are in the TR section above.

::: problem NR12's Example 13.2

The circuit in Fig. 13.11 was analyzed in Example 7.3 using first-order circuit analysis techniques. Use the Laplace transform method to find $v_o(t)$ for $t$ ≥ 0+.

::: figure assets/circuit/nr12-ex13-2.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.2
:::

::: answer
The same description as Example 7.3 in the TR section, with FD chosen instead of TR — which is what the book does too, revisiting the circuit with the Laplace transform. The answers come back as transforms, functions of $s$ with the initial condition already inside them: `v_2` is the book's $V_o(s)$, one inverse transform away from the $60e^{-25t}$ it printed the first time. One circuit, two domains, nothing retyped.

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

Consider the circuit in Fig. 13.13, where the initial current in the inductor is 29 mA and the initial voltage across the capacitor is 50 V. This circuit was analyzed in Example 8.10 using second-order circuit analysis techniques. Use the Laplace transform method to find $v(t)$ for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex13-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.3
:::

::: answer
The book draws the $s$-domain circuit with three impedances in parallel and three current sources: the real one, and one each standing for the inductor's initial current and the capacitor's initial voltage. Here the initial conditions are the fifth fields of `c` and `l`, exactly as in TR, and the source is written as its own transform — the 24 mA step is `0.024/s`. The book's $V(s)$ is the voltage at node 1, which the book then inverts by hand into a damped response; choose TR instead and that inversion is done for you.

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

The circuit in Fig. 13.20 has no initial stored energy, and at $t$ = 0 the switch closes. Find the Thévenin equivalent for the circuit to the left of the terminals a and b in the s domain, using Laplace methods.

::: figure assets/circuit/nr12-ex13-6.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.6
:::

::: answer
The Thévenin tool works in the $s$ domain as well, so the equivalent comes back as a pair of rational functions of $s$ rather than a pair of numbers: `vth` is the transform of the open-circuit voltage and `z` the impedance. The source is written as the transform of its step, `480/s`. The book goes on to connect the capacitor to the equivalent and find its current; that second step is one more run, in TR, with the capacitor in place.

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

The voltage source $v_g$ drives the circuit shown in Fig. 13.31. The output signal is the voltage across the capacitor, $v_o$. a) Find the transfer function for this circuit. b) Calculate the numerical values for the poles and zeros of the transfer function.

::: figure assets/circuit/nr12-ex13-9.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.9
:::

::: answer
Nothing in the app is labelled *transfer function*, because nothing needs to be. Leave the source as the symbol `vg`, run FD, and the voltage at node 2 comes back as a function of $s$ with `vg` in it; dividing by `vg` is the transfer function, part (a). Part (b), the poles and zeros, are the roots of that expression's denominator and numerator: poles at $s = -3000 \pm j4000$ and a zero at $s = -5000$, the book's values.

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

a) Show that the RLC circuit in Fig. 14.22 is a bandpass filter by deriving an expression for the transfer function $H(s)$. b) Compute the centre frequency. c) Calculate the cutoff frequencies, the bandwidth and $Q$. d) Compute $R$ and $L$ for a centre frequency of 5 kHz and a bandwidth of 200 Hz, using a 5 µF capacitor.

::: figure assets/circuit/nr12-ex14-6.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 14.6
:::

::: answer
A filter is a circuit with a name, and nothing in the app is filter-shaped. Leave $R$, $L$ and $C$ as symbols, run FD, and the ratio of output to input is the standard bandpass form the book derives in part (a): a first-order numerator over a second-order denominator, from which the centre frequency $\omega_0 = 1/\sqrt{LC}$ and the bandwidth $\beta = 1/RC$ are read off. Parts (b) to (d) are then ordinary algebra on that expression; for a 5 kHz centre and a 200 Hz bandwidth with a 5 µF capacitor the book's design values are $R$ = 159.2 Ω and $L$ = 202.6 µH.

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
