---
id: lesson-twoports
kind: lesson
title: Two-ports
updated: 2023-07-08
summary: >
  Find the *two-port equivalent* of a network using the **port** script. Learn
  how to include *two-ports* in your circuit using the **z**, **y**, **h**,
  **g**, **a** and **b** elements. Calculate gains with the **gain** tool.
---

A two-port is a network you have stopped caring about the inside of. What is
left is four numbers relating the voltage and current at one pair of terminals
to the voltage and current at the other. Symbulator will find those four
numbers for you, and will also take them as an element in a larger
circuit.{{i:two-port}}

## Find two-port equivalents {#port-script}

{{v7,8|The tool is called **port**.}}{{v9|Set **Type of analysis** to *Find
equivalent* and **Type of equivalent** to *Two-port parameters*.}} It takes the network and the two **top** nodes of the
pair of terminals you want to reduce. The two bottom nodes are always assumed
to be ground.

There are six kinds of parameters — z, y, h, g, a and b — and you choose which
you want.

::: problem AS7's Example 19.1
Determine the z parameters for the circuit.

::: figure assets/circuit/as7e1901.png
AS7's Example 19.1
:::

::: answer
First describe the network, exactly as you would describe any circuit:

```sym 7
"r1,1,2,20:r2,2,0,40:r3,2,3,30"→cir:s\port(cir,1,3)
```
```sym 8
"r1,1,2,20:r2,2,0,40:r3,2,3,30"→cir:s\port(cir,1,3)
```
```field 9 Circuit Description
r1,1,2,20
r2,2,0,40
r3,2,3,30
```

::: only 7
When asked, specify DC as the analysis and `z` as the parameter type.

Then it wants a name. Because `z11`, `z12`, `z21` and `z22` are reserved
variables on the calculator, `z` alone is not available — you are asked to add
between one and six more characters. The default offered is `p`, so pressing
Enter gives you a two-port called `zp`.
:::
::: only 8
When asked, specify DC as the analysis and `z` as the parameter type.

Then it wants a name. You are offered the chance to add between one and six
more characters to it, and you can leave that empty — the Nspire does not
reserve `z11`, `z12`, `z21` and `z22`, so the two-port can simply be called
`z`.
:::
::: only 9
*Find equivalent*, then *Two-port parameters*, with **Parameters** set to
*z — impedance* and **1** and **3** in the two node boxes. In DC.

There is no name to invent: version 9 does not store its answers in calculator
variables, so the four come back as `z11`, `z12`, `z21` and `z22`.
:::

```out 7,8
z11 is 60, z12 is 40, z21 is 40, z22 is 70
```

::: only 9
**Results** gives `z11` = {{o:60}}, `z12` = {{o:40}}, `z21` = {{o:40}} and
`z22` = {{o:70}}.
:::

Correct.
:::
:::

## Use two-ports as elements {#twoport-elements}

A two-port can be an element in a bigger circuit. Its description is three
fields: a name whose first letter says which kind it is, then the **top left**
node and the **top right** node. Both bottom nodes are ground, always.

```field 9 Circuit Description
z,1,2
```

That is a z-type two-port between nodes 1 and 2.

### Giving it its four parameters

::: only 7,8
Three possibilities.

**Store them first**, in variables named after the two-port plus 11, 12, 21
and 22:

```sym 7
40→zp11:𝐢*20→zp12:𝐢*30→zp21:50→zp22
```
```sym 8
40→z11:𝐢*20→z12:𝐢*30→z21:50→z22
```

**Enter them when prompted.** If you run a simulation without storing them
first, Symbulator asks whether you want to define them, and you can use SI
shorthand in the values you type.

**Leave them undefined**, in which case they stay symbolic and appear as
variables in the answers.
:::
::: only 9
Two possibilities.

**Leave them undefined**, in which case they stay symbolic and appear in the
answers as `z11`, `z12`, `z21` and `z22`. That is often what you want —
the answer as a formula in the parameters.

**Pin them in Expert Mode**, one equation each, under **Add equations**:

```field 9 Add equations
z11 = 40
z12 = 20j
z21 = 30j
z22 = 50
```

::: warning Expert Mode is only there for a plain solve
The **Add equations** box disappears as soon as you choose *Find equivalent*,
whichever kind — those tools do not take it. To use a two-port with
numbers inside one of them, solve it symbolically and substitute afterwards;
Example 19.6 below does exactly that.
:::
:::

