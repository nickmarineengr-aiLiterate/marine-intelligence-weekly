#!/usr/bin/env python3
"""The shared syllabus/topic mapping engine.

    ORAL ADAPTER   --.
                      >--  COMMON MAPPER  -->  GOVERNED MAPPING RECORD
    WRITTEN ADAPTER -'

ONE algorithm, two input adapters. Oral and Written differ only in what
evidence they can offer the mapper, not in how a topic is decided, so there is
no second Written-only taxonomy and no second Oral-only taxonomy here.

Every consumer -- Oral QB production, Written QP production, bulk backfill,
the validator and study-pack generation -- must call THIS module rather than
parsing mapping JSON itself. See tools/study/SKILL.md for the integration
contract.

WHY MAPPINGS ARE NOT NEAREST-NEIGHBOUR
--------------------------------------
The oral follow-up project proved that similarity/coverage scoring picks
semantically wrong parents (see docs the register cites). So this engine never
copies the mapping of a "similar" question. It decides from STRUCTURAL
evidence only:

  * WRITTEN -- the spec's governed `primary_category` field. Deterministic,
    authored, reviewable  ->  HIGH.
  * ORAL, pure file -- the QB file's own title names exactly one domain AND
    the question's own text either agrees or says nothing  ->  HIGH.
  * ORAL, pure file CONTRADICTED -- the title names one domain but the
    question's own text cues only OTHER domains  ->  MEDIUM, REVIEW_PENDING.
  * ORAL, mixed file -- a domain cue matches the question text  ->  MEDIUM,
    which is REVIEW_PENDING and never silently published.
  * anything else -> UNRESOLVED / ACCIDENTALLY_UNMAPPED, which fails the gate.

A STRONG SOURCE IS NOT A SETTLED DECISION. File-level evidence must never
suppress obvious question-level contradictory evidence: a QB file title is a
reliable statement about the FILE and an unreliable one about any particular
question inside it. That is why `mapping_evidence` (what was read) and
`mapping_confidence` (what was decided) are two fields and not one.

Stable ids are load-bearing: `topic_id` (D01..) and `canonical_question_id`
(`QB1_A#q1`, `QP2301-Q1`) must never change. Display names may.
"""
import hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import study_spine as SP

SCHEMA_VERSION = '1.1'   # 1.1 adds `mapping_evidence` to every record.

# The Oral decision RULES, versioned apart from the record schema so that
# changing how a topic is decided moves the taxonomy digest -- and therefore
# re-derives every stored mapping -- even when the record shape is untouched.
ORAL_DECISION_RULES = 'file-cue-contradiction-v1'

# No official DGMA instrument exists in this repository. When one is obtained,
# bump this and populate `syllabus_node_id`; nothing else in the record moves.
SYLLABUS_VERSION = 'MIW-DERIVED-1.0'
NO_OFFICIAL_SOURCE = 'NO_OFFICIAL_SOURCE_IN_REPO'

CONFIDENCE = ('HIGH', 'MEDIUM', 'LOW', 'UNRESOLVED')
STATUS = ('VALID_MAPPED', 'REVIEW_PENDING', 'INTENTIONALLY_UNMAPPED',
          'ACCIDENTALLY_UNMAPPED')
ROLE = ('PRIMARY', 'SECONDARY', 'CROSS_TOPIC')
CONTENT_TYPE = ('ORAL', 'WRITTEN')

# --------------------------------------------------------------------------- #
# TWO FIELDS, TWO QUESTIONS -- never collapse them into one number:
#
#   mapping_evidence    WHAT WAS READ.     How strong is the SOURCE signal?
#   mapping_confidence  WHAT WAS DECIDED.  How sure are we that THIS question
#                                          belongs to THIS topic?
#
# `mapping_confidence` is ALWAYS confidence in the mapping decision. It is
# never confidence that the file title was read correctly -- that claim lives
# in `mapping_evidence`, and the two can legitimately disagree.
# --------------------------------------------------------------------------- #
EVIDENCE = (
    'GOVERNED_FIELD',            # written spec primary_category
    'FILE_TITLE',                # oral file names one domain; question silent
    'FILE_TITLE_CORROBORATED',   # ... and the question's own cue agrees
    'FILE_TITLE_CONTRADICTED',   # ... but the question's own cue points away
    'TEXT_CUE',                  # mixed file; only the question text spoke
    'HUMAN_ADJUDICATION',        # a named reviewer decided, with a written note
    'NONE',                      # nothing spoke
)

