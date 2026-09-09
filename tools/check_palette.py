#!/usr/bin/env python3
"""Cross-check the palette across its three independent copies.

design/tokens.json is meant to be the canonical palette -- the note in
DESIGN.md says as much -- but nothing enforced that until now. Three files
each hard-code their own copy of the same colours:

    design/tokens.json      the canonical values (also design/tokens.css,
                             generated from the same source by hand today)
    web/assets/style.css    the :root custom properties, --token-name: #hex
    tex/symbulator.cls      \\definecolor{name}{HTML}{hex} for the PDFs

There is no build step that generates two of these from the third, so a
colour changed in one silently drifts out of sync with the other two. This
script is the guard rail: it parses all three, maps the LaTeX class's
shorter/renamed identifiers onto the token names, and reports any value
that disagrees with tokens.json, or that exists in one file with no
corresponding entry anywhere else.

Run standalone (`python3 tools/check_palette.py`) or via `build.py --check`,
which calls check_palette() and folds any mismatches into the same problem
list as every other validation.
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS_JSON = os.path.join(ROOT, "design", "tokens.json")
STYLE_CSS = os.path.join(ROOT, "web", "assets", "style.css")
SYMBULATOR_CLS = os.path.join(ROOT, "tex", "symbulator.cls")

# The LaTeX class can't use hyphens in \definecolor names and renamed a
# couple of tokens outright when it was written. This is the one place
# that mapping needs to be spelled out -- keep it current if either side
# adds or renames a colour.
CLS_TO_TOKEN = {
    "navy": "navy",
    "accent": "accent",
    "accentbg": "accent-bg",
    "sky": "sky",
    "ink": "ink",
    "slate": "ink-2",       # renamed in the class
    "rule": "rule",
    "amber": "amber",
    "amberbg": "amber-bg",
    "green": "green",
    "greenbg": "green-bg",
    "danger": "danger",
    "dangerbg": "danger-bg",
    "answer": "answer",
    "uicard": "ui-card",
    "uicontrol": "ui-control",
    "lcd": "lcd",
    "panel": "paper-2",     # renamed in the class
}

# Tokens that intentionally have no PDF equivalent -- the print side uses
# fewer shades than the screen side. Not a mismatch, just a narrower palette.
# inverse-bg/inverse-ink are a fixed-contrast UI chip (the primary button,
# the skip-to-content link) with no printed equivalent to speak of.
# gold/gold-ink mark something as new -- a screen affordance with no
# meaning on a printed page, so the PDF has no equivalent by design.
TOKEN_ONLY_ON_SCREEN = {"accent-dk", "ink-3", "paper", "rule-2", "lcd-edge",
                        "inverse-bg", "inverse-ink", "gold", "gold-ink"}

# Tokens with no Dark Mode value at all, by design -- the topbar (navy) and
# its keyline (sky) stay the same fixed band in both themes, same as the
# interface's own header, so there is nothing in tokens.json's "colour-dark"
# for these and style.css's dark block correctly leaves them unset too.
NO_DARK_VARIANT = {"navy", "sky"}


def load_tokens() -> dict[str, str]:
    with open(TOKENS_JSON) as f:
        data = json.load(f)
    return {k: v.lower() for k, v in data["colour"].items()}


def load_dark_tokens() -> dict[str, str]:
    with open(TOKENS_JSON) as f:
        data = json.load(f)
    dark = data.get("colour-dark", {})
    return {k: v.lower() for k, v in dark.items() if k != "note"}


def _extract_block(text: str, selector_re: str) -> str:
    """Return the body of the first `selector { ... }` block matching
    `selector_re`, or '' if not found. Good enough for these two flat,
    single-level blocks -- not a general CSS parser."""
    m = re.search(selector_re + r"\s*\{", text)
    if not m:
        return ""
    start = m.end()
    depth = 1
    i = start
    while i < len(text) and depth:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    return text[start:i - 1]


def parse_css_vars(path: str) -> dict[str, str]:
    """The :root block's custom properties -- the light (default) palette."""
    with open(path) as f:
        text = f.read()
    block = _extract_block(text, r":root")
    out = {}
    for m in re.finditer(r"--([a-z0-9-]+):\s*(#[0-9a-fA-F]{3,6})\s*;", block):
        out[m.group(1)] = m.group(2).lower()
    return out


def parse_dark_css_vars(path: str) -> dict[str, str]:
    """The html[data-theme="dark"] block's custom properties -- parsed
    separately from :root so a light and dark value for the same token
    name (e.g. --ink) don't collide in one dict."""
    with open(path) as f:
        text = f.read()
    block = _extract_block(text, r'html\[data-theme=(?:"dark"|\'dark\')\]')
    out = {}
    for m in re.finditer(r"--([a-z0-9-]+):\s*(#[0-9a-fA-F]{3,6})\s*;", block):
        out[m.group(1)] = m.group(2).lower()
    return out


