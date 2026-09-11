"""The back-of-book index is sound, in the source and in the build (#422).

An `{{i:term}}` marker is invisible on the page, so nothing a reader sees
says whether the index behind it is right. Four things go wrong with one,
and until 12 Sep 2026 nothing checked any of them:

* **a marker in the wrong place.** Inside a code fence it renders as text;
  in a heading, a table cell or a directive line it breaks the block or
  leaks into the sidebar. The source is scanned line by line for those.
* **a dangling target.** `toc.json` says `lesson-dc#ix-resistor-0`; the
  built page must carry `id="ix-resistor-0"`. A rename of the slugifier, a
  chapter dropped from a version, or a marker inside a span the version
  does not render all leave a number on the index page that opens the
  chapter at its top. Checked against the built HTML whenever a build is
  present, like check_search().
* **a term in the wrong vocabulary.** Version 9's index once offered *th
  script*, a thing version 9 does not have (#409). No version 9 term may
  contain the words *script*, *command* or *program*, on word boundaries --
  "circuit de**script**ion" is fine.
* **too many locations.** A term with nine numbers beside it is a term
  nobody follows. The cap is four: the place a thing is taught, the place
  it is stated precisely, a note that goes deeper, and one more.

It also asserts coverage: version 9 has three books and the index must
reach into all of them, so zero entries in the Manual or the Notes fails.
Two more rules: a term may not contain the characters makeindex treats as
commands (`! @ | "`), since the same markers feed the PDF's index; and
within one version two different terms may not claim the same anchor --
"expert mode" and "Expert Mode" slugify alike, and are legitimate only
because one lives in a 7,8 block and the other in a 9 block.

Proved red on 12 Sep 2026 by each route in turn, the tree restored and
re-checked clean after each: an anchor deleted from a built page; a
`{{i:th script}}` planted in an `::: only 9` block; a fifth location added
to a capped term; a marker put in a heading; `{{i:expert mode}}` planted
beside `{{i:Expert Mode}}` in one version 9 block, caught both as a shared
spot in toc.json and as a doubled id in the page; and a `!` in a term.
The first attempt at the shared-anchor sabotage stayed green -- it planted
the twin in a *different chapter* from the original's first occurrence, so
nothing collided anywhere and the guard was right. The doubled-id check
came out of that: the id on the page is what the browser resolves, so it
is the artefact to measure.
"""
import glob
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
BUILD = os.path.join(ROOT, "build", "web", "content")

#: Locations per term, per version. Four is one more than the three the
#: rule of thumb allows (taught / stated / deepened), for the handful of
#: terms -- SI prefixes, dependent sources -- that are genuinely explained
#: in a Course lesson, a Manual part and two Notes.
CAP = 4

#: Version 9 has an app, not scripts. #409 is what happens otherwise.
CALCULATOR_WORDS = re.compile(r"\b(script|command|program)s?\b", re.I)

#: makeindex's special characters. A term is also a `\index{}` entry.
BAD_CHARS = set('!@|"')

MARKER = re.compile(r"\{\{i:([^{}]*)\}\}")


def shelf_of(chapter: dict) -> str:
    """Mirror of index.php's shelf_of(): the book a chapter sits on."""
    if chapter.get("book", "course") == "manual":
        return "manual"
    if chapter.get("kind") == "note":
        return "notes"
    return "course"


def check_index_source(slugify) -> list[str]:
    out = []
    for path in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        name = os.path.basename(path)
        fence = False
        for no, line in enumerate(io.open(path, encoding="utf-8"), 1):
            s = line.strip()
            if s.startswith("```"):
                fence = not fence
                if "{{i:" in s:
                    out.append(f"index: {name}:{no}: marker on a code fence line")
                continue
            if "{{i:" not in line:
                continue
            where = None
            if fence:
                where = "inside a code fence (it would render as text)"
            elif s.startswith("#"):
                where = "in a heading (it would leak into the sidebar and the TeX title)"
            elif s.startswith("|"):
                where = "in a table row (it would break the table)"
            elif s.startswith(":::"):
                where = "on a directive line (it would become part of the title)"
            if where:
                out.append(f"index: {name}:{no}: {{{{i:}}}} marker {where}")
            for term in MARKER.findall(line):
                if term != term.strip() or not term.strip():
                    out.append(f"index: {name}:{no}: term {term!r} is empty or "
                               f"has stray whitespace")
                    continue
                bad = sorted(set(term) & BAD_CHARS)
                if bad:
                    out.append(f"index: {name}:{no}: term {term!r} contains "
                               f"{''.join(bad)}, which makeindex reads as a command")
    return out