# The governing invariant in one line. Evidence of these kinds may never be
# published as a settled mapping, however strong the source behind it is.
EVIDENCE_NEVER_HIGH = ('FILE_TITLE_CONTRADICTED', 'TEXT_CUE', 'NONE')

# Confidence -> the status a fresh mapping is allowed to carry (40D/40J).
STATUS_FOR_CONFIDENCE = {
    'HIGH': 'VALID_MAPPED',
    'MEDIUM': 'REVIEW_PENDING',
    'LOW': 'REVIEW_PENDING',
    'UNRESOLVED': 'ACCIDENTALLY_UNMAPPED',
}

_CUES = [(d, re.compile(p, re.I)) for d, p in SP.QUESTION_CUES]
_CAT2DOM = {c: d['domain_id'] for d in SP.DOMAINS for c in d['written_categories']}
_BY_ID = {d['domain_id']: d for d in SP.DOMAINS}


# --------------------------------------------------------------------------- #
# Taxonomy versioning (40G / 40H)
# --------------------------------------------------------------------------- #
def taxonomy_version():
    """Digest of everything that can change a mapping decision.

    If this digest moves, existing mappings may be STALE -- see
    classify_against_taxonomy(). If it does not move, an incremental run may
    safely leave untouched questions alone.
    """
    payload = json.dumps({
        'schema': SCHEMA_VERSION,
        'domains': [{k: d[k] for k in ('domain_id', 'written_categories',
                                       'prerequisites')} for d in SP.DOMAINS],
        'file_domain': SP.ORAL_FILE_DOMAIN,
        'cues': SP.QUESTION_CUES,
        'oral_rules': ORAL_DECISION_RULES,
    }, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()[:16]


def resolve_topic(topic_id):
    """topic_id -> the domain record, or None. Stable-id lookup."""
    return _BY_ID.get(topic_id)


# --------------------------------------------------------------------------- #
# Official syllabus join (DGMA Circular 49 of 2026, Annexure III)
# --------------------------------------------------------------------------- #
# The official join is STRUCTURAL, like every other decision in this module:
#
#     question --(governed topic mapping)--> MIW topic
#              --(hand-adjudicated crosswalk)--> official node(s)
#
# It composes two audited relations. It never scores question text against
# official wording -- that would be the nearest-neighbour mistake this engine
# exists to avoid, and regulatory prose is exactly the kind of text a crude
# sweep invents false relationships in.
#
# Precision, not ambiguity, is what the official confidence band reports:
#   HIGH   -- the topic has exactly one PRIMARY Annexure III node, so the
#             question is pinpointed.
#   MEDIUM -- the topic carries several PRIMARY nodes. The candidate set is
#             complete and correct; the question is simply not pinpointed
#             within it. Node-level refinement is future work, not a defect,
#             so these do NOT flood the adjudication queue.
# Only ORPHANED is a genuine finding requiring review.
OFFICIAL_VERSION = 'DGMA-C49-2026-ANNEX3'
OFFICIAL_STATUS = 'OFFICIAL_SOURCE_ADOPTED_NOT_YET_EFFECTIVE'
OFFICIAL_EFFECTIVE_FROM = '2027-01-01'
ALIGNMENT = ('CROSSWALK_ALIGNED', 'SUPPORTING_ONLY',
             'ORPHANED_IN_ADOPTED_SYLLABUS', 'UNRESOLVED')

_CROSSWALK_PATH = os.path.join(ROOT, 'docs', 'study', 'official_crosswalk.json')
_official_cache = None


def official_crosswalk():
    """Load the governed crosswalk once. Fails closed if it is missing."""
    global _official_cache
    if _official_cache is None:
        if not os.path.exists(_CROSSWALK_PATH):
            raise SystemExit('FAIL R-OFFICIAL-XWALK: '
                             'docs/study/official_crosswalk.json is missing')
        _official_cache = json.load(open(_CROSSWALK_PATH, encoding='utf-8'))
    return _official_cache


def official_nodes_for_topic(topic_id, role='PRIMARY'):
    """Ordered official node ids whose `role` edge lands on this topic."""
    edges = [e for e in official_crosswalk()['edges']
             if e['topic_id'] == topic_id and e['mapping_role'] == role]
    edges.sort(key=lambda e: e['official_order'])
    return [e['official_node_id'] for e in edges]


def attach_official(rec):
    """Add the adopted-syllabus join to a mapping record, in place."""
    topic = rec.get('topic_id')
    rec['official_syllabus_version'] = OFFICIAL_VERSION
    rec['official_effective_from'] = OFFICIAL_EFFECTIVE_FROM

    if topic is None:
        rec['official_syllabus_node_id'] = None
        rec['official_syllabus_node_candidates'] = []
        rec['official_mapping_confidence'] = 'UNRESOLVED'
        rec['official_mapping_basis'] = 'question has no MIW topic to cross from'
        rec['official_alignment_status'] = 'UNRESOLVED'
        return rec

    primary = official_nodes_for_topic(topic)
    supporting = official_nodes_for_topic(topic, 'SUPPORTING')
    rec['official_supporting_nodes'] = supporting

    # A topic with no PRIMARY node but a real SUPPORTING edge is NOT orphaned:
    # it has an official home, just a secondary one. Collapsing the two would
    # overstate the gap -- D08 (fire/LSA) sits under the emergency-response
    # node, whereas D07 (cargo) has no Annexure III edge of any kind because
    # cargo is a Class II subject.
    if primary:
        nodes, status = primary, 'CROSSWALK_ALIGNED'
        role_note = 'Annexure III node'
    elif supporting:
        nodes, status = supporting, 'SUPPORTING_ONLY'
        role_note = 'Annexure III node as a supporting subject'
    else:
        nodes, status = [], 'ORPHANED_IN_ADOPTED_SYLLABUS'
        role_note = ''

    rec['official_syllabus_node_candidates'] = nodes
    rec['official_alignment_status'] = status

    if not nodes:
        rec['official_syllabus_node_id'] = None
        rec['official_mapping_confidence'] = 'UNRESOLVED'
        rec['official_mapping_basis'] = (
            f'topic {topic} has no edge of any role into Annexure III')
    elif len(nodes) == 1:
        rec['official_syllabus_node_id'] = nodes[0]
        rec['official_mapping_confidence'] = 'HIGH'
        rec['official_mapping_basis'] = (
            f'topic {topic} maps to exactly one {role_note}')
    else:
        rec['official_syllabus_node_id'] = None
        rec['official_mapping_confidence'] = 'MEDIUM'
        rec['official_mapping_basis'] = (
            f'topic {topic} maps to {len(nodes)} Annexure III nodes; '
            'aligned to the set, not pinpointed to one')
    return rec


# --------------------------------------------------------------------------- #
# Record construction
# --------------------------------------------------------------------------- #
def _record(qid, content_type, topic_id, confidence, basis, *, evidence,
            role='PRIMARY', subtopic_id=None, last_reviewed=None,
            status=None, extra=None):
    rec = {
        'canonical_question_id': qid,
        'content_type': content_type,
        'schema_version': SCHEMA_VERSION,
        'syllabus_version': SYLLABUS_VERSION,
        # `syllabus_node_id` belongs to the CURRENTLY OPERATIVE version, which
        # is MIW-derived and has no official node ids of its own. The adopted
        # 2027 syllabus is joined separately by attach_official() below, so
        # the two versions can never be read as one.
        'syllabus_node_id': None,
        'syllabus_status': OFFICIAL_STATUS,
        'topic_id': topic_id,
        'subtopic_id': subtopic_id,
        'mapping_role': role,
        'mapping_evidence': evidence,
        'mapping_confidence': confidence,
        'mapping_basis': basis,
        'mapping_status': status or STATUS_FOR_CONFIDENCE[confidence],
        'taxonomy_version': taxonomy_version(),
        'last_reviewed': last_reviewed,
    }
    attach_official(rec)
    if extra:
        rec.update(extra)
    return rec


# --------------------------------------------------------------------------- #
# Adapters
# --------------------------------------------------------------------------- #
def cue_domains(text):
    """EVERY domain whose cue fires on this text, in registry order.

    Deliberately not first-match-wins: a caller checking for a CONTRADICTION
    needs the whole set, and a question that cues two domains is evidence of
    ambiguity rather than evidence for whichever cue happens to be listed
    first.
    """
    return [d for d, rx in _CUES if rx.search(text or '')]


def map_oral_question(question, file_name):
    """ORAL adapter. `question` is one entry from qb_content_index files[].questions."""
    qid = question['id']
    text = question.get('text')
    extra = {'source_file': file_name, 'anchor': question['anchor'],
             'text': text}
    dom = SP.ORAL_FILE_DOMAIN.get(file_name)

    if dom:
        fires = cue_domains(text)
        if not fires:
            # Silence is not contradiction. The file title stands alone.
            return _record(qid, 'ORAL', dom, 'HIGH',
                           'QB file title names exactly one domain',
                           evidence='FILE_TITLE', extra=extra)
        if dom in fires:
            return _record(qid, 'ORAL', dom, 'HIGH',
                           'QB file title names exactly one domain and the '
                           'question text cues that same domain',
                           evidence='FILE_TITLE_CORROBORATED', extra=extra)
        # CONTRADICTION. The file title remains the best available answer, so
        # topic_id is kept -- emptying a topic on a suspicion would be a worse
        # error than the one being fixed. What changes is the CLAIM: this is
        # no longer a settled mapping but a queued one, publishable only once
        # a human has adjudicated it.
        extra['contradicting_topic_ids'] = fires
        return _record(
            qid, 'ORAL', dom, 'MEDIUM',
            f'QB file title names {dom}, but the question text cues only '
            f'{"/".join(fires)} -- file-level evidence does not settle it',
            evidence='FILE_TITLE_CONTRADICTED', extra=extra)

    # Mixed file: first cue wins, exactly as before.
    hit = next(iter(cue_domains(text)), None)
    if hit:
        return _record(qid, 'ORAL', hit, 'MEDIUM',
                       'domain cue matched question text inside a mixed file',
                       evidence='TEXT_CUE', extra=extra)
    return _record(qid, 'ORAL', None, 'UNRESOLVED',
                   'mixed file and no domain cue matched',
                   evidence='NONE', extra=extra)


def map_written_question(question, paper_id):
    """WRITTEN adapter. `question` is one entry from a spec's questions[]."""
    qid = f"{paper_id}-{question['q_no']}"
    cat = (question.get('primary_category') or '').strip()
    dom = _CAT2DOM.get(cat)
    if dom:
        return _record(qid, 'WRITTEN', dom, 'HIGH',
                       f'spec primary_category {cat!r} (governed field)',
                       evidence='GOVERNED_FIELD', extra={'paper_id': paper_id, 'q_no': question['q_no'],
                              'subparts': len(question.get('subparts') or []),
                              'marks': question.get('total_marks')})
    return _record(qid, 'WRITTEN', None, 'UNRESOLVED',
                   f'primary_category {cat!r} is claimed by no domain',
                   evidence='NONE', extra={'paper_id': paper_id, 'q_no': question['q_no'],
                          'marks': question.get('total_marks')})


def map_question(item, content_type=None, **kw):
    """Single entry point. Dispatches to the correct adapter."""
    ct = content_type or item.get('content_type')
    if ct == 'ORAL':
        return map_oral_question(item, kw.get('file_name') or item.get('source_file'))
    if ct == 'WRITTEN':
        return map_written_question(item, kw.get('paper_id') or item.get('paper_id'))
    raise ValueError(f'content_type must be one of {CONTENT_TYPE}, got {ct!r}')


# --------------------------------------------------------------------------- #
# Validation (40J) -- one record at a time
# --------------------------------------------------------------------------- #
def validate_mapping(rec):
    """Return a list of human-readable errors. Empty list == valid."""
    e = []
    for f in ('canonical_question_id', 'content_type', 'topic_id',
              'mapping_role', 'mapping_evidence', 'mapping_confidence',
              'mapping_basis', 'mapping_status', 'syllabus_version',
              'schema_version'):
        if f not in rec:
            e.append(f'missing field {f}')
    if e:
        return e
    if rec['content_type'] not in CONTENT_TYPE:
        e.append(f"content_type {rec['content_type']!r} invalid")
    if rec['mapping_confidence'] not in CONFIDENCE:
        e.append(f"mapping_confidence {rec['mapping_confidence']!r} invalid")
    if rec['mapping_evidence'] not in EVIDENCE:
        e.append(f"mapping_evidence {rec['mapping_evidence']!r} invalid")
    # THE GOVERNING INVARIANT. A source may be strong and the decision still
    # unsettled, so evidence that the question's own text disputes -- or that
    # the file never spoke to at all -- may never be published as HIGH.
    if rec['mapping_evidence'] in EVIDENCE_NEVER_HIGH \
            and rec['mapping_confidence'] == 'HIGH':
        e.append(f"mapping_evidence {rec['mapping_evidence']} may never carry "
                 f'HIGH mapping_confidence')
    if rec['mapping_status'] not in STATUS:
        e.append(f"mapping_status {rec['mapping_status']!r} invalid")
    if rec['mapping_role'] not in ROLE:
        e.append(f"mapping_role {rec['mapping_role']!r} invalid")
    if rec['topic_id'] is not None and resolve_topic(rec['topic_id']) is None:
        e.append(f"topic_id {rec['topic_id']!r} is not a registered domain")
    # A mapped topic requires a status that admits one, and vice versa.
    if rec['topic_id'] is None and rec['mapping_status'] == 'VALID_MAPPED':
        e.append('VALID_MAPPED with no topic_id')
    if rec['topic_id'] is not None and rec['mapping_status'] == 'ACCIDENTALLY_UNMAPPED':
        e.append('ACCIDENTALLY_UNMAPPED but a topic_id is present')
    # 40D: MEDIUM/LOW may never be published as settled without a review stamp.
    if rec['mapping_confidence'] in ('MEDIUM', 'LOW') \
            and rec['mapping_status'] == 'VALID_MAPPED' \
            and not rec.get('last_reviewed'):
        e.append('MEDIUM/LOW promoted to VALID_MAPPED without last_reviewed')
    # No unearned claim of official authority. `syllabus_node_id` names a node
    # of the CURRENTLY OPERATIVE syllabus version. MIW-DERIVED-1.0 defines no
    # node ids at all, so any value there is fabricated -- and ingesting the
    # official circular must not soften this, because the official nodes
    # belong to the *adopted* version and are carried in the official_* fields.
    if rec.get('syllabus_node_id') is not None:
        if rec.get('syllabus_status') == NO_OFFICIAL_SOURCE:
            e.append('syllabus_node_id set while no official source is registered')
        elif rec.get('syllabus_version') == SYLLABUS_VERSION:
            e.append(f'syllabus_node_id set, but the operative version '
                     f'{SYLLABUS_VERSION} defines no syllabus nodes; official '
                     f'nodes belong in official_syllabus_node_id')

    # --- adopted-syllabus join -------------------------------------------- #
    if 'official_alignment_status' in rec:
        if rec['official_alignment_status'] not in ALIGNMENT:
            e.append(f"official_alignment_status "
                     f"{rec['official_alignment_status']!r} invalid")
        if rec.get('official_mapping_confidence') not in CONFIDENCE:
            e.append(f"official_mapping_confidence "
                     f"{rec.get('official_mapping_confidence')!r} invalid")
        if rec.get('official_syllabus_version') != OFFICIAL_VERSION:
            e.append('official_syllabus_version does not match the ingested '
                     'circular')
        known = {n['official_node_id']
                 for n in official_crosswalk()['edges']}
        for nid in rec.get('official_syllabus_node_candidates') or []:
            if nid not in known:
                e.append(f'official node {nid!r} is not in the crosswalk')
        single = rec.get('official_syllabus_node_id')
        cands = rec.get('official_syllabus_node_candidates') or []
        # A pinpointed node must be one of the candidates, and may only be
        # claimed when the candidate set actually singles it out.
        if single is not None and single not in cands:
            e.append('official_syllabus_node_id is not among its candidates')
        if single is not None and len(cands) != 1:
            e.append('official_syllabus_node_id pinpointed from an ambiguous '
                     'candidate set')
        if rec['official_alignment_status'] in ('CROSSWALK_ALIGNED',
                                                'SUPPORTING_ONLY') and not cands:
            e.append(f"{rec['official_alignment_status']} with no official "
                     'candidates')
        if rec['official_alignment_status'] == 'ORPHANED_IN_ADOPTED_SYLLABUS' \
                and cands:
            e.append('ORPHANED_IN_ADOPTED_SYLLABUS but candidates exist')
    return e


# --------------------------------------------------------------------------- #
# Store helpers (40K)
# --------------------------------------------------------------------------- #
def load_store(path):
    if not os.path.exists(path):
        return {'schema_version': SCHEMA_VERSION,
                'taxonomy_version': taxonomy_version(), 'mappings': {}}
    return json.load(open(path, encoding='utf-8'))


def save_store(store, path):
    store['mappings'] = dict(sorted(store['mappings'].items()))
    body = json.dumps(store, indent=2, ensure_ascii=False) + '\n'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='') as fh:
        fh.write(body)
    return body


