"""Mutation suite for the card/ledger examiner divergence gate.

Each mutation introduces one real defect class, runs
validate_card_examiner_divergence.py as a subprocess, and requires it to fail
semantically: non-zero exit, at least one named FAIL line, no traceback. Every
mutated file is restored byte-for-byte, so this can never re-baseline anything.

  A  an inline attribution with no relationship and no hold
  B  a card naming an examiner the published evidence contradicts
  C  a duplicated published row, inflating the pair's examiner count
  D  a card naming someone the alias register does not know
  E  a published relationship removed while its card still displays it

Mutations are preflighted in memory first. A mutation that matches nothing
writes nothing and exercises nothing -- it is an absent test that reports like
a passing one, so a no-op aborts the suite before any file is touched.

    PYTHONIOENCODING=utf-8 python tools/oral/mutate_card_examiner_divergence.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

TOOLS = Path(__file__).resolve().parent
GATE = TOOLS / "validate_card_examiner_divergence.py"
SNAPSHOT = L.OUT / "EXAMINER_INDEX_SNAPSHOT.json"

# A card with no published examiner of its own, so mutation A cannot
# accidentally land on a pair that is already legitimately published.
FREE_CARD = L.MEO / "QB10_B.html"
FREE_ANCHOR = 'id="q2"'

# A card whose attribution IS published, for the mutations that need one.
HELD_CARD = L.MEO / "QB7_H.html"
HELD_TAG = '<span class="q-tag examiner-tag">Examiner: Simon</span>'


def run_gate():
    p = subprocess.run([sys.executable, str(GATE)], capture_output=True, text=True,
                       cwd=str(TOOLS), env={**__import__("os").environ,
                                            "PYTHONIOENCODING": "utf-8"})
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def html_mutation(path, old, new):
    def apply(raw):
        text = raw.decode("utf-8")
        if old not in text:
            return None
        return text.replace(old, new, 1).encode("utf-8")
    return path, apply


def snapshot_duplicate(raw):
    d = json.loads(raw.decode("utf-8"))
    for r in d["rows"]:
        if r["canonical_question_id"] == "QB7_H#q1":
            d["rows"].append(dict(r))
            return json.dumps(d, indent=1, ensure_ascii=False).encode("utf-8")
    return None


def snapshot_remove(raw):
    d = json.loads(raw.decode("utf-8"))
    before = len(d["rows"])
    d["rows"] = [r for r in d["rows"] if r["canonical_question_id"] != "QB7_H#q1"]
    if len(d["rows"]) == before:
        return None
    return json.dumps(d, indent=1, ensure_ascii=False).encode("utf-8")


MUTATIONS = [
    ("A", "inline attribution with no relationship and no hold",
     "every in-card attribution is published or explicitly governed",
     html_mutation(FREE_CARD, FREE_ANCHOR,
                   FREE_ANCHOR + '><span class="q-tag examiner-tag">Examiner: Nair</span')),
    ("B", "card names an examiner the published evidence contradicts",
     "no card names an examiner the published evidence contradicts",
     html_mutation(HELD_CARD, HELD_TAG,
                   '<span class="q-tag examiner-tag">Examiner: Srivastava</span>')),
    ("C", "duplicate published row inflates the pair",
     "no published pair carries duplicate relationship rows",
     (SNAPSHOT, snapshot_duplicate)),
    ("D", "card names an examiner the alias register does not know",
     "every in-card examiner string resolves in the alias register",
     html_mutation(HELD_CARD, HELD_TAG,
                   '<span class="q-tag examiner-tag">Examiner: Fernandes</span>')),
    ("E", "relationship removed while its card still displays it",
     "every in-card attribution is published or explicitly governed",
     (SNAPSHOT, snapshot_remove)),
]


def main():
    rc, out = run_gate()
    if rc != 0:
        print("ABORT: the gate is not green before mutation\n" + out)
        return 2

    # ---- preflight: every mutation must change bytes ----------------------
    planned = []
    for mid, label, _expect, (path, apply) in MUTATIONS:
        original = path.read_bytes()
        mutated = apply(original)
        if mutated is None or mutated == original:
            print("ABORT: mutation %s (%s) is a no-op against %s" % (mid, label, path.name))
            return 2
        planned.append((mid, label, path, original, mutated))
    print("preflight: %d/%d mutations change bytes\n" % (len(planned), len(MUTATIONS)))

    escapes = crashes = 0
    for (mid, label, path, original, mutated), (_m, _l, expect, _t) in zip(planned, MUTATIONS):
        path.write_bytes(mutated)
        try:
            rc, out = run_gate()
        finally:
            path.write_bytes(original)
            assert path.read_bytes() == original, "restore failed for " + path.name

        caught = rc != 0 and expect in out and "Traceback" not in out
        if "Traceback" in out:
            crashes += 1
        if not caught:
            escapes += 1
        print("%s  %-58s %s" % (mid, label, "CAUGHT" if caught else "ESCAPED"))
        if not caught:
            print("    expected FAIL on: " + expect)
            print("    " + out.strip().replace("\n", "\n    ")[:900])

    rc, out = run_gate()
    residue = rc != 0
    print()
    print("%d mutations, %d escapes" % (len(MUTATIONS), escapes))
    print("crashes=%d residue=%s" % (crashes, residue))
    if residue:
        print("RESIDUE: the gate is not green after restore\n" + out)
    return 1 if (escapes or crashes or residue) else 0


if __name__ == "__main__":
    sys.exit(main())
