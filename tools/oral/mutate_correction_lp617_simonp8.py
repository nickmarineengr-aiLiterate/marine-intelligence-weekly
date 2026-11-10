#!/usr/bin/env python3
"""Mutation suite for CORR-LP617-SIMON-P8-20261030 (trap 141 follow-up B).

Every mutation names the PROPOSITION check it must trip; the shared harness
refuses a digest pin as a catch. Probes only validate_correction_lp617_simonp8.py
(validate_corrections owns the governed-artefact pin; the corpus re-infection
scan belongs to correction_lp617_mutate).

REGRESSION (A-D): the shipped list put back, sludge back in the list on its
  own, the removal line turned round, the permit rule dropped.
DATES (E-G): adoption given as entry into force, a near-miss reg-box date, the
  permit cut-off moved.
SCOPE (H, H2, H3): a worldwide ban asserted in the section and in the Simon
  tip; LP.6(17) said to bind 1972 Convention Parties (independent review F1). REG-BOX (I): the LP.6(17) row removed.
ISOLATION (J): a neighbouring card moves under this record.
RECORD (K-S): the stamp, the governed note, the derived index, trap 141's open
  item rewritten, its closure dropped, the record's proposition, its parent,
  its expected text, a source row.
NON-VACUITY (T, U): the target card leaves the census input; an SQ twin appears.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import edit_json, run_suite, sub_in_file  # noqa: E402

PAGE = REPO / "meoclass1/oralnotes/simon-notes-p8.html"
TWIN = REPO / "SQ/simon-notes-p8.html"
TRAPS = REPO / "meoclass1/known_traps.md"
GOV = HERE / "qb_content_index_governed.json"
IDX = REPO / "meoclass1/qb_content_index.json"
RECORD = HERE / "correction_corr_lp617_simon_p8_20261030_manifest.json"
REGISTRY = REPO / "docs/sources/MIW_SOURCE_REGISTRY.json"

PROBE = "validate_correction_lp617_simonp8.py"
WATCHED = [PAGE, TWIN, TRAPS, GOV, IDX, RECORD, REGISTRY]

#: State-agnostic anchor: present before and after the C1 list rewrite.
LIST = "<li>Dredged material; fish waste"
REMOVAL = ("<li><strong>Sewage sludge is no longer on the list:</strong> Resolution LP.6(17), "
           "adopted on 7 October 2022, deleted it from Annex 1, and the amendment entered into "
           "force on 15 January 2023. No new permits may be issued for dumping sewage sludge; a "
           "permit already issued may be kept until its expiry date, but not later than 31 May "
           "2027.</li>")
#: N3's tip only (another card's tip shares the strong label).
TIP = ('typically asks:</strong> "What is the difference between the London Dumping '
       'Convention and the 1996 Protocol?"')


def _gov_note_eif_drifts(d):
    for e in d["recently_updated"]:
        if e.get("files") == ["oralnotes/simon-notes-p8.html"]:
            e["note"] = e["note"].replace("15 January 2023", "15 January 2024")
            return
    raise AssertionError("governed p8 note absent")


def _index_note_drifts(d):
    for e in d["recently_updated"]:
        if e.get("files") == ["oralnotes/simon-notes-p8.html"]:
            e["note"] = e["note"] + " (hand-edited on the derived surface)"
            return
    raise AssertionError("generated index anchor absent")


def _record_cutoff_drifts(d):
    for k in ("authority", "rationale"):
        d[k] = d[k].replace("31 May 2027", "31 May 2028")


def _record_wrong_parent(d):
    d["governed_artefacts"][0]["governing_correction"] = "CORR-LP617-QB9A-Q7-20261030"


def _record_expected_text_drifts(d):
    ga = d["governed_artefacts"][0]
    ga["expected_text_after"] = ga["expected_text_after"].replace("31 May 2027", "31 May 2028")


def _source_row_drops_card(d):
    for s in d["sources"]:
        if s.get("source_id") == "SRC-IMO-LP6-17":
            s["used_by"] = [u for u in s["used_by"]
                            if u != "meoclass1/oralnotes/simon-notes-p8.html#n3"]
            return
    raise AssertionError("SRC-IMO-LP6-17 absent")


def _twin_appears():
    def apply():
        TWIN.write_bytes(PAGE.read_bytes())
    return apply


MUTATIONS = [
    ("A", "the shipped list put back",
     sub_in_file(PAGE, LIST, "<li>Dredged material; sewage sludge; fish waste", count=1),
     "shipped_wrong_phrase_absent"),
    ("B", "sludge back in the list on its own",
     sub_in_file(PAGE, LIST, "<li>Dredged material; fish waste; sewage sludge", count=1),
     "annex1_list_excludes_sludge"),
    ("C", "the removal line turned round",
     sub_in_file(PAGE, "<strong>Sewage sludge is no longer on the list:</strong>",
                 "<strong>Sewage sludge is still on the list:</strong>", count=1),
     "annex1_section_states_removal"),
    ("D", "the permit rule dropped",
     sub_in_file(PAGE, " No new permits may be issued for dumping sewage sludge; a permit already "
                       "issued may be kept until its expiry date, but not later than 31 May 2027.",
                 "", count=1),
     "no_new_permits_and_cutoff"),
    ("E", "adoption date given as entry into force",
     sub_in_file(PAGE, "the amendment entered into force on 15 January 2023",
                 "the amendment entered into force on 7 October 2022", count=1),
     "every_entry_into_force_is_15_jan_2023"),
    ("F", "a near-miss entry-into-force date in the reg-box",
     sub_in_file(PAGE, "Adopted 7 Oct 2022, in force 15 Jan 2023 — sewage sludge",
                 "Adopted 7 Oct 2022, in force 15 Jan 2024 — sewage sludge", count=1),
     "every_entry_into_force_is_15_jan_2023"),
    ("G", "permit cut-off moved",
     sub_in_file(PAGE, "until its expiry date, but not later than 31 May 2027.",
                 "until its expiry date, but not later than 31 May 2028.", count=1),
     "every_permit_cutoff_is_31_may_2027"),
    ("H", "the removal widened into a worldwide ban",
     sub_in_file(PAGE, "deleted it from Annex 1, and the amendment",
                 "deleted it from Annex 1 worldwide, and the amendment", count=1),
     "not_taught_as_worldwide_ban"),
    # Independent review F1 (30 Oct 2026), probes P5b and P6: outside the Annex 1 section.
    ("H2", "a worldwide ban asserted in the Simon tip",
     sub_in_file(PAGE, TIP, TIP + "Since Resolution LP.6(17) removed it, sewage sludge "
                                  "dumping is now banned worldwide. ", count=1),
     "not_taught_as_worldwide_ban"),
    ("H3", "LP.6(17) said to bind 1972 Convention Parties",
     sub_in_file(PAGE, REMOVAL, REMOVAL + "<li>LP.6(17) also binds every State party to the "
                                          "1972 Convention.</li>", count=1),
     "scope_not_extended_to_1972_parties"),
    ("I", "the LP.6(17) reg-box row removed",
     sub_in_file(PAGE, '<div class="reg-item"><span class="reg-code">Resolution LP.6(17)</span>',
                 '<div class="reg-item"><span class="reg-code">Resolution</span>', count=1),
     "reg_box_has_lp617_row"),
    ("J", "a neighbouring card (N4) moves under this record",
     sub_in_file(PAGE, "<li><strong>Full name:</strong> Basel Convention",
                 "<li><strong>Full name:</strong> The Basel Convention", count=1),
     "other_cards_unchanged"),
    ("K", "N3 stamp reverted to v1.0",
     sub_in_file(PAGE, "simon-notes-p8 · N3 · v1.1", "simon-notes-p8 · N3 · v1.0",
                 count=1),
     "stamp_records_correction"),
    ("L", "governed changelog note: entry-into-force year drifts",
     edit_json(GOV, _gov_note_eif_drifts), "governed_note_states_removal"),
    ("M", "governed correct, DERIVED index hand-edited",
     edit_json(IDX, _index_note_drifts), "generated_index_matches_governed_changelog"),
    ("N", "trap 141's open follow-up B rewritten",
     sub_in_file(TRAPS, "- **B.** `oralnotes/simon-notes-p8.html`",
                 "- **B.** (closed) `oralnotes/simon-notes-p8.html`", count=1),
     "trap_141_still_logs_followup_b"),
    ("O", "trap 141's closure of B dropped",
     sub_in_file(TRAPS, "card N3\ncorrected by CORR-LP617-SIMON-P8-20261030.",
                 "card N3\ncorrected.", count=1),
     "trap_141_closes_followup_b"),
    ("P", "record restated with the wrong permit cut-off",
     edit_json(RECORD, _record_cutoff_drifts), "record_states_the_proposition"),
    ("Q", "record names the wrong parent correction",
     edit_json(RECORD, _record_wrong_parent), "record_governs_the_page_as_propagation"),
    ("R", "record's expected text no longer what is live",
     edit_json(RECORD, _record_expected_text_drifts), "record_expected_text_is_live"),
    ("S", "source row no longer names the card",
     edit_json(REGISTRY, _source_row_drops_card), "sources_registered_for_the_card"),
    ("T", "remove the target card from the census input",
     sub_in_file(PAGE, '<div class="note-card" id="n3"', '<div class="note-card" id="n3x"', count=1),
     "target_card_present"),
    ("U", "an SQ twin appears", _twin_appears(), "no_sq_twin_exists"),
]


def main() -> int:
    return run_suite("CORR-LP617-SIMON-P8-20261030 mutation suite", PROBE, MUTATIONS, WATCHED)


if __name__ == "__main__":
    sys.exit(main())
