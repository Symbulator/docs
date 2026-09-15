---
id: nr12-sampler
kind: back
title: Examples from Nilsson & Riedel 12e
versions: [9]
updated: 2026-09-12
summary: >
  Forty-three worked examples from *Electric Circuits*, each described in
  Symbulator and checked against the answer the book prints.
---

Here is a selection of problems from *Electric Circuits*, 12th edition, by
James W. Nilsson and Susan A. Riedel (Pearson). These are not the easiest
problems in the book, but they are well suited to showing what Symbulator
can do, since they are the ones where the distance between *describing a
circuit* and *solving it by hand* is widest. The book works each of them by
a named method, node voltages, mesh currents, superposition, a transform,
and its questions say which. Here each question is trimmed to what is
asked, since Symbulator is told the circuit and never the method.

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
*Nilsson & Riedel 12ed* from the list of books. The entries are named for the
example each one comes from, and each arrives with its note, its picture, its
settings, its Solve card fields and the analysis it wants already set.

Pick one, press {{btn:Run Symbulator}}, and the answers below are what you get.
{{ref:input-files}} explains what an entry remembers and how to save your own.

## Direct current — DC {#nr12-dc}

Sixteen resistive problems open the chapter. The running theme is that the book's
*method* — node voltages, mesh currents, source transformations, superposition,
a delta-to-wye transform — is a way of getting an answer by hand, not a property
of the answer. Symbulator is told the circuit and never told the method, so the
same kind of description serves whichever chapter a problem came from. Five of
these are op-amp problems with lettered parts, five are finished in the
{{card:Solve}} card, and the last two are two-port problems from the book's
final chapter.

::: problem NR12's Example 3.7

Find the current $i_o$ and the voltage $v_o$ for the circuit in the figure.

::: figure assets/circuit/nr12-ex3-7.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 3.7
:::

::: answer
The circuit consists of a current source feeding a ladder of seven resistors. The question wants the current in one branch, $i_o$ in the 24 Ω resistor, and the voltage across another, $v_o$ across the 30 Ω. We describe the circuit as it is drawn, naming the source `j` and the resistors `r1` to `r7` from left to right, and taking the bottom rail as ground, so $i_o$ is the current through `r7` and $v_o$ the voltage across `r6`. One run in DC returns every current and voltage in the circuit, those two among them.

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

For the Wheatstone bridge in the figure, $R_3$ can be varied from 10 Ω to 2 kΩ. What range of resistor values can this bridge measure?

::: figure assets/circuit/nr12-ex3-10.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 3.10
:::

::: answer
A Wheatstone bridge measures a resistance nobody knows, $R_x$, by comparing it with resistances that are known. The adjustable resistor $R_3$ is turned until the galvanometer between the two arms of the bridge carries no current, and at that setting the unknown can be read off the others. So we describe the circuit with the two resistances the question leaves open as symbols rather than numbers, which we name `R_3` for the adjustable one and `R_x` for the unknown, after the book's. We name the two known resistors `r1` and `r2`, and call the two arms' midpoints **a** and **b**. We describe the galvanometer as a short circuit, the element `s`, which we name `sg`: the figure gives it no resistance, and what we will need from it is its current, which a short reports as `isg`. We leave the source as a symbol too, `V_s`, since its value plays no part at balance. We run this as it stands, in DC, and every answer comes back as a formula in the three symbols.

```field 9 Circuit Description
e,1,0,V_s
r1,1,a,1'k
r2,1,b,4'k
sg,a,b
r3,a,0,R_3
rx,b,0,R_x
```

Set {{ui:Analysis}} to *DC — direct current*.

With the results on screen, we open the {{card:Solve}} card under them and ask the question the way the bridge is used. The balance condition, no current through the galvanometer, is the equation `isg=0`. The resistance we want is the unknown, `R_x`. The setting of the dial is a condition, first at its lowest, 10 Ω:

```field 9 Equation(s) to solve in terms of the results
isg=0
```

```field 9 Unknown(s) to solve for
R_x
```

```field 9 Conditions
R_3=10
```

Press {{btn:Solve equations}}.

The card returns `R_x` = {{o:40}} Ω.

For the other end of the dial we keep the equation and the unknown as they are and change only the condition, to the highest setting, 2 kΩ, written with the usual shorthand:

```field 9 Conditions
R_3=2'k
```

Then press {{btn:Solve equations}} again.

The card returns `R_x` = {{o:8000}} Ω.

So the smallest resistance the bridge can measure is {{o:40}} Ω and the largest {{o:8000}} Ω: its range is 40 Ω to 8 kΩ.

:::
:::

::: problem NR12's Example 3.11

Find a) the current and b) the power supplied by the 40 V source in the circuit shown in the figure.

::: figure assets/circuit/nr12-ex3-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 3.11
:::

::: answer
The circuit is a bridge: five resistors in a diamond with a sixth across the middle, fed by one source. The question wants what that source delivers, its current and its power. We write the bridge as it is drawn, naming the source `e` and the six resistors `r1` to `r6`.

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

The source's card reports the power it delivers as `-pe`, which is the power the question asks for. Its current it reports *into* the source, the same way as for every other element, so the current it supplies is the negative of that, which we read with a minus sign in the {{card:Evaluate}} card.

**a)** We type `-i_e` into {{card:Evaluate}}:

```field 9 Evaluate
-i_e
```

It gives {{o:0.5}} A (the book's $i$).

**b)** The power it supplies is read off its card: `-p_e` = {{o:20}} W (the book's $p$).

:::
:::

::: problem NR12's Example 4.4

Find the power dissipated in the 5 Ω resistor in the circuit shown in the figure.

::: figure assets/circuit/nr12-ex4-4.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.4
:::

::: answer
The circuit is resistive, with a dependent voltage source at its far end. Its value is eight times $i_\phi$, the current through the 5 Ω resistor, and the question wants the power that resistor dissipates. In Symbulator a dependent source needs no special element. It is a source whose value names another answer. We name the 5 Ω resistor `r3`, so its current is `ir3`, and write the dependent source as `e2` with the value `8*ir3`. We number the nodes 1 to 4 from the source rightward, with the bottom rail as ground. The power asked for is then `pr3`, the power consumed by `r3`.

```field 9 Circuit Description
e1,1,0,20
r1,1,2,2
r2,2,0,20
r3,2,3,5
r4,3,0,10
r5,3,4,2
e2,4,0,8*ir3
```

Set {{ui:Analysis}} to *DC — direct current*. Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with **n** = 4.

Symbulator returns `p_r3` = {{o:7.2}} W (the book's $p$).

:::
:::

::: problem NR12's Example 4.7

Find the power dissipated in the 4 Ω resistor in the circuit shown in the figure.

::: figure assets/circuit/nr12-ex4-7.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.7
:::

::: answer
The circuit again has a dependent voltage source, this time worth fifteen times $i_\phi$, the current in the 20 Ω resistor, and again the question wants one resistor's power, the 4 Ω's. We name the 20 Ω `r4`, so its current is `ir4` and the source `e2` has the value `15*ir4`. The 4 Ω we name `r3`, and its power is `pr3`. We number the nodes 1 to 3 with the bottom rail as ground.

```field 9 Circuit Description
e1,1,0,50
r1,1,3,1
r2,1,2,5
r3,2,3,4
r4,2,0,20
e2,3,0,15*ir4
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `p_r3` = {{o:16}} W (the book's $p$).

:::
:::

::: problem NR12's Example 4.8

Find the branch currents $i_a$, $i_b$ and $i_c$ in the circuit for Example 4.3, repeated here in the figure.

::: figure assets/circuit/nr12-ex4-8.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.8
:::

::: answer
The circuit consists of a voltage source and a current source feeding three resistors, and the question wants the current in each of the three branches. We name the sources `e` and `j` and the resistors `r1` to `r3`, and take the bottom rail as ground. A current source is written like a voltage source, name, two nodes, value, and its current flows through it from the first node to the second. The 3 A source's arrow points up from the bottom rail into node 2, so we write it `j,0,2,3`. We write each resistor's nodes in the direction of the figure's arrow, so that its current is counted as the book counts it: $i_a$ is `ir1`, $i_b$ is `ir2` and $i_c$ is `ir3`.

```field 9 Circuit Description
e,1,0,50
r1,1,2,5
r2,2,0,10
r3,2,0,40
j,0,2,3
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_r1` = {{o:2}} A (the book's $i_a$), `i_r2` = {{o:4}} A (the book's $i_b$) and `i_r3` = {{o:1}} A (the book's $i_c$).

:::
:::

::: problem NR12's Example 4.13

a) Find the voltage $v_o$ in the circuit shown in the figure. b) Find the power developed by the 250 V voltage source. c) Find the power developed by the 8 A current source.

::: figure assets/circuit/nr12-ex4-13.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.13
:::

::: answer
The circuit consists of two sources, one of voltage and one of current, and six resistors. The question wants the voltage across the 100 Ω, and the power each source develops. We write every element as it stands in the figure, the 125 Ω across the voltage source and the 10 Ω under the current source included, naming the resistors `r1` to `r6` from left to right and the sources `e` and `j`. The current source's arrow points down, from node 2 towards the 10 Ω, so we write its nodes in that order, `j,2,9,8`, calling the node between the source and the resistor **9**. $v_o$ is the voltage across `r4`.

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

The power a source *develops* is what it delivers, which each source's card reports as `-pe` and `-pj`.

Symbulator returns **a)** `v_r4` = {{o:20}} V (the book's $v_o$), **b)** `-p_e` = {{o:2800}} W (the book's $p_{250\,V}$) and **c)** `-p_j` = {{o:480}} W (the book's $p_{8\,A}$).

:::
:::

::: problem NR12's Example 4.21

a) For the circuit shown in the figure, find the value of $R_L$ that results in maximum power being transferred to $R_L$. b) Calculate the maximum power that can be delivered to $R_L$.

::: figure assets/circuit/nr12-ex4-21.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.21
:::

::: answer
The circuit consists of a source and two resistors with a load $R_L$ connected across the second, and the question is which load draws the most power from those terminals, and how much. That is a question about the circuit *seen from* the load, so we describe the source and the two resistors and leave $R_L$ out, calling its terminals node **2** and ground. The {{card:Find equivalent}} card, with *Thévenin / Norton* chosen and those two terminals named, reduces the circuit to its Thévenin equivalent and reports beside it the load that would draw the most power and how much that is: by the maximum power theorem that load equals the Thévenin resistance, which the card reports as `req`, and the power it reports as `pmax`.

```field 9 Circuit Description
e,1,0,360
r1,1,2,30
r2,2,0,150
```

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **2** and **0**.

Symbulator returns **a)** `req` = {{o:25}} Ω (the book's $R_L$) and **b)** `pmax` = {{o:900}} W.

:::
:::

::: problem NR12's Example 4.23

Find $v_o$ in the circuit shown in the figure.

::: figure assets/circuit/nr12-ex4-23.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 4.23
:::

::: answer
The circuit consists of two independent sources, two dependent ones and three resistors, and the question wants the voltage across the 20 Ω. We name the 5 Ω resistor `r1`, the 20 Ω `r2` and the 10 Ω `r3`. The dependent current source is worth $0.4v_\Delta$, and $v_\Delta$ is the voltage across the 10 Ω, so we write its value as `0.4*vr3`. The dependent voltage source is worth $2i_\Delta$, and $i_\Delta$ is the current through the 5 Ω, so we write its value as `2*ir1`. We write each source's nodes in the order its arrow or its polarity marks give, name the three inner nodes **a**, **b** and **c**, and take the bottom-right node as ground. $v_o$ is the voltage across `r2`.

```field 9 Circuit Description
e1,1,c,10
r1,1,a,5
r2,a,c,20
r3,b,0,10
j1,0,b,5
j2,b,a,0.4*vr3
e2,0,c,2*ir1
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `v_r2` = {{o:24}} V (the book's $v_o$).

:::
:::

::: problem NR12's Example 5.1

The op amp in the circuit shown in the figure is ideal. a) Calculate $v_o$ if $v_a$ = 1 V and $v_b$ = 0 V. b) Repeat (a) for $v_a$ = 1 V and $v_b$ = 2 V. c) If $v_a$ = 1.5 V, specify the range of $v_b$ that avoids amplifier saturation.

