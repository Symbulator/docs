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
We describe the circuit as it is drawn, naming the current source `j` and the resistors `r1` to `r7`, with the bottom rail as ground. Symbulator solves the whole circuit at once and both answers are among the results.

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

::: applink NR12's Example 3.7 (DC)
:::

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
A Wheatstone bridge measures a resistance nobody knows, $R_x$, by comparing it with resistances that are known. The adjustable resistor $R_3$ is turned until the galvanometer between the two arms of the bridge carries no current, and at that setting the unknown can be read off the others. So we describe the circuit with the two resistances the question leaves open as symbols rather than numbers, which we name `r3` for the adjustable one and `rx` for the unknown, after the book's $R_3$ and $R_x$; we name the two known resistors `r1` and `r2`, and call the two arms' midpoints **a** and **b**. We describe the galvanometer as a resistor, which we name `rg`; the figure gives it no value, and none is needed, because at balance no current flows through it, so we leave its resistance as a symbol as well. We leave the source as a symbol too, `vs`, since its value plays no part at balance. The balance condition itself, no current through the galvanometer, is not a value that can be typed into any element, so we give it to Symbulator as an equation in {{card:Expert Mode}}, `i_rg = 0`, and name `rx` as the unknown to solve for.

```field 9 Circuit Description
e,1,0,vs
r1,1,a,1'k
r2,1,b,4'k
rg,a,b,rg
r3,a,0,r3
rx,b,0,rx
```

::: applink NR12's Example 3.10 (DC, Expert Mode)
:::

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

`rx` is the book's $R_x$.

That formula answers the question. The bridge reads four times whatever {{var:R_3}} is set to, so with {{var:R_3}} at its lowest, 10 Ω, the bridge reads {{o:40}} Ω, and at its highest, 2 kΩ, it reads {{o:8}} kΩ: the range of resistances this bridge can measure is 40 Ω to 8 kΩ.

:::
:::

::: problem NR12's Example 3.11

Find the current and power supplied by the 40 V source in the circuit shown in Fig. 3.35.

::: figure assets/circuit/nr12-ex3-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 3.11
:::

::: answer
We write the bridge as it is drawn, naming the source `e` and the six resistors `r1` to `r6`, each between the two nodes it joins, with the source's lower end as ground; nothing has to be simplified first. One thing to know when reading the results: Symbulator reports the current through a source and the power it *consumes*, both counted into the source, whereas the question asks what the source *supplies*. The two differ only in sign, so the answers to the question are the negatives of `i_e` and `p_e`, which we type into {{card:Evaluate}} as `-i_e` and `-p_e`.

```field 9 Circuit Description
e,1,0,40
r1,1,2,5
r2,2,3,100
r3,2,4,125
r4,3,4,25
r5,3,0,40
r6,4,0,37.5
```

::: applink NR12's Example 3.11 (DC)
:::

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `-i_e` = {{o:0.5}} A and `-p_e` = {{o:20}} W.

:::
:::

::: problem NR12's Example 4.4

Use the node-voltage method to find the power dissipated in the 5 Ω resistor in the circuit shown in Fig. 4.10.

::: figure assets/circuit/nr12-ex4-4.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.4
:::

::: answer
The circuit has a dependent voltage source, whose value is eight times the current $i_\phi$ through the 5 Ω resistor. In Symbulator a dependent source needs no special element: it is a source whose value names another result. We name the 5 Ω resistor `r3`, so its current is `ir3`, and we write the dependent source as `e2` with the value `8*ir3`; we number the nodes 1 to 4 from the source rightward, with the bottom rail as ground. The power the question asks for is then the power consumed by `r3`.

```field 9 Circuit Description
e,1,0,20
r1,1,2,2
r2,2,0,20
r3,2,3,5
r4,3,0,10
r5,3,4,2
e2,4,0,8*ir3
```

::: applink NR12's Example 4.4 (DC)
:::

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `p_r3` = {{o:7.2}} W.

:::
:::

::: problem NR12's Example 4.7

Use the mesh-current method to find the power dissipated in the 4 Ω resistor in the circuit shown in Fig. 4.23.

::: figure assets/circuit/nr12-ex4-7.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.7
:::

::: answer
Again a dependent voltage source, this time worth fifteen times the current $i_\phi$ in the 20 Ω resistor. We name that resistor `r4`, so its current is `ir4` and we write the source as `e2` with the value `15*ir4`; the 4 Ω resistor whose power is asked for we name `r3`.

```field 9 Circuit Description
e,1,0,50
r1,1,3,1
r2,1,2,5
r3,2,3,4
r4,2,0,20
e2,3,0,15*ir4
```

::: applink NR12's Example 4.7 (DC)
:::

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `p_r3` = {{o:16}} W.

:::
:::

::: problem NR12's Example 4.8

Use the mesh-current method to find branch currents $i_a$, $i_b$ and $i_c$ in the circuit for Example 4.3, repeated here as Fig. 4.25.

::: figure assets/circuit/nr12-ex4-8.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.8
:::

::: answer
A voltage source, three resistors and a current source. We name them `e`, `r1` to `r3` and `j`, and take the bottom rail as ground. A current source is written like a voltage source — name, two nodes, value — and its current flows through it from the first node to the second, so we write the 3 A source, whose arrow points up from the bottom rail into node 2, as `j,0,2,3`. The three branch currents the question names are the currents through the three resistors, each counted in the direction of the figure's arrow, which is the order we write each resistor's nodes in.

```field 9 Circuit Description
e,1,0,50
r1,1,2,5
r2,2,0,10
r3,2,0,40
j,0,2,3
```

