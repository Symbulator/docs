---
id: lesson-power
kind: lesson
title: Power in AC circuits
updated: 2023-07-08
summary: >
  Learn to solve *average power* and *complex power* problems in AC. Learn how
  you can use RMS values in Symbulator with {{v7,8|the **rms** flag}}{{v9|the {{ui:RMS phasors}} setting}}. Solve power
  factor problems using the **pf** {{v7,8|tool}}{{v9|mini-tool}}.
---

In this lesson you will learn how to run more advanced *alternating current*
simulations. You will learn how to solve *average power* problems, when and how
to use {{v7,8|the **rms** flag}}{{v9|the {{ui:RMS phasors}} setting}}, and how to solve *complex power* problems.

## Average power {#average-power}

::: problem AS7's Example 11.5
Determine the load impedance ZL that maximises the average power drawn from the
circuit. What is the maximum average power?

::: figure assets/circuit/as7e1105.png
AS7's Example 11.5
:::

::: answer
{{v7,8|Symbulator's {{tool:th}} tool}}{{v9|*Thévenin / Norton*}} helps us find all the answers we need. Notice this
circuit description does not include the load, because it is not needed{{v7,8| as
input to {{tool:th}}}}.

```sym 7
"e,1,0,10:r1,1,2,4:r2,2,0,8-6𝐢:r3,2,3,5𝐢"→cir
s\th(cir,3,0)
```
```sym 8
"e,1,0,10:r1,1,2,4:r2,2,0,8-6𝐢:r3,2,3,5𝐢"→cir
s\th(cir,3,0)
```
```field 9 Circuit Description
e,1,0,10
r1,1,2,4
r2,2,0,8-6j
r3,2,3,5j
```

::: only 9
*Find equivalent*, *Thévenin / Norton*, nodes **3** and **0**, in AC. In AC
the equivalent impedance is called `zeq` rather than `req`.
:::

::: only 7,8
When asked a type of analysis, specify AC. Then you will be asked if a load
problem is next. You don't have to answer Yes, but I invite you to, because I
want to show you something cool.
:::

{{v7,8|The **s\th** tool saves the equivalent impedance in `zeq`, which
evaluates approximately to 2.933 + j4.467.}}{{v9|*Thévenin / Norton* reports the
equivalent impedance, `zeq`, as 2.933 + j4.467.}} The load that will deliver the
maximum power is its conjugate, 2.933 − j4.467.

The average maximum power delivered by the circuit is {{v7,8|in
`apmax`, which evaluates to}}{{v9|`pmax` =}} 2.3674 W.

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
```out 7,8
2.36742424242424
```

::: only 7,8
It is the same answer.
:::

::: only 9
In AC, `pmax` is the *average* maximum power, computed from the real part of
the equivalent impedance: {{card:Results}} shows `pmax` = {{o:2.367}} W, the power
delivered when the load is the conjugate of `zeq`.{{i:maximum power transfer}}
:::
:::
:::

## RMS and PF {#rms-and-pf}

In the previous lesson we mentioned that after an AC simulation you also get
the complex power consumed. How to read these values depends on {{v7,8|a flag called
the RMS flag}}{{v9|the {{ui:RMS phasors}} setting}}.{{i:RMS}}

::: only 7,8
### The {{v7|s\rms}}{{v8|userms}} flag

You will learn in your circuits course that phasor analysis can be done in RMS
values. There are advantages to it, and you will have to solve AC circuits both
in normal values (also called magnitude values) and in RMS. Working in RMS
simply means every current and voltage in the analysis is taken to be RMS.
That's it.

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
### The RMS setting

You will learn in your circuits course that phasor analysis can be done in RMS
values. There are advantages to it, and you will have to solve AC circuits both
in normal values (also called magnitude values) and in RMS. Working in RMS
simply means every current and voltage in the analysis is taken to be RMS.
That's it.

The switch is in {{card:Settings}}, under **AC power convention**: tick
{{ui:RMS phasors}}.

With the tick **off**, Symbulator takes every phasor you type as a *peak*
value — the amplitude the sinusoid rises to — and the average power in an
element is computed with the factor of one half that peak values require:

$$
P = \tfrac{1}{2}\,V_{\text{peak}}\,I_{\text{peak}}\cos\theta
$$

With the tick **on**, it takes every phasor you type as an *RMS* value, and
the half disappears:

$$
P = V_{\text{rms}}\,I_{\text{rms}}\cos\theta
$$

That is the whole difference. The currents and voltages you get back are
in whatever convention you typed the sources in, unchanged; only the power
answers — `p` and `s` — depend on the tick, and the real power answers to
`p` and to `ap` alike, whichever way the tick is set (the calculator named
it `ap` with peak phasors and `p` with RMS ones); the reactive power is
`im(se)` in {{card:Evaluate}}, the imaginary part of the complex power,
and `re(se)` is the real power again. So for the same numbers
typed in, RMS on reports twice the power that RMS off does, and neither is
wrong: they answer different questions. Match the book you are working
from. The setting is always in view, so it is easier for you to notice
whether it is on or off.
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
```field 9 Circuit Description
e,1,0,30
r1,1,2,6
r2,2,0,-2j
r3,2,0,4
```

::: only 9
AC, with `omega` typed into the ω box, and {{ui:RMS phasors}} ticked in
{{card:Settings}}.
:::

Or, if you want to simplify the impedances, the resistors can be collapsed into
a single parallel combination.

{{v7,8|The average power *consumed* by the source is in `pe`. To get the average power
*delivered*, we ask for the negative of it, which gives us 125.4 W.}}{{v9|The average
power *consumed* by the source is `pe`; the power *delivered* is its opposite,
125.4 W.}}
:::
:::

### The pf {{v7,8|tool}}{{v9|mini-tool}} {#the-pf-tool}

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

In a nutshell: given a complex number or expression, pf returns the power
factor but says nothing about leading or lagging. Given the name of an element
in a string, right after an s\ac simulation, it returns the value and says
which. That second form works only if the expression can be evaluated
numerically.
:::
::: only 9
*pf* is the second of the mini-tools {{ref:lesson-ac}} introduced, and it
works as the calculator's did. In the {{card:Mini-Tools}} card choose
*pf — power factor*; it asks for one value, and there are two things you
can give it.{{i:power factor}}{{i:pf mini-tool}}

**A complex power.** Give it the name of a complex power answer, such as
`se`, or any complex expression — a number in rectangular or polar form,
an impedance, an expression with symbols in it:

```field 9 Value
se
```

It answers {{o:0.97342}} **lagging**: the absolute value of the real part
divided by the magnitude of the whole thing, and the word for the value as
given — nothing more, because by now you know what `se` is. It is the power
the source *consumes*, and the word belongs to that power.

**The name of an element.** Give it the name of an element of the circuit
you have just solved in AC:

```field 9 Value
e
```

It answers {{o:0.97342}} **leading**: the value and the word together, and
under them *this is the power factor for the power delivered by source e*.
This form works only when the element's voltage and current came out as
numbers.

The same number, the opposite word. That is not a contradiction: `se` is
the power the source consumes and `e` reads the power it delivers, and the
two powers are opposite, so their words are. The question *what is the
power factor of the circuit as seen by the source?* is answered by the
name, `e`.

In a nutshell: given a complex power, or any complex expression, pf returns
the power factor of that value as given, with its word and no explanation.
Given the name of an element, right after an AC solve, it reads the right
power for that element's kind and says in words which power that was. With
symbols in the value there is no word, only the expression.

::: note Which power the reading is taken on
The two forms do not read the same power, and the difference is what makes
the word come out right.

Given a **variable** such as `se`, `sj` or `sr1`, the calculation is done on
the value as it stands — the complex power *consumed*, which is what
Symbulator stores for every element, source or load alike — and the word
is that value's own. For an impedance that is its own reading. For a
source it is the reading of the power it *consumes*, which is the opposite
of the power it delivers, so the word comes out opposite to the source's
own. The tool cannot know better from a number alone: the same complex
power is consumed by one side of a branch and delivered by the other.

Given a **name**, the tool reads the sign convention off the element's
kind, the way the calculator did. For an impedance — `r`, and in version 9
`l` and `c` as well — the angle is taken between the element's voltage and
the current it *consumes*, so the reading is the element's own: an
inductive load reads lagging. For a source — `e` or `j` — the current is
negated first, so the angle is taken on the power the source *delivers*,
and the reading is that of the whole circuit the source sees. A source
feeding an inductive load reads lagging, the same word as the load.

The value is the same either way; only the word depends on it. A source
read on its consumed power, `se`, says the opposite word — which is why
the question *as seen by the source* wants the name, and the tool does the
negating itself.
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
```field 9 Circuit Description
e,1,0,220
r1,1,2,4+2j
r2,2,0,15-10j
```

::: only 9
Again AC with `omega` and {{ui:RMS phasors}} ticked.
:::

{{v7,8|The complex power absorbed in the source, line and load are in
`-se1`, `sr1` and `sr2`:}}{{v9|The complex power *delivered* by the source is
the opposite of the power it consumes, `-se`; the complex power *absorbed*
in the line and in the load are `sr1` and `sr2`:{{i:complex power}}}}

```sym 7
{-se1,sr1,sr2}
```
```sym 8
{-se1,sr1,sr2}
```
```out 7,8
{2163.8–911.1𝐢, 455.5+227.8𝐢, 1708.2–1138.8𝐢}
```

::: only 9
{{card:Results}} shows:

- `-se` = {{o:2163.8}} − {{o:911.1}}𝐢 VA
- `sr1` = {{o:455.5}} + {{o:227.8}}𝐢 VA
- `sr2` = {{o:1708.2}} − {{o:1138.8}}𝐢 VA
:::

These are correct.
:::
:::

::: practice

::: problem AS7's Practice Problem 11.10
Calculate the power factor of the entire circuit as seen by the source. What
is the average power supplied by the source?

::: figure assets/circuit/as7pp1110.png
AS7's Practice Problem 11.10
:::

::: answer
The values are RMS, so {{v7,8|set `true→s\rms`}}{{v9|tick {{ui:RMS phasors}} in
{{card:Settings}}}}.

```sym 7
true→s\rms:"e,1,0,165.:r,1,0,10.+[𝐢4.,8.-𝐢6.]"→cir:s\ac(cir,ω)
```
```sym 8
true→userms:"e,1,0,165.:r,1,0,10.+[𝐢4.,8.–6.𝐢]"→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
e,1,0,165
r1,1,2,10
r2,2,0,4j
r3,2,3,8
r4,3,0,-6j
```

::: only 9
Written out as four elements rather than one, which is clearer and costs
nothing here. The average power supplied is the opposite of the power the
source consumes: `pe` reads {{o:-2007.1}} W, so the source supplies
{{o:2007.1}} W.

For the power factor, use {{card:Mini-Tools}} with *pf*, giving it the
source's name, so that the reading is of the circuit the source sees:

```field 9 Value
e
```
:::

```out 7,8
-pe gives 2007.1 W;  s\pf("e") gives pf: 0.93595 lagging
```

::: only 9
It reads {{o:0.93595}} **lagging**.
:::
:::
:::

::: problem AS7's Problem 11.97
A power transmission system is modelled as shown. If {{var:V_s}} = 240 V rms,
find the average power absorbed by the load.

::: figure assets/circuit/as7p1197.png
AS7's Problem 11.97
:::

::: answer
Three impedances in series: the outgoing line, the load, and the return path.

```sym 7
true→s\rms:"evs,1,0,240.:rl1,1,2,.1+𝐢:rl,2,3,100+𝐢:rl2,3,0,.1+𝐢"→cir:s\ac(cir,ω):prl
```
```sym 8
true→userms:"evs,1,0,240.:rl1,1,2,.1+𝐢:rl,2,3,100+𝐢:rl2,3,0,.1+𝐢"→cir:s\ac(cir,ω):prl
```
```field 9 Circuit Description
evs,1,0,240
rl1,1,2,.1+1j
rl,2,3,100+1j
rl2,3,0,.1+1j
```

::: only 9
AC with {{ui:RMS phasors}} ticked. The power consumed `prl` reads {{o:573.2}} W.
:::

```out 7,8
573.2 W
```

Correct.
:::
:::

::: problem AS7's Problem 11.75
Consider the power system shown. Calculate the total complex power, the power
factor, and the parallel capacitance needed for a unity power factor.

::: figure assets/circuit/as7p1175.png
AS7's Problem 11.75
:::

::: answer
Three loads in parallel across a 240 V rms source. The first two parts need no
frequency at all, so leave omega as anything.

```sym 7
true→s\rms:"e,1,0,240:r1,1,0,80-𝐢50:r2,1,0,120+𝐢70:r3,1,0,60+𝐢0"→cir:s\ac(cir,ω)
```
```sym 8
true→userms:"e,1,0,240:r1,1,0,80–𝐢50:r2,1,0,120+𝐢70:r3,1,0,60+𝐢0"→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
e,1,0,240
r1,1,0,80-50j
r2,1,0,120+70j
r3,1,0,60
```

**(a)** The complex power delivered is the opposite of the power the source
consumes: {{v7,8|`-se`}}{{v9|the opposite of `se`}} gives
{{o:1835.9}} − {{o:114.7}}j VA.

**(b)** The power factor, from {{v7,8|`s\pf("e")`}}{{v9|*pf* in {{card:Mini-Tools}}
given the source's name, `e`}}, is {{o:0.99805}} leading.

**(c)** This one needs a frequency, because it needs a capacitor. Add one in
parallel with a symbolic value (let's say x), and run at the stated 50 Hz —
(2π)(50) in rad/s.

```sym 7
"e,1,0,240:r1,1,0,80-𝐢50:r2,1,0,120+𝐢70:r3,1,0,60+𝐢0:c,1,0,x"→cir
s\ac(cir,2π50.)
solve(s\pf(se)=1.,x)
```
```sym 8
"e,1,0,240:r1,1,0,80-𝐢50:r2,1,0,120+𝐢70:r3,1,0,60+𝐢0:c,1,0,x"→cir
s\ac(cir,2π50.)
solve(s\pf(se)=1.,x)
```
```field 9 Circuit Description
e,1,0,240
r1,1,0,80-50j
r2,1,0,120+70j
r3,1,0,60
c,1,0,x
```
::: applink AS7's Problem 11.75 (c, trying a capacitor)
:::

::: only 9
Put `2*pi*50` in the {{ui:ω — angular frequency}} box — it takes an expression.
Give *pf* the complex power `se` now and it answers with an expression in
`x`: the power factor as a function of the capacitance, which is what the
calculator solved for 1. In version 9, ask the {{card:Solve}} card instead
for the value of `x` that leaves no reactive power, which is the same
condition:

```field 9 Equation(s) to solve in terms of the results
im(se) = 0
```

```field 9 Unknown(s) to solve for
x
```

Tick {{ui:real solutions only}}.
:::

```out 7,8
-6.3 μF
```

::: only 9
It answers {{o:-6.34}} µF.
:::

A negative capacitance, and no positive value satisfies the equation — which
is probably why the textbook gives no number for this part. It is not a
failure of the method: the load is *already* leading, as part (b) said, so no
capacitor can bring it to unity. What it needs is the opposite.

Try an inductor instead:

```sym 7
"e,1,0,240:r1,1,0,80-𝐢50:r2,1,0,120+𝐢70:r3,1,0,60+𝐢0:l,1,0,x"→cir
s\ac(cir,2π50.)
solve(s\pf(se)=1.,x)
```
```sym 8
"e,1,0,240:r1,1,0,80-𝐢50:r2,1,0,120+𝐢70:r3,1,0,60+𝐢0:l,1,0,x"→cir
s\ac(cir,2π50.)
solve(s\pf(se)=1.,x)
```
```field 9 Circuit Description
e,1,0,240
r1,1,0,80-50j
r2,1,0,120+70j
r3,1,0,60
l,1,0,x
```
::: applink AS7's Problem 11.75 (c, an inductor instead)
:::

```out 7,8
1.5987 H
```

::: only 9
Solving the same way gives {{o:1.5987}} H, which is positive and therefore
the real answer.
:::

Check it by putting that number back in as the inductor's value: the power
factor comes out {{o:1}}. An inductor of about 1.6 H in parallel is what
brings this system to unity.
:::
:::

:::
