#!/usr/bin/env python3
"""
validate_status_consumers.py — POST31-CA3 page-side check for the Layer 3 status cores.

WHAT THIS GUARDS

validate_canonical.py checks the canonical DATA (source nodes, aliases, inbound
baseline, status records). This validator checks that the published Uday PAGES agree
with the status records, without the pages ever loading them:

    status/STATUS-*.json   machine currentness authority (repository only; 404 on the web)
    teaching node / hub    human explanation authority (e.g. P22 #topic-p22-3 for NZF)
    consumer marker        a static, dated "CURRENT STATUS" element on a consumer page:

        <div|span class="status-current" data-status-id="STATUS-NZF" data-as-of="2026-10-09">
          ... As of 9 October 2026: ... <label verbatim> ... <a href="miw-notes-mgmt-p22.html#topic-p22-3">
        </div|span>

Consumer declarations in each status record (consumers[]):
    role                 TEACHING_HUB | TEACHING_NODE | SPECIALISATION_STATUS_PROSE | STATUS_PROSE |
                         STATUS_DEPENDENT | POINTER
    marker               true  -> the consumer topic-block must carry exactly one marker for this status
                         false -> it must carry none
    requires_pointer_to  file#anchor the consumer must link to (for NZF: the teaching_hub)

Rules (error codes):
    SC_CONSUMER_UNRESOLVED   consumer / pointer target not in source_nodes.csv or not rendered
    SC_HUB_COUNT             teaching_hub present -> exactly one TEACHING_HUB consumer, equal to it;
                             no teaching_hub -> no TEACHING_HUB role at all
    SC_NZF_HUB_WRONG         STATUS-NZF teaching_hub is not P22 #topic-p22-3 (Founder R-CA2-4)
    SC_POINTER_TARGET_WRONG  requires_pointer_to is not the hub (NZF) / not a teaching consumer
    SC_HUB_POINTER_MISSING   the consumer (its marker, when it has one) lacks the required link
    SC_NZF_STATUS_POINTS_TO_P2  a consumer presents P2 #topic-9 as the NZF status authority
    SC_HNS_IN_FORCE_CLAIM    an HNS consumer says the 2010 HNS regime is in force before its EIF date
                             (dated correction sentences quoting the old wording are disclosures, not claims)
    SC_MARKER_NO_AS_OF       marker without a valid data-as-of, or without the matching visible date
    SC_MARKER_STALE          marker data-as-of != the status record's as_of
    SC_MARKER_LABEL          marker text does not carry the status record's label verbatim
    SC_MARKER_MISSING / SC_MARKER_UNDECLARED / SC_MARKER_DUPLICATE
    SC_LINK_UNRESOLVED       a Uday file#anchor link inside a consumer does not exist
    SC_PRIVATE_PATH          a page references the repository status JSON / canonical directory
    SC_UNKNOWN_STATUS_ID     a page uses a status id that is not an approved core
    SC_CANONICAL_ID_ON_PAGE  a page carries MERGE-### / PCT-* / CAND-* / CANON-* identifiers

No internet access. FAIL CLOSED: exit 0 only with an empty error list.

Usage:
    python tools/notes/canonical/validate_status_consumers.py
"""
from __future__ import annotations

import datetime as _dt
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import validate_canonical as V  # noqa: E402  (shared loaders; one definition of a node key)

NZF_HUB = 'meoclass1/oralnotes/miw-notes-mgmt-p22.html#topic-p22-3'
P2_T9 = 'meoclass1/oralnotes/miw-notes-mgmt-p2.html#topic-9'
TEACHING_ROLES = ('TEACHING_HUB', 'TEACHING_NODE')
ROLES = TEACHING_ROLES + ('SPECIALISATION_STATUS_PROSE', 'STATUS_PROSE', 'STATUS_DEPENDENT', 'POINTER')
MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
          'September', 'October', 'November', 'December')

_MARKER_OPEN = re.compile(r'<(div|span)\b([^>]*\bdata-status-id="([^"]*)"[^>]*)>')
_ATTR = lambda name: re.compile(r'\b' + name + r'="([^"]*)"')
_HREF = re.compile(r'href="([^"]*)"')
_UDAY_HREF = re.compile(r'^(?:\./)?(?:/?meoclass1/oralnotes/)?(miw-notes-mgmt-p(\d+)\.html)#([A-Za-z0-9_\-]+)$')
_PRIVATE = re.compile(r'tools/notes/canonical|status/STATUS-[A-Za-z0-9-]+\.json|STATUS-[A-Z0-9-]+\.json')
_STATUS_TOKEN = re.compile(r'\bSTATUS-[A-Z0-9][A-Z0-9-]*\b')
_CANON_ID = re.compile(r'\b(?:MERGE-\d{3}|PCT-[A-Z0-9][A-Z0-9-]*|CAND-[A-Z0-9][A-Z0-9-]*|CANON-[A-Z0-9][A-Z0-9-]*)\b')
_BLOCK_START = re.compile(r'<div\b[^>]*\bclass="topic-block"[^>]*\bid="([^"]+)"[^>]*>')

