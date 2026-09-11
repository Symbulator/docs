---
id: lesson-threephase
kind: lesson
title: Three-phase circuits
updated: 2023-07-08
summary: >
  Learn to solve simple *three-phase* circuits in Y-Y, Y-Δ, Δ-Δ and Δ-Y
  configurations, both balanced and unbalanced, to find line and phase
  currents, voltages and complex power.
---

In this lesson you will learn to use Symbulator to solve simple **three-phase**
systems, in their four basic configurations of wye-wye, wye-delta, delta-delta
and delta-wye. We will see both balanced and unbalanced examples, where you are
asked to find currents, voltages and complex power in the source, line and
load.

## About solving three-phase circuits {#about-threephase}

Three-phase circuits can be tricky to solve in Symbulator, for several
reasons.{{i:three-phase circuits}} It is not always clear which node to use as
ground. There are three times as many nodes as in an equivalent single-phase
circuit. And sources in a delta array bring mathematical trouble: more unknowns
than equations.

Symbulator does a great job on the simple three-phase circuits of a basic
Circuits I / II textbook, and here we will see examples and one or two tricks.
It would not be my tool of choice for anything larger: as circuits grow, the
number of nodes quickly passes what {{v7,8|the calculator}}{{v9|your device}} can solve.

## Wye-Wye {#wye-wye}

### Balanced wye-wye system

::: problem AS7's Examples 12.2 & 12.6
Calculate the line currents in the three-wire Y-Y system. Determine the total
average power, reactive power, and complex power absorbed at the source and at
the load. Assume that the values given for the source are RMS.

::: figure assets/circuit/as7e1202.png
AS7's Examples 12.2 and 12.6
:::

::: answer
Although not specified in the textbook, to get the answers they give we need to
assume the values are RMS. One must describe the circuit carefully in the case
of three-phase circuits, because it is very easy to make a mistake. Below is
how I describe this one:

```sym 7
true→s\rms
"ea0,ag,0,(110.∠0°):eb0,bg,0,(110.∠-120°):ec0,cg,0,(110.∠120°):rat,ag,ad,5.–𝐢2.:rbt,bg,bd,5.–𝐢2.:rct,cg,cd,5.–𝐢2.:ra0,ad,0,10.+8.𝐢:rc0,cd,0,10.+8.𝐢:rb0,bd,0,10.+8.𝐢"→cir
s\ac(cir,ω)
```
```sym 8
true→userms
"ea0,ag,0,(110.∠0°):eb0,bg,0,(110.∠–120°):ec0,cg,0,(110.∠120°):rat,ag,ad,5.–𝐢2.:rbt,bg,bd,5.–𝐢2.:rct,cg,cd,5.–𝐢2.:ra0,ad,0,10.+8.𝐢:rc0,cd,0,10.+8.𝐢:rb0,bd,0,10.+8.𝐢"→cir
s\ac(cir,ω)
```

::: only 9
```field 9 Circuit Description
ea0,ag,0,(110∠0°)
eb0,bg,0,(110∠-120°)
ec0,cg,0,(110∠120°)
rat,ag,ad,5-2j
rbt,bg,bd,5-2j
rct,cg,cd,5-2j
ra0,ad,0,10+8j
rb0,bd,0,10+8j
rc0,cd,0,10+8j
```

AC, with {{ui:RMS phasors}} ticked. Every value is already an impedance, so
the frequency is asked for but never used.
:::

Some observations about my description:

- Notice that I have specified the node at the centre of both Y's as node **0**.
  This is something you can do only in the case of balanced Y-Y systems, not
  for other configurations and not for unbalanced systems.
- Since Symbulator does not differentiate between lower and upper case
  {{v7,8|variables}}{{v9|in names}}, nodes called **a** and **A** would be considered the same node. Instead,
  we use the names **ag** and **ad**, where the g reminds us a node is on the
  generation side and the d reminds us it is on the demand side.

Once the simulation is completed, {{v7,8|we ask for the currents on the
transmission lines and get:}}{{v9|we look in the results for the currents on
the transmission lines:}}

```sym 7
{s\aa(irat),s\aa(irbt),s\aa(irct)}
```
```sym 8
{s\aa(irat),s\aa(irbt),s\aa(irct)}
```
```out 7,8
{"6.809ᴇ0∠-21.8°","6.809ᴇ0∠-141.8°","6.809ᴇ0∠98.2°"}
```

