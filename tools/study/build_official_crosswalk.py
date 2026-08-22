#!/usr/bin/env python3
"""Build docs/study/official_crosswalk.json -- official node -> MIW topic.

    official_syllabus.json (25 DGMA nodes)
              |
              |  hand-adjudicated crosswalk (this file)
              v
    study_spine.json (10 canonical MIW topics)

The crosswalk is deliberately hand-adjudicated rather than inferred. Twenty
five nodes is small enough to read, and a keyword matcher over official
regulatory prose invents relationships that are not there -- this project has
been bitten by exactly that before when crude sweeps manufactured false
wording ancestry between papers.

Cardinality is genuinely many-to-many and is not forced to 1:1:

  * one official node -> several MIW topics (node 12 reaches management,
    fire/LSA and machinery);
  * several official nodes -> one MIW topic (D01 carries nodes 3, 6, 7, 9,
    10 and 24).

Roles: PRIMARY is where a candidate should study the node. SUPPORTING is a
real but secondary claim. Every node has exactly one PRIMARY.

Confidence follows the study policy: HIGH may auto-accept, MEDIUM would
normally route to the review queue. Every MEDIUM edge here has instead been
adjudicated by reading the official wording, so it carries an explicit
adjudication stamp rather than sitting unresolved.

Determinism: no clock is read; the source circular's acquisition date is the
temporal anchor.

Usage:
    python tools/study/build_official_crosswalk.py            # write
    python tools/study/build_official_crosswalk.py --check    # fail if stale
"""
import argparse, collections, io, json, os, sys

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import official_syllabus as OS_

OFFICIAL = os.path.join(ROOT, 'docs', 'study', 'official_syllabus.json')
SPINE    = os.path.join(ROOT, 'docs', 'study', 'study_spine.json')
OUT      = os.path.join(ROOT, 'docs', 'study', 'official_crosswalk.json')

ADJUDICATION = 'ADJUDICATED_LAPTOP_2026-08-22'