# P2-T9 named as the place the Net-Zero Framework STATUS lives.
_P2_REF = re.compile(r'miw-notes-mgmt-p2\.html#topic-9|\bPart 2\s*(?:·\s*)?Topic 9\b|\bP2-T9\b')
_HUB_REF = re.compile(r'miw-notes-mgmt-p22\.html#topic-p22-3|\bPart 22\s*(?:·\s*)?Topic 3\b|\bP22-T3\b')
_NZF_WORD = re.compile(r'Net-Zero Framework|\bNZF\b|\bstatus\b', re.I)

# HNS in-force claims and the qualifiers that make a sentence a correct statement.
_HNS = re.compile(r'\bHNS\b')
_IN_FORCE = re.compile(r'\b(?:entered into force|came into force|is (?:now )?in force|now in force|in force since|'
                       r'became effective|governs|in force)\b', re.I)
_QUALIFIER = re.compile(r'not (?:yet )?in force|\bscheduled\b|\bonce\b|\bwhen (?:it is )?in force|\bwill\b|\buntil\b|'
                        r'\bnever\b|\bnot yet\b|29 Nov(?:ember)? 2027|\bOPRC-HNS\b|\bif\b', re.I)
# A dated correction that quotes the old wrong wording is a disclosure, not a claim.
_REFUTATION = re.compile(r'\bearlier versions?\b|\bpreviously (?:said|stated)\b|\bwas wrong\b|^Correction\b', re.I)


def human_date(iso: str) -> str:
    d = _dt.date.fromisoformat(iso)
    return f'{d.day} {MONTHS[d.month - 1]} {d.year}'


def text_of(fragment: str) -> str:
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', fragment))).strip()


def sentences(fragment: str) -> list:
    t = re.sub(r'<(?:br|/p|/li|/tr|/td|/div|/h\d)\b[^>]*>', ' ¶ ', fragment)
    out = []
    for chunk in text_of(t).split('¶'):
        out += [s.strip() for s in re.split(r'(?<=[.!?])\s+', chunk) if s.strip()]
    return out


def sentences_raw(fragment: str) -> list:
    """Sentence split that keeps hrefs, so a link counts as a reference."""
    t = re.sub(r'<a\b[^>]*href="([^"]*)"[^>]*>', lambda m: f' [{m.group(1)}] ', fragment)
    return sentences(t)


def find_markers(fragment: str) -> list:
    """[(tag, attrs, status_id, inner_html)] with nesting-aware closing for the same tag."""
    out = []
    for m in _MARKER_OPEN.finditer(fragment):
        tag = m.group(1)
        depth, pos = 1, m.end()
        tok = re.compile(r'<(/?)' + tag + r'\b[^>]*>')
        end = None
        for t in tok.finditer(fragment, pos):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                end = t.start()
                break
        inner = fragment[m.end():end] if end is not None else fragment[m.end():]
        out.append((tag, m.group(2), m.group(3), inner))
    return out


def topic_blocks(page_html: str) -> dict:
    st = [(mm.start(), mm.group(1)) for mm in _BLOCK_START.finditer(page_html)]
    out = {}
    for i, (p, a) in enumerate(st):
        e = st[i + 1][0] if i + 1 < len(st) else len(page_html)
        out[a] = page_html[p:e]
    return out


def load_pages(repo_root: str = V.REPO_ROOT) -> dict:
    d = os.path.join(repo_root, *V.UDAY_DIR_REL.split('/'))
    pages = {}
    for name in sorted(os.listdir(d)):
        if V.UDAY_GLOB_RE.match(name):
            with open(os.path.join(d, name), encoding='utf-8') as fh:
                pages[f'{V.UDAY_DIR_REL}/{name}'] = fh.read()
    return pages


def resolve_href(href: str):
    m = _UDAY_HREF.match(href)
    return f'{V.UDAY_DIR_REL}/{m.group(1)}#{m.group(3)}' if m else None


