---
id: lesson-equivalents
kind: lesson
title: Shorts, equivalent resistance and Thévenin/Norton
updated: 2023-07-08
summary: >
  Learn how to describe a *short circuit* using the **s** element. Learn how to
  find *equivalent resistances* using the **er** script, and *Thevenin and
  Norton equivalents* using the **th** script.
---

In this lesson, you will learn how to describe a *short circuit* using the
**s** element. And you will learn how to find *equivalent resistances* using
the **er** script, and *Thévenin and Norton equivalents* using the **th**
script.

## How to describe a short circuit {#describe-short}

Shorts are used mostly when we need to find out a current in a part of the
circuit where there is no element already. Otherwise, we would just define it
as a single node.

::: note Describing short circuits
In Symbulator, an ideal short circuit is described using three bits of
information, separated by commas: first, the name of the short, which must
start with the letter **s**; then, the name of the first node; and finally, the
name of the second node.

For example, an ideal short circuit called **s1**, connected between two nodes
called **3** and **5**, would be described as follows: `s1,3,5`{{i:short circuit}}
:::

### What answers do you get

No power is consumed, and no voltage is dropped, in a short circuit. For each
short in a circuit, Symbulator stores only the current through it, flowing from
the first node towards the second. For a short called sx, that is
{{v7,8|`isx`}}{{v9|the **current through** line of the `sx` block in **Results**}}.

::: problem HK5's Drill Problem 1-13
Find i1, i2, i3 and i4.

::: figure assets/circuit/hk5d0113.jpg
HK5's Drill Problem 1-13
:::

::: answer
My solution below. I define the shorts in the same direction as the arrows in
the schematic.

```sym 7
s\dc("r1,1,0,25:jd,0,2,.2v1:r2,2,3,10:ji,4,3,2.5:r3,4,5,100:s1,1,2:s2,2,4:s3,0,3:s4,3,5")
```
```sym 8
s\dc("r1,1,0,25:jd,0,2,.2v1:r2,2,3,10:ji,4,3,2.5:r3,4,5,100:s1,1,2:s2,2,4:s3,0,3:s4,3,5")
```
```field 9 Circuit Description
r1,1,0,25
jd,0,2,.2v1
r2,2,3,10
ji,4,3,2.5
r3,4,5,100
s1,1,2
s2,2,4
s3,0,3
s4,3,5
```

{{v7,8|We ask for the values of the variables:}}{{v9|Choose *Solve circuit* and
*DC*, then run it. Each short has its own block in **Results**, and the
number you want is on its **current through** line:}}

```sym 7
approx({is1,is2,is3,is4})
```
```sym 8
approx({is1,is2,is3,is4})
```
```out 7,8
{–2., 3., –8., –.5}
```

::: only 9
| Short | Current through |
|---|---|
| `s1` | {{o:-2}} A |
| `s2` | {{o:3}} A |
| `s3` | {{o:-8}} A |
| `s4` | {{o:-0.5}} A |
:::

These are correct. These answers can only be found using short circuits.
:::
:::

## The equivalent resistance script: er {#er-script}

As we saw before, Symbulator has the ability to provide the equivalent
resistance of a circuit as seen from any source. This allows us to solve
problems like the following.

::: problem AS2's Practice Problem 2.15
Find the equivalent resistance as seen by the 100 V source, and the value of
current i.

::: figure assets/circuit/as2pp0215.jpg
AS2's Practice Problem 2.15
:::

::: answer
```sym 7
s\dc("e,a,0,100:r13,a,1,13:r24,1,2,24:r10,1,3,10:r20,2,3,20:r30,2,0,30:r50,3,0,50"):re
```
```sym 8
s\dc("e,a,0,100:r13,a,1,13:r24,1,2,24:r10,1,3,10:r20,2,3,20:r30,2,0,30:r50,3,0,50"):re
```
```field 9 Circuit Description
e1,a,0,100
r13,a,1,13
r24,1,2,24
r10,1,3,10
r20,2,3,20
r30,2,0,30
r50,3,0,50
```

::: only 7,8
By evaluating `re` we get the equivalent resistance as seen by the source e. It
is 40 Ω. By evaluating `ir13` we get 2.5 A for current i. The answers were
easily found, because there was a source connected between the two desired
nodes.
:::
::: only 9
Solve it in DC. There is no special tool to reach for here: because a source
sits between the two nodes we care about, the equivalent resistance is one of
the answers Symbulator works out anyway. In the block for `e`, the
**resistance seen** line reads re = 40 Ω.

The current i is the current through r13, and its block gives ir13 = 2.5 A.

Both answers came free, because there was a source connected between the two
desired nodes. The rest of this lesson is about what to do when there is not.
:::
:::
:::

### What if there is no independent source?

But how can we find the equivalent resistance of a **passive circuit**, that is
to say, a circuit that has no *independent* source in it? One way is to connect
a 1 A current source between the two nodes where we want to find the equivalent
resistance, and then read the voltage drop across the source. This is the
manual way.

An easier way is to let Symbulator do that for us.{{i:er script}}

::: only 7,8
Just run the **er** script, and it will do the same thing automatically. The er
script finds the equivalent resistance of a passive circuit, and stores it — in
the case of a DC analysis — in **req**. It takes three arguments: the circuit
description in the form of a string, and the two nodes between which we need to
find the equivalent resistance.
:::
::: only 9
Version 9 puts this on the **Type of analysis** menu. Choose *Find equivalent*
instead of *Solve circuit*, and a second menu appears — **Type of equivalent**
— whose first entry is *Resistance / impedance*. Two node boxes appear with
it, for the pair of terminals you are measuring between.

That is the whole of it: no source to invent, no voltage to divide. Symbulator
does the 1 A trick internally and reports the answer.
:::

::: problem B11's Example 8.29
Calculate the equivalent resistance of the circuit shown below.

::: figure assets/circuit/b11e0829.jpg
B11's Example 8.29
:::

::: answer
Let me solve this problem step by step. After I label the nodes, I describe the
circuit and store it in a variable.

```sym 7
"r4,0,a,4:r2,0,b,2:r6,a,b,6:rb,a,c,3:ra,b,c,3"→cir
s\er(cir,0,c)
```
```sym 8
"r4,0,a,4:r2,0,b,2:r6,a,b,6:rb,a,c,3:ra,b,c,3"→cir
s\er(cir,0,c)
```
```field 9 Circuit Description
r4,0,a,4
r2,0,b,2
r6,a,b,6
rb,a,c,3
ra,b,c,3
```

::: only 7,8
When prompted, choose DC as analysis type. Once it is done, evaluate:

```sym 7
approx(req)
```
```sym 8
approx(req)
```

```out 7,8
2.89
```
:::
::: only 9
Set **Type of analysis** to *Find equivalent*, **Type of equivalent** to
*Resistance / impedance*, and the two node boxes to **0** and **c**. Leave
**Analysis** on *DC — direct current* and press **Run Symbulator**.

**Results** looks different from a normal solve: instead of the node and
element listing there is a single block headed **Equivalent impedance**, with
one line in it.

Req = 2.89 Ω
:::

The value is 2.89 Ω. This is correct.
:::
:::

### What counts as passive

The example above was made of resistors only. The er script can be applied to a
second type of passive circuit: one that includes resistors and dependent
sources, but no independent sources. A circuit with no independent sources can
only be reduced to an equivalent resistance, not to a Thévenin or Norton
equivalent, so the proper script to use is er. It is used in exactly the same
manner as for purely resistive circuits, making sure the dependent sources are
described properly.

## The Thévenin / Norton script: th {#th-script}

Just as a *passive circuit* can be reduced to an equivalent resistance, an
**active circuit** — one with independent sources — can be reduced to a
Thévenin or Norton equivalent.

One way to do this with Symbulator is to run a first simulation to find the
voltage between the two nodes where we want the equivalent (this is the
Thévenin voltage, VTH), and then a second simulation with a short circuit
connected between those nodes to find the current running through it (this is
the Norton current, INO). We then get REQ by dividing VTH/INO. This is the
manual way.

