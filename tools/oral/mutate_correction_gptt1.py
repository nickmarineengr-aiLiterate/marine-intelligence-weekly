#!/usr/bin/env python3
"""
Mutation suite for the GPT high-risk review tranche 1 corrections.

`validate_correction_gptt1.py` reports 68 green checks. Green output on its own
is indistinguishable from a validator that reads nothing, so every proposition
the tranche rests on is attacked here, and each mutation must trip the check
that OWNS it -- never the digest pin, which fires on any byte change at all
(enforced by oral_content_mutation.DIGEST_PINS).

MUTATIONS A, F, N, R AND V REINSTATE THE FIVE REJECTED WORDINGS VERBATIM.
Those are the ones a careless "restore the old phrasing" edit would produce,
and each has to be caught by the check that owns its proposition rather than by
a flat phrase ban -- see the validator's header for why the corrected cards now
legitimately contain the very words a keyword sweep would look for.

THE MUTATIONS THAT MATTER MOST ARE NOT THE WORDING ONES.

*   MUTATION Z1 LAUNDERS AN EVIDENCE TIER. It rewrites the Li-ion record's
    access note so MSC.1/Circ.1615 reads as a held, read instrument. Not one
    byte of candidate-facing product changes, every digest still matches, and
    the corpus quietly acquires a source it does not have. Only
    `msc1615_evidence_tier_recorded` sees it.

*   MUTATION Z2 ERASES A DEVIATION. The review said retaining the circular was
    "probably unnecessary"; it was retained anyway, deliberately, and the
    record says so. Delete that sentence and a decision becomes a drift that
    the next reviewer has no way to distinguish from an oversight.

*   MUTATION Z3 ERASES THE REPORT-ONLY LIST. Seven other cards in QB5_C_B
    carry the same empty 15-second block and the reg-box still carries STCW
    Table A-III/2. Drop that from the record and the next pass opens a file it
    believes is clean.

*   MUTATION Y RESTORES THE V/14 HOOK ON THE MANNING ROW'S TWIN. Deleting a
    hook is easy to over-apply: the manning row's SOLAS V/14 is CORRECT and
    must survive. Y removes it, and `cheatsheet_manning_v14_hook_retained` is
    the only thing that would ever notice an over-correction.
"""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import (                    # noqa: E402
    edit_json, run_suite, sub_in_file)

QB2A = REPO / "meoclass1/QB2_A.html"
QB5J = REPO / "meoclass1/QB5_J.html"
QB5CB = REPO / "meoclass1/QB5_C_B.html"
CHEAT = REPO / "meoclass1/QB5_B_CheatSheet.html"
M_GRAIN = HERE / "correction_corr_gpt_t1_grain_20260904_manifest.json"
M_LIION = HERE / "correction_corr_gpt_t1_liion_20260904_manifest.json"
M_EIAPP = HERE / "correction_corr_gpt_t1_eiapp_20260904_manifest.json"
M_QB5CB = HERE / "correction_corr_gpt_t1_qb5cb_20260904_manifest.json"
PROBE = "validate_correction_gptt1.py"


