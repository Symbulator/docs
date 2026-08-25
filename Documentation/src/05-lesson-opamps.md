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

For example, an ideal op amp called o1, whose input nodes are 2 and 3, and
whose output node is node 5, would be described as `o1,2,3,5`. And an ideal op
amp called o, whose input nodes are p and n and whose output node is also
called o, would be `o,p,n,o`
:::

### What answers do you get

For each ideal op amp in a circuit, Symbulator will store the following
answers:

- The current through the output node, flowing from the output node outwards.
  For an op amp called o, that is {{v7,8|`io`}}{{v9|`res.i("o")`}}.
- The power consumed by the visible part of the op amp. For an op amp called
  o2, {{v7,8|`po2`}}{{v9|`res["p_o2"]`}}; the power delivered is the negative of
  that.
- And, as with every element's nodes, the voltage of each of its nodes with
  reference to ground. For node o, {{v7,8|`vo`}}{{v9|`res.v("o")`}}.

### Livin' on the edge

Since I was born to be bad, I like to play with how I name nodes in order to
get the answers as close to the book as possible. So, do not be surprised if I
call one op amp "o" and then also name its output node "o". That way I can ask
for `vo` and `io`, and get the output voltage and current. But realise this: in
asking for `vo`, we are asking for the voltage in node o. And in asking for
`io`, the o stands for the element o.

::: only 7,8
You, too, can be bad to the bone, and live dangerously with your node naming,
as long as you anticipate what variables Symbulator will create to store the
answers. I tell you this because there are limits to what you can get away
with.

For example, when deciding the name of nodes, remember that for a node you name
#, Symbulator will create a variable called v# to store the voltage of that
node. Because of this, you should never name a node the same as any element for
which Symbulator will also calculate a voltage drop: r, e, j, c, l, for
example. If in doubt, play it safe: give nodes unique names, different from any
other node and from any element.

In this example, we got away with it because op amps are not that type of
element. Symbulator does not save a voltage drop for op amps in a variable
called vo, so there is no problem having a node called o in the same circuit.

::: danger Never describe a source as e,#,0,v#
If you describe a source as `e1,1,0,v1`, Symbulator will define the voltage of
node 1, namely v1, as having the value you provided for the source, which you
declared to be, wait for it… v1! The resulting equation, v1 = v1, is discarded
as trivial by the calculator, and this leaves Symbulator one equation short.
:::
:::
::: only 9
In Symbulator 9 the collision is impossible: node voltages are keyed `v_<node>`
and element quantities `v_<element>`, `i_<element>`, `p_<element>`, all inside
the result object, so a node called o and an op amp called o never contend for
the same name.

::: danger Never describe a source as e,#,0,v_#
If you describe a source as `e1,1,0,v_1`, you are declaring the voltage of node
1 to be the voltage of node 1. The resulting equation, v_1 = v_1, is trivially
true and carries no information, which leaves the system one equation short.
:::
:::

::: problem Bo2's Drill Exercise 3.2
For the op-amp circuit shown, find vo and the power absorbed by the op amp.

::: figure assets/circuit/bo2de0302.jpg
Bo2's Drill Exercise 3.2
:::

::: answer
My solution below:

```sym 7
s\dc("e,1,0,.1:r12,1,2,1'k:r2o,2,o,10'k:r30,3,0,1'k:r3o,3,o,20'k:o,3,2,o")
```
```sym 8
s\dc("e,1,0,.1:r12,1,2,1'k:r2o,2,o,10'k:r30,3,0,1'k:r3o,3,o,20'k:o,3,2,o")
```
```field 9 Circuit Description
e1,1,0,.1
r12,1,2,1'k
r2o,2,o,10'k
r30,3,0,1'k
r3o,3,o,20'k
o,3,2,o
```

We ask for the values of the variables `vo` and `po`:

```out
{–2.1, –.00063}
```

Which are correct. The voltage in node o is –2.1 V, and the op amp is absorbing
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
e1,1,0,vs
r1,2,0,r1
r2,2,3,r2
o,1,2,3
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **3** in the first and **0** in the second — the pair of terminals you are looking into.
:::

