#!/usr/bin/env python3
"""Build docs/study/coverage_matrix.json -- MIW coverage of Annexure III.

For every one of the 25 official nodes, how well do the governed corpora
actually cover it?

    STRONG   broad evidence, present in BOTH the oral and written corpora
    PARTIAL  real evidence, but thin or one-sided
    WEAK     incidental evidence only
    NONE     no evidence found

WHY A PROBE, AND WHY IT IS NOT A MAPPING
----------------------------------------
Questions are mapped to topics, not to official nodes, so topic evidence
alone would give every node sharing a topic the same score -- D01's six nodes
would each inherit all 46 oral questions and read as uniformly STRONG, which
is false. Instead each node carries hand-authored probe terms drawn from its
own official wording.

This probe is DIAGNOSTIC ONLY. It never writes a mapping, never changes a
topic, and nothing downstream may treat a probe hit as a question->node join.
That separation is deliberate: `mapping_engine` decides mappings from
structural evidence precisely because term matching picks wrong parents. A
coverage report is allowed to be approximate in a way a mapping is not.

Coverage measures BREADTH, not question count: a node needs evidence in both
corpora to reach STRONG, so twenty near-duplicate orals cannot manufacture it.

Determinism: no clock is read.

Usage:
    python tools/study/build_coverage_matrix.py            # write
    python tools/study/build_coverage_matrix.py --check    # fail if stale
"""
import argparse, collections, glob, io, json, os, re, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import mapping_engine as ME

OFFICIAL = os.path.join(ROOT, 'docs', 'study', 'official_syllabus.json')
STORE    = os.path.join(ROOT, 'docs', 'study', 'study_mappings.json')
SPECS    = os.path.join(ROOT, 'meoclass1', 'pastpapers', 'specs', '*.json')
EXAMINER = os.path.join(ROOT, 'meoclass1', 'oral-intelligence', 'examiner-audit',
                        'CURRENT_EXAMINER_RELATIONSHIPS.jsonl')
OUT      = os.path.join(ROOT, 'docs', 'study', 'coverage_matrix.json')

