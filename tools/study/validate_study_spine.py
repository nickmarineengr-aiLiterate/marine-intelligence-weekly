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
