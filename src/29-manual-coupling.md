---
id: manual-coupling
kind: manual
book: manual
title: Mutual inductance and transformers
versions: [9]
updated: 2026-09-11
summary: >
  m couples two named inductors and the node order carries the dots. t is an ideal transformer, two-terminal or four.
---

## m — mutual inductance

`m` names **two inductors**, not two nodes:{{i:mutual inductance}}

```
m1,l1,l2,0.01
```

Those are the names of two `l` elements already in the circuit, and the
last field is *M* in henries. It may be a symbol, and it may carry an SI
prefix.

**An `m` has no answers of its own.** It is a statement about two other
elements; its effect turns up in their currents.

### The dots are the node order

Symbulator cannot draw a dot, so **the first node you name in each coupled
inductor is its dotted end.** That is the whole convention, and it is the
one most likely to hand you a correct-looking wrong answer.{{i:dot convention}}

Two 30 mH coils coupled by 10 mH, the first across a 10 V source and the
second across a 30 Ω load, at 1000 rad/s. We name the coils `l1` and `l2`
and the load `r2`, and we write each coil's dotted end first, node 1 for
the primary and node 2 for the secondary:

```field 9 Circuit Description
e,1,0,10
l1,1,0,0.03
l2,2,0,0.03
m1,l1,l2,0.01
r2,2,0,30
```

Run in AC at ω = 1000, the current in the load is

::: result current through r2
i_{r2} = 0.0621 - 0.0552\text{j}\,\mathrm{A}
:::

Now write the second coil the other way round, `l2,0,2,0.03`, the same
coil with its dot at the other end, and run again:

::: result current through r2
i_{r2} = -0.0621 + 0.0552\text{j}\,\mathrm{A}
:::

Exactly the negative. Same magnitude, opposite sign, no error message.
Nothing will warn you.

So: read the schematic, decide which end of each coil carries the dot, and
name that node first in **both** coupled elements.

## t — the ideal transformer

```
t1,n1,n2,turns1,turns2
```

The two-node form names the top terminal of each side and grounds the other
two. A 120 V source on the primary, a 5 Ω load on the secondary, ten turns
to one; we name the transformer `t1` and the load `rl`, and call the two
tops node **1** and node **2**:{{i:transformer}}

```field 9 Circuit Description
e,1,0,120
t1,1,2,10,1
rl,2,0,5
```

Run in DC, the load's voltage and current are

::: result voltage drop across rl
v_{rl} = 12\,\mathrm{V}
:::
::: result current through rl
i_{rl} = \dfrac{12}{5}\,\mathrm{A}
:::

Ten to one, so a tenth of the 120 V across the load.

An ideal transformer has no leakage, no magnetising current and no losses.
For a real one, model it as coupled inductors with `m` instead — that is
the same choice you make on paper.

### Four terminals

When neither side sits on ground, name all four with bracketed pairs:

```
t1,[tl,bl],[tr,br],[10,1]
```

`[tl,bl]` is the left port, top terminal first; `[tr,br]` the right. The
turns must then be bracketed too. The two-node form is exactly this with
both bottoms on `0`.{{i:four-terminal form}}

A transformer reports **a current at each live terminal** rather than one
current, since the two sides carry different ones. The names are the
element's name followed by the node's: for `t1` with ports at nodes **1**
and **2**, they are `it11` and `it12`.

The same bracketed-pair form works on two-port blocks; see
{{ref:manual-twoports}}.
