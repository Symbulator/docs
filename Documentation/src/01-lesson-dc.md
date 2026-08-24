---
id: lesson-dc
kind: lesson
title: Direct current analysis
updated: 2023-07-08
summary: >
  Learn to describe a circuit in Symbulator, and how to run a *direct current*
  analysis using **dc**. Learn how to describe a *voltage source* using **e**,
  and a *resistor* (or a conductance) using **r**.
---

I firmly believe one learns best by *doing*. Because of this, I have written this
documentation of Symbulator as a tutorial, where you can learn how to use
Symbulator by working through a series of progressively more diverse and more
complex examples.

In a minute, I'll teach you how to swim. But for now, let's jump right into the
water!

## Run a direct current analysis {#run-dc}

{{v7|I want you to make MAIN the current folder in your calculator, delete all
variables you don't need (ideally, the current folder should be empty), and
type this:}}{{v8|I want you to create a new document in your calculator, or to
delete all variables you don't need from your current one (ideally, the current
document should be empty), and type this:}}{{v9|Open Symbulator 9. If you already
have it installed as a local app, then just open that app. If you do *not* have it locally, 
open the **[online app](https://symbulator.pythonanywhere.com/)** in a browser connected to the Internet. 
Once it is open, in the box labelled **Circuit Description**, type this — one element per
line:}}

```sym 7
s\dc("e1,1,0,36:r1,1,2,1'k:r2,2,3,3'k:r3,3,0,2'k")
```
```sym 8
s\dc("e1,1,0,36:r1,1,2,1'k:r2,2,3,3'k:r3,3,0,2'k")
```
```field 9 Circuit Description
e1,1,0,36
r1,1,2,1'k
r2,2,3,3'k
r3,3,0,2'k
```

::: only 7,8
Now I want you to press ENTER.
:::
::: only 9
Just below the box are two menus. Set **Type of analysis** to *Solve
circuit* and **Analysis** to *DC — direct current*. Then click the
**Run Symbulator** button.
:::

::: only 7
If you typed everything correctly and your calculator is properly set up with
Symbulator, you should have seen BUSY appear in the bottom right corner of your
screen, and your calculator seemingly go into a trance and spew out a series of
cryptic messages on the screen. Then, after a few seconds, it should have
returned back to normal, displaying a short message of Done.
:::
::: only 8
If you typed everything correctly and your calculator is properly set up with
Symbulator, you should have seen several lines of text appear on the screen,
with a series of cryptic messages. Then, after a few seconds, it should have
displayed a short message of Done.
:::
::: only 9
If you typed everything correctly, the button reads *Solving…* for a moment.
When it changes to "Solved!", the results are ready. Scroll down past the 
Outputs heading and you will find a **Results** section that was not
active before. It presents the results for every node and every element of 
the circuit you just solved.
:::

Congratulations! You have just run your first simulation in Symbulator.

### How does it work

Let's now go over what exactly it is that you typed, one piece at a time.

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
The selections that you made in the **Analysis and Settings** menu tell Symbulator
*what kind of question* you are asking (i.e. what **Type of analysis**) and
*which analysis* answers it. Choosing *Solve circuit* and *DC — direct current*
tells Symbulator that you want to solve a direct current circuit. Everything else 
on *Analysis and Settings* is optional. You will meet the other menus and
cards in later lessons, and until then they can be left exactly as they are.
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
The most important input you need to give Symbulator is the description of the 
circuit you want to analyse. That input goes inside the **Circuit Description** area, 
and takes the form of a series of lines of text, each one describing an element.{{i:circuit description}}
:::

```sym 9
e1,1,0,36
r1,1,2,1'k
r2,2,3,3'k
r3,3,0,2'k
```

::: only 9
A new line is the ordinary way to separate one element from the next, and it is
what you will see throughout this tutorial: it keeps a long circuit readable,
and it makes a mistake easy to find, because each line stands alone. Symbulator
also accepts a colon as a separator, which is how the calculator versions have
always done it. This is the same circuit in one line: 
:::

```sym 9
e1,1,0,36:r1,1,2,1'k:r2,2,3,3'k:r3,3,0,2'k
```

::: only 7,8
In terms of the simulation, the results of doing it this way are exactly the
same as doing it in a single step. I like to use **cir** as the name of the
variable where I store my circuits, and that's what you will see in this
tutorial. But you are free to use any other valid variable name. Throughout
this text, you will see both ways being used.
:::

::: only 9
You do not have to retype a circuit you have used before. You can save it, 
along with all the other current settings and inputs, into something called
an **entry**, so you can use them in the future. You can save this entry, along 
with other entries like it, in something called an **input file**. When you create 
an input file or an entry you will be asked to give names to both. Input files 
must have the .cir extension.
:::

### Look at the elements

Now let's examine the contents of the circuit description. {{v7,8|Study it, and
you will see that there are three colons in it. In Symbulator, colons are used
to separate elements in a circuit description. Thus, putting the colons aside,
we can see that in this description there are four elements being
described:}}{{v9|Study it, and you will see it has four lines. Each line describes
one element.}}

