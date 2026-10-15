#!/usr/bin/env python3
"""
validate_canonical.py — POST31-CA2 Layer 1 provenance resolver + Layer 3 status cores.

WHAT THIS GUARDS

Layer 1 identity for the MIW Engineering Management Notes ("Uday Notes") is the exact
published `file#anchor`, e.g.

    meoclass1/oralnotes/miw-notes-mgmt-p12.html#topic-51

It is never derived from a Part number, a topic badge, a TOC label, a version stamp or
an array position (FD-P1-02). Part 12 is the reason: its anchors are GLOBAL
(#topic-50 … #topic-54) while its badge, TOC and version stamp are LOCAL
("Part 12 · Topic 2", "T2", "P12-T2"), so a key computed from what the reader sees
points at the wrong node. Anchor strings alone are not unique across series either
(35 LOHAN/Uday collisions such as `topic-p13-1`), so a key without its file is unsafe.

Data validated (all in this directory):

    source_nodes.csv       one row per rendered Uday topic-block; key = file#anchor
    display_aliases.csv    badge / toc / version / phase1a_key -> exactly one key
    inbound_baseline.csv   every file-qualified reference to a Uday page, as data
    status/STATUS-*.json   Layer 3 status cores (data only; not rendered)

This is NOT a canonical subject-ID registry. No MERGE-### / PCT-* / CAND-* identifier
and no canonical subject id may appear here (FD-P1-11).

POST31 LOHAN SOURCE ADMISSION (10 Oct 2026). `LOHAN` is admitted as a second, SEPARATE
source series. Admission is source classification only:

  * source_nodes.csv carries 123 `series = LOHAN` rows keyed by the full
    `meoclass1/oralnotes/lohan-notes-p<N>.html#topic-p<N>-<n>` (publication_status
    SOURCE_COMPLETE_UNPUBLISHED). Uday rows are untouched.
  * inbound_baseline.csv records the LOHAN->Uday references. The referrer's series is
    derived from its path (lohan-notes pages and tools/notes/specs/lohan specs).
  * No LOHAN node may be an alias target, an inbound target or a status consumer: there
    is no Uday<->LOHAN relationship, equivalence or canonical subject id (D-L4 and the
    integration decision remain OPEN). Such use fails CROSS_SERIES_REFERENCE.
  * The original ban on LOHAN pages (LOHAN_ROW) is narrowed by FILE SCOPE, not loosened:
    only source_nodes.csv and inbound_baseline.csv may name LOHAN pages, and only
    well-formed rows of the admitted set (21 pages / 123 nodes) are accepted. Every other
    data file still fails LOHAN_ROW.
  * Admission does not publish. While a LOHAN page is absent from the tree its rows are
    checked structurally; the moment a page is present it is checked node-by-node against
    the rendered topic-blocks exactly as Uday pages are.

REVERSE-REFERENCE ISOLATION (audit F3, 10 Oct 2026). The live inbound scan above only sees
references whose TARGET is a Uday page, so a Uday page linking to a LOHAN page was never
examined. A second, referrer-driven scan now reads every Uday-series source file (the
published Parts, their SQ twins and their specs) for references to LOHAN pages, and the
policy is source-aware rather than a filename ban:

  * Every live Uday->LOHAN reference must equal a registered inbound_baseline.csv row
    (referrer file -> LOHAN file#anchor, with its count). Unregistered or page-level
    references fail CROSS_SERIES_UNREGISTERED; a target that is not a registered node of
    an admitted LOHAN page fails CROSS_SERIES_BAD_IDENTITY.
  * Whether a direction may be registered at all is a governance decision held in
    REGISTRABLE_DIRECTIONS. Today only LOHAN->Uday is registrable, so a Uday->LOHAN row
    still fails CROSS_SERIES_REFERENCE. Authorising the direction later is one reviewed
    line plus its rows; the live/registered checks then apply unchanged.
  * LOHAN->LOHAN navigation and references from non-series files (records, tools, hub
    indexes) are outside this rule. Nothing here infers a relationship.

LOHAN PUBLICATION STATE (D-L4 governance, 11 Oct 2026). The LOHAN series has ONE declared
state, LOHAN_SERIES_STATE, and every LOHAN row and every activation surface must agree with it:

  UNACTIVATED            production before D-L4: rows SOURCE_COMPLETE_UNPUBLISHED; the Notes
                         manifest and the Notes index do not list the series.
  PREVIEW_NONPUBLISHING  a local, nonpublishing rehearsal: rows SOURCE_COMPLETE_UNPUBLISHED; the
                         manifest and index list all 21 admitted pages but NOTHING presents them as
                         live. Never releasable (--release-candidate fails it).
  PUBLISHED_LIVE         the D-L4 release: rows PUBLISHED_LIVE, and the manifest, the index and the
                         exact page gate all carry the 21 admitted pages.

  * Rows disagreeing with the declared state fail BAD_PUBLICATION_STATUS; LOHAN rows that
    disagree with each other fail LOHAN_STATUS_MIXED.
  * UNPUBLISHED content shown as live (a "live" manifest status, a live badge or card on the
    index) fails LOHAN_UNPUBLISHED_SHOWN_LIVE.
  * An activated tree that still declares UNACTIVATED fails LOHAN_ACTIVATION_UNDECLARED; a
    manifest without the index (or the reverse) fails LOHAN_ACTIVATION_PARTIAL; an activated
    surface missing admitted pages fails LOHAN_ACTIVATION_INCOMPLETE.
  * PUBLISHED_LIVE without the complete manifest, index and exact gate on every page fails
    LOHAN_LIVE_WITHOUT_ACTIVATION.
  Changing the declared state is the D-F governance decision: one reviewed line plus the rows.

FAIL CLOSED. Any missing file, wrong header, unreadable row, unresolvable key, ambiguous
alias, broken inbound reference or unregistered rendered topic is an error. Exit 0 only
when the error list is empty.

Usage:
    python tools/notes/canonical/validate_canonical.py            # full validation
    python tools/notes/canonical/validate_canonical.py --no-live  # skip the live inbound re-scan
    python tools/notes/canonical/validate_canonical.py --release-candidate  # also refuse a preview state

The checks are pure functions over in-memory data (`validate`), so the mutation tests in
test_validate_canonical.py mutate copies in memory and never write files.
"""
from __future__ import annotations

import argparse
import copy
import csv
import html
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
STATUS_DIR = os.path.join(HERE, 'status')
CANON_REL = 'tools/notes/canonical/'

UDAY_DIR_REL = 'meoclass1/oralnotes'
UDAY_FILE_RE = re.compile(r'^meoclass1/oralnotes/miw-notes-mgmt-p(\d+)\.html$')
UDAY_GLOB_RE = re.compile(r'^miw-notes-mgmt-p(\d+)\.html$')
TOPIC_ANCHOR_RE = re.compile(r'^topic-(?:\d+|p\d+-\d+)$')
SHA_RE = re.compile(r'^[0-9a-f]{40}$')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')

# A file-qualified reference to a Uday page anywhere in the repository.
INBOUND_RE = re.compile(rb'miw-notes-mgmt-p(\d+)\.html#([A-Za-z0-9_\-]+)')

