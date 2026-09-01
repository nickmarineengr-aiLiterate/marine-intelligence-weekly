"""Audit meoclass1/examiner-index.html against the live Oral QB.

Reproduces every count from the rendered rows, resolves every link against
the real files and anchors, and reports drift between the displayed text and
the live question text.

Usage:  python tools/oral/audit_index.py
Outputs land in meoclass1/oral-intelligence/examiner-audit/.
"""
from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402


# Derived from the governed config -- see oral_lib.examiner_tier_literals.
VALID_TIERS = L.examiner_tier_literals()


def main():
    inv = L.build_inventory()
    by_qid = {r["canonical_question_id"]: r for r in inv}
    anchors = L.all_anchors()
    ix = L.parse_examiner_index(L.MEO / "examiner-index.html")
    rows = ix["rows"]

    pairs = []
    seen_pair = collections.Counter()
    for r in rows:
        fname, anchor = L.split_href(r["href"])
        qid = Path(fname).stem + "#" + anchor
        live = by_qid.get(qid)
        file_exists = (L.MEO / fname).exists()
        anchor_exists = anchor in anchors.get(fname, set())
        drift = None
        if live:
            drift = round(L.jaccard(r["display_text"], live["question_text"]), 3)
        problems = []
        if not file_exists:
            problems.append("FILE_MISSING")
        elif not anchor_exists:
            problems.append("ANCHOR_MISSING")
        elif live is None:
            problems.append("ANCHOR_NOT_A_QUESTION")
        elif not r["display_text"].strip():
            problems.append("BLANK_DISPLAY_TEXT")
        elif drift is not None and drift < 0.34:
            problems.append("TEXT_DRIFT")
        if r["tier"] not in VALID_TIERS:
            problems.append("INVALID_TIER_LITERAL")
        key = (r["examiner_slug"], qid)
        seen_pair[key] += 1
        pairs.append(
            {
                "row_index": r["row_index"],
                "examiner_slug": r["examiner_slug"],
                "examiner_raw": r["examiner_raw"],
                "tier": r["tier"],
                "href": r["href"],
                "target_file": fname,
                "target_anchor": anchor,
                "canonical_question_id": qid,
                "file_exists": file_exists,
                "anchor_exists": anchor_exists,
                "resolves_to_live_question": live is not None,
                "display_text": r["display_text"],
                "live_question_text": live["question_text"] if live else "",
                "text_similarity": drift,
                "status": ",".join(problems) or "OK",
            }
        )
    for p in pairs:
        p["duplicate_pair"] = seen_pair[(p["examiner_slug"], p["canonical_question_id"])] > 1

    # ---------------- counts ----------------
    tiers = collections.Counter(r["tier"] for r in rows)
    per_ex = collections.Counter(r["examiner_slug"] for r in rows)
    per_ex_tier = collections.defaultdict(collections.Counter)
    for r in rows:
        per_ex_tier[r["examiner_slug"]][r["tier"]] += 1

    unique_pairs = {(p["examiner_slug"], p["canonical_question_id"]) for p in pairs}
    linked_q = {p["canonical_question_id"] for p in pairs if p["resolves_to_live_question"]}
    ex_per_q = collections.defaultdict(set)
    for p in pairs:
        if p["resolves_to_live_question"]:
            ex_per_q[p["canonical_question_id"]].add(p["examiner_slug"])

    report = {
        "live_qb": {
            "files": len(set(r["file"] for r in inv)),
            "questions": len(inv),
            "gated_files": len({r["file"] for r in inv if r["gated"]}),
            "questions_without_answer": sum(1 for r in inv if not r["has_answer"]),
        },
        "examiner_index": {
            "rendered_rows": len(rows),
            "header_claims": ix["header"],
            "mininav_claims": ix["mininav"],
            "mininav_sum": sum(ix["mininav"].values()),
            "section_heading_counts": {s["slug"]: s["heading_count"] for s in ix["sections"]},
            "section_heading_sum": sum(s["heading_count"] or 0 for s in ix["sections"]),
            "ex_stats_partial": {s["slug"]: s["ex_stats"] for s in ix["sections"]},
            "rendered_rows_per_examiner": dict(per_ex),
            "tier_distribution": dict(tiers),
            "tier_distribution_per_examiner": {k: dict(v) for k, v in per_ex_tier.items()},
            "unique_examiner_question_pairs": len(unique_pairs),
            "duplicate_rows": sum(1 for p in pairs if p["duplicate_pair"]),
        },
        "link_integrity": {
            "rows_ok": sum(1 for p in pairs if p["status"] == "OK"),
            "file_missing": sum(1 for p in pairs if "FILE_MISSING" in p["status"]),
            "anchor_missing": sum(1 for p in pairs if "ANCHOR_MISSING" in p["status"]),
            "anchor_not_a_question": sum(
                1 for p in pairs if "ANCHOR_NOT_A_QUESTION" in p["status"]
            ),
            "text_drift": sum(1 for p in pairs if "TEXT_DRIFT" in p["status"]),
            "blank_display_text": sum(1 for p in pairs if "BLANK_DISPLAY_TEXT" in p["status"]),
            "invalid_tier_literal": sum(1 for p in pairs if "INVALID_TIER_LITERAL" in p["status"]),
        },
        "coverage": {
            "live_questions_with_examiner": len(linked_q),
            "live_questions_without_examiner": len(inv) - len(linked_q),
            "multi_examiner_questions": sum(1 for v in ex_per_q.values() if len(v) > 1),
            "max_examiners_on_one_question": max((len(v) for v in ex_per_q.values()), default=0),
        },
    }

    L.jdump(report, "EXAMINER_INDEX_REPRODUCTION.json")
    L.jdump(inv, "CURRENT_ORAL_QB_INVENTORY.json")

    L.OUT.mkdir(parents=True, exist_ok=True)
    cols = list(pairs[0].keys())
    with (L.OUT / "EXAMINER_INDEX_PAIRS.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(pairs)

    import json

    print(json.dumps(report, indent=2, ensure_ascii=False))
    bad = [p for p in pairs if p["status"] != "OK"]
    print("\n--- first 25 problem rows ---")
    for p in bad[:25]:
        print(
            p["status"],
            "|",
            p["examiner_slug"],
            "|",
            p["href"],
            "| sim=",
            p["text_similarity"],
            "|",
            p["display_text"][:70],
        )
    print("total problem rows:", len(bad))


if __name__ == "__main__":
    main()
