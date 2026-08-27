---
id: lesson-coupling
kind: lesson
title: Mutual inductance and ideal transformers
updated: 2023-07-08
summary: >
  Learn how to describe a *mutual inductance* between two inductors or two
  impedances using the **m** element. Learn how to describe an ideal
  *transformer* using the **t** element.
---

Two coils that share a magnetic field are not two separate elements, and a
circuit description has to say so. This lesson covers the two ways of saying
it: **m** for a mutual inductance between a pair of elements, and **t** for an
ideal transformer.

## How to describe mutual inductance {#describe-mutual}

Textbooks give a coupled pair one of two ways, and Symbulator takes
both.{{i:mutual inductance}}

- Two inductors in **henries**, coupled by a mutual inductance also in
  henries.
- Two impedances in **jΩ**, coupled by a mutual impedance also in jΩ. Written
  this way the coils are `r` elements with imaginary values.

Either way the coupling itself is an **m** element with four fields: a name
starting with `m`, the names of the two coupled elements, and the value of the
coupling. For example: `m1,l1,l2,1.5`

That is a mutual inductance of 1.5 H between inductors `l1` and `l2`. In jΩ it
looks the same, naming two `r` elements instead: `m1,r1,r2,2j`

::: warning Don't mix the two
`m1,l1,r1,2` couples an inductor given in henries to one given in jΩ. It will
not be refused and it will not be right. Keep all three values in the same
units: all henries, or all jΩ.
:::

### The dots are the node order

Every coupled-inductor problem in a textbook has a dot on each coil, marking
the ends that share polarity. Symbulator has no way to draw a dot, so **the
first node you name in each coupled element is its dotted end**.

That is the whole convention, and it is the thing most likely to give you a
correct-looking wrong answer. If you list the nodes of one coil the other way
round, the sign of the coupling flips and every current comes back wrong.

::: warning Keep the dots consistent
Read the schematic, decide which end of each coil is dotted, and declare that
node first — in both coupled elements. Look at the solved examples below and
notice that the dotted ends are always the first node given.
:::

The value of a mutual inductance can use SI prefixes.

**What answers do you get?** None. An `m` element is a statement about two
other elements, not a component with its own voltage and current — its effect
shows up in the currents of the elements it couples.

## Instructive m problems {#practice-mutual}

::: practice

::: problem AS7's Example 13.1
Calculate the phasor currents I{{sub:1}} and I{{sub:2}} in the circuit.

::: figure assets/circuit/as7e1301.png
AS7's Example 13.1
:::

::: answer
Three things to notice in the description. The bottom node of both halves is
ground. The coils are given in jΩ, so they are `r` elements with imaginary
values, and the mutual is imaginary too, to match. And the dotted node of each
coupled element is named first.

```sym 7
false→s\rms:"e,1,0,12:r1,1,2,-𝐢4:r2,2,0,𝐢5:m,r2,r3,𝐢3:r3,3,0,𝐢6:r4,3,0,12"→cir:s\ac(cir,ω)
```
```sym 8
false→userms:"e,1,0,12:r1,1,2,–𝐢4:r2,2,0,𝐢5:m,r2,r3,𝐢3:r3,3,0,𝐢6:r4,3,0,12"→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
e,1,0,12
r1,1,2,-4j
r2,2,0,5j
m,r2,r3,3j
r3,3,0,6j
r4,3,0,12
```

::: only 9
AC, and leave **RMS phasors** unticked. Then read the two currents with
**Mini-Tools** set to *aa*:
:::

```sym 7
{s\aa(ir2),s\aa(ir4)}
```
```sym 8
{s\aa(ir2),s\aa(ir4)}
```
```out 7,8
{"13.02ᴇ0∠-49.4°","2.910ᴇ0∠14.04°"}
```

::: only 9
`aa(ir2)` reads {{o:13.02}}∠{{o:-49.4}}° and `aa(ir4)` reads
{{o:2.910}}∠{{o:14.04}}°.
:::

Both are correct.
:::
:::

::: problem AS7's Practice Problem 13.1
Determine the voltage V{{sub:o}} in the circuit.

::: figure assets/circuit/as7pp1301.png
AS7's Practice Problem 13.1
:::

::: answer
Again the dotted node of the coupled inductor comes first.

```sym 7
false→s\rms:"e,1,0,(200.∠45°):r1,1,2,4.:r2,2,0,𝐢8.:m,r2,r3,𝐢1.:r3,0,o,𝐢5.:r4,o,0,10"→cir:s\ac(cir,ω)
```
```sym 8
false→userms:"e,1,0,(200.∠45°):r1,1,2,4.:r2,2,0,𝐢8.:m,r2,r3,𝐢1.:r3,0,o,𝐢5.:r4,o,0,10"→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
e,1,0,(200∠45°)
r1,1,2,4
r2,2,0,8j
m,r2,r3,1j
r3,0,o,5j
r4,o,0,10
```

```out 7,8
"20.00ᴇ0∠-134.43°"
```

::: only 9
`aa(vo)` reads {{o:20.00}}∠{{o:-134.43}}°.
:::

Correct.
:::
:::

