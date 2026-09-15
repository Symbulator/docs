r"""Every ribbon branch of web/index.php, executed against a real PHP server.

#421 (12 Sep 2026) put PHP on Roberto's laptop, so `index.php` can finally
be *run* rather than read. Until then this file was reviewed by eye, which
let three real bugs through in a single evening -- a variable used before
it was defined, a null dereference on a shelf page, and a sidebar that
duplicated the grid beside it. Any of the three would have been a fatal or
a blank page on the first request here.

What it asserts, per page: whether the ribbon offers *Download as PDF* and
which PDF, whether it offers *Split View* and on what page, whether
versions 7 and 8 still carry *How it works*, and what the property mark
says in each of its spellings.

    #420: a page belonging to no book offers neither link -- version 9's
    home page (the chooser) and the Technical Notes shelf (whose notes are
    printed inside symbulator-v9.pdf rather than a book of their own).

NOT wired into `build.py --check`, deliberately: that has to keep running
on a machine with no PHP. Run it before a deploy that touched the ribbon.

    py tools\check_ribbon.py                  # starts its own server
    py tools\check_ribbon.py --base http://127.0.0.1:8099/index.php

It builds nothing. Point it at a `build/web` that is current, or run
`py build.py --web` first -- testing yesterday's build is the one way this
check can pass and still be wrong.
"""
import argparse
import os
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(HERE)
BUILT = os.path.join(DOCS, "build", "web")

# winget drops php.exe here and does not put it on the PATH this session
# sees; look there before giving up, and say so plainly if it is absent.
WINGET_PHP = os.path.join(
    os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages",
    "PHP.PHP.8.4_Microsoft.Winget.Source_8wekyb3d8bbwe", "php.exe")

# page,                         PDF it should offer,      Split View target
CASES = [
    ("?v=9",                    None,                     None),
    ("?v=9&p=course",           "/symbulator-v9.pdf",     "/split/?page=course"),
    ("?v=9&p=manual",           "/symbulator-manual.pdf", "/split/?page=manual"),
    ("?v=9&p=notes",            None,                     None),
    ("?v=9&p=samplers",         None,                     None),
    ("?v=9&p=as7-sampler",      "/symbulator-as7-sampler.pdf",
     "/split/?page=as7-sampler"),
    ("?v=9&p=lesson-dc",        "/symbulator-v9.pdf",     "/split/?page=lesson-dc"),
    ("?v=9&p=manual-orientation", "/symbulator-manual.pdf",
     "/split/?page=manual-orientation"),
    ("?v=9&p=si-prefixes",      "/symbulator-v9.pdf",     "/split/?page=si-prefixes"),
    ("?v=7",                    "/symbulator-v7.pdf",     None),
    ("?v=7&p=lesson-dc",        "/symbulator-v7.pdf",     None),
    ("?v=8",                    "/symbulator-v8.pdf",     None),
]


def find_php():
    return shutil.which("php") or (os.path.isfile(WINGET_PHP) and WINGET_PHP)


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def ribbon(html):
    i = html.find("subbar-inner")
    nav = html[i:html.find("</nav>", i)]
    return dict(re.findall(r'<a href="([^"]+)"[^>]*>([^<]+)</a>', nav))


def mark(html):
    m = re.search(r'property-mark-top">(.*?)</span>\s*$', html, re.M | re.S)
    if not m:
        m = re.search(r'property-mark-top">(.*?)</span>', html, re.S)
    raw = m.group(1) if m else "?"
    lon = re.search(r'mark-long">([^<]*)<', raw)
    sho = re.search(r'mark-short">([^<]*)<', raw)
    if lon or sho:
        return "%s / %s" % (lon.group(1) if lon else "-",
                            sho.group(1) if sho else "-")
    return re.sub(r"<[^>]+>", "", raw).strip()


def run(base):
    bad = 0
    print("%-30s %-24s %-32s %s"
          % ("page", "PDF", "third link", "property mark"))
    print("-" * 106)
    for q, want_pdf, want_split in CASES:
        html = urllib.request.urlopen(base + q, timeout=30).read().decode(
            "utf-8", "replace")
        r = ribbon(html)
        pdf = next((u for u, t in r.items()
                    if t.strip() == "Download as PDF"), None)
        split = next((u for u, t in r.items() if t.strip() == "Split View"), None)
        how = next((u for u, t in r.items() if t.strip() == "How it works"), None)

        ok = pdf == want_pdf and split == want_split
        if q.startswith(("?v=7", "?v=8")):
            ok = ok and how is not None      # 7 and 8 keep their own link
        bad += not ok
        print("%s%-29s %-24s %-32s %s"
              % ("  " if ok else "**", q, pdf or "(none)",
                 split or (("How it works") if how else "(none)"), mark(html)))
    print()
    print("check_ribbon: %s (%d of %d)"
          % ("clean" if not bad else "%d FAILED" % bad,
             len(CASES) - bad, len(CASES)))
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", help="an index.php already being served")
    a = ap.parse_args()

    if a.base:
        return run(a.base)

    php = find_php()
    if not php:
        print("check_ribbon: no php found -- skipped.\n"
              "  winget install --id PHP.PHP.8.4 --exact --source winget\n"
              "  (winget does not add it to PATH for the current session)")
        return 0
    if not os.path.isfile(os.path.join(BUILT, "index.php")):
        print("check_ribbon: %s has no index.php -- run `py build.py --web`"
              % BUILT)
        return 1

    port = free_port()
    srv = subprocess.Popen([php, "-S", "127.0.0.1:%d" % port, "-t", BUILT],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    try:
        base = "http://127.0.0.1:%d/index.php" % port
        for _ in range(60):                      # wait for it to answer
            try:
                urllib.request.urlopen(base + "?v=9", timeout=2).read()
                break
            except Exception:
                time.sleep(0.25)
        else:
            print("check_ribbon: server never answered on port %d" % port)
            return 1
        return run(base)
    finally:
        srv.terminate()


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