::: only 9
Tick {{ui:Show AC answers as polar phasors}} in {{card:Settings}} and each line
impedance's *current through* reads straight off:

- `irat` = {{o:6.809}}∠{{o:-21.8}}° A
- `irbt` = {{o:6.809}}∠{{o:-141.8}}° A
- `irct` = {{o:6.809}}∠{{o:98.2}}° A
:::

The complex power at the source is `sea0+seb0+sec0`, which gives
−2086.2 − 834.5𝐢 VA. The real part is the average power absorbed by the source;
since it is negative, the source is delivering an average power of 2086 W. The
imaginary part is the reactive power: 834 var.

The complex power at the load is `sra0+srb0+src0`, which gives
1390.8 + 1112.6𝐢 VA. The load is consuming an average power of 1391 W and a
reactive power of 1113 var.

Before we move on, try simulating this circuit with a different node as the
centre of the load's Y array — call it d0, for the demand side. The voltage in
that node evaluates to 0 V, because the system is balanced. That is why we
could use 0 for both. In an unbalanced system we cannot.
:::
:::

::: practice Further wye-wye problems

::: problem AS7's Practice Problem 12.2 & 12.6
Calculate the line voltages and the line currents. Also calculate the complex
power at the source and at the load. Assume the source voltage is given as RMS.

::: figure assets/circuit/as7pp1202.png
AS7's Practice Problem 12.2 and 12.6
:::

::: answer
The textbook does not say so, but you only get its answers if you take the
values as RMS.

There are **three** impedances in each line here: one inside the generator, one
for the transmission line, and one for the load. The node names below say which
is which — **ag** in the generator, **as** on the supply side, **ad** on the demand
side.

```sym 7
true→s\rms
"ea0,ag,0,(120.∠30°):eb0,bg,0,(120.∠-90°):ec0,cg,0,(120.∠150°):rag,ag,as,.4+𝐢.3:rbg,bg,bs,.4+𝐢.3:rcg,cg,cs,.4+𝐢.3:rat,as,ad,.6+𝐢.7:rbt,bs,bd,.6+𝐢.7:rct,cs,cd,.6+𝐢.7:ra0,ad,0,24.+19.𝐢:rb0,bd,0,24.+19.𝐢:rc0,cd,0,24.+19.𝐢"→cir
s\ac(cir,ω)
```
```sym 8
true→userms
"ea0,ag,0,(120.∠30°):eb0,bg,0,(120.∠–90°):ec0,cg,0,(120.∠150°):rag,ag,as,.4+𝐢.3:rbg,bg,bs,.4+𝐢.3:rcg,cg,cs,.4+𝐢.3:rat,as,ad,.6+𝐢.7:rbt,bs,bd,.6+𝐢.7:rct,cs,cd,.6+𝐢.7:ra0,ad,0,24.+19.𝐢:rb0,bd,0,24.+19.𝐢:rc0,cd,0,24.+19.𝐢"→cir
s\ac(cir,ω)
```
```field 9 Circuit Description
ea0,ag,0,(120∠30°)
eb0,bg,0,(120∠-90°)
ec0,cg,0,(120∠150°)
rag,ag,as,.4+.3j
rbg,bg,bs,.4+.3j
rcg,cg,cs,.4+.3j
rat,as,ad,.6+.7j
rbt,bs,bd,.6+.7j
rct,cs,cd,.6+.7j
ra0,ad,0,24+19j
rb0,bd,0,24+19j
rc0,cd,0,24+19j
```

::: only 9
AC, with {{ui:RMS phasors}} ticked. Every value is already an impedance, so the
frequency is asked for but never used.
:::

The question asks for the line voltages — the differences between the lines.
{{v7,8|For the answers the textbook wants, ask for these:}}{{v9|For the answers the textbook wants, take these differences:}}

```sym 7
{s\aa(vag-vbg),s\aa(vbg-vcg),s\aa(vcg-vag)}
```
```sym 8
{s\aa(vag-vbg),s\aa(vbg-vcg),s\aa(vcg-vag)}
```
```out 7,8
{"207.8ᴇ0∠60.°","207.8ᴇ0∠-60.°","207.8ᴇ0∠180.°"}
```

::: only 9
In {{card:Mini-Tools}} with *aa*:

- `aa(vag-vbg)` = {{o:207.8}}∠{{o:60.00}}° V
- `aa(vbg-vcg)` = {{o:207.8}}∠{{o:-60.00}}° V
- `aa(vcg-vag)` = {{o:207.8}}∠{{o:180.0}}° V
:::

::: tip Which line voltage did you want?
If you ask me, that is not really the voltage between the lines, because the
transmission line starts *after* the generator. At the start of the
transmission line the answer is {{o:204.6}}∠{{o:60.03}}° V, and at the end of it
{{v7,8|{{o:198.7}}∠{{o:59.71}}° V — ask for}}{{v9|{{o:198.7}}∠{{o:59.71}}° V — from}}
{{v7,8|`s\aa(vas-vbs)`}}{{v9|`aa(vas-vbs)`}} and
{{v7,8|`s\aa(vad-vbd)`}}{{v9|`aa(vad-vbd)`}} respectively. All three are
different, and which one you want depends on where you are standing.
:::

The line currents are the currents through the transmission-line impedances:

```sym 7
{s\aa(irat),s\aa(irbt),s\aa(irct)}
```
```sym 8
{s\aa(irat),s\aa(irbt),s\aa(irct)}
```
```out 7,8
{"3.748ᴇ0∠-8.66°","3.748ᴇ0∠-128.66°","3.748ᴇ0∠111.34°"}
```

::: only 9
With polar phasors on, each transmission-line impedance's *current through*
reads:

- `irat` = {{o:3.748}}∠{{o:-8.660}}° A
- `irbt` = {{o:3.748}}∠{{o:-128.66}}° A
- `irct` = {{o:3.748}}∠{{o:111.34}}° A
:::

Finally the complex power. At the source:

```sym 7
sea0+seb0+sec0
```
```sym 8
sea0+seb0+sec0
```
```out 7,8
-1053.7-842.9𝐢
```

::: only 9
Evaluate `sea0+seb0+sec0`, which gives
{{o:-1054}} − {{o:842.9}}𝐢 VA.
:::

Note this does *not* include the power lost in the source's own internal
impedances, which you could add if you wanted them. At the load:

```sym 7
sra0+srb0+src0
```
```sym 8
sra0+srb0+src0
```
```out 7,8
1011.5+800.8𝐢
```

::: only 9
Evaluate `sra0+srb0+src0`, which gives
{{o:1012}} + {{o:800.8}}𝐢 VA.
:::

All correct.
:::
:::

:::

### Unbalanced wye-wye system

The balanced case let you use node **0** for the centre of *both* wyes, because the
voltage at the centre of the load is zero. Unbalanced, it is not — so the load
needs a centre node of its own.{{i:unbalanced system}}

::: practice

::: problem AS7's Example 12.10
For the unbalanced circuit, find (a) the line currents, (b) the total complex
power absorbed by the load, and (c) the total complex power absorbed by the
source.

::: figure assets/circuit/as7e1210.png
AS7's Example 12.10
:::

::: answer
The centre of the generator's wye is ground, and the centre of the load's wye
is a node of its own, called `n`.

```sym 7
true→s\rms
"ea,a,0,(120.∠0°):eb,b,0,(120.∠-120°):ecc,c,0,(120.∠120°):ra,a,n,5.𝐢:rb,b,n,10.:rcc,c,n,-10.𝐢"→cir
s\ac(cir,ω)
```
```sym 8
true→userms
"ea,a,0,(120.∠0°):eb,b,0,(120.∠–120°):ecc,c,0,(120.∠120°):ra,a,n,5.𝐢:rb,b,n,10.:rcc,c,n,–10.𝐢"→cir
s\ac(cir,ω)
```
```field 9 Circuit Description
ea,a,0,(120∠0°)
eb,b,0,(120∠-120°)
ec,c,0,(120∠120°)
ra,a,n,5j
rb,b,n,10
rc,c,n,-10j
```

::: only 9
AC, with {{ui:RMS phasors}} ticked.
:::

```sym 7
{s\aa(ira),s\aa(irb),s\aa(ircc),sra,srb,srcc,sea,seb,secc}
```
```sym 8
{s\aa(ira),s\aa(irb),s\aa(ircc),sra,srb,srcc,sea,seb,secc}
```
```out 7,8
{"56.78ᴇ0∠0.°","25.46ᴇ0∠135.°","42.76ᴇ0∠-155.1°",16122.𝐢,6480.,-18282.𝐢,-6814.,790.6-2951.𝐢,-456.5+5111.𝐢}
```

