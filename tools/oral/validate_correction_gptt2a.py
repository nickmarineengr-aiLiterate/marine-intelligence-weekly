#!/usr/bin/env python3
"""
Content validator for the GPT high-risk review tranche 2A corrections:

    CORR-GPT-T2A-GRAIN-20260905   QB2_A#q27  + meoclass1/known_traps.md (artefact)
    CORR-GPT-T2A-QB5CB-20260905   QB5_C_B#q5
    CORR-GPT-T2A-IMSBC-20260905   QB2_B#q15

WHY A CONTENT GATE, WHEN validate_corrections.py ALREADY PASSES
---------------------------------------------------------------
`validate_corrections.py` answers "are these the bytes we authorised?".
SKILL.md 8.2a is explicit that this is a different question from "is what we
authorised actually right?" -- a digest pin is perfectly happy with wrong text.

Every proposition this tranche rests on is the shape that gap exists for:

    "the net residual area UNDER THE GZ CURVE"    for an area BETWEEN two curves
    "0.075 m-rad" with NO upper limit at all      for a LEAST-OF-THREE bound
    "STCW Table A-III/2"                          for a casualty-investigation regime
    "flexitanks ... comply with"                  for a regime that excludes them twice

None is a wrong noun. Each is a claim of the wrong SHAPE, and a fact check
passes all four. So the substance is asserted here as named checks, one per
proposition a future well-meaning edit could quietly lose, and each is named so
`mutate_correction_gptt2a.py` can require its mutation to trip THAT check
rather than the digest pin, which fires on any edit at all.

THE THREE CHECKS THAT GUARD SOMETHING OTHER THAN THE PRODUCT
------------------------------------------------------------
*   `grain_lower_bound_provenance_is_figure_a7`. The corrected card teaches the
    residual area as measured FROM THE ANGLE OF EQUILIBRIUM. That is true and
    it is what the Code depicts -- but the word "equilibrium" appears NOWHERE
    in the Code as adopted, and A 7.1.2 states only the upper bound. The lower
    bound comes from figure A7. If the record ever starts claiming it as clause
    text, the corpus acquires a quotation the instrument does not contain, and
    that is the same class of error this tranche exists to fix. Nothing about
    the product would change; only this check would notice.

*   `imsbc_solas_vi_vii_reported_not_implemented`. The brief authorised the
    SOLAS VI/VII limb only if it were a direct consequence of the scope
    correction. It is not, so it was reported instead -- with the operative
    texts, so GPT can decide in one step. Delete that from the record and the
    next pass reads a card whose two short layers it has no reason to doubt.

*   `grain_brief_premise_corrections_recorded`. The brief asserted two facts
    that the tree does not bear out: that q27 carried two incomplete forms of
    the 0.075 proposition (it carried one, and a Numbers block with none), and
    that q15's 15-second answer cites SOLAS VI (both short layers cite VII).
    Working around a wrong premise silently is how a reviewer's model of the
    corpus drifts from the corpus. Both corrections are on the record.

NEGATIVE CHECKS RUN ON UNESCAPED TEXT
-------------------------------------
A guard spelled `h&m` is blind to `h&amp;m`, and this tranche's first edit
attempt failed for exactly that reason in the other direction: the replacement
was written with `&deg;` while the published bytes carried a literal degree
sign. Every search below runs against `html.unescape()` of the markup, and the
degree pattern matches all three encodings.

AND THEY ARE SCOPED TO THE REJECTED PROPOSITION, NOT TO A KEYWORD
-----------------------------------------------------------------
The corrected q27 TEACHES AGAINST the old wording, so it legitimately contains
the words "the area under the GZ curve" and "up to 40". A keyword ban would
fire on the sentence carrying the fix -- the trap CORR-GPT-PASS1's header
records. Two devices avoid it, and neither is a negator scan (a negator scan
cannot tell what a negator is negating -- Pass 1's mutation J walked through
one):

  1. `unquoted()`: both rejected forms are QUOTED in the corrected card, so
     "asserted" versus "taught against" is a syntactic fact, not a judgement.
     The card text was written to make that true rather than the guard being
     bent to accommodate the card.
  2. `criterion_sentences()`: the 40-degree bound is asserted at SENTENCE
     level -- every sentence that states the 0.075 figure must also carry the
     least-of enumeration. A sentence, not a page, is the unit a proposition
     lives in, and a global count is a proxy for a proposition, never the
     proposition itself.
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
    "grain": HERE / "correction_corr_gpt_t2a_grain_20260905_manifest.json",
    "qb5cb": HERE / "correction_corr_gpt_t2a_qb5cb_20260905_manifest.json",
    "imsbc": HERE / "correction_corr_gpt_t2a_imsbc_20260905_manifest.json",
}

TARGETS = [
    ("grain", "QB2_A.html", "q27", "meoclass1/QB2_A.html"),
    ("qb5cb", "QB5_C_B.html", "q5", "meoclass1/QB5_C_B.html"),
    ("imsbc", "QB2_B.html", "q15", "meoclass1/QB2_B.html"),
]

AUTH_DOC = ("meoclass1/oral-intelligence/examiner-audit/"
            "GPT_REVIEW_HIGHRISK_TRANCHE2A_20260905.md")

KNOWN_TRAPS = REPO / "meoclass1/known_traps.md"

# q26 was found clean by Pass 2 and must not move. This is the pin, and it is
# the ONLY thing that would catch an over-correction that tidied the
# neighbouring card while it was in the editor.
Q26_DIGEST = "adfa6bbde6599be1dcfccef569cb4ef3c8c3ff982546697f41614ef8507fa567"

# Matches the degree sign however it is encoded. The first edit attempt of this
# tranche failed with occurrences=0 because it assumed one encoding.
DEG = r"(?:°|&deg;|\s*degrees?)"

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-52s %s" % ("PASS" if ok else "FAIL", check, detail))


def card_html(page: str, anchor: str) -> str:
    """The one card's raw markup, by balanced-div scan."""
    start = page.find('id="%s"' % anchor)
    assert start >= 0, "anchor not found: %s" % anchor
    start = page.rfind('<div class="q-card', 0, start)
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


