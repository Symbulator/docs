# Symbulator (Python) — expert-mode equations on derived quantities are silently ignored

**Package:** `symbulator` 0.4.4 (PyPI) · **File:** `symbulator/engine.py` ·
**Function:** `solve_circuit` · **Severity:** wrong answer, no error, no warning

A patch against 0.4.4 is attached — `symbulator-0.4.4-expert-derived.patch`,
`patch -p1` from the source root. It applies cleanly, and the suite goes from
113 to 124 passing.

---

## Symptom

Expert mode accepts an equation written on any of the derived answers — `r_e`,
`p_r1`, `v_r2`, `z_e` — and appears to work. It does not. The equation is
discarded and the circuit comes back solved one constraint short: correct, but
parametrized in a leftover node voltage instead of resolved to numbers.

Nothing is raised, nothing is logged, and the result object looks normal. This
is the documentation's own worked example (B11's Example 5.6):

```python
ex("e,1,0,e:r1,1,2,rx:r2,2,3,4'k:r3,3,0,6'k", "dc",
   equations=["r_e = 12000", "i_r3 = 0.006"],
   unknowns=["e", "rx"])

# 0.4.4:      e  -> v_1
#             rx -> 166.666666666667*v_1 - 10000.0
# expected:   e  -> 72.0        (substituting v_1 = 72 by hand does give
#             rx -> 2000.0       rx = 2000, so the answer is not wrong,
#                                just not finished)
```

Restating the same fact in node-voltage and element-current terms works
perfectly today — `equations=["v_1 = 12000*i_r3", "i_r3 = 0.006"]` returns
72.0 and 2000.0. That is the workaround, and it is what the documentation
currently teaches. It is not obvious, and there is nothing to lead a user to
it, because the failing form does not look like it failed.

## Root cause

`analysis._derived()` computes the third-level quantities — branch voltage
`v_<element>`, power `p_`/`s_`/`ap_`, and the resistance/impedance a source
sees, `r_`/`z_` — **after** `solve_circuit()` returns. They are algebra on the
finished solution, not part of the KCL system, so the solver has never heard
of them.

So when `solve_circuit` parses `"r_e = 12000"`, `r_e` is a symbol it does not
recognise. It then falls into this, at the end of the `if equations:` block:

```python
# Convenience beyond the original: a brand-new symbol appearing
# in an extra equation (e.g. "pout = v_2*i_r2") becomes an
# unknown automatically, ...
for eq in extra_eqs:
    for sym in sorted(eq.free_symbols, key=str):
        if str(sym) not in existing and str(sym) not in reserved:
            circuit.unknowns.append(sym)
```

`r_e` is registered as a brand-new unknown. `sp.solve` then satisfies
`Eq(r_e, 12000)` by setting the phantom `r_e` to 12000, which costs it nothing
and tells the circuit nothing. Net effect: one more equation, one more unknown,
and the real system exactly as under-determined as it was before.

The convenience itself is right and worth keeping — `pout = v_2*i_r2` should
auto-declare `pout`. The bug is that it cannot tell a user's new label from a
name that already means something.

The counting is easy to confirm:

```python
from symbulator.elements import parse_circuit
from symbulator.engine import Circuit
c = Circuit(parse_circuit("e,1,0,e:r1,1,2,rx:r2,2,3,4'k:r3,3,0,6'k"), "dc", suffix="si")
c.stamp_all()
len(c.equations), [str(u) for u in c.unknowns]
# 7 equations, 7 unknowns: i_e, v_1, i_r1, v_2, i_r2, v_3, i_r3
```

Add `e` and `rx` (9 unknowns, 7 equations), then `i_r3 = 0.006` (9, 8), then
`r_e = 12000` as a phantom (10, 9). Still one short — hence the free `v_1`.

## The fix

A new `engine._derived_definition(circuit, name, domain)` recognises a symbol
that names a derived quantity **of an element actually in this circuit**, and
returns the equation defining it in terms of the system's own unknowns. That
equation is stamped in alongside the user's, so the constraint lands on the
circuit instead of on a phantom.

| Name | Definition stamped |
|---|---|
| `v_<element>` | `v_<element> = v(n1) - v(n2)` |
| `p_<element>` (dc) | `p_<element> = (v(n1) - v(n2)) * i_<element>` |
| `p_<opamp>` (dc) | `p_<opamp> = v(n_out) * (-i_<opamp>)` |
| `r_<source>` (dc) | `r_<source> * (-i_<source>) = v(n1) - v(n2)` |
| `z_<source>` (ac) | `z_<source> * (-i_<source>) = v(n1) - v(n2)` |

The `r_`/`z_` forms are written multiplied out rather than as a division, so
the system stays polynomial and a zero current cannot put a division by zero
into it.

**The AC powers are refused rather than supported.** `s_`, `p_` and `ap_` in
the AC domain are defined through `v * conjugate(i)`, and conjugation is not
something `sympy.solve` can carry through a system. Those now raise
`CircuitError` naming the quantity and pointing at the `v_`/`i_` restatement.
That is a deliberate choice: the alternative is the same silence this is meant
to end, and no working call is broken by it, since none of these ever worked.

Three properties kept intact:

- **An explicit `unknowns` list still wins.** Names the caller lists are
  already registered before this runs, so they are skipped. `r_b` as a
  component value in a circuit with no element `b` behaves exactly as before.
- **Matching is against real element names**, not a regex on the prefix, so
  `pout`, `vin`, `r_b` and friends are untouched unless they genuinely collide
  with an element in that circuit.
- **The auto-unknown convenience survives** for everything that is not a
  derived-quantity collision.

### Adjacent case, same cause, also fixed

A `j` source's current — and a capacitor's in AC — live in `circuit.known`
rather than the unknowns, so `i_j1 = 0.005` was phantomed by the same path.
Extra equations are now substituted against `known` first, which turns that
into a real constraint on the source's symbolic value. An equation that
reduces to nothing afterwards is dropped as redundant; one that reduces to a
contradiction now says so plainly instead of surfacing later as "could not
solve the system".

## Verification

All existing 113 tests pass unchanged. Eleven added, in
`symbulator/tests/test_expert.py`, covering `r_` (the case above, asserting
72 V and 2 kΩ), branch voltage, DC power, op-amp power, AC `z_`, the AC-power
refusal, the explicit-unknowns precedence, and the three `known`-current cases.

One of the new tests is there specifically to catch drift: the definitions in
`_derived_definition` duplicate the formulas in `analysis._derived`, so it
constrains `r_e = 12000` and then asserts the `r_e` that `_derived` reports
afterwards is in fact 12000. If the two ever disagree, that fails.

## Two things worth knowing, not fixed

**Quadratic derived quantities have two roots.** `p_r2 = 0.008` on a 12 V
divider with 4 k on top is satisfied by both 2 k and 8 k; `sp.solve` returns a
list and `solve_circuit` takes `solutions[0]`. That behaviour predates this
change and is unchanged by it, but constraining a power makes it much easier
to run into than constraining a voltage.

**The documentation has not been relaxed.** `02-lesson-symbolic.md` currently
teaches the `v_`/`i_` form and explains the limitation, which is correct for
0.4.4 as published. If this ships, that note should be cut back to a plain
recommendation rather than a workaround — happy to do that once there is a
version number to point at.
