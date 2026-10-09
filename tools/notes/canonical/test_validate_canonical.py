#!/usr/bin/env python3
"""Mutation tests for validate_canonical.py (POST31-CA2).

WHY THESE ARE NOT VACUOUS

A mutation harness proves nothing if a mutation silently fails to apply, or if the
validator fails for an unrelated reason. (The gap0609 harness was exactly that.) So
every case here:

  1. applies its mutation to a deep copy of the REAL registry / rendered scan;
  2. runs a `proof` predicate that must be FALSE on the unmutated data and TRUE on the
     mutated data, so the intended condition demonstrably changed;
  3. requires the validator to report the SPECIFIC error code(s) for that rule (all of
     them), not just "some failure".

The unmutated control (M8) must pass with zero errors, and the positive case (rule 8,
same anchor string in two files) must also pass. Nothing is written to disk.

Run:  PYTHONIOENCODING=utf-8 python tools/notes/canonical/test_validate_canonical.py [--json OUT]
"""
from __future__ import annotations

import copy
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate_canonical as V  # noqa: E402

P = 'meoclass1/oralnotes/miw-notes-mgmt-p'
K_BWM = f'{P}12.html#topic-51'          # P12 local "Topic 2"
K_P1_T2 = f'{P}1.html#topic-2'          # the same-NUMBER global anchor (a real node)
K_HNS = f'{P}4.html#topic-16'


def _row(reg, key):
    return next(r for r in reg['source_nodes'] if r['source_node_key'] == key)


def _alias(reg, key, typ):
    return next(r for r in reg['aliases'] if r['source_node_key'] == key and r['alias_type'] == typ)


def _keys(reg):
    return [r['source_node_key'] for r in reg['source_nodes']]


def _lookup_size(reg, typ, val):
    return len({r['source_node_key'] for r in reg['aliases'] if r['alias_type'] == typ and r['alias_value'] == val})


# ------------------------------------------------------------------ mutations
# each: (id, description, mutate(reg, rendered, live), proof(reg, rendered, live), expected_codes)

def m1(reg, ren, live):
    _row(reg, K_BWM)['source_node_key'] = 'topic-51'


def m1b(reg, ren, live):
    _row(reg, K_BWM)['source_node_key'] = '#topic-51'


def m2(reg, ren, live):
    reg['source_nodes'].append(dict(_row(reg, K_HNS)))


def m3(reg, ren, live):
    reg['aliases'].append({'source_node_key': f'{P}12.html#topic-52', 'alias_type': 'phase1a_key',
                           'alias_value': 'U-P12-T02', 'source': 'mutation'})


def m3b(reg, ren, live):
    reg['aliases'].append({'source_node_key': f'{P}12.html#topic-52', 'alias_type': 'toc',
                           'alias_value': 'T2', 'source': 'rendered:toc-link'})


def m4(reg, ren, live):
    r = dict(_row(reg, K_BWM))
    r.update(source_node_key=f'{P}12.html#topic-99', anchor='topic-99', ordinal_in_part='6')
    reg['source_nodes'].append(r)


def m5(reg, ren, live):
    reg['source_nodes'] = [r for r in reg['source_nodes'] if r['source_node_key'] != K_HNS]
    reg['aliases'] = [r for r in reg['aliases'] if r['source_node_key'] != K_HNS]


def m6(reg, ren, live):
    # The P12 trap: local "P12-T2" mapped to the same-number GLOBAL anchor #topic-2,
    # which is a real, resolvable node in Part 1. Resolution alone would not catch it.
    _alias(reg, K_BWM, 'version')['source_node_key'] = K_P1_T2


def m6b(reg, ren, live):
    _alias(reg, K_BWM, 'phase1a_key')['source_node_key'] = K_P1_T2


def m7(reg, ren, live):
    reg['inbound'][0]['target_source_node_key'] = f'{P}12.html#topic-99'


def m7b(reg, ren, live):
    live[('meoclass1/some-referrer.html', f'{P}12.html#topic-99')] += 1


def m9(reg, ren, live):
    reg['status']['STATUS-BWM']['consumers'].append({'source_node_key': 'U-P12-T02', 'role': 'mutation'})


def m9b(reg, ren, live):
    reg['inbound'][0]['target_source_node_key'] = 'P12-T2'


def m10(reg, ren, live):
    reg['raw_text']['source_nodes.csv'] += '\nMERGE-045'


def m11(reg, ren, live):
    lohan = 'meoclass1/oralnotes/lohan-notes-p13.html#topic-p13-4'
    r = dict(_row(reg, K_BWM))
    r.update(source_node_key=lohan, file=lohan.split('#')[0], anchor='topic-p13-4')
    reg['source_nodes'].append(r)
    reg['raw_text']['source_nodes.csv'] += '\n' + lohan


def m12(reg, ren, live):
    ren[f'{P}31.html']['topics'].append({'anchor': 'topic-p31-4', 'title': 'New unregistered topic',
                                         'badge': 'Part 31 · Topic 4', 'version': 'P31-T4', 'toc': 'T4'})


