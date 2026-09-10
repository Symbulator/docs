---
id: lesson-ac
kind: lesson
title: Alternating current analysis
updated: 2023-07-08
summary: >
  Learn how to run an *alternating current* analysis (via phasor analysis)
  using {{tool:ac}}. Learn how to describe capacitors, inductors, *impedances and
  admittances*, and sources for AC analysis.
---

In this lesson you will learn how to use the {{tool:ac}} {{v7,8|program}}{{v9|analysis}}
to solve AC circuits in Symbulator. You will also learn how to describe the
elements you already know so they suit AC analysis, and how to {{v7,8|use {{tool:er}} and
{{tool:th}} in their AC mode}}{{v9|find equivalents in AC}}.

## AC analysis in Symbulator {#ac-analysis}

The main thing to know is that in AC mode Symbulator understands phasors —
complex numbers.{{i:phasor}} It uses them in the input, in the analysis and in
the output.

::: danger Symbulator does not understand sinusoids
You should not feed Symbulator any sinusoids, or expect any sinusoid answers
from it. Any conversion to and from sinusoids has to be done by you.
:::

::: only 7,8
### The ac program

Symbulator has a program for analysing AC circuits, called **s\ac**. Unlike
s\dc and s\tr, which take only the circuit description, s\ac takes two inputs:
the description, in a string, and the frequency of the circuit in radians per
second.

### The AC mode

Besides s\ac itself, you can use s\er, s\th and s\ex in their AC mode: select
AC when asked what type of analysis you want. This lesson has examples of all
of them.
:::
::: only 9
### The AC analysis

Set {{ui:Analysis}} to *AC — alternating current*. Unlike DC and TR, it needs
one more input: the frequency in radians per second, typed into the
{{ui:ω — angular frequency}} box beside the menu.

### AC mode in the other tools

The equivalence tools work in AC the same way: choose *Find equivalent* as
usual, set {{ui:Analysis}} to *AC — alternating current*, and give the ω box a
frequency where the circuit needs one.
:::

### Describing elements for AC

When describing a circuit for AC analysis, element values have to be written
the way this analysis expects. Valueless elements, like the short circuit and
the op amp, are unchanged. Here's how to describe the ones with values:

- Current sources **j** and voltage sources **e** accept complex values. You can
  declare their value in rectangular form, e.g. `10-3𝐢`, or in angular form,
  e.g. `(100∠120°)`.
- The element **r** no longer represents just a resistor: it now represents an
  **impedance**.{{i:impedance}} If you are wondering why we didn't use the
  letter z, wait until we get to two-ports. In AC analysis, r accepts complex
  numbers as its value, such as `10-3𝐢`. We use r to describe resistors (real
  values) and conductances (real values, inverted), but also impedances
  (complex values) and admittances (the inverse of their complex value).
- The elements **c** and **l** are used to describe capacitors and inductors
  *only* when their values are given in farads and henries, respectively. For
  AC analysis their description no longer requires the fifth field for the
  initial condition, since alternating current analysis focuses on the steady
  state after transient effects are long gone. So we only use the name, the two
  nodes, and the value.

::: warning If it's in Ω, it's an r
When the problem gives us the values of capacitors and inductors in ohms, we
**must** describe them as impedances. If a capacitor has its value in farads,
describe it with **c**. If an inductor has its value in henries, describe it
with **l**. But anything that has its value in ohms — resistor, impedance,
capacitor or inductor — must be described using **r**.
:::

The values of all of these elements can use SI prefixes.

### What answers do you get

You get the same answers you did in DC, except that now they are phasors. The
one difference is that now, besides the real power consumed, you also get the
complex power consumed. We will discuss this in {{ref:lesson-power}}.

### Rectangular or polar {#polar-phasors}

A phasor can be written two ways, and circuit problems use both: in
*rectangular* form as `3 + 4j`, or in *polar* form as an amplitude and an
angle, 5∠53.13°. They are the same number. Which one you want depends on
the question — rectangular adds and subtracts easily, polar multiplies and
divides easily, and textbook answers are usually quoted in
polar.{{i:polar phasors}}

::: only 7,8
Symbulator answers in rectangular form, and the **aa** tool converts one
answer at a time. You will see it used throughout this lesson.
:::

