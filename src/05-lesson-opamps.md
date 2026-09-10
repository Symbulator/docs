---
id: lesson-opamps
kind: lesson
title: Operational amplifiers
updated: 2023-07-08
summary: >
  Learn how to describe an ideal *operational amplifier* (Op Amp) using the
  **o** element. And practice what you learn in a variety of solved op-amp
  problems, both easy and hard.
---

In this lesson, you will learn how to describe an ideal *operational amplifier*
— also called an Op Amp — using the **o** element. And you will practise what
you learn in a variety of solved op-amp problems, both easy and hard.

## How to describe an ideal operational amplifier {#describe-opamp}

There are many types of operational amplifiers. Symbulator can simulate the
ideal, linear type.{{i:operational amplifier}}

::: note Describing op amps
In Symbulator, an ideal op amp is described using four bits of information,
separated by commas: first, the name of the op amp, which must start with the
letter **o**; then, the names of the two input nodes, separated by a comma (the
polarity doesn't matter, you can give these input nodes in any order); and
finally, the name of the output node.

For example, an ideal op amp called **o1**, with input nodes **2** and **3** and output
node **5**, is described `o1,2,3,5`. And one called **o**, with input nodes **p** and **n** and
output node **o**, is `o,p,n,o`
:::

### What answers do you get

For each ideal op amp in a circuit, Symbulator {{v7,8|will store}}{{v9|gives}} the following
answers:

- The current through the output node, flowing from the output node outwards.
  For an op amp called **o**, that is `io`.
- The power consumed by the visible part of the op amp. For an op amp called
  o2, `po2`; the power delivered is the negative of
  that.
- And, as with every element's nodes, the voltage of each of its nodes with
  reference to ground. For node **o**, `vo`.

### Livin' on the edge

Since I was born to be bad, I like to play with node names to get the answers
as close to the book as possible. So do not be surprised if I call one op amp
"o" and name its output node "o" as well. That way I can ask for `vo` and `io`
and get the output voltage and current. But realise this: `vo` asks for the
voltage in node **o**, while in `io` the o stands for the element **o**.

::: only 7,8
You, too, can be bad to the bone, and live dangerously with your node naming,
as long as you anticipate what variables Symbulator will create to store the
answers. I tell you this because there are limits to what you can get away
with.

For example, when naming nodes, remember that for a node called #, Symbulator
creates a variable v# for its voltage. So never give a node the same name as an
element that has a voltage drop of its own: r, e, j, c, l. If in doubt, play it
safe and give every node a name of its own, different from any other node and
from any element.

In this example, we got away with it because op amps are not that type of
element. Symbulator does not save a voltage drop for op amps in a variable
called vo, so there is no problem having a node called **o** in the same circuit.

::: danger Never describe a source as e,#,0,v#
If you describe a source as `e1,1,0,v1`, Symbulator will define the voltage of
node **1**, namely v1, as having the value you provided for the source, which you
declared to be, wait for it… v1! The resulting equation, v1 = v1, is discarded
as trivial by the calculator, and this leaves Symbulator one equation short.
:::
:::
::: only 9
In Symbulator 9 the two cannot collide: {{card:Results}} lists node voltages and
element quantities separately, so a node called **o** and an op amp called **o** never
share a name.

::: danger Never describe a source as e,#,0,v_#
If you describe a source as `e1,1,0,v1`, you are declaring the voltage of node
1 to be the voltage of node **1**. The resulting equation, v1 = v1, is trivially
true and carries no information, which leaves the system one equation short.
:::
:::

::: problem Bo2's Drill Exercise 3.2
For the op-amp circuit shown, find vo and the power absorbed by the op amp.

::: figure assets/circuit/bo2de0302.jpg
Bo2's Drill Exercise 3.2
:::

::: answer
My solution:

```sym 7
s\dc("e,1,0,.1:r12,1,2,1'k:r2o,2,o,10'k:r30,3,0,1'k:r3o,3,o,20'k:o,3,2,o")
```
```sym 8
s\dc("e,1,0,.1:r12,1,2,1'k:r2o,2,o,10'k:r30,3,0,1'k:r3o,3,o,20'k:o,3,2,o")
```
```field 9 Circuit Description
e,1,0,.1
r12,1,2,1'k
r2o,2,o,10'k
r30,3,0,1'k
r3o,3,o,20'k
o,3,2,o
```

{{v7,8|We ask for the values of the variables `vo` and `po`:}}{{v9|Read `vo` and `po` in {{card:Results}}:}}

```sym 7
{vo,po}
```
```sym 8
{vo,po}
```
```out 7,8
{–2.1, –.00063}
```

::: only 9
- `vo` = {{o:-2.1}} V
- `po` = {{o:-0.00063}} W
:::

Which are correct. The voltage in node **o** is –2.1 V, and the op amp is absorbing
–.63 mW, which is to say it is delivering .63 mW of power to the circuit.
:::
:::

## Instructive Op Amp examples {#practice-opamps}

::: practice



### Solved Op Amp problems

::: problem Bo2's Drill Exercise 3.11 (Thévenin)

Find the Thévenin equivalent.

::: figure assets/practice/bo2s-drill-exercise-3-11-thevenin-1.jpg

:::

```sym 7
s\th("e,1,0,vs:r1,2,0,r1:r2,2,3,r2:o,1,2,3",3,0)
```
```sym 8
s\th("e,1,0,vs:r1,2,0,r1:r2,2,3,r2:o,1,2,3",3,0)
```
```field 9 Circuit Description
e,1,0,vs
r1,2,0,r1
r2,2,3,r2
o,1,2,3
```

::: only 9
Set {{ui:Type of analysis}} to *Find equivalent* and {{ui:Type of equivalent}} to *Thévenin / Norton*. Two node boxes appear: put **3** in the first and **0** in the second — the pair of terminals you are looking into.
:::

::: only 7,8
The {{tool:th}} script tells us it found the Thévenin voltage, but could not find
the Norton current. This is not a surprise, since an ideal op amp has zero
output resistance and a fixed voltage, an infinite current when
short-circuited. So the Thévenin equivalent is given by {{var:V_TH}} and no
resistance (or {{var:R_EQ}} = {{o:0}}Ω). Evaluating `vth` results in

((r1+r2) vs)/r1

This is correct, as can be seen by comparing it to the book's answer, shown
below.
:::

::: only 9
This one catches people out, and Symbulator says so:

::: result Thevenin voltage
v_{th} = \dfrac{vs\,(r_{1} + r_{2})}{r_{1}}
:::
::: result Norton current
i_{no} = \infty
:::
::: result equivalent resistance
R_{eq} = 0
:::
::: result maximum deliverable power
p_{max} = \infty
:::

with a note under the answers: the short-circuit current is unbounded, so
the equivalent is a voltage source with nothing in series.

That is not a failure to solve. An ideal op amp holds its output voltage
whatever current is drawn, so a short across its output carries an unbounded
current, which is exactly a source with no resistance in series:
{{var:R_EQ}} = {{o:0}} Ω. Symbulator finds it by putting a resistance across the
terminals and letting it fall to zero. {{var:V_TH}} matches the book's
answer.
:::

::: figure assets/practice/bo2s-drill-exercise-3-11-thevenin-2.jpg

:::

::: only 7,8
The Thevenin resistance, as explained above, is 0Ω.
:::

:::

::: problem AS2's Example 5.2

Find {{var:v_o}} and {{var:i_o}}.

::: figure assets/practice/as2s-example-5-2-3.jpg

:::

```sym 7
s\dc("e,2,0,1.:r5,1,0,5'k:r4,1,o,40'k:r2,o,0,20'k:o,2,1,o"):{vo,io}
```
```sym 8
s\dc("e,2,0,1.:r5,1,0,5'k:r4,1,o,40'k:r2,o,0,20'k:o,2,1,o"):{vo,io}
```
```field 9 Circuit Description
e,2,0,1.
r5,1,0,5'k
r4,1,o,40'k
r2,o,0,20'k
o,2,1,o
```

::: only 9
The answers you want are `vo` and `io`, in {{card:Results}}.
:::

::: only 7,8
The answer, {{o:{9.,.00065}}}, is correct: {{var:v_o}} is {{o:9}}V and {{var:i_o}} is
{{o:0.65}}mA
:::
::: only 9
The answer is {{var:v_o}} = {{o:9}}V and {{var:i_o}} = {{o:0.65}}mA. This is correct.
:::

:::

::: problem Bo2's Figure 3.3 (Inverting)

Find the gain of the overall circuit, {{var:v_o}}/{{var:v_S}}.

::: figure assets/practice/bo2s-figure-3-3-inverting-4.jpg

:::

```sym 7
s\dc("e,2,0,vs:r1,2,1,r1:r2,1,o,r2:o,1,0,o"):vo/vs
```
```sym 8
s\dc("e,2,0,vs:r1,2,1,r1:r2,1,o,r2:o,1,0,o"):vo/vs
```
```field 9 Circuit Description
e,2,0,vs
r1,2,1,r1
r2,1,o,r2
o,1,0,o
```

::: only 9
Ask {{card:Evaluate}} for:

```field 9 Evaluate
vo/vs
```
:::

::: only 7,8
We get **-r2/r1**, which is correct, as can be seen in the book's answer
above.
:::
::: only 9
We get

$$
\dfrac{v_{o}}{vs} = -\dfrac{r_{2}}{r_{1}}
$$

which is correct, as can be seen in the book's answer above.
:::

:::

::: problem AS2's Figure 5.10 (Inverting)

Find {{var:v_o}}.

::: figure assets/practice/as2s-figure-5-10-inverting-5.jpg

:::

```sym 7
s\dc("e,2,0,vi:r1,2,1,r1:rf,1,o,rf:o,0,1,o"):vo
```
```sym 8
s\dc("e,2,0,vi:r1,2,1,r1:rf,1,o,rf:o,0,1,o"):vo
```
```field 9 Circuit Description
e,2,0,vi
r1,2,1,r1
rf,1,o,rf
o,0,1,o
```

::: only 9
The answer you want is `vo`, in {{card:Results}}.
:::

This problem is almost identical to the one above. The answer we get is
correct:

::: only 7,8
-(rf/r1)vi
:::
::: only 9
::: result voltage of node o
v_{o} = -\dfrac{rf}{r_{1}}\,vi
:::
:::

:::

::: problem AS2's Example 5.3 (Inverting)

If {{var:v_i}} is 0.5V, calculate the output voltage {{var:v_o}} and the
current in the 10 kΩ resistor.

::: figure assets/practice/as2s-example-5-3-inverting-6.jpg

:::

```sym 7
s\dc("e,2,0,.5:r1,2,1,10'k:rf,1,o,25'k:o,0,1,o"):{vo,ir1}
```
```sym 8
s\dc("e,2,0,.5:r1,2,1,10'k:rf,1,o,25'k:o,0,1,o"):{vo,ir1}
```
```field 9 Circuit Description
e,2,0,.5
r1,2,1,10'k
rf,1,o,25'k
o,0,1,o
```

::: only 9
The answers you want are in {{card:Results}}:
:::

::: only 7,8
The answer, {{o:{-1.25, 5e-5}}}, is correct.
:::
::: only 9
::: result voltage of node o
v_{o} = -1.25\ \mathrm{V}
:::
::: result
i_{r1} = 5e-5\ \mathrm{A}
:::

This is correct.
:::

:::

::: problem TR5's Exercise 4-11 (Inverting)

Find {{var:v_O}} when {{var:v_S}} is 2V, -4V and 6V. Notice the output of the
op amp is limited to ±15V.

::: figure assets/practice/tr5s-exercise-4-11-inverting-7.jpg

:::

This may be the only non-linear problem you will see in this book, because I
solved it before I realized it included the ±15V constraint. But anyway, here
it goes.

```sym 7
s\dc("e,1,0,vs:r1,1,2,10'k:r2,2,o,33'k:o,0,2,o"):
{vo|vs=2.,vo|vs=-4.,vo|vs=6.}
```
```sym 8
s\dc("e,1,0,vs:r1,1,2,10'k:r2,2,o,33'k:o,0,2,o"):
{vo|vs=2.,vo|vs=–4.,vo|vs=6.}
```
```field 9 Circuit Description
e,1,0,vs
r1,1,2,10'k
r2,2,o,33'k
o,0,2,o
```

::: only 9
Put `vo` in {{card:Evaluate}} and the given value in its {{ui:Conditions}} box:

```field 9 Evaluate
vo
```

```field 9 Conditions
vs = 2
```

Then run it again with `vs = -4` and once more with `vs = 6`.
:::

::: only 7,8
The answer, {{o:{-6.6,13.2,-19.8}}}, is correct within the linear realm, but
since the output is constrained to no more than 15V or less than -15V, the
answer is {{var:v_O}}={{o:-15}}V for {{var:v_S}} = {{o:6}}V.
:::
::: only 9
The answers, `vo` = {{o:-6.6}} V, {{o:13.2}} V and {{o:-19.8}} V, are correct within the linear
realm, but since the output is constrained to no more than 15V or less than
-15V, the answer is {{var:v_O}}={{o:-15}}V for {{var:v_S}} = {{o:6}}V.
:::

:::

::: problem AS2's Practice Problem 5.3 (Inverting)

Find the output voltage of the op amp (i.e. {{var:v_o}}) and calculate the
current through the feedback resistor (i.e. the 15 kΩ resistor).

::: figure assets/practice/as2s-practice-problem-5-3-inverting-8.jpg

:::

My answer: Notice we used the m for milli in the value of the voltage
source.

```sym 7
s\dc("e,2,0,40'm:r1,2,1,5'k:rf,1,o,15'k:o,0,1,o"):approx({vo,irf})
```
```sym 8
s\dc("e,2,0,40'm:r1,2,1,5'k:rf,1,o,15'k:o,0,1,o"):approx({vo,irf})
```
```field 9 Circuit Description
e,2,0,40'm
r1,2,1,5'k
rf,1,o,15'k
o,0,1,o
```

::: only 7,8
The answer, **{-.12, 8e-6}**, is correct.
:::
::: only 9
The answers are:

::: result voltage of node o
v_{o} = -.12\ \mathrm{V}
:::
::: result
i_{rf} = 8e-6\ \mathrm{A}
:::

This is correct.
:::

:::

::: problem AS2's Example 5.4 (Inverting)

Determine {{var:v_o}}.

::: figure assets/practice/as2s-example-5-4-inverting-9.jpg

:::

```sym 7
s\dc("e6,1,0,6:r1,1,a,20'k:e2,b,0,2:rf,a,o,40'k:o,a,b,o"):vo
```
```sym 8
s\dc("e6,1,0,6:r1,1,a,20'k:e2,b,0,2:rf,a,o,40'k:o,a,b,o"):vo
```
```field 9 Circuit Description
e6,1,0,6
r1,1,a,20'k
e2,b,0,2
rf,a,o,40'k
o,a,b,o
```

::: only 9
The answer you want is `vo`, in {{card:Results}}.
:::

The answer, {{o:-6}}, is correct.

:::

::: problem TR5's Example 4-14 (Inverting)

Find the input-output relationship of the circuit.

::: figure assets/practice/tr5s-example-4-14-inverting-10.jpg

:::

The 'formal' way to *symbulate* this circuit would be as described below.

```sym 7
s\dc("e,1,0,vs:r1,1,b,r1:r2,b,0,r2:r3,b,a,r3:r4,a,o,r4:o,0,a,o:rl,o,0,rl")
```
```sym 8
s\dc("e,1,0,vs:r1,1,b,r1:r2,b,0,r2:r3,b,a,r3:r4,a,o,r4:o,0,a,o:rl,o,0,rl")
```
```field 9 Circuit Description
e,1,0,vs
r1,1,b,r1
r2,b,0,r2
r3,b,a,r3
r4,a,o,r4
o,0,a,o
rl,o,0,rl
```

However, since we are only interested in the ratio of the input to the
output, a smarter{{v7,8| (and faster – as in 49 seconds instead of 55 seconds)}} way
to *symbulate* it is this:

```sym 7
s\dc("e,1,0,1:r1,1,b,r1:r2,b,0,r2:r3,b,a,r3:r4,a,o,r4:o,0,a,o:rl,o,0,1")
```
```sym 8
s\dc("e,1,0,1:r1,1,b,r1:r2,b,0,r2:r3,b,a,r3:r4,a,o,r4:o,0,a,o:rl,o,0,1")
```
```field 9 Circuit Description
e,1,0,1
r1,1,b,r1
r2,b,0,r2
r3,b,a,r3
r4,a,o,r4
o,0,a,o
rl,o,0,1
```
::: applink TR5's Example 4-14 (Inverting, the quicker way)
:::

When we evaluate `vo/v1`, both approaches get the same answer:

::: only 7,8
::: figure assets/practice/tr5s-example-4-14-inverting-11.png

:::
:::

::: only 9
$$
\dfrac{v_{o}}{v_{1}} = -\dfrac{r_{2}\,r_{4}}{r_{1}\,r_{2} + r_{1}\,r_{3} + r_{2}\,r_{3}}
$$
:::

which is correct, as can be seen by comparing it to the book's answer.

::: figure assets/practice/tr5s-example-4-14-inverting-12.jpg

:::

:::

::: problem AS2's Practice Problem 5.4a (Transresistance)

This is a current-to-voltage converter, also called a *transresistance
amplifier*. Find {{var:v_o}}/{{var:i_S}}.

::: figure assets/practice/as2s-practice-problem-5-4a-transresistance-13.jpg

:::

```sym 7
s\dc("j,0,1,is:r,1,o,r:o,0,1,o"):vo/is
```
```sym 8
s\dc("j,0,1,is:r,1,o,r:o,0,1,o"):vo/is
```
```field 9 Circuit Description
j,0,1,is1
r,1,o,r
o,0,1,o
```

::: only 9
Ask {{card:Evaluate}} for:

```field 9 Evaluate
vo/is1
```
:::

::: only 7,8
The answer, **-r**, is correct.
:::
::: only 9
The answer is correct:

$$
\dfrac{v_{o}}{is_{1}} = -r
$$
:::

:::

::: problem AS2's Practice Problem 5.4b (Transresistance)

This is another *transresistance amplifier*. Again, find
{{var:v_o}}/{{var:i_S}}.

::: figure assets/practice/as2s-practice-problem-5-4b-transresistance-14.jpg

:::

```sym 7
s\dc("j,0,1,is:r1,1,2,r1:r2,2,0,r2:r3,2,o,r3:o,0,1,o")
```
```sym 8
s\dc("j,0,1,is:r1,1,2,r1:r2,2,0,r2:r3,2,o,r3:o,0,1,o")
```
```field 9 Circuit Description
j,0,1,is1
r1,1,2,r1
r2,2,0,r2
r3,2,o,r3
o,0,1,o
```

::: only 7,8
Asking:

`expand(vo/is)`

gets **-r1\*r3/r2-r1-r3**, which is equivalent to the book's answer.
:::
::: only 9
Ask {{card:Evaluate}} for `vo/is1`. It gives

$$
\dfrac{v_{o}}{is_{1}} = -r_{1} - \dfrac{r_{1}\,r_{3}}{r_{2}} - r_{3}
$$

which is equivalent to the book's answer — the same expression, gathered
differently.
:::

::: figure assets/practice/as2s-practice-problem-5-4b-transresistance-15.jpg

:::

:::

::: problem Bo2's Example 3.1 (Non-Inverting Amplifier)

Find {{var:v_o}}/{{var:v_1}}.

::: figure assets/practice/bo2s-example-3-1-non-inverting-amplifier-16.jpg

:::

```sym 7
s\dc("e,p,0,v2:r1,1,0,r1:r2,1,o,r2:o,p,1,o"):vo/v1
```
```sym 8
s\dc("e,p,0,v2:r1,1,0,r1:r2,1,o,r2:o,p,1,o"):vo/v1
```
```field 9 Circuit Description
e,p,0,v2
r1,1,0,r1
r2,1,o,r2
o,p,1,o
```

::: only 9
Ask {{card:Evaluate}} for:

```field 9 Evaluate
vo/v1
```
:::

::: only 7,8
We get {{o:1+r2/r1}}, which is correct.
:::
::: only 9
We get

$$
\dfrac{v_{o}}{v_{1}} = 1 + \dfrac{r_{2}}{r_{1}}
$$

which is correct.
:::

:::

::: problem AS2's Figure 5.16 (Non-Inverting Amplifier)

Find {{var:v_o}}.

::: figure assets/practice/as2s-figure-5-16-non-inverting-amplifier-17.jpg

:::

```sym 7
s\dc("e,2,0,vi:r1,0,1,r1:rf,1,o,rf:o,2,1,o"):vo
```
```sym 8
s\dc("e,2,0,vi:r1,0,1,r1:rf,1,o,rf:o,2,1,o"):vo
```
```field 9 Circuit Description
e,2,0,vi
r1,0,1,r1
rf,1,o,rf
o,2,1,o
```

::: only 9
The answer you want is `vo`, in {{card:Results}}.
:::

We get the right answer (below), an expression equivalent to the book's
answer.

::: only 7,8
$$
\left(\dfrac{r1 + rf}{r1}\right) vi
$$
:::
::: only 9
::: result voltage of node o
v_{o} = \left(\dfrac{r_{1} + rf}{r_{1}}\right) vi
:::
:::

:::

::: problem TR5's Example 4-13 (Non-Inverting Amplifier)

Find {{var:V_o}}/{{var:V_s}}.

::: figure assets/practice/tr5s-example-4-13-non-inverting-amplifier-18.jpg

:::

We can solve this problem in one simulation, as shown below.

```sym 7
s\dc("e,1,0,vs:r1,1,2,r1:r2,2,0,r2:o,2,3,o:r3,o,3,r3:r4,3,0,r4"):vo/vs
```
```sym 8
s\dc("e,1,0,vs:r1,1,2,r1:r2,2,0,r2:o,2,3,o:r3,o,3,r3:r4,3,0,r4"):vo/vs
```
```field 9 Circuit Description
e,1,0,vs
r1,1,2,r1
r2,2,0,r2
o,2,3,o
r3,o,3,r3
r4,3,0,r4
```

::: only 9
Ask {{card:Evaluate}} for:

```field 9 Evaluate
vo/vs
```
:::

We get

::: only 7,8
$$
\dfrac{r2\,(r3 + r4)}{(r1 + r2)\,r4}
$$
:::
::: only 9
$$
\dfrac{v_{o}}{v_{s}} = \dfrac{r_{2}\,(r_{3} + r_{4})}{(r_{1} + r_{2})\,r_{4}}
$$
:::

which is correct, as can be seen by comparing it to the book's answer.

::: figure assets/practice/tr5s-example-4-13-non-inverting-amplifier-19.jpg

:::

We can also solve it in stages, as shown below. First, simulate the left
half.

```sym 7
s\dc("e,1,0,vs:r1,1,2,r1:r2,2,0,r2"):v2/vs
```
```sym 8
s\dc("e,1,0,vs:r1,1,2,r1:r2,2,0,r2"):v2/vs
```
```field 9 Circuit Description
e,1,0,vs
r1,1,2,r1
r2,2,0,r2
```
::: applink TR5's Example 4-13 (the left half)
:::

::: only 9
Ask {{card:Evaluate}} for:

```field 9 Evaluate
v2/vs
```
:::

We get

::: only 7,8
$$
\dfrac{r2}{r1 + r2}
$$
:::
::: only 9
$$
\dfrac{v_{2}}{v_{s}} = \dfrac{r_{2}}{r_{1} + r_{2}}
$$
:::

which is correct for this part. Then, simulate the right half.

```sym 7
s\dc("e,2,0,1:o,2,3,o:r3,o,3,r3:r4,3,0,r4"):vo/v2
```
```sym 8
s\dc("e,2,0,1:o,2,3,o:r3,o,3,r3:r4,3,0,r4"):vo/v2
```
```field 9 Circuit Description
e,2,0,1
o,2,3,o
r3,o,3,r3
r4,3,0,r4
```
::: applink TR5's Example 4-13 (the right half)
:::

::: only 9
Ask {{card:Evaluate}} for:

```field 9 Evaluate
vo/v2
```
:::

We get

::: only 7,8
$$
\dfrac{r3 + r4}{r4}
$$
:::
::: only 9
$$
\dfrac{v_{o}}{v_{2}} = \dfrac{r_{3} + r_{4}}{r_{4}}
$$
:::

which is correct for this part. The product of these two partial answers
produces the same expression shown above after the big simulation, and is the
right answer.

:::

::: problem AS2's Figure 5.17 (Voltage Follower)

Find {{var:v_o}}.

::: figure assets/practice/as2s-figure-5-17-voltage-follower-20.jpg

:::

```sym 7
s\dc("e,1,0,vi:o,1,o,o"):vo
```
```sym 8
s\dc("e,1,0,vi:o,1,o,o"):vo
```
```field 9 Circuit Description
e,1,0,vi
o,1,o,o
```

::: only 9
The answer you want is `vo`, in {{card:Results}}.
:::

::: only 7,8
The answer, **vi**, is correct.
:::
::: only 9
The answer is correct:

::: result voltage of node o
v_{o} = vi
:::
:::

:::

::: problem TR5's Figure 4-32 (Voltage Follower)

::: figure assets/practice/tr5s-figure-4-32-voltage-follower-21.jpg

:::

::: figure assets/practice/tr5s-figure-4-32-voltage-follower-22.jpg

:::

Alright, so first we simulate the (b) circuit, to find its maximum power and
load power:

```sym 7
s\th("e,1,0,1.5:rs,1,2,2'k",2,0):{pmax,prL|L=1000}
```
```sym 8
s\th("e,1,0,1.5:rs,1,2,2'k",2,0):{pmax,prL|L=1000}
```
```field 9 Circuit Description
e,1,0,1.5
rs,1,2,2'k
```

::: only 9
Set {{ui:Type of analysis}} to *Find equivalent* and {{ui:Type of equivalent}} to *Thévenin / Norton*. Two node boxes appear: put **2** in the first and **0** in the second — the pair of terminals you are looking into. Tick the question about the load, choose *DC* and run it.

The answer you want is `pmax`, in {{card:Results}}, and under it `prl`, the power
in the load as {{ref:lesson-equivalents}} describes. Ask {{card:Evaluate}} for it
with the load in the {{ui:Conditions}} box:

```field 9 Evaluate
prl
```
```field 9 Conditions
load = 1000
```
:::

::: only 7,8
The answers we get, {{o:{2.8125e-4,2.5e-4}}}, are correct. Now we simulate the
(a) circuit.
:::
::: only 9
The answers we get, `pmax` = {{o:2.8125e-4}} W and `prl` = {{o:2.5e-4}} W in the 1 kΩ
load, are correct. Now we simulate the (a) circuit.
:::

```sym 7
s\dc("e,1,0,1.5:rs,1,2,2'k:o,2,o,o:rl,o,0,1'k"):prL
```
```sym 8
s\dc("e,1,0,1.5:rs,1,2,2'k:o,2,o,o:rl,o,0,1'k"):prL
```
```field 9 Circuit Description
e,1,0,1.5
rs,1,2,2'k
o,2,o,o
rl,o,0,1'k
```
::: applink TR5's Figure 4-32 (Voltage Follower, buffered)
:::

::: only 9
The answer you want is `prl`, in {{card:Results}} — the power consumed by the
load resistor **rl**.
:::

The answer, **.00225**, is correct. The apparent paradox — the load in (a)
drawing more power than the source in (b) seems able to provide — evaporates
once we remember that the ideal op amp in the schematic is only part of the
truth: the real one has its own source of power, which makes up the
difference.

:::

::: problem AS2's Example 5.5 (Inverting)

Find {{var:v_o}}.

::: figure assets/practice/as2s-example-5-5-inverting-23.jpg

:::

```sym 7
s\dc("e,1,0,6:r4,1,a,4'k:r10,a,o,10'k:e4,b,0,4:o,b,a,o"):vo
```
```sym 8
s\dc("e,1,0,6:r4,1,a,4'k:r10,a,o,10'k:e4,b,0,4:o,b,a,o"):vo
```
```field 9 Circuit Description
e1,1,0,6
r4,1,a,4'k
r10,a,o,10'k
e4,b,0,4
o,b,a,o
```

::: only 9
The answer you want is `vo`, in {{card:Results}}.
:::

The answer, {{o:-1}}, is correct.

:::

::: problem AS2's Practice Problem 5.5 (Non-Inverting)

Calculate {{var:v_o}}.

::: figure assets/practice/as2s-practice-problem-5-5-non-inverting-24.jpg

:::

```sym 7
s\dc("e,1,0,3:r4,1,2,4'k:r8,2,0,8'k:r2,3,0,2'k:r5,3,o,5'k:o,2,3,o")
```
```sym 8
s\dc("e,1,0,3:r4,1,2,4'k:r8,2,0,8'k:r2,3,0,2'k:r5,3,o,5'k:o,2,3,o")
```
```field 9 Circuit Description
e,1,0,3
r4,1,2,4'k
r8,2,0,8'k
r2,3,0,2'k
r5,3,o,5'k
o,2,3,o
```

The answer for `vo`, {{o:7}}, is correct.

:::

::: problem Bo2's Example 3.2 (Adder or Summing)

Find {{var:v_o}}.

::: figure assets/practice/bo2s-example-3-2-adder-or-summing-25.jpg

:::

```sym 7
s\dc("ea,3,0,va:eb,2,0,vb:r31,3,1,r1:r21,2,1,r1:r1o,1,o,r2:o,0,1,o"):vo
```
```sym 8
s\dc("ea,3,0,va:eb,2,0,vb:r31,3,1,r1:r21,2,1,r1:r1o,1,o,r2:o,0,1,o"):vo
```
```field 9 Circuit Description
ea,3,0,va
eb,2,0,vb
r31,3,1,r1
r21,2,1,r1
r1o,1,o,r2
o,0,1,o
```

::: only 9
The answer you want is `vo`, in {{card:Results}}:

::: result voltage of node o
v_{o} = -\dfrac{r_{2}}{r_{1}}\,(va + vb)
:::
:::

::: only 7,8
-(r2/r1)(va+vb)
:::

which is correct, as can be seen by comparing it to the book's answer.

::: figure assets/practice/bo2s-example-3-2-adder-or-summing-26.jpg

:::

:::

::: problem AS2's Figure 5.21 (Adder or Summing)

Find {{var:v_o}}.

::: figure assets/practice/as2s-figure-5-21-adder-or-summing-27.jpg

:::

```sym 7
s\dc("e1,b,0,v1:e2,c,0,v2:e3,d,0,v3:r1,b,a,r1:
r2,c,a,r2:r3,d,a,r3:rf,a,o,rf:o,0,a,o"):expand(vo)
```
```sym 8
s\dc("e1,b,0,v1:e2,c,0,v2:e3,d,0,v3:r1,b,a,r1:
r2,c,a,r2:r3,d,a,r3:rf,a,o,rf:o,0,a,o"):expand(vo)
```
```field 9 Circuit Description
e1,b,0,v1
e2,c,0,v2
e3,d,0,v3
r1,b,a,r1
r2,c,a,r2
r3,d,a,r3
rf,a,o,rf
o,0,a,o
```

::: only 9
Ask {{card:Evaluate}} for `expand(vo)`. It gives

$$
v_{o} = -\dfrac{rf\,v_{1}}{r_{1}} - \dfrac{rf\,v_{2}}{r_{2}} - \dfrac{rf\,v_{3}}{r_{3}}
$$
:::

::: only 7,8
-rf v1/r1 - rf v2/r2 - rf v3/r3
:::

which is correct, as can be seen by comparing it to the book's answer.

::: figure assets/practice/as2s-figure-5-21-adder-or-summing-28.jpg

:::

:::

::: problem AS2's Example 5.6 (Adder or Summing)

Find {{var:v_o}} and {{var:i_o}}.

::: figure assets/practice/as2s-example-5-6-adder-or-summing-29.jpg

:::

```sym 7
s\dc("e1,1,0,1:e2,2,0,2:r1,2,a,5'k:
r2,1,a,2.5'k:r3,a,o,10'k:r4,o,0,2'k:o,0,a,o"):{vo,io}
```
```sym 8
s\dc("e1,1,0,1:e2,2,0,2:r1,2,a,5'k:
r2,1,a,2.5'k:r3,a,o,10'k:r4,o,0,2'k:o,0,a,o"):{vo,io}
```
```field 9 Circuit Description
e1,1,0,1
e2,2,0,2
r1,2,a,5'k
r2,1,a,2.5'k
r3,a,o,10'k
r4,o,0,2'k
o,0,a,o
```

::: only 9
The answers you want are in {{card:Results}}:
:::

::: only 7,8
The answer, {{o:{-8.,-.0048}}}, is correct. Notice a current of 4.8mA is going
into the op amp.
:::
::: only 9
::: result voltage of node o
v_{o} = -8\ \mathrm{V}
:::
::: result
i_{o} = -.0048\ \mathrm{A}
:::

This is correct. Notice a current of 4.8mA is going into the op amp.
:::

:::

::: problem AS2's Practice Problem 5.6 (Adder or Summing)

Find {{var:v_o}} and {{var:i_o}}.

::: figure assets/practice/as2s-practice-problem-5-6-adder-or-summing-30.jpg

:::

```sym 7
s\dc("e2,2,0,1.5:e1,1,0,2:e6,6,0,1.2:r2,2,8,20'k:
r1,1,8,10'k:r6,6,8,6'k:r8,8,o,8'k:r4,o,0,4'k:o,0,8,o"):{vo,io}
```
```sym 8
s\dc("e2,2,0,1.5:e1,1,0,2:e6,6,0,1.2:r2,2,8,20'k:
r1,1,8,10'k:r6,6,8,6'k:r8,8,o,8'k:r4,o,0,4'k:o,0,8,o"):{vo,io}
```
```field 9 Circuit Description
e2,2,0,1.5
e1,1,0,2
e6,6,0,1.2
r2,2,8,20'k
r1,1,8,10'k
r6,6,8,6'k
r8,8,o,8'k
r4,o,0,4'k
o,0,8,o
```

::: only 9
The answers you want are in {{card:Results}}:
:::

::: only 7,8
The answer, {{o:{-3.8,-.001425}}}, is correct. Again, the current is going into
the op amp.
:::
::: only 9
::: result voltage of node o
v_{o} = -3.8\ \mathrm{V}
:::
::: result
i_{o} = -.001425\ \mathrm{A}
:::

This is correct. Again, the current is going into the op amp.
:::

:::

::: problem Bo2's Drill Exercise 3.3 (Difference or Differential)

::: figure assets/practice/bo2s-drill-exercise-3-3-difference-or-differential-31.jpg

:::

::: figure assets/practice/bo2s-drill-exercise-3-3-difference-or-differential-32.jpg

:::

```sym 7
s\dc("ea,4,0,va:eb,3,0,vb:r1,4,1,r1:r2,1,o,r2:
r3,3,2,r1:r4,2,0,r2:o,2,1,o")
```
```sym 8
s\dc("ea,4,0,va:eb,3,0,vb:r1,4,1,r1:r2,1,o,r2:
r3,3,2,r1:r4,2,0,r2:o,2,1,o")
```
```field 9 Circuit Description
ea,4,0,va
eb,3,0,vb
r1,4,1,r1
r2,1,o,r2
r3,3,2,r1
r4,2,0,r2
o,2,1,o
```

::: only 7,8
Evaluating `vo` we get the correct answer, equivalent to the book's answer
above.

((vb-va) r2)/r1
:::
::: only 9
`vo` is the correct answer, equivalent to the book's answer above:

::: result voltage of node o
v_{o} = \dfrac{(vb - va)\,r_{2}}{r_{1}}
:::
:::

:::

::: problem TR5's Exercise 4-13 (Difference or Differential)

Find {{var:v_o}}.

::: figure assets/practice/tr5s-exercise-4-13-difference-or-differential-33.jpg

:::

```sym 7
s\dc("e1,3,0,v1:e2,4,0,v2:r1,3,5,10'k:r2,4,6,10'k:
r3,5,o,40'k:r4,6,0,15'k:o,6,5,o")
```
```sym 8
s\dc("e1,3,0,v1:e2,4,0,v2:r1,3,5,10'k:r2,4,6,10'k:
r3,5,o,40'k:r4,6,0,15'k:o,6,5,o")
```
```field 9 Circuit Description
e1,3,0,v1
e2,4,0,v2
r1,3,5,10'k
r2,4,6,10'k
r3,5,o,40'k
r4,6,0,15'k
o,6,5,o
```

::: only 7,8
Evaluating `vo` we get {{o:3 v2 − 4 v1}}, which is the correct answer.
:::
::: only 9
`vo` is the correct answer:

::: result voltage of node o
v_{o} = 3\,v_{2} - 4\,v_{1}
:::
:::

:::

::: problem AS2's Figure 5.24 (Difference or Differential)

Find {{var:v_o}}. (And keep it in the memory, for you will use it in the next
three problems.)

::: figure assets/practice/as2s-figure-5-24-difference-or-differential-34.jpg

:::

```sym 7
s\dc("e1,d,0,v1:e2,c,0,v2:r1,d,a,r1:r3,c,b,r3:
r2,a,o,r2:r4,b,0,r4:o,b,a,o"):vo
```
```sym 8
s\dc("e1,d,0,v1:e2,c,0,v2:r1,d,a,r1:r3,c,b,r3:
r2,a,o,r2:r4,b,0,r4:o,b,a,o"):vo
```
```field 9 Circuit Description
e1,d,0,v1
e2,c,0,v2
r1,d,a,r1
r3,c,b,r3
r2,a,o,r2
r4,b,0,r4
o,b,a,o
```

::: only 9
The answer you want is in {{card:Results}}:
:::


::: only 7,8
$$
\dfrac{r1\,r4\,v2 - r2\,\bigl(r3\,v1 + r4\,(v1 - v2)\bigr)}{r1\,(r3 + r4)}
$$
:::
::: only 9
::: result voltage of node o
v_{o} = \dfrac{r_{1}\,r_{4}\,v_{2} - r_{2}\,\bigl(r_{3}\,v_{1} + r_{4}\,(v_{1} - v_{2})\bigr)}{r_{1}\,(r_{3} + r_{4})}
:::
:::

This expression is equivalent to the book's answer.

::: figure assets/practice/as2s-figure-5-24-difference-or-differential-35.jpg

:::

:::

::: problem AS2's Figure 5.24 (Subtractor)

For the same circuit of the previous problem, find {{var:v_o}} when
{{var:R_1}}={{var:R_2}} and {{var:R_3}}={{var:R_4}}.

Since we already have the expression for vo stored in the memory, we only do
this:

```sym 7
expand(vo)|r2=r1 and r3=r4
```
```sym 8
expand(vo)|r2=r1 and r3=r4
```

::: only 9
Ask {{card:Evaluate}} for `expand(vo)` and give it both equalities in the
{{ui:Conditions}} box:

```field 9 Conditions
r2 = r1
r3 = r4
```
:::

::: only 7,8
The answer we get, **v2-v1**, is correct.
:::
::: only 9
The answer we get is correct:

$$
v_{o} = v_{2} - v_{1}
$$
:::

:::

::: problem AS2's Example 5.7 (Difference or Differential)

Design an op amp circuit with inputs {{var:v_1}} and {{var:v_2}} such that
{{var:v_o}} = -5{{var:v_1}} + 3{{var:v_2}}.

My solution follows. The problem statement is a fancy way of saying: for the
circuit of the previous problem, find the resistor values that give an output
{{var:v_o}} = -5{{var:v_1}} + 3{{var:v_2}}. Not strictly a Symbulator problem, but
it shows how Symbulator fits into design problems.

First we take that part of {{var:v_o}} that is a factor of {{var:v_1}}, and
make it equal to -5. Thus:

```sym 7
Define v1=1:Define v2=0:expand(vo)=-5
```
```sym 8
Define v1=1:Define v2=0:expand(vo)=–5
```

::: only 9
Conditions again, this time on the inputs rather than the resistors:
`v1 = 1` and `v2 = 0`. Then `vo` is

::: result voltage of node o
v_{o} = -\frac{r_{2}}{r_{1}}
:::

which is equivalent to the book's expression, and it is that which has to
equal −5.

Symbulator will not always arrange an expression the way the book does. To
rearrange it, {{card:Evaluate}} takes `simplify()`, `collect()`, `expand()`,
`factor()` and `apart()`.
:::

::: only 7,8
We get {{o:-r2/r1=-5}}. Now make that part of {{var:v_o}} that is a factor of
{{var:v_2}} equal to 3. Thus:
:::
::: only 9
We get

$$
-\dfrac{r_{2}}{r_{1}} = -5
$$

Now make that part of {{var:v_o}} that is a factor of {{var:v_2}} equal to
3. Thus:
:::

```sym 7
Define v1=0:Define v2=1:expand(vo)=3
```
```sym 8
Define v1=0:Define v2=1:expand(vo)=3
```

::: only 9
With `v1 = 0` and `v2 = 1` instead, `vo` is

::: result voltage of node o
v_{o} = \frac{r_{4} \left(r_{1} + r_{2}\right)} {r_{1} \left(r_{3} + r_{4}\right)}
:::

which is equivalent to the book's expression, and it is that which has to
equal 3.

::: applink AS2's Example 5.7 (the v2 factor)
:::
:::

::: only 7,8
We get **r2\*r4/(r1\*(r3+r4))+r4/(r3+r4)=3** Now, since you have two
equations, you can solve for two unknowns. Of the four resistors you get to
choose, two can be whatever you want. The book recommends {{var:R_1}} = 10 kΩ
and {{var:R_3}} = 20 kΩ. Now let's find {{var:R_2}} and {{var:R_4}}.
:::
::: only 9
We get

$$
\dfrac{r_{4}\,(r_{1} + r_{2})}{r_{1}\,(r_{3} + r_{4})} = 3
$$

Now, since you have two equations, you can solve for two unknowns. Of the
four resistors you get to choose, two can be whatever you want. The book
recommends {{var:R_1}} = 10 kΩ and {{var:R_3}} = 20 kΩ. Now let's find
{{var:R_2}} and {{var:R_4}}.
:::

```sym 7
solve(ans(1) and ans(2),{r2,r4})|r1=10000 and r3=20000
```
```sym 8
solve(ans(1) and ans(2),{r2,r4})|r1=10000 and r3=20000
```

::: only 9
Write the two equations out in the {{card:Solve}} card, which solves a system
that is not a circuit:

```field 9 Equation(s) to solve in terms of the results
-r2/r1 = -5
r4*(r1 + r2)/(r1*(r3 + r4)) = 3
```

with `r2, r4` as the unknowns. The answer is a design rule rather than a
pair of numbers:

$$
r_{2} = 5\,r_{1}
$$
$$
r_{4} = r_{3}
$$

Put the book's **r1** = 10 kΩ and **r3** = 20 kΩ into it and you get {{o:50}} kΩ
and {{o:20}} kΩ.
:::

::: only 7,8
The expression above assumes that ans(1) and ans(2) are pointing to
the two equations we found before. We get **r2**={{o:50000}} and **r4**={{o:20000}}. This is
correct.
:::

Now, if this problem was part of a test, I'd like to verify that the answer
is correct. To confirm this, simulate the circuit using the four values given
above for the resistors.

```sym 7
s\dc("e1,d,0,v1:e2,c,0,v2:r1,d,a,10'k:
r3,c,b,20'k:r2,a,o,50'k:r4,b,0,20'k:o,b,a,o")
```
```sym 8
s\dc("e1,d,0,v1:e2,c,0,v2:r1,d,a,10'k:
r3,c,b,20'k:r2,a,o,50'k:r4,b,0,20'k:o,b,a,o")
```
```field 9 Circuit Description
e1,d,0,v1
e2,c,0,v2
r1,d,a,10'k
r3,c,b,20'k
r2,a,o,50'k
r4,b,0,20'k
o,b,a,o
```

::: applink AS2's Example 5.7 (checking the design)
:::

::: only 7,8
Evaluating `vo` gives us the desired output, **3\*v2-5\*v1**. The resistor
values are correct.
:::
::: only 9
`vo` is the desired output:

::: result voltage of node o
v_{o} = 3\,v_{2} - 5\,v_{1}
:::

The resistor values are correct.
:::

:::

::: problem AS2's Practice Problem 5.7 (Difference or Differential)

Design a difference amplifier with gain 4.

My solution follows. Again the statement is a fancy way of saying: for the
circuit of the previous problem, find the resistor values that give an output
{{var:v_o}} = {{o:4}} ({{var:v_2}}-{{var:v_1}}), that is, -4{{var:v_1}} +
4{{var:v_2}}. Same as before.

```sym 7
Define v1=1:Define v2=0:vo=-4
```
```sym 8
Define v1=1:Define v2=0:vo=–4
```

```sym 7
Define v1=0:Define v2=1:expand(vo)=4
```
```sym 8
Define v1=0:Define v2=1:expand(vo)=4
```

::: only 9
Exactly as in the previous problem: solve the circuit twice with
conditions on the inputs — `v1 = 1, v2 = 0`, then `v1 = 0, v2 = 1` — and
read `vo` each time. The two factors are the same as before, so the two
design equations are the same shape with 4 in place of 5 and 3.
:::

This time the book asks that you use {{var:R_1}} = 10 kΩ and {{var:R_3}} = 10 kΩ.
So we do that.

```sym 7
solve(ans(1) and ans(2),{r2,r4})|r1=10000 and r3=10000
```
```sym 8
solve(ans(1) and ans(2),{r2,r4})|r1=10000 and r3=10000
```

::: only 9
In the {{card:Solve}} card:

```field 9 Equation(s) to solve in terms of the results
-r2/r1 = -4
r4*(r1 + r2)/(r1*(r3 + r4)) = 4
```

with `r2, r4` as the unknowns. It answers

$$
r_{2} = 4\,r_{1}
$$
$$
r_{4} = 4\,r_{3}
$$

which at 10 kΩ each is {{o:40000}} Ω and {{o:40000}} Ω.
:::

::: only 7,8
We get **r2**={{o:40000}} and **r4**={{o:40000}}, the correct values for the remaining
resistors.
:::

:::

::: problem AS2's Practice Problem 5.8 (Instrumentation)

Find {{var:i_o}}.

::: figure assets/practice/as2s-practice-problem-5-8-instrumentation-36.jpg

:::

```sym 7
s\dc("e1,1,0,8.:e2,2,0,8.01:o1,1,3,3:o2,2,4,4:r1,3,5,20'k:
r2,4,6,20'k:r3,5,o,40'k:r4,6,0,40'k:o3,6,5,o:r5,o,0,10'k"):ir5
```
```sym 8
s\dc("e1,1,0,8.:e2,2,0,8.01:o1,1,3,3:o2,2,4,4:r1,3,5,20'k:
r2,4,6,20'k:r3,5,o,40'k:r4,6,0,40'k:o3,6,5,o:r5,o,0,10'k"):ir5
```
```field 9 Circuit Description
e1,1,0,8.
e2,2,0,8.01
o1,1,3,3
o2,2,4,4
r1,3,5,20'k
r2,4,6,20'k
r3,5,o,40'k
r4,6,0,40'k
o3,6,5,o
r5,o,0,10'k
```

::: only 9
The answer you want is `ir5`, in {{card:Results}}.
:::

In the schematic, the current {{var:i_o}} corresponds to `ir5`. The answer,
{{o:2e-6}}, is correct.

:::

::: problem Bo2's Example 3.3 (Cascade)

Find {{var:v_o}} in terms of the conductances and the applied voltage
{{var:v_S}}.

::: figure assets/practice/bo2s-example-3-3-cascade-37.jpg

:::

```sym 7
s\dc("e,1,0,vs:r12,1,2,1/g1:r14,1,4,1/g2:r4o,4,o,1/g3:
r2o,2,o,1/g4:r23,2,3,1/g:r34,3,4,1/g:o1,0,2,3:o2,0,4,o")
```
```sym 8
s\dc("e,1,0,vs:r12,1,2,1/g1:r14,1,4,1/g2:r4o,4,o,1/g3:
r2o,2,o,1/g4:r23,2,3,1/g:r34,3,4,1/g:o1,0,2,3:o2,0,4,o")
```
```field 9 Circuit Description
e,1,0,vs
r12,1,2,1/g1
r14,1,4,1/g2
r4o,4,o,1/g3
r2o,2,o,1/g4
r23,2,3,1/g
r34,3,4,1/g
o1,0,2,3
o2,0,4,o
```

::: only 7,8
Evaluating `vo` we get:

{{o:((g1-g2) vs)/(g3-g4)}}
:::
::: only 9
`vo` is:

::: result voltage of node o
v_{o} = \dfrac{(g_{1} - g_{2})\,vs}{g_{3} - g_{4}}
:::
:::

which is correct, as can be seen by comparing it to the book's answer.

::: figure assets/practice/bo2s-example-3-3-cascade-38.jpg

:::

:::

::: problem Bo2's Drill Exercise 3.4 (Cascade)

::: figure assets/practice/bo2s-drill-exercise-3-4-cascade-39.jpg

:::

::: figure assets/practice/bo2s-drill-exercise-3-4-cascade-40.jpg

:::

```sym 7
s\dc("e,1,0,vs:r1,2,o,1/1:r2,1,2,1/2:r3,2,3,1/3:
r4,4,0,1/4:r5,4,o,1/5:o1,0,2,3:o2,3,4,o")
```
```sym 8
s\dc("e,1,0,vs:r1,2,o,1/1:r2,1,2,1/2:r3,2,3,1/3:
r4,4,0,1/4:r5,4,o,1/5:o1,0,2,3:o2,3,4,o")
```
```field 9 Circuit Description
e,1,0,vs
r1,2,o,1/1
r2,1,2,1/2
r3,2,3,1/3
r4,4,0,1/4
r5,4,o,1/5
o1,0,2,3
o2,3,4,o
```

::: only 7,8
Evaluating `vo` we get: -**.75 vs**, which is correct.
:::
::: only 9
`vo` is correct:

::: result voltage of node o
v_{o} = -0.75\,vs
:::
:::

:::

::: problem AS2's Example 5.9 (Cascade)

Find {{var:v_o}} and {{var:i_o}}.

::: figure assets/practice/as2s-example-5-9-cascade-41.jpg

:::

```sym 7
s\dc("e,1,0,20'm:o1,1,2,a:o2,a,b,o:ro,o,b,10'k:
r4,b,0,4'k:r2,a,2,12'k:r3,2,0,3'k")
```
```sym 8
s\dc("e,1,0,20'm:o1,1,2,a:o2,a,b,o:ro,o,b,10'k:
r4,b,0,4'k:r2,a,2,12'k:r3,2,0,3'k")
```
```field 9 Circuit Description
e,1,0,20'm
o1,1,2,a
o2,a,b,o
ro,o,b,10'k
r4,b,0,4'k
r2,a,2,12'k
r3,2,0,3'k
```

::: only 7,8
Evaluating `approx({vo,iro})` we get the answer, {{o:{.35,2.5e-5}}}. This is
correct.
:::
::: only 9
`vo` is {{o:.35}} and `iro` is {{o:2.5e-5}}. This is
correct.
:::

:::

::: problem AS2's Practice Problem 5.9 (Cascade)

Determine {{var:v_o}} and {{var:i_o}}.

::: figure assets/practice/as2s-practice-problem-5-9-cascade-42.jpg

:::

```sym 7
s\dc("e,1,0,4:o1,1,2,2:o2,2,3,o:ro,3,0,4'k:r6,3,o,6'k"):{vo,iro}
```
```sym 8
s\dc("e,1,0,4:o1,1,2,2:o2,2,3,o:ro,3,0,4'k:r6,3,o,6'k"):{vo,iro}
```
```field 9 Circuit Description
e,1,0,4
o1,1,2,2
o2,2,3,o
ro,3,0,4'k
r6,3,o,6'k
```

::: only 9
The answers you want are `vo` and `iro`, in {{card:Results}}.
:::

::: only 7,8
The answer, {{o:{10,1/1000}}}, is correct. To say a 1/1000 A current is the
same as 1mA.
:::
::: only 9
The answer is `vo` = {{o:10}} V and `iro` = {{o:1/1000}} A, that is 1mA. This is correct.
:::

:::

::: problem AS2's Practice Problem 5.10 (Cascade)

If {{var:v_1}} = 2V and {{var:v_2}} = 1.5V, find {{var:v_o}} in the circuit.

::: figure assets/practice/as2s-practice-problem-5-10-cascade-43.jpg

:::

```sym 7
s\dc("e1,1,0,2:e2,2,0,1.5:o1,1,3,3:r1,2,5,10'k:r2,3,6,20'k:
r5,5,4,50'k:o2,0,5,4:r3,6,4,30'k:r6,6,o,60'k:o3,0,6,o"):vo
```
```sym 8
s\dc("e1,1,0,2:e2,2,0,1.5:o1,1,3,3:r1,2,5,10'k:r2,3,6,20'k:
r5,5,4,50'k:o2,0,5,4:r3,6,4,30'k:r6,6,o,60'k:o3,0,6,o"):vo
```
```field 9 Circuit Description
e1,1,0,2
e2,2,0,1.5
o1,1,3,3
r1,2,5,10'k
r2,3,6,20'k
r5,5,4,50'k
o2,0,5,4
r3,6,4,30'k
r6,6,o,60'k
o3,0,6,o
```

::: only 9
The answer you want is `vo`, in {{card:Results}}.
:::

The answer, {{o:9}}, is correct.

:::

::: problem TR5's Example 4-16 (Cascade)

Derive an expression for {{var:v_o}} in terms of the two inputs.

::: figure assets/practice/tr5s-example-4-16-cascade-44.jpg

:::

```sym 7
s\dc("e1,2,0,v1:e5,3,0,5:r1,2,4,5'k:r2,3,4,10'k:o1,0,4,a:r3,4,a,10'k:
r4,4,o,20'k:o2,a,5,o:r5,5,o,20'k:r6,5,0,10'k"):expand(approx(vo))
```
```sym 8
s\dc("e1,2,0,v1:e5,3,0,5:r1,2,4,5'k:r2,3,4,10'k:o1,0,4,a:r3,4,a,10'k:
r4,4,o,20'k:o2,a,5,o:r5,5,o,20'k:r6,5,0,10'k"):expand(approx(vo))
```
```field 9 Circuit Description
e1,2,0,v1
e5,3,0,5
r1,2,4,5'k
r2,3,4,10'k
o1,0,4,a
r3,4,a,10'k
r4,4,o,20'k
o2,a,5,o
r5,5,o,20'k
r6,5,0,10'k
```

::: only 9
Ask {{card:Evaluate}} for `expand(vo)` with {{ui:Rounding}} set to *approx (full precision)* in
{{card:Settings}}. The answer is arranged differently from the book's, which is a matter of presentation rather than of arithmetic.
:::

::: only 7,8
The answer, {{o:-2.4 v1 − 6}}, is correct.
:::
::: only 9
The answer is correct:

$$
v_{o} = -2.4\,v_{1} - 6
$$
:::

:::

::: problem TR5's Exercise 4-14 (Cascade)

Derive an expression for {{var:v_o}} in terms of the inputs {{var:v_1}} and
{{var:v_2}}.

::: figure assets/practice/tr5s-exercise-4-14-cascade-45.jpg

:::

```sym 7
s\dc("e1,3,0,v1:r1,3,4,10'k:o1,0,4,5:r2,4,5,40'k:r3,5,7,20'k:
e2,6,0,v2:r4,6,7,10'k:r5,7,o,40'k:o2,0,7,o"):expand(vo)
```
```sym 8
s\dc("e1,3,0,v1:r1,3,4,10'k:o1,0,4,5:r2,4,5,40'k:r3,5,7,20'k:
e2,6,0,v2:r4,6,7,10'k:r5,7,o,40'k:o2,0,7,o"):expand(vo)
```
```field 9 Circuit Description
e1,3,0,v1
r1,3,4,10'k
o1,0,4,5
r2,4,5,40'k
r3,5,7,20'k
e2,6,0,v2
r4,6,7,10'k
r5,7,o,40'k
o2,0,7,o
```

::: only 9
Ask {{card:Evaluate}} for `expand(vo)`.
:::

::: only 7,8
The answer, {{o:8 v1 – 4 v2}}, is correct.
:::
::: only 9
The answer is correct:

$$
v_{o} = 8\,v_{1} - 4\,v_{2}
$$
:::

:::

::: problem AS2's Example 5.10 (Cascade)

If {{var:v_1}} = 1V and {{var:v_2}} = 2V, find {{var:v_o}} in the circuit.

::: figure assets/practice/as2s-example-5-10-cascade-46.jpg

:::

```sym 7
s\dc("e1,1,0,1:e2,2,0,2:r2,1,3,2'k:r4,2,4,4'k:r6,3,a,6'k:r8,4,b,8'k:r5,a,c,5'k:r15,b,c,15'k:r10,c,o,10'k:oa,0,3,a:ob,0,4,b:oc,0,c,o"):approx(vo)
```
```sym 8
s\dc("e1,1,0,1:e2,2,0,2:r2,1,3,2'k:r4,2,4,4'k:r6,3,a,6'k:r8,4,b,8'k:r5,a,c,5'k:r15,b,c,15'k:r10,c,o,10'k:oa,0,3,a:ob,0,4,b:oc,0,c,o"):approx(vo)
```
```field 9 Circuit Description
e1,1,0,1
e2,2,0,2
r2,1,3,2'k
r4,2,4,4'k
r6,3,a,6'k
r8,4,b,8'k
r5,a,c,5'k
r15,b,c,15'k
r10,c,o,10'k
oa,0,3,a
ob,0,4,b
oc,0,c,o
```

The answer, {{o:8.667}}, is correct.

:::

::: problem TR5's Example 4-17 (Cascade)

Derive an expression for {{var:v_o}} in terms of the inputs {{var:v_1}} and
{{var:v_2}}.

::: figure assets/practice/tr5s-example-4-17-cascade-47.jpg

:::

```sym 7
s\dc("r1,5,0,r1:r2,5,a,r2:r3,a,6,r3:r4,6,o,r4:e1,3,0,v1:
e2,4,0,v2:o1,3,5,a:o2,4,6,o"):vo
```
```sym 8
s\dc("r1,5,0,r1:r2,5,a,r2:r3,a,6,r3:r4,6,o,r4:e1,3,0,v1:
e2,4,0,v2:o1,3,5,a:o2,4,6,o"):vo
```
```field 9 Circuit Description
r1,5,0,r1
r2,5,a,r2
r3,a,6,r3
r4,6,o,r4
e1,3,0,v1
e2,4,0,v2
o1,3,5,a
o2,4,6,o
```

::: only 9
The answer you want is `vo`, in {{card:Results}}.
:::

We get the right answer. Let's compare it with the book's answer.

::: figure assets/practice/tr5s-example-4-17-cascade-48.jpg

:::

Our answer, expanded via `expand(vo)`, is shown below:

::: only 7,8
$$
-\dfrac{r2\,r4\,v1}{r1\,r3} - \dfrac{r4\,v1}{r3} + \dfrac{r4\,v2}{r3} + v2
$$
:::
::: only 9
::: result voltage of node o
v_{o} = -\dfrac{r_{2}\,r_{4}\,v_{1}}{r_{1}\,r_{3}} - \dfrac{r_{4}\,v_{1}}{r_{3}} + \dfrac{r_{4}\,v_{2}}{r_{3}} + v_{2}
:::
:::

Playing with it by hand we get a form that, in my opinion, is *prettier* ;-)
than the book's:

