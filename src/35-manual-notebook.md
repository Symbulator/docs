---
id: manual-notebook
kind: manual
book: manual
title: Symbulator in a notebook
versions: [9]
updated: 2026-09-20
summary: >
  The solver as a Python package, used from a Jupyter notebook: a circuit is a string, an answer is a SymPy expression, and the Evaluate and Solve cards are two functions. With the notebooks to start from.
---

The app and the package are one solver. What a card does to a circuit, a
cell in a notebook does, and the answers are the same ones.{{i:Jupyter notebook}}

What a notebook adds is Python. An answer is a SymPy expression, so it
substitutes, differentiates, plots, and goes on into the rest of a
calculation.

## Getting set up

On your own computer, in a terminal:{{i:Python package (pip install symbulator)}}

```text
pip install symbulator[notebook]
```

That brings JupyterLab, NumPy and Matplotlib with the package. On Google
Colab the package is not installed, and the notebooks below begin with a
cell that installs it there and does nothing anywhere else:{{i:Colab}}

```text
import sys
if "google.colab" in sys.modules:
    %pip install -q symbulator matplotlib
```

## A circuit is a string

The description is the one the {{card:Input File}} card takes, an element
to a line or the elements joined by colons. {{ref:manual-grammar}} has the
grammar.

```sym 9
from symbulator import dc, draw

divider = """
e1,1,0,12
r1,1,2,1'k
r2,2,0,2'k
"""
draw(divider)
```

`draw` shows the schematic under the cell, from the description alone, as
the app does. `dc` runs the analysis and returns every answer in the
circuit:

```sym 9
res = dc(divider)
res["v2"]
```

```out
8
```

Answers have the app's names. Either spelling finds an answer, `ir1` or
`i_r1`; the package stores the second.

```sym 9
res["ir1"], res["i_r1"], res["pr1"]
```

```out
(1/250, 1/250, 2/125)
```

The answers are exact because the values are, and a value may be a symbol,
as in the app:

```sym 9
sym = dc("e,1,0,vs:r1,1,2,ra:r2,2,0,rb")
sym["vr2"]
```

```out
rb*vs/(ra + rb)
```

Being SymPy, it takes a value for each symbol with `subs`:

```sym 9
sym["vr2"].subs({"vs": 10, "ra": 4000, "rb": 6000})
```

```out
6
```

The Rounding setting is `rounded`, which returns a copy and leaves the
exact answers alone:

```sym 9
res.rounded(4)["ir1"]
```

```out
0.004000
```

## The analyses

Each choice in {{ui:Analysis}} is a function, and each tool of
{{card:Find equivalent}} is one too. Nodes are given as strings.

| In the app | In a cell |
|---|---|
| *DC* | `dc(circuit)` |
| *AC*, with ω | `ac(circuit, omega=1000)` |
| *FD* | `fd(circuit)` |
| *TR* | `tr(circuit)` |
| *Thévenin / Norton* | `th(circuit, "2", "0")` |
| *Resistance / impedance* | `er(circuit, "1", "0")` |
| *Two-port parameters* | `port(circuit, "1", "3", "z")` |

In AC, `omega` is a number, a symbol's name such as `"w"`, or an expression.
The equivalent tools take `domain="ac"` and an `omega` the same way. An AC
answer is complex, and `polar` shows it as magnitude and angle:

```sym 9
from symbulator import ac, polar

rl = "e,1,0,10:r,1,2,50:l,2,0,0.05"
ac(rl, omega=1000)["ir"]
```

```out
0.1 - 0.1*I
```

```sym 9
polar(ac(rl, omega=1000)["ir"])
```

```out
0.1414∠-45.00°
```

A TR answer is a function of `t`, the symbol the answers use. Import it to
use the same one, and `at` substitutes a time by name:

```sym 9
from symbulator import tr, t

rc = "e,1,0,10:r,1,2,1'k:c,2,0,1'u"
tr(rc)["v2"]
```

