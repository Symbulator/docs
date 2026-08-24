---
id: lesson-power
kind: lesson
title: Power in AC circuits
updated: 2023-07-08
summary: >
  Learn to solve *average power* and *complex power* problems in AC. Learn how
  you can use RMS values in Symbulator with the **rms** flag. Solve power
  factor problems using the **pf** tool.
---

In this lesson you will learn how to run more advanced *alternating current*
simulations. You will learn how to solve *average power* problems, when and how
to use the **rms** flag, and how to solve *complex power* problems.

## Average power {#average-power}

::: problem AS7's Example 11.5
Determine the load impedance ZL that maximises the average power drawn from the
circuit. What is the maximum average power?

::: figure assets/circuit/as7e1105.png
AS7's Example 11.5
:::

::: answer
Symbulator's **th** tool helps us find all the answers we need. Notice this
circuit description does not include the load, because it is not needed as
input to th.

```sym 7
"e,1,0,10:r1,1,2,4:r2,2,0,8-6𝐢:r3,2,3,5𝐢"→cir
s\th(cir,3,0)
```
```sym 8
"e,1,0,10:r1,1,2,4:r2,2,0,8-6𝐢:r3,2,3,5𝐢"→cir
s\th(cir,3,0)
```
```sym 9
eq = th("e,1,0,10:r1,1,2,4:r2,2,0,8-6j:r3,2,3,5j",
        "3", "0", domain="ac")
```

::: only 7,8
When asked a type of analysis, specify AC. Then you will be asked if a load
problem is next. You don't have to answer Yes, but I invite you to, because I
want to show you something cool.
:::

The tool saves the equivalent impedance in {{v7,8|`zeq`}}{{v9|`eq.z`}}, which
evaluates approximately to 2.933 + j4.467. The load that will deliver the
maximum power is its conjugate, 2.933 − j4.467.

The average maximum power delivered by the circuit is in
{{v7,8|`apmax`}}{{v9|`eq.pmax`}}, which evaluates to 2.3674 W.
{{v9|There is no separate `apmax` in Symbulator 9: `pmax` looks at the domain
you asked for, and in the AC domain it is already the *average* maximum power,
computed from the real part of the equivalent impedance.}}

::: only 7,8
Now, here's the cool part: when you answer Yes to the load question, Symbulator
saves expressions for the current through, voltage drop in, average power and
complex power in a load connected to the equivalent circuit, as a function of
the complex value of that load — the variable `load_`, where the underscore
tells the calculator to treat this variable as complex. This means you can
verify that this is the maximum power delivered:

```sym 7
aprl|load_=conj(zeq)
```
```sym 8
aprl|load_=conj(zeq)
```

It evaluates to the same answer.
:::
::: only 9
Now, here's the cool part. Symbulator 9 carries no load expressions on the
result — `th` returns `vth`, `ino`, `z` and `pmax`, and nothing else — but you
can build them yourself in two lines, exactly as in {{ref:lesson-equivalents}}.
The AC case wants the *average* power in the load, which for magnitude values
carries the familiar factor of one half:

```sym 9
from sympy import Symbol, conjugate, Abs, re, N
load = Symbol("load")
irl = eq.vth / (eq.z + load)
aprl = Abs(irl)**2 * re(load) / 2
```

Note that `load` here is an ordinary SymPy symbol and so complex by default,
which is what we want: the calculator needed the trailing underscore of
`load_` to say the same thing. Now substitute the conjugate of the equivalent
impedance and check that this really is the maximum power delivered:

```sym 9
N(aprl.subs(load, conjugate(eq.z)))
```
```out
2.36742424242424
```

It is the same answer.
:::
:::
:::

## RMS and PF {#rms-and-pf}

In the previous lesson we mentioned that after an AC simulation, besides real
power consumed, you also get the complex power consumed. The way you should
interpret these values depends on the setting of a flag called the RMS
flag.{{i:RMS}}

::: only 7,8
### The {{v7|s\rms}}{{v8|userms}} flag

You will learn in your circuits course that phasor analysis can be conducted
using RMS values. There are certain advantages to this, and you will have to
solve AC circuits both in normal values (also called magnitude values) and in
RMS values. Working in RMS values basically means that all the currents and
voltages in the analysis are considered to be RMS. That's it.

The flag that tells the program which you want is stored in a variable called
{{v7|**s\rms**}}{{v8|**userms**}}, and it can be true or false. By default, it is
*false*.

When the flag is false, AC analysis assumes normal values: Symbulator assumes
all the currents and voltages you give it are magnitude values, gives you all
the answers in magnitude values, and stores the average real power consumed in
r, e, j and o elements in a variable called **ap** plus the element name.

When the flag is true, AC analysis assumes RMS values throughout, and the
average real power consumed lands in a variable called **p** plus the element
name.
:::
::: only 9
### The use_rms argument

You will learn in your circuits course that phasor analysis can be conducted
using RMS values. There are certain advantages to this, and you will have to
solve AC circuits both in normal values (also called magnitude values) and in
RMS values. Working in RMS values basically means that all the currents and
voltages in the analysis are considered to be RMS. That's it.