::: only 9
Symbulator answers in rectangular form unless you ask otherwise. In
{{card:Settings}}, under *Display*, tick {{ui:Show AC answers as polar phasors}} and
every answer is shown as an amplitude and an angle. The circuit is re-solved
as soon as you tick it.

Three things it leaves alone:

- **Average power stays a plain number.** It is real, so an angle would be
  meaningless. Complex power *is* converted: its polar form is the apparent
  power and the power-factor angle. See {{ref:lesson-power}}.
- **Symbolic answers are left as they are.** There is no angle to take of
  $v_{in} r_b/(r_a + r_b)$.
- **It applies to AC only.** DC answers are real, and TR and FD answers are
  functions of *t* or *s*. The checkbox greys out there.

An answer that happens to be real still gets its angle, 0° or 180°, as the
**aa** tool does.

::: tip It combines with SI prefixes
With SI prefixes on too, the amplitude carries the prefix and the angle
stays in degrees: `632.5 m∠108.4°`.

A polar answer is always a decimal, even under *exact*: an angle in degrees
has no closed form to preserve.
:::

The **aa** tool is still the better choice for converting one value, or an
expression that is not an answer by itself, such as a difference between two
node voltages. {{ref:lesson-threephase}} uses it that way throughout.
:::

## Solved numerical examples {#ac-numerical}

### With values in F and H

::: problem AS7's Example 9.9
Find {{var:v}}(t) and {{var:i}}(t).

::: figure assets/circuit/as7e0909.png
AS7's Example 9.9
:::

::: answer
Since this is the first AC problem we will solve, I will explain every step,
including the manual ones, in full detail.

*Step 1: sinusoids to phasors.* We have to express the value of the source in
terms Symbulator can understand, so we convert it from a sinusoid to a phasor:
10∠0°. We can pass this as `(10∠0°)` or, since the angle is zero, simply as
`10`.

*Step 2: note the frequency.* The circuit has a capacitor with a value given in
farads. Because of this, Symbulator will need the frequency, given by the
problem as 4 rad/s, to convert that value into an impedance in ohms.

*Step 3: describe the circuit.*

```sym 7
"e,1,0,10:r1,1,2,5:c,2,0,.1"→cir
s\ac(cir,4)
```
```sym 8
"e,1,0,10:r1,1,2,5:c,2,0,.1"→cir
s\ac(cir,4)
```
```field 9 Circuit Description
e,1,0,10
r1,1,2,5
c,2,0,.1
```

::: only 9
Choose *AC — alternating current*, and put **4** in the {{ui:ω — angular frequency}} box that
appears beside it.
:::

Notice that, in our circuit description, the order we give to the nodes of the
resistor and the capacitor is chosen to be convenient for the answers we will
ask for.

*Step 4: read the answers.* Once Symbulator is done, you should take a look at
what it found:

- the usual voltages in the nodes, voltage drops in the elements, and currents
  through the elements, in variables that should be familiar by now
- the *average power consumed* in the source and the resistor, in
  {{v7,8|`ape` and `apr1`}}{{v9|`ape` and `apr1`}}. None is given
  for the capacitor, since capacitors and inductors do not consume real power.
- the *complex power consumed* in all elements, in {{v7,8|`sc`, `se` and
  `sr1`}}{{v9|`sc`, `se` and `sr1`}}
- the *equivalent impedance* of the rest of the circuit as seen by the source,
  in {{v7,8|`ze`}}{{v9|`ze`}}

To get the answers we need for this problem in particular, we ask for `ir1` and
`vc`. It is likely that {{v7,8|the calculator}}{{v9|Symbulator}} will give you the answers in
rectangular form, with a real part and an imaginary part.

::: only 7,8
If we want to see them as an amplitude and angle, we can use Symbulator's
**aa** tool:{{i:aa tool}}

```sym 7
s\aa(ir1)
```
```sym 8
s\aa(ir1)
```
```out
1.789∠26.57°
```
:::
::: only 9
If we want to see them as an amplitude and angle, open the {{card:Mini-Tools}}
card under the results, leave the tool set to *aa — amplitude and angle*,
and give it the answer's name:{{i:aa tool}}

```field 9 Value
ir1
```

It reads {{o:1.789}}∠{{o:26.57}}° A.

To see *every* answer in polar form, use the setting described in
*Rectangular or polar*, above.
:::

This is correct. You manually convert it to a sinusoid, by putting it back in
the same terms the input was given in:

