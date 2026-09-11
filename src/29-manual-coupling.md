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

`m` names **two inductors**, not two nodes:

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
one most likely to hand you a correct-looking wrong answer.

```field 9 Circuit Description
e,1,0,10
l1,1,0,0.03
l2,2,0,0.03
m1,l1,l2,0.01
r2,2,0,30
```

At ω = 1000 the current in **r2** comes back as

::: result current through r2
i_{r2} = 0.0621 - 0.0552\text{j}\,\mathrm{A}
:::

Write the second coil as `l2,0,2` instead — the same coil, the other way
round — and the answer is exactly its negative, `-0.0621 + 0.0552j`. Same
magnitude, opposite sign, no error message. Nothing will warn you.

So: read the schematic, decide which end of each coil carries the dot, and
name that node first in **both** coupled elements.

## t — the ideal transformer

```
t1,n1,n2,turns1,turns2
```

The two-node form names the top terminal of each side and grounds the other
two:

```field 9 Circuit Description
e,1,0,120
t1,1,2,10,1
rl,2,0,5
```

Ten to one, so 12 V across the load and

::: result current through rl
i_{rl} = \dfrac{12}{5}\,\mathrm{A}
:::

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
both bottoms on `0`.

A transformer reports **a current at each live terminal** rather than one
current, since the two sides carry different ones. The names are the
element's name followed by the node's: for `t1` with ports at nodes **1**
and **2**, they are `it11` and `it12`.

The same bracketed-pair form works on two-port blocks; see
{{ref:manual-twoports}}.
