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


# --------------------------------------------------------------------------- #
# Official syllabus join -- DGMA Circular 49 of 2026, Annexure III
# --------------------------------------------------------------------------- #
def test_future_oral_reaches_the_official_syllabus():
    """One brand-new oral question, all the way to Annexure III."""
    m = ME.map_question(NEW_ORAL_CLEAR, 'ORAL', file_name=PURE_FILE)
    ok('future oral: topic decided', m['topic_id'] == 'D03', m['topic_id'])
    ok('future oral: official version stamped',
       m['official_syllabus_version'] == ME.OFFICIAL_VERSION)
    ok('future oral: crosswalk aligned',
       m['official_alignment_status'] == 'CROSSWALK_ALIGNED',
       m['official_alignment_status'])
    ok('future oral: official candidates present',
       len(m['official_syllabus_node_candidates']) > 0)
    ok('future oral: candidates are real Annexure III nodes',
       all(c.startswith('C49-A3-') for c in m['official_syllabus_node_candidates']))
    ok('future oral: not falsely pinpointed',
       m['official_syllabus_node_id'] is None
       or len(m['official_syllabus_node_candidates']) == 1)
    ok('future oral: record is valid', ME.validate_mapping(m) == [],
       str(ME.validate_mapping(m)))


def test_future_written_reaches_the_official_syllabus():
    m = ME.map_question(NEW_WRITTEN, 'WRITTEN', paper_id='QP9901')
    ok('future written: topic decided', m['topic_id'] == 'D01', m['topic_id'])
    ok('future written: crosswalk aligned',
       m['official_alignment_status'] == 'CROSSWALK_ALIGNED')
    ok('future written: D01 owns several official nodes, so the set is used',
       m['official_syllabus_node_id'] is None
       and len(m['official_syllabus_node_candidates']) > 1,
       str(m['official_syllabus_node_candidates']))
    ok('future written: confidence band reports precision',
       m['official_mapping_confidence'] == 'MEDIUM')
    ok('future written: record is valid', ME.validate_mapping(m) == [])


def test_official_reverse_lookup():
    """Official node -> topic -> questions, the direction a study pack needs."""
    nodes = ME.official_nodes_for_topic('D01')
    ok('reverse: D01 owns Annexure III nodes', len(nodes) >= 1, str(nodes))
    ok('reverse: node 3 (classification) belongs to D01',
       'C49-A3-03' in nodes, str(nodes))
    store = {'schema_version': ME.SCHEMA_VERSION,
             'taxonomy_version': ME.taxonomy_version(), 'mappings': {}}
    ME.incremental_update(store, [(NEW_WRITTEN, 'WRITTEN', {'paper_id': 'QP9901'})])
    found = ME.get_topic_questions('D01', store)
    ok('reverse: topic lookup finds the new question', len(found) == 1, str(found))


def test_supporting_only_is_not_orphaned():
    """D08 has an official home; D07 has none. They must not read alike."""
    d08 = ME.attach_official({'topic_id': 'D08'})
    d07 = ME.attach_official({'topic_id': 'D07'})
    ok('D08 is SUPPORTING_ONLY, not orphaned',
       d08['official_alignment_status'] == 'SUPPORTING_ONLY',
       d08['official_alignment_status'])
    ok('D08 still has an official candidate',
       d08['official_syllabus_node_candidates'] == ['C49-A3-12'],
       str(d08['official_syllabus_node_candidates']))
    ok('D07 is genuinely orphaned in Annexure III',
       d07['official_alignment_status'] == 'ORPHANED_IN_ADOPTED_SYLLABUS',
       d07['official_alignment_status'])
    ok('D07 has no official candidates',
       d07['official_syllabus_node_candidates'] == [])


def test_official_pinpoint_must_be_earned():
    """A single official node may only be claimed when the set singles it out."""
    m = ME.map_question(NEW_WRITTEN, 'WRITTEN', paper_id='QP9901')
    bad = copy.deepcopy(m)
    bad['official_syllabus_node_id'] = bad['official_syllabus_node_candidates'][0]
    ok('validator rejects: pinpoint from an ambiguous candidate set',
       ME.validate_mapping(bad) != [], 'accepted an unearned pinpoint')
    bogus = copy.deepcopy(m)
    bogus['official_syllabus_node_candidates'] = ['C49-A3-99']
    ok('validator rejects: unknown official node',
       ME.validate_mapping(bogus) != [], 'accepted a node not in the crosswalk')
    lying = copy.deepcopy(m)
    lying['official_alignment_status'] = 'ORPHANED_IN_ADOPTED_SYLLABUS'
    ok('validator rejects: orphan claim with candidates present',
       ME.validate_mapping(lying) != [], 'accepted a contradictory orphan claim')


