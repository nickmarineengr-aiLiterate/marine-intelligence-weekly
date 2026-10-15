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

POST31 LOHAN SOURCE ADMISSION adds the L-series. LOHAN pages are absent from production
until D-L4, so every L case runs in a declared MODE and is meaningful in either checkout:

  absent  : no LOHAN page in the tree (production reality); rows are checked structurally.
  present : LOHAN pages in the tree (the simulated admitted tree); rows are checked node by
            node and the live LOHAN->Uday references must equal the baseline. If the checkout
            has no real LOHAN pages, the rendered pages and live references are synthesised
            in memory from the registry rows, so the case still runs.
  real    : exactly what the checkout contains (all pre-existing M cases).

Audit F3 (reverse-reference isolation) adds the R-series: Uday-series source files referring to
LOHAN pages. Each R case must report EXACTLY its expected codes, and RA cases temporarily
authorise the UDAY->LOHAN direction to prove the rule is registration, not a blanket ban.

D-L4 governance (11 Oct 2026) adds the S-series: the declared LOHAN_SERIES_STATE against the activation
evidence (manifest, index, exact gate). L7 is no longer pinned to UNPUBLISHED: it flips one row to the
status the DECLARED state forbids, so it stays meaningful before and after the D-F flip. The SC cases
are the three valid states and must PASS; every other S case must report EXACTLY its codes.

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


LP = 'meoclass1/oralnotes/lohan-notes-p'
K_L13_4 = f'{LP}13.html#topic-p13-4'
K_L1_1 = f'{LP}1.html#topic-p1-1'


def _lohan_rows(reg):
    return [r for r in reg['source_nodes'] if r['series'] == 'LOHAN']


def _is_lohan_referrer(path):
    return V.referrer_series(path)[0] == 'LOHAN'


def _strip_lohan(ren, live):
    ren = {f: v for f, v in ren.items() if v.get('series') != 'LOHAN'}
    live = Counter({k: n for k, n in live.items() if not _is_lohan_referrer(k[0])})
    return ren, live


def _synth_lohan(reg):
    """In-memory LOHAN rendered pages + live references derived from the registry rows."""
    ren = {}
    for r in sorted(_lohan_rows(reg), key=lambda r: (int(r['part']), int(r['ordinal_in_part']))):
        pg = ren.setdefault(r['file'], {'series': 'LOHAN', 'part': int(r['part']), 'topics': [], 'ids': set()})
        pg['topics'].append({'anchor': r['anchor'], 'title': r['title'], 'badge': '', 'version': '', 'toc': ''})
        pg['ids'].add(r['anchor'])
    live = Counter()
    for r in reg['inbound']:
        if _is_lohan_referrer(r['referrer_file']):
            live[(r['referrer_file'], r['target_source_node_key'])] += int(r['count'])
    return ren, live


def make_modes(reg, real_ren, real_live):
    """Return {mode: (ren, live)} and whether real LOHAN pages were present in this checkout."""
    have_real = any(v.get('series') == 'LOHAN' for v in real_ren.values())
    ren_a, live_a = _strip_lohan(real_ren, real_live)
    if have_real:
        ren_p = {f: v for f, v in real_ren.items()}
        live_p = Counter(real_live)
    else:
        sren, slive = _synth_lohan(reg)
        ren_p = dict(ren_a, **sren)
        live_p = Counter(live_a) + slive
    return {'real': (real_ren, real_live), 'absent': (ren_a, live_a), 'present': (ren_p, live_p)}, have_real


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
    # LOHAN admission is narrowed by FILE SCOPE: a LOHAN page named in any data file other
    # than source_nodes.csv / inbound_baseline.csv (here the alias table) is still LOHAN_ROW.
    reg['raw_text']['display_aliases.csv'] += '\n' + K_L13_4


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
    ('M11', 'LOHAN page named in a non-admitting data file (aliases) is still refused', m11,
     lambda reg, ren, live: 'lohan-notes' in reg['raw_text']['display_aliases.csv'], {'LOHAN_ROW'}),
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


def _lrow(reg, key=K_L13_4):
    return next(r for r in reg['source_nodes'] if r['source_node_key'] == key)


def _lib(reg, pred):
    return [r for r in reg['inbound'] if pred(r)]


def l1(reg, ren, live):
    reg['source_nodes'].append(dict(_lrow(reg)))


def l2(reg, ren, live):
    _lrow(reg)['source_node_key'] = 'topic-p13-4'


def l3(reg, ren, live):  # page/anchor-part mismatch: file p3 with an anchor of part 4
    r = _lrow(reg, f'{LP}3.html#topic-p3-1')
    r['source_node_key'] = f'{LP}3.html#topic-p4-1'
    r['anchor'] = 'topic-p4-1'


def l3b(reg, ren, live):  # Uday-style anchor under a LOHAN file
    r = _lrow(reg)
    r['source_node_key'] = f'{LP}13.html#topic-51'
    r['anchor'] = 'topic-51'


def l4(reg, ren, live):
    r = dict(_lrow(reg))
    r.update(source_node_key=f'{LP}22.html#topic-p22-1', file=f'{LP}22.html', anchor='topic-p22-1',
             part='22', ordinal_in_part='1')
    reg['source_nodes'].append(r)


def l5(reg, ren, live):
    _lrow(reg)['series'] = 'SONY'


def l6(reg, ren, live):
    _lrow(reg)['series'] = 'UDAY'


def l6b(reg, ren, live):
    _row(reg, K_HNS)['series'] = 'LOHAN'


def _forbidden_lohan_status():
    """The status the DECLARED state forbids (so L7 stays meaningful before and after D-F)."""
    return V.UNPUBLISHED_STATUS if V.required_status('LOHAN') == V.PUBLICATION_STATUS else V.PUBLICATION_STATUS