# Identifiers that must never enter this production layer.
FORBIDDEN_ID_RE = re.compile(r'\b(?:MERGE-\d{3}|PCT-[A-Z0-9][A-Z0-9-]*|CAND-[A-Z0-9][A-Z0-9-]*)\b')
FORBIDDEN_LOHAN_RE = re.compile(r'lohan-notes-p\d+\.html', re.I)

# POST31 LOHAN source admission. Only these two data files may name LOHAN pages.
LOHAN_FILE_RE = re.compile(r'^meoclass1/oralnotes/lohan-notes-p(\d+)\.html$')
LOHAN_GLOB_RE = re.compile(r'^lohan-notes-p(\d+)\.html$')
LOHAN_ANCHOR_RE = re.compile(r'^topic-p(\d+)-(\d+)$')
LOHAN_SPEC_RE = re.compile(r'^tools/notes/specs/lohan/p(\d+)\.json$')
LOHAN_REFERRER_LIKE_RE = re.compile(r'lohan-notes-|specs/lohan/', re.I)
LOHAN_PAGE_MENTION_RE = re.compile(r'lohan-notes-p(\d+)\.html', re.I)
ADMITTING_FILES = ('source_nodes.csv', 'inbound_baseline.csv')
# The admitted set. Changing it is a registry decision, not a data refresh.
LOHAN_ADMITTED_PAGES = frozenset(range(1, 22))
LOHAN_ADMITTED_NODES = 123

# Reverse-reference isolation (F3). Uday-series source files: published Parts, their SQ
# twins and their specs. A reference to a LOHAN page from one of these is cross-series.
UDAY_REFERRER_RE = re.compile(r'^(?:meoclass1/oralnotes|SQ)/miw-notes-mgmt-p(\d+)\.html$|^tools/notes/specs/p(\d+)\.json$')
LOHAN_TARGET_RE = re.compile(rb'lohan-notes-p(\d+)\.html(?:#([A-Za-z0-9_\-]+))?')

SOURCE_NODE_COLS = ['source_node_key', 'series', 'file', 'anchor', 'part', 'ordinal_in_part',
                    'title', 'anchor_scheme', 'publication_status', 'source_commit']
ALIAS_COLS = ['source_node_key', 'alias_type', 'alias_value', 'source']
INBOUND_COLS = ['referrer_file', 'target_source_node_key', 'count', 'source_commit']

SERIES = 'UDAY'
SERIES_LOHAN = 'LOHAN'
ADMITTED_SERIES = (SERIES, SERIES_LOHAN)
PUBLICATION_STATUS = 'PUBLISHED_LIVE'
UNPUBLISHED_STATUS = 'SOURCE_COMPLETE_UNPUBLISHED'
# The declared LOHAN publication state (see the module docstring). Changing it is the D-F
# governance decision, never a data refresh. This preview candidate declares a nonpublishing
# rehearsal; production (d8b48e8 / d504c03) is UNACTIVATED.
LOHAN_SERIES_STATES = ('UNACTIVATED', 'PREVIEW_NONPUBLISHING', 'PUBLISHED_LIVE')
LOHAN_SERIES_STATE = 'PUBLISHED_LIVE'


def required_status(series: str) -> str:
    """The publication_status every row of `series` must carry under the declared state."""
    if series == SERIES_LOHAN:
        return PUBLICATION_STATUS if LOHAN_SERIES_STATE == 'PUBLISHED_LIVE' else UNPUBLISHED_STATUS
    return PUBLICATION_STATUS


# Back-compatible names (read at import; validate() always calls required_status()).
LOHAN_PUBLICATION_STATUS = required_status(SERIES_LOHAN)
PUBLICATION_STATUS_BY_SERIES = {SERIES: PUBLICATION_STATUS, SERIES_LOHAN: LOHAN_PUBLICATION_STATUS}

# Activation surfaces. The gate text is pinned here AND in tools/notes/check_notes_release.py,
# which also proves it equals build_part.GATE, so a one-character change anywhere is caught.
NOTES_MANIFEST_REL = 'meoclass1/oralnotes/notes_content_index.json'
NOTES_INDEX_REL = 'meoclass1/oralnotes/index.html'
LOHAN_MANIFEST_KEY = 'lohan-notes'
LOHAN_INDEX_SECTION_RE = re.compile(r'<div class="series-block" id="sec-lohan-notes">(.*?)(?=<div class="series-block"|</main>|\Z)', re.S)
LOHAN_INDEX_LINK_RE = re.compile(r'href="(lohan-notes-p(\d+)\.html)"')
LIVE_CLAIM_RE = re.compile(r'\blive\b', re.I)
INDEX_LIVE_CLAIM_RE = re.compile(r'\b(?:sb|ncs)-live\b|✅\s*Live|\bLive\b')
LOHAN_GATE = '<script>if(!/miw_auth=1/.test(document.cookie)){window.location.replace("/SQ/pay.html");}</script>'
LOHAN_GATE_STUB = '<!-- GATE SCRIPT STRIPPED FOR REVIEW COPY -->'
# (referrer series, target series) pairs that may be REGISTERED in inbound_baseline.csv.
# LOHAN->UDAY was admitted by POST31 (10 Oct 2026). UDAY->LOHAN is not authorised: adding it
# is a governance decision (D-L4 / integration), never a data refresh.
REGISTRABLE_DIRECTIONS = frozenset({(SERIES_LOHAN, SERIES)})
# Alias types observed on the rendered page are page-scoped: the same "T2" exists in
# many Parts. Their lookup key is (file, type, value). phase1a_key is global.
PAGE_SCOPED_ALIAS_TYPES = ('badge', 'toc', 'version')
GLOBAL_ALIAS_TYPES = ('phase1a_key',)
ALIAS_TYPES = PAGE_SCOPED_ALIAS_TYPES + GLOBAL_ALIAS_TYPES
RENDERED_ALIAS_SOURCE = {'badge': 'rendered:topic-badge', 'toc': 'rendered:toc-link',
                         'version': 'rendered:topic-version'}

APPROVED_STATUS_IDS = ('STATUS-NZF', 'STATUS-HNS2010', 'STATUS-BWM')
STATUS_REQUIRED = ('status_id', 'subject', 'label', 'as_of', 'authority',
                   'authority_url_or_reference', 'history', 'next_decision_or_trigger',
                   'review_trigger', 'consumers')


def anchor_scheme_for(part: int, series: str = SERIES) -> str:
    if series == SERIES_LOHAN:
        return 'PART_LOCAL'
    if part <= 11:
        return 'GLOBAL'
    if part == 12:
        return 'GLOBAL_ANCHOR_LOCAL_LABELS'
    return 'PART_LOCAL'


# --------------------------------------------------------------------------- rendering

