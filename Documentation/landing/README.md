# symbulator.com — the front door

The landing page. One static page, no build step, no PHP: edit `index.html`
and `assets/landing.css` directly and upload.

This is **not** part of the documentation build. `build.py` does not touch
this folder and never will. The documentation is a separate site that now
lives on its own host — see below.

## What goes where

| Host | Served from | Built by |
|---|---|---|
| `symbulator.com` | this folder | nothing — upload it as it is |
| `learn.symbulator.com` | `build/web/` | `python3 build.py --web` |

Upload the whole of this folder to the `symbulator.com` document root. The
paths in `index.html` are absolute (`/assets/…`, `/favicon.ico`), so it has
to sit at the root rather than in a subdirectory.

## Files

    index.html                    the page
    9/index.html                  stops /9/ rendering as a file index
    favicon.ico                   16/32/48, from symicon0
    assets/landing.css            the whole stylesheet
    assets/banner.jpg             the masthead, cropped from the slide
    assets/mark.png               the plain scorpion, in the footer
    assets/favicon-32.png         PNG favicon for browsers that prefer one
    assets/apple-touch-icon.png   180x180, for an iOS home-screen icon

## Where it points

    symbulator.pythonanywhere.com   run it online
    install.symbulator.com          install on any device, phones included
    symbulator.com/9/local.zip      download the local package
    learn.symbulator.com            the documentation, ?v=7 / 8 / 9
    pypi.org/project/symbulator     the Python package, for developers
    github.com/Symbulator           the source

`local.zip` is referenced but not included here — it lives at `/9/local.zip`
on the host, and is deliberately kept out of this tree so a 14 MB binary is
not re-uploaded every time the page changes.

`9/index.html` is here, though, and does belong in the upload: without it
the server renders a browsable file index of `/9/`, listing whatever is in
that folder. It is a bare redirect back to the front door, so anyone who
lands on `/9/` by hand gets somewhere useful instead of a blank page. If you
would rather it were truly blank, delete its `<meta http-equiv="refresh">`
and the one line in its `<body>`.

## Colours and type

Both come from `design/tokens.css`, copied into `assets/landing.css` so the
page stands alone with no dependency on the documentation tree. If a token
changes there, change it here too — `python3 build.py --check` validates the
documentation's three copies but knows nothing about this file.

`--gold` (`#d9a521`, `#e8b93a` in dark) was added to the shared palette for
this page's "New!" chip. It is documented in `DESIGN.md` §1.

## Dark mode

Same contract as the documentation site: a `data-theme` attribute on `<html>`,
remembered in `localStorage` under `symbulator-docs-theme`, applied by a small
inline script in `<head>` before first paint so the page never flashes the
wrong theme. Setting the theme on either site carries to the other only if
they share an origin — across subdomains they are independent, which is worth
knowing but not worth fixing.

The navy band stays navy in both themes, matching the interface's header and
DESIGN.md §7.

## One thing left open

The hero's worked example is the voltage divider from the interface's own
syntax reference, with values checked against `symbulator` 0.4.4. The outputs
assume the interface is showing units and SI prefixes (`15 mW`, not `0.015`).
A symbolic example from the interface's Examples dropdown would suit the
headline better — swap it into the `INPUTS`/`OUTPUTS` block when convenient.
