# Open items on the documentation

Numbered on the running sequence shared with
`Symbulator/repos/local/NEXT.md`, which stood at #77 when this file started.
Nothing here is numbered twice and the sequence never restarts.

Opened 26 Aug 2026, from the integrity pass over the version 9 rewrite.

---

## #85 — Chapter 7's answers were dressed up as transcripts

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

## #89 — What the dangling-promise check still finds

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

## #90 — Gain Example 2 never made it into chapter 13

Both 2023 pages carry a second gain example after Gain Example 1 -- a two-port
with z parameters 4, 1.5, 10 and 3, a source with 5 Ω in series and a 2 Ω
load, answering Gv 4, Gi -2, Gp 8, Zin 1 Ω. `src/13-lesson-twoports.md` has
only Gain Example 1. The description is
`"es,3,0,1:rs,3,1,5:rl,2,0,2:zp,1,2"` on page 7 and the same with `z` on
page 8.

Restoring it means writing a version 9 panel and checking the four gains
against the app, so it is a small piece of authoring rather than a copy.

## #91 — Example 12.12's third answer was dropped

`src/09-lesson-threephase.md` says the generator current Iab "cannot"
be had from the two-source trick. The 2023 pages go further: Roberto tried
`s\aa(-(ie0a+ieb0)/3)`, reasoning that the current leaving two sources in the
simulation would in reality leave three, got `"5.959ᴇ0∠-177.18°"`, and notes
that it matches the book. A paragraph of his was lost, not just a value.

## #92 — A calculator fact stated for all three versions

`src/09-lesson-threephase.md`, in the balanced wye-wye walkthrough: "Since the
calculator does not differentiate between lower and upper case variables,
nodes called a and A would be considered the same node." That is ungated, and
it is a fact about the calculator. Whether version 9 is case-sensitive should
be measured and the bullet split -- the node names `ag` and `ad` are worth
keeping either way, but the reason given has to be true for the version
reading it.

## #93 — `import_practice.py` still drops Word equations

The importer reads runs of text. An answer Roberto set as a Word **equation**
is not a run of text, so it was dropped -- silently, because the sentence
promising it came through fine. That is where the `{ , , }` in chapter 6 came
from, and 57 further answers that had no placeholder at all.

`tools/restore_practice_answers.py` put them all back on 26 Aug 2026 and can
be re-run safely (it skips anything already present), but `import_practice.py`
itself is unchanged: the next import of a practice file would lose them again.
The OMML-to-markup renderer it needs is already written, in
`restore_practice_answers.render()`.

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
