#!/usr/bin/env python3
"""Build the granularity-aware per-node syllabus gap register and its queue.

    official_syllabus.json (25 nodes)  --.
    official_crosswalk.json (43 edges) --+
    study_mappings.json (1,098 records) --+--> syllabus_gap_register.json
    current-answers specs (8)          --+          |
    ORAL_NOTES_UNITS.jsonl (992)       --+          v
    qi/qi_families.json (270)          --'   gap_production_queue.json

WHY THIS FILE EXISTS
--------------------
`coverage_matrix.json` is a term-probe diagnostic and says so. The mapping
store is a question->topic->node join. Neither answers the question production
actually needs: for each of the 25 Annexure III nodes, what governed evidence
exists, and at what granularity was it actually observed?

THE ONE RULE EVERYTHING HERE OBEYS
----------------------------------
Evidence is counted at the granularity it was observed at, never promoted.

  * A record that pinpoints ONE official node raises that node's `resolved`
    tally.
  * A record aligned to a candidate SET raises the `topic_level` tally of every
    node in the set and the `resolved` tally of none of them. It stays attached
    to the set.
  * A record with no governed official node raises the `ambiguous` tally only
    of nodes it names as a cue-derived hypothesis, and is additionally listed
    in the unattributed pool so nothing is dropped.

Promoting topic-level evidence is what made nodes 02, 08, 13, 14, 15, 16 and 17
each report one topic's entire question count as if it were their own.
`tools/study/test_syllabus_fanout.py` is the regression that holds this.

CLASSIFICATION IS NOT RECURRENCE
--------------------------------
This builder READS the answer, Notes and QI stores and writes to neither. No
question, family, limb, occurrence or recurrence tally is created, altered or
deleted here. The official classification is a separate quantity and lives only
in the register.

Determinism: every collection is sorted, no clock is read, and the queue is
derived from the register file on disk and from nothing else, so two runs over
unchanged inputs are byte-identical.

Usage:
    python tools/study/build_syllabus_gap_register.py
"""
import collections, glob, hashlib, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
# The Notes layer owns its own path resolution. tools/notes/miw_paths.py exists
# precisely so no tool spells a Notes path against a root it guessed for itself,
# so the Notes input below is resolved from miw_paths.REPO_ROOT and this module's
# own ROOT is asserted equal to it rather than trusted.
sys.path.insert(0, os.path.join(ROOT, 'tools', 'notes'))

import mapping_engine as ME
import miw_paths as MP

assert os.path.normcase(os.path.abspath(MP.REPO_ROOT)) == \
       os.path.normcase(os.path.abspath(ROOT)), (
    'root disagreement: build_syllabus_gap_register ROOT=%s but '
    'miw_paths.REPO_ROOT=%s' % (ROOT, MP.REPO_ROOT))

OFFICIAL = os.path.join(ROOT, 'docs', 'study', 'official_syllabus.json')
STORE    = os.path.join(ROOT, 'docs', 'study', 'study_mappings.json')
CA_SPECS = os.path.join(ROOT, 'meoclass1', 'current-answers', 'specs', '*.json')
CA_REG   = os.path.join(ROOT, 'meoclass1', 'current-answers', 'registry.json')
NOTES    = os.path.join(MP.REPO_ROOT, 'meoclass1', 'oral-intelligence',
                        'examiner-audit', 'ORAL_NOTES_UNITS.jsonl')
QI_FAM   = os.path.join(ROOT, 'docs', 'study', 'qi', 'qi_families.json')
QI_OCC   = os.path.join(ROOT, 'docs', 'study', 'qi', 'qi_occurrences.json')

REGISTER = os.path.join(ROOT, 'docs', 'study', 'syllabus_gap_register.json')
QUEUE    = os.path.join(ROOT, 'docs', 'study', 'gap_production_queue.json')

FINAL_DIGEST = ('07170f572c99064fad25eedb0fe985886248a81a49b4eb5d4711fd38d1'
                '86f44d')

COVERAGE_STATES = (
    'NODE_EVIDENCED_GOVERNED_ANSWER',
    'NODE_EVIDENCED_NO_GOVERNED_ANSWER',
    'GOVERNED_ANSWER_WITHOUT_NODE_EVIDENCE',
    'TOPIC_LEVEL_EVIDENCE_ONLY',
    'HYPOTHESIS_EVIDENCE_ONLY',
    'NO_EVIDENCE',
)
MAPPING_STATES = ('RESOLVED_MAPPING', 'AMBIGUOUS_MAPPING', 'NO_MAPPING')
STREAMS = ('oral', 'written', 'current_answers', 'notes', 'written_qi_families')


