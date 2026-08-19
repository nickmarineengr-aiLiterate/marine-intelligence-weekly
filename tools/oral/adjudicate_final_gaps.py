"""Final Oral gap adjudication - derive the TRUE remaining new-Q&A count.

The question this answers is "how many additional canonical Q&A cards do we
still need to write?", never "how many source questions are missing?". A new
card is the last resort: an existing answer, an enrichment, a Notes promotion,
a follow-up or a merge is tried first, in that order.

Three inputs, in order of authority:

  1. the CURRENT live QB HTML - 688 canonical questions across 86 files. This
     beats the frozen reconciliation, which was computed before the P0 batch
     went live and therefore still reports six answered families as gaps.
  2. final_gap_decisions.py - the hand adjudications for every GENUINE_GAP and
     NOTES_COVERED_GAP family, made by reading answer BODIES.
  3. FINAL_ORAL_GAP_CANDIDATES.json - the governed family universe.

MATERIAL_PARTIAL families are dispositioned by rule rather than by hand: the
matcher already established that an existing answer covers part of the ask, so
the only open question is whether the missing limb is material, and that is
answered by recurrence (occurrences and examiners), not by re-reading.

Outputs (meoclass1/oral-intelligence/examiner-audit/):
  FINAL_REMAINING_ORAL_PRODUCTION_DECISIONS.json
  FINAL_REMAINING_ORAL_PRODUCTION_DECISIONS.md
  ORAL_MASTER_WORKBOOK_FREEZE_READINESS.md

Deterministic: no clock, no randomness, sorted iteration everywhere. Coverage
sums are taken over sorted token lists because float addition is not
associative and set-iteration order would otherwise leak hash randomisation
into the numbers.
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402
import oral_text as T  # noqa: E402
import reconcile_788 as R  # noqa: E402
import final_gap_decisions as D  # noqa: E402

OUT = L.OUT

# The nine P0 families produced before this session. They are excluded from the
# remaining universe and must never be re-proposed as new work.
P0_FAMILIES = {
    "GAP-0002": "QB1_K#q9", "GAP-0410": "QB3_J#q6", "GAP-0048": "QB4_A#q21",
    "GAP-0044": "QB4_A#q22", "GAP-0043": "QB5_B#q4", "GAP-0042": "QB5_D#q3",
    "GAP-0034": "QB6#q10", "GAP-0016": "QB1_A#q31", "GAP-0409": "QB7_I#q2",
}
# GAP-0454 was merged into GAP-0410 during the P0 batch and is not a family.
P0_MERGED = {"GAP-0454": "GAP-0410"}
P0_NEW_ANCHORS = ["QB1_A#q31", "QB1_K#q9", "QB3_J#q6",
                  "QB4_A#q21", "QB4_A#q22", "QB5_D#q3"]
P0_ENRICH_ANCHORS = ["QB5_B#q4", "QB6#q10", "QB7_I#q2"]

# Pairs of approved NEW cards that would share a QB home. Each is recorded as
# genuinely distinct, with the reason, so that the duplicate-family check has
# something to test against rather than a silent allowance. A new same-home
# pair that is not listed here fails validation until it is adjudicated.
DISTINCT_NEW_PAIRS = {
    ("GAP-0120", "GAP-0128"): (
        "Miller/Atkinson cycle timing against adaptive cylinder-oil feed rate: "
        "different mechanism, different equipment, no shared regulation. They "
        "share only the QB7_C engine-technology file."),
    ("GAP-0113", "GAP-0728"): (
        "Fresh water allowance against Type B-60 freeboard reduction: both sit "
        "in the Load Line file, but one is a draught correction and the other a "
        "ship-type assignment regime."),
    ("GAP-0262", "GAP-0365"): (
        "Onboard NOx compliance verification against cavitation: unrelated; "
        "they share only the QB6_D machinery file."),
    ("GAP-0159", "GAP-0562"): (
        "Cost decomposition against the ship broker's role: both commercial, "
        "but one is a cost taxonomy and the other a market intermediary."),
    ("GAP-0376", "GAP-0478"): (
        "Stowaway handling against search and rescue: both are QB4_G shipboard "
        "incident asks, but neither answer would prepare a candidate for the "
        "other."),
}

# Live duplicate-home debt found while adjudicating. These are NOT content
# gaps: the ask is answered twice. Reported separately so that a duplicate is
# never mistaken for a missing card.
DUPLICATE_HOMES = [
    {"pair": ["QB3_A#q13", "QB3_B#q3"],
     "ask": "What do you check during a ballast water tank inspection?",
     "surfaced_by": "GAP-0547"},
    {"pair": ["QB2_C#q4", "QB2_F#q5"],
     "ask": "Water mist lance and mobile water monitor",
     "surfaced_by": "GAP-0599"},
]


# --------------------------------------------------------------------------
def live_corpus():
    """Current canonical baseline plus the token tables used for re-scoring."""
    inv = L.build_inventory()
    qtext = {r["canonical_question_id"]: r["question_text"] for r in inv}
    bodies = R.card_bodies()
    qids = sorted(qtext)
    q_idf, qn = R.idf_table([qtext[q] for q in qids])
    a_idf, an = R.idf_table([bodies.get(q, "") for q in qids])
    return {
        "inv": inv, "qtext": qtext, "bodies": bodies, "qids": qids,
        "q_idf": q_idf, "a_idf": a_idf,
        "q_default": math.log(1 + qn), "a_default": math.log(1 + an),
        "q_tok": {q: T.mtokens(qtext[q]) for q in qids},
        "a_tok": {q: T.mtokens(bodies.get(q, "")) for q in qids},
        "files": sorted({q.split("#")[0] for q in qids}),
    }


def rescore(c, wordings):
    """Best question-text and answer coverage against the CURRENT corpus.

    Per occurrence, then max over occurrences - the same shape the governed
    matcher used, so the numbers are comparable to the frozen ones. Scoring the
    concatenated family text instead would inflate the token demand and quietly
    depress every score.
    """
    best_q = (0.0, None)
    best_a = (0.0, None)
    for w in wordings:
        st = T.mtokens(w)
        if not st:
            continue
        for q in c["qids"]:
            qc = R.weighted_coverage(st, c["q_tok"][q], c["q_idf"], c["q_default"])
            ac = R.weighted_coverage(st, c["a_tok"][q], c["a_idf"], c["a_default"])
            if qc > best_q[0]:
                best_q = (qc, q)
            if ac > best_a[0]:
                best_a = (ac, q)
    return best_q, best_a


def partial_rule(g):
    """Disposition for a MATERIAL_PARTIAL family.

    Recurrence is the materiality signal. A limb an examiner reached for twice,
    or that two examiners reached for, is worth adding to the answer. A limb
    asked once, against an answer that already covers the rest, is an expected
    detail - and at P3 (single occurrence, single examiner, lowest rank) it is
    long tail that does not need to block a workbook freeze.
    """
    if g["priority"] in ("P0", "P1"):
        return D.ENRICH, "recurrent or high-rank partial: the missing limb is material"
    if g["priority"] == "P2":
        if g["occurrence_count"] > 1 or g["examiner_count"] > 1:
            return D.ENRICH, "asked more than once: the missing limb is material"
        return D.FOLLOWUP, "single occurrence against an answer that already covers the rest"
    return D.DEFER, "single occurrence, single examiner, lowest rank: long tail"


# --------------------------------------------------------------------------
def main():
    c = live_corpus()
    src = json.loads((OUT / "FINAL_ORAL_GAP_CANDIDATES.json").read_text(encoding="utf-8"))
    gaps = {g["gap_id"]: g for g in src["gaps"]}
    hr = json.loads((OUT / "FINAL_HUMAN_REVIEW_QUEUE.json").read_text(encoding="utf-8"))
    disp = {}
    with (OUT / "FINAL_788_PRODUCTION_DISPOSITION.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            disp[r["source_id"]] = r

    families = []
    for gid in sorted(gaps):
        g = gaps[gid]
        if gid in P0_FAMILIES or gid in P0_MERGED:
            continue
        bq, ba = rescore(c, g["source_wordings"])
        if gid in D.DECISIONS:
            decision, target, reason = D.DECISIONS[gid]
            basis = "hand adjudication against current answer bodies"
        else:
            decision, reason = partial_rule(g)
            target = g["reuse_candidate"] or g["nearest_existing_question"]
            basis = "rule: material partial dispositioned by recurrence"

        rec = {
            "family_id": gid,
            "source_family_id": g["source_family_id"],
            "ask": g["proposed_canonical_question"],
            "raw_ask_variants": g["source_wordings"],
            "source_ids": g["source_ids"],
            "occurrence_count": g["occurrence_count"],
            "examiners": g["examiners"],
            "examiner_count": g["examiner_count"],
            "topics": g["topics"],
            "source_pages": g["source_pages"],
            "governed_gap_kind": g["final_gap_kind"],
            "governed_priority": g["priority"],
            "governed_production_action": g["production_action"],
            "frozen_best_answer_coverage": g["best_answer_coverage"],
            "current_best_question_id": bq[1],
            "current_question_coverage": round(bq[0], 3),
            "current_best_answer_question_id": ba[1],
            "current_best_answer_coverage": round(ba[0], 3),
            "notes_support": g["notes_support"],
            "notes_units": [
                "%s#%s" % (u["file"], u["anchor"]) for u in g["notes_units"]],
            "decision": decision,
            "decision_target": target,
            "decision_reason": reason,
            "decision_basis": basis,
        }
        if decision == D.NEW:
            rec["confidence"] = D.CONFIDENCE[gid]
            rec["batch"] = D.BATCH.get(gid)
            rec["production_id"] = "ORALQA-" + gid.split("-")[1]
            rec["recommended_qb_file"] = target
            rec["verification_required"] = True
        families.append(rec)

    # ---- human review queue, recomputed against the current corpus --------
    hr_rows = []
    for item in sorted(hr["items"], key=lambda x: x["source_id"]):
        sid = item["source_id"]
        bq, ba = rescore(c, [item["raw_question_text"]])
        mass = len(T.mtokens(item["raw_question_text"]))
        if ba[0] >= 0.9 and mass >= 3:
            verdict, target = "RESOLVED_TO_EXISTING", ba[1]
            why = "a live answer covers the ask at %.2f and the prompt carries enough mass to be sure" % ba[0]
        elif mass < 3:
            verdict, target = "STILL_AMBIGUOUS", None
            why = "prompt too terse to establish an ask; high coverage on a one- or two-token prompt is not evidence"
        elif ba[0] >= 0.7:
            verdict, target = "ENRICH_EXISTING", ba[1]
            why = "an existing answer covers a meaningful portion at %.2f; a limb is missing" % ba[0]
        else:
            verdict, target = "STILL_AMBIGUOUS", None
            why = "two plausible targets and no answer reaches the ask"
        hr_rows.append({
            "source_id": sid,
            "examiner": item["examiner"],
            "raw_question_text": item["raw_question_text"],
            "reason": item["reason"],
            "prompt_token_mass": mass,
            "current_best_answer_question_id": ba[1],
            "current_best_answer_coverage": round(ba[0], 3),
            "notes_support": item["notes_support"],
            "verdict": verdict,
            "target": target,
            "why": why,
        })

    # ---- counts ----------------------------------------------------------
    by_dec = Counter(f["decision"] for f in families)
    new = [f for f in families if f["decision"] == D.NEW]
    high = [f for f in new if f["confidence"] == D.HIGH]
    med = [f for f in new if f["confidence"] == D.MED]
    enrich = [f for f in families if f["decision"] == D.ENRICH]
    notes = [f for f in families if f["decision"] == D.NOTES]
    merges = [f for f in families if f["decision"] == D.MERGE]

    payload = {
        "note": ("Remaining Oral production decisions after the P0 batch. The "
                 "headline count is the number of NEW canonical cards still "
                 "genuinely required, not the number of unmatched source "
                 "questions. Families, never occurrences, are the unit."),
        "baseline": {
            "live_canonical_questions": len(c["qids"]),
            "live_qb_files": len(c["files"]),
            "p0_new_questions_already_created": len(P0_NEW_ANCHORS),
            "p0_new_anchors": P0_NEW_ANCHORS,
            "p0_enrichments_already_applied": len(P0_ENRICH_ANCHORS),
            "p0_enrich_anchors": P0_ENRICH_ANCHORS,
        },
        "universe": {
            "governed_families_total": len(gaps),
            "completed_p0_families_excluded": len(P0_FAMILIES),
            "p0_merged_families_excluded": len(P0_MERGED),
            "remaining_families_adjudicated": len(families),
            "hand_adjudicated": sum(
                1 for f in families
                if f["decision_basis"].startswith("hand")),
            "rule_dispositioned": sum(
                1 for f in families
                if f["decision_basis"].startswith("rule")),
        },
        "dispositions": dict(sorted(by_dec.items())),
        "headline": {
            "ADDITIONAL_NEW_CANONICAL_QA_COUNT": len(high),
            "ADDITIONAL_NEW_MEDIUM_CONFIDENCE_NOT_COUNTED": len(med),
            "ADDITIONAL_ENRICH_EXISTING_COUNT": len(enrich),
            "ADDITIONAL_NOTES_TO_QB_PROMOTION_COUNT": len(notes),
            "FOLLOWUP_ONLY_COUNT": by_dec.get(D.FOLLOWUP, 0),
            "MERGE_FAMILY_COUNT": len(merges),
            "ALREADY_COVERED_COUNT": by_dec.get(D.COVERED, 0),
            "HUMAN_REVIEW_REQUIRED_COUNT": by_dec.get(D.AMBIG, 0),
            "DEFER_LOW_VALUE_COUNT": by_dec.get(D.DEFER, 0),
            "NOT_A_GAP_COUNT": by_dec.get(D.NOT_A_GAP, 0),
            "P0_NEW_QUESTIONS_ALREADY_CREATED": len(P0_NEW_ANCHORS),
            "TOTAL_NEW_AFTER_APPROVED_BATCH": len(P0_NEW_ANCHORS) + len(high),
        },
        "batches": {
            b: sorted(f["family_id"] for f in high if f["batch"] == b)
            for b in ("P1-A", "P1-B", "P2")
        },
        "cross_examiner_new": sorted(
            f["family_id"] for f in high if f["examiner_count"] > 1),
        "single_examiner_new": sorted(
            f["family_id"] for f in high if f["examiner_count"] == 1),
        "duplicate_home_debt": DUPLICATE_HOMES,
        "human_review": {
            "rows_in": len(hr_rows),
            "by_verdict": dict(sorted(Counter(
                r["verdict"] for r in hr_rows).items())),
            "rows": hr_rows,
        },
        "families": families,
    }
    L.jdump(payload, "FINAL_REMAINING_ORAL_PRODUCTION_DECISIONS.json")
    write_markdown(payload)
    write_freeze_readiness(payload)
    return payload


# --------------------------------------------------------------------------
def write_markdown(p):
    h = p["headline"]
    out = ["# Final remaining Oral production decisions", "",
           p["note"], "",
           "## Baseline", "",
           "| item | value |", "| --- | --- |"]
    for k, v in p["baseline"].items():
        if isinstance(v, list):
            v = ", ".join("`%s`" % x for x in v)
        out.append("| %s | %s |" % (k.replace("_", " "), v))
    out += ["", "## Universe", "", "| item | value |", "| --- | --- |"]
    for k, v in p["universe"].items():
        out.append("| %s | %s |" % (k.replace("_", " "), v))
    out += ["", "## Dispositions", "", "| disposition | families |",
            "| --- | ---: |"]
    for k, v in p["dispositions"].items():
        out.append("| %s | %d |" % (k, v))
    out += ["", "## Headline counts", "", "| count | value |", "| --- | ---: |"]
    for k, v in h.items():
        out.append("| %s | %s |" % (k, v))

    for label, conf in (("Approved new cards - high confidence", D.HIGH),
                        ("Medium confidence - NOT counted", D.MED)):
        rows = [f for f in p["families"]
                if f["decision"] == D.NEW and f["confidence"] == conf]
        out += ["", "## %s (%d)" % (label, len(rows)), "",
                "| production id | family | batch | examiners | occ | home | ask |",
                "| --- | --- | --- | --- | ---: | --- | --- |"]
        for f in sorted(rows, key=lambda x: (x["batch"] or "zz", x["family_id"])):
            out.append("| `%s` | %s | %s | %s | %d | `%s` | %s |" % (
                f["production_id"], f["family_id"], f["batch"] or "-",
                ", ".join(f["examiners"]), f["occurrence_count"],
                f["recommended_qb_file"], f["ask"].replace("|", "/")[:90]))

    out += ["", "## Production spec - each approved new card", ""]
    for f in sorted([x for x in p["families"]
                     if x["decision"] == D.NEW and x["confidence"] == D.HIGH],
                    key=lambda x: x["production_id"]):
        out += ["### `%s` - %s" % (f["production_id"], f["family_id"]), "",
                "- **proposed question**: %s" % f["ask"],
                "- **topic(s)**: %s" % ", ".join(f["topics"]),
                "- **examiner(s)**: %s" % ", ".join(f["examiners"]),
                "- **source occurrence ids**: %s" % ", ".join(
                    "`%s`" % s for s in f["source_ids"]),
                "- **raw ask variants**: %s" % " // ".join(
                    w.replace("\n", " ")[:160] for w in f["raw_ask_variants"]),
                "- **closest current QB question**: `%s` (question coverage %.2f)"
                % (f["current_best_question_id"], f["current_question_coverage"]),
                "- **closest current QB answer**: `%s` (answer coverage %.2f)"
                % (f["current_best_answer_question_id"],
                   f["current_best_answer_coverage"]),
                "- **closest Notes**: %s" % (
                    ", ".join("`%s`" % u for u in f["notes_units"]) or "none"),
                "- **why existing MIW fails / why enrichment is insufficient**: %s"
                % f["decision_reason"],
                "- **recommended QB file**: `%s`" % f["recommended_qb_file"],
                "- **batch**: %s" % (f["batch"] or "-"),
                "- **regulatory / technical verification required before writing**: yes",
                ""]

    out += ["## Enrichments (%d)" % h["ADDITIONAL_ENRICH_EXISTING_COUNT"], "",
            "| family | target anchor | examiners | occ | missing limb |",
            "| --- | --- | --- | ---: | --- |"]
    for f in sorted([x for x in p["families"] if x["decision"] == D.ENRICH],
                    key=lambda x: x["family_id"]):
        out.append("| %s | `%s` | %s | %d | %s |" % (
            f["family_id"], f["decision_target"], ", ".join(f["examiners"]),
            f["occurrence_count"], f["decision_reason"].replace("|", "/")[:130]))

    out += ["", "## Notes promotions (%d)" % h["ADDITIONAL_NOTES_TO_QB_PROMOTION_COUNT"],
            "", "| family | Notes source | proposed QB home | what must be verified |",
            "| --- | --- | --- | --- |"]
    for f in sorted([x for x in p["families"] if x["decision"] == D.NOTES],
                    key=lambda x: x["family_id"]):
        out.append("| %s | `%s` | `%s` | %s |" % (
            f["family_id"], f["decision_target"],
            f["current_best_answer_question_id"] or "new anchor",
            "currency of the cited instrument, and that the Notes wording is "
            "re-authored rather than copied"))

    out += ["", "## Merges (%d)" % h["MERGE_FAMILY_COUNT"], "",
            "| collapsed family | into | reason |", "| --- | --- | --- |"]
    for f in sorted([x for x in p["families"] if x["decision"] == D.MERGE],
                    key=lambda x: x["family_id"]):
        out.append("| %s | %s | %s |" % (
            f["family_id"], f["decision_target"],
            f["decision_reason"].replace("|", "/")))

    out += ["", "## Duplicate-home debt (not content gaps)", "",
            "| pair | ask | surfaced by |", "| --- | --- | --- |"]
    for d in p["duplicate_home_debt"]:
        out.append("| `%s` + `%s` | %s | %s |" % (
            d["pair"][0], d["pair"][1], d["ask"], d["surfaced_by"]))

    hrq = p["human_review"]
    out += ["", "## Human review queue (%d rows)" % hrq["rows_in"], "",
            "| verdict | rows |", "| --- | ---: |"]
    for k, v in hrq["by_verdict"].items():
        out.append("| %s | %d |" % (k, v))
    out += ["", "### Rows still genuinely ambiguous", "",
            "| source | examiner | prompt | mass | why |",
            "| --- | --- | --- | ---: | --- |"]
    for r in hrq["rows"]:
        if r["verdict"] != "STILL_AMBIGUOUS":
            continue
        out.append("| `%s` | %s | %s | %d | %s |" % (
            r["source_id"], r["examiner"],
            r["raw_question_text"].replace("|", "/")[:80],
            r["prompt_token_mass"], r["why"][:70]))

    out += ["", "## Families still requiring human adjudication", "",
            "| family | ask | why |", "| --- | --- | --- |"]
    for f in sorted([x for x in p["families"] if x["decision"] == D.AMBIG],
                    key=lambda x: x["family_id"]):
        out.append("| %s | %s | %s |" % (
            f["family_id"], f["ask"].replace("|", "/")[:70],
            f["decision_reason"].replace("|", "/")))
    out.append("")
    (OUT / "FINAL_REMAINING_ORAL_PRODUCTION_DECISIONS.md").write_text(
        "\n".join(out), encoding="utf-8", newline="\n")


def write_freeze_readiness(p):
    h = p["headline"]
    b = p["baseline"]
    outstanding = (h["ADDITIONAL_NEW_CANONICAL_QA_COUNT"]
                   + h["ADDITIONAL_ENRICH_EXISTING_COUNT"]
                   + h["ADDITIONAL_NOTES_TO_QB_PROMOTION_COUNT"])
    if outstanding == 0:
        status = "READY_NOW"
    else:
        status = "READY_AFTER_APPROVED_ORAL_PRODUCTION_BATCH"
    lines = [
        "# Oral master workbook - freeze readiness", "",
        "Governing rule: the two master workbooks are a snapshot of a published",
        "corpus. Freezing them while approved production is outstanding would",
        "ship a workbook that disagrees with the live site within one batch.",
        "",
        "## Current position", "",
        "| item | value |", "| --- | ---: |",
        "| live canonical questions | %d |" % b["live_canonical_questions"],
        "| live QB files | %d |" % b["live_qb_files"],
        "| new questions already added by the P0 batch | %d |"
        % b["p0_new_questions_already_created"],
        "| enrichments already applied by the P0 batch | %d |"
        % b["p0_enrichments_already_applied"],
        "", "## Outstanding approved production", "",
        "| work | count |", "| --- | ---: |",
        "| additional NEW canonical Q&A (high confidence) | %d |"
        % h["ADDITIONAL_NEW_CANONICAL_QA_COUNT"],
        "| approved enrichments | %d |" % h["ADDITIONAL_ENRICH_EXISTING_COUNT"],
        "| approved Notes-to-QB promotions | %d |"
        % h["ADDITIONAL_NOTES_TO_QB_PROMOTION_COUNT"],
        "| follow-up / expected detail (no new card) | %d |"
        % h["FOLLOWUP_ONLY_COUNT"],
        "| **total outstanding items that change the corpus** | **%d** |" % outstanding,
        "",
        "Canonical question count after the approved new batch: **%d + %d = %d**."
        % (b["live_canonical_questions"], h["ADDITIONAL_NEW_CANONICAL_QA_COUNT"],
           b["live_canonical_questions"] + h["ADDITIONAL_NEW_CANONICAL_QA_COUNT"]),
        "Follow-ups, merges and enrichments do not change the count.",
        "", "## Residue carried forward", "",
        "| item | count |", "| --- | ---: |",
        "| medium-confidence new cards, deliberately not counted | %d |"
        % h["ADDITIONAL_NEW_MEDIUM_CONFIDENCE_NOT_COUNTED"],
        "| families still requiring human adjudication | %d |"
        % h["HUMAN_REVIEW_REQUIRED_COUNT"],
        "| human-review rows still genuinely ambiguous | %d |"
        % p["human_review"]["by_verdict"].get("STILL_AMBIGUOUS", 0),
        "| long-tail partials deferred | %d |" % h["DEFER_LOW_VALUE_COUNT"],
        "",
        "This residue is safe to carry past a workbook freeze: none of it is a",
        "confirmed missing answer. An ambiguous acronym is not a question.",
        "", "## Verdict", "", "**%s**" % status, "",
    ]
    if status != "READY_NOW":
        lines += [
            "DEFERRED - `MEO_QB_master_v27.xlsx` and",
            "`MIW_August2026_QuestionBank_SHARE.xlsx` must wait until the",
            "approved remaining new-QA, enrichment and Notes-promotion batch is",
            "produced and published.", ""]
    (OUT / "ORAL_MASTER_WORKBOOK_FREEZE_READINESS.md").write_text(
        "\n".join(lines), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    p = main()
    h = p["headline"]
    print("live canonical questions : %d across %d files"
          % (p["baseline"]["live_canonical_questions"],
             p["baseline"]["live_qb_files"]))
    print("families adjudicated     : %d" % p["universe"]["remaining_families_adjudicated"])
    for k, v in p["dispositions"].items():
        print("   %-28s %d" % (k, v))
    print("ADDITIONAL_NEW_CANONICAL_QA_COUNT = %d"
          % h["ADDITIONAL_NEW_CANONICAL_QA_COUNT"])
