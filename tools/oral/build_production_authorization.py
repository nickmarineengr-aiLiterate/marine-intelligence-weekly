"""Build the laptop-authorised final Oral production inventory.

The adjudicated dataset counts SOURCE FAMILIES. Production does not consume
families, it consumes EDITS: five source families wanting the same missing
paragraph in one answer is one edit, not five. This generator applies the
laptop review decisions and then collapses families into PRODUCTION ACTIONS, so
the number reported is the number of things somebody has to write.

Two structural facts the adjudicated dataset could not express are added here:

  1. A Notes promotion has a KIND. The adjudicated `decision_target` held the
     Notes SOURCE anchor, never a QB destination, so a promotion that creates a
     brand-new card was invisible to the projected canonical count.
  2. An enrichment and a follow-up landing on the same anchor are two actions
     but one file visit, so both are reported.

Outputs (meoclass1/oral-intelligence/examiner-audit/):
  FINAL_ORAL_PRODUCTION_AUTHORIZATION.json
  FINAL_ORAL_PRODUCTION_AUTHORIZATION.md

Deterministic: no clock, no randomness, sorted iteration everywhere.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import production_authorization_decisions as PD  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "meoclass1" / "oral-intelligence" / "examiner-audit"
SRC = AUDIT / "FINAL_REMAINING_ORAL_PRODUCTION_DECISIONS.json"
OUT_JSON = AUDIT / "FINAL_ORAL_PRODUCTION_AUTHORIZATION.json"
OUT_MD = AUDIT / "FINAL_ORAL_PRODUCTION_AUTHORIZATION.md"

QCARD = re.compile(
    r'<div[^>]*(?:class="[^"]*\bq-card\b[^"]*"[^>]*id="(q\d+)"'
    r'|id="(q\d+)"[^>]*class="[^"]*\bq-card\b[^"]*")')


def live_anchors():
    """Every canonical file#anchor on disk. Identity, never position."""
    out = set()
    for p in sorted((ROOT / "meoclass1").glob("QB*.html")):
        if "heat" in p.name.lower():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in QCARD.finditer(text):
            out.add("%s#%s" % (p.stem, m.group(1) or m.group(2)))
    return out


def applied_decision(fam):
    """The laptop disposition for a family, and whether the review moved it."""
    fid = fam["family_id"]
    if fid in PD.OVERRIDES:
        dec, tgt, why = PD.OVERRIDES[fid]
        return dec, tgt, "LAPTOP_CHANGED", why
    return (fam["decision"], fam["decision_target"], "LAPTOP_CONFIRMED",
            fam["decision_reason"])


