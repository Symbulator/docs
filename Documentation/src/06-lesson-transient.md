---
id: lesson-transient
kind: lesson
title: Transient analysis
updated: 2023-07-08
summary: >
  Learn to run a *transient* time-domain analysis with **tr**. Learn to
  describe *capacitors* with **c** and *inductors* with **l**. Save time with
  the **only** tool. Plot expressions in time with the **plot** tool.
---

Symbulator can simulate two types of energy-storing elements: capacitors and
inductors. It can conduct three types of analysis where these elements are
relevant: transient time-domain (TR) analysis, alternating current (AC)
analysis, and complex frequency-domain (FD) analysis. In this lesson we will
teach you how to conduct the transient analysis of a circuit, and how to
describe capacitors and inductors for it. AC and FD analysis are discussed in
subsequent lessons.

## How to describe a capacitor {#describe-capacitor}

::: note Describing capacitors
When describing an ideal capacitor for the purpose of a transient analysis, we
need five pieces of information, separated by commas: a unique name to identify
the capacitor (must start with the letter **c**), the names of its first and
second nodes, its value in farads (F), and its initial condition in volts,
understood as the voltage in the first node minus the voltage in the second.

For example, an ideal capacitor called **ca**, connected between two nodes
called **1** and **2**, with a capacitance of **3** F and an initial condition
of 0.1 V, would be described as follows: `ca,1,2,3,0.1`{{i:capacitor}}
:::

::: only 7
::: warning Can't use c#
The variables `c1` … `c99` are reserved by the calculator, and cannot be used
as names for capacitors. Instead, I recommend that you use letters (e.g. ca,
cb) or double c followed by a number (e.g. cc1, cc2).
:::
:::

### Values can use SI prefixes

The values of the capacitance and the initial condition of the capacitor can
use prefixes of the International System.

### What answers do you get

For each capacitor, a transient analysis will provide two answers: the voltage
drop in the capacitor, in volts, and the current through it, flowing from the
first node towards the second, in amperes.

::: note Note on capacitors in DC
In a DC simulation, the current through a capacitor is defined as 0. It
basically becomes an open circuit.
:::

## How to describe an inductor {#describe-inductor}

::: note Describing inductors
When describing an ideal inductor for the purpose of a transient analysis, we
need five pieces of information, separated by commas: a unique name to identify
the inductor (must start with the letter **l**), the names of its first and
second nodes, its value in henries (H), and its initial condition in amperes,
understood as the current flowing through it from the first node towards the
second.

For example, an ideal inductor called **l1**, connected between two nodes
called **1** and **2**, with an inductance of **0.1** H and an initial
condition of 0.2 A, would be described as follows: `l1,1,2,0.1,0.2`{{i:inductor}}
:::

For each inductor, a transient analysis will provide the voltage drop across it
and the current through it, with the same conventions as for capacitors.

::: note Note on inductors in DC
In a DC simulation, the voltage drop in an inductor is defined as 0. It
basically becomes a short circuit.
:::

## Running a transient analysis {#run-transient}

You will learn the subtleties of running transient simulations through a series
of examples. For now, suffice it to say that to run one we use
{{v7,8|an access program called **s\tr**, which takes one argument: the circuit
description in string form}}{{v9|the **tr** function, which takes the circuit
description and, optionally, the list of quantities you want back}}.

::: only 7
For transient simulations, Symbulator uses a software for Laplace transforms
called DiffEq, by Lars Frederiksen. Make sure you have it properly installed!
:::
::: only 8
For transient simulations, Symbulator uses the Laplace Functions by Lars
Frederiksen. Make sure you have them properly installed!
:::
::: only 9
For transient simulations, Symbulator 9 uses SymPy's own Laplace machinery.
There is nothing extra to install.
:::

::: problem Bo2's Example 4.15
::: figure assets/circuit/bo2e0415.jpg
Bo2's Example 4.15
:::

::: answer
For t ≤ 0 s, since the current source is inactive, there is nothing going on.
Without doing a simulation, we know the voltage v is 0 volts.

For 0 s < t ≤ 2 s, the source is active. By inspection of the graph, we learn
that for this interval the value of the source is t: the current in amperes is
the same as the time in seconds. We describe the circuit and run the transient
analysis:

```sym 7
s\tr("j,0,1,t:c,1,0,2,0")
```
```sym 8
s\tr("j,0,1,t:c,1,0,2,0")
```
```field 9 Circuit Description
j,0,1,t
c,1,0,2,0
```

The description of the source has four terms: name (starting with j), first
node, second node, and value. In this case the value is t. The description of
the capacitor has five terms: name, first node, second node, value in farads,
and its initial condition in volts. Here the initial condition is 0 volts.

Once the simulation is complete, ask for the value of the voltage, `vc`. We get
this value, which is correct:

```out
t^2/4
```

For 2 s < t, the voltage is equal to whatever value it had at time 2 s:

```sym 7
vc|t=2
```
```sym 8
vc|t=2
```
::: only 9
There is no `|t=2` on the web, but the **Solve** card will do it. Put both
lines in **Equation(s) to solve in terms of the results**, and name both
unknowns:

```field 9 Equation(s) to solve in terms of the results
x = vc
t = 2
```

```field 9 Unknown(s) to solve for
x, t
```

Naming `t` as an unknown is what makes the second equation bite: without it
the answer comes back still written in terms of t.
:::

We get a value of 1 volt, which is correct.
:::
:::

### Describing source values

For the purpose of a transient analysis, Symbulator accepts many types of
source values. The only thing you must do is describe these values properly.

**Step values: symbolic.** A source with an unknown step value starting at t=0
is described using a variable and the step function u(t). For example, a
voltage source e1, connected between nodes 1 and 0, with a value of V volts
starting at t=0, would be `e1,1,0,V*u(t)`.

**Step values: numerical.** A step source with a known numerical value can also
be described as above, `e1,1,0,12*u(t)`. However, to save some typing, when
your value is numerical you can skip the u(t), and Symbulator will assume it is
a numerical step value: `e1,1,0,12`. The results are the same.

**Impulse values.** A source with an impulse value at t=0 is described using
its value, symbolic or numerical, and the delta function δ(t). For example, a
current source j1, connected between nodes 0 and 1, with an impulse value of i
amperes at t=0, would be `j1,0,1,i*δ(t)`.

**Values as functions of time.** A source whose value is a function of time,
such as a ramp, a sinusoid or an exponential, is described by writing the value
as an expression in terms of t, as in `j,0,1,t`.
{{v7,8|Values as functions of t will activate the Impala mode, in order to save
time.}}

**Dependent values.** Sources with dependent values are described as we have
seen before, for example `j,0,1,3*vr1`.

### A word on intervals

For transient analyses, every time a switch opens or closes marks the end of
one time interval and the beginning of another. A simulation can only be done
for one time interval. When we run a TR simulation and get answers in terms of
t, this variable must be understood as the time elapsed since the start of
*that* interval in particular.

This is a distinction without a difference as long as the interval we simulate
starts at t=0, which is most often the case. However, sometimes problems have
switch changes at other times — Bo2's Example 5.6, where a switch closes at
t=1 s, and Bo2's Drill Exercise 5.6, where one closes at t=2 s, are examples in
the solved problems.

## Two useful tools {#tr-tools}

### The only tool

Unless you indicate otherwise, a Symbulator simulation will give you a whole
set of answers: voltages in all nodes, and voltage drops, currents and power
consumed in all elements. When the circuit has complicated symbolic
expressions, storing all these answers takes time.

::: only 7,8
In case you don't want all the answers, but only a chosen few, you may save
some time by using the **s\only** tool{{i:only tool}} to tell Symbulator —
before the simulation — which answers you want to save. Find it in Symbulator's
custom menu. Its argument is either an empty variable or a string with a
variable or a list of variables separated by commas. All of these are valid:

```sym 7
s\only(ir1)
s\only("ir1")
s\only("ir1,va,vr2")
```
```sym 8
s\only(ir1)
s\only("ir1")
s\only("ir1,va,vr2")
```

The s\only tool is valuable in TR analysis, because you can save time by not
having Symbulator find the inverse Laplace of answers that are not needed.
:::
::: only 9
In case you don't want all the answers, but only a chosen few, tick **Do you
want to limit the results to save time?** — it appears under the analysis
menus once you choose TR. A box opens asking **What results are you after?**
List them there, separated by commas:

```field 9 What results are you after? List the variables here
v2
```

This matters most in TR analysis, where each answer costs an inverse Laplace
transform. Asking for one instead of a dozen is the single easiest speed-up
available to you.
:::

### The plot tool

::: only 7,8
Very often we are asked to plot functions of time. The calculator has extensive
plotting capabilities, but just to save you some time, Symbulator includes a
handy **s\plot** tool that allows you to plot functions of time.

```sym 7
s\plot()
```
```sym 8
s\plot()
```
:::
::: only 9
Symbulator 9 draws the plot for you, in the **Plot** card below the results.
Solve the circuit first — the plot is of an answer, so there has to be one —
then open **Plot** and fill in four things:

- **Plot type**: *Plot a function of time*
- **Variable to plot**: the answer you want, such as `v2`
- **Start time (s)** and **End time (s)**: the window, for example 0 and
  0.005
- **Points**: how finely to sample it; 300 is the default and is usually
  plenty

Press **Run** and the curve appears under the card.

The second field is worth a moment. It takes an answer's name, not an
expression, and it must be one this circuit actually has — `v2` and `ir1`
rather than `vc` or a formula of your own. If you are unsure of the spelling,
**Results** lists every name above.

::: warning A curve the inverse Laplace could not find
Some circuits have an answer the inverse Laplace transform cannot close into
an expression. Symbulator samples the s-domain answer numerically for the
plot instead, so the picture still appears even when **Results** shows
nothing for that variable. If a plot is blank where you expected a curve,
check that the variable is spelled the way **Results** spells it.
:::
:::

## Instructive solved examples {#practice-transient}

::: practice


### Transient analysis of RC circuit

::: problem Bo2's Example 5.1

::: figure assets/practice/bo2s-example-5-1-1.jpg

:::

::: figure assets/practice/bo2s-example-5-1-2.jpg

:::

**Solution.** Here we have two intervals. For the first interval, when **t <
0s**, we assume that things have been steady for a long time now and any
transient effect has long passed. So for this first interval of t < 0s, we do
a DC simulation to find the initial conditions for the second interval.

```sym 7
s\dc("e,1,0,V:r1,1,2,r1:c,2,0,c:r,2,0,r")
```
```sym 8
s\dc("e,1,0,V:r1,1,2,r1:c,2,0,c:r,2,0,r")
```
```field 9 Circuit Description
e,1,0,V
r1,1,2,r1
c,2,0,c
r,2,0,r
```

When the simulation is *Done*, we ask for `vc`, the voltage in the capacitor
**c**. We get the expression shown below, which is correct.

For the second interval, when **0s ≤ t**, we do a transient simulation. We
give the capacitor as initial condition its voltage from the previous
interval.

```sym 7
s\tr("c,2,0,c,r*v/(r+r1):r,2,0,r")
```
```sym 8
s\tr("c,2,0,c,r*v/(r+r1):r,2,0,r")
```
```field 9 Circuit Description
c,2,0,c,r*v/(r+r1)
r,2,0,r
```

When the simulation is *Done*, we ask for `vc` again. We get the expression
below, which is correct.

e{{sup:-t/cr}} (r v)/(r+r1)

:::

::: problem Bo2's Drill Exercise 5.1

::: figure assets/practice/bo2s-drill-exercise-5-1-3.jpg

:::

**Solution.** Again, we have two intervals: the first for DC, the second for
TR.

