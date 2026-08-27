# Symbulator documentation

One source tree; three PDFs and one website come out of it.
See `SPEC.md` for the markup.

## Requirements

- Python 3.9 or newer, plus `pip install -r requirements.txt`
- IBM Plex, for the PDFs — `sh tools/install_plex.sh`, or your package manager
  (`apt install fonts-ibm-plex`, `brew install --cask font-ibm-plex`). Without
  it the build falls back to TeX Gyre and says so.
- XeLaTeX, for the PDFs only. On Windows install MiKTeX; on macOS MacTeX; on
  Linux `texlive-xetex texlive-fonts-recommended texlive-latex-extra`.
  Skip it and `--web` still works.
- PHP is *not* needed to build. It runs on the server, and cPanel already has it.


## Deploying

    cd "C:\Users\perez\Claude Code"
    py deploy_symbulator.py learn

Since 27 Aug 2026 this is how the site moves. It uploads only what changed
out of `build/web/`, over SSH, and verifies over HTTPS afterwards — by hash
for the assets, by content for the pages PHP renders. `--dry-run` first if
you want to see what it would send.

**Run `build.py` before deploying.** `build/web/` is generated; deploying
without rebuilding publishes whatever was last built.

The three PDFs are large (~27 MB each) and rarely change, so most deploys
move only `content/` and `assets/`. Do not let that become an assumption on
a deploy that touched `index.php` or `.htaccess`.

The ZIPs beside this file — `learn_symbulator_com.zip`,
`symbulator_com_landing.zip` — are how the site moved *before* that date.
They are history and are now stale; do not deploy from them.

## Build

    python3 build.py              # everything
    python3 build.py --web        # HTML fragments + toc.json only
    python3 build.py --pdf        # LaTeX + PDFs only (needs xelatex)
    python3 build.py --versions 8 # just one version

Output:

    build/web/      what a `learn` deploy uploads (see below)
                    (including content/v*/search.json -- see below)
    build/pdf/      symbulator-v7.pdf, -v8.pdf, -v9.pdf
    build/tex/      the generated LaTeX, kept for debugging
    build/preview/  flat HTML for looking at the site without PHP
                    (python3 tools/static_preview.py)

## While you write

    python3 tools/watch.py

Rebuilds the site the moment you save a file in `src/`, and refreshes
`build/preview/`. Open `build/preview/v7-home.html` in a browser and reload as
you go. Add `--pdf` if you also want the PDFs rebuilt, though that is slow
enough that you probably only want it before publishing.

## How one upload serves three versions

`index.php` picks the right content from `content/v7`, `v8` or `v9` according
to `?v=`, and the bundled `.htaccess` turns that into `/7/lesson-dc`. So a
deploy is one folder, not three. The three PDFs sit beside `index.php` and are
named `symbulator-v7.pdf`, `-v8`, `-v9` — the ribbon's **Download the PDF**
button links to them by name and is version-aware.

`.htaccess` is a dotfile, and file managers hide dotfiles by default. If it
never arrives, `https://learn.symbulator.com/9/lesson-dc` 404s while
`?v=9&p=lesson-dc` still works — so the home page looks fine and every pretty
URL is broken. `deploy_symbulator.py` sends it like any other file, which is
one reason to prefer it over a file manager.

## The sidebar search

The box at the top of the Contents column searches **only the version being
read**. It is three pieces:

- `build.py` writes `build/web/content/v<N>/search.json`, one entry per
  section and per worked problem, for that version alone.
- `web/index.php` renders the box and fetches that file on the reader's first
  keystroke -- a few hundred kilobytes, so it is not loaded before then.
- `web/assets/style.css` styles it, under `.docsearch`.

Nothing ties the three together but `build.py --check`, which fails if the
path or the element ids in `index.php` stop matching what the build writes,
if the stylesheet loses its rules, or if a built index is missing a chapter
its own table of contents lists. **A deploy that leaves `search.json` behind
gives every reader "Search is unavailable on this server."**

`tools/static_preview.py` generates its own markup and does not read
`index.php`, so the flat preview has no search box. That is expected.