def tech_scope(fid):
    return sorted(k for k, v in PD.TECH_SCOPE.items() if fid in v)


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    fams = {f["family_id"]: f for f in data["families"]}
    live = live_anchors()

    rows = []
    for fid in sorted(fams):
        fam = fams[fid]
        dec, tgt, status, why = applied_decision(fam)
        rows.append({
            "family_id": fid,
            "ask": fam["ask"],
            "examiner_ids": fam["examiners"],
            "source_occurrence_ids": fam["source_ids"],
            "occurrence_count": fam["occurrence_count"],
            "adjudicated_decision": fam["decision"],
            "laptop_decision": dec,
            "laptop_review_status": status,
            "laptop_review_reason": why,
            "target": tgt,
            "priority": None,
            "confidence": "HIGH" if dec == "NEW_CANONICAL_QA" else "N/A",
            "technical_verification_scope": tech_scope(fid),
            "production_action_id": None,
            "reason_correction": PD.REASON_CORRECTIONS.get(fid),
        })
    by_id = {r["family_id"]: r for r in rows}

    # ---- priorities: inherit the adjudicated batches, place the promotion ----
    batches = {k: list(v) for k, v in data["batches"].items()}
    for fid, (dec, _t, _w) in PD.OVERRIDES.items():
        if dec == "NEW_CANONICAL_QA" and not any(fid in v for v in batches.values()):
            batches.setdefault("P2", []).append(fid)
    for k in batches:
        batches[k] = sorted(batches[k])
    for k, v in batches.items():
        for fid in v:
            if fid in by_id:
                by_id[fid]["priority"] = k

    # ---- production actions: families collapse into edits ----
    actions = []

    def add(kind, key, members, target, note):
        actions.append({"kind": kind, "key": key, "family_ids": sorted(members),
                        "target": target, "note": note})

    new_gap = sorted(r["family_id"] for r in rows
                     if r["laptop_decision"] == "NEW_CANONICAL_QA")
    for fid in new_gap:
        add("NEW_CARD_FROM_GAP", fid, [fid], None,
            "brand-new canonical card authored from examiner source evidence")

    promo = sorted(r["family_id"] for r in rows
                   if r["laptop_decision"] == "NOTES_TO_QB_PROMOTION")
    for fid in promo:
        kind, note = PD.PROMOTION_KIND.get(fid, ("UNCLASSIFIED", ""))
        add("NEW_CARD_FROM_NOTES" if kind == "NEW_CARD"
            else "EXISTING_CARD_NOTES_PROMOTION", fid, [fid],
            by_id[fid]["target"], note)

    enrich = defaultdict(list)
    for r in rows:
        if r["laptop_decision"] == "ENRICH_EXISTING_QB":
            enrich[r["target"]].append(r["family_id"])
    for tgt in sorted(enrich):
        add("ENRICH_EDIT", tgt, enrich[tgt], tgt,
            "one answer edit satisfying %d source famil%s"
            % (len(enrich[tgt]), "y" if len(enrich[tgt]) == 1 else "ies"))

    follow = defaultdict(list)
    for r in rows:
        if r["laptop_decision"] == "FOLLOWUP_ONLY":
            follow[r["target"]].append(r["family_id"])
    for tgt in sorted(follow):
        add("FOLLOWUP_INSERTION", tgt, follow[tgt], tgt,
            "follow-up group inserted on one parent card")

    # stable, sortable ids
    pref = {"NEW_CARD_FROM_GAP": "NEW", "NEW_CARD_FROM_NOTES": "PROMNEW",
            "EXISTING_CARD_NOTES_PROMOTION": "PROMENR",
            "ENRICH_EDIT": "ENR", "FOLLOWUP_INSERTION": "FUP"}
    seq = Counter()
    for a in sorted(actions, key=lambda x: (x["kind"], x["key"])):
        seq[a["kind"]] += 1
        a["production_action_id"] = "%s-%03d" % (pref[a["kind"]], seq[a["kind"]])
        for fid in a["family_ids"]:
            by_id[fid]["production_action_id"] = a["production_action_id"]
    actions.sort(key=lambda x: x["production_action_id"])

    counts = Counter(r["laptop_decision"] for r in rows)
    kinds = Counter(a["kind"] for a in actions)
    baseline = data["baseline"]["live_canonical_questions"]
    a_new = kinds["NEW_CARD_FROM_GAP"]
    b_new = kinds["NEW_CARD_FROM_NOTES"]

    visits = len({a["target"] for a in actions
                  if a["kind"] in ("ENRICH_EDIT", "FOLLOWUP_INSERTION")})

    payload = {
        "note": ("Laptop-authorised final Oral production inventory. Counts are "
                 "PRODUCTION ACTIONS, not source families: the unit of work is "
                 "an edit somebody performs, and several families routinely "
                 "share one edit."),
        "baseline": {
            "live_canonical_questions": baseline,
            "live_qb_files": data["baseline"]["live_qb_files"],
            "independently_reproduced": baseline == len(live),
            "live_anchor_count": len(live),
        },
        "laptop_dispositions": dict(sorted(counts.items())),
        "adjudicated_dispositions": data["dispositions"],
        "changed_by_laptop": sorted(PD.OVERRIDES),
        "reason_corrections": sorted(PD.REASON_CORRECTIONS),
        "colocation_advisories": [
            {"pair": [a, b], "why": w} for a, b, w in PD.COLOCATION],
        "authorised": {
            "AUTHORISED_NEW_CANONICAL_QA": a_new,
            "AUTHORISED_NEW_CARD_NOTES_PROMOTIONS": b_new,
            "AUTHORISED_EXISTING_CARD_NOTES_PROMOTIONS":
                kinds["EXISTING_CARD_NOTES_PROMOTION"],
            "AUTHORISED_EXISTING_QB_ENRICHMENT_ACTIONS": kinds["ENRICH_EDIT"],
            "AUTHORISED_FOLLOWUP_INSERTION_ACTIONS": kinds["FOLLOWUP_INSERTION"],
            "ENRICHMENT_SOURCE_FAMILIES": counts["ENRICH_EXISTING_QB"],
            "FOLLOWUP_SOURCE_FAMILIES": counts["FOLLOWUP_ONLY"],
            "UNIQUE_EXISTING_CARD_VISITS": visits,
            "MERGED_NO_WORK": counts["MERGE_WITH_EXISTING_FAMILY"],
            "ALREADY_COVERED": counts["ALREADY_COVERED"],
            "DEFERRED": counts["DEFER_LOW_VALUE"],
            "AMBIGUOUS": counts["HUMAN_REVIEW_REQUIRED"],
            "NOT_A_GAP": counts["NOT_A_GAP"],
        },
        "workload": {
            "BRAND_NEW_ANSWER_BUILDS": a_new + b_new,
            "EXISTING_ANSWER_ENRICHMENTS": kinds["ENRICH_EDIT"],
            "NOTES_BASED_ANSWER_PROMOTIONS":
                b_new + kinds["EXISTING_CARD_NOTES_PROMOTION"],
            "FOLLOWUP_INSERTIONS": kinds["FOLLOWUP_INSERTION"],
            "TOTAL_PRODUCTION_ACTIONS": len(actions),
        },
        "projected_canonical": {
            "formula": "CURRENT + NEW_FROM_GAP + NEW_FROM_NOTES_PROMOTION",
            "CURRENT_CANONICAL": baseline,
            "APPROVED_NEW_FROM_GAP": a_new,
            "APPROVED_NEW_FROM_NOTES_PROMOTION": b_new,
            "FINAL_PROJECTED_CANONICAL": baseline + a_new + b_new,
            "superseded_provisional": baseline + data["headline"][
                "ADDITIONAL_NEW_CANONICAL_QA_COUNT"],
        },
        "p0_control": {
            "p0_new_questions_already_created":
                data["baseline"]["p0_new_questions_already_created"],
            "p0_families_excluded_from_universe":
                data["universe"]["completed_p0_families_excluded"],
            "total_new_cards_since_pre_p0":
                data["baseline"]["p0_new_questions_already_created"]
                + a_new + b_new,
        },
        "batches": batches,
        "duplicate_home_debt": data["duplicate_home_debt"],
        "production_actions": actions,
        "families": rows,
    }

    OUT_JSON.write_text(json.dumps(payload, indent=1, sort_keys=False,
                                   ensure_ascii=False) + "\n", encoding="utf-8")
    write_md(payload)
    print("wrote %s (%d actions, %d families)"
          % (OUT_JSON.name, len(actions), len(rows)))


