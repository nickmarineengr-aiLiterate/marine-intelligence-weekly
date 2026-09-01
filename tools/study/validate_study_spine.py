#!/usr/bin/env python3
"""Validate docs/study/study_spine.json against the canonical corpora.

Every check FAILS CLOSED: a missing input is an error, never a skip. The
checks that matter most are the ones that stop this layer telling a candidate
something the corpus cannot support --

  * no domain may claim official DGMA authority while no official source
    exists in the repository (R-OFFICIAL);
  * every oral id must resolve to a real file + anchor in the live QB index
    (R-ORAL-ID) -- a study pack that sends Nixon to a dead anchor is worse
    than no study pack;
  * mapped + unresolved must equal the corpus total (R-ACCOUNT) -- questions
    may not be silently dropped to make coverage look complete.

Usage:  python tools/study/validate_study_spine.py
"""
import collections, glob, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import study_spine as SP
import mapping_engine as ME
import evidence_model as EM
import ingest_historical_source_layer as IHSL

SPINE  = os.path.join(ROOT, 'docs', 'study', 'study_spine.json')
QB     = os.path.join(ROOT, 'meoclass1', 'qb_content_index.json')
SPECS  = os.path.join(ROOT, 'meoclass1', 'pastpapers', 'specs', '*.json')

VALID_CONFIDENCE = {'HIGH', 'MEDIUM', 'UNRESOLVED'}

fails, checks = [], 0


def check(rule, ok, detail=''):
    global checks
    checks += 1
    if not ok:
        fails.append(f'{rule}: {detail}')


def _live_corpus_counts(root):
    """(oral, written) canonical question counts, read from the CORPUS.

    Deliberately the same two inputs `build_study_mappings.corpus_items()`
    consumes, and deliberately NOT the mapping store: comparing the store
    against a count derived from the store would pass for any store.
    """
    import glob as _glob
    idx = json.load(open(os.path.join(root, 'meoclass1',
                                      'qb_content_index.json'),
                         encoding='utf-8'))
    oral = sum(len(f['questions']) for f in idx['files'].values())
    written = 0
    for spec_path in _glob.glob(os.path.join(root, 'meoclass1', 'pastpapers',
                                             'specs', '*.json')):
        with open(spec_path, encoding='utf-8') as fh:
            written += len(json.load(fh)['questions'])
    return oral, written