::: only 7,8
$$
v2\left(\dfrac{r4}{r3} + 1\right) -
v1\left(\dfrac{r4}{r3}\right)\left(\dfrac{r2}{r1} + 1\right)
$$
:::
::: only 9
::: result voltage of node o
v_{o} = v_{2}\left(\dfrac{r_{4}}{r_{3}} + 1\right) - v_{1}\left(\dfrac{r_{4}}{r_{3}}\right)\left(\dfrac{r_{2}}{r_{1}} + 1\right)
:::
:::

:::

::: problem TR5's Example 4-18 (Multiple)

Derive an expression for {{var:v_o}} in terms of the inputs {{var:v_1}} and
{{var:v_2}}.

::: figure assets/practice/tr5s-example-4-18-multiple-49.jpg

:::

```sym 7
s\dc("e2,a,0,v2:e1,f,0,v1:o2,a,c,b:o1,f,d,e:r1,b,c,r1:r2,c,d,r2:r3,d,e,r3")
```
```sym 8
s\dc("e2,a,0,v2:e1,f,0,v1:o2,a,c,b:o1,f,d,e:r1,b,c,r1:r2,c,d,r2:r3,d,e,r3")
```
```field 9 Circuit Description
e2,a,0,v2
e1,f,0,v1
o2,a,c,b
o1,f,d,e
r1,b,c,r1
r2,c,d,r2
r3,d,e,r3
```

To find vo, we ask for `vb-ve`. We get an expression that can easily be
rearranged to look like this:

::: only 7,8
$$
-\left(\dfrac{r1 + r2 + r3}{r2}\right)(v1 - v2)
$$
:::
::: only 9
::: result voltage of node o
v_{o} = -\left(\dfrac{r_{1} + r_{2} + r_{3}}{r_{2}}\right)(v_{1} - v_{2})
:::
:::

This is exactly the answer from the book:

::: figure assets/practice/tr5s-example-4-18-multiple-50.jpg

:::

If you are ever in doubt whether two expressions are the same,
{{v7,8|enter them both separately into the calculator and compare them with
the equality sign. If the answer is '**true**', they are the same.}}{{v9|subtract one from the other in {{card:Evaluate}}: if the answer is `0`, they
are the same.}}

:::

:::
