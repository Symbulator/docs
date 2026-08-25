---
id: lesson-sources
kind: lesson
title: Current sources, conductances and dependent sources
updated: 2023-07-08
summary: >
  Learn how to describe a *current source* using the **j** element. Simplify
  *parallel resistors* using the **pr** tool and its shorthand. Learn to
  describe *conductances* and *dependent sources*.
---

In this lesson you will learn how to describe a *current source* using the
**j** element, and a trick to simplify *parallel resistors* using the **pr**
tool or its shorthand. You will also learn how to describe *conductance* and
*dependent sources* in Symbulator using elements you already know.

## How to describe a current source {#describe-current-source}

::: note Describing current sources
In Symbulator, an ideal current source is described with four pieces of
information, separated by commas: a unique name to identify the current source
(which must start with the letter **j**), the names of the first and second
node of the source, and the value of the source in amperes (A). The value
should be given in terms of the current flowing through the source from the
first node towards the second node. This means that the value of the source is
how much current leaves the source out of the second node, and also how much
current enters the source's first node.

For example, an ideal current source called **j1**, connected between two nodes
called **0** and **3**, with a current of **5** A running through it from the
first node to the second node, would be described as follows:
`j1,0,3,5`{{i:current source}}
:::

You can use SI prefixes here as well. The value of a current source is often
given in milliamps; Symbulator will interpret any `'m` given in the value as a
division by a thousand.

### Answers for a current source

For each current source included in the circuit description, you get the same
answers you would get for a voltage source, using the same polarity
conventions: the voltage drop in it, the current through it, the power consumed
by it (for the delivered power, ask for the negative), and the equivalent
resistance of the rest of the circuit as seen by that source.

Let's see an example.

::: problem B11's Example 8.1
Given the circuit below, determine the current and voltage drop in R1.

::: figure assets/circuit/b11e0801.jpg
B11's Example 8.1
:::

::: answer
We ask Symbulator to run a DC simulation of the circuit described between
quotations:

```sym 7
s\dc("j,0,1,10'm:r1,1,0,20'k")
```
```sym 8
s\dc("j,0,1,10'm:r1,1,0,20'k")
```
```field 9 Circuit Description
j,0,1,10'm
r1,1,0,20'k
```

::: only 9
Two lines, two elements. Under **Type of analysis** leave *Solve circuit*, set
**Analysis** to *DC — direct current*, and click **Run Symbulator**. This is a
numerical circuit, so it is worth putting **Rounding** back to *approximate to
n significant digits* with **n** = 3 and ticking **Use SI prefixes**, as in
{{ref:lesson-dc}}.
:::

{{v7,8|We ask for the values of two variables, `ir1` and `vr1`. We get `.01`
and `200.`, meaning}}{{v9|The `r1` block gives both answers at once:
`ir1` = 10 mA on the **current through** line, and
`vr1` = 200 V on the **voltage drop** line — that is}} a 10 mA
current and a 200 V voltage drop.
:::
:::

## What about conductances? {#conductances}

Conductances are really resistors by another name.{{i:conductance}} So, we
describe them as resistors, using the element **r**, and we enter as the value
the inverse of the conductance: one divided by the value of the conductance
gives you the value of the resistor in Ω.

The following example is taken from the textbook *Elementary Linear Circuit
Analysis* (2ed) by Leonard S. Bobrow. From this point forward, I will refer to
this book as **Bo2**.

::: problem Bo2's Example 2.2
Given the circuit below, determine the voltages in the nodes.

::: figure assets/circuit/bo2e0202.jpg
Bo2's Example 2.2
:::

::: answer
As I explained before, in Symbulator all conductances are simulated as
resistors. So, the 4 siemens conductance becomes a 1/4 resistor, and so on.
Below is my description:

```sym 7
s\dc("j10,1,0,2:r12,1,2,1:r20,2,0,1/4:r30,3,0,1/3:r13,1,3,1/2:j32,3,2,3")
```
```sym 8
s\dc("j10,1,0,2:r12,1,2,1:r20,2,0,1/4:r30,3,0,1/3:r13,1,3,1/2:j32,3,2,3")
```
```field 9 Circuit Description
j10,1,0,2
r12,1,2,1
r20,2,0,1/4
r30,3,0,1/3
r13,1,3,1/2
j32,3,2,3
```

{{v7,8|We ask for these answers:}}{{v9|Run it in DC. The answers are the first
thing on the page, under **Node voltages**:}}

```sym 7
approx({v1,v2,v3})
```
```sym 8
approx({v1,v2,v3})
```
```out 7,8
{–1.3, .34, –1.12}
```

That indicates v1 = –1.3 V, v2 = .34 V, v3 = –1.12 V. This is correct.
:::
:::

## How to reduce parallel resistors {#parallel-resistors}

::: only 7,8
Symbulator has a way to help you reduce resistors connected in parallel to
their equivalent. It is a function called **pr**,{{i:pr tool}} and you can use
it either on its own or as part of circuit descriptions. Furthermore, to save
you some typing, you can invoke it on the fly using a shorthand.

### Using s\pr({r,r,r…})

When you do not need to know the current through, or the power consumed by,
each individual resistor, you can reduce any number of resistors in parallel to
a single equivalent value. You do this by invoking the **s\pr** function, and
giving it a list of resistance values separated by commas.

For example, to reduce three resistors in parallel with values of 10 Ω, 20 Ω
and 30 Ω:

```sym 7
s\pr({10,20,30})
```
```sym 8
s\pr({10,20,30})
```

You get 60/11 if you evaluate exactly, or 5.45 approximately.

You can also give symbolic values. For example, to reduce four resistors in
parallel with values r1, r2, r3 and r4:

```sym 7
s\pr({r1,r2,r3,r4})
```
```sym 8
s\pr({r1,r2,r3,r4})
```

You get the answer as a symbolic expression.

You can use the s\pr tool as part of a circuit description or on its own, on
the entry line, outside of Symbulator. This is useful because sometimes you may
not even need to run a simulation to find the answer to a problem which is
basically a resistor reduction problem.

### Reducing series and parallel combos

A similar reduction of resistors in series is possible through simple addition,
whenever we do not need to know specific answers for each resistor, such as the
voltage drop or power consumed in each, or the voltage in the node between
them. The current through series resistors is the same, so even through an
equivalent you can get the current.

::: problem AS7's Example 2.10
Find the equivalent resistance.

::: figure assets/circuit/as7e0210.png
AS7's Example 2.10
:::

::: answer
We don't need to run a simulation to find this answer. We can find it by typing
this on the entry line:

```sym 7
10+s\pr({3,6,1+s\pr({12,4,1+5})})
```
```sym 8
10+s\pr({3,6,1+s\pr({12,4,1+5})})
```

We evaluate approximately and get 11.2 Ω. This is correct.
:::
:::

::: problem AS7's Practice Problem 2.10
Find the equivalent resistance.

::: figure assets/circuit/as7pp0210.png
AS7's Practice Problem 2.10
:::

::: answer
Again, no simulation is needed:

```sym 7
16+s\pr({18,9,2+s\pr({20,1+s\pr({5,20})})})
```
```sym 8
16+s\pr({18,9,2+s\pr({20,1+s\pr({5,20})})})
```

We evaluate and get 19 Ω. This is correct.
:::
:::

### The [r,r,r…] shorthand for descriptions

It may not be too practical to have to type `s\pr({})` while you describe the
circuit. So, to make it easier to call for the reduction of parallel resistors
on the fly, I have added a shorthand. Symbulator will recognise any values
inside square brackets, such as `[10,20,30]` or `[r1,r2,r3,r4]`, as input to be
passed to the s\pr function. This shorthand only works within the circuit
description that is passed to Symbulator, and will not work outside of it.

