#!/usr/bin/env python3
"""Build the paid Solved QP product home at /solvedQP/index.html.

    specs/*.json  -->  solvedQP/index.html

This is a PROJECTION, not a second source of truth. Every sitting, every
question count and the "newest solved sitting" hook are derived from the
same canonical specs that produce the papers themselves. Adding a spec
adds a card here with no edit to this file.

Deliberately NOT shown to a paying candidate: recurrence_class, build
state, review state or any other authoring field. Those are production
metadata; a candidate must never be told a question is "expected".

Determinism: no clock read, no random value. Re-running with unchanged
specs is byte-identical.
"""
import argparse, glob, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import (REPO_ROOT, CONTACT, esc, strip_tags, read_css,
                           topbar, head_meta, footer, GATE_STUB, delivery_links)
import recurrence_model as RM
# KNOWN_ABSENT is owned by the year-sheet builder, which already distinguishes
# "no sitting was held" from "not yet in the MIW set". Importing it keeps ONE
# statement of which months genuinely have no examination -- a second hand-kept
# list here would drift, and a wrong "No sitting" is a factual claim about the
# examination, not a presentation detail.
from build_questions_year import KNOWN_ABSENT

SPEC_GLOB = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers', 'specs', '*.json')

# Coverage states shown on the product home.
AVAILABLE = 'AVAILABLE'
PLANNED_SOON = 'PLANNED_SOON'
NO_SITTING = 'NO_SITTING'

MODES = [
    ('Understand', 'What the examiner is actually asking, and the trap in the wording.'),
    ('Exam Plan', 'How to spend the marks — the shape of the answer before you write it.'),
    ('Answer', 'The full model written answer, regulation-referenced.'),
    ('Study Guide', 'The background you need if the topic is not yet solid.'),
    ('Recall', 'Fifteen-second revision — route, critical number, major trap.'),
]

HOME_CSS = """
  .sq-hero{background:linear-gradient(135deg,#0f172a,#1e293b);color:#e2e8f0;padding:2.5rem 0 2rem;}
  .sq-hero .wrap{max-width:1080px;margin:0 auto;padding:0 1.25rem;}
  .sq-hero h1{color:#fff;font-size:1.9rem;line-height:1.25;margin:.35rem 0 .5rem;}
  .sq-hero .sub{color:#94a3b8;font-size:.95rem;margin:0 0 1rem;max-width:62ch;line-height:1.6;}
  .sq-badge{display:inline-block;background:rgba(13,148,136,.18);color:#5eead4;border:1px solid rgba(13,148,136,.4);
            font-size:.72rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:4px 11px;border-radius:20px;}
  .sq-stats{display:flex;flex-wrap:wrap;gap:1.5rem;margin-top:1.1rem;}
  .sq-stats div{min-width:0;}
  .sq-stats b{display:block;color:#fff;font-size:1.35rem;line-height:1.1;}
  .sq-stats span{color:#94a3b8;font-size:.78rem;}
  .sq-section{max-width:1080px;margin:0 auto;padding:2rem 1.25rem 0;}
  .sq-section h2{font-size:1.15rem;margin:0 0 .35rem;}
  .sq-section .lead{color:var(--grey-text);font-size:.9rem;margin:0 0 1.1rem;max-width:70ch;line-height:1.6;}
  .sq-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem;}
  .sq-card{border:1px solid var(--grey-border);border-radius:12px;padding:1.1rem 1.15rem;background:#fff;
           display:flex;flex-direction:column;gap:.5rem;}
  .sq-card .m{font-size:.72rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--teal);}
  .sq-card h3{font-size:1.05rem;margin:0;}
  .sq-card h3 a{text-decoration:none;color:inherit;}
  .sq-card h3 a:hover{color:var(--teal);}
  .sq-card .meta{color:var(--grey-text);font-size:.8rem;line-height:1.6;margin:0;}
  .sq-card .go{margin-top:auto;font-size:.85rem;font-weight:600;color:var(--teal);text-decoration:none;}
  .sq-newest{border-color:var(--teal);box-shadow:0 0 0 1px var(--teal) inset;}
  .cov-year{font-size:1rem;margin:1.1rem 0 .6rem;color:var(--grey-text);}
  .cov-grid{grid-template-columns:repeat(auto-fill,minmax(210px,1fr));margin-bottom:.4rem;}
  .sq-card.cov{padding:.85rem .95rem;gap:.35rem;}
  .sq-card.cov h3{font-size:.95rem;}
  /* Unavailable states are visibly quieter than an available paper, so the
     difference reads at a glance rather than only on the label. */
  .cov-planned,.cov-absent{background:#f8fafc;border-style:dashed;}
  .cov-planned .m{color:var(--grey-text);}
  .cov-absent .m{color:#94a3b8;}
  .cov-absent h3{color:#94a3b8;}
  .sq-modes{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:.85rem;}
  .sq-mode{border:1px solid var(--grey-border);border-radius:10px;padding:.85rem .95rem;background:#fff;}
  .sq-mode b{display:block;font-size:.9rem;margin-bottom:.25rem;}
  .sq-mode span{color:var(--grey-text);font-size:.8rem;line-height:1.55;}
  .sq-note{max-width:1080px;margin:1.5rem auto 0;padding:0 1.25rem 2.5rem;color:var(--grey-text);font-size:.82rem;line-height:1.7;}
  @media(max-width:640px){.sq-hero h1{font-size:1.5rem;}.sq-stats{gap:1rem;}}
"""