## What to edit

- Text .............. `src/*.md`
- Chapter order ..... `book.yaml`
- Words that vary
  by version ........ `terms:` in `book.yaml`
- Look of the PDF ... `tex/symbulator.cls`
- Look of the site .. `web/assets/style.css`, `web/index.php`

Never edit anything in `build/` — the next build overwrites it.

## Figures

**All real, since 27 Aug 2026 — verified by opening the built PDFs, not by
build success.** Every one of the 314 `::: figure` references in `src/`
cites a raster (`.jpg`/`.jpeg`/`.png`), every one of those files is genuine
artwork, and both builds consume the raster directly: the HTML emitter
writes the path verbatim, and the LaTeX emitter passes a raster path
through unchanged (it only drops the extension — so XeLaTeX would pick a
`.pdf` twin — for non-raster references, of which there are currently
none).

This section used to describe an `.svg`-for-web / `.pdf`-for-print scheme
and "248 figures still to supply". That era ended when the real scans
arrived; what it left behind were ~250 orphaned placeholder `.svg`/`.pdf`
siblings in `assets/` that nothing referenced (removed 27 Aug 2026 —
`tools/make_placeholders.py` can redraw a placeholder any time a reference
appears without its file, and never overwrites real artwork).

## Outstanding

- `grep -rn TODO src/` — currently returns nothing; the conversion of the
  old site's chapters is complete.
- Every problem now has version 9 content (measured 27 Aug 2026; this
  bullet once said 217 imported problems were calculator-only). The last
  two — AS7's Example 2.10 and Practice Problem 2.10, the nested parallel
  reductions in `03-lesson-sources.md` — gained v9 answers through the
  Evaluate card's `pr()` that day. A counting caution for whoever measures
  next: some problems exist twice, as parallel `::: only 7,8` / `::: only
  9` twins (B11's Example 5.6 "using ex" in `02-lesson-symbolic.md` is
  one), so a per-block scan finds calculator-only blocks that are in fact
  covered by their twin.

- One correction to confirm: in `08-lesson-power.md`, the AC maximum-power
  example used to say the conjugate of the equivalent impedance was
  2.933 + j4.467. The impedance *is* 2.933 + j4.467, so its conjugate is
  2.933 − j4.467. Corrected on 21 August 2026, but it touches the calculator
  text as well as version 9's, so it is worth checking against the original.

The version 9 API claims have been checked against the real package and the
source corrected to match. `VERIFIED-v9-api.md` has the findings, run rather
than read — including two traps worth knowing about even now: `pf()` reports
leading/lagging backwards for a source unless you negate the current, and
time-domain answers use `Symbol("t", nonnegative=True)`, so a bare
`Symbol("t")` silently fails to substitute.

That second one said `positive=True` until 26 Aug 2026. It is `nonnegative`,
and the difference is load-bearing rather than pedantic: SymPy evaluates
DiracDelta of a strictly *positive* argument to 0, so under `positive` every
impulse quietly disappeared, and `symbulator.laplace` says so at length.
The same note, followed up in the app, turned out to be the whole of #95 in
`Symbulator/repos/local/NEXT.md` — and to point the wrong way round: the
boxes on the page parse `t` correctly and always did, and it is the answers
that lose the assumption on the way back.

## The look

`DESIGN.md` sets out the palette, the typography and the shared conventions,
with the tokens themselves in `design/tokens.css` and `design/tokens.json`.
It is written as a handoff to whoever is working on the Symbulator 9 interface,
so the app, the website and the PDFs can be kept in line.

## The written guide

`guide/how-to-use.pdf` explains all of this at length — editing, building,
publishing and the markup — typeset with the same class as the documentation
itself. Rebuild it with `sh guide/build-guide.sh` after editing
`guide/how-to-use.tex`.

## Checking the source

    python3 build.py --check

Validates cross-references, version terms, code-fence version tags and the
figure pairs, for every version, and exits non-zero if anything is wrong. The
same check runs at the start of every build, as a warning.
