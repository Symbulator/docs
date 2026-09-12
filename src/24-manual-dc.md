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
therefore pushes current into node 1.{{i:current source}}

A 3 mA source feeding two resistors in parallel, one of them given not as
a resistance but as a conductance $g$. We write the source with its arrow
pointing into node 1, `j,0,1`, name the resistors `r1` and `r2`, and give
the first the value `1/g`, since there is no conductance element and a
conductance is a resistance written as its reciprocal:

```field 9 Circuit Description
j,0,1,3'm
r1,1,0,1/g
r2,1,0,2'k
```

Run in DC, the voltage across the pair comes back in terms of that
conductance:

::: result voltage drop across r1
v_{r1} = \dfrac{6}{2000 g + 1}
:::

The algebra took care of the reciprocal itself.{{i:conductance}}

## Dependent sources

There is no letter for them. An `e` or a `j` whose value names an answer is
dependent, and that covers all four textbook types:{{i:dependent source}}

| | Value looks like |
|---|---|
| VCVS | `e2,3,0,5*v2` |
| VCCS | `j2,3,0,g*v2` |
| CCVS | `e2,3,0,r*ir1` |
| CCCS | `j2,3,0,beta*irb` |

The controlling quantity is just an answer name, so it may be any answer in
the circuit, and it may appear inside a larger expression.

## The parallel shorthand

In a **resistor's value only**, a bracketed list is that group in parallel.{{i:parallel resistors}}
A 9 V source across three resistors of 1 kΩ, 2 kΩ and 2 kΩ side by side,
the three written as one element we call `rp`:

```field 9 Circuit Description
e,1,0,9
rp,1,0,[1'k,2'k,2'k]
```

Run in DC, the current through the group is

::: result current through rp
i_{rp} = \dfrac{9}{500}\,\mathrm{A}
:::

which is 18 mA: 1 kΩ ‖ 2 kΩ ‖ 2 kΩ is 500 Ω. The entries may be symbols,
and the list may be any length.

It saves describing three elements and three nodes when the group is not
the thing you are studying. When it *is* the thing you are studying,
describe them separately so each reports its own current.

::: warning Brackets are not general
`[…]` means a parallel group here, a terminal pair on a transformer or
two-port, and a parameter set. Anywhere else it is an error rather than a
guess — see {{ref:manual-grammar}}.
:::
