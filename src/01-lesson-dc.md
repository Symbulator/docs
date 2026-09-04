---
id: lesson-dc
kind: lesson
title: Direct current analysis
updated: 2026-08-29
summary: >
  Learn to describe a circuit in Symbulator, and how to run a *direct current*
  analysis using **dc**. Learn how to describe a *voltage source* using **e**,
  and a *resistor* using **r**.
---

I firmly believe one learns best by *doing*, so I have written this
documentation as a tutorial, where you learn Symbulator by working through a
series of progressively more diverse and complex examples. In a moment, I'll teach you how to swim. But for now, let me throw you in the deep end!

## Run a direct current analysis {#run-dc}

{{v7|I want you to make MAIN the current folder in your calculator, delete all
variables you don't need (ideally, the current folder should be empty), and
type this:}}{{v8|I want you to create a new document in your calculator, or to
delete all variables you don't need from your current one (ideally, the current
document should be empty), and type this:}}{{v9|Open Symbulator 9 — the local app if you have it installed, otherwise the
**[online app](https://symbulator.pythonanywhere.com/)** in a browser. Click
**Clear all inputs**, at the top right, so every input field is empty. Then
type this into the **Circuit Description** box, one element per line:}}

```sym 7
s\dc("e1,1,0,36:r1,1,2,1'k:r2,2,3,3'k:r3,3,0,2'k")
```
```sym 8
s\dc("e1,1,0,36:r1,1,2,1'k:r2,2,3,3'k:r3,3,0,2'k")
```
```field 9 Circuit Description
e,1,0,36
r1,1,2,1'k
r2,2,3,3'k
r3,3,0,2'k
```

::: only 7,8
Now I want you to press ENTER.
:::
::: only 9
Scroll down to **Analysis & Settings** (if it is collapsed, open it with the
blue triangle to its left). Set **Type of analysis** to *Solve circuit* and
**Analysis** to *DC — direct current*. Then click **Run Symbulator**.
:::

::: only 7
If you typed everything correctly and your calculator is properly set up with
Symbulator, you should have seen BUSY appear in the bottom right corner, and
your calculator seemingly go into a trance and spew out a series of cryptic
messages. Then, after a few seconds, it should have returned to normal,
displaying a short Done.
:::
::: only 8
If you typed everything correctly and your calculator is properly set up with
Symbulator, you should have seen several lines of text appear, with a series
of cryptic messages. Then, after a few seconds, it should have displayed a
short Done.
:::
::: only 9
The button reads *Solving…* for a moment, then *Solved!*. Scroll down to
**Results**, under **OUTPUTS**: there is an answer for every node and every
element of the circuit.
:::

Congratulations! You have just run your first simulation in Symbulator 9.

### How does it work

Let's now go over what we just did, one piece at a time.

::: only 7
To analyse a direct current circuit in Symbulator, we use a program called
**s\dc()**. The program itself is called **dc**, but since it is found in the
Symbulator folder **s**, we have to refer to it as **s\dc**, so the calculator
knows exactly what we want. And because it is a program, it carries the
parenthesis **()** after its name.
:::
::: only 8
To analyse a direct current circuit in Symbulator, we use a program called
**s\dc()**. The program itself is called **dc**, but since it is found in the
Symbulator library **s**, we have to refer to it as **s\dc**, so the calculator
knows exactly what we want. And because it is a program, it carries the
parenthesis **()** after its name.
:::
::: only 9
The two menus in **Analysis & Settings** tell Symbulator what to do (in this case, solve
the circuit) and which analysis to run (in this case, in direct current). Everything else there
is optional; later lessons introduce it, and until then leave it as it is.
:::

::: only 7,8
The dc program takes one argument as its input: the description of the circuit
you want to analyse. That input goes inside the parenthesis.

In Symbulator, a circuit description takes the form of a string of text,
describing a series of elements, separated by colons.{{i:circuit description}}

The circuit description can be passed to the program directly as an argument,
as we did above, or it can be stored into a variable whose name is then fed in,
like this:
:::


```sym 7
"e1,1,0,36:r1,1,2,1'k:r2,2,3,3'k:r3,3,0,2'k"→cir
s\dc(cir)
```
```sym 8
"e1,1,0,36:r1,1,2,1'k:r2,2,3,3'k:r3,3,0,2'k"→cir
s\dc(cir)
```

::: only 9
The most important input is the description of the circuit you want to
analyse. It goes in the **Circuit Description** area, as a series of lines of
text, each describing one element.{{i:circuit description}}
:::

```field 9 Circuit Description
e,1,0,36
r1,1,2,1'k
r2,2,3,3'k
r3,3,0,2'k
```

::: only 9
Using one line per element keeps a long circuit readable,
and it makes mistakes easier to find. But it is not the only option: Symbulator
also accepts a colon as a separator. For example, this is the same circuit, described in one line: 
:::

```field 9 Circuit Description
e,1,0,36:r1,1,2,1'k:r2,2,3,3'k:r3,3,0,2'k
```

::: only 7,8
The results are exactly the same as doing it in a single step. I like to use
**cir** as the name of the variable where I store my circuits, and that is what
you will see in this tutorial, though any valid variable name will do. You will
see both ways used throughout.
:::

::: only 9
To reuse this circuit later, save it as an **entry** in an **input file**. You
will be asked to name both. Input files must have the `.cir` extension.
:::

### Look at the elements

Now let's examine the contents of the circuit description. {{v7,8|Study it and you will see three colons.
In Symbulator, colons separate elements in a circuit description, so putting
them aside, this description has four elements:}}{{v9|Study it, and you will see it has four lines. Each line describes
one element.}}

::: only 7,8
- The first one is `e1,1,0,36`
- the second one is `r1,1,2,1'k`
- the third one is `r2,2,3,3'k`
- the fourth one is `r3,3,0,2'k`
:::

At the moment they may look cryptic. But by the end of this lesson you will
read them with ease.