def test_two_syllabus_versions_stay_separate():
    """Adopted is not in force. The 01-Jan-2027 migration depends on this."""
    m = ME.map_question(NEW_ORAL_CLEAR, 'ORAL', file_name=PURE_FILE)
    ok('operative version is the MIW-derived one',
       m['syllabus_version'] == ME.SYLLABUS_VERSION, m['syllabus_version'])
    ok('adopted version is recorded separately',
       m['official_syllabus_version'] == ME.OFFICIAL_VERSION)
    ok('the two versions are not the same value',
       m['syllabus_version'] != m['official_syllabus_version'])
    ok('adopted syllabus carries its own effective date',
       m['official_effective_from'] == '2027-01-01', m['official_effective_from'])
    ok('operative version defines no syllabus node ids',
       m['syllabus_node_id'] is None)
    fabricated = copy.deepcopy(m)
    fabricated['syllabus_node_id'] = 'C49-A3-03'
    ok('validator rejects: official node smuggled into the operative version',
       ME.validate_mapping(fabricated) != [],
       'accepted an adopted-syllabus node as an operative one')


def test_final_source_guard():
    """The system may not silently revert to the July draft."""
    sys.path.insert(0, HERE)
    import official_syllabus as OS_
    ok('guard: final digest recognised',
       OS_.classify_digest(OS_.SOURCE_SHA256) == 'FINAL')
    ok('guard: the draft is named, not merely rejected',
       OS_.classify_digest(OS_.DRAFT_SHA256) == 'SUPERSEDED_DRAFT')
    ok('guard: anything else is unknown',
       OS_.classify_digest('0' * 64) == 'UNKNOWN')
    ok('guard: final and draft digests actually differ',
       OS_.SOURCE_SHA256 != OS_.DRAFT_SHA256)
    ok('guard: the draft carries fewer nodes than the final',
       OS_.DRAFT_NODES < OS_.EXPECTED_NODES)
    published = json.load(open(os.path.join(
        ROOT, 'docs', 'study', 'official_syllabus.json'), encoding='utf-8'))
    ok('guard: the committed extraction is pinned to the final circular',
       published['source']['sha256'] == OS_.SOURCE_SHA256)
    ok('guard: the committed extraction has all 25 official nodes',
       len(published['nodes']) == OS_.EXPECTED_NODES, str(len(published['nodes'])))
    ok('guard: every official node carries the source digest',
       all(n['source_digest'] == OS_.SOURCE_SHA256 for n in published['nodes']))
    ok('guard: the crosswalk is pinned to the same bytes',
       ME.official_crosswalk()['official_source']['sha256'] == OS_.SOURCE_SHA256)


def test_official_join_is_incremental():
    """One new question must not re-derive the official layer for the corpus."""
    store = {'schema_version': ME.SCHEMA_VERSION,
             'taxonomy_version': ME.taxonomy_version(), 'mappings': {}}
    ME.incremental_update(store, [(NEW_ORAL_CLEAR, 'ORAL', {'file_name': PURE_FILE})])
    first = copy.deepcopy(store['mappings'])
    ME.incremental_update(store, [(NEW_WRITTEN, 'WRITTEN', {'paper_id': 'QP9901'})])
    ok('incremental: the existing record was not rewritten',
       store['mappings'][NEW_ORAL_CLEAR['id']] == first[NEW_ORAL_CLEAR['id']])
    ok('incremental: only the new question was added',
       len(store['mappings']) == 2, str(len(store['mappings'])))


def main():
    for fn in (test_oral_high, test_oral_medium_routes_to_review,
               test_oral_unresolved, test_written,
               test_validator_rejects_bad_records,
               test_incremental_adds_only_the_new,
               test_taxonomy_drift_is_visible,
               test_review_stamp_survives_rederivation,
               test_topic_side_discoverability,
               test_future_oral_reaches_the_official_syllabus,
               test_future_written_reaches_the_official_syllabus,
               test_official_reverse_lookup,
               test_supporting_only_is_not_orphaned,
               test_official_pinpoint_must_be_earned,
               test_two_syllabus_versions_stay_separate,
               test_final_source_guard,
               test_official_join_is_incremental,
               test_no_fixture_leak):
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
