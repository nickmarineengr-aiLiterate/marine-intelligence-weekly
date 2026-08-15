#!/usr/bin/env python3
"""Shared rendering helpers for the Past Papers product.

Imported by build_paper.py and build_index.py so the paper and the two index
pages cannot drift in escaping, search-token construction, storage keys or
chrome. Nothing here reads the clock or the filesystem beyond the template
directory, so every generated file stays byte-reproducible.
"""
import html as html_mod
import io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
TPL = os.path.join(HERE, 'template')

BASE = 'https://marineintelligenceweekly.com'
CONTACT = 'contactus@marineintelligenceweekly.com'


def answers_built(spec):
    """How many questions in this spec carry an authored model answer."""
    return sum(1 for q in spec['questions'] if q.get('model_answer'))


def is_intake(spec):
    """True for an INTAKE spec: real transcribed questions, no answers yet.

    Defined here, once, because five stages need the same answer, and a spec
    that is intake to one stage but solved to another produces exactly the
    failure this predicate exists to prevent -- a topic page linking to a paper
    page that was never built.

    The rule matches build_index.paper_status(): a paper is a product only when
    an answer exists. Holding a transcription is not a product, so an intake
    paper has NO paper page, no verification directory and no answer-layer
    fields. Its questions reach the candidate through questions-<year>.html,
    which already renders them as 'Questions transcribed' and withholds every
    link to a solved answer.

    An intake paper becomes an ordinary paper the moment its first answer is
    authored. Nothing is cached and no spec field has to be flipped by hand.
    """
    return answers_built(spec) == 0

# localStorage keys. Namespaced by product and schema so a future schema change
# cannot silently reinterpret old state. Values are keyed by stable question_id
# (QP2607-Q1), never by DOM order.
LS_BOOKMARKS = 'miw:pastpapers:v1:bookmarks'
LS_PROGRESS = 'miw:pastpapers:v1:progress'

# Migration of study state saved before papers were renamed to the QP series.
# Injected into BOTH page scripts from here so the two can never drift apart.
#
# Properties: idempotent (a second run is a no-op), non-destructive (an existing
# QP key always wins, so a device that has studied under both spellings keeps the
# newer state), and safe to run on a fresh device (no legacy keys, no write).
# Keys are snapshotted before mutating, rather than deleting mid for-in.
# The topbar and the controls bar are both sticky and stack, so the controls bar
# must be offset by exactly the topbar's height. That height is content-driven --
# it wraps to two or three lines as the viewport narrows -- so no CSS constant
# can be right at every width. Hardcoding it produced two real defects: a 29px
# gap where content showed through between the bars on desktop, and on a 375px
# phone both bars claimed top:0, so the topbar covered the controls bar and the
# search input became unreachable. Measuring is the only correct answer.
STICKY_SYNC_JS = """  function plausibleBarHeight(px) {
    // A measurement SANITY GATE, not decoration. These bars are flex rows with
    // wrap; measured before layout has settled, every child can land on its own
    // line and the row reports a height many times its real one -- the Solved
    // QP home read its 46px topbar as 377px, which pushed the sticky search bar
    // a third of the way down the viewport and stayed wrong until the first
    // resize event. A "topbar" taller than a third of the viewport is not a
    // topbar, so the reading is discarded and the CSS fallback stands until a
    // later pass measures it properly.
    var h = window.innerHeight || 800;
    return px >= 16 && px <= h * 0.34;
  }
  function syncStickyOffsets() {
    var root = document.documentElement;
    var tb = document.querySelector('.topbar');
    var cb = document.querySelector('.controls-bar');
    if (tb && plausibleBarHeight(tb.offsetHeight)) {
      root.style.setProperty('--topbar-h', tb.offsetHeight + 'px');
    }
    if (cb && plausibleBarHeight(cb.offsetHeight)) {
      root.style.setProperty('--controls-h', cb.offsetHeight + 'px');
    }
  }
  syncStickyOffsets();
  // Re-measured as the document settles. Timers rather than
  // requestAnimationFrame on purpose: rAF never fires in a browser that is not
  // producing frames (a hidden or backgrounded tab), and a sticky offset that
  // is only correct in a visible tab is the kind of bug that reaches a reader
  // and never reaches a reviewer.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', syncStickyOffsets);
  }
  window.addEventListener('load', syncStickyOffsets);
  window.addEventListener('resize', syncStickyOffsets);
  window.addEventListener('orientationchange', syncStickyOffsets);
  setTimeout(syncStickyOffsets, 0);
  setTimeout(syncStickyOffsets, 250);
  if (window.document.fonts && window.document.fonts.ready &&
      typeof window.document.fonts.ready.then === 'function') {
    // Web fonts land after first paint and change the bars' wrapped height.
    window.document.fonts.ready.then(syncStickyOffsets);
  }"""