## How to describe a resistor {#describe-resistor}

Notice that the second, third and fourth elements in the list all start with
the letter **r**. These are resistors.{{i:resistor}}

::: note Describing resistors
An ideal resistor is described with four pieces of information, separated by
commas: a unique name (which must start with the letter **r**), the names of
its first and second node, and its value in ohms (Ω).

For example, an ideal resistor called **r1**, between nodes **a** and **b**,
of **300** Ω, is described `r1,a,b,300`
:::

### How to name resistors

Every resistor must have a name. As long as it starts with the letter **r**
and is unique, it can be whatever you want. *Unique* means no other element or
node has the same name.

::: only 7
With one exception: `rc` is reserved in the TI-89 calculator, and cannot name
a resistor or anything else.

::: warning Can't touch rc
The variable `rc` is reserved by the calculator, and cannot be used as a name.
:::
:::
::: only 8
Two exceptions I know of so far: `r` and `rr` should not name resistors,
because some of the answer variables they generate collide with reserved
ones.

::: warning Can't touch r or rr
The names `r` and `rr` cannot be used, because their answers conflict with
reserved variables in the calculator.
:::
:::

### How to name nodes

Naming the nodes is the first thing we do to solve a circuit. Every node must
have a name, and node names must be unique: no other node or element may have
the same one. Otherwise they can be whatever you want, with 
{{v7,8|two constraints. The first one is that:}}{{v9|one constraint:}}
 at least one node should be called **0** (zero). This will be considered the
*ground node* of your circuit{{i:ground node}} and will have, by definition, a
voltage of 0 volts.

::: warning You need a ground node
Every circuit must have a node called 0 to serve as reference or ground.
:::

::: only 7
The second restriction is that you cannot use the calculator's reserved
variables as names. Besides rc, there are c1, c2, c3 … c99, and more exotic
ones listed in the calculator's User's Manual.
:::
::: only 8
The second restriction is that you cannot use variables that are reserved in
the calculator as names. These are listed in the User's Manual of the
calculator.
:::

### Values can use SI prefixes

The values of circuit elements are often given with prefixes of the
International System (SI) — kilo, milli, micro. So Symbulator has a shorthand
for them: an SI prefix in an element's value, preceded by an apostrophe,
multiplies it by the corresponding factor, exactly.{{i:SI prefixes}}

::: only 9
The prefixes Symbulator accepts:

| Prefix | Shorthand | Factor |
|---|---|---|
| peta | `'P` | 10{{sup:15}} |
| tera | `'T` | 10{{sup:12}} |
| giga | `'G` | 10{{sup:9}} |
| mega | `'M` | 10{{sup:6}} |
| kilo | `'k` or `'K` | 10{{sup:3}} |
| milli | `'m` | 10{{sup:-3}} |
| micro | `'u` or `'µ` | 10{{sup:-6}} |
| nano | `'n` | 10{{sup:-9}} |
| pico | `'p` | 10{{sup:-12}} |
| femto | `'f` | 10{{sup:-15}} |
| atto | `'a` | 10{{sup:-18}} |
:::

::: tip Prefixes welcome!
You can use SI prefixes, preceded by an apostrophe, in the values of
elements.
:::

For example, an 8 kΩ resistor can be entered in many ways: `8000`, `8'k`,
`8000.` and `8E3` are all equivalent, except that the first two are treated as
exact and the other two as approximate.

## What answers do you get {#dc-answers}

After the simulation in DC is complete, Symbulator {{v7,8|stores a series of
answers in the calculator's memory, labelled with easy to remember names for
your convenience}}{{v9|fills in the **Results** section under **OUTPUTS** with every answer it
worked out}}.

::: only 9
The results are arranged in groups: **Node voltages** first, one per
node, and then **Results by element**, one group per element, headed by its
name and its kind — `r1` *resistor*, `e` *voltage source*.

Every answer is written the way you would write it by hand, as a named quantity
and its value: v{{sub:1}} = 36 V, i{{sub:r1}} = 6 mA.

### How answers are shown
By default, Symbulator answers *exactly*: it works symbolically, so a current
comes back as 3/500 A rather than a decimal. That is what you want for
symbolic results. For numerical work like the example in this lesson, decimals read better. Open the
**Settings** card and set **Rounding** to *approx to n digits*
with **n** = 3, then tick **Use SI prefixes in answers**. The current above
then reads 6 mA instead of 3/500 A.

Ticking the prefix box moves **Rounding** off *exact* by itself, since a
prefixed value is a decimal, and choosing *exact* again switches the prefixes
off. Symbulator says so on screen when it does.

In this tutorial, numerical examples assume approximate answers to three or
four figures with prefixes on, and symbolic ones assume *exact*. The text says
so when a change is needed.
:::

### Answer for each node

Symbulator calculates for each node a voltage with reference to ground, which is {{v7,8|stored in a variable called v plus the name of
the node. For example, for a node called 1, its voltage is stored in a variable
called v1}}{{v9|shown under **Node voltages** as `v` plus the node's name: node 1's
voltage is `v1`}}.

### Answers for each resistor

Symbulator calculates for each resistor the following answers:

- The voltage drop in the resistor, defined as the voltage in the first node minus the voltage in the second node, in volts. For a
  resistor called r5, this is {{v7,8|stored in}}{{v9|given in}} `vr5`.
- The current through the resistor, flowing from the first node towards the
  second, in amperes. For a resistor called rx, this is {{v7,8|stored in}}{{v9|given in}}
  `irx`.
- The power consumed by the resistor, in watts. For a resistor called r12, this
  is {{v7,8|stored in}}{{v9|given in}} `pr12`.

By now you should understand the description of the second, third and fourth
elements in our example.

## How to describe a voltage source {#describe-voltage-source}

The first element in our example, on the other hand, started with the letter
**e**. This element is a voltage source.{{i:voltage source}}