```out
10 - 10*exp(-1000*t)
```

```sym 9
tr(rc).at("v2", t=0.001)
```

```out
6.32120558828558
```

The capacitor's voltage is the voltage of node 2, since its other end is
ground. That is how to read any voltage that a TR or FD result does not give.

**What TR and FD do not give.** A TR or FD result holds the node voltages and
the element currents, and nothing worked out from them: no element's voltage
drop and no element's power. DC and AC store both. TR and FD leave them out
because every answer stored costs an inverse Laplace transform, and these are
one subtraction and one product away from what is stored. The drop across an
element is the difference of the node voltages at its two ends, ground
counting as zero:{{i:voltage drops and powers in TR and FD}}

```sym 9
res = tr(rc)
res["v1"] - res["v2"]
```

```out
10*exp(-1000*t)
```

That is the voltage across `r`. The power it consumes is the drop times its
current, the rule DC uses for every element:

```sym 9
(res["v1"] - res["v2"]) * res["ir"]
```

```out
exp(-2000*t)/10
```

A source follows the same rule, and reads negative while it delivers:

```sym 9
res["v1"] * res["ie"]
```

```out
-exp(-1000*t)/10
```

::: warning Not in FD
In FD an answer is a transform, and the product of two transforms is not the
transform of a product: V(s)I(s) is the transform of a convolution, not of a
power. Take a power in TR, or in AC, where it is stored.
:::

A Thévenin equivalent comes back with its four answers as attributes:

```sym 9
from symbulator import th

eq = th("e,1,0,20:r1,1,2,50:r2,2,0,150", "2", "0")
eq.vth, eq.z, eq.ino, eq.pmax
```

```out
(15, 75/2, 2/5, 3/2)
```

## The Evaluate and Solve cards

Once a circuit is solved, the app lets you write an expression in its
answers, and solve an equation in them. Those are two functions,
`evaluate` and `solve`, and they take the result of any analysis above.{{i:evaluate() and solve()}}

```sym 9
from symbulator import evaluate, solve

res = dc("e1,1,0,vs:r1,1,2,1'k:r2,2,0,1'k")
evaluate(res, "v2/vs")
```

```out
1/2
```

{{card:Evaluate}} in the app has a Conditions box, and here it is
`conditions`. An equation there gives a name a value while the expression
is worked out:

```sym 9
evaluate(res, "v2", conditions=["vs = 10"])
```

```out
5
```

A voltage drop that the result does not hold is the difference of two node
voltages, and it goes into an expression as one. The resistance of `r`, from
its drop and its current, in TR:

```sym 9
evaluate(tr(rc), "(v1 - v2)/ir")
```

```out
1000
```

The tools' own answers work the same way. A Thévenin result also answers to
the load's `irl`, `vrl` and `prl`, in the variable `load`, and a matched
load draws the maximum power:

```sym 9
evaluate(eq, "prl", conditions=["load = req"])
```

```out
3/2
```

{{card:Solve}} is `solve`. It substitutes the answers first, solves for
whatever is left, and returns a list of solutions, each a dictionary:

```sym 9
solve(res, ["v2 = 6"], ["vs"])
```

```out
[{'vs': 12}]
```

`conditions` pins a symbol when it is an equation and filters the roots when
it is a comparison, and `real_only=True` keeps real solutions only. A series
circuit's resonance is where the source sees no reactance, with ω left as
the symbol `w`:

```sym 9
res = ac("e,1,0,20:r,1,2,2:l,2,3,1'm:c,3,0,.4'u", "w")
solve(res, ["im(ze) = 0"], ["w"], conditions=["w > 0"], real_only=True)
```

```out
[{'w': 50000.0000000000}]
```

A value the {{card:Define}} card gives is a condition here, in `dc`, `ac`,
`fd` or `tr` as much as in `evaluate`.

## Expert Mode

The three boxes of {{card:Expert Mode}} are the three keywords `equations`,
`unknowns` and `conditions`, on any of `dc`, `ac`, `fd` and `tr`:

```sym 9
design = dc("e1,1,0,12:r1,1,2,4'k:r2,2,0,r_b",
            equations=["v_2 = 6"], unknowns=["r_b"])
design["r_b"]
```

```out
4000
```

Inside an equation, write an answer as the package stores it, with its
underscore: `v_2`, `p_jd1`. The shorter spelling often works too, but a name
such as `re` is SymPy's own function for the real part, and no rule of the
package can tell the two apart. {{ref:manual-symbols}} has Expert Mode.

## Cell magics

`%load_ext symbulator` adds a cell magic for each analysis: `%%dc`, `%%ac`,
`%%fd` and `%%tr`. A cell that starts with one is a circuit, an element to
a line, exactly as the input card takes it:

```sym 9
%load_ext symbulator
```

```sym 9
%%dc into=magic nodraw
e1,1,0,5
r1,1,2,1'k
r2,2,0,1'k
```

The cell draws the circuit and shows every answer, and `into` binds the
result to a name:

```sym 9
magic["v2"]
```

```out
5/2
```

Options go on the magic's line: `omega=1000` for `%%ac`, `rms`,
`variables=v_2,i_r1` to limit a transient, `into=` and `nodraw`.

## Plotting

SymPy plots a transient as it is, with Matplotlib behind it:

```sym 9
import sympy as sp

sp.plot(tr(rc)["v2"], (t, 0, 0.005),
        xlabel="t (s)", ylabel="v2 (V)");
```

`bode_samples` and `time_samples` return arrays for a frequency response or a
time response, for Matplotlib to draw. The monograph's notebook below uses
the first for the 1999 amplifier.

## Notebooks to start from

Each is already executed, so you can read the answers before you run
anything, and each opens in Google Colab. They are made from the app's own
example files, and every answer in them has been compared with the app's.

| Notebook | What is in it |
|---|---|
| [Quick start](https://colab.research.google.com/github/Symbulator/solver/blob/main/notebooks/quickstart.ipynb) | The package in a few cells, from a circuit to a plot. |
| [Claude's sampler](https://colab.research.google.com/github/Symbulator/solver/blob/main/notebooks/books/Showcase.ipynb) | The app's twelve showcase entries, one of each kind of analysis. |
| [A Baker's Dozen](https://colab.research.google.com/github/Symbulator/solver/blob/main/notebooks/books/Bakers_Dozen.ipynb) | Thirteen solved examples that look like an afternoon's work by hand. |
| [The Manual's circuits](https://colab.research.google.com/github/Symbulator/solver/blob/main/notebooks/books/Manual.ipynb) | Every circuit of this Manual, run, with its printed answer beneath. |
| [The monograph's exemplars](https://colab.research.google.com/github/Symbulator/solver/blob/main/notebooks/the_monograph.ipynb) | The exemplar circuits of *The Internal Logic of Symbulator*. |
| [Alexander & Sadiku](https://colab.research.google.com/github/Symbulator/solver/blob/main/notebooks/books/Alexander_Sadiku.ipynb) and [Nilsson & Riedel](https://colab.research.google.com/github/Symbulator/solver/blob/main/notebooks/books/Nilsson_Riedel.ipynb) | The two textbook samplers. |

The Course's own problems are there as well, one notebook to a lesson; the
folder on [GitHub](https://github.com/Symbulator/solver/tree/main/notebooks/books)
has them all.

## What stays in the app

The {{card:Numerical Solver}} is a page of the app and has no function in the
package. SPICE has two, `to_spice` and `from_spice`, for the
{{card:SPICE Translator}}'s two directions. The schematic is `draw`, and
`to_svg` returns it as text.

::: warning `t` is nonnegative
The symbol `t` is declared nonnegative, because a transient answer is only
valid for *t* ≥ 0. A limit taken through zero is the first place that
surprises. Import it, `from symbulator import t, s`, and every answer's
symbol is the one you hold.
:::
