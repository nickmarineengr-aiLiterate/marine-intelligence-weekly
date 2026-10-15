#!/usr/bin/env python3
"""Apply the PRIVATE LOHAN layer onto a working tree, for local or private qualification only.

The production site mounts the same layer at build time (assemble.mjs). This tool lets the
Notes validators run against exactly what production serves. It never runs in public CI:
public CI has no private layer and reports PROTECTED_CONTENT_UNAVAILABLE instead.

It copies <private>/lohan/overlay/** and <private>/lohan/source/** into <tree>. It refuses to
overwrite a TRACKED public file unless that file is one of the declared metadata replacements.
A replacement must start from the exact public bytes the pin names, so a stale overlay can
never mask a public change.

usage: python tools/notes/protected/overlay.py --private <checkout of miw-protected-notes> --tree <worktree>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

PIN_REL = 'tools/notes/protected/lohan.pin.json'
REPLACEABLE = {'meoclass1/oralnotes/index.html', 'meoclass1/oralnotes/notes_content_index.json',
               'tools/notes/canonical/source_nodes.csv'}


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--private', required=True)
    ap.add_argument('--tree', required=True)
    a = ap.parse_args(argv)
    tracked = set(subprocess.run(['git', '-c', 'safe.directory=*', 'ls-files', '-z'], cwd=a.tree,
                                 capture_output=True, check=True).stdout.decode('utf-8').split('\0')) - {''}
    pin_path = os.path.join(a.tree, *PIN_REL.split('/'))
    expected_public = {}
    if os.path.isfile(pin_path):
        with open(pin_path, encoding='utf-8') as fh:
            pin = json.load(fh)
        expected_public = {r['path']: r['public_sha256'] for r in pin.get('replace_files', [])}
    copied, replaced = 0, 0
    for layer in ('overlay', 'source'):
        root = os.path.join(a.private, 'lohan', layer)
        for dp, _, fns in os.walk(root):
            for fn in sorted(fns):
                src = os.path.join(dp, fn)
                rel = os.path.relpath(src, root).replace(os.sep, '/')
                dst = os.path.join(a.tree, *rel.split('/'))
                if rel in tracked:
                    if rel not in REPLACEABLE:
                        sys.exit('REFUSED: %s is a tracked public file and not a declared replacement' % rel)
                    want = expected_public.get(rel)
                    if want and sha(dst) != want:
                        sys.exit('REFUSED: public %s differs from the pinned public_sha256' % rel)
                    replaced += 1
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(src, dst)
                copied += 1
    print(json.dumps({'copied': copied, 'replaced_public_files': replaced}))


if __name__ == '__main__':
    main()