def check_index_build(versions) -> list[str]:
    out = []
    for v in versions:
        vdir = os.path.join(BUILD, f"v{v}")
        toc_path = os.path.join(vdir, "toc.json")
        if not os.path.isfile(toc_path):
            continue                      # nothing built yet; nothing to check
        toc = json.load(io.open(toc_path, encoding="utf-8"))
        index = toc.get("index", {})
        chapters = {c["id"]: c for c in toc["chapters"]}
        present = {cid for cid, c in chapters.items() if c.get("present")}
        html: dict[str, str] = {}
        reached: dict[str, set] = {}
        owner: dict[str, str] = {}        # anchor -> the term that claimed it
        locations = 0
        for term, spots in index.items():
            locations += len(spots)
            for spot in spots:
                # Two terms that slugify alike -- "expert mode" and "Expert
                # Mode" -- take the same ids and only one target survives.
                # Per version, because the pair above is legitimate when
                # one lives in a 7,8 block and the other in a 9 block.
                first = owner.setdefault(spot, term)
                if first != term:
                    out.append(f"index: v{v} terms {first!r} and {term!r} share "
                               f"the anchor {spot}; only one can be reached")
            if len(spots) > CAP:
                out.append(f"index: v{v} term {term!r} has {len(spots)} locations; "
                           f"the cap is {CAP} -- keep the best, drop the rest")
            if v == 9 and CALCULATOR_WORDS.search(term):
                out.append(f"index: v9 term {term!r} names a calculator tool "
                           f"(#409); version 9 has an app, not scripts")
            for spot in spots:
                cid, _, anchor = spot.partition("#")
                if cid not in present:
                    out.append(f"index: v{v} term {term!r} points at {cid}, "
                               f"which this version does not have")
                    continue
                if cid not in html:
                    page = os.path.join(vdir, cid + ".html")
                    html[cid] = (io.open(page, encoding="utf-8").read()
                                 if os.path.isfile(page) else "")
                hits = html[cid].count(f'id="{anchor}"')
                if hits == 0:
                    out.append(f"index: v{v} term {term!r} -> {spot} is dangling: "
                               f"no id=\"{anchor}\" in the built page")
                elif hits > 1:
                    # The artefact-level form of the shared-anchor rule: two
                    # terms that slugify alike on one page write the same id
                    # twice, and the browser scrolls to whichever came first.
                    out.append(f"index: v{v} {spot} carries id=\"{anchor}\" "
                               f"{hits} times; two terms slugify alike on that page")
                reached.setdefault(shelf_of(chapters[cid]), set()).add(term)
        census = ", ".join(f"{sh} {len(ts)}" for sh, ts in sorted(reached.items()))
        print(f"index: v{v}: {len(index)} terms, {locations} locations ({census})")
        if v == 9:
            for sh in ("course", "manual", "notes"):
                if not reached.get(sh):
                    out.append(f"index: v9 has no entry in the {sh} -- "
                               f"three books, and the index reaches one short")
    return out


def check_index(versions, slugify) -> list[str]:
    return check_index_source(slugify) + check_index_build(versions)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ROOT)
    from build import slugify as _slugify
    problems = check_index([7, 8, 9], _slugify)
    for p in problems:
        print("  " + p)
    print("index check: " + (f"{len(problems)} problem(s)" if problems else "ok"))
    sys.exit(1 if problems else 0)
