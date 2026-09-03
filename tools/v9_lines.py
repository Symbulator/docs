"""List lines visible in version 9 that match a regex.
usage: py tools/v9_lines.py REGEX [--para] [files...]
--para prints the whole paragraph around each hit plus the nearest preceding
'answers you want' line, for rewriting bracket answers."""
import re, sys, glob
args = sys.argv[1:]
para = "--para" in args
args = [a for a in args if a != "--para"]
pat = re.compile(args[0])
files = args[1:] or sorted(glob.glob("src/*.md"))
SPAN78 = re.compile(r"\{\{v[78](?:,[78])?\|.*?\}\}")
SPAN9 = re.compile(r"\{\{v9\|(.*?)\}\}")
def visible_lines(f):
    stack, fence, out = [], None, []
    lines = open(f, encoding="utf-8").read().split("\n")
    for n, raw in enumerate(lines, 1):
        if raw.startswith("```"):
            if fence is None:
                info = raw[3:].split()
                fence = ("9" in info[1].split(",")) if (info and info[0] in ("sym","out","field") and len(info) > 1) else True
            else:
                fence = None
            continue
        if fence is not None:
            vis = fence and all(stack)
        else:
            m = re.match(r"^:::\s*(\w+)?\s*(.*)$", raw)
            if m:
                name, arg = m.group(1), m.group(2).strip()
                if name is None:
                    if stack: stack.pop()
                elif name == "only": stack.append("9" in arg.split(","))
                elif name == "not": stack.append("9" not in arg.split(","))
                else: stack.append(True)
                continue
            vis = all(stack)
        out.append((n, raw, vis, fence is not None))
    return out
for f in files:
    vl = visible_lines(f)
    idx = {n: i for i, (n, *_ ) in enumerate(vl)}
    for i, (n, raw, vis, infence) in enumerate(vl):
        if not vis: continue
        shown = SPAN9.sub(r"\1", SPAN78.sub("", raw))
        if not pat.search(shown): continue
        if not para:
            print(f"{f}:{n}: {shown}"); continue
        want = ""
        for j in range(i-1, max(-1, i-25), -1):
            if re.search(r"you want|Ask \*\*Evaluate", vl[j][1]):
                want = vl[j][1]; break
        a = i
        while a > 0 and vl[a-1][1].strip() and not vl[a-1][3]: a -= 1
        b = i
        while b+1 < len(vl) and vl[b+1][1].strip() and not vl[b+1][3]: b += 1
        print(f"--- {f}:{vl[a][0]}-{vl[b][0]}  [{want.strip()}]")
        for k in range(a, b+1): print("   " + vl[k][1])