def jload(path):
    return json.load(open(path, encoding='utf-8'))


def write_json(path, payload):
    """Serialise, write, then MEASURE the exact bytes that landed.

    The determinism claim in this module's docstring is only worth what it can
    be shown to be worth. So every write reports the byte length and SHA-256 of
    what was on disk before it and of what is on disk after it, and states
    whether the two are byte-identical. Two consecutive runs over unchanged
    inputs must report `byte_identical_with_prior_run: true` on the second run;
    a semantic or stdout comparison is not accepted as a substitute for it.
    """
    body = json.dumps(payload, indent=2, ensure_ascii=False) + '\n'
    prior = None
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            prior = fh.read()
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(body)
    with open(path, 'rb') as fh:
        landed = fh.read()
    print('  byte-identity: ' + json.dumps({
        'path': os.path.relpath(path, ROOT).replace(os.sep, '/'),
        'prior_bytes': None if prior is None else len(prior),
        'prior_sha256': (None if prior is None
                         else hashlib.sha256(prior).hexdigest()),
        'written_bytes': len(landed),
        'written_sha256': hashlib.sha256(landed).hexdigest(),
        'byte_identical_with_prior_run': prior is not None and prior == landed,
    }))
    return body


# --------------------------------------------------------------------------- #
# Hypotheses -- the weakest tier, kept visibly apart from the governed set
# --------------------------------------------------------------------------- #
def hypothesis_nodes_for(rec):
    """Cue-derived candidate official nodes for a record with no governed one.

    A question that carries no MIW topic still gives a reviewer something to
    look at: the domains whose cues fire on its own text. Those are HYPOTHESES.
    They never enter `resolved` or `topic_level`, and they are stored in their
    own field so they can never be read as a governed candidate set.
    """
    if rec.get('official_syllabus_node_id') is not None:
        return []
    if rec.get('official_syllabus_node_candidates'):
        return []
    nodes = set()
    for topic in ME._candidates(rec):
        nodes.update(ME.official_nodes_for_topic(topic))
        nodes.update(ME.official_nodes_for_topic(topic, 'SUPPORTING'))
    return sorted(nodes)


def contribution_from_topic(source_id, content_type, topic_id):
    """Classify a non-question asset (an answer, a family) through the SAME
    crosswalk the questions use, by building a record and running the engine's
    own `attach_official` over it. No second resolution rule is defined here.
    """
    rec = {'canonical_question_id': source_id, 'content_type': content_type,
           'topic_id': topic_id, 'mapping_status': 'CLASSIFICATION_ONLY'}
    ME.attach_official(rec)
    return ME.coverage_contribution(rec)


# --------------------------------------------------------------------------- #
# Stream builders
# --------------------------------------------------------------------------- #
def question_contributions(store, content_type):
    out = []
    for qid in sorted(store):
        rec = store[qid]
        if rec.get('content_type') != content_type:
            continue
        out.append(ME.coverage_contribution(
            rec, hypothesis_nodes=hypothesis_nodes_for(rec)))
    return out


def _entity_topics(member_entities, store):
    """Family members -> the governed topics of the questions behind them.

    Only members that ARE governed questions in the mapping store can speak.
    A historical archive entity that never entered the store is silent here --
    it is not evidence of a topic, and inventing one would be the
    nearest-neighbour mistake the engine exists to avoid.
    """
    topics = set()
    seen = 0
    for m in member_entities or []:
        if not m.startswith('QIE-M-'):
            continue
        qid = m[len('QIE-M-'):]
        rec = store.get(qid)
        if rec and rec.get('topic_id'):
            topics.add(rec['topic_id'])
            seen += 1
    return sorted(topics), seen


