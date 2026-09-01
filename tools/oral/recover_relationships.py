"""Phase 2 step 1 - recover the rendered examiner index into canonical data.

The 863 question-level examiner pairings exist in exactly one hand-uploaded
HTML file with no generator and no upstream source. This tool lifts them into
a relationship ledger plus an evidence ledger, so the relation survives the
file.

CURRENT_INDEX_RECOVERY is never independent evidence: it records what the
existing product asserts, nothing more.

Outputs (meoclass1/oral-intelligence/examiner-audit/):
  CURRENT_EXAMINER_RELATIONSHIPS.jsonl
  EXAMINER_EVIDENCE_LEDGER_V2.jsonl
  RELATIONSHIP_RECOVERY_REPORT.json
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

OUT = L.OUT
INDEX = L.MEO / "examiner-index.html"

# Derived from the governed config -- see oral_lib.examiner_tier_literals.
VALID_TIERS = L.examiner_tier_literals()
# invalid literals seen in the wild -> the tier the row was meant to carry
TIER_REPAIR = {"cetip": "ce_tip"}

PROSE_RANK = {"STRONG_CE_TIP_ASSERTION": 3, "SUPPORTED_CE_TIP_MENTION": 2}


def load_prose():
    """canonical_question_id -> {examiner: strength} from the Phase 1 prose scan."""
    out = defaultdict(dict)
    for name in ("PROSE_EXAMINER_EVIDENCE.csv", "PROSE_CONNECTION_GAPS.csv"):
        p = OUT / name
        if not p.exists():
            continue
        with p.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                qid, ex = r["canonical_question_id"], r["examiner"]
                prev = out[qid].get(ex)
                if prev is None or PROSE_RANK.get(r["strength"], 1) > PROSE_RANK.get(prev, 1):
                    out[qid][ex] = r["strength"]
    return out


# Only these legacy mappings mean the source ask actually reached the question.
CONFIRMING_MAPPINGS = {"VERIFIED_MATCH", "VERIFIED_SAME_CORE"}


def load_primary():
    """(qid, examiner) -> [evidence_id], primary records only.

    The July per-examiner sheets are `DERIVED_PRODUCT_SURFACE` (a sibling of the
    index, 100% overlapping it). Counting them here would be circular and would
    inflate every confirmed number, so they are excluded — Phase 1 trap #4.
    """
    out = defaultdict(list)
    derived = defaultdict(list)
    with (OUT / "EXAMINER_EVIDENCE_LEDGER.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if r.get("attribution_kind") != "EXAMINER":
                continue
            qid = r.get("canonical_question_id")
            ex = r.get("examiner_normalized")
            if not qid or not ex:
                continue
            if r.get("evidence_class") != "PRIMARY_CANDIDATE_RECORD":
                derived[(qid, ex)].append(r["evidence_id"])
                continue
            if r.get("legacy_mapping") not in CONFIRMING_MAPPINGS:
                continue
            out[(qid, ex)].append(r["evidence_id"])
    return out, derived


def main():
    inv = {q["canonical_question_id"]: q for q in L.build_inventory()}
    parsed = L.parse_examiner_index(INDEX)
    prose = load_prose()
    primary, derived = load_primary()

    rels = {}
    evidence = []
    recovery_stats = Counter()
    blank_rows, invalid_tier_rows, duplicate_rows, drift_rows = [], [], [], []

    for row in parsed["rows"]:
        fname, anchor = L.split_href(row["href"])
        qid = Path(fname).stem + "#" + anchor
        live = inv.get(qid)
        examiner = row["examiner_raw"].split()[0]

        raw_tier = row["tier"]
        tier_valid = raw_tier in VALID_TIERS
        repaired_tier = raw_tier if tier_valid else TIER_REPAIR.get(raw_tier, "inferred")
        if not tier_valid:
            invalid_tier_rows.append({
                "row_index": row["row_index"],
                "examiner": examiner,
                "canonical_question_id": qid,
                "invalid_literal": raw_tier,
                "badge_text": row["badge"],
                "intended_tier": repaired_tier,
                "defect": "filterTier() has no toggle for this literal; the row "
                          "disappears permanently the first time a candidate filters",
            })

        display = row["display_text"]
        live_text = live["question_text"] if live else ""
        if not display.strip():
            recovery_status = "RECOVERED_FROM_LIVE_HTML" if live_text else "UNRECOVERABLE"
            blank_rows.append({
                "row_index": row["row_index"],
                "examiner": examiner,
                "canonical_question_id": qid,
                "recovered_text": live_text,
                "recovery_status": recovery_status,
            })
        elif live_text and L.jaccard(display, live_text) < 0.75:
            recovery_status = "DISPLAY_TEXT_DRIFT"
            drift_rows.append({
                "row_index": row["row_index"],
                "examiner": examiner,
                "canonical_question_id": qid,
                "index_display_text": display,
                "live_question_text": live_text,
                "similarity": round(L.jaccard(display, live_text), 3),
            })
        else:
            recovery_status = "DISPLAY_MATCHES_LIVE"
        recovery_stats[recovery_status] += 1

        key = (qid, examiner)
        ev_id = "IDXREC-%04d" % row["row_index"]
        evidence.append({
            "evidence_id": ev_id,
            "relationship_id": None,
            "examiner_raw": row["examiner_raw"],
            "examiner_normalized": examiner,
            "source_type": "CURRENT_INDEX_RECOVERY",
            "source_id": "meoclass1/examiner-index.html",
            "source_location": "row %d, section ex-%s" % (row["row_index"], row["examiner_slug"]),
            "source_date": None,
            "raw_question_text": display,
            "source_comment": row["badge"],
            "evidence_tier": "CURRENT_INDEX_RECOVERY",
            "match_status": "RESOLVED" if live else "UNRESOLVED_TARGET",
            "notes": "Records what the published index asserts. Not independent evidence.",
            "_row_index": row["row_index"],
        })

        if key in rels:
            rels[key]["duplicate_row_indexes"].append(row["row_index"])
            rels[key]["evidence_ids"].append(ev_id)
            duplicate_rows.append({
                "canonical_question_id": qid,
                "examiner": examiner,
                "row_indexes": list(rels[key]["duplicate_row_indexes"]),
                "resolution": "ONE_RELATIONSHIP_TWO_INDEX_ROWS",
            })
            continue

        rels[key] = {
            "relationship_id": "REL-%s-%s" % (examiner.upper(), qid.replace("#", "-")),
            "question_id": qid,
            "examiner": examiner,
            "examiner_raw": row["examiner_raw"],
            "target_file": fname,
            "target_anchor": anchor,
            "relationship_type": "UNSPECIFIED",
            "status": "PUBLISHED",
            "current_tier": raw_tier,
            "current_tier_valid": tier_valid,
            "repaired_tier": repaired_tier,
            "index_display_text": display,
            "current_question_text": live_text,
            "recovery_status": recovery_status,
            "source_layer": "CURRENT_INDEX_RECOVERY",
            "first_row_index": row["row_index"],
            "duplicate_row_indexes": [row["row_index"]],
            "evidence_ids": [ev_id],
            "notes": "",
        }

    for (qid, ex), rel in rels.items():
        prim = primary.get((qid, ex), [])
        pstr = prose.get(qid, {}).get(ex)
        rel["primary_evidence_ids"] = prim
        rel["primary_evidence_count"] = len(prim)
        rel["derived_sibling_evidence_count"] = len(derived.get((qid, ex), []))
        rel["prose_strength"] = pstr
        if len(prim) >= 2:
            best = "MULTI_SOURCE_CONFIRMED"
        elif len(prim) == 1:
            best = "PRIMARY_CONFIRMED"
        elif pstr:
            best = "CE_TIP"
        elif rel["current_tier"] == "header":
            best = "HEADER"
        else:
            best = "INFERRED_ONLY"
        rel["research_best_tier"] = best
        rel["evidence_count"] = len(rel["evidence_ids"]) + len(prim)
        rel["tier_changed"] = not (
            (best in ("MULTI_SOURCE_CONFIRMED", "PRIMARY_CONFIRMED")
             and rel["current_tier"] == "confirmed")
            or (best == "CE_TIP" and rel["current_tier"] in ("ce_tip", "cetip"))
            or (best == "HEADER" and rel["current_tier"] == "header")
            or (best == "INFERRED_ONLY" and rel["current_tier"] == "inferred")
        )

    owner = {}
    for rel in rels.values():
        for ri in rel["duplicate_row_indexes"]:
            owner[ri] = rel["relationship_id"]
    for e in evidence:
        e["relationship_id"] = owner.get(e.pop("_row_index"))

    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "CURRENT_EXAMINER_RELATIONSHIPS.jsonl").open("w", encoding="utf-8") as fh:
        for rel in sorted(rels.values(), key=lambda r: r["first_row_index"]):
            fh.write(json.dumps(rel, ensure_ascii=False) + "\n")
    with (OUT / "EXAMINER_EVIDENCE_LEDGER_V2.jsonl").open("w", encoding="utf-8") as fh:
        for e in evidence:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")

    report = {
        "index_rows_rendered": len(parsed["rows"]),
        "unique_relationships_recovered": len(rels),
        "evidence_records_written": len(evidence),
        "recovery_status": dict(recovery_stats),
        "blank_display_row_count": len(blank_rows),
        "blank_display_rows": blank_rows,
        "invalid_tier_rows": invalid_tier_rows,
        "duplicate_relationships": duplicate_rows,
        "display_text_drifts": drift_rows,
        "unresolved_targets": [r["question_id"] for r in rels.values()
                               if not r["current_question_text"]],
        "per_examiner_relationships": dict(Counter(r["examiner"] for r in rels.values())),
        "current_tier_distribution": dict(Counter(r["current_tier"] for r in rels.values())),
        "research_tier_distribution": dict(Counter(r["research_best_tier"] for r in rels.values())),
        "relationships_whose_tier_changes": sum(1 for r in rels.values() if r["tier_changed"]),
        "july_derived_sibling_check": {
            "relationships_also_present_in_july_per_examiner_sheets":
                sum(1 for r in rels.values() if r["derived_sibling_evidence_count"]),
            "note": "July per-examiner rows are excluded from tier strength as "
                    "DERIVED_PRODUCT_SURFACE; this count only shows the overlap.",
        },
    }
    L.jdump(report, "RELATIONSHIP_RECOVERY_REPORT.json")
    print(json.dumps({k: v for k, v in report.items() if not isinstance(v, list)}, indent=2))
    print("blank=%d invalid_tier=%d duplicate_rows=%d drifts=%d" % (
        len(blank_rows), len(invalid_tier_rows), len(duplicate_rows), len(drift_rows)))


if __name__ == "__main__":
    main()
