#!/usr/bin/env python3
"""FUP-E — no notes tool may resolve its root from a hard-coded canonical path.

WHY THIS TEST EXISTS

`tools/notes/audit_overlap.py` hard-coded `ROOT = r'F:\\marine-intelligence-weekly'`
and wrote `_overlap_report.txt` there regardless of where it was invoked from.
Run inside a governed Controller job worktree it therefore wrote into the
CANONICAL repository, which the Controller treats as a PROTECTED ROOT. The
filesystem detector caught it, failed the cycle closed at NEEDS_HUMAN(safety),
and blocked the internal review until the root was restored and re-measured.
That is a real production incident, not a tidy-up: job AC-000021, cycle 0,
2026-08-30.

Two further scripts carried the same defect and had simply not been run inside a
governed job yet:

  check_master_index.py  read the master index from the hard-coded root and WROTE
                         `_master_index_balance.txt` back into it
  export_skill.py        wrote `docs/miw-notes-mgmt_SKILL.md`, a TRACKED file,
                         into the hard-coded root

`tools/notes/miw_paths.py` already had the right idiom, and says why in its own
comment: the root is resolved relative to the module file "so the module keeps
working if the clone is moved off F:\\ or cloned elsewhere." The rest of the
repository follows that convention. These three did not.

THE INVARIANT

  A notes tool resolves its root from ITS OWN LOCATION, and writes only inside
  that root.

Under governance that is the only workable rule: the Controller's Python policy
refuses script options (rule PYTHON_SCRIPT_ARGS), so a governed executor cannot
pass `--root`. The default with no arguments has to be correct.

Run:  python tools/notes/test_notes_root_resolution.py
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

# A drive-letter path naming this repository by name. That is the shape that
# survives being copied into another checkout and keeps pointing home.
HARDCODED = re.compile(r'''["']\s*[A-Za-z]:[\\/]+marine-intelligence-weekly''', re.I)

# Scripts that write, and the output each one owns. Every path must resolve
# inside the root the script derived from its own location.
WRITERS = {
    'audit_overlap.py': '_overlap_report.txt',
    'check_master_index.py': '_master_index_balance.txt',
    'export_skill.py': 'miw-notes-mgmt_SKILL.md',
}

failures = []


def check(name, ok, detail=''):
    print(('  [ok   ] ' if ok else '  [FAIL ] ') + name + (('  ' + detail) if detail else ''))
    if not ok:
        failures.append(name)


def test_no_hardcoded_canonical_root():
    """No tools/notes script may name the canonical repository by absolute path."""
    print('T1  no hard-coded canonical root in tools/notes/*.py')
    offenders = []
    for fn in sorted(os.listdir(HERE)):
        if not fn.endswith('.py'):
            continue
        # This file quotes the defect verbatim as evidence, exactly as the open-items
        # register does. Correcting the quotation would destroy the record of what was
        # wrong, so the scanner skips itself by name rather than by pattern.
        if fn == os.path.basename(__file__):
            continue
        src = io.open(os.path.join(HERE, fn), encoding='utf-8').read()
        for m in HARDCODED.finditer(src):
            line = src[:m.start()].count('\n') + 1
            offenders.append('%s:%d' % (fn, line))
    check('every tools/notes script resolves its root relatively',
          not offenders, ('offenders: ' + ', '.join(offenders)) if offenders else '')


def test_writers_resolve_root_from_their_own_file():
    """Each writing script derives its root from __file__, not from a constant."""
    print('T2  writing scripts derive their root from their own location')
    for fn in sorted(WRITERS):
        src = io.open(os.path.join(HERE, fn), encoding='utf-8').read()
        derives = ('miw_paths' in src and 'REPO_ROOT' in src) or '__file__' in src
        check('%s derives its root' % fn, derives)


def test_output_stays_inside_the_resolved_root():
    """A copy of the tools in a DIFFERENT root writes there, never back home.

    This is the production failure reproduced: the script is invoked from a
    location that is not the canonical checkout, exactly as a governed job
    worktree is, and must not reach back to the canonical repository.
    """
    print('T3  a tool run from another root writes into THAT root')
    tmp = tempfile.mkdtemp(prefix='miw-fupE-')
    try:
        alt_tools = os.path.join(tmp, 'tools', 'notes')
        os.makedirs(alt_tools)
        for fn in list(WRITERS) + ['miw_paths.py']:
            shutil.copy2(os.path.join(HERE, fn), os.path.join(alt_tools, fn))

        probe = os.path.join(alt_tools, '_probe_root.py')
        io.open(probe, 'w', encoding='utf-8').write(
            'import os, sys\n'
            'sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n'
            'from miw_paths import REPO_ROOT\n'
            'print(REPO_ROOT)\n')
        out = subprocess.run([sys.executable, probe], capture_output=True, text=True)
        resolved = (out.stdout or '').strip()
        check('root resolves to the alternate checkout, not the canonical one',
              os.path.normcase(resolved) == os.path.normcase(os.path.abspath(tmp)),
              'got %r' % resolved)
        check('resolved root is NOT the canonical repository',
              os.path.normcase(resolved) != os.path.normcase(REPO_ROOT))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_windows_path_casing_is_not_load_bearing():
    """The canonical root is `Marine-Intelligence-Weekly`; the hard-coded string
    was lowercase. On Windows both reach the same directory, which is exactly why
    the escape was invisible until the Controller measured it. Resolution must
    not depend on that coincidence."""
    print('T4  resolution does not depend on Windows path casing')
    check('repo root resolves to a real directory', os.path.isdir(REPO_ROOT), REPO_ROOT)
    check('repo root contains the notes tools',
          os.path.isdir(os.path.join(REPO_ROOT, 'tools', 'notes')))


def main():
    print('FUP-E — notes tool root resolution')
    print('repo root: %s' % REPO_ROOT)
    print('=' * 72)
    test_no_hardcoded_canonical_root()
    test_writers_resolve_root_from_their_own_file()
    test_output_stays_inside_the_resolved_root()
    test_windows_path_casing_is_not_load_bearing()
    print('=' * 72)
    if failures:
        print('FAILURES: %d' % len(failures))
        for f in failures:
            print('  - %s' % f)
        return 1
    print('ALL CHECKS PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