def _classify_via_families(asset_id, content_type, family_ids, families, store):
    """One asset -> one contribution, through its QI families' governed members."""
    topics, members_seen = set(), 0
    for fid in family_ids or []:
        fam = families.get(fid)
        if not fam:
            continue
        t, n = _entity_topics(fam.get('member_entities'), store)
        topics.update(t)
        members_seen += n
    topics = sorted(topics)
    if len(topics) == 1:
        c = contribution_from_topic(asset_id, content_type, topics[0])
    else:
        # No single governed topic: either nothing governed spoke, or the
        # family's governed members disagree. Either way this is AMBIGUOUS and
        # every node any of those topics reaches is a hypothesis only.
        nodes = set()
        for t in topics:
            nodes.update(ME.official_nodes_for_topic(t))
            nodes.update(ME.official_nodes_for_topic(t, 'SUPPORTING'))
        c = {
            'canonical_question_id': asset_id,
            'content_type': content_type,
            'topic_id': None,
            'evidence_granularity': 'AMBIGUOUS',
            'evidence_granularity_basis': ME.GRANULARITY_BASIS['AMBIGUOUS'],
            'resolved_official_node_id': None,
            'candidate_official_node_ids': [],
            'hypothesis_official_node_ids': sorted(nodes),
            'official_mapping_confidence': 'UNRESOLVED',
            'official_alignment_status': 'UNRESOLVED',
            'mapping_status': 'CLASSIFICATION_ONLY',
            'review_required': True,
        }
    c['source_topic_ids'] = topics
    c['governed_members_read'] = members_seen
    c['family_ids'] = sorted(family_ids or [])
    return c


def current_answer_contributions(families, store):
    out = []
    for path in sorted(glob.glob(CA_SPECS)):
        spec = jload(path)
        cid = spec['current_answer_id']
        topic = spec.get('topic_id')
        if topic:
            c = contribution_from_topic(cid, 'CURRENT_ANSWER', topic)
            c['source_topic_ids'] = [topic]
            c['governed_members_read'] = 0
            c['family_ids'] = sorted(spec.get('family_ids') or [])
        else:
            c = _classify_via_families(cid, 'CURRENT_ANSWER',
                                       spec.get('family_ids'), families, store)
        c['title'] = spec.get('title')
        c['scope'] = spec.get('scope')
        c['answer_version'] = spec.get('answer_version')
        c['review_status'] = spec.get('review_status')
        c['candidate_visibility'] = spec.get('candidate_visibility')
        out.append(c)
    return out


def notes_contributions():
    """Every ORAL_NOTES_UNITS unit, read and never rewritten.

    A Notes unit carries no governed topic id and no governed link to a
    canonical question. The only signals it holds -- keywords, reg_codes and
    its own prose -- are exactly the text-similarity signals this project
    refuses to map from. So every unit is honestly AMBIGUOUS with an empty
    candidate set, and the whole layer is reported as awaiting the Notes-to-
    topic adjudication rather than quietly given nodes it has not earned.
    """
    out = []
    for line in open(NOTES, encoding='utf-8'):
        line = line.strip()
        if not line:
            continue
        u = json.loads(line)
        out.append({
            'canonical_question_id': u['note_unit_id'],
            'content_type': 'NOTES_UNIT',
            'topic_id': None,
            'evidence_granularity': 'AMBIGUOUS',
            'evidence_granularity_basis': ME.GRANULARITY_BASIS['AMBIGUOUS'],
            'resolved_official_node_id': None,
            'candidate_official_node_ids': [],
            'hypothesis_official_node_ids': [],
            'official_mapping_confidence': 'UNRESOLVED',
            'official_alignment_status': 'UNRESOLVED',
            'mapping_status': 'CLASSIFICATION_ONLY',
            'review_required': True,
            'series': u.get('series'),
            'source_file': u.get('file'),
        })
    return sorted(out, key=lambda c: c['canonical_question_id'])


def qi_family_contributions(families, store):
    out = []
    for fid in sorted(families):
        fam = families[fid]
        c = _classify_via_families(fid, 'WRITTEN_QI_FAMILY', [fid], families,
                                   store)
        c['label'] = fam.get('label')
        c['member_entity_count'] = len(fam.get('member_entities') or [])
        c['occurrence_count'] = len(fam.get('occurrence_ids') or [])
        out.append(c)
    return out


# --------------------------------------------------------------------------- #
# States -- computed from the tallies, never asserted
# --------------------------------------------------------------------------- #
def coverage_state(t):
    q_res = t['oral']['resolved'] + t['written']['resolved']
    a_res = t['current_answers']['resolved']
    topic = sum(t[s]['topic_level'] for s in STREAMS)
    amb = sum(t[s]['ambiguous'] for s in STREAMS)
    if q_res and a_res:
        return 'NODE_EVIDENCED_GOVERNED_ANSWER'
    if q_res:
        return 'NODE_EVIDENCED_NO_GOVERNED_ANSWER'
    if a_res:
        return 'GOVERNED_ANSWER_WITHOUT_NODE_EVIDENCE'
    if topic:
        return 'TOPIC_LEVEL_EVIDENCE_ONLY'
    if amb:
        return 'HYPOTHESIS_EVIDENCE_ONLY'
    return 'NO_EVIDENCE'


