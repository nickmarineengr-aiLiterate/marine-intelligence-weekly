#!/usr/bin/env python3
"""
Content validator for the GPT high-risk review tranche 1 corrections:

    CORR-GPT-T1-GRAIN-20260904   QB2_A#q11, QB2_A#q33
    CORR-GPT-T1-LIION-20260904   QB2_A#q7
    CORR-GPT-T1-EIAPP-20260904   QB5_J#q2
    CORR-GPT-T1-QB5CB-20260904   QB5_C_B#q5  + QB5_B_CheatSheet (artefact)

WHY A CONTENT GATE, WHEN validate_corrections.py ALREADY PASSES
---------------------------------------------------------------
`validate_corrections.py` answers "are these the bytes we authorised?".
SKILL.md 8.2a is explicit that this is a different question from "is what we
authorised actually right?" -- a pin is perfectly happy with wrong text.

Four of this tranche's propositions are exactly the shape that gap exists for,
and each is a defect no digest could ever see:

    "the area up to 40 degrees"     for  a criterion with THREE least-of limits
    "matching the rolling amplitude" for  a PRESCRIBED assumed shifted surface
    "CO2 will not extinguish"        for  a limit on ONE of two mechanisms
    "will result in immediate ..."   for  a conditional legal consequence

None of those is a wrong noun. Each is a claim of the wrong SHAPE, and a fact
check passes all four. So the substance is asserted here as named checks, one
per proposition a future well-meaning edit could quietly lose, and each is named
so `mutate_correction_gptt1.py` can require its mutation to trip THAT check
rather than the digest pin, which fires on any edit at all.

THREE CHECKS HERE GUARD SOMETHING OTHER THAN THE PRODUCT
--------------------------------------------------------
*   `msc1615_evidence_tier_recorded`. The Li-ion record says in terms that the
    circular is NOT HELD, that IMO's own CDN path 404'd, and that its title was
    confirmed against two independent SECONDARY sources. That honesty is the
    only thing standing between this corpus and a future reader who believes
    the instrument was read. Mutation T deletes it; nothing else would notice.

*   `msc1615_deviation_recorded`. The review's stated preference was that
    retaining MSC.1/Circ.1615 at all was "probably unnecessary". It was
    retained, as an explicitly scoped caution. A deviation from an
    authorisation has to be VISIBLE in the record, not inferable from the
    product, or the next reviewer cannot tell a decision from a drift.

*   `qb5cb_wider_defects_reported_not_fixed`. Seven other cards in QB5_C_B
    carry the same empty 15-second block, and the q5 reg-box still carries STCW
    Table A-III/2. Both were found while fixing something else and both were
    deliberately left. If that record disappears, the next pass reads a clean
    file and a clean reg-box.

NEGATIVE CHECKS RUN ON UNESCAPED TEXT
-------------------------------------
A guard spelled `h&m` is blind to `h&amp;m`. Every banned-phrase search below
runs against `html.unescape()` of the page, never the raw markup.

AND THEY ARE SCOPED TO THE REJECTED PROPOSITION, NOT TO A KEYWORD
-----------------------------------------------------------------
`QB2_A#q11`'s Common CE Failures block now TEACHES against the old wording, so
it legitimately contains the words "rolling amplitude" and "the area up to 40".
A keyword ban would fire on the sentence carrying the fix -- the same trap
CORR-GPT-PASS1's header records. The patterns below therefore match the
ASSERTION ("shifts to an angle matching the rolling amplitude"), not the topic,
and the `unquoted()` helper additionally exempts a directly quoted mention.
"""

from __future__ import annotations

import html as htmllib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_bytes import read_text                       # noqa: E402
from validate_batch_b import card_digests              # noqa: E402
from oral_supersession import (                        # noqa: E402
    resolve_authorised_card_state)

RECORDS = {
    "grain": HERE / "correction_corr_gpt_t1_grain_20260904_manifest.json",
    "liion": HERE / "correction_corr_gpt_t1_liion_20260904_manifest.json",
    "eiapp": HERE / "correction_corr_gpt_t1_eiapp_20260904_manifest.json",
    "qb5cb": HERE / "correction_corr_gpt_t1_qb5cb_20260904_manifest.json",
}