# official item -> [(topic, role, confidence, basis), ...]
CROSSWALK = {
 1: [('D06', 'PRIMARY',    'HIGH',   'Merchant Shipping Act 2025 and rules framed thereunder are the Indian legislation domain outright'),
     ('D01', 'SUPPORTING', 'HIGH',   'UNCLOS, the IMO role and the major convention set are the statutory framework D01 teaches')],
 2: [('D03', 'PRIMARY',    'HIGH',   'ISM Code, internal auditing, TQM and management systems are the core of the human-element and management domain'),
     ('D01', 'SUPPORTING', 'MEDIUM', 'DOC and SMC are statutory certificates, which D01 owns')],
 3: [('D01', 'PRIMARY',    'HIGH',   'classification societies, class surveys, RO Code and first-entry registration are D01 verbatim')],
 4: [('D10', 'PRIMARY',    'HIGH',   'intact and damage stability, dry-docking stability and the 2008 IS Code are naval architecture'),
     ('D01', 'SUPPORTING', 'MEDIUM', 'SOLAS Chapter II-1 subdivision requirements are statutory')],
 5: [('D06', 'PRIMARY',    'HIGH',   'the Official Log Book is a creature of the Merchant Shipping Act and its rules'),
     ('D01', 'SUPPORTING', 'MEDIUM', 'statutory record-keeping is inspected under the flag and port State system')],
 6: [('D01', 'PRIMARY',    'HIGH',   'statutory certificates, Load Lines, SOLAS and vetting oversight sit in the statutory framework'),
     ('D04', 'SUPPORTING', 'HIGH',   'MARPOL compliance and BWMS commissioning oversight are pollution prevention')],
 7: [('D01', 'PRIMARY',    'HIGH',   'ISPS Code and SOLAS Chapter XI-2 are statutory instruments carried by D01')],
 8: [('D03', 'PRIMARY',    'MEDIUM', 'MLC 2006, seafarer welfare and ill-treatment defence are human element; adjudicated over D01 because the node is dominated by labour and health rather than certification'),
     ('D01', 'SUPPORTING', 'MEDIUM', 'Ship Sanitation and Maritime Labour Certificates are statutory certificates')],
 9: [('D01', 'PRIMARY',    'HIGH',   'Port State Control, flag State duties, MoU regimes and detention are D01 outright')],
10: [('D01', 'PRIMARY',    'HIGH',   'HSSC and the statutory survey types are the survey half of D01')],
11: [('D02', 'PRIMARY',    'HIGH',   'H&M, P&I, charter parties, MIA 1906 and salvage are the commercial law domain verbatim')],
12: [('D03', 'PRIMARY',    'MEDIUM', 'the node is framed as emergency preparedness, risk assessment and ALARP under the ISM Code, which is management; adjudicated over D08'),
     ('D08', 'SUPPORTING', 'HIGH',   'fire main, drainage and emergency systems are fire safety and LSA'),
     ('D09', 'SUPPORTING', 'MEDIUM', 'the named failures -- bearing, turbocharger, boiler tube, lube oil -- are machinery')],
13: [('D03', 'PRIMARY',    'HIGH',   'human relations, leadership, resource management and crisis management are D03 outright')],
14: [('D03', 'PRIMARY',    'HIGH',   'the Chief Engineer as trainer is a human-element competence')],
15: [('D03', 'PRIMARY',    'MEDIUM', 'inventory, ROP and stores management are shipboard management; adjudicated over D09'),
     ('D09', 'SUPPORTING', 'MEDIUM', 'bunker calculation and low-BN cylinder oil selection are machinery decisions')],
16: [('D03', 'PRIMARY',    'MEDIUM', 'the node is explicitly Management Information Systems in ship management'),
     ('D09', 'SUPPORTING', 'HIGH',   'MASS trials, remote operation and sensor technology are automation')],
17: [('D03', 'PRIMARY',    'MEDIUM', 'standing orders, night order book and engine-room record discipline are management practice'),
     ('D04', 'SUPPORTING', 'HIGH',   'the Oil Record Book is a MARPOL instrument')],
18: [('D05', 'PRIMARY',    'MEDIUM', 'fuel economy, low sulphur fuels and change-over are the decarbonisation domain; adjudicated over D09'),
     ('D09', 'SUPPORTING', 'HIGH',   'power balancing, load diagrams and propulsive characteristics are machinery performance')],
19: [('D02', 'PRIMARY',    'MEDIUM', 'budgeting, voyage expenses and dry-dock cost analysis are commercial ship operation'),
     ('D03', 'SUPPORTING', 'MEDIUM', 'downtime reduction is an operational management competence')],
20: [('D09', 'PRIMARY',    'HIGH',   'HV systems, electrical propulsion, PWM and circuit breakers are electrical engineering')],
21: [('D09', 'PRIMARY',    'HIGH',   'engine developments, tribology and propulsion arrangements are machinery'),
     ('D05', 'SUPPORTING', 'HIGH',   'dual-fuel engines and the alternative-fuel supervisory bullets are decarbonisation')],
22: [('D05', 'PRIMARY',    'HIGH',   'GHG, EEXI, CII, carbon capture and MARPOL Annex VI are the decarbonisation domain verbatim'),
     ('D04', 'SUPPORTING', 'MEDIUM', 'MARPOL Annex VI is an air-pollution annex')],
23: [('D09', 'PRIMARY',    'MEDIUM', 'AI, IoT, blockchain and digitalisation are automation and digital systems'),
     ('D03', 'SUPPORTING', 'HIGH',   'cyber-risk management under the ISM Code is explicitly a management-level competence')],
24: [('D01', 'PRIMARY',    'MEDIUM', 'casualty investigation follows the IMO Casualty Investigation Code and is a flag State statutory duty'),
     ('D03', 'SUPPORTING', 'MEDIUM', 'classic casualties are taught through root-cause and human-factor analysis')],
25: [('D04', 'PRIMARY',    'MEDIUM', 'underwater radiated noise is treated by the IMO as marine environmental protection'),
     ('D10', 'SUPPORTING', 'MEDIUM', 'hull form and propeller design are the means of reducing it')],
}

VALID_ROLES = {'PRIMARY', 'SUPPORTING'}
VALID_CONFIDENCE = {'HIGH', 'MEDIUM'}


