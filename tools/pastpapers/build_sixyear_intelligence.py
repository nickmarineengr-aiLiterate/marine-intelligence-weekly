"""Six-year (2021-2026) QP question-lineage intelligence.

INTERNAL ONLY. Question wording and lineage; no answer content is read or written.

Reuses the governed recurrence model (normalise_stem / build_families) rather than
inventing a second equality rule, so a family computed here means the same thing as
a family rendered on a paid page.

INPUTS, BOTH COMMITTED
----------------------
    meoclass1/pastpapers/specs/QP*.json                      the solved papers
    meoclass1/pastpapers/intelligence/
        historical_qp_intelligence.json                      the question-only shelf

A clean checkout regenerates this layer with no source PDF and no local state.
The historical store is refreshed from PDFs by extract_historical_qp.py, which is
a separate step because the PDFs are third-party material kept out of git.

This script previously read its historical input from a hard-coded path inside
one Claude session's scratchpad directory, which meant the layer could not be
rebuilt at all once that directory was cleaned, and that the scratchpad copy and
the committed copy drifted without anything detecting it. Output is derived and
gitignored: the two committed inputs above are the truth.
"""
import json, glob, os, re, sys, difflib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import recurrence_model as RM

REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
MONTHS = RM.MONTHS

SPEC_GLOB = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers', 'specs', 'QP*.json')
INTEL_PATH = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers', 'intelligence',
                          'historical_qp_intelligence.json')
OUT_DIR = os.path.join(REPO_ROOT, 'meoclass1', 'pastpapers', 'intelligence', 'derived')


def write_json(path, payload):
    """LF newlines and no clock read, so a rebuild is byte-identical."""
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)
        fh.write('\n')


def solved_specs(spec_glob=SPEC_GLOB):
    out = []
    for f in sorted(glob.glob(spec_glob)):
        d = json.load(open(f, encoding='utf-8'))
        d['_status'] = 'SOLVED'
        out.append(d)
    return out


def historical_specs(solved_ids, intel_path=INTEL_PATH):
    """Shape the intelligence-only papers like a spec so the governed model can read them.

    GRADUATION IS APPLIED HERE, BY RULE
    -----------------------------------
    The store deliberately keeps a complete shelf record, including sittings that
    have since been solved. A paper that now has a canonical solved spec is
    dropped here, so the same sitting cannot appear twice in the six-year
    universe -- once as a solved question and once as its own intelligence-only
    ghost.

    This replaces a manual step. When September 2023 was solved, its record was
    deleted from the store BY HAND to stop the totals double-counting; the next
    paper would have needed the same surgery, and a forgotten deletion would
    have silently inflated the corpus. Doing it by rule means the totals hold
    across every future paper without anyone remembering anything.
    """
    doc = json.load(open(intel_path, encoding='utf-8'))
    out = []
    for p in doc['papers']:
        if p['paper_id'] in solved_ids:
            continue
        qs = []
        for q in p['questions']:
            limbs = q['printed_limbs']
            qs.append({
                'question_id': q['question_id'],
                'q_no': q['q_no'],
                'anchor': q['q_no'].lower(),
                'text_verbatim': q['text_verbatim'],
                # rubric is identical across the whole series: 9 printed, answer SIX,
                # "all questions carry equal marks", printed total 100 -> 16 each.
                'total_marks': 16,
                'subparts': [{'ref': f'({l})', 'marks': None, 'text': ''} for l in limbs],
                'short_title': None,
                'primary_category': None,
                'subject_tags': [], 'topic_tags': [],
                'host_recurrence_hint': q['host_recurrence_hint'],
                # NO model_answer: these are INTELLIGENCE_ONLY by construction.
            })
        out.append({
            'paper_id': p['paper_id'], 'year': p['year'], 'month': p['month'],
            'month_year': p['sitting'], 'questions': qs, '_status': 'INTELLIGENCE_ONLY',
            'printed_serial': p['printed_serial'], 'second_sitting': p['second_sitting'],
        })
    return out