**What answers do you get?** The current entering each port, named with the
two-port and the port number — for a two-port {{v7|`zp`, that is `izp1` and `izp2`}}{{!v7|`z`, that is `iz1` and `iz2`}}.

::: problem AS7's Example 19.2
Find I{{sub:1}} and I{{sub:2}} in the circuit.

::: figure assets/circuit/as7e1902.png
AS7's Example 19.2
:::

::: answer
```sym 7
"e,1,0,100:zp,1,2:r,2,0,10"→cir:s\ac(cir,ω)
```
```sym 8
"e,1,0,100:z,1,2:r1,2,0,10"→cir:s\ac(cir,ω)
```
```field 9 Circuit Description
e,1,0,100
z,1,2
r,2,0,10
```

::: only 9
With the four parameters pinned in **Add equations** as above, and AC.
:::

```sym 7
s\aa(izp1)
s\aa(izp2)
```
```sym 8
s\aa(iz1)
s\aa(iz2)
```

::: only 9
`aa(iz1)` reads {{o:2}}∠{{o:0}}° and `aa(iz2)` reads
{{o:1}}∠{{o:-90}}°.
:::
:::
:::

## Instructive two-port problems {#practice-twoports}

::: practice

::: problem AS7's Example 19.3
Obtain the y parameters for the network.

::: figure assets/circuit/as7e1903.png
AS7's Example 19.3
:::

::: answer
```sym 7
"r1,1,0,4:r2,1,2,2:r3,2,0,8"→cir:s\port(cir,1,2)
```
```sym 8
"r1,1,0,4:r2,1,2,2:r3,2,0,8"→cir:s\port(cir,1,2)
```
```field 9 Circuit Description
r1,1,0,4
r2,1,2,2
r3,2,0,8
```

::: only 9
*Find equivalent*, *Two-port parameters*, *y — admittance*, nodes **1** and
**2**, DC.
:::

```sym 7
{yp11,yp12,yp21,yp22}
```
```sym 8
{y11,y12,y21,y22}
```
```out 7,8
{3/4,-1/2,-1/2,5/8}
```

::: only 9
{{o:3/4}}, {{o:-1/2}}, {{o:-1/2}}, {{o:5/8}}.
:::

Correct.
:::
:::

::: problem AS7's Example 19.4
Determine the y parameters for the two-port shown. Note the dependent source.

::: figure assets/circuit/as7e1904.png
AS7's Example 19.4
:::

::: answer
```sym 7
"r1,1,2,8:r2,2,0,2:r3,2,3,4:j,2,3,2*ir1"→cir:s\port(cir,1,3):{yp11,yp12,yp21,yp22}
```
```sym 8
"r1,1,2,8:r2,2,0,2:r3,2,3,4:j,2,3,2*ir1"→cir:s\port(cir,1,3):{y11,y12,y21,y22}
```
```field 9 Circuit Description
r1,1,2,8
r2,2,0,2
r3,2,3,4
j,2,3,2*ir1
```

::: only 9
*y*, nodes **1** and **3**, DC. A two-port equivalent works perfectly well
around a controlled source.
:::

```out 7,8
{3/20,-1/20,-1/4,1/4}
```

::: only 9
{{o:3/20}}, {{o:-1/20}}, {{o:-1/4}}, {{o:1/4}}.
:::

Correct.
:::
:::

::: problem AS7's Example 19.5
Find the hybrid parameters for the two-port network.

::: figure assets/circuit/as7e1905.png
AS7's Example 19.5
:::

::: answer
```sym 7
"r1,1,2,2:r2,2,0,6:r3,2,3,3"→cir:s\port(cir,1,3):{h11,h12,h21,h22}
```
```sym 8
"r1,1,2,2:r2,2,0,6:r3,2,3,3"→cir:s\port(cir,1,3):{h11,h12,h21,h22}
```
```field 9 Circuit Description
r1,1,2,2
r2,2,0,6
r3,2,3,3
```

::: only 7,8
For h, g, a and b there is no name clash, so the single letter is available.
Specify DC and `h`, and leave the extra character empty.
:::
::: only 9
*h — hybrid*, nodes **1** and **3**, DC.
:::

```out 7,8
{4,2/3,-2/3,1/9}
```

::: only 9
{{o:4}}, {{o:2/3}}, {{o:-2/3}}, {{o:1/9}}.
:::

Correct.
:::
:::

::: problem AS7's Example 19.6
Determine the Thévenin equivalent at the output port of the circuit, whose
h parameters are 1000 Ω, −2, 10 and 2×10⁻⁴ S.

