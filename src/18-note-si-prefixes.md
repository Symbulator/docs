---
id: si-prefixes
kind: note
title: The SI prefixes Symbulator accepts
versions: [9]
updated: 2026-09-11
summary: >
  Every prefix Symbulator takes, from peta down to atto, with its shorthand and its factor — and the two places where case matters.
---

An SI prefix in an element's value, preceded by an apostrophe, multiplies
that value by the corresponding factor, exactly. `8'k` is 8000, and it is
8000 exactly, not 8000 to some number of figures.

Eleven prefixes are accepted:

| Prefix | Shorthand | Factor |
|---|---|---|
| peta | `'P` | 10{{sup:15}} |
| tera | `'T` | 10{{sup:12}} |
| giga | `'G` | 10{{sup:9}} |
| mega | `'M` | 10{{sup:6}} |
| kilo | `'k` or `'K` | 10{{sup:3}} |
| milli | `'m` | 10{{sup:-3}} |
| micro | `'u` or `'µ` | 10{{sup:-6}} |
| nano | `'n` | 10{{sup:-9}} |
| pico | `'p` | 10{{sup:-12}} |
| femto | `'f` | 10{{sup:-15}} |
| atto | `'a` | 10{{sup:-18}} |

They work in the value of every element, not only resistors.

::: warning Case matters
Kilo is the one prefix you may write either way, `'k` or `'K`. Every other
prefix is case-sensitive, and two of them are a factor of 10{{sup:9}} apart:
`'m` is milli and `'M` is mega. Micro is the other one with a choice: `'u`, or
either of the two mu characters a keyboard may give you, which look alike
and mean the same thing here. All of them are lower case.
:::

## Exact, and why that matters

A prefixed value is exact, and so is a plain integer. A decimal point or an
exponent makes a value approximate instead. So an 8 kΩ resistor can be
written four ways that are not quite the same thing:

- `8000` — exact
- `8'k` — exact
- `8000.` — approximate
- `8E3` — approximate

The difference does not show until an answer is symbolic or a division does
not come out even. `8000` and `8'k` let Symbulator keep a current as 3/500 A;
`8000.` and `8E3` make it 0.006 A from the start.

## Prefixes in the answers, not just the values

The table above is about what you *type*. Symbulator will also write its
answers with prefixes: tick {{ui:Use SI prefixes in answers}} in
{{card:Settings}}, and a current of 3/500 A reads 6 mA instead.

Ticking it moves {{ui:Rounding}} off *exact* by itself, since a prefixed
value is a decimal, and choosing *exact* again switches the prefixes off.
Symbulator says so on screen when it does.