$$
i(t) = 1.789 \cos(4t + 26.57°)\ \mathrm{A}
$$

Asking for the capacitor voltage the same way gives 4.472∠-63.43°, that is,

$$
v(t) = 4.472 \cos(4t - 63.43°)\ \mathrm{V}
$$

which is correct.

Future solved problems will not include this level of detail in the solution,
only the circuit description and the {{v7,8|commands we give}}{{v9|settings we choose}}.
:::
:::

::: problem AS7's Practice Problem 9.9
Determine {{var:v}}(t) and {{var:i}}(t).

::: figure assets/circuit/as7pp0909.png
AS7's Practice Problem 9.9
:::

::: answer
```sym 7
"e,1,0,(20∠30°):r1,1,2,4:l,2,0,.2"→cir
s\ac(cir,10)
```
```sym 8
"e,1,0,(20∠30°):r1,1,2,4:l,2,0,.2"→cir
s\ac(cir,10)
```
```field 9 Circuit Description
e,1,0,(20∠30°)
r1,1,2,4
l,2,0,.2
```

::: only 9
The source is given in polar form and typed as written: magnitude, the angle
sign, then degrees.

Then AC, with **10** for ω. {{card:Mini-Tools}} with *aa* reads
`ir1` as {{o:4.472}}∠{{o:3.43}}° A and `vl` as {{o:8.944}}∠{{o:93.43}}° V.
Both are correct.
:::

::: only 7,8
We ask for the current in the resistor and get 4.472∠3.43°, and for the voltage
in the inductor and get 8.944∠93.43°. Both are correct.
:::
:::
:::

::: problem AS7's Example 9.10
Find the input impedance of the circuit. Assume that the circuit operates at
ω = 50 rad/s.

::: figure assets/circuit/as7e0910.png
AS7's Example 9.10
:::

::: answer
Since this is a passive circuit, to reduce it we {{v7,8|will use the {{tool:er}} tool}}{{v9|find its equivalent impedance}}.

```sym 7
"ca,1,2,2'm:r1,2,3,3:cb,3,0,10'm:l1,2,4,.2:r2,4,0,8"→cir
s\er(cir,1,0)
```
```sym 8
"ca,1,2,2'm:r1,2,3,3:cb,3,0,10'm:l1,2,4,.2:r2,4,0,8"→cir
s\er(cir,1,0)
```
```field 9 Circuit Description
ca,1,2,2'm
r1,2,3,3
cb,3,0,10'm
l1,2,4,.2
r2,4,0,8
```

::: only 9
Set {{ui:Type of analysis}} to *Find equivalent* and {{ui:Type of equivalent}} to
*Resistance / impedance*, with nodes **1** and **0**, in AC at ω **50**. The answer
is called `zeq`.
:::

::: only 7,8
When asked what type of analysis, choose AC. Since there are capacitors in
farads and an inductor in henries, Symbulator will ask you for the frequency;
enter 50. Once the program is done, ask for the equivalent impedance, `zeq`.
:::

```out 7,8
3.22–𝐢11.07
```
::: only 9
::: result equivalent impedance
Z_{eq} = 3.22 - 11.07\,\text{j}\ \Omega
:::
:::

That is 3.22 − j11.07 Ω, which is correct.

::: tip The pr tool only reduces impedances
In case you were tempted to reduce this circuit by hand instead of simulating
it, remember that parallel reduction works on resistors and impedances only.
You would need to convert the capacitors and the inductor to impedances in ohms
before you do that.
:::
:::
:::

::: problem AS7's Problem 9.35
Find the steady-state current {{var:i}} in the circuit when
{{var:v_s}}(t) = 50 cos 200t V.

::: figure assets/circuit/as7p0935.png
AS7's Problem 9.35
:::

::: answer
The capacitor is in farads and the inductor in henries, so Symbulator needs the
frequency, and the source is entered as its phasor: 50 cos 200t is `50` at an
angular frequency of 200.

```sym 7
"e,1,0,50:r,1,2,10:c,2,3,5'm:l,3,0,20'm"→cir
s\ac(cir,200)
```
```sym 8
"e,1,0,50:r1,1,2,10:c,2,3,5'm:l,3,0,20'm"→cir
s\ac(cir,200)
```
```field 9 Circuit Description
e,1,0,50
r,1,2,10
c,2,3,5'm
l,3,0,20'm
```

