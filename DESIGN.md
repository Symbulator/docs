# Design system — Symbulator

A handoff note, written so that the three faces of Symbulator — the **interface**
(Symbulator 9, the web app), the **website** (this documentation) and the
**PDFs** (the same documentation in print) — can be brought into line with one
another.

Nothing here is a rule imposed on the interface. The palette below was sampled
*from* the interface, so most of it should already look familiar; where the
documentation departs, the reason is given, and the interface is welcome to
depart in the other direction for its own reasons.

Machine-readable copies of everything in this file live in `design/tokens.css`
and `design/tokens.json`.

---

## 1. Palette

Sampled from a screenshot of the interface on 20 August 2026.

| Token | Value | Role in the documentation | Where it came from |
|---|---|---|---|
| `navy` | `#203864` | The top bar; the PDF title | The interface's header band |
| `accent` | `#2f5fa8` | Section numbers, code-block rules, links, cross-references, current version | The interface's buttons and links |
| `accent-bg` | `#e9eff8` | The selected row in the version menu | Derived |
| `accent-dk` | `#24487e` | Pressed and border states | Derived |
| `sky` | `#8ec7f5` | The version numeral in the wordmark; the subtitle on the navy bar | The "Py" in the interface's wordmark |
| `ink` | `#1c2330` | Body text, headings | Shared with the interface |
| `ink-2` | `#545d6d` | Standfirsts, captions, secondary text | Derived |
| `ink-3` | `#858d9c` | Labels, page numbers, muted detail | Derived |
| `paper` | `#ffffff` | Cards, page | Shared |
| `paper-2` | `#f4f6fa` | Page background, output blocks | The interface's background |
| `rule` | `#e2e5ea` | Borders, dividers | Shared |
| `lcd` | `#f2f6fc` | Code blocks — things you type | Derived from `accent` |

### Three colours deliberately outside the blue family

These carry meaning, and meaning needs contrast. If the interface adopts
callouts or status colours, it would be good to use the same three.

| Token | Value | Meaning |
|---|---|---|
| `amber` | `#b7791f` on `#fbf3e2` | **Warning.** The only warm signal in the system. A palette of nothing but blues has no way to raise a hand. |
| `green` | `#2f7d4f` on `#ecf5ef` | **Tip.** Cannot be blue, or a tip is indistinguishable from an ordinary accented heading. |
| `danger` | `#a13030` on `#fdf1f1` | **Caution**, errors, and — set in bold — any value the software returns. |
| `gold` | `#d9a521`, text `#1c2330` | **New.** Added 21 August 2026 for the symbulator.com front door. Deliberately *not* amber: a colour that means both "caution" and "look at this" means neither. Hue 43 against amber's 36, and always a solid chip with dark text on it rather than tinted text, so the two never read as the same device. Dark theme: `#e8b93a`. |

The amber is inherited from the TI-89 keypad, which the earlier palette was
built on. It is the one thing that survived.

Gold has no PDF equivalent, by design — "new" is a screen affordance and
means nothing on a printed page — so it is listed in `TOKEN_ONLY_ON_SCREEN`
in `tools/check_palette.py` rather than in `tex/symbulator.cls`.

---

## 2. Typography

The documentation uses the **IBM Plex** family, loaded from Google Fonts:

| Role | Face | Used for |
|---|---|---|
| Display / UI | IBM Plex Sans | Headings, labels, navigation, standfirsts |
| Body | IBM Plex Serif | Long-form reading only |
| Code | IBM Plex Mono | Circuit descriptions, commands, returned values |

Plex was drawn for engineering and technical documentation, which is the
argument for it here.

The PDFs use the same three faces, installed locally rather than loaded from
Google. `tools/install_plex.sh` puts them in place; without them the LaTeX
class falls back to the TeX Gyre clones and warns, so the build never fails
for want of a font.

**The interface currently differs**, and this is the main thing to reconcile.
It uses the system stack (`-apple-system, "Segoe UI", Roboto, …`) with
`Consolas`/`Menlo` for code. That is a perfectly reasonable choice for an app —
system fonts load instantly and feel native — so the divergence may be
deliberate.

If you do want them to match, the change I would suggest is narrow:

- Adopt **IBM Plex Sans** for the interface's UI text.
- Adopt **IBM Plex Mono** for the circuit description box and the results panel.
  This one matters most: a reader moves between the documentation's examples and
  the app's input box constantly, and the same circuit description should look
  like the same thing in both.
- Do **not** adopt IBM Plex Serif. A serif is right for reading fourteen
  chapters; it is wrong for an application interface.

That gives a shared voice where the two products touch, without making the app
look like a document.