::: only 9
The three line currents read {{o:56.78}}∠{{o:0}}°, {{o:25.46}}∠{{o:135.0}}° and
{{o:42.76}}∠{{o:-155.1}}° A. The complex powers in the load are
{{o:16120}}𝐢, {{o:6480}} and {{o:-18280}}𝐢 VA, and in the three sources
{{o:-6814}}, {{o:790.6}} − {{o:2951}}𝐢 and {{o:-456.5}} + {{o:5111}}𝐢 VA.
:::

All correct. Two things are worth checking for yourself. Complex power is
conserved, so {{v7,8|`sea+seb+secc+sra+srb+srcc`}}{{v9|`sea+seb+sec+sra+srb+src`}}
evaluates to zero. And the voltage at the centre of the load is *not* zero, as
it was in the balanced case — `vn` is
{{o:120.0}} − {{o:283.9}}𝐢 V.

::: only 7,8
::: tip Why `ecc` and `rcc` rather than `ec` and `rc`
The third phase is named with a doubled letter because on the calculator the
short names collide with reserved ones. Version 9 has no such restriction and
names the third phase like the other two.
:::
:::
:::
:::

::: problem AS7's Example 12.9
The unbalanced Y-load has balanced voltages of 100 V in the *acb* sequence.
Calculate the line currents and the neutral current. Take {{var:Z_A}} = 15 Ω,
{{var:Z_B}} = 10 + j5 Ω and {{var:Z_C}} = 6 − j8 Ω.

::: figure assets/circuit/as7f1223.png
AS7's Example 12.9
:::

::: answer
Two things differ from the last one. The source values are *not* RMS this time.
And there is a neutral line joining the centre of the load to the centre of the
source, which you describe as a short circuit — an **s** element, which takes
just a name and two nodes.

Note also the angles: this is the *acb* sequence, so they run the other way
round.

```sym 7
false→s\rms
"ea,a,0,(100.∠0°):eb,b,0,(100.∠120°):ecc,c,0,(100.∠-120°):sn,0,n:ra,a,n,15:rb,b,n,10.+𝐢5.:rcc,c,n,6.-𝐢8."→cir
s\ac(cir,ω)
```
```sym 8
false→userms
"ea,a,0,(100.∠0°):eb,b,0,(100.∠120°):ecc,c,0,(100.∠–120°):sn,0,n:ra,a,n,15:rb,b,n,10.+𝐢5.:rcc,c,n,6.–𝐢8."→cir
s\ac(cir,ω)
```
```field 9 Circuit Description
ea,a,0,(100∠0°)
eb,b,0,(100∠120°)
ec,c,0,(100∠-120°)
sn,0,n
ra,a,n,15
rb,b,n,10+5j
rc,c,n,6-8j
```

::: only 9
AC, with {{ui:RMS phasors}} left unticked this time.
:::

```sym 7
{s\aa(ira),s\aa(irb),s\aa(ircc),s\aa(isn)}
```
```sym 8
{s\aa(ira),s\aa(irb),s\aa(ircc),s\aa(isn)}
```
```out 7,8
{"6.667ᴇ0∠0.°","8.944ᴇ0∠93.43°","10.000ᴇ0∠-66.87°","10.06ᴇ0∠178.47°"}
```

::: only 9
The three line currents read {{o:6.667}}∠{{o:0}}°, {{o:8.944}}∠{{o:93.43}}° and
{{o:10.00}}∠{{o:-66.87}}° A, and the neutral current
{{o:10.06}}∠{{o:178.5}}° A.
:::

All four are correct. The neutral carries a current precisely because the load
is unbalanced; in the balanced case it would be zero, which is why a balanced
three-wire system needs no neutral at all.
:::
:::

:::

## Wye-Delta {#wye-delta}

A wye source feeding a delta load. The source still has a centre to use as
ground; the load does not, which is the only new thing here.

### Balanced

::: problem AS7's Example 12.3
For the balanced Y-Δ circuit, find the phase currents and the line currents.

::: figure assets/circuit/as7e1203.png
AS7's Example 12.3
:::

::: answer
Nothing says these values are RMS, so leave the convention alone — the
question asks for no powers, so it makes no difference either way. The three
sources get the angles of the abc sequence.