::: figure assets/circuit/as7e1906.png
AS7's Example 19.6
:::

::: answer
```sym 7
"e,1,0,60:r,1,2,40:h,2,3"→cir:1000.→h11:-2→h12:10→h21:2.ᴇ-4→h22:s\th(cir,3,0):{vth,zeq}
```
```sym 8
"e,1,0,60:r1,1,2,40:h,2,3"→cir:1000.→h11:-2→h12:10→h21:2.ᴇ-4→h22:s\th(cir,3,0):{vth,req}
```
```field 9 Circuit Description
e,1,0,60
r,1,2,40
h,2,3
```

::: only 9
*Find equivalent*, *Thévenin / Norton*, nodes **3** and **0**, DC. The
parameters cannot be pinned here — the equivalent tools take no Expert Mode
equations — so the answers come back as formulas:

$v_{th} = \dfrac{-60\,h_{21}}{h_{11}h_{22} - h_{12}h_{21} + 40\,h_{22}}$

Which is more useful than it looks: put `vth` in **Evaluate** with the four
parameters in its **Conditions** box, and the number falls out.

```field 9 Evaluate
vth
```

```field 9 Conditions
h11 = 1000
h12 = -2
h21 = 10
h22 = 2e-4
```

Then ask for `req` under the same conditions.
:::

```out 7,8
{-29.69,51.46}
```

::: only 9
`vth` comes back {{o:-29.69}} V and `req` {{o:51.46}} Ω.
:::

Correct.
:::
:::

::: problem AS7's Example 19.7
Find the g parameters as functions of s for the circuit.

::: figure assets/circuit/as7e1907.png
AS7's Example 19.7
:::

::: answer
```sym 7
"l,1,2,1:r,2,0,1:c,2,3,1"→cir:s\port(cir,1,3):{{g11,g12},{g21,g22}}
```
```sym 8
"l,1,2,1:r1,2,0,1:c,2,3,1"→cir:s\port(cir,1,3):{{g11,g12},{g21,g22}}
```
```field 9 Circuit Description
l,1,2,1
r,2,0,1
c,2,3,1
```

::: only 9
*g — inverse hybrid*, nodes **1** and **3**, and this time in **FD**, since
the question asks for functions of s.
:::

```out 7,8
{1/(s+1),-1/(s+1),1/(s+1),(s^2+s+1)/(s*(s+1))}
```

::: only 9
`g11` = $1/(s+1)$, `g12` = $-1/(s+1)$, `g21` = $1/(s+1)$ and `g22` =
$(s^2+s+1)/(s(s+1))$.
:::
:::
:::

::: problem AS7's Practice Problem 19.7
For the ladder network, determine the g parameters in the s domain.

::: figure assets/circuit/as7pp1907.png
AS7's Practice Problem 19.7
:::

::: answer
```sym 7
"l1,1,2,1:r1,2,0,1:l2,2,3,1:r2,3,0,1"→cir:s\port(cir,1,3):{{g11,g12},{g21,g22}}
```
```sym 8
"l1,1,2,1:r1,2,0,1:l2,2,3,1:r2,3,0,1"→cir:s\port(cir,1,3):{{g11,g12},{g21,g22}}
```
```field 9 Circuit Description
l1,1,2,1
r1,2,0,1
l2,2,3,1
r2,3,0,1
```

```out 7,8
[[(s+2)/(s^2+3*s+1),-1/(s^2+3*s+1)][1/(s^2+3*s+1),s*(s+2)/(s^2+3*s+1)]]
```

::: only 9
*g*, nodes **1** and **3**, FD. The four come back as
$(s+2)/(s^2+3s+1)$, $-1/(s^2+3s+1)$, $1/(s^2+3s+1)$ and
$s(s+2)/(s^2+3s+1)$.
:::

Correct.
:::
:::

::: problem AS7's Example 19.8
Find the transmission parameters for the two-port network.

::: figure assets/circuit/as7e1908.png
AS7's Example 19.8
:::

::: answer
```sym 7
"r1,1,2,10:r2,2,0,20:e,2,3,3ir1"→cir:s\port(cir,1,3):[[a11,a12][a21,a22]]
```
```sym 8
"r1,1,2,10:r2,2,0,20:e,2,3,3ir1"→cir:s\port(cir,1,3):[[a11,a12][a21,a22]]
```
```field 9 Circuit Description
r1,1,2,10
r2,2,0,20
e,2,3,3*ir1
```

::: only 9
*a — transmission*, nodes **1** and **3**, DC.
:::

