#!/usr/bin/env python3
"""Content gate for CORR-INDIA-OILSPILL-REGULATORY-AUDIT-20260917.

Four propositions, each checked as a PROPOSITION rather than a banned string,
because the corrected text itself quotes what it rejects (SKILL.md 8.2a):

  A_TIER  NOSDCP tiers are graded by response CAPABILITY. The fixed bands
          <700 / 700-10,000 / >10,000 t are unsupported and may not be TAUGHT
          as tier definitions. A sentence may still NAME a band to reject it.
  B_OPRC  India ACCEDED to OPRC 1990 on 17 November 1997, in force for India
          17 February 1998. 1993 is NOSDCP's approval, never India's OPRC date.
  C_BUNK  India is NOT a Party to the Bunkers Convention 2001. Its bunker-oil
          liability rests on the Merchant Shipping Act, 2025, Part IX Ch IV as
          domestic law. Neither half may be dropped.
  D_PANS  India's Pre-Arrival Notification of Security is due AT LEAST 96
          hours before arrival, or within 2 hours of departure when the voyage
          is shorter. Never "approximately 96 hours", never a SOLAS/ISPS
          96-hour rule, never "to DGS".

Scope, deliberately narrow:

  * CORPUS sweeps cover the oral surfaces this batch owns - every meoclass1
    QB page, cheat sheet and oralnotes page, and the SQ free samples. The
    pastpapers / solvedQP product is NOT swept for C_BUNK: its QP2304
    follow-up line is held as a Founder proposal under the solvedQP
    correction skill, not corrected here, and a red gate would misstate that.
    A_TIER, B_OPRC and D_PANS had no pastpapers sites and do sweep there.
  * SITE checks on every corrected card, both sides of the SQ twin, which
    must stay byte-identical for q4 and q14. SQ q18 is a locked teaser.
  * OVER-CORRECTION guards: true teaching beside each false claim survives
    (QB3_J's capability trap, QB9_D's "India has not ratified", QB1_A Q4's
    Merchant Shipping Act 2025 citation, the Coast Guard 700-tonne stocking
    example named as an example).
  * PROVENANCE EXCLUDED: q-version stamps quote the rejected wording, so
    teaching checks strip every q-footer first; stamps are checked alone.
  * NON-VACUOUS: every sweep asserts it read something before it judges.
  * NO digest pin: validate_corrections.py owns the pins.
"""
from __future__ import annotations

import html as htmllib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio, read_text  # noqa: E402
from validate_batch_b import card_digests  # noqa: E402

enable_utf8_stdio()

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-58s %s" % ("PASS" if ok else "FAIL", check, detail))


GATED = QB / "QB1_A.html"
TWIN = REPO / "SQ" / "QB1_A.html"
QB9A = QB / "QB9_A.html"
QB9D = QB / "QB9_D.html"
QB3J = QB / "QB3_J.html"
NOTES = QB / "oralnotes" / "simon-notes-p3.html"
CHEAT = QB / "QB1_B_CheatSheet.html"
GOV = HERE / "qb_content_index_governed.json"
IDX = QB / "qb_content_index.json"
TRAPS = QB / "known_traps.md"
REGISTRY = REPO / "docs" / "sources" / "MIW_SOURCE_REGISTRY.json"
CORR_DATE = "2026-09-17"
STAMP = "India oil-spill regulatory audit"
MANIFEST = HERE / "correction_corr_india_oilspill_regulatory_audit_20260917_manifest.json"
SUB_ISSUES = ("A_TIER", "B_OPRC_DATE", "C_BUNKERS_STATUS", "D_PANS")

# ---- proposition patterns -------------------------------------------------
TIER = re.compile(r"\bTier[\s-]*(?:1|2|3|I{1,3})\b", re.I)
BAND = re.compile(r"(?:<|>|up to|exceeding|over|below|above)?\s*\b(?:700|10,?000)\s*(?:-|to|–)?\s*"
                  r"(?:10,?000\s*)?(?:t\b|MT\b|tonnes?\b|tons?\b)", re.I)
