# The thesis's figures, and the three illustrated editions

The 2001 thesis is full of circuit drawings. Its English translation —
*The Symbulator Book*, `../the_symbulator_book.tex` — carried **none**
until 10 Sep 2026: zero `\includegraphics` across all thirteen files,
while the text says "shown in the figure" throughout. The figures were
never lost. They sit embedded in the original Word chapters under
`../references/2000_thesis/`, and this folder is what recovers them.

## Order of operations

Two of these write assets the rest read, and neither is committed —
both are regenerable, so run them first in a fresh clone:

```
py carve_png.py            # -> thesis_png/   150 PNGs out of the .doc files
py render_v9.py            # -> v9_svg/        86 circuits drawn by v9
```

Then either:

```
py build_thesis_pdfs.py            # the three editions -> ../build_thesis/
py check_pdfs.py                   # and prove they differ as intended
```

or, for the Book itself:

```
py illustrate_book.py      # edits ../book/*.tex and ../the_symbulator_book.tex
```

`illustrate_book.py` has already been run; it refuses to run twice.

## What each piece does

| file | |
|---|---|
| `carve_png.py` | Carves embedded PNGs from a Word 97 `Data` stream, signature to `IEND`, so the extent is exact. 150 images, none corrupt. |
| `pair_figures.py` | Pairs each picture with its caption. **The delicate one** — see below. |
| `parse_book.py` | Reads the Book's `\problem{NNN}` markers: statement, entry blocks, and the `→` variable stores. |
| `to_v9.py` | Rewrites a Symbulator Q description as version 9. |
| `render_v9.py` | Draws every circuit with the v9 schematic engine. |
| `solve_all.py` | Runs every converted netlist through the solver. 84 of 89 solve. |
| `contact_sheet.py`, `compare_sheet.py` | Browsable HTML for checking the pairing by eye. |
| `build_thesis_pdfs.py` | The three editions. |
| `illustrate_book.py` | Puts the figures into the Book's own source, once. |

## The pairing, and the three ways it went wrong

Word stores a picture per *appearance*, in document order, and the `.txt`
extraction keeps captions in document order, so the two sequences agree —
but they are not the same length, and matching on counts alone silently
shifts every figure after the first discrepancy. Three faults, all found
by Roberto reading `compare_sheet.html`, and all worth keeping:

1. **A figure embedded twice.** Chapter 5's Figure 36 is in the file
   twice, byte for byte. The repeat ate Problem 021's slot, so 020 and
   021 showed the same drawing. Fixed by hash: a picture identical to the
   one before it is the same figure shown again.
2. **A caption the matcher could not see.** The extraction spaces long
   runs out character by character — `F i g u r a 4 1 .` — and a pattern
   written for the normal spelling finds nothing there. That hid **14**
   figures, Problem 025's among them. Captions are now matched against
   whitespace-stripped text, which the damage cannot fool.
3. **Classifying by the open set.** Screens were identified by listing
   words like "Pantalla" and "Tipo de red"; every one missed turned a
   screen into a drawing that then stole a circuit's slot. The circuit
   captions are the closed set — the thesis always writes *"Circuito para
   el Problema N° NNN"* — so that is the key now, and everything else is
   a screen.

Two guards worth re-running after any change here: every caption in every
chapter must find a picture (`py pair_figures.py`, all zeros in the last
two columns), and no scan may appear under two different problems.

## What the sources say, so nobody re-derives it

* **89 problems**, matching Appendix D of the thesis exactly.
* **93 figures.** Five problems have none, and the thesis says so itself:
  048, 057, 059, 060 and 072 each open *"Este problema no tiene figura."*
* **84 of 89 solve** under version 9; 052 and 071 do not, and 066, 074
  and 089 are not circuit runs (089 is the Appendix C problem solved with
  `cSolve`, deliberately, to argue against using the simulator).
* **Three problems store their two-port parameters in calculator
  variables** rather than in the description — `20.→zp11` and kin — and
  Q had no other way to do it. 039, 040 and 048. Read the `sq\` line
  alone and the block has no parameters at all, which is both a wrong
  drawing and wrong answers.
