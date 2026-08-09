#!/usr/bin/env python3
"""Deterministic integrity tests for questions-<year>.html.

Two families of test, and the second matters more.

POSITIVE  -- every canonical question is present, exactly once, under the right
             month, with its printed marks and a correct recurrence tag.

NEGATIVE  -- no answer content reached the artefact, and no third-party
             recurrence annotation did either. These are the tests that would
             catch the page quietly becoming a free copy of the paid product,
             and they check the shipped BYTES, not the rendered view: content
             that is merely hidden by CSS has still been given away.

Run standalone or from run_toolchain.py.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from html import unescape as _unescape
from render_common import REPO_ROOT, strip_tags
import recurrence_model as RM

PP_DIR = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers')

# A source-copy host recurrence annotation: 2018/APR, 2025/SEP/Q6, 2022/MAR/1.
HOST_RECURRENCE = re.compile(r'\b(19|20)\d{2}/[A-Z]{3,5}\b')


def _norm(s):
    """Tag-free, lowercase, whitespace-collapsed. Leak testing compares BYTES
    that a reader could recover, so markup and spacing must not hide a match."""
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', str(s))).strip().lower()


def _sentences(blocks, min_words=9):
    """Distinctive prose fragments from an answer, for leak testing."""
    if not blocks:
        return []
    buf = []
    for b in blocks.get('blocks', []):
        if 'p' in b:
            buf.append(b['p'])
        for k in ('ul', 'ol'):
            for item in b.get(k, []):
                buf.append(item)
    out = []
    for chunk in buf:
        for s in re.split(r'(?<=[.;])\s+', strip_tags(chunk)):
            s = s.strip()
            if len(s.split()) >= min_words:
                out.append(s)
    return out


def check_year(year, errors, warnings):
    path = os.path.join(PP_DIR, 'questions-%d.html' % year)
    if not os.path.exists(path):
        errors.append('questions-%d.html does not exist' % year)
        return
    html = open(path, encoding='utf-8').read()

    specs = [json.load(open(p, encoding='utf-8'))
             for p in sorted(glob.glob(os.path.join(PP_DIR, 'specs', '*.json')))]
    nodes = RM.load_nodes(specs)
    relations = RM.build_families(nodes)
    year_nodes = [n for n in nodes.values() if n['year'] == year]

    if not year_nodes:
        errors.append('no canonical questions for %d' % year)
        return

    # ---- POSITIVE ---------------------------------------------------------
    ids = re.findall(r'id="(QP\d{4}-Q\d+)"', html)
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        errors.append('duplicate question ids in the page: %s' % ', '.join(dupes))
    missing = sorted({n['question_id'] for n in year_nodes} - set(ids))
    if missing:
        errors.append('%d canonical question(s) missing from the page: %s'
                      % (len(missing), ', '.join(missing)))
    extra = sorted(set(ids) - {n['question_id'] for n in year_nodes})
    if extra:
        errors.append('page carries question ids not in the %d canonical set: %s'
                      % (year, ', '.join(extra)))

    for n in year_nodes:
        # The FULL printed stem must be present, not a preview. Compare on
        # collapsed whitespace so the line-splitting in the renderer is allowed.
        stem = re.sub(r'\s+', ' ', strip_tags(n['text_verbatim'])).strip()
        # Unescape before comparing. The spec holds "Hull & Propeller"; the page
        # correctly holds "Hull &amp; Propeller", so comparing raw spec text
        # against escaped HTML reports a missing stem for any question with an
        # ampersand -- or any other escaped character -- in its first 120
        # characters. No 2026 stem had one, so this stayed latent until the 2025
        # intake landed three of them.
        flat = _unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', html)))
        if stem[:120] not in flat:
            errors.append('%s printed stem not found in the page' % n['question_id'])
        if '%s marks' % n['marks'] not in html:
            warnings.append('%s printed marks (%s) not rendered'
                            % (n['question_id'], n['marks']))

    # All twelve months named, so a gap is always explicit rather than silent.
    for mn in range(1, 13):
        if '%s %d' % (RM.MONTHS[mn - 1], year) not in html:
            errors.append('%s %d does not appear on the page' % (RM.MONTHS[mn - 1], year))

    # A month with no sitting must say WHY, and a known-absent sitting must not
    # be described the same way as one MIW simply has not built.
    from build_questions_year import KNOWN_ABSENT
    for (y, mn), _ in KNOWN_ABSENT.items():
        if y != year:
            continue
        month = RM.MONTHS[mn - 1]
        seg = html.split('%s %d' % (month, year), 1)
        if len(seg) < 2 or 'No examination paper exists' not in seg[1][:900]:
            errors.append('%s %d is a known-absent sitting but the page does not say so'
                          % (month, year))

    # Recurrence tag must match the CHRONOLOGY, not the authoring field.
    for n in year_nodes:
        rel = relations[n['question_id']]
        block = _card_block(html, n['question_id'])
        if block is None:
            continue
        if 'data-rec="%s"' % rel['filter'] not in block:
            errors.append('%s recurrence filter tag is wrong (expected %s)'
                          % (n['question_id'], rel['filter']))

    # ---- NEGATIVE ---------------------------------------------------------
    spec_q = {q['question_id']: q for d in specs for q in d['questions']}
    html_norm = _norm(html)   # normalised once; the sweep runs ~600 fragments
    leaks = 0
    for n in year_nodes:
        q = spec_q[n['question_id']]
        # An answer layer legitimately quotes the printed question -- QP2602-Q7's
        # answer_route step is word-for-word the examiner's own "(ii) signature
        # subject to ratification, acceptance or approval". Finding that on a page
        # whose entire purpose is to print the question is not a leak, and a sweep
        # that cannot tell the difference is the April false-positive lesson
        # repeating. Anything already present in the stem is adjudicated out.
        stem_norm = _norm(n['text_verbatim'] + ' ' +
                          ' '.join(sp.get('text', '') for sp in n['subparts']))

        def leaked(fragment, minimum=40):
            f = _norm(fragment)
            return len(f) >= minimum and f in html_norm and f not in stem_norm

        for s in _sentences(q.get('model_answer'))[:6] + _sentences(q.get('study_notes'))[:4]:
            if leaked(s[:70]):
                errors.append('ANSWER LEAK: %s model/study prose present in the page: %r'
                              % (n['question_id'], s[:70]))
                leaks += 1
                if leaks > 8:
                    return
        qr = q.get('quick_revision') or {}
        if leaked(strip_tags(qr.get('recall_15s') or '')[:60]):
            errors.append('ANSWER LEAK: %s quick-revision recall text present'
                          % n['question_id'])
        for card in (q.get('retrieval_cards') or [])[:3]:
            if leaked(strip_tags(card.get('answer', ''))[:60]):
                errors.append('ANSWER LEAK: %s retrieval card answer present' % n['question_id'])
        for step in (q.get('answer_route') or {}).get('steps', [])[:3]:
            for pt in (step.get('points') or [])[:2]:
                if leaked(strip_tags(pt)[:55]):
                    errors.append('ANSWER LEAK: %s answer_route point %r present'
                                  % (n['question_id'], strip_tags(pt)[:55]))

    hits = sorted(set(HOST_RECURRENCE.findall(html)))
    raw = HOST_RECURRENCE.search(html)
    if raw:
        errors.append('THIRD-PARTY RECURRENCE LEAK: source-copy annotation %r reached the page'
                      % raw.group(0))

    if 'noindex' not in html:
        warnings.append('questions-%d.html is not noindex (publish build?)' % year)


def _card_block(html, qid):
    i = html.find('id="%s"' % qid)
    if i < 0:
        return None
    return html[max(0, i - 400):i + 2500]


def main():
    errors, warnings = [], []
    specs = [json.load(open(p, encoding='utf-8'))
             for p in sorted(glob.glob(os.path.join(PP_DIR, 'specs', '*.json')))]
    years = sorted({d['year'] for d in specs})
    for y in years:
        check_year(y, errors, warnings)

    for w in warnings:
        print('  WARN  %s' % w)
    for e in errors:
        print('  FAIL  %s' % e)
    if errors:
        print('QUESTIONS YEAR: %d error(s), %d warning(s)' % (len(errors), len(warnings)))
        sys.exit(1)
    print('QUESTIONS YEAR: OK  %d year(s), %d warning(s)' % (len(years), len(warnings)))


if __name__ == '__main__':
    main()
