#!/usr/bin/env python3
"""
Content validator for the GPT high-risk review tranche 2C corrections:

    CORR-GPT-T2C-ONMYVESSEL-20260905  QB5_C_B#q5, QB2_A#q27
                                      + tools/oral/qb_content_index_governed.json
    CORR-GPT-T2C-LNGASPHYX-20260905   QB7_D#q14
    CORR-GPT-T2C-GRAIN-20260905       QB2_A#q11
    CORR-GPT-T2C-IMSBC-20260905       QB2_B#q15
    CORR-GPT-T2C-CURRENCY-20260905    QB4_H#q13, QB5_E#q4, QB7_D#q15, QB3_C#q7

WHY A CONTENT GATE, WHEN validate_corrections.py ALREADY PASSES
---------------------------------------------------------------
`validate_corrections.py` answers "are these the bytes we authorised?".  A
digest pin is perfectly happy with wrong text, and every proposition this
tranche rests on is the shape that gap exists for:

    an automated fleet cloud-sync backup       for a capability nothing establishes
    "the sole Indian national aboard"          for a fact reporting does not reach
    "a mandatory framework under chapter VII"  for a Code chapter VI makes mandatory
    "Net Residual Area on GZ Curve"            for an area BETWEEN two curves
    "the 2026 edition"                         for a 1st Edition (2025), updated 2026
    "ISO 23306:2020"                           with no currency statement at all

None is a wrong noun.  Each is a claim of the wrong SHAPE or of the wrong
STRENGTH, and a spell check, a link check and a digest pin all pass every one.

THE CHECKS THAT GUARD SOMETHING OTHER THAN THE PRODUCT
------------------------------------------------------
*   `no_asphyxiation_entry_material_imported`.  The brief authorised ONE danger
    and named four things that must not arrive with it: enclosed-space entry
    permits, rescue procedures, a full atmosphere-testing regime, and unrelated
    confined-space material.  Over-import is the failure mode a "did the fix
    land?" check cannot see, because the fix DID land -- and then kept going.
    This is the only check that would notice.

*   `correction_log_note_free_of_barred_claim`.  The unverified True Confidence
    proposition was live in TWO places: the q5 card, and the governed
    correction-log note that generates into `meoclass1/qb_content_index.json`.
    The log is candidate-facing and is NOT a q-card, so no digest pin in this
    repo covers it.  Correcting only the card would have left the corpus
    publishing the barred claim, and every gate would have stayed green.

*   `grain_q11_lower_bound_not_quoted_as_clause_text`.  q11 now teaches the
    residual area FROM the angle of equilibrium.  That is true and it is what
    the Code depicts -- but the word "equilibrium" appears NOWHERE in the Code
    as adopted, and A 7.1.2 states only the upper bound.  If the card ever
    starts offering it as clause text, the corpus acquires a quotation the
    instrument does not contain, which is the same class of error this tranche
    exists to fix.

*   `bmp_propagation_reported_not_swept` and `k4_source_custody_gap_reported`.
    Two deviations that change no candidate-facing byte.  The BMP edition label
    is still wrong in six cards outside q13; MSC.551(108) and MSC.567(109) are
    NOT held in the true-source tree even though the card's footer says all five
    IGF amendments were read.  A deviation has to be visible in the record or
    the next reviewer cannot tell a decision from an oversight.

*   `brief_premise_corrections_recorded`.  The brief asserted three things the
    tree does not bear out: that q5 said "exactly five items" about IGF
    18.4.1.1.1, that q15's ISO card claimed no superseding standard was
    underway, and that q7 made an exhaustive "never been amended" claim.  None
    is true.  Working around a wrong premise silently is how a reviewer's model
    of the corpus drifts from the corpus.

NEGATIVE CHECKS RUN ON UNESCAPED TEXT, AND ARE SCOPED TO THE PROPOSITION
------------------------------------------------------------------------
A guard spelled `h&m` is blind to `h&amp;m`, and this tranche's first edit
attempt failed for exactly the mirror reason: the replacement was written with
`&mdash;` while the Casualty Link's published bytes carry a literal em dash.
Every search below runs against `html.unescape()` of the markup.

And the corrected cards TEACH AGAINST the old wordings, so they legitimately
contain the banned strings.  q13 says `never "the 2026 edition"`.  `unquoted()`
answers "asserted or quoted?" as a syntactic fact about paired quote spans
rather than as a judgement, and it is deliberately not a negator scan -- a
negator scan cannot tell what a negator is negating.
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
    "onmyvessel": HERE / "correction_corr_gpt_t2c_onmyvessel_20260905_manifest.json",
    "lngasphyx": HERE / "correction_corr_gpt_t2c_lngasphyx_20260905_manifest.json",
    "grain": HERE / "correction_corr_gpt_t2c_grain_20260905_manifest.json",
    "imsbc": HERE / "correction_corr_gpt_t2c_imsbc_20260905_manifest.json",
    "currency": HERE / "correction_corr_gpt_t2c_currency_20260905_manifest.json",
}

# (record key, page file, anchor, repo-relative path)
TARGETS = [
    ("onmyvessel", "QB5_C_B.html", "q5", "meoclass1/QB5_C_B.html"),
    ("onmyvessel", "QB2_A.html", "q27", "meoclass1/QB2_A.html"),
    ("lngasphyx", "QB7_D.html", "q14", "meoclass1/QB7_D.html"),
    ("grain", "QB2_A.html", "q11", "meoclass1/QB2_A.html"),
    ("imsbc", "QB2_B.html", "q15", "meoclass1/QB2_B.html"),
    ("currency", "QB4_H.html", "q13", "meoclass1/QB4_H.html"),
    ("currency", "QB5_E.html", "q4", "meoclass1/QB5_E.html"),
    ("currency", "QB7_D.html", "q15", "meoclass1/QB7_D.html"),
    ("currency", "QB3_C.html", "q7", "meoclass1/QB3_C.html"),
]

AUTH_DOC = ("meoclass1/oral-intelligence/examiner-audit/"
            "GPT_REVIEW_HIGHRISK_TRANCHE2C_20260905.md")

GOVERNED_LOG = REPO / "tools/oral/qb_content_index_governed.json"
PUBLISHED_INDEX = REPO / "meoclass1/qb_content_index.json"

# Cards the brief named and ACCEPTED.  These pins are the only thing that would
# catch an over-correction that tidied a neighbouring card while it was open.
#   q33  accepted on the residual-area start point; must NOT move for symmetry
#   q1   the "Herschberg" typo, DEFERRED because QB5_C_A is not otherwise opened
#   q3   QB2_F PFOS, verified correct under K-9 and deliberately not rewritten
HELD_PINS = {
    ("meoclass1/QB2_A.html", "q33"):
        "5e18d8b2d23febaad92e689b3c598bac31268550181ca1e0d71e38a5c6724220",
    ("meoclass1/QB5_C_A.html", "q1"):
        "dde663052929db79047728a3016aeb454848fd00c77e223cfd03f725f91248f8",
}

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-56s %s" % ("PASS" if ok else "FAIL", check, detail))


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


def _quoted_spans(text: str) -> list[tuple]:
    """(start, end) of every paired curly-quote span in the text."""
    spans, open_at = [], None
    for i, ch in enumerate(text):
        if ch in "“":
            open_at = i
        elif ch in "”" and open_at is not None:
            spans.append((open_at, i))
            open_at = None
    return spans


def unquoted(text: str, pattern: str) -> list[str]:
    """Every mention of `pattern` the text ASSERTS rather than directly quotes.

    Quoting is a SPAN relation, not character adjacency: q13 says
    never "the 2026 edition", so the phrase sits well inside a quotation whose
    boundaries are nowhere near it.  Containment inside a paired quote span is
    what "directly quotes" actually means.
    """
    spans = _quoted_spans(text)
    bad = []
    for m in re.finditer(pattern, text, re.I):
        if any(a < m.start() and m.end() <= b for a, b in spans):
            continue
        bad.append(text[max(0, m.start() - 70):m.start()].strip() + " >>" + m.group(0))
    return bad


def block(markup: str, needle: str, span: int = 2600) -> str:
    """Flattened text of the region that starts at `needle`.

    Scoped, because three checks in the tranche-2A suite escaped by being
    written CARD-WIDE for a proposition that lives in a BLOCK -- the
    correction's own explanatory text standing in for the thing it guarded.
    """
    i = markup.find(needle)
    return flatten(markup[i:i + span]) if i >= 0 else ""


def practice_block(markup: str, label: str) -> str:
    """Flattened text of ONE oral layer, bounded by its own div.

    A fixed byte span is not a block boundary: measured that way the
    15-second layer's word count ran on into the 60-second layer, so a
    "not bloated" budget was being applied to both layers at once. The unit a
    word budget lives in is the layer, and the layer's boundary is its markup.
    """
    i = markup.find(label)
    if i < 0:
        return ""
    j = markup.find("</div>", i)
    return flatten(markup[i:j if j > 0 else len(markup)])


def section(markup: str, start: str, end: str) -> str:
    """Flattened text between two MARKUP boundaries, not a byte count.

    A fixed span is not a block boundary, and this suite has now been bitten by
    that twice.  The 15-second word budget ran on into the 60-second layer; and
    `q15_cargo_groups_untouched` PASSED a mutation that deleted the cargo groups
    from the 15-second layer, because the 1600-character window reached into the
    60-second layer, which still had them.  A neighbouring block standing in for
    the block under test is the tranche-2A escape class, and the only fix is to
    stop at real markup.
    """
    i = markup.find(start)
    if i < 0:
        return ""
    j = markup.find(end, i + len(start))
    return flatten(markup[i:j if j > 0 else len(markup)])


def li_items(markup: str, heading: str) -> list[str]:
    """Flattened <li> texts of the first <ul> after `heading`."""
    i = markup.find(heading)
    if i < 0:
        return []
    j = markup.find("<ul>", i)
    k = markup.find("</ul>", j)
    if j < 0 or k < 0:
        return []
    # .strip() matters: flatten() collapses the newline after <li> into a
    # leading space, and an ORDER check written with startswith() then reports
    # "wrong position" for a list that is in exactly the right order. A guard
    # that fails on correct content is worse than no guard, because the next
    # reader repairs the card instead of the check.
    return [flatten(m.group(1)).strip()
            for m in re.finditer(r"<li>(.*?)</li>", markup[j:k], re.S)]


def main() -> int:  # noqa: C901
    print("correction content validator: GPT high-risk review tranche 2C")

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
           "all five AUTHORISED, origin gpt_content_review")

    auth_text = read_text(REPO / AUTH_DOC) if (REPO / AUTH_DOC).is_file() else ""
    report("authorisation_source_shared_and_present",
           all(r.get("authorisation_source") == AUTH_DOC for r in records.values())
           and bool(auth_text),
           "one authorisation record for the tranche")

    declared = {}
    for key, rec in records.items():
        for c in rec.get("cards", []):
            declared[(c.get("file"), c.get("anchor"))] = (key, c)
    report("all_nine_cards_declared",
           all((f, a) in declared for _, f, a, _ in TARGETS) and len(declared) == 9,
           "declared=%d" % len(declared))

    # ---- supersession ancestry ---------------------------------------
    # Every card in this tranche descends from something.  Unlike tranche 2A's
    # q27, none is unowned, so an ABSENT chain here is a defect rather than a
    # deliberate declaration -- and a WRONG predecessor is worse than none,
    # because it claims an earlier record vouched for a state it never saw.
    want_pred = {
        ("QB5_C_B.html", "q5"): ("correction_corr_gpt_t2a_qb5cb_20260905_manifest.json",
                                 "CORR-GPT-T2A-QB5CB-01"),
        ("QB2_A.html", "q27"): ("correction_corr_gpt_t2a_grain_20260905_manifest.json",
                                "CORR-GPT-T2A-GRAIN-01"),
        ("QB7_D.html", "q14"): ("correction_corr_cetip_h3b1_20260901_manifest.json",
                                "CORR-CETIP-01"),
        ("QB2_A.html", "q11"): ("correction_corr_gpt_t1_grain_20260904_manifest.json",
                                "CORR-GPT-T1-GRAIN-01"),
        ("QB2_B.html", "q15"): ("correction_corr_gpt_t2a_imsbc_20260905_manifest.json",
                                "CORR-GPT-T2A-IMSBC-01"),
        ("QB4_H.html", "q13"): ("batch_h1_manifest.json", "H1-001"),
        ("QB5_E.html", "q4"): ("batch_h4_manifest.json", "H4-004"),
        ("QB7_D.html", "q15"): ("correction_corr_cetip_h3b1_20260901_manifest.json",
                                "CORR-CETIP-02"),
        ("QB3_C.html", "q7"): ("batch_h3b2_manifest.json", "H3B2-001"),
    }
    bad_chain = []
    for tgt, (mani, act) in want_pred.items():
        sup = declared.get(tgt, (None, {}))[1].get("supersedes") or {}
        if sup.get("manifest") != mani or sup.get("action_id") != act:
            bad_chain.append("%s#%s" % tgt)
    report("supersession_ancestry_declared", not bad_chain,
           "predecessors named: %s" % (bad_chain or "all nine"))

    # ---- live digests, resolved through the chains --------------------
    pages, live_bad = {}, []
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
           "mismatched=%s" % (live_bad or "nine cards, resolved through their chains"))

    # ---- the cards the brief ACCEPTED and this tranche must not move ---
    held_bad = []
    for (rel, anchor), pin in HELD_PINS.items():
        live = card_digests(read_text(REPO / rel)).get(anchor)
        if live != pin:
            held_bad.append("%s#%s live=%s" % (rel.rsplit("/", 1)[-1], anchor,
                                               (live or "-")[:16]))
    report("accepted_and_deferred_cards_unmoved", not held_bad,
           "moved=%s" % (held_bad or "QB2_A#q33 accepted, QB5_C_A#q1 deferred"))

    q5 = pages[("QB5_C_B.html", "q5")]
    q27 = pages[("QB2_A.html", "q27")]
    q14 = pages[("QB7_D.html", "q14")]
    q11 = pages[("QB2_A.html", "q11")]
    q15b = pages[("QB2_B.html", "q15")]
    q13 = pages[("QB4_H.html", "q13")]
    q4 = pages[("QB5_E.html", "q4")]
    q15d = pages[("QB7_D.html", "q15")]
    q7 = pages[("QB3_C.html", "q7")]

    # =============== A. UNSUPPORTED CLAIMS =============================
    omv5 = section(q5, "<h4>On My Vessel</h4>", '<div class="reg-box"')
    report("q5_no_cloud_sync_fleet_claim_survives",
           not re.search(r"cloud[- ]sync|fleet telemetry|remote cloud", flatten(q5), re.I),
           "no automated fleet-wide backup capability asserted anywhere in the card")
    report("q5_no_tribunal_preservation_claim",
           not re.search(r"international maritime tribunal", flatten(q5), re.I),
           "the asserted evidentiary standing is gone with the system that carried it")
    report("q5_omv_preserves_originals_under_master_and_sms",
           all(t in omv5.lower() for t in ("original", "chain of custody", "sms"))
           and re.search(r"alteration|back-dating", omv5, re.I) is not None
           and re.search(r"marine safety investigation Authority", omv5, re.I) is not None,
           "preserve, protect, secure under Master/SMS, release to the Authority")
    report("q5_shore_replication_is_system_specific_not_asserted",
           re.search(r"system-specific", omv5, re.I) is not None
           and re.search(r"never substitutes for|no substitute for", omv5, re.I)
           is not None,
           "replication described, never claimed, never a substitute for originals")
    report("q5_no_new_named_company_system_invented",
           not re.search(r"Maersk[^.]{0,60}(system|platform|portal|telemetry)",
                         omv5, re.I),
           "the removed claim was not swapped for another invented Maersk system")

    # The ISM 9 / MSC.255(84) split is the card's teaching point and the brief
    # required it to survive intact.  Scoped to the reg-box, because the CE tip
    # states it too and either standing in for the other is the block-scope
    # escape the tranche-2A suite found three times.
    regbox5 = section(q5, "Regulatory References", '<div class="ce-tip"')
    report("q5_ism9_msc255_split_intact_in_regbox",
           "MSC.255(84)" in regbox5 and re.search(r"ISM Code\s*.?\s*9", regbox5)
           and "marine safety investigation" in regbox5,
           "both limbs still stated in the reg-box, unchanged by this correction")

    casualty5 = section(q5, "<h4>Casualty Link</h4>", "<h4>Examiner Chain")
    report("q5_no_sole_indian_national_claim",
           not re.search(r"sole Indian|only Indian", flatten(q5), re.I),
           "the unverified nationality proposition is removed, not hedged")
    report("q5_true_confidence_verified_facts_retained",
           "bulk carrier" in casualty5.lower()
           and re.search(r"twenty surviving crew|20 surviving crew", casualty5, re.I)
           and "Indian Navy" in casualty5
           and re.search(r"two Filipino", casualty5, re.I)
           and re.search(r"one Vietnamese", casualty5, re.I),
           "bulk carrier, three fatalities by nationality, twenty evacuated")
    report("q5_training_scenario_warning_survives",
           re.search(r"training scenario", casualty5, re.I) is not None
           and re.search(r"do not cite True Confidence", casualty5, re.I) is not None,
           "the card still warns the question premise is not the real casualty")

    omv27 = section(q27, "On My Vessel</strong>", "</div>")
    report("q27_no_dry_bulk_charter_invention",
           not re.search(r"dry bulk charter|industrial logistics", flatten(q27), re.I),
           "the invented charter scenario is gone")
    report("q27_no_loading_computer_module_requirement",
           not re.search(r"loading computer[^.]{0,120}module", flatten(q27), re.I),
           "no universal approved-IMSBC-and-Grain-module requirement asserted")
    report("q27_omv_admits_the_regime_and_answers_from_the_code",
           re.search(r"not a routine cargo regime", omv27, re.I) is not None
           and "Grain Code" in omv27 and "IMSBC" in omv27,
           "says so directly, then answers from the criteria and the group framework")
    report("q27_grain_criterion_from_t2a_intact",
           "between the heeling arm curve and the righting arm curve" in flatten(q27)
           and "0.075" in flatten(q27) and "A 7.1.2" in flatten(q27),
           "CORR-GPT-T2A-GRAIN's criterion propositions are untouched")

    # ---- the governed correction log ---------------------------------
    # NOT a q-card, so no digest pin in this repo covers it.  It generates into
    # meoclass1/qb_content_index.json, which candidates read.
    log_raw = read_text(GOVERNED_LOG)
    idx_raw = read_text(PUBLISHED_INDEX)
    report("correction_log_note_free_of_barred_claim",
           not re.search(r"sole Indian", log_raw, re.I)
           and not re.search(r"sole Indian", idx_raw, re.I),
           "the governed note AND the generated index are both clean")
    report("correction_log_note_keeps_verified_facts",
           "two Filipino and one Vietnamese" in log_raw
           and re.search(r"twenty surviving crew.{0,60}Indian Navy", log_raw, re.I),
           "the note still carries what the reporting actually supports")
    art = json.dumps(records["onmyvessel"].get("artefacts") or [])
    report("correction_log_declared_as_artefact",
           "qb_content_index_governed.json" in art and "why_no_digest" in art,
           "the un-pinnable file is declared with its reason, not left off the record")

    # =============== B. LNG ASPHYXIATION ================================
    dangers = li_items(q14, "<h4>The dangers")
    joined = " ".join(dangers).lower()
    report("q14_dangers_list_teaches_oxygen_deficiency",
           any("asphyxi" in d.lower() and "oxygen" in d.lower() for d in dangers),
           "%d danger entries, one of them the asphyxiation entry" % len(dangers))
    asph = next((d for d in dangers if "asphyxi" in d.lower()), "")
    report("q14_asphyxiation_tied_to_purge_and_inerting",
           re.search(r"nitrogen", asph, re.I) is not None
           and re.search(r"purg|inert", asph, re.I) is not None
           and re.search(r"vapour", asph, re.I) is not None
           and re.search(r"displac", asph, re.I) is not None,
           "nitrogen from purging/inerting AND the vapour itself, both by displacement")
    report("q14_asphyxiation_states_no_useful_warning",
           re.search(r"no useful warning|without warning", asph, re.I) is not None,
           "the property that makes it lethal is stated, not just the mechanism")
    report("q14_asphyxiation_explains_the_existing_controls",
           all(t in asph.lower() for t in ("gas detection", "upwind"))
           and re.search(r"essential[- ]personnel", asph, re.I) is not None,
           "detection, upwind positioning and essential-personnel control named as why")
    report("q14_asphyxiation_placed_between_rpt_and_rollover",
           len(dangers) >= 3
           and "asphyxi" in dangers[3].lower()
           and dangers[2].lower().startswith("rapid phase transition")
           and dangers[4].lower().startswith("rollover"),
           "position asserted by ORDER, not by presence: RPT -> asphyxiation -> rollover")

    # The negative half.  Over-import is the failure a "did the fix land?"
    # check cannot see, because the fix landed and then kept going.
    q14_flat = flatten(q14).lower()
    imported = [t for t in ("enclosed space", "enclosed-space", "entry permit",
                            "permit to work", "permit-to-work", "confined space",
                            "confined-space", "rescue team", "rescue harness",
                            "stand-by man", "standby man")
                if t in q14_flat]
    report("q14_no_entry_or_confined_space_material_imported", not imported,
           "imported=%s" % (imported or "none - the card involves no entry"))
    report("q14_short_layers_carry_the_hazard",
           re.search(r"oxygen deficiency", block(q14, "15-Second Answer", 1400), re.I)
           and re.search(r"oxygen deficiency", block(q14, "60-Second Answer", 2200), re.I),
           "neither oral short layer omits it")
    report("q14_short_layers_not_bloated",
           len(practice_block(q14, "15-Second Answer").split()) < 130
           and len(practice_block(q14, "60-Second Answer").split()) < 320,
           "one clause each; the layers are still oral-length")
    report("q14_igf_citations_unmoved",
           all(c in flatten(q14) for c in ("18.4.1.1.1", "18.4.1.1.2", "18.4.1.2",
                                           "18.4.3", "18.4.4.1", "18.4.5", "18.4.6",
                                           "8.4.2", "8.4.3")),
           "no IGF paragraph was added, moved or lost while the danger went in")

    # =============== C. GRAIN CONSISTENCY ===============================
    q11_flat = flatten(q11)
    report("q11_heading_no_longer_says_area_on_gz_curve",
           not re.search(r"Residual Area on GZ Curve", q11, re.I),
           "the rejected terminology is gone from the label")
    report("q11_heading_names_both_curves",
           re.search(r"Net Residual Area Between Heeling and Righting-Arm Curves",
                     q11, re.I) is not None,
           "the heading now names the object the clause actually measures")
    report("q11_no_unquoted_area_under_gz_curve_claim",
           not unquoted(q11_flat, r"area under the GZ curve"),
           "the rejected form is never ASSERTED (quoting it to teach against is fine)")
    report("q11_criterion_still_between_the_two_curves",
           "between the heeling arm curve and the righting arm curve" in q11_flat,
           "the already-correct criterion text was not disturbed")
    report("q11_criterion_still_least_of_three",
           all(t in q11_flat for t in ("least of", "maximum difference", "0.075"))
           and re.search(r"angle of flooding", q11_flat, re.I) is not None,
           "all three upper limits survive the heading change")

    # The start point, and -- the load-bearing half -- its provenance.
    report("q11_teaches_the_figure_a7_start_point",
           re.search(r"first intersection", q11_flat, re.I) is not None
           and re.search(r"figure A7", q11_flat, re.I) is not None
           and re.search(r"residual dynamic stability", q11_flat, re.I) is not None,
           "the lower bound is taught, and the figure it comes from is named")
    report("q11_lower_bound_not_quoted_as_clause_text",
           re.search(r"not in the clause at all", q11_flat, re.I) is not None
           and re.search(r"A 7\.1\.2 states only the upper limit", q11_flat, re.I)
           and re.search(r"appears nowhere in the Code", q11_flat, re.I) is not None,
           "the card states the LIMIT of its own evidence, in the card")
    report("q11_matches_q27_wording_for_one_clause",
           "first intersection" in flatten(q27) and "figure A7" in flatten(q27),
           "one clause, one wording across both cards that now teach it")

    # =============== D. IMSBC SOLAS ATTRIBUTION =========================
    s15 = practice_block(q15b, "15-Second Answer")
    s60 = practice_block(q15b, "60-Second Answer")
    report("q15_short_layers_anchor_to_solas_vi",
           "Chapter VI" in s15 and "Chapter VI" in s60,
           "both short layers now name the chapter that makes the Code mandatory")
    report("q15_chapter_vii_scoped_to_part_a1",
           "Part A-1" in s15 and "Part A-1" in s60,
           "chapter VII is kept, and scoped to the subset it governs")
    report("q15_chapter_vii_no_longer_stands_alone",
           not re.search(r"mandatory framework under SOLAS Chapter VII", s15 + s60, re.I)
           and not re.search(r"under SOLAS Chapter VII designed to ensure",
                             s15 + s60, re.I),
           "neither layer makes chapter VII the basis of the whole Code")
    report("q15_dangerous_goods_subset_named",
           re.search(r"dangerous goods in solid form in bulk", s15, re.I) is not None
           and re.search(r"dangerous goods in solid form in bulk", s60, re.I) is not None,
           "what part A-1 actually covers is stated, not implied")
    report("q15_cargo_groups_untouched",
           all(t in s15 for t in ("Group A", "Group B", "Group C"))
           and all(t in s60 for t in ("Group A", "Group B", "Group C"))
           and "Transportable Moisture Limit" in s60,
           "smallest correction: only the opening attribution clause moved")

    # =============== E. EXTERNAL CURRENTNESS ============================
    # K-1 MACN
    report("macn_no_founding_member_status_claim",
           not unquoted(flatten(q4), r"founding MACN member|a founding member of MACN"),
           "the status claim the source does not support is gone")
    macn_omv = section(q4, "<p><strong>Container (Maersk", "</p>")
    macn_tip = practice_block(q4, "CE Oral Tip")
    report("macn_helped_establish_wording_used",
           re.search(r"helped establish MACN in 2011", macn_omv, re.I) is not None
           and re.search(r"helped establish MACN in 2011", macn_tip, re.I)
           is not None,
           "asserted in BOTH blocks that carried the status claim, not one")
    report("macn_membership_figure_still_dated",
           "1 September 2026" in flatten(q4) and "225" in flatten(q4),
           "the number that moves still carries the date it was checked")

    # K-8 BMP
    q13_flat = flatten(q13)
    report("bmp_no_unquoted_2026_edition_claim",
           not unquoted(q13_flat, r"the 2026 edition|current edition is 2026"
                                  r"|current edition 2026|\(2026 ed\.\)"),
           "never asserted; the surviving mentions are quoted and taught against")
    report("bmp_publisher_label_used",
           re.search(r"1st Edition[^.]{0,20}2025", q13_flat, re.I) is not None
           and re.search(r"updated (in|during) 2026", q13_flat, re.I) is not None,
           "1st Edition (2025), updated 2026 - the publisher's own label")
    report("bmp_no_second_edition_invented",
           not re.search(r"2nd Edition|second edition of BMP|BMP MS 2", q13_flat, re.I)
           and re.search(r"no second edition", q13_flat, re.I) is not None,
           "and the card says so, so a future editor does not reintroduce it")
    report("bmp_common_ce_failure_entry_repaired",
           not re.search(r"or the 2025 first edition, as current", q13_flat, re.I),
           "the entry the correction itself falsified was rewritten in the same act")
    bmp_update = practice_block(q13, "What the 2026 update changed")
    report("bmp_2026_update_substance_intact",
           "Actions on Boarding by Activists" in bmp_update
           and "Section 6" in bmp_update
           and re.search(r"razor wire", bmp_update, re.I) is not None,
           "scoped to the block: the phrase also occurs in the trap list")
    report("bmp_first_edition_date_intact",
           "31 March 2025" in q13_flat,
           "the announcement date survives the relabelling")

    # K-6 ISO 23306
    q15d_flat = flatten(q15d)
    report("iso23306_current_published_edition_stated",
           re.search(r"ISO 23306:2020 remains the CURRENT PUBLISHED", q15d_flat)
           is not None
           and re.search(r"September 2026", q15d_flat) is not None,
           "the published edition is named AND dated")
    report("iso23306_edition_2_marked_under_development",
           "ISO/AWI 23306" in q15d_flat
           and re.search(r"UNDER DEVELOPMENT", q15d_flat) is not None
           and "3 August 2026" in q15d_flat,
           "the work item is named, dated, and labelled as a work item")
    report("iso23306_awi_not_stated_as_current_or_mandatory",
           re.search(r"An AWI is a work item, not a published standard", q15d_flat)
           is not None
           and not re.search(r"ISO/AWI 23306[^.]{0,60}(mandatory|in force|required)",
                             q15d_flat, re.I),
           "the two states are stated separately and neither is asserted as the other")
    report("iso23306_no_exhaustive_negative_claim",
           not re.search(r"no later edition|superseding standard", q15d_flat, re.I),
           "the barred exhaustive negative is absent, as it always was")
    report("iso23306_methane_number_position_intact",
           re.search(r"no methane number|no minimum methane number", q15d_flat, re.I)
           is not None,
           "the card's central teaching point is untouched")

    # K-7 MARPOL Annex VI reg. 16
    q7_flat = flatten(q7)
    report("reg16_currency_claim_is_scoped_and_dated",
           re.search(r"as at September 2026", q7_flat) is not None
           and re.search(r"amendment index", q7_flat, re.I) is not None,
           "an undated negative became a dated, scoped one")
    report("reg16_no_exhaustive_never_amended_claim",
           not re.search(r"never been amended|has never been amended", q7_flat, re.I),
           "no exhaustive historical negative anywhere in the card")
    report("reg16_other_amendment_subjects_named",
           re.search(r"emission control area|ECA", q7_flat, re.I) is not None
           and re.search(r"NO", q7_flat) is not None
           and "Technical Code" in q7_flat,
           "what the recent amendments DO concern is stated, so the scope is checkable")
    report("reg16_substantive_propositions_unmoved",
           all(t in q7_flat for t in ("MEPC.328(76)", "19 May 2005", "1 January 2000"))
           and "850" in q7_flat,
           "the six substances, the dates and the temperature floors are untouched")

    # =============== DEVIATIONS AND PREMISE CORRECTIONS =================
    prop_c = json.dumps(records["currency"].get("propagation") or {})
    report("bmp_propagation_reported_not_swept",
           all(t in prop_c for t in ("QB4_H#q2", "QB4_H#q11", "QB4_B#q16",
                                     "QB9_A#q9", "QB9_B#q5"))
           and "REPORTED" in prop_c
           and "QB4_H#q2" in auth_text and "QB4_B#q16" in auth_text,
           "six live sites outside q13 are named in the record AND in the report")
    report("bmp_source_registry_left_and_said_so",
           "SRC-BMPMS-2026" in prop_c and "SRC-BMPMS-2026" in q13_flat,
           "the registry id is left alone and the card explains why it says 2026")
    report("k4_source_custody_gap_reported",
           "MSC.551(108)" in auth_text and "NOT held" in auth_text
           and "source-custody" in auth_text,
           "the two IGF amendments the card claims to have read are not in the tree")
    report("k4_k5_k9_adjudicated_without_edit",
           "ADJUDICATED" in auth_text
           and re.search(r"K-9 .{0,60}PFOS.{0,40}NO CHANGE", auth_text, re.S) is not None
           and "QB2_F#q3" in json.dumps(records["currency"].get("invariants") or []),
           "three findings closed by verification, not by editing")
    report("brief_premise_corrections_recorded",
           auth_text.count("Premise correction") >= 2
           and "does not say \"exactly five items\"" in auth_text,
           "three premises the tree did not bear out are corrected on the record")
    report("deferred_items_recorded_with_reasons",
           "Herschberg" in auth_text and "DEFERRED" in auth_text
           and "17 empty 15-second layers" in auth_text,
           "the typo and the empty layers are carried, not silently dropped")

    # =============== CORPUS AND SURFACE INVARIANTS ======================
    idx = json.loads(idx_raw)
    report("corpus_totals_unmoved",
           idx.get("total_questions") == 761 and idx.get("total_files") == 86,
           "%s / %s" % (idx.get("total_questions"), idx.get("total_files")))
    hub = read_text(REPO / "meoclass1/index.html")
    report("hub_date_not_advanced",
           'id="stat-updated">2 Sep 2026<' in hub,
           "the hub still reads 2 Sep 2026, on the brief's instruction")
    report("content_index_effects_declared",
           all(r.get("content_index_effect") for r in records.values())
           and "IS regenerated" in (records["onmyvessel"]["content_index_effect"]),
           "the one record that DOES move the index says so")

    print("\n%d checks, %d FAIL%s"
          % (CHECKS, len(FAILS), (" -> %s" % FAILS) if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