For the first interval, when **t < 0s**, the current source is 2A. Simulate
in DC.

```sym 7
s\dc("j,0,1,2:r,1,0,3:c,1,0,1/12"):{vc,ic}
```
```sym 8
s\dc("j,0,1,2:r,1,0,3:c,1,0,1/12"):{vc,ic}
```
```field 9 Circuit Description
j,0,1,2
r,1,0,3
c,1,0,1/12
```

::: only 9
The answers you want are `vc` and `ic`, in **Results**.
:::

{ 6 , 0 }

So the voltage in the capacitor is 6V. We store this value in a variable
called **vc**{{sub:0}}, to use it as initial condition of the capacitor for
the second interval.

```sym 7
vcvc0
```
```sym 8
vcvc0
```

For the second interval, when **0s ≤ t**, we do a transient simulation. The
current source is 0A, and the capacitor has an initial condition: voltage
**vc**{{sub:0}}.

```sym 7
s\tr("j,0,1,0:r,1,0,3:c,1,0,1/12,vc0"):{vc,ic}
```
```sym 8
s\tr("j,0,1,0:r,1,0,3:c,1,0,1/12,vc0"):{vc,ic}
```
```field 9 Circuit Description
j,0,1,0
r,1,0,3
c,1,0,1/12,vc0
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `vc` and `ic`, in **Results**.
:::

When the simulation is *Done*, we get the expressions below. They are right.

{ 6e{{sup:-4t}} , -2e{{sup:-4t}} }

:::

::: problem Bo2's p224 5.2

::: figure assets/practice/bo2s-p224-5-2-4.jpg

:::

**Solution.** Again, we have two intervals: the first for DC, the second for
TR.

For the interval when **t < 0s**, the voltage source is 12A. Simulate in DC.

```sym 7
s\dc("e,1,0,12:r3,1,2,3:r6,2,0,6:r4,2,3,4:c,3,0,1/12"):{vc,ic,v2}
```
```sym 8
s\dc("e,1,0,12:r3,1,2,3:r6,2,0,6:r4,2,3,4:c,3,0,1/12"):{vc,ic,v2}
```
```field 9 Circuit Description
e,1,0,12
r3,1,2,3
r6,2,0,6
r4,2,3,4
c,3,0,1/12
```

::: only 9
The answers you want are `vc`, `ic` and `v2`, in **Results**.
:::

{ 8 , 0 , 8 }

For the interval when **0s ≤ t**, the voltage source is 0V. Simulate in TR,
giving the capacitor as initial condition its voltage from the previous
interval.

```sym 7
s\tr("e,1,0,0:r3,1,2,3:r6,2,0,6:r4,2,3,4:c,3,0,1/12,8"):{vc,ic,v2}
```
```sym 8
s\tr("e,1,0,0:r3,1,2,3:r6,2,0,6:r4,2,3,4:c,3,0,1/12,8"):{vc,ic,v2}
```
```field 9 Circuit Description
e,1,0,0
r3,1,2,3
r6,2,0,6
r4,2,3,4
c,3,0,1/12,8
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `vc`, `ic` and `v2`, in **Results**.
:::

{ 8e{{sup:-2t}} , (-4/3)e{{sup:-2t}} , (8/3)e{{sup:-2t}} }

:::

::: problem Bo2's Drill Exercise 5.2

::: figure assets/practice/bo2s-drill-exercise-5-2-5.jpg

:::

::: figure assets/practice/bo2s-drill-exercise-5-2-6.jpg

:::

**Solution.** For **t < 0s**, the 6A source is part of the circuit. Simulate
in DC.

```sym 7
s\dc("j,0,1,6:r10,1,0,3:r12,1,2,3:r20,2,0,3:c,2,0,1/10"):{vc,ic,v1}
```
```sym 8
s\dc("j,0,1,6:r10,1,0,3:r12,1,2,3:r20,2,0,3:c,2,0,1/10"):{vc,ic,v1}
```
```field 9 Circuit Description
j,0,1,6
r10,1,0,3
r12,1,2,3
r20,2,0,3
c,2,0,1/10
```

::: only 9
The answers you want are `vc`, `ic` and `v1`, in **Results**.
:::

{ 6 , 0 , 12 }

For **0s ≤ t**, the source is no longer relevant and can be excluded from the
circuit. Simulate in TR, giving the capacitor its proper initial condition.

```sym 7
s\tr("r10,1,0,3:r12,1,2,3:r20,2,0,3:c,2,0,1/10,6"):{vc,ic,v1}
```
```sym 8
s\tr("r10,1,0,3:r12,1,2,3:r20,2,0,3:c,2,0,1/10,6"):{vc,ic,v1}
```
```field 9 Circuit Description
r10,1,0,3
r12,1,2,3
r20,2,0,3
c,2,0,1/10,6
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `vc`, `ic` and `v1`, in **Results**.
:::

{ 6e{{sup:-5t}} , -3e{{sup:-5t}} , 3e{{sup:-5t}} }

:::

::: problem Bo2's Figure 5.10a

Look at the simple resistor-inductor (RL) circuit shown below, where at time
t=0 the inductor current is i{{sub:L}}(0). Determine v{{sub:L}}(t),
i{{sub:L}}(t) and v{{sub:R}}(t) for t≥0.

::: figure assets/practice/bo2s-figure-5-10a-7.jpg

:::

Since we are already given the initial condition, we only run the transient
simulation for t≥0. In our circuit description below, the initial condition
is **il0**.

```sym 7
s\tr("l,1,0,l,il0:r,1,0,r"):{vl,il,vr}
```
```sym 8
s\tr("l,1,0,l,il0:r,1,0,r"):{vl,il,vr}
```
```field 9 Circuit Description
l,1,0,l,il0
r,1,0,r
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `vl`, `il` and `vr`, in **Results**.
:::

After 22 seconds, we get the right answers:

{ -il0 r e{{sup:(-r t)/l}} , il0 e{{sup:(-r t)/l}} , -il0 r e{{sup:(-r t)/l}} }

:::

::: problem Bo2's Example 5.3

Determine i{{sub:L}}(t) for all t.

::: figure assets/practice/bo2s-example-5-3-8.jpg

:::

**Solution. **For **t < 0s**, simulate in DC.

```sym 7
s\dc("e,1,0,v:r1,1,2,r1:l,2,0,l:r2,2,0,r"):il
```
```sym 8
s\dc("e,1,0,v:r1,1,2,r1:l,2,0,l:r2,2,0,r"):il
```
```field 9 Circuit Description
e,1,0,v
r1,1,2,r1
l,2,0,l
r2,2,0,r
```

::: only 9
The answer you want is `il`, in **Results**.
:::

For **t ≥ 0s**, simulate in TR, giving the inductor its initial condition.

e{{sup:(-r t)/l}}v/r1

```sym 7
s\tr("l,2,0,l,v/r1:r2,2,0,r"):il
```
```sym 8
s\tr("l,2,0,l,v/r1:r2,2,0,r"):il
```
```field 9 Circuit Description
l,2,0,l,v/r1
r2,2,0,r
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answer you want is `il`, in **Results**.
:::

:::

::: problem Bo2's Drill Exercise 5.3

Find i{{sub:L}}(t), v{{sub:L}}(t) and i(t) for all t.

::: figure assets/practice/bo2s-drill-exercise-5-3-9.jpg

:::

**Solution. **For **t < 0s**, simulate in DC.

```sym 7
s\dc("e,1,0,8:r4,1,2,4:l,2,0,1:r12,2,0,12"):{il,vl,ir1}
```
```sym 8
s\dc("e,1,0,8:r4,1,2,4:l,2,0,1:r12,2,0,12"):{il,vl,ir1}
```
```field 9 Circuit Description
e,1,0,8
r4,1,2,4
l,2,0,1
r12,2,0,12
```

::: only 9
The answers you want are `il`, `vl` and `ir4`, in **Results**.
:::

{ 2 , 0 , 2 }

For **t ≥ 0s**, simulate in TR, giving the inductor its initial condition of
2A.

```sym 7
s\tr("e,1,0,0:r4,1,2,4:l,2,0,1,2:r12,2,0,12"):{il,vl,ir4}
```
```sym 8
s\tr("e,1,0,0:r4,1,2,4:l,2,0,1,2:r12,2,0,12"):{il,vl,ir4}
```
```field 9 Circuit Description
e,1,0,0
r4,1,2,4
l,2,0,1,2
r12,2,0,12
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `il`, `vl` and `ir4`, in **Results**.
:::

{ 2e{{sup:-3t}} , -6 e{{sup:-3t}} , (3/2)e{{sup:-3t}} }

In my machine the simulation took 30 seconds, 12 seconds of these (40%) were
used in finding the inverse Laplace of the answers. Later we will learn a
trick to save time by specifying to Symbulator which answers are required.

:::

::: problem Bo2's p230 (Dependent source)

Find i{{sub:L}}(t) for t≥0, given that i{{sub:L}}(0) = 5A.

::: figure assets/practice/bo2s-p230-dependent-source-10.jpg

:::

We only run the transient simulation for t≥0, with initial condition 5A.

5e{{sup:((-R t)/3L)}}

```sym 7
s\tr("r,v,0,r:j,v,0,2ir:l,v,0,l,5"):il
```
```sym 8
s\tr("r,v,0,r:j,v,0,2ir:l,v,0,l,5"):il
```
```field 9 Circuit Description
r,v,0,r
j,v,0,2*ir
l,v,0,l,5
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answer you want is `il`, in **Results**.
:::

:::

::: problem Bo2's Drill Exercise 5.4 (Dependent source)

Find i{{sub:L}}(t) and v{{sub:L}}(t) for all t.

::: figure assets/practice/bo2s-drill-exercise-5-4-dependent-source-11.jpg

:::

**Solution. **For **t < 0s**, simulate in DC. This gives us the initial
condition.

```sym 7
s\dc("ei,1,0,12:r6,1,2,6:l,2,0,16:r8,2,3,8:ed,3,0,3vr8"):{il,vl}
```
```sym 8
s\dc("ei,1,0,12:r6,1,2,6:l,2,0,16:r8,2,3,8:ed,3,0,3vr8"):{il,vl}
```
```field 9 Circuit Description
ei,1,0,12
r6,1,2,6
l,2,0,16
r8,2,3,8
ed,3,0,3*vr8
```

::: only 9
The answers you want are `il` and `vl`, in **Results**.
:::

{ 2 , 0 }

For **t ≥ 0s**, simulate in TR, giving the inductor its initial condition.

```sym 7
s\tr("l,2,0,16,2:r8,2,3,8:ed,3,0,3vr8"):{il,vl}
```
```sym 8
s\tr("l,2,0,16,2:r8,2,3,8:ed,3,0,3vr8"):{il,vl}
```
```field 9 Circuit Description
l,2,0,16,2
r8,2,3,8
ed,3,0,3*vr8
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `il` and `vl`, in **Results**.
:::

{ 2 e{{sup:-2t}} , -64 e{{sup:-2t}} }

:::

::: problem Bo2's Example 5.5 (Op Amp)

Determine v{{sub:C}}(t), i{{sub:C}}(t) and v{{sub:o}}(t) for all t.

::: figure assets/practice/bo2s-example-5-5-op-amp-12.jpg

:::

**Solution. **For **t < 0s**, simulate in DC. This gives us the initial
condition.

```sym 7
s\dc("e,3,0,4:r2,3,1,2:r5,1,o,5:c,1,o,1/20:o,0,1,o"):{vc,ic,vo}
```
```sym 8
s\dc("e,3,0,4:r2,3,1,2:r5,1,o,5:c,1,o,1/20:o,0,1,o"):{vc,ic,vo}
```
```field 9 Circuit Description
e,3,0,4
r2,3,1,2
r5,1,o,5
c,1,o,1/20
o,0,1,o
```