An easier way is to run the **th** script,{{i:th script}} which does exactly
that, automatically. It takes three arguments: the circuit description, the
first node and the second node.

::: problem RM3's Practice Problem 9-4
Find the Thévenin and Norton equivalents of the circuit below.

::: figure assets/circuit/rm3pp0904.jpg
RM3's Practice Problem 9-4
:::

::: answer
This is my circuit description, and this is how we run the th script:

```sym 7
"e,1,0,3.3:r1,1,2,66:r2,2,0,24"→cir
s\th(cir,2,0)
```
```sym 8
"e,1,0,3.3:r1,1,2,66:r2,2,0,24"→cir
s\th(cir,2,0)
```
```field 9 Circuit Description
e1,1,0,3.3
r1,1,2,66
r2,2,0,24
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to
*Thévenin / Norton*. Two node boxes appear: put **2** in the first and **0** in
the second — the pair of terminals you are looking into. Leave **Analysis** on
*DC — direct current* and press **Run Symbulator**.
:::

::: only 7,8
We could also have passed the circuit description directly:

```sym 7
s\th("e,1,0,3.3:r1,1,2,66:r2,2,0,24",2,0)
```
```sym 8
s\th("e,1,0,3.3:r1,1,2,66:r2,2,0,24",2,0)
```

When prompted to select a type of analysis, choose DC. Symbulator will let you
know what it's doing: first it runs one simulation and gives you the Thévenin
voltage, then a second one for the Norton current and the equivalent
resistance. In this case, VTH = 0.88 V, INO = 0.05 A and REQ = 17.6 Ω.
:::

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to
*Thévenin / Norton*. Two node boxes appear: put **2** in the first and **0** in
the second — the pair of terminals you are looking into. The answers are
`vth` = 0.88 V, `ino` = 0.05 A and `req` = 17.6 Ω.
:::
{{v7,8|At this point, when you press ENTER, Symbulator will ask whether you
are planning to run a problem with a load connected to this equivalent
circuit. For now, say No. After the script is done, the following variables
are stored:}}{{v9|The answers appear in **Results** under these names:}}

- **vth** has the Thévenin voltage
- **ino** has the Norton current
- **req** has the equivalent resistance
- **pmax** has the maximum power that the equivalent can deliver to a
  hypothetical load
:::
::: only 9
**Results** replaces the usual node-and-element listing with a single block
headed **Thévenin / Norton equivalent**. There are no prompts and no second
step; all four answers arrive together:

- **Thevenin voltage**, vth = 880 mV
- **Norton current**, ino = 50 mA
- **Equivalent resistance**, Req = 17.6 Ω
- **Maximum deliverable power**, pmax = 11 mW

The first three are what you came for. The fourth is Symbulator being
generous — the most this circuit could deliver into a matched load — and the
calculator versions do not report it at all.
:::
:::

### Problems with a load

One type of problem that books and professors like to present when teaching the
Thévenin / Norton equivalents is what I like to call RL problems. A typical RL
problem goes like this: "First, reduce the circuit, as seen by resistor RL, to
its Thévenin or Norton equivalent. Then, find the value of the voltage drop,
current and/or power consumed in the load resistor RL if its value is
(whatever) ohms."

::: only 7,8
Since this is such a typical problem, I've made some provisions in Symbulator
to help you solve them. Right after a Thévenin or Norton equivalent is found,
the th script asks whether you are planning to connect a load. The default is
No, but if you select Yes, Symbulator will save some special answers for that
very typical case, as functions of the **load** variable:

- **irl** has the current in the load
- **vrl** has the voltage drop in the load
- **prl** has the power consumed in the load
:::
::: only 9
Symbulator 9 does not ask, and it does not carry the load quantities on the
results either. **Results** shows four answers and no more: `vth`, `ino`,
`req` and `pmax`.

That is no great loss, because each load quantity is one line in
**Evaluate**, built from the two answers you already have. Writing R for
the load resistance:

| To find | Type into Evaluate |
|---|---|
| the current in the load | `vth/(req+R)` |
| the voltage drop in the load | `vth*R/(req+R)` |
| the power consumed in the load | `vth^2*R/(req+R)^2` |

Put the load's actual value where R is. The rest of this section reads
exactly as it does on the calculator, with those three in place of the
calculator's `irL`, `vrL` and `prL`.
:::

::: problem B11's Example 9.6
Find the Thévenin equivalent circuit for the network in the shaded area. Then
find the current through RL for RL values of 2 Ω, 10 Ω and 100 Ω.

::: figure assets/circuit/b11e0906.jpg
B11's Example 9.6
:::

::: answer
First we find the Thévenin equivalent.

```sym 7
s\th("e1,1,0,9:r1,1,2,3:r2,2,0,6",2,0):{vth,req}
```
```sym 8
s\th("e1,1,0,9:r1,1,2,3:r2,2,0,6",2,0):{vth,req}
```
```field 9 Circuit Description
e1,1,0,9
r1,1,2,3
r2,2,0,6
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to
*Thévenin / Norton*. Two node boxes appear: put **2** in the first and **0**
in the second. Choose *DC* and run it.

**Results** gives `vth` = {{o:6}} V and `req` = {{o:2}} Ω.
:::
```out 7,8
{6, 2}
```

Correct. Now we find the values of the current in the load for the different
values. We can do this in a single push, or separately. Here I find them in one
go:

```sym 7
{irL|Load=2.,irL|Load=10.,irL|Load=100.}
```
```sym 8
{irL|Load=2.,irL|Load=10.,irL|Load=100.}
```
::: only 9
There is no single push here — you ask **Evaluate** three times, once per
load, and the answers come back one at a time:

```field 9 Evaluate
vth/(req+2)
```

Then `vth/(req+10)`, then `vth/(req+100)`.
:::
```out
{1.5, .5, .059}
```

{{v7,8|Where `|` is the "given" operator.}} The answers are correct.
:::
:::

### Power transfer problems

Another type of problem often associated with the Thévenin / Norton equivalents
concerns the power transfer to a load, particularly the maximum power transfer
possible. Maximum power is transferred when the load RL equals the REQ of the
equivalent. Symbulator's th script gives you the maximum power that can be
delivered in {{v7,8|**pmax**}}{{v9|`eq.pmax`}}, and the power transferred to the
load as a function of its value in {{v7,8|**prl**}}{{v9|the `prl` expression
derived above}}.

### What if it's more than a load?

The formulas for the current, voltage and power in the load apply only when a
load is the only thing connected to the equivalent circuit. If the problem you
want to solve includes something more complicated, you will have to run your
own simulation.

::: only 7,8
To help you in those cases, let me show you one more goody of the th script, at
risk of promoting vagrancy among EE students: once it has found the Norton
equivalent of a circuit, it will automatically write for you the circuit
description of that Norton equivalent connected to a load, and store it in a
string called **eqcir**. You can use it as a starting point. It has the Norton
equivalent connected, between nodes **n** and **0**, to a load called **rl**
with a symbolic value of **load**, in ohms.
:::
::: only 9
Symbulator 9 writes no such string for you, and does not need to: the
equivalent is three lines, and you already have both numbers on screen.
Type them into a fresh **Circuit Description**, putting `ino` and `req`
where they belong:

```field 9 Circuit Description
jn,0,n,ino
re1,n,0,req
rl,n,0,load
```

Replace `ino` and `req` with the numbers **Results** just gave you. The
load is called `rl` and its value is the symbol `load`, so the answers
come back in terms of it.

You can use it as a starting point for a new simulation.
:::

::: problem RM3's Example 9-8
Find the Norton equivalent of the circuit left of a-b; then find the current
through RL.

::: figure assets/circuit/rm3e0908.jpg
RM3's Example 9-8
:::

::: answer
Let's first find the circuit equivalent:

```sym 7
s\th("e,1,0,24:r1,1,2,120:r2,2,0,280:j,2,0,560'm",2,0):{ino,req}
```
```sym 8
s\th("e,1,0,24:r1,1,2,120:r2,2,0,280:j,2,0,560'm",2,0):{ino,req}
```
```field 9 Circuit Description
e1,1,0,24
r1,1,2,120
r2,2,0,280
j,2,0,560'm
```