def l7(reg, ren, live):
    _lrow(reg)['publication_status'] = _forbidden_lohan_status()


def l7b(reg, ren, live):
    for r in _lohan_rows(reg):
        r['publication_status'] = _forbidden_lohan_status()


def l8(reg, ren, live):
    reg['source_nodes'] = [r for r in reg['source_nodes'] if r['source_node_key'] != K_L13_4]


def l9(reg, ren, live):  # a 124th LOHAN node on an admitted page
    r = dict(_lrow(reg))
    r.update(source_node_key=f'{LP}13.html#topic-p13-99', anchor='topic-p13-99', ordinal_in_part='99')
    reg['source_nodes'].append(r)


def l10(reg, ren, live):
    ren[f'{LP[:LP.rindex("/") + 1]}lohan-notes-p13.html']['topics'].append(
        {'anchor': 'topic-p13-99', 'title': 'Unregistered LOHAN topic', 'badge': '', 'version': '', 'toc': ''})


def l11(reg, ren, live):
    _lrow(reg)['title'] = 'A stale title the page no longer renders'


def l11b(reg, ren, live):
    pg = ren[f'{LP[:LP.rindex("/") + 1]}lohan-notes-p13.html']
    pg['topics'] = [t for t in pg['topics'] if t['anchor'] != 'topic-p13-4']


def l12(reg, ren, live):
    ren[f'{LP[:LP.rindex("/") + 1]}lohan-notes-p22.html'] = {'series': 'LOHAN', 'part': 22, 'ids': {'topic-p22-1'},
        'topics': [{'anchor': 'topic-p22-1', 'title': 'Unadmitted page', 'badge': '', 'version': '', 'toc': ''}]}


def l13(reg, ren, live):
    reg['aliases'].append({'source_node_key': K_L13_4, 'alias_type': 'phase1a_key',
                           'alias_value': 'LOHAN-P13-T04', 'source': 'mutation'})


def l14(reg, ren, live):
    reg['inbound'][0]['target_source_node_key'] = K_L13_4


def l15(reg, ren, live):
    reg['status']['STATUS-BWM']['consumers'].append({'source_node_key': K_L13_4, 'role': 'mutation'})


def l15b(reg, ren, live):
    reg['status']['STATUS-BWM']['teaching_hub'] = K_L13_4


def l16(reg, ren, live):
    r = dict(next(x for x in reg['inbound'] if _is_lohan_referrer(x['referrer_file'])))
    r['referrer_file'] = f'{LP}22.html'
    reg['inbound'].append(r)


def l16b(reg, ren, live):
    r = dict(next(x for x in reg['inbound'] if _is_lohan_referrer(x['referrer_file'])))
    r['referrer_file'] = 'tools/notes/specs/lohan/extra.json'
    reg['inbound'].append(r)


def l17(reg, ren, live):
    next(x for x in reg['inbound'] if _is_lohan_referrer(x['referrer_file']))['target_source_node_key'] = f'{P}12.html#topic-99'


def l18(reg, ren, live):
    reg['raw_text']['status/STATUS-NZF.json'] += ' ' + K_L1_1


def l19(reg, ren, live):
    reg['raw_text']['source_nodes.csv'] += '\nMERGE-045'


def l19b(reg, ren, live):
    reg['raw_text']['inbound_baseline.csv'] += '\nPCT-BWM-LIABILITY'


def l21(reg, ren, live):
    k = next(k for k in live if _is_lohan_referrer(k[0]))
    live[k] += 1


def l21b(reg, ren, live):
    victim = next(r for r in reg['inbound'] if _is_lohan_referrer(r['referrer_file']))
    reg['inbound'] = [r for r in reg['inbound'] if r is not victim]


def l22(reg, ren, live):
    tgt = next(r['target_source_node_key'] for r in reg['inbound'] if _is_lohan_referrer(r['referrer_file']))
    live[(f'{LP}22.html', tgt)] += 1


def l23(reg, ren, live):
    _lrow(reg)['source_commit'] = '43441b7'


def l24(reg, ren, live):
    _lrow(reg)['part'] = '14'


def l25(reg, ren, live):
    _lrow(reg)['anchor_scheme'] = 'GLOBAL'


def l26(reg, ren, live):
    _lrow(reg)['file'] = f'{LP}12.html'


def l27(reg, ren, live):
    _lrow(reg)['ordinal_in_part'] = '9'


def _n_lohan(reg):
    return len(_lohan_rows(reg))


