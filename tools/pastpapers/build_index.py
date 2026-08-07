#!/usr/bin/env python3
"""Generate the Past Papers manifest and both index pages from the specs.

Usage:
  python build_index.py [--publish]

Reads every meoclass1/pastpapers/specs/*.json and writes:
  meoclass1/pastpapers/pastpapers_content_index.json   retrieval index (NOT content)
  meoclass1/pastpapers/index.html                      Written Questions & Answers hub
  meoclass1/pastpapers/topics-2026.html                yearly topic/question coverage

The two pages answer different questions:
  index.html      "which paper do I want?" -- and, via question-level search,
                  "which paper contains this subject?" without knowing in advance
  topics-2026.html "where has this topic appeared this year?"

Both are GENERATED. Never hand-edit them; edit the spec and re-run.

The manifest indexes questions; it never copies answer text. Answers live in the
paper spec, which stays the single source of truth.
"""
import argparse, glob, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'tools', 'notes'))
from render_common import (REPO_ROOT, BASE, CONTACT, esc, esc_attr, strip_tags,
                           read_css, search_tokens, topbar, head_meta, footer,
                           GATE_STUB)

PP_DIR = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers')
SPEC_GLOB = os.path.join(PP_DIR, 'specs', '*.json')

# Small deterministic topic layer (brief section 27). Controlled parent
# categories over the subject_tags vocabulary -- a grouping, not a graph database.
TOPIC_TREE = [
    ('Pollution Prevention & Response', ['MARPOL', 'Pollution Prevention', 'Casualty & Investigation']),
    ('Cargo & Bulk Carriage', ['IMSBC']),
    ('Statutory Framework & Class', ['SOLAS', 'Classification']),
    ('Alternative Fuels & Decarbonisation', ['Alternative Fuels']),
    ('Marine Insurance & Commercial Law', ['Marine Insurance', 'Commercial Law']),
    ('Human Element & Management', ['Human Element', 'STCW', 'ISM']),
    ('Indian Maritime Legislation', ['Indian Legislation']),
]


def load_specs():
    specs = []
    for p in sorted(glob.glob(SPEC_GLOB)):
        specs.append(json.load(open(p, encoding='utf-8')))
    return specs


# ------------------------------------------------------------------ manifest

def build_manifest(specs):
    papers, questions = [], []
    for d in specs:
        pid = d['paper_id']
        url = 'meoclass1/pastpapers/%s.html' % pid
        built = [q for q in d['questions'] if q.get('model_answer')]
        papers.append({
            'paper_id': pid, 'sr_no': d['sr_no'], 'year': d['year'], 'month': d['month'],
            'month_year': d['month_year'], 'subject': d['subject'], 'class': d['class'],
            'function': d['function'], 'total_marks': d['total_marks'],
            'marks_note': d['marks_note'],
            'file': url, 'spec': 'meoclass1/pastpapers/specs/%s.json' % pid,
            'dedup_plan': 'meoclass1/pastpapers/verification/%s/DEDUP_AND_SOURCE_PLAN.md' % pid,
            'red_team_review': 'meoclass1/pastpapers/verification/%s/PILOT_RED_TEAM_REVIEW.md' % pid,
            'source_copy_provenance': '%s (host branding: %s)' % (
                d['source_copy_provenance']['described_as'],
                d['source_copy_provenance']['host_branding']),
            'official_source_verified': d['official_source_verified'],
            'transcription_verified': d['transcription_verified']['state'],
            'build_state': d['build_state'], 'review_state': d['review_state'],
            'gated': d['gated'], 'version': d['version'],
            'created': d['created'], 'updated': d['updated'],
            'question_count': len(d['questions']), 'answers_built': len(built),
            'subject_tags': sorted({t for q in d['questions'] for t in (q.get('subject_tags') or [])}),
        })
        for q in d['questions']:
            questions.append({
                'paper_id': pid, 'question_id': q['question_id'],
                'year': d['year'], 'month': d['month'], 'month_year': d['month_year'],
                'question_number': q['q_no'], 'marks': q['total_marks'],
                'question_text': strip_tags(q['text_verbatim']),
                'short_title': q.get('short_title', ''),
                'subject_tags': q.get('subject_tags') or [],
                'topic_tags': q.get('topic_tags') or [],
                'intent_tags': q.get('intent_tags') or [],
                'search_aliases': q.get('search_aliases') or [],
                'regulations': q.get('regulations') or [],
                'recurrence': q.get('recurrence') or [],
                'recurrence_class': q.get('recurrence_class', 'new'),
                'prior_sittings': q.get('prior_sittings', 0),
                'reuse_tier': q.get('reuse_tier'),
                'answer_status': q['answer_status'],
                'verification_status': q.get('verification_status'),
                'verification_file': q.get('verification_file'),
                'url': url, 'anchor': q['anchor'],
                'deep_link': '%s#%s' % (url, q['anchor']),
                'study_guide_available': bool(q.get('study_notes')),
                'cheat_sheet_available': bool(q.get('quick_revision')),
                'last_verified': d['updated'],
                'unresolved_count': len(q.get('unresolved') or []),
                'reverify_before_publication': q.get('reverify_before_publication') or [],
                'provenance_summary': q.get('provenance_summary'),
                'search_blob': search_tokens(q, d),
            })
    return {
        'manifest_version': '2.0',
        'generated_from': 'meoclass1/pastpapers/specs/*.json by tools/pastpapers/build_index.py',
        'generated': max(d['updated'] for d in specs) if specs else '',
        'scope': ('Past Written Papers (PP) series retrieval index. One entry per paper and one per '
                  'question. This file is an INDEX, not a content source: answer text lives only in '
                  'the paper spec. Regenerate with build_index.py; never hand-edit.'),
        'naming_convention': "EM<YYMM>.html; question_id EM<YYMM>-Q<n>; anchors #q1..#q9",
        'source_of_truth_policy': ('specs/<PAPER>.json is authoritative for content. This manifest is '
                                   'authoritative for retrieval. Both index pages and the paper page '
                                   'are generated; editing generated HTML is always wrong.'),
        'recurrence_classes': {
            'new': 'No prior sitting recorded on the source paper.',
            'topic_recurrence': 'Prior sittings recorded for the same topic; wording NOT compared.',
            'near_recurrence': 'Wording compared and substantially similar, with a recorded delta.',
            'exact_recurrence': 'Wording compared and materially identical.'},
        'recurrence_rule': ('A third-party recurrence table alone only supports topic_recurrence. '
                            'near_ and exact_ require the prior paper wording to have been compared.'),
        'topic_tree': [{'category': c, 'subject_tags': t} for c, t in TOPIC_TREE],
        'total_papers': len(papers), 'total_questions': len(questions),
        'total_reverify_before_publication': sum(len(q['reverify_before_publication']) for q in questions),
        'papers': papers, 'questions': questions,
    }


