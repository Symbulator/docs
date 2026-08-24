# Verifying the Symbulator 9 API claims — closed

**Status: done.** Everything this file used to list has been checked against
the real package and, as of 21 August 2026, the documentation has been
corrected to match. The findings are in `VERIFIED-v9-api.md`; the corrections
are in `src/`.

The original task was this: versions 7 and 8 came from Roberto's own pages and
practice files and were authoritative, but the version 9 text had been written
by reading the `symbulator` package's README and extrapolating. Nothing had
been run. Some of it was wrong, and it was.

## What was wrong, in one line each

| Claim in the documentation | Reality | Fixed in |
|---|---|---|
| `eq.irl`, `eq.vrl`, `eq.prl` exist on a `th` result | They do not — `AttributeError` | `04-lesson-equivalents.md` |
| `eq.eqcir` gives a ready-made description string | It does not | `04-lesson-equivalents.md` |
| `eq.apmax` / `eq.aprl` exist | They do not; `pmax` covers both domains | `08-lesson-power.md` |
| No `pr` tool, hand-roll one | `pr()` exists, and so does the `[…]` shorthand | `03-lesson-sources.md` |
| No `pf` tool, hand-roll one | `pf(v, i)` exists | `08-lesson-power.md` |
| No expert mode, solve afterwards | `equations=`/`unknowns=`/`conditions=` and `ex()` | `02-lesson-symbolic.md` |
| No plotting help beyond SymPy's `plot` | `bode_samples()` and `time_samples()` | `06`, `11` |
| — (not previously noticed) | `pf` reports leading/lagging backwards for a source | `08-lesson-power.md` |
| — (not previously noticed) | Time answers use `Symbol("t", positive=True)` | `06`, `12` |

Correct as written, and left alone: no `aa` tool, no reserved names, exact
arithmetic is safe, and `res["r_*"]`/`z_*` for sources — the last of which
picked up an explanatory note in `01-lesson-dc.md`.

## What is still open

1. ~~**`equations=` does not reduce derived keys.**~~ **Fixed in 0.4.5**
   (21 August 2026). Passing `r_e = 12000` used to yield a correct but
   still-parametrized answer, because the key was expanded into raw node
   variables instead of the solved closed form — in effect the equation was
   absorbed by a same-named phantom unknown and constrained nothing. The
   engine now stamps the defining equation for a derived quantity into the
   system, so `r_e`, `p_r1`, `v_r2`, `z_e` all work. Verified against the
   released package: the documentation's own example returns e = 72 V and
   rx = 2 kΩ in one call. `02-lesson-symbolic.md` has been rewritten to the
   natural form and no longer teaches the workaround.

   The AC power quantities (`s_`, `p_`, `ap_`) remain unavailable in
   `equations=` by design — they are defined through complex conjugation —
   but they now raise a clear error instead of being silently ignored.

2. **A sign error in shared prose, now corrected — please confirm.** In
   `08-lesson-power.md`, the AC maximum-power example said the conjugate of the
   equivalent impedance was 2.933 + j4.467. The equivalent impedance *is*
   2.933 + j4.467, so its conjugate is 2.933 − j4.467. This was wrong for all
   three versions, not just version 9. It has been corrected; since it touches
   the calculator text, Roberto may want to check it against his original.

3. **The 217 practice problems.** Still calculator-only, wrapped in
   `::: only 7,8`. This was blocked on the API question, and no longer is.
   Roughly 295 commands to translate.