::: only 9
The answers you want are `vc`, `ic` and `vo`, in **Results**.
:::

{ 10 , 0 , -10 }

For **t ≥ 0s**, simulate in TR, giving the capacitor its initial condition.

```sym 7
s\tr("r2,0,1,2:r5,1,o,5:c,1,o,1/20,10:o,0,1,o"):{vc,ic,vo}
```
```sym 8
s\tr("r2,0,1,2:r5,1,o,5:c,1,o,1/20,10:o,0,1,o"):{vc,ic,vo}
```
```field 9 Circuit Description
r2,0,1,2
r5,1,o,5
c,1,o,1/20,10
o,0,1,o
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `vc`, `ic` and `vo`, in **Results**.
:::

{ 10 e{{sup:-4t}} , -2 e{{sup:-4t}} , -10 e{{sup:-4t}} }

:::

::: problem Bo2's Drill Exercise 5.5 (Op Amp)

Determine v{{sub:C}}(t), i{{sub:C}}(t) and v{{sub:o}}(t) for all t.

::: figure assets/practice/bo2s-drill-exercise-5-5-op-amp-13.jpg

:::

**Solution. **For **t < 0s**, simulate in DC. This gives us the initial
condition.

```sym 7
s\dc("e,2,0,4:o,2,1,o:c,o,1,1/20:r5,o,1,5:r2,1,0,2"):{vc,ic,vo}
```
```sym 8
s\dc("e,2,0,4:o,2,1,o:c,o,1,1/20:r5,o,1,5:r2,1,0,2"):{vc,ic,vo}
```
```field 9 Circuit Description
e,2,0,4
o,2,1,o
c,o,1,1/20
r5,o,1,5
r2,1,0,2
```

::: only 9
The answers you want are `vc`, `ic` and `vo`, in **Results**.
:::

{ 10 , 0 , 14 }

For **t ≥ 0s**, simulate in TR, giving the capacitor its initial condition.

```sym 7
s\tr("o,0,1,o:c,o,1,1/20,10:r5,o,1,5:r2,1,0,2"):{vc,ic,vo}
```
```sym 8
s\tr("o,0,1,o:c,o,1,1/20,10:r5,o,1,5:r2,1,0,2"):{vc,ic,vo}
```
```field 9 Circuit Description
o,0,1,o
c,o,1,1/20,10
r5,o,1,5
r2,1,0,2
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `vc`, `ic` and `vo`, in **Results**.
:::

{ 10 e{{sup:-4t}} , -2 e{{sup:-4t}} , 10 e{{sup:-4t}} }

:::

::: problem Bo2's Example 5.6

In the circuit shown below, there are two switches: one that opens at time
t=0 and one that closes at time t=1 second. Determine v{{sub:C}}(t) and
i{{sub:C}}(t) for all t.

::: figure assets/practice/bo2s-example-5-6-14.jpg

:::

As we mentioned before, every time a switch moves marks the end of one
interval and the beginning of another interval for Symbulator.

For the first interval, which corresponds to t<0, we simulate in DC.

```sym 7
s\dc("e,2,0,10:r1,2,1,1:c,1,0,1/4:r4,1,0,4"):{vc,ic}
```
```sym 8
s\dc("e,2,0,10:r1,2,1,1:c,1,0,1/4:r4,1,0,4"):{vc,ic}
```
```field 9 Circuit Description
e,2,0,10
r1,2,1,1
c,1,0,1/4
r4,1,0,4
```

::: only 9
The answers you want are `vc` and `ic`, in **Results**.
:::

{ 8 , 0 }

The voltage in the capacitor at the end of this interval will serve as the
initial condition of the capacitor for the next interval. The second interval
runs between 0 and 1 second, e.g. 0 < t ≤ 1 second. We simulate in TR.

```sym 7
s\tr("c,1,0,1/4,8:r4,1,0,4"):{vc,ic}
```
```sym 8
s\tr("c,1,0,1/4,8:r4,1,0,4"):{vc,ic}
```
```field 9 Circuit Description
c,1,0,1/4,8
r4,1,0,4
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `vc` and `ic`, in **Results**.
:::

{ 8 e{{sup:-t}} , -2 e{{sup:-t}} }

The voltage in the capacitor at the end of this second interval will serve as
initial condition for the third interval. We can use its exact value, e.g.
{{v7|`8*e^-1`}}{{v8|`8*e^–1`}}, but the textbook prefers using its approximate value, e.g. `2.943`.

The third interval corresponds to t > 1 second. We simulate in TR. To make
things easier for Symbulator, we replace the resistors by their equivalent.

```sym 7
s\tr("c,1,0,1/4,2.943:re,1,0,[4,6]")
```
```sym 8
s\tr("c,1,0,1/4,2.943:re,1,0,[4,6]")
```
```field 9 Circuit Description
c,1,0,1/4,2.943
re,1,0,[4,6]
```

Ask for `{vc,ic}`. The expressions we get are equivalent to:

{ 2.943 e{{sup:(-5(t-1))/3}} , -1.226 e{{sup:(-5(t-1))/3}} }

These are the right answers, as can be seen by checking the book's answers.

::: figure assets/practice/bo2s-example-5-6-15.jpg

:::

::: figure assets/practice/bo2s-example-5-6-16.jpg

:::

:::

::: problem Bo2's Drill Exercise 5.6

Let’s see another example where a TR simulation is done for an interval that
starts at a time other than t=0. Determine i{{sub:L}}(t) and v{{sub:L}}(t)
for all t.

::: figure assets/practice/bo2s-drill-exercise-5-6-17.jpg

:::

For the first interval, which corresponds to t<0, we simulate in DC.

```sym 7
s\dc("e,1,0,9:r9,1,0,9:r3,1,2,3:l,2,0,6"):{il,vl}
```
```sym 8
s\dc("e,1,0,9:r9,1,0,9:r3,1,2,3:l,2,0,6"):{il,vl}
```
```field 9 Circuit Description
e,1,0,9
r9,1,0,9
r3,1,2,3
l,2,0,6
```

::: only 9
The answers you want are `il` and `vl`, in **Results**.
:::

{ 3 , 0 }

The 3A current in the inductor is its initial condition for the second
interval, which goes from 0 to 2 second, e.g. 0 < t ≤ 2 seconds. We simulate
in TR.

```sym 7
s\tr("r,1,0,9+3:l,1,0,6,3"):{il,vl}
```
```sym 8
s\tr("r,1,0,9+3:l,1,0,6,3"):{il,vl}
```
```field 9 Circuit Description
r,1,0,9+3
l,1,0,6,3
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `il` and `vl`, in **Results**.
:::

{ 3 e{{sup:-2t}} , -36 e{{sup:-2t}} }

The current in the capacitor at the end of this second interval will serve as
initial condition for the third interval. Find its approximate value thus:

```sym 7
iL|t=2.
```
```sym 8
iL|t=2.
```

.055

The third interval corresponds to t > 2 second. We simulate in TR. To make
things easier for Symbulator, we replace the resistors by their equivalent.

{ .055 e{{sup:(-(t-2)/2)}} , -.165 e{{sup:(-(t-2)/2)}} }

```sym 7
s\tr("r,1,0,[9+3,4]:l,1,0,6,.055"):{il,vl}
```
```sym 8
s\tr("r,1,0,[9+3,4]:l,1,0,6,.055"):{il,vl}
```
```field 9 Circuit Description
r,1,0,[9+3,4]
l,1,0,6,.055
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `il` and `vl`, in **Results**.
:::

These are the kind of expressions your book or professor are looking for.

:::

::: problem Bo2's Figure 5.19

In the following circuit, assume that all the initial conditions are zero.
The source is a step function **u(t)** with value **V** volts. Find
i{{sub:R}}, v{{sub:R}}, i{{sub:C}} and v{{sub:C}}.

::: figure assets/practice/bo2s-figure-5-19-18.jpg

:::

As discussed before, a step source with symbolic value requires that we use
the `u(t)` nomenclature to describe it. Since the value is V volts, we
describe the source as `V*u(t).`

```sym 7
s\tr("e,1,0,V*u(t):r,1,2,r:c,2,0,c,0"):{vc,vr,ic}
```
```sym 8
s\tr("e,1,0,V*u(t):r,1,2,r:c,2,0,c,0"):{vc,vr,ic}
```
```field 9 Circuit Description
e,1,0,V*Heaviside(t)
r,1,2,r
c,2,0,c,0
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `vc`, `vr` and `ic`, in **Results**.
:::

There is no need to ask for i{{sub:R}}, since i{{sub:R}}=i{{sub:C}}. We get
the following expressions:

{ v-v e{{sup:(-t/(c r))}} , v e{{sup:(-t/(c r))}} , (v/r)e{{sup:(-t/(c r))}} }

:::

::: problem Bo2's Figure 5.24

In the following circuit, assume that all the initial conditions are zero.
The source is a step function **u(t)** with value **V** volts. Find
i{{sub:R}}, v{{sub:R}}, i{{sub:L}} and v{{sub:L}}.

::: figure assets/practice/bo2s-figure-5-24-19.jpg

:::

```sym 7
s\tr("e,1,0,V*u(t):l,1,2,l,0:r,2,0,r"):{vl,vr,il}
```
```sym 8
s\tr("e,1,0,V*u(t):l,1,2,l,0:r,2,0,r"):{vl,vr,il}
```
```field 9 Circuit Description
e,1,0,V*Heaviside(t)
l,1,2,l,0
r,2,0,r
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `vl`, `vr` and `il`, in **Results**.
:::

There is no need to ask for i{{sub:R}}, since in a series circuit it will be
identical to i{{sub:L}}.

{ v e{{sup:(-r t)/l}} , v (1-e{{sup:(-r t)/l}}) , (v/r)(1-e{{sup:(-r t)/l}}) }

:::

::: problem Bo2's Drill Exercise 5.7

For the circuit below, with a step source of 12 volts, find i{{sub:L}},
v{{sub:L}}, i{{sub:L}} and v.

::: figure assets/practice/bo2s-drill-exercise-5-7-20.jpg

:::

As discussed before, a step source with numerical value can be described
without the `u(t)` nomenclature. Thus, we describe the source as `12`.

```sym 7
s\tr("e,1,0,12:r4,1,2,4:l,2,3,2,0:r2,3,0,2"):{il,vl,v2}
```
```sym 8
s\tr("e,1,0,12:r4,1,2,4:l,2,3,2,0:r2,3,0,2"):{il,vl,v2}
```
```field 9 Circuit Description
e,1,0,12
r4,1,2,4
l,2,3,2,0
r2,3,0,2
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `il`, `vl` and `v2`, in **Results**.
:::

{ 2-2e{{sup:-3t}} , 12 e{{sup:-3t}} , 8 e{{sup:-3t}}+4 }

:::

::: problem Bo2's Figure 5.26

In the following circuit, assume that all the initial conditions are zero.
The source is a step function **u(t)** with value **I** amperes. Find
i{{sub:C}}, i{{sub:R}}, and v.

::: figure assets/practice/bo2s-figure-5-26-21.jpg

:::

As discussed before, a step source with symbolic value requires that we use
the `u(t)` nomenclature to describe it. Since the value is I amperes, we
describe the source as `I*u(t)`. Thus:

```sym 7
s\tr("j,0,1,i*u(t):c,1,0,c,0:r,1,0,r"):{v1,ir,ic}
```
```sym 8
s\tr("j,0,1,i*u(t):c,1,0,c,0:r,1,0,r"):{v1,ir,ic}
```
```field 9 Circuit Description
j,0,1,i*Heaviside(t)
c,1,0,c,0
r,1,0,r
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `v1`, `ir` and `ic`, in **Results**.
:::

{ (i-i e{{sup:-t/(c r)}})*r , i-i e{{sup:-t/(c r)}} , i e{{sup:-t/(c r)}} }

:::

::: problem Bo2's Example 5.7 (Op Amp)

Suppose that *v*{{sub:s}}*(t)=u(t)*. Find v{{sub:C}}, i{{sub:C}}, and
v{{sub:o}}.

::: figure assets/practice/bo2s-example-5-7-op-amp-22.jpg

:::

This source is a step source with a value of 1 volt. Since its value is
numerical, the `u(t)` nomenclature is not needed. We describe the source
plainly as `1`.

```sym 7
s\tr("e,1,0,1:o,1,2,o:c,2,o,1/8,0:r2,2,o,2:r1,2,0,1"):{vc,ic,vo}
```
```sym 8
s\tr("e,1,0,1:o,1,2,o:c,2,o,1/8,0:r2,2,o,2:r1,2,0,1"):{vc,ic,vo}
```
```field 9 Circuit Description
e,1,0,1
o,1,2,o
c,2,o,1/8,0
r2,2,o,2
r1,2,0,1
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `vc`, `ic` and `vo`, in **Results**.
:::

{ 2 e{{sup:-4t}}-2 , -e{{sup:-4t}} , 3-2e{{sup:-4t}} }

:::

::: problem Bo2's Drill Exercise 5.8 (Op Amp)

Suppose that *v*{{sub:s}}*(t)=u(t)*. Find v{{sub:C}}, i{{sub:C}}, and
v{{sub:o}}.

::: figure assets/practice/bo2s-drill-exercise-5-8-op-amp-23.jpg

:::

Again, following the same logic as above, we describe the source plainly as
`1`.

```sym 7
s\tr("e,1,0,1:r1,1,2,1:r2,2,o,2:c,2,o,1/8,0:o,0,2,o"):{vc,ic,vo}
```
```sym 8
s\tr("e,1,0,1:r1,1,2,1:r2,2,o,2:c,2,o,1/8,0:o,0,2,o"):{vc,ic,vo}
```
```field 9 Circuit Description
e,1,0,1
r1,1,2,1
r2,2,o,2
c,2,o,1/8,0
o,0,2,o
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `vc`, `ic` and `vo`, in **Results**.
:::

{ 2-2 e{{sup:-4t}} , e{{sup:-4t}} , 2 e{{sup:-4t}}-2 }

:::

::: problem Bo2's p249 F5.28

For the circuit left, the source is *v*{{sub:s}}*(t)* *= V u(t) - V
u(t-t*{{sub:0}}*)*. This is shown in the plot to the right. Given this, find
the voltage drop in the capacitor for all *t*.

::: figure assets/practice/bo2s-p249-f5-28-24.jpg

:::

Because the source has two steps, this problem has to be analyzed in two
intervals. For the first interval, the initial conditions are zero and the
source value is V\*u(t). Our circuit description for the first interval is
given below.

```sym 7
s\tr("e,1,0,V*u(t):r,1,2,r:c,2,0,c,0"):vc
```
```sym 8
s\tr("e,1,0,V*u(t):r,1,2,r:c,2,0,c,0"):vc
```
```field 9 Circuit Description
e,1,0,V*Heaviside(t)
r,1,2,r
c,2,0,c,0
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answer you want is `vc`, in **Results**.
:::

The expression for the capacitor's voltage drop in the first interval is:

v-v e{{sup:(-t/(c r))}}

The second interval starts at t{{sub:0}}. In it, the initial condition of the
capacitor is given by the value of the expression above when t=t{{sub:0}}.
Here is how we find it:

```sym 7
vc|t=to
```
```sym 8
vc|t=to
```

::: only 9
Put `vc` in the **Evaluate** card and write `t = to` in its **Conditions**
box. That is what the calculator's `|` does: evaluate this expression under
this condition. The answer comes back {{o:V - V*exp(-to/(c*r))}}.
:::

The circuit description for the second interval uses the expression above as
the initial condition of the capacitor. In this second interval, the source
has a value of 0 volts, which is another way to say that it becomes a short,
so there is no need to include it in the circuit description.

(v-v e{{sup:(-to/(c r))}})e{{sup:((-t+to)/(c r))}}

```sym 7
s\tr("r,0,2,r:c,2,0,c,v-e^(-to/(c*r))*v"):vc
```
```sym 8
s\tr("r,0,2,r:c,2,0,c,v-e^(–to/(c*r))*v"):vc
```
```field 9 Circuit Description
r,0,2,r
c,2,0,c,v-e^(-to/(c*r))*v
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answer you want is `vc`, in **Results**.
:::

This is the expression for the capacitor's voltage drop in the second
interval.

:::

::: problem Bo2's Drill Exercise 5.9

Find the current through the inductor if the source is v{{sub:s}}(t) = V u(t)
– V u(t-t{{sub:o}}).

::: figure assets/practice/bo2s-drill-exercise-5-9-25.jpg

:::

Because the source has two steps, this problem has to be analyzed in two
intervals. For the first interval, the initial conditions are zero and the
source value is V\*u(t). Our circuit description for the first interval is
given below.

```sym 7
s\tr("e,1,0,V*u(t):l,1,2,l,0:r,2,0,r"):il
```
```sym 8
s\tr("e,1,0,V*u(t):l,1,2,l,0:r,2,0,r"):il
```
```field 9 Circuit Description
e,1,0,V*Heaviside(t)
l,1,2,l,0
r,2,0,r
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answer you want is `il`, in **Results**.
:::

The expression for the inductor's current in the first interval is:

(v/r)(1-e{{sup:((-r t)/l)}})

The second interval starts at t{{sub:0}}. In it, the initial condition of the
inductor is given by the value of the expression above when t=t{{sub:0}}.
Here is how we find it:

```sym 7
il|t=to
```
```sym 8
il|t=to
```

::: only 9
Put `il` in the **Evaluate** card and write `t = to` in its **Conditions**
box. The answer comes back {{o:V/r - V*exp(-r*to/l)/r}}, which is the same
expression gathered differently.
:::

The circuit description for the second interval uses the expression above as
the initial condition of the inductor. In this second interval, the source
becomes a short, so there is no need to include it in the circuit
description.

(v/r)(1-e{{sup:((-to r)/l)}})e{{sup:((-r t)/l)}}

```sym 7
s\tr("l,0,2,l,v/r-e^(-to*r/l)*v/r:r,2,0,r"):il
```
```sym 8
s\tr("l,0,2,l,v/r-e^(–to*r/l)*v/r:r,2,0,r"):il
```
```field 9 Circuit Description
l,0,2,l,v/r-e^(-to*r/l)*v/r
r,2,0,r
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answer you want is `il`, in **Results**.
:::

To put this in terms of the same t as the first interval, we replace **t**
with **t-t**{{sub:o}}:

(v/r)(1-e{{sup:((-to r)/l)}})e{{sup:((-r (t-to))/l)}}

This is the expression for the inductor's current in the second interval.

:::

::: problem Bo2's Figure 5.36

For the circuit shown in (a), find the voltage drop in the capacitor, given
that the voltage source is as shown in (b).

::: figure assets/practice/bo2s-figure-5-36-26.jpg

:::

This problem requires two intervals. In the first interval, a DC analysis of
the circuit with a source of 2 V gives us the voltage in the capacitor.

```sym 7
s\dc("e,1,0,2:r3,1,2,3:r5,2,3,5:c,3,0,1:j,0,2,2ir3"):vc
```
```sym 8
s\dc("e,1,0,2:r3,1,2,3:r5,2,3,5:c,3,0,1:j,0,2,2ir3"):vc
```
```field 9 Circuit Description
e,1,0,2
r3,1,2,3
r5,2,3,5
c,3,0,1
j,0,2,2*ir3
```

::: only 9
The answer you want is `vc`, in **Results**.
:::

2

This is the initial condition for the capacitor in the second interval, which
we analyze using TR and a source value of -4 V.

6e{{sup:( -t/6)}}-4

```sym 7
s\tr("e,1,0,-4:r3,1,2,3:r5,2,3,5:c,3,0,1,2:j,0,2,2ir3"):vc
```
```sym 8
s\tr("e,1,0,–4:r3,1,2,3:r5,2,3,5:c,3,0,1,2:j,0,2,2ir3"):vc
```
```field 9 Circuit Description
e,1,0,-4
r3,1,2,3
r5,2,3,5
c,3,0,1,2
j,0,2,2*ir3
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answer you want is `vc`, in **Results**.
:::

This is the expression for the voltage drop in the capacitor after t=0.

:::

### The only tool

::: problem Bo2's Drill Exercise 5.11

For the circuit of Bo2's Example 5.7, change the value of the capacitor to ¼
F. Find v{{sub:C}}(t) for the case that the source is v{{sub:S}}(t)=1 V for
t<0 and 3V for t≥0.

We let Symbulator know that we are only interested in one variable: vc.

```sym 7
s\only("vc")
```
```sym 8
s\only("vc")
```

::: only 9
This is optional: Symbulator 9 solves quickly enough that limiting the results rarely saves you anything worth having. If you want to anyway, tick **Do you want to limit the results to save time?** in **Settings** and list `vc` in the box beside it.
:::

Then we run the simulation for the first interval, just as we did before, but
with the new capacitor and source values.

```sym 7
s\dc("e,1,0,1:o,1,2,o:c,2,o,1/4:r2,2,o,2:r1,2,0,1"):vc
```
```sym 8
s\dc("e,1,0,1:o,1,2,o:c,2,o,1/4:r2,2,o,2:r1,2,0,1"):vc
```
```field 9 Circuit Description
e,1,0,1
o,1,2,o
c,2,o,1/4
r2,2,o,2
r1,2,0,1
```

::: only 9
The answer you want is `vc`, in **Results**.
:::

-2

This is the initial condition for the next interval. Before we run the
simulation for the second interval, we let Symbulator know, again, that we
are only interested in one variable: vc.

```sym 7
s\only("vc")
```
```sym 8
s\only("vc")
```

::: only 9
This is optional: Symbulator 9 solves quickly enough that limiting the results rarely saves you anything worth having. If you want to anyway, tick **Do you want to limit the results to save time?** in **Settings** and list `vc` in the box beside it.
:::

Then we run the simulation for the second interval, just as we did before,
but with the new capacitor and source values.

4e{{sup:(-2t)}}-6

