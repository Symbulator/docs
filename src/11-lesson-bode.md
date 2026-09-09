---
id: lesson-bode
kind: lesson
title: Bode plots and resonance
versions: [7, 9]
updated: 2026-08-27
absent_note: >
  Symbulator 8 has no Bode plotter. The Nspire's own graphing tools will plot a
  transfer function once you have it, and finding the transfer function itself
  is covered in the lesson on the complex frequency domain.
summary: >
  Learn to do gain and phase *Bode plots* for transfer functions of ω and s
  with the **bode** tool. Find the *resonant frequency* of an answer by solving
  for the frequency at which the reactance vanishes.
---

Two things that only make sense across a range of frequencies rather than at
one: the Bode plot, which draws a transfer function's gain and phase as
frequency sweeps, and resonance, which is the one frequency where a circuit's
reactance vanishes.

## Do Bode plots {#bode-plot}

A Bode plot shows the gain and the phase of a transfer function against
frequency, on a logarithmic axis.{{i:Bode plot}}

::: only 7
The tool is called **s\bode**, and it does two kinds of plot: gain plots (also
called magnitude or H(dB) plots) and phase plots. They are as good as you can
expect on a TI-89.

You invoke it by entering:

```sym 7
s\bode()
```

::: figure assets/screen/bode01.jpeg
The bode tool's menu
:::

The second option, **2: Clean & Exit**, clears the variables the tool created
while plotting. Use it when you are done. There is nothing more to say about
it.

The first option, **1: Bode Plot**, takes you to a screen with these fields:

::: figure assets/screen/bode02.jpeg
The bode tool's fields
:::

- **Transfer function** — the expression you want plotted, typed directly or
  as the name of the variable holding it. It must be a function of a single
  independent variable, and that variable must be either `s` or `ω`.
- **Plot type** — a gain plot, a phase plot, or both.
- **Minimal frequency** — the lowest frequency on the plot. It cannot be 0.
  Try 1, or 0.1, depending on the circuit.
- **Maximal frequency** — the highest, which must be larger than the minimum.
- The **unit** the two frequencies are given in.

Press Enter and Symbulator generates one or two expressions, stores them in
`y1(x)` and `y2(x)`, and plots them. Your independent variable has been
replaced by `x` at that point, so every graph option — minimum, maximum, zero,
trace — works normally. Just remember that `x` means your variable.
:::
::: only 9
Symbulator draws it in the {{card:Plotting Tools}} card below the results. Solve
the circuit first, then set **Plot type** to *Bode plot of a variable (FD)*;
the two time boxes become frequencies.

```field 9 Circuit Description
e,1,0,1
r1,1,2,1000
c1,2,0,1e-6
```

- {{ui:Variable to plot}}: `v2`
- {{ui:Start frequency (Hz)}} and {{ui:End frequency (Hz)}}: 10 and 100000
- {{ui:Points}}: 300

Both curves appear together, magnitude in decibels above and phase in degrees
below. For this low-pass RC that is the rolloff you would expect: flat at low
frequency, falling 20 dB per decade after the corner, with the phase heading
for −90°.

::: warning The variable, not an expression
The box takes an answer's *name*, as {{card:Results}} spells it, not a formula. A
formula belongs in the transfer-function plot type, next.

Solving in AC and plotting against frequency would not work: an AC result is
one phasor at one ω. The plot re-solves the circuit at every frequency.
:::

### When you have H(s) itself

The textbook often hands you the transfer function and no circuit. Symbulator
takes it directly: set **Plot
type** to *Bode plot of a transfer function H(s) (FD)*, and the variable box
becomes {{ui:Transfer function H(s)}}. Type the function there; the Circuit
Description is ignored for this plot type, so it works on an empty page.

- Write the function **in terms of `s`**. A textbook function of jω becomes
  one of s by writing `s` wherever jω appears — a Bode plot sweeps the
  imaginary axis, where s *is* jω.
- The expression takes the same shorthand a circuit value does — `^` for
  powers, implied multiplication, `1'k` — and it must be numeric apart from
  `s`. A leftover symbol is refused by name.
- The frequency boxes are in **hertz**. The examples in this
  lesson give their ranges in rad/s; divide by 2π for the same sweep in Hz
  (0.1 to 300 rad/s is about 0.016 to 48 Hz).
:::

::: practice

::: problem AS7's Example 14.3
Construct the Bode plots for the given transfer function.