def get_question_topic(qid, store):
    """canonical_question_id -> topic_id (or None)."""
    rec = store['mappings'].get(qid)
    return rec['topic_id'] if rec else None


def get_topic_questions(topic_id, store, content_type=None, statuses=None):
    """topic_id -> sorted canonical ids. The topic-side discoverability check."""
    ok = set(statuses or ('VALID_MAPPED',))
    return sorted(
        qid for qid, r in store['mappings'].items()
        if r['topic_id'] == topic_id and r['mapping_status'] in ok
        and (content_type is None or r['content_type'] == content_type))


# --------------------------------------------------------------------------- #
# Incremental update (40G) and taxonomy drift (40H)
# --------------------------------------------------------------------------- #
def classify_against_taxonomy(store):
    """Classify every stored mapping against the CURRENT taxonomy.

    UNCHANGED     -- stamped with the current taxonomy digest
    STALE         -- stamped with an older digest; must be re-derived
    NEEDS_REVIEW  -- carries a non-HIGH confidence and no review stamp
    ORPHANED_NODE -- points at a topic_id the registry no longer defines
    """
    now = taxonomy_version()
    out = {'UNCHANGED': [], 'STALE': [], 'NEEDS_REVIEW': [], 'ORPHANED_NODE': []}
    for qid, r in store['mappings'].items():
        if r['topic_id'] is not None and resolve_topic(r['topic_id']) is None:
            out['ORPHANED_NODE'].append(qid)
        elif r.get('taxonomy_version') != now:
            out['STALE'].append(qid)
        elif r['mapping_status'] == 'REVIEW_PENDING':
            out['NEEDS_REVIEW'].append(qid)
        else:
            out['UNCHANGED'].append(qid)
    return {k: sorted(v) for k, v in out.items()}