def main():
    if not os.path.exists(SPINE):
        print('FAIL R-EXISTS: docs/study/study_spine.json is missing')
        return 1
    spine = json.load(open(SPINE, encoding='utf-8'))
    qb = json.load(open(QB, encoding='utf-8'))
    specs = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(SPECS))]

    domains = spine['domains']
    ids = [d['domain_id'] for d in domains]

    # ---- R-ID: domain ids unique and registry-backed -----------------------
    check('R-ID-UNIQUE', len(ids) == len(set(ids)), f'duplicate domain ids in {ids}')
    check('R-ID-REGISTRY', set(ids) == set(SP.DOMAIN_IDS),
          f'spine ids {sorted(set(ids))} != registry {sorted(set(SP.DOMAIN_IDS))}')

    # ---- R-OFFICIAL: every claim of DGMA authority must be earned ----------
    # An official source now exists, so this is stricter than before, not
    # looser: a domain may claim exactly the nodes the governed crosswalk
    # gives it -- no more (invented authority) and no fewer (silently dropped
    # official scope).
    xwalk = ME.official_crosswalk()
    known_nodes = {e['official_node_id'] for e in xwalk['edges']}
    for d in domains:
        did = d['domain_id']
        check('R-OFFICIAL',
              d['official_syllabus_nodes'] == ME.official_nodes_for_topic(did),
              f'{did} official_syllabus_nodes disagree with the crosswalk')
        check('R-OFFICIAL-SUPPORTING',
              d.get('official_supporting_nodes')
              == ME.official_nodes_for_topic(did, 'SUPPORTING'),
              f'{did} official_supporting_nodes disagree with the crosswalk')
        for nid in d['official_syllabus_nodes'] + (d.get('official_supporting_nodes') or []):
            check('R-OFFICIAL-NODE', nid in known_nodes,
                  f'{did} cites unknown official node {nid!r}')
        check('R-OFFICIAL-STATUS',
              d['syllabus_status'] == ME.OFFICIAL_STATUS,
              f"{did} syllabus_status={d['syllabus_status']!r}")
        check('R-OFFICIAL-VERSION',
              d.get('official_syllabus_version') == ME.OFFICIAL_VERSION,
              f'{did} official_syllabus_version is not the ingested circular')

    # Every official node must be accounted for by some domain -- an official
    # subject may not vanish silently between the circular and the spine.
    claimed = {n for d in domains
               for n in d['official_syllabus_nodes']
               + (d.get('official_supporting_nodes') or [])}
    check('R-OFFICIAL-ACCOUNT', claimed == known_nodes,
          f'official nodes unaccounted for in the spine: '
          f'{sorted(known_nodes - claimed)}')

    # ---- R-EFFECTIVE: adopted is not the same as in force ------------------
    off = spine.get('official_syllabus') or {}
    check('R-EFFECTIVE-STATUS', off.get('status') == ME.OFFICIAL_STATUS,
          f"spine official status={off.get('status')!r}")
    check('R-EFFECTIVE-FROM', off.get('effective_from') == ME.OFFICIAL_EFFECTIVE_FROM,
          f"spine effective_from={off.get('effective_from')!r}")
    check('R-EFFECTIVE-OPERATIVE',
          off.get('currently_operative_version') == ME.SYLLABUS_VERSION,
          'spine does not record which syllabus version is operative today')
    check('R-EFFECTIVE-DIGEST',
          off.get('source_sha256') == xwalk['official_source']['sha256'],
          'spine official digest does not match the crosswalk source')

    check('R-AUTHORITY', 'not an official dgma syllabus' in spine['authority'].lower(),
          'spine does not disclaim official authority for its own headings')

    # ---- R-TOPIC01: the study pack may not cite a question that is not there
    # A pack that sends Nixon to a dead anchor is worse than no pack, and a
    # pack is exactly the kind of hand-written file that rots as the corpus
    # moves. Every id it prints is re-resolved here on every run.
    pack = os.path.join(ROOT, 'docs', 'study',
                        'TOPIC_01_STATUTORY_SURVEYS_AND_CLASS.md')
    check('R-TOPIC01-EXISTS', os.path.exists(pack), 'Topic 01 pack is missing')
    if os.path.exists(pack):
        import re as _re
        text = open(pack, encoding='utf-8').read()
        live_ids = {q['id'] for f in qb['files'].values() for q in f['questions']}
        store_ids = set(json.load(open(os.path.join(
            ROOT, 'docs', 'study', 'study_mappings.json'),
            encoding='utf-8'))['mappings'])
        cited_oral = sorted(set(_re.findall(r'QB[0-9A-Za-z_]+#q\d+', text)))
        cited_written = sorted(set(_re.findall(r'QP\d{4}-Q\d+', text)))
        check('R-TOPIC01-ORAL-CITED', bool(cited_oral),
              'Topic 01 pack cites no oral questions at all')
        for qid in cited_oral:
            check('R-TOPIC01-ORAL', qid in live_ids,
                  f'Topic 01 pack cites oral {qid}, which is not in the QB index')
        for qid in cited_written:
            check('R-TOPIC01-WRITTEN', qid in store_ids,
                  f'Topic 01 pack cites written {qid}, which is not mapped')
        # The pack quotes official wording: it must name the instrument it
        # quotes and must not present the 2027 syllabus as already in force.
        check('R-TOPIC01-SOURCE', 'No.49 of 2026' in text,
              'Topic 01 pack does not name the official circular it quotes')
        check('R-TOPIC01-NOT-IN-FORCE',
              '2027-01-01' in text or '01-Jan-2027' in text,
              'Topic 01 pack does not state when the official syllabus takes effect')

    # ---- R-COVER: every official node is accounted for by the matrix -------
    cov_path = os.path.join(ROOT, 'docs', 'study', 'coverage_matrix.json')
    check('R-COVER-EXISTS', os.path.exists(cov_path),
          'docs/study/coverage_matrix.json is missing')
    if os.path.exists(cov_path):
        cov = json.load(open(cov_path, encoding='utf-8'))
        scored = {r['official_node_id'] for r in cov['nodes']}
        check('R-COVER-ACCOUNT', scored == known_nodes,
              f'official nodes never scored for coverage: '
              f'{sorted(known_nodes - scored)}')
        check('R-COVER-DIGEST',
              cov['official_source']['sha256'] == xwalk['official_source']['sha256'],
              'coverage matrix was built against different source bytes')
        for r in cov['nodes']:
            check('R-COVER-BAND',
                  r['coverage'] in ('STRONG', 'PARTIAL', 'WEAK', 'NONE'),
                  f"{r['official_node_id']} coverage={r['coverage']!r}")
            # Coverage must never claim more than the evidence: a node with no
            # evidence at all may not be reported as covered.
            if r['oral_evidence'] == 0 and r['written_evidence'] == 0:
                check('R-COVER-HONEST', r['coverage'] == 'NONE',
                      f"{r['official_node_id']} claims {r['coverage']} with no evidence")
        check('R-COVER-DIAGNOSTIC', 'DIAGNOSTIC ONLY' in cov['authority'],
              'coverage matrix does not disclaim being a mapping')

    # ---- R-CAT: every written primary_category claimed exactly once --------
    claimed = collections.Counter(c for d in domains for c in d['written_categories'])
    actual = {(q.get('primary_category') or '').strip()
              for s in specs for q in s['questions']}
    for c in sorted(actual):
        check('R-CAT-CLAIMED', claimed[c] == 1,
              f'primary_category {c!r} claimed by {claimed[c]} domains (want 1)')
    for c in sorted(claimed):
        check('R-CAT-REAL', c in actual,
              f'domain claims {c!r}, which no spec uses (stale registry key)')

    # ---- R-PREREQ: real ids, acyclic ---------------------------------------
    pre = {d['domain_id']: d['prerequisites'] for d in domains}
    for did, ps in pre.items():
        for p in ps:
            check('R-PREREQ-ID', p in ids, f'{did} requires unknown domain {p}')
    colour = {}

    def cyclic(n, stack):
        if colour.get(n) == 'done':
            return False
        if n in stack:
            return True
        stack.append(n)
        for p in pre.get(n, []):
            if p in ids and cyclic(p, stack):
                return True
        stack.pop()
        colour[n] = 'done'
        return False

    for did in ids:
        check('R-PREREQ-ACYCLIC', not cyclic(did, []),
              f'prerequisite cycle reachable from {did}')

    # ---- R-ORAL-ID: every mapped/queued oral id resolves --------------------
    live = {}
    for fname, f in qb['files'].items():
        for q in f['questions']:
            live[q['id']] = (fname, q['anchor'])
    queue = spine['ambiguous_mapping_queue']
    for r in queue:
        check('R-ORAL-ID', r['id'] in live, f"queue id {r['id']} not in QB index")
        check('R-ORAL-ANCHOR', live.get(r['id'], (None, None))[1] == r['anchor'],
              f"queue id {r['id']} anchor mismatch")
        check('R-CONF', r['confidence'] in VALID_CONFIDENCE,
              f"queue id {r['id']} confidence {r['confidence']!r}")
    for d in domains:
        for fn in d['oral']['files']:
            check('R-ORAL-FILE', fn in qb['files'],
                  f"{d['domain_id']} references unknown QB file {fn}")

    # ---- R-ACCOUNT: nothing silently dropped -------------------------------
    t = spine['totals']
    check('R-ACCOUNT-ORAL',
          t['oral_questions_mapped'] + t['oral_questions_unresolved']
          == qb['total_questions'],
          f"mapped {t['oral_questions_mapped']} + unresolved "
          f"{t['oral_questions_unresolved']} != corpus {qb['total_questions']}")
    check('R-ACCOUNT-ORAL-SUM',
          sum(d['oral']['questions'] for d in domains) == t['oral_questions_mapped'],
          'per-domain oral counts do not sum to the mapped total')
    n_written = sum(len(s['questions']) for s in specs)
    check('R-ACCOUNT-WRITTEN',
          t['written_questions_mapped'] + t['written_questions_unmapped'] == n_written,
          f"written mapped+unmapped != corpus {n_written}")
    check('R-ACCOUNT-WRITTEN-SUM',
          sum(d['written']['questions'] for d in domains) == t['written_questions_mapped'],
          'per-domain written counts do not sum to the mapped total')
    check('R-QUEUE-SIZE', len(queue) == t['oral_questions_unresolved'],
          'queue length disagrees with the declared unresolved total')

    # ---- R-CONF-SPLIT: HIGH+MEDIUM accounts for each domain ----------------
    for d in domains:
        o = d['oral']
        check('R-CONF-SPLIT',
              o['high_confidence'] + o['medium_confidence'] == o['questions'],
              f"{d['domain_id']} confidence split does not sum")

    # ---- R-PRIORITY: transparent, normalised weights -----------------------
    check('R-WEIGHTS', abs(sum(SP.PRIORITY_WEIGHTS.values()) - 1.0) < 1e-9,
          f'priority weights sum to {sum(SP.PRIORITY_WEIGHTS.values())}')
    ranks = sorted(d['priority_rank'] for d in domains)
    check('R-RANK', ranks == list(range(1, len(domains) + 1)),
          f'priority ranks are not a permutation: {ranks}')
    for d in domains:
        sp = d['study_priority']
        check('R-SCORE', abs(sum(sp['components'].values()) - sp['score']) < 1e-6,
              f"{d['domain_id']} score != sum of components")
        check('R-SCORE-KEYS', set(sp['components']) == set(SP.PRIORITY_WEIGHTS),
              f"{d['domain_id']} component keys differ from the weight registry")

    # ---- R-WRITTEN-REF: written references resolve -------------------------
    known_papers = {s['paper_id'] for s in specs}
    for d in domains:
        for fam, _n in d['written_question_intelligence']['largest_families']:
            check('R-FAMILY-STR', isinstance(fam, str) and fam.strip() != '',
                  f"{d['domain_id']} has an empty recurrence family label")
    check('R-PAPERS', all(d['written']['papers'] <= len(known_papers) for d in domains),
          'a domain claims more papers than exist')

    # ---- R-STORE: the governed mapping store (40B / 40D / 40J) -------------
    store_path = os.path.join(ROOT, 'docs', 'study', 'study_mappings.json')
    check('R-STORE-EXISTS', os.path.exists(store_path),
          'docs/study/study_mappings.json is missing -- run build_study_mappings.py')
    if os.path.exists(store_path):
        store = json.load(open(store_path, encoding='utf-8'))
        maps = store['mappings']

        # every canonical question in both corpora has a governed record
        expected = set(live)
        for s in specs:
            for q in s['questions']:
                expected.add(f"{s['paper_id']}-{q['q_no']}")
        missing = expected - set(maps)
        check('R-STORE-COVERAGE', not missing,
              f'{len(missing)} canonical questions have NO mapping record '
              f'(e.g. {sorted(missing)[:3]}) -- silent syllabus drift')
        extra = set(maps) - expected
        check('R-STORE-ORPHAN', not extra,
              f'{len(extra)} mapping records reference no live question '
              f'(e.g. {sorted(extra)[:3]}) -- test fixture leak?')

        # each record must satisfy the engine's own contract
        bad = []
        for qid, r in maps.items():
            errs = ME.validate_mapping(r)
            if errs:
                bad.append(f'{qid}: {errs[0]}')
        check('R-STORE-RECORD', not bad,
              f'{len(bad)} invalid mapping records (e.g. {bad[:2]})')

        # 40J: an unmapped question must be INTENTIONALLY so, never accidental
        accidental = [q for q, r in maps.items()
                      if r['mapping_status'] == 'ACCIDENTALLY_UNMAPPED']
        queued = {i['canonical_question_id']
                  for i in json.load(open(os.path.join(
                      ROOT, 'docs', 'study', 'mapping_review_queue.json'),
                      encoding='utf-8'))['items']}
        unqueued = [q for q in accidental if q not in queued]
        check('R-STORE-NO-SILENT-DRIFT', not unqueued,
              f'{len(unqueued)} unmapped questions are not in the review queue '
              f'(e.g. {unqueued[:3]})')

        # ---- R-QUEUE: HELD is not UNADJUDICATED ---------------------------
        # The queue's summary counters must keep human HOLDs apart from items
        # nobody has read. They were summed together until 2026-08-23, which
        # reported finished governance work as outstanding backlog.
        q = json.load(open(os.path.join(
            ROOT, 'docs', 'study', 'mapping_review_queue.json'),
            encoding='utf-8'))
        qstates = q.get('queue_states') or {}
        check('R-QUEUE-STATES-SPLIT',
              'fresh_unadjudicated' in qstates and 'held_adjudicated' in qstates,
              'mapping_review_queue.json reports no fresh/held split')
        check('R-QUEUE-STATES-PARTITION',
              qstates.get('fresh_unadjudicated', 0)
              + qstates.get('held_adjudicated', -1) == qstates.get('total'),
              f'queue_states do not partition the total: {qstates}')
        live_held = {i['canonical_question_id'] for i in q['items']
                     if i.get('review_status') == ME.HELD_ADJUDICATED}
        check('R-QUEUE-HELD-COUNTED',
              qstates.get('held_adjudicated') == len(live_held),
              f"queue says {qstates.get('held_adjudicated')} held, items show "
              f'{len(live_held)}')
        # Every held item must carry the human stamp that earned the hold --
        # otherwise 'held' becomes a place to park unread work.
        unstamped = sorted(x for x in live_held
                           if not maps[x].get('adjudicated_candidate_topic_ids')
                           and not maps[x].get('review_hold'))
        check('R-QUEUE-HELD-IS-HUMAN', not unstamped,
              f'{len(unstamped)} held items carry no human hold record: '
              f'{unstamped[:3]}')
        ftc = q.get('file_title_contradictions') or {}
        by_file = ftc.get('by_file') or {}
        miscounted = sorted(
            f for f, v in by_file.items()
            if v.get('fresh_unadjudicated', 0) + v.get('held_adjudicated', 0)
            != len(v.get('questions', [])))
        check('R-QUEUE-FILE-SPLIT-SUMS', not miscounted,
              f'{len(miscounted)} contradiction files have a split that does '
              f'not sum to their question list: {miscounted[:3]}')
        held_as_fresh = sorted(
            f for f, v in by_file.items()
            if any(qq.get('review_status') == ME.HELD_ADJUDICATED
                   for qq in v.get('questions', []))
            and v.get('held_adjudicated', 0) == 0)
        check('R-QUEUE-NO-HELD-AS-FRESH', not held_as_fresh,
              f'{len(held_as_fresh)} files report a human-held question as '
              f'unadjudicated: {held_as_fresh[:3]}')

        # taxonomy drift must be visible, not silent
        cls = ME.classify_against_taxonomy(store)
        check('R-STORE-FRESH', not cls['STALE'],
              f"{len(cls['STALE'])} mappings carry a superseded taxonomy digest")
        check('R-STORE-NODES', not cls['ORPHANED_NODE'],
              f"{len(cls['ORPHANED_NODE'])} mappings point at a deleted topic id")
        check('R-STORE-VERSION',
              store.get('taxonomy_version') == ME.taxonomy_version(),
              'store taxonomy_version does not match the registry')

        # the spine and the store must agree -- two views, one truth
        store_mapped = sum(1 for r in maps.values()
                           if r['content_type'] == 'ORAL' and r['topic_id'])
        check('R-STORE-AGREES-SPINE', store_mapped == t['oral_questions_mapped'],
              f'store maps {store_mapped} oral questions, spine says '
              f"{t['oral_questions_mapped']}")

    # ---- R-HSL: the adopted historical SOURCE layer -------------------------
    # Adopted 2026-08-23 as source-layer-only. The gate here is not that it is
    # correct -- its own ingest tool validates that -- but that it has not
    # quietly grown into a coverage claim. A provenance layer that starts
    # carrying question text, or dates that stop saying who claimed them, has
    # become something nobody adjudicated.
    hsl_path = os.path.join(ROOT, 'docs', 'study', 'historical_source_layer.json')
    check('R-HSL-EXISTS', os.path.exists(hsl_path),
          'docs/study/historical_source_layer.json is missing')
    if os.path.exists(hsl_path):
        hsl = json.load(open(hsl_path, encoding='utf-8'))
        errs = IHSL.validate(hsl)
        check('R-HSL-VALID', not errs, f'{len(errs)} error(s): {errs[:2]}')
        check('R-HSL-SCOPE', hsl.get('status') == 'ADOPTED_SOURCE_LAYER_ONLY',
              f"status is {hsl.get('status')!r}, not ADOPTED_SOURCE_LAYER_ONLY")
        # It must add nothing to the QI coverage layer that drives claims.
        horizon = json.load(open(os.path.join(
            ROOT, 'docs', 'study', 'written_evidence_horizon.json'),
            encoding='utf-8'))
        h = horizon['layers']['historical_written_qi']
        check('R-HSL-NO-COVERAGE-DRIFT',
              h.get('papers_total') is None and h.get('questions_total') is None,
              'the historical QI coverage layer has been populated without an '
              'adjudicated ingest')
        allowed, why = EM.date_certainty_gate(h)
        check('R-HSL-NO-PUBLIC-DATED-CLAIM', not allowed,
              f'a public dated historical claim is now licensed ({why}) -- '
              f'this requires a Founder decision, not a build')
        for phrase in horizon['public_claim']['forbidden_until_validated']:
            check(f'R-HSL-FORBIDDEN', phrase.lower() not in
                  horizon['public_claim']['derived_sentence'].lower(),
                  f'derived public sentence contains {phrase!r}')

    # ======================================================================= #
    # R-GRAN / R-GAP / R-QUEUE-GAP / R-CHANGE
    # The granularity-aware syllabus coverage and gap layer (job AC-000022).
    #
    # Nothing below replaces or relaxes any check above. These are additional
    # invariants for a layer that did not previously exist, plus non-mutation
    # gates over the stores that layer only READS.
    # ======================================================================= #
    D = os.path.join(ROOT, 'docs', 'study')
    FINAL_DIGEST = ('07170f572c99064fad25eedb0fe985886248a81a49b4eb5d4711fd38'
                    'd186f44d')

    # Recurrence quantities as they stood BEFORE this classification layer was
    # built. Classification is not recurrence: if any of these move, something
    # wrote to a store that is supposed to be read-only here.
    PRE_JOB_QI = {'families': 270, 'entities_in_families': 629,
                  'entities_with_no_recurrence_value': 185}
    PRE_JOB_OCC = {'recurrence_bearing': 1584, 'limb_records_not_counted': 698,
                   'total_records': 2282}
    # Four of these were CORPUS SIZES frozen at the moment the classification
    # layer was built: oral 738, written 360, mappings 1098, unmapped 39.
    # August 2026 Oral production legitimately took the corpus to 759, and all
    # four went red -- not because anything created a question, but because a
    # guard had pinned a TOTAL. That is a confirmed defect class here ("pin
    # identities, not totals"), and it expires in the dangerous direction too:
    # had the corpus SHRUNK to 738 by losing a question, these checks would
    # have stayed silent.
    #
    # The PROPOSITION is untouched and is not stood down: classification must
    # create no question. It is now asserted against the LIVE corpus instead
    # of against a number -- the same corpus the mapper itself consumes
    # (qb_content_index.json + pastpapers/specs/*.json), read here
    # independently of the mapping store so the comparison is not circular.
    # Any question the classification layer invented still fails, at any
    # corpus size, forever.
    _live_oral, _live_written = _live_corpus_counts(ROOT)
    PRE_JOB_CORPUS = {'oral': _live_oral, 'written': _live_written,
                      'mappings': _live_oral + _live_written,
                      'accidentally_unmapped': None,   # derived below
                      'current_answers': 8,
                      'notes_units': 992, 'crosswalk_edges': 43,
                      'official_nodes': 25}

    official_path = os.path.join(D, 'official_syllabus.json')
    check('R-GRAN-OFFICIAL-EXISTS', os.path.exists(official_path),
          'docs/study/official_syllabus.json is missing')
    official = json.load(open(official_path, encoding='utf-8'))
    onodes = official['nodes']
    onode_ids = [n['official_node_id'] for n in onodes]

    # ---- the canonical node set -------------------------------------------
    check('R-GRAN-NODE-COUNT', len(onodes) == 25,
          f'official syllabus carries {len(onodes)} nodes, not 25')
    check('R-GRAN-NODE-UNIQUE', len(set(onode_ids)) == len(onode_ids),
          'official node ids are not unique')
    check('R-GRAN-NODE-SEQUENCE',
          onode_ids == [f'C49-A3-{i:02d}' for i in range(1, 26)],
          f'official node ids are not C49-A3-01..25: {sorted(onode_ids)[:3]}')
    for nid in onode_ids:
        check('R-GRAN-NODE-STABLE-ID', nid.startswith('C49-A3-'),
              f'{nid!r} is not a stable Annexure III node id')

    # ---- the final digest governs -----------------------------------------
    check('R-GRAN-DIGEST-SYLLABUS',
          official['source']['sha256'] == FINAL_DIGEST,
          'official_syllabus.json does not carry the governing final digest')
    check('R-GRAN-DIGEST-XWALK',
          xwalk['official_source']['sha256'] == FINAL_DIGEST,
          'official_crosswalk.json does not carry the governing final digest')

    # ---- every crosswalk target names a real node -------------------------
    for e in xwalk['edges']:
        check('R-GRAN-XWALK-TARGET', e['official_node_id'] in set(onode_ids),
              f"crosswalk edge names unknown node {e['official_node_id']!r}")
    check('R-GRAN-XWALK-EDGES',
          len(xwalk['edges']) == PRE_JOB_CORPUS['crosswalk_edges'],
          f"crosswalk holds {len(xwalk['edges'])} edges, not "
          f"{PRE_JOB_CORPUS['crosswalk_edges']}")

    # ---- granularity is explicit, agrees with the join, and never fans out -
    gstore = json.load(open(os.path.join(D, 'study_mappings.json'),
                            encoding='utf-8'))['mappings']
    check('R-GRAN-CORPUS-STABLE',
          len(gstore) == PRE_JOB_CORPUS['mappings'],
          f'mapping store holds {len(gstore)} records, not '
          f"{PRE_JOB_CORPUS['mappings']} -- classification must create no "
          f'question')
    bad_gran = [q for q, r in gstore.items()
                if r.get('evidence_granularity') not in ME.EVIDENCE_GRANULARITY]
    check('R-GRAN-PRESENT', not bad_gran,
          f'{len(bad_gran)} records carry no valid evidence_granularity: '
          f'{sorted(bad_gran)[:3]}')
    disagree = [q for q, r in gstore.items()
                if r.get('evidence_granularity') != ME.granularity_for(r)]
    check('R-GRAN-AGREES', not disagree,
          f'{len(disagree)} records carry a granularity that disagrees with '
          f'their official join: {sorted(disagree)[:3]}')
    # A resolved node id implies exactly one deterministic mapping.
    nondet = [q for q, r in gstore.items()
              if r.get('official_syllabus_node_id') is not None
              and len(r.get('official_syllabus_node_candidates') or []) != 1]
    check('R-GRAN-RESOLVED-IS-DETERMINISTIC', not nondet,
          f'{len(nondet)} records pinpoint a node from a non-singleton '
          f'candidate set: {sorted(nondet)[:3]}')
    unreal = sorted({n for r in gstore.values()
                     for n in ((r.get('official_syllabus_node_candidates') or [])
                               + ([r['official_syllabus_node_id']]
                                  if r.get('official_syllabus_node_id') else []))
                     if n not in set(onode_ids)})
    check('R-GRAN-MAP-TARGET', not unreal,
          f'mappings name official node ids that do not exist: {unreal[:3]}')

    # THE FAN-OUT GATE. Fold every TOPIC_LEVEL record and require that not one
    # node-level tally moved. This is the invariant
    # tools/study/test_syllabus_fanout.py pins, checked here over the whole
    # live corpus rather than one record.
    topic_level = [ME.coverage_contribution(r) for r in gstore.values()
                   if r.get('evidence_granularity') == 'TOPIC_LEVEL']
    fan = ME.tally_contributions(topic_level, onode_ids)
    inflated = sorted(n for n, t in fan['by_node'].items() if t['resolved'])
    check('R-GRAN-NO-FANOUT', not inflated,
          f'{len(inflated)} nodes gained node-level evidence from topic-level '
          f'records: {inflated[:5]}')
    check('R-GRAN-FANOUT-TOTALS', fan['totals']['resolved'] == 0
          and fan['totals']['topic_level'] == len(topic_level),
          f"topic-level fold reports {fan['totals']}")

    # ---- the register ------------------------------------------------------
    reg_path = os.path.join(D, 'syllabus_gap_register.json')
    check('R-GAP-EXISTS', os.path.exists(reg_path),
          'docs/study/syllabus_gap_register.json is missing')
    if os.path.exists(reg_path):
        import build_syllabus_gap_register as GAP
        reg = json.load(open(reg_path, encoding='utf-8'))
        recs = reg['nodes']
        check('R-GAP-25', len(recs) == 25,
              f'register carries {len(recs)} records, not 25')
        rids = [r['official_node_id'] for r in recs]
        check('R-GAP-IDS', rids == sorted(onode_ids),
              'register node ids are not exactly the 25 official ids in order')
        check('R-GAP-NO-DUPLICATE', len(set(rids)) == len(rids),
              'register carries a duplicate official node id')
        check('R-GAP-DIGEST',
              reg['official_source']['sha256'] == FINAL_DIGEST,
              'register does not cite the governing final digest')
        check('R-GAP-NOT-DIAGNOSTIC-PROMOTION',
              'diagnostic only' in reg['authority'].lower(),
              'register does not restate that coverage_matrix stays DIAGNOSTIC')
        for r in recs:
            nid = r['official_node_id']
            for f in ('official_label', 'miw_topic_edges', 'tallies',
                      'coverage_state', 'evidence_granularity',
                      'review_required', 'provenance', 'mapping_state'):
                check('R-GAP-FIELDS', f in r, f'{nid} has no {f}')
            t = r['tallies']
            check('R-GAP-STREAMS', set(t) == set(GAP.STREAMS),
                  f'{nid} tallies cover {sorted(t)}')
            check('R-GAP-THREE-QUANTITIES',
                  all(set(v) == {'resolved', 'topic_level', 'ambiguous'}
                      for v in t.values()),
                  f'{nid} does not expose the three quantities separately')
            check('R-GAP-STATE-DERIVED',
                  r['coverage_state'] == GAP.coverage_state(t),
                  f"{nid} coverage_state {r['coverage_state']!r} is not what "
                  f'its own tallies compute')
            check('R-GAP-MAPPING-DERIVED',
                  r['mapping_state'] == GAP.mapping_state(t),
                  f"{nid} mapping_state is not what its tallies compute")
            check('R-GAP-GRAN-DERIVED',
                  r['evidence_granularity'] == GAP.node_granularity(t),
                  f'{nid} evidence_granularity is not what its tallies compute')
            check('R-GAP-REVIEW-FLAG',
                  r['review_required'] == (r['evidence_granularity']
                                           != 'NODE_LEVEL'),
                  f'{nid} review_required disagrees with its granularity')
            check('R-GAP-EDGE-TARGETS',
                  all(ed['topic_id'] in set(SP.DOMAIN_IDS)
                      for ed in r['miw_topic_edges']),
                  f'{nid} cites a topic id that is not a registered domain')

        # classification created nothing
        ins = reg['inputs']
        check('R-GAP-NO-NEW-QUESTIONS',
              ins['oral_questions'] == PRE_JOB_CORPUS['oral']
              and ins['written_questions'] == PRE_JOB_CORPUS['written'],
              f'register consumed {ins["oral_questions"]} oral / '
              f'{ins["written_questions"]} written, expected '
              f"{PRE_JOB_CORPUS['oral']}/{PRE_JOB_CORPUS['written']}")
        check('R-GAP-NO-NEW-ANSWERS',
              ins['current_answer_specs'] == PRE_JOB_CORPUS['current_answers'],
              f"register consumed {ins['current_answer_specs']} answer specs")
        check('R-GAP-NO-NEW-NOTES',
              ins['notes_units'] == PRE_JOB_CORPUS['notes_units'],
              f"register consumed {ins['notes_units']} notes units")
        check('R-GAP-NO-NEW-FAMILIES',
              ins['written_qi_families'] == PRE_JOB_QI['families'],
              f"register consumed {ins['written_qi_families']} QI families")

        # the 39 stay visible, unresolved, and uncounted as coverage
        au = reg['accidentally_unmapped']
        live39 = sorted(q for q, r in gstore.items()
                        if r.get('mapping_status') == 'ACCIDENTALLY_UNMAPPED')
        # Register vs STORE, never vs a frozen 39. The identity comparison
        # immediately below (R-GAP-UNMAPPED-MATCHES-STORE) is the strong one;
        # this keeps the count check meaningful rather than expiring with it.
        check('R-GAP-UNMAPPED-COUNT',
              au['count'] == len(live39),
              f"register reports {au['count']} accidentally-unmapped "
              f"questions, store holds {len(live39)}")
        check('R-GAP-UNMAPPED-MATCHES-STORE',
              [q['canonical_question_id'] for q in au['questions']] == live39,
              'the register unmapped list disagrees with the mapping store')
        for q in au['questions']:
            check('R-GAP-UNMAPPED-AMBIGUOUS',
                  q['mapping_state'] == 'AMBIGUOUS_MAPPING'
                  and q['review_required'] is True
                  and q['evidence_granularity'] == 'AMBIGUOUS',
                  f"{q['canonical_question_id']} is not carried as ambiguous")
        resolved_ids = {r['official_node_id'] for r in recs}
        check('R-GAP-UNMAPPED-NOT-COVERAGE',
              all(not q.get('candidate_official_node_ids')
                  for q in au['questions']),
              'an accidentally-unmapped question carries a governed candidate '
              'set, which would count it as coverage')
        check('R-GAP-UNMAPPED-HYPOTHESIS-REAL',
              all(n in resolved_ids for q in au['questions']
                  for n in q.get('hypothesis_official_node_ids') or []),
              'an unmapped question names a hypothesis node that does not exist')

        # D07 keeps an unresolved status
        d07 = reg['domains_without_official_home']
        check('R-GAP-D07-UNRESOLVED', 'D07' in d07['domain_ids'],
              'D07 is no longer reported as having no official home')
        check('R-GAP-D07-AMBIGUOUS',
              d07['mapping_state'] == 'AMBIGUOUS_MAPPING'
              and d07['review_required'] is True,
              'D07 is not carried as AMBIGUOUS_MAPPING pending adjudication')
        check('R-GAP-D07-NO-CANON',
              'adjudication' in d07['what'].lower(),
              'the D07 entry does not say the question is unadjudicated')
        eng_src = open(os.path.join(HERE, 'mapping_engine.py'),
                       encoding='utf-8').read()
        check('R-GAP-D07-COMMENT-KEPT',
              'cargo is a Class II subject' in eng_src,
              'the original D07 source comment has been deleted')
        check('R-GAP-D07-COMMENT-LABELLED',
              'UNADJUDICATED' in eng_src and 'HYPOTHESIS' in eng_src,
              'the D07 comment is not labelled as an unadjudicated hypothesis')
        status_src = open(os.path.join(D, 'SYLLABUS_SOURCE_STATUS.md'),
                          encoding='utf-8').read()
        check('R-GAP-D07-NOTE',
              'UNADJUDICATED HYPOTHESIS' in status_src,
              'SYLLABUS_SOURCE_STATUS.md carries no durable D07 note')
        check('R-GAP-DRAFT-ABSENT-NOTE',
              'DRAFT SOURCE — ABSENT' in status_src.upper()
              and 'SOURCE ACQUISITION' in status_src.upper()
              and 'official_change_crosswalk.json' in status_src,
              'SYLLABUS_SOURCE_STATUS.md does not record the absent draft and '
              'the unverified crosswalk basis')

    # ---- the coverage matrix keeps its place and its baseline --------------
    cm_path = os.path.join(D, 'coverage_matrix.json')
    check('R-GAP-COVER-EXISTS', os.path.exists(cm_path),
          'docs/study/coverage_matrix.json is missing')
    if os.path.exists(cm_path):
        cm = json.load(open(cm_path, encoding='utf-8'))
        check('R-GAP-COVER-ORAL-BASELINE',
              cm['method']['oral_corpus'] == PRE_JOB_CORPUS['oral'],
              f"coverage matrix oral baseline is "
              f"{cm['method']['oral_corpus']}, not {PRE_JOB_CORPUS['oral']}")
        check('R-GAP-COVER-DIAGNOSTIC',
              cm['authority'].strip().upper().startswith('DIAGNOSTIC ONLY'),
              'coverage_matrix.json no longer declares itself DIAGNOSTIC ONLY')
        check('R-GAP-COVER-DIGEST',
              cm['official_source']['sha256'] == FINAL_DIGEST,
              'coverage matrix does not cite the governing final digest')

    # ---- the queue derives from the register, and only from it -------------
    q_path = os.path.join(D, 'gap_production_queue.json')
    check('R-QUEUE-GAP-EXISTS', os.path.exists(q_path),
          'docs/study/gap_production_queue.json is missing')
    if os.path.exists(q_path) and os.path.exists(reg_path):
        import build_syllabus_gap_register as GAP
        gq = json.load(open(q_path, encoding='utf-8'))
        rebuilt = GAP.build_queue(json.load(open(reg_path, encoding='utf-8')))
        check('R-QUEUE-GAP-DERIVED', gq == rebuilt,
              'the queue on disk is not what the register alone derives')
        check('R-QUEUE-GAP-SOURCE',
              gq['derived_from']['register']
              == 'docs/study/syllabus_gap_register.json',
              'the queue does not declare the register as its only source')
        placed = [n['official_node_id']
                  for lane in gq['lanes'].values() for n in lane]
        check('R-QUEUE-GAP-ACCOUNT', sorted(placed) == sorted(onode_ids),
              'the queue does not place every official node exactly once')
        check('R-QUEUE-GAP-COUNTS',
              gq['counts'] == {k: len(v) for k, v in gq['lanes'].items()},
              'the queue counts disagree with its own lanes')
        for lane in ('P0', 'P1', 'P2', 'P3'):
            offenders = [n['official_node_id'] for n in gq['lanes'][lane]
                         if n['mapping_state'] == 'AMBIGUOUS_MAPPING']
            check('R-QUEUE-GAP-NO-AMBIGUOUS-IN-P',
                  not offenders,
                  f'{lane} holds AMBIGUOUS_MAPPING nodes {offenders[:3]}')
        review = {n['official_node_id'] for n in gq['lanes']['REVIEW']}
        expect_review = {r['official_node_id']
                         for r in json.load(open(reg_path, encoding='utf-8'))['nodes']
                         if r['mapping_state'] == 'AMBIGUOUS_MAPPING'}
        check('R-QUEUE-GAP-REVIEW-LANE', review == expect_review,
              'the review lane is not exactly the AMBIGUOUS_MAPPING nodes')
        for lane in ('P0', 'P1', 'P2', 'P3', 'REVIEW'):
            check('R-QUEUE-GAP-RULE-STATED',
                  bool(gq['rules'].get(lane)),
                  f'{lane} has no stated derivation rule')

    # ---- recurrence is untouched by classification -------------------------
    qi_fam_path = os.path.join(D, 'qi', 'qi_families.json')
    qi_occ_path = os.path.join(D, 'qi', 'qi_occurrences.json')
    check('R-GAP-QI-FAM-EXISTS', os.path.exists(qi_fam_path),
          'docs/study/qi/qi_families.json is missing')
    if os.path.exists(qi_fam_path):
        qfc = json.load(open(qi_fam_path, encoding='utf-8'))['counts']
        for k, v in PRE_JOB_QI.items():
            check('R-GAP-QI-RECURRENCE-HELD', qfc.get(k) == v,
                  f'qi_families counts.{k} is {qfc.get(k)}, was {v} before '
                  f'classification')
    check('R-GAP-QI-OCC-EXISTS', os.path.exists(qi_occ_path),
          'docs/study/qi/qi_occurrences.json is missing')
    if os.path.exists(qi_occ_path):
        qoc = json.load(open(qi_occ_path, encoding='utf-8'))['counts']
        for k, v in PRE_JOB_OCC.items():
            check('R-GAP-OCC-RECURRENCE-HELD', qoc.get(k) == v,
                  f'qi_occurrences counts.{k} is {qoc.get(k)}, was {v} before '
                  f'classification')

    # ---- the draft-to-final crosswalk declares its own weakness ------------
    cx_path = os.path.join(D, 'official_change_crosswalk.json')
    check('R-CHANGE-EXISTS', os.path.exists(cx_path),
          'docs/study/official_change_crosswalk.json is missing')
    if os.path.exists(cx_path):
        cx = json.load(open(cx_path, encoding='utf-8'))
        check('R-CHANGE-DISTINCT',
              cx['schema'] != xwalk.get('schema')
              and 'edges' not in cx,
              'the change crosswalk has been conflated with the topic '
              'crosswalk')
        check('R-CHANGE-AUTHORITY-ABSENT',
              'absent' in cx['authority'].lower(),
              'the change crosswalk does not state that the draft is absent')
        check('R-CHANGE-AUTHORITY-SECTION3',
              'section 3' in cx['authority'].lower()
              and 'SYLLABUS_SOURCE_STATUS.md' in cx['authority'],
              'the change crosswalk does not name its narrative basis')
        check('R-CHANGE-DRAFT-UNACQUIRED',
              cx['draft_source']['text_extracted'] is False
              and cx['draft_source']['item_count'] == 23,
              'the change crosswalk claims draft text it does not have')
        check('R-CHANGE-FINAL-DIGEST',
              cx['final_source']['sha256'] == FINAL_DIGEST,
              'the change crosswalk does not cite the governing final digest')
        check('R-CHANGE-RECORDS', len(cx['records']) == 25,
              f"the change crosswalk carries {len(cx['records'])} records")
        check('R-CHANGE-NARRATIVE-UNCONFIRMED',
              cx['narrative_counts']['confirmed_by_source_comparison'] is False,
              'the change crosswalk claims its narrative counts are confirmed')
        for r in cx['records']:
            check('R-CHANGE-UNVERIFIED',
                  r['provenance'] == 'NARRATIVE_UNVERIFIED'
                  and r['classification'] == 'AMBIGUOUS'
                  and r['review_required'] is True
                  and r['source_verified'] is False,
                  f"{r['final_official_node_id']} is not carried as unverified")
            check('R-CHANGE-TARGET',
                  r['final_official_node_id'] in set(onode_ids),
                  f"{r['final_official_node_id']} is not a real official node")

    # ======================================================================= #
    # R-ROOT / R-ORAL-NONMUT / R-QUEUE-GAP-BYTES
    #
    # These do not restate anything above. They exist because three properties
    # this layer depends on were previously only ARGUED and never MEASURED:
    #   * that every tool here resolves the same repository root, and that the
    #     Notes input is addressed through tools/notes/miw_paths.REPO_ROOT
    #     rather than through a root a study tool guessed for itself;
    #   * that the Oral occurrence, examiner-attribution and recurrence
    #     quantities this classification layer READ are the same quantities
    #     that were present before it ran -- compared against the pre-job blob
    #     in git, not against a number typed into this file;
    #   * that the production queue on disk is byte-identical to what the
    #     register alone re-derives.
    # Every one FAILS CLOSED: if git cannot answer, that is a failure here, not
    # a skip, because an unmeasurable non-mutation claim is not a passing one.
    # ======================================================================= #
    sys.path.insert(0, os.path.join(ROOT, 'tools', 'notes'))
    import miw_paths as MP
    import build_syllabus_gap_register as GAPR

    def _same_root(a, b):
        return (os.path.normcase(os.path.abspath(a))
                == os.path.normcase(os.path.abspath(b)))

    print('resolved roots:')
    print('  validate_study_spine.ROOT        = ' + ROOT)
    print('  mapping_engine.ROOT              = ' + ME.ROOT)
    print('  build_syllabus_gap_register.ROOT = ' + GAPR.ROOT)
    print('  miw_paths.REPO_ROOT              = ' + MP.REPO_ROOT)
    print('  notes input (via REPO_ROOT)      = ' + GAPR.NOTES)
    check('R-ROOT-MIWPATHS', _same_root(MP.REPO_ROOT, ROOT),
          f'miw_paths.REPO_ROOT {MP.REPO_ROOT!r} is not this tool root {ROOT!r}')
    check('R-ROOT-ENGINE', _same_root(ME.ROOT, ROOT),
          f'mapping_engine resolved root {ME.ROOT!r}')
    check('R-ROOT-BUILDER', _same_root(GAPR.ROOT, ROOT),
          f'the gap-register builder resolved root {GAPR.ROOT!r}')
    check('R-ROOT-NOTES-VIA-MIWPATHS',
          GAPR.NOTES == os.path.join(
              MP.REPO_ROOT, 'meoclass1', 'oral-intelligence', 'examiner-audit',
              'ORAL_NOTES_UNITS.jsonl'),
          f'the Notes input {GAPR.NOTES!r} is not resolved through '
          f'miw_paths.REPO_ROOT')

    # ---- the pre-job baseline, read back out of git ------------------------
    def _pre_job_blob(rel):
        """The bytes of `rel` at HEAD -- i.e. before this job wrote anything."""
        import subprocess
        try:
            r = subprocess.run(['git', 'show', 'HEAD:' + rel], cwd=ROOT,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               timeout=180)
        except Exception as exc:                                # noqa: BLE001
            return None, f'git could not be run: {exc}'
        if r.returncode != 0:
            return None, r.stderr.decode('utf-8', 'replace').strip()[:200]
        return r.stdout, ''

    ORAL_SOURCES = [
        ('oral mapping store', 'docs/study/study_mappings.json'),
        ('oral examiner attribution',
         'meoclass1/oral-intelligence/examiner-audit/'
         'CURRENT_EXAMINER_RELATIONSHIPS.jsonl'),
        ('oral recurrence families',
         'meoclass1/oral-intelligence/examiner-audit/'
         'CROSS_EXAMINER_FAMILIES.json'),
        ('oral QB index', 'meoclass1/qb_content_index.json'),
        ('oral notes units',
         'meoclass1/oral-intelligence/examiner-audit/ORAL_NOTES_UNITS.jsonl'),
    ]

    def _oral_quantities(raw, rel):
        """The Oral quantities this job reads, computed from raw file bytes."""
        text = raw.decode('utf-8')
        if rel.endswith('study_mappings.json'):
            m = json.loads(text)['mappings']
            oral = {q: r for q, r in m.items()
                    if r.get('content_type') == 'ORAL'}
            return {'oral_occurrence_records': len(oral),
                    'oral_with_topic': sum(1 for r in oral.values()
                                           if r.get('topic_id')),
                    'oral_accidentally_unmapped':
                        sum(1 for r in oral.values()
                            if r.get('mapping_status')
                            == 'ACCIDENTALLY_UNMAPPED'),
                    'store_records_total': len(m)}, oral
        if rel.endswith('CURRENT_EXAMINER_RELATIONSHIPS.jsonl'):
            rows = [json.loads(l) for l in text.splitlines() if l.strip()]
            return {'examiner_attribution_records': len(rows),
                    'distinct_examiners':
                        len({r.get('examiner') for r in rows}),
                    'distinct_attributed_questions':
                        len({r.get('question_id') for r in rows}),
                    'evidence_id_total':
                        sum(len(r.get('evidence_ids') or []) for r in rows)}, None
        if rel.endswith('CROSS_EXAMINER_FAMILIES.json'):
            fams = json.loads(text)
            return {'oral_recurrence_families': len(fams),
                    'independent_source_occurrences':
                        sum(f.get('independent_source_occurrences') or 0
                            for f in fams),
                    'distinct_wordings':
                        sum(f.get('distinct_wordings') or 0 for f in fams),
                    'matched_question_ids':
                        sum(len(f.get('matched_question_ids') or [])
                            for f in fams)}, None
        if rel.endswith('qb_content_index.json'):
            idx = json.loads(text)
            files = idx.get('files') if isinstance(idx, dict) else None
            return {'qb_index_bytes': len(raw),
                    'qb_index_files': (len(files) if files is not None
                                       else None)}, None
        return {'lines': len([l for l in text.splitlines() if l.strip()]),
                'bytes': len(raw)}, None

    print('ORAL NON-MUTATION EVIDENCE (pre-job = blob at HEAD, '
          'post-job = worktree):')
    live_oral, base_oral = None, None
    for label, rel in ORAL_SOURCES:
        pre, err = _pre_job_blob(rel)
        check('R-ORAL-BASELINE-READABLE', pre is not None,
              f'the pre-job blob of {rel} could not be read from git ({err}); '
              f'non-mutation cannot be measured, so it is not claimed')
        with open(os.path.join(ROOT, *rel.split('/')), 'rb') as fh:
            post = fh.read()
        if pre is None:
            continue
        before, before_recs = _oral_quantities(pre, rel)
        after, after_recs = _oral_quantities(post, rel)
        if rel.endswith('study_mappings.json'):
            base_oral, live_oral = before_recs, after_recs
        for k in sorted(before):
            print(f'  {label:26s} {k:32s} before={before[k]} after={after[k]}')
            check('R-ORAL-NONMUT-QUANTITY', before[k] == after[k],
                  f'{rel} {k} moved from {before[k]} to {after[k]} during '
                  f'classification')
        if not rel.endswith('study_mappings.json'):
            check('R-ORAL-NONMUT-BYTES', pre == post,
                  f'{rel} is not byte-identical to its pre-job blob '
                  f'({len(pre)} -> {len(post)} bytes)')

    # The mapping store IS rewritten by this job (it gains the granularity
    # fields). So it gets the strict test: every Oral record that existed keeps
    # every field it had, at the same value, and only granularity fields appear.
    if base_oral is not None and live_oral is not None:
        CLASSIFICATION_ONLY_KEYS = {'evidence_granularity',
                                    'evidence_granularity_basis',
                                    'official_supporting_nodes'}
        check('R-ORAL-NONMUT-IDS', sorted(base_oral) == sorted(live_oral),
              'the set of Oral question ids changed during classification')
        moved, added = [], set()
        for qid, before_rec in base_oral.items():
            after_rec = live_oral.get(qid) or {}
            for k, v in before_rec.items():
                if after_rec.get(k) != v:
                    moved.append(f'{qid}.{k}')
            added |= set(after_rec) - set(before_rec)
        check('R-ORAL-NONMUT-FIELDS', not moved,
              f'{len(moved)} pre-existing Oral record values changed: '
              f'{sorted(moved)[:5]}')
        check('R-ORAL-NONMUT-ONLY-GRANULARITY-ADDED',
              added <= CLASSIFICATION_ONLY_KEYS,
              f'classification added non-granularity fields to Oral records: '
              f'{sorted(added - CLASSIFICATION_ONLY_KEYS)}')
        print(f'  oral mapping store         fields_changed                   '
              f'{len(moved)}  fields_added={sorted(added)}')

    # ---- the queue is byte-identical to what the register alone derives ----
    if os.path.exists(q_path) and os.path.exists(reg_path):
        import hashlib
        with open(q_path, 'rb') as fh:
            on_disk = fh.read()
        rederived = (json.dumps(
            GAPR.build_queue(json.load(open(reg_path, encoding='utf-8'))),
            indent=2, ensure_ascii=False) + '\n').encode('utf-8')
        print('QUEUE BYTE IDENTITY:')
        print(f'  on-disk    {len(on_disk):6d} bytes '
              f'sha256={hashlib.sha256(on_disk).hexdigest()}')
        print(f'  re-derived {len(rederived):6d} bytes '
              f'sha256={hashlib.sha256(rederived).hexdigest()}')
        check('R-QUEUE-GAP-BYTE-IDENTICAL', on_disk == rederived,
              'the queue file on disk is not byte-identical to the bytes the '
              'register alone re-derives')

    # ---- report ------------------------------------------------------------
    print(f'study spine validator -- {checks} checks')
    if fails:
        for f in fails:
            print('  FAIL ' + f)
        print(f'\n{len(fails)} FAILED')
        return 1
    print('  all PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
