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

## Working a feedback round

Roberto reviews the chapter in rounds, across sessions. The procedure --
batches, holding the build until his word, what each kind of change
costs, the gates, the X merge, the notes, the handover -- is written up
in `Notes/PROMPT_nr12_feedback_rounds.md` at the project root. Read it
before the first item. The rules below are the product of those rounds;
a correction that generalises becomes the next numbered rule here, in
his words, and is applied across the chapter.

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

**Eight more, derived on 13 Sep 2026 from the difference between the
original Example 3.10 and its revision**, and applied to all 43 the same
day; `gen.py` carries the mechanics (an Evaluate box for every `@`
answer, `evals` with conditions, `solveq` runs, several roots):

8. **Open with the thing, not the trick.** The first sentences say what
   the device or circuit in the figure is for and what the question
   wants, in words a student meeting the term for the first time can
   follow. The app is not mentioned until that is done.
9. **The problem's names where it gives them, ours declared.** `R_3`,
   `R_x`, `V_s` because the figure says so; `sg`, `a`, `b` because we
   chose them, and the sentence says so.
10. **The ordinary route before the expert one.** Run, read the results,
    then ask the Solve or Evaluate card; Expert Mode only where that
    cannot answer, and the page says why. No entry needs it now.
11. **Every value the reader sees is produced by a step the reader can
    perform.** No number, formula or range in prose without the boxes
    that produce it shown just above.
12. **Exactly what is typed, in the box it is typed into**, under the
    app's own label, spelled as the reader would spell it, and the button
    named.
13. **One answer per value asked.** A range, a set of cases, parts (a)
    and (b): each its own evaluation, never a formula read twice.
14. **One job per paragraph, in the session's order**: the thing; how we
    describe it; the run; what we ask the card; what it returns; the
    conclusion, last, in the problem's own terms and units.
15. **Two vocabularies, kept apart**: the book's words for the physical
    things, the app's exact labels for its controls, the app's answer
    names in code.

**Three more from Roberto's second read, 13 Sep 2026:**

16. **Say nothing the reader already knows from the entries before.** No
    "each between the two nodes it joins" or "with the bottom rail as
    ground" past the first entries that established it, and nothing the
    settings line under the description says again ("we set the analysis
    to DC", "we leave omega as a symbol").
17. **How to read the results comes after the run.** A sign convention, a
    note the solver will print, which answer is which: the `interpret`
    field, rendered after the settings line and before the results — not
    in the paragraph that describes the circuit.
18. **A single-letter name only when it is the only element of its type.**
    `e1` and `e2`, never `e` and `e2`; `e` alone is fine when it is the
    only source. And the figure is "the figure", never the book's
    `Fig. 4.42`, since the page does not use the book's numbering.

**Two more, 13 Sep 2026:**

19. **Rounding at n = 3 or 4, unless the book asks for more -- and two
    things are at play** (Roberto, 13 Sep 2026): what the reader is told
    and what the answer looks like. Every problem is told {{ui:Rounding}}
    *approx to n digits*, **n** = 4 (`DIGITS` in `gen.py`), and its values
    are printed at 4. Where the book prints more figures the spec says so
    with `digits=` (5.7, 8.4 and 11.1 at 5, 18.6 at 7) and the page prints
    that many -- *"show as many as the book; the reader will know why"* --
    but the reader is told *approx (full precision)* and the `.cir` says
    `rounding: approx`, never an n above 4, which "seems capricious and
    retroactively selected"; a student does not know the answer's
    figures before running it. `rounding_told()` in `gen.py` is the split.
    The settings line names the setting, the `.cir` entries carry it as
    `rounding:`, and every value on the page -- the panels, the returns
    sentence, Evaluate and Solve card outputs, the polar forms -- is
    printed at that n, so the page shows what the card shows. Under
    *approx* only an integer stays exact: 66600/709 reads 93.94 at 4.
20. **The Find equivalent card's answers by the card's names.** `req` in
    DC and `zeq` otherwise, never `z` (Roberto: "the card never reports
    the equivalent resistance as z"); typeset `R_{eq}`, `Z_{eq}`,
    `v_{th}`, `i_{no}`, `p_{max}`, labelled *equivalent resistance*,
    *equivalent impedance*, *Thevenin voltage*, *Norton current*,
    *maximum deliverable power* -- `symbulator_ui._TOOL_LABELS` and the
    template's `TEXNAME`, verbatim. The runner still keys the equivalent
    as `z`, `th()`'s own attribute; `fmt.tool_name()` does the mapping.
21. **A design is verified, not made.** Where the book says *Design a…*,
    the page's question reads *You have designed a…, as per the problem's
    specifications. Verify that…* — the reader types the book's finished
    values and the run checks them; the `shows` paragraph says *verify a
    design made for…* and the part's answer says the run *verifies* it
    (Roberto, 13 Sep 2026, on 5.3 and 5.5). A part that genuinely
    computes values, like 14.6's (d), is not a design instruction and
    keeps its wording.
22. **No "the book's" aside when the names agree.** `z11` = 10 Ω (the
    book's $z_{11}$) says the name twice; the aside is for `v_4` being the
    book's $v_o$, not for a typesetting difference. `gen.py`'s
    `same_name()` compares the two with underscores, braces and case
    stripped, at every site that writes the aside (Roberto, 13 Sep 2026,
    on 18.1).
23. **An intuition is stated as one, and the run verifies it.** Where the
    steady state before a switch can be read by inspection -- an inductor
    as a wire carrying the source's whole 20 A, a capacitor as an open
    sitting at the source's 100 V -- the paragraph says the deduction,
    the value it gives and *that should be the initial condition*, then
    *To verify this intuition, we can run a DC simulation* (Roberto's
    words, 13 Sep 2026, for 7.1; 7.3 and 7.5 follow). Without that
    framing the same sentence is correct but irrelevant, and a reader may
    think they must replace the element by a short themselves. Where the
    steady value needs a calculation (a divider, a coupled primary, two
    inductors in a loop) the aside is dropped and the run simply finds
    it: *the circuit has been steady for a long time*, and how a closed
    switch is written.
24. **No Rounding instruction where exact shows what the page shows.**
    7.1's panels read `20 e^{-5t}` while the card at *approx to 4* prints
    `20.0 e^{-5t}`; the reader was told a setting that does not produce
    what they see (Roberto, 13 Sep 2026). `gen.py`'s `is_exact()` runs the
    problem and every Evaluate and Solve step both ways; when nothing
    differs, the settings line says nothing about Rounding -- the app's
    default is *exact* -- and the entry says `rounding: exact`. A first
    run (`pre`) is classified on its own.
25. **A floating side's bottom is ground.** A transformer's or coupled
    coil's secondary with no path to the primary is written with its
    bottom on node 0 -- one connection between two otherwise separate
    networks carries no current, so nothing changes -- and the page says
    so in half a sentence, instead of a node of its own plus a paragraph
    about the island note the solver would print (Roberto, 13 Sep 2026,
    on 13.7; 9.15 the same).

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
- `digits` — the Rounding setting the problem runs at (rule 19); 4 unless
  the book prints more figures.

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
