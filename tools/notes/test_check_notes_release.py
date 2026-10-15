#!/usr/bin/env python3
"""Negative and mutation controls for check_notes_release.py (D-L4 governance, 11 Oct 2026).

Same discipline as test_validate_canonical.py: every case starts from the REAL checkout data, applies
one mutation in memory (or in a temp copy, never in the worktree), proves the mutation took effect,
and requires EXACTLY the expected finding codes. P cases are positives that must produce nothing.
The cases that need an activated LOHAN series synthesise it when the checkout is unactivated, so
the suite is meaningful on production (d504c03) and on the preview alike.

Run:  python -X utf8 tools/notes/test_check_notes_release.py [--json OUT]
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'canonical'))
import build_part  # noqa: E402
import check_notes_release as C  # noqa: E402
import validate_canonical as V  # noqa: E402

ROOT = C.REPO_ROOT
NOTES = os.path.join(ROOT, *C.NOTES_DIR_REL.split('/'))


def _read(rel):
    with open(os.path.join(ROOT, *rel.split('/')), encoding='utf-8') as fh:
        return fh.read()


RAW_MAN = _read(C.MANIFEST_REL)
MAN, _ = C.load_manifest(RAW_MAN)
INDEX = _read(C.INDEX_REL)
F4 = _read(C.F4_REL)
ACTIVATED = C.LOHAN_KEY in MAN['series']
_LISTED = sorted(MAN['series'].get(C.LOHAN_KEY, {}).get('files', {})) if ACTIVATED else []
# O-3: in a public checkout the LOHAN pages are protected-unavailable (private repo). Cases that need
# their bytes are then N/A, stated as such; the private qualification runs them all.
PROTECTED_UNAVAILABLE = [fn for fn in _LISTED if not os.path.isfile(os.path.join(NOTES, fn))]
if PROTECTED_UNAVAILABLE and not set(PROTECTED_UNAVAILABLE) <= C.protected_declared(NOTES):
    raise SystemExit('LOHAN pages missing that the O-3 pin does not declare: %s' % PROTECTED_UNAVAILABLE[:3])
PAGES = {fn: _read(f'{C.NOTES_DIR_REL}/{fn}') for fn in _LISTED if fn not in PROTECTED_UNAVAILABLE}
LOHAN_ATTR = MAN['series'][C.LOHAN_KEY]['source_attribution'] if ACTIVATED else ''
P20 = 'lohan-notes-p20.html'


def codes(findings):
    return sorted({c for c, _ in findings})


def man_case(mutate, notes_dir=None, raw=None):
    m = copy.deepcopy(MAN)
    mutate(m)
    if raw is not None:
        m2, dups = C.load_manifest(raw)
        return C.check_manifest(m2, dups, notes_dir), m2 != MAN or bool(dups)
    return C.check_manifest(m, [], notes_dir), m != MAN


def _lohan(m):
    return m['series'][C.LOHAN_KEY]


def _set_total(m, delta=0):
    m['total_files'] = sum(len(s['files']) for s in m['series'].values()) + delta


def attr_case(man_attr=None, page_edit=None, index_edit=None):
    pages = dict(PAGES)
    if page_edit:
        fn, f = page_edit
        pages[fn] = f(pages[fn])
    idx = index_edit(INDEX) if index_edit else INDEX
    attr = LOHAN_ATTR if man_attr is None else man_attr
    changed = attr != LOHAN_ATTR or pages != PAGES or idx != INDEX
    return C.check_attribution(attr, pages, idx), changed


def _sub_region(region_re, old, new):
    def f(h):
        m = region_re.search(h)
        assert m and old in m.group(1), (old, region_re.pattern)
        return h[:m.start(1)] + m.group(1).replace(old, new, 1) + h[m.end(1):]
    return f


def _append_body(text):
    return lambda h: h.replace('</main>', f'<p>{text}</p></main>', 1) if '</main>' in h else h.replace('</body>', f'<p>{text}</p></body>', 1)


def route_case(edit):
    tmp = tempfile.mkdtemp(prefix='routes-')
    try:
        shutil.copytree(os.path.join(ROOT, 'api', '_lib'), os.path.join(tmp, 'api', '_lib'))
        p = os.path.join(tmp, 'api', '_lib', 'routes.js')
        with open(p, encoding='utf-8') as fh:
            src = fh.read()
        new = edit(src)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(new)
        paths = [f'/{C.NOTES_DIR_REL}/lohan-notes-p1.html', f'/{C.NOTES_DIR_REL}/lohan-notes-p21.html', f'/{C.MANIFEST_REL}', f'/{C.INDEX_REL}']
        return C.check_routes(C.probe_routes(tmp, paths)), new != src
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def disclaimer_case(policy, index_html=None):
    return C.check_disclaimer(policy, INDEX if index_html is None else index_html), True


GATE = C.GATE_REFERENCE
with open(os.path.join(ROOT, *C.POLICY_REL.split('/')), encoding='utf-8') as _fh:
    POLICY = json.load(_fh)
APPROVED_TEXT = 'Synthetic approved disclaimer text for the test only.'
# A synthetic index whose disclaimer block holds ONLY the synthetic text (replacing any pending block).
_BLOCK_RE = re.compile(r'<div\b[^>]*\bid="%s"[^>]*>.*?</div>' % C.DISCLAIMER_ANCHOR, re.S)
_SYN_BLOCK = f'<div class="x" id="{C.DISCLAIMER_ANCHOR}">{APPROVED_TEXT}</div>'
SYN_INDEX = _BLOCK_RE.sub(lambda m: _SYN_BLOCK, INDEX, count=1) if _BLOCK_RE.search(INDEX) \
    else INDEX.replace('</body>', _SYN_BLOCK + '</body>', 1)
assert C.disclaimer_block_text(SYN_INDEX) == APPROVED_TEXT
SYN_SHA = hashlib.sha256(APPROVED_TEXT.encode('utf-8')).hexdigest()

CASES = [  # (id, description, needs_activation, run() -> (findings, changed), EXACT expected codes)
    # ---------------- manifest
    ('P-M0', 'real manifest: totals, paths, ids, compilers all clean', False,
     lambda: (C.check_manifest(MAN, C.load_manifest(RAW_MAN)[1], NOTES), True), set()),
    ('N-M1', 'total_files off by one', False, lambda: man_case(lambda m: _set_total(m, +1)), {'MANIFEST_TOTAL_MISMATCH'}),
    ('N-M2', 'one file listed under two series (total kept consistent)', False,
     lambda: man_case(lambda m: (m['series']['simon-notes']['files'].__setitem__(
         'miw-notes-mgmt-p1.html', dict(m['series']['engineering-management-notes']['files']['miw-notes-mgmt-p1.html'], part=99)), _set_total(m))),
     {'MANIFEST_DUPLICATE_PATH'}),
    ('N-M3', 'duplicate JSON key inside one object (json.load would hide it)', False,
     lambda: man_case(lambda m: None, raw=RAW_MAN.replace('"total_files":', '"total_files": 0,\n "total_files":', 1)),
     {'MANIFEST_DUPLICATE_KEY'}),
    ('N-M4', 'two files of one series share a part number', False,
     lambda: man_case(lambda m: m['series']['engineering-management-notes']['files']['miw-notes-mgmt-p2.html'].__setitem__('part', 1)),
     {'MANIFEST_DUPLICATE_ID'}),
    ('N-M5', 'a listed file is missing on disk', False,
     lambda: man_case(lambda m: (m['series']['engineering-management-notes']['files'].__setitem__('miw-notes-mgmt-p99.html', {'part': 99}), _set_total(m)), notes_dir=NOTES),
     {'MANIFEST_FILE_MISSING'}),
    ('N-M6', 'Uday series attribution names the LOHAN compiler', False,
     lambda: man_case(lambda m: m['series']['engineering-management-notes'].__setitem__('source_attribution', 'Originally compiled by Sandeep Lohan.')),
     {'COMPILER_MISMATCH'}),
    ('N-M7', 'Simon series attribution names the Uday compiler (the AT8 gap, now closed)', False,
     lambda: man_case(lambda m: m['series']['simon-notes'].__setitem__('source_attribution', 'Originally prepared by Uday Sankar S. Transcribed.')),
     {'COMPILER_MISMATCH'}),
    ('N-M8', 'unknown series without an authorised-compiler entry', False,
     lambda: man_case(lambda m: m['series'].__setitem__('future-notes', {'files': {}, 'source_attribution': 'Originally compiled by X.'})),
     {'COMPILER_MISMATCH'}),
    ('N-M9', "F4's _COMPILER rule drifts (widened)", False,
     lambda: (C.check_compiler_rule(F4.replace(C.F4_RULE_LINE, C.F4_RULE_LINE.replace('[^.,<]+', '[^<]+'))), True),
     {'COMPILER_RULE_DRIFT'}),
    # Founder rebrand 15 Oct 2026: the LOHAN series credits NO compiler (authorised None).
    ('N-L1', 'LOHAN attribution credits a compiler (Uday) although the series credits none', True,
     lambda: man_case(lambda m: _lohan(m).__setitem__('source_attribution', LOHAN_ATTR + ' Originally compiled by Uday Sankar S.')),
     {'COMPILER_MISMATCH'}),
    ('N-L2', 'LOHAN attribution re-credits the historical compiler', True,
     lambda: man_case(lambda m: _lohan(m).__setitem__('source_attribution', LOHAN_ATTR + ' Originally compiled by Sandeep Lohan.')),
     {'COMPILER_MISMATCH'}),
    ('N-L3', 'LOHAN attribution credits a compiler in the "prepared by" form', True,
     lambda: man_case(lambda m: _lohan(m).__setitem__('source_attribution', LOHAN_ATTR + ' Originally prepared by A. Person.')),
     {'COMPILER_MISMATCH'}),
    # ---------------- gate
    ('P-G0', 'gate reference: build_part.GATE == validate_canonical.LOHAN_GATE == pinned sha256', False,
     lambda: (C.check_gate_reference(build_part.GATE, V.LOHAN_GATE), True), set()),
    ('N-G1', 'build_part.GATE altered by one character', False,
     lambda: (C.check_gate_reference(build_part.GATE.replace('miw_auth=1', 'miw_auth=0'), V.LOHAN_GATE), True), {'GATE_REFERENCE_DRIFT'}),
    ('N-G2', 'validate_canonical.LOHAN_GATE altered', False,
     lambda: (C.check_gate_reference(build_part.GATE, V.LOHAN_GATE.replace('pay.html', 'pay.htm')), True), {'GATE_REFERENCE_DRIFT'}),
    ('P-G3', 'every listed LOHAN page carries the exact gate', True, lambda: (C.check_lohan_gates(PAGES), True), set()),
    ('N-G4', 'page gate redirect altered by one character (GN2: miw_auth=1 still present, health_check misses it)', True,
     lambda: (C.check_lohan_gates({P20: PAGES[P20].replace('/SQ/pay.html', '/SQ/pay.htm', 1)}), True), {'LOHAN_GATE_NOT_EXACT'}),
    ('N-G4b', 'page gate cookie token altered', True,
     lambda: (C.check_lohan_gates({P20: PAGES[P20].replace('miw_auth=1', 'miw_auth=l', 1)}), True), {'LOHAN_GATE_NOT_EXACT'}),
    ('N-G5', 'review-copy stub restored', True,
     lambda: (C.check_lohan_gates({P20: PAGES[P20].replace(GATE, C.GATE_STUB, 1)}), True), {'LOHAN_GATE_NOT_EXACT'}),
    ('N-G6', 'gate inserted twice (GN3)', True,
     lambda: (C.check_lohan_gates({P20: PAGES[P20].replace(GATE, GATE + GATE, 1)}), True), {'LOHAN_GATE_NOT_EXACT'}),
    ('N-G7', 'gate present once but not first after <body>', True,
     lambda: (C.check_lohan_gates({P20: PAGES[P20].replace(GATE, '', 1).replace('</body>', GATE + '</body>', 1)}), True), {'LOHAN_GATE_NOT_EXACT'}),
    # ---------------- entitlement
    ('P-E0', 'routes.js resolves LOHAN pages, manifest and index to ORAL_QB_NOTES', False, lambda: route_case(lambda s: s), set()),
    ('N-E1', 'oralnotes prefix re-mapped to another entitlement', False,
     lambda: route_case(lambda s: s.replace('{ prefix: "/meoclass1/oralnotes/", requires: "ORAL_QB_NOTES" }',
                                            '{ prefix: "/meoclass1/oralnotes/", requires: "SOLVED_QP" }')), {'ROUTE_ENTITLEMENT'}),
    ('N-E2', 'LOHAN pages made public (prefix before the rules)', False,
     lambda: route_case(lambda s: s.replace('for (const pub of PUBLIC_PREFIXES) {', 'if (p.startsWith("/meoclass1/oralnotes/lohan-")) return null;\n  for (const pub of PUBLIC_PREFIXES) {')),
     {'ROUTE_ENTITLEMENT'}),
    # ---------------- attribution / notice
    ('P-A0', 'real LOHAN attribution, notices and index pass', True, lambda: attr_case(), set()),
    ('P-A1', 'LOHAN cross-references and examiner names in a page body pass (AT5)', True,
     lambda: attr_case(page_edit=(P20, _append_body('See Uday Notes Part 13, Topic 4; Simon P8 - BWM Convention. Reported examiner focus: Simon (5).'))), set()),
    ('P-A2', 'regulatory prose about approvals that is not about the material passes', True,
     lambda: attr_case(page_edit=(P20, _append_body('The OWS must be type approved by the Administration. Training at an MMD-approved institute is required.'))), set()),
    ('N-A1', 'header loses the series identity', True,
     lambda: attr_case(page_edit=(P20, _sub_region(C.ATTRIB_STRIP_RE, C.EDITION + '.', 'MIW study edition.'))),
     {'ATTRIBUTION_POLICY'}),
    ('N-A2', 'footer names the historical compiler', True,
     lambda: attr_case(page_edit=(P20, _sub_region(C.FOOTER_RE, '© 2026 MIW. All Rights Reserved.', '© 2026 MIW. All Rights Reserved. Originally compiled by Sandeep Lohan.'))),
     {'PEER_NAME_OUTSIDE_DISCLAIMER'}),
    ('N-A2b', 'footer loses the (c) 2026 MIW notice', True,
     lambda: attr_case(page_edit=(P20, _sub_region(C.FOOTER_RE, '© 2026 MIW. All Rights Reserved.', 'MIW.'))),
     {'ATTRIBUTION_POLICY'}),
    ('N-A3', 'page body claims the notes are approved by DGMA', True,
     lambda: attr_case(page_edit=(P20, _append_body('These notes are approved by DGMA for the MEO Class I oral.'))), {'ENDORSEMENT_CLAIM'}),
    ('N-A4', 'header calls the edition DGMA-approved', True,
     lambda: attr_case(page_edit=(P20, _sub_region(C.ATTRIB_STRIP_RE, C.EDITION + '.', C.EDITION + '. A DGMA-approved study edition.'))),
     {'ENDORSEMENT_CLAIM'}),
    ('N-A5', 'footer calls it an official DG Shipping publication', True,
     lambda: attr_case(page_edit=(P20, _sub_region(C.FOOTER_RE, 'See the', 'An official DG Shipping publication. See the'))),
     {'ENDORSEMENT_CLAIM'}),
    ('N-A6', 'header reads the edition date as the verification date', True,
     lambda: attr_case(page_edit=(P20, _sub_region(C.ATTRIB_STRIP_RE, 'Verified baseline: September 2026.', 'Verified baseline: October 2026.'))),
     {'ATTRIBUTION_POLICY', 'CURRENTNESS_CLAIM'}),
    ('N-A7', 'footer invents an original compilation date', True,
     lambda: attr_case(page_edit=(P20, _sub_region(C.FOOTER_RE, '© 2026 MIW. All Rights Reserved.',
                                                   '© 2026 MIW. All Rights Reserved. Originally compiled in 2012.'))),
     {'ORIGINAL_DATE_CLAIM'}),
    ('N-A8', 'header loses the disclaimer link', True,
     lambda: attr_case(page_edit=(P20, _sub_region(C.ATTRIB_STRIP_RE, 'href="index.html#miw-study-material-disclaimer"', 'href="index.html"'))),
     {'ATTRIBUTION_POLICY'}),
    # Renaming the anchor also un-exempts the block, so the clause-2 name is now outside it.
    ('N-A9', 'index loses the disclaimer block anchor', True,
     lambda: attr_case(index_edit=lambda h: h.replace(f'id="{C.DISCLAIMER_ANCHOR}"', 'id="disclaimer"')),
     {'ATTRIBUTION_POLICY', 'PEER_NAME_OUTSIDE_DISCLAIMER'}),
    ('N-P1', 'page body names the historical compiler', True,
     lambda: attr_case(page_edit=(P20, _append_body('Based on the notes of Sandeep Lohan.'))), {'PEER_NAME_OUTSIDE_DISCLAIMER'}),
    ('N-P2', 'index LOHAN section names the historical compiler outside the disclaimer block', True,
     lambda: attr_case(index_edit=lambda h: h.replace('<p class="series-attrib">', '<p class="series-attrib">After Lohan. ', 1)),
     {'PEER_NAME_OUTSIDE_DISCLAIMER'}),
    ('N-P3', 'manifest LOHAN attribution names the historical compiler', True,
     lambda: attr_case(man_attr=LOHAN_ATTR + ' Adapted from Lohan.'), {'PEER_NAME_OUTSIDE_DISCLAIMER'}),
    ('N-A10', 'manifest attribution drops the no-endorsement statement', True,
     lambda: attr_case(man_attr=LOHAN_ATTR.replace('not approved, endorsed or issued by DGMA', 'prepared for DGMA candidates')),
     {'ATTRIBUTION_POLICY'}),
    ('N-A11', 'manifest attribution claims IMO endorsement', True,
     lambda: attr_case(man_attr=LOHAN_ATTR + ' Endorsed by the IMO.'), {'ENDORSEMENT_CLAIM'}),
    # ---------------- disclaimer record
    ('N-D1', 'disclaimer record PENDING (the state of this candidate)', True,
     lambda: disclaimer_case({'title': 'D', 'status': 'PENDING_FOUNDER_TEXT', 'text_sha256': None}), {'DISCLAIMER_NOT_APPROVED'}),
    ('N-D2', 'disclaimer record missing', True, lambda: disclaimer_case(None), {'DISCLAIMER_NOT_APPROVED'}),
    ('P-D3', 'the Founder-approved v1.0 record, text file and rendered block pass', True,
     lambda: disclaimer_case(POLICY), set()),
    ('N-D7', 'approved record but the approved text file is not the pinned one', True,
     lambda: disclaimer_case(dict(POLICY, approved_text_sha256='0' * 64)), {'DISCLAIMER_NOT_APPROVED'}),
    ('N-D8', 'rendered block edited AND its sha256 re-recorded (forged record); approved file unchanged', True,
     lambda: disclaimer_case(dict(POLICY, text_sha256=hashlib.sha256(
         C.disclaimer_block_text(INDEX.replace('Not official.', 'Official.', 1)).encode('utf-8')).hexdigest()),
         INDEX.replace('Not official.', 'Official.', 1)), {'DISCLAIMER_NOT_APPROVED'}),
    ('N-D4', 'approved record, rendered block edited afterwards', True,
     lambda: disclaimer_case({'title': 'D', 'status': 'APPROVED', 'text_sha256': SYN_SHA},
                             SYN_INDEX.replace(APPROVED_TEXT, APPROVED_TEXT + ' Edited.')),
     {'DISCLAIMER_NOT_APPROVED'}),
    # Isolates the status rule: the real record and index with every hash correct, only the status
    # not APPROVED (otherwise a later hash check would mask a disabled status check: MG14).
    ('N-D6', 'record NOT approved even though every sha256 matches', True,
     lambda: disclaimer_case(dict(POLICY, status='PENDING_FOUNDER_TEXT')),
     {'DISCLAIMER_NOT_APPROVED'}),
    ('N-D6b', 'record NOT approved, synthetic block whose sha256 matches', True,
     lambda: disclaimer_case({'title': 'D', 'status': 'PENDING_FOUNDER_TEXT', 'text_sha256': SYN_SHA}, SYN_INDEX),
     {'DISCLAIMER_NOT_APPROVED'}),
    ('N-D5', 'approved record but the index still shows the pending block', True,
     lambda: disclaimer_case({'title': 'D', 'status': 'APPROVED', 'text_sha256': SYN_SHA}), {'DISCLAIMER_NOT_APPROVED'}),
]


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    out_json = argv[argv.index('--json') + 1] if '--json' in argv else None
    results, fails = [], 0
    print(f'(checkout LOHAN activated: {ACTIVATED}; {len(PAGES)} LOHAN pages)')
    if PROTECTED_UNAVAILABLE:
        print(f'PROTECTED_CONTENT_UNAVAILABLE: {len(PROTECTED_UNAVAILABLE)} LOHAN pages are in the private repo; '
              'cases that need them are N/A here and run in the private qualification')
    for cid, desc, needs, fn, expected in CASES:
        if needs and (not ACTIVATED or PROTECTED_UNAVAILABLE):
            why = 'needs an activated LOHAN series' if not ACTIVATED else 'PROTECTED_CONTENT_UNAVAILABLE'
            results.append({'id': cid, 'result': 'N/A', 'description': desc, 'summary': why})
            print(f'N/A   {cid:6} {desc}  ({why})')
            continue
        try:
            findings, changed = fn()
            got = codes(findings)
            proof = changed or cid.startswith('P-')
            ok = proof and set(got) == expected
            detail = f'required EXACTLY {sorted(expected)}; got {got}'
        except Exception as e:  # a case that cannot run is a failure, never a pass
            ok, got, detail, findings = False, [], f'ERROR {type(e).__name__}: {e}', []
        fails += 0 if ok else 1
        results.append({'id': cid, 'description': desc, 'result': 'PASS' if ok else 'FAIL', 'expected_codes': sorted(expected),
                        'reported_codes': got, 'summary': detail, 'findings': [list(x) for x in findings[:4]]})
        print(f"{'PASS' if ok else 'FAIL'}  {cid:6} {desc}  {detail}")
    ran = sum(1 for r in results if r['result'] != 'N/A')
    print(f'{ran - fails}/{ran} release-check cases PASS ({len(results) - ran} N/A)')
    if out_json:
        with open(out_json, 'w', encoding='utf-8') as fh:
            json.dump({'cases': results, 'pass': ran - fails, 'ran': ran, 'total': len(results)}, fh, ensure_ascii=False, indent=1)
    return 1 if fails or ran == 0 else 0


if __name__ == '__main__':
    sys.exit(main())