::: figure assets/circuit/nr12-ex5-1.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.1
:::

::: answer
The circuit is an op amp with two inputs, $v_a$ into the inverting side through a 25 kΩ resistor and $v_b$ straight into the non-inverting side, with a 100 kΩ feedback resistor. The question wants the output for two pairs of input values, and then the range of one input that keeps the amplifier out of saturation. An ideal op amp is the element `o`, whose three nodes are its non-inverting input, its inverting input and its output, in that order. We choose to write the two inputs as voltage sources with the symbolic values `va` and `vb` rather than the numbers in the question, so that one run returns the output as a formula in both, and each part can then be asked of that formula. We name the sources `ea` and `eb`, the resistors `r1` and `r2`, and number the nodes from the $v_a$ input, the output being node **3**. Symbulator's ideal op amp has no supplies, so it reports whatever output the inputs demand. Whether that output is within the ±10 V supplies of the figure is something we check afterwards.

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

`v_3` is the book's $v_o$.

Part (a) is that formula at $v_a$ = 1 V and $v_b$ = 0 V. We type the output's name into {{card:Evaluate}} and the two values into its {{ui:Conditions}} box:

```field 9 Evaluate
v_3
```

```field 9 Conditions
va = 1
vb = 0
```

It gives {{o:-4}} V (the book's $v_o$).

Part (b) changes only the second condition:

```field 9 Evaluate
v_3
```

```field 9 Conditions
va = 1
vb = 2
```

It gives {{o:6}} V (the book's $v_o$).

Part (c) asks where saturation begins. The op amp is linear while its output lies between the supply rails, which the figure gives as ±10 V, so the question is which $v_b$ puts the output exactly on a rail. That is a question for the {{card:Solve}} card: the output on the upper rail is the equation, $v_b$ the unknown, and $v_a$ = 1.5 V a condition:

```field 9 Equation(s) to solve in terms of the results
v_3=10
```

```field 9 Unknown(s) to solve for
vb
```

```field 9 Conditions
va=1.5
```

Press {{btn:Solve equations}}.

The card returns `vb` = {{o:3.2}} V.

For the lower rail we keep the unknown and the condition and change only the equation:

```field 9 Equation(s) to solve in terms of the results
v_3=-10
```

Then press {{btn:Solve equations}} again.

The card returns `vb` = {{o:-0.8}} V.

**a)** So {{var:v_o}} = {{o:-4}} V, inside the ±10 V supplies: the op amp is in its linear region and that is the answer.

**b)** Now {{var:v_o}} = {{o:6}} V, which is inside the supplies again.

**c)** The output reaches +10 V at {{var:v_b}} = {{o:3.2}} V and −10 V at {{var:v_b}} = {{o:-0.8}} V, so the op amp avoids saturation for {{o:-0.8}} V ≤ {{var:v_b}} ≤ {{o:3.2}} V.

:::
:::

::: problem NR12's Example 5.3

a) You have designed a summing amplifier, as per the problem's specifications. Verify that its output voltage is $v_o = -4v_a - v_b - 5v_c$, using an ideal op amp with ±12 V power supplies and a 20 kΩ feedback resistor. b) Suppose $v_a$ = 2 V and $v_c$ = $-$1 V. What range of input voltages for $v_b$ allows the op amp to remain linear?

::: figure assets/circuit/nr12-ex5-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.3
:::

::: answer
The circuit is a summing amplifier, which adds several input voltages, each with its own gain, and inverts the sum. The question asks us to verify a design made for the gains given, then to find the range of one input that keeps it linear. The output of a summing amplifier with feedback resistor $R_f$ and input resistors $R_a$, $R_b$ and $R_c$ is $v_o = -(R_f/R_a)v_a - (R_f/R_b)v_b - (R_f/R_c)v_c$, so with $R_f$ fixed at 20 kΩ the gains of 4, 1 and 5 want $R_a$ = 20/4 = 5 kΩ, $R_b$ = 20/1 = 20 kΩ and $R_c$ = 20/5 = 4 kΩ. That is the design, and the run checks it. We describe the circuit with those four resistors, which we name `r1`, `r2`, `r3` and `rf`. We write the three inputs as sources `ea`, `eb` and `ec` with the symbolic values `va`, `vb` and `vc`, so that the output comes back as a formula, and we write the op amp `o` with its non-inverting input at ground, its inverting input at a node we call **n**, and its output at node **4**.

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

`v_4` is the book's $v_o$.

Part (b) fixes two of the inputs and asks for the range of the third that keeps the output between the ±12 V rails. In the {{card:Solve}} card we put the output on the lower rail as the equation, name $v_b$ as the unknown, and give the two fixed inputs as conditions:

```field 9 Equation(s) to solve in terms of the results
v_4=-12
```

```field 9 Unknown(s) to solve for
vb
```

```field 9 Conditions
va=2
vc=-1
```

Press {{btn:Solve equations}}.

The card returns `vb` = {{o:9}} V.

For the upper rail we change only the equation:

```field 9 Equation(s) to solve in terms of the results
v_4=12
```

Then press {{btn:Solve equations}} again.

The card returns `vb` = {{o:-15}} V.

**a)** The run returns exactly the formula the design was to produce, which verifies the three resistor values.

**b)** The output sits on the −12 V rail at {{var:v_b}} = {{o:9}} V and on the +12 V rail at {{var:v_b}} = {{o:-15}} V, so the op amp remains linear for {{o:-15}} V ≤ {{var:v_b}} ≤ {{o:9}} V.

:::
:::

::: problem NR12's Example 5.3 part c

c) Suppose $v_a$ = 2 V, $v_b$ = 3 V and $v_c$ = $-$1 V. Using the input resistor values found in part (a), how large can the feedback resistor be before the op amp saturates?

::: figure assets/circuit/nr12-ex5-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.3
:::

::: answer
The circuit is the same summing amplifier with the three inputs now given as numbers, and the question is turned round: not the output for a given feedback resistor, but the largest feedback resistor for which the output stays within the rails. We describe the circuit as in part (a), the inputs as sources of 2, 3 and −1 V, and leave the feedback resistor as the symbol `rf` instead of a number, so that the run returns the output as a formula in `rf`.

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

Set {{ui:Analysis}} to *DC — direct current*. Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with **n** = 4.

::: result voltage at node 4
v_{4} = - 0.0003 rf\,\mathrm{V}
:::

`v_4` is the book's $v_o$.

The output is negative for any feedback resistor, so the rail it can reach is −12 V, and the largest feedback resistor is the one that puts the output exactly there. In the {{card:Solve}} card that is one equation and one unknown:

```field 9 Equation(s) to solve in terms of the results
v_4=-12
```

```field 9 Unknown(s) to solve for
rf
```

Press {{btn:Solve equations}}.

The card returns `rf` = {{o:40000}} Ω.

**c)** So the feedback resistor can be as large as {{o:40000}} Ω, 40 kΩ. Any larger and the output would have to go beyond −12 V, which it cannot: the op amp saturates.

:::
:::

::: problem NR12's Example 5.5

a) You have designed a difference amplifier, as per the problem's specifications. Verify that it amplifies the difference between two input voltages by a gain of 8, using an ideal op amp and ±8 V power supplies. b) Suppose $v_a$ = 1 V. What range of $v_b$ keeps the op amp linear?

::: figure assets/circuit/nr12-ex5-5.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.5
:::

::: answer
The circuit is a difference amplifier, which amplifies the difference between its two inputs. The question asks us to verify a design made for a gain of 8, then to find the range of one input that keeps it linear. Its output is $v_o = (R_b/R_a)(v_b - v_a)$, provided the four resistors satisfy $R_a/R_b = R_c/R_d$, so a gain of 8 needs $R_b$ eight times $R_a$ and $R_d$ eight times $R_c$. One choice, the book's, is $R_a$ = $R_c$ = 1.5 kΩ and $R_b$ = $R_d$ = 12 kΩ. We describe the circuit with those values, naming the resistors `ra` to `rd` after the book's, write the two inputs as sources with the symbolic values `va` and `vb` so that the output comes back as a formula, and call the op amp's two input nodes **p** and **n** and its output node **3**. The run checks the design.

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
v_{3} = - 8.0 va + 8.0 vb\,\mathrm{V}
:::