_BLOCK_RE = re.compile(r'<div\b[^>]*\bclass="topic-block"[^>]*>')
_ID_RE = re.compile(r'\bid="([^"]+)"')
_TITLE_RE = re.compile(r'<h2\b[^>]*class="topic-title"[^>]*>(.*?)</h2>', re.S)
_BADGE_RE = re.compile(r'<div\b[^>]*class="topic-badge"[^>]*>(.*?)</div>', re.S)
_VERSION_RE = re.compile(r'<(?:span|div)\b[^>]*class="topic-version"[^>]*>(.*?)</(?:span|div)>', re.S)
_TOC_RE = re.compile(r'<a\b[^>]*class="toc-link"[^>]*href="#([^"]+)"[^>]*>(.*?)</a>', re.S)
_ANY_ID_RE = re.compile(r'\bid="([^"]+)"')


def _text(fragment: str) -> str:
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', fragment))).strip()


def version_token(stamp: str) -> str:
    """'Notes-p12 · P12-T2 · v1.0' -> 'P12-T2'; 'Notes-p5 · T21 · v1.0' -> 'T21'."""
    parts = [p.strip() for p in stamp.split('·')]
    return parts[1] if len(parts) >= 3 else ''


def toc_token(label: str) -> str:
    """'T2 · BWM Convention (D-1/D-2)' -> 'T2'."""
    return label.split('·')[0].strip()


def scan_rendered(repo_root: str = REPO_ROOT) -> dict:
    """Return {file_rel: {'series','part','topics': [{anchor,title,badge,version,toc}], 'ids': set()}}
    for every Uday Part page and every LOHAN page present on disk (a LOHAN page is
    absent until its candidate lands; absence is not an error here)."""
    out = {}
    d = os.path.join(repo_root, *UDAY_DIR_REL.split('/'))
    for name in sorted(os.listdir(d)):
        m = UDAY_GLOB_RE.match(name)
        series = SERIES
        if not m:
            m = LOHAN_GLOB_RE.match(name)
            series = SERIES_LOHAN
        if not m:
            continue
        rel = f'{UDAY_DIR_REL}/{name}'
        with open(os.path.join(d, name), encoding='utf-8') as fh:
            s = fh.read()
        toc = {}
        for a, label in _TOC_RE.findall(s):
            toc.setdefault(a, toc_token(_text(label)))
        starts = [(mm.start(), mm.group(0)) for mm in _BLOCK_RE.finditer(s)]
        topics = []
        for i, (pos, tag) in enumerate(starts):
            idm = _ID_RE.search(tag)
            end = starts[i + 1][0] if i + 1 < len(starts) else len(s)
            seg = s[pos:end]
            t = _TITLE_RE.search(seg)
            b = _BADGE_RE.search(seg)
            v = _VERSION_RE.search(seg)
            anchor = idm.group(1) if idm else ''
            topics.append({
                'anchor': anchor,
                'title': _text(t.group(1)) if t else '',
                'badge': _text(b.group(1)) if b else '',
                'version': version_token(_text(v.group(1))) if v else '',
                'toc': toc.get(anchor, ''),
            })
        out[rel] = {'series': series, 'part': int(m.group(1)), 'topics': topics, 'ids': set(_ANY_ID_RE.findall(s))}
    return out


# --------------------------------------------------------------------------- inbound

PROTECTED_PIN_REL = 'o3/lohan.pin.json'


def protected_present(repo_root: str = REPO_ROOT) -> list:
    """O-3: the pin-declared protected pages that are present on disk (a private overlay or the
    production mount). They are never tracked in the public repository, but where present they
    are what production serves, so every governance scan must see them."""
    p = os.path.join(repo_root, *PROTECTED_PIN_REL.split('/'))
    if not os.path.isfile(p):
        return []
    with open(p, encoding='utf-8') as fh:
        pin = json.load(fh)
    mount = pin.get('mount', '')
    rels = [mount + f['path'] for f in pin.get('deploy_files', [])]
    # the private authoring specs (never mounted) ride with the overlay and are LOHAN referrers too
    rels += ['tools/notes/specs/lohan/p%d.json' % n for n in sorted(LOHAN_ADMITTED_PAGES)]
    return [r for r in rels if os.path.isfile(os.path.join(repo_root, *r.split('/')))]


