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
                           GATE_STUB, LS_BOOKMARKS, LS_PROGRESS, LS_MIGRATE_JS,
                           STICKY_SYNC_JS)

PP_DIR = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers')
SPEC_GLOB = os.path.join(PP_DIR, 'specs', '*.json')

# Small deterministic topic layer (brief section 27). Controlled parent
# categories over the subject_tags vocabulary -- a grouping, not a graph database.
MONTHS = ('January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December')
MONTH_ABBR = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

# Years the sitting navigator advertises, newest first. A year listed here
# renders all twelve months whether or not a paper exists for each: unbuilt
# months come from THIS configuration, never from placeholder spec files. That
# is what lets the index scale to 12 papers a year without the repository
# filling up with empty JSON.
#
# Any year that has a spec is included automatically, so this list only needs to
# name years we want to advertise BEFORE the first paper of that year is built.
SERIES_YEARS = (2026, 2025)


def paper_status(answers_built):
    """Student-facing availability. Deliberately two-valued.

    Production has richer internal state (build_state, review_state,
    official_source_verified) and the manifest keeps all of it. The student view
    does not: the only thing a student can act on is whether there is an answer
    to read. Holding a source copy of a sitting is not a product, so a month is
    'available' only when answers actually exist -- a paper can never appear
    solved because a PDF sits in a folder.
    """
    return 'available' if answers_built > 0 else 'coming_later'


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
            'month_num': MONTHS.index(d['month']) + 1,
            'paper_status': paper_status(len(built)),
            'month_year': d['month_year'], 'subject': d['subject'], 'class': d['class'],
            'function': d['function'], 'total_marks': d['total_marks'],
            'marks_note': d['marks_note'],
            'file': url, 'spec': 'meoclass1/pastpapers/specs/%s.json' % pid,
            'dedup_plan': 'meoclass1/pastpapers/verification/%s/DEDUP_AND_SOURCE_PLAN.md' % pid,
            'red_team_review': 'meoclass1/pastpapers/verification/%s/PILOT_RED_TEAM_REVIEW.md' % pid,
            # Source-copy classification is neutral by policy: it records WHAT
            # kind of copy this is, never WHO hosted it. The host's identity is
            # kept locally, outside this public repository.
            'source_copy_provenance': d['source_copy_provenance']['described_as'],
            'source_copy_type': d['source_copy_provenance']['source_copy_type'],
            'source_authority': d['source_copy_provenance']['source_authority'],
            # Deliberately distinct from source_authority. Removing a host's name
            # from a scan does not make the scan an official source, so this
            # continues to report actual verification status.
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
                'primary_category': q.get('primary_category'),
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
        'naming_convention': ("QP<YY><MM>.html, where QP = Question Paper, YY = year and "
                              "MM = month of the sitting (QP2607 = July 2026); "
                              "question_id QP<YY><MM>-Q<n>; anchors #q1..#q9"),
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
        # Navigator shape. Years carrying a spec plus any advertised ahead of
        # their first paper. Consumers can render the full grid from this
        # without a placeholder spec existing for every month.
        'series_years': sorted(set(SERIES_YEARS) | {p['year'] for p in papers}, reverse=True),
        'months': list(MONTHS),
        'paper_status_model': {
            'available': 'Answers are published for this sitting.',
            'coming_later': ('No answers yet. Covers every case a student cannot act on -- '
                             'not transcribed, in production, or source copy held only. '
                             'Holding a source copy never reads as solved.'),
        },
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

    # Search is the only thing in the sticky bar. The previous build also put a
    # filter button per year and per subject tag here: seventeen buttons with a
    # single paper, and a bar 303px tall on a phone, which pushed the search
    # input itself off screen. Year selection now lives in the sitting grid and
    # subject selection on the topics page, so this bar stays one row.
    a('  <div class="controls-bar"><div class="controls-inner">')
    a('    <label class="search-wrap"><span aria-hidden="true">&#128269;</span>')
    a('      <input id="q-search" type="search" autocomplete="off" '
      'placeholder="Search every question &mdash; e.g. general average, SOPEP, ammonia, MARPOL Annex VI" '
      'aria-label="Search all written questions">')
    a('      <button id="q-clear" class="icon-btn" type="button" aria-label="Clear search">&times;</button>')
    a('    </label>')
    a('    <span class="count-label" id="idx-count" role="status" aria-live="polite"></span>')
    a('  </div></div>')

    a('<main id="idx-main">')

    # ---- A. "I know the sitting" -----------------------------------------
    # One compact block per year, twelve months each, whatever exists. This
    # replaced a full article per paper: at 24 papers that was 24 large cards
    # to scroll, which is a list, not a navigator.
    by_ym = {(p['year'], p['month_num']): p for p in man['papers']}
    a('<section class="nav-block" aria-labelledby="h-sittings">')
    a('  <h2 id="h-sittings" class="sec-h">Browse by sitting</h2>')
    for year in man['series_years']:
        got = sum(1 for (y, _), p in by_ym.items()
                  if y == year and p['paper_status'] == 'available')
        a('  <article class="year-block">')
        a('    <div class="year-head"><h3>%d</h3>'
          '<span class="year-count">%s</span></div>'
          % (year, 'no papers yet' if not got else
             '%d of 12 available' % got))
        a('    <ol class="month-grid">')
        for i, abbr in enumerate(MONTH_ABBR, start=1):
            p = by_ym.get((year, i))
            avail = bool(p) and p['paper_status'] == 'available'
            if avail:
                a('      <li class="m avail"><a href="%s.html" '
                  'aria-label="%s %d &mdash; %d questions with model answers">'
                  '<span class="m-ab">%s</span>'
                  '<span class="m-st">%d Qs</span></a></li>'
                  % (esc_attr(p['paper_id']), MONTHS[i - 1], year,
                     p['answers_built'], abbr, p['answers_built']))
            else:
                # Not a link and not focusable: there is nothing to open. The
                # state is announced in text, never by colour alone.
                a('      <li class="m soon"><span aria-label="%s %d &mdash; coming later">'
                  '<span class="m-ab">%s</span>'
                  '<span class="m-st">&mdash;</span></span></li>'
                  % (MONTHS[i - 1], year, abbr))
        a('    </ol>')
        a('  </article>')
    a('  <p class="rec-note">Months marked &mdash; are not yet available. A sitting appears '
      'here only once its answers are written; holding a copy of a paper is not the same '
      'as having solved it.</p>')
    a('</section>')

    # ---- B. "I know the topic" -------------------------------------------
    a('<section class="nav-block" aria-labelledby="h-topics">')
    a('  <h2 id="h-topics" class="sec-h">Browse by topic</h2>')
    a('  <p class="rec-note" style="margin-top:0;">Where each topic has appeared, with its '
      'recurrence history.</p>')
    a('  <p class="btn-row">')
    for year in sorted({p['year'] for p in man['papers']}, reverse=True):
        a('    <a class="nav-btn" href="topics-%d.html">%d topic coverage</a>' % (year, year))
    a('  </p>')
    a('</section>')

    # ---- C. "I want to carry on studying" --------------------------------
    a('<section class="nav-block" aria-labelledby="h-study">')
    a('  <h2 id="h-study" class="sec-h">My study</h2>')
    a('  <p class="rec-note" style="margin-top:0;">Saved on this device only. '
      'No account, nothing sent anywhere.</p>')
    a('  <p class="btn-row">')
    a('    <button class="filter-btn" type="button" data-f="all" aria-pressed="true">All questions</button>')
    a('    <button class="filter-btn" type="button" data-f="bookmarked" aria-pressed="false">&#9733; Bookmarked</button>')
    a('    <button class="filter-btn" type="button" data-f="studied" aria-pressed="false">&#10003; Studied</button>')
    a('    <button class="filter-btn" type="button" data-f="unstudied" aria-pressed="false">Not studied</button>')
    a('  </p>')
    a('</section>')

    a('<section class="nav-block" aria-labelledby="results-head">')
    a('  <h2 id="results-head" class="sec-h">Questions</h2>')
    a('  <p class="rec-note" id="idx-hint" style="margin-top:0;">Search above, or pick a study '
      'filter, to look inside every question across every paper. You do not need to know which '
      'paper it came from. Results link straight to the answer.</p>')
    a('  <div id="idx-results"></div>')
    a('  <div id="idx-empty" style="display:none;" class="rec-note">No question matches that search.</div>')
    a('</section>')

    if not publish:
        a('<section class="nav-block"><h2 class="sec-h">Production state</h2>')
        a('  <table class="prod-table"><thead><tr><th>Paper</th><th>Build</th>'
          '<th>Review</th><th>Official source verified</th></tr></thead><tbody>')
        for p in man['papers']:
            a('    <tr><td>%s &middot; %s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
              % (esc(p['paper_id']), esc(p['month_year']), esc(p['build_state']),
                 esc(p['review_state']),
                 'yes' if p['official_source_verified'] else 'NO'))
        a('  </tbody></table>')
        a('</section>')

    a('</main>')
    o.extend(footer(publish))
    a('<script>')
    a('var ROWS=%s;' % _index_js(man))
    a(open(os.path.join(HERE, 'template', 'index.js'), encoding='utf-8').read().rstrip('\n')
      .replace('__LS_BOOKMARKS__', LS_BOOKMARKS)
      .replace('__LS_PROGRESS__', LS_PROGRESS)
      .replace('__LS_MIGRATE__', LS_MIGRATE_JS)
      .replace('__STICKY_SYNC__', STICKY_SYNC_JS))
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

    # ONE primary category per question, plus secondary tags.
    #
    # Previously a question rendered under every category whose subject_tags it
    # touched: 9 questions became 13 cards, and the placements misled -- an iron
    # ore FSA question sat under "Statutory Framework & Class" purely because it
    # carried a SOLAS tag. At 12 papers a year that is a few hundred duplicate
    # cards and a topic page nobody can navigate. The primary category says where
    # a question's SUBSTANCE sits; subject_tags stay searchable and filterable.
    used = set()
    for cat, subs in TOPIC_TREE:
        group = [q for q in qs if q.get('primary_category') == cat]
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
            # Secondary tags: the subject tags this question carries other than
            # the one naming its primary category, plus its topic tags. They are
            # shown so the cross-cutting relevance is visible, and they remain
            # searchable -- but they no longer duplicate the card.
            secondary = [t for t in q['subject_tags'] if t not in subs]
            a('    <div class="pc-topics" style="margin-top:6px;">%s%s</div>'
              % (''.join('<span class="q-tag">%s</span>' % esc(t) for t in secondary),
                 ''.join('<span class="q-tag sub">%s</span>' % esc(t)
                         for t in q['topic_tags'][:4])))
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