Where the calculator versions used a flag variable that persisted between runs,
Symbulator 9 takes it as an argument to `ac`, so it can never be left set from
a previous problem:

```sym 9
res = ac(cir, omega=omega, use_rms=True)
```
:::

::: problem AS7's Example 11.10
Determine the power factor of the entire circuit as seen by the source.
Calculate the average power delivered by the source.

::: figure assets/circuit/as7e1110.png
AS7's Example 11.10
:::

::: answer
The source value in this problem is given in RMS values, so we must say so.

```sym 7
true→s\rms
"e,1,0,30.:r1,1,2,6.:r2,2,0,-𝐢2.:r3,2,0,4."→cir
s\ac(cir,ω)
```
```sym 8
true→userms
"e,1,0,30.:r1,1,2,6.:r2,2,0,–𝐢2.:r3,2,0,4."→cir
s\ac(cir,ω)
```
```sym 9
res = ac("e,1,0,30:r1,1,2,6:r2,2,0,-2j:r3,2,0,4",
         omega=Symbol("omega"), use_rms=True)
```

Or, if you want to simplify the impedances, the resistors can be collapsed into
a single parallel combination.

The average power *consumed* by the source is in `pe`. To get the average power
*delivered*, we ask for the negative of it, which gives us 125.4 W.
:::
:::

### The pf tool

::: only 7,8
To find the power factor of an element answer, we can use the **s\pf**
tool.{{i:power factor}} We can use this tool in two ways.

**With a complex expression as input.** One way is to give it a complex
expression, with real and imaginary parts. It can contain symbolic and/or
numerical values, exact or approximate; it can be a complex number in
rectangular or angular form; or it can be a variable holding such an
expression, such as the complex power consumed in an element:

```sym 7
s\pf(se)
```
```sym 8
s\pf(se)
```

The pf tool takes this complex value and calculates the power factor as the
absolute value of the real part divided by the magnitude of the whole thing.

Now, this is not the whole picture: we need to know whether this power factor
is leading or lagging.

**With an element name as input.** The second way is to give it a string with
the name of a single element that was part of an s\ac simulation that just
finished. The tool recognises three elements in this form: e, j and r:

```sym 7
s\pf("e")
```
```sym 8
s\pf("e")
```
```out
pf: 0.97342 leading
```

In a nutshell: if you give pf a complex number or expression, you get a number
or expression for the power factor, but no indication of leading or lagging. If
you give it the name of an element in a string, right after an s\ac simulation,
you get the value and a verbal description of lagging or leading. This second
form only works if the expression can be evaluated numerically.
:::
::: only 9
Symbulator 9 has the same tool, spelled `pf`, but it takes the voltage and the
current as two separate arguments rather than a single complex power or an
element name:{{i:power factor}}

```sym 9
from symbulator import pf
pf(res["v_e"], -res["i_e"])
```
```out
pf: 0.97342 leading
```

It returns the value and the verbal description together, in one string, just
as the calculator prints them.

::: warning Mind the sign for a source
The minus sign in front of `res["i_e"]` is not a typo, and leaving it out will
quietly give you the wrong word. Symbulator reports the power, voltage and
current *consumed by* each element, source or not, so the current stored in
`i_e` runs into the source rather than out of it. The calculator's pf tool
knew, from the element name you handed it, that `e` was a source, and flipped
the sign for you. The Python function is given two bare phasors and cannot
know where they came from, so it cannot. Call it with `-res["i_e"]` — the
current the source *delivers* — and you get **0.97342 leading**; call it with
`res["i_e"]` and you get 0.97342 lagging, which is the same magnitude and the
wrong answer.

The rule of thumb: negate the current for a source, leave it alone for a load.
:::
:::

## Complex power {#complex-power}

::: problem AS7's Example 11.13
The figure shows a load being fed by a voltage source through a transmission
line. The impedance of the line is represented by the (4+j2) Ω impedance and a
return path. Find the real power and reactive power delivered by the source,
and absorbed by the line and load.

::: figure assets/circuit/as7e1113.png
AS7's Example 11.13
:::

::: answer
The value of this circuit's source is given in RMS. Since the problem asks for
answers regarding the line and the load, we should have separate impedances,
one for each.

```sym 7
true→s\rms
"e1,1,0,220.:r1,1,2,4.+2.𝐢:r2,2,0,15.–10.𝐢"→cir
s\ac(cir,ω)
```
```sym 8
true→userms
"e1,1,0,220.:r1,1,2,4.+2.𝐢:r2,2,0,15.–10.𝐢"→cir
s\ac(cir,ω)
```
```sym 9
res = ac("e1,1,0,220:r1,1,2,4+2j:r2,2,0,15-10j",
         omega=Symbol("omega"), use_rms=True)
```

The complex power absorbed in the source, line and load are in `-se1`, `sr1`
and `sr2`:

```out
{2163.8–911.1𝐢, 455.5+227.8𝐢, 1708.2–1138.8𝐢}
```

These are correct.
:::
:::

::: practice Further power problems
TODO: convert the remaining problems in this lesson from docs-page7:
AS7's Practice Problem 11.10, Problem 11.97 and Problem 11.75 (which includes
the nice trick of solving for the capacitance that gives unity power factor).
:::
