#!/usr/bin/env python3
"""notes_release_gate.py — the proposed BLOCKING release gate for the Notes (D-L4 governance, 11 Oct 2026).

One command, one exit code. Every step is a subprocess with its own exit code; a step that cannot
run is a failure, never a pass. Nothing here writes to the tree.

  1  validate_canonical            registry + LOHAN publication state (release-candidate in main/release)
  2  test_validate_canonical       its mutation/control cases (L7 + S-series included)
  3  validate_status_consumers
  4  test_validate_status_consumers
  5  check_notes_release           manifest totals / duplicates / compiler identity, exact gate,
                                   ORAL_QB_NOTES entitlement, LOHAN attribution + disclaimer
  6  test_check_notes_release      its negative and mutation controls
  7  test_notes_controls           the Notes controls, F4 attribution rule included
  8  rights record                 release mode only: the private Founder rights record (--rights-record)
                                   must exist and its latest entry must clear public-source publication

Modes:
  preview  local rehearsal: release-only blockers (disclaimer text) are listed, not failed
  main     CI on the production branch: a preview state or an unapproved disclaimer fails
  release  the Founder's pre-push D-J run: as main, plus the private rights record

Usage: python tools/notes/notes_release_gate.py [--mode preview|main|release] [--rights-record FILE] [--json OUT]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

# Fields the latest rights-record entry must carry before LOHAN source can be published in a PUBLIC
# repository. Values 'UNKNOWN' / '' / None mean "not established" and hold publication.
RIGHTS_REQUIRED = ('permission_basis', 'evidence_reference', 'rights_holder', 'authorised_adaptations',
                   'distribution_channels', 'paid_access_scope', 'public_source_disclosure_covered')
# O-3 private-source delivery (Founder FD-P1, 15 Oct 2026): the content never enters public Git, so
# public-source disclosure is not required; gated paid distribution must be established instead.
RIGHTS_BASE = tuple(k for k in RIGHTS_REQUIRED if k != 'public_source_disclosure_covered')
DELIVERY_MODES = ('PUBLIC_GIT', 'PRIVATE_SOURCE')
PIN_REL = 'o3/lohan.pin.json'


def steps(mode: str, delivery: str = 'PUBLIC_GIT') -> list:
    rc = ['--release-candidate'] if mode in ('main', 'release') else []
    if delivery == 'PRIVATE_SOURCE' and mode == 'release':
        rc = rc + ['--require-protected']
    py = [sys.executable, '-X', 'utf8']
    return [
        ('validate_canonical', py + ['tools/notes/canonical/validate_canonical.py'] + rc),
        ('test_validate_canonical', py + ['tools/notes/canonical/test_validate_canonical.py']),
        ('validate_status_consumers', py + ['tools/notes/canonical/validate_status_consumers.py']),
        ('test_validate_status_consumers', py + ['tools/notes/canonical/test_validate_status_consumers.py']),
        ('check_notes_release', py + ['tools/notes/check_notes_release.py', '--mode', mode]),
        ('test_check_notes_release', py + ['tools/notes/test_check_notes_release.py']),
        ('test_notes_controls', py + ['tools/oral/test_notes_controls.py']),
    ]


def check_rights_record(path: str | None, delivery: str = 'PUBLIC_GIT') -> tuple:
    """(ok, message). The record is private and append-only (JSON Lines); the LAST entry governs."""
    if not path:
        return False, 'no --rights-record given; LOHAN source publication stays on HOLD'
    try:
        with open(path, encoding='utf-8', newline='') as fh:
            lines = [l.rstrip('\r\n') for l in fh if l.strip()]
        entries = [json.loads(l) for l in lines]
    except (OSError, ValueError) as e:
        return False, f'rights record unreadable: {e}'
    if not entries:
        return False, 'rights record has no entries'
    # append-only: each entry names the sha256 of the line before it (the first names GENESIS)
    prev = 'GENESIS'
    for i, (line, e) in enumerate(zip(lines, entries), start=1):
        if e.get('prev_entry_sha256') != prev:
            return False, f'rights record chain broken at entry {i} ({e.get("record_id")!r}); an earlier entry was edited or removed'
        prev = hashlib.sha256(line.encode('utf-8')).hexdigest()
    last = entries[-1]
    required = RIGHTS_REQUIRED if delivery == 'PUBLIC_GIT' else RIGHTS_BASE
    missing = [k for k in required if last.get(k) in (None, '', [], 'UNKNOWN')]
    if missing:
        return False, f'latest rights entry {last.get("record_id")!r} leaves {missing} unestablished; HOLD'
    if delivery == 'PUBLIC_GIT':
        if str(last.get('public_source_disclosure_covered')).upper() != 'YES':
            return False, f'latest rights entry {last.get("record_id")!r}: public source disclosure not covered; HOLD'
        return True, f'latest rights entry {last.get("record_id")!r} clears public-source publication'
    channels = last.get('distribution_channels')
    channels = channels if isinstance(channels, list) else [channels]
    if 'gated website' not in channels:
        return False, f'latest rights entry {last.get("record_id")!r}: distribution_channels lacks "gated website"; HOLD'
    if str(last.get('paid_access_scope', '')).strip().upper().startswith('NO'):
        return False, f'latest rights entry {last.get("record_id")!r}: paid access not covered; HOLD'
    if not os.path.isfile(os.path.join(ROOT, *PIN_REL.split('/'))):
        return False, f'PRIVATE_SOURCE delivery but no public pin at {PIN_REL}; HOLD'
    return True, f'latest rights entry {last.get("record_id")!r} clears PRIVATE_SOURCE (O-3) gated publication'


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--mode', choices=('preview', 'main', 'release'), default='preview')
    ap.add_argument('--rights-record', help='release mode: the private Founder rights record (JSON Lines)')
    ap.add_argument('--json', help='write the step results as JSON')
    ap.add_argument('--delivery-mode', choices=DELIVERY_MODES, default='PUBLIC_GIT',
                    help='PUBLIC_GIT (default, strictest) or PRIVATE_SOURCE (O-3 private content repo + pinned mount)')
    a = ap.parse_args(argv)
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    results, failed = [], 0
    for name, cmd in steps(a.mode, a.delivery_mode):
        t0 = time.time()
        try:
            r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', env=env, timeout=1800)
            rc, out = r.returncode, (r.stdout + r.stderr)
        except Exception as e:  # did not run => failure
            rc, out = 99, f'{type(e).__name__}: {e}'
        tail = [l for l in out.strip().splitlines() if l.strip()][-1:] or ['(no output)']
        ok = rc == 0
        failed += 0 if ok else 1
        results.append({'step': name, 'rc': rc, 'ok': ok, 'secs': round(time.time() - t0, 1), 'last_line': tail[0],
                        'blockers': [l.strip() for l in out.splitlines() if '[BLOCK]' in l],
                        'protected_unavailable': 'PROTECTED_CONTENT_UNAVAILABLE' in out})
        print(f"{'PASS' if ok else 'FAIL'}  {name:32} rc={rc}  {tail[0][:150]}")
    if a.mode == 'release':
        ok, msg = check_rights_record(a.rights_record, a.delivery_mode)
        failed += 0 if ok else 1
        results.append({'step': 'rights_record', 'rc': 0 if ok else 1, 'ok': ok, 'last_line': msg, 'blockers': []})
        print(f"{'PASS' if ok else 'FAIL'}  {'rights_record':32} {msg}")
    blockers = [b for r in results for b in r['blockers']]
    for b in blockers:
        print(f'  release blocker: {b}')
    verdict = 'FAIL' if failed else ('PASS_WITH_RELEASE_BLOCKERS' if blockers else 'PASS')
    if verdict != 'FAIL' and any(r.get('protected_unavailable') for r in results):
        # O-3 public checkout: never presented as a full pass.
        verdict = 'PASS_PUBLIC_LAYER_ONLY (PROTECTED_CONTENT_UNAVAILABLE)'
    print(f'NOTES RELEASE GATE [{a.mode}, {a.delivery_mode}]: {verdict} ({len(results) - failed}/{len(results)} steps green)')
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump({'mode': a.mode, 'verdict': verdict, 'steps': results}, fh, ensure_ascii=False, indent=1)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