# ------------------------------------------------------------------ pages

def _index_js(man):
    rows = [{'qid': q['question_id'], 'p': q['paper_id'], 'n': q['question_number'],
             'my': q['month_year'], 'y': q['year'], 'm': q['month'], 't': q['short_title'],
             'mk': q['marks'], 'st': q['question_text'][:180],
             'u': '%s#%s' % (os.path.basename(q['url']), q['anchor']),
             'sub': q['subject_tags'], 'built': q['answer_status'] != 'Not Built',
             's': q['search_blob']} for q in man['questions']]
    return json.dumps(rows, ensure_ascii=False, separators=(',', ':'))


def build_index_page(man, publish):
    o = []
    a = o.append
    title = 'MEO Class I &mdash; Written Questions & Answers | Marine Intelligence Weekly'
    desc = ('Past written examination papers for MEO Class I, with model answers, study guides and '
            'quick revision. Search every question by topic, regulation, year or paper.')
    o.extend(head_meta(strip_tags(title), strip_tags(desc), '/meoclass1/pastpapers/', publish))
    a('<style>')
    a(read_css())
    a('</style>')
    a('</head>')
    a('<body>')
    a(GATE_STUB)
    a('<a class="skip" href="#idx-main">Skip to content</a>')
    o.extend(topbar('Written Questions'))
    a('<header class="page-header"><div class="wrap">')
    a('  <span class="badge">MEO Class I</span>')
    a('  <h1>Written Questions &amp; Answers</h1>')
    a('  <p class="sub">Complete past written papers with model answers, study guides and rapid '
      'revision. Search any question by topic, regulation or wording &mdash; you do not need to know '
      'which paper it came from.</p>')
    a('  <div class="header-meta"><span>%d paper%s</span><span>%d questions</span>'
      '<span>%d with model answers</span></div>'
      % (man['total_papers'], '' if man['total_papers'] == 1 else 's',
         man['total_questions'], sum(p['answers_built'] for p in man['papers'])))
    a('</div></header>')

    if not publish:
        a('<div class="review-banner"><strong>Founder review copy.</strong> Generated by '
          '<code>tools/pastpapers/build_index.py</code> from the paper specs. Not published, '
          'not indexed.</div>')

    a('<div class="controls-bar"><div class="controls-inner">')
    a('  <label class="search-wrap"><span aria-hidden="true">&#128269;</span>')
    a('    <input id="q-search" type="search" autocomplete="off" '
      'placeholder="Search every question &mdash; e.g. general average, SOPEP, ammonia, MARPOL Annex VI" '
      'aria-label="Search all written questions">')
    a('    <button id="q-clear" class="icon-btn" type="button" aria-label="Clear search">&times;</button>')
    a('  </label>')
    a('  <button class="filter-btn" type="button" data-f="all" aria-pressed="true">All</button>')
    a('  <button class="filter-btn" type="button" data-f="bookmarked" aria-pressed="false">My bookmarks</button>')
    a('  <button class="filter-btn" type="button" data-f="unstudied" aria-pressed="false">Not studied</button>')
    for y in sorted({p['year'] for p in man['papers']}):
        a('  <button class="filter-btn" type="button" data-f="y:%d" aria-pressed="false">%d</button>' % (y, y))
    for s in sorted({s for p in man['papers'] for s in p['subject_tags']}):
        a('  <button class="filter-btn" type="button" data-f="s:%s" aria-pressed="false">%s</button>'
          % (esc_attr(s.lower()), esc(s)))
    a('  <span class="count-label" id="idx-count" role="status" aria-live="polite"></span>')
    a('</div></div>')

    a('<main id="idx-main" style="max-width:1000px;margin:0 auto;padding:20px;">')
    a('<h2 style="font-size:15px;color:var(--teal-dark);text-transform:uppercase;letter-spacing:.05em;">Papers</h2>')
    for p in man['papers']:
        a('<article class="paper-card" data-paper="%s" data-year="%d" data-subjects="%s">'
          % (esc_attr(p['paper_id']), p['year'], esc_attr(' '.join(p['subject_tags']).lower())))
        a('  <h3><a href="%s" style="color:inherit;text-decoration:none;">%s &mdash; %s</a></h3>'
          % (esc_attr('%s.html' % p['paper_id']), esc(p['month_year']), esc(p['subject'])))
        a('  <div class="pc-meta">%s &middot; %s &middot; %s &middot; <b>%d of %d questions '
          'with model answers</b></div>'
          % (esc(p['sr_no']), esc(p['class']), esc(p['function']),
             p['answers_built'], p['question_count']))
        a('  <div class="pc-topics">%s</div>'
          % ''.join('<span class="q-tag">%s</span>' % esc(t) for t in p['subject_tags']))
        a('  <p style="margin:12px 0 0;"><a class="nav-btn" href="%s.html">Open paper</a>'
          ' <a class="nav-btn" href="%s.html#rapid-revision" '
          'style="background:var(--navy);">Rapid revision</a></p>'
          % (esc_attr(p['paper_id']), esc_attr(p['paper_id'])))
        if not publish:
            a('  <p class="rec-note">Build state: %s &middot; review state: %s &middot; '
              'official source verified: %s</p>'
              % (esc(p['build_state']), esc(p['review_state']),
                 'yes' if p['official_source_verified'] else 'NO'))
        a('</article>')

    a('<h2 id="results-head" style="font-size:15px;color:var(--teal-dark);text-transform:uppercase;'
      'letter-spacing:.05em;margin-top:28px;">Questions</h2>')
    a('<p class="rec-note" id="idx-hint">Type above to search every question across every paper. '
      'Results link straight to the answer.</p>')
    a('<div id="idx-results"></div>')
    a('<div id="idx-empty" style="display:none;" class="rec-note">No question matches that search.</div>')
    a('</main>')
    o.extend(footer(publish))
    a('<script>')
    a('var ROWS=%s;' % _index_js(man))
    a(open(os.path.join(HERE, 'template', 'index.js'), encoding='utf-8').read().rstrip('\n')
      .replace('__LS_BOOKMARKS__', 'miw:pastpapers:v1:bookmarks')
      .replace('__LS_PROGRESS__', 'miw:pastpapers:v1:progress'))
    a('</script>')
    a('</body>')
    a('</html>')
    return '\n'.join(o) + '\n'