::: note Describing voltage sources
In Symbulator, a voltage source is described with four pieces of information,
separated by commas: a unique name (which must start with the letter **e**),
the names of its positive and negative node, and its value in volts (V).

For example, an ideal voltage source called **e1**, with its positive terminal
in node **3**, its negative terminal in the ground node **0**, and a value of
12 volts, is described `e1,3,0,12`
:::

### How to name voltage sources

Every voltage source in your circuit must have a unique name that starts with
the letter **e**, and it can be whatever you want.

### Values can use SI prefixes

A voltage source's value can use SI prefixes too — they work in the values of
every element.

### Answers for a voltage source

For each voltage source, the following answers are calculated:

- The voltage drop in the source, defined as the voltage in the first node
  minus the voltage in the second, in volts. For a source called e5, `ve5`.
- The current through the source, flowing from the first node towards the
  second, in amperes. For a source called ex, `iex`.
- The power consumed — attention: not delivered, but consumed — by the source,
  in watts. For a source called e12, `pe12`. If we want the power delivered, we ask for the
  negative of this value.
- The equivalent resistance of the rest of the circuit, as seen by the source.
  For a source called e2, `re2`.

::: note For sources only
The equivalent resistance is a property of the *view from a source*, not for every element. It exists only for sources.

::: only 7,8
There is no `rr1` for a resistor — a resistor's resistance is the value you
gave it. The same applies to the impedance answers in AC analysis, which you
will meet in {{ref:lesson-ac}}.
:::
:::

## A numerical DC simulation, step by step {#step-by-step}

Let's go back now to the simulation we ran earlier. That simulation corresponds
to the circuit given in Example 5.7 in Boylestad's *Introductory Circuit
Analysis* (11ed). Moving forward, I will refer to that textbook as **B11**.

The problem statement and the circuit schematic are reproduced exactly as they
appear in the textbook, as they will be for every other problem in this
tutorial. Since this is
for educational purposes, it is my understanding that it falls squarely within
the "fair use" doctrine of copyright law. In any event, no copyright
infringement is meant.

::: problem B11's Example 5.7
::: figure assets/circuit/b11e0507.jpg
B11's Example 5.7
:::

::: answer
All the values in this circuit are numbers: no element value is unknown. This
is a *numerical circuit* — one where we know the numerical value of every
element in it.

I will now walk you step by step through the solution. This process applies to
most numerical simulations in Symbulator: (1) describe the circuit, (2)
run the simulation, and (3) get the answers.

**Step 1: Describe the circuit.** Description starts with **naming the
nodes**. As we said, you can call them anything you want, number or letter, as
long as the name is unique — but one node must always be called 0 (zero), the
ground node, with a voltage of 0 V. In this circuit the ground node is marked
with the ground symbol. That is not always so; when it is not marked, you pick
a node to serve as zero.

I labelled the nodes in this circuit, starting in the ground and moving
clockwise, as 0, 1, 2 and 3. It helps me to pencil the names in the schematic
itself.

::: tip Write 'em down!
Write the names of your nodes and elements onto the circuit schematic itself,
so you don't forget who's who.
:::

::: figure assets/circuit/b11e0507b.jpg
B11's Example 5.7, with the node names pencilled in
:::

After naming the nodes, I am ready to describe the elements of the circuit in
Symbulator notation.

Let's start with the source: when I only have one voltage source, like here, I
enjoy {{v7,8|naming it with a single letter: e}}{{v9|giving it a short name: e}}. So the voltage source is
{{v7,8|`e,1,0,36`}}{{v9|`e,1,0,36`}}: its name is
{{v7,8|e}}{{v9|e}}, its positive node is 1, its negative node is 0, and its
value is 36 volts between them.

Now the resistors. I named the first r1 and described it `r1,1,2,1'k`: its
name is r1, its first node 1, its second node 2, and its value 1 kΩ. The
second is `r2,2,3,3'k`, and the third `r3,3,0,2'k`.

::: note An important point about SI prefixes
In the case of kilo, we can write it as either `'k` or `'K`. But that's not the
case for every other SI prefix: their case matters. For example, `'m` means
milli, while `'M` means mega. {{v7,8|Symbulator's custom menu includes the
spelling of all SI prefixes.}}
:::

::: only 7,8
We pass the description to Symbulator as a string: open with a quotation mark,
enter each element's description separated by colons, and close with a
quotation mark. We can store the string in a variable:
:::
::: only 9
Those four element descriptions, gathered together, are the whole circuit. Put them in
the **Circuit description** box, one to a line:
:::

```sym 7
"e,1,0,36:r1,1,2,1'k:r2,2,3,3'k:r3,3,0,2'k"→cir
```
```sym 8
"e,1,0,36:r1,1,2,1'k:r2,2,3,3'k:r3,3,0,2'k"→cir
```
```field 9 Circuit Description
e,1,0,36
r1,1,2,1'k
r2,2,3,3'k
r3,3,0,2'k
```

**Step 2: Run the simulation.** {{v7,8|We can now ask Symbulator to simulate
this circuit in direct current:}}{{v9|Under the box, choose the simulation:}}

```sym 7
s\dc(cir)
```
```sym 8
s\dc(cir)
```

::: only 9
- **Type of analysis** → *Solve circuit*
- **Analysis** → *DC — direct current*

Then press **Run Symbulator**.
:::

::: only 7
Symbulator says Done when a simulation completes. It took my calculator 16
seconds to solve this circuit, in which time it found 16 answers and stored
each in a memorably named variable in the current folder.
:::
::: only 8
Symbulator says Done when a simulation completes. It took my calculator under
2 seconds to solve this circuit, in which time it found 16 answers and stored
each in a memorably named variable in the current document.
:::
::: only 9
The page fills in below — this circuit takes under a second on a computer,
and maybe a bit more on a mobile — and a line at the foot of **Results** says
what happened: *DC analysis · 16 result(s)*, and how long it took.
:::