TARGETS = [
    ("grain", "QB2_A.html", "q11", "meoclass1/QB2_A.html"),
    ("grain", "QB2_A.html", "q33", "meoclass1/QB2_A.html"),
    ("liion", "QB2_A.html", "q7", "meoclass1/QB2_A.html"),
    ("eiapp", "QB5_J.html", "q2", "meoclass1/QB5_J.html"),
    ("qb5cb", "QB5_C_B.html", "q5", "meoclass1/QB5_C_B.html"),
]

CHEATSHEET = REPO / "meoclass1/QB5_B_CheatSheet.html"

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-48s %s" % ("PASS" if ok else "FAIL", check, detail))


def card_html(page: str, anchor: str) -> str:
    """The one card's raw markup, by balanced-div scan."""
    start = page.find('id="%s"' % anchor)
    assert start >= 0, "anchor not found: %s" % anchor
    start = page.rfind('<div class="q-card"', 0, start)
    assert start >= 0, "card not found: %s" % anchor
    depth, pos = 0, start
    pat = re.compile(r"<div\b|</div>")
    while True:
        m = pat.search(page, pos)
        if not m:
            break
        depth += -1 if m.group(0) == "</div>" else 1
        pos = m.end()
        if depth == 0:
            break
    return page[start:pos]


