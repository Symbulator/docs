# Open items on the documentation

Numbered on the running sequence shared with
`Symbulator/repos/local/NEXT.md`, which stood at #77 when this file started.
Nothing here is numbered twice and the sequence never restarts.

Opened 26 Aug 2026, from the integrity pass over the version 9 rewrite.

---

## #85 — Chapter 7's answers were dressed up as transcripts — no change needed

Seven answers in `src/07-lesson-ac.md` appear in the 2023 pages as prose --
"We get 4.789 angle -16.7, which is correct" -- and the conversion reformatted
them into `out 7,8` blocks with quotes and `ᴇ0` exponents that were never
there. Roberto asked to see all seven before deciding; they are listed in the
session notes and are reproduced here so the decision has the evidence beside
it. **Values are identical in every case.** What differs is the shape, and
the units the prose carried and the transcript dropped.

| Where | 2023 page 7 says | `out 7,8` now says |
|---|---|---|
| `aa(ir)` | We ask for s\aa(ir) and get 4.789∠-16.7º, which is correct. | `"4.789ᴇ0∠-16.7°"` |
| `aa(12/zeq)` | We get 414.5∠-71.6º **mA**, which is correct. | `"414.5ᴇ-3∠-71.6°"` |
| `aa(icx)` | We get 7.59∠108.4º, which is correct. | `"7.59ᴇ0∠108.4°"` |
| `{aa(v1),aa(v2)}` | We get 11.33∠60.02º and 33.02∠57.13º, which are correct. | `{"11.33ᴇ0∠60.02°","33.02ᴇ0∠57.13°"}` |
| `{aa(vro),aa(ico)}` | We get 1.55∠-95.18º **V** and 3.26∠-3.74º **mA**, which are correct. | `{"1.55ᴇ0∠-95.18°","3.26ᴇ-3∠-3.74°"}` |
| `{aa(v1),aa(v2)}` | We get 2.708∠-56.73º **V** and 6.914∠-80.70º **mA**, which are correct. | `{"2.708ᴇ0∠-56.73°","6.914ᴇ0∠-80.70°"}` |
| one more, version 7 only | prose | (the expression below) |

Two things fall out of the table whichever way it goes:

* **The transcripts dropped the units.** Four of the seven carry V or mA in
  the 2023 prose and nothing in the block, and the version 9 lines beside
  them carry nothing either.
* **The `ᴇ-3` is the units in disguise.** `414.5ᴇ-3` and `3.26ᴇ-3` are the
  prose's `mA` rewritten as an exponent, which is not what the calculator
  printed for these.

The unit question in the last row is **settled**: the 2023 page reads
"2.708 V and 6.914 mA" for `sa(v1)` and `sa(v2)`, both of which are node
voltages. Roberto confirmed on 26 Aug 2026 that the A should be a V. The
documentation already said V for both, so nothing needed changing -- the slip
lives only in the 2023 archive. The other two `mA` in the chapter are real
currents and stay.

**Settled on 27 Aug 2026, by reading the chapter rather than the note above.**
The premise had gone stale. Six of the seven already carry their units, in the
sentence that follows the block — "That is 414.5 mA at an angle of −71.6°,
which is correct." The seventh is a pair of node voltages, and the 2023 prose
gives no units for those either, so the chapter matches the page.

What remains true is narrower, and is a question rather than a defect: those
`out 7,8` blocks are **reconstructions**, not quotes. The 2023 pages carry
prose for these seven, so nobody transcribed a screen. The form is right — the
same `ᴇ0∠` shape appears verbatim in the 2023 page for chapter 9's Example
12.12, so that is genuinely what the calculator printed — but a reader cannot
tell a reconstructed transcript from a real one, and here they are reading the
former.

