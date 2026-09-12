import sys
import os

# --- paths, resolved from this file rather than hardcoded -------------------
# tools/nr12 -> tools -> Documentation -> the project root.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
DOCS = os.path.join(_ROOT, "Documentation")
EXAMPLES = os.path.join(_ROOT, "Application", "v9", "repos", "server", "examples")
PDF = os.path.join(_ROOT, "Other", "NR12.pdf")
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
# -*- coding: utf-8 -*-
"""The hand-written prose of the sampler chapter: front matter, opening, section heads."""

FRONT = """---
id: nr12-sampler
kind: back
title: Select problems from Nilsson & Riedel 12ed
versions: [9]
updated: 2026-09-12
summary: >
  Forty-three worked examples from *Electric Circuits*, each described in
  Symbulator and checked against the answer the book prints. DC, AC, TR and FD,
  with Expert Mode and symbolic answers where they earn their place.
---
"""

OPENING = """Nilsson and Riedel's *Electric Circuits* is the book a great many
engineers learned this material from, and its worked examples are unusually
well suited to showing what Symbulator is for: each one states a circuit,
states a question, and then prints the answer. That last part is what makes
this chapter checkable rather than merely illustrative — **every answer below
was compared against the number the book prints**, and the page says so
example by example.

The selection is deliberate. These are not the easiest problems in the book;
they are the ones where the distance between *describing a circuit* and
*solving it by hand* is widest — a delta that has to be transformed, a
supermesh, a dependent source whose controlling current is three steps away, a
transformer whose secondary floats, a switch that opens twice. The book meets
each with a method. Symbulator meets all of them with the same six words:
describe the circuit, choose an analysis.

::: note What this chapter is not
It is not a solutions manual, and it will not teach you circuit analysis.
Every example here is worked in full in the book itself, and the book's
derivation is the part worth reading — {{ref:lesson-dc}} onward is where
Symbulator is taught. This is a demonstration, aimed at someone who already
knows the material and wants to see what the software does with it.

The circuits are reproduced from *Electric Circuits*, 12th edition, by
James W. Nilsson and Susan A. Riedel (Pearson), and are the authors' and
publisher's property. For the purpose of teaching students how to use
Symbulator, these diagrams are reproduced under the principle of fair use. No
copyright infringement is intended.
:::

## How to read an entry {#nr12-how}

Each entry gives the book's question, the book's own figure, the Symbulator
description, the analysis to choose, and the answers. Where an answer is a
number it is quoted in prose, and the sentence says that it is the book's
number too. Where an answer is an *expression* — a function of *t*, a
transfer function in *s*, a formula in the circuit's own symbols — it is shown
in a results panel exactly as the app prints it.

Four things recur, and they are the reason these particular examples were
chosen:

- **A dependent source is a value, not a device.** Write `8*ir3` in a source's
  value field and the controlling current is named; there is no constraint
  equation to write and none to get wrong.
- **The case is never chosen by anyone.** Overdamped, critically damped and
  underdamped are the same three lines with different numbers, and the algebra
  decides which one comes out.
- **A symbol left in the circuit stays in the answer.** That is how a design
  problem gets checked, how a transfer function appears without being asked
  for, and how one run answers all three parts of a question.
- **{{card:Expert Mode}} turns a question inside out.** When the thing you know
  is an answer and the thing you want is a component value, state the answer as
  an equation and name the component as the unknown.

### Every circuit is in the app already {#nr12-entries}

Nothing here has to be typed. All forty-three circuits ship with Symbulator as
a built-in example book — open {{card:Built-in Examples}} and pick
*Nilsson & Riedel 12ed* from the list of books; the entries are named for the
example each one comes from, and each arrives with its note, its picture, its
settings, its Expert Mode fields and the analysis it wants already set.

Pick one, press {{btn:Run Symbulator}}, and the answers below are what you get.
{{ref:input-files}} explains what an entry remembers and how to save your own.
"""

INTROS = {
    "DC": """Sixteen resistive problems, and the running theme is that the book's
*method* — node voltages, mesh currents, source transformations, superposition,
a delta-to-wye — is a way of getting an answer by hand, not a property of the
answer. Symbulator is told the circuit and never told the method. Two of these
run in {{card:Expert Mode}}, and two are two-port problems.""",

    "TR": """Fourteen transient problems. The pattern is always the same and always
the one you would follow by hand: run the *t* < 0 circuit in DC to read the
capacitor voltages and inductor currents, put those numbers in the fifth field
of the `c` and `l` lines, and run the *t* ≥ 0 circuit in TR. No time constant
is ever computed, no solution form is ever selected, and a sequential-switching
problem is simply one more run.""",

    "AC": """Eight problems in the sinusoidal steady state. Impedances given in
ohms go in as they are written, complex ones included, and then the frequency
never enters — which is why several of these leave **omega** as a symbol.
Where the book gives henries and farads instead, the frequency goes in the
{{ui:ω — angular frequency}} box and the conversion is the solver's.""",

    "FD": """Five problems in the *s* domain. FD returns every answer as a function
of *s*, initial conditions included, which makes a transfer function nothing
more than the answer with the source left as a symbol. Nothing on this page is
labelled *filter* or *transfer function*, because nothing needs to be.""",
}
