#!/usr/bin/env python3
"""Shared rendering helpers for the Past Papers product.

Imported by build_paper.py and build_index.py so the paper and the two index
pages cannot drift in escaping, search-token construction, storage keys or
chrome. Nothing here reads the clock or the filesystem beyond the template
directory, so every generated file stays byte-reproducible.
"""
import html as html_mod
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
TPL = os.path.join(HERE, 'template')

BASE = 'https://marineintelligenceweekly.com'
CONTACT = 'contactus@marineintelligenceweekly.com'

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
STICKY_SYNC_JS = """  function syncStickyOffsets() {
    var root = document.documentElement;
    var tb = document.querySelector('.topbar');
    var cb = document.querySelector('.controls-bar');
    if (tb) root.style.setProperty('--topbar-h', tb.offsetHeight + 'px');
    if (cb) root.style.setProperty('--controls-h', cb.offsetHeight + 'px');
  }
  syncStickyOffsets();
  window.addEventListener('resize', syncStickyOffsets);
  window.addEventListener('orientationchange', syncStickyOffsets);
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


def search_tokens(q, paper, publish=False):
    """Deterministic search string for a question card.

    publish=True is a candidate-facing build. It drops two authoring inputs:
      * recurrence_class   -- tells a candidate what to expect; not ours to say;
      * recurrence         -- third-party source-copy annotations for sittings
                              MIW never read.
    Both stay in the review build. They were previously baked into every
    shipped page's data-search attribute, so although invisible they were
    present in the delivered bytes and searchable by anyone who looked.

    Driven from the spec, NOT from rendered text. QB10_A searches
    `card.innerText`, which excludes display:none subtrees -- so its search
    silently misses answer content while a card is collapsed. Generating the
    tokens here means search works on collapsed cards and on metadata that is
    never displayed at all.
    """
    parts = [
        q['q_no'], q['question_id'], paper['paper_id'], paper['sr_no'],
        paper['month'], str(paper['year']), paper['month_year'], paper['subject'],
        q.get('short_title', ''), strip_tags(q['text_verbatim']),
        '%s marks' % q['total_marks'],
        '' if publish else q.get('recurrence_class', ''),
    ]
    parts += q.get('topic_tags') or []
    parts += q.get('subject_tags') or []
    parts += q.get('intent_tags') or []
    parts += q.get('search_aliases') or []
    parts += q.get('regulations') or []
    if not publish:
        parts += q.get('recurrence') or []
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


# Navigation for the paid Written delivery surface at /solvedQP/. It must not
# link into /meoclass1/: a customer who owns SOLVED_QP but not ORAL_QB_NOTES
# would be bounced to the login page by their own product's own navigation.
DELIVERY_LINKS = [
    ('Solved QP', '/solvedQP/'),
    ('Questions by year', '/solvedQP/questions-2026.html'),
]


def topbar(active='', links=None):
    """Consistent navigation across every Past Papers page. Kept compact."""
    if links is None:
        links = [
            ('MEO Class I', '/meoclass1/'),
            ('Written Questions', '/meoclass1/pastpapers/'),
            ('2026 Topics', '/meoclass1/pastpapers/topics-2026.html'),
            ('Question Bank', '/meoclass1/#question-banks'),
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


def footer(publish):
    return ['<footer class="page-footer">',
            '  Marine Intelligence Weekly &mdash; MEO Class I Written Questions &amp; Answers '
            '&middot; Compiled by Nixon Antony, 2/E, Maersk A/S<br>',
            '  Examination questions are reproduced for study purposes. For personal '
            'exam-preparation use. Not for redistribution. Corrections: '
            '<a href="mailto:%s">%s</a>' % (CONTACT, CONTACT),
            '</footer>']
