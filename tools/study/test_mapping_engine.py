#!/usr/bin/env python3
"""Acceptance tests for the syllabus/topic mapping engine.

Covers the future-question contract (40M): a brand-new Oral question and a
brand-new Written question must flow

    new question -> canonical id -> mapper -> confidence -> review routing
                 -> governed record -> validator -> discoverable by topic

FIXTURES ARE SYNTHETIC AND IN-MEMORY.
A self-test that harvests live corpus state is a wasting asset -- it passes
until the corpus grows and then silently measures nothing. Every fixture here
is constructed in the test, and no test ever writes to
docs/study/study_mappings.json, so no fixture can leak into production data.

Usage:  python tools/study/test_mapping_engine.py
"""
import copy, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import mapping_engine as ME
import study_spine as SP

PASS, FAIL = [], []


def ok(name, cond, detail=''):
    (PASS if cond else FAIL).append(name if cond else f'{name}: {detail}')


# --------------------------------------------------------------------------- #
# Synthetic fixtures -- a pure file, a mixed file, and a spec question.
# --------------------------------------------------------------------------- #
PURE_FILE = 'QB4_A.html'          # registry says this is D03, one domain
MIXED_FILE = 'QB1_F.html'         # registry says mixed -> cue adjudication

NEW_ORAL_CLEAR = {'id': 'QB4_A#q999', 'anchor': 'q999', 'qnum': 999,
                  'text': 'What is the ISM Code requirement for a master review?'}
NEW_ORAL_CUED = {'id': 'QB1_F#q998', 'anchor': 'q998', 'qnum': 998,
                 'text': 'Explain the intermediate survey and what the class '
                         'surveyor examines.'}
NEW_ORAL_VAGUE = {'id': 'QB1_F#q997', 'anchor': 'q997', 'qnum': 997,
                  'text': 'Tell me about your last ship.'}
NEW_WRITTEN = {'q_no': 'Q9', 'short_title': 'Synthetic PSC question',
               'primary_category': 'Statutory Framework & Class',
               'subject_tags': ['Port State Control'], 'total_marks': 16,
               'subparts': []}
NEW_WRITTEN_BAD = {'q_no': 'Q8', 'short_title': 'Synthetic uncategorised',
                   'primary_category': 'Astro-Navigation & Sorcery',
                   'subject_tags': [], 'total_marks': 16, 'subparts': []}


def test_oral_high():
    m = ME.map_question(NEW_ORAL_CLEAR, 'ORAL', file_name=PURE_FILE)
    ok('oral/pure-file -> HIGH', m['mapping_confidence'] == 'HIGH',
       m['mapping_confidence'])
    ok('oral/pure-file -> VALID_MAPPED', m['mapping_status'] == 'VALID_MAPPED',
       m['mapping_status'])
    ok('oral/pure-file -> D03', m['topic_id'] == 'D03', str(m['topic_id']))
    ok('oral/record valid', ME.validate_mapping(m) == [], str(ME.validate_mapping(m)))
    ok('oral/carries canonical id',
       m['canonical_question_id'] == 'QB4_A#q999', m['canonical_question_id'])
    # 40B contract fields
    for f in ('content_type', 'syllabus_version', 'syllabus_node_id', 'topic_id',
              'subtopic_id', 'mapping_role', 'mapping_confidence',
              'mapping_basis', 'mapping_status', 'last_reviewed'):
        ok(f'oral/contract field {f}', f in m, 'absent')


def test_oral_medium_routes_to_review():
    m = ME.map_question(NEW_ORAL_CUED, 'ORAL', file_name=MIXED_FILE)
    ok('oral/mixed-file -> MEDIUM', m['mapping_confidence'] == 'MEDIUM',
       m['mapping_confidence'])
    ok('oral/MEDIUM never auto-published',
       m['mapping_status'] == 'REVIEW_PENDING', m['mapping_status'])
    ok('oral/mixed-file cue found D01', m['topic_id'] == 'D01', str(m['topic_id']))


