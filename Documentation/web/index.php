<?php
/**
 * Symbulator documentation — front controller.
 *
 * Serves the generated content in content/v7, v8 and v9. Everything under
 * content/ comes from build.py; edit the source tree, not these files.
 *
 * URLs:  /?v=7                  landing page for version 7
 *        /?v=7&p=lesson-dc      one chapter
 *        /?v=9&p=index          the back-of-book index
 * With the bundled .htaccess:  /7/lesson-dc  works too.
 */

$book = json_decode(file_get_contents(__DIR__ . '/content/book.json'), true);
// PHP turns numeric JSON keys into integers, so normalise them back to strings
$versions = array_map('strval', array_keys($book['versions']));
$byVersion = [];
foreach ($book['versions'] as $n => $vm) { $byVersion[(string) $n] = $vm; }

$v = isset($_GET['v']) ? preg_replace('/[^0-9]/', '', $_GET['v']) : '';
if (!in_array($v, $versions, true)) {
    $v = end($versions);            // newest by default
}
$toc = json_decode(
    file_get_contents(__DIR__ . "/content/v$v/toc.json"), true);

$page = isset($_GET['p']) ? preg_replace('/[^a-z0-9\-]/', '', $_GET['p']) : '';
$ids = array_column($toc['chapters'], 'id');
$isHome = ($page === '');
$isIndex = ($page === 'index');
if (!$isHome && !$isIndex && !in_array($page, $ids, true)) {
    http_response_code(404);
    $page = '';
    $isHome = true;
}

/** Current chapter record, or null on the landing page. */
$current = null;
foreach ($toc['chapters'] as $c) {
    if ($c['id'] === $page) { $current = $c; }
}

function url($v, $p = '') {
    // Root-absolute, and pretty: /9/lesson-dc, not ?v=9&p=lesson-dc.
    //
    // Both forms reach the same page -- .htaccess rewrites the first into
    // the second, and index.php only ever reads $_GET. Emitting the pretty
    // one keeps the address bar honest: a relative '?v=..' link followed
    // from /9/lesson-dc lands on /9/lesson-dc?v=9&p=lesson-ac, which serves
    // the right chapter under the wrong path.
    //
    // .htaccess only rewrites [789] and a lowercase-alnum-hyphen slug, so
    // anything else falls back to the query form rather than 404ing. That
    // fallback is also what makes a missing .htaccess a visible-but-partial
    // failure instead of a site-wide one.
    if (!preg_match('/^[789]$/', (string) $v)
        || ($p !== '' && !preg_match('/^[a-z0-9-]+$/', $p))) {
        return '/?v=' . rawurlencode($v)
             . ($p === '' ? '' : '&amp;p=' . rawurlencode($p));
    }
    return '/' . rawurlencode($v) . '/' . ($p === '' ? '' : rawurlencode($p));
}
function e($s) { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); }

// previous / next, for the footer pager
$pos = array_search($page, $ids, true);
$prev = ($pos !== false && $pos > 0) ? $toc['chapters'][$pos - 1] : null;
$next = ($pos !== false && $pos < count($ids) - 1) ? $toc['chapters'][$pos + 1] : null;

$pageTitle = $isHome ? $toc['name']
           : ($isIndex ? 'Index — ' . $toc['name']
                       : $current['title'] . ' — ' . $toc['name']);
?>
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($pageTitle) ?></title>
<meta name="description" content="<?= e($book['subtitle']) ?> — documentation for <?= e($toc['name']) ?>, <?= e($toc['platform']) ?>.">
<script>
// Applied as early as possible (before the stylesheet is even parsed) so a
// saved Dark Mode preference takes effect before first paint -- otherwise
// the page would flash light, then flip to dark, on every reload. Same
// mechanism as the Symbulator 9 interface's own #themeToggle, with its own
// storage key so the two never read each other's preference.
(function () {
  var saved = null;
  try { saved = localStorage.getItem('symbulator-docs-theme'); } catch (e) {}
  if (saved === 'dark') { document.documentElement.setAttribute('data-theme', 'dark'); }
})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#203864">
<?php
// A stamp that changes when the file does. Without one, the host's
// `Cache-Control: max-age=604800` keeps a returning visitor on a
// week-old stylesheet -- which on 25 Aug 2026 meant a phone still
// showing the pre-fix banner a day after the fix was deployed and
// verified. filemtime() means this page never needs remembering to
// bump, unlike the landing page, which has no build step and is
// stamped by tools/stamp_assets.py instead.
function asset(string $name): string {
    $path = __DIR__ . '/assets/' . $name;
    $v = is_file($path) ? substr(md5_file($path), 0, 8) : '0';
    return '/assets/' . $name . '?v=' . $v;
}
?>
<link rel="stylesheet" href="<?= asset('banner.css') ?>">
<link rel="stylesheet" href="<?= asset('style.css') ?>">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
</head>
<body class="v<?= e($v) ?><?= $isHome ? ' home' : '' ?>">

