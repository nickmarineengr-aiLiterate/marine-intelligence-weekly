#!/usr/bin/env python3
"""Mutation suite for CORR-LP617-QB9A-Q7-20261030 (trap 141 follow-up A).

Every mutation names the PROPOSITION check it must trip; the shared harness
refuses a digest pin as a catch. Probes only validate_correction_lp617_qb9a.py
(validate_corrections owns the pins and is exercised by corrections_mutate;
the corpus re-infection scan belongs to correction_lp617_mutate).

REGRESSION (A-D): the shipped example put back, sludge back in the example on
  its own, the removal sentence turned round, the permit rule dropped.
DATES (E-G): adoption given as entry into force, a near-miss entry-into-force
  date, the permit cut-off moved.
SCOPE (H, H2, H3): a worldwide ban asserted in the London limb and in the CE
  Oral Tip; LP.6(17) said to bind 1972 Convention Parties (independent review F1).
REG-BOX (I): the LP.6(17) row removed.
RECORD (J-Q): the stamp, the governed note, the derived index, trap 141's open
  item rewritten, its closure dropped, the record's proposition, its T4a
  ownership chain, a source row.
NON-VACUITY (R, S): the target card leaves the census input; an SQ twin appears.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import edit_json, run_suite, sub_in_file  # noqa: E402

PAGE = REPO / "meoclass1/QB9_A.html"
TWIN = REPO / "SQ/QB9_A.html"
TRAPS = REPO / "meoclass1/known_traps.md"
GOV = HERE / "qb_content_index_governed.json"
IDX = REPO / "meoclass1/qb_content_index.json"
RECORD = HERE / "correction_corr_lp617_qb9a_q7_20261030_manifest.json"
REGISTRY = REPO / "docs/sources/MIW_SOURCE_REGISTRY.json"

PROBE = "validate_correction_lp617_qb9a.py"
WATCHED = [PAGE, TWIN, TRAPS, GOV, IDX, RECORD, REGISTRY]

EXAMPLE = "(such as dredged material, fish waste, or organic material of natural origin)"


def _gov_note_cutoff_drifts(d):
    for e in d["recently_updated"]:
        if (e.get("date") == "2026-10-30" and "QB9_A" in e.get("note", "")
                and "LP.6(17)" in e.get("note", "")):
            e["note"] = e["note"].replace("31 May 2027", "31 May 2028")
            return
    raise AssertionError("governed QB9_A note absent")


def _index_note_drifts(d):
    for e in d["recently_updated"]:
        if e.get("date") == "2026-10-30":
            e["note"] = e["note"] + " (hand-edited on the derived surface)"
            return
    raise AssertionError("generated index anchor absent")


def _record_eif_drifts(d):
    for k in ("authority", "rationale"):
        d[k] = d[k].replace("15 January 2023", "15 January 2024")


def _record_drops_supersession(d):
    d["cards"][0].pop("supersedes")


def _source_row_drops_card(d):
    for s in d["sources"]:
        if s.get("source_id") == "SRC-IMO-STATUS-TREATIES-VOL2-2026-09-30":
            s["used_by"] = [u for u in s["used_by"] if u != "meoclass1/QB9_A.html#q7"]
            return
    raise AssertionError("status row absent")


#: q7's own CE Oral Tip (the strong label alone recurs on other cards).
TIP = ("CE Oral Tip (Kochi MMD):</strong> Examiner Simon regularly tests candidates on the "
       "electronic data exchange amendments under FAL.")


MUTATIONS = [
    # ---- REGRESSION ----------------------------------------------------------
    ("A", "the shipped example put back",
     sub_in_file(PAGE, EXAMPLE,
                 "(such as dredged material, sewage sludge, or organic waste of natural origin)",
                 count=1),
     "shipped_wrong_phrase_absent"),

    ("B", "sludge back in the example on its own",
     sub_in_file(PAGE, EXAMPLE,
                 "(such as dredged material, fish waste, sewage sludge, or organic material of "
                 "natural origin)", count=1),
     "reverse_list_example_excludes_sludge"),

    ("C", "the removal sentence turned round",
     sub_in_file(PAGE, "<strong>Sewage sludge is no longer on that list:</strong>",
                 "<strong>Sewage sludge is still on that list:</strong>", count=1),
     "reverse_list_states_removal"),

    ("D", "the permit rule dropped",
     sub_in_file(PAGE, " No new permits may be issued for dumping sewage sludge; a permit already "
                       "issued may be kept until its expiry date, but not later than 31 May 2027.",
                 "", count=1),
     "no_new_permits_and_cutoff"),

    # ---- DATES ---------------------------------------------------------------
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

    # ---- SCOPE ---------------------------------------------------------------
    ("H", "the removal widened into a worldwide ban",
     sub_in_file(PAGE, "deleted it from Annex 1, and the amendment",
                 "deleted it from Annex 1 worldwide, and the amendment", count=1),
     "not_taught_as_worldwide_ban"),

    # ---- REG-BOX -------------------------------------------------------------
    # Independent review F1 (30 Oct 2026), probes P1 and P2: outside the London limb.
    ("H2", "a worldwide ban asserted in the CE Oral Tip",
     sub_in_file(PAGE, TIP,
                 "CE Oral Tip (Kochi MMD):</strong> Since Resolution LP.6(17), dumping "
                 "sewage sludge at sea is banned worldwide. Examiner Simon regularly tests "
                 "candidates on the electronic data exchange amendments under FAL.", count=1),
     "not_taught_as_worldwide_ban"),

    ("H3", "LP.6(17) said to bind 1972 Convention Parties",
     sub_in_file(PAGE, TIP,
                 "CE Oral Tip (Kochi MMD):</strong> LP.6(17) also binds every State party "
                 "to the 1972 Convention. Examiner Simon regularly tests candidates on the "
                 "electronic data exchange amendments under FAL.", count=1),
     "scope_not_extended_to_1972_parties"),

    ("I", "the LP.6(17) reg-box row removed",
     sub_in_file(PAGE, '<div class="reg-item"><span class="reg-code">Resolution LP.6(17)</span>'
                       '<span class="reg-desc">Adopted 7 Oct 2022, in force 15 Jan 2023 — sewage '
                       'sludge deleted from Annex 1; no new permits; existing permits not beyond '
                       '31 May 2027</span></div>', "", count=1),
     "reg_box_has_lp617_row"),

    # ---- RECORD --------------------------------------------------------------
    ("J", "stamp reverted to v1.1",
     sub_in_file(PAGE, "QB9_A · Q7 · v1.2", "QB9_A · Q7 · v1.1", count=1),
     "stamp_records_correction"),

    ("K", "governed changelog note: permit cut-off drifts",
     edit_json(GOV, _gov_note_cutoff_drifts),
     "governed_note_states_removal"),

    ("L", "governed correct, DERIVED index hand-edited",
     edit_json(IDX, _index_note_drifts),
     "generated_index_matches_governed_changelog"),

    ("M", "trap 141's open follow-up A rewritten",
     sub_in_file(TRAPS, "- **A.** `QB9_A` Q7", "- **A.** (closed) `QB9_A` Q7", count=1),
     "trap_141_still_logs_followup_a"),

    ("N", "trap 141's closure of A dropped",
     sub_in_file(TRAPS, "`QB9_A` Q7 corrected by\nCORR-LP617-QB9A-Q7-20261030.",
                 "`QB9_A` Q7 corrected.", count=1),
     "trap_141_closes_followup_a"),

    ("O", "record restated with the wrong entry-into-force year",
     edit_json(RECORD, _record_eif_drifts),
     "record_states_the_proposition"),

    ("P", "record no longer continues the T4a pin",
     edit_json(RECORD, _record_drops_supersession),
     "record_continues_the_t4a_pin"),

    ("Q", "source row no longer names the card",
     edit_json(REGISTRY, _source_row_drops_card),
     "sources_registered_for_the_card"),

    # ---- NON-VACUITY ---------------------------------------------------------
    ("R", "remove the target card from the census input",
     sub_in_file(PAGE, '<div class="q-card" id="q7"', '<div class="q-card" id="q7x"', count=1),
     "target_card_present"),
]


def _twin_appears():
    """S: an SQ twin appears without its own identity check."""
    def apply():
        TWIN.write_bytes(PAGE.read_bytes())
    return apply


def main() -> int:
    muts = list(MUTATIONS)
    muts.append(("S", "an SQ twin appears", _twin_appears(), "no_sq_twin_exists"))
    return run_suite("CORR-LP617-QB9A-Q7-20261030 mutation suite", PROBE, muts, WATCHED)


if __name__ == "__main__":
    sys.exit(main())
