---
id: lesson-fd
kind: lesson
title: The complex frequency domain
updated: 2023-07-08
summary: >
  Learn to solve *complex-frequency domain* problems using **fd**. Move between
  the time domain and the s-domain with the **t2s** and **s2t** shortcuts. Learn
  to solve transfer function problems.
---

Every analysis so far has answered in the same domain you asked in. This one
does not, and that is the point of it: the complex frequency domain, or
s-domain, is where a differential equation becomes an algebraic one. Symbulator
will do the algebra; your job is to be clear about which domain each number is
in.{{i:frequency domain}}

## s-domain analysis {#s-domain}

{{v7,8|Symbulator has a tool called **fd**}}{{v9|Symbulator has an analysis
type called *FD — complex frequency domain*}} that solves a circuit in the
domain of complex frequency, where $s = j\omega$.

The rule that matters is this one, and it catches everybody once:

::: warning FD is in s. TR is in time.
The value of a source given to **FD** is read as an s-domain expression. The
same value given to **TR** is read as a function of time.

A source value of `1` in FD is not the same thing as a source value of `1` in
TR. In FD it is an impulse; in TR it is a constant. Neither is wrong — they are
answers to different questions — but they are not interchangeable, and nothing
will warn you.
:::

The same applies to what comes back: **FD answers in s**. Voltages and currents
are functions of s, and if you want them in time you have to transform them
back.

Resistances are read in the s-domain too, which is more useful than it sounds:
it means you can describe a capacitor or an inductor *as an impedance*, writing
its value in terms of s, as long as its initial condition is zero.

Other than the domain, FD and TR are twins. Capacitors and inductors given in
farads and henries are described identically in both, and so is everything
else — shorts, op-amps, transformers, all of it.

::: problem AS7's Example 16.1
Find {{var:v_o}}(t) in the circuit, assuming zero initial conditions.

::: figure assets/circuit/as7e1601.png
AS7's Example 16.1
:::

::: answer
Before we start: this problem does not need the s-domain at all. The source is
given as a function of time and the answer is wanted as a function of time, so
TR will do it in one step. Notice that the source value is written in the
time domain, because that is what TR reads:

```sym 7
"e,1,0,u(t):r1,1,2,1:r2,2,o,5:c,2,0,1/3,0:l,o,0,1,0"→cir:s\tr(cir):vo
```
```sym 8
"e,1,0,u(t):r1,1,2,1:r2,2,o,5:c,2,0,1/3,0:l,o,0,1,0"→cir:s\tr(cir):vo
```
```field 9 Circuit Description
e,1,0,u(t)
r1,1,2,1
r2,2,o,5
c,2,0,1/3,0
l,o,0,1,0
```

::: only 9
Run it in TR. The answer is `vo`:

$$
v_o(t) = \dfrac{3\sqrt{2}}{2}\,e^{-4t}\sin(\sqrt{2}\,t)
$$

::: applink AS7's Example 16.1 (in TR, the one-step way)
:::
:::

Now let us do it properly, in the s-domain, which is what you would want if any
of the intermediate answers interested you.

The extreme version describes everything as an impedance in s — the source as
`1/s`, the capacitor as `3/s`, the inductor as `s`:

```sym 7
"e,1,0,1/s:r1,1,2,1:r2,2,o,5:r3,2,0,3/s:r4,o,0,s"→cir:s\fd(cir):vo
```
```sym 8
"e,1,0,1/s:r1,1,2,1:r2,2,o,5:r3,2,0,3/s:r4,o,0,s"→cir:s\fd(cir):vo
```
```field 9 Circuit Description
e,1,0,1/s
r1,1,2,1
r2,2,o,5
r3,2,0,3/s
r4,o,0,s
```

::: applink AS7's Example 16.1 (in FD, everything as an impedance)
:::

That was to prove it can be done. In practice the schematic gives you farads
and henries, so give Symbulator farads and henries and let it do the converting:

```sym 7
"e,1,0,1/s:r1,1,2,1:r2,2,o,5:c,2,0,1/3,0:l,o,0,1,0"→cir:s\fd(cir):vo
```
```sym 8
"e,1,0,1/s:r1,1,2,1:r2,2,o,5:c,2,0,1/3,0:l,o,0,1,0"→cir:s\fd(cir):vo
```
```field 9 Circuit Description
e,1,0,1/s
r1,1,2,1
r2,2,o,5
c,2,0,1/3,0
l,o,0,1,0
```

::: only 9
Choose *FD — complex frequency domain*.

::: applink AS7's Example 16.1 (in FD, farads and henries)
:::
:::

Both give the same answer, in the s-domain:

$$
v_o(s) = \dfrac{3}{s^2 + 8s + 18}
$$

Note the source: `1/s`, not `1`. The unit step is `1/s` in the s-domain, and
writing `1` there would have described an impulse instead.
:::
:::

## The t2s and s2t shortcuts {#t2s-s2t}