```sym 7
"ea0,a,0,(100.∠10°):eb0,b,0,(100.∠-110°):ec0,c,0,(100.∠130°):rab,a,b,8.+4.𝐢:rca,c,a,8.+4.𝐢:rbc,b,c,8.+4.𝐢"→cir:s\ac(cir,ω)
```
```sym 8
"ea0,a,0,(100.∠10°):eb0,b,0,(100.∠–110°):ec0,c,0,(100.∠130°):rab,a,b,8.+4.𝐢:rca,c,a,8.+4.𝐢:rbc,b,c,8.+4.𝐢"→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
ea0,a,0,(100∠10°)
eb0,b,0,(100∠-110°)
ec0,c,0,(100∠130°)
rab,a,b,8+4j
rca,c,a,8+4j
rbc,b,c,8+4j
```

The phase currents are the currents in the three load impedances:

```sym 7
{s\aa(irab),s\aa(irbc),s\aa(irca)}
```
```sym 8
{s\aa(irab),s\aa(irbc),s\aa(irca)}
```
```out 7,8
{"19.36ᴇ0∠13.43°","19.36ᴇ0∠-106.57°","19.36ᴇ0∠133.43°"}
```

::: only 9
`aa(irab)`, `aa(irbc)` and `aa(irca)` read {{o:19.36}}∠{{o:13.43}}°,
{{o:19.36}}∠{{o:-106.57}}° and {{o:19.36}}∠{{o:133.43}}° A.
:::

The line currents are the currents the sources deliver, which is the opposite
of the current through each source element:

```sym 7
{s\aa(-iea0),s\aa(-ieb0),s\aa(-iec0)}
```
```sym 8
{s\aa(–iea0),s\aa(–ieb0),s\aa(–iec0)}
```
```out 7,8
{"33.54ᴇ0∠-16.57°","33.54ᴇ0∠-136.57°","33.54ᴇ0∠103.43°"}
```

::: only 9
`aa(-iea0)`, `aa(-ieb0)` and `aa(-iec0)` read {{o:33.54}}∠{{o:-16.57}}°,
{{o:33.54}}∠{{o:-136.57}}° and {{o:33.54}}∠{{o:103.43}}° A.
:::

Both sets are correct, and they show the relationship you would expect of a
delta load: the line current is √3 times the phase current, and lags it by 30°.
:::
:::

::: problem AS7's Example 12.11
For the balanced Y-Δ circuit, find the line current {{var:I_aA}}, the phase
voltage {{var:V_AB}}, and the phase current {{var:I_AC}}. The source frequency
is 60 Hz.

::: figure assets/circuit/as7e1211.png
AS7's Example 12.11
:::

::: answer
This one has line impedances, so each source reaches the load through a
resistor, and the load's three nodes are separate from the source's three.

```sym 7
"ea1,na1,0,(100.∠0°):eb1,nb1,0,(100.∠-120°):ec1,nc1,0,(100.∠120°):raa,na1,na2,1:rbb,nb1,nb2,1:rcc,nc1,nc2,1:rac,na2,nc2,100.+24.*π*𝐢:rcb,nc2,nb2,100.+24.*π*𝐢:rba,nb2,na2,100.+24.*π*𝐢"→cir:s\ac(cir,ω)
```
```sym 8
"ea1,na1,0,(100.∠0°):eb1,nb1,0,(100.∠–120°):ec1,nc1,0,(100.∠120°):raa,na1,na2,1:rbb,nb1,nb2,1:rcc,nc1,nc2,1:rac,na2,nc2,100.+24.*π*𝐢:rcb,nc2,nb2,100.+24.*π*𝐢:rba,nb2,na2,100.+24.*π*𝐢"→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
ea1,na1,0,100
eb1,nb1,0,(100∠-120°)
ec1,nc1,0,(100∠120°)
raa,na1,na2,1
rbb,nb1,nb2,1
rcc,nc1,nc2,1
rac,na2,nc2,100+24*pi*j
rcb,nc2,nb2,100+24*pi*j
rba,nb2,na2,100+24*pi*j
```

The line current is the current in one of the line resistors, and the phase
voltage is the difference between two load nodes:

::: only 9
`aa(iraa)` reads {{o:2.35}}∠{{o:-36.2}}° A and `aa(vna2-vnb2)` reads
{{o:169.94}}∠{{o:30.81}}° V. Both are correct.
:::

