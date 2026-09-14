# -*- coding: utf-8 -*-
"""This book's settings for the shared sampler code in tools/sampler."""

#: the book, in Other/ at the project root (not in any repo)
PDF = "AS7.pdf"
#: how the chapter credits a figure: "<CREDIT> -- the circuit for Example 4.10"
CREDIT = "Alexander & Sadiku, 7th edition"
#: a figure's file in Documentation/assets/circuit: (ex|pp, chapter, number)
FIGNAME = "as7-%s%s-%s.jpg"
#: a problem's title prefix, "AS7's Example 4.10"
ABBR = "AS7"
#: the example book the app ships, and its title in the picker
CIR_FILE = "Alexander_Sadiku.cir"
CIR_TITLE = "Problems from Alexander & Sadiku 7ed"
#: the generated chapter in Documentation/src, and its section anchors
CHAPTER = "97-as7-sampler.md"
ANCHOR = "as7"
#: a figure caption in the PDF: "Figure 3.12" on a block of its own
CAPTION_RE = r"^Figure\s*(\d+)\.(\d+)\s*(?:\n|$)"
