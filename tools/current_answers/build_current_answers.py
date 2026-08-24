#!/usr/bin/env python3
"""Build the current-answer registry and the gated candidate pages.

    python tools/current_answers/build_current_answers.py
    python tools/current_answers/build_current_answers.py --check   # stale?

TWO OUTPUTS, ONE SOURCE
-----------------------
    meoclass1/current-answers/specs/CA-EM-*.json      hand-authored, canonical
        |
        +--> meoclass1/current-answers/registry.json  the small internal index
        +--> solvedQP/current/CA-EM-*.html            the gated candidate page

RENDERER REUSE, AND WHERE IT STOPS
----------------------------------
Section 38: do not fork the Written renderer. This module imports
`render_common` for the head, CSS, topbar, gate stub and footer, and
`build_paper.render_blocks` / `quick_revision` for the answer body -- so a
current answer and a solved answer are literally the same markup produced by
the same code, and the CSS cannot drift between them.

What is NOT reused is `build_paper.build_card`, and that is deliberate rather
than lazy. `build_card` prints `q_no`, printed marks, the paper's month_year
and a Layer-1 recurrence badge computed from the CALENDAR of solved specs. A
current answer has none of those things, and manufacturing them is precisely
the failure this whole layer exists to prevent (sections 21 and 22). The mode
selector goes with it: it is driven by `paper.js`, which is loaded per paper and
keyed on a paper id. Every section here renders open instead, which is the same
no-JS fallback the solved pages already guarantee.
"""

import argparse
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, 'tools', 'pastpapers'))
sys.path.insert(0, os.path.join(REPO, 'tools', 'study'))

import ca_model as M                                            # noqa: E402
from render_common import (head_meta, read_css, topbar, footer, GATE_STUB,     # noqa: E402
                           esc, esc_attr, strip_tags, delivery_links)
from build_paper import render_blocks, quick_revision            # noqa: E402
import qi_projection as QIP                                      # noqa: E402

CA_CSS = """
  .ca-hero{background:#0d1b2a;color:#e8eef5;padding:26px 20px}
  .ca-hero .wrap{max-width:1000px;margin:0 auto}
  .ca-kind{display:inline-block;font-size:.72rem;letter-spacing:.09em;
           text-transform:uppercase;background:#1b6ca8;color:#fff;
           padding:4px 10px;border-radius:3px;font-weight:700}
  .ca-hero h1{margin:12px 0 6px;font-size:1.5rem;line-height:1.28}
  .ca-stem{background:#12263a;border-left:4px solid #1b6ca8;padding:12px 14px;
           margin:14px 0 0;font-size:1rem;line-height:1.55}
  .ca-meta{margin-top:12px;font-size:.85rem;opacity:.88}
  .ca-meta span{margin-right:14px}
  .ca-note{max-width:1000px;margin:16px auto 0;padding:0 20px}
  .ca-note .box{border:1px solid #d7dee6;background:#f7f9fb;border-radius:4px;
                padding:12px 14px;font-size:.9rem;line-height:1.55}
  .ca-sec{max-width:1000px;margin:22px auto;padding:0 20px}
  .ca-sec>.layer{border:1px solid #d7dee6;border-radius:4px;padding:16px 18px;
                 background:#fff}
  .ca-sec .layer-title{font-weight:700;font-size:.78rem;letter-spacing:.08em;
                       text-transform:uppercase;color:#1b6ca8;margin-bottom:10px}
  .ca-auth li{margin-bottom:8px;line-height:1.5}
  .ca-cls{display:inline-block;font-size:.7rem;letter-spacing:.05em;
          background:#eef3f8;color:#264a63;border-radius:3px;padding:2px 7px;
          margin-right:6px}
  .ca-ver{font-size:.85rem;color:#4a5a68}
  .ca-ver table{border-collapse:collapse;width:100%;margin-top:8px}
  .ca-ver th,.ca-ver td{border:1px solid #dde4ea;padding:6px 9px;
                        text-align:left;vertical-align:top}
"""


# --------------------------------------------------------------------------
# REGISTRY
# --------------------------------------------------------------------------

