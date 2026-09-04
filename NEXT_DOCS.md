# Open items on the documentation

Numbered on the running sequence shared with
`Application/v9/repos/local/NEXT.md`, which stood at #77 when this file started.
Nothing here is numbered twice and the sequence never restarts.

Opened 26 Aug 2026, from the integrity pass over the version 9 rewrite.

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
  and asked for `sa(ir)` instead of `sa(ir1)`. Both restored.
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
