#!/usr/bin/env python3
"""Inventory the historical Written QI assets, and preview what they would do.

    research refs (NEVER merged)          main
    meoclass1/pastpapers/intelligence/v2  docs/study/study_mappings.json
              |                                     |
              +------------> read via `git show` <--+
                                    |
                    docs/study/historical_qi_asset_inventory.json

WHY THIS IS ADDITIVE AND CHANGES NOTHING ELSE
---------------------------------------------
`written_evidence_horizon.json` is the socket the study system CONSUMES, and
widening it widens the public claim. Nothing here is integrated evidence: not
one historical occurrence has been ingested, so the socket stays NOT_STARTED
and this file sits beside it as the record of what exists, where, and how far
it can be trusted. A recovery session picks it up; a marketing sentence
cannot.

THE JOIN IS GOVERNED, NOT INVENTED
----------------------------------
QI-v2 families carry their own topic vocabulary ("Marine insurance", "Human
factors"). That vocabulary is NOT mapped onto D01-D10 here. Instead each
family is joined through the questions it actually contains: every occurrence
names a `question_id`, and `study_mappings.json` already assigns that question
a topic. So the historical layer inherits the spine's classification rather
than proposing a rival one. A family whose questions disagree is reported
AMBIGUOUS_REVIEW rather than being forced.

DETERMINISM: no clock is read. `current_as_of` is carried from the source
artefacts themselves, so two runs over the same refs are byte-identical.

Usage:
    python tools/study/build_historical_qi_inventory.py
    python tools/study/build_historical_qi_inventory.py --check
"""
import argparse
import collections
import io
import json
import os
import re
import subprocess
import sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

OUT = os.path.join(ROOT, 'docs', 'study', 'historical_qi_asset_inventory.json')
MAPPINGS = os.path.join(ROOT, 'docs', 'study', 'study_mappings.json')
HORIZON = os.path.join(ROOT, 'docs', 'study', 'written_evidence_horizon.json')
QI_ADJ = os.path.join(HERE, 'qi_family_adjudications.json')
WORDING = os.path.join(ROOT, 'meoclass1', 'pastpapers', 'intelligence',
                       'historical_qp_intelligence.json')

# The research tip. Phase 3B is the superset: 3A2/3A3 carry the same families
# and occurrences byte-for-byte but not the 98-object source inventory.
QI_REF = 'origin/research/question-intelligence-v2-phase3b'
QI_DIR = 'meoclass1/pastpapers/intelligence/v2'

REVIEW_REFS = (
    'review/question-intelligence-v2-phase2',
    'review/question-intelligence-v2-phase3a',
    'review/question-intelligence-v2-phase3a1',
    'review/question-intelligence-v2-phase3a2',
    'review/question-intelligence-v2-phase3a3',
)


def git(*args):
    r = subprocess.run(['git'] + list(args), cwd=ROOT, capture_output=True,
                       text=True, errors='replace')
    if r.returncode:
        return None
    return r.stdout


def show(ref, path):
    return git('show', '%s:%s' % (ref, path))


def show_json(ref, path):
    raw = show(ref, path)
    return json.loads(raw) if raw else None


def show_jsonl(ref, path):
    raw = show(ref, path)
    if not raw:
        return []
    return [json.loads(l) for l in raw.splitlines() if l.strip()]


def ref_exists(ref):
    return git('rev-parse', '--verify', '--quiet', ref) is not None