LCASES = [  # (id, description, mode, mutate, proof, expected codes)
    ('L1', 'duplicate LOHAN source key', 'absent', l1,
     lambda reg, ren, live: Counter(_keys(reg))[K_L13_4] == 2, {'DUPLICATE_KEY', 'LOHAN_ADMISSION_COUNT'}),
    ('L2', 'anchor-only LOHAN identity (file stripped)', 'absent', l2,
     lambda reg, ren, live: 'topic-p13-4' in _keys(reg), {'KEY_WITHOUT_FILE'}),
    ('L3', 'malformed LOHAN row: file p3 with a part-4 anchor', 'absent', l3,
     lambda reg, ren, live: f'{LP}3.html#topic-p4-1' in _keys(reg), {'KEY_MALFORMED'}),
    ('L3b', 'malformed LOHAN row: Uday-style anchor under a LOHAN file', 'absent', l3b,
     lambda reg, ren, live: f'{LP}13.html#topic-51' in _keys(reg), {'KEY_MALFORMED'}),
    ('L4', 'unregistered LOHAN page (p22) in the registry', 'absent', l4,
     lambda reg, ren, live: f'{LP}22.html#topic-p22-1' in _keys(reg), {'LOHAN_PAGE_UNREGISTERED', 'LOHAN_ADMISSION_COUNT'}),
    ('L5', 'unknown source series on a LOHAN row', 'absent', l5,
     lambda reg, ren, live: _lrow(reg)['series'] == 'SONY', {'UNKNOWN_SERIES'}),
    ('L6', 'LOHAN file labelled UDAY (series/file mismatch)', 'absent', l6,
     lambda reg, ren, live: _lrow(reg)['series'] == 'UDAY', {'BAD_SERIES'}),
    ('L6b', 'Uday file labelled LOHAN (collision with the other series)', 'absent', l6b,
     lambda reg, ren, live: _row(reg, K_HNS)['series'] == 'LOHAN', {'BAD_SERIES', 'LOHAN_ADMISSION_COUNT'}),
    # L7 (D-L4 governance): no longer pinned to UNPUBLISHED. One LOHAN row carries the status its
    # declared LOHAN_SERIES_STATE forbids (PUBLISHED_LIVE while unactivated/preview, or the reverse
    # once D-F declares PUBLISHED_LIVE), so the series is both wrong and mixed.
    ('L7', 'one LOHAN row claims the status its declared state forbids (wrong and mixed)', 'absent', l7,
     lambda reg, ren, live: _lrow(reg)['publication_status'] == _forbidden_lohan_status(),
     {'BAD_PUBLICATION_STATUS', 'LOHAN_STATUS_MIXED'}),
    ('L7b', 'every LOHAN row claims the forbidden status (uniform, still wrong for the declared state)', 'absent', l7b,
     lambda reg, ren, live: all(r['publication_status'] == _forbidden_lohan_status() for r in _lohan_rows(reg)),
     {'BAD_PUBLICATION_STATUS'}),
    ('L8', 'a LOHAN source row is dropped (122 of 123)', 'absent', l8,
     lambda reg, ren, live: _n_lohan(reg) == 122, {'LOHAN_ADMISSION_COUNT'}),
    ('L9', 'a 124th LOHAN node appears on an admitted page', 'absent', l9,
     lambda reg, ren, live: _n_lohan(reg) == 124, {'LOHAN_ADMISSION_COUNT'}),
    ('L10', 'LOHAN page in the tree renders a topic-block that is not registered', 'present', l10,
     lambda reg, ren, live: any(t['anchor'] == 'topic-p13-99' for f, v in ren.items() if f.endswith('lohan-notes-p13.html') for t in v['topics']),
     {'RENDERED_NOT_REGISTERED'}),
    ('L11', 'LOHAN row title no longer matches the rendered page', 'present', l11,
     lambda reg, ren, live: _lrow(reg)['title'].startswith('A stale title'), {'TITLE_MISMATCH'}),
    ('L11b', 'registered LOHAN node is not rendered on its page', 'present', l11b,
     lambda reg, ren, live: not any(t['anchor'] == 'topic-p13-4' for f, v in ren.items() if f.endswith('lohan-notes-p13.html') for t in v['topics']),
     {'KEY_NOT_RENDERED'}),
    ('L12', 'unadmitted LOHAN page appears in the tree', 'present', l12,
     lambda reg, ren, live: any(f.endswith('lohan-notes-p22.html') for f in ren), {'LOHAN_PAGE_UNREGISTERED', 'RENDERED_NOT_REGISTERED'}),
    ('L13', 'cross-series: alias targets a LOHAN node', 'absent', l13,
     lambda reg, ren, live: any(r['source_node_key'] == K_L13_4 for r in reg['aliases']), {'CROSS_SERIES_REFERENCE'}),
    ('L14', 'cross-series: inbound row targets a LOHAN node', 'absent', l14,
     lambda reg, ren, live: reg['inbound'][0]['target_source_node_key'] == K_L13_4, {'CROSS_SERIES_REFERENCE'}),
    ('L15', 'cross-series: status core consumer is a LOHAN node', 'absent', l15,
     lambda reg, ren, live: any(c['source_node_key'] == K_L13_4 for c in reg['status']['STATUS-BWM']['consumers']), {'CROSS_SERIES_REFERENCE'}),
    ('L15b', 'cross-series: status core teaching_hub is a LOHAN node', 'absent', l15b,
     lambda reg, ren, live: reg['status']['STATUS-BWM'].get('teaching_hub') == K_L13_4, {'CROSS_SERIES_REFERENCE'}),
    ('L16', 'inbound referrer is an unregistered LOHAN page', 'absent', l16,
     lambda reg, ren, live: any(r['referrer_file'] == f'{LP}22.html' for r in reg['inbound']), {'LOHAN_REFERRER_UNREGISTERED'}),
    ('L16b', 'inbound referrer is a LOHAN-looking path that is not a recognised spec', 'absent', l16b,
     lambda reg, ren, live: any(r['referrer_file'].endswith('specs/lohan/extra.json') for r in reg['inbound']), {'LOHAN_REFERRER_UNREGISTERED'}),
    ('L17', 'LOHAN->Uday inbound row with a broken Uday target', 'absent', l17,
     lambda reg, ren, live: any(_is_lohan_referrer(r['referrer_file']) and r['target_source_node_key'].endswith('#topic-99') for r in reg['inbound']),
     {'INBOUND_BROKEN'}),
    ('L18', 'LOHAN page named inside a status core', 'absent', l18,
     lambda reg, ren, live: 'lohan-notes' in reg['raw_text']['status/STATUS-NZF.json'], {'LOHAN_ROW'}),
    ('L19', 'MERGE-### enters the data alongside LOHAN rows', 'absent', l19,
     lambda reg, ren, live: 'MERGE-045' in reg['raw_text']['source_nodes.csv'], {'FORBIDDEN_SUBJECT_ID'}),
    ('L19b', 'PCT-* canonical id enters the inbound baseline', 'absent', l19b,
     lambda reg, ren, live: 'PCT-BWM-LIABILITY' in reg['raw_text']['inbound_baseline.csv'], {'FORBIDDEN_SUBJECT_ID'}),
    ('L21', 'live LOHAN->Uday reference count drifts from the baseline', 'present', l21,
     lambda reg, ren, live: sum(n for k, n in live.items() if _is_lohan_referrer(k[0])) == 129, {'LOHAN_INBOUND_DRIFT'}),
    ('L21b', 'baseline loses a LOHAN row that is still live', 'present', l21b,
     lambda reg, ren, live: len(_lib(reg, lambda r: _is_lohan_referrer(r['referrer_file']))) == 125, {'LOHAN_INBOUND_DRIFT'}),
    ('L22', 'live reference from an unadmitted LOHAN page', 'present', l22,
     lambda reg, ren, live: any(k[0] == f'{LP}22.html' for k in live), {'LOHAN_REFERRER_UNREGISTERED'}),
    ('L23', 'LOHAN row source_commit is not a 40-hex commit', 'absent', l23,
     lambda reg, ren, live: _lrow(reg)['source_commit'] == '43441b7', {'BAD_SOURCE_COMMIT'}),
    ('L24', 'LOHAN row part disagrees with its file', 'absent', l24,
     lambda reg, ren, live: _lrow(reg)['part'] == '14', {'PART_MISMATCH'}),
    ('L25', 'LOHAN row uses a Uday anchor scheme', 'absent', l25,
     lambda reg, ren, live: _lrow(reg)['anchor_scheme'] == 'GLOBAL', {'SCHEME_MISMATCH'}),
    ('L26', 'LOHAN row file column disagrees with its key', 'absent', l26,
     lambda reg, ren, live: _lrow(reg)['file'] == f'{LP}12.html', {'KEY_FIELD_MISMATCH'}),
    ('L27', 'LOHAN ordinal disagrees with its anchor', 'absent', l27,
     lambda reg, ren, live: _lrow(reg)['ordinal_in_part'] == '9', {'ORDINAL_MISMATCH'}),
]


