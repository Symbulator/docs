---
id: introduction
kind: front
title: Introduction
updated: 2026-08-26
summary: >
  Learn about Symbulator and how it can help you focus on learning how circuits
  work, instead of struggling with math. Get the latest version of Symbulator
  and get ready to roll.
---

## What is Symbulator {#what-is-symbulator}

Symbulator is a program to solve linear electric circuits symbolically and
numerically {{v7,8|in a calculator}}{{v9|on your device}}. It accepts inputs
with numerical and symbolic values, and provides numerical and symbolic
results. The name is a portmanteau of *"symbolic simulator"*.
Symbulator is widely regarded as the best symbolic simulator of linear
electric circuits ever made for a {{v7,8|calculator.}}{{v9|handheld device.}}

### What analyses can it do?

Symbulator can solve circuits using four types of analysis: direct current (DC), alternating current (AC), transient time-domain (TR), and complex
frequency-domain (FD). Symbulator can analyse numerical and, more importantly, symbolic linear
circuits. It will return the voltages in all nodes, and the currents, voltage
drops and power in all elements. Symbulator can also find the passive, Thévenin, Norton and two-port equivalent of a
circuit. It can do time domain{{!v8| and Bode}} plots.

### What elements does it accept?

Symbulator accepts elements such as resistors, inductors, mutual inductance,
capacitors, independent and dependent current and voltage sources, ideal
operational amplifiers, ideal transformers and six types of two-ports.

### Where does it run?

::: only 7
Released in 2023, Symbulator 7 is written for the TI-89 Titanium
calculator by Texas Instruments, like all its predecessors, and runs in all compatible devices, like the
Voyage 200 and the classic TI-89. There is a version for the TI-Nspire
CX II CAS called version 8, and a newer Python/SymPy port called version 9.
:::
::: only 8
Released in 2023, Symbulator 8 is adapted to run on the TI-Nspire CX II CAS calculator by
Texas Instruments. There is also a version for the TI-89 Titanium called
version 7, and a newer Python/SymPy port called version 9.
:::
::: only 9
Released in 2026, Symbulator 9 is a port of the classic TI-Basic code to run in Python with the SymPy computer algebra library.
It runs anywhere Python runs: your mobile phone, your tablet, your laptop, a Jupyter notebook, or a browser on any computer.
Since it is not bound by the memory of a calculator, it solves circuits faster than versions 7 and 8.
:::

## Why use Symbulator? {#why-use-it}

Symbulator is extremely useful in solving a wide variety of circuit theory
problems, such as those faced by engineering students in Circuits I and II classes. It allows the student to focus on the conceptual
understanding of circuit analysis, rather than the mathematical techniques used
for their solution.

### Strengths

- A fantastic tool when you need a symbolic approach to solve a small or medium sized circuit composed of ideal, linear elements.
- Useful whenever you have to solve circuits with symbolic values, or when you need symbolic results.
- Offers the simplest way to define dependent sources.
- Includes special elements such as ideal transformers and six different two-ports, often not included in other simulators.

### Limitations

- Since it is a linear circuit simulator, Symbulator does not simulate non-linear elements, such as diodes and transistors.
- Symbulator will not help you answer problems that rely on applying formulas selectively, as opposed to solving a circuit completely.
- Finally, a simulator is not a replacement for your brain or an excuse to not study your circuit theory classes: you must understand circuit theory to use it.

### Symbulator is free!

You do not have to pay anything to use Symbulator. It has always been free of
cost, and always will be. *(You are welcome!)*

Since 2026, Symbulator is open source under the MIT licence. You are free to use it,
change it and port it to other platforms; all the licence asks is that the
copyright notice and the attribution travel with it.

::: only 7
## Download {#download}

### Symbulator

The latest version of Symbulator for the TI-89 platform is version 7 (date
stamp **08 July 2023**). We believe it is free of bugs, but if any is found, we
will revise and reupload, updating the date stamp. You can use it in the TI-89
Titanium and the Voyage 200.

