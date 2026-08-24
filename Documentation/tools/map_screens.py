"""Where each 2023 screen grab sat, so it can be placed in the new source.

The old site is one long HTML page per version. Each <img src="screen/7/..">
sits inside the prose that introduces it, so the sentence just before the
image is the anchor: find that sentence in src/*.md and the screen belongs
there. Reports only -- it does not edit.
"""
import html
import io
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ARCHIVE = Path(r"C:\Users\perez\OneDrive\_High Archive"
               r"\_High Archive - Personal\Documents\Roberto\Creaciones"
               r"\Symbulator\Websites\2023 Website")
SRC = Path(__file__).resolve().parent.parent / "src"

TAG = re.compile(r"<[^>]+>")


def text_of(fragment: str) -> str:
    """Visible text of an HTML fragment, whitespace collapsed."""
    t = html.unescape(TAG.sub(" ", fragment))
    return re.sub(r"\s+", " ", t).strip()


def anchors(page: Path, version: str):
    """(image, preceding text, following text) for every screen grab."""
    doc = io.open(page, encoding="utf-8", errors="replace").read()
    out = []
    pat = r'<img[^>]*src="[^"]*?(screen/%s/[^"]+)"[^>]*>' % version
    for m in re.finditer(pat, doc):
        before = text_of(doc[max(0, m.start() - 1200):m.start()])
        after = text_of(doc[m.end():m.end() + 400])
        cap = re.search(r'title="([^"]*)"', m.group(0))
        out.append((m.group(1), before[-220:],
                    cap.group(1) if cap else ""))
    return out


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else "7"
    page = ARCHIVE / f"docs-page{version}.html"
    if not page.is_file():
        sys.exit(f"not found: {page}")

    bodies = {p.name: io.open(p, encoding="utf-8").read() for p in
              sorted(SRC.glob("*.md"))}

    found = missing = 0
    for img, before, caption in anchors(page, version):
        # The last few words before the image are the most specific thing
        # to search for; back off to shorter phrases if the longest misses.
        hit = None
        words = before.split()
        for n in (14, 10, 7, 5):
            if len(words) < n:
                continue
            phrase = " ".join(words[-n:])
            key = (chr(92) + 's+').join(re.escape(w) for w in phrase.split())
            for name, body in bodies.items():
                if re.search(key, body, re.I):
                    hit = (name, n)
                    break
            if hit:
                break
        exists = (ARCHIVE / img).is_file()
        if hit:
            found += 1
            print(f"  {img:30} -> {hit[0]:26} | {caption[:40]}"
                  f"{'' if exists else '  MISSING'}")
        else:
            missing += 1
            print(f"  {img:32} -> ?  ...{before[-90:]!r}"
                  f"{'' if exists else '   FILE MISSING'}")
    print(f"\nversion {version}: {found} located, {missing} unplaced")


main()