- The first one is `e1,1,0,36`
- the second one is `r1,1,2,1'k`
- the third one is `r2,2,3,3'k`
- the fourth one is `r3,3,0,2'k`

At the moment, they may look cryptic and indecipherable. But by the time you
are done with this lesson, you will be able to understand them with ease.

## How to describe a resistor {#describe-resistor}

Notice that the second, third and fourth elements in the list all start with
the letter **r**. These are resistors.{{i:resistor}}

::: note Describing resistors
In Symbulator, an ideal resistor is described with four pieces of information,
separated by commas, as follows: a unique name to identify the resistor (which
must start with the letter **r**), the names of the first and second node of
the resistor, and the value of the resistor in ohms (Ω).

For example, an ideal resistor called **r1**, connected between two nodes
called **a** and **b** with a resistance of **300** Ω, would be described in
Symbulator as follows: `r1,a,b,300`
:::

### How to name resistors

Every resistor in your circuit must have a name. As long as it starts with the
letter **r**, and as long as it is unique, this name can be whatever you want.

::: only 7
With one exception: the variable `rc` is reserved in the TI-89 calculator. You
cannot use rc as a name for a resistor or anything else.

::: warning Can't touch rc
The variable `rc` is reserved by the calculator, and cannot be used as a name.
:::
:::
::: only 8
There are two exceptions I know of so far: the names `r` and `rr` should not be
used as names for resistors, because some of the variables they generate as
answers have the same name as reserved variables.

::: warning Can't touch r or rr
The names `r` and `rr` cannot be used, because their answers conflict with
reserved variables in the calculator.
:::
:::
::: only 9
::: tip No reserved names
Pending.
:::
:::

### How to name nodes

Naming the nodes in a circuit is the first thing we all do before we analyse it. 
In a circuit description for Symbulator, every node in
your circuit must have a name. Node names must be unique: no other node or
circuit element should have the same name. As long as these names are unique,
they can be whatever you want, with 
{{v7,8|two constraints. The first one is that:}}{{v9|one constraint:}}
 at least one node should be called **0** (zero). This will be considered the
*ground node* of your circuit{{i:ground node}} and will have, by definition, a
voltage of 0 volts.

::: warning You need a ground node
Every circuit in Symbulator must have a node called 0 to serve as reference or
ground node.
:::

::: only 7
The second restriction is that you cannot use variables that are reserved in
the calculator as names. Besides rc, discussed above, there are others, such as
c1, c2, c3 … c99. Others, more exotic, are listed in the User's Manual of the
calculator.
:::
::: only 8
The second restriction is that you cannot use variables that are reserved in
the calculator as names. These are listed in the User's Manual of the
calculator.
:::

### Values can use SI prefixes

The values of circuit elements are often given using prefixes of the
International System (SI), such as kilo, milli, micro, etc. Because of this,
Symbulator includes a shorthand that helps it understand SI prefixes. Whenever
an SI prefix is used in the value of an element in a circuit description,
preceded by an apostrophe, Symbulator will multiply it by the corresponding
factor, using exact values.{{i:SI prefixes}}

::: tip Prefixes welcome!
You can use SI prefixes, preceded by an apostrophe, in the values of your
elements, and Symbulator will understand this as shorthand to multiply that
value by the corresponding factor.
:::

So, for example, the value of a 3 kΩ resistor can be described to Symbulator as
`3'k`, and it will understand that this means $3 \times 10^{3}$. The value of
an 8 kΩ resistor can be entered in many ways: `8000`, `8'k`, `8000.` and `8E3`
are all equivalent, except that the first two will be treated as exact values,
while the other two will be treated as approximate values.

## What answers do you get {#dc-answers}

After the simulation in DC is complete, Symbulator {{v7,8|stores a series of
answers in the calculator's memory, labelled with easy to remember names for
your convenience}}{{v9|fills in the **Results** section for you, under
**[ O U T P U T S ]**. Nothing is hidden away: every answer it worked out is
on the page, and reading them is a matter of scrolling and looking}}.

::: only 9
The **Results** section comes in two parts. **Node voltages** first, one line
per node, and then **Results by element**, which gives each element a small
block of its own headed by its name and its kind — `r1` *resistor*, `e1`
*voltage source*.

