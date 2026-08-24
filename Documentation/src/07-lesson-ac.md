---
id: lesson-ac
kind: lesson
title: Alternating current analysis
updated: 2023-07-08
summary: >
  Learn how to run an *alternating current* analysis (via phasor analysis)
  using **ac**. Learn how to describe capacitors, inductors, *impedances and
  admittances*, and sources for AC analysis.
---

In this lesson you will learn how to use the **ac** {{v7,8|program}}{{v9|function}}
to solve AC circuits in Symbulator. You will also learn how to describe the
elements you already know so they are suitable inputs for AC analysis, and how
to use tools you already know, such as **er** and **th**, in their AC mode.

## AC analysis in Symbulator {#ac-analysis}

The main thing you need to know is that, when working in AC mode, Symbulator
understands phasors, namely complex numbers.{{i:phasor}} You can analyse
alternating current circuits by means of phasors: Symbulator uses them in the
input, in the analysis and in the output.

::: danger Symbulator does not understand sinusoids
You should not feed Symbulator any sinusoids, or expect any sinusoid answers
from it. Any conversion to and from sinusoids has to be done by you.
:::

::: only 7,8
### The ac program

Symbulator has a program dedicated to analysing AC circuits, called **s\ac**.
As opposed to s\dc and s\tr, which take only the circuit description, s\ac
takes two inputs: the circuit description, in a string, and the frequency of
the circuit in radians per second.

### The AC mode

Besides the s\ac program itself, you can use other Symbulator tools and
programs, such as s\er, s\th and s\ex, in their AC mode. You do this by
selecting AC from the options when asked what type of analysis you want to
conduct. In this lesson, we will see examples of all of these.
:::
::: only 9
### The ac function

Symbulator has a function dedicated to analysing AC circuits, called **ac**. As
opposed to `dc` and `tr`, it takes a second argument: the frequency of the
circuit in radians per second, passed as `omega`.

### AC mode in the other tools

The `er` and `th` tools also work in AC. Rather than prompting you, they take
`domain="ac"` and, where the circuit needs it, `omega`.
:::

### Describing elements for AC

When describing a circuit for AC analysis, you have to describe the value of
elements in the correct way for this type of analysis. Valueless elements, like
the short circuit and the op amp, are described the same way. Here's how to
describe elements with values:

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

## Solved numerical examples {#ac-numerical}

### With values in F and H

::: problem AS7's Example 9.9
Find v(t) and i(t).

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
e1,1,0,10
r1,1,2,5
c,2,0,.1
```

::: only 9
Choose *AC — alternating current*, and put **4** in the **omega** box that
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
  {{v7,8|`ape` and `apr1`}}{{v9|`ap_e1` and `ap_r1`}}. None is given
  for the capacitor, since capacitors and inductors do not consume real power.
- the *complex power consumed* in all elements, in {{v7,8|`sc`, `se` and
  `sr1`}}{{v9|`s_c`, `s_e1` and `s_r1`}}
- the *equivalent impedance* of the rest of the circuit as seen by the source,
  in {{v7,8|`ze`}}{{v9|`z_e1`}}

To get the answers we need for this problem in particular, we ask for `ir1` and
`vc`. It is likely that the {{t:machine}} will give you the answers in
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
If we want to see them as an amplitude and angle, open the **Mini-tools**
card under the results, leave the tool set to *aa — amplitude and angle*,
and give it the answer's name:{{i:aa tool}}

```field 9 Value
i_r1
```

It reads {{o:1.789}}∠{{o:26.57}}°.
:::

This is correct. You manually convert it to a sinusoid, by putting it back in
the same terms the input was given in:

$$
i(t) = 1.789 \cos(4t + 26.57°)\ \mathrm{A}
$$

Asking for the capacitor voltage the same way gives 4.472∠-63.43°, that is,
$v(t) = 4.472 \cos(4t - 63.43°)$ V, which is correct.

Future solved problems will not include this level of detail in the solution,
only the circuit description and the commands we give.
:::
:::

::: problem AS7's Practice Problem 9.9
Determine v(t) and i(t).

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
e1,1,0,20*exp(j*pi/6)
r1,1,2,4
l,2,0,.2
```

::: only 9
The angle sign is one thing version 9 does not read: `(20∠30°)` is fine on
the calculator and is refused here. Write the source in exponential form
instead — `20*exp(j*pi/6)` is the same phasor, 20 volts at 30 degrees,
since 30° is π/6 radians.

Then AC, with **10** for omega. **Mini-tools** with *aa* reads
`i_r1` as {{o:4.472}}∠{{o:3.43}}° and `v_l` as {{o:8.944}}∠{{o:93.43}}°.
Both are correct.
:::

We ask for the current in the resistor and get 4.472∠3.43°, and for the voltage
in the inductor and get 8.944∠93.43°. Both are correct.
:::
:::

::: problem AS7's Example 9.10
Find the input impedance of the circuit. Assume that the circuit operates at
ω = 50 rad/s.

::: figure assets/circuit/as7e0910.png
AS7's Example 9.10
:::

