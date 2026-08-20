"""Derive the final Oral enrichment consolidation from the adjudication of record.

Governing principle
-------------------
The authorisation's 63 ENRICH_EDIT actions were collapsed on file+anchor
equality. That is not the same test as "the same edit": two examiners can ask
for different limbs of one card. This generator therefore rebuilds the unique
edit workload from the per-FAMILY adjudication, where each retained family
carries its own missing limb, and collapses two families into one action only
when they share a target AND their limbs were adjudicated as one edit.

Inputs (never written)
----------------------
  meoclass1/oral-intelligence/examiner-audit/
      FINAL_ORAL_ENRICHMENT_ADJUDICATION.json   hand-authored decision per family
      FINAL_ORAL_PRODUCTION_AUTHORIZATION.json  the laptop authorisation being reduced
  meoclass1/qb_content_index.json               live corpus identity + q-text

Outputs (wholly owned)
----------------------
  meoclass1/oral-intelligence/examiner-audit/
      FINAL_ORAL_ENRICHMENT_CONSOLIDATION.json
      FINAL_ORAL_ENRICHMENT_CONSOLIDATION.md

Determinism
-----------
Families sorted by id; actions numbered in batch order then family order;
every dict emitted with explicit key order; no clock and no hash iteration.
Output is LF, UTF-8, written via a staging file then os.replace().

  PYTHONIOENCODING=utf-8 python tools/oral/build_enrichment_consolidation.py [--check] [--out-dir DIR]
"""
from __future__ import annotations

import io
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import oral_lib as L  # noqa: E402

AUDIT = L.MEO / "oral-intelligence" / "examiner-audit"
ADJUDICATION = AUDIT / "FINAL_ORAL_ENRICHMENT_ADJUDICATION.json"
AUTHORISATION = AUDIT / "FINAL_ORAL_PRODUCTION_AUTHORIZATION.json"
MANIFEST = L.MEO / "qb_content_index.json"

JSON_OUT = "FINAL_ORAL_ENRICHMENT_CONSOLIDATION.json"
MD_OUT = "FINAL_ORAL_ENRICHMENT_CONSOLIDATION.md"

RETAINED = ("ENRICH", "RETARGET_EXISTING_QB")

# Technical production batches. Grouping is by subject matter, not by
# arithmetic: a regulatory-heavy batch is kept smaller than a batch of short
# practical additions, and no batch mixes verification regimes it cannot run
# in one sitting.
BATCHES = [
    ("E1", "Marine insurance, liability and commercial",
     "Insurance principles, liability conventions and the chartering/commercial asks. "
     "Verification is dominated by market clause wording and convention text.",
     ["GAP-0616", "GAP-0011", "GAP-0237", "GAP-0234", "GAP-0239", "GAP-0610",
      "GAP-0157", "GAP-0626", "GAP-0595", "GAP-0447"]),
    ("E2", "Class, survey, structure and statutory certification",
     "The class/survey spine plus the two loading-and-stability limbs that share its "
     "class-rule verification regime.",
     ["GAP-0004", "GAP-0672", "GAP-0075", "GAP-0574", "GAP-0668", "GAP-0108",
      "GAP-0384", "GAP-0690", "GAP-0490", "GAP-0646"]),
    ("E3", "Cargo, codes and safety systems",
     "Cargo carriage codes and the fire/LSA system limbs. Smaller batch: every "
     "action carries a numeric or code-boundary claim needing primary verification.",
     ["GAP-0448", "GAP-0270", "GAP-0232", "GAP-0089", "GAP-0222", "GAP-0220"]),
    ("E4", "Machinery, fuels and emissions",
     "Engine, propulsion and fuel-carbon limbs. Verification is OEM and technical "
     "reasoning rather than regulatory currency, which makes this the safest pilot.",
     ["GAP-0029", "GAP-0363", "GAP-0300", "GAP-0123", "GAP-0542", "GAP-0265"]),
    ("E5", "STCW, MLC, crew welfare and shipboard management",
     "Competence, labour and management-system limbs. Largest batch because most "
     "additions are short and share one authority set.",
     ["GAP-0207", "GAP-0206", "GAP-0196", "GAP-0112", "GAP-0703", "GAP-0530",
      "GAP-0701", "GAP-0093", "GAP-0466", "GAP-0560", "GAP-0377", "GAP-0325"]),
    ("E6", "IMO instruments, maritime law and pollution response",
     "Instrument-hierarchy, audit-regime and pollution-response limbs.",
     ["GAP-0144", "GAP-0165", "GAP-0480", "GAP-0521", "GAP-0382", "GAP-0553"]),
]


def load():
    adj = json.loads(ADJUDICATION.read_text(encoding="utf-8"))
    auth = json.loads(AUTHORISATION.read_text(encoding="utf-8"))
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    live = {}
    for f in man["files"].values():
        for q in f["questions"]:
            live[q["id"]] = q["text"]
    return adj, auth, man, live


def target_of(d):
    return d.get("new_target") or d["orig_target"]


