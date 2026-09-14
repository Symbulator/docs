# -*- coding: utf-8 -*-
"""Short problem titles, so each one is the base of its .cir entry's name.

app_links joins a chapter's problems to the app's entries on the title, and
parse_book truncates an entry name at 80 characters, so a title is short and
the same on both sides. See tools/nr12/titles.py for the whole story.
"""

SHORT = {
    "7.13a":  "AS7's Example 7.13 to 4 s",
    "7.13b":  "AS7's Example 7.13 after 4 s",
    "19.17a": "AS7's Example 19.17 gains",
    "19.17b": "AS7's Example 19.17 output impedance",
}


def short_title(num):
    """The problem's title, and the base of its entry's name."""
    import book, fmt
    return SHORT.get(num, "%s's %s %s" % (book.ABBR, fmt.num_label(num), fmt.base_num(num)))
