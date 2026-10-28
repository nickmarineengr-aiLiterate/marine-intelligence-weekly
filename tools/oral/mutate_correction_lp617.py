#!/usr/bin/env python3
"""Mutation suite for CORR-LP617-SEWAGE-SLUDGE-20261028.

Every mutation names the PROPOSITION check it must trip; the shared harness
refuses a digest pin as a catch. Probes only validate_correction_lp617.py
(validate_corrections owns the pins and is exercised by corrections_mutate).

REGRESSION (A-E): each of the three limbs that shipped the defect goes back to
  it on its own - the CE Oral Tip's shipped sentence, sludge back in the
  reverse-list enumeration, sludge back in the 60-second list, the removal
  clause dropped - so a "somewhere on the card it is right" check cannot pass.
DATES (F-I4): the closed-world date checks - adoption given as entry into
  force, a near-miss entry-into-force date, a wrong permit cut-off in the body
  and in the tip (including the card's two other true dates), and a wrong
  entry-into-force date written before its verb.
SCOPE (J-L): the treaty-scope limb deleted, the correction widened into a
  worldwide ban (in a sludge sentence and outside one), the MARPOL Annex IV
  separation dropped.
ADDED CONTRADICTIONS (I5-I7, J2, K3): a wrong sentence added BESIDE correct
  text - a cut-off "on entry into force", an "effective" date, a cut-off that
  never says "permit", scope extended to 1972 Convention Parties, a worldwide
  reg-box row. Exact-phrase limb checks prove the right text is present and
  cannot see these; they come from the independent re-check of 28 Oct 2026.
CROSS-QUESTION (M): the examiner question answered the wrong way.
TWIN (N, O): the SQ free sample regresses on its own, and drifts by one byte.
CORPUS (P): the defect reappears on a page this record never touched.
OVER-CORRECTION (Q): a blanket substitution wipes QB3_C's correct Annex VI text.
RECORD (R-Y): the stamp, the governed note, the derived index, the trap GREP,
  a logged follow-up, the record's proposition and trap link, a source row.
NON-VACUITY (Z): the target card disappears from the census input.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import edit_json, run_suite, sub_in_file  # noqa: E402

GATED = REPO / "meoclass1/QB1_A.html"
TWIN = REPO / "SQ/QB1_A.html"
QB3C = REPO / "meoclass1/QB3_C.html"
SHEET = REPO / "meoclass1/QB9_A_CheatSheet.html"
TRAPS = REPO / "meoclass1/known_traps.md"
GOV = HERE / "qb_content_index_governed.json"
IDX = REPO / "meoclass1/qb_content_index.json"
RECORD = HERE / "correction_corr_lp617_sewage_sludge_20261028_manifest.json"
REGISTRY = REPO / "docs/sources/MIW_SOURCE_REGISTRY.json"

PROBE = "validate_correction_lp617.py"
WATCHED = [GATED, TWIN, QB3C, SHEET, TRAPS, GOV, IDX, RECORD, REGISTRY]

TIP_FIX = ("Sewage sludge: <strong>no longer</strong> on the permitted list — Resolution "
           "LP.6(17) (adopted 7 October 2022, in force generally 15 January 2023) removed it "
           "from Annex 1; no new dumping permits, and existing permits end by 31 May 2027 at "
           "the latest.")
SCOPE = (" The amendment binds Contracting Parties to the 1996 Protocol — a State party only "
         "to the 1972 Convention is not bound by the Protocol's Annex 1.")
ANNEX_IV = (" It is dumping law only: it does not change MARPOL Annex IV, which governs a "
            "ship's own sewage discharge.")


def _gov_note_date_drifts(d):
    for e in d["recently_updated"]:
        if e.get("date") == "2026-10-28" and "LP.6(17)" in e.get("note", ""):
            e["note"] = e["note"].replace("15 January 2023", "15 January 2024")
            return
    raise AssertionError("governed LP.6(17) note absent")


def _index_note_drifts(d):
    for e in d["recently_updated"]:
        if e.get("date") == "2026-10-28":
            e["note"] = e["note"] + " (hand-edited on the derived surface)"
            return
    raise AssertionError("generated index anchor absent")


def _record_cutoff_drifts(d):
    for k in ("authority", "rationale"):
        d[k] = d[k].replace("31 May 2027", "31 May 2028")


def _record_forgets_trap(d):
    d["known_traps_entries"] = []


def _source_row_drops_card(d):
    for s in d["sources"]:
        if s.get("source_id") == "SRC-IMO-LP6-17":
            s["used_by"] = [u for u in s["used_by"] if u != "meoclass1/QB1_A.html#q13"]
            return
    raise AssertionError("SRC-IMO-LP6-17 absent")


MUTATIONS = [
    # ---- REGRESSION ----------------------------------------------------------
    ("A", "CE Oral Tip: the shipped sentence put back (gated)",
     sub_in_file(GATED, TIP_FIX,
                 "Sewage sludge: on the permitted list under 1996 Protocol (subject to conditions).",
                 count=1),
     "no_sludge_taught_as_permitted:gated"),

    ("B", "reverse list: sludge back in the Annex 1 enumeration",
     sub_in_file(GATED, "Permitted materials include: dredged material, fish waste,",
                 "Permitted materials include: dredged material, sewage sludge, fish waste,",
                 count=1),
     "reverse_list_enumeration_excludes_sludge:gated"),

    ("C", "reverse list: the removal sentence turned round",
     sub_in_file(GATED, "<strong>Sewage sludge is no longer on the list.</strong>",
                 "<strong>Sewage sludge is on the list.</strong>", count=1),
     "reverse_list_states_removal:gated"),

    ("D", "60-second answer: sludge back in the permitted list",
     sub_in_file(GATED, "Annex 1 of the Protocol — dredged material, fish waste, some inert",
                 "Annex 1 of the Protocol — dredged material, sewage sludge, fish waste, some inert",
                 count=1),
     "no_sludge_taught_as_permitted:gated"),

    ("E", "60-second answer: the removal clause dropped",
     sub_in_file(GATED, "; sewage sludge was removed from Annex 1 by Resolution LP.6(17), in force "
                        "from 15 January 2023. They are",
                 ". They are", count=1),
     "s60_states_removal:gated"),

    # ---- DATES ---------------------------------------------------------------
    ("F", "body: adoption date given as entry into force",
     sub_in_file(GATED, "entered into force generally on 15 January 2023",
                 "entered into force generally on 7 October 2022", count=1),
     "every_entry_into_force_is_15_jan_2023:gated"),

    ("G", "CE tip: entry into force a near-miss date",
     sub_in_file(GATED, "in force generally 15 January 2023) removed it",
                 "in force generally 1 January 2023) removed it", count=1),
     "every_entry_into_force_is_15_jan_2023:gated"),

    ("H", "body: permit cut-off moved",
     sub_in_file(GATED, "expiry date, but not later than 31 May 2027",
                 "expiry date, but not later than 31 December 2027", count=1),
     "every_permit_cutoff_is_31_may_2027:gated"),

    ("I", "CE tip: permit cut-off moved",
     sub_in_file(GATED, "existing permits end by 31 May 2027 at the latest",
                 "existing permits end by 31 May 2028 at the latest", count=1),
     "every_permit_cutoff_is_31_may_2027:gated"),

    # I2-I4 are the escapes the independent review of 28 Oct 2026 demonstrated
    # against the first version of the gate (findings F1 and F2): a cut-off
    # moved onto one of the card's two other true dates, and an
    # entry-into-force date written before its verb.
    ("I2", "CE tip: permit cut-off moved onto the entry-into-force date",
     sub_in_file(GATED, "existing permits end by 31 May 2027 at the latest",
                 "existing permits end by 15 January 2023 at the latest", count=1),
     "every_permit_cutoff_is_31_may_2027:gated"),

    ("I3", "CE tip: permit cut-off moved onto the adoption date",
     sub_in_file(GATED, "existing permits end by 31 May 2027 at the latest",
                 "existing permits end by 7 October 2022 at the latest", count=1),
     "every_permit_cutoff_is_31_may_2027:gated"),

    ("I4", "body: a wrong entry-into-force date written before its verb",
     sub_in_file(GATED, "deleted it from Annex 1, and the amendment entered into force generally "
                        "on 15 January 2023.",
                 "deleted it from Annex 1; 15 January 2024 is when it entered into force.",
                 count=1),
     "every_entry_into_force_is_15_jan_2023:gated"),

    # I5-I7 and J2, K3 pin the escapes the re-check of 28 Oct 2026 found (R1,
    # R3): contradictory sentences ADDED beside correct text, which exact-phrase
    # limb checks cannot see.
    ("I5", "body: added sentence ending existing permits on entry into force",
     sub_in_file(GATED, "not later than 31 May 2027.",
                 "not later than 31 May 2027. Existing permits lapse on entry into force, "
                 "15 January 2023.", count=1),
     "every_permit_cutoff_is_31_may_2027:gated"),

    ("I6", "body: added 'effective' claim giving the adoption date",
     sub_in_file(GATED, "not later than 31 May 2027.",
                 "not later than 31 May 2027. The deletion became effective on 7 October 2022.",
                 count=1),
     "every_entry_into_force_is_15_jan_2023:gated"),

    ("I7", "body: added cut-off that never says 'permit'",
     sub_in_file(GATED, "not later than 31 May 2027.",
                 "not later than 31 May 2027. Dumping under existing authorisations may "
                 "continue until 31 December 2028.", count=1),
     "every_permit_cutoff_is_31_may_2027:gated"),

    # ---- SCOPE ---------------------------------------------------------------
    ("J", "treaty-scope limb deleted",
     sub_in_file(GATED, SCOPE, "", count=1),
     "scope_binds_protocol_parties_only:gated"),

    ("J2", "added sentence extending the amendment to 1972 Convention Parties",
     sub_in_file(GATED, "not bound by the Protocol's Annex 1.",
                 "not bound by the Protocol's Annex 1. It also binds Parties to the 1972 "
                 "Convention.", count=1),
     "scope_not_extended_to_1972_parties:gated"),

    ("K", "correction widened into a worldwide ban",
     sub_in_file(GATED, "removed it from Annex 1; no new dumping permits",
                 "removed it from Annex 1 worldwide; no new dumping permits", count=1),
     "not_taught_as_worldwide_ban:gated"),

    # Review finding F3: the first version only read sentences naming sludge.
    ("K2", "worldwide reach asserted in a sentence that does not name sludge",
     sub_in_file(GATED, "not bound by the Protocol's Annex 1.",
                 "not bound by the Protocol's Annex 1. The ban now applies to all IMO "
                 "Member States.", count=1),
     "not_taught_as_worldwide_ban:gated"),

    ("K3", "reg-box row widened to a worldwide deletion",
     sub_in_file(GATED, "sewage sludge deleted from Annex 1; no new permits",
                 "sewage sludge deleted from Annex 1 worldwide; no new permits", count=1),
     "not_taught_as_worldwide_ban:gated"),

    ("L", "MARPOL Annex IV separation dropped",
     sub_in_file(GATED, ANNEX_IV, "", count=1),
     "marpol_annex_iv_separated:gated"),

    # ---- CROSS-QUESTION ------------------------------------------------------
    ("M", "examiner cross-question answered Yes",
     sub_in_file(GATED, "permitted reverse list?”</em> — <strong>No.</strong>",
                 "permitted reverse list?”</em> — <strong>Yes.</strong>", count=1),
     "ce_tip_cross_question_answered_no:gated"),

    # ---- TWIN ----------------------------------------------------------------
    ("N", "SQ twin alone: sludge back in the enumeration",
     sub_in_file(TWIN, "Permitted materials include: dredged material, fish waste,",
                 "Permitted materials include: dredged material, sewage sludge, fish waste,",
                 count=1),
     "reverse_list_enumeration_excludes_sludge:twin"),

    ("O", "SQ twin drifts from the gated copy by one harmless byte",
     sub_in_file(TWIN, "Permitted materials include:", "Permitted materials include :", count=1),
     "twin_identical_to_gated"),

    # ---- CORPUS --------------------------------------------------------------
    ("P", "defect reappears on a page this record never touched",
     sub_in_file(SHEET, "London Convention — what does it cover?",
                 "London Convention — what does it cover? Sewage sludge is on the permitted "
                 "list under the 1996 Protocol.", count=1),
     "corpus_no_other_page_teaches_sludge_permitted"),

    # ---- OVER-CORRECTION -----------------------------------------------------
    ("Q", "blanket substitution wipes QB3_C's correct Annex VI text",
     sub_in_file(QB3C, "Sewage sludge and sludge oil generated during normal operation",
                 "Sludge oil generated during normal operation", count=0),
     "qb3c_annex_vi_sludge_burning_survives"),

    # ---- RECORD --------------------------------------------------------------
    ("R", "stamp reverted to v1.0",
     sub_in_file(GATED, "QB1 · Q13 · v1.1", "QB1 · Q13 · v1.0", count=1),
     "stamp_records_correction"),

    ("S", "governed changelog note: entry-into-force year drifts",
     edit_json(GOV, _gov_note_date_drifts),
     "governed_note_states_removal"),

    ("T", "governed correct, DERIVED index hand-edited",
     edit_json(IDX, _index_note_drifts),
     "generated_index_matches_governed_changelog"),

    ("U", "trap 141 made GREP: SKIP",
     sub_in_file(TRAPS, "GREP: on the permitted list under 1996 Protocol",
                 "GREP: SKIP", count=1),
     "trap_141_greps_the_shipped_phrase"),

    ("V", "trap 141 forgets follow-up B (a tolerated site)",
     sub_in_file(TRAPS, "- **B.** `oralnotes/simon-notes-p8.html`",
                 "- `oralnotes/simon-notes-p8.html`", count=1),
     "trap_141_logs_open_followups"),

    ("W", "record restated with the wrong permit cut-off",
     edit_json(RECORD, _record_cutoff_drifts),
     "record_states_the_proposition"),

    ("X", "record detached from trap 141",
     edit_json(RECORD, _record_forgets_trap),
     "record_cites_trap_141"),

    ("Y", "source row no longer names the card",
     edit_json(REGISTRY, _source_row_drops_card),
     "sources_registered_for_the_card"),

    # ---- NON-VACUITY ---------------------------------------------------------
    ("Z", "remove the target card from the census input",
     sub_in_file(TWIN, '<div class="q-card" id="q13"', '<div class="q-card" id="q13x"', count=1),
     "target_card_present"),
]


def main() -> int:
    return run_suite("CORR-LP617-SEWAGE-SLUDGE-20261028 mutation suite", PROBE,
                     MUTATIONS, WATCHED)


if __name__ == "__main__":
    sys.exit(main())
