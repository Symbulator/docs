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

## Build

    python3 build.py              # everything
    python3 build.py --web        # HTML fragments + toc.json only
    python3 build.py --pdf        # LaTeX + PDFs only (needs xelatex)
    python3 build.py --versions 8 # just one version

Output:

    build/web/      upload this whole folder to the server
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

## Deploy

Copy `build/web/` to the docs folder in cPanel and drop the three PDFs in
beside `index.php`. That is the whole deployment: one upload serves all three
versions, and `index.php` picks the right content from `content/v7`, `v8` or
`v9` according to `?v=`. The bundled `.htaccess` turns that into `/7/lesson-dc`.

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

`assets/circuit/*.svg` for the web and `*.pdf` for print, same basename; the
source refers to the `.svg` and the LaTeX emitter drops the extension so
XeLaTeX picks up the PDF. The three figures currently there are stand-ins
drawn by `tools/make_demo_figures.py`, to be replaced by the real schematics.

## Outstanding

- `grep -rn TODO src/` — the chapters still to be converted from the old site
  (lessons 9 to 13 and the credits).
- The 217 imported practice problems are still calculator-only, wrapped in
  `::: only 7,8`. Translating them was blocked on the version 9 API question
  and no longer is; it is roughly 295 commands.
- 248 figures still to supply, almost all of them `assets/practice/*`. See the
  tail of `python3 build.py --check`.

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
