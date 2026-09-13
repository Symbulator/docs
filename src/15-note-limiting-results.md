---
id: limiting-results
kind: note
title: Limiting the results to save time
versions: [9]
updated: 2026-09-11
summary: >
  A transient run returns every voltage, current and power in the circuit, and each one costs an inverse Laplace transform. Ask for only the answers you want and the wait gets shorter.
---

Unless you say otherwise, Symbulator gives you the whole set of answers:
the voltage at every node, and the voltage drop, current and power in
every element. That is usually what you want, and for a direct current
or an alternating current analysis it costs almost nothing.

**Transient analysis is the exception.** Each TR answer is found by
inverting a Laplace transform, and that is the slow step. A circuit with
a dozen elements has several dozen answers, and you are very often after
one of them.{{i:limiting the results (TR)}}

## Asking for a few answers

Choose **tr** in the analysis menu, and a question appears in
{{card:Settings}}:

> **Do you want to limit the results to save time?**

Tick it, and a field opens. List the answers you want, separated by
commas:

```field 9 What results are you after? List the variables here
v2
```

Every answer name Symbulator knows is allowed here — `v2` for the voltage
at node **2**, `ir1` for the current through **r1**, `pr3` for the power
in **r3**.

Ask for one answer instead of a dozen and you skip a dozen inverse
transforms. On a small circuit the difference is not worth the tick; on
a large one, or a symbolic one, it is the easiest speed-up there is.

::: tip It changes what is computed, not what is correct
Limiting the results does not approximate anything. The answers you ask
for are the same answers you would have got without the tick — there are
simply fewer of them.
:::

## When not to bother

If you are exploring, leave it alone. The whole answer set is the point
of Symbulator: you run a circuit and read what happened everywhere in
it, which is exactly what you cannot do on paper. Reach for this when a
particular run is slow enough to interrupt you, and not before.
