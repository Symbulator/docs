# Rewriting the Symbulator 9 documentation around the interface

**Started 23 Aug 2026.** Roberto's brief: the version 9 chapters were written
as if they documented the `symbulator` PyPI package. They document the *web
app*. A reader of these chapters has a browser open at a page of fields,
menus and cards — not a Python prompt.

This file is the working plan and the honest state of it. Delete it when the
job is finished.

---

## The translation

| Written as | Should be |
|---|---|
| `dc("e1,1,0,5:r1,1,2,1'k")` | type it into **Circuit description**, one element per line |
| calling a named function | choose **Type of analysis**, then **Analysis** |
| "press ENTER" | click **Run Symbulator** |
| `plot(...)` | fill in the **Plot** card, click **Run** |
| "the answer is in `ir1`" | read `i_r1` in the **Results** section |
| `pip install symbulator` | how to reach the live app; point at the interface's own text |
| storing a description in a variable | the **Circuit** card — *Save inputs to new entry* |

Two rules from Roberto, and both matter more than they look:

**Spell it out.** Not "type the description" but "type the description, as
follows:" and then the description. Not "read it in the Results section" but
"under `r1` you will see `i_r1` given as 6 mA". A reader with the browser open
should be able to follow without inventing anything.

**Vary the wording.** Fourteen chapters of "Under Type of analysis choose
Solve circuit" would be unreadable. Same instruction, different sentences.

## The markup

`build.py` grew a `field` fence for this — see `SPEC.md`:

    ```field 9 Circuit description
    e1,1,0,36
    r1,1,2,1'k
    ```

The name is required; `--check` fails without it. It renders as a labelled
panel resembling the interface's box, and as ordinary typed input in the PDFs.
`out` fences keep their meaning for what comes back.

Still to add: an inline role for control names, so **Run Symbulator** and
*DC — direct current* are marked as interface objects rather than emphasis.
Today they are plain bold, which cannot be styled distinctly later.

## Long form once, short form after

Roberto, 24 Aug 2026. **The first problem in a chapter — or the first to use a
newly introduced feature — gets the full walkthrough. Everything after it gets
the short form.**

The reason is that the long form teaches and the short form practises. A
reader who has been walked through the Plot card once does not need walking
through it again three problems later; being walked through it anyway is how a
tutorial starts to feel like it doubts you.

**Long form** — naming every control, in order, with the value spelled out:

> In the box labelled **Circuit description**, type the circuit, one element
> per line:
>
> ```field 9 Circuit description
> e,1,0,36
> r1,1,2,1'k
> ```
>
> Under **Type of analysis** choose *Solve circuit*, and under **Analysis**
> choose *DC — direct current*. Click **Run Symbulator**.
>
> Scroll to **Results**. In the block headed `r1` *resistor*, the line marked
> **current through** reads *i*<sub>r1</sub> = 6 mA.

**Short form** — the same instruction, assuming the reader has done it before:

> Describe it and run it in DC:
>
> ```field 9 Circuit description
> e,1,0,36
> r1,1,2,1'k
> ```
>
> **Results** gives *i*<sub>r1</sub> = 6 mA.

Both still spell out what to type and what to look for -- that rule does not
relax. What the short form drops is the tour of the interface.

"Newly introduced feature" resets the clock: the first time a chapter uses the
**Evaluate** card, the **Plot** card, *Find equivalent*, Expert Mode or the
**Solve equations** card, that one gets the long form even if it is the fifth
problem in the chapter.

## Naming variables in the text

Roberto, 24 Aug 2026. The app accepts `i_r1` and `ir1` alike and treats them
as the same thing -- verified against `/api/evaluate`, both spellings, every
combination of rounding, units and SI prefixes. The documentation therefore
picks one, and the choice is:

**No underscores.** `ir1`, `vr5`, `pe`, not `i_r1`, `v_r5`, `p_e`. This holds
in prose, in inline code spans, and in anything the reader types -- an
Evaluate expression reads `pr1 + pr2 + pr3 + pe`, and an equation to solve
reads `re = 12000`.

**Except as a real subscript.** Where a quantity is named in ordinary prose,
`v{{sub:r1}}` renders it the way the interface does, as v with a subscript,
and that is better than `vr1`. Use it freely.

**But never inside a version span**, because `{{sub:...}}` closes the
`{{v9|...}}` around it -- see SPEC.md. Inside a span, fall back to the plain
`` `vr5` `` form. This costs nothing, since plain is the default anyway.

**Never raw HTML.** `<sub>` is escaped by the build and lands on the page as
literal text.