#: a sentence that names a band only to reject it
BAND_REJECTED = re.compile(r"not a tier definition|no tier tonnage|no tonnage|not by (?:fixed )?tonnage|"
                           r"not (?:established|supported)|stocking example|trap|invented", re.I)
OPRC = re.compile(r"\bOPRC\b")
INDIA = re.compile(r"\bIndia(?:n|'s)?\b")
ACCEDE = re.compile(r"ratif|acced|accession|party to|a Party", re.I)
BUNK = re.compile(r"Bunkers?\s+(?:Oil Pollution|Convention|CLC)|Bunkers\s+2001|Civil Liability for Bunker", re.I)
NEG = re.compile(r"\b(?:not|never|no|neither|nor)\b|has not|hasn't|isn't|unratified", re.I)
PARTY_ASSERT = re.compile(
    r"\bIndia\b[^.]{0,40}?\b(?:is|as)\s+(?:a\s+)?(?:Party|party|Contracting State|contracting state|State Party)\b"
    r"|\bIndia\b[^.]{0,20}?\b(?:has\s+)?(?:ratified|acceded to|implements)\b"
    r"|domestic implementation of the Bunker Convention", re.I)
PANS = re.compile(r"\bPANS\b|Pre-?Arrival Notification of Security|pre-arrival security notice", re.I)
N96 = re.compile(r"\b96\b|ninety-six", re.I)
NOT_OPRC = re.compile(r"Intervention|1973 Protocol|OPRC-HNS|HNS Protocol|\bCLC\b|LLMC|Bunker|Nairobi|\bWRC\b")


# --------------------------------------------------------------------------
# helpers (the NOSDCP gate's, reused verbatim in behaviour)
# --------------------------------------------------------------------------

def card_html(page: str, anchor: str, cls: str = "q-card") -> str | None:
    at = page.find('<div class="%s" id="%s"' % (cls, anchor))
    if at < 0:
        return None
    depth, pos = 0, at
    tok = re.compile(r"<div\b|</div>")
    while True:
        m = tok.search(page, pos)
        if not m:
            return None
        depth += -1 if m.group(0) == "</div>" else 1
        pos = m.end()
        if depth == 0:
            return page[at:pos]


def strip_footers(markup: str) -> str:
    out, pos = [], 0
    for m in re.finditer(r'<div class="q-footer"', markup):
        if m.start() < pos:
            continue
        out.append(markup[pos:m.start()])
        depth, end = 0, m.start()
        for tok in re.finditer(r"<div\b|</div>", markup[m.start():]):
            depth += -1 if tok.group(0) == "</div>" else 1
            end = m.start() + tok.end()
            if depth == 0:
                break
        pos = end
    out.append(markup[pos:])
    return "".join(out)


def footer(markup: str) -> str:
    at = markup.find('<span class="q-version"')
    return flatten(markup[at:]) if at >= 0 else ""


def flatten(markup: str) -> str:
    """Tags out, entities decoded. A closing block tag becomes a pilcrow, so a
    reg-box item or list item can never run into its neighbour and borrow the
    neighbour's qualifying words."""
    markup = re.sub(r"</(?:div|p|li|h4|h5|td|tr)>|<br\s*/?>", " ¶ ", markup)
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", markup)))


def prose(flat: str) -> str:
    """Pilcrows out again, for phrase checks that may span an inline tag."""
    return re.sub(r"\s*¶\s*", " ", flat)


def sentences(flat: str) -> list[str]:
    """Full sentences: a ';' does NOT end one, because the conditional limb of
    a rule ('...96 hours before arrival; if the voyage is shorter...') must be
    read with the rule it qualifies. Blocks (pilcrows) and the numbers-box
    ' · ' separator do end one."""
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(])|\s·\s|\s*¶\s*|\s(?=Q:\s)", flat)
    return [s.strip() for s in parts if s and s.strip()]