def write_md(p):
    a = p["authorised"]
    w = p["workload"]
    pc = p["projected_canonical"]
    L = []
    L.append("# Final Oral production authorization - laptop review\n")
    L.append("Independent review of the final gap adjudication. Counts below are "
             "**production actions**, not source families.\n")
    L.append("## Authorised workload\n")
    L.append("| action | count |")
    L.append("| --- | ---: |")
    for k, v in w.items():
        L.append("| %s | %d |" % (k.replace("_", " ").lower(), v))
    L.append("")
    L.append("## Projected canonical count\n")
    L.append("```")
    L.append("%d current" % pc["CURRENT_CANONICAL"])
    L.append("+ %d new cards from gap families" % pc["APPROVED_NEW_FROM_GAP"])
    L.append("+ %d new cards from Notes promotions"
             % pc["APPROVED_NEW_FROM_NOTES_PROMOTION"])
    L.append("= %d" % pc["FINAL_PROJECTED_CANONICAL"])
    L.append("```")
    L.append("")
    L.append("This supersedes the provisional %d, which counted no Notes "
             "promotion as card-creating.\n" % pc["superseded_provisional"])
    L.append("## Dispositions the laptop review changed\n")
    L.append("| family | adjudicated | laptop |")
    L.append("| --- | --- | --- |")
    for r in p["families"]:
        if r["laptop_review_status"] == "LAPTOP_CHANGED":
            L.append("| %s | %s | %s |" % (r["family_id"],
                                           r["adjudicated_decision"],
                                           r["laptop_decision"]))
    L.append("")
    L.append("## Enrichment actions serving more than one family\n")
    L.append("| action | target | families |")
    L.append("| --- | --- | --- |")
    for act in p["production_actions"]:
        if act["kind"] in ("ENRICH_EDIT", "FOLLOWUP_INSERTION") \
                and len(act["family_ids"]) > 1:
            L.append("| %s | `%s` | %s |" % (act["production_action_id"],
                                             act["target"],
                                             ", ".join(act["family_ids"])))
    L.append("")
    L.append("Enrichment source families: %d. Unique enrichment edits: %d.\n"
             % (a["ENRICHMENT_SOURCE_FAMILIES"],
                a["AUTHORISED_EXISTING_QB_ENRICHMENT_ACTIONS"]))
    L.append("Follow-up source families: %d. Unique insertion groups: %d.\n"
             % (a["FOLLOWUP_SOURCE_FAMILIES"],
                a["AUTHORISED_FOLLOWUP_INSERTION_ACTIONS"]))
    L.append("Distinct existing cards visited: %d.\n"
             % a["UNIQUE_EXISTING_CARD_VISITS"])
    L.append("## Production batches\n")
    for k in sorted(p["batches"]):
        L.append("- **%s** (%d): %s" % (k, len(p["batches"][k]),
                                        ", ".join(p["batches"][k])))
    L.append("")
    OUT_MD.write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
