#!/usr/bin/env python3
"""
test_validate_status_consumers.py — mutation tests for validate_status_consumers.py (POST31-CA3).

Each case deep-copies the REAL candidate data (status records, source-node keys, Uday
pages), applies one mutation in memory, proves the mutation actually changed the input,
and REQUIRES the rule's own error code. Nothing is written to disk. The unmutated control
must pass with zero errors.

Usage: python tools/notes/canonical/test_validate_status_consumers.py
"""
from __future__ import annotations

import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import validate_canonical as V  # noqa: E402
import validate_status_consumers as S  # noqa: E402

P = 'meoclass1/oralnotes/miw-notes-mgmt-p{}.html'
HUB_HREF = 'href="miw-notes-mgmt-p22.html#topic-p22-3"'


def real():
    reg, errors = V.load_registry()
    assert not errors, errors
    keys = {r['source_node_key'] for r in reg['source_nodes']}
    return reg['status'], keys, S.load_pages()


BASE = real()


def page_sub(pages, n, old, new, count=1):
    f = P.format(n)
    assert pages[f].count(old) >= 1, f'mutation anchor missing in {f}: {old[:60]!r}'
    pages[f] = pages[f].replace(old, new, count)


def consumer(status, sid, key_suffix):
    hits = [c for c in status[sid]['consumers'] if c['source_node_key'].endswith(key_suffix)]
    assert len(hits) == 1, key_suffix
    return hits[0]


# ---------------------------------------------------------------- mutations

def m1(st, keys, pg):  # NZF consumer points to P2 instead of P22
    page_sub(pg, 24, HUB_HREF, 'href="miw-notes-mgmt-p2.html#topic-9"')


def m2(st, keys, pg):  # second NZF TEACHING_HUB
    consumer(st, 'STATUS-NZF', 'p2.html#topic-9')['role'] = 'TEACHING_HUB'


def m3(st, keys, pg):  # HNS consumer says "in force" without a qualifier
    page_sub(pg, 8, 'No correction was required to these figures.',
             'No correction was required to these figures. The HNS Convention is in force and governs these claims.')


def m4(st, keys, pg):  # marker without an as-of date
    f = P.format(24)
    b = S.topic_blocks(pg[f])['topic-p24-1']
    nb = b.replace(' data-as-of="2026-10-09"', '', 1).replace('As of 9 October 2026: ', '', 1)
    assert nb != b
    pg[f] = pg[f].replace(b, nb)


def m5(st, keys, pg):  # consumer uses a nonexistent file#anchor
    page_sub(pg, 23, 'miw-notes-mgmt-p22.html#topic-p22-3', 'miw-notes-mgmt-p22.html#topic-p22-9')


def m6(st, keys, pg):  # consumer links directly to the repository status JSON
    page_sub(pg, 28, '(current status: <a ', '(<a href="/tools/notes/canonical/status/STATUS-NZF.json">data</a>; current status: <a ')


def m7(st, keys, pg):  # invented canonical ID on a page
    page_sub(pg, 31, 'Full current treatment', 'Canonical subject MERGE-072. Full current treatment')


def m8(st, keys, pg):  # unknown status id
    page_sub(pg, 29, 'data-status-id="STATUS-NZF"', 'data-status-id="STATUS-ECA"')


# additional controls on the same rules
def m10(st, keys, pg):  # record refreshed but markers not re-dated
    st['STATUS-NZF']['as_of'] = '2026-12-05'


def m11(st, keys, pg):  # marker label drifts from the record
    page_sub(pg, 24, 'APPROVED (MEPC 83) — NOT ADOPTED — NOT IN FORCE', 'ADOPTED — NOT IN FORCE')


def m12(st, keys, pg):  # marker placed on a node that is not a declared consumer
    f = P.format(23)
    b = S.topic_blocks(pg[f])['topic-p23-1']
    mk = S.find_markers(S.topic_blocks(pg[P.format(24)])['topic-p24-1'])[0]
    nb = b.replace('<div class="verify-note">', f'<div{mk[1]}>{mk[3]}</div><div class="verify-note">', 1)
    assert nb != b
    pg[f] = pg[f].replace(b, nb)


def m13(st, keys, pg):  # P23 reverted to the CA2 wording (CA1 CA-A03)
    page_sub(pg, 23, 'The draft Net-Zero Framework must not be confused with CII, which is tank-to-wake: its current status is in '
                     '<a href="miw-notes-mgmt-p22.html#topic-p22-3">Part 22 · Topic 3</a>, and its pricing mechanics in Part 2 Topic 9.',
             'Part 2 Topic 9 covers the draft Net-Zero Framework and must not be confused with CII, which is tank-to-wake.')