Having to transform every source by hand before typing it, and every answer by
hand afterwards, would make the s-domain more trouble than it saves. Symbulator
gives you both directions.{{i:Laplace transform}}

{{v7,8|**s\t2s(expression)** converts an expression that is a function of time
into its s-domain equivalent, and **s\s2t(expression)** converts back.}}{{v9|`t2s(expression)`
converts an expression that is a function of time into its s-domain
equivalent, and `s2t(expression)` converts back. Both work wherever you can
write an expression: in a source value, in {{card:Evaluate}}, and in the {{card:Solve}}
card.}}

::: only 7,8
These are wrappers around {{t:laplace}}'s Laplace and inverse Laplace
transforms. Symbulator uses DiffEq, by Lars Frederiksen, as a dependency for
them.
:::

So the whole problem can be done in the s-domain while you write the source in
the domain the schematic gave it to you in:

```sym 7
"e,1,0,s\t2s(u(t)):r1,1,2,1:r2,2,o,5:c,2,0,1/3,0:l,o,0,1,0"→cir:s\fd(cir):s\s2t(vo)
```
```sym 8
"e,1,0,s\t2s(u(t)):r1,1,2,1:r2,2,o,5:c,2,0,1/3,0:l,o,0,1,0"→cir:s\fd(cir):s\s2t(vo)
```
```field 9 Circuit Description
e,1,0,t2s(u(t))
r1,1,2,1
r2,2,o,5
c,2,0,1/3,0
l,o,0,1,0
```

::: only 9
Run that in FD, then put the answer back into the time domain from
{{card:Evaluate}}:

```field 9 Evaluate
s2t(vo)
```

::: applink AS7's Example 16.1 (in FD, and back to time)
:::
:::

::: only 7,8
### The curly-bracket shorthand

There is a shorter way to say "this source value is in the time domain": wrap
it in curly brackets, and Symbulator converts it for you.

```sym 7
"e,1,0,{u(t)}:r1,1,2,1:r2,2,o,5:c,2,0,1/3,0:l,o,0,1,0"→cir:s\fd(cir)
```
```sym 8
"e,1,0,{u(t)}:r1,1,2,1:r2,2,o,5:c,2,0,1/3,0:l,o,0,1,0"→cir:s\fd(cir)
```

The shorthand works only inside a circuit description, so the answer still
needs `s\s2t` when you ask for it:

```sym 7
s\s2t(vo)
```
```sym 8
s\s2t(vo)
```

Either way, the same answer.
:::
::: only 9
### The curly-bracket shorthand

Wrap the value in curly brackets — `{u(t)}` — and FD reads it as `t2s(u(t))`.
It works only inside a circuit description, so the answer still needs `s2t(...)` when you ask for it
in {{card:Evaluate}}.
:::

## Instructive FD problems {#practice-fd}

::: practice

::: problem AS7's Practice Problem 16.1
Determine {{var:v_o}}(t) in the circuit.

::: figure assets/circuit/as7pp1601.png
AS7's Practice Problem 16.1
:::

::: answer
The same shape as the example above, so the same approach: describe it in FD
with the source converted, then transform the answer back.

```sym 7
"e,1,0,s\t2s(u(t)):r1,1,2,6:c,1,0,1/4,0:l,1,o,2,0:r2,o,0,3"→cir:s\fd(cir):s\s2t(vo)
```
```sym 8
"e,1,0,s\t2s(u(t)):r1,1,2,6:c,1,0,1/4,0:l,1,o,2,0:r2,o,0,3"→cir:s\fd(cir):s\s2t(vo)
```
```field 9 Circuit Description
e,1,0,t2s(u(t))
r1,1,2,6
c,1,0,1/4,0
l,1,o,2,0
r2,o,0,3
```

::: only 9
FD, then `s2t(vo)` in {{card:Evaluate}}.
:::
:::
:::

:::

## Transfer function problems {#transfer-functions}

A transfer function is a ratio of two answers, so there is nothing new to
learn: solve the circuit with a symbolic source, then divide.

Because both answers are functions of s, so is their ratio — which is exactly
what a transfer function is meant to be.

::: problem NR11's Example 13.7
Find the transfer function H(s) = {{var:V_o}}/{{var:V_s}}.

::: figure assets/circuit/nr11e1307.png
NR11's Example 13.7
:::

::: answer
Give the source a symbolic value and solve in FD:

```sym 7
"e,1,0,vs:r1,1,2,1'k:c,2,0,1'µ:r2,2,o,1'k"→cir:s\fd(cir):vo/vs
```
```sym 8
"e,1,0,vs:r1,1,2,1'k:c,2,0,1'µ:r2,2,o,1'k"→cir:s\fd(cir):vo/vs
```
```field 9 Circuit Description
e,1,0,vs
r1,1,2,1'k
c,2,0,1'µ
r2,2,o,1'k
```

::: only 9
Solve in FD, then ask {{card:Evaluate}} for the ratio:

```field 9 Evaluate
vo/vs
```
:::

The answer is a function of s, as a transfer function should be.
:::
:::