MUTATIONS = [
    # ------------- FAMILY A: the three-limb criterion -------------------
    ("A", "reinstate the short-form criterion in the 60-second answer",
     sub_in_file(QB2A,
                 "taken up to <strong>the least of</strong> the angle of "
                 "maximum difference between the ordinates of the two curves, "
                 "40°, and the angle of flooding",
                 "up to 40°"),
     "grain_60s_answer_carries_the_criterion"),

    ("B", "drop the least-of enumeration from the body criterion",
     sub_in_file(QB2A,
                 "That area is taken up to <strong>the least of three "
                 "angles</strong>, and the examiner wants all three: "
                 "<strong>(i)</strong> the angle of heel of maximum "
                 "difference between the ordinates of the two curves; "
                 "<strong>(ii) 40&deg;</strong>; and <strong>(iii)</strong> "
                 "the angle of flooding (&theta;<sub>f</sub>).",
                 "That area is taken up to 40&deg;."),
     "grain_residual_area_three_limits_q11"),

    ("C", "revert q33's Numbers block to the short form",
     sub_in_file(QB2A,
                 "residual area taken to the <em>least</em> of the "
                 "maximum-difference angle, 40&deg; and the flooding angle",
                 "residual area to 40&deg;"),
     "grain_q33_numbers_block_carries_least_of"),

    ("D", "revert q33's body statement to the short form",
     sub_in_file(QB2A,
                 "not less than 0.075 m&middot;rad, taken up to the least of "
                 "the maximum-difference angle, 40&deg; and the angle of "
                 "flooding (A 7.1.2)",
                 "up to 40&deg; not less than 0.075 m&middot;rad"),
     "grain_residual_area_three_limits_q33"),

    ("E", "strip the clause citation so the claim cannot be re-checked",
     sub_in_file(QB2A, "Net Residual Area on GZ Curve (A 7.1.2):",
                 "Net Residual Area on GZ Curve:"),
     "grain_criterion_named_by_clause"),

    ("C2", "revert q11's Key Numbers entry to the short form",
     sub_in_file(QB2A,
                 "under A 7.1.2, taken "
                 "up to <strong>the least of</strong> the maximum-difference "
                 "angle, 40&deg;, "
                 "and the angle of flooding.",
                 "under A 7.1.2, up to 40&deg;."),
     "grain_memory_layers_carry_the_criterion"),

    # ------------- FAMILY A: the assumed shifted surface ----------------
    ("F", "reinstate the rolling-amplitude description in the 60-second answer",
     sub_in_file(QB2A,
                 "The Code does not model the ship&rsquo;s roll angle at all.",
                 "As the ship rolls, the grain surface shifts to an angle "
                 "matching the rolling amplitude."),
     "grain_roll_amplitude_claim_absent"),

    ("G", "delete the explicit 'these are not roll angles' denial",
     sub_in_file(QB2A,
                 "They are not the vessel&rsquo;s rolling amplitude</strong>, "
                 "and no one angle applies to every grain compartment.",
                 "</strong>"),
     "grain_assumed_surface_not_the_roll"),

    ("H", "delete the no-universal-angle statement only",
     sub_in_file(QB2A,
                 ", and no one angle applies to every grain compartment", ""),
     "grain_no_universal_shift_angle"),

    ("I", "collapse Part B to a single universal angle (drop B 5.1)",
     sub_in_file(QB2A, "<strong>B 5.1 &mdash; partly filled compartment:</strong>",
                 "<strong>Partly filled compartment:</strong>"),
     "grain_partB_clauses_by_number"),

    ("J", "un-anchor the CE tip from its clauses",
     sub_in_file(QB2A,
                 "the surface after shifting is assumed at <strong>25&deg; to "
                 "the horizontal</strong> under B 5.1, and B 1.5 applies a "
                 "<strong>1.12 &times;</strong> factor",
                 "the shifting calculation is more severe"),
     "grain_ce_tip_carries_both_angles"),

    # ------------- FAMILY A: casualty and vessel claims -----------------
    ("K", "reinstate MV Leros Strength as grain casualty support",
     sub_in_file(QB2A,
                 "<p>No specific casualty is necessary to answer this question;",
                 "<p><em>MV Leros Strength (1997)</em> &mdash; a bulk carrier "
                 "lost with all hands, highlighting compliance with grain "
                 "loading codes. No specific casualty is necessary to answer "
                 "this question;"),
     "leros_strength_absent_from_page"),

    ("L", "reinstate the fabricated Maersk geared-bulk claim",
     sub_in_file(QB2A,
                 "<p>Bulk grain is not a cargo regime I operate.",
                 "<p>On Maersk managed logistics networks, geared fleet "
                 "configurations carrying agricultural bulk integrate grain "
                 "shifting moment modules into the loadicator."),
     "grain_fabricated_vessel_claim_absent"),

    ("M", "re-attribute the 0.30 m GM to SOLAS VI",
     sub_in_file(QB2A,
                 "free surface effects, under Grain Code A 7.1.3",
                 "free surface effects, required under SOLAS VI"),
     "grain_gm_attributed_to_the_code"),

    # ------------- FAMILY B: CO2 --------------------------------------
    ("N", "reinstate 'CO2 will not extinguish a Li-ion thermal runaway'",
     sub_in_file(QB2A,
                 "The answer that passes separates the <strong>flame</strong> "
                 "from the <strong>cell</strong>.",
                 "Your answer must be: No, CO2 will not extinguish a Li-ion "
                 "thermal runaway."),
     "liion_categorical_uselessness_absent"),

    ("O", "delete the positive statement that CO2 can suppress flaming combustion",
     sub_in_file(QB2A,
                 "<strong>CO<sub>2</sub> can suppress oxygen-dependent flaming "
                 "combustion in an enclosed protected space</strong>, and "
                 "fixed CO<sub>2</sub> has been used operationally against "
                 "shipboard battery and vehicle fires &mdash; that is what the "
                 "installation is for. ",
                 ""),
     "liion_co2_can_suppress_flaming_combustion"),

    ("P", "reinstate the 'waste your fixed extinguishing agent' conclusion",
     sub_in_file(QB2A,
                 "<strong>Do not tell the panel you would withhold an "
                 "installed fixed system merely because batteries are "
                 "involved</strong>",
                 "Releasing it early can waste your fixed extinguishing agent"),
     "liion_no_withholding_instruction"),

    ("Q", "sever the release decision from the Master and the fire control plan",
     sub_in_file(QB2A,
                 "is a decision for the Master under the ship&rsquo;s fire "
                 "control plan and emergency procedure, on my technical "
                 "advice. What decides it is the location and accessibility of "
                 "the fire, whether the space is enclosed and can be sealed, "
                 "whether anybody is unaccounted for inside, and what is "
                 "actually installed &mdash; not the mere presence of lithium "
                 "cells.",
                 "is my call as Chief Engineer."),
     "liion_release_decision_is_the_masters"),

    ("R", "restore an unconditioned universal action sequence in the 60s answer",
     sub_in_file(QB2A,
                 "My engineering actions follow the ship&rsquo;s fire control "
                 "plan and the Master&rsquo;s emergency command, and what I "
                 "actually do depends on where the container is, whether the "
                 "space is enclosed and can be sealed, and whether the cells "
                 "can be reached at all. For a container in a closed hold I",
                 "My immediate engineering actions are that I"),
     "liion_action_sequence_is_conditioned"),

    ("S", "erase the boundary-versus-direct cooling distinction",
     sub_in_file(QB2A,
                 "Say which cooling you mean: for a closed container stowed in "
                 "a hold you can reach only the <em>boundary</em>; direct "
                 "cooling of the cells is available only where the pack is "
                 "accessible.",
                 ""),
     "liion_boundary_vs_direct_cooling"),

    # ------------- FAMILY B: the wrong-scope circular -------------------
    ("T", "reinstate the false lithium-battery title for MSC.1/Circ.1615",
     sub_in_file(QB2A,
                 "<span class=\"reg-code\">Scope caution — "
                 "MSC.1/Circ.1615</span>",
                 "<span class=\"reg-code\">IMO Guidance &mdash; "
                 "MSC.1/Circ.1615 (Guidelines for preventing and mitigating "
                 "lithium battery fires)</span>"),
     "msc1615_false_title_absent"),

    ("U", "delete the 'not generic containership guidance' negative",
     sub_in_file(QB2A,
                 "but it is <strong>not</strong> generic containership or "
                 "containerized-lithium-battery fire guidance and must not be "
                 "quoted as though it were.",
                 "and it is widely consulted."),
     "msc1615_not_generic_container_guidance"),

    ("V", "re-merge IMDG transport classification with firefighting guidance",
     sub_in_file(QB2A,
                 "This is a <em>transport</em> classification — it "
                 "governs declaration, packing, marking, stowage and "
                 "segregation, and it is not shipboard firefighting guidance.",
                 "This governs the shipboard response."),
     "imdg_transport_and_firefighting_separated"),

    ("W", "assert EmS F-A / S-I as a fixed pair, unqualified",
     sub_in_file(QB2A,
                 "as shown against the applicable UN entry in the IMDG "
                 "amendment in force",
                 "always"),
     "ems_qualified_to_the_amendment_in_force"),

    # ------------- FAMILY C: the EIAPP illustration ---------------------
    ("X", "reinstate automatic EIAPP invalidation in the deep-dive",
     sub_in_file(QB5J,
                 "A: Only within the full range of adjustments the NOx "
                 "Technical File identifies as allowable. Working outside the "
                 "approved configuration has to go down the applicable "
                 "approved route — amendment of the technical file, and "
                 "verification at survey by the engine parameter check method "
                 "— and an unapproved departure can leave the engine no "
                 "longer compliant with its certified NOx configuration.",
                 "A: Only within the NOx Technical File — outside it the "
                 "EIAPP is invalidated."),
     "eiapp_absolute_invalidation_absent"),

    # ------------- FAMILY D: QB5_C_B#q5 --------------------------------
    ("AA", "empty the 15-second answer again",
     sub_in_file(QB5CB,
                 "<span class=\"pb-label\">15-Second Answer</span>Stabilise "
                 "the ship first,",
                 "<span class=\"pb-label\">15-Second Answer</span></div><div "
                 "class=\"practice-block-x\">Stabilise the ship first,"),
     "qb5cb_15s_answer_is_substantive"),

    ("AB", "reinstate ISM Code Section 5 as casualty-investigation authority",
     sub_in_file(QB5CB,
                 "<span class=\"reg-code\">Casualty Investigation Code "
                 "(MSC.255(84))</span>",
                 "<span class=\"reg-code\">ISM Code Section 5</span>"),
     "qb5cb_ism_section_5_absent"),

    ("AC", "strip a reg-code back out, restoring the malformed row shape",
     sub_in_file(QB5CB,
                 "<span class=\"reg-code\">MLC 2006, Regulation 4.3</span>",
                 ""),
     "qb5cb_regbox_rows_well_formed"),

    ("AD", "truncate the Casualty Investigation Code title again",
     sub_in_file(QB5CB, "into a Marine Casualty or Marine Incident</em>, "
                        "adopted by resolution <strong>MSC.255(84)</strong>.",
                 "into a Marine Casualty.</em>"),
     "qb5cb_cic_full_instrument_identity"),

    ("AE", "restore the hostage/piracy CE tip",
     sub_in_file(QB5CB,
                 "The discriminator is not piracy procedure &mdash; it is "
                 "<em>who investigates</em>.",
                 "This is a hostage/piracy-adjacent scenario."),
     "qb5cb_ce_tip_is_the_real_discriminator"),

    ("AF", "reinstate 'physically seize and lock away' the Oil Record Book",
     sub_in_file(QB5CB,
                 "<strong>Logbook Preservation:</strong> Preserve the active "
                 "Engine Room Logbook, Bell Book and Oil Record Book exactly "
                 "as they stand",
                 "<strong>Logbook Securing:</strong> Physically seize and lock "
                 "away the active Engine Room Logbook, Bell Book and Oil "
                 "Record Book"),
     "qb5cb_no_seizure_of_statutory_records"),

    ("AG", "delete the preservation principle that replaced the seizure",
     sub_in_file(QB5CB,
                 "<em>The records are not mine to impound.</em> ", ""),
     "qb5cb_preservation_principle_stated"),

    ("AH", "reinstate the automatic prosecution / CoC-cancellation claim",
     sub_in_file(QB5CB,
                 "is a serious matter that may lead to investigation and, "
                 "depending on the facts, the jurisdiction and the authority "
                 "seized of the case, to administrative or criminal "
                 "proceedings, to action against the Certificate of "
                 "Competency, and to civil liability for the company. What "
                 "actually follows is decided by the competent authority on "
                 "the evidence &mdash; it is not automatic &mdash; but",
                 "will result in immediate criminal prosecution, cancellation "
                 "of the Certificate of Competency (CoC), and massive "
                 "international legal liability. And"),
     "qb5cb_automatic_consequence_absent"),

    ("AI", "soften the professional warning while keeping the conditional form",
     sub_in_file(QB5CB,
                 "but the exposure is real enough that the only defensible "
                 "course is a complete, contemporaneous and unaltered record.",
                 "but in practice little usually follows."),
     "qb5cb_professional_warning_not_weakened"),

    # ------------- FAMILY D artefact: the cheat sheet -------------------
    ("AJ", "reinstate the unsupported SOLAS V/14 hook on the pre-arrival row",
     sub_in_file(CHEAT,
                 "ISM Code §6.3 (familiarisation on a new "
                 "assignment)</td>",
                 "ISM Code §6.3 (familiarisation on a new assignment) / "
                 "SOLAS V/14</td>"),
     "cheatsheet_prearrival_v14_hook_removed"),

    ("Y", "OVER-CORRECT: delete V/14 from the manning row, where it is right",
     sub_in_file(CHEAT, "STCW 2010 / SOLAS V/14 / MLC 2006",
                 "STCW 2010 / MLC 2006"),
     "cheatsheet_manning_v14_hook_retained"),

    # ------------- governance the product cannot show ------------------
    ("Z1", "LAUNDER THE EVIDENCE TIER: claim MSC.1/Circ.1615 was retrieved",
     edit_json(M_LIION, lambda d: d["authority"].__setitem__(
         "msc1_circ_1615_evidence_tier",
         "The circular is held in the corpus and was read in full.")),
     "msc1615_evidence_tier_recorded"),

    ("Z2", "ERASE THE DEVIATION: hide that retention departed from the review",
     edit_json(M_LIION, lambda d: d["authority"].__setitem__(
         "msc1_circ_1615_treatment",
         "The circular was retained with an accurate scope label.")),
     "msc1615_deviation_recorded"),

    ("Z3", "ERASE THE REPORT-ONLY LIST: make QB5_C_B look clean",
     edit_json(M_QB5CB, lambda d: d["propagation"].__setitem__(
         "found_and_not_swept",
         ["Nothing else was found."])),
     "qb5cb_wider_defects_reported_not_fixed"),

    ("Z5", "drop the Grain primary text, leaving the record unre-checkable",
     edit_json(M_GRAIN, lambda d: d["authority"].__setitem__(
         "operative_text_A_7_1_2", "A 7.1.2 sets the residual area.")),
     "grain_primary_text_recorded"),

    ("Z6", "hide the OCR limit on the scanned instrument",
     edit_json(M_GRAIN, lambda d: d["authority"].__setitem__(
         "access_note", "Read from the held PDF.")),
     "grain_ocr_limit_recorded"),

    ("Z7", "undeclare the cheat sheet, taking it outside the event's scope",
     edit_json(M_QB5CB, lambda d: d.__setitem__(
         "artefacts", [a for a in d["artefacts"]
                       if not a["path"].endswith("QB5_B_CheatSheet.html")])),
     "qb5cb_cheatsheet_artefact_declared"),

    ("Z8", "drop Pass 1's QB3_F adjudication, re-opening a settled decision",
     edit_json(M_EIAPP, lambda d: d["propagation"].__setitem__(
         "found_and_not_swept", [])),
     "eiapp_qb3f_adjudication_carried_forward"),

    ("Z9", "break the supersession ancestry by naming the wrong predecessor",
     edit_json(M_EIAPP, lambda d: d["cards"][0]["supersedes"].__setitem__(
         "action_id", "H6-001")),
     "supersession_ancestry_declared"),
]

WATCHED = [QB2A, QB5J, QB5CB, CHEAT, M_GRAIN, M_LIION, M_EIAPP, M_QB5CB]

if __name__ == "__main__":
    raise SystemExit(run_suite(
        "mutation suite: GPT high-risk review tranche 1 "
        "(QB2_A#q7/#q11/#q33, QB5_J#q2, QB5_C_B#q5, QB5_B_CheatSheet)",
        PROBE, MUTATIONS, WATCHED))