::: applink NR12's Example 4.8 (DC)
:::

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_r1` = {{o:2}} A (the book's $i_a$), `i_r2` = {{o:4}} A (the book's $i_b$) and `i_r3` = {{o:1}} A (the book's $i_c$).

:::
:::

::: problem NR12's Example 4.13

a) Use source transformations to find the voltage $v_o$ in the circuit shown in Fig. 4.42. b) Find the power developed by the 250 V voltage source. c) Find the power developed by the 8 A current source.

::: figure assets/circuit/nr12-ex4-13.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.13
:::

::: answer
We write every element as it stands in the figure, the 125 Ω across the source and the 10 Ω under the current source included, naming the resistors `r1` to `r6` from left to right. The current source's arrow points down, from node 2 towards the 10 Ω, so we write its nodes in that order, `j,2,9,8`, calling the node between the source and the resistor **9**. The *power developed* by a source is the power it supplies, and Symbulator reports the power each element consumes, so parts (b) and (c) are the negatives of `p_e` and `p_j`, which we type into {{card:Evaluate}} as `-p_e` and `-p_j`. The question's $v_o$ is the voltage across the 100 Ω, `r4`.

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

::: applink NR12's Example 4.13 (DC)
:::

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `v_r4` = {{o:20}} V (the book's $v_o$), `-p_e` = {{o:2800}} W and `-p_j` = {{o:480}} W.

:::
:::

::: problem NR12's Example 4.21

a) For the circuit shown in Fig. 4.65, find the value of $R_L$ that results in maximum power being transferred to $R_L$. b) Calculate the maximum power that can be delivered to $R_L$.

::: figure assets/circuit/nr12-ex4-21.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.21
:::

::: answer
The circuit to the left of $R_L$ is a source and two resistors. We describe those three and leave $R_L$ out, because the question is about what to connect at its terminals, and we call those terminals node **2** and ground. The {{card:Find equivalent}} card with *Thévenin / Norton* chosen and the two terminals named reduces the circuit to its Thévenin equivalent, and reports with it the load that would draw the most power from those terminals and how much that power is. By the maximum power theorem that load equals the Thévenin resistance, which the card reports as `z`; the power it reports as `pmax`.

```field 9 Circuit Description
e,1,0,360
r1,1,2,30
r2,2,0,150
```

::: applink NR12's Example 4.21 (Thévenin)
:::

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **2** and **0**.

Symbulator returns `z` = {{o:25}} Ω (the book's $R_L$) and `pmax` = {{o:900}} W (the book's $p_{max}$).

:::
:::

::: problem NR12's Example 4.23

Use the principle of superposition to find $v_o$ in the circuit shown in Fig. 4.71.

::: figure assets/circuit/nr12-ex4-23.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.23
:::

::: answer
Two independent sources and two dependent ones. We name the 5 Ω resistor `r1`, the 20 Ω `r2` and the 10 Ω `r3`. The dependent current source is worth $0.4v_\Delta$, and $v_\Delta$ is the voltage across the 10 Ω, so we write its value as `0.4*vr3`; the dependent voltage source is worth $2i_\Delta$, and $i_\Delta$ is the current through the 5 Ω, so we write its value as `2*ir1`. We write each source's nodes in the order its arrow or its polarity marks give, and we take the bottom-right node as ground. The question's $v_o$ is the voltage across the 20 Ω, `r2`.

```field 9 Circuit Description
e,1,c,10
r1,1,a,5
r2,a,c,20
r3,b,0,10
j1,0,b,5
j2,b,a,0.4*vr3
e2,0,c,2*ir1
```

::: applink NR12's Example 4.23 (DC)
:::

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `v_r2` = {{o:24}} V (the book's $v_o$).

:::
:::

::: problem NR12's Example 5.1

The op amp in the circuit shown in Fig. 5.7 is ideal. a) Calculate $v_o$ if $v_a$ = 1 V and $v_b$ = 0 V. b) Repeat (a) for $v_a$ = 1 V and $v_b$ = 2 V. c) If $v_a$ = 1.5 V, specify the range of $v_b$ that avoids amplifier saturation.

::: figure assets/circuit/nr12-ex5-1.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.1
:::

::: answer
An ideal op amp is the element `o`, whose three nodes are its non-inverting input, its inverting input and its output, in that order. We choose to write the circuit's two inputs as voltage sources with the symbolic values `va` and `vb` rather than the numbers in the question, so that a single run returns the output as a formula in both and each part can be read off it afterwards; we name those sources `ea` and `eb`, the two resistors `r1` and `r2`, and number the nodes from the $v_a$ input. Symbulator's ideal op amp has no supplies: it reports whatever output the inputs demand, so whether the amplifier is saturated is checked afterwards against the ±10 V supplies in the figure.

```field 9 Circuit Description
ea,1,0,va
r1,1,2,25'k
r2,2,3,100'k
eb,4,0,vb
o,4,2,3
```

::: applink NR12's Example 5.1 (DC)
:::

Set {{ui:Analysis}} to *DC — direct current*.

::: result voltage at node 3
v_{3} = - 4 va + 5 vb\,\mathrm{V}
:::

`v_3` is the book's $v_o$.

**a)** With {{var:v_a}} = 1 V and {{var:v_b}} = 0 V the formula gives {{var:v_o}} = 5(0) − 4(1) = {{o:-4}} V. That is inside the ±10 V supplies, so the op amp is in its linear region and −4 V is the answer.

**b)** With {{var:v_a}} = 1 V and {{var:v_b}} = 2 V, {{var:v_o}} = 5(2) − 4(1) = {{o:6}} V. Inside the supplies again, so the op amp is still linear.

**c)** With {{var:v_a}} = 1.5 V the formula becomes {{var:v_o}} = 5{{var:v_b}} − 6. The op amp stays linear while that lies between the rails: 5{{var:v_b}} − 6 = 10 gives {{var:v_b}} = {{o:3.2}} V, and 5{{var:v_b}} − 6 = −10 gives {{var:v_b}} = {{o:-0.8}} V, so the range is {{o:-0.8}} V ≤ {{var:v_b}} ≤ {{o:3.2}} V.

:::
:::

::: problem NR12's Example 5.3

a) Design a summing amplifier whose output voltage is $v_o = -4v_a - v_b - 5v_c$, using an ideal op amp with ±12 V power supplies and a 20 kΩ feedback resistor. b) Suppose $v_a$ = 2 V and $v_c$ = $-$1 V. What range of input voltages for $v_b$ allows the op amp to remain linear?

::: figure assets/circuit/nr12-ex5-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.3
:::

::: answer
The output of a summing amplifier with feedback resistor $R_f$ and input resistors $R_a$, $R_b$ and $R_c$ is $v_o = -(R_f/R_a)v_a - (R_f/R_b)v_b - (R_f/R_c)v_c$. The question fixes $R_f$ at 20 kΩ and asks for gains of 4, 1 and 5, so the input resistors are $R_a$ = 20/4 = 5 kΩ, $R_b$ = 20/1 = 20 kΩ and $R_c$ = 20/5 = 4 kΩ. That is the design, and the run is its check. We describe the circuit with those four resistors, naming them `r1`, `r2`, `r3` and `rf`; we write the three inputs as sources `ea`, `eb` and `ec` with the symbolic values `va`, `vb` and `vc`, so that the output comes back as a formula; and we write the op amp `o` with its non-inverting input at ground, its inverting input at a node we call **n**, and its output at node **4**.

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

::: applink NR12's Example 5.3 (DC)
:::

Set {{ui:Analysis}} to *DC — direct current*.

::: result voltage at node 4
v_{4} = - 4 va - vb - 5 vc\,\mathrm{V}
:::

`v_4` is the book's $v_o$.

**a)** The run returns exactly the formula the design was asked for, which is the check that the resistor values are right.

**b)** With {{var:v_a}} = 2 V and {{var:v_c}} = −1 V the formula becomes {{var:v_o}} = −4(2) − {{var:v_b}} − 5(−1) = −{{var:v_b}} − 3. The output reaches the −12 V rail when −{{var:v_b}} − 3 = −12, at {{var:v_b}} = {{o:9}} V, and the +12 V rail when −{{var:v_b}} − 3 = 12, at {{var:v_b}} = {{o:-15}} V. So the op amp stays linear for {{o:-15}} V ≤ {{var:v_b}} ≤ {{o:9}} V.

:::
:::

::: problem NR12's Example 5.3 part c

c) Suppose $v_a$ = 2 V, $v_b$ = 3 V and $v_c$ = $-$1 V. Using the input resistor values found in part (a), how large can the feedback resistor be before the op amp saturates?

::: figure assets/circuit/nr12-ex5-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.3
:::

::: answer
Part (c) keeps the input resistors found in part (a) but asks a different kind of question. The inputs are now the numbers 2 V, 3 V and −1 V, and the unknown is the feedback resistor. With these inputs the summing amplifier's output is negative, so the rail it can reach is −12 V, and the largest feedback resistor is the one that puts the output exactly there. In Symbulator that is a question for {{card:Expert Mode}}: we write the feedback resistor as the symbol `rf` instead of a number, we write the output at the rail as the equation `v_4 = -12`, and we name `rf` as the unknown to solve for.

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

::: applink NR12's Example 5.3 part c (DC, Expert Mode)
:::

```field 9 Add equation(s)
v_4 = -12
```

```field 9 Add unknown(s)
rf
```

Set {{ui:Analysis}} to *DC — direct current*. This one needs {{ui:Enable Expert Mode}} ticked in the {{card:Expert Mode}} box; the equations and unknowns go in the fields it reveals.

Symbulator returns `rf` = {{o:40000}} Ω (the book's $R_f$).

**c)** So the feedback resistor can be as large as {{o:40}} kΩ. Any larger and the output would have to go beyond −12 V, which it cannot: the op amp saturates.

:::
:::

::: problem NR12's Example 5.5

a) Design a difference amplifier that amplifies the difference between two input voltages by a gain of 8, using an ideal op amp and ±8 V power supplies. b) Suppose $v_a$ = 1 V. What range of $v_b$ keeps the op amp linear?

::: figure assets/circuit/nr12-ex5-5.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.5
:::

::: answer
A difference amplifier's output is $v_o = (R_b/R_a)(v_b - v_a)$, provided the four resistors satisfy $R_a/R_b = R_c/R_d$. A gain of 8 therefore needs $R_b$ eight times $R_a$ and $R_d$ eight times $R_c$; one choice, the book's, is $R_a$ = $R_c$ = 1.5 kΩ and $R_b$ = $R_d$ = 12 kΩ. We describe the circuit with those values, naming the resistors `ra` to `rd` after the book's, and we write the two inputs as sources with the symbolic values `va` and `vb`, so that the output comes back as a formula; the run checks the design.

```field 9 Circuit Description
ea,1,0,va
eb,2,0,vb
ra,1,n,1.5'k
rb,n,3,12'k
rc,2,p,1.5'k
rd,p,0,12'k
o,p,n,3
```

::: applink NR12's Example 5.5 (DC)
:::

Set {{ui:Analysis}} to *DC — direct current*.

::: result voltage at node 3
v_{3} = - 8 va + 8 vb\,\mathrm{V}
:::

`v_3` is the book's $v_o$.

**a)** The run returns exactly 8({{var:v_b}} − {{var:v_a}}), the gain the design was asked for.

**b)** With {{var:v_a}} = 1 V the output is {{var:v_o}} = 8{{var:v_b}} − 8, which reaches +8 V when 8{{var:v_b}} − 8 = 8, at {{var:v_b}} = {{o:2}} V, and −8 V when 8{{var:v_b}} − 8 = −8, at {{var:v_b}} = {{o:0}} V. So the op amp remains in its linear region for {{o:0}} V ≤ {{var:v_b}} ≤ {{o:2}} V.

:::
:::

::: problem NR12's Example 5.7

Analyze the noninverting amplifier of Example 5.4 using the realistic op amp model, with open-loop gain $A$ = 50,000, input resistance $R_i$ = 100 kΩ and output resistance $R_o$ = 7.5 kΩ; there is no load resistance at the output. Find the gain $v_o/v_g$.

::: figure assets/circuit/nr12-ex5-7.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.7
:::

::: answer
The realistic op amp in the figure is not the `o` element but three ordinary ones: the input resistance $R_i$ between the two inputs, the output resistance $R_o$ in series with the output, and a dependent voltage source whose value is the open-loop gain times the voltage between the inputs, $A(v_p - v_n)$. We call the two input nodes **p** and **n**, write the input resistance as `ri` between them, the output resistance as `ro`, and the dependent source as `ea` with the value `50000*(vp-vn)`. We leave the source as the symbol `vg`, so that the output voltage comes back as a multiple of `vg`; the gain asked for is that multiple, which we type into {{card:Evaluate}} as `v_3/vg`.

```field 9 Circuit Description
eg,1,0,vg
rg,1,p,1'k
ri,p,n,100'k
rs,n,0,2'k
rf,n,3,10'k
ro,4,3,7.5'k
ea,4,0,50000*(vp-vn)
```

::: applink NR12's Example 5.7 (DC)
:::

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `v_3/vg` = {{o:5.9988}} (the book's $v_o/v_g$).

:::
:::

::: problem NR12's Example 18.1

Find the z parameters for the circuit shown in Fig. 18.3.

::: figure assets/circuit/nr12-ex18-1.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 18.1
:::

::: answer
A two-port is a circuit seen from two pairs of terminals, and its z parameters are the four numbers that relate the two voltages to the two currents at those pairs. We take port 1 as node **1** with ground and port 2 as node **2** with ground, write the three resistors between those nodes, naming each after its value, and name the two ports to the {{card:Find equivalent}} card with *Two-port parameters* chosen and the kind set to **z**; it returns the four parameters, named `z11` to `z22`.

```field 9 Circuit Description
r5,1,2,5
r20,1,0,20
r15,2,0,15
```

::: applink NR12's Example 18.1 (z parameters)
:::

Open {{card:Find equivalent}}, choose *Two-port parameters*, kind **z**, with the ports at **1** and **2**.

Symbulator returns `z11` = {{o:10}} Ω (the book's $z_{11}$), `z12` = {{o:7.5}} Ω (the book's $z_{12}$), `z21` = {{o:7.5}} Ω (the book's $z_{21}$) and `z22` = {{o:9.375}} Ω (the book's $z_{22}$).

:::
:::

::: problem NR12's Example 18.6

Two identical amplifiers are connected in cascade. Each is described by its h parameters: $h_{11}$ = 1000 Ω, $h_{12}$ = 0.0015, $h_{21}$ = 100, $h_{22}$ = 100 µS. The source has 500 Ω of internal resistance and the load is 10 kΩ. Find the voltage gain $V_2/V_g$.

::: figure assets/circuit/nr12-ex18-6.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 18.6
:::

::: answer
A two-port that is known only by its parameters is an element of its own. Since these are h parameters we use the element `h`, and write the four values after the two nodes as a bracketed term, `[1000,0.0015,100,0.0001]`, the 100 µS written as 0.0001. We write the two amplifiers in cascade as two such lines, `h1` and `h2`, sharing a node we call **b**, between the source's 500 Ω and the 10 kΩ load; we leave the source as the symbol `vg`, so that the output comes back as a multiple of it, and the gain asked for is that multiple, which we type into {{card:Evaluate}} as `v_c/vg`.

```field 9 Circuit Description
e,1,0,vg
rs,1,a,500
h1,a,b,[1000,0.0015,100,0.0001]
h2,b,c,[1000,0.0015,100,0.0001]
rl,c,0,10'k
```

::: applink NR12's Example 18.6 (DC)
:::

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `v_c/vg` = {{o:33333.3}} (the book's $V_2/V_g$).

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
There are two intervals. Before $t$ = 0 the switch has been closed for a long time, so any transient has died away and every current is steady; in a steady circuit an inductor carries its current with no voltage across it, which is to say it behaves as a wire. So we describe the circuit as it stands before the switch opens — the 20 A source, the 0.1 Ω resistor, the inductor and the three resistors beyond it — and run it in DC to find the inductor's current. We name the source `j`, the inductor `l` and the resistors `r0` to `r3`, and we write the inductor with no fifth field, since nothing about its past is being told:

```field 9 Circuit Description
j,0,1,20
r0,1,0,0.1
l,1,0,2
r1,1,2,2
r2,2,0,10
r3,2,0,40
```

::: applink NR12's Example 7.1 (DC, before the switch opens)
:::

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_l` = {{o:20}} A (the book's $i_L(0)$).

Opening the switch disconnects the source and the 0.1 Ω resistor, and leaves the inductor to release its energy through the three resistors. That is the circuit for the second interval, $t$ ≥ 0, and we describe it with the same names, dropping `j` and `r0`. The inductor now starts with the 20 A just found, which we write into its line as a fifth field, after the inductance. We set the analysis to TR, and the answers come back as functions of $t$.

```field 9 Circuit Description
l,1,0,2,20
r1,1,2,2
r2,2,0,10
r3,2,0,40
```

::: applink NR12's Example 7.1 (TR)
:::

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

Here `i_l` is the book's $i_L$, `i_r3` is the book's $i_o$ and `v_2` is the book's $v_o$.

:::
:::

::: problem NR12's Example 7.3

The switch in the circuit shown in Fig. 7.15 has been in position x for a long time. At $t$ = 0 it moves instantaneously to position y. Find a) $v_C(t)$ for $t$ ≥ 0, b) $v_o(t)$ for $t$ ≥ 0+, and c) $i_o(t)$ for $t$ ≥ 0+.