def _quoted_spans(text: str) -> list[tuple]:
    """(start, end) of every paired curly-quote span in the text."""
    spans, open_at = [], None
    for i, ch in enumerate(text):
        if ch == "“":
            open_at = i
        elif ch == "”" and open_at is not None:
            spans.append((open_at, i))
            open_at = None
    return spans


def unquoted(text: str, pattern: str) -> list[str]:
    """Every mention of `pattern` the text ASSERTS rather than directly quotes.

    QUOTING IS A SPAN RELATION, NOT CHARACTER ADJACENCY. The tranche-1 gate
    exempted a match only when a quote sat within two characters either side.
    That works only when the rejected phrase happens to be quoted at exactly its
    own boundaries, which is an accident of phrasing rather than a property of
    the claim: here the card quotes "the area under the GZ curve up to 40°",
    so the opening quote is four characters early and the closing one is nine
    late, and an adjacency test called a taught-against phrase an assertion.
    Containment inside a paired quote span is what "directly quotes" actually
    means, and it does not care where the phrase sits inside the quotation.

    It is deliberately NOT a negator scan. A negator scan cannot tell what a
    negator is negating -- Pass 1's mutation J walked through one.
    """
    spans = _quoted_spans(text)
    bad = []
    for m in re.finditer(pattern, text, re.I):
        if any(a < m.start() and m.end() <= b for a, b in spans):
            continue
        bad.append(text[max(0, m.start() - 60):m.start()].strip() + " >>" + m.group(0))
    return bad


def criterion_sentences(text: str) -> list[str]:
    """Every sentence that states the 0.075 figure.

    The unit a proposition lives in is a sentence. Asserting "the card mentions
    'least' somewhere" would pass a card that stated the criterion correctly in
    one block and bare in another -- which is precisely the state q11 and q33
    were left in by the pre-tranche-1 corpus.
    """
    out = []
    for sentence in re.split(r"(?<=[.;])\s+", text):
        if "0.075" in sentence:
            out.append(sentence)
    return out


def block(markup: str, needle: str, span: int = 2600) -> str:
    """Flattened text of the region that starts at `needle`."""
    i = markup.find(needle)
    return flatten(markup[i:i + span]) if i >= 0 else ""