The **th** script tells us it found the Thévenin voltage, but could not find
the Norton current. This is not a surprise, since an ideal op amp has zero
output resistance and a fixed voltage, an infinite current when
short-circuited. So the Thévenin equivalent is given by V{{sub:TH}} and no
resistance (or R{{sub:EQ}} = 0Ω). Evaluating `vth` results in

This is correct, as can be seen by comparing it to the book's answer, shown
below.

::: figure assets/practice/bo2s-drill-exercise-3-11-thevenin-2.jpg

:::

The Thevenin resistance, as explained above, is 0Ω.

:::

::: problem AS2's Example 5.2

Find v{{sub:o}} and i{{sub:o}}.

::: figure assets/practice/as2s-example-5-2-3.jpg

:::

```sym 7
s\dc("e,2,0,1.:r5,1,0,5'k:r4,1,o,40'k:r2,o,0,20'k:o,2,1,o"):{vo,io}
```
```sym 8
s\dc("e,2,0,1.:r5,1,0,5'k:r4,1,o,40'k:r2,o,0,20'k:o,2,1,o"):{vo,io}
```
```field 9 Circuit Description
e1,2,0,1.
r5,1,0,5'k
r4,1,o,40'k
r2,o,0,20'k
o,2,1,o
```

::: only 9
The answers you want are `vo` and `io`, in **Results**.
:::

The answer, **{9.,.00065}**, is correct: v{{sub:o}} is 9V and i{{sub:o}} is
0.65mA

:::

::: problem Bo2's Figure 3.3 (Inverting)

Find the gain of the overall circuit, v{{sub:o}}/v{{sub:S}}.

::: figure assets/practice/bo2s-figure-3-3-inverting-4.jpg

:::

```sym 7
s\dc("e,2,0,vs:r1,2,1,r1:r2,1,o,r2:o,1,0,o"):vo/vs
```
```sym 8
s\dc("e,2,0,vs:r1,2,1,r1:r2,1,o,r2:o,1,0,o"):vo/vs
```
```field 9 Circuit Description
e1,2,0,vs
r1,2,1,r1
r2,1,o,r2
o,1,0,o
```

::: only 9
Ask **Evaluate** for:

```field 9 Evaluate
vo/vs
```
:::

We get **-r2/r1**, which is correct, as can be seen in the book's answer
above.

:::

::: problem AS2's Figure 5.10 (Inverting)

Find v{{sub:o}}.

::: figure assets/practice/as2s-figure-5-10-inverting-5.jpg

:::

```sym 7
s\dc("e,2,0,vi:r1,2,1,r1:rf,1,o,rf:o,0,1,o"):vo
```
```sym 8
s\dc("e,2,0,vi:r1,2,1,r1:rf,1,o,rf:o,0,1,o"):vo
```
```field 9 Circuit Description
e1,2,0,vi
r1,2,1,r1
rf,1,o,rf
o,0,1,o
```

::: only 9
The answer you want is `vo`, in **Results**.
:::

This problem is almost identical to the one above. The answer we get is
correct:

:::

::: problem AS2's Example 5.3 (Inverting)

If v{{sub:i}} is 0.5V, calculate the output voltage v{{sub:o}} and the
current in the 10’kΩ resistor.

::: figure assets/practice/as2s-example-5-3-inverting-6.jpg

:::

```sym 7
s\dc("e,2,0,.5:r1,2,1,10'k:rf,1,o,25'k:o,0,1,o"):{vo,ir1}
```
```sym 8
s\dc("e,2,0,.5:r1,2,1,10'k:rf,1,o,25'k:o,0,1,o"):{vo,ir1}
```
```field 9 Circuit Description
e1,2,0,.5
r1,2,1,10'k
rf,1,o,25'k
o,0,1,o
```

::: only 9
The answers you want are `vo` and `ir1`, in **Results**.
:::

The answer, **{-1.25,5.e**-**5}**, is correct.

:::

::: problem TR5's Exercise 4-11 (Inverting)