For a DC analysis, these answers are as follows:

- The **voltage of each node**, so the voltages of nodes 1, 2 and 3 are in
  {{v7,8|v1, v2 and v3}}{{v9|`v1`, `v2` and `v3`, under **Node voltages**}}.
- The **current through each element**. The direction of the current is defined
  as going from the first node in the element's description to the second.
- The **voltage drop in each element**, defined as the difference in voltage
  between the first node in the element's description and the second, in that
  order.
- The **power consumed in each element**. An important point is that this is
  the power consumed, not the power delivered.
- Finally, **for each source**, **the equivalent resistance** of the rest of the
  circuit **as seen by that source**.

::: note The sign is in the details
To read the signs of your answers correctly, mind the details:

- The current in the elements is defined as going through the element from the
  first node to the second node.
- The voltage drop is defined as the voltage of the first node minus the
  voltage of the second node.
- The power given is the power consumed. So, if you want power delivered,
  evaluate the negative of that power.
:::

**Step 3: Get the answers.** We can now answer the six questions in the
problem.

*Answer to question (a).* The equivalent resistance as seen by the source
{{v7,8|e}}{{v9|e}}:

```sym 7
re
```
```sym 8
re
```
```out 7,8
6000
```

::: only 9
Nothing to compute: in **Results by element**, the resistance seen by the
source reads `re` = {{o:6}} kΩ. Correct.
:::

::: only 7,8
That is 6 kΩ. Correct.
:::

*Answer to question (b).* Current {{var:I_s}} is defined in the schematic as the current
flowing through the source, in the direction that goes from node 0 to node 1.
One way to find this value is evaluating the negative of the current through
the source, which {{v7,8|as you know flows}}{{v9|we defined as flowing}} in the opposite direction:

```sym 7
–ie
```
```sym 8
–ie
```
```out 7,8
.006
```

::: only 9
The current through the source reads `ie` = −6 mA. The answer we want is its
opposite, 6 mA.
:::

{{v7,8|That is 6 mA. }}Another way, since this is a series circuit where every element
carries the same current, is to
{{v7,8|evaluate the current through any of the resistors}}{{v9|read the
current through any resistor}}.

*Answer to question (c).* The voltage drop in resistor {{var:R_1}} — since its polarity
is defined in the schematic in the same way it is defined in our circuit
description — is as follows.

::: only 7,8
It is found by evaluating `vr1`: the {{t:machine}} returns `6`, that is 6 V.
For {{var:R_2}}, `vr2` gives {{o:18}} V. And for {{var:R_3}}, `vr3` gives {{o:12}} V. These are all the right
answers.
:::
::: only 9
The voltage drop `vr1` reads {{o:6}} V, `vr2` reads {{o:18}} V and `vr3` reads {{o:12}} V. All
correct.
:::

::: only 7,8
*Answer to question (d).* Since the problem asks for the power supplied by the
source, and we know that `pe` has the power consumed by it, we need to evaluate
the negative of it, and we get `.216`, that is 216 mW delivered.
:::
::: only 9
*Answer to question (d).* We know that the power consumed is given in `pe`. We
get the power supplied by the source by switching the sign: 216 mW delivered.
:::

::: only 7,8
*Answer to question (e).* The power consumed by the resistors is found
evaluating `pr1`, `pr2` and `pr3`. We get `.036`, `.108` and `.072`, that is
36 mW, 108 mW and 72 mW consumed, respectively.
:::
::: only 9
*Answer to question (e).* The power consumed by the resistors is given in
`pr1`, `pr2` and `pr3`: 36 mW, 108 mW and 72 mW, respectively.
:::

*Answer to question (f).* Let's ask {{v7,8|the calculator}}{{v9|Evaluate}} whether the sum of the
consumed power in the resistors equals the power supplied by the source:

```sym 7
pr1+pr2+pr3=–pe
```
```sym 8
pr1+pr2+pr3=–pe
```
```out 7,8
true
```

::: only 9
If the resistors consume exactly what the source delivers, the four powers
add up to zero. In **Evaluate**:

```field 9 Evaluate
pr1 + pr2 + pr3 + pe
```

The answer is {{o:0}}.
:::

This is the right answer, and concludes the solution to this, your first ever
problem in Symbulator.
:::
:::

## Instructive numerical examples, solved {#practice-dc}

::: practice


### Numerical problems in DC using e and r

These practice problems are taken from several textbooks, chosen because they
apply only the concepts you have learned so far. They let you practise and
reinforce them before Lesson 2.

The problem below comes from Figure 1-26 (a) in Hyatt and Kemmerly's
*Engineering Circuit Analysis* (5ed). Moving forward, we will refer to that
textbook as **HK5**.

::: problem HK5's Figure 1-26

We are asked for the current, voltage drop and power consumed in each
resistor, the power *delivered* by each voltage source, and a check that the
powers in the circuit add up to zero.

::: figure assets/practice/hk5s-figure-1-26-1.jpg

:::

Here is my solution.

I named the nodes thus: the bottom node **0**, and the top nodes, from left to
right, **1**, **2** and **3**. My description of the
circuit{{v7,8|, as the argument of the DC simulation command}}:

```sym 7
s\dc("e1,1,0,120:r1,1,2,30:e2,2,3,30:r2,3,0,15")
```
```sym 8
s\dc("e1,1,0,120:r1,1,2,30:e2,2,3,30:r2,3,0,15")
```
```field 9 Circuit Description
e1,1,0,120
r1,1,2,30
e2,2,3,30
r2,3,0,15
```

{{v7,8|When the simulation is done, you can ask the calculator for the answers
you need:}}{{v9|Run it, and the answers are all on the page already:}}

- {{v7,8|Evaluating `ir1` or `ir2` gets the current in the resistors}}{{v9|The
  current through either resistor, `ir1` or, `ir2` is}}: {{o:2}} A