LS_MIGRATE_JS = """  function migrateLegacyKeys(o) {
    var keys = Object.keys(o), changed = false, i, m, nk;
    for (i = 0; i < keys.length; i++) {
      m = /^EM(\\d{4}-Q\\d+)$/.exec(keys[i]);
      if (!m) continue;
      nk = 'QP' + m[1];
      if (!Object.prototype.hasOwnProperty.call(o, nk)) o[nk] = o[keys[i]];
      delete o[keys[i]];
      changed = true;
    }
    return changed;
  }"""

GATE = ('<script>if(!/miw_auth=1/.test(document.cookie))'
        '{window.location.replace("/SQ/pay.html");}</script>')
GATE_STUB = '<!-- GATE SCRIPT STRIPPED FOR REVIEW COPY -->'


def esc(s):
    """Escape bare ampersands only. Inline tags and entities are author intent."""
    return re.sub(r'&(?![A-Za-z#][A-Za-z0-9]{1,8};)', '&amp;', str(s))


def esc_attr(s):
    """Full escape for attribute values and anywhere markup must not survive."""
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;'))


def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', str(s))).strip()


def plain_text(s):
    """Tag-free, entity-DECODED text for <title> and meta@content.

    Those are plain-text slots: a browser does not render markup inside them.
    Page titles are authored with display entities like '&mdash;', and running
    esc_attr() straight over one yields '&amp;mdash;', which the browser then
    shows as the literal characters "&mdash;" in the tab and in every share
    preview. Decoding first means esc_attr only ever escapes real characters.
    """
    return html_mod.unescape(strip_tags(s))


def read_css():
    """style.css is verbatim from a live reference file; pastpapers.css is ours."""
    a = open(os.path.join(TPL, 'style.css'), encoding='utf-8').read().rstrip('\n')
    b = open(os.path.join(TPL, 'pastpapers.css'), encoding='utf-8').read().rstrip('\n')
    return a + '\n' + b


def block_text(blocks):
    """Flatten a blocks object to plain text -- used to build search tokens."""
    if not blocks:
        return ''
    buf = []
    for b in blocks.get('blocks', []):
        for k in ('h', 'p'):
            if k in b:
                buf.append(b[k])
        for k in ('ul', 'ol'):
            if k in b:
                buf.extend(b[k])
        if 'table' in b:
            buf.extend(b['table'].get('headers', []))
            for row in b['table'].get('rows', []):
                buf.extend(row)
    return strip_tags(' '.join(buf))


def block_headings(blocks):
    """Just the h-level headings -- the useful part of an answer for search."""
    if not blocks:
        return []
    return [strip_tags(b['h']) for b in blocks.get('blocks', []) if 'h' in b]


SPEC_GLOB = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers', 'specs', '*.json')


def load_all_specs():
    """Every spec in the corpus, in stable paper_id order.

    Several builders need the WHOLE corpus rather than the one spec they were
    handed, because chronological recurrence is a property of the corpus and not
    of any single paper. Loading it in one place keeps them from disagreeing
    about which papers exist.
    """
    import glob
    return [json.load(io.open(p, encoding='utf-8'))
            for p in sorted(glob.glob(SPEC_GLOB))]


def corpus_relations(specs=None):
    """(nodes, relations) for the whole corpus, from recurrence_model.

    This is the ONLY source of candidate-facing recurrence. The host's printed
    annotation (``host_recurrence_hint``) is discovery-only provenance and never
    reaches a rendered surface; the authoring field ``recurrence_class`` records
    what was true in PRODUCTION order and is not chronology. See
    recurrence_model.py for the three questions where the two disagree.
    """
    import recurrence_model as RM
    specs = specs if specs is not None else load_all_specs()
    nodes = RM.load_nodes(specs)
    return nodes, RM.build_families(nodes)