`v_3` is the book's $v_o$.

Part (b) fixes $v_a$ and asks for the range of $v_b$ that keeps the output between the ±8 V rails. In the {{card:Solve}} card, the output on the upper rail is the equation, $v_b$ the unknown and $v_a$ = 1 V a condition:

```field 9 Equation(s) to solve in terms of the results
v_3=8
```

```field 9 Unknown(s) to solve for
vb
```

```field 9 Conditions
va=1
```

Press {{btn:Solve equations}}.

The card returns `vb` = {{o:2}} V.

For the lower rail we change only the equation:

```field 9 Equation(s) to solve in terms of the results
v_3=-8
```

Then press {{btn:Solve equations}} again.

The card returns `vb` = {{o:0}} V.

**a)** The run returns exactly 8({{var:v_b}} − {{var:v_a}}), the gain the design was to produce, which verifies it.

**b)** The output reaches +8 V at {{var:v_b}} = {{o:2}} V and −8 V at {{var:v_b}} = {{o:0}} V, so the op amp remains linear for {{o:0}} V ≤ {{var:v_b}} ≤ {{o:2}} V.

:::
:::

::: problem NR12's Example 5.7

Analyze the noninverting amplifier of Example 5.4 using the realistic op amp model, with open-loop gain $A$ = 50,000, input resistance $R_i$ = 100 kΩ and output resistance $R_o$ = 7.5 kΩ; there is no load resistance at the output. Find the gain $v_o/v_g$.

::: figure assets/circuit/nr12-ex5-7.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 5.7
:::

::: answer
The circuit is a noninverting amplifier built not round an ideal op amp but round a realistic model of one: a dependent voltage source with a large but finite gain, an input resistance between its two inputs, and an output resistance in series with its output. The question wants the gain of the whole amplifier, output over source. We write the model as those three ordinary elements. We call the op amp's two input nodes **p** and **n**, write the input resistance as `ri` between them, the output resistance as `ro`, and the dependent source as `ea` with the value `50000*(vp-vn)`, the open-loop gain times the voltage between the inputs, $A(v_p - v_n)$. The other three resistors are `rg`, `rs` and `rf`. We leave the source as the symbol `vg`, so that the output comes back as a multiple of it. The gain is that multiple, which we will read in the {{card:Evaluate}} card.

```field 9 Circuit Description
eg,1,0,vg
rg,1,p,1'k
ri,p,n,100'k
rs,n,0,2'k
rf,n,3,10'k
ro,4,3,7.5'k
ea,4,0,50000*(vp-vn)
```

Set {{ui:Analysis}} to *DC — direct current*. Set {{ui:Rounding}} in {{card:Settings}} to *approx (full precision)*.

Then we type `v_3/vg` into {{card:Evaluate}}:

```field 9 Evaluate
v_3/vg
```

It gives {{o:5.9988}} (the book's $v_o/v_g$).

:::
:::

::: problem NR12's Example 18.1

Find the z parameters for the circuit shown in the figure.

::: figure assets/circuit/nr12-ex18-1.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 18.1
:::

::: answer
The circuit is a T of three resistors seen as a two-port, and the question wants its z parameters: the four numbers that relate the two port voltages to the two port currents. We take port 1 as node **1** with ground and port 2 as node **2** with ground, write the three resistors between those nodes, naming each after its value, and name the two ports to the {{card:Find equivalent}} card with *Two-port parameters* chosen and the kind set to **z**. It returns the four parameters, named `z11` to `z22`.

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
The circuit consists of two identical amplifiers, each known only by its four h parameters, one feeding the other between a source with an internal resistance and a load. The question wants the voltage gain of the pair. A two-port known only by its parameters is an element of its own. Since these are h parameters we use the element `h`, and write the four values after the two nodes as a bracketed term, `[1000,0.0015,100,0.0001]`, the 100 µS written as 0.0001. We write the two amplifiers as two such lines, `h1` and `h2`, sharing a node we call **b**, between the source's 500 Ω and the 10 kΩ load. We leave the source as the symbol `vg`, so that the output comes back as a multiple of it, and the gain is that multiple, which we will read in the {{card:Evaluate}} card.

```field 9 Circuit Description
e,1,0,vg
rs,1,a,500
h1,a,b,[1000,0.0015,100,0.0001]
h2,b,c,[1000,0.0015,100,0.0001]
rl,c,0,10'k
```

Set {{ui:Analysis}} to *DC — direct current*. Set {{ui:Rounding}} in {{card:Settings}} to *approx (full precision)*.

Then we type `v_c/vg` into {{card:Evaluate}}:

```field 9 Evaluate
v_c/vg
```

It gives {{o:33333.33}} (the book's $V_2/V_g$).

:::
:::

## Transients — TR {#nr12-tr}

Fourteen transient problems follow, three of them from the book's Laplace
chapter. The pattern is the one you would follow by hand: run the circuit as it
was before the switch moved in DC, read off the capacitor voltages and inductor
currents, put those numbers in the fifth field of the `c` and `l` lines, and run
the circuit as it is afterwards in TR. No time constant is computed, no solution
form is selected, and sequential switching is simply one more run. The
Laplace-chapter problems are no different: TR transforms, solves and inverts,
so what the book does in $s$ the solver does out of sight.

::: problem NR12's Example 7.1

The switch in the circuit shown in the figure has been closed for a long time before it is opened at $t$ = 0. Find a) $i_L(t)$ for $t$ ≥ 0, b) $i_o(t)$ for $t$ ≥ 0+, c) $v_o(t)$ for $t$ ≥ 0+.

::: figure assets/circuit/nr12-ex7-1.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.1
:::

::: answer
The circuit consists of an inductor that has been fed by a current source for a long time, and a switch that then cuts the source off and leaves the inductor to discharge through three resistors. The question wants the inductor's current and two other quantities afterwards, as functions of time. There are two intervals, and two runs. Before $t$ = 0 the switch has been closed for a long time, so any transient has died away and every current is steady. In a steady circuit an inductor carries its current with no voltage across it, which is to say it behaves as a wire. The full current of the source, 20 A, would run through it, and should be the initial condition of the inductor. To verify this intuition, we can run a DC simulation. Describe the circuit as it stands before the switch opens, the 20 A source, the 0.1 Ω resistor, the inductor and the three resistors beyond it, and run it for the inductor's current. We name the source `j`, the inductor `l` and the resistors `r0` to `r3`, and write the inductor with no fifth field, since nothing about its past is being told:

```field 9 Circuit Description
j,0,1,20
r0,1,0,0.1
l,1,0,2
r1,1,2,2
r2,2,0,10
r3,2,0,40
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_l` = {{o:20}} A (the book's $i_L(0)$).

Opening the switch disconnects the source and the 0.1 Ω resistor and leaves the inductor to release its energy through the three resistors. That is the circuit for the second interval, $t$ ≥ 0, and we describe it with the same names, dropping `j` and `r0`. The inductor now starts with the 20 A just found, which we write into its line as a fifth field, after the inductance. The answers come back as functions of $t$: $i_L$ is the current through `l`, $i_o$ the current through `r3`, and $v_o$ the voltage at node 2.

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

**a)** is `i_l`, **b)** is `i_r3` (the book's $i_o$) and **c)** is `v_2` (the book's $v_o$).

:::
:::

::: problem NR12's Example 7.3

The switch in the circuit shown in the figure has been in position x for a long time. At $t$ = 0 it moves instantaneously to position y. Find a) $v_C(t)$ for $t$ ≥ 0, b) $v_o(t)$ for $t$ ≥ 0+, and c) $i_o(t)$ for $t$ ≥ 0+.

::: figure assets/circuit/nr12-ex7-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.3
:::

::: answer
The circuit consists of a capacitor charged from one source, then switched over to a set of resistors to discharge. The question wants its voltage and two other quantities after the switch moves. There are two intervals, and two runs. At position x the capacitor has been connected to the 100 V source through the 10 kΩ resistor for a long time, and a capacitor in a steady circuit carries no current, so nothing flows in the 10 kΩ and the capacitor sits at the voltage of the source, 100 V, which would be its initial condition for the next interval. To confirm that intuition, we describe that circuit, the source, the 10 kΩ, which we name `r0`, and the capacitor, written without a fifth field, and run it in DC to find the capacitor's voltage:

```field 9 Circuit Description
e,1,0,100
r0,1,2,10'k
c,2,0,0.5'u
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `v_2` = {{o:100}} V (the book's $v_C(0)$).

At position y the capacitor is connected instead to the 32 kΩ resistor and the two beyond it, and discharges through them. We describe that second circuit with the 100 V just found as the capacitor's fifth field, naming the three resistors `r1` to `r3` and the capacitor's node **1**, and set the analysis to TR. $v_C$ is the voltage at node 1, $v_o$ the voltage at node 2, and $i_o$ the current through `r3`.

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
v_{1} = 100.0 e^{- 25.0 t}\,\mathrm{V}
:::

::: result voltage at node 2
v_{2} = 60.0 e^{- 25.0 t}\,\mathrm{V}
:::

::: result current through r3
i_{r3} = 0.001 e^{- 25.0 t}\,\mathrm{A}
:::

**a)** is `v_1` (the book's $v_C$), **b)** is `v_2` (the book's $v_o$) and **c)** is `i_r3` (the book's $i_o$).

:::
:::

::: problem NR12's Example 7.5

The switch in the circuit shown in the figure has been in position a for a long time. At $t$ = 0 it moves from position a to position b. The switch is a make-before-break type, so the inductor current is continuous. a) Find the expression for $i(t)$ for $t$ ≥ 0. b) What is the initial voltage across the inductor just after the switch has been moved to position b?

::: figure assets/circuit/nr12-ex7-5.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.5
:::

::: answer
The circuit consists of an inductor that has been carrying a current from one source and is switched, without a break, onto another. The question wants its current afterwards and the voltage across it the instant after the switch moves. There are two intervals, and two runs. With the switch at position a, the inductor has been in parallel with the 10 Ω resistor and the 8 A source for a long time, so the circuit is steady. The inductor behaves as a wire, so the whole 8 A would flow through it and none through the resistor, and that, with its sign, should be its initial condition. To verify this intuition, we can run a DC simulation. The direction matters: the source's arrow points down through the source, so its current comes up through the inductor, against the book's arrow for $i$. We write the source as `j,1,0,8`, its current flowing from node 1 down to ground, and the inductor as `l,1,0,0.2`, so that its current is counted downward like the book's $i$. A DC run then gives the current with its sign:

```field 9 Circuit Description
j,1,0,8
r,1,0,10
l,1,0,0.2
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_l` = {{o:-8}} A (the book's $i(0)$).

Moving the switch to b connects the inductor, through the 2 Ω resistor, to the 24 V source instead. Because the switch is make-before-break, the inductor's current does not jump at the switching: it starts at the −8 A just found. We describe the second circuit with that −8 as the inductor's fifth field, sign included, naming the source `e` and the resistor `r1`, and set the analysis to TR. $i$ is the current through `l`.

```field 9 Circuit Description
e,1,0,24
r1,1,2,2
l,2,0,0.2,-8
```

::: applink NR12's Example 7.5 (TR)
:::

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through l
i_{l} = 12.0 - 20.0 e^{- 10.0 t}\,\mathrm{A}
:::

**a)** is `i_l` (the book's $i$).

**b)** The inductor is between node 2 and ground, so the voltage across it is `v_2`, and we read its value the instant after the switch has moved, at $t$ = 0, with {{card:Evaluate}}:

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

There is no energy stored in the circuit in the figure at the time the switch is closed. Find the solutions for $i_o$, $v_o$, $i_1$ and $i_2$.

::: figure assets/circuit/nr12-ex7-10.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.10
:::

::: answer
The circuit consists of two coils wound on one core, both fed from the same node through one resistor, and a switch that connects the source at $t$ = 0. The question wants the source's current, the voltage across the coils and the current in each, all as functions of time. We write each coil as an inductor line of its own, `l1` and `l2`, and the coupling between them as the `m` line, which names the two coils and their mutual inductance, 6 H. No energy is stored, so we write neither inductor with a fifth field. The switch closing at $t$ = 0 needs no element: in TR a source with a plain numerical value is a step that begins at $t$ = 0, which is exactly what closing the switch on the 120 V source does. We name the source `e` and the resistor `r1`, and set the analysis to TR. $i_o$ is the current through `r1`, $v_o$ the voltage at node 2, and $i_1$ and $i_2$ the currents through `l1` and `l2`.

```field 9 Circuit Description
e,1,0,120
r1,1,2,7.5
l1,2,0,3
l2,2,0,15
m,l1,l2,6
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through r1
i_{r1} = 16.0 - 16.0 e^{- 5.0 t}\,\mathrm{A}
:::

::: result voltage at node 2
v_{2} = 120.0 e^{- 5.0 t}\,\mathrm{V}
:::

::: result current through l1
i_{l1} = 24.0 - 24.0 e^{- 5.0 t}\,\mathrm{A}
:::

::: result current through l2
i_{l2} = -8.0 + 8.0 e^{- 5.0 t}\,\mathrm{A}
:::

Here `i_r1` is the book's $i_o$, `v_2` is the book's $v_o$, `i_l1` is the book's $i_1$ and `i_l2` is the book's $i_2$.

:::
:::

::: problem NR12's Example 7.11 to 35 ms

The two switches in the circuit shown in the figure have been closed for a long time. At $t$ = 0 switch 1 is opened; then, 35 ms later, switch 2 is opened. a) Find $i_L(t)$ for 0 ≤ $t$ ≤ 35 ms.

::: figure assets/circuit/nr12-ex7-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.11
:::

::: answer
The circuit has an inductor and two switches that open one after the other. The question wants the inductor's current between the two openings. There are three intervals this time, and three runs. In the first, both switches have been closed for a long time and the circuit is steady. We describe the whole circuit, the 60 V source, the 4 Ω, 12 Ω, 6 Ω and 3 Ω resistors, the inductor and the 18 Ω, naming each resistor after its value, and run it in DC for the inductor's current:

```field 9 Circuit Description
e,1,0,60
r4,1,2,4
r12,2,0,12
r6,2,0,6
r3,2,3,3
l,3,0,0.15
r18,3,0,18
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_l` = {{o:6}} A (the book's $i_L(0)$).

In the second interval switch 1 has opened, which disconnects the 60 V source and the 4 Ω and 12 Ω resistors. We describe what remains, the 6 Ω, the 3 Ω, the inductor and the 18 Ω, with the same names, and give the inductor the 6 A just found as its fifth field. $i_L$ is the current through `l`.

```field 9 Circuit Description
r6,2,0,6
r3,2,3,3
l,3,0,0.15,6
r18,3,0,18
```

::: applink NR12's Example 7.11 to 35 ms (TR)
:::

Set {{ui:Analysis}} to *TR — transient / time domain*. Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with **n** = 4.

::: result current through l
i_{l} = 6.0 e^{- 40.0 t}\,\mathrm{A}
:::

**a)** is `i_l`.

This run holds until switch 2 opens at 35 ms, and the inductor's current at that instant is where the third interval starts. We read it from the answer with {{card:Evaluate}}, giving the instant in seconds:

```field 9 Evaluate
i_l
```

```field 9 Conditions
t = 0.035
```

It gives {{o:1.48}} A (the book's $i_L(35\,\mathrm{ms})$).

:::
:::

::: problem NR12's Example 7.11 after 35 ms

b) Find $i_L(t)$ for $t$ ≥ 35 ms. (Time is measured from the second switching.)

::: figure assets/circuit/nr12-ex7-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.11
:::

::: answer
This is the third interval of the same problem: switch 2 has opened too, removing the 18 Ω resistor, so the inductor now discharges through the 3 Ω and 6 Ω alone, and the question wants its current from that moment on. We describe that circuit with the 18 Ω dropped, and give the inductor as its fifth field the current found at the end of the previous entry, $6e^{-40 \times 0.035} = 6e^{-1.4}$, about 1.48 A. We write it as the expression `6*exp(-1.4)`, which is exact. We measure time from the second switching, as the book does, so this run's $t$ = 0 is the instant switch 2 opens. The analysis is TR.

```field 9 Circuit Description
r6,2,0,6
r3,2,3,3
l,3,0,0.15,6*exp(-1.4)
```

Set {{ui:Analysis}} to *TR — transient / time domain*. Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with **n** = 4.

::: result current through l
i_{l} = 1.48 e^{- 60.0 t}\,\mathrm{A}
:::

**b)** is `i_l`.

:::
:::

::: problem NR12's Example 7.13

a) When the switch is closed in the circuit shown in the figure, the voltage on the capacitor is 10 V. Find the expression for $v_o$ for $t$ ≥ 0. b) Assume that the capacitor short-circuits when its terminal voltage reaches 150 V. How many milliseconds elapse before the capacitor short-circuits?

::: figure assets/circuit/nr12-ex7-13.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 7.13
:::

::: answer
The circuit consists of a charged capacitor across two resistors and a dependent current source whose value is seven times the current in one of the resistors. The question wants the capacitor's voltage as a function of time, and then how long it takes to reach 150 V. The 10 V on the capacitor is given, and we write it into the capacitor's fifth field. We name the 20 kΩ resistor `r2`, so its current is `ir2` and the dependent source's value is `7*ir2`. The source's arrow points up into node 1, so we write it `j,0,1,7*ir2`. We set the analysis to TR. $v_o$ is the voltage at node 1.

```field 9 Circuit Description
c,1,0,5'u,10
r1,1,0,10'k
r2,1,0,20'k
j,0,1,7*ir2
```

Set {{ui:Analysis}} to *TR — transient / time domain*. Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with **n** = 4.

::: result voltage at node 1
v_{1} = 10.0 e^{40 t}\,\mathrm{V}
:::

**a)** is `v_1` (the book's $v_o$).

The exponent is positive, so the voltage grows instead of decaying: the dependent source feeds the capacitor faster than the resistors drain it.

**b)** The time it takes to reach 150 V is a question for the {{card:Solve}} card, with the time as the unknown:

```field 9 Equation(s) to solve in terms of the results
v_1=150
```

```field 9 Unknown(s) to solve for
t
```

Press {{btn:Solve equations}}.

The card returns `t` = {{o:0.0677}} s.

So the capacitor short-circuits after {{o:67.7}} ms.

:::
:::

::: problem NR12's Example 8.2

For the circuit in the figure, $v(0^+)$ = 12 V and $i_L(0^+)$ = 30 mA. Find the expression for $v(t)$. (Example 8.3 asks the same circuit for its three branch currents.)

::: figure assets/circuit/nr12-ex8-2.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.2
:::

::: answer
The circuit consists of a capacitor, an inductor and a resistor in parallel with no source, holding an initial voltage and an initial current. The question wants the voltage across the three as a function of time, and the following example wants the three branch currents. We write each element as a line between node 1 and ground, naming them `c`, `l` and `r`, and put the two initial conditions the question gives in the fifth fields: 12 V on the capacitor and 30 mA, written 0.03, on the inductor. The run is the circuit releasing the energy it holds. $v$ is the voltage at node 1, and $i_R$ and $i_L$ the currents through `r` and `l`.