def build():
    official = json.load(open(OFFICIAL, encoding='utf-8'))
    spine = json.load(open(SPINE, encoding='utf-8'))
    topics = {d['domain_id']: d['name'] for d in spine['domains']}

    nodes = {n['official_number']: n for n in official['nodes']}
    if set(CROSSWALK) != set(nodes):
        missing = sorted(set(nodes) - set(CROSSWALK))
        extra = sorted(set(CROSSWALK) - set(nodes))
        raise SystemExit(f'FAIL R-XWALK-COVER: unmapped={missing} unknown={extra}')

    edges = []
    for number in sorted(CROSSWALK):
        node = nodes[number]
        primaries = [e for e in CROSSWALK[number] if e[1] == 'PRIMARY']
        if len(primaries) != 1:
            raise SystemExit(f'FAIL R-XWALK-PRIMARY: node {number} has '
                             f'{len(primaries)} PRIMARY edges, expected 1')
        for topic, role, confidence, basis in CROSSWALK[number]:
            if topic not in topics:
                raise SystemExit(f'FAIL R-XWALK-TOPIC: node {number} -> unknown topic {topic}')
            if role not in VALID_ROLES or confidence not in VALID_CONFIDENCE:
                raise SystemExit(f'FAIL R-XWALK-ENUM: node {number} {role}/{confidence}')
            edges.append({
                'official_node_id': node['official_node_id'],
                'official_number': number,
                'official_order': node['official_order'],
                'source_page': node['source_page'],
                'topic_id': topic,
                'topic_name': topics[topic],
                'mapping_role': role,
                'mapping_confidence': confidence,
                'mapping_basis': basis,
                'review_status': ADJUDICATION,
                'syllabus_version': OS_.SYLLABUS_VERSION_ADOPTED,
            })

    by_topic = collections.Counter(e['topic_id'] for e in edges)
    primary_by_topic = collections.Counter(
        e['topic_id'] for e in edges if e['mapping_role'] == 'PRIMARY')
    unsupported = sorted(t for t in topics if primary_by_topic.get(t, 0) == 0
                         and by_topic.get(t, 0) == 0)

    return {
        'schema_version': '1.0',
        'generated_by': 'tools/study/build_official_crosswalk.py',
        'authority': ('Hand-adjudicated. Official wording is authoritative as '
                      'to scope; MIW topics are the durable study layer.'),
        'official_source': {
            'circular': official['source']['circular'],
            'annex': official['annex']['annex_id'],
            'sha256': official['source']['sha256'],
            'syllabus_version': OS_.SYLLABUS_VERSION_ADOPTED,
            'effective_from': OS_.EFFECTIVE_FROM,
        },
        'totals': {
            'official_nodes': len(nodes),
            'edges': len(edges),
            'primary_edges': sum(1 for e in edges if e['mapping_role'] == 'PRIMARY'),
            'supporting_edges': sum(1 for e in edges if e['mapping_role'] == 'SUPPORTING'),
            'high_confidence': sum(1 for e in edges if e['mapping_confidence'] == 'HIGH'),
            'medium_confidence': sum(1 for e in edges if e['mapping_confidence'] == 'MEDIUM'),
            'topics_with_official_backing': len(by_topic),
            'topics_without_official_backing': unsupported,
        },
        'edges_by_topic': {t: by_topic.get(t, 0) for t in sorted(topics)},
        'primary_by_topic': {t: primary_by_topic.get(t, 0) for t in sorted(topics)},
        'edges': edges,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    text = json.dumps(build(), indent=2, ensure_ascii=False) + '\n'
    if args.check:
        if not os.path.exists(OUT):
            print('FAIL: docs/study/official_crosswalk.json is missing')
            return 1
        if open(OUT, encoding='utf-8').read() != text:
            print('FAIL: docs/study/official_crosswalk.json is stale')
            return 1
        print('official crosswalk -- up to date')
        return 0

    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    built = json.loads(text)
    print(f'wrote {os.path.relpath(OUT, ROOT)} -- '
          f'{built["totals"]["edges"]} edges over '
          f'{built["totals"]["official_nodes"]} official nodes')
    if built['totals']['topics_without_official_backing']:
        print('  topics with no Annexure III backing: '
              + ', '.join(built['totals']['topics_without_official_backing']))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