- {{v7,8|Evaluating `vr1` gets}}{{v9|`vr1` gives}}
  the voltage drop in the 30Ω resistor: {{o:60}} V
- {{v7,8|Evaluating `vr2` gets}}{{v9|`vr2` is}} the voltage drop in the 15Ω resistor: {{o:30}} V
- {{v7,8|Evaluating `pr1` gets}}{{v9|`pr1` is}} the power consumed in the 30Ω resistor: {{o:120}} W
- {{v7,8|Evaluating `pr2` gets}}{{v9|`pr2` is}} the power consumed in the 15Ω resistor: {{o:60}} W
- {{v7,8|Evaluating }}{{v7|`-pe1`}}{{v8|`–pe1`}}{{v9|Flipping the sign of `pe1`}} gets the power delivered by the 120V source: {{o:240}} W
- {{v7,8|Evaluating }}{{v7|`-pe2`}}{{v8|`–pe2`}}{{v9|Flipping the sign of `pe2`}} gets the power delivered by the 30V source: {{o:-60}} W. The source consumes 60W, so it delivers *negative* 60W.
- {{v7,8|Evaluating `pr1+pr2+pe1+pe2` gets}}{{v9|`pr1+pr2+pe1+pe2` is}} the sum of powers: {{o:0}} W. As expected.

Wasn't that easy?

::: only 7,8
We could also have asked for all the answers with one array:

```sym 7
{ir1,vr1,vr2,pr1,pr2,-pe1,-pe2,pr1+pr2+pe1+pe2}
```
```sym 8
{ir1,vr1,vr2,pr1,pr2,–pe1,–pe2,pr1+pr2+pe1+pe2}
```
:::

:::

::: problem B11's Example 5.20

The practice problems get progressively more complicated, so you build up your
*'symbulating'* skills with confidence.

::: figure assets/practice/b11s-example-5-20-2.jpg

:::

I named the nodes clockwise from the ground: **0**, **1**, **2**, **3** and
**4**. My circuit description{{v7,8|, as an argument of the DC simulation command}}:

```sym 7
s\dc("e1,1,0,50:r1,1,2,4:e2,2,3,12.5:r2,3,4,7:r3,4,0,4")
```
```sym 8
s\dc("e1,1,0,50:r1,1,2,4:e2,2,3,12.5:r2,3,4,7:r3,4,0,4")
```
```field 9 Circuit Description
e1,1,0,50
r1,1,2,4
e2,2,3,12.5
r2,3,4,7
r3,4,0,4
```

When it's done, ask for the answers we need. {{v7,8|Evaluating `ir1` gets}}{{v9|`ir1` is}} the
current I: {{o:2.5}} A. {{v7,8|Evaluating `vr2` gets}}{{v9|`vr2` is}} the voltage drop in the 7Ω
resistor: {{o:17.5}} V

:::

::: problem B11's Example 6.13

::: figure assets/practice/b11s-example-6-13-3.jpg

:::

Since the ground is the bottom node, I named it **0**. I named the top node
**1**.

```sym 7
s\dc("e,1,0,24:r1,1,0,10:r2,1,0,220:r3,1,0,1.2'k")
```
```sym 8
s\dc("e,1,0,24:r1,1,0,10:r2,1,0,220:r3,1,0,1.2'k")
```
```field 9 Circuit Description
e,1,0,24
r1,1,0,10
r2,1,0,220
r3,1,0,1.2'k
```

- {{v7,8|Evaluating `re` gets}}{{v9|`re` is}} the total resistance: {{o:9.49}} Ω
- {{v7,8|Evaluating }}{{v7|`-ie`}}{{v8|`–ie`}}{{v9|Flipping the sign of `ie`}} gets us the source current: {{o:2.53}} A
- {{v7,8|Evaluating `ir1` gets}}{{v9|`ir1` is}} {{var:I_1}}: {{o:2.4}} A, {{v7,8|`ir2` gets}}{{v9|`ir2` is}} {{var:I_2}}: {{o:109}} mA, and {{v7,8|`ir3` gets}}{{v9|`ir3` is}} {{var:I_3}}: {{o:20}} mA.

:::

::: problem B11's Example 7.2

Determine {{var:I_4}}, {{var:I_S}} and {{var:V_2}}.

My solution: I named
the top node **1**, and the other **2**:

::: figure assets/practice/b11s-example-7-2-4.jpg

:::

```sym 7
s\dc("e,1,0,12:r1,1,2,6.8'k:r2,2,0,18'k:r3,2,0,2'k:r4,1,0,8.2'k")
```
```sym 8
s\dc("e,1,0,12:r1,1,2,6.8'k:r2,2,0,18'k:r3,2,0,2'k:r4,1,0,8.2'k")
```
```field 9 Circuit Description
e,1,0,12
r1,1,2,6.8'k
r2,2,0,18'k
r3,2,0,2'k
r4,1,0,8.2'k
```

Answers: `v2` is {{o:2.51}} V, {{v7|`-ie`}}{{v8|`–ie`}}{{v9|the opposite of `ie`}} (i.e. {{var:I_S}}) is {{o:2.86}} mA and
`ir4` is {{o:1.46}} mA.

:::

::: problem B11's Example 7.7

::: figure assets/practice/b11s-example-7-7-5.jpg

:::

I have labelled the node names I used. My solution:

```sym 7
s\dc("e1,0,1,6:e2,0,2,18:r1,1,a,5:r2,a,2,3:r3,1,b,6:r4,b,2,2")
```
```sym 8
s\dc("e1,0,1,6:e2,0,2,18:r1,1,a,5:r2,a,2,3:r3,1,b,6:r4,b,2,2")
```
```field 9 Circuit Description
e1,0,1,6
e2,0,2,18
r1,1,a,5
r2,a,2,3
r3,1,b,6
r4,b,2,2
```