```field 9 Circuit Description
c,1,0,0.2'u,12
l,1,0,50'm,0.03
r,1,0,200
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result voltage at node 1
v_{1} = 26.0 e^{- 20000.0 t} - 14.0 e^{- 5000.0 t}\,\mathrm{V}
:::

::: result current through r
i_{r} = 0.13 e^{- 20000.0 t} - 0.07 e^{- 5000.0 t}\,\mathrm{A}
:::

::: result current through l
i_{l} = - 0.026 e^{- 20000.0 t} + 0.056 e^{- 5000.0 t}\,\mathrm{A}
:::

`v_1` is the book's $v$.

:::
:::

::: problem NR12's Example 8.4

In the circuit shown in the figure, $V_0$ = 0 and $I_0$ = $-$12.25 mA. Calculate the voltage response for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex8-4.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.4
:::

::: answer
The circuit is the same three elements in parallel with different values, an initial current in the inductor and none on the capacitor. The question wants the voltage across them as a function of time. We describe them as before: $V_0$ = 0 goes in the capacitor's fifth field and $I_0$ = −12.25 mA in the inductor's, written −0.01225 with the sign the question gives it. We set the analysis to TR. $v$ is the voltage at node 1.

```field 9 Circuit Description
c,1,0,125'n,0
l,1,0,8,-0.01225
r,1,0,20'k
```

Set {{ui:Analysis}} to *TR — transient / time domain*. Set {{ui:Rounding}} in {{card:Settings}} to *approx (full precision)*.

::: result voltage at node 1
v_{1} = 100.02 e^{- 200.0 t} \sin{\left(979.8 t \right)}\,\mathrm{V}
:::

`v_1` is the book's $v$.

The book prints the amplitude as 100 and the frequency of the sine as 979.80, both rounded. To the same figures the run gives 100.02 and 979.80.

:::
:::

::: problem NR12's Example 8.11

The 0.1 µF capacitor in the circuit shown in the figure is charged to 100 V. At $t$ = 0 the capacitor is discharged through a series combination of a 100 mH inductor and a 560 Ω resistor. a) Find $i(t)$ for $t$ ≥ 0. b) Find $v_C(t)$ for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex8-11.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.11
:::

::: answer
The circuit is a charged capacitor discharging round a loop through an inductor and a resistor. The question wants the loop current and the capacitor's voltage as functions of time. We write the capacitor with 100 V as its fifth field, and the inductor and the resistor after it round the loop, naming the three `c`, `l` and `r`. We write the inductor's nodes as 2 then 1 on purpose, so that its current is counted in the direction of the book's arrow for $i$. Written the other way round, the answer would come back with its sign reversed. We set the analysis to TR. $i$ is the current through `l` and $v_C$ the voltage at node 1.

```field 9 Circuit Description
c,1,0,0.1'u,100
l,2,1,0.1
r,2,0,560
```

Set {{ui:Analysis}} to *TR — transient / time domain*. Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with **n** = 4.

::: result current through l
i_{l} = - 0.1042 e^{- 2800.0 t} \sin{\left(9600.0 t \right)}\,\mathrm{A}
:::

::: result voltage at node 1
v_{1} = \left(29.17 \sin{\left(9600.0 t \right)} + 100.0 \cos{\left(9600.0 t \right)}\right) e^{- 2800.0 t}\,\mathrm{V}
:::

**a)** is `i_l` (the book's $i$) and **b)** is `v_1` (the book's $v_C$).

:::
:::

::: problem NR12's Example 8.12

No energy is stored in the 100 mH inductor or the 0.4 µF capacitor when the switch in the circuit shown in the figure is closed. Find $v_C(t)$ for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex8-12.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 8.12
:::

::: answer
The circuit is a source switched at $t$ = 0 onto a loop of an inductor, a resistor and a capacitor, none of them holding any energy. The question wants the capacitor's voltage as a function of time. In TR a source with a plain numerical value is a step beginning at $t$ = 0, which is what the switch closing does, so the switch needs no element. We write the 48 V source and then the three elements in order round the loop, numbering the nodes 1 to 3, and write the inductor and the capacitor without a fifth field, since neither stores energy. We set the analysis to TR. $v_C$ is the voltage at node 3, the capacitor's upper end.

```field 9 Circuit Description
e,1,0,48
l,1,2,0.1
r,2,3,1250
c,3,0,0.4'u
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result voltage at node 3
v_{3} = 48.0 + 16.0 e^{- 10000.0 t} - 64.0 e^{- 2500.0 t}\,\mathrm{V}
:::

`v_3` is the book's $v_C$.

:::
:::

::: problem NR12's Example 13.5

The circuit in the figure has no initial stored energy. At $t$ = 0 the switch closes. Find $i_1(t)$ and $i_2(t)$ for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex13-5.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.5
:::

::: answer
The circuit consists of two loops sharing a resistor, each with an inductor, switched onto a source at $t$ = 0 with no energy stored. The question wants the two loop currents as functions of time. No energy is stored, so we write the two inductors without fifth fields, and the switch closing at $t$ = 0 onto the 336 V source needs no element of its own: in TR a numerical source value is a step that begins at $t$ = 0. We name the inductors `l1` and `l2` after the book's $i_1$ and $i_2$, which are the currents through them, and the resistors `r1` and `r2`. TR returns the two currents as functions of $t$. The Laplace transform and its inversion happen inside the solver.

```field 9 Circuit Description
e,1,0,336
l1,1,2,8.4
r1,2,0,42
l2,2,3,10
r2,3,0,48
```

Set {{ui:Analysis}} to *TR — transient / time domain*.

::: result current through l1
i_{l1} = 15.0 - 1.0 e^{- 12.0 t} - 14.0 e^{- 2.0 t}\,\mathrm{A}
:::

::: result current through l2
i_{l2} = 7.0 + 1.4 e^{- 12.0 t} - 8.4 e^{- 2.0 t}\,\mathrm{A}
:::

Here `i_l1` is the book's $i_1$ and `i_l2` is the book's $i_2$.

:::
:::

::: problem NR12's Example 13.7

The make-before-break switch in the circuit in the figure has been in position a for a long time. At $t$ = 0 it moves instantaneously to position b. Find $i_2(t)$ for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex13-7.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.7
:::

::: answer
The circuit consists of two coupled coils, the primary fed from a source through a switch and the secondary closed on two resistors. The switch takes the source out at $t$ = 0, and the question wants the secondary's current afterwards. There are two intervals, and two runs. With the switch at position a the primary side has been steady for a long time. We describe the whole circuit, naming the resistors after their values, `r9`, `r3`, `r2b` and `r10`, the coils `l1` and `l2`, and the coupling as the `m` line with their mutual inductance, 2 H. We call the secondary's top **q** and the node between its two resistors **c**, and take its bottom as ground -- nothing conducts between the two windings, so joining their bottoms changes no current. A DC run gives both currents:

```field 9 Circuit Description
e,1,0,60
r9,1,a,9
r3,a,p,3
l1,p,0,2
m,l1,l2,2
l2,q,0,8
r2b,q,c,2
r10,c,0,10
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_l1` = {{o:5}} A (the book's $i_1(0)$) and `i_l2` = {{o:0}} A (the book's $i_2(0)$).

At $t$ = 0 the switch moves to b, which takes the source and the 9 Ω out and closes the primary on the 3 Ω alone. We describe that circuit with the same names and the two currents just found as the coils' fifth fields, 5 and 0. $i_2$ is the current through `l2`.

```field 9 Circuit Description
r3,0,p,3
l1,p,0,2,5
m,l1,l2,2
l2,q,0,8,0
r2b,q,c,2
r10,c,0,10
```

::: applink NR12's Example 13.7 (TR)
:::

Set {{ui:Analysis}} to *TR — transient / time domain*. Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with **n** = 4.

::: result current through l2
i_{l2} = 0.25 \left(5.0 e^{2 t} - 5.0\right) e^{- 3 t}\,\mathrm{A}
:::

`i_l2` is the book's $i_2$.

:::
:::

::: problem NR12's Example 13.13

The switch in the circuit shown in the figure has been closed for a long time. At $t$ = 0 it opens. Find the output voltage $v_o$ and the current in the 3 H inductor, $i_1$.

::: figure assets/circuit/nr12-ex13-13.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.13
:::

::: answer
The circuit consists of two inductors, one carrying a current from a source and the other idle behind a closed switch that shorts it out. Opening the switch at $t$ = 0 forces the two into series, and the question wants the voltage across the second and the current in the first afterwards. There are two intervals, and two runs. While the switch is closed it joins the junction after $L_1$ to the bottom rail, and the circuit has been steady for a long time. We describe that circuit and run it in DC for the two inductor currents. We write the closed switch by giving both its ends the same node, ground, and name the inductors `l1` and `l2` after the book's $L_1$ and $L_2$:

```field 9 Circuit Description
e,1,0,100
r1,1,2,10
l1,2,0,3
r2,0,4,15
l2,4,0,2
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `i_l1` = {{o:10}} A (the book's $i_1(0)$) and `i_l2` = {{o:0}} A (the book's $i_2(0)$).

Opening the switch removes that wire, so the two inductors are now in series with the 15 Ω between them. We describe that circuit with the 10 A and 0 just found as their fifth fields, numbering the nodes 1 to 4 from the source. $v_o$ is the voltage at node 3, the top of the 15 Ω and $L_2$, and $i_1$ the current through `l1`.

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

The $\delta(t)$ in $v_o$ is an impulse. Opening the switch puts the two inductors in series, one carrying 10 A and the other none, and they must carry the same current from then on. An inductor's current cannot jump without an impulse of voltage across it, and the weight of this one, 12, is what it takes to bring $L_2$'s current from 0 to the 6 A the pair settle on.

:::
:::

## Sinusoidal steady state — AC {#nr12-ac}

Eight problems are in the sinusoidal steady state. Where the book gives
its impedances in ohms they go in as written, complex ones included, and the
frequency never enters: **omega** is left as a symbol in the
{{ui:ω — angular frequency}} box and nothing depends on it. Where the book gives
henries and farads instead, the frequency goes in that box and the conversion to
impedance is the solver's. Two of the eight state their source in rms, and say
so in {{card:Settings}}.

::: problem NR12's Example 9.9

The sinusoidal current source in the circuit shown in the figure produces the current $i_s$ = 8 cos 200,000$t$ A. b) Find the equivalent admittance to the right of the current source. c) Find the phasor voltage $v$. d) Find the phasor current $i$. e) Find the steady-state expressions for $v$ and $i$.

::: figure assets/circuit/nr12-ex9-9.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.9
:::

::: answer
The circuit consists of a sinusoidal current source at 200,000 rad/s feeding a resistor, a capacitor, and a branch of a resistor and an inductor. The question wants the admittance the source sees, the voltage across it and the current in the inductive branch as phasors, and those two as functions of time. The inductor and the capacitor are given as an inductance and a capacitance, and we write them as they are, `l,2,0,40'u` and `c,1,0,1'u`, putting the source's frequency, 200,000 rad/s, in the {{ui:ω — angular frequency}} box. The conversion to impedances is done inside the solver, so part (a), constructing the frequency-domain equivalent circuit, is out of scope for Symbulator and has been skipped. We write the current source as `j,0,1,8`, its arrow pointing up into node 1, with its 8 A as the amplitude, which is what the book's phasors carry too, and name the resistors `r1` and `r2`. In AC each answer is a phasor, printed both as a complex number and as an amplitude with an angle: $v$ is the voltage at node 1 and $i$ the current through `r2`.

```field 9 Circuit Description
j,0,1,8
r1,1,0,10
r2,1,2,6
l,2,0,40'u
c,1,0,1'u
```

Set {{ui:Analysis}} to *AC — alternating current*. Put **200000** in the {{ui:ω — angular frequency}} box. Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with **n** = 4.

**b)** Symbulator reports the impedance seen by each source, here `z_j`, and the admittance the source sees is its reciprocal, so we type into {{card:Evaluate}}:

```field 9 Evaluate
1/z_j
```

It gives {{o:0.16 + 0.12j}} S ({{o:0.2000}}∠{{o:36.87}}°, the book's $Y$).

**c)** and **d)** are read off the run: `v_1` = {{o:32 - 24j}} V ({{o:40.00}}∠{{o:-36.87}}°, the book's $v$) and `i_r2` = {{o:-4j}} A ({{o:4.000}}∠{{o:-90.00}}°, the book's $i$).

**e)** The steady-state expressions are the two phasors written back as functions of time at the source's frequency, which is circuit theory rather than a run: $v$ = 40 cos(200,000$t$ − 36.87°) V and $i$ = 4 cos(200,000$t$ − 90°) A.

:::
:::

::: problem NR12's Example 9.10

Find $I_0$, $I_1$, $I_2$, $I_3$, $I_4$, $I_5$, $V_1$ and $V_2$ in the circuit in the figure.

::: figure assets/circuit/nr12-ex9-10.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.10
:::

::: answer
The circuit is a bridge of five impedances fed by one source, every impedance given in ohms and several of them complex. The question wants the current in every branch and the voltage at two nodes. We write each impedance exactly as given, `-4j`, `63.2+2.4j`, `20+60j`, as a resistor with a complex value, naming the five `r1` to `r5` in the order of the book's $I_1$ to $I_5$, and we write each one's nodes in the direction of the figure's arrow, so that its current is counted as the book counts it. We keep the figure's letters for the nodes, with **d** as ground, so $V_1$ and $V_2$ are the voltages at **b** and **c**.

```field 9 Circuit Description
e,a,0,120
r1,a,b,-4j
r2,a,c,63.2+2.4j
r3,b,c,10
r4,b,0,20+60j
r5,c,0,-20j
```

Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box, since nothing here depends on the frequency. Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with **n** = 4.

The source current $I_0$ leaves the source's positive terminal, which is the opposite of how Symbulator counts a source's current, so we read it with a minus sign in the {{card:Evaluate}} card.

Symbulator returns `i_r1` = {{o:2 + 2.667j}} A ({{o:3.333}}∠{{o:53.13}}°, the book's $I_1$), `i_r2` = {{o:0.4 + 0.5333j}} A ({{o:0.6667}}∠{{o:53.13}}°, the book's $I_2$), `i_r3` = {{o:1.333 + 4.267j}} A ({{o:4.470}}∠{{o:72.65}}°, the book's $I_3$), `i_r4` = {{o:0.6667 - 1.6j}} A ({{o:1.733}}∠{{o:-67.38}}°, the book's $I_4$), `i_r5` = {{o:1.733 + 4.8j}} A ({{o:5.103}}∠{{o:70.14}}°, the book's $I_5$), `v_b` = {{o:109.3 + 8j}} V ({{o:109.6}}∠{{o:4.185}}°, the book's $V_1$) and `v_c` = {{o:96 - 34.67j}} V ({{o:102.1}}∠{{o:-19.86}}°, the book's $V_2$).

Then we type `-i_e` into {{card:Evaluate}}:

```field 9 Evaluate
-i_e
```

It gives {{o:2.4 + 3.2j}} A ({{o:4.000}}∠{{o:53.13}}°, the book's $I_0$).

:::
:::

::: problem NR12's Example 9.12

Find the Thévenin equivalent circuit with respect to terminals a,b for the circuit shown in the figure.

::: figure assets/circuit/nr12-ex9-12.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.12
:::

::: answer
This is an AC circuit with a dependent source inside it, and the question wants its Thévenin equivalent, a voltage and an impedance, seen from two terminals. The dependent voltage source is worth ten times $V_x$, the voltage across the 60 Ω resistor. We name that resistor `r2` and place it between node 2 and ground, so that $V_x$ is the voltage at node 2 and the source's value is `10*v2`. The figure names the terminals a and b. Terminal b is the bottom rail, which we take as ground, so we keep **a** as the top terminal's node and name **a** and **0** to the {{card:Find equivalent}} card with *Thévenin / Norton* chosen, which returns the equivalent's voltage and impedance. A dependent source in the circuit is no obstacle to it.

```field 9 Circuit Description
e1,1,0,120
r1,1,2,12
r2,2,0,60
r3,2,a,-40j
e2,3,0,10*v2
r4,3,a,120
```

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **a** and **0**. Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box, since nothing here depends on the frequency. Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with **n** = 4.

Symbulator returns `vth` = {{o:784 - 288j}} V ({{o:835.2}}∠{{o:-20.17}}°) and `zeq` = {{o:91.2 - 38.4j}} Ω ({{o:98.95}}∠{{o:-22.83}}°, the book's $Z_{Th}$).

:::
:::

::: problem NR12's Example 9.14

Find the voltages $V_1$, $V_2$ and $V_3$ in the circuit shown in the figure.

::: figure assets/circuit/nr12-ex9-14.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 9.14
:::

::: answer
This is an AC circuit of two loops with a dependent voltage source in the far one, worth 39 times $I_x$, the current down through the middle branch. The question wants three voltages, each marked across a pair of impedances in series: $V_1$ across the 1 Ω and {{var:j_2}} Ω on the left, $V_2$ across the 12 Ω and −{{var:j_16}} Ω in the middle, $V_3$ across the 1 Ω and {{var:j_3}} Ω on the right. Nothing else connects inside a pair, so we write each pair as one impedance, `r1` worth `1+2j`, `r2` worth `12-16j` and `r3` worth `1+3j`, and each voltage asked is then that element's own drop. $I_x$ is the current through `r2`, so the dependent source's value is `39*ir2`. We name the source's top node **a**, the top of the middle branch **b** and the dependent source's top **c**.

```field 9 Circuit Description
e1,a,0,150
r1,a,b,1+2j
r2,b,0,12-16j
r3,b,c,1+3j
e2,c,0,39*ir2
```

Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box, since nothing here depends on the frequency. Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with **n** = 4.

Symbulator returns `v_r1` = {{o:78 - 104j}} V ({{o:130.0}}∠{{o:-53.13}}°, the book's $V_1$), `v_r2` = {{o:72 + 104j}} V ({{o:126.5}}∠{{o:55.30}}°, the book's $V_2$) and `v_r3` = {{o:150 - 130j}} V ({{o:198.5}}∠{{o:-40.91}}°, the book's $V_3$).

:::
:::

::: problem NR12's Example 9.15

A linear transformer has $R_1$ = 200 Ω, $R_2$ = 100 Ω, $L_1$ = 9 H, $L_2$ = 4 H and $k$ = 0.5, and couples a load of an 800 Ω resistor in series with a 1 µF capacitor to a 300 V (rms) source of internal impedance $500 + j100$ Ω at 400 rad/s. g) Calculate the Thévenin equivalent with respect to the terminals of the load impedance.

::: answer
The circuit consists of a linear transformer, two coupled coils each with its own winding resistance, between a source with an internal impedance and a load. The question wants the Thévenin equivalent seen from the load's terminals. Of the book's seven parts, (a) to (f) are the steps of its own method -- the frequency-domain equivalent circuit, the two self-impedances, the reflected impedance, its scaling factor and the impedance looking into the primary -- and are skipped. Only (g) asks about the circuit itself. The coils are given as inductances, so we write them as they are, `l1,p,0,9` and `l2,q,0,4`, and put the frequency, 400 rad/s, in the {{ui:ω — angular frequency}} box. The coupling the book gives as $k$, and the `m` line takes it as it is, `m,l1,l2,k=0.5`, naming the two coils. The mutual inductance is worked out inside. The winding resistances $R_1$ and $R_2$ we name `r3` and `r6`, and the source's internal impedance, given in ohms, `r1` and `r2`. We leave the load out, because the question asks for the equivalent seen from its terminals: we call the top one node **c** and take the bottom one as ground -- nothing conducts between the two windings, so joining their bottoms changes no current -- and name **c** and **0** to the {{card:Find equivalent}} card with *Thévenin / Norton* chosen.

```field 9 Circuit Description
e,1,0,300
r1,1,2,500
r2,2,a,100j
r3,a,p,200
l1,p,0,9
m,l1,l2,k=0.5
l2,q,0,4
r6,q,c,100
```

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **c** and **0**. Set {{ui:Analysis}} to *AC — alternating current*. Put **400** in the {{ui:ω — angular frequency}} box. Tick {{ui:RMS phasors}} in {{card:Settings}}, since the book's source is given in rms. Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with **n** = 4.

Symbulator returns `vth` = {{o:93.94 + 17.77j}} V ({{o:95.60}}∠{{o:10.71}}°) and `zeq` = {{o:171.1 + 1224j}} Ω ({{o:1236}}∠{{o:82.04}}°, the book's $Z_{Th}$).

:::
:::

::: problem NR12's Example 10.8

a) Calculate the total average and reactive power delivered to each impedance in the circuit shown in the figure. b) Calculate the average and reactive powers associated with each source. c) Verify that the average power delivered equals the average power absorbed, and likewise for the reactive power.

::: figure assets/circuit/nr12-ex10-8.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 10.8
:::

::: answer
This entry takes the circuit of Example 9.14, which we describe the same way, and asks a question about power: how much average and reactive power each of its three impedances takes, how much each source supplies, and whether what is delivered balances what is absorbed. One run answers all three parts.

```field 9 Circuit Description
e1,a,0,150
r1,a,b,1+2j
r2,b,0,12-16j
r3,b,c,1+3j
e2,c,0,39*ir2
```

Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box, since nothing here depends on the frequency. Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with **n** = 4.

Every card of an AC run carries two power rows, *average (real) power*, the answer `p`, and *reactive power*, the answer `q`. On an impedance they read *consumed*, and each impedance in the figure is one element of our description, so part (a) is read straight off the three cards. On a source they read *delivered*, `-p` and `-q`, the negatives of the `p` and `q` answers, so part (b) is read off the two source cards the same way. For part (c), if every watt delivered is absorbed somewhere, the five `p` answers add to zero, and likewise the five `q`, which makes two sums in the {{card:Evaluate}} card.

**a)** The three impedances' cards read `p_r1` = {{o:1690}} W (the book's $P_1$), `q_r1` = {{o:3380}} var (the book's $Q_1$), `p_r2` = {{o:240}} W (the book's $P_2$), `q_r2` = {{o:-320}} var (the book's $Q_2$), `p_r3` = {{o:1970}} W (the book's $P_3$) and `q_r3` = {{o:5910}} var (the book's $Q_3$).

**b)** The two sources' cards read `-p_e1` = {{o:-1950}} W, `-q_e1` = {{o:3900}} var, `-p_e2` = {{o:5850}} W and `-q_e2` = {{o:5070}} var.

**c)** We type the sum of the five `p` answers into {{card:Evaluate}}:

```field 9 Evaluate
p_e1+p_e2+p_r1+p_r2+p_r3
```

It gives {{o:0}} W.

Then we do the same with the five `q`:

```field 9 Evaluate
q_e1+q_e2+q_r1+q_r2+q_r3
```

It gives {{o:0}} var.

A negative reading is the same power the other way: the $12 - j16$ Ω impedance's `q_r2` = −320 var means it delivers 320 var, and the independent source's `-p_e1` = −1950 W means it absorbs 1950 W. Both sums being zero, the average power delivered equals the average power absorbed, and the reactive power likewise.

:::
:::

::: problem NR12's Example 10.12

The variable resistor in the circuit in the figure is adjusted until maximum average power is delivered to $R_L$. a) What is the value of $R_L$ in ohms? b) What is the maximum average power delivered to $R_L$?

::: figure assets/circuit/nr12-ex10-12.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 10.12
:::

::: answer
The circuit consists of a source feeding a load through an ideal transformer whose windings share a node. The question wants the load that draws the most average power and how much that is. An ideal transformer is the element `t`. Because its primary and secondary here share a node, we write each winding as a bracketed pair of terminals, top node then bottom, `[p,x]` for the primary and `[a,x]` for the secondary, followed by the turns. The dots sit at opposite ends of the two windings, the primary's at the top and the secondary's at the bottom, and that polarity is a minus sign on one of the turn counts, so we write the ratio as `[-4,1]`. We name the two resistors after their values, `r60` and `r20`. The same transformer can also be written with the secondary's pair the other way round and the sign dropped, `t,[p,x],[x,a],[4,1]`, since reversing a pair reverses its polarity too, and the answers are the same. We leave the load $R_L$ out of the description and name its terminals, node **a** and ground, to the {{card:Find equivalent}} card with *Thévenin / Norton* chosen, which reports the load that would draw the most average power from those terminals and how much: by the maximum power theorem that load is the Thévenin impedance, reported as `zeq`, and the power is `pmax`.

```field 9 Circuit Description
e,1,0,840
r60,1,p,60
t,[p,x],[a,x],[-4,1]
r20,x,0,20
```

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **a** and **0**. Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box, since nothing here depends on the frequency. Tick {{ui:RMS phasors}} in {{card:Settings}}, since the book's source is given in rms. Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with **n** = 4.

Symbulator returns **a)** `zeq` = {{o:35}} Ω (the book's $R_L$) and **b)** `pmax` = {{o:315}} W.

:::
:::

::: problem NR12's Example 11.1

A balanced, positive-sequence Y-connected generator with an internal impedance of $0.2 + j0.5$ Ω per phase and an internal voltage of 120 V per phase feeds a balanced Y-connected load of $39 + j28$ Ω per phase over a line of $0.8 + j1.5$ Ω per phase; the a-phase internal voltage is the reference. b) Calculate the three line currents. c) Calculate the phase voltages at the load. d) Calculate the line voltages at the load. e) Calculate the phase voltages at the generator terminals. f) Calculate the line voltages at the generator terminals. g) Repeat for a negative phase sequence.

::: figure assets/circuit/nr12-ex11-1.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 11.1
:::

::: answer
The circuit consists of a three-phase generator, a three-phase line and a three-phase load, all Y-connected and all balanced. The question wants the three line currents and the phase and line voltages at the load and at the generator, first for a positive phase sequence and then for a negative one. We describe the whole circuit, one phase at a time. There are three sources at the generator's internal nodes, which we call **ga**, **gb** and **gc**, each written as a phasor, its magnitude and its angle in degrees: `(120∠0°)`, `(120∠-120°)` and `(120∠120°)`. Then come the generator's, the line's and the load's impedance in each phase, all in ohms, which we name `rga`, `rla` and `rfa` for the a phase and likewise for b and c. We take the generator's neutral as ground and call the load's neutral **nn**. The generator's terminals we call **a**, **b** and **c** and the load's **pa**, **pb** and **pc**.

```field 9 Circuit Description
ea,ga,0,(120∠0°)
eb,gb,0,(120∠-120°)
ec,gc,0,(120∠120°)
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