<a class="skip" href="#main">Skip to content</a>

<header class="topbar">
  <div class="topbar-inner">
    <div class="header-brand">
      <!-- The scorpion goes home to symbulator.com from every page and every
           property (#77). The wordmark beside it still goes to this site's
           own front page, which is the more useful thing to click while you
           are reading. -->
      <a class="header-logo-link" href="https://symbulator.com"
         aria-label="Symbulator home">
        <img src="/assets/logo.png" alt="Symbulator logo" class="header-logo">
      </a>
      <a class="header-title" href="<?= url($v) ?>">
        <p class="brand-name">Symbulator <span class="vnum"><?= e($toc['label']) ?></span></p>
        <!-- Static, and identical to the line on symbulator.com and in
             the app. It used to read "For <platform>", which made the
             lockup say something different on every version of the
             site; the version is already in the wordmark beside it and
             in the menu. -->
        <p class="brand-sub">the best portable symbolic simulator of linear circuits</p>
      </a>
    </div>
  </div>
</header>

<div class="subbar">
  <div class="subbar-inner">
      <!-- Plain links, not chips. The ribbon is the same row on all three
           properties and reads as one website only if its contents look
           alike; the two solid buttons that used to be here were the most
           visible thing making this page look unrelated to symbulator.com.
           The styling comes from the shared banner.css. -->
      <nav>
        <a href="/symbulator-v<?= e($v) ?>.pdf">Download as PDF</a>
        <a href="https://symbulator.pythonanywhere.com">Online App</a>
      </nav>

  
      <span class="subbar-spacer"></span>
      <details class="versions" id="version-picker">
        <summary aria-label="Choose a version">
          <span class="vkey-full">Symbulator <?= e($toc['label']) ?></span>
          <span class="vkey-num"><?= e($toc['label']) ?></span>
          <svg class="chev" viewBox="0 0 16 16" aria-hidden="true" fill="none"
               stroke="currentColor" stroke-width="1.6" stroke-linecap="round"
               stroke-linejoin="round"><path d="M4 6.5 8 10.5l4-4"/></svg>
        </summary>
        <ul class="version-list">
          <?php foreach ($versions as $n): $vm = $byVersion[$n]; ?>
            <li>
              <a href="<?= url($n, in_array($page, $ids, true) ? $page : '') ?>"
                 <?= $n === $v ? 'aria-current="true" class="is-current"' : '' ?>>
                <span class="v-name">Symbulator <?= e($vm['label']) ?></span>
                <span class="v-plat">For <?= e($vm['platform']) ?></span>
              </a>
            </li>
          <?php endforeach; ?>
        </ul>
      </details>

      <button type="button" id="theme-toggle" class="theme-toggle"
              aria-label="Switch to dark mode" title="Switch to dark mode"><svg viewBox="0 0 24 24" fill="#8ec7f5" aria-hidden="true"><path d="M20.4 14.7A8.5 8.5 0 1 1 9.3 3.6a7 7 0 1 0 11.1 11.1Z"/></svg></button>
  </div>
</div>

<div class="shell">

<nav class="sidebar" aria-label="Contents">

  <?php /* #87. Searches this version only -- the index is written per
           version by build.py and fetched by the script below, so a reader
           of 7 is never sent to a page that exists only in 9. It sits here
           rather than in the banner because the banner is shared with
           symbolator.com and the app, and only this site has a search. */ ?>
  <form class="docsearch" role="search" onsubmit="return false;">
    <label for="docsearch">Search Symbulator <?= e($toc['label']) ?></label>
    <input type="search" id="docsearch" data-version="<?= e($v) ?>"
           autocomplete="off" spellcheck="false"
           placeholder="Search Symbulator <?= e($toc['label']) ?>">
    <p class="docsearch-status" id="docsearch-status" role="status" hidden></p>
    <ol class="docsearch-results" id="docsearch-results" hidden></ol>
  </form>
  <script>
  /* The index is a few hundred kilobytes, so it is not fetched until the
     reader actually types. Nothing here is required for the page to work:
     without JavaScript the box simply does nothing, and Contents is still
     the way around. */
  (function () {
    var box = document.getElementById('docsearch');
    if (!box) return;
    var list = document.getElementById('docsearch-results');
    var note = document.getElementById('docsearch-status');
    var version = box.getAttribute('data-version');
    var index = null, loading = false, latest = '';

    function say(msg) { note.textContent = msg; note.hidden = !msg; }

    function esc(s) {
      return s.replace(/[&<>]/g, function (c) {
        return c === '&' ? '&amp;' : c === '<' ? '&lt;' : '&gt;';
      });
    }

    function load() {
      if (index || loading) return;
      loading = true;
      say('Loading…');
      fetch('/content/v' + version + '/search.json')
        .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
        .then(function (data) {
          index = data; loading = false; say(''); run(latest);
        })
        .catch(function () {
          loading = false;
          say('Search is unavailable on this server.');
        });
    }

    function snippet(text, term) {
      var i = text.toLowerCase().indexOf(term);
      if (i < 0) { return esc(text.slice(0, 110)) + '…'; }
      var from = Math.max(0, i - 40);
      var to = Math.min(text.length, i + term.length + 80);
      return (from > 0 ? '…' : '')
           + esc(text.slice(from, i))
           + '<mark>' + esc(text.substr(i, term.length)) + '</mark>'
           + esc(text.slice(i + term.length, to))
           + (to < text.length ? '…' : '');
    }

    function run(raw) {
      latest = raw;
      var q = raw.trim().toLowerCase();
      list.innerHTML = '';
      list.hidden = true;
      if (q.length < 2) { say(''); return; }
      if (!index) { load(); return; }

      var terms = q.split(/\s+/);
      var hits = [];
      for (var k = 0; k < index.length; k++) {
        var entry = index[k];
        var head = ((entry.q || '') + ' ' + (entry.s || '') + ' '
                    + (entry.c || '')).toLowerCase();
        var body = head + ' ' + entry.t.toLowerCase();
        var score = 0, all = true;
        for (var t = 0; t < terms.length; t++) {
          if (body.indexOf(terms[t]) < 0) { all = false; break; }
          score += head.indexOf(terms[t]) >= 0 ? 4 : 1;
        }
        if (all) { hits.push([score, k, entry]); }
      }
      hits.sort(function (a, b) { return b[0] - a[0] || a[1] - b[1]; });

      if (!hits.length) {
        say('No match in Symbulator ' + version + '.');
        return;
      }
      say(hits.length + (hits.length === 1 ? ' match' : ' matches')
          + (hits.length > 12 ? ', showing the first 12' : ''));
      var frag = document.createDocumentFragment();
      hits.slice(0, 12).forEach(function (hit) {
        var entry = hit[2];
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.href = '/' + version + '/' + entry.p
               + (entry.a ? '#' + entry.a : '');
        a.innerHTML =
          '<span class="docsearch-where">' + esc(entry.c) + '</span>'
          + '<span class="docsearch-what">'
          + esc(entry.q || entry.s || entry.c) + '</span>'
          + '<span class="docsearch-snip">'
          + snippet(entry.t, terms[0]) + '</span>';
        li.appendChild(a);
        frag.appendChild(li);
      });
      list.appendChild(frag);
      list.hidden = false;
    }

    box.addEventListener('input', function () { run(box.value); });
    box.addEventListener('focus', load, { once: true });
    box.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') { box.value = ''; run(''); }
    });
  })();
  </script>

  <details class="toc" id="toc" open>
    <summary class="sidebar-title">Contents<svg class="toc-chev" viewBox="0 0 16 16"
      aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8"
      stroke-linecap="round" stroke-linejoin="round"><path d="M4 6.5 8 10.5l4-4"/></svg></summary>
  <ol class="chapters">
    <?php foreach ($toc['chapters'] as $c): ?>
      <li class="<?= $c['id'] === $page ? 'is-current' : '' ?><?= $c['present'] ? '' : ' is-absent' ?>">
        <a href="<?= url($v, $c['id']) ?>">
          <?php /* Introduction and the credits have no lesson number, so no
                    eyebrow. Printing one anyway repeated the title:
                    "Introduction Introduction". */ ?>
          <?php if ($c['eyebrow']): ?>
            <span class="ch-eyebrow"><?= e($c['eyebrow']) ?></span>
          <?php endif; ?>
          <span class="ch-title"><?= e($c['title']) ?></span>
        </a>
        <?php if ($c['id'] === $page && $c['sections']): ?>
          <ul class="sections">
            <?php foreach ($c['sections'] as $s): ?>
              <li><a href="#<?= e($s['anchor']) ?>">
                <span class="secno"><?= e($s['number']) ?></span>
                <?= e($s['title']) ?></a></li>
            <?php endforeach; ?>
          </ul>
        <?php endif; ?>
      </li>
    <?php endforeach; ?>
    <li class="<?= $isIndex ? 'is-current' : '' ?>">
      <a href="<?= url($v, 'index') ?>"><span class="ch-title">Index</span></a>
    </li>
  </ol>
  </details>