Every answer is written the way you would write it by hand, as a named quantity
and its value: v{{sub:1}} = 36 V, i{{sub:r1}} = 6 mA. You never type
those names — they are labels, there so you know what you are looking at.

::: tip How answers are shown, and how to change it
Out of the box, Symbulator answers *exactly*. It works symbolically, so it
would rather tell you a current is 3/500 A than round it off. That is the right
default for a machine doing algebra, and in the symbolic lessons later on it is
exactly what you want: an answer of v{{sub:in}}·r{{sub:2}}/(r{{sub:1}}
+ r{{sub:2}}) cannot be rounded, and should not be.

For numerical work like this lesson, decimals read better. Open the
**Settings** card and set **Rounding** to *approximate to n significant digits*
with **n** = 3, then tick **Use SI prefixes in answers**. The current above
then reads 6 mA instead of 3/500 A.

One thing to expect: ticking the prefix box moves **Rounding** off *exact* by
itself, because a prefixed value is a decimal. Symbulator says so on screen
rather than doing it silently, and the reverse happens too — choose *exact*
again and the prefixes switch off.

Throughout this tutorial the numerical examples assume approximate answers to
three or four figures with prefixes on, and the symbolic ones assume *exact*.
Where a change is needed, the text says so.
:::
:::

### Answer for each node

For each node used in the description of the circuit, its voltage with
reference to the ground is {{v7,8|stored in a variable called v plus the name of
the node. For example, for a node called 1, its voltage is stored in a variable
called v1}}{{v9|shown under **Node voltages**, labelled *v* with the node's name
below it. Node 1 appears as `v1`}}.

### Answers for each resistor

For each resistor included in the description of the circuit, the following
answers are calculated:

- The voltage drop in the resistor, that is to say, the voltage in the first
  node declared minus the voltage in the second node declared, in volts. For a
  resistor called r5, this is {{v7,8|stored in `vr5`}}{{v9|the line marked
  **voltage drop**, labelled `vr5`}}.
- The current through the resistor, flowing from the first node towards the
  second, in amperes. For a resistor called rx, this is {{v7,8|stored in
  `irx`}}{{v9|the line marked **current through**, labelled `irx`}}.
- The power consumed by the resistor, in watts. For a resistor called r12, this
  is {{v7,8|stored in `pr12`}}{{v9|the line marked **power consumed**, labelled
  `pr12`}}.

By now, you should be able to understand the description of the second, third
and fourth elements in our example.

## How to describe a voltage source {#describe-voltage-source}

The first element in our example, on the other hand, started with the letter
**e**. This element is a voltage source.{{i:voltage source}}

::: note Describing voltage sources
In Symbulator, a voltage source is described with four pieces of information,
separated by commas, as follows: a unique name to identify the source (which
must start with the letter **e**), the name of the positive node of the source,
the name of the negative node of the source, and the value of the source in
volts (V).

For example, an ideal voltage source called **e1**, connected with its positive
terminal in node **3** and with its negative terminal in the ground node **0**,
with a value of 12 volts, would be described as follows: `e1,3,0,12`
:::

### How to name voltage sources

Every voltage source in your circuit must have a unique name that starts with
the letter **e**, and it can be whatever you want.

### Values can use SI prefixes

The values of a voltage source in the circuit description can also use SI
prefixes. They can be used in the values of all elements in the circuit
description.

### Answers for a voltage source

For each voltage source included in the description of the circuit, the
following answers are calculated:

- The voltage drop in the source, that is, the voltage in the first node
  declared minus the voltage in the second node declared, in volts. For a
  source called e5, {{v7,8|`ve5`}}{{v9|the **voltage drop** line,
  `ve5`}}.
- The current through the source, flowing from the first node towards the
  second, in amperes. For a source called ex, {{v7,8|`iex`}}{{v9|the
  **current through** line, `iex`}}.
- The power consumed — attention: not delivered, but consumed — by the source,
  in watts. For a source called e12, {{v7,8|`pe12`}}{{v9|the **power consumed**
  line, `pe12`}}. If we want the power delivered, we ask for the
  negative of this value.
- The equivalent resistance of the rest of the circuit, as seen by the source.
  For a source called e2, {{v7,8|`re2`}}{{v9|the **resistance seen** line, `re2`}}.

::: note This last one belongs to sources only
That equivalent resistance is a property of the *view from a source*, not a
per-element quantity, so it exists only for sources. There is no
{{v7,8|`rr1`}}{{v9|`rr1`}} for a resistor — a resistor's resistance
is the value you gave it. {{v9|Look at any resistor's block in **Results by
element** and you will see three lines, not four: current, voltage and power,
and no resistance seen.}} The same applies to the impedance answers in AC
analysis, which you will meet in {{ref:lesson-ac}}.
:::