# Probe terms per official item, taken from that item's own official wording.
PROBES = {
 1: [r'merchant shipping act', r'\bunclos\b', r'law of the sea', r'imo assembly',
     r'tacit acceptance', r'ratificat', r'flag state.{0,20}imo'],
 2: [r'\bism code\b', r'safety management system', r'\bdoc\b', r'\bsmc\b',
     r'internal audit', r'non.?conformit', r'iso 9001', r'iso 14001',
     r'iso 50001', r'\btqm\b', r'total quality'],
 3: [r'classification societ', r'class survey', r'continuous survey',
     r'enhanced survey', r'recognized organi', r'recognised organi', r'\bro code\b',
     r'withdrawal of class', r'suspension of class', r'\biacs\b',
     r'registration of indian ships', r'open registry', r'transfer of class'],
 4: [r'intact stability', r'damage stability', r'\bis code\b', r'metacentric',
     r'subdivision', r'free surface', r'probabilistic', r'grounding.{0,20}stabilit',
     r'dry.?dock.{0,25}stabilit'],
 5: [r'official log ?book', r'\bolb\b', r'log ?book entr'],
 6: [r'load line', r'\bsire\b', r'\btmsa\b', r'rightship', r'vetting',
     r'statutory certificate', r'bwms commissioning', r'intertanko', r'\bbimco\b',
     r'\bocimf\b', r'ballast water management.{0,20}certificat'],
 7: [r'\bisps\b', r'ship security', r'\bssp\b', r'\bssas\b', r'piracy',
     r'\bxi-2\b', r'citadel', r'security level'],
 8: [r'ship sanitation', r'maritime declaration of health', r'deratting',
     r'\bmlc\b', r'maritime labour', r'\bdmlc\b', r'\bilo\b',
     r'international health regulation', r'human rights', r'repatriation.{0,20}right'],
 9: [r'port state control', r'\bpsc\b', r'memorandum of understanding',
     r'paris mou', r'tokyo mou', r'detention', r'member state audit',
     r'\bimsas\b', r'flag state control'],
10: [r'\bhssc\b', r'harmoni[sz]ed system of survey', r'renewal survey',
     r'intermediate survey', r'annual survey', r'in.?water survey',
     r'periodical survey', r'initial survey'],
11: [r'\bp&i\b', r'protection and indemnity', r'hull and machinery',
     r'charter part', r'general average', r'particular average', r'salvage',
     r'\blof\b', r"lloyd", r'marine insurance', r'bareboat', r'\bclub\b'],
12: [r'emergency response', r'damage control', r'contingency plan',
     r'risk assessment', r'\balarp\b', r'root cause', r'emergency generator',
     r'flooding of', r'emergency preparedness', r'drill'],
13: [r'leadership', r'motivat', r'conflict', r'human error',
     r'situational awareness', r'delegat', r'cross.?cultural', r'fatigue',
     r'harassment', r'psychological safety', r'team.?work', r'crisis management',
     r'resource management'],
14: [r'training need', r'instructional', r'mentor', r'counsell?ing',
     r'on.?board training', r'\btrainer\b', r'familiaris'],
15: [r'inventory', r'\bspares?\b', r're.?order', r'safety stock', r'\bstores\b',
     r'bunker requirement', r'low bn', r'cylinder oil consumption'],
16: [r'management information system', r'decision support', r'expert system',
     r'\bmass\b', r'autonomous', r'remote operation', r'e.?certificat',
     r'sensor technolog'],
17: [r'oil record book', r'\borb\b', r'standing order', r'night order',
     r'engine ?room log', r'record keeping'],
18: [r'fuel consumption', r'iso 8217', r'low sulphur', r'change.?over',
     r'bunker management', r'load diagram', r'specific fuel', r'fuel economy',
     r'power balanc'],
19: [r'budget', r'cost control', r'voyage expense', r'dry.?dock.{0,15}cost',
     r'canal toll', r'port charge', r'downtime', r'operating cost',
     r'cost.{0,10}benefit'],
20: [r'high voltage', r'\bhv\b', r'busbar', r'insulation resistance',
     r'circuit breaker', r'vacuum circuit', r'azipod', r'electrical propulsion',
     r'pulse width', r'synchronous motor'],
21: [r'camshaft', r'common rail', r'electronically controlled engine',
     r'dual.?fuel', r'tribolog', r'alpha lubricat', r'contra.?rotating',
     r'water ?jet', r'\bpto\b', r'\bpti\b', r'turbo ?alternator',
     r'wake equali[sz]ing', r'cylinder lubricat'],
22: [r'\bghg\b', r'greenhouse', r'\beexi\b', r'\bcii\b', r'carbon intensity',
     r'carbon capture', r'annex vi', r'decarboni[sz]', r'net.?zero',
     r'fouling', r'coating', r'carbon.?neutral'],
23: [r'artificial intelligence', r'\bai\b', r'\biot\b', r'blockchain',
     r'digitali[sz]', r'smart ship', r'predictive maintenance', r'cyber'],
24: [r'casualty investigation', r'casualty code', r'marine casualty',
     r'accident investigation', r'\bmaib\b', r'very serious casualty'],
25: [r'underwater noise', r'radiated noise', r'underwater radiated'],
}


def compile_probes():
    return {n: [re.compile(p, re.I) for p in pats] for n, pats in PROBES.items()}


def classify(oral, written):
    total = oral + written
    if total == 0:
        return 'NONE'
    if total >= 10 and oral >= 2 and written >= 2:
        return 'STRONG'
    if total >= 4:
        return 'PARTIAL'
    return 'WEAK'