::: only 9
*Find equivalent*, *Thévenin / Norton*, nodes **2** and **0**, in DC.
:::
```out 7,8
{.36, 84.}
```

::: only 9
**Results** gives `ino` = {{o:-0.36}} A and `req` = {{o:84}} Ω.

The sign differs from the calculator's, which prints {{o:0.36}}: version 9
reports the Norton current in the direction it actually flows, from the
first node to the second. Nothing else changes — carry the sign through and
the load current below comes out the same.
:::

Correct. Now to the second part of the question. In order to find the current
through RL, we cannot use the load expressions, because now the load is not the
only thing connected to the terminals of the equivalent: there is also a
current source. We have to run a new simulation.

The fastest way is to start from the equivalent circuit description:

```out
"jN,0,n,iNo:rE,n,0,rEq:rL,n,0,L"
```

We change the value of the load to 168 Ω, and add the 180 mA source flowing
from node 0 to node n. Then we run a dc simulation and ask for the current in
the load:

```sym 7
s\dc("jN,0,n,iNo:rE,n,0,rEq:rL,n,0,168:j,0,n,180'm"):irL
```
```sym 8
s\dc("jN,0,n,iNo:rE,n,0,rEq:rL,n,0,168:j,0,n,180'm"):irL
```
```field 9 Circuit Description
jn,0,n,-0.36
re1,n,0,84
rl,n,0,168
j,0,n,180'm
```

```out 7,8
–.06
```

::: only 9
Run it in DC. The `rl` block's **current through** line reads
{{o:-0.06}} A.
:::

Correct: there is a current of 60 mA flowing through RL from 0 to n.

Using the equivalent circuit description is meant to save you time. If you find
it confusing to use, just don't use it.
:::
:::

## Instructive solved examples {#practice-equivalents}

::: practice


### Practice problems for resistive circuits

::: problem B11's Example 8.29

Calculate the equivalent resistance of the circuit shown below.

Let me solve this problem step by step, since it is the first time you see
the **er** script.

::: figure assets/practice/b11s-example-8-29-1.jpg

:::

After I label the nodes, I describe the circuit. In this case, I store it in
a variable.

```sym 7
"r4,0,a,4:r2,0,b,2:r6,a,b,6:rb,a,c,3:ra,b,c,3"→cir
```
```sym 8
"r4,0,a,4:r2,0,b,2:r6,a,b,6:rb,a,c,3:ra,b,c,3"→cir
```

```field 9 Circuit Description
r4,0,a,4
r2,0,b,2
r6,a,b,6
rb,a,c,3
ra,b,c,3
```

::: only 7,8
Run the **er** script, giving it as arguments the circuit and the nodes:
`s\er(cir,0,c)` When prompted, choose DC as analysis type. Once it is done,
evaluate `approx(req)` The value is **2.89** Ω.
:::
::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to
*Impedance*, with nodes **0** and **c**, in DC. The answer is `req` =
{{o:2.891}} Ω.
:::

This is correct. Below are many practice examples of this type.

:::

::: problem B11's Example 8.30

Find the equivalent resistance of the circuit below.

::: figure assets/practice/b11s-example-8-30-2.jpg

:::

```sym 7
s\er("rac,a,c,6:rad,a,d,9:rab,a,b,6:rcd,c,d,9:rbc,b,c,6:rbd,b,d,9",a,c)
```
```sym 8
s\er("rac,a,c,6:rad,a,d,9:rab,a,b,6:rcd,c,d,9:rbc,b,c,6:rbd,b,d,9",a,c)
```

```field 9 Circuit Description
rac,a,c,6
rad,a,0,9
rab,a,b,6
rcd,c,0,9
rbc,b,c,6
rbd,b,0,9
```

::: only 7,8
Choose DC. When *Done*, use `approx(req)` to find the equivalent resistance
is **3.27** Ω.
:::
::: only 9
*Find equivalent*, *Impedance*, nodes **a** and **c**, in DC: `req` is
{{o:3.273}} Ω.
:::

::: only 9
The calculator description names its four nodes a, b, c and d. Version 9
needs one of them to be the reference node, so d is called 0 here instead.
Which node you ground makes no difference to the answer in a network with
no sources — grounding b gives the same {{o:3.273}} Ω.
:::

:::

::: problem AS2's Example 2.9

Find the equivalent resistance of the circuit below.

::: figure assets/practice/as2s-example-2-9-3.jpg

:::

We don't need to run a simulation for this. We can reduce it using s\pr.

```sym 7
4+s\pr({1+5,2+s\pr({6,3})})+8
```
```sym 8
4+s\pr({1+5,2+s\pr({6,3})})+8
```

Evaluating approximately gives us the equivalent resistance: **14.4** Ω.

:::

::: problem AS2's Practice Problem 2.9

Find the equivalent resistance of the circuit below.

::: figure assets/practice/as2s-practice-problem-2-9-4.jpg

:::

We don't need to run a simulation for this. We can reduce it using s\pr.

```sym 7
2+s\pr({6,3+s\pr({4,4+5+3})})+1
```
```sym 8
2+s\pr({6,3+s\pr({4,4+5+3})})+1
```

Evaluating approximately gives us the equivalent resistance: **6** Ω.

:::

::: problem AS2's Example 2.11

Find the equivalent *conductance* of the circuit below.

::: figure assets/practice/as2s-example-2-11-5.jpg

:::

We don't need to run a simulation for this. We can reduce it using s\pr.

```sym 7
1/(s\pr({1/6,1/5+s\pr({1/8,1/12})}))
```
```sym 8
1/(s\pr({1/6,1/5+s\pr({1/8,1/12})}))
```

Evaluating approximately gives us the equivalent conductance: **10** S.

:::

::: problem AS2's Practice Problem 2.11

Find the equivalent *conductance* of the circuit below.

::: figure assets/practice/as2s-practice-problem-2-11-6.jpg

:::

We don't need to run a simulation for this. We can reduce it using s\pr.

```sym 7
1/(s\pr({1/8,1/4})+s\pr({1/2,1/12+1/6}))
```
```sym 8
1/(s\pr({1/8,1/4})+s\pr({1/2,1/12+1/6}))
```

Evaluating approximately gives us the equivalent conductance: **4** S.

:::

### Examples with dependent sources

::: problem Bo2's Drill Problem 3.14

Find the equivalent resistance of the circuit below.

::: figure assets/practice/bo2s-drill-problem-3-14-7.jpg

:::

```sym 7
s\er("r4,a,0,4:ri,a,0,6:ji,a,0,iri/2",a,0)
```
```sym 8
s\er("r4,a,0,4:ri,a,0,6:ji,a,0,iri/2",a,0)
```
```field 9 Circuit Description
r4,a,0,4
ri,a,0,6
ji,a,0,i_ri/2
```

::: only 7,8
Choose DC. Wait for *Done*. Evaluate `req` to find the equivalent resistance
is **2** Ω.
:::
::: only 9
*Find equivalent*, *Impedance*, nodes **a** and **0**, in DC: `req` is
{{o:2}} Ω.
:::

:::

::: problem AS2's Example 4.10

Find the equivalent resistance of the circuit below.

::: figure assets/practice/as2s-example-4-10-8.jpg

:::

```sym 7
s\er("r4,a,0,4:rx,0,a,2:j,a,0,2irx",a,0)
```
```sym 8
s\er("r4,a,0,4:rx,0,a,2:j,a,0,2irx",a,0)
```
```field 9 Circuit Description
r4,a,0,4
rx,0,a,2
j,a,0,2*i_rx
```

::: only 7,8
Choose DC. Wait for *Done*. Evaluate `req`. The equivalent resistance is
**-4** Ω. It may be surprising to have a negative resistance. This is the
result of the dependent sources.
:::
::: only 9
*Find equivalent*, *Impedance*, nodes **a** and **0**, in DC: `req` is
{{o:-4}} Ω. It may be surprising to have a negative resistance. This is
the result of the dependent sources.
:::