### When to reduce resistors

A simulation where it makes sense to use pr is B11's Example 7.4, which you saw
in the practice problems of {{ref:lesson-dc}}. It makes sense to reduce R4 and
R5 to an equivalent resistor, since we do not need to know their individual
currents or power use:

```sym 7
s\dc("e,1,0,16.8:r1,1,2,9:r2,1,2,6:r3,2,3,4:re,3,0,[6,3]:r6,2,0,3")
```
```sym 8
s\dc("e,1,0,16.8:r1,1,2,9:r2,1,2,6:r3,2,3,4:re,3,0,[6,3]:r6,2,0,3")
```
An example where using pr makes no sense is B11's Example 8.3, because you need
to know the value of the current through R1.

Finally, a simulation where you can reduce part of the resistors is B11's
Example 6.22. We must leave R1 alone, because we need the current through it,
but we can reduce R2 and R3:

```sym 7
s\dc("jt,0,1,12'm:r1,1,0,1'k:re,1,0,[10'k,22'k]")
```
```sym 8
s\dc("jt,0,1,12'm:r1,1,0,1'k:re,1,0,[10'k,22'k]")
```
Moving forward, we will use the `pr({,,})` tool, or its shorthand `[,,]`, in
circuit descriptions whenever we feel it is appropriate.
:::

::: only 9
Symbulator 9 has the same tool, spelled `pr`, and you can use it in two
places.{{i:parallel resistors}}

Inside a circuit description, write it where a value goes — that is what the
`re,3,0,[6,3]` shorthand below does, and `pr(6,3)` means the same thing.

On its own, type it into the **Evaluate** card. It nests as deeply as you like:

```field 9 Evaluate
16 + pr(18, 9, 2 + pr(20, 1 + pr(5, 20)))
```

Press **Evaluate** and you get **19**.

It works on symbols as readily as on numbers, so `pr(r1, r2)` evaluates to
$r1 r2/(r1 + r2)$ — useful when the resistors in your circuit are still
unknowns.

### The [r,r,r…] shorthand for descriptions

It may not be too practical to have to call `pr()` separately while you
describe the circuit. So, to make it easier to call for the reduction of
parallel resistors on the fly, there is a shorthand: Symbulator will recognise
any values inside square brackets, such as `[10,20,30]` or `[r1,r2,r3,r4]`, as
input to be passed to `pr`. This shorthand only works within the circuit
description that is passed to Symbulator, and will not work outside of it.

### When to reduce resistors

A simulation where it makes sense to use pr is B11's Example 7.4, which you saw
in the practice problems of {{ref:lesson-dc}}. It makes sense to reduce R4 and
R5 to an equivalent resistor, since we do not need to know their individual
currents or power use:

```field 9 Circuit Description
e1,1,0,16.8
r1,1,2,9
r2,1,2,6
r3,2,3,4
re1,3,0,[6,3]
r6,2,0,3
```

Run it in DC, then ask **Evaluate** for `-ie`, the current the source
delivers. The answer is **3 A**.

An example where using pr makes no sense is B11's Example 8.3, because you need
to know the value of the current through R1.

Finally, a simulation where you can reduce part of the resistors is B11's
Example 6.22. We must leave R1 alone, because we need the current through it,
but we can reduce R2 and R3:

```field 9 Circuit Description
jt,0,1,12'm
r1,1,0,1'k
re,1,0,[10'k,22'k]
```

Moving forward, we will use the `pr(,,)` tool, or its shorthand `[,,]`, in
circuit descriptions whenever we feel it is appropriate.

::: note Reduce only what you don't need to see
The reason to reduce resistors at all is speed, and the cost is information:
once two resistors become one, you can no longer ask for the current through,
or the power consumed by, either of them individually. Reduce only the ones the
problem does not ask about.
:::

::: note One difference worth knowing
Where a hand-rolled `1 / sum(1/v for v in values)` would divide by zero,
Symbulator's `pr` checks for it: if any of the values you give it is exactly
zero, the combination is zero, because a short circuit across a parallel
network wins. The calculator tool did the same.
:::
:::

## How to describe dependent sources {#dependent-sources}

One of my favourite scenes in cinema comes from *The Dark Knight*: the Joker,
played masterfully by Heath Ledger, is rolling on the floor of a Gotham City
prison, taking a bare-knuckle beating from an ever-more-frustrated Batman.
Master of the situation and laughing hysterically, the Joker says: *"You have
nothing! Nothing to threaten me with!"*

Even though the movie had not been made yet, I remember feeling something along
the same lines — although maybe less hysterical — back in 1999, when I realised
that one of the consequences of having used a 100% symbolic implementation for
Symbulator was that I could make any element's value dependent on any answer of
the circuit. I could simulate voltage or current sources that were dependent on
any voltage, current or combination thereof, with the same ease that I could
simulate a 12 V source.

Here is what you need to know for simulating dependent
sources{{i:dependent source}} in Symbulator: nothing. There is nothing special
to it, nothing at all. Just write the value as a function of the circuit's
answers, using the variables that by now you should know well, and run the
simulation like it's nobody's business. For example:

::: only 7,8
- if the source depends on the current through a resistor called r1, you define
  its value as `ir1`
- if the source depends on the voltage drop in a resistor called r2, you define
  its value as `vr2`
- if the source depends on the current through a short called s3, you define
  its value as `is3`
- if the source depends on the difference between the voltage of two nodes a
  and b, you define its value as `va-vb`
:::
::: only 9
- if the source depends on the current through a resistor called r1, you define
  its value as `ir1`
- if the source depends on the voltage drop in a resistor called r2, you define
  its value as `vr2`
- if the source depends on the current through a short called s3, you define
  its value as `is3`
- if the source depends on the difference between the voltage of two nodes a
  and b, you define its value as `va-vb`
:::

With Symbulator, instead of fearing them, you will laugh in the face of
dependent sources, thinking: *"You have nothing!"* Booyah!

::: tip Dependent sources are just sources
For Symbulator, dependent sources are just sources and require no special
notation. When you declare their value, just state the expression that
describes it, using variables Symbulator knows and paying attention to their
polarity, and you are off to the races.
:::

## Instructive solved examples {#practice-sources}

::: practice


### Circuits with E, J and R

::: problem B11's Example 8.2

Determine the values of V{{sub:S}}, I{{sub:1}} and I{{sub:2}}.

::: figure assets/practice/b11s-example-8-2-1.jpg

:::

In the line below, we concatenate three commands using colons. The first
stores the circuit's definition in a variable. The second asks Symbulator to
run a DC simulation of the circuit described in that variable. The third asks
the calculator to provide us the values of three variables that – given the
circuit description – answer the questions.

```sym 7
s\dc("j,0,1,7:e,1,0,12:r1,1,0,4"):
{v1,ie,ir1}
```
```sym 8
s\dc("j,0,1,7:e,1,0,12:r1,1,0,4"):
{v1,ie,ir1}
```
```field 9 Circuit Description
j,0,1,7
e1,1,0,12
r1,1,0,4
```

::: only 9
The answers you want are `v1`, `ie` and `ir1`, in **Results**.
:::

The calculator returns **{12,4,3}**, meaning V{{sub:S}} is 12V, I{{sub:1}} is
4A and I{{sub:2}} is 3A. These are the correct answers. We will continue to
use the single line instruction as we move on.

:::

::: problem B11's Example 8.15

Determine the current through each resistor. My solution below, direction in
blue:

::: figure assets/practice/b11s-example-8-15-2.jpg

:::

