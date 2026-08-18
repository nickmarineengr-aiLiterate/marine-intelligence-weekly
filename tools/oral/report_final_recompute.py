"""Phase 2A-iii final recompute — analysis and human-readable companions.

Reads only committed generated datasets and re-derives every number it prints.
Nothing here computes a disposition; if a figure in the handoff disagrees with
a figure here, the dataset is the authority and this script is wrong.

  PYTHONIOENCODING=utf-8 python tools/oral/report_final_recompute.py

Portability: repo-relative, no drive letters, no timestamps in semantic output.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

OUT = L.OUT

CANON_ORDER = ("EXACT_MATCH", "NEAR_MATCH", "SAME_CORE_ASK",
               "PARTIAL_COVERAGE", "MISSING", "AMBIGUOUS")
NOTES_ORDER = ("NOTES_COMPLETE_SUPPORT", "NOTES_STRONG_SUPPORT",
               "NOTES_PARTIAL_SUPPORT", "NOTES_TOPIC_SUPPORT",
               "NO_NOTES_SUPPORT")


def jl(n):
    return [json.loads(x) for x in (OUT / n).open(encoding="utf-8") if x.strip()]


def js(n):
    return json.loads((OUT / n).read_text(encoding="utf-8"))


def md(lines, name):
    (OUT / name).write_text("\n".join(lines) + "\n", encoding="utf-8",
                            newline="\n")


def count(rows, key):
    t = {}
    for r in rows:
        t[r[key]] = t.get(r[key], 0) + 1
    return t


def table(head, rows):
    out = ["| " + " | ".join(head) + " |",
           "|" + "|".join(["---"] * len(head)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return out


def main():
    final = jl("FINAL_788_PRODUCTION_DISPOSITION.jsonl")
    mv = js("RECONCILIATION_MOVEMENT_REPORT.json")
    rel = js("RELEASE_A_CONNECTIONS.json")
    exc = js("RELEASE_A_EXCLUSIONS.json")["excluded"]
    gaps = js("FINAL_ORAL_GAP_CANDIDATES.json")
    p0 = js("FINAL_P0_PRODUCTION_BATCH.json")
    hrq = js("FINAL_HUMAN_REVIEW_QUEUE.json")
    rt = js("FINAL_RETIERING_PROPOSAL.json")
    dt = js("DISPLAY_TEXT_CORRECTION_CANDIDATES.json")
    fams = js("ALL_SURVEYORS_SOURCE_FAMILIES.json")
    relns = jl("CURRENT_EXAMINER_RELATIONSHIPS.jsonl")
    nev = jl("ORAL_NOTES_EXAMINER_EVIDENCE.jsonl")
    rev = js("ORAL_NOTES_REVERSE_CONNECTIONS.json")["rows"]

    disp = count(final, "content_disposition")
    notes = count(final, "notes_support")
    prod = count(final, "production_action")
    mapping = count(final, "examiner_mapping_status")
    byex = count(final, "examiner")

    # cross-tab canonical x notes
    cross = {}
    for r in final:
        cross.setdefault(r["content_disposition"], {})
        k = r["notes_support"]
        cross[r["content_disposition"]][k] = \
            cross[r["content_disposition"]].get(k, 0) + 1

    # unique examiner-question pairs across the 788
    pairs = {(r["examiner"], r["matched_question_id"]) for r in final
             if r["matched_question_id"]}

    # family analysis
    fam_gap = {}
    for g in gaps["gaps"]:
        fam_gap[g["source_family_id"]] = g["final_gap_kind"]

    per_examiner = {}
    for ex in sorted(byex):
        rows = [r for r in final if r["examiner"] == ex]
        rel_pairs = [c for c in rel["connections"] if c["examiner"] == ex]
        per_examiner[ex] = {
            "raw_occurrences": len(rows),
            "dispositions": {k: count(rows, "content_disposition").get(k, 0)
                             for k in CANON_ORDER},
            "mapped_occurrences": sum(1 for r in rows
                                      if r["matched_question_id"]),
            "unique_pairs": len({(r["examiner"], r["matched_question_id"])
                                 for r in rows if r["matched_question_id"]}),
            "release_a_pairs": len(rel_pairs),
            "release_a_tiers": count(rel_pairs, "strongest_evidence_tier"),
            "gap_or_ambiguous": sum(1 for r in rows
                                    if r["content_disposition"] in
                                    ("MISSING", "AMBIGUOUS")),
            "p0_items": sorted(i["production_id"] for i in p0["items"]
                               if ex in i["examiners"]),
        }

    # examiners outside the 788 must survive the recompute
    idx_ex = sorted({r["examiner"] for r in relns})
    src_ex = sorted(byex)
    preserved = {}
    for ex in idx_ex:
        preserved[ex] = {
            "in_788_source": ex in src_ex,
            "relationships_retained": sum(1 for r in relns
                                          if r["examiner"] == ex),
            "note_evidence_records": sum(1 for e in nev if e["examiner"] == ex),
        }

    note_expl = {
        "unique_note_evidence_records": len(nev),
        "unique_examiner_note_unit_relations": len(
            {(e["examiner"], e["note_unit_id"]) for e in nev}),
        "reverse_classes": count(rev, "reverse_class"),
        "new_explicit_connections": sum(
            1 for r in rev
            if r["reverse_class"] == "NOTE_CREATES_NEW_EXPLICIT_CONNECTION"),
        "new_explicit_with_resolvable_target": sum(
            1 for r in rev
            if r["reverse_class"] == "NOTE_CREATES_NEW_EXPLICIT_CONNECTION"
            and r.get("canonical_question_id")),
    }

    summary = {
        "note": ("Every figure re-derived from the committed datasets. The "
                 "datasets are the authority; this file is a reading of them."),
        "source_occurrences": len(final),
        "per_examiner_source": byex,
        "canonical_qb_questions": len(L.build_inventory()),
        "note_units": len(jl("ORAL_NOTES_UNITS.jsonl")),
        "content_dispositions": {k: disp.get(k, 0) for k in CANON_ORDER},
        "content_disposition_sum": sum(disp.values()),
        "notes_support": {k: notes.get(k, 0) for k in NOTES_ORDER},
        "production_actions": dict(sorted(prod.items())),
        "examiner_mapping": dict(sorted(mapping.items())),
        "unique_examiner_question_pairs": len(pairs),
        "canonical_x_notes": {k: dict(sorted(v.items()))
                              for k, v in sorted(cross.items())},
        "source_families": {
            "total": len(fams),
            "cross_examiner": sum(1 for f in fams if f["examiner_count"] > 1),
            "same_examiner_repeated": sum(
                1 for f in fams
                if f["examiner_count"] == 1 and f["occurrence_count"] > 1),
            "singleton": sum(1 for f in fams if f["occurrence_count"] == 1),
            "gap_families": sum(1 for k in fam_gap.values()
                                if k in ("GENUINE_GAP", "NOTES_COVERED_GAP")),
            "material_partial_families": sum(1 for k in fam_gap.values()
                                             if k == "MATERIAL_PARTIAL"),
        },
        "movement": {
            "disposition_changed": mv["disposition_changed"],
            "target_changed_only": mv["target_changed_only"],
            "unchanged": mv["unchanged"],
            "reasons": mv["reason_breakdown"],
            "transitions": mv["transitions"],
        },
        "release_a": {
            "unique_pairs": rel["unique_pairs"],
            "evidence_composition": rel["evidence_composition"],
            "per_examiner": rel["per_examiner"],
            "excluded": len(exc),
            "excluded_reasons": rel["excluded_reasons"],
        },
        "gaps": {
            "families": gaps["families"],
            "kinds": gaps["final_gap_kinds"],
            "verdict_changed_by_notes": gaps["verdict_changed_by_notes"],
        },
        "p0": {
            "count": p0["p0_count"],
            "by_action": p0["by_production_action"],
            "demoted_or_referred": p0["demoted_or_referred"],
            "merged": p0["merged_families"],
        },
        "human_review": {"total": hrq["total"], "by_reason": hrq["by_reason"]},
        "retiering_proposals": rt["proposed_changes"],
        "display_text_candidates": dt["count"],
        "note_explicit_impact": note_expl,
        "per_examiner_detail": per_examiner,
        "examiners_preserved": preserved,
    }
    L.jdump(summary, "PHASE2A_III_FINAL_RECOMPUTE_SUMMARY.json")

    # ---------------------------------------------------------- markdown
    m = ["# Release A — candidate connection set", "",
         "Connection-only publication. Nothing here is published by this "
         "session; this is the set the Laptop is asked to authorise.", "",
         "**%d unique examiner-question relationships.**" % rel["unique_pairs"],
         ""]
    m += table(["Strongest evidence tier", "Pairs"],
               sorted(rel["evidence_composition"].items()))
    m += ["", "## Per examiner", ""]
    m += table(["Examiner", "Release-A pairs"],
               sorted(rel["per_examiner"].items()))
    m += ["", "## Why pairs were excluded", "",
          "Padding this set would be the one failure the project exists to "
          "prevent, so every rejected pair is recorded with its reason rather "
          "than dropped.", ""]
    m += table(["Reason", "Pairs"], list(rel["excluded_reasons"].items()))
    m += ["", "## Connections", ""]
    m += table(["Relation", "Examiner", "Question", "Tier", "Text"],
               [[c["relation_id"], c["examiner"], c["canonical_question_id"],
                 c["strongest_evidence_tier"],
                 (c["candidate_safe_question_text"] or "")[:70]]
                for c in rel["connections"]])
    md(m, "RELEASE_A_CONNECTIONS.md")

    m = ["# Final P0 production batch", "",
         "The smallest set a candidate still cannot answer from the existing "
         "QB answer plus the relevant Oral Notes. Every item carries exactly "
         "one production action.", "",
         "**%d items.**" % p0["p0_count"], ""]
    m += table(["Action", "Items"],
               [[k, ", ".join(v)] for k, v in
                sorted(p0["by_production_action"].items())])
    m += ["", "## Items", ""]
    for i in p0["items"]:
        m += ["### %s — %s" % (i["production_id"], i["production_action"]), "",
              "- **Proposed canonical question:** %s"
              % i["proposed_canonical_question"],
              "- **Examiner(s):** %s (%d occurrence(s))"
              % (", ".join(i["examiners"]), i["occurrence_count"]),
              "- **Source occurrences:** %s"
              % ", ".join(i["source_occurrence_ids"]),
              "- **Closest existing QB:** %s (coverage %.2f, best answer "
              "%.2f)" % (i["current_closest_qb"] or "none",
                         i["canonical_coverage"] or 0.0,
                         i["best_answer_coverage"] or 0.0),
              "- **Notes support:** %s" % i["notes_support"],
              "- **Reuse:** %s" % (", ".join(
                  "%s#%s" % (u["file"], u["anchor"])
                  for u in i["recommended_miw_sources_to_reuse"]) or "none"),
              "- **Adjudicated:** %s" % ("yes" if i["adjudicated"] else "no"),
              "- **Raw source wording:** %s"
              % " / ".join(w[:120] for w in i["raw_source_wordings"]), ""]
    if p0["adjudications_applied"]:
        m += ["## Adjudications applied", ""]
        for a in p0["adjudications_applied"]:
            m += ["- **%s → %s** — %s" % (a["gap_id"], a["decision"],
                                          a["reason"]), ""]
    md(m, "FINAL_P0_PRODUCTION_BATCH.md")

    m = ["# Movement from the Phase-2 baseline", "",
         "Baseline `de6d3f2`. A row that keeps its disposition but changes "
         "target has still moved and is counted separately.", "",
         "- disposition changed: **%d**" % mv["disposition_changed"],
         "- target changed only: **%d**" % mv["target_changed_only"],
         "- unchanged: **%d**" % mv["unchanged"], "",
         "## Reasons", ""]
    m += table(["Reason", "Rows"], sorted(mv["reason_breakdown"].items()))
    m += ["", "## Transitions", ""]
    m += table(["From → to", "Rows"], list(mv["transitions"].items()))
    md(m, "RECONCILIATION_MOVEMENT_REPORT.md")

    m = ["# Display-text correction candidates", "",
         "Candidate-facing question text carrying internal production "
         "vocabulary. **No live file is modified by this session.** The "
         "examiner-index V2 generator must reject these shapes at build time.",
         "", "**%d candidates**, %d naming an examiner, %d needing a human "
         "rewrite." % (dt["count"], dt["carrying_examiner_name"],
                       dt["requiring_human_rewrite"]), ""]
    m += table(["Question", "Current text", "Proposed", "Examiner metadata"],
               [[r["canonical_question_id"], r["current_text"][:60],
                 (r["proposed_candidate_text"] or "*needs authoring*")[:60],
                 r["examiner_metadata_to_separate"] or "—"]
                for r in dt["rows"]])
    md(m, "DISPLAY_TEXT_CORRECTION_CANDIDATES.md")

    print("source occurrences        %d %s" % (len(final), byex))
    print("canonical QB              %d" % summary["canonical_qb_questions"])
    print("note units                %d" % summary["note_units"])
    print("dispositions              %s" % summary["content_dispositions"])
    print("  sum                     %d" % summary["content_disposition_sum"])
    print("families                  %s" % summary["source_families"])
    print("unique examiner-q pairs   %d" % len(pairs))
    print("release A                 %d %s"
          % (rel["unique_pairs"], rel["evidence_composition"]))
    print("P0                        %d" % p0["p0_count"])
    print("human review              %d" % hrq["total"])
    print("canonical x notes MISSING %s" % summary["canonical_x_notes"]
          .get("MISSING"))
    print("canonical x notes PARTIAL %s" % summary["canonical_x_notes"]
          .get("PARTIAL_COVERAGE"))
    print("note explicit             %s" % note_expl)
    return 0


if __name__ == "__main__":
    sys.exit(main())