def build():
    official = json.load(open(OFFICIAL, encoding='utf-8'))
    store = json.load(open(STORE, encoding='utf-8'))['mappings']
    probes = compile_probes()

    if set(PROBES) != {n['official_number'] for n in official['nodes']}:
        raise SystemExit('FAIL R-COVER-PROBE: probe set does not cover every '
                         'official node exactly')

    oral_texts = {qid: (r.get('text') or '')
                  for qid, r in store.items() if r['content_type'] == 'ORAL'}

    written_texts = {}
    for path in sorted(glob.glob(SPECS)):
        spec = json.load(open(path, encoding='utf-8'))
        for q in spec['questions']:
            blob = ' '.join(filter(None, [
                q.get('short_title'), q.get('text_verbatim'),
                ' '.join(q.get('subject_tags') or []),
                ' '.join(q.get('topic_tags') or []),
                ' '.join(q.get('search_aliases') or []),
            ]))
            written_texts[f"{spec['paper_id']}-{q['q_no']}"] = blob

    # examiner reach, counted over oral hits only (examiners are an oral signal)
    ex_by_q = collections.defaultdict(set)
    if os.path.exists(EXAMINER):
        for line in open(EXAMINER, encoding='utf-8'):
            line = line.strip()
            if not line:
                continue
            rel = json.loads(line)
            qid = rel.get('question_id') or rel.get('id')
            name = rel.get('examiner') or rel.get('examiner_name')
            if qid and name:
                ex_by_q[qid].add(name)

    rows = []
    for node in official['nodes']:
        n = node['official_number']
        pats = probes[n]
        o_hits = sorted(q for q, t in oral_texts.items()
                        if any(p.search(t) for p in pats))
        w_hits = sorted(q for q, t in written_texts.items()
                        if any(p.search(t) for p in pats))
        examiners = sorted({e for q in o_hits for e in ex_by_q.get(q, ())})
        primary = [e['topic_id'] for e in ME.official_crosswalk()['edges']
                   if e['official_number'] == n and e['mapping_role'] == 'PRIMARY']
        rows.append({
            'official_node_id': node['official_node_id'],
            'official_number': n,
            'primary_topic': primary[0] if primary else None,
            'coverage': classify(len(o_hits), len(w_hits)),
            'oral_evidence': len(o_hits),
            'written_evidence': len(w_hits),
            'examiners': len(examiners),
            'examiner_names': examiners,
            'oral_examples': o_hits[:8],
            'written_examples': w_hits[:8],
            'subject': node['official_text'][:110].rstrip() + '...',
        })

    dist = collections.Counter(r['coverage'] for r in rows)
    if len(rows) != len(official['nodes']):
        raise SystemExit('FAIL R-COVER-ACCOUNT: not every official node scored')

    return {
        'schema_version': '1.0',
        'generated_by': 'tools/study/build_coverage_matrix.py',
        'authority': ('DIAGNOSTIC ONLY. Probe hits are evidence of coverage, '
                      'never a question-to-node mapping.'),
        'official_source': {
            'circular': official['source']['circular'],
            'annex': official['annex']['annex_id'],
            'sha256': official['source']['sha256'],
            'syllabus_version': ME.OFFICIAL_VERSION,
        },
        'method': {
            'oral_corpus': len(oral_texts),
            'written_corpus': len(written_texts),
            'rule': ('STRONG = >=10 hits with >=2 in each corpus; '
                     'PARTIAL = >=4; WEAK = 1-3; NONE = 0'),
        },
        'distribution': {k: dist.get(k, 0)
                         for k in ('STRONG', 'PARTIAL', 'WEAK', 'NONE')},
        'nodes': rows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    text = json.dumps(build(), indent=2, ensure_ascii=False) + '\n'
    if args.check:
        if not os.path.exists(OUT) or open(OUT, encoding='utf-8').read() != text:
            print('FAIL: docs/study/coverage_matrix.json is missing or stale')
            return 1
        print('coverage matrix -- up to date')
        return 0

    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    built = json.loads(text)
    print(f'wrote {os.path.relpath(OUT, ROOT)}')
    print('  ' + json.dumps(built['distribution']))
    for r in built['nodes']:
        print(f"  {r['official_node_id']} {r['coverage']:8s} "
              f"oral={r['oral_evidence']:3d} written={r['written_evidence']:3d} "
              f"examiners={r['examiners']:2d} -> {r['primary_topic']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
