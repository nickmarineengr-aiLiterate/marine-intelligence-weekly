#!/usr/bin/env python3
"""
Mutation suite for CORR-GPT-PASS1-20260904.

`validate_correction_gptpass1.py` reports 40 green checks. Green output on its
own is indistinguishable from a validator that reads nothing, so every
proposition the correction rests on is attacked here, and each mutation must
trip the check that OWNS that proposition -- never the digest pin, which fires
on any byte change at all (enforced by oral_content_mutation.DIGEST_PINS).

THE MUTATIONS THAT MATTER MOST ARE NOT THE CONTENT ONES.

*   MUTATION P LAUNDERS HISTORY. It rewrites `batch_h6_manifest.json`'s topic
    prose so the overturned "DERIVED from the ISM 10.3" reading disappears and
    the original authoring looks as though it had been right all along. Nothing
    about the live product changes, every card digest still matches, and the
    corpus quietly loses the record of what it once taught. That is invisible
    to every digest check in the toolchain -- the same blind spot F1b's
    hold-laundering mutations were written for -- and `p` must be caught by
    `h6_historical_prose_not_laundered`.

*   MUTATION T OVERCLAIMS A SOURCE. It flips the SOLAS II-2 row to
    `RETRIEVED` with a local path, i.e. it pretends the consolidated chapter
    II-2 text was acquired when it was not. The candidate-facing numbers are
    unchanged and correct, so no content check anywhere would notice. The
    review's instruction was explicit -- *do not pretend primary IMO SOLAS text
    was acquired* -- and this is the only guard that enforces it.

*   MUTATION S IS THE DESTRUCTIVE REPLACE. It deletes the superseded tier-2
    Grain row instead of retaining it, which is what "upgrade the source" looks
    like when done carelessly. The registry's own history convention says a
    superseded entry is retained and marked, never overwritten.

Mutations A, F, I and L reintroduce the four rejected wordings verbatim, and
each must be caught by the negation-window check that owns it rather than by a
flat phrase ban -- see the validator's header for why that distinction is the
one that keeps the guard honest.
"""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import (                    # noqa: E402
    edit_json, run_suite, sub_in_file)

QB5J = REPO / "meoclass1/QB5_J.html"
QB1D = REPO / "meoclass1/QB1_D.html"
QB5I = REPO / "meoclass1/QB5_I.html"
MANIFEST = HERE / "correction_corr_gpt_pass1_20260904_manifest.json"
H6 = HERE / "batch_h6_manifest.json"
REGISTRY = REPO / "docs/sources/MIW_SOURCE_REGISTRY.json"
PROBE = "validate_correction_gptpass1.py"


def _reg(data, source_id):
    for s in data["sources"]:
        if s["source_id"] == source_id:
            return s
    raise AssertionError("source row absent: %s" % source_id)


