"""Mutation suite for the Examiner Index V2 release gate.

Each mutation corrupts one artefact the way a real defect would, runs the
relevant validator as a subprocess, and requires it to FAIL SEMANTICALLY:
non-zero exit, at least one named FAIL line, no traceback. Every artefact is
restored byte-for-byte afterwards, so this can never re-baseline anything.

Mutations (brief s42):
  A  re-add a review-rejected Release-A pair          -> validate_phase2 + index gate
  B  blank evidence_ids on an approved relation       -> validate_phase2 + index gate
  C  corrupt one generated anchor                     -> index gate
  D  hand-alter one section heading count             -> index gate
  E  invalid tier literal on a row                    -> index gate
  F  duplicate a rendered relationship                -> index gate
  G  SQ teaser count differs from the snapshot        -> index gate
  H  raw .docx tracked by git                         -> index gate
  I  tamper the snapshot's own totals                 -> index gate
  J  relabel a CE-tip row as Confirmed in the HTML    -> index gate

    PYTHONIOENCODING=utf-8 python tools/oral/mutate_examiner_index.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

TOOLS = Path(__file__).resolve().parent
OUT = L.OUT
INDEX = L.MEO / "examiner-index.html"
SQ = L.REPO / "SQ" / "examiner-index.html"
SNAP = OUT / "EXAMINER_INDEX_SNAPSHOT.json"
PUB = OUT / "RELEASE_A_PUBLICATION.json"
P2RES = OUT / "PHASE2_VALIDATION_RESULTS.json"   # validate_phase2.py writes this
RA = OUT / "RELEASE_A_CONNECTIONS.json"
DUMMY = L.REPO / "docs" / "MIW-master-Question-bank" / "MUTATION_H_dummy.docx"

ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONHASHSEED="0")


def run(script):
    r = subprocess.run([sys.executable, str(TOOLS / script)], capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=ENV,
                       cwd=str(L.REPO))
    fails = [ln for ln in r.stdout.splitlines() if ln.startswith("FAIL")]
    crashed = "Traceback" in r.stderr or "Traceback" in r.stdout
    return r.returncode, fails, crashed


class Guard:
    """Snapshot bytes of every artefact a mutation may touch; restore on exit."""
    def __init__(self, *paths):
        self.paths = paths
        self.saved = {p: (p.read_bytes() if p.exists() else None) for p in paths}

    def __enter__(self):
        return self

    def __exit__(self, *a):
        for p, b in self.saved.items():
            if b is None:
                if p.exists():
                    p.unlink()
            else:
                p.write_bytes(b)


def wtext(p, s):
    p.write_bytes(s.encode("utf-8"))


def rtext(p):
    return p.read_bytes().decode("utf-8")


# ------------------------------------------------------------- mutations

def m_A():
    ra = json.loads(rtext(RA))
    c = next(x for x in ra["connections"] if x["relation_id"] == "RELA-NAIR-QB1_K-q5")
    pub = json.loads(rtext(PUB))
    c = dict(c, disposition="NEW_RELATIONSHIP", existing_relationship_id=None,
             research_tier=c["strongest_evidence_tier"], retiered=False,
             evidence_ids=["JULY-NEW-109"], primary_evidence_ids=["JULY-NEW-109"],
             external_evidence_ids=[], note_evidence_ids=[], derived_corroboration_ids=[],
             weak_corroboration_ids=[])
    pub["connections"].append(c)
    pub["published_pairs"] += 1
    pub["new_relationships"] += 1
    pub["composition_published"][c["strongest_evidence_tier"]] += 1
    wtext(PUB, json.dumps(pub, ensure_ascii=False, indent=1) + "\n")


def m_B():
    pub = json.loads(rtext(PUB))
    pub["connections"][0]["evidence_ids"] = []
    wtext(PUB, json.dumps(pub, ensure_ascii=False, indent=1) + "\n")


def m_C():
    h = rtext(INDEX)
    h2 = h.replace('href="/meoclass1/QB1_A.html#q1"', 'href="/meoclass1/QB1_A.html#q9999"', 1)
    assert h2 != h
    wtext(INDEX, h2)


def m_D():
    h = rtext(INDEX)
    m = re.search(r'<h2>Simon <span class="ex-count">(\d+) questions</span>', h)
    n = int(m.group(1))
    wtext(INDEX, h.replace(m.group(0), m.group(0).replace(str(n), str(n + 1)), 1))


def m_E():
    h = rtext(INDEX)
    h2 = h.replace('class="q-row tier-ce_tip" data-tier="ce_tip"',
                   'class="q-row tier-cetip" data-tier="cetip"', 1)
    assert h2 != h
    wtext(INDEX, h2)


def m_F():
    h = rtext(INDEX)
    m = re.search(r'<div class="q-row tier-confirmed" data-tier="confirmed">.*?</div>\s*</div>', h, re.S)
    row = m.group(0)
    wtext(INDEX, h.replace(row, row + row, 1))


def m_G():
    s = rtext(SQ)
    m = re.search(r'<div class="stat-num">(\d+)</div><div class="stat-label">Questions Tagged', s)
    n = int(m.group(1))
    wtext(SQ, s.replace(m.group(0), m.group(0).replace(str(n), str(n + 100)), 1))


def m_H():
    DUMMY.write_bytes(b"not really a docx")
    subprocess.run(["git", "add", "-f", str(DUMMY.relative_to(L.REPO)).replace("\\", "/")],
                   cwd=str(L.REPO), check=True, capture_output=True)


def undo_H():
    subprocess.run(["git", "rm", "--cached", "-q", "--",
                    str(DUMMY.relative_to(L.REPO)).replace("\\", "/")],
                   cwd=str(L.REPO), capture_output=True)
    if DUMMY.exists():
        DUMMY.unlink()


def m_I():
    snap = json.loads(rtext(SNAP))
    snap["totals"]["relationships"] += 1
    wtext(SNAP, json.dumps(snap, ensure_ascii=False, indent=1) + "\n")


def m_J():
    h = rtext(INDEX)
    h2 = h.replace('class="q-row tier-ce_tip" data-tier="ce_tip"',
                   'class="q-row tier-confirmed" data-tier="confirmed"', 1)
    assert h2 != h
    wtext(INDEX, h2)


MUTATIONS = [
    ("A", "re-add review-rejected RELA-NAIR-QB1_K-q5", m_A, ("validate_phase2.py", "validate_examiner_index.py")),
    ("B", "blank evidence_ids on an approved relation", m_B, ("validate_phase2.py", "validate_examiner_index.py")),
    ("C", "corrupt one generated anchor", m_C, ("validate_examiner_index.py",)),
    ("D", "hand-alter Simon's section heading count", m_D, ("validate_examiner_index.py",)),
    ("E", "invalid tier literal 'cetip' on a row", m_E, ("validate_examiner_index.py",)),
    ("F", "duplicate a rendered relationship", m_F, ("validate_examiner_index.py",)),
    ("G", "SQ 'Questions Tagged' differs from snapshot", m_G, ("validate_examiner_index.py",)),
    ("H", "raw .docx tracked by git", m_H, ("validate_examiner_index.py",)),
    ("I", "tamper snapshot totals", m_I, ("validate_examiner_index.py",)),
    ("J", "relabel a CE-tip row Confirmed in the HTML", m_J, ("validate_examiner_index.py",)),
]


def main():
    # baseline must be green or the suite proves nothing
    for s in ("validate_phase2.py", "validate_examiner_index.py"):
        rc, fails, crashed = run(s)
        if rc != 0 or fails or crashed:
            print("BASELINE NOT GREEN: %s exit=%d fails=%d crashed=%s" % (s, rc, len(fails), crashed))
            return 2
    print("baseline green")
    escapes = 0
    for code, label, mut, validators in MUTATIONS:
        with Guard(PUB, INDEX, SQ, SNAP, P2RES):
            try:
                mut()
                for v in validators:
                    rc, fails, crashed = run(v)
                    ok = rc != 0 and fails and not crashed
                    print("%s  %-46s %-27s exit=%d fails=%d crash=%s  %s" % (
                        code, label, v, rc, len(fails), crashed, "CAUGHT" if ok else "ESCAPE"))
                    for f in fails[:2]:
                        print("      " + f[:130])
                    if not ok:
                        escapes += 1
            finally:
                if code == "H":
                    undo_H()
    # prove restoration
    rc, fails, crashed = run("validate_examiner_index.py")
    st = subprocess.run(["git", "status", "--short", "--untracked-files=all"],
                        cwd=str(L.REPO), capture_output=True, text=True).stdout
    dirty = [ln for ln in st.splitlines() if "MUTATION_H_dummy" in ln]
    print("\nrestored: index gate exit=%d fails=%d; dummy docx traces: %d" % (rc, len(fails), len(dirty)))
    print("%d mutations, %d escapes" % (len(MUTATIONS), escapes))
    return 1 if (escapes or rc != 0 or dirty) else 0


if __name__ == "__main__":
    sys.exit(main())