::: answer
Since this is a passive circuit, to reduce it we will use the **er** tool.

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
Set **Type of analysis** to *Find equivalent* and **Type of equivalent** to
*Impedance*, with nodes **1** and **0**, in AC at omega **50**. The answer
is called `zeq`.
:::

::: only 7,8
When asked what type of analysis, choose AC. Since there are capacitors in
farads and an inductor in henries, Symbulator will ask you for the frequency;
enter 50. Once the program is done, ask for the equivalent impedance, `zeq`.
:::
::: only 9
The domain and the frequency are arguments, so nothing is prompted. Read the
equivalent impedance off the object with `eq.z`.
:::

```out
3.22–𝐢11.07
```

That is 3.22 − j11.07 Ω, which is correct.

::: tip The pr tool only reduces impedances
In case you were tempted to reduce this circuit by hand instead of simulating
it, remember that parallel reduction works on resistors and impedances only.
You would need to convert the capacitors and the inductor to impedances in ohms
before you do that.
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
circuit, so we could use the er tool. However, the structure of this circuit is
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
```out
0.25-0.025𝐢
```

That is 0.25 − j0.025 S, which is correct.
:::
:::

::: practice Further numerical examples
TODO: convert the remaining problems in this section from docs-page7:
AS7's Problem 9.35, 9.39, 9.73, Example 10.1, Practice Problem 10.1,
Example 10.13 and Example 10.14.
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
*Find equivalent*, *Impedance*, nodes **1** and **0**, AC. The problem gives
2000 Hz and the omega box wants radians per second, so type `2*pi*2e3`
straight into it — it takes an expression, not only a number.
:::

::: only 7,8
When asked, specify AC. Then we are asked for the frequency. The problem gives
2000 Hz; Symbulator asks for radians per second, so I enter `2π2E3`. I could
also have entered 12566.37.

Please notice two things. First, I did not use an SI prefix: the shorthand only
works in the circuit description string. Second, I used 2E3 instead of 2000
because I wanted an approximate value rather than an exact one — when I tried
with exact values only, cSolve was taking too long.

::: warning If exact fails in AC, try approximate
It is a known bug of the TI CAS that `cSolve` often struggles with some exact
equations. You may see that it takes forever to solve, or the {{t:machine}} runs
out of memory. In those cases, try again using approximate values — add a
decimal point to the end of the values, or use engineering notation — or with
symbolic values. More often than not, this bypasses the bug and you get a
solution surprisingly fast.
:::
:::
::: only 9
::: tip No cSolve, no ceiling
The exact-versus-approximate problem that plagues the calculator versions comes
from a bug in the TI CAS's `cSolve`. Symbulator 9 solves through SymPy instead,
so exact inputs are safe, and you can leave the frequency as `2*pi*2e3` rather
than pre-computing it.
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
Now open the **Solve** card and ask for the capacitance that leaves no
imaginary part:

```field 9 Equation(s) to solve in terms of the results
im(zeq) = 0
```

```field 9 Unknown(s) to solve for
c
```

Tick **real only** before running it. Without it the answer comes back
carrying an `im(c)` term, because nothing has told Symbulator that a
capacitance is a real number.
:::

The answer is c = 0.000001235, or 1.235 µF. This is not the answer the book
gives.

Initially I used cSolve here, which also works, but my friend Qifan Wang — who
verified my answers to this problem — pointed out, correctly, that it is not
necessary: focusing on the imaginary part removes all references to the complex
operator, so for practical purposes we are solving an equation with real terms
only.

Let's now repeat the process, using what I suspect is the frequency they meant:
2000 rad/s. I also want to show you something cool. Now that we know the answer
is in the range of µF, we can declare the value of the capacitor as `c'µ`, so
that the value of c we get will be in that scale:

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

The answer is c = 25, that is to say 25 µF. This is the right answer in the
book. So they asked the wrong question — they asked it using the wrong
frequency unit.
:::
:::

## Solved symbolic examples {#ac-symbolic}

::: problem AS7's Problem 10.69
Find Vo/Vs.

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
e1,1,0,vs
c,1,2,c
r1,2,o,r
o,0,2,o
```

::: only 9
The omega box takes a name as readily as a number: type `omega` into it and
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

In a sense, this is not a problem. First, because it makes no sense to solve
large circuits symbolically: the resulting expressions are beyond our
understanding. Second, because there are already many established tools to
solve such large circuits numerically.
:::
::: only 9
Symbulator 9 is not bound by the memory of a handheld, so it goes considerably
further than versions 7 and 8 before it slows down. It is still a symbolic
solver, though, and symbolic effort grows quickly with the number of nodes. A
circuit that would fill a page with algebra is one you should be solving
numerically anyway.
:::

What matters is that you know the limits, so that they don't take you by
surprise in an exam. Think of Symbulator as a wonderful Swiss knife of circuit
simulators: no matter how good it is, it is still a pocket knife. You would not
try to chop a tree down with it. SPICE and its children — LTspice, PSpice,
MultiSim — are the chainsaws of circuit simulation. They won't give you
symbolic answers, but when you need to chop a tree down, they are the way to
go.
:::
