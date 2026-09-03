"""#224: which built-in app entry each worked problem in the tutorial is.

The tutorial's chapters and the app's input files were written as two
separate things and were never numbered against each other. Lesson 6 has
51 worked problems in the book and 80 entries across its four `.cir`
files, because a transient problem is usually two runs -- a DC pass for
the initial condition, then the TR itself. So there is no positional
correspondence to exploit, and the join has to be made on content.

Two keys are available, and both are needed:

  * the figure. Since #219 an entry carries `image:` pointing at the
    tutorial's own artwork on learn.symbulator.com, and the chapter
    carries `::: figure` naming the same file. 297 of the 310 lesson
    entries have one.
  * the title. An entry is titled like the problem it belongs to, with a
    parenthetical saying which run it is: `[Bo2's Example 5.1 (TR)]`.

Neither alone is enough. The figure misses the entries that reuse a
picture the chapter prints once, and it *over*-collects: the two entries
of `AS2's Example 5.7` carry the figure of `AS2's Figure 5.24`, because
the circuit they solve is four elements deep inside that one drawing.
The title misses the ones the chapter names differently. Run in the
order below -- most specific claim first, each entry claimed once --
they leave a residue this module's self-check prints, so a gap is a
number someone can look at rather than a silent absence.

Run it on its own to see that number:

    py tools\\app_links.py

This module reads the *app* tree, which is a sibling of this one. That
is the same reach across that `SHARED_BANNER` in build.py already makes
for the banner, and it fails the same way -- loudly, naming the layout
it expected -- rather than quietly shipping a book with no links in it.
"""

from __future__ import annotations

import os
import re
import unicodedata
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: The app's built-in input files. `repos/server/examples` is the source;
#: `repos/local/examples` is generated from it by build_local.py, so this
#: reads the one people edit.
EXAMPLES = os.path.normpath(os.path.join(
    ROOT, "..", "Application", "v9", "repos", "server", "examples"))

#: Hardwired to version 9 (Roberto, 2 Sep 2026: "X is for experiments,
#: not for users. Use the default app link, v9, always, hardwired.").
APP_URL = "https://symbulator.pythonanywhere.com/"

#: Where the split view lives on this site. Root-absolute, like every
#: other URL this build writes.
SPLIT_URL = "/split/"

#: chapter id -> the `.cir` books that hold its circuits, in reading
#: order. Four of the thirteen lessons are split across parts, and the
#: parts are one continuous run of problems in the book.
CHAPTER_BOOKS = {
    "lesson-dc":          ["1"],
    "lesson-symbolic":    ["2"],
    "lesson-sources":     ["3"],
    "lesson-equivalents": ["4a", "4b"],
    "lesson-opamps":      ["5a", "5b"],
    "lesson-transient":   ["6a", "6b", "6c", "6d"],
    "lesson-ac":          ["7"],
    "lesson-power":       ["8"],
    "lesson-threephase":  ["9"],
    "lesson-coupling":    ["10"],
    "lesson-bode":        ["11"],
    "lesson-fd":          ["12"],
    "lesson-twoports":    ["13"],
}

_ENTRY_RE = re.compile(r"^\[(.+?)\]\s*$", re.M)
_IMAGE_RE = re.compile(r"^image:\s*(\S+)", re.M)
_QUAL_RE = re.compile(r"^(.*?)\s*\((.*)\)\s*$")


@dataclass(frozen=True)
class Entry:
    """One entry of one built-in input file."""
    lesson: str      # "4b" -- the app's ?lesson= word
    index: int       # 1-based, the app's ?entry=
    title: str       # as it stands between the brackets
    image: str       # site-relative figure path, or ""

    @property
    def anchor(self) -> str:
        return f"e-{self.lesson}-{self.index}"

    @property
    def app_href(self) -> str:
        return f"{APP_URL}?lesson={self.lesson}&entry={self.index}"

    @property
    def split_href(self) -> str:
        return f"{SPLIT_URL}?lesson={self.lesson}&entry={self.index}"


