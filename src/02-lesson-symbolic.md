---
id: lesson-symbolic
kind: lesson
title: Symbolic circuits and {{v7,8|expert mode}}{{v9|Expert Mode}}
updated: 2026-09-06
summary: >
  Learn how to solve different types of *symbolic* circuits in Symbulator. Use
  {{v7,8|the solve command on}}{{v9|{{card:Solve}} in}} Symbulator. And explore
  {{v7,8|**ex**, }}the powerful {{v7,8|*expert mode*}}{{v9|{{card:Expert Mode}}}}, for the ambitious user.
---

Here you will learn about the types of symbolic circuits and how to solve
them in Symbulator, using {{v7,8|the solve command}}{{v9|{{card:Solve}}}} when needed, and — for the more
adventurous — the powerful {{v7,8|*expert mode*}}{{v9|{{card:Expert Mode}}}}.

## About symbolic problems {#about-symbolic}

The problem we saw in {{ref:lesson-dc}} was a *numerical problem* because it
involved a numerical circuit: from the start, we knew the values of all its
elements. None were unknown.

A circuit with one or more elements whose value we do not know is a
**symbolic circuit**.{{i:symbolic circuit}} A *symbolic
problem* is one that involves a symbolic circuit. It gives me great joy when I
encounter a symbolic problem, because the ability to simulate symbolic circuits
is what sets Symbulator apart from other {{v7,8|programs}}{{v9|simulators}}.

::: note Variables are case-sensitive; names are not
Element and node names ignore case — **R1** and **r1** are the same resistor,
and so is any reference built from a name: `2*VR1`, `2*vr1` and `2*v_r1`
all mean r1's voltage drop. A variable that names nothing in the circuit
is different: `e,1,2,c` and `e,1,2,C` are two *different* symbolic
sources, and telling Symbulator that `c = 5` says nothing about `C`.
Pick one spelling for each unknown and keep it.{{v9|{{i:case sensitivity}}}}
:::

I find it useful to distinguish between two types of symbolic problems:

- **Purely symbolic problems** use symbolic circuits whose answers are also
  symbolic, given as expressions of unknown variables. Solving them in
  Symbulator is as straightforward as solving numerical problems.
- **Numerical-from-symbolic problems** start with a symbolic circuit but ask
  for numerical answers. That is possible when the problem gives us more
  information about the circuit.{{v9|{{i:numerical-from-symbolic problems}}}}

Numerical-from-symbolic problems can be solved in two ways. If they are simple
— one or two unknown values, one or two numerical answers wanted — it is
quicker to simulate the circuit symbolically and then solve for the numerical
answers with the {{v7,8|{{tool:solve}} command of the
calculator}}{{v9|{{card:Solve}} card, under the results}}. If they are not simple, it is easier to use
{{v7,8|**expert mode**}}{{v9|{{card:Expert Mode}}}}.

Let's see an example of each.

### Solving a purely symbolic problem

Since Symbulator is natively a symbolic simulator, there is nothing special
about solving a purely symbolic problem. The only limitation comes from the
computing capacity of {{v7,8|the calculator}}{{v9|your device}}: {{v7,8|while small circuits can be
solved relatively fast, larger circuits may be too slow to solve and may cause
a memory error}}{{v9|while small circuits are solved almost instantly, large
symbolic circuits can take longer to solve, and on top of that, they may
produce expressions too large to be useful to a human}}.

Let's see a simple purely symbolic problem, from *Fundamentals of Electric
Circuits* by Alexander and Sadiku (5th edition), from now on referred to as
**AS5**.

::: problem AS5's Figure 2.29
::: figure assets/circuit/as5f0229.png
AS5's Figure 2.29
:::

::: answer
All the values in this circuit are variables: no element value is known. This is an example of a symbolic circuit. Imagine you are asked to
find symbolic expressions for the current {{var:i}}, the voltage drop in {{var:R_2}}, and the
power consumed by {{var:R_1}} and {{var:R_2}}. Since we are being asked to find symbolic answers
from a symbolic circuit, this is a purely symbolic problem.

This is how I would describe this circuit. First, the nodes. The node called **a**
in the schematic stays node **a**. The node called **b** is my ground, so it becomes
node **0**. The node between the two resistors I call **c**.

