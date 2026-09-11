---
id: manual-toolbox
kind: manual
book: manual
title: The rest of the toolbox
versions: [9]
updated: 2026-09-11
summary: >
  By-Hand Equations, the Numerical Solver, the SPICE Translator, the schematic, and the solver as a Python package.
---

Five things the app does that are not a circuit solve. Four of them are
documented nowhere else.

## By-Hand Equations

Tick it and a card appears with the system a first course would have you
write: **nodal**, with supernodes, or **mesh**, with supermeshes. It names
the method it used and counts the supernodes or supermeshes it needed.{{i:By-Hand Equations card}}{{i:nodal and mesh analysis}}{{i:supernodes and supermeshes}}

It is written independently of the classic solve and then compared with it.
The classic solve stays the authority and is never fed by the by-hand one —
the point is that two different derivations agree, which is worth something
when you are checking your own work against the machine's.

Use it to find where your hand derivation went wrong, not to avoid doing
one.

## The Numerical Solver

A property of its own, at `/eqsheet/`, reached from the app's **Explore
Numerically** card. It is a TK!Solver-style equation sheet rather than a
circuit solver: a list of equations, each variable marked **Known** or
**Unknown**, and a numerical solve over the lot.{{i:Numerical Solver}}

Two ways in:

- **From a solve.** The card hands over the system and the results from a
  DC or numeric-ω AC run, already loaded.
- **Empty.** Open it with nothing and type your own equations. It does not
  need a circuit.

Every unknown carries a **Restriction** — *Unrestricted*, *Positive*,
*Negative*, or *Range* with a from/to pair. This is not cosmetic: a
restricted solve runs a bounded least-squares rather than the unrestricted
root finder, and a system whose root lies outside its restriction says so
instead of handing back a boundary value that looks like an answer.

Any identifier works as a variable name, Python keywords included — `is`,
the natural name for a source current, is accepted.

It needs SciPy, which the offline builds bundle.

## The SPICE Translator

Both directions, in a card of its own.{{i:SPICE Translator}}

**Symbulator to SPICE** returns a netlist with a title line and `.end`,
ready to paste into ngspice or LTspice. Anything it cannot translate comes
out as a `*` comment and is reported — it never quietly drops an element.
Dependent sources translate whenever their value is affine in node voltages.

**SPICE to Symbulator** takes the linear subset of a netlist. Elements and
directives outside that subset are dropped and reported, never guessed at.

It is a prototype, and says so on the card. Read the warnings both ways.

## The schematic

Symbulator draws the circuit you described, from the description alone. It
is worth a glance before trusting any answer: the fastest way to catch a
node typed wrong is to see the picture disagree with the circuit in your
head.{{i:schematic}}

It is a drawing of what you *wrote*, not of what you meant — which is
exactly what makes it useful.

## The package

The solver is on PyPI and does not need the app:{{i:Python package (pip install symbulator)}}

```
pip install symbulator
```

```
from symbulator import dc
r = dc("e,1,0,10:r1,1,2,1'k:r2,2,0,2'k")
r.v2
```

Every answer is a SymPy expression, so it substitutes, differentiates and
lambdifies like any other. In a notebook there are `%%dc`, `%%ac`, `%%fd`
and `%%tr` cell magics that take a circuit written one element per line,
the way the app's input card does.

::: warning `t` is nonnegative
The symbol `t` is declared nonnegative, because a transient answer is only
valid for *t* ≥ 0. That surprises the first person who tries to take a
limit through zero. `from symbulator import t, s` gets you the same symbols
the answers use.
:::
