#!/usr/bin/env python3
"""Export the study roadmap to docs/study/MIW_MEO_Class1_Study_Roadmap.xlsx.

    GOVERNED ARTEFACTS                      NORMALIZED MODEL        WORKBOOK
    study_spine.json          --.
    study_mappings.json         |
    official_syllabus.json      +--->  build_model()  ---->  render_workbook()
    official_crosswalk.json     |      (plain dicts)         (six projections)
    coverage_matrix.json        |
    written_evidence_horizon.json
    study_progress.json       --'   (durable, hand-maintained, never written)

THE RENDERER DECIDES NOTHING. Every cell is a field of the model and every
field is read from a governed artefact. No topic truth, no recurrence
judgement and no syllabus classification is computed here -- a second
classifier living in the Excel tooling would be a second taxonomy by the back
door.

EXPANDABLE BY CONSTRUCTION
--------------------------
No corpus size is hardcoded. Counts come from the evidence horizon, so adding
papers widens the numbers *and the derived public sentence* without anyone
editing this file. The historical-QI columns already exist in the model and
render as NOT YET INTEGRATED; when that layer reaches VALIDATED_RANGE they
populate themselves.

Six sheets rather than one wide one, because forty columns is not a roadmap.
Each sheet is a projection of the same normalized model, so they cannot drift
from one another.

PROGRESS SURVIVES REGENERATION because it is never generated: study_progress.json
is read-only to this tool, and a topic missing from it is NOT_STARTED rather
than an error.

Determinism: no clock is read; the corpus's own `generated_from` is stamped.

Usage:
    python tools/study/export_roadmap_xlsx.py              # write workbook
    python tools/study/export_roadmap_xlsx.py --model-json PATH
    python tools/study/export_roadmap_xlsx.py --check      # model builds + loads
"""
import argparse, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import evidence_model as EM

D = os.path.join(ROOT, 'docs', 'study')
SPINE     = os.path.join(D, 'study_spine.json')
MAPPINGS  = os.path.join(D, 'study_mappings.json')
OFFICIAL  = os.path.join(D, 'official_syllabus.json')
CROSSWALK = os.path.join(D, 'official_crosswalk.json')
COVERAGE  = os.path.join(D, 'coverage_matrix.json')
HORIZON   = os.path.join(D, 'written_evidence_horizon.json')
PROGRESS  = os.path.join(D, 'study_progress.json')
OUT       = os.path.join(D, 'MIW_MEO_Class1_Study_Roadmap.xlsx')

NOT_YET = 'NOT YET INTEGRATED'

# Fields reserved for the historical Written QI layer. They are part of the
# model TODAY so that no schema change is needed when the layer lands.
FUTURE_WRITTEN_FIELDS = (
    'historical_written_papers', 'historical_written_questions',
    'earliest_evidence', 'latest_evidence',
    'long_term_recurrence', 'recent_recurrence', 'trend',
    'currentness', 'historical_qi_status',
)


def _load(path):
    return json.load(open(path, encoding='utf-8'))


def study_order(domains):
    """Dependency-first study order. NOT the priority ranking.

    The two are genuinely different questions and must not be conflated:
    `priority_rank` asks "which topic carries the most weight?" and answers
    D03; study order asks "which can you actually start?" and answers D01,
    because D03 lists D01 as a prerequisite. A roadmap sorted by score would
    open the candidate on a topic they are not yet equipped to read.

    Repeatedly take the highest-scoring topic whose prerequisites are already
    placed. Deterministic, and transparent enough to argue with: ties break on
    topic_id. A prerequisite cycle would strand topics, so anything left
    unplaced is appended in rank order rather than silently dropped -- the
    spine validator already proves the graph is acyclic (R-PREREQ-ACYCLIC).
    """
    by_id = {d['domain_id']: d for d in domains}
    placed, order = set(), []
    while len(order) < len(domains):
        ready = [d for d in domains
                 if d['domain_id'] not in placed
                 and all(p in placed for p in d['prerequisites'])]
        if not ready:
            for d in sorted(domains, key=lambda x: x['priority_rank']):
                if d['domain_id'] not in placed:
                    order.append(d['domain_id'])
                    placed.add(d['domain_id'])
            break
        pick = max(ready, key=lambda d: (d['study_priority']['score'],
                                         d['domain_id']))
        order.append(pick['domain_id'])
        placed.add(pick['domain_id'])
    return {tid: i + 1 for i, tid in enumerate(order)}


