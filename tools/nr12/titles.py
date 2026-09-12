import sys
import os

# --- paths, resolved from this file rather than hardcoded -------------------
# tools/nr12 -> tools -> Documentation -> the project root.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))
DOCS = os.path.join(_ROOT, "Documentation")
EXAMPLES = os.path.join(_ROOT, "Application", "v9", "repos", "server", "examples")
PDF = os.path.join(_ROOT, "Other", "NR12.pdf")
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
# -*- coding: utf-8 -*-
"""Short problem titles, so each one is the base of its .cir entry's name.

app_links joins a chapter's problems to the app's entries on the title: stage 4
claims an entry whose title is the problem's title plus a parenthetical. That
only works if the two agree, and parse_book truncates an entry name at 80
characters -- so the title has to be short, and the book's own descriptive title
moves into the body of the problem instead.

The two pairs that share a figure need bases that differ from each other, or the
join cannot tell them apart.
"""

SHORT = {
    "5.3c":  "NR12's Example 5.3 part c",
    "7.11a": "NR12's Example 7.11 to 35 ms",
    "7.11b": "NR12's Example 7.11 after 35 ms",
}


def short_title(num):
    """The problem's title, and the base of its entry's name."""
    return SHORT.get(num, "NR12's Example %s" % num)
