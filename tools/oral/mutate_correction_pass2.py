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
from oral_content_mutation import run_suite, sub_in_file  # noqa: E402

enable_utf8_stdio()

QB4_E = QB / "QB4_E.html"
QB4_C = QB / "QB4_C.html"
QB8_A = QB / "QB8_A.html"
QB5_A = QB / "QB5_A.html"
QB3_A = QB / "QB3_A.html"
QB10_B = QB / "QB10_B.html"
QB3_B = QB / "QB3_B.html"

GATE = "validate_correction_pass2.py"
WATCHED = [QB4_E, QB4_C, QB8_A, QB5_A, QB3_A, QB10_B, QB3_B]

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
]


def main() -> int:
    return run_suite("Pass-2 known-defect remediation -- mutation suite",
                     GATE, MUTATIONS, WATCHED)


if __name__ == "__main__":
    raise SystemExit(main())
