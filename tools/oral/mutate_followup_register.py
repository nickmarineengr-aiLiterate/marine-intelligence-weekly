#!/usr/bin/env python3
"""
Mutation suite for the follow-up authorisation register guard.

WHY THE `intended_check` COLUMN MATTERS HERE MORE THAN USUAL
------------------------------------------------------------
`validate_followup_register.py` carries a check that re-derives the whole
register from its pinned sources and byte-compares. That check fires on
EVERY mutation, because every mutation changes bytes. A naive harness would
therefore report 12/12 caught while proving nothing about the other 31 checks.

So each mutation declares the check it is supposed to trip, and a mutation is
only CAUGHT when that named check is among the failures. A mutation that fails
the validator solely through the byte-currency check is reported as WEAK, which
is a defect in the guard, not a pass.

Restore is from this harness's own byte snapshot, by exact path. It never runs
`git checkout -- <file>`: that destroys uncommitted edits in the working tree.

Usage:
    python tools/oral/mutate_followup_register.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from oral_mutation import MutationSpec, preflight_or_die  # noqa: E402

TARGET = "tools/oral/oral_followup_register.json"
VALIDATOR = "tools/oral/validate_followup_register.py"

BYTE_CURRENCY_CHECK = "register_is_byte_current_with_its_generator"


# --------------------------------------------------------------------------
# mutation helpers -- all structural, because a literal string replace on JSON
# is exactly the "anchor has moved, replace silently no-ops" trap.
# --------------------------------------------------------------------------
def _load(text):
    return json.loads(text)


def _dump(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def jmut(mutation_id, fn, intended_check, why):
    def apply(text):
        obj = _load(text)
        fn(obj)
        return _dump(obj)

    spec = MutationSpec(mutation_id=mutation_id, target=TARGET, apply=apply,
                        intended_reason=why)
    return spec, intended_check


def _find(obj, fup_id):
    for a in obj["actions"]:
        if a["followup_id"] == fup_id:
            return a
    raise KeyError(fup_id)


# --------------------------------------------------------------------------
# A. an action silently disappears
def m_remove(obj):
    obj["actions"] = [a for a in obj["actions"] if a["followup_id"] != "FUP-020"]


# B. two actions claim the same identity
def m_dup_id(obj):
    _find(obj, "FUP-020")["followup_id"] = "FUP-021"


# C. two actions own the same source family
def m_dup_family(obj):
    _find(obj, "FUP-020")["source_family_ids"] = list(
        _find(obj, "FUP-021")["source_family_ids"])


# D. a source family is dropped from its action and is now orphaned
def m_drop_family(obj):
    a = _find(obj, "FUP-001")
    a["source_family_ids"] = a["source_family_ids"][:-1]


# E. the parent anchor is corrupted to one that does not exist
def m_bad_anchor(obj):
    a = _find(obj, "FUP-006")
    a["parent_anchor"] = "q9999"
    a["parent_canonical_id"] = "QB1_A#q9999"
    a["relationship_edge"]["parent_question"] = "QB1_A#q9999"
    a["relationship_edge"]["answer_home"] = "QB1_A#q9999"


# F. the pinned parent q-text no longer matches the live card, undeclared
def m_bad_qtext(obj):
    _find(obj, "FUP-006")["parent_qtext"] = "Something the card does not say."


# G. a relationship type outside the governed vocabulary
def m_bad_relationship(obj):
    _find(obj, "FUP-006")["relationship_type"] = "SUPPLEMENTARY_ASK"


# H. a verification class outside the governed vocabulary
def m_bad_verification(obj):
    _find(obj, "FUP-006")["verification_class"] = "NO_VERIFICATION_NEEDED"


# I. an ungoverned action is appended
def m_fake_action(obj):
    fake = json.loads(json.dumps(_find(obj, "FUP-035")))
    fake["followup_id"] = "FUP-036"
    fake["source_family_ids"] = ["GAP-9999"]
    fake["source_occurrence_ids"] = ["ASC-9999"]
    fake["relationship_edge"]["followup"] = "FUP-036"
    obj["actions"].append(fake)


# J. an occurrence identity is swapped for one the source never recorded
def m_bad_occurrence(obj):
    _find(obj, "FUP-006")["source_occurrence_ids"] = ["ASC-0001"]


# K. a follow-up quietly becomes a new card
def m_new_card(obj):
    _find(obj, "FUP-006")["creates_new_card"] = True


# L. provenance is stripped
def m_no_provenance(obj):
    obj["provenance"]["sources"] = {}


MUTATIONS = [
    jmut("A", m_remove, "action_count_matches_reconstructed_truth",
         "an authorised action is silently dropped from the register"),
    jmut("B", m_dup_id, "followup_ids_unique",
         "two records claim one follow-up identity"),
    jmut("C", m_dup_family, "no_duplicate_source_family_ownership",
         "one source family is owned by two actions"),
    jmut("D", m_drop_family, "every_source_family_accounted_exactly_once",
         "a source family is dropped and becomes an orphan"),
    jmut("E", m_bad_anchor, "every_parent_anchor_resolves",
         "the parent anchor no longer exists on the live page"),
    jmut("F", m_bad_qtext, "parent_qtext_matches_live_card_or_drift_declared",
         "the pinned parent q-text drifts without being declared"),
    jmut("G", m_bad_relationship, "relationship_type_is_governed",
         "an ungoverned relationship type is introduced"),
    jmut("H", m_bad_verification, "verification_class_is_governed",
         "an ungoverned verification class is introduced"),
    jmut("I", m_fake_action, "no_ungoverned_family_in_register",
         "an action with no upstream authorisation is appended"),
    jmut("J", m_bad_occurrence, "source_occurrence_ids_match_upstream",
         "a source occurrence identity is replaced with a foreign one"),
    jmut("K", m_new_card, "creates_new_card_false_unless_excepted",
         "a follow-up is switched to create a canonical card"),
    jmut("L", m_no_provenance, "register_provenance_present",
         "the provenance block is stripped from the register"),
]


FAILED_RE = re.compile(r"^failed:\s*(.+)$", re.M)


def run_validator():
    proc = subprocess.run(
        [sys.executable, VALIDATOR], cwd=str(REPO),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    out = proc.stdout.decode("utf-8", errors="replace")
    m = FAILED_RE.search(out)
    failed = set()
    if m:
        failed = {s.strip() for s in m.group(1).split(",") if s.strip()}
    return proc.returncode, failed, out


def main():
    path = REPO / TARGET
    specs = [s for s, _ in MUTATIONS]
    preflight_or_die(specs, root=REPO)

    snapshot = path.read_bytes()

    # A guard that is already red proves nothing about what a mutation did.
    rc, failed, out = run_validator()
    if rc != 0:
        print("BASELINE IS NOT GREEN -- refusing to launch")
        print(out[-2000:])
        return 1
    print("baseline: validator green\n")

    caught = weak = escapes = crashes = 0
    try:
        for spec, intended in MUTATIONS:
            text = path.read_text(encoding="utf-8")
            path.write_text(spec.apply(text), encoding="utf-8", newline="\n")
            try:
                rc, failed, out = run_validator()
            except Exception as exc:                      # noqa: BLE001
                crashes += 1
                print("%-2s CRASH  %s" % (spec.mutation_id, exc))
                continue
            finally:
                path.write_bytes(snapshot)

            if rc == 0:
                escapes += 1
                verdict = "ESCAPE"
            elif intended in failed:
                caught += 1
                verdict = "caught"
            else:
                weak += 1
                verdict = "WEAK"

            others = sorted(failed - {intended, BYTE_CURRENCY_CHECK})
            print("%-2s %-7s rc=%d  intended=%s%s"
                  % (spec.mutation_id, verdict, rc, intended,
                     ("  also=" + ",".join(others)) if others else ""))
    finally:
        path.write_bytes(snapshot)

    # Restore must be proved, not assumed.
    restored = path.read_bytes() == snapshot
    rc, _, _ = run_validator()
    print("\nrestore verified: %s   post-restore validator rc=%d"
          % (restored, rc))
    print("mutations=%d caught=%d weak=%d escapes=%d no-ops=0 crashes=%d"
          % (len(MUTATIONS), caught, weak, escapes, crashes))

    bad = escapes or crashes or weak or not restored or rc != 0
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