def mapping_state(t):
    if any(t[s]['resolved'] for s in STREAMS):
        return 'RESOLVED_MAPPING'
    if any(t[s]['topic_level'] or t[s]['ambiguous'] for s in STREAMS):
        return 'AMBIGUOUS_MAPPING'
    return 'NO_MAPPING'


def node_granularity(t):
    if any(t[s]['resolved'] for s in STREAMS):
        return 'NODE_LEVEL'
    if any(t[s]['topic_level'] for s in STREAMS):
        return 'TOPIC_LEVEL'
    return 'AMBIGUOUS'


# --------------------------------------------------------------------------- #
# Register
# --------------------------------------------------------------------------- #
def build_register():
    official = jload(OFFICIAL)
    nodes = official['nodes']
    node_ids = [n['official_node_id'] for n in nodes]
    store = jload(STORE)['mappings']
    families = {f['family_id']: f for f in jload(QI_FAM)['families']}
    xwalk = ME.official_crosswalk()

    streams = {
        'oral': question_contributions(store, 'ORAL'),
        'written': question_contributions(store, 'WRITTEN'),
        'current_answers': current_answer_contributions(families, store),
        'notes': notes_contributions(),
        'written_qi_families': qi_family_contributions(families, store),
    }
    tallies = {k: ME.tally_contributions(v, node_ids)
               for k, v in streams.items()}

    edges_by_node = collections.defaultdict(list)
    for e in xwalk['edges']:
        edges_by_node[e['official_node_id']].append({
            'topic_id': e['topic_id'],
            'topic_name': e.get('topic_name'),
            'mapping_role': e['mapping_role'],
            'mapping_confidence': e.get('mapping_confidence'),
        })

    records = []
    for node in sorted(nodes, key=lambda n: n['official_node_id']):
        nid = node['official_node_id']
        t = {s: tallies[s]['by_node'][nid] for s in STREAMS}
        state = coverage_state(t)
        mstate = mapping_state(t)
        gran = node_granularity(t)
        edges = sorted(edges_by_node.get(nid, []),
                       key=lambda e: (e['mapping_role'], e['topic_id']))
        records.append({
            'official_node_id': nid,
            'official_number': node['official_number'],
            'official_label': ' '.join(
                node['official_text'].split())[:160].rstrip() + '...',
            'official_source_page': node.get('source_page'),
            'miw_topic_edges': edges,
            'tallies': t,
            'coverage_state': state,
            'mapping_state': mstate,
            'evidence_granularity': gran,
            'review_required': gran != 'NODE_LEVEL',
            'provenance': {
                'official_source_sha256': FINAL_DIGEST,
                'official_syllabus_version': ME.OFFICIAL_VERSION,
                'crosswalk': 'docs/study/official_crosswalk.json',
                'mapping_store': 'docs/study/study_mappings.json',
                'current_answer_specs': 'meoclass1/current-answers/specs/*.json',
                'notes_units': ('meoclass1/oral-intelligence/examiner-audit/'
                                'ORAL_NOTES_UNITS.jsonl'),
                'qi_families': 'docs/study/qi/qi_families.json',
                'derived_by': 'tools/study/build_syllabus_gap_register.py',
                'evidence_granularity_basis': ME.GRANULARITY_BASIS[gran],
            },
        })

    # ---- the unresolved backlog, carried in full and never counted as cover
    unresolved = []
    for qid in sorted(store):
        r = store[qid]
        if r.get('mapping_status') != 'ACCIDENTALLY_UNMAPPED':
            continue
        unresolved.append({
            'canonical_question_id': qid,
            'content_type': r.get('content_type'),
            'topic_id': r.get('topic_id'),
            'source_file': r.get('source_file') or r.get('paper_id'),
            'mapping_state': 'AMBIGUOUS_MAPPING',
            'evidence_granularity': r.get('evidence_granularity'),
            'candidate_official_node_ids':
                list(r.get('official_syllabus_node_candidates') or []),
            'hypothesis_official_node_ids': hypothesis_nodes_for(r),
            'why_not_deterministic': r.get('official_mapping_basis'),
            'mapping_evidence': r.get('mapping_evidence'),
            'mapping_basis': r.get('mapping_basis'),
            'review_required': True,
        })

    # ---- domains with no Annexure III edge of any role ----------------------
    homeless = sorted(
        d for d in {e['topic_id'] for e in xwalk['edges']}
        | {dd['domain_id'] for dd in __import__('study_spine').DOMAINS}
        if not ME.official_nodes_for_topic(d)
        and not ME.official_nodes_for_topic(d, 'SUPPORTING'))

    counts_by_state = collections.Counter(r['coverage_state'] for r in records)
    counts_by_mapping = collections.Counter(r['mapping_state'] for r in records)

    return {
        'schema': 'miw.study.syllabus_gap_register.v1',
        'schema_version': '1.0',
        'generated_by': 'tools/study/build_syllabus_gap_register.py',
        'hand_editable': False,
        'authority': (
            'AUTHORITATIVE granularity-aware per-node coverage view for the '
            'final DGMA Circular 49 of 2026 Annexure III syllabus. Every '
            'contribution is counted at the granularity it was observed at. '
            'Node-level tallies count only evidence that pinpointed exactly '
            'one official node. Topic-level evidence stays attached to its '
            'candidate set and never raises a node-level tally. '
            'docs/study/coverage_matrix.json remains DIAGNOSTIC ONLY and is '
            'not promoted by this file.'),
        'classification_is_not_recurrence': (
            'This file records official syllabus CLASSIFICATION. It creates no '
            'question and no family, and it alters no recurrence count, family '
            'identity, limb record, occurrence record or examiner attribution. '
            'The answer, Notes and QI stores are read-only inputs here.'),
        'official_source': {
            'circular': official['source']['circular'],
            'annex': official['annex']['annex_id'],
            'sha256': FINAL_DIGEST,
            'syllabus_version': ME.OFFICIAL_VERSION,
            'status': ME.OFFICIAL_STATUS,
            'effective_from': ME.OFFICIAL_EFFECTIVE_FROM,
        },
        'evidence_granularity_model': {
            'values': list(ME.EVIDENCE_GRANULARITY),
            'basis': ME.GRANULARITY_BASIS,
            'regression': 'tools/study/test_syllabus_fanout.py',
        },
        'inputs': {
            'oral_questions': len(streams['oral']),
            'written_questions': len(streams['written']),
            'current_answer_specs': len(streams['current_answers']),
            'notes_units': len(streams['notes']),
            'written_qi_families': len(streams['written_qi_families']),
            'crosswalk_edges': len(xwalk['edges']),
            'official_nodes': len(records),
        },
        'totals': {s: tallies[s]['totals'] for s in STREAMS},
        'unattributed_evidence': {
            'what': ('Contributions whose granularity is AMBIGUOUS and which '
                     'name no hypothesis node. They are counted here so the '
                     'per-node view can never be mistaken for the whole '
                     'corpus.'),
            **{s: len(tallies[s]['unattributed_ids']) for s in STREAMS},
        },
        'counts_by_coverage_state': {k: counts_by_state.get(k, 0)
                                     for k in COVERAGE_STATES},
        'counts_by_mapping_state': {k: counts_by_mapping.get(k, 0)
                                    for k in MAPPING_STATES},
        'accidentally_unmapped': {
            'what': ('Questions with no MIW topic at all. They remain visible '
                     'and unresolved, are never counted as resolved coverage, '
                     'and require adjudication, not derivation.'),
            'count': len(unresolved),
            'questions': unresolved,
        },
        'domains_without_official_home': {
            'what': ('MIW domains carrying no Annexure III edge of any role. '
                     'Why a domain has no official home is an ADJUDICATION '
                     'and is not settled here. See '
                     'docs/study/SYLLABUS_SOURCE_STATUS.md section 9.'),
            'domain_ids': homeless,
            'mapping_state': 'AMBIGUOUS_MAPPING',
            'review_required': True,
        },
        'current_answer_classifications': streams['current_answers'],
        'nodes': records,
    }