</nav>
<script>
/* Restore the reader's last Contents choice. Runs here, right after the
   element, rather than at the end of the body, so a folded list never
   flashes open first. Default: open on a wide screen, folded on a narrow
   one, where fourteen chapters would otherwise sit on top of every page. */
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
</script>

<main id="main">
<?php if ($isHome): ?>

  <ol class="chapter-cards">
    <?php foreach ($toc['chapters'] as $c): ?>
      <li<?= $c['present'] ? '' : ' class="is-absent"' ?>>
        <a href="<?= url($v, $c['id']) ?>">
          <?php if ($c['eyebrow']): ?>
            <p class="card-eyebrow"><?= e($c['eyebrow']) ?></p>
          <?php endif; ?>
          <h2><?= e($c['title']) ?></h2>
          <p class="card-summary"><?= strip_tags($c['summary'], '<em><strong><code>') ?></p>
        </a>
      </li>
    <?php endforeach; ?>
  </ol>

<?php elseif ($isIndex): ?>

  <article class="chapter">
    <header class="chapter-head">
      <p class="eyebrow">Index</p>
      <h1>Index</h1>
    </header>
    <ul class="book-index">
      <?php foreach ($toc['index'] as $term => $spots): ?>
        <li><span class="ix-term"><?= e($term) ?></span>
          <?php foreach ($spots as $i => $spot):
                  [$cid, $anchor] = explode('#', $spot); ?>
            <a href="<?= url($v, $cid) . '#' . e($anchor) ?>"><?= $i + 1 ?></a><?php endforeach; ?>
        </li>
      <?php endforeach; ?>
      <?php if (!$toc['index']): ?><li>No entries yet.</li><?php endif; ?>
    </ul>
  </article>