::: figure assets/circuit/nr12-ex7-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.3
:::

::: answer
Two intervals again. At position x the capacitor has been connected to the 100 V source through the 10 kΩ resistor for a long time, and a capacitor in a steady circuit carries no current, so nothing flows in the 10 kΩ and the capacitor sits at the voltage of the source. We describe that circuit — the source, the 10 kΩ, which we name `r0`, and the capacitor, written without a fifth field — and run it in DC to find the capacitor's voltage:

```field 9 Circuit Description
e,1,0,100
r0,1,2,10'k
c,2,0,0.5'u
```

::: applink NR12's Example 7.3 (DC, before the switch moves)
:::

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `v_2` = {{o:100}} V (the book's $v_C(0)$).

At position y the capacitor is connected instead to the 32 kΩ resistor and the two beyond it, and discharges through them. We describe that second circuit with the 100 V just found as the capacitor's fifth field, naming the three resistors `r1` to `r3` and the capacitor's node **1**, and set the analysis to TR.

```field 9 Circuit Description
c,1,0,0.5'u,100
r1,1,2,32'k
r2,2,0,240'k
r3,2,0,60'k
```

::: applink NR12's Example 7.3 (TR)
:::

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

Here `v_1` is the book's $v_C$, `v_2` is the book's $v_o$ and `i_r3` is the book's $i_o$.

:::
:::

::: problem NR12's Example 7.5

The switch in the circuit shown in Fig. 7.21 has been in position a for a long time. At $t$ = 0 it moves from position a to position b. The switch is a make-before-break type, so the inductor current is continuous. a) Find the expression for $i(t)$ for $t$ ≥ 0. b) What is the initial voltage across the inductor just after the switch has been moved to position b?

