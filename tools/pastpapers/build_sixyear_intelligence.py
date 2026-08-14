"""Six-year (2021-2026) QP question-lineage intelligence.

INTERNAL ONLY. Question wording and lineage; no answer content is read or written.

Reuses the governed recurrence model (normalise_stem / build_families) rather than
inventing a second equality rule, so a family computed here means the same thing as
a family rendered on a paid page.
"""
import json, glob, os, re, sys, difflib, collections

sys.path.insert(0, os.path.abspath('tools/pastpapers'))
import recurrence_model as RM

MONTHS = RM.MONTHS
S = r'C:/Users/User/AppData/Local/Temp/claude/F--RulesApp/8fd949e3-b943-42c3-a2cf-25535f0b6e97/scratchpad'


def solved_specs():
    out = []
    for f in sorted(glob.glob('meoclass1/pastpapers/specs/QP*.json')):
        d = json.load(open(f, encoding='utf-8'))
        d['_status'] = 'SOLVED'
        out.append(d)
    return out


def historical_specs():
    """Shape the intelligence-only papers like a spec so the governed model can read them."""
    out = []
    for p in json.load(open(S + '/hist_raw.json', encoding='utf-8')):
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
            'paper_id': p['paper_id'], 'year': p['year'], 'month': p['month_name'],
            'month_year': p['sitting'], 'questions': qs, '_status': 'INTELLIGENCE_ONLY',
            'printed_serial': p['printed_serial'], 'second_sitting': p['second_sitting'],
        })
    return out


def main():
    specs = solved_specs() + historical_specs()
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
    json.dump(records, open(S + '/sixyear_families.json', 'w', encoding='utf-8', newline='
'),
              indent=1, ensure_ascii=False)
    json.dump({q: {'status': nodes[q]['status'], 'year': nodes[q]['year'],
                   'month': nodes[q]['month_num'], 'paper': nodes[q]['paper_id'],
                   'q_no': nodes[q]['q_no'], 'stem': nodes[q]['text_verbatim']}
               for q in order},
              open(S + '/sixyear_nodes.json', 'w', encoding='utf-8', newline='
'), indent=1, ensure_ascii=False)

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