```sym 7
{s\aa(iraa),s\aa(vna2-vnb2),s\aa(irac)}
```
```sym 8
{s\aa(iraa),s\aa(vna2-vnb2),s\aa(irac)}
```
```out 7,8
{"2.35∠-36.2°","169.94∠30.8°","1.36∠-66.2°"}
```

::: only 9
For the phase current, `aa(irac)` reads {{o:1.357}}∠{{o:-66.2}}° A.
:::
:::
:::

### Unbalanced

If you find a simple unbalanced wye-delta problem, let me know.

## Delta-Delta {#delta-delta}

Until now, choosing a ground node was easy: the centre of the wye of sources.
A delta has no centre, which is the first problem. It is solved by picking one
of the delta's own nodes on the generator side and calling it **0**.

The second problem is subtler, and it is not Symbulator's alone — SPICE-like
simulators dislike it too. **A triangle of three voltage sources cannot be
solved.** The third source adds no information, because the first two already
fix the voltages at all three nodes, but it does add an unknown: the current
through it. Drop the redundant equation and the system has one unknown too
many.{{v9|{{i:delta-connected sources}}}}

::: warning Describe a delta source with two sources, not three
The trick is to leave one source out — the one opposite the node you chose as
ground. Two sources fix all three node voltages, so everything outside the
delta behaves exactly as it should.

The cost is that you learn nothing about the currents *inside* the sources:
the currents you get for the two you kept are not the currents they would
carry in a real three-source arrangement. Everything beyond the delta is
right; the inside of the generator is not.
:::

### Balanced

::: problem AS7's Example 12.4
A balanced Δ-connected load of 20 − j15 Ω is fed by a Δ-connected,
positive-sequence generator with {{var:V_ab}} = 330∠0° V. Find the phase
currents of the load and the line currents.

::: figure assets/circuit/as7e1204.png
AS7's Example 12.4
:::

::: answer
Node **c** becomes ground, so the source left out is the one opposite it. To
read the line currents we add three shorts to act as the lines.

```sym 7
"e0a,0,ag,(330.∠120°):eb0,bg,0,(330.∠-120°):sat,ag,ad:sbt,bg,bd:sct,0,cd:rab,ad,bd,20.-15.𝐢:rbc,bd,cd,20.-15.𝐢:rca,cd,ad,20.-15.𝐢"→cir:s\ac(cir,ω)
```
```sym 8
"e0a,0,ag,(330.∠120°):eb0,bg,0,(330.∠–120°):sat,ag,ad:sbt,bg,bd:sct,0,cd:rab,ad,bd,20.–15.𝐢:rbc,bd,cd,20.–15.𝐢:rca,cd,ad,20.–15.𝐢"→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
e0a,0,ag,(330∠120°)
eb0,bg,0,(330∠-120°)
sat,ag,ad
sbt,bg,bd
sct,0,cd
rab,ad,bd,20-15j
rbc,bd,cd,20-15j
rca,cd,ad,20-15j
```

The line currents are the currents through the shorts:

```sym 7
{s\aa(isat),s\aa(isbt),s\aa(isct)}
```
```sym 8
{s\aa(isat),s\aa(isbt),s\aa(isct)}
```
```out 7,8
{"22.86ᴇ0∠6.87°","22.86ᴇ0∠-113.13°","22.86ᴇ0∠126.87°"}
```

::: only 9
`aa(isat)`, `aa(isbt)` and `aa(isct)` read {{o:22.86}}∠{{o:6.87}}°,
{{o:22.86}}∠{{o:-113.13}}° and {{o:22.86}}∠{{o:126.87}}° A.
:::

Correct.
:::
:::

### Unbalanced

Nothing changes in the method. The load impedances simply differ, and the
answers stop being three copies of one another.

::: practice

::: problem AS7's Practice Problem 12.9
The unbalanced Δ-load is supplied by balanced line-to-line voltages of 440 V
in positive sequence. Find the line currents, taking {{var:V_ab}} as the
reference.

::: figure assets/circuit/as7pp1209.png
AS7's Practice Problem 12.9
:::