def build_registry(entries):
    """The small internal index section 41 asks for, and nothing more.

    Deliberately NOT a candidate browse surface. Every route into this library
    today comes from somewhere that already knows which concept it wants -- a
    Phase-2 family, an archive question, a topic page -- so a browse index would
    be a second navigation model to keep in step for no candidate gain. It is
    derived, so building one later costs nothing.
    """
    rows = []
    for caid in sorted(entries):
        e = entries[caid]
        rows.append({
            'current_answer_id': caid,
            'title': e.get('title'),
            'scope': e.get('scope'),
            'limb_label': (e.get('limb_of') or {}).get('limb_label'),
            'family_ids': e.get('family_ids') or [],
            'topic_id': e.get('topic_id'),
            'review_status': e.get('review_status'),
            'answer_version': e.get('answer_version'),
            'authority_review_date': e.get('authority_review_date'),
            'currentness_as_of': e.get('currentness_as_of'),
            'next_review_trigger': e.get('next_review_trigger'),
            'candidate_visibility': e.get('candidate_visibility'),
            'url': M.page_url(caid),
            'renderable': e.get('review_status') in M.RENDERABLE,
        })
    by_family = {}
    for r in rows:
        for fid in r['family_ids']:
            by_family.setdefault(fid, []).append(r['current_answer_id'])
    return {
        'schema': M.REGISTRY_SCHEMA,
        'schema_version': '1.0',
        'generated_by': 'tools/current_answers/build_current_answers.py',
        'hand_editable': False,
        'what_this_is': (
            'The index of MIW present-day canonical answers. These are NOT '
            'past-paper questions: no entry here has a sitting, a printed '
            'serial or printed marks, and no entry here is evidence that any '
            'examiner ever set this wording.'),
        'counts': {
            'entries': len(rows),
            'verified': sum(1 for r in rows if r['renderable']),
            'whole_question': sum(1 for r in rows if r['scope'] == 'WHOLE_QUESTION'),
            'limb': sum(1 for r in rows if r['scope'] == 'LIMB'),
            'families_reached': len(by_family),
        },
        'by_family': {k: sorted(v) for k, v in sorted(by_family.items())},
        'entries': rows,
    }


# --------------------------------------------------------------------------
# PAGE
# --------------------------------------------------------------------------

def _authority_block(e, a):
    a('<section class="ca-sec"><div class="layer ca-auth">')
    a('  <div class="layer-title">Authority this answer rests on</div>')
    a('  <ul>')
    for s in e.get('authority_sources') or []:
        a('    <li><span class="ca-cls">%s</span>%s'
          % (esc(s.get('class', '')), esc(s.get('source', ''))))
        if s.get('checked'):
            a('      <div class="ca-ver">%s</div>' % esc(s['checked']))
        a('    </li>')
    a('  </ul>')
    a('  <p class="ca-ver"><b>Authority read and dated %s.</b> This answer states '
      'the position as at %s. It is not anchored to any examination sitting.</p>'
      % (esc(e.get('authority_review_date', '')), esc(e.get('currentness_as_of', ''))))
    nyf = e.get('not_yet_in_force') or []
    if nyf:
        # ADOPTED IS NOT IN FORCE. The same rule R-P2-FUTURE-DECLARED enforces
        # in the Phase-2 store, rendered where a candidate can act on it.
        a('  <div class="layer-title" style="margin-top:14px">Adopted but NOT yet '
          'in force &mdash; do not write these as current law</div>')
        a('  <ul>')
        for x in nyf:
            a('    <li>%s</li>' % esc(x))
        a('  </ul>')
    sup = e.get('superseded_framework') or []
    if sup:
        a('  <div class="layer-title" style="margin-top:14px">Superseded &mdash; '
          'do not cite</div>')
        a('  <ul>')
        for x in sup:
            a('    <li>%s</li>' % esc(x))
        a('  </ul>')
    a('</div></section>')


def _version_block(e, a):
    a('<section class="ca-sec"><div class="layer ca-ver">')
    a('  <div class="layer-title">Version and review record</div>')
    a('  <p>Version <b>%s</b>. A current answer is not frozen the way a past-paper '
      'answer is: a past-paper answer must stay true to its sitting, and this one '
      'must stay true to today. It is re-reviewed when its authority moves.</p>'
      % esc(e.get('answer_version', '')))
    if e.get('next_review_trigger'):
        a('  <p><b>Next review is triggered by:</b> %s</p>'
          % esc(e['next_review_trigger']))
    rr = e.get('review_record') or {}
    if rr:
        a('  <p><b>Independent review:</b> %s &mdash; %s</p>'
          % (esc(rr.get('verdict', '')), esc(rr.get('reviewer', ''))))
    a('  <table><tr><th>Version</th><th>Date</th><th>Reason</th>'
      '<th>Authority that moved</th></tr>')
    for v in e.get('version_history') or []:
        a('    <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
          % (esc(v.get('version', '')), esc(v.get('date', '')),
             esc(v.get('reason', '')), esc(v.get('authority', '') or '&mdash;')))
    a('  </table>')
    a('</div></section>')


