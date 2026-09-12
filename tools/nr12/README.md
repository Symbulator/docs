# The Nilsson & Riedel sampler — its generator (#425)

**Two published files are output of this folder and must not be edited by
hand:**

| generated | from |
|---|---|
| `Documentation/src/98-nr12-sampler.md` | `specs.py` + `chapter_parts.py`, rendered by `gen.py` |
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
| `chapter_parts.py` | the chapter's own prose — front matter, opening, the four section intros |
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

Each spec carries three reader-facing fields:

- `ask` — the book's question, as the book words it. Also becomes the
  `.cir` entry's `note:`, with `$…$` maths unwrapped.
- `shows` — one paragraph on what the example demonstrates. This is the
  editorial voice of the page.
- `parts` — for a problem with lettered parts, one entry per part,
  answered separately (the four op-amp problems have these).

`gen.py`'s `polish()` applies house typography to `ask` and `shows`: em
dashes, Ω, µ, ≥, the accent on Thévenin, and `{{var:}}` around a bare
variable like `R1`. It skips `code spans` and `$maths$`, so a name that
must stay literal belongs in backticks. **Arithmetic minus signs must be
written as U+2212 (−)**, or `polish()` reads ` - ` as an em dash.

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
