#!/usr/bin/env python3
"""The gate on the candidate-safe QI projection. Fails closed.

    python tools/study/validate_qi_projection.py

Thirteen invariants, and they are deliberately split between the ARTEFACT and the
SHIPPED BYTES. Checking the projection alone would prove that the right thing
was computed and nothing at all about what a candidate can read: the failure
this layer exists to prevent is a page that says more than the evidence
supports, and a page is bytes.

    R-PROJ-A   every modern repeat tag on a page is the calendar model's own
    R-PROJ-B   every longitudinal tag on a page is in the projection's closed
               vocabulary AND is the one that question was projected
    R-PROJ-C   no longitudinal tag on a question with no governed family
    R-PROJ-D   no secondary-claimed date, year or count reaches a candidate
    R-PROJ-E   readiness reaches only the answer a governed record NAMES
    R-PROJ-F   an unsafe currentness never renders as verified
    R-PROJ-G   a historical variant never inherits its successor's readiness
    R-PROJ-H   the modern tag population is intact -- one per question, none lost
    R-PROJ-I   all nine August 2026 questions are accounted for
    R-PROJ-J   the workbook's prose matches the architecture that is live
    R-PROJ-K   topic readiness on the page equals the adapter's
    R-PROJ-L   Phase-1 recurrence is untouched by projection work
"""
import glob
import io
import json
import os
import re
import sys
from html import unescape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'tools', 'pastpapers'))

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import qi_projection as QIP
import study_qi_adapter as SQI
import recurrence_model as RM

D = os.path.join(ROOT, 'docs', 'study')

#: Every candidate-facing surface that may carry the projection, and whether
#: the middleware matcher gates it. Derived from middleware.js, not assumed:
#: a path off the matcher is PUBLIC because the gate is never invoked there.
GATED_GLOBS = ('solvedQP/questions-*.html', 'solvedQP/QP*.html',
               'meoclass1/pastpapers/questions-*.html',
               'meoclass1/pastpapers/QP*.html',
               'meoclass1/topics.html', 'meoclass1/study.html')
PUBLIC_GLOBS = ('SQ/*.html', 'index.html', 'archive/*.html')

BLOCK = re.compile(r'<div class="qy-long">(.*?)</div>', re.S)
CHIP = re.compile(r'<span class="q-tag[^"]*">(.*?)</span>')
REC_TAG = re.compile(r'<span class="q-tag rec">(.*?)</span>')

# The two candidate surfaces do NOT share a card shape and pretending they do
# is how a census silently measures one of them twice. The year sheet keys the
# card on the canonical id; the solved paper keys it on the in-page anchor and
# carries the canonical id in data-qid.
YEAR_CARD = re.compile(r'<div class="hit" [^>]*id="(QP\d{4}-Q\d+)"')
PAPER_CARD = re.compile(r'<article class="q-card" [^>]*data-qid="(QP\d{4}-Q\d+)"')

# The solved paper prints a SECOND rec badge -- "N sittings in this set" -- next
# to the status label. It is a count of the family, not a status, and it is a
# legitimate part of the modern layer; the census has to know the difference
# rather than report it as an unknown tag.
SITTINGS_BADGE = re.compile(r'^\d+ sittings? in this set$')

FAILS = []
PASSES = []
QUIET = False


def ok(rule, cond, detail=''):
    (PASSES if cond else FAILS).append((rule, detail))
    if not QUIET:
        print('  %s %-14s %s' % ('PASS' if cond else 'FAIL', rule,
                                 '' if cond else detail))


def _read(p):
    return io.open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()


def _files(globs):
    out = []
    for g in globs:
        out += sorted(glob.glob(os.path.join(ROOT, g)))
    return [os.path.relpath(p, ROOT).replace('\\', '/') for p in out]


