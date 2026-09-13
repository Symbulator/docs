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
farads, not reactances — and the solver does the conversion.{{i:AC analysis}}{{i:angular frequency (ω)}}

A 10 V source driving a 50 Ω resistor and a 50 mH inductor in series, at
1000 rad/s. We name the three `e`, `r` and `l`, and write the inductor as
its inductance:

```field 9 Circuit Description
e,1,0,10
r,1,2,50
l,2,0,0.05
```

Set {{ui:Analysis}} to *AC — alternating current*, put **1000** in the
{{ui:ω — angular frequency}} box, and run. At that frequency the inductor
is 50 Ω of reactance, so the loop's impedance is 50 + 50j, and the answers
say so:

::: result current through r
i_{r} = 0.1 - 0.1\text{j}\,\mathrm{A}
:::
::: result voltage drop across l
v_{l} = 5.0 + 5.0\text{j}\,\mathrm{V}
:::

You may also give reactances directly, as ohms, if that is how the problem
is stated — a resistor-valued `l` is not a thing, so put the reactance in
as an impedance and leave ω out of it.{{i:impedance}}{{i:reactances given in ohms}}

**Rectangular or polar** is a display choice: tick {{ui:Show AC answers as
polar phasors}} in {{card:Settings}} and `0.1 - 0.1j` reads
`0.1414∠-45°`. Nothing about the answer changes. The {{tool:aa}} mini-tool
does the same conversion for one value you type.{{i:polar phasors}}{{i:aa mini-tool}}

## The four power answers

In AC an element reports more than in DC:

| | |
|---|---|
| `p` | average (real) power consumed, *P* = Re **S**, in watts — `ap` is the same answer under the calculator's name |
| `q` | reactive power consumed, *Q* = Im **S**, in var |
| `s` | complex power consumed, **S** = *P* + j*Q*, in VA |
| `z` | impedance seen |

The three are *P*, *Q* and **S** as every book writes them, whichever way
the RMS setting is: RMS changes their values, not their names. A source's
card shows the delivered forms, `-pe`, `-qe` and `-se`, and the power
factor of the power it delivers; the answers `pe`, `qe` and `se` are the
consumed values all the same.

The same shape with a 30 Ω resistor and a 40 mH inductor, at 1000 rad/s
again, so that the impedance is 30 + 40j, a 3-4-5 triangle:

```field 9 Circuit Description
e,1,0,10
r,1,2,30
l,2,0,0.04
```

Run in AC at ω = 1000, the source's card reads

::: result complex power delivered by e
-s_{e} = 0.6 + 0.8\text{j}\,\mathrm{VA}
:::

the negative of `se`, since a source's card shows what it delivers. So
*P* = 0.6 W, *Q* = 0.8 var, |*S*| = 1.0 VA, and the card's last row gives
the power factor of that delivered power, 0.6 lagging.{{i:complex power}}
The card's next two rows are those two parts, `-pe` = 0.6 W and `-qe` =
0.8 var, and `abs(se)` in {{card:Evaluate}} is the apparent
power.{{i:reactive power}}

**An inductor or a capacitor reports only its complex power.** That is
not an omission: a pure reactance consumes no average power, and a zero
printed every time would be noise; its reactive power is `im(sl)` in
{{card:Evaluate}}.{{i:average power}}

The {{tool:pf}} mini-tool takes one value, and which of two things it is
decides what comes back.{{i:power factor}}{{i:pf mini-tool}} Given a complex
power such as `se` — or any complex value, an impedance, an expression with
symbols in it — it returns the power factor of that value as given,
|*P*|/|*S*|, with the word the value carries when it is a number and
symbolic when it is not. Given the **name** of an element of the AC solve, `e` or `r1`,
it returns the power factor with its lead/lag sense, and it works only when
that element's voltage and current came out as numbers.

**The two forms read different powers, and that is what makes the word
right.** A variable such as `se`, `sj` or `sr1` is read as it stands: the
complex power *consumed*, which is what every element stores, source or
load — and its word is that power's own, so `se` at a source says the
opposite word to `e`, the consumed power being the opposite of the
delivered one. A name is read by the element's kind, as the
calculator read it: an impedance (`r`, `l`, `c`) on the power it
*consumes*, so an inductive load reads lagging; a source (`e`, `j`) on the
power it *delivers*, the current negated first, so a source reads the
circuit it sees, and a source feeding an inductive load says lagging like
the load. The value is the same either way; only the word depends on it,
and a source read on `se` says the opposite word. Under a name's reading
the tool says which power in words — *the power delivered by source e*,
*the power consumed by impedance r1*; under a value's it says nothing, the
value being what you gave it.

::: warning RMS is the one setting that changes an answer
**RMS phasors**, in {{card:Settings}}, is not a display choice. Off means
peak amplitude, the ÷2 convention. For the same phasor magnitudes, RMS
reports twice the power that peak does — a 10 V source across 5 Ω gives
10 W with the tick off and 20 W with it on. With the tick on every
current and voltage label on the cards reads *effective*, since the
magnitudes are then RMS values, the textbook's effective values. Match
the book you are working from before comparing numbers.{{i:RMS}}
:::

## Three-phase

There is no three-phase mode, and none is needed. A three-phase circuit is
an AC circuit with three sources whose values carry the phase — `120`,
`120*exp(-2j*pi/3)`, `120*exp(2j*pi/3)` — and Y or Δ is just how you wire
the nodes. Balanced and unbalanced are the same description with different
values.{{i:three-phase circuits}}

Line and phase quantities are then read off the elements directly: there is
no separate answer for them, because each is some element's own current or
voltage.
