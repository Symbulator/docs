---
id: manual-opamps
kind: manual
book: manual
title: Operational amplifiers
versions: [9]
updated: 2026-09-11
summary: >
  The o element is an ideal op amp — a nullor. What that buys you, what it hides, and how to model a real one when the ideal answer is not enough.
---

`o` takes three nodes, in this order:

```
o1,n+,n−,nout
```

No power rails, no supply, no gain figure. It is an **ideal** op amp: a
nullor, which is the statement that the two inputs are at the same
potential and draw no current, and that the output supplies whatever the
rest of the circuit needs.{{i:operational amplifier}}{{i:nullor}}

An inverting amplifier: a 2 V source into the op amp's inverting input
through 10 kΩ, a 47 kΩ resistor feeding the output back to that input, and
the non-inverting input on ground. We name the source `e` and the
resistors `r1` and `r2`, call the summing junction **m** and the output
**o**, and write the op amp's three nodes in the order the element wants,
non-inverting input first:

```field 9 Circuit Description
e,1,0,2
r1,1,m,10'k
r2,m,o,47'k
o1,0,m,o
```

Run in DC, the output is

::: result voltage at node o
v_{o} = -\dfrac{47}{5}\,\mathrm{V}
:::

That is −9.4 V from 2 V, a gain of −4.7, which is −47k/10k, arrived at from
the nullor conditions rather than from the formula.

Note the node order — **0** is the non-inverting input and **m** the
inverting one. Swap them and the feedback becomes positive, which is a
different circuit and will usually refuse to solve.

## What the op amp reports

An `o` reports a **current** and a **power**, and no voltage drop — its
input terminals are at the same potential by definition, so a drop across
it would not mean anything. The current is the one it sources or sinks at
its output.

## When ideal is not enough

There is no finite-gain op amp element. Model one as a dependent source,
which is what a finite-gain op amp is. The same amplifier, with the `o`
element replaced by a voltage source we call `ea`, driving the output node
with 100,000 times the voltage between the two inputs — the non-inverting
one, at ground, minus the inverting one at **m**:{{i:op amp model (finite gain)}}

```field 9 Circuit Description
e,1,0,2
r1,1,m,10'k
r2,m,o,47'k
ea,o,0,100000*(0-vm)
```

Run in DC, the output is now

::: result voltage at node o
v_{o} = -\dfrac{9400000}{1000057}\,\mathrm{V}
:::

which is −9.39946 V against the ideal −9.4 V: the two differ in the fifth
figure, which is the honest way to find out whether the ideal model was
good enough for your problem.

The same shape gives you finite input impedance (a resistor across the
inputs) and non-zero output impedance (a resistor in series with `ea`).
Once you are modelling it, the op amp is just circuit elements.

::: tip The ideal answer first
Run the nullor version, then the modelled one, and compare. If they agree
to more figures than your problem needs, the ideal answer was the right
one and the model was wasted work.
:::
