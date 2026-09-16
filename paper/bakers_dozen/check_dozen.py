"""Check A Baker's Dozen against the app, before trusting or rebuilding it.

    py paper\\bakers_dozen\\check_dozen.py

Two things can go stale without anyone touching this folder, and this
catches both:

1. **An entry moves.** build_dozen.py names each run by book and position
   (`Lesson_06d`, 19). Insert an entry above it in the .cir and the booklet
   silently prints a different circuit and links to the wrong problem.
   EXPECT below pins each position to its title, and a mismatch fails.
2. **An answer changes.** The booklet's answers are hand-set LaTeX. This
   posts every run through the real app (the same path
   repos/server/tools/verify_lesson.py uses) and prints the app's answers
   for the names in WATCH, for a person to read beside the booklet. It
   does not compare automatically, because the booklet writes answers in
   its own form (polar, factored, with the roots restored).

Exits 1 if an entry moved or a run no longer solves.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(os.path.dirname(HERE))
SERVER = os.path.join(os.path.dirname(DOCS), "Application", "v9", "repos",
                      "server")

# (book, position) -> the entry's title as the .cir has it.
EXPECT = {
    ("Alexander_Sadiku", 2): "AS7's Example 3.4 (DC)",
    ("Nilsson_Riedel", 14): "NR12's Example 5.7 (DC)",
    ("Lesson_05b", 14): "Bo2's Example 3.3 (Cascade)",
    ("Lesson_07", 6): "AS7's Problem 9.73",
    ("Lesson_07", 10): "AS7's Example 10.14 (Dependent source)",
    ("Lesson_09", 6): "AS7's Example 12.11 (wye-delta with line impedances)",
    ("Alexander_Sadiku", 48): "AS7's Practice Problem 13.13 (AC)",
    ("Lesson_10", 17): "NR11's capacitor shorted by a switch, coupled 0.8 H and 1.6 H coils (DC, t < 0)",
    ("Lesson_10", 18): "NR11's capacitor shorted by a switch, coupled 0.8 H and 1.6 H coils (TR, t > 0)",
    ("Lesson_06d", 7): "Bo2's Drill Exercise 6.6 (Op Amp, DC)",
    ("Lesson_06d", 8): "Bo2's Drill Exercise 6.6 (Op Amp, TR)",
    ("Lesson_06d", 18): "A more complex problem (DC)",
    ("Lesson_06d", 19): "A more complex problem (TR)",
    ("Lesson_13", 14): "AS7's Problem 19.2",
    ("Nilsson_Riedel", 16): "NR12's Example 18.6 (DC)",
    ("Lesson_03", 49): "The Showing-off Problem (Expert)",
}

# (book, position) -> the answer names the booklet prints for that run.
WATCH = {
    ("Alexander_Sadiku", 2): ["v1", "v2", "v3", "v4"],
    ("Nilsson_Riedel", 14): ["v3"],
    ("Lesson_05b", 14): ["vo"],
    ("Lesson_07", 6): ["zeq"],
    ("Lesson_07", 10): ["v1", "v2"],
    ("Lesson_09", 6): ["iraa", "irac"],
    ("Alexander_Sadiku", 48): ["ir8"],
    ("Lesson_10", 17): ["il1", "il2"],
    ("Lesson_10", 18): [],
    ("Lesson_06d", 7): ["vca", "vcb"],
    ("Lesson_06d", 8): ["vo"],
    ("Lesson_06d", 18): ["vca", "vcb"],
    ("Lesson_06d", 19): ["v1", "v2"],
    ("Lesson_13", 14): ["z11", "z12", "z21", "z22"],
    ("Nilsson_Riedel", 16): ["vc"],
    ("Lesson_03", 49): ["vs", "is", "ir5"],
}


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.path.insert(0, HERE)
    sys.path.insert(0, SERVER)
    sys.path.insert(0, os.path.join(SERVER, "tools"))
    import build_dozen
    import circuitbook
    import app as flask_app
    from verify_lesson import rounding_args, shown_answers

    runs = [(p["title"], r) for p in build_dozen.P + [build_dozen.BONUS]
            for r in p["runs"]]
    used = {(r[1], r[2]) for _, r in runs}
    if used != set(EXPECT):
        print("EXPECT does not list exactly the runs build_dozen.py uses:")
        print("  missing:", sorted(used - set(EXPECT)))
        print("  extra:  ", sorted(set(EXPECT) - used))
        return 1

    client = flask_app.app.test_client()
    books, bad = {}, 0
    for title, (label, book, n, _key, _settings, printed) in runs:
        if book not in books:
            text = io.open(os.path.join(SERVER, "examples", book + ".cir"),
                           encoding="utf-8").read()
            books[book] = circuitbook.parse_book(text)[0]
        e = books[book][n - 1]
        print(f"\n== {title} | {label} | {book} #{n}")
        # The app keeps only the first MAX_NAME_LEN characters of a title,
        # so compare the way it reads the file.
        want = EXPECT[(book, n)].strip()[:circuitbook.MAX_NAME_LEN]
        if e["name"] != want:
            print(f"   ** ENTRY MOVED: #{n} is now {e['name']!r}")
            bad += 1
            continue
        payload = {
            "desc": e["desc"], "domain": e.get("domain", "dc"),
            "omega": e.get("omega", ""), "tool": e.get("tool") or "solve",
            "n1": e.get("n1", ""), "n2": e.get("n2", ""),
            "kind": e.get("kind", "z"), "si": bool(e.get("si")),
            "units": bool(e.get("units", True)),
            "use_rms": bool(e.get("rms")), "polar": bool(e.get("polar")),
            "equations": e.get("equations", []),
            "unknowns": e.get("unknowns", ""),
            "conditions": e.get("conditions", []),
            "variables": ([v.strip() for v in str(e.get("vars", "")).split(",")
                           if v.strip()] or None),
        }
        payload.update(rounding_args(e))
        r = client.post("/api/solve", json=payload).get_json()
        if not r.get("ok"):
            print(f"   ** DOES NOT SOLVE: {r.get('error')}")
            bad += 1
            continue
        shown = shown_answers(r)
        for name in WATCH[(book, n)]:
            print(f"   app  {name} = {shown.get(name, '(not among the answers)')}")
        if e.get("evaluate"):
            ev = client.post("/api/evaluate", json={
                "expr": e["evaluate"], "values": r.get("values") or {},
                "domain": e.get("domain", "dc"),
                "conditions": e.get("evaluate_conditions", []),
                **rounding_args(e), "si": bool(e.get("si")),
                "units": bool(e.get("units", True))}).get_json()
            print(f"   app  evaluate {e['evaluate']} = "
                  f"{ev.get('plain') or ev.get('error')}")
        for line in printed:
            print(f"   book {line}")
    print(f"\n{bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
