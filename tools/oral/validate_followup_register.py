#!/usr/bin/env python3
"""
Validate the Oral follow-up authorisation register.

WHY THIS GATE EXISTS
--------------------
The register is the ONLY committed statement of what follow-up production is
authorised to do. Before it existed the 35 actions lived in handoff prose on a
branch nobody would think to grep, which is the same defect class that was
closed twice already this month. A source of truth that nothing checks decays
into a source of truth that nothing can rely on.

WHAT IT CHECKS, AND WHY EACH ONE
--------------------------------
* IDENTITY      contiguous, unique FUP ids that still match an independent
                re-derivation from the pinned sources. This is what stops the
                register drifting away from the evidence it claims to encode.
* ACCOUNTING    every follow-up source family is owned by exactly ONE action,
                and every action's families exist upstream. Orphans and
                double-ownership are both silent ways to lose or duplicate work.
* TARGETS       every parent card still exists on the LIVE corpus, and the
                pinned parent q-text still matches. The register was built
                against a 721-question corpus; a later batch can move a card,
                and a stale parent pin would send a follow-up to the wrong home.
* VOCABULARY    every enum value is governed. `relationship_type` is checked
                against `validate_phase2.RELATIONSHIP_TYPES`, not a local copy,
                so the register can never carry a type the phase-2 gate rejects.
* SCOPE         `creates_new_card` is false unless an explicit exception names
                the action. A follow-up that quietly becomes a new card changes
                the canonical count without a manifest saying so.

FAILS CLOSED
------------
If the pinned source blobs are unavailable this gate reports `unavailable` and
returns non-zero. It never skips: a guard that passes when it cannot see its
evidence is worse than no guard.

Usage:
    python tools/oral/validate_followup_register.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import oral_lib  # noqa: E402
import build_followup_register as B  # noqa: E402
from validate_phase2 import RELATIONSHIP_TYPES  # noqa: E402

REGISTER = HERE / "oral_followup_register.json"

# Actions explicitly permitted to create a new card. Empty by design: no
# follow-up in this register was authorised to add a canonical question, and
# every source action is a FOLLOWUP_INSERTION onto an existing parent. An
# addition here is a deliberate, reviewable act.
NEW_CARD_EXCEPTIONS = set()

EXPECTED_ACTIONS = 35
EXPECTED_SOURCE_FAMILIES = 39

_checks = 0
_failed = []


def report(name, ok, detail=""):
    global _checks
    _checks += 1
    if not ok:
        _failed.append(name)
    print("%-4s %-52s %s" % ("PASS" if ok else "FAIL", name, detail))


def unavailable(reason):
    print("unavailable: %s" % reason)
    print("\n0 checks, 1 FAIL")
    return 2


def main():
    if not REGISTER.exists():
        return unavailable("register %s is absent" % REGISTER.name)

    try:
        reg = json.loads(REGISTER.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return unavailable("register unreadable: %s" % exc)

    # ---- the pinned sources must be readable, or this gate is blind --------
    try:
        auth = B.read_blob(B.SOURCES["authorisation"]["blob"])
        dec = B.read_blob(B.SOURCES["decisions"]["blob"])
    except SystemExit as exc:
        return unavailable(str(exc))

    actions = reg.get("actions") or []

    # ------------------------------------------------------------------ 1
    # Identity
    # ------------------------------------------------------------------
    ids = [a["followup_id"] for a in actions]
    report("action_count_matches_reconstructed_truth",
           len(actions) == EXPECTED_ACTIONS,
           "%d actions (expected %d)" % (len(actions), EXPECTED_ACTIONS))

    dupes = sorted(k for k, v in Counter(ids).items() if v > 1)
    report("followup_ids_unique", not dupes, "duplicates=%s" % (dupes or "none"))

    expected_ids = ["FUP-%03d" % i for i in range(1, len(actions) + 1)]
    report("followup_ids_contiguous_from_001", sorted(ids) == expected_ids,
           "first=%s last=%s" % (min(ids) if ids else "-", max(ids) if ids else "-"))

    # ------------------------------------------------------------------ 2
    # The register must still match an independent re-derivation. This is the
    # check that makes every other one meaningful: it proves the register is
    # the evidence, not a hand-edited approximation of it.
    # ------------------------------------------------------------------
    try:
        fresh = B.build()
    except SystemExit as exc:
        return unavailable("re-derivation failed: %s" % exc)

    report("register_is_byte_current_with_its_generator",
           B.serialise(fresh) == REGISTER.read_text(encoding="utf-8"),
           "run build_followup_register.py to refresh")

    derived_pairs = {a["followup_id"]: a["parent_canonical_id"]
                     for a in fresh["actions"]}
    live_pairs = {a["followup_id"]: a["parent_canonical_id"] for a in actions}
    report("ids_and_targets_match_independent_derivation",
           derived_pairs == live_pairs,
           "%d derived / %d in register" % (len(derived_pairs), len(live_pairs)))

    # ------------------------------------------------------------------ 3
    # Accounting against the upstream sources
    # ------------------------------------------------------------------
    upstream = {f["family_id"] for f in auth["families"]
                if f["adjudicated_decision"] == B.FOLLOWUP_DISPOSITION}
    report("upstream_followup_family_count",
           len(upstream) == EXPECTED_SOURCE_FAMILIES,
           "%d upstream (expected %d)" % (len(upstream), EXPECTED_SOURCE_FAMILIES))

    owned = [fid for a in actions for fid in a["source_family_ids"]]
    multi = sorted(k for k, v in Counter(owned).items() if v > 1)
    report("no_duplicate_source_family_ownership", not multi,
           "shared=%s" % (multi or "none"))

    report("every_source_family_accounted_exactly_once",
           set(owned) == upstream and len(owned) == len(upstream),
           "owned=%d upstream=%d" % (len(owned), len(upstream)))

    orphan = sorted(upstream - set(owned))
    report("no_unexplained_orphan_family", not orphan,
           "orphans=%s" % (orphan or "none"))

    alien = sorted(set(owned) - upstream)
    report("no_ungoverned_family_in_register", not alien,
           "alien=%s" % (alien or "none"))

    # occurrence identities must exist upstream, and must not be invented
    up_occ = {}
    for f in auth["families"]:
        up_occ[f["family_id"]] = set(f["source_occurrence_ids"])
    bad_occ = []
    for a in actions:
        want = set()
        for fid in a["source_family_ids"]:
            want |= up_occ.get(fid, set())
        if set(a["source_occurrence_ids"]) != want:
            bad_occ.append(a["followup_id"])
    report("source_occurrence_ids_match_upstream", not bad_occ,
           "bad=%s" % (bad_occ or "none"))

    dec_by = {f["family_id"]: f for f in dec["families"]}
    bad_ask = [a["followup_id"] for a in actions
               for i, fid in enumerate(a["source_family_ids"])
               if dec_by.get(fid, {}).get("ask") != a["original_asks"][i]]
    report("original_ask_matches_upstream_record", not bad_ask,
           "bad=%s" % (sorted(set(bad_ask)) or "none"))

    # ------------------------------------------------------------------ 4
    # Live-corpus targets
    # ------------------------------------------------------------------
    inv = oral_lib.build_inventory()
    by_qid = {r["canonical_question_id"]: r for r in inv}
    anchors = oral_lib.all_anchors()

    miss_file = [a["followup_id"] for a in actions
                 if a["parent_file"] not in anchors]
    report("every_parent_file_resolves", not miss_file,
           "missing=%s" % (miss_file or "none"))

    miss_anchor = [a["followup_id"] for a in actions
                   if a["parent_file"] in anchors
                   and a["parent_anchor"] not in anchors[a["parent_file"]]]
    report("every_parent_anchor_resolves", not miss_anchor,
           "missing=%s" % (miss_anchor or "none"))

    non_canon = [a["followup_id"] for a in actions
                 if a["parent_canonical_id"] not in by_qid]
    report("every_parent_is_a_canonical_question", not non_canon,
           "bad=%s" % (non_canon or "none"))

    # A stale parent pin is exactly how a follow-up lands on the wrong card
    # after some later batch rewrites a question text. Drift must be declared,
    # never discovered at authoring time.
    drift = [a["followup_id"] for a in actions
             if a["parent_canonical_id"] in by_qid
             and a["parent_qtext"] != by_qid[a["parent_canonical_id"]]["question_text"]
             and a["target_structural_check"] != "TARGET_DRIFTED"]
    report("parent_qtext_matches_live_card_or_drift_declared", not drift,
           "undeclared_drift=%s" % (drift or "none"))

    bad_struct = [a["followup_id"] for a in actions
                  if a["target_structural_check"] not in B.STRUCTURAL_STATES]
    report("target_structural_check_is_governed", not bad_struct,
           "bad=%s" % (bad_struct or "none"))

    # ------------------------------------------------------------------ 5
    # Vocabularies
    # ------------------------------------------------------------------
    def enum_check(name, field, allowed):
        bad = [a["followup_id"] for a in actions if a.get(field) not in allowed]
        report(name, not bad, "bad=%s" % (bad or "none"))

    enum_check("relationship_type_is_governed", "relationship_type",
               RELATIONSHIP_TYPES)
    enum_check("verification_class_is_governed", "verification_class",
               B.VERIFICATION_CLASSES)
    enum_check("priority_is_governed", "priority", B.PRIORITIES)
    enum_check("status_is_governed", "status", B.STATUSES)
    enum_check("target_confidence_is_governed", "target_confidence",
               B.TARGET_CONFIDENCES)
    enum_check("target_review_status_is_governed", "target_review_status",
               B.TARGET_REVIEW_STATUSES)

    bad_kind = [a["followup_id"] for a in actions
                if a.get("kind") != B.FOLLOWUP_KIND]
    report("kind_is_followup_insertion", not bad_kind,
           "bad=%s" % (bad_kind or "none"))

    # The relationship must be directed and must name this action, or a later
    # examiner simulator cannot walk it without re-authoring.
    bad_edge = []
    for a in actions:
        e = a.get("relationship_edge") or {}
        if (e.get("parent_question") != a["parent_canonical_id"]
                or e.get("followup") != a["followup_id"]
                or e.get("edge") != "EXAMINER_FOLLOW_UP"
                or e.get("answer_home") != a["parent_canonical_id"]):
            bad_edge.append(a["followup_id"])
    report("relationship_edge_is_directed_and_consistent", not bad_edge,
           "bad=%s" % (bad_edge or "none"))

    # ------------------------------------------------------------------ 6
    # Scope and provenance
    # ------------------------------------------------------------------
    bad_new = [a["followup_id"] for a in actions
               if a.get("creates_new_card")
               and a["followup_id"] not in NEW_CARD_EXCEPTIONS]
    report("creates_new_card_false_unless_excepted", not bad_new,
           "bad=%s" % (bad_new or "none"))

    prov = reg.get("provenance") or {}
    srcs = prov.get("sources") or {}
    report("register_provenance_present",
           bool(srcs) and set(srcs) == set(B.SOURCES)
           and all(srcs[k].get("blob") == B.SOURCES[k]["blob"] for k in B.SOURCES),
           "sources=%s" % sorted(srcs))

    report("register_declares_no_authored_content",
           prov.get("content_authored_here") is False,
           str(prov.get("content_authored_here")))

    report("register_is_an_authorisation_record_not_a_batch_manifest",
           reg.get("record_class") == "AUTHORISATION_REGISTER",
           str(reg.get("record_class")))

    missing_prov = [a["followup_id"] for a in actions
                    if not a.get("source_families")
                    or any(not m.get("decision_basis")
                           for m in a["source_families"])]
    report("every_action_carries_family_provenance", not missing_prov,
           "bad=%s" % (missing_prov or "none"))

    # ------------------------------------------------------------------ 7
    # The reconciliation equation must still hold arithmetically.
    # ------------------------------------------------------------------
    rec = reg.get("reconciliation") or {}
    report("reconciliation_equation_holds",
           rec.get("raw_followup_designated_source_families") == len(owned)
           and rec.get("final_followup_actions") == len(actions),
           "%s -> %s" % (rec.get("raw_followup_designated_source_families"),
                         rec.get("final_followup_actions")))

    sizes = rec.get("group_size_distribution") or {}
    report("group_size_distribution_sums_to_family_count",
           sum(int(k) * v for k, v in sizes.items()) == len(owned)
           and sum(sizes.values()) == len(actions),
           str(sizes))

    print("\n%d checks, %d FAIL" % (_checks, len(_failed)))
    if _failed:
        print("failed: %s" % ", ".join(sorted(set(_failed))))
    return 1 if _failed else 0


if __name__ == "__main__":
    sys.exit(main())