def tracked_files(repo_root: str = REPO_ROOT) -> list:
    r = subprocess.run(['git', '-C', repo_root, 'ls-files', '-z'], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError('git ls-files failed: ' + r.stderr.decode('utf-8', 'replace'))
    files = [p for p in r.stdout.decode('utf-8').split('\0') if p]
    seen = set(files)
    return files + [p for p in protected_present(repo_root) if p not in seen]


def scan_inbound(repo_root: str = REPO_ROOT, files: list | None = None) -> Counter:
    """Counter{(referrer_file, 'meoclass1/oralnotes/miw-notes-mgmt-pN.html#anchor'): n}.
    Excludes this canonical directory (its own data would count itself)."""
    c = Counter()
    for rel in (files if files is not None else tracked_files(repo_root)):
        if rel.startswith(CANON_REL):
            continue
        p = os.path.join(repo_root, *rel.split('/'))
        if not os.path.isfile(p):
            continue
        with open(p, 'rb') as fh:
            data = fh.read()
        for part, anchor in INBOUND_RE.findall(data):
            key = f'{UDAY_DIR_REL}/miw-notes-mgmt-p{int(part)}.html#{anchor.decode("ascii")}'
            c[(rel, key)] += 1
    return c


def scan_cross_series(repo_root: str = REPO_ROOT, files: list | None = None) -> Counter:
    """Counter{(uday_referrer, 'meoclass1/oralnotes/lohan-notes-pN.html[#anchor]'): n} for every
    reference to a LOHAN page from a Uday-series source file. Page-level references (no
    anchor) are kept as the bare file so they can never match a node-level registration."""
    c = Counter()
    for rel in (files if files is not None else tracked_files(repo_root)):
        if not UDAY_REFERRER_RE.match(rel):
            continue
        p = os.path.join(repo_root, *rel.split('/'))
        if not os.path.isfile(p):
            continue
        with open(p, 'rb') as fh:
            data = fh.read()
        for part, anchor in LOHAN_TARGET_RE.findall(data):
            tgt = f'{UDAY_DIR_REL}/lohan-notes-p{int(part)}.html'
            c[(rel, f'{tgt}#{anchor.decode("ascii")}' if anchor else tgt)] += 1
    return c


def gate_exact(page_html: str) -> bool:
    """The house gate appears exactly once, there is no review-copy stub, and the gate is the
    first thing after <body> (whitespace only between them)."""
    if page_html.count(LOHAN_GATE) != 1 or LOHAN_GATE_STUB in page_html:
        return False
    m = re.search(r'<body\b[^>]*>\s*', page_html)
    return bool(m) and page_html.startswith(LOHAN_GATE, m.end())


def scan_activation(repo_root: str = REPO_ROOT) -> dict:
    """Evidence of how far the LOHAN series is activated, read from the tree:
    the Notes manifest entry, the Notes index section, and the exact gate on each page.
    Every field is plain data so the tests can construct any state in memory."""
    ev = {'manifest_series': False, 'manifest_files': [], 'manifest_live_claims': [],
          'manifest_error': '', 'nav_section': False, 'nav_files': [], 'nav_live_claims': [],
          'pages_on_disk': [], 'gated_exact': [], 'protected_unavailable': []}
    mp = os.path.join(repo_root, *NOTES_MANIFEST_REL.split('/'))
    try:
        with open(mp, encoding='utf-8') as fh:
            man = json.load(fh)
        ser = (man.get('series') or {}).get(LOHAN_MANIFEST_KEY)
    except (OSError, ValueError) as e:
        ev['manifest_error'] = str(e)
        ser = None
    if isinstance(ser, dict):
        ev['manifest_series'] = True
        files = ser.get('files') or {}
        ev['manifest_files'] = sorted(files)
        claims = [('series', str(ser.get('status', '')))]
        claims += [(f, str(v.get('status', ''))) for f, v in files.items() if isinstance(v, dict)]
        ev['manifest_live_claims'] = [f'{w}: {s}' for w, s in claims if LIVE_CLAIM_RE.search(s)]
    ip = os.path.join(repo_root, *NOTES_INDEX_REL.split('/'))
    if os.path.isfile(ip):
        with open(ip, encoding='utf-8') as fh:
            m = LOHAN_INDEX_SECTION_RE.search(fh.read())
        if m:
            ev['nav_section'] = True
            sec = m.group(1)
            ev['nav_files'] = sorted({f for f, _ in LOHAN_INDEX_LINK_RE.findall(sec)})
            ev['nav_live_claims'] = sorted(set(INDEX_LIVE_CLAIM_RE.findall(sec)))
    d = os.path.join(repo_root, *UDAY_DIR_REL.split('/'))
    for name in sorted(os.listdir(d)):
        if LOHAN_GLOB_RE.match(name):
            ev['pages_on_disk'].append(name)
            with open(os.path.join(d, name), encoding='utf-8') as fh:
                if gate_exact(fh.read()):
                    ev['gated_exact'].append(name)
    # O-3: a pin-declared page absent from this checkout is PROTECTED_CONTENT_UNAVAILABLE. Its gate
    # is attested by the pin (verified at package build and again at the production mount).
    pp = os.path.join(repo_root, *PROTECTED_PIN_REL.split('/'))
    if os.path.isfile(pp):
        with open(pp, encoding='utf-8') as fh:
            pin = json.load(fh)
        for f in pin.get('deploy_files', []):
            name = f['path']
            if LOHAN_GLOB_RE.match(name) and name not in ev['pages_on_disk']:
                ev['protected_unavailable'].append(name)
                ev['gated_exact'].append(name)
    return ev


def _lohan_page_set() -> set:
    return {f'lohan-notes-p{n}.html' for n in LOHAN_ADMITTED_PAGES}


def validate_publication_state(activation: dict, release_candidate: bool = False) -> list:
    """The declared-state rules over the activation evidence. Returns [(code, message)]."""
    E = []
    err = lambda code, msg: E.append((code, msg))
    state = LOHAN_SERIES_STATE
    if state not in LOHAN_SERIES_STATES:
        err('LOHAN_STATE_UNKNOWN', f'LOHAN_SERIES_STATE {state!r} is not one of {LOHAN_SERIES_STATES}')
        return E
    want = _lohan_page_set()
    man, nav = activation.get('manifest_series', False), activation.get('nav_section', False) or bool(activation.get('nav_files'))
    mfiles, nfiles = set(activation.get('manifest_files', [])), set(activation.get('nav_files', []))
    gated = set(activation.get('gated_exact', []))
    live_claims = list(activation.get('manifest_live_claims', [])) + list(activation.get('nav_live_claims', []))
    if activation.get('manifest_error'):
        err('LOHAN_ACTIVATION_UNREADABLE', f'Notes manifest unreadable: {activation["manifest_error"]}')
    if man != nav:
        err('LOHAN_ACTIVATION_PARTIAL', f'LOHAN listed in the Notes manifest={man} but in the Notes index={nav}; activation is one event')
    if (man or nav) and state == 'UNACTIVATED':
        err('LOHAN_ACTIVATION_UNDECLARED', 'the LOHAN series is activated in the tree but LOHAN_SERIES_STATE is UNACTIVATED (an activated series may not silently keep its unpublished state)')
    if state in ('UNACTIVATED', 'PREVIEW_NONPUBLISHING') and live_claims:
        err('LOHAN_UNPUBLISHED_SHOWN_LIVE', f'LOHAN is {state} but is presented as live: {live_claims[:3]}')
    if state == 'PREVIEW_NONPUBLISHING' and not (man and nav):
        err('LOHAN_PREVIEW_NOT_ACTIVATED', 'PREVIEW_NONPUBLISHING declared but the manifest/index do not both carry the series')
    if state in ('PREVIEW_NONPUBLISHING', 'PUBLISHED_LIVE'):
        for label, got in (('manifest', mfiles), ('index', nfiles)):
            if (man if label == 'manifest' else nav) and got != want:
                err('LOHAN_ACTIVATION_INCOMPLETE', f'{label} lists {len(got)} LOHAN pages != the {len(want)} admitted; missing {sorted(want - got)[:3]}, extra {sorted(got - want)[:3]}')
    if state == 'PUBLISHED_LIVE':
        missing = []
        if mfiles != want:
            missing.append(f'manifest {len(mfiles)}/{len(want)}')
        if nfiles != want:
            missing.append(f'index {len(nfiles)}/{len(want)}')
        if gated != want:
            missing.append(f'exact gate {len(gated & want)}/{len(want)} (ungated: {sorted(want - gated)[:3]})')
        if not activation.get('manifest_live_claims'):
            missing.append('manifest status does not say live')
        if missing:
            err('LOHAN_LIVE_WITHOUT_ACTIVATION', 'PUBLISHED_LIVE requires the activated manifest, index and gate: ' + '; '.join(missing))
    if release_candidate and state == 'PREVIEW_NONPUBLISHING':
        err('LOHAN_PREVIEW_NOT_RELEASABLE', 'a PREVIEW_NONPUBLISHING tree is never a release candidate')
    return E


# --------------------------------------------------------------------------- loading

def _read_csv(path: str, cols: list, errors: list, label: str) -> list:
    if not os.path.isfile(path):
        errors.append(('MISSING_FILE', f'{label}: {path} not found'))
        return []
    with open(path, encoding='utf-8', newline='') as fh:
        r = csv.reader(fh)
        rows = list(r)
    if not rows:
        errors.append(('EMPTY_FILE', f'{label}: no header'))
        return []
    if rows[0] != cols:
        errors.append(('BAD_HEADER', f'{label}: header {rows[0]} != {cols}'))
        return []
    out = []
    for i, row in enumerate(rows[1:], start=2):
        if len(row) != len(cols):
            errors.append(('BAD_ROW', f'{label} line {i}: {len(row)} fields, expected {len(cols)}'))
            continue
        out.append(dict(zip(cols, row)))
    if not out:
        errors.append(('EMPTY_FILE', f'{label}: header only'))
    return out


def load_registry(canon_dir: str = HERE) -> tuple:
    errors = []
    reg = {
        'source_nodes': _read_csv(os.path.join(canon_dir, 'source_nodes.csv'), SOURCE_NODE_COLS, errors, 'source_nodes.csv'),
        'aliases': _read_csv(os.path.join(canon_dir, 'display_aliases.csv'), ALIAS_COLS, errors, 'display_aliases.csv'),
        'inbound': _read_csv(os.path.join(canon_dir, 'inbound_baseline.csv'), INBOUND_COLS, errors, 'inbound_baseline.csv'),
        'status': {},
        'raw_text': {},
    }
    for name in ('source_nodes.csv', 'display_aliases.csv', 'inbound_baseline.csv'):
        p = os.path.join(canon_dir, name)
        if os.path.isfile(p):
            with open(p, encoding='utf-8') as fh:
                reg['raw_text'][name] = fh.read()
    sdir = os.path.join(canon_dir, 'status')
    if not os.path.isdir(sdir):
        errors.append(('MISSING_FILE', f'status directory {sdir} not found'))
    else:
        for name in sorted(os.listdir(sdir)):
            p = os.path.join(sdir, name)
            with open(p, encoding='utf-8') as fh:
                txt = fh.read()
            reg['raw_text'][f'status/{name}'] = txt
            if not name.endswith('.json'):
                errors.append(('STATUS_STRAY_FILE', f'status/{name} is not a .json status record'))
                continue
            try:
                reg['status'][name[:-5]] = json.loads(txt)
            except ValueError as e:
                errors.append(('STATUS_BAD_JSON', f'status/{name}: {e}'))
    return reg, errors


# --------------------------------------------------------------------------- validation

def split_key(key: str):
    """Return (file, anchor) for a well-formed key, else None. Anchor-only keys, keys
    without a Uday file component, or with an empty anchor are malformed."""
    if key.count('#') != 1:
        return None
    f, a = key.split('#')
    if not f or not a or not UDAY_FILE_RE.match(f):
        return None
    return f, a


def split_key_any(key: str):
    """Return (series, file, anchor) for a well-formed key of an admitted series, else None.
    A LOHAN key must be a lohan-notes file whose anchor is topic-p<N>-<n> with the SAME N."""
    if key.count('#') != 1:
        return None
    f, a = key.split('#')
    if not f or not a:
        return None
    if UDAY_FILE_RE.match(f):
        return SERIES, f, a
    m = LOHAN_FILE_RE.match(f)
    if m:
        am = LOHAN_ANCHOR_RE.match(a)
        if am and am.group(1) == m.group(1):
            return SERIES_LOHAN, f, a
    return None


def is_lohan_key(key) -> bool:
    return isinstance(key, str) and key.count('#') == 1 and bool(LOHAN_FILE_RE.match(key.split('#')[0]))


def referrer_series(path: str):
    """Classify an inbound referrer by path: ('LOHAN', page), ('LOHAN_UNKNOWN', None) for a
    lohan-looking path that is not a recognised LOHAN page/spec, ('UDAY', part) for a
    Uday-series source file, else ('OTHER', None)."""
    m = LOHAN_FILE_RE.match(path) or LOHAN_SPEC_RE.match(path)
    if m:
        return SERIES_LOHAN, int(m.group(1))
    if LOHAN_REFERRER_LIKE_RE.search(path):
        return 'LOHAN_UNKNOWN', None
    m = UDAY_REFERRER_RE.match(path)
    if m:
        return SERIES, int(m.group(1) or m.group(2))
    return 'OTHER', None


def validate(reg: dict, rendered: dict, live_inbound: Counter | None = None,
             live_cross: Counter | None = None, activation: dict | None = None,
             release_candidate: bool = False) -> list:
    """Pure function: returns a list of (code, message). Empty list == PASS.
    `activation` (scan_activation()) enables the publication-state rules; None skips them."""
    E = []
    err = lambda code, msg: E.append((code, msg))

    # ---- forbidden identifiers / LOHAN anywhere in the data
    for name, txt in reg.get('raw_text', {}).items():
        for m in sorted(set(FORBIDDEN_ID_RE.findall(txt))):
            err('FORBIDDEN_SUBJECT_ID', f'{name}: contains sandbox/canonical subject id {m}')
        if name in ADMITTING_FILES:
            # LOHAN pages may be named here, but only the admitted set (row-level rules below).
            for n in sorted({int(x) for x in LOHAN_PAGE_MENTION_RE.findall(txt)}):
                if n not in LOHAN_ADMITTED_PAGES:
                    err('LOHAN_PAGE_UNREGISTERED', f'{name}: names lohan-notes-p{n}.html, which is not an admitted LOHAN page')
        elif FORBIDDEN_LOHAN_RE.search(txt):
            err('LOHAN_ROW', f'{name}: references a LOHAN page (only source_nodes.csv / inbound_baseline.csv may; no relationships are authorised)')

    rendered_nodes = {}
    rendered_lohan = {}
    for f, info in rendered.items():
        is_lohan = info.get('series') == SERIES_LOHAN
        if is_lohan and info['part'] not in LOHAN_ADMITTED_PAGES:
            err('LOHAN_PAGE_UNREGISTERED', f'{f}: LOHAN page present in the tree but not an admitted page')
        for i, t in enumerate(info['topics'], start=1):
            if not t['anchor']:
                err('RENDERED_BLOCK_NO_ID', f'{f}: topic-block #{i} has no id')
                continue
            (rendered_lohan if is_lohan else rendered_nodes)[f'{f}#{t["anchor"]}'] = \
                dict(t, file=f, part=info['part'], ordinal=i)
    rendered_anchor_strings = {k.split('#')[1] for k in rendered_nodes}
    rendered_all = dict(rendered_nodes, **rendered_lohan)

    # ---- source_nodes (Uday + LOHAN)
    sn = reg.get('source_nodes', [])
    keys = [r['source_node_key'] for r in sn]
    keyset = set(keys)
    for k, n in Counter(keys).items():
        if n > 1:
            err('DUPLICATE_KEY', f'source_node_key {k} appears {n} times')
    registered = set()          # UDAY nodes: the only valid alias / inbound / status targets
    registered_lohan = set()    # LOHAN nodes: source classification only
    for r in sn:
        k = r['source_node_key']
        sk = split_key_any(k)
        if sk is None:
            if '#' not in k or k.startswith('#') or not k.split('#')[0]:
                err('KEY_WITHOUT_FILE', f'source_node_key {k!r} has no file component (anchor-only identity is rejected)')
            else:
                err('KEY_MALFORMED', f'source_node_key {k!r} is not <uday file>#<anchor> or <lohan file>#topic-p<N>-<n>')
            if r['series'] not in ADMITTED_SERIES:
                err('UNKNOWN_SERIES', f'{k}: series {r["series"]!r} is not an admitted source series {ADMITTED_SERIES}')
            continue
        kser, f, a = sk
        if kser == SERIES_LOHAN:
            if int(LOHAN_FILE_RE.match(f).group(1)) not in LOHAN_ADMITTED_PAGES:
                err('LOHAN_PAGE_UNREGISTERED', f'{k}: {f} is not an admitted LOHAN page')
        if r['file'] != f or r['anchor'] != a:
            err('KEY_FIELD_MISMATCH', f'{k}: key != file#anchor columns ({r["file"]}#{r["anchor"]})')
        if r['series'] not in ADMITTED_SERIES:
            err('UNKNOWN_SERIES', f'{k}: series {r["series"]!r} is not an admitted source series {ADMITTED_SERIES}')
        elif r['series'] != kser:
            err('BAD_SERIES', f'{k}: series {r["series"]!r} != {kser} (the series of its file)')
        if r['publication_status'] != required_status(kser):
            err('BAD_PUBLICATION_STATUS', f'{k}: publication_status {r["publication_status"]!r} != {required_status(kser)!r} (declared LOHAN state {LOHAN_SERIES_STATE})')
        if not SHA_RE.match(r['source_commit']):
            err('BAD_SOURCE_COMMIT', f'{k}: source_commit {r["source_commit"]!r} is not a 40-hex commit')
        node = rendered_all.get(k)
        file_part = int((UDAY_FILE_RE.match(f) or LOHAN_FILE_RE.match(f)).group(1))
        if node is None:
            if kser == SERIES_LOHAN and f not in rendered:
                # Admitted but not yet in the tree: no page is exposed. Structural checks only.
                registered_lohan.add(k)
                if r['part'] != str(file_part):
                    err('PART_MISMATCH', f'{k}: part {r["part"]} != {file_part} (from its file)')
                if r['ordinal_in_part'] != LOHAN_ANCHOR_RE.match(a).group(2):
                    err('ORDINAL_MISMATCH', f'{k}: ordinal_in_part {r["ordinal_in_part"]} != anchor ordinal {LOHAN_ANCHOR_RE.match(a).group(2)}')
                if not r['title'].strip():
                    err('TITLE_MISMATCH', f'{k}: empty title')
                if r['anchor_scheme'] != anchor_scheme_for(file_part, kser):
                    err('SCHEME_MISMATCH', f'{k}: anchor_scheme {r["anchor_scheme"]!r} != {anchor_scheme_for(file_part, kser)}')
            else:
                err('KEY_NOT_RENDERED', f'{k}: no rendered topic-block with this id in {f}')
            continue
        (registered if kser == SERIES else registered_lohan).add(k)
        if str(node['part']) != r['part']:
            err('PART_MISMATCH', f'{k}: part {r["part"]} != {node["part"]}')
        if str(node['ordinal']) != r['ordinal_in_part']:
            err('ORDINAL_MISMATCH', f'{k}: ordinal_in_part {r["ordinal_in_part"]} != rendered {node["ordinal"]}')
        if node['title'] != r['title']:
            err('TITLE_MISMATCH', f'{k}: title {r["title"]!r} != rendered {node["title"]!r}')
        if r['anchor_scheme'] != anchor_scheme_for(node['part'], kser):
            err('SCHEME_MISMATCH', f'{k}: anchor_scheme {r["anchor_scheme"]!r} != {anchor_scheme_for(node["part"], kser)}')
    for k in rendered_all:
        if k not in keyset:
            err('RENDERED_NOT_REGISTERED', f'rendered topic-block {k} is not in source_nodes.csv')

    # ---- LOHAN admitted-set pin (changing it is a registry decision, not a data refresh)
    lohan_rows = [r for r in sn if r['series'] == SERIES_LOHAN or is_lohan_key(r['source_node_key'])]
    lohan_pages = {r['file'] for r in lohan_rows}
    want_pages = {f'{UDAY_DIR_REL}/lohan-notes-p{n}.html' for n in LOHAN_ADMITTED_PAGES}
    if len(lohan_rows) != LOHAN_ADMITTED_NODES:
        err('LOHAN_ADMISSION_COUNT', f'{len(lohan_rows)} LOHAN source rows registered; the admitted set is {LOHAN_ADMITTED_NODES}')
    if lohan_pages != want_pages:
        err('LOHAN_ADMISSION_COUNT', f'LOHAN pages registered {len(lohan_pages)} != admitted {len(want_pages)}: missing {sorted(want_pages - lohan_pages)[:3]}, extra {sorted(lohan_pages - want_pages)[:3]}')
    # ---- LOHAN publication state: one status for the whole series, agreeing with the declaration
    lohan_statuses = Counter(r['publication_status'] for r in lohan_rows)
    if len(lohan_statuses) > 1:
        err('LOHAN_STATUS_MIXED', f'LOHAN rows carry mixed publication statuses {dict(lohan_statuses)}; the series has one state')
    if activation is not None:
        E.extend(validate_publication_state(activation, release_candidate))

    # ---- aliases
    al = reg.get('aliases', [])
    alias_values = set()
    lookup = defaultdict(set)
    seen_rows = Counter()
    for r in al:
        k, typ, val, src = r['source_node_key'], r['alias_type'], r['alias_value'], r['source']
        seen_rows[(k, typ, val)] += 1
        alias_values.add(val)
        if typ not in ALIAS_TYPES:
            err('ALIAS_BAD_TYPE', f'alias {val!r}: type {typ!r} not in {ALIAS_TYPES}')
            continue
        if not val:
            err('ALIAS_EMPTY', f'{k}: empty {typ} alias')
            continue
        if '#' in val or '.html' in val:
            err('ALIAS_LOOKS_LIKE_KEY', f'alias {val!r} has key form; aliases never become keys')
        if TOPIC_ANCHOR_RE.match(val) or val in rendered_anchor_strings:
            err('ALIAS_IS_ANCHOR', f'alias {val!r} equals an anchor string; aliases never become keys')
        if is_lohan_key(k):
            err('CROSS_SERIES_REFERENCE', f'alias {typ}={val!r} targets LOHAN node {k!r}; no alias or relationship is authorised for LOHAN')
            continue
        sk = split_key(k)
        if sk is None or k not in registered:
            err('ALIAS_UNRESOLVED', f'alias {typ}={val!r} targets unregistered/malformed key {k!r}')
            continue
        if typ in PAGE_SCOPED_ALIAS_TYPES:
            lookup[(sk[0], typ, val)].add(k)
            if src != RENDERED_ALIAS_SOURCE[typ]:
                err('ALIAS_BAD_SOURCE', f'{k}: {typ} alias source {src!r} != {RENDERED_ALIAS_SOURCE[typ]!r}')
            observed = rendered_nodes[k][typ]
            if observed != val:
                err('ALIAS_NOT_OBSERVED', f'{k}: {typ} alias {val!r} is not what the page renders for this node ({observed!r})')
        else:
            lookup[(typ, val)].add(k)
            if not src:
                err('ALIAS_BAD_SOURCE', f'{k}: {typ} alias has no source')
    for lk, ks in lookup.items():
        if len(ks) > 1:
            err('ALIAS_AMBIGUOUS', f'alias {lk} resolves to {len(ks)} nodes: {sorted(ks)}')
    for row, n in seen_rows.items():
        if n > 1:
            err('ALIAS_DUPLICATE_ROW', f'alias row {row} repeated {n} times')
    # completeness: every rendered label is recorded, so a reader-visible label always resolves
    have = {(r['source_node_key'], r['alias_type']) for r in al}
    for k, node in rendered_nodes.items():
        for typ in PAGE_SCOPED_ALIAS_TYPES:
            if node[typ] and (k, typ) not in have:
                err('ALIAS_MISSING', f'{k}: rendered {typ} {node[typ]!r} has no alias row')
    for k in keys:
        if k in alias_values:
            err('ALIAS_USED_AS_KEY', f'source_node_key {k!r} is also an alias value')

    # ---- P12: local labels must resolve to the REAL global anchors #topic-(49+n)
    p12 = f'{UDAY_DIR_REL}/miw-notes-mgmt-p12.html'
    # A P12-labelled alias ("Part 12 · Topic n", "P12-Tn", "U-P12-Tnn"), or any page-scoped
    # alias attached to a P12 node ("Tn"), means local topic n == #topic-(49+n).
    for r in al:
        val, k = r['alias_value'], r['source_node_key']
        m = re.fullmatch(r'(?:Part 12 · Topic |P12-T|U-P12-T)0*(\d+)', val)
        if m is None and k.startswith(p12 + '#') and r['alias_type'] in PAGE_SCOPED_ALIAS_TYPES:
            m = re.fullmatch(r'T(\d+)', val)
        if m is None:
            continue
        want = f'{p12}#topic-{49 + int(m.group(1))}'
        if k != want:
            err('P12_LOCAL_TO_WRONG_ANCHOR', f'P12 {r["alias_type"]} alias {val!r} -> {k}; must be {want}')

    # ---- inbound baseline
    ib = reg.get('inbound', [])
    pairs = Counter()
    for r in ib:
        t = r['target_source_node_key']
        pairs[(r['referrer_file'], t)] += 1
        if t in alias_values:
            err('ALIAS_USED_AS_KEY', f'inbound target {t!r} is an alias, not a key')
        rser, rpage = referrer_series(r['referrer_file'])
        if ('#' not in t or not t.split('#')[0]) and TOPIC_ANCHOR_RE.match(t.lstrip('#')):
            err('KEY_WITHOUT_FILE', f'inbound target {t!r} (from {r["referrer_file"]}) has no file component (anchor-only identity is rejected)')
        if is_lohan_key(t):
            if (rser, SERIES_LOHAN) not in REGISTRABLE_DIRECTIONS:
                err('CROSS_SERIES_REFERENCE', f'inbound target {t!r} is a LOHAN node; only LOHAN->Uday references are recorded (no Uday->LOHAN or LOHAN->LOHAN relationship is authorised)')
            elif t not in registered_lohan:
                err('CROSS_SERIES_BAD_IDENTITY', f'inbound target {t!r} (from {r["referrer_file"]}) is not a registered node of an admitted LOHAN page')
        elif t not in registered:
            err('INBOUND_BROKEN', f'inbound target {t!r} (from {r["referrer_file"]}) does not resolve to a registered node')
        if rser == 'LOHAN_UNKNOWN' or (rser == SERIES_LOHAN and rpage not in LOHAN_ADMITTED_PAGES):
            err('LOHAN_REFERRER_UNREGISTERED', f'inbound referrer {r["referrer_file"]} is not a recognised, admitted LOHAN page/spec')
        if not r['count'].isdigit() or int(r['count']) < 1:
            err('INBOUND_BAD_COUNT', f'{r["referrer_file"]} -> {t}: count {r["count"]!r}')
        if not SHA_RE.match(r['source_commit']):
            err('BAD_SOURCE_COMMIT', f'inbound {r["referrer_file"]}: source_commit {r["source_commit"]!r}')
        if r['referrer_file'].startswith(CANON_REL):
            err('INBOUND_SELF_REFERENCE', f'inbound referrer {r["referrer_file"]} is inside the canonical data directory')
    for p, n in pairs.items():
        if n > 1:
            err('INBOUND_DUPLICATE_ROW', f'inbound row {p} repeated {n} times')
    if live_inbound is not None:
        # LOHAN referrers present in the tree must match the baseline exactly (both ways).
        live_lohan = Counter()
        for (ref, t), n in live_inbound.items():
            rser, rpage = referrer_series(ref)
            if rser == 'LOHAN_UNKNOWN' or (rser == SERIES_LOHAN and rpage not in LOHAN_ADMITTED_PAGES):
                err('LOHAN_REFERRER_UNREGISTERED', f'{ref}: live reference(s) from an unadmitted LOHAN-looking file')
            elif rser == SERIES_LOHAN:
                live_lohan[(ref, t)] += n
        # Not vacuous: once LOHAN pages are rendered, zero live references is itself drift.
        if live_lohan or any(v.get('series') == SERIES_LOHAN for v in rendered.values()):
            base_lohan = Counter()
            for r in ib:
                if referrer_series(r['referrer_file'])[0] == SERIES_LOHAN and r['count'].isdigit():
                    base_lohan[(r['referrer_file'], r['target_source_node_key'])] += int(r['count'])
            if live_lohan != base_lohan:
                diff = sorted(set(live_lohan.items()) ^ set(base_lohan.items()))
                err('LOHAN_INBOUND_DRIFT', f'live LOHAN->Uday references != baseline ({sum(live_lohan.values())} vs {sum(base_lohan.values())}); first diffs {diff[:3]}')
        for (ref, t), n in sorted(live_inbound.items()):
            if t not in registered:
                f, a = t.split('#')
                ids = rendered.get(f, {}).get('ids', set())
                if TOPIC_ANCHOR_RE.match(a) or a not in ids:
                    err('LIVE_INBOUND_BROKEN', f'{ref}: {n} live reference(s) to {t} do not resolve')
    if live_cross is not None:
        # Reverse direction (F3): every live Uday->LOHAN reference must be a registered row,
        # and every registered Uday->LOHAN row must still be live. The registration itself is
        # only valid once its direction is in REGISTRABLE_DIRECTIONS (checked above).
        base_cross = Counter()
        for r in ib:
            if referrer_series(r['referrer_file'])[0] == SERIES and is_lohan_key(r['target_source_node_key']) \
                    and r['count'].isdigit():
                base_cross[(r['referrer_file'], r['target_source_node_key'])] += int(r['count'])
        live_u = Counter({k: n for k, n in live_cross.items() if referrer_series(k[0])[0] == SERIES})
        for (ref, t), n in sorted(live_u.items()):
            if '#' not in t:
                err('CROSS_SERIES_UNREGISTERED', f'{ref}: {n} page-level reference(s) to LOHAN page {t}; only a registered file#anchor node reference is admissible')
                continue
            if t not in registered_lohan:
                err('CROSS_SERIES_BAD_IDENTITY', f'{ref}: {n} live reference(s) to {t}, which is not a registered node of an admitted LOHAN page')
            if base_cross[(ref, t)] != n:
                err('CROSS_SERIES_UNREGISTERED', f'{ref}: {n} live Uday->LOHAN reference(s) to {t}; registered {base_cross[(ref, t)]}')
        for (ref, t), n in sorted(base_cross.items()):
            if (ref, t) not in live_u:
                err('CROSS_SERIES_DRIFT', f'registered Uday->LOHAN reference {ref} -> {t} (x{n}) is not live')

    # ---- status cores
    st = reg.get('status', {})
    for sid in APPROVED_STATUS_IDS:
        if sid not in st:
            err('STATUS_MISSING', f'status/{sid}.json not found')
    for stem, rec in st.items():
        if stem not in APPROVED_STATUS_IDS:
            err('STATUS_NOT_APPROVED', f'status/{stem}.json is not one of the approved cores {APPROVED_STATUS_IDS}')
        if not isinstance(rec, dict):
            err('STATUS_BAD_SHAPE', f'status/{stem}.json is not an object')
            continue
        for fld in STATUS_REQUIRED:
            if fld not in rec or rec[fld] in ('', None, [], {}):
                err('STATUS_FIELD_MISSING', f'{stem}: required field {fld!r} missing or empty')
        if rec.get('status_id') != stem:
            err('STATUS_ID_MISMATCH', f'{stem}: status_id {rec.get("status_id")!r} != file stem')
        if not DATE_RE.match(str(rec.get('as_of', ''))):
            err('STATUS_BAD_DATE', f'{stem}: as_of {rec.get("as_of")!r} is not YYYY-MM-DD')
        if not isinstance(rec.get('history', None), list):
            err('STATUS_BAD_SHAPE', f'{stem}: history must be a list')
        cons = rec.get('consumers', [])
        if not isinstance(cons, list):
            err('STATUS_BAD_SHAPE', f'{stem}: consumers must be a list')
            cons = []
        seen = Counter()
        for c in cons:
            k = c.get('source_node_key') if isinstance(c, dict) else None
            if not isinstance(k, str):
                err('STATUS_CONSUMER_BAD', f'{stem}: consumer {c!r} has no source_node_key string')
                continue
            seen[k] += 1
            if k in alias_values:
                err('ALIAS_USED_AS_KEY', f'{stem}: consumer {k!r} is an alias, not a key')
            if is_lohan_key(k):
                err('CROSS_SERIES_REFERENCE', f'{stem}: consumer {k!r} is a LOHAN node; status cores bind Uday nodes only')
            elif split_key(k) is None:
                err('STATUS_CONSUMER_BAD', f'{stem}: consumer {k!r} is not <uday file>#<anchor>')
            elif k not in registered:
                err('STATUS_CONSUMER_UNRESOLVED', f'{stem}: consumer {k} does not resolve to a registered node')
        for k, n in seen.items():
            if n > 1:
                err('STATUS_CONSUMER_DUPLICATE', f'{stem}: consumer {k} listed {n} times')
        hub = rec.get('teaching_hub')
        if is_lohan_key(hub):
            err('CROSS_SERIES_REFERENCE', f'{stem}: teaching_hub {hub!r} is a LOHAN node')
        elif hub is not None and hub not in registered:
            err('STATUS_CONSUMER_UNRESOLVED', f'{stem}: teaching_hub {hub!r} does not resolve')
    return E


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--no-live', action='store_true', help='skip the live inbound re-scan of tracked files')
    ap.add_argument('--release-candidate', action='store_true',
                    help='the tree is offered for release: a PREVIEW_NONPUBLISHING state fails')
    ap.add_argument('--require-protected', action='store_true',
                    help='O-3: the private overlay must be present; any PROTECTED_CONTENT_UNAVAILABLE page fails')
    args = ap.parse_args(argv)
    reg, errors = load_registry()
    rendered = scan_rendered()
    files = None if args.no_live else tracked_files()
    live = None if args.no_live else scan_inbound(files=files)
    cross = None if args.no_live else scan_cross_series(files=files)
    activation = scan_activation()
    errors += validate(reg, rendered, live, cross, activation, args.release_candidate)
    unavailable = activation.get('protected_unavailable', [])
    if unavailable:
        print(f'PROTECTED_CONTENT_UNAVAILABLE: {len(unavailable)} pin-declared LOHAN page(s) are not in this checkout; '
              'their content checks run in the private qualification (--require-protected)')
        if args.require_protected:
            errors.append(('PROTECTED_CONTENT_UNAVAILABLE', f'{len(unavailable)} protected LOHAN page(s) absent: {unavailable[:3]}'))
    uday_pages = {f: v for f, v in rendered.items() if v.get('series') == SERIES}
    lohan_pages = {f: v for f, v in rendered.items() if v.get('series') == SERIES_LOHAN}
    n_nodes = sum(len(v['topics']) for v in uday_pages.values())
    print(f'rendered Uday topic-blocks : {n_nodes} in {len(uday_pages)} Parts')
    print(f'rendered LOHAN topic-blocks: {sum(len(v["topics"]) for v in lohan_pages.values())} in {len(lohan_pages)} pages (0 = candidate pages not in tree; rows checked structurally)')
    by_series = Counter(r['series'] for r in reg['source_nodes'])
    print(f'source_nodes rows          : {len(reg["source_nodes"])} {dict(by_series)}')
    print(f'display_aliases rows       : {len(reg["aliases"])}')
    ib_total = sum(int(r["count"]) for r in reg["inbound"] if r["count"].isdigit())
    ib_lohan = sum(int(r["count"]) for r in reg["inbound"] if r["count"].isdigit() and referrer_series(r["referrer_file"])[0] == SERIES_LOHAN)
    print(f'inbound_baseline rows      : {len(reg["inbound"])} (refs {ib_total}; LOHAN-referrer refs {ib_lohan}; other {ib_total - ib_lohan})')
    if live is not None:
        live_l = sum(n for (ref, _), n in live.items() if referrer_series(ref)[0] == SERIES_LOHAN)
        print(f'live inbound references    : {sum(live.values())} across {len({r for r, _ in live})} referrer files (LOHAN referrers: {live_l})')
        reg_x = sum(int(r['count']) for r in reg['inbound'] if r['count'].isdigit()
                    and referrer_series(r['referrer_file'])[0] == SERIES and is_lohan_key(r['target_source_node_key']))
        n_scope = sum(1 for f in files if UDAY_REFERRER_RE.match(f))
        print(f'live Uday->LOHAN references: {sum(cross.values())} in {len({r for r, _ in cross})} of {n_scope} Uday source files scanned (registered: {reg_x})')
    print(f'status cores               : {sorted(reg["status"])}')
    print(f'LOHAN declared state       : {LOHAN_SERIES_STATE} (rows {dict(Counter(r["publication_status"] for r in reg["source_nodes"] if r["series"] == SERIES_LOHAN))}); '
          f'manifest {len(activation["manifest_files"])}, index {len(activation["nav_files"])}, exact gate {len(activation["gated_exact"])}/{len(activation["pages_on_disk"])} pages, '
          f'live claims {len(activation["manifest_live_claims"]) + len(activation["nav_live_claims"])}'
          f'{"; release-candidate mode" if args.release_candidate else ""}')
    for code, msg in errors:
        print(f'  [FAIL ] {code}: {msg}')
    if errors:
        print(f'RESULT: FAIL ({len(errors)} error(s))')
        return 1
    print('RESULT: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
