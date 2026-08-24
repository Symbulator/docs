# Symbulator 9 API — verified against the real package

Checked against `symbulator` 0.4.1, installed and actually run (not just read)
in the interface-chat sandbox. Every claim below with a code sample was
executed for real; outputs are pasted verbatim.

## 1. Calls in the documentation — all confirmed correct

`dc(desc)`, `ac(desc, omega=…)`, `tr(desc)`, `th(desc, n1, n2, domain=…)`,
`er(desc, n1, n2, domain=…)`, `res.v(node)`, `res.i(name)`,
`res["p_*"]`/`res["v_*"]`, `use_rms=True` (on `ac`/`th`), `variables=[…]`
(on `tr`) all match the real signatures and behave as documented. Ran the
worked example in `01-lesson-dc.md:445` end to end
(`dc("e,1,0,36:r1,1,2,1'k:r2,2,3,3'k:r3,3,0,2'k")`) and every one of
`r_e`, `-i("e")`, `v_r1/2/3`, `p_r1/2/3`, `p_e` matched the stated answers
exactly (6000, 0.006, 6/18/12, 0.036/0.108/0.072, and the closing equality
check evaluates to Python `True`).

One nuance worth stating explicitly in the text: `res["r_*"]` (and `z_*`) are
only computed for **source** elements (`e`/`j`), giving the resistance/
impedance that source sees looking into the rest of the circuit — not a
per-element value available for any component. The one worked example that
uses it (`r_e`) already applies it correctly to a source, so no fix needed,
just worth a sentence since a reader might otherwise try `res["r_r1"]` and be
confused when it's missing.

## 2. `th()`'s return object — the TODO's suspicion was right

`th()` returns a `TheveninResult` dataclass with **exactly four fields**:
`domain, vth, ino, z, pmax`. Confirmed by reading `equiv.py` and running it.

- `eq.vth`, `eq.ino`, `eq.z`, `eq.pmax` — **correct as documented.**
- `eq.irl`, `eq.vrl`, `eq.prl`, `eq.eqcir`, `eq.apmax`, `eq.aprl` — **do not
  exist.** Confirmed by running the exact worked example in
  `04-lesson-equivalents.md:314` (`eq.irl.subs(...)`) — it raises
  `AttributeError: 'TheveninResult' object has no attribute 'irl'`. Every
  reader who reaches that example will hit a crash, not `{1.5, .5, .059}`.

**The fix**, verified to reproduce the documented answer exactly: there is no
built-in load-family helper, so derive it from `vth`/`z` with two lines of
SymPy, once, right where `irl`/`vrl`/`prl` are introduced:

```python
from sympy import Symbol, simplify
load = Symbol("load")
irl = simplify(eq.vth / (eq.z + load))
vrl = simplify(irl * load)
prl = simplify(irl**2 * load)
```

Ran this against `th("e1,1,0,9:r1,1,2,3:r2,2,0,6", "2", "0", domain="dc")`:
`irl = 6/(load + 2)`, and `[float(irl.subs(load, x)) for x in (2,10,100)]` →
`[1.5, 0.5, 0.0588…]` — matches `{1.5, .5, .059}` exactly.

`eq.eqcir` (04-lesson-equivalents.md:368, a ready-made equivalent-circuit
description string) has no equivalent at all — nothing in `equiv.py`
generates one. If it's worth keeping, the fix is a one-line f-string:
`f"vth,1,0,{eq.vth}:z,1,0,{eq.z}:rl,1,0,rl"` (adjust node names to taste).

`eq.apmax`/`eq.aprl` (08-lesson-power.md:55,77 — apparent-power versions for
the AC case) also don't exist. The real `pmax` field already handles both
domains (it branches on `domain` internally — real max power for dc, using
`sp.re(z)` for ac). I did not derive an apparent-power formula myself since I
couldn't find the original TI source's exact definition to match against —
flagging this one back to Roberto rather than guessing.

## 3. Claims of absence