# --------------------------------------------------------------------------- #
# Queue -- derived from the register FILE and from nothing else
# --------------------------------------------------------------------------- #
QUEUE_RULES = {
    'REVIEW': ('mapping_state == AMBIGUOUS_MAPPING. The node has evidence, but '
               'none of it pinpoints the node, so no production priority can '
               'be derived from it honestly. Adjudication first.'),
    'P0': ('mapping_state != AMBIGUOUS_MAPPING and coverage_state == '
           'NO_EVIDENCE. The governed corpus is not yet useful to a candidate '
           'for this official node at all.'),
    'P1': ('coverage_state == NODE_EVIDENCED_NO_GOVERNED_ANSWER. There is '
           'node-level question evidence and no adequate governed answer.'),
    'P2': ('coverage_state == GOVERNED_ANSWER_WITHOUT_NODE_EVIDENCE, or a '
           'governed answer exists alongside topic-level or hypothesis-only '
           'evidence. The coverage is legacy or misaligned with the final '
           'syllabus.'),
    'P3': ('node-level question evidence and a governed answer, with no '
           'unaligned residue. Coverage strengthening.'),
}


def lane_for(rec):
    if rec['mapping_state'] == 'AMBIGUOUS_MAPPING':
        return 'REVIEW'
    state = rec['coverage_state']
    t = rec['tallies']
    if state == 'NO_EVIDENCE':
        return 'P0'
    if state == 'NODE_EVIDENCED_NO_GOVERNED_ANSWER':
        return 'P1'
    if state == 'GOVERNED_ANSWER_WITHOUT_NODE_EVIDENCE':
        return 'P2'
    residue = sum(t[s]['topic_level'] + t[s]['ambiguous'] for s in STREAMS)
    return 'P2' if residue else 'P3'