def m13(reg, ren, live):
    reg['status']['STATUS-ECA'] = copy.deepcopy(reg['status']['STATUS-BWM'])
    reg['status']['STATUS-ECA']['status_id'] = 'STATUS-ECA'


def m14(reg, ren, live):
    reg['status']['STATUS-NZF']['consumers'].append({'source_node_key': f'{P}22.html#topic-p22-9', 'role': 'mutation'})


def m15(reg, ren, live):
    reg['aliases'].append({'source_node_key': K_BWM, 'alias_type': 'phase1a_key',
                           'alias_value': 'topic-51', 'source': 'mutation'})


def m16(reg, ren, live):
    _alias(reg, K_BWM, 'badge')['alias_value'] = 'Topic 51'


def m17(reg, ren, live):
    del reg['status']['STATUS-HNS2010']['as_of']


CASES = [
    ('M1', 'strip file from a source key (anchor-only identity)', m1,
     lambda reg, ren, live: 'topic-51' in _keys(reg), {'KEY_WITHOUT_FILE'}),
    ('M1b', 'empty file component (#anchor)', m1b,
     lambda reg, ren, live: '#topic-51' in _keys(reg), {'KEY_WITHOUT_FILE'}),
    ('M2', 'duplicate source_node_key', m2,
     lambda reg, ren, live: Counter(_keys(reg))[K_HNS] == 2, {'DUPLICATE_KEY'}),
    ('M3', 'global alias points to two nodes', m3,
     lambda reg, ren, live: _lookup_size(reg, 'phase1a_key', 'U-P12-T02') == 2, {'ALIAS_AMBIGUOUS'}),
    ('M3b', 'page-scoped alias points to two nodes in one file', m3b,
     lambda reg, ren, live: len({r['source_node_key'] for r in reg['aliases'] if r['alias_type'] == 'toc' and r['alias_value'] == 'T2' and r['source_node_key'].startswith(f'{P}12.html#')}) == 2,
     {'ALIAS_AMBIGUOUS'}),
    ('M4', 'register a nonexistent anchor', m4,
     lambda reg, ren, live: f'{P}12.html#topic-99' in _keys(reg) and 'topic-99' not in {t['anchor'] for t in ren[f'{P}12.html']['topics']},
     {'KEY_NOT_RENDERED'}),
    ('M5', 'remove a rendered topic from source_nodes', m5,
     lambda reg, ren, live: K_HNS not in _keys(reg) and 'topic-16' in {t['anchor'] for t in ren[f'{P}4.html']['topics']},
     {'RENDERED_NOT_REGISTERED'}),
    ('M6', 'P12 local version label mapped to same-number global anchor #topic-2 (a real node)', m6,
     lambda reg, ren, live: any(r['alias_value'] == 'P12-T2' and r['source_node_key'] == K_P1_T2 for r in reg['aliases']) and K_P1_T2 in _keys(reg),
     {'P12_LOCAL_TO_WRONG_ANCHOR'}),
    ('M6b', 'P12 Phase 1A key mapped to same-number global anchor', m6b,
     lambda reg, ren, live: any(r['alias_value'] == 'U-P12-T02' and r['source_node_key'] == K_P1_T2 for r in reg['aliases']),
     {'P12_LOCAL_TO_WRONG_ANCHOR'}),
    ('M7', 'broken inbound baseline target', m7,
     lambda reg, ren, live: reg['inbound'][0]['target_source_node_key'] == f'{P}12.html#topic-99', {'INBOUND_BROKEN'}),
    ('M7b', 'broken live inbound reference', m7b,
     lambda reg, ren, live: live[('meoclass1/some-referrer.html', f'{P}12.html#topic-99')] == 1, {'LIVE_INBOUND_BROKEN'}),
    ('M9', 'status consumer given as an alias, not a key', m9,
     lambda reg, ren, live: any(c['source_node_key'] == 'U-P12-T02' for c in reg['status']['STATUS-BWM']['consumers']),
     {'ALIAS_USED_AS_KEY'}),
    ('M9b', 'inbound target given as an alias', m9b,
     lambda reg, ren, live: reg['inbound'][0]['target_source_node_key'] == 'P12-T2', {'ALIAS_USED_AS_KEY'}),
    ('M10', 'MERGE-### subject id enters the data', m10,
     lambda reg, ren, live: 'MERGE-045' in reg['raw_text']['source_nodes.csv'], {'FORBIDDEN_SUBJECT_ID'}),
    ('M11', 'LOHAN source node enters the data', m11,
     lambda reg, ren, live: any('lohan-notes' in k for k in _keys(reg)), {'LOHAN_ROW'}),
    ('M12', 'new rendered topic-block not registered', m12,
     lambda reg, ren, live: any(t['anchor'] == 'topic-p31-4' for t in ren[f'{P}31.html']['topics']), {'RENDERED_NOT_REGISTERED'}),
    ('M13', 'unapproved status core added', m13,
     lambda reg, ren, live: 'STATUS-ECA' in reg['status'], {'STATUS_NOT_APPROVED'}),
    ('M14', 'status consumer does not resolve', m14,
     lambda reg, ren, live: any(c['source_node_key'].endswith('#topic-p22-9') for c in reg['status']['STATUS-NZF']['consumers']),
     {'STATUS_CONSUMER_UNRESOLVED'}),
    ('M15', 'alias value equal to an anchor string (alias becoming a key)', m15,
     lambda reg, ren, live: any(r['alias_value'] == 'topic-51' for r in reg['aliases']), {'ALIAS_IS_ANCHOR'}),
    ('M16', 'P12 badge alias rewritten to a global-style label the page does not render', m16,
     lambda reg, ren, live: _alias(reg, K_BWM, 'badge')['alias_value'] == 'Topic 51', {'ALIAS_NOT_OBSERVED'}),
    ('M17', 'status record loses a required field', m17,
     lambda reg, ren, live: 'as_of' not in reg['status']['STATUS-HNS2010'], {'STATUS_FIELD_MISSING'}),
]