# ------------------------------------------------------------------ reverse references (F3)
# Uday-series source files referring to LOHAN pages. Each case carries the live cross-series
# scan as a fourth object, and must report EXACTLY its expected codes (a stricter bar than the
# M/L cases), so a case cannot pass on an unrelated failure. `auth` cases run with UDAY->LOHAN
# temporarily added to REGISTRABLE_DIRECTIONS, to prove the rule is registration, not a ban.

U5 = f'{P}5.html'
U_SPEC = 'tools/notes/specs/p19.json'
U_SQ = 'SQ/miw-notes-mgmt-p1.html'
L_BAD_PART = f'{LP}3.html#topic-p4-1'
L_UNADMITTED = f'{LP}22.html#topic-p22-1'
L_UNREG_NODE = f'{LP}13.html#topic-p13-99'
L_UDAY_ANCHOR = f'{LP}13.html#topic-51'


def _uday_ref(path):
    return V.referrer_series(path)[0] == 'UDAY'


def _rev_live(cross, tgt=None):
    return sum(n for (r, t), n in cross.items() if _uday_ref(r) and (tgt is None or t == tgt))


def _rev_rows(reg, tgt=None):
    return [r for r in reg['inbound'] if _uday_ref(r['referrer_file']) and
            (V.is_lohan_key(r['target_source_node_key']) if tgt is None else r['target_source_node_key'] == tgt)]


def _register(reg, ref, tgt, n=1):
    reg['inbound'].append({'referrer_file': ref, 'target_source_node_key': tgt, 'count': str(n),
                           'source_commit': reg['inbound'][0]['source_commit']})


def _link(cross, ref, tgt, n=1):
    cross[(ref, tgt)] += n