::: figure assets/circuit/nr12-ex7-5.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.5
:::

::: answer
With the switch at position a, the inductor has been in parallel with the 10 Ω resistor and the 8 A source for a long time. In that steady state the inductor is a wire, so the whole 8 A flows through it and none through the resistor. The direction matters: the source's arrow points down through the source, so its current comes up through the inductor, against the book's arrow for $i$. We write the source as `j,1,0,8`, its current flowing from node 1 down to ground, and the inductor as `l,1,0,0.2`, so that its current is counted downward like the book's $i$; a DC run then gives the current with its sign:

```field 9 Circuit Description
j,1,0,8
r,1,0,10
l,1,0,0.2
```

::: applink NR12's Example 7.5 (DC, at position a)
:::

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_l` = {{o:-8}} A (the book's $i(0)$).

Moving the switch to b connects the inductor, through the 2 Ω resistor, to the 24 V source instead. Because the switch is make-before-break, the inductor's current does not jump at the switching: it starts at the −8 A just found. We describe the second circuit with that −8 as the inductor's fifth field, sign included, naming the source `e` and the resistor `r1`, and set the analysis to TR.

```field 9 Circuit Description
e,1,0,24
r1,1,2,2
l,2,0,0.2,-8
```

::: applink NR12's Example 7.5 (TR)
:::

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through l
i_{l} = 12 - 20 e^{- 10 t}\,\mathrm{A}
:::

`i_l` is the book's $i$.

Part (b) asks for the voltage across the inductor the instant after the switch has moved. The inductor is between node 2 and ground, so its voltage is `v_2`, and we read its value at $t$ = 0 with {{card:Evaluate}}:

```field 9 Evaluate
v_2
```

```field 9 Conditions
t = 0
```

It gives {{o:40}} V (the book's $v(0^+)$).

:::
:::

::: problem NR12's Example 7.10

There is no energy stored in the circuit in Fig. 7.37 at the time the switch is closed. Find the solutions for $i_o$, $v_o$, $i_1$ and $i_2$.

::: figure assets/circuit/nr12-ex7-10.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.10
:::

::: answer
Two coils wound on one core, both fed from the same node. We write each coil as an inductor line of its own, `l1` and `l2`, and the coupling between them as the `m` line, which names the two coils and their mutual inductance, 6 H. No energy is stored, so we write neither inductor with a fifth field. The switch closing at $t$ = 0 needs no element: in TR a source with a plain numerical value is a step that begins at $t$ = 0, which is exactly what closing the switch on the 120 V source does. We name the source `e` and the resistor `r1`, and set the analysis to TR.

```field 9 Circuit Description
e,1,0,120
r1,1,2,7.5
l1,2,0,3
l2,2,0,15
m,l1,l2,6
```

::: applink NR12's Example 7.10 (TR)
:::

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

Here `i_r1` is the book's $i_o$, `v_2` is the book's $v_o$, `i_l1` is the book's $i_1$ and `i_l2` is the book's $i_2$.

:::
:::

::: problem NR12's Example 7.11 to 35 ms

The two switches in the circuit shown in Fig. 7.39 have been closed for a long time. At $t$ = 0 switch 1 is opened; then, 35 ms later, switch 2 is opened. a) Find $i_L(t)$ for 0 ≤ $t$ ≤ 35 ms.

::: figure assets/circuit/nr12-ex7-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.11
:::

::: answer
Three intervals this time, and three runs. In the first, both switches have been closed for a long time, the circuit is steady, and the inductor is a wire in parallel with the 18 Ω resistor. We describe the whole circuit — the 60 V source, the 4 Ω, 12 Ω, 6 Ω and 3 Ω resistors, the inductor and the 18 Ω — naming each resistor after its value, and run it in DC for the inductor's current:

```field 9 Circuit Description
e,1,0,60
r4,1,2,4
r12,2,0,12
r6,2,0,6
r3,2,3,3
l,3,0,0.15
r18,3,0,18
```

::: applink NR12's Example 7.11 to 35 ms (DC, both switches closed)
:::

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_l` = {{o:6}} A (the book's $i_L(0)$).

In the second interval switch 1 has opened, which disconnects the 60 V source and the 4 Ω and 12 Ω resistors. We describe what remains — the 6 Ω, the 3 Ω, the inductor and the 18 Ω, with the same names — and give the inductor the 6 A just found as its fifth field. We set the analysis to TR.

```field 9 Circuit Description
r6,2,0,6
r3,2,3,3
l,3,0,0.15,6
r18,3,0,18
```

::: applink NR12's Example 7.11 to 35 ms (TR)
:::

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through l
i_{l} = 6 e^{- 40 t}\,\mathrm{A}
:::

`i_l` is the book's $i_L$.

This run holds until switch 2 opens at 35 ms, and the inductor's current at that instant is where the third interval starts. We read it from the answer with {{card:Evaluate}}, giving the instant in seconds:

```field 9 Evaluate
i_l
```

```field 9 Conditions
t = 0.035
```

It gives {{o:1.47958}} A (the book's $i_L(35\,\mathrm{ms})$).

:::
:::

::: problem NR12's Example 7.11 after 35 ms

b) Find $i_L(t)$ for $t$ ≥ 35 ms. (Time is measured from the second switching.)

::: figure assets/circuit/nr12-ex7-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.11
:::

::: answer
In the third interval switch 2 has opened too, removing the 18 Ω resistor, so the inductor now discharges through the 3 Ω and 6 Ω alone. We describe that circuit with the 18 Ω dropped, and give the inductor as its fifth field the current found at the end of the previous entry, $6e^{-40 \times 0.035} = 6e^{-1.4}$, about 1.48 A; we write it as the expression `6*exp(-1.4)`, which is exact. We measure time from the second switching, as the book does, so this run's $t$ = 0 is the instant switch 2 opens. The analysis is TR.

```field 9 Circuit Description
r6,2,0,6
r3,2,3,3
l,3,0,0.15,6*exp(-1.4)
```

::: applink NR12's Example 7.11 after 35 ms (TR)
:::

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through l
i_{l} = 1.47958 e^{- 60 t}\,\mathrm{A}
:::

`i_l` is the book's $i_L$.

:::
:::

::: problem NR12's Example 7.13

a) When the switch is closed in the circuit shown in Fig. 7.45, the voltage on the capacitor is 10 V. Find the expression for $v_o$ for $t$ ≥ 0. b) Assume that the capacitor short-circuits when its terminal voltage reaches 150 V. How many milliseconds elapse before the capacitor short-circuits?

::: figure assets/circuit/nr12-ex7-13.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.13
:::

::: answer
The capacitor's 10 V is given in the question, and we write it into the capacitor's fifth field. The dependent current source is worth seven times the current $i_\Delta$ in the 20 kΩ resistor; we name that resistor `r2`, so the source's value is `7*ir2`, and since its arrow points up into node 1 we write it as `j,0,1,7*ir2`. We set the analysis to TR.

```field 9 Circuit Description
c,1,0,5'u,10
r1,1,0,10'k
r2,1,0,20'k
j,0,1,7*ir2
```

::: applink NR12's Example 7.13 (TR)
:::

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result voltage at node 1
v_{1} = 10 e^{40 t}\,\mathrm{V}
:::

`v_1` is the book's $v_o$.

The exponent is positive, so the voltage grows instead of decaying: the dependent source feeds the capacitor faster than the resistors drain it. Part (b) is read off the answer: $10e^{40t}$ = 150 when $e^{40t}$ = 15, that is when $t = (\ln 15)/40$ = {{o:0.0677}} s, so the capacitor short-circuits after {{o:67.7}} ms.

