---
id: lesson-threephase
kind: lesson
title: Three-phase circuits
updated: 2023-07-08
summary: >
  Learn to solve simple *three-phase* circuits in Y-Y, Y-Δ, Δ-Δ and Δ-Y
  configurations, both balanced and unbalanced, to find line and phase
  currents, voltages and complex power.
---

In this lesson you will learn to use Symbulator to solve simple **three-phase**
systems, in their four basic configurations of wye-wye, wye-delta, delta-delta
and delta-wye. We will see both balanced and unbalanced examples, where you are
asked to find currents, voltages and complex power in the source, line and
load.

## About solving three-phase circuits {#about-threephase}

Three-phase circuits can be tricky to solve in Symbulator, for several
reasons.{{i:three-phase circuits}} For example, it is not always clear which
node should be used as ground node. There are three times as many nodes as
there would be for an equivalent single-phase circuit. And, in the case of
sources in a delta array, there are some mathematical issues, where we have
more unknowns than equations.

Symbulator does a great job of solving the simple three-phase circuits you may
encounter in a basic Circuits I / II textbook. Here we will see some examples,
and one or two tricks, to solve them. Having said that, Symbulator would not be
my tool of choice for solving anything larger than such basic circuits. As
circuits grow larger, the number of nodes quickly grows beyond what the
{{t:machine}} can solve.

## Wye-Wye {#wye-wye}

### Balanced wye-wye system

::: problem AS7's Examples 12.2 & 12.6
Calculate the line currents in the three-wire Y-Y system. Determine the total
average power, reactive power, and complex power absorbed at the source and at
the load. Assume that the values given for the source are RMS.

::: figure assets/circuit/as7e1202.png
AS7's Examples 12.2 and 12.6
:::

::: answer
Although not specified in the textbook, to get the answers they give we need to
assume the values are RMS. One must describe the circuit carefully in the case
of three-phase circuits, because it is very easy to make a mistake. Below is
how I describe this one:

```sym 7
true→s\rms
"ea0,ag,0,(110.∠0°):eb0,bg,0,(110.∠-120°):ec0,cg,0,(110.∠120°):rat,ag,ad,5.–𝐢2.:rbt,bg,bd,5.–𝐢2.:rct,cg,cd,5.–𝐢2.:ra0,ad,0,10.+8.𝐢:rc0,cd,0,10.+8.𝐢:rb0,bd,0,10.+8.𝐢"→cir
s\ac(cir,ω)
```
```sym 8
true→userms
"ea0,ag,0,(110.∠0°):eb0,bg,0,(110.∠–120°):ec0,cg,0,(110.∠120°):rat,ag,ad,5.–𝐢2.:rbt,bg,bd,5.–𝐢2.:rct,cg,cd,5.–𝐢2.:ra0,ad,0,10.+8.𝐢:rc0,cd,0,10.+8.𝐢:rb0,bd,0,10.+8.𝐢"→cir
s\ac(cir,ω)
```

Some observations about my description:

- Notice that I have specified the node at the centre of both Y's as node 0.
  This is something you can do only in the case of balanced Y-Y systems, not
  for other configurations and not for unbalanced systems.
- Since the calculator does not differentiate between lower and upper case
  variables, nodes called a and A would be considered the same node. Instead,
  we use the names ag and ad, where the g reminds us a node is on the
  generation side and the d reminds us it is on the demand side.

Once the simulation is completed, we ask for the currents on the transmission
lines and get:

```out
{"6.809ᴇ0∠-21.8°","6.809ᴇ0∠-141.8°","6.809ᴇ0∠98.2°"}
```

The complex power at the source is `sea0+seb0+sec0`, which gives
−2086.2 − 834.5𝐢 VA. The real part is the average power absorbed by the source;
since it is negative, the source is delivering an average power of 2086 W. The
imaginary part is the reactive power: 834 VAR.

The complex power at the load is `sra0+srb0+src0`, which gives
1390.8 + 1112.6𝐢 VA. The load is consuming an average power of 1391 W and a
reactive power of 1113 VAR.

Before we move on, I want you to try simulating this circuit using a different
node as the centre of the Y array of the load — call it d0, to remind you it is
the centre for the demand side. If you evaluate the voltage in that node, you
will see it is 0 V, because the system is balanced. That's why we were able to
use 0 for both. When we solve an unbalanced system, we cannot.
:::
:::

::: practice Further wye-wye problems
TODO: convert AS7's Practice Problem 12.2 & 12.6, Example 12.10 (unbalanced)
and Example 12.9 (unbalanced with a neutral line) from docs-page7.
:::

## Wye-Delta {#wye-delta}

TODO: convert this section from docs-page7, starting at AS7's Example 12.3.

## Delta-Delta {#delta-delta}

TODO: convert this section from docs-page7.

## Delta-Wye {#delta-wye}

TODO: convert this section from docs-page7.