def test_oral_unresolved():
    m = ME.map_question(NEW_ORAL_VAGUE, 'ORAL', file_name=MIXED_FILE)
    ok('oral/no-cue -> UNRESOLVED', m['mapping_confidence'] == 'UNRESOLVED',
       m['mapping_confidence'])
    ok('oral/no-cue -> ACCIDENTALLY_UNMAPPED',
       m['mapping_status'] == 'ACCIDENTALLY_UNMAPPED', m['mapping_status'])
    ok('oral/no-cue has no topic', m['topic_id'] is None, str(m['topic_id']))


def test_written():
    m = ME.map_question(NEW_WRITTEN, 'WRITTEN', paper_id='QP9901')
    ok('written -> HIGH', m['mapping_confidence'] == 'HIGH', m['mapping_confidence'])
    ok('written -> D01', m['topic_id'] == 'D01', str(m['topic_id']))
    ok('written canonical id', m['canonical_question_id'] == 'QP9901-Q9',
       m['canonical_question_id'])
    ok('written record valid', ME.validate_mapping(m) == [])
    bad = ME.map_question(NEW_WRITTEN_BAD, 'WRITTEN', paper_id='QP9901')
    ok('written/unknown category -> UNRESOLVED',
       bad['mapping_confidence'] == 'UNRESOLVED', bad['mapping_confidence'])


def test_validator_rejects_bad_records():
    good = ME.map_question(NEW_WRITTEN, 'WRITTEN', paper_id='QP9901')
    cases = [
        ('unknown topic id', {'topic_id': 'D99'}),
        ('bad confidence', {'mapping_confidence': 'VERY_SURE'}),
        ('bad status', {'mapping_status': 'PROBABLY'}),
        ('bad role', {'mapping_role': 'MAINISH'}),
        ('valid_mapped without topic', {'topic_id': None}),
        ('unearned official node', {'syllabus_node_id': 'MEO1-SYL-1.1'}),
        ('medium promoted without review',
         {'mapping_confidence': 'MEDIUM', 'mapping_status': 'VALID_MAPPED',
          'last_reviewed': None}),
    ]
    for name, patch in cases:
        r = {**good, **patch}
        ok(f'validator rejects: {name}', ME.validate_mapping(r) != [],
           'accepted an invalid record')


def test_incremental_adds_only_the_new():
    store = {'schema_version': ME.SCHEMA_VERSION,
             'taxonomy_version': ME.taxonomy_version(), 'mappings': {}}
    base = [(NEW_ORAL_CLEAR, 'ORAL', {'file_name': PURE_FILE}),
            (NEW_WRITTEN, 'WRITTEN', {'paper_id': 'QP9901'})]
    store, s1 = ME.incremental_update(store, base)
    ok('incremental/first run adds', s1['added'] == 2, str(s1))
    store, s2 = ME.incremental_update(store, base)
    ok('incremental/second run skips', s2 == {'added': 0, 'refreshed': 0,
                                              'skipped': 2, 'migrated': 0}, str(s2))
    extra = base + [(NEW_ORAL_CUED, 'ORAL', {'file_name': MIXED_FILE})]
    store, s3 = ME.incremental_update(store, extra)
    ok('incremental/one new question reprocesses nothing else',
       s3['added'] == 1 and s3['skipped'] == 2 and s3['refreshed'] == 0, str(s3))


def test_taxonomy_drift_is_visible():
    store = {'schema_version': ME.SCHEMA_VERSION,
             'taxonomy_version': ME.taxonomy_version(), 'mappings': {}}
    store, _ = ME.incremental_update(
        store, [(NEW_ORAL_CLEAR, 'ORAL', {'file_name': PURE_FILE})])
    ok('drift/clean store is UNCHANGED',
       len(ME.classify_against_taxonomy(store)['UNCHANGED']) == 1)
    # simulate a taxonomy edit by ageing the stamp
    aged = copy.deepcopy(store)
    for r in aged['mappings'].values():
        r['taxonomy_version'] = 'deadbeefdeadbeef'
    ok('drift/aged mapping is STALE',
       len(ME.classify_against_taxonomy(aged)['STALE']) == 1)
    orph = copy.deepcopy(store)
    for r in orph['mappings'].values():
        r['topic_id'] = 'D99'
    ok('drift/deleted node is ORPHANED_NODE',
       len(ME.classify_against_taxonomy(orph)['ORPHANED_NODE']) == 1)
    # and a re-derive after drift refreshes rather than duplicating
    refreshed, s = ME.incremental_update(
        aged, [(NEW_ORAL_CLEAR, 'ORAL', {'file_name': PURE_FILE})])
    ok('drift/stale mapping is refreshed', s['refreshed'] == 1, str(s))
    ok('drift/refresh does not duplicate', len(refreshed['mappings']) == 1)


