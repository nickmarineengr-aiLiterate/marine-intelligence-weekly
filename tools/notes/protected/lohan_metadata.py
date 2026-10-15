#!/usr/bin/env python3
"""Generate the LOHAN series metadata in its two forms (O-3, Founder FD-P2, 15 Oct 2026).

  full   (PRIVATE; packaged into the protected release and mounted behind ORAL_QB_NOTES):
         titles, topic summaries and keywords on the Notes index cards and in the manifest,
         topic titles in source_nodes.csv.
  public (committed to the public repository): IDs, part numbers and counts only. Card
         titles become "Part N", summaries and keywords are dropped, and registry titles
         become the topic ID (P<N>-T<n>).

Both forms carry the same series identity ("MIW MEO Class 1 Engineering Study Standard"),
attribution, live state and the Founder-approved disclaimer v1.0 (the text is MIW's own
and public). Nothing outside the LOHAN section, entry or rows is changed.

Inputs come from a tree that holds the private overlay (specs and the full metadata from
the private content repository): --source-tree. The base files to splice into come from
--base-tree (the public tree).

usage: python tools/notes/protected/lohan_metadata.py --source-tree S --base-tree B --out-tree O --form full|public
"""
from __future__ import annotations

import argparse
import csv
import html
import io
import json
import os
import re
import sys

SERIES_KEY = 'lohan-notes'
NAME = 'MIW MEO Class 1 Engineering Study Standard'
INDEX_REL = 'meoclass1/oralnotes/index.html'
MANIFEST_REL = 'meoclass1/oralnotes/notes_content_index.json'
NODES_REL = 'tools/notes/canonical/source_nodes.csv'
DISCLAIMER_TXT_REL = 'tools/notes/policy/study_material_disclaimer_v1.0.txt'
SECTION_RE = re.compile(r'  <div class="series-block" id="sec-lohan-notes">.*?(?=\n  <!-- WRITTEN QUESTION NOTES SERIES -->)', re.S)
INSERT_BEFORE = '\n  <!-- WRITTEN QUESTION NOTES SERIES -->'
DISC_LINK = '<a href="#miw-study-material-disclaimer">MIW Study Material Disclaimer v1.0 (October 2026)</a>'
ATTRIBUTION_TEXT = (NAME + ' — October 2026. An independent MIW study standard, compiled, updated and verified by '
                    'Marine Intelligence Weekly and aligned with the DGMA MEO Class I syllabus; not approved, endorsed '
                    'or issued by DGMA. Verified baseline: September 2026. See the MIW Study Material Disclaimer v1.0 '
                    '(October 2026).')
ATTRIBUTION_HTML = ('<strong>' + NAME + ' — October 2026.</strong> An independent MIW study standard, compiled, '
                    'updated and verified by Marine Intelligence Weekly and aligned with the DGMA MEO Class I syllabus; '
                    'not approved, endorsed or issued by DGMA. <strong>Verified baseline: September 2026.</strong> '
                    'Read the ' + DISC_LINK + ' before relying on these notes.')
SERIES_STATUS = 'gated - live - Parts 1-21 (123 topics)'
FILE_STATUS = 'gated - live'


def read(p):
    with open(p, encoding='utf-8', newline='') as fh:
        return fh.read()


def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='') as fh:
        fh.write(s)


def disclaimer_html(txt: str) -> str:
    """Render the approved plain-text disclaimer. No nested <div> (the checker reads to the
    first </div>). Each numbered clause becomes a paragraph; the footer is the last line."""
    lines = [l.strip() for l in txt.strip().split('\n') if l.strip()]
    title = lines[0]
    out = ['<strong>%s</strong>' % html.escape(title, quote=False)]
    for l in lines[1:]:
        if l == 'Page footer:':
            continue
        out.append('<p>%s</p>' % html.escape(l, quote=False))
    return '\n      '.join(out)


def load_manifest_raw(s):
    return json.loads(s)


