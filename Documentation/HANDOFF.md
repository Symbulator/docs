# Handoff — the Symbulator 9 documentation, from here

Paste this whole file as the first message of a new session.

---

You are picking up work on the Symbulator documentation. Read
`C:\Users\perez\Claude Code\CLAUDE.md` first — it is the shared index across
both trees — then `C:\Users\perez\Claude Code\Sym Docum\Documentation\README.md`
(the build), `SPEC.md` (the markup) and `NEXT_DOCS.md` (the worklist).

**Your task is #81 in `NEXT_DOCS.md`, then the rest of the open items in that
file, in whatever order makes sense.** Everything below is context that is not
in those files, or that is worth having up front.

## Where things stand, 26 Aug 2026

Everything is committed, pushed and deployed. Nothing is half-done.

| Thing | State |
|---|---|
| `learn.symbulator.com` | deployed and verified, including all three PDFs |
| `install.symbulator.com`, `symbulator.com/9/local.zip` | deployed and verified |
| `symbulator.com` (landing) | untouched, needs nothing |
| PythonAnywhere | **Roberto reloads it himself** — ask, don't assume |
| `Symbulator/docs` | pushed, `631fe03` |
| `Symbulator/server`, `Symbulator/local` | pushed, `e6c15b2` / `385db30` |
| `Symbulator/solver` | clean, untouched, no PyPI publish pending |

## Rules Roberto has stated. Follow them exactly.

**Fine-tuning, not redesign.** *"At this stage of the design, we are
fine-tuning. If something seems to you as a design change, please do not run
with it. Seek clarification and confirmation."* The test: am I completing a
decision he already made, or making one for him?

**His numbers are authoritative.** Verify every value against the app, but if
the app disagrees with the page, **report it and wait**. Never write a
computed number over a documented one. Rounding to sensible significant
figures and adding units are fine and need no approval — the rule is about
replacing a value with a *different* value. A correction usually belongs to
the *problem*, not the version, so it propagates to 7 and 8 too.

**Names come from the app; values come from the page.** Version 9 prints its
own answer names and the older text never had them, so read names off a real
run.

**No underscores in displayed variables.** Write `ve1`, not `v_e1`. Version 9
accepts both. The exceptions are LaTeX, where the underscore *is* the
subscript, and one place that tells the reader underscores are allowed.

**Version 7 and 8 are not touched by version 9 feedback**, and their genuine
differences from each other must be preserved — they run different operating
systems and have different restrictions.

**Answers are read, not asked for.** In version 9 an answer is never fetched
with a bracketed array; it is read off the results, one named line each
(`irat = 6.809∠-21.8°`), and the prose says "we look in the results and see
that", not "we ask for". That is item #80.

**Conventions:** filenames use underscores and are ASCII; deploy instructions
carry full paths and full URLs; one shell command per block; `&&` does not work
in his PowerShell 5.1; items are numbered on a running sequence that never
restarts (`NEXT_DOCS.md` and `repos/local/NEXT.md` share it, currently at #88).

## The single most useful resource

`Sym Docum\Documentation\originals\` — `docs-page7.html` and
`docs-page8.html`, Roberto's original version 7 and 8 documentation, now kept
in the repo beside the sources. `originals/README.md` explains what they are
and what they have already settled. The master copy is under OneDrive; these
are byte-identical.

The whole of `src/` was converted from them, and the conversion introduced
most of the defects still open. **Check them before changing any answer.**
Read them; do not edit them.

`tools/check_against_originals.py` verifies printed answers against them
automatically — 59 of 83 confirmed verbatim, the residual understood and
written up as #85 and #86.

## What the conversion got wrong, so you know the shape of it

Four patterns, all of which have already bitten:

1. **Silent corrections with invented justifications.** Where the previous AI
   thought an answer was wrong it changed it and wrote a warning explaining the
   gap it had created, instead of raising it. Two were found and removed; if you
   meet a `::: warning` that argues about a printed answer, treat it as suspect.
2. **Version 9 read as the PyPI package, not the web app.** `eq.z`, `res["i_e"]`
   and friends named a local variable inside `symbulator_ui.py` that no reader
   can type. All removed, but the same mindset produced other prose.
3. **Merging versions 7 and 8 into one `out 7,8` block**, which silently drops
   every place the two pages legitimately differ. That is how a typo Roberto had
   already fixed in page 8 got reinstated.
4. **Calculator shorthand pasted into version 9 panels.** `.2v1` is implied
   multiplication the calculator understood and version 9 does not; the panel
   then cannot produce the answers printed beside it. That is #84, and every
   panel wants checking for it.

## Verifying your work

    cd "C:\Users\perez\Claude Code\Sym Docum\Documentation"
    python build.py --check                      # palette, banner, markup
    python tools/check_answer_parity.py          # v9 against v7/8 answers
    python tools/check_against_originals.py      # against the 2023 pages
    python tools/check_v9_panels.py              # all 311 panels still solve
    python tools/check_v9_timing.py

`check_answer_parity.py` currently reports **4**, all understood: RM3's 9-8 (a
documented sign difference), 11.75 (version 9 adds detail), 12.2 & 12.6 (an
abbreviation plus a version 9 tip), 12.10 (precision). Anything beyond those
four is something you introduced.

To run a circuit, drive the Flask app in-process rather than the package:

```python
import sys
sys.path.insert(0, r"C:\Users\perez\Claude Code\Symbulator\repos\server")
import app as flask_app
c = flask_app.app.test_client()
j = c.post("/api/solve", json={"desc": "e1,1,0,10\nr1,1,0,5", "domain": "dc",
                               "tool": "solve", "digits": 6, "si": False,
                               "units": False}).get_json()
```

Tools take `tool`: `solve`, `er`, `th`, `port` (with `kind` = z/y/h/g/a/b), and
`n1`/`n2` for the node pair. Mini-Tools is `/api/minitool` with `tool` `aa`,
`pf` or `gain`; `/api/evaluate` and `/api/solveq` take the `values` dict a solve
returns. Solves take 30–90 seconds — run them in the background, not foreground.

## Deploying, when the docs change

    cd "C:\Users\perez\Claude Code\Sym Docum\Documentation"
    python build.py

XeLaTeX is **not on PATH**; prepend
`C:\Users\perez\AppData\Local\Programs\MiKTeX\miktex\bin\x64` or the PDF step
dies with a bare `FileNotFoundError`.

Then, from `C:\Users\perez\Claude Code`:

    python deploy_symbulator.py learn --dry-run
    python deploy_symbulator.py learn

It authenticates by ssh key (no password), uploads only what changed, and
verifies over HTTPS afterwards. **Copy `learn_symbulator_com.zip` to a dated
name before rebuilding it** — it is untracked, so git will not save you.

If you ever touch the app rather than the docs, the release chain is
`build_local.py` → `build_zip.py --assets ../../local` → `stage_install_site.py`
→ `deploy_symbulator.py install` and `zip`, plus a `CACHE_VERSION` bump in
`repos/local/sw.js`. Skipping the middle two silently deploys a stale build
while every check passes.

## Two habits that caught real errors today

**Measure, then believe.** A build that prints success can produce nothing; a
script that reports "52 rewritten" can have skipped two thirds of the book
because a regex swallowed the wrong region; a staging step will happily re-stage
yesterday's build and call it done. Hash the artefact against its source and
compare counts against an independent estimate.

**Beware heredocs with backslashes.** Writing `**s\th**` through a shell
heredoc produced `**s<TAB>h**` in the source and would have shipped. Use the
Write/Edit tools for any content containing backslashes.