def test_review_stamp_survives_rederivation():
    store = {'schema_version': ME.SCHEMA_VERSION,
             'taxonomy_version': ME.taxonomy_version(), 'mappings': {}}
    store, _ = ME.incremental_update(
        store, [(NEW_ORAL_CUED, 'ORAL', {'file_name': MIXED_FILE})])
    qid = NEW_ORAL_CUED['id']
    # a human adjudicates it
    store['mappings'][qid]['mapping_status'] = 'VALID_MAPPED'
    store['mappings'][qid]['last_reviewed'] = '2026-08-22'
    for r in store['mappings'].values():
        r['taxonomy_version'] = 'deadbeefdeadbeef'
    store, _ = ME.incremental_update(
        store, [(NEW_ORAL_CUED, 'ORAL', {'file_name': MIXED_FILE})])
    ok('review stamp survives re-derivation',
       store['mappings'][qid]['last_reviewed'] == '2026-08-22',
       str(store['mappings'][qid]['last_reviewed']))
    ok('adjudicated record stays VALID_MAPPED',
       store['mappings'][qid]['mapping_status'] == 'VALID_MAPPED')
    ok('adjudicated record passes the validator',
       ME.validate_mapping(store['mappings'][qid]) == [],
       str(ME.validate_mapping(store['mappings'][qid])))


def test_topic_side_discoverability():
    store = {'schema_version': ME.SCHEMA_VERSION,
             'taxonomy_version': ME.taxonomy_version(), 'mappings': {}}
    store, _ = ME.incremental_update(store, [
        (NEW_ORAL_CLEAR, 'ORAL', {'file_name': PURE_FILE}),
        (NEW_WRITTEN, 'WRITTEN', {'paper_id': 'QP9901'}),
        (NEW_ORAL_CUED, 'ORAL', {'file_name': MIXED_FILE}),
    ])
    ok('lookup: question -> topic',
       ME.get_question_topic('QB4_A#q999', store) == 'D03')
    ok('lookup: topic -> questions (D01 written)',
       ME.get_topic_questions('D01', store, content_type='WRITTEN') == ['QP9901-Q9'])
    ok('topic view excludes REVIEW_PENDING by default',
       ME.get_topic_questions('D01', store, content_type='ORAL') == [])
    ok('topic view can include REVIEW_PENDING on request',
       ME.get_topic_questions('D01', store, content_type='ORAL',
                              statuses=('VALID_MAPPED', 'REVIEW_PENDING'))
       == ['QB1_F#q998'])
    q = ME.review_queue(store)
    ok('review queue carries the pending item',
       [i['canonical_question_id'] for i in q] == ['QB1_F#q998'], str(q))
    ok('review queue offers a recommendation',
       q and q[0]['recommended_topic_id'] == 'D01')
    ok('review queue states the ambiguity reason', q and bool(q[0]['reason']))


def test_no_fixture_leak():
    """The production store must not contain any synthetic id."""
    p = os.path.join(ROOT, 'docs', 'study', 'study_mappings.json')
    if not os.path.exists(p):
        ok('no fixture leak', True)
        return
    live = json.load(open(p, encoding='utf-8'))['mappings']
    synth = [q for q in live if q.startswith('QP9901')
             or q.endswith(('#q999', '#q998', '#q997'))]
    ok('no fixture leak into production store', not synth, str(synth))


def main():
    for fn in (test_oral_high, test_oral_medium_routes_to_review,
               test_oral_unresolved, test_written,
               test_validator_rejects_bad_records,
               test_incremental_adds_only_the_new,
               test_taxonomy_drift_is_visible,
               test_review_stamp_survives_rederivation,
               test_topic_side_discoverability, test_no_fixture_leak):
        fn()
    print(f'mapping engine acceptance -- {len(PASS) + len(FAIL)} assertions')
    for f in FAIL:
        print('  FAIL ' + f)
    if FAIL:
        print(f'\n{len(FAIL)} FAILED')
        return 1
    print(f'  all {len(PASS)} PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
