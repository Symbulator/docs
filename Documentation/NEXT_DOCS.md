# Open items on the documentation

Numbered on the running sequence shared with
`Symbulator/repos/local/NEXT.md`, which stood at #77 when this file started.
Nothing here is numbered twice and the sequence never restarts.

Opened 26 Aug 2026, from the integrity pass over the version 9 rewrite.

---

## #80 — Array answers become named lines in version 9

Roberto's second piece of feedback. Anywhere the older versions ask for a
bracketed array and print bare values, version 9 must instead *read the
answers off the results*, one per line, `name = value`, with the name spelled
as version 9 spells it. The verb changes too: not "we ask for", but "we look
in the results and see that".

Version 9 only; 7 and 8 keep their arrays. Values stay as documented -- see
#85 before changing any of them.

Known instances include four untagged ```out``` blocks that render in all
three versions, and passages that abbreviate ("and the other two lines
follow") instead of naming each answer.

## #81 — Simplest names, where the calculator's reason is gone

Roberto's rule: a name that exists only to dodge a calculator restriction
should be simplified in version 9. Meaningful names stay -- `ra0` is the
resistor from a to 0, and `raa`/`rbb`/`rcc` in Example 12.11 are the lines
a-A, b-B, c-C, not dodges.

**The restrictions are gone as of 26 Aug 2026** (server `e6c15b2`, local
`385db30`, deployed to install.symbulator.com and the ZIP). The banned-name
table was 129 entries guarding a namespace the parser does not have; it is
now derived and comes to two, `s` and `eturn`. So all of these are legal:

| Name | Was dodging | Version 9 |
|---|---|---|
| `ecc` (ch 9, three circuits) | `ec` | **`ec`** -- verified |
| `rcc` (ch 9, three circuits) | `rc` | **`rc`** -- verified |
| `rrc` (ch 3, two circuits) | `rc` | **`rc`** -- verified |
| `zp`, `yp` (ch 13) | the Titanium's table variables | `z`, `y` -- untested |
| `e1` (113 circuits, all chapters) | `e` | **`e`** -- decision needed |

Version 7 and 8 keep their dodges: those calculators have the real
restriction, and Roberto's instruction is to preserve per-version
differences, since the two machines run different operating systems.

Watch for knock-on edits when renaming:

* Derived answer names in version 9 prose -- `ircc` becomes `irc`, `srcc`
  becomes `src`.
* `src/09-lesson-threephase.md` line 293 currently reads
  `` `sea+seb+secc+sra+srb+srcc` `` **ungated**. It was a version span whose
  halves became identical after the underscore change; a version 9 rename
  makes them differ again, so it has to be split back into
  `{{v7,8|...srcc}}{{v9|...src}}`.
* The tip at line 298, "Why `ecc` and `rcc` rather than `ec` and `rc`",
  should now say what is true: on the calculator those names collided with
  reserved ones; version 9 has no such restriction.
* `e` -> `e1` is a separate decision. It touches 113 circuits and every
  answer derived from them (`pe1` -> `pe`, `ie1` -> `ie`), so it is worth
  agreeing before starting.

## #82 — Eleven examples lost their calculator code

A `field 9` panel replaced the `sym 7`/`sym 8` pair instead of joining it, so
a version 7 reader meets "...and get:" followed by a result with no circuit
and no code:

* ch 9 — Examples 12.11, 12.4, 12.5; Practice Problems 12.9, 12.10
* ch 13 — Examples 19.3, 19.4, 19.5, 19.7, 19.8; Practice Problem 19.7

The 2023 pages have the original code for all of them.

## #83 — Twenty-seven empty answer sets in chapter 6

`src/06-lesson-transient.md` literally contains `{ , , }` at lines 422, 481,
540, 577, 680, 769, 825, 881, 940, 1026, 1099, 1134, 1169, 1205, 1242, 1278,
1666, 1697, 1728, 1761, 1791, 1824, 1854, 1907, 2181, 2508, 2606. Not version
gating -- **all three versions show it**, and it is already live.

The values were lost on import. The 2023 pages are the source to refill them
from.

## #84 — A version 9 panel that cannot produce its own answers

HK5's Drill Problem 1-13, `src/04-lesson-equivalents.md`. The panel says
`jd,0,2,.2v1` -- calculator shorthand. Version 9 reads `v1` as an unknown and
returns symbolic answers. Written `jd,0,2,0.2*v_1` it gives -2, 3, -8, -0.5,
matching the printed answers exactly.

Every `field 9` panel wants checking for the same thing.

## #85 — Chapter 7's answers were dressed up as transcripts

Seven answers in `src/07-lesson-ac.md` appear in the 2023 pages as prose --
"We get 4.789 angle -16.7, which is correct" -- and the conversion reformatted
them into `out 7,8` blocks with quotes and `e0` exponents that were never
there. What remains is whether those blocks should go back to reading as
prose, since they are not transcripts of anything the calculator printed.

The unit question is **settled**: the 2023 page reads "2.708 V and 6.914 mA"
for `sa(v1)` and `sa(v2)`, both of which are node voltages. Roberto
confirmed on 26 Aug 2026 that the A should be a V. The documentation already
said V for both, so nothing needed changing -- the slip lives only in the
2023 archive. The other two `mA` in the chapter are real currents and stay.

## #86 — Example 12.10's answer array is truncated

`src/09-lesson-threephase.md`. The block ends at `-18282.𝐢`; the original
continues `,-6814.,790.6-2951.𝐢,-4...`.

## #87 — A search bar for the documentation

Approved 26 Aug 2026. Searches **only the version being read**. Placement left
to judgement: top of the sidebar, so `design/banner.css` -- shared with the
landing page and the app -- is not touched for a feature only this site has.

Build-time JSON index per version, emitted by `build.py`, loaded on first
keystroke, and guarded by `build.py --check` so it cannot go stale.

## #88 — Two new checks to finish and wire in

`tools/check_dangling_promises.py` finds sentences ending in a colon that a
reader of that version sees answered by nothing -- how the missing panel in
9.2 was found. It still reports about thirty false positives where the answer
is set as display maths; tighten before it gates a build.

`tools/check_against_originals.py` verifies printed answers against the 2023
pages: 59 of 83 confirmed verbatim, and the residual is understood (#85, #86,
the two package-API values, two composed prose summaries). Code blocks were
tried and abandoned -- the originals interleave code with prose and the
conversion regrouped it, so the comparison reported hundreds of differences
that were reformatting, not drift.

Both need `docs-page7.html` and `docs-page8.html`, which live outside this
tree in the 2023 Website folder.

---

## Settled on 26 Aug 2026

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
