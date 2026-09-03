# The 2023 documentation, as Roberto wrote it

`docs-page7.html` and `docs-page8.html` are the original Symbulator 7 and 8
documentation — one hand-written page per version, from the 2023 website.
Everything in `../src/` was converted from them.

**They are the source of truth for every printed answer and every piece of
calculator code.** Where the current documentation and one of these disagree,
these are right until Roberto says otherwise.

**Read them. Do not edit them.** They are an archive, and their value is that
they record what those calculators actually printed in 2023. Corrections
belong in `../src/`; any that also apply here are Roberto's to make.

Copied here on 26 Aug 2026 from the master copy, which stays where it is:

    C:\Users\perez\OneDrive\_High Archive\_High Archive - Personal\
        Documents\Roberto\Creaciones\Symbulator\Websites\2023 Website\

A third file lives there, `docs-page-blank.html` — the page template, holding
no answers, so it is not copied.

`../tools/check_against_originals.py` reads this folder and verifies every
printed answer in `../src/` against these two pages.

## Why they are worth keeping beside the sources

Each of these was settled by reading these files, and could not have been
settled without them.

**AS7's Example 12.11.** The sources printed `1.36∠-6.2°` for the phase
current. Page 7 carries that typo — but **page 8 prints the correct
`-66.2°`**, because Roberto caught the dropped six himself between the two
versions. The conversion merged the pair into one `out 7,8` block using page
7's value and reinstated a typo he had already fixed. The previous AI, meeting
the same discrepancy, invented a warning arguing that `-6.2°` was a different
phase current correctly labelled.

**AS7's Practice Problem 11.10.** `s\pf("e") gives pf: 0.93595 leading` is
verbatim in both pages. That ruled out the suspicion that the line had been
fabricated, and left a typed word as the explanation — the load is inductive,
so it is lagging.

**The corrupt exponent.** Six lines in chapter 9 read `ᴐ00`, with a
small-capital open O. These pages print `ᴇ0`, which fixed both the wrong
letter and the wrong digit count.

**Chapter 7's units.** Seven answers appear here as prose, with their units —
"We get 2.708∠-56.73º V and 6.914∠-80.70º mA" — where the conversion had
reformatted them into unit-less transcripts with quotes and `ᴇ0` exponents
that the calculator never printed for them.

**The two-port naming.** Page 7 uses `zp`, `zp11`, `izp1`, `r`; page 8 uses
`z`, `z11`, `iz1`, `r1`. The conversion gave page 7's spelling to both. Only
these files show that the two versions were deliberately different — the
Titanium and the Nspire have different reserved names.