Find v{{sub:O}} when v{{sub:S}} is 2V, -4V and 6V. Notice the output of the
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
e1,1,0,vs
r1,1,2,10'k
r2,2,o,33'k
o,0,2,o
```

::: only 9
Ask **Evaluate** for:

```field 9 Evaluate
vo|vs=2.
vo|vs=-4.
vo|vs=6.
```
:::

The answer, **{-6.6,13.2,-19.8}**, is correct within the linear realm, but
since the output is constrained to no more than 15V or less than -15V, the
answer is v{{sub:O}}=**-15**V for v{{sub:S}} = 6V.

:::

::: problem AS2's Practice Problem 5.3 (Inverting)

Find the output voltage of the op amp (e.g. v{{sub:o}}) and calculate the
current through the feedback resistor (e.g. the 15’kΩ resistor).

::: figure assets/practice/as2s-practice-problem-5-3-inverting-8.jpg

:::

My answer below. Notice we used the m for milli in the value of the voltage
source.

```sym 7
s\dc("e,2,0,40'm:r1,2,1,5'k:rf,1,o,15'k:o,0,1,o"):approx({vo,irf})
```
```sym 8
s\dc("e,2,0,40'm:r1,2,1,5'k:rf,1,o,15'k:o,0,1,o"):approx({vo,irf})
```
```field 9 Circuit Description
e1,2,0,40'm
r1,2,1,5'k
rf,1,o,15'k
o,0,1,o
```

The answer, **{-.12,8.e**-**6}**, is correct.

:::

::: problem AS2's Example 5.4 (Inverting)

Determine v{{sub:o}}.

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
The answer you want is `vo`, in **Results**.
:::

The answer, **-6**, is correct.

:::

::: problem TR5's Example 4-14 (Inverting)

Find the input-output relationship of the circuit below.

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
e1,1,0,vs
r1,1,b,r1
r2,b,0,r2
r3,b,a,r3
r4,a,o,r4
o,0,a,o
rl,o,0,rl
```

However, since we are only interested in the ratio of the input to the
output, a smarter (and faster – as in 49 seconds instead of 55 seconds) way
to *symbulate* it is this:

```sym 7
s\dc("e,1,0,1:r1,1,b,r1:r2,b,0,r2:r3,b,a,r3:r4,a,o,r4:o,0,a,o:rl,o,0,1")
```
```sym 8
s\dc("e,1,0,1:r1,1,b,r1:r2,b,0,r2:r3,b,a,r3:r4,a,o,r4:o,0,a,o:rl,o,0,1")
```
```field 9 Circuit Description
e1,1,0,1
r1,1,b,r1
r2,b,0,r2
r3,b,a,r3
r4,a,o,r4
o,0,a,o
rl,o,0,1
```

When we evaluate `vo/v1`, both approaches get the same answer, shown left
below:

::: figure assets/practice/tr5s-example-4-14-inverting-11.png

:::

::: figure assets/practice/tr5s-example-4-14-inverting-12.jpg

:::

which is correct, as can be seen by comparing it to the book's answer, shown
right.

:::

::: problem AS2's Practice Problem 5.4a (Transresistance)

This is a current-to-voltage converter, also called a *transresistance
amplifier*. Find v{{sub:o}}/i{{sub:S}}.

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
Ask **Evaluate** for:

```field 9 Evaluate
vo/is
```
:::

The answer, **-r**, is correct.

:::

::: problem AS2's Practice Problem 5.4b (Transresistance)

This is another *transresistance amplifier*. Again, find
v{{sub:o}}/i{{sub:S}}.

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

Asking:

`expand(vo/is)`

gets **-r1\*r3/r2-r1-r3**, which is equivalent to the book's answer.

::: figure assets/practice/as2s-practice-problem-5-4b-transresistance-15.jpg

:::

:::

::: problem Bo2's Example 3.1 (Non-Inverting Amplifier)

Find v{{sub:o}}/v{{sub:1}}.

::: figure assets/practice/bo2s-example-3-1-non-inverting-amplifier-16.jpg

:::

