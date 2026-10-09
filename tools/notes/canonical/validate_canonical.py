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

This is NOT a canonical subject-ID registry. No MERGE-### / PCT-* / CAND-* identifier,
no LOHAN row and no canonical subject id may appear here (FD-P1-11; D-L4 open).

FAIL CLOSED. Any missing file, wrong header, unreadable row, unresolvable key, ambiguous
alias, broken inbound reference or unregistered rendered topic is an error. Exit 0 only
when the error list is empty.

Usage:
    python tools/notes/canonical/validate_canonical.py            # full validation
    python tools/notes/canonical/validate_canonical.py --no-live  # skip the live inbound re-scan

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

SOURCE_NODE_COLS = ['source_node_key', 'series', 'file', 'anchor', 'part', 'ordinal_in_part',
                    'title', 'anchor_scheme', 'publication_status', 'source_commit']
ALIAS_COLS = ['source_node_key', 'alias_type', 'alias_value', 'source']
INBOUND_COLS = ['referrer_file', 'target_source_node_key', 'count', 'source_commit']

SERIES = 'UDAY'
PUBLICATION_STATUS = 'PUBLISHED_LIVE'
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


def anchor_scheme_for(part: int) -> str:
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
    """Return {file_rel: {'topics': [{anchor,title,badge,version,toc}], 'ids': set()}}
    for every live Uday Part page on disk."""
    out = {}
    d = os.path.join(repo_root, *UDAY_DIR_REL.split('/'))
    for name in sorted(os.listdir(d)):
        m = UDAY_GLOB_RE.match(name)
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
        out[rel] = {'part': int(m.group(1)), 'topics': topics, 'ids': set(_ANY_ID_RE.findall(s))}
    return out


# --------------------------------------------------------------------------- inbound