def incremental_update(store, items, force=False):
    """Map only what is new or stale. Returns (store, stats).

    `items` is an iterable of (record_input, content_type, kwargs). A question
    whose mapping already carries the current taxonomy digest is left alone
    unless `force` -- so adding one question does not reprocess 721.
    """
    now = taxonomy_version()
    stats = {'added': 0, 'refreshed': 0, 'skipped': 0, 'migrated': 0}
    for item, ct, kw in items:
        rec = map_question(item, ct, **kw)
        qid = rec['canonical_question_id']
        old = store['mappings'].get(qid)
        if old is None:
            stats['added'] += 1
        elif force or old.get('taxonomy_version') != now:
            # Preserve a human review stamp across a re-derivation.
            if old.get('last_reviewed') and old.get('topic_id') == rec['topic_id']:
                rec['last_reviewed'] = old['last_reviewed']
                rec['mapping_status'] = old['mapping_status']
            if old.get('topic_id') != rec['topic_id'] and old.get('topic_id'):
                rec['previous_topic_id'] = old['topic_id']
                stats['migrated'] += 1
            stats['refreshed'] += 1
        else:
            stats['skipped'] += 1
            continue
        store['mappings'][qid] = rec
    store['taxonomy_version'] = now
    store['schema_version'] = SCHEMA_VERSION
    return store, stats


