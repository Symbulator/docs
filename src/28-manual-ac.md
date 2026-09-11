---
id: manual-ac
kind: manual
book: manual
title: AC, phasors and power
versions: [9]
updated: 2026-09-11
summary: >
  Sinusoidal steady state at one ω, rectangular or polar, and the four power answers — including the one setting that changes an answer rather than its appearance.
---

Choose **AC** and give an **ω**. Elements keep their own units — henries and
farads, not reactances — and the solver does the conversion.

```field 9 Circuit Description
e,1,0,10
r,1,2,50
l,2,0,0.05
```

At ω = 1000 rad/s the inductor is 50 Ω of reactance, so the impedance is
50 + 50j:

::: result current through r
i_{r} = 0.1 - 0.1\text{j}\,\mathrm{A}
:::
::: result voltage drop across l
v_{l} = 5.0 + 5.0\text{j}\,\mathrm{V}
:::

You may also give reactances directly, as ohms, if that is how the problem
is stated — a resistor-valued `l` is not a thing, so put the reactance in
as an impedance and leave ω out of it.

**Rectangular or polar** is a display choice: tick {{ui:Show AC answers as
polar phasors}} in {{card:Settings}} and `0.1 - 0.1j` reads
`0.1414∠-45°`. Nothing about the answer changes. The {{tool:aa}} mini-tool
does the same conversion for one value you type.

## The four power answers

In AC an element reports more than in DC:

| | |
|---|---|
| `ap` | average power, in watts — the real power |
| `s` | complex power, **S** = *P* + j*Q*, in VA |
| `p` | the power answer, labelled by the convention in force |
| `z` | impedance seen |

```field 9 Circuit Description
e,1,0,10
r,1,2,30
l,2,0,0.04
```

At ω = 1000 that is 30 + 40j — a 3-4-5 triangle — and the source reports
complex power −0.6 − 0.8j VA. So *P* = 0.6 W, *Q* = 0.8 var, |*S*| = 1.0 VA
and the power factor is 0.6, lagging.

**An inductor reports no average power**, only complex. That is not an
omission: a pure reactance consumes none, and a zero printed every time
would be noise.

The {{tool:pf}} mini-tool takes a complex power or an impedance and returns
the power factor with its lead/lag sense.

::: warning RMS is the one setting that changes an answer
**RMS phasors**, in {{card:Settings}}, is not a display choice. Off means
peak amplitude, the ÷2 convention. For the same phasor magnitudes, RMS
reports twice the power that peak does — a 10 V source across 5 Ω gives
10 W with the tick off and 20 W with it on, and the answer's label changes
with it. Match the book you are working from before comparing numbers.
:::

## Three-phase

There is no three-phase mode, and none is needed. A three-phase circuit is
an AC circuit with three sources whose values carry the phase — `120`,
`120*exp(-2j*pi/3)`, `120*exp(2j*pi/3)` — and Y or Δ is just how you wire
the nodes. Balanced and unbalanced are the same description with different
values.

Line and phase quantities are then read off the elements directly: there is
no separate answer for them, because each is some element's own current or
voltage.
