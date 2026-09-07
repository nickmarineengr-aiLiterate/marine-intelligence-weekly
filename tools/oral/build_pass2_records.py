#!/usr/bin/env python3
"""Emit the six Pass-2 correction manifests, one per defect family.

Bounded by family rather than by commit: the six cards this batch touched have
nothing in common except that Pass 1 left them open, so a single record would
have to claim one authority for six unrelated propositions. Each record names
the instrument that settled its own family, and each carries a `supersedes`
claim for every card an earlier record had pinned -- there are four.

Digests are recomputed from the worktree at emit time rather than typed in, so
a record can never pin a state that is not on disk.
"""
from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))

from review_pool import canonical_card_digests  # noqa: E402
from oral_bytes import read_text  # noqa: E402

DATE = "2026-09-07"
BASELINE = "05b49d8"
CONTENT_COMMIT = "78d703c"
#: The remediation round that closed the three P1s an independent clean-context
#: review found inside this batch's own declared scope. It is a governing commit
#: in its own right: two of the records below make claims that only became true
#: at this commit, and one WITHDRAWS a claim that was false at the first.
REMEDIATION_COMMIT = "5de0c08"

AUTH = ("MIW PASS 2 RESUMPTION - KNOWN-DEFECT REMEDIATION instruction of "
        "7 September 2026, sections 3-16. The instruction is explicitly NOT a "
        "discovery tranche: it authorises work only on already-known "
        "unresolved P1/P2 content defects, previously identified "
        "source-blocked items, bounded same-defect propagation, and "
        "already-classified structural residue. The unresolved queue was "
        "reconstructed from repository governance - "
        "meoclass1/oral-intelligence/examiner-audit/"
        "PASS1_P1_DISPOSITION_REGISTER.json and the two D01 remediation "
        "handoffs - and not from the instruction's own list, which the "
        "instruction requires and which turned out to matter: the register "
        "and the cards disagreed with the instruction on three items.")

#: pre-edit digest -> the record that pinned it, so a supersession claim can
#: name its predecessor without a human retyping a hash.
PRIOR_PINS = {
    "QB4_E.html#q12": {
        "manifest": "correction_corr_pre_t4_z7esp_20260905_manifest.json",
        "action_id": "CORR-PRE-T4-Z7ESP-02",
        "post_edit_digest": "68fbdbfda51fe72bbfbe7f0ef8344d7b5ca699d1d12b4f1eec9dc2923e8c8a1b",
    },
    "QB8_A.html#q3": {
        "manifest": "correction_corr_g1_007_qb8a_q3_artefacts_20260824_manifest.json",
        "action_id": "CORR-G1-007-01",
        "post_edit_digest": "8154bb0a82488d0c69714f14715a68e102fd01fef559333fa8d384d0a365858f",
    },
    "QB5_A.html#q4": {
        "manifest": "correction_corr_fair_treatment_20260821_manifest.json",
        "action_id": "CORR-FT-06",
        "post_edit_digest": "45b6e5b4578a603523c7499a9036951f4a0c9a9b44012b3c811dfae7d2081e40",
    },
    "QB10_B.html#q1": {
        "manifest": "correction_corr_g1_010_roro_attribution_20260825_manifest.json",
        "action_id": "CORR-G1-010-02",
        "post_edit_digest": "3ecca484502640a396cc33c947649b27544b98fbc10ee6f99b4938c9ebbfd976",
    },
    "QB3_B.html#q1": {
        "manifest": "correction_corr_d01s02_hssc_reach_20260907_manifest.json",
        "action_id": "D01S02-HSSC-01",
        "post_edit_digest": "d00a9c6b6aca8774e7c1de6ff7d87f3e0b2c448b95381b21885a088bfb3267a4",
    },
}

SUPERSEDES_NOTE = ("The predecessor record stays exactly as published. This "
                   "correction is a later authorised state descending from "
                   "that pin, not a rebaseline.")


def digests(file_name: str) -> dict:
    return canonical_card_digests(read_text(REPO / "meoclass1" / file_name))


def card(file_name, anchor, classification, what_changed, pre):
    key = "%s#%s" % (file_name, anchor)
    entry = {
        "correction_action_id": None,  # filled by caller
        "file": file_name,
        "path": "meoclass1/%s" % file_name,
        "anchor": anchor,
        "classification": classification,
        "pre_edit_digest": pre,
        "post_edit_digest": digests(file_name)[anchor],
        "what_changed": what_changed,
    }
    if key in PRIOR_PINS:
        entry["supersedes"] = dict(PRIOR_PINS[key], note=SUPERSEDES_NOTE)
    return entry


# Pre-edit digests, as they stood at 05b49d8 (before this batch).
PRE = {
    "QB4_E.html#q12": "68fbdbfda51fe72bbfbe7f0ef8344d7b5ca699d1d12b4f1eec9dc2923e8c8a1b",
    "QB4_C.html#q5": "23fc1261548d22a7c4e6350f42503b8251178b1452d838e600e0ae3b628e5e43",
    "QB8_A.html#q3": "8154bb0a82488d0c69714f14715a68e102fd01fef559333fa8d384d0a365858f",
    "QB5_A.html#q4": "45b6e5b4578a603523c7499a9036951f4a0c9a9b44012b3c811dfae7d2081e40",
    "QB3_A.html#q5": "5eb232c07cc9cd054f50aca416f8a69ac26cafd96892ad8bb652cf34d2c2daf9",
    "QB10_B.html#q1": "3ecca484502640a396cc33c947649b27544b98fbc10ee6f99b4938c9ebbfd976",
    "QB3_B.html#q1": "d00a9c6b6aca8774e7c1de6ff7d87f3e0b2c448b95381b21885a088bfb3267a4",
}