def flatten(markup: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", markup)))


_QUOTES = "\"“”‘’'"


def unquoted(text: str, pattern: str) -> list[str]:
    """Every mention of `pattern` the text ASSERTS rather than directly quotes.

    Exempt only when a quotation mark sits immediately either side. A negation
    window was tried in the Pass-1 gate and its own mutation J walked through
    it: a negator scan cannot tell what a negator is negating.
    """
    bad = []
    for m in re.finditer(pattern, text, re.I):
        before = text[max(0, m.start() - 2):m.start()]
        after = text[m.end():m.end() + 3]
        if any(q in before for q in _QUOTES) and any(q in after for q in _QUOTES):
            continue
        bad.append(text[max(0, m.start() - 56):m.start()].strip() + " >>" + m.group(0))
    return bad


def block(markup: str, needle: str, span: int = 2600) -> str:
    """Flattened text of the region that starts at `needle`.

    Used where a proposition must live in a NAMED layer -- the 60-second
    answer, the CE tip -- and not merely somewhere in the card. Pass 1's
    `iso19030_scope_is_hull_and_propeller` passed on a global count while the
    reg-box it was meant to guard had been gutted; a count is a proxy for a
    proposition, never the proposition.
    """
    i = markup.find(needle)
    return flatten(markup[i:i + span]) if i >= 0 else ""


def main() -> int:  # noqa: C901
    print("correction content validator: GPT high-risk review tranche 1")

    # ================= the records =====================================
    records = {}
    for key, path in RECORDS.items():
        if not path.is_file():
            report("correction_record_present_%s" % key, False, "missing %s" % path.name)
            print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
            return 1
        records[key] = json.loads(read_text(path))
    report("correction_records_present", True, "%d records" % len(records))

    report("correction_records_authorised",
           all(r.get("status") == "AUTHORISED" for r in records.values())
           and all(r.get("origin") == "gpt_content_review" for r in records.values()),
           "all four AUTHORISED, origin gpt_content_review")

    want_auth = ("meoclass1/oral-intelligence/examiner-audit/"
                 "GPT_REVIEW_HIGHRISK_TRANCHE1_20260904.md")
    report("authorisation_source_shared_and_present",
           all(r.get("authorisation_source") == want_auth for r in records.values())
           and (REPO / want_auth).is_file(),
           "one authorisation record for the tranche")

    declared = {}
    for key, rec in records.items():
        for c in rec.get("cards", []):
            declared[(c.get("file"), c.get("anchor"))] = (key, c)
    report("all_five_cards_declared",
           all((f, a) in declared for _, f, a, _ in TARGETS),
           "declared=%d" % len(declared))

    # ---- supersession ancestry ---------------------------------------
    want_pred = {
        ("QB2_A.html", "q11"): ("correction_corr_grain_terminology_20260902_manifest.json",
                                "CORR-GRAINT-01"),
        ("QB2_A.html", "q33"): ("correction_corr_grain_terminology_20260902_manifest.json",
                                "CORR-GRAINT-02"),
        ("QB2_A.html", "q7"): ("batch_e3_enrichment_manifest.json", "ENRICH-A026"),
        ("QB5_J.html", "q2"): ("correction_corr_gpt_pass1_20260904_manifest.json",
                               "CORR-GPT-P1-01"),
        ("QB5_C_B.html", "q5"): ("correction_corr_cicterm_20260904_manifest.json",
                                 "CORR-CICTERM-01"),
    }
    bad_chain = []
    for tgt, (mani, act) in want_pred.items():
        card = declared.get(tgt, (None, {}))[1]
        sup = card.get("supersedes") or {}
        if sup.get("manifest") != mani or sup.get("action_id") != act:
            bad_chain.append("%s#%s wrong-predecessor" % tgt)
        elif not (card.get("pre_edit_digest") or "").startswith(
                sup.get("post_edit_digest") or "\0"):
            # E3 pinned 16 hex characters, this record pins 64. The claim must
            # be recorded in the PREDECESSOR's convention (oral_supersession
            # compares literally) and must still agree on the shared prefix.
            bad_chain.append("%s#%s chain-break" % tgt)
    report("supersession_ancestry_declared", not bad_chain,
           "bad=%s" % (bad_chain or "none"))

    # ---- live digests -------------------------------------------------
    pages = {}
    for _, fname, anchor, rel in TARGETS:
        if fname not in pages:
            pages[fname] = read_text(REPO / rel)
        live = card_digests(pages[fname])[anchor]
        key, entry = declared[(fname, anchor)]
        # Resolved through the chain for the reason recorded in the Pass-1
        # gate: a raw equality expires the first time a later authorised
        # record touches the card, and this tranche is itself the proof --
        # it superseded a pin written the previous day.
        res = resolve_authorised_card_state(
            manifest=RECORDS[key].name,
            action_id=entry["correction_action_id"],
            file=fname, anchor=anchor,
            pinned_post_digest=entry.get("post_edit_digest"),
            live_digest=live, directory=RECORDS[key].parent)
        report("digest_matches_manifest_%s_%s" % (fname.split(".")[0].lower(), anchor),
               bool(getattr(res, "ok", False)),
               "%s live=%s" % (getattr(res, "status", res), live[:16]))

    g11 = card_html(pages["QB2_A.html"], "q11")
    g33 = card_html(pages["QB2_A.html"], "q33")
    l7 = card_html(pages["QB2_A.html"], "q7")
    j2 = card_html(pages["QB5_J.html"], "q2")
    c5 = card_html(pages["QB5_C_B.html"], "q5")
    t11, t33, t7, t2, t5 = (flatten(x) for x in (g11, g33, l7, j2, c5))

    # ============ FAMILY A: the three-limb residual-area criterion ======
    # A 7.1.2 joins its three limits with "whichever is the least". The card
    # kept only the second, which is not a smaller claim - it is a different
    # and larger area, because the maximum-difference angle usually governs.
    # SCOPED TO THE BLOCK THAT CARRIES THE CLAIM, NOT TO THE CARD. Mutations
    # B, C, D, E, I and M each gutted one block and ESCAPED a card-wide check,
    # because the same words survived in a sibling block. A card-wide `in` is a
    # proxy for a proposition, never the proposition -- the same defect Pass 1
    # recorded against its own `iso19030_scope_is_hull_and_propeller`.
    body11 = block(g11, "Net Residual Area on GZ Curve", 1400)
    report("grain_residual_area_three_limits_q11",
           "least of three angles" in body11
           and "maximum difference between the ordinates" in body11
           and "40" in body11 and "flooding" in body11 and "0.075" in body11,
           "the BODY criterion enumerates all three limits")

    body33 = block(g33, "The three intact-stability criteria are untouched", 900)
    report("grain_residual_area_three_limits_q33",
           "least of" in body33 and "maximum-difference" in body33
           and "40" in body33 and "flooding" in body33 and "0.075" in body33,
           "q33's BODY statement enumerates all three limits")

    nums33 = block(g33, "MSC.552(108)</strong> &middot; adopted", 1600)
    report("grain_q33_numbers_block_carries_least_of",
           "least" in nums33 and "maximum-difference" in nums33
           and "flooding" in nums33,
           "q33's Numbers block does not revert to the short form")

    # The fix must not live only in a deep dive. These are the layers a
    # candidate actually recites from.
    report("grain_60s_answer_carries_the_criterion",
           "least of" in block(g11, 'practice-60')
           and "0.075" in block(g11, 'practice-60'),
           "the 60-second layer states the criterion in full")

    report("grain_memory_layers_carry_the_criterion",
           "least of" in block(g11, "Key Numbers", 3000)
           and "least" in block(g11, "Numbers to Memorise", 2200)
           and "least" in block(g11, "Common CE Failures", 2200),
           "Key Numbers + Numbers to Memorise + Common CE Failures")

    report("grain_criterion_named_by_clause",
           "A 7.1.2" in body11 and "A 7.1.2" in body33,
           "the clause is cited IN the block making the claim")

    # The old wording, asserted rather than quoted, must be gone. The Common CE
    # Failures block legitimately QUOTES it in order to reject it.
    bad = unquoted(t11, r"residual (?:dynamic )?stability area up to 40")
    report("grain_short_form_criterion_absent", not bad, "asserted=%s" % (bad or "none"))

    # ============ FAMILY A: the assumed shifted surface ==================
    report("grain_assumed_surface_not_the_roll",
           "not the vessel" in t11 and "rolling amplitude" in t11
           and "assumed shifted-surface angles" in t11,
           "the card says in terms that these are not roll angles")

    bad = unquoted(t11, r"shifts to an angle matching the rolling amplitude")
    report("grain_roll_amplitude_claim_absent", not bad, "asserted=%s" % (bad or "none"))

    partb = block(g11, "The Assumed Shift Angle Is a Code Assumption", 3400)
    report("grain_partB_clauses_by_number",
           all(k in partb for k in ("B 2.3", "B 5.1", "B 3.2.1", "B 3.3",
                                    "B 1.3", "B 1.5", "1.06", "1.12")),
           "every configuration is named IN the section that enumerates them")

    report("grain_both_angles_and_their_conditions",
           "filled compartment, trimmed" in t11
           and "A 16, A 17 or A 18" in t11
           and t11.count("15") >= 3 and t11.count("25") >= 3,
           "15 and 25 each tied to the configuration that produces it")

    report("grain_no_universal_shift_angle",
           "no one angle applies to every grain compartment" in t11,
           "the card denies a single universal angle explicitly")

    report("grain_ce_tip_carries_both_angles",
           all(k in block(g11, "ce-tip", 2600) for k in ("B 2.3", "B 5.1", "1.12")),
           "the CE tip's filled/partly-filled split is clause-anchored")

    # ============ FAMILY A: casualty and vessel claims ==================
    # Flat absence is safe here: nothing in the corrected card quotes the name.
    report("leros_strength_absent_from_page",
           "leros" not in htmllib.unescape(pages["QB2_A.html"]).lower(),
           "no grain casualty is attributed to her anywhere on the page")

    report("grain_casualty_link_says_none_needed",
           "No specific casualty is necessary" in t11
           and "transverse grain shift" in t11,
           "the block states the position rather than leaving a hole")

    bad = unquoted(t11, r"geared (?:bulk )?fleet|geared fleet configurations")
    report("grain_fabricated_vessel_claim_absent", not bad,
           "asserted=%s" % (bad or "none"))

    report("grain_on_my_vessel_is_truthful",
           "not a cargo regime I operate" in t11
           and "would not claim grain experience I do not have" in t11
           and "container vessels" in t11,
           "the block asserts only what is true of the ship he sails")

    keynums = block(g11, "Key Numbers", 3000)
    report("grain_gm_attributed_to_the_code",
           "A 7.1.3" in keynums
           and not unquoted(keynums, r"0\.30 met\w+ .{0,80}SOLAS VI"),
           "the 0.30 m is the Grain Code's criterion, not SOLAS VI's")

    report("grain_accepted_substance_intact",
           all(k in t11 for k in ("A 3.1", "A 3.2", "A 3.5", "MSC.552(108)",
                                  "Document of Authorisation"))
           and all(k in t33 for k in ("MSC.552(108)", "23 May 2024",
                                      "1 January 2026")),
           "the DoA regime and the whole 2026 amendment layer survive")

    # ============ FAMILY B: CO2 is not categorically useless ============
    report("liion_co2_can_suppress_flaming_combustion",
           "can suppress oxygen-dependent flaming combustion in an enclosed "
           "protected space" in t7,
           "limb B is stated positively, in the trap the examiner asks")

    report("liion_co2_cannot_cool_or_terminate",
           "cannot cool the battery or terminate the internal thermal runaway" in t7
           and "removes no heat from the cells" in t7
           and "re-ignition" in t7,
           "limb A survives the correction, in two places")

    bad = unquoted(t7, r"CO2 will not extinguish|will not extinguish a Li-ion")
    report("liion_categorical_uselessness_absent", not bad,
           "asserted=%s" % (bad or "none"))

    # ============ FAMILY B: do not withhold the fixed system ============
    report("liion_no_withholding_instruction",
           "Do not tell the panel you would withhold an installed fixed system"
           in t7,
           "the instruction is reversed explicitly, not merely deleted")

    bad = unquoted(t7, r"waste your fixed extinguishing agent")
    report("liion_waste_the_agent_claim_absent", not bad,
           "asserted=%s" % (bad or "none"))

    report("liion_release_decision_is_the_masters",
           "fire control plan" in t7
           and re.search(r"Master.{0,80}decision|decision for the Master", t7)
           and "not the mere presence of lithium cells" in t7,
           "who decides, and what it does NOT turn on")

    report("liion_release_criteria_enumerated",
           all(k in t7 for k in ("enclosed", "sealed", "unaccounted for inside",
                                 "actually installed", "accessibility")),
           "location / enclosure / persons / installation / accessibility")

    report("liion_action_sequence_is_conditioned",
           "under the Master" in t7 and "depends on where" in t7,
           "no universal sequence detached from the ship survives")

    report("liion_boundary_vs_direct_cooling",
           t7.count("direct cooling of the cells") >= 2
           and "only the boundary" in t7,
           "the two cooling regimes are distinguished, more than once")

    # ============ FAMILY B: the wrong-scope circular =====================
    report("msc1615_ro_ro_scope_stated",
           "ro-ro spaces and special category spaces" in t7
           and "ro-ro passenger ships" in t7,
           "the real scope is on the page, in the row that cites it")

    report("msc1615_not_generic_container_guidance",
           "not" in t7 and "generic containership" in t7
           and "must not be quoted as though it were" in t7,
           "the negative is stated to the candidate explicitly")

    bad = unquoted(t7, r"Guidelines for preventing and mitigating lithium battery fires")
    report("msc1615_false_title_absent", not bad, "asserted=%s" % (bad or "none"))

    report("imdg_transport_and_firefighting_separated",
           "transport classification" in t7
           and "not shipboard firefighting guidance" in t7
           and "UN 3480" in t7 and "UN 3481" in t7,
           "classification labelled as transport, not tactics")

    report("ems_qualified_to_the_amendment_in_force",
           "amendment in force" in t7 and "F-A" in t7 and "S-I" in t7,
           "EmS is not asserted as a remembered pair")

    report("liion_accepted_substance_intact",
           all(k in t7 for k in ("separator", "Hydrofluoric", "vermiculite",
                                 "Felicity Ace", "SCBA")),
           "mechanism, AVD, casualty and the HF tip all survive")

    # ============ FAMILY C: the surviving EIAPP site ====================
    bad = unquoted(t2, r"invalidat\w*\s+(?:the\s+)?EIAPP|EIAPP is invalidated")
    report("eiapp_absolute_invalidation_absent", not bad,
           "asserted=%s" % (bad or "none"))

    dd = block(j2, "Deep-Dive: Trap Questions", 3000)
    report("eiapp_deepdive_carries_governed_wording",
           "full range of adjustments the NOx Technical File identifies as "
           "allowable" in dd
           and "engine parameter check method" in dd
           and "can leave the engine no longer compliant" in dd,
           "the illustration now says what the rule above it says")

    report("eiapp_pass1_wording_still_intact",
           "can render the engine non-compliant" in t2
           and t2.count("can leave the engine no longer compliant") >= 2,
           "the body Trap point and REG-BOX are unchanged")

    report("qb5j_accepted_spine_intact",
           all(k in t2 for k in ("42,700", "ISO 3046-1", "ISO 19030",
                                 "fuel index")),
           "the Pass-1 diagnostic spine is untouched")

    # ============ FAMILY D: QB5_C_B#q5 ==================================
    # Read the answer out of ITS OWN practice-block. Mutation AA moved the
    # text into a sibling div, leaving the authorised block empty again, and a
    # windowed read walked straight into the sibling and passed.
    m15 = re.search(r'<span class="pb-label">15-Second Answer</span>(.*?)</div>',
                    c5, re.S)
    fifteen = flatten(m15.group(1)) if m15 else ""
    report("qb5cb_15s_answer_is_substantive",
           len(fifteen) > 300 and "marine safety investigation" in fifteen
           and "9" in fifteen and "preserve" in fifteen.lower(),
           "len=%d" % len(fifteen))

    report("qb5cb_15s_answer_claims_no_investigator_role",
           "not to investigate" in fifteen,
           "the CE's limit is stated in the layer he recites first")

    report("qb5cb_ism_section_5_absent",
           "ISM Code Section 5" not in t5 and "ISM Code section 5" not in t5,
           "the Master's-authority clause is gone from a casualty reg-box")

    # C: every regulatory proposition must have BOTH a code and a description.
    reg = re.search(r'<div class="reg-box">.*?</div>\s*(?:</div>)?', c5, re.S)
    items = re.findall(r'<div class="reg-item">(.*?)</div>', c5, re.S)
    malformed = [i for i in items
                 if 'class="reg-code"' not in i or 'class="reg-desc"' not in i]
    report("qb5cb_regbox_rows_well_formed",
           bool(reg) and len(items) == 4 and not malformed,
           "rows=%d malformed=%d" % (len(items), len(malformed)))

    report("qb5cb_cic_full_instrument_identity",
           t5.count("Marine Casualty or Marine Incident") >= 2
           and t5.count("MSC.255(84)") >= 2,
           "full identity in BOTH the body and the reg-box, count=%d"
           % t5.count("Marine Casualty or Marine Incident"))

    ce_tip = block(c5, 'class="ce-tip"', 2400)
    report("qb5cb_ce_tip_is_the_real_discriminator",
           "who investigates" in ce_tip
           and "flag State" in ce_tip and "9" in ce_tip
           and "hostage" not in ce_tip,
           "the tip answers the question the card actually asks")

    bad = unquoted(t5, r"seize and lock away|Physically seize")
    report("qb5cb_no_seizure_of_statutory_records", not bad,
           "asserted=%s" % (bad or "none"))

    report("qb5cb_preservation_principle_stated",
           "not mine to impound" in t5
           and "chain of custody" in t5
           and "remain available for inspection" in t5
           and "those authorised to receive them" in t5,
           "preserve / prevent alteration / make available / custody")

    bad = unquoted(t5, r"will result in immediate criminal prosecution")
    report("qb5cb_automatic_consequence_absent", not bad,
           "asserted=%s" % (bad or "none"))

    report("qb5cb_legal_consequence_is_conditional",
           "may lead to investigation" in t5
           and "it is not automatic" in t5
           and "decided by the competent authority on the evidence" in t5,
           "conditional, and says so in terms")

    report("qb5cb_professional_warning_not_weakened",
           "unaltered record" in t5 and "the exposure is real" in t5,
           "softening the modality did not soften the warning")

    report("qb5cb_accepted_substance_intact",
           all(k in t5 for k in ("True Confidence", "s.231", "Voyage Data "
                                 "Recorder", "Designated Person Ashore"))
           and "training scenario" in t5,
           "governed MS Act, VDR, DPA and the casualty-premise note survive")

    # ============ FAMILY D artefact: the cheat-sheet hook ===============
    cs = read_text(CHEATSHEET)
    rows = re.findall(r"<tr>(.*?)</tr>", cs, re.S)
    pre = [r for r in rows if "Pre-arrival" in r]
    man = [r for r in rows if "Manning check" in r]
    report("cheatsheet_prearrival_v14_hook_removed",
           len(pre) == 1 and "V/14" not in pre[0] and "6.3" in pre[0],
           "the unsupported hook is gone; ISM 6.3 remains")
    report("cheatsheet_manning_v14_hook_retained",
           len(man) == 1 and "V/14" in man[0],
           "V/14 kept where manning is actually the subject")

    # ============ governance the product cannot show ====================
    auth_l = json.dumps(records["liion"].get("authority") or {})
    report("msc1615_evidence_tier_recorded",
           "NOT HELD" in auth_l and "404" in auth_l
           and "SECONDARY SOURCES" in auth_l,
           "the record does not pretend the circular was read")

    report("msc1615_deviation_recorded",
           "RETENTION WITH AN EXPLICIT SCOPE LABEL WAS CHOSEN" in auth_l
           and "probably unnecessary" in auth_l,
           "a departure from the authorisation is visible in the record")

    ag = records["grain"].get("authority") or {}
    auth_g = json.dumps(ag)
    # FIELD BY FIELD, not a blob search. Mutation Z5 replaced the A 7.1.2 quote
    # with a paraphrase and escaped, because "whichever is the least" also
    # appears in why_the_old_wording_is_wrong -- a neighbouring field vouching
    # for one that had been gutted.
    report("grain_primary_text_recorded",
           "whichever is the least" in ag.get("operative_text_A_7_1_2", "")
           and "0.075 metre-radians" in ag.get("operative_text_A_7_1_2", "")
           and "at 15 degrees" in ag.get("operative_text_B_2_3", "")
           and "at 25 degrees" in ag.get("operative_text_B_5_1", "")
           and "5b2107d3" in ag.get("instrument", ""),
           "A 7.1.2, B 2.3 and B 5.1 each quoted in their own field")

    report("grain_ocr_limit_recorded",
           "OCR" in auth_g and "page image" in auth_g,
           "the scan's text-layer limit is on the record, not hidden")

    prop_q = json.dumps(records["qb5cb"].get("propagation") or {})
    unchanged_q = json.dumps(
        (records["qb5cb"]["cards"][0].get("deliberately_unchanged") or []))
    report("qb5cb_wider_defects_reported_not_fixed",
           "SEVEN remaining empty" in prop_q
           and "q1, q2, q3, q4, q6, q7 and q8" in prop_q
           and "STCW Table A-III/2" in unchanged_q,
           "the eighth defect found while fixing seven is on the record")

    report("qb5cb_cheatsheet_artefact_declared",
           any(a.get("path") == "meoclass1/QB5_B_CheatSheet.html"
               for a in records["qb5cb"].get("artefacts", [])),
           "a file no digest can pin is still inside the event's scope")

    prop_e = json.dumps(records["eiapp"].get("propagation") or {})
    report("eiapp_qb3f_adjudication_carried_forward",
           "QB3_F" in prop_e and "already conditional" in prop_e,
           "Pass 1's decision not to widen is re-asserted, not re-litigated")

    print("\n%d checks, %d FAIL%s"
          % (CHECKS, len(FAILS), (" -> %s" % FAILS) if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
