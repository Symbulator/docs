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
rest of the circuit needs.

```field 9 Circuit Description
e,1,0,2
r1,1,m,10'k
r2,m,o,47'k
o1,0,m,o
```

The inverting amplifier. Node **m** is the summing junction, **o** the
output.

::: result voltage drop across r2
v_{r2} = \dfrac{47}{5}\,\mathrm{V}
:::

So the output sits at −9.4 V: a gain of −4.7, which is −47k/10k, arrived at
from the nullor conditions rather than from the formula.

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
which is what a finite-gain op amp is:

```field 9 Circuit Description
e,1,0,2
r1,1,m,10'k
r2,m,o,47'k
ea,o,0,100000*(0-vm)
```

`ea` is a VCVS of gain 10⁵ driving the output node from the differential
input — here `0 - vm`, the non-inverting input minus the inverting one.
Solve it and the answer differs from the ideal one in the fifth figure,
which is the honest way to find out whether the ideal model was good enough
for your problem.

The same shape gives you finite input impedance (a resistor across the
inputs) and non-zero output impedance (a resistor in series with `ea`).
Once you are modelling it, the op amp is just circuit elements.

::: tip The ideal answer first
Run the nullor version, then the modelled one, and compare. If they agree
to more figures than your problem needs, the ideal answer was the right
one and the model was wasted work.
:::