## A numerical DC simulation, step by step {#step-by-step}

Let's go back now to the simulation we ran earlier. That simulation corresponds
to the circuit given in Example 5.7 in Boylestad's *Introductory Circuit
Analysis* (11ed). Moving forward, I will refer to that textbook as **B11**.

For your benefit, the problem statement and the circuit schematic have been
scanned and are reproduced below, exactly as they appear in the textbook. This
will be the case in every other problem shown in this tutorial. Since this is
for educational purposes, it is my understanding that it falls squarely within
the "fair use" doctrine of copyright law. In any event, no copyright
infringement is meant.

::: problem B11's Example 5.7
::: figure assets/circuit/b11e0507.jpg
B11's Example 5.7
:::

::: answer
As you can see, all the values in this circuit are numbers: no element values
are unknown. This is an example of a **numerical circuit**. A circuit is
numerical if we know the numerical value of every element in it.

I will now walk you step by step through the solution of this numerical
problem. The process you will see here applies to most numerical simulations in
Symbulator. First, you describe the circuit. Then, you run the simulation.
Finally, you get the answers.

**Step 1: describe the circuit.** The first step in solving a circuit is to
describe it. Circuit description starts with **naming the nodes**. As we
mentioned earlier, you can call the nodes anything you want, be it a number or
a letter, as long as the name is unique. But you must always have one node
called 0 (zero); this is your ground node and has a voltage of 0 V. In this
particular circuit, the ground node is indicated with the ground symbol, but
that is not always the case. When it is not marked, you pick a node to serve as
zero.

I labelled the nodes in this circuit, starting in the ground and moving
clockwise, as 0, 1, 2 and 3. It helps me to pencil the names in the schematic
itself.

::: tip Write 'em down!
I strongly recommend that you write down the names of your nodes and your
elements onto the circuit schematic itself, so you don't forget who's who.
:::

::: figure assets/circuit/b11e0507b.jpg
B11's Example 5.7, with the node names pencilled in
:::

After naming the nodes, I am ready to describe the elements of the circuit in
Symbulator notation.

Let's start with the source: when I only have one voltage source, like here, I
enjoy {{v7,8|naming it with a single letter: e}}{{v9|giving it a short name: e1}}. Having chosen a name for it,
I can now describe the voltage source as follows:
{{v7,8|`e,1,0,36`}}{{v9|`e1,1,0,36`}}, given that its name is
{{v7,8|e}}{{v9|e1}}, its positive node is called 1, its negative node is called
0, and its value is 36 volts between these nodes in that order.

::: only 9
A bare `e` is one of the few names Symbulator 9 will not accept. It builds an
answer's name out of the quantity and the element, so an element called `e`
would report its resistance as `re` — and `re` already means something else to
the mathematics underneath. Symbulator refuses the name rather than quietly
reading it wrong, and suggests `e1`. The same goes for a handful of other short
names; you will be told plainly if you pick one.
:::

Now I describe the resistors. I named the first resistor r1, and I described it
as follows: `r1,1,2,1'k`, because its name is r1, its first node is called 1,
its second node is called 2, and its value is 1 kΩ. The second resistor we
describe similarly: `r2,2,3,3'k` and likewise for the third resistor:
`r3,3,0,2'k`.

::: note An important point about SI prefixes
In the case of kilo, we can write it as either `'k` or `'K`. But that's not the
case for every other SI prefix: their case matters. For example, `'m` means
milli, while `'M` means mega. {{v7,8|Symbulator's custom menu includes the
spelling of all SI prefixes.}}
:::

::: only 7,8
We pass the description of a circuit to Symbulator as a string. This means we
open with a quotation mark, then enter the descriptions of each element as
above, separated with colons, and then close with a quotation mark. We can
store this string in a variable, like this:
:::
::: only 9
Those four descriptions, gathered together, are the whole circuit. Put them in
the **Circuit description** box, one to a line:
:::

```sym 7
"e,1,0,36:r1,1,2,1'k:r2,2,3,3'k:r3,3,0,2'k"→cir
```
```sym 8
"e,1,0,36:r1,1,2,1'k:r2,2,3,3'k:r3,3,0,2'k"→cir
```
```field 9 Circuit Description
e1,1,0,36
r1,1,2,1'k
r2,2,3,3'k
r3,3,0,2'k
```

