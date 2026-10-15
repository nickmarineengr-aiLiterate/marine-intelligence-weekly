#!/usr/bin/env python3
"""check_notes_release.py — Notes manifest, entitlement and LOHAN attribution checks (D-L4 governance).

Bounded, additive checks for the Notes release. They change nothing and never reduce an existing
check; they are invoked by tools/notes/notes_release_gate.py (the proposed BLOCKING gate), not left
as optional scripts.

MANIFEST (meoclass1/oralnotes/notes_content_index.json)
  MANIFEST_DUPLICATE_KEY     a JSON object repeats a key (json.load would silently keep the last)
  MANIFEST_TOTAL_MISMATCH    total_files != the sum of the per-series file counts
  MANIFEST_DUPLICATE_PATH    one file name listed under two series
  MANIFEST_DUPLICATE_ID      two files of one series share a part number or a topic range
  MANIFEST_FILE_MISSING      a listed file is not on disk (a LOHAN page the public O-3 pin declares is
                             PROTECTED_CONTENT_UNAVAILABLE instead: its bytes live in the private repo)
  PROTECTED_CONTENT_UNAVAILABLE  --mode release or --require-protected, and a pin-declared LOHAN page is
                             absent: no release decision is made without the protected content
  COMPILER_MISMATCH          a series' compiler, extracted with F4's own rule, is not its authorised
                             compiler (lohan-notes -> none since the Founder rebrand of 15 Oct 2026;
                             each other series its own)
  COMPILER_RULE_DRIFT        F4's _COMPILER rule in tools/oral/test_notes_controls.py is not the rule
                             these checks were qualified against
GATE
  GATE_REFERENCE_DRIFT       build_part.GATE or validate_canonical.LOHAN_GATE differs from the pinned
                             reference text (sha256 below)
  LOHAN_GATE_NOT_EXACT       a listed LOHAN page lacks the exact gate once, first after <body>, or
                             still carries the review-copy stub
ENTITLEMENT
  ROUTE_ENTITLEMENT          api/_lib/routes.js does not resolve every LOHAN page, the manifest and
                             the index to ORAL_QB_NOTES (probed with node; no node = fail closed)
LOHAN ATTRIBUTION AND NOTICE (only when the series is listed in the manifest)
  Policy: Founder decisions of 15 Oct 2026 (FD-1 v1.0 and the series rebrand). The series is the
  independent "MIW MEO Class 1 Engineering Study Standard"; the historical peer acknowledgement
  lives ONLY in clause 2 of the approved disclaimer.
  ATTRIBUTION_POLICY         the manifest attribution, every page header strip, every page footer
                             or the index section lacks a required marker (series identity,
                             no-endorsement statement, verified baseline, disclaimer v1.0
                             reference and link; page footers also the (c) 2026 MIW notice)
  PEER_NAME_OUTSIDE_DISCLAIMER  the historical compiler's name appears in a page, in the LOHAN
                             manifest entry or in the index LOHAN section outside the disclaimer
                             block (it may appear only in disclaimer clause 2)
  CURRENTNESS_CLAIM          an attribution region presents the edition date (October 2026) as the
                             regulatory verification date
  ENDORSEMENT_CLAIM          an un-negated claim that the notes are approved / endorsed / issued /
                             certified by DGMA, DG Shipping, the MMD or the IMO (attribution regions;
                             page bodies only where the sentence is about this material)
  ORIGINAL_DATE_CLAIM        an attribution region states an original compilation date (unestablished)
  DISCLAIMER_NOT_APPROVED    the index disclaimer block is not the Founder-approved text recorded in
                             tools/notes/policy/study_material_disclaimer.json (status APPROVED and
                             an equal sha256), or the rendered block is not, word for word, the
                             approved text file whose own sha256 the policy pins. Release-blocking;
                             in --mode preview it is listed as a BLOCKER instead of a failure.
                             The approved block itself is exempt from the claim scans: its words
                             are the Founder's, bound by hash.

Usage:
  python tools/notes/check_notes_release.py [--mode preview|main|release] [--json OUT]
Tests: python tools/notes/test_check_notes_release.py
"""
from __future__ import annotations