```sym 7
s\dc("j6,0,1,6:r2,1,0,2:r6,1,2,6:r8,0,2,8:j8,2,0,8"):
approx({ir2,ir6,ir8})
```
```sym 8
s\dc("j6,0,1,6:r2,1,0,2:r6,1,2,6:r8,0,2,8:j8,2,0,8"):
approx({ir2,ir6,ir8})
```
```field 9 Circuit Description
j6,0,1,6
r2,1,0,2
r6,1,2,6
r8,0,2,8
j8,2,0,8
```

::: only 9
The answers you want are `ir2`, `ir6` and `ir8`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

We get these answers: **{1.25,4.75,3.25}**. So I{{sub:R2}} is 1.25A,
I{{sub:R6}} is 4.75A, and I{{sub:R8}} is 3.25A.

:::

::: problem B11's Example 8.21

::: figure assets/practice/b11s-example-8-21-3.jpg

:::

Determine the voltage in each node and the current through each resistor.

My solution below:

```sym 7
s\dc("j1,0,1,4:r1,1,0,2:r3,1,2,12:r2,0,2,6:j2,2,0,2"):
{v1,v2,ir1,ir2,ir3}
```
```sym 8
s\dc("j1,0,1,4:r1,1,0,2:r3,1,2,12:r2,0,2,6:j2,2,0,2"):
{v1,v2,ir1,ir2,ir3}
```
```field 9 Circuit Description
j1,0,1,4
r1,1,0,2
r3,1,2,12
r2,0,2,6
j2,2,0,2
```

::: only 9
The answers you want are `v1`, `v2`, `ir1`, `ir2` and `ir3`, in **Results**.
:::

We get the following answers: **{6,-6,3,1,1}**. So V{{sub:1}}=6V,
V{{sub:2}}=-6V, I{{sub:R1}}=3A, and I{{sub:R2}}=I{{sub:R3}}=1A.

:::

::: problem Bo2's Drill Exercise 2.2 (Conductances)

Given the circuit below, determine the voltages in the nodes.

::: figure assets/practice/bo2s-drill-exercise-2-2-conductances-4.jpg

:::

Below my solution:

```sym 7
s\dc("r10,1,0,1/3:r12,1,2,1/2:r13,1,3,1/2:r23,2,3,1/6:
r20,2,0,1/8:j12,1,2,17:j03,0,3,2"):approx({v1,v2,v3})
```
```sym 8
s\dc("r10,1,0,1/3:r12,1,2,1/2:r13,1,3,1/2:r23,2,3,1/6:
r20,2,0,1/8:j12,1,2,17:j03,0,3,2"):approx({v1,v2,v3})
```
```field 9 Circuit Description
r10,1,0,1/3
r12,1,2,1/2
r13,1,3,1/2
r23,2,3,1/6
r20,2,0,1/8
j12,1,2,17
j03,0,3,2
```

::: only 9
The answers you want are `v1`, `v2` and `v3`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

The answer, **{-2.,1.,.5}**, indicates v{{sub:1}}=-2V, v{{sub:2}}=1V,
v{{sub:3}}=0.5V. This is correct.

:::

::: problem HK5's Figure 1-24b (Expert)

Determine *i*{{sub:x}} and *v*{{sub:x}} in the following circuit.

::: figure assets/practice/hk5s-figure-1-24b-expert-5.jpg

:::

My solution below:

```sym 7
s\ex("j6,0,1,6:r5,1,2,5:r2,2,0,2:r1,1,3,1:
r3,0,4,3:j10,2,3,10:rx,3,4,rx"):{ir1,vrx}
```
```sym 8
s\ex("j6,0,1,6:r5,1,2,5:r2,2,0,2:r1,1,3,1:
r3,0,4,3:j10,2,3,10:rx,3,4,rx"):{ir1,vrx}
```
```field 9 Circuit Description
j6,0,1,6
r5,1,2,5
r2,2,0,2
r1,1,3,1
r3,0,4,3
j10,2,3,10
rx,3,4,rx
```

::: only 9
Set **Analysis** to *DC — direct current*. This one needs **Enable Expert Mode** ticked in **Settings**; the equations and unknowns go in the boxes it reveals.

The answers you want are `ir1` and `vrx`, in **Results**.
:::

Select DC. Add equation `ir2=4`. Add unknown `rx`. Run the simulation. The
answer, **{-8,80}**, means that I{{sub:X}} is -8A and that V{{sub:X}} is 80V.

:::

::: problem HK5's Example 2.2 (Conductances)

Determine the voltages in the nodes. My solution below:

::: figure assets/practice/hk5s-example-2-2-conductances-6.jpg

:::

```sym 7
s\dc("j01,0,1,-8:j30,3,0,-25:j21,2,1,-3:r12,1,2,1/3:r23,2,3,1/2:r13,1,3,1/4:r20,2,0,1:r30,3,0,1/5"):{v1,v2,v3}
```
```sym 8
s\dc("j01,0,1,–8:j30,3,0,–25:j21,2,1,–3:r12,1,2,1/3:r23,2,3,1/2:r13,1,3,1/4:r20,2,0,1:r30,3,0,1/5"):{v1,v2,v3}
```
```field 9 Circuit Description
j01,0,1,-8
j30,3,0,-25
j21,2,1,-3
r12,1,2,1/3
r23,2,3,1/2
r13,1,3,1/4
r20,2,0,1
r30,3,0,1/5
```

::: only 9
The answers you want are `v1`, `v2` and `v3`, in **Results**.
:::

The answer, **{1,2,3}**, is correct: v{{sub:1}}=1V, v{{sub:2}}=2V,
v{{sub:3}}=3V.

:::

::: problem B11's Example 8.5

Determine the current I{{sub:2}} in the circuit shown below. My solution is
below the circuit.

::: figure assets/practice/b11s-example-8-5-7.jpg

:::

```sym 7
s\dc("j1,1,0,4:r1,1,0,3:e2,1,2,5:r2,0,2,2"):approx(ir2)
```
```sym 8
s\dc("j1,1,0,4:r1,1,0,3:e2,1,2,5:r2,0,2,2"):approx(ir2)
```
```field 9 Circuit Description
j1,1,0,4
r1,1,0,3
e2,1,2,5
r2,0,2,2
```

This gives us a value for I{{sub:2}} of **3.4** A. This is correct.

:::

::: problem Bo2's Example 2.5 (Conductances)

::: figure assets/practice/bo2s-example-2-5-conductances-8.jpg

:::

Determine the voltages in the nodes, and the current through the voltage
source.

```sym 7
s\dc("j,0,1,3:e,3,2,3:r12,1,2,1/7:r20,2,0,1/3:r30,3,0,1/5:r13,1,3,1/2"):
approx({v1,v2,v3,-ie})
```
```sym 8
s\dc("j,0,1,3:e,3,2,3:r12,1,2,1/7:r20,2,0,1/3:r30,3,0,1/5:r13,1,3,1/2"):
approx({v1,v2,v3,–ie})
```
```field 9 Circuit Description
j,0,1,3
e1,3,2,3
r12,1,2,1/7
r20,2,0,1/3
r30,3,0,1/5
r13,1,3,1/2
```

