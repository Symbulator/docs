# A Baker's Dozen (#464)

A 14-page PDF of twelve solved examples from Symbulator 9's documentation,
plus a bonus. It is served at **https://learn.symbulator.com/dozen.pdf** and
linked from **https://symbulator.com/** as the sixth item of *What it does*,
under the label *Get a taste*. Made on 16 Sep 2026 at Roberto's request.

These notes exist so the selection can be changed later without re-deriving
why it is what it is.

## Roberto's brief (16 Sep 2026)

- The most interesting solved examples in the documentation, **between 10
  and 20**.
- **Grandfathered in:** his own 2013 one-of-each problem (Lesson 3's
  *Showing-off Problem*) and Prof. Eliane Boulet's transient (Lesson 6's
  *A more complex problem*).
- Problems that **look complex but Symbulator solves in one pass**, or in
  two when a switch splits the problem into intervals. Three intervals
  breaks the rule.
- **No two problems of the same type.** Each one makes a different point.
- Title **A Baker's Dozen** (Roberto, 17 Sep 2026): thirteen, the
  thirteenth being his. It was first titled for a plain dozen, "even though
  it's 13, because mine is a bonus". Each page's kicker reads *Sample N of
  12*, and the bonus page's reads *Bonus*. His problem is the bonus, titled **"A freebie, on the house"** at his
  word. The page still names it as Lesson 3's Showing-off Problem so a
  reader can find it in the Course.

## The selection, and the point each one makes

| # | Problem | Where | Point | Runs |
|---|---|---|---|---|
| 1 | AS7 Example 3.4 | AS7 sampler, `?lesson=as7&entry=2` | supernodes around a dependent source | 1 |
| 2 | NR12 Example 5.7 | NR12 sampler, `?lesson=nr12&entry=14` | a realistic op-amp model, exact gain | 1 |
| 3 | Bo2 Example 3.3 | Lesson 5, `?lesson=5b&entry=14` | symbolic: two op amps, all conductances | 1 |
| 4 | AS7 Problem 9.73 | Lesson 7, `?lesson=7&entry=6` | eight impedances that need delta-wye by hand | 1 |
| 5 | AS7 Example 10.14 | Lesson 7, `?lesson=7&entry=10` | AC nodal with a dependent source | 1 |
| 6 | AS7 Example 12.11 | Lesson 9, `?lesson=9&entry=6` | three-phase wye-delta, no transformation | 1 |
| 7 | AS7 Practice Problem 13.13 | AS7 sampler, `?lesson=as7&entry=48` | coupled coils (k) in AC | 1 |
| 8 | NR11 capacitor shorted by a switch, coupled 0.8 H and 1.6 H | Lesson 10, `?lesson=10&entry=17,18` | a transient across a coupling | 2 |
| 9 | Bo2 Drill Exercise 6.6 | Lesson 6, `?lesson=6d&entry=7,8` | active second order, repeated pole | 2 |
| 10 | Prof. Boulet's exam problem | Lesson 6, `?lesson=6d&entry=18,19` | damped-sine source, two modes *(grandfathered)* | 2 |
| 11 | AS7 Problem 19.2 | Lesson 13, `?lesson=13&entry=14` | a two-port with no ground | 1 |
| 12 | NR12 Example 18.6 | NR12 sampler, `?lesson=nr12&entry=16` | two-ports as elements, cascaded | 1 |
| Bonus | The Showing-off Problem | Lesson 3, `?lesson=3&entry=49` | Expert Mode, one dependent source of each kind *(grandfathered)* | 1 |

**Reserves**, each left out only because it repeats a point already made:

- **AS7 Problem 10.77** (Lesson 7, entry 14): AC op amp, everything
  symbolic including ω. Repeats #3.
- **NR12 Example 9.15** (NR12 sampler, entry 41): Thévenin through a linear
  transformer, RMS. Repeats #7.
- **AS7 Practice Problem 5.13** (AS7 sampler, entry 15): R_G for a
  three-op-amp instrumentation amplifier. Overlaps #3 and the bonus.

**Left out on purpose:**

- **The 1999 two-stage amplifier** (`The_Monograph.cir`, entry 1) qualifies
  easily, but it is in the monograph, not the documentation.
- **Three-interval problems** (Bo2 Example 5.6, NR12 Example 7.11) take
  three runs.
- **AS7 Example 10.6** takes three runs by superposition.
- **Bo2 Example 6.6**, the 3991 V inductor kick, is striking but looks
  simple.

## How it is built

- `build_dozen.py` holds the whole selection: the question, the *Why it is
  here* line, the settings line and the answers for each problem. It lays
  them out as HTML in the docs palette (`style.css`) and prints
  `paper/the_bakers_dozen.pdf` through Microsoft Edge, headless. **It needs
  the network**, for IBM Plex and KaTeX from their CDNs.