import argparse
import hashlib
import html as htmlmod
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
NOTES_DIR_REL = 'meoclass1/oralnotes'
MANIFEST_REL = f'{NOTES_DIR_REL}/notes_content_index.json'
INDEX_REL = f'{NOTES_DIR_REL}/index.html'
POLICY_REL = 'tools/notes/policy/study_material_disclaimer.json'
F4_REL = 'tools/oral/test_notes_controls.py'

LOHAN_KEY = 'lohan-notes'
# Each series' authorised compiler as F4's rule extracts it (None: the series credits no compiler).
AUTHORISED_COMPILERS = {
    'simon-notes': 'Vignesh Siva',
    'current-topics': None,
    'engineering-management-notes': 'Uday Sankar S',
    LOHAN_KEY: None,  # Founder rebrand, 15 Oct 2026: the series credits no compiler on its pages
}
# F4's compiler rule, verbatim (tools/oral/test_notes_controls.py). Re-checked against the file.
COMPILER_RULE = r"Originally (?:compiled|prepared) by ([^.,<]+)"
COMPILER_RE = re.compile(COMPILER_RULE)
F4_RULE_LINE = '_COMPILER = re.compile(r"Originally (?:compiled|prepared) by ([^.,<]+)")'

# The house gate (build_part.GATE), pinned by text and by hash.
GATE_REFERENCE = '<script>if(!/miw_auth=1/.test(document.cookie)){window.location.replace("/SQ/pay.html");}</script>'
GATE_SHA256 = '8452a05a07b2f86af24c5e28924b776fcf80720a0840160851d1daf1156f36c6'
GATE_STUB = '<!-- GATE SCRIPT STRIPPED FOR REVIEW COPY -->'
REQUIRED_ENTITLEMENT = 'ORAL_QB_NOTES'

# Series identity policy (Founder, 15 Oct 2026; supersedes the 11 Oct MIW Modernised Edition
# policy). Markers are matched on visible text.
SERIES_NAME = 'MIW MEO Class 1 Engineering Study Standard'
EDITION = SERIES_NAME + ' — October 2026'  # the edition label; its date is not a verification date
POLICY_MARKERS = {
    'series identity': re.compile(re.escape(SERIES_NAME)),
    'no-endorsement statement': re.compile(r'\bnot approved, endorsed or issued by DGMA\b'),
    'disclaimer v1.0 reference': re.compile(r'MIW Study Material Disclaimer v1\.0'),
}
FOOTER_MARKERS = {
    'copyright notice': re.compile(re.escape('© 2026 MIW. All Rights Reserved.')),
}
# The historical compiler may be named ONLY in clause 2 of the approved disclaimer.
PEER_NAME_RE = re.compile(r'\bLohan\b')
BASELINE_MARKER = re.compile(r'Verified baseline: September 2026')
DISCLAIMER_ANCHOR = 'miw-study-material-disclaimer'
DISCLAIMER_LINK_RE = re.compile(r'href="index\.html#' + DISCLAIMER_ANCHOR + '"')