::: only 9
The answers you want are `v1`, `v2` and `v3`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
-ie
```

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

The answer, **{-.5,-1.5,1.5,11.5}**, is correct: v{{sub:1}}=-.5,
v{{sub:2}}=-1.5, v{{sub:3}}=1.5, i=11.5

:::

::: problem B11's Example 8.22

Determine V{{sub:1}} and V{{sub:2}}. My solution below:

::: figure assets/practice/b11s-example-8-22-9.jpg

:::

```sym 7
s\dc("j1,0,1,6:r1,1,0,4:e,1,2,12:r3,1,2,10:r2,2,0,2:j2,2,0,4"):
approx({v1,v2})
```
```sym 8
s\dc("j1,0,1,6:r1,1,0,4:e,1,2,12:r3,1,2,10:r2,2,0,2:j2,2,0,4"):
approx({v1,v2})
```
```field 9 Circuit Description
j1,0,1,6
r1,1,0,4
e1,1,2,12
r3,1,2,10
r2,2,0,2
j2,2,0,4
```

::: only 9
The answers you want are `v1` and `v2`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

The answer, **{10.67,-1.33}**, tells us that V{{sub:1}} is 10.67V and
V{{sub:2}} is -1.33V.

:::

::: problem B11's Example 8.19

Determine V{{sub:1}}, I{{sub:1}} and I{{sub:2}}, in the circuit below:

::: figure assets/practice/b11s-example-8-19-10.jpg

:::

My solution below:

```sym 7
s\dc("e,2,0,24:r1,1,2,6:r2,1,0,12:j,0,1,1"):approx({v1,ir1,ir2})
```
```sym 8
s\dc("e,2,0,24:r1,1,2,6:r2,1,0,12:j,0,1,1"):approx({v1,ir1,ir2})
```
```field 9 Circuit Description
e1,2,0,24
r1,1,2,6
r2,1,0,12
j,0,1,1
```

The answer, **{20.,-.667,1.67}**, tells us that V{{sub:1}} is 20V, I{{sub:1}}
is -.667A and I{{sub:2}} is 1.67V.

:::

::: problem B11's Example 8.14

::: figure assets/practice/b11s-example-8-14-11.jpg

:::

Determine I{{sub:2}} and I{{sub:3}}.

```sym 7
s\dc("e1,1,0,20:r1,1,2,6:r2,2,a,4:j,a,0,4:r3,a,3,2:e2,0,3,12"):
approx({ir2,ir3})
```
```sym 8
s\dc("e1,1,0,20:r1,1,2,6:r2,2,a,4:j,a,0,4:r3,a,3,2:e2,0,3,12"):
approx({ir2,ir3})
```
```field 9 Circuit Description
e1,1,0,20
r1,1,2,6
r2,2,a,4
j,a,0,4
r3,a,3,2
e2,0,3,12
```

::: only 9
The answers you want are `ir2` and `ir3`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

Answer: **{3.33,-.666}**. This is correct.

:::

::: problem B11's Example 8.20

Determine V{{sub:1}}, V{{sub:2}}, , I{{sub:1}}, I{{sub:2}} and I{{sub:3}}. My
solution is found below the circuit schematic:

::: figure assets/practice/b11s-example-8-20-12.jpg

:::

```sym 7
s\dc("e,3,0,64:r1,3,1,8:r2,1,2,4:j,1,2,2:r3,2,0,10"):
approx({v1,v2,ir1,ir2,ir3})
```
```sym 8
s\dc("e,3,0,64:r1,3,1,8:r2,1,2,4:j,1,2,2:r3,2,0,10"):
approx({v1,v2,ir1,ir2,ir3})
```
```field 9 Circuit Description
e1,3,0,64
r1,3,1,8
r2,1,2,4
j,1,2,2
r3,2,0,10
```

::: only 9
The answers you want are `v1`, `v2`, `ir1`, `ir2` and `ir3`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

Answer: **{37.82,32.73,3.27,1.27,3.27}**. You should know how to read these
by now, but here it is just in case: V{{sub:1}} = 37.82V, V{{sub:2}} =
32.73V, I{{sub:1}} = 3.27A, I{{sub:2}} = 1.27A, I{{sub:3}} = 3.27A.

:::

::: problem RM3's Example 9-12 (*solve*)

If R{{sub:3}} is to be replaced with R{{sub:4}} and I{{sub:4}}, determine the
value and direction of the source.

::: figure assets/practice/rm3s-example-9-12-solve-13.jpg

:::

So that we can keep the name of node b, we will use the top left node as
reference.

First, make sure you understand what this problem is asking you to do. The
idea is that, despite the change, we keep the same voltage drop and current
flow between nodes **a** and **b**. We must first know what they are. So we
simulate the original circuit:

```sym 7
s\dc("e,0,b,20:r1,0,a,16:r2,a,b,40:r3,a,b,60"):{va-vb,ir3}
```
```sym 8
s\dc("e,0,b,20:r1,0,a,16:r2,a,b,40:r3,a,b,60"):{va-vb,ir3}
```
```field 9 Circuit Description
e1,0,b,20
r1,0,a,16
r2,a,b,40
r3,a,b,60
```

::: only 9
The answer you want is `ir3`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
va-vb
```
:::

We find that the voltage drop is 12V and the current is 0.2A. These are the
currents and voltages that we have to keep once we do the replacement.
Simulate the circuit now replacing R{{sub:3}} with a resistor R{{sub:4}} of
240Ω and a source **j** with value I{{sub:4}}. Run this:

```sym 7
s\dc("e,0,b,20:r1,0,a,16:r2,a,b,40:r4,a,b,240:j,a,b,i4")
```
```sym 8
s\dc("e,0,b,20:r1,0,a,16:r2,a,b,40:r4,a,b,240:j,a,b,i4")
```
```field 9 Circuit Description
e1,0,b,20
r1,0,a,16
r2,a,b,40
r4,a,b,240
j,a,b,i4
```

Notice that both the voltage drop (given by va-vb) and the current (given by
`ir4+ij`) are algebraic functions in terms of i4. Now you can find i4 solving
by voltage drop:

::: only 9
Both routes go in the **Solve** card, which solves against the answers the
circuit just produced:

```field 9 Equation
v_a-v_b = 12
```

with `i4` as the unknown — or `i_r4+i_j = 0.2` for the same answer by
current instead.
:::

```sym 7
solve(va-vb=12.,i4)       …or by current flow…       solve(ir4+ij=0.2,i4)
```
```sym 8
solve(va-vb=12.,i4)       …or by current flow…       solve(ir4+ij=0.2,i4)
```

The result is the same: i4 = **.15** A The required current source is .15A
from **a** to **b**.

:::

::: problem RM3's Example 8-13

Solve for the currents through R{{sub:2}} and R{{sub:3}} in the circuit
shown. My solution is below:

::: figure assets/practice/rm3s-example-8-13-14.jpg

:::

```sym 7
s\dc("r1,a,0,10'k:r2,1,0,5'k:r3,b,a,6'k:r4,0,2,16'k:
j,a,b,2'm:e1,1,b,10:e2,b,2,8"):approx({ir2,ir3})
```
```sym 8
s\dc("r1,a,0,10'k:r2,1,0,5'k:r3,b,a,6'k:r4,0,2,16'k:
j,a,b,2'm:e1,1,b,10:e2,b,2,8"):approx({ir2,ir3})
```
```field 9 Circuit Description
r1,a,0,10'k
r2,1,0,5'k
r3,b,a,6'k
r4,0,2,16'k
j,a,b,2'm
e1,1,b,10
e2,b,2,8
```

::: only 9
The answers you want are `ir2` and `ir3`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

The answer, **{.00154,.00111}** is correct: I{{sub:R2}} = 1.54 mA and
I{{sub:R3}} = 1.11 mA.

:::

::: problem B11's Example 6.3 (Hidden source)

Determine V{{sub:S}} and I{{sub:1}}.

::: figure assets/practice/b11s-example-6-3-hidden-source-15.jpg

:::

The problem presents a seemingly ‘hanging' node with 20V. To simulate this,
imagine a ‘hidden' 20V voltage source connected to the node.

```sym 7
s\dc("j,0,1,6:r1,1,2,2:r2,1,2,1:e,2,0,20"):
{v1,ir1}
```
```sym 8
s\dc("j,0,1,6:r1,1,2,2:r2,1,2,1:e,2,0,20"):
{v1,ir1}
```
```field 9 Circuit Description
j,0,1,6
r1,1,2,2
r2,1,2,1
e1,2,0,20
```