Set {{ui:Analysis}} to *AC — alternating current*. Leave **omega** in the {{ui:ω — angular frequency}} box, since nothing here depends on the frequency. Set {{ui:Rounding}} in {{card:Settings}} to *approx (full precision)*.

Every quantity the question asks for is the current through one element, the voltage at one node or the difference between two node voltages, so each part is read off the run or typed into the {{card:Evaluate}} card. The book prints each answer as a phasor, and the same value in that form follows each answer in parentheses.

**b)** The three line currents are the currents through the line impedances `rla`, `rlb` and `rlc`, read off their cards: `i_rla` = {{o:1.92 - 1.44j}} A ({{o:2.4000}}∠{{o:-36.870}}°, the book's $I_{aA}$), `i_rlb` = {{o:-2.2071 - 0.94277j}} A ({{o:2.4000}}∠{{o:-156.87}}°, the book's $I_{bB}$) and `i_rlc` = {{o:0.28708 + 2.3828j}} A ({{o:2.4000}}∠{{o:83.130}}°, the book's $I_{cC}$).

**c)** The phase voltages at the load are the voltages of its three nodes above its neutral **nn**. We type `v_pa-v_nn` into {{card:Evaluate}}:

```field 9 Evaluate
v_pa-v_nn
```

It gives {{o:115.2 - 2.4j}} V ({{o:115.22}}∠{{o:-1.1935}}°, the book's $V_{AN}$).

Likewise `v_pb-v_nn`:

```field 9 Evaluate
v_pb-v_nn
```

It gives {{o:-59.678 - 98.566j}} V ({{o:115.22}}∠{{o:-121.19}}°, the book's $V_{BN}$).

And `v_pc-v_nn`:

```field 9 Evaluate
v_pc-v_nn
```

It gives {{o:-55.522 + 100.97j}} V ({{o:115.22}}∠{{o:118.81}}°, the book's $V_{CN}$).

**d)** The line voltages at the load are the differences between pairs of its nodes. We type `v_pa-v_pb`:

```field 9 Evaluate
v_pa-v_pb
```

It gives {{o:174.88 + 96.166j}} V ({{o:199.58}}∠{{o:28.807}}°, the book's $V_{AB}$).

Likewise `v_pb-v_pc`:

```field 9 Evaluate
v_pb-v_pc
```

It gives {{o:-4.1569 - 199.53j}} V ({{o:199.58}}∠{{o:-91.193}}°, the book's $V_{BC}$).

And `v_pc-v_pa`:

```field 9 Evaluate
v_pc-v_pa
```

It gives {{o:-170.72 + 103.37j}} V ({{o:199.58}}∠{{o:148.81}}°, the book's $V_{CA}$).

**e)** The phase voltages at the generator's terminals are the voltages at nodes **a**, **b** and **c**, read off the run: `v_a` = {{o:118.9 - 0.672j}} V ({{o:118.90}}∠{{o:-0.32383}}°, the book's $V_{an}$), `v_b` = {{o:-60.03 - 102.63j}} V ({{o:118.90}}∠{{o:-120.32}}°, the book's $V_{bn}$) and `v_c` = {{o:-58.866 + 103.3j}} V ({{o:118.90}}∠{{o:119.68}}°, the book's $V_{cn}$).

**f)** The line voltages at the generator's terminals are the differences between those three. We type `v_a-v_b`:

```field 9 Evaluate
v_a-v_b
```

It gives {{o:178.93 + 101.96j}} V ({{o:205.94}}∠{{o:29.676}}°, the book's $V_{ab}$).

Likewise `v_b-v_c`:

```field 9 Evaluate
v_b-v_c
```

It gives {{o:-1.1639 - 205.93j}} V ({{o:205.94}}∠{{o:-90.324}}°, the book's $V_{bc}$).

And `v_c-v_a`:

```field 9 Evaluate
v_c-v_a
```

It gives {{o:-177.76 + 103.97j}} V ({{o:205.94}}∠{{o:149.68}}°, the book's $V_{ca}$).

**g)** A negative phase sequence is the same description with the angles of `eb` and `ec` exchanged, `(120∠120°)` and `(120∠-120°)`. Running it returns the same fifteen answers with every b-phase value and c-phase value exchanged, and the line voltages now lag the phase voltages by 30° instead of leading them.

:::
:::

## The s domain — FD {#nr12-fd}

Five problems are in the $s$ domain. FD returns every answer as a
function of $s$, initial conditions included, so a transfer function is nothing
more than the answer with the source left as a symbol, and two of these are
exactly that. Two others ask for a function of time, and are worked the way the
book works them: the circuit is solved in the $s$ domain and the answer inverted
afterwards, which is what `s2t` does in the {{card:Evaluate}} card. Nothing on
this page is labelled *filter* or *transfer function*, because nothing needs to
be. The book's other Laplace-chapter examples are in the TR section above, where
the solver transforms and inverts out of sight.

::: problem NR12's Example 13.2

The circuit in the figure is the circuit of Example 7.3. Find $v_o(t)$ for $t$ ≥ 0+.

::: figure assets/circuit/nr12-ex13-2.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.2
:::

::: answer
This is the circuit of Example 7.3, a capacitor charged from one source and switched over to a set of resistors, asked again with the answer wanted as a Laplace transform. Its first interval is the same: before the switch moves the capacitor has sat across the 100 V source through the 10 kΩ for a long time, so the circuit is steady. We describe that circuit as before and run it in DC for the capacitor's voltage:

```field 9 Circuit Description
e,1,0,100
r0,1,2,10'k
c,2,0,0.5'u
```

Set {{ui:Analysis}} to *DC — direct current*.

Symbulator returns `v_2` = {{o:100}} V (the book's $v_C(0)$).

The second interval is the same description as Example 7.3's second run, with the 100 V in the capacitor's fifth field. The analysis is the one difference. This chapter of the book works every problem by the Laplace method, which transforms the circuit into the $s$ domain, solves it there and inverts the result, so we set the analysis to FD. FD does the first two of those, returning each answer as a function of $s$ with the initial condition already inside it. $V_o(s)$ is the voltage at node 2.

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
v_{2} = \frac{60.0}{s + 25.0}\,\mathrm{V}
:::

`v_2` is the book's $V_o(s)$.

The question asks for $v_o(t)$, and the run has given its transform. Inverting it is the third step, and ours to take: `s2t` turns a function of $s$ back into a function of $t$, and we give it the answer just read.

```field 9 Evaluate
s2t(v_2)
```

It gives:

::: result the voltage at node 2, back in the time domain
v_{o}(t) = 60.0 e^{- 25.0 t}\,\mathrm{V}
:::

That is what Example 7.3 reached in a single TR run, which transforms, solves and inverts out of sight. Here the halves are separate and visible. FD does what the book does down to its $V_o(s)$, and `s2t` does the inversion the book performs with a table of transforms.

:::
:::

::: problem NR12's Example 13.3

Consider the circuit in the figure, where the initial current in the inductor is 29 mA and the initial voltage across the capacitor is 50 V. Find $v(t)$ for $t$ ≥ 0.

::: figure assets/circuit/nr12-ex13-3.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.3
:::

::: answer
The circuit is a parallel RLC circuit holding an initial current and an initial voltage, with a constant current source switched on at $t$ = 0. The question wants the voltage across it, and the book works it by the Laplace method. In the $s$ domain a constant $I$ switched on at $t$ = 0 has the transform $I/s$, so we write the 24 mA source's value as `0.024/s`. We put the two initial conditions the question gives in the fifth fields of the capacitor and the inductor, 50 V and 29 mA written 0.029, and name the four elements `j`, `c`, `l` and `r`. We set the analysis to FD, which returns the transform $V(s)$ of the voltage asked for, the voltage at node 1.

```field 9 Circuit Description
j,0,1,0.024/s
c,1,0,25'n,50
l,1,0,25'm,0.029
r,1,0,500
```

Set {{ui:Analysis}} to *FD — complex frequency domain*.

::: result voltage at node 1
v_{1} = \frac{50.0 s - 200000.0}{s^{2} + 80000.0 s + 1600000000.0}\,\mathrm{V}
:::

`v_1` is the book's $V(s)$.

The question asks for $v(t)$. `s2t` inverts a function of $s$ back into a function of $t$, so we give it the answer just read.

```field 9 Evaluate
s2t(v_1)
```

It gives:

::: result the voltage at node 1, back in the time domain
v(t) = \left(50.0 - 2200000.0 t\right) e^{- 40000.0 t}\,\mathrm{V}
:::

The book arrives at the same expression by a partial fraction expansion and a table of transforms, its last two steps. The same description run in TR returns it in one go, the solver transforming and inverting out of sight.

:::
:::

::: problem NR12's Example 13.6

The circuit in the figure has no initial stored energy, and at $t$ = 0 the switch closes. Find the Thévenin equivalent for the circuit to the left of the terminals a and b in the s domain.

::: figure assets/circuit/nr12-ex13-6.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.6
:::

::: answer
The circuit is a source switched at $t$ = 0 onto two resistors and an inductor, and the question wants the Thévenin equivalent of that part of the circuit, seen from two terminals, as functions of $s$. The 480 V source switched on at $t$ = 0 is a step, whose transform is $480/s$, so we write its value as `480/s`. We call the terminals a and b node **a** and ground, and name them to the {{card:Find equivalent}} card with *Thévenin / Norton* chosen. The card works in FD as it does in DC and AC, and returns the equivalent's voltage and impedance as functions of $s$. We leave out the capacitor to the right of the terminals, since the question asks for the equivalent seen from them.

```field 9 Circuit Description
e,1,0,480/s
r1,1,2,20
l,2,0,0.002
r2,2,a,60
```

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two terminals **a** and **0**. Set {{ui:Analysis}} to *FD — complex frequency domain*.

::: result Thevenin voltage
v_{th} = \frac{480.0}{s + 10000.0}\,\mathrm{V}
:::

::: result equivalent impedance
Z_{eq} = \frac{80.0 s + 600000.0}{s + 10000.0}\,\Omega
:::

`zeq` is the book's $Z_{Th}$.

:::
:::

::: problem NR12's Example 13.9

The voltage source $v_g$ drives the circuit shown in the figure. The output signal is the voltage across the capacitor, $v_o$. a) Find the transfer function for this circuit. b) Calculate the numerical values for the poles and zeros of the transfer function.

::: figure assets/circuit/nr12-ex13-9.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 13.9
:::

::: answer
The circuit consists of a source driving a resistor, a capacitor and an inductive branch, with the capacitor's voltage as the output. The question wants the transfer function from source to output, and its poles and zeros. A transfer function is the ratio of an output to the input that produced it, as functions of $s$, so we leave the source as the symbol `vg`, so that the output comes back as a multiple of it. We number the nodes from the source, so the output, the capacitor's voltage, is the voltage at node 2, and the transfer function is that voltage divided by `vg`, which we will read in the {{card:Evaluate}} card.

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

**a)** is the transfer function above.

**b)** The poles of a transfer function are the values of $s$ that make its denominator zero, and the zeros are the values that make its numerator zero. The {{card:Mini-Tools}} card finds both at once: we choose *pz — poles and zeros* in its {{ui:Tool}} menu and give it the transfer function.

```field 9 Value
v2/vg
```

Press {{btn:Run}}.

The card returns the poles {{o:-3000 - 4000j}} and {{o:-3000 + 4000j}}, and the zero {{o:-5000}}.

So the transfer function has poles at $s = -3000 \pm j4000$ and a zero at $s = -5000$. The card cancels any factor the numerator and the denominator share before it reads the roots, so a pole and a zero at the same place are not reported.

:::
:::

::: problem NR12's Example 14.6

a) Show that the RLC circuit in the figure is a bandpass filter by deriving an expression for the transfer function $H(s)$. b) Compute the centre frequency. c) Calculate the cutoff frequencies, the bandwidth and $Q$. d) Compute $R$ and $L$ for a centre frequency of 5 kHz and a bandwidth of 200 Hz, using a 5 µF capacitor.

