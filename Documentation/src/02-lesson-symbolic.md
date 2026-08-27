---
id: lesson-symbolic
kind: lesson
title: Symbolic circuits and expert mode
updated: 2023-07-08
summary: >
  Learn how to solve different types of *symbolic* circuits in Symbulator. Use
  the solve command on Symbulator answers. And explore **ex**, the powerful
  *expert mode*, for the ambitious user.
---

Here you will learn about the different types of symbolic circuits and how to
solve them in Symbulator, using the solve command when needed, and — for the
more adventurous users — leveraging the powerful *expert mode*.

## About symbolic problems {#about-symbolic}

The problem we saw in {{ref:lesson-dc}} was a numerical problem because it
involved a numerical circuit: from the start, we knew the numerical values for
all the elements in it. None of them were unknown.

When a circuit has one or more elements for which we do not have a numerical
value, we call it a **symbolic circuit**.{{i:symbolic circuit}} A symbolic
problem is one that involves a symbolic circuit. It gives me great joy when I
encounter a symbolic problem, because the ability to simulate symbolic circuits
is what sets Symbulator apart from other programs.

I find it useful to distinguish between two types of symbolic problems:

- **Purely symbolic problems** are problems that use symbolic circuits where the
  desired answers are also symbolic. The answers are given as expressions of
  unknown variables. Solving them in Symbulator is as straightforward as
  solving numerical problems.
- **Numerical-from-symbolic problems** start with a symbolic circuit, but ask us
  to find numerical answers. This is possible when the problem gives us
  additional information about the circuit.

Numerical-from-symbolic problems can be solved in two ways. If they are simple
— just one or two unknown values, and only one or two numerical answers wanted
— it is time-efficient to simulate the circuit symbolically and then solve for
the numerical answers with the {{v7,8|**solve** command of the
calculator}}{{v9|**Solve** card, which sits under the results and
does exactly that job}}. If they are not simple, it is easier and more
time-efficient to use **expert mode**{{v9|, which version 9 offers in its
**Expert Mode** box}}.

Let's see an example of each.

### Solving a purely symbolic problem

Since Symbulator is natively a symbolic simulator, there is nothing special
about solving a purely symbolic problem. The only limitation comes from the
computing capacity of the {{t:machine}}: {{v7,8|while small circuits can be
solved relatively fast, larger circuits may be too slow to solve and may cause
a memory error}}{{v9|while small circuits are solved almost instantly, large
symbolic circuits can produce expressions too large to be useful}}.

Let's see a simple purely symbolic problem, from *Fundamentals of Electric
Circuits* by Alexander and Sadiku (5th edition), from now on referred to as
**AS5**.

::: problem AS5's Figure 2.29
::: figure assets/circuit/as5f0229.png
AS5's Figure 2.29
:::

::: answer
As you can see, all the values in this circuit are variables: no element values
are known. This is an example of a symbolic circuit. Imagine you are asked to
find symbolic expressions for the current i, the voltage drop in R2, and the
power consumed by R1 and R2. Since we are being asked to find symbolic answers
from a symbolic circuit, this is a purely symbolic problem.

This is how I would describe this circuit. First, I name the nodes. The node
called a in the schematic, I will still call node a. The node called b will
serve as my ground node, so I call it node 0. And the node between the two
resistors, I will call node c.

Then, we name the elements. I will name the source ev, and will call the
resistors r1 and r2. For the values of the elements, I will use variables. The
value of the source will be v, and the values of the resistors will be r1 and
r2. It is not a problem that the symbolic value is the same as the name of the
element.

```sym 7
"ev,a,0,v:r1,a,c,r1:r2,c,0,r2"→cir
s\dc(cir)
```
```sym 8
"ev,a,0,v:r1,a,c,r1:r2,c,0,r2"→cir
s\dc(cir)
```

::: only 9
::: tip Turn rounding back to exact for this lesson
{{ref:lesson-dc}} had you set **Rounding** to *approximate to n significant
digits*, which is right for numbers and pointless here: there is nothing to
round. Open **Settings** and put **Rounding** back to *exact*. The **Use SI
prefixes** tick will clear itself when you do, which is what we want — a
prefix has nothing to attach itself to in an answer like
$v/(r1 + r2)$.
:::

Type the three elements into the box, one to a line:

```field 9 Circuit Description
ev,a,0,v
r1,a,c,r1
r2,c,0,r2
```

