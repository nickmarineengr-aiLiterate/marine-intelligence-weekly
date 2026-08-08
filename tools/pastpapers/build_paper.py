#!/usr/bin/env python3
"""MIW past written papers -- deterministic interactive paper builder.

Usage:
  python build_paper.py <spec.json> [-o <outfile>] [--gated] [--publish]

Assembles meoclass1/pastpapers/<PAPER_ID>.html from:
  - template/style.css      (verbatim from a live reference file, via extract_shell.py)
  - template/pastpapers.css (this product's styles)
  - template/paper.js       (client behaviour)
  - a JSON content spec (validated first by validate_spec.py)

Interaction model follows meoclass1/QB10_A.html. Every question becomes a
collapsible card carrying a Model Written Answer, an expandable Study Guide and
a Quick Revision block, all generated from the one canonical question object --
no answer text is ever duplicated across files.

Modes:
  default   Founder review: noindex, quality banner, production metadata visible
            in a collapsed per-question block.
  --publish Student-facing: full SEO head, JSON-LD, production metadata omitted.
  --gated   Adds the access gate. The review workflow never uses it.

Determinism: no clock reading, no random value, no absolute path. Every date
rendered comes from the spec, so re-running with an unchanged spec is
byte-identical -- audit_paper.py asserts this.
"""
import argparse, io, json, os, re, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import (REPO_ROOT, TPL, BASE, CONTACT, LS_BOOKMARKS, LS_PROGRESS,
                           LS_MIGRATE_JS, STICKY_SYNC_JS, GATE, GATE_STUB, esc, esc_attr, strip_tags,
                           read_css, block_text, search_tokens, topbar, head_meta, footer)

CHEV = ('<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>')


# ------------------------------------------------------------------ blocks

def render_blocks(blocks, out, indent='    '):
    for nd in blocks.get('blocks', []):
        if 'h' in nd:
            out.append('%s<h3>%s</h3>' % (indent, esc(nd['h'])))
        elif 'p' in nd:
            out.append('%s<p>%s</p>' % (indent, esc(nd['p'])))
        elif 'ul' in nd:
            out.append('%s<ul>' % indent)
            for li in nd['ul']:
                out.append('%s  <li>%s</li>' % (indent, esc(li)))
            out.append('%s</ul>' % indent)
        elif 'ol' in nd:
            out.append('%s<ol>' % indent)
            for li in nd['ol']:
                out.append('%s  <li>%s</li>' % (indent, esc(li)))
            out.append('%s</ol>' % indent)
        elif 'table' in nd:
            t = nd['table']
            out.append('%s<table class="reg-tbl">' % indent)
            out.append('%s  <tr>%s</tr>' % (
                indent, ''.join('<th>%s</th>' % esc(h) for h in t['headers'])))
            for row in t['rows']:
                out.append('%s  <tr>%s</tr>' % (
                    indent, ''.join('<td>%s</td>' % esc(c) for c in row)))
            out.append('%s</table>' % indent)
        else:
            raise ValueError('unknown block type: %r' % list(nd.keys()))


# ------------------------------------------------------------------ card

def quick_revision(qr, out):
    out.append('  <section class="layer qr" aria-label="Quick revision">')
    out.append('    <div class="layer-title">Quick revision</div>')
    out.append('    <dl>')
    if qr.get('recall_15s'):
        out.append('      <dt>15-second recall</dt><dd>%s</dd>' % esc(qr['recall_15s']))
    # The skeleton is NOT repeated here. It renders once per card, as the Exam
    # Approach block above the model answer, where it does its actual job:
    # showing the shape of the answer before the prose rather than after it.
    if qr.get('keywords'):
        out.append('      <dt>Keywords</dt><dd>%s</dd>'
                   % ''.join('<span class="kw">%s</span>' % esc(k) for k in qr['keywords']))
    if qr.get('critical_numbers'):
        out.append('      <dt>Critical numbers</dt><dd><ul>')
        for n in qr['critical_numbers']:
            out.append('        <li>%s</li>' % esc(n))
        out.append('      </ul></dd>')
    if qr.get('critical_regulation'):
        out.append('      <dt>Critical regulation</dt><dd>%s</dd>' % esc(qr['critical_regulation']))
    if qr.get('major_trap'):
        out.append('      <dt>Major trap</dt><dd class="trap">%s</dd>' % esc(qr['major_trap']))
    out.append('    </dl>')
    out.append('  </section>')


