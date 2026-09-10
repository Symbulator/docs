"""Rewrite a 2001-thesis (Symbulator Q) circuit description as version 9.

The description language barely moved in twenty-five years. What changed,
and all this does:

  * the separator: Q used `;`, v9 uses `:` or one element per line;
  * row padding: Q padded a short circuit and a two-port with a trailing
    `0` so every row had four terms. v9's `s` takes three
    (name,n1,n2) and a two-port takes name,n1,n2 with the parameters
    optional, so the padding zero is dropped;
  * the square-root glyph, which the .doc extraction left as a literal
    U+221A that v9's value reader rejects: `√2` -> `sqrt(2)`;
  * the analysis, which was the tool name in Q (`sq\\dc`, `sq\\thevenin`)
    and is a setting in v9.

Nothing else is touched: no value is altered, no element renamed, no
node renumbered. Where a construct has no v9 spelling the problem is
flagged rather than quietly patched.
"""
import re

# Q tool -> (v9 analysis, how the run is made)
TOOLS = {
    "dc":       ("dc", "plain"),
    "ac":       ("ac", "plain"),
    "tr":       ("tr", "plain"),
    "fd":       ("fd", "plain"),
    "fd_to_tr": ("tr", "plain"),
    "expert":   ("dc", "plain"),      # Expert Mode is a card in v9
    "experto":  ("dc", "plain"),
    "thevenin": ("dc", "th"),
    "Thevenin": ("dc", "th"),
    "norton":   ("dc", "er"),
    "port":     ("dc", "port"),
    # mini-tools: not a circuit run at all
    "gain": (None, "tool"), "bode": (None, "tool"), "plot": (None, "tool"),
    "absang": (None, "tool"), "par": (None, "tool"), "solves": (None, "tool"),
    "makemenu": (None, "tool"),
}

PAD_ZERO = re.compile(r"^([szyhgab]\w*\s*,[^,]+,[^,]+),\s*0\s*$", re.I)

#: Element types that take no initial condition in v9. Q's frequency-domain
#: form padded *every* row to five terms with a trailing `,0`; v9 keeps the
#: fifth term only for an inductor and a capacitor, where it means an
#: initial current or voltage.
NO_IC = "rejsmo"
FIVE = re.compile(r"^(\w+\s*,[^,]+,[^,]+,[^,]+),\s*0\s*$")
SPACED = re.compile(r"\b[A-Za-z0-9]\s+,|\,\s+[A-Za-z0-9]\s+[,;]")


def fix_row(row, fd=False):
    """One element row, Q spelling -> v9 spelling."""
    row = row.strip()
    if not row:
        return "", ""
    note = ""
    if row[:1].lower() in NO_IC:
        m5 = FIVE.match(row)
        if m5:
            row = m5.group(1).strip()
            note = ("dropped Q's frequency-domain padding zero -- v9 keeps a "
                    "fifth term only on an inductor or a capacitor")
    m = PAD_ZERO.match(row)
    if m:
        kind = "short circuit" if row[0].lower() == "s" else "two-port"
        row = m.group(1).strip()
        note = f"dropped Q's padding zero from the {kind} row"
    if "√" in row:
        row = re.sub(r"√\s*\(", "sqrt(", row)
        row = re.sub(r"√\s*([0-9.]+)", r"sqrt(\1)", row)
        note = (note + "; " if note else "") + "square-root glyph -> sqrt()"
    return row, note


def with_params(row, stores):
    """A two-port row gains its stored parameters, v9 style (#163)."""
    if not stores or row[:1].lower() not in "zyhgab":
        return row, ""
    name = row.split(",")[0].strip()
    keys = [f"{name}{i}" for i in ("11", "12", "21", "22")]
    vals = [stores.get(k) for k in keys]
    if not all(vals):
        return row, ""
    if row.count(",") >= 3:                 # already carries parameters
        return row, ""
    return (f"{row},[{','.join(vals)}]",
            f"folded in the stored parameters {name}11/12/21/22, which Q "
            f"kept in calculator variables")


def to_v9(desc, fd=False, stores=None):
    """-> (v9 description, [notes]). One element per line."""
    rows, notes = [], []
    for part in desc.split(";"):
        row, note = fix_row(part, fd=fd)
        if row:
            row, pnote = with_params(row, stores)
            rows.append(row)
            if pnote:
                notes.append(pnote)
        if note:
            notes.append(note)
    return "\n".join(rows), notes


def damaged(desc):
    """Extraction damage, as opposed to notation: letters spread out by
    the .doc text extraction, or a glyph that did not survive it."""
    why = []
    if SPACED.search(desc):
        why.append("characters spaced out by the .doc extraction")
    for ch in desc:
        if ord(ch) > 0x2000 and ch not in "√":
            why.append(f"unrecovered glyph {ch!r} (U+{ord(ch):04X})")
            break
    return why


def convert(tool, desc, rest, stores=None):
    """-> dict(analysis, how, desc, args, notes, damage) ; analysis None
    means this entry is not a circuit run."""
    analysis, how = TOOLS.get(tool, (None, "unknown"))
    if how in ("tool", "unknown") or not desc:
        return dict(analysis=None, how=how, desc="", args="",
                    notes=[f"sq\\{tool} is not a circuit run"], damage=[])
    v9, notes = to_v9(desc, fd=(analysis in ("fd", "tr")), stores=stores)
    return dict(analysis=analysis, how=how, desc=v9, args=(rest or "").strip(),
                notes=notes, damage=damaged(desc))