Answers: `vr1` is {{o:7.5}} V, `vr3` is {{o:9}} V. For {{var:V_ba}}, `vb-va`
is {{o:-1.5}} V. For {{var:I_S}}, {{v7|`-ie2`}}{{v8|`–ie2`}}{{v9|the opposite of `ie2`}} is {{o:3}} A.

:::

::: problem B11's Figure 7.32

Determine {{var:I_6}} and {{var:V_6}}.

::: figure assets/practice/b11s-figure-7-32-6.jpg

:::

My solution:

```sym 7
s\dc("e,1,0,240:r1,1,2,5:r2,2,0,6:r3,2,3,4:r4,3,0,6:r5,3,4,1:r6,4,0,2")
```
```sym 8
s\dc("e,1,0,240:r1,1,2,5:r2,2,0,6:r3,2,3,4:r4,3,0,6:r5,3,4,1:r6,4,0,2")
```
```field 9 Circuit Description
e,1,0,240
r1,1,2,5
r2,2,0,6
r3,2,3,4
r4,3,0,6
r5,3,4,1
r6,4,0,2
```

Answers: `ir6` is {{o:10}} A, and `vr6` is {{o:20}} V.

:::

::: problem B11's Example 7.10

Calculate the indicated currents and voltages.

::: figure assets/practice/b11s-example-7-10-7.jpg

:::

My solution:

```sym 7
s\dc("r2,2,3,8'k:r1,3,4,4'k:r3,1,2,12'k:r4,1,4,24'k:
r5,1,0,12'k:e,4,0,72:r6,4,5,12'k:r7,5,0,9'k:r8,5,6,3'k:r9,0,6,6'k")
```
```sym 8
s\dc("r2,2,3,8'k:r1,3,4,4'k:r3,1,2,12'k:r4,1,4,24'k:
r5,1,0,12'k:e,4,0,72:r6,4,5,12'k:r7,5,0,9'k:r8,5,6,3'k:r9,0,6,6'k")
```
```field 9 Circuit Description
r2,2,3,8'k
r1,3,4,4'k
r3,1,2,12'k
r4,1,4,24'k
r5,1,0,12'k
e,4,0,72
r6,4,5,12'k
r7,5,0,9'k
r8,5,6,3'k
r9,0,6,6'k
```

Answers: `ir5` is {{o:3}} mA, {{v7|`-ie`}}{{v8|`–ie`}}{{v9|the opposite of `ie`}} (i.e. {{var:I_S}}) is {{o:7.36}} mA, and
`vr7` is {{o:19.6}} V.

:::

::: problem B11's Example 7.4

Determine the currents {{var:I_1}}, {{var:I_2}}, {{var:I_A}}, {{var:I_B}} and
{{var:I_C}}, and the voltage drop in areas A, B and C.

::: figure assets/practice/b11s-example-7-4-8.jpg

:::

My solution:

```sym 7
s\dc("e,1,0,16.8:r1,1,2,9:r2,1,2,6:r3,2,3,4:r4,3,0,6:r5,3,0,3:r6,2,0,3")
```
```sym 8
s\dc("e,1,0,16.8:r1,1,2,9:r2,1,2,6:r3,2,3,4:r4,3,0,6:r5,3,0,3:r6,2,0,3")
```
```field 9 Circuit Description
e,1,0,16.8
r1,1,2,9
r2,1,2,6
r3,2,3,4
r4,3,0,6
r5,3,0,3
r6,2,0,3
```

Current {{var:I_1}} is found via `ir1` = {{o:1.2}} A, {{var:I_2}} via `ir2` =
{{o:1.8}} A, {{var:I_A}}, via {{v7|`-ie`}}{{v8|`–ie`}}{{v9|the opposite of `ie`}} = {{o:3}} A, {{var:I_B}} via `ir3` =
{{o:1}} A and {{var:I_C}} via `ir6` = {{o:2}} A. The voltage drop in area A is
`vr1` = {{o:10.8}} V; in both B and C it is `v2` = {{o:6}} V.

:::

::: problem B11's Example 6.15

::: figure assets/practice/b11s-example-6-15-9.jpg

:::

My solution:

```sym 7
s\dc("e,1,0,28:r1,1,0,1.6'k:r2,1,0,20'k:r3,1,0,56'k")
```
```sym 8
s\dc("e,1,0,28:r1,1,0,1.6'k:r2,1,0,20'k:r3,1,0,56'k")
```
```field 9 Circuit Description
e,1,0,28
r1,1,0,1.6'k
r2,1,0,20'k
r3,1,0,56'k
```

- {{v7,8|Evaluating `re` gets}}{{v9|`re` is}} the total resistance: {{o:1.44}} kΩ
- {{v7,8|Evaluating `ir1` gets}}{{v9|`ir1` is}} {{o:17.5}} mA, {{v7,8|`ir2` gets}}{{v9|`ir2` is}} {{o:1.4}} mA, and {{v7,8|`ir3` gets}}{{v9|`ir3` is}} {{o:0.5}} mA
- {{v7,8|Evaluating }}{{v7|`-pe`}}{{v8|`–pe`}}{{v9|Flipping the sign of `pe`}} gets the power: {{o:543}} mW

These are the correct answers.

:::

::: problem B11's Figure 7.40

Determine {{var:V_b}} and {{var:V_c}}.

::: figure assets/practice/b11s-figure-7-40-10.jpg

:::

My solution:

```sym 7
s\dc("e,a,0,120:r1,a,b,10:r2,b,c,20:r3,c,0,30:
rl1,a,0,20:rl2,b,0,20:rl3,c,0,20")
```
```sym 8
s\dc("e,a,0,120:r1,a,b,10:r2,b,c,20:r3,c,0,30:
rl1,a,0,20:rl2,b,0,20:rl3,c,0,20")
```
```field 9 Circuit Description
e,a,0,120
r1,a,b,10
r2,b,c,20
r3,c,0,30
rl1,a,0,20
rl2,b,0,20
rl3,c,0,20
```