def parse_cls_colors(path: str) -> dict[str, str]:
    with open(path) as f:
        text = f.read()
    out = {}
    for m in re.finditer(r"\\definecolor\{([a-zA-Z0-9]+)\}\{HTML\}\{([0-9a-fA-F]{6})\}", text):
        out[m.group(1)] = "#" + m.group(2).lower()
    return out


def check_palette(verbose: bool = False) -> list[str]:
    """Returns a list of human-readable problems; empty means everything
    agrees. Safe to call even if one of the three files is missing --
    reports that as a problem too, rather than raising."""
    problems: list[str] = []

    for label, path in (("tokens.json", TOKENS_JSON), ("style.css", STYLE_CSS),
                         ("symbulator.cls", SYMBULATOR_CLS)):
        if not os.path.isfile(path):
            problems.append(f"palette: {label} not found at {path}")
    if problems:
        return problems

    tokens = load_tokens()
    css_vars = parse_css_vars(STYLE_CSS)
    cls_colors = parse_cls_colors(SYMBULATOR_CLS)

    # 1. Every token should appear in style.css with the same value,
    #    unless it's explicitly screen-only in the .cls (still required in
    #    the CSS -- the CSS is the full palette).
    for name, value in tokens.items():
        css_value = css_vars.get(name)
        if css_value is None:
            problems.append(f"palette: --{name} is in tokens.json but missing from style.css")
        elif css_value != value:
            problems.append(
                f"palette: --{name} = {css_value} in style.css, "
                f"but tokens.json says {value}"
            )

    # 2. Every .cls colour should map to a known token and match its value.
    for cls_name, cls_value in cls_colors.items():
        token_name = CLS_TO_TOKEN.get(cls_name)
        if token_name is None:
            problems.append(
                f"palette: \\definecolor{{{cls_name}}} in symbulator.cls has no "
                f"entry in CLS_TO_TOKEN (tools/check_palette.py) -- add one, or "
                f"if it's meant to be a class-only colour, ignore it explicitly"
            )
            continue
        token_value = tokens.get(token_name)
        if token_value is None:
            problems.append(
                f"palette: symbulator.cls's {cls_name} maps to token "
                f"'{token_name}', which doesn't exist in tokens.json"
            )
        elif cls_value != token_value:
            problems.append(
                f"palette: {cls_name} = {cls_value} in symbulator.cls, "
                f"but tokens.json's {token_name} = {token_value}"
            )

    # 3. Every token mapped from the .cls side should actually be there --
    #    catches a colour quietly dropped from the class.
    mapped_from_cls = set(CLS_TO_TOKEN.values())
    for name in tokens:
        if name in TOKEN_ONLY_ON_SCREEN:
            continue
        if name not in mapped_from_cls:
            problems.append(
                f"palette: token '{name}' has no symbulator.cls colour at all "
                f"(not in TOKEN_ONLY_ON_SCREEN and not in CLS_TO_TOKEN's values)"
            )

    # 4. Dark Mode: style.css's html[data-theme="dark"] block should match
    #    tokens.json's "colour-dark", token for token -- checked completely
    #    separately from steps 1-3 above (a light and dark value for the
    #    same --name, e.g. --ink, are two different things, not a
    #    mismatch). There is no dark-mode equivalent in the PDF, so this
    #    has nothing to do with symbulator.cls.
    dark_tokens = load_dark_tokens()
    dark_css_vars = parse_dark_css_vars(STYLE_CSS)
    for name, value in dark_tokens.items():
        css_value = dark_css_vars.get(name)
        if css_value is None:
            problems.append(
                f"palette: --{name} is in tokens.json's colour-dark but "
                f"missing from style.css's html[data-theme=\"dark\"] block"
            )
        elif css_value != value:
            problems.append(
                f"palette: --{name} = {css_value} in style.css's dark block, "
                f"but tokens.json's colour-dark says {value}"
            )
    for name in dark_css_vars:
        if name not in dark_tokens:
            problems.append(
                f"palette: --{name} is in style.css's html[data-theme=\"dark\"] "
                f"block but missing from tokens.json's colour-dark"
            )
    # Every token that *does* get a dark variant should exist in the light
    # palette too (nothing dark-only), and every light token should either
    # have a dark variant or be explicitly exempted as a fixed band.
    for name in tokens:
        if name in NO_DARK_VARIANT:
            continue
        if name not in dark_tokens:
            problems.append(
                f"palette: token '{name}' has no Dark Mode value in "
                f"tokens.json's colour-dark (add one, or add '{name}' to "
                f"NO_DARK_VARIANT in tools/check_palette.py if it's meant "
                f"to stay the same in both themes)"
            )

    if verbose:
        print(f"palette: checked {len(tokens)} token(s), "
              f"{len(css_vars)} CSS var(s), {len(cls_colors)} .cls colour(s), "
              f"{len(dark_tokens)} dark token(s)")

    return problems


def main() -> int:
    problems = check_palette(verbose=True)
    for p in problems:
        print("  " + p, file=sys.stderr)
    print(f"check_palette: {len(problems)} problem(s)" if problems else "check_palette: clean")
    return len(problems)


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 1)