**Step 2: run the simulation.** {{v7,8|We can now ask Symbulator to simulate
this circuit in direct current:}}{{v9|The two menus under the box say what kind
of simulation to run. We want a plain solve of the circuit as described, in
direct current, so:}}

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
Symbulator will let you know when it has completed a successful simulation by
saying Done. It took my calculator 16 seconds to solve this circuit. In that
time, Symbulator found a total of 16 answers, and stored each one in a
memorably named variable in the current folder.
:::
::: only 8
Symbulator will let you know when it has completed a successful simulation by
saying Done. It took my calculator under 2 seconds to solve this circuit. In
that time, Symbulator found a total of 16 answers, and stored each one in a
memorably named variable in the current document.
:::
::: only 9
The page fills in below almost immediately — this circuit takes well under a
second — and a line at the foot of the **Results** section tells you what just
happened: *DC analysis · 16 result(s)*, and how long it took. Sixteen answers,
found and displayed in one go.
:::

For a DC analysis, these answers are as follows:

- The **voltage of each node**, so the voltages of nodes 1, 2 and 3 are in
  {{v7,8|v1, v2 and v3}}{{v9|the three lines under **Node voltages**:
  `v1`, `v2` and `v3`}}.
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
So that you interpret the signs of your answers correctly, remember to pay
attention to the details. For example:

- The current in the elements is defined as going through the element from the
  first node to the second node.
- The voltage drop is defined as the voltage of the first node minus the
  voltage of the second node.
- The power given is the power consumed. So, if you want power delivered,
  evaluate the negative of that power.
:::

**Step 3: get the answers.** We can now answer the six questions in the
problem.

*Answer to question (a).* The equivalent resistance as seen by the source
{{v7,8|e}}{{v9|e1}}:

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
Nothing to compute. Find the block headed `e` *voltage source* in **Results by
element**, and read the line marked **resistance seen**:

r{{sub:e}} = 6 kΩ
:::

That is to say, 6 kΩ. Correct.

*Answer to question (b).* Current Is is defined in the schematic as the current
flowing through the source, in the direction that goes from node 0 to node 1.
One way to find this value is evaluating the negative of the current through
the source, which as you know flows in the opposite direction:

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
The **current through** line in the same block reads ie1 = −6 mA. The answer
we want is its opposite, 6 mA.
:::

That is to say, 6 mA. Another way to find the answer, given that this is a
series circuit where all elements have the same current through them, is to
{{v7,8|evaluate the current through any of the resistors}}{{v9|read the
**current through** line of any resistor — all three say 6 mA}}.

*Answer to question (c).* The voltage drop in resistor R1 — since its polarity
is defined in the schematic in the same way it is defined in our circuit
description — is as follows.

::: only 7,8
It is found by evaluating `vr1`: the {{t:machine}} returns `6`, that is 6 V.
For R2, `vr2` gives 18 V. And for R3, `vr3` gives 12 V. These are all the right
answers.
:::
::: only 9
It is already on screen. In the block for `r1`, the **voltage drop** line reads
v{{sub:r1}} = 6 V. Look at the blocks for `r2` and `r3` and you will find
v{{sub:r2}} = 18 V and v{{sub:r3}} = 12 V. These are all the right
answers.
:::