```sym 7
s\dc("e,p,0,v2:r1,1,0,r1:r2,1,o,r2:o,p,1,o"):vo/v1
```
```sym 8
s\dc("e,p,0,v2:r1,1,0,r1:r2,1,o,r2:o,p,1,o"):vo/v1
```
```field 9 Circuit Description
e1,p,0,v2
r1,1,0,r1
r2,1,o,r2
o,p,1,o
```

::: only 9
Ask **Evaluate** for:

```field 9 Evaluate
vo/v1
```
:::

We get **1+r2/r1**, which is correct.

:::

::: problem AS2's Figure 5.16 (Non-Inverting Amplifier)

Find v{{sub:o}}.

::: figure assets/practice/as2s-figure-5-16-non-inverting-amplifier-17.jpg

:::

```sym 7
s\dc("e,2,0,vi:r1,0,1,r1:rf,1,o,rf:o,2,1,o"):vo
```
```sym 8
s\dc("e,2,0,vi:r1,0,1,r1:rf,1,o,rf:o,2,1,o"):vo
```
```field 9 Circuit Description
e1,2,0,vi
r1,0,1,r1
rf,1,o,rf
o,2,1,o
```

::: only 9
The answer you want is `vo`, in **Results**.
:::

We get the right answer (below), an expression equivalent to the book's
answer.

:::

::: problem TR5's Example 4-13 (Non-Inverting Amplifier)

Find Vo/Vs.

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
e1,1,0,vs
r1,1,2,r1
r2,2,0,r2
o,2,3,o
r3,o,3,r3
r4,3,0,r4
```

::: only 9
Ask **Evaluate** for:

```field 9 Evaluate
vo/vs
```
:::

which is correct, as can be seen by comparing it to the book's answer, shown
below:

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
e1,1,0,vs
r1,1,2,r1
r2,2,0,r2
```

::: only 9
Ask **Evaluate** for:

```field 9 Evaluate
v2/vs
```
:::

Which is correct for this part. Then, simulate the right half.

```sym 7
s\dc("e,2,0,1:o,2,3,o:r3,o,3,r3:r4,3,0,r4"):vo/v2
```
```sym 8
s\dc("e,2,0,1:o,2,3,o:r3,o,3,r3:r4,3,0,r4"):vo/v2
```
```field 9 Circuit Description
e1,2,0,1
o,2,3,o
r3,o,3,r3
r4,3,0,r4
```

::: only 9
Ask **Evaluate** for:

```field 9 Evaluate
vo/v2
```
:::

Which is correct for this part. The product of these two partial answers
produces the same expression shown above after the big simulation, and is the
right answer.

:::

::: problem AS2's Figure 5.17 (Voltage Follower)

Find v{{sub:o}}.

::: figure assets/practice/as2s-figure-5-17-voltage-follower-20.jpg

:::

```sym 7
s\dc("e,1,0,vi:o,1,o,o"):vo
```
```sym 8
s\dc("e,1,0,vi:o,1,o,o"):vo
```
```field 9 Circuit Description
e1,1,0,vi
o,1,o,o
```

::: only 9
The answer you want is `vo`, in **Results**.
:::

The answer, **vi**, is correct.

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
e1,1,0,1.5
rs,1,2,2'k
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **2** in the first and **0** in the second — the pair of terminals you are looking into.