$$
H(\omega) = \dfrac{200\,j\omega}{(j\omega + 2)(j\omega + 10)}
$$

::: only 7
We write the expression using the character the calculator understands for the
imaginary operator — 𝐢, rather than the textbook's j. In my experience it pays
to type it outside the tool first, where you can see it clearly:

::: figure assets/screen/as71403s1.jpeg
The expression, typed outside the tool
:::

When I'm happy with it I copy it to the clipboard, run `s\bode()`, and paste
it into the field. Gain Plot as the type, 0.1 as the minimum frequency and 100
as the maximum, *in rad/sec* as the unit. Press Enter.

I wanted to see more of the plot to the right, so I pressed HOME and ran the
tool again — the previous values are still there, so only the maximum needs
changing. 300 gives a better-looking plot.

Press **F5** and choose **4:Maximum**, then pick bounds around the peak:

::: figure assets/screen/as71403s2.jpeg
Finding the maximum
:::

There is a maximum gain of 24.4 at x = 0.65052 — and since x is the logarithm
of the frequency, that is 10^0.65052 = 4.47 rad/s.

Press F5 again and choose the zero option, with bounds around where the line
crosses the axis:

::: figure assets/screen/as71403s3.jpeg
Finding the zero
:::

That is x = 2.3005, so 10^2.3005 = 199.8 rad/s.

Now the phase plot. Run the tool again and ask for a Phase plot:

::: figure assets/screen/as71403s4.jpeg
The phase plot
:::

The Zero option works here too, and shows the phase passing through zero
exactly where the gain is at its maximum:

::: figure assets/screen/as71403s5.jpeg
Phase zero at the gain peak
:::
:::
::: only 9
Symbulator takes the expression directly: set **Plot
type** to *Bode plot of a transfer function H(s) (FD)* and type the problem's
function into the box, writing `s` wherever the textbook writes jω — no
imaginary operator involved. The frequency boxes are in hertz, so the
sweep of 0.1 to 300 rad/s is about 0.016 to 48 Hz.

```field 9 Transfer function H(s)
200*s/((s+2)*(s+10))
```

- {{ui:Start frequency (Hz)}} and {{ui:End frequency (Hz)}}: 0.016 and 48

::: figure assets/plot/as7e1403-bode.png
AS7's Example 14.3: the Bode plot Symbulator draws
:::

Reading the answers off the curve: the maximum of {{o:24.4}} dB at 4.47 rad/s
sits near 0.71 Hz, and the zero crossing at 199.8 rad/s near 31.8 Hz.
:::
:::

::: problem AS7's Practice Problem 14.3
Draw the Bode plots for the given transfer function.

$$
H(\omega) = \dfrac{5\,(j\omega + 2)}{j\omega\,(j\omega + 10)}
$$

::: only 7
Solved exactly as the one above. I used 0.1 and 100 as the minimum and maximum
frequencies. This is the gain plot:

::: figure assets/screen/as7pp1403s1.jpeg
The gain plot
:::

And this is the phase plot:

::: figure assets/screen/as7pp1403s2.jpeg
The phase plot
:::
:::
::: only 9
The transfer-function plot type again: write the function in terms of `s`
and sweep. The sweep of 0.1 to 100 rad/s is about 0.016 to 16 Hz.

```field 9 Transfer function H(s)
5*(s+2)/(s*(s+10))
```

- {{ui:Start frequency (Hz)}} and {{ui:End frequency (Hz)}}: 0.016 and 16

::: figure assets/plot/as7pp1403-bode.png
AS7's Practice Problem 14.3: the Bode plot Symbulator draws
:::
:::
:::

::: problem AS7's Example 14.4
Construct the Bode plots for the given transfer function.

$$
H(\omega) = \dfrac{j\omega + 10}{j\omega\,(j\omega + 5)^{2}}
$$

::: only 7
Same as above. This is the gain plot:

::: figure assets/screen/as7e1404s1.jpeg
The gain plot
:::

And this is the phase plot:

::: figure assets/screen/as7e1404s2.jpeg
The phase plot
:::
:::
::: only 9
Solved the same way: the *Bode plot of a transfer function H(s) (FD)* type, with
the function written in terms of `s`.

```field 9 Transfer function H(s)
(s+10)/(s*(s+5)^2)
```

- {{ui:Start frequency (Hz)}} and {{ui:End frequency (Hz)}}: 0.016 and 16

::: figure assets/plot/as7e1404-bode.png
AS7's Example 14.4: the Bode plot Symbulator draws
:::
:::
:::