def main(out_dir=OUT_DIR, spec_glob=SPEC_GLOB, intel_path=INTEL_PATH):
    solved = solved_specs(spec_glob)
    specs = solved + historical_specs({d['paper_id'] for d in solved}, intel_path)
    os.makedirs(out_dir, exist_ok=True)
    status = {d['paper_id']: d['_status'] for d in specs}
    nodes = RM.load_nodes(specs)
    for qid, n in nodes.items():
        n['status'] = status[n['paper_id']]
    rel = RM.build_families(nodes)

    order = sorted(nodes, key=lambda q: RM._sort_key(nodes[q]))

    # ---- family-level lineage -------------------------------------------------
    fams = collections.defaultdict(list)
    for qid in order:
        key = tuple(sorted(set([qid] + list(rel[qid].get('others') or []))))
        fams[key].append(qid)

    records = []
    for key, members in fams.items():
        members = sorted(members, key=lambda q: RM._sort_key(nodes[q]))
        stems = {nodes[q]['_stem'] for q in members}
        sittings = [(nodes[q]['year'], nodes[q]['month_num']) for q in members]
        years = sorted({y for y, _ in sittings})
        first = members[0]
        if len(members) == 1:
            cls = 'UNIQUE'
        elif len(stems) == 1:
            cls = 'EXACT_REPEAT'
        else:
            cls = 'NEAR_REPEAT'
        # dormancy: largest gap in months between consecutive sittings
        idx = sorted((y * 12 + m) for y, m in sittings)
        gap = max((b - a for a, b in zip(idx, idx[1:])), default=0)
        records.append({
            'family_id': first,
            'class': cls,
            'size': len(members),
            'years': years,
            'year_span': len(years),
            'first_seen': nodes[first]['month_year'],
            'first_seen_key': RM._sort_key(nodes[first])[:2],
            'last_seen': nodes[members[-1]]['month_year'],
            'max_gap_months': gap,
            'members': members,
            'statuses': sorted({nodes[q]['status'] for q in members}),
            'stem': nodes[first]['text_verbatim'][:220],
        })
    write_json(os.path.join(out_dir, 'sixyear_families.json'), records)
    write_json(os.path.join(out_dir, 'sixyear_nodes.json'),
               {q: {'status': nodes[q]['status'], 'year': nodes[q]['year'],
                    'month': nodes[q]['month_num'], 'paper': nodes[q]['paper_id'],
                    'q_no': nodes[q]['q_no'], 'stem': nodes[q]['text_verbatim']}
                for q in order})

    # ---- report ---------------------------------------------------------------
    print('=' * 78)
    print('SIX-YEAR QP INTELLIGENCE  2021-2026   (INTERNAL)')
    print('=' * 78)
    byyear = collections.Counter(nodes[q]['year'] for q in order)
    papers = collections.defaultdict(set)
    for q in order:
        papers[nodes[q]['year']].add(nodes[q]['paper_id'])
    print(f"\n{'year':6s} {'papers':>7s} {'questions':>10s}   solved / intelligence-only")
    for y in sorted(byyear):
        sv = len({p for p in papers[y] if status[p] == 'SOLVED'})
        iv = len(papers[y]) - sv
        print(f'{y:<6d} {len(papers[y]):>7d} {byyear[y]:>10d}   {sv} / {iv}')
    print(f"{'TOTAL':6s} {sum(len(v) for v in papers.values()):>7d} {len(order):>10d}")

    cc = collections.Counter(r['class'] for r in records)
    nq = len(order)
    print('\n--- family classes (families / questions involved) ---')
    for c in ('EXACT_REPEAT', 'NEAR_REPEAT', 'UNIQUE'):
        f = [r for r in records if r['class'] == c]
        qn = sum(r['size'] for r in f)
        print(f'  {c:14s} {len(f):4d} families  {qn:4d} questions  {qn/nq*100:5.1f}% of corpus')
    print(f'  {"TOTAL":14s} {len(records):4d} families  {nq:4d} questions')

    print('\n--- longest-running families (by distinct years) ---')
    for r in sorted(records, key=lambda x: (-x['year_span'], -x['size']))[:12]:
        print(f"  {r['year_span']}y x{r['size']:<2d} {r['first_seen']:>15s} -> {r['last_seen']:<15s} "
              f"{r['class']:12s} {r['stem'][:70]}")

    print('\n--- dormant-return (gap >= 24 months, then returned) ---')
    dr = [r for r in records if r['max_gap_months'] >= 24 and r['size'] > 1]
    print(f'  {len(dr)} families')
    for r in sorted(dr, key=lambda x: -x['max_gap_months'])[:10]:
        print(f"  gap {r['max_gap_months']:>3d}mo  x{r['size']:<2d} {r['first_seen']:>15s} -> "
              f"{r['last_seen']:<15s} {r['stem'][:62]}")

    print('\n--- first-seen correction: solved questions whose family actually STARTS in 2021/2022 ---')
    moved = [r for r in records
             if r['size'] > 1 and r['first_seen_key'][0] <= 2022
             and 'SOLVED' in r['statuses'] and 'INTELLIGENCE_ONLY' in r['statuses']]
    print(f'  {len(moved)} families now root before 2023')
    for r in sorted(moved, key=lambda x: x['first_seen_key'])[:15]:
        sv = [m for m in r['members'] if nodes[m]['status'] == 'SOLVED']
        print(f"  {r['first_seen']:>15s} x{r['size']:<2d} {r['class']:12s} solved: {','.join(sv[:3])}")
        print(f"                   {r['stem'][:88]}")
    return records, nodes, rel


if __name__ == '__main__':
    main()