::: problem AS7's Example 13.2
Calculate the mesh currents in the circuit.

::: figure assets/circuit/as7e1302.png
AS7's Example 13.2
:::

::: answer
Notice the node order again, matching the dots.

```sym 7
false→s\rms:"e,1,0,100.:r1,1,2,4.-𝐢3.:r2,2,0,𝐢6.:m,r2,r3,𝐢2.:r3,3,2,𝐢8.:r4,3,0,5"→cir:s\ac(cir,ω)
```
```sym 8
false→userms:"e,1,0,100.:r1,1,2,4.–𝐢3.:r2,2,0,𝐢6.:m,r2,r3,𝐢2.:r3,3,2,𝐢8.:r4,3,0,5"→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
e,1,0,100
r1,1,2,4-3j
r2,2,0,6j
m,r2,r3,2j
r3,3,2,8j
r4,3,0,5
```

```out 7,8
{"20.30ᴇ0∠3.5°","8.693ᴇ0∠19.03°"}
```

::: only 9
`aa(ir1)` reads {{o:20.30}}∠{{o:3.5}}° and `aa(ir4)` reads
{{o:8.693}}∠{{o:19.03}}°.
:::

Correct.
:::
:::

:::

## How to describe ideal transformers {#describe-transformer}

An ideal transformer has four terminals — two a side. Symbulator simulates the
case where **one terminal on each side is grounded**, which covers the
textbook problems; you name only the two live nodes.{{i:transformer}}

A **t** element takes five fields: a name starting with `t`, the live node on
the first side, the live node on the second side, and the turns on each
side. For example: `t1,1,2,80,800`

That is 80 turns on the side connected to node 1 and 800 on the side connected
to node 2, wound the same way. Only the ratio matters, so `1,10` would describe
the same transformer.

**Polarity is a minus sign.** If the dots are on opposite ends, make one of
the two turn counts negative: `t,a,b,1,-5`

It does not matter which of the two you make negative, as long as one of them
is.

**What answers do you get?** The voltages at the two live nodes, as for any
node in the circuit, and the current entering the transformer, named with the
transformer and the node — for a transformer `t` on node 2, that is
`it2`.

## Instructive t problems {#practice-transformer}

::: practice

::: problem AS7's Figure 13.33
Obtain V{{sub:Th}} and Z{{sub:Eq}} for the part of the circuit to the right of
nodes a and b.

::: figure assets/circuit/as7f1333.png
AS7's Figure 13.33
:::

::: answer
Everything left of a and b is ignored. Note that this one is entirely
symbolic — the turns ratio, the impedance and the source are all names.

```sym 7
"t,2,3,1,n:r2,3,4,z2:e2,4,0,vs2"→cir:s\th(cir,2,0)
```
```sym 8
"t,2,3,1,n:r2,3,4,z2:e2,4,0,vs2"→cir:s\th(cir,2,0)
```
```field 9 Circuit Description
t,2,3,1,n
r2,3,4,z2
e2,4,0,vs2
```

::: only 9
*Find equivalent*, *Thévenin / Norton*, nodes **2** and **0**, in DC.
:::

```out 7,8
{vs2/n,z2/n^2}
```

::: only 9
`vth` is $v_{s2}/n$ and `req` is $z_2/n^2$.
:::

Correct — the transformer refers the source by the turns ratio and the
impedance by its square, which is exactly what an ideal transformer does.
:::
:::

::: problem AS7's Example 13.8
For the ideal transformer circuit, find the source current I{{sub:1}}, the
output voltage V{{sub:o}}, and the complex power supplied by the source.

::: figure assets/circuit/as7e1308.png
AS7's Example 13.8
:::

::: answer
One of the turn counts is negative here, because the dots are of opposite
polarity.

```sym 7
true→s\rms:"e,1,0,120.:r1,1,2,4.-𝐢6.:t,2,3,1,-2:ro,3,0,20."→cir:s\ac(cir,ω)
```
```sym 8
true→userms:"e,1,0,120.:r1,1,2,4.–𝐢6.:t,2,3,1,-2:ro,3,0,20."→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
e,1,0,120
r1,1,2,4-6j
t,2,3,1,-2
ro,3,0,20
```

::: only 9
AC, with **RMS phasors** ticked this time — the question asks for complex
power, and that is the convention it wants.
:::

```out 7,8
{"11.09ᴇ0∠33.69°","110.9ᴇ0∠-146.31°","1.331ᴇ3∠-33.69°"}
```

::: only 9
Three readings from **Mini-Tools** with *aa*: `ir1` is
{{o:11.09}}∠{{o:33.69}}°, `vro` is {{o:110.9}}∠{{o:-146.31}}°, and
`-se` — the complex power *supplied*, so the opposite of the power consumed
by the source — is {{o:1331}}∠{{o:-33.69}}°.

Three conversions in a row is the point at which the setting is less work
than the tool: tick **Show AC answers as polar phasors** in **Settings** and
the first two are already in that form when the circuit solves. The third
still wants *aa*, because `-se` is an expression rather than an answer.
:::

All three are correct.
:::
:::

:::
