#!/usr/bin/env python3
"""
Mutation suite for CORR-IGF-CHAIN-20260905 (the IGF six-amendment closure).

`validate_correction_igfchain.py` reports 22 green checks. Green output is
indistinguishable from a validator that reads nothing, so every proposition is
attacked here and each mutation must trip the check that OWNS it -- never a
digest pin, which fires on any byte change at all.

THE GATE FOUND TWO REAL DEFECTS BEFORE THIS SUITE EXISTED
-----------------------------------------------------------
Its first run was red twice, and both reds were content, not gate:

*   `base_not_counted_as_amendment_q14` -- the clarifier that MSC.391(95) is
    the ADOPTING resolution and not one of the six had been written into q15
    and not into q14. A reader seeing "six" on one card and no statement about
    the base on the other is one step from correcting six to seven.
*   `footer_says_six_not_five_q15` -- the check was reading the card's
    `q-version` STAMP, which says, correctly, "closure claim named five IGF
    amendments and omitted MSC.458(101)". A version stamp DESCRIBES the defect
    it records; a negative check that reads it reports the changelog as the
    defect. The fix was to bound `footer_of` at the paragraph's `</p>` instead
    of running to the end of the card.

MUTATION A IS THE ONE THIS RECORD EXISTS FOR
----------------------------------------------
It drops MSC.458(101) back out of the q15 enumeration and restores "five" --
the exact state of the corpus this morning, and the state a careless revert of
this one paragraph reproduces. It must be caught by the ENUMERATION check, not
by the count check, which is why the two are separate: the original defect was
a wrong COUNT that a list was then edited to agree with, so a gate that tested
only one of them would have passed the corpus that shipped.

MUTATIONS G AND H ATTACK THE CUSTODY, NOT THE PROSE
-----------------------------------------------------
A footer that NAMES six resolutions the corpus does not hold is no more
reproducible than one that names five -- and that is precisely how this defect
survived its first correction, from four to five, with two of the five named
but unheld. G removes a resolution from the true-source manifest and H
corrupts a digest; the prose is untouched in both and must still go red.
"""

from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import (                    # noqa: E402
    edit_json, run_suite, sub_in_file)

PAGE = REPO / "meoclass1/QB7_D.html"
MANIFEST = HERE / "correction_corr_igf_chain_20260905_manifest.json"
REGISTRY = REPO / "docs/sources/MIW_SOURCE_REGISTRY.json"
INDEX = REPO / "meoclass1/qb_content_index.json"
TRAPS = REPO / "meoclass1/known_traps.md"
TS_MANIFEST = pathlib.Path(
    r"F:\RulesApp-Local-Input\true-source\03-imo-instruments\IGF-Code"
    r"\manifest.json")
PROBE = "validate_correction_igfchain.py"

Q15_LIST = ("All <strong>six</strong> IGF amendment resolutions in force or "
            "adopted &mdash; <strong>MSC.422(98)</strong>, "
            "<strong>MSC.458(101)</strong>, <strong>MSC.475(102)</strong>")
Q15_LIST_SHORT = ("The <strong>five</strong> IGF amendment resolutions in "
                  "force or adopted &mdash; <strong>MSC.422(98)</strong>, "
                  "<strong>MSC.475(102)</strong>")


def edit_bom_json(path, mutate):
    """`edit_json` for a file that carries a UTF-8 BOM.

    The true-source IGF manifest is PowerShell-emitted and BOM-prefixed, and
    the shared `edit_json` decodes with plain utf-8 -- so mutations G, H and I
    CRASHED on their first run with "Unexpected UTF-8 BOM". A crash is not a
    catch: the suite reported nothing about whether the custody checks work.
    Handled locally rather than by changing `oral_content_mutation`, which
    every other suite in this repository depends on and which no other suite
    needs this for. The Snapshot custody restores raw bytes either way, so the
    BOM survives the round trip regardless of what this writes.
    """
    def apply():
        raw = pathlib.Path(path).read_bytes()
        data = json.loads(raw.decode("utf-8-sig"))
        mutate(data)
        body = json.dumps(data, indent=1, ensure_ascii=False) + "\n"
        pathlib.Path(path).write_bytes(b"\xef\xbb\xbf" + body.encode("utf-8"))
    return apply


def _set_status(value):
    def mutate(d):
        d["status"] = value
    return mutate


def _drop_ts_file(name):
    def mutate(d):
        d["files"] = [f for f in d["files"] if name not in f["path"]]
    return mutate


def _corrupt_ts_digest(name):
    def mutate(d):
        for f in d["files"]:
            if name in f["path"]:
                f["sha256"] = "0" * 64
    return mutate


def _drop_registry_row(sid):
    def mutate(d):
        d["sources"] = [s for s in d["sources"] if s["source_id"] != sid]
    return mutate