::: only 9
AC, with {{ui:ω — angular frequency}} set to **200**.
:::

::: only 7
Choose AC. Symbulator asks for the frequency because of the farads and
henries; enter 200. Then ask for `s\aa(ir)`.
:::
::: only 8
Choose AC. Symbulator asks for the frequency because of the farads and
henries; enter 200. Then ask for `s\aa(ir1)`.
:::

```sym 7
s\aa(ir)
```
```sym 8
s\aa(ir1)
```

::: only 7,8
We get {{o:4.789}}∠{{o:-16.7}}° A.
:::

::: only 9
Read it with {{card:Mini-Tools}} set to *aa*: `aa(ir)` gives
{{o:4.789}}∠{{o:-16.70}}° A. Correct.
:::

::: only 7,8
That is 4.789 A at an angle of −16.7°, which is correct.
:::

::: only 7,8
::: tip Why the resistor is r on one calculator and r1 on the other
The version 7 description above names its resistor `r`; the version 8 one
cannot, because the Nspire reserves `r` (and `rr`), as {{ref:lesson-dc}}
notes — `r1` is the usual fix there.
:::
:::
:::
:::

### With values in Ω only

When the values of all the capacitors and inductors in the circuit are given in
imaginary ohms, they must be entered in the circuit description as impedances,
**r**. In these cases, Symbulator will not need a frequency.

::: problem AS7's Problem 9.37
Determine the admittance Y for the circuit.

::: figure assets/circuit/as7p0937.png
AS7's Problem 9.37
:::

::: answer
Since the values are in ohms, these are all impedances. This is a passive
circuit, so we could {{v7,8|use the er tool}}{{v9|find its equivalent}}. However, the structure of this circuit is
so simple that we can reduce it by hand. The problem asks for the equivalent
admittance, so our answer will be the inverse of the equivalent impedance:

```sym 7
1/(s\pr({4,𝐢8,-𝐢10}))
```
```sym 8
1/(s\pr({4,𝐢8,-𝐢10}))
```
```field 9 Evaluate
1/pr(4,8j,-10j)
```
```out 7,8
0.25-0.025𝐢
```
::: only 9
$$
0.25 - 0.025\,\text{j}\ \mathrm{S}
$$
:::

That is 0.25 − j0.025 S, which is correct.
:::
:::

::: problem AS7's Problem 9.39
For the circuit shown, find the equivalent impedance, and use that to find the
current I. Let omega = 10 rad/s.

::: figure assets/circuit/as7p0939.png
AS7's Problem 9.39
:::

::: answer
The frequency the question gives is superfluous: every value is already in
ohms. Nothing here needs a full simulation either; the equivalent impedance
is one expression, using the parallel shorthand:

```sym 7
4+𝐢20+s\pr({16,-𝐢14+𝐢25})→zeq
```
```sym 8
4+𝐢20+s\pr({16,–𝐢14+𝐢25})→zeq
```
```field 9 Evaluate
4+20j+pr(16,-14j+25j)
```
```out 7,8
9.135+𝐢27.47
```
::: only 9
$$
9.135 + 27.47\,\text{j}\ \Omega
$$
:::

That is 9.135 + j27.47 Ω. The current is the source voltage divided by it:

```sym 7
s\aa(12/zeq)
```
```sym 8
s\aa(12/zeq)
```
::: only 7,8
We get {{o:414.5}}∠{{o:-71.6}}° mA.
:::

::: only 9
Put the whole thing in {{card:Mini-Tools}} with *aa*: `aa(12/(4+20j+pr(16,-14j+25j)))` gives
{{o:0.4145}}∠{{o:-71.60}}° A. Correct.
:::

::: only 7,8
That is 414.5 mA at an angle of −71.6°, which is correct.
:::

::: tip The same answer from a simulation
You can also let Symbulator do the reduction, using the square-bracket
shorthand for parallel elements inside a value:

```field 9 Circuit Description
e,1,0,12
r1,1,0,4+20j+[16,-14j+25j]
```

AC asks for a frequency anyway; put in anything, since every value is
already an impedance. Then `aa(ir1)` gives the same {{o:0.4145}}∠{{o:-71.60}}° A.
:::
:::
:::

::: problem AS7's Problem 9.73
Determine the equivalent impedance for the circuit.

