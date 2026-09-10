"""Run every converted thesis netlist through the version 9 solver."""
import re
import sys

import sympy as sp
import symbulator as sb

from parse_book import parse
from to_v9 import convert

NUM = re.compile(r"^([0-9]*\.?[0-9]+(?:[eE][-+]?\d+)?)")


def omega_from(args):
    """Q passed omega as sq\\ac's second argument: a number, or `x` for a
    symbolic sweep."""
    a = (args or "").split(")")[0].split(":")[0].strip().rstrip(",")
    if not a:
        return None, "omega missing from the source"
    m = NUM.match(a)
    if m:
        return float(m.group(1)), ""
    if a in ("\u03c9", "w"):
        return sp.Symbol("omega", positive=True), ""
    if re.fullmatch(r"[A-Za-z]\w*", a):
        return sp.Symbol(a, positive=True), ""
    return None, f"omega not readable from {a!r}"


def nodes_from(args):
    """Q's trailing `,n1,n2` for a thevenin/norton/port run."""
    parts = [p.strip() for p in (args or "").split(")")[0].split(",")
             if p.strip()]
    if len(parts) >= 2 and all(re.fullmatch(r"\w+", p) for p in parts[:2]):
        return parts[0], parts[1], ""
    return None, None, f"port nodes not readable from {args!r}"


def kind_named(desc):
    """Does the description contain an actual two-port element?"""
    return any(r.strip()[:1].lower() in "zyhgab"
               for r in desc.splitlines() if r.strip())


def two_port_kind(desc):
    """Q chose the parameter set from a menu, so a description with a
    two-port element names its own kind and one without defaults to z."""
    for r in desc.splitlines():
        c0 = r.strip()[:1].lower()
        if c0 in "zyhgab":
            return c0
    return "z"


def run(c):
    """-> (Result-ish or None, error string)"""
    a, how, desc, args = c["analysis"], c["how"], c["desc"], c["args"]
    try:
        if how == "plain":
            if a == "dc":
                return sb.dc(desc), ""
            if a == "ac":
                om, err = omega_from(args)
                if om is None:
                    return None, err
                return sb.ac(desc, om), ""
            if a == "tr":
                return sb.tr(desc), ""
            if a == "fd":
                return sb.fd(desc), ""
        if how in ("th", "er", "port"):
            n1, n2, err = nodes_from(args)
            if n1 is None:
                return None, err
            if how == "th":
                try:
                    return sb.th(desc, n1, n2), ""
                except Exception as exc:
                    if "not active" not in str(exc):
                        raise
                    # Q's single `thevenin` tool covered both cases; v9
                    # splits them, and says so in the error itself.
                    return sb.er(desc, n1, n2), "used er(): passive network"
            if how == "er":
                return sb.er(desc, n1, n2), ""
            kind = two_port_kind(desc)
            return sb.port(desc, n1, n2, kind), (
                "" if kind_named(desc) else "no two-port element in the "
                "description; computed z parameters")
        return None, f"no runner for {a!r}/{how!r}"
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def main():
    probs = parse()
    ok, failed, notrun = [], [], []
    for p in probs:
        if not p["netlists"]:
            notrun.append((p["num"], "no netlist in the Book"))
            continue
        tool, desc, rest = p["netlists"][0]
        c = convert(tool, desc, rest, stores=p.get('stores'))
        if c["analysis"] is None:
            notrun.append((p["num"], c["notes"][0]))
            continue
        res, err = run(c)
        (ok if res is not None else failed).append(
            (p["num"], tool, err, c))
    print(f"{len(probs)} problems: {len(ok)} solved, {len(failed)} failed, "
          f"{len(notrun)} not a circuit run\n")
    if failed:
        print("--- failed ---")
        for num, tool, err, c in failed:
            print(f"  {num}  sq\\{tool:9} {err[:88]}")
    if notrun:
        print("\n--- not a circuit run ---")
        for num, why in notrun:
            print(f"  {num}  {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