# Endorsement claims. A claim is acceptable only inside a sentence that negates it.
_BODIES = r'(?:DGMA|DG\s*Shipping|Directorate\s+General\s+of\s+(?:Shipping|Maritime\s+Administration)|MMD|Mercantile\s+Marine\s+Department|IMO)'
_VERBS = r'(?:approved|endorsed|issued|certified|accredited|sanctioned|authori[sz]ed|recogni[sz]ed|ratified)'
CLAIM_RES = [
    re.compile(r'\b%s\s+(?:\w+\s+){0,3}?by\s+(?:the\s+)?%s\b' % (_VERBS, _BODIES), re.I),
    re.compile(r'\b%s[-\s]%s\b' % (_BODIES, _VERBS), re.I),
    re.compile(r'\bofficial(?:ly)?\s+(?:\w+\s+){0,2}%s\b' % _BODIES, re.I),
    re.compile(r'\b%s\s+official\s+(?:notes|study|material|edition|publication)' % _BODIES, re.I),
]
# Page-body scope: only claims ABOUT this material (regulatory prose legitimately says "approved by
# the Administration", "MMD-approved institute"; those are not claims about the notes).
SELF_RE = re.compile(r'\b(?:these notes|this (?:edition|material|series|page)|MIW|Marine Intelligence Weekly|LOHAN Notes)\b', re.I)
NEGATION_RE = re.compile(r"\b(?:not|nor|no|never|neither|without|isn't|aren't)\b", re.I)
# The original compilation date is unestablished: no attribution region may state one.
ORIGINAL_DATE_RE = re.compile(r'\b(?:originally\s+)?compiled\b[^.;]{0,60}?\b(?:in|on|during|circa|c\.)\s+'
                              r'(?:\d{4}|(?:January|February|March|April|May|June|July|August|September|October|'
                              r'November|December)\s+\d{4})\b|\b(?:compiled|compilation)\s*(?:date)?\s*[:(]\s*\d{4}', re.I)
CURRENTNESS_RE = re.compile(r'\b(?:verified|baseline|current|up to date|updated)\b[^.]{0,40}\bOctober 2026\b'
                            r'|\bOctober 2026\b[^.]{0,20}\b(?:verified|baseline)\b', re.I)

_STRIP_RE = re.compile(r'<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>', re.S | re.I)
ATTRIB_STRIP_RE = re.compile(r'<div class="attribution-strip">(.*?)</div>', re.S)
FOOTER_RE = re.compile(r'<div class="page-footer">(.*?)</div>', re.S)
INDEX_SECTION_RE = re.compile(r'<div class="series-block" id="sec-lohan-notes">(.*?)(?=<div class="series-block"|</main>|\Z)', re.S)
DISCLAIMER_BLOCK_RE = re.compile(r'<div\b[^>]*\bid="miw-study-material-disclaimer"[^>]*>.*?</div>', re.S)
APPROVED_TEXT_REL = 'tools/notes/policy/study_material_disclaimer_v1.0.txt'