def search_tokens(q, paper, relation=None):
    """Deterministic search string for a question card.

    Driven from the spec, NOT from rendered text. QB10_A searches
    `card.innerText`, which excludes display:none subtrees -- so its search
    silently misses answer content while a card is collapsed. Generating the
    tokens here means search works on collapsed cards and on metadata that is
    never displayed at all.

    Two recurrence signals are deliberately ABSENT. ``host_recurrence_hint`` is
    the source copy host's own claim, which policy classes discovery-only and
    which the 2026 set proved wrong in both directions; shipping it inside a
    data-search attribute makes it invisible on screen and still present in the
    bytes, which is the worst of both. ``recurrence_class`` is an authoring
    field recorded in production order, so searching "exact repeat" against it
    returns the wrong questions. The canonical status label is passed in as
    ``relation`` instead.
    """
    parts = [
        q['q_no'], q['question_id'], paper['paper_id'], paper['sr_no'],
        paper['month'], str(paper['year']), paper['month_year'], paper['subject'],
        q.get('short_title', ''), strip_tags(q['text_verbatim']),
        '%s marks' % q['total_marks'],
        relation['label_plain'] if relation else '',
    ]
    parts += q.get('topic_tags') or []
    parts += q.get('subject_tags') or []
    parts += q.get('intent_tags') or []
    parts += q.get('search_aliases') or []
    parts += q.get('regulations') or []
    parts += block_headings(q.get('model_answer'))
    parts += block_headings(q.get('study_notes'))
    qr = q.get('quick_revision') or {}
    parts += qr.get('keywords') or []
    if qr.get('critical_regulation'):
        parts.append(strip_tags(qr['critical_regulation']))
    seen, out = set(), []
    for p in parts:
        t = strip_tags(p).lower()
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return ' '.join(out)


def solved_years(specs=None):
    """Years holding at least one solved paper, ascending.

    Derived from the specs every time. A year appears in the delivered
    navigation because a paper in it was solved, never because a builder
    was told the year exists.
    """
    specs = specs if specs is not None else load_all_specs()
    return sorted({s['year'] for s in specs if not is_intake(s)})


def delivery_links(year=None, years=None):
    """Navigation for the paid Written delivery surface at /solvedQP/.

    It must not link into /meoclass1/: a customer who owns SOLVED_QP but not
    ORAL_QB_NOTES would be bounced to the login page by their own product's
    own navigation.

    The year link is CONTEXTUAL, not global. A paper page links to the sheet
    for ITS OWN year -- QP2404 to questions-2024.html, QP2601 to
    questions-2026.html -- because that is the sheet its reader is actually
    in. This replaces a single hard-coded link to questions-2026.html, which
    was correct only while 2026 was the only solved year and silently sent a
    2024 reader to the wrong sheet once 2024 and 2025 were solved.

    Pages with no single year -- the product home -- get one link per solved
    year instead, so every sheet stays reachable without guessing a URL.
    """
    links = [('Solved QP', '/solvedQP/')]
    if year is not None:
        links.append(('Questions by year', '/solvedQP/questions-%d.html' % year))
    else:
        for y in (years if years is not None else solved_years()):
            links.append(('%d questions' % y, '/solvedQP/questions-%d.html' % y))
    return links


def promo_links():
    """Navigation for the Written promo served inside the ORAL product.

    Its reader owns ORAL_QB_NOTES and, by definition, does NOT own SOLVED_QP --
    the page exists to sell them that. So the default Written navigation is
    exactly wrong here: 'Written Questions', '2026 Topics' and the review tree
    it points at are all behind the entitlement the reader has not bought, and
    every one of them would bounce them to a login page from inside a page they
    are legitimately reading. A funnel that logs its prospect out is not a
    funnel.

    These are the storefront links already proven on the public sample at
    SQ/solved-qp-sample-january-2026.html. Reused verbatim rather than invented:
    the promo and the sample are the same product moment reached by two
    audiences, and they should not teach two different routes to the same shop.
    """
    return [('MEO Class I store', '/SQ/index.html'),
            ('Get full access &middot; &#8377;1,500', '/SQ/index.html#solved-qp')]


