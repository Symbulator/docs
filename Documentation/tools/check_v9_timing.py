"""Every version 9 circuit panel, through the app's own timeout.

check_v9_panels.py calls the solver directly, which has no time limit --
so a panel that takes 94 seconds passes there and fails for every reader,
because the web app kills a solve at 25. Two of chapter 9's panels were
in exactly that state and the other checker said they were fine.

This runs each panel the way a reader meets it: through the Flask route,
with the same timeout, and reports anything slow enough to be worth
knowing about even when it does finish.

    python tools/check_v9_timing.py            # every panel
    python tools/check_v9_timing.py 09         # just files matching "09"
"""
import glob
import io
import os
import re
import sys
import time

sys.path.insert(0, r"C:\Users\perez\Claude Code\Symbulator\repos\server")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import app as flask_app                                      # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
OPEN = re.compile(r"^```field 9 Circuit Description\s*$")

#: Slower than this and a reader notices, even though it still works.
SLOW = 5.0


def panels(path):
    lines = io.open(path, encoding="utf-8").read().split("\n")
    i = 0
    while i < len(lines):
        if OPEN.match(lines[i]):
            body, j = [], i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                body.append(lines[j])
                j += 1
            yield i + 1, ":".join(b.strip() for b in body if b.strip())
            i = j
        i += 1


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else ""
    client = flask_app.app.test_client()
    slow = failed = ok = 0

    for path in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        name = os.path.basename(path)
        if want and want not in name:
            continue
        for line, desc in panels(path):
            if not desc or ":" not in desc:
                continue
            # The panel does not say which analysis; try each in turn and
            # keep the first that answers, as the other checker does.
            best, verdict = None, None
            # Try the likeliest domain first, and never stop at a timeout
            # in the wrong one: a DC solve of an AC circuit can itself run
            # past the limit, which made every panel here look broken.
            order = [("ac", "1"), ("dc", ""), ("tr", ""), ("fd", "")]
            if not re.search(r"\d[jJ]|∠", desc):
                order = [("dc", ""), ("ac", "1"), ("tr", ""), ("fd", "")]
            for domain, omega in order:
                t0 = time.time()
                r = client.post("/api/solve", json={
                    "desc": desc, "domain": domain, "omega": omega,
                    "tool": "solve", "digits": 4, "si": False,
                    "units": False})
                elapsed = time.time() - t0
                if r.status_code == 200:
                    best, verdict = elapsed, domain
                    break
                payload = r.get_json(silent=True) or {}
                if "longer than" in str(payload.get("error", "")):
                    # Remember it, but keep trying: another domain may be
                    # the one this panel is actually for.
                    if verdict is None:
                        best, verdict = elapsed, "TIMEOUT"
                    continue
            if verdict == "TIMEOUT":
                failed += 1
                print(f"  TIMED OUT  {name}:{line}  ({best:.0f} s)")
                print(f"             {desc[:92]}")
            elif best is None:
                ok += 1          # refused for a reason check_v9_panels covers
            elif best > SLOW:
                slow += 1
                print(f"  slow       {name}:{line}  {best:.1f} s "
                      f"({verdict})")
                print(f"             {desc[:92]}")
            else:
                ok += 1

    print(f"\n{ok} answered promptly, {slow} slow (over {SLOW:.0f} s), "
          f"{failed} timed out")


if __name__ == "__main__":
    # The app solves in a child process; without this guard every child
    # re-imports and re-runs this script.
    main()
