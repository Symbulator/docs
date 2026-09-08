#!/usr/bin/env python3
"""
Static preview of the website, for looking at it without a PHP server.

The real site is index.php, which reads the same content/ folder. This script
writes flat .html files you can open by double-clicking:

    python3 tools/static_preview.py
    open build/preview/v7-lesson-dc.html

Preview only. Anything shipped to the server comes from build/web.
"""
import base64
import html
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, "build", "web")
OUT = os.path.join(ROOT, "build", "preview")


def e(s):
    return html.escape(str(s), quote=True)


def link(v, p=""):
    return f"v{v}-{p or 'home'}.html"


# Same anti-flash mechanism as web/index.php: applied before the stylesheet
# is even parsed, so a saved Dark Mode preference takes effect before first
# paint. Same storage key as index.php, so a preference set on the live site
# carries over to these flat preview files and back.
THEME_ANTIFLASH = """<script>
(function () {
  var saved = null;
  try { saved = localStorage.getItem('symbulator-docs-theme'); } catch (e) {}
  if (saved === 'dark') { document.documentElement.setAttribute('data-theme', 'dark'); }
})();
</script>"""


def head(title, v, subtitle, home=False):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
{THEME_ANTIFLASH}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&amp;family=IBM+Plex+Sans:wght@400;500;600;700&amp;family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&amp;display=swap" rel="stylesheet">
<link rel="icon" href="assets/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta name="theme-color" content="#203864">
<style>__BANNER_CSS__</style>
<style>__CSS__</style>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
</head><body class="v{v}{' home' if home else ''}">"""


# Same wiring as web/index.php's #theme-toggle script: the early inline
# script in head() already applied a saved preference before first paint,
# so this only flips the attribute, persists it, and updates the icon/label.
THEME_TOGGLE_SCRIPT = """<script>
(function () {
  var btn = document.getElementById('theme-toggle');
  if (!btn) return;
  var ICON_MOON = '<svg viewBox="0 0 24 24" fill="#8ec7f5" aria-hidden="true"><path d="M20.4 14.7A8.5 8.5 0 1 1 9.3 3.6a7 7 0 1 0 11.1 11.1Z"/></svg>';
  var ICON_SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="#8ec7f5" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.4M12 19.1v2.4M4.6 4.6l1.7 1.7M17.7 17.7l1.7 1.7M2.5 12h2.4M19.1 12h2.4M4.6 19.4l1.7-1.7M17.7 6.3l1.7-1.7"/></svg>';
  function isDark() { return document.documentElement.getAttribute('data-theme') === 'dark'; }
  function sync() {
    var dark = isDark();
    btn.innerHTML = dark ? ICON_SUN : ICON_MOON;
    var label = dark ? 'Switch to light mode' : 'Switch to dark mode';
    btn.setAttribute('aria-label', label);
    btn.title = label;
  }
  sync();
  btn.addEventListener('click', function () {
    var nextDark = !isDark();
    if (nextDark) { document.documentElement.setAttribute('data-theme', 'dark'); }
    else { document.documentElement.removeAttribute('data-theme'); }
    try { localStorage.setItem('symbulator-docs-theme', nextDark ? 'dark' : 'light'); } catch (e) {}
    sync();
  });
})();
</script>"""

TOC_SCRIPT = """<script>
(function () {
  var toc = document.getElementById('toc');
  if (!toc) return;
  var KEY = 'symbulator-docs-toc', saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  if (saved === 'closed') { toc.open = false; }
  else if (saved !== 'open' && window.matchMedia('(max-width: 62rem)').matches) {
    toc.open = false;
  }
  toc.addEventListener('toggle', function () {
    try { localStorage.setItem(KEY, toc.open ? 'open' : 'closed'); } catch (e) {}
  });
})();
</script>"""

TAIL = """
""" + THEME_TOGGLE_SCRIPT + """
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
 onload="renderMathInElement(document.body,{delimiters:[
  {left:'\\\\[',right:'\\\\]',display:true},
  {left:'\\\\(',right:'\\\\)',display:false}]});"></script>