def oral_pages(include_pastpapers: bool) -> list[pathlib.Path]:
    pages = sorted(QB.rglob("*.html")) + sorted((REPO / "SQ").glob("*.html"))
    if include_pastpapers:
        pages += sorted((REPO / "solvedQP").glob("*.html"))
    else:
        pages = [p for p in pages if "pastpapers" not in p.parts]
    return pages


def page_sentences(p: pathlib.Path) -> list[str]:
    try:
        return sentences(flatten(strip_footers(read_text(p))))
    except (OSError, UnicodeDecodeError):
        return []


def rel(p: pathlib.Path) -> str:
    return p.relative_to(REPO).as_posix()


# --------------------------------------------------------------------------
# proposition predicates - one sentence at a time
# --------------------------------------------------------------------------

def tier_band_taught(s: str) -> bool:
    return bool(TIER.search(s) and BAND.search(s) and not BAND_REJECTED.search(s))


def oprc_wrong_date(s: str) -> bool:
    """A year sitting next to an accession/party verb in an OPRC + India
    sentence must be 1997/1998 (or the Convention's own 1990/1995)."""
    if not (OPRC.search(s) and INDIA.search(s)):
        return False
    years: set[str] = set()
    for m in ACCEDE.finditer(s):
        window = s[max(0, m.start() - 60):m.end() + 60]
        # The verb must belong to OPRC and India - not to a neighbouring
        # instrument in the same sentence ("1973 Protocol ... India not ratified").
        if not (OPRC.search(window) and INDIA.search(window)) or NOT_OPRC.search(window):
            continue
        years |= set(re.findall(r"\b(19[89]\d|20[0-2]\d)\b", window))
    years -= {"1990", "1995", "1997", "1998"}
    if "1993" in years and re.search(r"approv\w*\s+NOSDCP", s) and re.search(r"not India's OPRC date", s):
        years.discard("1993")
    return bool(years)


OTHER_INSTRUMENT = re.compile(r"LLMC|\bCLC\b|\bFund\b|OPRC|MARPOL|Nairobi|Wreck|\bWRC\b|\bHNS\b|Protocol|SOLAS")


def bunkers_party_asserted(s: str) -> bool:
    """India asserted as a Party to the Bunkers Convention - not to a different
    instrument named between the two mentions ('... to which India is a party'
    about LLMC in the same sentence is not this claim)."""
    bunks = [m.start() for m in BUNK.finditer(s)]
    if not bunks:
        return False
    for m in PARTY_ASSERT.finditer(s):
        if m.group(0).lower().startswith("domestic implementation"):
            return True
        if NEG.search(s[max(0, m.start() - 30):m.end()]):
            continue
        near = min(bunks, key=lambda b: abs(b - m.start()))
        between = s[min(near, m.start()):max(near, m.end())]
        if not OTHER_INSTRUMENT.search(between):
            return True
    return False


QUALIFIED = re.compile(r"not (?:a )?Party|not a Contracting|not ratified|unratified", re.I)


def bunkers_in_force_unqualified(s: str) -> bool:
    """'Bunker Convention ... in force' said on a sentence about Indian waters
    without saying India is not a Party."""
    return bool(BUNK.search(s) and re.search(r"\bin force\b", s, re.I)
                and INDIA.search(s)
                and not re.search(r"not (?:a )?Party|not a Contracting|not ratified|unratified", s, re.I))


def pans_defects(s: str) -> list[str]:
    if not PANS.search(s):
        return []
    bad = []
    if re.search(r"≈\s*(?:<[^>]+>\s*)?96|approx\w*\s+96|about 96|~\s*96", s, re.I):
        bad.append("approximate")
    if N96.search(s) and not re.search(r"at least 96|≥\s*96|≥96", s) and not re.search(r"shorter than 96", s):
        bad.append("96 without 'at least'")
    if re.search(r"at least 96|≥\s*96", s) and not re.search(r"\b2 h(?:ours?)?\b", s):
        bad.append("no short-voyage limb")
    if re.search(r"(?:to|notify|notifies)\s+(?:the\s+)?DGS\b|DGS port office", s):
        bad.append("sent to DGS")
    if re.search(r"Pre-?arrival security notice\s*\(PANS", s, re.I):
        bad.append("wrong expansion")
    return bad