Answers: `vb` is {{o:66.21}} V, and `vc` is {{o:24.83}} V.

:::

::: problem B11's Example 8.10

Determine the current through each resistor.

::: figure assets/practice/b11s-example-8-10-11.jpg

:::

My solution:

```sym 7
s\dc("e1,1,0,15:r1,1,a,4:e3,3,0,20:r3,3,a,10:e2,0,2,40:r2,a,2,5")
```
```sym 8
s\dc("e1,1,0,15:r1,1,a,4:e3,3,0,20:r3,3,a,10:e2,0,2,40:r2,a,2,5")
```
```field 9 Circuit Description
e1,1,0,15
r1,1,a,4
e3,3,0,20
r3,3,a,10
e2,0,2,40
r2,a,2,5
```

::: only 7,8
Through an array, and using the `approx` command, we ask for all the three
answers:
:::

```sym 7
approx({ir1,ir2,ir3})
```
```sym 8
approx({ir1,ir2,ir3})
```

::: only 7,8
The calculator returns {{o:{4.77,7.18,2.41}}} meaning {{var:I_R1}} ={{o:4.77}}A,
{{var:I_R2}} ={{o:7.18}}A and {{var:I_R3}} ={{o:2.41}}A. These are the correct answers. We
could get this answer in a single-line command:
:::
::: only 9
Reading the current through each of the three resistors, `ir1`, `ir2` and
`ir3`:
{{var:I_R1}} ={{o:4.77}}A, {{var:I_R2}} ={{o:7.18}}A and {{var:I_R3}} ={{o:2.41}}A. These are the
correct answers.
:::

```sym 7
s\dc("e1,1,0,15:r1,1,a,4:e3,3,0,20:r3,3,a,10:e2,0,2,40:r2,a,2,5"):
approx({ir1,ir2,ir3})
```
```sym 8
s\dc("e1,1,0,15:r1,1,a,4:e3,3,0,20:r3,3,a,10:e2,0,2,40:r2,a,2,5"):
approx({ir1,ir2,ir3})
```

{{v7,8|Moving forward, we will often use this single-line approach for getting
our answers.}}

:::

::: problem B11's Example 7.6

::: figure assets/practice/b11s-example-7-6-12.jpg

:::

My solution:

```sym 7
s\dc("e,1,0,24:r1,1,2,6:r2,1,2,6:r3,1,2,2:r4,2,0,8:r5,2,0,12")
```
```sym 8
s\dc("e,1,0,24:r1,1,2,6:r2,1,2,6:r3,1,2,2:r4,2,0,8:r5,2,0,12")
```
```field 9 Circuit Description
e,1,0,24
r1,1,2,6
r2,1,2,6
r3,1,2,2
r4,2,0,8
r5,2,0,12
```

Answer: {{v7|`-ie`}}{{v8|`–ie`}}{{v9|The opposite of `ie`}} is {{var:I_S}}={{o:4}} A, `ir2` is {{var:I_2}} = {{o:.8}} A, `ir4`
is {{var:I_4}}={{o:2.4}} A, `vr1` is {{var:V_1}}={{o:4.8}} V, `vr5` is
{{var:V_5}}={{o:19.2}} V.

:::

::: problem B11's Example 7.11

::: figure assets/practice/b11s-example-7-11-13.jpg

:::

My solution:

```sym 7
s\dc("e1,a,0,20:e2,a,b,5:e3,c,0,8:r1,a,c,10:r2,b,c,4:r3,b,0,5")
```
```sym 8
s\dc("e1,a,0,20:e2,a,b,5:e3,c,0,8:r1,a,c,10:r2,b,c,4:r3,b,0,5")
```
```field 9 Circuit Description
e1,a,0,20
e2,a,b,5
e3,c,0,8
r1,a,c,10
r2,b,c,4
r3,b,0,5
```

Answers: `va`={{o:20}} V, `vb`={{o:15}} V, `vc`={{o:8}} V, `va-vc`= {{o:12}} V,
`vb-vc`={{o:7}} V, `ir2`={{o:1.75}} A, {{var:I_S}} via {{v7|`-ie3`}}{{v8|`–ie3`}}{{v9|the opposite of `ie3`}}={{o:-2.95}} A

:::

::: problem B11's Example 8.24

Find the voltage drop in the 3Ω resistor.

::: figure assets/practice/b11s-example-8-24-14.jpg

:::

My solution:

```sym 7
s\dc("e8,1,0,8:r2,1,2,2:r4,2,0,4:r6,2,3,6:r3,3,0,3:r10,3,4,10:e1,0,4,1")
```
```sym 8
s\dc("e8,1,0,8:r2,1,2,2:r4,2,0,4:r6,2,3,6:r3,3,0,3:r10,3,4,10:e1,0,4,1")
```
```field 9 Circuit Description
e8,1,0,8
r2,1,2,2
r4,2,0,4
r6,2,3,6
r3,3,0,3
r10,3,4,10
e1,0,4,1
```

{{v7,8|Now, evaluating **vr3** via `approx(vr3)` finds}}{{v9|The voltage drop `vr3` shows}} that {{var:V_3Ω}} is {{o:1.1}} V. This is
correct.

:::

::: problem B11's Example 8.18

Find the current through the 10Ω resistor in the network shown.

::: figure assets/practice/b11s-example-8-18-15.jpg

:::

My solution:

```sym 7
s\dc("e15,1,0,15:r10,1,2,10:r8,1,3,8:r5,3,2,5:r3,3,0,3:r2,2,0,2"):
approx(ir10)
```
```sym 8
s\dc("e15,1,0,15:r10,1,2,10:r8,1,3,8:r5,3,2,5:r3,3,0,3:r2,2,0,2"):
approx(ir10)
```
```field 9 Circuit Description
e15,1,0,15
r10,1,2,10
r8,1,3,8
r5,3,2,5
r3,3,0,3
r2,2,0,2
```

