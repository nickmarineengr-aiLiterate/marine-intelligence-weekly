#!/usr/bin/env python3
"""MIW Engineering Management Notes — Part builder.

Assembles meoclass1/oralnotes/miw-notes-mgmt-p<N>.html from:
  - tools/notes/template/shell_head.html + shell_tail.html (extracted from a
    live reference Part by extract_template.py — carries CSS/JS verbatim)
  - a JSON content spec (see tools/notes/spec_schema.md)

Usage:
  python build_part.py <spec.json> [-o <outfile>] [--gated]

Design rule: the shell (CSS, watermark, topbar, scripts) is NEVER retyped —
it is lifted from the reference Part and only its variable text is rewritten.
This keeps per-Part authoring cost to the topic content alone.
"""
import argparse, html, io, json, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, 'template')
GATE = '<script>if(!/miw_auth=1/.test(document.cookie)){window.location.replace("/SQ/pay.html");}</script>'
GATE_STUB = '<!-- GATE SCRIPT STRIPPED FOR REVIEW COPY -->'
BASE = 'https://marineintelligenceweekly.com'
NOTES_DIR = BASE + '/meoclass1/oralnotes/'


def esc(s):
    """Escape only bare ampersands; allow inline tags and existing entities."""
    return re.sub(r'&(?![A-Za-z#][A-Za-z0-9]{1,8};)', '&amp;', str(s))


# ---------------------------------------------------------------- topic parts

def _body_nodes(nodes, out):
    for nd in nodes:
        if 'p' in nd:
            style = ' style="%s"' % nd['style'] if nd.get('style') else ''
            out.append('  <p class="notes-body"%s>%s</p>' % (style, esc(nd['p'])))
        elif 'ul' in nd:
            out.append('  <ul class="notes-list">')
            for li in nd['ul']:
                out.append('    <li>%s</li>' % esc(li))
            out.append('  </ul>')
        elif 'table' in nd:
            t = nd['table']
            out.append('  <table class="revision-table">')
            if t.get('head'):
                out.append('    <tr>' + ''.join('<th>%s</th>' % esc(c) for c in t['head']) + '</tr>')
            for row in t['rows']:
                out.append('    <tr>' + ''.join('<td>%s</td>' % esc(c) for c in row) + '</tr>')
            out.append('  </table>')
        elif 'ascii' in nd:
            out.append('  <div class="timeline-block">%s</div>' % esc(nd['ascii']))
        elif 'raw' in nd:
            out.append('  ' + nd['raw'])
        else:
            raise SystemExit('Unknown body node: %r' % nd)


