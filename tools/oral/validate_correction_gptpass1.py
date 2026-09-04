#!/usr/bin/env python3
"""
Content validator for CORR-GPT-PASS1-20260904.

WHY THIS EXISTS AND WHY THE DIGEST PIN IS NOT ENOUGH
----------------------------------------------------
`validate_corrections.py` answers "is this card still exactly the bytes that
were authorised?". SKILL.md 8.2a is explicit that this is a different question
from "is what was authorised actually right?", and a pin is perfectly happy
with wrong text because it pins whatever it is given.

The four propositions this record corrects are the shape that gap was written
for. NONE of them was a wrong FACT. Each was a CONDITIONAL rule stated in
ABSOLUTE terms:

    "invalidates the EIAPP certificate"      for  "can render non-compliant"
    "the standard method for separating"     for  "a framework for measuring"
    "those tables stop being valid"          for  "not, by themselves, sufficient"
    "Critical equipment - main engine, ..."  for  "typical examples an SMS may designate"

A fact check passes all four. The noun is identical in each pair and the claim
is not. So the substance is asserted here, as named checks, one per proposition
a future well-meaning edit could quietly lose -- and each is named so that
`mutate_correction_gptpass1.py` can require its mutation to trip THAT check
rather than the digest pin, which fires on any edit at all.

WHAT ELSE IS ASSERTED HERE, AND WHY
-----------------------------------
Two things beyond the cards, both of which would otherwise be decoration:

*   THE HISTORICAL RECORD IS ASSERTED TO STILL BE WRONG. `batch_h6_manifest.json`
    describes the critical-spares list as DERIVED from ISM 10.3 -- the
    proposition known_traps entry 64 overturned. It is deliberately NOT
    rewritten, because laundering a shipped batch's prose to make the original
    authoring look correct is precisely what the two record families exist to
    prevent. `h6_historical_prose_not_laundered` fails if some future pass
    "tidies" it, and the supersession chain is what carries the current truth.

*   THE SOURCE TRANCHE IS ASSERTED. `CORRECTION_FIELD_CLASSES` says in terms
    that a field no validator touches is decoration. This record's `artefacts`
    entry claims four specific registry outcomes, so those four are checked:
    the tier-1 Grain acquisition, the NON-DESTRUCTIVE demotion of the tier-2
    row it replaces, the discharge of PENDING_FILING on the MS Act corrigenda,
    and -- the one that matters most -- that the SOLAS II-2 row was NOT
    upgraded, because the consolidated text still is not held.

NEGATIVE CHECKS RUN ON UNESCAPED TEXT
-------------------------------------
A guard spelled `h&m` is blind to `h&amp;m`. Every banned-phrase search below
runs against `html.unescape()` of the page, never the raw markup.

REJECTED WORDINGS ARE EXEMPT ONLY WHEN QUOTED -- NOT WHEN MERELY "NEGATED"
--------------------------------------------------------------------------
A flat ban cannot be used, because the standard teaching move -- do not say
"the tables stop being valid" -- would fire on the sentence carrying the fix.
The LSA ventilation gate solved that with a 240-character NEGATION WINDOW: a
mention is forgiven if any denial word precedes it.

THAT WINDOW WAS TRIED HERE FIRST, AND THIS SUITE'S MUTATION J DEFEATED IT.
Reinstating "the moment the waterline is inclined they stop being valid" in the
CE Oral Tip ESCAPED, because the tip opens "Lead with the limitation, not the
definition" -- an unrelated `not`, ninety characters upstream, which the window
read as a denial of a claim made later in the same sentence. A negator scan
cannot tell what a negator is negating.

So the exemption here is narrower and mechanical: a mention is acceptable only
when it is DIRECTLY QUOTED. That still permits the teaching move, which the
house style writes in quotation marks anyway, and it cannot be satisfied by a
stray denial word elsewhere in the passage. Recorded because the same latent
weakness sits in every gate that borrowed the negation window.
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

CORRECTION_ID = "CORR-GPT-PASS1-20260904"
MANIFEST = HERE / "correction_corr_gpt_pass1_20260904_manifest.json"
H6_MANIFEST = HERE / "batch_h6_manifest.json"
REGISTRY = REPO / "docs" / "sources" / "MIW_SOURCE_REGISTRY.json"

TARGETS = [
    ("QB5_J.html", "q2", "meoclass1/QB5_J.html"),
    ("QB1_D.html", "q7", "meoclass1/QB1_D.html"),
    ("QB5_I.html", "q8", "meoclass1/QB5_I.html"),
]

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-46s %s" % ("PASS" if ok else "FAIL", check, detail))


def card_text(page_text: str, anchor: str) -> str:
    """The one card, unescaped, tags stripped to plain prose.

    QB1_D carries its short-form answers inside a JSON island rather than as
    markup, so the card block is taken by balanced-div scan (the same shape the
    digest extractor uses) rather than by 'up to the next q-card', which would
    stop short on the dialects that nest.
    """
    start = page_text.find('id="%s"' % anchor)
    assert start >= 0, "anchor not found: %s" % anchor
    start = page_text.rfind('<div class="q-card"', 0, start)
    assert start >= 0, "card not found: %s" % anchor
    depth, pos = 0, start
    pat = re.compile(r"<div\b|</div>")
    while True:
        m = pat.search(page_text, pos)
        if not m:
            break
        depth += -1 if m.group(0) == "</div>" else 1
        pos = m.end()
        if depth == 0:
            break
    flat = re.sub(r"<[^>]+>", " ", page_text[start:pos])
    return re.sub(r"\s+", " ", htmllib.unescape(flat))


_QUOTES = "\"\u201c\u201d\u2018\u2019'"


def unquoted(text: str, pattern: str) -> list[str]:
    """Every mention of `pattern` the card ASSERTS rather than quotes.

    A mention is exempt only if a quotation mark sits immediately either side
    of it (a trailing period inside the closing quote is allowed). See the
    module header: a negation window was tried here and mutation J walked
    straight through it.
    """
    bad = []
    for m in re.finditer(pattern, text, re.I):
        before = text[max(0, m.start() - 2):m.start()]
        after = text[m.end():m.end() + 3]
        opened = any(q in before for q in _QUOTES)
        closed = any(q in after for q in _QUOTES)
        if opened and closed:
            continue
        bad.append(text[max(0, m.start() - 56):m.start()].strip()
                   + " >>" + m.group(0))
    return bad


def main() -> int:
    print("correction content validator: %s" % CORRECTION_ID)

    # ---- the record ------------------------------------------------------
    if not MANIFEST.is_file():
        report("correction_record_present", False, "missing %s" % MANIFEST.name)
        print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
        return 1
    record = json.loads(read_text(MANIFEST))
    report("correction_record_present", True, MANIFEST.name)

    report("correction_record_authorised",
           record.get("status") == "AUTHORISED"
           and record.get("correction_id") == CORRECTION_ID,
           "status=%s id=%s" % (record.get("status"), record.get("correction_id")))

    declared = {(c.get("file"), c.get("anchor")): c for c in record.get("cards", [])}
    report("all_three_cards_declared",
           all((f, a) in declared for f, a, _ in TARGETS),
           "declared=%d" % len(declared))

    # The primary authority must be NAMED, not implied -- a correction whose
    # record does not say which instrument decided it cannot be re-checked.
    auth = json.dumps(record.get("authority") or {})
    report("nox_primary_authority_recorded",
           "2.4.1" in auth and "6.2.1.2" in auth and "allowable adjustments" in auth,
           "NTC 2.4.1 + 6.2.1.2 + the allowable-adjustment range are quoted")

    # The instrument was an image-only scan. If that stops being recorded, a
    # later reader will believe the clauses were read off a text layer.
    report("nox_access_limit_recorded",
           "image-only scan" in auth.lower() and "ocr" in auth.lower(),
           "the OCR route and the empty text layer are on the record")

    # ---- supersession ancestry -------------------------------------------
    want_pred = {
        ("QB5_J.html", "q2"): ("batch_h6_manifest.json", "H6-001"),
        ("QB1_D.html", "q7"): ("correction_corr_cetip_qb1d_q7_20260902_manifest.json",
                               "CORR-CETIP-Q7-01"),
        ("QB5_I.html", "q8"): ("correction_corr_ism_spares_20260902_manifest.json",
                               "CORR-ISM-01"),
    }
    bad_chain = []
    for key, (mani, act) in want_pred.items():
        sup = (declared.get(key) or {}).get("supersedes") or {}
        if sup.get("manifest") != mani or sup.get("action_id") != act:
            bad_chain.append("%s#%s" % key)
        elif sup.get("post_edit_digest") != (declared[key] or {}).get("pre_edit_digest"):
            bad_chain.append("%s#%s chain-break" % key)
    report("supersession_ancestry_declared", not bad_chain,
           "bad=%s" % (bad_chain or "none"))

    # ---- the live cards --------------------------------------------------
    pages = {}
    for fname, anchor, rel in TARGETS:
        page = read_text(REPO / rel)
        pages[fname] = page
        live = card_digests(page)[anchor]
        entry = declared[(fname, anchor)]
        # RESOLVED THROUGH THE CHAIN, NOT COMPARED RAW. `live == my pin` asks
        # "is my state live?", and that stopped being true on 2026-09-04 when
        # CORR-GPT-T1-EIAPP-20260904 corrected one surviving EIAPP site in
        # QB5_J#q2 -- a legitimate, authorised, declared successor. The claim
        # this record can make forever is the stronger one: my state is the
        # ANCESTOR of what is live, with a continuous chain in between. With no
        # successor declared this is byte-for-byte the original comparison.
        res = resolve_authorised_card_state(
            manifest=MANIFEST.name, action_id=entry["correction_action_id"],
            file=fname, anchor=anchor,
            pinned_post_digest=entry.get("post_edit_digest"),
            live_digest=live, directory=MANIFEST.parent)
        report("digest_matches_manifest_%s" % fname.split(".")[0].lower(),
               bool(getattr(res, "ok", False)),
               "%s live=%s" % (getattr(res, "status", res), live[:16]))

    jt = card_text(pages["QB5_J.html"], "q2")
    dt = card_text(pages["QB1_D.html"], "q7")
    it = card_text(pages["QB5_I.html"], "q8")

    # ================= QB5_J#q2 -- 1A, NOx ================================
    report("nox_file_defines_approved_configuration",
           re.search(r"identifies the components, settings and operating values", jt)
           is not None
           and "approved NOx-relevant components, settings and operating values" in jt,
           "both the body and the reg-box state what the file defines")

    # 2.4.1.2 is the clause that makes the absolute claim impossible. If the
    # card stops saying adjustment is allowed at all, the correction is lost.
    report("nox_allowable_adjustment_range_stated",
           "full range of adjustments that are allowed" in jt
           and "full range of allowable adjustments" in jt,
           "the allowable-adjustment range survives in body and reg-box")

    report("nox_approved_route_stated",
           "amendment of the technical file" in jt
           and "engine parameter check method" in jt
           and "approved procedure, verification or survey route" in jt,
           "technical-file amendment + parameter check + survey route")

    report("nox_consequence_is_conditional",
           "can leave the engine no longer compliant" in jt
           and "can render the engine non-compliant" in jt,
           "both locations say CAN, and name the certified NOx configuration")

    bad = unquoted(jt, r"invalidat\w*\s+(?:the\s+)?EIAPP")
    report("nox_absolute_invalidation_absent", not bad, "asserted=%s" % (bad or "none"))

    report("nox_practical_warning_preserved",
           "casually to chase performance" in jt,
           "the oral warning survives the rewrite")

    # ================= QB5_J#q2 -- 1B, ISO 19030 ==========================
    report("iso19030_scope_is_hull_and_propeller",
           jt.count("changes in hull and propeller performance") >= 2,
           "measurement scope stated in body and reg-box")

    # Mutation I gutted the reg-box coupling and this check still passed,
    # because two surviving mentions elsewhere satisfied a count of >= 2. A
    # global count is a proxy for a proposition, never the proposition.
    report("iso19030_needs_corrected_engine_data",
           jt.count("corrected engine") >= 3
           and "distinguish the hull and propeller contribution" in jt
           and "read together with corrected engine-performance data it helps" in jt,
           "all three couplings present, including the reg-box's own")

    report("iso19030_not_an_engine_diagnostic",
           "does not itself assess engine condition" in jt,
           "the negative is stated explicitly to the candidate")

    bad = unquoted(jt, r"standard method for separating")
    report("iso19030_overclaim_absent", not bad, "asserted=%s" % (bad or "none"))

    report("qb5j_accepted_spine_intact",
           all(s in jt for s in ("42,700", "ISO 3046-1", "fuel index",
                                "weather", "draught")),
           "baseline / normalise / engine parameters / localise / confirm")

    # ================= QB1_D#q7 -- hydrostatics ===========================
    report("hydrostatics_stated_as_insufficient_not_invalid",
           "not, by themselves, sufficient" in dt
           and "no longer sufficient by themselves" in dt
           and "will not give you the answer on their own" in dt,
           "all three corrected locations carry the sufficiency formulation")

    bad = unquoted(dt, r"stop being valid")
    report("hydrostatics_invalidity_claim_absent", not bad,
           "asserted=%s" % (bad or "none"))

    report("hydrostatics_reason_is_per_station_draught",
           "every station is then at a different draught" in dt
           and "every station is at a different draught" in dt,
           "the corrected 60s answer and the already-correct body agree on WHY")

    report("bonjean_reconstruction_stated",
           "reconstruct the immersed sectional areas station by station" in dt,
           "the positive replacement claim is present")

    report("bonjean_accepted_substance_intact",
           all(s in dt for s in ("upright and on even keel", "Simpson",
                                 "longitudinal centre of buoyancy", "launching",
                                 "grounding", "immersed sectional area")),
           "every element the review accepted survives")

    # The two sections that were already right are the formulation the rest
    # was brought into line with. Losing them re-opens the defect.
    report("bonjean_already_correct_sections_kept",
           "Why the hydrostatic tables are not enough" in dt
           and "that assumption has failed" in dt,
           "body heading + deep-dive retained verbatim")

    # ================= QB5_I#q8 -- universal-list risk =====================
    report("critical_equipment_framed_as_example",
           "typical examples that a company" in it and "may designate" in it,
           "the list is introduced as SMS-designated examples")

    report("ism_does_not_prescribe_the_lists",
           "ISM 10.3 does not prescribe this list" in it
           and "the ISM Code prescribes no critical-spares list" in it,
           "stated once for equipment and once for spares")

    report("ship_specific_variation_stated",
           "legitimately differs from ship to ship" in it
           and "the vessel" in it and "risk assessment" in it,
           "variation is attributed to design, machinery and trade")

    report("class_spares_conditional",
           "where applicable under the vessel" in it
           and "differs between societies" in it
           and "rather than a single universal list" in it,
           "class rules conditioned on the ship's own rules and notation")

    # The ISM logic CORR-ISM-SPARES-20260902 established must survive intact;
    # this record corrects the illustration underneath it, nothing else.
    # Mutation Q replaced the operative phrase and this check still passed,
    # because the loose token "stand-by" survives in a nearby bullet heading.
    # Assert ISM 10.3's own words instead.
    report("ism_10_3_limbs_intact",
           "sudden operational failure" in it
           and "regular testing of stand-by arrangements" in it
           and "not in continuous use" in it,
           "identification + reliability measures + stand-by testing")

    report("ism_10_4_content_intact",
           "10.4" in it and "operational maintenance routine" in it,
           "10.4 keeps its own content")

    report("ce_inventory_answer_not_weakened",
           all(s in it for s in ("steering gear", "emergency fire pump",
                                 "oily-water separator", "fuel valves",
                                 "cylinder-liner", "PCBs")),
           "every named example survives in both lists")

    # ================= H6 governance residue ==============================
    # This check asserts that a WRONG historical record is STILL wrong.
    h6 = json.loads(read_text(H6_MANIFEST))
    h6_card = [c for c in h6.get("cards", [])
               if c.get("file") == "QB5_I.html" and c.get("anchor") == "q8"]
    report("h6_historical_prose_not_laundered",
           len(h6_card) == 1
           and "DERIVED from the ISM 10.3" in (h6_card[0].get("topic") or ""),
           "H6 still records what H6 shipped")

    report("h6_pin_not_rebaselined",
           len(h6_card) == 1
           and h6_card[0].get("post_edit_digest", "").startswith("4d3f8617"),
           "H6's release evidence is untouched; the chain carries the truth")

    # ================= source-governance tranche ==========================
    reg = json.loads(read_text(REGISTRY))
    rows = {s["source_id"]: s for s in reg["sources"]}

    tier1 = rows.get("SRC-GRAINCODE-MSC23-59") or {}
    report("grain_tier1_instrument_registered",
           tier1.get("access_status") == "RETRIEVED"
           and tier1.get("sha256") == ("5b2107d304bcfd8ad6c5cc080c33a94a"
                                       "9d168b5aaa3895277c61134e6cad8678"),
           "MSC.23(59) registered with its digest")

    # It is the ADOPTED baseline, not a consolidated edition. If that caveat
    # is ever dropped the row starts reading as present-day Grain Code text.
    report("grain_tier1_not_claimed_consolidated",
           "not a consolidated" in json.dumps(tier1).lower()
           and tier1.get("currentness") == "CURRENT_BUT_RECHECK_ON_EVENT",
           "baseline-vs-consolidated limit stated")

    old = rows.get("SRC-GRAINCODE-PARTA-TEXT") or {}
    report("grain_tier2_row_superseded_not_deleted",
           old.get("currentness") == "HISTORICAL_SUPERSEDED"
           and old.get("superseded_by") == "SRC-GRAINCODE-MSC23-59"
           and bool(old.get("verified_claims")),
           "predecessor retained with its evidence intact")

    corr = rows.get("SRC-MSACT-2025-CORRIGENDA") or {}
    report("msact_corrigenda_filed",
           "PENDING_FILING" not in str(corr.get("local_path"))
           and str(corr.get("local_path", "")).endswith(".pdf"),
           "local_path=%s" % str(corr.get("local_path"))[-46:])

    # The most important negative in the tranche: the review said do NOT
    # pretend primary IMO SOLAS text was acquired. It was not.
    solas = rows.get("SRC-SOLAS-II2-REG10-SPARECHARGES") or {}
    report("solas_row_not_overclaimed",
           solas.get("access_status") == "ACCESS_LIMITED"
           and not solas.get("local_path")
           and "still NO consolidated chapter II-2 text" in str(solas.get("access_note")),
           "consolidated SOLAS II-2 is still honestly recorded as not held")

    print("\n%d checks, %d FAIL%s"
          % (CHECKS, len(FAILS), (" -> %s" % FAILS) if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