def build_page(e, entries):
    caid = e['current_answer_id']
    title = '%s | Current framework answer | Marine Intelligence Weekly' % e['title']
    desc = ('MIW present-day canonical answer: %s. Current framework as at %s. '
            'Not a past-paper question.' % (e['title'], e.get('currentness_as_of', '')))

    o = []
    a = o.append
    # publish=False -> noindex, the same head every delivered /solvedQP/ page
    # carries. Paid content is never indexable.
    o.extend(head_meta(strip_tags(title), strip_tags(desc), M.page_url(caid), False))
    a('<style>')
    a(read_css())
    a(CA_CSS)
    a('</style>')
    a('</head>')
    a('<body data-current-answer="%s">' % esc_attr(caid))
    a(GATE_STUB)
    a('<a class="skip" href="#ca-main">Skip to content</a>')
    o.extend(topbar('Solved QP', links=delivery_links()))

    # ---------------------------------------------------------------- hero
    # Section 21: the page says what it is in its own first line. No exam
    # month, no sitting, no printed marks -- because there are none.
    a('<header class="ca-hero"><div class="wrap">')
    a('  <span class="ca-kind">Current framework answer</span>')
    a('  <h1>%s</h1>' % esc(e['title']))
    if e.get('scope') == 'LIMB':
        lo = e.get('limb_of') or {}
        a('  <div class="ca-meta"><span>One limb of a recurring multi-part '
          'question &mdash; %s</span></div>' % esc(lo.get('limb_label', '')))
    a('  <div class="ca-stem">%s</div>' % esc(e['canonical_question']))
    depth = e.get('recommended_exam_depth') or {}
    bits = ['Current framework as at %s' % e.get('currentness_as_of', '')]
    if depth.get('marks_band'):
        # Section 22. "Prepare to this depth" is a recommendation MIW makes.
        # "This was a 16-mark question" is a claim about a printed paper and
        # would be false, so the wording carries the distinction, not a number
        # standing on its own.
        bits.append('Prepare to roughly %s-mark depth (MIW recommendation, '
                    'not a printed mark)' % depth['marks_band'])
    a('  <div class="ca-meta">%s</div>'
      % ''.join('<span>%s</span>' % esc(b) for b in bits))
    a('</div></header>')

    # -------------------------------------------------------- what this is
    a('<div class="ca-note"><div class="box">')
    a('  <b>This is not a past-paper question.</b> MIW has not invented a sitting '
      'to hold this answer. The question above is MIW&rsquo;s own present-day '
      'statement of an examinable concept that keeps recurring; it carries no '
      'examination date, no printed serial and no printed mark, and its presence '
      'here is not evidence that any examiner set this wording. What it carries '
      'instead is a <b>review date</b>. A past-paper answer must stay true to its '
      'own sitting; this one must stay true to today.')
    a('</div></div>')

    # ------------------------------------------------------- the QI signal
    # The SAME governed projection block every other candidate surface uses.
    # Rendered against the FAMILY, because that is what this answer serves --
    # and the family's own recurrence is untouched by this page existing.
    fam_blocks = []
    for fid in e.get('family_ids') or []:
        blk = _family_signal(fid)
        if blk:
            fam_blocks.append(blk)
    if fam_blocks:
        a('<div class="ca-note"><div class="box">')
        a('  <b>Why MIW answered this.</b> ' + ' '.join(fam_blocks))
        a('</div></div>')

    a('<main id="ca-main">')

    if e.get('understand_first'):
        a('<section class="ca-sec"><div class="layer">')
        a('  <div class="layer-title">Understand first</div>')
        a('  <p>%s</p>' % esc(e['understand_first']))
        a('</div></section>')

    if e.get('exam_plan'):
        a('<section class="ca-sec"><div class="layer">')
        a('  <div class="layer-title">Exam plan</div>')
        render_blocks(e['exam_plan'], o, indent='    ')
        a('</div></section>')

    a('<section class="ca-sec"><div class="layer">')
    a('  <div class="layer-title">Model answer &mdash; current framework</div>')
    render_blocks(e['answer'], o, indent='    ')
    a('</div></section>')

    if e.get('study_guide'):
        a('<section class="ca-sec"><div class="layer">')
        a('  <div class="layer-title">Study guide</div>')
        render_blocks(e['study_guide'], o, indent='    ')
        a('</div></section>')

    if e.get('quick_revision'):
        a('<section class="ca-sec"><div class="layer">')
        a('  <div class="layer-title">Recall</div>')
        quick_revision(e['quick_revision'], o)
        a('</div></section>')

    _authority_block(e, a)

    # Where this concept HAS been examined. Statements, not claims about this
    # page: these are real sittings, and they are the evidence that made the
    # concept worth answering.
    ev = e.get('created_from') or []
    if ev:
        a('<section class="ca-sec"><div class="layer">')
        a('  <div class="layer-title">Where this concept has actually been set</div>')
        a('  <p>MIW holds printed question wording for these sittings. They are '
          'the evidence behind this answer &mdash; the answer itself belongs to '
          'none of them.</p>')
        a('  <ul>')
        for x in ev:
            a('    <li>%s</li>' % esc(x))
        a('  </ul>')
        a('</div></section>')

    sib = e.get('sibling_limbs') or []
    if sib:
        a('<section class="ca-sec"><div class="layer">')
        a('  <div class="layer-title">The other limbs of this question</div>')
        a('  <p>This entry answers <b>one</b> limb. The others are answered '
          'elsewhere, and each was reviewed on its own.</p>')
        a('  <ul>')
        for s in sib:
            href = s.get('href')
            label = '%s %s' % (s.get('limb_id', ''), s.get('limb_label', ''))
            if href:
                a('    <li>%s &mdash; <a href="%s">%s</a></li>'
                  % (esc(label), esc_attr(href), esc(s.get('owner_label', 'open'))))
            else:
                a('    <li>%s &mdash; %s</li>'
                  % (esc(label), esc(s.get('owner_label', ''))))
        a('  </ul>')
        a('</div></section>')

    _version_block(e, a)

    a('</main>')
    o.extend(footer(True))
    a('</body>')
    a('</html>')
    return '\n'.join(o) + '\n'