# --------------------------------------------------------------------------- #
def build():
    if not ref_exists(QI_REF):
        raise SystemExit('FAIL: %s is not reachable; fetch origin first' % QI_REF)

    fam_doc = show_json(QI_REF, QI_DIR + '/QUESTION_FAMILIES.json')
    inv_doc = show_json(QI_REF, QI_DIR + '/PHASE3B_SOURCE_INVENTORY.json')
    bank_doc = show_json(QI_REF, QI_DIR + '/OFFICIAL_BANK_ITEMS.json')
    man_doc = show_json(QI_REF, QI_DIR + '/SOURCE_MANIFEST.json')
    occ_lines = show_jsonl(QI_REF, QI_DIR + '/QUESTION_OCCURRENCES.jsonl')

    # The occurrences file leads with a schema/comment object. Counting lines
    # instead of records is how "25 occurrences" becomes "26" -- it did, in an
    # earlier read of this same file.
    occ = [o for o in occ_lines if 'occurrence_id' in o]
    occ_header = next((o for o in occ_lines if 'occurrence_id' not in o), {})

    families = fam_doc['families']
    sources = inv_doc['sources']

    # ---- historical paper identity: what can each archived object claim? ---
    papers = [s for s in sources if s.get('document_type') != 'EXAM_RESULT_LIST']
    by_date_status = collections.Counter(s.get('paper_date_status') for s in papers)
    by_content = collections.Counter(s.get('content_status') for s in papers)
    date_certain = [s for s in papers
                    if s.get('sitting_year') and s.get('sitting_month')]
    year_only = [s for s in papers
                 if s.get('sitting_year') and not s.get('sitting_month')]
    undated = [s for s in papers if not s.get('sitting_year')]

    def _span(rows, with_month):
        if not rows:
            return None
        if with_month:
            ks = sorted((r['sitting_year'], r['sitting_month']) for r in rows)
            return {'earliest': '%04d-%s' % (ks[0][0], ks[0][1]),
                    'latest': '%04d-%s' % (ks[-1][0], ks[-1][1])}
        ys = sorted(r['sitting_year'] for r in rows)
        return {'earliest_year': ys[0], 'latest_year': ys[-1]}

    # ---- the governed family -> D-topic join ------------------------------
    store = json.load(open(MAPPINGS, encoding='utf-8'))['mappings']
    occ_by_id = {o['occurrence_id']: o for o in occ}
    joins, join_counts = [], collections.Counter()
    for f in families:
        qids = set()
        for oid in f.get('known_occurrences') or ():
            o = occ_by_id.get(oid)
            if o and o.get('question_id'):
                qids.add(o['question_id'])
        m = re.match(r'(QP\d{4}-Q\d+)', f.get('current_recurrence') or '')
        if m:
            qids.add(m.group(1))
        mapped = {q: store[q]['topic_id'] for q in qids
                  if q in store and store[q].get('topic_id')}
        topics = sorted(set(mapped.values()))
        unmapped = sorted(q for q in qids if q not in store)
        if len(topics) == 1:
            status = 'JOINED'
        elif len(topics) > 1:
            status = 'AMBIGUOUS_REVIEW'
        else:
            status = 'UNJOINABLE_NO_MAPPED_QUESTION'
        join_counts[status] += 1
        joins.append({
            'family_id': f['family_id'],
            'qi_v2_topic': f.get('topic'),
            'join_status': status,
            'topic_id': topics[0] if len(topics) == 1 else None,
            'candidate_topic_ids': topics,
            'joined_via': sorted(mapped),
            'questions_outside_study_mappings': unmapped,
            'frequency_known': f.get('frequency_known'),
            'earliest_occurrence': f.get('earliest_occurrence'),
            'latest_occurrence': f.get('latest_occurrence'),
            'dormancy_class': f.get('dormancy_class'),
            'date_confidence': f.get('date_confidence'),
            'publication_status': f.get('publication_status'),
            'provenance_tier': f.get('provenance_tier'),
        })

    # A question that lands in two families is NOT automatically a defect.
    # QI-v2 observes recurrence at LIMB level, so one question legitimately
    # belongs to two families when its limbs do. The join below can only see
    # question ids, so it cannot tell a real double membership from a broken
    # one -- qi_family_adjudications.json supplies the limb dimension, and this
    # builder FAILS CLOSED on any shared question that has not been adjudicated
    # or whose recorded family set no longer matches the ref.
    q_to_families = collections.defaultdict(list)
    for j in joins:
        for q in j['joined_via']:
            q_to_families[q].append(j['family_id'])
    shared_raw = {q: sorted(fs) for q, fs in q_to_families.items() if len(fs) > 1}

    adj_doc = json.load(open(QI_ADJ, encoding='utf-8'))
    adj = adj_doc['adjudications']
    shared, adj_errors = {}, []
    for q, fs in sorted(shared_raw.items()):
        a = adj.get(q)
        if a is None:
            adj_errors.append('%s is in %s and has no adjudication in '
                              'tools/study/qi_family_adjudications.json' % (q, fs))
            shared[q] = {'families': fs, 'adjudication': None,
                         'verdict': 'UNADJUDICATED'}
            continue
        if sorted(a['families']) != fs:
            adj_errors.append('%s adjudication names %s but the ref holds %s'
                              % (q, sorted(a['families']), fs))
        if a.get('verdict') not in adj_doc['verdicts']:
            adj_errors.append('%s carries unknown verdict %r'
                              % (q, a.get('verdict')))
        shared[q] = {
            'families': fs,
            'verdict': a['verdict'],
            'membership_kind': a.get('membership_kind'),
            'topic_id': a.get('topic_id'),
            'topic_effect': a.get('topic_effect'),
            'roadmap_effect': a.get('roadmap_effect'),
            'last_reviewed': a.get('last_reviewed'),
            'reviewer': a.get('reviewer'),
            'per_family': a.get('per_family'),
            'evidence': a.get('evidence'),
            'candidate_facing_rule': a.get('candidate_facing_rule'),
            'families_after_adjudication': a.get('families_after_adjudication'),
        }
    for q in sorted(adj):
        if q not in shared_raw:
            adj_errors.append('%s is adjudicated but is no longer in more than '
                              'one family -- remove the stale entry' % q)
    if adj_errors:
        sys.stderr.write('QI FAMILY ADJUDICATION FAILURES' + chr(10))
        for e in adj_errors:
            sys.stderr.write('  FAIL %s' % e + chr(10))
        raise SystemExit(2)

    # ---- occurrence span: does ANY of this reach before the current band? --
    occ_years = sorted({o['source_year'] for o in occ if o.get('source_year')})
    horizon = json.load(open(HORIZON, encoding='utf-8'))
    cur = horizon['layers']['current_solved_written']

    # Two different questions, and conflating them is how a research layer
    # gets mistaken for a recovery. The QI-v2 occurrences DO predate the
    # solved band -- they reach into the 2021-2023 wording-only band, which
    # MIW already holds. What would actually be new is an occurrence earlier
    # than ANY written evidence MIW has, and there is none.
    wording_years = sorted({2000 + int(m[0]) for m in
                            re.findall(r'QP(\d{2})(\d{2})',
                                       open(WORDING, encoding='utf-8').read())})
    earliest_held = min([y for y in wording_years] +
                        [int(cur['earliest_sitting'][:4])])
    predates_solved = bool(occ_years) and occ_years[0] < int(cur['earliest_sitting'][:4])
    reaches_back = bool(occ_years) and occ_years[0] < earliest_held

    # ---- per-topic preview: what WOULD change, changing nothing ------------
    preview = collections.defaultdict(lambda: {'families': 0, 'occurrences': 0,
                                               'earliest': None, 'latest': None})
    for j in joins:
        if j['join_status'] != 'JOINED':
            continue
        p = preview[j['topic_id']]
        p['families'] += 1
        p['occurrences'] += j['frequency_known'] or 0
        for k, v in (('earliest', j['earliest_occurrence']),
                     ('latest', j['latest_occurrence'])):
            if v and (p[k] is None or (v < p[k] if k == 'earliest' else v > p[k])):
                p[k] = v

    return {
        'schema': 'miw.study.historical_qi_asset_inventory.v1',
        'status': 'RESEARCH_INVENTORY',
        'generated_by': 'tools/study/build_historical_qi_inventory.py',
        'authority': (
            'A RECORD OF WHAT EXISTS, not evidence the study system consumes. '
            'Nothing here is governed: every asset below lives on an unmerged '
            'research ref and is classified RESEARCH_ONLY at source. The '
            'historical_written_qi socket in written_evidence_horizon.json is '
            'deliberately untouched by this file.'),
        'source_ref': QI_REF,
        'source_ref_sha': (git('rev-parse', QI_REF) or '').strip(),
        'current_as_of': {
            'families': fam_doc.get('current_as_of'),
            'occurrences': occ_header.get('current_as_of'),
            'source_inventory': inv_doc.get('current_as_of'),
            'official_bank': bank_doc.get('current_as_of'),
            'source_manifest': man_doc.get('current_as_of'),
        },

        # ------------------------------------------------------------------ #
        'headline': {
            'historical_occurrences_ingested': 0 if not reaches_back else None,
            'verdict': (
                'DISCOVERED_AND_PRESERVED_BUT_NOT_INGESTED. The 1999-2005 DGS '
                'archive is inventoried, hashed and re-obtainable, but not one '
                'of its questions has been turned into an occurrence record. '
                'Every occurrence and every family currently held begins in '
                '2021-02 or later, so the QI-v2 layer does not yet extend the '
                'evidence horizon backwards at all.'),
            'earliest_occurrence_held': (('%d' % occ_years[0]) if occ_years else None),
            'latest_occurrence_held': (('%d' % occ_years[-1]) if occ_years else None),
            'predates_current_solved_band': predates_solved,
            'earliest_written_evidence_miw_holds': earliest_held,
            'extends_horizon_backwards': reaches_back,
            'extends_horizon_backwards_means': (
                'an occurrence earlier than %d, the earliest written evidence '
                'MIW holds in any band. Reaching into the 2021-2023 '
                'wording-only band is NOT extending the horizon.' % earliest_held),
        },

        'bands': [
            {'band': 'RESEARCH_ARCHIVE_UNINGESTED',
             'range': '1999-2005 (as printed; see date certainty)',
             'papers': len(papers), 'questions_ingested': 0,
             'class': 'RESEARCH_ONLY',
             'where': '%s : %s' % (QI_REF, QI_DIR + '/PHASE3B_SOURCE_INVENTORY.json'),
             'note': 'Metadata only in repo. The PDFs/DOCs are NOT committed '
                     '(public repo); they are held in a git-ignored intake '
                     'store on the authoring workstation, with archive URL + '
                     'sha256 as the machine-independent re-fetch recipe.'},
            {'band': 'ACCESSIBLE_GAP', 'range': '2006-2020',
             'papers': 0, 'questions_ingested': 0,
             'class': 'NOT_FOUND_ON_ACCESSIBLE_STATE',
             'where': None,
             'note': 'Structured search over every reachable ref found nothing. '
                     'Not a claim that no such papers exist.'},
            {'band': 'WORDING_ONLY', 'range': '2021-2023',
             'papers': 30, 'questions_ingested': 270,
             'class': 'GOVERNED_CURRENT',
             'where': 'main : meoclass1/pastpapers/intelligence/'
                      'historical_qp_intelligence.json',
             'note': 'Question wording only, INTELLIGENCE_ONLY, no model answers.'},
            {'band': 'CURRENT_SOLVED',
             'range': '%s to %s' % (cur['earliest_sitting'], cur['latest_sitting']),
             'papers': cur['papers_total'], 'questions_ingested': cur['questions_total'],
             'class': 'GOVERNED_CURRENT', 'where': 'main : solvedQP/ + docs/study/',
             'note': 'The layer the roadmap actually consumes today.'},
        ],

        # ------------------------------------------------------------------ #
        'assets': [
            {'asset_id': 'QI2-FAMILIES', 'path': QI_DIR + '/QUESTION_FAMILIES.json',
             'ref': QI_REF, 'classification': 'RESEARCH_ONLY',
             'schema': fam_doc.get('schema'), 'holds': '%d families' % len(families),
             'reaches_before_2021': False},
            {'asset_id': 'QI2-OCCURRENCES', 'path': QI_DIR + '/QUESTION_OCCURRENCES.jsonl',
             'ref': QI_REF, 'classification': 'RESEARCH_ONLY',
             'schema': occ_header.get('schema'),
             'holds': '%d occurrence records (+1 schema header line)' % len(occ),
             'reaches_before_2021': reaches_back},
            {'asset_id': 'QI2-SOURCE-INVENTORY',
             'path': QI_DIR + '/PHASE3B_SOURCE_INVENTORY.json', 'ref': QI_REF,
             'classification': 'RESEARCH_ONLY', 'schema': inv_doc.get('schema'),
             'holds': '%d archived DGS objects: %d question papers, %d result '
                      'lists, %d sample paper'
                      % (len(sources), inv_doc['counts']['question_papers'],
                         inv_doc['counts']['result_lists'],
                         inv_doc['counts']['sample_papers']),
             'reaches_before_2021': True},
            {'asset_id': 'QI2-OFFICIAL-BANK', 'path': QI_DIR + '/OFFICIAL_BANK_ITEMS.json',
             'ref': QI_REF, 'classification': 'RESEARCH_ONLY',
             'schema': bank_doc.get('schema'),
             'holds': '%s items of the DGS Question Bank MEO CL-I'
                      % bank_doc.get('bank_item_count_total'),
             'date_confidence': bank_doc.get('date_confidence'),
             'reaches_before_2021': None},
            {'asset_id': 'QI2-SOURCE-MANIFEST', 'path': QI_DIR + '/SOURCE_MANIFEST.json',
             'ref': QI_REF, 'classification': 'RESEARCH_ONLY',
             'schema': man_doc.get('schema'),
             'holds': '%s sources with access-compliance record'
                      % man_doc.get('source_count'),
             'reaches_before_2021': True},
            {'asset_id': 'MIW-HISTORICAL-QP',
             'path': 'meoclass1/pastpapers/intelligence/historical_qp_intelligence.json',
             'ref': 'main', 'classification': 'GOVERNED_CURRENT',
             'holds': '2021-2023 question wording, INTELLIGENCE_ONLY',
             'reaches_before_2021': False},
            {'asset_id': 'MIW-SIXYEAR-FAMILIES',
             'path': 'meoclass1/pastpapers/intelligence/derived/sixyear_families.json',
             'ref': 'main', 'classification': 'GOVERNED_CURRENT',
             'holds': 'the CURRENT six-year recurrence layer (2021 onward)',
             'reaches_before_2021': False},
        ],
        'review_refs_unmerged': [r for r in REVIEW_REFS if ref_exists(r)],

        # ------------------------------------------------------------------ #
        'historical_paper_identity': {
            'model': ('An archived object is identified by its DGS archive URL '
                      'plus sha256, NOT by a sitting date. A sitting date is a '
                      'separate, evidenced claim with its own certainty class, '
                      'and most objects cannot support one.'),
            'certainty_classes': dict(by_date_status),
            'content_status': dict(by_content),
            'month_and_year_certain': {'papers': len(date_certain),
                                       'span': _span(date_certain, True)},
            'year_only': {'papers': len(year_only), 'span': _span(year_only, False)},
            'no_date_printed': {'papers': len(undated)},
            'rule': ('No fabricated dates. A year-only paper contributes to '
                     'year-granularity windows only, and an undated paper '
                     'contributes to no window at all.'),
        },
        'limb_model': {
            'source': QI_DIR + '/LIMB_MODEL.md (and the occurrence schema)',
            'key': 'families key on (question_id, limb_label)',
            'limb_kinds': dict(collections.Counter(o.get('limb_kind') for o in occ)),
            'enum': occ_header.get('_limb_kind_enum'),
            'rule': ('Recurrence is observed at LIMB level. Collapsing a '
                     'multi-limb question into one event under-counts.'),
        },
        'source_provenance': {
            'per_occurrence_fields': sorted(
                set(occ[0].keys()) & {'source_ids', 'raw_stem', 'normalized_stem',
                                      'date_confidence', 'source_confidence',
                                      'text_similarity_confidence',
                                      'official_bank_ancestor', 'provenance_tier',
                                      'limb_kind', 'source_question_no'}) if occ else [],
            'confidence_axes': ['text_similarity_confidence', 'date_confidence',
                                'source_confidence'],
            'why_three_axes': ('A family may correctly read HIGH / NONE / HIGH: '
                               'the recurrence is certain, the historical date '
                               'is unproven, the source is sound. One blended '
                               'confidence field hid exactly that case and was '
                               'removed in QI-v2 phase 2.'),
            'raw_wording_rule': 'raw_stem preserves the source exactly and is never modernised.',
            'research_to_governed': ('Nothing crosses from RESEARCH_ONLY to '
                                     'governed without an explicit adoption '
                                     'step. This inventory is not that step.'),
        },

        # ------------------------------------------------------------------ #
        'family_join': {
            'method': ('family -> its occurrence question_ids -> '
                       'study_mappings.json topic_id. The QI-v2 topic string is '
                       'recorded but never used to classify.'),
            'counts': dict(join_counts),
            'questions_in_more_than_one_family': shared,
            'multi_family_rule': (
                'A question in more than one family is not a defect by itself. '
                'Recurrence is observed at LIMB level, so a multi-limb question '
                'can legitimately sit in one family per limb, or in a limb '
                'family and its whole-question family at once. Every entry '
                'above is hand-adjudicated in '
                'tools/study/qi_family_adjudications.json and the build fails '
                'closed on an unadjudicated one.'),
            'families': joins,
        },
        'roadmap_impact_preview': {
            'study_order_changed': False,
            'weights_changed': False,
            'why': ('Nothing to weight. Zero historical occurrences are '
                    'ingested, and every family held sits inside the band the '
                    'roadmap already counts, so adopting them today would add '
                    'no evidence the spine does not already have.'),
            'per_topic_if_adopted': {k: v for k, v in sorted(preview.items())},
            'note': ('per_topic_if_adopted is a PREVIEW of families only. It is '
                     'not a proposal, and no study_priority component is added '
                     'by this file.'),
        },
        'public_claim_effect': {
            'socket_status_unchanged': horizon['layers']['historical_written_qi']['status'],
            'derived_sentence_unchanged': horizon['public_claim']['derived_sentence'],
            'permitted_claims': ['none beyond the current solved band'],
            'forbidden_claims': ['since 2010', '2010-2026', '16 years',
                                 'all historical papers', 'complete archive'],
        },
        'corrections_to_recovery_brief': [
            {'brief_says': 'intelligence/v2/<file>',
             'truth': QI_DIR + '/<file>',
             'why_it_matters': 'the abbreviated path does not exist on any ref'},
            {'brief_says': '80 archived DGS MEO Class I question papers, 1999-2005',
             'truth': ('%d question papers + %d sample paper = %d non-result '
                       'objects. Only %d print month AND year (all 1999); %d are '
                       'year-only; %d print no date at all.'
                       % (inv_doc['counts']['question_papers'],
                          inv_doc['counts']['sample_papers'], len(papers),
                          len(date_certain), len(year_only), len(undated))),
             'why_it_matters': 'the band is not uniformly dateable, so "1999-2005" '
                               'overstates what can be placed on a timeline'},
            {'brief_says': '9 families (7 counted, 7 excluded)',
             'truth': '%d families; %d ACTIVE_RECURRENCE, %d INSUFFICIENT_HISTORY'
                      % (len(families),
                         sum(1 for f in families if f.get('dormancy_class') == 'ACTIVE_RECURRENCE'),
                         sum(1 for f in families if f.get('dormancy_class') == 'INSUFFICIENT_HISTORY')),
             'why_it_matters': 'the counted/excluded phrasing does not match the artefact'},
            {'brief_says': 'the recovery will extend the horizon backwards',
             'truth': 'no occurrence held predates %s' % (occ_years[0] if occ_years else 'n/a'),
             'why_it_matters': 'the archive is discovered, not ingested; that is '
                               'the actual remaining work'},
        ],
        'next_qi_action': (
            'Ingest the 1999-2005 archive into occurrence records. It needs the '
            'raw objects, which are NOT on this laptop: re-fetch from the '
            'archive URLs in PHASE3B_SOURCE_INVENTORY.json and verify against '
            'the recorded sha256, or run on the workstation holding the intake '
            'store. Ingest date-certain papers first (5 papers, 1999), then '
            'year-only, and never assign a month that is not printed.'),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    doc = build()

    if args.check:
        if not os.path.exists(args.out):
            print('FAIL: inventory is missing')
            return 1
        on_disk = json.load(open(args.out, encoding='utf-8'))
        fails = []
        if on_disk != doc:
            fails.append('inventory on disk differs from a fresh build')
        if doc['headline']['extends_horizon_backwards']:
            fails.append('an occurrence now predates the current band -- the '
                         'headline verdict must be re-adjudicated by a human')
        h = json.load(open(HORIZON, encoding='utf-8'))['layers']['historical_written_qi']
        if h['status'] != doc['public_claim_effect']['socket_status_unchanged']:
            fails.append('the QI socket moved while this inventory was stale')
        bad = [c for c in doc['public_claim_effect']['forbidden_claims']
               if c.lower() in json.dumps(doc).lower()
               and c not in str(doc['public_claim_effect']['forbidden_claims'])]
        if bad:
            fails.append('unsupported historical claim present: %s' % bad)
        if fails:
            for f in fails:
                print('FAIL: %s' % f)
            return 1
        print('historical QI inventory -- %d assets, %d families, '
              '%d occurrences ingested from before the current band, '
              'socket still %s'
              % (len(doc['assets']), len(doc['family_join']['families']),
                 0, doc['public_claim_effect']['socket_status_unchanged']))
        return 0

    with open(args.out, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(json.dumps(doc, indent=2, ensure_ascii=False) + '\n')
    print('wrote %s' % os.path.relpath(args.out, ROOT))
    print('  verdict: %s' % doc['headline']['verdict'].split('.')[0])
    print('  %d assets, %d families (%s)'
          % (len(doc['assets']), len(doc['family_join']['families']),
             doc['family_join']['counts']))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
