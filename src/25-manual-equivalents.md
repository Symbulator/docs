---
id: manual-equivalents
kind: manual
book: manual
title: Equivalents and the load question
versions: [9]
updated: 2026-09-11
summary: >
  Equivalent resistance, Thévenin and Norton at a pair of nodes, and the load answers that come with them.
---

Two of the four tools answer a question *about* a circuit instead of
solving it. Both take a pair of nodes.

## Equivalent resistance

*Find equivalent → Resistance / impedance*, with the two nodes.{{i:equivalent resistance}}

Three resistors and no source: a 100 Ω in series with a 200 Ω and a 300 Ω
in parallel, and the question is the resistance of the whole seen from its
two ends. We name them `r1` to `r3`, call the free end node **1** and the
junction node **2**, and put the far end on ground:

```field 9 Circuit Description
r1,1,2,100
r2,2,0,200
r3,2,0,300
```

Open {{card:Find equivalent}}, choose *Resistance / impedance*, and give
the two nodes **1** and **0**:

::: result equivalent resistance
R_{eq} = 220\,\Omega
:::

100 Ω in series with 200 ‖ 300. No source is needed and none is present:
this is a question about the network, not about a circuit that runs.

**If the circuit does contain independent sources**, they are suppressed
first — voltage sources shorted, current sources opened — which is the
textbook procedure. Dependent sources are not suppressed, because they are
part of the network's behaviour.{{i:passive circuit}}

In AC the same tool returns an impedance, and the menu says so.

## Thévenin and Norton

*Find equivalent → Thévenin / Norton*, with the two nodes. One run returns
both forms, because they are the same two numbers.{{i:Thévenin equivalent}}

A 20 V source and a divider of 50 Ω and 150 Ω, and the question is what
the circuit looks like from the divider's midpoint: a single source behind
a single resistance. We describe the three elements, naming them `e`, `r1`
and `r2`, and call the midpoint node **2**:

```field 9 Circuit Description
e,1,0,20
r1,1,2,50
r2,2,0,150
```

Open {{card:Find equivalent}}, choose *Thévenin / Norton*, and give the two
terminals **2** and **0**:

::: result Thévenin voltage
v_{th} = 15\,\mathrm{V}
:::
::: result equivalent resistance
R_{eq} = \dfrac{75}{2}\,\Omega
:::
::: result Norton current
i_{no} = \dfrac{2}{5}\,\mathrm{A}
:::

**The Norton current is reported in the direction it actually flows**, from
the first node to the second. Carry the sign through rather than assuming a
positive value.{{i:Norton equivalent}}

A fourth answer comes with those three, unasked:

::: result maximum deliverable power
p_{max} = \dfrac{3}{2}\,\mathrm{W}
:::

`pmax` is the maximum power transfer result — the power delivered when the
load equals `R_eq`, which for this circuit is 15²/(4×37.5).{{i:maximum power transfer}}

## The load question

Under the two node boxes is a tick: **Are you running a problem with a load
connected to this equivalent circuit?** It adds three more answers, each an
expression in a symbol `load`:{{i:load problems (irl, vrl, prl)}}

| | |
|---|---|
| `irl` | current in the load |
| `vrl` | voltage drop in the load |
| `prl` | power consumed in the load |

Give `load` a value in {{card:Define}} and all three become numbers.

::: warning The load formulas assume a load and nothing else
They hold only when the load is the one thing across those terminals.
Connect anything more and none of them applies; the problem has to be run
as a circuit again. {{ref:equivalent-circuit}} covers the button that
writes that circuit for you.
:::