::: only 9
The answers you want are `v1` and `ir1`, in **Results**.
:::

We get the answer: **{24,2}**, which is correct. V{{sub:S}} is **24**V and
I{{sub:1}} is **2**A.

:::

::: problem HK5's Figure 1-24c (Expert)

Determine *i*{{sub:x}} and *v*{{sub:x}} in the following circuit.

::: figure assets/practice/hk5s-figure-1-24c-expert-16.jpg

:::

```sym 7
s\ex("e,1,0,60:r8,1,2,8:r10,2,0,10:r4,2,3,4:r2,3,0,2:j,0,3,ix"):
{ix,v3}
```
```sym 8
s\ex("e,1,0,60:r8,1,2,8:r10,2,0,10:r4,2,3,4:r2,3,0,2:j,0,3,ix"):
{ix,v3}
```
```field 9 Circuit Description
e1,1,0,60
r8,1,2,8
r10,2,0,10
r4,2,3,4
r2,3,0,2
j,0,3,ix
```

::: only 9
Set **Analysis** to *DC — direct current*. This one needs **Enable Expert Mode** ticked in **Settings**; the equations and unknowns go in the boxes it reveals.

The answers you want are `ix` and `v3`, in **Results**.
:::

Select DC. Add equation `ir8=5`. Add unknown `ix`. Run the simulation, and
you will get: **{1,8}**. This is correct: I{{sub:X}} is 1A and that
V{{sub:X}} is 8V.

:::

::: problem B11's Example 6.22 (Hidden source)

Determine I{{sub:1}}.

::: figure assets/practice/b11s-example-6-22-hidden-source-17.jpg

:::

Although no source is shown, the circuit has a current. I use a ‘hidden'
current source.

```sym 7
s\dc("jt,0,1,12'm:r1,1,0,1'k:r2,1,0,10'k:r3,1,0,22'k"):approx(ir1)
```
```sym 8
s\dc("jt,0,1,12'm:r1,1,0,1'k:r2,1,0,10'k:r3,1,0,22'k"):approx(ir1)
```
```field 9 Circuit Description
jt,0,1,12'm
r1,1,0,1'k
r2,1,0,10'k
r3,1,0,22'k
```

We get I1 = **10.48** mA, which is correct.

:::

::: problem B11's Example 6.21 (Hidden source, Expert)

Determine I{{sub:S}}, I{{sub:1}} and I{{sub:3}}.

::: figure assets/practice/b11s-example-6-21-hidden-source-expert-18.jpg

:::

This ‘hidden source' problem is perfect for Expert. My solution:

```sym 7
s\ex("js,0,1,is:r1,1,0,6:r2,1,0,3:r3,1,0,1"):approx({is,ir1,ir3})
```
```sym 8
s\ex("js,0,1,is:r1,1,0,6:r2,1,0,3:r3,1,0,1"):approx({is,ir1,ir3})
```
```field 9 Circuit Description
js,0,1,is1
r1,1,0,6
r2,1,0,3
r3,1,0,1
```

::: only 7,8
Select DC, and press Enter. Add equation `ir2=2'm.` Add unknown `is`. Run the
simulation.
:::
::: only 9
Choose DC. Open **Expert Mode**, put `ir2 = 2'm` in **Add equations** and
`is` in **Add unknowns**, then **Run Symbulator**.
:::

The answer, **{.009,.001,.006}**, is correct, since the currents are as
follows: I{{sub:S}} is 9mA, I{{sub:1}} is 1mA and I{{sub:3}} is 6mA.

:::

::: problem Bo2's Example 1.9

Determine I{{sub:1}}, I{{sub:2}} and v.

::: figure assets/practice/bo2s-example-1-9-19.jpg

:::

This is my solution.

```sym 7
s\dc("ji,0,1,2:r1,1,0,3:jd,0,1,4v1:r2,1,0,5"):{ir1,v1,ir2}
```
```sym 8
s\dc("ji,0,1,2:r1,1,0,3:jd,0,1,4v1:r2,1,0,5"):{ir1,v1,ir2}
```
```field 9 Circuit Description
ji,0,1,2
r1,1,0,3
jd,0,1,4*v1
r2,1,0,5
```

::: only 9
The answers you want are `ir1`, `v1` and `ir2`, in **Results**.
:::

The answer, **{-5/26,-15/26,-3/26}, **is correct: I{{sub:1}}=-5/26,
I{{sub:2}}=-3/26 and v=-15/26.

:::

::: problem AS2's Practice Problem 2.7

Find v{{sub:o}} and i{{sub:o}} in the circuit. My solution below:

::: figure assets/practice/as2s-practice-problem-2-7-20.jpg

:::

```sym 7
s\dc("ji,0,o,6:ro,o,0,2:jd,o,0,iro/4:r8,o,0,8"):{vo,iro}
```
```sym 8
s\dc("ji,0,o,6:ro,o,0,2:jd,o,0,iro/4:r8,o,0,8"):{vo,iro}
```
```field 9 Circuit Description
ji,0,o,6
ro,o,0,2
jd,o,0,iro/4
r8,o,0,8
```

::: only 9
The answers you want are `vo` and `iro`, in **Results**.
:::

The answer, **{8,4}**, is correct: v{{sub:o}} = 8 and i{{sub:o}} = 4.

:::

::: problem HK5's Example 1-3

Determine the power delivered by each source and consumed by both resistors.

::: figure assets/practice/hk5s-example-1-3-21.jpg

:::

```sym 7
s\dc("ei,1,0,120:r1,1,2,30:ed,2,3,2vra:ra,0,3,15"):{-pei,-ped,pr1+pra}
```
```sym 8
s\dc("ei,1,0,120:r1,1,2,30:ed,2,3,2vra:ra,0,3,15"):{–pei,–ped,pr1+pra}
```
```field 9 Circuit Description
ei,1,0,120
r1,1,2,30
ed,2,3,2*vra
ra,0,3,15
```

::: only 9
Ask **Evaluate** for:

```field 9 Evaluate
-pei
-ped
pr1+pra
```
:::

The answer, **{960,1920,2880}**, is right: the independent source delivers
960W, the dependent source delivers 1920W, and the resistors consume 2880W
together.

:::

::: problem AS2's Practice Problem 2.6

Find v{{sub:x}} and v{{sub:o}} in the circuit. My solution below:

::: figure assets/practice/as2s-practice-problem-p2-6-22.jpg

:::

```sym 7
s\dc("ei,x,1,35:rx,x,0,10:ed,0,2,2vx:ro,1,2,5"):{vx,vro}
```
```sym 8
s\dc("ei,x,1,35:rx,x,0,10:ed,0,2,2vx:ro,1,2,5"):{vx,vro}
```
```field 9 Circuit Description
ei,x,1,35
rx,x,0,10
ed,0,2,2*vx
ro,1,2,5
```

::: only 9
The answers you want are `vx` and `vro`, in **Results**.
:::

The answer, **{10,-5}**, is correct: v{{sub:x}} =10 and v{{sub:o}} =-5.

:::

::: problem Bo2's Example 1.10

::: figure assets/practice/bo2s-example-1-10-23.jpg

:::

Determine v{{sub:1}}, v{{sub:2}} and i. My solution below. The simulation
took 14 seconds.

```sym 7
s\dc("ei,1,0,2:r1,1,2,1/3:ed,3,2,4*ir1:r2,3,0,1/5"):{ir1,vr1,vr2}
```
```sym 8
s\dc("ei,1,0,2:r1,1,2,1/3:ed,3,2,4*ir1:r2,3,0,1/5"):{ir1,vr1,vr2}
```
```field 9 Circuit Description
ei,1,0,2
r1,1,2,1/3
ed,3,2,4*ir1
r2,3,0,1/5
```

