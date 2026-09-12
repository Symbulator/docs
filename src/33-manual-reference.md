---
id: manual-reference
kind: manual
book: manual
title: Reference
versions: [9]
updated: 2026-09-11
summary: >
  Every element, every answer name, what each tool returns, every setting, and what a saved file remembers. Lookup, not reading.
---

## Elements

`name` first, then these, comma-separated. Italic fields are optional.

| | Element | Fields | Notes |
|---|---|---|---|
| **r** | resistor | `n1,n2,value` | value may be `[r,r,…]` in parallel |
| **l** | inductor | `n1,n2,value` *,i₀* | i₀ read by FD and TR |
| **c** | capacitor | `n1,n2,value` *,v₀* | v₀ read by FD and TR |
| **e** | voltage source | `n1,n2,value` | dependent if value names an answer |
| **j** | current source | `n1,n2,value` | current flows n1 → n2 inside it |
| **o** | ideal op amp | `n+,n−,nout` | a nullor; reports i and p, no v |
| **m** | mutual inductance | `Lname1,Lname2,M` | names two inductors; no answers |
| **s** | short circuit | `n1,n2` | |
| **t** | transformer | `n1,n2,t1,t2` | or `[tl,bl],[tr,br],[t1,t2]` |
| **z y h g a b** | two-port | `n1,n2` *,[p11,p12,p21,p22]* | or bracketed pairs |

Node `0` is ground. Names are letters, digits and underscores; the first
character picks the type.

## Answer names

Both spellings work everywhere: `ir1` and `i_r1`, `v2` and `v_2`. Case is
ignored.

| | | Where |
|---|---|---|
| `v<node>` | node voltage | all |
| `i<el>` | current, first node → second | all |
| `v<el>` | voltage drop, first minus second | all |
| `p<el>` | power consumed | all |
| `ap<el>` | average power | AC |
| `s<el>` | complex power, P + jQ | AC |
| `z<el>` | impedance seen | AC, FD |
| `r<el>` | resistance seen | DC |
| `i<el><node>` | terminal current | transformers, two-ports |

## SI prefixes

Apostrophe, then the letter. Exact, not decimal.

| | | | | | |
|---|---|---|---|---|---|
| `'P` 10¹⁵ | `'T` 10¹² | `'G` 10⁹ | `'M` 10⁶ | `'k` `'K` 10³ | |
| `'m` 10⁻³ | `'u` `'µ` 10⁻⁶ | `'n` 10⁻⁹ | `'p` 10⁻¹² | `'f` 10⁻¹⁵ | `'a` 10⁻¹⁸ |

Case matters everywhere but kilo. `8000` and `8'k` are exact; `8000.` and
`8E3` are approximate.

## Analyses

| | | |
|---|---|---|
| **DC** | steady state | ignores initial conditions |
| **AC** | one ω, phasors | needs an ω |
| **FD** | s-domain | initial conditions included |
| **TR** | time domain | answers in `t`, valid for t ≥ 0 |

## Tools and mini-tools

| Tool | Takes | Returns |
|---|---|---|
| Resistance / impedance | two nodes | `req` or `zeq` |
| Thévenin / Norton | two nodes | `vth`, `ino`, `req`, `pmax` |
| …with the load tick | | plus `irl`, `vrl`, `prl` |
| Two-port parameters | two nodes, a kind | four parameters of that kind |
| {{tool:pf}} | a complex power, or an element's name | power factor with lead/lag: of the value as given, or of the power the element delivers (a source) or consumes (an impedance) |
| {{tool:gain}} | parameters and a load | *G*ᵥ, *G*ᵢ, *G*ₚ, *Z*ᵢₙ |
| {{tool:aa}} | a complex value | amplitude and angle |

## Plots

| | Analysis |
|---|---|
| Plot a function of time | TR |
| Bode plot of a variable | FD |
| Bode plot of transfer function H(s) | none needed |
| Plot a variable against another | DC |

## Settings

| | Changes |
|---|---|
| **Rounding** — exact / exact+approx / approx to *n* / approx full | the display |
| **Show units** | the display |
| **Use SI prefixes in answers** | the display; forces off *exact* |
| **Show AC answers as polar phasors** | the display; AC only |
| **Show equations** | adds the Equations card |
| **RMS phasors** | **the answer.** AC only |

Full detail in {{ref:settings}}.

## What a saved file remembers

A `.cir` entry carries **32 fields**: the description, the analysis and its
settings, Define, Evaluate and its conditions, Solve, Expert Mode's three
boxes, the plot's five, the display settings, a note and an image. Saving
and reloading returns you to the run, not just the circuit.{{i:input files (.cir)}}
{{ref:input-files}} has the format.

## Outside the tool

Fourier series and transforms · convolution · energy · nonlinear devices ·
transmission lines · noise and tolerance analysis.{{i:Fourier series and transforms}}{{i:convolution}}{{i:energy}}{{i:nonlinear devices}}{{i:transmission lines}}{{i:noise and tolerance analysis}}

Supported but not automated, because each is something you do *to* the
circuit and then solve: superposition · source transformation ·
power-factor correction · pole-zero work · magnitude and frequency scaling.{{i:superposition}}{{i:source transformation}}{{i:power-factor correction}}{{i:poles and zeros}}