Leave **Type of analysis** on *Solve circuit*, set **Analysis** to
*DC — direct current*, and press **Run Symbulator**.
:::

{{v7|This simulation took 15 seconds in my calculator.}}{{v8|This simulation
took a couple of seconds in my calculator.}}{{v9|The answer comes back almost at
once — symbolic circuits this small cost nothing.}} To find the current i, we
{{v7,8|ask for `ir1` or `ir2`}}{{v9|look at the block for `r1` or for `r2` and
read the **current through** line}}. To find the voltage drop on r2, we
{{v7,8|ask for `vr2`}}{{v9|read the **voltage drop** line in the `r2` block}}.

Both are expressions rather than numbers:

$i_{r1} = \dfrac{v}{r1 + r2}$ and
$v_{r2} = \dfrac{r2\,v}{r1 + r2}$

which is the voltage divider you would have written by hand.

To find the power consumed in r2, we {{v7,8|ask for `pr2`}}{{v9|read the
**power consumed** line of the `r2` block}}. To find the power delivered by the
source, we {{v7,8|ask for the negative of `pev`}}{{v9|take the opposite of the
source's **power consumed** line — type `-pev` into **Evaluate**}}.

$p_{r2} = \dfrac{r2\,v^2}{(r1 + r2)^2}$ and
$-p_{ev} = \dfrac{v^2}{r1 + r2}$

It is this ability to simulate symbolically, as if it were nothing, that puts
Symbulator in a league of its own. Getting symbolic answers from a symbolic circuit takes
no extra effort.
:::
:::

## Numerical from symbolic, with solve {#with-solve}

Getting numerical answers from a symbolic circuit, on the other hand, requires
an additional step. This additional step can be the use of the solve command,
as we will see in this next example. Or it can be the use of the expert mode,
as we will see in the example after that.

::: problem B11's Example 5.6, with solve
::: figure assets/circuit/b11e0506.jpg
B11's Example 5.6
:::

::: answer
This is a very nice numerical-from-symbolic problem. We should be able to solve
it into numerical results because, even though the problem hides two values
from us (the value of the source E and of the resistor R1), it gives us in
exchange two answers (the equivalent resistance RT and the current I3) that we
can use to solve for the unknowns.

Since this circuit is structurally identical to B11's Example 5.7 solved in
{{ref:lesson-dc}}, we will use the same names for the nodes. The circuit
description is identical except for the element's values. As values for the
elements in the circuit, Symbulator will accept numbers, variables or even
algebraic expressions. For this example, I will use e for the value of source
e, and r1 for the value of the r1 resistor.

::: only 7,8
::: warning Clean your {{t:container}}
Make sure that the variables you are going to use as symbolic values are empty,
meaning that they do not exist in {{t:container_the}}. You can do this either by
emptying the whole {{t:container}} or by deleting these specific variables from
the memory, thus: `DelVar e,r1`
:::
:::

```sym 7
"e,1,0,e:r1,1,2,r1:r2,2,3,4'k:r3,3,0,6'k"→cir
s\dc(cir)
```
```sym 8
"e,1,0,e:r1,1,2,r1:r2,2,3,4'k:r3,3,0,6'k"→cir
s\dc(cir)
```
```field 9 Circuit Description
e,1,0,e
r1,1,2,r1
r2,2,3,4'k
r3,3,0,6'k
```

::: only 9
Run it in DC, as before.
:::

A moment later, Symbulator is done, and we are ready to answer the questions.
Using the symbolic answers provided by Symbulator and the known answers given
by the problem, we will write two equations, and then solve them for the two
unknowns that interest us.

The problem says that I3 is 6 mA. In Symbulator, I3 is {{v7,8|`ir3`}}{{v9|the
**current through** line of the `r3` block, `ir3`}}, the current
through resistor r3. {{v7,8|If you evaluate it, you will see it produces an
algebraic expression in terms of the two unknowns, e and r1.}}{{v9|Look at it
and you will see an expression rather than a number — $e/(r1 + 10000)$ — in
terms of the two unknowns, e and r1.}} This is what we call a symbolic answer.
The problem also says that RT is 12 kΩ; the equivalent resistance as seen by
the source e is {{v7,8|given by `re`, which when evaluated gives another
algebraic expression in terms of r1}}{{v9|the **resistance seen** line,
`re`, which is $r1 + 10000$}}. We can then write two new equations
and solve them for e and r1{{v7,8|:}}{{v9|.}}

```sym 7
solve(re=12000 and ir3=.006,{e,r1})
```
```sym 8
solve(re=12000 and ir3=.006,{e,r1})
```

::: only 9
That is what the **Solve** card is for. You will find it under the
results, beside **Evaluate**. Open it and fill in two boxes.

In the first, headed **Equation(s) to solve in terms of the results**, write
one equation per line, using the same names the results use:

```field 9 Equation(s) to solve in terms of the results
re = 12000
ir3 = 0.006
```

In the second, headed **Unknown(s) to solve for**, name what you want found, separated by
commas:

```field 9 Unknown(s) to solve for
e, r1
```

Then press **Solve equations**.
:::

::: only 7,8
::: note The apostrophe shorthand does not work here
Notice that you cannot use `'k` here as a shorthand for kilo, or any other SI
prefix, because that shorthand only works within the values in the description
of the circuit.
:::
:::

An instant later we get the answers: {{v7,8|e = 72 V and r1 = 2000 Ω}}{{v9|the
card lists *e* = 72.0 and *r1* = 2000.0, that is a source of 72 V and a
resistor of 2000 Ω}}. These are the right answers. Not many other circuit
simulators allow this flexibility.
:::
:::

## Numerical from symbolic, using ex {#expert-mode}

::: only 7,8
Symbulator's true strength is seen in numerical-from-symbolic problems like the
one we solved above, when we use its expert mode of simulation.{{i:expert mode}}
Expert mode cracks these problems open even faster, and can give you fully
numerical values to all the answers of problems that have an equal number of
unknown values and of answers provided by the problem. Learning to use the
expert mode pays off handsomely in terms of additional power and speed.

Let's solve the same circuit again, this time using the expert mode's program
**ex**.

::: problem B11's Example 5.6, using ex
::: answer
We will use the same circuit description as before, with a single change: we
will use rx for the value of resistor R1, instead of the r1 value we used
before. Like this:

```sym 7
"e,1,0,e:r1,1,2,rx:r2,2,3,4'k:r3,3,0,6'k"→cir
```
```sym 8
"e,1,0,e:r1,1,2,rx:r2,2,3,4'k:r3,3,0,6'k"→cir
```

We use rx instead of r1 for our symbolic value because the expert mode will try
to save into that variable the value it finds, and r1 (as well as other r#
variables) cannot be used to store anything: trying to store a value into r1
results in an error.

To run an expert mode simulation, type this:

```sym 7
s\ex(cir)
```
```sym 8
s\ex(cir)
```

When prompted, select DC and press Enter. Now you will see a prompt asking you
to add equations, variables and conditions. You may recall from your algebra
class that you need an equal number of equations and unknowns in order to solve
a set of equations into numerical values. The statement of the problem gives us
the information we need to write the two additional equations.

In "Add equations" type:

```sym 7
re=12'k and ir3=6'm
```
```sym 8
re=12'k and ir3=6'm
```

In "Add unknowns" type:

```sym 7
e,rx
```
```sym 8
e,rx
```

Now we have six variables and six equations. Press Enter and wait just a few
seconds. A few other dialogs will appear. In this and all the other expert
examples in this volume, just press OK in these prompts without changing
anything in them. When Symbulator says "Done", go ahead and retrieve the
answers: `rx` gives 2000 and `e` gives 72. Both are right.

The speed advantage of the expert mode is not necessarily evident in this
simple problem. It does give you an idea of what the expert mode is all about:
you get to halt the simulation in mid-air and give Symbulator extra
information. Had this circuit been larger, the benefit in computation time
would be clear.
:::
:::
:::

::: only 9
Symbulator's true strength is seen in numerical-from-symbolic problems like the
one we solved above, when we use its expert mode of simulation.{{i:expert mode}}
Expert mode cracks these problems open in a single call, and can give you fully
numerical values to all the answers of problems that have an equal number of
unknown values and of answers provided by the problem.

The three things the calculator stopped to ask you for — extra equations, extra
unknowns and extra conditions — are three boxes in Symbulator 9, and they are
hidden until you ask for them. Open the **Expert Mode** box and tick **Enable
Expert Mode**; three new fields appear:

- **Add equations** — one per line, written in the names the results use.
- **Add unknowns** — comma-separated.
- **Add conditions** — for narrowing a solution down, which we will use later.

They apply to whatever analysis you run, so expert mode works the same way in
DC, AC, FD and TR.

::: problem B11's Example 5.6, using ex
::: answer
We will use the same circuit description as before, with a single change: we
will use rx for the value of resistor R1, instead of the r1 value we used
before.

The statement of the problem gives us the information we need to write the two
additional equations: the source sees 12 kΩ, and the current through R3 is
6 mA. Both go in as strings, written in the same names the answers come back
under — so `re=12'k` on the calculator becomes `re = 12000` here:

```field 9 Circuit Description
e,1,0,e
r1,1,2,rx
r2,2,3,4'k
r3,3,0,6'k
```

```field 9 Add equations
re = 12000
ir3 = 0.006
```

```field 9 Add unknowns
e, rx
```

Run it in DC as usual. This time nothing comes back symbolic: Symbulator has
enough to pin every value down, so the whole circuit arrives in numbers. The
node voltages read v{{sub:1}} = 72 V, v{{sub:2}} = 60 V and
v{{sub:3}} = 36 V, and at the foot of **Results by element** you will find
the two unknowns you asked for, listed like any other answer:
*e* = 72 and r{{sub:x}} = 2000.

Both are right, and they arrived alongside everything else rather than in a
separate step — the whole circuit is solved, not just the two unknowns. That is
also why the rx-instead-of-r1 precaution the calculator needed does not apply
here; see the note below.

The speed advantage of the expert mode is not necessarily evident in this
simple problem. It does give you an idea of what the expert mode is all about:
you get to hand Symbulator extra information before it solves, rather than
after. Had this circuit been larger, the benefit in computation time would be
clear.

::: note What you can write an equation about
Anything the simulation reports: node voltages `v1`, `v2`, …, element
currents `ir3`, branch voltages `vr1`, powers `pr2`, and the resistance or
impedance a source sees, `re` and `ze`. The one exception is the AC power
family — `s_`, `p_` and `ap_` in an AC analysis — which is defined through
complex conjugation and cannot be solved as part of the system; Symbulator
will tell you so rather than quietly ignoring the equation, and you can
restate the constraint in voltages and currents instead.

One thing to watch: a quantity that depends on an unknown quadratically, such
as a power, can be satisfied by two different component values. Symbulator
returns one of them. If the answer surprises you, check whether the other root
is the one the problem meant.
:::
:::
:::

::: note Coming from a calculator version?
Two of the calculator's precautions are gone. There is no need to avoid `r1` as
a symbolic value — Symbulator 9 never writes answers into your namespace, so
there is nothing to collide with — and there are no follow-up dialogs to click
through. The rest maps across directly: "Add equations" is `equations=`, "Add
unknowns" is `unknowns=`, "Add conditions" is `conditions=`.
:::
:::

## Instructive symbolic examples, solved {#practice-symbolic}

::: practice

### Numeric-from-symbolic, with solve

::: problem HK5's Figure 1-24a (*solve*)

Determine *i*{{sub:x}} and *v*{{sub:x}} in the following circuit:

::: figure assets/practice/hk5s-figure-1-24a-solve-1.jpg

:::

I named the nodes thus: bottom is **0**, top left is **1**, top right is
**2**. I named the elements according to their value: this facilitates
remembering who's who in the circuit. I also defined the resistors' nodes in
the direction of the current indicated in the diagram.

```sym 7
s\dc("e18,1,0,18:ra,1,0,ra:r6,1,0,6:r5,2,1,5:evx,2,0,vx")
```
```sym 8
s\dc("e18,1,0,18:ra,1,0,ra:r6,1,0,6:r5,2,1,5:evx,2,0,vx")
```
```field 9 Circuit Description
e18,1,0,18
ra,1,0,ra
r6,1,0,6
r5,2,1,5
evx,2,0,vx
```

Explore the answers. Since **ir5** (which we
know is 12 A) is in terms of v{{sub:x}}, we can find v{{sub:x}}:

```sym 7
solve(ir5=12,vx)
```
```sym 8
solve(ir5=12,vx)
```

::: only 9
Solve it in DC, then use the **Solve equations** card:

```field 9 Equation(s) to solve in terms of the results
ir5 = 12
```

```field 9 Unknown(s) to solve for
vx
```
:::

We get that v{{sub:x}} is {{o:78}} V, which is correct.
{{v7,8|Evaluating `ir6` we find}}{{v9|The `r6` block already shows}} that
i{{sub:x}} is {{o:3}} A. The fact that we can find numerical answers in this
problem can be quite puzzling until one realizes that ignoring the value of
R{{sub:A}} doesn't matter: due to the circuit's structure, it is not needed
to answer the two questions we have been asked.

:::

### Numeric-from-symbolic, with Expert

::: problem B11's Example 6.19 (Expert)

::: figure assets/practice/b11s-example-6-19-expert-2.jpg

:::

This problem, having three unknown element values and three known answers, is
a perfect candidate for the expert mode. Below is my circuit description.

```sym 7
s\ex("e,1,0,e:r1,1,0,2'k:r2,1,0,r2:r3,1,0,r3")
```
```sym 8
s\ex("e,1,0,e:r1,1,0,2'k:r2,1,0,r2:r3,1,0,r3")
```
```field 9 Circuit Description
e,1,0,e
r1,1,0,2'k
r2,1,0,r2
r3,1,0,r3
```

Select DC. Add these three equations:

```sym 7
ir1=8'm and ir2=10'm and ir3=2'm
```
```sym 8
ir1=8'm and ir2=10'm and ir3=2'm
```
```field 9 Add equations
ir1 = 0.008
ir2 = 0.010
ir3 = 0.002
```

Add these unknowns:

```sym 7
e,r2,r3
```
```sym 8
e,r2,r3
```
```field 9 Add unknowns
e, r2, r3
```

::: only 7,8
Press Enter and Enter. When Symbulator is *Done*, find I{{sub:S}} and E by
asking:

```sym 7
approx(-ie1)
```
```sym 8
approx(-ie1)
```

We get that I{{sub:S}} is {{o:0.02}} A.

```sym 7
e
```
```sym 8
e
```

We get that E is {{o:16}} V. These are correct.
:::
::: only 9
Run it. Everything comes back numerical: *e* = 16 appears among the results, so
E is {{o:16}} V, and the source's **current through** line gives
i{{sub:e}} = −0.02 A, so I{{sub:S}} is {{o:0.02}} A. These are correct.
The solver also fills in the two resistors it had to find on the way,
*r2* = 1600 Ω and *r3* = 8000 Ω.
:::

:::

::: problem B11's Example 7.12 (Expert)

Determine R{{sub:1}}, R{{sub:2}} and R{{sub:3}} for the voltage divider
supply. Can 2W resistors be used?

::: figure assets/practice/b11s-example-7-12-expert-3.jpg

:::

This problem is also perfect for the expert mode, because: (a) the target is
to obtain numerical values, and (b) we have N unknown element values, and in
turn we are given N numerical answers. Here is how I solved it:

```sym 7
s\ex("e,a,c,72:r1,a,b,r1:r2,b,0,r2:r3,0,c,r3:rl1,a,0,rl1:rl2,b,0,rl2")
```
```sym 8
s\ex("e,a,c,72:r1,a,b,r1:r2,b,0,r2:r3,0,c,r3:rl1,a,0,rl1:rl2,b,0,rl2")
```
```field 9 Circuit Description
e,a,c,72
r1,a,b,r1
r2,b,0,r2
r3,0,c,r3
rl1,a,0,rl1
rl2,b,0,rl2
```

Choose DC. Add these five equations:

```sym 7
irl1=20'm and vrl1=60 and irl2=10'm and vrl2=20 and -ie=50'm
```
```sym 8
irl1=20'm and vrl1=60 and irl2=10'm and vrl2=20 and –ie=50'm
```
```field 9 Add equations
irl1 = 0.020
vrl1 = 60
irl2 = 0.010
vrl2 = 20
-ie = 0.050
```

{{v7,8|Add these five variables to the list of first level
variables:}}{{v9|List these five as the unknowns to solve for:}}

```sym 7
r1,r2,r3,rl1,rl2
```
```sym 8
r1,r2,r3,rl1,rl2
```
```field 9 Add unknowns
r1, r2, r3, rl1, rl2
```

{{v7,8|Press Enter and Enter. When Done, evaluate these variables to find the
answers:}}{{v9|Run it, and read the answers straight off the results:}}
`r1` = {{o:1333.3}} Ω, `r2` = {{o:1000}} Ω, `r3` = {{o:240}} Ω. These are
correct.

{{v7,8|Then we ask for the powers consumed in the resistors, and find
that:}}{{v9|The **power consumed** line of each resistor's block gives:}}

`pr1` is {{o:1.2}} W, `pr2` is {{o:0.4}} W, and `pr3` is {{o:0.6}} W

Since all are smaller than 2W, it is possible to use 2W resistors in the
design.

:::
:::
