"""Phase 2 step 4 - Founder-reviewable reconciliation reporting.

Every count in every table below is derived from the records written by
`recover_relationships.py`, `ingest_all_surveyors.py` and `reconcile_788.py`.
Nothing is hand-entered: the moment a number is typed by hand it starts drifting
from the data, which is exactly the defect the live index already has.

Outputs (meoclass1/oral-intelligence/examiner-audit/):
  READY_CONNECTIONS_V2.json
  INFERRED_ONLY_DISPOSITION.csv
  CROSS_EXAMINER_FAMILIES.json
  ORAL_788_RECONCILIATION_MATRIX.md
  JOHN_RECONCILIATION.md / PAUL_ / SIMON_ / NAIR_
  HUMAN_REVIEW_QUEUE.md
  ORAL_P0_GAPS.md
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
DISPS = ["EXACT_MATCH", "NEAR_MATCH", "SAME_CORE_ASK", "PARTIAL_COVERAGE",
         "MISSING", "AMBIGUOUS"]
MAPS = ["ALREADY_LINKED", "NEW_LINK", "CONFLICTING_LINK", "UNMAPPED", "NOT_APPLICABLE"]


def jsonl(name):
    return [json.loads(l) for l in (OUT / name).open(encoding="utf-8")]


def load_csv(name):
    p = OUT / name
    if not p.exists():
        return []
    with p.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def main():
    rels = jsonl("CURRENT_EXAMINER_RELATIONSHIPS.jsonl")
    recon = jsonl("ORAL_788_RECONCILIATION.jsonl")
    src = jsonl("ALL_SURVEYORS_SOURCE_RECORDS.jsonl")
    fams = json.loads((OUT / "ALL_SURVEYORS_SOURCE_FAMILIES.json").read_text(encoding="utf-8"))
    gaps = json.loads((OUT / "ORAL_GAP_CANDIDATES.json").read_text(encoding="utf-8"))
    review = json.loads((OUT / "HUMAN_REVIEW_QUEUE.json").read_text(encoding="utf-8"))
    inv = {q["canonical_question_id"]: q for q in L.build_inventory()}

    linked = {(r["question_id"], r["examiner"]) for r in rels}
    ex_of_q = defaultdict(set)
    for r in rels:
        ex_of_q[r["question_id"]].add(r["examiner"])

    # 788 support for a pair, used to corroborate the Phase 1 ready connections
    support_788 = defaultdict(list)
    for r in recon:
        if r["matched_question_id"] and r["content_disposition"] != "MISSING":
            support_788[(r["matched_question_id"], r["examiner"])].append(r["source_id"])

    # ---------------------------------------------------------------- ready
    ready = []
    for row in load_csv("EXISTING_CONNECTION_GAPS.csv"):
        ready.append({
            "canonical_question_id": row["canonical_question_id"],
            "examiner": row["examiner"],
            "channel": "MASTER_TRACKER_PRIMARY",
            "phase1_evidence": row.get("evidence_ids", ""),
            "phase1_strength": row.get("classification", ""),
        })
    for row in load_csv("PROSE_CONNECTION_GAPS.csv"):
        ready.append({
            "canonical_question_id": row["canonical_question_id"],
            "examiner": row["examiner"],
            "channel": "PAGE_PROSE_CE_TIP",
            "phase1_evidence": "",
            "phase1_strength": row.get("strength", ""),
        })

    seen = {}
    for r in ready:
        key = (r["canonical_question_id"], r["examiner"])
        q = inv.get(r["canonical_question_id"])
        r["target_resolves_to_live_question"] = bool(q)
        r["question_text"] = q["question_text"] if q else None
        r["url"] = q["url"] if q else None
        r["corroborating_source_ids"] = support_788.get(key, [])

        if key in linked:
            r["status"] = "SUPERSEDED_ALREADY_LINKED"
        elif not q:
            r["status"] = "CONFLICTED_TARGET_DOES_NOT_RESOLVE"
        elif r["channel"] == "MASTER_TRACKER_PRIMARY":
            r["status"] = ("READY_VERIFIED_MULTI_SOURCE" if r["corroborating_source_ids"]
                           else "READY_VERIFIED")
        elif r["phase1_strength"] == "STRONG_CE_TIP_ASSERTION":
            r["status"] = ("READY_VERIFIED_MULTI_SOURCE" if r["corroborating_source_ids"]
                           else "READY_BUT_CE_TIP_ONLY")
        elif r["corroborating_source_ids"]:
            r["status"] = "READY_VERIFIED_MULTI_SOURCE"
        else:
            r["status"] = "NEEDS_REVIEW_WEAK_PROSE"

        # one relationship, many evidence records: collapse duplicate channels
        prev = seen.get(key)
        rank = {"READY_VERIFIED_MULTI_SOURCE": 4, "READY_VERIFIED": 3,
                "READY_BUT_CE_TIP_ONLY": 2, "NEEDS_REVIEW_WEAK_PROSE": 1,
                "SUPERSEDED_ALREADY_LINKED": 5, "CONFLICTED_TARGET_DOES_NOT_RESOLVE": 0}
        if prev is None or rank[r["status"]] > rank[prev["status"]]:
            if prev:
                r["channels"] = sorted(set(prev.get("channels", [prev["channel"]])
                                           + [r["channel"]]))
            else:
                r["channels"] = [r["channel"]]
            seen[key] = r
        else:
            prev["channels"] = sorted(set(prev.get("channels", [prev["channel"]])
                                          + [r["channel"]]))
    ready = sorted(seen.values(), key=lambda r: (r["status"], r["examiner"]))
    L.jdump(ready, "READY_CONNECTIONS_V2.json")
    ready_counts = Counter(r["status"] for r in ready)

    # ------------------------------------------------- inference disposition
    inf_rows = []
    for row in load_csv("INFERRED_ONLY_CONNECTIONS.csv"):
        key = (row["canonical_question_id"], row["examiner"])
        sup = support_788.get(key, [])
        if sup:
            status = "PROMOTED_BY_EVIDENCE"
        else:
            status = "STILL_INFERRED"
        inf_rows.append({
            "canonical_question_id": row["canonical_question_id"],
            "examiner": row["examiner"],
            "current_tier": row["tier"],
            "disposition": status,
            "corroborating_source_ids": ";".join(sup),
            "note": ("the external compilation reports this examiner asking this "
                     "question" if sup else
                     "no external occurrence reaches this question for this examiner; "
                     "absence of evidence is not contradiction"),
        })
    with (OUT / "INFERRED_ONLY_DISPOSITION.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(inf_rows[0]))
        w.writeheader()
        w.writerows(inf_rows)
    inf_counts = Counter(r["disposition"] for r in inf_rows)

    # ------------------------------------------------- cross-examiner families
    cross = []
    for f in fams:
        if f["examiner_count"] < 2:
            continue
        rows = [r for r in recon if r["source_family_id"] == f["family_id"]]
        cross.append({
            "family_id": f["family_id"],
            "representative_text": f["representative_text"],
            "examiners_supported": f["examiners_supported"],
            "independent_source_occurrences": f["occurrence_count"],
            "distinct_wordings": f["distinct_wordings"],
            "dispositions": dict(Counter(r["content_disposition"] for r in rows)),
            "matched_question_ids": sorted({r["matched_question_id"] for r in rows
                                            if r["matched_question_id"]}),
            "note": "recurrence across examiners; no probability is derived from it",
        })
    L.jdump(sorted(cross, key=lambda c: -c["independent_source_occurrences"]),
            "CROSS_EXAMINER_FAMILIES.json")

    # ------------------------------------------------------------- matrices
    per_ex = defaultdict(lambda: Counter())
    for r in recon:
        per_ex[r["examiner"]][r["content_disposition"]] += 1
        per_ex[r["examiner"]]["M_" + r["examiner_mapping_status"]] += 1
    fam_ex = defaultdict(set)
    for f in fams:
        for e in f["examiners_supported"]:
            fam_ex[e].add(f["family_id"])
    gap_ex = defaultdict(Counter)
    for g in gaps:
        for e in g["examiners"]:
            gap_ex[e][g["priority"]] += 1
            gap_ex[e][g["gap_kind"]] += 1
    newpairs = defaultdict(set)
    for r in recon:
        if r["examiner_mapping_status"] == "NEW_LINK":
            newpairs[r["examiner"]].add((r["matched_question_id"], r["examiner"]))

    order = ["John", "Simon", "Nair", "Paul"]
    matrix_rows = []
    for e in order:
        c = per_ex[e]
        matrix_rows.append([
            e, sum(c[d] for d in DISPS), len(fam_ex[e]),
            c["EXACT_MATCH"], c["NEAR_MATCH"], c["SAME_CORE_ASK"],
            c["PARTIAL_COVERAGE"], c["MISSING"], c["AMBIGUOUS"],
            c["M_ALREADY_LINKED"], len(newpairs[e]), c["M_CONFLICTING_LINK"],
            gap_ex[e]["P0"],
        ])
    matrix_rows.append([
        "**Total**", len(recon), len(fams),
        sum(per_ex[e]["EXACT_MATCH"] for e in order),
        sum(per_ex[e]["NEAR_MATCH"] for e in order),
        sum(per_ex[e]["SAME_CORE_ASK"] for e in order),
        sum(per_ex[e]["PARTIAL_COVERAGE"] for e in order),
        sum(per_ex[e]["MISSING"] for e in order),
        sum(per_ex[e]["AMBIGUOUS"] for e in order),
        sum(per_ex[e]["M_ALREADY_LINKED"] for e in order),
        len({(r["matched_question_id"], r["examiner"]) for r in recon
             if r["examiner_mapping_status"] == "NEW_LINK"}),
        sum(per_ex[e]["M_CONFLICTING_LINK"] for e in order),
        sum(1 for g in gaps if g["priority"] == "P0"),
    ])

    rec = json.loads((OUT / "RELATIONSHIP_RECOVERY_REPORT.json").read_text(encoding="utf-8"))
    ing = json.loads((OUT / "ALL_SURVEYORS_INGESTION_REPORT.json").read_text(encoding="utf-8"))
    summ = json.loads((OUT / "ORAL_788_RECONCILIATION_SUMMARY.json").read_text(encoding="utf-8"))

    doc = ["# Oral 788-Question Reconciliation Matrix (Phase 2)", "",
           "**Date:** 18 August 2026 · **MEO Class 1 orals: 24 August 2026**  ",
           "**Branch:** `research/oral-examiner-intelligence-v1-reconcile`  ",
           "**Baseline:** Phase 0/1 audit @ `d8ed9e6`", "",
           "Every number here is derived from the records in this folder. None is typed by hand.",
           "", "---", "", "## 1. Global reconciliation", "",
           md_table(
               ["Layer", "Count"],
               [["Raw source occurrences ingested", ing["raw_source_occurrences_parsed"]],
                ["Normalised source families", ing["normalized_source_families"]],
                ["Live Oral QB questions compared against", len(inv)],
                ["Examiner relationships recovered from the index", rec["unique_relationships_recovered"]],
                ["Source occurrences dispositioned", summ["source_occurrences_dispositioned"]],
                ["Cross-examiner families", len(cross)],
                ["Gap families (genuine + material partial)", len(gaps)],
                ["Human review queue", len(review)]]),
           "", "## 2. Content coverage of the 788", "",
           md_table(["Disposition", "Occurrences"],
                    [[d, summ["content_dispositions"].get(d, 0)] for d in DISPS]),
           "", "## 3. Examiner mapping (independent of content)", "",
           md_table(["Status", "Occurrences"],
                    [[m, summ["examiner_mapping"].get(m, 0)] for m in MAPS]),
           "",
           "Unique new examiner→question pairs proposed: **%d**. Already-linked pairs "
           "confirmed by the external source: **%d**." % (
               summ["new_links_unique_pairs"], summ["already_linked_unique_pairs"]),
           "", "## 4. Surveyor-by-surveyor matrix", "",
           md_table(["Examiner", "Raw occ.", "Families", "Exact", "Near", "Same core",
                     "Partial", "Missing", "Ambiguous", "Already linked", "New links",
                     "Conflicts", "P0 gaps"], matrix_rows),
           "", "## 5. Relationship types", "",
           md_table(["Type", "Occurrences"],
                    sorted(summ["relationship_types"].items(), key=lambda x: -x[1])),
           "", "## 6. Gap candidates", "",
           md_table(["Priority", "Genuine gap", "Material partial"],
                    [[p,
                      summ["gap_priority_by_kind"]["GENUINE_GAP"].get(p, 0),
                      summ["gap_priority_by_kind"]["MATERIAL_PARTIAL"].get(p, 0)]
                     for p in ("P0", "P1", "P2", "P3")]),
           "", "## 7. Ready connections, re-verified", "",
           md_table(["Status", "Pairs"],
                    sorted(ready_counts.items(), key=lambda x: -x[1])),
           "", "## 8. Inference-only relationships", "",
           md_table(["Disposition", "Pairs"], sorted(inf_counts.items(), key=lambda x: -x[1])),
           "",
           "`CONFLICTED` is deliberately zero: the external compilation can corroborate an "
           "inference, but its silence about a pair is absence of evidence, not contradiction.",
           "", "## 9. Recovered index defects", "",
           md_table(["Defect", "Count", "Resolution"],
                    [["Blank display rows", rec["blank_display_row_count"],
                      "question text recovered from live HTML into the relationship ledger"],
                     ["Invalid `cetip` tier literals", len(rec["invalid_tier_rows"]),
                      "intended tier `ce_tip` recorded in `repaired_tier`"],
                     ["Duplicate relationship", len(rec["duplicate_relationships"]),
                      "one relationship, two index rows, both kept as evidence"],
                     ["Display-text drift rows", len(rec["display_text_drifts"]),
                      "live text is canonical; index wording kept as a historical variant"]]),
           "", "## 10. July workbook status", "",
           "The July per-examiner sheets overlap the recovered relationships on **%d** of "
           "**%d** pairs. They are carried as `DERIVED_PRODUCT_SURFACE` and are excluded "
           "from every evidence-strength calculation in this phase. Counting them would be "
           "circular." % (rec["july_derived_sibling_check"][
               "relationships_also_present_in_july_per_examiner_sheets"],
               rec["unique_relationships_recovered"]),
           ""]
    (OUT / "ORAL_788_RECONCILIATION_MATRIX.md").write_text("\n".join(doc) + "\n",
                                                           encoding="utf-8")

    # ------------------------------------------------- per-examiner reports
    for e in order:
        rows = [r for r in recon if r["examiner"] == e]
        c = per_ex[e]
        eg = [g for g in gaps if e in g["examiners"]]
        pairs_now = sum(1 for r in rels if r["examiner"] == e)
        new = sorted({(r["matched_question_id"], r["raw_question_text"], r["source_id"])
                      for r in rows if r["examiner_mapping_status"] == "NEW_LINK"})
        d = ["# %s — 788 Reconciliation" % e, "",
             "**Source occurrences:** %d · **Relationships published today:** %d" % (
                 len(rows), pairs_now), "",
             "## Content coverage", "",
             md_table(["Disposition", "Count"], [[x, c[x]] for x in DISPS]), "",
             "## Examiner mapping", "",
             md_table(["Status", "Count"], [[m, c["M_" + m]] for m in MAPS]), "",
             "Unique new pairs proposed: **%d**." % len(newpairs[e]), "",
             "## Gap candidates", "",
             md_table(["Priority", "Families"],
                      [[p, sum(1 for g in eg if g["priority"] == p)]
                       for p in ("P0", "P1", "P2", "P3")]), "",
             "## P0 gaps", ""]
        p0 = [g for g in eg if g["priority"] == "P0"]
        if p0:
            d.append(md_table(
                ["Proposed question", "Occ.", "Examiners", "Reuse candidate"],
                [[g["proposed_canonical_question"][:90].replace("|", "/"),
                  g["occurrence_count"], "/".join(g["examiners"]),
                  g["reuse_candidate"] or "—"] for g in p0]))
        else:
            d.append("None.")
        d += ["", "## Proposed new examiner connections (first 40)", "",
              md_table(["Question", "Source wording", "Source id"],
                       [[q, t[:70].replace("|", "/"), sid] for q, t, sid in new[:40]]),
              "", "Full list: `ORAL_788_RECONCILIATION.jsonl`, "
              "`examiner_mapping_status == NEW_LINK`.", ""]
        (OUT / ("%s_RECONCILIATION.md" % e.upper())).write_text("\n".join(d) + "\n",
                                                                encoding="utf-8")

    # ------------------------------------------------------- review + P0 docs
    q = ["# Human Review Queue — Oral 788 Reconciliation", "",
         "Only cases where model judgement remains material. %d of %d source "
         "occurrences (%.1f%%)." % (len(review), len(recon), 100.0 * len(review) / len(recon)),
         "", md_table(["Reason", "Count"],
                      sorted(Counter(r["reason"] for r in review).items(),
                             key=lambda x: -x[1])), ""]
    for reason in sorted({r["reason"] for r in review}):
        q += ["## %s" % reason, "",
              md_table(["Source id", "Examiner", "Source wording", "Candidate A",
                        "cov", "Candidate B", "cov"],
                       [[r["source_id"], r["examiner"],
                         r["raw_question_text"][:60].replace("|", "/"),
                         r["candidate_a"] or "—", r["candidate_a_coverage"],
                         r["candidate_b"] or "—", r["candidate_b_coverage"] or "—"]
                        for r in review if r["reason"] == reason]), ""]
    (OUT / "HUMAN_REVIEW_QUEUE.md").write_text("\n".join(q) + "\n", encoding="utf-8")

    p0 = [g for g in gaps if g["priority"] == "P0"]
    d = ["# P0 Oral Gaps — pre-24-August production candidates", "",
         "%d families. A gap reaches P0 only when no existing MIW answer prepares the "
         "candidate **and** the ask either recurs across examiners/sittings or concerns a "
         "current rule MIW holds almost nothing on. No probability of being asked is "
         "derived anywhere in this phase." % len(p0), ""]
    for g in p0:
        d += ["### %s — %s" % (g["gap_id"], g["proposed_canonical_question"][:110]), "",
              "- **Examiner(s):** %s" % ", ".join(g["examiners"]),
              "- **Source occurrences:** %d (pages %s)" % (
                  g["occurrence_count"], ", ".join(str(p) for p in g["source_pages"])),
              "- **Source wording(s):**"]
        for w in g["source_wordings"]:
            d.append("  - %s" % w)
        d += ["- **Topic:** %s" % "; ".join(g["topics"]),
              "- **Why current coverage is insufficient:** nearest live question `%s` "
              "covers %.0f%% of the ask; best existing answer covers %.0f%%." % (
                  g["nearest_existing_question"] or "none",
                  100 * (g["nearest_coverage"] or 0), 100 * g["best_answer_coverage"]),
              "- **Reuse candidate:** %s" % (g["reuse_candidate"] or "none identified"),
              "- **Priority factors:** %s" % "; ".join(g["priority_factors"]), ""]
    (OUT / "ORAL_P0_GAPS.md").write_text("\n".join(d) + "\n", encoding="utf-8")

    print(json.dumps({
        "ready_connections": dict(ready_counts),
        "inference_disposition": dict(inf_counts),
        "cross_examiner_families": len(cross),
        "p0_gaps": len(p0),
        "human_review": len(review),
    }, indent=2))


if __name__ == "__main__":
    main()
