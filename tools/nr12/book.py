# -*- coding: utf-8 -*-
"""This book's settings for the shared sampler code in tools/sampler."""

#: the book, in Other/ at the project root (not in any repo)
PDF = "NR12.pdf"
#: how the chapter credits a figure: "<CREDIT> -- the circuit for Example 4.10"
CREDIT = "Nilsson & Riedel, 12th edition"
#: a figure's file in Documentation/assets/circuit: (ex|pp, chapter, number)
FIGNAME = "nr12-%s%s-%s.jpg"
#: a problem's title prefix, "NR12's Example 4.10"
ABBR = "NR12"
#: the example book the app ships, and its title in the picker
CIR_FILE = "Nilsson_Riedel.cir"
CIR_TITLE = "Problems from Nilsson & Riedel 12ed"
#: the generated chapter in Documentation/src, and its section anchors
CHAPTER = "98-nr12-sampler.md"
ANCHOR = "nr12"
#: a figure caption in the PDF: "Figure 4.10 <triangle> ..."
CAPTION_RE = r"^Figure\s*(\d+)\.(\d+)\s*[\u25b2\u25bc\u2b25\u25c0\u25b6]"
