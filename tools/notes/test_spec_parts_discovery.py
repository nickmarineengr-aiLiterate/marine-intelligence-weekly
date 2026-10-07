#!/usr/bin/env python3
"""WP-23C (2026-10-07) — audit_overlap.py and match_qb.py must discover Parts
from tools/notes/specs/ rather than carry a hard-coded Part tuple.

Run:  python tools/notes/test_spec_parts_discovery.py
"""
import os, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from miw_paths import spec_parts, SPECS_DIR  # noqa: E402


def test_discovers_real_specs():
    parts = spec_parts()
    assert parts == sorted(parts), parts
    assert 19 in parts and 22 in parts, parts
    for p in parts:
        assert os.path.exists(os.path.join(SPECS_DIR, 'p%d.json' % p))


def test_ignores_non_spec_files():
    with tempfile.TemporaryDirectory() as d:
        for n in ('p23.json', 'p7.json', 'p23.json.bak', 'notes.txt', 'px.json'):
            open(os.path.join(d, n), 'w').close()
        assert spec_parts(d) == [7, 23], spec_parts(d)


def test_tools_no_longer_hard_code_tuple():
    for name in ('audit_overlap.py', 'match_qb.py'):
        src = open(os.path.join(HERE, name), encoding='utf-8').read()
        assert '(19, 20, 21, 22)' not in src, name
        assert 'spec_parts' in src, name


if __name__ == '__main__':
    for fn in (test_discovers_real_specs, test_ignores_non_spec_files,
               test_tools_no_longer_hard_code_tuple):
        fn(); print('PASS', fn.__name__)
