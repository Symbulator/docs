# The historical sources — what is on file, and where

This folder is the **primary-source archive of Symbulator's history**,
assembled in August 2026 from Roberto Pérez-Franco's personal papers
for the writing of the monograph (*The Internal Logic of Symbulator*,
`../symbulator_monograph.tex`) and the completion of *The Symbulator
Book* (`../the_symbulator_book.tex`). Roberto supplied every item and
declared the archive **public** (27–28 Aug 2026). Everything here is
version-controlled in the `Symbulator/docs` repository.

**Read these; never edit them.** Where a current text and one of these
sources disagree, the source is right until Roberto says otherwise —
the same rule `../../originals/README.md` states for the 2023
documentation pages. The one nuance learned the hard way: a source can
be *internally* wrong (a mangled extraction, a swapped table row), and
the referee then is the solver — reconstruct the circuit, run it,
compare with the printed answer. That settled Problem 032's `2E3` and
Problem 003's −5.4 A during the Book's completion.

## Inventory

| Item | What it is |
|---|---|
| `1999_paper_spanish_original.docx` | The 1999 competition paper, in Spanish, submitted under the pseudonym *Thévenin* — first place, IEEE Region 9 Student Paper Contest 2000. The earliest account of the design decisions (equation generation over MNA; the TI-89 over the HP line). |
| `1999_paper_english_translation.html` | Its English translation. |
| `2000_thesis/` | **The central source**: the 2000–2001 graduation thesis, *Symbulator: un simulador de circuitos lineales para calculadoras*, defended 9 July 2001, 100/100. Eighteen Word 97 `.doc` files — front pages (`00_`), chapters 1–12 (`01_`–`12_`), closing pages (`13_`), appendices A–D (`14_`–`17_`) — each with an extracted `.txt` beside it. The `.txt` are best-effort (no Word on this machine): produced by `2000_thesis/extract_doc_text.py` (olefile + FIB parse, printable-run fallback); some keystroke glyphs and symbols (∠ ° π √ Ω) were mangled in extraction, so read `.txt` for content and treat garbled spans as recoverable from context. |
| `2000_thesis/english_translation/` | The Burkett–Hutcheson English translation of the thesis (*The Symbulator Book*), abandoned ca. 2001 after the preface, notice, and chapters 1–4; plus the two TI calculator keystroke fonts (`ti89pcb.ttf`, `ti92____.ttf`) it was meant to use. Their working drafts carry flattened tracked changes ("AnnotationNotation") and margin notes to each other. Completed in 2026 as `../the_symbulator_book.tex` + `../book/`, in their voice; published at `learn.symbulator.com/book.pdf`. |
| `2001_jury_record.jpg` | Facsimile of the *Informe de Sustentación* — the defense record of 9 July 2001, three grades of 100 and the tribunal's citation (Logreira, Boulet de Cabrera, Paredes de Vásquez). Reproduced in the monograph's Appendix A. |
| `2000_ieee_award.jpg` | Facsimile of the IEEE Region 9 First Place certificate, October 2000 ("*A Simbolic Simulator*", spelling as issued). Also in the monograph's Appendix A. Note: the same scan lives inside the website archive as `2001_website/symbulator/frontpage/diploma.jpg`. |
| `2001_website.zip`, `2001_website/` | The complete official site of the Symbulator Q era (paxm.org/symbulator), zipped and extracted. `doc/` is the online documentation (introduction, instructions, expert, impala, tools, examples — the monograph's `website2001` citations); `espanol/tododoc.zip` is the complete Spanish documentation bundle; `english/` holds the **same translation ZIPs** later filed under `2000_thesis/english_translation/` — the site was already distributing them in 2001; `download/` is the whole period software shelf (sq.zip is Symbulator Q itself, diffeq.zip is Frederiksen's Laplace engine); `frontpage/comments.html` is a large trove of period user testimonials. |
| `2014_symbulator_book_part1.pdf`, `_part2.pdf` | The unfinished English edition of the Symbulator Book, ca. 2014, documenting Symbulator 6 (the `book2014` citation). Distinct from the 2001 thesis translation. |
| `2014_unpublished_paper_fragment.md` | Fragment of an unwritten paper, ca. 2014 — source of the Hamming paraphrase ("the purpose of circuit analysis is insight, not mathematics") on the monograph's title page. |

Not historical, but kept beside the sources: `../figures/` holds the
monograph's Appendix B schematics (generated — regenerate with
`../render_exemplars.py`, which draws each exemplar with the v9
schematic engine and converts via svglib).

## Related but elsewhere

- **The TI calculator sources themselves** (versions 4–8, plus decoded
  copies): the `symbulator_calculator` git repository, pushed to
  `https://github.com/Symbulator/calculator`.
- **The 2023 documentation originals** (every printed answer of the
  v7/v8 docs): `../../originals/`, with its own README and rules.
- **What was built from this archive**: the monograph
  (`learn.symbulator.com/monograph.pdf`) and the completed Book
  (`learn.symbulator.com/book.pdf`), both sourced from `../`.

## Known discrepancies inside the sources

Recorded so nobody re-litigates them:

- Thesis chapter 12's prose says Problem 087 (Bode) came from
  Prof. Edilberto Yee and Problem 088 (plot) from Prof. Eliane Boulet;
  **Apéndice D's table swaps them**. The prose is the more detailed
  account and is what the monograph and the Book follow.
- The thesis prints Problem 003's `ijb` as 5.4; the Burkett–Hutcheson
  translation prints −5.4, and the solver confirms −5.4 from the
  printed netlist.
- Thesis Problem 032's printed values (−10.4/5.63/4.77 W) require an
  RMS-100 V source entered as `100*√2` and `r2 = 2E3`; the extraction
  of that description line was mangled and the reconstruction was
  verified numerically.