def exam_approach(q, out):
    """The answer skeleton, rendered BEFORE the model answer.

    Purpose is exam-writing, not revision: it is the map a candidate plans on
    paper in the first two minutes. Placing it after the full model answer --
    which is where it used to live, inside Quick Revision -- meant a student
    only met the plan once they had already read the finished essay.

    Always visible inside the card body rather than a nested <details>. Cards
    are collapsed by default, so this adds nothing to the list view, and a
    plan that has to be un-hidden is a plan that gets skipped. It renders from
    quick_revision.skeleton, so there is still exactly one copy of this text in
    the spec feeding both this block and the paper-level Rapid Revision table.
    """
    skel = (q.get('quick_revision') or {}).get('skeleton') or []
    if not skel:
        return
    out.append('  <section class="layer skel" aria-label="Exam approach">')
    out.append('    <div class="layer-title">Exam approach &mdash; answer skeleton '
               '<span class="skel-marks">%s marks</span></div>' % q['total_marks'])
    out.append('    <ol class="skel-list">')
    for s in skel:
        out.append('      <li>%s</li>' % esc(s))
    out.append('    </ol>')
    out.append('  </section>')


def build_card(q, paper, out, publish):
    qid = q['question_id']
    subjects = ' '.join((q.get('subject_tags') or [])).lower()
    out.append('<article class="q-card" id="%s" data-qid="%s" data-subjects="%s" data-search="%s">'
               % (q['anchor'], esc_attr(qid), esc_attr(subjects),
                  esc_attr(search_tokens(q, paper))))
    out.append('  <div class="q-head">')
    out.append('    <button class="q-toggle" type="button" aria-expanded="false" '
               'aria-controls="%s-body">' % esc_attr(q['anchor']))
    out.append('      <span class="q-num">%s</span>' % esc(q['q_no']))
    out.append('      <span class="q-main">')
    out.append('        <span class="q-title">%s</span>' % esc(q.get('short_title', q['q_no'])))
    rec = q.get('recurrence_class', 'new')
    rec_label = {'new': 'New', 'topic_recurrence': 'Topic recurs',
                 'near_recurrence': 'Near repeat', 'exact_recurrence': 'Exact repeat'}.get(rec, rec)
    out.append('        <span class="q-meta">%s marks<span class="sep">&middot;</span>%s'
               '<span class="sep">&middot;</span>%s</span>'
               % (q['total_marks'], esc(paper['month_year']), esc(rec_label)))
    for line in q['text_verbatim'].split('\n'):
        out.append('        <span class="q-stem">%s</span>' % esc(line))
    out.append('        <span class="q-tags">')
    for t in (q.get('subject_tags') or []):
        out.append('          <span class="q-tag">%s</span>' % esc(t))
    for t in (q.get('topic_tags') or [])[:4]:
        out.append('          <span class="q-tag sub">%s</span>' % esc(t))
    if q.get('prior_sittings'):
        out.append('          <span class="q-tag rec">%d prior sitting%s</span>'
                   % (q['prior_sittings'], '' if q['prior_sittings'] == 1 else 's'))
    out.append('        </span>')
    out.append('      </span>')
    out.append('      %s' % CHEV)
    out.append('    </button>')
    out.append('    <div class="q-acts">')
    out.append('      <button class="icon-btn bm" type="button" aria-pressed="false" '
               'aria-label="Bookmark %s" title="Bookmark this question">&#9733;</button>' % esc_attr(qid))
    out.append('      <button class="icon-btn st" type="button" aria-pressed="false" '
               'aria-label="Mark %s as studied" title="Mark as studied">&#10003;</button>' % esc_attr(qid))
    out.append('    </div>')
    out.append('  </div>')

    out.append('  <div class="q-body" id="%s-body" hidden>' % esc_attr(q['anchor']))

    exam_approach(q, out)

    out.append('  <section class="layer ma" aria-label="Model written answer">')
    out.append('    <div class="layer-title">Model written answer</div>')
    render_blocks(q['model_answer'], out)
    out.append('  </section>')

    out.append('  <details class="layer sg">')
    out.append('    <summary>Study guide</summary>')
    out.append('    <div class="inner">')
    render_blocks(q['study_notes'], out, indent='      ')
    out.append('    </div>')
    out.append('  </details>')

    quick_revision(q.get('quick_revision') or {}, out)

    xl = q.get('cross_links') or []
    if xl:
        out.append('  <p class="rec-note">Also on the platform: %s</p>'
                   % ' &middot; '.join('<a href="%s">%s</a>'
                                       % (esc_attr(x['href']), esc(x['label'])) for x in xl))
    if q.get('recurrence'):
        out.append('  <p class="rec-note">Recurrence recorded on the source paper: %s. %s</p>'
                   % (', '.join(esc(r) for r in q['recurrence']),
                      esc(q.get('recurrence_note', ''))))

    # Production metadata: review mode only. Never shipped to students.
    if not publish:
        out.append('  <details class="prod-meta">')
        out.append('    <summary>Production metadata (review build only)</summary>')
        out.append('    <div class="pm-inner">')
        out.append('      <b>Reuse tier</b> %s &middot; <b>Verification</b> %s'
                   % (esc(q.get('reuse_tier') or '?'), esc(q.get('verification_status') or '')))
        ps = q.get('provenance_summary') or {}
        if ps:
            out.append('      <br><b>Provenance</b> %s'
                       % esc(' · '.join('%s %s' % (k, v) for k, v in ps.items() if v)))
        if q.get('sources'):
            out.append('      <br><b>Sources</b><ul>')
            for s in q['sources']:
                out.append('        <li>%s</li>' % esc(s))
            out.append('      </ul>')
        if q.get('unresolved'):
            out.append('      <b>Unresolved</b><ul>')
            for u in q['unresolved']:
                out.append('        <li>%s</li>' % esc(u))
            out.append('      </ul>')
        rv = q.get('reverify_before_publication') or []
        if rv:
            out.append('      <b>Re-verify before publication</b><ul>')
            for r in rv:
                out.append('        <li>%s &mdash; %s <i>(%s)</i></li>'
                           % (esc(r.get('claim', '')), esc(r.get('why', '')), esc(r.get('class', ''))))
            out.append('      </ul>')
        out.append('    </div>')
        out.append('  </details>')

    out.append('  </div>')
    out.append('</article>')


