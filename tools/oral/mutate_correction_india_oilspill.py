#!/usr/bin/env python3
"""Mutation suite for CORR-INDIA-OILSPILL-REGULATORY-AUDIT-20260917.

Every mutation names the PROPOSITION check it must trip; the shared harness
refuses a digest pin as a catch. Probes only validate_correction_india_oilspill.py.

Per proposition, three directions:

  REGRESSION     the shipped defect comes back at one corrected site.
  CORPUS         the defect appears on a page this record never touched, so a
                 site-only gate cannot pass.
  OVER-CORRECTION true teaching beside the false claim is wiped out by a
                 blanket fix (QB3_J's capability trap, QB9_D's "India has not
                 ratified", Q4's Merchant Shipping Act 2025 citation, the SOLAS
                 limb of Q18).

  A_TIER  A1-A5   B_OPRC_DATE  B1-B2   C_BUNKERS_STATUS  C1-C6
  D_PANS  D1-D6   RECORD  R1-R5        NON-VACUITY  N1
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import edit_json, run_suite, sub_in_file  # noqa: E402

QB = REPO / "meoclass1"
GATED = QB / "QB1_A.html"
TWIN = REPO / "SQ/QB1_A.html"
QB9A = QB / "QB9_A.html"
QB3J = QB / "QB3_J.html"
QB9D = QB / "QB9_D.html"
QB9E = QB / "QB9_E.html"
CHEAT = QB / "QB1_B_CheatSheet.html"
NOTES = QB / "oralnotes/simon-notes-p3.html"
NOTES7 = QB / "oralnotes/simon-notes-p7.html"
TRAPS = QB / "known_traps.md"
GOV = HERE / "qb_content_index_governed.json"
IDX = QB / "qb_content_index.json"
REGISTRY = REPO / "docs/sources/MIW_SOURCE_REGISTRY.json"

PROBE = "validate_correction_india_oilspill.py"
WATCHED = [GATED, TWIN, QB9A, QB3J, QB9D, QB9E, CHEAT, NOTES, NOTES7, TRAPS, GOV, IDX, REGISTRY]


def _gov_note_drops_not_a_party(d):
    for e in d["recently_updated"]:
        if e.get("date") == "2026-09-17":
            assert "not a Party" in e["note"]
            e["note"] = e["note"].replace("not a Party", "a Party")
            return
    raise AssertionError("governed 2026-09-17 note absent")


def _index_note_drifts(d):
    for e in d["recently_updated"]:
        if e.get("date") == "2026-09-17":
            e["note"] = e["note"] + " (hand-edited on the derived surface)"
            return
    raise AssertionError("generated index anchor absent")


def _plan_row_claims_retrieved(d):
    for s in d["sources"]:
        if s["source_id"] == "SRC-ICG-NOSDCP-2015-PLAN":
            s["access_status"] = "RETRIEVED"
            return
    raise AssertionError("SRC-ICG-NOSDCP-2015-PLAN absent")


MUTATIONS = [
    # ================================================================ A_TIER
    ("A1", "QB9_A Q8: Tier 1 <700 tonnes reinstated",
     sub_in_file(QB9A, "<li><em>Tier 1 (Local):</em> within the responsible agency's own resources",
                 "<li><em>Tier 1 (Local):</em> small spills (&lt;700 tonnes) within the responsible agency's own "
                 "resources", count=1),
     "A_qb9a_q8_no_tier_band_taught"),
    ("A2", "notes n5: Tier 2 up to 10,000 MT reinstated",
     sub_in_file(NOTES, "Tier 2: beyond local capability",
                 "Tier 2: Regional incidents up to <strong>10,000 MT</strong>, beyond local capability", count=1),
     "A_notes_n5_no_tier_band_taught"),
    ("A3", "untouched page (QB3_J Q5) re-infected with the bands",
     sub_in_file(QB3J, "<li><strong>Tiered response:</strong> Tier I/II/III by scale and capability.",
                 "<li><strong>Tiered response:</strong> Tier I up to 700 tonnes, Tier II up to 10,000 tonnes, "
                 "Tier III above 10,000 tonnes.", count=1),
     "A_corpus_no_tier_tonnage_band_taught"),
    ("A4", "over-correction: QB3_J's capability trap flattened",
     sub_in_file(QB3J, "not fixed spill-size tonnage bands", "and fixed spill-size tonnage bands", count=1),
     "A_overcorrection_qb3j_capability_trap_survives"),
    ("A5", "the 700-tonne stocking example relabelled a definition",
     sub_in_file(QB9A, "700-tonne figure is a dispersant-stocking example of risk exposure, not a tier definition",
                 "700-tonne figure is the Tier 1 limit", count=1),
     "A_qb9a_q8_stocking_example_named_as_example"),

    # ================================================================ B_OPRC_DATE
    ("B1", "notes reg-box: 'India ratified/acceded 1993' restored",
     sub_in_file(NOTES, "India acceded on <strong>17 November 1997</strong>, in force for India "
                        "<strong>17 February 1998</strong> (IMO Status of Treaties).",
                 "India ratified/acceded 1993 (verify exact year before quoting).", count=1),
     "B_notes_accession_date_stated"),
    ("B2", "untouched page (QB3_J) says India became party in 1993",
     sub_in_file(QB3J, "It is India's implementation of its obligations as a party to <strong>OPRC 1990</strong>",
                 "It is India's implementation of its obligations as a party to <strong>OPRC 1990</strong> "
                 "since 1993", count=1),
     "B_corpus_no_wrong_india_oprc_date"),

    # ================================================================ C_BUNKERS_STATUS
    ("C1", "Q4 reg-box back to 'domestic implementation of the Bunker Convention' (gated)",
     sub_in_file(GATED, "India is not a Party to the Bunker Convention itself.",
                 "This is the domestic implementation of the Bunker Convention.", count=1),
     "C_q4_not_a_party_stated:gated"),
    ("C2", "SQ twin only: Q4 reg-box drifts",
     sub_in_file(TWIN, "India is not a Party to the Bunker Convention itself.",
                 "India implements the Bunker Convention.", count=1),
     "twin_identical_to_gated"),
    ("C3", "untouched page (QB9_E) asserts India ratified the Bunker Convention",
     sub_in_file(QB9E, "the Bunker Convention certificate is filed alongside the statutory trading certificates "
                       "in the ship’s master file.",
                 "the Bunker Convention certificate is filed alongside the statutory trading certificates "
                 "in the ship’s master file, since India has ratified the Bunker Convention.", count=1),
     "C_corpus_india_not_taught_as_party"),
    ("C4", "cheat sheet back to '(IS in force)' for Indian waters",
     sub_in_file(CHEAT, "which IS in force internationally (since 21 Nov 2008) — but India is not a Party; "
                        "bunker-spill liability in Indian waters rests on the Merchant Shipping Act, 2025, "
                        "Part IX Ch IV.",
                 "(IS in force).", count=1),
     "C_cheatsheet_in_force_qualified"),
    ("C5", "over-correction: QB9_D's true 'has not ratified' removed",
     sub_in_file(QB9D, "India has not ratified the Bunker Convention", "India's position on the Bunker Convention"),
     "C_overcorrection_qb9d_not_ratified_survives"),
    ("C6", "over-correction: Q4 loses the domestic Act (gated)",
     sub_in_file(GATED, "India's domestic bunker-oil pollution liability regime, modelled on the Bunker Convention",
                 "an Indian statute", count=1),
     "C_q4_domestic_act_kept:gated"),

    # ================================================================ D_PANS
    ("D1", "Q14 numbers box back to '≈ 96 hours' (gated)",
     sub_in_file(GATED, "at least <strong>96 hours</strong> before arrival, or within <strong>2 hours</strong> of "
                        "departure from the last port if the voyage is shorter than 96 hours.</div>",
                 "≈ <strong>96 hours</strong> for India.</div>", count=1),
     "D_q14_pans_conditional_rule:gated"),
    ("D2", "Q18 reg-box: 96-hour rule attributed to SOLAS XI-2 again",
     sub_in_file(GATED, "Security-related information a port State may require before a ship enters its port — "
                        "the security layer to FAL facilitation",
                 "96-hour advance security notification — security layer to FAL facilitation", count=1),
     "D_q18_no_solas_96_hour_rule"),
    ("D3", "Q18 CE tip: short-voyage limb dropped",
     sub_in_file(GATED, "PANS: India requires the Pre-Arrival Notification of Security at least 96 hours before "
                        "arrival — or within 2 hours of departure when the voyage is shorter than 96 hours;",
                 "PANS: India requires the Pre-Arrival Notification of Security at least 96 hours before "
                 "arrival;", count=1),
     "D_q18_every_pans_site_conditional"),
    ("D4", "Q18 body: PANS sent to a DGS port office again",
     sub_in_file(GATED, "submitted to the <strong>port of call and its Port Facility Security Officer</strong>",
                 "submitted to the <strong>DGS port office</strong>", count=1),
     "D_q18_every_pans_site_conditional"),
    ("D5", "untouched page (simon-notes-p7) gains 'PANS ≈ 96 hours'",
     sub_in_file(NOTES7, "ISPS pre-arrival security information — required in addition to FAL forms",
                 "ISPS pre-arrival security information — required in addition to FAL forms; PANS ≈ 96 hours "
                 "for India", count=1),
     "D_corpus_no_pans_defect"),
    ("D6", "over-correction: Q18 SOLAS XI-2/9.2 limb deleted",
     sub_in_file(GATED, "<strong>SOLAS regulation XI-2/9.2</strong> lets a Contracting Government",
                 "the port State may", count=1),
     "D_q18_solas_limb_kept"),

    # ================================================================ RECORD
    ("R1", "Q18 stamp loses the correction",
     sub_in_file(GATED, "QB1 · Q18 · v1.1 — corrected 17 Sep 2026 (India oil-spill regulatory audit)",
                 "QB1 · Q18 · v1.0", count=1),
     "stamps_record_correction"),
    ("R2", "governed changelog note: 'not a Party' flipped",
     edit_json(GOV, _gov_note_drops_not_a_party),
     "governed_note_states_all_four"),
    ("R3", "governed correct, DERIVED index hand-edited",
     edit_json(IDX, _index_note_drifts),
     "generated_index_matches_governed_changelog"),
    ("R4", "trap 134 turned into a literal GREP ban",
     sub_in_file(TRAPS, "GREP: SKIP (proposition-scoped by design",
                 "GREP: 700 tonnes (proposition-scoped by design", count=1),
     "trap_134_not_a_blanket_ban"),
    ("R5", "NOSDCP plan row claims the text was retrieved",
     edit_json(REGISTRY, _plan_row_claims_retrieved),
     "nosdcp_plan_recorded_access_limited"),

    # ================================================================ NON-VACUITY
    ("N1", "remove a target card from the census input",
     sub_in_file(QB9A, '<div class="q-card" id="q8"', '<div class="q-card" id="q8x"', count=1),
     "target_cards_present"),
]


def main() -> int:
    return run_suite("CORR-INDIA-OILSPILL-REGULATORY-AUDIT-20260917 mutation suite", PROBE,
                     MUTATIONS, WATCHED)


if __name__ == "__main__":
    sys.exit(main())
