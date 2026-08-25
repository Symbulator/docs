"""Content stamps on the landing page's stylesheet links.

symbulator.com serves its stylesheets with `Cache-Control: max-age=604800`,
so a returning visitor keeps a stylesheet for a week no matter what is
deployed over it. On 24 Aug 2026 the banner gained the rule that stops the
wordmark rendering as an underlined blue anchor; on 25 Aug a phone that had
visited before still showed the underlined version, because it never asked
for the file again. The deploy was correct and invisible.

A query string fixes it: `/assets/banner.css?v=a1b2c3d4` is a different URL
to the cache, so changing the stamp forces exactly one refetch and nothing
else. The stamp is the first 8 hex of the file's SHA-256, so it changes when
and only when the file does.

The learn site does not need this -- `web/index.php` stamps itself at request
time with filemtime(). Only the landing page, which has no build step and so
nothing that could do it for it.

    python tools/stamp_assets.py           # rewrite the stamps
    python tools/stamp_assets.py --check   # complain if any is stale
"""
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "landing", "index.html")

#: Only local stylesheets. The Google Fonts link is someone else's URL and
#: carries its own caching; appending to it would just break the request.
_LINK = re.compile(r'(<link rel="stylesheet" href="/assets/)([\w.-]+\.css)(\?v=[0-9a-f]+)?(")')


def stamp(name: str) -> str:
    """The first 8 hex of a stylesheet's SHA-256."""
    path = os.path.join(ROOT, "landing", "assets", name)
    data = io.open(path, "rb").read()
    return hashlib.sha256(data).hexdigest()[:8]


def apply(check_only: bool = False) -> list[str]:
    text = io.open(PAGE, encoding="utf-8").read()
    stale: list[str] = []

    def sub(m):
        name, had = m.group(2), (m.group(3) or "")
        want = "?v=" + stamp(name)
        if had != want:
            stale.append(f"landing/index.html: {name} is stamped "
                         f"{had or '(not at all)'}, should be {want}")
        return m.group(1) + name + want + m.group(4)

    out = _LINK.sub(sub, text)
    if not _LINK.search(text):
        return ["landing/index.html: no local stylesheet links found -- "
                "stamp_assets.py needs updating to match the markup"]
    if stale and not check_only:
        io.open(PAGE, "w", encoding="utf-8", newline="\n").write(out)
        for s in stale:
            print("  stamped:", s.split(": ", 1)[1])
        return []
    return stale


def check_asset_stamps() -> list[str]:
    """For build.py --check: the landing stamps match the files on disk."""
    return [s + " -- run python tools/stamp_assets.py" for s in apply(True)]


if __name__ == "__main__":
    problems = apply("--check" in sys.argv)
    for p in problems:
        print("  " + p)
    if problems:
        sys.exit(1)
    print("stylesheet stamps are current")
