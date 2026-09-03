#!/usr/bin/env python3
"""
Mutation suite for CORR-ISM-SPARES-20260902  (QB5_I#q8).

`validate_correction_ismspares.py` reports 38 green checks. Green output on its
own is indistinguishable from a validator that reads nothing, so every
proposition the correction rests on is attacked here and each mutation must
trip the check that OWNS that proposition -- never the digest pin, which fires
on any byte change at all (enforced by oral_content_mutation.DIGEST_PINS).

MUTATION J IS THE ONE THAT MATTERS MOST.
It reintroduces the corrected-away wording in the page-level CHEAT SHEET only,
leaving the card itself correct. That is precisely the shape of known_traps
entry 51 -- a repair that fixes the prose and leaves the mnemonic -- and it is
how this very card carried "the critical-spares list is DERIVED from the
critical-equipment list" in its memory card for a week after the body was
fixed. A card-scoped guard cannot see it; only the page-wide checks can.
"""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import (                    # noqa: E402
    edit_json, run_suite, sub_in_file)

CARD = REPO / "meoclass1/QB5_I.html"
MANIFEST = HERE / "correction_corr_ism_spares_20260902_manifest.json"
PROBE = "validate_correction_ismspares.py"

MUTATIONS = [
    ("A", "reinstate the ISM 10.3 'drives the list' claim in the body",
     sub_in_file(CARD,
                 "ISM 10.3 makes the company identify the equipment",
                 "The critical-equipment list under ISM 10.3 drives the "
                 "critical-spares list; ISM 10.3 makes the company identify "
                 "the equipment"),
     "no_derivation_claim"),

    ("B", "reinstate the automatic ISM 9 non-conformity in the 60-second answer",
     sub_in_file(CARD,
                 "If a safety-critical spare cannot be obtained, that is not a "
                 "stores problem:",
                 "If a critical spare cannot be obtained, that is not a stores "
                 "problem &mdash; I raise it as a non-conformity under ISM 9 "
                 "and it goes on the record. Also:"),
     "no_automatic_ism9"),

    ("C", "re-file the reliability measures back under ISM 10.4",
     sub_in_file(CARD,
                 "Integration of the 10.2 inspections and the 10.3 reliability "
                 "measures into the ship&rsquo;s operational maintenance routine",
                 "Measures to promote reliability of that equipment, including "
                 "regular testing of stand-by arrangements"),
     "ism_10_4_regbox_is_integration"),

    ("D", "delete the ISM 10.3 stand-by testing limb everywhere",
     sub_in_file(CARD, "regular testing of stand-by arrangements",
                 "periodic proving of equipment"),
     "ism_10_3_standby_testing_limb"),

    ("E", "remove the 'informed by' hierarchy from the body",
     sub_in_file(CARD,
                 "the critical-spares list is <em>informed by</em> the 10.3",
                 "the critical-spares list follows the 10.3"),
     "spares_list_is_informed_not_derived"),

    ("F", "delete the 'not prescribed by the ISM Code' qualifier",
     sub_in_file(CARD,
                 "<em>None of this arithmetic is prescribed by the ISM "
                 "Code.</em> ",
                 ""),
     "stock_arithmetic_not_prescribed_by_code"),

    ("G", "make every ISM 9 limb unconditional again",
     sub_in_file(CARD, "definition of a non-conformity",
                 "view of the matter"),
     "ism9_conditional_on_sms_definition"),

    ("H", "corrupt the SOLAS II-2/10.3.3 spare-charge ceiling",
     sub_in_file(CARD, "<strong>not more than 60</strong> in total",
                 "<strong>not more than 40</strong> in total"),
     "solas_ii2_10_3_3_intact"),

    ("I", "strip the leadership limb from the CE Oral Tip",
     sub_in_file(CARD,
                 "&ldquo;I own the standard, the second engineer owns the "
                 "record, I verify by sampling&rdquo;",
                 "&ldquo;the second engineer runs stores&rdquo;"),
     "leadership_limb_preserved"),

    ("J", "reinstate the defect in the CHEAT SHEET only, card left correct",
     sub_in_file(CARD,
                 "so the list is INFORMED by 10.3, not written by it",
                 "so the critical-spares list is DERIVED from the "
                 "critical-equipment list"),
     "no_derivation_claim_page_wide"),

    ("K", "drop the supersession claim on H6's pin from the record",
     edit_json(MANIFEST,
               lambda d: d["cards"][0].pop("supersedes", None)),
     "supersedes_h6_pin"),
]

WATCHED = [CARD, MANIFEST]

if __name__ == "__main__":
    raise SystemExit(run_suite(
        "mutation suite: CORR-ISM-SPARES-20260902 (QB5_I#q8)",
        PROBE, MUTATIONS, WATCHED))