def text_of(fragment: str) -> str:
    s = _STRIP_RE.sub(' ', fragment)
    return re.sub(r'\s+', ' ', htmlmod.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def sentences(text: str) -> list:
    return [s for s in re.split(r'(?<=[.!?])\s+', text) if s]


def endorsement_claims(text: str, self_scope: bool = False) -> list:
    """Un-negated official-endorsement claims in `text`. With self_scope, only sentences that are
    about this material count (page bodies)."""
    out = []
    for s in sentences(text):
        if self_scope and not SELF_RE.search(s):
            continue
        for rx in CLAIM_RES:
            m = rx.search(s)
            if m and not NEGATION_RE.search(s):
                out.append(m.group(0))
    return out


def currentness_claims(text: str) -> list:
    """The edition date presented as a verification/currentness date."""
    return [m.group(0) for m in CURRENTNESS_RE.finditer(text.replace(EDITION, ''))]


def original_date_claims(text: str) -> list:
    return [m.group(0) for m in ORIGINAL_DATE_RE.finditer(text)]


def missing_policy_markers(text: str, need_baseline: bool = True) -> list:
    miss = [name for name, rx in POLICY_MARKERS.items() if not rx.search(text)]
    if need_baseline and not BASELINE_MARKER.search(text):
        miss.append('verified baseline (September 2026)')
    return miss


# --------------------------------------------------------------------------- manifest

def load_manifest(raw: str) -> tuple:
    """Return (manifest, duplicate-key findings)."""
    dups = []

    def hook(pairs):
        c = Counter(k for k, _ in pairs)
        dups.extend(k for k, n in c.items() if n > 1)
        return dict(pairs)
    return json.loads(raw, object_pairs_hook=hook), dups


PIN_REL = 'o3/lohan.pin.json'


def protected_declared(notes_dir: str | None) -> set:
    """Page names the public O-3 pin declares for the LOHAN mount (empty without a pin)."""
    if not notes_dir:
        return set()
    root = os.path.abspath(os.path.join(notes_dir, '..', '..'))
    pp = os.path.join(root, *PIN_REL.split('/'))
    if not os.path.isfile(pp):
        return set()
    with open(pp, encoding='utf-8') as fh:
        pin = json.load(fh)
    return {f['path'] for f in pin.get('deploy_files', [])}


def check_manifest(man: dict, dup_keys: list, notes_dir: str | None) -> list:
    F = []
    f = lambda code, msg: F.append((code, msg))
    for k in sorted(set(dup_keys)):
        f('MANIFEST_DUPLICATE_KEY', f'JSON key {k!r} repeated inside one object')
    series = man.get('series') or {}
    total = sum(len(s.get('files') or {}) for s in series.values())
    if man.get('total_files') != total:
        f('MANIFEST_TOTAL_MISMATCH', f'total_files {man.get("total_files")!r} != sum of series file counts {total}')
    owner = {}
    for sk, s in series.items():
        files = s.get('files') or {}
        parts, ranges = Counter(), Counter()
        for fn, meta in files.items():
            if fn in owner:
                f('MANIFEST_DUPLICATE_PATH', f'{fn} listed under {owner[fn]} and {sk}')
            owner.setdefault(fn, sk)
            if isinstance(meta, dict):
                if 'part' in meta:
                    parts[meta['part']] += 1
                if meta.get('topic_range'):
                    ranges[meta['topic_range']] += 1
            if notes_dir is not None and not os.path.isfile(os.path.join(notes_dir, fn)):
                if not (sk == LOHAN_KEY and fn in protected_declared(notes_dir)):
                    f('MANIFEST_FILE_MISSING', f'{sk}: {fn} is listed but not on disk')
        for p, n in parts.items():
            if n > 1:
                f('MANIFEST_DUPLICATE_ID', f'{sk}: part {p!r} appears on {n} files')
        for r, n in ranges.items():
            if n > 1:
                f('MANIFEST_DUPLICATE_ID', f'{sk}: topic range {r!r} appears on {n} files')
    for sk, s in series.items():
        m = COMPILER_RE.search(s.get('source_attribution') or '')
        got = m.group(1) if m else None
        if sk not in AUTHORISED_COMPILERS:
            f('COMPILER_MISMATCH', f'{sk}: series has no authorised-compiler entry (extracted {got!r})')
        elif got != AUTHORISED_COMPILERS[sk]:
            f('COMPILER_MISMATCH', f'{sk}: extracted compiler {got!r} != authorised {AUTHORISED_COMPILERS[sk]!r}')
    return F


def check_compiler_rule(f4_text: str) -> list:
    if f4_text.count(F4_RULE_LINE) != 1:
        return [('COMPILER_RULE_DRIFT', f'{F4_REL} no longer defines exactly {F4_RULE_LINE!r}')]
    return []


# --------------------------------------------------------------------------- gate

def gate_exact(page_html: str) -> bool:
    if page_html.count(GATE_REFERENCE) != 1 or GATE_STUB in page_html:
        return False
    m = re.search(r'<body\b[^>]*>\s*', page_html)
    return bool(m) and page_html.startswith(GATE_REFERENCE, m.end())


def check_gate_reference(build_gate: str, validator_gate: str) -> list:
    F = []
    if hashlib.sha256(GATE_REFERENCE.encode('utf-8')).hexdigest() != GATE_SHA256:
        F.append(('GATE_REFERENCE_DRIFT', 'the pinned GATE_REFERENCE text no longer matches GATE_SHA256'))
    for label, g in (('build_part.GATE', build_gate), ('validate_canonical.LOHAN_GATE', validator_gate)):
        if g != GATE_REFERENCE:
            F.append(('GATE_REFERENCE_DRIFT', f'{label} differs from the pinned gate reference'))
    return F


def check_lohan_gates(pages: dict) -> list:
    return [('LOHAN_GATE_NOT_EXACT', f'{fn}: gate not exactly once / first after <body> / stub present')
            for fn, h in sorted(pages.items()) if not gate_exact(h)]


# --------------------------------------------------------------------------- entitlement

def probe_routes(repo_root: str, paths: list) -> dict:
    node = shutil.which('node')
    if not node:
        raise RuntimeError('node not found')
    url = 'file:///' + os.path.join(repo_root, 'api', '_lib', 'routes.js').replace('\\', '/').lstrip('/')
    js = ('const m = await import(%s); const out = {};'
          'for (const p of %s) out[p] = m.requiredEntitlementForPath(p);'
          'process.stdout.write(JSON.stringify(out));') % (json.dumps(url), json.dumps(paths))
    r = subprocess.run([node, '--input-type=module', '-e', js], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:300])
    return json.loads(r.stdout)