def load_specs():
    out = []
    for p in sorted(glob.glob(SPEC_GLOB)):
        with open(p, encoding='utf-8') as fh:
            out.append(json.load(fh))
    return out


def solved_sittings(specs):
    """Specs that actually carry model answers, oldest first."""
    solved = [d for d in specs if any(q.get('model_answer') for q in d['questions'])]
    return sorted(solved, key=lambda d: (d['year'], RM.MONTH_NUM[d['month']]))


def coverage(specs):
    """Honest month-by-month coverage: (year, month_num, month, state, paper_id).

    Three states, and one deliberate silence:

      AVAILABLE     a solved paper exists -- clickable
      PLANNED_SOON  the sitting is in the MIW set and transcribed, but not yet
                    solved. Shown so a candidate can see what is coming, with
                    NO link, because there is no answer page to open.
      NO_SITTING    no examination was held that month (KNOWN_ABSENT)

    A month that is neither in the spec set nor in KNOWN_ABSENT is NOT RENDERED
    AT ALL. That is what stops the page inventing sittings: the later months of
    the current year simply do not appear until a real source paper exists for
    them. Coverage is asserted from evidence, never from the calendar.
    """
    by_key = {(d['year'], RM.MONTH_NUM[d['month']]): d for d in specs}
    years = sorted({y for y, _ in by_key} | {y for y, _ in KNOWN_ABSENT})
    rows = []
    for y in years:
        for mn in range(1, 13):
            d = by_key.get((y, mn))
            if d is not None:
                solved = any(q.get('model_answer') for q in d['questions'])
                rows.append((y, mn, RM.MONTHS[mn - 1],
                             AVAILABLE if solved else PLANNED_SOON,
                             d['paper_id']))
            elif (y, mn) in KNOWN_ABSENT:
                rows.append((y, mn, RM.MONTHS[mn - 1], NO_SITTING, None))
    return rows


def newest_sitting(specs):
    s = solved_sittings(specs)
    return s[-1] if s else None


