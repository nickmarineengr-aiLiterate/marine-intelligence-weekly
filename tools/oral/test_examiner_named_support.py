"""Examiner window (P2, F6 / D-I) controls: F6-T1 to F6-T8.

`examiner_named_supporting_units` exists because a series with no examiner
cues pushed every examiner-named unit out of the content top 5 for 57 asks
once the LOHAN series was added, mostly on a pure unit-id tie-break. These
controls pin the additive fix and nothing more:

    F6-T1  byte-identical output under PYTHONHASHSEED 0, 1 and 524287
    F6-T2  a synthetic cue-free series never removes a P2 unit unless that
           unit's own tier fell
    F6-T3  notes_support and notes_units are identical with and without P2
    F6-T4  every P2 unit has tier >= TOPIC and the ledger names the examiner
           for the unit
    F6-T5  <= 5 units, in total order
    F6-T6  ASC-0130 keeps Simon P1-N9 and P4-N18 with LOHAN present
    F6-T7  0 of 788 canonical dispositions change
    F6-T8  mutation: replacing P2 with the "top-5 intersect examiner" rule
           must FAIL F6-T2 on ASC-0130

Without the LOHAN series in the corpus, F6-T6 runs against the synthetic
cue-free series as a proxy and says so; the real F6-T6 needs a corpus that
carries NOTE-LOHAN-* units. Everything is computed in memory: no artefact is
written, and the committed examiner ledger is checked unchanged at the end.

  PYTHONIOENCODING=utf-8 python tools/oral/test_examiner_named_support.py

Portability: repo-relative, no drive letters, no external inputs.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L               # noqa: E402
import oral_notes as N             # noqa: E402
import notes_coverage as C         # noqa: E402
import ingest_oral_notes as I      # noqa: E402

FAILURES = []
CHECKS = [0]


def ok(name, condition, detail=""):
    CHECKS[0] += 1
    if not condition:
        FAILURES.append("%s %s" % (name, ("- " + detail) if detail else ""))


# --------------------------------------------------------------------------
# fixtures, built once, the same way ingest_oral_notes.main builds them
# --------------------------------------------------------------------------
LEDGER = L.OUT / "ORAL_NOTES_EXAMINER_EVIDENCE.jsonl"
LEDGER_BYTES = LEDGER.read_bytes() if LEDGER.exists() else None

UNITS = N.build_units()
IDX = C.unit_index(UNITS)
IDF, DEFAULT = C.idf_over_units(IDX)
ALIAS = json.loads((L.OUT / "EXAMINER_ALIAS_REGISTER.json").read_text(
    encoding="utf-8"))
CUES, _ = N.harvest_cues(N.examiner_aliases(ALIAS))
EVIDENCE = I.build_evidence(CUES)
SRC = [json.loads(l) for l in
       (L.OUT / "ALL_SURVEYORS_SOURCE_RECORDS.jsonl").open(encoding="utf-8")]
RECON = {r["source_id"]: r for r in (
    json.loads(l) for l in
    (L.OUT / "ORAL_788_RECONCILIATION.jsonl").open(encoding="utf-8"))}
COVERAGE = I.build_coverage(SRC, RECON, IDX, IDF, DEFAULT, EVIDENCE)
BY_SID = {c["source_id"]: c for c in COVERAGE}

UNIT_EXAMINERS = defaultdict(set)
for _e in EVIDENCE:
    UNIT_EXAMINERS[_e["note_unit_id"]].add(_e["examiner"])

ASC_0130 = "ASC-0130"
SIMON_0130 = ("NOTE-SIMON-P1-N9-", "NOTE-SIMON-P4-N18-")
LOHAN_PRESENT = any(u.startswith("NOTE-LOHAN-") for u in IDX)


def digest():
    """sha256 of everything this run would write for the examiner window."""
    h = hashlib.sha256()
    for rows in (EVIDENCE, COVERAGE):
        for r in rows:
            h.update((json.dumps(r, ensure_ascii=False, sort_keys=True)
                      + "\n").encode("utf-8"))
    return h.hexdigest()


if "--emit-digest" in sys.argv:
    print(digest())
    sys.exit(0)


def ranked_lists(idx, idf, default):
    return {s["source_id"]: C.best_support(C.source_tokens(s), idx, idf,
                                           default, limit=len(idx))
            for s in SRC}


def synthetic_series(units):
    """A cue-free series that ties every unit and wins every tie-break.

    Each unit is cloned under an id that sorts before every real id
    ('NOTE-0SYN-' < 'NOTE-A...'), so the clone has the original's score tuple
    and outranks it on the unit-id tie-break: the LOHAN displacement
    mechanism, at its worst, without any LOHAN content. The clones add no
    ledger entry, so they name no examiner.
    """
    clone = {u["note_unit_id"]: "NOTE-0SYN-" + u["note_unit_id"][5:]
             for u in units}
    out = []
    for u in units:
        c = dict(u)
        c["note_unit_id"] = clone[u["note_unit_id"]]
        c["parent_unit_id"] = clone.get(u["parent_unit_id"])
        c["series"] = "SYNTHETIC_CUE_FREE"
        c["file"] = "synthetic-cue-free.html"
        out.append(c)
    return out


SYN_UNITS = synthetic_series(UNITS)
ok("the synthetic series names no examiner",
   not any(u["note_unit_id"] in UNIT_EXAMINERS for u in SYN_UNITS))
BASE_RANKED = ranked_lists(IDX, IDF, DEFAULT)
# Scored with the corpus's own IDF table. Doubling the corpus moves IDF, and a
# 0.001 body-coverage drift can then swap two same-tier examiner units at the
# window edge (ASC-0687): an IDF effect, not displacement. Holding IDF fixed
# makes F6-T2 measure exactly what it is for - cue-free competition - while a
# real added series is still scored with its real IDF in F6-T6.
SYN_RANKED = ranked_lists(C.unit_index(UNITS + SYN_UNITS), IDF, DEFAULT)


def t2_violations(selector):
    """(source_id, unit) pairs a cue-free series removed without a tier fall."""
    bad = []
    for s in SRC:
        sid, ex = s["source_id"], s.get("surveyor_normalized")
        before = selector(BASE_RANKED[sid], ex, UNIT_EXAMINERS)
        after = set(selector(SYN_RANKED[sid], ex, UNIT_EXAMINERS))
        tier_before = {h["note_unit_id"]: h["notes_support"]
                       for h in BASE_RANKED[sid]}
        tier_after = {h["note_unit_id"]: h["notes_support"]
                      for h in SYN_RANKED[sid]}
        for u in before:
            if u in after:
                continue
            fell = (C.SUPPORT_RANK[tier_after.get(u, C.NO_SUPPORT)]
                    < C.SUPPORT_RANK[tier_before[u]])
            if not fell:
                bad.append((sid, u))
    return bad


def top5_intersection(ranked, examiner, unit_examiners):
    """The P0 rule recast as a selector: only the content top 5 is looked at."""
    return I.examiner_named_support(ranked[:5], examiner, unit_examiners)


# ==========================================================================
# F6-T1  determinism under PYTHONHASHSEED 0 / 1 / 524287
# ==========================================================================
_digests = {}
for _seed in ("0", "1", "524287"):
    _env = dict(os.environ, PYTHONHASHSEED=_seed, PYTHONIOENCODING="utf-8")
    _p = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                         "--emit-digest"], env=_env, capture_output=True,
                        text=True)
    _digests[_seed] = _p.stdout.strip() if _p.returncode == 0 else (
        "ERROR " + _p.stderr.strip()[-300:])
ok("F6-T1 output is byte-identical under PYTHONHASHSEED 0/1/524287",
   len(set(_digests.values())) == 1 and not any(
       d.startswith("ERROR") for d in _digests.values()), str(_digests))
ok("F6-T1 the in-process run matches the seeded runs",
   digest() in _digests.values(), digest())

# ==========================================================================
# F6-T2  a cue-free series removes no P2 unit unless its own tier fell
# ==========================================================================
_t2 = t2_violations(I.examiner_named_support)
ok("F6-T2 the synthetic cue-free series removes no P2 unit without a tier "
   "fall", not _t2, str(_t2[:10]))

# ==========================================================================
# F6-T3  notes_support / notes_units identical with and without P2
# ==========================================================================
_t3 = []
for s in SRC:
    # best_support's window is a prefix of its full ranked scan
    p0 = BASE_RANKED[s["source_id"]][:5]
    ex = s.get("surveyor_normalized")
    rec = BY_SID[s["source_id"]]
    p0_cued = sorted({h["note_unit_id"] for h in p0
                      if ex in UNIT_EXAMINERS.get(h["note_unit_id"], ())})
    if (rec["notes_units"] != p0
            or rec["notes_support"] != (p0[0]["notes_support"] if p0
                                        else C.NO_SUPPORT)
            or rec["notes_units_naming_this_examiner"] != p0_cued):
        _t3.append(s["source_id"])
ok("F6-T3 notes_support, notes_units and notes_units_naming_this_examiner "
   "equal the P0 computation", not _t3, str(_t3[:10]))
ok("F6-T3 one coverage record per source ask, in source-id order",
   [c["source_id"] for c in COVERAGE]
   == sorted(s["source_id"] for s in SRC))

# ==========================================================================
# F6-T4  tier >= TOPIC and the ledger names the examiner for every P2 unit
# F6-T5  <= 5 units, in total order, the first ones of the full scan
# ==========================================================================
_t4, _t5 = [], []
for s in SRC:
    sid, ex = s["source_id"], s.get("surveyor_normalized")
    got = BY_SID[sid]["examiner_named_supporting_units"]
    pos = {h["note_unit_id"]: i for i, h in enumerate(BASE_RANKED[sid])}
    for u in got:
        h = BASE_RANKED[sid][pos[u]] if u in pos else None
        if (h is None or C.SUPPORT_RANK[h["notes_support"]]
                < C.SUPPORT_RANK[C.TOPIC_SUPPORT]
                or ex not in UNIT_EXAMINERS.get(u, ())):
            _t4.append((sid, u))
    want = [h["note_unit_id"] for h in BASE_RANKED[sid]
            if ex in UNIT_EXAMINERS.get(h["note_unit_id"], ())][:5]
    order = [pos.get(u, -1) for u in got]
    if len(got) > 5 or got != want or order != sorted(set(order)):
        _t5.append(sid)
ok("F6-T4 every P2 unit reaches TOPIC and is ledger-named for the examiner",
   not _t4, str(_t4[:10]))
ok("F6-T5 at most 5 P2 units, in total order, none skipped", not _t5,
   str(_t5[:10]))
ok("F6-T5 the window constant is 5", I.EXAMINER_WINDOW == 5)

# ==========================================================================
# F6-T6  ASC-0130 keeps Simon P1-N9 and P4-N18 with LOHAN present
# ==========================================================================
def _keeps_simon(units):
    return all(any(u.startswith(p) for u in units) for p in SIMON_0130)


ok("F6-T6 production: ASC-0130 carries Simon P1-N9 and P4-N18",
   _keeps_simon(BY_SID[ASC_0130]["examiner_named_supporting_units"]),
   str(BY_SID[ASC_0130]["examiner_named_supporting_units"]))
_syn_0130 = I.examiner_named_support(
    SYN_RANKED[ASC_0130], BY_SID[ASC_0130]["examiner"], UNIT_EXAMINERS)
ok("F6-T6 proxy: ASC-0130 keeps Simon P1-N9 and P4-N18 under the synthetic "
   "cue-free series", _keeps_simon(_syn_0130), str(_syn_0130))
if LOHAN_PRESENT:
    ok("F6-T6 LOHAN: ASC-0130 keeps Simon P1-N9 and P4-N18 with LOHAN present",
       _keeps_simon(BY_SID[ASC_0130]["examiner_named_supporting_units"]),
       str(BY_SID[ASC_0130]["examiner_named_supporting_units"]))

# ==========================================================================
# F6-T7  0 / 788 canonical dispositions change
# ==========================================================================
_t7 = [c["source_id"] for c in COVERAGE
       if (c["canonical_disposition"], c["canonical_question_id"])
       != (RECON.get(c["source_id"], {}).get("content_disposition"),
           RECON.get(c["source_id"], {}).get("matched_question_id"))]
ok("F6-T7 788 source asks are covered", len(COVERAGE) == 788,
   str(len(COVERAGE)))
ok("F6-T7 0 canonical dispositions differ from the reconciliation", not _t7,
   str(_t7[:10]))
_recon_src = (Path(__file__).resolve().parent / "reconcile_788.py").read_text(
    encoding="utf-8")
ok("F6-T7 the canonical reconciliation reads nothing the examiner window "
   "writes", not any(x in _recon_src for x in (
       "ingest_oral_notes", "ORAL_NOTES_COVERAGE",
       "examiner_named_supporting_units")))

# ==========================================================================
# F6-T8  the top-5 intersection mutant must fail F6-T2 on ASC-0130
# ==========================================================================
_t8 = t2_violations(top5_intersection)
ok("F6-T8 the top-5 intersection fails F6-T2 on ASC-0130",
   any(sid == ASC_0130 for sid, _ in _t8), str(_t8[:10]))

# ==========================================================================
# read-only: the committed examiner ledger is untouched (A-4)
# ==========================================================================
ok("the committed examiner ledger is unchanged by this run",
   (LEDGER.read_bytes() if LEDGER.exists() else None) == LEDGER_BYTES)


# ==========================================================================
if __name__ == "__main__":
    _p0 = sum(1 for c in COVERAGE if c["notes_units_naming_this_examiner"])
    _p2 = sum(1 for c in COVERAGE if c["examiner_named_supporting_units"])
    print("corpus: %d units%s | evidence %d | occurrences with examiner "
          "support: P0 %d -> P2 %d" % (
              len(UNITS), " (LOHAN present)" if LOHAN_PRESENT else
              " (no LOHAN: F6-T6 proxy only)", len(EVIDENCE), _p0, _p2))
    print("F6-T1 digests %s" % json.dumps(_digests, sort_keys=True))
    print("F6-T8 mutant violations %d (ASC-0130: %s)" % (
        len(_t8), sorted(u for sid, u in _t8 if sid == ASC_0130)))
    for f in FAILURES:
        print("FAIL  " + f)
    print("\n%d examiner window controls / %d failures" % (
        CHECKS[0], len(FAILURES)))
    sys.exit(1 if FAILURES else 0)