```out 7,8
[[1.765,15.29][.0588,1.176]]
```

::: only 9
{{o:1.765}}, {{o:15.29}}, {{o:0.0588}}, {{o:1.176}}.
:::

Correct.
:::
:::

:::

## The gain tool {#gain-tool}

Network problems ask for gains: voltage gain, current gain, power gain, and
the impedance seen at the input. {{v7,8|Symbulator has a tool for that, called
**gain**.}}{{v9|Symbulator has a tool for that, in the **Mini-Tools** card:
choose *gain*.}}{{i:gain tool}}

It wants four values — the voltage and current at the input, then the voltage
and current at the output — and answers with all four figures at once.

::: problem Gain Example 1
For the circuit below, find G{{sub:v}}, G{{sub:i}}, G{{sub:p}} and
Z{{sub:in}}. The two-port has y parameters y{{sub:11}} = 0.4,
y{{sub:12}} = −0.002, y{{sub:21}} = −5 and y{{sub:22}} = 0.04.

::: figure assets/circuit/gain-example-1.png
Gain Example 1
:::

::: answer
The source is 1 V because its value does not matter to a gain — it cancels.
A symbolic `vs` would do just as well.

```sym 7
"es,3,0,1:rs,3,1,2:rl,2,0,20:yp,1,2"→cir:s\dc(cir)
```
```sym 8
"es,3,0,1:rs,3,1,2:rl,2,0,20:y,1,2"→cir:s\dc(cir)
```
```field 9 Circuit Description
es,3,0,1
rs,3,1,2
rl,2,0,20
y,1,2
```

::: only 9
Pin the four parameters in **Add equations**:

```field 9 Add equations
y11 = 0.4
y12 = -0.002
y21 = -5
y22 = 0.04
```

Solve in DC, then open **Mini-Tools**, choose *gain*, and give it the four:
:::

```sym 7
s\gain()
```
```sym 8
s\gain()
```

::: only 9
```field 9 v1
v1
```

```field 9 i1
iy1
```

```field 9 v2
v2
```

```field 9 i2
iy2
```
:::

```out 7,8
Av 55.6, Ai -9.62, Ap 534, Zin 3.46 Ω
```

::: only 9
| | |
|---|---|
| Av — voltage gain | {{o:55.56}} |
| Ai — current gain | {{o:-9.615}} |
| Ap — power gain | {{o:534.2}} |
| Zi — input impedance | {{o:3.462}} Ω |
:::

These are correct.
:::
:::

::: problem Gain Example 2
Find G{{sub:v}}, G{{sub:i}}, G{{sub:p}} and Z{{sub:in}} for a two-port with
z parameters z{{sub:11}} = 4, z{{sub:12}} = 1.5, z{{sub:21}} = 10 and
z{{sub:22}} = 3, driven by a source V{{sub:s}} with 5 Ω in series and loaded
with 2 Ω.

There is no picture of this one — the description below is the whole circuit.

::: answer
The same shape as before, with z parameters instead of y.

```sym 7
"es,3,0,1:rs,3,1,5:rl,2,0,2:zp,1,2"→cir:s\dc(cir)
```
```sym 8
"es,3,0,1:rs,3,1,5:rl,2,0,2:z,1,2"→cir:s\dc(cir)
```
```field 9 Circuit Description
es,3,0,1
rs,3,1,5
rl,2,0,2
z,1,2
```

::: only 7,8
When prompted, specify DC as the analysis and **z** as the parameter type. You
can store the parameters in variables beforehand or type them when asked.
:::

::: only 9
Pin the four parameters in **Add equations**:

```field 9 Add equations
z11 = 4
z12 = 1.5
z21 = 10
z22 = 3
```

Solve in DC, then open **Mini-Tools**, choose *gain*, and give it the four:
:::

```sym 7
s\gain()
```
```sym 8
s\gain()
```

::: only 7,8
It asks for the in voltage, in current, out voltage and out current. Type
`v1`, `izp1`, `v2` and `izp2` respectively.
:::

::: only 9
```field 9 v1
v1
```

```field 9 i1
iz1
```

```field 9 v2
v2
```

```field 9 i2
iz2
```
:::

```out 7,8
Gv 4, Gi -2, Gp 8, Zin 1 Ω
```

::: only 9
| | |
|---|---|
| Av — voltage gain | {{o:4}} |
| Ai — current gain | {{o:-2}} |
| Ap — power gain | {{o:8}} |
| Zi — input impedance | {{o:1}} Ω |
:::

These are correct.
:::
:::
