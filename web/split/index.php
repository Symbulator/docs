<?php
// #224: the split view. Documentation on the left, the live app on the
// right, and every worked problem in the tutorial loadable into the
// right pane in one click.
//
// This page is a shell and nothing else. It holds no documentation and
// no app -- both panes are iframes onto the real sites, which stay the
// only sources of truth. Nothing here needs redeploying when either of
// them changes.
//
// It is PHP rather than plain HTML for one reason: the stylesheet stamp.
// learn.symbulator.com serves assets with a week-long max-age, so a
// returning visitor keeps a stale stylesheet unless the URL changes when
// the file does; index.php solves that with filemtime() at request time
// and this page borrows the same trick rather than inventing a second
// one. See the note above asset() in ../index.php.
//
// It lives at /split/ as a real directory, so .htaccess needs no rule
// for it -- the rewrite there only claims ^[789].

function asset(string $name): string {
    $path = __DIR__ . '/../assets/' . $name;
    $v = is_file($path) ? substr(md5_file($path), 0, 8) : '0';
    return '/assets/' . $name . '?v=' . $v;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Symbulator 9 — split view</title>
<meta name="description" content="The Symbulator 9 tutorial beside the live app, with every worked problem loadable in one click.">
<script>
// Before first paint, as on every other page of this site, and reading
// the same key so the split view opens in the theme the reader chose.
(function () {
  var saved = null;
  try { saved = localStorage.getItem('symbulator-docs-theme'); } catch (e) {}
  if (saved === 'dark') { document.documentElement.setAttribute('data-theme', 'dark'); }
})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/favicon-32.png" type="image/png" sizes="32x32">
<meta name="theme-color" content="#203864">
<!-- style.css is loaded for its design tokens: the split view paints
     itself from the same --navy, --ink and --rule as the rest of the
     site rather than restating any hex of its own. -->
<link rel="stylesheet" href="<?= asset('style.css') ?>">
<style>
  html, body { height: 100%; }
  body {
    margin: 0; display: flex; flex-direction: column;
    background: var(--paper-2); color: var(--ink);
    font-family: var(--sans); overflow: hidden;
  }

  /* --- the bar -------------------------------------------------------
     Deliberately not the shared two-band lockup. That banner is a tall
     navy block designed to open a page; here every pixel it took would
     come out of the two panes, which are the entire point of the view.
     One slim band, the same navy, and the wordmark links home. */
  .splitbar {
    position: relative;
    flex: none; display: flex; align-items: center; gap: 0.9rem;
    background: var(--navy); color: #fff;
    padding: 0.4rem 0.85rem; font-size: 0.86rem;
  }
  .splitbar a { color: #fff; }
  /* #231: the wordmark is one colour -- the sky -- and the numeral is
     the contrasting element. It used to be the other way round by
     accident: a span carried over from another lockup coloured
     "bulator" and left "Sym" white, splitting the word down the middle.
     The colour has to be stated here rather than left to `.splitbar a`
     above, which paints every link in the bar white. */
  .splitbar .mark {
    font-weight: 700; letter-spacing: 0.01em; text-decoration: none;
    white-space: nowrap; flex: none;
    color: var(--sky, #8ec7f5);
  }
  .splitbar .mark .vnum { color: #fff; }
  /* #304: the position badge is a button that opens the lesson menu --
     the shell has no table of contents, and this is where a reader
     looks to see where they are. Reset to look exactly as the badge
     did, plus a caret. */
  .splitbar .wherewrap { position: relative; min-width: 0; display: flex; }
  .splitbar button.where {
    font: inherit; background: none; border: 0; padding: 0; margin: 0;
    cursor: pointer; text-align: left;
    color: var(--sky); font-size: 0.78rem; letter-spacing: 0.09em;
    text-transform: uppercase; white-space: nowrap;
    overflow: hidden; text-overflow: ellipsis; min-width: 0;
  }
  .splitbar button.where::after { content: " \25BE"; opacity: 0.8; }
  .splitbar button.where:hover, .splitbar button.where:focus-visible { color: #fff; }
  .splitbar button.where:focus-visible { outline: 2px solid var(--sky); outline-offset: 2px; }
  .menu {
    position: absolute; top: 100%; left: 0.85rem; z-index: 20;
    max-width: calc(100vw - 1.7rem);
    margin: 0.35rem 0 0; padding: 0.3rem 0; list-style: none;
    background: var(--paper); color: var(--ink);
    border: 1px solid var(--rule); border-radius: 6px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    min-width: min(17rem, calc(100vw - 1.7rem)); max-height: 72vh; overflow: auto;
    font-size: 0.86rem; letter-spacing: 0; text-transform: none;
  }
  .menu[hidden] { display: none; }
  .menu button {
    display: block; width: 100%; text-align: left; font: inherit;
    padding: 0.38rem 0.85rem; background: none; border: 0;
    color: var(--ink); cursor: pointer; white-space: nowrap;
    overflow: hidden; text-overflow: ellipsis;
  }
  /* #306 (Roberto, 7 Sep 2026): on a phone the badge is hidden, so a
     Contents button between the wordmark and the tabs opens the same
     menu. Drawn like the tabs' buttons, and only where the badge is not. */
  .splitbar .contents {
    display: none; font: inherit; font-size: 0.8rem; cursor: pointer;
    background: transparent; color: #fff;
    border: 1px solid rgba(255,255,255,0.45); border-radius: 3px;
    padding: 0.16rem 0.6rem; white-space: nowrap; flex: none;
  }
  .splitbar .contents[aria-expanded="true"] { background: #fff; color: var(--navy); }
  .menu button:hover, .menu button:focus-visible { background: var(--paper-2); outline: 0; }
  .menu button[aria-current="true"] { font-weight: 600; color: var(--accent); }
  .menu .num {
    display: inline-block; min-width: 4.6em; margin-right: 0.6rem; color: var(--ink-3);
    font-size: 0.78rem; letter-spacing: 0.06em; text-transform: uppercase;
  }
  .splitbar .spacer { flex: 1 1 auto; }
  .splitbar .tabs { flex: none; }
  /* Below the tab breakpoint the bar is wordmark + tabs; the position
     line gives up its space rather than pushing either onto a second
     line, which is what a wrapped lockup was doing at 375px. */
  @media (max-width: 480px) {
    .splitbar { gap: 0.5rem; padding: 0.4rem 0.55rem; }
    .splitbar .wherewrap { display: none; }
    .splitbar .contents { display: inline-block; }
    .menu { left: 0.55rem; }
  }
  .splitbar .plain {
    font-size: 0.8rem; opacity: 0.92; white-space: nowrap;
  }
  @media (max-width: 700px) { .splitbar .plain { display: none; } }

  /* --- the tabs, on a narrow screen ----------------------------------- */
  .tabs { display: none; gap: 0.3rem; }
  .tabs button {
    font: inherit; font-size: 0.8rem; cursor: pointer;
    background: transparent; color: #fff;
    border: 1px solid rgba(255,255,255,0.45); border-radius: 3px;
    padding: 0.16rem 0.6rem;
  }
  .tabs button[aria-pressed="true"] {
    background: #fff; color: var(--navy); border-color: #fff; font-weight: 600;
  }

  /* --- the panes ------------------------------------------------------ */
  .panes { flex: 1 1 auto; display: flex; min-height: 0; }
  .pane { min-width: 0; position: relative; background: var(--paper); }
  .pane.docs { flex: 0 0 auto; }
  .pane.app  { flex: 1 1 auto; }
  .pane iframe { width: 100%; height: 100%; border: 0; display: block; }

  .divider {
    flex: 0 0 6px; cursor: col-resize; background: var(--rule);
    position: relative; touch-action: none;
  }
  .divider::after {
    content: ""; position: absolute; inset-block: 0;
    inset-inline-start: 2px; width: 2px; background: var(--ink-3);
    opacity: 0.35;
  }
  .divider:hover::after, .divider:focus-visible::after { opacity: 0.8; }
  .divider:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
  /* While a drag is in flight the panes must not swallow the pointer --
     an iframe eats mousemove, and the divider would stick to the cursor
     the moment it crossed one. */
  body.dragging iframe { pointer-events: none; }
  body.dragging { cursor: col-resize; }

  /* --- narrow: one pane at a time ------------------------------------- */
  @media (max-width: 820px) {
    .tabs { display: flex; }
    .divider { display: none; }
    .pane { flex: 1 1 auto !important; }
    body[data-show="docs"] .pane.app  { display: none; }
    body[data-show="app"]  .pane.docs { display: none; }
  }

  .nojs { padding: 1rem; font-size: 0.9rem; }
</style>
</head>
<body data-show="docs">

<div class="splitbar">
  <a class="mark" href="/9/">Symbulator <span class="vnum">9</span></a>
  <button type="button" class="contents" id="contentsBtn" aria-haspopup="menu"
          aria-expanded="false" aria-controls="lessonMenu">Contents</button>
  <span class="wherewrap">
    <button type="button" class="where" id="where" aria-haspopup="menu"
            aria-expanded="false" aria-controls="lessonMenu"
            title="Go to a lesson">Documentation</button>
  </span>
  <ul class="menu" id="lessonMenu" role="menu" hidden></ul>
  <span class="spacer"></span>
  <span class="plain" id="hint">Links in the left pane load the circuit on the right.</span>
  <span class="tabs">
    <button type="button" id="tabDocs" aria-pressed="true">Docs</button>
    <button type="button" id="tabApp"  aria-pressed="false">App</button>
  </span>
</div>

<div class="panes" id="panes">
  <div class="pane docs" id="paneDocs" style="flex-basis:50%">
    <iframe id="docsFrame" title="Symbulator 9 documentation"
            src="/9/lesson-dc"></iframe>
  </div>
  <div class="divider" id="divider" role="separator" aria-orientation="vertical"
       tabindex="0" aria-label="Resize the two panes"></div>
  <div class="pane app" id="paneApp">
    <iframe id="appFrame" title="The Symbulator 9 app"
            src="https://symbulator.pythonanywhere.com/"
            allow="clipboard-write"></iframe>
  </div>
</div>

<script>
// -------------------------------------------------------------------------
// #224: the split view's shell.
//
// The postMessage protocol, in full. Two messages, one each way:
//
//   docs pane -> shell   { from: 'symbulator-docs', type: 'open',
//                          lesson: '6a', entry: 3, anchor: 'e-6a-3' }
//     Sent when a reader clicks "Open in app" inside the embedded docs.
//     The shell points the right pane at that entry instead of letting
//     the click navigate the left pane away to the app.
//
//   shell -> docs pane   { from: 'symbulator-split', type: 'scrollto',
//                          anchor: 'e-6a-3' }
//     Sent once the docs pane reports itself ready, and again whenever
//     the shell needs the left pane moved to a problem it is already
//     showing -- a hash change alone would not scroll a document the
//     browser considers already loaded.
//
//   docs pane -> shell   { from: 'symbulator-docs', type: 'ready',
//                          chapter: 'lesson-transient' }
//     Sent on load, so the shell knows the pane can be spoken to and
//     which chapter it settled on.
//
// The docs pane is same-origin with this shell -- both are served by
// learn.symbulator.com -- so messages to it are addressed to
// location.origin rather than '*', and messages from it are accepted
// only when they arrive from that frame's own window. The app pane is a
// different origin and is never messaged at all: it is driven by its
// src, which is the whole reason a click reloads it.
// -------------------------------------------------------------------------
(function () {
  'use strict';

  var APP = 'https://symbulator.pythonanywhere.com/';
  var docsFrame = document.getElementById('docsFrame');
  var appFrame  = document.getElementById('appFrame');
  var whereEl   = document.getElementById('where');

  // lesson word -> chapter slug. Written by build.py from the same
  // CHAPTER_BOOKS the links themselves are generated from, so the two
  // cannot drift: tools/app_links.py is the one place that knows Lesson
  // 6 is four books.
  var LESSONS = {};     // "6a" -> "lesson-transient"
  var CHAPTERS = {};    // "lesson-transient" -> "6a", its first book
  var pending = null;   // what was asked for before lessons.json arrived
  var onPage = '';      // the chapter, when opened on one rather than an entry
  var current = '';     // #304: the chapter the docs pane is on, for the menu

  function qs() {
    try { return new URLSearchParams(location.search); }
    catch (e) { return new URLSearchParams(''); }
  }

  function normalise(lesson) {
    // The app accepts 4b, 04b, 7 and 07 alike; this page keeps the
    // short spelling so its own URLs stay tidy and predictable.
    var m = String(lesson || '').trim().toLowerCase().match(/^0?(\d{1,2})([a-d]?)$/);
    return m ? m[1] + m[2] : '';
  }

  function docsUrlFor(lesson, anchor) {
    var chapter = LESSONS[lesson];
    if (!chapter) { return null; }
    return '/9/' + chapter + (anchor ? '#' + anchor : '');
  }

  // Point the right pane at an entry. This reloads the app, which is
  // deliberate and is what the reader asked for by clicking "show me
  // this one" -- but it does mean anything typed there is replaced. The
  // introduction says so, and so does the bar above.
  function loadApp(lesson, entry) {
    appFrame.src = APP + '?lesson=' + encodeURIComponent(lesson) +
                   '&entry=' + encodeURIComponent(entry);
  }

  function scrollDocsTo(anchor) {
    try {
      docsFrame.contentWindow.postMessage(
        { from: 'symbulator-split', type: 'scrollto', anchor: anchor },
        location.origin);
    } catch (e) { /* the pane is not ready; its 'ready' message will do it */ }
  }

  // The one place that moves the view. `reloadDocs` is false when the
  // click came from inside the docs pane, which is already on the right
  // page and only needs scrolling.
  function show(lesson, entry, reloadDocs) {
    lesson = normalise(lesson);
    entry = parseInt(entry, 10) || 1;
    if (!lesson) { return; }
    // No longer showing a whole chapter: a later 'ready' must not put the
    // chapter's title back over the entry this is about to name.
    onPage = '';
    var anchor = 'e-' + lesson + '-' + entry;
    current = LESSONS[lesson] || current;
    markCurrent();
    loadApp(lesson, entry);
    if (!Object.keys(LESSONS).length) {
      pending = function () { show(lesson, entry, reloadDocs); };
    } else if (reloadDocs) {
      var url = docsUrlFor(lesson, anchor);
      if (url) { docsFrame.src = url; }
    } else {
      scrollDocsTo(anchor);
    }
    whereEl.textContent = 'Lesson ' + lesson + ' · entry ' + entry;
    // Shareable at whatever the reader is looking at, without adding a
    // history entry per click -- the back button should leave the split
    // view, not walk back through the problems visited inside it.
    try {
      history.replaceState(null, '',
        location.pathname + '?lesson=' + lesson + '&entry=' + entry);
    } catch (e) {}
  }

  // ---- the lesson map ---------------------------------------------------
  fetch('/split/lessons.json', { cache: 'no-cache' })
    .then(function (r) { return r.json(); })
    .then(function (data) {
      LESSONS = (data && data.lessons) || {};
      CHAPTERS = (data && data.chapters) || {};
      buildMenu((data && data.titles) || []);
      if (pending) { pending(); pending = null; }
    })
    .catch(function () {
      // No map: the app pane still works from the query string, and the
      // docs pane stays on whatever it opened with. Degraded, not broken.
    });

  // ---- messages from the docs pane --------------------------------------
  window.addEventListener('message', function (ev) {
    if (ev.origin !== location.origin) { return; }
    if (!docsFrame.contentWindow || ev.source !== docsFrame.contentWindow) { return; }
    var msg = ev.data;
    if (!msg || msg.from !== 'symbulator-docs') { return; }
    if (msg.type === 'open') {
      show(msg.lesson, msg.entry, false);
    } else if (msg.type === 'ready') {
      // Opened on a page (#226): the bar says which chapter, in the words
      // the chapter itself uses.
      if (onPage && msg.title) { whereEl.textContent = msg.title; }
      var q = qs();
      var lesson = normalise(q.get('lesson') || q.get('input'));
      var entry = parseInt(q.get('entry') || '1', 10) || 1;
      if (lesson) { scrollDocsTo('e-' + lesson + '-' + entry); }
    }
  });

  // #226: the ribbon's "Split View" link carries the chapter the reader
  // is on rather than an entry -- they have not picked a problem, they
  // have asked to see this page beside the app. The left pane opens on
  // that chapter; the right pane opens on the chapter's first book, so
  // Lesson 6 opens the app on Lesson 6's entries rather than on whatever
  // it had last. A chapter with no book of its own (the introduction,
  // the credits) leaves the app at its own default.
  function showPage(page) {
    if (!/^[a-z0-9-]+$/.test(page)) { return; }
    if (!Object.keys(CHAPTERS).length) {
      pending = function () { showPage(page); };
      return;
    }
    onPage = page;
    current = page;
    markCurrent();
    docsFrame.src = '/9/' + page;
    var lesson = CHAPTERS[page];
    if (lesson) { loadApp(lesson, 1); }
    // A placeholder until the pane reports its real title, which is the
    // only place the chapter's name exists.
    whereEl.textContent = page.replace(/-/g, ' ');
    try {
      history.replaceState(null, '', location.pathname + '?page=' + page);
    } catch (e) {}
  }

  // ---- #304: the lesson menu --------------------------------------------
  // Roberto, 7 Sep 2026: "There's no table of content in split, so how
  // about we make a drop down menu for all the lessons, visible when one
  // clicks here" -- the position badge. Picking a chapter does what the
  // ribbon's Split View link does for it (showPage): the left pane opens
  // on the chapter, the right pane on the chapter's first book.
  var menu = document.getElementById('lessonMenu');
  var contentsBtn = document.getElementById('contentsBtn');   // #306
  var opener = whereEl;      // which trigger opened it, for the focus return
  var triggers = [whereEl, contentsBtn];

  function buildMenu(titles) {
    menu.innerHTML = '';
    titles.forEach(function (row) {
      var li = document.createElement('li');
      li.setAttribute('role', 'none');
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('role', 'menuitem');
      b.dataset.page = row[0];
      var num = document.createElement('span');
      num.className = 'num';
      num.textContent = row[1] || '';
      b.appendChild(num);
      b.appendChild(document.createTextNode(row[2] || row[0]));
      b.addEventListener('click', function () {
        closeMenu();
        showPage(row[0]);
      });
      li.appendChild(b);
      menu.appendChild(li);
    });
    markCurrent();
  }

  function markCurrent() {
    var items = menu.querySelectorAll('button[data-page]');
    for (var i = 0; i < items.length; i++) {
      items[i].setAttribute('aria-current', String(items[i].dataset.page === current));
    }
  }

  function openMenu(from) {
    if (!menu.children.length) { return; }
    opener = from || whereEl;
    menu.hidden = false;
    triggers.forEach(function (t) { t.setAttribute('aria-expanded', 'true'); });
    var cur = menu.querySelector('button[aria-current="true"]') || menu.querySelector('button');
    if (cur) { cur.focus(); }
  }
  function closeMenu() {
    menu.hidden = true;
    triggers.forEach(function (t) { t.setAttribute('aria-expanded', 'false'); });
  }
  triggers.forEach(function (t) {
    t.addEventListener('click', function () {
      if (menu.hidden) { openMenu(t); } else { closeMenu(); }
    });
  });
  document.addEventListener('click', function (ev) {
    if (menu.hidden) { return; }
    var onTrigger = triggers.some(function (t) { return t === ev.target || t.contains(ev.target); });
    if (onTrigger || menu.contains(ev.target)) { return; }
    closeMenu();
  });
  document.addEventListener('keydown', function (ev) {
    if (menu.hidden) { return; }
    if (ev.key === 'Escape') { closeMenu(); opener.focus(); return; }
    var items = Array.prototype.slice.call(menu.querySelectorAll('button'));
    var i = items.indexOf(document.activeElement);
    if (ev.key === 'ArrowDown') { ev.preventDefault(); (items[i + 1] || items[0]).focus(); }
    if (ev.key === 'ArrowUp') { ev.preventDefault(); (items[i - 1] || items[items.length - 1]).focus(); }
  });
  // A click inside either iframe never reaches this document, so the
  // menu also closes when the focus leaves for a pane.
  window.addEventListener('blur', closeMenu);

  // ---- opening state ----------------------------------------------------
  (function start() {
    var q = qs();
    var lesson = normalise(q.get('lesson') || q.get('input'));
    if (lesson) { show(lesson, q.get('entry') || 1, true); return; }
    var page = (q.get('page') || '').trim().toLowerCase();
    if (page) { showPage(page); return; }
    // Neither: the defaults in the markup stand.
  })();

  // ---- the divider ------------------------------------------------------
  var panes = document.getElementById('panes');
  var paneDocs = document.getElementById('paneDocs');
  var divider = document.getElementById('divider');
  var KEY = 'symbulator-split-ratio';

  function setRatio(pct) {
    pct = Math.min(80, Math.max(20, pct));
    paneDocs.style.flexBasis = pct + '%';
    try { localStorage.setItem(KEY, String(Math.round(pct))); } catch (e) {}
  }
  try {
    var saved = parseFloat(localStorage.getItem(KEY));
    if (saved) { paneDocs.style.flexBasis = saved + '%'; }
  } catch (e) {}

  divider.addEventListener('pointerdown', function (ev) {
    ev.preventDefault();
    divider.setPointerCapture(ev.pointerId);
    document.body.classList.add('dragging');
  });
  divider.addEventListener('pointermove', function (ev) {
    if (!document.body.classList.contains('dragging')) { return; }
    var box = panes.getBoundingClientRect();
    if (!box.width) { return; }
    setRatio(((ev.clientX - box.left) / box.width) * 100);
  });
  function endDrag(ev) {
    if (!document.body.classList.contains('dragging')) { return; }
    document.body.classList.remove('dragging');
    try { divider.releasePointerCapture(ev.pointerId); } catch (e) {}
  }
  divider.addEventListener('pointerup', endDrag);
  divider.addEventListener('pointercancel', endDrag);
  // Keyboard, because a separator that only answers to a mouse is not a
  // control everyone has.
  divider.addEventListener('keydown', function (ev) {
    var step = ev.key === 'ArrowLeft' ? -4 : ev.key === 'ArrowRight' ? 4 : 0;
    if (!step) { return; }
    ev.preventDefault();
    var box = panes.getBoundingClientRect();
    var now = paneDocs.getBoundingClientRect().width;
    if (box.width) { setRatio(((now + step * box.width / 100) / box.width) * 100); }
  });

  // ---- the tabs, on a narrow screen -------------------------------------
  var tabDocs = document.getElementById('tabDocs');
  var tabApp = document.getElementById('tabApp');
  function showPane(which) {
    document.body.setAttribute('data-show', which);
    tabDocs.setAttribute('aria-pressed', String(which === 'docs'));
    tabApp.setAttribute('aria-pressed', String(which === 'app'));
  }
  tabDocs.addEventListener('click', function () { showPane('docs'); });
  tabApp.addEventListener('click', function () { showPane('app'); });
  // A click in the left pane on a narrow screen has just loaded
  // something into a pane the reader cannot see. Bring it forward.
  window.addEventListener('message', function (ev) {
    if (ev.origin !== location.origin) { return; }
    var msg = ev.data;
    if (msg && msg.from === 'symbulator-docs' && msg.type === 'open'
        && window.matchMedia('(max-width: 820px)').matches) {
      showPane('app');
    }
  });
}());
</script>
</body>
</html>
