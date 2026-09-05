#!/usr/bin/env python3
"""
Mutation suite for CORR-BMP-EDITION-PROP-20260905 (the BMP MS edition sweep).

`validate_correction_bmpprop.py` reports 25 green checks. Green output is
indistinguishable from a validator that reads nothing, so every proposition the
record rests on is attacked here, and each mutation must trip the check that
OWNS it -- never a digest pin, which fires on any byte change at all.

THE GATE HAD ALREADY EARNED ITS KEEP BEFORE THIS SUITE EXISTED
---------------------------------------------------------------
Its first three runs were red, and all three reds were defects in the GATE:

*   `_quoted_spans` was copied from the T2C gate, which serves HTML pages and
    therefore knows only CURLY quotes. `known_traps.md` is Markdown and rejects
    the wrong label as **"the 2026 edition"** -- straight quotes -- so the gate
    reported the trap entry that TEACHES AGAINST the defect as an instance of
    it. Same shape as the E1 lesson: a guard spelled for one form of a mark is
    blind to the other.
*   Then it fired on trap 80's own `GREP: SKIP` marker, which quotes the label
    in a Markdown CODE SPAN. The marker that documents the exemption was
    flagged by the sweep the exemption exists for.
*   Then it fired on "no 2025/2026 edition" in two past-paper analyses, about
    the HSSC Survey Guidelines. The pattern was not BMP-scoped at all. A sweep
    that fires on unrelated publications teaches the next reader that its red
    output is noise, and a gate nobody believes is a gate nobody reads.

The fourth red was a real content finding: the version stamps this correction
itself wrote said "not a 2026 edition" OUTSIDE any quotation, so the corpus's
own repair asserted the label it was removing. They now quote it.

MUTATION F IS THE ONE THIS RECORD EXISTS FOR
---------------------------------------------
It restores the exact wording the 31 August family left behind. That is not a
hypothetical regression: it is the state of the corpus five hours ago, and the
state a careless `git checkout` of any one of these four pages reproduces.

AND THREE GUARD AGAINST OVER-CORRECTION, NOT UNDER-CORRECTION
--------------------------------------------------------------
*   MUTATION H strips the BMP5 technique content the cards exist to teach. The
    sweep's whole discipline is that only the LABEL changes; a pass that
    deletes the substance is the failure a "did the wrong label go?" check
    cannot see.
*   MUTATION I moves QB4_H#q13, the PRIMARY, which belongs to another record.
    A propagation that edits the primary has stopped being a propagation and
    two records then claim the same bytes.
*   MUTATION J removes the label entirely instead of correcting it, leaving a
    card that says nothing about the edition at all. Absence of the wrong
    answer is not presence of the right one.
"""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import (                    # noqa: E402
    edit_json, run_suite, sub_in_file)

QB4_H = REPO / "meoclass1/QB4_H.html"
QB4_B = REPO / "meoclass1/QB4_B.html"
QB9_A = REPO / "meoclass1/QB9_A.html"
QB9_B = REPO / "meoclass1/QB9_B.html"
TRAPS = REPO / "meoclass1/known_traps.md"
MANIFEST = HERE / "correction_corr_bmp_edition_prop_20260905_manifest.json"
INDEX = REPO / "meoclass1/qb_content_index.json"
PROBE = "validate_correction_bmpprop.py"

# The corrected currentness sentence, shared by four cards.
NOTE_NEW = ("the current edition is the <strong>1st Edition (2025)</strong>, "
            "updated during 2026")
NOTE_OLD = "the current edition is <strong>2026</strong>"


def _set_status(value):
    def mutate(d):
        d["status"] = value
    return mutate


def _drop_q13_pin(d):
    d["invariants"]["q13_untouched_digest"] = "0" * 64


def _move_totals(d):
    d["total_questions"] = 999


def _reclassify_primary(d):
    for c in d["cards"]:
        if c["anchor"] == "q11":
            c["classification"] = "PROPAGATED_FACT_CORRECTION"


def _break_artefact(d):
    d["artefacts"][0]["path"] = "meoclass1/no_such_file.md"


