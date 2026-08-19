"""Mutation suite for the strong CE-tip review gate.

Each mutation corrupts one artefact the way a real defect would, runs
validate_ce_tip_review.py as a subprocess, and requires it to FAIL
SEMANTICALLY: non-zero exit, at least one named FAIL line, no traceback.
Every artefact is restored byte-for-byte afterwards.

Mutations (brief s36):
  A1 publish a HOLD row by hand in the snapshot        -> gate
  A2 give a HOLD decision a candidate tier             -> gate
  B1 promote a CE-tip-only approval to Confirmed       -> gate
  B2 promote the PARTIAL-mapped primary pair to Confirmed (MASTER-AQ-0080) -> gate
  B3 keep APPROVE_CE_TIP but write candidate_tier 'confirmed' -> gate
  C  blank evidence_ids on an approved row             -> gate
  D1 wrong target anchor on an approved row            -> gate
  D2 re-point an approved row at the neighbouring question -> gate
  E  duplicate a decision record                       -> gate
  F1 add an eleventh, unreviewed relationship          -> gate
  F2 add an eleventh row to the snapshot via the review route -> gate
  G1 swap the pinned wording for topic-only card prose  -> gate
  G2 edit the live card so the tip no longer names the examiner -> gate
  H  reintroduce the historically review-held RELA-SIMON-QB9_H-q11 -> gate
  I  evidence id that names a different examiner       -> gate
  J  evidence id whose governed target is another question -> gate
  K  hand-raise a review row's tier in the snapshot    -> gate

    PYTHONIOENCODING=utf-8 python tools/oral/mutate_ce_tip_review.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402
import build_examiner_index as G  # noqa: E402

TOOLS = Path(__file__).resolve().parent
OUT = L.OUT
DEC = OUT / G.REVIEW_NAME
SNAP = OUT / G.SNAPSHOT_NAME
INDEX = L.MEO / "examiner-index.html"
SQ = L.REPO / "SQ" / "examiner-index.html"
SQ_HOME = L.REPO / "SQ" / "index.html"
CARD_QB9F = L.MEO / "QB9_F.html"

ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONHASHSEED="0")
GATE = "validate_ce_tip_review.py"


def run(script):
    r = subprocess.run([sys.executable, str(TOOLS / script)], capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=ENV,
                       cwd=str(L.REPO))
    fails = [ln for ln in r.stdout.splitlines() if ln.startswith("FAIL")]
    crashed = "Traceback" in r.stderr or "Traceback" in r.stdout
    return r.returncode, fails, crashed


class Guard:
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


def rj(p):
    return json.loads(p.read_bytes().decode("utf-8"))


def wj(p, obj):
    p.write_bytes((json.dumps(obj, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))


def dec_rows():
    d = rj(DEC)
    return d, d["decisions"]


def approved(rows, rid=None):
    for r in rows:
        if r["decision"].startswith("APPROVE_") and (rid is None or r["relation_id"] == rid):
            return r
    raise KeyError(rid)


def held(rows):
    return next(r for r in rows if r["decision"].startswith("HOLD_"))


# ------------------------------------------------------------- mutations

def m_A1():
    d, rows = dec_rows()
    h = held(rows)
    snap = rj(SNAP)
    twin = next(r for r in snap["rows"] if "CE_TIP_REVIEW" in r["sources"])
    row = dict(twin, examiner=h["examiner"], canonical_question_id=h["canonical_question_id"],
               refs=[h["relation_id"]], sources=["CE_TIP_REVIEW"])
    snap["rows"].append(row)
    wj(SNAP, snap)


def m_A2():
    d, rows = dec_rows()
    held(rows)["candidate_tier"] = "ce_tip"
    wj(DEC, d)


def m_B1():
    d, rows = dec_rows()
    r = approved(rows, "RELA-SIMON-QB1_F-q3")          # prose-only evidence
    r["decision"] = "APPROVE_CONFIRMED_RELATIONSHIP"
    r["candidate_tier"] = "confirmed"
    d["decisions_by_outcome"] = None
    wj(DEC, d)


def m_B2():
    d, rows = dec_rows()
    r = approved(rows, "RELA-SIMON-QB9_F-q8")          # MASTER-AQ-0080 is PARTIAL_MATCH
    r["decision"] = "APPROVE_CONFIRMED_RELATIONSHIP"
    r["candidate_tier"] = "confirmed"
    wj(DEC, d)


def m_B3():
    d, rows = dec_rows()
    approved(rows)["candidate_tier"] = "confirmed"
    wj(DEC, d)


def m_C():
    d, rows = dec_rows()
    approved(rows)["evidence_ids"] = []
    wj(DEC, d)


def m_D1():
    d, rows = dec_rows()
    r = approved(rows, "RELA-SIMON-QB9_F-q8")
    r["reviewed_target"]["anchor"] = "q9"
    wj(DEC, d)


def m_D2():
    d, rows = dec_rows()
    r = approved(rows, "RELA-SIMON-QB9_F-q8")
    r["canonical_question_id"] = "QB9_F#q9"
    r["relation_id"] = "RELA-SIMON-QB9_F-q9"
    r["reviewed_target"]["anchor"] = "q9"
    wj(DEC, d)


def m_E():
    d, rows = dec_rows()
    rows.append(dict(approved(rows)))
    d["reviewed"] = len(rows)
    wj(DEC, d)


def m_F1():
    d, rows = dec_rows()
    r = dict(approved(rows, "RELA-SIMON-QB6_F-q4"))
    # a real STRONG_CE_TIP prose row (QB6_F#q5, Simon) that was never in the held set
    r.update(relation_id="RELA-SIMON-QB6_F-q5", canonical_question_id="QB6_F#q5",
             reviewed_target={"file": "QB6_F.html", "anchor": "q5", "url": "/meoclass1/QB6_F.html#q5"},
             reviewed_question_text="What is a ship's Call Sign and how does it differ from the IMO number?",
             reviewed_ce_tip_wording="Simon", evidence_ids=["PROSE:Simon:QB6_F#q5"],
             corroboration_ids=[])
    rows.append(r)
    d["reviewed"] = len(rows)
    wj(DEC, d)


def m_F2():
    snap = rj(SNAP)
    twin = next(r for r in snap["rows"] if "CE_TIP_REVIEW" in r["sources"])
    row = dict(twin, canonical_question_id="QB6_F#q5", anchor="q5", q_number=5,
               url="/meoclass1/QB6_F.html#q5", refs=["RELA-SIMON-QB6_F-q5"],
               display_text="What is a ship's Call Sign and how does it differ from the IMO number?")
    snap["rows"].append(row)
    wj(SNAP, snap)


def m_G1():
    d, rows = dec_rows()
    # 'Kochi MMD Focus' is on the QB9_F card but names no examiner by itself
    approved(rows, "RELA-SIMON-QB9_F-q8")["reviewed_ce_tip_wording"] = "Kochi MMD Focus"
    wj(DEC, d)


def m_G2():
    h = CARD_QB9F.read_bytes().decode("utf-8")
    needle = "Examiner Simon wants a direct answer on India"
    assert needle in h, "fixture drift: QB9_F#q8 tip wording not found"
    CARD_QB9F.write_bytes(h.replace(needle, "The examiner wants a direct answer on India", 1).encode("utf-8"))


def m_H():
    d, rows = dec_rows()
    r = dict(approved(rows, "RELA-SIMON-QB9_F-q8"))
    r.update(relation_id="RELA-SIMON-QB9_H-q11", canonical_question_id="QB9_H#q11",
             reviewed_target={"file": "QB9_H.html", "anchor": "q11", "url": "/meoclass1/QB9_H.html#q11"},
             evidence_ids=["PROSE:Simon:QB9_H#q11"], corroboration_ids=[])
    rows.append(r)
    d["reviewed"] = len(rows)
    wj(DEC, d)


def m_I():
    d, rows = dec_rows()
    # MASTER-AQ-0012 is Nair's container-tracking record
    approved(rows, "RELA-SIMON-QB1_F-q3")["evidence_ids"] = sorted(
        ["MASTER-AQ-0012", "PROSE:Simon:QB1_F#q3"])
    wj(DEC, d)


def m_J():
    d, rows = dec_rows()
    # MASTER-AQ-0228 is Simon's, but its governed target is QB2_B#q11
    approved(rows, "RELA-SIMON-QB1_F-q3")["evidence_ids"] = sorted(
        ["MASTER-AQ-0228", "PROSE:Simon:QB1_F#q3"])
    wj(DEC, d)


def m_K():
    snap = rj(SNAP)
    r = next(r for r in snap["rows"] if "CE_TIP_REVIEW" in r["sources"])
    r["tier"] = "confirmed"
    r["tier_rank"] = 5
    wj(SNAP, snap)


MUTATIONS = [
    ("A1", "publish a HOLD row by hand in the snapshot", m_A1),
    ("A2", "give a HOLD decision a candidate tier", m_A2),
    ("B1", "promote a prose-only approval to Confirmed", m_B1),
    ("B2", "promote the PARTIAL-mapped primary pair to Confirmed", m_B2),
    ("B3", "APPROVE_CE_TIP with candidate_tier 'confirmed'", m_B3),
    ("C", "blank evidence_ids on an approved row", m_C),
    ("D1", "wrong target anchor on an approved row", m_D1),
    ("D2", "re-point an approved row at the neighbouring question", m_D2),
    ("E", "duplicate a decision record", m_E),
    ("F1", "add an eleventh, unreviewed relationship", m_F1),
    ("F2", "add an eleventh snapshot row via the review route", m_F2),
    ("G1", "swap pinned wording for topic-only card prose", m_G1),
    ("G2", "edit the live card so the tip no longer names Simon", m_G2),
    ("H", "reintroduce review-held RELA-SIMON-QB9_H-q11", m_H),
    ("I", "evidence id names a different examiner", m_I),
    ("J", "evidence id's governed target is another question", m_J),
    ("K", "hand-raise a review row's tier in the snapshot", m_K),
]


def main():
    rc, fails, crashed = run(GATE)
    if rc != 0 or fails or crashed:
        print("BASELINE NOT GREEN: exit=%d fails=%d crashed=%s" % (rc, len(fails), crashed))
        return 2
    print("baseline green")
    escapes = 0
    for code, label, mut in MUTATIONS:
        with Guard(DEC, SNAP, INDEX, SQ, SQ_HOME, CARD_QB9F):
            mut()
            rc, fails, crashed = run(GATE)
            ok = rc != 0 and fails and not crashed
            print("%-3s %-52s exit=%d fails=%d crash=%s  %s" % (
                code, label, rc, len(fails), crashed, "CAUGHT" if ok else "ESCAPE"))
            for f in fails[:2]:
                print("      " + f[:140])
            if not ok:
                escapes += 1
    rc, fails, crashed = run(GATE)
    st = subprocess.run(["git", "status", "--short", "--", str(CARD_QB9F)],
                        cwd=str(L.REPO), capture_output=True, text=True).stdout.strip()
    print("\nrestored: gate exit=%d fails=%d; QB9_F.html dirty: %s" % (rc, len(fails), bool(st)))
    print("%d mutations, %d escapes" % (len(MUTATIONS), escapes))
    return 1 if (escapes or rc != 0 or st) else 0


if __name__ == "__main__":
    sys.exit(main())
