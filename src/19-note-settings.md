---
id: settings
kind: note
title: Every control in the Settings card
versions: [9]
updated: 2026-09-11
summary: >
  Rounding, the four Display ticks and the AC power convention, each with what it changes, what it does not, and why two of them appear only in AC.
---

Nothing in {{card:Settings}} changes an answer. Every control there changes
how an answer is *written* — how many figures it carries, whether it wears a
unit, whether a complex number is shown as a phasor. The one exception is the
AC power convention at the foot of the card, which changes what the average
power in an AC circuit *means*, and is called out below.{{i:Settings card}}

The lessons reach for these controls as they need them. This note is the
whole card in one place, for when you want to know what a tick does without
hunting for the lesson that first used it.

## Rounding

A menu of four, most exact first, with a second box for **n** that appears
only when the choice needs one.{{i:Rounding setting}}

| Choice | What you get |
|---|---|
| *exact* | The symbolic answer, unrounded: a current comes back as 3/500 A |
| *exact and approx to n digits* | Both, side by side, for any answer that is a pure number |
| *approx to n digits* | The decimal alone, to **n** significant figures |
| *approx (full precision)* | The decimal alone, at full working precision |

**n** takes 2 to 12 and starts at 4. A symbolic answer has nothing to
approximate and is left exact under every choice, so *exact and approx*
shows one value for `x*vin/(r1 + x)` and two for `0.006`.

The rounding is done in decimal, not in binary, so the last digit is the one
you would write by hand.

## Display

Four ticks, and they are independent of each other except where noted.

**Show units in answers** — V, A, W, VA, Ω. On by default. Quantities with no
unit to show, such as a power factor or a gain, stay bare whatever this says.

**Use SI prefixes in answers** — 0.002 becomes 2 m, 1200 becomes 1.2 k. Off
by default. It applies to numeric answers only; a symbolic answer is left as
it is. {{ref:si-prefixes}} has the full table, and the same shorthand for
values you type. Either mu works for micro, whichever your keyboard gives
you.

::: note SI prefixes and *exact* cannot both apply
A prefixed value is a decimal, so ticking the prefixes moves **Rounding**
off *exact* by itself, and choosing *exact* again switches the prefixes off.
Whichever you touched last wins, the other visibly changes, and the card
says so on screen rather than leaving you to notice.
:::

**Show AC answers as polar phasors** — 3 + 4j becomes 5∠53.13°. Average
power stays real either way, being a real quantity. This tick appears only
in AC: in DC every answer is real, and in FD and TR the answers are
functions of *s* or *t*, with no angle to take.{{i:polar phasors}}

**Show equations** — adds an {{card:Equations}} card listing the system the
solver assembled. Off by default, because on anything larger than a teaching
circuit that system is a page of algebra. The card arrives open when it
appears.{{i:Equations card}}

## AC power convention

**RMS phasors.** Off means peak amplitude — the ÷2 convention. It affects AC
power only, so the row appears in AC and nowhere else.{{i:RMS}}

This is the one setting on the card that changes an answer rather than its
appearance. For the same phasor magnitudes, RMS reports twice what peak
does — a source of 10 V across a 5 Ω resistor gives 10 W with the tick off
and 20 W with it on — and the answer is labelled *average power* under the
peak convention and *power consumed* under RMS. Set it to match the book you
are working from before comparing numbers.

::: tip A hidden setting keeps its value
The two AC controls disappear outside AC rather than greying out, and
neither is cleared while it is hidden. Set a circuit up in AC with RMS
phasors on, run it in DC, come back to AC, and the tick is where you left
it — it travels with the entry when you save one, too.
:::