```sym 7
s\tr("e,1,0,3:o,1,2,o:c,2,o,1/4,-2:r2,2,o,2:r1,2,0,1"):vc
```
```sym 8
s\tr("e,1,0,3:o,1,2,o:c,2,o,1/4,–2:r2,2,o,2:r1,2,0,1"):vc
```
```field 9 Circuit Description
e,1,0,3
o,1,2,o
c,2,o,1/4,-2
r2,2,o,2
r1,2,0,1
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answer you want is `vc`, in **Results**.
:::

:::

::: problem Bo2's Figure 5.38 (Impulse)

Find the voltage drop and current in the capacitor, given a source of I δ(t)
A, where δ(t) is the impulse function and I is a constant.

::: figure assets/practice/bo2s-figure-5-38-impulse-27.jpg

:::

As we mentioned before, impulse sources must be described using the δ(t)
nomenclature. To save some typing time, you find it in the menu.

```sym 7
s\tr("j,0,1,i*δ(t):c,1,0,c,0:r,1,0,r")
```
```sym 8
s\tr("j,0,1,i*δ(t):c,1,0,c,0:r,1,0,r")
```
```field 9 Circuit Description
j,0,1,i*DiracDelta(t)
c,1,0,c,0
r,1,0,r
```

Once the simulation completes, we ask for the variables of interest:

(i/c)e{{sup:(-t/(c r))}}

(-i/(c r))e{{sup:(-t/(c r))}}

::: only 9
They are already in **Results**: `vc` is {{o:i*exp(-t/(c*r))/c}} and `ic`
is {{o:i*DiracDelta(t) - i*exp(-t/(c*r))/(c*r)}}.

The impulse survives in the capacitor's current, which is right — the
charge arrives all at once, and the delta is that instant.
:::

```sym 7
vc
```
```sym 8
vc
```

```sym 7
ic
```
```sym 8
ic
```

:::

::: problem Bo2's Drill Exercise 5.13 (Impulse)

For the circuit of Bo2's Example 5.7, find v{{sub:C}}(t), i{{sub:C}}(t) and
v{{sub:o}}(t) due to an impulse voltage source of v{{sub:S}}(t)= δ(t) (that
is to say, a 1V impulse in t=0.)

Nothing new here. Again we use the δ(t) nomenclature for the source.

```sym 7
s\tr("e,1,0,δ(t):o,1,2,o:c,2,o,1/8,0:r2,2,o,2:r1,2,0,1"):{vc,ic,vo}
```
```sym 8
s\tr("e,1,0,δ(t):o,1,2,o:c,2,o,1/8,0:r2,2,o,2:r1,2,0,1"):{vc,ic,vo}
```
```field 9 Circuit Description
e,1,0,DiracDelta(t)
o,1,2,o
c,2,o,1/8,0
r2,2,o,2
r1,2,0,1
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `vc`, `ic` and `vo`, in **Results**.
:::

{ -8 e{{sup:-4t}} , 4 e{{sup:-4t}} , 8 e{{sup:-4t}} }

:::

::: problem Bo2's Figure 5.39 (Ramp)

Find iL(t) and vL(t) for a circuit that has in parallel a resistor R, an
inductor L and a current source with a ramp value I r(t). Initial conditions
are zero.

A ramp value I r(t) means a value of I t. We describe this source simply as
`i*t`.

```sym 7
s\tr("j,0,1,i*t:r,1,0,r:l,1,0,l,0"):{il,vl}
```
```sym 8
s\tr("j,0,1,i*t:r,1,0,r:l,1,0,l,0"):{il,vl}
```
```field 9 Circuit Description
j,0,1,i*t
r,1,0,r
l,1,0,l,0
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `il` and `vl`, in **Results**.
:::

{ ((i l)/r)(e{{sup:((-r t)/l)}}-1)+i t , i l(1-e{{sup:((-r t)/l)}}) }

:::

::: problem Bo2's Drill Exercise 5.14 (Ramp)

For the circuit of Bo2's Example 5.7, find v{{sub:C}}(t) and i{{sub:C}}(t)
due to a ramp input voltage of v{{sub:S}}(t)= r(t).

Nothing new here. The command below should be clear to you by now.

```sym 7
s\tr("e,1,0,t:o,1,2,o:c,2,o,1/8,0:r2,2,o,2:r1,2,0,1"):{vc,ic}
```
```sym 8
s\tr("e,1,0,t:o,1,2,o:c,2,o,1/8,0:r2,2,o,2:r1,2,0,1"):{vc,ic}
```
```field 9 Circuit Description
e,1,0,t
o,1,2,o
c,2,o,1/8,0
r2,2,o,2
r1,2,0,1
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `vc` and `ic`, in **Results**.
:::

{ (1/2)(1-e{{sup:-4t}})-2t , (1/4)(e{{sup:-4t}}-1) }

:::

::: problem Bo2's Example 5.12 (Exponential)

Assume initial conditions zero. Find i{{sub:L}}(t) and v{{sub:L}}(t), given
that i{{sub:S}}(t) = 2 *e* {{sup:-4t}} A.

::: figure assets/practice/bo2s-example-5-12-exponential-28.jpg

:::

Describe the source as given to you by the problem, using an exponential.

```sym 7
s\tr("j,0,1,2e^(-4t):r,0,1,6:l,1,0,2,0"):{il,vl}
```
```sym 8
s\tr("j,0,1,2e^(–4t):r,0,1,6:l,1,0,2,0"):{il,vl}
```
```field 9 Circuit Description
j,0,1,2*exp(-4*t)
r,0,1,6
l,1,0,2,0
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `il` and `vl`, in **Results**.
:::

{ 6 e{{sup:-3t}}-6 e{{sup:-4t}} , 48 e{{sup:-4t}}-36 e{{sup:-3t}} }

:::

::: problem Bo2's p265 (Exponential)

Repeat Bo2's Example 5.12 if the current source is now i{{sub:S}}(t) = 2 *e*
{{sup:-3t}} A.

All we do is change one digit in the circuit description: replace `4` with
`3`.

```sym 7
s\tr("j,0,1,2e^(-3t):r,0,1,6:l,1,0,2,0"):{il,vl}
```
```sym 8
s\tr("j,0,1,2e^(–3t):r,0,1,6:l,1,0,2,0"):{il,vl}
```
```field 9 Circuit Description
j,0,1,2*exp(-3*t)
r,0,1,6
l,1,0,2,0
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `il` and `vl`, in **Results**.
:::

{ 6 t e{{sup:-3t}} , (12-36 t) e{{sup:-3t}} }

:::

::: problem Bo2's Example 5.13 (Exponential)

Find the voltage drop in the capacitor and the current in the 3 Ω resistor,
if the source value is v{{sub:S}}(t)=18*e*{{sup:-t/2}}.

::: figure assets/practice/bo2s-example-5-13-exponential-29.jpg

:::

```sym 7
s\tr("e,1,0,18e^(-t/2):r3,1,2,3:r5,2,3,5:c,3,0,1,0:j,0,2,2ir3"):{vc,ir3}
```
```sym 8
s\tr("e,1,0,18e^(–t/2):r3,1,2,3:r5,2,3,5:c,3,0,1,0:j,0,2,2ir3"):{vc,ir3}
```
```field 9 Circuit Description
e,1,0,18*exp(-t/2)
r3,1,2,3
r5,2,3,5
c,3,0,1,0
j,0,2,2*ir3
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `vc` and `ir3`, in **Results**.
:::

{ 9 e{{sup:(-t/6)}}-9 e{{sup:(-t/2)}} , (3/2) e{{sup:(-t/2)}}-(1/2)e{{sup:(-t/6)}} }

:::

::: problem Bo2's Drill Exercise 5.16 (Exponential)

For the circuit of Bo2's Example 5.7, find v{{sub:C}}(t) and i{{sub:C}}(t)
for the case when the source's value is v{{sub:S}}(t)= 2 *e* {{sup:-4t}}. As
before, assume initial conditions are zero.

```sym 7
s\tr("e,1,0,2e^(-4t):o,1,2,o:c,2,o,1/8,0:r2,2,o,2:r1,2,0,1"):{vc,ic}
```
```sym 8
s\tr("e,1,0,2e^(–4t):o,1,2,o:c,2,o,1/8,0:r2,2,o,2:r1,2,0,1"):{vc,ic}
```
```field 9 Circuit Description
e,1,0,2*exp(-4*t)
o,1,2,o
c,2,o,1/8,0
r2,2,o,2
r1,2,0,1
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.

The answers you want are `vc` and `ic`, in **Results**.
:::

{ -16 t e{{sup:-4 t}} , (8 t-2) e{{sup:-4t}} }

:::

::: problem Bo2's Example 6.1

Find the current in the inductor i(t) and the voltage drop in the capacitor
v(t).

::: figure assets/practice/bo2s-example-6-1-30.jpg

:::

Since we have switches changing in time t=0, this is a two interval problem.
The first interval is for t<0. We can analyze the first interval using DC.

```sym 7
s\dc("e,3,0,9:r2,3,1,5:r1,1,0,5:l,1,2,1/2:c,2,0,1/8:r3,2,0,2"):{vc,il}
```
```sym 8
s\dc("e,3,0,9:r2,3,1,5:r1,1,0,5:l,1,2,1/2:c,2,0,1/8:r3,2,0,2"):{vc,il}
```
```field 9 Circuit Description
e,3,0,9
r2,3,1,5
r1,1,0,5
l,1,2,1/2
c,2,0,1/8
r3,2,0,2
```

::: only 9
The answers you want are `vc` and `il`, in **Results**.
:::

{2,1}

These are the initial conditions for the second interval. The second is for
t≥0. We can analyze the second interval using TR. We only care about `vc` and
`il`.

```sym 7
s\only("vc,il"):s\tr("r1,1,0,5:l,1,2,1/2,1:c,2,0,1/8,2"):{vc,il}
```
```sym 8
s\only("vc,il"):s\tr("r1,1,0,5:l,1,2,1/2,1:c,2,0,1/8,2"):{vc,il}
```
```field 9 Circuit Description
r1,1,0,5
l,1,2,1/2,1
c,2,0,1/8,2
```

{ 4 e{{sup:-2t}}-2 e{{sup:-8t}} , 2 e{{sup:-8t}}-e{{sup:-2t}} }

Notice that the use of the only tool saves approximately 10 seconds here.

:::

### The plot tool

Imagine, for example, that in Bo2's Example 6.1 we are asked to plot i(t) and
v(t) for times between 0 s and 1.5 s. The first step is to run the `plot`
tool:

```sym 7
s\plot()
```
```sym 8
s\plot()
```

::: only 7,8
A window opens, asking you to enter three things: first, a function of time;
second, a minimal time; and third, a maximal time. Let's plot v{{sub:C}}(t)
first. Unless you have deleted the value of the variable **vc**, you should
have the answer to the simulation above stored in it. So enter `vc` as the
function, `0` as the minimal time and `1.5` as the maximal time. Press Enter,
and wait a little. The graph of the voltage drop in the capacitor between
time 0 and 1.5 seconds should appear in the screen.
:::
::: only 9
Open the **Plot** card, leave **Plot type** on *Plot a function of time*, and
give it `vc` as the variable, `0` as the minimum and `1.5` as the maximum.
The answers from the solve above are already in scope, so the name is all it
needs. The graph of the capacitor's voltage drop between 0 and 1.5 seconds
appears beneath.
:::

Compare it to the graph given by the textbook, shown below. Repeat this
procedure giving `ic` as the function. Compare the resulting graph to that
given by the textbook, shown below.

::: figure assets/practice/practice-problems-for-lesson-6-31.jpg
Practice Problems for Lesson 6
:::

::: problem Bo2's Drill Exercise 6.1

For the circuit shown below, find v(t) and i(t) for t≥0.

::: figure assets/practice/bo2s-drill-exercise-6-1-32.jpg

:::

Nothing new here. This is a two interval problem, as others seen before. The
first interval, for t<0, is analyzed in DC to find the initial conditions.

```sym 7
s\dc("j,0,1,1:r3,1,0,3:r6,1,0,6:l,1,2,1/4:c,2,0,1/3"):{vc,il}
```
```sym 8
s\dc("j,0,1,1:r3,1,0,3:r6,1,0,6:l,1,2,1/4:c,2,0,1/3"):{vc,il}
```
```field 9 Circuit Description
j,0,1,1
r3,1,0,3
r6,1,0,6
l,1,2,1/4
c,2,0,1/3
```

::: only 9
The answers you want are `vc` and `il`, in **Results**.
:::

{2,0}

These conditions are used in the TR analysis of the second interval,
for t≥0.

3e{{sup:-2t}}-e{{sup:-6t}}