RCASES = [  # (id, description, mode, auth, mutate(reg, ren, live, cross), proof(...), EXACT expected codes)
    ('R1', 'Uday Part page links to a real LOHAN node, unregistered', 'present', False,
     lambda reg, ren, live, x: _link(x, U5, K_L13_4),
     lambda reg, ren, live, x: _rev_live(x, K_L13_4) == 1, {'CROSS_SERIES_UNREGISTERED'}),
    ('R1a', 'same, LOHAN pages absent from the tree (production today)', 'absent', False,
     lambda reg, ren, live, x: _link(x, U5, K_L13_4),
     lambda reg, ren, live, x: _rev_live(x, K_L13_4) == 1, {'CROSS_SERIES_UNREGISTERED'}),
    ('R1b', 'Uday spec references a LOHAN node, unregistered', 'present', False,
     lambda reg, ren, live, x: _link(x, U_SPEC, K_L1_1),
     lambda reg, ren, live, x: _rev_live(x, K_L1_1) == 1, {'CROSS_SERIES_UNREGISTERED'}),
    ('R1c', 'Uday SQ twin references a LOHAN node, unregistered', 'present', False,
     lambda reg, ren, live, x: _link(x, U_SQ, K_L1_1),
     lambda reg, ren, live, x: _rev_live(x, K_L1_1) == 1, {'CROSS_SERIES_UNREGISTERED'}),
    ('R2', 'Uday page links to a LOHAN page with no anchor (page-level)', 'present', False,
     lambda reg, ren, live, x: _link(x, U5, f'{LP}13.html'),
     lambda reg, ren, live, x: _rev_live(x, f'{LP}13.html') == 1, {'CROSS_SERIES_UNREGISTERED'}),
    ('R3', 'invalid cross-series identity: LOHAN p3 file with a part-4 anchor', 'present', False,
     lambda reg, ren, live, x: _link(x, U5, L_BAD_PART),
     lambda reg, ren, live, x: _rev_live(x, L_BAD_PART) == 1, {'CROSS_SERIES_BAD_IDENTITY', 'CROSS_SERIES_UNREGISTERED'}),
    ('R3b', 'invalid cross-series identity: unadmitted LOHAN page p22', 'present', False,
     lambda reg, ren, live, x: _link(x, U5, L_UNADMITTED),
     lambda reg, ren, live, x: _rev_live(x, L_UNADMITTED) == 1, {'CROSS_SERIES_BAD_IDENTITY', 'CROSS_SERIES_UNREGISTERED'}),
    ('R3c', 'invalid cross-series identity: unregistered node on an admitted LOHAN page', 'present', False,
     lambda reg, ren, live, x: _link(x, U5, L_UNREG_NODE),
     lambda reg, ren, live, x: _rev_live(x, L_UNREG_NODE) == 1, {'CROSS_SERIES_BAD_IDENTITY', 'CROSS_SERIES_UNREGISTERED'}),
    ('R3d', 'invalid cross-series identity: Uday-style anchor under a LOHAN file', 'present', False,
     lambda reg, ren, live, x: _link(x, U5, L_UDAY_ANCHOR),
     lambda reg, ren, live, x: _rev_live(x, L_UDAY_ANCHOR) == 1, {'CROSS_SERIES_BAD_IDENTITY', 'CROSS_SERIES_UNREGISTERED'}),
    ('R4', 'Uday->LOHAN row registered while the direction is not authorised', 'absent', False,
     lambda reg, ren, live, x: _register(reg, U5, K_L13_4),
     lambda reg, ren, live, x: len(_rev_rows(reg, K_L13_4)) == 1, {'CROSS_SERIES_REFERENCE', 'CROSS_SERIES_DRIFT'}),
    ('R4b', 'self-registration bypass: link AND register without authorisation', 'present', False,
     lambda reg, ren, live, x: (_register(reg, U5, K_L13_4), _link(x, U5, K_L13_4)),
     lambda reg, ren, live, x: len(_rev_rows(reg, K_L13_4)) == 1 and _rev_live(x, K_L13_4) == 1, {'CROSS_SERIES_REFERENCE'}),
    ('R5', 'anchor-only registered target from a Uday referrer', 'absent', False,
     lambda reg, ren, live, x: _register(reg, U5, 'topic-p13-4'),
     lambda reg, ren, live, x: len(_rev_rows(reg, 'topic-p13-4')) == 1, {'KEY_WITHOUT_FILE', 'INBOUND_BROKEN'}),
    ('R5b', 'anchor-only registered target with an empty file (#anchor)', 'absent', False,
     lambda reg, ren, live, x: _register(reg, U5, '#topic-p13-4'),
     lambda reg, ren, live, x: len(_rev_rows(reg, '#topic-p13-4')) == 1, {'KEY_WITHOUT_FILE', 'INBOUND_BROKEN'}),
    # narrowness: what the rule must NOT catch
    ('R-pos1', 'LOHAN->LOHAN navigation reference is intra-series (not caught)', 'present', False,
     lambda reg, ren, live, x: _link(x, f'{LP}12.html', K_L13_4),
     lambda reg, ren, live, x: x[(f'{LP}12.html', K_L13_4)] == 1, set()),
    ('R-pos2', 'a governance record naming a LOHAN node is not a series reference (not caught)', 'present', False,
     lambda reg, ren, live, x: _link(x, 'docs/notes/POST31_LOHAN_SOURCE_ADMISSION_20261010.md', K_L13_4),
     lambda reg, ren, live, x: x[('docs/notes/POST31_LOHAN_SOURCE_ADMISSION_20261010.md', K_L13_4)] == 1, set()),
    # governance authorises UDAY->LOHAN: registered references pass, everything else still fails
    ('RA-pos', '[authorised] registered + live Uday->LOHAN node reference PASSES', 'present', True,
     lambda reg, ren, live, x: (_register(reg, U5, K_L13_4), _link(x, U5, K_L13_4)),
     lambda reg, ren, live, x: len(_rev_rows(reg, K_L13_4)) == 1 and _rev_live(x, K_L13_4) == 1, set()),
    ('RA-pos-a', '[authorised] same, LOHAN pages absent', 'absent', True,
     lambda reg, ren, live, x: (_register(reg, U_SPEC, K_L1_1, 2), _link(x, U_SPEC, K_L1_1, 2)),
     lambda reg, ren, live, x: len(_rev_rows(reg, K_L1_1)) == 1 and _rev_live(x, K_L1_1) == 2, set()),
    ('RA1', '[authorised] live count exceeds the registered count', 'present', True,
     lambda reg, ren, live, x: (_register(reg, U5, K_L13_4), _link(x, U5, K_L13_4, 2)),
     lambda reg, ren, live, x: _rev_live(x, K_L13_4) == 2, {'CROSS_SERIES_UNREGISTERED'}),
    ('RA1b', '[authorised] live reference with no registration', 'present', True,
     lambda reg, ren, live, x: _link(x, U5, K_L13_4),
     lambda reg, ren, live, x: _rev_live(x, K_L13_4) == 1, {'CROSS_SERIES_UNREGISTERED'}),
    ('RA2', '[authorised] registered reference is no longer live', 'present', True,
     lambda reg, ren, live, x: _register(reg, U5, K_L13_4),
     lambda reg, ren, live, x: len(_rev_rows(reg, K_L13_4)) == 1, {'CROSS_SERIES_DRIFT'}),
    ('RA3', '[authorised] registered + live target with an invalid cross-series identity', 'present', True,
     lambda reg, ren, live, x: (_register(reg, U5, L_BAD_PART), _link(x, U5, L_BAD_PART)),
     lambda reg, ren, live, x: len(_rev_rows(reg, L_BAD_PART)) == 1, {'CROSS_SERIES_BAD_IDENTITY'}),
    ('RA4', '[authorised] anchor-only registration is still rejected', 'present', True,
     lambda reg, ren, live, x: _register(reg, U5, 'topic-p13-4'),
     lambda reg, ren, live, x: len(_rev_rows(reg, 'topic-p13-4')) == 1, {'KEY_WITHOUT_FILE', 'INBOUND_BROKEN'}),
    ('RA5', '[authorised UDAY->LOHAN only] LOHAN->LOHAN registration is still refused', 'absent', True,
     lambda reg, ren, live, x: _register(reg, f'{LP}12.html', K_L13_4),
     lambda reg, ren, live, x: any(r['referrer_file'] == f'{LP}12.html' and r['target_source_node_key'] == K_L13_4 for r in reg['inbound']),
     {'CROSS_SERIES_REFERENCE'}),
]