::: only 9
The answers you want are `ir1`, `vr1` and `vr2`, in **Results**.
:::

The answers, **{-15/26,-5/26,-3/26}**, is correct: v{{sub:1}}=-5/26,
v{{sub:2}}=-3/26 and i=-15/26.

:::

::: problem AS2's Example 2.6

::: figure assets/practice/as2s-example-2-6-24.jpg

:::

Determine v{{sub:o}} and *i* in the circuit. My solution is shown below:

```sym 7
s\dc("e12,1,o,12:ri,1,2,4:ed,2,3,2vo:e4,0,3,4:ro,o,0,6"):{vo,iri}
```
```sym 8
s\dc("e12,1,o,12:ri,1,2,4:ed,2,3,2vo:e4,0,3,4:ro,o,0,6"):{vo,iri}
```
```field 9 Circuit Description
e12,1,o,12
ri,1,2,4
ed,2,3,2*vo
e4,0,3,4
ro,o,0,6
```

::: only 9
The answers you want are `vo` and `iri`, in **Results**.
:::

The answer, **{48,-8}**, is correct: v{{sub:o}} =48 and *i* = -8.

:::

::: problem HK5's Drill Problem 1.11

Find the power absorbed by each element in the circuit. My solution below:

::: figure assets/practice/hk5s-drill-problem-1-11-25.jpg

:::

```sym 7
s\dc("r1,x,0,30:ei,1,x,12:r2,1,2,8:r3,2,3,7:ed,3,0,4vx"):
approx({pr1,pei,pr2,pr3,ped})
```
```sym 8
s\dc("r1,x,0,30:ei,1,x,12:r2,1,2,8:r3,2,3,7:ed,3,0,4vx"):
approx({pr1,pei,pr2,pr3,ped})
```
```field 9 Circuit Description
r1,x,0,30
ei,1,x,12
r2,1,2,8
r3,2,3,7
ed,3,0,4*vx
```

::: only 9
The answers you want are `pr1`, `pei`, `pr2`, `pr3` and `ped`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

The answer, **{.768,1.92,.2048,.1792,-3.072}**, is correct.

:::

::: problem AS2's Example 3.6

Determine the value of I{{sub:o}} in the circuit. My solution below:

::: figure assets/practice/as2s-example-3-6-26.jpg

:::

```sym 7
s\dc("ei,a,0,24:ro,a,b,10:r12,b,0,12:r4,b,c,4:r24,a,c,24:ed,c,0,4iro"):
approx(iro)
```
```sym 8
s\dc("ei,a,0,24:ro,a,b,10:r12,b,0,12:r4,b,c,4:r24,a,c,24:ed,c,0,4iro"):
approx(iro)
```
```field 9 Circuit Description
ei,a,0,24
ro,a,b,10
r12,b,0,12
r4,b,c,4
r24,a,c,24
ed,c,0,4*iro
```

::: only 9
The answer you want is `iro`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

The answer, **1.5** A, is correct.

:::

::: problem Bo2's Drill Exercise 1.12

Determine i, v and i{{sub:d}}.

::: figure assets/practice/bo2s-drill-exercise-1-12-27.jpg

:::

We are given an unnecessary piece of information: the 4V drop in the 2Ω
resistor.

My solution is shown below the schematic.

```sym 7
s\dc("ei,1,0,10:r1,1,2,1:r2,2,3,2:r3,2,0,3:
r4,3,0,2:ed,2,3,ir1/2"):{ir1,vr3,ied}
```
```sym 8
s\dc("ei,1,0,10:r1,1,2,1:r2,2,3,2:r3,2,0,3:
r4,3,0,2:ed,2,3,ir1/2"):{ir1,vr3,ied}
```
```field 9 Circuit Description
ei,1,0,10
r1,1,2,1
r2,2,3,2
r3,2,0,3
r4,3,0,2
ed,2,3,ir1/2
```

::: only 9
The answers you want are `ir1`, `vr3` and `ied`, in **Results**.
:::

The answer, **{4,6,1}**, is correct: i=4, v=6 and i{{sub:d}}=1.

:::

::: problem AS2's Example 3.2

Determine the voltages at the nodes.

::: figure assets/practice/as2s-example-3-2-28.jpg

:::

My solution below:

```sym 7
s\dc("ji,0,1,3:jd,3,0,2ir2:r2,1,2,2:r4a,1,3,4:r8,2,3,8:r4b,2,0,4"):
approx({v1,v2,v3})
```
```sym 8
s\dc("ji,0,1,3:jd,3,0,2ir2:r2,1,2,2:r4a,1,3,4:r8,2,3,8:r4b,2,0,4"):
approx({v1,v2,v3})
```
```field 9 Circuit Description
ji,0,1,3
jd,3,0,2*ir2
r2,1,2,2
r4a,1,3,4
r8,2,3,8
r4b,2,0,4
```

::: only 9
The answers you want are `v1`, `v2` and `v3`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

The answer, **{4.8,2.4,-2.4}**, is correct.

:::

::: problem AS2's Example 3.4

Find the node voltages in the circuit. My solution below:

::: figure assets/practice/as2s-example-3-4-29.jpg

:::

```sym 7
s\dc("r2,1,0,2:e,1,2,20:j,0,2,10:r6,2,3,6:rx,1,4,3:r4,3,0,4:
ed,3,4,3vrx:r1,4,0,1"):approx({v1,v2,v3,v4})
```
```sym 8
s\dc("r2,1,0,2:e,1,2,20:j,0,2,10:r6,2,3,6:rx,1,4,3:r4,3,0,4:
ed,3,4,3vrx:r1,4,0,1"):approx({v1,v2,v3,v4})
```
```field 9 Circuit Description
r2,1,0,2
e1,1,2,20
j,0,2,10
r6,2,3,6
rx,1,4,3
r4,3,0,4
ed,3,4,3*vrx
r1,4,0,1
```

::: only 9
The answers you want are `v1`, `v2`, `v3` and `v4`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

The answer, **{26.67,6.67,173.33,-46.67}**, is correct.

:::

::: problem Bo2's Drill Exercise 2.6

Determine the voltage in each node.

Notice that in the schematic, the resistors' values are given in siemens.
Symbulator has to be fed the resistors with values in ohms. This means that,
when we simulate them, we have to convert them from siemens to ohms by
dividing 1 over the siemens value.

::: figure assets/practice/bo2s-drill-exercise-2-6-30.jpg

:::

My solution below:

```sym 7
s\dc("j,0,1,6:ei,3,1,6:ed,2,3,3v1:r5,1,0,1/5:r2,1,2,1/2:
r3,2,0,1/3:r1,2,3,1:r4,3,0,1"):{v1,v2,v3}
```
```sym 8
s\dc("j,0,1,6:ei,3,1,6:ed,2,3,3v1:r5,1,0,1/5:r2,1,2,1/2:
r3,2,0,1/3:r1,2,3,1:r4,3,0,1"):{v1,v2,v3}
```
```field 9 Circuit Description
j,0,1,6
ei,3,1,6
ed,2,3,3*v1
r5,1,0,1/5
r2,1,2,1/2
r3,2,0,1/3
r1,2,3,1
r4,3,0,1
```

::: only 9
The answers you want are `v1`, `v2` and `v3`, in **Results**.
:::

The answer, **{-1,2,5}**, is correct.

:::

::: problem Bo2's Example 2.7

Determine the voltages in all nodes. My solution below the schematic:

::: figure assets/practice/bo2s-example-2-7-31.jpg

:::