def _family_signal(fid):
    """One sentence about the family, from the governed QI layer.

    Reads the GATED projection through the same library every other surface
    uses. It reports what the family does; it never reports this page, because
    this page is not an occurrence.
    """
    try:
        doc = QIP.load()
    except Exception:
        return ''
    row = None
    for r in doc.get('questions', []):
        if fid in (r.get('canonical_family_ids') or []):
            row = r
            break
    if not row:
        return ''
    txt = row.get('longitudinal_text') or []
    if not txt:
        return ''
    return ('MIW&rsquo;s governed question intelligence reads this concept as: '
            '%s.' % ', '.join(t.lower() for t in txt))


# --------------------------------------------------------------------------

def write(path, text):
    prev = (io.open(path, encoding='utf-8', newline='').read()
            if os.path.exists(path) else None)
    with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    return 'IDENTICAL' if prev == text else ('CHANGED' if prev is not None else 'NEW')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true',
                    help='fail if anything on disk differs from what would be built')
    args = ap.parse_args()

    entries = M.load_entries()
    os.makedirs(M.PAGE_DIR, exist_ok=True)
    os.makedirs(M.SPEC_DIR, exist_ok=True)

    planned = {M.REGISTRY: json.dumps(build_registry(entries), indent=1,
                                      ensure_ascii=False) + '\n'}
    for caid, e in sorted(entries.items()):
        # DRAFT and AUTHORITY_ESTABLISHED entries are not rendered at all.
        # An unreviewed answer that merely lacks a badge is still an answer a
        # candidate can read and write in an exam.
        if e.get('review_status') not in M.RENDERABLE:
            continue
        planned[M.page_path(caid)] = build_page(e, entries)

    stale = []
    for path, text in sorted(planned.items()):
        rel = os.path.relpath(path, REPO).replace('\\', '/')
        if args.check:
            cur = (io.open(path, encoding='utf-8', newline='').read()
                   if os.path.exists(path) else None)
            st = 'IDENTICAL' if cur == text else ('MISSING' if cur is None else 'STALE')
            if st != 'IDENTICAL':
                stale.append(rel)
        else:
            st = write(path, text)
        print('%-52s %s' % (rel, st))

    # An orphaned page is a live URL for an answer that no longer exists.
    keep = {os.path.basename(p) for p in planned if p.endswith('.html')}
    for name in sorted(os.listdir(M.PAGE_DIR)) if os.path.isdir(M.PAGE_DIR) else []:
        if name.endswith('.html') and name not in keep:
            print('%-52s ORPHAN' % ('solvedQP/current/' + name))
            stale.append('solvedQP/current/' + name)

    if args.check and stale:
        print('\nSTALE: %s' % ', '.join(stale))
        return 1
    print('\n%d entry/entries, %d page(s)'
          % (len(entries), sum(1 for p in planned if p.endswith('.html'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())
