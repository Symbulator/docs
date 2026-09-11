---
id: manual-symbols
kind: manual
book: manual
title: Symbols, Define and Expert Mode
versions: [9]
updated: 2026-09-11
summary: >
  Any value may be a symbol, and the answer comes back in terms of it. Define supplies values; Expert Mode adds equations, unknowns and conditions to the system.
---

This is the part that is not SPICE. Any value may be a symbol, and the
answer is an expression rather than a number.

```field 9 Circuit Description
e,1,0,vs
r1,1,2,ra
r2,2,0,rb
```

::: result voltage drop across r2
v_{r2} = \dfrac{rb\,vs}{ra + rb}
:::

The divider rule, derived rather than recalled. No values were given and
none were needed.

## Define

{{card:Define}} gives values to symbols without editing the description.
One per line, `name = value`:

```field 9 Define
ra = 4'k
rb = 6'k
vs = 10
```

Same circuit, and `v_{r2}` now reads 6 V. The description still says `ra`,
so changing the value is one line and re-running, not an edit to the
circuit.

A symbol left undefined stays symbolic. You can define some and not others,
and get a partly symbolic answer — which is usually what you want when one
component is the unknown.

## Evaluate

{{card:Evaluate}} takes expressions over the answers, one per line, after
the solve:

```field 9 Evaluate
vr1/ir1
pr1 + pr2
```

{{ui:Conditions}} constrain the evaluation without changing the circuit —
`ra = rb`, say, to see what the divider does when the two are equal.

## Solve

{{card:Solve}} goes the other way. Give it an equation over the answers and
an unknown, and it finds the value that satisfies it.

```field 9 Solve
vr2 = 7
```

with `rb` as the unknown. The answer is the resistance that puts 7 V across
**r2**.

::: warning More than one answer is normal
An equation on a power or on a product of answers is quadratic in its
unknown, so it can have two roots, and both may be physical. Symbulator
returns every root and offers a picker under the outputs. It does not
choose for you, and the first one shown is not more correct than the
second — read the picker before quoting an answer.
:::

**Real solutions only** is a tick on the same card. Leave it on unless a
complex root is meaningful in your problem.

## Expert Mode

Expert Mode adds to the system the solver assembles, rather than working on
its answers afterwards. Three boxes:

- **equations** — extra relations, one per line or separated by `and`
- **unknowns** — extra symbols to solve for
- **conditions** — constraints applied to the result

Use it when the thing you want is not an answer the circuit produces. The
classic case is a component value the circuit must have for some condition
to hold: put the condition in *equations*, the component in *unknowns*, and
the circuit is solved and the condition satisfied in one system rather than
two passes.

Values in these boxes are parsed exactly as circuit values are, so `4.7'k`
works and a bare `4.7k` does not.

::: tip See what was assembled
Tick {{ui:Show equations}} in {{card:Settings}} and an {{card:Equations}}
card appears with the system the solver actually built — the fastest way to
find out why an Expert Mode run did not do what you expected.
:::
