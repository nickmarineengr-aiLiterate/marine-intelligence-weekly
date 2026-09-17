#!/usr/bin/env python3
"""Mutation suite for CORR-NOSDCP-MINISTRY-20260916.

Every mutation names the PROPOSITION check it must trip; the shared harness
refuses a digest pin as a catch. Probes only validate_correction_nosdcp.py, so
the suite runs in minutes, not hours (validate_corrections owns the pins and
is exercised by corrections_mutate).

REGRESSION (A-H, L, U-X): a corrected limb goes back to the shipped defect - the
  ministry, the "nodal" designation, the P&I "all costs" statement, the DPA/DGS
  reporting chain - one site at a time, so a card-scoped "somewhere on the
  card it is right" check cannot pass.
TWIN (B): the SQ free sample drifts from the gated copy.
CORPUS (I): the defect reappears on a page this record never touched.
OVER-CORRECTION (J, K): a blanket "Earth Sciences" ban wipes QB9_E's correct
  use; the trap entry becomes a literal GREP ban.
WORDING (M, N): the two phrasings the approval ruled out come back.
RECORD (O, P, Q): the stamp, the governed note, the derived index.
NON-VACUITY (R): a target card disappears from the census input.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import edit_json, run_suite, sub_in_file  # noqa: E402

GATED = REPO / "meoclass1/QB1_A.html"
TWIN = REPO / "SQ/QB1_A.html"
QB9A = REPO / "meoclass1/QB9_A.html"
QB9E = REPO / "meoclass1/QB9_E.html"
TRAPS = REPO / "meoclass1/known_traps.md"
GOV = HERE / "qb_content_index_governed.json"
IDX = REPO / "meoclass1/qb_content_index.json"

PROBE = "validate_correction_nosdcp.py"
WATCHED = [GATED, TWIN, QB9A, QB9E, TRAPS, GOV, IDX]


def _both(*applies):
    def apply():
        for a in applies:
            a()
    return apply


def _gov_note_ministry_back(d):
    for e in d["recently_updated"]:
        if e.get("date") == "2026-09-16" and "NOSDCP" in e.get("note", ""):
            e["note"] = e["note"].replace(
                "sits under the Ministry of Defence, not the Ministry of Earth Sciences",
                "sits under the Ministry of Earth Sciences")
            return
    raise AssertionError("governed NOSDCP note absent")


def _index_note_drifts(d):
    for e in d["recently_updated"]:
        if e.get("date") == "2026-09-16":
            e["note"] = e["note"] + " (hand-edited on the derived surface)"
            return
    raise AssertionError("generated index anchor absent")


MUTATIONS = [
    # ---- REGRESSION ----------------------------------------------------------
    ("A", "Q15 body: ministry back to Earth Sciences (gated)",
     sub_in_file(GATED, "<strong>Ministry: Ministry of Defence.</strong>",
                 "<strong>Authority: Ministry of Earth Sciences.</strong>", count=1),
     "q15_no_earth_sciences_as_authority:gated"),

    ("C", "Q15 15-second answer only: under the Ministry of Earth Sciences",
     sub_in_file(GATED, "Contingency Plan under the Ministry of Defence, with the Indian Coast Guard",
                 "Contingency Plan under the Ministry of Earth Sciences, with the Indian Coast Guard",
                 count=1),
     "q15_no_earth_sciences_as_authority:gated"),

    ("D", "Q14 60-second answer: Coast Guard back to 'nodal agency'",
     sub_in_file(GATED, "under the Ministry of Defence, is the Central Coordinating Authority, with",
                 "is the nodal agency, with", count=1),
     "no_nodal_designation:gated"),

    ("E", "Q15 liability: P&I club strictly liable for all costs",
     sub_in_file(GATED, "<strong>P&amp;I club is the liability insurer, not the liable party</strong>",
                 "<strong>P&amp;I club is strictly liable for all costs</strong>", count=1),
     "no_pandi_liable_for_all_costs:gated"),

    ("F", "Q14 memory map: back to 'P&I club pays'",
     sub_in_file(GATED, "(Polluter Pays → shipowner liable; P&amp;I insures)",
                 "(Polluter Pays → P&amp;I club pays)", count=1),
     "no_pandi_liable_for_all_costs:gated"),

    ("G", "Q14 CE tip: fixed DPA/DGS reporting chain restored",
     sub_in_file(GATED, "CE → Master → coastal State under MARPOL Protocol I",
                 "CE → Master → DPA → ICG/Coast Guard → DGS → port authority; coastal State under MARPOL Protocol I",
                 count=1),
     "no_dpa_before_statutory_report:gated"),

    ("H", "Q15 drops the Business Rules 'Agency' wording, merging the terms",
     sub_in_file(GATED, "the Coast Guard Organisation as the <strong>Central Coordinating Agency</strong>",
                 "the Coast Guard Organisation as the <strong>Central Coordinating Authority</strong>",
                 count=1),
     "q15_business_rules_say_agency:gated"),

    # Q14 states the limit at three sites (body, 60-second answer, scenario).
    # The proposition is card-level - the card must teach limited liability -
    # so all three go; "within port limits" must NOT stand in for them.
    ("L", "Q14 loses every liability-limit statement",
     _both(sub_in_file(GATED, "strictly, but normally within the convention limits and subject to the convention defences; the <strong>P&amp;I club insures",
                       "strictly and without limit; the <strong>P&amp;I club insures", count=1),
           sub_in_file(GATED, "the shipowner is liable, normally within convention limits, and the P&amp;I club insures that liability.",
                       "the shipowner is liable and the P&amp;I club insures that liability.", count=1),
           sub_in_file(GATED, "and its P&amp;I insurer, within the applicable liability limits.",
                       "and its P&amp;I insurer.", count=1)),
     "q14_shipowner_liable_pandi_insures:gated"),

    ("S", "Q15 direct action made unconditional",
     sub_in_file(GATED, "; where the applicable liability convention provides for direct action (for example CLC 1992), a claim may also be brought <strong>directly against the insurer</strong>.",
                 "; claims can be made <strong>directly against the insurer</strong>.", count=1),
     "direct_action_is_qualified:gated"),

    # ---- GPT-REVIEW AMENDMENTS (17 Sep 2026) ---------------------------------
    ("U", "Bunkers Convention named again in the Q14 direct-action sentence",
     sub_in_file(GATED, "provides for direct action (for example CLC 1992), a claim may also be brought directly against the insurer.",
                 "provides for direct action (CLC 1992, Bunkers Convention), a claim may also be brought directly against the insurer.",
                 count=1),
     "direct_action_names_no_bunkers_convention:gated"),

    ("V", "Q15 CE tip: 'the Coast Guard leads the operational response' restored",
     sub_in_file(GATED, "Response responsibility depends on where the spill occurs: the Coast Guard leads within its maritime-zone responsibilities and coordinates nationally under NOSDCP.",
                 "The Coast Guard leads the operational response under NOSDCP.", count=1),
     "no_unqualified_coast_guard_leads:gated"),

    ("W", "Q14 scenario: 'ICG declares Tier 2 or Tier 3' restored",
     sub_in_file(GATED, "if the incident exceeds local capability, the response escalates to Tier 2 or Tier 3 under NOSDCP, with the Coast Guard taking the coordinating/overall response role;",
                 "ICG declares Tier 2 or Tier 3 NOSDCP response;", count=1),
     "no_icg_declares_tier:gated"),

    ("X", "Q15 60-second answer re-bloated with the Authority/Agency detail",
     sub_in_file(GATED, "The Indian Coast Guard is the Central Coordinating Authority; the DG Coast Guard chairs it.",
                 "The Indian Coast Guard is the Central Coordinating Authority - designated in 1986, plan approved in 1993, "
                 "revised edition released in 2015 and amended since by circular - and the DG Coast Guard chairs it; the "
                 "Allocation of Business Rules word the same role as Central Coordinating Agency, which the Coast Guard's own "
                 "documents also quote when citing the Rules.", count=1),
     "q15_60s_speakable_and_complete:gated"),

    ("T", "DGMA inserted into the Protocol I reporting chain",
     sub_in_file(GATED, "The Master reports <strong>without delay</strong> to the coastal State under",
                 "The Master reports <strong>without delay</strong> via DGMA to the coastal State under", count=1),
     "no_dgma_in_reporting_chain:gated"),

    # ---- TWIN ----------------------------------------------------------------
    ("B", "SQ twin only: ministry back to Earth Sciences",
     sub_in_file(TWIN, "<strong>Ministry: Ministry of Defence.</strong>",
                 "<strong>Authority: Ministry of Earth Sciences.</strong>", count=1),
     "twin_identical_to_gated"),

    # ---- CORPUS --------------------------------------------------------------
    ("I", "an untouched page binds NOSDCP to Earth Sciences",
     sub_in_file(QB9A, "Contingency Plan managed by the Coast Guard.",
                 "Contingency Plan managed by the Coast Guard under the Ministry of Earth Sciences.",
                 count=1),
     "corpus_no_earth_sciences_nosdcp_binding"),

    # ---- OVER-CORRECTION -----------------------------------------------------
    ("J", "blanket ban: QB9_E's correct Earth Sciences usage replaced",
     sub_in_file(QB9E, "Ministry of Earth Sciences", "Ministry of Defence"),
     "qb9e_legit_moes_usage_survives"),

    ("K", "trap 133 turned into a literal GREP ban",
     sub_in_file(TRAPS, 'GREP: SKIP (context-dependent by design: "Ministry of Earth Sciences"',
                 'GREP: Ministry of Earth Sciences (context-dependent by design: "Ministry of Earth Sciences"',
                 count=1),
     "trap_133_not_a_blanket_ban"),

    # ---- WORDING THE APPROVAL RULED OUT --------------------------------------
    ("M", "edition asserted as current",
     sub_in_file(GATED, "the revised NOSDCP edition was released in <strong>2015</strong>",
                 "the current edition is <strong>2015</strong>", count=1),
     "no_current_edition_2015_claim:gated"),

    ("N", "INCOIS described as 'only' forecasting drift",
     sub_in_file(GATED, "MoES institutions such as INCOIS support the response with oceanographic and spill-trajectory services",
                 "INCOIS only forecasts spill drift", count=1),
     "incois_not_only:gated"),

    # ---- RECORD --------------------------------------------------------------
    ("O", "Q15 stamp removed from the gated card",
     sub_in_file(GATED, "QB1 · Q15 · v1.1 — corrected 16 Sep 2026 (NOSDCP authority correction)",
                 "QB1 · Q15 · v1.1", count=1),
     "stamps_record_correction"),

    ("P", "governed changelog note back to Earth Sciences",
     edit_json(GOV, _gov_note_ministry_back),
     "governed_note_states_mod_and_authority"),

    ("Q", "governed correct, DERIVED index hand-edited",
     edit_json(IDX, _index_note_drifts),
     "generated_index_matches_governed_changelog"),

    # ---- NON-VACUITY ---------------------------------------------------------
    ("R", "remove a target card from the census input",
     sub_in_file(TWIN, '<div class="q-card" id="q15"', '<div class="q-card" id="q15x"', count=1),
     "target_cards_present"),
]


def main() -> int:
    return run_suite("CORR-NOSDCP-MINISTRY-20260916 mutation suite", PROBE,
                     MUTATIONS, WATCHED)


if __name__ == "__main__":
    sys.exit(main())
