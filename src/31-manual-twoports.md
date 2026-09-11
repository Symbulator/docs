---
id: manual-twoports
kind: manual
book: manual
title: Two-ports
versions: [9]
updated: 2026-09-11
summary: >
  Six parameter sets out of any network, the same six letters as circuit elements, and the gain tool.
---

## Finding the parameters

*Find equivalent → Two-port parameters*, two nodes, and a kind:{{i:two-port parameters (z, y, h, g, a, b)}}

| | |
|---|---|
| **z** | impedance |
| **y** | admittance |
| **h** | hybrid |
| **g** | inverse hybrid |
| **a** | transmission |
| **b** | inverse transmission |

```field 9 Circuit Description
ra,1,2,10
rb,2,0,20
rc,2,3,30
```

A T network. Ports at **1** and **3**:

::: result open-circuit input impedance
z_{11} = 30\,\Omega
:::
::: result open-circuit reverse transfer impedance
z_{12} = 20\,\Omega
:::
::: result open-circuit forward transfer impedance
z_{21} = 20\,\Omega
:::
::: result open-circuit output impedance
z_{22} = 50\,\Omega
:::

10 + 20 and 30 + 20 on the diagonal, the shared 20 off it. `z12 = z21`
because the network is reciprocal — passive and source-free. A network with
a dependent source in it will not be, and that is a result rather than a
mistake.

Run it again with **y** and you get the inverse matrix, as you should.

## A two-port as an element

The same six letters are element types. Give the block its four parameters
in brackets and it behaves as that two-port:{{i:two-port}}

```field 9 Circuit Description
e,1,0,10
r1,1,a,50
z1,a,b,[100,10,20,50]
rl,b,0,1'k
```

The order is `[p11,p12,p21,p22]`. Leave the brackets off and the parameters
become symbols — `zp11`, `zp12` and so on — which is how you solve for the
block a circuit would need.

**A two-port reports a current at each port**, named for the element and
then the node — a block `z1` with ports at **a** and **b** reports `iz1a`
and `iz1b`. With four terminals named, it reports four.

### Four terminals

`z1,[tl,bl],[tr,br],[…]` when neither port sits on ground — the same form
as the transformer in {{ref:manual-coupling}}. A port whose far side floats
gets its own reference automatically, and Symbulator says so in the notes
rather than refusing.{{i:floating section (island)}}

## The gain mini-tool

{{tool:gain}} takes a two-port and a load and returns what a cascade
designer actually wants:{{i:gain mini-tool}}

| | |
|---|---|
| *G*<sub>v</sub> | voltage gain |
| *G*<sub>i</sub> | current gain |
| *G*<sub>p</sub> | power gain |
| *Z*<sub>in</sub> | input impedance |

It is a mini-tool, so it takes the four parameters and the load as values
you type rather than needing a circuit.

::: tip Interconnections are wiring, not formulas
Series, parallel and cascade combinations have no tool. Wire two blocks
together in one description and solve — the combination falls out, and you
never have to remember which interconnection adds which matrix.{{i:interconnected two-ports}}
:::
