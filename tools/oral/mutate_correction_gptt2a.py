#!/usr/bin/env python3
"""
Mutation suite for the GPT high-risk review tranche 2A corrections.

`validate_correction_gptt2a.py` reports 42 green checks. Green output on its own
is indistinguishable from a validator that reads nothing, so every proposition
the tranche rests on is attacked here, and each mutation must trip the check
that OWNS it -- never the digest pin, which fires on any byte change at all
(enforced by oral_content_mutation.DIGEST_PINS, which this tranche extended with
`live_cards_match_authorised_state`).

MUTATIONS A, C, L, P, S AND V REINSTATE THE REJECTED WORDINGS.
Those are what a careless "restore the old phrasing" edit produces, and each has
to be caught by the check that owns its proposition rather than by a flat phrase
ban -- because the corrected cards now legitimately CONTAIN the very words a
keyword sweep would look for. q27 quotes "the area under the GZ curve" twice
while teaching against it.

THE MUTATIONS THAT MATTER MOST CHANGE NO CANDIDATE-FACING BYTE.

*   MUTATION I RELABELS DERIVED EVIDENCE AS QUOTED. It deletes the record's
    statement that NO CLAUSE OF THE CODE STATES THE LOWER BOUND. The card still
    teaches the angle of equilibrium, every digest still matches, and the corpus
    quietly acquires the claim that A 7.1.2 says something it does not. That is
    the same class of error this tranche exists to fix, committed by the record
    instead of by the card. Only `grain_lower_bound_provenance_is_figure_a7`
    would ever see it.

*   MUTATION J ERASES A CORRECTION TO THE BRIEF. The brief asserted two facts
    the tree does not bear out. Delete the record of that and the next reviewer
    inherits a wrong model of the corpus and no way to discover it.

*   MUTATION K ERASES THE REPORT-ONLY LIST. q11's heading still carries the
    rejected terminology as a label, and neither q11 nor q33 teaches the lower
    bound. Both were found while fixing q27 and both were deliberately left.
    Drop that and the next pass opens a file it believes is finished.

*   MUTATION X ERASES A DELIBERATE NON-IMPLEMENTATION. The SOLAS VI/VII limb was
    adjudicated, found unambiguous, and NOT implemented because the brief made
    implementation conditional on something that is not true. A deviation has to
    be visible in the record or the next reviewer cannot tell a decision from an
    oversight.

*   MUTATION Y FABRICATES AN ANCESTOR. q27 has never been owned by any record.
    Inventing a `supersedes` claim would assert that some earlier record vouched
    for this card. `grain_q27_declares_no_ancestry` is the only check that
    treats the ABSENCE of a chain as load-bearing evidence.

AND TWO GUARD AGAINST OVER-CORRECTION, NOT UNDER-CORRECTION.

*   MUTATION H edits q26, which Pass 2 found clean and which must not move.
*   MUTATION N strips the MSC.552(108) content out of known_traps trap 55. The
    trap was edited; deleting a correct neighbouring paragraph while in there is
    exactly the accident a scoped correction is supposed to prevent, and only
    `known_traps_msc552_layer_intact` would notice.

THREE MUTATIONS EXIST BECAUSE THREE CHECKS ALREADY ESCAPED
----------------------------------------------------------
D, G and R passed on the first run of this suite while the proposition they
guard had been deleted, because each was written CARD-WIDE for a proposition
that lives in a BLOCK: the lower bound survived in the Numbers entry after being
cut from the body, the flooding angle survived in the body after being cut from
the Numbers entry, and MSC.255(84) survived in the NEW ISM 9 row after being
stripped off the Casualty Investigation Code row -- a correction's own text
standing in for the thing it was meant to guard. All three checks are now scoped
to the block that must carry the claim. The suite also found the gate's failure
PATH broken: a bad attribute on the mismatch-reporting line meant every HTML
mutation crashed the validator instead of failing it, which reads as "no failing
check" and would have been indistinguishable from a clean escape.
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
QB2B = REPO / "meoclass1/QB2_B.html"
QB5CB = REPO / "meoclass1/QB5_C_B.html"
TRAPS = REPO / "meoclass1/known_traps.md"
M_GRAIN = HERE / "correction_corr_gpt_t2a_grain_20260905_manifest.json"
M_QB5CB = HERE / "correction_corr_gpt_t2a_qb5cb_20260905_manifest.json"
M_IMSBC = HERE / "correction_corr_gpt_t2a_imsbc_20260905_manifest.json"
PROBE = "validate_correction_gptt2a.py"


MUTATIONS = [
    # ---------- FAMILY A: the object of the criterion -------------------
    ("A", "assert 'the area under the GZ curve' outside a quotation",
     sub_in_file(QB2A,
                 "It is the area BETWEEN two curves, and 40&deg; is only one",
                 "It is the area under the GZ curve, and 40&deg; is only one"),
     "q27_never_asserts_area_under_the_gz_curve"),

    ("B", "strip the between-the-curves formulation from the body bullet",
     sub_in_file(QB2A,
                 "the net or residual area <strong>between the heeling arm "
                 "curve and the righting arm curve</strong>, taken "
                 "<strong>from the angle of equilibrium</strong>",
                 "the net or residual area, taken "
                 "<strong>from the angle of equilibrium</strong>"),
     "q27_body_site_corrected"),

    ("C", "reduce the body criterion to the single 40-degree bound",
     sub_in_file(QB2A,
                 "up to <strong>the least of</strong> <strong>(i)</strong> the "
                 "angle of heel of <strong>maximum difference between the "
                 "ordinates of the two curves</strong>, <strong>(ii) 40&deg;"
                 "</strong> and <strong>(iii)</strong> the <strong>angle of "
                 "flooding</strong> (&theta;<sub>f</sub>), shall in all "
                 "conditions of loading be not less than <strong>0.075 "
                 "metre-radians</strong>.",
                 "up to <strong>40&deg;</strong>, shall in all conditions of "
                 "loading be not less than <strong>0.075 metre-radians</strong>."),
     "q27_no_criterion_sentence_bounds_only_at_40"),

    ("D", "delete the angle-of-equilibrium lower bound from the card",
     sub_in_file(QB2A,
                 "taken <strong>from the angle of equilibrium</strong> (the "
                 "first intersection of the two curves, where the assumed "
                 "shift has heeled the ship) up to",
                 "taken up to"),
     "q27_teaches_angle_of_equilibrium_lower_bound"),

    ("E", "delete the criterion from Numbers to Memorise",
     sub_in_file(QB2A,
                 "<li><strong>0.075 metre-radians (Grain Code A 7.1.2):</strong> "
                 "The minimum net or residual area <strong>between the heeling "
                 "arm curve and the righting arm curve</strong>, taken from the "
                 "angle of equilibrium up to <strong>the least of</strong> the "
                 "maximum-difference angle, 40&deg; and the angle of flooding. "
                 "Never shorten it to &ldquo;the area up to 40&deg;&rdquo;, and "
                 "never call it &ldquo;the area under the GZ curve&rdquo;.</li>",
                 ""),
     "q27_numbers_site_corrected"),

    ("F", "drop the deck-edge limb from the Numbers 12-degree entry",
     sub_in_file(QB2A,
                 "<li><strong>12&deg; (Grain Code A 7.1.1):</strong> The maximum "
                 "angle of heel due to the assumed grain shift &mdash; or, for "
                 "ships constructed on or after 1 January 1994, the angle at "
                 "which the deck edge is immersed, whichever is the lesser.</li>",
                 "<li><strong>12&deg;:</strong> The maximum allowable final "
                 "calculated angle of heel due to a dynamic grain shift.</li>"),
     "q27_12_degree_entry_carries_deck_edge_limb"),

    ("G", "remove the flooding angle from both q27 criterion statements",
     sub_in_file(QB2A,
                 "and the angle of flooding. Never shorten it",
                 "and nothing further. Never shorten it"),
     "q27_states_all_three_least_of_limits"),

    # ---------- FAMILY B: over-correction ------------------------------
    ("H", "tidy q26, the neighbouring card Pass 2 found clean",
     sub_in_file(QB2A,
                 "the buoyancy of the timber stack increases the righting lever "
                 "(GZ) curve at large angles",
                 "the buoyancy of the timber stack increases the GZ curve at "
                 "large angles"),
     "q26_byte_unchanged"),

    ("N", "delete the MSC.552(108) content from known_traps trap 55",
     sub_in_file(TRAPS,
                 "> **“specially suitable compartment, partly filled in way "
                 "of the hatch opening, with ends\n> untrimmed”** — new "
                 "definition **A 2.8**.",
                 "> a third configuration was added."),
     "known_traps_msc552_layer_intact"),

    # ---------- FAMILY C: the record, not the product ------------------
    ("I", "relabel the derived lower bound as quoted clause text",
     edit_json(M_GRAIN, lambda d: d["authority"].__setitem__(
         "figure_A7_derived_not_quoted",
         "The lower bound is the angle of equilibrium, per A 7.1.2.")),
     "grain_lower_bound_provenance_is_figure_a7"),

    ("J", "erase the corrections to the brief's own factual premise",
     edit_json(M_GRAIN, lambda d: d.__setitem__(
         "candidate_verdict", "UPHELD ON BOTH. The instrument was re-read.")),
     "grain_brief_premise_corrections_recorded"),

    ("K", "erase the q11 / q33 report-only findings",
     edit_json(M_GRAIN, lambda d: d["propagation"].__setitem__(
         "found_and_not_swept", [])),
     "grain_q11_q33_residuals_reported_not_fixed"),

    ("O", "drop known_traps.md from the record's artefacts",
     edit_json(M_GRAIN, lambda d: d.__setitem__("artefacts", [])),
     "known_traps_declared_as_artefact"),

    ("Y", "fabricate a supersession ancestor for the unowned q27",
     edit_json(M_GRAIN, lambda d: d["cards"][0].__setitem__(
         "supersedes", {"manifest": "correction_corr_gpt_t1_grain_20260904_manifest.json",
                        "action_id": "CORR-GPT-T1-GRAIN-01",
                        "post_edit_digest": "907305079f536fe59f7e754ee940f06c11566"
                                            "62c33ee5409b9cac2fd77bd5a23"})),
     "grain_q27_declares_no_ancestry"),

    ("W", "erase the IMSBC evolving-instrument position",
     edit_json(M_IMSBC, lambda d: d["authority"].__setitem__(
         "source_currentness", "MSC.268(85) is the base Code.")),
     "imsbc_currentness_position_recorded"),

    ("X", "erase the deliberate non-implementation of the VI/VII limb",
     edit_json(M_IMSBC, lambda d: d["cards"][0].__setitem__(
         "deliberately_unchanged",
         ["The main answer, which is correct as it stands."])),
     "imsbc_solas_vi_vii_reported_not_implemented"),

    # ---------- FAMILY D: known_traps, the authoring source ------------
    ("L", "reinstate the short-form criterion in the authoring file",
     sub_in_file(TRAPS,
                 "**A 7.1.2**, the net or residual\n  area **between the "
                 "heeling arm curve and the righting arm curve**, taken from "
                 "the **angle of\n  equilibrium** up to the **least** of the "
                 "maximum-difference angle, **40°** and the angle of\n  "
                 "flooding, not less than **0.075 m·rad**;",
                 "**0.075 m·rad** residual area to 40°;"),
     "known_traps_short_form_removed"),

    ("M", "delete the standing authoring rule",
     sub_in_file(TRAPS,
                 "* **AUTHORING RULE — never write the A 7.1.2 criterion "
                 "in the short form.**",
                 "* **A note on style.**"),
     "known_traps_carries_authoring_rule"),

    ("N2", "reduce trap 74 to the incident, dropping its rule",
     sub_in_file(TRAPS,
                 "the row is answering a question the card did not ask.",
                 "the row is unhelpful."),
     "known_traps_74_states_the_regbox_rule"),

    ("N3", "drop the second exclusion limb from trap 75",
     sub_in_file(TRAPS,
                 "**TWO INDEPENDENT LIMBS, EITHER ONE SUFFICIENT.**",
                 "**The reason.**"),
     "known_traps_75_states_the_definition_rule"),

    ("O2", "drop the qb5cb record's authoring trap",
     edit_json(M_QB5CB, lambda d: d.__setitem__("known_traps_entries", [])),
     "known_traps_declared_as_artefact"),

    # ---------- FAMILY E: QB5_C_B's reg-box ----------------------------
    ("P", "reinstate the STCW Table A-III/2 row verbatim",
     sub_in_file(QB5CB,
                 '<span class="reg-code">ISM Code &sect;9</span>',
                 '<span class="reg-code">STCW Code, Table A-III/2</span>'),
     "qb5cb_regbox_stcw_a_iii_2_removed"),

    ("Q", "let ISM 9 read as the flag-State investigation",
     sub_in_file(QB5CB,
                 "It is <strong>not</strong> the flag State&rsquo;s statutory "
                 "<strong>marine safety investigation</strong>, which is "
                 "conducted by that State&rsquo;s marine safety investigation "
                 "Authority under the Casualty Investigation Code "
                 "(MSC.255(84)) in the first row above.",
                 "It is the investigation regime that applies after a casualty."),
     "qb5cb_ism9_not_flag_state_investigation"),

    ("R", "strip the statutory reference from the reg-box",
     sub_in_file(QB5CB,
                 '<span class="reg-code">Casualty Investigation Code '
                 '(MSC.255(84))</span>',
                 '<span class="reg-code">Casualty Investigation Code</span>'),
     "qb5cb_regbox_retains_msc255_84"),

    ("Z", "drop the byte-unchanged declaration for the correct row",
     edit_json(M_QB5CB, lambda d: d["cards"][0].__setitem__(
         "deliberately_unchanged",
         ["The MLC row and the ISPS row."])),
     "qb5cb_msc255_row_declared_byte_unchanged"),

    ("K2", "turn the deferred correction-log entry into a silent omission",
     edit_json(M_GRAIN, lambda d: d.__setitem__(
         "content_index_effect", "None on counts.")),
     "content_log_entry_deferred_on_the_record"),

    # ---------- FAMILY F: QB2_B's IMSBC scope --------------------------
    ("S", "put flexitanks back inside IMSBC scope",
     sub_in_file(QB2B,
                 "and a <strong>flexitank is liquid cargo carried inside a "
                 "freight container</strong>, so it is excluded twice over "
                 "&mdash; neither solid nor uncontained. Neither is an IMSBC "
                 "operation.",
                 "and a flexitank inside a standard box is handled under the "
                 "IMSBC weight and distribution limits."),
     "qb2b_onmyvessel_flexitank_not_inside_imsbc"),

    ("T", "remove the definition the exclusion rests on",
     sub_in_file(QB2B,
                 "<em>&ldquo;which is loaded directly into the cargo spaces of "
                 "a ship without any intermediate form of containment&rdquo;"
                 "</em>",
                 "<em>and carried in bulk</em>"),
     "qb2b_onmyvessel_states_the_definition"),

    ("U", "corrupt the trap answer that already drew the line",
     sub_in_file(QB2B,
                 "whereas the <strong>IMSBC Code</strong> governs loose, "
                 "un-packaged hazardous materials loaded directly into the "
                 "ship's bulk cargo holds.",
                 "whereas the <strong>IMSBC Code</strong> governs bulk cargo "
                 "generally."),
     "qb2b_imsbc_imdg_distinction_preserved"),

    ("V", "teach the 2027 IMSBC amendment as already mandatory",
     sub_in_file(QB2B,
                 "What actually governs my ship is the <strong>IMDG Code"
                 "</strong>",
                 "Amendment 08-25 (MSC.575(110)) is mandatory now. What "
                 "actually governs my ship is the <strong>IMDG Code</strong>"),
     "qb2b_no_2027_amendment_taught_as_mandatory"),
]


if __name__ == "__main__":
    raise SystemExit(run_suite(
        "mutation suite: GPT high-risk review tranche 2A content gate",
        PROBE, MUTATIONS,
        [QB2A, QB2B, QB5CB, TRAPS, M_GRAIN, M_QB5CB, M_IMSBC]))
