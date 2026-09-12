---
id: manual-grammar
kind: manual
book: manual
title: The circuit description
versions: [9]
updated: 2026-09-11
summary: >
  All fifteen element letters with their fields, the naming rules, node 0, brackets, and the SI prefix shorthand. The densest page here, and the one to come back to.
---

A circuit description is one element per line. The first character of the
name picks the type; the fields that follow are positional and
comma-separated.{{i:circuit description}}

Take the simplest circuit worth describing: a 12 V source driving a 1 kΩ
and a 2 kΩ resistor in series. We name the source `e1` and the resistors
`r1` and `r2`, take the source's lower end as node `0`, call its upper end
node **1** and the junction of the two resistors node **2**, and write
each element between the two nodes it joins:

```field 9 Circuit Description
e1,1,0,12
r1,1,2,1'k
r2,2,0,2'k
```

**Node `0` is ground**, always, and every circuit needs one; the other
node names are ours to choose.{{i:ground node}}{{i:reference node}}

## The fifteen letters

`name` is always the first field. Everything else is positional.{{i:element types}}

| | Element | Fields after the name |
|---|---|---|
| **r** | resistor | `n1,n2,value` |
| **l** | inductor | `n1,n2,value` *,initial current* |
| **c** | capacitor | `n1,n2,value` *,initial voltage* |
| **e** | voltage source | `n1,n2,value` |
| **j** | current source | `n1,n2,value` |
| **o** | ideal op amp | `n+,n−,nout` |
| **m** | mutual inductance | `Lname1,Lname2,M` |
| **s** | short circuit | `n1,n2` |
| **t** | ideal transformer | `n1,n2,turns1,turns2` |
| **z y h g a b** | two-port block | `n1,n2` *,[p11,p12,p21,p22]* |

Italic fields are optional. The initial conditions on **l** and **c** are
read by FD and TR and ignored by DC and AC.

Note what **m** takes: the *names of two inductors*, not nodes. Node order
on those inductors is the dot convention — the first node you name in each
coupled element is its dotted end. Get it backwards and every current comes
back wrong, looking right.{{i:dot convention}}

An **m** has no answers of its own. It is a statement about two other
elements, and its effect shows up in their currents.

::: tip Sign and direction, once
A current is positive flowing from the first node toward the second. A
voltage drop is the first node's potential minus the second's. Every answer
in the book follows from those two sentences; if a sign surprises you, read
the element's node order.
:::

## Names

Letters, digits and underscores. The first character sets the type, so
`rload` is a resistor and `r_b` is a resistor.{{i:names of elements and nodes}}

A name must be identifier-safe. `r-x` looks reasonable and is refused,
because `2*i_r-x` would silently read as `2*i_r` minus `x`.

Node names are yours: `1`, `2`, `in`, `out`, `b`, `e`, `c`. Only `0` is
reserved.

## Values

A value is a number, a symbol, or an expression in either. Here is the
divider again with its source left as a symbol we call `vs`, and beside it
a second source, `e2`, driving a 2 kΩ resistor, whose value is five times
the voltage at the divider's midpoint:

```field 9 Circuit Description
e1,1,0,vs
r1,1,2,1'k
r2,2,0,1'k
e2,3,0,5*v2
r3,3,0,2'k
```

Because `vs` is a symbol, every answer comes back in terms of it. `e2` is a
**dependent source**: its value names `v2`, the voltage at node 2, so it is
five times whatever the rest of the circuit puts there. Any answer name may
appear in any value. That is how all four dependent-source types are
written, and why there is no separate letter for them.

An underscore in a symbol makes a subscript in the typeset answer, and
nothing else. {{ref:underscores}} has it.{{i:underscore}}

### SI prefixes

An apostrophe and a letter multiply the value, exactly:

`4.7'k` · `10'u` · `560'm` · `1'M`

Eleven prefixes, peta down to atto; the full table is in
{{ref:si-prefixes}}. Two things to know here: **case matters** — `'m` is
milli and `'M` is mega — and **a prefixed value is exact**, as is a plain
integer. `8000` and `8'k` are exact; `8000.` and `8E3` are approximate, and
that difference shows up the moment an answer is symbolic.{{i:SI prefixes}}{{i:exact and approximate values}}

## Brackets

Brackets mean exactly three things.{{i:brackets}}

**A parallel group, in a resistor's value only.** `[r1,r2,r3]` is those three
in parallel. Three resistors of 1 kΩ, 2 kΩ and 2 kΩ side by side between
node 1 and ground, written as one element we call `rp`:

```field 9 Circuit Description
rp,1,0,[1'k,2'k,2'k]
```

**A pair of terminals**, for a transformer or a two-port, when neither side
sits on ground. `[top,bottom]`. Here a two-port block, `z1`, sits between a
source and a load with neither of its ports touching ground; we call its
four terminals **a**, **b**, **c** and **d**, top before bottom on each
side:

```field 9 Circuit Description
e,1,0,10
r1,1,a,50
r2,b,0,50
z1,[a,b],[c,d],[100,10,20,50]
rl,c,d,1'k
```

The two-node form `z1,1,2` is the same element with both bottoms on `0`,
and a four-terminal block reports a current at each of its four terminals
rather than two.

**A parameter set**, the four numbers of a two-port, or a transformer's two
turns counts.

Anywhere else, a bracket is an error rather than a guess.

## Separators

A line each is the readable form. A colon does the same job on one line —
`e,1,0,12:r1,1,2,1'k` — and both are accepted everywhere, including in a
saved file.{{i:separators (newline or colon)}}