DECISIONS = ('AFFIRM', 'REASSIGN', 'HOLD_REVIEW')


def apply_adjudications(store, adjudications):
    """Apply human review decisions (40D). Returns (store, stats, refusals).

    THREE DECISIONS, ONE GUARD.

      AFFIRM       the mapper is right. Stamp it VALID_MAPPED.
      REASSIGN     the mapper is wrong. Move the question to `topic_id` and
                   stamp it. This is the bounded overlay that lets a human
                   correct a mapping the engine cannot see is wrong -- for
                   instance a question whose own text carries no domain cue at
                   all, so no contradiction can ever be detected for it.
      HOLD_REVIEW  the evidence does not settle it. Keep the mapper's topic as
                   a placeholder, force REVIEW_PENDING and record the
                   candidate topics a later reviewer will need. Never
                   published, and deliberately NOT forced into a topic merely
                   to empty the queue.

    The guard is the same for all three: the entry must RESTATE what the
    mapper currently says, in `mapper_topic_id` (defaulting to `topic_id`).
    If the taxonomy has since moved the question, the entry is refused rather
    than silently rubber-stamping a stale decision.

    Idempotency: a REASSIGN records `adjudicated_from_topic_id`, and the guard
    compares against THAT on later runs. So re-applying an override to an
    already-overridden store is a no-op, while a genuine taxonomy move -- which
    produces a fresh record without that field -- is still caught.
    """
    stats = {'applied': 0, 'reassigned': 0, 'held': 0,
             'refused_topic_moved': 0, 'refused_unknown_id': 0}
    refusals = []
    for qid, a in adjudications.items():
        rec = store['mappings'].get(qid)
        if rec is None:
            stats['refused_unknown_id'] += 1
            refusals.append(f'{qid}: no such question')
            continue
        decision = a.get('decision', 'AFFIRM')
        if decision not in DECISIONS:
            stats['refused_unknown_id'] += 1
            refusals.append(f'{qid}: unknown decision {decision!r}')
            continue

        expected = a.get('mapper_topic_id', a['topic_id'])
        actual = rec.get('adjudicated_from_topic_id', rec['topic_id'])
        if actual != expected:
            stats['refused_topic_moved'] += 1
            refusals.append(
                f'{qid}: adjudicated against mapper topic {expected}, mapper '
                f'now says {actual} -- re-review required')
            continue

        if decision == 'HOLD_REVIEW':
            rec['mapping_confidence'] = 'MEDIUM'
            rec['mapping_status'] = 'REVIEW_PENDING'
            rec['review_hold'] = True
            rec['adjudicated_candidate_topic_ids'] = \
                a.get('candidate_topic_ids') or []
            rec['reviewed_by'] = a.get('reviewer')
            rec['review_note'] = a.get('note')
            rec['mapping_basis'] = (
                'human review found the evidence does not settle this '
                f"question: {a.get('note') or 'no note'}")
            stats['held'] += 1
            continue

        if decision == 'REASSIGN':
            if rec['topic_id'] != a['topic_id']:
                # Drop and re-add so the two provenance keys land in the same
                # ORDER whether or not incremental_update already inserted
                # `previous_topic_id` on this pass. Without this the store is
                # byte-different on a cold build vs a refresh, and --check
                # flips for a reason nobody can see in the data.
                rec.pop('previous_topic_id', None)
                rec['adjudicated_from_topic_id'] = actual
                rec['previous_topic_id'] = actual
                rec['topic_id'] = a['topic_id']
                # The evidence for the NEW topic is the reviewer, not the file
                # title that put the question in the wrong place. Leaving
                # `mapping_evidence` as FILE_TITLE here would re-tell exactly
                # the lie this whole change exists to stop.
                rec['mapping_evidence'] = 'HUMAN_ADJUDICATION'
                rec['mapping_confidence'] = 'HIGH'
                # The official-syllabus join is a FUNCTION of the topic, so it
                # must be recomputed here. Without this the record would carry
                # the old topic's Annexure III nodes under the new topic.
                attach_official(rec)
            rec['mapping_basis'] = (
                f'human adjudication moved this question from {actual} to '
                f"{a['topic_id']}: {a.get('note') or 'no note'}")
            stats['reassigned'] += 1

        rec['last_reviewed'] = a['last_reviewed']
        rec['reviewed_by'] = a.get('reviewer')
        rec['review_note'] = a.get('note')
        rec['mapping_status'] = 'VALID_MAPPED'
        stats['applied'] += 1
    return store, stats, refusals


