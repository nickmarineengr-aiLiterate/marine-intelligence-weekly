"""
miw_paths.py — single source of truth for MIW repository paths.

Created 2026-08-06 after a duplicate-truth failure: two divergent copies of the oral
notes manifest coexisted for 11 days (`notes-content-index.json` vs
`notes_content_index.json`), differing only by a hyphen. Nothing loads these manifests
at request time, so the stale copy broke no page and raised no error — it was invisible
until someone compared MD5s by hand.

Rule: no tool in this repo should ever spell a manifest filename as a bare inline
string. Import it from here. If a name has to change, it changes in exactly one place.

Usage:
    import sys, os
    sys.path.insert(0, os.path.join(REPO_ROOT, 'tools', 'notes'))
    from miw_paths import NOTES_MANIFEST, WRITTEN_MANIFEST, QB_MANIFEST, assert_no_legacy_manifest

See tools/notes/SKILL.md section 8a.
"""

import os

# Repo root resolved relative to THIS file (tools/notes/miw_paths.py -> repo root),
# so the module keeps working if the clone is moved off F:\ or cloned elsewhere.
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

MEOCLASS1 = os.path.join(REPO_ROOT, 'meoclass1')
ORALNOTES = os.path.join(MEOCLASS1, 'oralnotes')
PASTPAPERS = os.path.join(MEOCLASS1, 'pastpapers')

# --- Manifests: four, each authoritative for its own series. Never merge. ---

# ORAL / page-range series: Simon Sir Notes, Current Topics, MIW Engineering
# Management Notes (Uday Notes). UNDERSCORES.
NOTES_MANIFEST = os.path.join(ORALNOTES, 'notes_content_index.json')

# WRITTEN answer series: WA1-HKC, WA2-GHG, WA3-LIEN. Separate by design.
WRITTEN_MANIFEST = os.path.join(ORALNOTES, 'written_content_index.json')

# QB series.
QB_MANIFEST = os.path.join(MEOCLASS1, 'qb_content_index.json')

# PAST PAPERS series: one full official written sitting per file (QP2607 etc.).
# Fourth series, added 2026-08-07. Deliberately NOT folded into WRITTEN_MANIFEST:
# that file is reserved for the WA topic-chapter series, which is a different
# content shape (one topic, unlimited depth) from this one (one exam sitting,
# marks-calibrated and time-boxed).
PASTPAPERS_MANIFEST = os.path.join(PASTPAPERS, 'pastpapers_content_index.json')

# Repo-relative forms, for tools that address GitHub rather than the local disk
# (e.g. meoclass1/qb_health_check.py, which scans the remote tree).
NOTES_MANIFEST_REL = 'meoclass1/oralnotes/notes_content_index.json'
WRITTEN_MANIFEST_REL = 'meoclass1/oralnotes/written_content_index.json'
QB_MANIFEST_REL = 'meoclass1/qb_content_index.json'
PASTPAPERS_MANIFEST_REL = 'meoclass1/pastpapers/pastpapers_content_index.json'

# Names that must never exist again. Deleted 2026-08-06 (commit 89291e5;
# content recoverable at 64ab22d).
LEGACY_MANIFEST_NAMES = (
    os.path.join(ORALNOTES, 'notes-content-index.json'),
)


def _is_git_tracked(path):
    """True if git tracks this path. None if git can't answer."""
    import subprocess
    try:
        r = subprocess.run(
            ['git', '-C', REPO_ROOT, 'ls-files', '--error-unmatch', path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15,
        )
        return r.returncode == 0
    except Exception:
        return None


def _exists(path):
    """os.path.exists that survives a locked/permission-denied entry."""
    try:
        return os.path.exists(path)
    except OSError:
        return True   # can't stat it, but something is there


def assert_no_legacy_manifest(raise_on_find=True):
    """Guard against a retired manifest filename returning.

    The failure this prevents is a *second source of truth inside the repository*, so
    severity is keyed to git tracking, not mere presence on disk:

      - tracked by git  -> raise. This is a real duplicate; it would be pushed and
                           would mislead every future session.
      - untracked       -> warn loudly and continue. Local cruft (e.g. a file left
                           behind because the OS had it locked) cannot reach the repo,
                           and must not block legitimate work.

    Returns the list of offending paths found (empty when clean).
    """
    found = [p for p in LEGACY_MANIFEST_NAMES if _exists(p)]
    if not found:
        return []

    tracked = [p for p in found if _is_git_tracked(p) is True]

    if tracked and raise_on_find:
        raise RuntimeError(
            'Retired manifest filename(s) are TRACKED BY GIT again: '
            + ', '.join(tracked)
            + '. The canonical oral-notes manifest is ' + NOTES_MANIFEST
            + '. Remove the duplicate (git rm) — do not edit or read it. '
              'See tools/notes/SKILL.md section 8a.'
        )

    import sys as _sys
    for p in found:
        print(
            'WARNING: retired manifest filename present on disk (untracked, will not '
            'reach the repo): %s — delete it. Canonical file is %s. See '
            'tools/notes/SKILL.md section 8a.' % (p, NOTES_MANIFEST),
            file=_sys.stderr,
        )
    return found



def load_json(path):
    """Read a UTF-8 JSON file, with the offending path named on failure."""
    import json
    try:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh)
    except Exception as exc:
        raise RuntimeError('Failed to load %s: %s' % (path, exc)) from exc
