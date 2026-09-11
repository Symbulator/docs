---
id: manual-answers
kind: manual
book: manual
title: Running it, and reading the answer
versions: [9]
updated: 2026-09-11
summary: >
  One run returns every answer in the circuit. The names they come back under, what each one means, and the two spellings of any of them.
---

Paste the description, pick an analysis, press **Run**. There is nothing to
select first: a run returns *every* answer in the circuit, not the one you
asked about.{{i:Results card}}

```field 9 Circuit Description
e1,1,0,12
r1,1,2,1'k
r2,2,0,2'k
```

In DC that comes back as two node voltages and three answers per element:

::: result voltage at node 2
v_{2} = 8\,\mathrm{V}
:::
::: result current through r1
i_{r1} = \dfrac{1}{250}\,\mathrm{A}
:::
::: result power consumed by r1
p_{r1} = \dfrac{2}{125}\,\mathrm{W}
:::

Exact, because `12`, `1'k` and `2'k` are exact. 1/250 A is 4 mA; see
{{ref:settings}} for how to be shown the decimal instead.

## The answer names

A node's voltage is `v` and the node's name. An element's answers are a
letter and the element's name.{{i:answer names}}

| Name | Answer | Where |
|---|---|---|
| `v2` | voltage at node **2** | every node |
| `ir1` | current through **r1** | every element |
| `vr1` | voltage drop across **r1** | every element |
| `pr1` | power consumed by **r1** | every element |
| `apr1` | average power | AC |
| `sr1` | complex power | AC |
| `zr1` | impedance seen | AC, FD |
| `rr1` | resistance seen | DC |

*Resistance seen* and *impedance seen* are the element's own voltage over
its own current — useful on a source, where it is the resistance the source
is driving.{{i:resistance seen by a source}}

**Every name has two spellings.** `ir1` and `i_r1` are the same current,
`v2` and `v_2` the same voltage, and capitals make no difference. Use
whichever you like, anywhere a name is accepted. {{ref:underscores}} says
why both exist.{{i:case sensitivity}}

## Signs

Two sentences, and every sign in the book follows from them:{{i:sign conventions}}

- A **current** is positive flowing from the element's first node toward
  its second.
- A **voltage drop** is the first node's potential minus the second's.

So `e1,1,0,12` above reports `ie1 = -1/250 A`: current flows *out* of the
source's first node into the circuit, which is negative by that rule. A
source delivering power reports negative power consumed.{{i:power consumed and delivered}}

If a sign surprises you, read the element's node order before doubting the
answer.

## Asking about one thing

The whole answer set is the point, but three cards narrow it when you want
that:

- {{card:Evaluate}} takes an expression over the answers — `vr1/ir1`, or
  `pr1+pr2` — and can carry {{ui:Conditions}}.
- {{card:Solve}} solves equations written over the answers.
- In TR, the results can be limited before they are computed, which saves
  real time. {{ref:limiting-results}} has it.
