#!/usr/bin/env python3
"""Mutation suite for CORR-T5-DDCASCADE-20260906.

`validate_correction_t5struct.py` reports 22 green checks, and green output is
indistinguishable from a validator that reads nothing. Every proposition is
attacked here, and each mutation must trip the check that OWNS it - never the
digest pin, which fires on any byte change at all and would therefore "catch"
everything while the substantive checks rotted as dead code.

THE TWO MUTATIONS THIS SUITE EXISTS FOR
---------------------------------------
A restores the cascade on one block - the exact state of the corpus this
morning, and what a careless revert of one paragraph reproduces.

C is the important one. It deletes a whole typed block instead of its
duplicated tail, which is what a WRONG repair of this defect looks like: the
candidate silently loses a section, and every digest pin in the toolchain is
perfectly happy because the pin is recomputed from whatever is there. Only
`every_typed_block_survived_the_repair` can see it, and that check exists
because this mutation does.

D AND E ATTACK THE RECORD'S ARITHMETIC, NOT THE PAGE
----------------------------------------------------
The gate re-derives 146 and 6 from the baseline tree rather than reading them
back out of the record. D and E overstate them in the manifest with the pages
untouched, and both must go red - otherwise `invariants` would be decoration a
future session could quote as evidence.

G IS THE ANTI-COMPLACENCY MUTATION
----------------------------------
It removes the Pass-2 residue declaration from the record. Nothing on any page
changes and no candidate is affected - but a record that closed one residue
generation while silently implying the field is clear is how the next session
comes to believe there is nothing left. The successor family has to stay named.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import (                    # noqa: E402
    edit_json, run_suite, sub_in_file)

MANIFEST = HERE / "correction_corr_t5_ddcascade_20260906_manifest.json"
QB1_G = REPO / "meoclass1/QB1_G.html"
QB1_I = REPO / "meoclass1/QB1_I.html"
QB1_F = REPO / "meoclass1/QB1_F.html"
TRAPS = REPO / "meoclass1/known_traps.md"
PROBE = "validate_correction_t5struct.py"

# A real repaired block on QB1_G#q40, and the cascade restored onto it.
CASUALTY_OK = ('<div class="dd-block dd-casualty"><strong class="dd-label">'
               '⚓ Casualty Link</strong><p>')
CASCADE_BACK = (CASUALTY_OK + 'STRAY TAIL\n* <strong>On My Vessel:</strong> '
                'reintroduced cascade\n</p></div>' +
                '<div class="dd-block dd-spare"><strong class="dd-label">'
                'spare</strong><p>x</p></div>')

EMPTY_PROMISE = ('<details class="deep-dive"><summary>Deep-Dive — CE '
                 'Relevance, Traps, Failures, Numbers, Casualty, Examiner '
                 'Chain, On My Vessel</summary></details>')


def _first_casualty_block(path):
    """The first dd-casualty block on the page, verbatim - as (old, new)."""
    text = path.read_text(encoding="utf-8")
    i = text.find(CASUALTY_OK)
    assert i >= 0, "no dd-casualty block on %s" % path.name
    end = text.find("</p></div>", i) + len("</p></div>")
    return text[i:end]


def restore_cascade():
    old = _first_casualty_block(QB1_G)
    body_end = old.rfind("</p></div>")
    new = (old[:body_end] + "\n* <strong>On My Vessel:</strong> a stray "
           "section restored by mutation" + old[body_end:])
    return sub_in_file(QB1_G, old, new, count=1)


def delete_a_typed_block():
    """Remove a whole block rather than its tail - the WRONG repair."""
    old = _first_casualty_block(QB1_G)
    return sub_in_file(QB1_G, old, "", count=1)


def empty_a_typed_block():
    old = _first_casualty_block(QB1_G)
    head = old[:old.find("<p>") + 3]
    return sub_in_file(QB1_G, old, head + "</p></div>", count=1)


def _bump(field, value):
    def mutate(d):
        d["invariants"][field] = value
    return mutate


def _drop_residue_declaration(d):
    d["propagation"]["residue_remaining"] = "none remaining"


def _drop_artefact(d):
    d["artefacts"] = [a for a in d["artefacts"]
                      if "analyse_ddcascade" not in a["path"]]


MUTATIONS = [
    ("A", "restore the cascade onto one repaired dd-block",
     restore_cascade(), "no_cascaded_deep_dive_block_remains"),

    ("B", "reintroduce an empty deep-dive promise on QB1_I",
     sub_in_file(QB1_I, "<div class=\"q-footer\">",
                 EMPTY_PROMISE + "<div class=\"q-footer\">", count=1),
     "no_empty_deep_dive_promise_remains"),

    # The wrong repair. Every digest pin is happy; only the survival check sees it.
    ("C", "delete a whole typed block instead of its duplicated tail",
     delete_a_typed_block(), "every_typed_block_survived_the_repair"),

    ("D", "keep the block but empty its body",
     empty_a_typed_block(), "no_block_was_emptied_by_the_repair"),

    ("E", "overstate the repaired block count in the record",
     edit_json(MANIFEST, _bump("cascaded_blocks_repaired", 200)),
     "declared_block_count_matches_baseline"),

    ("F", "overstate the empty-promise count in the record",
     edit_json(MANIFEST, _bump("empty_deep_dive_promises_removed", 12)),
     "declared_empty_promise_count_matches_baseline"),

    ("G", "claim the residue field is clear and drop the Pass-2 backlog",
     edit_json(MANIFEST, _drop_residue_declaration),
     "remaining_residue_generation_is_declared"),

    ("H", "restore an orphaned markdown bullet in QB1_F",
     sub_in_file(QB1_F, "<strong>Annex VI (Air):</strong> <strong>",
                 "<strong>Annex VI (Air):</strong> * <strong>", count=1),
     "no_orphaned_markdown_bullet_in_repaired_files"),

    ("I", "silently claim a block was refused as unproven",
     edit_json(MANIFEST, _bump("blocks_refused_as_unproven", 3)),
     "no_block_was_refused_as_unproven"),

    ("J", "delete the losslessness proof the record depends on",
     edit_json(MANIFEST, _drop_artefact), "declared_artefacts_exist"),

    # The lesson, not the product. A trap entry stripped of the two traps that
    # cost this repair a re-run is an entry that teaches nothing.
    ("K", "strip the label-vs-position lesson out of known_traps 90",
     sub_in_file(TRAPS, "**Match by LABEL, never by position.**",
                 "**Blocks are matched.**", count=1),
     "known_traps_entry_90_carries_the_lesson"),

    ("L", "corrupt a pinned post-state so the digest guard must fire",
     edit_json(MANIFEST, lambda d: d["cards"][0].update(
         {"post_edit_digest": "0" * 64})),
     "every_pinned_state_is_live_or_a_proven_ancestor"),

    # An overlap that is edited but not declared is indistinguishable from an
    # unauthorised edit, and it is the thing a reader of this record would most
    # reasonably assume had not happened.
    ("M", "erase the declaration that QB2_H#q2 was edited here",
     edit_json(MANIFEST, lambda d: d["propagation"].pop(
         "cards_edited_here_but_pinned_by_a_sibling_record", None) and None),
     "sibling_pinned_card_is_declared"),

    ("N", "pin QB2_H#q2 here as well, so one card is owned by two records",
     edit_json(MANIFEST, lambda d: d["cards"].append(
         dict(d["cards"][0], file="QB2_H.html", path="meoclass1/QB2_H.html",
              anchor="q2", correction_action_id="T5-DDCASCADE-99")) or None),
     "sibling_pinned_card_is_not_also_pinned_here"),
]


def main() -> int:
    return run_suite("CORR-T5-DDCASCADE-20260906", PROBE, MUTATIONS,
                     [QB1_G, QB1_I, QB1_F, MANIFEST, TRAPS])


if __name__ == "__main__":
    raise SystemExit(main())