def build(specs):
    sittings = solved_sittings(specs)
    newest = sittings[-1] if sittings else None
    total_q = sum(len(d['questions']) for d in sittings)

    title = 'MIW Solved Question Papers &mdash; MEO Class I Engineering Management'
    desc = ('Complete solved MEO Class I Engineering Management written papers, every question '
            'worked through Understand, Exam Plan, Answer, Study Guide and Recall.')

    o = []
    a = o.append
    # noindex: this is paid content. publish=False gives that.
    o.extend(head_meta(strip_tags(title), strip_tags(desc), '/solvedQP/', False))
    a('<style>')
    a(read_css())
    a(HOME_CSS)
    a('</style>')
    a('</head>')
    a('<body>')
    a(GATE_STUB)
    a('<a class="skip" href="#sq-main">Skip to papers</a>')
    # The home covers every solved year, so its navigation carries one link
    # per year rather than a single hard-coded sheet.
    home_years = sorted({d['year'] for d in sittings})
    o.extend(topbar('Solved QP', links=delivery_links(years=home_years)))

    a('<header class="sq-hero">')
    a('  <div class="wrap">')
    a('    <span class="sq-badge">Written &middot; Solved</span>')
    a('    <h1>MIW Solved Question Papers</h1>')
    a('    <p class="sub">MEO Class I &mdash; Engineering Management. Every question from every '
      'available sitting, worked end to end: what the examiner is asking, how to spend the marks, '
      'the full model answer, the background, and a fifteen-second recall.</p>')
    a('    <div class="sq-stats">')
    a('      <div><b>%d</b><span>solved sittings</span></div>' % len(sittings))
    a('      <div><b>%d</b><span>questions</span></div>' % total_q)
    a('      <div><b>5</b><span>study modes each</span></div>')
    if newest:
        a('      <div><b>%s</b><span>newest solved sitting</span></div>' % esc(newest['month_year']))
    a('    </div>')
    a('  </div>')
    a('</header>')

    a('<main id="sq-main">')

    # ---- papers ----------------------------------------------------
    a('<section class="sq-section">')
    a('  <h2>Solved papers</h2>')
    a('  <p class="lead">Each paper opens as a full interactive sitting &mdash; search across '
      'questions, bookmark, and track what you have worked through.</p>')
    a('  <div class="sq-grid">')
    for d in reversed(sittings):          # newest first for the reader
        pid = d['paper_id']
        is_newest = newest is not None and pid == newest['paper_id']
        a('    <article class="sq-card%s">' % (' sq-newest' if is_newest else ''))
        a('      <span class="m">%s</span>' % ('Newest sitting' if is_newest else esc(d['subject'])))
        a('      <h3><a href="/solvedQP/%s.html">%s</a></h3>' % (pid, esc(d['month_year'])))
        a('      <p class="meta">Sr. No. %s &middot; %d questions &middot; answer six<br>%s &middot; total marks %s</p>'
          % (esc(d['sr_no']), len(d['questions']), esc(d['time_allowed']), esc(d['total_marks'])))
        a('      <a class="go" href="/solvedQP/%s.html">Open %s &rarr;</a>'
          % (pid, esc(d['month_year'].split()[0])))
        a('    </article>')
    a('  </div>')
    a('</section>')

    # ---- coverage, stated honestly ---------------------------------
    # The product is deliberately partial during controlled testing. A candidate
    # is owed a straight answer about what exists, what is coming and what was
    # never set -- not a grid that quietly omits the difference.
    rows = coverage(specs)
    if rows:
        a('<section class="sq-section">')
        a('  <h2>Coverage by sitting</h2>')
        a('  <p class="lead">What is solved today, what is being worked on, and which months '
          'had no examination. Months with no entry below are simply not in the MIW source '
          'set yet &mdash; that is a statement about our coverage, not about whether a '
          'sitting was held.</p>')
        for y in sorted({r[0] for r in rows}, reverse=True):
            a('  <h3 class="cov-year">%d</h3>' % y)
            a('  <div class="sq-grid cov-grid">')
            for (_yr, _mn, month, state, pid) in [r for r in rows if r[0] == y]:
                if state == AVAILABLE:
                    a('    <article class="sq-card cov cov-available">')
                    a('      <span class="m">Available</span>')
                    a('      <h3><a href="/solvedQP/%s.html">%s %d</a></h3>' % (pid, esc(month), y))
                    a('      <a class="go" href="/solvedQP/%s.html">Open %s &rarr;</a>'
                      % (pid, esc(month)))
                elif state == PLANNED_SOON:
                    # No anchor at all. A disabled-looking link that does nothing
                    # reads as a broken product; absence of a control is honest.
                    a('    <article class="sq-card cov cov-planned">')
                    a('      <span class="m">Planned soon</span>')
                    a('      <h3>%s %d</h3>' % (esc(month), y))
                    a('      <p class="meta">Questions transcribed from the printed paper. '
                      'Worked answers are in preparation.</p>')
                else:
                    a('    <article class="sq-card cov cov-absent">')
                    a('      <span class="m">No sitting</span>')
                    a('      <h3>%s %d</h3>' % (esc(month), y))
                    a('      <p class="meta">No examination paper exists for this month.</p>')
                a('    </article>')
            a('  </div>')
        a('</section>')

    # ---- how each question is worked -------------------------------
    a('<section class="sq-section">')
    a('  <h2>How every question is worked</h2>')
    a('  <p class="lead">The same five modes on every question, in the same order. '
      'The route through an answer is written once and reused by the plan, the guide and the recall.</p>')
    a('  <div class="sq-modes">')
    for name, blurb in MODES:
        a('    <div class="sq-mode"><b>%s</b><span>%s</span></div>' % (esc(name), esc(blurb)))
    a('  </div>')
    a('</section>')

    # ---- questions by year ----------------------------------------
    years = sorted({d['year'] for d in sittings})
    a('<section class="sq-section">')
    a('  <h2>Questions by year</h2>')
    a('  <p class="lead">Every question set in a year, month by month, with printed marks, topic '
      'and how often the question has recurred across sittings. Questions only &mdash; use it to '
      'test yourself before opening an answer.</p>')
    a('  <div class="sq-grid">')
    for y in reversed(years):
        n = sum(len(d['questions']) for d in sittings if d['year'] == y)
        a('    <article class="sq-card">')
        a('      <span class="m">Question intelligence</span>')
        a('      <h3><a href="/solvedQP/questions-%d.html">%d &mdash; all questions</a></h3>' % (y, y))
        a('      <p class="meta">%d questions across %d sittings, with recurrence history.</p>'
          % (n, sum(1 for d in sittings if d['year'] == y)))
        a('      <a class="go" href="/solvedQP/questions-%d.html">Open the %d sheet &rarr;</a>' % (y, y))
        a('    </article>')
    a('  </div>')
    a('</section>')

    a('<p class="sq-note">Your access covers every solved paper here, including all future '
      'sittings added to this collection. Spotted something that needs correcting? '
      '<a href="mailto:%s?subject=Solved%%20QP%%20correction">%s</a>.</p>' % (CONTACT, CONTACT))
    a('</main>')
    o.extend(footer(True))
    a('</body>')
    a('</html>')
    return '\n'.join(o) + '\n'


def write(path, text):
    prev = open(path, encoding='utf-8', newline='').read() if os.path.exists(path) else None
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    return 'IDENTICAL' if prev == text else ('CHANGED' if prev is not None else 'NEW')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--out', default=None)
    args = ap.parse_args()

    specs = load_specs()
    if not specs:
        print('ERROR: no specs found under %s' % SPEC_GLOB)
        sys.exit(1)

    path = args.out or os.path.join(REPO_ROOT, 'solvedQP', 'index.html')
    st = write(path, build(specs))
    n = newest_sitting(specs)
    print('solvedQP/index.html  %s' % st)
    print('  %d solved sittings, newest %s' % (len(solved_sittings(specs)),
                                               n['month_year'] if n else 'none'))


if __name__ == '__main__':
    main()