::: problem AS7's Practice Problem 14.4
Construct the Bode plots for the given transfer function.

$$
H(\omega) = \dfrac{50\,j\omega}{(j\omega + 4)(j\omega + 10)^{2}}
$$

::: only 7
Same as above, so this time let us do both plots together — the tool will draw
gain and phase in one go:

::: figure assets/screen/as7pp1404s1.jpeg
Both plots together
:::
:::
::: only 9
Symbulator always draws both, magnitude above and phase below, so there is nothing extra to
ask for.

```field 9 Transfer function H(s)
50*s/((s+4)*(s+10)^2)
```

- {{ui:Start frequency (Hz)}} and {{ui:End frequency (Hz)}}: 0.016 and 16

::: figure assets/plot/as7pp1404-bode.png
AS7's Practice Problem 14.4: the Bode plot Symbulator draws
:::
:::
:::

::: problem AS7's Example 14.5
Draw the Bode plots for the given transfer function.

$$
H(s) = \dfrac{s + 1}{s^{2} + 12s + 100}
$$

::: only 7
To be sure of typing it clearly, write the expression outside the tool first:

::: figure assets/screen/as7e1405s1.jpeg
The expression
:::

Gain Plot, 0.1 as the minimum frequency and 100 as the maximum, *in rad/sec*
as the unit. Press Enter and we get this:

::: figure assets/screen/as7e1405s2.jpeg
The gain plot
:::

Now the phase. Press HOME, run the tool again, and ask for a Phase plot:

::: figure assets/screen/as7e1405s3.jpeg
The phase plot
:::
:::
::: only 9
The same transfer-function type, and this one is already written in `s`. If a
symbol other than `s` slips in, the error names it.

```field 9 Transfer function H(s)
(s+1)/(s^2+12*s+100)
```

- {{ui:Start frequency (Hz)}} and {{ui:End frequency (Hz)}}: 0.016 and 16

::: figure assets/plot/as7e1405-bode.png
AS7's Example 14.5: the Bode plot Symbulator draws
:::
:::
:::

::: problem AS7's Practice Problem 14.5
Draw the Bode plots for the given transfer function.

$$
H(s) = \dfrac{10}{s\,(s^{2} + 80s + 400)}
$$

::: only 7
Solved the same way as the one above, so there is nothing new to show. Let me
use it instead to demonstrate plotting gain and phase together:

::: figure assets/screen/as7pp1405s1.jpeg
Gain and phase together
:::
:::
::: only 9
Nothing new here either: the transfer-function type, the function written in
terms of `s`, both curves drawn together.

```field 9 Transfer function H(s)
10/(s*(s^2+80*s+400))
```

- {{ui:Start frequency (Hz)}} and {{ui:End frequency (Hz)}}: 0.016 and 16

::: figure assets/plot/as7pp1405-bode.png
AS7's Practice Problem 14.5: the Bode plot Symbulator draws
:::
:::
:::

:::

## Resonance {#resonance}

The resonant frequency is the one at which a circuit's reactance vanishes —
where the impedance the source sees becomes purely real.{{i:resonance}}

::: only 7
There is no dedicated tool. You solve the circuit symbolically in ω and then
put the condition to the calculator's **Numeric Solver** (APPS, then 9), or to
**nSolve**.
:::
::: only 9
There is no dedicated tool, and none is needed: solve the circuit in AC with
`w` in the {{ui:ω — angular frequency}} box, then put the condition to the {{card:Solve}} card.

Two things make it work, and both are easy to leave out:

- **Tick *real solutions only*.** Solving `im(ze) = 0` over the complex field returns
  answers written in terms of `re(w)` and `im(w)` rather than `w` — useless.
  Declaring the unknown real is what makes it solvable.
- **Add `w > 0` as a condition.** The algebra gives ± the frequency, and only
  one of the two is a frequency.
:::

::: practice

::: problem AS7's Example 14.7
Find the resonance frequency ω{{sub:0}} and the bandwidth frequencies
ω{{sub:1}} and ω{{sub:2}}.

::: figure assets/circuit/as7e1407.png
AS7's Example 14.7
:::

::: answer
```sym 7
"e,1,0,20.:r,1,2,2.:l,2,3,1.'m:c,3,0,.4'μ"→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
e,1,0,20
r,1,2,2
l,2,3,1'm
c,3,0,.4'u
```

