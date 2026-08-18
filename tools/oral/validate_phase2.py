"""Phase 2 gate - deterministic validation of the reconciliation artefacts.

Fails closed: an unavailable input is a failure, never a silent pass. Run after
any regeneration; a new failure means something regressed.

  PYTHONIOENCODING=utf-8 python tools/oral/validate_phase2.py
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

OUT = L.OUT

CONTENT_DISPOSITIONS = {"EXACT_MATCH", "NEAR_MATCH", "SAME_CORE_ASK",
                        "PARTIAL_COVERAGE", "MISSING", "AMBIGUOUS"}
MAPPING_STATUSES = {"ALREADY_LINKED", "NEW_LINK", "CONFLICTING_LINK",
                    "UNMAPPED", "NOT_APPLICABLE"}
RELATIONSHIP_TYPES = {"PRIMARY_ASK", "CROSS_QUESTION", "FOLLOW_UP",
                      "EXPECTED_DETAIL", "UNSPECIFIED", "TOPIC_INFERENCE_ONLY"}
RESEARCH_TIERS = {"MULTI_SOURCE_CONFIRMED", "PRIMARY_CONFIRMED",
                  "EXTERNAL_SOURCE_CONFIRMED", "CE_TIP", "HEADER",
                  "INFERRED_ONLY", "CONFLICTED"}
EVIDENCE_TIERS = {"PRIMARY_TRACKER", "EXTERNAL_SURVEYOR_COMPILATION",
                  "EXPLICIT_QCARD", "CE_TIP", "HEADER_METADATA",
                  "CURRENT_INDEX_RECOVERY", "TOPIC_INFERRED"}

results = []


def check(name, ok, detail=""):
    results.append({"check": name,
                    "status": "PASS" if ok else "FAIL",
                    "detail": detail})


def jsonl(name):
    p = OUT / name
    if not p.exists():
        return None
    return [json.loads(l) for l in p.open(encoding="utf-8")]


def main():
    inv = {q["canonical_question_id"]: q for q in L.build_inventory()}
    anchors = L.all_anchors()

    rels = jsonl("CURRENT_EXAMINER_RELATIONSHIPS.jsonl")
    ev = jsonl("EXAMINER_EVIDENCE_LEDGER_V2.jsonl")
    src = jsonl("ALL_SURVEYORS_SOURCE_RECORDS.jsonl")
    recon = jsonl("ORAL_788_RECONCILIATION.jsonl")
    for name, obj in (("CURRENT_EXAMINER_RELATIONSHIPS.jsonl", rels),
                      ("EXAMINER_EVIDENCE_LEDGER_V2.jsonl", ev),
                      ("ALL_SURVEYORS_SOURCE_RECORDS.jsonl", src),
                      ("ORAL_788_RECONCILIATION.jsonl", recon)):
        check("input available: " + name, obj is not None,
              "missing" if obj is None else "%d records" % len(obj))
    if not all((rels, ev, src, recon)):
        return emit()

    gaps = json.loads((OUT / "ORAL_GAP_CANDIDATES.json").read_text(encoding="utf-8"))
    ready = json.loads((OUT / "READY_CONNECTIONS_V2.json").read_text(encoding="utf-8"))
    fams = json.loads((OUT / "ALL_SURVEYORS_SOURCE_FAMILIES.json").read_text(encoding="utf-8"))
    alias = json.loads((OUT / "EXAMINER_ALIAS_REGISTER.json").read_text(encoding="utf-8"))
    known = {e["canonical_name"] for e in alias["examiners"]} | {"John"}

    # --- identifier integrity ------------------------------------------------
    bad = [r["relationship_id"] for r in rels if r["question_id"] not in inv]
    check("every relationship resolves to a live question", not bad, str(bad[:5]))

    bad = [r["relationship_id"] for r in rels
           if not (L.MEO / r["target_file"]).exists()]
    check("every relationship target file exists", not bad, str(bad[:5]))

    bad = [r["relationship_id"] for r in rels
           if r["target_anchor"] not in anchors.get(r["target_file"], set())]
    check("every relationship anchor exists", not bad, str(bad[:5]))

    dup = [k for k, v in Counter(r["relationship_id"] for r in rels).items() if v > 1]
    check("no duplicate relationship ids", not dup, str(dup[:5]))

    dup = [k for k, v in Counter(e["evidence_id"] for e in ev).items() if v > 1]
    check("no duplicate evidence ids", not dup, str(dup[:5]))

    rel_ids = {r["relationship_id"] for r in rels}
    bad = [e["evidence_id"] for e in ev if e["relationship_id"] not in rel_ids]
    check("every evidence record resolves to a relationship", not bad, str(bad[:5]))

    ref = {i for r in rels for i in r["evidence_ids"]}
    have = {e["evidence_id"] for e in ev}
    check("every referenced evidence id exists", ref <= have, str(sorted(ref - have)[:5]))

    bad = [r["relationship_id"] for r in rels if r["examiner"] not in known]
    check("every examiner resolves in the alias register", not bad, str(bad[:5]))

    # --- vocabulary ----------------------------------------------------------
    bad = sorted({r["research_best_tier"] for r in rels} - RESEARCH_TIERS)
    check("no impossible research tier values", not bad, str(bad))

    bad = sorted({r["relationship_type"] for r in rels} - RELATIONSHIP_TYPES)
    check("relationship type vocabulary is closed (relationships)", not bad, str(bad))

    bad = sorted({e["evidence_tier"] for e in ev} - EVIDENCE_TIERS)
    check("evidence tier vocabulary is closed", not bad, str(bad))

    bad = sorted({r["evidence_tier"] for r in recon} - EVIDENCE_TIERS)
    check("788 evidence tier vocabulary is closed", not bad, str(bad))

    bad = sorted({r["relationship_type"] for r in recon} - RELATIONSHIP_TYPES)
    check("relationship type vocabulary is closed (788)", not bad, str(bad))

    # --- source accounting ---------------------------------------------------
    check("788 source occurrences ingested", len(src) == 788, "%d parsed" % len(src))

    src_ids = [s["source_id"] for s in src]
    dup = [k for k, v in Counter(src_ids).items() if v > 1]
    check("no duplicate source ids", not dup, str(dup[:5]))

    rec_ids = [r["source_id"] for r in recon]
    check("every source occurrence is dispositioned exactly once",
          sorted(rec_ids) == sorted(src_ids) and len(rec_ids) == len(set(rec_ids)),
          "%d source / %d dispositioned" % (len(src_ids), len(rec_ids)))

    bad = [r["source_id"] for r in recon
           if r["content_disposition"] not in CONTENT_DISPOSITIONS]
    check("one closed-vocabulary content disposition per occurrence", not bad, str(bad[:5]))

    bad = [r["source_id"] for r in recon
           if r["examiner_mapping_status"] not in MAPPING_STATUSES]
    check("one closed-vocabulary mapping status per occurrence", not bad, str(bad[:5]))

    bad = [r["source_id"] for r in recon
           if r["content_disposition"] != "MISSING" and r["matched_question_id"] is None]
    check("every non-MISSING occurrence carries a target", not bad, str(bad[:5]))

    bad = [r["source_id"] for r in recon
           if r["matched_question_id"] and r["matched_question_id"] not in inv]
    check("every matched question id resolves to live HTML", not bad, str(bad[:5]))

    fam_ids = {f["family_id"] for f in fams}
    bad = [r["source_id"] for r in recon if r["source_family_id"] not in fam_ids]
    check("every occurrence belongs to a known source family", not bad, str(bad[:5]))

    covered = {sid for f in fams for sid in f["source_ids"]}
    check("no source occurrence dropped by family clustering",
          covered == set(src_ids), "%d of %d covered" % (len(covered), len(src_ids)))

    # --- derived structures --------------------------------------------------
    bad = [g["gap_id"] for g in gaps
           if g["reuse_candidate"] and g["reuse_candidate"] not in inv]
    check("every gap reuse candidate resolves", not bad, str(bad[:5]))

    bad = [g["gap_id"] for g in gaps if g["source_family_id"] not in fam_ids]
    check("every gap resolves to a source family", not bad, str(bad[:5]))

    bad = [g["gap_id"] for g in gaps
           if not set(g["source_ids"]) <= set(src_ids)]
    check("every gap traces to real source occurrences", not bad, str(bad[:5]))

    bad = [r["canonical_question_id"] for r in ready
           if r["canonical_question_id"] not in inv]
    check("every ready connection resolves to a live question", not bad, str(bad[:5]))

    bad = [r["canonical_question_id"] for r in ready if r["examiner"] not in known]
    check("every ready-connection examiner resolves", not bad, str(bad[:5]))

    # --- counts are derived, never carried -----------------------------------
    summ = json.loads((OUT / "ORAL_788_RECONCILIATION_SUMMARY.json").read_text(encoding="utf-8"))
    live = dict(Counter(r["content_disposition"] for r in recon))
    check("summary dispositions recomputed from records",
          live == summ["content_dispositions"], "summary vs recount")

    matrix = (OUT / "ORAL_788_RECONCILIATION_MATRIX.md").read_text(encoding="utf-8")
    check("matrix reports the ingested total",
          "| Raw source occurrences ingested | 788 |" in matrix,
          "matrix headline total")

    # --- boundary: this phase writes no live candidate page ------------------
    check("research outputs stay inside the audit folder",
          OUT.name == "examiner-audit" and OUT.parent.name == "oral-intelligence",
          str(OUT))
    stray = [p.name for p in OUT.glob("*")
             if p.suffix.lower() in (".html", ".htm")]
    check("no HTML page written into the research folder", not stray, str(stray[:5]))

    return emit()


def emit():
    n_pass = sum(1 for r in results if r["status"] == "PASS")
    n_fail = len(results) - n_pass
    L.jdump({"passed": n_pass, "failed": n_fail, "checks": results},
            "PHASE2_VALIDATION_RESULTS.json")
    for r in results:
        print("%-5s %s %s" % (r["status"], r["check"],
                              ("- " + r["detail"]) if r["status"] == "FAIL" else ""))
    print("\n%d PASS / %d FAIL" % (n_pass, n_fail))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
