# -*- coding: utf-8 -*-
"""Sweep the official DG Shipping MEO CL-I bank against the whole solved corpus.

Phase 3A change: this tool no longer carries its own classifier. It calls
tools/qi_similarity.py, so the short-stem floor and the examiner-demand,
actor, polarity and number guards apply here exactly as they do in the
controls. Phase 2's floor lived in this file's loop instead, which meant the
classifier could be called directly and would happily return an exact repeat
for the word "Deviation".

    python .../match_bank_to_corpus.py [out.json] [--compare old.json]

`--compare` prints the Phase-2 vs Phase-3A delta match by match, which is how
the drop from the Phase-2 headline is accounted for rather than asserted.
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

# Phase 3A pointed both of these at an absolute Desktop drive. SPECS is
# committed repository content sitting two directories above this tool, so the
# sweep and the QP2608 Paper DNA were not reproducible from a clean checkout.
BANK = qi_paths.EXTRACTED_BANK
SPECS = qi_paths.SPECS

# Classes the layer treats as a strong recurrence signal.
STRONG = ('EXACT_REPEAT', 'NEAR_VERBATIM')
REPORTABLE = STRONG + ('SAME_CORE_ASK',)


def load(path):
    with io.open(path, encoding='utf-8-sig') as fh:
        return json.load(fh)


def sweep():
    bank = {int(k): v for k, v in load(BANK)['items'].items()}
    bank_stems = {n: qs.Stem(v) for n, v in bank.items()}

    hits = []
    for f in sorted(glob.glob(os.path.join(SPECS, '*.json'))):
        spec = load(f)
        pid = spec.get('paper_id')
        for q in spec.get('questions', []):
            qid = q['question_id']
            rows = [('__WHOLE__', q.get('total_marks'), q.get('text_verbatim'))]
            for sp in (q.get('subparts') or []):
                if sp.get('label'):
                    rows.append((sp['label'], sp.get('marks'), sp['text']))
            for lab, marks, text in rows:
                if not text:
                    continue
                stem = qs.Stem(text)
                best = None
                for n, bs in bank_stems.items():
                    r = qs.classify(stem, bs)
                    key = (qs._RANK.get(r.cls, -1), max(r.fwd, r.rev))
                    if best is None or key > best[0]:
                        best = (key, n, r)
                if best is None:
                    continue
                _, n, r = best
                if r.cls in ('NO_MEANINGFUL_MATCH', 'UNSCOREABLE_SHORT_STEM'):
                    # still recorded, so the delta can explain a lost match
                    if r.cls == 'NO_MEANINGFUL_MATCH':
                        continue
                hits.append(dict(
                    paper=pid, question=qid, limb=lab, marks=marks,
                    bank_item=n, fwd=round(r.fwd, 2), rev=round(r.rev, 2),
                    demand=round(r.demand_compat, 2), actor=r.actor_rel,
                    cls=r.cls, containment=r.containment_class,
                    reasons=r.reasons))
    return hits


def main():
    args = [a for a in sys.argv[1:]]
    compare = None
    if '--compare' in args:
        i = args.index('--compare')
        compare = args[i + 1]
        del args[i:i + 2]
    out = args[0] if args else None

    hits = sweep()
    strong = [h for h in hits if h['cls'] in STRONG]
    core = [h for h in hits if h['cls'] == 'SAME_CORE_ASK']

    print('QI-v2 bank-vs-corpus sweep  (classifier: tools/qi_similarity.py)')
    print('  reportable matches : %d' % len([h for h in hits if h['cls'] in REPORTABLE]))
    print('  strong  (exact/near): %d' % len(strong))
    print('  same core ask       : %d' % len(core))
    print()
    print('%-9s %-14s %-10s %5s %-9s %5s %5s %5s %-9s %s'
          % ('PAPER', 'QUESTION', 'LIMB', 'MK', 'BANK', 'FWD', 'REV', 'DMD',
             'ACTOR', 'CLASS'))
    for h in sorted(strong, key=lambda x: (x['paper'], x['question'])):
        print('%-9s %-14s %-10s %5s BANK-%-4s %5.2f %5.2f %5.2f %-9s %s'
              % (h['paper'], h['question'], h['limb'], h['marks'],
                 h['bank_item'], h['fwd'], h['rev'], h['demand'],
                 h['actor'], h['cls']))

    print()
    print('=== PAPERS BY STRONG-MATCH COUNT ===')
    for p, c in collections.Counter(h['paper'] for h in strong).most_common():
        print('  %s  %d' % (p, c))

    if compare:
        old = load(compare)
        oldstrong = {(h['paper'], h['question'], h['limb']): h for h in old
                     if h['cls'] in ('EXACT_OR_NEAR_VERBATIM',
                                     'ANCESTOR_ABSORBED_AND_EXTENDED',
                                     'ANCESTOR_NARROWED')}
        newstrong = {(h['paper'], h['question'], h['limb']): h for h in strong}
        lost = sorted(set(oldstrong) - set(newstrong))
        gained = sorted(set(newstrong) - set(oldstrong))
        print()
        print('=== PHASE-2 -> PHASE-3A DELTA ===')
        print('  Phase-2 strong : %d' % len(oldstrong))
        print('  Phase-3A strong: %d' % len(newstrong))
        print('  lost           : %d' % len(lost))
        print('  gained         : %d' % len(gained))
        print()
        by = {h['cls'] for h in hits}
        for k in lost:
            o = oldstrong[k]
            now = next((h for h in hits
                        if (h['paper'], h['question'], h['limb']) == k), None)
            print('  LOST  %-9s %-14s %-8s was %-32s now %s'
                  % (k[0], k[1], k[2], o['cls'],
                     now['cls'] if now else 'NO_MEANINGFUL_MATCH'))
            if now:
                for r in now['reasons']:
                    print('          reason: %s' % r)
        for k in gained:
            n = newstrong[k]
            print('  GAINED %-9s %-14s %-8s now %s (BANK-%s fwd %.2f rev %.2f)'
                  % (k[0], k[1], k[2], n['cls'], n['bank_item'],
                     n['fwd'], n['rev']))
        del by

    if out:
        with io.open(out, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(hits, indent=1, ensure_ascii=False))
        print('\nwrote %s' % out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
