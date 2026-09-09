---
id: introduction
kind: front
title: Introduction
updated: 2026-09-09
summary: >
  Learn about Symbulator and how it can help you focus on learning how circuits work, instead of struggling with math. Get the latest version of Symbulator and get ready to roll.
---

## What is Symbulator {#what-is-symbulator}

Symbulator is a program to solve linear electric circuits symbolically and
numerically {{v7,8|in a calculator}}{{v9|on your device}}. It takes numerical and symbolic
values, and returns numerical and symbolic results. The odd-sounding name is a portmanteau of *"**symb**olic sim**ulator**"*.
Symbulator is widely regarded as the best symbolic simulator of linear
electric circuits ever {{v7,8|made for a calculator}}{{v9|to run on a handheld device}}.

### What analyses can it do?

Symbulator can solve circuits using four types of analysis: direct current (DC), alternating current (AC), transient time-domain (TR), and complex
frequency-domain (FD). It analyses numerical and, more importantly, symbolic linear circuits,
returning the voltages in all nodes and the currents, voltage drops and power
in all elements. It also finds the passive, Thévenin / Norton and two-port
equivalent of a circuit, and draws time domain{{!v8| and Bode}} plots.

### What elements does it accept?

Symbulator accepts elements such as resistors, inductors, mutual inductance,
capacitors, independent and dependent current and voltage sources, ideal
operational amplifiers, ideal transformers and six types of two-ports.

### Where does it run?

::: only 7
Symbulator 7, released in 2023, is written — like all its predecessors — for
Texas Instruments' TI-89 Titanium, and runs on all compatible devices, such as
the Voyage 200 and the classic TI-89. There is a version for the TI-Nspire
CX II CAS called version 8, and a newer Python/SymPy port called version 9.
:::
::: only 8
Symbulator 8, released in 2023, is adapted to run on the TI-Nspire CX II CAS calculator by
Texas Instruments. There is also a version for the TI-89 Titanium called
version 7, and a newer Python/SymPy port called version 9.
:::
::: only 9
Symbulator 9, released in 2026, is a port of the classic code to Python, powered by the SymPy computer algebra library.
It runs anywhere Python runs: your mobile phone, tablet, laptop, a Jupyter notebook, or a browser on any computer.
Version 9 solves circuits faster than versions 7 and 8.
:::

## Why use Symbulator? {#why-use-it}

Symbulator is extremely useful on the circuit theory problems engineering
students face in Circuits I and II. It lets the student focus on understanding
circuit analysis rather than on the mathematics of solving it.

### Strengths

- A fantastic tool to solve circuits composed of ideal, linear elements.
- Shines in solving circuits with symbolic values, and symbolic results.
- Offers the absolute simplest way to define dependent sources.
- Includes ideal transformers and six different two-ports.

### Limitations

- Does not simulate non-linear elements, such as diodes and transistors.
- Will not answer under-defined problems that rely on applying formulas selectively rather than solving a circuit completely.
- Is not a replacement for your brain or an excuse to not study. You must understand circuit theory to use it.

### Symbulator is free!

Symbulator has always been free of charge, and always will be.
*(You are welcome!)* Since 2026, Symbulator is also open source under the MIT licence. You are free to use it,
change it and port it to other platforms; all the licence asks is that the
copyright notice and the attribution to the original author travel with it.

::: only 7
## Download {#download}

### Symbulator

The latest version of Symbulator for the TI-89 platform is version 7 (date
stamp **08 July 2023**). We believe it is free of bugs; if any is found we will
revise and reupload, updating the date stamp. It runs on the TI-89 Titanium and
the Voyage 200.

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
(date stamp **08 July 2023**). It may still contain the occasional bug; as bugs
are found and fixed, we will revise and reupload, updating the date stamp.