def validate(status: dict, node_keys: set, pages: dict) -> list:
    """Pure function. status = {stem: record}; node_keys = source_node_key set; pages = {file: html}."""
    E = []
    err = lambda code, msg: E.append((code, msg))
    approved = set(V.APPROVED_STATUS_IDS)
    blocks = {f: topic_blocks(h) for f, h in pages.items()}
    ids = {f: set(V._ANY_ID_RE.findall(h)) for f, h in pages.items()}

    def block_of(key):
        f, a = key.split('#', 1)
        return blocks.get(f, {}).get(a)

    # ---- page-wide hygiene: private paths, unknown status ids, canonical subject ids
    declared_markers = {}   # (file, anchor, sid) -> True
    for f, h in pages.items():
        for m in sorted(set(_PRIVATE.findall(h))):
            err('SC_PRIVATE_PATH', f'{f}: references repository status data {m!r} (not a public route)')
        for tok in sorted(set(_STATUS_TOKEN.findall(h))):
            if tok not in approved:
                err('SC_UNKNOWN_STATUS_ID', f'{f}: status id {tok!r} is not an approved core')
        for m in sorted(set(_CANON_ID.findall(h))):
            err('SC_CANONICAL_ID_ON_PAGE', f'{f}: carries canonical/subject id {m!r} (no canonical-ID freeze yet)')
        for a, b in blocks[f].items():
            for _, _, sid, _ in find_markers(b):
                declared_markers.setdefault((f, a, sid), 0)
                declared_markers[(f, a, sid)] += 1
        outside = len(find_markers(h)) - sum(n for (ff, _, _), n in declared_markers.items() if ff == f)
        if outside:
            err('SC_MARKER_UNDECLARED', f'{f}: {outside} status marker(s) outside any topic-block')

    consumers_by_sid = {}
    for stem, rec in status.items():
        sid = rec.get('status_id', stem)
        if sid not in approved:
            err('SC_UNKNOWN_STATUS_ID', f'status record {stem}: {sid!r} is not an approved core')
            continue
        cons = [c for c in rec.get('consumers', []) if isinstance(c, dict)]
        consumers_by_sid[sid] = {c.get('source_node_key'): c for c in cons}
        as_of = str(rec.get('as_of', ''))
        label = rec.get('label', '')
        hub = rec.get('teaching_hub')

        # ---- rule 2/3: hubs
        hubs = [c['source_node_key'] for c in cons if c.get('role') == 'TEACHING_HUB']
        if hub is not None:
            if hubs != [hub]:
                err('SC_HUB_COUNT', f'{sid}: teaching_hub {hub} but TEACHING_HUB consumers = {hubs}')
        elif hubs:
            err('SC_HUB_COUNT', f'{sid}: TEACHING_HUB role used without a teaching_hub field: {hubs}')
        if sid == 'STATUS-NZF' and hub != NZF_HUB:
            err('SC_NZF_HUB_WRONG', f'STATUS-NZF teaching_hub {hub!r} != {NZF_HUB} (Founder R-CA2-4)')

        for c in cons:
            key = c.get('source_node_key')
            role = c.get('role')
            if role not in ROLES:
                err('SC_CONSUMER_UNRESOLVED', f'{sid}: consumer {key} has unknown role {role!r}')
            # ---- rule 1
            if key not in node_keys or block_of(key) is None:
                err('SC_CONSUMER_UNRESOLVED', f'{sid}: consumer {key} does not resolve to a registered, rendered node')
                continue
            b = block_of(key)
            f = key.split('#')[0]
            markers = [mk for mk in find_markers(b) if mk[2] == sid]
            want = c.get('marker')
            if want is True and not markers:
                err('SC_MARKER_MISSING', f'{sid}: {key} declares marker=true but carries no marker')
            if want is not True and markers:
                err('SC_MARKER_UNDECLARED', f'{sid}: {key} carries a marker but does not declare marker=true')
            if len(markers) > 1:
                err('SC_MARKER_DUPLICATE', f'{sid}: {key} carries {len(markers)} markers')

            # ---- rule 7 + label/staleness
            for tag, attrs, _, inner in markers:
                a = _ATTR('data-as-of').search(attrs)
                visible = text_of(inner)
                if not a or not V.DATE_RE.match(a.group(1)):
                    err('SC_MARKER_NO_AS_OF', f'{sid}: {key} marker has no valid data-as-of')
                else:
                    try:
                        hd = human_date(a.group(1))
                    except ValueError:
                        err('SC_MARKER_NO_AS_OF', f'{sid}: {key} marker data-as-of {a.group(1)!r} is not a date')
                        hd = None
                    if hd and not re.search(r'\bas of ' + re.escape(hd) + r'\b', visible, re.I):
                        err('SC_MARKER_NO_AS_OF', f'{sid}: {key} marker does not show "As of {hd}"')
                    if a.group(1) != as_of:
                        err('SC_MARKER_STALE', f'{sid}: {key} marker as-of {a.group(1)} != record as_of {as_of}')
                if label and label not in visible:
                    err('SC_MARKER_LABEL', f'{sid}: {key} marker does not carry the label {label!r}')

            # ---- rule 4: pointer
            tgt = c.get('requires_pointer_to')
            if tgt is not None:
                tc = consumers_by_sid[sid].get(tgt)
                if sid == 'STATUS-NZF' and tgt != hub:
                    err('SC_POINTER_TARGET_WRONG', f'{sid}: {key} must point to the hub {hub}, not {tgt}')
                elif tc is None or tc.get('role') not in TEACHING_ROLES:
                    err('SC_POINTER_TARGET_WRONG', f'{sid}: {key} pointer target {tgt} is not a teaching consumer of {sid}')
                if tgt not in node_keys:
                    err('SC_CONSUMER_UNRESOLVED', f'{sid}: pointer target {tgt} is not a registered node')
                scope = markers[0][3] if markers else b
                links = {resolve_href(h) for h in _HREF.findall(scope)}
                if tgt not in links:
                    where = 'its marker' if markers else 'its topic-block'
                    err('SC_HUB_POINTER_MISSING', f'{sid}: {key} — {where} has no link to {tgt}')

            # ---- M5: every Uday file#anchor link in the consumer resolves
            for h in _HREF.findall(b):
                k = resolve_href(h)
                if k is None:
                    continue
                tf, ta = k.split('#')
                if tf not in pages or ta not in ids[tf]:
                    err('SC_LINK_UNRESOLVED', f'{sid}: {key} links to {h!r}, which does not exist')

            # ---- rule 5: NZF status must never be attributed to P2-T9
            if sid == 'STATUS-NZF' and key not in (hub, P2_T9):
                for _, _, _, inner in markers:
                    if P2_T9 in {resolve_href(h) for h in _HREF.findall(inner)}:
                        err('SC_NZF_STATUS_POINTS_TO_P2', f'{key}: NZF status marker links to {P2_T9}')
                for s in sentences_raw(b):
                    if _P2_REF.search(s) and _NZF_WORD.search(s) and not _HUB_REF.search(s):
                        err('SC_NZF_STATUS_POINTS_TO_P2', f'{key}: presents Part 2 Topic 9 as the NZF reference: {s[:140]!r}')

            # ---- rule 6: HNS not in force before its scheduled EIF
            if sid == 'STATUS-HNS2010':
                eif = (rec.get('status_detail') or {}).get('entry_into_force', '')
                if V.DATE_RE.match(eif) and as_of < eif:
                    for s in sentences(b):
                        if _REFUTATION.search(s):
                            continue
                        if _HNS.search(s) and _IN_FORCE.search(s) and not _QUALIFIER.search(s):
                            err('SC_HNS_IN_FORCE_CLAIM', f'{key}: HNS stated as in force before {eif}: {s[:140]!r}')

    # ---- markers on pages that no record declares
    for (f, a, sid), n in declared_markers.items():
        key = f'{f}#{a}'
        if sid in approved and key not in consumers_by_sid.get(sid, {}):
            err('SC_MARKER_UNDECLARED', f'{key}: carries a {sid} marker but is not a {sid} consumer')
    return E


def main(argv=None) -> int:
    reg, errors = V.load_registry()
    node_keys = {r['source_node_key'] for r in reg['source_nodes']}
    pages = load_pages()
    errors = [e for e in errors if e[0].startswith('STATUS') or e[0] == 'MISSING_FILE'] + validate(reg['status'], node_keys, pages)
    n_markers = sum(len(find_markers(h)) for h in pages.values())
    n_cons = sum(len(r.get('consumers', [])) for r in reg['status'].values())
    print(f'Uday pages scanned          : {len(pages)}')
    print(f'status cores                : {sorted(reg["status"])}')
    print(f'declared consumers          : {n_cons}')
    print(f'status markers on pages     : {n_markers}')
    for code, msg in errors:
        print(f'  [FAIL ] {code}: {msg}')
    if errors:
        print(f'RESULT: FAIL ({len(errors)} error(s))')
        return 1
    print('RESULT: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