def m14(st, keys, pg):  # the CA2-corrected P4 error re-introduced inside topic-16
    f = P.format(4)
    b = S.topic_blocks(pg[f])['topic-16']
    nb = b.replace('<div class="topic-footer">', '<p>The 2010 HNS Protocol entered into force in 2021.</p><div class="topic-footer">', 1)
    assert nb != b
    pg[f] = pg[f].replace(b, nb)


def m15(st, keys, pg):  # NZF hub moved off P22
    st['STATUS-NZF']['teaching_hub'] = 'meoclass1/oralnotes/miw-notes-mgmt-p2.html#topic-9'


def m16(st, keys, pg):  # declared marker removed from the page
    f = P.format(12)
    b = S.topic_blocks(pg[f])['topic-51']
    mk = S.find_markers(b)[0]
    whole = f'<{mk[0]}{mk[1]}>{mk[3]}</{mk[0]}>'
    assert whole in b
    pg[f] = pg[f].replace(whole, '')


def m17(st, keys, pg):  # pointer target is not a teaching consumer
    consumer(st, 'STATUS-HNS2010', 'p8.html#topic-36')['requires_pointer_to'] = 'meoclass1/oralnotes/miw-notes-mgmt-p9.html#topic-40'


def m18(st, keys, pg):  # consumer key not registered
    consumer(st, 'STATUS-BWM', 'p12.html#topic-51')['source_node_key'] = 'meoclass1/oralnotes/miw-notes-mgmt-p12.html#topic-2'


CASES = [
    ('M1', 'NZF consumer points to P2 instead of P22', m1, {'SC_NZF_STATUS_POINTS_TO_P2', 'SC_HUB_POINTER_MISSING'}),
    ('M2', 'second NZF TEACHING_HUB', m2, {'SC_HUB_COUNT'}),
    ('M3', 'HNS "in force" without scheduled/not-yet qualifier', m3, {'SC_HNS_IN_FORCE_CLAIM'}),
    ('M4', 'marker without as-of date', m4, {'SC_MARKER_NO_AS_OF'}),
    ('M5', 'consumer uses nonexistent file#anchor', m5, {'SC_LINK_UNRESOLVED'}),
    ('M6', 'direct link to /tools/notes/canonical/status/*.json', m6, {'SC_PRIVATE_PATH'}),
    ('M7', 'invented canonical ID on page', m7, {'SC_CANONICAL_ID_ON_PAGE'}),
    ('M8', 'unknown status id', m8, {'SC_UNKNOWN_STATUS_ID'}),
    ('M10', 'record re-dated, markers stale', m10, {'SC_MARKER_STALE'}),
    ('M11', 'marker label drift', m11, {'SC_MARKER_LABEL'}),
    ('M12', 'marker on an undeclared node', m12, {'SC_MARKER_UNDECLARED'}),
    ('M13', 'P23 pointer reverted to P2-T9', m13, {'SC_NZF_STATUS_POINTS_TO_P2'}),
    ('M14', 'P4 "entered into force 2021" re-introduced', m14, {'SC_HNS_IN_FORCE_CLAIM'}),
    ('M15', 'NZF hub moved off P22', m15, {'SC_NZF_HUB_WRONG'}),
    ('M16', 'declared marker removed', m16, {'SC_MARKER_MISSING'}),
    ('M17', 'pointer target not a teaching consumer', m17, {'SC_POINTER_TARGET_WRONG'}),
    ('M18', 'consumer key not registered', m18, {'SC_CONSUMER_UNRESOLVED'}),
]


def run_case(fn):
    st, keys, pg = copy.deepcopy(BASE)
    before = (copy.deepcopy(st), dict(pg))
    fn(st, keys, pg)
    changed = st != before[0] or pg != before[1]
    return changed, {c for c, _ in S.validate(st, keys, pg)}


def main(argv=None) -> int:
    results = []
    # M9: unmutated candidate must pass
    st, keys, pg = copy.deepcopy(BASE)
    ctrl = S.validate(st, keys, pg)
    results.append(('M9', 'unmutated candidate', not ctrl, f'{len(ctrl)} errors {sorted({c for c, _ in ctrl})}'))
    for cid, what, fn, required in CASES:
        try:
            changed, codes = run_case(fn)
        except AssertionError as e:
            results.append((cid, what, False, f'mutation could not be applied: {e}'))
            continue
        ok = changed and required <= codes
        results.append((cid, what, ok, f'mutated={changed} required={sorted(required)} got={sorted(codes)}'))
    for cid, what, ok, detail in results:
        print(f'  [{"PASS" if ok else "FAIL"}] {cid:4} {what} — {detail}')
    n_ok = sum(1 for r in results if r[2])
    print(f'{n_ok}/{len(results)} mutation/control cases PASS')
    return 0 if n_ok == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