# ------------------------------------------------------------------ document

def build(spec, gated=False, publish=False):
    d = spec
    pid = d['paper_id']
    qs = d['questions']
    built = [q for q in qs if q.get('model_answer')]

    title = ('%s %s &mdash; MEO Class I Written Questions & Answers | Marine Intelligence Weekly'
             % (d['subject'], d['month_year']))
    desc = ('All %d questions from the %s MEO Class I %s written paper (%s), with model written '
            'answers, study guides and quick revision.'
            % (len(qs), d['month_year'], d['subject'], d['sr_no']))

    o = []
    a = o.append

    extra = []
    ld = {'@context': 'https://schema.org', '@type': 'LearningResource',
          'name': '%s %s -- MEO Class I Written Questions and Answers' % (d['subject'], d['month_year']),
          'description': strip_tags(desc),
          'educationalLevel': 'MEO Class I (Marine Engineer Officer, Management Level)',
          'learningResourceType': 'Past examination paper with model answers',
          'inLanguage': 'en',
          'about': sorted({t for q in qs for t in (q.get('subject_tags') or [])}),
          'isPartOf': {'@type': 'Collection', 'name': 'MIW MEO Class I Written Questions & Answers',
                       'url': '%s/meoclass1/pastpapers/' % BASE},
          'version': d['version']}
    if publish:
        ld['url'] = '%s/meoclass1/pastpapers/%s.html' % (BASE, pid)
        # Honest representation: an ordered list of the actual exam questions, each
        # carrying a real short answer. Not FAQPage -- these are examination
        # questions with model answers, not frequently asked questions.
        ld['hasPart'] = [{
            '@type': 'Question',
            'position': i + 1,
            'name': strip_tags(q['text_verbatim']),
            'url': '%s/meoclass1/pastpapers/%s.html#%s' % (BASE, pid, q['anchor']),
            'answerCount': 1,
            'acceptedAnswer': {'@type': 'Answer',
                               'text': strip_tags((q.get('quick_revision') or {}).get('recall_15s', ''))},
        } for i, q in enumerate(built) if (q.get('quick_revision') or {}).get('recall_15s')]
        extra.append('<script type="application/ld+json">')
        extra.append(json.dumps(ld, indent=2, ensure_ascii=False))
        extra.append('</script>')
        extra.append('<script type="application/ld+json">')
        extra.append(json.dumps({
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Marine Intelligence Weekly', 'item': BASE},
                {'@type': 'ListItem', 'position': 2, 'name': 'MEO Class I', 'item': '%s/meoclass1/' % BASE},
                {'@type': 'ListItem', 'position': 3, 'name': 'Written Questions & Answers',
                 'item': '%s/meoclass1/pastpapers/' % BASE},
                {'@type': 'ListItem', 'position': 4, 'name': '%s %s' % (d['subject'], d['month_year'])},
            ]}, indent=2, ensure_ascii=False))
        extra.append('</script>')

    o.extend(head_meta(strip_tags(title), strip_tags(desc),
                       '/meoclass1/pastpapers/%s.html' % pid, publish, extra))
    a('<style>')
    a(read_css())
    a('</style>')
    a('</head>')
    a('')
    a('<body>')
    a(GATE if gated else GATE_STUB)
    a('<a class="skip" href="#paper-main">Skip to questions</a>')
    a('')
    o.extend(topbar('Written Questions'))
    a('')
    a('<header class="page-header">')
    a('  <div class="wrap">')
    a('    <span class="badge">Written Questions &amp; Answers &middot; %s</span>' % esc(d['sr_no']))
    a('    <h1>%s &mdash; %s</h1>' % (esc(d['subject']), esc(d['month_year'])))
    a('    <p class="sub">%s &middot; Function: %s &middot; %s</p>'
      % (esc(d['printed_authority']), esc(d['function']), esc(d['class'])))
    a('    <div class="header-meta">')
    a('      <span>Sr. No. %s</span>' % esc(d['sr_no']))
    a('      <span>%s</span>' % esc(d['time_allowed']))
    a('      <span>Total marks %s</span>' % esc(d['total_marks']))
    a('      <span>%d questions &middot; answer six</span>' % len(qs))
    a('      <span>%s</span>' % esc(d.get('region_note', '')))
    a('    </div>')
    a('  </div>')
    a('</header>')
    a('')

    if not publish:
        a('<div class="review-banner">')
        a('  <strong>Founder review copy &mdash; ungated, uncommitted, not published.</strong> '
          'Generated from <code>specs/%s.json</code> by the Past Papers toolchain. '
          'Build state <strong>%s</strong>, review state <strong>%s</strong>, version %s, '
          'updated %s. Production metadata is shown per question in this build only.'
          % (pid, esc(d['build_state']), esc(d['review_state']), esc(d['version']), esc(d['updated'])))
        a('</div>')

    # controls
    a('<div class="controls-bar">')
    a('  <div class="controls-inner">')
    a('    <label class="search-wrap">')
    a('      <span class="visually-hidden-label" aria-hidden="true">&#128269;</span>')
    a('      <input id="search-input" type="search" autocomplete="off" '
      'placeholder="Search questions, topics, regulations &mdash; e.g. general average, SOPEP, ammonia" '
      'aria-label="Search questions in this paper">')
    a('      <button id="search-clear" class="icon-btn" type="button" aria-label="Clear search">&times;</button>')
    a('    </label>')
    for key, label in [('all', 'All'), ('bookmarked', 'Bookmarked'),
                       ('unstudied', 'Not studied'), ('studied', 'Studied')]:
        a('    <button class="filter-btn" type="button" data-filter="%s" aria-pressed="%s">%s</button>'
          % (key, 'true' if key == 'all' else 'false', label))
    for s in sorted({t for q in qs for t in (q.get('subject_tags') or [])}):
        a('    <button class="filter-btn" type="button" data-filter="%s" aria-pressed="false">%s</button>'
          % (esc_attr(s.lower()), esc(s)))
    a('    <button id="reset-progress" class="filter-btn" type="button">Clear my progress</button>')
    a('    <span class="count-label" id="count-label" role="status" aria-live="polite"></span>')
    a('  </div>')
    a('</div>')
    a('')

    a('<div class="main-layout">')
    a('<nav class="sidebar" aria-label="Question index">')
    a('  <h2>Questions</h2>')
    a('  <div class="toc-list">')
    for q in qs:
        a('    <a class="toc-link" href="#%s" data-qid="%s"><span class="tn">%s</span>'
          '<span class="tt">%s</span></a>'
          % (q['anchor'], esc_attr(q['question_id']), esc(q['q_no']),
             esc(q.get('short_title', ''))))
    a('    <a class="toc-link" href="#rapid-revision"><span class="tn">&#9733;</span>'
      '<span class="tt">Rapid revision</span></a>')
    a('  </div>')
    a('</nav>')
    a('')
    a('<main id="paper-main">')
    a('<p id="ls-warning" class="rec-note" hidden>Your browser is blocking local storage, so '
      'bookmarks and studied marks will not be saved. Everything else works normally.</p>')

    a('<section aria-label="Examination instructions" class="reg-ref-box">')
    a('  <div class="rrb-title">Examination instructions, as printed</div>')
    a('  <ul>')
    for i in d['instructions']:
        a('    <li>%s</li>' % esc(i))
    a('  </ul>')
    a('  <p class="rec-note">%s</p>' % esc(d.get('marks_note', '')))
    a('</section>')
    a('')

    for q in qs:
        build_card(q, d, o, publish)
        a('')

    a('<div id="no-results">No question matches that search. Try a topic, a regulation '
      'or a question number &mdash; for example <b>general average</b>, <b>MARPOL Annex VI</b> or <b>Q5</b>.</div>')

    # ---- paper-level rapid revision -------------------------------------
    a('<section class="cheat" id="rapid-revision">')
    a('  <h2>%s rapid revision</h2>' % esc(d['month_year']))
    a('  <p class="lead">Every question in one pass. Generated from each question\'s Quick Revision '
      'block &mdash; open the full answer from the question number.</p>')
    a('  <table class="rapid">')
    a('    <thead><tr><th>Q</th><th>Topic</th><th>Answer skeleton</th>'
      '<th>Critical rule / number</th><th>Major trap</th></tr></thead>')
    a('    <tbody>')
    for q in built:
        qr = q.get('quick_revision') or {}
        skel = ' &rarr; '.join(esc(s) for s in (qr.get('skeleton') or [])[:6])
        crit = esc(qr.get('critical_regulation', ''))
        nums = (qr.get('critical_numbers') or [])
        if nums:
            crit += '<br><span class="rec-note">%s</span>' % esc(nums[0])
        a('      <tr>')
        a('        <td data-l="Question"><a href="#%s">%s</a></td>' % (q['anchor'], esc(q['q_no'])))
        a('        <td data-l="Topic">%s<br><span class="rec-note">%s marks</span></td>'
          % (esc(q.get('short_title', '')), q['total_marks']))
        a('        <td data-l="Answer skeleton">%s</td>' % skel)
        a('        <td data-l="Critical rule">%s</td>' % crit)
        a('        <td data-l="Major trap">%s</td>' % esc(qr.get('major_trap', '')))
        a('      </tr>')
    a('    </tbody>')
    a('  </table>')
    a('</section>')

    a('<div class="q-footer">')
    a('  <span class="correction-link">Correction? <a href="mailto:%s?subject=Past%%20Paper%%20%s%%2C%%20Correction%%20Required">%s</a></span>'
      % (CONTACT, pid, CONTACT))
    a('  <span class="q-version">Written Questions &middot; %s &middot; v%s &middot; %s</span>'
      % (pid, esc(d['version']), 'GATED' if gated else 'UNGATED REVIEW COPY'))
    a('</div>')
    a('</main>')
    a('</div>')
    a('')
    o.extend(footer(publish))
    a('')
    js = open(os.path.join(TPL, 'paper.js'), encoding='utf-8').read()
    js = (js.replace('__LS_BOOKMARKS__', LS_BOOKMARKS)
            .replace('__LS_PROGRESS__', LS_PROGRESS)
            .replace('__LS_MIGRATE__', LS_MIGRATE_JS)
            .replace('__STICKY_SYNC__', STICKY_SYNC_JS))
    a('<script>')
    a(js.rstrip('\n'))
    a('</script>')
    a('</body>')
    a('</html>')
    return '\n'.join(o) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('spec')
    ap.add_argument('-o', '--out')
    ap.add_argument('--gated', action='store_true')
    ap.add_argument('--publish', action='store_true')
    args = ap.parse_args()

    spec = json.load(open(args.spec, encoding='utf-8'))
    html = build(spec, gated=args.gated, publish=args.publish)

    out = args.out or os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers',
                                   '%s.html' % spec['paper_id'])
    prev = open(out, encoding='utf-8', newline='').read() if os.path.exists(out) else None
    with io.open(out, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(html)

    try:
        rel = os.path.relpath(out, REPO_ROOT).replace('\\', '/')
    except ValueError:
        # -o may point at another drive (Windows). Not an error; just report it whole.
        rel = out.replace('\\', '/')
    n = sum(1 for q in spec['questions'] if q.get('model_answer'))
    print('built %s' % rel)
    print('  %d bytes, %d questions, %d with answers'
          % (len(html.encode('utf-8')), len(spec['questions']), n))
    print('  mode: %s, gate: %s'
          % ('PUBLISH' if args.publish else 'review (noindex)',
             'PRESENT' if args.gated else 'stripped'))
    if prev is not None:
        print('  rebuild: %s' % ('IDENTICAL to previous output' if prev == html else 'CHANGED'))


if __name__ == '__main__':
    main()
