"""Mutation harness for the final Oral production authorisation.

A validator that has never been observed to fail is not evidence. Each mutation
below breaks exactly one property, and the run is only a pass if:

  * the mutation was genuinely APPLIED - proved by a SHA-256 delta on the file,
    never by the fact that the mutating code ran. A mutation that silently
    no-ops is reported as an ESCAPE, not as a pass;
  * the validator FAILED while it was applied, and named the expected check;
  * the file was RESTORED byte-for-byte afterwards, proved by digest.

A crash is never a pass. An escape is never a pass.
"""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "meoclass1" / "oral-intelligence" / "examiner-audit"
DATA = AUDIT / "FINAL_ORAL_PRODUCTION_AUTHORIZATION.json"
VALIDATOR = Path(__file__).resolve().parent / "validate_production_authorization.py"


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write(payload) -> None:
    DATA.write_text(json.dumps(payload, indent=1, sort_keys=False,
                               ensure_ascii=False) + "\n",
                    encoding="utf-8", newline="\n")


def run_validator():
    r = subprocess.run([sys.executable, str(VALIDATOR)],
                       capture_output=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


# ---------------------------------------------------------------- mutations
def m_ambiguous_as_new(d):
    amb = next(r for r in d["families"]
               if r["laptop_decision"] == "HUMAN_REVIEW_REQUIRED")
    d["production_actions"].append({
        "kind": "NEW_CARD_FROM_GAP", "key": amb["family_id"],
        "family_ids": [amb["family_id"]], "target": None, "note": "injected",
        "production_action_id": "NEW-999"})
    return d


def m_duplicate_action_id(d):
    d["production_actions"][1]["production_action_id"] = \
        d["production_actions"][0]["production_action_id"]
    return d


def m_new_without_evidence(d):
    a = next(a for a in d["production_actions"]
             if a["kind"] == "NEW_CARD_FROM_GAP")
    for r in d["families"]:
        if r["family_id"] == a["family_ids"][0]:
            r["source_occurrence_ids"] = []
    return d


def m_p0_reentry(d):
    row = copy.deepcopy(d["families"][0])
    row["family_id"] = "GAP-0002"
    row["laptop_decision"] = "NEW_CANONICAL_QA"
    d["families"].append(row)
    return d


def m_dead_enrichment_target(d):
    a = next(a for a in d["production_actions"] if a["kind"] == "ENRICH_EDIT")
    a["target"] = "QB1_A#q9999"
    return d


def m_projected_count_omits_promotions(d):
    pc = d["projected_canonical"]
    pc["APPROVED_NEW_FROM_NOTES_PROMOTION"] = 0
    pc["FINAL_PROJECTED_CANONICAL"] = (pc["CURRENT_CANONICAL"]
                                       + pc["APPROVED_NEW_FROM_GAP"])
    return d


def m_family_in_two_actions(d):
    a = next(a for a in d["production_actions"] if a["kind"] == "ENRICH_EDIT")
    fid = a["family_ids"][0]
    d["production_actions"].append({
        "kind": "FOLLOWUP_INSERTION", "key": "x", "family_ids": [fid],
        "target": a["target"], "note": "injected",
        "production_action_id": "FUP-999"})
    return d


def m_covered_target_also_promoted(d):
    row = next(r for r in d["families"]
               if r["laptop_decision"] == "ALREADY_COVERED"
               and str(r["target"]).startswith("QB"))
    other = next(r for r in d["families"]
                 if r["laptop_decision"] == "NOTES_TO_QB_PROMOTION")
    other["target"] = row["target"]
    return d


def m_enrichment_not_deduped(d):
    d["authorised"]["AUTHORISED_EXISTING_QB_ENRICHMENT_ACTIONS"] = \
        d["authorised"]["ENRICHMENT_SOURCE_FAMILIES"]
    return d


def m_unclassified_promotion(d):
    row = next(r for r in d["families"]
               if r["laptop_decision"] == "ENRICH_EXISTING_QB")
    row["laptop_decision"] = "NOTES_TO_QB_PROMOTION"
    return d


def m_override_not_applied(d):
    row = next(r for r in d["families"] if r["family_id"] == "GAP-0516")
    row["laptop_decision"] = "DEFER_LOW_VALUE"
    return d


def m_family_dropped(d):
    d["families"] = [r for r in d["families"] if r["family_id"] != "GAP-0080"]
    return d


def m_headline_inflated(d):
    d["authorised"]["AUTHORISED_NEW_CANONICAL_QA"] += 5
    return d


def m_changed_status_unrecorded(d):
    row = next(r for r in d["families"]
               if r["laptop_review_status"] == "LAPTOP_CONFIRMED")
    row["laptop_review_status"] = "LAPTOP_CHANGED"
    return d


def m_cheatsheet_target(d):
    a = next(a for a in d["production_actions"]
             if a["kind"] == "FOLLOWUP_INSERTION")
    a["target"] = "QB1_A_CheatSheet#q1"
    return d


def m_baseline_lie(d):
    d["baseline"]["live_canonical_questions"] = 999
    return d


def m_duplicate_home_debt_dropped(d):
    d["duplicate_home_debt"] = []
    return d


MUTATIONS = [
    ("A  ambiguous family authorised as NEW", m_ambiguous_as_new, "A "),
    ("B  duplicate production action id", m_duplicate_action_id, "B "),
    ("C  approved new card without evidence", m_new_without_evidence, "C "),
    ("D  completed P0 family reintroduced", m_p0_reentry, "D "),
    ("E  enrichment target does not resolve", m_dead_enrichment_target, "E "),
    ("F  projected count omits Notes promotions",
     m_projected_count_omits_promotions, "F "),
    ("G1 family assigned to two action kinds", m_family_in_two_actions, "G1"),
    ("G2 covered target also promoted-from", m_covered_target_also_promoted, "G2"),
    ("N3 enrichment edits not deduplicated", m_enrichment_not_deduped, "N3"),
    ("N7 promotion left unclassified", m_unclassified_promotion, "N7"),
    ("S6 recorded override not applied", m_override_not_applied, "S6"),
    ("S1 adjudicated family dropped", m_family_dropped, "S1"),
    ("N1 headline count inflated", m_headline_inflated, "N1"),
    ("S5 unrecorded family marked changed", m_changed_status_unrecorded, "S5"),
    ("P1 action targets a cheatsheet", m_cheatsheet_target, "P1"),
    ("baseline claim falsified", m_baseline_lie, "baseline"),
    ("P2 duplicate-home debt dropped", m_duplicate_home_debt_dropped, "P2"),
]


def main():
    if not DATA.exists():
        print("unavailable: %s not generated" % DATA.name)
        sys.exit(1)
    original = DATA.read_bytes()
    base = digest(DATA)

    rc, _ = run_validator()
    if rc != 0:
        print("unavailable: validator does not pass before mutation")
        sys.exit(1)
    print("baseline validator PASSES, digest %s\n" % base[:16])

    escapes = crashes = noops = caught = 0
    for name, fn, expect in MUTATIONS:
        payload = json.loads(original.decode("utf-8"))
        try:
            write(fn(payload))
        except Exception as exc:  # a mutation that cannot build is a crash
            print("CRASH  %-46s %s" % (name, exc))
            crashes += 1
            DATA.write_bytes(original)
            continue

        if digest(DATA) == base:
            print("NO-OP  %-46s mutation did not change the file" % name)
            noops += 1
            DATA.write_bytes(original)
            continue

        rc, out = run_validator()
        named = ("FAIL %s" % expect.strip()) in out or expect.strip() in \
            "\n".join(l for l in out.splitlines() if l.startswith("FAIL"))
        if rc == 0:
            print("ESCAPE %-46s validator still passed" % name)
            escapes += 1
        elif not named:
            print("WEAK   %-46s failed, but not via %s" % (name, expect.strip()))
            escapes += 1
        else:
            print("CAUGHT %-46s -> %s" % (name, expect.strip()))
            caught += 1

        DATA.write_bytes(original)
        if digest(DATA) != base:
            print("RESTORE FAILED after %s" % name)
            sys.exit(1)

    print("\n%d mutations: %d caught, %d escapes, %d no-ops, %d crashes"
          % (len(MUTATIONS), caught, escapes, noops, crashes))
    print("restored digest %s == baseline %s"
          % (digest(DATA)[:16], base[:16]))
    sys.exit(0 if (escapes == 0 and noops == 0 and crashes == 0) else 1)


if __name__ == "__main__":
    main()
