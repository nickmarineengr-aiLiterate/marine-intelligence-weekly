#!/usr/bin/env python3
"""Content gate for CORR-NOSDCP-MINISTRY-20260916 - who owns NOSDCP, who pays.

The propositions, in three lines:
  1. NOSDCP sits under the MINISTRY OF DEFENCE; the Indian Coast Guard is the
     Central Coordinating Authority (the Allocation of Business Rules say
     "Central Coordinating Agency"). Not the Ministry of Earth Sciences, and
     not a "nodal agency".
  2. The SHIPOWNER is liable, normally within convention limits; the P&I club
     is the liability INSURER - never "the P&I club is liable for all costs".
  3. The Master reports to the coastal State under MARPOL Protocol I; the
     Company/DPA is informed in parallel, not as a step in front of it.

Deliberately narrow, following validate_correction_itc51.py:

  * PROPOSITION-SCOPED. "Earth Sciences" is legitimate in this bank (QB9_E,
    marine spatial planning). The gate never bans the phrase: it fails only
    where the phrase is BOUND to NOSDCP / Coast Guard authority without a
    negation, and it asserts that QB9_E's legitimate use survives, so a
    blanket substitution goes red too.
  * SITE-SCOPED on the two corrected cards, in BOTH the gated page and its
    SQ twin, and the twin must stay byte-identical to the gated copy.
  * CORPUS-WIDE only for the ministry and "nodal" bindings, and only inside
    sentences that name NOSDCP - the defect this record closes.
  * PROVENANCE EXCLUDED. The v1.1 stamps quote the rejected wording to record
    what moved, so teaching checks strip every q-footer first; the stamps are
    then checked on their own.
  * NON-VACUOUS. Every sweep asserts it read something before it judges.
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
    print("%-4s %-56s %s" % ("PASS" if ok else "FAIL", check, detail))


GATED = QB / "QB1_A.html"
TWIN = REPO / "SQ" / "QB1_A.html"
CARDS = ("q14", "q15")
GOV = HERE / "qb_content_index_governed.json"
IDX = QB / "qb_content_index.json"
TRAPS = QB / "known_traps.md"
CORR_DATE = "2026-09-16"
STAMP = "NOSDCP authority correction"

NOSDCP = re.compile(r"NOS-?DCP|Oil Spill Disaster Contingency", re.I)
EARTH = re.compile(r"Earth Sciences|\bMoES\b")
NEGATED = re.compile(r"\b(?:not|never|Not)\b[^.]{0,30}$")
NODAL = re.compile(r"\bnodal\b", re.I)
#: One P&I mention at a time: a span may not run across a second "P&I", or the
#: CE tip's "the P&I club insures ... never 'the P&I club is liable for all
#: costs'" would be read as one assertion starting at the first mention.
PANDI_LIABLE = re.compile(
    r"P&I(?:(?!P&I)[^.]){0,60}?(?:strictly\s+liable|liable\s+for\s+(?:ALL|all)|all\s+(?:\w+\s+){0,3}costs|club\s+pays)"
    r"|(?:recover\w*|recovery\s+of)\s+all\s+costs(?:(?!P&I)[^.]){0,60}P&I", re.I)
#: A correction quotes the wording it rejects (SKILL.md 8.2a), so a hit counts
#: only when it is ASSERTED - not when a negation governs it.
REJECTS = re.compile(r"\b(?:never|not)\b[^.]{0,12}$", re.I)


def pandi_asserted(text: str) -> list[str]:
    return [m.group(0)[:80] for m in PANDI_LIABLE.finditer(text)
            if not REJECTS.search(text[max(0, m.start() - 40):m.start()])]
DPA_CHAIN = re.compile(r"Master\s*→\s*DPA|DPA\s*→\s*ICG")


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def card_html(page: str, anchor: str) -> str | None:
    at = page.find('<div class="q-card" id="%s"' % anchor)
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
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", markup)))


def sentences(flat: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.;!?])\s+|\s(?=Q:\s)", flat) if s.strip()]


def earth_bound_unnegated(text: str) -> list[str]:
    """Earth Sciences / MoES occurrences NOT negated and NOT framed as support."""
    bad = []
    for s in sentences(text):
        for m in EARTH.finditer(s):
            before = s[:m.start()]
            if NEGATED.search(before):
                continue
            if re.search(r"INCOIS", s) and re.search(r"support", s, re.I):
                continue
            bad.append(s.strip()[:120])
    return bad


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------

def main() -> int:
    pages = {"gated": read_text(GATED), "twin": read_text(TWIN)}
    cards = {}
    for side, page in pages.items():
        for a in CARDS:
            cards[(side, a)] = card_html(page, a)
    missing = [("%s#%s" % k) for k, v in cards.items() if v is None]
    report("target_cards_present", not missing, "missing=%s" % (missing or "none"))
    if missing:
        return finish()

    teach = {k: flatten(strip_footers(v)) for k, v in cards.items()}
    for k, t in teach.items():
        report("non_vacuous_nosdcp:%s#%s" % k, len(NOSDCP.findall(t)) >= 2,
               "%d NOSDCP mention(s)" % len(NOSDCP.findall(t)))

    # The SQ free sample must be the gated card, byte for byte.
    g, t = card_digests(pages["gated"]), card_digests(pages["twin"])
    report("twin_identical_to_gated", all(g.get(a) == t.get(a) for a in CARDS),
           "q14 %s q15 %s" % tuple("==" if g.get(a) == t.get(a) else "!=" for a in CARDS))

    for side in ("gated", "twin"):
        q14, q15 = teach[(side, "q14")], teach[(side, "q15")]
        both = q14 + " " + q15

        # 1. Ministry and designation.
        report("q15_ministry_of_defence:%s" % side,
               re.search(r"Ministry:\s*Ministry of Defence", q15) is not None
               and len(re.findall(r"Ministry of Defence", q15)) >= 4,
               "%d mention(s)" % len(re.findall(r"Ministry of Defence", q15)))
        report("q15_no_earth_sciences_as_authority:%s" % side,
               not earth_bound_unnegated(q15), "bound=%r" % (earth_bound_unnegated(q15)[:2] or None))
        report("q15_central_coordinating_authority:%s" % side,
               len(re.findall(r"Central Coordinating Authority", q15)) >= 4)
        # Site-scoped: body, 60-second answer and reg-box each carry "Agency",
        # and every one of them is attributed to the Business Rules.
        agency = [m.start() for m in re.finditer(r"Central Coordinating Agency", q15)]
        unattributed = [q15[max(0, i - 60):i + 30] for i in agency
                        if not re.search(r"Allocation of Business|Business Rules", q15[max(0, i - 250):i])]
        report("q15_business_rules_say_agency:%s" % side,
               len(agency) >= 3 and not unattributed,
               "%d site(s), unattributed=%r" % (len(agency), unattributed[:1] or None))
        report("q14_central_coordinating_authority:%s" % side,
               "Central Coordinating Authority" in q14)
        report("no_nodal_designation:%s" % side, not NODAL.search(both),
               "found=%r" % (NODAL.search(both).group(0) if NODAL.search(both) else None))

        # 2. Liability: shipowner liable, P&I insures.
        hits = pandi_asserted(both)
        report("no_pandi_liable_for_all_costs:%s" % side, not hits,
               "asserted=%r" % (hits[:2] or None))
        report("pandi_rejection_still_quoted:%s" % side,
               re.search(r"never\s+\"the P&I club is liable for all costs\"", q15) is not None,
               "the CE tip names the wrong answer so candidates can recognise it")
        for a, t_ in (("q14", q14), ("q15", q15)):
            report("%s_shipowner_liable_pandi_insures:%s" % (a, side),
                   re.search(r"shipowner[^.]{0,40}liable", t_) is not None
                   and re.search(r"P&I[^.]{0,40}insur|insur\w*[^.]{0,20}P&I", t_) is not None
                   # "within port limits" is geography, not liability: the
                   # limit must be a convention or liability limit.
                   and re.search(r"within[^.]{0,25}(?:convention|liability)\s+limits", t_) is not None)

        # Direct action against the insurer is Convention-conditional: every
        # site that teaches it must carry the qualification.
        da = [s for s in sentences(both) if re.search(r"directly against the insurer", s)]
        unq = [s[:90] for s in da if not re.search(r"where the applicable Convention provides for direct action", s)]
        report("direct_action_is_qualified:%s" % side, len(da) >= 3 and not unq,
               "%d site(s), unqualified=%r" % (len(da), unq[:1] or None))

        # 3. Reporting.
        report("no_dpa_before_statutory_report:%s" % side, not DPA_CHAIN.search(both))
        # Renaming DGS must never put DGMA into the Protocol I reporting chain.
        chain = [s[:90] for s in sentences(both)
                 if re.search(r"Protocol I|MRCC|reporting chain", s) and re.search(r"\bDGMA\b|\bDGS\b", s)]
        report("no_dgma_in_reporting_chain:%s" % side, not chain, "found=%r" % (chain[:1] or None))
        report("reporting_protocol_i_parallel_dpa:%s" % side,
               all("Protocol I" in t_ and re.search(r"DPA[^.]{0,30}(?:in parallel)|in parallel[^.]{0,30}DPA", t_)
                   for t_ in (q14, q15)))
        report("no_dgs_in_teaching:%s" % side, not re.search(r"\bDGS\b", both))

        # 4. Wording the approval ruled out.
        report("no_current_edition_2015_claim:%s" % side,
               not re.search(r"current edition[^.]{0,20}2015", q15, re.I))
        report("incois_not_only:%s" % side,
               not re.search(r"INCOIS[^.]{0,20}\bonly\b|\bonly\b[^.]{0,20}INCOIS", both))

    # 5. Stamps record the correction (read deliberately: the one place the old
    #    wording is quoted, so the one place it could hide as teaching).
    stamps = 0
    for a in CARDS:
        f = footer(cards[("gated", a)])
        ok = "v1.1" in f and STAMP in f and "Central Coordinating Authority" in f
        if a == "q15":
            ok = ok and "Ministry of Defence" in f
        stamps += ok
    report("stamps_record_correction", stamps == len(CARDS), "%d/%d" % (stamps, len(CARDS)))

    # 6. Corpus-wide: no page binds NOSDCP to Earth Sciences or to "nodal".
    scanned, nos_sentences, bad_earth, bad_nodal = 0, 0, [], []
    for p in sorted(QB.rglob("*.html")):
        try:
            flat = flatten(strip_footers(read_text(p)))
        except (OSError, UnicodeDecodeError):
            continue
        scanned += 1
        for s in sentences(flat):
            if not NOSDCP.search(s):
                continue
            nos_sentences += 1
            if earth_bound_unnegated(s):
                bad_earth.append("%s: %s" % (p.name, s[:100]))
            if NODAL.search(s):
                bad_nodal.append("%s: %s" % (p.name, s[:100]))
    report("corpus_scan_non_vacuous", scanned > 50 and nos_sentences > 40,
           "%d page(s), %d NOSDCP sentence(s)" % (scanned, nos_sentences))
    report("corpus_no_earth_sciences_nosdcp_binding", not bad_earth,
           "found=%r" % (bad_earth[:2] or None))
    report("corpus_no_nodal_nosdcp_designation", not bad_nodal,
           "found=%r" % (bad_nodal[:2] or None))

    # 7. Over-correction guard: the phrase is legitimate elsewhere.
    qb9e = read_text(QB / "QB9_E.html")
    report("qb9e_legit_moes_usage_survives",
           len(re.findall(r"Ministry of Earth Sciences", qb9e)) >= 2
           and "National Centre for Coastal Research" in qb9e,
           "Earth Sciences is correct for marine spatial planning")

    # 8. Changelog: governed note states the correction; derived index agrees.
    gov = json.loads(read_text(GOV))
    notes = [e for e in gov.get("recently_updated", []) if e.get("date") == CORR_DATE
             and "NOSDCP" in e.get("note", "")]
    note = notes[0]["note"] if notes else ""
    report("governed_note_present", len(notes) == 1, "%d note(s)" % len(notes))
    report("governed_note_states_mod_and_authority",
           "Ministry of Defence" in note and "Central Coordinating Authority" in note
           and re.search(r"not the Ministry of\s+Earth Sciences", note) is not None)
    idx = json.loads(read_text(IDX))
    report("generated_index_matches_governed_changelog",
           [e.get("note") for e in gov.get("recently_updated", [])]
           == [e.get("note") for e in idx.get("recently_updated", [])])

    # 9. The trap entry prevents recurrence without a blanket ban.
    traps = read_text(TRAPS)
    at = traps.find("### 133. NOSDCP")
    entry = traps[at:] if at >= 0 else ""
    nxt = re.search(r"\n### \d+\.", entry[5:])
    entry = entry[:nxt.start() + 5] if nxt else entry
    report("trap_133_present", at >= 0)
    grep = re.search(r"^GREP:\s*(.+)$", entry, re.M)
    report("trap_133_not_a_blanket_ban",
           bool(grep) and grep.group(1).strip().upper().startswith("SKIP"),
           "GREP=%r" % (grep.group(1)[:40] if grep else None))
    report("trap_133_logs_both_followups",
           "Follow-up A" in entry and "Follow-up B" in entry and "NOT actioned" in entry)

    return finish()


def finish() -> int:
    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    for f in FAILS:
        print("  FAIL " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