::: figure assets/circuit/as7p0973.png
AS7's Problem 9.73
:::

::: answer
Eight impedances and no source: a job for *Find equivalent* rather than a
solve. The names carry the two nodes each element bridges, a convenience
only.

```sym 7
"r10,1,0,𝐢6:r20,2,0,𝐢8:r30,3,0,𝐢8:r40,4,0,𝐢12:r12,1,2,2:r23,2,3,-𝐢6:r34,3,4,4:r14,1,4,-𝐢4"→cir
s\er(cir,1,0)
```
```sym 8
"r10,1,0,𝐢6:r20,2,0,𝐢8:r30,3,0,𝐢8:r40,4,0,𝐢12:r12,1,2,2:r23,2,3,–𝐢6:r34,3,4,4:r14,1,4,–𝐢4"→cir
s\er(cir,1,0)
```
```field 9 Circuit Description
r10,1,0,6j
r20,2,0,8j
r30,3,0,8j
r40,4,0,12j
r12,1,2,2
r23,2,3,-6j
r34,3,4,4
r14,1,4,-4j
```

::: only 9
Set {{ui:Type of analysis}} to *Find equivalent* and {{ui:Type of equivalent}} to
*Resistance / impedance*, with nodes **1** and **0**, in AC. The answer is called `zeq`.
:::

```out 7,8
0.3794+𝐢1.46
```
::: only 9
::: result equivalent impedance
Z_{eq} = 0.3794 + 1.46\,\text{j}\ \Omega
:::
:::

That is 0.3794 + j1.46 Ω, which is correct.
:::
:::

### With dependent sources

A dependent source is described exactly like an independent one — the value is
just an expression naming another element's answer instead of a
number.{{i:dependent source}}

{{v7,8|Version 7 runs the quantity and the element together, as in `2icx`.}}{{v9|The
name is the one the answers use: the current through **cx** is `icx`, the
voltage across **rx** is `vrx`.}}

::: practice

::: problem AS7's Example 10.1
Find {{var:i_x}} in the circuit.

::: figure assets/circuit/as7e1001.png
AS7's Example 10.1
:::

::: answer
The current source is controlled by the current through the capacitor **cx**,
which is what the last field of **j1** says.

```sym 7
"e1,1,0,20:r1,1,2,10:cx,2,0,.1:l1,2,3,1:j1,0,3,2icx:l2,3,0,.5"→cir
s\ac(cir,4)
```
```sym 8
"e1,1,0,20:r1,1,2,10:cx,2,0,.1:l1,2,3,1:j1,0,3,2icx:l2,3,0,.5"→cir
s\ac(cir,4)
```
```field 9 Circuit Description
e,1,0,20
r1,1,2,10
cx,2,0,.1
l1,2,3,1
j1,0,3,2*icx
l2,3,0,.5
```

::: only 9
AC, with {{ui:ω — angular frequency}} set to **4**.
:::

```sym 7
s\aa(icx)
```
```sym 8
s\aa(icx)
```
::: only 7,8
We get {{o:7.59}}∠{{o:108.4}}° A.
:::

::: only 9
`aa(icx)` gives {{o:7.589}}∠{{o:108.4}}° A. Correct.
:::

::: only 7,8
That is 7.59 A at an angle of 108.4°, which is correct.
:::
:::
:::

::: problem AS7's Practice Problem 10.1
Find {{var:v_1}} and {{var:v_2}} in the circuit.

::: figure assets/circuit/as7pp1001.png
AS7's Practice Problem 10.1
:::

::: answer
This one is controlled by a *voltage* rather than a current — three times the
voltage across **rx**.

```sym 7
"j,0,1,10:rx,1,0,2:c,1,2,.2:l,2,0,2:r,2,3,4:e,3,0,3vrx"→cir
s\ac(cir,2)
```
```sym 8
"j,0,1,10:rx,1,0,2:c,1,2,.2:l,2,0,2:r1,2,3,4:e,3,0,3vrx"→cir
s\ac(cir,2)
```
```field 9 Circuit Description
j,0,1,10
rx,1,0,2
c,1,2,.2
l,2,0,2
r,2,3,4
e,3,0,3*vrx
```

::: only 9
AC, with {{ui:ω — angular frequency}} set to **2**.
:::