:::

::: problem AS2's Practice Problem 4.10

Find the equivalent resistance of the circuit below.

::: figure assets/practice/as2s-practice-problem-4-10-9.jpg

:::

```sym 7
s\er("r15,a,0,15:e,1,a,4vrx:r10,1,x,10:rx,x,0,5",a,0)
```
```sym 8
s\er("r15,a,0,15:e,1,a,4vrx:r10,1,x,10:rx,x,0,5",a,0)
```
```field 9 Circuit Description
r15,a,0,15
e1,1,a,4*v_rx
r10,1,x,10
rx,x,0,5
```

::: only 7,8
Choose DC. Wait for *Done*. Evaluating `req` approximately, we find the
equivalent resistance is **-7.5** Ω.
:::
::: only 9
*Find equivalent*, *Impedance*, nodes **a** and **0**, in DC: `req` is
{{o:-7.500}} Ω. The source is called `e1` rather than `e` here — version 9
keeps `e` for Euler's number.
:::

:::

::: problem HK5's Figure 2-29

Find the equivalent resistance of the circuit below.

::: figure assets/practice/hk5s-figure-2-29-10.jpg

:::

```sym 7
s\er("e,3,0,1.5is:r3,3,2,3:r2,2,0,2:s,2,1",1,0)
```
```sym 8
s\er("e,3,0,1.5is:r3,3,2,3:r2,2,0,2:s,2,1",1,0)
```
```field 9 Circuit Description
e1,3,0,1.5*i_s1
r3,3,2,3
r2,2,0,2
s1,2,1
```

::: only 7,8
Choose DC. Wait for *Done*. Evaluate `req`. The equivalent resistance is
**0.6** Ω.
:::
::: only 9
*Find equivalent*, *Impedance*, nodes **1** and **0**, in DC: `req` is
{{o:0.6000}} Ω. Both the source and the short are renamed, for the same
reason: version 9 reserves `e` and `s`.
:::

:::

::: problem HK5's Drill Problem 2-9d

Find the equivalent resistance of the circuit below.

::: figure assets/practice/hk5-drill-problem-2-9d-11.jpg

:::

```sym 7
s\er("r10,1,2,10:r5,2,3,5:r1,2,0,30:e,1,0,20ir1",3,0)
```
```sym 8
s\er("r10,1,2,10:r5,2,3,5:r1,2,0,30:e,1,0,20ir1",3,0)
```
```field 9 Circuit Description
r10,1,2,10
r5,2,3,5
r1,2,0,30
e1,1,0,20*i_r1
```

::: only 7,8
Choose DC. Wait for *Done*. Evaluate `req`. The equivalent resistance is
**20** Ω.
:::
::: only 9
*Find equivalent*, *Impedance*, nodes **3** and **0**, in DC: `req` is
{{o:20}} Ω.
:::

:::

::: problem Bo2's Example 3.12

Find the equivalent resistance of the circuit below.

::: figure assets/practice/bo2s-example-3-12-12.jpg

:::

```sym 7
s\er("r1,1,0,6:r4,a,0,4:e,a,1,6ir1",a,0)
```
```sym 8
s\er("r1,1,0,6:r4,a,0,4:e,a,1,6ir1",a,0)
```
```field 9 Circuit Description
r1,1,0,6
r4,a,0,4
e1,a,1,6*i_r1
```

::: only 7,8
Choose DC. Wait for *Done*. Evaluate `req`. The equivalent resistance is
**3** Ω.
:::
::: only 9
*Find equivalent*, *Impedance*, nodes **a** and **0**, in DC: `req` is
{{o:3}} Ω.
:::

:::

::: problem B11's Example 9.7

Find the Thévenin equivalent of the circuit below, as seen from the
R{{sub:3}} resistor.

::: figure assets/practice/b11s-example-9-7-13.jpg

:::

```sym 7
s\th("j,0,1,12:r1,1,0,4:r2,1,a,2",a,0)
```
```sym 8
s\th("j,0,1,12:r1,1,0,4:r2,1,a,2",a,0)
```
```field 9 Circuit Description
j,0,1,12
r1,1,0,4
r2,1,a,2
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **a** in the first and **0** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `vth` we find V{{sub:TH}} = **48** V. Via `req` we find
R{{sub:EQ}} = **6** Ω.

:::

::: problem B11's Example 9.11

Find the Norton equivalent of the circuit below, as seen from the R{{sub:L}}
resistor.

::: figure assets/practice/b11s-example-9-11-14.jpg

:::

```sym 7
s\th("e,1,0,9:r1,1,2,3:r2,2,0,6",2,0)
```
```sym 8
s\th("e,1,0,9:r1,1,2,3:r2,2,0,6",2,0)
```
```field 9 Circuit Description
e1,1,0,9
r1,1,2,3
r2,2,0,6
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **2** in the first and **0** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `ino` we find I{{sub:NO}} = **3** A. Via `req` we find
R{{sub:EQ}} = **2** Ω.

:::

::: problem AS2's Practice Problem 4.12

Find the Norton equivalent of the circuit below.

::: figure assets/practice/as2s-practice-problem-4-12-15.jpg

:::

```sym 7
s\th("r6,1,0,6:j,0,1,10:r2,x,0,2:e,1,x,2vx",x,0)
```
```sym 8
s\th("r6,1,0,6:j,0,1,10:r2,x,0,2:e,1,x,2vx",x,0)
```
```field 9 Circuit Description
r6,1,0,6
j,0,1,10
r2,x,0,2
e1,1,x,2*vx
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **x** in the first and **0** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `ino` we find I{{sub:NO}} = **10** A. Via `req` we find
R{{sub:EQ}} = **1** Ω.

:::

::: problem B11's Example 9.12

::: figure assets/practice/b11s-example-9-12-16.jpg

:::

Find the Norton equivalent of the circuit, as seen from the R{{sub:L}}
resistor.

```sym 7
s\th("r2,1,0,4:r1,1,2,5:j,1,2,10",2,0)
```
```sym 8
s\th("r2,1,0,4:r1,1,2,5:j,1,2,10",2,0)
```
```field 9 Circuit Description
r2,1,0,4
r1,1,2,5
j,1,2,10
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **2** in the first and **0** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `ino` we find I{{sub:NO}} = **5.56** A. Via `req` we find
R{{sub:EQ}} = **9** Ω.

:::

::: problem HK5's Drill Problem 2-8b

Find the Thévenin equivalent of the circuit below.

::: figure assets/practice/hk5s-drill-problem-2-8b-17.jpg

:::

```sym 7
s\th("j,0,2,0.01v1:r,0,2,20:e,1,2,100",1,0)
```
```sym 8
s\th("j,0,2,0.01v1:r,0,2,20:e,1,2,100",1,0)
```
```field 9 Circuit Description
j,0,2,0.01*v1
r,0,2,20
e1,1,2,100
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **1** in the first and **0** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `vth` we find V{{sub:TH}} = **125** V. Via `req` we find
R{{sub:EQ}} = **25** Ω.

:::

::: problem HK5's Figure 2-27

Find the Thévenin equivalent of the circuit below.

::: figure assets/practice/hk5s-figure-2-27-18.jpg

:::

```sym 7
s\th("e,1,0,4:r2,1,2,2'k:r3,2,x,3'k:j,0,2,vx/4000",x,0)
```
```sym 8
s\th("e,1,0,4:r2,1,2,2'k:r3,2,x,3'k:j,0,2,vx/4000",x,0)
```
```field 9 Circuit Description
e1,1,0,4
r2,1,2,2'k
r3,2,x,3'k
j,0,2,vx/4000
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **x** in the first and **0** in the second — the pair of terminals you are looking into.
:::

Via `vth` we find V{{sub:TH}} = **8** V. Via `req` we find R{{sub:EQ}} =
**10** kΩ.

:::

::: problem B11's Example 9.8

Find the Thévenin equivalent of the circuit below, as seen from the
R{{sub:4}} resistor.

I ignore the textbook's decision to call the nodes **a** and **b**, since b
is ground anyway.