::: only 7
In the Numeric Solver's **eqn** field, enter `abs(ze)=real(ze)`. It offers an
interval for ω from −1ᴇ14 to 1ᴇ14; since there is no negative frequency here,
change the lower bound to 0:

::: figure assets/screen/as7e1407s1.jpeg
The Numeric Solver, ready
:::

With the cursor in the blank next to ω=, press **F2 Solve**:

::: figure assets/screen/as7e1407s2.jpeg
The resonant frequency
:::

So ω{{sub:0}} is 50000 rad/s. For ω{{sub:1}}, the lower bandwidth
frequency, change the equation and the bounds:

::: figure assets/screen/as7e1407s3.jpeg
Set up for the lower bandwidth frequency
:::

::: figure assets/screen/as7e1407s4.jpeg
ω1
:::

ω{{sub:1}} is 49010 rad/s. For the upper one, change the bounds again:

::: figure assets/screen/as7e1407s5.jpeg
Set up for the upper bandwidth frequency
:::

::: figure assets/screen/as7e1407s6.jpeg
ω2
:::

ω{{sub:2}} is 51010 rad/s.
:::
::: only 9
Put `w` in the ω box and solve in AC. Then, in the {{card:Solve}} card:

```field 9 Equation(s) to solve in terms of the results
im(ze) = 0
```

```field 9 Unknown(s) to solve for
w
```

```field 9 Conditions
w>0
```

with {{ui:real solutions only}} ticked. It gives ω{{sub:0}} = {{o:50000}} rad/s.

The bandwidth frequencies are the half-power points, where the impedance
magnitude is √2 times its resistance. Same circuit, different equation:

```field 9 Equation(s) to solve in terms of the results
abs(ze) = sqrt(2)*2
```

With the condition `w<50000` that gives ω{{sub:1}} = {{o:49010}} rad/s, and
with `w>50000` it gives ω{{sub:2}} = {{o:51010}} rad/s.
:::

All three are correct.
:::
:::

::: problem AS7's Example 14.8
Find the resonance frequency and the bandwidth frequencies.

::: figure assets/circuit/as7e1408.png
AS7's Example 14.8
:::

::: answer
```sym 7
"e,1,0,10:r,1,0,8'k:l,1,0,.2'm:c,1,0,8'μ"→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
e,1,0,10
r,1,0,8'k
l,1,0,.2'm
c,1,0,8'u
```

Trying the same equation as before does not go well here. The peak of
resonance is so sharp — a needle — that a numerical search struggles to find
its way to the solution. A different condition converges immediately: ask
instead for the frequency at which the source's current has no imaginary
part.

::: only 7
::: figure assets/screen/as7e1408s1.jpeg
imag(ie)=0 converges at once
:::

ω{{sub:0}} is 25000 rad/s. For ω{{sub:1}}, go back to the previous
example's equation and change the bounds:

::: figure assets/screen/as7e1408s2.jpeg
ω1
:::

ω{{sub:1}} is 24992.2 rad/s. And for ω{{sub:2}}:

::: figure assets/screen/as7e1408s3.jpeg
ω2
:::

ω{{sub:2}} is 25007.8 rad/s.
:::
::: only 9
```field 9 Equation(s) to solve in terms of the results
im(ie) = 0
```

with `w>0` and {{ui:real solutions only}}, giving ω{{sub:0}} = {{o:25000}} rad/s.

Symbulator 9 solves this symbolically rather than by searching, so the sharp
peak costs it nothing. The alternative equation is still worth knowing: at
resonance the source sees a purely real load, so its current is in phase with
its voltage.
:::
:::
:::

::: problem AS7's Example 14.9
Determine the resonant frequency ω{{sub:0}} of the circuit.

::: figure assets/circuit/as7e1409.png
AS7's Example 14.9
:::

::: answer
```sym 7
"j,0,1,1:c,1,0,.1:r1,1,0,10:l,1,2,2:r2,2,0,2"→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
j,0,1,1
c,1,0,.1
r1,1,0,10
l,1,2,2
r2,2,0,2
```

This time, look for the frequency at which the imaginary part of the voltage
at node **1** vanishes.

```sym 7
nSolve(imag(v1)=0,ω)|ω>0
```

::: only 9
```field 9 Equation(s) to solve in terms of the results
im(v1) = 0
```

with `w>0` and {{ui:real solutions only}}.
:::

ω{{sub:0}} is {{o:2}} rad/s. Correct.
:::
:::

:::
