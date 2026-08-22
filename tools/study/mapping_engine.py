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
  * ORAL, pure file -- the QB file's own title names exactly one domain  ->  HIGH.
  * ORAL, mixed file -- a domain cue matches the question text  ->  MEDIUM,
    which is REVIEW_PENDING and never silently published.
  * anything else -> UNRESOLVED / ACCIDENTALLY_UNMAPPED, which fails the gate.

Stable ids are load-bearing: `topic_id` (D01..) and `canonical_question_id`
(`QB1_A#q1`, `QP2301-Q1`) must never change. Display names may.
"""
import hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import study_spine as SP

SCHEMA_VERSION = '1.0'

# No official DGMA instrument exists in this repository. When one is obtained,
# bump this and populate `syllabus_node_id`; nothing else in the record moves.
SYLLABUS_VERSION = 'MIW-DERIVED-1.0'
NO_OFFICIAL_SOURCE = 'NO_OFFICIAL_SOURCE_IN_REPO'

CONFIDENCE = ('HIGH', 'MEDIUM', 'LOW', 'UNRESOLVED')
STATUS = ('VALID_MAPPED', 'REVIEW_PENDING', 'INTENTIONALLY_UNMAPPED',
          'ACCIDENTALLY_UNMAPPED')
ROLE = ('PRIMARY', 'SECONDARY', 'CROSS_TOPIC')
CONTENT_TYPE = ('ORAL', 'WRITTEN')

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
    }, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()[:16]


def resolve_topic(topic_id):
    """topic_id -> the domain record, or None. Stable-id lookup."""
    return _BY_ID.get(topic_id)


# --------------------------------------------------------------------------- #
# Record construction
# --------------------------------------------------------------------------- #
def _record(qid, content_type, topic_id, confidence, basis, *,
            role='PRIMARY', subtopic_id=None, last_reviewed=None,
            status=None, extra=None):
    rec = {
        'canonical_question_id': qid,
        'content_type': content_type,
        'schema_version': SCHEMA_VERSION,
        'syllabus_version': SYLLABUS_VERSION,
        'syllabus_node_id': None,          # populated when an official source exists
        'syllabus_status': NO_OFFICIAL_SOURCE,
        'topic_id': topic_id,
        'subtopic_id': subtopic_id,
        'mapping_role': role,
        'mapping_confidence': confidence,
        'mapping_basis': basis,
        'mapping_status': status or STATUS_FOR_CONFIDENCE[confidence],
        'taxonomy_version': taxonomy_version(),
        'last_reviewed': last_reviewed,
    }
    if extra:
        rec.update(extra)
    return rec


# --------------------------------------------------------------------------- #
# Adapters
# --------------------------------------------------------------------------- #
def map_oral_question(question, file_name):
    """ORAL adapter. `question` is one entry from qb_content_index files[].questions."""
    qid = question['id']
    dom = SP.ORAL_FILE_DOMAIN.get(file_name)
    if dom:
        return _record(qid, 'ORAL', dom, 'HIGH',
                       'QB file title names exactly one domain',
                       extra={'source_file': file_name,
                              'anchor': question['anchor'],
                              'text': question.get('text')})
    hit = next((d for d, rx in _CUES if rx.search(question.get('text') or '')), None)
    if hit:
        return _record(qid, 'ORAL', hit, 'MEDIUM',
                       'domain cue matched question text inside a mixed file',
                       extra={'source_file': file_name,
                              'anchor': question['anchor'],
                              'text': question.get('text')})
    return _record(qid, 'ORAL', None, 'UNRESOLVED',
                   'mixed file and no domain cue matched',
                   extra={'source_file': file_name, 'anchor': question['anchor'],
                          'text': question.get('text')})


def map_written_question(question, paper_id):
    """WRITTEN adapter. `question` is one entry from a spec's questions[]."""
    qid = f"{paper_id}-{question['q_no']}"
    cat = (question.get('primary_category') or '').strip()
    dom = _CAT2DOM.get(cat)
    if dom:
        return _record(qid, 'WRITTEN', dom, 'HIGH',
                       f'spec primary_category {cat!r} (governed field)',
                       extra={'paper_id': paper_id, 'q_no': question['q_no'],
                              'subparts': len(question.get('subparts') or []),
                              'marks': question.get('total_marks')})
    return _record(qid, 'WRITTEN', None, 'UNRESOLVED',
                   f'primary_category {cat!r} is claimed by no domain',
                   extra={'paper_id': paper_id, 'q_no': question['q_no'],
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
              'mapping_role', 'mapping_confidence', 'mapping_basis',
              'mapping_status', 'syllabus_version', 'schema_version'):
        if f not in rec:
            e.append(f'missing field {f}')
    if e:
        return e
    if rec['content_type'] not in CONTENT_TYPE:
        e.append(f"content_type {rec['content_type']!r} invalid")
    if rec['mapping_confidence'] not in CONFIDENCE:
        e.append(f"mapping_confidence {rec['mapping_confidence']!r} invalid")
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
    # No unearned claim of official authority.
    if rec.get('syllabus_node_id') is not None \
            and rec.get('syllabus_status') == NO_OFFICIAL_SOURCE:
        e.append('syllabus_node_id set while no official source is registered')
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


def apply_adjudications(store, adjudications):
    """Apply human review stamps (40D). Returns (store, stats).

    An adjudication may only promote a mapping whose topic_id it RESTATES
    correctly. If the taxonomy has since moved the question elsewhere, the
    stamp is refused rather than silently rubber-stamping a stale decision --
    the whole point of recording topic_id in the adjudication file.
    """
    stats = {'applied': 0, 'refused_topic_moved': 0, 'refused_unknown_id': 0}
    refusals = []
    for qid, a in adjudications.items():
        rec = store['mappings'].get(qid)
        if rec is None:
            stats['refused_unknown_id'] += 1
            refusals.append(f'{qid}: no such question')
            continue
        if rec['topic_id'] != a['topic_id']:
            stats['refused_topic_moved'] += 1
            refusals.append(
                f"{qid}: adjudicated {a['topic_id']}, mapper now says "
                f"{rec['topic_id']} -- re-review required")
            continue
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
                'mapping_confidence': r['mapping_confidence'],
                'reason': r['mapping_basis'],
                'recommended_topic_id': r['topic_id'] or (cands[0] if cands else None),
                'review_status': 'AWAITING_ADJUDICATION',
            })
    return q


def _candidates(rec):
    """Every domain whose cue also fires -- the evidence a reviewer needs."""
    text = rec.get('text') or ''
    return [d for d, rx in _CUES if rx.search(text)] if text else []