def card(n, entry, form):
    href = 'lohan-notes-p%d.html' % n
    k = entry['topic_count']
    if form == 'full':
        kw = html.escape(entry['_kw'], quote=True)
        title = html.escape(entry['title'], quote=False)
        sub = html.escape(entry['summary'], quote=False)
        return ('      <a class="note-card available" href="%s" data-kw="%s">\n'
                '        <div class="nc-header">\n'
                '          <span class="nc-part">Engineering Standard · Part %d</span>\n'
                '          <span class="nc-status ncs-live">✅ Live</span>\n'
                '        </div>\n'
                '        <div class="nc-title">%s</div>\n'
                '        <div class="nc-sub">%s</div>\n'
                '        <div class="nc-pages">📄 %d topics</div>\n'
                '        <div class="nc-btn">Open Part %d</div>\n'
                '      </a>\n' % (href, kw, n, title, sub, k, n))
    return ('      <a class="note-card available" href="%s">\n'
            '        <div class="nc-header">\n'
            '          <span class="nc-part">Engineering Standard · Part %d</span>\n'
            '          <span class="nc-status ncs-live">✅ Live</span>\n'
            '        </div>\n'
            '        <div class="nc-title">Part %d</div>\n'
            '        <div class="nc-pages">📄 %d topics · %s</div>\n'
            '        <div class="nc-btn">Open Part %d</div>\n'
            '      </a>\n' % (href, n, n, k, entry['topic_range'], n))