- **The circuit descriptions are not typed here.** They are read from the
  app tree's `.cir` entries by book and position, so they cannot drift from
  what the links open.
- **The answers are typed here**, as LaTeX. They were checked against the
  app through `/api/solve` on 16 Sep 2026.
- **AS7 Problem 19.2's figure** is `ladder.svg`, drawn by `ladder.py`,
  because the chapter's own schematic is unreadable at page width. The
  other figures come from `Documentation/assets/`.
- **Boulet's answers** are printed with their √3 terms. Lesson 6 had lost
  every root in all three versions until #464 restored them. Do not copy
  the answers back from an old build.
- `Documentation/build.py` copies the PDF to `build/web/dozen.pdf` and fails
  if it is missing, and `Deploy/deploy_targets.ini` verifies it by hash
  after a `learn` deploy.

## The LaTeX version

`bakers_dozen.tex` is the same booklet as a LaTeX document, made at
Roberto's request on 17 Sep 2026 for the public repository. It is
**generated** by `build_dozen_tex.py` from the same `P` and `BONUS` data as
the published PDF, so the two cannot disagree. Edit `build_dozen.py`, then
regenerate. Never edit the `.tex` by hand.

    py paper\bakers_dozen\build_dozen_tex.py          # write the .tex
    py paper\bakers_dozen\build_dozen_tex.py --pdf    # and compile it

- **Compiles with XeLaTeX**: 14 A4 pages, with no overfull boxes and no
  missing characters in the log. It needs IBM Plex Sans, Serif and Mono
  installed, plus DejaVu Sans Mono, which ships with TeX distributions.
- **Plex Serif and Mono have no Greek and no ∠**, so Ω, ω and Δ are set as
  maths and ∠ in DejaVu Sans Mono, through `newunicodechar`.
- **Figures** come from `Documentation/assets/` by relative path. They are
  sized as the HTML booklet sizes them, at 96 px to the inch and capped at
  62 mm tall. **AS7 Problem 19.2's ladder is drawn with circuitikz**, not
  taken from `ladder.svg`, which XeLaTeX cannot include.
- **`--pdf` writes `bakers_dozen_latex.pdf`** beside the source, for
  checking. It is not committed, and the published
  `learn.symbulator.com/dozen.pdf` is still the Edge-printed one.
- **Run labels are not uppercased**, because *TR, t > 0* carries a
  variable.

## Changing the selection

1. **Run `py paper\bakers_dozen\check_dozen.py` first.** It fails if any
   entry has moved in its `.cir` (EXPECT pins each position to its title)
   or no longer solves. It also prints the app's answers beside the
   booklet's for a person to compare. It was proved red on 16 Sep 2026 by
   pretending an entry had moved.
2. **To swap a problem**, edit its `dict` in `build_dozen.py` and its lines
   in `check_dozen.py`'s EXPECT and WATCH. Take the answers from the app,
   not from the chapter, because chapters have been wrong (see Boulet).
   Keep the brief: one or two runs, a point no other entry makes.
3. **If an entry moved**, fix its position in both files. Positions shift
   whenever an entry is inserted above one in a `.cir` book.
4. **Rebuild:** `py paper\bakers_dozen\build_dozen.py`, then read the pages
   back (a new figure can overflow a page), then `py build.py --web` and a
   `learn` deploy.
5. **If the page count or size changes**, update the *Get a taste* item in
   `Documentation/landing/index.html`, which says *PDF, 1.0 MB, 14 pages*,
   and deploy `landing` too.
6. **If the count stops being twelve plus a bonus**, the title, the
   cover's *Sample N of 12* kickers and the landing blurb all say so.

## Things worth knowing

- **Entry titles over 80 characters are cut** by the app (`circuitbook.py`,
  `MAX_NAME_LEN`). The two NR11 entries of #8 were 82 long, and the app's
  picker showed them ending in *"(DC, t <"*. At Roberto's word they were
  renamed the same night, *"switch and coupled"* becoming *"switch,
  coupled"* (79 characters), together with the Lesson 10 problem heading
  and its two `::: applink` lines, which join on the title. No title in any
  book is over 80 now. `check_dozen.py` still compares titles the way the
  app reads them. A renamed entry changes the docs' app links, so run
  `Documentation/tools/app_links.py` before and after.
- **The landing item moved four times on 16 Sep 2026**: last in *Learn it*,
  then first there, then below *What it will not do*, and finally beside
  *Expert mode*. Leave it where it is unless Roberto says otherwise.
- **The same evening, Roberto removed the landing page's *Open a worked
  problem* card** (*Hundreds of them, built in*). Do not restore it as part
  of this item.