The answer you want is `pmax`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
prL|L=1000
```
:::

The answers we get, **{2.8125e-4,2.5e-4}**, are correct. Now we simulate the
(a) circuit.

```sym 7
s\dc("e,1,0,1.5:rs,1,2,2'k:o,2,o,o:rl,o,0,1'k"):prL
```
```sym 8
s\dc("e,1,0,1.5:rs,1,2,2'k:o,2,o,o:rl,o,0,1'k"):prL
```
```field 9 Circuit Description
e1,1,0,1.5
rs,1,2,2'k
o,2,o,o
rl,o,0,1'k
```

::: only 9
The answer you want is `prL`, in **Results**.
:::

The answer,**.00225**, is correct. The explanation to the apparent paradox
that the load in (a) is drawing more power than the source in (b) seems able
to provide evaporates once we remember that the ideal op amp shown in the
schematic is only part of the truth: the real op amp has its own source of
power, which provides the difference.

:::

::: problem AS2's Example 5.5 (Inverting)

Find v{{sub:o}}.

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
The answer you want is `vo`, in **Results**.
:::

The answer, **-1**, is correct.

:::

::: problem AS2's Practice Problem 5.5 (Non-Inverting)

Calculate v{{sub:o}}.

::: figure assets/practice/as2s-practice-problem-5-5-non-inverting-24.jpg

:::

```sym 7
s\dc("e,1,0,3:r4,1,2,4'k:r8,2,0,8'k:r2,3,0,2'k:r5,3,o,5'k:o,2,3,o")
```
```sym 8
s\dc("e,1,0,3:r4,1,2,4'k:r8,2,0,8'k:r2,3,0,2'k:r5,3,o,5'k:o,2,3,o")
```
```field 9 Circuit Description
e1,1,0,3
r4,1,2,4'k
r8,2,0,8'k
r2,3,0,2'k
r5,3,o,5'k
o,2,3,o
```

The answer for `vo`, **7**, is correct.

:::

::: problem Bo2's Example 3.2 (Adder or Summing)

Find v{{sub:o}}.

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
The answer you want is `vo`, in **Results**.
:::

which is correct, as can be seen by comparing it to the book's answer, shown
below:

::: figure assets/practice/bo2s-example-3-2-adder-or-summing-26.jpg

:::

:::

::: problem AS2's Figure 5.21 (Adder or Summing)

Find v{{sub:o}}.

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
Ask **Evaluate** for:

```field 9 Evaluate
expand(vo)
```
:::

which is correct, as can be seen by comparing it to the book's answer, shown
below:

::: figure assets/practice/as2s-figure-5-21-adder-or-summing-28.jpg

:::

:::

::: problem AS2's Example 5.6 (Adder or Summing)

Find v{{sub:o}} and i{{sub:o}}.

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
The answers you want are `vo` and `io`, in **Results**.
:::

The answer, **{-8.,-.0048}**, is correct. Notice a current of 4.8mA is going
into the op amp.

:::

::: problem AS2's Practice Problem 5.6 (Adder or Summing)

Find v{{sub:o}} and i{{sub:o}}.

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
The answers you want are `vo` and `io`, in **Results**.
:::

The answer, **{-3.8,-.001425}**, is correct. Again, the current is going into
the op amp.

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

{{v7,8|Evaluating `vo` we get}}{{v9|`vo` is}} the correct answer, equivalent to the book's answer
above.

:::

::: problem TR5's Exercise 4-13 (Difference or Differential)

Find v{{sub:o}}.

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

{{v7,8|Evaluating `vo` we get}}{{v9|`vo` is}} **3** **v2** **– ** **4** **v1**, which is the correct
answer.

:::

::: problem AS2's Figure 5.24 (Difference or Differential)

Find v{{sub:o}}. (And keep it in the memory, for you will use it in the next
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
The answer you want is `vo`, in **Results**.
:::

This expression is equivalent to the book's answer, better formatted, shown
below:

::: figure assets/practice/as2s-figure-5-24-difference-or-differential-35.jpg

:::

:::

::: problem AS2's Figure 5.24 (Subtractor)

For the same circuit of the previous problem, find v{{sub:o}} when
R{{sub:1}}=R{{sub:2}} and R{{sub:3}}=R{{sub:4}}.

Since we already have the expression for vo stored in the memory, we only do
this:

```sym 7
expand(vo)|r2=r1 and r3=r4
```
```sym 8
expand(vo)|r2=r1 and r3=r4
```

The answer we get, **v2-v1**, is correct.

:::

::: problem AS2's Example 5.7 (Difference or Differential)

Design an op amp circuit with inputs v{{sub:1}} and v{{sub:2}} such that
v{{sub:o}} = -5v{{sub:1}} + 3v{{sub:2}}.

My solution follows. The problem statement is a fancy way to say: for the
same circuit of the previous problem, find what values of resistors you need
to use if you want to get an output v{{sub:o}} = -5v{{sub:1}} + 3v{{sub:2}}.
Although this is not strictly a Symbulator problem, I present it here because
it illustrates how Symbulator fits in such design problems.

First we take that part of v{{sub:o}} that is a factor of v{{sub:1}}, and
make it equal to -5. Thus:

```sym 7
Define v1=1:Define v2=0:expand(vo)=-5
```
```sym 8
Define v1=1:Define v2=0:expand(vo)=–5
```

We get **-r2/r1=-5**. Now make that part of v{{sub:o}} that is a factor of
v{{sub:2}} equal to 3. Thus:

```sym 7
Define v1=0:Define v2=1:expand(vo)=3
```
```sym 8
Define v1=0:Define v2=1:expand(vo)=3
```

We get **r2\*r4/(r1\*(r3+r4))+r4/(r3+r4)=3** Now, since you have two
equations, you can solve for two unknowns. Out of the four resistors whose
values you can decide upon, two can be whatever you want. The book recommends
you use R{{sub:1}} = 10’k and R{{sub:3}}=20’k. Now let's find the values for
the other two resistors, R{{sub:2}} and R{{sub:4}}.

```sym 7
solve(ans(1) and ans(2),{r2,r4})|r1=10000 and r3=20000
```
```sym 8
solve(ans(1) and ans(2),{r2,r4})|r1=10000 and r3=20000
```

The expression above assumes that ans(1) and ans(2) are pointing to the two
equations we found before. We get **r2=50000 and r4=20000**. This is correct.

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

{{v7,8|Evaluating `vo` gives us}}{{v9|`vo` is}} the desired output, **3\*v2-5\*v1**. The resistor
values are correct.

:::

::: problem AS2's Practice Problem 5.7 (Difference or Differential)

Design a difference amplifier with gain 4.

My solution follows. The problem statement, again, is just a fancy way to
say: for the same circuit of the previous problem, find what values of
resistors you need to use if you want to get an output v{{sub:o}} = **4**
(v{{sub:2}}-v{{sub:1}}), or in other terms, -4v{{sub:1}} + 4v{{sub:2}}. Same
as before.

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

This time the book asks that you use R{{sub:1}} = 10’k and R{{sub:3}} = 10’k.
So we do that.

```sym 7
solve(ans(1) and ans(2),{r2,r4})|r1=10000 and r3=10000
```
```sym 8
solve(ans(1) and ans(2),{r2,r4})|r1=10000 and r3=10000
```

We get **r2=40000 and r4=40000**, the correct values for the remaining
resistors.

:::

::: problem AS2's Practice Problem 5.8 (Instrumentation)

Find i{{sub:o}}.

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
The answer you want is `ir5`, in **Results**.
:::

In the schematic, the current i{{sub:o}} corresponds to `ir5`. The answer,
**2.e**-**6**, is correct.

:::

::: problem Bo2's Example 3.3 (Cascade)

Find v{{sub:o}} in terms of the conductances and the applied voltage
v{{sub:S}}.

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
e1,1,0,vs
r12,1,2,1/g1
r14,1,4,1/g2
r4o,4,o,1/g3
r2o,2,o,1/g4
r23,2,3,1/g
r34,3,4,1/g
o1,0,2,3
o2,0,4,o
```

