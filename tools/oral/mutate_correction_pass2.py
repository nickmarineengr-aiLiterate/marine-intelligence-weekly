#!/usr/bin/env python3
"""Mutation suite for the six Pass-2 corrections.

Every mutation reverts a real defect in ONE layer and leaves the other
corrected layers standing, because that is the state these cards were actually
found in: QB4_E carried a correct list of twelve underneath three layers that
said eleven, and QB10_B carried the lowering-speed claim in a formula block and
again in Numbers to Memorise. A card-wide "is the right text present anywhere"
check passes on both of those, which is why each layer is guarded by name and
why the mutations attack them one at a time.

Where a defect could be restated, it is restated in DIFFERENT WORDS rather than
by reverting the old string -- B spells the count out, K renames the verb, N
changes the figure. A gate that only knows the original spelling escapes those,
and that is the escape class trap 116 records.

Two mutations attack rendering rather than wording: R reintroduces the
unescaped "<" at a fresh site with different surrounding text, and S proves the
rendered-text check is not merely a source-text check wearing a different name.

Serial. Byte-exact restoration verified after every mutation.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio  # noqa: E402
from oral_bytes import read_text, write_text  # noqa: E402
from oral_content_mutation import edit_json, run_suite, sub_in_file  # noqa: E402

enable_utf8_stdio()

QB4_E = QB / "QB4_E.html"
QB4_C = QB / "QB4_C.html"
QB8_A = QB / "QB8_A.html"
QB5_A = QB / "QB5_A.html"
QB3_A = QB / "QB3_A.html"
QB10_B = QB / "QB10_B.html"
QB3_B = QB / "QB3_B.html"
QB4_A = QB / "QB4_A.html"
QB4_A_CS = QB / "QB4_A_CheatSheet.html"
QB1_C = QB / "QB1_C.html"
QB1_G = QB / "QB1_G.html"
NOTES_P7 = QB / "oralnotes" / "miw-notes-mgmt-p7.html"
SIMON_P2 = QB / "oralnotes" / "simon-notes-p2.html"
SIMON_P6 = QB / "oralnotes" / "simon-notes-p6.html"
IDX_GOV = REPO / "tools" / "oral" / "qb_content_index_governed.json"

def _strip_instrument(path):
    """Remove every ITC-Hulls attribution from one file, keeping the substance.

    A card-wide "does the instrument appear anywhere" check cannot be tested by
    deleting one of three mentions. This deletes all of them and leaves the
    teaching otherwise intact, so only the attribution is on trial.
    """
    def apply():
        text = read_text(path)
        assert "ITC-Hulls" in text or "Institute Time Clauses" in text
        text = text.replace("Institute Time Clauses &ndash; Hulls (1/11/95) cl. 5.1",
                            "the standard hull policy")
        text = text.replace("ITC-Hulls (1/11/95) cl. 5.1", "the standard hull policy")
        text = text.replace("ITC-Hulls cl. 5.1", "the standard hull policy")
        text = text.replace("ITC-Hulls", "the standard hull policy")
        write_text(path, text)
    return apply


# SUPERSEDED LITERALS, 8 Sep 2026. Four anchors in this file quoted the
# ITC-Hulls citation as "cl. 4.2". CORR-ITC51-20260908 corrected that citation
# to cl. 5.1 across all fourteen candidate-facing sites, which left Z7b's
# search target absent from QB4_A - and a mutation whose target has moved does
# not fail loudly, it either crashes on the assert or silently no-ops. The
# anchors are re-pointed at the corrected text so this suite keeps testing the
# proposition it was written for. Nothing about what Z7b and Z7c PROVE has
# changed; only the bytes they reach for. See known_traps 132.
def _stale_pass2_entry(d):
    """Move the Pass-2 entry's date off 2026-09-07, wherever it now sits."""
    for e in d["recently_updated"]:
        if e.get("date") == "2026-09-07":
            e["date"] = "2026-09-04"
            return
    raise AssertionError("no 2026-09-07 entry in the governed correction log")


GATE = "validate_correction_pass2.py"
WATCHED = [QB4_E, QB4_C, QB8_A, QB5_A, QB3_A, QB10_B, QB3_B, QB4_A,
           QB4_A_CS, QB1_C, QB1_G,
           NOTES_P7, SIMON_P2, SIMON_P6, IDX_GOV]