To get Symbulator 8, download this file:
**[s.tns](https://symbulator.com/8/s.tns)**, transfer it to your
calculator, and refresh the libraries.

### Laplace Functions

Since the CAS in the TI-Nspire CX II CAS does not do Laplace transforms,
Symbulator relies for this on another software, which I call Laplace Functions.

This software was made, around the same time Symbulator was being created, by
my friend Lars Frederiksen, one of the most gifted programmers for TI-Basic
ever. Lars made two programs for the TI-92+/Voyage and the TI-89: one he called
DiffEq, because it also solves differential equations, and the other Advanced
Laplace, which packed improved versions of his Laplace functions.

The latter was automatically adapted for the TI-Nspire by Philippe Fortin, who
renamed the group of functions ETS_specfunc. Not being a fan of that name, and
given my friendship and collaboration with Lars, I have taken the liberty of
renaming the file here to **LF**, which in my eyes stands both for Laplace
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

You can use Symbulator 9 in two ways:
- as an online app running on a remote server, or
- as an offline app running locally on your device.

The easiest way to start is the **[online app](https://symbulator.pythonanywhere.com/)**.

To run it offline on your own device, follow the instructions at the bottom of the online app, under {{btn:Run Symbulator 9 locally}}.

:::

::: danger Use at your own risk!
Every effort has gone into Symbulator, and it has no known bugs. Even so, it
is provided "as is", without warranty of any kind, express or implied,
including but not limited to the warranty of fitness for a particular
purpose. You use it at your own risk.
:::

Please report any problems to help [at] symbulator [dot] com

::: only 7,8
## {{v7|Install}}{{v8|Before you start}} {#install}

::: only 7
Given the way TI-89 calculators work, programs run faster once they have been
executed at least once and then *archived*. We call that 'installing' them.
Both Symbulator and DiffEq have installation programs, which you run in your
calculator as follows:

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
I share as Tips in this documentation. The first: always make MAIN your current
folder before running a simulation, and empty MAIN of spurious variables before
each one.

::: tip Pro Tip
Before running a simulation in Symbulator, make MAIN your current folder, and
delete all the variables that are not related to your simulation.
:::
:::

::: only 8
### Clean slate

Before running a simulation in the Nspire, either create a new document or
delete from the current one every variable unrelated to your simulation.

And if a simulation fails or aborts and leaves variables behind, move to a new
document or delete them before running it again.

::: tip Pro Tip
Start each simulation from a clean document, and clear out anything a failed
simulation left behind before trying again.
:::
:::
:::

::: only 9

## Built-in examples {#built-in-examples}

You do not have to type the tutorial's circuits. The **Built-in
examples** list at the top of the app holds an entry for every
simulation in every lesson; click a title to load one and solve it as if
you had typed it yourself.

{{ref:input-files}} explains how to load them, save your own work, and
download it to your device.

## Reading and running side by side {#split-view}

This tutorial has you moving between the page you are reading and the app you
are running. Two windows work. There is a tidier way.

The **[split view](/split/)** puts both in one window: the documentation on
the left, the live app on the right. Drag the divider to resize them; on a
phone or a narrow window they become two tabs. Both halves are the real thing,
simply shown together.

The two halves are connected. On the website, every worked problem carries two
links under its title:

- {{btn:Open in app ↗}} loads that circuit, with its analysis and settings, ready to run.

- {{btn:Open in split view}} does the same, but in the split view, on the problem you were reading.

Inside the split view, {{btn:Open in app ↗}} loads the circuit into the right-hand
pane instead of a new tab, and the second link is not shown.

::: warning Loading a problem starts the app fresh
{{btn:Open in app ↗}} reloads the app with the circuit you asked for, replacing
anything you had typed there. To keep your own work, save it to an entry and
download the file **before** you click the next problem. {{ref:input-files}}
explains how.
:::

A problem with more than one simulation carries a link for each, marked **DC**
or **TR**. A few problems have no link, because they are worked by hand.
{{pdf|In the PDF, the links are on the web edition at `learn.symbulator.com`;
everything else on this page applies either way.}}

The split view keeps its address current as you move, so it can be shared
where you are. Send someone:

::: address learn.symbulator.com/split/?lesson=6a&entry=3
:::

and they open on the same problem, with the same circuit loaded.
:::