```html
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## 3. Shared conventions worth keeping aligned

**Typed input versus returned output.** The documentation draws a hard
distinction, taken from Roberto's own Word styles: something you type is set in
mono on a pale blue panel with an accent rule down its left edge and a small
`TYPE` label; something the software returns is set on a grey panel labelled
`RETURNS`, and inline returned values are bold in `#a13030`. The interface makes
the same distinction spatially, with `[INPUTS]` and `[OUTPUTS]`. Same idea,
different mechanism — worth being aware of each other.

**Callouts.** Four kinds — tip, note, warning, caution — each with an icon *and*
a word, never colour alone. That is for greyscale printing and for colour-blind
readers. Icons are drawn as inline SVG on the web and TikZ in the PDF; no icon
font, no image files. See `web/assets/style.css` and `tex/symbulator.cls`.

**The version selector.** A native `<details>` disclosure with real links
inside, so it works without JavaScript. Three entries: Symbulator 7 (For TI-89
Titanium), Symbulator 8 (For TI-Nspire CX II CAS), Symbulator 9 (For Python /
SymPy).

**Naming.** The wordmark reads "Symbulator" plus the version numeral, the
numeral in `sky`. The display label lives in one field, `label:` in
`book.yaml`, and flows to the wordmark, the menu, the tooltips and the
narrow-screen fallback. Version 9 was briefly labelled "Py" here; it is now
"9", matching the app's rename.

**Radius and depth.** The documentation uses 3–6px radii and almost no shadow —
one soft shadow on the version menu, nothing else. The interface uses 8–10px
radii and a light card shadow. If these should agree, the app's slightly
rounder, softer treatment is the better one to standardise on; a document page
just has less need for it.

---

## 4. What is in this zip

```
DESIGN.md            this file
design/tokens.css    the palette as CSS custom properties
design/tokens.json   the same, as data
web/assets/style.css the full documentation stylesheet
tex/symbulator.cls   the LaTeX class — the PDF's entire look
build/pdf/           the three PDFs, as built
build/preview/       a few flat HTML pages, openable without a server
guide/how-to-use.pdf how the documentation is built and published
README.md, SPEC.md   the build system and the source markup
src/, book.yaml      the documentation source itself
```

The two files that define the look are `web/assets/style.css` and
`tex/symbulator.cls`. Everything else follows from them.

---

## 5. One task, now done — with one thing to pass on

`TODO-verify-v9-api.md` used to ask for every Symbulator 9 call in the
documentation to be checked against the real package. That has been done
against `symbulator` 0.4.4, and the source corrected; `VERIFIED-v9-api.md` has
the findings, run rather than read.

One item was passed to the interface side and has since been fixed, in
0.4.5: an `equations=` entry written on a derived answer key (`r_*`, `p_*`,
`v_<element>`, `z_*`) used to be absorbed by a same-named phantom unknown and
constrain nothing, leaving the system a parameter short and the answer
correct but parametrized. The engine now stamps the defining equation for
those quantities, so an expert-mode panel in the interface can accept them as
written. The AC power quantities are still refused, deliberately, with an
error that says so.

## 6. Open questions for the interface

1. **Fonts** — adopt IBM Plex Sans and Mono, or keep the system stack? (§2)
2. **The navy bar** — the documentation now carries a full navy band at the top
   of every page, matching the app's header. Over a long document that is a
   heavy element to have fixed on screen. If the app has a view on how much
   navy is right, the documentation should follow it.
3. **The three signal colours** — if the interface grows warnings or hints, are
   the amber, green and red above the right ones to share?
4. **Radius and shadow** — converge on the app's softer treatment, or leave them
   as they are?

---

## 7. Dark Mode (added 21 August 2026)

The website now has the same Dark Mode switch as the interface: a button in
the topbar flips a `data-theme="dark"` attribute on `<html>`, an early inline
script in `<head>` applies a saved preference before first paint (no flash of
the wrong theme), and the preference is kept in `localStorage`. Every colour
in §1 gets a dark counterpart in `design/tokens.css` / `tokens.json`
(`colour-dark`), reusing the interface's own dark values wherever a role is
shared between the two.

Two things were deliberately left alone:

- **The navy topbar stays navy in both themes** — same as the interface's
  header, which is a fixed band rather than a themed one. There is no
  dark variant of `navy` or `sky`.
- **Circuit figures keep a white card behind them in dark mode.** The SVGs
  are line art on a transparent background, drawn to be read on paper; rather
  than recolour them, dark mode frames them in a small white panel, the way a
  printed figure would look pasted onto a dark page.

One new token pair, `inverse-bg` / `inverse-ink`, was added for the one or two
elements — the primary button, the skip-to-content link — that want a fixed
dark chip regardless of theme. In light mode `inverse-bg` equals `ink`
exactly (so light mode is pixel-identical to before); dark mode gives it its
own value, since `ink` itself is now light and can no longer serve that role.
