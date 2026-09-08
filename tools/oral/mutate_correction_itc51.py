#!/usr/bin/env python3
"""Mutation suite for CORR-ITC51-20260908.

WHAT THIS SUITE HAS TO PROVE, beyond "a digest moved"
-----------------------------------------------------
The defect this correction closes was invisible to the gate that was watching
the very cards it lived in. That gate asked "does this card name ITC-Hulls?"
and the answer was yes at all fourteen defective sites, because the instrument
was right and only the clause number was wrong. So a suite that merely proves
"something changed" would reproduce the original escape exactly.

Every mutation below therefore names the PROPOSITION check it must trip.
`run_suite` refuses outright to accept a digest pin as a catch (DIGEST_PINS),
which is the rule that makes that non-negotiable.

THE TWO DIRECTIONS
------------------
  * REGRESSION (A, B, C, D, E, H) - a corrected site goes back to attributing
    automatic termination to Clause 4.2.
  * OVER-CORRECTION (F, F2, G) - the opposite failure, and the one a naive fix
    for this defect actually causes: a future session runs a blanket
    4.2 -> 5.1 substitution, or collapses the three instruments into one. A
    gate that only forbade 4.2 would be green on every one of these.

Both directions matter here more than usual, because the defect BEING fixed was
itself an over-correction of an over-correction: rounds 1-3 of Pass 2 removed a
true claim, round 4 restored it under the wrong clause number. F and G exist so
that the next swing of that pendulum is caught by a machine.

B AND H ARE THE SITE-SCOPING PROOF
----------------------------------
QB4_A carries three ITC citations in teaching text and QB4_C three. B corrupts
ONE of QB4_A's and H corrupts ONE of QB4_C's, leaving the others correct. A
page-scoped check - "cl. 5.1 appears on this page" - passes both, which is
precisely the state these files were in before the correction. If either
escapes, the gate is a presence check wearing a proposition's name.

I IS THE NON-VACUITY PROOF
--------------------------
It removes a target from the extractor's input entirely rather than corrupting
it. A census that reports success over a set it never read is the silent-failure
class this whole batch was convened to close, so it is tested directly.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import (                    # noqa: E402
    edit_json, run_suite, sub_in_file)

QB1_C = REPO / "meoclass1/QB1_C.html"
QB1_F = REPO / "meoclass1/QB1_F.html"
QB1_G = REPO / "meoclass1/QB1_G.html"
QB4_A = REPO / "meoclass1/QB4_A.html"
QB4_C = REPO / "meoclass1/QB4_C.html"
CS4A = REPO / "meoclass1/QB4_A_CheatSheet.html"
CS1K = REPO / "meoclass1/QB1_K_CheatSheet.html"
GOV = HERE / "qb_content_index_governed.json"
IDX = REPO / "meoclass1/qb_content_index.json"

PROBE = "validate_correction_itc51.py"

WATCHED = [QB1_C, QB1_F, QB1_G, QB4_A, QB4_C, CS4A, CS1K, GOV, IDX]


def _gov_note_back_to_4_2(d):
    """Put the 7 Sep note's attribution back to Clause 4.2, governed only."""
    for e in d["recently_updated"]:
        if "ITC-Hulls cl. 5.1 terminates hull cover automatically" in e.get("note", ""):
            e["note"] = e["note"].replace(
                "ITC-Hulls cl. 5.1 terminates hull cover automatically",
                "ITC-Hulls cl. 4.2 terminates hull cover automatically")
            return
    raise AssertionError("governed changelog anchor absent")


def _index_note_drifts(d):
    """Make the DERIVED index disagree with its governed source, and only that.

    The governed file is untouched, so nothing about the clause proposition is
    wrong here - the failure is purely that a generated surface no longer
    matches what generated it. That is its own defect class and it needs its
    own check.
    """
    for e in d["recently_updated"]:
        if e.get("date") == "2026-09-08":
            e["note"] = e["note"] + " (hand-edited on the derived surface)"
            return
    raise AssertionError("generated index anchor absent")