def build_topic(part, t):
    n = t['n']
    tid = 'topic-p%d-%d' % (part, n)
    o = []
    o.append('<div class="topic-block" id="%s" data-kw="%s">' % (tid, esc(t.get('kw', ''))))
    o.append('  <div class="topic-header">')
    o.append('    <div class="topic-badge">Part %d · Topic %d</div>' % (part, n))
    o.append('    <div class="topic-title-wrap">')
    o.append('      <h2 class="topic-title">%s</h2>' % esc(t['title']))
    o.append('      <div class="topic-meta">')
    o.append('        <span class="topic-tag">%s</span>' % esc(t['tag']))
    o.append('        <span class="topic-pages">%s</span>' % esc(t['pages']))
    o.append('        <span class="topic-examiner">Examiner: %s</span>' % esc(t['examiner']))
    freq = t.get('freq', 'high')
    label = {'high': '⭐ High Frequency', 'medium': '◆ Medium Frequency'}[freq]
    o.append('        <span class="freq-%s">%s</span>' % (freq, label))
    o.append('      </div>')
    o.append('    </div>')
    o.append('  </div>')
    o.append('')

    if t.get('verify'):
        o.append('  <div class="verify-note">')
        o.append('    🔎 <strong>Verification note:</strong> %s' % esc(t['verify']))
        o.append('  </div>')
        o.append('')

    o.append('  <div class="section-head">📖 Definition</div>')
    o.append('  <p class="notes-body">%s</p>' % esc(t['definition']))
    o.append('')

    o.append('  <div class="section-head">⚓ Why It Matters (CE Perspective)</div>')
    o.append('  <ul class="notes-list">')
    for li in t['why']:
        o.append('    <li>%s</li>' % esc(li))
    o.append('  </ul>')
    o.append('')

    if t.get('timeline'):
        o.append('  <div class="section-head">📅 Historical Background</div>')
        rows = ['<span class="t-year">%s</span>  %s' % (esc(y), esc(d)) for y, d in t['timeline']]
        o.append('  <div class="timeline-block">' + '\n'.join(rows) + '</div>')
        o.append('')

    if t.get('regs'):
        r = t['regs']
        o.append('  <div class="section-head">⚖ Regulatory References</div>')
        o.append('  <div class="reg-box">')
        o.append('    <div class="reg-box-title">%s</div>' % esc(r.get('title', 'Key Instruments')))
        for code, desc in r['items']:
            o.append('    <div class="reg-item"><span class="reg-code">%s</span>'
                     '<span class="reg-desc">%s</span></div>' % (esc(code), esc(desc)))
        o.append('  </div>')
        o.append('')

    for sec in t.get('sections', []):
        o.append('  <div class="section-head">%s</div>' % esc(sec['head']))
        _body_nodes(sec['body'], o)
        o.append('')

    if t.get('ce_tip'):
        c = t['ce_tip']
        o.append('  <div class="ce-tip"><strong>🎓 CE Oral Tip (%s):</strong> %s</div>'
                 % (esc(c.get('examiner', t['examiner'])), esc(c['text'])))
        o.append('')

    o.append('  <div class="section-head">🎯 Oral Q&amp;A</div>')
    o.append('  <div class="qa-block">')
    for i, (q, a) in enumerate(t['qa'], 1):
        q = q if re.match(r'^Q\d+\.', q) else 'Q%d. %s' % (i, q)
        o.append('    <div class="qa-item"><div class="qa-q">%s</div>'
                 '<div class="qa-a">%s</div></div>' % (esc(q), esc(a)))
    o.append('  </div>')
    o.append('')

    o.append('  <div class="exam-focus-box">')
    o.append('    <div class="exam-focus-head">✍ Written Exam Focus</div>')
    for marks, q in t['exam']:
        o.append('    <div class="exam-q"><span class="marks-badge">%s</span>%s</div>'
                 % (esc(marks), esc(q)))
    o.append('  </div>')
    o.append('')

    o.append('  <div class="memory-box">')
    o.append('    <div class="memory-head">🧠 Memory Box</div>')
    o.append('    <ul class="memory-list">')
    for li in t['memory']:
        o.append('      <li>%s</li>' % esc(li))
    o.append('    </ul>')
    o.append('  </div>')
    o.append('')

    if t.get('deep_dive'):
        d = t['deep_dive']
        o.append('  <div class="deep-dive">')
        o.append('    <button class="deep-dive-toggle" onclick="toggleDD(this)">▶ Deep Dive — %s</button>'
                 % esc(d['title']))
        o.append('    <div class="deep-dive-body">')
        for tag, txt in d['blocks']:
            o.append('      <%s>%s</%s>' % (tag, esc(txt), tag))
        o.append('    </div>')
        o.append('  </div>')
        o.append('')

    o.append('  <div class="section-head">📚 References</div>')
    o.append('  <ul class="ref-list">')
    for li in t['refs']:
        o.append('    <li>%s</li>' % esc(li))
    o.append('  </ul>')
    o.append('')

    o.append('  <div class="topic-footer">')
    o.append('    <div class="correction-link">Found an error? <a href="mailto:contactus@'
             'marineintelligenceweekly.com?subject=Notes-p%d · Topic %d · Correction Required">'
             'Report correction</a></div>' % (part, n))
    o.append('    <div class="topic-version">Notes-p%d · P%d-T%d · v%s</div>'
             % (part, part, n, t.get('version', '1.0')))
    o.append('  </div>')
    o.append('</div>')
    return '\n'.join(o)