{{v7,8|Evaluating `vo` we get}}{{v9|`vo` is}}:

which is correct, as can be seen by comparing it to the book's answer, shown
below:

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
e1,1,0,vs
r1,2,o,1/1
r2,1,2,1/2
r3,2,3,1/3
r4,4,0,1/4
r5,4,o,1/5
o1,0,2,3
o2,3,4,o
```

{{v7,8|Evaluating `vo` we get}}{{v9|`vo` is}}: -**.75 vs**, which is correct.

:::

::: problem AS2's Example 5.9 (Cascade)

Find v{{sub:o}} and i{{sub:o}}.

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
e1,1,0,20'm
o1,1,2,a
o2,a,b,o
ro,o,b,10'k
r4,b,0,4'k
r2,a,2,12'k
r3,2,0,3'k
```

{{v7,8|Evaluating `approx({vo,iro})` we get the answer, **{.35,2.5e-5}**.}}{{v9|`vo` is **.35** and `iro` is **2.5e-5**.}} This is
correct.

:::

::: problem AS2's Practice Problem 5.9 (Cascade)

Determine v{{sub:o}} and i{{sub:o}}.

::: figure assets/practice/as2s-practice-problem-5-9-cascade-42.jpg

:::

```sym 7
s\dc("e,1,0,4:o1,1,2,2:o2,2,3,o:ro,3,0,4'k:r6,3,o,6'k"):{vo,iro}
```
```sym 8
s\dc("e,1,0,4:o1,1,2,2:o2,2,3,o:ro,3,0,4'k:r6,3,o,6'k"):{vo,iro}
```
```field 9 Circuit Description
e1,1,0,4
o1,1,2,2
o2,2,3,o
ro,3,0,4'k
r6,3,o,6'k
```