:::
:::

::: problem NR12's Example 8.2

For the circuit in Fig. 8.6, $v(0^+)$ = 12 V and $i_L(0^+)$ = 30 mA. Find the expression for $v(t)$. (Example 8.3 asks the same circuit for its three branch currents.)

::: figure assets/circuit/nr12-ex8-2.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.2
:::

::: answer
A capacitor, an inductor and a resistor in parallel. We write each as a line between node 1 and ground, naming them `c`, `l` and `r`, and put the two initial conditions the question gives in the fifth fields: 12 V on the capacitor and 30 mA, written 0.03, on the inductor. There is no source; the run is the circuit releasing the energy it holds. We set the analysis to TR.

```field 9 Circuit Description
c,1,0,0.2'u,12
l,1,0,50'm,0.03
r,1,0,200
```

::: applink NR12's Example 8.2 (TR)
:::

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

Here `v_1` is the book's $v$, `i_r` is the book's $i_R$ and `i_l` is the book's $i_L$.

:::
:::

::: problem NR12's Example 8.4

In the circuit shown in Fig. 8.8, $V_0$ = 0 and $I_0$ = $-$12.25 mA. Calculate the voltage response for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex8-4.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.4
:::

::: answer
The same three elements in parallel, and we describe them the same way. $V_0$ = 0 goes in the capacitor's fifth field and $I_0$ = −12.25 mA in the inductor's, written −0.01225 with the sign the question gives it. We set the analysis to TR.

```field 9 Circuit Description
c,1,0,125'n,0
l,1,0,8,-0.01225
r,1,0,20'k
```

::: applink NR12's Example 8.4 (TR)
:::

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result voltage at node 1
v_{1} = 100.021 e^{- 200 t} \sin{\left(979.796 t \right)}\,\mathrm{V}
:::

`v_1` is the book's $v$.

The book prints the amplitude as 100 and the frequency of the sine as 979.80, both rounded; at six digits the run shows 100.021 and 979.796 for the same expression.

:::
:::

::: problem NR12's Example 8.11

The 0.1 µF capacitor in the circuit shown in Fig. 8.17 is charged to 100 V. At $t$ = 0 the capacitor is discharged through a series combination of a 100 mH inductor and a 560 Ω resistor. a) Find $i(t)$ for $t$ ≥ 0. b) Find $v_C(t)$ for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex8-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.11
:::

::: answer
We write the charged capacitor as the capacitor line with 100 V as its fifth field, and the inductor and the resistor after it round the loop, naming the three `c`, `l` and `r`. We write the inductor's nodes as 2 then 1 on purpose, so that its current is counted in the direction of the book's arrow for $i$; written the other way round the answer would come back with its sign reversed. The capacitor's voltage $v_C$ is then the voltage at node 1. We set the analysis to TR.

```field 9 Circuit Description
c,1,0,0.1'u,100
l,2,1,0.1
r,2,0,560
```

::: applink NR12's Example 8.11 (TR)
:::

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through l
i_{l} = - 0.104167 e^{- 2800 t} \sin{\left(9600 t \right)}\,\mathrm{A}
:::

::: result voltage at node 1
v_{1} = \left(29.1667 \sin{\left(9600 t \right)} + 100 \cos{\left(9600 t \right)}\right) e^{- 2800 t}\,\mathrm{V}
:::

Here `i_l` is the book's $i$ and `v_1` is the book's $v_C$.

:::
:::

::: problem NR12's Example 8.12

No energy is stored in the 100 mH inductor or the 0.4 µF capacitor when the switch in the circuit shown in Fig. 8.18 is closed. Find $v_C(t)$ for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex8-12.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.12
:::

::: answer
A single loop: the 48 V source, which in TR is a step beginning at $t$ = 0 and so stands for the switch closing, then the inductor, the resistor and the capacitor. We write them in that order, numbering the nodes 1 to 3 round the loop; neither the inductor nor the capacitor stores energy, so we write both without a fifth field. $v_C$ is then the voltage at node 3, the capacitor's upper end. We set the analysis to TR.

```field 9 Circuit Description
e,1,0,48
l,1,2,0.1
r,2,3,1250
c,3,0,0.4'u
```

::: applink NR12's Example 8.12 (TR)
:::

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result voltage at node 3
v_{3} = 48 - 64 e^{- 2500 t} + 16 e^{- 10000 t}\,\mathrm{V}
:::

`v_3` is the book's $v_C$.

:::
:::

::: problem NR12's Example 13.5

The circuit in Fig. 13.17 has no initial stored energy. At $t$ = 0 the switch closes. Use Laplace methods to find $i_1(t)$ and $i_2(t)$ for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex13-5.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.5
:::

::: answer
No energy is stored, so we write the two inductors without fifth fields, and the switch closing at $t$ = 0 onto the 336 V source needs no element of its own: in TR a numerical source value is a step that begins at $t$ = 0. We name the inductors `l1` and `l2` after the book's $i_1$ and $i_2$, which are the currents through them, and the resistors `r1` and `r2`. The question comes from the book's Laplace chapter, but we set the analysis to TR, which returns the two currents as functions of $t$; the transform and its inversion happen inside the solver.

```field 9 Circuit Description
e,1,0,336
l1,1,2,8.4
r1,2,0,42
l2,2,3,10
r2,3,0,48
```

::: applink NR12's Example 13.5 (TR)
:::

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through l1
i_{l1} = 15 - 14 e^{- 2 t} - e^{- 12 t}\,\mathrm{A}
:::

::: result current through l2
i_{l2} = 7 - 8.4 e^{- 2 t} + 1.4 e^{- 12 t}\,\mathrm{A}
:::

Here `i_l1` is the book's $i_1$ and `i_l2` is the book's $i_2$.

:::
:::

::: problem NR12's Example 13.7

The make-before-break switch in the circuit in Fig. 13.23 has been in position a for a long time. At $t$ = 0 it moves instantaneously to position b. Use Laplace methods to find $i_2(t)$ for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex13-7.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.7
:::

::: answer
Two intervals. With the switch at position a the primary side has been steady for a long time: the 60 V source drives a constant current through the 9 Ω, the 3 Ω and the 2 H coil, which in a steady circuit is a wire. The secondary has no source of its own, and a constant current in the primary induces nothing in it, so its current is zero. We describe the whole circuit, naming the resistors after their values, `r9`, `r3`, `r2b` and `r10`, the coils `l1` and `l2`, and the coupling as the `m` line with their mutual inductance, 2 H; we call the secondary's nodes **q**, **c** and **d**. A DC run gives both currents; it also notes that the secondary has no path to ground, which is true of the figure and changes nothing:

```field 9 Circuit Description
e,1,0,60
r9,1,a,9
r3,a,p,3
l1,p,0,2
m,l1,l2,2
l2,q,d,8
r2b,q,c,2
r10,c,d,10
```

::: applink NR12's Example 13.7 (DC, at position a)
:::

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_l1` = {{o:5}} A (the book's $i_1(0)$) and `i_l2` = {{o:0}} A (the book's $i_2(0)$).

At $t$ = 0 the switch moves to b, which takes the source and the 9 Ω out and closes the primary on the 3 Ω alone. We describe that circuit with the same names and the two currents just found as the coils' fifth fields, 5 and 0. The secondary is still not connected to ground, so its bottom is simply the node we called **d**, and Symbulator again notes that it measures that side's voltages against **d**; the currents are unaffected. We set the analysis to TR, and $i_2$ is the current through `l2`.

```field 9 Circuit Description
r3,0,p,3
l1,p,0,2,5
m,l1,l2,2
l2,q,d,8,0
r2b,q,c,2
r10,c,d,10
```

::: applink NR12's Example 13.7 (TR)
:::

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through l2
i_{l2} = \frac{\left(5 e^{2 t} - 5\right) e^{- 3 t}}{4}\,\mathrm{A}
:::

`i_l2` is the book's $i_2$.

:::
:::

::: problem NR12's Example 13.13

The switch in the circuit shown in Fig. 13.50 has been closed for a long time. At $t$ = 0 it opens. Use Laplace methods to find the output voltage $v_o$ and the current in the 3 H inductor, $i_1$.

::: figure assets/circuit/nr12-ex13-13.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.13
:::

::: answer
Two intervals. While the switch is closed it is a wire from the junction after $L_1$ down to the bottom rail, so the circuit that has been steady for a long time is the 100 V source, the 10 Ω and $L_1$ in a loop through that wire, with the 15 Ω and $L_2$ hanging across a short circuit and carrying nothing. We describe that circuit and run it in DC for the two inductor currents; we write the closed switch by giving both its ends the same node, ground, and name the inductors `l1` and `l2` after the book's $L_1$ and $L_2$:

```field 9 Circuit Description
e,1,0,100
r1,1,2,10
l1,2,0,3
r2,0,4,15
l2,4,0,2
```

::: applink NR12's Example 13.13 (DC, switch closed)
:::

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_l1` = {{o:10}} A (the book's $i_1(0)$) and `i_l2` = {{o:0}} A (the book's $i_2(0)$).

