# Symbulator documentation — source format

One source tree. Three PDFs and one website are generated from it by `build.py`.

```
book.yaml          book metadata, version table, chapter order, version terms
src/*.md           one file per chapter
assets/            figures (svg/png/jpg), referenced as assets/circuit/foo.svg
tex/symbulator.cls LaTeX class (look of the PDF)
web/               index.php, assets/style.css  (look of the website)
build/             generated — never edit by hand
```

## Chapter file

Each file opens with YAML front matter:

```yaml
---
id: lesson-dc                 # stable, used for anchors, URLs and cross-references
kind: lesson                  # lesson (numbered) | front | back (not numbered)
title: Direct current analysis
versions: [7, 8, 9]           # omit = all versions
absent_note: >                # optional; shown in versions not listed above.
  Symbulator 8 has no Bode plotter...
  If absent_note is omitted, the chapter vanishes from that version entirely
  and the remaining chapters renumber.
updated: 2023-07-08
summary: >
  Learn to describe a circuit and run a DC analysis...   # chapter opener
---
```

## Body

Markdown for the ordinary things:

| Syntax | Meaning |
|---|---|
| `## Title {#label}` | section (numbered `N.M`), optional explicit anchor |
| `### Title` | subsection (not numbered) |
| `- item` / `1. item` | lists |
| `**bold**`, `*italic*`, `` `code` `` | inline |
| `[text](url)` | link |
| `$x^2$`, `$$...$$` | maths (LaTeX in the PDF, KaTeX on the web) |
| `> quoted` | quotation (see below) |
| `\| a \| b \|` | table (see below) |
| `\*`, `\\` | a literal `*` or `\` (see below) |

### Escapes -- and the two characters that are *not* escapes

`\*` is a literal asterisk and `\\` a literal backslash. Nothing else is an
escape sequence. That matters more than it sounds: a backslash is ordinary
content in this book, because the calculator's own namespace is spelled
`s\dc`, `s\tr`, `s\rms`, and a general `\.` escape would silently eat every
one of them.

Use `\*` for the multiplication sign inside an answer quoted back from the
software -- `**{.904\*vs,10952.}**`. Without it the interior `*` breaks the
`**...**` match and the remaining stars re-pair themselves across the rest
of the paragraph: the sentence renders with its italics shifted one span to
the right and a stray `*` left over at the end. Eleven lines in four lessons
were doing exactly that until 2 Sep 2026, because the escape was written in
the sources from the start but never implemented in `build.py`.

### Tables

A pipe table, the ordinary Markdown kind. The rule under the header is what
makes it a table -- without it, a line starting with a pipe is just a
paragraph:

```
| Code | Textbook |
|---|---|
| **AS2** | *Fundamentals of Electric Circuits* (2nd ed.), 2004 |
```

Cells take inline markup. The first column is set tight and the last takes
the slack and wraps, which is the shape every table in this book has: a short
key against a line of prose.

**Leave the header cells empty and there is no header** -- `| | |` over the
rule. (Chapter 13's gain answers used this until 29 Aug 2026, when answers
in tables were converted to the prose form the rest of the book uses (#157);
the feature remains for a genuine label-against-value table.)

Answers are never given in tables: an answer reads as prose, its values in
`{{o:...}}` spans -- see #157 in NEXT_DOCS.md. A table is for reference
material, like the problem-credits table or "type this to find that".

A cell that needs a literal pipe writes `\|`. That matters here more than in
most books: the calculator's "with" operator is a pipe and gets discussed.

Every row must have as many cells as the header. A row that does not stops
the build and names itself, rather than quietly losing a column.

### Quotations

Ordinary Markdown, one `>` per line, with `>` alone between paragraphs:

```
> The masterpiece of TI-89 programming.
>
> — **Alex Astashyn**, EE major, Polytechnic University, New York, USA
```

A final paragraph opening with an em dash (or an en dash) is treated as the
**attribution** and set apart from the words -- smaller and quieter, with
whatever is bold inside it, normally the person's name, in full-strength ink.
Nothing marks it up as an attribution; it is recognised, because a dash is
what a person writing a quotation types anyway.

### Braces — inline commands

| Syntax | Meaning |
|---|---|
| `{{v7\|text}}`, `{{v7,8\|text}}` | show only in those versions |
| `{{!v8\|text}}` | show in every version except those |
| `{{web\|text}}`, `{{pdf\|text}}` | show on the website only, or in the PDFs only |
| `{{t:container}}` | version term from `book.yaml` (`folder` / `document` / `session`) |
| `{{i:resistor}}` | index entry (invisible) |
| `{{ref:lesson-dc}}` | cross-reference, renders as "Lesson 3" or "section 3.2" |
| `{{sub:R1}}` | subscript — `I{{sub:R1}}` renders as I with a subscript R1 |
| `{{o:1.2}}` | a value the software returned |

::: warning A version span cannot contain another brace command
The inline parser closes a `{{v9|...}}` span at the **first** `}}` it meets.
Nest anything inside it — `{{sub:r5}}`, `{{o:0.006}}`, `{{t:machine}}` — and
the span ends early, and the rest of it leaks onto the page as literal
markup: `{{v7,8|The calculator returns` and all. It builds, it renders, and
it is visible only if you read that paragraph on that one version.

Where either half needs markup of its own, use block directives instead:

```
::: only 7,8
The calculator returns {{o:{4.77,7.18}}} meaning I{{sub:R1}} = 4.77 A.
:::
::: only 9
Reading the **current through** line: I{{sub:R1}} = 4.77 A.
:::
```

`build.py --check` fails on a nested span, so this is caught rather than
shipped. It reads whole files, not single lines, because a span routinely
wraps across a line break — an earlier per-line version of the check missed
six of them for exactly that reason.
:::

Never write raw HTML. `<sub>r1</sub>` is escaped by the build and appears on
the page as those literal characters; 37 of them shipped that way on
24 Aug 2026 before anyone noticed.

### Colons — block directives

```
::: tip Pro Tip
Make MAIN your current folder before you simulate.
:::
```

| Directive | Argument | Body |
|---|---|---|
| `tip` `note` `warning` `danger` | box title | contents |
| `figure` | image path | caption |
| `problem` | problem title (e.g. `B11's Example 5.7`) | statement, figure, `answer` |
| `answer` | — | worked solution (only inside `problem`) |
| `practice` | heading | merged practice problems |
| `only` | `7,8` | contents shown only in those versions |
| `not` | `8` | contents hidden in those versions |
| `web` `pdf` | — | contents shown on the website only, or in the PDFs only |
| `address` | the URL, as it should be read | — (empty; still closed with `:::`) |

Directives nest. Close every one with `:::`.

`address` sets a URL on a line of its own, centred, on the input panel's
tint, for an address the reader is meant to share or type -- the split
view's link in the Introduction is the first. Write it as it should be read,
without `https://`; the link target adds it. The text is set verbatim, so
`&` and `?` need no escaping there.

### Code

Calculator input and program output are fenced:

````
```sym 7
s\dc(cir)
```
```sym 9
dc(cir)
```
```out
Done
```
````

`sym` = something the reader types. `out` = something the software returns.
`text` = neither: a listing, such as the contents of a `.cir` input file. It
is set like the others but carries no label, because "type" would be untrue
and "returns" would say Symbulator produced it.
A bare `sym` with no version applies to all versions. Consecutive fences
tagged with different versions are variants of the same instruction: only the
matching one is emitted.

### `field` — typing into a named box

Version 9 has no command line. Every input goes into a labelled field of the
web interface, so the field's name is part of the instruction and belongs in
the markup rather than only in the prose around it:

````
```field 9 Circuit description
e1,1,0,36
r1,1,2,1'k
```
````

The third part of the fence line is the field's name, written exactly as the
interface spells it — **Circuit description**, **Parameters**, **Evaluate**,
**Solve equations**, and so on. It is not optional: `build.py --check` fails a
`field` fence that does not name its field, because an unlabelled box tells the
reader nothing about where to type.

Only `field` takes that third part. A stray word after the version on a `sym`,
`out` or `text` fence is a parse error rather than silent text, so a mistyped
`sym 9 Circuit description` is caught rather than swallowed.

On the web it renders as a panel with the field's name above it, resembling
the box on screen; in the PDFs it is set as typed input like `sym`, since print
has no interface to imitate.

## Build

```
python3 build.py --check    # validate the source and stop
python3 build.py            # everything
python3 build.py --web      # HTML fragments + toc only
python3 build.py --pdf      # LaTeX + PDFs only
python3 build.py --versions 7
```