def main() -> int:  # noqa: C901
    print("correction content validator: GPT high-risk review tranche 2A")

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
           "all three AUTHORISED, origin gpt_content_review")

    report("authorisation_source_shared_and_present",
           all(r.get("authorisation_source") == AUTH_DOC for r in records.values())
           and (REPO / AUTH_DOC).is_file(),
           "one authorisation record for the tranche")

    declared = {}
    for key, rec in records.items():
        for c in rec.get("cards", []):
            declared[(c.get("file"), c.get("anchor"))] = (key, c)
    report("all_three_cards_declared",
           all((f, a) in declared for _, f, a, _ in TARGETS),
           "declared=%d" % len(declared))

    # ---- supersession ancestry ---------------------------------------
    # q27 declares NONE, deliberately: no record has ever owned it. Asserting
    # its absence is as load-bearing as asserting the other two chains, because
    # a fabricated ancestor would be a claim that some earlier record vouched
    # for this card, and none did.
    q27_card = declared[("QB2_A.html", "q27")][1]
    report("grain_q27_declares_no_ancestry",
           "supersedes" not in q27_card
           and "never been owned" in (q27_card.get("supersession_note") or ""),
           "q27 was unowned before this record, and says so")

    want_pred = {
        ("QB5_C_B.html", "q5"): ("correction_corr_gpt_t1_qb5cb_20260904_manifest.json",
                                 "CORR-GPT-T1-QB5CB-01"),
        ("QB2_B.html", "q15"): ("batch_h3b1_manifest.json", "H3B1-006"),
    }
    bad_chain = []
    for tgt, (mani, act) in want_pred.items():
        sup = declared.get(tgt, (None, {}))[1].get("supersedes") or {}
        if sup.get("manifest") != mani or sup.get("action_id") != act:
            bad_chain.append("%s#%s" % tgt)
    report("supersession_ancestry_declared", not bad_chain,
           "predecessors named: %s" % (bad_chain or "q5 <- T1-QB5CB-01, q15 <- H3B1-006"))

    # ---- live digests, resolved through any chain ---------------------
    pages = {}
    live_bad = []
    for key, fname, anchor, rel in TARGETS:
        page = read_text(REPO / rel)
        pages[(fname, anchor)] = card_html(page, anchor)
        live = card_digests(page).get(anchor)
        card = declared[(fname, anchor)][1]
        res = resolve_authorised_card_state(
            manifest=RECORDS[key].name,
            action_id=card["correction_action_id"],
            file=fname, anchor=anchor,
            pinned_post_digest=card["post_edit_digest"],
            live_digest=live)
        if not res.ok:
            live_bad.append("%s#%s: %s" % (fname, anchor, res.describe()))
    report("live_cards_match_authorised_state", not live_bad,
           "mismatched=%s" % (live_bad or "three cards, resolved through their chains"))

    q27 = flatten(pages[("QB2_A.html", "q27")])
    q5 = pages[("QB5_C_B.html", "q5")]
    q15 = pages[("QB2_B.html", "q15")]

    # =================== GRAIN: the named gates ========================
    report("q27_area_is_between_the_two_curves",
           re.search(r"between the heeling arm curve and the righting arm curve",
                     q27, re.I) is not None,
           "the object is the area BETWEEN two curves")

    sentences = criterion_sentences(q27)
    report("q27_criterion_stated_at_least_once", len(sentences) >= 1,
           "%d sentence(s) state 0.075" % len(sentences))

    bare = [s[:80] for s in sentences if not re.search(r"\bleast\b", s, re.I)]
    report("q27_no_criterion_sentence_bounds_only_at_40", not bare,
           "every 0.075 sentence carries the least-of enumeration"
           if not bare else "bare=%s" % bare)

    # BLOCK-SCOPED, NOT CARD-SCOPED. Both of the next two checks were written
    # card-wide first, and the mutation suite walked straight through both:
    # deleting the lower bound from the body left the Numbers entry's copy
    # standing, and deleting the flooding angle from the Numbers entry left the
    # body's. A proposition that must appear in two places has to be asserted in
    # two places -- the card is not the unit it lives in.
    body = block(pages[("QB2_A.html", "q27")], "For Grain Shift Risks", 3000)
    numbers = block(pages[("QB2_A.html", "q27")], "Numbers to Memorise", 1600)

    limbs = {
        "maximum difference": r"maximum[- ]difference|maximum difference between the ordinates",
        "40 degrees": r"40" + DEG,
        "flooding angle": r"angle of flooding|flooding angle",
    }
    missing = ["%s in %s" % (n, where)
               for where, text in (("body", body), ("numbers", numbers))
               for n, pat in limbs.items() if not re.search(pat, text, re.I)]
    report("q27_states_all_three_least_of_limits", not missing,
           "missing=%s" % (missing or "all three limbs in BOTH criterion blocks"))

    report("q27_teaches_angle_of_equilibrium_lower_bound",
           re.search(r"from the angle of equilibrium", body, re.I) is not None
           and re.search(r"figure A7", body, re.I) is not None,
           "lower bound taught in the block that teaches the detailed criterion,"
           " and attributed to figure A7 not to the clause")

    asserted_gz = unquoted(q27, r"area under the GZ curve")
    report("q27_never_asserts_area_under_the_gz_curve", not asserted_gz,
           "both mentions are quoted rejections"
           if not asserted_gz else "asserted=%s" % asserted_gz)

    # Both residual sites, by the block they live in -- not by a global count.
    report("q27_body_site_corrected",
           "0.075" in body and "least of" in body.lower()
           and "between the heeling arm curve" in body,
           "the Risk Mitigations bullet carries the full criterion")
    report("q27_numbers_site_corrected",
           "0.075" in numbers and "least of" in numbers.lower()
           and "A 7.1.2" in numbers,
           "Numbers to Memorise carries the criterion it never had")

    report("q27_12_degree_entry_carries_deck_edge_limb",
           re.search(r"deck edge is immersed", numbers, re.I) is not None
           and "A 7.1.1" in numbers,
           "A 7.1.1's second limb is in the Numbers block, as it is on q11")

    q26_live = card_digests(read_text(REPO / "meoclass1/QB2_A.html")).get("q26")
    report("q26_byte_unchanged", q26_live == Q26_DIGEST,
           "q26 %s" % ("unmoved" if q26_live == Q26_DIGEST else "MOVED -> %s" % q26_live))

    auth_g = json.dumps(records["grain"].get("authority") or {})
    report("grain_lower_bound_provenance_is_figure_a7",
           "NO CLAUSE OF THE CODE STATES THE LOWER BOUND" in auth_g
           and "figure_A7_derived_not_quoted" in auth_g,
           "the record does not claim the lower bound as A 7.1.2 clause text")

    verdict_g = records["grain"].get("candidate_verdict") or ""
    report("grain_brief_premise_corrections_recorded",
           "TWO CORRECTIONS TO THE BRIEF'S OWN FACTUAL PREMISE" in verdict_g
           and "There is no third site" in verdict_g,
           "the sweep's disagreement with the brief is on the record")

    prop_g = json.dumps(records["grain"].get("propagation") or {})
    report("grain_q11_q33_residuals_reported_not_fixed",
           "Net Residual Area on GZ Curve" in prop_g
           and "Neither q11 nor q33 teaches the LOWER bound" in prop_g,
           "two findings on tranche-1 cards are queued, not silently swept")

    # =================== known_traps: the authoring source =============
    traps = read_text(KNOWN_TRAPS)
    report("known_traps_short_form_removed",
           "0.075 m·rad** residual area to 40" not in traps
           and "residual area to 40°" not in traps,
           "the short form is gone from the authoring file")
    report("known_traps_carries_full_a71",
           "A 7.1.1" in traps and "A 7.1.2" in traps and "A 7.1.3" in traps
           and "between the heeling arm curve and the righting arm curve" in traps,
           "trap 55 states the three criteria in full")
    report("known_traps_carries_authoring_rule",
           "AUTHORING RULE" in traps
           and "never write the A 7.1.2 criterion in the short form" in traps,
           "a standing rule, not just a repaired sentence")
    report("known_traps_msc552_layer_intact",
           "MSC.552(108)" in traps and "A 2.8" in traps and "B 1.1.5" in traps
           and "MSC.575(110)" in traps,
           "the 2026 amendment content of trap 55 survived the edit")
    # The other 36 correction records on disk each leave an authoring trap, and
    # validate_corrections asserts one exists. Existence is the weak claim; what
    # matters is that the trap carries the RULE, so these two check the
    # proposition rather than the heading number.
    report("known_traps_74_states_the_regbox_rule",
           "### 74." in traps
           and "Table A-III/2" in traps
           and "answering a question the card did not ask" in traps
           and "Never add a regulation" in traps,
           "trap 74 carries the reference-row rule, not just the incident")
    report("known_traps_75_states_the_definition_rule",
           "### 75." in traps
           and "without any intermediate form of containment" in traps
           and "EITHER ONE SUFFICIENT" in traps
           and "MSC.575(110)" in traps,
           "trap 75 carries both exclusion limbs and the currency caution")

    want_traps = {"grain": 55, "qb5cb": 74, "imsbc": 75}
    bad_art = [k for k, n in want_traps.items()
               if not (any(a.get("path") == "meoclass1/known_traps.md"
                           for a in records[k].get("artefacts", []))
                       and n in (records[k].get("known_traps_entries") or []))]
    report("known_traps_declared_as_artefact", not bad_art,
           "all three records own their trap"
           if not bad_art else "undeclared=%s" % bad_art)

    # =================== QB5_C_B: the reg-box ==========================
    regbox = block(q5, '<div class="reg-box">', 4000)
    report("qb5cb_regbox_stcw_a_iii_2_removed",
           "A-III/2" not in flatten(q5),
           "STCW Table A-III/2 is gone from the whole card")
    report("qb5cb_regbox_has_ism_9",
           re.search(r"ISM Code §9", regbox) is not None
           or "ISM Code &sect;9" in q5,
           "ISM Code section 9 occupies the slot")
    report("qb5cb_ism9_row_states_company_sms_scope",
           "non-conformities, accidents and hazardous occurrences" in regbox
           and re.search(r"corrective action under §9\.2", regbox) is not None,
           "the row states SMS reporting/investigation and 9.2 corrective action")
    # Scoped to the reg-code of the row that must carry it. Card-wide, this
    # check passed while the resolution number was stripped off the Casualty
    # Investigation Code row, because the NEW ISM 9 row also cites MSC.255(84)
    # when denying that it is the statutory regime. A correction's own text
    # standing in for the thing it was meant to guard is a real escape.
    ci_row = re.search(r'<span class="reg-code">Casualty Investigation Code[^<]*</span>',
                       q5)
    report("qb5cb_regbox_retains_msc255_84",
           ci_row is not None and "MSC.255(84)" in ci_row.group(0)
           and "flag State" in regbox,
           "the statutory row still carries its resolution number")
    report("qb5cb_ism9_not_flag_state_investigation",
           re.search(r"is not the flag State’s statutory marine safety investigation",
                     regbox) is not None,
           "the row denies the reading the brief warned against, in terms")

    unchanged_q = json.dumps(
        records["qb5cb"]["cards"][0].get("deliberately_unchanged") or [])
    report("qb5cb_msc255_row_declared_byte_unchanged",
           "BYTE-UNCHANGED" in unchanged_q,
           "the correct row was not edited to carry the distinction")

    # =================== QB2_B: IMSBC scope ============================
    vessel = block(q15, "On My Vessel", 3000)
    report("qb2b_onmyvessel_no_containerised_cargo_under_imsbc",
           not re.search(r"containeri[sz]ed bulk shipments", vessel, re.I),
           "the containerised-bulk-under-IMSBC claim is gone")
    bad_flexi = [s for s in re.split(r"(?<=[.;])\s+", vessel)
                 if re.search(r"flexitank", s, re.I)
                 and re.search(r"IMSBC", s, re.I)
                 and not re.search(r"not|excluded|outside", s, re.I)]
    report("qb2b_onmyvessel_flexitank_not_inside_imsbc", not bad_flexi,
           "every flexitank sentence places it OUTSIDE the Code"
           if not bad_flexi else "bad=%s" % bad_flexi)
    report("qb2b_onmyvessel_states_the_definition",
           "without any intermediate form of containment" in vessel
           and "VI/1-1.2" in vessel,
           "the exclusion rests on the definition, with its regulation")
    report("qb2b_onmyvessel_names_the_governing_regimes",
           "IMDG" in vessel and re.search(r"CTU", vessel)
           and "Cargo Securing Manual" in vessel,
           "what does govern a containership is named")

    trap = block(q15, "difference between a Group B cargo", 900)
    report("qb2b_imsbc_imdg_distinction_preserved",
           "packaged form" in trap
           and re.search(r"loose, un-packaged", trap) is not None,
           "the card's already-correct trap answer survives")

    report("qb2b_no_2027_amendment_taught_as_mandatory",
           "MSC.575" not in flatten(q15) and "08-25" not in flatten(q15),
           "no IMSBC amendment 08-25 fact entered the card")
    auth_i = json.dumps(records["imsbc"].get("authority") or {})
    report("imsbc_currentness_position_recorded",
           "1 January 2027" in auth_i and "DELIBERATELY NOT INTRODUCED" in auth_i,
           "the evolving-instrument position is on the record, not in the card")

    report("imsbc_solas_vi_vii_reported_not_implemented",
           "SOLAS VI vs VII" in read_text(REPO / AUTH_DOC)
           and "NOT IMPLEMENTED" in read_text(REPO / AUTH_DOC)
           and "SEPARATE defect" in json.dumps(
               records["imsbc"]["cards"][0].get("deliberately_unchanged") or []),
           "the unauthorised limb is reported with its evidence, not silently left")

    effects = [r.get("content_index_effect") or "" for r in records.values()]
    report("content_log_entry_deferred_on_the_record",
           all("DECISION, NOT AN OMISSION" in e and "OWED" in e for e in effects),
           "the un-written correction-log entry is a recorded decision")

    print("\n%d checks, %d FAIL%s"
          % (CHECKS, len(FAILS), (" -> %s" % FAILS) if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