Opening the switch removes that wire, so the two inductors are now in series with the 15 Ω between them. We describe that circuit with the 10 A and 0 just found as their fifth fields, numbering the nodes 1 to 4 from the source. The output voltage $v_o$ is then the voltage at node 3, the top of the 15 Ω and $L_2$, and $i_1$ is the current through `l1`. We set the analysis to TR.

```field 9 Circuit Description
e,1,0,100
r1,1,2,10
l1,2,3,3,10
r2,3,4,15
l2,4,0,2,0
```

::: applink NR12's Example 13.13 (TR)
:::

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result voltage at node 3
v_{3} = 12 \delta\left(t\right) + 60 + 10 e^{- 5 t}\,\mathrm{V}
:::

::: result current through l1
i_{l1} = 4 + 2 e^{- 5 t}\,\mathrm{A}
:::

Here `v_3` is the book's $v_o$ and `i_l1` is the book's $i_1$.

The $\delta(t)$ in $v_o$ is an impulse. Opening the switch puts the two inductors in series, one carrying 10 A and the other none, and they must carry the same current from then on; an inductor's current cannot jump without an impulse of voltage across it, and the weight of this one, 12, is what it takes to bring $L_2$'s current from 0 to the 6 A the pair settle on.

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
The inductor and the capacitor are given as an inductance and a capacitance, and we write them as they are, `l,2,0,40'u` and `c,1,0,1'u`, putting the source's frequency, 200,000 rad/s, in the {{ui:ω — angular frequency}} box; the conversion to impedances is done inside the solver. We write the current source as `j,0,1,8`, its arrow pointing up into node 1, with its 8 A as the amplitude, which is what the book's phasors carry too, and we name the resistors `r1` and `r2`. We set the analysis to AC, and each answer is a phasor, printed both as a complex number and as an amplitude with an angle.

```field 9 Circuit Description
j,0,1,8
r1,1,0,10
r2,1,2,6
l,2,0,40'u
c,1,0,1'u
```

::: applink NR12's Example 9.9 (AC)
:::

Set {{ui:Analysis}} to *AC — alternating current*. Put **200000** in the {{ui:ω — angular frequency}} box.

Symbulator returns `v_1` = {{o:32 - 24j}} V ({{o:40.00}}∠{{o:-36.87}}°, the book's $V$) and `i_r2` = {{o:-4j}} A ({{o:4.000}}∠{{o:-90.00}}°, the book's $I$).

Part (b) asks for the admittance the source sees. Symbulator reports the impedance seen by each source, here `z_j`, and an admittance is the reciprocal of an impedance, so we type into {{card:Evaluate}}:

```field 9 Evaluate
1/z_j
```

It gives {{o:0.16 + 0.12j}} S (the book's $Y$).

Part (e) is the two phasors written back as functions of time at the source's frequency: $v$ = 40 cos(200,000$t$ − 36.87°) V and $i$ = 4 cos(200,000$t$ − 90°) A.

:::
:::

::: problem NR12's Example 9.10

Use a delta-to-wye impedance transformation to find $I_0$, $I_1$, $I_2$, $I_3$, $I_4$, $I_5$, $V_1$ and $V_2$ in the circuit in Fig. 9.23.

::: figure assets/circuit/nr12-ex9-10.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.10
:::

::: answer
Every impedance in this circuit is given in ohms, some purely reactive and some complex. We write each exactly as given — `-4j`, `63.2+2.4j`, `20+60j` — as a resistor with a complex value, naming the five `r1` to `r5` in the order of the book's $I_1$ to $I_5$, and we write each one's nodes in the direction of the figure's arrow, so that its current is counted as the book counts it. Nothing depends on the frequency, so we leave **omega** as a symbol in the {{ui:ω — angular frequency}} box. We keep the figure's letters for the nodes, with **d** as ground, so $V_1$ and $V_2$ are the voltages at **b** and **c**. The source current $I_0$ leaves the source's positive terminal, which is the opposite of how Symbulator counts a source's current, so it is `-i_e`, which we type into {{card:Evaluate}}. We set the analysis to AC.

```field 9 Circuit Description
e,a,0,120
r1,a,b,-4j
r2,a,c,63.2+2.4j
r3,b,c,10
r4,b,0,20+60j
r5,c,0,-20j
```

::: applink NR12's Example 9.10 (AC)
:::

Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box; nothing here depends on the frequency.

Symbulator returns `-i_e` = {{o:2.4 + 3.2j}} A ({{o:4.000}}∠{{o:53.13}}°, the book's $I_0$), `i_r1` = {{o:2 + 2.66667j}} A ({{o:3.333}}∠{{o:53.13}}°, the book's $I_1$), `i_r2` = {{o:0.4 + 0.533333j}} A ({{o:0.6667}}∠{{o:53.13}}°, the book's $I_2$), `i_r3` = {{o:1.33333 + 4.26667j}} A ({{o:4.470}}∠{{o:72.65}}°, the book's $I_3$), `i_r4` = {{o:0.666667 - 1.6j}} A ({{o:1.733}}∠{{o:-67.38}}°, the book's $I_4$), `i_r5` = {{o:1.73333 + 4.8j}} A ({{o:5.103}}∠{{o:70.14}}°, the book's $I_5$), `v_b` = {{o:109.333 + 8j}} V ({{o:109.6}}∠{{o:4.185}}°, the book's $V_1$) and `v_c` = {{o:96 - 34.6667j}} V ({{o:102.1}}∠{{o:-19.86}}°, the book's $V_2$).

:::
:::

::: problem NR12's Example 9.12

Find the Thévenin equivalent circuit with respect to terminals a,b for the circuit shown in Fig. 9.32.

::: figure assets/circuit/nr12-ex9-12.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.12
:::

::: answer
The dependent voltage source is worth ten times $V_x$, the voltage across the 60 Ω resistor. We name that resistor `r2` and place it between node 2 and ground, so that $V_x$ is the voltage at node 2 and we can write the source's value as `10*v2`. We call the question's terminals a and b nodes **9** and **0**, and name them to the {{card:Find equivalent}} card with *Thévenin / Norton* chosen, which returns the equivalent's voltage and impedance; a dependent source in the circuit is no obstacle to it. The impedances are in ohms and nothing depends on the frequency, so we leave **omega** as a symbol. We set the analysis to AC.

```field 9 Circuit Description
e,1,0,120
r1,1,2,12
r2,2,0,60
r3,2,9,-40j
e2,3,0,10*v2
r4,3,9,120
```

::: applink NR12's Example 9.12 (Thévenin)
:::

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **9** and **0**. Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box; nothing here depends on the frequency.

Symbulator returns `vth` = {{o:784 - 288j}} V ({{o:835.2}}∠{{o:-20.17}}°, the book's $V_{Th}$) and `z` = {{o:91.2 - 38.4j}} Ω ({{o:98.95}}∠{{o:-22.83}}°, the book's $Z_{Th}$).

:::
:::

::: problem NR12's Example 9.14

Use the mesh-current method to find the voltages $V_1$, $V_2$ and $V_3$ in the circuit shown in Fig. 9.39.

::: figure assets/circuit/nr12-ex9-14.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.14
:::

::: answer
The dependent source is worth 39 times $I_x$, the current down through the middle branch, the 12 Ω and −{{var:j_16}} Ω in series. We name the 12 Ω `r3`, so its current is `ir3` and we write the source's value as `39*ir3`; we name the other impedances `r1` to `r6`, and call the top of the middle branch node **a**, the far side of the −{{var:j_16}} Ω node **c** and the dependent source's top node **b**. The three voltages asked for are marked across three parts of the circuit in the figure: $V_1$ across the 1 Ω and {{var:j_2}} Ω on the left, which is the difference between the voltages at node 1 and node **a**; $V_2$ across the middle branch, which is the voltage at node **a** itself; and $V_3$ across the 1 Ω and {{var:j_3}} Ω on the right, the difference between nodes **a** and **b**. We type the two differences into {{card:Evaluate}} as `v_1 - v_a` and `v_a - v_b`. Nothing depends on the frequency, so we leave **omega** as a symbol; we set the analysis to AC.

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

::: applink NR12's Example 9.14 (AC)
:::

Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box; nothing here depends on the frequency.

Symbulator returns `v_1 - v_a` = {{o:78 - 104j}} V ({{o:130.0}}∠{{o:-53.13}}°, the book's $V_1$), `v_a` = {{o:72 + 104j}} V ({{o:126.5}}∠{{o:55.30}}°, the book's $V_2$) and `v_a - v_b` = {{o:150 - 130j}} V ({{o:198.5}}∠{{o:-40.91}}°, the book's $V_3$).

:::
:::

::: problem NR12's Example 9.15

A linear transformer has $R_1$ = 200 Ω, $R_2$ = 100 Ω, $L_1$ = 9 H, $L_2$ = 4 H and $k$ = 0.5, and couples a load of an 800 Ω resistor in series with a 1 µF capacitor to a 300 V (rms) source of internal impedance $500 + j100$ Ω at 400 rad/s. g) Calculate the Thévenin equivalent with respect to the terminals of the load impedance.

::: figure assets/circuit/nr12-ex9-15.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.15
:::

::: answer
The transformer's two coils are given as inductances, and the frequency is given, so we work out their impedances first: $j\omega L_1$ = $j$400 × 9 = $j$3600 Ω and $j\omega L_2$ = $j$400 × 4 = $j$1600 Ω. The coupling is set by $k$: the mutual inductance is $M = k\sqrt{L_1 L_2}$ = 0.5 × 6 = 3 H, so $j\omega M$ = $j$1200 Ω. We then write each coil as an impedance, `r4` and `r5`, and the coupling between them as the `m` line naming the two and their mutual impedance, `m,r4,r5,1200j`; we name the winding resistances $R_1$ and $R_2$ `r3` and `r6`, and the source's internal impedance `r1` and `r2`. We leave the load out, because the question asks for the equivalent seen from its terminals, which we call nodes **c** and **d** and name to the {{card:Find equivalent}} card with *Thévenin / Norton* chosen. Two things about the secondary side. It is not connected to ground anywhere — nothing conducts between the two windings — so its bottom is simply the node we have called **d**, and Symbulator says in a note that it has measured that side's voltages against **d**; the currents, the voltage differences and the equivalent are unaffected. And the source is given in rms, so we tick {{ui:RMS phasors}} in {{card:Settings}}. Every value is in ohms already, so we leave **omega** as a symbol; we set the analysis to AC.

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

::: applink NR12's Example 9.15 (Thévenin)
:::

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **c** and **d**. Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box; nothing here depends on the frequency. Tick {{ui:RMS phasors}} in {{card:Settings}}, since the book's source is given in rms.

Symbulator returns `vth` = {{o:93.9351 + 17.7715j}} V ({{o:95.60}}∠{{o:10.71}}°, the book's $V_{Th}$) and `z` = {{o:171.086 + 1224.26j}} Ω ({{o:1236}}∠{{o:82.04}}°, the book's $Z_{Th}$).

:::
:::

::: problem NR12's Example 10.8

a) Calculate the total average and reactive power delivered to each impedance in the circuit shown in Fig. 10.18. b) Calculate the average and reactive powers associated with each source. c) Verify that the average power delivered equals the average power absorbed, and likewise for the reactive power.

