---
id: manual-frequency
kind: manual
book: manual
title: The s-domain, transfer functions and plots
versions: [9]
updated: 2026-09-11
summary: >
  FD returns answers in s, which is where transfer functions come from. The t2s and s2t shortcuts, and all four plot types.
---

## FD

Choose **FD** and the answers come back as functions of *s*, initial
conditions included.{{i:frequency domain}}{{i:s-domain}}

```field 9 Circuit Description
e,1,0,vs
r,1,2,1'k
c,2,0,1'u
```

::: result voltage drop across c
v_{c} = \dfrac{1000\,vs}{s + 1000}
:::

Leave the source symbolic and the answer *is* the transfer function: divide
by `vs` and you have H(s) = 1000/(s + 1000), a first-order low pass with its
pole at −1000. Nothing is labelled "transfer function" because nothing
needs to be — it is the answer with the input left as a symbol.{{i:transfer function}}

Poles and zeros are then yours to take: factor the denominator, or hand the
expression to SymPy, which is what the answer already is.{{i:poles and zeros}}

## t2s and s2t

Two shortcuts convert an expression between the domains:{{i:t2s and s2t}}{{i:Laplace transform}}

```
t2s(10*exp(-1000*t))
s2t(1000/(s + 1000))
```

Curly brackets are shorthand for the same thing inside a value, so a source
may be written in *t* and used in an FD run.{{i:curly-bracket shorthand}}

## The four plots

The Plot card offers four, and which ones are available depends on the
analysis:{{i:plots (Plotting Tools card)}}

| Plot | Analysis | What it wants |
|---|---|---|
| **Plot a function of time** | TR | an answer name, and a time range |
| **Bode plot of a variable** | FD | an answer name, and a frequency range |
| **Bode plot of transfer function H(s)** | — | H(s) typed directly |
| **Plot a variable against another** | DC | two answer names, and a sweep range |

The third needs no circuit at all: type `1000/(s+1000)` and get its
magnitude and phase. Useful when the transfer function came from somewhere
else, or when you are checking a hand derivation.{{i:Bode plot of a transfer function H(s)}}

The fourth is a **DC sweep** — one answer plotted against another as a value
varies, which is how a load line or a maximum-power curve is drawn. Give it
the two names and a range.{{i:DC sweep plot}}

## Resonance

There is no resonance tool. Resonance is the frequency that clears the
reactance, so it is a {{card:Solve}} problem: take the impedance answer,
set its imaginary part to zero, and solve for ω. The same works for
half-power points, which makes bandwidth and *Q* two more lines of algebra
rather than a feature.{{i:resonance}}

::: tip Filters are just circuits
There is nothing filter-shaped in Symbulator. Describe the circuit, run FD,
and read the transfer function; run the Bode plot to see it. A passive
filter and an active one differ only by having an `o` in them.{{i:filters}}
:::