Nothing was changed. If it should be, the change is presentational: drop the
seven `out 7,8` blocks and let the prose carry the answers, the way the pages
did.

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
  nothing else. **Unblocked, and waiting on a deploy.** #95 and #96 in
  `Symbulator/repos/local/NEXT.md` were built on 26 Aug 2026: `t = to` now
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

They live in `Symbulator/repos/local/NEXT.md` now, with the measurements.
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
#114 -- are in `Symbulator/repos/local/NEXT.md`.

---

## #98 — Lesson 1 says version 9 refuses a bare `e`, and it does not

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

**Suggested fix:** delete the note at :471.

---

## #99 — Two answer names in Lesson 1 survived the `e1` → `e` rename

`src/01-lesson-dc.md:822` (B11's Example 6.13) and `:1005` (B11's Example
6.15). Both read `{{v9|`re1` is}}` where the version 9 circuit names its
source `e`, so the answer is `re`. The calculator half of the same
sentence says `re`, correctly.

**Suggested fix:** `re1` → `re` in both.

Found by sweeping every panel in every chapter for names the version 9 text
quotes that the circuit beside it does not produce. Those two are the only
such cases in Lessons 1 and 2.

---

## #100 — Lesson 4 points at a `prl` expression that is never derived

`src/04-lesson-equivalents.md:452`. The version 9 half of the sentence
names `prl`, which does not exist in version 9. What was derived above is
`vth^2*R/(req+R)^2`, unnamed. The calculator half is right -- **prl** is a
real variable there.

**Suggested fix:** name the expression rather than `prl`.

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

## #102 — Lesson 1's B11's Example 5.20 gives a voltage drop in watts

`src/01-lesson-dc.md:796`: "`vr2` is the voltage drop in the 7Ω resistor:
17.5 **W**". A voltage drop is in **V**, and the app shows 17.5 V. Shared
text, so wrong for all three versions.

**Suggested fix:** W → V.

---

## #103 — Lesson 5 asks for `vo/is` where the source is `is1`

`src/05-lesson-opamps.md`, AS7's Practice Problems 5.4a and 5.4b. Both
circuits name the source's value `is1`, and both instructions say `vo/is`,
which fails outright -- `is` is a Python keyword:

    vo/is   ->  Could not read the value 'vo/is': invalid syntax.
    vo/is1  ->  -r                                  (the printed answer)

The same rename that was settled in Lesson 3 today, missed in two more
places. 5.4b carries #104 as well.

**Suggested fix:** `is` → `is1` in both.

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

## #108 — Lesson 6's Drill Exercise 5.3 names a resistor that is not there

`src/06-lesson-transient.md:657` asks for `ir1`; that circuit's resistors
are `r4` and `r12`. The 2 A it prints is `ir4`, which is what the same
problem's transient half says four paragraphs later.

**Suggested fix:** `ir1` → `ir4`.

---

## #109 — Lesson 6 shows the same paragraph three times, twice over

`src/06-lesson-transient.md:1528, 1532, 1536` and again at `1574, 1578,
1582`. Six `only 9` blocks in two runs of three, each holding exactly the
same sentence about limiting the results. A version 9 reader sees it three
times running, then three times again further down.

The calculator versions are fine: each block replaces one of three
`s\only("vc")` calls, which do belong there individually.

**Suggested fix:** keep one of each run.

---

## #111 — Lesson 6's Drill Exercise 6.1 prints answers that cannot be right

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

**Suggested fix:** quote the same two expressions the calculator lines do.

---

## #113 — Lesson 9 says version 9 cannot read the angle sign, then uses it

`src/09-lesson-threephase.md:458`:

> Version 9 does not read the angle sign, so each source is written in
> exponential form: 100 V at 10° is `(100∠10°)`.

Version 9 does read it -- Lesson 7 says so correctly, and every circuit
panel in Lesson 9 uses it and solves. The example contradicts the claim in
the same breath, and "exponential form" is the wrong name for polar form
anyway.

**Suggested fix:** delete it, or use the Lesson 7 wording.

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
