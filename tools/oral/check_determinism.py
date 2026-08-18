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

# One entry per generator, so a new artefact cannot be added without stating
# which script produces it. This is an ordered sequence rather than a mapping
# because the Phase 2A-iii package reads what the earlier generators write -
# the Notes coverage carries each occurrence's canonical disposition, and the
# final package reads both - so alphabetical order would run the consumers
# before the producers.
GENERATORS = (
    ("reconcile_788.py", [
        "ORAL_788_RECONCILIATION.jsonl",
        "ORAL_GAP_CANDIDATES.json",
        "HUMAN_REVIEW_QUEUE.json",
        "ORAL_788_RECONCILIATION_SUMMARY.json",
    ]),
    # Phase 2A-ii. The Notes layer walks a directory, groups by set membership
    # and sorts note units, examiner cues and coverage hits - every one of
    # which is a place where iteration order could reach the emitted bytes.
    ("ingest_oral_notes.py", [
        "ORAL_NOTES_INVENTORY.json",
        "ORAL_NOTES_UNITS.jsonl",
        "ORAL_NOTES_EXAMINER_EVIDENCE.jsonl",
        "ORAL_NOTES_CUE_AUDIT.json",
        "ORAL_NOTES_COVERAGE.jsonl",
        "ORAL_NOTES_COVERAGE_SUMMARY.json",
    ]),
    # Phase 2A-ii impact layer: reads the reconciliation, so it follows it.
    ("report_notes_impact.py", [
        "ORAL_NOTES_P0_IMPACT.json",
        "ORAL_NOTES_REVERSE_CONNECTIONS.json",
    ]),
    # Phase 2A-iii final package: Release A, P0, movement and review residue.
    # Every one of these is read by a production session or by the index
    # generator, so an artefact whose bytes move under a hash seed is an
    # artefact nobody can review or diff.
    ("build_final_package.py", [
        "FINAL_788_PRODUCTION_DISPOSITION.jsonl",
        "RECONCILIATION_MOVEMENT_REPORT.json",
        "RELEASE_A_CONNECTIONS.json",
        "RELEASE_A_EXCLUSIONS.json",
        "FINAL_ORAL_GAP_CANDIDATES.json",
        "FINAL_P0_PRODUCTION_BATCH.json",
        "FINAL_HUMAN_REVIEW_QUEUE.json",
        "FINAL_RETIERING_PROPOSAL.json",
        "DISPLAY_TEXT_CORRECTION_CANDIDATES.json",
    ]),
    ("report_final_recompute.py", [
        "PHASE2A_III_FINAL_RECOMPUTE_SUMMARY.json",
        "RELEASE_A_CONNECTIONS.md",
        "FINAL_P0_PRODUCTION_BATCH.md",
        "RECONCILIATION_MOVEMENT_REPORT.md",
        "DISPLAY_TEXT_CORRECTION_CANDIDATES.md",
    ]),
)

GENERATED = [n for _, names in GENERATORS for n in names]

# Two seeds, deliberately different, so any residual dependence on set or dict
# iteration order shows up as a byte difference rather than hiding behind a
# lucky repeat run.
SEEDS = ("0", "1", "524287")


def run(seed):
    env = dict(os.environ, PYTHONHASHSEED=seed, PYTHONIOENCODING="utf-8")
    _rewind()
    for script, _ in GENERATORS:
        p = subprocess.run([sys.executable, str(TOOLS / script)],
                           capture_output=True, text=True,
                           cwd=str(L.REPO), env=env)
        if p.returncode != 0:
            raise SystemExit("%s failed under PYTHONHASHSEED=%s:\n%s"
                             % (script, seed, p.stderr))
    return {n: (OUT / n).read_bytes() for n in GENERATED}


# The pre-run state is written to disk BEFORE anything is regenerated.
# Holding it only in memory meant that a run killed part-way - and this gate is
# slow enough to be killed by a timeout - left the regenerated artefacts in
# place with no way back, which is exactly the silent re-baselining the gate
# exists to prevent. A stale snapshot is restored on the next run.
SNAPSHOT = OUT / ".determinism-snapshot"


def _save(before):
    SNAPSHOT.mkdir(parents=True, exist_ok=True)
    for n, b in before.items():
        (SNAPSHOT / n).write_bytes(b)


def _rewind():
    """Put every snapshotted artefact back, WITHOUT consuming the snapshot.

    One generator reads an artefact another generator writes: the Notes
    coverage carries each occurrence's canonical disposition, which comes from
    ORAL_788_RECONCILIATION.jsonl. Running the seeds back to back therefore fed
    the second seed a reconciliation the first seed had just rewritten, and the
    coverage differed for that reason rather than for a seed-dependent one.
    Reproducibility means the same INPUTS under a different seed, so each seed
    starts from the same state.
    """
    if not SNAPSHOT.is_dir():
        return []
    names = []
    for p in sorted(SNAPSHOT.iterdir()):
        (OUT / p.name).write_bytes(p.read_bytes())
        names.append(p.name)
    return names


def _restore_from_disk():
    names = _rewind()
    if SNAPSHOT.is_dir():
        for p in sorted(SNAPSHOT.iterdir()):
            p.unlink()
        SNAPSHOT.rmdir()
    return names


def main():
    stale = _restore_from_disk()
    if stale:
        print("restored %d artefact(s) left behind by an interrupted run"
              % len(stale))

    before = {n: (OUT / n).read_bytes() for n in GENERATED if (OUT / n).exists()}
    _save(before)
    try:
        runs = [run(s) for s in SEEDS]
    finally:
        _restore_from_disk()

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
