#!/usr/bin/env python3
"""
Mutation suite for CORR-GRAIN-TERMINOLOGY-20260902  (QB2_A#q11 and #q33).

`validate_correction_grainterm.py` reports 21 green checks. Green output alone
is indistinguishable from a validator that reads nothing, so every proposition
is attacked here and each mutation must trip the check that OWNS it -- never a
digest pin, which fires on any byte change at all
(enforced by oral_content_mutation.DIGEST_PINS).

TWO MUTATIONS EARN THEIR PLACE PARTICULARLY.

F reinstates the rejected proposition in the SIBLING card only, leaving the
reported card correct. That is the half-finished repair of known_traps entry
51, and it is what actually happened here: the review reported #q11 and the
identical claim sat undisturbed in #q33 until the scope pass found it.

H makes #q33 attribute the grain-manual update requirement to MSC.552(108)
itself. #q33's one genuinely correct distinction is that the requirement is
class and P&I guidance and NOT in the resolution text; a correction that
"tidied" that away would over-claim to a panel, which is the exact failure the
BMP-MS currency round taught.
"""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import (                    # noqa: E402
    edit_json, run_suite, sub_in_file)

CARD = REPO / "meoclass1/QB2_A.html"
MANIFEST = HERE / "correction_corr_grain_terminology_20260902_manifest.json"
PROBE = "validate_correction_grainterm.py"


def _drop_supersedes(anchor):
    def mutate(d):
        for c in d["cards"]:
            if c["anchor"] == anchor:
                c.pop("supersedes", None)
    return mutate


MUTATIONS = [
    ("A", "reinstate the rejected DoA-invalidity claim in q11",
     sub_in_file(CARD,
                 "The Code does not make the DoA &ldquo;invalid&rdquo; on its "
                 "own terms.",
                 "The DoA is invalid unless accompanied by an approved Grain "
                 "Stability Booklet."),
     "doa_invalidity_never_asserted_q11"),

    ("B", "delete the A 3.2 accompany-or-incorporate wording",
     sub_in_file(CARD,
                 "shall accompany or be incorporated into the grain loading "
                 "manual",
                 "is issued alongside the ship's stability paperwork"),
     "a3_2_accompany_or_incorporated"),

    ("C", "delete the A 6.1 printed-booklet-form requirement",
     sub_in_file(CARD, "printed booklet form", "a convenient format"),
     "a6_1_printed_booklet_form"),

    ("D", "delete the A 3.5 no-document route",
     # Three forms exist, one of them split by an inline <em>, so the long
     # literal misses it and the flattened check still finds the survivor.
     sub_in_file(CARD, "shall not load grain", "may load grain"),
     "a3_5_no_document_route"),

    ("E", "weaken the A 3.1 evidential effect",
     sub_in_file(CARD,
                 "accepted as evidence that the ship is capable",
                 "conclusive proof that the ship is certified"),
     "a3_1_evidence_of_capability"),

    ("F", "reinstate the rejected claim in the SIBLING card q33 only",
     sub_in_file(CARD,
                 "Say it precisely: the Code does not declare the "
                 "<strong>Document of Authorisation</strong> &ldquo;invalid"
                 "&rdquo; without the booklet &mdash; under",
                 "The Document of Authorisation is invalid without that "
                 "booklet &mdash; under"),
     "doa_invalidity_never_asserted_q33"),

    ("G", "drop the MSC.552(108) third configuration from q11",
     sub_in_file(CARD, "three compartment configurations",
                 "two compartment configurations"),
     "msc552_three_configurations_retained"),

    ("H", "attribute the grain-manual requirement to the resolution itself",
     sub_in_file(CARD,
                 "is <strong>class-society and P&amp;I practical guidance"
                 "</strong>; it is <strong>not</strong> in the text of "
                 "MSC.552(108)",
                 "is stated in the text of MSC.552(108)"),
     "msc552_guidance_not_resolution_on_q33"),

    ("I", "stop calling the manual the Code's own term",
     sub_in_file(CARD,
                 "while <strong>grain loading manual</strong> is the "
                 "Code&rsquo;s own term for the document",
                 "while the manual is one of several names in use"),
     "formal_term_is_grain_loading_manual"),

    ("J", "drop the supersession claim on the 31-August grain correction",
     edit_json(MANIFEST, _drop_supersedes("q11")),
     "supersedes_declared_q11"),

    ("K", "drop the supersession claim on batch H2's pin",
     edit_json(MANIFEST, _drop_supersedes("q33")),
     "supersedes_declared_q33"),
]

WATCHED = [CARD, MANIFEST]

if __name__ == "__main__":
    raise SystemExit(run_suite(
        "mutation suite: CORR-GRAIN-TERMINOLOGY-20260902 (QB2_A#q11, #q33)",
        PROBE, MUTATIONS, WATCHED))