```sym 7
{s\aa(v1),s\aa(v2)}
```
```sym 8
{s\aa(v1),s\aa(v2)}
```
::: only 7,8
We get {{o:11.33}}∠{{o:60.02}}° V and {{o:33.02}}∠{{o:57.13}}° V.
:::

::: only 9
`aa(v1)` gives {{o:11.33}}∠{{o:60.02}}° V and `aa(v2)` gives
{{o:33.02}}∠{{o:57.13}}° V.
:::

Both are correct.
:::
:::

::: problem AS7's Example 10.13
Obtain {{var:v_o}} and {{var:i_o}} in the circuit.

::: figure assets/circuit/as7e1013.png
AS7's Example 10.13
:::

::: answer
The book wants its answers in terms of cosine rather than sine, so the source
is taken as 8 cos(1000t − 40°) — as a phasor, `(8∠-40°)`.

Note the decimal points on the values. They make the arithmetic approximate,
which here is what you want: an exact solve of this circuit carries surds
through every step for no benefit.

```sym 7
"e1,1,0,(8.∠-40º):r1,1,2,4.'k:co,2,0,2.'µ:l1,2,3,50.'m:j1,0,3,.5ico:ro,3,0,2.'k"→cir
s\ac(cir,1000.)
```
```sym 8
"e1,1,0,(8.∠-40º):r1,1,2,4.'k:co,2,0,2.'µ:l1,2,3,50.'m:j1,0,3,.5ico:ro,3,0,2.'k"→cir
s\ac(cir,1000.)
```
```field 9 Circuit Description
e,1,0,(8∠-40°)
r1,1,2,4'k
co,2,0,2'µ
l1,2,3,50'm
j1,0,3,.5*ico
ro,3,0,2'k
```

::: only 9
AC, with {{ui:ω — angular frequency}} set to **1000**.
:::

```sym 7
{s\aa(vro),s\aa(ico)}
```
```sym 8
{s\aa(vro),s\aa(ico)}
```
::: only 7,8
We get {{o:1.55}}∠{{o:-95.18}}° V and {{o:3.26}}∠{{o:-3.74}}° mA.
:::

::: only 9
`aa(vro)` gives {{o:1.550}}∠{{o:-95.18}}° V and `aa(ico)` gives
{{o:0.003264}}∠{{o:-3.743}}° A. Both correct.
:::

::: only 7,8
That is 1.55 V at −95.18° and 3.26 mA at −3.74°, both correct.
:::
:::
:::

::: problem AS7's Example 10.14
Find {{var:V_1}} and {{var:V_2}} in the circuit.

::: figure assets/circuit/as7e1014.png
AS7's Example 10.14
:::

::: answer
Every value here is already in ohms, so no frequency matters. Again the decimal
points keep the arithmetic approximate.

```sym 7
"j1,0,1,3.:r1,1,0,1.:rx,1,0,-𝐢1.:r3,1,2,-𝐢2:j2,1,2,.2vrx:r4,1,2,2.+𝐢2.:r5,2,0,-𝐢1.:r6,2,3,2.+𝐢2.:e1,3,0,(18.∠30º)"→cir
s\ac(cir,ω)
```
```sym 8
"j1,0,1,3.:r1,1,0,1.:rx,1,0,–𝐢1.:r3,1,2,–𝐢2:j2,1,2,.2vrx:r4,1,2,2.+𝐢2.:r5,2,0,–𝐢1.:r6,2,3,2.+𝐢2.:e1,3,0,(18.∠30º)"→cir
s\ac(cir,ω)
```
```field 9 Circuit Description
j1,0,1,3
r1,1,0,1
rx,1,0,-1j
r3,1,2,-2j
j2,1,2,.2*vrx
r4,1,2,2+2j
r5,2,0,-1j
r6,2,3,2+2j
e,3,0,(18∠30°)
```

::: only 9
AC. The frequency is asked for but never used, so anything will do.
:::

```sym 7
{s\aa(v1),s\aa(v2)}
```
```sym 8
{s\aa(v1),s\aa(v2)}
```
::: only 7,8
We get {{o:2.708}}∠{{o:-56.73}}° V and {{o:6.914}}∠{{o:-80.70}}° V.
:::

::: only 9
`aa(v1)` gives {{o:2.708}}∠{{o:-56.73}}° V and `aa(v2)` gives
{{o:6.914}}∠{{o:-80.70}}° V. Both correct.
:::

