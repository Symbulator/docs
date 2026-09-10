"""Pull each numbered problem out of the completed English Book.

The Book (Documentation/paper/book/ch*.tex) is the Burkett-Hutcheson
translation of the 2001 thesis, finished in 2026. It carries a
\\problem{NNN} marker per problem -- 89 of them, matching Appendix D of
the thesis exactly -- so problem boundaries are read, not inferred.
"""
import glob
import io
import os
import re

BOOK = r"C:\Users\perez\Claude Symbulator\Documentation\paper\book"

PROBLEM = re.compile(r"\\problem\{(\d{3})\}")
STATEMENT = re.compile(r"\\emph\{Problem:\s*(.*?)\}\s*\n\s*\n", re.S)
ENTRY = re.compile(r"\\begin\{entry\}\s*(.*?)\s*\\end\{entry\}", re.S)
# sq\tool( ... ) -- the description is the first quoted string
SQ = re.compile(r"sq\\(\w+)\((.*)\)\s*$", re.S)
QUOTED = re.compile(r'"([^"]*)"')
#: `value -> name` on the calculator's STO key, as the Book prints it.
STORE = re.compile(r"([^:;\s]+?)\s*\u2192\s*([A-Za-z]\w*)")


def chapters():
    for p in sorted(glob.glob(os.path.join(BOOK, "ch*.tex")) + glob.glob(os.path.join(BOOK, "backmatter.tex"))):
        yield os.path.basename(p), io.open(p, encoding="utf-8").read()


def parse():
    """[{num, chapter, statement, entries:[str], netlists:[(tool, desc, rest)]}]"""
    out = []
    for name, text in chapters():
        marks = list(PROBLEM.finditer(text))
        for k, m in enumerate(marks):
            start = m.end()
            end = marks[k + 1].start() if k + 1 < len(marks) else len(text)
            body = text[start:end]

            st = STATEMENT.search(body)
            statement = " ".join(st.group(1).split()) if st else ""

            entries = [" ".join(e.split()) for e in ENTRY.findall(body)]
            stores = {}
            for e in entries:
                # `var`, not `name`: `name` is the chapter filename in the
                # enclosing loop, and shadowing it made every problem after
                # the first store report its chapter as "zp22".
                for value, var in STORE.findall(e):
                    stores.setdefault(var, value)
            nets = []
            for e in entries:
                sq = SQ.search(e)
                if not sq:
                    continue
                tool, args = sq.group(1), sq.group(2)
                q = QUOTED.search(args)
                if not q:
                    nets.append((tool, "", args))
                    continue
                desc = q.group(1)
                rest = args[q.end():].lstrip(", ").strip()
                nets.append((tool, desc, rest))

            out.append(dict(num=m.group(1), chapter=name, statement=statement,
                            entries=entries, netlists=nets, body=body,
                            stores=stores))
    return out


if __name__ == "__main__":
    probs = parse()
    print("problems:", len(probs))
    no_stmt = [p["num"] for p in probs if not p["statement"]]
    no_net = [p["num"] for p in probs if not p["netlists"]]
    print("without a statement:", len(no_stmt), no_stmt[:20])
    print("without a netlist:  ", len(no_net), no_net[:20])
    print()
    for p in probs[:3]:
        print(f"--- {p['num']} ({p['chapter']}) ---")
        print("   ", p["statement"][:90])
        for tool, desc, rest in p["netlists"]:
            print(f"    sq\\{tool}  desc={desc[:70]!r}  rest={rest[:30]!r}")
