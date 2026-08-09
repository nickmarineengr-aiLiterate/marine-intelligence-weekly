#!/usr/bin/env python3
"""Deterministic tests for the free Solved QP sample.

The negative tests are the point of this file. A marketing page that renders
the paid product and hides it with CSS has given the product away; the only
honest proof is that the withheld bytes are not in the artefact at all. Every
check below therefore reads the shipped file, not a browser view.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render_common import REPO_ROOT, strip_tags
import recurrence_model as RM

PP_DIR = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers')
HOST_RECURRENCE = re.compile(r'\b(19|20)\d{2}/[A-Z]{3,5}\b')
RUPEE_VALUE = re.compile(r'(?:&#8377;|₹|Rs\.?\s*)\s*\d')


def _norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', str(s))).strip().lower()


def _answer_fragments(q, limit=14):
    """Distinctive prose from deep inside the answer -- especially LATER
    paragraphs, which is where a CSS-hidden leak would still be recoverable."""
    frags = []
    blocks = (q.get('model_answer') or {}).get('blocks', [])
    for b in blocks:
        if 'p' in b:
            frags.append(strip_tags(b['p']))
        for k in ('ul', 'ol'):
            for item in b.get(k, []):
                frags.append(strip_tags(item))
    # Skip the opening: take from the middle and the tail, which no legitimate
    # preview would ever contain.
    frags = [f for f in frags if len(f.split()) >= 12]
    return frags[len(frags) // 3:][:limit]


def check(cfg_path, errors, warnings):
    cfg = json.load(open(cfg_path, encoding='utf-8'))
    out = os.path.join(REPO_ROOT, cfg['output'].replace('/', os.sep))
    name = cfg['output']
    if not os.path.exists(out):
        errors.append('%s does not exist' % name)
        return
    html = open(out, encoding='utf-8').read()
    hn = _norm(html)

    specs = [json.load(open(p, encoding='utf-8'))
             for p in sorted(glob.glob(os.path.join(PP_DIR, 'specs', '*.json')))]
    spec = next(d for d in specs if d['paper_id'] == cfg['paper_id'])
    relations = RM.build_families(RM.load_nodes(specs))
    demo = set(cfg['full_demo_questions'])

    # ---- 1. the whole sitting is visible ---------------------------------
    for q in spec['questions']:
        stem = _norm(q['text_verbatim'])[:110]
        if stem not in hn:
            errors.append('%s: printed stem for %s is missing' % (name, q['q_no']))
    if len(re.findall(r'class="q-card"', html)) != len(spec['questions']):
        errors.append('%s: expected %d question cards' % (name, len(spec['questions'])))

    # ---- 2. exactly the approved demos are complete ----------------------
    for q in spec['questions']:
        block = _card(html, q['anchor'])
        if block is None:
            errors.append('%s: no card for %s' % (name, q['q_no']))
            continue
        is_full = 'data-demo="full"' in block
        if is_full != (q['q_no'] in demo):
            errors.append('%s: %s full-demo flag is wrong (config says %s)'
                          % (name, q['q_no'], q['q_no'] in demo))
            continue
        if is_full:
            for mode in ('understand', 'plan', 'answer', 'guide', 'recall'):
                if 'data-mode="%s"' % mode not in block:
                    errors.append('%s: demo %s is missing the %s mode' % (name, q['q_no'], mode))
            if 'Model written answer' not in block:
                errors.append('%s: demo %s has no model answer' % (name, q['q_no']))
            if 'Study guide' not in block:
                errors.append('%s: demo %s has no study guide' % (name, q['q_no']))

    # ---- 3. a demo must not unlock a paid paper --------------------------
    for qno in demo:
        q = next(x for x in spec['questions'] if x['q_no'] == qno)
        rel = relations[q['question_id']]
        if rel['family_size'] > 1:
            errors.append('%s: full demo %s belongs to a recurrence family with %s -- '
                          'publishing it publishes those paid questions'
                          % (name, q['question_id'], ', '.join(rel['others'])))

    # ---- 4. NEGATIVE: no preview answer content in the shipped bytes -----
    for q in spec['questions']:
        if q['q_no'] in demo:
            continue
        qid = q['question_id']
        for frag in _answer_fragments(q):
            probe = _norm(frag)[:70]
            if len(probe) >= 40 and probe in hn:
                errors.append('ANSWER LEAK: %s later-paragraph answer text is present in %s: %r'
                              % (qid, name, probe))
                break
        sg = (q.get('study_notes') or {}).get('blocks', [])
        for b in sg:
            if 'p' in b:
                probe = _norm(b['p'])[:70]
                if len(probe) >= 40 and probe in hn:
                    errors.append('STUDY GUIDE LEAK: %s study-guide prose present in %s' % (qid, name))
                    break
        qr = q.get('quick_revision') or {}
        for k in ('recall_15s', 'major_trap', 'critical_regulation'):
            probe = _norm(qr.get(k) or '')[:60]
            if len(probe) >= 40 and probe in hn:
                errors.append('QUICK REVISION LEAK: %s %s present in %s' % (qid, k, name))
        for card in (q.get('retrieval_cards') or []):
            probe = _norm(card.get('answer', ''))[:60]
            if len(probe) >= 40 and probe in hn:
                errors.append('FLASHCARD LEAK: %s card answer present in %s' % (qid, name))
                break
        # Route POINTS are withheld; route TITLES are the deliberate preview.
        stem_norm = _norm(q['text_verbatim'])
        for step in (q.get('answer_route') or {}).get('steps', []):
            for pt in (step.get('points') or []):
                probe = _norm(pt)[:55]
                if len(probe) >= 40 and probe in hn and probe not in stem_norm:
                    errors.append('ROUTE POINT LEAK: %s point %r present in %s'
                                  % (qid, probe, name))
                    break

    # ---- 5. no other paper's answers, above all not July -----------------
    for d in specs:
        if d['paper_id'] == cfg['paper_id']:
            continue
        for q in d['questions']:
            frags = _answer_fragments(q, limit=4)
            for frag in frags:
                probe = _norm(frag)[:70]
                if len(probe) >= 45 and probe in hn:
                    errors.append('CROSS-PAPER LEAK: %s answer text present in %s'
                                  % (q['question_id'], name))
                    break

    # ---- 6. conversion surface -------------------------------------------
    previews = [q for q in spec['questions'] if q['q_no'] not in demo]
    locks = html.count('class="sq-lock"')
    if locks < len(previews) + 1:
        errors.append('%s: expected a lock block on each of the %d preview questions plus the '
                      'paper-level offer; found %d' % (name, len(previews), locks))
    if cfg['commercial']['cta_href'] not in html:
        errors.append('%s: CTA target %s is missing' % (name, cfg['commercial']['cta_href']))

    # ---- 7. no invented price --------------------------------------------
    if cfg['commercial']['price_display'] == 'PRICE_TBD' and RUPEE_VALUE.search(html):
        errors.append('%s: a currency value is rendered while the price is PRICE_TBD'
                      % name)

    # ---- 8. no third-party recurrence annotation -------------------------
    m = HOST_RECURRENCE.search(html)
    if m:
        errors.append('%s: third-party recurrence annotation %r reached the page' % (name, m.group(0)))

    # ---- 9. review state --------------------------------------------------
    if 'noindex' not in html:
        warnings.append('%s is not noindex -- correct only for an approved publish build' % name)


def _card(html, anchor):
    i = html.find('id="%s"' % anchor)
    if i < 0:
        return None
    j = html.find('</article>', i)
    return html[i:j if j > 0 else len(html)]


def main():
    errors, warnings = [], []
    configs = sorted(glob.glob(os.path.join(PP_DIR, 'sample', '*.sample.json')))
    if not configs:
        print('SAMPLE: no projection config found')
        sys.exit(1)
    for c in configs:
        check(c, errors, warnings)
    for w in warnings:
        print('  WARN  %s' % w)
    for e in errors:
        print('  FAIL  %s' % e)
    if errors:
        print('SAMPLE: %d error(s), %d warning(s)' % (len(errors), len(warnings)))
        sys.exit(1)
    print('SAMPLE: OK  %d sample(s), %d warning(s)' % (len(configs), len(warnings)))


if __name__ == '__main__':
    main()