MUTATIONS = [
    # ---------------------------------------------------------------- IACS
    ("A", "drop KR from the 60s list, leave the 15s answer corrected",
     sub_in_file(QB4_E,
                 "<strong>Korean Register (KR)</strong>, Lloyd's Register (LR)",
                 "Lloyd's Register (LR)", count=1),
     "iacs_60s_enumerates_all_twelve_societies"),

    ("B", "restore the count hedge SPELLED OUT - no digits at all",
     sub_in_file(QB4_E,
                 "There is no “11 or 12” to hedge over — the current figure is twelve.",
                 "The register stands at eleven or twelve members depending on whether "
                 "Türk Loydu is counted.", count=1),
     "iacs_no_count_ambiguity_hedge"),

    ("C", "restore 'eleven members' in the CE tip only, both answers left right",
     sub_in_file(QB4_E,
                 "so IACS stands at twelve Members today.",
                 "so IACS consists of eleven members today.", count=1),
     "iacs_no_layer_claims_eleven_members"),

    ("D", "reinstate the authoring scaffold in the CE tip",
     sub_in_file(QB4_E,
                 "This proves you read current maritime news.</p></div>",
                 "This proves you read current maritime news.</p>\r\n"
                 "          <p>Below are Q13-Q15 drafted in the exact required "
                 "chat-ready format.</p></div>", count=1),
     "iacs_scaffold_removed"),

    # ---------------------------------------------------------------- PR1C
    ("E", "make an overdue CoC automatic again, in the 60s layer only",
     sub_in_file(QB4_C,
                 "instead make the vessel <strong>subject to a suspension procedure</strong> "
                 "(A.2.1, A.1.4) — that is not automatic",
                 "instead suspend classification automatically as well (A.2.1, A.1.4) — the "
                 "two triggers behave alike", count=1),
     "pr1c_procedure_limb_is_condition_of_class"),

    ("F", "restore the universal insurance claim with a DIFFERENT verb",
     sub_in_file(QB4_C,
                 "<li>Insurance: PR1C contains no insurance provision at all,",
                 "<li>Insurance: suspension of class invalidates P&amp;I and H&amp;M "
                 "coverage in every case,", count=1),
     "pr1c_no_universal_insurance_void_claim"),

    ("G", "restore 'all statutory certificates' in the consequences bullet only",
     sub_in_file(QB4_C,
                 "is to state that <strong>certain</strong> statutory certificates are "
                 "implicitly invalidated",
                 "is to state that every statutory certificate is invalidated", count=1),
     "pr1c_no_all_statutory_certificates_claim"),

    ("H", "re-cite UR Z15 in the Numbers block, leaving the reg box on PR1C",
     sub_in_file(QB4_C,
                 "<p><strong>IACS PR1C Rev.7</strong> (Nov 2024, applies from 1 January 2026):",
                 "<p><strong>IACS UR Z15</strong> defines the procedural requirements:",
                 count=1),
     "pr1c_no_ur_z15_attribution"),

    # I and I2 are a pair, and the pair is the point. Each deletes the B.1.1
    # notification limb from ONE spoken layer and leaves the other carrying it.
    # A single card-wide check passes on both, because the surviving layer
    # satisfies it -- which is how the first draft of this gate let I escape.
    ("I", "delete the Owner/Flag limb from the 60s, leaving the 15s carrying it",
     sub_in_file(QB4_C,
                 "The Society must confirm the suspension in writing to the Owner and to the "
                 "Flag State (B.1.1), and for",
                 "For", count=1),
     "pr1c_60s_owner_and_flag_notification_taught"),

    ("I2", "delete the Owner/Flag limb from the 15s, leaving the 60s carrying it",
     sub_in_file(QB4_C,
                 "Under IACS PR1C the Society confirms either in writing to the Owner and the "
                 "Flag State, and for SOLAS ships that letter states",
                 "Under IACS PR1C, for SOLAS ships the notification letter states", count=1),
     "pr1c_15s_owner_and_flag_notification_taught"),

    # ------------------------------------------------------------ ALLIANCE
    ("J", "offer 2M as a current example again, in the 15s layer only",
     sub_in_file(QB8_A,
                 "(as at 2026: Gemini Cooperation, Ocean Alliance, Premier Alliance)",
                 "(e.g., 2M, Ocean Alliance)", count=1),
     "alliance_2m_not_offered_as_current_example"),

    ("K", "give the BAF back to the engine room, with a new verb and noun",
     sub_in_file(QB8_A,
                 "It is set and administered by the carrier&#x27;s commercial department",
                 "The surcharge is administered by the engine department&#x27;s consumption "
                 "reporting", count=1),
     "alliance_no_engine_room_owns_baf_claim"),

    ("L", "make the CBER merely 'historical' again, dropping the expiry",
     sub_in_file(QB8_A,
                 "it <strong>expired on 25 April 2024</strong>",
                 "it is now largely of historical interest", count=1),
     "alliance_cber_expiry_taught"),

    ("M", "restore the Ever Given sole-cause claim for the SCFI record",
     sub_in_file(QB8_A,
                 "The blockage took effective capacity out of the market for weeks, and spot "
                 "rates rose sharply.",
                 "The sudden restriction in available vessel space across major alliances led "
                 "to an unprecedented increase in container spot rates, with the SCFI index "
                 "hitting historic highs.", count=1),
     "alliance_no_scfi_sole_cause_claim"),

    # --------------------------------------------------------------- HUMAN
    ("N", "restore the fabricated anecdote with a DIFFERENT recovery figure",
     sub_in_file(QB5_A,
                 "<p>Answer this from your own ship, and keep it to what you actually did.",
                 "<p>Morale recovered within 36 hours of restoring the roster. "
                 "Answer this from your own ship, and keep it to what you actually did.",
                 count=1),
     "human_no_invented_recovery_time"),

    ("O", "empty the year out of the Numbers block, leaving the level count",
     sub_in_file(QB5_A,
                 "<li><strong>1943</strong> — Maslow&#x27;s paper",
                 "<li>— Maslow&#x27;s paper", count=1),
     "human_numbers_block_carries_the_year"),

    ("P", "re-attach fair treatment to MLC Reg. 1.4",
     sub_in_file(QB5_A,
                 "<td>STCW (competency recognition and certification). <strong>No MLC hook "
                 "here</strong> — MLC Reg. 1.4 is <em>Recruitment and placement</em>, not "
                 "fair treatment,",
                 "<td>STCW (competency recognition), MLC Reg. 1.4 (Recruitment / Fair "
                 "Treatment),", count=1),
     "human_no_mlc_1_4_fair_treatment_attribution"),

    # ------------------------------------------------------------- CLOSEUP
    ("Q", "widen the close-up scope back to all bulkers and tankers",
     sub_in_file(QB3_A,
                 "so it is <strong>not</strong> an oil tanker requirement",
                 "and it applies to oil tankers on the same terms", count=1),
     "closeup_scoped_to_single_side_skin_bulk_carriers"),

    ("Q2", "drop the extent and hold scope again, keeping the population right",
     sub_in_file(QB3_A,
                 "a close-up examination of at least <strong>25% of cargo hold side shell "
                 "frames</strong>, their lower end attachments and adjacent shell plating, "
                 "in a forward cargo hold and one other selected hold",
                 "a close-up examination of cargo hold side shell frames and their end "
                 "attachments", count=1),
     "closeup_extent_restated"),

    # --------------------------------------------------------------- AMEND
    ("R", "reintroduce an unescaped '<' at a FRESH site with new wording",
     sub_in_file(QB10_B,
                 "<strong>3,000 GT:</strong> threshold for mandatory electronic inclinometers",
                 "<strong>3,000 GT:</strong> ships <3,000 GT are outside the requirement; "
                 "threshold for mandatory electronic inclinometers", count=1),
     "amend_lt_before_numeral_is_escaped"),

    # Rewritten after trap 126. Two earlier drafts of this mutation were both
    # wrong, in opposite directions, and the sequence is the lesson:
    #   draft 1  "<on ships over 500 GT>" - closes itself, eats only itself
    #   draft 2  "<em comply ..."          - eats text, and the gate CAUGHT it,
    #            which felt like proof. It was not: the gate modelled "<" plus
    #            ANY character as tag-opening, so mutation and gate shared one
    #            wrong model of HTML and agreed with each other.
    # A browser opens a tag only on "<" plus an ASCII LETTER. So the damaging
    # form is an unclosed opening whose name is not a real element, and that is
    # what the gate now tests against a real element list.
    ("S", "unclosed non-element opening - the form that actually eats text",
     sub_in_file(QB10_B,
                 "New installations comply immediately from 1 Jan 2028;",
                 "New installations <clause comply immediately from 1 Jan 2028;",
                 count=1),
     "amend_no_unclosed_pseudo_tag_eating_text"),

    ("S2", "a '<' before a numeral is NOT the same defect - hygiene only",
     sub_in_file(QB10_B,
                 "(e.g. &lt;150 GT, fishing vessels)",
                 "(e.g. <150 GT, fishing vessels)", count=1),
     "amend_lt_before_numeral_is_escaped"),

    ("T", "say the formula is gone using 'superseded' instead of 'replaces'",
     sub_in_file(QB10_B,
                 "<strong>The formula is not abolished</strong> — 1.0 m/s is a ceiling on the "
                 "formula-derived minimum",
                 "The old H-dependent formula is superseded by the flat range — 1.0 m/s is now "
                 "the minimum", count=1),
     "amend_formula_block_no_formula_replaced_claim"),

    ("U", "revert ONLY the Numbers block, leaving the formula block correct",
     sub_in_file(QB10_B,
                 "minimum is <em>S</em> = 0.4 + 0.02<em>H</em> or 1.0 m/s, whichever is less; "
                 "maximum 1.3 m/s unless the Administration accepts another. The formula still "
                 "stands.",
                 "new lifeboat lowering speed range of 1.0-1.3 m/s, replacing the old "
                 "H-dependent formula.", count=1),
     "amend_numbers_block_carries_the_formula"),

    ("V", "restore 'removed' for the III/33.2 amendment",
     sub_in_file(QB10_B,
                 "The effect is to confine the 5-knot headway launch capability to "
                 "davit-launched lifeboats",
                 "The effect is that SOLAS III/33 removed the 5-knot headway requirement",
                 count=1),
     "amend_no_requirement_removed_claim"),

    ("W", "give MSC.559(108) the ventilation requirement itself back",
     sub_in_file(QB10_B,
                 "<strong>MSC.559(108)</strong> — amendments to the Requirements for "
                 "maintenance, thorough examination, operational testing, overhaul and repair "
                 "of lifeboats and rescue boats, launching appliances and release gear "
                 "(resolution MSC.402(96)),",
                 "<strong>MSC.559(108)</strong> — the lifeboat ventilation testing regime,",
                 count=1),
     "amend_msc559_named_as_amending_msc402"),

    ("X", "restore the self-dating currency claim with a different month",
     sub_in_file(QB10_B,
                 "that package entered into force on 1 January 2026 and has been in force ever "
                 "since",
                 "it is now late-2026 and that entire package is already in force", count=1),
     "amend_no_self_dating_currency_claim"),
    # ---------------------------------------------------- review escapes
    # Every mutation below was proposed by the clean-context verifier as one
    # it believed WOULD escape the first draft of the gate. Each did. They are
    # kept as the standing proof that the checks written to close them work.
    ("Y1", "wrong lowering-speed MAXIMUM - the provision this record exists to fix",
     sub_in_file(QB10_B,
                 "The maximum lowering speed shall be <strong>1.3 m/s</strong>",
                 "The maximum lowering speed shall be <strong>2.3 m/s</strong>", count=1),
     "amend_formula_block_maximum_is_1_3_ms"),

    ("Y2", "put Maersk in Premier Alliance - right names, wrong members",
     sub_in_file(QB8_A,
                 "<strong>Premier Alliance</strong> (ONE, HMM, Yang Ming",
                 "<strong>Premier Alliance</strong> (ONE, HMM, Maersk", count=1),
     "alliance_membership_correct_premier"),

    ("Y3", "delete the age condition from the close-up requirement",
     sub_in_file(QB3_A,
                 "The requirement is also <strong>age-conditioned</strong>; this card "
                 "does not state the age band, because it could not be verified against "
                 "Z10.2 directly — check the applicable clause before quoting a "
                 "threshold in an oral. ",
                 "", count=1),
     "closeup_is_age_conditioned"),

    ("Y4", "restore the unqualified certificate claim in the CE Oral Tip ONLY",
     sub_in_file(QB4_C,
                 "under PR1C B.1.3 that letter states that <em>certain</em> statutory "
                 "certificates are implicitly invalidated — not all of them — and trading "
                 "on that basis exposes us",
                 "operating under either status invalidates our statutory certificates "
                 "and exposes us", count=1),
     "pr1c_ce_tip_no_unqualified_certificate_claim"),

    ("Y5", "let QB3_B's memorisation layer drift back to bulk carriers/tankers",
     sub_in_file(QB3_B,
                 "<strong>single side skin bulk carriers only</strong> (UR Z10.2; not oil "
                 "tankers), forward hold + one other selected hold, and age-conditioned.",
                 "(bulk carriers/tankers), forward hold + one other selected hold.",
                 count=1),
     "closeup_sibling_numbers_layer_not_over_broad"),
    # ------------------------------------------- second-review escapes
    # Z1-Z3 are the escapes the SECOND independent review demonstrated in a
    # sandbox against the hardened gate. Each is kept as standing proof that
    # the fix works, because each exploited a different way for an absence
    # check to be true-by-accident.
    ("Z1", "reinstate the P1 defect behind a bare 'no' in the same sentence",
     sub_in_file(QB4_C,
                 "This demonstrates a strong compliance-driven approach.",
                 "Make no mistake, sir, every statutory certificate is invalidated the "
                 "moment class is suspended. This demonstrates a strong compliance-driven "
                 "approach.", count=1),
     "pr1c_ce_tip_no_unqualified_certificate_claim"),

    ("Z2", "universal insurance loss with a verb the first list did not carry",
     sub_in_file(QB4_C,
                 "<li>Insurance: PR1C contains no insurance provision at all,",
                 "<li>Insurance: once class is suspended our P&amp;I and H&amp;M cover is "
                 "forfeited outright in every case,", count=1),
     "pr1c_no_universal_insurance_void_claim"),

    ("Z3", "widen QB3_B's Numbers layer without the parenthesised spelling",
     sub_in_file(QB3_B,
                 "forward hold + one other selected hold, and age-conditioned.",
                 "forward hold + one other selected hold; in practice it is applied to "
                 "bulk carriers and tankers generally.", count=1),
     "closeup_sibling_numbers_layer_not_over_broad"),

    # ------------------------------------------------- QB4_A#q9, 8th card
    # The card the PR1C record's sweep claimed did not exist. Each mutation
    # reverts one layer and leaves the rest corrected.
    ("Z4", "restore 'all statutory certificates' in the cascade bullet only",
     sub_in_file(QB4_A,
                 "Under PR1C B.1.3 the Society&#x27;s letter states that "
                 "<strong>certain</strong> statutory certificates",
                 "All statutory certificates", count=1),
     "qb4a_no_all_statutory_certificates_claim"),

    ("Z5", "make an overdue CoC automatic again in the 60s layer",
     sub_in_file(QB4_A,
                 "IACS PR1C A.2.1 provides that the vessel&#x27;s class becomes "
                 "<strong>subject to a suspension procedure</strong>",
                 "the society suspends class automatically", count=1),
     "qb4a_coc_is_a_suspension_procedure"),

    ("Z6", "re-cite UR Z23 for the Flag State notification",
     sub_in_file(QB4_A,
                 "<strong>IACS PR1C B.1.1</strong>, with B.1.2 covering withdrawal",
                 "<strong>IACS UR Z23</strong>, with SOLAS Ch I/Reg 6", count=1),
     "qb4a_no_ur_z23_attribution"),

    ("Z7", "attribute the insurance consequence to PR1C again",
     sub_in_file(QB4_A,
                 "and the standard hull wording goes further than a warranty: Institute "
                 "Time Clauses",
                 "and under PR1C P&amp;I Club cover falls away automatically: Institute "
                 "Time Clauses", count=1),
     "qb4a_no_universal_insurance_loss_claim"),

    # Z7b reintroduces the trap-130 understatement, and is caught by the check
    # that forbids it. Z7c is its twin: it removes EVERY instrument mention
    # without adding the understatement, which is the only way to exercise the
    # instrument check on its own -- a card-wide presence check survives losing
    # one of three mentions, and that is how the first draft of Z7b escaped.
    ("Z7b", "reintroduce the trap-130 understatement",
     sub_in_file(QB4_A,
                 "Institute Time Clauses &ndash; Hulls (1/11/95) cl. 5.1 terminates hull "
                 "cover",
                 "the class warranty is breached so cover may be prejudiced; a policy "
                 "terminates hull cover", count=1),
     "qb4a_no_insurance_understatement"),

    ("Z7c", "strip EVERY instrument mention, leaving the substance correct",
     _strip_instrument(QB4_A),
     "qb4a_insurance_limb_names_its_instrument"),

    ("Z8", "restore the unqualified claim in QB4_A's CE Oral Tip only",
     sub_in_file(QB4_A,
                 "under PR1C B.1.3 the Society&#x27;s letter to Owner and Flag State says "
                 "that <em>certain</em> RO-issued statutory certificates are implicitly "
                 "invalidated",
                 "all RO-issued statutory certificates become invalid simultaneously",
                 count=1),
     "qb4a_ce_tip_no_unqualified_certificate_claim"),
    # -------------------------------------------- third-review escapes
    # X1-X5 are the five mutations the THIRD independent review demonstrated
    # walking past the gate in a sandbox. Each attacked a different disarm path
    # in asserts(), and all five now fail closed. They are the reason that
    # helper was rebuilt around a single rule -- a denial governs its own
    # clause and no further.
    ("X1", "CoC suspends automatically, in words the old literal check never held",
     sub_in_file(QB4_A,
                 "IACS PR1C A.2.1 provides that the vessel&#x27;s class becomes "
                 "<strong>subject to a suspension procedure</strong>",
                 "class is suspended automatically on the due date", count=1),
     "qb4a_coc_is_a_suspension_procedure"),

    ("X2", "assert the defect after a denial about a DIFFERENT subject",
     sub_in_file(QB4_C,
                 "<li>Insurance: PR1C contains no insurance provision at all,",
                 "<li>Insurance: PR1C is not an insurance document, yet our cover falls "
                 "away the moment class is suspended,", count=1),
     "pr1c_no_universal_insurance_void_claim"),

    ("X3", "assert the defect, then append a rhetorical question",
     sub_in_file(QB4_A,
                 "The ship cannot sail. I immediately inform the Master",
                 "Every statutory certificate is invalidated at once - what else could "
                 "&quot;implicitly invalidated&quot; mean? The ship cannot sail. I "
                 "immediately inform the Master", count=1),
     "qb4a_no_all_statutory_certificates_claim"),

    ("X4", "hide the defect behind an imperative 'Do not forget:'",
     sub_in_file(QB4_C,
                 "This demonstrates a strong compliance-driven approach.",
                 "Do not forget: all statutory certificates become invalid. This "
                 "demonstrates a strong compliance-driven approach.", count=1),
     "pr1c_ce_tip_no_unqualified_certificate_claim"),

    ("X5", "hide the defect behind a parenthetical 'whether or not'",
     sub_in_file(QB4_C,
                 "<li>Insurance: PR1C contains no insurance provision at all,",
                 "<li>Insurance: our cover, whether or not the club agrees, lapses "
                 "outright,", count=1),
     "pr1c_no_universal_insurance_void_claim"),

    # ------------------------------------------- derived + sibling surfaces
    ("X6", "restore the P0: the cheat sheet contradicting its own card",
     sub_in_file(QB4_A_CS,
                 "PR1C B.1.1 letter to Owner + Flag State; B.1.3 says "
                 "<strong>certain</strong> statutory certs implicitly invalidated (not all)",
                 "ALL RO-issued statutory certs invalid simultaneously", count=1),
     "cheatsheet_no_all_statutory_certs_claim"),

    ("X7", "re-cite the deleted PR No.1 on the cheat sheet",
     sub_in_file(QB4_A_CS,
                 "<td>IACS PR1C (suspension/withdrawal) + PR 35 (imposing/clearing CoC)</td>",
                 "<td>IACS PR No.1/3</td>", count=1),
     "cheatsheet_no_false_pr_citation"),

    ("X8", "restore the automatic-suspension claim on QB1_C q6",
     sub_in_file(QB1_C,
                 "IACS PR1C A.2.1 makes the vessel&#x27;s class <strong>subject to a "
                 "suspension procedure</strong>",
                 "there is automatic Suspension of Class", count=1),
     "qb1c_no_pr1c_family_defect"),

    ("X9", "restore the automatic insurance void on QB1_G q36",
     sub_in_file(QB1_G,
                 "On insurance, cite the policy and not PR1C: ITC-Hulls",
                 "Suspension automatically voids the vessel&#x27;s hull insurance. ITC-Hulls",
                 count=1),
     "qb1g_q36_no_pr1c_family_defect"),

    ("X10", "put the defect back on a surface the sweep must find",
     sub_in_file(QB4_E,
                 "IACS PR1C B.1.3 has the Society tell the Owner and the Flag State that "
                 "<em>certain</em> statutory certificates",
                 "all statutory certificates", count=1),
     "qb4e_q13_no_pr1c_family_defect"),
    # ------------------------------------------- terminal-closure classes
    # A-E guard the SOURCE-OWNED and GENERATED surfaces that sat outside every
    # earlier gate in this batch; F-L take one QB10_B proposition each; M and N
    # attack the two ways a resolved proposition can quietly come back.
    ("TA", "restore the deleted PR 1 as a live citation (simon-notes-p6)",
     sub_in_file(SIMON_P6,
                 '<span class="reg-code">IACS PR 35 / PR1C</span>',
                 '<span class="reg-code">IACS PR 1</span>', count=1),
     "notes_and_qb_no_bare_pr1_or_pr3_citation"),

    ("TB", "restore the PR 3 misattribution (simon-notes-p2)",
     sub_in_file(SIMON_P2,
                 '<span class="reg-code">IACS PR1C / PR 35</span>',
                 '<span class="reg-code">IACS PR No.3</span>', count=1),
     "notes_and_qb_no_bare_pr1_or_pr3_citation"),

    ("TC", "drop PR 35 from the instrument that imposes and clears a CoC",
     sub_in_file(SIMON_P6, "IACS PR 35 / PR1C", "IACS class rules", count=1),
     "notes_simon_notes_p6_cites_the_right_instrument"),

    ("TD", "make six months a suspension TRIGGER again (notes p7)",
     sub_in_file(NOTES_P7,
                 "The six-month figure is corrected rather than retained: under IACS",
                 "The 6-month automatic-suspension trigger is standard practice: under IACS",
                 count=1),
     "notes_p7_six_months_is_withdrawal_not_a_trigger"),

    # Selected by DATE, not by position. This mutation used to stale
    # recently_updated[0] on the assumption that index 0 is the Pass-2 entry.
    # CORR-ITC51-20260908 prepended an entry, so [0] became a different record
    # and TE staled that instead - the check it names stayed green and the
    # mutation ESCAPED, caught only by the generic determinism check. A guard
    # that indexes into a growing log expires the first time the log grows.
    ("TE", "stale the correction log after a rebuild",
     edit_json(IDX_GOV, _stale_pass2_entry),
     "qb_content_index_records_the_pass2_batch"),

    # ---- F-L: one per QB10_B proposition --------------------------------
    ("TF", "STCW-F: collapse Convention and amendments again",
     sub_in_file(QB10_B,
                 "the <em>Convention</em> itself (STCW-F 1995) has been in force since 2012",
                 "the Convention and Code both arrived together", count=1),
     "qb10b_stcwf_convention_vs_amendments"),

    ("TG", "Polar: drop the size thresholds back to a vague population",
     sub_in_file(QB10_B, "24 m LOA and above", "a certain size and above", count=1),
     "qb10b_polar_population_is_precise"),

    # Retired and replaced. The proposition TH guarded - "do not assert an
    # unverified pairing" - was itself wrong: the pairing IS verifiable, and the
    # fifth review found the card had removed a correct citation on a source gap
    # nobody had tested. The live risk is now the opposite one, so TH attacks
    # that instead: silently dropping the adoption date that ties the citation
    # to its claim.
    ("TH", "Polar: strip the adoption date that anchors the citation",
     sub_in_file(QB10_B, "adopted 8 June 2023, inserts", "inserts", count=1),
     "qb10b_polar_cites_msc538"),

    # Deleting the parenthetical is a NO-OP in teaching terms: the bullet
    # states both dates again in its own prose. The real defect is collapsing
    # designation into enforcement, so that is what this mutation does now.
    ("TI", "ECA: collapse designation into enforcement, one date for both",
     sub_in_file(QB10_B,
                 "the areas become ECAs on 1 March 2026",
                 "the areas become ECAs on 1 March 2027", count=1),
     "qb10b_eca_both_dates_present"),

    ("TJ", "Bulk Jupiter: restore the unsupported causal attribution",
     sub_in_file(QB10_B,
                 "the loss of the bulk carrier <em>Bulk Jupiter</em>",
                 "this traces directly to the bulk carrier <em>Bulk Jupiter</em>", count=1),
     "qb10b_no_unsupported_jupiter_causal_claim"),

    ("TK", "LRIT: strip the as-at date from a perishable status",
     sub_in_file(QB10_B,
                 "(status as at September 2026 &mdash; re-check before any sitting, this is a "
                 "moving item)",
                 "", count=1),
     "qb10b_lrit_is_as_at_dated"),

    ("TL", "MSC 112: present a future session as settled",
     sub_in_file(QB10_B,
                 "(December 2026, still a future session as at September 2026)",
                 "(December 2026)", count=1),
     "qb10b_msc112_is_as_at_dated"),

    # ---- M: an unsupported claim back in a memorisation layer ------------
    ("TM", "put the removed causal claim back in the Casualty Link layer only",
     sub_in_file(QB10_B,
                 "Use her to explain <em>why</em> recorded roll data matters",
                 "The requirement traces directly to her", count=1),
     "qb10b_no_unsupported_jupiter_causal_claim"),

    # ---- N: a source-gap claim restated as certain fact -------------------
    ("TN", "restate the liquefaction mechanism as a cargo shift",
     sub_in_file(QB10_B,
                 "she was lost to bauxite <strong>liquefaction</strong>, not a cargo shift",
                 "she was lost to a bauxite cargo shift", count=1),
     "qb10b_jupiter_named_and_mechanism_correct"),
    # ------------------------- fifth-review P1s, kept as standing proof
    # All three passed the terminal-closure gate green. Each is now attacked
    # by the check that was rebuilt to catch it.
    ("TR1", "swap the Polar chapter subjects back",
     sub_in_file(QB10_B,
                 "<strong>9-1, Safety of navigation</strong>, and "
                 "<strong>11-1, Voyage planning</strong>",
                 "<strong>9-1, Voyage planning</strong>, and "
                 "<strong>11-1, Safety of navigation</strong>", count=1),
     "qb10b_polar_chapter_subjects_not_swapped"),

    ("TR2", "call the Polar chapters regulations again",
     sub_in_file(QB10_B,
                 "inserts two new <strong>chapters</strong> into",
                 "inserts New regulations 9-1 and 11-1 into", count=1),
     "qb10b_polar_chapters_not_regulations"),

    ("TR3", "withdraw the verifiable Polar citation as a false source gap",
     sub_in_file(QB10_B, "MSC.538(107), adopted 8 June 2023, inserts",
                 "An unnamed resolution inserts", count=1),
     "qb10b_polar_cites_msc538"),

    ("TR4", "restore the phantom 2022 STCW-F amendments",
     sub_in_file(QB10_B,
                 "MSC.561(108), the revised annex to the 1995 Convention, and "
                 "MSC.562(108), the new STCW-F Code, both adopted 23 May 2024",
                 "the 2022 amendments and the new STCW-F Code", count=1),
     "qb10b_stcwf_no_phantom_2022_amendments"),
]


def main() -> int:
    return run_suite("Pass-2 known-defect remediation -- mutation suite",
                     GATE, MUTATIONS, WATCHED)


if __name__ == "__main__":
    raise SystemExit(main())