::: figure assets/circuit/nr12-ex14-6.jpg
Nilsson & Riedel, 12th edition — the circuit for Example 14.6
:::

::: answer
The circuit consists of a series resistor feeding a parallel inductor and capacitor, with the voltage across the pair as the output. The question wants its transfer function shown to be a bandpass, its centre frequency, bandwidth and $Q$ in general, and then the resistor and inductor for a given centre frequency and bandwidth. Nothing in the question is a number until part (d), so we leave the three elements as the symbols `R`, `L` and `C` and the source as `vi`, naming the resistor `rr` to keep its name apart from its value. We set the analysis to FD. The transfer function is the output voltage, at node 2, divided by the input, which we will read in the {{card:Evaluate}} card, and it comes back in terms of the three symbols.

```field 9 Circuit Description
e,1,0,vi
rr,1,2,R
c,2,0,C
l,2,0,L
```

Set {{ui:Analysis}} to *FD — complex frequency domain*. Set {{ui:Rounding}} in {{card:Settings}} to *approx to n digits* with **n** = 4.

::: result transfer function
H(s) = \dfrac{v_{2}}{v_{i}} = \frac{L s}{C L R s^{2} + L s + R}
:::

**a)** Dividing numerator and denominator by $RLC$ puts the transfer function in the standard form $H(s) = \dfrac{s/RC}{s^2 + s/RC + 1/LC}$: a first-order numerator in $s$ over a second-order denominator, which is the shape of a bandpass filter.

**b)** The centre frequency is the $\omega_0$ of that denominator, $\omega_0 = 1/\sqrt{LC}$.

**c)** The bandwidth is the coefficient of $s$ in the denominator, $\beta = 1/RC$. The cutoff frequencies are $\omega_{c} = \mp\beta/2 + \sqrt{(\beta/2)^2 + \omega_0^2}$, and $Q = \omega_0/\beta$.

**d)** The question gives the centre frequency, the bandwidth and the capacitor and asks for $R$ and $L$. Those are two equations in two unknowns, which the {{card:Solve}} card takes as they stand: $\omega_0 = 1/\sqrt{LC}$ at 2π × 5000 rad/s and $\beta = 1/RC$ at 2π × 200 rad/s, with the capacitor as a condition:

```field 9 Equation(s) to solve in terms of the results
1/sqrt(L*C)=2*pi*5000
1/(R*C)=2*pi*200
```

```field 9 Unknown(s) to solve for
L, R
```

```field 9 Conditions
C=5'u
```

Tick {{ui:real solutions only}} and press {{btn:Solve equations}}.

The card returns `L` = {{o:0.0002026}} H and `R` = {{o:159.2}} Ω.

That is $L$ = 202.6 µH and $R$ = 159.2 Ω.

:::
:::
