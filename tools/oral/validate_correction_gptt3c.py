#!/usr/bin/env python3
"""Content gates for GPT high-risk content review, Tranche 3C.

WHY THIS EXISTS
---------------
`validate_corrections.py` pins each corrected card's post-correction digest and
asks "are these bytes the ones we authorised?".  It cannot ask "is what we
authorised actually correct?", because a pin is perfectly happy with wrong text.

Tranche 3C turns on regulatory PROPOSITIONS that a later well-meaning edit could
quietly drop:

  * CII is measured per CAPACITY-nautical-mile, and the capacity measure is
    SHIP-TYPE SPECIFIC.  Restoring "gCO2/DWT.nm" anywhere as a positive teaching
    statement re-breaks it for every ro-ro and cruise passenger ship.
  * MARPOL Annex I reg. 34.1.5 has TWO limbs split on 31 December 1979.  Dropping
    either limb, or blurring the date, restores a defect that was wrong by a
    factor of two for every pre-1980 tanker.
  * QB2_A#q31 must not claim bulk-carrier experience the Founder cannot ground,
    and must not restore five casualty facts that were wrong or unverifiable.
  * Three IACS Unified Requirements must stay HELD and hash-pinned, or the
    Z-series corrections revert to resting on evidence nobody can re-derive.

TWO RULES THIS FILE OBEYS
-------------------------
1. **No check may be satisfied by the digest pin.**  Any edit trips the pin, so
   accepting it as the catch would prove only that the pin works while these
   substantive checks rot as dead code.  Nothing here reads a digest of a card.
2. **A correction quotes the wording it rejects**, so a flat banned-phrase grep
   fails on the very sentences carrying the fix.  Every negative check below
   asserts that a rejected phrase is QUOTED OR NEGATED, never that it is absent.

FAILS CLOSED.  If a held instrument or the registry cannot be read, that is
reported and the exit code is non-zero -- never skipped.

DIALECT
-------
Prints "<N> checks, <M> FAIL", the repo's standard batch-validator summary, so
`run_oral_release.py` classifies it with the shared validator parser.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_batch_b import CARD_OPEN, _balanced_end                # noqa: E402

REPO = Path(__file__).resolve().parents[2]
QB = REPO / "meoclass1"
SOURCES = REPO / "docs" / "sources"
REGISTRY = SOURCES / "MIW_SOURCE_REGISTRY.json"
CUSTODY = SOURCES / "T3C_IACS_CUSTODY_REPAIR.json"

CHECKS: list[tuple[str, bool, str]] = []


def report(name: str, ok: bool, detail: str = "") -> None:
    CHECKS.append((name, bool(ok), detail))


def page(name: str) -> str:
    """LF-normalised, entity-unescaped page text.

    Unescaped because a guard spelled `h&m` is blind to `h&amp;m`, and the same
    is true of every `&le;`, `&ndash;` and `&rsquo;` in these pages.  Checks that
    need raw markup use `raw()` instead.
    """
    return html.unescape(raw(name))


def raw(name: str) -> str:
    return (QB / name).read_text(encoding="utf-8", newline="").replace("\r\n", "\n")


def card(name: str, anchor: str) -> str:
    text = raw(name)
    for m in CARD_OPEN.finditer(text):
        got = re.search(r'\bid="([^"]+)"', m.group(0))
        if got and got.group(1) == anchor:
            return html.unescape(text[m.start():_balanced_end(text, m.start())])
    raise AssertionError("card %s#%s not found" % (name, anchor))


def negated_or_quoted(block: str, phrase: str, window: int = 420) -> bool:
    """True if EVERY occurrence of `phrase` sits inside a rejection.

    The window is deliberately wide: the tightest real case in this corpus put
    the denial behind two full quoted phrases.
    """
    markers = ("wrong", "not ", "no,", "never", "trap", "reject", "instead of",
               "rather than", "is not", "always", "&ldquo;", "“", "myth")
    for m in re.finditer(re.escape(phrase), block, re.I):
        lo = max(0, m.start() - window)
        near = block[lo:m.end() + window].lower()
        if not any(k in near for k in markers):
            return False
    return True


def sha256_of(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def pdf_text(path: Path) -> str | None:
    try:
        import fitz
    except ImportError:
        return None
    try:
        doc = fitz.open(path)
    except Exception:
        return None
    return re.sub(r"\s+", " ", " ".join(p.get_text() for p in doc))


# =====================================================================
# FAMILY A -- CII capacity / unit, and the F-1 provenance deletion
# =====================================================================
DWT_CATEGORIES = ("bulk carriers", "tankers", "container ships", "gas carriers",
                  "LNG carriers", "general cargo ships", "combination carriers")
GT_CATEGORIES = ("cruise passenger ships", "ro-ro cargo ships", "ro-ro passenger ships")


def family_a() -> None:
    q1 = card("QB6.html", "q1")
    q10 = card("QB7_I.html", "q10")

    # --- the headline proposition -------------------------------------------
    report("cii_q1_teaches_capacity_not_dwt_unit",
           "gCO₂ per capacity" in q1 or "capacity-nautical-mile" in q1,
           "capacity form present in QB6#q1")

    # RULE 2: the card QUOTES the form it rejects, in its new trap.  Assert the
    # rejected form is always rejected -- never that it is absent.
    report("cii_q1_no_surviving_universal_dwt_unit",
           negated_or_quoted(q1, "gCO₂/DWT·nm")
           and negated_or_quoted(q1, "gCO₂ per DWT·nm"),
           "every DWT-unit mention in QB6#q1 is quoted or negated")

    report("cii_q1_ship_type_split_survives",
           all(c in q1 for c in DWT_CATEGORIES) and all(c in q1 for c in GT_CATEGORIES),
           "both capacity lists present in full")

    # PRESENCE IS NOT BINDING.  Mutation A2 blurred the GT limb in the
    # 60-second layer to "gross tonnage for certain ship types" and this gate
    # stayed green, because "cruise passenger ships" still appeared in three
    # OTHER layers.  A card can therefore lose the split in the layer a
    # candidate actually recites while a presence check reports success.  The
    # proposition is that wherever the DWT categories are listed, the GT
    # categories are listed with them.
    unbound = []
    for m in re.finditer(r"bulk carriers, tankers, container ships", q1):
        if "cruise passenger ships" not in q1[m.start():m.start() + 500]:
            unbound.append(m.start())
    report("cii_q1_every_dwt_list_is_paired_with_its_gt_list", not unbound,
           "DWT category lists with no GT list within 500 chars: %s"
           % (unbound or "none"))

    report("cii_q1_gt_limb_is_positive_teaching",
           re.search(r"GT[^.]{0,120}(ro-ro|cruise)", q1, re.I) is not None
           or re.search(r"(ro-ro|cruise)[^.]{0,160}GT\b", q1) is not None,
           "GT is taught against the ro-ro / cruise categories, not merely mentioned")

    # --- every layer, not just the deep ones --------------------------------
    layers = {
        "15s": re.search(r'tier tier-15.*?</div>\s*<div class="tier tier-60', q1, re.S),
        "60s": re.search(r'tier tier-60.*?</div>\s*<h4>Formula', q1, re.S),
        "formula": re.search(r'class="formula".*?</p>', q1, re.S),
        "ce_tip": re.search(r'class="ce-tip".*?</div>', q1, re.S),
    }
    missing = [k for k, m in layers.items()
               if not m or "capacity" not in m.group(0).lower()]
    report("cii_q1_capacity_reaches_every_short_layer", not missing,
           "layers lacking the capacity form: %s" % (missing or "none"))

    # The formula block needed its own check.  Mutation A3 reverted the
    # formula's UNIT to gCO2/DWT.nm while its explanatory sentence beneath still
    # said "capacity", so a "does this layer mention capacity?" test passed on a
    # layer whose headline expression was wrong.  The quantity is what a
    # candidate copies onto the board.
    report("cii_q1_formula_expresses_the_capacity_quantity",
           "Attained CII (gCO₂ per capacity·nm)" in q1
           and re.search(r"=\s*Σ\(M_fuel × Cf\)\s*/\s*\(C × D", q1) is not None,
           "the formula's own unit and denominator are the capacity form")

    # --- F-3 : the outlier that started one layer behind its own body -------
    report("cii_q10_short_layer_aligned_with_its_body",
           "capacity" in q10.lower() and "DWT-mile" not in q10,
           "QB7_I#q10 15-second layer no longer says per DWT-mile")
    report("cii_q10_body_still_says_capacity_times_distance",
           "capacity" in q10.lower() and re.search(r"capacity\s*(times|×|x)\s*distance",
                                                   q10, re.I) is not None,
           "the body limb this correction aligned TO is still present")

    # --- F-1 : provenance, not accuracy -------------------------------------
    report("f1_no_triple_e_engine_specification",
           "11G90ME" not in q1 and "35,000 kW" not in q1,
           "the MAN B&W 11G90ME-C / 35,000 kW MCR claim is gone from QB6#q1")
    report("f1_no_substitute_vessel_specification",
           not re.search(r"(MAN B&W|Wärtsilä|Sulzer)[^<]{0,60}(MCR|kW)", q1),
           "no replacement engine specification was substituted")
    report("f1_triple_e_dwt_duplicate_removed",
           "165,000" not in q1,
           "the same Triple-E specification in the CE-relevance worked example is gone")
    report("f1_worked_example_arithmetic_survives",
           "3.114" in q1 and "249" in q1,
           "deleting the specification did not cost the card its arithmetic")

    # --- currentness --------------------------------------------------------
    report("cii_q1_cites_current_g1_chain",
           "MEPC.412(84)" in q1 and "MEPC.352(78)" in q1,
           "both the G1 guidelines and the 2026 amendment are cited")
    report("cii_q1_states_g1_adoption_date",
           "1 May 2026" in q1, "MEPC.412(84) adoption date stated")


# =====================================================================
# FAMILY B -- MARPOL Annex I reg. 34.1.5, both limbs, all seven sites
# =====================================================================
def family_b() -> None:
    text = page("QB3_F.html")
    q3, q11 = card("QB3_F.html", "q3"), card("QB3_F.html", "q11")

    # RULE 2 in action.  The corrected body bullet QUOTES the form it rejects
    # -- "quoting 1/30,000 alone is wrong for every pre-1980 tanker" -- so a
    # flat count of "1/30,000" returns EIGHT where there are SEVEN teaching
    # sites.  Counting the rejection as a defect is precisely the failure mode
    # that makes a naive banned-phrase grep unusable on a correction.  The
    # exclusion is deliberately narrow and literal, not a wide sentiment
    # window: a wide window would also swallow the legitimate limb 200
    # characters above it, and the gate would go quietly vacuous.
    REJECTED = r"1/30,000 alone is wrong"
    positives = [m for m in re.finditer(r"1/30,000", text)
                 if not re.match(REJECTED, text[m.start():m.start() + len(REJECTED)])]
    hi = len(positives)
    lo = len(re.findall(r"1/15,000", text))
    report("reg34_rejected_form_is_quoted_not_taught",
           len(re.findall(REJECTED, text)) == 1,
           "the card states the error it corrects, exactly once")
    report("reg34_seven_sites_still_seven", hi == 7,
           "positive teaching occurrences of 1/30,000=%d (expected 7)" % hi)
    report("reg34_every_site_carries_both_limbs", hi == lo and lo > 0,
           "1/30,000 taught=%d  1/15,000 taught=%d" % (hi, lo))

    # Pairing, not counting: equal totals could still be seven of one in one
    # block and seven of the other elsewhere.  Require the limbs to be adjacent.
    unpaired = []
    for m in positives:
        near = text[max(0, m.start() - 700):m.end() + 700]
        if "1/15,000" not in near:
            unpaired.append(m.start())
    report("reg34_limbs_are_adjacent_not_merely_equal", not unpaired,
           "1/30,000 sites with no 1/15,000 within 700 chars: %s" % (unpaired or "none"))

    # The boundary date, in every form the pages use.
    boundary = re.findall(r"31 Dec(?:ember)? 1979", text)
    report("reg34_boundary_date_exact", len(boundary) >= hi,
           "'31 December 1979' occurrences=%d for %d limb pairs" % (len(boundary), hi))
    # Counting boundary dates is not the same as binding them.  Mutation B2
    # rewrote three "on or before 31 Dec 1979" to "before 1980" -- which moves
    # every tanker delivered ON 31 December 1979 into the wrong limb -- and the
    # count stayed above the threshold because the "after 31 Dec 1979" halves
    # were untouched.  Each limb must be bound to its OWN side of the boundary.
    lo_unbound = [m.start() for m in re.finditer(r"1/15,000", text)
                  if not re.search(r"on or before\s*<?/?\w*>?\s*31 Dec",
                                   text[max(0, m.start() - 260):m.end() + 260], re.I)]
    # The upper limb may name the date itself OR refer back to it in the same
    # sentence ("...on or before 31 December 1979, 1/30,000 for one delivered
    # AFTER THAT DATE").  That back-reference is exact and unambiguous, which is
    # the brief's actual requirement, so a gate that demanded the literal date
    # twice would have failed two CORRECT compact forms and pushed the card
    # towards clumsier wording to satisfy the guard.  The anti-blur protection
    # lives in the lower-limb check above, which is what mutation B2 attacks.
    def upper_limb_bound(window: str) -> bool:
        if re.search(r"after\s*<?/?\w*>?\s*(31 Dec|that date)", window, re.I):
            return True
        # Compact grid form: "...1/15,000 ... on or before 31 Dec 1979;
        # 1/30,000 if delivered after".  The bare "after" is bound by the
        # boundary stated in the same clause.  Accepting it still fails under
        # mutation B2, which rewrites that boundary to "before 1980".
        return bool(re.search(r"delivered after", window, re.I)
                    and re.search(r"on or before\s*<?/?\w*>?\s*31 Dec", window, re.I))

    hi_unbound = [m.start() for m in positives
                  if not upper_limb_bound(text[max(0, m.start() - 320):m.end() + 320])]
    report("reg34_lower_limb_bound_to_on_or_before_31_dec_1979", not lo_unbound,
           "1/15,000 sites not bound to 'on or before 31 Dec 1979': %s"
           % (lo_unbound or "none"))
    report("reg34_upper_limb_bound_to_after_31_dec_1979", not hi_unbound,
           "1/30,000 sites not bound to 'after 31 Dec 1979': %s"
           % (hi_unbound or "none"))

    report("reg34_boundary_is_two_sided",
           re.search(r"on or before\s*<?/?\w*>?\s*31 Dec", text, re.I) is not None
           and re.search(r"after\s*<?/?\w*>?\s*31 Dec", text, re.I) is not None,
           "both 'on or before' and 'after' limbs present")

    for label, block in (("q3", q3), ("q11", q11)):
        h = len([m for m in re.finditer(r"1/30,000", block)
                 if not re.match(REJECTED, block[m.start():m.start() + len(REJECTED)])])
        l = len(re.findall(r"1/15,000", block))
        report("reg34_%s_no_one_number_universal" % label, h == l and h > 0,
               "%s: 1/30,000=%d 1/15,000=%d" % (label, h, l))

    # The seventh site is OUTSIDE every q-card, so no card digest can reach it.
    # This is the only thing asserting it.
    grid = re.search(r"Annex I Reg 34 Cargo Discharge.{0,600}", text, re.S)
    report("reg34_page_level_rapid_recall_limb_present",
           grid is not None and "1/15,000" in grid.group(0) and "1/30,000" in grid.group(0),
           "the page-level Rapid Recall grid teaches both limbs")
    in_cards = sum(len([m for m in re.finditer(r"1/30,000", b)
                        if not re.match(REJECTED, b[m.start():m.start() + len(REJECTED)])])
                   for b in (q3, q11))
    report("reg34_seventh_site_is_outside_the_cards", in_cards == hi - 1,
           "in-card sites=%d of %d, so exactly one is page-level" % (in_cards, hi))

    # The criteria the brief said NOT to touch.
    # These must check the BODY LIST bullet, not any mention of the number.
    # Mutation B4 changed the body bullet from 50 to 12 nautical miles and a
    # "does q3 say 50 NM anywhere?" test stayed green on the 15-second answer
    # and the Key Numbers block -- a candidate reading the conditions list would
    # have had the wrong distance while the guard reported success.
    plain = re.sub(r"<[^>]+>", "", q3)      # tags stripped: the bullet is
    plain = re.sub(r"\s+", " ", plain)       # "More than <strong>50 ...</strong>"
    report("reg34_body_list_distance_limb_exact",
           "More than 50 nautical miles from nearest land" in plain,
           "the conditions-list bullet still states 50 nautical miles")
    report("reg34_body_list_rate_limb_exact",
           "Instantaneous rate ≤ 30 litres per nautical mile" in plain,
           "the conditions-list bullet still states 30 litres per nautical mile")

    for name, pat in (("50 nautical miles", r"50\s*(NM|nautical mile)"),
                      ("30 litres per nautical mile", r"30\s*(L/NM|litres per nautical mile)"),
                      ("special area", r"[Ss]pecial [Aa]rea"),
                      ("en route", r"[Ee]n route"),
                      ("ODME/ODMCS", r"ODM[EC]S?")):
        report("reg34_untouched_criterion_%s" % re.sub(r"\W+", "_", name).strip("_"),
               re.search(pat, q3) is not None, "%s still taught in q3" % name)

    report("reg34_corpus_wide_no_other_file_teaches_the_fraction",
           not [p for p in sorted(QB.glob("QB*.html"))
                if p.name != "QB3_F.html" and "1/30,000" in p.read_text(
                    encoding="utf-8", errors="replace")],
           "no file outside QB3_F states the reg.34 total-quantity fraction")


# =====================================================================
# FAMILY C -- QB2_A#q31 provenance, casualty facts, source confidence
# =====================================================================
REMOVED_CASUALTY_FACTS = {
    "cargo tonnage 72,100": "72,100",
    "beam 32.26 m": "32.26",
    "rescue by a passing tanker": "passing tanker",
    "distance range 230 to 240": "230 to 240",
    "distance range 230-240": "230–240",
}


def family_c() -> None:
    q31 = card("QB2_A.html", "q31")

    # --- F-5 : provenance ----------------------------------------------------
    vessel = re.search(r"On My Vessel.*?</div>", q31, re.S)
    report("f5_on_my_vessel_block_located", vessel is not None, "block found")
    blk = vessel.group(0) if vessel else ""
    report("f5_no_personal_fine_ore_routine",
           "fine ore or concentrate loading" not in q31
           and not re.search(r"\bI confirm with the Chief Officer\b", q31),
           "the personal fine-ore pre-loading routine is gone")
    report("f5_states_the_experience_boundary",
           "container-vessel experience" in blk or "container vessel" in blk,
           "the block says plainly this is not the candidate's cargo operation")
    report("f5_still_answers_from_requirements",
           "IMSBC" in blk and ("declaration" in blk or "certificate" in blk),
           "it answers from the applicable requirements rather than refusing")
    report("f5_keeps_the_engineering_content",
           "emergency generator" in blk and "emergency fire pump" in blk,
           "the engineering half, which was never a bulk-carrier claim, is kept")

    # --- casualty facts ------------------------------------------------------
    for label, phrase in REMOVED_CASUALTY_FACTS.items():
        report("q31_removed_%s" % re.sub(r"\W+", "_", label).strip("_"),
               phrase not in q31, "'%s' absent" % phrase)

    for label, phrase in (("imo_number", "9145530"),
                          ("reported_cargo_tonnage", "71,200"),
                          ("deadweight", "72,900"),
                          ("disputed_distance_upper_limb", "290"),
                          ("rescuing_vessel", "Varad")):
        report("q31_verified_fact_%s" % label, phrase in q31, "'%s' present" % phrase)

    report("q31_cargo_tonnage_labelled_as_reported",
           re.search(r"reported[^.]{0,40}71,200|71,200[^.]{0,60}reported", q31, re.I)
           is not None,
           "the cargo figure is presented as reported, not certificated")
    report("q31_distance_presented_as_disputed",
           re.search(r"(differ|disputed|range)", q31, re.I) is not None
           and "230" in q31 and "290" in q31,
           "the real spread is given and flagged as disputed")
    report("q31_high_seas_conclusion_survives_the_dispute",
           re.search(r"(beyond the|200-mile)[^.]{0,60}EEZ", q31, re.I) is not None,
           "the legal conclusion is stated as unaffected by the distance dispute")
    report("q31_cause_still_undetermined",
           re.search(r"(cause has not been determined|NO cause determined|"
                     r"cause is undetermined)", q31, re.I) is not None,
           "the card still refuses to state a cause")
    report("q31_liquefaction_still_a_hypothesis",
           re.search(r"hypothesis", q31, re.I) is not None,
           "liquefaction is still labelled a hypothesis")

    # The WORD is not the PROPOSITION.  Mutation C5 rewrote the body's
    # "but it is a hypothesis" to "but it is now established" -- converting an
    # open casualty into a finding, which is the single judgement this card
    # exists to teach -- and the word-level check stayed green on three other
    # sentences that still contained "hypothesis".
    report("q31_body_refuses_to_convert_hypothesis_into_finding",
           "but it is a hypothesis" in q31
           and not re.search(r"(is now established|has been established|"
                             r"the cause was liquefaction)", q31, re.I),
           "the body still says the leading hypothesis is only a hypothesis")
    report("q31_no_positive_cause_assertion",
           not re.search(r"(the cargo liquefied\.|liquefaction caused|"
                         r"was caused by liquefaction)", q31, re.I),
           "no sentence asserts liquefaction as the cause")

    # --- source-confidence block --------------------------------------------
    report("q31_source_confidence_block_exists",
           "Source confidence" in q31, "the block this card alone lacked is present")
    scb = re.search(r"Source confidence.*?</div>", q31, re.S)
    body = scb.group(0) if scb else ""
    report("q31_scb_states_no_primary_casualty_source",
           "no published flag-State" in body or "NO primary casualty source" in body.upper()
           or "has published nothing" in body,
           "it says in terms that no investigation source exists")
    report("q31_scb_separates_regulatory_from_casualty",
           "Regulatory limbs" in body and "Casualty facts" in body,
           "high-confidence regulatory limbs kept distinct from reported facts")
    report("q31_scb_lists_what_is_not_claimed",
           "not claimed" in body.lower() or "Deliberately not claimed" in body,
           "the block enumerates what the card refuses to assert")
    report("q31_scb_carries_a_currentness_date",
           "5 September 2026" in body, "the block is dated")
    report("q31_scb_makes_no_read_claim_for_an_unread_source",
           "read in full" not in body and "chapter" not in body.lower(),
           "no claim that a casualty document was opened, and no chapter structure asserted")

    # --- the governance ruling: a registered source must exist ---------------
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    rows = {s["source_id"]: s for s in reg["sources"]}
    row = rows.get("SRC-CASUALTY-OCEANWINNER-2026")
    report("q31_named_casualty_source_registered", row is not None,
           "SRC-CASUALTY-OCEANWINNER-2026 present")
    if row:
        report("q31_casualty_row_declares_no_primary_source",
               row.get("access_status") == "NO_PRIMARY_SOURCE_EXISTS_YET",
               "access_status=%s" % row.get("access_status"))
        report("q31_casualty_row_records_the_corrected_facts",
               any("72,100" in c for c in row.get("claims_NOT_established", []))
               and any("230 to 240" in c or "230-240" in c
                       for c in row.get("claims_NOT_established", [])),
               "the row records what the card used to say and why it was wrong")
        report("q31_casualty_row_points_back_at_the_card",
               "meoclass1/QB2_A.html#q31" in (row.get("used_by") or []),
               "used_by names the card")


# =====================================================================
# FAMILY D -- IACS source custody, and Z20 paragraph-level verification
# =====================================================================
IACS_ROWS = {
    "SRC-IACS-URZ7-REV29-CORR1": ("IACS-UR-Z7-Rev29-Corr1.pdf", "Rev.29 Corr.1",
                                  "Hull Classification Surveys"),
    "SRC-IACS-URZ18-REV9": ("IACS-UR-Z18-Rev9.pdf", "Rev.9", "Survey of Machinery"),
    "SRC-IACS-URZ20-REV2": ("IACS-UR-Z20-Rev2.pdf", "Rev.2",
                            "Planned Maintenance Scheme"),
}

# (paragraph, a phrase that must be in the HELD UR, a phrase that must be in the CARD)
Z20_CLAIMS = [
    ("1.1.1", "alternative to the Continuous Machinery Survey", "alternative to CMS"),
    ("1.1.3", "limited to components and systems covered by CMS",
     "limited to components and systems covered by CMS"),
    ("1.1.4", "surveyed and credited in the usual way", "surveyed and credited in the usual way"),
    ("1.2.1", "intervals for PMS shall not exceed those specified for CMS",
     "shall not exceed those specified for CMS"),
    ("1.3.1", "chief engineer shall be the responsible person on board in charge of the PMS",
     "chief engineer shall be the responsible person on board in charge of the PMS"),
    ("1.3.2", "reported and signed by the chief engineer", "reported and signed by the chief engineer"),
    ("1.3.3", "only be permitted by the chief engineer", "only be permitted by the chief engineer"),
    ("2.1.1", "programmed and maintained by a computerized system",
     "programmed and maintained by a computerised system"),
    ("2.3.1", "Certificate of Approval for Planned Maintenance Scheme",
     "Certificate of Approval for Planned Maintenance Scheme"),
    ("2.3.1", "certification is to be kept on board", "certification is to be kept on board"),
    ("2.3.3", "annual report covering the year", "annual report"),
    ("2.3.5", "agreed intervals between overhauls are exceeded",
     "agreed intervals between overhauls are exceeded"),
    ("2.3.6", "sale or change of management", "change of management"),
    ("3.1.1", "within one year from the date of approval", "within one year"),
    ("3.2.1", "preferably concurrently with the annual survey of machinery",
     "preferably concurrently with the annual machinery survey"),
]


def family_d() -> None:
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    rows = {s["source_id"]: s for s in reg["sources"]}

    for sid, (fname, revision, title_frag) in IACS_ROWS.items():
        row = rows.get(sid)
        report("iacs_row_%s_registered" % sid.split("-")[-1], row is not None, sid)
        if not row:
            continue
        held = SOURCES / fname
        digest = sha256_of(held)
        report("iacs_%s_bytes_held" % sid.split("-")[-1], digest is not None,
               "%s %s" % (fname, "held" if digest else "MISSING"))
        report("iacs_%s_hash_matches_registry" % sid.split("-")[-1],
               digest is not None and digest == row.get("sha256"),
               "registry=%s..." % str(row.get("sha256"))[:12])
        report("iacs_%s_revision_metadata_present" % sid.split("-")[-1],
               row.get("revision") == revision and bool(row.get("revision_date")),
               "revision=%s date=%s" % (row.get("revision"), row.get("revision_date")))
        report("iacs_%s_currentness_verified" % sid.split("-")[-1],
               row.get("currentness") == "CURRENT_VERIFIED",
               "currentness=%s" % row.get("currentness"))
        report("iacs_%s_title_correct" % sid.split("-")[-1],
               title_frag.lower() in str(row.get("title", "")).lower(),
               "title carries '%s'" % title_frag)

    report("iacs_custody_record_exists", CUSTODY.exists(), str(CUSTODY.name))
    if CUSTODY.exists():
        rec = json.loads(CUSTODY.read_text(encoding="utf-8"))
        report("iacs_custody_record_is_not_a_correction_manifest",
               rec.get("kind") == "SOURCE_CUSTODY_REPAIR",
               "kind=%s -- it changes no candidate byte, so it pins no card"
               % rec.get("kind"))
        report("iacs_custody_record_names_all_three",
               {i["registry_row"] for i in rec.get("instruments_acquired", [])}
               == set(IACS_ROWS),
               "all three instruments recorded")

    # ---- Z20 paragraph-level content verification --------------------------
    # FAILS CLOSED: if the held instrument cannot be read, that is a FAIL, not
    # a skip.  A guard that cannot run has silently expired.
    z20 = pdf_text(SOURCES / "IACS-UR-Z20-Rev2.pdf")
    if z20 is None:
        report("z20_source_readable", False,
               "UNAVAILABLE -- held UR Z20 could not be read; paragraph verification "
               "cannot run and is reported as FAIL, never skipped")
    else:
        report("z20_source_readable", True, "%d chars extracted" % len(z20))
        q23 = re.sub(r"\s+", " ", card("QB1_F.html", "q23"))
        bad_src, bad_card = [], []
        for para, in_ur, in_card in Z20_CLAIMS:
            if in_ur.lower() not in z20.lower():
                bad_src.append(para)
            if in_card.lower() not in q23.lower():
                bad_card.append(para)
        report("z20_every_cited_paragraph_is_in_the_held_source", not bad_src,
               "paragraphs not located in UR Z20 Rev.2: %s" % (bad_src or "none"))
        report("z20_every_cited_paragraph_is_still_in_the_card", not bad_card,
               "paragraphs no longer taught by QB1_F#q23: %s" % (bad_card or "none"))
        report("z20_card_states_the_current_revision",
               "Rev.2" in q23 and "2019" in q23,
               "the card names the revision it was verified against")
        report("z20_card_still_separates_class_from_statutory",
               re.search(r"no statutory or IMO PMS certificate", q23, re.I) is not None,
               "the card's central point is intact")

    # ---- the two corrections whose evidence this pass repaired -------------
    z18 = pdf_text(SOURCES / "IACS-UR-Z18-Rev9.pdf")
    if z18 is None:
        report("z18_source_readable", False, "UNAVAILABLE -- reported, never skipped")
    else:
        report("z18_source_readable", True, "%d chars extracted" % len(z18))
        report("z18_boiler_section_is_separate_from_cms",
               "Survey of Steam Boilers" in z18 and "not to exceed 36 months" in z18,
               "CORR-CSM-BOILER-SURVEY-20260823's relied-on propositions hold in Rev.9")
        report("z18_continuous_survey_five_year_interval",
               "not to exceed five (5) years" in z18,
               "the 5-year CMS interval the boiler correction contrasted with")
        report("z18_pms_and_cbm_sections_as_cited",
               "Planned Maintenance Scheme" in z18 and "Condition Based Maintenance" in z18,
               "CORR-URZ7-20260901's relied-on section list holds in Rev.9")

    z7 = pdf_text(SOURCES / "IACS-UR-Z7-Rev29-Corr1.pdf")
    if z7 is None:
        report("z7_source_readable", False, "UNAVAILABLE -- reported, never skipped")
    else:
        report("z7_source_readable", True, "%d chars extracted" % len(z7))
        report("z7_is_hull_not_machinery",
               "Hull Classification Surveys" in z7
               and "Planned Maintenance" not in z7,
               "Z7 carries no machinery content, which is what CORR-URZ7-20260901 turned on")

    # ---- CII source custody (family A's currentness limb) ------------------
    g1 = rows.get("SRC-IMO-MEPC412-84-CII-G1")
    report("cii_g1_source_registered", g1 is not None, "SRC-IMO-MEPC412-84-CII-G1")
    if g1:
        d = sha256_of(SOURCES / "MEPC.412-84.pdf")
        report("cii_g1_bytes_held_and_hash_matches",
               d is not None and d == g1.get("sha256"),
               "held=%s registry=%s..." % (bool(d), str(g1.get("sha256"))[:12]))
        report("cii_g1_currentness_verified",
               g1.get("currentness") == "CURRENT_VERIFIED"
               and g1.get("checked_on") == "2026-09-05",
               "currentness=%s checked_on=%s" % (g1.get("currentness"), g1.get("checked_on")))
        report("cii_g1_revalidation_trigger_set",
               g1.get("revalidation_trigger") == "ON_RELEVANT_MEPC_SESSION",
               "trigger=%s" % g1.get("revalidation_trigger"))
        claims = " ".join(g1.get("verified_claims", []))
        report("cii_g1_row_records_both_capacity_lists",
               "deadweight tonnage (DWT) is used" in claims.lower()
               or "DWT) is used" in claims,
               "the DWT limb is recorded as a verified claim")
        report("cii_g1_row_records_the_gt_limb",
               "gross tonnage (gt) is used" in claims.lower(),
               "the GT limb is recorded as a verified claim")

    g1src = pdf_text(SOURCES / "MEPC.412-84.pdf")
    if g1src is None:
        report("cii_g1_source_readable", False, "UNAVAILABLE -- reported, never skipped")
    else:
        report("cii_g1_source_readable", True, "%d chars extracted" % len(g1src))
        report("cii_g1_source_carries_the_gt_categories",
               "ro-ro passenger ships, gross tonnage" in g1src
               or ("gross tonnage (GT)" in g1src and "ro-ro passenger ships" in g1src),
               "the held resolution actually says what the card teaches")
        report("cii_g1_source_carries_the_dwt_categories",
               "deadweight tonnage (DWT)" in g1src and "combination" in g1src,
               "the DWT category list is in the held resolution")


def main() -> int:
    for fn in (family_a, family_b, family_c, family_d):
        try:
            fn()
        except Exception as exc:                                   # fail closed
            report("%s_ran" % fn.__name__, False,
                   "%s: %s" % (type(exc).__name__, exc))

    width = max(len(n) for n, _, _ in CHECKS)
    for name, ok, detail in CHECKS:
        print("%s %-*s %s" % ("PASS" if ok else "FAIL", width, name, detail))
    failed = sum(1 for _, ok, _ in CHECKS if not ok)
    print("\nGPT Tranche 3C content gates: %d checks, %d FAIL" % (len(CHECKS), failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
