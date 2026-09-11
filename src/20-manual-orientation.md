---
id: manual-orientation
kind: manual
book: manual
title: What Symbulator is
versions: [9]
updated: 2026-09-11
summary: >
  A symbolic solver for linear circuits. What it does, what it refuses, and the nine things a circuits course covers that it will not.
---

Symbulator solves linear electric circuits symbolically. You describe the
circuit as text, choose an analysis, and get every current, voltage and power
in it — as exact expressions, not decimals, unless you ask otherwise.

It is not SPICE. There is no netlist to compile, no convergence to tune, no
timestep. A circuit is a handful of lines, and the answer comes back as
algebra you can read.

## What it solves

Four analyses, on the same description:

| | |
|---|---|
| **DC** | direct current, steady state |
| **AC** | sinusoidal steady state at one ω, in phasors |
| **FD** | the s-domain, initial conditions included |
| **TR** | transient, in the time domain |

Fifteen element types, listed in {{ref:manual-grammar}}. Four tools that
answer a question about a circuit rather than solving it outright:
equivalent resistance, Thévenin/Norton, two-port parameters, and gain.

Every value may be a symbol. That is the point of the thing: leave `r1` as
`r1` and the answer comes back in terms of `r1`.

## What it will not do

Linear circuits only, lumped elements only. Nine topics from a first course
in circuits fall outside it, and it is cheaper to say so here than to have
you hunt:

- **Fourier series and transforms.** Not implemented.
- **Convolution.** Not implemented.
- **Energy.** You get power; integrating it is yours.
- **Nonlinear devices.** No diode curve, no transistor model. A transistor
  enters as its small-signal equivalent, which is linear, and works.
- **Transmission lines**, and anything distributed.
- **Noise, tolerance, Monte Carlo.** Not a statistical simulator.

Four more are supported but not automated — **superposition**, **source
transformation**, **power-factor correction** and **pole-zero work**. Each
is a thing you do to the circuit, then solve. No tool does it for you.

## Where it runs

Three builds of one interface, and they behave identically:

| | |
|---|---|
| **Online** | `symbulator.pythonanywhere.com` — nothing to install |
| **In your browser, offline** | `install.symbulator.com` — installs as an app |
| **On your machine** | `symbulator.com/9/local.zip` — a folder and a launcher |

The solver is also a Python package: `pip install symbulator`.
