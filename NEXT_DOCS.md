# Open items on the documentation

Numbered on the running sequence shared with
`Application/v9/repos/local/NEXT.md`, which stood at #77 when this file started.

## #456 — the Samplers, a book of their own with a PDF per textbook — **live 15 Sep 2026**

Roberto: *"the samplers should be their own thing. In the learn landing page,
they would be a fourth card: The Samplers. And they should not be part of the
PDF of the Course."* Then, on one PDF each or one combined: *"Separate PDFs
is good."* They had been pages 312–416 of the Course's 418, printed after the
credits.

- **The books.** Both sampler chapters carry `book: samplers` (written by
  each `chapter_head.md`, so regeneration keeps it). `build.py`'s Course PDF
  now takes `book == "course"` alone, and a new loop prints one PDF per
  sampler chapter, `symbulator-<chapter id>.pdf`, with the chapter's title as
  the subtitle, *Symbulator 9 Samplers* on the title page, and no index.
- **References across PDFs.** `TexRenderer.in_doc` holds the chapters the
  document prints; a `{{ref:}}` to one outside it reads *Name (in the
  Course)* instead of a `\pageref` that printed **page ??**. The samplers'
  heads point at *Working with input files* in the Course, and **the
  Manual's PDF had been printing six such ??** since it was first built,
  unnoticed. Measured over all six PDFs: none left.
- **learn.** `index.php` has a fourth shelf: `shelf_of` knows `samplers`,
  a fourth cover (*Working from a particular textbook?*, a teal
  `--ui-control` stripe, *2 textbooks*), the shelf page `/9/samplers`
  (bookless, like the Notes: no single PDF is right there), the property
  mark *Samplers*, and a sampler page's *Download as PDF* naming its own
  file. The covers go two by two (`minmax(24rem, 1fr)`), since three across
  left the fourth alone on a row. The addresses `/9/as7-sampler` and
  `/9/nr12-sampler` are unchanged, so the app links and the split view are
  too. `static_preview.py` mirrors the mark; `check_ribbon.py` gained the
  shelf page and a sampler page (12 of 12, locally and on the live host);
  `Deploy/deploy_targets.ini` verifies both sampler PDFs, the shelf page and
  the cover.
- AS7's head said *fifty* three times; the book has fifty-two since #454.

PDFs: the Course (v9) **313** pages, AS7's sampler **57**, NR12's **52**, the
Manual **46**, v7 **235** and v8 **223** unchanged. Deployed; v9 and both
sampler PDFs hashed live against the build; version 7's and 8's
`lesson-dc` byte-identical across the deploy.

## #455 — lettered questions and lettered answers, both samplers — **live 15 Sep 2026** (*"Punch it. Build everything."*)

Roberto on AS7's Example 19.17: he had read only its last request, *Find
the output voltage $V_o$*, and took the three Evaluate steps above it for
answers to questions nobody asked. His fix: one letter per question, and
the answers say which letter they answer; then *"make a rule out of this
and apply to the rest of the problems."* It is rule 31 in
`tools/nr12/README.md`, with its boundary: several requests, or one
request for things of different kinds, are lettered; a list of values of
one kind is one question.

`sampler/gen.py` gained a spec field `letters` (answer → part), which puts
the bold letter into the returns sentence, into a sentence under result
panels and into an automatic Evaluate step, and `check_letters`, which
fails generation when a lettered ask has a part the page never labels.

AS7, 17 entries: 19.17a/b lettered (a)–(e), with (e) $V_o$ read off the
run last and (d) pointing at 19.17b; letters added to 2.15, 4.12, 4.13,
5.1, P6.10, 7.13 (both intervals), 14.10, P14.10, 14.2, 19.9; the
answers labelled in 16.6 and P16.6, whose asks already had letters.
11.14 and 16.9 already complied. NR12, 14 entries: 3.11 lettered a) and
b), its power moved after the current so the parts read in order; the
answers labelled in 4.13, 4.21, 7.1, 7.3, 7.5, 7.11a/b, 7.13, 8.11, 9.9
(its c) and d) now after b)), 10.8, 10.12, 13.9 and 14.6, several of
which said *Part (b) asks…*. Only the asks moved in the two `.cir`
books, as notes. **Shipped with a full build, the PDFs included at his word**: v9 **418** pages, the Manual **46**, v7 **235** and v8 **223** unchanged; `check: clean`, card truth 15 and 36 panels with none disagreeing; `learn` deployed and verified, v9's PDF hashed live against the build and version 7's and 8's `lesson-dc` word-for-word unchanged. The offline pair at cache **v231** (ZIP 32,044,268 b), the staging copy proved the ZIP's build and the live `sw.js` and both books hashed against it. X47 pushed. Both PythonAnywhere accounts want their pulls.

## #454 — AS7's Example 10.6 and Practice Problem 10.6: superposition across frequencies — **live 15 Sep 2026**

Roberto asked to see 10.6, parked in #449, and then: *"Punch it. Add both
problems if you can."* Both circuits run at several frequencies at once, and
a DC or AC run works at one, so each is answered with one run per source and
the other sources set to zero -- a voltage source at zero is a short, a
current source at zero an open, which is superposition itself. 10.6 takes
three runs (DC with the 5 V source alone, AC at 2 rad/s, AC at 5 rad/s) and
Practice Problem 10.6 two (AC at 5 and at 10 rad/s); a sine source is its
cosine phasor, `(2∠-90°)` and `(75∠-90°)`. The time-domain sum is stated
after the runs, as in NR12's 9.9. **Both books slip, and the entries say
so**: 10.6's third term is 2.328∠−77.91°, where the book prints −80°, so it
reads 2.328 sin(5t + 12.09°) and not sin(5t + 10°), and its −30.79° rounds
the other way (−30.78°); P10.6's second amplitude is 3.151, where the book
prints 3.154.

The generator learned three things for them, none of which moves an existing
entry (the NR12 chapter and book regenerate unchanged): a first run may be AC
at its own `omega` (and `rms`), carried to the settings line, the runner and
the `.cir` entry; a spec may name its main run's `tag` (*AC at 5 rad/s*)
rather than the analysis alone; and `cir_note` overrides the main entry's
note, hard-coded until now to *the circuit after the switch has moved*.
The AS7 book is 52 problems (AC 17), 57 app entries; runner 62 ok, card
guard 0 disagreeing, `verify_lesson Alexander_Sadiku` 0 with a problem,
`app_links` 442 of 444, `build.py --check` clean. Figures cropped by
`figrect` and checked on a sheet.

## #453 — claimed by the app tree, 15 Sep 2026: **a riser no longer climbs through a lifted body** (solver 0.6.14). Only AS7's Example 10.4's drawing moves; the monograph's Appendix B does not. Write-up in `Application/v9/repos/local/NEXT.md`.

## #452 — Roberto's first review round of the AS7 sampler — **live 15 Sep 2026** (the hold lifted by *"Punch it"*)

Held at his word (*"Don't rebuild the lesson until told"*). 2.15 reads $R_{ab}$ off the source's card as `r_e` instead of an Evaluate step. 3.7 reads each mesh current off the one element its mesh alone contains, written along the book's clockwise arrow (`r6,0,p,6` turned for it), with the By-Hand step gone. Figures re-cropped: 3.11 (the whole circuit), 4.12 (the line above it), 4.13 (its base), P19.9 (the matrix above it), 19.12 (its `Vs` label). **Rule 19 restored in the generator**: under *approx (full precision)* the page prints the book's figures, not the card's every digit -- `shown_digits()` in `tools/sampler/gen.py`, where rule 29's card rendering had been passing zero digits -- so 5.1 prints −1.9999698 and 0.00019999799 A, with a note on the book's own last digits. Both chapter summaries end at *prints.*, the credits sit above the two samplers, and the landing page has its *Against the textbook* section (those three are live). Mesh directions became #451.

## #451 — claimed by the app tree, 15 Sep 2026: **mesh currents clockwise by default, and a flip** (solver 0.6.14). The docs moved with it: Lesson 1's By-Hand paragraph and the Manual's toolbox. Write-up in `Application/v9/repos/local/NEXT.md`.

## #450 — claimed by the app tree, 14 Sep 2026: **a short named `s`, `limit()` in Evaluate, and `r20b`** (solver 0.6.13). The docs moved with it: Lesson 4's HK5 Figure 2-29 written with `s` and `is` as the book writes it, the Manual's answers page and a *Limits* section on its frequency page, and the AS7 sampler's 7.5 back to `s` and its four limits read with `limit()`. Write-up in `Application/v9/repos/local/NEXT.md`.

## #449 — Examples from Alexander & Sadiku 7e: a second sampler — **live on learn 14 Sep 2026, cache v229**

Roberto: *"select around fifty to sixty problems, like you did for NR12,
and ... create a similar lesson ... The more difficult the problem and the
more comprehensive is Symbulator's solution, the better."* Fifty problems
from *Fundamentals of Electric Circuits*, 7th edition, at
`src/97-as7-sampler.md`, generated from `tools/as7/specs.py` by the
sampler code that now lives in `tools/sampler` and serves both books.
**None of the fifty repeats a problem the Course's lessons already take
from this book** (checked against all 62 `AS7's` entry titles in the
lesson books). DC 21, TR 8, AC 15, FD 6.

What the fifty show, beyond the NR12 sampler's range: the
**By-Hand Equations** card naming mesh currents (Example 3.7, all four
the opposite of the book's, which the entry says); the **Resistance /
impedance** tool on a circuit with no independent source (4.10, −4 Ω);
the **pf** mini-tool (11.14) and **pz** with a double pole (14.2, `-1 ×2`);
a closed switch as an `s` element (7.5); coupled coils in ohms (P13.2)
and by *k* (P13.13); an ideal transformer with opposite dots sharing a
node (13.14); two filters whose corner frequency is found in the Solve
card from `abs(v_2/vi)=1/sqrt(2)` (14.10, P14.10); the initial- and
final-value theorems as `s=oo` and `s=0` in Evaluate's Conditions box
(16.6); impulse, step and sinusoidal responses from one transfer function
with `s2t` (16.9); and five two-ports as elements -- transmission
parameters under the Thévenin tool (19.9, P19.9), a z-block with
bracketed four-terminal ports in series with a resistor (19.12), and a
transistor as an `h` element (19.17, split in two for its output
impedance).

Gates: runner **58 ok, 0 bad**; card guard **0 disagreeing**; all 50
entries through the real app with `verify_lesson.py Alexander_Sadiku`,
**0 with a problem**; `app_links` **437 of 439**, no loose end from the
new chapter; `build.py --check` clean; the built page served by local PHP
with 50 problems, 50 figures, no broken image, no KaTeX error. The NR12
chapter and its book regenerate byte-identical after every shared change.

**Things this round learned, worth keeping.** (The first two below were fixed the
same evening as #450: `s` is accepted and Evaluate takes `limit()`. `r20b` parses too.)

* **The real app refuses an element named `s`** (its current would be
  `is`, a keyword) where the solver API accepts it. `verify_lesson.py`
  caught it on 7.5 after the runner had passed it: *the solver's API is
  not the app*, again. The short is `s1`.
* **Evaluate has no `limit`.** `s=oo` in the Conditions box works when
  the expression cancels first (16.6) and prints NaN when it does not
  (P16.6, where the entry says so and reads $v_o(0)$ from $v_o(t)$).
* **The By-Hand card's answers arrive exact** and the page rounds them
  as it typesets (#359), so the runner now applies the app's own
  `_round_expr` to a By-Hand reading, and the rule-29 exactness test
  counts By-Hand answers. 3.7 prints −3.929, as the book does.
* **The book's figures defeat the crop detector** on this layout (a
  margin column, banners drawn as images, stacked (a)/(b) parts): 32 of
  the 50 specs carry an explicit `figrect` in PDF points, read off a
  gridded render, and `export_figs.py` honours it.
* The pf and aa mini-tools reply with one `plain` value, not `rows`; the
  minitool step reads that as the row `value`.

Two printed answers the circuits do not reproduce, and the entries say
so: P10.13's amplitude (536.4 mV from the book's PSpice run, 536.55 by
the circuit) and 19.17's $V_o$ (−105.09 mV printed, −105.02 from the
book's own gain times the input). Dropped from the selection: E8.6 and
E8.8, whose overdamped answers the app writes as $e^{-at}(A\cosh bt +
B\sinh bt)$ -- equal to the book's two exponentials, but unreadable
against them; E8.9 (its printed initial condition contradicts its
circuit); P4.13 (a unit misprint); E10.6 (superposition across three
frequencies, three runs the generator cannot yet group).

**Shipped 14 Sep 2026 with #450** at Roberto's word: `learn` web only, the PDFs held, and the example book on install and the ZIP at cache v229. The PythonAnywhere accounts take it at their pull, after solver 0.6.13 reaches PyPI.

## #448 — DC, AC, TR and FD in capitals in version 9 — **live 14 Sep 2026**

Roberto: *"in the v9 documentation, find instances of fd like this ...
and please capitalise them ... Whereas the lower case is appropriate for
v7 and v8, it is not for v9."* Every built version 9 page was scanned for
the four names as words outside code, maths and file syntax (`analysis:
dc` in an input file stays lowercase), and four turned up: Lesson 7's
*use the ac analysis* and Lesson 12's summary *using fd*, both shared
prose now split by version spans, the limiting-results note's **tr** and
the equivalent-circuit note's *dc simulation*. A rescan finds none, and
every version 7 and 8 page is byte-identical across the rebuild.

## #447 — Lesson 10 works a coupling given as k: NR9's Assessment Problem 9.14 — **live 14 Sep 2026, cache v228**

Roberto asked for an example of `m,l1,l2,k=...` in the Course, keeping
NR12's Example 9.15 in the sampler. The 12th edition gives *k* as data in
one other circuit, Problem 18.36, which prints no answer. It went live
at cache v227 checked three ways (Symbulator with `k=`, with *M* = 26 mH,
and a mesh solve by hand). Roberto then pointed at the 9th edition for a
**solved** one, and its **Assessment Problem 9.14** replaced 18.36 within
the hour: *k* = 0.4 at 800 rad/s, and all three printed answers match the
real app -- the primary current `ir1` = 0.5∠−53.13° A, the secondary
`ir2` = 0.08∠0° A, and the reflected impedance `ze − (184 + 100 + 400j)`
= 10.24 − j7.68 Ω in Evaluate. Version 9 only, at the end of *Instructive
m problems*, with the lesson's *k* sentence pointing at it; a figure drawn
by Symbulator through the monograph's own pipeline
(`paper/render_exemplars.py`'s fonts and flattening), `sym_nr9_ap0914.png`,
and an entry in `Lesson_10.cir`. Versions 7 and 8 byte-identical.
**`assets/circuit/sym_nr12_p1836.png` lingers on the host** from the v227
deploy and is no longer referenced -- Roberto's typed prune.

## #445 — claimed by the app tree, 14 Sep 2026: **the `pz` mini-tool, poles and zeros**. The docs moved with it: 13.9's part (b) reads the poles and the zero off `pz` instead of two Solve card runs on polynomials copied out by hand, Lesson 7's Mini-Tools card lists four tools, and the Manual's orientation, frequency page and reference table name it. Write-up in `Application/v9/repos/local/NEXT.md`.

## #444 — 13.2 and 13.3 answer the question they ask, a function of time — **live 14 Sep 2026, cache v226**

Roberto: *"If the question asks for a voltage as a function of time, why
use FD? Unless the question asks for both functions, of s and t. Also,
the claim that FD returns also the answer in the time domain is
nonsense. You need s2t for that."* Both questions ask for $v(t)$; both
entries stopped at the transform and waved at TR (*"FD returns the
transform and TR its inverse"*, *"Choosing TR instead would return its
inverse"*). They keep the FD run, since the book works them by the
Laplace method and prints the transform, and add the inversion as a step
of its own: `s2t(v_2)` and `s2t(v_1)` in Evaluate, shown as result
panels. The answers are the book's, 60e^−25t and (50 − 2.2×10⁶t)e^−40000t,
checked by `gen.py` against `expect`. The FD section's intro now says
which two of its five invert and how. `gen.py` learned to show an
Evaluate step whose answer is an expression (`label`, `texname`), which
it could not before: `runner.number_of` reads a leading number and took
`(50.0` out of the second answer. **Rule 30** in `tools/nr12/README.md`.

## #443 — the page prints what the card prints — **live 14 Sep 2026, cache v226**

Roberto, on 13.6: *"says it uses approx but the answers it shows are
exact. I had already reported a similar problem. Fix here and
elsewhere."* **Measured, it was all 34 symbolic answers in the chapter,
across 21 entries.** `gen.py` rounded a symbolic answer through its own
`fmt.tex_value`, so the page printed `60` where the card prints `60.0`,
`10000` where it prints `1.0 \cdot 10^{4}`, and every transient's terms
in a different order. A panel now carries the card's own LaTeX
(`runner.app_display`; an `@` answer, `runner.app_evaluate_display`).

**The Rounding instruction was decided wrongly too, and took two
attempts to decide rightly.** An entry is now told *exact* when every
answer it shows reads the same at exact and at n = 4 with the numbers
written one way (`gen._same_but_for_notation`). The first attempt asked
instead whether exact held a number too long to read, and 14.6's Solve
card came back `L = 1 H`: exact's answer there is `1/(500*pi**2)`, which
holds no long number and is still not the 202.6 µH the book prints, and
`number_of` read its leading `1`. A Solve card line now refuses to print
an expression as its leading number. Thirty-one entries of fifty are
*exact* now; 7.11b, 8.4, 8.11, 13.7, 14.6 and the AC entries keep n.
Guard: `tools/nr12/check_card_truth.py` reads the BUILT chapter, asks the
app, and is proved red by `--prove-red`. **Rule 29.**

## #442 — Roberto's review round of 14 Sep 2026 — **live 14 Sep 2026, caches v225 and v226**

- **10.8** reads parts (a) and (b) as `p` and `q` off the cards and (c)
  as two sums in Evaluate, now that every AC card shows both powers.
  `gen.py` gained `groups`, one results sentence per lettered part.
- **Rules 26 and 27**, voice: every sentence has a verb, no semicolon
  joins two clauses. His rewrite of 10.12 is the model. 77 semicolons in
  44 prose fields and a verbless opener on most entries, all rewritten;
  *We set the analysis to TR* restored where it had been cut, the
  analysis not being a setting.
- **10.12** writes the transformer his way, both pairs top node then
  bottom, `t,[p,x],[a,x],[-4,1]`, with the reversed-pair form as the
  alternative.
- **11.1** gives its sources as phasors in degrees, `(120∠-120°)`
  (**rule 28**; the Manual's three-phase paragraph moved the same way),
  and answers each part under its letter, (b) to (f) and (g) in words.
- **9.15** checked against the book at his ask: the values match; the
  live PDF is a day behind, the PDFs being held.

## #441 — claimed by the app tree, 13 Sep 2026: **the AC powers are `s`, `ap` and `q`, no `p`; *effective* under RMS** (solver 0.6.11, withdrawing #439's both-names). The docs moved with it: the Manual's AC table with three power rows and the RMS warning saying the labels turn *effective*, its answers table with `qr1`, Lesson 8's version 9 reading `ape`, the sampler's 10.16 reading `apmax`. Write-up in `Application/v9/repos/local/NEXT.md`

## #440 — the split view opens a named book's chapter — **13 Sep 2026**

Roberto: *"the link to open these problems in split view is not opening
the documentation side of the window in the right page. I'm getting
Lesson 1 instead of the NR chapter."* The shell's `normalise()` took a
lesson as a number and a letter, `^0?(\d{1,2})([a-d]?)$`, so `nr12` --
the sampler's book name since #425 -- came back as no lesson at all and
the docs pane stayed on its default. It accepts a lowercase name now,
and `lessons.json` already mapped `nr12` to `nr12-sampler`. Web only,
one function in `web/split/index.php`.

## #439 — claimed by the app tree, 13 Sep 2026: **in AC the real power answers to `p` and `ap` alike**, and Evaluate's `re()`/`im()` said out loud. The Manual's AC table has one power row again, its answers chapter names the functions, Lesson 8 (version 9) says the reactive power is `im(se)`. Write-up in `Application/v9/repos/local/NEXT.md`

## #438 — claimed by the app tree, 13 Sep 2026: **the `m` line checked, and `k=` accepted** (solver 0.6.10). The docs moved with it: the Manual's coupling chapter gains the `k=` form and the checks, its grammar and reference tables the spelling, Lesson 10's *Don't mix the two* warning says the mixed form is refused now (version 9 only; 7 and 8 keep the old sentence), and the sampler's 9.15 reads `m,l1,l2,k=0.5`. Write-up in `Application/v9/repos/local/NEXT.md`

## #436 — the sampler at the book's rounding, and the Find equivalent card's own names — **live 13 Sep 2026; the last round at cache v222**

**The evening's batch (rules 19 as split, 23, 24; cache v222).** Roberto,
one item at a time and then *"Run the train"*:

- **Rule 19 split in two.** *"There are two things at play: what we tell
  the user (who is going to ask himself how we knew what to tell him)
  and what the answer looks like."* An n of 5 or 7 *"seems capricious
  and retroactively selected"*, so the four problems whose book answers
  carry more figures (5.7, 8.4, 11.1, 18.6) are told *approx (full
  precision)* and their entries say `rounding: approx`, while the page
  prints as many figures as the book -- *"the reader will know why"*.
  `rounding_told()` in `gen.py` is the split.
- **Rule 24.** 7.1's panels read `20 e^{-5t}` while *approx to 4* prints
  `20.0 e^{-5t}`. `is_exact()` runs every problem and its Evaluate and
  Solve steps both ways; where nothing differs the settings line says
  nothing about Rounding and the entry says `rounding: exact` -- ten
  problems and six first runs, each first run classified on its own.
- **Rule 23.** *"In a steady circuit an inductor ... behaves as a wire"*
  was first dropped as correct but irrelevant -- a reader may think they
  must replace the inductor by a short -- and then, on his second look,
  kept where it reads the initial condition by inspection and reframed
  in his words: *The full current of the source, 20 A, would run through
  it, and should be the initial condition of the inductor. To verify this
  intuition, we can run a DC simulation.* 7.1, 7.3 and 7.5 carry that
  shape; the four first runs whose steady value needs a calculation keep
  only *the circuit has been steady for a long time*.
- The docs' three mentions of where the *limit the results* tick is now
  say *in Settings* (#437, app tree).

Gates: runner 63 ok, `app_links` 384 of 386, `build.py --check` clean,
`verify_lesson.py Nilsson_Riedel` clean on all 50. `learn` deployed web
only; the book's `rounding:` lines changed, so the offline pair went to
cache v222 and both PythonAnywhere accounts want a pull.

Roberto, 13 Sep 2026: *"unless the book asks for more precision, use
rounding at n=3 or 4 for every problem"* — and, reading Example 4.21,
*"the card never reports the equivalent resistance as z. Even in AC, it
is reported as zeq. But in DC, it is req."* Rules 19 and 20 in
`tools/nr12/README.md`.

**Rounding.** Every entry ran at 6, and the page said nothing about it.
Now `gen.py` carries `DIGITS = 4`, a spec may say `digits=`, and the
setting is threaded through everything that prints a value: the
settings line ends *Set Rounding in Settings to approx to n digits with
n = 4*, the `.cir` entries carry `rounding: 4`, the panels and the
returns sentence round at n, the Evaluate and Solve card runs go
through the real app at n, and the polar forms too. Four problems
print more because the book does — 5.7 (5.9988), 8.4 (979.80) and 11.1
(115.22) at 5, 18.6 (33,333.33) at 7. Two formatter faults surfaced on
the way and are fixed in `fmt.py`: a value rounded to n came back as a
Float with n digits of *binary* precision, so every later read printed
its noise (2.66699 for 2.667, and a 1.6e9 coefficient in 13.9's
transfer function as 1599995904) — it is read back through its decimal
string now, as the app does since #391; and a non-integer Rational with
a small denominator was kept exact and printed at six figures whatever
n said (9.15's `66600/709` read 93.9351 under n = 4; it reads 93.94).
Under *approx* only an integer stays exact, which is what the card does.

**The card's names.** The page called the equivalent `z`, typeset it
`Z_{Th}` and labelled it *Thevenin impedance*; the card says `req` in DC
and `zeq` otherwise, `R_{eq}` / `Z_{eq}`, *equivalent resistance* /
*equivalent impedance*, and `v_{th}`, `i_{no}`, *maximum deliverable
power* for the rest — `_TOOL_LABELS` and the template's `TEXNAME`,
which `fmt.py` now copies. The runner keeps `z` as its key, `th()`'s
own attribute; `fmt.tool_name()` maps it. Five problems moved (4.21,
9.12, 9.15, 10.16, 13.6) and the two maximum-power paragraphs now say
`req` and `zeq`.

Gates: runner **63 ok**, `app_links` 384 of 386, `build.py --check`
clean, `verify_lesson.py Nilsson_Riedel` clean on all 50. The app's
book changed only in its `rounding:` lines, so it rides the v218 train.

**The late-evening items, same day (cache v223, solver 0.6.10):** rule 25,
a floating side's bottom is ground (13.7 and 9.15); 9.12's terminal is
the figure's **a**, not a 9 picked to stay clear of 1–3; 9.14's nodes
are letters, V₁, V₂ and V₃ being the book's names, and then Roberto's
simpler description with each series pair as one impedance, so `v_r1`,
`v_r2`, `v_r3` are the answers and 10.8 reads `s_r1`, `s_r2`, `s_r3`
with the balance one Evaluate step; 9.9's part (a) and 9.15's (a)–(f)
named as the book's own method and skipped; 9.15's coils in henries
with the book's *k* on the `m` line, `m,l1,l2,k=0.5` (#438), and no
figure, the book printing only the equivalent in ohms and the words
being enough (`nofig` on the spec).

**Example 5.3, an hour later (cache v219).** Roberto: part (a) should
not ask the reader to design what the page then verifies — it reads
*"a) You have designed a summing amplifier, as per the problem's
specifications. Verify that its output voltage is …"*, the description
paragraph says *verify a design made for the gains given*, and the
part (a) answer *verifies the three resistor values*. The `.cir` note
carries the same words, so it took a second app train.

**And a rule, an hour later (cache v221).** Roberto: 5.5 needs the same
fix, and it is a rule for the chapter — **rule 21** in the nr12 README,
*a design is verified, not made*: where the book says *Design a…* the
page reads *You have designed a…, as per the problem's specifications.
Verify that…*, since the reader types the book's finished values and
the run checks them. 5.3 and 5.5 are the two; 14.6's part (d) genuinely
computes `R` and `L` in the Solve card and keeps its wording.

**Rule 22, from 18.1 (web only, no `.cir` change).** Roberto: *"When
both Symbulator and the book use the same variable name for an answer,
there is no need to reiterate the name of the variable given by the
book"* — `z11` = 10 Ω *(the book's $z_{11}$)* said it twice. `gen.py`'s
`same_name()` compares the app's name and the book's symbol with
underscores, braces and case stripped, and every site that writes the
aside skips it when they agree: twenty sentences lost theirs (the Solve
card's `vb`, `rf`, `t`, `R_x`, `L`, `R`; the two-port's four; `vth` and
`pmax`), while `req` beside $R_L$, `zeq` beside $Z_{Th}$ and `v_4` beside
$v_o$ keep it, those being different names.

## #434 and #435 — claimed by the app tree, 13 Sep 2026: **a source's card reads the power it delivers** (`-pe1 = 10 W`, labelled *power delivered*; in AC the average power delivered and the delivered power's **power factor** as a row) and ***real solutions only* ticked by default in DC and TR**. The docs moved with #434: the Manual's *Signs* paragraph, Lesson 2's *power delivered* line, Lesson 3's Drill Problem 1.11 panels, and the sampler's 3.11 and 4.13, which read the card instead of Evaluate with a minus sign. **The sampler's questions also lost the book's method** the same day (*"Use the node-voltage method to find…"* is *"Find…"*, in fourteen entries; the chapter opening says once that the book prescribes one), at Roberto's word. Write-ups in `Application/v9/repos/local/NEXT.md`

## #433 — claimed by the app tree, 12 Sep 2026: **the Solve card's conditions and equations behave like Expert Mode's** — an equality condition on a symbol substitutes, and an equation that names none of the unknowns is solved rather than dropped; found by Roberto solving NR12's Example 3.10 with the Solve card. Nothing in the docs tree changes for it. Write-up in `Application/v9/repos/local/NEXT.md`

## #431 — no underscores in the interface's example variables (app side) — **live 13 Sep 2026; the write-up is in `Application/v9/repos/local/NEXT.md`**. Nothing in the docs tree changed; the sampler's own `i_l1` spellings are prose about the package's names and were left as they are.

## #432 — Roberto's Course review round of 13 Sep 2026 — **live 13 Sep 2026, web only**

Seven wording fixes from Roberto reading Lessons 7 and 8 on the web after #430, each applied to the version 9 pages alone by `{{v7,8|…}}{{v9|…}}` spans or inside an existing `::: only 9` block, so versions 7 and 8 stay as written -- captured before the deploy and proved unmoved after, six pages.

  * Lesson 7: *That is 3.22 − j11.07 Ω, which is correct* and its 0.25 − j0.025 S twin are just *This is correct* -- the value is shown above; *a convenience only* is *for convenience*; *carries surds through every step* is *carries unresolved square roots through every step* (Roberto: *what is surds?* -- the old textbook word for a root left as a radical, which is exactly the kind of word the seven rules forbid); the ten-second solve says *and about twice that on a phone*.
  * Lesson 8: the RMS setting's one-line explanation (*Off means peak amplitude, the convention with the divide-by-two*) is now two short paragraphs with the two formulas as display maths -- peak values carry the factor of one half, RMS values do not, only the power answers depend on the tick, and the same numbers typed in report twice the power with the tick on. *The complex power absorbed in the source, line and load are in `-se`* was wrong: `-se` is the power *delivered*; the sentence now says so and keeps *absorbed* for the line and the load. *The average power supplied is the opposite of the power the source consumes, `pe`: 2007.1 W* implied `pe` was positive; it now reads *`pe` reads −2007.1 W, so the source supplies 2007.1 W*, on the model of the sentence Roberto liked (*the opposite of `se` gives*). And *always in view, so it cannot be left set from a problem you finished an hour ago* claimed more than being in view can deliver; it is now *so it is easier for you to notice whether it is on or off*.

**A sanity sweep at Roberto's ask, over every sentence that reads a sign off `se`, `pe` or `ape`** -- the Course's AC lessons, the Manual, the sampler and the example books' notes: every *delivered* or *supplied* power is the opposite of the variable, every unnegated variable is called consumed or absorbed, and Lesson 9's three-phase page reasons it out in words. Nothing further to fix; the two sentences above were the confusions.

**Web only, at Roberto's word** (*except the PDFs*): `build.py --web` and a `learn` deploy. The PDFs live on `learn` are this morning's #430 build and now lag these seven fixes and the two RMS formulas; the next full `python build.py` clears that.

## #430 — the pf tool as version 8 has it: one value, a power or a name (docs half) — **live, 13 Sep 2026**

**Deployed in full at Roberto's word, 13 Sep 2026** — a full `python
build.py`, the documented exception to `--web`, since the lesson's typeset
text changed. v9 **354** pages (353 before), v7 **235**, v8 **223**, the
Manual **40**, all served at the local byte counts; the build printed no
*NO PDF PRODUCED*. Six version 7 and 8 pages were captured before the
deploy and diffed after, normalised for whitespace and the stylesheet's
cache-bust: **unmoved**, and no version 9 wording leaked into them. After
Roberto's review rounds (in the app half) the value form's paragraph says
`se` reads *0.97342 lagging* with no line under it, and the paragraph
*the same number, the opposite word* explains why that is not a
contradiction; the Manual says a name's reading carries the words and a
value's does not.


The app half -- what the tool now does and why -- is #430 in
`Application/v9/repos/local/NEXT.md`. This is what the books say about it.

**The rule the pages now state, in Roberto's words of 13 Sep 2026.** When
the *variable* of the power is given -- `se`, `sj`, `sr` -- the
calculation is done on the complex power *consumed*, regardless of
whether the element is a source or an impedance, and the answer is the
value alone. When the *name* of the element is given, a source (`e`, `j`)
is read on the power it **delivers** and an impedance (`r`) on the power
it **consumes**, and that is what decides leading or lagging. *This is
crucial and should be in the documentation.* It is now in three places,
each in its own register.

  * **`08-lesson-power.md`, *The pf mini-tool*, version 9 pages only.**
    Rewritten around the two forms, each with its one `Value` field box
    (`se`, then `e`), the reading each gives, and the line the tool prints
    under it. The *Mind the sign for a source* warning box is gone -- it
    documented the workaround the old port needed -- and in its place a
    `::: note` box, *Which power the reading is taken on*, carries the
    rule above with the reasons: why a variable cannot say the word, why
    a name can, and that the value is the same either way. The
    version 7 and 8 text is untouched.
  * **Practice Problem 11.10 and Problem 11.75 (b)**: the version 9 answer
    gives *pf* the source's name instead of `ve` and `-ie`. 11.75 (c)
    gains one sentence: *pf* given `se` now answers with an expression in
    `x`, which is what the calculator solved for 1, and the {{card:Solve}}
    card's `im(se) = 0` is the same condition.
  * **`07-lesson-ac.md`**, the Mini-Tools card list: *pf* takes one value,
    a complex power for the factor alone or a name for the factor and the
    word.
  * **`28-manual-ac.md`**: the one-line description becomes two
    paragraphs -- what each form takes and returns, then the rule, ending
    with the three lines the tool prints. **`33-manual-reference.md`**:
    the table row reads *a complex power, or an element's name* ->
    *power factor; with lead/lag for a name*.
  * **`examples/Lesson_08.cir`** (the app tree): the three notes that said
    *pf with ve and -ie* now say *pf given the source's name, e*, and
    Example 11.10's says why.

**Checked.** `build.py --check` clean; `app_links.py` 384 of 386 as
before (no entry was renamed); `build.py --web` run and
`?v=9&p=lesson-power` read back through the local PHP server -- the
section, the note box (`callout note`), the two problems and the
11.75 (c) sentence all render as written, and nothing of it appears
under `?v=7` or `?v=8` because every change is inside `::: only 9` or a
`{{v9|...}}` span, bar the Lesson 8 heading's existing version span.

**Not deployed, and the PDFs are affected.** The lesson's typeset text
changed, so this is the documented exception to `--web`: when Roberto
says go it is a full `python build.py` and a `learn` deploy, and the
version 7 and 8 pages should be captured before and diffed after as
usual.

## #429 — the Nilsson & Riedel sampler, made to read well — **live 12 Sep 2026** (learn, PDFs and the offline pair at cache v206; the server awaits its pull)

**Deployed in full at Roberto's word, 12 Sep 2026, after the review round
below.** `learn` carries the chapter and the four rebuilt PDFs — v9
**353** pages (347 before; the six are the first runs), v7 **235**, v8
**223** and the Manual **39**, all served at the local byte counts, the
six captured version 7 and 8 pages byte-identical across the deploy. The
offline pair is at cache **v206** with the ZIP at **32,004,118 b**; the
install host serves the 50-entry book and `sw.js` at v206, checked by
fetching. **Both PythonAnywhere accounts took their pulls the same
evening** (version 9 on build `2026-09-12 10:24 UTC`, X on `10:27 UTC`),
each verified by fetching its `/api/examples?file=Nilsson_Riedel.cir`:
the first runs and `rg,a,b,rg` are served by both. The chapter was then
retitled *Examples from Nilsson & Riedel 12e* (web only; the PDFs keep
the old title until the next full build, at Roberto's word), and the
app's book keeps its own title, *Problems from Nilsson & Riedel 12ed*,
in the picker — a one-line change in `gen.py`'s `main()` when wanted.

A readability pass over `/9/nr12-sampler`, prose only: every circuit,
setting and expected answer is untouched, and `runner.check` still reads
**43 ok, 0 bad**. The edits are in `tools/nr12/specs.py` (`ask`, `shows`,
`parts`), `chapter_head.md`, the four `intro_*.md` files and `gen.py`; the
chapter and the app's `examples/Nilsson_Riedel.cir` are regenerated from
them, never edited.

**Roberto's second read, 13 Sep 2026 — three more rules (16–18 in
`tools/nr12/README.md`).** Nothing the reader already knows from earlier
entries or from the settings line is said again (3.11 lost its "each
between the two nodes it joins … nothing has to be simplified first",
and every "we set the analysis to …" and "we leave omega as a symbol"
that the line under the description repeats is gone); a consideration
about how to read the results — the sign of what a source *supplies*,
the solver's note on a floating secondary, which answer is which — comes
*after* the sentence that runs the simulation, through a new `interpret`
field (3.11, 4.13, 9.10, 9.14, 9.15, 10.8, 11.1, 13.7); a single-letter
name is used only for the only element of its type, so the six entries
that had `e` beside `e2` (4.4, 4.7, 4.23, 9.12, 9.14, 10.8) now say `e1`,
their `.cir` entries with them; and the book's figure numbers are gone
from every question, `Fig. 4.42` reading *the figure*, since the page
does not use the book's numbering — 34 of them. Checked on the way: the
book does say *power developed* in Example 4.13, verbatim. Gates as
before, 63 ok, 50 of 50 through the app, 384 of 386 linked; live on
`learn` and the offline pair at cache **v215**, the version 9 account
wanting its pull, no `pip`.

**The fifteen rules applied to the Manual, 13 Sep 2026.** The eleven
Manual chapters with worked circuits (`21-manual-grammar` to
`31-manual-twoports`, 22 circuits) were revised the same way, by hand,
the Manual being hand-written markdown. Each worked circuit now opens
with what it is before its description (rule 8), declares every name we
chose in the first person plural (7, 9), states the analysis and the
card in the app's own words (12, 15), and shows every number it once
asserted as the result of a shown step (11): the Define example shows
its 6 V as a result panel, the Solve example shows the card's two boxes
and returns `rb` = 9333.33 Ω, the inverting amplifier shows its −9.4 V
output as a panel and the finite-gain model its −9400000/1000057 V
beside it, the AC power example shows `s_e` as a panel, the dot-reversed
coil shows its negated current as a second panel, and the transformer
shows the 12 V it had merely stated. The Expert Mode section no longer
calls a component value its "classic case" (rule 10): that is the Solve
card's job now, and the section says when Expert Mode is still the tool
— when the condition must be inside the solve so every answer carries
it. Every number was recomputed through the app before it was written
(`scratchpad/manual_numbers.py` for the record of the run), and
`build.py --check` solves all 22 circuits. Live on `learn`, web only;
**the Manual's PDF is not built, at Roberto's word**, and the three
tutorial PDFs do not contain the Manual.

**The fifteen rules applied to all 43, 13 Sep 2026.** Roberto asked for
the original Example 3.10 to be set beside its revision and rules derived
from the difference, then said *"Apply all fifteen across the chapter and
then the Manual, but do them yourself all. We will go over the results
together."* The eight new rules (8–15) are listed in `tools/nr12/README.md`
beside the first seven. What they did to the page, measured: every `shows`
paragraph now opens with what the circuit is and what the question wants
before any mention of the app (rule 8), and runs in the session's order
(14); every answer the reader gets by typing into Evaluate is shown as
its box and its result — 16 such boxes where there had been none, the
`-i_e`, `-p_e`, `v_1 - v_a`, `Abs(...)`, `1/z_j` and `v_3/vg` answers
among them (rules 11, 12); every range and every lettered part is
answered once per value in the Solve card or the Evaluate card, with
conditions — 5.1's parts (a) and (b) by Evaluate with `va = 1`, `vb = 0`,
its part (c) and 5.3's and 5.5's ranges by two Solve card runs each,
one per rail, 7.13's time to 150 V and 13.9's poles and zero by the
Solve card with `t` and `s` as unknowns, 14.6's $R$ and $L$ by the Solve
card from the two design equations (rules 11, 13); and **Expert Mode
appears on no entry now** — 5.3c, the last, is the Solve card with `rf`
as the unknown, the ordinary route answering it (rule 10). 4.21 lost a
sentence answering a part the page does not ask. The generator computes
every Evaluate and Solve card step through the real app's `evaluate_ui`
and `solveq_ui`, and the runner checks them all: **63 ok** — 43
examples, 7 first runs, 13 card runs. `verify_lesson.py` 50 of 50, the
link join 384 of 386. The chapter summary and the DC intro no longer
name Expert Mode. Live on `learn` (web only, the PDFs still held) and on
the offline pair at cache **v214**; the version 9 account wants a pull
and a Reload, no `pip`. **A caution earned on the way:** an hour went on
a solver bug that did not exist — the op-amp of 5.1 "could not be solved"
through every path tried, because the description had been *retyped* into
the test script with one node wrong; the spec's own description solved
at once. Copy a description from its source, never retype it.

**Example 3.10 answered from the Solve card, 13 Sep 2026.** Roberto's
ruling, after #433 made it work: *"Use my approach with Solve, which is
more representative of the exploratory way a student would follow. Show
explicitly the evaluation of both end values of the variable
resistance"*, then *"Use the underscores as well. And put the value of
r3 as a condition, not an equation … use the prefix like so: R_3=2'k."*
The page now describes the galvanometer as a short `sg`, leaves `V_s`,
`R_3` and `R_x` as symbols, runs the circuit in DC, and shows the
{{card:Solve}} card twice — `isg=0`, unknown `R_x`, condition `R_3=10`
giving 40 Ω, then `R_3=2'k` giving 8000 Ω — each with its three boxes,
spelled as his file spells them, and its answer read from the real
app's `solveq_ui`. A `solveq` field on the spec carries it (see
`tools/nr12/README.md`); the runner checks each run, so it reads **52
ok**. The head entry carries the first run's Solve fields exactly as
his own file had them; the second run is not an entry of its own — at
his word, the page just tells the student what to change in the
Conditions box and shows that box alone — so the app's book keeps **50
entries**, the app **406 across 21 books**. Expert
Mode remains on 5.3c alone, and the DC intro says so. Live on `learn`
(web only, the PDFs still held) and on the offline pair at cache
**v213** (v211 and v212 went up in the hour before, the first with spaces
round the `=`, which his file has not, the second with the other end as
an entry of its own); the version 9 account wants a pull and a Reload for
the book, no `pip`.

**Roberto's review, 12 Sep 2026 — seven rules, applied to all 43.** He
read Examples 3.7 and 3.10 and derived rules; the rules were then
applied down the page while he walked. They are listed in
`tools/nr12/README.md` and stand as the chapter's editorial standard:
no book title; the paragraph above the run compares nothing with the
book's method and states no result; only what the question asks is
reported; explain as to someone who does not know; what follows from an
answer comes after it; **nothing from thin air**; and **fact or choice**
— what the statement, the diagram or circuit theory gives is stated as
fact, every decision of ours (a name, a node, a symbol left open, a
source's node order) is stated as a choice, in the first person plural
the Course uses.

**What "nothing from thin air" did to the page.** Seven switched circuits
had been carrying an initial condition in a fifth field — 20 A, 100 V,
−8 A, 6 A, 5 A and 0, 10 A and 0 — that the book finds from the circuit
before the switch moves and the page had simply asserted. Each now has a
**first run** on the page: the pre-switch circuit described, run in DC,
its answer read, and only then written into the fifth field of the
second run, the way Lesson 6 does it. Each first run is its own app
entry (*NR12's Example 7.1 (DC, before the switch opens)*), so the
app's book has **50 entries** where it had 43, every one placed beside
its run with `::: applink`; `app_links.py` reads **384 of 386**, no
`nr12-sampler` loose end. Two values at an instant — 7.5's inductor
voltage at $t$ = 0 and 7.11a's current at 35 ms — are read with an
**Evaluate step** on the page (the answer's name in Evaluate, the
instant in Conditions), and 7.11b's fifth field is the exact expression
`6*exp(-1.4)` rather than a rounded number. 9.9's admittance is
`1/z_j` in Evaluate, 9.15's coil reactances are worked out from 9 H, 4 H,
$k$ and 400 rad/s in the text, the two op-amp designs do their resistor
arithmetic before the description, and 13.9's poles and zeros and 14.6's
$R$ and $L$ are arithmetic on the returned expression, after it.

**The galvanometer.** Roberto asked where 3.10's *500 Ω resistor `rg`*
came from. Not from the book: Fig. 3.30 gives the galvanometer no value,
and the 500 was the Assessment Problem printed beneath the example. It
was invented when the circuit was modelled and presented as the book's.
It is a symbol now (`rg,a,b,rg`; the answer is unchanged, since no
current flows through it at balance), and a sweep of every number in
every description against the book's own pages found no other invented
value — the only mismatches are the book's numbers in other units
(12.25 mA as 0.01225, 100 µS as 0.0001) and 7.11b's carried-over
current.

**Rule 3 trimmed the answer sets**: `r_e` from 3.11, node voltages and
currents where only a power was asked (4.4, 4.7), `v_2` from 4.8, `-i_e`
from 4.13, `vth` from 4.21 and 10.12, `i_r3` from 9.14, `v_nn` from
11.1, `v_1` from 13.2 and `i_l1` from 13.7. Two answers the book asks for
were **added**: 8.11's $v_C(t)$ and 9.10's $I_2$, both verified.

**The mechanism**, all in `gen.py` and `runner.py`: `pre` (first runs,
rendered, written to the `.cir`, and verified by the runner as specs of
their own — *50 ok* is 43 + 7), `evals` (Evaluate steps, their value
computed from the run and asserted against the book), `booknames` (the
book's symbol beside each value, or in a sentence under result panels),
`hide` (verified but shown another way) and `after`. The chapter's own
prose moved out of Python into `chapter_head.md` and `intro_*.md` at
Roberto's ask, so he edits the top matter as markdown; his rewrite of it
is in. **`learn` was deployed after each round so he could read it
live**, web only; the PDFs and the app train (cache bump, the offline
pair, both PythonAnywhere pulls for the 50-entry book) wait for his word.

**The questions were checked against the book itself**, page by page,
from `Other/NR12.pdf`'s text layer (readable for prose, scrambled for
maths). What that found: 7.13's `ask` carried a sentence that is not the
book's question and lacked its part (b); 7.5 had dropped the sentence
that explains why an initial current can be given (the switch is
make-before-break); 13.6 had been cut to a bare "find the Thévenin
equivalent"; 13.9's two parts and 13.13's second unknown were missing;
and the references in 13.2 and 13.3 to Examples 7.3 and 8.10 are the
book's own words, so they stay in the `ask`. Every book symbol that had
been flattened by stripping the LaTeX — `vC(t)`, `iL`, `io`, `V2/Vg` — is
maths again.

**Seven things wrong on the generated page, found by reading it:**

  * `polish()`'s em-dash rule ran over the whole string *after* the
    code/maths split, so Example 5.3's question rendered as
    `v_o = −4v_a — v_b — 5v_c`. Every rule now skips the kept spans.
  * The bare-variable rule read `j8`, `j5`, `j0.5` and `j28` as variables
    named *j*, so 9.9's paragraph said *{{var:j_8}}* and 11.1's question
    read *0.2 + j₀.5 Ω*. Those are maths now.
  * The bare word *ohms* became Ω: *"What is the value of R_L in Ω?"*.
    Only a number followed by *ohm* is a unit now.
  * 18.1's four answers were named `11`, `12`, `21`, `22`; the app names
    them `z11` to `z22`, and so does the page.
  * 5.3c's answer had no unit (`rf = 40000`).
  * 4.21 said the tool "answers all three parts" of a question the page
    stated in two; the book's (c) is now named and answered.
  * 4.8's "special case" was described as a current source shared by no
    other mesh. The book's special case is the **supermesh** — a source
    shared by *two* meshes.

**The closing sentence.** *— the same answers the book prints* ran
forty-three times and read as boilerplate by the tenth. It is gone: the
sentence reads *Symbulator returns …* and stops, the claim is made once
and in bold in *How to read an entry*, and the entries whose answers need
a word — the negated `-i_e` and `-p_e` where the book asks what a source
*supplies* (3.11, 4.13), the book's rounded amplitude (8.4), drops
printed as node differences (9.14), magnitudes only (11.1) — say it in
their own paragraph, where it is information rather than a refrain.

**Every `shows` paragraph was rewritten** to the same shape: what the
book does with the problem, what Symbulator does instead, and which app
answer is which book quantity (`v_r6` is the book's $v_o$). The facts
added were checked rather than recalled: 4.21's part (c), 35.7%, by a DC
solve with the 25 Ω load in place (900 W of 2520 W); 7.13's 67.7 ms and
13.9's poles $-3000 \pm j4000$ and zero $-5000$ by algebra on the
verified expressions; 14.6's 159.2 Ω and 202.6 µH by hand from
$\omega_0$ and $\beta$; 7.10's 1.5 H equivalent and 7.11b's 1.48 A the
same way. The section intros gained the context the old ones assumed —
that three TR entries are Laplace-chapter problems, that two AC entries
are rms — and `gen.py` now asserts each intro's opening count against the
specs it introduces.

**Gates**, all green on the regenerated tree: `runner` 43 ok;
`app_links.py` **377 of 379** with no `nr12-sampler` loose end;
`build.py --check` clean; `verify_lesson.py Nilsson_Riedel` **0 entries
with a problem** over all 43; and the chapter served locally through
`php -S` — 43 problems, **0 KaTeX errors**, the maths in the questions
rendering. The Browser pane could not screenshot it (`innerWidth` 0, the
pane hidden — the zero-measurement trap again), so the check was made on
the DOM's text instead.

**Not deployed, at the brief's word.** The `.cir` moved — every `ask`
is also an entry's `note:` — so this is a docs *and* app round when
Roberto gives it: a full `python build.py` (the prose is typeset) and the
`learn` deploy; then a cache bump in `repos/local/sw.js`, `build_local.py`,
`build_zip.py --assets ../../local`, `stage_install_site.py`, the `install`
and `zip` deploys, and a pull plus Reload on **both** PythonAnywhere
accounts. No solver change, so no `pip`. Capture `/7/` and `/8/` first.

## #428 — Contents goes back above the chapter on a phone — **live 13 Sep 2026**

On a phone the sidebar sat *beside* the chapter instead of above it, and
took more of the screen than the text: measured at a 385px viewport,
**170px of sidebar against 141px of chapter**, every line wrapping after
two or three words.

**A specificity collision, and #396's own comment is the clue.** The
mobile block collapses the layout with

    .shell:has(.toc:not([open])) { grid-template-columns: minmax(0, 1fr); }

at (0,3,0). #396 had scoped the desktop rule away from the home page to
stop a 19px sideways scroll, making it

    body:not(.home) .shell:has(.toc:not([open])) { ... max-content ... }

at (0,4,1). **A media query adds no specificity**, so the desktop rule won
inside the mobile block — but only when Contents was folded, which is its
default on a phone and not on a desktop. That is why it survived: the
desktop layout it was written for never showed it.

The fix is to give the mobile rule the same shape, `body:not(.home)`
included, so the two selectors match and the later one wins. Measured
after: **one column, 335px of chapter on a 375px screen, sidebar above**,
with Contents open and closed alike; desktop unchanged at 170+843 folded
and 272+741 open; and no sideways scroll on the home page at either width,
so #396 stays fixed.

**The lesson is the one #396 half-learned.** When two rules differ only by
a scoping prefix, changing one changes which media queries can still beat
it. Keep the pair the same shape, or the narrower one silently stops
applying.

## #425 — Select problems from Nilsson & Riedel 12ed — **live 13 Sep 2026**

A chapter of **43 worked examples** from *Electric Circuits*, 12th edition,
each described in Symbulator and **checked against the answer the book
prints**: `/9/nr12-sampler`, `kind: back`, version 9 only. DC 16, TR 14,
AC 8, FD 5 — the four analyses were a requirement of the brief, not an
accident of what was easy.

**The selection is the point.** These are the problems where the distance
between *describing* a circuit and *solving it by hand* is widest: a delta
that must be transformed (3.11, 9.10), a supermesh (4.8), a dependent
source three steps from its controlling current (4.4, 4.7, 9.12, 9.14), a
linear transformer (9.15), a switch that opens twice (7.11), an impulse
(13.13), the full three-phase circuit rather than the single-phase
equivalent the book has to build first (11.1), cascaded two-ports (18.6).
{card:Expert Mode} appears twice, where the thing you know is an answer
and the thing you want is a component: the Wheatstone balance (3.10,
`i_rg = 0` → `rx = 4*r3`) and a saturating summing amplifier's feedback
resistor (5.3c, `v_4 = -12` → 40 kΩ).

**The join to the app.** Every circuit ships as a built-in book,
`examples/Nilsson_Riedel.cir`, so the app now carries **399 entries across
21 books** (measured with `grep -c '^\[' *.cir`, not quoted). Each problem
carries the usual *Open in app* / *Open in split view* pair. That needed
three things changed together, and they must stay together:

  * `openFromUrl()` in the app's template gains `?lesson=nr12`;
  * `app_links.py` gains a `NAMED_BOOKS` table for books with no lesson
    number, and `"nr12-sampler": ["nr12"]` in `CHAPTER_BOOKS`, which is
    also what writes the split view's `lessons.json` in both directions;
  * the problem titles are **short** — `NR12's Example 4.4` — because
    `parse_book` truncates an entry name at 80 characters and the join is
    on the title. The book's own descriptive title moved into the body.

All 43 resolve, no loose ends; the coverage report reads 377 of 379.

**The textbook code is NR12**, the credits table's own, matching the
`NR11's …` entries already in the app. It said `N&R's` for one deploy;
the session working on the documentation caught it.

**Four things measured rather than asserted.**

  * Every answer compared with the book's printed one — 43 of 43 — and
    twice the book's *text layer* misled: it renders `v = 24(2) = 48 V` as
    `v 24 24 8V`, and two wrong expectations were written from it before
    Symbulator disagreed. That disagreement is the whole value of checking
    against a printed answer instead of one's own reading of it.
  * Every entry run through the **real app** with `verify_lesson.py`, not
    just through the solver API. That is what caught 9.15, which passed
    `th()` and failed the app outright — see #426.
  * The figures: 41 crops from the PDF, taken by clustering the vector ink
    above each `Figure N.M ▲` caption. Three needed a hand-set top where
    the cluster swept in a formula or a line of prose.
  * The op-amp problems answer **every lettered part** (5.1, 5.3, 5.3c,
    5.5). They first stated the formula and left (b) and (c) to the reader,
    which Roberto rejected: *"Make sure you answer each part, separately."*

**Fair use**, in the credits chapter's own words: *for the purpose of
teaching students how to use Symbulator, these diagrams are reproduced
under the principle of fair use. No copyright infringement is intended.*

**The PDFs were rebuilt** — the documented exception to the `--web`
default, since a whole chapter had moved: v9 **347** pages, v7 **235**,
v8 **223**, the Manual **39** (shipped at Roberto's word). Versions 7 and
8 were proved unmoved across the deploy over eight pages, compared
semantically — byte identity is unreachable while a shared stylesheet
carries a content hash.

**A build warning worth keeping.** The first full run printed **NO PDF
PRODUCED for v7, v9** while in fact writing and copying all four PDFs
correctly; a re-run with no source change was clean. MiKTeX fetching a
package on first use is the likely cause. `build.py` is right to treat the
message as fatal and the right response is to re-run — never to ship the
files a failed run disowned.

## #424 — the Course read as a version 9 book — **live 13 Sep 2026**

**Deployed at Roberto's "ship it" on 13 Sep 2026, both passes together,
and verified by fetching**: `/9/lesson-equivalents` carries the twenty
"In DC, `vth` gives …" sentences and no "Via"; `/9/lesson-ac` the
*Mini-Tools card* subsection; `/9/lesson-power` the heading *The pf
mini-tool*; `/9/manual-orientation` *Three tools*; `/7/lesson-dc` "your
first simulation in Symbulator."; `/7/lesson-equivalents` a sidebar
listing *The equivalent resistance script: er* where it listed nothing.
**The deploy was built from a clean `git worktree` of HEAD, not from the
working tree**, with a junction beside it so `build.py` could reach the
app tree: the working tree carries #423's uncommitted work and the
Nilsson & Riedel sampler chapter that Roberto is having written
(*"Do not include that one in your revision"*). The sampler's 47 asset
files were already on the server from that session and its chapter is
not in the live `toc.json`, so the clean build changed nothing about it.
23 files moved. **What did not deploy:** the `.cir` fix, which wants
Roberto's pull on `symbulator.pythonanywhere.com` (no pip) and the
offline pair's next `build_local.py` train — not run, because that train
would copy the drawer session's uncommitted template. The summary PDF is
`Notes/course_review_424.pdf`, copied to
`C:\Users\perez\Downloads\Symbulator_Course_review_424.pdf`.

Roberto: *"Can you read the Course and identify its shortcomings? For
example, I just noticed that it mentions the aa tool in passing without
having introduced it first. And it calls it a tool, not a mini-tool
(which would be the right term). … the current Course for v9 was adapted
in a series of pushes from the v7/v8 documentation, and it does not read
yet as a 'native for v9' Course."* Summary for his review in
`Notes/course_review_424.pdf`; the edits as one table in
`Notes/course_review_424.py`.

**How it was read.** Version 9's view of every chapter, with source line
numbers, through `tools/v9_lines.py` — 6,274 lines across the
Introduction, the thirteen lessons and the credits — then a regex sweep
for the calculator's vocabulary over the same view. The sweep is worth a
warning: `v9_lines.py` strips spans with a flat regex, so a nested span
shows as a fragment (`answers with the  command of the calculator}}`) and
reads like a leftover when the build handles it perfectly. Check the
source before believing the tool.

**What was wrong, by kind.**

- *Tool for mini-tool.* aa, pf and gain are the three entries of the
  {{card:Mini-Tools}} card and the app calls them mini-tools; the Course
  called all three "tools", in two headings, three chapter summaries,
  the index and the prose. And `pr()` is neither: it is a function,
  usable in a value or in {{card:Evaluate}}.
- *aa used before it was introduced.* Lesson 7 mentioned "the aa tool"
  twice in its *Rectangular or polar* section and then used it in the
  first worked example, with no sentence anywhere saying what the
  Mini-Tools card is. **A short subsection, *The Mini-Tools card*, now
  sits in Lesson 7 before the first AC problem**, naming the card, the
  three mini-tools, what each takes, and which lesson introduces each;
  Lessons 8 and 13 refer back to it.
- *Calculator habits in shared prose the adaptation never split.*
  "evaluate the negative of that power", "store this value in a
  variable", "when the simulation is *Done*", "stored in the memory",
  "in variables that should be familiar", "sets Symbulator apart from
  other programs", "cSolve", "Expert" for Expert Mode in three headings
  and sentences, "the computer". Each is now a `{{v7,8|…}}{{v9|…}}` pair.
- *The wrong version number for 7 and 8.* Lesson 1's "your first
  simulation in Symbulator 9" was shared prose, so the 2023 pages have
  been telling calculator readers they ran version 9. **This is the one
  edit that changes what 7 and 8 render**: the 2023 original reads
  "Symbulator" (checked in `originals/docs-page7.html` and `-page8`), and
  that is what they say again, with `{{v9| 9}}` for version 9.
- *A worked example that cannot give its printed answer.* Bo2's Drill
  Exercise 5.1 (TR) in Lesson 6 uses `vc0` as the capacitor's initial
  condition; the calculator text stores it with `vc→vc0`, the version 9
  text said nothing, and the built-in entry in
  `Application/v9/repos/server/examples/Lesson_06a.cir` had no Define
  either — so the app answered `i_c = -vc0·e^{-4t}/3` where the note
  promises `-2e^{-4t}`. Version 9 now shows a {{card:Define}} field with
  `vc0 = 6` and says so; **the `.cir` entry gains `defines: vc0=6`**,
  checked through the solver (`i_c = -2*exp(-4*t)`) and through
  `circuitbook.parse_book`. That is the one app-tree change and it rides
  the next app deploy.
- *Gaps a version 9 reader saw.* "We can use its exact value, , but the
  textbook prefers…" — the exact value was in 7- and 8-only spans; a
  `{{v9|8*exp(-1)}}` fills it. Three bare answer lines (`.055`, `2`,
  `-2`) followed 7/8-only code with nothing in version 9 to introduce
  them; a version 9 sentence now leads into each.
- *Small things.* "equationse"; a leading space before a paragraph;
  "Say 'given' in Evaluate's Conditions box" (the calculator's `|`
  operator, meaningless here); "It returns the value and the verbal
  description together, in one string"; "Store them in Define";
  "the best symbolic simulator … ever to run on a handheld device" for
  a version that runs in a browser; "Symbulator is a program".

**Measured, not asserted.** 62 scripted edits across 11 source files,
nine index-term and heading edits by hand, four heading anchors. The
built `content/v7` and `content/v8` are byte-identical to the pre-edit
build **except `lesson-dc.html`**, whose one difference is the word "9"
removed from that sentence; their `toc.json` (index and chapters) is
identical. Version 9 changed in eleven Course pages and two Manual pages.
`build.py --check` clean, the index guard clean (123 terms, one more than
#422 left: *Mini-Tools card*, on the new subsection; *aa mini-tool*, *pf
mini-tool*, *gain mini-tool* and *pr function* replace the four "tool"
terms), `check_against_originals.py` 81 blocks
verified as before.

**The trap this one walked into.** Splitting a heading into spans moves
its anchor: `slugify()` drops every `{{…}}`, so "The pf
{{v7,8|tool}}{{v9|mini-tool}}" became `id="the-pf"` and the 7/8 markup
moved on three pages. The byte comparison caught it; the three headings
carry explicit anchors (`{#the-pf-tool}` and kin) that keep the ids they
had. And a `{{v7|…}}` span in Lesson 11's summary left a hole for version
8, which renders that chapter's summary on its "not in this version"
page although it has no Bode lesson: `{{v7,8|…}}` is right there even
though the chapter is `versions: [7, 9]`.

**And one the comparison found that predates this round.** The sidebar's
section list is built from each `h2` by stripping every brace command,
so a heading written in two versions has been listed truncated or empty
in the Contents column of **all three versions** since the day it was
split: Lesson 4's two main sections as *nothing at all*, Lesson 2's as
*"Numerical from symbolic, with"*, the Introduction's *Install* as "".
`build_web()` now resolves the version's span first
(`resolve_vspans(b.text, v)`) and drops emphasis marks. The 7 and 8
sidebars change on those pages — from broken to right — and that is the
second thing this round alters in what they show; both are listed for
Roberto's veto in the PDF.

**The second pass, 13 Sep 2026, at Roberto's word** (*"yes, please do
that round now"*): the practice sections. 56 edits in
`Notes/course_review_424b.py`, gated the same way. Twenty of them are one
sentence of Lesson 4 written twenty times — *"Choose DC. Via `vth` we find
V = 48 V. Via `req` we find R = 6 Ω."* — which a regex turns into *"In DC,
`vth` gives V = 48 V and `req` gives R = 6 Ω."*; the rest are the
calculator verbs in the worked problems: *"Select DC. Add equation. Add
unknown. Run the simulation."* becomes *"In DC, with … in Add equation(s)
and … in Add unknown(s), run it."*; *"ask for"* becomes *read*, *look
for*, or names Evaluate; *"Evaluating approximately gives us"* becomes
*"Evaluate gives"*; *"When it's done, ask for the answers we need"*,
*"Once the simulation completes, we ask for the variables of interest"*,
*"We get that v_x is 78 V"* and their kin are reworded. "This is
correct." was kept: it is the author confirming against the book, and it
restates no value. **Roberto's two rulings**: the Manual's Orientation
now counts *three* tools (equivalent resistance, Thévenin/Norton, two-port
parameters) and *three* mini-tools (aa, pf, gain) — it had said "four
tools … and gain" — and the Reference's table is headed *Tools and
mini-tools*; and "Thevenin" is spelt with its accent everywhere it lacked
one: Lesson 4's summary (all three versions, at his word), five
`::: result Thevenin voltage` panel labels (version 9), and one 7/8-only
sentence in Lesson 5, a spelling correction in frozen text and flagged as
such. The PDFs were not rebuilt.

**Numbering.** This item took #423 first and found, uncommitted in the
app tree's `NEXT.md`, the drawer restyle already holding it, so it moved
to #424; the app session was writing to the same `Documentation` tree at
the same time (the monograph figures, a Nilsson & Riedel sampler chapter),
so every commit here names its files rather than using `-a`. **One of the
#422 commits did not**: `d60cabd` swept that session's uncommitted
`paper/render_exemplars.py` in under the #422 message. Nothing is lost —
the file is what that session wrote — but the history attributes it to
the wrong item.

---

## #423 — claimed by the app tree, 12 Sep 2026: **the schematic drawer restyled on Nilsson & Riedel 12e** — symbols, stroke weights, label face and colours measured from the book's own vector figures. The docs side of it is the monograph's Appendix B, re-rendered by `paper/render_exemplars.py` (now embedding DejaVu Serif) and the book rebuilt. Write-up in `Application/v9/repos/local/NEXT.md`

## #422 — the index, rebuilt for version 9's three books — **live 12 Sep 2026**

**Deployed at Roberto's "Ship it!" the same evening and verified by
fetching, not by the upload log:** 37 files moved (35 version 9 pages
and `toc.json`, `index.php`, `assets/style.css`; 675 already identical).
`/9/index` serves 122 terms, 213 book labels and 240 anchor links; two
targets fetched at random -- `ix-si-prefixes-1` on Tech Note E and
`ix-numerical-solver-0` on the Manual's toolbox part -- are each present
exactly once on their page. `/7/index` and `/8/index` were captured
before the deploy and re-fetched after: identical once whitespace and
the `style.css?v=` hash are normalised, 34 and 32 terms as before. The
dry run caught one thing worth keeping: a scratch copy of the old page,
`build/web/index_old.php`, left there for the rendering comparison,
would have gone up as a new file. **`build/web` is what a `learn` deploy
uploads, so nothing may be parked in it, however briefly.**

Roberto: *"There is an index in Symbulator's documentation, but it is not
good. I want to replace it with a proper index."* And, mid-way: *"I'm
interested in an index for v9. Feel free to exclude versions 7 and 8."*

**Measured before and after**, on the built `toc.json`, by
`tools/check_index.py`:

    before   v9: 33 terms,  34 locations (course 33, manual 0, notes 0)
    after    v9: 122 terms, 240 locations (course 97, manual 101, notes 15)
             v7: 34 terms,  35 locations -- unchanged
             v8: 32 terms,  33 locations -- unchanged

The mechanism was never the problem. `{{i:term}}` already emits an
invisible anchor at the exact sentence, records `chapter#anchor` in
`toc.json`, and writes `\index{}` for makeindex; `index.php` renders the
numbers. What was missing was **the judgement**: 42 markers, all in the
Course, none in the Manual or the Notes, several in the calculator's
vocabulary. The job was deciding which terms and where.

### The rules the terms were chosen by

- **Where a thing is explained, not where it is mentioned.** *resistor*
  appears hundreds of times and is taught once. Each term gets the place it
  is taught (a Course lesson), the place it is stated precisely (a Manual
  part), and a Note where one goes deeper -- and nothing else. The cap is
  four locations, and one term reaches it (*SI prefixes*: Lesson 1, the
  grammar part, and two places in Tech Note E).
- **The reader's word, not the system's.** *Thévenin equivalent*, not *th
  tool*; *operational amplifier*, with *nullor* as a secondary entry at the
  Manual's line, not the other way about. Software names are secondary
  entries where someone would genuinely type them -- *pf tool*, *aa tool*,
  *pr tool*, *Solve card*, *Numerical Solver*.
- **The concept, not every case.** *three-phase circuits*, not balanced
  wye-wye, unbalanced wye-wye, and six more; the one three-phase entry
  added is *delta-connected sources*, because that passage teaches a trap.
- **Synonyms are settled by alphabetical adjacency, not by duplicate
  entries.** *op amp model (finite gain)* sits beside *operational
  amplifier*; *frequency domain* and *s-domain* both exist because they
  sort far apart and both are looked up.
- **What Symbulator will not do is indexed too.** *Fourier series and
  transforms*, *convolution*, *energy*, *nonlinear devices*, *transmission
  lines*, *noise and tolerance analysis* each land on the Manual's
  Orientation, where the limits are stated, and on the Reference's last
  section; *superposition*, *source transformation*, *power-factor
  correction* and *poles and zeros* -- supported but not automated -- the
  same. A reader who looks up *Fourier* and finds an entry that says "not
  here, and here is why" is better served than one who finds nothing.

The vocabulary started from the coverage inventory of 11 Sep 2026 (read
out of `elements.py`, `__init__.py`, `circuitbook.py` and the app template,
not out of the prose) and was placed by reading every explanatory section
of the Course, the whole Manual and all six Notes.

### Versions 7 and 8 are untouched, by construction

Every new marker in shared prose is written `{{v9|{{i:term}}}}` -- the
inline parser has counted brace depth since #358 -- so neither the anchor
nor the entry exists in 7 or 8. Markers inside `::: only 9` blocks and in
the version 9 chapters are bare. **Verified by measurement, not by
reading:** the built `content/v7` and `content/v8` directories are
byte-identical to the build of `e4523b3`, `toc.json` included, and the
rendered `/7/index` and `/8/index` pages are identical to the old
`index.php`'s output once whitespace between tags is normalised (the PHP
control blocks indent differently; the markup, text and links are the
same). The only other 7/8 change is the shared `style.css` gaining a rule
they never trigger, which moves their cache-bust hash -- the benign
difference #390 and #395 documented.

Two things were deliberately **not** done to 7 and 8, and each is one
line to lift: their index keeps the old byte-order sort (uppercase first,
so *Bode plot* leads and *aa tool* follows *SI prefixes*) behind an `if v
== 9` in `build_web()`; and the shared markers were not added there even
where the concept is version-neutral. The existing `expert mode` marker is
renamed *Expert Mode* in the version 9 block only; 7 and 8 keep the lower
case they had.

### What changed in the machinery

- **`build.py`**: version 9's index is in reading order and dictionary
  order. The spots were `sorted(set(...))`, which put `lesson-ac` ahead
  of `lesson-sources` for *dependent source* and would put a tenth spot
  ahead of a second; they now keep the order the renderer met them in.
  The terms sort with accents folded and case ignored (`_ascii(t).lower()`),
  so *Thévenin* files under T and a capital does not lead the list.
- **`web/index.php`**: when a version has more than one shelf, each
  number is preceded by the book it opens -- *SI prefixes* COURSE 1
  MANUAL 2 NOTES 3 4 -- and carries the chapter title as a tooltip. One
  shelf, and the markup is the old markup. Labels are Course, Manual,
  Notes; the numbering runs on across books.
- **`web/assets/style.css`**: one rule, `.ix-book`, in the palette's
  `--ink-3`.
- **`tools/check_index.py`**, wired into `build.py --check`. In the
  source: no marker in a code fence, a heading, a table row or a
  directive line; no term with `! @ | "` (makeindex's specials -- the
  same markers feed the PDF's index). In the build, per version: every
  `chapter#anchor` in `toc.json` has its `id=` in the built page, and has
  it **once** (two terms that slugify alike -- *expert mode* / *Expert
  Mode* -- write the same id twice on one page, and the browser scrolls
  to the first); no version 9 term contains *script*, *command* or
  *program* on a word boundary (#409, and "circuit de**script**ion" is
  why the boundary matters); no term has more than four locations; and
  version 9 reaches all three shelves. It prints the census above on
  every run.

**Proved red seven ways before being believed**, each sabotage restored
afterwards and the tree re-checked clean: an anchor deleted from a built
page; `{{i:th script}}` planted in an `::: only 9` block; a fifth location
on *SI prefixes*; a marker in a heading; `{{i:expert mode}}` planted
beside `{{i:Expert Mode}}` in the same version 9 block, caught twice over
(the shared spot in `toc.json` and the doubled id in the page); and a
`!` in a term. **The first attempt at the shared-anchor sabotage stayed
green**, because it planted the twin in a different chapter from the
original's first occurrence, which gives two different `chapter#anchor`
strings and two different pages -- no collision anywhere, so the guard was
right and the test was wrong. The doubled-id check was added on the back
of that, because the id on the page is the artefact the reader's browser
actually resolves.

### How it was placed, for the record

`Notes/index_markers_422.py` holds the whole table -- 177 edits across 34
source files, each an anchor of sentence text that must occur exactly
once in its file, and the terms to place after it. It reads the `::: only`
blocks around each anchor and chooses bare or gated form itself; an anchor
inside an `::: only 7,8` block is refused. Dry run by default, `--apply`
to write. Kept so the placement can be audited or re-run, not because it
will be needed twice.

### Not done, and worth knowing

- **The PDFs were not rebuilt.** The standing `--web` instruction holds;
  the new markers add `\index{}` entries, so the next full build's
  `symbulator-v9.pdf` index grows from 33 to 122 terms. Two things to
  watch then: makeindex sorts by bytes, so *δ(t)* and *ω* may file oddly,
  and its case handling differs from the web's folded sort.
- **`tools/static_preview.py` still writes the flat numbers** with no
  book labels. It generates its own markup and does not read `index.php`;
  the preview is for looking at chapters, and the index page there is
  functional but unlabelled.
- **A sentence in shared prose says "Symbulator 9" to readers of 7 and
  8**: `src/01-lesson-dc.md` line 68, *"You have just run your first
  simulation in Symbulator 9."*, sits outside the `::: only 9` block above
  it. Seen while placing markers, not touched -- frozen text, Roberto's
  call.
- 122 terms is a little over the 120 the brief called the noise line.
  Thirteen candidates were cut on the way (*voltage divider*, *purely
  symbolic problems*, *admittance*, *Mini-Tools card*, *reciprocal
  network* and eight more); what remains is listed by the census, and
  trimming is a matter of deleting markers.

---

## #421 — PHP on the laptop, and the first executed test of `index.php` — **12 Sep 2026**

For the whole life of this tree, `web/index.php` has been reviewed by
reading. The notes said *"there is no PHP on this machine"* — and the
wording was the problem: Roberto read *this machine* as a data centre
somewhere and had no idea the missing piece was on his own laptop, which
he could have fixed in a minute at any point. **Say whose machine.**

He installed it the moment it was clear:

    winget install --id PHP.PHP.8.4 --exact --source winget

PHP **8.4.24**, ZTS, and `json_decode` is compiled in, so no `php.ini` is
needed — `index.php` uses no extension beyond it (checked by grepping for
`mb_*`, `iconv`, `curl_*`, `simplexml` and friends: two `json_decode`
calls and nothing else). winget installs to

    C:\Users\perez\AppData\Local\Microsoft\WinGet\Packages\PHP.PHP.8.4_Microsoft.Winget.Source_8wekyb3d8bbwe\php.exe

and **does not put it on the PATH that Bash or PowerShell see in this
session** — call it by that full path, or open a fresh login shell.

What it buys, immediately:

    php -l web/index.php                          syntax, before a deploy
    php -S 127.0.0.1:8099 -t build/web            the real site, locally

`php -S` ignores `.htaccess`, so pretty URLs do not route — but
`index.php` reads `$_GET['v']` and `$_GET['p']` directly, so
`?v=9&p=notes` reaches every branch the pretty URL would. That is enough
to test all of it.

**This is the guard the three bugs of 11 Sep would have failed against** —
`$thisShelf` used before it was defined, `$pageTitle` dereferencing a null
chapter, and the sidebar duplicating its own grid. All three were found by
reading, after they were written, and any of them would have been a blank
page or a fatal on the first request here.

---

## #420 — the ribbon stops guessing which book you are in — **12 Sep 2026**

Roberto, across five messages while looking at the live site. Three books
have made two ribbon links ambiguous and one mark too short.

**The two links.** *Download as PDF* and *Split View* both name a book.
On a page that belongs to no book they had to guess, and both guessed the
Course: the home page offered `symbulator-v9.pdf` and a split view opened
on `introduction` — to a reader who had not yet chosen a book, on the very
page whose job is that choice. The Technical Notes shelf had the same
shape, handing over the Course's 309 pages.

One predicate rather than three patches:

    $bookless = ($v === '9') && ($isHome || $shelf === 'notes');

and both links sit behind it. Everything else keeps both, and they were
already right:

| page | PDF | Split View |
|---|---|---|
| `/9/` | — | — |
| `/9/course`, a lesson | `symbulator-v9.pdf` | that page |
| `/9/manual`, a manual part | `symbulator-manual.pdf` | that page |
| `/9/notes` | — | — |
| a technical note | `symbulator-v9.pdf` | that page |
| versions 7 and 8 | their own | *How it works* |

A **technical note is not bookless**: the six notes are printed inside
`symbulator-v9.pdf` at their own page numbers, so a note page's PDF link
is correct. Only the shelf, which is a contents page for a book that has
no PDF of its own, loses it.

Two things that would have gone wrong silently. The version test and the
7/8 test are an `if/else`, so widening the *outer* condition with
`&& !$isHome` would have dropped a version 9 reader into the else arm and
printed versions 7 and 8's *How it works* on version 9's home page; the
home test is nested inside instead. And `$isHome` is true on 7 and 8's
home pages too, so `$bookless` names the version — those have one book,
the link is unambiguous, and their pages must not move.

**`/9/manual` needed no change at all.** Roberto asked for the Manual's
PDF and a split view onto the Manual there; both were already correct,
verified by fetching the live ribbon and by driving
`/split/?page=manual`, which loads the Manual in the left pane with its
fourteen parts and the MANUAL mark.

**The mark reads Technical Notes.** It said *Notes*, on a comment's
assurance that TECHNICAL NOTES "cannot be measured from here." It can:

| viewport | band | long form | clearance from the wordmark |
|---|---|---|---|
| 1200 | top | 165.1px | 430px |
| 860 | top | 165.1px | 142px |
| 700 | top | 165.1px | 24px |
| 680 / 660 / 645 | top | 165.1px | 24px |
| 600 | top | 121.9px | 24px |
| 320 | slot | 121.9px | in a 155px slot, one line, unclipped |

It never collides — but below 700 the 24px stops closing, which means the
*wordmark* is giving up room instead. So the top band takes the short
spelling under 700px and the long one above it; the phone slot sits below
the wordmark, competes with nothing, and stays long. Both spellings are
emitted with one shown, the idiom the banner already uses for
`.vkey-full`/`.vkey-num`. **The rule lives in learn's own `style.css`,
not the shared `banner.css`** — no other property has this mark, and the
shared file would have to be propagated to the landing page and the app
for nothing.

Only the Technical Notes emit two spans; Course and Manual are one word
and render as plain text.

**The landing page still sold one book**, and its section heading was by
then a flat denial of the Manual: *"A course, not a manual."* It now reads
*"A course, a manual, and the fine print."*, the Course's card is named
(*Read the documentation* no longer names one thing) and the Manual has a
card of its own, with the Technical Notes in its last sentence. The blurbs
are lifted from the live chooser rather than invented, so the landing and
the front door describe each book the same way. All 21 outbound links were
fetched: every one 200, including the two new shelf URLs. The two 404s are
bare `preconnect` origins, which is what they are meant to be.

### What was measured, and the three instruments that lied

Every claim above is a measurement, and **three of the first attempts were
wrong in the instrument rather than the subject** — which is now five
instances in two days.

1. Reading the mark's width with `getBoundingClientRect()` returned
   **155px for both spellings**: the slot is a block filling its parent
   and its box says nothing about its glyphs. A `Range` over the text node
   is what measures text.
2. Sweeping widths by setting `documentElement.style.width` produced
   seventeen identical rows. **Media queries key off the viewport**, not
   an element's width, so the sweep re-measured one emulation seventeen
   times. Real `resize_window` calls were needed.
3. Every screenshot came back a flat dark rectangle while the DOM read
   back perfectly. **The Browser pane was hidden** — and a hidden pane
   does not paint and does not fire `requestAnimationFrame`, which is also
   why a perfectly ordinary `await` in a probe timed out at 45 seconds.

### The check

`tools/check_ribbon.py` — ten pages through a real PHP server, asserting
each one's PDF target, third link and property mark. Proved red three
ways before being believed: `$bookless` forced false (2 failures),
forced true (8), and `$inManual` forced false (2); the restored copy is
green. It needs PHP, so it is opt-in rather than wired into
`build.py --check`, which must keep running on a machine without it.

### Numbering

Written as #410 throughout and renumbered before commit: the root
`CLAUDE.md` records the app tree's Numerical Solver round as **#391–#419**,
so #410 was inside a range another session already holds — and
`NEXT.md` does not spell those numbers out as headings, so a grep for
`#410` came back clean in *both* trees. **Grep the prose and the ranges,
not just the headings.**

---

## #409 — version 9's index spoke the calculator's vocabulary, and the fix reached 7 and 8 — **fixed 12 Sep 2026, live**

Roberto: *"That index is bad, by the way. In v9 it talks of the 'th
script', which doesn't exist in v9."*

**How it got there is the part worth keeping.** The version 9 wording pass
(#251–#254) rewrote the prose to drop *script*, *command* and the rest of
the calculator's words — but an `{{i:}}` marker is not prose. Nobody
re-read the markers, and nothing checks them. Three of them in
`src/04-lesson-equivalents.md`:

| line | block | marker | |
|---|---|---|---|
| 234 | `::: only 7,8` | `{{i:th script}}` | correct there |
| 239 | `::: only 9` | `{{i:th script}}` | wrong |
| 142 | **shared prose** | `{{i:er script}}` | wrong in 9 — and one term serves all three versions |

**The first fix was a breach, and the guard caught it.** Re-terming all
three to *equivalent resistance* and *Thévenin equivalent* reads as an
improvement and is one for version 9. But the shared marker is read by
versions 7 and 8, and the marker at 234 sits inside *their* block, so
their index lost two terms that are **correct for them** — those versions
really do have an `er` script and a `th` script. That is frozen text,
changed without asking.

`v78_semantic.py` fired on `/7/lesson-equivalents` and
`/8/lesson-equivalents`. Note what it could and could not see: the
**visible text on those two pages was identical**, so only the normalised
markup diff showed anything at all, and the actual damage was on a third
page, `/7/index`, which was not in the capture set.

**The fix is to gate the markers, not to re-word them.** Shared prose now
carries none; `{{i:er script}}` sits inside the `::: only 7,8` block,
`{{i:equivalent resistance}}` inside `::: only 9`, and `{{i:th script}}`
is restored at 234. Measured on the live site afterwards, not asserted:

    v7: 34 terms, 'er script' and 'th script' both present
    v8: 32 terms, 'er script' and 'th script' both present
    v9: 33 terms, no term naming a script or a command

**One residue, and it is benign — but know what it is before the next
deploy.** The two lesson pages still report DIFFERS in the semantic
guard's markup column with their visible text identical. The whole
difference, all seven chunks, is the invisible anchor

    <span class="ix" id="ix-er-script-0"></span>

moving one sentence later: out of the shared paragraph and into the
only-7,8 block, which is precisely what gating the marker means.
**An index anchor's position is part of 7 and 8's markup even when the
term is unchanged**, so the guard reports a moved marker exactly as
loudly as a changed one. Read the diff before reverting on its word.

**And the check was wrong before the subject was, again.** The first
script written to read the live index pages matched `class="ixterm"`;
the class is `ix-term`. It returned **0 terms for all three versions** —
including version 9, which certainly has an index. A zero that spans the
control is the instrument, not the specimen.

---

## #408 — the Manual's credits — **done 12 Sep 2026, live**

Roberto: *"I think we need an equivalent of 'Roll the credits' for the
Manual. Boil it down to the essentials."* Then, on reading the draft:
*"You need to add the acknowledgements."*

`src/34-manual-credits.md`, `kind: manual-back`, `book: manual`. The
author and the dates in two paragraphs, then all **23 named
collaborators** across versions 1–6, 7–8 and 9; the Claude section
carrying the `::: warning Use AI responsibly` box in Roberto's own words;
the software it stands on, with ahkab described the way the standing rule
requires — a second opinion, at arm's length, no code taken; and the MIT
licence.

The contact section is a role address, not a riddle: **`help@symbulator.com`**.
The Course's credits obfuscate Roberto's personal address by describing
it; a role address needs no such thing. The `::: tip The long version`
that pointed back at the Course went with it — the Manual's own last page
does not need to end by sending the reader elsewhere.

Two things bit on the way, both in tooling rather than in prose:

- **`tools/static_preview.py` marked every Manual part COURSE.** Its
  `_mark` helper took the version and nothing else, so it could not know
  which book a page belonged to. It takes the page id now.
- **The white-text guard refused the Manual's PDF** on the contents page,
  honestly and wrongly: dot leaders are *text*, so a sparse page of
  chapter titles and leaders reads as a very high text-to-ink ratio. The
  guard strips runs of three or more dots before measuring.

---

## #407 — the home page is a choice between three books, not a list of 35 — **done 12 Sep 2026, live**

Roberto: *"I don't like the cluttered look of the current
learn.symbulator.com page… we should not have all three books there with
all their chapters. Instead… a box or card for each, that — when clicked
takes the user to that 'landing' page where the layout of the chapters is
presented."* And: move the chooser text **above** each card, and write one
for the Technical Notes.

`/9/` is three covers now. Each has its own landing page —
**`/9/course`, `/9/manual`, `/9/notes`** — recognised as virtual slugs
before the 404 fallback, so no `.htaccess` rule was needed and the
routing stays `^([789])`. One function decides where a chapter lives:

    function shelf_of($c) {
        if (($c['book'] ?? 'course') === 'manual') { return 'manual'; }
        if (($c['kind'] ?? '') === 'note')         { return 'notes'; }
        return 'course';
    }

The sidebar reads it too, so a reader in the Manual sees the Manual's
parts and not 35 entries from three books (Roberto: *"I think the sidebar
should only show the chapters for the relevant book"*). Four near-copies
of the card grid collapsed into one `$renderGrid` closure.

**`web/index.php` cannot be run on this machine, so it was reviewed by
reading — and reading found three real bugs** that a browser would have
found in seconds: `$thisShelf` was used by the pager before it was
defined, `$pageTitle` dereferenced a null chapter on a shelf page, and
the sidebar duplicated the grid it sat beside. Worth remembering as the
cost of a PHP page with no local runtime: the review has to be as careful
as a test suite, because it *is* the test suite.

Then the fine tuning, all Roberto's:

- **Dark-mode contrast on the cover titles**, reported with a screenshot.
  The cause is deliberate and easy to walk into again: `--navy` is a
  fixed brand colour that the dark theme **never overrides**, so the
  title sat at **1.56:1** on the dark ground. Titles take `var(--ink)`
  now and the eyebrow and meta lines `var(--ink-2)`.
- **19px of horizontal overflow** on every page without a sidebar. The
  shell's first grid track was sized from content that was no longer
  there:

      body:not(.home) .shell:has(.toc:not([open])) {
        grid-template-columns: max-content minmax(0, 1fr);
      }

  `:has()` takes the specificity of its argument, which is what makes
  this rule win where a plainer one had not.
- **The Notes heading.** My proposal was rejected on the substance —
  *"the notes don't cover every 'something', only a small set of obscure
  somethings"* — and he chose **"Want the detail the lessons leave out?"**
  The blurb under it is his wording too.

**On the numbers:** two commits in this round are labelled #395 and #396,
which the app tree also used the same day. Roberto, asked: *"Do not worry
about the numbers."* Recorded rather than tidied, since the commits are
pushed; the write-ups above carry the numbers that are actually free.

## #406 - claimed by the app tree, 11 Sep 2026: a range's two ends move into a popover, so the Restriction column stops reserving room for fields almost no row uses. Roberto's design, and it supersedes three rounds of shrinking those boxes (#391 grew them, #404 shrank them twice) - all of which treated the symptom. At rest the cell is the menu alone plus a compact chip of the values; editing happens in the popover. No docs work. Write-up in `Application/v9/repos/local/NEXT.md`

## #404 - claimed by the app tree, 11 Sep 2026: the Numerical Solver's number fields are sized so the Restriction column stays on screen. In Complex mode a row carries two boxes and a Domain menu, which pushed Restriction off the right edge; the pair drop to 4.8rem and the range's ends to 4rem, with the j kept beside its box rather than stacked above it. Both reported from the live site with screengrabs, and both measured rather than eyeballed: Complex with a range open went from 37px of overflow to none at 950px. Partly walks back #391, which had grown the range ends to a full value box when Restriction still had the row to itself. No docs work. Write-up in `Application/v9/repos/local/NEXT.md`

## #400 - claimed by the app tree, 11 Sep 2026: the offline builds say which build they are, and offer a reload when a newer one has installed behind them. Neither page could answer "which version am I looking at", so a stale cache and a not-yet-deployed change were indistinguishable - and on 11 Sep that ambiguity cost four exchanges, with the wrong diagnosis given in both directions. A build stamp on the Solver (the app has one; the Solver never did) and an update notice driven by the service worker's own controllerchange. Not an auto-reload: it would discard a typed circuit. No docs work. Write-up in `Application/v9/repos/local/NEXT.md`

## #399 - claimed by the app tree, 11 Sep 2026: the Numerical Solver's two modes are named Real and Complex, not "DC - real" and "AC - phasor". Roberto, on learning that all four domains hand over: FD rides the complex mode and TR the real one, so naming them after two of the four circuit analyses misdescribes what they are. The payload's own `mode` values stay dc and ac - that is the contract, not a label. No docs work. Write-up in `Application/v9/repos/local/NEXT.md`

## #398 - claimed by the app tree, 11 Sep 2026: the Numerical Solver's equation list drops its Variables column and lets What it is wrap, and both tables scroll sideways at any width so no control can sit past the edge unreachable. Roberto: the Variables column "doesn't add much". No docs work. Write-up in `Application/v9/repos/local/NEXT.md`

## #396 - claimed by the app tree, 11 Sep 2026: the Solver's two panels stack, equations above variables, and a range's two ends sit on their own line. Measured, not chosen: side by side the variable table wanted 721px in a 613px column, putting a range field 61px past the window. Also fixes a label shape regression - a system saved between #393 and #395 carries the old object form and rendered an empty What it is column, because a saved file outlives the build that wrote it. No docs work. Write-up in `Application/v9/repos/local/NEXT.md`

## #397 - claimed by the app tree, 11 Sep 2026: a Copy pill beside each field of the SPICE Translator, so a translated netlist goes to the clipboard without selecting it by hand. The app already had this logic once (the two-port parameter term), so it is factored out rather than written twice. Same idiom as the docs' own Copy pill (#313). No docs work. Write-up in `Application/v9/repos/local/NEXT.md`

## #395 — claimed by the app tree, 11 Sep 2026: the Numerical Solver handover stops needing a file. The app and the Solver are same-origin in every build, so a system too large for a URL goes through localStorage instead of a downloaded numerical_system.json. The URL stays the path for short systems because a link is shareable; the file survives only as a last resort. #393 is what forced the issue — its labels quadrupled the payload and pushed an ordinary circuit over the 6000-character cap — so the label encoding is trimmed in the same item. No docs work. Write-up in `Application/v9/repos/local/NEXT.md`

## #394 — claimed by the app tree, 11 Sep 2026: the Numerical Solver is wider (92rem, was 76) and the equations column takes the larger share of the split, with the stack breakpoint raised to 68rem. Roberto while testing #391: *"Feel free to make the equations card/column wider. You can even put them equations above and results below."* Kept side by side, because the page's loop is ticking an equation and watching the variables answer. No docs work. Write-up in `Application/v9/repos/local/NEXT.md`

## #393 — claimed by the app tree, 11 Sep 2026: every equation handed to the Numerical Solver carries a label saying what it is — *nodal equation for node 3*, *element equation for voltage source e1*, *power equation for resistor r1*, *expert mode equation* — so the checkbox list distinguishes the stamped system from the expert extras from the third level. Roberto's ask while testing #391. Needs the engine to record each stamped equation's provenance, which it does not today. No docs work until it ships. Write-up in `Application/v9/repos/local/NEXT.md`

## #392 — claimed by the app tree, 11 Sep 2026: a chained comparison — `7 > x > 3`, the way anyone writes a range — is accepted wherever conditions are typed (Expert Mode, the Solve card, the Evaluate card). All three parsers split on the first operator they met, so the second half reached a value parser that refuses comparisons. One splitter in the solver now, imported by the other two. **Solver change, so a release**. No docs work unless a chapter states the old limitation — worth a grep for condition syntax before the next docs pass. Write-up in `Application/v9/repos/local/NEXT.md`

## #391 — claimed by the app tree, 11 Sep 2026: the third level crosses into the Numerical Solver — the defining equations for power, branch voltage and a source's seen resistance, behind a checkbox on the app's Numerical Solver card (off by default). No docs work now; **a follow-up may be wanted once it ships**, since the Manual's Numerical Solver part names that card's controls. Write-up in `Application/v9/repos/local/NEXT.md`

## #390 — the Manual: a second book on version 9 — **done 11 Sep 2026, live on `learn.symbulator.com`**

Fourteen parts, 6,384 words, 22 circuits. The Course is 49,712 words and
297 worked problems, so the Manual is about an eighth the length and a
thirteenth the examples, over the same ground plus four features the
Course never mentions.

**The architecture, and why it is not a fourth version.** `build.py` has
thought in versions since it was written, and the routing is hard-wired to
`^([789])`. A fourth pseudo-version would have to pass through every
`versions:` check and every `{{v7,8|…}}` span — exactly the machinery that
must not break 7 and 8. So a chapter names its book in front matter,
`book: manual`, defaulting to `course`, and the split happens in the
renderers. **Versions 7 and 8 are untouched by construction**, not by
care: every Manual chapter is `versions: [9]`, so `for_version(7)` never
sees one. Measured — v9's toc carries 21 course chapters and 14 manual;
v7 and v8 carry 15 course and zero manual.

**The change that would have bitten.** Nothing stopped the Manual's
fourteen parts from being swept into `symbulator-v9.pdf`: the TeX renderer
walks `for_version(9)` and takes what it finds, and the Manual is version
9 material. The three tutorial PDFs are filtered to the Course now — 21
chapters of 35 — and the Manual gets a PDF of its own when Roberto calls
it final.

**The pager was the same shape of bug, found by asking what the flat list
does at a boundary.** The credits' *next* turned the page into Part 1 of a
different book and Part 1's *previous* turned back into the credits. It
stays inside its book now.

**Invented examples needed a guard.** The Course's 297 answers are checked
against printed textbook answers; an invented circuit has nothing behind
it but whoever typed it. `tools/check_manual_examples.py` requires every
```field 9 Circuit Description fence in a `book: manual` chapter to parse
and to solve, and `build.py --check` runs it, because a guard nobody runs
is not a guard. Every printed `::: result` panel was *generated* from
`symbulator_ui` and pasted, not typed.

**Proved red, and the failures were instructive.** A grammar sabotage was
caught immediately. The solve half took three attempts, and the first two
"misses" were the test asserting the wrong thing rather than the guard
failing: renaming a node to 9 only makes an island, which the solver gives
its own reference on purpose since #320; and a voltage source in parallel
with a resistor and a current source is an ordinary solvable circuit. The
third case was verified unsolvable in all four domains *before* being used
as a test, which is the order it should have been done in.

**What the writing itself caught**, all by running rather than re-reading:
the load control is *"Are you running a problem with a load connected to
this equivalent circuit?"*, not the wording invented for it; `pmax` is one
of the Thévenin tool's four base answers, not one of the three the load
tick adds; a transformer's terminal currents are `it11` and `it12`, the
element name then the node name; a two-port's are `iz1a` and `iz1b`.

**And one claim about the build that was wrong twice before it was
checked.** A manual chapter was never going to render as "Lesson 14":
`for_version` numbers only `kind == "lesson"`, so `number` stays None and
`eyebrow_for` returns an empty string. They carry *Part 1* … *Part 14*
now, numbered in their own sequence beside the lesson numbers and the note
letters.

**`static_preview.py` drifted again**, exactly as its own comment warns in
capitals: it writes its own banner and its own `<head>` and reads nothing
from `index.php`, so every Manual part was marked COURSE and titled
*Symbulator 9 Course*. Caught by looking at a rendered page. Its `_mark`
takes the page id now. Verified on four cases: a Manual page says Manual,
a Course page Course, a version 7 page Documentation, and the chooser —
which is in neither book — Documentation.

**What cannot be verified here.** The chooser, the three-group home page
and the sidebar's Manual rule all live in `index.php`, and there is no PHP
on this machine. Tag balance was compared across the edit (102/102 before,
120/120 after) and the logic was exercised through the Python mirror, but
the rendering is unproven until it is served. The deploy guard is the one
#389 describes: capture `/7/` and `/8/` before, diff byte for byte after,
identical or revert.

**Live, and verified by fetching.** All fourteen parts return 200 in
version 9 and 404 in both 7 and 8; the chooser, the three headings and the
per-book property mark are all served as intended — a Manual page says
Manual, a Course page Course, and the chooser, which is in neither book,
Documentation. The three card grids fill with no short row: 15 cards in 5
rows, 6 in 2, 14 in 5, measured on the live page.

**Versions 7 and 8 were proved unmoved, and the rule needed refining.**
Six pages were captured before the deploy and re-fetched after. They are
*not* byte-identical, and the guard was right to say so. Two differences,
both benign and both worth knowing:

* the shared `style.css` is cache-busted by content hash, so adding the
  chooser's rules changed the query string on **every page of every
  version**;
* the sidebar's HTML indentation shifted where the Manual's `<?php ?>`
  block went in.

Normalised for whitespace and that hash, all six pages are identical; the
visible text is identical; and the word *chooser* appears nowhere in a
version 7 or 8 page.

**So the standard is "semantically identical", not "byte-identical".** A
byte diff is still the right first test — it is what surfaced both of
these — but a shared stylesheet makes zero unreachable, and a rule that
can never be met is one that gets waived rather than applied.

**Not done, deliberately:** the Manual's own PDF, which Roberto asked for
*when it is final*.

---

## #389 — version 9's book is the Course — **built, deliberately not deployed**

Roberto, 11 Sep 2026, deciding the names for a second, shorter book: the
tutorial becomes the **Course** and the concentrated guide will be the
**Manual**. His landing page had already drawn the line — *"A course, not
a manual."* — three weeks before he asked for one.

The hard constraint came with it: *"Nothing here should be reflected or
break 7/8, which remain parallel versions of the tutorial."*

**Measuring first turned this from a rename into three conditionals.** All
three naming sites were version-blind: 7, 8 and 9 served the same
*Symbulator Tutorial* heading and the same *Documentation* property mark,
verified by fetching all three live pages. Two variables now carry it,
computed once near the top of `web/index.php` so a later edit cannot move
one site and miss the others:

    $bookName     = ($v === '9') ? 'Course' : 'Tutorial';
    $propertyMark = ($v === '9') ? $bookName : 'Documentation';

Four sites read them: the tab title, both spellings of the property mark,
and the section heading. The Manual does not exist yet, so version 9 says
*Course* everywhere; `$bookName` is the single place that learns to tell
the two apart when it does.

**What did not need touching, measured rather than assumed:** `book.yaml`'s
title is plain *Symbulator*, so the three PDF covers name no tutorial and
no PDF is version-gated; the app's ribbon link is keyed
`documentationdocs.2612` and says *Documentation* in all thirteen
languages, so there is no i18n work and no app work; and the `learn`
target's `verify_pages` markers are stylesheet paths, `class="shell"` and
*Symbulator 8*, none of which this touches.

**`tools/static_preview.py` was mirrored, because its own comments say to.**
It writes its own `<head>` and its own banner and reads nothing from
`index.php` — the drift that once left the preview showing a superseded
header for a day. It carries a `_mark(toc)` helper now. It does not render
the section heading at all, which is a pre-existing gap from #380/#381 and
is left alone.

**The thing to know before deploying this: it cannot be tested here.**
`index.php` is PHP, this machine has none, and the file ships verbatim into
`build/web` — so the build-and-diff trick that proved versions 7 and 8
unmoved on #386 would pass trivially and prove nothing. What was done
instead:

* the **Python mirror** was run, and it is the same condition: the preview
  builds *Symbulator 7 Documentation* / *Symbulator 8 Documentation* /
  *Symbulator 9 Course*, with the marks to match;
* the PHP **tag balance** was compared before and against after — 99 opens
  and 99 closes before, 102 and 102 after, the delta exactly the three
  `<?= e(...) ?>` added. The before-count matters as much as the after: a
  balance checker that cannot see the known-good file as good is measuring
  something else, which cost three readings on an earlier item;
* the three insertions were compared against the **53 interpolations
  already in the file** and are byte-identical in form to `<?= e($v) ?>`.

**The guard for the eventual deploy** is capture-and-compare, and it runs
after the change is live because nothing else can: fetch and store `/7/`,
`/8/`, `/7/lesson-dc` and `/8/lesson-dc` before deploying, fetch the same
four after, and diff byte for byte. Identical or revert — not "one blank
line", since none of their sources change at all.

**Not deployed, at Roberto's word:** *"Nobody uses the website yet, so
rename now and ship later."* It ships with the Manual.

**Still to come, and deliberately not built yet:** the chooser, first thing
on `/9/`, in his words — *The Manual, you already know circuit simulation;
The Course, you are new to circuits or to simulation.* A chooser with one
live option is worse than no chooser, so it waits for the Manual. The
coverage inventory behind all of this is the artifact published the same
day: 59 theory topics, 52 within version 9's reach, and four features that
ship and are named nowhere — the Numerical Solver, the SPICE Translator,
multiple solutions, and the DC sweep plot.

---

## #388 — Tech Note F, every control in the Settings card — **built, not deployed**

Roberto, 11 Sep 2026: *"A5. … the Settings card to another technical
note."*

**This one is new writing, not a move, and that was flagged before it was
written.** {{card:Settings}} is named in eight chapters and always in
situ — one control at a time, where that control is first needed. There
was no block to lift out, and taking those mentions away would leave a
lesson saying "open Settings" with no idea what is in it.

So the note is the *whole card in one place*, written from the app's own
markup rather than from the chapters' prose: `templates/index.html`'s
Settings `<details>` for the controls and their defaults, and
`syncSettings()` for why the two AC controls disappear outside AC and
keep their values while hidden.

Two claims in the draft were checked rather than asserted, and both
needed correcting:

* **The RMS convention.** The draft said the two conventions differ by a
  factor of two and did not say which way. Solved both ways through
  `symbulator_ui` on `e,1,0,10:r1,1,0,5` at 1 krad/s: peak reports 10 W,
  RMS 20 W. The answer's *label* moves too — *average power* with the
  tick off, *power consumed* with it on — which no lesson says and which
  a reference page is exactly the place for.
* **Micro.** The solver takes three spellings, not the two the table
  prints: `'u`, MICRO SIGN `'µ` and GREEK SMALL LETTER MU `'μ`
  (`si_prefix.py`'s `_SI_PREFIXES`). The last two are indistinguishable
  on screen, so listing all three in a table would read as a typo; both
  notes say instead that either mu works.

Lesson 1 gained a pointer where a reader first opens the card. Nothing
was removed from any lesson.

---

## #387 — Tech Note E, the SI prefixes — **built, not deployed**

Roberto, 11 Sep 2026: *"A5. Move the SI prefix table to a technical
note."*

The eleven-row table moves. What stays in Lesson 1 is the sentence
saying what the apostrophe shorthand *is*, and the `::: tip` beside it —
both shared with versions 7 and 8, and both load-bearing: the very next
circuit description in that lesson contains `1'k`. It is the *list* that
is reference material, not the idea.

The four spellings of 8 kΩ went with it, but only for version 9: the
sentence is now `::: only 7,8` as it stood plus an `::: only 9` rewrite
that points at the note, so 7 and 8 read exactly what they read before.

The table was checked against `symbolator/si_prefix.py`'s
`_SI_PREFIXES` — eleven prefixes, peta to atto, kilo taking `'k` or
`'K` — rather than copied forward on trust.

---

## #386 — Tech Note D, the equivalent circuit and its example — **built, not deployed**

Roberto, 11 Sep 2026: *"A4. Keep the checkbox but move the 'equivalent
circuit', with its example, to the technical note."*

The checkbox stays: the load question is what produces `irl`, `vrl`,
`prl` and `pmax`, and those are core Lesson 4. What moved is the
{{btn:Load circuit equivalent?}} button under the answers, and RM3's
Example 9-8, which exists to demonstrate it.

**The 7/8 copy could not move and did not.** A note is `versions: [9]`,
and the calculator's `eqcir` string is versions 7 and 8's own feature,
described in their own words. So the worked problem was wrapped in
`::: only 7,8` rather than deleted — 7 and 8 keep it exactly as it
reads today, and version 9 meets it in the note.

**The build caught the half-done state, by line number.** Wrapping the
problem left six pieces of version 9 material stranded inside it —
three `::: only 9` blocks, two `field 9` fences and an `::: applink` —
and `build.py --check` named every one: *a ```field 9 panel is inside an
::: only 7,8 block, so version 9 never sees it*. That guard is the
reason this restructure was safe to attempt at all.

---

## #385 — Tech Note C, the two jobs of the underscore — **built, not deployed**

Roberto, 11 Sep 2026: *"A2. Move it to a technical note"*, and then
*"you can move the 'underscores for pretty print that matches the look
of the book' example to the technical note."*

Same character, two meanings, two chapters, and neither chapter was
about notation: Lesson 1 said an answer's name may carry an underscore
or not, Lesson 3 said an underscore in a *symbolic value* makes a
subscript. Both move; each lesson keeps a pointer, and Lesson 3's sits
where the aside was, at the problem whose printed answer prompted it.

**Both `::: result` panels were checked against the app.** A result panel
is hand-written LaTeX and nothing in the build compares it with what
Symbulator returns — which is how TR5's Example 4.5 printed a wrong
subscript for as long as it existed (#370), and this note's whole subject
is how an answer is spelled. Both circuits were solved through
`symbulator_ui.solve_ui` and both panels match, once the book's `\beta`
and the app's literal `β` are normalised against each other.

The comparison also turned up something the note had not said: in the
*plain* circuit `re1` still prints as *r*<sub>e1</sub>, because trailing
digits are subscripted anyway (#274). A reader holding the two panels
side by side would have seen a subscript in the one that is supposed to
have none and concluded the note was wrong about its own subject. It is
named in one sentence now.

**A first attempt at the Lesson 3 cut left an unclosed directive.** The
end of the block was computed by counting `:::` lines forward from the
result panel; the block ends with three of them and the arithmetic took
the wrong one. `build.py` refused the build. The replacement matches the
whole block verbatim instead, so there is nothing to count — and the same
rule was applied to #386's much larger cut.

---

## #384 — `--check` read a nested version wrapper as if it were in every version — **fixed**

Found by #385, and it had been true since version filtering existed.

`check()` filters the top level with `walk(ch.blocks, v)`, which drops an
`only`/`not` wrapper whose versions do not include `v`. `_check_block`
then recursed with a bare `for c in b.children`, and *that* recursion knew
nothing about versions. So the moment a version wrapper sat inside another
directive, everything in it was checked against all three books.

The symptom was a cross-reference. Lesson 1's `{{ref:underscores}}` is in
a top-level `::: only 9` and passed; Lesson 3's identical pointer is in an
`::: only 9` inside a `::: problem`, and was reported as an unknown label
for v7 and v8 — where the reference does not exist and neither does the
note.

Version wrappers are dropped on the way down now. **Code fences
deliberately stay unfiltered:** the unknown-version guard above them must
run wherever the fence is, and a fence tagged `10` is kept by no version
at all, so filtering it there would have retired that guard silently —
the narrowing would have been invisible.

**Proved red on purpose, three ways**, since `check: clean` is also what a
checker that has stopped looking prints. A bogus reference planted inside
a `::: problem`: bare, it must be caught in 7, 8 and 9; inside `only 9`,
in 9 alone; inside `only 7,8`, in 7 and 8 alone. All three came back
exactly right, and the file was restored afterwards and re-checked clean.

---

## #383 — a technical note may carry worked examples — **done**

Roberto, 11 Sep 2026: *"May be good to give all technical notes the
ability, in principle, to carry examples."*

A chapter's worked problems get their **Open in app** links by matching
each problem's title against the entries of that chapter's example
book(s). Which books those were was a hard-coded map keyed on chapter id,
`CHAPTER_BOOKS`, listing the thirteen lessons — so a note's problems found
no pool and rendered without links, **silently**, which is the part that
made this worth fixing before writing any note that needed it.

A chapter may now name its own books in front matter:

    books: [4a, 4b]

The map stays as the default for the lessons, where thirteen ids beside
thirteen books reads best. A note says it in its own file, which is where
*that* reads best — the note is the thing that moves, and a note moved
away from a map entry would lose its links without a word.

**The coverage report needed the same change and did not get it at
first.** `app_links.py --self-check` still walked `CHAPTER_BOOKS` alone,
so the two entries Tech Note D links came back as *claimed by no problem*
while the built page carried working links to both. That is the worse
half of a stale guard — not a miss but a false alarm, and a report with
known-wrong lines in it stops being read. It reads a chapter's own
`books:` now, and pools claims across chapters, since a book can be
claimed from two places and an entry claimed by either is claimed.
Coverage went from *331 of 336* to *334 of 336*; the three are the
entries the notes took.

The change was proved behaviour-neutral for the lessons before anything
depended on it: the per-lesson app-link counts were unchanged.

---

## #382 — the Introduction points at Tech Note A, and says it is optional — **done 11 Sep 2026, live on `learn.symbulator.com`, all three PDFs rebuilt**

Roberto, 11 Sep 2026: *"find a pertinent place in the documentation … to
tell the reader to go read the Technical Note A if they are interested in
learning how to use input files. Make sure you mention it is optional."*

The place chose itself. The Introduction's **Built-in examples** section
already handed off to that chapter — it is where a reader first meets
loading an example — but it said nothing about the chapter being
optional, and since #380 it is not a pseudo-lesson between the
Introduction and Lesson 1 any more but a note in a section of its own.

Both are said now: that it is a technical note, in the section of that
name at the end of the tutorial, and that **nothing in the lessons
depends on it** — every lesson can be followed without saving a file.

**The letter is deliberately not in the prose.** `{{ref:}}` renders a note
by its title, and the letter is assigned by position, so "Tech Note A"
written into a sentence goes stale the day a note is inserted before it.
The *section* is named instead.

It sits inside the existing `::: only 9` block, so versions 7 and 8 —
which have no technical notes — are untouched, and the built v7 page
carries no mention of it. One added sentence changes the typeset text, so
this was a full `python build.py` and a PDF redeploy, not `--web`; all three
are byte-identical live to the local build.

---

## #381 — a heading over the lessons, and no partial row anywhere — **done 11 Sep 2026, live on `learn.symbulator.com`**

Two asks from Roberto after seeing #380 live.

**A heading for the tutorial.** The lessons carry the same small-caps
label the notes do — **Symbulator Tutorial** — so the two sections are
named the same way. No rule above it: the nav band's own border already
closes the space, and a second line 1.4rem under it read as a double
rule. All three versions get it; only version 9 has notes below.

**Every row fills.** Roberto: *"if there is only one box in a line, it
expands to occupy the full line … make sure that it's always like
that."* The grid now has **six** columns and a card spans two, three or
six by breakpoint. Six divides by both three and two, so an orphan spans
the row and a pair splits it — which `span 1.5` could not. Which card
stretches is `:nth-child` arithmetic on the count, so it needs nothing
from PHP and stays right when the column count changes under a media
query. The two-up breakpoint is a **range**, not a `min-width`: with
fifteen cards the last is an odd child, and a stray
`:last-child:nth-child(2n + 1)` would have stretched a row that was
already full. The `:only-child` and `:has()` special cases #380 added are
gone — they were special cases of this rule.

**`kind` decides the order now, not `book.yaml`.** Roberto asked whether a
note listed before Lesson 1 would still render at the end. It would not
have: `kind` grouped the home page cards, because that loop filters,
while the sidebar, the Previous/Next pager and the three PDFs followed
`book.yaml` literally — a note listed first would have **printed** first,
and the sidebar would have opened with a "Technical Notes" separator
above the Introduction, that separator being emitted at the first note
the loop meets. Chapters are sorted by kind once at load time now,
stably, so the author's order within each group is kept and the answer
to his question is yes. Proved by listing the note first and rebuilding:
the rendered order came back unchanged.

**How the grid was tested, since `index.php` cannot be rendered here.**
The rule is pure CSS, so it was exercised directly: every card count
from 1 to 9 and 13 to 17, at each layout, asking of the **laid-out
boxes** whether the last row's widths sum to the grid's own. Two
attempts before one meant anything:

* the first resized the pane, which does not reach the page here — every
  probe reported `innerWidth: 980`, so it measured the three-up layout
  three times and called it three breakpoints;
* the second put the layouts side by side in narrow columns, which made
  the **control** degenerate: at 300px the old `auto-fill` rule yields a
  single column, where every row is trivially full, so the known-bad
  case passed.

Full width, one layout per page, the control finally failed as it
should. **The old rule leaves a partial row on 10 of the 14 counts**,
short by 631px where one card is left over and 316px where two are; the
new rule leaves none. A control that cannot fail proves nothing about
the test.

---

## #380 — Technical Notes: a section of their own, under the lessons — **done 11 Sep 2026, live on `learn.symbulator.com`, all three PDFs rebuilt**

Roberto, 11 Sep 2026: *"there are some topics that are optional and can
be dry, but need to be covered in the documentation ... that category
could be called Technical Notes"*, and on the symptom: the *Working with
input files* chapter *"sits awkwardly as a pseudo-lesson between the
Introduction and Lesson 1 ... it's ruining the symmetry of the rectangle
where lessons are kept, because it pushes all the lessons and the
credits end up on a line of their own."*

**The grid was doing arithmetic, and it backed him up.** The home page
tiles `repeat(auto-fill, minmax(17rem, 1fr))` in a 66rem container --
three columns at full width. Versions 7 and 8 have 15 chapters, which is
3 x 5 exactly; version 9 had 16, and the sixteenth left the credits
alone on the last row. **7 and 8 were the control group**: the same
stylesheet, one card fewer, no complaint.

**What shipped.** A third `kind`. Every chapter already declared `front`,
`lesson` or `back` and `build.py` already parsed it -- the only reason
the page could not group by it is that `kind` was never copied into
`toc.json`. Notes are ordered in `book.yaml` after the lessons and before
the credits, so **the printed book, the sidebar and the home page all
read in one order** and the grouping is purely a rendering concern.

* `src/00b-input-files.md` -> `src/14-note-input-files.md`, `kind: note`.
* `build.py`: one `eyebrow_for()` that three renderers ask -- the HTML
  chapter head, the TeX one and `toc.json`. Notes are **lettered, not
  numbered** (Roberto's call): they have no reading order and a number
  would imply one. `for_version` assigns the letter beside the lesson
  number so the two sequences cannot drift.
* `tex/symbulator.cls`: a `\technote` macro -- unnumbered like a front
  chapter, but labelled in the accent small caps a lesson number wears,
  and carrying "Tech Note A" into the contents and the running head.
* `web/index.php`: both loops split on the kind; the notes render under a
  rule on the home page and under a labelled separator in the sidebar.

**The wrinkle only a rendered mock could show.** With fewer notes than
columns, the card grid's rule-coloured background showed through the
empty cells as a **grey void** -- which the lessons grid never hits,
being always full. A lone note now spans the row and reads as a wide
card; two split it; three or more tile as the lessons do. That was
invisible in the markup and obvious in the picture.

**Verified live by fetching**: v9's main grid is **15 cards** with the
Technical Notes section below it and `Tech Note A` on the card; v7 and v8
are 15 cards with no section and no separator; `/9/input-files` carries
the eyebrow and its pager now runs Two-ports -> Working with input files
-> Roll the credits. All three PDFs were rebuilt -- **this changes what
the typeset text says, so it was a full `python build.py`, not `--web`**
-- and each is byte-identical live to the local build. Page counts are
unmoved at v7 **235**, v8 **223**, v9 **300**: the chapter travelled, it
did not grow.

**One honest limit.** The 3 x 5 is a desktop-width property. Below about
51rem the grid drops to two columns and 15 leaves an orphan anyway. The
durable win is that nothing dry sits between the Introduction and Lesson
1 and the lessons form a block of their own.

**A note for the next one.** There is no `php` on this machine, so
`index.php` cannot be linted before a deploy, and a parse error there
500s every page on the site. What stood in for it:
`scratchpad/check_php.py`, a balance count of the alternative-syntax
`foreach`/`endforeach` and `if`/`endif`. **Three versions of it read the
committed file as unbalanced before one read it correctly** -- and a
checker that cannot see the known-good file as good is measuring
something other than balance. Run it against `HEAD` as well as the
working tree, every time.

---

## #365 — the Book gets its figures, and `book.pdf` on the site with them — **done 10 Sep 2026, live on `learn.symbulator.com/book.pdf`**

Roberto, 10 Sep 2026: *"I had not realised that the PDF has no images."*
It had none by design -- the Book's own *Note on this Edition* said the
figures "are not reproduced in this edition", on the reasoning that a
problem's circuit is fully defined by its description. He reversed that,
so the note was rewritten as well; leaving it would have had the book
contradicting itself in print.

**The figures were never lost.** They are embedded in the original Word
chapters under `paper/references/2000_thesis/`, and `carve_png.py` pulls
them out signature-to-`IEND`, so the extent of each is exact: **150
images, none corrupt**, splitting cleanly into 60 calculator screens
(59 at exactly 164x104) and 90 drawings. 93 figures now sit in the Book,
one per problem that has one.

**Five problems have none, and the thesis says so itself** -- 048, 057,
059, 060 and 072 each open *"Este problema no tiene figura."* That is the
whole gap; nothing is missing that the source has.

**Edited the source, not the PDF.** `build.py` copies
`paper/the_symbulator_book.pdf` to the site as `book.pdf`, so uploading a
rebuilt PDF alone would have been undone by the next `xelatex` --
the generated-files-are-not-source trap this file's parent `CLAUDE.md`
already names. `thesis_circuits/illustrate_book.py` puts the figures into
`paper/book/ch*.tex` and the packages into the main file, once, and
refuses to run twice.

**The pairing is the delicate part, and it was wrong three times**, each
found by Roberto reading the comparison sheet rather than by any check of
mine. All three are written up in `paper/thesis_circuits/README.md`; the
short form is that Word stores a picture per *appearance*, so counts lie:
a figure embedded twice ate a problem's slot; a caption the matcher could
not see (the extraction spaces characters out, `F i g u r a 4 1 .`) hid
**14** figures; and classifying screens by an open-ended word list meant
every word missed stole a circuit's slot. The last one is the lesson:
**key on the closed set.** The thesis always writes *"Circuito para el
Problema N NNN"*, and everything else is a screen.

Verified by fetching: `learn.symbulator.com/book.pdf` is **143 pages with
93 images**, sha256-identical to the local build, and its editorial note
reads *"are reproduced in this edition"*. It was 117 pages and zero.

Two companion editions exist but are **not deployed and not linked**:
one with every description converted to version 9 notation (for Antony
Garcia), and one with every circuit redrawn by the v9 schematic engine
for comparison. `py thesis_circuits/build_thesis_pdfs.py` rebuilds all
three; `check_pdfs.py` proves they differ in the two axes they should.

## #364 — claimed by the app tree, 10 Sep 2026: a tools housekeeping item — `review_schematics.py` took `--help` as its output directory and had committed 3.5 MB into a folder of that name. No docs work. Write-up in `Application/v9/repos/local/NEXT.md`

## #363 — claimed by the app tree, 10 Sep 2026: Lesson 5's Practice Problem 5.7 gets the app entry it never had, so the chapter's only link-less problem carries **Open in app** and **Open in split view** like its neighbours. No docs source changes — the links row is generated from the title match, so the fix is one entry in `Application/v9/repos/server/examples/Lesson_05b.cir` and the page gains its row on the next build. Write-up in `Application/v9/repos/local/NEXT.md`

## #370 — the underscore trick, and a result panel that disagreed with the app — **done 10 Sep 2026**

Roberto, 10 Sep 2026, reading Lesson 3 entry 48 on the live app: *"the
answers in the Results section would look more similar to the answers in
the book if the symbolic variables used in the description carried an
underscore. This is a nice tip."*

So TR5's Example 4.5 (Symbolic) keeps its own description and gains a
closing note, version 9 only: put an underscore in a symbolic value's
name and everything after it is set as a subscript. The note carries the
alternative description as a **Circuit Description** box — `v_cc`, `r_b`,
`v_γ`, `r_e1`, `r_c` — and the answer it produces as a result panel.

Version 9 alone, because the trick is about *typesetting* an answer, which
is the thing the calculator books cannot do.

**The answer in that panel was solved, not transcribed.** Roberto sent a
screenshot; the underscored description was driven through `/api/solve`
and the LaTeX the card returns was read back. It matched the screenshot,
denominator order included — but running the *chapter's own* description
at the same time is what found the real bug.

**The result panel already on that problem disagreed with the app.** It
read `re_{1}\,\beta + re_{1} + rb`, subscripting the `1` onto `re`; the
app returns `r_{e1} \beta + r_{e1} + rb`, subscripting `e1` onto `r`.
Roberto ruled: *"re_{1} was wrong, r_e1 was right."* Corrected.

**Why it matters beyond one panel.** #276's rule is that a `::: result`
panel shows the card answer *as the app shows it*, and the panel is
hand-written LaTeX — so nothing checks it. This one had been wrong since
it was written, and it was found only because a note about something else
made someone run the circuit. A sweep for the same shape
(`re_{1}`, `rb_{1}`, `rc_{1}`) across all fourteen chapters found no
others.

**Worth knowing about the cause:** the value is spelled `re1` and the
element is *also* named `re1`, so the symbol reaches the answer through
the answer-name canonicaliser as `r_e1`. That is why the app prints an
underscore the description never had — and it is why the underscore trick
reads so naturally here in the first place.

## #369 — the two notes that were rules, applied as rules — **done 10 Sep 2026**

Roberto, 10 Sep 2026, after #368 shipped: *"For the comments that are
generalisable to rules that apply across the whole documentation, did you
do that? I didn't mean for them to be specific for those passages."* He
was right about two of the eight, and the answer was no.

**A tool gets its own tier.** `{{tool:pr}}` joins #357's places and
controls and #361's buttons, with a `ui-tool` token through all three
copies of the palette and a `\uitool` macro. **Violet**, `#7c4d9a` light
and `#c9a3e8` dark — the fourth hue, clear of the blue places, the teal
settings, the salmon buttons and the red answers.

**The measurement changed the job.** The first scan said 66 bare `port`s,
20 `th`s and so on; almost all of it was noise. Stripping bold as well as
code showed what was really there: **the book already had a convention**,
a tool name set `**bold**`, used consistently — and #368 had broken it by
setting Lesson 3's two mentions as `` `pr` `` in code, a third style.
What was genuinely unformatted was **six** mentions in the whole book.

So the conversion is **27 bold names** plus **11 unformatted or
miscoded** ones. Bold was the right instinct and the wrong marker: it is
also what a node name, an element name and a symbolic value wear (#267,
#302), so *run **dc** on **r1*** said the two were the same kind of word.

**Where the tier actually lands, measured per version:**

| | spans | |
|---|---|---|
| 7 and 8 | 32 each | `th` 9, `er` 7, `pr` 5, then `dc`, `ac`, `fd`, `port`, `solve`, `tr`, `plot` |
| 9 | **11** | `pr` 6, `ac` 2, `dc` 1, `pr()` 1, `fd` 1 |

**That inversion is deliberate and Roberto checked it on purpose.** Every
other tier is version 9 only; this one is three times commoner in the
older books, because *script* is calculator language — *"An easier way is
the **th** script"* renders 5 times in 7 and 8 and **zero** times in 9.
He asked exactly that question and accepted the answer: *"I have
absolutely no problem with the higher frequency in v7 and 8. I just
wanted to make sure that v9 was not using those words."*

**Version 9's *"Run it in DC"* stays plain**, five times over. That names
the analysis in prose rather than calling the tool, and it is the main
reason version 9's count is low. Revisit only if the distinction stops
reading.

**A caution about the sample that sold it.** The strip sent for approval
put four tiers in one sentence — *"the **th** script: open **Settings**,
tick **Show equations** …"* — which is 7/8 wording stitched to version
9's UI names, a sentence neither book contains. Roberto spotted it in two
questions. **A colour sample should be built from a real paragraph**, not
a composed one; the composition is what hid the version split until he
asked.

**Every problem named in prose links back to it.** The rule he meant in
#368, applied to the book: **12 mentions** in three chapters, ten of them
in Lesson 6. The scan sorted 95 candidates into three kinds and only one
was the rule:

| | count | what happened |
|---|---|---|
| figure captions, a bare line naming the example | 83 | left alone; the caption is the label |
| prose cross-references | 4 | bold and linked |
| the opening line of a problem, restating the textbook's question | 8 | bold and linked, at his word |

The second scan is the one to keep: the first counted a caption as a
prose mention and reported 95 sites, which would have put a link inside
every figure label in the book.

**A reference now reads as the prose does.** A problem's title often
carries a qualifier the chapter added — *(Op Amp)*, *(Exponential)*,
*(Hidden source)* — and the prose never repeats it. So a problem
reference drops a trailing parenthetical, **unless dropping it would make
two problems read the same**. Measured first: 296 problem titles, exactly
one collision (AS2's Figure 5.24, once *(Subtractor)* and once
*(Difference or Differential)*), and that pair keeps its qualifiers.

Zero plain prose mentions remain, by the same scan that found them.

**Numbering:** this item and #368 were first written as #364 and #365,
which the app tree had already spent that morning (#363–#367). Renumbered
before anything shipped. The sequence is shared between the trees and
this is the second time it has collided — read both files' heads before
taking a number.

## #368 — a subsection and a worked example can be linked to — **done 10 Sep 2026, source only**

Roberto, 10 Sep 2026, with eight notes on Lessons 3 and 4. The one that
needed building: *"make the example name bold and include a link to that
problem. If you have not done so already, create an anchor in each
section, subsection and example."*

**The anchors already existed; nothing could reach them.** Every heading
gets an anchor at parse time and every `::: problem` has carried a
`prob-<slug>` id since #224 — but `Book.labels`, which is what `{{ref:}}`
resolves against, registered chapters and `##` headings and nothing else.
So the markup could point at a lesson or a section and never at a
subsection or an example.

`labels` now registers `###` headings and every problem. A problem's
display name is its own title with the version spans resolved, so
`{{ref:prob-b11s-example-74}}` prints *B11's Example 7.4* and links to it
across chapters.

**The bug on the way in, and what it says about `walk`.** The first cut
registered the two subsection headings and **none** of the problems.
`walk()` flattens the version and medium wrappers but hands back every
other block whole, and a worked problem lives inside a `::: practice`
block — so a flat walk never meets one. `walk_deep()` descends, in
document order, which is the order the renderer's `prob-` counters
follow.

**Two anchor computations now have to agree**, `labels`' and the HTML
renderer's, and they are the same three lines over the same order. The
one thing that could split them is a problem visible in one medium only,
which would shift every counter after it — so `check_problem_media()`
bans that shape, and goes red on a temporary file that has one. Then the
agreement was measured rather than argued: **841 `prob-` ids across the
three rendered versions, 0 not in `labels`.**

**Print needed more than the web did.** A reference resolves through
`\pageref{lbl:<anchor>}`, and only chapters and headings emitted a
matching `\label` — a problem reference would have printed `??` and left
a warning nobody reads. `TexRenderer` now emits one per problem, on the
same counter (48 in Lesson 3 alone).

The other seven notes, all Lesson 3 unless said otherwise: `pr` described
as reducing resistors **and impedances**, named `pr()`, and said to work
in both places; the shorthand callout rewritten to cover both places and
its heading shortened; a colon that introduced nothing turned into a full
stop; `pr` set as code wherever it was bare prose; the example titles a
point and a half taller (`1.125rem` on the web, `\fontsize{13}{15.5}` in
print); and in Lesson 4, *an expression in terms of the variable
{{var:load}}* and the dropped *under `pmax`*.

**The linking found a reference to a problem that does not exist.** The
sentence naming the case where `pr` makes no sense pointed at *B11's
Example 8.3*, and the book has no such problem — 8.1, 8.2, 8.5, 8.10,
8.15, 8.21, 8.22, 8.24, 8.26 and 8.30 exist, and 8.3 never did. It had
read that way since the chapter was written; nothing could have caught it
before, because a name in prose was not a reference to anything.
**Roberto's replacement is *B11's Example 6.13*** (10 Sep 2026), and it
is the better example on its own merits: a 24 V source with three
resistors in parallel across it, and the problem asks for all three
branch currents, which is exactly what reducing them would erase. The
reason clause moved with it, from *the current through R₁* to **the
current through each resistor**.

**The correction was made in all three books** at his word, and the
reference resolves per version — `/7/`, `/8/` and `/9/lesson-dc#prob-
b11s-example-613` — Example 6.13 being a problem all three share. Only
the wrong reference and its reason were touched in 7 and 8: `pr` stays
bare there, and *Example 7.4* and *6.22* are still plain text in the
older books, which is the frozen-prose rule and not an oversight.

**The full title stands where a reference prints one.** The 6.22 link
reads *B11's Example 6.22 (Hidden source)* rather than the bare number
the prose used, because a reference renders what its target is called;
Roberto looked and left it (10 Sep 2026).

## #362 — a pair of symbolic answers stacks instead of running off a phone — **done 9 Sep 2026, source only**

Roberto, 9 Sep 2026, reading Lesson 2 on his phone: the two power answers
above *It is this ability to simulate symbolically* were one display joined
by `\quad\text{and}\quad`, and too wide to fit. *"Since they are two,
there's no obligation to have them in the same line."*

Now an `aligned` block, stacked and lined up on the `=`. The word *and*
goes with the change: the prose above already introduces them one at a
time (*to find the power consumed... to find the power delivered...*), so
it was carrying nothing the reader needed.

**Not a new construct.** `\begin{aligned}` is already used in Lesson 6 and
Lesson 13, seven blocks between them, and it was checked on the live site
rather than assumed — `learn.symbulator.com/9/lesson-twoports` renders its
`g_{11}` block through KaTeX at 143px tall, which is the several rows.

The display is not inside a version wrapper, so 7 and 8 take it too. That
is the #260 shape: layout only, not a word changed, and the two books
showed the same over-wide line.

**The sibling pair one screen earlier was left alone on purpose.** Line 130
has the same `\quad\text{and}\quad` construction, but it sits inside
`::: only 7,8` — version 9 shows `::: result` panels there instead, so no
version 9 reader ever meets it.


## #361 — a button is not a field: the app's vocabulary grows a third tier — **done 9 Sep 2026, source only**

Roberto, 9 Sep 2026: *"I think buttons should use a different colour in
the text ... the Run Symbulator text should be different. Maybe salmon?"*

`{{btn:Run Symbulator}}` joins `{{card:}}` and `{{ui:}}` from #357, with
its own `ui-button` token through all three copies of the palette and a
`\uibtn` macro for the PDFs. **35 spans over 19 labels**, promoted out of
`{{ui:}}`; version 9 now renders 274 cards, 318 controls and 35 buttons,
and versions 7 and 8 still render none of any tier.

**The sorting rule:** a button is something you *press* and it acts — *Run
Symbulator*, *Download*, *Add equation(s)*, *Write the equations*. A field,
checkbox or menu option is something you *set* and then read — *Type of
analysis*, *Rounding*, *Show equations* — and stays teal. The italic menu
*values* (*DC — direct current*) were already a fourth thing and are
untouched.

**Salmon was asked for and not shipped, for a reason worth keeping.** The
answer colour in dark mode is `--answer: #ff9c9c`, which *is* a salmon. A
salmon button beside it would have said that the button and the value
`0.006` are the same kind of thing — the exact distinction these colours
exist to draw. The warmth was kept and pulled toward orange: **`#b0561a`**
light, **`#f0a868`** dark. Roberto was sent both, side by side in both
themes, with the clash visible in the dark salmon row rather than described.

One label needed a second pass: *Write the equations* wraps across a line
break in the source, so a whole-string replace missed it while every other
label matched. Any future sweep over these commands wants the same warning
— a brace command is not confined to one line.

## #358 — brace commands may nest — **done 9 Sep 2026, source only**

Roberto, 9 Sep 2026, after #357 had to leave 44 sites in plain bold:
*"Option A, and fix the parser."*

`INLINE_RE`'s brace group matched `{{`, then anything without braces, then
the first `}}`. So `{{v9|tick {{ui:Show equations}}}}` ended at the inner
closer: the version span was truncated and the rest of it reached the page
as literal markup. The trap was found on 24 Aug 2026, and the response then
was to document it in `SPEC.md` and write a check that banned nesting —
which is why it was still there to bite #357 thirty-six times.

`parse_inline` now scans instead of pattern-matching for braces: a new
`brace_end()` counts depth and returns the real closer. Everything else
still goes through `INLINE_RE`, and an **unbalanced** `{{` falls through to
it, so a damaged source degrades exactly as it used to rather than
swallowing the paragraph.

**The guard was inverted rather than deleted.**
`check_nested_version_spans()` banned the thing that is now legal;
`check_brace_balance()` takes its place and reports an opener with no
closer, at the line where it starts. Both directions were proved rather
than assumed:

* a synthetic `{{v7,8|the calculator's {{ui:Settings}} menu}}{{v9|the
  {{card:Results}} card}}` renders as *the calculator's Settings menu* in 7
  and *the Results card* in 9, each with its inner span intact;
* `parse_inline` returns one `vspan` where it used to return a truncated
  one plus leaked text;
* the new guard goes **red** on a temporary file holding an unclosed `{{`,
  and clean on the real tree;
* `brace_end` returns the end index on a nested span and -1 on an unclosed
  one.

The `SPEC.md` warning box that told authors not to nest is now a note
saying they may.

**What this unlocks beyond #357:** `{{o:}}`, `{{sub:}}`, `{{var:}}` and
`{{t:}}` can all live inside a version span now. Several passages were
split into `::: only` blocks purely to work around this, and they can be
folded back if anyone wants the prose tighter — not done here, since it
would touch text for no visible gain.

## #357 — the app's own vocabulary gets its own colour, in two tiers — **done 9 Sep 2026, source only**

Roberto, 9 Sep 2026: *"everything that is in bold because it is a feature
could benefit of having a slightly different colour of text... I love how the
answers pop up because of the different colour."* Then, unprompted: *"If you
want to use one colour for card names, and another colour for features inside
those cards, that's good."*

**Why it could not be a stylesheet rule.** Bold was doing two unrelated jobs:
the app's vocabulary, and node names, element names, symbolic values and
unknowns, which #267 and #302 deliberately set bold. Colouring `strong` would
have lit up **r1**, **0** and **e** as though they were buttons. Measured
before deciding: 1,470 bold spans in `src/`, 378 distinct.

So two new inline commands, `{{card:Results}}` and `{{ui:Show equations}}`,
rendering `.ui-card` and `.ui-ctl` on the web and `\uicard` / `\uictl` in the
PDFs. Two new tokens through all three copies of the palette — `ui-card`
`#24487e` / `#7fb0e8` and `ui-control` `#0f6b5c` / `#5fd3bd` — plus the
`CLS_TO_TOKEN` entries, so `check_palette.py` guards them like every other
colour. Same weight the bold had; only the colour is new.

**The card list is not a judgement call — it was read off the app.** Every
`div.card` summary in `repos/server/templates/index.html`: Input File,
Circuit Description, Analysis & Settings, Equations, Results, Evaluate,
Solve, Mini-Tools, Plotting Tools, By-Hand Equations. That is also what
settles the awkward ones — **Settings** and **Expert Mode** *look* like
cards in the prose but are `summary` sections nested inside Analysis &
Settings, so they are controls.

**The colours are Roberto's pick from a rendered strip**, and the first
pair lost: teal cards with violet controls read as two unrelated hues
against a page whose links are blue. He asked for the theme's own family
instead — *"colours more in line with the blue palette of the default
theme"* — so cards took the deep blue `#24487e` and controls the teal
that had been the cards'. The sample he chose from carried a link in every
paragraph, because the risk with a blue is that a card name reads as
something clickable; bold and unlinked is what separates them.

627 spans converted over 61 names: 273 cards and 354 controls in the
rendered version 9 pages, 0 in versions 7 and 8, which name calculator
functions rather than app controls and were measured at **zero** feature
bolds before a line was touched.

**44 sites could not take the colour at first**, and that is what became
#358. They sat inside a `{{v9|...}}` version span, which the inline parser
closed at the first `}}` it met, so a brace command nested in one
truncated it and leaked markup onto the page. They were reverted to bold
by walking the real brace depth, Roberto was given the choice between
living with them and fixing the parser, and he chose the parser. All 44
are converted now.

Three heading occurrences (Solve twice, Expert Mode once) were left bold on
purpose: `slugify` strips brace commands, and an anchor is not worth the
risk.

**Unverified until a PDF build:** the `\uicard` / `\uictl` macros are in
`symbulator.cls` and the TeX renderer emits them, but no PDF has been built
since — the PDFs are held.

## #356 — Lesson 1 §1.6's heading — **done 9 Sep 2026, source only**

Roberto, 9 Sep 2026: *"I don't like this wording: 1.6 Comparing it with your
own working. Maybe: 1.6 Compare with your work"* — and, in the same breath,
an instruction worth keeping: *"feel free to push back on any of my
suggestions that you think is wrong."*

Shipped as **Compare it with your own work** — his imperative and his *work*,
with two words of his cut restored, and he was told which and why:

* **it** — the object. Without it the heading does not say what is being
  compared, and this section compares *Symbulator's system of equations*
  with the reader's own method, not the reader's work with anything.
* **own** — the contrast. *Your work* on its own can read as *your job*;
  *your own work* can only mean the working the reader did.

The imperative was the right instinct and matches §1.1, *Run a direct current
analysis*. What went was *working*, correct British usage for the steps of a
calculation but narrower than the book's readership; *work* costs nothing
here.

Version 9 only — the section is inside `::: only 9`, so 7 and 8 do not have
it at all. The anchor `{#by-hand-equations}` is untouched, so the section
keeps its number: `Book.labels` computes *section 1.6* from position, never
from the title.

## #355 — Lesson 1's three steps stand on their own line — **done 9 Sep 2026, source only**

Roberto, 9 Sep 2026. The three run-in labels of *A numerical DC simulation,
step by step* were bold sentences with the prose continuing straight after
them; each is now a line of its own, with the paragraph beginning below:

    **Step 1: Describe the circuit.** Description starts with **naming the nodes**...
    **Step 1: Describe the circuit**

    Description starts with **naming the nodes**...

The trailing full stop goes with the split — a label on its own line is not a
sentence. Same for steps 2 and 3.

**They are still bold paragraphs, not headings.** That is what was asked for,
and it is also the safe reading: a `####` would have put three new anchors
into `Book.labels` and into the chapter's contents list for a passage that
reads as one continuous walkthrough.

**Step 2's line is a version span across a line break** — `{{v7,8|We can now
ask Symbulator to simulate this circuit in direct current:}}{{v9|Under the
box, choose the simulation:}}` — so the rewrap had to leave the braces
unbroken. `build.py --check` reads whole files rather than single lines for
exactly this, and it passes.

None of the three is inside a version wrapper, so **all three books** take the
change.

## #354 — Lesson 1's two-spellings sentence says what the two ways are — **done 9 Sep 2026, source only**

Roberto, 9 Sep 2026, revising the opening line of the passage #347 added, in
three passes — *these names* to *these answers*, then *the name of any of
Symbulator's answers*, then the clause that says what the choice is:

    You may write any of these names two ways.
    You may write the name of any of Symbulator's answers in two ways: with or without an underscore.

The two substantive gains: the sentence no longer says *names* where the list
above it gives **answers** (`vr5`, `irx`, `pr12`), and the reader is told what
the two ways *are* in the same breath, instead of inferring it from the `ir1`
/ `i_r1` example that follows.

On the *in*: both forms are grammatical — *write it two ways* is an adverbial
noun phrase, *write it in two ways* the standard form — but with a long object
(*the name of any of Symbulator's answers*) the bare version briefly reads as
though *two ways* were a second object, so the preposition earns its place.

**And the clause the new opening made redundant is gone.** The next sentence
had gone on to say *"the underscore between the prefix and the name it
belongs to is optional"*, which *with or without an underscore* now says
first; it was flagged as a judgement call and Roberto took it out the same
hour. The sentence reads *"…`v2` and `v_2` the same voltage; capitals make
no difference either"*, the colon becoming a semicolon now that nothing is
being introduced.

**Nothing was lost with it.** Where the underscore goes is no longer stated,
but the four examples show it — `ir1` / `i_r1` and `v2` / `v_2` — and *either*
still has its antecedent in the opening sentence's *with or without an
underscore*, which is why that clause could go and the *capitals* one could
not.

A fourth pass the same hour rewrote the passage's closing sentence, which had
been both incomplete and too broad:

    …in **Evaluate**, in a condition, or as an element's value, Symbulator recognises both.
    …in **Evaluate**, in **Solve**, in a condition, or (in the case of dependent sources) as part of an element's value, Symbulator recognises both formats.

**Solve** is bolded to match **Evaluate**, per #269. Both halves of the claim
were checked in `repos/server/symbulator_ui.py` rather than taken on trust:
`prepare_inputs` rewrites sans-underscore names in the description's
**values** with names and nodes left untouched — which is exactly a dependent
source referring to another element's answer, and nothing else — and the
comment at the expert-mode branch says outright that this happens *"the same
way Evaluate and the Solve panel already do"*. So the parenthetical narrows a
claim that had been wider than the code, and *in Solve* adds one that was
true and unstated.

Version 9 only — the passage is inside `::: only 9`, so 7 and 8 are untouched.
`01-lesson-dc.md` is **CRLF** where `00-introduction.md` is LF; the edit was
made line-ending-aware and the file is still 0 bare LF, because a whole-file
ending flip would have shown up as a 1,400-line diff.

## #352 — the *Use at your own risk* box shortened, and the report address moved out of it — **done 9 Sep 2026, source only**

Roberto, 9 Sep 2026: shorten it, and *"maybe move the 'Please report' email to
be in the regular text below the caution."*

75 words to 43. **What was cut is the padding, not the disclaimer.** *"as
is"*, *express or implied* and *including but not limited to the warranty of
fitness for a particular purpose* all survive verbatim, because shortening
those narrows what the notice covers. What went was the throat-clearing
(*Every effort has been made in the development of this software, and there
are no known bugs in it*) and a restatement the box's own title already makes
(*Every time you use Symbulator, you do so at your own risk*).

`Please report any problems to help@symbulator.com` is now a plain paragraph
under the box. It is the only address in `src/`, and the house style is plain
text rather than a `mailto:` link — left as found.

**The box is not inside a version wrapper**, so 7 and 8 take the change too.
That is right: it is the same licence disclaimer in all three books.

## #351 — *Input files and entries* leaves the Introduction and becomes a chapter — **done 9 Sep 2026, source only**

Roberto, 9 Sep 2026: *"On the one hand, it is important. On the other hand, it
feels heavy, premature and out of place."*

The useful diagnosis is sharper than length: it was **reference material in a
narrative chapter** — sixty lines on saving, updating, renaming and
downloading, read before the reader has typed a circuit to save.

**The test that decides where such a section belongs: does the reader need it
*before* Lesson 1, or *at a moment during* the work?** *Input files* fails it
— nothing in it matters until the reader first saves something, and Lesson 1
already names both words in two sentences at exactly that point
(`01-lesson-dc.md:147`). Keep the test; it is what settled the split-view
question below without a second argument.

So: a new `src/00b-input-files.md`, *Working with input files*, listed in
`book.yaml` after the Introduction, carrying the original text **verbatim** —
the two definitions, the `.cir` lead-in, and *Loading input files* / *Saving
your work* / *What an entry remembers*, promoted `###` to `##`. The
Introduction keeps five lines under **Built-in examples**: the tutorial's
circuits are already in the app, click a title to load one.

**The build already supported all of this; `build.py` did not change.**

* `versions: [9]` in the front matter, and `Book.for_version` drops the
  chapter for 7 and 8 outright — no empty page, no `absent_note` placeholder.
* `kind: front`, **not** `lesson`, so the numbering counter never sees it and
  v9 still numbers its lessons **1–13**, the same as 7 and 8. `kind: lesson`
  here would have shifted every lesson number in one version only.
* The chapter id is `input-files`, which is what the old section's anchor
  was. `Book.labels` keys chapter ids and section anchors into **one flat
  dict**, so the Introduction's surviving heading had to be renamed —
  `{#built-in-examples}` — or the two would have collided silently. Both
  existing `{{ref:input-files}}` calls (the new stub's, and the split-view
  warning's) now resolve to the chapter and render as its title.

Verified by loading the book through `build.py`'s own API rather than by
reading the front matter and believing it: v7 and v8 list fourteen chapters
and no `input-files`; v9 lists it unnumbered between `introduction` and
`lesson-dc`; lessons are 1–13 in all three; `ref:input-files` resolves to
`('Working with input files', 'input-files', '')`. `build.py --check` clean.

**The split view stays in the Introduction.** Asked separately the same day,
and it passes the test above: it answers *how am I meant to read this book*,
which is wanted before Lesson 1, not during. 294 words, most of them working.
Its warning about losing typed work now points at a chapter that explains
saving, instead of at a section forty lines further up the same page.

## #350 — *ever capable of running on a handheld device* — **done 9 Sep 2026, source only**

Roberto, 9 Sep 2026, asking whether it should read *"ever made that is
capable"*.

Neither. After a superlative, `ever` wants a verb to attach to — *the best
film ever made*, *the first person ever to walk on the moon*. `capable` is an
adjective, so the span read as *at all times capable*.

`00-introduction.md:16` is a version span, and **only the v9 half moved**:

    ever {{v7,8|made for a calculator}}{{v9|capable of running on a handheld device}}
    ever {{v7,8|made for a calculator}}{{v9|to run on a handheld device}}

7 and 8 were already idiomatic, and their text is frozen besides. The
*capability* sense was kept rather than borrowed from the app's *made for a
handheld device*: version 9 is not made for handhelds, it runs on one, which
is what the original was reaching for.

The app's paragraph is a **different sentence** that happens to make the same
claim — that one is #353, in `NEXT.md`.

## #349 — the credits put the AI collaborator above the software — **done and live on the web 9 Sep 2026; the three PDFs deliberately skipped**

Roberto, 9 Sep 2026: *"In the credits, move the AI collaborator part to
appear above the Software I rely on."*

Under **Acknowledgements** the order is now **Human collaborators → AI
collaborator → Software I relied on**.

**The trap was the version scoping, not the move.** *AI collaborator* was
`###` nested *inside* the `::: only 9` block that wraps the Python / SymPy /
ahkab paragraphs. Lifting it out naively would have carried v9-only content
into the Symbulator 7 and 8 books, where it makes no sense at all. It now has
an `::: only 9` block of its own and the original closes after the ahkab
paragraph. Verified in the builds and then live: v7 and v8 still show
*Human collaborators → Software I relied on* and no AI section; only v9 has
all three.

**Moved by slicing the file's own bytes, never retyped.** The prose is
Roberto's and carries em dashes and trailing spaces; retyping is how a word
changes in transit. The diff is the same lines out and the same lines in,
with `prose unchanged: True`, the `:::` count 10 → 12 for the one new block,
and `::: only 9` 1 → 2. The *Use AI responsibly* callout came across intact.

**Note for whoever ships the next PDF build:** the credits chapter is in
**all three** books, so this is the #343 shape — a `--web` deploy leaves v7,
v8 *and* v9 printing the old order, not just v9.

## #347 — Lesson 1 says that an answer's name may be written either way, and §1.6 drops its underscores — **done and live on the web 9 Sep 2026; PDFs deliberately skipped**

Roberto, 9 Sep 2026, two comments on §1.6's use of `v_2` and `i_r3`.

**The rule had never been stated.** The tutorial teaches the naming scheme in
Lesson 1 — *Answers for each node*, *Answers for each resistor* — and then
uses the flat spelling everywhere, but nothing told the reader that the
underscored form exists or that it is the same name. The note goes exactly
there, at the end of those two lists, which is where the question arises and
before any name is used in anger: `ir1` and `i_r1` are the same current,
`v2` and `v_2` the same voltage, capitals make no difference, version 9 added
the longer form so machine-written output reads back unambiguously, and the
two can be mixed freely. Inside `::: only 9` — the calculators never had the
underscored spelling — and confirmed absent from the v7 and v8 builds.

**Checked against the app before it was written down, and the first check was
wrong.** `Result["IR1"]` raises `KeyError`, so the monograph's
"case-insensitive" claim does *not* hold for the Python API's dict lookup.
On the path a reader actually uses — Evaluate, conditions, Define, an
element's value, all through the same canonicaliser — `ir1`, `i_r1`, `IR1`,
`I_R1` and `Ir1` all resolve. Proving that took a second attempt: the first
used a dependent source with a coefficient of `0`, which would have "passed"
whatever the answer was.

**§1.6's underscores removed**: `**v_2**` → `**v2**`, `**i_r3**` → `**ir3**`.
That was the only place in Lesson 1 where an *app variable* carried an
underscore, so the tutorial is now uniformly on the short spelling and the
new note's closing claim is true rather than aspirational. The two
`\dfrac{v_1 - v_2}{I_T}` fractions are **mathematics, not app variables**,
and were left alone — verified still present and identical in all three
version builds.

## #346 — Lesson 1 §1.6 shows the reader Symbulator's own equations before it mentions the by-hand ones — **done and live on the web 9 Sep 2026; PDFs deliberately skipped**

Roberto, 9 Sep 2026: *"Its first paragraph assumes that the user knows what
Symbulator's equations look like. However, nothing in the documentation
before that point asks the users to examine the equations that Symbulator
generated."*

Two things were wrong in that paragraph, not one. It said *"you may have
noticed that it did not do it the way your course does"* — the reader could
not have noticed — and then *"the equations it shows"*, which they had never
seen, the **Show equations** setting being off by default. The opening now
states plainly that Symbulator does not solve the way the course does, and a
new passage sends the reader to look before the by-hand card is mentioned at
all: open **Settings**, tick **Show equations**, and an **Equations** card
appears (just above **Results** since #345); open it and it lists the system.
It also says no second solve is needed, and why the setting is off by default.

**Two claims measured rather than asserted.** *No re-solve* — the change
handler re-renders from the cached system and its own comment says so; I had
assumed the opposite first. *"Short enough to read line by line"* — Lesson
1's circuit was driven through the live site and produces **7 rows**: four
element equations and three KCL, which is exactly the "one per element and
one per node" the next paragraph claims, so the example demonstrates the
point rather than merely asserting it.

Written as flowing prose. I first added two `###` subheadings and took them
back out: they restructure the section and the sidebar, which was not asked
for.

**The PDFs are stale on purpose.** #346 and #347 both change typeset text, so
`--web` leaves `symbulator-v9.pdf` on `learn` saying *"the equations it
shows"* and printing `v_2` / `i_r3`. Roberto, 9 Sep 2026: *"Skip the pdfs for
now."* v7 and v8 are unaffected — everything here is inside `::: only 9`.
A later `python build.py` (no `--web`) and a `learn` deploy clears it.
Nothing here is numbered twice and the sequence never restarts.

Opened 26 Aug 2026, from the integrity pass over the version 9 rewrite.

---

## #343 — Roberto's credits revision, and the PDFs rebuilt for it — **done 9 Sep 2026, live on learn, web and PDFs**

Roberto rewrote the human-collaborators and technology sections of
`src/99-credits.md` himself, after a proofread: the Antony García
paragraph expanded (May 2013, the WPI PhD candidacy, *"and we became
friends"*), the three version cohorts set in bold and the first two
merged into one paragraph, *Technology* retitled **Software I relied
on**, NumPy named beside Python and SymPy, and the ahkab paragraph
tightened to Giuseppe Venturini alone.

Three corrections made on the fly under the standing instruction, all
his wording otherwise untouched: **NumPy** for *Numpy* (the project's
own capitalisation, and what this tree's prose already used),
**Throughout its development** for *Through its development*, and three
lines rewrapped from 86–97 columns to the paragraph's 76.

**This is the exception to `--web`, and it is the shape to watch for.**
The credits chapter is in all three books, so a web-only build would
have left the PDFs printing the old paragraph — the half of the site
nobody notices is stale. Full `python build.py`, with `build/tex/`
deleted first so a truncated `.aux` could not fail the run silently.

Pagination did not move: v9 **297**, v7 **236**, v8 **223**, the same as
the 8 Sep build. All three fetched back from the host and hashed against
the local build (`24457c5d…`, `4121cf24…`, `f302e1d6…`, all matching),
and `learn.symbulator.com/9/credits` serves every changed phrase.

One thing worth keeping from verifying it. **Grepping the built PDF for
those phrases reports misses that are not misses.** pypdf's extraction
drops the spaces out of justified lines — *ofJuniorChamberInternational*
— and XeLaTeX hyphenates across line ends, so *circuit theorist* is
*consummate cir-/cuit theorist* in the file and matches nothing. Four of
seven probes came back MISS on a book that was completely correct. Read
the extracted page, do not trust the probe; the same lesson as the Ω and
∠ re-encoding trap under #221/#222.

---

## #342 — the documentation's browser tab says *Documentation* — **done 9 Sep 2026, live on learn and the landing page**

The docs half of #342 (the app half, and the reasoning, are in
`Application/v9/repos/local/NEXT.md`). The tab read `Symbulator 9`, which
is what the app's tab read too; a reader with both open could not tell
them apart. It now reads **Symbulator 9 Documentation**, and a chapter
reads *Direct current analysis — Symbulator 9 Documentation*. Versions 7
and 8 say their own numbers — the suffix is appended to `$toc['name']`,
not hard-coded.

Two files, because **the site's `<head>` has two authors.**
`web/index.php` serves it and `tools/static_preview.py` writes its own
markup for `build/preview/` — the trap this tree already learned once,
when a fixed banner in `index.php` did nothing to the preview for a day.
Both now build the name from one place in their own file (`$siteName`,
`site_name`) with a comment in each pointing at the other.

Checked by running the preview generator: `v9-home.html`,
`v9-lesson-dc.html` and `v9-index.html` carry the three forms above.
`index.php` cannot be run here — there is no PHP on this machine — so it
is the identical expression to the generator's, and verifying it is a
matter of fetching a page after the deploy.

The landing page (`landing/index.html`, no build step) reads **Symbulator
9 Welcome!**. Its `og:title` is left as the sentence it is: that is a
shared-link preview, not a tab.

---

## #333 — Lesson 1 introduces the By-Hand Equations card, once, where the reader has just finished their first solved problem — **done 8 Sep 2026, live on learn (web; the PDFs take it at their next build)**

Roberto's call, 8 Sep 2026: *"since now there's a single button and
several by hand methods selected automatically, it is not worth to add a
comment to each problem. Instead, add a note that introduces the feature,
at a pertinent location, such as after the first problem solved."*

That replaced the earlier plan of a generated line on every problem —
which #331 made redundant: with one button that works out the method for
you, there is nothing per-problem left to say.

So: one `::: tip` inside `::: only 9`, placed immediately after *B11's
Example 5.7* closes ("your first ever problem in Symbulator") and before
the practice section. Five short paragraphs: why Symbulator's equations
look unfamiliar (it stamps every element and every node at once and never
picks a method), what the card does instead, how to reach it, what it
draws on the circuit, and the two caveats — not every method suits every
circuit, and the classic answers are the ones to trust.

The homework framing is the point of it, in Roberto's words: it is for
the moment a reader's own answer disagrees with Symbulator's and they
cannot see why. Both systems name the same quantities the same way, so
the two pages can be laid side by side and the line where they part
company found — usually a sign.

It is a **section of its own**, `## Comparing it with your own working
{#by-hand-equations}`, inside the `::: only 9` block -- it renders as
**1.6**, between the first worked problem and the practice section.

It was briefly a `tip` box instead, on the reasoning that a grep found no
heading inside an `only` block anywhere in `src/`. Roberto: *"You can use
a heading inside an only block."* Worth keeping as a lesson about this
tree rather than about markup: **no existing instance is not the same as
not supported**, and the build would have said so in a second. Ask the
build, or ask him; do not infer a rule from a grep.

Checked: present in v9, absent from v7 and v8, `h2` with its anchor,
numbered in sequence. The anchor draws no sidebar link, and neither do
`run-dc` or `practice-dc` -- the nav is built from `toc.json`, which
lists chapters, not sections. Live and verified by fetching.

## #323 — the docs' half: *Switching with coupled coils* in Lesson 10 (four Nilsson & Riedel problems, version 9), and the three passages that still said a floating side stops the solver — **done and live 7 Sep 2026, web and PDFs**

Write-up in `Application/v9/repos/local/NEXT.md` under #323. The four
problems are credited to Nilsson and Riedel's *Electric Circuits*, 11th
edition, without problem numbers (Roberto has none), and each carries
its DC-then-TR pair of app links. The field labels follow the app's
own -- *Do you want to limit the results to save time?* and the
*What results are you after?* box, and an **Evaluate** box for `v4-v5`.

## #320 — the docs' half: Lesson 13 says a port may be a `[top,bottom]` pair, and gains the three problems a reader sent — **done and live 7 Sep 2026, web and PDFs (v7 235 / v8 222 / v9 289 pages); six problems in all, 19.17, 19.63 and 19.71 added the same morning**

The section's sentence *the two bottom nodes are always assumed to be
ground* is now a version span: true of 7 and 8, and version 9 says a
port whose lower terminal is not ground is written as a pair in its
node box, and that a side with no path to node 0 is measured against a
reference of its own. Three problems appended in a `::: only 9` block
after the #314 ones: AS7's Problem 19.2 (z of the two-rail ladder,
41/15 and 1/15, with what grounding the bottoms would have given),
19.19 (y in s, as an aligned display) and 19.70 (g of the
parallel-series connection, 0.06 S, -1.3, 0.7, 23.5 Ω, and the note the
plain solve carries). Their figures are the app's own drawings; the
first two show **f** as the reference the tool takes and the captions
say so. Each problem's title matches its entry in `Lesson_13.cir`, so
`app_links.py` reports 317 of 319. The app write-up is #320–#322 in
`Application/v9/repos/local/NEXT.md`.

## #319 — the monograph brought up to solver 0.6.2 — **done, live on `learn.symbulator.com/monograph.pdf` 9 Sep 2026**

Roberto's ask of 6 Sep 2026 (*"remind me to ask you"*) was the
four-terminal forms alone; he widened it on 9 Sep to *"update anything
else in the monograph that feels outdated."* The monograph was
anchored on **0.5.19** and the engine is on **0.6.2**, so this is
eight releases of drift, not one item. **45 pages → 51.**

### The four-terminal forms (the original ask)

A new §2.2.2, *Ports of two terminals*, states the shapes
(`t,[tl,bl],[tr,br],[N1,N2]`, `z,[tl,bl],[tr,br],[p11,…]`), the rules
that keep them unambiguous (both node terms bare or both paired;
paired nodes force paired turns; a port whose terminals are one node
is a short), and — the point worth making once — that there is **no
second stamping rule**: `port_nodes` hands every port back as a
(top, bottom) pair with `0` for the classic form's bottoms, so the
equations collapse term for term onto the calculator's. The element
catalog now writes ports as `P₁, P₂` with the caption defining `P`,
and the two-port row carries its optional parameter list.

`Stamp-DC` (Alg. 2) reads a port voltage as `u_k = v_{a_k} - v_{b_k}`
and hands its four (node, current) pairs to a new **Alg. 3,
`Port-Currents`**: drop terminals on a reference, sum pairs sharing a
node, emit one named answer apiece. The notation section gained
`(a₁,b₁)`, `(a₂,b₂)`, `u_k` and `R`. The answer-inventory section
gained the per-terminal rule, the shared-node sum, and the **internal
unknown** the tapped autotransformer forces the transformer's free
current into (`Circuit.internal`) — the one solved quantity a reader
never sees.

**#322/#323 came with it**, and they change a check the monograph
stated as absolute. `Parse-and-Validate` (Alg. 1) now returns
`(E, R)`: union-find, then one reference per **island** that holds a
port terminal or a coupled coil's, chosen preferred → first port
bottom → first node, and *reported* rather than taken silently; an
island of ordinary elements is still refused by name. §2.1's
one-sentence version of the same check was corrected too, and
"ground never gets a symbol" became "a reference never gets a symbol,
for every n ∈ R".

### What else was outdated

- **The by-hand equations (#329, #332) had no section at all** —
  the largest gap. New §4.5, six subsections: the subordination
  (never fed by the classic solve; three verdicts, not two),
  **Alg. 9 `Read-Branches`** (Z and E by differentiating the engine's
  own equation — the discipline being that a second reading is
  *derived*, never written beside the first), **Alg. 10
  `By-Hand-Nodal`**, mesh in prose, a worked five-element example
  showing nodal's 3 rows against mesh's 2 with the supermesh, the
  **augmented method** and why coupled coils go to mesh and
  transformers/two-ports to nodal, and the standing sweep — written
  *without* the counts, deliberately, see the correction below.
  §2.1's *"It never uses mesh analysis"* now says that is still true
  of the solve and points here.
- **The SPICE translator (#160–#163)** was unmentioned; a paragraph in
  §4.4, including the `1'M`/`1M`/`1MEG` trap and that an
  untranslatable element is omitted-and-named, never a failure.
- **Brackets (#165)** — the value-language bullet still said `[…]`
  means `pr` everywhere. It is positional now: `pr` in a resistor's
  value, structure on a port element, refused elsewhere.
- **Decimal rounding (#318)** — a note in §4.4 on why `sp.N(x, n)` is
  not decimal rounding, with the −36.20493° case.
- **The abstract** names the by-hand systems; the `ch:tools` intro
  notes the last tool states no physics either.
- Header comment `0.5.19` → `0.6.2`.

### Appendix B *was* affected after all

The old entry said it was not. It was: `schematic.py` moved on
8 Sep (#322 parameter lanes, #337/#338 the op-amp routing and its
name on the hypotenuse), and the figures were 1 Sep. `py
paper/render_exemplars.py` re-run; all eight SVGs changed.

### Verified, not assumed

All three worked exemplars re-run against 0.6.2 and unchanged:
`v_th = vs2/n`, `z_eq = z2/n²`; the coupled coils' `(e^-t ± e^-3t)/2`
and `3(e^-3t − e^-t)/2`; `v_o = vs(g1−g2)/(g3−g4)`. Every new claim
about the four-terminal forms was run first, not read off the source:
the floating-primary transformer, the tapped autotransformer, the
four-terminal `z` block, and both by-hand systems of the worked
example. `xelatex` twice, 0 errors, 0 undefined references, the same
3 pre-existing overfull boxes.

### A correction, caught the same day by re-running the check

The section was first written quoting #329's table — *194 nodal and
143 mesh systems, 319 and 247 under `--cover`*. Re-running
`repos/server/tools/check_byhand.py` to confirm those figures before
leaving them in a published document returned **204 and 149**, and
`--cover` **333 and 262** — all four still 100% agreeing, with 0
differing, 0 unsure and 0 unsolved. Every one of the four had moved in
the day since #329's own sweep; #332 turned refusals into support, so
more systems build. Two of them moved by more than the eye would
guess: `--cover` nodal 319 → 333 and mesh 247 → 262.

Nothing was wrong with the *claim* (every system built agrees, none
differs); what was wrong was pinning it to a snapshot. So neither the
monograph nor `byhand.py`'s docstring quotes a pair of counts any
more — both name the tool and say the figure that matters is the zero
beside *differs*. Same lesson the project keeps relearning elsewhere:
a number restated in a second file is a number that goes quietly
stale.

**This correction is one paragraph in §4.5.6 and is not yet on
`learn`** — the live PDF still carries the two snapshot figures. It
rides the next `learn` deploy.

### Deployed

`py build.py --web` then `py Deploy\deploy_symbulator.py learn`, on
Roberto's go the same day. **Exactly one file moved** — `monograph.pdf`,
1,057,743 b — with 689 of the 690 already identical, which is the
check that this was a monograph-only change: no app build, no cache
bump, no solver release, and the three tutorial PDFs (rebuilt that
morning for #343) untouched. Verified twice over: the deploy's own
hash check against the served bytes, then the file fetched back from
`https://learn.symbulator.com/monograph.pdf` and its MD5 compared to
the local build (`efe15b7f…`, equal) and its table of contents read to
confirm §4.5.6 is there.

## #318 — claimed by the app tree, 6 Sep 2026: decimal rounding in the package and, pending, the app; no docs work -- the tutorial prints the book's values, which are the correct ones. Write-up in `Application/v9/repos/local/NEXT.md`

## #317 — documentation for using symbulator in Jupyter — **deferred by Roberto, 6 Sep 2026, until the app's documentation is ready**; the entry is in `Application/v9/repos/local/NEXT.md`

## #316 — the docs' half: `build.py` ships `monograph.ipynb` beside `monograph.pdf` and the landing page links it — **done and live 6 Sep 2026**

Two edits. `build.py` copies
`Application/v9/repos/solver/notebooks/the_monograph.ipynb` into
`build/web/monograph.ipynb`, reaching across into the app tree the way
it does for `banner.css`, and raises `SystemExit` naming the layout
when the file is absent -- the landing page would otherwise carry a
dead link. `landing/index.html` gained one line in the monograph card:
*Its exemplar circuits as a Jupyter notebook: download or open in
Colab*, the first link with the `download` attribute, the second the
Colab-on-GitHub form. `Deploy/deploy_targets.ini`'s `learn` target
verifies the new file by hash. `build.py --web`, then `learn` and
`landing` deployed and verified; the app write-up is #316 in
`Application/v9/repos/local/NEXT.md`.

## #315 — claimed by the app tree, 6 Sep 2026: the package in a notebook. Write-up in `Application/v9/repos/local/NEXT.md`; no docs work, by Roberto's decision (the notebook use is documented in the solver's README and a quickstart notebook, not here)

## #314 — the docs' half: the four-terminal forms, the transformer's two currents, Example 13.11 restored, and five worked examples for the new forms — **done and live on learn, web and PDFs, 6 Sep 2026**

The app's half is #314 in `Application/v9/repos/local/NEXT.md`. Four
things here; the fourth came after the drawings and the package, in the
order Roberto set (*"Once you are done with the drawings, and we publish
that package, I want you to update the documentation for both
transformers and two-ports"*, then *"add the new features and create
examples for the new things. Also add them to the built in examples
input files"*).

**The five examples, all version 9 only** (`::: only 9` around each
problem, the precedent being Lesson 2's Showing-off Problem). In the
coupling lesson: *The autotransformer as one tapped winding*
(`t,[1,0],[2,1],[80,120]` -- the second winding's bottom is the first's
top, and it gives Example 13.11's answers to the digit from a description
that looks like the circuit); *A transformer whose primary is not
grounded* (the 8 Ω load reflected as 32 Ω, 5/18 A in the primary, the
current at each of the three live terminals); and *Both windings between
live nodes, and why a side needs a ground* (the referencing resistor
carries nothing, and deleting it produces the floating message, quoted).
In the two-port lesson: *An h-parameter model with a resistor under its
common terminal* (emitter degeneration: gain −16.45 against −97.56 with
the common terminal grounded, which the two-node form cannot express)
and *A z-block with its second port lifted off ground* (`iz2` and `iz3`
equal and opposite, node 3 below ground). Every number was read off the
app through the dev server before it was typed, and each problem has an
entry of the same title in `Lesson_10.cir` or `Lesson_13.cir`, so the
app links resolve (`app_links.py`: 314 of 316). **Their figures are the
app's own drawings**: `tools`-free -- rendered by `symbulator.schematic`
through headless Chrome at 2×, cropped, and saved as
`assets/circuit/sym_*.png` (ASCII names), the way #296 used the app's
Bode plots; `measure_figures.py` re-run, 328 figures.

**Deployed.** The web pages at the end of the app's release train, and
the PDFs after the examples, since both the restored 13.11 and the new
problems change the typeset text -- the standing `--web` default lifted
for the reason it exists to be lifted.

**The answer paragraph said one current; version 8 gave two.** The
coupling lesson's *What answers do you get?* is shared text for 7, 8 and
9, and it read *the current entering the transformer, named with the
transformer and the node -- for a transformer `t` on node 2, that is
`it2`*. The 2023 page for version 8 says *each of the two non-ground
nodes* and names `ita1` and `ita2`. The port had lost the secondary
and the conversion had followed the port rather than the original; the
paragraph now says two currents for all three versions, with a version 9
span adding that four named terminals give four.

**Example 13.11, the autotransformer, is back.** It was in the 2023
page and absent from the lesson -- the one problem whose answers read
`it2` and `-it1-it2`, which version 9 could not produce until now. It
is restored from the original as written: 7 and 8 fences verbatim, the
version 9 field, the three currents explained as *what enters at node
1*, *the opposite of what enters at node 2* and *the opposite of their
sum*, and a version 9 result panel pair reading `75∠-6.87°` and
`30∠173.13°`, measured through the app. Its figure was in neither the
docs tree nor on the live site (`symbulator.com/circuit/as7e1311.png`
is a 404); it was recovered from the 2023 website's master folder on
OneDrive, where it is `as7ex1311.png`, and copied in under the
sibling-consistent ASCII name `as7e1311.png`; `tools/measure_figures.py`
re-run, 323 figures measured. An entry in `Lesson_10.cir` gives it its
app link.

**The paired forms, version 9 only.** The coupling lesson's syntax
section gains the bracketed turns, `t1,1,2,[80,800]`, and the
four-terminal form `t1,[1,3],[2,4],[80,800]`, with the floating rule
and the note that either node of a pair may be 0; the two-port lesson's
*Use two-ports as elements* gains `z,[1,3],[2,4]` and its answers, `iz1`
to `iz4`, under the element's own name. Both as `::: only 9` blocks, so
7 and 8 keep the calculator's account. The full documentation pass for
both elements, with the drawings, is the item after the drawer.

## #313 — a Copy button on every typed-input box — **done and live, 5 Sep 2026**

Roberto, 5 Sep 2026: *"Thinking about a easy way to pass the transfer
functions from the documentation to the app, could we offer a 'copy with
a click' option on the documentation for these transfer functions?"*

Every `field` box -- the panel that shows what the reader types into a
named field of the app -- now carries a small **Copy** pill in its label
row, at the right where the other panels float *type* and *returns*. A
click puts the box's text on the clipboard and the pill reads *Copied*
for a moment; where the clipboard API is refused it falls back to the
old select-and-`execCommand` route, and says *Select and copy* if even
that fails. One delegated handler in `web/index.php`, one rule block in
`style.css` on the palette's tokens, hidden in print. The split view's
docs iframe gained `allow="clipboard-write"` so the button works inside
it too. Lesson 11's six transfer functions were the ask; the same button
now sits on every circuit description, Evaluate line and Solve equation
in the book -- 315 boxes -- so a whole problem can be carried into the
app field by field. The search index strips the buttons as it strips the
app links, so *Copy* is not a word the search finds on every page.

Verified live on Lesson 11: sixteen buttons on the page; a real mouse
click on the first transfer-function box's pill wrote to the clipboard
(the browser harness reported the write) and the pill said *Copied*. The
PDFs were rebuilt and deployed straight after (v7 234 / v8 221 / v9 278
pages, unchanged in count), so they carry the evening's wording; the
button itself is web-only, as the TeX shows no *Copy*.
Worth knowing: a *programmatic* click fails both routes and shows
*Select and copy*, because the clipboard needs a user activation that a
script's `click()` does not carry -- so an automated check of this button
has to press it with the mouse.

## #312 — one sun-and-moon in the split view — **done and live, 5 Sep 2026, both halves**

Roberto, 5 Sep 2026: *"We get duplicate dark mode toggle buttons now on
the app side of split. Can you think of a way of solving that
duplication?"* #310 gave the shell a toggle for the docs pane; #311 then
uncovered the app's own, in the ribbon it keeps when framed.

One toggle, the shell's, driving both panes. The docs pane is
same-origin and is set directly, as before. The app pane is another
origin, so it is *told*: the shell posts `{ from: 'symbulator-split',
type: 'theme', dark }` on every click and once more on each load of the
pane, so an entry opened later matches too; the app, when framed, hides
its sun-and-moon and applies a theme message that comes from
`learn.symbulator.com` (or its own origin, which is how the dev server is
tested), storing it like a click so the app opened on its own later
remembers the choice. This is the one message the app pane receives;
the protocol comment at the head of `split/index.php` and the root
`CLAUDE.md` say so, where they used to say it was never messaged at all.

Verified on the dev server by framing the app inside itself: the framed
copy's toggle is `display: none`, a theme message from the parent sets
and stores dark then light, and the same message posted to a top-level
page is ignored. The shell's half is live; the app's half rides Roberto's
next pull, and until then the split view shows the shell's toggle beside
the app's own, harmlessly.

## #310 — light and dark in the split view — **done and live, 5 Sep 2026**

Roberto, 5 Sep 2026: *"I don't see the light dark mode toggle on the doc
side of the split view."* The docs page hides its whole ribbon when
embedded (`html.embedded .topbar, .subbar { display: none }`, #224), and
its sun-and-moon lives in that ribbon; the shell read the stored theme
on load but offered no way to change it.

The shell's bar now carries the toggle, at the right-hand end after the
Docs and App tabs: the docs page's own icons and logic (`ICON_MOON`,
`ICON_SUN`, the `symbulator-docs-theme` key), sized for the slimmer bar.
A click sets `data-theme` on the shell and, the pane being same-origin,
on the docs pane's root directly, so both change together without a
reload; a pane that navigates afterwards reads the stored key itself
before first paint, as it always did. The app pane is another origin and
keeps its own toggle.

Verified live: both roots go dark and back together, the stored key
follows, the button's label flips between the two modes.

## #306 — a Contents button for the phone layout — **done and live, 5 Sep 2026**

Roberto, 5 Sep 2026: *"it is important for the user in mobile using
split view to have a way to navigate the lessons. How about we add, in
the space between the Symbulator 9 text and the Docs button, a Contents
button that deploys the menu?"* #304's menu hung off the position badge,
and below 480px the badge is hidden to keep the bar on one line, so a
phone had no way into it.

A **Contents** button now sits between the wordmark and the tabs, drawn
like the tabs' buttons and shown only where the badge is not (the same
480px breakpoint, one way each). Both triggers open the one menu, which
moved out of the badge's wrapper to be a child of the bar -- hidden
inside a hidden wrapper it could not have shown -- positioned under the
bar's left edge and capped at the viewport's width, items ellipsised.
Escape returns focus to whichever trigger opened it. Nothing else in the
shell changed.

Verified live at 375px: the badge hidden, Contents shown; a tap opens the
fifteen items inside the viewport; choosing Lesson 11 loads
`/9/lesson-bode` on the left and `?lesson=11&entry=1` on the right and
closes the menu.

## #304 — a lesson menu in the split view's bar — **done and live, 5 Sep 2026**

Roberto, 5 Sep 2026: *"There's no table of content in split, so how about
we make a drop down menu for all the lessons, visible when one clicks
here"* -- the position badge (*Lesson 4b · entry 31*).

The badge is a button now, with a caret; it opens a menu of every version
9 chapter in reading order, *Lesson 3* in small capitals beside each
title, the current chapter marked. Picking one does what the ribbon's
*Split View* link does for a chapter (`showPage`): the left pane opens on
the chapter, the right pane on the chapter's first book, the URL becomes
`?page=…`. Escape, an outside click, or the focus leaving for a pane
closes it; the arrow keys walk it. The titles ride in `lessons.json`,
written by `build.py` from `book.for_version(9)` -- they exist nowhere
else the shell can reach without loading every chapter -- as a third key
beside `lessons` and `chapters`. Below 480px the badge's wrapper is
hidden as the badge was, so a phone keeps the two tabs and no menu.

Verified live: fifteen items, *Lesson 4 · Shorts, equivalent resistance
and Thévenin/Norton* marked current on `?lesson=4a&entry=7`; choosing
Lesson 6 loads `/9/lesson-transient` on the left, `?lesson=6a&entry=1` on
the right, the URL `?page=lesson-transient`, the badge *Transient
analysis*.

## #303 — a placed link scrolls the split view to itself — **done and live, 5 Sep 2026**

Roberto, 5 Sep 2026, on the placed pairs: *"when that link is clicked,
the documentation scrolls up to where it used to be. You need to add new
anchors in the new locations for those links, each one linking to its own
location's anchor."*

The anchors were already there -- `applink_rows` puts `id="e-6a-3"` on
whichever pair renders it, head or placed -- but the docs pane's `goTo`
(`web/index.php`) scrolled to `el.closest('.problem')` on purpose, so that
a head link put the problem's title in view. That was right for #224,
when every link was at the head, and wrong from #297 on: a placed link's
anchor was found and then the pane scrolled to the head anyway. Now a
link whose row follows the problem title scrolls to the problem as
before, and any other scrolls to its own row. One function, in the docs
page; the shell and the protocol are unchanged.

## #302 — element names set as element names, not as answers — **done and live (web), 5 Sep 2026**

Roberto, 5 Sep 2026, on Lesson 4's *The current through `rl`, `irl`, reads
−0.06 A*: *"rl appears as if it was an answer variable, in the same
format as irl. However, rl is not such a thing. Instead, rl is the name
of an element, so show it in regular text but bold, as other element
names. Do this fix on every other instance of this mistake across the
documentation."*

A sweep of every version 9 line with a short element-shaped name in code
(`tools/v9_lines.py`, then read by hand) found nineteen such names in
eight chapters: **rl** twice (Lessons 4 and 5), **cx**, **rx** and **j1**
in Lesson 7, **l1**, **l2** and the kind letters **r** and **m** in
Lesson 10, the node names **ag**, **as**, **ad** in Lesson 9, **s1** and
**s** in Lesson 4, **r1**/**R1** in Lessons 1 and 2, the book's **r1** and
**r3** values in Lesson 5's design problem, and the two-ports **z1**,
**zp** and **z** in Lesson 13. Answer names (`icx`, `vrx`, `irl`, `z111`),
unknowns the reader types into a field (`rx`, `l`) and circuit lines stay
in code. Rule: #267's -- a name the circuit gives an element or a node is
bold when bare in prose; code is for what the app returns or the reader
types.

The same passage now says the second part of RM3's 9-8 runs with **SI
prefixes** ticked, so `irl` reads −60 mA like the sentence after it
(Roberto: *"currently it says 0.06 and then 60m. Make both 60m"*); the
entry's `si:` is on to match.

---

## #301 — a problem's later runs link from the solution, not the head — **done and live (web), 5 Sep 2026**

Roberto, 5 Sep 2026, on RM3's Example 9-8: *"When you have multiple links
like here, put the second onwards at the right place of the solution as
opposed to the top."* #297's directive, applied as a rule: the first
entry's pair stays under the title; every later one is placed with
`::: applink` where the solution reaches that run.

Thirty-five problems had more than one pair at the head, 39 extra runs
between them (Lesson 6 alone has 24 problems whose DC pass for the
initial condition precedes the TR). For 32 of them the runs line up with
the problem's **Circuit Description** boxes one for one, so a script
(`place_links.py`, kept in the session's scratch, not the tree) put the
k-th entry after the k-th box; the three whose runs are not boxes were
placed by hand -- B11's 6.22 *(Partial reduction)* after its answer,
RM3's 9-8 *(with the load)* after the edited equivalent, and AS2's 5.7's
*(the v2 factor)* after its result panel and *(checking the design)*
after the verification circuit. A recount over the built tree finds no
problem with more than one head link. `build.py --check` clean: every
placed title names an entry.

## #298 — the five `out` fences a version 9 reader saw as calculator text — **done and live (web), 5 Sep 2026**

Roberto, 5 Sep 2026, on Lesson 6's `t^2/4`: *"Make sure to show these
expressions mathematically."* A sweep of every ```` ```out ```` fence
visible in version 9 (a script over the `only`/`not` nesting and the
fence's version list) found five: that one, and four complex answers in
Lesson 7 written with the calculator's 𝐢 -- `3.22–𝐢11.07`,
`0.25-0.025𝐢`, `9.135+𝐢27.47`, `0.3794+𝐢1.46`. Each fence is now
`out 7,8`, and version 9 gets the answer as mathematics: a `::: result`
panel where it is a card answer (`v_{c} = t^{2}/4`, the two `Z_{eq}`),
a `$$` display where it came out of **Evaluate**, the imaginary unit
written `j` after the number as the app writes it, with the unit. No
other version 9 page shows an `out` fence now.

**The PDFs are held** (Roberto, the same evening: *"Do not do the PDFs
for now until I tell you."*). The full build that was running was
stopped, the three `symbulator-v*.pdf` were removed from `build/web`
before the `learn` deploy so the live PDFs stayed as they were (the
script never deletes without `--delete`), and `build/pdf/` still holds
the earlier run's PDFs, which predate #296–#298 anyway. **Lifted at the
end of the session** (Roberto: *"build, commit, and upload everything,
including the PDFs"*): rebuilt and deployed at v7 **234** / v8 **221** /
v9 **278** pages, carrying #293–#304, the white-text check clean.

## #297 — `::: applink`: a run's app links beside the run — **done and live (web), 5 Sep 2026**

Roberto, 5 Sep 2026, on AS7's Example 16.1: *"Having four sets of links
at the top of this problem is confusing. Please insert these pairs of
links at the location of the solution where they are logically
related."* That problem is four app entries -- TR in one step, FD with
everything as an impedance, FD with farads and henries, FD and back to
time -- and #224 stacked all four pairs under the title, two of them
labelled *in FD* because `entry_label` shortens a qualifier at its comma.

A new directive, `::: applink <entry title>` (empty, closed with `:::`),
renders one pair where it stands, labelled with the run's full
qualifier; the problem head leaves that entry out, and a problem whose
runs are all placed has no head links at all. The argument is the entry's
title as its input file writes it, brackets and all, folded the way the
join folds (`app_links._fold`), so the two *in FD* runs name different
entries. A title that names no entry of the chapter is a `SourceError`,
so a renamed entry fails the build rather than silently losing its link.
The head and the inline pair share one renderer (`applink_rows`), so the
entry anchor `e-12-3` the split view scrolls to is emitted exactly once,
by whichever of the two draws it -- and the split view now lands on the
run itself. The search index already strips `class="problem-links"`
paragraphs, and the inline one uses that class unchanged. The PDFs print
nothing for it, like the head links.

Example 16.1 places its four pairs after the TR result, after each FD
description and after the `s2t(vo)` Evaluate box in the next section --
the fourth run's text lives outside the problem block, which is why the
directive takes a full title rather than a qualifier of "the current
problem". `SPEC.md` has the row and the paragraph.

---

## #296 — Lesson 11's transfer functions shown, and the plots as pictures — **done and live (web; PDFs held), 5 Sep 2026**

Roberto, 5 Sep 2026: *"In the Bode lesson, the transfer functions for
the problems are not shown. Please make sure the functions are shown and
also include as images the resulting graphs."* The six practice problems
(AS7's Examples 14.3, 14.4, 14.5 and the three Practice Problems) said
*Construct the Bode plots for the given transfer function* and never gave
it; version 7 showed two of them as calculator screenshots.

Each statement now carries its function as a display, in the textbook's
form -- `H(ω)` in jω for 14.3, 14.4 and their practice problems, `H(s)`
for 14.5 and its practice problem. 14.3 and 14.5 were read off the
chapter's own screenshots (`as71403s1.jpeg`, `as7e1405s1.jpeg`); the
other four are Alexander & Sadiku's, checked against the version 7 plot
screenshots the chapter already carried (PP 14.3 crosses 0 dB at ω ≈ 1,
14.4 crosses left of it, PP 14.4 peaks near ω = 5 with the phase running
+90° to −180°, PP 14.5's phase starts at −90°). The version 9 block of
each problem gains the **Transfer function H(s)** box with the function
as the reader types it, the two frequencies in hertz, and a figure of the
plot: `assets/plot/<problem>-bode.png`, six PNGs drawn by
`bode_tf_ui` -- the same samples the app's Plot card draws -- through
matplotlib, magnitude above and phase below on a log axis in Hz, 300
points over the chapter's own sweeps (0.1–300 rad/s for 14.3, 0.1–100 for
the rest). The peaks agree with the chapter: 24.44 dB at 4.48 rad/s for
14.3, where the text says 24.4 at 4.47. The six carry a 120 mm override
in `tools/figure_sizes.json`, since the detector's label-height rule was
written for scanned circuits. Version 7's pages are untouched, and the
figures sit inside `::: only 9`.

Not done: app entries for the six. An input-file entry needs at least one
element line (`parse_book` skips one without), and the transfer-function
plot has no circuit, so an entry would have to carry a dummy element to
exist. Left alone rather than mislead; the two loose ends `app_links.py`
reports for this chapter are these.

The transformer passage in Lesson 10 (AS7's Figure 13.33) also moved to
result panels the same evening, at Roberto's ask -- `v_{th} = vs_{2}/n`,
`R_{eq} = z_{2}/n^{2}` -- the same rule as #294.

## #293 — Lesson 4's Thévenin-with-a-load material, rewritten around the app's own load answers — **done and live (web; PDFs held), 5 Sep 2026**

Roberto, 5 Sep 2026: *"The features of the th() tool of Symbulator were
not properly ported from v8 to v9. And the documentation for v9 for
thevenin equivalents, as a consequence, are full of material made up by
the AI. We need to correct that."*

The app's half is **#292** (`Application/v9/repos/local/NEXT.md`): the
load question under the port nodes, the three load answers **irl**,
**vrl** and **prl** in the variable `load`, and the *Load circuit
equivalent?* button. This is the book's half, written from the 2023
version 8 page (`originals/docs-page8.html`, *Problems with a load* and
*What if it's more than a load?*) rather than from the invented
workaround the version 9 text carried -- a table of hand-typed
expressions, `vth/(req+R)`, `vth*R/(req+R)`, `vth^2*R/(req+R)^2`, and a
three-line circuit the reader was told to type with rounded numbers.

What changed, version 9 pages only (7 and 8 untouched):

* **Problems with a load** describes the question -- *Are you running a
  problem with a load connected to this equivalent circuit?* -- the three
  answers it adds under the four, and how to read one at a value: ask
  **Evaluate** for `irl` with `load = 2` in **Conditions**.
* **B11's Example 9.6** ticks the question, shows `i_{rl} = 6/(load + 2)`
  as a result panel under the four, and evaluates `irl` at 2, 10 and 100.
  Roberto, later that night: it says to set **Rounding** to *approx to n
  digits*, **n** = 2, so the third answer reads .059 rather than 1/17; the
  entry's `rounding:` moved to 2 with it.
* **Power transfer problems** names `prl` again instead of *the
  expression derived above*.
* **What if it's more than a load?** describes the button, its warning
  and what it writes: the three-line equivalent in the description with
  `iNo` and `rEq` in **Define**, exact.
* **RM3's Example 9-8** uses the button, then edits the load to 168 Ω
  and adds the 180 mA source -- the calculator's own sequence.
* The nine practice problems that said *Answer Y when offered the load
  formulas* -- Bo2's 3.10, 3.5, 3.7 and Drill 3.7, RM3's 9-7, 9-13 and
  Practice Problem 9.5, B11's 9.15, and **AS2's 4.8**, which Roberto's
  list did not name but carried the same workaround -- now say *tick the
  question about the load* in the setup line and ask **Evaluate** for
  `irl`, `vrl` or `prl` with the load in **Conditions**. The 7/8 *Answer
  Y* sentence is unchanged, and became a 7,8 span so version 9 does not
  print *Choose DC* twice.
* **Lesson 5's TR5 Figure 4-32** did the same for `prl` at 1000, so no
  version 9 page types a load expression by hand any more:
  `tools/v9_lines.py 'vth/\(req|vth\^2'` finds nothing.

The example books moved with the chapters (their `evaluate:` lines now
read `irl`/`vrl`/`prl` with an `evaluate_conditions: load = …`, and RM3's
9-8 follow-up entry is the circuit the button writes, with its two
`defines:`); `verify_lesson.py` was run over Lesson_04a and Lesson_04b,
see #292.

`build.py --check` clean; `build.py --web` built. **The PDFs are not
rebuilt** -- this changes what the typeset text says, so the next deploy
is one of the exceptions to `--web` and wants a full `python build.py`
first.

---

## #294 — symbolic answers on their own lines, as mathematics — **done and live (web; PDFs held), 5 Sep 2026**

Roberto, 5 Sep 2026, three asks in one:

1. *"format these expressions as single line preceded by their variable:
   'The answers we get, {vs*µ/(µ+1),ro/(µ+1)}, are correct,'"* -- TR5's
   Example 4-8 (Symbolic) in Lesson 4, and its twin two problems earlier,
   `{vs*µ/(µ+1),ro}`. Both versions: 7 and 8 get `$$` displays headed
   `vth =` and `req =` (the set form #273 had kept for them is what he
   quoted, so the ruling is his); version 9 gets `::: result` panels
   labelled *Thevenin voltage* and *equivalent resistance*, in the app's
   form `v_{th} = …`, `R_{eq} = …`.
2. *"in the op amp lesson, put these in single lines: vth = (expression),
   ino = ∞, req = 0, pmax = ∞"* -- Bo2's Drill Exercise 3.11 (Thévenin):
   four result panels, `\infty` set as the symbol.
3. *"make all the answers in this chapter that are symbolic values appear
   in their own single line as mathematical expressions"* -- Lesson 5,
   version 9. Twenty passages. A card answer (`vo`) becomes a
   `::: result voltage of node o` panel; an **Evaluate** ratio or a
   **Solve** answer a `$$` display with the quantity in front
   (`\dfrac{v_{o}}{is_{1}} = -r`, `r_{2} = 5\,r_{1}`). Where the line
   was shared by all three versions it is split into `::: only 7,8` /
   `::: only 9` blocks and the 7/8 half keeps its words. Identifiers
   follow #274: `vs`, `vi`, `rf`, `ro` stay as the app writes them, a
   trailing digit is a subscript.

Numeric answers already on their own panels (#284) and the numeric
inline ones (`vo` = 9 V) are untouched -- the ask was symbolic values.
`build.py --check` clean. Same PDF note as #293.

## #281 — the Expert Mode fields with the plural in parentheses, the book's half — **done and live, 6 Sep 2026**

Roberto, 6 Sep 2026: like the Solve card's *Equation(s) to solve* and
*Unknown(s) to solve for*, the Expert Mode fields should be **Add
equation(s)**, **Add unknown(s)**, **Add condition(s)**, and Lesson 2's
three bullets should say one or many — *separated by `and` or one per
line* for equations and conditions, *separated by commas or one per
line* for unknowns.

**The book leads; the app's half is #279**, claimed by the app tree the
same afternoon. Those names are the app's own labels (`i18n/en.json`),
and a field box is meant to spell its field as the interface does;
Roberto said not to wait for the app. So the twelve mentions in Lessons
3, 6 and 13 — prose and field boxes — carry the new spelling now, and
Lesson 2's twelve, with the rewritten bullets, followed the same evening
when he released the file, applied on top of his own edits, together
with two wording changes from the same round: *But it does give you an
idea of what*, and the quadratic note, *Symbulator returns multiple
solutions when they exist* (it used to say Symbulator returned one).
No old spelling is left anywhere in the version 9 pages.

The commit that shipped the first half, `3d4e7a6`, is titled `#278` —
the number the app tree had taken an hour earlier for its colour themes,
which this file already recorded. The item is #281; the commit message
cannot be changed once pushed. Same lesson as 3 Sep: claim a number in
both trees before using it.

---

## #284 — numeric card answers as result panels, one per answer — **done and live, 6 Sep 2026**

Roberto, 6 Sep 2026, on Lesson 2's *The power consumed in each resistor
is given in `pr1`, `pr2` and `pr3`: `pr1` is 1.2 W, `pr2` is 0.4 W, and
`pr3` is 0.6 W*: use the new labelled single-line form — *given in:*
then one panel per answer — and do the same wherever that structure
occurs, dropping the duplicate mention of the names.

**The sweep.** A survey of every version 9 line giving numeric card
answers keyed by result name (110 lines) read against its lead-in; two
shapes were converted, 30 passages in Lessons 2 to 6:

- Lesson 6's *The answers you want are `vc`, `ic` and `v2`, in Results.*
  followed by *`vc` = 8 V, `ic` = 0 A and `v2` = 8 V.* — seventeen of them —
  now *The answers you want are in **Results**:* and a panel per answer;
- a whole sentence of the form *The answer is `v1` = 4.8 V, `v2` = 2.4 V
  and `v3` = −2.4 V. This is correct.* (Lessons 3, 4, 5; *Results gives*,
  *We read*) — the lead-in loses the values and the *This is correct.*
  becomes its own paragraph after the panels.

A `::: result` panel now holds a number with its unit
(`v_{c} = 8\ \mathrm{V}`), the label from the name as before, and the
converter reads the circuit description to tell a node voltage from an
element's drop — with the op-amp rule from #276 built in this time (an op
amp's name is its output node, so `v_o` is *voltage of node o*, never a
drop in o). Versions 7 and 8 are untouched: every converted passage sits
in `::: only 9`.

**Left as they were, on purpose:** the phasor lists in Lessons 9 and 10
(magnitude and angle, not a plain unit), the complex powers in Lesson 8,
the two-port parameters in Lesson 13 (the label rule would say *impedance
seen by 11*), Lesson 5's symbolic design rules, and sentences that carry
on past the values (*…and the load current is 3 A for 6 Ω*).

Also in this train: Roberto's credits chapter, now dated (it had no
`updated:` line, so the page printed no date), and the app tree's claims
of #282 and #283.

---

## #288 — `is` instead of `is1` as a source's symbolic value, and three small fixes — **done and live, 6 Sep 2026**

Roberto, 6 Sep 2026, on B11's Example 6.21: *can we replace the value
is1 with is? Can you run the simulation to verify?* Versions 7 and 8 had
always said `is`; version 9 had been given `is1` — with a note in two
problems explaining the odd name — on the belief that `is`, a Python
keyword, would not survive the app.

**It does, and it was measured rather than assumed.** The solver alone
takes `is` and returns 9 mA, 1 mA and 6 mA, the same as with `is1`.
Through the app's own path — `solve_ui` in `symbulator_ui.py`, the code
the online app runs — with `ir2 = 2'm` as the equation and `is` as the
unknown, the run succeeds and reports *is = 9 m* with no warning. The
app's keyword guard bans an *element* named `s`, whose answer would be
`is`; a value symbol called `is` is a plain symbol. The three other
Lesson 3 problems that used `is1` were run the same way and return the
answers the chapter prints (*1000·is*, *2·is*; *−12·is*, *−6000·is*;
*re1·(β+1)* with the `β*is` source).

**Changed:** the four version 9 circuit descriptions (B11's Example 6.21,
TR5's Figure 4-4, Bo2's Example 1.11, TR5's Example 4.5) and the Expert
Mode instruction, and the two notes excusing `is1` are gone. No `is1` is
left in the book. **The app's four entries in `Lesson_03_*.cir` still say
`is1`**; a prompt for the app session was handed to Roberto, since the
book and the app should agree.

**In the same train, three small things:** HK5's Figures 1-24b and 1-24c
name their variables as the diagrams do, lower-case *i_x* and *v_x* (the
1-24b figure was read to confirm it matches); B11's Example 6.22 reads
*Looking at the value of `ir1`, we get I₁ = 10.48 mA* (a panel form was
tried at Roberto's suggestion and withdrawn at his word); and HK5's Drill
Problem 1-11's lead-in drops the four names its values line repeats,
*The current through each short is given in:* — the only other lead-in
of that shape, Lesson 1's *given in `pr1`, `pr2` and `pr3`: 36 mW, 108 mW
and 72 mW*, keeps its names because its values are not keyed.

---

## #287 — the figure label target a quarter larger, for every figure — **done and live, 6 Sep 2026**

Roberto, 6 Sep 2026, on HK5's Drill Problem 1-13 in the browser: the
labels in the figure sit at about two-thirds of the prose's height, and
*images like this one* are still short. After Lesson 1's sweep (#265),
HK5's Figure 1-26 and TR5's Example 4-7's answer image, each an override
on a figure that #153's rule had sized, the pattern was the rule itself:
`TARGET_MM = 2.7`, the label height it aims for in print, was too low
for the way the measuring tool reads a label's height.

**Raised to 3.4 mm**, the same quarter Lesson 1 got, in the three places
that hold it: `tools/measure_figures.py` (so a re-measure keeps it), the
manifest `tools/figure_sizes.json` (what the build reads), and
`build.py`'s fallback. Every figure the rule sizes — 294 of 316 — grows
by a quarter, capped at the 156 mm line, which 43 now reach; the 22
hand-set overrides keep their widths, and since Lesson 1's were already a
quarter up, the book is uniform again. HK5's Drill Problem 1-13 goes from
117 to 147 mm (408 to 513 px on the web); AS2's Practice Problem 2.15,
which Roberto asked about next, from 78 to 98 mm (272 to 342 px).

**One override on the way:** the textbook's answer in TR5's Example 4-7
is a one-line formula image, 412 × 61 px, and the tool had taken almost
the whole image height as label text, shrinking it to 21 mm wide. It is
set to 42 mm (146 px), about the height of a line.

**Why the browser showed it:** the web sizes a figure in pixels against
the desktop column (#256), so browser zoom scales figure and prose
together and the shortfall Roberto saw was the rule's. If labels still
read short after this build, the same number moves again.

---

## #290 — Lesson 4's equivalent-tool wording, and the PDFs caught up — **done and live, 6 Sep 2026**

Roberto, 6 Sep 2026, three small things in Lesson 4, then *run
everything*:

- the card's heading in B11's Example 8.29 said *Equivalent impedance*;
  it is a DC problem, and the app's label is now lower case, so it reads
  ***equivalent resistance***. The rest of the book already followed the
  rule he stated — *Thévenin voltage* and *Norton current* keep their
  capitals, *equivalent resistance*, *equivalent impedance* and *maximum
  deliverable power* are lower case, impedance only for an AC `zeq` — and
  the built pages carry no capitalised tool label; the one place still
  saying *Equivalent impedance* for DC is the app's own `js.tool.er`
  heading, for the other session;
- the manual-method paragraph (*the Thévenin voltage, VTH … REQ is then
  VTH/INO*) had been left bare as theory text; its three quantities now
  carry the subscripted mark the answers use, `{{var:V_TH}}` and kin;
- the three bare *RL* in *Problems with a load* (*an R_L problem*, *as seen
  by resistor R_L*, *the load resistor R_L*) marked the same way.

**The PDFs were rebuilt and deployed with this train**, the first full
build since #277, so #281, #284, #287 and #288 reached print at once —
the labelled field boxes, the result panels for numeric answers, the
larger figures and the `is` rename. The figures cost pages: v7 **234**
(221), v8 **221** (211), v9 **271** (253). Hash-verified live.

---

## #289 — claimed by the app tree (6 Sep 2026)

The th/er tool's answer labels in lower case; write-up in
`Application/v9/repos/local/NEXT.md`. Nothing for the docs.

## #286 — claimed by the app tree (6 Sep 2026)

Lesson 3's four `is1` entries renamed `is` in the example book; write-up
in `Application/v9/repos/local/NEXT.md`.

## #285 — claimed by the app tree (6 Sep 2026)

The app's footer reworded, no copyright sign; write-up in
`Application/v9/repos/local/NEXT.md`. Nothing for the docs.

## #283 — claimed by the app tree (6 Sep 2026)

The MIT `LICENSE` file added to `server` and to this repository; write-up
in `Application/v9/repos/local/NEXT.md`.

## #282 — claimed by the app tree (6 Sep 2026)

Two theme names renamed; write-up in `Application/v9/repos/local/NEXT.md`.
Nothing for the docs.

## #280 — claimed by the app tree (6 Sep 2026)

Display-style maths in the app's results, so fractions are set at full
size; write-up in `Application/v9/repos/local/NEXT.md`. Nothing for the docs.

## #279 — claimed by the app tree (6 Sep 2026)

Expert Mode's three labels with the parenthetical *(s)*, English only; the
write-up is in `Application/v9/repos/local/NEXT.md`. Nothing for the docs.

## #278 — claimed by the app tree (6 Sep 2026)

Thirteen colour themes for the app and the scorpion on a transparent
ground (the landing's and learn's logo copies change with it); the write-up and the palettes are in
`Application/v9/repos/local/NEXT.md`. Listed here so the shared sequence
skips it. Nothing for the docs.

## #277 — every box labelled in print as on the web — **done and live, 6 Sep 2026**

Roberto, 6 Sep 2026: the labels on the field boxes plain, not bold (done
on the web in a line of CSS); then *can you add the labels to the print
boxes in the PDFs as well?*; then *all boxes, in results and inputs,
should be labelled both online and PDF.*

Until now the PDF set a `field` fence as plain typed input — *in print
there is no interface to imitate*, the build said, *the sentence above
names the field anyway* — and typed input and returned output carried
no word at all, where the web says TYPE and RETURNS. Now, in the class:

- **`symfield{name}`** — the typed-input box with the field's name over
  it, `build.py` passing the name the fence carries (*Circuit
  Description*, *Unknown(s) to solve for*);
- **`symtype`** says *type* and **`symout`** says *returns*, the web's
  own words, through one `\symboxlabel` command — sans, footnotesize,
  slate, plain;
- **`symlisting`** for a ```text fence: symout's box and no label, as on
  the web, where a listing is neither typed nor returned and is
  unlabelled on purpose;
- the result panel (#276) already had its label.

Unit-rendered from the build (each fence kind emits its environment) and
typeset against the class in one sample holding all five boxes. The PDFs were rebuilt and deployed the same evening, the first full build
since #269: every box now carries its label in print, and the eight items
held since #270 landed at once. The labels and panels cost pages -- v7
**221** (207), v8 **211** (197), v9 **253** (236). Pages 34 and 69 of v9
and 15 of v7 were read before the deploy.

---

## #276 — a card answer as the app shows it: the `::: result` panel — **done and live, 6 Sep 2026**

Roberto, 6 Sep 2026, with a picture of the app's Results card — a small
label, *resistance seen*, over `r_e = r_1 + 10000` on a panel: *what would
it take to include the answers in this form, online and PDF?* Not much:
the field panel, KaTeX/LaTeX and #273's `name = expression` displays were
the parts; one directive puts them together. Decisions on the way: the
PDF is the light panel, the web follows the page's mode like every other
panel; the label is plain, not bold; and — a departure from the app,
whose card names the element once as a heading that a single panel
cannot show — the label names the element: *current through r3*,
*voltage drop in c*, *power consumed by r1*, *resistance seen by e*.

**The directive.** `::: result` with one LaTeX line as its body, kept raw
(no inline markup), written in the app's form: `i_{r3} = \dfrac{e}{r_{1} +
10000}`. `build.py` parses it without touching the body, derives the label
from the name — `RESULT_LABELS` by the kind letter with the element from
the subscript, `RESULT_SPECIAL` for `v_{th}`, `i_{no}`, `R_{eq}`, `Z_{eq}`,
`p_{max}` in the app's words — and takes the argument as an override
(`::: result voltage of node 2`). Web: `<div class="code result">` in the
returned-output colours (`--paper-2`, the slate rule) with the label
inside at the top left the way a field's name sits, the display inside.
PDF: `symresult` in the class, `symout`'s grey panel and rule with the
label in the sans face. Unit-tested labels; a sample typeset against the
class; `SPEC.md` has the row.

**The conversion: 67 displays → 112 panels**, one per answer. A set that
#273 had turned into an aligned list became one panel per row. A `v_{X}`
whose X is not an element of the nearest circuit description is a node
voltage and is labelled so — *voltage of node o* in the op-amp problems,
*node 1* and *node 2* in the transients — which the converter decides by
reading the description, not by guessing from the letter. Lesson 2's
shared divider display (*i_{r1} = … and v_{r2} = …*) split by version so
7 and 8 keep the display. **Left as displays, on purpose:** the four
Evaluate ratios in Lesson 5 (`v_o / v_s = …`, not a card answer), Lesson
1's Evaluate expression, Lesson 3's Mini-Tools result, the g-parameter
tables in Lesson 13 (a table, not a row), the hand-written `i(t) = …`
sinusoids in Lesson 7, and `v_o(t) = …` in Lesson 12.

**Web only; the PDFs stay held**, now seven items behind the web
(#270–#276). The class is ready for them: `symresult`, `\symvar`,
`Scale=0.95`, all proved against the class in samples.

---

## #275 — the mono type a step larger — **done and live, 6 Sep 2026**

Roberto, 6 Sep 2026, on a **Solve** card box: the type in the field
rectangles reads smaller than the prose; make the heights more similar,
for all the computer type across the book. IBM Plex Mono was set at
0.86 of the body size on the web (inline `code` 0.86em, the panels and
the `::: address` line 0.86rem) and `Scale=0.86` in the class. Now
0.92em inline, 0.95rem in the panels and the address line, and
`Scale=0.95` in the class for the next PDF build.

---

## #274 — inside an expression, an identifier's trailing digits are its subscript — **done and live, 6 Sep 2026**

Roberto, 6 Sep 2026, on `r_{e} = r1 + 10000`: *the variables on the right
side of the equal sign should also get the same subscript treatment* —
the `1` of `r1` below the line, everywhere.

**The rule is SymPy's**, which is what the app applies when it draws an
answer: `latex(Symbol('r1'))` is `r_{1}`, `il0` is `il_{0}`, and a
letters-only name — `vs`, `gm`, `rl` — stays as it is. So the book now
does exactly that inside every display and inline expression a version
9 reader sees: 27 lines across Lessons 2, 3, 5 and 6, from `\dfrac{v}{r1
+ r2}` to `\dfrac{v}{r_{1} + r_{2}}`. A result name in front of an
expression (`i_{r3}`, from #273) is protected, as are LaTeX commands
and `\text{}`; displays under `::: only 7,8` are left alone, since
those show what the calculator printed. A dry run listed every changed
line before the write — the first pass had missed every fraction's
numerator, because the protector swallowed a `\dfrac{…}` argument with
its command name; the print showed it.

---

## #273 — a displayed card answer carries its name, one line per answer — **done and live, 6 Sep 2026**

Roberto, 6 Sep 2026, in two examples from Lesson 2: a version 9 answer
read from a card and shown as mathematics should stand on its own line
*with the variable up front, as the user would see it in the card* —
`ir3 = e/(r1 + 10000)`, `re = r1 + 10000`. Then: the form should match
the app's, the kind letter tall and the element low; then: *full sweep*.

**The form is the app's own.** `templates/index.html` renders a result
as `${sym}_{${element}}` in plain maths — `v_{c}`, `i_{r3}`, `v_{2}` —
with five special names in `TEXNAME`: `v_{th}`, `i_{no}`, `R_{eq}`,
`Z_{eq}`, `p_{max}`. The book now writes exactly that (a strip of four
candidate forms was typeset with the class and sent; Roberto chose the
italic letters of plain maths with the app's subscripts, not
`\mathrm`). A ratio from Evaluate is a fraction of names,
`\dfrac{v_{o}}{v_{s}} = …`.

**The sweep.** An extractor listed all 79 `$$` displays outside Lesson 2
with their version context, set elements and the names their lead-in
gives — *The answers you want are `vc`, `ic` and `vo`, in Results* names
them in the set's order, a `field 9 Evaluate` box or a calculator
request `{vc,il}` where there is no sentence. 25 came back unresolved and
were mapped by hand from the problem text; four pairs of single displays
that follow two request boxes were assigned by the circuits themselves —
each initial condition matches its element, so *v_c* takes the answer
that starts at the capacitor's voltage and *i_l* the one that starts at
the inductor's current. The plan was printed in full and read before
anything was written. **68 displays rewritten**, plus Lesson 2's two on
release, plus one bare 7/8 answer line that sat between two of them:

- a version 9 display gets its name in place: `v_{o} = …`;
- a display shared with 7 and 8 becomes a version pair — 7 and 8 keep
  the calculator's form (`\{ 10e^{-4t} , -2e^{-4t} , -10e^{-4t} \}` is
  what the calculator printed), 9 gets the named form;
- a set becomes an `aligned` block, one row per answer, `v_{c} &= …`.

**Left alone:** displays that are not card answers (Lesson 1's Evaluate
expression *(v1 − v2)/I_T*, Lesson 3's Mini-Tools `pr` result), and
those already named (Lessons 7, 12, 13). The 7/8 books' own bare answer
lines outside any display were not in scope.

Proved by typesetting one aligned list and three named fractions against
the real class (no errors) before the build; the web renders the same
markup through KaTeX, which Lesson 13's g-parameter tables already use.

**Web only, at Roberto's ask; the PDFs stay held** — four items behind
the web now (#270–#273).

---

## #272 — a result's name in bold, its value in red; bold italic kept for the problem's own variables — **done and live, 6 Sep 2026**

Roberto, 6 Sep 2026, on Lesson 2's *the card lists e = 72.0 and r1 =
2000.0*: those *e* and *r1* are answers Symbulator gives back in
**Results**, so they are bold and not italic — bold italic is reserved
for the variables the problem gives — and the numbers are red like every
other answer. Spread through the whole book.

**The rule, in one line:** a Symbulator result named bare in prose (not
in code) is **bold**; its value is `{{o:…}}`; a problem's own variable
stays `{{var:…}}`. The survey looked for a bare name followed by `=`,
*is* or *reads* and a value, 26 candidate lines read in context; sixteen
edits in five chapters. Lesson 2's quoted passage sat inside a
`{{v7,8|…}}{{v9|…}}` span and became a `::: only` pair; its *e = 72 and r1
= 2000*, *e = 16* and *r2 = 1600 Ω and r3 = 8000 Ω* lost their italics
for bold. Lesson 3's *v1 = –1.3 V, v2 = .34 V, v3 = –1.12 V* and the
hidden-source *voltage drop is 12V*; Lesson 4's **Req** = 2.89 Ω line
under the Equivalent impedance heading, *vth = 880 mV, ino = 50 mA…*,
and the maximum-power *9Ω … 13.44W*; Lesson 5's three 7/8 bold answers
(`**r2=50000 and r4=20000**` → **r2**={{o:50000}} and **r4**={{o:20000}},
and `-r2/r1=-5` as one red answer); Lesson 7's two *c = …* answers.

**Left:** *Let omega = 10 rad/s* and *the voltage v is 0 volts*, which
are given, not returned; and *the book's answer is 25 µF*, which is the
book's.

**Deployed web only, at Roberto's ask.** `build.py --web`; the three
PDFs on learn are the ones from the #267–#269 build and now lag the web
in three ways — this item, #270's chapter title and #271's face — until
the next full build.

---

## #271 — a marked variable in Plex Serif SemiBold Italic — **done and live, 6 Sep 2026**

Roberto found the marked variables (#261, *I_3*, *V_ab*) *a bit chubby*
and asked for a crisper font. The face is IBM Plex Serif everywhere; the
chubbiness had two causes. In the PDF the mark was the family's real
Bold Italic, weight 700, heavy at body size. On the web the site loaded
no italic above 400 at all (roman 400, roman 600, italic 400), so every
browser was faking bold italic by slanting the semibold roman.

A strip of five weights was typeset (`scratchpad/varfont/sample.pdf`:
700, 600, 500, 400, and Plex Sans SemiBold Italic) and, when he asked
whether a more elegant face would fit, a second strip of four serifs
(Plex Serif, STIX Two Text, Libertinus Serif, EB Garamond — the three
alternatives are in MiKTeX; STIX Two is also on Google Fonts). He chose
to stay with Plex at **SemiBold Italic, 600**.

**The change is contained to the mark.** PDF: `symbulator.cls` gains
`\symvarfont` (IBM Plex Serif SemiBold with its SemiBold Italic; plain
bold in the Latin Modern fallback) and `\symvar{}`, which `build.py`
emits for every `{{var:}}` — proved by compiling a one-line document
against the class. Web: the mark is `<em class="var">` at weight 600 in
`style.css`, and `index.php` now loads Plex Serif's italic 600 cut
(`ital,wght@…;1,600`), so the browser draws the real cut.

---

## #270 — a chapter title may differ by version — **done and live, 6 Sep 2026**

The last of #269's questions: Lesson 2 is titled *Symbolic circuits and
expert mode* in the sidebar, the home-page cards, the search index and
the PDF's contents and running foot — one front-matter string for three
versions. Roberto: capitalise it in version 9, without bold (a title is
printed raw in all those places, so bold would show as asterisks).

`build.py` gains `title_for(ch, v)`, which resolves version spans in a
title, applied at every place a title is printed; the title now reads
`Symbolic circuits and {{v7,8|expert mode}}{{v9|Expert Mode}}`. Unit-tested
for all three versions; `SPEC.md` records that a title may carry a
version span and nothing else.

---

## #269 — *Solve* and *Expert Mode*, capitalised and bold in version 9 — **done and live, 6 Sep 2026**

Roberto, 6 Sep 2026: in version 9 *solve* is not a command but a tool in
a card, so it is **Solve**; likewise *expert mode* is **Expert Mode**. Text
and headings alike, the problem title *B11's Example 5.6, with solve*
included.

**Where.** Lesson 2 throughout (the summary, the intro, both headings,
the problem title, and every version 9 sentence that named the mode),
the Introduction's *the **Expert Mode** equations*, four sentences in
Lesson 6 and one in Lesson 13. Shared sentences take a version span —
`{{v7,8|expert mode}}{{v9|**Expert Mode**}}` — and the 7 and 8 text keeps
its lower case, since there the feature was `ex`, a program. Headings
take the same span, as the book's headings already do. Every other
capitalised *Solve* in the book is the verb (*Solve it in DC*) and stays.

**The problem title needed a change to the linker first.** A problem's
title is the key `tools/app_links.py` joins to the app's entry titles,
and `_fold` used to drop a version span outright — so *with
{{v7,8|solve}}{{v9|**Solve**}}* would have keyed as *with* and unlinked
the problem. `_fold` now keeps a span's version 9 body (the app is
version 9, so that is the spelling the entry titles were written
against) and loses the rest. Proved: the retitled form folds to exactly
today's key, and the coverage run is unchanged at 308 of 310 with the
same 17 loose ends.

**Open:** the chapter title, *Symbolic circuits and expert mode*, in the
sidebar and the PDF contents. Left as it is until Roberto says.

---

## #268 — no Evaluate for a sign flip — **done and live, 6 Sep 2026**

Roberto, 6 Sep 2026, on Lesson 2's *we switch the sign of `pev` — type
`-pev` into Evaluate*: *humans are capable of changing the sign in their
minds* — a ruling he had already given earlier sessions. Evaluate is for
an expression worth computing, not for a minus sign. Recorded in memory
so it outlives the session.

**Fixed in three chapters.** Lesson 2's line now ends at *switch the sign
of `pev`*. Lesson 3 had four: *ask Evaluate for `-ie`* became *the
current the source delivers is the opposite of `ie`*, and three Evaluate
boxes holding nothing but a negation are gone — Bo2's Example 2.5 and the
`-ies` drill now say in words that *i* and *i_s* are the opposites of
`ie` and `ies`, and HK5's Example 1-3 keeps its box for `pr1+pra`, a sum
worth computing, while saying the delivered powers are the opposites of
`pei` and `ped` (its three power values took the red answer face too,
which #266 had missed: they follow no name or equals sign). Lesson 8's
*`-pe` in Evaluate* and *`-se` in Evaluate* became *the opposite of*.
A scan for any Evaluate box whose only content is a negated name finds
none.

---

## #267 — node names, element names, symbolic values and unknowns set bold — **done and live, 6 Sep 2026**

Roberto, 6 Sep 2026, in four steps over Lesson 2's AS5 Figure 2.29 and
B11's Example 5.6: bold the node names (*the node called **a** … becomes
node **0** … I call **c***), then the element names and the values given
to them (*the source **ev** … **v** for the source*), then a source
called *E*, then the unknowns (*in terms of the two unknowns, **e** and
**r1***). The book already set node names bold in most places (*the
bottom node **0***); this makes it every place.

**Node names: 61** in nine chapters, everywhere a bare name followed
*node* or *nodes* in prose — Lesson 1's describing rules, Lesson 4's
*nodes **a**, **b**, **c** and **d***, the op-amp notes, the step and
impulse sources, Lesson 9's ground discussion (*nodes called **a** and
**A***, the names ***ag** and **ad***), the transformer's and the
two-port's nodes. **Element names and values: 30** edits in five
chapters plus Lesson 2's — the describing rules (*a resistor called
**r5***), the dependent-source rules and *values **r1**, **r2**, **r3**
and **r4*** in Lesson 3, *short called **sx***, the op amps ***o1*** and
***o***, ***e1*** and ***j1*** in Lesson 6. **Unknowns:** the four
mentions in Lesson 2; no other chapter names one bare. Bo2's Figure 5.3
in Lesson 6 had its symbolic values *R*, *L*, *I* and its asked *iL(t)*,
*vL(t)* unmarked from #261/#262, so those took `{{var:}}`.

**Left alone:** names in code spans (Symbulator's own), a variable
prefix (*a variable called v*), the *letter z* aside in Lesson 7, and
the book's own labels for terminals (*terminals a-b*).

**Lesson 2 was locked** while Roberto edited it (the rule from #266), so
its share of #267–#269 sat in a queue — seven items — and was applied
in one pass when he released the file for this train, from the file as
he left it. His own Lesson 2 edits of the same day are in this commit.

**Open, from the same conversation:** the marked variable's face.
Roberto finds Plex Serif Bold Italic *chubby*; a strip of five weights
was typeset and sent (`scratchpad/varfont/sample.pdf`) — the
recommendation is SemiBold Italic (600) on both outputs, which also
means loading the italic 600 cut on the web, where bold italic is
currently a synthesised slant of the semibold roman. Waiting on his
letter.

---

## #266 — every answer number in the red answer face — **done and live, 5 Sep 2026**

Roberto, 5 Sep 2026: *make sure that all the numbers given as part of
answers are shown in that nice red font — {{o:…}} — consistently.* His
example, B11's Example 8.10: *I_R1 = 4.77 A, I_R2 = 7.18 A and I_R3 =
2.41 A* had none.

**The sweep** was a survey of every prose line (outside code fences,
maths and existing `{{o:}}` spans) for four shapes, 353 candidate lines
read in context with their directive stack, then 419 values wrapped
across eight chapters (`{{o:}}` count 354 → 772):

- after a marked variable — `{{var:I_R1}} ={{o:4.77}}A`;
- bold answers — the `V_TH = **48** V` lines through Lesson 4, single
  ones like `**3.4** A`, and the symbolic ones, `**1+r2/r1**`,
  `**3 v2 − 4 v1**` (a symbolic value still typesets as mathematics
  through `answer_math`; one sympy cannot parse falls back to plain
  red, as before);
- the 7/8 calculator sets, `**{12,4,3}**` → `{{o:{12,4,3}}}`, the form
  one line already used;
- after a Symbulator name — ``` `vth` = {{o:30}} V ```, and the trailing
  values of the same sentence, *{{o:3}} A for 6 Ω, {{o:1.5}} A for 16 Ω*.

Three paragraphs had their answers inside a `{{v7,8|…}}` / `{{v9|…}}`
span, which cannot hold a brace command (the nested-span rule), so they
became `::: only` pairs: Lesson 3's first answer, B11's Example 8.2 and
AS2's Example 5.9.

**Left plain, on purpose:** values the problem gives rather than
returns (*R_1 is 50 Ω*, *Z_A = 15 Ω*, *v_1 = 2V*), node names and
settings in bold (*put **2** in the first box*, *ω set to **4***),
element values in the describing notes, and a restatement of an answer
in another unit (*1/1000 A, that is 1mA*). Spacing kept as written.
`tools/check_against_originals.py` reads ```out``` fences, not `{{o:}}`
spans, so it is unaffected.

**And a lesson, recorded in memory as well.** The sweep wrote to
`src/01-lesson-dc.md` while Roberto had the file open in his editor. His
buffer predated the sweep; the conflict cost the lesson's last problem
its shared 7/8 answer, which he had folded into his revised version 9
block. Reconciled from the two versions he pasted: the 7/8 answer back
as its own `::: only 7,8` block, word for word as committed, and his
version 9 revision word for word in `::: only 9`; the one thing changed
in both is `.{{o:133}}` → `{{o:.133}}`, the decimal point inside the
span. **From now on, a source he says is open is not edited until he
releases it, whatever the feedback in between says.**

---

## #265 — Lesson 1's figures a quarter larger — **done and live, 5 Sep 2026**

Roberto, 5 Sep 2026, in three steps: B11's Example 5.7 *a bit larger*,
then HK5's Figure 1-26, then *the figures in general in lesson 1*. Each
is a width override in `tools/figure_sizes.json`, the block the manifest
reserves for hand-set widths and a re-measure preserves.

| | was | now |
|---|---|---|
| B11's Example 5.7 (`circuit/b11e0507.jpg`) | 112.6 mm / 393 px | 135 mm / 471 px |
| HK5's Figure 1-26 | 47 mm / 164 px | 62 mm / 216 px |
| the other 17 figures of Lesson 1 | the label rule's width | × 1.25, capped at the 156 mm line |

Four of the 17 hit the line (B11's Examples 7.4 and 7.11, Figure 7.40,
RM3's Example 7-5); B11's Example 7.10 was already there and got no
entry. The two smallest were small for the same reason — big labels in
the scan, so #153's rule shrank the whole picture — and RM3's Figure
7-16 (58 → 72 mm) could still take more. The practice figures are shared
with the 7 and 8 books, which grow the same way; each PDF gained one
page: v7 **207**, v8 **197**, v9 **237**.

---

## #264 — bold inside italic, and italic inside bold — **done and live, 5 Sep 2026**

Roberto's Introduction edit of 5 Sep 2026 wrote the name's origin as
*"**symb**olic sim**ulator**"* — bold inside italic — and the inline
parser could not nest them: it rendered five italic runs and no bold,
because the em closed at the first star of `**symb**` and the stars
re-paired down the sentence. Asked which way to go, Roberto chose
extending the parser.

**One level of nesting each way.** The em body now admits a whole
`**…**` group as one atom, and the strong body a whole `*…*` group, so
the inner stars cannot close the outer span; the body is parsed again
and the group becomes a node inside. The inner group is the plain form,
so nesting stops at one level. Strong is still tried first at any
position, so `**bold**` never reads as an italic starting with a star.

**Proved by comparing the old and new rules over every paragraph** —
3,069 of them, fenced code and maths stripped, the unit the real build
tokenises (a whole-file comparison lied: a stray star inside a code span
started an italic across paragraphs, which the real build never sees).
Exactly two paragraphs change: the Introduction's line, and Lesson 11's
*`**Tick *real solutions only*.**`*, italic inside bold, which had been
rendering as two stray stars and two fragments of italic for as long as
it existed and now reads as bold with the italic inside. That second
case is why the rule went symmetric. Side effect: `***x***`, which used
to print a stray star, now reads as bold inside italic; no source
writes it. `SPEC.md` records the nesting.

---

## #263 — the two PDF links at the foot of every page removed — **done and live, 5 Sep 2026**

Roberto, 5 Sep 2026: remove the two links at the bottom of the
documentation pages — confirmed as the footer's *Download the
documentation for Symbulator 9 (PDF, 26.9MB) · The internal logic of
Symbulator (PDF, 1.0MB)*, not the Previous / Next pager. Gone from
`web/index.php` with the `pdf_note()` helper only they used; the ribbon
still offers the PDF and the landing page carries the monograph. The
deploy's verification rule for the lesson page had named the removed
text (*Download the documentation for* and *MB)*), so those two markers
came out of `Deploy/deploy_targets.ini` in the same change — the next
deploy would otherwise have failed on its own success.

Also in this train, Roberto's own edits to the Introduction and Lesson
1 (wording, the portmanteau line, *where you are. Send someone:*, and
the last problem's version 9 answer), and his removal of #260's display
in Lesson 1's *How answers are shown*, which now reads as one sentence.

---

## #262 — the bare variables respelled with subscripts, and the single letters marked — **done and live, 5 Sep 2026**

Roberto, 5 Sep 2026, on the two decisions #261 left open: respell the
bare forms with subscripts, and set the single-letter element values bold
italic too.

**Respelled: 51 tokens.** `RL` → *R*\textsubscript{L}, `R1`…`R5`,
`I1`, `I3`, `RT`, `VTH`, `REQ`, `INO`, `Is`, `Vs`, `Vo`, `Ap`, `Zi` —
each `{{var:XY}}` became `{{var:X_Y}}`, so the mark and the subscript
now match the diagrams. `E` stays bare, having nothing to subscript. Two
bare statements took subscripts on the way: Lesson 4's *Find i1, i2, i3
and i4* and Lesson 6's *Find v1 and v*.

**Single-letter element values: 16 tokens.** *R*, *L* and *C* in the four
Lesson 6 statements that give them (*R=12Ω, L=2H and C=1/50F* and its
kin), the amplitude *V* in *V u(t) − V u(t − t₀)* in two problems, the
step amplitude *A* in the unknown-source drill, and the conductance *g*
in TR5's Example 4.4.

**And the single-letter *i* and *v* a problem asks for: 50 tokens.** One
step past the brief, taken because a half-marked list looked wrong:
*Determine i, v and i_d* with only the last one marked. So *i* and *v*
are marked where they sit beside marked variables — the *Determine i, v…*
statements and their *i=4, v=6* answer lines in Lesson 3, *Find v(t) and
i(t)* in Lessons 6 and 7, *the current i* in Lesson 2's symbolic problem
and Lesson 7's steady-state current. Roberto can send them back plain.

One line #261 had missed came right as well: Lesson 6's *For the circuit
left, the source is v_s(t) = V u(t) − V u(t − t₀)* wrapped its variable
in italics (`*v*{{sub:s}}*(t)*`), which put a `*` where #261's pattern
wanted a letter. It now reads `{{var:v_s}}*(t)* *= {{var:V}} u(t) −
{{var:V}} u(t−{{var:t_0}})*` — three marks inside an italic expression,
checked by rendering the line. The second *V* was caught on a second
look: it sits at the end of the source line, before a wrap, where a
pattern that wanted *u(* after it could not see it.

Four more *i(t)* / *v(t)* were caught after the first deploy, by reading
the PDF: three sat on the wrapped second line of a statement the pattern
had only run over the first line of, and one pair is the tutorial's own
reference to Example 6.1's variables. A sweep over every prose line for a
bare *i(t)* or *v(t)* now finds none.

Built in full and deployed the same day; the PDFs unchanged at 206 / 196
/ 236 pages.

---

## #261 — a problem's own variables set bold italic: `{{var:…}}` — **done and live, 5 Sep 2026**

Roberto, 5 Sep 2026: find every variable the *problem* names — in its
text or its diagram, as distinct from the name Symbulator files the answer
under — and set it bold italic. *Current Is is defined in the schematic
as…*: that `Is` is the problem's.

**The markup** is a brace command rather than raw `***…***`, so the
intent is greppable and the style lives in one place: `{{var:I_s}}` is
*I* with *s* below, bold italic, on the web
(`<strong><em>I<sub>s</sub></em></strong>`) and in the PDF
(`\textbf{\textit{I\textsubscript{s}}}`). `_` starts the subscript; a
name without one (`{{var:E}}`) is set plain. Documented in `SPEC.md`
beside `{{sub:}}`. It carries no nested brace, so it is safe inside
nothing and beside everything; the nested-span check stays green.

**The sweep.** Two greps over `src/` — every `X{{sub:Y}}` token, and
every bare capital-led token shaped like a variable — gave 457 candidate
lines, read in context with their directive stack. On 374 of them, 589
tokens became `{{var:…}}`: every subscripted book variable in a problem
statement or its answer discussion, plus the bare ones written without a
subscript — `I3` and `RT` in Lesson 2, `R1`/`R2`/`R3` where the text
names a diagram's resistor, `E` in B11's Example 6.19, `VTH`/`INO`/`REQ`
and `RL` in Lesson 4, `Ap` and `Zi` in Lesson 13, and the bare `Is`, `Vs`
and `Vo` that a stop-list for the verb *is* had swallowed on the first pass —
Roberto's own example, *Current Is is defined in the schematic*, among
them, caught by reading the PDF before deploying. **Spellings were kept
as written**: `RL` stays *RL*, not *R*\textsubscript{L}; normalising
them is a separate decision.

**Left alone, each for a reason:**

- Symbulator's own names in code (`ir3`, `vth`, `req`) and every
  `{{o:…}}` answer — the software's text, checked against the originals.
- Four lines where the notation is the tutorial's, not a problem's:
  Lesson 1's *v₁ = 36 V, i_r1 = 6 mA* explaining how answers are shown;
  Lesson 2's node voltages read off the results; the Showing-off
  Problem's *i_R5*, a derived quantity nobody asked for.
- Theory text outside problems: Lesson 4's manual-method paragraph
  (*VTH*, *INO*, *REQ*) and its "RL problem" paragraphs; Lesson 8's RMS
  discussion.
- Inline maths and #260's displays — bold italic is not a convention
  inside mathematics.
- Single-letter element values in Lesson 6's statements (*R=12Ω, L=2H,
  C=1/50F*), which no pattern can tell from prose.

The problem statements are shared by the three versions, so the 7 and 8
books show the marks too — words unchanged, the same layout-only
treatment as #260. The build's diff against the previous one touches
exactly the chapters with problems, in all three versions, plus the
search indexes.

Also in this train: the Introduction's split-view line now reads *where
you are. Send someone:* (a full stop, not a colon, before the address —
Roberto, 5 Sep 2026).

---

## #260 — compound expressions set on a line of their own — **done and live, 4 Sep 2026**

Roberto, 4 Sep 2026, on Lesson 1's *That is what you want for symbolic
results: v_in·r2/(r1 + r2) cannot be rounded*: put the expression on a
line of its own, typeset. Then: find the others like it, with several
terms, and do the same; then build, commit and deploy everything.

**The sweep** was two greps over `src/`, read in context: every inline
`$…$` holding an operator, and every prose fraction (a slash beside a
parenthesis) outside code fences, maths blocks, inline code and `{{o:…}}`
answers. The rule applied: an expression with a compound numerator or
denominator, or a function of *t* or *s*, moves into a `$$` block set with
`\dfrac`, the way Lesson 2 already sets its voltage divider; a monomial
ratio (`v_{s2}/n`), a sum of two terms (`r1 + 10000`), a problem statement's
*Find v_o/v_S* and an answer the software printed (`{{o:…}}`, the bold
7/8 answers, the bare 7/8 output lines) stay as they are — the answers
because they are the software's own text, checked against the originals.

**Nine displays, seven chapters:**

| chapter | expression | version |
|---|---|---|
| Lesson 1, *How answers are shown* | v_in r2 / (r1 + r2) | 9 |
| Lesson 1, RM3's Figure 7-16 | (v1 − v2) / I_T | shared |
| Lesson 2, the rounding tip | v / (r1 + r2) | 9 |
| Lesson 2, B11's Example 5.6 | e / (r1 + 10000) | 9 |
| Lesson 3, `pr()` on symbols | r1 r2 / (r1 + r2) | 9 |
| Lesson 4, Bo2's Example 3.11 | (9x − 35) / (4(x − 3)) | shared |
| Lesson 7, AS7's Example 9.9 | v(t) = 4.472 cos(4t − 63.43°) V | shared |
| Lesson 13, Example 19.7 | the four g parameters, 2 × 2 `aligned` | 9 |
| Lesson 13, Practice Problem 19.7 | the four g parameters, 2 × 2 `aligned` | 9 |

**The 7 and 8 books.** Three of the nine sit in paragraphs the three
versions share. Their words are untouched — the sentence is the same,
broken around the display — and the change is layout only, the same
treatment the sibling `i(t)` display in Lesson 7 already had in all three
versions. Verified by building before and after and diffing the v7 and v8
trees: exactly `lesson-dc`, `lesson-equivalents` and `lesson-ac` differ,
each by its one moved expression, and `search.json`. The Lesson 2
paragraph is the exception that proves it: its expression sat inside a
`{{v9|…}}` span, and a display cannot live in a span, so the paragraph is
now a `::: only 7,8` / `::: only 9` pair — the 7,8 side is the brace text
resolved word for word, and the built `lesson-symbolic` pages for 7 and 8
are byte-identical to before.

**Left inline, on purpose:** Lesson 7's *There is no angle to take of
v_in r_b/(r_a + r_b)* is a bullet in a list, and the markup's list items
hold inline text only (`build.py` joins continuation lines into the
item), so a `$$` block cannot go there. The three `only 9` bullets would
have to become paragraphs to display it. Also left: the `g` names on the
Practice Problem 19.7 display are inferred from the order the four come
back in, which is the order Example 19.7 names them.

Built in full (PDFs included, because the typeset text changed) and
deployed the same night: v7 **206**, v8 **196**, v9 **236** pages,
unchanged. Page 12, 32 and 227 of the v9 PDF were rendered and read.

---

## #259 — an address on a line of its own: the `address` directive — **done and live, 4 Sep 2026**

Roberto, 4 Sep 2026: the Introduction's *send someone
learn.symbulator.com/split/?lesson=6a&entry=3 and they open on the same
problem* should put the link on a line of its own, centred, with a
background of its own — *send someone:* / the address / *and they open
on the same problem, with the same circuit loaded.*

**A new block directive**, `::: address <url>` with an empty body, closed
with `:::` like every directive. The URL is written as it should be read,
without a scheme; the link target adds `https://` unless one is there.
On the web it is `<p class="address">` with the link inside — centred,
mono, on the input panel's tint (`--lcd`), without the accent rule a
typed fence carries, since nothing here is typed. `overflow-wrap:
anywhere` so a long query string breaks inside the panel on a phone. In
the PDF it is `\symaddress{target}{text}` in `symbulator.cls`: a
`tcolorbox` on the same tint, `halign=center`, mono, the text in the
accent colour under `\href`. The argument is escaped verbatim on both
sides — not run through `inline()`, since a URL wants no curly quotes —
and the TeX side escapes `%` and `#` in the target the way the inline
link does. `SPEC.md` has the row and a paragraph.

First and only use so far: the Introduction's split-view paragraph.
---

## #258 — the docs wordmark's β at 80%, like the other two — **done and live, 4 Sep 2026**

Roberto, 4 Sep 2026, after #257 went live: *did the beta next to the 9
spring back to its old height?* It had not sprung back; **it had never
been shortened on this site.** Measured live before touching anything:

| site | markup | numeral | β |
|---|---|---|---|
| symbulator.com | `.tm` with the β in a `.beta` span | 20.6 px | 16.5 px |
| the app | the same | 20.6 px | 16.5 px |
| learn | `9β` as bare text in a `.vnum` span | 20.6 px | **20.6 px** |

**A miss in #229, not a regression.** The 80% rule in the shared
`banner.css` is `.brand-name .tm .beta`, and its comment names the two
consumers that draw a β: the app and the landing page. This page draws
one too, but wrote it as bare text with no span for the rule to catch —
the numeral was styled, because `banner.css` matches both `.vnum` and
`.tm`, and the β inherited the numeral's full size. So learn had shown
the tall β since #137, and the claim that #229 applied *everywhere it
appears* was wrong about this site. Nobody noticed because the three
lockups are never on one screen.

**The fix is one line of markup** in `web/index.php`: the numeral's span
is `.tm`, the markup the other two use, and the β is wrapped in
`<span class="beta">`. No change to the shared `banner.css`, so nothing
had to propagate; the split view's own bar keeps its `.vnum`, which is
its own rule and carries no β. `tools/static_preview.py` still emits a
plain `.vnum` label — it draws no β at all, so it is not wrong, only
different.

Deployed the same day: one file moved (`index.php`), and the live page
measured at 16.5 px for the β against 20.6 px for the numeral on the
version 9 page, with the 7 page still reading a plain `Symbulator 7`.

**For #137:** nothing new to clear. `web/index.php` is already one of
the five spots that item lists; the β is in the same place, only wrapped
now, so removing it is the same edit as before.

---

## #257 — on a phone the ribbon keeps Split View and drops the PDF link — **done and live, 4 Sep 2026**

Roberto, 4 Sep 2026: in mobile view hide *Download as PDF* when the
ribbon needs the space, and keep *Split View* always visible.

**What was happening.** The shared `banner.css` caps the ribbon's nav at
one line and clips whatever wraps (Roberto's rule of 28 Aug 2026: a link
that would wrap hides instead). Flexbox wraps the *last* link in flex
order first, and the last link was Split View — so a 375 px phone showed
*Download as PDF · Online App* and lost the one link a phone reader is
most likely to want. Measured live: all three fit down to about 400 px;
at 375 px Split View was on a second, clipped line.

**The fix is four lines in `web/assets/style.css`, and no markup
change.** The nav lays out in `row-reverse`, and each of its three links
gets an explicit `order` that reverses the DOM again (first child order
3, last child order 1). Visually the row still reads *Download as PDF ·
Online App · Split View* left to right, and tab order and screen-reader
order are untouched because the DOM is; but in flex order the PDF link
is now last, so it is the one that wraps into the clip. `justify-content:
flex-end` keeps the links packed left, since in row-reverse main-end is
the left edge. Version 7 and 8 pages, whose third link is *How it
works*, get the same treatment for free.

Nothing about *when* a link hides changed — it is still the shared
one-line clip, decided by real widths rather than a media query — only
*which* link. The rule is learn-only, in this site's own stylesheet; the
landing page and the app keep their own priorities and the shared
`banner.css` is untouched.

**Measured, not eyeballed** — the rule was injected into the live page
and the links' boxes read against the nav's clip:

| viewport | before | after |
|---|---|---|
| 320 px | PDF · App (Split View clipped) | App · Split View (PDF clipped) |
| 375 px | PDF · App (Split View clipped) | App · Split View (PDF clipped) |
| 430 px and up | all three | all three, usual order |

A fourth link ever added to the nav arrives with `order: 0` and lands at
the right-hand end, visibly, rather than silently becoming the first to
hide; the comment in `style.css` says so.

Deployed the same day: one file moved (`assets/style.css`), hash-verified
against the host, and the live page measured at 375 px serving the new
stylesheet hash with the PDF link clipped and *Online App · Split View*
showing in order.

---

## #256 — figures keep their size on a phone — **done and live, 4 Sep 2026**

Roberto, reading the tutorial on his phone in portrait, found the figures
too small to read. Measured rather than eyeballed, the finding was
systematic: **every one of the 314 measured figures showed its labels at
5.0 px on a 375 px phone**, against a body text whose cap height is 12 px,
while the same figures show them at 8.7–9.4 px on a desktop.

**The cause was #153's web rule.** The manifest gives each figure the
width in mm that puts its labels at body-text height in print, and the
web rendered that as *the same percentage of the column*. A percentage
keeps the figure-to-page ratio constant, so when the column shrinks from
544 px (`--measure: 34rem`) to 291 px inside a phone's problem card, the
figure shrinks with it while the text does not. HK5's Figure 1-26, 30% of
the line, was 88 px wide on the phone — an 887 px scan at a tenth of its
size.

**The fix is two small things, web only; the PDF rule is untouched.**

1. `build.py` emits `width:min(100%, Npx)` instead of `width:P%`, with
   N = the manifest's mm width at the desktop column's scale
   (`MEASURE_PX = 544`). On a desktop that is the width the figure had
   (a little more inside a card, whose padding the percentage used to
   absorb: median labels 8.7 → 9.4 px). On a phone the figure keeps that
   width and the column gives way, capped at 100% so nothing overflows.
2. `style.css`, under the 40 rem breakpoint: `.problem figure` drops the
   card's 1.3 rem side padding, so a figure that wants the width runs to
   the card's inner edge — 333 px rather than 291. Not past the border:
   problems are bordered, shadowed cards, and an image over the border
   looked wrong in the mockup.

**Outcome on a 375 px phone**, from the manifest's own label heights:

| labels on screen | today | rule 1 | rules 1 + 2 |
|---|---|---|---|
| median | 5.0 px | 9.1 px | 9.4 px |
| under 6 px | 314 | 37 | 8 |
| 8 px or better | 0 | 204 | 247 |

117 figures want more than 333 px and stay capped; pinch-to-zoom covers
them, and a tighter crop of the widest scans (strips such as
`tr5s-figure-4-32-voltage-follower-21.jpg`, 1100 × 259 with 14 px labels)
would finish the job. No pan-and-scroll containers: panning a circuit is
worse than zooming it.

Verified live after the deploy by driving the page at the mobile preset:
the inline widths are on the page and the figures measure at the new
sizes. The decision was made on a mockup with two real figures at real
phone size, today against the two rules, sent to Roberto as an artifact
(*Figures on a Phone*); his answer was *Punch it*.

---

## #254 — the legibility pass over the version 9 text — **done and live, 3 Sep 2026**

Roberto's brief, late on 3 Sep 2026: read the version 9 documentation
end to end, mark anything old, out of place, verbose or convoluted, and
rewrite for clarity and economy; commit, build and upload without waiting,
so he can read it on the web in the morning; and keep a safety copy in
case he wants it all reverted.

**The safety copy is two things.** The git tag
`before-legibility-pass-2026-09-03` on commit `a08a1c8` (the sources with
#251–#253 applied and nothing from this pass), and
`C:\Users\perez\Claude Symbulator\Notes\docs_src_before_legibility_pass_2026-09-03.zip`
(`src/` and `book.yaml` at the same point). To revert everything from this
pass and nothing else:

    git -C "C:\Users\perez\Claude Symbulator\Documentation" checkout before-legibility-pass-2026-09-03 -- src book.yaml

then `py build.py --web` and the `learn` deploy. A single chapter can be
taken back the same way by naming its file.

**What changed.** Every chapter's version 9 rendering was read with
`tools/v9_lines.py` and the port-era prose rewritten in place — the same
rules as #251, applied to legibility rather than to a word list. The
kinds of change, with the reader's first page as the example:

- **Padding out.** *Nothing is hidden away: every answer it worked out is
  on the page, and reading them is a matter of scrolling and looking* →
  *with every answer it worked out*. *That is the right default for a
  machine doing algebra, and exactly what you want for…* → *That is what
  you want for symbolic results*. The split-view and input-file sections
  of the introduction lost about a third of their words and none of their
  facts.
- **Comparisons with the calculator that only a 7/8 reader could follow.**
  *Symbulator 9 has the same tool* (same as what? the 7/8 text above is
  hidden), *Symbulator 9 writes no such string for you*, *There is no
  stored `zeq` to divide by*, *the collision is impossible*, *Version 9 is
  not bound by the memory of a handheld*, *That is the difference a desktop
  makes*, the *Why the resistor is r on one calculator and r1 on the other*
  tip — all reworded to stand alone, or made 7/8-only.
- **Calculator vocabulary that had survived #251** in shared sentences:
  *the er script*, *the th script*, *the port script*, *the only tool*,
  *the plot tool*, *the rms flag*, *the fd gate*, *s\pr*, *s\plot()*, *My
  one-line solution*, *store it in a variable*, *ans(1)*, *described
  between quotations*, *with no leading comma*, *copy this equation into
  the clipboard*, *Ask for `{vc,ic}`*, *We get `{vs*µ/(µ+1),ro}`* — each
  now a `{{v7,8|…}}` span or an `::: only` block, the 7/8 words untouched.
  Lesson 6's two subheadings read *Limiting the results* and *Plotting an
  answer* in version 9 via spans in the heading, which work.
- **The card's real name.** *the **Plot** card* is the **Plotting Tools**
  card (#174), in Lessons 6 and 11. *approximate to n significant digits*
  is *approx to n digits*, the label the app actually shows, in Lessons 2
  and 3.
- **Restated values**, the #251 rule again: Lesson 4's `Req = 2.89 Ω …
  The value is 2.89 Ω`, Lesson 5's *We get r2=50000 and r4=20000* right
  after `50 kΩ and 20 kΩ`, Lesson 7's phasor repeated in prose, Lesson 8's
  `pmax` stated three times — 7/8-only or folded.
- **Two bugs in passing.** Lesson 6 described the TR analysis as *the
  `tr` function, which takes the circuit description and, optionally, the
  list of quantities you want back* — the Python API, not the app; it now
  says to set **Analysis** to *TR*. Lesson 2 pointed at a *Solve
  equations* card that does not exist (the card is **Solve**; the button
  is *Solve equations*).

**What was left alone, on purpose.** Roberto's own voice — the Joker, the
Swiss knife, *Booyah!*, *Your idea of fun, right?*, the fair-use
paragraph — and every shared sentence that reads fine in both versions.
The 7/8 text is byte-for-byte what it was, which is what
`check_against_originals.py` confirms: 75 verified (two more than before,
since two answers became blocks it can see), the same 23 not found.

**Numbers.** 11 chapters touched, 411 lines in and 544 out; `--check`
clean; deployed to `learn` from a `--web` build, 37 files, verified.

**The PDFs followed on 4 Sep 2026**, at Roberto's ask: full `py build.py`,
then a `learn` deploy of the three, each fetched and hash-checked against
the local build. **v9 is 236 pages** (241 before the pass), v7 **206** and
v8 **196** — those two gained a page each not from new words but from
paragraph splits, several shared sentences having become `::: only 7,8`
blocks. Verified in the built text, not assumed: *This process applies to*
present, *the calculator versions wrap* and *the er script* gone,
*Plotting Tools* present.

**A trap worth knowing: a stopped XeLaTeX run poisons the next build.**
The first attempt failed with `Runaway argument? … File ended while
scanning use of \@newl@bel` and *NO PDF PRODUCED for v9*, because
`build/tex/symbulator-v9.aux` was a 16,384-byte fragment — a buffer flush
cut mid-line when the previous night's build was stopped part-way.
XeLaTeX reads its own `.aux` back on the second pass and chokes. `build.py`
does not clear the intermediates, so the fix is to delete
`build/tex/symbulator-v9.{aux,toc,out,log}` by hand and build again.
**And `build.py` exited 0 anyway**, printing the failure to stdout while
returning success — so a caller trusting the exit code would have deployed
two fresh PDFs and one stale one. Read the output, or check the file
timestamps, rather than the status.

---

## #253 — an entry saves the Plotting Tools' inputs — **done and live, 3 Sep 2026**

Roberto's note from the session working on the input-file tool: the
inputs of the **Plotting Tools** card are saved in an entry like everything
else. The introduction's *What an entry remembers* said "the plot"; it now
names the card. One sentence, version 9 only (the whole section is).

---

## #252 — `::: web` / `::: pdf` blocks and `{{web|…}}` / `{{pdf|…}}` spans — **done and live, 3 Sep 2026**

Roberto asked for a "PDF only" and a "web only" tag, so a passage can
address one medium — a link that means nothing on paper, a page reference
that means nothing on screen. Two block directives and two inline spans,
the same shape as `only`/`not` and `{{v9|…}}`, in `build.py`:

- `walk()` takes a `medium` ("web" or "pdf") and flattens a matching
  block, drops the other. Each renderer passes its own medium; the search
  index is built as "web". **The label pass and `--check` pass no medium
  and see both**, so a heading anchored inside a `::: web` block is still
  a known label in the PDF — it resolves to the chapter rather than
  failing the build.
- `{{web|…}}` / `{{pdf|…}}` parse to an `mspan` node; each renderer emits
  it only when the medium is its own. The nested-span guard
  (`check_nested_version_spans`) covers them too: like a version span, one
  closes at the first `}}`, so no brace command inside.

Proved on a real build, not by reading: a throwaway paragraph in the
introduction with all four forms — the web build carried the two `web`
texts and neither `pdf` one, `--tex-only` the reverse, `--check` clean —
then the file was restored. Documented in `SPEC.md`'s two tables.

First use, at Roberto's ask the same day: the introduction's *If you are
reading this in the PDF, the links are on the web edition…* is a
`{{pdf|…}}` span now, reading *In the PDF, …* — the only passage in the
book that addressed one medium's reader (Lesson 6's *easier read on screen
than in print* is about the app's screen, not the PDF, and stays).

---

## #251 — the version 9 wording pass: no calculator, no "line", terse answers — **done and live, 3 Sep 2026**

Roberto's rulings of 3 Sep 2026, given twice: first to the wrong session,
which applied them, saved the diff as
`C:\Users\perez\Claude Symbulator\Notes\docs_legacy_wording_2026-09-03.patch`
and reverted; then here, with a second batch. The patch applied clean to
HEAD and was taken whole (rulings 1–9 below); ruling 10 and the second
batch were done on top. **Version 9 text only** — the 7/8 wording is frozen
as Roberto wrote it, so every shared sentence that changed went into a
`{{v7,8|…}}{{v9|…}}` pair or, where a `{{sub:}}` or `{{o:}}` sits inside,
into `::: only 7,8` / `::: only 9` blocks.

**The rulings.**

1. "It is already on screen." goes (Lesson 1, answer c).
2. **No "line", no "block" for a Results entry.** The reader is thinking
   about circuits, and a line is a conductor. Name the quantity or the
   variable instead: *the current through the source reads `ie` = −6 mA*,
   *`vr1` gives the voltage drop in the 30Ω resistor: 60 V*, *the current
   through any resistor*. "Value" is the fallback word, rarely needed.
3. Never "the computer" — Symbulator runs on phones. `book.yaml`'s
   `machine` term is *device* for 9; "ask the computer" became "ask
   Evaluate". Lesson 1 now says a solve takes *under a second on a
   computer, and maybe a bit more on a mobile* (Roberto measured 1.15 s).
4. The "add everything up and expect nothing" sentence goes.
5. "voltage drop areas" → "voltage drop in areas".
6. No command-line framing: "as an argument of the DC simulation command",
   "the command below", "the er script", "the th script", "three arguments"
   are 7/8-only now.
7. **No reference to the calculator anywhere in version 9 text**: the 20
   rounding notes read *Here we use **Rounding** — approx to n digits, with
   n = 3* (also in `tools/v9_calls.py`); the four "still describes the
   calculator" notes and the four comparison callouts are gone. Roberto's
   two "calculator-based simulator" remarks are 7/8-only rather than
   reworded, since dropping the qualifier would broaden the claim.
8. "the solve command" → "**Solve**" (the card); 9. "ex" → "expert mode",
   the section heading included (`{{v7,8|using ex}}{{v9|in expert mode}}`,
   the anchor unchanged).
10. **No curly-bracket answers.** `{.6,.2,.4,-2.}` is a calculator list;
    version 9 says *The answer is I1=.6 A, I2=.2 A, I3=.4 A and Vab=-2 V.
    This is correct.* 54 paragraphs split across lessons 1, 3, 4 and 5.
    Where the 7/8 text never named the values, the names come from the
    `The answers you want are …` line above (they were generated from the
    same calculator list, so the order matches) and the load quantities from
    the Evaluate box; units only where the prefix makes them certain
    (v → V, i → A, p → W, r → Ω), values verbatim as printed.
11. **No restated values.** *That is 6 kΩ. Correct.* right after `re` =
    6 kΩ is gone for 9 (kept for 7/8, where it follows the `6000` output);
    likewise *That is 6 mA*, and the five Lesson 7 *That is 4.789 A at an
    angle of −16.7°* sentences that repeated the `aa()` phasor just above
    them — those blocks now end *Correct.* The four after an unversioned
    `out` block (*That is 3.22 − j11.07 Ω*) stay: they convert 𝐢-notation
    and add the unit.
12. Answers say as little as will state the result. Lesson 1's answer (c)
    is *The voltage drop `vr1` reads 6 V, `vr2` reads 18 V and `vr3` reads
    12 V. All correct.*
13. The sources-only note ends at its statement; the tangent about
    resistors having no `rr1` (and the AC pointer) is 7/8-only.
14. Small ones: *This process applies to most* and *between them.* (no *in
    that order*) — these two in all three versions, at Roberto's word;
    *Those four element descriptions*; *which we defined as
    flowing in the opposite direction*; credits say open source since
    **2026**, not 2016.
15. **The SI prefix table** (Lesson 1, after "Symbulator has a shorthand
    for them"): word, shorthand, factor — the eleven prefixes
    `repos/solver/symbulator/si_prefix.py` accepts, peta to atto, `'k`/`'K`
    and `'u`/`'µ` both spelled. Version 9 only, since that file is the
    source; factors as powers of ten via `{{sup:}}`, which works in a cell.

**Lesson 6's calculator outputs.** Seventeen lines like `{ 6 , 0 }` sat as
bare paragraphs, visible in all three versions. They are `out 7,8` blocks
now, byte-identical inside, and version 9 reads the same values by name
(*`vc` = 6 V and `ic` = 0 A*). That is why `check_against_originals.py`
moved from 11 not-found to **23**: it never examined a bare paragraph, and
six of the seventeen — `{8,0,8}`, `{6,0,12}`, `{2,0,2}`, `{10,0,-10}`,
`{10,0,14}`, `{9,9/4}` — are not in the 2023 pages in any spacing. The
values were not touched; they were simply never checked before.

**The PDFs are behind, on purpose.** Deployed with `--web` — Roberto
started a full build and then held it ("Don't build the PDFs yet"). This
changes typeset text on every lesson, so **the live PDFs still say
"line" and carry the calculator notes** until the next full `py build.py`
and `learn` deploy. `SPEC.md`'s span example still reads "the **current
through** line" — it documents markup, not the book.

**Tooling.** `tools/v9_lines.py REGEX [--para] [files]` prints the lines
version 9 actually renders — fences with a version list, `::: only`/`not`
blocks and single-line spans all honoured. It found everything above; the
plain grep had been reporting 7/8-only text as leftovers. Run it with
`PYTHONUTF8=1` on Windows or the first Ω kills it.

---

## #231, #233, #234 — the docs side of the fine-tuning batch — **done and live, 3 Sep 2026**

Three of the nine items from Roberto's round of 3 Sep 2026; the other
six are app-side and written up in `Application/v9/repos/local/NEXT.md`.

### #231 — the split view's wordmark is one colour

`web/split/index.php`. It read **Sym**bulator in two tones — "Sym" white,
"bulator" sky — because a span carried over from another lockup coloured
half the word. The whole word is sky now and the **numeral is white**,
so the contrast falls between the name and the version rather than down
the middle of the name (Roberto's A1: the 9 stays white).

The colour has to be stated on `.mark` rather than left to inherit:
`.splitbar a` paints every link in the bar white.

While in there, the bar's own default position label said *Tutorial*.
It says *Documentation* now, for #232's consistency.

### #233 — the landing hero says it is a beta

The gold **New!** chip stays; the line beside it reads *Symbulator 9, in
beta version, for Python and SymPy*. Roberto's A4 — keep the chip, add
the state in words — which happily avoids a problem the alternative had:
`landing.css:20` says in as many words that gold means *"new", and only
that*, deliberately not amber. Had the chip itself become "Beta", that
comment would have turned false and `chip-new` would have become a
misnomer. Nothing renamed, no CSS touched.

Commas rather than a bare insertion: *"Symbulator 9 in beta version for
Python and SymPy"* runs on without a breath.

### #234 — the split view offered on the landing page

A second entry under *Learn it*, below *Read the documentation* — second
on purpose (A8): reading the documentation is the plain way in, and this
is the one that needs a sentence of explanation.

    THE DOCUMENTATION AND THE APP, SIDE BY SIDE
    Read and run at the same time →
    Every lesson on the left, the live app on the right. Each worked
    problem carries a link that loads that exact circuit into the app —
    read the explanation, then run it without typing a character.
    learn.symbulator.com/split/

Title names the benefit rather than the feature (A7): "split view" means
nothing to someone who has not seen one, and the kicker underneath says
what it is. **No CSS was needed** — every `.way` on the page is already
`way-wide` and `.ways` is a single-column grid, so the two simply stack.

---


## #230 — A regex that could never match, and the checker that could never see it — **done 3 Sep 2026, nothing to deploy**

`build.py`'s `plain()` — the function that reduces a rendered page to its
words for the search index — carried two literal control bytes where a
word boundary and a backreference had been written. The pattern still
compiled and simply never matched, so its script/style stripping had not
fired once since the line was written. Harmless only because no chapter
contains a script tag; a guard that cannot go off is not a guard.

**The checker for this exact failure had the same blind spot as the
bug.** `tools/check_control_chars.py` exists because a shell heredoc once
ate backslash escapes in two chapters — its own docstring says so — and
it was scanning `src/*.md` alone. It now scans `build.py` and
`tools/*.py` as well, collapsing CRLF first so a Windows line ending is
not a finding while a lone carriage return still is.

Proved in both directions rather than assumed: the repaired pattern
strips `<script>` and `<style>` bodies and leaves `<scriptural>` alone,
the word boundary doing its job; re-damaging `build.py` on purpose makes
the widened checker report both bytes on line 1146 and name the intended
escape, and restoring it goes green again. **All three `search.json`
files are byte-identical after the rebuild** — the repair changes nothing
that ships, which is why there is nothing to deploy and the `learn` dry
run reports 0 files.

And the bug reproduced itself during the fix: the first attempt at the
CRLF line wrote a real carriage return into the checker, the escape eaten
passing through a nested shell string. Which is the best argument
available for scanning the tools as well as the prose.

---


## #226 — "Split View" in the ribbon — **done and live on learn, 2 Sep 2026**

Roberto, 2 Sep 2026: replace *How it works* in the ribbon under the
banner with **Split View**, taking the reader to the split view of the
page they are already on.

The link carries `?page=<chapter>` rather than a lesson and an entry,
because the reader has not picked a problem — they have asked to see
this chapter beside the app. `/split/` grew a third way in for it: the
left pane opens on that chapter, and the right pane opens on the
chapter's **first book**, so Lesson 6 opens the app on Lesson 6's
entries rather than on whatever it had last. A chapter with no book of
its own — the introduction, the credits — leaves the app at its default.
On the home page there is no chapter to carry, so the link says
`?page=introduction`.

**Versions 7 and 8 keep the old link.** There is no split view for them:
the app *is* version 9, so a "Split View" link on a version 7 page would
quietly move that reader onto version 9's documentation — the exact
opposite of "the same page where they are". This is the one deliberate
departure from "replace it", and it is worth a second look if the
ribbon is ever revisited.

Two things the implementation turned up:

* **`lessons.json` now writes both directions of the map.** Inverting
  one of them in the page would not do, because JavaScript does not keep
  an object's key order for keys that look like array indices:
  `{"1":…,"10":…,"4a":…}` comes back as `1, 10, 4a`, so "the chapter's
  first book" would silently have been the wrong one for Lesson 1
  against Lesson 10. Both directions are generated from `CHAPTER_BOOKS`.
* **The bar shows the chapter's own title**, carried in the `ready`
  message. Only the pane knows it: deriving *Transient analysis* from
  `lesson-transient` is guesswork, and wrong in every language the book
  is ever set in. Clicking an entry then switches the bar to
  `Lesson 6b · entry 3` and the URL to `?lesson=6b&entry=3`, so a split
  view opened on a chapter stays shareable at whatever the reader
  reaches inside it.

Verified live on `learn.symbulator.com`: the v9 ribbon links
`/split/?page=lesson-transient`, the v9 home page links
`/split/?page=introduction`, and the v7 ribbon still reads
*How it works*.

---

## #224 — The split view, and an app link on every worked problem — **done and live on learn, 2 Sep 2026**

Roberto's brief, 2 Sep 2026: a page that shows the documentation and the
live app side by side, and a link on every worked problem that loads that
problem's circuit into the app. Entirely a docs-tree item — **the app
tree is untouched**, no cache bump, no solver release, no PDF rebuild.

### What is where

| | |
|---|---|
| `tools/app_links.py` | the join: which app entries a worked problem is. Run it on its own for the coverage report |
| `build.py` | `HtmlRenderer.problem_furniture()` emits the anchors and the links; `chapter()` resolves a chapter up front; `plain()` keeps the link text out of the search index; `build_web()` copies `split/` and writes `split/lessons.json` |
| `web/split/index.php` | the shell. Two iframes, a draggable divider, the postMessage protocol documented at its head |
| `web/index.php` | the embedded-mode script at the foot: link interception, and the scroll that has to survive a chapter still settling |
| `web/assets/style.css` | `.problem-links` and the `html.embedded` rules |
| `src/00-introduction.md` | § *Reading and running side by side* |
| `deploy_targets.ini` | verifies `/split/` renders and `lessons.json` is there |

### The join, and why it takes six stages

The chapters and the `.cir` books were written separately and never
numbered against each other: Lesson 6 is 51 worked problems in the book
against 80 entries in its four books, because a transient problem is
usually a DC pass for the initial condition and then the TR. So the
match is made on content, and **neither available key works alone**.
The figure (`image:` on the entry, `::: figure` in the chapter) matches
248 of 280 and *over*-collects — the two entries of `AS2's Example 5.7`
carry the figure of `AS2's Figure 5.24`, being four elements deep inside
that drawing. The title matches a different 262 and misses wherever the
chapter and the book word the distinction differently.

Six stages, most specific first, each entry claimed once. Two of them
are there for one case each and both were found by the coverage report
rather than by reading:

* **stage 0**, before the exact-title match: a title the chapter uses
  *twice* is two problems. Lesson 4 walks through `B11's Example 8.29`
  in Part 1 and sets it again in Part 2, and each part has its own book.
  Without this the first occurrence took both entries and the second got
  none.
* **stage 3b**, after the specific title stages: several problems still
  sharing a base, none of which named its entry recognisably — Lesson
  2's *with solve* against *using ex*. It runs after stage 2 so that a
  problem which *did* name its entry has already taken it, which is what
  keeps Lesson 5's `(Subtractor)` from being handed its sibling's
  drawing.

**308 of the 310 lesson entries are linked.** The residue is real and
was checked one by one, not assumed: 15 problems have no entry (the
Bode sketches of AS7 14.3–14.5, worked with pencil and paper; the AS7
2.10 pair this file already records as having no v9 content; AS7's
9.37; AS2's 2.9 and 2.11 pairs; `AS2's Practice Problem 5.7`; the
Showing-off Problem) and 2 entries have no worked problem (`B11's
Example 7.4`, which the chapter only mentions in passing, and Lesson
11's `A low-pass RC`, which is Claude's own demonstration).

### Two anchors, doing different jobs

`prob-<slug>` on the section, so every problem can be linked to,
including the fifteen with no entry. `e-<lesson>-<entry>` on each
*link* — `e-6a-3` — so the shell can derive the anchor straight from
`?lesson=6a&entry=3` with no lookup table. The entry anchor cannot live
on the section because a problem is often several entries and only one
could own it.

### Three bugs the harness found that reading would not have

There is no PHP on this machine, so the panes were served by a harness
that strips the PHP and lifts the embedded script out of `index.php`
verbatim. All three of these were invisible in the source and obvious
within a minute of driving the real thing:

1. **`scroll-behavior: smooth`.** style.css sets it on the root, so a
   `scrollIntoView()` with no behavior of its own *animates*, and each
   correction restarted the animation before the last one arrived. The
   pane parked a few hundred pixels into a five-thousand-pixel journey
   and stayed there — indistinguishable from a message never delivered.
   Every scroll in the embedded script now says `behavior: 'instant'`,
   which overrides the CSS property; `'auto'` defers to it, which is
   what made this so quiet.
2. **The page is still growing when the scroll is asked for.** A circuit
   scan is an `<img>` with a width and no height, so it reserves
   nothing; the fonts load with `display=swap` and re-flow everything;
   KaTeX then typesets the maths. Fixed timers were tried and are not
   enough — a run that stopped correcting at 1.2s sat 39,000px past its
   problem, and a later one left a title clipped 37px above the top
   edge. The correction is now driven by a `ResizeObserver` on the root:
   whatever changes the height last has the last word, and it lets go
   after six seconds or as soon as the reader moves.
3. **Scroll restoration.** Reloading the shell made the browser restore
   the *iframe's* previous position, which beat the anchor. The embedded
   page sets `history.scrollRestoration = 'manual'`: the shell always
   says where the pane should be, so remembering where it last was can
   only contradict it.

Measured after each fix rather than assumed, and swept across seven
entries in two books rather than the one that proved it: every problem
lands at exactly 12px from the top of the pane.

**A fourth appeared only once it was live**, and is the sharpest of the
four. The `ResizeObserver` gave up after a fixed six seconds, which was
comfortably enough locally — and on the deployed site left Bo2's Example
5.1 sitting 505px down the pane, because Lesson 6's 49 scans come off a
disk in well under six seconds and over a network they do not. It now
stops when the height has been *still* for 1.5s, with a 20s backstop.
Re-measured live across all four books of Lesson 6: every one at 12px.
A local harness proves the mechanism; only the real host proves the
timing.

**And twice the measurements were zero because the browser pane was
hidden** — `innerWidth: 0`, every rect 0 — which is the trap already
written up in the top-level `CLAUDE.md`. The second time it was not the
pane at all but the mobile layout doing its job: clicking an app link on
a narrow screen switches to the app tab, which hides the docs pane, so
the docs document legitimately had no layout to measure.

### The walkthroughs have no link, and must not get one

Links attach to `::: problem` blocks. A chapter that teaches by having
the reader *type* a circuit — a `field 9` block, like Lesson 1 §1.1
*Run a direct current analysis* — gets none, and that is correct rather
than an oversight. Roberto, 2 Sep 2026, asked whether §1.1 had been left
out deliberately and then settled it: **"It's a manual example. It's
meant to be manual."** The section exists to make the reader type the
circuit; a button that loaded it for them would remove the exercise.

The circuit itself is not unreachable — §1.1's is `Lesson_01.cir` entry
1, linked from §1.5 where `::: problem B11's Example 5.7` presents it
formally. So the gap is only at first contact, and it is the point.

Written down because it looks exactly like a bug from the outside: a
future pass counting links against `field 9` blocks will find these
missing and be tempted to fix them. Do not.

### Still open

Nothing blocking. Two things a reader may raise once it is live:

* Clicking a link **reloads the app pane**, discarding anything typed
  there. Roberto's decision, 2 Sep 2026 — "what the user is doing is
  saying: show me the app and load this entry" — and the introduction
  and the shell's own bar both warn about it. Keeping the app alive
  across clicks would need the app to accept a `postMessage`, which is
  an app-tree change with a cache bump and a five-site deploy behind it.
* The new introduction section is prose in `src/`, so a **full** PDF
  build would print it. It is worded to be true in print (it says the
  links are on the website, and points a PDF reader at
  `learn.symbulator.com`), but there is no web-only gate in the markup
  and adding one would be a change to SPEC.md's directives.

---

## #220 — Units of measure across lessons 1–13 — **done and live on learn, 2 Sep 2026**

Roberto's findings list, worked prose-only: no circuit description, no
`'k`/`'m`/`'µ` inside an Evaluate or Solve block, no variable names.
Nine `src/*.md` files, 48 lines.

**Three that were wrong.** Lesson 6, Bo2's p224 5.2 called a voltage
source "12A"; it is 12 V. Lesson 3, TR5's Example 4.4 called the
transconductance *g* "100mA" — a current, for a quantity measured in
siemens; it is 100 mS. The same problem's answer read `RIN=10.95'kΩ`.

**The apostrophe leaking out of the input language.** `'k` is how a
value is *typed*; it is not a unit and does not belong in a sentence.
Lesson 4 (RM3's 9-7, B11's 9.15), Lesson 5 (AS2's 5.3 and 5.7 with both
practice problems) and Lesson 3 all had it, in both the straight and the
curly apostrophe — `10'kΩ` and `10’kΩ` are the same mistake and a search
for one will not find the other.

**Consistency.** Lesson 1's B11 6.13 gave I₃ as "0.02 A" beside siblings
in mA. Lesson 9 spelled the reactive-power unit "VAR" twice; SI and IEEE
spell it `var`. Lesson 11 mixed rad/sec and rad/s across seventeen
places.

### Three findings the list did not survive contact with

**`ap_` is average power, not apparent power — the report was inverted.**
The list asked for Lesson 7's AS7 Example 9.9 to be rewritten so that
`pe`/`pr1` held average power and `ape`/`apr1` apparent power. The
chapter was right and the change would have broken it.
`analysis.py:211` reads `out[f"p_{e.name}" if use_rms else
f"ap_{e.name}"] = sp.re(s)`: **both names hold the same quantity**, the
real part of V·conj(I), and which one is used depends only on the RMS
setting — `ap` for peak-amplitude phasors, `p` for RMS. The app agrees
(`_ELEMENT_KEYS` in `symbulator_ui.py` labels `ap_{n}` "average power",
in W) and so does Lesson 8's own text. "None is given for the capacitor"
is right too: `p_`/`ap_` are emitted only for kinds `e`, `j`, `r`, `o`.
Lesson 7 was left alone. What is actually wrong is the solver README —
**#223**.

**Two "rad/sec" were kept on purpose.** In `s\bode()` the calculator
offers a literal choice reading `in Hz` / `in rad/sec`
(`symbulator_calculator/decoded/v7_programs_partial.txt:436`). Renaming
those two would send a v7/v8 reader hunting for a menu entry that does
not exist, so they are italicised as the UI labels they are. Every
*measurement* in the lesson is rad/s.

**v9 ships with SI prefixes off**, so mA and kΩ in a sentence that
narrates the screen describe a screen the reader does not have.
`<input type="checkbox" id="siUnits">` in `templates/index.html` carries
no `checked`. Lesson 1's bullet is a summary and reads in mA; Lesson 2's
B11 6.19 quotes the **current through** line directly and was left at
`−0.02 A` for that reason. Anything that later turns the setting on by
default makes this a real inconsistency rather than a considered one.

Verified by `build.py --check` (clean), `tools/check_against_originals.py`
(unchanged at its baseline, 73 verified / 11 not found — it reads `out`
blocks, so prose edits do not move it) and by grepping the built pages
for each changed string.

**Live on learn, 2 Sep 2026**, pages and PDFs both, and verified on the
*served* pages rather than on the build: 12 V, 100 mS, 10.95 kΩ, the kΩ
conversions in lessons 4 and 5, `I₃: 20 mA`, `var` twice, nine `rad/s`
with the two dialog labels still `rad/sec` on v7 only, `0.4 S` and
`4 Ω`. No `'k` or `’k` left anywhere in prose. The host was pruned the
same day of 278 orphans left from the placeholder era; remote count is
now 662, matching local exactly, with all 316 asset references
resolving.

---

## #221 — `\*` is an escape now, and always should have been — **done and live on learn, 2 Sep 2026**

`build.py`'s inline parser had no escape mechanism at all, while the
sources have been writing `\*` for a literal multiplication sign since
the conversion. Eleven lines across four lessons were affected and the
damage was not local to them.

`INLINE_RE`'s strong rule was `\*\*[^*]+\*\*`. In
`**{.904\*vs,10952.}**` the interior `*` makes that fail, so the scan
falls through to the em rule, which matches `*{.904\*` — and every
star for the rest of the paragraph is then paired one position out of
step. The sentence in TR5's Example 4.4 rendered as *"is correct: v*<sub>O</sub>*
=.904 v"* with the italics shifted a span to the right and a bare `*`
left sitting before the full stop. In the PDFs it was worse: `tex_escape`
maps `\` to `\textbackslash{}`, so the backslash printed.

The fix is an `esc` alternative, `\\[*\\]`, plus `(?:\\[*\\]|[^*])+` in
place of `[^*]+` inside strong and em, so an escaped star no longer
terminates a span.

**The escape set is deliberately two characters, not a general `\.`.**
A backslash is ordinary content in this book: the calculator's namespace
is spelled `s\dc`, `s\tr`, `s\rms`, `s\pf`, `s\bode`, and a general
escape would silently swallow every one.

### The atom order is the whole trick, and the first version got it wrong

The obvious spelling of that atom is `(?:[^*\\]|\\[*\\])` — escape or
non-special character — and it is **wrong**, because `[^*\\]` bans a
*lone* backslash from emphasis altogether. `**s\bode**` stopped being
bold, along with every other `**s\...**` in the book. Nine built pages
moved that had nothing to do with `\*`.

`(?:\\[*\\]|[^*])` is correct and the order is load-bearing: the escape
alternative goes first so `\*` is swallowed as a unit and its star
cannot close the span, and `[^*]` then still admits a bare backslash as
ordinary content.

**Nothing in the source told me this. The diff did.** The change was
verified by building the site twice — once with `build.py` stashed, once
with it restored — and diffing the two trees. The first run touched
lessons that contain no `\*` at all, which is what exposed the
regression; the second touches exactly the four lessons that do
(equivalents, opamps, sources, transient) plus the three search
indexes, and every hunk in them is one of the eleven lines. A parser is
another artefact whose model you cannot read the truth off.

Documented in `SPEC.md` under *Escapes — and the two characters that are
not escapes*.

**It exposed one content bug the moment it went in.** TR5's Example 4.8
in Lesson 4 read `**{vs\*µ/(µ+1**),**ro/(µ+1)}**` — a stray `**` in the
middle of the braced pair, which the broken parser had been hiding.
Corrected to one bold span.

This is the docs-tree instance of *measure the artefact, not the model
that produced it*: the parser was self-evidently fine from the code, and
only the rendered page showed that eleven paragraphs were being mangled.
Nobody had looked.

### The PDFs, and an ohm that is not the ohm you typed

Roberto lifted the `--web` standing instruction for one run so the
typeset half would stop disagreeing with the web half — `tex_escape`
maps `\` to `\textbackslash{}`, so every `\*` had been *printing* a
backslash in all three books. Rebuilt and deployed 2 Sep 2026: **0
occurrences of `\*` in the v9 PDF text**, `{.904*vs,10952.}` and
`r2*r4/(r1*(r3+r4))+r4/(r3+r4)=3` and `3*v2-5*v1` all correct. v9 is
**241 pages**, one more than before, from the added units and two
rewrapped sentences; v7 and v8 are unchanged at 205 and 195. All three
hash-verified against the local build.

**A built PDF encodes Ω as U+2126 (ohm sign), not the U+03A9 that is in
the source.** Two of the verification probes came back as misses on that
alone, and a book that was entirely correct looked broken for as long as
it took to print the codepoints. Normalise, or search for both, before
concluding anything about a PDF from a grep.

---

## #222 — Units on the bare answer lines — **done and live on learn, 2 Sep 2026**

Many solved-example answer lines carried no unit at all. #220 did the six
Roberto named — Lesson 1's B11 7.11 (V and A), Lesson 3's Bo2 1.9, AS2's
Practice Problem 2.7 and Bo2's 1.10 (V and A), and Lesson 13's Gain
Examples 1 and 2, whose y and z parameters had no S or Ω (the app's own
`_PORT_UNITS` is `{"z": "ohm", "y": "S"}`; the gains stay bare because
they are dimensionless). This is the rest of it: **41 edits across ten
chapters**, every unit decided from what the quantity *is* — the element
kind behind the name, or the analysis — and never from the shape of the
number.

The bulk is Lesson 9 and Lesson 7, where nearly every `aa()` reading was
a bare polar pair: `aa(iraa)` reads 2.35∠−36.2°, with nothing saying
amperes. A list gets one unit at its end (`… and 42.76∠−155.1° A`,
matching the `… and −18280𝐢 VA` already in the book); a sentence pairing
two different quantities gets one each (`aa(vro) … ° V and aa(ico) … °
A`). Lesson 7 corroborates that pair itself in the next sentence — "That
is 1.55 V at −95.18° and 3.26 mA" — which is the kind of check worth
looking for before stamping a unit on anything.

### What was deliberately left bare, and why

This is the more useful half of the item. Six kinds of answer take no
unit, and stamping one on them would have been the error:

* **Power factors** — Lesson 8's four (`0.97342 leading`, `0.93595
  lagging`, `0.99805 leading`, and the `1` at unity). Dimensionless by
  definition; *leading* and *lagging* are the qualifiers, not units.
* **h and a two-port parameters** — Lesson 13's 19.6 and AS7's 19.8.
  `h11` is Ω, `h12` and `h21` are dimensionless, `h22` is S; for the
  transmission parameters A and D are dimensionless, B is Ω, C is S.
  Mixed by construction, which is exactly why the app's `_PORT_UNITS`
  units z and y and nothing else. The y quadruples beside them *did*
  get their S.
* **Gains** — Av, Ai, Ap, Gv, Gi, Gp. Ratios.
* **Symbolic answers** — `vth = vs*(r1 + r2)/r1`, `r2 = 5*r1`,
  `((g1-g2) vs)/(g3-g4)`. They carry their units in their symbols;
  stamping V on a formula in terms of `vs` tells the reader nothing.
* **Infinity** — the ideal op-amp's `ino` and `pmax`. Not measurements.
  (`req` = 0 sits in that same list and is genuinely ohms; it was left
  alone so the list does not carry one lone unit among four entries
  that cannot. Marginal either way.)
* **`c` = 25 in Lesson 7's Example 9.14.** The circuit line is
  `c,1,0,c'µ`, so the unknown being solved is the *coefficient of the
  multiplier*, not the capacitance. "25 µF" is true of the capacitor and
  false of `c`, and writing it would be a different claim from the one
  the app makes. This is the trap #220 named — a name whose prefix does
  not say what it measures — and it is the single most interesting line
  in the sweep.

### The scanner was wrong twice before it was right

Worth recording, because the same mistake is available to anyone who
repeats this.

The first pass flagged **238** bare markers by asking whether a unit
followed each `{{o:}}` immediately. That is the wrong question: in
`{{o:6.809}}∠{{o:-21.8}}° A` the magnitude is covered by the unit after
the angle, and in `{{o:-1054}} − {{o:842.9}}𝐢 VA` the real part is
covered by the one after the imaginary part. Rewritten to scan forward
to the end of the answer phrase, it said **152**.

Then it said 128, then 102, and the difference was a bug: the scan
treated the `:` **inside a following `{{o:...}}` marker** as a colon
ending the sentence, so any answer followed by another answer looked
unitless. Markers have to be substituted out *before* the sentence scan,
not after. Order matters, and the 26 phantom hits all looked perfectly
plausible in a list.

What survives is `tools/`-worthy but was not kept: the population is
small enough that the real work was reading all 73 lines, and the
scanner only ever narrowed the field.

### Verifying it in the PDF: two glyphs that are not the glyphs you typed

The rebuilt PDFs (205 / 195 / 241 pages, unchanged — #222's additions
were too small to move pagination) confirm every unit, but only once the
probes were right, and they were not right first time.

* **Ω extracts as U+2126** (OHM SIGN), not the U+03A9 in the source.
* **∠ extracts as U+0338** (COMBINING LONG SOLIDUS OVERLAY), not U+2220.

Both make a perfectly correct book grep as broken: `42.76∠-155.1° A` is
in the PDF and searching for it by the source's characters finds
nothing. Normalise, or search for a fragment either side of the glyph,
and print codepoints before concluding anything. Between #221 and #222
this cost five false misses.

---

## #216 — Appendix B, redrawn — **done and live on learn, 1 Sep 2026**

Appendix B of *The Internal Logic of Symbulator* is not artwork: it is
seven circuits rendered by the v9 schematic engine itself, through
`paper/render_exemplars.py`. That drawer changed on 1 Sep 2026 (#213 —
the reference marks and the typeset values) and again the same day
(resistors 20% smaller, dependent sources 10% larger), so the appendix
was showing a hand the app no longer uses. Regenerated, and the
monograph rebuilt: **45 pages**, was 44.

**The script no longer keeps its own copy of the circuits.** It reads
them from the app's example book, `repos/server/examples/The_Monograph.cir`,
by entry name — the same seven entries the reader meets in the app,
drawn by the same drawer. The duplicate copy is exactly what drifted
when Roberto restated the showcase's controls (#215) and this file
stayed as it was; a rename on either side now fails the script loudly
instead.

### Two bugs it found, both only visible in the rendered page

**Every resistance in the appendix has been printing as `10 |`.**
Helvetica is a Type 1 face in WinAnsi: no omega, no pi, no angle sign,
and reportlab draws what it cannot encode as a bar or as nothing. The
SVGs had all four characters correct the whole time — it was the PDF
conversion that lost them, and only a rendered page shows it. This has
been true since the figures were first generated on 28 Aug 2026. Fixed
by embedding DejaVu Sans (upright and oblique), through
`svglib.register_font` rather than reportlab's own `registerFont`:
svglib keeps a separate map from an SVG `font-family` to a face, and a
family it does not know falls back to Helvetica silently — which is
what the first attempt at the fix did, omegas still missing and nothing
said. Adobe's Symbol font, tried before that, drew blanks: svglib will
not honour a per-tspan `font-family` switch.

**The labels are now laid out here, not by svglib.** With DejaVu
embedded, `J` and its subscript `D1` came out on top of each other
while `R` and its `5` were fine: the advance svglib used was not the
advance it drew with. Rather than chase which metric it was reading,
every run is measured against the same reportlab face the page is drawn
in and handed over already positioned, `text-anchor="start"`. Two
details that cost a round each: a label's own anchor has to be honoured
by measuring the whole label first, and the renderer strips a run's
outer whitespace (Unicode-aware, so a no-break space does not survive
either) — so a run is drawn without its outer spaces, at its own x plus
the width of the leading ones. The mutual-inductance caption read
`M=  1H(couples  L1and  L2)` until it was.

### §5.2 follows the example, on Roberto's ruling

#215 renamed the showcase's unknowns to `es` and `js`, which left §5.2's
prose saying `vs` and `is` two pages before Figure B.2 showed sources
valued `es` and `js` — a document contradicting its own appendix.
Roberto ruled that the prose should follow the example (1 Sep 2026), and
it does: the symbols are now $E_s$ and $J_s$, the verbatim listing is
the shipped description character for character (`es,e,0,es`,
`jd1,a,b,0.2vr7`, `ped2 = 0`, `conditions: es > 0, js > 0`), and the
`is` footnote survives as what it always was — the story of solver
0.5.19 shielding Python keywords — reworded to say the names *were*
`vs` and `is` when the chapter was drafted, and that which name the
example ships under is a matter of taste rather than of what the reader
may write. The closed forms are untouched.

The listing was the easy thing to miss: §5.2 quotes the circuit twice,
once in prose and once in a `tabbing` block, and only the prose was
caught on the first pass. It showed up by reading the rendered page.

Deployed: `py deploy_symbulator.py learn` uploaded one file
(`monograph.pdf`, 1,019,308 bytes; 661 already identical) and verified
it by fetching — the live PDF hash-matches the local build. **45 pages**,
was 44.

---

## #195 — the monograph and the solver agree about levels — **done, deployed**

Roberto, 30 Aug 2026: *"I want the solver's code to match the monograph.
The monograph and the solver should match in the sense that someone using
the monograph will not find that the package code contradicts it, or
viceversa."*

Two halves: the monograph, rewritten by Fable 5 who wrote it; and the
solver's comments, brought into line here.

### How it started: degrees were never a second taxonomy

Roberto: the monograph distinguishes *degrees* from *levels* of variables,
but that distinction is a translation artefact — he said "degrees" when
explaining it, his friends' translation of the thesis said "levels", and
Fable took the coincidence for deliberate precision and built an apparatus
on it, including a paragraph reconciling the two.

It was worse than redundant. The invented degree taxonomy **contradicted
the thesis the monograph cites**, on three counts:

| | thesis §4.2.3–6 | old monograph |
|---|---|---|
| voltage-source current | first level | second degree |
| current-source current | second level | first degree |
| voltage drop | second level | third degree |

Fable's own account of how: the degree scheme classified *by kind of
quantity* — voltages, then currents, then derived — under which every
branch current is second by construction. When that collided with the
thesis's explicit first-level listing, it read the collision as two
deliberate taxonomies rather than as its own error.

### Roberto's ruling: classify from the code

He asked Fable to justify the second-degree classification, openly allowing
that he might be the one who was wrong — *"Maybe Fable is right and I was
wrong."* He was not. `_stamp_e` appends the voltage source's current to
`self.unknowns`; `_stamp_j` puts the current source's into `self.known`
with *"no new unknown or equation needed at all"*, adding the value into
both nodes' KCL sums as a plain term — which is exactly the mechanism
Roberto described from memory. Thesis and code agree; the monograph was
alone.

He then ruled that the monograph should classify **by what the version 9
code does**, not by the thesis. That matters for one item: the port
computes voltage drops in `analysis._derived`, the same round as the
powers, where the thesis keeps them as second-level standing expressions.

One correction went the other way. Roberto thought voltage drops post-dated
the thesis; §4.2.4 has them, as second-level variables, with a census —
*"7 caídas de voltaje en las 3 resistencias y las 4 fuentes"*. His memory
was right about the half that mattered, though: §4.2.5 says drops are
among the expressions deliberately **never evaluated**, so in 2000 a drop
existed as a classified expression but never as a stored answer. Version 9
evaluates it. **The quantity changed status between the calculator and the
port**, which is why the two authorities disagree, and the monograph now
says so.

### The monograph, as it stands

Classifies by the code, and states both departures from the census in
§4.3 with citations rather than smoothing them: resistor currents (second
level on the calculator, stamped into the simultaneous solve here) and
voltage drops (second-level standing expressions in the thesis, computed
after the solve here, beside the powers and the seen resistance "an answer
the census never reached at all"). The thesis-census paragraph is left
intact as the thesis's own account. Roberto's KCL-term point is now in the
exposition. 26 + 11 edits, two clean `xelatex` passes, **44 pages before
and after**.

Deployed to `learn.symbulator.com/monograph.pdf` and verified live by hash.

### The solver's comments

Six sites mention levels; eleven other hits for "degree" are angles — Bode
phase, schematic labels, the `100<30 degrees` input syntax — and were left
alone. Of the six:

- **`engine.py`'s `_expand_solution` comment was wrong twice.** It called
  `circuit.known` *"Third-level"* (those are substituted, second level) and
  offered *"an op-amp's output current"* as an example — but `_stamp_o`
  appends `i_out` to `self.unknowns`. Measured: `known` is populated in
  exactly two places, `_stamp_c` and `_stamp_j`, and nowhere else.
- **The module design note** was right about the calculator and silent
  about where the port lands; it now names the resistor-current departure
  and points at the monograph's §4.3.
- **`analysis._derived`** now says "third level" is this port's rule —
  whatever the round derives — and records that the thesis counts only the
  powers and keeps the drop at second level.

Comments only: no behaviour change, **311 solver tests pass**, and no
release is implied. The repo sits one commit ahead of PyPI 0.5.22 with
identical behaviour, so version X, which runs the published package, is
unaffected.

---

## #194 — version 9's TR steps are its own — **done, deployed**

Roberto, 30 Aug 2026, asked whether any references to **`ex`** — the
calculator's expert-mode call — survived in the version 9 documentation.
He had seen some a while back; a clean-up pass by Fable 5 since then had
caught most of them.

Measured on the **built v9 pages**, not the source: the source legitimately
contains `ex` inside `{{v7,8|...}}` spans, because versions 7 and 8 really
do call `s\ex`. Exactly **one** survived in v9, in "Advanced use of Expert
in TR" — *"two things you need to know in order to use `ex` like a boss"*.
Now `{{v7,8|`ex`}}{{v9|expert mode}}`. Version 7's eleven are untouched and
correct.

### The larger fault underneath it

The three steps immediately below that sentence were **ungated**, and they
describe **Impala** — the version 4 trick of stamping a placeholder for a
time-varying source, solving, then substituting the real value back:

> Generate a set of equations and unknowns for the system, in the frequency
> domain. *Any time-dependent source is replaced with a dummy variable.*
> … *Replace any dummy variable with the original source value*, and
> convert the answers to the time domain.

True of versions 7 and 8. **Not true of version 9**, which has no Impala
and needs none: `laplace.tr()` calls `_sources_to_s(desc)` and moves every
independent source into the s-domain *before* stamping, so no placeholder
exists at any point (established the same day, while fixing #176's TR
stamp — see `NEXT.md`). Ungated, the block taught a version 9 reader the
calculator's algorithm as their own.

The old steps are now `::: only 7,8`, where they are right, and version 9
has its own:

- Move every independent source into the frequency domain, and generate a
  set of equations and unknowns for the system there.
- Solve these frequency domain equations.
- Convert the answers back to the time domain.

Deliberately three steps with the same shape, because the sentence after
them — "the expert tool freezes this process halfway between steps 1 and
2" — has to stay true in both versions, and it does.

### Deployed

`learn.symbulator.com`, 30 Aug 2026, **with v9's PDF rebuilt at Roberto's
explicit ask** — an exception to the standing `--web`-only instruction at
the head of `README.md`, not a lifting of it. v7 and v8 need no PDF: their
text did not change, only its gating. Three files, 27 MB.

Verified live: v9 says *Move every independent source* and has no *dummy
variable* and no *use ex like a boss*; v7 still has all three; the v9 PDF
on the server matches the local build by hash. Guards clean — 241 pages,
zero LaTeX errors, `check_white_text` clean, 73 blocks verified against the
originals with the same 11 not found, control chars and palette clean.

---

**#192 and #193 deployed together, 30 Aug 2026** — the first `landing`
deploy since the #140–#157 day, and it behaved: one file, 20,848 bytes,
13 already identical, and the whole diff was the four intended lines (7
insertions against 6 deletions, the extra one being the re-wrap of the
Analyses entry). `build.py --check` was run first, since a landing-only
session otherwise never runs the guard that compares the landing copy of
`banner.css` against the canonical in the app tree — clean.

Verified on `https://symbulator.com/`: no *fourteen* anywhere in the page,
*Thirteen lessons* in the kicker, *thirteen lessons* in the
`og:description`, *Direct current* and *alternating current* still bold in
Analyses, and `<b>two-port</b>` in Equivalents. Line 295's "three-phase
and two-ports" left alone as agreed.

---

## #193 — landing page: spell out DC and AC, bold two-port — **done, deployed**

Roberto, 30 Aug 2026, two wording fixes in the definition list on the
landing page. **Ships with #192**, which is the other landing change
waiting: one `landing` deploy covers all three.

**1. Spell the analyses out, keeping the bold on the terms.** Line 184, in
the *Analyses* entry:

    <dd><b>DC</b> and <b>AC</b> as phasor analysis, <b>transient</b> in the time

becomes

    <dd><b>Direct current</b> and <b>alternating current</b> as phasor analysis,
        <b>transient</b> in the time

Capital **D** on *Direct*, because it opens the sentence; lower-case **a**
on *alternating*, as Roberto wrote it. `<b>transient</b>` and
`<b>complex frequency domain</b>` further down that entry are untouched.
The line will want re-wrapping afterwards — the replacement is a good deal
longer than what it replaces, and the file is hand-wrapped.

**2. Bold the two-port.** Line 197, in the *Equivalents* entry:

    two-port parameters in six varieties.

becomes

    <b>two-port</b> parameters in six varieties.

Note this is the *Equivalents* entry, **not** line 295, which says
"three-phase and two-ports" in the lessons kicker. That is a different
sentence about what the lessons cover, it is not bold, and Roberto did not
ask for it — leave it.

### Deploying

Same as #192: the landing page has no build step, `landing/` *is* the
site, and `py deploy_symbulator.py landing` uploads it. Do #192 and this
one together and the whole diff should be four lines in
`landing/index.html` — two for the lesson count, two for these. Check that
it is.

---

## #192 — the landing page says fourteen lessons — **done, deployed**

Roberto, 30 Aug 2026: on the landing page, *fourteen lessons* should be
**thirteen**.

Confirmed against the source before recording it. `book.yaml` lists **15
chapters**, and of those exactly **13 carry `kind: lesson`** — the other
two being the Introduction (`kind: front`) and the Credits (`kind: back`).
So thirteen is right, and the fourteen looks like a chapter count that
dropped only one of the two non-lessons.

**Two places to change, not one**, and the second is the one that gets
missed because it is invisible on the page:

    landing/index.html:290   <p class="way-kicker">Fourteen lessons, with worked problems</p>
    landing/index.html:13    <meta property="og:description" content="... or read fourteen lessons of worked problems.">

The meta description is what appears when the site is shared on social
media or in a search result, so leaving it behind would keep the wrong
number in circulation where nobody looks for it. Mind the capital **F** in
the first and the lower-case **f** in the second.

### Deploying it

The landing page **has no build step** — `landing/` *is* the site, and
`py deploy_symbulator.py landing` uploads it. That target has not been
touched in a while: this would be the first `landing` deploy since the
#140–#157 day, so expect the diff to be exactly these two lines and check
that it is.

Nothing else counts lessons: `grep -ri "fourteen\|thirteen"` over
`landing/` and `src/` finds only these two.

---

**Deployed 30 Aug 2026** to `learn.symbulator.com`, with all three PDFs
rebuilt — v9 **241 pages**, v7 205, v8 195 — and Roberto's own revision of
the Acknowledgements in the same upload. Guards: 73 blocks verified against
the originals and the same 11 not found, control chars clean, palette clean
at 25 tokens, `check_white_text` clean on all three, zero LaTeX errors.
Verified live: the blue note rule served, *approx (full precision)* in
Lesson 5, and the credits' new **AI collaborator** section and *Use AI
responsibly* callout.

**This was the last full build for now** — see the standing instruction at
the head of `README.md`: builds are `--web` only until Roberto says
otherwise.

---

## #188 — the note callout is blue — **done, deployed**

Roberto, 30 Aug 2026: the **note** kind reads too grey.

It was grey because it had no rule of its own. `tip`, `warning` and
`danger` each override the base `.callout`; `note` fell through to the
neutral default — `--ink-3` on `--paper-2` — and so was the only one of
the four without a hue.

Both outputs now use the palette's **`accent`** (#2f5fa8), the same token
the links and the section numbers use, so screen and print are the same
blue and dark mode picks up #5b96e0 on its own.

The web side needed one thing untangled first. `.callout` set
`--accent: var(--ink-3)` **on the element**, shadowing the page's blue
inside every callout — so a `note` rule could not have asked for
`var(--accent)` at all; that is a cycle. The callout-local variable is
renamed `--callout-accent`, which removes the shadow. Checked before
doing it: **no callout anywhere in the book contains a link**, so nothing
was relying on the shadow to tint one.

Verified: light `#2f5fa8` on `#e9eff8`, dark `#5b96e0` on `#24344a`, both
sitting correctly beside tip green and warning amber; the PDF's note box
blue to match, `check_palette` clean at 25 tokens, `check_white_text`
clean, zero LaTeX errors.

---

## #190 — the *approx* option names its precision — **done, deployed**

Roberto asked what an accurate description of the **approx** rounding
option would be, guessing "approx without rounding" or "approx with 12
digits". Measured, it is neither:

| exact | approx | approx to 4 |
|---|---|---|
| `15/2` | 7.5 | 7.500 |
| `3/500` | 0.006 | 0.006000 |
| `1/3` | 0.3333333333333333 | 0.3333 |

`approx` converts to a decimal and shows **the shortest form that is still
exactly the same number** at double precision — so `15/2` needs two digits
and `1/3` needs sixteen. There is no fixed count; the ceiling is the
machine's, about 15 to 17 significant digits. The real contrast with
*approx to n digits* is who decides the width: the number, or the setting.

Roberto's choice of label: **approx (full precision)**. Changed in the
menu, and in the one tutorial line that names the option (Lesson 5), the
way #179 established.

---

## #177 — Antony García in the credits — **done, deployed**

Roberto, 30 Aug 2026, alongside Antony's two app suggestions (#175, #176):
add him to the list of people who have made Symbulator better.

`src/99-credits.md`, appended to the end of the list, which is not
alphabetical: "… Carlos Perez Ortega (Chile), Qifan Wang and Antony
García (Panama)." A plain space in the name, not a non-breaking one, to
match every other entry in the list.

The rest of that chapter is still deliberately untouched by #173's cutting
pass — it is Roberto's own life, his thanks to his father, and other
people's words.

Built and deployed to `learn.symbulator.com` the same day, all three PDFs
rebuilt with it; verified live on
`https://learn.symbulator.com/9/credits`.

---

## #171 — a problem no longer reserves a page it cannot fill — **done, deployed**

Roberto, 30 Aug 2026: the PDFs have too much blank space in them.

Measured before touching anything, by rendering all 259 pages of v9 and
finding every run of white 12 mm or taller inside the text block, ignoring
the sixteen pages that legitimately end a chapter: **27 pages' worth of dead
space**, 11 at the feet of pages and 16 as holes in the middle, with 40% of
pages carrying more than 25 mm of it.

The cause of the first half was #152's own guard. `_problem_need()` demanded
room for a problem's title, its statement **and its first figure**, capped at
170 mm, and `\Needspace*` moved the whole box to the next page when the
current one had less. A problem whose circuit would not fit therefore threw
away everything it had been standing on.

Two changes, both in `build.py`:

- the demand is the rule, the title and the opening lines only, capped at
  `PROBLEM_NEED_MAX = 34.0` mm. The figure term is gone: circuits float now
  (#172), so there is nothing to reserve for.
- `\needspace`, not `\Needspace*`. The starred form fills out the page it
  breaks from, which does not remove blank space, it moves it from the foot
  into the middle of the page. That is what the 16 pages of mid-page holes
  were, and measuring only the feet had hidden them.

Alone this took v9 from 259 pages to 253. With #172 it reaches 241.

---

## #172 — the circuits choose their own page — **done, deployed**

Roberto, 30 Aug 2026, asked for figures placed "so as to make the best use of
the space", with the text moving above or below them. That is LaTeX's float
mechanism, and the frame around problems was what forbade it: **LaTeX refuses
`\begin{figure}` inside any box** ("Not in outer par mode"), and 280 of v9's
282 circuits sat inside the `problem` tcolorbox. A circuit that did not fit in
what was left of a page took the rest of the page with it, and nothing could
move up past it.

So the frame goes. `problem` in `tex/symbulator.cls` is now a rule and a bold
title, the way the practice sections already read, and `build.py` emits each
circuit as a real float. The frame was not itself the problem — frameless with
the circuits still nailed in place measures **worse** than before (263 pages) —
it was only in the way.

**Placement is `[!ht]`, never `[b]` or `[p]`.** A circuit may stay where it was
written or rise to the top of the page it lands on; it may not sink to the foot
of a page or take a page of its own, either of which would put it after the
words that introduce it. Verified by instrumenting the build so every problem
and every circuit carried a unique printed marker, then reading the built PDF:
of **284 circuits, none is printed before its own title** and only two land
more than a page after it.

`\FloatBarrier` at the head of each problem (the `placeins` package) was tried
and dropped. It changed neither of those numbers, and it flushed the page it
fired on — putting back exactly the mid-page holes #171 exists to remove, two
of them over 120 mm.

A figure inside a **callout** still cannot float, because a callout is still a
tcolorbox. `TexRenderer.boxdepth` counts how deep we are and falls back to the
old in-place `symfigure` there. One figure in the book is in that position.

**The text had to stop saying where the circuits are.** 70 phrases pointed at a
figure by its position — "the circuit below", "my solution below the
schematic", "comparing it to the book's answer, shown below". Every one is
reworded. References to a ```sym or ```out block, or to a callout, are left
alone: those still sit exactly where they are written, so "below" is still
true. Which was which was decided by walking forward from each "below" to the
first block it could be pointing at, not by eye.

Result, measured the same way as the baseline in #171:

| | pages | dead space | pages over 25 mm |
|---|---|---|---|
| before | 259 | 27.2 pages' worth | 40% |
| #171 alone | 253 | 20.5 | 30% |
| frameless, circuits fixed | 263 | 24.3 | 33% |
| **#171 + #172** | **241** | **6.1** | **4%** |

v7 and v8 shrank with it — they share `src/` and the class.

---

## #173 — fewer words for the same thing — **done, deployed**

Roberto, 30 Aug 2026: "Sometimes I use too many words to say things." His two
examples, both from his own revision of Lesson 1: "For each resistor included
in the description of the circuit" → "For each resistor", and "that is to say"
→ "defined as".

A cutting pass, not a rewrite. No sentence says anything it did not say
before, the first person stays, and so do the jokes — the Joker, the Swiss
knife, "born to be bad". **167 edits, 2,035 words** across every chapter that
has them: 96 over lessons 2 to 9, then 24 in the Introduction and 47 in
Lesson 1 when Roberto asked for those two as well. Lessons 10 to 13 were
written recently and are already tight, and **`99-credits.md` was left alone
on purpose** — it is Roberto's own life, his thanks to his father, and other
people's words.

The one repeated cut worth naming: the two sentences about `approx` and
**Rounding** appear **twenty** times across Lessons 1, 3 and 4. They now say
the same thing in a clause less.

Also fixed here: `src/02-lesson-symbolic.md` carried a literal `&#8239;`, the
narrow no-break space as an HTML entity. The web swallowed it; the PDF printed
the seven characters. It is a plain space now.

**`00-introduction.md` and `01-lesson-dc.md` were done in a second round**,
after Roberto asked for them, on top of his own uncommitted revision rather
than instead of it — his revision is committed here as he left it. His draft
carries trailing spaces on some lines, so the matcher tolerates them; a source
that has moved on still fails loudly rather than being half-edited.

Four things in that draft were repaired while passing through, and they are
not cuts, so they are listed here: "the first thing we all to solve it" →
"the first thing we do to solve it"; "will starts a new input file" →
"starts"; a comma splice at "the right default for a machine doing algebra,
it is exactly what you want"; and a missing full stop after "you cannot write
back to it". Also `Python Anywhere` → `PythonAnywhere`, `labeled` →
`labelled` to match the rest of the book, "in your device" → "on your
device", and "what input cards carry" → "what input files carry", which
looked like a slip for *files*. Say if any of those was deliberate.

**Guards, all clean after the pass**: `check_against_originals.py` reports the
same 73 blocks verified and the same 11 not found as before it, so no printed
answer moved; `check_control_chars.py` clean; `check_white_text.py` clean on
all three PDFs; `build.py --check` clean; zero LaTeX errors in all three logs.

**Deployed 30 Aug 2026** to `learn.symbulator.com`: 39 files, and the three
PDFs verified live by hash against the local build — v9 240 pages, v7 205,
v8 195. The pages carry the reworded prose (`circuit below` returns nothing
on the built site).

---

## #164 — Lesson 13 revised for the two-port parameter term — 29 Aug 2026

Roberto, 29 Aug 2026, on discovering that the v9 port had left two-port
parameters reachable only through expert mode: revise the two-port
documentation in Lesson 13 once #163 (the parameter term,
`z,1,2,[100,10,20,50]`) landed in solver 0.5.21 — "in addition to, and
independent from, the SPICE stuff".

What changed in `src/13-lesson-twoports.md` (v9 panels only, except
where noted):

- **"Giving it its four parameters"** teaches three possibilities in
  Roberto's order of preference: the description's fourth term
  (primary — the parameters travel with the circuit and reach *every*
  analysis, the equivalent tools included), the **Define** field
  (the closest cousin of v7/v8's store-the-values-first), and leaving
  them symbolic. A note box documents the naming rule (`z` owns
  `z11`…`z22`, `z1` owns `z111`…`z122` — no warning in the app, per
  Roberto: well-documented behaviour, not a surprise) and that plain
  variables are case-sensitive while name-derived references fold.
- **Example 19.2** carries `z,1,2,[40,20j,30j,50]` in the description
  instead of four expert equations.
- **Example 19.6** runs the Thévenin *directly* — the old v9 text
  taught a workaround ("the equivalent tools take no Expert Mode
  equations", solve symbolically, substitute in Evaluate) that #163
  made unnecessary; the formula view is kept as what you get when the
  term is left off. Verified: vth = −29.69 V, req = 51.46 Ω straight
  from `th()` with the term.
- **Both gain examples** carry their parameters in the description.
- The **element description** section states the two guards (no port
  node on ground, no shared port node — v7/8-era measures, confirmed
  live in 0.5.21 and stopping the solve with clear messages).
- One **shared-text correction**, originals-verified: the port
  currents are named by the two-port and the *node* (`i_z5`, `i_z9`
  for ports on nodes 5 and 9), not the "port number" the conversion
  had said — Roberto's 2023 pages say "current entering the
  transformer at nodes 1 and 2", so this restores the original.
- **Lesson 2** gains the case-sensitivity note where symbolic values
  are introduced (Roberto's ask the same day): names fold
  (`2*VR1` ≡ `2*v_r1`), free variables don't (`c` ≠ `C`) — every
  claim measured before writing. Both chapters' `updated:` moved to
  2026-08-29.

The companion `examples/Lesson_13.cir` (app tree) moved to the new
notation the same day, which exposed a real bug: the app's AC
imaginary-unit normalisation sympified the parameter term whole,
evaluating its internal `pr(...)` encoding as the parallel-combination
function and collapsing `[40,20j,30j,50]` into one number. Fixed in
`symbulator_ui.normalise_imaginary` (entry-by-entry normalisation);
caught by `tools/verify_lesson.py Lesson_13`, whose run now ends
0 problems — with 19.6 *newly* machine-checkable (its vth/req come
back as named answers now that the parameters ride the description;
the two gain entries stay mini-tool-only by design, their numbers
verified directly against `gain()`). Shipped at cache v86 on both
offline sites; the server needs Roberto's next pull.

## #151 — The tutorial PDFs are A4 — built 29 Aug 2026, not yet deployed

Roberto's call: the three tutorial PDFs move from the 170 mm × 240 mm trade
size to A4, joining the monograph and the Book. One edit, the `\geometry`
line in `tex/symbulator.cls`; the margin scheme is unchanged, so the text
block grew with the page to a 156 mm measure — within 2 mm of what the two
paper/ PDFs have had all along. Verified in the XeLaTeX logs
(597.5 × 845.0 pt = 210 × 297 mm), not by eye.

The A4 rebuild is also what exposed #153: the old fixed figure rule sized
every image at 72% of the line, so the wider line silently enlarged every
figure by a third, and Roberto's page-by-page review of the result produced
the visual pass below.

## #152 — Problem headers are never orphaned — built 29 Aug 2026

A problem box that started near the foot of a page left its header (and
often the one-line statement) stranded there, with the statement figure —
unbreakable — opening the next page. Pages 24, 26 and 130 of the first A4
build all showed it.

`build.py` now emits `\Needspace*{...}` before every `\begin{problem}`,
sized per problem: title + estimated statement lines + the height of the
first figure (known from #153's manifest), capped at 170 mm. If the page
has less room than the problem's opening needs, the whole box starts on the
next page. `tex/symbulator.cls` gained `\RequirePackage{needspace}`.
Print-only by nature; the web has no page breaks.

## #153 — Figures sized by the text inside them — built 29 Aug 2026

The rule until now was `width=0.72\linewidth` for every figure. But the
scans came from a dozen textbooks and were resampled to arbitrary pixel
sizes (most practice crops to a uniform 1100 px in 2023), so a fixed
fraction printed some labels at half the body size and others at triple —
Roberto's examples: B11 7.10 and RM3 9-12 too small, B11 8.10 and the
RM3 7-16 ladder too large, expression crops enormous. His rule: **a figure
is right when its label text matches the body text height.**

`tools/measure_figures.py` estimates the label text height of every scan
(threshold, merge characters into words by horizontal dilation, filter
word-shaped components, median height — with guards for the beige Bo2
scans, whose Otsu threshold must be capped, and for dashed boxes/mesh
arrows, whose 8–11 px dash swarm otherwise outvotes the characters) and
writes `tools/figure_sizes.json`. `build.py` renders each figure at
`px_width × 2.7 mm / text_px`, capped at the line (`\symfig` in the cls
caps at `\linewidth`, since problem boxes are ~9 mm narrower), and gives
the web the same width as a percentage of the column, so both outputs
agree. The manifest's `overrides` block (width in mm, preserved across
re-runs) covers the two strips the detector cannot read; a figure absent
from the manifest falls back to the old 72% and means a re-measure is due.
Calibrated against every page Roberto judged; verified page by page after
the rebuild. Median computed width 86 mm; 10 of 316 figures cap at full
line.

## #154 — Standalone expressions are display math — built 29 Aug 2026

Expressions that stood alone in a paragraph were set inline — fractions
squashed to the line height, ragged left, "lost in the text" (Roberto, on
the old page 35). Twelve paragraphs across lessons 2, 5, 12 and 13 are now
`$$` display blocks — centered, padded, full-size fractions — including
the four bare-ASCII answer lines in lesson 5 (`r2/(r1+r2)` and kin), now
typeset with the same values. Inline math that is part of a sentence stays
inline. Renders as `\[...\]` in the PDFs and MathJax display on the web;
no renderer change was needed, the `$$` block syntax existed all along.

## #155 — v9 shows no captures of Symbulator's own output — built 29 Aug 2026

Five figures in the v9 pages were pictures of Symbulator's answer: four
TI-89 pixel-font captures (TR5 4.1, Bo2 1.11, TR5 Ex 4.3, TR5 4.5 — the
lesson 3 symbolic finale) and one screenshot of the v9 app's own MathJax
(TR5 4-14). Each is now a `::: only 7,8` figure plus a `::: only 9` `$$`
block carrying **what the running v9 solver actually returns** — every one
of the five was solved with the local 0.5.19 package first and the raw
result typeset, not transcribed from the old image. All five came back
equivalent to the captures and to the textbook answers beside them (the
Ex 4.3 capture's apparent `g1` is really `gl`). The stale "shown left /
shown right" prose — describing the 2023 site's side-by-side layout that
stacked vertically here — was reworded in each spot. The AC and Bode
lessons already had this shape (`only 7` captures, LaTeX for the rest) and
needed nothing. Textbook-scan expressions stay as images under #153's
sizing.

## #156 — β, γ and μ no longer print as tofu — built 29 Aug 2026

IBM Plex has no Greek, so every code block naming a transistor gain printed
□ where β, γ, μ or µ should be — pages 75–77 of the first A4 build, and
the XeLaTeX logs' "Missing character" lines as the definitive list (which
also surfaced the superscript minus in the two-ports lesson). Fixed where
δ, ω and π were already fixed: four new entries in `build.py`'s GLYPHS map,
plus `⁻` → `\textsuperscript{-}`. The rebuilt logs report **zero** missing
characters across all three books. Web unaffected (its fonts have Greek).

## #157 — Answers read as prose, never as tables — built 29 Aug 2026

Three `only 9` answer tables — HK5's Drill 1-13 shorts (which also
rendered broken, values wrapping under their labels) and chapter 13's two
gain tables — are now the prose form the rest of the book uses, values in
`{{o:...}}` spans, byte-identical. The two legitimate reference tables
(problem credits, lesson 4's "type this to find that") stay tables, and
SPEC.md now states the rule. `check_against_originals.py` still reports
exactly the known 11-block residue, nothing added.

Also fixed in the same pass, found by the review itself: **Lesson 4's
chapter title ran off the page edge** — "Shorts, equivalent resistance and
Thévenin/Norton" was 162 pt overfull at its fixed 26 pt size (and had been
on the old page size too, unnoticed). Chapter titles now wrap
(`\raggedright` in the titleformat). The rebuilt books: v7 229, v8 218,
v9 259 pages, `build.py --check` clean, all verified but **not deployed**.

---

## #119 — The full v9 read-through, 27 Aug 2026 — closed; everything live

Roberto asked for a complete read of the version 9 documentation for
clarity, soundness and correspondence with the interface as deployed
(build `2026-08-27 05:36 UTC`). Every checkable claim was checked by
running, not by eye. Findings fell into: **A** wrong or
self-contradicting claims, **B** interface mismatches, **C** leftovers
of the Python-API era, **D** misplaced/duplicated content, **E**
workflow harmonisations now that Evaluate has Conditions, **F** ungated
calculator narration shown to v9, **G** typos and formatting.

**B, D, F and G are fixed, built and deployed** — 151 edits, commit
`694e3d3`, live on learn.symbulator.com with the three PDFs rebuilt.
Also settled by Roberto: the v8 RMS flag is `userms` (v7 keeps
`s\rms`), Impala mode is genuine and stays, and two questions were
closed against the originals: the v8 page names its sources `e` (the
real v7→v8 difference in Lesson 7's 9.35 is `r`→`r1`), and both pages
list `pmax` as stored by the calculator's th script.

**C and E are done too**, authorised the same day. C rewrote the
Python-API leftovers in the interface's own language (Lesson 7's AC
intro, Lesson 2's `equations=` mapping, Lesson 8's "use_rms argument"
heading and "Python function", Lesson 5's "result object", Lesson 3's
one-liner) and normalised Lesson 6's v9 panels to the calculator's own
notation — `u(t)`, `δ(t)`, `2e^(-4t)` — which measurement showed
version 9 reads identically. E moved the two pre-Conditions workarounds
(Bo2 4.15's `t = 2`, Example 19.6's six-unknown trick) onto Evaluate +
Conditions, put the calculator's SI shorthand into the expert and Solve
panels (it works — measured), aligned 9.89's two passes on
`im(zeq) = 0`, and restored the Greek glyphs (β, γ) the 2023 pages use
— which needed the app's description whitelist widened to admit them,
the same courtesy µ and δ already had (`repos/server` #121). The
touched lesson files re-verified: 0 problems.

**The A list is ruled on, fixed and live** (Roberto's rulings A1–A9,
applied the same day, commit `cddffea` and its predecessors): Lesson
12's TR note reads time-domain again and its curly-bracket denial
became the shorthand's documentation (measurement showed v9 has it);
Lesson 4 keeps only the real reservation (`s`, whose current would be
`is`; `e` is not reserved); Lesson 6's plot slip reads `il`; the
Introduction's Bode claim is gated `{{!v8|...}}` and "fifteen years"
became "a dozen"; Lesson 7's `e`-naming tip was rewritten from the
originals (the true v7→v8 difference is `r`→`r1`).

**A7 was dissolved rather than patched:** instead of excusing Lesson
11's five H(s)-only practice problems, the app grew a *Bode plot of a
transfer function H(s)* plot type (`repos/server` #123), and the
chapter now teaches it — a "When you have H(s) itself" subsection
(write jω as `s`; the axis is Hz, rad/sec ÷ 2π) plus a v9 note on each
of the six problems. `updated: 2026-08-27` on that chapter.

All of it deployed with the 27 Aug evening batch (build `2026-08-27
11:15 UTC`, PDFs 320/303/355 pages) and verified by fetching the live
pages. Still open here: Roberto's announced edits to
`src/99-credits.md`, which had not landed when the batch shipped —
when they do, `build.py` + `py deploy_symbulator.py learn`.

---

## #85 — Chapter 7's answers were dressed up as transcripts — settled

Seven answers in `src/07-lesson-ac.md` appeared as `out 7,8` transcript
blocks — quoted strings with `ᴇ0` exponents and `{…}` set braces. **Both 2023
pages carry prose for all of them and never a transcript:** "We get
414.5∠-71.6º mA, which is correct." The quotes, the exponents and the braces
were added by the conversion.

That mattered because the form is otherwise genuine — chapter 9's Example
12.12 carries `{"9.106ᴇ0∠168.48°","5.500ᴇ0∠172.47°"}` verbatim in the 2023
page, a real screen — so a reader had no way to tell a reconstruction from a
transcript, and six of these were reconstructions.

**Roberto's decision, 27 Aug 2026: go back to the version 7 wording.** The six
`out 7,8` blocks are gone, replaced by `::: only 7,8` prose in the pages' own
words. The closing sentence that reads the answer with its units is unchanged,
so nothing was lost.

The units question was already closed and needed nothing: six of the seven
carry V or mA in that closing sentence, and the seventh is a pair of node
voltages the pages give no units for either. Page 7 reads "6.914∠-80.70º mA"
for what is a node voltage; that slip stays in the archive only, per his
26 Aug decision, and was not reintroduced.

**Two flattened version differences turned up while doing it**, which is the
hazard the shared `out 7,8` blocks were always going to carry:

* Page 8 names the resistor `r1` where page 7 names it `r`, in Problem 9.35
  and in Practice Problem 10.1 — because version 8 reserves `r` as a resistor
  name, as lesson 1 says in its own words. The conversion gave both versions
  page 7's `r`, so version 8 was shown a description its own machine refuses,
  and asked for `s\aa(ir)` instead of `s\aa(ir1)`. Both restored.
* Problem 10.77 lost its `sym 8` fences entirely. Page 8 carries the problem
  with the same description and the same ask; a version 8 reader was shown the
  circuit in prose with nothing to type. Restored.

**The seventh answer** was not a reconstruction but a placeholder: an `out 7`
block whose content was the literal text `(the expression below)`, so version 7
read "type `vo/vs` returns **(the expression below)**". Roberto's call: version
7 keeps its TI-89 photograph, which is its machine; versions 8 and 9 get the
expression itself. Verified against the app first — `vo/vs` comes back as

    (1j*cb*omega*r2*r3 + r2 + r3)
    / (r3*(-ca*cb*omega**2*r1*r2 + 1j*ca*omega*r1 + 1j*cb*omega*r2 + 1))

which `simplify` confirms is the expression the chapter prints, and it took
10.7 s — the chapter's "about ten seconds" is right.

`check_against_originals.py` went from **24 unverifiable blocks to 11**, and
chapter 7 no longer appears among them.

## #89 — What the dangling-promise check still finds — down to 5, all judgement calls

`tools/check_dangling_promises.py` was tightened on 26 Aug 2026 (see #88) and
now reports 18 rather than about 74. Most of the residue is real. Worth
fixing, in rough order of how badly it reads:

* **`vo` is: (nothing).** `src/05-lesson-opamps.md`, Bo2's Example 3.3
  (Cascade) in version 9, and "Evaluating `vo` we get:" in 7 and 8. The
  answer for that problem is the one Word equation the restore could not
  place; a reader is shown the book's scan and never Symbulator's answer.
* **`vc|t=to` and `il|t=to` have no version 9 equivalent, and the obvious
  workaround does not work.** Two places in `src/06-lesson-transient.md` say
  "Here is how we find it:" and then show a `sym 7`/`sym 8` fence using the
  calculator's `|` operator, so a version 9 reader is shown the promise and
  nothing else. **Written, and live since 27 Aug 2026.** #95 and #96 in
  `Application/v9/repos/local/NEXT.md` were built on 26 Aug 2026: `t = to` now
  works in the Solve card, and **Evaluate** has a *Conditions* box that says
  `vc|t=to` directly. Neither is live yet, so writing it up now would
  document a version of the app no reader has. Write it when it ships.
* The rest are prose that hands off to a following sentence -- the credits
  list, `lesson-dc`'s "flows in the opposite direction:", `lesson-sources`'s
  "under Node voltages:". Judgement calls, not defects.

**Worked through on 27 Aug 2026: 18 → 15 → 5.** What was fixed, and what each
turned out to be:

* **The op-amp `vo`.** Not missing after all — the restore had placed it. It
  was *glued to the following sentence*, so it rendered as
  "((g1-g2) vs)/(g3-g4) which is correct, as can be seen…" — one paragraph,
  and therefore not marked as an answer. Now `{{o:…}}` on a line of its own.
  Verified against the app: `v_o = vs*(g1 - g2)/(g3 - g4)`.
* **`vc|t=to` and `il|t=to`.** Unblocked by #95 and #96 shipping, and now
  written. Both say to put the name in **Evaluate** with `t = to` in
  **Conditions**, which is exactly what the calculator's `|` did. Measured
  first: `V - V*exp(-to/(c*r))` and `V/r - V*exp(-r*to/l)/r`, matching the
  expressions the chapter prints.
* **Chapter 10's two syntax sections.** Both illustrated the element layout
  with a ```` ```field 9 ```` block, which renders for version 9 only — so
  readers of 7 and 8 were told the field layout in prose and shown no example
  at all. Now inline, the way *How to describe a resistor* has always shown
  `r1,a,b,300`. This was the whole of it: a scan found no other section with
  the same hole.
* **Lesson 2's `approx(-ie1)` and `e`.** Two lines of calculator input set as
  ordinary paragraphs rather than as fences. Now `sym 7`/`sym 8` fences.
* **Lesson 2's "solve them for e and r1:".** The colon promised something a
  version 9 reader only reaches after a paragraph of explanation. Split:
  `{{v7,8|:}}{{v9|.}}`.

The remaining **5 are the judgement calls** the note above already named — the
credits list, `lesson-dc`'s "flows in the opposite direction:", and
`lesson-sources`'s "under Node voltages:". Prose that hands off to the next
sentence. Left alone.

## #90 — Gain Example 2 never made it into chapter 13 — restored

Both 2023 pages carry a second gain example after Gain Example 1 -- a two-port
with z parameters 4, 1.5, 10 and 3, a source with 5 Ω in series and a 2 Ω
load, answering Gv 4, Gi -2, Gp 8, Zin 1 Ω. `src/13-lesson-twoports.md` has
only Gain Example 1. The description is
`"es,3,0,1:rs,3,1,5:rl,2,0,2:zp,1,2"` on page 7 and the same with `z` on
page 8.

Restoring it means writing a version 9 panel and checking the four gains
against the app, so it is a small piece of authoring rather than a copy.

**Written on 27 Aug 2026**, in the shape Gain Example 1 uses, with the version
7 and 8 halves following the 2023 pages (`zp,1,2` on page 7, `z,1,2` on page 8;
`izp1`/`izp2` for the currents) and a version 9 half using **Add equations**
and the *gain* mini-tool.

All four answers were computed before the panel was written, not copied:

    Av = 4      Ai = -2      Ap = 8      Zi = 1 Ω

which is what both 2023 pages print. There is no figure — the pages say so
too — so no placeholder was needed. `Lesson_13.cir` carries a matching entry.

## #91 — Example 12.12's third answer was dropped — restored

`src/09-lesson-threephase.md` says the generator current Iab "cannot"
be had from the two-source trick. The 2023 pages go further: Roberto tried
`s\aa(-(ie0a+ieb0)/3)`, reasoning that the current leaving two sources in the
simulation would in reality leave three, got `"5.959ᴇ0∠-177.18°"`, and notes
that it matches the book. A paragraph of his was lost, not just a value.

**Restored on 27 Aug 2026**, the paragraph as well as the value. The chapter
had come to say the two-source trick "cannot" give the generator current; the
2023 pages show Roberto trying `-(ie0a+ieb0)/3`, reasoning that current
leaving two sources in the simulation would leave three in reality, and
getting the book's answer.

Version 9 reproduces it exactly:

    -(ie0a+ieb0)/3  =  -5.95184 - 0.29332j
                    =  5.95906 ∠ -177.179°

against the 5.959∠-177.18° both pages print. His reasoning is back in his own
words, with a warning after it that this is a guess that was checked and not a
method — the argument holds in a balanced circuit and this one is not
balanced, which he says himself.

One thing was **not** carried over: the pages call this "the third answer"
having just called the same two answers "the second and third", which is a
slip. The restored text says "the remaining answer, the generator current",
which is unambiguous and does not put words in his mouth.

## #92 — A calculator fact stated for all three versions — settled by measurement

`src/09-lesson-threephase.md`, in the balanced wye-wye walkthrough: "Since the
calculator does not differentiate between lower and upper case variables,
nodes called a and A would be considered the same node." That is ungated, and
it is a fact about the calculator. Whether version 9 is case-sensitive should
be measured and the bullet split -- the node names `ag` and `ad` are worth
keeping either way, but the reason given has to be true for the version
reading it.

**Measured on 27 Aug 2026, and the fact is true of version 9 too**, so the
bullet did not need splitting after all — only its attribution was wrong.

    r1,a,A,5      ->  refused: both nodes of 'r1' can't be the same node
    e,A,0,10 ...  ->  answers reported as v_a

Version 9 folds case exactly as the calculator does. "Since the calculator
does not differentiate…" now reads "Since Symbulator does not differentiate…",
which is true for every version reading it, and the `ag`/`ad` names keep their
reason.

## #93 — `import_practice.py` still drops Word equations — fixed

The importer reads runs of text. An answer Roberto set as a Word **equation**
is not a run of text, so it was dropped -- silently, because the sentence
promising it came through fine. That is where the `{ , , }` in chapter 6 came
from, and 57 further answers that had no placeholder at all.

`tools/restore_practice_answers.py` put them all back on 26 Aug 2026 and can
be re-run safely (it skips anything already present), but `import_practice.py`
itself is unchanged: the next import of a practice file would lose them again.
The OMML-to-markup renderer it needs is already written, in
`restore_practice_answers.render()`.

**Fixed on 27 Aug 2026.** `runs_to_markup` walked `p.iter(w:r)`, and an OMML
equation is not a `w:r` — so it was stepped over silently, while the sentence
introducing the answer came through fine.

The walk is now `paragraph_items(p)`, which yields runs *and* `m:oMath`
subtrees in document order, skipping anything inside an equation so it is not
rendered twice. The renderer itself is imported from
`restore_practice_answers.render` rather than copied, so a fix to either
reaches both.

Measured across the six practice files:

    89 paragraphs carry an equation
    62 of them have no ordinary text at all -- the old importer
       emitted an empty line for each

and the first few now render as `((r1+r2) vs)/r1`, `-(rf/r1)vi`,
`((r1+rf)/r1)vi`, which is what they should always have been.

## #94 and #95 — moved to the app's list

Both are the app, not the documentation, and both were found from this side:

* **#94**, a number glued to an answer name silently unbinds it. What #84
  turned out to be: `.2v1` multiplies correctly but leaves `v1` a free
  symbol, and nothing says so.
* **#95**, there is no version 9 way to say `vc|t=to`. What blocks the second
  bullet of #89.

They live in `Application/v9/repos/local/NEXT.md` now, with the measurements.
**#96** is there too: Roberto's request, on 26 Aug 2026, for a *Conditions*
field on the **Evaluate** card. All three were built the same day and none is
deployed.

Worth carrying back here: the #95 write-up was **backwards** at first, and
this file said so confidently. It blamed the `t` a reader types; the fault
was the `t` in the answers, which lose their assumption crossing back from
the browser as strings. `README.md`'s note on that trap was wrong in one word
too, and is fixed.

---

## Found building the example input files, 26 Aug 2026

Thirteen lessons' worth of `.cir` entries were written, one per simulation
the tutorial runs, and every entry was run and read against the answer its
chapter prints. These are what that turned up. Nothing below has been
changed in the documentation.

The app-side findings from the same pass -- #105, #107, #110, #112 and
#114 -- are in `Application/v9/repos/local/NEXT.md`.

---

## #98 — Lesson 1 says version 9 refuses a bare `e`, and it does not — fixed

`src/01-lesson-dc.md:471`, in an `only 9` note:

> A bare `e` is one of the few names Symbulator 9 will not accept. […]
> Symbulator refuses the name rather than quietly reading it wrong, and
> suggests `e`.

Three things are wrong with it. **The app accepts `e`** -- `e,1,0,36`
solves. **The chapter's own panels use it**, including the very first
circuit a reader types. And **the suggestion is the name it just
refused**; something was lost there, presumably `e1`.

The "No reserved names" tip 200 lines earlier is correct and says the
opposite: two names are refused, `s` and `eturn`, and everything else
including `e` and `rc` is fine. That matches the app exactly.

**Fixed** (deleted): the note at 01-lesson-dc.md:471 is gone.

---

## #99 — Two answer names in Lesson 1 survived the `e1` → `e` rename — fixed

`src/01-lesson-dc.md:822` (B11's Example 6.13) and `:1005` (B11's Example
6.15). Both read `{{v9|`re1` is}}` where the version 9 circuit names its
source `e`, so the answer is `re`. The calculator half of the same
sentence says `re`, correctly.

**Fixed** (applied): `re1` reads `re` in both places.

Found by sweeping every panel in every chapter for names the version 9 text
quotes that the circuit beside it does not produce. Those two are the only
such cases in Lessons 1 and 2.

---

## #100 — Lesson 4 points at a `prl` expression that is never derived — fixed

`src/04-lesson-equivalents.md:452`. The version 9 half of the sentence
names `prl`, which does not exist in version 9. What was derived above is
`vth^2*R/(req+R)^2`, unnamed. The calculator half is right -- **prl** is a
real variable there.

**Fixed** (applied): the expression is named rather than pointed at as `prl`.

---

## #101 — Lesson 1's B11's Example 6.13 prints 0.11 A where the screen says 109 mA

`src/01-lesson-dc.md:822`. The current is exactly 24/220 = 0.10909…, so at
the lesson's own setting -- three significant digits, SI prefixes on -- the
screen reads **109 mA**. The page says **0.11 A**, the same number rounded
to two decimals.

The most visible instance of a difference that also affects a handful of
answers in Lessons 3 and 4: the calculator prints a fixed number of
decimals, version 9 counts significant digits. No setting reproduces the
page here -- n = 2 gives 110 mA, n = 3 gives 109 mA.

**Left alone.** The number is not wrong, and it is the calculator's own
display convention.

---

## #102 — Lesson 1's B11's Example 5.20 gives a voltage drop in watts — fixed

`src/01-lesson-dc.md:796`: "`vr2` is the voltage drop in the 7Ω resistor:
17.5 **W**". A voltage drop is in **V**, and the app shows 17.5 V. Shared
text, so wrong for all three versions.

**Fixed** (applied): it reads 17.5 V.

---

## #103 — Lesson 5 asks for `vo/is` where the source is `is1` — fixed

`src/05-lesson-opamps.md`, AS7's Practice Problems 5.4a and 5.4b. Both
circuits name the source's value `is1`, and both instructions say `vo/is`,
which fails outright -- `is` is a Python keyword:

    vo/is   ->  Could not read the value 'vo/is': invalid syntax.
    vo/is1  ->  -r                                  (the printed answer)

The same rename that was settled in Lesson 3 today, missed in two more
places. 5.4b carries #104 as well.

**Fixed** (applied): version 9 asks for `vo/is1`; the calculator halves keep their own `is`.

---

## #104 — `expand(...)` does not exist in version 9's Evaluate card

Four places in Lesson 5 tell a version 9 reader to evaluate `expand(vo)`:
AS7's Figure 5.21, TR5's Example 4-16, TR5's Exercise 4-14 and TR5's
Example 4-17. All four fail with "'Symbol' object is not callable" -- the
evaluator's namespace is a deliberately small list and `expand` is not in
it.

The chapter contradicts itself here: at AS2's Figure 5.24 (Subtractor) it
says plainly *"Version 9 has no `expand`"*.

**A decision rather than a typo.** Either add `expand` to the namespace --
it is a pure function on expressions like the ones already there, and the
calculator had it -- or drop it from the four instructions, since `vo` on
its own gives the same expression differently arranged.

---

## #106 — Lesson 5's two remaining `|` panels

The seven in Lesson 4 were converted on 26 Aug 2026. Two remain, both in
Lesson 5: **TR5's Exercise 4-11**, `vo|vs=2.` and its two siblings, and
**TR5's Figure 4-32**, `prL|L=1000`. Neither can be followed as written.

The first is now straightforward -- `vo` in **Evaluate** with `vs = 2` in
its **Conditions** box, which is what that box is for. The second takes the
algebraic form Lesson 4 uses throughout: `vth^2*1000/(req+1000)^2`.

---

## #108 — Lesson 6's Drill Exercise 5.3 names a resistor that is not there — fixed

`src/06-lesson-transient.md:657` asks for `ir1`; that circuit's resistors
are `r4` and `r12`. The 2 A it prints is `ir4`, which is what the same
problem's transient half says four paragraphs later.

**Fixed** (applied, and completed on 27 Aug): `ir1` reads `ir4`. Only version 9 had been corrected until 27 Aug -- the two calculator fences still carried the typo, which is in the 2023 original too: lesson6.docx names `ir1` in the DC line and `ir4` in the TR line for the same circuit, and that circuit has no `r1`.

---

## #109 — Lesson 6 shows the same paragraph three times, twice over — fixed

`src/06-lesson-transient.md:1528, 1532, 1536` and again at `1574, 1578,
1582`. Six `only 9` blocks in two runs of three, each holding exactly the
same sentence about limiting the results. A version 9 reader sees it three
times running, then three times again further down.

The calculator versions are fine: each block replaces one of three
`s\only("vc")` calls, which do belong there individually.

**Fixed** (applied): one of each run kept.

---

## #111 — Lesson 6's Drill Exercise 6.1 prints answers that cannot be right — fixed

`src/06-lesson-transient.md:1395`, an `only 9` sentence quoting
`vc = 2 - 3*exp(-2*t) + exp(-6*t)` and `il = 2*exp(-2*t) - 2*exp(-6*t)`.

Neither is what the app produces, and the first contradicts the problem's
own set-up:

|  | at t = 0 | as t → ∞ |
|---|---|---|
| the page's `vc` | 0 | **2** |
| the app's `vc` | **2** | 0 |

The initial condition two panels earlier is vc = 2, and the transient
interval has no source in it, so the voltage must start at 2 and decay to
nothing. `il` is out by a sign.

**The calculator lines directly above are right** -- they print
`3e^-2t - e^-6t` and `2e^-6t - 2e^-2t`, which is exactly what the app
gives. Only the version 9 sentence is wrong.

**Fixed** (applied): the same two expressions the calculator lines quote.

---

## #113 — Lesson 9 says version 9 cannot read the angle sign, then uses it — fixed

`src/09-lesson-threephase.md:458`:

> Version 9 does not read the angle sign, so each source is written in
> exponential form: 100 V at 10° is `(100∠10°)`.

Version 9 does read it -- Lesson 7 says so correctly, and every circuit
panel in Lesson 9 uses it and solves. The example contradicts the claim in
the same breath, and "exponential form" is the wrong name for polar form
anyway.

**Fixed** (applied 27 Aug): deleted. Versions 7 and 8 carry no such note and neither 2023 page mentions an angle sign; version 9 reads it fine (`v_1` comes back `100.0∠10.00°`).

---

## Settled on 26 Aug 2026

**#80, array answers become named lines in version 9.** The four untagged
```out``` blocks that rendered in all three versions are now `out 7,8` with a
version 9 reading beside each, one named line per answer; the two passages
that abbreviated ("and the other two lines follow") now name all three. The
verb changed with them: version 9 "looks in the results and sees", it does not
"ask for".

Worth knowing for the next one of these: with **Show AC answers as polar
phasors** ticked, version 9's results really do read `6.809∠-21.8°` on the
*current through* line, so "look in the results and see that" is literally
true for a polar answer and not just a form of words.

**#81, simplest names where the calculator's reason is gone.** All of it.

| Name | Version 9 now | Verified |
|---|---|---|
| `ecc` → `ec`, `rcc` → `rc` (ch 9, three circuits) | done | answers unchanged |
| `rrc` → `rc` (ch 3, two circuits) | done | solves |
| `zp` → `z`, `yp` → `y` (ch 13) | done | `iz1` = 2∠0°, `iz2` = 1∠-90° |
| `e1` → `e` (160 panels) | done | all 311 panels still read |

`e1` → `e` was Roberto's call on 26 Aug 2026. It reaches only panels where
`e1` is the **only** source named e-something: a circuit with `e1` and `e2` is
numbering two sources, which is meaningful, and 32 panels keep it on that
basis. Versions 7 and 8 keep `e1` everywhere. `tools/rename_e1_to_e.py` did
it and explains the rule.

Knock-ons that had to be split by hand, because a version span does not
survive a line break: chapter 1's "The first one is `e1,1,0,36`" bullet,
`pe1` in one wrapped `{{v9|...}}`, chapter 8's `-se1`, and `ve1`/`-ie1` in
another wrapped span.

And a tip in chapter 7 that said "Version 9 will not let you call an element
`e`" is now the opposite, because it is: the banned list is derived and comes
to two names, `s` and `eturn`, neither of which is `e`.

Chapter 1's `::: only 9` tip that read **"Pending."** -- live on the site --
now says what is true about reserved names in version 9.

**#82, eleven examples lost their calculator code.** Fourteen, in the end.
Restored verbatim from the 2023 pages, each version from its own page:
chapter 9's Examples 12.11, 12.4, 12.5, 12.12 and Practice Problems 12.9 and
12.10; chapter 13's Examples 19.3, 19.4, 19.5, 19.7, 19.8 and Practice
Problem 19.7; the requests that were lost in the balanced wye-wye walkthrough
and in AS7's 12.2 & 12.6; and Example 12.3, which had lost only its version 8
half.

That last one is the pattern worth remembering: an audit of *which versions
have code for each problem* found three gaps the eyeball list had missed
(12.12, 12.3, and the two lost requests), because a problem with a `sym 7`
fence and no `sym 8` looks complete until you read it as a version 8 reader.

**Chapter 13's two-port names were flattened, and are not any more.** Page 7
uses `zp`, `zp11`, `izp1` and `r`; page 8 uses `z`, `z11`, `iz1` and `r1`,
because the Nspire does not reserve `z11`..`z22` and the Titanium does. The
conversion gave page 7's spelling to both. Split back, including the
paragraph that explains the naming prompt, which differs between the two
machines. One loose end: page 8's own Example 19.4 says "we specify DC and y,
and agree to the default p character" while its code says `{y11,...}` -- a
leftover from page 7 in Roberto's own text. Followed the code.

**#83, twenty-seven empty answer sets in chapter 6.** All 27 refilled, and 57
more answers that had been lost the same way with no placeholder to mark
them. The values were never in the text: they are Word **equations** in the
practice `.docx`, which the importer never read. See #93.

`tools/restore_practice_answers.py` does it, anchored on the sentence before
or after each answer, and reports rather than guesses when neither anchor is
unambiguous. Twelve were placed by hand, and three "expert mode" problems in
chapter 6 needed restructuring, because the answers belong *after* the
request fence and the anchor put them before it.

Two things learned the hard way: a code fence sets its contents literally, so
`{{sup:...}}` cannot live in an `out` block -- an answer with an exponent has
to be a paragraph. And the answers to chapter 6's practice problems are
ungated on purpose: they are the same expression in all three versions.

**#84, a version 9 panel that cannot produce its own answers.** HK5's Drill
Problem 1-13 said `jd,0,2,.2v1`; version 9 read `v1` as a free symbol and
answered symbolically. Written `jd,0,2,0.2*v1` it gives -2, 3, -8 and -0.5,
which is what the page prints. Fixed, and no underscore needed.

The sweep for others found two more of the same family and one false alarm:

* `irL|Load=...` in **two** version 9 **Evaluate** panels in chapter 4. `|` is
  the calculator's "given" operator and version 9 refuses it outright. Both
  now use the equivalent this chapter had already settled on a few pages
  earlier -- `vth*5/(req+5)` and `ino*req/(req+1e4)` -- and the four values
  match the printed answers.
* `e1,1,0,3t` in chapter 6 is **fine**: version 9 reads `3t` as 3·t and gives
  the same answer as `3*t`.

Which is worth being exact about, because the obvious reading of `.2v1` --
"version 9 does not do implied multiplication" -- is wrong, and the real
cause is #94.

**#86, Example 12.10's answer array is truncated.** The block ended at
`-18282.𝐢`. It now carries all nine values, and the version 9 side names the
three source powers as well as the three load powers. Verified against the
app: `sea` = -6814.15, `seb` = 790.615 - 2950.61𝐢, `sec` = -456.462 + 5110.62𝐢.

**#87, a search bar for the documentation.** Built. Top of the sidebar, so
`design/banner.css` -- shared with the landing page and the app -- is
untouched. `build.py` writes `content/v<N>/search.json` per version, one entry
per section and per worked problem; `web/index.php` fetches it on the reader's
first keystroke; `build.py --check` fails if the path or the element ids drift,
if the stylesheet loses its rules, or if a built index is missing a chapter its
own table of contents lists. `README.md` has the full account, including the
one that will bite: **a deploy that leaves `search.json` behind gives every
reader "Search is unavailable on this server."**

Driven in a real browser against the real index before being called done, since
there is no PHP on this machine to serve `index.php`: "thevenin" finds three,
"polar phasors" finds five, the links come out as `/9/lesson-ac#ac-analysis`,
and version 8's index has no Bode chapter in it while 7's and 9's do.

**#88, two new checks to finish and wire in.** `check_dangling_promises.py`
went from about 74 reports to 18 by learning four things: display maths is an
answer (`<span class="math">`); a callout is an answer; a paragraph with no
word longer than three letters is an expression rather than a sentence, which
is what tells `2-2e^-3t` from prose without marking up the source; and one
sentence may stand between a promise and its answer, though not a figure,
because "the answer is: ... as you can see below:" is exactly how a missing
answer reads. It is **not** wired into `build.py --check` yet: the residue at
#89 is real, and gating the build on it would fail the build for reasons that
are not the build's fault.

`check_against_originals.py` needs nothing: it went from 59 of 83 verified to
71 of 93 as the restored blocks arrived, and the 22 it cannot find are the
understood set -- chapter 7's prose (#85), the two composed prose summaries,
the two package-API values, and the answers deliberately corrected since 2023.

Both now read `originals/`, inside this tree, rather than the OneDrive master.

**RM3's Practice Problem 9.5's dropped zero.** The page printed `.00296` for
the current at a 100 kΩ load. So does the 2023 Word file. But it is larger
than the `.000457` above it, which cannot happen as the load grows, and
42/142000 = .000296 -- which the app confirms. Roberto's call on 26 Aug 2026:
corrected, in all three versions, since it is the problem that is wrong and
not the version.

**#78, Lesson 8's answers.** Talked through on 26 Aug 2026 and closed by
Roberto. It produced the package-API sweep -- `eq.z`, `eq.pmax`, `res[...]`
named a local variable inside `symbulator_ui.py` that no reader can type --
the underscore rule, and naming the `th` tool where the 2023 page says `er`.

**#79, the power factor in AS7's Practice Problem 11.10.** The page recorded
`0.93595 leading`; the load is 11.88 + 4.47j, inductive, so it is **lagging**.
Fixed in the `out 7,8` block, which covers versions 7 and 8; version 9 already
said lagging. The warning written to explain the gap is gone.

No bug in `s\pf` after all. The tool flips the sign for a source, which is why
the pf-tool example reads `0.97342 leading` correctly for a capacitive load --
the 2023 pages simply carry a typed word. Checked the other two lead/lag
claims in the chapter: Problem 11.75 is `leading` and is **right**, its complex
power being 1835.9 - 114.7j, negative reactive and so capacitive.

**AS7's Example 12.11.** The phase current was printed as `1.36∠-6.2°`; the
correct value is `-66.2°`, confirmed twice over -- the app returns
`1.35690∠-66.2049°` for `i_rac`, which is the expression the original asks
for, and **page 8 already prints -66.2**. Roberto caught the dropped six in
2023; the conversion merged pages 7 and 8 into one `out 7,8` block using page
7's value and reinstated the typo. Fixed, and the warning invented to explain
it away is gone.

**AS7's Example 12.9.** Version 9 said `93.44`; exact value 93.43494882, so
`93.43` -- what versions 7 and 8 already said. Version 9 corrected.

**The corrupt exponent.** Six lines in chapter 9 read `ᴐ00` where the
originals print `ᴇ0`. Both the letter and the digit count were wrong; fixed.

**AS7's Example 12.10.** No disagreement -- 16122 and 16120 are one number at
two precisions. At four digits with SI prefixes: 16.12k, 6.48k, -18.28k.

**RM3's Example 9-8, HK5's Drill 1-13, AS7's Example 19.8.** All three were
false alarms from the parity tool reading en-dash minus signs and leading-dot
decimals as different numbers. Tool fixed; the answers always agreed.

**AS7's Example 19.8 units.** The app prints none for transmission parameters
on purpose, so they belong in the prose: a11 dimensionless, a12 in **Ω**,
a21 in **S**, a22 dimensionless.