```sym 7
s\dc("j,0,1,1:r3,0,1,3:r4,2,1,4:r1,2,0,1:r2,2,3,2:
r5,3,0,5:ei,3,4,1.5:ed,4,0,2vr4"):{v1,v2,v3,v4}
```
```sym 8
s\dc("j,0,1,1:r3,0,1,3:r4,2,1,4:r1,2,0,1:r2,2,3,2:
r5,3,0,5:ei,3,4,1.5:ed,4,0,2vr4"):{v1,v2,v3,v4}
```
```field 9 Circuit Description
j,0,1,1
r3,0,1,3
r4,2,1,4
r1,2,0,1
r2,2,3,2
r5,3,0,5
ei,3,4,1.5
ed,4,0,2*vr4
```

::: only 9
The answers you want are `v1`, `v2`, `v3` and `v4`, in **Results**.
:::

The answer, **{1.5,-.5,-2.5,-4.}**, is correct.

:::

::: problem Bo2's Example 2.6

Determine the voltages in all nodes.

::: figure assets/practice/bo2s-example-2-6-32.jpg

:::

My solution below:

```sym 7
s\dc("e1,0,1,1:e2,3,4,.5:ed,3,2,3vr4:j,0,4,2:r4,1,2,1/4:
r1,2,0,1:r8,3,0,1/8:r2,2,4,1/2"):{v1,v2,v3,v4}
```
```sym 8
s\dc("e1,0,1,1:e2,3,4,.5:ed,3,2,3vr4:j,0,4,2:r4,1,2,1/4:
r1,2,0,1:r8,3,0,1/8:r2,2,4,1/2"):{v1,v2,v3,v4}
```
```field 9 Circuit Description
e1,0,1,1
e2,3,4,.5
ed,3,2,3*vr4
j,0,4,2
r4,1,2,1/4
r1,2,0,1
r8,3,0,1/8
r2,2,4,1/2
```

::: only 9
The answers you want are `v1`, `v2`, `v3` and `v4`, in **Results**.
:::

The answer, **{-1,-2.,1.,.5}**, is correct.

:::

::: problem HK5's Drill Problem 1-12

Find i{{sub:A}}, i{{sub:B}} and i{{sub:C}}.

::: figure assets/practice/hk5s-drill-problem-1-12-33.jpg

:::

My solution below:

```sym 7
s\dc("jl,x,0,5.6:ra,0,x,18:jb,0,x,.1vx:r9,0,x,9:jr,0,x,2"):
approx({ira,ijb,ir9})
```
```sym 8
s\dc("jl,x,0,5.6:ra,0,x,18:jb,0,x,.1vx:r9,0,x,9:jr,0,x,2"):
approx({ira,ijb,ir9})
```
```field 9 Circuit Description
jl,x,0,5.6
ra,0,x,18
jb,0,x,.1*vx
r9,0,x,9
jr,0,x,2
```

::: only 9
The answers you want are `ira`, `ijb` and `ir9`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

The answer, **{3.,-5.4,6.}**, is correct.

:::

### Numerical-from-symbolic examples

::: problem Bo2's Drill Exercise 1.10

Determine i, v, i{{sub:s}} and v{{sub:s}}.

::: figure assets/practice/bo2s-drill-exercise-1-10-34.jpg

:::

With one unknown value and one known solution, this problem is a job for
Expert.

Determine i, v, i{{sub:s}} and v{{sub:s}}.

```sym 7
s\ex("es,2,0,vs:jd,0,3,2ir1:r7,0,1,7:r1,3,1,1:r3,3,2,3:r4,1,2,4"):
{ir1,vjd,-ies,vs}
```
```sym 8
s\ex("es,2,0,vs:jd,0,3,2ir1:r7,0,1,7:r1,3,1,1:r3,3,2,3:r4,1,2,4"):
{ir1,vjd,–ies,vs}
```
```field 9 Circuit Description
es,2,0,vs
jd,0,3,2*ir1
r7,0,1,7
r1,3,1,1
r3,3,2,3
r4,1,2,4
```

::: only 9
Set **Analysis** to *DC — direct current*. This one needs **Enable Expert Mode** ticked in **Settings**; the equations and unknowns go in the boxes it reveals.