MUTATIONS = [
    # ---------------- QB5_J#q2 : NOx / EIAPP ---------------------------
    ("A", "reinstate absolute EIAPP invalidation in the trap point",
     sub_in_file(QB5J,
                 "an unapproved departure can leave the engine no longer "
                 "compliant with its certified NOx configuration",
                 "going outside them invalidates the EIAPP certificate"),
     "nox_absolute_invalidation_absent"),

    ("B", "reinstate absolute EIAPP invalidation in the reg-box",
     sub_in_file(QB5J,
                 "an unapproved departure can render the engine non-compliant "
                 "with its certified NOx configuration",
                 "going outside them invalidates the EIAPP certificate"),
     "nox_absolute_invalidation_absent"),

    ("C", "delete the allowable-adjustment range from the reg-box (NTC 2.4.1.2)",
     sub_in_file(QB5J,
                 ", and the full range of allowable adjustments (NTC 2008 2.4.1)",
                 ""),
     "nox_allowable_adjustment_range_stated"),

    ("D", "remove the approved procedure / survey route",
     sub_in_file(QB5J,
                 "must follow the applicable approved procedure, verification "
                 "or survey route",
                 "must not be attempted"),
     "nox_approved_route_stated"),

    ("E", "harden the conditional consequence back into a certainty",
     sub_in_file(QB5J,
                 "an unapproved departure can render the engine non-compliant",
                 "an unapproved departure renders the engine non-compliant"),
     "nox_consequence_is_conditional"),

    ("F", "drop the practical oral warning",
     sub_in_file(QB5J,
                 " Do not re-time or change NOx-critical settings casually to "
                 "chase performance.",
                 ""),
     "nox_practical_warning_preserved"),

    # ---------------- QB5_J#q2 : ISO 19030 -----------------------------
    ("G", "reinstate the ISO 19030 overclaim in the reg-box",
     sub_in_file(QB5J,
                 "Framework for measuring changes in hull and propeller "
                 "performance; read together with corrected engine-performance "
                 "data it helps distinguish the hull and propeller contribution "
                 "from machinery deterioration. It does not itself assess "
                 "engine condition",
                 "Measurement of changes in hull and propeller performance "
                 "&mdash; the standard method for separating hull fouling from "
                 "engine deterioration"),
     "iso19030_overclaim_absent"),

    ("H", "delete the explicit 'not an engine diagnostic' negative",
     sub_in_file(QB5J, ". It does not itself assess engine condition", ""),
     "iso19030_not_an_engine_diagnostic"),

    ("I", "sever ISO 19030 from the corrected engine data it must be read with",
     sub_in_file(QB5J,
                 "read together with corrected engine-performance data it helps "
                 "distinguish",
                 "it alone distinguishes"),
     "iso19030_needs_corrected_engine_data"),

    # ---------------- QB1_D#q7 : hydrostatics --------------------------
    ("J", "reinstate 'stop being valid' in the CE Oral Tip",
     sub_in_file(QB1D,
                 "the moment the waterline is inclined they are no longer "
                 "sufficient by themselves",
                 "the moment the waterline is inclined they stop being valid"),
     "hydrostatics_invalidity_claim_absent"),

    ("K", "remove the sufficiency formulation from the 60-second answer",
     sub_in_file(QB1D,
                 "those tables are not, by themselves, sufficient, because "
                 "every station is then at a different draught",
                 "those tables do not apply"),
     "hydrostatics_stated_as_insufficient_not_invalid"),

    ("L", "delete the positive Bonjean reconstruction claim",
     sub_in_file(QB1D,
                 "Bonjean curves let us reconstruct the immersed sectional "
                 "areas station by station for that actual waterline.",
                 "Bonjean curves solve that."),
     "bonjean_reconstruction_stated"),

    ("M", "delete the already-correct body heading the rest was aligned to",
     sub_in_file(QB1D, "Why the hydrostatic tables are not enough",
                 "About the hydrostatic tables"),
     "bonjean_already_correct_sections_kept"),

    # ---------------- QB5_I#q8 : universal-list risk --------------------
    ("N", "strip the example framing from the critical-equipment list",
     sub_in_file(QB5I,
                 "<em>typical examples that a company&rsquo;s SMS and risk "
                 "assessment may designate, depending on the ship&rsquo;s "
                 "design, machinery and trade</em>: main engine",
                 "main engine"),
     "critical_equipment_framed_as_example"),

    ("O", "delete the 'ISM prescribes no critical-spares list' qualifier",
     sub_in_file(QB5I,
                 " &mdash; the ISM Code prescribes no critical-spares list", ""),
     "ism_does_not_prescribe_the_lists"),

    ("P", "re-universalise the class spare-parts list",
     sub_in_file(QB5I,
                 "The scope differs between societies and with the ship&rsquo;s "
                 "notation, so quote the rules your ship is actually classed "
                 "under rather than a single universal list.",
                 "The list is the same for every vessel."),
     "class_spares_conditional"),

    ("Q", "delete ISM 10.3's stand-by testing limb",
     sub_in_file(QB5I, "regular testing of stand-by arrangements",
                 "periodic proving of equipment"),
     "ism_10_3_limbs_intact"),

    ("R", "gut the CE inventory answer of its worked examples",
     sub_in_file(QB5I, "fuel valves, pump plungers", "various parts"),
     "ce_inventory_answer_not_weakened"),

    # ---------------- governance: history laundering ---------------------
    ("S", "LAUNDER H6's topic prose so the overturned claim disappears",
     edit_json(H6, lambda d: d["cards"][1].__setitem__(
         "topic", d["cards"][1]["topic"].replace(
             "the critical-spares list DERIVED from the ISM 10.3 "
             "critical-equipment list rather than chosen",
             "the critical-spares list INFORMED BY the ISM 10.3 "
             "critical-equipment list"))),
     "h6_historical_prose_not_laundered"),

    ("T", "rebaseline H6's pin to the live state",
     edit_json(H6, lambda d: d["cards"][1].__setitem__(
         "post_edit_digest",
         "bc41fb2398958f2922def116a3c8f9c3492b94dea67b9691df5bbcf5736ffd9e")),
     "h6_pin_not_rebaselined"),

    ("U", "drop the supersession ancestry from this record",
     edit_json(MANIFEST,
               lambda d: [c.pop("supersedes", None) for c in d["cards"]]),
     "supersession_ancestry_declared"),

    # ---------------- governance: source overclaim -----------------------
    ("V", "PRETEND the consolidated SOLAS chapter II-2 text was acquired",
     edit_json(REGISTRY, lambda d: _reg(d, "SRC-SOLAS-II2-REG10-SPARECHARGES")
               .update({"access_status": "RETRIEVED",
                        "local_path": "F:/RulesApp-Local-Input/true-source/"
                                      "03-imo-instruments/SOLAS-1974/"
                                      "chapter-II-2/consolidated.pdf",
                        "access_note": "Consolidated chapter II-2 obtained."})),
     "solas_row_not_overclaimed"),

    ("W", "DESTRUCTIVELY replace the superseded tier-2 Grain row",
     edit_json(REGISTRY, lambda d: d.__setitem__(
         "sources", [s for s in d["sources"]
                     if s["source_id"] != "SRC-GRAINCODE-PARTA-TEXT"])),
     "grain_tier2_row_superseded_not_deleted"),

    ("X", "claim the 1991 adoption resolution is a consolidated edition",
     edit_json(REGISTRY, lambda d: _reg(d, "SRC-GRAINCODE-MSC23-59")
               .update({"currentness": "CURRENT_VERIFIED",
                        "edition": "The consolidated International Grain Code.",
                        "access_note": "Consolidated text held."})),
     "grain_tier1_not_claimed_consolidated"),

    ("Y", "revert the MS Act corrigenda to PENDING_FILING",
     edit_json(REGISTRY, lambda d: _reg(d, "SRC-MSACT-2025-CORRIGENDA")
               .update({"local_path": "PENDING_FILING - not filed"})),
     "msact_corrigenda_filed"),

    ("Z", "strip the OCR / image-only-scan access limit from the record",
     edit_json(MANIFEST, lambda d: d["authority"].__setitem__(
         "nox_access_note", "Read from the held PDF.")),
     "nox_access_limit_recorded"),
]

WATCHED = [QB5J, QB1D, QB5I, MANIFEST, H6, REGISTRY]

if __name__ == "__main__":
    raise SystemExit(run_suite(
        "mutation suite: CORR-GPT-PASS1-20260904 (QB5_J#q2, QB1_D#q7, QB5_I#q8)",
        PROBE, MUTATIONS, WATCHED))
