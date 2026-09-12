# The Nilsson & Riedel sampler — its generator (#425)

**Two published files are output of this folder and must not be edited by
hand:**

| generated | from |
|---|---|
| `Documentation/src/98-nr12-sampler.md` | `specs.py` + `chapter_head.md` + `intro_*.md`, rendered by `gen.py` |
| `Application/v9/repos/server/examples/Nilsson_Riedel.cir` | the same `specs.py`, rendered by `gen.py` |

Editing either by hand works right up until the next `gen.py`, which
discards it — the same trap `repos/local/index.html` has. Worse here,
because the two outputs share their source: a chapter's `ask` text is also
the `.cir` entry's `note:`, so hand-editing the page and not the book
desyncs the app's built-in entry from the page describing it.

    py Documentation\tools\nr12\gen.py

runs from anywhere and rewrites both. It printed byte-identical output to
what is live when it was moved here, which is the check to repeat after any
edit: regenerate, then `git status` — only what you meant to change should
appear.

## The files

| | |
|---|---|
| `specs.py` | **the data.** One dict per example: the book's question, the Symbulator description, the analysis, the answers to check against, and the prose. 43 of them |
| `chapter_head.md` | **hand-editable markdown**: the front matter, the opening and *How to read an entry* — everything before the first section heading. `gen.py` copies it verbatim to the top of the chapter |
| `intro_dc.md`, `intro_tr.md`, `intro_ac.md`, `intro_fd.md` | **hand-editable markdown**: the paragraph under each section heading. Each must open with its count in words (*Sixteen*, *Fourteen*…), which `gen.py` asserts against the specs |
| `titles.py` | the short problem titles. **Load-bearing — see below** |
| `gen.py` | renders both outputs |
| `fmt.py` | rounding and LaTeX for the answers |
| `runner.py` | **the verifier.** Solves every spec and compares with the book |
| `figlib.py`, `export_figs.py` | crop the figures out of `Other/NR12.pdf` |

## Two things that will bite

**The titles are a join key, and they are capped at 80 characters.**
`Documentation/tools/app_links.py` matches each problem to its `.cir` entry
*on the title* — the problem's title is the entry's title minus its
parenthetical, which is what its stage 4 claims. And `parse_book` in
`circuitbook.py` silently truncates an entry name at 80 characters. So a
title is not free prose: lengthen one past the cap, or reword it so the
problem and the entry disagree, and that example loses its **Open in app**
and **Open in split view** links with no error anywhere. After touching
`titles.py`, run

    py Documentation\tools\app_links.py

and check the coverage number has not fallen and that no `nr12-sampler`
line appears among the loose ends.

**Verify before you publish.** `runner.py` re-solves all 43 and compares
against the number the book prints:

    py -c "import sys; sys.path.insert(0, r'Documentation\tools\nr12'); import runner, specs; runner.check(specs.SPECS)"

Expect `43 ok, 0 bad`. That guards the *answers*; it does not guard the
app, which is a separate and stricter test — `repos/server/tools/verify_lesson.py
Nilsson_Riedel` posts every entry through the real app and is what caught
Example 9.15, which passed the solver API and failed the app outright.

## Editing the prose

**Roberto's seven rules, from his review of 12 Sep 2026** — every entry
follows them, and `gen.py` enforces the mechanical ones:

1. **No book title.** The book's example title names the book's method,
   which is not how the reader solves the problem. Neither the page nor
   the `.cir` note shows it.
2. **The paragraph above the run compares nothing with the book's method
   and states no result.** It says how *we* describe the circuit and what
   the settings mean.
3. **Only what the question asks is reported.** Trim `expect`; an answer
   the runner should still verify but the page shows another way goes in
   `hide`.
4. **Explain as to someone who does not know** — name the thing in the
   figure and what the question wants before saying how the description
   expresses it.
5. **What follows from an answer comes after it**: a range read off a
   formula, a value at an instant, a lettered part (`after`, `evals`,
   `parts`), never in the paragraph above the run.
6. **Nothing from thin air.** A value that is not in the problem statement
   is found on the page — an initial condition by a first DC run of the
   circuit before the switch moves (`pre`), a value at an instant by an
   Evaluate step (`evals`), a design value by arithmetic written in full.
   The sweep of 12 Sep 2026 found one invented value on the page, a 500 Ω
   galvanometer; it is a symbol now.
7. **Fact or choice.** What the statement, the diagram or circuit theory
   gives is stated as fact; every decision of ours — a name, a node, a
   symbol left open, the order of a source's nodes — is stated as a
   choice, in the first person plural the Course uses: *we name the
   galvanometer `rg`*, never *the galvanometer is a resistor named `rg`*.

The reader-facing fields of a spec:

- `ask` — the book's question, as the book words it. Also becomes the
  `.cir` entry's `note:`, with `$…$` maths unwrapped.