# ------------------------------------------------------------------ publication state (D-L4 governance)
# The declared LOHAN_SERIES_STATE against the activation evidence. Every S case is checkout-independent:
# the evidence is built in memory from the admitted page set, the LOHAN rows are set to the case's
# status, and the declared state is overridden for the case only. Each must report EXACTLY its codes.
# The three SC controls (one per valid state) must PASS with zero errors.

_ALL = sorted(f'lohan-notes-p{n}.html' for n in V.LOHAN_ADMITTED_PAGES)


def _ev(kind):
    none = {'manifest_series': False, 'manifest_files': [], 'manifest_live_claims': [], 'manifest_error': '',
            'nav_section': False, 'nav_files': [], 'nav_live_claims': [], 'pages_on_disk': list(_ALL), 'gated_exact': []}
    if kind == 'none':
        return none
    ev = dict(none, manifest_series=True, manifest_files=list(_ALL), nav_section=True, nav_files=list(_ALL),
              gated_exact=list(_ALL))
    if kind == 'live':
        ev.update(manifest_live_claims=['series: gated - live - Parts 1-21'], nav_live_claims=['ncs-live'])
    return ev


def _with(kind, **kw):
    ev = _ev(kind)
    for k, f in kw.items():
        ev[k] = f(ev[k]) if callable(f) else f
    return ev


def _set_rows(reg, how):
    rows = _lohan_rows(reg)
    for i, r in enumerate(rows):
        r['publication_status'] = {'unpub': V.UNPUBLISHED_STATUS, 'live': V.PUBLICATION_STATUS,
                                   'mixed': V.PUBLICATION_STATUS if i % 2 else V.UNPUBLISHED_STATUS}[how]


U_, P_, L_ = 'UNACTIVATED', 'PREVIEW_NONPUBLISHING', 'PUBLISHED_LIVE'
_VALID = {U_: ('unpub', 'none'), P_: ('unpub', 'preview'), L_: ('live', 'live')}