def check_routes(resolved: dict) -> list:
    return [('ROUTE_ENTITLEMENT', f'{p} -> {v!r}, expected {REQUIRED_ENTITLEMENT!r}')
            for p, v in sorted(resolved.items()) if v != REQUIRED_ENTITLEMENT]


# --------------------------------------------------------------------------- attribution / notice

def region_claims(text: str, where: str) -> list:
    """Claims no attribution region may make: an edition date read as a verification date, an
    un-negated official endorsement, or an original compilation date (it is unestablished)."""
    out = [('CURRENTNESS_CLAIM', f'{where}: {c!r}') for c in currentness_claims(text)]
    out += [('ENDORSEMENT_CLAIM', f'{where}: {c!r}') for c in endorsement_claims(text)]
    out += [('ORIGINAL_DATE_CLAIM', f'{where}: {c!r}') for c in original_date_claims(text)]
    return out


def check_attribution(man_attr: str, pages: dict, index_html: str, man_text: str = '') -> list:
    F = []
    f = lambda code, msg: F.append((code, msg))
    miss = missing_policy_markers(man_attr, need_baseline=False)
    if miss:
        f('ATTRIBUTION_POLICY', f'manifest {LOHAN_KEY}.source_attribution lacks {miss}')
    if PEER_NAME_RE.search(man_text or man_attr):
        f('PEER_NAME_OUTSIDE_DISCLAIMER', f'manifest {LOHAN_KEY} entry names the historical compiler')
    F.extend(region_claims(man_attr, f'manifest {LOHAN_KEY}.source_attribution'))
    for fn, h in sorted(pages.items()):
        regions = {'header': ATTRIB_STRIP_RE.search(h), 'footer': FOOTER_RE.search(h)}
        for name, m in regions.items():
            if not m:
                f('ATTRIBUTION_POLICY', f'{fn}: no {name} attribution region')
                continue
            t = text_of(m.group(1))
            miss = missing_policy_markers(t)
            if name == 'footer':
                miss += [k for k, rx in FOOTER_MARKERS.items() if not rx.search(t)]
            if miss:
                f('ATTRIBUTION_POLICY', f'{fn} {name}: lacks {miss}')
            if not DISCLAIMER_LINK_RE.search(m.group(1)):
                f('ATTRIBUTION_POLICY', f'{fn} {name}: no link to index.html#{DISCLAIMER_ANCHOR}')
            F.extend(region_claims(t, f'{fn} {name}'))
        for c in endorsement_claims(text_of(h), self_scope=True):
            f('ENDORSEMENT_CLAIM', f'{fn} (page text about the material): {c!r}')
        if PEER_NAME_RE.search(text_of(h)):
            f('PEER_NAME_OUTSIDE_DISCLAIMER', f'{fn}: names the historical compiler')
    m = INDEX_SECTION_RE.search(index_html)
    if not m:
        f('ATTRIBUTION_POLICY', 'index: no #sec-lohan-notes section')
    else:
        t = text_of(DISCLAIMER_BLOCK_RE.sub(' ', m.group(1)))  # approved block: hash-bound, exempt
        miss = missing_policy_markers(t)
        if miss:
            f('ATTRIBUTION_POLICY', f'index LOHAN section lacks {miss}')
        if f'id="{DISCLAIMER_ANCHOR}"' not in index_html:
            f('ATTRIBUTION_POLICY', f'index: no disclaimer block id="{DISCLAIMER_ANCHOR}"')
        if PEER_NAME_RE.search(t):
            f('PEER_NAME_OUTSIDE_DISCLAIMER', 'index LOHAN section names the historical compiler outside the disclaimer block')
        F.extend(region_claims(t, 'index LOHAN section'))
    return F


