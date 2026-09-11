---
id: manual-transients
kind: manual
book: manual
title: Capacitors, inductors and TR
versions: [9]
updated: 2026-09-11
summary: >
  Storage elements, initial conditions in the fifth field, transient analysis, switched circuits as two runs, and plotting an answer against time.
---

`c` and `l` take the same four fields as a resistor, plus an optional fifth
— the initial voltage on a capacitor, the initial current in an inductor.{{i:capacitor}}{{i:inductor}}

```
c1,2,0,10'u        no initial charge
c1,2,0,10'u,5      starting at 5 V
l1,2,0,2'm,0.3     starting at 300 mA
```

**The fifth field is read by TR and FD only.** DC and AC ignore it, which
is correct: in DC a capacitor is an open circuit and the initial condition
has nothing to say.{{i:initial conditions}}

## TR

Choose **TR** and the answers come back as functions of `t`.{{i:transient analysis (TR)}}

```field 9 Circuit Description
e,1,0,10
r,1,2,1'k
c,2,0,1'u
```

::: result voltage drop across c
v_{c} = 10 - 10\,e^{-1000\,t}
:::

The familiar step response, τ = RC = 1 ms, and derived rather than
recalled. Answers are valid for *t* ≥ 0.{{i:step response}}

Give the capacitor a starting voltage and only the coefficient changes:

```field 9 Circuit Description
e,1,0,10
r,1,2,1'k
c,2,0,1'u,4
```

::: result voltage drop across c
v_{c} = 10 - 6\,e^{-1000\,t}
:::

It starts at 4 and climbs to 10, so the swing is 6 rather than 10.

## No source at all

A natural response needs no source — the energy is already in the element:{{i:natural response}}

```field 9 Circuit Description
r,1,0,1'k
c,1,0,1'u,10
```

::: result voltage drop across c
v_{c} = 10\,e^{-1000\,t}
:::

Second-order circuits are no different: add an inductor and the answer
comes back over-, critically or under-damped as the values dictate. You do
not select the case; the algebra does.{{i:second-order circuits (damping)}}

## Switched circuits, in two runs

There is no switch element and no *t* < 0. A switched problem is two runs,
and this is the whole method:{{i:switched circuits (two runs)}}

1. **Run the *t* < 0 circuit in DC.** Read the capacitor voltages and
   inductor currents.
2. **Write the *t* > 0 circuit**, putting those numbers in the fifth field.
3. **Run it in TR.**

That is the same thing you would do by hand, and step 1 is where the
initial conditions come from rather than being assumed.

## Two things that make TR bearable

**Limit the results.** Every TR answer costs an inverse Laplace transform,
so a circuit with a dozen elements pays for dozens of them. Ask for the one
or two you want and the wait collapses. {{ref:limiting-results}} has it.{{i:limiting the results (TR)}}

**Plot it.** The Plot card takes *Plot a function of time (TR)*, an answer
name, and a time range. {{ref:manual-frequency}} covers all four plot
types.{{i:plots (Plotting Tools card)}}