def build_queue(register):
    lanes = collections.OrderedDict(
        (k, []) for k in ('P0', 'P1', 'P2', 'P3', 'REVIEW'))
    for rec in sorted(register['nodes'], key=lambda r: r['official_node_id']):
        lane = lane_for(rec)
        lanes[lane].append({
            'official_node_id': rec['official_node_id'],
            'official_number': rec['official_number'],
            'official_label': rec['official_label'],
            'coverage_state': rec['coverage_state'],
            'mapping_state': rec['mapping_state'],
            'evidence_granularity': rec['evidence_granularity'],
            'review_required': rec['review_required'],
            'tallies': rec['tallies'],
            'lane': lane,
            'rule': QUEUE_RULES[lane],
        })
    return {
        'schema': 'miw.study.gap_production_queue.v1',
        'schema_version': '1.0',
        'generated_by': 'tools/study/build_syllabus_gap_register.py',
        'hand_editable': False,
        'authority': (
            'Derived from docs/study/syllabus_gap_register.json and from '
            'nothing else. No priority in this file is hand-asserted. A node '
            'whose mapping state is AMBIGUOUS_MAPPING is in the review lane '
            'and in no production lane, because a priority derived from '
            'topic-smeared evidence would be a fabricated priority.'),
        'derived_from': {
            'register': 'docs/study/syllabus_gap_register.json',
            'register_schema': register['schema'],
            'official_source_sha256': register['official_source']['sha256'],
        },
        'rules': QUEUE_RULES,
        'counts': {k: len(v) for k, v in lanes.items()},
        'lanes': dict(lanes),
    }


def main():
    print('resolved roots:')
    print('  build_syllabus_gap_register.ROOT = ' + ROOT)
    print('  miw_paths.REPO_ROOT              = ' + MP.REPO_ROOT)
    print('  notes input (via REPO_ROOT)      = ' + NOTES)
    register = build_register()
    write_json(REGISTER, register)
    print(f'wrote docs/study/syllabus_gap_register.json '
          f"({len(register['nodes'])} official nodes)")
    print('  inputs: ' + json.dumps(register['inputs']))
    print('  totals: ' + json.dumps(register['totals']))
    for r in register['nodes']:
        t = r['tallies']
        print(f"  {r['official_node_id']} {r['evidence_granularity']:11s} "
              f"oral={t['oral']['resolved']:3d}/{t['oral']['topic_level']:3d}/"
              f"{t['oral']['ambiguous']:3d} "
              f"wr={t['written']['resolved']:3d}/{t['written']['topic_level']:3d}/"
              f"{t['written']['ambiguous']:3d} "
              f"ca={t['current_answers']['resolved']}/"
              f"{t['current_answers']['topic_level']}/"
              f"{t['current_answers']['ambiguous']} "
              f"notes={t['notes']['resolved']}/{t['notes']['topic_level']}/"
              f"{t['notes']['ambiguous']} "
              f"-> {r['coverage_state']}")

    # The queue reads the register back off disk. It must not be able to see
    # anything the register did not publish.
    queue = build_queue(jload(REGISTER))
    write_json(QUEUE, queue)
    print('wrote docs/study/gap_production_queue.json')
    print('  counts: ' + json.dumps(queue['counts']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