def _blank_registry_digest(sid):
    def mutate(d):
        for s in d["sources"]:
            if s["source_id"] == sid:
                s["sha256"] = ""
    return mutate


MUTATIONS = [
    # ---- the regression this record exists to make impossible -----------
    ("A", "drop MSC.458(101) back out of the q15 enumeration and restore five",
     sub_in_file(PAGE, Q15_LIST, Q15_LIST_SHORT),
     "footer_names_msc458_q15"),

    ("B", "leave the q15 list complete but regress the COUNT WORD to five",
     sub_in_file(PAGE,
                 "All <strong>six</strong> IGF amendment resolutions in force",
                 "The <strong>five</strong> IGF amendment resolutions in force"),
     "footer_says_six_not_five_q15"),

    ("C", "regress the q14 count word",
     sub_in_file(PAGE,
                 "All <strong>six</strong> IGF amendment resolutions were "
                 "opened and read",
                 "All <strong>five</strong> IGF amendments were opened and read"),
     "footer_says_six_not_five_q14"),

    ("D", "delete the base-resolution clarifier from q14, so a reader is one "
          "step from correcting six to seven",
     sub_in_file(PAGE,
                 "&mdash; MSC.391(95) adopts the Code itself and is not one "
                 "of them:", ":"),
     "base_not_counted_as_amendment_q14"),

    ("E", "delete the base-resolution clarifier from q15",
     sub_in_file(PAGE,
                 "MSC.391(95) is the resolution that adopts the Code itself "
                 "and is not one of the six. ", ""),
     "base_not_counted_as_amendment_q15"),

    ("F", "delete the substantive BDN conclusion from q15, leaving a closure "
          "claim that closes over nothing",
     sub_in_file(PAGE,
                 "and <strong>none amends the Bunker Delivery Note "
                 "annex</strong>", "and that is all"),
     "bdn_conclusion_retained_q15"),

    # ---- the custody behind the claim -----------------------------------
    ("G", "remove MSC.475(102) from the true-source manifest, so the footer "
          "names a resolution the corpus does not hold",
     edit_bom_json(TS_MANIFEST, _drop_ts_file("MSC.475(102)")),
     "held_all_six_amendments_plus_base"),

    ("H", "corrupt the held digest for MSC.524(106)",
     edit_bom_json(TS_MANIFEST, _corrupt_ts_digest("MSC.524(106)")),
     "held_all_six_amendments_plus_base"),

    ("I", "mark the true-source package incomplete again",
     edit_bom_json(TS_MANIFEST, lambda d: d.__setitem__("constructionStatus",
                                                    "constructed")),
     "true_source_marked_complete"),

    # ---- the registry ----------------------------------------------------
    ("J", "delete the MSC.458(101) registry row -- the resolution whose "
          "absence from the registry is what made the omission invisible",
     edit_json(REGISTRY, _drop_registry_row("SRC-IGF-MSC458-101")),
     "registry_has_all_six_igf_rows"),

    ("K", "blank a registry row's digest, so the row names an instrument it "
          "cannot prove it read",
     edit_json(REGISTRY, _blank_registry_digest("SRC-IGF-MSC422-98")),
     "registry_rows_carry_digests"),

    # ---- the record itself ----------------------------------------------
    ("L", "mark the correction record superseded",
     edit_json(MANIFEST, _set_status("SUPERSEDED")),
     "correction_record_authorised"),

    ("M", "break the supersession chain by falsifying a pre-edit digest",
     edit_json(MANIFEST, lambda d: d["cards"][0].__setitem__(
         "pre_edit_digest", "f" * 64)),
     "supersession_chain_unbroken"),

    ("N", "move the corpus totals",
     edit_json(INDEX, lambda d: d.__setitem__("total_questions", 999)),
     "canonical_questions_unchanged"),

    # ---- the lesson, not just the fix -----------------------------------
    ("O", "drop the known_traps declaration, so the defect class is repaired "
          "in two cards and recorded nowhere",
     edit_json(MANIFEST, lambda d: d.__setitem__("known_traps_entries", [])),
     "known_traps_entry_declared_and_exists"),

    ("P", "gut entry 81 of the resolution it exists to name",
     sub_in_file(TRAPS, "MSC.458(101)", "one of the amendments"),
     "known_traps_entry_carries_the_lesson"),
]

WATCHED = [PAGE, MANIFEST, REGISTRY, INDEX, TS_MANIFEST, TRAPS]

if __name__ == "__main__":
    raise SystemExit(run_suite(
        "mutation suite: CORR-IGF-CHAIN-20260905 (IGF six-amendment closure)",
        PROBE, MUTATIONS, WATCHED))