::: answer
```sym 7
false→s\rms
"e0a,0,ag,(440.∠120°):eb0,bg,0,(440.∠-120°):sla,ag,ad:slb,bg,bd:slc,0,cd:rab,ad,bd,10.-𝐢5.:rbc,bd,cd,16.:rca,cd,ad,8.+𝐢6."→cir:s\ac(cir,ω)
```
```sym 8
false→userms
"e0a,0,ag,(440.∠120°):eb0,bg,0,(440.∠–120°):sla,ag,ad:slb,bg,bd:slc,0,cd:rab,ad,bd,10.–𝐢5.:rbc,bd,cd,16.:rca,cd,ad,8.+𝐢6."→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
e0a,0,ag,(440∠120°)
eb0,bg,0,(440∠-120°)
sla,ag,ad
slb,bg,bd
slc,0,cd
rab,ad,bd,10-5j
rbc,bd,cd,16
rca,cd,ad,8+6j
```

```sym 7
{s\aa(isla),s\aa(islb),s\aa(islc)}
```
```sym 8
{s\aa(isla),s\aa(islb),s\aa(islc)}
```
```out 7,8
{"39.71ᴇ0∠-41.07°","64.12ᴇ0∠-139.77°","70.13ᴇ0∠74.27°"}
```

::: only 9
`aa(isla)`, `aa(islb)` and `aa(islc)` read {{o:39.71}}∠{{o:-41.07}}°,
{{o:64.12}}∠{{o:-139.77}}° and {{o:70.13}}∠{{o:74.27}}° A.
:::

Correct — and unlike the balanced case, all three differ in magnitude as well
as angle.
:::
:::

::: problem AS7's Practice Problem 12.10
Find the line currents in the unbalanced three-phase circuit, and the real
power absorbed by the load.

::: figure assets/circuit/as7pp1210.png
AS7's Practice Problem 12.10
:::

::: answer
These values are RMS, so {{v7,8|set the flag}}{{v9|tick {{ui:RMS phasors}} in
{{card:Settings}}}} — this one does ask for power.

```sym 7
true→s\rms
"e0a,0,ag,(220.∠-120°):eb0,bg,0,(220.∠120°):sla,ag,ad:slb,bg,bd:slc,0,cd:rab,ad,bd,-𝐢5.:rbc,bd,cd,𝐢10.:rca,cd,ad,10."→cir:s\ac(cir,ω)
```
```sym 8
true→userms
"e0a,0,ag,(220.∠–120°):eb0,bg,0,(220.∠120°):sla,ag,ad:slb,bg,bd:slc,0,cd:rab,ad,bd,–𝐢5.:rbc,bd,cd,𝐢10.:rca,cd,ad,10."→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
e0a,0,ag,(220∠-120°)
eb0,bg,0,(220∠120°)
sla,ag,ad
slb,bg,bd
slc,0,cd
rab,ad,bd,-5j
rbc,bd,cd,10j
rca,cd,ad,10
```

```sym 7
{s\aa(isla),s\aa(islb),s\aa(islc),prca+prab+prbc}
```
```sym 8
{s\aa(isla),s\aa(islb),s\aa(islc),prca+prab+prbc}
```
```out 7,8
{"64.00ᴇ0∠80.1°","38.11ᴇ0∠-60.°","42.50ᴇ0∠-135.°",4840.0}
```

::: only 9
The three line currents read {{o:64.00}}∠{{o:80.1}}°,
{{o:38.11}}∠{{o:-60}}° and {{o:42.50}}∠{{o:-135}}° A.

For the power, add the three loads' consumption in {{card:Evaluate}}:

```field 9 Evaluate
prca+prab+prbc
```

It gives {{o:4840}} W.
:::

Correct.
:::
:::

::: problem AS7's Example 12.12
For the unbalanced Δ-Δ circuit, find the generator current {{var:I_ab}}, the
line current {{var:I_bB}} and the phase current {{var:I_BC}}.

::: figure assets/circuit/as7e1212.png
AS7's Example 12.12
:::

::: answer
Two of the three are ordinary element currents. The first — the current
*inside* the generator — is the awkward one, and it is dealt with after them.

```sym 7
false→s\rms
"e0a,0,ag,(208.∠130°):eb0,bg,0,(208.∠-110°):rla,ag,ad,2.+𝐢5.:rlb,bg,bd,2.+𝐢5.:rlc,0,cd,2.+𝐢5.:rab,ad,bd,50.:rbc,bd,cd,𝐢30.:rca,cd,ad,-𝐢40."→cir:s\ac(cir,ω)
```
```sym 8
false→userms
"e0a,0,ag,(208.∠130°):eb0,bg,0,(208.∠–110°):rla,ag,ad,2.+𝐢5.:rlb,bg,bd,2.+𝐢5.:rlc,0,cd,2.+𝐢5.:rab,ad,bd,50.:rbc,bd,cd,𝐢30.:rca,cd,ad,–𝐢40."→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
e0a,0,ag,(208∠130°)
eb0,bg,0,(208∠-110°)
rla,ag,ad,2+5j
rlb,bg,bd,2+5j
rlc,0,cd,2+5j
rab,ad,bd,50
rbc,bd,cd,30j
rca,cd,ad,-40j
```