SCASES = [  # (id, description, declared state, rows, evidence, release_candidate, EXACT expected codes)
    ('SC-U', '[control] UNACTIVATED, rows unpublished, nothing activated (production today)', U_, 'unpub', _ev('none'), False, set()),
    ('SC-P', '[control] PREVIEW_NONPUBLISHING, rows unpublished, fully activated, nothing says live', P_, 'unpub', _ev('preview'), False, set()),
    ('SC-L', '[control] PUBLISHED_LIVE, rows live, manifest + index + exact gate complete', L_, 'live', _ev('live'), False, set()),
    ('SC-L-rc', '[control] PUBLISHED_LIVE is releasable (release-candidate mode)', L_, 'live', _ev('live'), True, set()),
    ('S1', 'activated tree still declares UNACTIVATED (silent unpublished state)', U_, 'unpub', _ev('preview'), False,
     {'LOHAN_ACTIVATION_UNDECLARED'}),
    ('S1b', 'activated and shown live while declared UNACTIVATED', U_, 'unpub', _ev('live'), False,
     {'LOHAN_ACTIVATION_UNDECLARED', 'LOHAN_UNPUBLISHED_SHOWN_LIVE'}),
    ('S2', 'preview: manifest status says live (the 4eef181 defect)', P_, 'unpub',
     _with('preview', manifest_live_claims=['lohan-notes-p1.html: gated - live']), False, {'LOHAN_UNPUBLISHED_SHOWN_LIVE'}),
    ('S3', 'preview: an index card says Live (the 4eef181 defect)', P_, 'unpub',
     _with('preview', nav_live_claims=['✅ Live']), False, {'LOHAN_UNPUBLISHED_SHOWN_LIVE'}),
    ('S4', 'preview: manifest lists the series, index does not', P_, 'unpub',
     _with('preview', nav_section=False, nav_files=[]), False, {'LOHAN_ACTIVATION_PARTIAL', 'LOHAN_PREVIEW_NOT_ACTIVATED'}),
    ('S4b', 'index lists the series, manifest does not, declared UNACTIVATED', U_, 'unpub',
     _with('none', nav_section=True, nav_files=list(_ALL)), False, {'LOHAN_ACTIVATION_PARTIAL', 'LOHAN_ACTIVATION_UNDECLARED'}),
    ('S5', 'preview: manifest is missing an admitted page', P_, 'unpub',
     _with('preview', manifest_files=lambda v: [f for f in v if f != 'lohan-notes-p7.html']), False, {'LOHAN_ACTIVATION_INCOMPLETE'}),
    ('S6', 'preview offered as a release candidate', P_, 'unpub', _ev('preview'), True, {'LOHAN_PREVIEW_NOT_RELEASABLE'}),
    ('S7', 'PUBLISHED_LIVE declared but the rows were not flipped', L_, 'unpub', _ev('live'), False, {'BAD_PUBLICATION_STATUS'}),
    ('S8', 'PUBLISHED_LIVE declared, rows mixed', L_, 'mixed', _ev('live'), False, {'BAD_PUBLICATION_STATUS', 'LOHAN_STATUS_MIXED'}),
    ('S8b', 'UNACTIVATED declared, rows mixed', U_, 'mixed', _ev('none'), False, {'BAD_PUBLICATION_STATUS', 'LOHAN_STATUS_MIXED'}),
    ('S9', 'PUBLISHED_LIVE with no activation at all', L_, 'live', _ev('none'), False, {'LOHAN_LIVE_WITHOUT_ACTIVATION'}),
    ('S10', 'PUBLISHED_LIVE but one page lacks the exact gate', L_, 'live',
     _with('live', gated_exact=lambda v: [f for f in v if f != 'lohan-notes-p12.html']), False, {'LOHAN_LIVE_WITHOUT_ACTIVATION'}),
    ('S11', 'PUBLISHED_LIVE but the index misses a page', L_, 'live',
     _with('live', nav_files=lambda v: [f for f in v if f != 'lohan-notes-p21.html']), False,
     {'LOHAN_LIVE_WITHOUT_ACTIVATION', 'LOHAN_ACTIVATION_INCOMPLETE'}),
    ('S12', 'PUBLISHED_LIVE but the manifest still says preview (no live status)', L_, 'live',
     _with('live', manifest_live_claims=[]), False, {'LOHAN_LIVE_WITHOUT_ACTIVATION'}),
    ('S13', 'unknown declared state', 'LIVE', 'unpub', _ev('none'), False, {'LOHAN_STATE_UNKNOWN'}),
    ('S14', 'PREVIEW_NONPUBLISHING declared on an unactivated tree', P_, 'unpub', _ev('none'), False, {'LOHAN_PREVIEW_NOT_ACTIVATED'}),
    ('S15', 'rows flipped to PUBLISHED_LIVE, declaration not (the S1a fixture)', U_, 'live', _ev('none'), False, {'BAD_PUBLICATION_STATUS'}),
    ('S16', 'unreadable Notes manifest', U_, 'unpub', _with('none', manifest_error='Expecting value: line 1'), False,
     {'LOHAN_ACTIVATION_UNREADABLE'}),
]


def run_state_case(base_reg, ren, live, cross, state, rows, ev, rc):
    reg = copy.deepcopy(base_reg)
    _set_rows(reg, rows)
    saved = V.LOHAN_SERIES_STATE
    V.LOHAN_SERIES_STATE = state
    try:
        errs = V.validate(reg, copy.deepcopy(ren), Counter(live), Counter(cross), copy.deepcopy(ev), rc)
    finally:
        V.LOHAN_SERIES_STATE = saved
    return reg, errs