# ---------------------------------------------------------------- page shell

def _sub(pat, repl, s, label):
    new, n = re.subn(pat, lambda m: repl, s, count=1, flags=re.S)
    if n != 1:
        raise SystemExit('Shell rewrite failed (%d matches) for: %s' % (n, label))
    return new


def render_shell(head, tail, sp):
    p = sp['part']
    fname = 'miw-notes-mgmt-p%d.html' % p
    topics = sp['topics']

    head = _sub(r'<title>.*?</title>',
                '<title>MIW Engineering Management Notes — Part %d | MEO Class 1 | %s</title>'
                % (p, esc(sp['title_topics'])), head, 'title')
    head = _sub(r'(<meta name="description" content=").*?(">)',
                '<meta name="description" content="%s">' % esc(sp['meta_description']),
                head, 'description')
    head = _sub(r'(<link rel="canonical" href=").*?(">)',
                '<link rel="canonical" href="%s%s">' % (NOTES_DIR, fname), head, 'canonical')
    head = _sub(r'(<span class="notes-badge-text">).*?(</span>)',
                '<span class="notes-badge-text">Engineering Management · Part %d of 31</span>' % p,
                head, 'notes-badge-text')
    head = _sub(r'<h1 class="page-title">.*?</h1>',
                '<h1 class="page-title">Engineering Management Notes — Part %d</h1>' % p,
                head, 'h1')
    head = _sub(r'<p class="page-sub">.*?</p>',
                '<p class="page-sub">%s</p>' % esc(sp['page_sub']), head, 'page-sub')

    meta = ['<div class="header-meta">']
    meta.append('            <span class="header-meta-item"><strong>Pages:</strong> %s of %s</span>'
                % (sp['pages'], sp.get('total_pages', 768)))
    meta.append('            <span class="header-meta-item"><strong>Topics:</strong> %d '
                '(local P%d-T1–P%d-T%d — see note below)</span>'
                % (len(topics), p, p, len(topics)))
    meta.append('            <span class="header-meta-item"><strong>Access:</strong> Subscriber Only</span>')
    meta.append('            <span class="header-meta-item"><strong>Subject:</strong> Engineering Management</span>')
    meta.append('            <span class="header-meta-item"><strong>Exam:</strong> MEO Class 1 — Kochi MMD</span>')
    meta.append('        </div>')
    head = _sub(r'<div class="header-meta">.*?</div>\s*(?=<div class="attribution-strip">)',
                '\n'.join(meta) + '\n        ', head, 'header-meta')

    prev = sp.get('prev_part')
    seq = ('Originally compiled by <strong>Uday Sankar S., Anglo-Eastern</strong>. Transcribed, expanded '
           'and verified by <strong>Nixon Antony, 2/E, Maersk A/S</strong> for Marine Intelligence Weekly. '
           '<strong>Sequencing note:</strong> Part %d (pp. %s) continues directly from Part %d (pp. %s). '
           'Topic numbering below uses local <strong>Part %d</strong> badges (not a continuous global '
           'T-number), consistent with the platform\'s standing rule to defer global renumbering until all '
           '31 Parts are confirmed live.' % (p, sp['pages'], prev, sp['prev_pages'], p))
    head = _sub(r'(<div class="attribution-strip">).*?(</div>)',
                '<div class="attribution-strip">\n            %s\n        </div>' % seq,
                head, 'attribution-strip')

    sb = ['<aside class="sidebar">']
    sb.append('    <div class="toc-head">Topics · Part %d</div>' % p)
    for t in topics:
        sb.append('    <a class="toc-link" href="#topic-p%d-%d">T%d · %s</a>'
                  % (p, t['n'], t['n'], esc(t.get('toc', t['title']))))
    sb.append('    <div class="toc-divider"></div>')
    sb.append('    <div class="toc-head">Navigate</div>')
    sb.append('    <a class="toc-link" href="%s">← Notes Index</a>' % NOTES_DIR)
    if prev:
        sb.append('    <a class="toc-link" href="miw-notes-mgmt-p%d.html">← Part %d</a>' % (prev, prev))
    if sp.get('next_part'):
        sb.append('    <a class="toc-link" href="miw-notes-mgmt-p%d.html">Part %d →</a>'
                  % (sp['next_part'], sp['next_part']))
    sb.append('    <div class="toc-divider"></div>')
    sb.append('    <div class="qb-sidebar-box">')
    sb.append('        <div class="qb-sidebar-title">🔗 Related QB Files</div>')
    for href, label in sp.get('qb_links', []):
        sb.append('        <a class="qb-sidebar-link" href="%s">%s</a>' % (href, esc(label)))
    sb.append('    </div>')
    sb.append('</aside>')
    head = _sub(r'<aside class="sidebar">.*?</aside>', '\n'.join(sb), head, 'sidebar')

    # drop the reference file's leftover topic-comment banner
    head = re.sub(r'<!-- =+ -->\s*<!-- TOPIC 1 .*?-->\s*<!-- =+ -->\s*$', '', head, flags=re.S)

    if not sp.get('gated'):
        head = head.replace(GATE, GATE_STUB)

    foot = ['<div class="page-footer">']
    foot.append('    Part %d of 31 · Pages %s of %s · Engineering Management Notes — '
                'Marine Intelligence Weekly<br>' % (p, sp['pages'], sp.get('total_pages', 768)))
    foot.append('    Originally compiled by Uday Sankar S., Anglo-Eastern. Transcribed, expanded and '
                'verified by Nixon Antony, 2/E, Maersk A/S.<br>')
    foot.append('    This is subscriber-only content for MEO Class 1 exam preparation (Kochi MMD). '
                'Unauthorized redistribution is prohibited.<br>')
    foot.append('    Found an error? <a href="mailto:contactus@marineintelligenceweekly.com?subject='
                'Notes-p%d · Correction Required">Contact us</a> ·' % p)
    foot.append('    <a href="%s">← Back to Notes Index</a>' % NOTES_DIR)
    foot.append('</div>')
    tail = _sub(r'<div class="page-footer">.*?</div>\s*(?=<script>)',
                '\n'.join(foot) + '\n\n', tail, 'page-footer')
    return head, tail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('spec')
    ap.add_argument('-o', '--out')
    ap.add_argument('--gated', action='store_true')
    a = ap.parse_args()

    sp = json.load(open(a.spec, encoding='utf-8'))
    if a.gated:
        sp['gated'] = True
    head = open(os.path.join(TPL, 'shell_head.html'), encoding='utf-8').read()
    tail = open(os.path.join(TPL, 'shell_tail.html'), encoding='utf-8').read()
    head, tail = render_shell(head, tail, sp)

    body = []
    for t in sp['topics']:
        bar = '<!-- ' + '=' * 74 + ' -->'
        body.append('\n%s\n<!-- TOPIC %d — %s -->\n%s\n'
                    % (bar, t['n'], t.get('toc', t['title']).upper(), bar))
        body.append(build_topic(sp['part'], t))
    out = head + '\n'.join(body) + tail

    dest = a.out or os.path.join(HERE, '..', '..', 'meoclass1', 'oralnotes',
                                 'miw-notes-mgmt-p%d.html' % sp['part'])
    dest = os.path.abspath(dest)
    with open(dest, 'w', encoding='utf-8', newline='\n') as f:
        f.write(out)
    print('BUILT  :', dest)
    print('BYTES  :', len(out.encode('utf-8')))
    print('TOPICS :', len(sp['topics']))
    print('GATED  :', bool(sp.get('gated')))


if __name__ == '__main__':
    main()