def disclaimer_block_text(index_html: str):
    m = re.search(r'<div\b[^>]*\bid="%s"[^>]*>(.*?)</div>' % DISCLAIMER_ANCHOR, index_html, re.S)
    return text_of(m.group(1)) if m else None


def check_disclaimer(policy: dict | None, index_html: str, repo_root: str = REPO_ROOT) -> list:
    if not isinstance(policy, dict):
        return [('DISCLAIMER_NOT_APPROVED', f'{POLICY_REL} missing or unreadable')]
    block = disclaimer_block_text(index_html)
    if block is None:
        return [('DISCLAIMER_NOT_APPROVED', f'index has no #{DISCLAIMER_ANCHOR} block')]
    if policy.get('status') != 'APPROVED':
        return [('DISCLAIMER_NOT_APPROVED', f'{policy.get("title", "disclaimer")}: status {policy.get("status")!r}; the approved text is not on file')]
    sha = hashlib.sha256(block.encode('utf-8')).hexdigest()
    if sha != policy.get('text_sha256'):
        return [('DISCLAIMER_NOT_APPROVED', f'index disclaimer text sha256 {sha[:12]}… != approved {str(policy.get("text_sha256"))[:12]}…')]
    # The rendered block must be the approved text file word for word, and that file must be the
    # one whose sha256 the policy pins (the Founder-approved FD-1 v1.0 text).
    try:
        with open(os.path.join(repo_root, *APPROVED_TEXT_REL.split('/')), 'rb') as fh:
            raw = fh.read()
    except OSError:
        return [('DISCLAIMER_NOT_APPROVED', f'{APPROVED_TEXT_REL} missing')]
    if hashlib.sha256(raw).hexdigest() != policy.get('approved_text_sha256'):
        return [('DISCLAIMER_NOT_APPROVED', f'{APPROVED_TEXT_REL} sha256 != policy approved_text_sha256')]
    norm = lambda x: ' '.join(x.split())
    approved = norm('\n'.join(l for l in raw.decode('utf-8').split('\n') if l.strip() != 'Page footer:'))
    if norm(block) != approved:
        return [('DISCLAIMER_NOT_APPROVED', 'rendered disclaimer block != the approved v1.0 text')]
    return []


# --------------------------------------------------------------------------- runner

RELEASE_ONLY = {'DISCLAIMER_NOT_APPROVED'}


