#!/usr/bin/env python3
"""Mutation suite for CORR-T5-HYDRANT-20260906.

WHAT THE MUTATIONS ARE SHAPED AROUND
------------------------------------
This record turns on a TWO-LIMB rule, and the failure mode is not a wholesale
revert - nobody puts "4 to 6 Bar" back on purpose. It is the quiet loss of the
second limb. `0.25 N/mm2 below 6,000 GT` reads like a qualification, so it is
the first thing an editor tightening a bullet deletes, and the card is then
wrong for every ship under the threshold while still looking authoritative and
still citing SOLAS.

So mutations D, E and F drop ONLY the lower limb, on each of the three sites in
turn, and each must be caught by that site's own limb check. G drops the GT
threshold while leaving both numbers, which is the subtler version: two figures
and nothing saying which ship gets which.

MUTATION K ATTACKS THE REASON, NOT THE RESULT
---------------------------------------------
It removes the governing figures from QB9_B#q5 - a card this record does not
edit. QB9_B is why the 4.0 bar site was a CONTRADICTION rather than merely an
unsourced number, and that contradiction is the recorded justification for
correcting it under section 7. If QB9_B silently stopped carrying the figures,
the justification would evaporate and nothing would notice. A gate that asserts
only its own edits cannot see this.

MUTATION L IS THE PROVENANCE TRAP, DELIBERATELY REVERSED
---------------------------------------------------------
It puts "4 to 6 Bar" back into the card's VERSION STAMP only. A stamp legitimately
quotes what was removed, so this must NOT be caught - and the suite asserts the
gate's scoping by requiring the *element* checks to stay green while a card-wide
grep would fire. It is registered against the check that would wrongly own it,
inverted: see `PROVENANCE_PROBE` and `provenance_check` below.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import (                    # noqa: E402
    Snapshot, edit_json, run_probe, run_suite, sub_in_file)

MANIFEST = HERE / "correction_corr_t5_hydrant_20260906_manifest.json"
QB2_A = REPO / "meoclass1/QB2_A.html"
QB2_B = REPO / "meoclass1/QB2_B.html"
QB2_H = REPO / "meoclass1/QB2_H.html"
QB9_B = REPO / "meoclass1/QB9_B.html"
TRAPS = REPO / "meoclass1/known_traps.md"
PROBE = "validate_correction_t5hydrant.py"

LOWER = "and <strong>0.25 N/mm&sup2;</strong> below"
THRESHOLD = "at 6,000 GT and upwards and"


def _drop_passenger_note(d):
    d["authority"] = d["authority"].replace(
        "The passenger-ship limbs are deliberately NOT introduced",
        "Passenger ships are out of scope")


def _drop_deferral(d):
    d["propagation"].pop("deferred_to_k_items", None)


MUTATIONS = [
    # ---- wholesale revert ------------------------------------------------
    ("A", "put the 4-6 bar required minimum back on QB2_A q8",
     sub_in_file(QB2_A,
                 "<li><strong>0.27 / 0.25 N/mm&sup2;:</strong> SOLAS "
                 "II-2/10.2.1.6",
                 "<li><strong>4 to 6 Bar:</strong> Typical minimum operational "
                 "pressure range required at the furthest hydrant. SOLAS "
                 "II-2/10.2.1.6", count=1),
     "N-3_false_figure_gone_from_the_teaching_layers"),

    ("B", "put the 4.0 bar minimum back on QB2_H q2",
     sub_in_file(QB2_H, "deplete the fire main below the SOLAS",
                 "deplete the fire main pressure below the 4.0 bar minimum "
                 "required at the highest hydrant, per SOLAS", count=1),
     "E-2_false_figure_gone_from_the_teaching_layers"),

    ("C", "drop the governing provision from QB2_B q18",
     sub_in_file(QB2_B, "SOLAS II-2/10.2.1.6 minimum pressure at the hydrants",
                 "The minimum pressure at the hydrants", count=1),
     "E-3_element_cites_the_governing_provision"),

    # ---- the real failure mode: the second limb goes quietly -------------
    ("D", "drop the LOWER limb from QB2_A q8",
     sub_in_file(QB2_A, LOWER, "", count=1),
     "N-3_element_carries_the_LOWER_limb"),

    ("E", "drop the LOWER limb from QB2_B q18",
     sub_in_file(QB2_B, LOWER, "", count=1),
     "E-3_element_carries_the_LOWER_limb"),

    ("F", "drop the LOWER limb from QB2_H q2",
     sub_in_file(QB2_H, LOWER, "", count=1),
     "E-2_element_carries_the_LOWER_limb"),

    ("G", "keep both figures but delete the 6,000 GT threshold",
     sub_in_file(QB2_A, THRESHOLD, "and", count=1),
     "N-3_element_carries_the_GT_threshold"),

    ("H", "drop the two-pumps condition that makes the figure mean anything",
     sub_in_file(QB2_B,
                 "at the hydrants with the two required pumps delivering "
                 "simultaneously", "at the hydrants", count=1),
     "E-3_element_states_the_two_pumps_condition"),

    ("I", "silently widen the scope from cargo ships to all ships",
     sub_in_file(QB2_H, "&mdash; for cargo ships <strong>0.27", "&mdash; "
                 "<strong>0.27", count=1),
     "E-2_element_scopes_the_figures_to_cargo_ships"),

    ("J", "delete the statement that a monitor-throw figure is not a minimum",
     sub_in_file(QB2_A,
                 " A higher pressure quoted for deck-monitor throw is a design "
                 "or operational target, not a SOLAS minimum.", "", count=1),
     "N3_says_a_monitor_throw_figure_is_not_a_SOLAS_minimum"),

    ("K", "remove the governing figures from the sibling card that justified E-2",
     sub_in_file(QB9_B, "and <strong>0.25 N/mm&sup2;</strong> below", "",
                 count=1),
     "sibling_card_still_carries_the_governing_figures"),

    ("L", "soften E-3 to 'incomplete' instead of wrong below the threshold",
     sub_in_file(QB2_B, "Quoting 0.27 alone is wrong for a ship under 6,000 GT.",
                 "Quoting 0.27 alone is incomplete.", count=1),
     "E3_says_the_single_limb_form_is_wrong_below_the_threshold"),

    # ---- the record ------------------------------------------------------
    ("M", "erase the statement that passenger limbs were left out on purpose",
     edit_json(MANIFEST, _drop_passenger_note),
     "passenger_limbs_are_explicitly_out_of_scope"),

    ("N", "drop the deferred hose-test contradiction instead of raising it",
     edit_json(MANIFEST, _drop_deferral),
     "unresolved_hose_test_contradiction_is_deferred_not_guessed"),

    ("O", "strip the contradiction lesson out of known_traps 93",
     sub_in_file(TRAPS,
                 "**Internal contradiction is a stronger signal than a "
                 "suspicious number.**", "**Check numbers.**", count=1),
     "known_traps_entry_93_carries_the_lesson"),
]

#: A version stamp legitimately QUOTES the figure it removed. This edit must
#: NOT be caught: if it is, the gate is reading its own audit trail, which is
#: known_traps entry 89 and cost three Tranche 4A gates a red run. Asserted as
#: an explicit negative rather than left untested, because "the gate is
#: correctly scoped" is a claim like any other.
PROVENANCE_PROBE = (
    "P", "quote '4 to 6 Bar' in the version stamp only - MUST NOT be caught",
    sub_in_file(QB2_A, "gave &ldquo;4 to 6 Bar&rdquo;",
                "gave &ldquo;4 to 6 Bar&rdquo; (4 to 6 Bar)", count=1))


def provenance_check() -> int:
    mid, desc, apply = PROVENANCE_PROBE
    snap = Snapshot([QB2_A])
    try:
        apply()
        _rc, failing = run_probe(PROBE)
    finally:
        bad = snap.restore()
    if bad:
        print("    RESTORE FAILED: %s" % bad)
        return 2
    # The digest pin necessarily fires - it fires on ANY byte change, which is
    # exactly why it may never be a mutation's catch. The claim under test is
    # that no CONTENT check reads the audit trail, so the pin is excluded.
    content_failures = failing - {"every_pinned_state_is_live_or_a_proven_ancestor"}
    ok = not content_failures
    print("%-3s %-58s %s" % (mid, desc, "CORRECTLY IGNORED by every content "
                             "check" if ok
                             else "WRONGLY CAUGHT %s" % sorted(content_failures)))
    return 0 if ok else 1


def main() -> int:
    rc = run_suite("CORR-T5-HYDRANT-20260906", PROBE, MUTATIONS,
                   [QB2_A, QB2_B, QB2_H, QB9_B, MANIFEST, TRAPS])
    print("\nprovenance scoping probe")
    print("------------------------")
    return rc or provenance_check()


if __name__ == "__main__":
    raise SystemExit(main())