def topbar(active='', links=None):
    """Consistent navigation across every Past Papers page. Kept compact.

    `links` overrides the default set. The paid delivery surface passes
    delivery_links(), which keeps its navigation inside /solvedQP/.
    """
    if links is None:
        links = [
            ('MEO Class I', '/meoclass1/'),
            ('Written Questions', '/meoclass1/pastpapers/'),
            ('2026 Topics', '/meoclass1/pastpapers/topics-2026.html'),
            # No '#question-banks' anchor has ever existed on that page. The
            # fragment was inert -- the browser lands at the top of the hub,
            # which IS the Question Bank -- so it promised a jump it could not
            # make. Dropping it is the whole fix; the hub needs no new anchor.
            ('Question Bank', '/meoclass1/'),
        ]
    out = ['<nav class="topbar" aria-label="Primary">',
           '  <span class="logo">&#9875; MIW</span>',
           '  <span class="topbar-sub">Written Questions &amp; Answers</span>',
           '  <span class="topbar-links">']
    for label, href in links:
        cur = ' aria-current="page"' if label == active else ''
        out.append('    <a href="%s"%s>%s</a>' % (href, cur, esc(label)))
    out.append('  </span>')
    out.append('</nav>')
    return out


def head_meta(title, description, canonical_path, publish, extra=()):
    """Head block. Review mode is noindex; publish mode carries full SEO."""
    o = ['<!DOCTYPE html>', '<html lang="en">', '<head>',
         '<meta charset="UTF-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
         '<title>%s</title>' % esc_attr(plain_text(title)),
         '<meta name="description" content="%s">' % esc_attr(plain_text(description))]
    if publish:
        o.append('<meta name="robots" content="index, follow, max-image-preview:large">')
        o.append('<link rel="canonical" href="%s%s">' % (BASE, canonical_path))
        o.append('<meta property="og:type" content="article">')
        o.append('<meta property="og:title" content="%s">' % esc_attr(plain_text(title)))
        o.append('<meta property="og:description" content="%s">' % esc_attr(plain_text(description)))
        o.append('<meta property="og:url" content="%s%s">' % (BASE, canonical_path))
        o.append('<meta property="og:site_name" content="Marine Intelligence Weekly">')
        o.append('<meta name="twitter:card" content="summary">')
    else:
        # Founder review build. Never indexable.
        o.append('<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">')
        o.append('<link rel="canonical" href="%s%s">' % (BASE, canonical_path))
    o.append('<meta name="geo.region" content="IN-KL">')
    o.extend(extra)
    return o