- `shows` — the paragraph above the run (rules 2, 4 and 7).
- `pre` — first runs, each `{text, desc, tag, expect, booknames, note}`,
  rendered before the main description as text, description, settings
  and answers, and written to the `.cir` as an entry of their own just
  before the main one (rule 6). The runner verifies each first run's
  `expect` as a spec of its own — *50 ok* is 43 examples and 7 first runs.
- `booknames` — answer name → the book's symbol, set beside the value:
  *`i_r7` = 2 A (the book's $i_o$)*, or under the result panels.
- `parts` — a lettered part answered in prose, after the results.
- `evals` — Evaluate steps after the results: the answer's name in the
  Evaluate box and the instant in Conditions, the way Lesson 6 does it;
  `gen.py` computes the value from the run and asserts it against
  `expect`, so an Evaluate step is verified too.
- `solveq` — Solve card runs, each `{tag, text, equations, unknowns,
  conditions, real_only, expect, unit, book, note}`, shown after the
  settings line with the card's three boxes and the button, and answered
  from the **real app**: `runner.app_values` runs `solve_ui` for the
  values the page holds and `runner.app_solveq` runs `solveq_ui` on them
  (the docs build imports the app tree, as `build.py --check` already
  does). The runner checks each run's `expect` too, so *ok* counts them.
  The first run's fields ride in the problem's head entry, as Roberto's
  own file had it (`solve_equations:` and kin); a later run is an entry of
  its own, linked beside its boxes, unless it says `entry=False`, in which
  case it shows only the boxes named in `boxes` and its own `press` line —
  "change the condition and press Solve equations again". Example 3.10 is the one that uses it,
  at Roberto's word (13 Sep 2026): the Solve card *"is more representative
  of the exploratory way a student would follow"* than Expert Mode.
- `after` — what follows from the answers, last of all.

`gen.py`'s `polish()` applies house typography to `ask`, `shows` and
`parts`: em dashes, Ω after a number, µ, ≥, the accent on Thévenin, and
`{{var:}}` around a bare variable like `R1`. **Every rule skips `code
spans` and `$maths$`** — since #429; before it only the variable rule did,
and the em-dash rule ran over the whole string afterwards, which turned
Example 5.3's `$v_o = -4v_a - v_b - 5v_c$` into dashes and nobody saw it
until the page was read. So: the book's own symbols go in `$…$` (`$i_o$`,
`$v_C(t)$`, `$0.2 + j0.5$` — bare, `j0.5` is read as a variable named `j`
with subscript 0), an app name goes in backticks, and **an arithmetic minus
in plain prose is U+2212 (−)**, because ` - ` still becomes an em dash
there. The bare word *ohms* stays a word (`in ohms`); only `10 ohm` becomes
`10 Ω`.

`cir_entry()` unwraps the maths for the `.cir` note — `$h_{11}$` becomes
`h_11` — so anything inside `$…$` in an `ask` must still read as plain text
without its dollars: no `\mathbf`, no `\geq`. Write `$t$ ≥ 0`, with the sign
outside.

**The numeric closing sentence carries no claim.** It reads *Symbulator
returns …* and stops; the statement that every value was compared with the
book is made once, in the chapter's *How to read an entry*, and an entry
whose answer needs a word about it — a sign convention, a rounding — says so
in its own `shows` paragraph. (It used to end *— the same answers the book
prints* forty-three times.)

Each section's intro opens with its count in words, and `gen.py` asserts
that word against the specs it introduces, so adding a DC example without
changing *Sixteen* fails the build rather than printing a stale number.

## Checking an `ask` against the book

`Other/NR12.pdf` is on this machine (not in the repo). Its text layer
scrambles the maths — `v = 24(2) = 48 V` comes out as `v 24 24 8V` — but
the **question prose is readable**, and `page` in each spec is the 1-based
PDF page. `fitz` (PyMuPDF) extracts it:

    import fitz; doc = fitz.open(r"...\Other\NR12.pdf"); print(doc[page - 1].get_text())

The #429 pass checked all 43 that way and found an `ask` that carried a
sentence the book never asks (7.13), one that had dropped the sentence that
explains its initial condition (7.5, make-before-break), and two whose
cross-references to earlier examples turned out to be the book's own words
(13.2, 13.3). Read the book before rewording.

## The figures

41 crops in `Documentation/assets/circuit/nr12-ex*.jpg`, taken by
clustering the vector ink above each `Figure N.M ▲` caption in
`Other/NR12.pdf` — a 26 MB file that is **not** in the repo, so
`export_figs.py` only runs on a machine that has it.

Four figures needed a hand-set top where the clustering swept in a formula
or a line of prose. If you re-export, note that `figlib.save()`'s `pad`
expands the box in **all** directions: pass `pad=0` and pad the rect
yourself, or the crop climbs back into the line above. And the first value
in the ink-top list *is* the top wire — cutting below it loses the rail and
its junction dots.