::: only 7,8
That is 2.708 V at −56.73° and 6.914 V at −80.70°, both correct.
:::
:::
:::

:::

## Solved numerical-from-symbolic examples {#ac-numerical-from-symbolic}

::: problem AS7's Problem 9.89
Calculate the value of C so that the net impedance is purely resistive at 2 kHz.

::: figure assets/circuit/as7p0989.png
AS7's Problem 9.89
:::

::: answer
The answer given by the book is 25 µF. But I think this is one of those
unfortunately common instances where there is a mistake in the book. I believe
they meant to ask "at 2k rad/s", because that is the frequency at which the
answer they give is right. Let me tell you how I solved this problem and I will
let you be the judge.

```sym 7
"c,1,0,c:r1,1,2,10:l,2,0,5'm"→cir
s\er(cir,1,0)
```
```sym 8
"c,1,0,c:r1,1,2,10:l,2,0,5'm"→cir
s\er(cir,1,0)
```
```field 9 Circuit Description
c,1,0,c
r1,1,2,10
l,2,0,5'm
```

::: only 9
*Find equivalent*, *Resistance / impedance*, nodes **1** and **0**, AC. The problem gives
2000 Hz and the ω box wants radians per second, so type `2*pi*2e3`
straight into it — it takes an expression, not only a number.
:::

::: only 7,8
When asked, specify AC. Then we are asked for the frequency. The problem gives
2000 Hz; Symbulator asks for radians per second, so I enter `2π2E3`. I could
also have entered 12566.37.

Notice two things. First, I did not use an SI prefix: the shorthand only works
in the circuit description string. Second, I used 2E3 rather than 2000 because
I wanted an approximate value — with exact values, cSolve took too long.

::: warning If exact fails in AC, try approximate
It is a known bug of the TI CAS that `cSolve` often struggles with some exact
equations. You may see that it takes forever to solve, or the {{t:machine}} runs
out of memory. In those cases, try again using approximate values — add a
decimal point to the end of the values, or use engineering notation — or with
symbolic values. More often than not, this bypasses the bug and you get a
solution surprisingly fast.
:::
:::

Once the simulation finishes, solve for the value of c that makes the imaginary
part of the equivalent impedance zero:

```sym 7
solve(imag(zeq)=0,c)
```
```sym 8
solve(imag(zeq)=0,c)
```
::: only 9
Now open the {{card:Solve}} card and ask for the capacitance that leaves no
imaginary part:

```field 9 Equation(s) to solve in terms of the results
im(zeq) = 0
```

```field 9 Unknown(s) to solve for
c
```

Tick {{ui:real solutions only}} before running it. Without it the answer comes back
carrying an `im(c)` term, because nothing has told Symbulator that a
capacitance is a real number.
:::

The answer is **c** = {{o:0.000001235}}, or 1.235 µF. This is not the answer the book
gives.

I first used cSolve here, which also works, but my friend Qifan Wang — who
verified my answers — pointed out, correctly, that it is not necessary:
focusing on the imaginary part removes every reference to the complex operator,
so we are solving an equation in real terms only.

Let's now repeat the process, using what I suspect is the frequency they meant:
2000 rad/s. I also want to show you something cool. Now that we know the answer
is in the range of µF, we can declare the value of the capacitor as `c'µ`, so
that the value of c we get will be in that scale:

::: only 9
```field 9 Circuit Description
c,1,0,c'µ
r1,1,2,10
l,2,0,5'm
```
::: applink AS7's Problem 9.89 (at 2000 rad/s, as it was meant)
:::

*Find equivalent*, *Resistance / impedance*, nodes **1** and **0**, in AC at ω
**2000**. That gives `zeq` = {{o:500j/(-c + 25 + 25j)}}, and the condition
goes to the {{card:Solve}} card:

```field 9 Equation(s) to solve in terms of the results
im(zeq) = 0
```

with `c` as the unknown and {{ui:real solutions only}} ticked — the same
equation as before, now against the new `zeq` — which answers
`c` = {{o:25}}.
:::

```sym 7
"c,1,0,c'µ:r1,1,2,10:l,2,0,5'm"→cir
s\er(cir,1,0)
solve(imag(zeq)=0,c)
```
```sym 8
"c,1,0,c'µ:r1,1,2,10:l,2,0,5'm"→cir
s\er(cir,1,0)
solve(imag(zeq)=0,c)
```

