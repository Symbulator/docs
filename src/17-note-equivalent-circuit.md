---
id: equivalent-circuit
kind: note
title: When a load is not the only thing attached
versions: [9]
updated: 2026-09-11
books: [4a, 4b]
summary: >
  The load formulas assume a load and nothing else. When something more is connected to the equivalent, Symbulator will write the equivalent circuit into the input fields for you, ready to be added to.
---

Lesson 4's load answers — `irl`, `vrl`, `prl` and `pmax` — are formulas, and
they hold only when a load is the one thing connected to the equivalent
circuit. Connect anything else to those terminals and none of them applies
any more, and the problem has to be run as a circuit again.{{i:load problems (irl, vrl, prl)}}

Symbulator will write that circuit for you, so you are adding to it rather
than typing it out.

## The button

With the load question ticked, a button appears at the foot of
{{card:Results}}, under the equivalent's answers:
{{btn:Load circuit equivalent?}} It is live once the equivalent has been
found, and goes dead again if you change any input until you run again.{{i:equivalent circuit button}}

Press it and it warns you first: the equivalent circuit will overwrite the
{{card:Circuit Description}}, {{card:Define}} and {{card:Expert Mode}} fields
and switch the analysis to *Solve circuit*, so a circuit you have not saved
yet can be saved before it goes. Proceed, and the description becomes

```field 9 Circuit Description
jN,0,n,iNo
rE,n,0,rEq
rL,n,0,load
```

with {{card:Define}} holding the values of `iNo` and `rEq` that
{{card:Results}} found, exact rather than rounded, and a value for `load` if
you had given it one. It is the Norton equivalent connected, between nodes
**n** and **0**, to a load called **rL** with the symbolic value **load**, in
ohms. You can use it as a starting point.

## An example

::: problem RM3's Example 9-8
Find the Norton equivalent of the circuit left of a-b; then find the current
through {{var:R_L}}.

::: figure assets/circuit/rm3e0908.jpg
RM3's Example 9-8
:::

::: answer
Let's first find the circuit equivalent:

```field 9 Circuit Description
e,1,0,24
r1,1,2,120
r2,2,0,280
j,2,0,560'm
```

*Find equivalent*, *Thévenin / Norton*, nodes **2** and **0**, in DC, with
the load question ticked. {{card:Results}} gives:

::: result
i_{no} = -0.36\ \mathrm{A}
:::
::: result
R_{eq} = 84\ \Omega
:::

The Norton current is reported in the direction it actually flows, from the
first node to the second. Carry the sign through and the load current below
comes out the same.

Now to the second part of the question. In order to find the current through
{{var:R_L}}, we cannot use the load expressions, because now the load is not
the only thing connected to the terminals of the equivalent: there is also a
current source. We have to run a new simulation.

The fastest way is the button above. Proceed past its warning and the
description is replaced by the equivalent, with `iNo` and `rEq` already in
{{card:Define}}:

```field 9 Circuit Description
jN,0,n,iNo
rE,n,0,rEq
rL,n,0,load
```

We change the value of the load to 168 Ω, and add the 180 mA source flowing
from node **0** to node **n**. Then we run a DC simulation and ask for the
current in the load:

```field 9 Circuit Description
jN,0,n,iNo
rE,n,0,rEq
rL,n,0,168
j,0,n,180'm
```

::: applink RM3's Example 9-8 (with the load)
:::

The analysis is already *Solve circuit*; run it in DC, with **SI prefixes**
ticked in {{card:Settings}}. The current through **rl**, `irl`, reads
{{o:-60}} mA.

Correct: there is a current of 60 mA flowing through {{var:R_L}} from 0 to n.

Using the equivalent circuit description is meant to save you time. If you
find it confusing to use, just don't use it.
:::
:::