::: figure assets/practice/b11s-example-9-8-19.jpg

:::

```sym 7
s\th("r1,2,0,6:r2,2,1,4:r3,1,0,2:e,0,1,8",2,0)
```
```sym 8
s\th("r1,2,0,6:r2,2,1,4:r3,1,0,2:e,0,1,8",2,0)
```
```field 9 Circuit Description
r1,2,0,6
r2,2,1,4
r3,1,0,2
e1,0,1,8
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **2** in the first and **0** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `vth` we get V{{sub:TH}}= **-4.8** V. Via `req` we get
R{{sub:EQ}}= **2.4** Ω.

:::

::: problem B11's Example 8.6

Find the Norton equivalent of the circuit below.

::: figure assets/practice/b11s-example-8-6-20.jpg

:::

```sym 7
s\th("j1,0,1,6:r1,1,0,3:j2,1,0,10:r2,1,0,6",1,0)
```
```sym 8
s\th("j1,0,1,6:r1,1,0,3:j2,1,0,10:r2,1,0,6",1,0)
```
```field 9 Circuit Description
j1,0,1,6
r1,1,0,3
j2,1,0,10
r2,1,0,6
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **1** in the first and **0** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `ino` we find I{{sub:NO}} = **-4** A. Via `req` we find
R{{sub:EQ}} = **2** Ω.

:::

::: problem Bo2's Drill Exercise 3.12

Find the Norton equivalent of the circuit below.

::: figure assets/practice/bo2s-drill-exercise-3-12-21.jpg

:::

```sym 7
s\th("e,1,0,12:r6,1,2,6:j,0,2,3ir6:r3,2,0,3",2,0)
```
```sym 8
s\th("e,1,0,12:r6,1,2,6:j,0,2,3ir6:r3,2,0,3",2,0)
```
```field 9 Circuit Description
e1,1,0,12
r6,1,2,6
j,0,2,3*ir6
r3,2,0,3
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **2** in the first and **0** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `ino` we find I{{sub:NO}} = **8** A. Via `req` we find
R{{sub:EQ}} = **1** Ω.

:::

::: problem Bo2's Drill Exercise 3.9

Find the Thévenin equivalent of the circuit below.

::: figure assets/practice/bo2s-drill-exercise-3-9-22.jpg

:::

```sym 7
s\th("j,b,0,10:r1,0,b,1:e,a,0,3ir1:r6,a,b,6",a,b)
```
```sym 8
s\th("j,b,0,10:r1,0,b,1:e,a,0,3ir1:r6,a,b,6",a,b)
```
```field 9 Circuit Description
j,b,0,10
r1,0,b,1
e1,a,0,3*ir1
r6,a,b,6
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **a** in the first and **b** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `vth` we find V{{sub:TH}} = **24** V. Via `req` we find
R{{sub:EQ}} = **2.4** Ω.

:::

::: problem AS2's Example 4.12

Find Norton equivalent of the circuit below.

::: figure assets/practice/as2s-example-4-12-23.jpg

:::