def build_topics_page(man, year, publish):
    qs = [q for q in man['questions'] if q['year'] == year]
    o = []
    a = o.append
    title = 'MEO Class I Written Questions &mdash; %d topic coverage | Marine Intelligence Weekly' % year
    desc = ('Every MEO Class I written examination question recorded for %d, grouped by topic, with '
            'recurrence history and direct links to the model answers.' % year)
    o.extend(head_meta(strip_tags(title), strip_tags(desc),
                       '/meoclass1/pastpapers/topics-%d.html' % year, publish))
    a('<style>')
    a(read_css())
    a('</style>')
    a('</head>')
    a('<body>')
    a(GATE_STUB)
    a('<a class="skip" href="#t-main">Skip to content</a>')
    o.extend(topbar('2026 Topics'))
    a('<header class="page-header"><div class="wrap">')
    a('  <span class="badge">MEO Class I &middot; Written Questions</span>')
    a('  <h1>%d &mdash; topic and question coverage</h1>' % year)
    a('  <p class="sub">Where each topic has appeared in %d, with the recurrence history recorded on '
      'each source paper. Answers the question &ldquo;where has this come up?&rdquo; rather than '
      '&ldquo;which paper do I want?&rdquo;</p>' % year)
    a('  <div class="header-meta"><span>%d questions</span><span>%d paper%s</span></div>'
      % (len(qs), len({q['paper_id'] for q in qs}),
         '' if len({q['paper_id'] for q in qs}) == 1 else 's'))
    a('</div></header>')
    if not publish:
        a('<div class="review-banner"><strong>Founder review copy.</strong> Generated by '
          '<code>tools/pastpapers/build_index.py</code>. Updates automatically as papers are built.</div>')
    a('<main id="t-main" style="max-width:1000px;margin:0 auto;padding:20px;">')

    used = set()
    for cat, subs in TOPIC_TREE:
        group = [q for q in qs if set(q['subject_tags']) & set(subs)]
        if not group:
            continue
        a('<section class="topic-group">')
        a('  <h3>%s</h3>' % esc(cat))
        a('  <div class="tg-sub">%s</div>' % esc(' &middot; '.join(subs)))
        for q in sorted(group, key=lambda x: (x['paper_id'], x['question_number'])):
            used.add(q['question_id'])
            a('  <div class="hit">')
            a('    <div class="hit-top">%s <span class="sep">&middot;</span> %s '
              '<span class="sep">&middot;</span> %s marks</div>'
              % (esc(q['month_year']), esc(q['question_number']), q['marks']))
            a('    <div class="hit-title"><a href="%s">%s</a></div>'
              % (esc_attr('%s.html#%s' % (q['paper_id'], q['anchor'])), esc(q['short_title'])))
            a('    <div class="hit-stem">%s</div>' % esc(q['question_text'][:230] + '&hellip;'))
            a('    <div class="pc-topics" style="margin-top:6px;">%s</div>'
              % ''.join('<span class="q-tag sub">%s</span>' % esc(t) for t in q['topic_tags'][:5]))
            prior = [r for r in q['recurrence'] if not r.startswith('%d/' % year)]
            if prior:
                a('    <div class="rec-note">Other recorded sittings: %s. '
                  '<i>Topic recurrence only &mdash; wording not compared.</i></div>'
                  % ', '.join(esc(r) for r in prior))
            else:
                a('    <div class="rec-note">No prior sitting recorded.</div>')
            a('  </div>')
        a('</section>')

    leftover = [q for q in qs if q['question_id'] not in used]
    if leftover:
        a('<section class="topic-group"><h3>Uncategorised</h3>')
        a('  <div class="tg-sub">Subject tags not yet mapped in the topic tree &mdash; '
          'extend TOPIC_TREE in build_index.py</div>')
        for q in leftover:
            a('  <div class="hit"><div class="hit-title"><a href="%s.html#%s">%s %s</a></div></div>'
              % (esc_attr(q['paper_id']), esc_attr(q['anchor']), esc(q['question_number']),
                 esc(q['short_title'])))
        a('</section>')

    a('</main>')
    o.extend(footer(publish))
    a('</body>')
    a('</html>')
    return '\n'.join(o) + '\n'


def write(path, text):
    prev = open(path, encoding='utf-8', newline='').read() if os.path.exists(path) else None
    with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    return 'IDENTICAL' if prev == text else ('CHANGED' if prev is not None else 'NEW')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--publish', action='store_true')
    args = ap.parse_args()

    specs = load_specs()
    if not specs:
        print('ERROR: no specs found under %s' % SPEC_GLOB)
        sys.exit(1)

    man = build_manifest(specs)
    mpath = os.path.join(PP_DIR, 'pastpapers_content_index.json')
    s1 = write(mpath, json.dumps(man, indent=2, ensure_ascii=False) + '\n')
    print('manifest        %-9s %d paper(s), %d question(s), %d re-verify flag(s)'
          % (s1, man['total_papers'], man['total_questions'],
             man['total_reverify_before_publication']))

    s2 = write(os.path.join(PP_DIR, 'index.html'), build_index_page(man, args.publish))
    print('index.html      %s' % s2)

    for year in sorted({p['year'] for p in man['papers']}):
        s3 = write(os.path.join(PP_DIR, 'topics-%d.html' % year),
                   build_topics_page(man, year, args.publish))
        print('topics-%d.html %s' % (year, s3))


if __name__ == '__main__':
    main()
