#!/usr/bin/env python3
"""
Content gate for the CORR-SAFETY-* records (the P0 safety corrections, 19 Oct 2026).

WHAT IT ASSERTS
---------------
Propositions, not strings. For each of the six unsafe positions the corrections removed there is

  * a CARD check, closed-world on every corrected card, that the safe position is STATED there, and
  * a CORPUS check, open-world over every authored surface, that the unsafe position is stated NOWHERE.

The six positions: EEBDs as fire-fighting/entry equipment; lifeboat falls "turned end-for-end" as an alternative to
renewal; a +15 C lifeboat engine start; a 19.5-23.5 % oxygen band, or a fixed H2S/CO ppm figure, as the enclosed-space
entry criterion; ventilating or opening a crankcase after an oil-mist / crankcase-explosion warning (and the false
"SOLAS II-1 obligation"); IMDG stowage category D "under deck only" and "separated from" as 6 m / 12 m.

A corpus hit inside a SEPARATELY GOVERNED PRODUCT (RulesApp) is not this gate's to fix. It passes only if a CORR-SAFETY
record declares it in `propagation.cross_product_safety_items` with status OPEN and the exact matching fragment; the
landing gate (check_founder_authorisation_for_landing.py L4) then refuses landing until that item is CLOSED_VERIFIED.
A declared item that no longer matches is a stale declaration and FAILS, so the record cannot drift from the corpus.

TEXT UNIT
---------
A block (li / p / tr / kn-card). The q-version footer is stripped first, because every corrected footer quotes the
rejected wording on purpose. Two blind spots of the first P0 gate are closed here and pinned by mutations: a key-number
card's value and description are ONE unit (`<div class="kn-val">1 ppm</div><div class="kn-desc">H2S entry limit`), and
an arrow ("limit?" -> "1 ppm") does not split a sentence.

Prints the repo dialect "<N> checks, <M> FAIL".
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
from oral_bytes import read_text  # noqa: E402  (UTF-8 contract)

RECORD_GLOB = "correction_corr_safety_*_manifest.json"
SURFACES = ("meoclass1/*.html", "meoclass1/oralnotes/*.html", "meoclass1/pastpapers/*.html", "solvedQP/*.html",
            "RulesApp/repository/index/*.json")
CROSS_PRODUCT_PREFIXES = ("RulesApp/",)
CARD_OPEN = re.compile(r'<div class="q-card[^"]*"[^>]*>', re.I)

_checks, _failed = 0, []


def report(name, ok, detail=""):
    global _checks
    _checks += 1
    if not ok:
        _failed.append(name)
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  -- " + detail) if detail else ""))


# ------------------------------------------------------------------ text
def balanced_end(text, start):
    depth = 0
    for m in re.finditer(r"<div\b[^>]*>|</div\s*>", text[start:], re.I):
        depth += -1 if m.group(0).startswith("</") else 1
        if depth == 0:
            return start + m.end()
    return None


def card_block(page, anchor):
    for m in CARD_OPEN.finditer(page):
        if re.search(r'\bid="%s"' % re.escape(anchor), m.group(0)):
            end = balanced_end(page, m.start())
            return page[m.start():end] if end else None
    return None


def visible(fragment):
    t = re.sub(r'<span class="q-version">.*?</span>', " ", fragment, flags=re.S)
    t = re.sub(r"<(script|style)\b.*?</\1>", " ", t, flags=re.S | re.I)
    t = re.sub(r"</div>\s*<div class=\"kn-desc\">", " : ", t)
    t = re.sub(r"</t[dh]\s*>", " ¦ ", t, flags=re.I)
    t = re.sub(r"</?(div|p|li|tr|h\d|ul|ol|table|pre|details|summary|br)\b[^>]*>", "\n", t, flags=re.I)
    t = re.sub(r"<[A-Za-z/!][^>]*>", " ", t)
    t = html.unescape(t).replace("−", "-").replace("–", "-").replace(" ", " ")
    return "\n".join(" ".join(l.split()) for l in t.split("\n") if l.strip())


def units(text):
    return [s for s in re.split(r"\n|(?<=[.;!?])\s+(?=[A-Z\"'(])", text) if s.strip()]


def surface_text(p):
    t = read_text(p)
    if p.suffix == ".json":
        t = html.unescape(re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), t))
    return t


# ------------------------------------------------------------------ the six unsafe positions
NEG = r"(?:\bnot\b|\bnever\b|\bno\b|escape[- ]only|for escape only)"


def unsafe_eebd(s):
    if not re.search(r"\bEEBDs?\b", s):
        return False
    for m in re.finditer(r"(entr(y|ies)|entered|enter(ing)?|fire squad|fire party|fire-?fighters?|rescue team)"
                         r"[^.;—]{0,60}\b(using|with|wearing|donned|on)\b[^.;—]{0,40}\bEEBDs?\b"
                         r"|\b(using|with|wearing|donned|on)\b[^.;—]{0,40}\bEEBDs?\b[^.;—]{0,40}"
                         r"(to enter|entr|for fire-?fighting)", s, re.I):
        if not re.search(NEG, s[max(0, m.start() - 25):m.end()], re.I):
            return True
    return False


def unsafe_falls(s):
    return bool(re.search(r"\bfalls?\b", s, re.I) and re.search(r"end[- ]for[- ]end", s, re.I)
                and not re.search(r"(not an alternative|no longer|deleted|superseded|pre-2008|before 2008)", s, re.I))


def unsafe_cold_start(s):
    return bool(re.search(r"(lifeboat|rescue boat|engine)", s, re.I) and re.search(r"start", s, re.I)
                and re.search(r"(?<![-0-9.])15 ?°? ?C\b", s))


def unsafe_o2_band(s):
    return bool(re.search(r"(O₂|O2|O_2|oxygen)", s, re.I)
                and re.search(r"19\.5 ?%|19\.5 ?[-to ]+ ?23(\.5)? ?%|23\.5 ?%|23 ?% max", s, re.I))


def unsafe_fixed_ppm_entry(s):
    return bool(re.search(r"(H₂S|H2S|H_2S|\bCO\b)", s) and re.search(r"\b(1|5|10|25) ?ppm\b", s)
                and re.search(r"(entry|enter|limit|max|strictly|permissible|<|&lt;)", s, re.I)
                and not re.search(r"50 ?% of", s, re.I))


def unsafe_crankcase(s):
    if not re.search(r"(crankcase explosion|crankcase (alarm|warning)|oil[- ]mist (alarm|warning|detector|detection|high)"
                     r"|high oil[- ]mist)", s, re.I):
        return False
    return bool(re.search(r"\b(ventilat\w*|open(ing)? the crankcase|admit air)\b", s, re.I)
                and not re.search(r"(do not|never|until|without|cooled for)", s, re.I))


def unsafe_solas_stop(s):
    return bool(re.search(r"emergency stop", s, re.I) and re.search(r"SOLAS\s*§?\s*II-1\s*obligation", s, re.I))


def unsafe_imdg(s):
    return bool(re.search(r"categor(y|ies)\s*D\b[^.;]{0,80}under deck only", s, re.I)
                or re.search(r"separated from[^.;]{0,40}(6 ?m ?/ ?12 ?m|12 ?m(eters|etres)? on deck|6 ?m(eters|etres)? "
                             r"(horizontal separation )?under deck)", s, re.I))


PROPOSITIONS = {
    "eebd_not_entry_equipment": unsafe_eebd,
    "falls_no_end_for_end_alternative": unsafe_falls,
    "lsa_engine_cold_start_not_plus15": unsafe_cold_start,
    "enclosed_space_o2_not_19_5_band": unsafe_o2_band,
    "enclosed_space_toxic_not_fixed_ppm": unsafe_fixed_ppm_entry,
    "crankcase_no_ventilate_on_warning": unsafe_crankcase,
    "crankcase_no_solas_stop_attribution": unsafe_solas_stop,
    "imdg_cat_d_and_separated_from": unsafe_imdg,
}

# ------------------------------------------------------------------ closed-world card checks
H = lambda rx: (lambda t: bool(re.search(rx, t, re.I | re.S)))       # noqa: E731
NOT = lambda rx: (lambda t: not re.search(rx, t, re.I | re.S))       # noqa: E731
CARD_CHECKS = {
    ("meoclass1/QB1_F.html", "q1"): [
        ("qb1f_q1_entry_in_firefighters_outfit", H(r"fire-?fighter'?s outfits? with self-contained breathing apparatus")),
        ("qb1f_q1_eebd_escape_only_stated", H(r"EEBDs? (are|is) escape[- ]only")),
        ("qb1f_q1_co2_alarm_is_a_minimum", H(r"in no case less than 20 s")),
        ("qb1f_q1_no_due_diligence_fire_exclusion", NOT(r"want of due diligence[^.]{0,120}outside cover")),
        ("qb1f_q1_no_class_c_electrical", NOT(r"class C fire")),
        ("qb1f_q1_dc_link_stored_energy", H(r"DC-link capacitors stay charged after isolation")),
        ("qb1f_q1_casualty_reporting_notice_04_2026", H(r"MS Notice 04 of 2026")),
    ],
    ("meoclass1/QB1_E.html", "q1"): [
        ("qb1e_q1_falls_renewal_rule_twice", lambda t: len(re.findall(r"whichever is earlier", t)) >= 2
         and bool(re.search(r"deterioration[^.]{0,80}not more than 5 years", t))),
        ("qb1e_q1_no_end_for_end", NOT(r"end[- ]for[- ]end")),
        ("qb1e_q1_cold_start_minus_15_lsa_4_4_6_2", lambda t: bool(re.search(r"-15 ?°C", t)) and "4.4.6.2" in t),
        ("qb1e_q1_ahead_astern_not_attributed_to_4_4_6_2", NOT(r"ahead/astern \(LSA Code 4\.4\.6\.2")),
        ("qb1e_q1_weekly_test_ambient_condition_20_6_2", H(r"provided the ambient temperature is above the minimum")),
    ],
    ("meoclass1/QB5_A.html", "q11"): [
        ("qb5a_q11_o2_steady_20_9", lambda t: bool(re.search(r"steady[^.]{0,40}20\.9 ?%", t)) and t.count("20.9") >= 3),
        ("qb5a_q11_co2_below_0_5", H(r"CO₂[^.]{0,30}(<|below|less than) ?0\.5 ?%")),
        ("qb5a_q11_toxic_below_50pct_oel", H(r"50 ?% of the (applicable )?(OEL|occupational exposure limit)")),
        ("qb5a_q11_cites_msc581", H(r"MSC\.581\(110\)")),
        ("qb5a_q11_section9_wording_not_essential_only", lambda t: "very careful consideration" in t
         and not re.search(r"if entry is essential", t, re.I)),
        ("qb5a_q11_no_xi1_5_enclosed", NOT(r"XI-1,? ?(Reg\.?|/) ?5\b")),
        ("qb5a_q11_low_level_toxic_flammable_6_5_3", H(r"6\.5\.3[^;]{0,140}even low levels of flammable or toxic")),
        ("qb5a_q11_oel_from_accepted_standards_7_7", H(r"accepted national or international standards")),
    ],
    ("meoclass1/QB5_A.html", "q8"): [
        ("qb5a_q8_no_air_before_cooling", H(r"do not open the crankcase doors[^.]{0,80}until the engine has cooled")),
        ("qb5a_q8_maker_period_not_universal_20min", lambda t: "maker" in t and not re.search(r"20 ?min", t)),
        ("qb5a_q8_no_ventilate_step", NOT(r"Execute \(stop, ventilate")),
        ("qb5a_q8_extinguisher_ready_when_doors_opened", H(r"portable extinguisher ready when the doors are first opened")),
    ],
    ("meoclass1/QB8_A.html", "q5"): [
        ("qb8a_q5_cat_d_on_deck_only", H(r"Category D:[^.]{0,200}on deck only")),
        ("qb8a_q5_cat_d_e_prohibited_other_passenger", lambda t: len(re.findall(
            r"prohibited[^.]{0,20}on other passenger ships", t)) >= 2),
        ("qb8a_q5_no_under_deck_only", NOT(r"under deck only")),
        ("qb8a_q5_container_table_level4_bulkheads", H(r"two bulkheads")),
        # SOLAS II-2/19.3.8 is NOT put on this container-hold card: Table 19.1 row 3.8 applies it to container cargo
        # spaces for decks only (note 2). The SW1 heat rule is entry-specific (DGL column 16a).
        ("qb8a_q5_no_19_3_8_bulkhead_rule_for_container_hold", NOT(r"19\.3\.8")),
        ("qb8a_q5_sw1_entry_specific_column_16a", lambda t: len(re.findall(r"column 16a", t)) >= 2),
    ],
    ("meoclass1/QB5_B.html", "q15"): [
        ("qb5b_q15_lowering_is_not_entry", H(r"lowering the pump from deck is not an entry")),
        ("qb5b_q15_msc581_criteria", lambda t: "20.9%" in t and bool(re.search(r"CO₂ below 0\.5", t))
         and bool(re.search(r"50% of the applicable OEL", t))),
        ("qb5b_q15_unsafe_atmosphere_section9", H(r"section 9")),
        ("qb5b_q15_no_a1050_or_xi1_5_current", lambda t: not re.search(r"A\.1050\(27\)</span>|XI-1, Reg\. 5", t)),
        ("qb5b_q15_entry_permit_conditional", lambda t: len(re.findall(r"only if (someone must|entry is unavoidable)",
                                                                       t)) >= 3
         and not re.search(r"enclosed space permit required|enclosed space entry \(pump must be lowered", t)),
        ("qb5b_q15_low_level_toxic_flammable_6_5_3", H(r"6\.5\.3[^;]{0,140}even low levels of flammable or toxic")),
        ("qb5b_q15_test_from_outside_7_3", H(r"from outside with sampling hoses or fixed lines")),
    ],
    ("meoclass1/QB5_A.html", "q10"): [
        ("qb5a_q10_toxic_below_50pct_oel", H(r"below 50% of the applicable OEL")),
        ("qb5a_q10_ba_reduces_not_eliminates", lambda t: "does not remove the hazard" in t
         and "SCBA eliminates" not in t),
    ],
    ("meoclass1/QB1_F.html", "q8"): [
        ("qb1f_q8_msc581_criteria", lambda t: t.count("20.9%") >= 2 and "21.0%" not in t),
        ("qb1f_q8_bottom_inspections_a1207_4_6", lambda t: "two inspections of the outside of the bottom" in t
         and "out-of-water bottom surveys" not in t),
        ("qb1f_q8_z10_2_scope_single_side_skin", NOT(r"bulk carriers and oil tankers, the annual survey|bulk carrier or "
                                                     r"oil tanker, is the close-up")),
        ("qb1f_q8_no_universal_wastage_percentage", NOT(r"15[–-]20 ?%")),
        ("qb1f_q8_entry_and_hot_work_separate", NOT(r"fit for hot work and entry")),
        ("qb1f_q8_no_drafting_residue", NOT(r"unverified this pass")),
        # all five sites (detailed s.1, reg box, trap Q2, Numbers, Common Failures) carry the age bands
        ("qb1f_q8_z10_2_age_bands", lambda t: len(re.findall(r"forward (cargo )?hold (at|for ships of) 10[–-]15 years",
                                                             t, re.I)) >= 5 and "3.2.4.2" in t),
        ("qb1f_q8_wastage_prompt_repair_z7_1_3", H(r"repaired promptly; only isolated, localised damage")),
    ],
    ("meoclass1/QB3_B.html", "q1"): [
        ("qb3b_q1_msc581_criteria", lambda t: "20.9%" in t and "CO₂" in t and "toxics 0 ppm" not in t),
        ("qb3b_q1_permit_and_attendant_8_5", lambda t: "risk assessment and entry permit" in t
         and "does not enter before help has arrived" in t),
    ],
    ("meoclass1/QB3_B.html", "q3"): [
        ("qb3b_q3_toxic_below_50pct_oel", lambda t: "50% of the applicable OEL" in t and "5 ppm" not in t),
        ("qb3b_q3_coating_grades_iacs_z7", lambda t: "UR Z7 1.2.10" in t and "hard scale at 10%" in t
         and "PSPC criteria" not in t and "Evaluation (PSPC" not in t and "coating grade definitions" not in t),
        ("qb3b_q3_poor_coating_annual_interval_z7_2_2_7", lambda t: t.count("2.2.7") >= 2
         and "intermediate survey cycle no longer applies" not in t),
    ],
    ("meoclass1/QB3_G.html", "q4"): [
        ("qb3g_q4_recycling_regime_attributed", lambda t: "MEPC.210(63)" in t and "Competent person" in t
         and "MSC.581(110)" in t and "0 ppm" not in t),
        ("qb3g_q4_retest_every_eight_hour_shift", H(r"at least once in every eight-hour shift")),
    ],
}
FILE_CHECKS = {
    "meoclass1/QB5_A_CheatSheet.html": [
        ("qb5a_cheatsheet_msc581_criteria", lambda t: "steady 20.9%" in t and "0.5% (5,000 ppm)" in t
         and "50% of OEL" in t),
        ("qb5a_cheatsheet_oel_source_and_6_5_3", lambda t: "accepted national or international standards" in t
         and "(6.5.3)" in t and "SMS / flag State" not in t),
        ("qb5a_cheatsheet_stop_work_trap_answered", H(r"stop work\?.{0,60}no entry unless a steady 20\.9")),
    ],
    "meoclass1/QB5_B_CheatSheet.html": [
        ("qb5b_cheatsheet_msc581_criteria", lambda t: "MSC.581(110) 7.4" in t and "A.1050" not in t),
    ],
    "meoclass1/QB1_E.html": [
        ("qb1e_page_cheatsheet_minus_15", H(r"≤ 2 min @ -15 °C")),
    ],
}
# wording the review brief names as invented, or figures with no primary source: forbidden on every corrected card
# and on both cheat sheets (round 2, whole-card review round 1)
INVENTED_WORDING = [
    (r"continuous (atmosphere )?monitoring (is )?required|IMO requires continuous", "continuous-monitoring duty"),
    (r"only if (entry is )?essential|if entry is essential|essential entry", "'essential entry' (not IMO wording)"),
    (r"< ?10 ?% (LEL|LFL)", "unsourced <10% LEL figure"),
    (r"OEL (comes )?from the SMS", "OEL source is accepted standards (7.7)"),
    (r"second explosion", "'second explosion' on the doors-opened warning"),
    (r"as per PSPC criteria", "coating grades are IACS UR Z7"),
]
FORBIDDEN_PUBLIC = [(r"\bP1-[AB]\b|\bP0\b", "batch label"), (r"(?i)\bTODO\b|\bFIXME\b|\bDRAFT NOTE\b", "editorial marker")]


def main() -> int:
    records = sorted(HERE.glob(RECORD_GLOB))
    report("safety_records_present", len(records) >= 7, "%d record(s)" % len(records))
    declared, cards = [], []
    for p in records:
        m = json.loads(read_text(p))
        prop = m.get("propagation") if isinstance(m.get("propagation"), dict) else {}
        for item in prop.get("cross_product_safety_items") or []:
            declared.append((item.get("path"), item.get("proposition"), item.get("match"), item.get("status"), p.name))
        cards += [(c["path"], c["anchor"]) for c in m.get("cards") or []]
    report("records_carry_founder_authorisation", all("founder_authorisation" in json.loads(read_text(p))
                                                      for p in records), "")
    for (path, anchor), checks in CARD_CHECKS.items():
        page = REPO / path
        block = card_block(read_text(page), anchor) if page.is_file() else None
        report("card_present_%s_%s" % (Path(path).stem, anchor), bool(block) and (path, anchor) in cards,
               "declared by a record=%s" % ((path, anchor) in cards))
        text = visible(block or "")
        for name, fn in checks:
            report(name, bool(block) and fn(text))
        raw = html.unescape(re.sub(r"<[^>]+>", " ", block or ""))
        report("no_production_vocabulary_%s_%s" % (Path(path).stem, anchor),
               not any(re.search(rx, raw) for rx, _ in FORBIDDEN_PUBLIC))
        hits = [why for rx, why in INVENTED_WORDING if re.search(rx, text, re.I)]
        report("no_invented_wording_%s_%s" % (Path(path).stem, anchor), not hits, "; ".join(hits))
    for path, checks in FILE_CHECKS.items():
        text = visible(read_text(REPO / path))
        for name, fn in checks:
            report(name, fn(text))
        if "CheatSheet" in path:
            hits = [why for rx, why in INVENTED_WORDING if re.search(rx, text, re.I)]
            report("no_invented_wording_%s" % Path(path).stem, not hits, "; ".join(hits))
    seen = set()
    files = sorted({p for g in SURFACES for p in REPO.glob(g)})
    for prop_name, fn in PROPOSITIONS.items():
        undeclared = []
        for p in files:
            rel = p.relative_to(REPO).as_posix()
            for s in (s for s in units(visible(surface_text(p))) if fn(s)):
                owner = [d for d in declared if d[0] == rel and d[1] == prop_name and d[2] and d[2] in s
                         and d[3] == "OPEN" and rel.startswith(CROSS_PRODUCT_PREFIXES)]
                if owner:
                    seen.update(owner)
                else:
                    undeclared.append("%s: %s" % (rel, s[:100]))
        report("corpus_%s" % prop_name, not undeclared, "; ".join(undeclared[:3]))
    stale = [d for d in declared if d[3] == "OPEN" and d not in seen]
    report("cross_product_items_not_stale", not stale, "stale=%s" % [d[:2] for d in stale])
    report("cross_product_items_only_in_separate_products",
           all(str(d[0]).startswith(CROSS_PRODUCT_PREFIXES) for d in declared), "")
    print("\n%d checks, %d FAIL" % (_checks, len(_failed)))
    return 1 if _failed else 0


if __name__ == "__main__":
    sys.exit(main())