</body></html>"""


def topbar(book, toc, v, page, ids):
    items = []
    for n, vm in book["versions"].items():
        cur = ' aria-current="true" class="is-current"' if n == str(v) else ""
        target = page if page in ids else ""
        items.append(
            f'<li><a href="{link(n, target)}"{cur}>'
            f'<span class="v-name">Symbulator {e(vm["label"])}</span>'
            f'<span class="v-plat">For {e(vm["platform"])}</span></a></li>')
    chev = ('<svg class="chev" viewBox="0 0 16 16" aria-hidden="true" fill="none"'
            ' stroke="currentColor" stroke-width="1.6" stroke-linecap="round"'
            ' stroke-linejoin="round"><path d="M4 6.5 8 10.5l4-4"/></svg>')
    # Same markup as web/index.php's topbar-right: the version picker plus a
    # Dark Mode toggle button, starting on the moon icon (light mode default);
    # TAIL's script swaps the icon/label to match a restored dark preference.
    theme_toggle = (
        '<button type="button" id="theme-toggle" class="theme-toggle" '
        'aria-label="Switch to dark mode" title="Switch to dark mode">'
        '<svg viewBox="0 0 24 24" fill="#8ec7f5" aria-hidden="true">'
        '<path d="M20.4 14.7A8.5 8.5 0 1 1 9.3 3.6a7 7 0 1 0 11.1 11.1Z"/></svg>'
        '</button>'
    )
    # Same markup as web/index.php: the shared lockup from the shared banner.css
    # in .topbar, then a second .subbar band carrying this site's own
    # controls -- a row of plain links, the version picker and the Dark Mode
    # toggle. Keep the two files in step; the banner is meant to exist once,
    # and THIS FILE IS THE ONE THAT GETS FORGOTTEN, because it generates its
    # own markup rather than reading index.php. It was left emitting a
    # superseded header for a day once already.
    ribbon = ('<nav>'
              f'<a href="symbulator-v{v}.pdf">Download as PDF</a>'
              '<a href="https://symbulator.pythonanywhere.com">Online App</a>'
              '</nav>')
    return (f'<header class="topbar"><div class="topbar-inner">'
            '<div class="header-brand">'
            '<a class="header-logo-link" href="https://symbulator.com" '
            'aria-label="Symbulator home">'
            '<img src="assets/logo.png" alt="Symbulator logo" class="header-logo">'
            '</a>'
            f'<a class="header-title" href="{link(v)}">'
            # The β is temporary: version 9 is in beta (Roberto,
            # 28 Aug 2026); only the 9 carries it, matching index.php.
            f'<p class="brand-name">Symbulator <span class="vnum">{e(toc["label"])}'
            f'{"β" if str(toc["label"]) == "9" else ""}</span></p>'
            # Static, matching web/index.php, the landing page and the
            # app. This generator does not read index.php, so a change
            # to the lockup there has to be made here as well or the
            # preview quietly shows the superseded one.
            '<p class="brand-sub">the best portable symbolic simulator of linear circuits</p>'
            # The property mark (#135): one word, two spellings,
            # exactly one shown -- see banner.css.
            '<p class="property-mark property-mark-slot">Documentation</p>'
            '</a></div>'
            '<span class="property-mark property-mark-top">Documentation</span>'
            '</div></header>'
            f'<div class="subbar"><div class="subbar-inner">{ribbon}'
            f'<details class="versions" id="version-picker">'
            f'<summary aria-label="Choose a version">'
            f'<span class="vkey-full">Symbulator {e(toc["label"])}</span>'
            f'<span class="vkey-num">{e(toc["label"])}</span>{chev}</summary>'
            f'<ul class="version-list">{"".join(items)}</ul>'
            f'</details><span class="subbar-spacer"></span>'
            f'{theme_toggle}</div></div>')


def sidebar(toc, v, page):
    items = []
    for c in toc["chapters"]:
        cls = ("is-current" if c["id"] == page else "") + \
              ("" if c["present"] else " is-absent")
        secs = ""
        if c["id"] == page and c["sections"]:
            secs = "<ul class='sections'>" + "".join(
                f'<li><a href="#{e(s["anchor"])}">'
                f'<span class="secno">{e(s["number"])}</span> {e(s["title"])}</a></li>'
                for s in c["sections"]) + "</ul>"
        # No eyebrow where there is no lesson number: printing the title in
        # that slot repeated it, as "Introduction Introduction".
        eyebrow = (f'<span class="ch-eyebrow">{e(c["eyebrow"])}</span>'
                   if c["eyebrow"] else "")
        items.append(
            f'<li class="{cls}"><a href="{link(v, c["id"])}">'
            f'{eyebrow}'
            f'<span class="ch-title">{e(c["title"])}</span></a>{secs}</li>')
    items.append(f'<li><a href="{link(v, "index")}">'
                 f'<span class="ch-title">Index</span></a></li>')
    chev = ('<svg class="toc-chev" viewBox="0 0 16 16" aria-hidden="true"'
            ' fill="none" stroke="currentColor" stroke-width="1.8"'
            ' stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M4 6.5 8 10.5l4-4"/></svg>')
    # Same disclosure as web/index.php: Contents folds away, and the small
    # script right after it restores the reader's last choice.
    return ('<nav class="sidebar" aria-label="Contents">'
            '<details class="toc" id="toc" open>'
            f'<summary class="sidebar-title">Contents{chev}</summary>'
            f'<ol class="chapters">{"".join(items)}</ol>'
            '</details></nav>' + TOC_SCRIPT)


def build():
    book = json.load(open(os.path.join(WEB, "content", "book.json")))
    os.makedirs(OUT, exist_ok=True)
    for name in ("assets",):
        shutil.copytree(os.path.join(WEB, name), os.path.join(OUT, name),
                        dirs_exist_ok=True)
    css = open(os.path.join(WEB, "assets", "style.css"), encoding="utf-8").read()
    banner_css = open(os.path.join(WEB, "assets", "banner.css"),
                      encoding="utf-8").read()

    def finish(markup):
        """Inline the stylesheet and figures so a single file renders alone."""
        markup = markup.replace("__BANNER_CSS__", banner_css)
        markup = markup.replace("__CSS__", css)

        # build.py writes site paths root-absolute, because index.php is
        # served from both /?v=9&p=lesson-dc and /9/lesson-dc and only an
        # absolute path resolves the same under both. The preview is the one
        # consumer that must undo it: these are flat files opened from disk,
        # where "/assets/x.svg" points at the root of the drive.
        markup = markup.replace('src="/assets/', 'src="assets/')

        INLINE_LIMIT = 120 * 1024      # bigger figures load from assets/

        def datauri(m):
            path = os.path.join(WEB, m.group(1))
            if not os.path.isfile(path):
                return m.group(0)
            if os.path.getsize(path) > INLINE_LIMIT:
                return m.group(0)
            blob = base64.b64encode(open(path, "rb").read()).decode()
            mime = "image/svg+xml" if path.endswith(".svg") else "image/png"
            return f'src="data:{mime};base64,{blob}"'

        return re.sub(r'src="(assets/[^"]+)"', datauri, markup)

    for v in book["versions"]:
        toc = json.load(open(os.path.join(WEB, "content", f"v{v}", "toc.json")))
        # #342: the tab says which property this is, as web/index.php does.
        # This generator writes its own <head>, so a change there has to be
        # made here too or the preview drifts from the site again.
        site_name = toc["name"] + " Documentation"
        ids = [c["id"] for c in toc["chapters"]]

        # landing page
        def _card(c):
            absent_cls = "" if c["present"] else ' class="is-absent"'
            eyebrow = (f'<p class="card-eyebrow">{e(c["eyebrow"])}</p>'
                       if c["eyebrow"] else "")
            return (
                f'<li{absent_cls}>'
                f'<a href="{link(v, c["id"])}">{eyebrow}'
                f'<h2>{e(c["title"])}</h2>'
                f'<p class="card-summary">{e(c["summary"])}</p></a></li>'
            )

        cards = "".join(_card(c) for c in toc["chapters"])
        page = (head(site_name, v, book["subtitle"], home=True)
                + topbar(book, toc, v, "", ids)
                + '<div class="shell"><main id="main">'
                + f'<ol class="chapter-cards">{cards}</ol>'
                + "</main></div>" + TAIL)
        open(os.path.join(OUT, link(v)), "w", encoding="utf-8").write(finish(page))

        # chapters
        for i, c in enumerate(toc["chapters"]):
            body = open(os.path.join(WEB, "content", f"v{v}", c["id"] + ".html"),
                        encoding="utf-8").read()
            # Cross-references arrive as href="/9/lesson-ac"; reduce them to
            # the bare chapter id, which the loop below turns into this
            # preview's own flat filename. The old query form is still
            # handled so a preview built over an older build/web/ works.
            body = body.replace(f'href="/{v}/', 'href="')
            body = body.replace(f'?v={v}&amp;p=', "").replace(".html#", "#")
            for other in ids:                       # rewrite cross-reference hrefs
                body = body.replace(f'href="{other}"', f'href="{link(v, other)}"')
                body = body.replace(f'href="{other}#', f'href="{link(v, other)}#')
            prev_c = toc["chapters"][i - 1] if i else None
            next_c = toc["chapters"][i + 1] if i + 1 < len(toc["chapters"]) else None
            pager = '<nav class="pager">'
            if prev_c:
                pager += (f'<a class="pager-prev" href="{link(v, prev_c["id"])}">'
                          f'<span>Previous</span>{e(prev_c["title"])}</a>')
            if next_c:
                pager += (f'<a class="pager-next" href="{link(v, next_c["id"])}">'
                          f'<span>Next</span>{e(next_c["title"])}</a>')
            pager += "</nav>"
            page = (head(c["title"] + " — " + site_name, v, book["subtitle"])
                    + topbar(book, toc, v, c["id"], ids)
                    + '<div class="shell">' + sidebar(toc, v, c["id"])
                    + f'<main id="main"><article class="chapter">{body}</article>'
                    + pager + "</main></div>"
                    + '<footer class="foot"><p>Symbulator — '
                    + f'{e(toc["name"])}, {e(toc["platform"])}. Documentation by '
                    + 'Roberto Perez-Franco. MIT licence.</p></footer>'
                    + TAIL)
            open(os.path.join(OUT, link(v, c["id"])), "w",
                 encoding="utf-8").write(finish(page))

        # index
        entries = "".join(
            f'<li><span class="ix-term">{e(term)}</span>' +
            "".join(f'<a href="{link(v, spot.split("#")[0])}#{spot.split("#")[1]}">'
                    f'{n + 1}</a>' for n, spot in enumerate(spots)) + "</li>"
            for term, spots in toc["index"].items()) or "<li>No entries yet.</li>"
        page = (head("Index — " + site_name, v, book["subtitle"])
                + topbar(book, toc, v, "index", ids)
                + '<div class="shell">' + sidebar(toc, v, "index")
                + '<main id="main"><article class="chapter">'
                  '<header class="chapter-head"><p class="eyebrow">Index</p>'
                  '<h1>Index</h1></header>'
                  f'<ul class="book-index">{entries}</ul></article></main></div>'
                + TAIL)
        open(os.path.join(OUT, link(v, "index")), "w",
             encoding="utf-8").write(finish(page))

    print("preview:", OUT)


if __name__ == "__main__":
    if not os.path.isdir(WEB):
        sys.exit("run build.py first")
    build()
