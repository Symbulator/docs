# The Alexander & Sadiku sampler -- its data

`src/97-as7-sampler.md` and `examples/Alexander_Sadiku.cir` are generated
from `specs.py` here by the shared generator in `tools/sampler`, exactly as
the Nilsson & Riedel sampler is. **The rules for writing an entry, the spec
fields, the gates and the train are in `tools/nr12/README.md`**, which is
the one canonical copy; nothing here restates them.

    py Documentation\tools\as7\gen.py
    py -c "import runner, specs; runner.check(specs.SPECS, verbose=False)"   (from tools/as7)
    py Documentation\tools\as7\check_card_truth.py

The book is `Other/AS7.pdf`, 993 pages, readable with pymupdf; a printed
page number is the PDF page minus 26. A problem number is `3.4` for an
example and `p3.4` for a practice problem.