def page_cards(text):
    """(question_id, modern_tag, [longitudinal chips]) for every card on a page.

    Sliced on the card boundary rather than scanned whole-page, because the
    assertion is about what sits inside ONE card: a chip that drifted into the
    neighbouring question is exactly the defect a page-wide chip census would
    call clean.
    """
    starts = [(m.start(), m.group(1)) for m in YEAR_CARD.finditer(text)]
    starts += [(m.start(), m.group(1)) for m in PAPER_CARD.finditer(text)]
    starts.sort()
    out = []
    for i, (pos, qid) in enumerate(starts):
        body = text[pos:starts[i + 1][0] if i + 1 < len(starts) else len(text)]
        tags = [t for t in REC_TAG.findall(body) if not SITTINGS_BADGE.match(t)]
        blk = BLOCK.search(body)
        chips = CHIP.findall(blk.group(1)) if blk else []
        out.append((qid, tags[0] if tags else None, chips))
    return out


def run():
    """Run every invariant and return the list of failed rule ids.

    Separated from main() so the mutation suite can drive the gate in-process
    and assert on WHICH rule caught a mutation, rather than on an exit code
    that cannot tell one failure from another.
    """
    del FAILS[:], PASSES[:]
    QIP._CACHE.clear()
    proj = QIP.build() if os.environ.get('QIP_LIVE') else QIP.load()
    by_id = {r['question_id']: r for r in proj['questions']}
    gated = _files(GATED_GLOBS)
    public = _files(PUBLIC_GLOBS)

    # Card census over every gated surface that renders question cards.
    cards = []
    for p in gated:
        if '/topics.html' in p or '/study.html' in p:
            continue
        cards += [(p,) + c for c in page_cards(_read(p))]

    if not QUIET:
        print('QI projection gate  (%d gated surfaces, %d cards, %d projected '
              'questions)' % (len(gated), len(cards), len(proj['questions'])))

    # ---- FRESH ---------------------------------------------------------
    # The artefact must be exactly what its inputs produce. Without this the
    # rest of the gate validates the pages against a file anyone could edit,
    # and a hand-removed currentness warning would make page and model agree
    # on the wrong answer.
    fresh = QIP.build()
    stale = [k for k in ('questions', 'topics', 'families', 'totals')
             if json.dumps(fresh[k], sort_keys=True)
             != json.dumps(proj[k], sort_keys=True)]
    ok('R-PROJ-FRESH', not stale,
       'safe_qi_projection.json does not match its inputs: %s' % stale)

    # ---- A -----------------------------------------------------------------
    legal_modern = set(RM.STATUS_LABEL.values())
    bad = sorted({t for _, _, t, _ in cards if t and t not in legal_modern})
    ok('R-PROJ-A', not bad,
       'modern tags not produced by recurrence_model: %s' % bad)

    # ---- B -----------------------------------------------------------------
    vocab = set(QIP.LONGITUDINAL_TEXT.values()) | {QIP.WIDER_RECURRENCE_TEXT} \
        | set(QIP.READINESS_TEXT.values()) | set(QIP.READY_TEXT_BY_BASIS.values()) \
        | set(QIP.CURRENTNESS_TEXT.values())
    # BOTH directions. Checking only that the page says nothing extra leaves
    # the opposite defect wide open: a warning silently dropped from a card
    # reads as "no warning", which is the more dangerous of the two.
    off_vocab, wrong_q, dropped = [], [], []
    for path, qid, _, chips in cards:
        expected = {t for _, t in QIP.tags_for(qid, audience='GATED', doc=proj)}
        for c in chips:
            if c not in vocab and not c.startswith('Current framework: see '):
                off_vocab.append('%s %s: %r' % (path, qid, c))
            if c not in expected:
                wrong_q.append('%s %s: %r' % (path, qid, c))
        for e in sorted(expected - set(chips)):
            dropped.append('%s %s: %r' % (path, qid, e))
    ok('R-PROJ-B', not off_vocab and not wrong_q and not dropped,
       'off-vocabulary %s; not projected for that question %s; projected but '
       'not rendered %s' % (off_vocab[:3], wrong_q[:3], dropped[:3]))

    # ---- C -----------------------------------------------------------------
    orphan = [('%s %s' % (p, q)) for p, q, _, chips in cards
              if chips and not (by_id.get(q) or {}).get('canonical_family_ids')]
    ok('R-PROJ-C', not orphan,
       'longitudinal chips on questions with no governed family: %s' % orphan[:5])

    # ---- D -----------------------------------------------------------------
    # A secondary-claimed year or count must not reach a candidate in any form.
    # Two probes: a label that does not survive on printed evidence alone, and
    # a literal pre-2021 year or "asked N times" phrasing inside a chip.
    unsafe_label, dated = [], []
    printed_ok = {}
    for fid, f in proj['families'].items():
        printed_ok[fid] = set(f['labels_printed_only'])
    for path, qid, _, chips in cards:
        row = by_id.get(qid) or {}
        for sig in row.get('longitudinal_signal') or ():
            if sig == QIP.WIDER_RECURRENCE:
                continue
            if not any(sig in printed_ok.get(f, set())
                       for f in row.get('canonical_family_ids') or ()):
                unsafe_label.append('%s %s: %s' % (path, qid, sig))
        for c in chips:
            if re.search(r'\b(19\d{2}|20(0\d|1\d|20))\b', c) or \
                    re.search(r'\basked\s+\d+\s+times\b', c, re.I):
                dated.append('%s %s: %r' % (path, qid, c))
    ok('R-PROJ-D', not unsafe_label and not dated,
       'labels not surviving printed evidence %s; dated/counted claims %s'
       % (unsafe_label[:3], dated[:3]))

    # ---- E -----------------------------------------------------------------
    p2 = json.load(open(os.path.join(HERE, 'qi_phase2_adjudications.json'),
                        encoding='utf-8'))
    named = set()
    for r in p2['families']:
        v = r.get('canonical_current_answer')
        nid = v.get('question_id') if isinstance(v, dict) else v
        if nid:
            named.add(nid)
    wrong = [r['question_id'] for r in proj['questions']
             if r['readiness_basis'] == 'PHASE2_GOVERNED_REVIEW'
             and r['question_id'] not in named]
    ok('R-PROJ-E', not wrong,
       'verified readiness on questions no governed record names: %s' % wrong[:5])

    # ---- F -----------------------------------------------------------------
    # Agreement with the adapter is proved, not copied.
    same = QIP.UNSAFE_CURRENTNESS == SQI.UNSAFE_CURRENTNESS
    leak = [r['question_id'] for r in proj['questions']
            if r['readiness_text'] == QIP.READY_TEXT_BY_BASIS['PHASE2_GOVERNED_REVIEW']
            and r['readiness_basis'] != 'PHASE2_GOVERNED_REVIEW']
    hold = [r['question_id'] for r in proj['questions']
            if r['raw_readiness'] == ['CURRENTNESS_HOLD'] and r['readiness_basis']]
    ok('R-PROJ-F', same and not leak and not hold,
       'unsafe-set drift=%s; verified wording without governed basis %s; '
       'hold carrying a readiness basis %s' % (not same, leak[:3], hold[:3]))

    # ---- G -----------------------------------------------------------------
    bad_inherit = []
    for r in p2['families']:
        if r['final_state'] != 'SUPERSEDED_WITH_SUCCESSOR':
            continue
        v = r.get('canonical_current_answer')
        nid = v.get('question_id') if isinstance(v, dict) else v
        for q in proj['questions']:
            if r['family_id'] in (q['canonical_family_ids'] or ()) \
                    and q['question_id'] != nid \
                    and q['readiness_basis'] == 'PHASE2_GOVERNED_REVIEW':
                bad_inherit.append(q['question_id'])
    ok('R-PROJ-G', not bad_inherit,
       'historical variants inheriting successor readiness: %s' % bad_inherit[:5])

    # ---- H -----------------------------------------------------------------
    missing = [(p, q) for p, q, t, _ in cards if not t]
    ok('R-PROJ-H', not missing and len(cards) > 0,
       '%d cards carry no modern recurrence tag: %s' % (len(missing), missing[:5]))

    # ---- I -----------------------------------------------------------------
    aug = {'QP2608-Q%d' % i for i in range(1, 10)}
    in_proj = aug - set(by_id)
    on_page = aug - {q for p, q, _, _ in cards if 'questions-2026' in p}
    ok('R-PROJ-I', not in_proj and not on_page,
       'absent from projection %s; absent from the 2026 year sheet %s'
       % (sorted(in_proj), sorted(on_page)))

    # ---- J -----------------------------------------------------------------
    import importlib
    import export_roadmap_xlsx as RX
    # Reloaded on purpose: the assertion is about what the exporter SAYS TODAY.
    # A cached module would let an edit to its prose pass unnoticed, which is
    # exactly the staleness this rule exists to catch.
    RX = importlib.reload(RX)
    model = RX.build_model()
    L = model.get('longitudinal_qi') or {}
    fam = json.load(open(os.path.join(D, 'qi', 'qi_families.json'), encoding='utf-8'))
    occ = json.load(open(os.path.join(D, 'qi', 'qi_occurrences.json'), encoding='utf-8'))
    # ...and the SHIPPED workbook, not only the model behind it.
    shipped_ok, shipped_why = True, ''
    xlsx = os.path.join(D, 'MIW_MEO_Class1_Study_Roadmap.xlsx')
    if os.path.exists(xlsx):
        try:
            import openpyxl
            ws = openpyxl.load_workbook(xlsx, read_only=True)['WRITTEN QI']
            body = ' ~ '.join(' | '.join(str(c) for c in r if c is not None)
                              for r in ws.values)
            shipped_ok = ('CANONICAL LONGITUDINAL QI' in body
                          and 'LIVE' in body
                          and str(fam['counts']['families']) in body)
            shipped_why = '' if shipped_ok else 'WRITTEN QI sheet omits the live layer'
        except ImportError:
            shipped_why = '(openpyxl absent -- shipped workbook not read)'
    ok('R-PROJ-J',
       L.get('status') == 'LIVE'
       and L.get('families') == fam['counts']['families']
       and L.get('occurrences') == occ['counts']['recurrence_bearing']
       and 'NOT YET INTEGRATED' not in str(L)
       and shipped_ok,
       'the workbook does not describe the live longitudinal layer: %s %s'
       % (L.get('status'), shipped_why))

    # ---- K -----------------------------------------------------------------
    sq = json.load(open(os.path.join(D, 'study_qi.json'), encoding='utf-8'))
    drift = []
    for t in model['topics']:
        a = sq['topics'].get(t['topic_id']) or {}
        if t['families_ready_now'] != a.get('ready_to_study_now', 0) or \
                t['families_mapped'] != a.get('mapped_families', 0):
            drift.append(t['topic_id'])
    # Per SECTION, never page-wide. A substring search over the whole document
    # passes whenever ANY topic happens to carry the number being looked for,
    # so inflating D01's chip to a figure D02 legitimately shows would slip
    # straight through.
    topics_html = _read('meoclass1/topics.html')
    sections = dict(re.findall(
        r'<section class="t-section" id="(D\d\d)">(.*?)</section>',
        topics_html, re.S))
    page_drift = []
    for t in model['topics']:
        body = sections.get(t['topic_id'], '')
        found = re.findall(r'<span class="chip ready">(\d+) ready to study</span>', body)
        want = [str(t['families_ready_now'])] if t['families_ready_now'] else []
        if found != want:
            page_drift.append('%s page=%s model=%s' % (t['topic_id'], found, want))
    ok('R-PROJ-K', not drift and not page_drift,
       'model vs adapter %s; page vs model %s' % (drift, page_drift))

    # ---- L -----------------------------------------------------------------
    ok('R-PROJ-L',
       fam['counts']['families'] == 270 and occ['counts']['recurrence_bearing'] == 1584,
       'Phase-1 recurrence moved: %d families, %d occurrences'
       % (fam['counts']['families'], occ['counts']['recurrence_bearing']))

    # ---- public tier -------------------------------------------------------
    banned = set(QIP.READINESS_TEXT.values()) | set(QIP.READY_TEXT_BY_BASIS.values()) \
        | set(QIP.CURRENTNESS_TEXT.values())
    leaks = []
    for p in public:
        body = unescape(_read(p))
        for b in banned:
            if unescape(b) in body:
                leaks.append('%s: %r' % (p, b))
    ok('R-PROJ-PUB', not leaks,
       'answer-readiness wording on a surface off the middleware matcher: %s'
       % leaks[:5])

    return [r for r, _ in FAILS]


def main():
    failed = run()
    print()
    if failed:
        print('QI projection gate FAILED: %d of %d invariants -- %s'
              % (len(failed), len(failed) + len(PASSES), ', '.join(failed)))
        sys.exit(1)
    print('QI projection gate: %d invariants hold.' % len(PASSES))


if __name__ == '__main__':
    main()