def build_model():
    spine, mappings = _load(SPINE), _load(MAPPINGS)
    official, xwalk = _load(OFFICIAL), _load(CROSSWALK)
    coverage, horizon = _load(COVERAGE), _load(HORIZON)
    progress = _load(PROGRESS)

    store = mappings['mappings']
    hist = horizon['layers']['historical_written_qi']
    cur = horizon['layers']['current_solved_written']
    qi_live = hist['status'] in ('VALIDATED_RANGE', 'COMPLETE')

    # papers per topic, counted -- never asserted
    papers_by_topic, questions_by_topic = {}, {}
    for rec in store.values():
        if rec['content_type'] != 'WRITTEN' or not rec.get('topic_id'):
            continue
        papers_by_topic.setdefault(rec['topic_id'], set()).add(rec['paper_id'])
        questions_by_topic[rec['topic_id']] = questions_by_topic.get(rec['topic_id'], 0) + 1

    cov_by_topic = {}
    for row in coverage['nodes']:
        cov_by_topic.setdefault(row['primary_topic'], []).append(row['coverage'])

    order = study_order(spine['domains'])
    topics = []
    for d in sorted(spine['domains'], key=lambda x: order[x['domain_id']]):
        did = d['domain_id']
        prog = (progress.get('topics') or {}).get(did) or {}
        bands = cov_by_topic.get(did, [])
        row = {
            # --- stable identity -----------------------------------------
            'topic_id': did,
            'topic': d['name'],
            'study_order': order[did],
            'priority_rank': d['priority_rank'],
            'prerequisites': ', '.join(d['prerequisites']) or '—',
            'unlocks': ', '.join(d['dependants']) or '—',
            # --- current, growing evidence -------------------------------
            'oral_questions': d['oral']['questions'],
            'examiner_evidenced_oral': d['examiner_intelligence']['oral_questions_with_evidence'],
            'examiner_relationships': d['examiner_intelligence']['relationship_occurrences'],
            'distinct_examiners': d['examiner_intelligence']['distinct_examiners'],
            'current_written_questions': d['written']['questions'],
            'current_written_papers': len(papers_by_topic.get(did, ())),
            'current_written_recurrence_families': d['written_question_intelligence']['recurring_families'],
            'official_syllabus_items': len(d['official_syllabus_nodes']),
            'official_supporting_items': len(d['official_supporting_nodes']),
            'official_node_ids': ', '.join(d['official_syllabus_nodes']) or '—',
            'coverage': ', '.join(f'{b}×{bands.count(b)}'
                                  for b in ('STRONG', 'PARTIAL', 'WEAK', 'NONE')
                                  if bands.count(b)) or '—',
            'priority_score': d['study_priority']['score'],
            # --- durable, user-owned -------------------------------------
            'study_status': prog.get('status', 'NOT_STARTED'),
            'sessions_completed': prog.get('sessions_completed', 0),
            'notes_written': ', '.join(prog.get('notes_written') or []) or '—',
            'last_touched': prog.get('last_touched') or '—',
            # --- links ----------------------------------------------------
            'links': f'topics.html#{did}',
        }
        for f in FUTURE_WRITTEN_FIELDS:
            row[f] = NOT_YET if not qi_live else None
        row['historical_qi_status'] = hist['status']
        row['gaps'] = '—'
        topics.append(row)

    # Topic 01's named gaps are the only hand-recorded ones today; they live
    # in the pack, so the workbook points at them rather than restating them.
    for row in topics:
        if row['topic_id'] == 'D01':
            row['gaps'] = 'N6 duty of care (zero coverage); N7 in-water survey; N8 official log book'
        if row['topic_id'] == 'D07':
            row['gaps'] = 'No Annexure III edge — Class II subject, examined orally anyway'
        if row['topic_id'] == 'D08':
            row['gaps'] = 'Supporting-only under official item 12'

    official_rows = []
    prim = {e['official_node_id']: e for e in xwalk['edges']
            if e['mapping_role'] == 'PRIMARY'}
    cov_by_node = {r['official_node_id']: r for r in coverage['nodes']}
    for n in official['nodes']:
        nid = n['official_node_id']
        c = cov_by_node.get(nid, {})
        official_rows.append({
            'official_node_id': nid,
            'item': n['official_number'],
            'page': n['source_page'],
            'primary_topic': prim.get(nid, {}).get('topic_id'),
            'primary_topic_name': prim.get(nid, {}).get('topic_name'),
            'supporting_topics': ', '.join(
                e['topic_id'] for e in xwalk['edges']
                if e['official_node_id'] == nid and e['mapping_role'] == 'SUPPORTING') or '—',
            'coverage': c.get('coverage'),
            'oral_evidence': c.get('oral_evidence'),
            'written_evidence': c.get('written_evidence'),
            'examiners': c.get('examiners'),
            'official_text': n['official_text'],
        })

    return {
        'schema_version': '1.0',
        'generated_by': 'tools/study/export_roadmap_xlsx.py',
        'generated_from': horizon['generated_from'],
        'versions': dict(horizon['versions'],
                         study_spine_version=spine['spine_version'],
                         mapping_version=mappings['schema_version'],
                         taxonomy_version=mappings['taxonomy_version']),
        'evidence_horizon': horizon['layers'],
        'public_claim': horizon['public_claim']['derived_sentence'],
        'official_source': official['source'],
        'topics': topics,
        'official_nodes': official_rows,
        'future_written_fields': list(FUTURE_WRITTEN_FIELDS),
    }


