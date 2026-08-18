# -*- coding: utf-8 -*-
"""Sweep the archived official DG Shipping MEO Class I papers against the
official 185-item question bank and against MIW's own solved corpus.

RESEARCH ONLY. Phase 3B.

This answers the only question that decides whether the archived papers are
worth ingesting as history:

    does any question actually asked in an archived Class I sitting connect to
    an official bank item, or to a question MIW already holds?

It uses the hardened Phase-3A.3 classifier unchanged - no thresholds are
touched here. A sweep that had to loosen the classifier to find matches would
be measuring the loosening, not the history.

    python .../sweep_historical_papers.py <extract.json> [out.json]
"""
from __future__ import unicode_literals

import collections
import glob
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qi_similarity as qs                                        # noqa: E402
import qi_paths                                                   # noqa: E402

STRONG = ('EXACT_REPEAT', 'NEAR_VERBATIM')
REPORTABLE = STRONG + ('SAME_CORE_ASK',)


def load(path):
    with io.open(path, encoding='utf-8-sig') as fh:
        return json.load(fh)


def historical_units(extract):
    """Yield the comparable units of every archived paper.

    A unit is a printed question or a printed subpart - the paper's own
    divisions. No authoring scaffold is ever created here (LIMB_MODEL.md).
    """
    for p in extract['papers']:
        for q in p['questions']:
            subs = q.get('subparts') or []
            if subs:
                for sp in subs:
                    if sp.get('raw_text'):
                        yield p, q, sp['label'], sp['marks_printed'], sp['raw_text']
                # the whole question is also offered, so a bank item absorbed
                # into a multi-limb question is still findable
                if q.get('raw_text'):
                    yield p, q, '__WHOLE__', q.get('marks_printed'), q['raw_text']
            elif q.get('raw_text'):
                yield p, q, '__WHOLE__', q.get('marks_printed'), q['raw_text']


def corpus_stems():
    """MIW's own solved corpus, keyed for reporting."""
    out = []
    for f in sorted(glob.glob(os.path.join(qi_paths.SPECS, '*.json'))):
        spec = load(f)
        pid = spec.get('paper_id')
        for q in spec.get('questions', []):
            qid = q['question_id']
            if q.get('text_verbatim'):
                out.append((pid, qid, '__WHOLE__', qs.Stem(q['text_verbatim'])))
            for sp in (q.get('subparts') or []):
                if sp.get('label') and sp.get('text'):
                    out.append((pid, qid, sp['label'], qs.Stem(sp['text'])))
    return out


def best_of(stem, candidates):
    """candidates: iterable of (key, Stem). Returns (key, Result) or None."""
    best = None
    for key, cand in candidates:
        r = qs.classify(stem, cand)
        rank = (qs._RANK.get(r.cls, -1), max(r.fwd, r.rev))
        if best is None or rank > best[0]:
            best = (rank, key, r)
    if best is None:
        return None
    return best[1], best[2]


def main():
    if len(sys.argv) < 2:
        print('usage: sweep_historical_papers.py <extract.json> [out.json]')
        return 2
    extract = load(sys.argv[1])
    out_path = sys.argv[2] if len(sys.argv) > 2 else None

    bank = {int(k): v for k, v in load(qi_paths.EXTRACTED_BANK)['items'].items()}
    bank_items = [(n, qs.Stem(v)) for n, v in bank.items()]
    corpus = corpus_stems()
    corpus_items = [((pid, qid, lab), st) for pid, qid, lab, st in corpus]

    rows = []
    n_units = 0
    for p, q, lab, marks, text in historical_units(extract):
        n_units += 1
        stem = qs.Stem(text)

        bk = best_of(stem, bank_items)
        cp = best_of(stem, corpus_items)

        bank_cls = bk[1].cls if bk else 'NO_MEANINGFUL_MATCH'
        corp_cls = cp[1].cls if cp else 'NO_MEANINGFUL_MATCH'
        if bank_cls not in REPORTABLE and corp_cls not in REPORTABLE:
            continue

        row = {
            'file': p['file'],
            'subject': p['subject'],
            'printed_year': p['header']['printed_year'],
            'printed_month': p['header']['printed_month'],
            'date_evidence': p['header']['printed_month_source'],
            'is_sample_paper': p['header']['is_sample_paper'],
            'question_no': q['question_no'],
            'limb': lab,
            'marks_printed': marks,
            'text': text[:400],
        }
        if bk:
            row['bank_item'] = bk[0]
            row['bank_cls'] = bk[1].cls
            row['bank_fwd'] = round(bk[1].fwd, 2)
            row['bank_rev'] = round(bk[1].rev, 2)
        if cp:
            row['corpus_paper'] = cp[0][0]
            row['corpus_question'] = cp[0][1]
            row['corpus_limb'] = cp[0][2]
            row['corpus_cls'] = cp[1].cls
        rows.append(row)

    bank_counts = collections.Counter(r.get('bank_cls') for r in rows)
    corp_counts = collections.Counter(r.get('corpus_cls') for r in rows)

    print('archived papers        : %d' % len(extract['papers']))
    print('comparable units swept : %d' % n_units)
    print('reportable rows        : %d' % len(rows))
    print('')
    print('vs OFFICIAL BANK  : ' + ', '.join(
        '%s=%d' % (k, v) for k, v in bank_counts.most_common() if k))
    print('vs MIW CORPUS     : ' + ', '.join(
        '%s=%d' % (k, v) for k, v in corp_counts.most_common() if k))

    strong = [r for r in rows
              if r.get('bank_cls') in STRONG or r.get('corpus_cls') in STRONG]
    print('')
    print('strong (exact/near) rows: %d' % len(strong))
    for r in strong[:40]:
        print('  %s %s Q%s%s -> bank %s %s / corpus %s' % (
            r['file'], r['subject'][:22], r['question_no'],
            '' if r['limb'] == '__WHOLE__' else r['limb'],
            r.get('bank_item'), r.get('bank_cls'), r.get('corpus_cls')))

    if out_path:
        with io.open(out_path, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps({
                'schema': 'miw.pastpapers.qi_v2.historical_sweep.v1',
                'status': 'RESEARCH_ONLY',
                'units_swept': n_units,
                'papers': len(extract['papers']),
                'bank_class_counts': dict(bank_counts),
                'corpus_class_counts': dict(corp_counts),
                'rows': rows,
            }, indent=1, ensure_ascii=False) + '\n')
        print('\nwrote %s' % out_path)
    return 0


if __name__ == '__main__':
    sys.exit(main())