def _fold(s: str) -> str:
    """A comparison key. Accents folded (the book says Thevenin in one
    place and Thevenin-with-an-acute in the other), emphasis markers and
    version spans taken out, everything but letters and digits dropped."""
    s = re.sub(r"\{\{[^}]*\}\}", "", s)
    s = "".join(c for c in unicodedata.normalize("NFKD", s)
                if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _split_qual(title: str) -> tuple[str, str]:
    """Bo2's Example 5.1 (TR) -> ("Bo2's Example 5.1", "TR").

    Lesson 2 writes the same distinction with a comma rather than
    brackets -- "B11's Example 5.6, with solve" against "..., using ex" --
    so a comma counts too when there is no parenthetical. Only those two
    titles in the book take that form, and no entry title has a comma
    outside its brackets, so the two readings cannot collide."""
    m = _QUAL_RE.match(title)
    if m:
        return m.group(1), m.group(2)
    if "," in title:
        base, qual = title.split(",", 1)
        return base.strip(), qual.strip()
    return title, ""


def load_books(examples_dir: str = EXAMPLES) -> dict[str, list[Entry]]:
    """Every lesson book, as lesson word -> entries in file order."""
    if not os.path.isdir(examples_dir):
        raise SystemExit(
            f"app_links: {examples_dir} is missing. The tutorial's worked "
            "problems link to the app's built-in entries (#224), which are "
            "read from the app repository (Application/v9/repos/server/"
            "examples, a sibling tree's grandchild of Documentation -- see "
            "the top-level CLAUDE.md). Without it this site would build "
            "with no app links at all, which is a silent loss rather than "
            "a visible one, so the build stops here instead.")
    books: dict[str, list[Entry]] = {}
    for name in sorted(os.listdir(examples_dir)):
        m = re.fullmatch(r"Lesson_0?(\d{1,2})([a-d]?)\.cir", name)
        if not m:
            continue
        lesson = m.group(1) + m.group(2)
        text = open(os.path.join(examples_dir, name), encoding="utf-8").read()
        parts = _ENTRY_RE.split(text)[1:]
        entries = []
        for i in range(0, len(parts), 2):
            img = _IMAGE_RE.search(parts[i + 1])
            path = ""
            if img:
                path = img.group(1).split("learn.symbulator.com/")[-1]
                path = path.lstrip("/")
            entries.append(Entry(lesson, i // 2 + 1, parts[i], path))
        books[lesson] = entries
    return books


def resolve_chapter(chapter_id: str, problems: list, books=None) -> list:
    """The entries of each worked problem, in the order the problems are
    given. `problems` is (title, [figure paths]) per problem, already
    filtered to the version being rendered.

    Each entry is claimed by at most one problem, and the stages run
    most-specific first so that a problem naming its own variant takes it
    before a problem that only shares the base title can.
    """
    books = load_books() if books is None else books
    pool: list[Entry] = []
    for key in CHAPTER_BOOKS.get(chapter_id, []):
        pool += books.get(key, [])
    found: list[list[Entry]] = [[] for _ in problems]
    if not pool:
        return found

    taken: set[Entry] = set()
    keys = []
    for title, figs in problems:
        base, qual = _split_qual(title)
        keys.append((_fold(title), _fold(base), _fold(qual),
                     {f.lstrip("/") for f in figs}))
    ent = []
    for e in pool:
        base, qual = _split_qual(e.title)
        ent.append((_fold(e.title), _fold(base), _fold(qual)))

    def claim(test):
        for i in range(len(problems)):
            for j, e in enumerate(pool):
                if e not in taken and test(keys[i], ent[j], e):
                    found[i].append(e)
                    taken.add(e)

    def distribute(idxs: list[int]):
        """Split the still-unclaimed entries of one base between the
        problems that share it, in reading order. Both sequences are in
        reading order, so contiguous chunks line them up without anyone
        having to know where Part 2 begins."""
        base = keys[idxs[0]][1]
        group = [e for j, e in enumerate(pool)
                 if ent[j][1] == base and e not in taken]
        for n, i in enumerate(idxs):
            lo = n * len(group) // len(idxs)
            hi = (n + 1) * len(group) // len(idxs)
            for e in group[lo:hi]:
                found[i].append(e)
                taken.add(e)

    def sharing(same_title: bool, unsatisfied: bool) -> list[list[int]]:
        groups: dict[str, list[int]] = {}
        for i, k in enumerate(keys):
            if unsatisfied and found[i]:
                continue
            groups.setdefault(k[0] if same_title else k[1], []).append(i)
        return [g for g in groups.values() if len(g) > 1]

    # 0. A title the chapter uses twice is two problems, not one. Lesson 4
    #    walks through B11's Example 8.29 in Part 1 and sets it again in
    #    Part 2, and the two parts have a book each. Split before stage 1,
    #    or the exact match hands Part 2's entry to Part 1.
    for g in sharing(same_title=True, unsatisfied=False):
        distribute(g)

    # 1. the same title, word for word.
    claim(lambda p, c, e: p[0] == c[0])
    # 2. the same base and the same parenthetical -- "(Subtractor)" is
    #    that problem's entry even though a sibling problem shares the
    #    drawing it is four elements deep inside.
    claim(lambda p, c, e: p[1] == c[1] and p[2] and p[2] == c[2])
    # 3. the entry refines the problem's own parenthetical:
    #    "(Tricky)" -> "(Tricky, as it comes)".
    claim(lambda p, c, e: p[1] == c[1] and p[2] and c[2].startswith(p[2]))
    # 3b. Several problems still share a base and none of them named its
    #     entry in a way the three stages above could recognise -- Lesson
    #     2's "with solve" against "using ex", where the book and the app
    #     word the same distinction differently. Split what is left of the
    #     base between them in reading order. After stage 2, so that a
    #     problem which *did* name its entry has already taken it: Lesson
    #     5's "(Subtractor)" is claimed before its sibling can be handed
    #     the drawing they share.
    for g in sharing(same_title=False, unsatisfied=True):
        distribute(g)
    # 4. the problem has no parenthetical and the entry adds one:
    #    "Bo2's Example 5.1" -> "(DC, for the initial condition)", "(TR)".
    claim(lambda p, c, e: p[1] == c[1] and not p[2])
    # 5. the same base, any parenthetical. Last of the title stages, so a
    #    problem that names its variant has already taken it.
    claim(lambda p, c, e: p[1] == c[1])
    # 6. the figure. Only entries no title stage accounted for, which is
    #    what keeps a shared drawing from dragging in its neighbours.
    claim(lambda p, c, e: bool(e.image) and e.image in p[3])
    return found


def entry_label(entry: Entry, problem_title: str) -> str:
    """What tells one of a problem's entries from another: the entry's
    parenthetical, less whatever of it the problem's title already said.
    Empty when the problem has a single entry -- there is nothing to tell
    apart, and "Open in app" alone reads better than "Open in app: TR"."""
    _, cq = _split_qual(entry.title)
    _, pq = _split_qual(problem_title)
    if not cq:
        return ""
    if pq and cq.startswith(pq) and cq[len(pq):].lstrip().startswith(","):
        cq = cq[len(pq):].lstrip()[1:].strip()
    # "DC, for the initial condition" is a sentence, not a label. The part
    # before the comma is the run it is -- DC, TR -- which is the whole
    # distinction being drawn.
    if len(cq) > 24 and "," in cq:
        cq = cq.split(",", 1)[0].strip()
    return cq


def chapter_problems(ch, v: int) -> list:
    """Every worked problem visible in version v, with its figures, in
    reading order. Shared with build.py so the map and the page are made
    from the same walk of the same tree."""
    import build
    out = []

    def figures(b):
        figs = []

        def dig(blocks):
            for c in build.walk(blocks, v):
                if c.kind == "figure":
                    figs.append(c.arg)
                elif c.children:
                    dig(c.children)
        dig(b.children)
        return figs

    def visit(blocks):
        for b in build.walk(blocks, v):
            if b.kind == "problem":
                out.append((b.arg, figures(b)))
            elif b.children:
                visit(b.children)

    visit(ch.blocks)
    return out


def _self_check() -> int:
    """Coverage, measured against the real chapters. Prints the residue on
    both sides: problems with no entry, and entries no problem claimed."""
    import sys
    sys.path.insert(0, ROOT)
    import build

    books = load_books()
    total = sum(len(v) for v in books.values())
    claimed = 0
    gaps = []
    book = build.load_book()
    for ch in book.chapters:
        if ch.id not in CHAPTER_BOOKS:
            continue
        problems = chapter_problems(ch, 9)
        got = resolve_chapter(ch.id, problems, books)
        for (title, _), entries in zip(problems, got):
            claimed += len(entries)
            if not entries:
                gaps.append(f"{ch.id}: PROBLEM {title} -- no entry")
        seen = {e for es in got for e in es}
        for key in CHAPTER_BOOKS[ch.id]:
            for e in books[key]:
                if e not in seen:
                    gaps.append(f"{ch.id}: ENTRY {e.lesson}#{e.index} "
                                f"{e.title} -- claimed by no problem")
    for line in gaps:
        print("  " + line)
    print(f"app_links: {claimed} of {total} entries linked, "
          f"{len(gaps)} loose end(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(_self_check())
