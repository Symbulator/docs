---
id: lesson-bode
kind: lesson
title: Bode plots and resonance
versions: [7, 9]
updated: 2023-07-08
absent_note: >
  Symbulator 8 has no Bode plotter. The Nspire's own graphing tools will plot a
  transfer function once you have it, and finding the transfer function itself
  is covered in the lesson on the complex frequency domain.
summary: >
  Learn to do gain and phase *Bode plots* for transfer functions of ω and s
  with the **bode** tool. Find the *resonant frequency* of an answer with the
  Numeric Solver and the nSolve command.
---

TODO: convert this lesson from docs-page7.

## Do Bode plots {#bode-plot}

TODO. A Bode plot shows the gain and the phase of a transfer function against
frequency, on a logarithmic axis.{{i:Bode plot}}

::: only 7
The tool is called **s\bode**.
:::
::: only 9
Symbulator 9 draws it for you. Solve the circuit first, then open the
**Plot** card and set **Plot type** to *Bode plot (magnitude & phase vs.
frequency)*. The two time boxes become frequency boxes:

```field 9 Circuit Description
e1,1,0,1
r1,1,2,1000
c1,2,0,1e-6
```

- **Variable to plot**: `v_2`
- **Start frequency (Hz)** and **End frequency (Hz)**: 10 and 100000
- **Points**: 300

Both curves appear together, magnitude in decibels above and phase in
degrees below.
```out
f        = [10.0, 100.0, 1000.0, 10000.0, 100000.0]
mag_db   = [-0.02, -1.45, -16.07, -35.96, -55.96]
phase_deg = [-3.6, -32.14, -80.96, -89.09, -89.91]
```

That is the low-pass RC rolloff you would expect: flat at low frequency, then
falling 20 dB per decade, with the phase heading for −90°. Pass a larger `n`
for a smooth curve; 200 is the default.

::: warning Do not try to Bode-plot an ac() result
It is tempting to reach for an `ac` answer and plot it against frequency, but
an `ac` result is a phasor computed at one fixed ω — a single point, not a
function of frequency. There is nothing in it to sweep. `bode_samples` takes
the circuit description itself and re-solves it at every frequency, which is
why it needs the description rather than a result.
:::
:::

## Resonance {#resonance}

TODO. The resonant frequency is the frequency at which the imaginary part of
the impedance vanishes.
