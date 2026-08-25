"""Import figures the 2023 archive holds under a slightly different name.

The source refers to `as7e1212`; the archive file is `as7ex1212.png`. One
"x", from the site's habit of abbreviating "example" two different ways.
`import_lesson_figures.py` matches by book-and-number code and never saw
these, so `make_placeholders.py` drew boxes over real artwork that was
sitting on disk the whole time.

Only exact and ex-variant matches are taken -- nothing fuzzier, because a
wrong figure is worse than a placeholder. A figure that is already real
(no placeholder marker) is never overwritten.

    python tools/import_variant_figures.py            # report
    python tools/import_variant_figures.py --write    # copy them in
"""
import glob
import io
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
ARCHIVE = (r"C:\Users\perez\OneDrive\_High Archive\_High Archive - Personal"
           r"\Documents\Roberto\Creaciones\Symbulator\Websites"
           r"\2023 Website")


# The site abbreviates the *kind* of figure two ways, and the source and
# the files do not always agree on which. `as7e1212` is `as7ex1212.png`,
# `as7f1333` is `as7fi1333.png`, `as7p1175` is `as7pr1175.png`. The book
# code and the number are always the same; only these two letters move.
_KINDS = [("e", "ex"), ("f", "fi"), ("p", "pr"), ("d", "de")]
_CODE_RE = re.compile(r"^([a-z]+\d*?)([a-z]+)(\d{3,}[a-z]?)$")


def _variant(key):
    """The same figure code with the other spelling of its kind letter."""
    m = _CODE_RE.match(key)
    if not m:
        return key
    book, kind, number = m.groups()
    for short, long in _KINDS:
        if kind == short:
            return f"{book}{long}{number}"
        if kind == long:
            return f"{book}{short}{number}"
    return key


def archive_index():
    """stem (lowercased) -> full path, for every figure in the archive."""
    out = {}
    for sub in ("circuit", "practice"):
        folder = os.path.join(ARCHIVE, sub)
        if not os.path.isdir(folder):
            continue
        for name in os.listdir(folder):
            stem, ext = os.path.splitext(name)
            if ext.lower() in (".png", ".jpg", ".jpeg", ".gif"):
                out.setdefault(stem.lower(), os.path.join(folder, name))
    return out


def is_placeholder(path):
    if not os.path.isfile(path):
        return True
    head = io.open(path, encoding="utf-8", errors="replace").read(1500)
    return "placeholder" in head.lower() or "to be supplied" in head.lower()


def referenced():
    """(folder, stem, extension) for every figure the source refers to."""
    out = set()
    for path in glob.glob(os.path.join(SRC, "*.md")):
        text = io.open(path, encoding="utf-8").read()
        for m in re.finditer(r"assets/(circuit|practice)/([^\s\)]+)", text):
            stem, ext = os.path.splitext(m.group(2))
            out.add((m.group(1), stem, ext))
    return sorted(out)


def main():
    write = "--write" in sys.argv
    index = archive_index()
    taken = missing = already = 0
    rewrites = []

    for folder, stem, ext in referenced():
        svg = os.path.join(ROOT, "assets", folder, stem + ".svg")
        raster = os.path.join(ROOT, "assets", folder, stem + ext)
        # Real artwork already in place? Leave it.
        if os.path.isfile(raster) and not is_placeholder(raster):
            already += 1
            continue
        if not is_placeholder(svg):
            already += 1
            continue

        key = stem.lower()
        source = index.get(key) or index.get(_variant(key))
        if source is None:
            missing += 1
            continue

        got_ext = os.path.splitext(source)[1].lower()
        dest = os.path.join(ROOT, "assets", folder, stem + got_ext)
        taken += 1
        print(f"  {folder}/{stem}{ext:<6} <- {os.path.basename(source)}")
        if got_ext != ext.lower():
            rewrites.append((f"assets/{folder}/{stem}{ext}",
                             f"assets/{folder}/{stem}{got_ext}"))
        if write:
            shutil.copyfile(source, dest)
            # The placeholder pair would otherwise still be found first.
            for stale in (svg, os.path.splitext(svg)[0] + ".pdf"):
                if os.path.isfile(stale) and is_placeholder(stale):
                    os.remove(stale)

    if rewrites and write:
        for path in glob.glob(os.path.join(SRC, "*.md")):
            text = io.open(path, encoding="utf-8").read()
            new = text
            for old_ref, new_ref in rewrites:
                new = new.replace(old_ref, new_ref)
            if new != text:
                io.open(path, "w", encoding="utf-8",
                        newline="\n").write(new)

    print(f"\n{taken} imported, {already} already real, {missing} not in "
          f"the archive")
    if rewrites:
        print(f"{len(rewrites)} reference(s) needed a different extension")
    if taken and not write:
        print("dry run -- pass --write to copy them in")


main()
