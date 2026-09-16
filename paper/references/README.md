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
| `1999_paper_spanish_original.docx` | The 1999 competition paper, in Spanish, submitted under the pseudonym *Thévenin* — first place, IEEE Region 9 Student Paper Competition (certificate October 2000). The earliest account of the design decisions (equation generation over MNA; the TI-89 over the HP line). |
| `1999_paper_spanish_original.pdf` | **The same paper as a PDF**, printed from Word in 2008 and re-saved in 2013 — so it is a **later rendering of the text, not the 1999 submission itself**: the body still carries *Seudónimo: Thévenin*, which is how the paper was judged, but Roberto's name was added to the file's own properties afterwards (`Author: Roberto Perez Franco`). Roberto's word, 16 Sep 2026: *"the paper was submitted under the pseudonym Thévenin. I added my name later."* Its text matches the `.docx` word for word. Publish it as the paper, never as a facsimile of the entry. |
| `2000_noticieeero_28_4_panama.pdf` | ***El NoticIEEEro***, IEEE Sección Panamá, **volume 28 no. 4, December 2000**, 12 pages. The paper reprinted under Roberto's own name on pages 3, 6 and 7, headed *Resumen del proyecto ganador del "1999 Regional Student Paper Contest"*, with one worked example (the FD Bode circuit) instead of the paper's four. Page 5 announces the contest result itself — first place, $550, ahead of Santo Tomás Aquino (Colombia) and a second UTP entry. **The first publication of the paper anywhere.** |
| `2001_buran_17_ieee_barcelona.pdf` | ***BURAN* nº 17, September 2001**, *Rama de Estudiantes del IEEE de Barcelona*, pages 24–29. The paper published in full under Roberto's own name and e-mail, all four worked examples and eight calculator screens. Adds what the 1999 text could not know: half a year after release users in seventeen countries, Chris Riegel's and Jay Myers' testimonials, and the site named as `http://scs.ticalc.org` with "más de cuarenta ejemplos". **This is the IEEE paper's month — September 2001.** |
| `1999_paper_english_translation.html` | The English translation of the paper. |
| `2000_thesis/` | **The central source**: the 2000–2001 graduation thesis, *Symbulator: un simulador de circuitos lineales para calculadoras*, defended 9 July 2001, 100/100. Eighteen Word 97 `.doc` files — front pages (`00_`), chapters 1–12 (`01_`–`12_`), closing pages (`13_`), appendices A–D (`14_`–`17_`) — each with an extracted `.txt` beside it. The `.txt` are best-effort (no Word on this machine): produced by `2000_thesis/extract_doc_text.py` (olefile + FIB parse, printable-run fallback); some keystroke glyphs and symbols (∠ ° π √ Ω) were mangled in extraction, so read `.txt` for content and treat garbled spans as recoverable from context. |
| `2000_thesis/english_translation/` | The Burkett–Hutcheson English translation of the thesis (*The Symbulator Book*), abandoned ca. 2001 after the preface, notice, and chapters 1–4; plus the two TI calculator keystroke fonts (`ti89pcb.ttf`, `ti92____.ttf`) it was meant to use. Their working drafts carry flattened tracked changes ("AnnotationNotation") and margin notes to each other. Completed in 2026 as `../the_symbulator_book.tex` + `../book/`, in their voice; published at `learn.symbulator.com/book.pdf`. |
| `2001_jury_record.jpg` | Facsimile of the *Informe de Sustentación* — the defense record of 9 July 2001, three grades of 100 and the tribunal's citation (Logreira, Boulet de Cabrera, Paredes de Vásquez). Reproduced in the monograph's Appendix A. |
| `2000_ieee_award_colour.jpg` | **The colour scan of the IEEE Region 9 First Place certificate**, October 2000 — 2000×1554, supplied 16 Sep 2026 and **the one the monograph prints** (Appendix A). Reads *First Place in the 2000 Region 9 Student Paper Competition* for "*Symbulator: A Simbolic Simulator of Circuits for Calculators*", signed by the IEEE's Secretary and President. |
| `2000_ieee_award.jpg` | The earlier black-and-white scan of the same certificate, 821×626. Superseded by the colour one above for printing; kept because it is the copy the 2001 site served, as `2001_website/symbulator/frontpage/diploma.jpg`. |
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

- **The competition's year is printed two ways.** The certificate
  (`2000_ieee_award.jpg`) reads *First Place in the 2000 Region 9
  Student Paper Competition*, October 2000; the Panama bulletin of
  December 2000 calls the same result the *"1999 Regional Student Paper
  Contest"* and heads its list *Ganadores del Paper Contest Estudiantil
  1999*. Both are primary and both are IEEE's own. Treat the paper as
  written and entered in 1999 and the award as October 2000, and quote
  the certificate's wording when a year must be attached to the prize.
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