::: figure assets/circuit/nr12-ex10-8.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 10.8
:::

::: answer
The circuit of Example 9.14, which we describe the same way, asked a different question. Symbulator reports every element's complex power as `s_` followed by the element's name: its real part is the average power and its imaginary part the reactive power, so parts (a) and (b) are all read from one run. Each impedance in the figure is two elements in our description, a resistor and a reactance in series, so the power delivered to the impedance is the sum of their two `s` answers, which we type into {{card:Evaluate}} as `s_r1 + s_r2`. The balance of part (c) is the sum of all eight, typed the same way. Nothing depends on the frequency, so we leave **omega** as a symbol; we set the analysis to AC.

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

::: applink NR12's Example 10.8 (AC)
:::

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
An ideal transformer is the element `t`. Its primary and secondary here share a node, so we write each winding as a bracketed pair of terminals, `[p,x]` for the primary and `[x,a]` for the secondary, followed by the turns ratio `[4,1]`; we name the two resistors after their values, `r60` and `r20`. We leave the load $R_L$ out of the description and name its terminals, node **a** and ground, to the {{card:Find equivalent}} card with *Thévenin / Norton* chosen, which reports the load that would draw the most average power from those terminals and how much. By the maximum power theorem that load is the Thévenin impedance, reported as `z`, and the power is `pmax`. The source is given as 840 V rms, so we tick {{ui:RMS phasors}} in {{card:Settings}}; there is no reactance anywhere, so we leave **omega** as a symbol. We set the analysis to AC.

```field 9 Circuit Description
e,1,0,840
r60,1,p,60
t,[p,x],[x,a],[4,1]
r20,x,0,20
```

::: applink NR12's Example 10.12 (Thévenin)
:::

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **a** and **0**. Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box; nothing here depends on the frequency. Tick {{ui:RMS phasors}} in {{card:Settings}}, since the book's source is given in rms.

Symbulator returns `z` = {{o:35}} Ω (the book's $R_L$) and `pmax` = {{o:315}} W (the book's $p_{max}$).

:::
:::

::: problem NR12's Example 11.1

A balanced, positive-sequence Y-connected generator with an internal impedance of $0.2 + j0.5$ Ω per phase and an internal voltage of 120 V per phase feeds a balanced Y-connected load of $39 + j28$ Ω per phase over a line of $0.8 + j1.5$ Ω per phase; the a-phase internal voltage is the reference. b) Calculate the three line currents. c) Calculate the phase voltages at the load. d) Calculate the line voltages at the load. e) Calculate the phase voltages at the generator terminals.

::: figure assets/circuit/nr12-ex11-1.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 11.1
:::

::: answer
We describe the whole three-phase circuit, one phase at a time: three sources at the generator's internal nodes, which we call **ga**, **gb** and **gc**, each carrying its phase in its value — `120*exp(-2j*pi/3)` is 120 V at −120° — then the generator's, the line's and the load's impedance in each phase, all in ohms, which we name `rga`, `rla` and `rfa` for the a phase and likewise for b and c. We take the generator's neutral as ground and call the load's neutral **nn**; we call the generator's terminals **a**, **b** and **c** and the load's **pa**, **pb** and **pc**. Nothing depends on the frequency, so we leave **omega** as a symbol. The question's quantities are then ordinary results: the a-phase line current $I_{aA}$ is the current through the line impedance `rla`; the phase voltage at the load, $V_{AN}$, is the voltage between **pa** and **nn**; the line voltage $V_{AB}$ is the voltage between **pa** and **pb**; and the phase voltage at the generator's terminal, $V_{An}$, is the voltage at node **a**. We type each difference into {{card:Evaluate}} as `v_pa - v_nn`, and its magnitude as `Abs(v_pa - v_nn)`, since the book quotes the voltages by magnitude. We set the analysis to AC.

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

::: applink NR12's Example 11.1 (AC)
:::

Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box; nothing here depends on the frequency.