The answers you want are `ir1`, `vjd` and `vs`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
-ies
```
:::

Select DC, Add` vr4=4` to the equations and `vs` to the unknowns. Run the
simulation. The answer, **{2,-9,-3,3}**, is correct: i=2, v=-9, i{{sub:s}}=-3
and v{{sub:s}}=3.

:::

::: problem Bo2's Drill Exercise 1.11

Determine i, v and v{{sub:d}}. (Since all element values are known, the tip
we are given by the book – namely, that the voltage drop in the 6Ω resistor
is 1.5V – is totally superfluous.)

::: figure assets/practice/bo2s-drill-exercise-1-11-35.jpg

:::

```sym 7
s\dc("e,1,0,12:r1,1,2,1:r4,2,0,4:r10,2,3,10:r6,3,0,6:
r2,3,4,2:j,4,0,vr10/15"):approx({vr10,ir2,vj})
```
```sym 8
s\dc("e,1,0,12:r1,1,2,1:r4,2,0,4:r10,2,3,10:r6,3,0,6:
r2,3,4,2:j,4,0,vr10/15"):approx({vr10,ir2,vj})
```
```field 9 Circuit Description
e1,1,0,12
r1,1,2,1
r4,2,0,4
r10,2,3,10
r6,3,0,6
r2,3,4,2
j,4,0,vr10/15
```

::: only 9
The answers you want are `vr10`, `ir2` and `vj`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

The answer, **{7.5,.5,.5}** is correct: i=.5, v=7.5 and v{{sub:d}}=.5.

:::

### Symbolic examples

::: problem TR5's Exercise 4.2

Find v{{sub:O}} and i{{sub:O}} in terms of i{{sub:S}}.

::: figure assets/practice/tr5s-exercise-4-2-36.jpg

:::

This is my solution. The simulation took 14 seconds.

```sym 7
s\dc("ji,0,x,is:r1,x,0,1'k:r2,x,o,2'k:jd,0,o,vx/500:ro,o,0,500"):
{vo,iro}
```
```sym 8
s\dc("ji,0,x,is:r1,x,0,1'k:r2,x,o,2'k:jd,0,o,vx/500:ro,o,0,500"):
{vo,iro}
```
```field 9 Circuit Description
ji,0,x,is1
r1,x,0,1'k
r2,x,o,2'k
jd,0,o,vx/500
ro,o,0,500
```

::: only 9
The answers you want are `vo` and `iro`, in **Results**.
:::

The answer, **{1000\*is,2\*is}**, is correct: *v*{{sub:O}}*=1000*
*i*{{sub:S}} and *i*{{sub:O}}*=2 i*{{sub:S}}.

:::

::: problem TR5's Example 4.4

Find v{{sub:O}} and the equivalent resistance R{{sub:IN}}, in terms of
v{{sub:S}}, when R{{sub:1}} is 50, R{{sub:2}} is 1'k, R{{sub:3}} is 100,
R{{sub:4}} is 5'k and g is 100mA (e.g. 100'm).

::: figure assets/practice/tr5s-example-4-4-37.jpg

:::

This is my solution. The simulation took 18 seconds.

```sym 7
s\dc("e,1,0,vs:r1,1,2,50:r2,2,o,1'k:r3,o,0,100:
r4,o,0,5'k:j,0,o,100'm*vr2"):approx({vo,re})
```
```sym 8
s\dc("e,1,0,vs:r1,1,2,50:r2,2,o,1'k:r3,o,0,100:
r4,o,0,5'k:j,0,o,100'm*vr2"):approx({vo,re})
```
```field 9 Circuit Description
e1,1,0,vs
r1,1,2,50
r2,2,o,1'k
r3,o,0,100
r4,o,0,5'k
j,0,o,100'm*vr2
```

::: only 9
The answers you want are `vo` and `re`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

The answer, **{.904\*vs,10951.}**, is correct: *v*{{sub:O}}*=.904 v*{{sub:S}}
and *R*{{sub:IN}}*=10.95'kΩ*.

:::

::: problem TR5's Figure 4-4

Find the voltage drop, current, and power consumed by the 500Ω resistor, and
the ratio of that power to that delivered by the independent source, all in
terms of *i*{{sub:S}}.

::: figure assets/practice/tr5s-figure-4-4-38.jpg

:::

I have not labeled the nodes in the figure, so you can practice doing it. My
solution:

```sym 7
s\dc("js,0,1,is:r50,1,0,50:rx,1,0,25:jd,o,0,48irx:
r3,o,0,300:ro,o,0,500"):{iro,vo,pro,pro/(-pjs)}
```
```sym 8
s\dc("js,0,1,is:r50,1,0,50:rx,1,0,25:jd,o,0,48irx:
r3,o,0,300:ro,o,0,500"):{iro,vo,pro,pro/(–pjs)}
```
```field 9 Circuit Description
js,0,1,is1
r50,1,0,50
rx,1,0,25
jd,o,0,48*irx
r3,o,0,300
ro,o,0,500
```

::: only 9
The answers you want are `iro`, `vo` and `pro`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
pro/(-pjs)
```
:::

The answers we get are correct: i{{sub:O}}=**-12is**, v{{sub:O}}=**-6000is**,
p{{sub:O}}=**72000is**{{sup:2}}, and p{{sub:O}}/p{{sub:S}}=**4320**.

:::

::: problem TR5's Example 4.1 (Symbolic)

Find *v*{{sub:O}}.

::: figure assets/practice/tr5s-example-4-1-symbolic-39.jpg

:::

I did not label the nodes, so you can practice. Remember not using **rc**: it
is reserved.

```sym 7
s\dc("ei,1,0,vs:rs,1,2,rs:rx,2,0,rp:ed,0,3,r*irx:rrc,3,o,rrc:rl,o,0,rl"):vo
```
```sym 8
s\dc("ei,1,0,vs:rs,1,2,rs:rx,2,0,rp:ed,0,3,r*irx:rrc,3,o,rrc:rl,o,0,rl"):vo
```
```field 9 Circuit Description
ei,1,0,vs
rs,1,2,rs
rx,2,0,rp
ed,0,3,r*irx
rrc,3,o,rrc
rl,o,0,rl
```

::: only 9
The answer you want is `vo`, in **Results**.
:::

The answer, shown left, is correct. The textbook's answer is shown right.

::: figure assets/practice/tr5s-example-4-1-symbolic-40.jpg

:::

::: figure assets/practice/tr5s-example-4-1-symbolic-41.jpg

:::

:::

::: problem Bo2's Example 1.11 (Symbolic)

Determine v{{sub:2}}.

::: figure assets/practice/bo2s-example-1-11-symbolic-42.jpg

:::

My solution below. In my solution I named the value of the source v{{sub:1}},
to keep it similar to the book. This required avoiding naming any node as
**1**: if there was a node 1, Symbulator would store in **v1** the voltage of
the node, creating trouble. There is no problem with using r1 as a value,
since nothing will be stored in that r1 value.

```sym 7
s\dc("e,a,0,v1:r1,a,3,r1:rg,3,0,rg:j,2,0,gm*vrg:rd,2,0,rd:rl,2,0,rl"):v2
```
```sym 8
s\dc("e,a,0,v1:r1,a,3,r1:rg,3,0,rg:j,2,0,gm*vrg:rd,2,0,rd:rl,2,0,rl"):v2
```
```field 9 Circuit Description
e1,a,0,v1
r1,a,3,r1
rg,3,0,rg
j,2,0,gm*vrg
rd,2,0,rd
rl,2,0,rl
```

::: only 9
The answer you want is `v2`, in **Results**.
:::

The simulation took 25 seconds. The answer I got is shown left (the
textbook's right.)

::: figure assets/practice/bo2s-example-1-11-symbolic-43.jpg

:::

::: figure assets/practice/bo2s-example-1-11-symbolic-44.jpg

:::

:::

::: problem TR5's Example 4-7 (Symbolic)

Find R{{sub:IN}}, e.g. the resistance as seen by the current source. My
solution below.

::: figure assets/practice/tr5-example-4-7-symbolic-45.jpg

:::

```sym 7
s\dc("ji,0,a,is:re,a,0,re:jd,b,a,β*is:rl,b,0,rl"):rji
```
```sym 8
s\dc("ji,0,a,is:re,a,0,re:jd,b,a,β*is:rl,b,0,rl"):rji
```
```field 9 Circuit Description
ji,0,a,is1
re1,a,0,re1
jd,b,a,beta*is1
rl,b,0,rl
```

::: only 9
The answer you want is `rji`, in **Results**.
:::

The answer we get, `re*(β+1)`, is correct, as can be seen by comparing it to
the textbook's answer, shown below.

::: figure assets/practice/tr5-example-4-7-symbolic-46.jpg

:::

:::

::: problem TR5's Exercise 4.3 (Symbolic)

Find v{{sub:O}}, in terms of the value in the circuit. For resistors, use
their conductance value.

::: figure assets/practice/tr5s-exercise-4-3-symbolic-47.jpg

:::

This is my solution. We use **µ** as a constant in the dependent source. It
is not confused with the SI prefix for micro because the prefix has an
apostrophe.

```sym 7
s\dc("ei,1,0,vs:ed,2,0,μ*(vrx):r1,1,2,1/g1:
r2,2,o,1/g2:rx,1,o,1/gx:rl,o,0,1/gl"):vo
```
```sym 8
s\dc("ei,1,0,vs:ed,2,0,μ*(vrx):r1,1,2,1/g1:
r2,2,o,1/g2:rx,1,o,1/gx:rl,o,0,1/gl"):vo
```
```field 9 Circuit Description
ei,1,0,vs
ed,2,0,μ*(vrx)
r1,1,2,1/g1
r2,2,o,1/g2
rx,1,o,1/gx
rl,o,0,1/gl
```

::: only 9
The answer you want is `vo`, in **Results**.
:::

This is the answer we get. It is correct. Compare it with the textbook's
answer.

::: figure assets/practice/tr5s-exercise-4-3-symbolic-48.png

:::

::: figure assets/practice/tr5s-exercise-4-3-symbolic-49.jpg

:::

The last four problems show Symbulator at its DC best. I don't know of any
calculator-based program that was able to provide this kind of purely
symbolic answer to a circuit simulator back in 1999 when I made Symbulator.
As a matter of fact, even today – a quarter of a century later - I know of no
other calculator-based simulator that can do this.

:::

::: problem TR5's Example 4.5 (Symbolic)

Find i{{sub:B}}.

::: figure assets/practice/tr5s-example-4-5-symbolic-50.jpg

:::

My solution is shown below. Be patient. This simulation takes more than one
minute.

```sym 7
s\dc("e1,1,0,vcc:rb,1,b,rb:e2,e,b,vγ:re,e,0,re:rrc,1,c,rrc:j,c,e,β*irb"):irb
```
```sym 8
s\dc("e1,1,0,vcc:rb,1,b,rb:e2,e,b,vγ:re,e,0,re:rrc,1,c,rrc:j,c,e,β*irb"):irb
```
```field 9 Circuit Description
e1,1,0,vcc
rb,1,b,rb
e2,e,b,vgamma
re1,e,0,re1
rrc,1,c,rrc
j,c,e,beta*irb
```

::: only 9
The answer you want is `irb`, in **Results**.
:::

Compare my answer, left, to the book's answer, right.

::: figure assets/practice/tr5s-example-4-5-symbolic-51.jpg

:::

::: figure assets/practice/tr5s-example-4-5-symbolic-52.jpg

:::

:::

###

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