<?php else: ?>

  <article class="chapter">
    <?php readfile(__DIR__ . "/content/v$v/$page.html"); ?>
  </article>

  <nav class="pager">
    <?php if ($prev): ?>
      <a class="pager-prev" href="<?= url($v, $prev['id']) ?>">
        <span>Previous</span><?= e($prev['title']) ?></a>
    <?php endif; ?>
    <?php if ($next): ?>
      <a class="pager-next" href="<?= url($v, $next['id']) ?>">
        <span>Next</span><?= e($next['title']) ?></a>
    <?php endif; ?>
  </nav>

<?php endif; ?>
</main>
</div>

<footer class="foot">
  <p><?= e($book['title']) ?> — <?= e($toc['name']) ?>, <?= e($toc['platform']) ?>.
     Documentation by Roberto Perez-Franco. MIT licence.</p>
  <p><a href="/symbulator-v<?= e($v) ?>.pdf">This documentation as a PDF</a></p>
</footer>

<script>
(function () {
  var picker = document.getElementById('version-picker');
  if (!picker) return;
  document.addEventListener('click', function (e) {
    if (!picker.contains(e.target)) picker.open = false;
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && picker.open) { picker.open = false;
      picker.querySelector('summary').focus(); }
  });
})();

// Dark Mode toggle. The early inline script in <head> already applied a
// saved preference (if any) before first paint, so this only has to wire
// up the button: flip the attribute, persist it, and update the icon/label.
// Same SVGs and logic as the interface's own #themeToggle.
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
</script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[
    {left:'\\[',right:'\\]',display:true},
    {left:'\\(',right:'\\)',display:false}]});"></script>
</body>
</html>