Then the elements. I name the source **ev** and the resistors **r1** and **r2**, and give
them variables for values: **v** for the source, **r1** and **r2** for the resistors. It is
no problem that a symbolic value carries the same name as its element.

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
{{ref:lesson-dc}} had you set {{ui:Rounding}} to *approx to n digits*. There is
nothing to round here, so open {{card:Settings}} and put it back to *exact*. The
{{ui:Use SI prefixes}} tick clears itself: a prefix has no place in an answer
like

$$
\dfrac{v}{r_{1} + r_{2}}
$$
:::

Type the three elements into the box, one to a line:

```field 9 Circuit Description
ev,a,0,v
r1,a,c,r1
r2,c,0,r2
```

Leave {{ui:Type of analysis}} on *Solve circuit*, set {{ui:Analysis}} to
*DC — direct current*, and press {{btn:Run Symbulator}}.
:::

{{v7|This simulation took 15 seconds in my calculator.}}{{v8|This simulation
took a couple of seconds in my calculator.}}{{v9|The answer comes back at once.}} To find the current i, we
{{v7,8|ask for `ir1` or `ir2`}}{{v9|read `ir1` or `ir2`}}. To find the voltage drop on r2, we
{{v7,8|ask for `vr2`}}{{v9|read `vr2`}}.

Both are expressions rather than numbers:

::: only 7,8
$$
i_{r1} = \dfrac{v}{r_{1} + r_{2}} \quad\text{and}\quad v_{r2} = \dfrac{r_{2}\,v}{r_{1} + r_{2}}
$$
:::
::: only 9
::: result
i_{r1} = \dfrac{v}{r_{1} + r_{2}}
:::
::: result
v_{r2} = \dfrac{r_{2}\,v}{r_{1} + r_{2}}
:::
:::

which is the voltage divider you would have written by hand.

