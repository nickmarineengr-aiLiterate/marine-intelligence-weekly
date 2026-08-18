"""Byte-reproducibility gate for the Oral reconciliation.

Re-running `reconcile_788.py` used to change five records: the recorded
spelling repairs were emitted in set-iteration order, so they varied between
runs under string hash randomisation. No disposition moved, but an artefact
whose bytes depend on the interpreter's hash seed cannot be diffed, reviewed or
trusted as a baseline.

This gate runs the generation twice under deliberately different hash seeds and
requires the emitted artefacts to be byte-identical. It restores whatever was
on disk before it ran, so it never becomes a way of silently re-baselining.

  PYTHONIOENCODING=utf-8 python tools/oral/check_determinism.py

Portability: repo-relative; no drive letters, no machine-local paths.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

OUT = L.OUT
TOOLS = Path(__file__).resolve().parent

GENERATED = [
    "ORAL_788_RECONCILIATION.jsonl",
    "ORAL_GAP_CANDIDATES.json",
    "HUMAN_REVIEW_QUEUE.json",
    "ORAL_788_RECONCILIATION_SUMMARY.json",
]

# Two seeds, deliberately different, so any residual dependence on set or dict
# iteration order shows up as a byte difference rather than hiding behind a
# lucky repeat run.
SEEDS = ("0", "1", "524287")


def run(seed):
    env = dict(os.environ, PYTHONHASHSEED=seed, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, str(TOOLS / "reconcile_788.py")],
                       capture_output=True, text=True, cwd=str(L.REPO), env=env)
    if p.returncode != 0:
        raise SystemExit("reconcile_788.py failed under PYTHONHASHSEED=%s:\n%s"
                         % (seed, p.stderr))
    return {n: (OUT / n).read_bytes() for n in GENERATED}


def main():
    before = {n: (OUT / n).read_bytes() for n in GENERATED if (OUT / n).exists()}
    try:
        runs = [run(s) for s in SEEDS]
    finally:
        for n, b in before.items():
            (OUT / n).write_bytes(b)

    bad = []
    for name in GENERATED:
        sizes = {r[name] for r in runs}
        status = "IDENTICAL" if len(sizes) == 1 else "DIFFERS"
        if len(sizes) != 1:
            bad.append(name)
        print("%-10s %-42s %d bytes" % (status, name, len(runs[0][name])))

    print("\n%d artefacts / %d non-reproducible (seeds %s)"
          % (len(GENERATED), len(bad), ", ".join(SEEDS)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
