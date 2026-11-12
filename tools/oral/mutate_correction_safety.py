#!/usr/bin/env python3
"""Mutation suite for the CORR-SAFETY-* records (validate_correction_safety.py).

Every mutation names the check that OWNS its proposition; a digest pin is never accepted as the catch
(oral_content_mutation.DIGEST_PINS). Four directions:

  * REGRESSION   each of the six unsafe positions put back, on the corrected card and on pages the corrections never
                 touched (a corpus check that only looked at corrected cards would be decoration).
  * ESCAPES      the three ways the first P0 gate was shown to be blind, pinned so they cannot return: a corrective
                 qualifier in the SAME sentence as a reintroduced EEBD entry (M01), a key-number card whose value and
                 description sit in separate divs, and an arrow between a trap question and its wrong answer.
  * OVER-SWEEP   true teaching removed (the CO2 criterion, the recycling regime, the container-ship table rule).
  * GOVERNANCE   the cross-product RulesApp item fixed while its record still says OPEN, closed while the text is
                 still wrong, its declaration removed or moved onto an MIW page, a record without founder_authorisation,
                 a card dropped from its record, and a production label in a public footer.
  * ROUND 2      each S1-S3 finding of the independent whole-card review put back (AH-AY), including the round-2
                 withdrawal of SOLAS II-2/19.3.8 from the container-hold card (AK).
  * HPFUEL       CORR-SAFETY-HPFUEL-PIPE-20261022 (BA-BI): the clamp put back on QB5_A#q11 and planted on an untouched
                 page (also as repair tape, and beside an unrelated "never"), and each reviewed safe step removed or
                 reordered (fire watch first, stop before cut-out, load transfer, no deferral, the clamp statement).
"""
from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_bytes import read_text, write_text           # noqa: E402
from oral_content_mutation import edit_json, run_suite, sub_in_file   # noqa: E402

MC = REPO / "meoclass1"
QB1_F, QB1_E, QB5_A, QB5_B, QB8_A = (MC / "QB1_F.html", MC / "QB1_E.html", MC / "QB5_A.html", MC / "QB5_B.html",
                                    MC / "QB8_A.html")
QB3_B, QB3_G, QB2_E = MC / "QB3_B.html", MC / "QB3_G.html", MC / "QB2_E.html"
CS_A, CS_B = MC / "QB5_A_CheatSheet.html", MC / "QB5_B_CheatSheet.html"
RA_DATA = REPO / "RulesApp/repository/index/repo-data.json"
RA_SEARCH = REPO / "RulesApp/repository/index/search-index.json"
REC = {k: HERE / ("correction_corr_safety_%s_20261019_manifest.json" % k) for k in
       ("eebd_entry", "lsa_falls_coldstart", "enclosed_space", "crankcase_response", "imdg_stowage_segregation",
        "enclosed_space_propagation", "enclosed_space_ext", "enclosed_space_cheatsheets")}
REC["hpfuel_pipe"] = HERE / "correction_corr_safety_hpfuel_pipe_20261022_manifest.json"
PROBE = "validate_correction_safety.py"


def multi(*ops):
    def apply():
        for op in ops:
            op()
    return apply


def drop_cross_product(data):
    data["propagation"]["cross_product_safety_items"] = []


def move_cross_product_to_miw(data):
    for item in data["propagation"]["cross_product_safety_items"]:
        item["path"] = "meoclass1/QB1_E.html"


def drop_founder_authorisation(data):
    data.pop("founder_authorisation", None)


def close_cross_product_unverified(data):
    for item in data["propagation"]["cross_product_safety_items"]:
        item["status"] = "CLOSED_VERIFIED"


def drop_qb3g_card(data):
    data["cards"] = [c for c in data["cards"] if c["path"] != "meoclass1/QB3_G.html"]


RULESAPP_WAS = "Five-yearly: davit falls (wires) must be turned end-for-end or replaced outright"
RULESAPP_FIX = "Five-yearly: davit falls (wires) are renewed on deterioration or at not more than 5 years"

