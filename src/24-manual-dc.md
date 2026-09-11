---
id: manual-dc
kind: manual
book: manual
title: Sources, conductances and shorthands
versions: [9]
updated: 2026-09-11
summary: >
  Current sources, dependent sources of all four kinds, conductance as a value, and the parallel-resistor shorthand.
---

## Current sources

`j` takes the same four fields as `e`, and its current flows **from the
first node to the second, inside the element**. A source written `j,0,1`
therefore pushes current into node 1.

```field 9 Circuit Description
j,0,1,3'm
r1,1,0,1/g
r2,1,0,2'k
```

::: result voltage drop across r1
v_{r1} = \dfrac{6}{2000 g + 1}
:::

Two things are happening in three lines. The source drives 3 mA into node
1; and **r1**'s value is `1/g`, so the answer comes back in terms of a
conductance. There is no conductance element — a conductance is a
resistance written as its reciprocal, and the algebra takes care of itself.

## Dependent sources

There is no letter for them. An `e` or a `j` whose value names an answer is
dependent, and that covers all four textbook types:

| | Value looks like |
|---|---|
| VCVS | `e2,3,0,5*v2` |
| VCCS | `j2,3,0,g*v2` |
| CCVS | `e2,3,0,r*ir1` |
| CCCS | `j2,3,0,beta*irb` |

The controlling quantity is just an answer name, so it may be any answer in
the circuit, and it may appear inside a larger expression.

## The parallel shorthand

In a **resistor's value only**, a bracketed list is that group in parallel:

```field 9 Circuit Description
e,1,0,9
rp,1,0,[1'k,2'k,2'k]
```

::: result current through rp
i_{rp} = \dfrac{9}{500}\,\mathrm{A}
:::

1 kΩ ‖ 2 kΩ ‖ 2 kΩ is 500 Ω, so 18 mA. The entries may be symbols, and the
list may be any length.

It saves describing three elements and three nodes when the group is not
the thing you are studying. When it *is* the thing you are studying,
describe them separately so each reports its own current.

::: warning Brackets are not general
`[…]` means a parallel group here, a terminal pair on a transformer or
two-port, and a parameter set. Anywhere else it is an error rather than a
guess — see {{ref:manual-grammar}}.
:::
