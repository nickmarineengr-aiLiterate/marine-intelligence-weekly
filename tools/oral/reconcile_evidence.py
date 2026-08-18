"""Reconcile every historical MIW examiner record against the live Oral QB
and against the current examiner-index, and emit the evidence ledger.

Entities kept strictly apart (see ORAL_EXISTING_TRUTH_AUDIT.md §4):
  * canonical question       - one live q-card
  * evidence record          - one source row asserting an examiner asked it
  * examiner->question pair  - deduplicated relationship
  * index connection         - a pair the live examiner-index actually shows

Usage:
  python tools/oral/reconcile_evidence.py --master <xlsx> --july <xlsx>
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402
import audit_sources as S  # noqa: E402

ALIASES = {
    "nair": "Nair",
    "nair sir": "Nair",
    "simon": "Simon",
    "simon sir": "Simon",
    "rajappan": "Rajappan",
    "rajappan sir": "Rajappan",
    "srivastava": "Srivastava",
    "srivastava sir": "Srivastava",
    "senthil": "Senthil",
    "senthil sir": "Senthil",
    "paul": "Paul",
    "paul sir": "Paul",
    "john": "John",
    "john sir": "John",
}

# match thresholds, applied to the *token* similarity in oral_lib
T_VERIFIED = 0.75
T_SAME_CORE = 0.50
T_PARTIAL = 0.34

# Evidence provenance. The July per-examiner sheets restate canonical MIW
# wording and are 100% subsumed by examiner-index.html: they are a sibling
# product surface of the same attribution pass, never independent proof.
PRIMARY = "PRIMARY_CANDIDATE_RECORD"
DERIVED = "DERIVED_PRODUCT_SURFACE"


NON_EXAMINER = {
    "untraced whatsapp locate thread": "UNTRACED_SOURCE",
    "nixon own notes": "FOUNDER_NOTES",
    "not yet assigned": "UNATTRIBUTED",
    "rathesh whatsapp report": "CANDIDATE_REPORTER_NOT_EXAMINER",
}


def normalise_examiner(raw):
    k = L.norm(raw)
    return ALIASES.get(k), k


def attribution_kind(raw):
    k = L.norm(raw)
    if k in ALIASES:
        return "EXAMINER"
    return NON_EXAMINER.get(k, "UNKNOWN_ATTRIBUTION" if k else "EMPTY")


def best_match(text, candidates):
    """candidates: list of inventory rows. Returns (row, score, runner_up)."""
    scored = sorted(
        ((L.containment(text, c["question_text"]), L.jaccard(text, c["question_text"]), c)
         for c in candidates),
        key=lambda t: (t[1], t[0]),
        reverse=True,
    )
    if not scored:
        return None, 0.0, 0.0
    cont, jac, row = scored[0]
    runner = scored[1][1] if len(scored) > 1 else 0.0
    return row, jac, runner


def classify(score, runner, file_ok):
    if not file_ok:
        return "STALE_TARGET"
    if score >= T_VERIFIED:
        return "VERIFIED_MATCH"
    if score >= T_SAME_CORE:
        return "VERIFIED_SAME_CORE"
    if score >= T_PARTIAL:
        if runner >= score - 0.05:
            return "AMBIGUOUS"
        return "PARTIAL_MATCH"
    if score > 0:
        return "WRONG_MATCH"
    return "UNRESOLVED"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", required=True)
    ap.add_argument("--july", required=True)
    a = ap.parse_args()

    inv = L.build_inventory()
    by_file = collections.defaultdict(list)
    for r in inv:
        by_file[r["file"]].append(r)
    by_qid = {r["canonical_question_id"]: r for r in inv}

    ix = L.parse_examiner_index(L.MEO / "examiner-index.html")
    index_pairs = set()
    index_tier = {}
    for r in ix["rows"]:
        f, anch = L.split_href(r["href"])
        ex = normalise_examiner(r["examiner_raw"])[0]
        qid = Path(f).stem + "#" + anch
        index_pairs.add((ex, qid))
        # keep the strongest tier seen for the pair
        rank = {"confirmed": 3, "ce_tip": 2, "cetip": 2, "header": 1, "inferred": 0}
        if index_tier.get((ex, qid)) is None or rank.get(r["tier"], -1) > rank.get(
            index_tier[(ex, qid)], -1
        ):
            index_tier[(ex, qid)] = r["tier"]

    ledger = []
    legacy_review = []
    unresolved = []

    # ---------------- source A: master tracker (All Questions) --------------
    m = S.audit_master(Path(a.master))
    for i, r in enumerate(m["tracker"]):
        ex_norm, ex_key = normalise_examiner(r.get("Examiner"))
        raw_q = str(r.get("Question") or "").strip()
        live_file = str(r.get("Live_File") or "").strip()
        matched_txt = str(r.get("Live_Q_Text (matched)") or "").strip()
        build = str(r.get("Build_Status") or "").strip()
        conf = str(r.get("Match_Confidence") or "").strip()
        rec = {
            "evidence_id": "MASTER-AQ-%04d" % (i + 1),
            "evidence_source": "MEO_QB_master_v26.xlsx#All Questions",
            "evidence_class": PRIMARY,
            "source_record_id": str(r.get("No.") or i + 1),
            "examiner_raw": str(r.get("Examiner") or ""),
            "examiner_normalized": ex_norm,
            "attribution_kind": attribution_kind(r.get("Examiner")),
            "source_wording": raw_q,
            "source_date": str(r.get("Date") or ""),
            "attempt": str(r.get("Attempt") or ""),
            "vessel": str(r.get("Vessel") or ""),
            "result": str(r.get("Result") or ""),
            "claimed_live_file": live_file,
            "claimed_live_text": matched_txt,
            "legacy_build_status": build,
            "legacy_match_confidence": conf,
        }
        if not live_file:
            rec.update(
                disposition="NO_CURRENT_QB_MATCH" if not build else "STALE_SOURCE_RECORD",
                canonical_question_id=None,
                match_score=None,
                legacy_mapping="UNRESOLVED",
            )
            unresolved.append(rec)
            ledger.append(rec)
            continue
        cands = by_file.get(live_file, [])
        probe = matched_txt or raw_q
        row, score, runner = best_match(probe, cands)
        klass = classify(score, runner, bool(cands))
        qid = row["canonical_question_id"] if row else None
        # the legacy-defect test: does the ORIGINAL candidate ask still match?
        raw_score = L.jaccard(raw_q, row["question_text"]) if row else 0.0
        rec.update(
            canonical_question_id=qid,
            matched_question_text=row["question_text"] if row else "",
            match_score=round(score, 3),
            runner_up_score=round(runner, 3),
            source_vs_matched_score=round(raw_score, 3),
            legacy_mapping=klass,
        )
        if klass in ("VERIFIED_MATCH", "VERIFIED_SAME_CORE"):
            rec["disposition"] = (
                "ALREADY_CANONICAL_AND_LINKED"
                if (ex_norm, qid) in index_pairs
                else "ALREADY_CANONICAL_LINK_MISSING"
            )
        elif klass == "PARTIAL_MATCH":
            rec["disposition"] = "PARTIAL_COVERAGE"
        elif klass in ("WRONG_MATCH", "AMBIGUOUS"):
            rec["disposition"] = "CANONICAL_MATCH_BUT_LEGACY_MAPPING_WRONG"
        elif klass == "STALE_TARGET":
            rec["disposition"] = "STALE_SOURCE_RECORD"
        else:
            rec["disposition"] = "AMBIGUOUS"
        # legacy fuzzy-match defect: keyword overlap survives, demand does not
        if row and raw_score < T_PARTIAL and score >= T_SAME_CORE:
            legacy_review.append(
                {
                    "evidence_id": rec["evidence_id"],
                    "examiner": ex_norm,
                    "source_wording": raw_q,
                    "legacy_claimed_text": matched_txt,
                    "live_question": row["question_text"],
                    "canonical_question_id": qid,
                    "source_vs_live": round(raw_score, 3),
                    "legacy_confidence": conf,
                    "defect_class": "SOURCE_ASK_NOT_COVERED_BY_MAPPED_QUESTION",
                }
            )
        elif row and raw_score < T_PARTIAL and score < T_SAME_CORE:
            legacy_review.append(
                {
                    "evidence_id": rec["evidence_id"],
                    "examiner": ex_norm,
                    "source_wording": raw_q,
                    "legacy_claimed_text": matched_txt,
                    "live_question": row["question_text"],
                    "canonical_question_id": qid,
                    "source_vs_live": round(raw_score, 3),
                    "legacy_confidence": conf,
                    "defect_class": "MAPPING_UNVERIFIABLE_AGAINST_LIVE_FILE",
                }
            )
        ledger.append(rec)

    # ---------------- source B: July per-examiner sheets --------------------
    j = S.audit_july(Path(a.july))
    for ex_sheet, rows in j["per_examiner"].items():
        ex_norm, _ = normalise_examiner(ex_sheet)
        for i, r in enumerate(rows):
            q = str(r.get("question") or "").strip()
            link = r.get("link") or ""
            fname = Path(link.split("#")[0]).name if link else ""
            cands = by_file.get(fname) or inv
            row, score, runner = best_match(q, cands)
            klass = classify(score, runner, bool(cands))
            qid = row["canonical_question_id"] if row else None
            rec = {
                "evidence_id": "JULY-%s-%03d" % (ex_sheet[:4].upper(), i + 1),
                "evidence_source": "MIW_July2026_QuestionBank_SHARE.xlsx#" + ex_sheet,
                "evidence_class": DERIVED,
                "source_record_id": str(r.get("no") or i + 1),
                "examiner_raw": ex_sheet,
                "examiner_normalized": ex_norm,
                "attribution_kind": attribution_kind(ex_sheet),
                "source_wording": q,
                "source_date": "2026-07",
                "claimed_live_file": fname,
                "claimed_live_text": "",
                "legacy_build_status": "",
                "legacy_match_confidence": "july-sheet-hyperlink(file-only)",
                "canonical_question_id": qid,
                "matched_question_text": row["question_text"] if row else "",
                "match_score": round(score, 3),
                "runner_up_score": round(runner, 3),
                "source_vs_matched_score": round(score, 3),
                "legacy_mapping": klass,
            }
            if klass in ("VERIFIED_MATCH", "VERIFIED_SAME_CORE"):
                rec["disposition"] = (
                    "ALREADY_CANONICAL_AND_LINKED"
                    if (ex_norm, qid) in index_pairs
                    else "ALREADY_CANONICAL_LINK_MISSING"
                )
            elif klass == "PARTIAL_MATCH":
                rec["disposition"] = "PARTIAL_COVERAGE"
            else:
                rec["disposition"] = "AMBIGUOUS"
            ledger.append(rec)

    # ---------------- source C: June/July "New Questions" -------------------
    for i, r in enumerate(j["new_questions"]):
        ex_norm, _ = normalise_examiner(r.get("Examiner"))
        q = str(r.get("Question") or "").strip()
        link = r.get("link") or ""
        fname = Path(link.split("#")[0]).name if link else ""
        cands = by_file.get(fname) or inv
        row, score, runner = best_match(q, cands)
        klass = classify(score, runner, bool(cands))
        qid = row["canonical_question_id"] if row else None
        rec = {
            "evidence_id": "JULY-NEW-%03d" % (i + 1),
            "evidence_source": "MIW_July2026_QuestionBank_SHARE.xlsx#New Questions (July 2026)",
            "evidence_class": PRIMARY,
            "source_record_id": str(r.get("No.") or i + 1),
            "examiner_raw": str(r.get("Examiner") or ""),
            "examiner_normalized": ex_norm,
            "attribution_kind": attribution_kind(r.get("Examiner")),
            "source_wording": q,
            "source_date": "2026-07",
            "vessel": str(r.get("Ship Type") or ""),
            "claimed_live_file": fname,
            "legacy_match_confidence": "july-new-hyperlink(file-only)",
            "canonical_question_id": qid,
            "matched_question_text": row["question_text"] if row else "",
            "match_score": round(score, 3),
            "runner_up_score": round(runner, 3),
            "source_vs_matched_score": round(score, 3),
            "legacy_mapping": klass,
        }
        if klass in ("VERIFIED_MATCH", "VERIFIED_SAME_CORE"):
            rec["disposition"] = (
                "ALREADY_CANONICAL_AND_LINKED"
                if (ex_norm, qid) in index_pairs
                else "ALREADY_CANONICAL_LINK_MISSING"
            )
        elif klass == "PARTIAL_MATCH":
            rec["disposition"] = "PARTIAL_COVERAGE"
        else:
            rec["disposition"] = "AMBIGUOUS"
        ledger.append(rec)

    # ---------------- derive pairs from evidence ----------------------------
    pair_evidence = collections.defaultdict(list)
    primary_evidence = collections.defaultdict(list)
    for rec in ledger:
        ex, qid = rec.get("examiner_normalized"), rec.get("canonical_question_id")
        if ex and qid and rec["legacy_mapping"] in ("VERIFIED_MATCH", "VERIFIED_SAME_CORE"):
            pair_evidence[(ex, qid)].append(rec["evidence_id"])
            if rec.get("evidence_class") == PRIMARY:
                primary_evidence[(ex, qid)].append(rec["evidence_id"])

    gaps = []
    for (ex, qid), evids in sorted(primary_evidence.items()):
        if (ex, qid) in index_pairs:
            continue
        q = by_qid.get(qid)
        gaps.append(
            {
                "examiner": ex,
                "canonical_question_id": qid,
                "url": q["url"] if q else "",
                "question_text": q["question_text"] if q else "",
                "evidence_count": len(evids),
                "evidence_ids": ";".join(evids),
                "classification": (
                    "READY_CONNECTION_MULTI_SOURCE" if len(evids) > 1 else "READY_CONNECTION"
                ),
            }
        )

    inferred_only = [
        {"examiner": ex, "canonical_question_id": qid, "tier": t}
        for (ex, qid), t in sorted(index_tier.items())
        if t == "inferred" and (ex, qid) not in primary_evidence
    ]
    supported = [
        (ex, qid) for (ex, qid), t in index_tier.items() if (ex, qid) in primary_evidence
    ]

    # ---------------- write ------------------------------------------------
    L.OUT.mkdir(parents=True, exist_ok=True)
    with (L.OUT / "EXAMINER_EVIDENCE_LEDGER.jsonl").open("w", encoding="utf-8") as fh:
        for rec in ledger:
            fh.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")

    def wcsv(name, rows):
        if not rows:
            (L.OUT / name).write_text("", encoding="utf-8")
            return
        keys = sorted({k for r in rows for k in r})
        with (L.OUT / name).open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)

    wcsv("LEGACY_MATCH_REVIEW.csv", legacy_review)
    wcsv("EXISTING_CONNECTION_GAPS.csv", gaps)
    wcsv("INFERRED_ONLY_CONNECTIONS.csv", inferred_only)

    summary = {
        "evidence_records": len(ledger),
        "evidence_by_source": dict(collections.Counter(r["evidence_source"] for r in ledger)),
        "evidence_by_examiner": dict(
            collections.Counter(r["examiner_normalized"] for r in ledger)
        ),
        "legacy_mapping_classification": dict(
            collections.Counter(r["legacy_mapping"] for r in ledger)
        ),
        "disposition": dict(collections.Counter(r["disposition"] for r in ledger)),
        "evidence_records_primary": sum(1 for r in ledger if r.get("evidence_class") == PRIMARY),
        "evidence_records_derived": sum(1 for r in ledger if r.get("evidence_class") == DERIVED),
        "attribution_kinds": dict(
            collections.Counter(r.get("attribution_kind", "EXAMINER") for r in ledger)
        ),
        "pairs_backed_by_any_evidence": len(pair_evidence),
        "pairs_backed_by_PRIMARY_evidence": len(primary_evidence),
        "index_pairs": len(index_pairs),
        "pairs_evidenced_and_linked": len(supported),
        "READY_CONNECTION_gaps": len(gaps),
        "ready_connection_by_examiner": dict(collections.Counter(g["examiner"] for g in gaps)),
        "index_pairs_with_no_evidence": len(index_pairs) - len(supported),
        "index_pairs_with_no_PRIMARY_evidence": len(index_pairs) - len(supported),
        "inferred_tier_pairs_with_primary_evidence": sum(
            1 for (ex, qid), t in index_tier.items()
            if t == "inferred" and (ex, qid) in primary_evidence
        ),
        "inferred_only_connections": len(inferred_only),
        "legacy_match_review_rows": len(legacy_review),
        "legacy_defect_classes": dict(
            collections.Counter(r["defect_class"] for r in legacy_review)
        ),
        "unresolved_source_rows": len(unresolved),
    }
    L.jdump(summary, "RECONCILIATION_SUMMARY.json")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