def collisions(reg):
    """Anchor strings registered in BOTH series (the reason keys are file-qualified)."""
    u = {r['anchor'] for r in reg['source_nodes'] if r['series'] == 'UDAY'}
    l = {r['anchor'] for r in reg['source_nodes'] if r['series'] == 'LOHAN'}
    return sorted(u & l)


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
    holders = [x for x in V.load_registry()[0]['source_nodes'] if x['anchor'] == 'topic-p13-1' and x['series'] == 'UDAY']
    proof = len({r['file'] for r in reg['source_nodes'] if r['anchor'] == 'topic-p13-1' and r['series'] == 'UDAY'}) == 2 and len(holders) == 1
    errs = V.validate(reg, ren, None)
    return proof, errs


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    out_json = argv[argv.index('--json') + 1] if '--json' in argv else None
    base_reg, load_errs = V.load_registry()
    base_ren = V.scan_rendered()
    base_live = V.scan_inbound()
    base_cross = V.scan_cross_series()
    results, failures = [], 0

    def record(cid, desc, ok, detail):
        nonlocal failures
        failures += 0 if ok else 1
        results.append({'id': cid, 'description': desc, 'result': 'PASS' if ok else 'FAIL', **detail})
        print(f"{'PASS' if ok else 'FAIL'}  {cid:5} {desc}  {detail.get('summary', '')}")

    base_act = V.scan_activation()
    # M8 — unmutated control (the checkout exactly as found, publication-state rules included)
    ctrl = V.validate(copy.deepcopy(base_reg), copy.deepcopy(base_ren), Counter(base_live), Counter(base_cross),
                      copy.deepcopy(base_act))
    record('M8', 'unmutated control must PASS', not load_errs and not ctrl,
           {'summary': f'errors={len(load_errs) + len(ctrl)}', 'errors': [list(e) for e in load_errs + ctrl]})
    if load_errs or ctrl:
        for e in load_errs + ctrl:
            print('   control error:', e)

    # M8a / M8b — the same registry validated with LOHAN pages ABSENT and PRESENT
    modes, have_real = make_modes(base_reg, base_ren, base_live)
    print(f'   (checkout has real LOHAN pages: {have_real}; absent/present modes derived accordingly)')
    for mode, label in (('absent', 'M8a'), ('present', 'M8b')):
        mren, mlive = modes[mode]
        errs = V.validate(copy.deepcopy(base_reg), copy.deepcopy(mren), Counter(mlive), Counter(base_cross))
        n_l_pages = sum(1 for v in mren.values() if v.get('series') == 'LOHAN')
        n_l_live = sum(n for k, n in mlive.items() if _is_lohan_referrer(k[0]))
        ok = not errs and (n_l_pages == 0 and n_l_live == 0 if mode == 'absent' else n_l_pages == 21 and n_l_live == 128)
        record(label, f'unmutated control, LOHAN pages {mode} (LOHAN pages={n_l_pages}, live LOHAN refs={n_l_live})', ok,
               {'summary': f'errors={len(errs)}', 'errors': [list(e) for e in errs]})

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

    for cid, desc, mode, mutate, proof, expected in LCASES:
        mren, mlive = modes[mode]
        reg, ren, live = copy.deepcopy(base_reg), copy.deepcopy(mren), Counter(mlive)
        before = proof(reg, ren, live)
        mutate(reg, ren, live)
        after = proof(reg, ren, live)
        changed = (reg != base_reg) or (ren != mren) or (live != mlive)
        errs = V.validate(reg, ren, live)
        codes = sorted({c for c, _ in errs})
        ok = (not before) and after and changed and expected <= set(codes)
        record(cid, f'[{mode}] {desc}', ok, {'summary': f'proof {before}->{after}; required {sorted(expected)}; got {codes}',
                                             'mode': mode, 'proof_before': before, 'proof_after': after, 'data_changed': changed,
                                             'expected_codes': sorted(expected), 'reported_codes': codes, 'n_errors': len(errs)})

    # R-series: reverse-reference isolation (F3)
    n_scope = sum(1 for f in V.tracked_files() if V.UDAY_REFERRER_RE.match(f))
    record('R-scan', f'live Uday->LOHAN references in this checkout = 0 across {n_scope} Uday source files; registered = 0',
           _rev_live(base_cross) == 0 and not _rev_rows(base_reg) and n_scope >= 32,
           {'summary': f'live={_rev_live(base_cross)} registered={len(_rev_rows(base_reg))} scope_files={n_scope}'})
    for cid, desc, mode, auth, mutate, proof, expected in RCASES:
        mren, mlive = modes[mode]
        reg, ren, live, cross = copy.deepcopy(base_reg), copy.deepcopy(mren), Counter(mlive), Counter(base_cross)
        before = proof(reg, ren, live, cross)
        mutate(reg, ren, live, cross)
        after = proof(reg, ren, live, cross)
        changed = (reg != base_reg) or (cross != base_cross)
        saved = V.REGISTRABLE_DIRECTIONS
        if auth:
            V.REGISTRABLE_DIRECTIONS = saved | {(V.SERIES, V.SERIES_LOHAN)}
        try:
            errs = V.validate(reg, ren, live, cross)
        finally:
            V.REGISTRABLE_DIRECTIONS = saved
        codes = sorted({c for c, _ in errs})
        ok = (not before) and after and changed and set(codes) == expected
        record(cid, f'[{mode}] {desc}', ok, {'summary': f'proof {before}->{after}; required EXACTLY {sorted(expected)}; got {codes}',
                                             'mode': mode, 'authorised': auth, 'proof_before': before, 'proof_after': after,
                                             'data_changed': changed, 'expected_codes': sorted(expected), 'reported_codes': codes,
                                             'exact': True, 'n_errors': len(errs), 'errors': [list(e) for e in errs]})

    # S-series: LOHAN publication state (D-L4 governance)
    print(f'   (declared LOHAN state in this checkout: {V.LOHAN_SERIES_STATE}; S cases override it per case)')
    aren, alive = modes['absent']
    for cid, desc, state, rows, ev, rc, expected in SCASES:
        reg, errs = run_state_case(base_reg, aren, alive, base_cross, state, rows, ev, rc)
        codes = sorted({c for c, _ in errs})
        if cid.startswith('SC-'):
            proof = True   # controls: the valid configuration of the declared state
        else:
            vrows, vkind = _VALID.get(state, ('unpub', 'none'))
            proof = (rows != vrows) or (ev != _ev(vkind)) or rc or state not in _VALID
        ok = proof and set(codes) == expected
        record(cid, f'[state {state}{", release" if rc else ""}] {desc}', ok,
               {'summary': f'required EXACTLY {sorted(expected)}; got {codes}', 'declared_state': state,
                'rows': rows, 'release_candidate': rc, 'proof_differs_from_valid': proof,
                'expected_codes': sorted(expected), 'reported_codes': codes, 'exact': True,
                'n_errors': len(errs), 'errors': [list(e) for e in errs[:5]]})

    # positive: the same anchor STRING in LOHAN and Uday is permitted because keys carry the file
    coll = collisions(base_reg)
    mren, mlive = modes['present']
    perrs = V.validate(copy.deepcopy(base_reg), copy.deepcopy(mren), Counter(mlive))
    record('L-pos1', f'LOHAN/Uday anchor-string collisions ({len(coll)}) are permitted; 123 LOHAN rows; 0 duplicate keys',
           len(coll) == 35 and len(_lohan_rows(base_reg)) == 123 and len(set(_keys(base_reg))) == len(_keys(base_reg)) and not perrs,
           {'summary': f'collisions={len(coll)} errors={len(perrs)}', 'collision_count': len(coll)})
    ucount = sum(1 for r in base_reg['source_nodes'] if r['series'] == 'UDAY')
    record('L-pos2', f'Uday rows are still exactly the {ucount} rendered Uday topic-blocks and carry no LOHAN column values',
           ucount == 118 and all(r['publication_status'] == 'PUBLISHED_LIVE' for r in base_reg['source_nodes'] if r['series'] == 'UDAY'),
           {'summary': f'uday_rows={ucount}'})

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