def review_queue(store):
    """Machine-readable adjudication queue (40I)."""
    q = []
    for qid, r in sorted(store['mappings'].items()):
        if r['mapping_status'] in ('REVIEW_PENDING', 'ACCIDENTALLY_UNMAPPED'):
            cands = _candidates(r)
            q.append({
                'canonical_question_id': qid,
                'content_type': r['content_type'],
                'text': r.get('text') or r.get('short_title'),
                'source_file': r.get('source_file') or r.get('paper_id'),
                'current_topic_id': r['topic_id'],
                'candidate_topic_ids': cands,
                'mapping_evidence': r.get('mapping_evidence'),
                'mapping_confidence': r['mapping_confidence'],
                'reason': r['mapping_basis'],
                'recommended_topic_id': r['topic_id'] or (cands[0] if cands else None),
                # A human who has already looked and could not settle it is a
                # different queue state from one nobody has read yet.
                'review_status': ('HELD_PENDING_EVIDENCE' if r.get('review_hold')
                                  else 'AWAITING_ADJUDICATION'),
            })
    return q


# Queue states, and the reason they must never be summed into one number.
#
# HELD is not UNADJUDICATED. A held item has been read by a named human who
# wrote down why the evidence does not settle it; an awaiting item has been
# read by nobody. Rolling them together makes finished governance work look
# like a backlog -- which is the exact pressure that gets a hold cleared for
# the wrong reason, and the SKILL contract already forbids forcing a topic
# merely to empty the queue.
FRESH_UNADJUDICATED = 'AWAITING_ADJUDICATION'
HELD_ADJUDICATED = 'HELD_PENDING_EVIDENCE'


def queue_summary(items):
    """-> counts that keep human HOLDs apart from unread items.

    ``total`` is every open item; the two components partition it. Any caller
    reporting "how much work is left" wants ``fresh_unadjudicated``.
    """
    fresh = sum(1 for i in items if i.get('review_status') != HELD_ADJUDICATED)
    held = sum(1 for i in items if i.get('review_status') == HELD_ADJUDICATED)
    return {'total': len(items),
            'fresh_unadjudicated': fresh,
            'held_adjudicated': held}


def _candidates(rec):
    """Every domain whose cue also fires -- the evidence a reviewer needs.

    A human HOLD_REVIEW supplies its own candidate set, which outranks the
    cues: the reviewer has already read the question, and the cue lexicon is
    what failed to settle it.
    """
    held = rec.get('adjudicated_candidate_topic_ids')
    if held:
        return list(held)
    text = rec.get('text') or ''
    return [d for d, rx in _CUES if rx.search(text)] if text else []
