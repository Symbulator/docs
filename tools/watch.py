#!/usr/bin/env python3
"""
Rebuild whenever a source file changes, then refresh the static preview.

    python3 tools/watch.py            # web + preview only, the fast loop
    python3 tools/watch.py --pdf      # also rebuild the PDFs (much slower)

Leave it running in a terminal while you edit src/*.md; reload the browser tab
to see the change. Stop it with Ctrl-C.
"""
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WATCH = [os.path.join(ROOT, d) for d in ("src", "tex", "web")]
WATCH.append(os.path.join(ROOT, "book.yaml"))


def stamp():
    out = {}
    for target in WATCH:
        if os.path.isfile(target):
            out[target] = os.path.getmtime(target)
            continue
        for base, _dirs, files in os.walk(target):
            for f in files:
                p = os.path.join(base, f)
                out[p] = os.path.getmtime(p)
    return out


def rebuild(with_pdf):
    args = [sys.executable, "build.py"] + ([] if with_pdf else ["--web"])
    if subprocess.run(args, cwd=ROOT).returncode == 0:
        subprocess.run([sys.executable, "tools/static_preview.py"], cwd=ROOT)
    print(time.strftime("  waiting for changes  (%H:%M:%S)"))


if __name__ == "__main__":
    pdf = "--pdf" in sys.argv
    print("watching src/, tex/, web/ and book.yaml — Ctrl-C to stop")
    rebuild(pdf)
    last = stamp()
    try:
        while True:
            time.sleep(1)
            now = stamp()
            if now != last:
                last = now
                print("\nchange detected, rebuilding")
                rebuild(pdf)
    except KeyboardInterrupt:
        print("\nstopped")
