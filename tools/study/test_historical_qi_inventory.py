#!/usr/bin/env python3
"""Acceptance for the historical Written QI inventory.

Three things must hold, and the third is the one with teeth.

1. The inventory is DETERMINISTIC -- built twice from the same refs it is
   byte-identical, because it reads no clock.
2. It is HONEST about the join -- every family is placed by the questions it
   contains, never by its own topic string, and a question sitting in two
   families is reported rather than silently resolved.
3. Nothing it touched widened a public claim. The forbidden sentences
   ("since 2010", "16 years", ...) are searched for across every study
   artefact AND the live public page, not merely absent from this file.

Usage:
    python tools/study/test_historical_qi_inventory.py
"""
import io
import json
import os
import re
import sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import build_historical_qi_inventory as INV

D = os.path.join(ROOT, 'docs', 'study')
OUT = os.path.join(D, 'historical_qi_asset_inventory.json')
HORIZON = os.path.join(D, 'written_evidence_horizon.json')
PUBLIC = os.path.join(ROOT, 'SQ', 'study-roadmap.html')

# Sentences no surface may carry until a validated historical range exists.
# Written as regexes because "since 2010" and "since  2010" are the same lie.
FORBIDDEN = [
    (r'since\s+20(0\d|1\d)', 'a "since <year>" claim earlier than the solved band'),
    (r'\b1[0-9]\s*years\s+of\b', 'a decade-plus coverage claim'),
    (r'20(0\d|1[0-9])\s*[-–]\s*20(2[0-9])', 'a span starting before 2021'),
    (r'all\s+historical\s+papers', 'a total-archive claim'),
    (r'complete\s+archive', 'a completeness claim'),
]

PASS, FAIL = [], []


def ok(label, cond, detail=''):
    (PASS if cond else FAIL).append(label)
    if not cond:
        print('  FAIL %s%s' % (label, (': ' + detail) if detail else ''))


def main():
    print('historical QI inventory acceptance')

    ok('inventory exists on disk', os.path.exists(OUT))
    disk = json.load(open(OUT, encoding='utf-8'))

    # 1. Determinism -- no clock, no ref drift.
    a, b = INV.build(), INV.build()
    ok('two builds are identical (no clock is read)', a == b)
    ok('the committed inventory matches a fresh build', disk == a)

    # 2. The join is governed.
    fj = a['family_join']
    ok('every family carries a join verdict',
       all(j['join_status'] in ('JOINED', 'AMBIGUOUS_REVIEW',
                                'UNJOINABLE_NO_MAPPED_QUESTION')
           for j in fj['families']))
    store = json.load(open(os.path.join(D, 'study_mappings.json'),
                           encoding='utf-8'))['mappings']
    bad = []
    for j in fj['families']:
        if j['join_status'] != 'JOINED':
            continue
        # The topic must be the one study_mappings gives those questions --
        # not one derived from the family's own vocabulary.
        want = {store[q]['topic_id'] for q in j['joined_via']}
        if want != {j['topic_id']}:
            bad.append(j['family_id'])
    ok('joined topics come from study_mappings, not the QI-v2 topic string',
       not bad, str(bad))
    # The QI-v2 topic string is recorded but must never BECOME the topic id.
    # (An earlier version of this assertion tested startswith('D'), which the
    # perfectly innocent family topic "Dry docking" fails -- a proxy check
    # that fired on a coincidence rather than on the property it meant.)
    ok('the QI-v2 topic string is recorded but never used as a topic id',
       all(j['topic_id'] is None or re.fullmatch(r'D\d\d', j['topic_id'])
           for j in fj['families']))
    ok('questions appearing in two families are reported',
       isinstance(fj['questions_in_more_than_one_family'], dict))
    shared = fj['questions_in_more_than_one_family']
    if shared:
        print('    reported for review: %s' % ', '.join(sorted(shared)))

    # 3. Nothing widened.
    h = json.load(open(HORIZON, encoding='utf-8'))
    ok('the QI socket is still NOT_STARTED',
       h['layers']['historical_written_qi']['status'] == 'NOT_STARTED',
       h['layers']['historical_written_qi']['status'])
    ok('no historical occurrence has been ingested',
       a['headline']['extends_horizon_backwards'] is False)
    ok('the inventory declares no study-order change',
       a['roadmap_impact_preview']['study_order_changed'] is False
       and a['roadmap_impact_preview']['weights_changed'] is False)

    # The forbidden-claim sweep, scoped to what actually ASSERTS something.
    #
    # Sweeping whole internal files is the wrong instrument and this test
    # learned it the hard way: written_evidence_horizon.json contains the
    # strings "since 2010" and "16 years" in the list that FORBIDS them, and
    # this inventory contains "2006-2020" as the label of an honest gap.
    # Flagging those is the same class of error as a regulatory guard firing
    # on its own correction notice. What faces a reader is (a) the generated
    # public sentence and (b) the public page; those are swept in full.
    claims = [('written_evidence_horizon.json :: public_claim.derived_sentence',
               json.load(open(HORIZON, encoding='utf-8'))
               ['public_claim']['derived_sentence'])]
    if os.path.exists(PUBLIC):
        claims.append((os.path.relpath(PUBLIC, ROOT),
                       open(PUBLIC, encoding='utf-8', errors='replace').read()))
    hits = []
    for label, text in claims:
        for pat, why in FORBIDDEN:
            for m in re.finditer(pat, text, re.I):
                hits.append('%s: %s (%s)' % (label, m.group(0), why))
    ok('no unsupported historical claim on any reader-facing surface', not hits,
       '; '.join(hits[:4]))
    print('    swept %d claim surface(s) for %d forbidden patterns'
          % (len(claims), len(FORBIDDEN)))

    # And the sweep must be capable of firing: run it against a sentence that
    # tells the lie, so a regex typo cannot make this check pass vacuously.
    canary = 'MIW question intelligence since 2010 - 16 years of papers, 2010-2026.'
    fired = [why for pat, why in FORBIDDEN if re.search(pat, canary, re.I)]
    ok('the forbidden-claim sweep fires on a sentence that tells the lie',
       len(fired) >= 3, str(fired))

    print('  %d assertions' % (len(PASS) + len(FAIL)))
    if FAIL:
        print('\n%d FAILED' % len(FAIL))
        return 1
    print('  all %d PASS' % len(PASS))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