::: only 9
The answer you want is `ir10`, in **Results**.

Here we use **Rounding** — *approx to n digits*, with **n** = 3.
:::

We find that `ir10` = {{o:1.22}} A.

:::

::: problem B11's Example 8.26

Find the voltage drop in the 2Ω resistor.

::: figure assets/practice/b11s-example-8-26-16.jpg

:::

My solution is below:

```sym 7
s\dc("e,1,0,240:r1,1,2,3:r2,2,3,4:r3,3,4,1:
r4,4,5,2:r5,3,5,6:r6,2,5,6:r7,5,0,9")
```
```sym 8
s\dc("e,1,0,240:r1,1,2,3:r2,2,3,4:r3,3,4,1:
r4,4,5,2:r5,3,5,6:r6,2,5,6:r7,5,0,9")
```
```field 9 Circuit Description
e,1,0,240
r1,1,2,3
r2,2,3,4
r3,3,4,1
r4,4,5,2
r5,3,5,6
r6,2,5,6
r7,5,0,9
```

{{v7,8|Evaluating `approx(vr4)`, we find}}{{v9|`vr4` gives}} the
voltage drop in {{var:R_4}} (the 2Ω resistor): it is {{o:10.67}} V

:::

### Circuits with ‘hidden source'

Sometimes the schematics of circuits are presented in such a way that sources
of voltage are not shown explicitly, yet their voltage is provided. These are
what I call ‘hidden source' problems. Below I offer two examples of these
types of problems. Both are taken from the textbook *Circuit Analysis: Theory
and Practice* (3ed) by Allan H. Robbins and Wilhelm C. Miller, to which from
this point on we will refer as **RM3**.

::: problem RM3's Example 7-5 (Hidden source)

Find the indicated currents and voltages.

::: figure assets/practice/rm3s-example-7-5-hidden-source-17.jpg

:::

In my solution below, notice I introduced two sources, one for 12V and one
for -6V:

```sym 7
s\dc("e1,1,0,12.:r1,1,b,10:r2,b,a,10:r3,a,2,50:
r4,b,2,30:e2,2,0,-6"):approx({ir1,ir2,ir4,va-vb})
```
```sym 8
s\dc("e1,1,0,12.:r1,1,b,10:r2,b,a,10:r3,a,2,50:
r4,b,2,30:e2,2,0,–6"):approx({ir1,ir2,ir4,va-vb})
```
```field 9 Circuit Description
e1,1,0,12.
r1,1,b,10
r2,b,a,10
r3,a,2,50
r4,b,2,30
e2,2,0,-6
```

::: only 9
The answers you want are `ir1`, `ir2` and `ir4`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
va-vb
```

Here we use **Rounding** — *approx to n digits*, with **n** = 3.
:::

::: only 7,8
The answer, {{o:{.6,.2,.4,-2.}}}, indicates {{var:I_1}}={{o:.6}} A, {{var:I_2}}={{o:.2}} A,
{{var:I_3}}={{o:.4}} A and {{var:V_ab}}={{o:-2}} V. This is correct.
:::
::: only 9
The answer is {{var:I_1}}={{o:.6}} A, {{var:I_2}}={{o:.2}} A, {{var:I_3}}={{o:.4}} A and
{{var:V_ab}}={{o:-2}} V. This is correct.
:::

:::

::: problem RM3's Figure 7-16 (Hidden source)

Find the total circuit resistance, and the indicated currents and voltages.

::: figure assets/practice/rm3s-figure-7-16-hidden-source-18.jpg

:::

My solution:

This is how I named the nodes: the top, **1**; the bottom, **2**, and **a**
and **b** as in the figure. In my solution below, notice I introduced two
sources, one for -10V and one for -2V:

```sym 7
s\dc("r1,1,b,4'k:r2,1,a,3'k:r3,b,a,2'k:r4,b,a,3'k:r5,1,b,1'k:
rt,a,2,6'k:e1,1,0,-2:e2,2,0,-10"): approx({(v1-v2)/irt,irt,ir1,ir2,va-vb})
```
```sym 8
s\dc("r1,1,b,4'k:r2,1,a,3'k:r3,b,a,2'k:r4,b,a,3'k:r5,1,b,1'k:
rt,a,2,6'k:e1,1,0,–2:e2,2,0,–10"): approx({(v1-v2)/irt,irt,ir1,ir2,va-vb})
```
```field 9 Circuit Description
r1,1,b,4'k
r2,1,a,3'k
r3,b,a,2'k
r4,b,a,3'k
r5,1,b,1'k
rt,a,2,6'k
e1,1,0,-2
e2,2,0,-10
```

::: only 7,8
The answer we get indicates that the equivalent resistance, given by

$$
\dfrac{v_1 - v_2}{I_T}
$$

is {{o:7.2}} kΩ, and that
{{var:I_T}}={{o:1.11}} mA, {{var:I_1}}={{o:.133}} mA,
{{var:I_2}}={{o:.444}} mA and {{var:V_ab}}={{o:-0.8}} V. This is correct.
:::

::: only 9

Here we use **Rounding** — *approx to n digits*, with **n** = 3.

Three answers are given directly in **Results**. The values of `irt`, `ir1` and `ir2` tell us that {{var:I_T}}={{o:1.11}} mA, {{var:I_1}}={{o:.133}} mA, and {{var:I_2}}={{o:.444}} mA.

The other two answers can be found using **Evaluate**. The equivalent resistance, given by the expression:

$$
\dfrac{v_1 - v_2}{I_T}
$$

is found by evaluating:

```field 9 Evaluate
(v1-v2)/irt
```

which gives a value of {{o:7.2}} kΩ.

And the value of {{var:V_ab}} is found by evaluating:

```field 9 Evaluate
va-vb
```

which gives the value of {{o:-0.8}} V. This is correct.
:::

:::

:::
