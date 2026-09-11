---
id: input-files
kind: note
title: Working with input files
versions: [9]
updated: 2026-09-09
summary: >
  Load the tutorial's built-in examples, save your own circuits as entries, and download an input file to your device. Plus everything an entry remembers, so you can pick up where you left off.
---

Everything you type into Symbulator — circuit, analysis, settings, the
{{card:Evaluate}} and {{card:Solve}} cards — can be saved and reused. Two words matter
here.

- An **entry** is one named set of inputs: a circuit, the analysis to run on it, and the settings.

- An **input file** is a named collection of entries, such as *Circuits for Lesson 1 of the Tutorial*.

Input files are plain text with the extension **`.cir`**. They are optional. The buttons to load, download and create them are in the {{card:Input File}} card at the top of the app.

## Loading input files

Symbulator comes with an input file for each lesson of this tutorial, holding
an entry for every simulation in it. A problem that takes more than one
simulation has an entry for each, so a lesson file may hold more entries than
the lesson has problems. With them you can follow the whole tutorial without
typing a circuit.

{{card:Built-in examples}} lists them; click a title to load it. These files are
**read-only**: change a loaded one as much as you like, but you cannot write
back to it.

To open your own input file, click {{btn:Upload}} and choose the `.cir` file. The dropdown beneath then reads *Entries in* and the file's name.
Choosing an entry fills in every box on the page. Solve it as if you had just
typed it.

Saving an entry while a read-only file is loaded, or clicking {{btn:Create new}}, starts a blank input file of your own.

## Saving your work

Two links under the circuit box appear when they apply:

- {{btn:Save inputs to new entry}} adds what is on screen as a new entry and asks
  for a name.
- {{btn:Update inputs in this entry}} writes your changes back into the loaded
  entry. It appears once you have changed something.

Beside the dropdown, {{btn:Rename}} and {{btn:Delete}} act on the entry itself.
Neither is offered for the built-in examples, since they are read-only.

::: warning Nothing reaches your disk until you press Download
Saving an entry writes it into the file open **in your browser**. Only
{{btn:Download}} produces a `.cir` on your device.

Your work is mirrored into the browser's storage, so closing the tab does not
lose it, and you are warned before anything replaces a file with entries you
have not downloaded. Still, download when you are done.
:::

## What an entry remembers

An entry keeps everything you typed, not just the circuit: the analysis and
what it needs (the frequency, the nodes of an equivalent, the kind of
two-port), the {{card:Expert Mode}} equations, unknowns and conditions, everything in
{{card:Settings}}, {{card:Evaluate}} and its {{ui:Conditions}}, the {{card:Solve}} card, the
{{card:Plotting Tools}} inputs, and a note of your own shown when the entry is
loaded. Load one a year later and you are back where you left off.

The {{card:About input file (.cir) format}} section inside the {{card:Input File}} card explains what input files carry, in detail.