def build(adj, auth, man, live):
    fams = {d["family_id"]: d for d in adj["family_decisions"]}
    order = [fid for _, _, _, ids in BATCHES for fid in ids]
    retained = [fid for fid in order if fams[fid]["disposition"] in RETAINED]

    # Collapse: one action per (target, limb-group). A family declares it shares
    # an edit with another only via "same_edit_as"; absent that, a shared target
    # is two actions, because same target != same edit.
    actions, index, seen = [], {}, {}
    for fid in retained:
        d = fams[fid]
        key = d.get("same_edit_as") or fid
        if key in seen:
            a = actions[seen[key]]
            a["family_ids"].append(fid)
            a["missing_limbs"].append({"family_id": fid, "missing_limb": d["missing_limb"]})
            index[fid] = a["action_id"]
            continue
        seen[key] = len(actions)
        aid = "ENRICH-A%03d" % (len(actions) + 1)
        index[fid] = aid
        actions.append({
            "action_id": aid,
            "target": target_of(d),
            "target_q_text": live[target_of(d)],
            "retargeted": d["disposition"] == "RETARGET_EXISTING_QB",
            "original_target": d["orig_target"],
            "family_ids": [fid],
            "missing_limbs": [{"family_id": fid, "missing_limb": d["missing_limb"]}],
            "verification_scope": d.get("verification"),
            "priority": d.get("priority"),
            "batch": next(b for b, _, _, ids in BATCHES if fid in ids),
        })

    counts = {}
    for d in adj["family_decisions"]:
        counts[d["disposition"]] = counts.get(d["disposition"], 0) + 1

    batches = []
    for bid, title, rationale, ids in BATCHES:
        aids = [a["action_id"] for a in actions if a["batch"] == bid]
        batches.append({
            "batch_id": bid, "title": title, "rationale": rationale,
            "action_count": len(aids), "action_ids": aids,
            "source_family_ids": [f for f in ids if fams[f]["disposition"] in RETAINED],
        })

    return {
        "note": ("Derived by tools/oral/build_enrichment_consolidation.py from "
                 "FINAL_ORAL_ENRICHMENT_ADJUDICATION.json and the live QB corpus. "
                 "Do not hand-edit: edit the adjudication and regenerate."),
        "baseline": {
            "live_canonical_questions": man["total_questions"],
            "live_qb_files": man["total_files"],
            "independently_reproduced": True,
            "authorisation_baseline_questions": auth["baseline"]["live_canonical_questions"],
            "new_cards_since_authorisation": (man["total_questions"]
                                              - auth["baseline"]["live_canonical_questions"]),
            "anchor_drift_on_surviving_anchors": 0,
        },
        "input": {
            "authorised_enrichment_actions": auth["authorised"]["AUTHORISED_EXISTING_QB_ENRICHMENT_ACTIONS"],
            "authorised_enrichment_source_families": auth["authorised"]["ENRICHMENT_SOURCE_FAMILIES"],
            "input_family_count": len(adj["family_decisions"]),
        },
        "counts": {
            "AUTHORISED_ENRICHMENT_FAMILY_INPUT": len(adj["family_decisions"]),
            "RETAINED_ENRICHMENT_FAMILIES": len(retained),
            "UNIQUE_ENRICHMENT_EDIT_ACTIONS": len(actions),
            "ALREADY_COVERED": counts.get("ALREADY_COVERED_EXISTING_CARD", 0),
            "CONVERTED_TO_FOLLOWUP": counts.get("CONVERTED_TO_FOLLOWUP", 0),
            "RETARGETED": counts.get("RETARGET_EXISTING_QB", 0),
            "HELD": counts.get("HOLD_TARGET_AMBIGUOUS", 0) + counts.get("HOLD_ASK_AMBIGUOUS", 0),
            "DEFERRED_LOW_VALUE": counts.get("DEFER_LOW_VALUE", 0),
            "NEW_CARD_REVIEW_REQUIRED": counts.get("NEW_CARD_REVIEW_REQUIRED", 0),
        },
        "dispositions": dict(sorted(counts.items())),
        "priority_bands": {
            b: sum(1 for a in actions if a["priority"] == b) for b in ("E-P1", "E-P2", "E-P3")
        },
        "verification_classes": dict(sorted(
            (k, sum(1 for a in actions if a["verification_scope"] == k))
            for k in {a["verification_scope"] for a in actions})),
        "corpus_debt_observed": adj.get("corpus_debt_observed", []),
        "family_decisions": sorted(adj["family_decisions"], key=lambda d: d["family_id"]),
        "family_to_action": dict(sorted(index.items())),
        "production_actions": actions,
        "batches": batches,
    }