MUTATIONS = [
    # ---- the regression this record exists to make impossible -----------
    ("A", "regress the QB4_H#q2 currentness note to the 31 August wording",
     sub_in_file(QB4_H, NOTE_NEW, NOTE_OLD),
     "note_carries_publisher_label_qb4_h_q2"),

    ("B", "regress the QB4_B#q16 currentness note",
     sub_in_file(QB4_B, NOTE_NEW, NOTE_OLD),
     "note_carries_publisher_label_qb4_b_q16"),

    ("C", "regress the QB9_A#q9 currentness note",
     sub_in_file(QB9_A, NOTE_NEW, NOTE_OLD),
     "note_carries_publisher_label_qb9_a_q9"),

    ("D", "regress the QB9_B#q5 currentness note",
     sub_in_file(QB9_B, NOTE_NEW, NOTE_OLD),
     "note_carries_publisher_label_qb9_b_q5"),

    ("E", "regress the QB4_H#q2 reg-box description",
     sub_in_file(QB4_H,
                 "Industry guidance, 1st Edition (2025) as updated in 2026;",
                 "Industry guidance, current edition 2026;"),
     "regbox_carries_publisher_label_qb4_h_q2"),

    ("F", "regress the QB4_H#q11 source-confidence footer",
     sub_in_file(QB4_H,
                 "the current BMP MS edition is the 1st Edition (2025) as "
                 "updated in 2026 &mdash; there is no second edition.",
                 "the current BMP MS edition is 2026."),
     "source_confidence_label_qb4_h_q11"),

    # ---- the negative sweep, attacked through the quote device ----------
    ("G", "reinstate the rejected label as an ASSERTION on a candidate page, "
          "outside any quotation, which is what a careless restore produces",
     sub_in_file(QB9_B, "</body>",
                 "<p>BMP Maritime Security is now at the 2026 edition.</p>"
                 "</body>", 1),
     "no_candidate_surface_asserts_a_2026_edition"),

    # ---- over-correction ------------------------------------------------
    ("H", "strip the BMP5 technique content the cards exist to preserve",
     sub_in_file(QB4_B, "BMP5", "the earlier publication"),
     "technique_retained_qb4_b_q16"),

    ("I", "move the PRIMARY, which belongs to CORR-GPT-T2C-CURRENCY-20260905",
     sub_in_file(QB4_H,
                 "&ldquo;Actions on Boarding by Activists&rdquo;",
                 "&ldquo;Actions on Boarding&rdquo;"),
     "q13_untouched"),

    ("J", "delete the label instead of correcting it, so the card says "
          "nothing about the edition at all",
     sub_in_file(QB9_A, NOTE_NEW, "the edition is not stated here"),
     "note_carries_publisher_label_qb9_a_q9"),

    # ---- the study document --------------------------------------------
    ("K", "reinstate trap 54's assertion that a second edition followed",
     sub_in_file(TRAPS,
                 "It remains the **1st Edition (2025)**,\nupdated during 2026",
                 "A **second edition followed in 2026**. It was\nnot updated"),
     "trap_54_no_longer_asserts_a_second_edition"),

    ("L", "erase the record of WHICH correction closed the reported gap, "
          "leaving trap 80 saying the sweep never happened",
     sub_in_file(TRAPS, "CORR-BMP-EDITION-PROP-20260905", "a later pass"),
     "trap_80_records_the_sweep"),

    # ---- the record itself ----------------------------------------------
    ("M", "mark the correction record superseded",
     edit_json(MANIFEST, _set_status("SUPERSEDED")),
     "correction_record_authorised"),

    ("N", "break the supersession chain by falsifying a pre-edit digest",
     edit_json(MANIFEST, lambda d: d["cards"][0].__setitem__(
         "pre_edit_digest", "f" * 64)),
     "supersession_chain_unbroken"),

    ("O", "blank the q13 pin, so the primary could move unnoticed",
     edit_json(MANIFEST, _drop_q13_pin),
     "q13_untouched"),

    ("P", "move the corpus totals",
     edit_json(INDEX, _move_totals),
     "canonical_questions_unchanged"),

    # ---- the record's INFORMATIONAL fields ------------------------------
    # oral_manifest's field table is closed BECAUSE a field no validator reads
    # is decoration. These three prove the gate reads them. The corpus-wide
    # auditor found all three defects in this record; no per-correction gate
    # would have.
    ("Q", "demote the primary, leaving a correction family with no origin",
     edit_json(MANIFEST, _reclassify_primary),
     "exactly_one_primary_correction"),

    ("R", "drop the known_traps declaration, so the lesson is fixed in the "
          "cards and recorded nowhere",
     edit_json(MANIFEST, lambda d: d.__setitem__("known_traps_entries", [])),
     "known_traps_entries_declared_and_exist"),

    ("S", "point a declared artefact at a file that does not exist",
     edit_json(MANIFEST, _break_artefact),
     "declared_artefacts_exist"),
]

WATCHED = [QB4_H, QB4_B, QB9_A, QB9_B, TRAPS, MANIFEST, INDEX]

if __name__ == "__main__":
    raise SystemExit(run_suite(
        "mutation suite: CORR-BMP-EDITION-PROP-20260905 (BMP MS edition sweep)",
        PROBE, MUTATIONS, WATCHED))