```sym 7
s\th("rx,0,b,4:e,0,b,10:r5,0,a,5:j,0,a,2irx",a,b)
```
```sym 8
s\th("rx,0,b,4:e,0,b,10:r5,0,a,5:j,0,a,2irx",a,b)
```
```field 9 Circuit Description
rx,0,b,4
e1,0,b,10
r5,0,a,5
j,0,a,2*irx
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **a** in the first and **b** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `ino` we find I{{sub:NO}} = **7** A. Via `req` we find
R{{sub:EQ}} = **5** Ω.

:::

::: problem B11's Example 9.10 (Hidden source)

Find the Thévenin equivalent of the circuit below.

::: figure assets/practice/b11s-example-9-10-hidden-source-24.jpg

:::

My solution is below:

```sym 7
s\th("e1,3,0,-6:e2,4,0,10:r1,2,3,0.8'k:
r2,2,4,4'k:r3,2,0,6'k:r4,2,1,1.4'k",1,0)
```
```sym 8
s\th("e1,3,0,–6:e2,4,0,10:r1,2,3,0.8'k:
r2,2,4,4'k:r3,2,0,6'k:r4,2,1,1.4'k",1,0)
```
```field 9 Circuit Description
e1,3,0,-6
e2,4,0,10
r1,2,3,0.8'k
r2,2,4,4'k
r3,2,0,6'k
r4,2,1,1.4'k
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **1** in the first and **0** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `vth` we find V{{sub:TH}} = -**3** V. Via `req` we find
R{{sub:EQ}} = **2** kΩ.

:::

::: problem B11's Example 9.9

Find the Thévenin equivalent of the circuit below, as seen from the
R{{sub:L}} resistor.

::: figure assets/practice/b11s-example-9-9-25.jpg

:::

```sym 7
s\th("e,1,0,72:r1,1,b,6:r2,1,a,12:r3,0,b,3:r4,0,a,4",b,a)
```
```sym 8
s\th("e,1,0,72:r1,1,b,6:r2,1,a,12:r3,0,b,3:r4,0,a,4",b,a)
```
```field 9 Circuit Description
e1,1,0,72
r1,1,b,6
r2,1,a,12
r3,0,b,3
r4,0,a,4
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **b** in the first and **a** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `vth` we find V{{sub:TH}} = **6** V. Via `req` we find
R{{sub:EQ}} = **5** Ω.

:::

::: problem AS2's Example 4.11

Find the Norton equivalent of the circuit below.

::: figure assets/practice/as2s-example-4-11-26.jpg

:::

```sym 7
s\th("j,0,2,2:e,4,0,12:r1,2,4,4:r2,2,3,8:r3,0,1,8:r4,3,1,5",3,1)
```
```sym 8
s\th("j,0,2,2:e,4,0,12:r1,2,4,4:r2,2,3,8:r3,0,1,8:r4,3,1,5",3,1)
```
```field 9 Circuit Description
j,0,2,2
e1,4,0,12
r1,2,4,4
r2,2,3,8
r3,0,1,8
r4,3,1,5
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **3** in the first and **1** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `ino` we find I{{sub:NO}} = **1** A. Via `req` we find
R{{sub:EQ}} = **4** Ω.

:::

::: problem HK5's Drill Problem 2-8a

Find the Thévenin equivalent of the circuit below.

::: figure assets/practice/hk5s-drill-problem-2-8a-27.jpg

:::

```sym 7
s\th("e1,1,0,100:r2,1,2,20:j,0,2,4:r1,2,3,10:e5,3,4,50",4,0)
```
```sym 8
s\th("e1,1,0,100:r2,1,2,20:j,0,2,4:r1,2,3,10:e5,3,4,50",4,0)
```
```field 9 Circuit Description
e1,1,0,100
r2,1,2,20
j,0,2,4
r1,2,3,10
e5,3,4,50
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **4** in the first and **0** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `vth` we find V{{sub:TH}} = **130** V. Via `req` we find
R{{sub:EQ}} = **30** Ω.

:::

::: problem B11's Example 8.7

Find Norton equivalent of the circuit below.

::: figure assets/practice/b11s-example-8-7-28.jpg

:::

```sym 7
s\th("j7,0,1,7:j3,1,0,3:r1,1,0,4:j4,0,1,4",1,0)
```
```sym 8
s\th("j7,0,1,7:j3,1,0,3:r1,1,0,4:j4,0,1,4",1,0)
```
```field 9 Circuit Description
j7,0,1,7
j3,1,0,3
r1,1,0,4
j4,0,1,4
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **1** in the first and **0** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `ino` we find I{{sub:NO}} = **8** A. Via `req` we find
R{{sub:EQ}} = **4** Ω.

:::

::: problem AS2's Practice Problem 4.9

Find the Thévenin equivalent of the circuit below.

::: figure assets/practice/as2s-practice-problem-4-9-29.jpg

:::

```sym 7
s\th("e,1,0,6:r5,1,2,5:rx,2,3,3:j,0,2,1.5irx:r4,3,0,4",3,0)
```
```sym 8
s\th("e,1,0,6:r5,1,2,5:rx,2,3,3:j,0,2,1.5irx:r4,3,0,4",3,0)
```
```field 9 Circuit Description
e1,1,0,6
r5,1,2,5
rx,2,3,3
j,0,2,1.5*irx
r4,3,0,4
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **3** in the first and **0** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `vth` we find V{{sub:TH}} = **5.33** V. Via `req` we find
R{{sub:EQ}} = **0.44** Ω.

:::

::: problem AS2's Example 4.9

Find the Thévenin equivalent of the circuit below.

::: figure assets/practice/as2s-example-4-9-30.jpg

:::

```sym 7
s\th("j,b,0,5:rx,0,b,4:r1,0,1,2:r2,1,b,6:r3,1,a,2:e,1,0,2vrx",a,b)
```
```sym 8
s\th("j,b,0,5:rx,0,b,4:r1,0,1,2:r2,1,b,6:r3,1,a,2:e,1,0,2vrx",a,b)
```
```field 9 Circuit Description
j,b,0,5
rx,0,b,4
r1,0,1,2
r2,1,b,6
r3,1,a,2
e1,1,0,2*vrx
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **a** in the first and **b** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `vth` we find V{{sub:TH}} = **20** V. Via `req` we find
R{{sub:EQ}} = **6** Ω.

:::

::: problem Bo2's Drill Exercise 3.8

Find the Thévenin equivalent of the circuit below.

::: figure assets/practice/bo2s-drill-exercise-3-8-31.jpg

:::

```sym 7
s\th("j,0,1,3:r1,0,1,1:r6,1,2,6:r10,1,3,10:r8,2,0,8:r2,2,3,2",3,0)
```
```sym 8
s\th("j,0,1,3:r1,0,1,1:r6,1,2,6:r10,1,3,10:r8,2,0,8:r2,2,3,2",3,0)
```
```field 9 Circuit Description
j,0,1,3
r1,0,1,1
r6,1,2,6
r10,1,3,10
r8,2,0,8
r2,2,3,2
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **3** in the first and **0** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `vth` we find V{{sub:TH}} = **2** V. Via `req` we find
R{{sub:EQ}} = **4** Ω.

:::

::: problem B11's Example 9.13

Find Norton equivalent of the shaded part of the circuit.

::: figure assets/practice/b11s-example-9-13-32.jpg

:::

```sym 7
s\th("e1,1,0,7:r1,1,a,4:j,a,0,8:r2,a,0,6",a,0)
```
```sym 8
s\th("e1,1,0,7:r1,1,a,4:j,a,0,8:r2,a,0,6",a,0)
```
```field 9 Circuit Description
e1,1,0,7
r1,1,a,4
j,a,0,8
r2,a,0,6
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **a** in the first and **0** in the second — the pair of terminals you are looking into.
:::

Choose DC. Via `ino` we find I{{sub:NO}} = **-6.25** A. Via `req` we find
R{{sub:EQ}} = **2.4** Ω.

:::

### Tricky problems

Some circuit theory books – and some professors – find it entertaining or
instructive to surprise unsuspecting students with tricky problems, like the
two we solve below.

::: problem Bo2's Example 3.11 (Tricky)

Find the Norton equivalent of the circuit below.

::: figure assets/practice/bo2s-example-3-11-tricky-33.jpg

:::

Since you do not know beforehand that this is a tricky problem, you go for
the usual:

```sym 7
s\th("r2,0,b,2:r8,0,2,8:r3,2,a,3:r1,1,a,1:e,1,0,1:j,2,b,3ir8",a,b)
```
```sym 8
s\th("r2,0,b,2:r8,0,2,8:r3,2,a,3:r1,1,a,1:e,1,0,1:j,2,b,3ir8",a,b)
```
```field 9 Circuit Description
r2,0,b,2
r8,0,2,8
r3,2,a,3
r1,1,a,1
e1,1,0,1
j,2,b,3*ir8
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **a** in the first and **b** in the second — the pair of terminals you are looking into.
:::

{{v7,8|You choose DC, press Enter and wait. Symbulator reports the
calculator was unable to solve the equations.}}{{v9|Run it in DC and it is
refused: *Could not solve the system of equations.*}} This often means there
is a division by zero somewhere.

{{v7,8|Clean the variables from the MAIN folder and try again, this time –
following Symbulator's advise –using a symbolic value.}}{{v9|Symbulator's own
advice is to try again with a symbolic value, which is what we do.}} We chose
to use **x** instead of **3** in the dependent source.

```sym 7
s\th("r2,0,b,2:r8,0,2,8:r3,2,a,3:r1,1,a,1:e,1,0,1:j,2,b,x*ir8",a,b)
```
```sym 8
s\th("r2,0,b,2:r8,0,2,8:r3,2,a,3:r1,1,a,1:e,1,0,1:j,2,b,x*ir8",a,b)
```
```field 9 Circuit Description
r2,0,b,2
r8,0,2,8
r3,2,a,3
r1,1,a,1
e1,1,0,1
j,2,b,x*ir8
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **a** in the first and **b** in the second — the pair of terminals you are looking into.
:::

Now it solves. The expression for `ino` is fine, but the one for `req`,
$(9x-35)/(4(x-3))$, will divide by zero at $x = 3$ — the very value we
replaced.

::: only 7,8
Via `Define x=3: {ino,req} `we find that I{{sub:NO}} = **1** A, and
R{{sub:EQ}} is undefined.
:::
::: only 9
Put `x = 3` in **Add conditions** and run it again: I{{sub:NO}} = **1** A,
and R{{sub:EQ}} is undefined.
:::

This means the equivalent resistance is, for practical purposes, infinite.
Your idea of fun, right?

:::

::: problem Bo2's Drill Exercise 3.13 (Tricky)

Below is another tricky problem. Find the Norton equivalent of the circuit
below.

::: figure assets/practice/bo2s-drill-exercise-3-13-tricky-34.jpg

:::

As in the previous example, we get an error if we simulate using **2** and
**3** in the dependent sources. So, we use **2x** and **3x** instead, where
**x** will be later defined as 1.

```sym 7
s\th("ei,1,b,6:ed,b,0,2*x*ir2:r1,1,0,6:r2,0,a,2:jd,a,0,3*x*ir1",a,b)
```
```sym 8
s\th("ei,1,b,6:ed,b,0,2*x*ir2:r1,1,0,6:r2,0,a,2:jd,a,0,3*x*ir1",a,b)
```
```field 9 Circuit Description
ei,1,b,6
ed,b,0,2*x*ir2
r1,1,0,6
r2,0,a,2
jd,a,0,3*x*ir1
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **a** in the first and **b** in the second — the pair of terminals you are looking into.
:::

Exploring the answers, we see that the denominator of the expression for`
req,` (x-1), given that x=1), results in a division by zero. Via
`1→x:{ino,req} `we find that I{{sub:NO}} = -3A, and R{{sub:EQ}} is undefined
or, for practical purposes, infinite:

:::

::: problem TR5's Exercise 4-6 (Symbolic)

::: figure assets/practice/tr5s-exercise-4-6-symbolic-35.jpg

:::

First let's find the input resistance, R{{sub:IN}}, e.g. the resistance as
seen by the v{{sub:S}} source. We use **μ** for the constant in the dependent
source.

```sym 7
s\dc("ei,3,0,vs:rf,3,2,rf:ro,2,t,ro:ed,2,0,μ*vrf"):rei
```
```sym 8
s\dc("ei,3,0,vs:rf,3,2,rf:ro,2,t,ro:ed,2,0,μ*vrf"):rei
```
```field 9 Circuit Description
ei,3,0,vs
rf,3,2,rf
ro,2,t,ro
ed,2,0,μ*vrf
```

::: only 9
The answer you want is `rei`, in **Results**.
:::

We get `rf*(µ+1)`, which is correct. The textbook's answers are shown right
of the circuit schematic. Now we find the output Thévenin equivalent circuit
as seen by R{{sub:L}}.

```sym 7
s\th("ei,3,0,vs:rf,3,2,rf:ro,2,t,ro:ed,2,0,μ*vrf",t,0):{vth,req}
```
```sym 8
s\th("ei,3,0,vs:rf,3,2,rf:ro,2,t,ro:ed,2,0,μ*vrf",t,0):{vth,req}
```
```field 9 Circuit Description
ei,3,0,vs
rf,3,2,rf
ro,2,t,ro
ed,2,0,μ*vrf
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **t** in the first and **0** in the second — the pair of terminals you are looking into.

The answers you want are `vth` and `req`, in **Results**.
:::

We get `{vs*µ/(µ+1),ro}`, which is correct, as can be seen in the textbook's
answers for v{{sub:T}} and R{{sub:T}}, shown right of the circuit schematic
above.

:::

::: problem TR5's Example 4-8 (Symbolic)

Find the Thévenin equivalent as seen by the load.

::: figure assets/practice/tr5s-example-4-8-symbolic-36.jpg

:::

My answer starts by defining **v**{{sub:x}} as **va-vb**. This is done thus:

```sym 7
Define vx=va-vb
```
```sym 8
Define vx=va-vb
```

Now I run the th script, with the circuit description shown below:

```sym 7
s\th("ei,a,0,vs:ed,1,0,μ*(vx):ro,b,1,ro",b,0):
{vth,req}
```
```sym 8
s\th("ei,a,0,vs:ed,1,0,μ*(vx):ro,b,1,ro",b,0):
{vth,req}
```
```field 9 Circuit Description
ei,a,0,vs
ed,1,0,μ*(vx)
ro,b,1,ro
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **b** in the first and **0** in the second — the pair of terminals you are looking into.

The answers you want are `vth` and `req`, in **Results**.
:::

The answers we get, **{vs\*µ/(µ+1**),**ro/(µ+1)}**, are correct, as can be
seen by comparing them to those in the book:

::: figure assets/practice/tr5s-example-4-8-symbolic-37.jpg

:::

I am not sure there is any other circuit simulator for calculators that can
do this.

:::

::: problem AS2's Example 4.8

Find the Thévenin equivalent of the circuit shown to the left of terminals
a-b. Then find the current through RL = 6, 16 and 36Ω.

::: figure assets/practice/as2s-example-4-8-38.jpg

:::

My solution below.

```sym 7
s\th("e,1,0,32.:r4,1,2,4:r12,2,0,12:j,0,2,2:r1,2,3,1",3,0):
{vth,req,irL|Load=6,irL|Load=16,irL|Load=36}
```
```sym 8
s\th("e,1,0,32.:r4,1,2,4:r12,2,0,12:j,0,2,2:r1,2,3,1",3,0):
{vth,req,irL|Load=6,irL|Load=16,irL|Load=36}
```
```field 9 Circuit Description
e1,1,0,32.
r4,1,2,4
r12,2,0,12
j,0,2,2
r1,2,3,1
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **3** in the first and **0** in the second — the pair of terminals you are looking into.

The answers you want are `vth` and `req`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
irL|Load=6
irL|Load=16
irL|Load=36
```
:::

Select DC when asked. Answer Y when offered the load formulas.

The answer, **{30.,4.,3.,1.5,.75}**, is correct.

:::

::: problem Bo2's Example 3.10

Find the Norton equivalent of the circuit left of the a-b terminals, and then
find the voltage drop and the current through the ¼ Ω resistor. My one-line
solution below.

::: figure assets/practice/bo2s-example-3-10-39.jpg

:::

```sym 7
s\th("e,3,0,3:r31,3,1,1/2:r10,1,0,1/2:r12,1,2,1/4:j,2,0,v1/2",2,0):
{ino,req,vrL|Load=1/4,irL|Load=1/4}
```
```sym 8
s\th("e,3,0,3:r31,3,1,1/2:r10,1,0,1/2:r12,1,2,1/4:j,2,0,v1/2",2,0):
{ino,req,vrL|Load=1/4,irL|Load=1/4}
```
```field 9 Circuit Description
e1,3,0,3
r31,3,1,1/2
r10,1,0,1/2
r12,1,2,1/4
j,2,0,v1/2
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **2** in the first and **0** in the second — the pair of terminals you are looking into.

The answers you want are `ino` and `req`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
vrL|Load=1/4
irL|Load=1/4
```
:::

Select DC when asked. Answer Y when offered the load formulas.

The book gives the answers as fractions. We get it right:
**{21/8,4/9**,**21/50,42/25}. **

:::

::: problem RM3's Example 9-7

Find the Norton equivalent of the circuit external to R{{sub:L}}. Then
determine the load current I{{sub:L}} when R{{sub:L}} = 0 Ω, 2'k Ω and 5'k Ω.
My one-line solution below.

::: figure assets/practice/rm3s-example-9-7-40.jpg

:::

```sym 7
s\th("e,1,0,15.:r1,1,2,6'k:j,0,2,5'm:r2,2,0,2'k",2,0):
{ino,req, irL|Load=0,irL|Load=2000,irL|Load=5000}
```
```sym 8
s\th("e,1,0,15.:r1,1,2,6'k:j,0,2,5'm:r2,2,0,2'k",2,0):
{ino,req, irL|Load=0,irL|Load=2000,irL|Load=5000}
```
```field 9 Circuit Description
e1,1,0,15.
r1,1,2,6'k
j,0,2,5'm
r2,2,0,2'k
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **2** in the first and **0** in the second — the pair of terminals you are looking into.

The answers you want are `ino` and `req`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
irL|Load=0
irL|Load=2000
irL|Load=5000
```
:::

Select DC when asked. Answer Y when offered the load formulas.

The answer, **{.0075,1500.**,**.0075,.00321,.00173}**, is correct.

:::

::: problem Bo2's Example 3.5

Find the Norton equivalent of the circuit external to the 1Ω resistor. Then
determine the voltage drop across this 1Ω resistor.

::: figure assets/practice/bo2s-example-3-5-41.jpg

:::

My solution below.

```sym 7
s\th("e,1,0,24:r12,1,2,12:r20,2,0,4:r23,2,3,4:r34,3,4,2:
j,4,0,3:r40,4,0,5",3,0):{ino,req,vrL|Load=1}
```
```sym 8
s\th("e,1,0,24:r12,1,2,12:r20,2,0,4:r23,2,3,4:r34,3,4,2:
j,4,0,3:r40,4,0,5",3,0):{ino,req,vrL|Load=1}
```
```field 9 Circuit Description
e1,1,0,24
r12,1,2,12
r20,2,0,4
r23,2,3,4
r34,3,4,2
j,4,0,3
r40,4,0,5
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **3** in the first and **0** in the second — the pair of terminals you are looking into.

The answers you want are `ino` and `req`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
vrL|Load=1
```
:::

Select DC when asked. Answer Y when offered the load formulas.

The answer, **{-9/7,7/2,-1}**, is correct.

:::

::: problem RM3's Example 9-13

Use Millman's Theorem to simplify the circuit left of a-b so that there is
only one voltage and one resistor. Then find the current in the load resistor
R{{sub:L}}.

::: figure assets/practice/rm3s-example-9-13-42.jpg

:::

I don't know Millman's Theorem, but in my book this is called the Thévenin
equivalent.

```sym 7
s\th("r1,0,1,240.:e1,2,1,96:r2,0,3,200:e2,3,2,40:
r3,0,4,800:e3,2,4,80",2,0):{vth,req,irL|Load=192}
```
```sym 8
s\th("r1,0,1,240.:e1,2,1,96:r2,0,3,200:e2,3,2,40:
r3,0,4,800:e3,2,4,80",2,0):{vth,req,irL|Load=192}
```
```field 9 Circuit Description
r1,0,1,240.
e1,2,1,96
r2,0,3,200
e2,3,2,40
r3,0,4,800
e3,2,4,80
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **2** in the first and **0** in the second — the pair of terminals you are looking into.

The answers you want are `vth` and `req`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
irL|Load=192
```
:::

Select DC when asked. Answer Y when offered the load formulas.

The answer, **{28.8,96.,.1}**, is correct.

:::

::: problem Bo2's Example 3.7

Find the Thévenin equivalent for the circuit left of a-b. Then find the
voltage across the 3 Ω resistor, and also if it was 6 Ω. My answer is
presented below.

::: figure assets/practice/bo2s-example-3-7-43.jpg

:::

```sym 7
s\th("e,1,0,20:r6,1,2,6:r1,1,3,1:r2,3,2,2:j32,3,2,15:j30,3,0,15",2,0):
{vth,req,vrL|Load=3,vrL|Load=6.}
```
```sym 8
s\th("e,1,0,20:r6,1,2,6:r1,1,3,1:r2,3,2,2:j32,3,2,15:j30,3,0,15",2,0):
{vth,req,vrL|Load=3,vrL|Load=6.}
```
```field 9 Circuit Description
e1,1,0,20
r6,1,2,6
r1,1,3,1
r2,3,2,2
j32,3,2,15
j30,3,0,15
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **2** in the first and **0** in the second — the pair of terminals you are looking into.

The answers you want are `vth` and `req`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
vrL|Load=3
vrL|Load=6.
```
:::

Select DC when asked. Answer Y when offered the load formulas.

The answer we find, **{30,2,18,22.5}**, is correct.

:::

::: problem Bo2's Drill Exercise 3.7

Find the Thévenin equivalent for the circuit left of a-b. Then find the
voltage *v*.

My answer below.

::: figure assets/practice/bo2s-drill-exercise-3-7-44.jpg

:::

```sym 7
s\th("e,1,0,8:r3,1,2,3:r12,1,3,12:r6,2,0,6:r2,2,3,2",3,0):
{vth,req,vrL|Load=5.}
```
```sym 8
s\th("e,1,0,8:r3,1,2,3:r12,1,3,12:r6,2,0,6:r2,2,3,2",3,0):
{vth,req,vrL|Load=5.}
```
```field 9 Circuit Description
e1,1,0,8
r3,1,2,3
r12,1,3,12
r6,2,0,6
r2,2,3,2
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **3** in the first and **0** in the second — the pair of terminals you are looking into.

The answers you want are `vth` and `req`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
vrL|Load=5.
```
:::

Select DC when asked. Answer Y when offered the load formulas.

The answer, **{6,3,3.75}**, is correct.

:::

::: problem RM3's Practice Problem 9.5

::: figure assets/practice/rm3s-practice-problem-9-5-45.jpg

:::

My solution below.

```sym 7
s\th("e1,1,0,35.:r1,1,2,15'k:r2,2,3,60'k:e2,3,0,70:r3,2,4,30'k",4,0):
{ino,req,irL|Load=0,irL|Load=1e4,irL|Load=5e4,irL|Load=1e5}
```
```sym 8
s\th("e1,1,0,35.:r1,1,2,15'k:r2,2,3,60'k:e2,3,0,70:r3,2,4,30'k",4,0):
{ino,req,irL|Load=0,irL|Load=1e4,irL|Load=5e4,irL|Load=1e5}
```
```field 9 Circuit Description
e1,1,0,35.
r1,1,2,15'k
r2,2,3,60'k
e2,3,0,70
r3,2,4,30'k
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **4** in the first and **0** in the second — the pair of terminals you are looking into.

The answers you want are `ino` and `req`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
irL|Load=0
irL|Load=1e4
irL|Load=5e4
irL|Load=1e5
```
:::

Select DC when asked. Answer Y when offered the load formulas.

The answer, **{.001,42000**,**.001**,.**000808**,.**000457**,.**00296}**, is
correct.

:::

### Power transfer problems

::: problem AS2's Example 4.13

Find the R{{sub:L}} value for maximum power transfer and the maximum power
transferred.

::: figure assets/practice/as2s-example-4-13-46.jpg

:::

R{{sub:L}} for maximum transfer is **rEq**. The maximum power is in **pMax**.
My solution below:

```sym 7
s\th("e,1,0,12:r6,1,2,6:r12,2,0,12:r3,2,3,3:j,0,3,2:r2,3,4,2",4,0):
approx({req,pmax})
```
```sym 8
s\th("e,1,0,12:r6,1,2,6:r12,2,0,12:r3,2,3,3:j,0,3,2:r2,3,4,2",4,0):
approx({req,pmax})
```
```field 9 Circuit Description
e1,1,0,12
r6,1,2,6
r12,2,0,12
r3,2,3,3
j,0,3,2
r2,3,4,2
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **4** in the first and **0** in the second — the pair of terminals you are looking into.

The answers you want are `req` and `pmax`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

Select DC. You can answer N when asked about the load equations. The answer,
**{9.,13.44}**, is correct: the maximum transfer of power occurs when the
load is 9Ω. At this point, the power transferred is 13.44W. Now let's solve
another one.

:::

::: problem AS2's Practice Problem 4.13

Find the R{{sub:L}} value for maximum power transfer and the maximum power
transferred.

::: figure assets/practice/as2s-practice-problem-4-13-47.jpg

:::

```sym 7
s\th("ei,1,0,9:rx,1,2,2:r1,2,4,1:ed,4,0,3vrx:r4,2,3,4",3,0):
approx({req,pmax})
```
```sym 8
s\th("ei,1,0,9:rx,1,2,2:r1,2,4,1:ed,4,0,3vrx:r4,2,3,4",3,0):
approx({req,pmax})
```
```field 9 Circuit Description
ei,1,0,9
rx,1,2,2
r1,2,4,1
ed,4,0,3*vrx
r4,2,3,4
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **3** in the first and **0** in the second — the pair of terminals you are looking into.

The answers you want are `req` and `pmax`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

Select DC. You can answer N. The logic of this problem is identical to the
previous one. The answer is **{4.22,2.901}**.

:::

::: problem B11's Example 9.15

::: figure assets/practice/b11s-example-9-15-48.jpg

:::

::: figure assets/practice/b11s-example-9-15-49.jpg

:::

My one-line solution to all three questions is presented below.

```sym 7
s\th("j,0,1,10'm:rs,1,0,40'k",1,0):
{req,pmax,prl|load=68000.,prl|load=8200.}
```
```sym 8
s\th("j,0,1,10'm:rs,1,0,40'k",1,0):
{req,pmax,prl|load=68000.,prl|load=8200.}
```
```field 9 Circuit Description
j,0,1,10'm
rs,1,0,40'k
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **1** in the first and **0** in the second — the pair of terminals you are looking into.

The answers you want are `req` and `pmax`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
prl|load=68000.
prl|load=8200.
```
:::

Select DC and answer Y about the load formulas. The answer we obtain,
**{40000,1,.93,.57}**, is correct. Let's deconstruct it.

Part (a) is answered by the first two values: a 40'k Ω resistor as load would
receive 1W power. Since this is the maximum – this is the most that any load
could receive ever.

Parts (b) is answered by the third value. Making use of the variable **prL**,
which contains the power delivered by the circuit equivalent to the load, as
a function of the load value **L**, we find that a load of 68'kΩ receives
.93W, which is less than the maximum.

Parts (c) is answered in similar manner by the fourth value. A load of 8.2'kΩ
receives .57W, which is less than the maximum. Any resistance other than 40'k
gets less power.

:::

::: problem B11's Example 9.17

::: figure assets/practice/b11s-example-9-17-50.jpg

:::

Find the R{{sub:L}} value for maximum power transfer and the maximum power
transferred.

```sym 7
s\th("j,2,0,6:r2,2,0,10:r1,2,3,3:r3,0,1,2:e,3,4,68",4,1):
approx({req,pmax})
```
```sym 8
s\th("j,2,0,6:r2,2,0,10:r1,2,3,3:r3,0,1,2:e,3,4,68",4,1):
approx({req,pmax})
```
```field 9 Circuit Description
j,2,0,6
r2,2,0,10
r1,2,3,3
r3,0,1,2
e1,3,4,68
```

::: only 9
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to *Thévenin / Norton*. Two node boxes appear: put **4** in the first and **1** in the second — the pair of terminals you are looking into.

The answers you want are `req` and `pmax`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

Select DC. You can answer N. Answer is **{15.,273.07}. **Let's now see one
that is a little different.

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
