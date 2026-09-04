#!/usr/bin/env python3
"""
Mutation suite for GPT REVIEW PASS 2B -- the four MS Act 2025 correction records.

WHAT THIS PROVES, AND WHAT IT DELIBERATELY DOES NOT
---------------------------------------------------
`validate_correction_msact2b.py` makes 54 assertions. A green validator proves
only that the assertions PASS today; it does not prove any of them would ever go
red, and a check that cannot fail is decoration with a nice name.

So each mutation below reintroduces one specific defect this pass corrected, and
must be caught by ITS OWN named content check. `run_suite` refuses any mutation
whose required catch is a digest pin, because every mutation trips a pin -- being
caught by one would prove nothing except that sha256 works.

THE THREE MUTATIONS THAT MATTER MOST ARE NOT THE OBVIOUS ONES
--------------------------------------------------------------
*   MUTATION H LAUNDERS THE HISTORY. It rewrites QB1_I's v1.2 line -- the entry
    recording that these rows were once re-based with a caveat -- so the card
    reads as though it were always correct. Nothing candidate-facing becomes
    false, every section citation stays right, and no fact check anywhere would
    notice. Brief section 6 exists precisely to forbid this, and
    `qb1i_v12_history_line_preserved` is the only thing that can see it.

*   MUTATION P SWEEPS A PAST PAPER. It writes the 2025 machinery into QP2512, a
    December 2025 sitting -- which looks like MORE correctness and is a defect:
    a present-day answer can never be written into a sitting-anchored paper. The
    corpus has no other guard that treats "fixing" a past paper as damage.

*   MUTATION R SILENTLY REPAIRS THE REGISTRY. It overwrites the locator claim
    with the corrected text alone, deleting the record that it was ever wrong.
    The claim ends up TRUE, which is why no correctness check can catch it;
    `registry_records_the_correction_transparently` catches it because the
    registry's own history convention is that a superseded entry is retained and
    marked, never overwritten.

Mutations A, B, C and D reintroduce the rejected wordings verbatim. Each must be
caught by the attribution test rather than by a flat phrase ban -- see the
validator's header for why that distinction is what keeps this guard honest, and
why a quoted-only exemption was tried and rejected.

MUTATION N IS THE INVERSE OF A. It does not reintroduce a defect at all: it
DELETES the denial sentence. The banned phrase then disappears from the page
entirely, so a naive negative check goes greener, not redder. Only
`denial_present_*` notices that the correction stopped teaching anything.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from oral_content_mutation import (                            # noqa: E402
    REPO, edit_json, run_suite, sub_in_file)

MEO = REPO / "meoclass1"
QB9H = MEO / "QB9_H.html"
QB9D = MEO / "QB9_D.html"
QB1I = MEO / "QB1_I.html"
QB3J = MEO / "QB3_J.html"
QB5B = MEO / "QB5_B.html"
QB5BCS = MEO / "QB5_B_CheatSheet.html"
QB5CB = MEO / "QB5_C_B.html"
QB9HCS = MEO / "QB9_H_CheatSheet.html"
P15 = MEO / "oralnotes" / "miw-notes-mgmt-p15.html"
P6 = MEO / "oralnotes" / "simon-notes-p6.html"
QP2512 = MEO / "pastpapers" / "QP2512.html"
REGISTRY = REPO / "docs" / "sources" / "MIW_SOURCE_REGISTRY.json"
TOOLS = REPO / "tools" / "oral"
REC_A = TOOLS / "correction_corr_msact2b_cehandover_20260904_manifest.json"
REC_C = TOOLS / "correction_corr_msact2b_casualty_20260904_manifest.json"

PROBE = "validate_correction_msact2b.py"


def drop_record(path):
    """Delete a correction record outright -- the collapse mutation."""
    def apply():
        path.unlink()
    return apply


MUTATIONS = [
    # ---------------------------------------------- the stale vocabulary
    ("A", "QB9_H#q2 reg-box goes back to teaching 'formal investigation' as 2025 machinery",
     sub_in_file(QB9H,
                 "administrative action and proceedings s.232. The Act does not use",
                 "administrative action, preliminary inquiry and formal investigation "
                 "under the MS Act 2025 s.232. The Act now uses"),
     "no_msact2025_claim_says_formal_investigation"),

    ("B", "QB9_H#q11 Key Numbers reverts to the 1958 pairing under the 2025 Act",
     sub_in_file(QB9H,
                 "marine safety investigation <strong>s.231(5)–(6)</strong> → "
                 "administrative action or proceedings <strong>s.232</strong>",
                 "formal investigation before a court with assessors under the "
                 "MS Act 2025 <strong>s.232</strong>"),
     "no_msact2025_claim_says_formal_investigation"),

    ("C", "QB5_C_B#q5 re-attributes formal investigation to the 2025 Act",
     sub_in_file(QB5CB,
                 "<strong>s.232</strong> administrative action or proceedings. "
                 "The 2025 Act does not use",
                 "<strong>s.232</strong> the formal investigation before a court. "
                 "The Merchant Shipping Act, 2025 uses"),
     "no_msact2025_claim_says_formal_investigation"),

    ("D", "simon-notes reg-box reverts to 'Part XI - preliminary inquiry and formal investigation'",
     sub_in_file(P6,
                 "administrative action or proceedings (s.232). The 2025 Act does not use",
                 "formal investigation of marine casualties (s.232). The MS Act 2025 uses"),
     "no_msact2025_claim_says_formal_investigation"),

    ("E", "p15 reverts to calling the restructure a '2025 renumbering'",
     sub_in_file(P15,
                 "This is a restructure, not a renumbering — the 2025 Act does not carry",
                 "This is a 2025 renumbering — the MS Act 2025 carries the "
                 "preliminary inquiry and formal investigation limbs forward, and carries"),
     "no_msact2025_claim_says_formal_investigation"),

    # ------------------------------------- deleting the teaching, not the term
    #
    # N REMOVES BOTH OF q2's DENIALS, and the first attempt at it is worth
    # recording. Deleting only the prose denial ESCAPED, correctly: q2's reg-box
    # carries a second one, so the card still told the candidate the Act does not
    # use the term. The mutation was wrong, not the gate. A mutation has to
    # represent the REAL risk -- the card ceasing to teach the denial at all --
    # and a card with two denials only loses it when both go.
    ("N", "QB9_H#q2 stops teaching the denial at all: BOTH its denial sentences are deleted",
     lambda: (sub_in_file(QB9H,
                          "Two cautions: the 2025 Act does <strong>not</strong> use the expression "
                          "“formal investigation” for this machinery — that was the "
                          "previous framework’s language — and",
                          "Note that")(),
              sub_in_file(QB9H,
                          "administrative action and proceedings s.232. The Act does not use "
                          "“formal investigation” for this machinery",
                          "administrative action and proceedings s.232")()),
     "denial_present_QB9_H_q2"),

    # ------------------------------------------------ the Part XI machinery
    ("F", "the 24-hour notice limb is dropped from QB9_H",
     sub_in_file(QB9H, "s.231(2)", "Part XI"),
     "part_xi_four_steps_QB9_H"),

    ("G", "certificate powers are folded back into the safety investigation",
     sub_in_file(QB9H, "s.312", "the investigating body"),
     "certificate_power_separated_to_s312"),

    ("V", "QB9_H#q11 overclaims: the Act is said to DEFINE 'very serious marine casualty'",
     sub_in_file(QB9H,
                 "it does <strong>not</strong> define the term, which remains Casualty "
                 "Investigation Code terminology",
                 "the Act defines “very serious marine casualty” in the same place"),
     "vsmc_boundary_stated_not_overclaimed"),

    # -------------------------------------------------- the CE handover hook
    ("H1", "the cheat sheet's handover row gets a Merchant Shipping Act section back",
     sub_in_file(QB5BCS,
                 "— <em>no MS Act 2025 provision governs CE handover",
                 "/ MS Act 2025, s.77 — <em>and no MS Act 2025 provision governs CE handover"),
     "cheatsheet_takeover_row_cites_no_act_provision"),

    ("H2", "the cheat sheet re-invents the statutory CE Takeover Certificate",
     sub_in_file(QB5BCS,
                 "no ISM clause prescribes a takeover certificate",
                 "ISM Code §5 prescribes the CE Takeover Certificate"),
     "cheatsheet_does_not_invent_an_ism_certificate"),

    ("H3", "QB5_B#q1 gets the unverifiable 1958 s.77 equivalence back",
     sub_in_file(QB5B,
                 "in force 15 March 2026. The 2025 Act contains",
                 "in force 15 March 2026, replacing the repealed 1958 Act, §77. "
                 "The 2025 Act contains"),
     "qb5b_q1_no_1958_s77_equivalence"),

    # -------------------------------------------------------- QB9_D's powers
    ("I", "QB9_D loses the s.312 limb, leaving Part IV to cover a power it cannot reach",
     sub_in_file(QB9D, "s.312", "Part IV"),
     "qb9d_has_s312_limb"),

    ("J", "QB9_D re-merges the powers and hands them back to the DGS",
     sub_in_file(QB9D,
                 "Furthermore, a Chief Engineer’s Certificate of Competency can be "
                 "withdrawn, suspended or cancelled under <strong>two separate powers, "
                 "and merging them is a common oral error</strong>.",
                 "Furthermore, under the broad powers of the MS Act, the DGS retains "
                 "the statutory right to conduct inquiries, suspend, or cancel a "
                 "Chief Engineer’s Certificate of Competency (CoC).",
                 1),
     "qb9d_powers_not_merged"),

    # ------------------------------------------------------------- QB1_I
    ("K", "QB1_I reverts to the pre-2025 noun 'Indian ship'",
     sub_in_file(QB1I, "an <strong>Indian vessel</strong> — the Act’s own term",
                 "an <strong>Indian ship</strong> — the Act’s own term"),
     "qb1i_uses_act_terminology_indian_vessel"),

    ("L", "QB1_I's register-book row loses s.20(9)",
     sub_in_file(QB1I, "s.20(9)", "Part III"),
     "qb1i_uses_s20_9"),

    ("H", "QB1_I's v1.2 history line is LAUNDERED so the card reads as always-correct",
     sub_in_file(QB1I,
                 "v1.2 · corrected 3 Aug 2026: residual reg-box rows re-based from "
                 "MS Act 1958 Sec 24/34 to MS Act 2025 Part III (exact sections pending "
                 "verification); prior v1.1 15 Jul 2026",
                 "v1.2 · 3 Aug 2026: reg-box rows verified against the MS Act 2025; "
                 "prior v1.1 15 Jul 2026"),
     "qb1i_v12_history_line_preserved"),

    # ------------------------------------------------------------- QB3_J
    ("M", "QB3_J claims the Act itself names NOS-DCP",
     sub_in_file(QB3J,
                 "The Act itself does not name NOS-DCP — that is a separate national "
                 "administrative plan, not a creature of these sections",
                 "These sections are the statutory basis on which the Act establishes "
                 "NOS-DCP as India’s national contingency plan"),
     "qb3j_does_not_claim_act_names_nosdcp"),

    # ---------------------------------------------------------- the registry
    ("R", "the registry locator is SILENTLY repaired, deleting the record of the error",
     edit_json(REGISTRY, lambda d: _silently_repair(d)),
     "registry_records_the_correction_transparently"),

    ("S", "the registry's s.324 saving drops the s.411A limb",
     edit_json(REGISTRY, lambda d: _drop_411a(d)),
     "registry_carries_s324_narrow_limb"),

    ("T", "the registry stops recording the control-byte extraction hazard",
     edit_json(REGISTRY, lambda d: _drop_hazard(d)),
     "registry_records_control_byte_hazard"),

    ("U", "claims_NOT_established reverts, so the registry contradicts what production cites",
     edit_json(REGISTRY, lambda d: _revert_not_established(d)),
     "registry_claims_not_established_narrowed"),

    # ----------------------------------------------------- scope and records
    ("P", "a PAST PAPER is 'improved' with the 2025 machinery it must never carry",
     sub_in_file(QP2512,
                 "<b>s.358</b> shipping casualties a",
                 "<b>MS Act 2025 s.231(2)</b> notice within twenty-four hours a"),
     "no_pastpaper_was_modified"),

    ("W", "the four records are collapsed: the stale-law record is deleted",
     drop_record(REC_C),
     "four_distinct_records_not_collapsed"),

    ("X", "the CE-handover record is deleted",
     drop_record(REC_A),
     "record_A_present"),

    ("Y", "the hub Last Updated is patched early, against the brief's report-only instruction",
     sub_in_file(MEO / "index.html", "2 Sep 2026", "4 Sep 2026"),
     "last_updated_reported_not_patched"),
]


# --- registry mutators ------------------------------------------------------
def _msact(d):
    return next(s for s in d["sources"] if s.get("source_id") == "SRC-MSACT-2025")


def _silently_repair(d):
    row = _msact(d)
    row["verified_claims"] = [
        c.split(" LOCATOR CORRECTED")[0] if "LOCATOR CORRECTED" in c else c
        for c in row["verified_claims"]]


def _drop_411a(d):
    row = _msact(d)
    row["verified_claims"] = [
        c.replace(" but not including section 411A therein", "")
        for c in row["verified_claims"]]


def _drop_hazard(d):
    row = _msact(d)
    row["verified_claims"] = [c.replace("0x03", "special")
                              for c in row["verified_claims"]]


def _revert_not_established(d):
    _msact(d)["claims_NOT_established"] = [
        "Section numbers outside s.4, s.5 and the Part V sections listed in verified_claims.",
        "The commencement notification S.O. 1244(E) itself (RQ-33).",
    ]


WATCHED = [QB9H, QB9D, QB1I, QB3J, QB5B, QB5BCS, QB5CB, QB9HCS, P15, P6,
           QP2512, REGISTRY, REC_A, REC_C, MEO / "index.html"]

if __name__ == "__main__":
    raise SystemExit(run_suite(
        "GPT REVIEW PASS 2B -- MS Act 2025 content mutation suite",
        PROBE, MUTATIONS, WATCHED))