2e{{sup:-6t}}-2e{{sup:-2t}}

::: only 9
The answers are `vc` = {{o:3*exp(-2*t) - exp(-6*t)}} and `il` =
{{o:2*exp(-6*t) - 2*exp(-2*t)}}, both in **Results**.
:::

```sym 7
s\only("vc,il"):s\tr("r3,1,0,3:r6,1,0,6:l,1,2,1/4,0:c,2,0,1/3,2")
```
```sym 8
s\only("vc,il"):s\tr("r3,1,0,3:r6,1,0,6:l,1,2,1/4,0:c,2,0,1/3,2")
```
```field 9 Circuit Description
r3,1,0,3
r6,1,0,6
l,1,2,1/4,0
c,2,0,1/3,2
```

```sym 7
vc
```
```sym 8
vc
```

```sym 7
il
```
```sym 8
il
```

Using `only` saves about 13 seconds, or about a third of the calculation
time, because only about 8 seconds are used finding the inverse Laplace of
the selected answers, instead of 21 seconds finding it for all the answers.

:::

::: problem Bo2's Example 6.2

Find i(t) and v(t) for the circuit shown below.

::: figure assets/practice/bo2s-example-6-2-33.jpg

:::

I decided to simulate this using only fractions, not decimals.

::: only 7,8
So I convert the 3.5V value to its exact fractional equivalent, thus:
:::
::: only 9
So write the value as the fraction it is: `7/2` rather than `3.5`. Version
9 needs no conversion step — a fraction stays exact, and it is the decimal
point that would make the arithmetic approximate.
:::

```sym 7
exact(3.5)
```
```sym 8
exact(3.5)
```

7/2

Because of the switches, this is a two interval problem. The first interval
is to be analyzed using DC. Notice that for t<0 the circuit is such that we
basically have two separate circuits. We simulate each one of them
separately:

```sym 7
s\dc("e1,0,1,7/2:r1,1,2,4:c,2,0,2:r2,2,0,1/6"):vc
```
```sym 8
s\dc("e1,0,1,7/2:r1,1,2,4:c,2,0,2:r2,2,0,1/6"):vc
```
```field 9 Circuit Description
e,0,1,7/2
r1,1,2,4
c,2,0,2
r2,2,0,1/6
```

::: only 9
The answer you want is `vc`, in **Results**.
:::

-7/50

```sym 7
s\dc("r3,3,0,1/6:l,3,0,1/50:r4,3,4,3:e2,4,0,3"):il
```
```sym 8
s\dc("r3,3,0,1/6:l,3,0,1/50:r4,3,4,3:e2,4,0,3"):il
```
```field 9 Circuit Description
r3,3,0,1/6
l,3,0,1/50
r4,3,4,3
e2,4,0,3
```

::: only 9
The answer you want is `il`, in **Results**.
:::

1

The second interval, for t≥0, is analyzed using TR. I could have described
the circuit again from scratch. But out of laziness I preferred to copy/paste
the descriptions from the DC simulations. To avoid renaming the nodes, I
simulated the right switch as a short circuit between nodes 2 and 3.

(-7/50)e{{sup:-3t}}cos(4t)-(1/50)e{{sup:-3t}}sin(4t)

e{{sup:-3t}}cos(4t)-e{{sup:-3t}}sin(4t)

::: only 9
`vc` comes back {{o:-(sin(4*t) + 7*cos(4*t))*exp(-3*t)/50}} and `il`
{{o:(cos(4*t) - sin(4*t))*exp(-3*t)}}.
:::

```sym 7
s\only("vc,il"):s\tr("c,1,0,2,-7/50:r,1,0,[1/6,1/6]:l,1,0,1/50,1")
```
```sym 8
s\only("vc,il"):s\tr("c,1,0,2,–7/50:r,1,0,[1/6,1/6]:l,1,0,1/50,1")
```
```field 9 Circuit Description
c,1,0,2,-7/50
r,1,0,[1/6,1/6]
l,1,0,1/50,1
```

```sym 7
vc
```
```sym 8
vc
```

```sym 7
il
```
```sym 8
il
```

The TR simulation took 30 s in my calculator. These are the right answers.

:::

::: problem Bo2's Example 6.3

Find i(t) and v(t) for the circuit shown below.

::: figure assets/practice/bo2s-example-6-3-34.jpg

:::

Since the sources change value, this is a two interval problem. For t<0, in
DC:

```sym 7
s\dc("e,1,0,5:r3,1,2,3:l,2,3,1:c,3,0,1:r1,3,0,1:j,0,3,1"):{vc,il}
```
```sym 8
s\dc("e,1,0,5:r3,1,2,3:l,2,3,1:c,3,0,1:r1,3,0,1:j,0,3,1"):{vc,il}
```
```field 9 Circuit Description
e,1,0,5
r3,1,2,3
l,2,3,1
c,3,0,1
r1,3,0,1
j,0,3,1
```

::: only 9
The answers you want are `vc` and `il`, in **Results**.
:::

{2,1}

Using these as initial conditions, now we use TR for t≥0:

```sym 7
s\only("vc,il"):s\tr("r3,0,2,3:l,2,3,1,1:c,3,0,1,2:r1,3,0,1"):{vc,il}
```
```sym 8
s\only("vc,il"):s\tr("r3,0,2,3:l,2,3,1,1:c,3,0,1,2:r1,3,0,1"):{vc,il}
```
```field 9 Circuit Description
r3,0,2,3
l,2,3,1,1
c,3,0,1,2
r1,3,0,1
```

{ (3t+2)e{{sup:-2t}} , (1-3t)e{{sup:-2t}} }

:::

### 

### Is the textbook wrong?

Anybody that has even written a textbook, or read one for that matter, can
attest to the fact that errors in the problems or the answers come with the
territory. (As a matter of fact, I am sure this book I am writing right now
has many errors.) We are all only human. Errors in an engineering textbook,
however, can be *very* frustrating to an engineering student. When one is
learning from a textbook, and the textbook has errors in the problems or
answers, confusion and hair-pulling will likely ensue. If you think you have
found an error in your circuit analysis textbook, Symbulator can help you
bring some sanity to the situation to confirm whether your guess is right.

Below is an example of using Symbulator to confirm an error in a textbook.

::: problem Bo2's Drill Exercise 6.4

::: figure assets/practice/bo2s-drill-exercise-6-4-35.jpg

:::

My copy of Bo2 is second-hand. I noticed this problem had scribbles on it.
The previous owner, evidently, struggled with this problem and concluded that
the value of the inductor had to be ½ H, not 1 H as the schematic says.
Symbulator can be used to show that he is right, and the book is wrong. Here
is how we do it. First, we can solve the circuit as shown, with a 1 H
inductor.

```sym 7
s\dc("e,2,0,2:r,1,2,1:l,1,0,1:c,1,0,1/8"):{il,vc}
```
```sym 8
s\dc("e,2,0,2:r,1,2,1:l,1,0,1:c,1,0,1/8"):{il,vc}
```
```field 9 Circuit Description
e,2,0,2
r,1,2,1
l,1,0,1
c,1,0,1/8
```

::: only 9
The answers you want are `il` and `vc`, in **Results**.
:::

{2,0}

```sym 7
s\only("il,vc"):s\tr("r,1,0,1:l,1,0,1,2:c,1,0,1/8,0"):{il,vc}
```
```sym 8
s\only("il,vc"):s\tr("r,1,0,1:l,1,0,1,2:c,1,0,1/8,0"):{il,vc}
```
```field 9 Circuit Description
r,1,0,1
l,1,0,1,2
c,1,0,1/8,0
```

The answer we get doesn't match the answer provided by the book. Now let's
repeat the TR simulation using the ½ H value for the inductor:

```sym 7
s\only("il,vc"):s\tr("r,1,0,1:l,1,0,1/2,2:c,1,0,1/8,0"):{il,vc}
```
```sym 8
s\only("il,vc"):s\tr("r,1,0,1:l,1,0,1/2,2:c,1,0,1/8,0"):{il,vc}
```
```field 9 Circuit Description
r,1,0,1
l,1,0,1/2,2
c,1,0,1/8,0
```

Now the answer we get matches the answer provided by the book. An expert user
of Symbulator can use the `fd` gate and the `t2s` tool, which we have not
discussed yet here, to find the value of the inductor given the book's
answer. Below is how I found the ½ H value myself, reverse-engineering the
answer:

::: only 9
```field 9 Evaluate
t2s(-16*t*e^(-4*t))
```

which gives {{o:-16/(s + 4)**2}}.
:::

```sym 7
s\t2s(-16*t*e^(-4*t)):
```
```sym 8
s\t2s(–16*t*e^(–4*t)):
```

-16/(s+4)^2

```sym 7
s\t2s((8*t+2)*e^(-4*t))
```
```sym 8
s\t2s((8*t+2)*e^(–4*t))
```

2\*(s+8)/(s+4)^2

```sym 7
s\fd("r,1,0,1:l,1,0,l,2:c,1,0,1/8,0"):vc
```
```sym 8
s\fd("r,1,0,1:l,1,0,l,2:c,1,0,1/8,0"):vc
```
```field 9 Circuit Description
r,1,0,1
l,1,0,l,2
c,1,0,1/8,0
```

::: only 9
Set **Analysis** to *FD — complex frequency domain*.

The answer you want is `vc`, in **Results**.
:::

-16\*l/(l\*s^2+8\*l\*s+8)

```sym 7
solve(-16/(s+4)^2=-16*l/(l*s^2+8*l*s+8),l)
```
```sym 8
solve(–16/(s+4)^2=–16*l/(l*s^2+8*l*s+8),l)
```

::: only 9
That is what the **Solve** card is for — a system that is not a circuit:

```field 9 Equation
-16/(s+4)^2 = -16*l/(l*s^2+8*l*s+8)
```

with `l` as the unknown. It answers `l` = {{o:1/2}}.
:::

l=1/2

The `fd` gate and `t2s` tool are used for frequency domain analysis, and will
be discussed separately in a subsequent part of Symbulator's documentation.

:::

::: problem Bo2's Drill Exercise 6.5

In the circuit below, suppose that v{{sub:S}}(t)= 12 – 12 u(t) V. Find
i{{sub:2}}(t) for t≥0.

::: figure assets/practice/bo2s-drill-exercise-6-5-36.jpg

:::

```sym 7
s\dc("e,3,0,12:r6,3,1,6:l1,1,0,6:r3,1,2,3:l2,2,0,4"):{il1,il2}
```
```sym 8
s\dc("e,3,0,12:r6,3,1,6:l1,1,0,6:r3,1,2,3:l2,2,0,4"):{il1,il2}
```
```field 9 Circuit Description
e,3,0,12
r6,3,1,6
l1,1,0,6
r3,1,2,3
l2,2,0,4
```

::: only 9
The answers you want are `il1` and `il2`, in **Results**.
:::

{2,0}

```sym 7
s\only("il2"):s\tr("r6,0,1,6:l1,1,0,6,2:r3,1,2,3:l2,2,0,4,0"):il2
```
```sym 8
s\only("il2"):s\tr("r6,0,1,6:l1,1,0,6,2:r3,1,2,3:l2,2,0,4,0"):il2
```
```field 9 Circuit Description
r6,0,1,6
l1,1,0,6,2
r3,1,2,3
l2,2,0,4,0
```

(12/11)(e{{sup:-3t}}-e{{sup:-t/4}})

:::

::: problem Bo2's Drill Exercise 6.6 (Op Amp)

In the circuit below, suppose that v{{sub:S}}(t)= 2 – 2 u(t) V. Find
v{{sub:o}}(t) for t≥0.