*Answer to question (d).* Since the problem asks for the power supplied by the
source, and we know that {{v7,8|`pe` has}}{{v9|the **power consumed** line of
the source's block, `pe1`, holds}} the power consumed by it, we need
{{v7,8|to evaluate the negative of it, and we get `.216`}}{{v9|its opposite,
which is 216 mW}}, that is 216 mW delivered.

*Answer to question (e).* The power consumed by the resistors is
{{v7,8|found evaluating `pr1`, `pr2` and `pr3`. We get `.036`, `.108` and
`.072`}}{{v9|on the **power consumed** line of each resistor's block:
`pr1` = 36 mW, `pr2` = 108 mW and `pr3` =
72 mW}}, that is 36 mW, 108 mW and 72 mW consumed, respectively.

*Answer to question (f).* Let's ask the {{t:machine}} whether the sum of the
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
The tidiest way to check a balance like this is to add everything up and expect
nothing. If the resistors consume exactly what the source delivers, then all
four powers together must come to zero. In **Evaluate**:

```field 9 Evaluate
pr1 + pr2 + pr3 + pe1
```

The answer is **0** — not a small number, but zero. If you want to be sure it
is genuinely zero and not three digits' worth of rounding, set **Rounding**
back to *exact* for a moment: Symbulator returns to fractions and still
says 0.
:::

This is the right answer, and concludes the solution to this, your first ever
problem in Symbulator.
:::
:::

## Instructive numerical examples, solved {#practice-dc}

::: practice


### Numerical problems in DC using e and r

The following are practice problems taken from several textbooks. They were
chosen because they apply only the concepts that you have learned so far in
Lesson 1. This will allow you to practice these concepts and reinforce them
before moving to Lesson 2.

The problem below comes from Figure 1-26 (a) in Hyatt and Kemmerly's
*Engineering Circuit Analysis* (5ed). Moving forward, we will refer to that
textbook as **HK5**.

::: problem HK5's Figure 1-26

We are asked to determine the current, voltage drop and power consumed in
each resistor, as well as the power *delivered* by each voltage source. We
are also asked to check that the powers in the circuit add up to zero. Here
is my solution.

::: figure assets/practice/hk5s-figure-1-26-1.jpg

:::

Here is my solution.

I named the nodes thus: the bottom node is named **0**, the top nodes, from
left to right, are named **1**, **2** and **3**. My description of the
circuit is given below, followed after a colon by the DC simulation command.

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

- {{v7,8|Evaluating `ir1` or `ir2` gets}}{{v9|The **current through** line of
  either resistor gives}} the current in the resistors: {{o:2}} A
- {{v7,8|Evaluating `vr1` gets}}{{v9|The **voltage drop** line of `r1` gives}}
  the voltage drop in the 30Ω resistor: {{o:60}} V
- Evaluating `vr2` gets the voltage drop in the 15Ω resistor: {{o:30}} V
- Evaluating `pr1` gets the power consumed in the 30Ω resistor: {{o:120}} W
- Evaluating `pr2` gets the power consumed in the 15Ω resistor: {{o:60}} W
- {{v7,8|Evaluating }}{{v7|`-pe1`}}{{v8|`–pe1`}}{{v9|Flipping the sign of `pe1`}} gets the power delivered by the 120V source: {{o:240}} W
- {{v7,8|Evaluating }}{{v7|`-pe2`}}{{v8|`–pe2`}}{{v9|Flipping the sign of `pe2`}} gets the power delivered by the 30V source: {{o:-60}} W. This means this source is actually consuming 60W.
- Evaluating `pr1+pr2+pe1+pe2` gets the sum of powers: {{o:0}} W. As expected.

Wasn't that easy? We could also have asked for all the answers with one
array:

```sym 7
{ir1,vr1,vr2,pr1,pr2,-pe1,-pe2,pr1+pr2+pe1+pe2}
```
```sym 8
{ir1,vr1,vr2,pr1,pr2,–pe1,–pe2,pr1+pr2+pe1+pe2}
```

:::

::: problem B11's Example 5.20

The practice problems will get progressively more complicated as we move on.
This will allow you to build up your *'symbulating'* skills with confidence.

::: figure assets/practice/b11s-example-5-20-2.jpg

:::

I named the nodes clockwise starting from the ground: **0**, **1**, **2**,
**3** and **4**. Below is my circuit description, given as an argument of the
command to do the DC simulation:

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

When it's done, ask for the answers we need. Evaluating `ir1` gets the
current I: {{o:2.5}} A. Evaluating `vr2` gets the voltage drop in the 7Ω
resistor: {{o:17.5}} W

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
e1,1,0,24
r1,1,0,10
r2,1,0,220
r3,1,0,1.2'k
```

- Evaluating {{v7,8|`re`}}{{v9|`re1`}} gets the total resistance: {{o:9.49}} Ω
- {{v7,8|Evaluating }}{{v7|`-ie`}}{{v8|`–ie`}}{{v9|Flipping the sign of `ie1`}} gets us the source current: {{o:2.53}} A
- Evaluating `ir1` gets I{{sub:1}}: {{o:2.4}} A, `ir2` gets I{{sub:2}}: {{o:0.11}} A, and `ir3` gets I{{sub:3}}: {{o:0.02}} A.

:::

::: problem B11's Example 7.2

Determine I{{sub:4}}, I{{sub:S}} and V{{sub:2}}. My solution below. I named
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
e1,1,0,12
r1,1,2,6.8'k
r2,2,0,18'k
r3,2,0,2'k
r4,1,0,8.2'k
```

Answers: `v2` is {{o:2.51}} V, {{v7|`-ie`}}{{v8|`–ie`}}{{v9|the opposite of `ie1`}} (e.g. I{{sub:S}}) is {{o:2.86}} mA and
`ir4` is {{o:1.46}} mA.

:::

::: problem B11's Example 7.7

::: figure assets/practice/b11s-example-7-7-5.jpg

:::

For your benefit, I have labeled the node names I used. My solution:

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

Answers: `vr1` is {{o:7.5}} V, `vr3` is {{o:9}} V. For V{{sub:ba}}, `vb-va`
is {{o:-1.5}} V. For I{{sub:S}}, {{v7|`-ie2`}}{{v8|`–ie2`}}{{v9|the opposite of `ie2`}} is {{o:3}} A.

:::

::: problem B11's Figure 7.32

Determine I{{sub:6}} and V{{sub:6}}.

::: figure assets/practice/b11s-figure-7-32-6.jpg

:::

My solution below:

```sym 7
s\dc("e,1,0,240:r1,1,2,5:r2,2,0,6:r3,2,3,4:r4,3,0,6:r5,3,4,1:r6,4,0,2")
```
```sym 8
s\dc("e,1,0,240:r1,1,2,5:r2,2,0,6:r3,2,3,4:r4,3,0,6:r5,3,4,1:r6,4,0,2")
```
```field 9 Circuit Description
e1,1,0,240
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

My solution below:

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
e1,4,0,72
r6,4,5,12'k
r7,5,0,9'k
r8,5,6,3'k
r9,0,6,6'k
```

Answers: `ir5` is {{o:3}} mA, {{v7|`-ie`}}{{v8|`–ie`}}{{v9|the opposite of `ie1`}} (e.g. I{{sub:S}}) is {{o:7.36}} mA, and
`vr7` is {{o:19.6}} V.

:::

::: problem B11's Example 7.4

Determine the currents I{{sub:1}}, I{{sub:2}}, I{{sub:A}}, I{{sub:B}} and
I{{sub:C}}, and the voltage drop areas A, B and C.

::: figure assets/practice/b11s-example-7-4-8.jpg

:::

My solution below:

```sym 7
s\dc("e,1,0,16.8:r1,1,2,9:r2,1,2,6:r3,2,3,4:r4,3,0,6:r5,3,0,3:r6,2,0,3")
```
```sym 8
s\dc("e,1,0,16.8:r1,1,2,9:r2,1,2,6:r3,2,3,4:r4,3,0,6:r5,3,0,3:r6,2,0,3")
```
```field 9 Circuit Description
e1,1,0,16.8
r1,1,2,9
r2,1,2,6
r3,2,3,4
r4,3,0,6
r5,3,0,3
r6,2,0,3
```

Current I{{sub:1}} is found via `ir1` = {{o:1.2}} A, I{{sub:2}} via `ir2` =
{{o:1.8}} A, I{{sub:A}}, via {{v7|`-ie`}}{{v8|`–ie`}}{{v9|the opposite of `ie1`}} = {{o:3}} A, I{{sub:B}} via `ir3` =
{{o:1}} A and I{{sub:C}} via `ir6` = {{o:2}} A. The voltage drop in area A is
`vr1` = {{o:10.8}} V; in both B and C it is `v2` = {{o:6}} V.

:::

::: problem B11's Example 6.15

::: figure assets/practice/b11s-example-6-15-9.jpg

:::

My solution below:

```sym 7
s\dc("e,1,0,28:r1,1,0,1.6'k:r2,1,0,20'k:r3,1,0,56'k")
```
```sym 8
s\dc("e,1,0,28:r1,1,0,1.6'k:r2,1,0,20'k:r3,1,0,56'k")
```
```field 9 Circuit Description
e1,1,0,28
r1,1,0,1.6'k
r2,1,0,20'k
r3,1,0,56'k
```

- Evaluating {{v7,8|`re`}}{{v9|`re1`}} gets the total resistance: {{o:1.44}} kΩ
- Evaluating `ir1` gets {{o:17.5}} mA, `ir2` gets {{o:1.4}} mA, and `ir3` gets {{o:0.5}} mA
- {{v7,8|Evaluating }}{{v7|`-pe`}}{{v8|`–pe`}}{{v9|Flipping the sign of `pe1`}} gets the power: {{o:543}} mW

These are the correct answers.

:::

::: problem B11's Figure 7.40

Determine V{{sub:b}} and V{{sub:c}}.

::: figure assets/practice/b11s-figure-7-40-10.jpg

:::

My solution below:

```sym 7
s\dc("e,a,0,120:r1,a,b,10:r2,b,c,20:r3,c,0,30:
rl1,a,0,20:rl2,b,0,20:rl3,c,0,20")
```
```sym 8
s\dc("e,a,0,120:r1,a,b,10:r2,b,c,20:r3,c,0,30:
rl1,a,0,20:rl2,b,0,20:rl3,c,0,20")
```
```field 9 Circuit Description
e1,a,0,120
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

My solution below:

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

Through an array, and using the `approx` command, we ask for all the three
answers:

```sym 7
approx({ir1,ir2,ir3})
```
```sym 8
approx({ir1,ir2,ir3})
```

::: only 7,8
The calculator returns {{o:{4.77,7.18,2.41}}} meaning I{{sub:R1}} =4.77A,
I{{sub:R2}} =7.18A and I{{sub:R3}} =2.41A. These are the correct answers. We
could get this answer in a single-line command:
:::
::: only 9
Reading the **current through** line of each of the three resistors:
I{{sub:R1}} =4.77A, I{{sub:R2}} =7.18A and I{{sub:R3}} =2.41A. These are the
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
```field 9 Circuit Description
e1,1,0,15
r1,1,a,4
e3,3,0,20
r3,3,a,10
e2,0,2,40
r2,a,2,5
```

::: only 9
The answers you want are `ir1`, `ir2` and `ir3`, in **Results**.

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

Moving forward, we will often use this single-line approach for getting our
answers.

:::

::: problem B11's Example 7.6

::: figure assets/practice/b11s-example-7-6-12.jpg

:::

My solution below:

```sym 7
s\dc("e,1,0,24:r1,1,2,6:r2,1,2,6:r3,1,2,2:r4,2,0,8:r5,2,0,12")
```
```sym 8
s\dc("e,1,0,24:r1,1,2,6:r2,1,2,6:r3,1,2,2:r4,2,0,8:r5,2,0,12")
```
```field 9 Circuit Description
e1,1,0,24
r1,1,2,6
r2,1,2,6
r3,1,2,2
r4,2,0,8
r5,2,0,12
```

Answer: {{v7|`-ie`}}{{v8|`–ie`}}{{v9|The opposite of `ie1`}} is I{{sub:S}}={{o:4}} A, `ir2 `is I{{sub:2}}=.{{o:8}} A, `ir4`
is I{{sub:4}}={{o:2.4}} A, `vr1` is V{{sub:1}}={{o:4.8}} V, `vr5` is
V{{sub:5}}={{o:19.2}} V.

:::

::: problem B11's Example 7.11

::: figure assets/practice/b11s-example-7-11-13.jpg

:::

My solution below:

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

Answers: `va`={{o:20}}, `vb`={{o:15}}, `vc`={{o:8}}, `va-vc`= {{o:12}},
`vb-vc`={{o:7}}, `ir2`={{o:1.75}}, I{{sub:S}} via {{v7|`-ie3`}}{{v8|`–ie3`}}{{v9|the opposite of `ie3`}}={{o:-2.95}}

:::

::: problem B11's Example 8.24

Find the voltage drop in the 3Ω resistor.

::: figure assets/practice/b11s-example-8-24-14.jpg

:::

My solution below:

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

{{v7,8|Now, evaluating **vr3** via `approx(vr3)` finds}}{{v9|The **voltage
drop** line of the `r3` block shows}} that V{{sub:3Ω}} is {{o:1.1}} V. This is
correct.

:::

::: problem B11's Example 8.18

Find the current through the 10Ω resistor in the network shown below.

::: figure assets/practice/b11s-example-8-18-15.jpg

:::

My solution below:

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

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
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
e1,1,0,240
r1,1,2,3
r2,2,3,4
r3,3,4,1
r4,4,5,2
r5,3,5,6
r6,2,5,6
r7,5,0,9
```

{{v7,8|Evaluating `approx(vr4)`, we find}}{{v9|The `r4` block gives}} the
voltage drop in R{{sub:4}} (the 2Ω resistor): it is {{o:10.67}} V

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

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

The answer, {{o:{.6,.2,.4,-2.}}}, indicates I{{sub:1}}=.6, I{{sub:2}}=.2,
I{{sub:3}}=.4 and V{{sub:ab}}=-2. This is correct.

:::

::: problem RM3's Figure 7-16 (Hidden source)

Find the total circuit resistance, and the indicated currents and voltages.

::: figure assets/practice/rm3s-figure-7-16-hidden-source-18.jpg

:::

My solution below:

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

::: only 9
The answers you want are `irt`, `ir1` and `ir2`, in **Results**.

Ask **Evaluate** for:

```field 9 Evaluate
(v1-v2)/irt
va-vb
```

The calculator versions wrap this in `approx` to get a decimal. Version 9 does that through **Rounding** instead — *approximate to n significant digits* with **n** = 3 is a good setting for this one.
:::

The answer we get indicates that the equivalent resistance, given by
(v{{sub:1}}-v{{sub:2}})/I{{sub:T}}, is {{o:7.2}} KΩ, and that
I{{sub:T}}={{o:1.11}} **m**A, I{{sub:1}}=.{{o:133}} **m**A,
I{{sub:2}}=.{{o:444}} **m**A and V{{sub:ab}}={{o:-0.8}} V. This is correct.

:::

:::
