"""Rename value symbols that version 9 cannot read, inside v9 panels only.

`is` is a Python keyword and `re` is SymPy's real-part function, so a
circuit that uses either as a symbolic value fails to parse -- the same
collision that had `e` renamed to `e1`, but reached through a value rather
than an element name. The calculator has no such problem, so the fences for
versions 7 and 8 keep the original spelling and only the version 9 panels
move.

Each panel is solved after the rename; anything that still fails is left
alone and reported, because a panel that does not read for some other
reason is not something a rename fixes.

Usage:
    python tools/rename_v9_symbols.py            # report
    python tools/rename_v9_symbols.py --write    # apply
"""
import glob
import io
import os
import re
import sys

sys.path.insert(0, r"C:\Users\perez\Claude Code\Application\v9\repos\server")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import symbulator_ui as ui                                    # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
OPEN = re.compile(r"^```field 9 Circuit Description\s*$")

# Old spelling -> new. Applied as whole words inside a panel, so `re` does
# not touch `rrc` and `is` does not touch `is1`.
RENAMES = {"is": "is1", "re": "re1", "s": "s1"}


def apply(line: str) -> str:
    def sub(m):
        return RENAMES.get(m.group(0), m.group(0))
    return re.sub(r"(?<![\w])(" + "|".join(RENAMES) + r")(?![\w])", sub, line)


def reads(desc: str) -> bool:
    for domain, omega in (("dc", ""), ("ac", "1000"), ("tr", "")):
        try:
            if ui._validate(desc, domain, omega, None):
                continue
            r = ui.solve_ui(desc, domain, omega, None, "solve", "", "", "z",
                            [], [], [], digits=0, si=False, units=True)
            if r.get("ok"):
                return True
        except Exception:                                     # noqa: BLE001
            continue
    return False


def main():
    write = "--write" in sys.argv
    done = left = 0
    for path in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        name = os.path.basename(path)
        lines = io.open(path, encoding="utf-8").read().split("\n")
        changed = False
        i = 0
        while i < len(lines):
            if not OPEN.match(lines[i]):
                i += 1
                continue
            start, j = i + 1, i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            body = lines[start:j]
            desc = ":".join(b.strip() for b in body if b.strip())
            if desc and not reads(desc):
                new_body = [apply(b) for b in body]
                new_desc = ":".join(b.strip() for b in new_body if b.strip())
                if new_desc != desc and reads(new_desc):
                    done += 1
                    changed = True
                    print(f"  {name}:{start}")
                    print(f"      -  {desc[:92]}")
                    print(f"      +  {new_desc[:92]}")
                    lines[start:j] = new_body
                else:
                    left += 1
                    print(f"  {name}:{start}  still failing")
                    print(f"      {desc[:92]}")
            i = j + 1
        if changed and write:
            io.open(path, "w", encoding="utf-8",
                    newline="\n").write("\n".join(lines))
    print(f"\n{done} renamed, {left} still failing")
    if done and not write:
        print("dry run -- pass --write to apply")


if __name__ == "__main__":
    main()