::: figure assets/practice/bo2s-drill-exercise-6-6-op-amp-37.jpg

:::

Simulate the first interval in DC to find the initial conditions of the
capacitors.

```sym 7
s\dc("e,3,0,2:r1,3,1,1:r2,1,2,2:r3,1,o,2:ca,1,0,1:
cb,2,o,1/4:o,0,2,o"):{vca,vcb}
```
```sym 8
s\dc("e,3,0,2:r1,3,1,1:r2,1,2,2:r3,1,o,2:ca,1,0,1:
cb,2,o,1/4:o,0,2,o"):{vca,vcb}
```
```field 9 Circuit Description
e,3,0,2
r1,3,1,1
r2,1,2,2
r3,1,o,2
ca,1,0,1
cb,2,o,1/4
o,0,2,o
```

::: only 9
The answers you want are `vca` and `vcb`, in **Results**.
:::

{0,4}

Then simulate the second interval in TR, to find the voltage in node *o*.

(-4t-4)e{{sup:-t}}

```sym 7
s\only("vo"):s\tr("r1,0,1,1:r2,1,2,2:r3,1,o,2:
ca,1,0,1,0:cb,2,o,1/4,4:o,0,2,o"):vo
```
```sym 8
s\only("vo"):s\tr("r1,0,1,1:r2,1,2,2:r3,1,o,2:
ca,1,0,1,0:cb,2,o,1/4,4:o,0,2,o"):vo
```
```field 9 Circuit Description
r1,0,1,1
r2,1,2,2
r3,1,o,2
ca,1,0,1,0
cb,2,o,1/4,4
o,0,2,o
```

:::

::: problem Bo2's Example 6.5 (Plot)

In the circuit below, use v{{sub:S}}=2/5V, R=12Ω, L=2H and C=1/50F. Find v(t)
and i(t), and plot them for time 0<t<1.5 seconds.

::: figure assets/practice/bo2s-example-6-5-plot-38.jpg

:::

```sym 7
s\only("vc,il"):s\tr("e,1,0,2/5:r,1,2,12:l,2,3,2,0:c,3,0,1/50,0")
```
```sym 8
s\only("vc,il"):s\tr("e,1,0,2/5:r,1,2,12:l,2,3,2,0:c,3,0,1/50,0")
```
```field 9 Circuit Description
e,1,0,2/5
r,1,2,12
l,2,3,2,0
c,3,0,1/50,0
```

```sym 7
vc
```
```sym 8
vc
```

-(2/5)e{{sup:-3t}}cos(4t)-(3/10)e{{sup:-3t}}sin(4t)+2/5

```sym 7
il
```
```sym 8
il
```

(1/20)e{{sup:-3t}}sin(4t)

::: only 9
We look in the results and see that `vc` is the first of those and `il` the
second.
:::

These are the right answers. To plot them, run the `plot` tool, thus:
s\plot(). Once the plot window opens, enter `vc` as function, `0` as minimal
time and `1.5` as maximal time. Compare to the graph from the book, shown
below. Repeat the plot for `il`, and compare to the graph from the book
below.

::: figure assets/practice/bo2s-example-6-5-plot-39.jpg

:::

:::

::: problem Bo2's Drill Exercise 6.7

For the circuit in Bo2's Example 6.5, use v{{sub:S}}=3V, R=5Ω, L=1/2H and
C=1/8F. Find v(t) and i(t).

```sym 7
s\only("vc,il"):s\tr("e,1,0,3:r,1,2,5:l,2,3,1/2,0:c,3,0,1/8,0"):{vc,il}
```
```sym 8
s\only("vc,il"):s\tr("e,1,0,3:r,1,2,5:l,2,3,1/2,0:c,3,0,1/8,0"):{vc,il}
```
```field 9 Circuit Description
e,1,0,3
r,1,2,5
l,2,3,1/2,0
c,3,0,1/8,0
```

{ -4e{{sup:-2t}}+e{{sup:-8t}}+3 , e{{sup:-2t}}-e{{sup:-8t}} }

:::

::: problem Bo2's Drill Exercise 6.8 (Ramp)

For the circuit in Bo2's Drill Exercise 6.7, find the voltage drop in the
capacitor v(t) if the source has a value v{{sub:S}}(t) = 3 r(t).

2e{{sup:-2t}}-(e{{sup:-8t}})/8+3t-15/8

```sym 7
s\only("vc"):s\tr("e,1,0,3t:r,1,2,5:l,2,3,1/2,0:c,3,0,1/8,0"):vc
```
```sym 8
s\only("vc"):s\tr("e,1,0,3t:r,1,2,5:l,2,3,1/2,0:c,3,0,1/8,0"):vc
```
```field 9 Circuit Description
e,1,0,3t
r,1,2,5
l,2,3,1/2,0
c,3,0,1/8,0
```

:::

::: problem Bo2's Example 6.6 (Plot)

For the circuit below, plot the voltage drop in the inductor for 0 < t < 5ms.

::: figure assets/practice/bo2s-example-6-6-plot-40.jpg

:::

First, find the initial conditions for t<0 by running a DC simulation.

```sym 7
s\dc("e,1,0,12:r,1,2,3:l,2,3,1:c,3,0,1'µ:s,3,0"):{il,vc}
```
```sym 8
s\dc("e,1,0,12:r,1,2,3:l,2,3,1:c,3,0,1'µ:s,3,0"):{il,vc}
```
```field 9 Circuit Description
e,1,0,12
r,1,2,3
l,2,3,1
c,3,0,1'µ
s1,3,0
```

::: only 9
The answers you want are `il` and `vc`, in **Results**.
:::

{4,0}

Then, find the `vl` for t≥0 by running a TR simulation.

```sym 7
s\only("vl"):s\tr("e,1,0,12.:r,1,2,3:l,2,3,1,4:c,3,0,1'µ,0")
```
```sym 8
s\only("vl"):s\tr("e,1,0,12.:r,1,2,3:l,2,3,1,4:c,3,0,1'µ,0")
```
```field 9 Circuit Description
e,1,0,12.
r,1,2,3
l,2,3,1,4
c,3,0,1'µ,0
```

Finally, run `s\plot()` and enter `vl` as function, `0` as minimal time and
`0.005` as maximal time. In the resulting plot you will see something
outstanding: around t = 1.57 ms, the voltage drop across the inductor is 3991
volts!

:::

::: problem Bo2's Drill Exercise 6.9

For the circuit below, R=1Ω, L=2H, C=1/2F and i{{sub:S}}(t)=u(t). Find i(t)
and v(t).

::: figure assets/practice/bo2s-drill-exercise-6-9-41.jpg

:::

```sym 7
s\only("il,vc"):s\tr("j,0,1,1:r,1,0,1:l,1,0,2,0:c,1,0,1/2,0"):{il,vc}
```
```sym 8
s\only("il,vc"):s\tr("j,0,1,1:r,1,0,1:l,1,0,2,0:c,1,0,1/2,0"):{il,vc}
```
```field 9 Circuit Description
j,0,1,1
r,1,0,1
l,1,0,2,0
c,1,0,1/2,0
```

{ (-t-1)e{{sup:-t}}+1 , 2te{{sup:-t}} }

:::

::: problem Bo2's Figure 6.23 (Op Amp)

For the circuit below, find v{{sub:o}}(t) if v{{sub:S}}(t) = u(t).

::: figure assets/practice/bo2s-figure-6-23-op-amp-42.jpg

:::

```sym 7
s\only("vo"):s\tr("e,3,0,1:r1,3,1,1:r2,1,2,1:
ca,2,0,1/5,0:cb,1,o,1,0:o,2,o,o"):vo
```
```sym 8
s\only("vo"):s\tr("e,3,0,1:r1,3,1,1:r2,1,2,1:
ca,2,0,1/5,0:cb,1,o,1,0:o,2,o,o"):vo
```
```field 9 Circuit Description
e,3,0,1
r1,3,1,1
r2,1,2,1
ca,2,0,1/5,0
cb,1,o,1,0
o,2,o,o
```

1-e{{sup:-t}} cos(2t)-(1/2)e{{sup:-t}} sin(2t)

:::

::: problem Bo2's Drill Exercise 6.10 (Op Amp)

In the circuit above, change capacitor's value from 1/5 F to 25/16 F. Find
v{{sub:o}}(t) if v{{sub:S}}(t) = 3 u(t).

-4e{{sup:-2t/5}}+e{{sup:-8t/5}}+3

```sym 7
s\only("vo"):s\tr("e,3,0,3:r1,3,1,1:r2,1,2,1:
ca,2,0,25/16,0:cb,1,o,1,0:o,2,o,o"):vo
```
```sym 8
s\only("vo"):s\tr("e,3,0,3:r1,3,1,1:r2,1,2,1:
ca,2,0,25/16,0:cb,1,o,1,0:o,2,o,o"):vo
```
```field 9 Circuit Description
e,3,0,3
r1,3,1,1
r2,1,2,1
ca,2,0,25/16,0
cb,1,o,1,0
o,2,o,o
```

:::

::: problem Bo2's Drill Exercise 6.11 (p307)

For the circuit below, suppose that R{{sub:1}} = R{{sub:2}} = 1Ω, L = 1H, C =
1F and v{{sub:S}}(t)= 2e{{sup:-2t}} u(t). Find i(t) if all initial conditions
are zero.

::: figure assets/practice/bo2s-drill-exercise-6-11-p307-43.jpg

:::

```sym 7
s\only("il"):s\tr("e,3,0,2e^(-2t):r2,3,2,1:r1,2,1,1:c,2,0,1,0:l,1,0,1,0"):il
```
```sym 8
s\only("il"):s\tr("e,3,0,2e^(–2t):r2,3,2,1:r1,2,1,1:c,2,0,1,0:l,1,0,1,0"):il
```
```field 9 Circuit Description
e,3,0,2e^(-2t)
r2,3,2,1
r1,2,1,1
c,2,0,1,0
l,1,0,1,0
```

-(e{{sup:t}} cos(t)-e{{sup:t}} sin(t)-1) e{{sup:-2t}}

:::

::: problem A more complex problem

The circuit below comes from the circuits analysis class of Professor Eliane
Boulet de Cabrera, from Universidad Tecnologica de Panama. Find v1 and v.

::: figure assets/practice/a-more-complex-problem-44.png

:::

Because of the switches, this is a two interval problem. The first is run in
DC.

```sym 7
s\dc("e,3,0,18:r8,3,1,8:ca,1,0,1/6:r12,1,0,12:
r18,1,2,18:r6,2,0,6:cb,2,0,1/3"):{vca,vcb}
```
```sym 8
s\dc("e,3,0,18:r8,3,1,8:ca,1,0,1/6:r12,1,0,12:
r18,1,2,18:r6,2,0,6:cb,2,0,1/3"):{vca,vcb}
```
```field 9 Circuit Description
e,3,0,18
r8,3,1,8
ca,1,0,1/6
r12,1,0,12
r18,1,2,18
r6,2,0,6
cb,2,0,1/3
```

::: only 9
The answers you want are `vca` and `vcb`, in **Results**.
:::

{9,9/4}

These serve as initial conditions for the second interval, which is run in
TR. Since we only want v1 and v2, it pays off to let Symbulator know this:

```sym 7
s\only("v1,v2"):
```
```sym 8
s\only("v1,v2"):
```

