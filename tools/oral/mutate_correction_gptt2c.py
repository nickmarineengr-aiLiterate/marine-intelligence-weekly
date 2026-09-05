#!/usr/bin/env python3
"""
Mutation suite for the GPT high-risk review tranche 2C corrections.

`validate_correction_gptt2c.py` reports 72 green checks.  Green output on its
own is indistinguishable from a validator that reads nothing, so every
proposition the tranche rests on is attacked here, and each mutation must trip
the check that OWNS it -- never the digest pin, which fires on any byte change
at all (enforced by `oral_content_mutation.DIGEST_PINS`, which already carries
`live_cards_match_authorised_state`).

THE SUITE HAS ALREADY EARNED ITS KEEP ONCE, BEFORE IT WAS WRITTEN
-----------------------------------------------------------------
The gate's FIRST run, against content its author believed correct, returned
eleven failures.  One was a real content escape and five were defects in the
gate itself:

*   QB5_E#q4 asserted "a founding MACN member" TWICE -- in On My Vessel AND in
    the CE Oral Tip.  The scope sweep had read a truncated listing of the card's
    MACN hits and corrected only the first.  The stronger of the two claims was
    in the block a candidate is told to memorise.  Mutation P now guards it.

*   `HELD_PINS` carried a FABRICATED digest for QB2_A#q33 -- transcribed from
    memory rather than read from `CORR-GPT-T1-GRAIN-01`.  It would have failed
    forever on correct content, which is worse than not existing: the next
    reader repairs the card instead of the pin.

*   `li_items(q14, "The dangers")` matched the 60-SECOND ANSWER's sentence "The
    dangers are cryogenic embrittlement..." before it ever reached the `<h4>`
    heading, and then walked the PROCEDURE list.  Four of the five q14 checks
    were reading the wrong block.  This is the block-scope escape class the
    tranche-2A suite found three times, arriving for a fourth.

*   The word budget for "not bloated" was measured over a fixed byte span that
    ran past the 15-second layer into the 60-second one, so one budget was
    being applied to two layers at once.
*   `flatten()` leaves a leading space, so an ORDER check written with
    `startswith()` reported "wrong position" for a correctly ordered list.

None of that is visible from a green run.  It is visible from a red one.

THE MUTATIONS THAT MATTER MOST CHANGE NO CANDIDATE-FACING BYTE
---------------------------------------------------------------
*   MUTATION L ERASES THE BMP PROPAGATION REPORT.  The wrong edition label is
    still live in six cards outside q13.  Delete that from the record and the
    next pass opens a file it believes is finished -- while QB4_H itself
    contradicts across q2, q11 and q13.

*   MUTATION M ERASES THE K-4 SOURCE-CUSTODY GAP.  MSC.551(108) and
    MSC.567(109) are NOT held in the true-source tree, yet the card's footer
    says all five IGF amendments were opened and read.  That is why the K-4
    "keep" is a keep WITH a caveat rather than a clean pass, and deleting the
    caveat converts a qualified decision into an unqualified one.

*   MUTATION N ERASES THE BRIEF'S PREMISE CORRECTIONS.  The brief asserted
    three things the tree does not bear out.  Working around a wrong premise
    silently is how the next reviewer inherits a wrong model of the corpus with
    no way to discover it.

*   MUTATION O DELETES THE GOVERNED CORRECTION LOG FROM THE ARTEFACTS.  The log
    is not a q-card, so no digest in this repo pins it.  Drop the declaration
    and the only record that the tranche touched a candidate-facing surface
    outside the cards disappears.

AND FOUR GUARD AGAINST OVER-CORRECTION, NOT UNDER-CORRECTION
-------------------------------------------------------------
*   MUTATION I imports an enclosed-space entry permit into q14.  The fix landed
    and then kept going -- the failure a "did it land?" check cannot see.
*   MUTATION J edits QB2_A#q33, which the brief ACCEPTED and forbade changing
    for symmetry.
*   MUTATION K edits QB5_C_A#q1, whose typo was DEFERRED.  A deferral that
    nothing enforces is a deferral that quietly happens anyway.
*   MUTATION W advances the hub date, which the brief forbade.

THE NEGATIVE CHECKS ARE ATTACKED THROUGH THE QUOTE DEVICE, NOT AROUND IT
-------------------------------------------------------------------------
The corrected cards legitimately CONTAIN the banned strings, because they teach
against them: q13 says never "the 2026 edition".  A flat keyword ban would fire
on the sentence carrying the fix.  Mutations Q and R therefore reinstate the
rejected wording as an ASSERTION, outside any quotation, which is what a
careless "restore the old phrasing" edit actually produces -- and each must be
caught by `unquoted()`, not by a phrase count.
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
QB3C = REPO / "meoclass1/QB3_C.html"
QB4H = REPO / "meoclass1/QB4_H.html"
QB5CA = REPO / "meoclass1/QB5_C_A.html"
QB5CB = REPO / "meoclass1/QB5_C_B.html"
QB5E = REPO / "meoclass1/QB5_E.html"
QB7D = REPO / "meoclass1/QB7_D.html"
HUB = REPO / "meoclass1/index.html"
LOG = REPO / "tools/oral/qb_content_index_governed.json"
INDEX = REPO / "meoclass1/qb_content_index.json"
AUTH = REPO / ("meoclass1/oral-intelligence/examiner-audit/"
               "GPT_REVIEW_HIGHRISK_TRANCHE2C_20260905.md")

M_OMV = HERE / "correction_corr_gpt_t2c_onmyvessel_20260905_manifest.json"
M_LNG = HERE / "correction_corr_gpt_t2c_lngasphyx_20260905_manifest.json"
M_GRAIN = HERE / "correction_corr_gpt_t2c_grain_20260905_manifest.json"
M_IMSBC = HERE / "correction_corr_gpt_t2c_imsbc_20260905_manifest.json"
M_CURR = HERE / "correction_corr_gpt_t2c_currency_20260905_manifest.json"

PROBE = "validate_correction_gptt2c.py"


MUTATIONS = [
    # ============ FAMILY A: reinstate the unsupported claims ============
    ("A", "reinstate the fleet cloud-sync backup in QB5_C_B#q5",
     sub_in_file(QB5CB,
                 "What I can honestly promise is what is actually in my hands:",
                 "I maintain an automated, remote cloud-sync backup for our "
                 "critical machinery logs via our fleet telemetry. Beyond that:"),
     "q5_no_cloud_sync_fleet_claim_survives"),

    ("B", "reinstate the maritime-tribunal preservation claim",
     sub_in_file(QB5CB,
                 "and made available through the Master to the flag State",
                 "and securely preserved for international maritime tribunals, "
                 "and made available through the Master to the flag State"),
     "q5_no_tribunal_preservation_claim"),

    ("C", "strip the Master / SMS / chain-of-custody frame from the block",
     sub_in_file(QB5CB,
                 "protected against alteration, back-dating or loss, secured "
                 "under the Master&rsquo;s authority and the company&rsquo;s "
                 "SMS procedure with a documented chain of custody, and",
                 "and"),
     "q5_omv_preserves_originals_under_master_and_sms"),

    ("D", "promote shore replication from system-specific to asserted fact",
     sub_in_file(QB5CB,
                 "that is a <em>system-specific</em> arrangement whose "
                 "evidentiary status is for the company and the investigating "
                 "authority to establish &mdash; it is not a fleet-wide "
                 "capability I would assert to an examiner, and it never "
                 "substitutes for preserving the originals on board.",
                 "that replication is what preserves the record."),
     "q5_shore_replication_is_system_specific_not_asserted"),

    ("E", "reinstate the sole-Indian-national claim in the casualty block",
     sub_in_file(QB5CB,
                 "the <strong>twenty surviving crew were evacuated by the "
                 "Indian Navy</strong>",
                 "the vessel&#x27;s sole Indian crew member was among the 20 "
                 "survivors evacuated by the Indian Navy"),
     "q5_no_sole_indian_national_claim"),

    ("F", "drop the verified bulk-carrier descriptor and the evacuation facts",
     sub_in_file(QB5CB,
                 "<strong>bulk carrier True Confidence (2024)</strong>",
                 "<strong>merchant vessel True Confidence (2024)</strong>"),
     "q5_true_confidence_verified_facts_retained"),

    ("G", "delete the training-scenario warning from the casualty block",
     sub_in_file(QB5CB,
                 "do not cite True Confidence to an examiner as an incident "
                 "involving Indian fatalities.",
                 "it is a useful illustration."),
     "q5_training_scenario_warning_survives"),

    ("H", "reinstate the invented dry-bulk loading-computer requirement in q27",
     sub_in_file(QB2A,
                 "<p>This is not a routine cargo regime on the container "
                 "vessels I have sailed.",
                 "<p>Any specialized dry bulk charters require the vessel's "
                 "loading computer to be configured with approved IMSBC and "
                 "Grain modules. This is not a routine cargo regime on the "
                 "container vessels I have sailed."),
     "q27_no_dry_bulk_charter_invention"),

    # ---- the surface no digest in this repo pins ----------------------
    ("A2", "reinstate the barred claim in the governed correction-log note",
     sub_in_file(LOG,
                 "and the twenty surviving crew were evacuated by the Indian Navy.",
                 "the vessel's sole Indian crew member (of 20) survived."),
     "correction_log_note_free_of_barred_claim"),

    ("A3", "strip the verified facts out of the correction-log note",
     sub_in_file(LOG,
                 "True Confidence's three fatalities were two Filipino and one "
                 "Vietnamese national, and the twenty surviving crew were "
                 "evacuated by the Indian Navy.",
                 "True Confidence's crew nationalities did not match."),
     "correction_log_note_keeps_verified_facts"),

    ("O", "drop the governed correction log from the record's artefacts",
     edit_json(M_OMV, lambda d: d.__setitem__("artefacts", [])),
     "correction_log_declared_as_artefact"),

    # ============ FAMILY B: the LNG danger, and its over-import =========
    ("I1", "delete the asphyxiation danger from the list",
     sub_in_file(QB7D,
                 "<li><strong>Oxygen deficiency and asphyxiation.</strong> The "
                 "<strong>nitrogen</strong> used to purge and inert the transfer "
                 "line and the hose, and LNG <strong>vapour</strong> itself, are "
                 "simple asphyxiants: both displace air, and an oxygen-deficient "
                 "atmosphere gives <strong>no useful warning</strong> before it "
                 "disables a person. That is the reason behind the gas detection, "
                 "the upwind positioning and the essential-personnel-only rule "
                 "&mdash; they are people-safety controls, not just leak-finding."
                 "</li>\n",
                 ""),
     "q14_dangers_list_teaches_oxygen_deficiency"),

    ("I2", "sever the danger from purging and inerting, leaving only the vapour",
     sub_in_file(QB7D,
                 "The <strong>nitrogen</strong> used to purge and inert the "
                 "transfer line and the hose, and LNG <strong>vapour</strong> "
                 "itself, are simple asphyxiants: both displace air,",
                 "LNG <strong>vapour</strong> is a simple asphyxiant,"),
     "q14_asphyxiation_tied_to_purge_and_inerting"),

    ("I3", "delete the no-useful-warning property, keeping the mechanism",
     sub_in_file(QB7D,
                 "and an oxygen-deficient atmosphere gives <strong>no useful "
                 "warning</strong> before it disables a person.",
                 "and the atmosphere can become oxygen-deficient."),
     "q14_asphyxiation_states_no_useful_warning"),

    ("I4", "delete the link from the hazard to the controls it explains",
     sub_in_file(QB7D,
                 "That is the reason behind the gas detection, the upwind "
                 "positioning and the essential-personnel-only rule &mdash; they "
                 "are people-safety controls, not just leak-finding.",
                 "It is a recognised hazard of the operation."),
     "q14_asphyxiation_explains_the_existing_controls"),

    ("I5", "move the asphyxiation entry to the end of the dangers list",
     sub_in_file(QB7D,
                 "<li><strong>Oxygen deficiency and asphyxiation.</strong> The "
                 "<strong>nitrogen</strong>",
                 "<li><strong>Purge-gas note.</strong> See below.</li>\n"
                 "<li><strong>Oxygen deficiency and asphyxiation.</strong> The "
                 "<strong>nitrogen</strong>"),
     "q14_asphyxiation_placed_between_rpt_and_rollover"),

    # OVER-CORRECTION. The fix landed, and then kept going.
    ("I", "import an enclosed-space entry permit regime into q14",
     sub_in_file(QB7D,
                 "they are people-safety controls, not just leak-finding.",
                 "they are people-safety controls. Any entry into the affected "
                 "area is an enclosed space entry under a permit to work, with "
                 "a stand-by man and a rescue team on station."),
     "q14_no_entry_or_confined_space_material_imported"),

    ("I6", "drop the hazard from the 15-second oral layer",
     sub_in_file(QB7D,
                 "<strong>RPT</strong> on water, and <strong>oxygen deficiency"
                 "</strong> from purge nitrogen and from the vapour itself.",
                 "and <strong>RPT</strong> on water."),
     "q14_short_layers_carry_the_hazard"),

    # ============ FAMILY C: grain wording, and the ACCEPTED card ========
    ("Q", "reinstate the rejected terminology in the q11 heading",
     sub_in_file(QB2A,
                 "<li><strong>Net Residual Area Between Heeling and "
                 "Righting-Arm Curves (A 7.1.2):</strong>",
                 "<li><strong>Net Residual Area on GZ Curve (A 7.1.2):</strong>"),
     "q11_heading_no_longer_says_area_on_gz_curve"),

    ("R", "assert 'the area under the GZ curve' in q11 outside a quotation",
     sub_in_file(QB2A,
                 "It comes from <strong>figure A7</strong> of the Code,",
                 "It is the area under the GZ curve, and it comes from "
                 "<strong>figure A7</strong> of the Code,"),
     "q11_no_unquoted_area_under_gz_curve_claim"),

    ("S", "delete the figure-A7 start point from q11",
     sub_in_file(QB2A,
                 "It comes from <strong>figure A7</strong> of the Code, which "
                 "shades the &ldquo;residual dynamic stability&rdquo; area from "
                 "the <strong>first intersection</strong> of the heeling arm "
                 "line with the righting arm curve",
                 "It is a matter of interpretation"),
     "q11_teaches_the_figure_a7_start_point"),

    ("T", "relabel the derived lower bound as A 7.1.2 clause text",
     sub_in_file(QB2A,
                 "<em>The LOWER bound is not in the clause at all: A 7.1.2 "
                 "states only the upper limit.",
                 "<em>The LOWER bound is stated by A 7.1.2 itself as the angle "
                 "of equilibrium."),
     "q11_lower_bound_not_quoted_as_clause_text"),

    # OVER-CORRECTION. q33 is ACCEPTED; the brief forbade touching it.
    ("J", "equalise QB2_A#q33 with q11 for symmetry, which the brief forbade",
     sub_in_file(QB2A,
                 "MSC.552(108) adds a <strong>third</strong>.",
                 "MSC.552(108) adds a <strong>third</strong> configuration, "
                 "taken from the angle of equilibrium per figure A7."),
     "accepted_and_deferred_cards_unmoved"),

    # OVER-CORRECTION. The Herschberg typo was DEFERRED, not authorised.
    ("K", "fix the DEFERRED Herschberg typo without an authorisation",
     sub_in_file(QB5CA, "Herschberg", "Herzberg"),
     "accepted_and_deferred_cards_unmoved"),

    # ============ FAMILY D: the IMSBC attribution =======================
    ("U", "restore SOLAS chapter VII as the sole basis in the 15-second layer",
     sub_in_file(QB2B,
                 "The IMSBC Code provides a mandatory framework for solid bulk "
                 "cargoes under <strong>SOLAS Chapter VI</strong>, the "
                 "carriage-of-cargoes chapter that gives it force generally; "
                 "<strong>Chapter VII Part A-1</strong> adds the regime for the "
                 "subset that is <em>dangerous goods in solid form in bulk</em>.",
                 "The IMSBC Code provides a mandatory framework under SOLAS "
                 "Chapter VII to manage the risks of transporting solid bulk "
                 "cargo."),
     "q15_chapter_vii_no_longer_stands_alone"),

    ("U2", "strip Part A-1 out of the 60-second layer, leaving a bare VI",
     sub_in_file(QB2B,
                 "with <strong>Chapter VII Part A-1</strong> governing the "
                 "subset that is <em>dangerous goods in solid form in bulk</em>. ",
                 ""),
     "q15_chapter_vii_scoped_to_part_a1"),

    ("U3", "delete the cargo groups from the 15-second layer while in there",
     sub_in_file(QB2B,
                 "<strong>Group A</strong> (liquefiable cargoes), "
                 "<strong>Group B</strong> (chemical hazards), and "
                 "<strong>Group C</strong> (physically stable cargoes)",
                 "three groups"),
     "q15_cargo_groups_untouched"),

    # ============ FAMILY E: currentness =================================
    ("P", "reinstate the founding-member status in the q4 CE Oral Tip",
     sub_in_file(QB5E,
                 "Know whether your own company is an MACN member &mdash; "
                 "Maersk, for one, helped establish MACN in 2011.",
                 "Know that your own company (Maersk) is a founding MACN member."),
     "macn_no_founding_member_status_claim"),

    ("P2", "drop the helped-establish wording from the On My Vessel block",
     sub_in_file(QB5E,
                 "Container (Maersk — helped establish MACN in 2011)",
                 "Container (Maersk — an MACN participant)"),
     "macn_helped_establish_wording_used"),

    ("V", "reinstate 'the 2026 edition' as an assertion in q13",
     sub_in_file(QB4H,
                 "The current edition is the <strong>1st Edition (2025)"
                 "</strong>, updated in 2026.",
                 "The current edition is <strong>2026</strong>."),
     "bmp_no_unquoted_2026_edition_claim"),

    ("V2", "invent a second edition of BMP Maritime Security",
     sub_in_file(QB4H,
                 "There is no second edition &mdash; say",
                 "The 2nd Edition superseded it &mdash; say"),
     "bmp_no_second_edition_invented"),

    ("V3", "restore the Common CE Failures entry the correction falsified",
     sub_in_file(QB4H,
                 "Teaching BMP5 as current, or calling BMP MS &ldquo;the 2026 "
                 "edition&rdquo; &mdash; the publishers label it the 1st "
                 "Edition, 2025, updated during 2026, and there is no second "
                 "edition.",
                 "Teaching BMP5, or the 2025 first edition, as current."),
     "bmp_common_ce_failure_entry_repaired"),

    ("V4", "delete the activist-boarding substance while relabelling the edition",
     sub_in_file(QB4H,
                 "&ldquo;Actions on Boarding by Activists&rdquo;, placed in "
                 "Section 6, Incident Response",
                 "a new section"),
     "bmp_2026_update_substance_intact"),

    ("X", "collapse the ISO published / under-development distinction",
     sub_in_file(QB7D,
                 "<strong>ISO 23306:2020 remains the CURRENT PUBLISHED "
                 "International Standard</strong> for LNG marine-fuel "
                 "specification as at September 2026, and it is the edition to "
                 "quote; ISO has however flagged it <strong>&ldquo;to be "
                 "revised&rdquo;</strong> and a second edition is "
                 "<strong>UNDER DEVELOPMENT</strong> as <strong>ISO/AWI 23306"
                 "</strong>, the new work item having been registered on 3 "
                 "August 2026. An AWI is a work item, not a published standard "
                 "&mdash; do not order fuel to it and do not quote it as "
                 "current.",
                 "ISO 23306:2020 is the standard, and no later edition or "
                 "superseding standard has been issued or is underway."),
     "iso23306_current_published_edition_stated"),

    ("X2", "state the AWI as the standard to order to",
     sub_in_file(QB7D,
                 "An AWI is a work item, not a published standard &mdash; do "
                 "not order fuel to it and do not quote it as current.",
                 "ISO/AWI 23306 is required for new orders."),
     "iso23306_awi_not_stated_as_current_or_mandatory"),

    ("Y", "strip the date back out of the regulation 16 currency claim",
     sub_in_file(QB3C,
                 "Scope the claim rather than making it absolute: <em>no later "
                 "IMO amendment affecting the regulation 16 incineration "
                 "provisions was identified in the held in-force chain, or in "
                 "the current IMO Annex VI amendment index, as at September "
                 "2026</em> &mdash; the recent amendments concern other "
                 "provisions, the emission control areas and the NO<sub>x</sub> "
                 "Technical Code. So the current text is the MEPC.328(76) text.",
                 "No amendment in the held in-force chain touches it, so the "
                 "current text is the MEPC.328(76) text."),
     "reg16_currency_claim_is_scoped_and_dated"),

    ("Y2", "upgrade the scoped negative to an exhaustive historical one",
     sub_in_file(QB3C,
                 "<li><strong>Regulation 16 is unamended.</strong> Scope the "
                 "claim rather than making it absolute:",
                 "<li><strong>Regulation 16 has never been amended since "
                 "MEPC.328(76).</strong> Scope the claim rather than making it "
                 "absolute:"),
     "reg16_no_exhaustive_never_amended_claim"),

    # ============ FAMILY F: the record, not the product =================
    ("L", "erase the BMP propagation report from the currency record",
     edit_json(M_CURR, lambda d: d["propagation"].__setitem__(
         "found_and_not_swept", [])),
     "bmp_propagation_reported_not_swept"),

    ("M", "erase the K-4 source-custody gap from the authorisation record",
     sub_in_file(AUTH,
                 "**REFERRED TO GPT, because it bears on how far that keep can "
                 "be trusted:** `MSC.551(108)` and\n`MSC.567(109)` are **NOT "
                 "held**",
                 "The amendments were verified externally. `MSC.551(108)` and\n"
                 "`MSC.567(109)` are held"),
     "k4_source_custody_gap_reported"),

    ("N", "erase the corrections to the brief's own factual premises",
     sub_in_file(AUTH, "**Premise correction:**", "Note:"),
     "brief_premise_corrections_recorded"),

    ("N2", "erase the record of the deferred typo and empty layers",
     sub_in_file(AUTH,
                 '**P2 typo, QB5_C_A#q1** — "Herschberg\'s Two-Factor Theory" '
                 'should be "Herzberg\'s". **DEFERRED.**',
                 "Nothing further is outstanding."),
     "deferred_items_recorded_with_reasons"),

    ("Z", "fabricate a supersession ancestor for QB4_H#q13",
     edit_json(M_CURR, lambda d: d["cards"][0].__setitem__(
         "supersedes", {"manifest": "batch_h4_manifest.json",
                        "action_id": "H4-004",
                        "post_edit_digest": d["cards"][0]["pre_edit_digest"]})),
     "supersession_ancestry_declared"),

    ("Z2", "downgrade a record from AUTHORISED to SUPERSEDED",
     edit_json(M_LNG, lambda d: d.__setitem__("status", "SUPERSEDED")),
     "correction_records_authorised"),

    ("Z3", "drop the IMSBC record's declared card, leaving eight",
     edit_json(M_IMSBC, lambda d: d.__setitem__("cards", d["cards"][:0] or [])),
     "all_nine_cards_declared"),

    ("Z4", "deny that the grain record moves nothing in the content index",
     edit_json(M_GRAIN, lambda d: d.__setitem__("content_index_effect", "")),
     "content_index_effects_declared"),

    # ============ FAMILY G: the surfaces the brief froze =================
    ("W", "advance the hub date the brief said not to touch",
     sub_in_file(HUB,
                 '<span class="stat-val" id="stat-updated">2 Sep 2026</span>',
                 '<span class="stat-val" id="stat-updated">5 Sep 2026</span>'),
     "hub_date_not_advanced"),

    ("W2", "restate the corpus total as a number the corpus does not carry",
     edit_json(INDEX, lambda d: d.__setitem__("total_questions", 762)),
     "corpus_totals_unmoved"),
]


if __name__ == "__main__":
    raise SystemExit(run_suite(
        "mutation suite: GPT high-risk review tranche 2C content gate",
        PROBE, MUTATIONS,
        [QB2A, QB2B, QB3C, QB4H, QB5CA, QB5CB, QB5E, QB7D, HUB, LOG, INDEX,
         AUTH, M_OMV, M_LNG, M_GRAIN, M_IMSBC, M_CURR]))