def run(repo_root: str = REPO_ROOT, mode: str = 'preview', require_protected: bool = False) -> dict:
    sys.path.insert(0, os.path.join(repo_root, 'tools', 'notes'))
    sys.path.insert(0, os.path.join(repo_root, 'tools', 'notes', 'canonical'))
    import build_part  # noqa: E402
    import validate_canonical as V  # noqa: E402
    findings = []
    notes_dir = os.path.join(repo_root, *NOTES_DIR_REL.split('/'))
    with open(os.path.join(repo_root, *MANIFEST_REL.split('/')), encoding='utf-8') as fh:
        man, dups = load_manifest(fh.read())
    findings += check_manifest(man, dups, notes_dir)
    with open(os.path.join(repo_root, *F4_REL.split('/')), encoding='utf-8') as fh:
        findings += check_compiler_rule(fh.read())
    findings += check_gate_reference(build_part.GATE, V.LOHAN_GATE)
    ser = (man.get('series') or {}).get(LOHAN_KEY)
    activated = isinstance(ser, dict)
    pages = {}
    if activated:
        for fn in sorted(ser.get('files') or {}):
            p = os.path.join(notes_dir, fn)
            if os.path.isfile(p):
                with open(p, encoding='utf-8') as fh:
                    pages[fn] = fh.read()
        findings += check_lohan_gates(pages)
    probe = [f'/{NOTES_DIR_REL}/{fn}' for fn in (sorted(pages) or ['lohan-notes-p1.html'])]
    probe += [f'/{MANIFEST_REL}', f'/{INDEX_REL}']
    try:
        resolved = probe_routes(repo_root, probe)
        findings += check_routes(resolved)
    except Exception as e:  # fail closed
        resolved = {}
        findings.append(('ROUTE_ENTITLEMENT', f'route probe could not run: {e}'))
    with open(os.path.join(repo_root, *INDEX_REL.split('/')), encoding='utf-8') as fh:
        index_html = fh.read()
    blockers = []
    if activated:
        findings += check_attribution(ser.get('source_attribution') or '', pages, index_html,
                                      json.dumps(ser, ensure_ascii=False))
        try:
            with open(os.path.join(repo_root, *POLICY_REL.split('/')), encoding='utf-8') as fh:
                policy = json.load(fh)
        except (OSError, ValueError):
            policy = None
        dis = check_disclaimer(policy, index_html, repo_root)
        if mode == 'preview':
            blockers += dis
        else:
            findings += dis
    unavailable = sorted(fn for fn in ((ser or {}).get('files') or {}) if fn not in pages
                         and fn in protected_declared(notes_dir)) if activated else []
    if unavailable and (mode == 'release' or require_protected):
        findings.append(('PROTECTED_CONTENT_UNAVAILABLE', f'{len(unavailable)} protected LOHAN page(s) absent: {unavailable[:3]}'))
    return {'mode': mode, 'lohan_activated': activated, 'lohan_pages_checked': len(pages),
            'protected_unavailable': unavailable,
            'routes': resolved, 'findings': findings, 'release_blockers': blockers,
            'manifest_total_files': man.get('total_files')}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--mode', choices=('preview', 'main', 'release'), default='preview',
                    help='preview lists release-only blockers without failing; main/release fail on them')
    ap.add_argument('--json', help='write the result as JSON')
    ap.add_argument('--require-protected', action='store_true',
                    help='O-3: fail when a pin-declared LOHAN page is absent (implied by --mode release)')
    a = ap.parse_args(argv)
    res = run(mode=a.mode, require_protected=a.require_protected)
    if res['protected_unavailable']:
        print(f'PROTECTED_CONTENT_UNAVAILABLE: {len(res["protected_unavailable"])} pin-declared LOHAN page(s) not in this '
              'checkout; their checks run in the private qualification')
    print(f'mode {res["mode"]}; LOHAN activated {res["lohan_activated"]}; LOHAN pages checked {res["lohan_pages_checked"]}; '
          f'routes probed {len(res["routes"])}; total_files {res["manifest_total_files"]}')
    for code, msg in res['findings']:
        print(f'  [FAIL ] {code}: {msg}')
    for code, msg in res['release_blockers']:
        print(f'  [BLOCK] {code}: {msg} (release-only; preview mode)')
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump(res, fh, ensure_ascii=False, indent=1)
    if res['findings']:
        print(f'RESULT: FAIL ({len(res["findings"])} finding(s))')
        return 1
    print('RESULT: PASS' + (f' with {len(res["release_blockers"])} release blocker(s)' if res['release_blockers'] else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