Symbulator returns `i_rla` = {{o:1.92 - 1.44j}} A ({{o:2.400}}∠{{o:-36.87}}°, the book's $I_{aA}$), `|v_pa - v_nn|` = {{o:115.225}} V (the book's $|V_{AN}|$), `|v_pa - v_pb|` = {{o:199.576}} V (the book's $|V_{AB}|$) and `|v_a|` = {{o:118.898}} V (the book's $|V_{An}|$).

The question asks for all three phases of each quantity. In a balanced circuit the b and c phases carry the same magnitudes as the a phase, at −120° and +120° from it, and the run's `i_rlb` and `i_rlc`, `v_pb` and `v_pc` bear that out.

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
The circuit is Example 7.3's, and so is its first interval: before the switch moves the capacitor has sat across the 100 V source through the 10 kΩ for a long time, carrying no current. We describe that circuit as before and run it in DC for the capacitor's voltage:

```field 9 Circuit Description
e,1,0,100
r0,1,2,10'k
c,2,0,0.5'u
```

::: applink NR12's Example 13.2 (DC, before the switch moves)
:::

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `v_2` = {{o:100}} V (the book's $v_C(0)$).

The second interval is the same description as Example 7.3's second run, the 100 V in the capacitor's fifth field, with one difference: we set the analysis to FD instead of TR. FD returns each answer as a function of $s$, the Laplace transform of the answer in time, with the initial condition already inside it.

```field 9 Circuit Description
c,1,0,0.5'u,100
r1,1,2,32'k
r2,2,0,240'k
r3,2,0,60'k
```

::: applink NR12's Example 13.2 (FD)
:::

Set {{ui:Analysis}} to *FD — complex frequency domain*.

::: result voltage at node 2
v_{2} = \frac{60}{s + 25}\,\mathrm{V}
:::

`v_2` is the book's $V_o(s)$.

That is the transform of the answer Example 7.3 found in the time domain, $60e^{-25t}$: FD returns the transform, TR its inverse, for the same description.

:::
:::

::: problem NR12's Example 13.3

Consider the circuit in Fig. 13.13, where the initial current in the inductor is 29 mA and the initial voltage across the capacitor is 50 V. This circuit was analyzed in Example 8.10 using second-order circuit analysis techniques. Use the Laplace transform method to find $v(t)$ for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex13-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.3
:::

::: answer
The 24 mA source is a constant current switched on at $t$ = 0. In the $s$ domain a constant $I$ switched on at $t$ = 0 has the transform $I/s$, so we write the source's value as `0.024/s`. We put the two initial conditions the question gives in the fifth fields of the capacitor and the inductor, 50 V and 29 mA written 0.029, and name the four elements `j`, `c`, `l` and `r`. We set the analysis to FD, and the answer is the transform $V(s)$ of the voltage the question asks for; the book inverts it into $v(t)$ by hand, and choosing TR instead would do that inversion in the same run.

```field 9 Circuit Description
j,0,1,0.024/s
c,1,0,25'n,50
l,1,0,25'm,0.029
r,1,0,500
```

::: applink NR12's Example 13.3 (FD)
:::

Set {{ui:Analysis}} to *FD — complex frequency domain*.

::: result voltage at node 1
v_{1} = \frac{50 s - 200000}{s^{2} + 80000 s + 1600000000}\,\mathrm{V}
:::

`v_1` is the book's $V(s)$.

:::
:::

::: problem NR12's Example 13.6

The circuit in Fig. 13.20 has no initial stored energy, and at $t$ = 0 the switch closes. Find the Thévenin equivalent for the circuit to the left of the terminals a and b in the s domain, using Laplace methods.

::: figure assets/circuit/nr12-ex13-6.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.6
:::

::: answer
The 480 V source switched on at $t$ = 0 is a step, whose transform is $480/s$, so we write its value as `480/s`. We call the terminals a and b node **a** and ground, and name them to the {{card:Find equivalent}} card with *Thévenin / Norton* chosen; the card works in FD as it does in DC and AC, and returns the equivalent's voltage and impedance as functions of $s$. We leave out the capacitor to the right of the terminals, since the question asks for the equivalent seen from them.

```field 9 Circuit Description
e,1,0,480/s
r1,1,2,20
l,2,0,0.002
r2,2,a,60
```

::: applink NR12's Example 13.6 (Thévenin)
:::

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **a** and **0**. Set {{ui:Analysis}} to *FD — complex frequency domain*.

::: result Thevenin voltage
V_{Th} = \frac{480}{s + 10000}\,\mathrm{V}
:::

::: result Thevenin impedance
Z_{Th} = \frac{80 s + 600000}{s + 10000}\,\Omega
:::

Here `vth` is the book's $V_{Th}$ and `z` is the book's $Z_{Th}$.

:::
:::

::: problem NR12's Example 13.9

The voltage source $v_g$ drives the circuit shown in Fig. 13.31. The output signal is the voltage across the capacitor, $v_o$. a) Find the transfer function for this circuit. b) Calculate the numerical values for the poles and zeros of the transfer function.

::: figure assets/circuit/nr12-ex13-9.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.9
:::

::: answer
A transfer function is the ratio of an output to the input that produced it, as functions of $s$. We therefore leave the source as the symbol `vg`, so that the output comes back as a multiple of it, and set the analysis to FD. We number the nodes from the source, so the output, the capacitor's voltage, is the voltage at node 2, and the transfer function is `v_2/vg`, which we type into {{card:Evaluate}}.

```field 9 Circuit Description
e,1,0,vg
r1,1,2,1000
r2,2,3,250
l,3,0,50'm
c,2,0,1'u
```

::: applink NR12's Example 13.9 (FD)
:::

Set {{ui:Analysis}} to *FD — complex frequency domain*.

::: result transfer function
H(s) = \dfrac{v_{2}}{v_{g}} = \frac{1000 \left(s + 5000\right)}{s^{2} + 6000 s + 25000000}
:::

Part (b): the poles are the roots of the denominator, $s^2 + 6000s + 25{,}000{,}000 = 0$, which are $s = -3000 \pm j4000$; the zero is the root of the numerator, $s = -5000$.

:::
:::

::: problem NR12's Example 14.6

a) Show that the RLC circuit in Fig. 14.22 is a bandpass filter by deriving an expression for the transfer function $H(s)$. b) Compute the centre frequency. c) Calculate the cutoff frequencies, the bandwidth and $Q$. d) Compute $R$ and $L$ for a centre frequency of 5 kHz and a bandwidth of 200 Hz, using a 5 µF capacitor.

::: figure assets/circuit/nr12-ex14-6.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 14.6
:::

::: answer
Nothing in this question is a number until part (d), so we leave the three elements as the symbols `R`, `L` and `C` and the source as `vi`, naming the resistor `rr` to keep its name apart from its value; we set the analysis to FD, and the transfer function is the output voltage, at node 2, divided by the input, which we type into {{card:Evaluate}} as `v_2/vi`. The run returns it in terms of the three symbols, and parts (a) to (d) are read off that one expression.

```field 9 Circuit Description
e,1,0,vi
rr,1,2,R
c,2,0,C
l,2,0,L
```

::: applink NR12's Example 14.6 (FD)
:::

Set {{ui:Analysis}} to *FD — complex frequency domain*.

::: result transfer function
H(s) = \dfrac{v_{2}}{v_{i}} = \frac{L s}{C L R s^{2} + L s + R}
:::

Dividing numerator and denominator by $RLC$ puts it in the standard form $H(s) = \dfrac{s/RC}{s^2 + s/RC + 1/LC}$, which is a bandpass, part (a). Part (b): the centre frequency is $\omega_0 = 1/\sqrt{LC}$. Part (c): the bandwidth is $\beta = 1/RC$, the cutoff frequencies are $\omega_{c} = \mp\beta/2 + \sqrt{(\beta/2)^2 + \omega_0^2}$, and $Q = \omega_0/\beta$. Part (d): with $C$ = 5 µF, a centre frequency of 5 kHz is $\omega_0$ = 2π × 5000 rad/s, so $L = 1/(\omega_0^2 C)$ = {{o:202.6}} µH, and a bandwidth of 200 Hz is $\beta$ = 2π × 200 rad/s, so $R = 1/(\beta C)$ = {{o:159.2}} Ω.

:::
:::
