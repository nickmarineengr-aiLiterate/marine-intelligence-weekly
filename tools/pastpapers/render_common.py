#!/usr/bin/env python3
"""Shared rendering helpers for the Past Papers product.

Imported by build_paper.py and build_index.py so the paper and the two index
pages cannot drift in escaping, search-token construction, storage keys or
chrome. Nothing here reads the clock or the filesystem beyond the template
directory, so every generated file stays byte-reproducible.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
TPL = os.path.join(HERE, 'template')

BASE = 'https://marineintelligenceweekly.com'
CONTACT = 'contactus@marineintelligenceweekly.com'

# localStorage keys. Namespaced by product and schema so a future schema change
# cannot silently reinterpret old state. Values are keyed by stable question_id
# (EM2607-Q1), never by DOM order.
LS_BOOKMARKS = 'miw:pastpapers:v1:bookmarks'
LS_PROGRESS = 'miw:pastpapers:v1:progress'

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


def search_tokens(q, paper):
    """Deterministic search string for a question card.

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
        q.get('recurrence_class', ''),
    ]
    parts += q.get('topic_tags') or []
    parts += q.get('subject_tags') or []
    parts += q.get('intent_tags') or []
    parts += q.get('search_aliases') or []
    parts += q.get('regulations') or []
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


def topbar(active=''):
    """Consistent navigation across every Past Papers page. Kept compact."""
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
         '<title>%s</title>' % esc_attr(title),
         '<meta name="description" content="%s">' % esc_attr(description)]
    if publish:
        o.append('<meta name="robots" content="index, follow, max-image-preview:large">')
        o.append('<link rel="canonical" href="%s%s">' % (BASE, canonical_path))
        o.append('<meta property="og:type" content="article">')
        o.append('<meta property="og:title" content="%s">' % esc_attr(title))
        o.append('<meta property="og:description" content="%s">' % esc_attr(description))
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