# =====================================================================
# CORPUS SEARCH -- the one client-side definition, shared by every page
# =====================================================================
#
# WHY THIS EXISTS
# ---------------
# Before this, three pages each had their own search and each was correctly
# scoped to itself: the paper page searched its nine questions, the year sheet
# searched its year, the home page searched the corpus. Correct in isolation,
# and together they taught the reader the corpus was empty -- a candidate inside
# QP2607 typing "port state control" saw "no question matches that search" while
# 23 questions across 18 sittings existed one page away.
#
# The fix is not a fourth search. It is a fallback the scoped searches can call
# when they come up empty, and an explicit "search all solved papers" the reader
# can elect at any time. Both must fold and match EXACTLY as the home page does,
# or the same query would answer differently depending on where it was typed --
# so the folding lives here once and every page gets this same string.
#
# MATCHING CONTRACT (mirrors build_solvedqp_manifest.norm_search)
#   * lowercase; everything except [a-z0-9'&] collapses to a single space
#   * all terms must be present (AND), substring, order-independent
#   * iteration order is manifest order, which is (year, month) then q_no --
#     so results are deterministic and need no sort
#
# PAID-TEXT BOUNDARY
# ------------------
# This reads solvedqp_content_index.json and nothing else. That file is built by
# a generator whose assert_no_paid_text() fails the build rather than emit one
# sentence of a model answer, so there is no answer text here to leak even if
# the payload is downloaded directly. Results render stem, short title, sitting
# and question number -- the discovery surface, never the product.
CORPUS_SEARCH_JS = r"""  window.MIWCorpus = (function () {
    var IDX = null, PENDING = null;
    var SRC = '/solvedQP/solvedqp_content_index.json';

    function fold(s) {
      return String(s).toLowerCase()
        .replace(/[^a-z0-9'&]+/g, ' ').replace(/\s+/g, ' ').trim();
    }
    function terms(q) { return fold(q).split(' ').filter(Boolean); }

    function load() {
      if (IDX) return Promise.resolve(IDX);
      if (PENDING) return PENDING;
      PENDING = fetch(SRC, { cache: 'no-store' })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (j) { IDX = j; PENDING = null; return j; })
        .catch(function () { PENDING = null; return null; });
      return PENDING;
    }

    // opts.excludePaper -- omit the paper the reader is already in.
    // opts.excludeYear  -- omit the year sheet the reader is already in.
    function match(q, opts) {
      opts = opts || {};
      var t = terms(q), groups = [], nq = 0;
      if (!IDX || !t.length) return { groups: groups, questions: 0, papers: 0 };
      IDX.papers.forEach(function (p) {
        if (p.status !== 'AVAILABLE' || !p.questions.length) return;
        if (opts.excludePaper && p.paper_id === opts.excludePaper) return;
        if (opts.excludeYear && p.year === opts.excludeYear) return;
        var hits = p.questions.filter(function (x) {
          var s = x.search_text || '';
          return t.every(function (w) { return s.indexOf(w) >= 0; });
        });
        if (hits.length) { groups.push({ paper: p, hits: hits }); nq += hits.length; }
      });
      return { groups: groups, questions: nq, papers: groups.length };
    }

    function esc(s) {
      return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
      });
    }

    // Deep links go straight to /solvedQP/QP####.html#qN. The gate is an edge
    // concern -- a reader without entitlement is redirected by middleware and
    // arrives back here after login. Degrading the link to a storefront URL
    // would throw away the anchor the reader actually asked for.
    function renderGroups(res) {
      var h = [];
      res.groups.forEach(function (g) {
        h.push('<div class="mc-paper">');
        h.push('<h4><a href="' + esc(g.paper.href) + '">' + esc(g.paper.sitting) +
               '</a> <span class="mc-sr">' + esc(g.paper.sr_no) + '</span></h4>');
        g.hits.forEach(function (x) {
          var topic = (x.topic_tags && x.topic_tags.length) ? x.topic_tags[0]
                    : (x.primary_category || '');
          h.push('<a class="mc-q" href="' + esc(x.href) + '">' +
                 '<b>' + esc(x.question_number) + '</b>' +
                 '<span class="mc-t">' + esc(x.short_title || '') + '</span>' +
                 (topic ? '<span class="mc-tag">' + esc(topic) + '</span>' : '') +
                 '</a>');
        });
        h.push('</div>');
      });
      return h.join('');
    }

    function summary(res) {
      return res.papers + (res.papers === 1 ? ' sitting' : ' sittings') + ' &middot; ' +
             res.questions + (res.questions === 1 ? ' question' : ' questions');
    }

    return { load: load, match: match, fold: fold, terms: terms,
             renderGroups: renderGroups, summary: summary, esc: esc,
             index: function () { return IDX; } };
  })();"""


# The broaden-scope panel. Rendered empty on the server and filled in by
# CORPUS_SEARCH_JS, so a reader with JS disabled sees no broken promise.
def corpus_fallback_block(scope_label):
    """Server-side shell for the 'search all solved papers' escape hatch.

    ``scope_label`` names what the LOCAL search covered -- "this paper",
    "2024" -- because a result count means nothing without its scope. The
    reader is never asked to infer which corpus they just searched.
    """
    return [
        '<div class="mc-wrap" id="mc-wrap" hidden>',
        '  <div class="mc-head">',
        '    <span class="mc-scope">Across all solved papers</span>',
        '    <span class="mc-sum" id="mc-sum" role="status" aria-live="polite"></span>',
        '  </div>',
        '  <p class="mc-note" id="mc-note">Nothing in %s &mdash; these are from other '
        'sittings.</p>' % esc(scope_label),
        '  <div class="mc-res" id="mc-res"></div>',
        '</div>',
        '<div class="mc-offer" id="mc-offer" hidden>',
        '  <button type="button" id="mc-offer-btn" class="mc-offer-btn"></button>',
        '</div>',
    ]


def footer(publish):
    return ['<footer class="page-footer">',
            '  Marine Intelligence Weekly &mdash; MEO Class I Written Questions &amp; Answers '
            '&middot; Compiled by Nixon Antony, 2/E, Maersk A/S<br>',
            '  Examination questions are reproduced for study purposes. For personal '
            'exam-preparation use. Not for redistribution. Corrections: '
            '<a href="mailto:%s">%s</a>' % (CONTACT, CONTACT),
            '</footer>']