::: only 9
The answers you want are `vo` and `iro`, in **Results**.
:::

The answer, **{10,1/1000}**, is correct. To say a 1/1000 A current is the
same as 1mA.

:::

::: problem AS2's Practice Problem 5.10 (Cascade)

If v{{sub:1}} = 2V and v{{sub:2}} = 1.5V, find v{{sub:o}} in the circuit
below.

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
The answer you want is `vo`, in **Results**.
:::

The answer, **9**. , is correct.

:::

::: problem TR5's Example 4-16 (Cascade)

Derive an expression for v{{sub:o}} in terms of the two inputs.

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
Ask **Evaluate** for:

```field 9 Evaluate
expand(vo)
```
:::

The answer, **-2.4** **v1 – 6**, is correct.

:::

::: problem TR5's Exercise 4-14 (Cascade)

Derive an expression for v{{sub:o}} in terms of the inputs v{{sub:1}} and
v{{sub:2}}.

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
Ask **Evaluate** for:

```field 9 Evaluate
expand(vo)
```
:::

The answer, **8 v1 – 4 v2**, is correct.

:::

::: problem AS2's Example 5.10 (Cascade)

If v{{sub:1}} = 1V and v{{sub:2}} = 2V, find v{{sub:o}} in the circuit below.

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

The answer, **8.667**, is correct.

:::

::: problem TR5's Example 4-17 (Cascade)

Derive an expression for v{{sub:o}} in terms of the inputs v{{sub:1}} and
v{{sub:2}}.

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
The answer you want is `vo`, in **Results**.
:::

We get the right answer. Let's compare it with the book's answer, which is
below:

::: figure assets/practice/tr5s-example-4-17-cascade-48.jpg

:::

Our answer, expanded via `expand(vo)`, is shown below:

Playing with it by hand we get a form that, in my opinion, is *prettier* ;-)
than the book's:

:::

::: problem TR5's Example 4-18 (Multiple)

Derive an expression for v{{sub:o}} in terms of the inputs v{{sub:1}} and
v{{sub:2}}.

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

This is exactly the answer from the book:

::: figure assets/practice/tr5s-example-4-18-multiple-50.jpg

:::

If you are ever in doubt about whether two expressions are the same,
{{v7,8|enter them both, separately, into the calculator, and then ask the
calculator to compare them using the equality sign. If the answer is
'**true**', then they are the same.}}{{v9|subtract one from the other in
**Evaluate**. If the answer is `0`, they are the same — an equality sign
would only be read as a comparison to solve, not as a question about
sameness.}}

:::

::: only 9
::: note Some of this narration still describes the calculator
Every problem below carries a **Circuit Description** panel you can type
straight into Symbulator 9, and the circuits and answers are identical
across the versions. What has not all been rewritten is the narration
between them: where it says to evaluate a name or press a key, do the
version 9 equivalent — the results are already on screen, and
{{ref:introduction}} lists the correspondences.
:::
:::
:::