MUTATIONS = [
    # ---- REGRESSION -------------------------------------------------------
    ("A", "QB1_F#q1: fire squad makes entry on EEBDs again",
     sub_in_file(QB1_F, "The ship's fire squad entered wearing fire-fighter's outfits with self-contained breathing "
                        "apparatus &mdash; EEBDs are escape-only devices and are never worn by fire-fighters (FSS Code "
                        "ch.3, 2.2.1.2; MSC/Circ.849) &mdash;", "The ship's fire squad made entry using appropriate PPE "
                        "and EEBD,", count=1),
     "qb1f_q1_entry_in_firefighters_outfit"),
    ("B", "QB1_E#q1: falls 'renewed, or turned end-for-end' again",
     sub_in_file(QB1_E, "falls used in launching inspected periodically (special regard to areas passing through "
                        "sheaves) and renewed on deterioration or at intervals of not more than 5 years, whichever is "
                        "earlier", "lifeboat/liferaft launching falls renewed, or turned end-for-end, within 5 years",
                 count=1),
     "qb1e_q1_no_end_for_end"),
    ("C", "QB1_E page cheat sheet: +15 C start again (outside the card)",
     sub_in_file(QB1_E, "≤ 2 min @ −15 °C (LSA 4.4.6.2)", "≤ 2 min @ 15°C", count=1),
     "qb1e_page_cheatsheet_minus_15"),
    ("D", "QB1_E#q1: ahead/astern re-attributed to LSA 4.4.6.2",
     sub_in_file(QB1_E, "(LSA Code 4.4.6.2; rescue boats via 5.1.1.1). At the weekly test",
                 "and run ahead/astern (LSA Code 4.4.6.2; rescue boats via 5.1.1.1); at the weekly test", count=1),
     "qb1e_q1_ahead_astern_not_attributed_to_4_4_6_2"),
    ("E", "QB2_E (never corrected): falls end-for-end planted",
     sub_in_file(QB2_E, "</body>", "<p>Falls are renewed, or turned end-for-end, every 5 years.</p></body>", count=1),
     "corpus_falls_no_end_for_end_alternative"),
    ("F", "QB5_A#q11: O2 19.5-23.5% band back in the table",
     sub_in_file(QB5_A, "<td><strong>steady 20.9% by volume</strong></td>", "<td><strong>19.5% to 23.5%</strong></td>",
                 count=1),
     "corpus_enclosed_space_o2_not_19_5_band"),
    ("G", "QB5_A#q11: 'if entry is essential' wording back",
     sub_in_file(QB5_A, "Entry into such a space falls under MSC.581(110) section 9: it requires very careful "
                        "consideration, and positive-pressure breathing apparatus should always be worn",
                 "If entry is essential, MSC.581(110) section 9 applies: positive-pressure breathing apparatus",
                 count=1),
     "qb5a_q11_section9_wording_not_essential_only"),
    ("H", "QB5_A#q11: SOLAS XI-1/5 cited for enclosed spaces again",
     sub_in_file(QB5_A, '<span class="reg-code">SOLAS III/19.3.6 &amp; XI-1/7</span><span class="reg-desc">Enclosed '
                        'space entry and rescue drills (III/19.3.6); atmosphere testing instrument for enclosed spaces '
                        'carried on board (XI-1/7)</span>',
                 '<span class="reg-code">SOLAS Ch. XI-1, Reg. 5</span><span class="reg-desc">Enclosed space entry '
                 'procedures</span>', count=1),
     "qb5a_q11_no_xi1_5_enclosed"),
    ("I", "QB5_A#q8: 'stop, ventilate, investigate' back in the tip",
     sub_in_file(QB5_A, "Execute (keep everyone clear of the engine and the crankcase relief valves; do not open the "
                        "crankcase doors or let air into the crankcase until the engine has cooled for the period in "
                        "the maker's instructions — if air goes into the crankcase an explosion can occur; then find "
                        "the hot spot, with a portable extinguisher ready when the doors are first opened if no fixed "
                        "extinguishing system is in use)", "Execute (stop, ventilate, investigate per maker's manual)",
                 count=1),
     "qb5a_q8_no_ventilate_step"),
    ("J", "QB5_A#q8: 'emergency stop - SOLAS II-1 obligation' back",
     sub_in_file(QB5_A, "Decision (reduce speed at once and stop the engine as soon as it is navigationally safe — as "
                        "the engine maker's manual directs (WinGD X82DF OM 2.6, for example); it is not a SOLAS rule)",
                 "Decision (emergency stop — SOLAS §II-1 obligation)", count=1),
     "corpus_crankcase_no_solas_stop_attribution"),
    ("K", "QB5_A#q8: WinGD 20 min made universal",
     sub_in_file(QB5_A, "until the engine has cooled for the period in the maker's instructions",
                 "until the engine has cooled for 20 min", count=1),
     "qb5a_q8_maker_period_not_universal_20min"),
    ("L", "QB8_A#q5: category D 'under deck only' again",
     sub_in_file(QB8_A, "<li><strong>Category D:</strong> <strong>on deck only</strong>",
                 "<li><strong>Category D:</strong> Cargo must be stowed <strong>under deck only</strong>", count=1),
     "qb8a_q5_cat_d_on_deck_only"),
    ("M", "QB8_A#q5: 'Separated from (6m/12m)' planted",
     sub_in_file(QB8_A, "Segregation between incompatible goods uses four terms:",
                 "Segregation uses &quot;Separated from&quot; (6m/12m) among four terms:", count=1),
     "corpus_imdg_cat_d_and_separated_from"),
    ("N", "QB5_B#q15: O2 19.5-23.5% back in step 2",
     sub_in_file(QB5_B, "steady readings meet the IMO criteria — 20.9% O₂ by volume",
                 "readings meet O₂ 19.5–23.5% (target 20.9%)", count=1),
     "corpus_enclosed_space_o2_not_19_5_band"),
    ("O", "QB5_B#q15: 'lowering the pump is not an entry' dropped",
     sub_in_file(QB5_B, "lowering the pump from deck is not an entry, but the tank", "the tank", count=1),
     "qb5b_q15_lowering_is_not_entry"),
    ("P", "QB5_A#q10: 'SCBA eliminates' back",
     sub_in_file(QB5_A, "which reduces exposure, it does not remove the hazard",
                 "SCBA eliminates Likelihood of exposure", count=1),
     "qb5a_q10_ba_reduces_not_eliminates"),
    ("Q", "QB1_F#q8: minimum O2 21.0% back",
     sub_in_file(QB1_F, "<li>Oxygen for entry: a <strong>steady 20.9%</strong> by volume",
                 "<li>Minimum safe oxygen level for entry: <strong>21.0%</strong> by volume", count=1),
     "qb1f_q8_msc581_criteria"),
    ("R", "QB3_B#q3: '<5 ppm H2S maximum permissible before entry' back",
     sub_in_file(QB3_B, "toxic gases such as H₂S below 50% of the applicable OEL — not a fixed ppm.",
                 "&lt;5 ppm H₂S — maximum permissible before entry.", count=1),
     "corpus_enclosed_space_toxic_not_fixed_ppm"),
    # ---- ESCAPES (blind spots of the first P0 gate) ----------------------
    ("S", "M01 escape: EEBD entry reintroduced inside the corrective sentence",
     sub_in_file(QB1_F, "The ship's fire squad entered wearing fire-fighter's outfits with self-contained breathing "
                        "apparatus &mdash; EEBDs", "The ship's fire squad made entry using appropriate PPE and EEBD "
                        "&mdash; EEBDs", count=1),
     "corpus_eebd_not_entry_equipment"),
    ("T", "kn-card escape: value '1 ppm' and description 'H2S entry limit' in separate divs",
     sub_in_file(CS_A, '<div class="kn-val">&lt;50% OEL</div><div class="kn-desc">Toxic gases (H₂S, CO) for enclosed '
                       'space entry</div>', '<div class="kn-val">1 ppm</div><div class="kn-desc">H₂S TLV-TWA for '
                       'enclosed space entry</div>', count=1),
     "corpus_enclosed_space_toxic_not_fixed_ppm"),
    ("U", "arrow escape: '\"H2S limit?\" -> 1 ppm' across an arrow",
     sub_in_file(CS_B, "→ no one enters unless toxic gases are below 50% of the applicable OEL with the other "
                       "MSC.581(110) 7.4 criteria met — not a fixed ppm", "→ 1 ppm TLV-TWA (not 10 ppm)", count=1),
     "corpus_enclosed_space_toxic_not_fixed_ppm"),
    # ---- OVER-SWEEP ---------------------------------------------------------
    ("V", "QB5_A#q11: the CO2 criterion deleted everywhere on the card",
     multi(sub_in_file(QB5_A, "CO₂ below 0.5% (5,000 ppm), flammable", "flammable", count=1),
           sub_in_file(QB5_A, "<tr><td>CO₂</td><td><strong>&lt;0.5% by volume (5,000 ppm)</strong></td>",
                       "<tr><td>CO</td><td><strong>n/a</strong></td>", count=1),
           sub_in_file(QB5_A, "Then give the rest of the IMO set: CO₂ below 0.5%,", "Then give the rest of the IMO set:",
                       count=1),
           sub_in_file(QB5_A, "steady 20.9% O₂, CO₂ below 0.5%, below 1% LFL", "steady 20.9% O₂, below 1% LFL", count=1),
           sub_in_file(QB5_A, "steady 20.9% O₂; CO₂ &lt;0.5%; flammables", "steady 20.9% O₂; flammables", count=1)),
     "qb5a_q11_co2_below_0_5"),
    ("W", "QB3_G#q4: recycling regime replaced by an unsourced 0 ppm target",
     sub_in_file(QB3_G, "not more than 50% of the OEL for toxic gases", "toxic gases as close to 0 ppm as achievable",
                 count=1),
     "qb3g_q4_recycling_regime_attributed"),
    ("X", "QB8_A#q5: container-ship level-4 'two bulkheads' rule deleted",
     multi(sub_in_file(QB8_A, " or two bulkheads where an open container is involved", "", count=1),
           sub_in_file(QB8_A, "(closed v closed) or two bulkheads (where an open container is involved);",
                       "(closed v closed);", count=1)),
     "qb8a_q5_container_table_level4_bulkheads"),
    ("Y", "QB5_A cheat sheet: CO2 row deleted",
     sub_in_file(CS_A, '<td><strong>&lt;0.5% (5,000 ppm)</strong></td>', '<td><strong>n/a</strong></td>', count=1),
     "qb5a_cheatsheet_msc581_criteria"),
    # ---- GOVERNANCE ---------------------------------------------------------
    ("Z", "RulesApp corrected but the record still says OPEN",
     multi(sub_in_file(RA_DATA, RULESAPP_WAS, RULESAPP_FIX, count=1),
           sub_in_file(RA_SEARCH, RULESAPP_WAS, RULESAPP_FIX, count=1)),
     "cross_product_items_not_stale"),
    ("AA", "RulesApp cross-product declaration removed from the record",
     edit_json(REC["lsa_falls_coldstart"], drop_cross_product), "corpus_falls_no_end_for_end_alternative"),
    ("AB", "cross-product declaration moved onto an MIW page",
     edit_json(REC["lsa_falls_coldstart"], move_cross_product_to_miw), "cross_product_items_only_in_separate_products"),
    ("AC", "a record loses founder_authorisation",
     edit_json(REC["crankcase_response"], drop_founder_authorisation), "records_carry_founder_authorisation"),
    ("AD", "QB3_G#q4 dropped from its record",
     edit_json(REC["enclosed_space_ext"], drop_qb3g_card), "card_present_QB3_G_q4"),
    ("AE", "production label 'P0' leaks into a public footer",
     sub_in_file(QB5_A, "corrected 19 Oct 2026 by CORR-SAFETY-CRANKCASE-RESPONSE-20261019",
                 "corrected 19 Oct 2026 by CORR-P0-CRANKCASE-RESPONSE-20261019", count=1),
     "no_production_vocabulary_QB5_A_q8"),
    ("AF", "QB1_F#q1: MS Notice 07 of 2023 back as the casualty-reporting notice",
     sub_in_file(QB1_F, "DGS/DGMA MS Notice 04 of 2026", "DG Shipping MS Notice 07 of 2023", count=1),
     "qb1f_q1_casualty_reporting_notice_04_2026"),
    ("AG", "QB1_F#q1: 'Class C fire' back",
     sub_in_file(QB1_F, "confirmed an electrical fire within the enclosure", "confirmed a class C fire within the "
                        "enclosure", count=1),
     "qb1f_q1_no_class_c_electrical"),
    # ---- ROUND 2 (whole-card review round 1) ---------------------------------
    ("AH", "RulesApp item marked CLOSED_VERIFIED while the falls text is still wrong",
     edit_json(REC["lsa_falls_coldstart"], close_cross_product_unverified), "corpus_falls_no_end_for_end_alternative"),
    ("AI", "QB3_G#q4: 'continuous monitoring is required throughout' back",
     sub_in_file(QB3_G, "so the Competent person re-tests as often as necessary", "so continuous monitoring is required "
                        "throughout; the Competent person re-tests as often as necessary", count=1),
     "no_invented_wording_QB3_G_q4"),
    ("AJ", "QB5_B#q15: unsourced '<10% LEL for pumping' back",
     sub_in_file(QB5_B, "Re-test while the work continues, and stop on any alarm",
                 "The &lt;10% LEL figure for pumping is a company/SMS limit. Re-test while the work continues, and stop "
                 "on any alarm", count=1),
     "no_invented_wording_QB5_B_q15"),
    ("AK", "QB8_A#q5: SOLAS II-2/19.3.8 bulkhead rule put on the container hold (Table 19.1: decks only)",
     sub_in_file(QB8_A, "so I first check whether this Class 3 entry carries it.",
                 "so I first check whether this Class 3 entry carries it. Separately, SOLAS II-2/19.3.8 requires the "
                 "bulkhead to be A-60 unless the goods are at least 3 m away.", count=1),
     "qb8a_q5_no_19_3_8_bulkhead_rule_for_container_hold"),
    ("AS", "QB8_A#q5: SW1 presented as applying to every Class 3 entry (column 16a caveat dropped)",
     multi(sub_in_file(QB8_A, " SW1 is assigned entry by entry in column 16a of the Dangerous Goods List, so I first check "
                              "whether this Class 3 entry carries it.", "", count=1),
           sub_in_file(QB8_A, " &mdash; after checking in column 16a of the Dangerous Goods List which entries carry SW1",
                       "", count=1)),
     "qb8a_q5_sw1_entry_specific_column_16a"),
    ("AT", "QB3_B#q3: Poor coating = 'intermediate survey cycle no longer applies' back",
     sub_in_file(QB3_B, "with thickness measurements as the surveyor deems necessary.",
                 "with thickness measurements. The standard intermediate survey cycle no longer applies to that space.",
                 count=1),
     "qb3b_q3_poor_coating_annual_interval_z7_2_2_7"),
    ("AV", "QB1_F#q8: 'out-of-water bottom surveys' back in the 15-second answer",
     sub_in_file(QB1_F, "and a minimum of two inspections of the outside of the bottom in any five-year period,",
                 "and mandatory out-of-water bottom surveys twice in a five-year cycle, and two inspections of the outside "
                 "of the bottom in any five-year period,", count=1),
     "qb1f_q8_bottom_inspections_a1207_4_6"),
    ("AW", "QB1_F#q8: 15-20% crop-and-renew trap answer back",
     sub_in_file(QB1_F, "Wastage is assessed against the classification society&#x27;s renewal criteria for that member;",
                 "Wastage exceeding 15–20% requires immediate crop-and-renew;", count=1),
     "qb1f_q8_no_universal_wastage_percentage"),
    ("AX", "QB1_F#q8: Z10.2 'forward + one other hold' for every age again (trap Q2)",
     sub_in_file(QB1_F, "adjacent shell plating — in the forward cargo hold for ships of 10–15 years, and in the forward "
                        "hold and one other selected hold for ships over 15 years (UR Z10.2 3.2.4.1, 3.2.4.2) — and any",
                 "adjacent shell plating in a forward hold and one other selected hold — and any", count=1),
     "qb1f_q8_z10_2_age_bands"),
    ("AY", "QB1_F#q8: every wastage finding left as a condition of class",
     sub_in_file(QB1_F, "is to be repaired promptly; only isolated, localised damage that does not affect structural "
                        "integrity may be left", "may be left", count=1),
     "qb1f_q8_wastage_prompt_repair_z7_1_3"),
    ("AU", "QB5_A cheat sheet: stop-work trap left unanswered again",
     sub_in_file(CS_A, " (trap — answer: no entry unless a steady 20.9% is read first; once inside, test frequently and "
                       "leave at any sign of deterioration or if ventilation fails, MSC.581(110) 7.4, 8.1, 8.3)",
                 " (trap)", count=1),
     "qb5a_cheatsheet_stop_work_trap_answered"),
    ("AL", "QB5_A#q11: the 6.5.3 low-level toxic/flammable trigger dropped",
     sub_in_file(QB5_A, " MSC.581(110) 6.5.3 adds that if testing shows O₂ below 20.9%, or even low levels of flammable "
                        "or toxic gases, the space should be treated as one where the atmosphere is known or suspected "
                        "to be unsafe (section 9).", "", count=2),
     "qb5a_q11_low_level_toxic_flammable_6_5_3"),
    ("AM", "QB3_B#q3: coating grades attributed to PSPC again",
     sub_in_file(QB3_B, "classifying it as Good, Fair or Poor as defined in IACS UR Z7 1.2.10",
                 "classifying it as Good, Fair, or Poor as per PSPC criteria", count=1),
     "qb3b_q3_coating_grades_iacs_z7"),
    ("AN", "QB5_A cheat sheet: OEL 'from the SMS / flag State' back",
     sub_in_file(CS_A, "OEL from accepted national or international standards (7.7), e.g. ACGIH TLV; entry needs below "
                       "half of it", "OEL from the SMS / flag State (e.g. ACGIH TLV); the entry limit is half of it",
                 count=1),
     "qb5a_cheatsheet_oel_source_and_6_5_3"),
    ("AO", "QB5_B#q15: enclosed-space permit made unconditional again",
     sub_in_file(QB5_B, "<strong>HIGH</strong> — no entry; an enclosed space permit only if entry is unavoidable</td>",
                 "<strong>HIGH</strong> — enclosed space permit required</td>", count=1),
     "qb5b_q15_entry_permit_conditional"),
    ("AP", "QB1_E#q1: weekly-test ambient-temperature condition dropped",
     sub_in_file(QB1_E, ", provided the ambient temperature is above the minimum required for starting and running the "
                        "engine,", ",", count=1),
     "qb1e_q1_weekly_test_ambient_condition_20_6_2"),
    ("AQ", "QB3_B#q1: attendant / permit steps cut back to 'four elements'",
     sub_in_file(QB3_B, "who in an emergency does not enter before help has arrived (8.5).", "who does not enter.",
                 count=1),
     "qb3b_q1_permit_and_attendant_8_5"),
    ("AR", "QB5_A#q8: 'second explosion' back in the tip",
     sub_in_file(QB5_A, "— if air goes into the crankcase an explosion can occur;",
                 "— fresh air reaching a hot spot can cause a second explosion;", count=1),
     "no_invented_wording_QB5_A_q8"),
    # ---- HPFUEL (CORR-SAFETY-HPFUEL-PIPE-20261022) ---------------------------
    ("BA", "QB5_A#q11: slow ahead + temporary clamp on the HP fuel pipe back",
     sub_in_file(QB5_A, "Decision: post a fire watch with fire-fighting equipment ready and keep people clear of the "
                        "spray.", "Decision: reduce to slow ahead to reduce FO injection pressure, isolate that injector "
                        "and fit a temporary clamp, reduce likelihood to 1.", count=1),
     "corpus_hp_fuel_pipe_no_clamp_repair"),
    ("BB", "QB2_E (never corrected): HP fuel-pipe clamp planted",
     sub_in_file(QB2_E, "</body>", "<p>A leaking high-pressure fuel pipe can be fitted with a temporary clamp until "
                                   "the next port.</p></body>", count=1),
     "corpus_hp_fuel_pipe_no_clamp_repair"),
    ("BC", "QB2_E: injection pipe wrapped with repair tape planted",
     sub_in_file(QB2_E, "</body>", "<p>Leaking injection pipe: wrap it with repair tape and run on to port.</p></body>",
                 count=1),
     "corpus_hp_fuel_pipe_no_clamp_repair"),
    ("BD", "QB2_E: clamp beside an unrelated 'never' (the negation must be about the repair)",
     sub_in_file(QB2_E, "</body>", "<p>Never run with an open leak: isolate that injector and fit a temporary clamp."
                                   "</p></body>", count=1),
     "corpus_hp_fuel_pipe_no_clamp_repair"),
    ("BE", "QB5_A#q11: 'a clamp is not an accepted repair' statement dropped",
     sub_in_file(QB5_A, "A clamp is not an accepted repair on a high-pressure fuel pipe: if no spare",
                 "If no spare", count=1),
     "qb5a_q11_hp_pipe_clamp_not_accepted"),
    ("BF", "QB5_A#q11: repair deferred to next port again",
     sub_in_file(QB5_A, "Entire process documented in engine log and defect report raised.",
                 "Full repair deferred to next port. Entire process documented in engine log and defect report raised.",
                 count=1),
     "qb5a_q11_hp_pipe_no_deferral_to_port"),
    ("BG", "QB5_A#q11: fire watch no longer posted first",
     sub_in_file(QB5_A, "Decision: post a fire watch with fire-fighting equipment ready and keep people clear of the "
                        "spray. With the Master's agreement", "Decision: with the Master's agreement", count=1),
     "qb5a_q11_hp_pipe_fire_watch_first"),
    ("BH", "QB5_A#q11: injection cut out before the engine is stopped (WinGD 10.14: engine stopped first)",
     sub_in_file(QB5_A, "then stop the engine and cut out that cylinder's injection",
                 "then cut out that cylinder's injection and stop the engine", count=1),
     "qb5a_q11_hp_pipe_stop_then_cut_out"),
    ("BI", "QB5_A#q11: auxiliary engine stopped without transferring the load",
     sub_in_file(QB5_A, "start the standby generator, transfer the load to it, then stop the leaking engine",
                 "start the standby generator and stop the leaking engine", count=1),
     "qb5a_q11_hp_pipe_aux_load_transfer"),
    ("BJ", "the HP fuel-pipe record loses founder_authorisation",
     edit_json(REC["hpfuel_pipe"], drop_founder_authorisation), "records_carry_founder_authorisation"),
]

WATCHED = [QB1_F, QB1_E, QB5_A, QB5_B, QB8_A, QB3_B, QB3_G, QB2_E, CS_A, CS_B, RA_DATA, RA_SEARCH] + list(REC.values())


def main() -> int:
    return run_suite("CORR-SAFETY-* (P0 safety corrections)", PROBE, MUTATIONS, WATCHED)


if __name__ == "__main__":
    raise SystemExit(main())