def tracked_files(repo_root: str = REPO_ROOT) -> list:
    r = subprocess.run(['git', '-C', repo_root, 'ls-files', '-z'], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError('git ls-files failed: ' + r.stderr.decode('utf-8', 'replace'))
    return [p for p in r.stdout.decode('utf-8').split('\0') if p]


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


def validate(reg: dict, rendered: dict, live_inbound: Counter | None = None) -> list:
    """Pure function: returns a list of (code, message). Empty list == PASS."""
    E = []
    err = lambda code, msg: E.append((code, msg))

    # ---- forbidden identifiers / LOHAN anywhere in the data
    for name, txt in reg.get('raw_text', {}).items():
        for m in sorted(set(FORBIDDEN_ID_RE.findall(txt))):
            err('FORBIDDEN_SUBJECT_ID', f'{name}: contains sandbox/canonical subject id {m}')
        if FORBIDDEN_LOHAN_RE.search(txt):
            err('LOHAN_ROW', f'{name}: references a LOHAN page (D-L4 open; not permitted in CA2)')

    rendered_nodes = {}
    for f, info in rendered.items():
        for i, t in enumerate(info['topics'], start=1):
            if not t['anchor']:
                err('RENDERED_BLOCK_NO_ID', f'{f}: topic-block #{i} has no id')
                continue
            rendered_nodes[f'{f}#{t["anchor"]}'] = dict(t, file=f, part=info['part'], ordinal=i)
    rendered_anchor_strings = {k.split('#')[1] for k in rendered_nodes}

    # ---- source_nodes
    sn = reg.get('source_nodes', [])
    keys = [r['source_node_key'] for r in sn]
    for k, n in Counter(keys).items():
        if n > 1:
            err('DUPLICATE_KEY', f'source_node_key {k} appears {n} times')
    registered = set()
    for r in sn:
        k = r['source_node_key']
        sk = split_key(k)
        if sk is None:
            if '#' not in k or k.startswith('#') or not k.split('#')[0]:
                err('KEY_WITHOUT_FILE', f'source_node_key {k!r} has no file component (anchor-only identity is rejected)')
            else:
                err('KEY_MALFORMED', f'source_node_key {k!r} is not <uday file>#<anchor>')
            continue
        f, a = sk
        if r['file'] != f or r['anchor'] != a:
            err('KEY_FIELD_MISMATCH', f'{k}: key != file#anchor columns ({r["file"]}#{r["anchor"]})')
        if r['series'] != SERIES:
            err('BAD_SERIES', f'{k}: series {r["series"]!r} != {SERIES}')
        if r['publication_status'] != PUBLICATION_STATUS:
            err('BAD_PUBLICATION_STATUS', f'{k}: publication_status {r["publication_status"]!r}')
        if not SHA_RE.match(r['source_commit']):
            err('BAD_SOURCE_COMMIT', f'{k}: source_commit {r["source_commit"]!r} is not a 40-hex commit')
        node = rendered_nodes.get(k)
        if node is None:
            err('KEY_NOT_RENDERED', f'{k}: no rendered topic-block with this id in {f}')
            continue
        registered.add(k)
        if str(node['part']) != r['part']:
            err('PART_MISMATCH', f'{k}: part {r["part"]} != {node["part"]}')
        if str(node['ordinal']) != r['ordinal_in_part']:
            err('ORDINAL_MISMATCH', f'{k}: ordinal_in_part {r["ordinal_in_part"]} != rendered {node["ordinal"]}')
        if node['title'] != r['title']:
            err('TITLE_MISMATCH', f'{k}: title {r["title"]!r} != rendered {node["title"]!r}')
        if r['anchor_scheme'] != anchor_scheme_for(node['part']):
            err('SCHEME_MISMATCH', f'{k}: anchor_scheme {r["anchor_scheme"]!r} != {anchor_scheme_for(node["part"])}')
    for k in rendered_nodes:
        if k not in set(keys):
            err('RENDERED_NOT_REGISTERED', f'rendered topic-block {k} is not in source_nodes.csv')

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
        if t not in registered:
            err('INBOUND_BROKEN', f'inbound target {t!r} (from {r["referrer_file"]}) does not resolve to a registered node')
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
        for (ref, t), n in sorted(live_inbound.items()):
            if t not in registered:
                f, a = t.split('#')
                ids = rendered.get(f, {}).get('ids', set())
                if TOPIC_ANCHOR_RE.match(a) or a not in ids:
                    err('LIVE_INBOUND_BROKEN', f'{ref}: {n} live reference(s) to {t} do not resolve')

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
            if split_key(k) is None:
                err('STATUS_CONSUMER_BAD', f'{stem}: consumer {k!r} is not <uday file>#<anchor>')
            elif k not in registered:
                err('STATUS_CONSUMER_UNRESOLVED', f'{stem}: consumer {k} does not resolve to a registered node')
        for k, n in seen.items():
            if n > 1:
                err('STATUS_CONSUMER_DUPLICATE', f'{stem}: consumer {k} listed {n} times')
        hub = rec.get('teaching_hub')
        if hub is not None and hub not in registered:
            err('STATUS_CONSUMER_UNRESOLVED', f'{stem}: teaching_hub {hub!r} does not resolve')
    return E


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--no-live', action='store_true', help='skip the live inbound re-scan of tracked files')
    args = ap.parse_args(argv)
    reg, errors = load_registry()
    rendered = scan_rendered()
    live = None if args.no_live else scan_inbound()
    errors += validate(reg, rendered, live)
    n_nodes = sum(len(v['topics']) for v in rendered.values())
    print(f'rendered Uday topic-blocks : {n_nodes} in {len(rendered)} Parts')
    print(f'source_nodes rows          : {len(reg["source_nodes"])}')
    print(f'display_aliases rows       : {len(reg["aliases"])}')
    print(f'inbound_baseline rows      : {len(reg["inbound"])} (refs {sum(int(r["count"]) for r in reg["inbound"] if r["count"].isdigit())})')
    if live is not None:
        print(f'live inbound references    : {sum(live.values())} across {len({r for r, _ in live})} referrer files')
    print(f'status cores               : {sorted(reg["status"])}')
    for code, msg in errors:
        print(f'  [FAIL ] {code}: {msg}')
    if errors:
        print(f'RESULT: FAIL ({len(errors)} error(s))')
        return 1
    print('RESULT: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
