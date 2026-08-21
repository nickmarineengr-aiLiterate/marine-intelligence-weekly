#!/usr/bin/env python3
"""Generate the authoritative Oral follow-up authorisation register.

WHY THIS EXISTS
---------------
The 35 follow-up actions FUP-001..FUP-035 were produced on a research branch and
never reached `main`. A repo-wide grep of the working tree therefore found zero
FUP identifiers, and the workload survived only in handoff prose. That is the
same defect class that was closed twice already (the release sequence living in
scratch history; a post-release correction shipping without governed
authorisation). This generator re-derives the register from the committed
research records and writes it to `main` so follow-up production starts from a
committed source of truth.

WHAT IT IS NOT
--------------
It is an AUTHORISATION register, not a batch production manifest. It records
what is authorised for future processing. Each production batch (F1, F2, ...)
still writes its own `batch_f*_manifest.json` recording what was actually
implemented, validated against `oral_manifest.py` like every other batch.

SOURCES (pinned by blob SHA, not by branch tip)
-----------------------------------------------
Branches move; blobs do not. Every source is addressed by its content hash, so
the register cannot silently re-derive against a different record.

  FINAL_ORAL_PRODUCTION_AUTHORIZATION.json   the action/family authorisation
  FINAL_REMAINING_ORAL_PRODUCTION_DECISIONS.json  the per-family evidence
  FINAL_ORAL_ENRICHMENT_CONSOLIDATION.json   follow-up/enrichment colocation

Usage:
    python tools/oral/build_followup_register.py            # write the register
    python tools/oral/build_followup_register.py --check    # byte-compare only
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import oral_lib  # noqa: E402

OUT = REPO / "tools" / "oral" / "oral_followup_register.json"

REGISTER_VERSION = "1.0"
GENERATED_BY = "tools/oral/build_followup_register.py"

# --------------------------------------------------------------------------
# Pinned sources. A blob SHA is the whole provenance claim: it identifies the
# exact bytes, independent of which branch happens to carry them today.
# --------------------------------------------------------------------------
SOURCES = {
    "authorisation": {
        "blob": "b3f3a972c14daef66b5809c243f5d98bde1e80a6",
        "path": "meoclass1/oral-intelligence/examiner-audit/"
                "FINAL_ORAL_PRODUCTION_AUTHORIZATION.json",
        "seen_on_refs": [
            "origin/review/oral-final-gap-decision-laptop",
            "origin/research/oral-final-enrichment-consolidation",
        ],
        "role": "follow-up families and the 35 grouped insertion actions",
    },
    "decisions": {
        "blob": "5170fbe4c562b150ae4ba0cd5aa09712d83ae5d9",
        "path": "meoclass1/oral-intelligence/examiner-audit/"
                "FINAL_REMAINING_ORAL_PRODUCTION_DECISIONS.json",
        "seen_on_refs": ["origin/review/oral-final-gap-decision-laptop"],
        "role": "per-family evidence: occurrences, decision basis, coverage",
    },
    "enrichment": {
        "blob": "d4571ac3071348d2ddfb04ee69957b2cb86788cd",
        "path": "meoclass1/oral-intelligence/examiner-audit/"
                "FINAL_ORAL_ENRICHMENT_CONSOLIDATION.json",
        "seen_on_refs": ["origin/research/oral-final-enrichment-consolidation"],
        "role": "follow-up / enrichment colocation on a shared parent card",
    },
}

FOLLOWUP_DISPOSITION = "FOLLOWUP_ONLY"
FOLLOWUP_KIND = "FOLLOWUP_INSERTION"

BASIS_HAND = "hand adjudication against current answer bodies"
BASIS_RULE = "rule: material partial dispositioned by recurrence"

# Governed relationship vocabulary. Single-sourced from validate_phase2.py so a
# type can never be added here without the phase-2 gate accepting it too.
from validate_phase2 import RELATIONSHIP_TYPES  # noqa: E402

# Verification vocabulary as used by the enrichment consolidation, plus one
# register-only value. The follow-up families carry an EMPTY
# `technical_verification_scope` in every source record, so assigning any
# governed class here would be invention. The batch that produces a follow-up
# assigns the real class; until then the register says so out loud.
GOVERNED_VERIFICATION_CLASSES = {
    "CLASS_RULE_VERIFY_REQUIRED",
    "CURRENT_REG_VERIFY_REQUIRED",
    "EXISTING_VERIFIED_MIWCORPUS_SUFFICIENT",
    "OEM_VERIFY_REQUIRED",
    "PRIMARY_AUTHORITY_REQUIRED",
    "TECHNICAL_REASONING_ONLY",
}
VERIFICATION_PENDING = "UNCLASSIFIED_PENDING_BATCH_SCOPING"
VERIFICATION_CLASSES = GOVERNED_VERIFICATION_CLASSES | {VERIFICATION_PENDING}

TARGET_CONFIDENCES = {"HIGH", "MEDIUM", "LOW"}
TARGET_REVIEW_STATUSES = {
    "CONFIRMED",
    "REQUIRES_LIVE_ADJUDICATION",
    "RETARGET_REQUIRED",
    "METADATA_ONLY_CANDIDATE",
}
STATUSES = {"AUTHORISED_NOT_STARTED", "IN_BATCH", "PRODUCED", "WITHDRAWN"}
PRIORITIES = {"F-P1", "F-P2", "F-P3"}
STRUCTURAL_STATES = {
    "TARGET_RESOLVES",
    "TARGET_MISSING",
    "TARGET_DRIFTED",
    "TARGET_REVIEW_REQUIRED",
}

# Coverage at or above this band means the parent answer already carries most of
# the ask, which is what makes it a plausible home for a follow-up limb. Taken
# from the observed distribution of `current_best_answer_coverage` across the 39
# families (min 0.235, max 0.700).
STRONG_COVERAGE = 0.60

# --------------------------------------------------------------------------
# Currentness and authority hints. These are HINTS derived from the candidate's
# own reported ask - never a claim about what the law says.
# --------------------------------------------------------------------------
CURRENTNESS_PATTERNS = [
    (r"\b(19|20)\d{2}\b", "explicit year"),
    (r"\bamendment", "amendment"),
    (r"\b(coming|came|come)\s+in(to)?\s+force\b", "entry into force"),
    (r"\bnew\b", "novelty word"),
    (r"\blatest\b", "novelty word"),
    (r"\brecent", "novelty word"),
    (r"\bupcoming\b", "novelty word"),
    (r"\bsecretary[- ]general\b", "sitting officeholder"),
    (r"\bthis year\b", "relative date"),
    (r"\bcurrent\b", "relative date"),
]

AUTHORITY_TOKENS = [
    "SOLAS", "MARPOL", "STCW", "MLC", "ISM", "ISPS", "FSS", "LSA", "IMDG",
    "IBC", "IGC", "BWM", "FAL", "COLREG", "AFS", "OPRC", "CLC", "SUA",
    "Load Line", "Tonnage", "Merchant Shipping", "MS Act", "P&I", "ITC",
    "York-Antwerp", "Hong Kong", "Polar Code", "ILO", "ICC", "PSC", "CIC",
    "MSI", "DGS", "DG Shipping", "IACS", "MEPC", "MSC", "IMO",
]


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def read_blob(sha):
    """Read a pinned blob. Fails CLOSED: an unavailable source is fatal."""
    try:
        raw = subprocess.run(
            ["git", "cat-file", "blob", sha],
            cwd=str(REPO), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=True,
        ).stdout
    except (subprocess.CalledProcessError, OSError) as exc:
        raise SystemExit(
            "FATAL: pinned source blob %s is unavailable (%s).\n"
            "Run `git fetch origin --prune` - the research refs carry it."
            % (sha, exc)
        )
    return json.loads(raw.decode("utf-8"))


def currentness(ask):
    hits = []
    low = ask.lower()
    for pat, label in CURRENTNESS_PATTERNS:
        if re.search(pat, low):
            hits.append(label)
    # stable, de-duplicated, deterministic
    return sorted(set(hits))


def authority_hints(text):
    out = []
    for tok in AUTHORITY_TOKENS:
        if re.search(r"(?<![A-Za-z])" + re.escape(tok) + r"(?![A-Za-z])",
                     text, re.I):
            out.append(tok)
    return sorted(set(out))


def relationship_for(reason, basis):
    """Classify from the adjudicator's own words, never from the ask text.

    A rule-dispositioned family had its target chosen by a coverage score, so
    the only honest governed value is TOPIC_INFERENCE_ONLY - the relationship
    was inferred from topical proximity and nothing else.
    """
    low = (reason or "").lower()
    if basis == BASIS_HAND:
        if "expected detail" in low or "expected-detail" in low:
            return "EXPECTED_DETAIL"
        if "follow-up" in low or "follow up" in low:
            return "FOLLOW_UP"
        return "FOLLOW_UP"
    return "TOPIC_INFERENCE_ONLY"


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------
def build():
    auth = read_blob(SOURCES["authorisation"]["blob"])
    dec = read_blob(SOURCES["decisions"]["blob"])
    enr = read_blob(SOURCES["enrichment"]["blob"])

    # ---- representation 1: families dispositioned FOLLOWUP_ONLY -----------
    fam_auth = [f for f in auth["families"]
                if f["adjudicated_decision"] == FOLLOWUP_DISPOSITION]
    # ---- representation 2: the grouped production actions -----------------
    act_auth = [a for a in auth["production_actions"]
                if a["kind"] == FOLLOWUP_KIND]
    # ---- representation 3: the per-family evidence record -----------------
    dec_by_id = {f["family_id"]: f for f in dec["families"]}
    fam_dec = [f for f in dec["families"] if f["decision"] == FOLLOWUP_DISPOSITION]

    # Agreement across the three representations is a precondition, not a
    # result. Disagreement means the register cannot be trusted at all.
    if {f["family_id"] for f in fam_auth} != {f["family_id"] for f in fam_dec}:
        raise SystemExit("FATAL: follow-up family sets disagree between sources")

    # ---- independent regrouping ------------------------------------------
    # Do NOT read the committed production_action_id. Re-derive it: group the
    # families by parent target and number the groups in sorted target order,
    # then compare with what was committed. That is what makes this a
    # reconstruction rather than a copy.
    groups = defaultdict(list)
    for f in sorted(fam_auth, key=lambda x: x["family_id"]):
        groups[f["target"]].append(f["family_id"])

    derived = {}
    for i, tgt in enumerate(sorted(groups), 1):
        derived["FUP-%03d" % i] = tgt

    committed = {a["production_action_id"]: a["target"] for a in act_auth}
    if derived != committed:
        raise SystemExit(
            "FATAL: independently derived FUP numbering does not match the "
            "committed identifiers. Derived %d, committed %d."
            % (len(derived), len(committed))
        )

    # ---- live corpus, for the structural target check ---------------------
    inv = oral_lib.build_inventory()
    by_qid = {r["canonical_question_id"]: r for r in inv}
    anchors = oral_lib.all_anchors()

    # ---- colocation (representation 4) ------------------------------------
    coloc = defaultdict(list)
    for c in enr.get("followup_colocation", []):
        for fid in c["followup_family_ids"]:
            coloc[fid].append(c["enrichment_action_id"])

    actions = []
    for fup_id in sorted(derived):
        target = derived[fup_id]
        fname, anchor = target.split("#", 1)
        page = fname + ".html"
        members = groups[target]

        # ---- structural check against the LIVE corpus ---------------------
        if page not in anchors:
            structural = "TARGET_MISSING"
            parent_qtext = None
        elif target not in by_qid:
            structural = ("TARGET_MISSING" if anchor not in anchors[page]
                          else "TARGET_REVIEW_REQUIRED")
            parent_qtext = None
        else:
            parent_qtext = by_qid[target]["question_text"]
            structural = ("TARGET_RESOLVES" if parent_qtext.strip()
                          else "TARGET_REVIEW_REQUIRED")

        src_families = []
        for fid in members:
            fa = next(f for f in fam_auth if f["family_id"] == fid)
            fd = dec_by_id[fid]
            basis = fd["decision_basis"]
            # Score drift: the coverage score that originally chose this parent
            # no longer chooses it. Only meaningful for rule-dispositioned
            # families - a hand adjudication overrides the score by design.
            drifted = (basis == BASIS_RULE
                       and fd["decision_target"] != fd["current_best_answer_question_id"])
            src_families.append({
                "source_family_id": fid,
                "upstream_source_family_id": fd["source_family_id"],
                "source_occurrence_ids": list(fa["source_occurrence_ids"]),
                "occurrence_count": fd["occurrence_count"],
                "examiners": list(fa["examiner_ids"]),
                "original_ask": fd["ask"],
                "raw_ask_variants": list(fd["raw_ask_variants"]),
                "topics": list(fd["topics"]),
                "source_pages": list(fd["source_pages"]),
                "governed_gap_kind": fd["governed_gap_kind"],
                "governed_priority": fd["governed_priority"],
                "notes_support": fd["notes_support"],
                "notes_units": list(fd["notes_units"]),
                "decision_basis": basis,
                "decision_reason": fd["decision_reason"],
                "best_answer_coverage": fd["current_best_answer_coverage"],
                "current_best_answer_question_id": fd["current_best_answer_question_id"],
                "target_score_drifted": drifted,
                "relationship_type": relationship_for(fd["decision_reason"], basis),
                "colocated_enrichment_actions": sorted(coloc.get(fid, [])),
            })

        hand = all(m["decision_basis"] == BASIS_HAND for m in src_families)
        any_drift = any(m["target_score_drifted"] for m in src_families)
        min_cov = min(m["best_answer_coverage"] for m in src_families)

        # ---- target confidence -------------------------------------------
        if hand:
            confidence = "HIGH"
        elif any_drift:
            confidence = "LOW"
        elif min_cov >= STRONG_COVERAGE:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        # ---- target review status ----------------------------------------
        metadata_only = any(
            "not an answer" in (m["decision_reason"] or "").lower()
            for m in src_families)
        if metadata_only:
            review = "METADATA_ONLY_CANDIDATE"
        elif hand:
            review = "CONFIRMED"
        elif any_drift:
            review = "RETARGET_REQUIRED"
        else:
            review = "REQUIRES_LIVE_ADJUDICATION"

        priority = {"HIGH": "F-P1", "MEDIUM": "F-P2", "LOW": "F-P3"}[confidence]

        rels = sorted({m["relationship_type"] for m in src_families})
        if len(rels) != 1:
            raise SystemExit(
                "FATAL: %s mixes relationship types %s - the register has no "
                "governed value for a mixed group." % (fup_id, rels)
            )

        asks = [m["original_ask"] for m in src_families]
        cur = sorted({t for m in src_families for t in currentness(m["original_ask"])})
        hints = authority_hints(" ".join(asks) + " " + (parent_qtext or ""))

        caution = []
        if any_drift:
            caution.append(
                "The coverage score that selected this parent no longer selects "
                "it; adjudicate the home against live answer bodies before "
                "authoring.")
        if confidence != "HIGH":
            caution.append(
                "Target was chosen by a coverage score, not by hand "
                "adjudication.")
        colo = sorted({a for m in src_families
                       for a in m["colocated_enrichment_actions"]})
        if colo:
            caution.append(
                "Parent card was already edited by shipped enrichment %s; read "
                "the live card before adding a limb." % ", ".join(colo))
        if metadata_only:
            caution.append(
                "Source states this is not an answer - it may belong as a trap "
                "or expected-detail marker rather than a Q&A limb.")

        actions.append({
            "followup_id": fup_id,
            "kind": FOLLOWUP_KIND,
            "status": "AUTHORISED_NOT_STARTED",
            "priority": priority,
            "batch": None,
            "source_family_ids": list(members),
            "source_occurrence_ids": sorted(
                {o for m in src_families for o in m["source_occurrence_ids"]}),
            "examiners": sorted({e for m in src_families for e in m["examiners"]}),
            "original_asks": asks,
            "parent_canonical_id": target,
            "parent_file": page,
            "parent_anchor": anchor,
            "parent_qtext": parent_qtext,
            "relationship_type": rels[0],
            "relationship_edge": {
                "parent_question": target,
                "edge": "EXAMINER_FOLLOW_UP",
                "followup": fup_id,
                "answer_home": target,
            },
            "authorised_followup_limb": {
                "note": "The authorised limb is the candidate-reported ask "
                        "below, to be answered on the parent card. No answer "
                        "text is authorised here; content is authored in the "
                        "production batch.",
                "asks": asks,
            },
            "verification_class": VERIFICATION_PENDING,
            "currentness_required": bool(cur),
            "currentness_triggers": cur,
            "primary_authority_hint": hints,
            "target_confidence": confidence,
            "target_review_status": review,
            "target_structural_check": structural,
            "creates_new_card": False,
            "colocated_enrichment_actions": colo,
            "caution": caution,
            "source_families": src_families,
        })

    # ---- reconciliation proof --------------------------------------------
    sizes = Counter(len(groups[t]) for t in groups)
    reconciliation = {
        "raw_followup_designated_source_families": len(fam_auth),
        "grouping_rule": "one action per parent canonical question id; "
                         "families sharing a parent card are one insertion",
        "group_size_distribution": {str(k): sizes[k] for k in sorted(sizes)},
        "multi_family_groups": [
            {"followup_id": fid, "target": derived[fid],
             "source_family_ids": groups[derived[fid]]}
            for fid in sorted(derived) if len(groups[derived[fid]]) > 1
        ],
        "final_followup_actions": len(derived),
        "equation": "%d source families -> %d parent cards -> %d actions" % (
            len(fam_auth), len(groups), len(derived)),
        "id_assignment_rule": "FUP-NNN in ascending lexicographic order of the "
                              "parent canonical question id",
        "independently_regenerated": True,
        "matches_committed_identifiers": True,
        "representations_cross_checked": [
            "authorisation.families[] where adjudicated_decision=FOLLOWUP_ONLY",
            "authorisation.production_actions[] where kind=FOLLOWUP_INSERTION",
            "decisions.families[] where decision=FOLLOWUP_ONLY",
            "enrichment.followup_colocation[]",
        ],
        "source_headline_counts": {
            "FOLLOWUP_SOURCE_FAMILIES": auth["authorised"]["FOLLOWUP_SOURCE_FAMILIES"],
            "AUTHORISED_FOLLOWUP_INSERTION_ACTIONS":
                auth["authorised"]["AUTHORISED_FOLLOWUP_INSERTION_ACTIONS"],
            "FOLLOWUP_INSERTIONS": auth["workload"]["FOLLOWUP_INSERTIONS"],
        },
    }

    reg = {
        "register_version": REGISTER_VERSION,
        "generated_by": GENERATED_BY,
        "record_class": "AUTHORISATION_REGISTER",
        "note": "Authoritative register of the Oral examiner follow-up actions "
                "authorised for future production. This says WHAT is "
                "authorised. Each production batch writes its own "
                "batch_f*_manifest.json saying what was IMPLEMENTED. The two "
                "must never be collapsed.",
        "provenance": {
            "sources": SOURCES,
            "derivation": "Families dispositioned FOLLOWUP_ONLY are grouped by "
                          "parent canonical question id; identifiers are "
                          "re-derived and compared against the committed ones.",
            "content_authored_here": False,
        },
        "vocabularies": {
            "relationship_type": sorted(RELATIONSHIP_TYPES),
            "verification_class": sorted(VERIFICATION_CLASSES),
            "target_confidence": sorted(TARGET_CONFIDENCES),
            "target_review_status": sorted(TARGET_REVIEW_STATUSES),
            "status": sorted(STATUSES),
            "priority": sorted(PRIORITIES),
            "target_structural_check": sorted(STRUCTURAL_STATES),
        },
        "confidence_model": {
            "HIGH": "decision_basis is hand adjudication against current "
                    "answer bodies - a person reasoned about this parent card",
            "MEDIUM": "target chosen by coverage score, score still selects it, "
                      "and best-answer coverage is at or above %.2f" % STRONG_COVERAGE,
            "LOW": "target chosen by coverage score and either the score no "
                   "longer selects it, or coverage is below %.2f" % STRONG_COVERAGE,
            "caution": "A LAPTOP_CONFIRMED follow-up disposition confirms the "
                       "DISPOSITION, not the target. All 39 families are "
                       "LAPTOP_CONFIRMED; only 4 had their parent card chosen "
                       "by hand.",
        },
        "live_corpus_at_generation": {
            "canonical_questions": len(inv),
            "question_bearing_files": len({r["file"] for r in inv}),
        },
        "reconciliation": reconciliation,
        "summary": {
            "total_actions": len(actions),
            "by_priority": dict(sorted(Counter(
                a["priority"] for a in actions).items())),
            "by_relationship_type": dict(sorted(Counter(
                a["relationship_type"] for a in actions).items())),
            "by_target_confidence": dict(sorted(Counter(
                a["target_confidence"] for a in actions).items())),
            "by_target_review_status": dict(sorted(Counter(
                a["target_review_status"] for a in actions).items())),
            "by_target_structural_check": dict(sorted(Counter(
                a["target_structural_check"] for a in actions).items())),
            "by_status": dict(sorted(Counter(a["status"] for a in actions).items())),
            "parent_files": dict(sorted(Counter(
                a["parent_file"] for a in actions).items())),
            "currentness_required": sum(1 for a in actions
                                        if a["currentness_required"]),
            "creates_new_card": sum(1 for a in actions if a["creates_new_card"]),
        },
        "actions": actions,
    }
    return reg


def serialise(reg):
    return json.dumps(reg, indent=2, ensure_ascii=False) + "\n"


def main():
    check = "--check" in sys.argv
    reg = build()
    text = serialise(reg)

    if check:
        if not OUT.exists():
            print("STALE: %s does not exist" % OUT.name)
            return 3
        live = OUT.read_text(encoding="utf-8")
        if live != text:
            print("STALE: %s does not match a fresh build" % OUT.name)
            return 3
        print("CURRENT: %s is byte-identical to a fresh build" % OUT.name)
        return 0

    OUT.write_text(text, encoding="utf-8", newline="\n")
    r = reg["reconciliation"]
    print("wrote %s" % OUT.relative_to(REPO))
    print("  %s" % r["equation"])
    print("  group sizes: %s" % r["group_size_distribution"])
    print("  identifiers independently regenerated and matched: %s"
          % r["matches_committed_identifiers"])
    for k, v in reg["summary"].items():
        print("  %-28s %s" % (k, v))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