COMMON = {
    "kind": "POST_RELEASE_CORRECTION",
    "status": "AUTHORISED",
    "date": DATE,
    "baseline_commit": BASELINE,
    "authorisation_source": AUTH,
    "governing_commits": [CONTENT_COMMIT, REMEDIATION_COMMIT],
}


def build():
    records = []

    # ---------------------------------------------------------------- IACS
    c = card("QB4_E.html", "q12", "PRIMARY_CORRECTION",
             "15-second answer: 'currently consists of 11 full member societies' and the "
             "hedge 'IACS now has 11 or 12 members depending on the inclusion of the newest "
             "member, Turk Loydu' replaced by a flat statement of twelve with the full "
             "abbreviation list and the two membership events dated. 60-second answer: the "
             "member list read 'As of 2026, the members are' and enumerated ELEVEN, omitting "
             "the Korean Register; KR restored and the count stated. Detail list: 'Turk Loydu "
             "(Turkey - admitted recently)' dated to 1 November 2023 and identified as the "
             "twelfth. CE Oral Tip: the model answer told the candidate to say 'bringing the "
             "list to 11 current members'; replaced, and the tip now names KR as the member "
             "candidates drop. Structural: a live authoring scaffold ('Below are Q13-Q15 "
             "drafted in the exact required chat-ready format, using quote blocks and "
             "collapsible sections') and its preceding horizontal rule were removed from the "
             "end of the CE tip - the only two-line scaffold block left in this file.",
             PRE["QB4_E.html#q12"])
    c["correction_action_id"] = "P2-IACS-01"
    records.append(("correction_corr_pass2_iacs_members_20260907_manifest.json", dict(
        COMMON,
        origin="pass2_known_defect_remediation",
        correction_id="CORR-PASS2-IACS-MEMBERS-20260907",
        title="QB4_E q12 - the card whose job is to list the IACS members taught eleven in "
              "three candidate-facing layers, above its own list of twelve, having dropped KR.",
        candidate_claim="Not a candidate report. Carried from PASS1_P1_DISPOSITION_REGISTER "
                        "as REQUIRES_EXTERNAL_VERIFICATION, blocker "
                        "K-ITEM-P1-IACS-MEMBERSHIP.",
        candidate_verdict="UPHELD. The blocker is discharged, and the decisive evidence was "
                          "internal: the card's own detail list already carried all twelve "
                          "including KR, so the card contradicted itself and no external "
                          "source was needed to establish that at least one of its two "
                          "answers was wrong.",
        authority="PRIMARY-INTENDED, DEGRADED TO CORROBORATED - recorded honestly. "
                  "iacs.org.uk returned HTTP 403 to this session on both the membership page "
                  "and the site root, so the issuer's own page could not be read and this "
                  "entry is ACCESS_LIMITED on the primary. The figure of twelve rests on "
                  "three independent legs that agree: (1) the card's own detail list, "
                  "authored earlier and never corrected, enumerating all twelve including KR; "
                  "(2) the Founder-recorded prior verification carried in the Pass-2 "
                  "instruction, which names the same twelve; (3) a public sweep this pass "
                  "returning the same twelve, with Turk Loydu admitted 1 November 2023 as the "
                  "twelfth and RMRS terminated 11 March 2022. Membership: ABS, BV, CCS, CRS, "
                  "DNV, IRClass, KR, LR, ClassNK, PRS, RINA, TL. KR has been a member since "
                  "long before any of the disputed events and is not itself in question - the "
                  "defect was an omission from one list, not a contested admission.",
        propagation={
            "same_defect_swept": "The corpus was searched for '11 members', '11 full member', "
                                 "'eleven members' and 'IACS now has'. QB4_E q12 is the only "
                                 "site. No other card states an IACS membership count.",
            "checked_clean": "The RMRS 'expelled' wording elsewhere in the same card carries "
                             "the correct March 2022 date and no count, and was left alone - "
                             "it is a terminology preference, not a false proposition.",
            "derived_surfaces": "NONE. corpus 761 / 86 unchanged.",
            "hub_date": "NOT ADVANCED.",
        },
        invariants=[
            "The UR Z7 / UR Z10-series distinction corrected on 5 Sep 2026 is untouched and "
            "still reads Z7 = hull classification surveys.",
            "The Role of IACS, IACS vs RO, and UR/UI sections are byte-identical.",
            "The detail list of twelve societies is byte-identical apart from the TL line's "
            "admission date - it was already correct and was NOT rewritten to match the "
            "corrected summary, because it was the summary that was wrong.",
            "No claim is made about which society is 'newest' beyond TL's dated admission.",
        ],
        known_traps_entries=[120],
        cards=[c],
    )))

    # ---------------------------------------------------------------- PR1C
    c = card("QB4_C.html", "q5", "PRIMARY_CORRECTION",
             "15-second: 'Both invalidate statutory certificates and void insurance' replaced "
             "by the B.1.1 written notification to Owner and Flag State and B.1.3's 'certain' "
             "statutory certificates, with the explicit note that PR1C says nothing about "
             "insurance. 60-second: the sentence that blended the triggers ('fails to rectify "
             "a Condition of Class within the specified window or misses a mandatory survey. "
             "The class certificate is paused, automatically rendering all statutory "
             "certificates invalid and voiding insurance cover') split into the A.1.1-A.1.3 "
             "automatic limb and the A.2.1/A.1.4 suspension-procedure limb, with the "
             "disclassed-until-reinstatement rule added. Consequences list: 'Statutory "
             "certificates ... automatically become invalid' replaced by B.1.3 as written. "
             "Insurance bullet: the universal freeze/void claim replaced by the class-warranty "
             "analysis, which also removed the 'H\\&M' markdown-escape artefact. Withdrawal "
             "triggers: A.4.1's six-month rule added, which the card had gestured at as "
             "'beyond the allowed time limits'. Regulatory References: 'IACS UR Z15' replaced "
             "by PR1C Rev.7 with clause map and an explicit note of what UR Z15 actually is. "
             "Numbers & Regs: the same UR Z15 misattribution replaced, and two stray '**' "
             "markdown bold artefacts closed. Trap Questions: the model answer's 'the "
             "statutory certificates are legally invalidated, and insurance cover may be "
             "voided' rewritten to lead with the trigger distinction. Casualty Link: "
             "'automatic invalidation of their statutory certificates' softened to B.1.3. "
             "REMEDIATED AFTER INDEPENDENT REVIEW: the CE Oral Tip was missed by the first "
             "attempt and still read 'Operating under either status invalidates our statutory "
             "certificates', unqualified - in the one layer that is a script for what the "
             "candidate says to the examiner. Corrected, together with the Stop-Work bullet's "
             "bare 'without valid statutory certificates or insurance'; and the A.1 line in "
             "Numbers & Regs now carries A.1.2/A.1.3's three-month window and the "
             "under-attendance exception.",
             PRE["QB4_C.html#q5"])
    c["correction_action_id"] = "P2-PR1C-01"
    records.append(("correction_corr_pass2_pr1c_suspension_20260907_manifest.json", dict(
        COMMON,
        origin="pass2_known_defect_remediation",
        correction_id="CORR-PASS2-PR1C-SUSPENSION-20260907",
        title="QB4_C q5 - the same PR1C defect family D01-S01 corrected on QB1_K q2, plus a "
              "false governing citation: IACS UR Z15 is Mobile Offshore Drilling Unit surveys.",
        candidate_claim="Not a candidate report. Same-defect propagation from "
                        "CORR-D01-COC-PR1C-20260907 (RC-05), which corrected QB1_K q2 on the "
                        "identical proposition. The Pass-2 instruction named this card as a "
                        "known open member of that family.",
        candidate_verdict="UPHELD, and the card was worse than the family description. Beyond "
                          "the blended triggers, the overstated statutory-certificate "
                          "consequence and the universal insurance claim, the instrument "
                          "cited as governing the whole answer was the wrong document.",
        authority="PRIMARY - IACS PR1C Rev.7 (November 2024), 'Procedure for Suspension and "
                  "Reinstatement or Withdrawal of Class in Case of Surveys or Conditions of "
                  "Class Going Overdue', retrieved and read this pass from IACS's own hosting, "
                  "together with Rev.6 for comparison. RETRIEVAL ROUTE, recorded because an "
                  "independent reviewer could not reproduce it and reasonably challenged the "
                  "PRIMARY claim on that basis: iacs.org.uk refuses a default user agent with "
                  "HTTP 403, and returns 200 to a browser user agent. Rev.7 is at "
                  "https://iacs.s3.af-south-1.amazonaws.com/wp-content/uploads/2024/11/"
                  "18161614/PR-1C-Rev.7-Nov-2024-CLN.pdf and Rev.6 at "
                  "https://iacs.s3.af-south-1.amazonaws.com/wp-content/uploads/2023/08/"
                  "10163156/pr1crev6-2.pdf - both on IACS's own S3 bucket, both read in full "
                  "this pass. A.1.1 Special (Renewal) overdue: the "
                  "5-year Class Certificate expires and 'classification is automatically "
                  "suspended'. A.1.2 Annual, A.1.3 Intermediate: same automatic language. "
                  "A.1.4 continuous survey item: 'subject to a suspension procedure'. A.2.1 "
                  "overdue condition of class: 'the vessel's class will be subject to a "
                  "suspension procedure'. A.2.2: the vessel is disclassed from the date of "
                  "suspension until reinstatement. A.4.1: six months suspended for overdue "
                  "surveys and/or conditions of class and the class is to be withdrawn, with a "
                  "longer period available where the vessel is not trading. B.1.1/B.1.2: "
                  "written confirmation to Owner and Flag State. B.1.3: for SOLAS ships the "
                  "letter states that 'certain statutory certificates are implicitly "
                  "invalidated'. A full-text search of BOTH revisions for 'insur', 'warrant' "
                  "and 'P&I' returns ZERO hits, which is the basis for deleting the universal "
                  "insurance claim rather than merely softening it. "
                  "REVISION CURRENCY, and this CLOSES the open point D01-S01 recorded: Rev.7 "
                  "clause 8 states 'Rev.7 of this Procedural Requirement applies from 1 "
                  "January 2026', so Rev.7 governs at today's date; and A.1.1, A.2.1, A.4.1 "
                  "and B.1.3 are textually identical between Rev.6 and Rev.7, so the clause "
                  "lettering D01-S01 asked to be checked is stable and the QB1_K q2 caveat "
                  "can be resolved. "
                  "UR Z15 is 'Hull, Structure, Equipment and Machinery Surveys of Mobile "
                  "Offshore Drilling Units' - verified from the IACS UR text as republished by "
                  "a Member society, table of contents read.",
        propagation={
            "same_defect_swept": "The corpus was searched for 'void insurance', 'voiding "
                                 "insurance', 'insurance is void', 'all statutory "
                                 "certificates', 'automatically become invalid' and 'UR Z15'. "
                                 "Beyond QB4_C q5 the only remaining hits are the already-"
                                 "corrected QB1_K q2, and past-paper examiner wording.",
            "already_correct_sibling": "meoclass1/QB1_F.html section 4 'Class Status Ladder' "
                                       "already teaches the correct distinction, the six-month "
                                       "rule and 'certain statutory certificates', and cites "
                                       "PR1C Rev.7 - it was used as a consistency control, not "
                                       "as proof. Primary text decided every point.",
            "examiner_wording_keep": "Past-paper stems using 'enlist all statutory "
                                     "certificates' are sitting-anchored examiner wording and "
                                     "were not touched.",
            "not_swept_reported": "QB1_F q23 was named by the instruction as a member of this "
                                  "family. It is not. The card is about the Certificate of "
                                  "Approval for a Planned Maintenance Scheme under IACS UR "
                                  "Z20 and contains no PR1C, suspension, withdrawal, "
                                  "statutory-certificate or insurance proposition at all. "
                                  "Classified ALREADY_CORRECT for this family and not "
                                  "touched.",
            "derived_surfaces": "NONE. corpus 761 / 86 unchanged.",
            "hub_date": "NOT ADVANCED.",
        },
        invariants=[
            "The suspension-versus-withdrawal distinction the card exists to teach is "
            "preserved: temporary and reversible against permanent removal from the register.",
            "The Merchant Shipping Act 2025 Part VI Sec 125/127 material corrected on "
            "15 Jul 2026 is unchanged in substance and still replaces 1958 Sec 334.",
            "SOLAS II-1/3-1 and ISM 10.2 reg-box entries unchanged.",
            "Every candidate-facing layer now carries the 'certain' qualifier, including the "
            "CE Oral Tip, which the first attempt missed and which the gate did not read.",
            "No claim that insurance is unaffected - the class warranty analysis is added, "
            "not the opposite overstatement.",
            "No claim that PR1C is a ceiling: it is the harmonised floor, and an individual "
            "society's Rules may go further.",
        ],
        known_traps_entries=[113, 121],
        cards=[c],
    )))

    # ------------------------------------------------------------ ALLIANCE
    c = card("QB8_A.html", "q3", "PRIMARY_CORRECTION",
             "15-second: the consortium examples '(e.g., 2M, Ocean Alliance)' replaced by the "
             "2026 line-up. Section 2: 'such as the Ocean Alliance or THE Alliance' replaced "
             "by the three current groupings with their members, the February 2025 "
             "restructuring explained, and 2M's January 2025 end stated. Key Numbers: the BAF "
             "entry's claim that the surcharge is 'managed by the engineering department's "
             "fuel tracking' replaced by what a BAF actually is and who sets it; the "
             "Regulation 906/2009 entry gains its name (CBER) and its 25 April 2024 expiry. "
             "CE Oral Tip: the model answer's closing claim that engine-room efficiency keeps "
             "costs 'within the baseline projections managed by the commercial BAF framework' "
             "replaced, with an explicit warning not to claim engine-room influence over the "
             "BAF. CE Relevance: 'cannot be recovered retrospectively through the standard BAF "
             "surcharge' replaced by the price-versus-consumption distinction. Casualty Link: "
             "the claim that Ever Given 'led to' the SCFI's historic highs replaced by the "
             "contributory framing with the actual timing of the peak.",
             PRE["QB8_A.html#q3"])
    c["correction_action_id"] = "P2-ALLIANCE-01"
    records.append(("correction_corr_pass2_alliance_currentness_20260907_manifest.json", dict(
        COMMON,
        origin="pass2_known_defect_remediation",
        correction_id="CORR-PASS2-ALLIANCE-CURRENTNESS-20260907",
        title="QB8_A q3 - a commercial-currentness card naming 2M and THE Alliance as current, "
              "eighteen months after both ceased to exist, plus three unsupported BAF claims.",
        candidate_claim="Not a candidate report. Carried from PASS1_P1_DISPOSITION_REGISTER "
                        "as REQUIRES_LATER_SURGICAL_CORRECTION, blocker recorded as 'no "
                        "Pass-1 family covers it; no primary instrument governs it'.",
        candidate_verdict="UPHELD. The Pass-1 blocker was correct that no primary instrument "
                          "governs a commercial roster, which is exactly why the card had "
                          "decayed unnoticed - there is no resolution number for a detector "
                          "to date-check.",
        authority="PUBLIC-VERIFIED, and stated as such rather than dressed as primary. There "
                  "is no issuer of record for an alliance roster. Verified this pass from "
                  "converging public reporting: 2M (Maersk/MSC) ended January 2025 and MSC now "
                  "operates standalone; Gemini Cooperation (Maersk and Hapag-Lloyd) began "
                  "February 2025 on a hub-and-spoke model; the residual THE Alliance members "
                  "ONE, HMM and Yang Ming rebranded as Premier Alliance in February 2025; "
                  "Ocean Alliance (CMA CGM, COSCO, Evergreen, OOCL) is the only pre-2025 "
                  "grouping still intact and runs to 2032. "
                  "PRIMARY for the competition-law limb: Commission Regulation (EC) No "
                  "906/2009, the Consortia Block Exemption Regulation. The Commission decided "
                  "in October 2023 not to renew it and it EXPIRED on 25 April 2024; EU-trade "
                  "consortia now self-assess under Article 101 with no dedicated exemption. "
                  "The EU's 2008 abolition of the liner-conference exemption, already in the "
                  "card, is unchanged and correct. "
                  "The BAF corrections are removals of unsupported claims rather than "
                  "assertions of new ones: there is no IMO or industry-standard BAF formula, "
                  "and the card's claim that the engine department manages the surcharge had "
                  "no source and is not how the instrument works.",
        propagation={
            "same_defect_swept": "The corpus was searched for '2M', 'THE Alliance', 'Ocean "
                                 "Three', 'Gemini' and 'Premier Alliance'. QB8_A q3 is the "
                                 "only card naming a container alliance as current.",
            "checked_clean": "The Baltic Dry Index composition limb added on 24 Aug 2026 "
                             "(Capesize 40 / Panamax 30 / Supramax 30 since 1 March 2018, "
                             "Handysize reported separately as BHSI) is untouched and remains "
                             "consistent with known_traps 48.",
            "not_corrected_reported": "The reg-box entries 'ISM Code Section 7' and 'ISO 50001 "
                                      "Standards' are weak fits for a freight-rate question - "
                                      "neither is false, both are filler. Left in place: "
                                      "section 4 of the instruction forbids low-value work "
                                      "delaying P1 corrections, and removing a true-but-"
                                      "irrelevant reference is a style decision, not a defect "
                                      "closure. Reported for a later editorial pass.",
            "derived_surfaces": "NONE. corpus 761 / 86 unchanged.",
            "hub_date": "NOT ADVANCED.",
        },
        invariants=[
            "The conference-versus-consortium distinction the question actually asks about is "
            "preserved and strengthened, not diluted by the roster update.",
            "The 2008 EU abolition of the liner conference block exemption is unchanged.",
            "The freight-rate SOURCES limb added 24 Aug 2026 - Baltic Exchange indices, "
            "container indices, Worldscale, brokers, own fixtures - is byte-identical.",
            "The BDI weighting and the 1 March 2018 Handysize removal are byte-identical.",
            "Ever Given remains in the card as a real casualty with its real date; only the "
            "causal overstatement about the SCFI record was removed.",
        ],
        known_traps_entries=[48, 124],
        cards=[c],
    )))

    # --------------------------------------------------------------- HUMAN
    c = card("QB5_A.html", "q4", "PRIMARY_CORRECTION",
             "Numbers to Memorise: the block had lost the only two numbers it exists to "
             "teach. The markup read '<li>- Maslow theory published</li>' and '<li>levels "
             "(pyramid sequence - bottom to top)</li>' across two separate <ul> elements, with "
             "the 1943 and the 5 absent from the source, not merely mis-rendered. Both "
             "restored and the two lists merged into one, with the level sequence spelled out. "
             "Five Levels table: the Esteem row's Regulatory Hook 'MLC Reg. 1.4 (Recruitment / "
             "Fair Treatment)' replaced - Reg. 1.4 is Recruitment and placement, and the row "
             "now says plainly that this level has no MLC hook. Trap Questions: 'Maslow's "
             "model is strictly upward progression' replaced by the accurate contrast, which "
             "puts the regression claim where it belongs (Alderfer) without misattributing "
             "rigidity to Maslow. On My Vessel: the fabricated first-person anecdote - a "
             "10-day tropical port stay, 24 hours off-duty every third day, motivation "
             "recovering within 48 hours, 'entirely consistent with Maslow's Level 1->3 "
             "restoration effect' - replaced by guidance to answer from the candidate's own "
             "ship, with an explicit instruction not to invent figures and a statement that "
             "no such restoration effect exists.",
             PRE["QB5_A.html#q4"])
    c["correction_action_id"] = "P2-HUMAN-01"
    records.append(("correction_corr_pass2_human_element_20260907_manifest.json", dict(
        COMMON,
        origin="pass2_known_defect_remediation",
        correction_id="CORR-PASS2-HUMAN-ELEMENT-20260907",
        title="QB5_A q4 - the Maslow card had lost both of its numbers from the HTML, "
              "misattributed fair treatment to MLC Reg. 1.4, and rested on a fabricated "
              "anecdote citing an invented psychological effect.",
        candidate_claim="Not a candidate report. Carried from PASS1_P1_DISPOSITION_REGISTER "
                        "as REQUIRES_LATER_SURGICAL_CORRECTION.",
        candidate_verdict="UPHELD, with one item the Pass-1 note had not identified: the "
                          "Numbers to Memorise block was not merely thin, it was empty of "
                          "numbers. A card that tells the candidate 'Forgetting Maslow's year "
                          "(1943) - examiners often ask' four lines above a memorisation list "
                          "that does not contain 1943 is a content-loss defect, not a style "
                          "one.",
        authority="MIXED, and separated deliberately. "
                  "PRIMARY for the legal limb: MLC 2006 Regulation 1.4 is 'Recruitment and "
                  "placement'; Regulation 3.1 is 'Accommodation and recreational facilities'; "
                  "3.2 food and catering; 2.3 hours of work and rest; 4.1 medical care; 4.4 "
                  "access to shore-based welfare. The card's other MLC citations were checked "
                  "against this and are correct - only the Reg. 1.4 fair-treatment gloss was "
                  "wrong, and it is the third instance of a fair-treatment proposition being "
                  "pinned to an MLC regulation that does not carry it (see traps 38 and 41). "
                  "The Standard A2.3 rest figures the card quotes - 10 hours in 24, 77 in "
                  "seven days - are correct and were not touched. "
                  "SECONDARY for the theory limb, which is appropriate because the subject is "
                  "management theory and not an instrument: Maslow's 1943 paper 'A Theory of "
                  "Human Motivation' sets out the five-level model and expressly qualifies the "
                  "hierarchy as non-rigid, with partial satisfaction and possible reversal of "
                  "order; the pyramid diagram is a later teaching device. Alderfer's 1969 ERG "
                  "formulation introduces frustration-regression explicitly. "
                  "NO AUTHORITY, and therefore removed rather than rewritten: the 'Maslow "
                  "Level 1->3 restoration effect' does not exist in the literature. It was not "
                  "a mis-citation of a real effect; it was a name invented to lend a "
                  "fabricated anecdote's 48-hour recovery figure the appearance of theoretical "
                  "support.",
        propagation={
            "same_defect_swept": "The corpus was searched for 'MLC Reg. 1.4', 'MLC 1.4' and "
                                 "'Regulation 1.4'. QB5_A q4 is the only site pairing Reg. 1.4 "
                                 "with fair treatment; the other hits describe recruitment and "
                                 "placement correctly. The 'restoration effect' string appears "
                                 "nowhere else.",
            "same_family_prior": "The fabricated first-person anecdote is the family closed by "
                                 "CORR-GPT-T2C-ONMYVESSEL-20260905 on QB5_C_B q5 and QB2_A "
                                 "q27. This is a further site of that family, found by the "
                                 "Pass-1 disposition rather than by a new sweep.",
            "not_swept_reported": "QB5_A.html and QB5_B.html carry 31 instances of a duplicated "
                                  "'<h5>On My Vessel (Maersk A/S)</h5><p>(Maersk A/S):</p>' "
                                  "label stutter. It is cosmetic, loses no content, and is NOT "
                                  "one of the residue classes section 12 of the instruction "
                                  "enumerates. Reported as a new P3 class, not swept - section "
                                  "15 requires a new class to be reported rather than expanded.",
            "derived_surfaces": "NONE. corpus 761 / 86 unchanged.",
            "hub_date": "NOT ADVANCED.",
        },
        invariants=[
            "The five levels, their order, and their maritime application are unchanged - the "
            "teaching the card exists for is preserved in full.",
            "The MLC 3.2 / 2.3 / 4.1 / 3.1 / 4.4 citations, all correct, are byte-identical.",
            "The Standard A2.3 figures 10 hrs / 24 and 77 hrs / 7 days are byte-identical.",
            "Alderfer's ERG mapping to Maslow's levels is unchanged; only the sentence about "
            "Maslow's own rigidity was corrected.",
            "The MV Sewol casualty link, its date and its death toll are byte-identical.",
            "The CE-level management teaching - diagnose the lowest unmet level first, never "
            "reach for a Level 4 intervention over a Level 1 problem - is preserved, which is "
            "the part of this card that is actually worth marks.",
        ],
        known_traps_entries=[38, 41, 125],
        cards=[c],
    )))

    # ------------------------------------------------------------- CLOSEUP
    c = card("QB3_A.html", "q5", "PRIMARY_CORRECTION",
             "The 'Annual Survey Close-Up Extension (bulk carriers/oil tankers)' bullet "
             "rewritten. Two defects in one sentence: the requirement was scoped to bulk "
             "carriers and oil tankers generally when it belongs to single side skin bulk "
             "carriers under IACS UR Z10.2, and the whole claim was cited to a marinegyaan.com "
             "blog post via an anchor rendered to the candidate as '[reference]' - the only "
             "such placeholder anywhere in the corpus. The blog link is removed and the scope "
             "corrected, with the sibling requirements named so a candidate can place a double "
             "side skin bulker (Z10.5) and an oil tanker (Z10.1/Z10.4). "
             "REMEDIATED AFTER INDEPENDENT REVIEW: the first attempt at this correction "
             "removed the '25% of cargo hold side shell frames, forward hold + one other "
             "selected hold' figure as blog-sourced, dropped the 'can require' modality, "
             "and dropped the age condition - leaving an UNCONDITIONAL rule. That was wrong "
             "on the facts: D01-S02 DOES assert the 25% and the hold scope on QB3_B q1 and "
             "attributes them to UR Z10.2, and it expressly records that the requirement is "
             "age-conditioned with the band unverified. The bullet is now restated in QB3_B "
             "q1's own wording - extent, hold scope, 'can require' modality, age condition "
             "and source gap included - and cross-referenced to it.",
             PRE["QB3_A.html#q5"])
    c["correction_action_id"] = "P2-CLOSEUP-01"
    sibling = card("QB3_B.html", "q1", "PROPAGATED_FACT_CORRECTION",
                   "Numbers to Memorise still read '25% - annual close-up survey extent of "
                   "cargo hold side shell frames (bulk carriers/tankers), forward hold + one "
                   "other selected hold'. That is the exact over-broad scope this card's own "
                   "body and reg-box refute, both of which D01-S02 corrected to single side "
                   "skin bulk carriers under UR Z10.2. The memorisation layer was left behind "
                   "by that pass and contradicted the card it sits in. Corrected, with the age "
                   "condition added to the line.",
                   PRE["QB3_B.html#q1"])
    sibling["correction_action_id"] = "P2-CLOSEUP-02"

    records.append(("correction_corr_pass2_closeup_scope_20260907_manifest.json", dict(
        COMMON,
        origin="pass2_known_defect_remediation",
        correction_id="CORR-PASS2-CLOSEUP-SCOPE-20260907",
        title="QB3_A q5 - the annual close-up proposition D01-S02 corrected on QB3_B q1, "
              "propagated here and still resting on the corpus's only blog citation.",
        candidate_claim="Not a candidate report. The instruction listed 'QB3_A#q5 weak/blog "
                        "citation if still open'. It was open, and reading the card showed the "
                        "citation was not the only problem: the proposition it supported is "
                        "the one D01-S02 had already adjudicated elsewhere.",
        candidate_verdict="UPHELD on both limbs. The instruction anticipated a citation-quality "
                          "defect; the actual finding is a citation-quality defect carrying a "
                          "scope defect, which is why replacing the link with a better one "
                          "would not have been a fix.",
        authority="HELD IN-REPOSITORY, and its provenance stated rather than re-derived. The "
                  "governing adjudication is CORR-D01S02-HSSC-REACH-20260907 on QB3_B q1, "
                  "whose recorded source basis is the IACS UR index read that pass: UR Z10.2 "
                  "governs single side skin bulk carriers, Z10.5 double side skin, and "
                  "Z10.1/Z10.4 oil tankers, with cargo hold side shell frames being a "
                  "single-side-skin feature. That record was independently revalidated by Lane "
                  "B. This correction propagates a settled adjudication to a sibling site; it "
                  "does not open a new one, and it deliberately asserts nothing that record "
                  "did not - in particular no percentage and no hold count.",
        propagation={
            "same_defect_swept": "The corpus was searched for 'side shell frames', 'close-up' "
                                 "with 'annual', and 'single side skin'. The corrected QB3_B "
                                 "q1 and this card are the only two sites that stated the "
                                 "scope; QB3_A q5 was the one D01-S02's sweep did not reach, "
                                 "because that sweep was scoped to the HSSC token family and "
                                 "this card never contained the token.",
            "sibling_memorisation_layer": "QB3_B#q1's Numbers block is corrected here as "
                                          "P2-CLOSEUP-02 - a seventh declared card. Bounded "
                                          "same-defect propagation, not new discovery: D01-S02 "
                                          "had already adjudicated the proposition, and one "
                                          "layer of that card never received it.",
            "citation_class_swept": "'[reference]' as rendered anchor text: one occurrence "
                                    "corpus-wide, now zero. marinegyaan.com as a cited source: "
                                    "this was the only candidate-facing link to it.",
            "derived_surfaces": "NONE. corpus 761 / 86 unchanged.",
            "hub_date": "NOT ADVANCED.",
        },
        invariants=[
            "The drydock-planning teaching the question actually asks about - two bottom "
            "inspections in five years, maximum 36 months, the IWS substitution limits, the "
            "6-12 month planning timeline - is byte-identical.",
            "The coinciding-surveys list is otherwise unchanged.",
            "Extent, hold scope, modality and age condition now match QB3_B#q1 exactly - "
            "this record asserts nothing that record does not, which is a claim the first "
            "attempt made and did not honour.",
            "No age BAND is asserted, because none is verified - the source gap is carried "
            "forward visibly rather than resolved by guessing.",
            "The card's HSSC framing is left as it stands: this is the statutory bottom-"
            "inspection regime, where HSSC is the correct regime, and is not the class-cycle "
            "misattribution trap 112 covers.",
        ],
        known_traps_entries=[112, 116, 127],
        cards=[c, sibling],
    )))

    # --------------------------------------------------------------- AMEND
    c = card("QB10_B.html", "q1", "PRIMARY_CORRECTION",
             "Formula block: 'Lifeboat lowering speed (post-2026): min 1.0 m/s, max 1.3 m/s - "
             "replaces the old S = 0.4 + 0.02H formula' replaced by the amended LSA Code text "
             "with its resolution, its applicability, and an explicit statement that the "
             "formula is not abolished. Numbers to Memorise: the same '1.0-1.3 m/s ... "
             "(replacing the old H-dependent formula)' entry replaced on the same basis. "
             "1 January 2024 tranche: the free-fall row's 'SOLAS III/33 removed the 5-knot "
             "headway test-launch requirement for ships >=20,000 GT' replaced by the actual "
             "amended text of III/33.2, its resolution, and the narrowed-not-abolished framing; "
             "the invented rationale ('studies showed the test added no meaningful data on "
             "dynamic loads at that speed') removed. 1 January 2028 tranche: a raw '<' in "
             "'(e.g. <150 GT, fishing vessels)' was escaped to '&lt;' as correct markup "
             "hygiene. WITHDRAWN AFTER INDEPENDENT REVIEW: the first version of this record "
             "claimed that raw '<' was deleting about 150 characters of rendered teaching, "
             "including two entry-into-force dates. That was FALSE. HTML5 emits '<' as a "
             "literal character unless the next character is an ASCII letter, so '<150 GT' "
             "always rendered correctly - verified by serving the pre-fix string to a real "
             "browser and reading the rendered text back, which returned the passage complete "
             "with both dates. The claim reached a candidate-facing version stamp before it "
             "was tested. It is withdrawn from the card, from this record, and from "
             "known_traps 126, which now records the actual lesson. "
             "Regulatory References: the 'MSC.559(108) / MSC.560(108) - Lifeboat ventilation "
             "testing regime' entry rebuilt to separate four instruments candidates conflate, "
             "and a new MSC.482(103) entry added for the 2024 tranche, which had no reference "
             "at all. Trap Warning: the self-dating 'it is now mid-2026' replaced by the "
             "instrument date.",
             PRE["QB10_B.html#q1"])
    c["correction_action_id"] = "P2-AMEND-01"
    records.append(("correction_corr_pass2_amendment_overview_20260907_manifest.json", dict(
        COMMON,
        origin="pass2_known_defect_remediation",
        correction_id="CORR-PASS2-AMENDMENT-OVERVIEW-20260907",
        title="QB10_B q1 - K-ITEM-P1-LSA-LOWERING-SPEED closed against MSC.554(108), which "
              "does not replace the formula; and the free-fall row, suspected of being "
              "fabricated, turns out to be real but inverted.",
        candidate_claim="Not a candidate report. Carried from PASS1_P1_DISPOSITION_REGISTER "
                        "as REQUIRES_SOURCE_ACQUISITION, blocker "
                        "K-ITEM-P1-LSA-LOWERING-SPEED, which recorded that a REPLACEMENT claim "
                        "cannot be adjudicated from the number alone and that guessing a "
                        "figure would repeat the defect class Pass 1 existed to close. That "
                        "reasoning was right, and the acquisition it asked for is what closed "
                        "the item.",
        candidate_verdict="UPHELD on the lowering speed. PARTLY_CORRECT, and corrected in the "
                          "opposite direction, on the free-fall row: the Pass-2 instruction "
                          "characterised it as a 'false free-fall / 5-knot / 20,000-GT "
                          "proposition'. It is not false. MSC.482(103) really did change "
                          "SOLAS III/33.2 with effect from 1 January 2024, and the card was "
                          "right about the date. What it got wrong was the direction - the "
                          "requirement was narrowed to davit-launched lifeboats, not removed - "
                          "and the population, which is cargo ships rather than ships. Deleting "
                          "the row as fabricated, which is what the instruction's framing "
                          "invited, would have removed a true amendment from a currency card.",
        authority="PRIMARY - three IMO resolutions retrieved from the IMO document server and "
                  "read in full this pass. "
                  "MSC.554(108), 'Amendments to the International Life-Saving Appliance (LSA) "
                  "Code', adopted 23 May 2024, in force 1 January 2026, applying to life-saving "
                  "appliances installed on or after that date. Paragraph 6.1.2.8 is replaced: "
                  "'The speed at which the fully loaded survival craft or rescue boat is "
                  "lowered to the water shall not be less than that obtained from the formula: "
                  "S = 0.4 + 0.02H, or 1.0, whichever is less', with S the lowering speed in "
                  "m/s and H the height from davit head to the waterline at the lightest "
                  "sea-going condition. Paragraph 6.1.2.10 is replaced: 'The maximum lowering "
                  "speed of a fully loaded survival craft or rescue boat shall be 1.3 m/s. The "
                  "Administration may accept a maximum lowering speed other than 1.3 m/s, "
                  "having regard to the design of the survival craft or rescue boat, the "
                  "protection of its occupants from excessive forces, and the strength of the "
                  "launching arrangements taking into account inertia forces during an "
                  "emergency stop.' The formula therefore survives; 1.0 m/s caps the "
                  "formula-derived minimum. "
                  "MSC.482(103), adopted 13 May 2021, in force 1 January 2024. Paragraph 33.2 "
                  "is replaced by: 'On cargo ships of 20,000 gross tonnage and upwards, "
                  "davit-launched lifeboats shall be capable of being launched, utilizing "
                  "painters where necessary, with the ship making headway at speeds up to 5 "
                  "knots in calm water.' The same resolution adds SOLAS II-1/25-1, the water "
                  "level detectors the card already lists in the same tranche. "
                  "MSC.559(108), adopted 23 May 2024, in force 1 January 2026: 'Amendments to "
                  "the Requirements for maintenance, thorough examination, operational testing, "
                  "overhaul and repair of lifeboats and rescue boats, launching appliances and "
                  "release gear (resolution MSC.402(96))', made - in its own recitals - 'taking "
                  "into account the amendments to the LSA Code adopted by resolution "
                  "MSC.535(107), with respect to ventilation means' and 'recognizing the need "
                  "to keep the Requirements up to date with regard to annual thorough "
                  "examination and operational testing of ventilation systems'. So MSC.559(108) "
                  "is the TESTING regime and MSC.535(107) is the ventilation requirement it "
                  "serves; the card had the former standing for both, and MSC.535(107) - which "
                  "known_traps 42 governs - appeared nowhere on the card.",
        propagation={
            "same_defect_swept": "The corpus was searched for '0.4 + 0.02', '1.3 m/s', "
                                 "'lowering speed', 'free-fall' with '5 knot', and 'III/33'. "
                                 "QB10_B q1 is the only site making the replacement claim or "
                                 "the removal claim.",
            "checked_clean": "known_traps 46 records that the rescue boat's 5-knot figure "
                             "belongs to launching rather than recovery. That is a different "
                             "5-knot provision from SOLAS III/33.2 and is not disturbed here.",
            "not_corrected_quarantined": "NOTHING is left quarantined in this card: the "
                                         "instruction permitted a partial correction with the "
                                         "uncertain claims fenced off, and that fallback was "
                                         "not needed for the propositions this record touches, "
                                         "because every one of them was settled from primary "
                                         "text. Propositions NOT touched are listed below and "
                                         "are unverified rather than quarantined - they carry "
                                         "no correction and no assurance.",
            "not_verified_reported": "The following load-bearing propositions in this card were "
                                     "NOT verified this pass and are declared open: the "
                                     "MSC.595(111) MASS Code adoption and its 1 Jul 2026 "
                                     "voluntary status; the STCW-F entry, which says the "
                                     "Convention 'entered force 1 Jan 2026' where the 1995 "
                                     "Convention has been in force since 2012 and it is the "
                                     "amendments that are likely meant; the Polar Code "
                                     "non-SOLAS extension and its 1 Jan 2027 retroactivity; "
                                     "MEPC.392(82); the LRIT approved-in-principle status; the "
                                     "MSC 112 expectations, which are future events; and the "
                                     "Bulk Jupiter causal attribution for the inclinometer "
                                     "requirement, which also names the ship as 'Jupiter'. "
                                     "This card needs a dedicated proposition-by-proposition "
                                     "pass; six families is what this batch could verify to "
                                     "primary standard.",
            "derived_surfaces": "NONE. corpus 761 / 86 unchanged.",
            "hub_date": "NOT ADVANCED.",
        },
        invariants=[
            "The 1 Jan 2026 tranche content corrected by CORR-G1-010 - the ro-ro package "
            "attributed to MSC.550(108) rather than MSC.532(107) - is byte-identical.",
            "The MSC.520(106) versus MSC.521(106) discrimination the card teaches is unchanged.",
            "The four-year SOLAS cycle framing, and the warning not to conflate it with MARPOL "
            "Annex VI's own timeline, are unchanged.",
            "No entry-into-force date is altered anywhere in the card, and none was ever "
            "missing from it - see the withdrawn claim above.",
            "The MSC.552(108) grain reg-box entry, which a prior record pins, is byte-identical "
            "- the new MSC.482(103) entry was anchored on the MSC.559 item being replaced "
            "rather than by inserting before MSC.552, precisely so that pin could not move.",
        ],
        known_traps_entries=[42, 46, 122, 123, 126],
        cards=[c],
    )))

    return records


def main() -> int:
    out = []
    for name, record in build():
        path = HERE / name
        path.write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n",
                        encoding="utf-8", newline="\n")
        out.append(name)
    print("Wrote %d correction manifests:" % len(out))
    for n in out:
        print("  tools/oral/%s" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
