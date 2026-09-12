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
was compared with the one the book prints.**

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
number it is quoted in a sentence; where it is an *expression* — a function of
$t$, a transfer function in $s$, a formula in the circuit's own symbols — it is
shown in a results panel, as the app prints it. Between the figure and the
description, a short paragraph says what the book does with the problem and
what Symbulator does instead: that paragraph is the reason the example is here.

**Every value on the page, in a panel or in a sentence, was compared with the
answer the book prints, and they agree.** Where the two are written differently
— the book rounds an amplitude, or asks for the current a source *supplies*
where Symbulator reports what it *consumes* — the entry's paragraph says so.

The names are the app's own. `i_r3` is the current through the element called
`r3`, `v_2` the voltage at node 2, `p_e` the power consumed by the source called
`e`, and `v_r6` the voltage across `r6`. The book names its quantities
differently — $i_o$, $v_o$, $V_{Th}$ — so each entry says which of the app's
answers is which of the book's.

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
    "DC": """Sixteen resistive problems. The running theme is that the book's
*method* — node voltages, mesh currents, source transformations, superposition,
a delta-to-wye transform — is a way of getting an answer by hand, not a property
of the answer. Symbulator is told the circuit and never told the method, so the
same kind of description serves whichever chapter a problem came from. Five of
these are op-amp problems with lettered parts, two run in {{card:Expert Mode}},
and the last two are two-port problems from the book's final chapter.""",

    "TR": """Fourteen transient problems, three of them from the book's Laplace
chapter. The pattern is the one you would follow by hand: run the circuit as it
was before the switch moved in DC, read off the capacitor voltages and inductor
currents, put those numbers in the fifth field of the `c` and `l` lines, and run
the circuit as it is afterwards in TR. No time constant is computed, no solution
form is selected, and sequential switching is simply one more run. The
Laplace-chapter problems are no different: TR transforms, solves and inverts,
so what the book does in $s$ the solver does out of sight.""",

    "AC": """Eight problems in the sinusoidal steady state. Where the book gives
its impedances in ohms they go in as written, complex ones included, and the
frequency never enters: **omega** is left as a symbol in the
{{ui:ω — angular frequency}} box and nothing depends on it. Where the book gives
henries and farads instead, the frequency goes in that box and the conversion to
impedance is the solver's. Two of the eight state their source in rms, and say
so in {{card:Settings}}.""",

    "FD": """Five problems in the $s$ domain. FD returns every answer as a
function of $s$, initial conditions included, so a transfer function is nothing
more than the answer with the source left as a symbol — two of these are exactly
that. Nothing on this page is labelled *filter* or *transfer function*, because
nothing needs to be. The book's other Laplace-chapter examples, the ones it
inverts back into time, are in the TR section above.""",
}
