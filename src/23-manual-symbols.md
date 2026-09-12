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
answer is an expression rather than a number.{{i:symbolic circuit}}

A divider with no values at all: a source and two resistors in series,
every value left as a symbol. We name the symbols `vs`, `ra` and `rb`, and
the elements `e`, `r1` and `r2`:

```field 9 Circuit Description
e,1,0,vs
r1,1,2,ra
r2,2,0,rb
```

Run in DC, the voltage across the second resistor comes back as

::: result voltage drop across r2
v_{r2} = \dfrac{rb\,vs}{ra + rb}
:::

The divider rule, derived rather than recalled. No values were given and
none were needed.

## Define

{{card:Define}} gives values to symbols without editing the description.
One per line, `name = value`:{{i:Define card}}

```field 9 Define
ra = 4'k
rb = 6'k
vs = 10
```

Run the same circuit again and the same answer now reads

::: result voltage drop across r2
v_{r2} = 6\,\mathrm{V}
:::

The description still says `ra`, so changing a value is one line and a
re-run, not an edit to the circuit.

A symbol left undefined stays symbolic. You can define some and not others,
and get a partly symbolic answer — which is usually what you want when one
component is the unknown.

## Evaluate

{{card:Evaluate}} takes expressions over the answers, one per line, after
the solve:{{i:Evaluate card}}

```field 9 Evaluate
vr1/ir1
pr1 + pr2
```

{{ui:Conditions}} constrain the evaluation without changing the circuit —
`ra = rb`, say, to see what the divider does when the two are equal.{{i:Conditions (Evaluate)}}

## Solve

{{card:Solve}} goes the other way. Give it an equation over the answers and
an unknown, and it finds the value that satisfies it.{{i:Solve card}}

Suppose we want the resistor that puts 7 V across **r2**. We take `rb` out
of {{card:Define}}, so that it stays a symbol and the answers come back in
terms of it, leave `ra` and `vs` defined, and run again. Then, in the
{{card:Solve}} card, the equation and the unknown:

```field 9 Equation(s) to solve in terms of the results
vr2 = 7
```

```field 9 Unknown(s) to solve for
rb
```

Press {{btn:Solve equations}}, and the card returns `rb` = {{o:9333.33}} Ω:
the resistance that puts 7 V across **r2** when `ra` is 4 kΩ and `vs` is
10 V. A value the equation needs but the circuit does not know can also be
given in the card's {{ui:Conditions}} box, `ra = 4'k` on a line of its own,
instead of in Define.

::: warning More than one answer is normal
An equation on a power or on a product of answers is quadratic in its
unknown, so it can have two roots, and both may be physical. Symbulator
returns every root and offers a picker under the outputs. It does not
choose for you, and the first one shown is not more correct than the
second — read the picker before quoting an answer.{{i:multiple solutions}}
:::

**Real solutions only** is a tick on the same card. Leave it on unless a
complex root is meaningful in your problem.{{i:real solutions only}}

## Expert Mode

Expert Mode adds to the system the solver assembles, rather than working on
its answers afterwards. Three boxes:{{i:Expert Mode}}

- **equations** — extra relations, one per line or separated by `and`
- **unknowns** — extra symbols to solve for
- **conditions** — constraints applied to the result

Use it when the condition has to be part of the solve itself, so that
*every* answer comes back with it applied: the whole circuit at the
component value that meets the condition, not the component alone. Put the
condition in *equations* and the component in *unknowns*, and the circuit
is solved and the condition satisfied in one system. For the component's
value on its own, the {{card:Solve}} card above is the shorter route, and
it is the one this documentation's worked examples take.

Values in these boxes are parsed exactly as circuit values are, so `4.7'k`
works and a bare `4.7k` does not.

::: tip See what was assembled
Tick {{ui:Show equations}} in {{card:Settings}} and an {{card:Equations}}
card appears with the system the solver actually built — the fastest way to
find out why an Expert Mode run did not do what you expected.{{i:Equations card}}
:::