def section(entries, form, disc_html):
    total_topics = sum(e['topic_count'] for e in entries.values())
    head = ('  <div class="series-block" id="sec-lohan-notes">\n'
            '    <div class="series-title">\n'
            '      <h2>📒 %s</h2>\n'
            '      <span class="series-badge sb-live">Parts 1–21 Live · %d topics · Verified baseline September 2026</span>\n'
            '    </div>\n'
            '    <p class="series-attrib">%s</p>\n'
            '    <div class="series-attrib" id="miw-study-material-disclaimer">\n      %s\n    </div>\n'
            '    <div class="notes-grid">\n\n' % (NAME, total_topics, ATTRIBUTION_HTML, disc_html))
    cards = '\n'.join(card(n, entries[n], form) for n in sorted(entries))
    return head + cards + '\n    </div>\n  </div>\n'


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--source-tree', required=True)
    ap.add_argument('--base-tree', required=True)
    ap.add_argument('--out-tree', required=True)
    ap.add_argument('--form', choices=('full', 'public'), required=True)
    a = ap.parse_args(argv)
    S, B, O = a.source_tree, a.base_tree, a.out_tree
    j = lambda root, rel: os.path.join(root, *rel.split('/'))

    # ---- source facts: the private manifest entry (titles, summaries) and the specs (keywords)
    src_man = json.loads(read(j(S, MANIFEST_REL)))
    src_ser = src_man['series'][SERIES_KEY]
    entries = {}
    for fn, v in src_ser['files'].items():
        n = int(re.match(r'lohan-notes-p(\d+)\.html$', fn).group(1))
        spec = json.loads(read(j(S, 'tools/notes/specs/lohan/p%d.json' % n)))
        kws = [t.get('kw', '') for t in spec['topics']]
        entries[n] = {'title': v['title'], 'summary': v['summary'], 'topic_count': len(spec['topics']),
                      'topic_range': 'P%d-T1–P%d-T%d' % (n, n, len(spec['topics'])),
                      'last_verified': v['last_verified'], '_kw': ', '.join(k for k in kws if k)}
        if entries[n]['topic_count'] != v['topic_count']:
            sys.exit('ABORT: p%d topic_count manifest %s != spec %s' % (n, v['topic_count'], entries[n]['topic_count']))
    if sorted(entries) != list(range(1, 22)):
        sys.exit('ABORT: LOHAN parts are not exactly 1..21')
    for n, e in entries.items():
        for f in ('title', 'summary', '_kw'):
            if re.search(r'Lohan|LOHAN|Source PDF', e[f]):
                sys.exit('ABORT: p%d %s still names the source' % (n, f))

    disc_txt = read(j(B, DISCLAIMER_TXT_REL))
    disc = disclaimer_html(disc_txt)

    # ---- index.html: splice the LOHAN section into the base index
    base_index = read(j(B, INDEX_REL))
    sec = section(entries, a.form, disc)
    if SECTION_RE.search(base_index):
        new_index = SECTION_RE.sub(lambda m: sec.rstrip('\n'), base_index, count=1)
    else:
        if base_index.count(INSERT_BEFORE) != 1:
            sys.exit('ABORT: insertion anchor not found exactly once in the base index')
        new_index = base_index.replace(INSERT_BEFORE, '\n' + sec.rstrip('\n') + '\n' + INSERT_BEFORE, 1)
    write(j(O, INDEX_REL), new_index)

    # ---- manifest: replace the LOHAN series entry; keep key order and every other series
    base_man_raw = read(j(B, MANIFEST_REL))
    base_man = json.loads(base_man_raw)
    files = {}
    for n in sorted(entries):
        e = entries[n]
        rec = {'part': n}
        if a.form == 'full':
            rec['title'] = e['title']
        else:
            rec['title'] = 'Part %d' % n
        rec['topic_count'] = e['topic_count']
        rec['topic_range'] = e['topic_range']
        if a.form == 'full':
            rec['summary'] = e['summary']
        rec['status'] = FILE_STATUS
        rec['last_verified'] = e['last_verified']
        files['lohan-notes-p%d.html' % n] = rec
    ser = {'series_name': NAME,
           'source_attribution': ATTRIBUTION_TEXT,
           'series_identity': 'Independent MIW study standard (internal key lohan-notes); NOT a continuation of the '
                              'Engineering Management series and NOT canonical-topic pages',
           'file_naming_convention': 'lohan-notes-p<N>.html',
           'status': SERIES_STATUS,
           'files': files}
    base_man['series'][SERIES_KEY] = ser
    base_man['total_files'] = sum(len(v.get('files') or {}) for v in base_man['series'].values())
    indent = next(i for i in (2, 1, 4) if json.dumps(json.loads(base_man_raw), ensure_ascii=False, indent=i) in base_man_raw) \
        if any(json.dumps(json.loads(base_man_raw), ensure_ascii=False, indent=i) in base_man_raw for i in (2, 1, 4)) else 2
    nl = '\r\n' if '\r\n' in base_man_raw else '\n'
    out = json.dumps(base_man, ensure_ascii=False, indent=indent)
    if nl != '\n':
        out = out.replace('\n', nl)
    write(j(O, MANIFEST_REL), out + (nl if base_man_raw.endswith(('\n',)) else ''))

    # ---- source_nodes.csv: LOHAN rows from the private registry, retitled for the public form
    src_rows = list(csv.reader(io.StringIO(read(j(S, NODES_REL)))))
    base_raw = read(j(B, NODES_REL))
    base_rows = list(csv.reader(io.StringIO(base_raw)))
    hdr = base_rows[0]
    ti, si, pi, oi, ki = (hdr.index(c) for c in ('title', 'publication_status', 'part', 'ordinal_in_part', 'series'))
    lohan = [r for r in src_rows[1:] if r[ki] == 'LOHAN' or r[0].startswith('lohan')]
    if len(lohan) != 123:
        sys.exit('ABORT: %d LOHAN registry rows, expected 123' % len(lohan))
    kept = [r for r in base_rows[1:] if not (r[ki] == 'LOHAN' or r[0].startswith('lohan'))]
    for r in lohan:
        r[si] = 'PUBLISHED_LIVE'
        if a.form == 'public':
            r[ti] = 'P%s-T%s' % (r[pi], r[oi])
    nl = '\r\n' if '\r\n' in base_raw else '\n'
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator=nl)
    w.writerow(hdr)
    w.writerows(kept + lohan)
    write(j(O, NODES_REL), buf.getvalue())
    print(json.dumps({'form': a.form, 'parts': len(entries), 'topics': sum(e['topic_count'] for e in entries.values()),
                      'registry_rows': len(lohan), 'total_files': base_man['total_files']}))


if __name__ == '__main__':
    main()