| Claim | Verdict |
|---|---|
| No `pr` tool, hand-roll one | **Wrong.** `symbulator.pr(*impedances)` exists and does exactly this — parallel combination of any number of values, and it's *more* correct than the hand-rolled version in the doc: it explicitly short-circuits to 0 if any argument is 0, whereas the doc's `1/sum(1/v for v in values)` would raise `ZeroDivisionError` on that same input. No square-bracket `[…]` shorthand *in circuit-description strings* — that part is correctly absent, it's a plain function call instead. |
| No `pf` tool, hand-roll one | **Wrong**, `symbulator.pf(voltage, current)` exists — but see the correctness note below, which affects both the real function and the doc's own hand-rolled version equally. |
| No `aa` tool | **Correct**, confirmed absent. The suggested `Abs()`/`arg()` replacement is fine. |
| No plotting tool, use SymPy's `plot()` | **Half right, and it leaves a documented TODO unanswered.** For `tr()` results (functions of `t`), SymPy's `plot()` genuinely works. But `bode_samples(desc, key, f_min, f_max, n=200, ...)` also exists, returning `(freq, mag_db, phase_deg)` ready for any plotting library — and this is the piece that actually matters, because SymPy's `plot()` **cannot** produce a Bode plot from an `ac()` result the way the doc's advice implies (an `ac()` result is a phasor at one fixed `omega`, not a function of frequency). Ran it: `bode_samples("e,1,0,1:r1,1,2,1000:c1,2,0,1e-6", "v_2", 10, 100000, n=5)` returns a clean RC-lowpass rolloff (`mag_db` falling from ~0 to -56 dB, `phase_deg` from -3.6° to -89.9°). **This directly answers `11-lesson-bode.md`'s own open TODO** ("confirm whether the Python port exposes a bode helper, or whether this should show Matplotlib directly") — it does, use it. There's a `time_samples()` twin for `tr()` too, which is also worth mentioning since inverse-Laplace results can fail to reach closed form (see `tr()`'s own docstring) and `time_samples()` sidesteps that by sampling numerically instead. |
| No interactive expert mode, solve afterward with SymPy | **Wrong, and this is the one I'd fix first.** `dc()`, `ac()`, `fd()`, and `tr()` all take `equations=`, `unknowns=`, `conditions=` directly — the exact same three lists the calculator's "Add equations / Add unknowns / Add conditions" prompts collected — and `ex(desc, domain, ...)` is a thin wrapper over the same three (domain becomes an argument instead of a prompt). This is a real, integrated expert mode, not "solve the finished result afterward" — and that distinction matters concretely: in the doc's own `02-lesson-symbolic.md` expert-mode example, the unknown (`rx`) is a *circuit element's own value*, not a solved output — there is no finished symbolic result to hand to `sympy.solve()` afterward, because the circuit can't be solved at all until `rx` is resolved. I ran the doc's exact example (`"e,1,0,e:r1,1,2,rx:r2,2,3,4'k:r3,3,0,6'k"`, `equations=["r_e = 12000", "i_r3 = 0.006"]`, `unknowns=["e", "rx"]`) through `ex()`: **it is a real, one-call expert-mode solve**, not a manual two-step process. One caveat worth documenting alongside it: this particular example didn't fully collapse to numbers on the first pass — `e` came back as `v_1` and `rx` as `166.667*v_1 - 10000.0` (a properly-determined but still-symbolic result, because `rx` multiplies an unknown current, making the system nonlinear). Substituting `v_1 = 72` by hand gives `rx = 2000` exactly, matching the documented answer — so the fix isn't "there's no expert mode," it's "solve the returned parametrized expression by hand as a fallback when it doesn't fully resolve," which is a real and useful thing to teach either way. |
| No reserved names | **Correct.** Results come back as a plain object (`.get()`/`[]`/`.v()`/`.i()`), never written into a shared namespace, so there's no possibility of a name collision with anything. |
| Exact arithmetic is safe, no `cSolve` bug | **Correct**, structurally — SymPy is a different, mature solver with no relation to the TI CAS's specific `cSolve` performance pathology described in the doc. |

## 4. One correctness bug found that isn't in the TODO at all: `pf()` leading/lagging can come out backwards

Ran the doc's own `pf` worked example (08-lesson-power.md, AS7 Example 11.10:
`ac("e,1,0,30:r1,1,2,6:r2,2,0,-2j:r3,2,0,4", omega=Symbol("omega"),
use_rms=True)`, then power factor of the source). The documented v7/v8 answer
is **0.97342 leading**. Both the doc's own hand-rolled `pf(s)` *and* the real
package's `pf(v_e, i_e)`, called naively on the source's own `s_e`/`v_e`/`i_e`
(which represent power/voltage/current **consumed by** the source, per the
package's stated sign convention), give **0.97342 lagging** — the direction
is backwards. Negating first — `pf(v_e, -i_e)`, i.e. using the power the
source *delivers* rather than consumes — gives **0.97342 leading**, matching
the documented answer exactly.

This makes sense once you notice the original calculator's `pf` tool
special-cased its string-argument form ("recognises three elements in this
form: e, j and r") — it likely auto-flipped the sign for source elements
internally. The Python port's `pf(voltage, current)` takes raw values and
can't know whether they came from a source or a load, so it can't do that
flip for you. **Whatever code goes in the v9 lesson needs the sign called out
explicitly** — either `pf(v_e, -i_e)` for a source, or note that `s_e`
represents consumed power and the reader should negate it for "leading/
lagging" purposes when looking at a source rather than a load. This affects
the doc's own hand-rolled workaround identically, so it's not fixed by simply
switching to the real `pf()` function — the sign issue is conceptual, not a
package bug.

## Not checked

`variables:` in `book.yaml` / the 217 practice problems (out of scope per the
TODO — "should wait until the API above is confirmed," and now it has been).
`th()`'s `pmax` formula for the ac case, and `port()`'s h/g parameter
conventions, I read in source but didn't independently re-derive from first
principles — the code comments in `equiv.py` are detailed enough that I trust
them, but flagging that as "read, not re-derived" for completeness.

---

# Part 2 — applied to the source, and re-checked against 0.4.4

Added 21 August 2026. Everything in Part 1 has now been written into `src/`.
While doing that, each claim was re-run against `symbulator` **0.4.4** (Part 1
used 0.4.1), which turned up three corrections to Part 1 itself and two new
findings. Every number below was executed, not reasoned about.

## Corrections to Part 1

**1. The `[…]` shorthand is *not* absent.** Part 1 said the square-bracket
shorthand was correctly documented as missing. In 0.4.4 it works, inside
circuit-description strings, exactly as on the calculator — numerically and
symbolically:

```python
dc("e,1,0,16.8:r1,1,2,9:r2,1,2,6:r3,2,3,4:re,3,0,[6,3]:r6,2,0,3")
# -i("e") -> 3.0, i.e. re was reduced to 2 Ω        (B11 Example 7.4)
dc("jt,0,1,12'm:r1,1,0,1'k:re,1,0,[10'k,22'k]")
# v_1 -> 10.476…, matching 0.012 * pr(1000, pr(10000, 22000))
dc("e,1,0,v:re,1,0,[ra,rb]")      # i_e -> -v/rb - v/ra
```

Either it arrived between 0.4.1 and 0.4.4, or the earlier check was wrong.
Version 9 now gets the same shorthand section the calculator versions have.

**2. `apmax` maps straight onto `eq.pmax`, no formula needed.** Part 1 flagged
the apparent-power question back to Roberto rather than guessing. It did not
need guessing: for the documentation's own worked example,

```python
eq = th("e,1,0,10:r1,1,2,4:r2,2,0,8-6j:r3,2,3,5j", "3", "0", domain="ac")
eq.pmax        # -> 2.36742424242424
```

which is the documented 2.3674 W exactly. `pmax` branches on the domain and,
in the AC domain, already *is* the average maximum power. The lesson now says
so. The load-family counterpart checks out too — with
`aprl = Abs(vth/(z+load))**2 * re(load) / 2`, substituting `conjugate(eq.z)`
gives 2.36742424242424, the same number.

**3. A sign error in the shared prose.** Verifying the above exposed something
that was wrong for all three versions: `eq.z` is 2.933 + j4.467, so the
maximum-power load is its conjugate, 2.933 − j4.467. The text gave the
conjugate as 2.933 + j4.467. Corrected, and flagged in
`TODO-verify-v9-api.md` for Roberto to check against his original.

## Expert mode: it works, with one caveat that changes the advice

Part 1 was right that `ex()` and the `equations=`/`unknowns=`/`conditions=`
arguments are a real integrated expert mode, and right that the documentation's
own example came back parametrized (`e = v_1`, `rx = 166.667*v_1 - 10000`)
rather than numeric. Part 1 concluded the fix was to teach the by-hand
substitution as a fallback. It is better than that: the example resolves
completely in one call once the equations are written in primitive terms.

```python
ex("e,1,0,e:r1,1,2,rx:r2,2,3,4'k:r3,3,0,6'k", "dc",
   equations=["v_1 = 12000*i_r3", "i_r3 = 0.006"],
   unknowns=["e", "rx"])
# res["e"] -> 72.0,  res["rx"] -> 2000.0     — the documented answers
```

The failure was in `r_e = 12000`, not in the expert mode. Derived keys —
`r_*`, `p_*` — are expanded into raw node variables inside `equations=` rather
than the solved closed form, so they contribute nothing and leave the system a
parameter short. `v_1 = 12000*i_r3` states the identical fact in `v_`/`i_`
terms and closes it. `v_1 = -12000*i_e` works equally well.

**Fixed in symbulator 0.4.5**, released 21 August 2026. `solve_circuit` now
recognises a symbol that names a derived quantity of an element in the circuit
and stamps its defining equation into the system, so the constraint lands on
the circuit instead of on a phantom of the same name. Re-verified against the
released package: the example above returns 72.0 and 2000.0 written the
natural way, as `equations=["r_e = 12000", "i_r3 = 0.006"]`. Branch voltages
(`v_r2`), DC powers (`p_r2`) and the impedance a source sees (`z_e`) work
too, and an equation on a `j` source's own current is no longer swallowed.

The AC power family stays out, by design — `s_`, `p_` and `ap_` are defined
through `v * conjugate(i)`, which `sympy.solve` cannot carry — but it now
raises a `CircuitError` naming the quantity rather than failing silently.

`02-lesson-symbolic.md` has been rewritten accordingly: the workaround is
gone, the example reads the way the calculator's did, and the lesson notes
that this needs 0.4.5 or newer.

## New finding: the time symbol carries an assumption

Time-domain answers are written in `Symbol("t", positive=True)`. A bare
`Symbol("t")` is a *different* symbol to SymPy, and nothing complains:

```python
res = tr("e,1,0,10/s:r1,1,2,1000:c1,2,0,1e-6")
res["v_2"]                                  # 10.0 - 10.0*exp(-1000.0*t)
Symbol("t") in res["v_2"].free_symbols      # False
res["v_2"].subs(Symbol("t"), 0.001)         # unchanged — silently does nothing
res["v_2"].subs(Symbol("t", positive=True), 0.001)   # 6.32120558828558
```

The documentation's plotting line was `plot(res["v_2"], (Symbol("t"), 0, 5e-3))`
— broken, and broken quietly. `t2s()` has the same trap: `t2s(exp(-2*t))` with
the package's own symbol gives `1/(s + 2)`, but the string form
`t2s("exp(-2*t)")` sympifies to the assumption-free `t`, treats it as a
constant and returns `exp(-2*t)/s`. Both places now carry a warning.

## Confirmed working, as documented

- `pf(res["v_e"], -res["i_e"])` returns the string `pf: 0.97342 leading`,
  matching the calculator's printed output character for character. Without the
  minus sign: `pf: 0.97342 lagging`. Part 1's sign finding stands, and is now a
  warning box in the lesson.
- `pr(16 + pr(18, 9, …))` nests and reproduces the 19 Ω of AS7's Practice
  Problem 2.10; `pr(6, 0, 4)` returns 0; `pr([18, 9])` accepts a list.
- `bode_samples("e,1,0,1:r1,1,2,1000:c1,2,0,1e-6", "v_2", 10, 100000, n=5)` →
  mag_db `[-0.02, -1.45, -16.07, -35.96, -55.96]`, phase_deg
  `[-3.6, -32.14, -80.96, -89.09, -89.91]`. `time_samples` on the same RC with
  a `10/s` step → `[0.0, 7.135, 9.179, 9.765, 9.933]`.
- `s2t` and `t2s` are exported, answering `12-lesson-fd.md`'s open question.
- The AC lesson's numbers: `Abs(res.i("r1"))` → 1.789 at 26.56°, `v_c` → 4.472
  at −63.44°, and `ap_*`, `s_*`, `z_*` all present. `er(…, domain="ac",
  omega=…)` works.
- `res["r_r1"]` raises `KeyError`; only `r_e` exists on that circuit — the note
  Part 1 asked for is now in `01-lesson-dc.md`.
- `gain(v1, i1, v2, i2)` and `port(desc, n1, n2, kind, …)` exist, for
  `13-lesson-twoports.md` when it gets written.

## Still not checked

`th()`'s `pmax` for the AC case is now confirmed numerically against the one
worked example, but not re-derived from first principles for the general case.
`port()`'s h/g parameter conventions remain read, not re-derived. The 217
practice problems are untouched.