MUTATIONS = [
    # ---- REGRESSION -----------------------------------------------------
    ("A", "revert QB1_C's single citation to cl. 4.2",
     sub_in_file(QB1_C,
                 "Institute Time Clauses &ndash; Hulls (1/11/95) cl. 5.1 "
                 "terminates hull cover",
                 "Institute Time Clauses &ndash; Hulls (1/11/95) cl. 4.2 "
                 "terminates hull cover", count=1),
     "every_termination_site_cites_5_1"),

    ("B", "revert ONE of QB4_A's three sites, leaving two correct",
     sub_in_file(QB4_A,
                 "ITC-Hulls (1/11/95) cl. 5.1 terminates hull cover "
                 "automatically on suspension or withdrawal",
                 "ITC-Hulls (1/11/95) cl. 4.2 terminates hull cover "
                 "automatically on suspension or withdrawal", count=1),
     "every_termination_site_cites_5_1"),

    ("H", "revert ONE of QB4_C's three sites, leaving two correct",
     sub_in_file(QB4_C,
                 "under ITC-Hulls (1/11/95) cl. 5.1 hull cover terminates "
                 "automatically",
                 "under ITC-Hulls (1/11/95) cl. 4.2 hull cover terminates "
                 "automatically", count=1),
     "every_termination_site_cites_5_1"),

    ("C", "revert the QB4_A cheat sheet, the surface with no q-card digest",
     sub_in_file(CS4A,
                 "ITC-Hulls (1/11/95) cl. 5.1, deferred to next port",
                 "ITC-Hulls (1/11/95) cl. 4.2, deferred to next port", count=1),
     "cheatsheet_agrees:QB4_A_CheatSheet.html"),

    ("D", "revert the GOVERNED changelog only",
     edit_json(GOV, _gov_note_back_to_4_2),
     "governed_changelog_no_4_2_termination"),

    ("E", "governed source correct, DERIVED index hand-edited and stale",
     edit_json(IDX, _index_note_drifts),
     "generated_index_matches_governed_changelog"),

    # ---- OVER-CORRECTION ------------------------------------------------
    ("F", "strip the duty/breach mechanism from a stamp, leaving a bare 4.2",
     sub_in_file(QB1_C,
                 "discharge from liability for breach of the Clause 4.1 duty "
                 "to maintain class",
                 "same automatic termination of cover", count=1),
     "clause_4_2_survives_only_as_duty_breach"),

    ("F2", "blanket 4.2 -> 5.1 inside a stamp, deleting what 4.2 IS",
     sub_in_file(QB1_G,
                 "Clause 4.2. Clause 4.2 is a different mechanism",
                 "Clause 5.1. Clause 5.1 is the same mechanism", count=1),
     "clause_4_2_survives_only_as_duty_breach"),

    ("G", "collapse the layers: attribute hull termination to PR1C",
     sub_in_file(QB1_C,
                 "cite the policy rather than PR1C: Institute Time Clauses",
                 "cite PR1C, which terminates hull cover automatically, and "
                 "Institute Time Clauses", count=1),
     "pr1c_not_rewritten_as_itc:QB1_C.html"),

    ("G2", "delete QB4_A's P&I warranty, folding P&I into the hull policy",
     sub_in_file(QB4_A,
                 "seaworthy and in class&quot; is a fundamental warranty under "
                 "standard P&amp;I Club Rules",
                 "seaworthy and in class&quot; is a term of the hull policy",
                 count=1),
     "qb4a_keeps_pandi_warranty_as_pandi"),

    ("J", "corrupt the already-correct seed reg-box the review read from",
     sub_in_file(QB1_F,
                 "Institute Time Clauses – Hulls 1/11/95, cl. 4 and 5.1",
                 "Institute Time Clauses – Hulls 1/11/95, cl. 4.2",
                 count=1),
     "qb1f_regbox_keeps_cl_4_and_5_1"),

    # ---- NON-VACUITY ----------------------------------------------------
    ("I", "remove a target from the census input entirely",
     sub_in_file(CS1K,
                 "under ITC-Hulls cl. 5.1",
                 "under the standard hull policy", count=1),
     "census_exact:QB1_K_CheatSheet.html"),

    ("I2", "remove a card's correction stamp, emptying the stamp census",
     sub_in_file(QB4_C,
                 "(ITC-Hulls clause correction)",
                 "(routine edit)", count=1),
     "stamp_census_non_vacuous"),
]


def main() -> int:
    return run_suite("CORR-ITC51-20260908 mutation suite", PROBE,
                     MUTATIONS, WATCHED)


if __name__ == "__main__":
    sys.exit(main())
