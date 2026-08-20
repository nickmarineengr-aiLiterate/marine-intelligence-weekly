"""Validate the final Oral enrichment consolidation against the live corpus.

Every check fails closed: a missing input is an error, never a skip. The
guard that matters most is target resolution — an enrichment aimed at a card
that does not own the ask is worse than no enrichment at all, because it
looks like coverage.

  PYTHONIOENCODING=utf-8 python tools/oral/validate_enrichment_consolidation.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import oral_lib as L  # noqa: E402

AUDIT = L.MEO / "oral-intelligence" / "examiner-audit"
ADJ = AUDIT / "FINAL_ORAL_ENRICHMENT_ADJUDICATION.json"
AUTH = AUDIT / "FINAL_ORAL_PRODUCTION_AUTHORIZATION.json"
CONS = AUDIT / "FINAL_ORAL_ENRICHMENT_CONSOLIDATION.json"
MANIFEST = L.MEO / "qb_content_index.json"

RETAINED = ("ENRICH", "RETARGET_EXISTING_QB")
KNOWN = {"ENRICH", "RETARGET_EXISTING_QB", "ALREADY_COVERED_EXISTING_CARD",
         "CONVERTED_TO_FOLLOWUP", "HOLD_TARGET_AMBIGUOUS", "HOLD_ASK_AMBIGUOUS",
         "DEFER_LOW_VALUE", "NEW_CARD_REVIEW_REQUIRED"}

errors = []


def err(code, msg):
    errors.append(f"[{code}] {msg}")


def require(path):
    if not path.exists():
        err("C00", f"required input missing: {path}")
        raise SystemExit(_report())
    return json.loads(path.read_text(encoding="utf-8"))


def _report():
    for e in errors:
        print(e)
    print(f"\n{len(errors)} error(s)")
    return 1 if errors else 0


def main():
    adj, auth, cons, man = (require(p) for p in (ADJ, AUTH, CONS, MANIFEST))

    live = {}
    for f in man["files"].values():
        for q in f["questions"]:
            live[q["id"]] = q["text"]

    fams = adj["family_decisions"]
    by_id = {d["family_id"]: d for d in fams}
    actions = cons["production_actions"]

    # C01 every authorised enrichment family is adjudicated exactly once
    authorised = [fid for a in auth["production_actions"] if a["kind"] == "ENRICH_EDIT"
                  for fid in a["family_ids"]]
    dup = [k for k, v in Counter(d["family_id"] for d in fams).items() if v > 1]
    if dup:
        err("C01", f"family adjudicated more than once: {sorted(dup)}")
    for fid in sorted(set(authorised) - set(by_id)):
        err("C01", f"authorised enrichment family missing from adjudication: {fid}")
    for fid in sorted(set(by_id) - set(authorised)):
        err("C01", f"adjudicated family is not an authorised enrichment family: {fid}")

    # C02 dispositions are from the known set
    for d in fams:
        if d["disposition"] not in KNOWN:
            err("C02", f"{d['family_id']}: unknown disposition {d['disposition']!r}")

    # C03 counts are derived, not asserted
    if cons["counts"]["AUTHORISED_ENRICHMENT_FAMILY_INPUT"] != len(fams):
        err("C03", "input family count disagrees with the adjudication records")
    if sum(cons["dispositions"].values()) != len(fams):
        err("C03", "disposition tally does not sum to the input family count")
    retained = [d for d in fams if d["disposition"] in RETAINED]
    if cons["counts"]["RETAINED_ENRICHMENT_FAMILIES"] != len(retained):
        err("C03", "retained family count disagrees with the records")
    if cons["counts"]["UNIQUE_ENRICHMENT_EDIT_ACTIONS"] != len(actions):
        err("C03", "unique action count disagrees with the action records")

    # C04 action ids unique
    d2 = [k for k, v in Counter(a["action_id"] for a in actions).items() if v > 1]
    if d2:
        err("C04", f"duplicate production action id: {sorted(d2)}")

    # C05 every action has at least one family; every retained family has an action
    mapped = set()
    for a in actions:
        if not a["family_ids"]:
            err("C05", f"{a['action_id']}: production action with zero families")
        mapped.update(a["family_ids"])
    for d in retained:
        if d["family_id"] not in mapped:
            err("C05", f"{d['family_id']}: retained but has no production action")
        if cons["family_to_action"].get(d["family_id"]) is None:
            err("C05", f"{d['family_id']}: retained but absent from family_to_action")
    for d in fams:
        if d["disposition"] not in RETAINED and d["family_id"] in mapped:
            err("C05", f"{d['family_id']}: not retained yet mapped to an action")

    # C06 a family may not appear in two actions
    seen = Counter(fid for a in actions for fid in a["family_ids"])
    for fid, n in sorted(seen.items()):
        if n > 1:
            err("C06", f"{fid}: assigned to {n} incompatible actions")

    # C07 target resolution: file+anchor exists and the recorded q-text is the live one
    for a in actions:
        if a["target"] not in live:
            err("C07", f"{a['action_id']}: target {a['target']} does not resolve in the live corpus")
        elif a["target_q_text"] != live[a["target"]]:
            err("C07", f"{a['action_id']}: recorded q-text does not match live HTML at {a['target']}")
        for fid in a["family_ids"]:
            d = by_id.get(fid)
            if d is None:
                err("C07", f"{a['action_id']}: references family {fid}, which is not adjudicated")
                continue
            t = d.get("new_target") or d["orig_target"]
            if t != a["target"]:
                err("C07", f"{fid}: family target {t} disagrees with action target {a['target']}")

    # C08 every retained family states a missing limb
    for d in retained:
        if not (d.get("missing_limb") or "").strip():
            err("C08", f"{d['family_id']}: retained enrichment with a blank missing limb")
    for a in actions:
        for m in a["missing_limbs"]:
            if not (m.get("missing_limb") or "").strip():
                err("C08", f"{a['action_id']}: limb entry for {m['family_id']} is blank")

    # C09 already-covered needs an evidence target that resolves, plus evidence text
    for d in fams:
        if d["disposition"] != "ALREADY_COVERED_EXISTING_CARD":
            continue
        t = d.get("evidence_target")
        if not t:
            err("C09", f"{d['family_id']}: ALREADY_COVERED without an evidence target")
        elif t not in live:
            err("C09", f"{d['family_id']}: evidence target {t} does not resolve")
        if not (d.get("evidence") or "").strip():
            err("C09", f"{d['family_id']}: ALREADY_COVERED without evidence text")

    # C10 retarget needs old, new, and both reasons
    for d in fams:
        if d["disposition"] != "RETARGET_EXISTING_QB":
            continue
        if not d.get("new_target"):
            err("C10", f"{d['family_id']}: retarget without a new target")
        elif d["new_target"] == d["orig_target"]:
            err("C10", f"{d['family_id']}: retarget to the same target")
        for k in ("why_old_wrong", "why_new_right"):
            if not (d.get(k) or "").strip():
                err("C10", f"{d['family_id']}: retarget without {k}")

    # C11 follow-up conversion needs a parent that resolves, and an insertion note
    for d in fams:
        if d["disposition"] != "CONVERTED_TO_FOLLOWUP":
            continue
        p = d.get("parent")
        if not p:
            err("C11", f"{d['family_id']}: follow-up conversion without a parent")
        elif p not in live:
            err("C11", f"{d['family_id']}: follow-up parent {p} does not resolve")
        if not (d.get("insertion") or "").strip():
            err("C11", f"{d['family_id']}: follow-up conversion without an insertion location")

    # C12 holds and defers must carry a reason and must NOT carry a limb
    for d in fams:
        if d["disposition"] in RETAINED:
            continue
        if not (d.get("why") or "").strip():
            err("C12", f"{d['family_id']}: {d['disposition']} without a reason")

    # C13 batches cover every retained family exactly once and nothing else
    bfam = [f for b in cons["batches"] for f in b["source_family_ids"]]
    if sorted(bfam) != sorted(d["family_id"] for d in retained):
        err("C13", "batch membership does not equal the retained family set")
    bact = [a for b in cons["batches"] for a in b["action_ids"]]
    if sorted(bact) != sorted(a["action_id"] for a in actions):
        err("C13", "batch action ids do not equal the action set")
    for b in cons["batches"]:
        if b["action_count"] != len(b["action_ids"]):
            err("C13", f"{b['batch_id']}: action_count disagrees with action_ids")

    # C14 baseline agrees with the live manifest
    if cons["baseline"]["live_canonical_questions"] != man["total_questions"]:
        err("C14", "baseline question count disagrees with the live manifest")
    if cons["baseline"]["live_qb_files"] != man["total_files"]:
        err("C14", "baseline file count disagrees with the live manifest")

    # C15 every action carries a priority band and a verification class
    for a in actions:
        if a["priority"] not in ("E-P1", "E-P2", "E-P3"):
            err("C15", f"{a['action_id']}: bad priority {a['priority']!r}")
        if not a["verification_scope"]:
            err("C15", f"{a['action_id']}: no verification scope")

    checks = 15
    if not errors:
        print(f"OK  {checks} checks, {len(fams)} families, {len(actions)} actions, 0 errors")
        return 0
    return _report()


if __name__ == "__main__":
    sys.exit(main())
