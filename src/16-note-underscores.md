---
id: underscores
kind: note
title: Underscores, and subscripts in your answers
versions: [9]
updated: 2026-09-11
books: [3]
summary: >
  An underscore does two jobs. In an answer's name it is optional, so `ir1` and `i_r1` mean the same current. In a symbolic value it is not: it puts what follows into a subscript, and makes an answer read the way a textbook prints it.
---

The underscore does two different jobs in Symbulator, and it is worth
knowing which is which. In the name of an **answer** it is optional and
changes nothing. In the **value** you give an element, it changes how the
answer is typeset.{{i:underscore}}

## In an answer's name, it is optional

You may write the name of any of Symbulator's answers in two ways: with
or without an underscore. `ir1` and `i_r1` are the same current, `v2` and
`v_2` the same voltage; capitals make no difference either.{{i:answer names}}

Version 9 added the longer spelling so that a name written out by a
machine reads back without ambiguity; the shorter one is what the
calculators used, and it is what this tutorial uses throughout. Neither
is more correct than the other, and you can mix them freely — wherever
you type an answer's name, in {{card:Evaluate}}, in {{card:Solve}}, in a
condition, or (in the case of dependent sources) as part of an element's
value, Symbulator recognises both formats.

## In a symbolic value, it makes a subscript

Textbooks set their symbols with subscripts: {{var:v_cc}}, {{var:r_b}},
{{var:i_rb}}. Symbolic answers can be made to read the same way, and the
trick is very simple: **put an underscore in your symbolic variable
names.** The text after the underscore is set as a subscript.{{i:subscripts in answers}}

That is all there is to it. `v_cc` prints as {{var:v_cc}}, `r_e1` as
{{var:r_e1}}. It costs nothing, it changes no answer, and it makes a
symbolic result that much easier to compare with the page you are
working from.

::: problem TR5's Example 4.5 (Symbolic)
The same circuit twice: once with plain names, once with subscripted
ones, so the difference is only in how the answer reads.
:::

Given this circuit description, with plain names:

```field 9 Circuit Description
e1,1,0,vcc
rb,1,b,rb
e2,e,b,vγ
re1,e,0,re1
rc,1,c,rc
j,c,e,β*irb
```

the current through **rb** comes back as

::: result
i_{rb} = \dfrac{vcc + v\gamma}{r_{e1}\,\beta + r_{e1} + rb}
:::

One subscript arrives without being asked for: **re1** prints as
{{var:r_e1}}, because trailing digits are set as a subscript anyway. The
underscore is what gets you the rest.

Run the same circuit with underscores in the symbolic values instead:

```field 9 Circuit Description
e1,1,0,v_cc
rb,1,b,r_b
e2,e,b,v_γ
re1,e,0,r_e1
rc,1,c,r_c
j,c,e,β*irb
```

and the answer is typeset the way the book prints it:

::: result
i_{rb} = \dfrac{v_{cc} + v_{\gamma}}{r_{b} + r_{e1}\,\beta + r_{e1}}
:::

The two answers are the same expression. Only their appearance differs.