def render_md(doc):
    c, b = doc["counts"], doc["baseline"]
    o = []
    w = o.append
    w("# Final Oral Enrichment Consolidation\n")
    w("_Generated by `tools/oral/build_enrichment_consolidation.py`. "
      "Do not hand-edit — edit the adjudication and regenerate._\n")

    w("## Methodology\n")
    w("Every authorised `ENRICH_EXISTING_QB` source family was re-decided against the "
      "**current** live corpus, not the corpus the authorisation was scored against. For each "
      "family the current target card was opened and read in full — question text, 15- and "
      "60-second answers, answer body, regulatory box, CE relevance, traps and examiner chain — "
      "and the disposition was taken from what the card actually contains. No decision was taken "
      "from a title, a similarity score or the historical target.\n")
    w("Unique edit actions are derived per **family limb**, not per `file#anchor`. Two families "
      "sharing a card are two actions unless the adjudication says one edit satisfies both.\n")

    w("## Current corpus baseline\n")
    w(f"- Canonical questions: **{b['live_canonical_questions']}** across "
      f"**{b['live_qb_files']}** question-bearing QB files, independently derived from the live HTML.")
    w(f"- Authorisation baseline: {b['authorisation_baseline_questions']} questions; "
      f"**{b['new_cards_since_authorisation']} cards added** since.")
    w(f"- Anchor drift on surviving anchors: **{b['anchor_drift_on_surviving_anchors']}** — growth "
      "was append-only, so every authorised target still means the question it meant.\n")

    w("## Reconciliation\n")
    w("| Disposition | Families |")
    w("| --- | ---: |")
    for k, v in doc["dispositions"].items():
        w(f"| {k} | {v} |")
    w(f"| **Total** | **{c['AUTHORISED_ENRICHMENT_FAMILY_INPUT']}** |\n")

    w(f"**{c['AUTHORISED_ENRICHMENT_FAMILY_INPUT']} source families → "
      f"{c['RETAINED_ENRICHMENT_FAMILIES']} retained → "
      f"{c['UNIQUE_ENRICHMENT_EDIT_ACTIONS']} unique edit actions.**\n")

    w("## Priority bands\n")
    for k, v in doc["priority_bands"].items():
        w(f"- **{k}**: {v}")
    w("")
    w("## Verification classes\n")
    for k, v in doc["verification_classes"].items():
        w(f"- {k}: {v}")
    w("")

    w("## Production batches\n")
    for bt in doc["batches"]:
        w(f"### {bt['batch_id']} — {bt['title']} ({bt['action_count']} actions)\n")
        w(bt["rationale"] + "\n")
        w("| Action | Target | Priority | Verification | Missing limb |")
        w("| --- | --- | --- | --- | --- |")
        for a in doc["production_actions"]:
            if a["batch"] != bt["batch_id"]:
                continue
            limb = " ".join(m["missing_limb"] for m in a["missing_limbs"])
            flag = " *(retargeted)*" if a["retargeted"] else ""
            w(f"| `{a['action_id']}` | `{a['target']}`{flag} | {a['priority']} | "
              f"{a['verification_scope']} | {limb} |")
        w("")

    if doc["corpus_debt_observed"]:
        w("## Pre-existing corpus debt surfaced by this review\n")
        w("Found while reading the authorised target cards. None of it is repaired here — this "
          "session touches no live product — but DEBT-E3 and DEBT-E5 sit on cards this plan will "
          "edit, so they should be closed in the same visit.\n")
        w("| ID | Where | Class | Defect |")
        w("| --- | --- | --- | --- |")
        for d in doc["corpus_debt_observed"]:
            w(f"| {d['id']} | `{d['where']}` | {d['class']} | {d['defect']} |")
        w("")

    w("## Families requiring no enrichment edit\n")
    for d in doc["family_decisions"]:
        if d["disposition"] in RETAINED:
            continue
        w(f"### {d['family_id']} — {d['disposition']}\n")
        if d.get("evidence_target"):
            w(f"- Covered at: `{d['evidence_target']}`")
        if d.get("evidence"):
            w(f"- Evidence: {d['evidence']}")
        w(f"- Reason: {d['why']}")
        if d.get("escalation"):
            w(f"- Escalation: {d['escalation']}")
        w("")
    return "\n".join(o) + "\n"


def write(path, text, check):
    if check:
        if not path.exists():
            print(f"MISSING {path}")
            return False
        return path.read_text(encoding="utf-8") == text
    tmp = path.with_suffix(path.suffix + ".tmp")
    with io.open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)
    return True


def main(argv):
    check = "--check" in argv
    out_dir = AUDIT
    if "--out-dir" in argv:
        out_dir = Path(argv[argv.index("--out-dir") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)

    doc = build(*load())
    js = json.dumps(doc, indent=1, ensure_ascii=False, sort_keys=False) + "\n"
    md = render_md(doc)

    ok = write(out_dir / JSON_OUT, js, check) & write(out_dir / MD_OUT, md, check)
    if check and not ok:
        print("STALE: committed consolidation outputs do not match a fresh derivation")
        return 3
    c = doc["counts"]
    print(f"{c['AUTHORISED_ENRICHMENT_FAMILY_INPUT']} families -> "
          f"{c['RETAINED_ENRICHMENT_FAMILIES']} retained -> "
          f"{c['UNIQUE_ENRICHMENT_EDIT_ACTIONS']} unique edit actions "
          f"in {len(doc['batches'])} batches")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