```sym 7
{s\aa(irlb),s\aa(irbc)}
```
```sym 8
{s\aa(irlb),s\aa(irbc)}
```
```out 7,8
{"9.106ᴇ0∠168.48°","5.500ᴇ0∠172.47°"}
```

::: only 9
*Find equivalent* is not needed here — a plain AC solve gives both. `aa(irlb)`
reads {{o:9.106}}∠{{o:168.48}}° A and `aa(irbc)` reads
{{o:5.500}}∠{{o:172.47}}° A, matching the printed answers.
:::

The remaining answer, the generator current, is trickier. They ask for the
current in the source we did not simulate — and even for one of the two we did
have, we could not trust it, since the real circuit uses three.

Now, I tried something, and I think I got lucky, because I got the answer the
book gives. This is what I tried:

```sym 7
s\aa(-(ie0a+ieb0)/3)
```
```sym 8
s\aa(–(ie0a+ieb0)/3)
```

::: only 9
`-(ie0a+ieb0)/3` in {{card:Mini-Tools}} with *aa*, which takes an expression as
readily as a name and answers with the magnitude and the angle.
:::

What I thought was: the current coming out of the two sources in my simulation
would, in reality, come out of three. So adding those two currents and dividing
by three may approximate the current out of one source. I am confident that
holds in a balanced circuit. This one is not balanced, but it was the best I
had. So I tried it.

```out 7,8
"5.959ᴇ0∠-177.18°"
```

::: only 9
{{o:5.959}}∠{{o:-177.18}}° A
:::

And it worked. That is the answer in the book.

::: warning Treat that as a guess that was checked, not as a method
The argument holds in a balanced circuit. This one is not balanced; it was
used because there was nothing better to hand, and it happened to land on the
book's figure. Check it against something before trusting it elsewhere.
:::
:::
:::

:::

## Delta-Wye {#delta-wye}

The Δ-Y is the platypus of three-phase systems. The sensible route is usually
to convert the Δ source into an equivalent Y and solve it as a Y-Y — and if
you are doing this by hand, do that.

Inside Symbulator there is another way: make the **centre of the wye load**
the ground node, and describe the delta source with two sources as before.

### Balanced

::: problem AS7's Example 12.5
For the balanced Δ-Y circuit, find the line currents.

::: figure assets/circuit/as7e1205.png
AS7's Example 12.5
:::

::: answer
```sym 7
false→s\rms
"eca,c,a,(210.∠120°):ebc,b,c,(210.∠-120°):ra,a,0,40.+𝐢25.:rb,b,0,40.+𝐢25.:rcc,c,0,40.+𝐢25."→cir:s\ac(cir,ω)
```
```sym 8
false→userms
"eca,c,a,(210.∠120°):ebc,b,c,(210.∠–120°):ra,a,0,40.+𝐢25.:rb,b,0,40.+𝐢25.:rcc,c,0,40.+𝐢25."→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
eca,c,a,(210∠120°)
ebc,b,c,(210∠-120°)
ra,a,0,40+25j
rb,b,0,40+25j
rc,c,0,40+25j
```

Node **0** here is the centre of the load's wye, not a node of the source at all.

```sym 7
{s\aa(ira),s\aa(irb),s\aa(ircc)}
```
```sym 8
{s\aa(ira),s\aa(irb),s\aa(ircc)}
```
```out 7,8
{"2.570ᴇ0∠-62.01°","2.570ᴇ0∠177.99°","2.570ᴇ0∠57.99°"}
```

::: only 9
`aa(ira)`, `aa(irb)` and `aa(irc)` read {{o:2.570}}∠{{o:-62.01}}°,
{{o:2.570}}∠{{o:177.99}}° and {{o:2.570}}∠{{o:57.99}}° A.
:::

Correct — balanced, so three equal magnitudes 120° apart.
:::
:::

### Unbalanced

If you find a simple unbalanced delta-wye problem, let me know.