def solas_96_asserted(s: str) -> bool:
    return bool(re.search(r"SOLAS|ISPS", s) and N96.search(s)
                and not re.search(r"national rules|Rules, 2024|MS Notice|rather than to SOLAS", s))


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------

def main() -> int:
    gated, twin = read_text(GATED), read_text(TWIN)
    cards = {("gated", a): card_html(gated, a) for a in ("q4", "q14", "q18")}
    cards.update({("twin", a): card_html(twin, a) for a in ("q4", "q14", "q18")})
    q8 = card_html(read_text(QB9A), "q8")
    n5_html = card_html(read_text(NOTES), "n5", cls="note-card")
    missing = [("%s#%s" % k) for k, v in cards.items() if v is None] \
        + ([] if q8 else ["QB9_A#q8"]) + ([] if n5_html else ["simon-notes-p3#n5"])
    report("target_cards_present", not missing, "missing=%s" % (missing or "none"))
    if missing:
        return finish()
    # Structural text (pilcrows) for sentence sweeps; prose for phrase checks.
    flat = {k: flatten(strip_footers(v)) for k, v in cards.items()}
    teach = {k: prose(v) for k, v in flat.items()}
    q8f = flatten(strip_footers(q8))
    q8t = prose(q8f)
    n5f = flatten(n5_html)
    n5 = prose(n5f)

    g, t = card_digests(gated), card_digests(twin)
    report("twin_identical_to_gated", all(g.get(a) == t.get(a) for a in ("q4", "q14")),
           "q4 %s q14 %s" % tuple("==" if g.get(a) == t.get(a) else "!=" for a in ("q4", "q14")))
    report("twin_q18_still_locked_teaser",
           "qb-lock" in cards[("twin", "q18")] and not N96.search(teach[("twin", "q18")]))

    # ================================================================ A_TIER
    report("A_non_vacuous_sites", bool(TIER.search(q8t)) and len(TIER.findall(n5)) >= 3,
           "QB9_A#q8 tiers=%d, notes n5 tiers=%d" % (len(TIER.findall(q8t)), len(TIER.findall(n5))))
    for name, text, structural in (("qb9a_q8", q8t, q8f), ("notes_n5", n5, n5f)):
        taught = [s[:90] for s in sentences(structural) if tier_band_taught(s)]
        report("A_%s_no_tier_band_taught" % name, not taught, "taught=%r" % (taught[:1] or None))
        report("A_%s_tiers_by_capability" % name,
               re.search(r"capabilit", text) is not None
               and re.search(r"beyond local capability", text) is not None
               and re.search(r"beyond regional capability", text) is not None)
        report("A_%s_stocking_example_named_as_example" % name,
               re.search(r"700-tonne figure is a dispersant-stocking example of risk exposure, not a tier definition",
                         text) is not None)
    report("A_notes_heading_not_volume", "Oil Spill Volume Tiers" not in n5 and "by Capability" in n5)
    report("A_notes_tip_not_by_volume",
           "tiers by volume" not in n5 and "tiers by response capability, not by tonnage" in n5)
    report("A_qb9a_key_number_not_a_threshold",
           not re.search(r"Tier 3 \(>\s*10,000", q8t) and "no tier tonnage threshold is quoted" in q8t)

    scanned, tier_sents, taught = 0, 0, []
    for p in oral_pages(include_pastpapers=True):
        ss = page_sentences(p)
        if not ss:
            continue
        scanned += 1
        for s in ss:
            if TIER.search(s):
                tier_sents += 1
                if tier_band_taught(s):
                    taught.append("%s: %s" % (rel(p), s[:100]))
    report("A_corpus_scan_non_vacuous", scanned > 200 and tier_sents > 50,
           "%d page(s), %d tier sentence(s)" % (scanned, tier_sents))
    report("A_corpus_no_tier_tonnage_band_taught", not taught, "found=%r" % (taught[:2] or None))

    qb3j = flatten(read_text(QB3J))
    report("A_overcorrection_qb3j_capability_trap_survives",
           "not fixed spill-size tonnage bands" in qb3j and "by capability" in qb3j)
    report("A_overcorrection_qb1a_q15_no_tonnage_line_survives",
           "Tier tonnage limits are not given here" in flatten(card_html(gated, "q15") or ""))

    # ================================================================ B_OPRC
    reg = re.search(r"OPRC Convention 1990(.*?)(?:</div>|$)", read_text(NOTES), re.S)
    regt = flatten(reg.group(1)) if reg else ""
    report("B_notes_accession_date_stated",
           "17 November 1997" in regt and "17 February 1998" in regt and "IMO Status of Treaties" in regt,
           "reg=%r" % regt[:80])
    report("B_notes_1993_is_nosdcp_approval",
           re.search(r"1993 is the year the Government of India approved NOSDCP, not India's OPRC date", regt)
           is not None)
    report("B_notes_no_verify_hedge", "verify exact year" not in regt)
    scanned, oprc_india, wrong = 0, 0, []
    for p in oral_pages(include_pastpapers=True):
        for s in page_sentences(p):
            if OPRC.search(s) and INDIA.search(s):
                oprc_india += 1
                if oprc_wrong_date(s):
                    wrong.append("%s: %s" % (rel(p), s[:100]))
        scanned += 1
    report("B_corpus_scan_non_vacuous", oprc_india > 10, "%d OPRC+India sentence(s)" % oprc_india)
    report("B_corpus_no_wrong_india_oprc_date", not wrong, "found=%r" % (wrong[:2] or None))

    # ================================================================ C_BUNK
    for side in ("gated", "twin"):
        q4 = teach[(side, "q4")]
        report("C_q4_not_a_party_stated:%s" % side,
               "India is not a Party to the Bunker Convention itself" in q4)
        report("C_q4_domestic_act_kept:%s" % side,
               re.search(r"Merchant Shipping Act, 2025, Part IX Ch IV", q4) is not None
               and re.search(r"domestic bunker-oil pollution liability regime", q4) is not None)
        report("C_q4_no_unverified_1958_equivalent:%s" % side, "1958 Act equivalent" not in q4)
        report("C_q4_sections_as_read:%s" % side,
               "ss.198, 204, 205, 206–207" in q4 and "above 1,000 GT" in q4)
    cheat = flatten(read_text(CHEAT))
    report("C_cheatsheet_in_force_qualified",
           re.search(r"in force internationally \(since 21 Nov 2008\) — but India is not a Party", cheat) is not None)
    scanned, bunk_sents, asserted, unqual = 0, 0, [], []
    for p in oral_pages(include_pastpapers=False):
        ss = page_sentences(p)
        if not ss:
            continue
        scanned += 1
        for s in ss:
            if BUNK.search(s):
                bunk_sents += 1
                if bunkers_party_asserted(s):
                    asserted.append("%s: %s" % (rel(p), s[:100]))
        # "in force" is judged per BLOCK: a reg-box item may state the Act and
        # qualify India's treaty status in its next sentence.
        page = re.sub(r"(?is)<script\b.*?</script>", " ", strip_footers(read_text(p)))
        for block in re.split(r"\s*¶\s*", flatten(page)):
            for s in sentences(block):
                if bunkers_in_force_unqualified(s) and not QUALIFIED.search(block):
                    unqual.append("%s: %s" % (rel(p), s[:100]))
    report("C_corpus_scan_non_vacuous", scanned > 150 and bunk_sents > 30,
           "%d page(s), %d Bunkers sentence(s)" % (scanned, bunk_sents))
    report("C_corpus_india_not_taught_as_party", not asserted, "found=%r" % (asserted[:2] or None))
    report("C_corpus_in_force_not_applied_to_india_unqualified", not unqual, "found=%r" % (unqual[:2] or None))
    qb9d = flatten(read_text(QB9D))
    report("C_overcorrection_qb9d_not_ratified_survives",
           len(re.findall(r"India has not ratified (?:the )?Bunker Convention", qb9d)) >= 2)

    # ================================================================ D_PANS
    for side in ("gated", "twin"):
        q14 = teach[(side, "q14")]
        pans = [s for s in sentences(flat[(side, "q14")]) if PANS.search(s)]
        bad = [(s[:70], pans_defects(s)) for s in pans if pans_defects(s)]
        report("D_q14_pans_conditional_rule:%s" % side,
               len(pans) == 1 and not bad
               and "Pre-Arrival Notification of Security" in q14 and "not a pollution report" in q14,
               "sites=%d bad=%r" % (len(pans), bad[:1] or None))
    q18 = teach[("gated", "q18")]
    pans18 = [s for s in sentences(flat[("gated", "q18")]) if PANS.search(s)]
    bad18 = [(s[:70], pans_defects(s)) for s in pans18 if pans_defects(s)]
    report("D_q18_pans_sites_non_vacuous", len(pans18) >= 5, "%d site(s)" % len(pans18))
    report("D_q18_every_pans_site_conditional", not bad18, "bad=%r" % (bad18[:1] or None))
    report("D_q18_source_recipients_scope",
           all(k in q18 for k in ("Merchant Shipping Notice 13 of 2024", "Port Facility Security Officer",
                                  "regional authority", "500 GT and above", "FAL Form 7")))
    report("D_q18_no_solas_96_hour_rule",
           not [s for s in sentences(flat[("gated", "q18")]) if solas_96_asserted(s)])
    # Bound to the security-layer limb itself: Q18's E6 enrichment separately
    # names "SOLAS regulation XI-2/9.2.2" in the declaration list, so a bare
    # substring test passed with this limb deleted (mutation D6 proved it).
    report("D_q18_solas_limb_kept",
           re.search(r"SOLAS regulation XI-2/9\.2 lets a Contracting Government require a ship intending "
                     r"to enter its port to provide security-related information before entry", q18) is not None)

    scanned, pans_sents, bad = 0, 0, []
    for p in oral_pages(include_pastpapers=True):
        ss = page_sentences(p)
        scanned += bool(ss)
        for s in ss:
            if PANS.search(s):
                pans_sents += 1
                d = pans_defects(s)
                if d:
                    bad.append("%s: %s %r" % (rel(p), s[:70], d))
    report("D_corpus_scan_non_vacuous", pans_sents >= 7, "%d PANS sentence(s)" % pans_sents)
    report("D_corpus_no_pans_defect", not bad, "found=%r" % (bad[:2] or None))

    # ================================================================ RECORD
    stamps = {
        "q4": footer(cards[("gated", "q4")]), "q14": footer(cards[("gated", "q14")]),
        "q18": footer(cards[("gated", "q18")]), "q8": footer(q8)}
    report("stamps_record_correction",
           "v1.2" in stamps["q4"] and STAMP in stamps["q4"]
           and "v1.2" in stamps["q14"] and STAMP in stamps["q14"]
           and "v1.1" in stamps["q14"] and "NOSDCP authority correction" in stamps["q14"]
           and "v1.1" in stamps["q18"] and STAMP in stamps["q18"]
           and "v1.2" in stamps["q8"] and STAMP in stamps["q8"],
           "q14 keeps the NOSDCP v1.1 provenance")

    gov = json.loads(read_text(GOV))
    notes_ = [e for e in gov.get("recently_updated", []) if e.get("date") == CORR_DATE]
    note = notes_[0]["note"] if len(notes_) == 1 else ""
    report("governed_note_present", len(notes_) == 1, "%d note(s)" % len(notes_))
    report("governed_note_states_all_four",
           all(k in note for k in ("capability", "17 November 1997", "not a Party", "at least 96 hours",
                                   "2 hours", "QB1_A", "QB9_A"))
           and sorted(notes_[0].get("files", [])) == ["QB1_A.html", "QB9_A.html"] if notes_ else False)
    idx = json.loads(read_text(IDX))
    report("generated_index_matches_governed_changelog",
           [e.get("note") for e in gov.get("recently_updated", [])]
           == [e.get("note") for e in idx.get("recently_updated", [])])

    traps = read_text(TRAPS)
    at = traps.find("### 134. ")
    entry = traps[at:] if at >= 0 else ""
    nxt = re.search(r"\n### \d+\.", entry[5:])
    entry = entry[:nxt.start() + 5] if nxt else entry
    report("trap_134_present", at >= 0)
    grep = re.search(r"^GREP:\s*(.+)$", entry, re.M)
    report("trap_134_not_a_blanket_ban",
           bool(grep) and grep.group(1).strip().upper().startswith("SKIP"),
           "GREP=%r" % (grep.group(1)[:40] if grep else None))
    report("trap_134_four_sub_issues",
           all(k in entry for k in ("A_TIER", "B_OPRC_DATE", "C_BUNKERS_STATUS", "D_PANS")))
    report("trap_134_logs_held_items",
           "QP2304" in entry and "QP2310" in entry and "Nairobi" in entry)
    e133 = traps[traps.find("### 133. "):at] if at >= 0 else ""
    report("trap_133_points_to_resolution", "resolved in entry 134" in e133)

    # The record carries the four propositions as a structured block. The
    # schema admits `sub_issues` only because these checks read it.
    man = json.loads(read_text(MANIFEST)) if MANIFEST.is_file() else {}
    subs = man.get("sub_issues") or {}
    verdicts = {"CORRECT", "PARTLY_CORRECT", "INCORRECT", "UNSUPPORTED", "OUTDATED"}
    well_formed = subs and set(subs) == set(SUB_ISSUES) and all(
        s.get("verdict", "").split(" ")[0] in verdicts
        and s.get("authority") and s.get("evidence_class") and s.get("confidence")
        and s.get("safe_to_implement") is True
        for s in subs.values())
    report("record_states_four_sub_issues", bool(well_formed),
           "keys=%s" % (sorted(subs) or "none"))
    declared = {c.get("correction_action_id"): c.get("sub_issue") for c in man.get("cards", [])}
    unmapped = sorted(a for a, s in declared.items() if s not in SUB_ISSUES)
    listed = {a for s in subs.values() for a in (s.get("cards") or [])}
    orphan = sorted(listed - set(declared))
    # every card's sub_issue must be one of the four, every card a sub_issue
    # lists must exist, and the two directions must agree on which is which
    crossed = sorted(a for a in listed if declared.get(a) and a not in
                     (subs.get(declared[a], {}).get("cards") or []))
    report("record_sub_issue_cards_resolve",
           bool(declared) and not unmapped and not orphan and not crossed,
           "unmapped=%s orphan=%s crossed=%s" % (unmapped or None, orphan or None, crossed or None))
    report("record_verdicts_match_the_correction",
           subs.get("A_TIER", {}).get("verdict") == "UNSUPPORTED"
           and subs.get("B_OPRC_DATE", {}).get("verdict") == "INCORRECT"
           and re.search(r"not a Party", subs.get("C_BUNKERS_STATUS", {}).get("verdict", ""), re.I)
           and subs.get("D_PANS", {}).get("verdict", "").startswith("PARTLY_CORRECT"))

    reg = json.loads(read_text(REGISTRY))
    ids = {s["source_id"]: s for s in reg["sources"]}
    need = ["SRC-IMO-STATUS-TREATIES-2026-08-26", "SRC-DGMA-MSNOTICE-13-2024-PANS", "SRC-ICG-NOSDCP-2015-PLAN"]
    report("sources_registered", all(n in ids for n in need),
           "missing=%r" % ([n for n in need if n not in ids] or None))
    plan = ids.get("SRC-ICG-NOSDCP-2015-PLAN", {})
    report("nosdcp_plan_recorded_access_limited", plan.get("access_status") == "ACCESS_LIMITED"
           and "Tier tonnage thresholds." in json.dumps(plan.get("claims_NOT_established", [])))

    return finish()


def finish() -> int:
    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    for f in FAILS:
        print("  FAIL " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