```sym 7
s\tr("ca,1,0,1/6,9:r12,1,0,12:r18,1,2,18:r6,2,0,6:
cb,2,0,1/3,9/4:j,0,2,10e^(-t)sin(2t+30°)")
```
```sym 8
s\tr("ca,1,0,1/6,9:r12,1,0,12:r18,1,2,18:r6,2,0,6:
cb,2,0,1/3,9/4:j,0,2,10e^(–t)sin(2t+30°)")
```
```field 9 Circuit Description
ca,1,0,1/6,9
r12,1,0,12
r18,1,2,18
r6,2,0,6
cb,2,0,1/3,9/4
j,0,2,10*exp(-t)*sin(2*t+(30*pi/180))
```

::: only 9
Set **Analysis** to *TR — transient / time domain*.
:::

Be patient. This took 78 seconds in my calculator, including over half a
minute just to find the inverse Laplace of the two desired answers.

(53/17-20/17)e{{sup:-t}} cos(2t)+(-203/17-5/17)e{{sup:-t}} sin(2t)+(803/17+193/34)e{{sup:-t/2}}+(9/2-53)e{{sup:-t}}

(-2453/34-20/17)e{{sup:-t}} cos(2t)+(245/34-203/17)e{{sup:-t}} sin(2t)+(803/17+193/34)e{{sup:-t/2}}+(53/2-9/4)e{{sup:-t}}

::: only 9
Version 9 answers this one in about a second. `v1` and `v2` are in
**Results**; they are long enough that they are easier read on screen than
in print.
:::

```sym 7
v1
```
```sym 8
v1
```

```sym 7
v2
```
```sym 8
v2
```

These are the correct answers, which explains why Professor Boulet – who made
the problem up - is a living legend among circuit students at UTP.

:::

### Advanced use of Expert in TR

The **expert** tool can be very useful in transient analysis. Using it,
however, requires some knowledge. Here’s two things you need to know in order
to use `ex` like a boss:

First, when Symbulator solves a problem using TR, it follows these general
steps:

- Generate a set of equations and unknowns for the system, in the frequency domain. Any time-dependent source is replaced with a dummy variable.
- Solve these frequency domain equations.
- Replace any dummy variable with the original source value, and convert the answers to the time domain.

Second, when Symbulator solves a problem using the expert tool, it freezes
this process halfway between steps 1 and 2, so that you can tinkle with the
equations and unknowns before they are solved.

::: only 7,8
In the problems below, you will see that, when we tinkle with the equations,
we have to do so in the frequency domain.
:::
::: only 9
That is where version 9 differs, and it is the more comfortable of the two.
The equations are still solved in the frequency domain — that has not
changed, and it is why initial conditions and impulses behave as they do —
but what you *type* is read in the **time domain**, and converted for you on
the way in. Write the answer you know the way you would write it on paper.

The rule covers everything you add: equations, conditions and the
expressions inside them. A relation between plain parameters, such as
`x = 3`, is left alone — it fixes a symbol in the circuit rather than
describing a signal, and there is nothing to transform.
:::

::: problem Bo2's Drill Exercise 4.5 (Expert)

For this circuit, we know that the capacitor’s initial condition is zero,
that v{{sub:s}} is an unknown step source (e.g. of the form A *u(t)*, where A
is a constant value in volts) and that the voltage drop in the capacitor for
t>0 is found to be 1-e^(-t/2). Find the voltage drop in the resistor, the
current through the capacitor and the value of the source.

::: figure assets/practice/bo2s-drill-exercise-4-5-expert-45.png

:::

This problem is a match made in heaven for the **expert** tool, because we
have one unknown value in the circuit (e.g. the value of the step source) and
we have one known answer (e.g. the voltage drop in the capacitor.) So, the
game plan here is to run this circuit through Symbulator’s expert mode, add
one new equation and one new unknown, and then solve. First, let’s generate
the new equation.

::: only 7,8
A non-expert user would think that the new equation is 1-e^(-t/2)=vc. But you
know better. You know that Symbulator solves the equations of TR problems in
the frequency domain. So we have to convert this expression from the time
domain to the frequency domain. Symbulator has a shortcut to invoke
DiffEq’s Laplace Transform to do so: `s\t2s`.
:::

::: only 9
The non-expert user is right here: the new equation is simply
`1-e^(-t/2) = vc`. Everything you type into expert mode in version 9 —
equations, conditions, expressions — is read in the **time domain**, the
same domain as the answers on screen. You do not convert, and you do not
have to remember which side of the transform you are standing on.

::: note The calculator does not offer this at all
Expert mode on the calculator asks *Analysis? 1:DC 2:AC 3:FD* — TR is not
among the choices, which is how it avoided the question. Version 9 keeps
expert mode for TR and answers the question instead: everything is in time.
:::

If you would rather convert by hand, **t2s** is still there and an equation
already written in s is left alone rather than transformed twice:

```field 9 Evaluate
t2s(1-e^(-t/2))
```

which gives {{o:1/(s*(2*s + 1))}} — the same statement, one domain over.
:::

```sym 7
s\t2s(1-e^(-t/2))=vc
```
```sym 8
s\t2s(1-e^(–t/2))=vc
```

We have our new equation. Copy this equation into the clipboard, since we
will want to paste it in the Expert window. Now let’s run the Expert
simulation of the circuit. Let’s define the value of the source as `a*u(t)`,
since we know it’s a step source; the variable `a` will serve as the unknown
value, for which we will solve in the Expert mode.

```sym 7
s\ex("e,1,0,a*u(t):r,1,2,2:c,2,0,1,0")
```
```sym 8
s\ex("e,1,0,a*u(t):r,1,2,2:c,2,0,1,0")
```
```field 9 Circuit Description
e,1,0,a*Heaviside(t)
r,1,2,2
c,2,0,1,0
```

::: only 7,8
When prompted, select TR as the desired option. Then you will see the typical
Expert prompt. In the equations field, paste the new equation, adding the
word` and `first:
:::
::: only 9
Choose TR, then open **Expert Mode**. **Add equations** takes one per line,
so there is no ` and ` to prefix — the word exists on the calculator only
because the equation is being appended to a list:

```field 9 Add equations
1-e^(-t/2) = vc
```
:::

```sym 7
and 1/s-2/(2*s+1)=vc
```
```sym 8
and 1/s-2/(2*s+1)=vc
```

::: only 7,8
In the unknown field, add the variable a, preceded by a comma:
:::
::: only 9
**Add unknowns** likewise takes the name on its own, with no leading comma:

```field 9 Add unknowns
a
```
:::

```sym 7
,a
```
```sym 8
,a
```

Let Symbulator solve the equations now. Once it is done, we want to do a
quick sanity check. If the system solved correctly, we should see that
Symbulator has as voltage drop in the capacitor the expression we already
know from the problem statement:

```sym 7
vc
```
```sym 8
vc
```

::: only 7,8
1-e{{sup:-t/2}}
:::
::: only 9
`vc` in **Results** reads {{o:1 - exp(-t/2)}}, which it does.
:::

::: only 7,8
This is correct, so we proceed to ask for the answers we want:
:::
::: only 9
This is correct, and the answers we want are on screen with it: `ic` is
{{o:exp(-t/2)/2}}, and the resistor's **voltage drop** line gives
{{o:exp(-t/2)}}.
:::

```sym 7
ic
```
```sym 8
ic
```

::: only 7,8
(1/2)e{{sup:-t/2}}
:::

```sym 7
vr
```
```sym 8
vr
```

::: only 7,8
e{{sup:-t/2}}
:::

```sym 7
a
```
```sym 8
a
```

These are the correct answers. The value of the step source is 1 volt.

:::

::: problem Bo2's Drill Exercise 4.13 (Expert)

::: figure assets/practice/bo2s-drill-exercise-4-13-expert-46.png

:::

This problem is solved just like the one we already saw. First, find the new
equation:

```sym 7
vr=s\t2s(e^(-t))
```
```sym 8
vr=s\t2s(e^(–t))
```

::: only 9
No transform this time either — write what you know:

```field 9 Add equations
vr = e^(-t)
```
:::

Then run the Expert simulation. I decided to use `vs` as the step value of
the source:

```sym 7
s\ex("e,1,0,vs*u(t):r,1,2,1:c,2,0,1,0"):
```
```sym 8
s\ex("e,1,0,vs*u(t):r,1,2,1:c,2,0,1,0"):
```
```field 9 Circuit Description
e,1,0,vs*u(t)
r,1,2,1
c,2,0,1,0
```

::: only 7,8
When prompted, select TR. In the equations field, add the new equation you
found:
:::
::: only 9
Choose TR, and put `vs` in **Add unknowns** beside the equation above.
:::

```sym 7
and vr=1/(s+1)
```
```sym 8
and vr=1/(s+1)
```

::: only 7,8
In the unknowns field, add the new variable:
:::

```sym 7
,vs
```
```sym 8
,vs
```

::: only 7,8
Let Symbulator rip. Once it finishes solving, ask for the sanity check:
:::
::: only 9
Run it. The sanity check is already on screen: `vr` reads
{{o:exp(-t)}}, which is what we told it.
:::

```sym 7
vr
```
```sym 8
vr
```

::: only 7,8
e{{sup:-t}}
:::

::: only 7,8
Looks good, so go ahead and ask for the answers:
:::
::: only 9
And the answers with it: `ir` is {{o:exp(-t)}} and the source's value
`vs` is {{o:1}} V.
:::

```sym 7
ir
```
```sym 8
ir
```

::: only 7,8
e{{sup:-t}}
:::

```sym 7
vc
```
```sym 8
vc
```

::: only 7,8
1-e{{sup:-t}}
:::

```sym 7
vs
```
```sym 8
vs
```

Ain’t that a beauty? Yes, ma’am! Atta boy, Symbulator! Atta boy!

:::

::: problem Bo2's 164 (Expert)

::: figure assets/practice/bo2s-164-expert-47.png

:::

This is the same thing as the previous two, so there is no need for
commentary.

```sym 7
il=s\t2s(1-e^(-2*t))
```
```sym 8
il=s\t2s(1-e^(–2*t))
```

```sym 7
s\ex("e,1,0,vs*u(t):r,1,2,2:l,2,0,1,0")
```
```sym 8
s\ex("e,1,0,vs*u(t):r,1,2,2:l,2,0,1,0")
```
```field 9 Circuit Description
e,1,0,vs*Heaviside(t)
r,1,2,2
l,2,0,1,0
```

::: only 7,8
Choose TR, and add `,vs` to the unknowns and the following to the equations
:::
::: only 9
Choose TR, put `vs` in **Add unknowns**, and give **Add equations** the
answer you know — in time, as always here:

```field 9 Add equations
1-e^(-2*t) = il
```
:::

```sym 7
and il=1/s-1/(s+2)
```
```sym 8
and il=1/s-1/(s+2)
```

{{v7,8|And solve. When done, ask for the sanity check:}}{{v9|Run it,
then put the sanity check into **Evaluate**:}}

```sym 7
il
```
```sym 8
il
```

::: only 7,8
1-e{{sup:-2t}}
:::

::: only 7,8
Since that adds up, ask for the answers:
:::
::: only 9
It does add up — `il` reads {{o:1 - exp(-2*t)}} — and the answers are on
screen with it: `vl` is {{o:2*exp(-2*t)}}, `vr` is
{{o:2 - 2*exp(-2*t)}}, and the source's value `vs` is {{o:2}} V.
:::

```sym 7
vl
```
```sym 8
vl
```

::: only 7,8
2e{{sup:-2t}}
:::

```sym 7
vr
```
```sym 8
vr
```

::: only 7,8
2-2e{{sup:-2t}}
:::

```sym 7
vs
```
```sym 8
vs
```

::: only 7,8
2
:::

```sym 7
vl*il
```
```sym 8
vl*il
```

::: only 7,8
2e{{sup:-4t}}(e{{sup:2t}}-1)
:::

This is the end of the TR section of the book.

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