The answer is **c** = {{o:25}}, that is to say 25 µF. This is the right answer in the
book. So they asked the wrong question — they asked it using the wrong
frequency unit.
:::
:::

## Solved symbolic examples {#ac-symbolic}

::: problem AS7's Problem 10.69
Find {{var:V_o}}/{{var:V_s}}.

::: figure assets/circuit/as7p1069.png
AS7's Problem 10.69
:::

::: answer
```sym 7
"e,1,0,vs:c,1,2,c:r1,2,o,r:o,0,2,o"→cir
s\ac(cir,ω)
```
```sym 8
"e,1,0,vs:c,1,2,c:r1,2,o,r:o,0,2,o"→cir
s\ac(cir,ω)
```
```field 9 Circuit Description
e,1,0,vs
c,1,2,c
r1,2,o,r
o,0,2,o
```

::: only 9
The ω box takes a name as readily as a number: type `omega` into it and
the answers come back as functions of it.
:::

We ask for `vo/vs` and get −c·ω·r·𝐢, which is correct.
:::
:::

::: note Know Symbulator's limits
::: only 7,8
Symbulator is a calculator program. It runs on limited hardware, supported by a
limited CAS. It can solve most of the problems you will find in the textbooks
used in Circuits I and II courses, and it particularly shines when solving
symbolic problems. However, as you move to larger and more complex problems, it
will struggle.

In a sense this is not a problem. First, solving large circuits symbolically
makes no sense: the expressions are beyond our understanding. Second, there are
already many established tools for solving them numerically.
:::
::: only 9
Symbulator is a symbolic solver, and symbolic effort grows quickly with the
number of nodes. A circuit that would fill a page with algebra is one you
should be solving numerically anyway.
:::

What matters is that you know the limits, so that they don't take you by
surprise in an exam. Think of Symbulator as a wonderful Swiss knife of circuit
simulators: no matter how good it is, it is still a pocket knife. You would not
try to chop a tree down with it. SPICE and its children — LTspice, PSpice,
MultiSim — are the chainsaws of circuit simulation. They won't give you
symbolic answers, but when you need to chop a tree down, they are the way to
go.

::: problem AS7's Problem 10.77
Compute the closed-loop gain {{var:V_o}}/{{var:V_s}} for the op-amp circuit.

::: figure assets/circuit/as7pr1077.png
AS7's Problem 10.77
:::

::: answer
Here is an example that takes Symbulator to the limit of what it can solve
symbolically — everything in it is a symbol, including the frequency.

```sym 7
"e,1,0,vs:r1,1,2,r1:ca,2,0,ca:r3,0,3,r3:o,2,3,o:cb,3,o,cb:r2,3,o,r2"→cir:s\ac(cir,ω)
```
```sym 8
"e,1,0,vs:r1,1,2,r1:ca,2,0,ca:r3,0,3,r3:o,2,3,o:cb,3,o,cb:r2,3,o,r2"→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
e,1,0,vs
r1,1,2,r1
ca,2,0,ca
r3,0,3,r3
o,2,3,o
cb,3,o,cb
r2,3,o,r2
```

{{v7,8|Notice `ca` and `cb`: `c1` and `c2` are reserved variables on the
calculator.}}

Then ask for the ratio:

```sym 7
vo/vs
```
```sym 8
vo/vs
```

::: only 9
```field 9 Evaluate
vo/vs
```
:::

::: only 7
::: figure assets/screen/ansas7p1077.png
The closed-loop gain, on a TI-89
:::
:::

::: only 8,9
$$
\frac{V_o}{V_s} = \frac{j\,c_b r_2 r_3 \omega + r_2 + r_3}
{r_3\left(-c_a c_b r_1 r_2 \omega^2 + j\,c_a r_1 \omega
+ j\,c_b r_2 \omega + 1\right)}
$$
:::

It looks different from the answer in the book, but evaluating both shows they
are the same expression arranged differently.

::: only 7
This is the limit, and I know it because I have measured it: Symbulator solves
this on my TI-89 Titanium in six minutes, and on my friend Qifan's Voyage 200
it fails altogether unless the source is reduced to a nominal 1 V.
:::
::: only 9
This circuit takes Symbulator 9 about ten seconds, with every value
symbolic.
:::
:::
:::
:::