def positive_rule8(reg, ren):
    """Same anchor string in two different files must be PERMITTED (keys include the file)."""
    reg, ren = copy.deepcopy(reg), copy.deepcopy(ren)
    f99 = f'{P}99.html'
    ren[f99] = {'part': 99, 'ids': {'topic-p13-1'}, 'topics': [
        {'anchor': 'topic-p13-1', 'title': 'Synthetic collision fixture', 'badge': 'Part 99 · Topic 1',
         'version': 'P99-T1', 'toc': 'T1'}]}
    k = f'{f99}#topic-p13-1'
    reg['source_nodes'].append({'source_node_key': k, 'series': 'UDAY', 'file': f99, 'anchor': 'topic-p13-1',
                                'part': '99', 'ordinal_in_part': '1', 'title': 'Synthetic collision fixture',
                                'anchor_scheme': 'PART_LOCAL', 'publication_status': 'PUBLISHED_LIVE',
                                'source_commit': reg['source_nodes'][0]['source_commit']})
    for typ, val in (('badge', 'Part 99 · Topic 1'), ('toc', 'T1'), ('version', 'P99-T1')):
        reg['aliases'].append({'source_node_key': k, 'alias_type': typ, 'alias_value': val,
                               'source': V.RENDERED_ALIAS_SOURCE[typ]})
    holders = [x for x in V.load_registry()[0]['source_nodes'] if x['anchor'] == 'topic-p13-1']
    proof = len({r['file'] for r in reg['source_nodes'] if r['anchor'] == 'topic-p13-1'}) == 2 and len(holders) == 1
    errs = V.validate(reg, ren, None)
    return proof, errs


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    out_json = argv[argv.index('--json') + 1] if '--json' in argv else None
    base_reg, load_errs = V.load_registry()
    base_ren = V.scan_rendered()
    base_live = V.scan_inbound()
    results, failures = [], 0

    def record(cid, desc, ok, detail):
        nonlocal failures
        failures += 0 if ok else 1
        results.append({'id': cid, 'description': desc, 'result': 'PASS' if ok else 'FAIL', **detail})
        print(f"{'PASS' if ok else 'FAIL'}  {cid:5} {desc}  {detail.get('summary', '')}")

    # M8 — unmutated control
    ctrl = V.validate(copy.deepcopy(base_reg), copy.deepcopy(base_ren), Counter(base_live))
    record('M8', 'unmutated control must PASS', not load_errs and not ctrl,
           {'summary': f'errors={len(load_errs) + len(ctrl)}', 'errors': [list(e) for e in load_errs + ctrl]})
    if load_errs or ctrl:
        for e in load_errs + ctrl:
            print('   control error:', e)

    for cid, desc, mutate, proof, expected in CASES:
        reg, ren, live = copy.deepcopy(base_reg), copy.deepcopy(base_ren), Counter(base_live)
        before = proof(reg, ren, live)
        mutate(reg, ren, live)
        after = proof(reg, ren, live)
        changed = (reg != base_reg) or (ren != base_ren) or (live != base_live)
        errs = V.validate(reg, ren, live)
        codes = sorted({c for c, _ in errs})
        hit = sorted(expected & set(codes))
        ok = (not before) and after and changed and expected <= set(codes)
        record(cid, desc, ok, {'summary': f'proof {before}->{after}; required {sorted(expected)}; got {codes}',
                               'proof_before': before, 'proof_after': after, 'data_changed': changed,
                               'expected_codes': sorted(expected), 'reported_codes': codes,
                               'matched_codes': hit, 'n_errors': len(errs)})

    proof8, errs8 = positive_rule8(base_reg, base_ren)
    record('R8+', 'same anchor string in two files is permitted (positive)', proof8 and not errs8,
           {'summary': f'proof={proof8}; errors={len(errs8)}', 'errors': [list(e) for e in errs8]})

    total = len(results)
    print(f'{total - failures}/{total} mutation/control cases PASS')
    if out_json:
        with open(out_json, 'w', encoding='utf-8') as fh:
            json.dump({'cases': results, 'pass': total - failures, 'total': total}, fh, ensure_ascii=False, indent=1)
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