To find the power consumed in r2, we {{v7,8|ask for `pr2`}}{{v9|read `pr2`}}. To find the power delivered by the
source, we {{v7,8|ask for the negative of `pev`}}{{v9|read the *power delivered* row of the source's card, `-pev`}}.

$$
\begin{aligned}
p_{r2} &= \dfrac{r_{2}\,v^2}{(r_{1} + r_{2})^2} \\[0.6em]
-p_{ev} &= \dfrac{v^2}{r_{1} + r_{2}}
\end{aligned}
$$

It is this ability to simulate symbolically, as if it were nothing, that puts
Symbulator in a league of its own. Symbolic answers from a symbolic circuit
take no extra effort.
:::
:::

## Numerical from symbolic, with {{v7,8|solve}}{{v9|**Solve**}} {#with-solve}

Getting numerical answers from a symbolic circuit, on the other hand, takes an
extra step: {{v7,8|the solve command}}{{v9|{{card:Solve}}}}, as in this next example, or {{v7,8|expert mode}}{{v9|{{card:Expert Mode}}}}, as in
the one after.

::: problem B11's Example 5.6, with {{v7,8|solve}}{{v9|{{card:Solve}}}}
::: figure assets/circuit/b11e0506.jpg
B11's Example 5.6
:::

::: answer
This is a very nice numerical-from-symbolic problem. We can solve it into
numbers because, although it hides two values from us (the source **E** and the
resistor {{var:R_1}}), it gives us in exchange two answers (the equivalent resistance {{var:R_T}}
and the current {{var:I_3}}) to solve for them with.

Since this circuit is structurally identical to **{{ref:prob-b11s-example-57}}** solved in
{{ref:lesson-dc}}, we will use the same names for the nodes. The description is
identical except for the values. Symbulator accepts numbers, variables or even
algebraic expressions as values. Here I use **e** for source **e**, and **r1** for
resistor **r1**.

::: only 7,8
::: warning Clean your {{t:container}}
Make sure the variables you will use as symbolic values are empty — that they
do not exist in {{t:container_the}}. Empty the whole {{t:container}}, or delete
just those variables: `DelVar e,r1`
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

A moment later Symbulator is done. From its symbolic answers and the answers
the problem gives us, we write two equations and solve them for the two
unknowns.

::: only 7,8
The problem says that {{var:I_3}} is 6 mA. In Symbulator, {{var:I_3}} is `ir3`, the current through resistor **r3**. If you evaluate it, you will see it produces an
algebraic expression in terms of the two unknowns, **e** and **r1**. This is what we call a symbolic answer.
The problem also says that {{var:R_T}} is 12 kΩ; the equivalent resistance as seen by
the source **e** is given by `re`, which when evaluated gives another
algebraic expression in terms of r1. We can then write two new equations
and solve them for e and r1:
:::
::: only 9
The problem says that {{var:I_3}} is 6 mA. In Symbulator, {{var:I_3}} is `ir3`, the current through resistor **r3**. Look at it
and you will see an expression rather than a number, in terms of the two
unknowns, **e** and **r1**:

::: result
i_{r3} = \dfrac{e}{r_{1} + 10000}
:::

This is what we call a symbolic answer.
The problem also says that {{var:R_T}} is 12 kΩ; the equivalent resistance as seen by
the source **e** is `re`, which is:

::: result
r_{e} = r_{1} + 10000
:::

We can then write two new equations
and solve them for **e** and **r1**.
:::

```sym 7
solve(re=12000 and ir3=.006,{e,r1})
```
```sym 8
solve(re=12000 and ir3=.006,{e,r1})
```

::: only 9
That is what the {{card:Solve}} card, under the results beside {{card:Evaluate}}, is
for. It has two boxes.{{i:Solve card}}

In the first box, headed {{ui:Equation(s) to solve in terms of the results}}, write the equations, using the same names the results use.

The shorthand works in these boxes too, so `re = 12'k` reads as 12000.

You can write the equations separated by `and`, like this:

```field 9 Equation(s) to solve in terms of the results
re = 12'k and ir3 = 6'm
```

Or one equation per line, like this:

```field 9 Equation(s) to solve in terms of the results
re = 12'k
ir3 = 6'm
```

In the second box, headed {{ui:Unknown(s) to solve for}}, name what you want found. You can write the unknowns separated by commas, like this:

```field 9 Unknown(s) to solve for
e, r1
```

Or one unknown per line, like this:

```field 9 Unknown(s) to solve for
e
r1
```

Then press {{btn:Solve equations}}.
:::

::: only 7,8
::: note The apostrophe shorthand does not work here
You cannot use `'k` here as a shorthand for kilo, or any other SI prefix: it
works only in the values in the circuit description.
:::
:::

::: only 7,8
An instant later we get the answers: **e** = {{o:72}} V and **r1** = {{o:2000}} Ω. These are the right answers. Not many other circuit
simulators allow this flexibility.
:::
::: only 9
An instant later we get the answers: the card lists **e** = {{o:72.0}} and **r1** = {{o:2000.0}}: a 72 V source and a
2000 Ω resistor. These are the right answers. Not many other circuit
simulators allow this flexibility.
:::
:::
:::

## Numerical from symbolic, {{v7,8|using ex}}{{v9|in **Expert Mode**}} {#expert-mode}

::: only 7,8
Symbulator's true strength is seen in numerical-from-symbolic problems like the
one we solved above, when we use its expert mode of simulation.{{i:expert mode}}
Expert mode cracks these problems open even faster, and gives fully numerical
answers whenever the problem provides as many answers as it hides values.
Learning it pays off handsomely in power and speed.

Let's solve the same circuit again, this time using the expert mode's program
**ex**.

::: problem B11's Example 5.6, using ex
::: answer
We will use the same circuit description as before, with a single change: we
will use rx for the value of resistor {{var:R_1}}, instead of the r1 value we used
before. Like this:

```sym 7
"e,1,0,e:r1,1,2,rx:r2,2,3,4'k:r3,3,0,6'k"→cir
```
```sym 8
"e,1,0,e:r1,1,2,rx:r2,2,3,4'k:r3,3,0,6'k"→cir
```

We use rx instead of r1 because expert mode saves the value it finds into that
variable, and r1 — like the other r# variables — cannot store anything: trying
to results in an error.

To run an expert mode simulation, type this:

```sym 7
s\ex(cir)
```
```sym 8
s\ex(cir)
```

When prompted, select DC and press Enter. Now you will see a prompt asking you
to add equations, variables and conditions. You may recall from algebra that solving a set
of equations into numbers needs as many equations as unknowns. The statement of the problem gives us
the information we need to write the two additional equations.

In "Add equation(s)" type:

```sym 7
re=12'k and ir3=6'm
```
```sym 8
re=12'k and ir3=6'm
```

In "Add unknown(s)" type:

```sym 7
e,rx
```
```sym 8
e,rx
```

Now we have six variables and six equations. Press Enter and wait a few
seconds. A few other dialogs appear; in this and every other expert example in
this volume, just press OK without changing anything. When Symbulator says "Done", go ahead and retrieve the
answers: `rx` gives {{o:2000}} and `e` gives {{o:72}}. Both are right.

The speed advantage is not obvious in so simple a problem, but the idea is:
you halt the simulation in mid-air and give Symbulator extra information. Had
the circuit been larger, the saving would be clear.
:::
:::
:::

::: only 9
Symbulator's true strength is seen in numerical-from-symbolic problems like the
one we solved above, when we use its {{card:Expert Mode}} of simulation.{{i:Expert Mode}}
{{card:Expert Mode}} cracks these problems open in a single call, and gives fully
numerical answers whenever the problem provides as many answers as it hides
values.

{{card:Expert Mode}} takes extra equations, unknowns and conditions in three boxes.
Open the {{card:Expert Mode}} box and tick {{ui:Enable Expert Mode}} to see them:

- {{btn:Add equation(s)}} — one or many, separated by `and` or one per line, written in the names the results use.
- {{btn:Add unknown(s)}} — one or many, separated by commas or one per line.
- {{btn:Add condition(s)}} — one or many, separated by `and` or one per line, for narrowing a solution down, which we will use later.

They apply to whatever analysis you run, so {{card:Expert Mode}} works the same way in
DC, AC, FD and TR.

::: problem B11's Example 5.6, using ex
::: answer
We use the same circuit description as before, **r1** included.

The problem gives us the two extra equations: the source sees 12 kΩ, and the
current through {{var:R_3}} is 6 mA. They use the names the answers come back under,
and the SI shorthand works here too:

```field 9 Circuit Description
e,1,0,e
r1,1,2,r1
r2,2,3,4'k
r3,3,0,6'k
```

```field 9 Add equation(s)
re = 12'k
ir3 = 6'm
```

```field 9 Add unknown(s)
e, r1
```

Run it in DC. This time everything comes back numerical: the node voltages
read v{{sub:1}} = 72 V, v{{sub:2}} = 60 V and v{{sub:3}} = 36 V, and at the
foot of {{card:Results by element}} are the two unknowns, listed like any other
answer: **e** = {{o:72}} and **r1** = {{o:2000}}. Both are right, and the whole circuit was
solved with them in one step.

The speed advantage of {{card:Expert Mode}} is not necessarily evident in this
simple problem. But it does give you an idea of what {{card:Expert Mode}} is all about:
you get to hand Symbulator extra information before it solves, rather than
after. Had this circuit been larger, the benefit in computation time would be
clear.

::: note What you can write an equation about
Anything the simulation reports: node voltages such as `v1`, currents `ir3`,
voltage drops `vr1`, powers `pr2`, and the resistance or impedance a source
sees, `re` or `ze`. The one exception is AC power (`s`, `p` and `ap` in an AC
analysis), which involves a complex conjugate and cannot be solved for;
Symbulator says so, and you can restate the constraint in voltages and
currents.
:::

::: tip Why you may get two answers
A quantity that is quadratic in an unknown, such as a power, can be satisfied
by two values. Symbulator returns multiple solutions when they exist.{{i:multiple solutions}}
:::
:::
:::
:::

## Instructive symbolic examples, solved {#practice-symbolic}

::: practice

### Numeric-from-symbolic, with {{v7,8|solve}}{{v9|**Solve**}}

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
know is 12 A) is in terms of {{var:v_x}}, we can find {{var:v_x}}:

```sym 7
solve(ir5=12,vx)
```
```sym 8
solve(ir5=12,vx)
```

::: only 9
Solve it in DC, then use the {{card:Solve}} card:

```field 9 Equation(s) to solve in terms of the results
ir5 = 12
```

```field 9 Unknown(s) to solve for
vx
```
:::

{{v7,8|We get that {{var:v_x}} is {{o:78}} V, which is correct.}}{{v9|{{var:v_x}} is {{o:78}} V, which is correct.}}
{{v7,8|Evaluating `ir6` we find}}{{v9|The current `ir6` already shows}} that
{{var:i_x}} is {{o:3}} A. The fact that we can find numerical answers in this
problem can be quite puzzling until one realizes that ignoring the value of
{{var:R_A}} doesn't matter: due to the circuit's structure, it is not needed
to answer the two questions we have been asked.

:::

### Numeric-from-symbolic, {{v7,8|with Expert}}{{v9|in **Expert Mode**}} {#numeric-from-symbolic-with-expert}

::: problem B11's Example 6.19 (Expert)

::: figure assets/practice/b11s-example-6-19-expert-2.jpg

:::

This problem, having three unknown element values and three known answers, is
a perfect candidate for {{v7,8|the expert mode}}{{v9|{{card:Expert Mode}}}}. Below is my circuit description.

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

{{v7,8|Select DC. Add these three equations:}}{{v9|Choose DC and, in {{card:Expert Mode}}, add these three equations:}}

```sym 7
ir1=8'm and ir2=10'm and ir3=2'm
```
```sym 8
ir1=8'm and ir2=10'm and ir3=2'm
```
```field 9 Add equation(s)
ir1 = 8'm
ir2 = 10'm
ir3 = 2'm
```

Add these unknowns:

```sym 7
e,r2,r3
```
```sym 8
e,r2,r3
```
```field 9 Add unknown(s)
e, r2, r3
```

::: only 7,8
Press Enter and Enter. When Symbulator is *Done*, find {{var:I_S}} and {{var:E}} by
asking:

```sym 7
approx(-ie1)
```
```sym 8
approx(-ie1)
```

We get that {{var:I_S}} is {{o:0.02}} A.

```sym 7
e
```
```sym 8
e
```

We get that E is {{o:16}} V. These are correct.
:::
::: only 9
Run it. Everything comes back numerical: **e** = {{o:16}}, so {{var:E}} is {{o:16}} V, and
`ie` = −0.02 A, so {{var:I_S}} is {{o:0.02}} A. Both correct. The two
resistors come back too: **r2** = {{o:1600}} Ω and **r3** = {{o:8000}} Ω.
:::

:::

::: problem B11's Example 7.12 (Expert)

Determine {{var:R_1}}, {{var:R_2}} and {{var:R_3}} for the voltage divider
supply. Can 2W resistors be used?

::: figure assets/practice/b11s-example-7-12-expert-3.jpg

:::

This problem is also perfect for {{v7,8|the expert mode}}{{v9|{{card:Expert Mode}}}}, because: (a) the target is
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

{{v7,8|Choose DC. Add these five equations:}}{{v9|Choose DC and, in {{card:Expert Mode}}, add these five equations:}}

```sym 7
irl1=20'm and vrl1=60 and irl2=10'm and vrl2=20 and -ie=50'm
```
```sym 8
irl1=20'm and vrl1=60 and irl2=10'm and vrl2=20 and –ie=50'm
```
```field 9 Add equation(s)
irl1 = 20'm
vrl1 = 60
irl2 = 10'm
vrl2 = 20
-ie = 50'm
```

{{v7,8|Add these five variables to the list of first level
variables:}}{{v9|List these five as the unknowns to solve for:}}

```sym 7
r1,r2,r3,rl1,rl2
```
```sym 8
r1,r2,r3,rl1,rl2
```
```field 9 Add unknown(s)
r1, r2, r3, rl1, rl2
```

{{v7,8|Press Enter and Enter. When Done, evaluate these variables to find the
answers:}}{{v9|Run it, and read the answers straight off the results:}}
`r1` = {{o:1333.3}} Ω, `r2` = {{o:1000}} Ω, `r3` = {{o:240}} Ω. These are
correct.

::: only 7,8
Then we ask for the powers consumed in the resistors, and find
that:

`pr1` is {{o:1.2}} W, `pr2` is {{o:0.4}} W, and `pr3` is {{o:0.6}} W
:::
::: only 9
The power consumed in each resistor is given in:

::: result
p_{r1} = 1.2\ \mathrm{W}
:::
::: result
p_{r2} = 0.4\ \mathrm{W}
:::
::: result
p_{r3} = 0.6\ \mathrm{W}
:::
:::

Since all are smaller than 2W, it is possible to use 2W resistors in the
design.

:::

:::