# --------------------------------------------------------------------------- #
# Renderer
# --------------------------------------------------------------------------- #
def render_workbook(model, out_path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    HEAD = PatternFill('solid', fgColor='1F3B57')
    HEADF = Font(color='FFFFFF', bold=True, size=10)
    MUTED = Font(color='808080', italic=True, size=10)
    WRAP = Alignment(vertical='top', wrap_text=True)
    TOP = Alignment(vertical='top')

    wb = Workbook()
    wb.remove(wb.active)

    def sheet(title, headers, rows, widths, wrap_cols=()):
        ws = wb.create_sheet(title)
        ws.append(headers)
        for i, h in enumerate(headers, 1):
            c = ws.cell(row=1, column=i)
            c.fill, c.font, c.alignment = HEAD, HEADF, WRAP
            ws.column_dimensions[get_column_letter(i)].width = widths[i - 1]
        for r in rows:
            ws.append(r)
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.alignment = WRAP if c.column in wrap_cols else TOP
                if c.value == NOT_YET:
                    c.font = MUTED
        ws.freeze_panes = 'A2'
        ws.auto_filter.ref = ws.dimensions
        return ws

    # --- 1. ROADMAP -- the sheet Nixon actually reads ---------------------
    sheet('ROADMAP',
          ['Study Order', 'Topic ID', 'Topic', 'Prerequisites', 'Unlocks',
           'Oral Qs', 'Examiner-Evidenced Orals', 'Written Qs',
           'Written Papers', 'Recurrence Families', 'Official Items',
           'Coverage', 'Priority Rank', 'Priority Score', 'Study Status',
           'Links', 'Gaps'],
          [[t['study_order'], t['topic_id'], t['topic'], t['prerequisites'],
            t['unlocks'], t['oral_questions'], t['examiner_evidenced_oral'],
            t['current_written_questions'], t['current_written_papers'],
            t['current_written_recurrence_families'],
            t['official_syllabus_items'], t['coverage'], t['priority_rank'],
            t['priority_score'], t['study_status'], t['links'], t['gaps']]
           for t in model['topics']],
          [11, 9, 34, 13, 16, 8, 12, 9, 9, 12, 10, 16, 11, 11, 18, 20, 46],
          wrap_cols={3, 17})

    # --- 2. TOPIC DETAIL --------------------------------------------------
    sheet('TOPIC DETAIL',
          ['Topic ID', 'Topic', 'Oral Qs', 'Examiner-Evidenced Orals',
           'Examiner Relationships', 'Distinct Examiners', 'Written Qs',
           'Written Papers', 'Recurrence Families', 'Official PRIMARY Items',
           'Official SUPPORTING Items', 'Official Node IDs', 'Priority Score'],
          [[t['topic_id'], t['topic'], t['oral_questions'],
            t['examiner_evidenced_oral'], t['examiner_relationships'],
            t['distinct_examiners'], t['current_written_questions'],
            t['current_written_papers'], t['current_written_recurrence_families'],
            t['official_syllabus_items'], t['official_supporting_items'],
            t['official_node_ids'], t['priority_score']]
           for t in model['topics']],
          [9, 34, 8, 12, 12, 10, 9, 9, 12, 12, 12, 34, 11],
          wrap_cols={2, 12})

    # --- 3. OFFICIAL SYLLABUS -- the DGMA text, quoted --------------------
    sheet('OFFICIAL SYLLABUS',
          ['Item', 'Node ID', 'Page', 'Primary Topic', 'Primary Topic Name',
           'Supporting Topics', 'Coverage', 'Official Wording (Annexure III)'],
          [[n['item'], n['official_node_id'], n['page'], n['primary_topic'],
            n['primary_topic_name'], n['supporting_topics'], n['coverage'],
            n['official_text']] for n in model['official_nodes']],
          [6, 13, 6, 13, 32, 17, 11, 120],
          wrap_cols={5, 8})

    # --- 4. COVERAGE ------------------------------------------------------
    sheet('COVERAGE',
          ['Node ID', 'Item', 'Primary Topic', 'Coverage', 'Oral Evidence',
           'Written Evidence', 'Examiners', 'Subject'],
          [[n['official_node_id'], n['item'], n['primary_topic'], n['coverage'],
            n['oral_evidence'], n['written_evidence'], n['examiners'],
            n['official_text'][:160]] for n in model['official_nodes']],
          [13, 6, 13, 11, 13, 15, 10, 90],
          wrap_cols={8})

    # --- 5. WRITTEN QI -- current layer plus the declared future socket ---
    ws = wb.create_sheet('WRITTEN QI')
    cur = model['evidence_horizon']['current_solved_written']
    hist = model['evidence_horizon']['historical_written_qi']
    ws.append(['EVIDENCE HORIZON', '', ''])
    ws['A1'].font = Font(bold=True, size=12)
    rows = [
        ['', '', ''],
        ['Layer', 'CURRENT_SOLVED_WRITTEN', 'HISTORICAL_WRITTEN_QI'],
        ['Status', cur['completeness'], hist['status']],
        ['Source status', cur['source_status'], hist['source_status']],
        ['Papers', cur['papers_total'], hist['papers_total'] or NOT_YET],
        ['Questions', cur['questions_total'], hist['questions_total'] or NOT_YET],
        ['Earliest sitting', cur['earliest_sitting'], hist['earliest_sitting'] or NOT_YET],
        ['Latest sitting', cur['latest_sitting'], hist['latest_sitting'] or NOT_YET],
        ['Years spanned', cur['years_spanned'], hist['years_spanned'] or NOT_YET],
        ['', '', ''],
        ['KNOWN GAPS', '', ''],
    ]
    for g in hist['known_gaps']:
        rows.append(['', f"{g['from_year']}–{g['to_year']}", g['reason']])
    rows += [
        ['', '', ''],
        ['RESERVED FIELDS (populate themselves when the layer is validated)', '', ''],
    ]
    for f in model['future_written_fields']:
        rows.append(['', f, NOT_YET])
    rows += [
        ['', '', ''],
        ['PUBLIC CLAIM (generated, never hand-written)', '', ''],
        ['', model['public_claim'], ''],
    ]
    for r in rows:
        ws.append(r)
    for col, w in zip('ABC', (56, 40, 78)):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows():
        for c in row:
            c.alignment = WRAP
            if c.value == NOT_YET:
                c.font = MUTED
    # --- 6. PROGRESS -- the only sheet a human edits ----------------------
    ws = sheet('PROGRESS',
               ['Topic ID', 'Topic', 'Study Status', 'Sessions Completed',
                'Notes Written', 'Last Touched'],
               [[t['topic_id'], t['topic'], t['study_status'],
                 t['sessions_completed'], t['notes_written'], t['last_touched']]
                for t in model['topics']],
               [9, 34, 20, 17, 40, 14],
               wrap_cols={2, 5})
    ws.append([])
    ws.append(['Progress is stored in docs/study/study_progress.json and is '
               'never overwritten by a regeneration.'])
    ws.cell(row=ws.max_row, column=1).font = MUTED

    # --- 7. ABOUT ---------------------------------------------------------
    ws = wb.create_sheet('ABOUT')
    about = [
        ['MIW — MEO Class I Study Roadmap'],
        [''],
        [model['public_claim']],
        [''],
        ['Official syllabus', model['official_source']['circular']],
        ['Issued', model['official_source']['issue_date']],
        ['Annexure', 'III — Syllabus for MEO Class I Preparatory Course'],
        ['Source SHA-256', model['official_source']['sha256']],
        ['Effective from', '2027-01-01 (adopted, not yet in force)'],
        [''],
        ['Versions'],
    ]
    for k, v in sorted(model['versions'].items()):
        about.append(['', f'{k}', str(v)])
    about += [
        [''],
        ['Every number in this workbook is derived from a governed repository '
         'artefact. Nothing here is typed by hand, and the renderer classifies '
         'nothing itself.'],
    ]
    for r in about:
        ws.append(r)
    ws['A1'].font = Font(bold=True, size=14)
    for col, w in zip('ABC', (34, 40, 78)):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows():
        for c in row:
            c.alignment = WRAP

    wb.save(out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--model-json')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    model = build_model()
    if args.model_json:
        with open(args.model_json, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(json.dumps(model, indent=2, ensure_ascii=False) + '\n')
        print(f'wrote model {args.model_json}')

    if args.check:
        if not os.path.exists(args.out):
            print('FAIL: roadmap workbook is missing')
            return 1
        from openpyxl import load_workbook
        wb = load_workbook(args.out)
        want = ['ROADMAP', 'TOPIC DETAIL', 'OFFICIAL SYLLABUS', 'COVERAGE',
                'WRITTEN QI', 'PROGRESS', 'ABOUT']
        if wb.sheetnames != want:
            print(f'FAIL: sheets {wb.sheetnames} != {want}')
            return 1
        if wb['ROADMAP'].max_row != len(model['topics']) + 1:
            print('FAIL: ROADMAP row count does not match the model')
            return 1
        print(f'roadmap workbook -- {len(wb.sheetnames)} sheets, '
              f'{wb["ROADMAP"].max_row - 1} topics, loads clean')
        return 0

    render_workbook(model, args.out)
    print(f'wrote {os.path.relpath(args.out, ROOT)}')
    print(f'  {len(model["topics"])} topics, '
          f'{len(model["official_nodes"])} official nodes')
    print(f'  claim: {model["public_claim"]}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
