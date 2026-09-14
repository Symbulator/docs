---
id: as7-sampler
kind: back
title: Examples from Alexander & Sadiku 7e
versions: [9]
updated: 2026-09-14
summary: >
  Fifty worked examples from *Fundamentals of Electric Circuits*, each described
  in Symbulator and checked against the answer the book prints. DC, AC, TR and
  FD, with two-ports, the By-Hand Equations card, the Solve card and the
  Mini-Tools.
---

Here is a selection of problems from *Fundamentals of Electric Circuits*, 7th
edition, by Charles K. Alexander and Matthew N. O. Sadiku (McGraw-Hill). The
Course's own lessons already draw many of their problems from this book, and
none of the fifty here repeats one of theirs. These are not the easiest
problems in the book, but they are well suited to showing what Symbulator can
do, since they are the ones where the distance between *describing a circuit*
and *solving it by hand* is widest. The book works each of them by a named
method, and here each question is trimmed to what is asked, since Symbulator is
told the circuit and never the method.

::: note What this chapter is not
This is not a solutions manual, and it will not teach you circuit analysis.
Every example here is worked in full in the book itself, and the book's
derivation is the part worth reading. This is a demonstration, aimed at someone
who already knows the material and wants to see how the software deals with it.
:::

The problems and diagrams are reproduced for the purpose of teaching students how to use
Symbulator, under the principle of fair use. No copyright infringement is intended.

## How to read an entry {#as7-how}

Each entry gives the book's question, the book's own figure, the Symbulator
description, the analysis to choose, and the answers. Every value on the page,
in a panel or in a sentence, was compared with the answer the book prints, and
they agree. Where the two are written differently, the entry's paragraph says
so.

The names are the app's own. `i_r3` is the current through the element called
`r3`, `v_2` the voltage at node 2, `p_e` the power consumed by the source called
`e`, and `v_r6` the voltage across `r6`. The book names its quantities
differently, so each entry says which of the app's answers is which of the
book's.

### Every circuit is in the app already {#as7-entries}

Nothing here has to be typed. All fifty circuits ship with Symbulator as a
built-in example book. Open {{card:Built-in Examples}} and pick
*Alexander & Sadiku 7ed* from the list of books. The entries are named for the
example each one comes from, and each arrives with its note, its picture, its
settings, its Solve card fields and the analysis it wants already set.

Pick one, press {{btn:Run Symbulator}}, and the answers below are what you get.
{{ref:input-files}} explains what an entry remembers and how to save your own.