To get Symbulator 7, download this file:
**[s7.tig](https://symbulator.com/7/s7.tig)**, which you will
transfer to your calculator.

### DiffEq

Since the CAS in the TI-89 Titanium does not do Laplace transforms, Symbulator
relies for that on a software called DiffEq, made by my friend Lars
Frederiksen.

To get DiffEq, download this file:
**[diffeq.zip](https://symbulator.com/7/diffeq.zip)**. From that
zip file you need to extract a file called *diff206.89g*, which you then
transfer to your calculator.
:::

::: only 8
## Download {#download}

### Symbulator

The version of Symbulator for the TI-Nspire CX II CAS is called version 8 beta
(date stamp **08 July 2023**). It may still contain the occasional bug. As bugs
are discovered and fixed, we will revise and reupload the program, updating the
date stamp.

To get Symbulator 8, download this file:
**[s.tns](https://symbulator.com/8/s.tns)**, transfer it to your
calculator, and refresh the libraries.

### Laplace Functions

Since the CAS in the TI-Nspire CX II CAS does not do Laplace transforms,
Symbulator relies for this on another software, which I call Laplace Functions.

This software was made, around the same time Symbulator was being created, by
my friend Lars Frederiksen, one of the most gifted programmers for TI-Basic
ever. Lars made two programs for the TI-92+/Voyage and the TI-89: one he called
DiffEq, a reference to the fact that it also solves differential equations, and
the other Advanced Laplace, which packed improved versions of his Laplace
functions.

The latter was automatically adapted for the TI-Nspire by Philippe Fortin, who
renamed the group of functions ETS_specfunc. Since I am not a fan of that name,
and given my friendship and collaboration with Lars, I have taken the liberty
of renaming the file here to **LF**, which in my eyes stands both for Laplace
Functions and for Lars Frederiksen.

Download **[lf.tns](https://symbulator.com/8/lf.tns)**, transfer
it to your calculator, and refresh the libraries.

### Solved problems

I have solved all the problems in this documentation, each in a separate
TI-Nspire document. This zip file,
**[problems.zip](https://symbulator.com/8/problems.zip)**,
contains three hundred solved problems.
:::

::: only 9

## Get Symbulator {#download}

You can use Symbulator 9 in two ways: as an online app or as a local app. 
To get started, go to the online app, **[here](https://symbulator.pythonanywhere.com/)**. At the bottom of that online app you will find the instructions on how to install a local version of it so you can run Symbulator 9 locally.

:::

::: danger Use at your own risk!
Every effort has been made in the development of this software, and there are
no known bugs in it. However, Symbulator is provided "as is", without warranty
of any kind, express or implied, including but not limited to the warranty of
fitness for a particular purpose. Every time you use Symbulator, you do so at
your own risk.

If you have any problems downloading, installing or executing Symbulator, send
us a message to this email: the word help at this domain, like so: hxxx@sxxxxxxxxx.cxx
:::

::: only 7,8
## {{v7|Install}}{{v8|Before you start}} {#install}

::: only 7
Given the way TI-89 calculators work, programs run faster when they have been
*archived* after having been executed at least once. We refer to this process
as 'installing' them. Both Symbulator and DiffEq have installation programs,
which you execute in your calculator as follows:

```sym 7
s\install()
Archive s\install
```

and

```sym 7
dif\install()
Archive dif\install
```

That is all the software you need!

### Where to symbulate

After years of using Symbulator, I have developed certain *best practices* that
I will share with you as Tips in this documentation. My first recommendation is
that you always make MAIN your current folder in the calculator before running
a simulation, and that you empty the MAIN folder of all spurious variables
before running each simulation.

::: tip Pro Tip
Before running a simulation in Symbulator, make MAIN your current folder, and
delete all the variables that are not related to your simulation.
:::
:::

::: only 8
### Clean slate

I recommend that, before running a simulation in the Nspire, you either create
a new document or delete from the current one all the variables that are not
related to your simulation.

Furthermore, if for any reason a simulation fails or aborts and there are
leftover variables, you should either move to a new document or delete these
variables before you run the simulation again.

::: tip Pro Tip
Start each simulation from a clean document, and clear out anything a failed
simulation left behind before trying again.
:::
:::
:::

::: only 9

## Input files and entries {#input-files}

Everything you put into Symbulator — the circuit, the analysis, the settings,
and whatever is in the **Evaluate** and **Solve** cards — can be kept and used
again. There are two words for it.

An **entry** is one set of inputs meant to be solved together: a circuit, the
analysis to run on it, and the settings to run it with. It has a name.

An **input file** holds as many entries as you like, and names itself: a
file can say it is *Circuits for Lesson 1 of the Tutorial*, and that is what
you will see it called. It is plain text, its extension is `.cir`, and you
will find it in the **Input File** card at the top of the page — marked
*optional*, because nothing needs it. You can use Symbulator for a whole
session without ever opening one.

### Loading one

Symbulator arrives with a set of input files of its own: one for each lesson
of this tutorial, holding an entry for every simulation that lesson runs.
Not one per problem — a few problems are worked through with more than one
simulation, and each of those gets its own entry — so a lesson file has
rather more entries than the lesson has problems. Between them they let you
follow the whole tutorial without typing a circuit at all, and try any of
them again later without having to find the page it came from.

Symbulator opens on the first of these. **Built-in examples** lists the
rest: click it and choose one by its title. That link is always there, so it
is also how you move from one to the next.

To open a file of your own, press **Upload** and choose a `.cir`. Either way
the dropdown beneath then reads *Entries in* whatever the file calls itself,
and choosing an entry fills in every box on the page at once — circuit,
analysis, settings and all. Then solve it exactly as you would something you
had just typed.

The supplied files are **read-only**. Load one and change it as much as you
like, but you cannot write back to it: saving starts a file of your own, and
**Create new** starts an empty one.

### Saving your work

Two links sit under the circuit box, and each appears only when it applies:

- **Save inputs to new entry** adds what is on screen as a new entry and asks
  you to name it. This is the one you want the first time.
- **Update inputs in this entry** writes your changes back into the entry you
  loaded. It appears once you have actually changed something.

Beside the dropdown, **Rename** and **Delete** act on the entry itself.
Neither is offered for the built-in examples.

::: warning Nothing reaches your disk until you press Download
Saving an entry writes it into the file open **in your browser**. The only
thing that produces a `.cir` on your computer is **Download**.

Symbulator does what it can in the meantime: your work is mirrored into the
browser's own storage, so closing the tab does not lose it, and you are warned
before anything replaces a file holding entries you have not downloaded. None
of that is a file, though. Download when you are done.
:::

### What an entry remembers

All of it, not just the circuit. The analysis and whatever that analysis needs
— the frequency, the two node names for an equivalent, which kind of two-port
— then the Expert Mode equations, unknowns and conditions, everything in
**Settings**, whatever is in **Evaluate** and its **Conditions**, the **Solve**
card, the plot, and a note of your own that is shown when the entry is loaded.

So an entry is a piece of work rather than a circuit. Load one a year later
and you are back where you left off, with the same rounding, asking the same
question.

### Writing one by hand

Because it is plain text, you can write an input file in any editor, which is
a convenient way to set a problem sheet. A `title:` line above the first entry
names the file. An entry is its own name in square brackets, then the element
lines, then `key: value` lines. Anything after a hash is a comment.

```text
# Lines that start with a hash are comments.

title: Two problems to be going on with

[Divider]

e1,1,0,20
r1,1,2,5'k
r2,2,0,15'k

analysis: dc
rounding: exact
si: no
units: yes


[Series RL at 1 kHz]

e1,1,0,10
r1,1,2,50
l1,2,0,0.02

analysis: ac
omega: 2*pi*1000
rounding: approx
si: no
units: yes
rms: no
note: the current lags the voltage
```

Every `key: value` line is optional: leave one out and Symbulator's own
default applies, exactly as though you had never touched that setting. Order
does not matter either — a line whose key Symbulator knows is a setting, and
anything else is an element, wherever in the entry it appears.

**About input file (.cir) format**, inside the **Input File** card, lists
every key the app reads and writes.

:::