## Do not send a reader to Evaluate for arithmetic they can do

Roberto, 24 Aug 2026. Changing a sign is instant for a human, and routing it
through the Evaluate card makes the documentation look like it distrusts the
reader.

Not this:

> pe holds the power consumed by it, we need its opposite. Type `-pe` into
> **Evaluate** and you get 216 mW.

This:

> pe holds the power consumed by it. We need its opposite, which is 216 mW
> delivered.

Evaluate earns its place when the arithmetic is real -- summing four powers
to show they cancel, dividing two answers, evaluating an expression in terms
of unknowns. Negating one number is not that.

## How answers are displayed — the standing rule

Roberto, 24 Aug 2026: **apply this intelligently, per example.**

- **Numerical examples** — *approximate to n significant digits*, n = 3 or 4,
  with **Use SI prefixes in answers** ticked. Quote what that shows: 6 mA,
  6 kOhm, 216 mW.
- **Symbolic examples** — *exact*. An answer that is an expression cannot be
  rounded, and rounding it would be wrong rather than merely ugly.
- **Examples whose answers are exact anyway** — leave the setting alone and
  quote the exact value. Do not tell a reader to change a setting that
  changes nothing.

Where an example needs a different setting from the one before it, say so in
the text. Do not assume the reader still has the setting from three lessons
ago.

Two behaviours of the app to keep in mind, both verified rather than assumed:

- Ticking **Use SI prefixes** moves **Rounding** off *exact* automatically, and
  choosing *exact* unticks SI prefixes. Both changes are announced on screen.
  Prefixed values are decimals, so the two cannot coexist.
- SI prefixes apply to numeric answers only. A symbolic answer is left alone,
  which is why *exact* is the honest setting for the symbolic lessons.

Quote the value the reader will see at the setting the example asks for -- not
the exact value, and not a value at some other precision.

## Values

Versions 7 and 8 carry numbers Roberto computed himself, so **those are the
reference**. Every value quoted in version 9 is computed against the real
solver (`pip install symbulator`, 0.5.0) rather than copied.

**Any disagreement gets reported to him explicitly** — it would mean either
the solver or the original is wrong, and both matter.

Disagreements found so far: *none*.

Lesson 1's circuit, `e1,1,0,36:r1,1,2,1'k:r2,2,3,3'k:r3,3,0,2'k`, computed:

    i_e1 = -3/500   i_r1 = i_r2 = i_r3 = 3/500      (6 mA)
    v_1 = 36   v_2 = 30   v_3 = 12
    v_r1 = 6   v_r2 = 18   v_r3 = 12
    p_r1 = 9/250   p_r2 = 27/250   p_r3 = 9/125     (36, 108, 72 mW)

Worth knowing, and confirmed by running it: **the solver accepts newlines,
colons, or a mix of both** as element separators. So the interface's one
element per line is a presentation choice, not a different syntax, and a
reader pasting a colon-separated example from a printed page is fine.

## State

Counted by `grep`, not by impression.

| | done | left |
|---|---|---|
| `field` fences written | 4 | — |
| `sym 9` fences still to convert | — | 53 |
| `dc("` occurrences remaining | — | 273 |

- **Lesson 1** — opening rewritten: entering the circuit, the two menus, Run
  Symbulator, where the answers appear, separators, and the Circuit card in
  place of storing a variable. The rest of the chapter is untouched.
- **Everything else** — untouched.

## Still to do

1. Finish lesson 1, then lessons 2 to 8, which all have real version 9 content
   built on the wrong premise.
2. Lessons 9 to 13 and the credits: convert from
   `C:\Users\perez\OneDrive\_High Archive\_High Archive - Personal\Documents\Roberto\Creaciones\Symbulator\Websites\2023 Website\docs-page7.html`,
   which has all thirteen lessons. The `TODO:` markers in `src/*.md` name the
   sections and the examples.
3. Carry the 217 imported practice problems into version 9. Roberto asked for
   light instructions there — nothing in them is new to the student.
4. Recover the real figures. The docs reference 247 and **242 are placeholder
   boxes**; the artwork is in `circuit/` beside that HTML, 323 files, matching
   by original code (`as2ex0206.jpg`) rather than by the slugified titles the
   import produced. `docs-page7.html` links each problem to its image, so the
   mapping is recoverable by walking the old HTML. Report the hit rate and
   list the misses rather than leaving silent gaps.
5. Then, and only then, the styling half of objective 2: making inputs and
   outputs on the page look like the interface's. `.code.field` is a first
   pass; the **Results** panel has no equivalent yet.
