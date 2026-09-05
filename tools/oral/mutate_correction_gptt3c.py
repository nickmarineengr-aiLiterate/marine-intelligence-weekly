#!/usr/bin/env python3
"""Mutation proof for the Tranche 3C content gates.

WHAT THIS PROVES, AND WHAT IT DOES NOT
--------------------------------------
`validate_correction_gptt3c.py` asserts a set of regulatory propositions.  A
validator that asserts nothing passes just as green as one that asserts
everything, so each gate has to be shown to FAIL when the proposition it guards
is removed.  That is what this harness does: it corrupts one proposition at a
time, runs the validator, and requires the INTENDED check to be the one that
goes red.

Two rules from the release skill are enforced structurally here:

* **Every mutation's required check must be a CONTENT check, never a digest
  pin.**  Any edit trips the pin, so accepting the pin as the catch would prove
  only that the pin works while the substantive checks rot as dead code.  This
  harness does not run `validate_corrections.py` at all.
* **A mutation that changes no bytes has exercised nothing.**  `preflight_or_die`
  is the first statement of `main()`, so a spec whose `old` string has drifted
  refuses to launch the suite instead of quietly passing.

Restoration is from this harness's own byte snapshot, by exact path, in a
`finally`.  It never runs `git checkout -- .` or any blanket reset: that
destroys uncommitted branch edits.  A killed process still leaves bytes on
disk, which is why this should be run through `run_oral_release.py` when it is
registered as a gate -- it is NOT registered by this pass, on the brief's
instruction.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oral_mutation import (                                          # noqa: E402
    mutation_verdict, preflight_or_die, replace_spec, require_control_baseline,
    validator_fail_details, validator_failing)

REPO = Path(__file__).resolve().parents[2]
VALIDATOR = "tools/oral/validate_correction_gptt3c.py"

QB6 = "meoclass1/QB6.html"
QB7I = "meoclass1/QB7_I.html"
QB3F = "meoclass1/QB3_F.html"
QB2A = "meoclass1/QB2_A.html"
QB1F = "meoclass1/QB1_F.html"
REG = "docs/sources/MIW_SOURCE_REGISTRY.json"
CUSTODY = "docs/sources/T3C_IACS_CUSTODY_REPAIR.json"
Z20PDF = "docs/sources/IACS-UR-Z20-Rev2.pdf"

# (spec, the check that MUST go red)
SPECS = [
    # ---------------- FAMILY A : CII capacity / unit -----------------------
    (replace_spec(
        "A1-restore-universal-dwt-unit", QB6,
        "gCO₂ per capacity-nautical-mile", "gCO₂/DWT·nm",
        intended_reason="the exact defect F-2 corrected: a universal DWT unit "
                        "restored into the 15-second layer"),
     "cii_q1_no_surviving_universal_dwt_unit"),

    (replace_spec(
        "A2-drop-the-gt-limb", QB6,
        "gross tonnage (GT) for cruise passenger ships",
        "gross tonnage for certain ship types",
        intended_reason="the ship-type distinction blurred away in the 60-second "
                        "answer, which is how a universal quietly returns"),
     "cii_q1_every_dwt_list_is_paired_with_its_gt_list"),

    (replace_spec(
        "A3-strip-capacity-from-the-formula", QB6,
        "Attained CII (gCO₂ per capacity·nm)", "Attained CII (gCO₂/DWT·nm)",
        intended_reason="the formula block reverted while the prose stays "
                        "correct -- a layer-level regression the prose hides"),
     "cii_q1_formula_expresses_the_capacity_quantity"),

    (replace_spec(
        "A4-reinstate-the-triple-e-engine", QB6,
        "<li>At 18 knots, daily HFO",
        "<li>MAN B&W 11G90ME-C main engine ~35,000 kW MCR</li>\n<li>At 18 knots, daily HFO",
        intended_reason="F-1's deleted vessel specification put back into "
                        "'On My Vessel'"),
     "f1_no_triple_e_engine_specification"),

    (replace_spec(
        "A5-substitute-a-different-engine-spec", QB6,
        "<li>At 18 knots, daily HFO",
        "<li>MAN B&W 12K98ME rated 68,640 kW MCR</li>\n<li>At 18 knots, daily HFO",
        intended_reason="the trap F-1 expressly forbade -- replacing one "
                        "ungrounded vessel specification with another. Source "
                        "proof does not rescue a provenance failure."),
     "f1_no_substitute_vessel_specification"),

    (replace_spec(
        "A6-drop-the-g1-currentness-chain", QB6,
        "MEPC.412(84)", "MEPC.352(78)",
        intended_reason="the 2026 amendment citation lost, leaving the card "
                        "resting on the superseded G1 wording",
        count=6),
     "cii_q1_cites_current_g1_chain"),

    (replace_spec(
        "A7-revert-the-qb7i-short-layer", QB7I,
        "per unit of <strong>capacity</strong> per nautical mile",
        "per DWT-mile",
        intended_reason="F-3 reverted: the 15-second answer contradicting its "
                        "own already-correct body again"),
     "cii_q10_short_layer_aligned_with_its_body"),

    # ---------------- FAMILY B : MARPOL Annex I reg. 34.1.5 ----------------
    (replace_spec(
        "B1-drop-a-limb-from-the-body-list", QB3F,
        "not more than <strong>1/15,000</strong>",
        "not more than <strong>1/30,000</strong>",
        intended_reason="one limb collapsed back to the universal, in the body "
                        "list -- the site the whole finding began at"),
     "reg34_every_site_carries_both_limbs"),

    (replace_spec(
        "B2-blur-the-boundary-date", QB3F,
        "on or before 31 Dec 1979", "before 1980",
        intended_reason="the date boundary made inexact in the compact split. "
                        "'Before 1980' silently moves every tanker delivered "
                        "ON 31 December 1979 into the wrong limb.",
        count=3),
     "reg34_lower_limb_bound_to_on_or_before_31_dec_1979"),

    (replace_spec(
        "B3-revert-the-page-level-grid", QB3F,
        "&le;1/15,000 of cargo if delivered on or before 31 Dec 1979; &le;1/30,000 if delivered after",
        "&le;1/30,000 of cargo",
        intended_reason="the SEVENTH site -- the page-level Rapid Recall grid "
                        "outside every q-card, which no card digest can reach. "
                        "This mutation is the only thing standing between that "
                        "site and an unguarded regression."),
     "reg34_page_level_rapid_recall_limb_present"),

    (replace_spec(
        "B4-delete-an-untouched-criterion", QB3F,
        "More than <strong>50 nautical miles</strong> from nearest land",
        "More than <strong>12 nautical miles</strong> from nearest land",
        intended_reason="proves the gate also protects the reg.34 criteria the "
                        "brief said NOT to alter, so a future edit cannot "
                        "quietly change one under cover of this correction"),
     "reg34_body_list_distance_limb_exact"),

    # ---------------- FAMILY C : QB2_A#q31 --------------------------------
    (replace_spec(
        "C1-restore-the-personal-fine-ore-routine", QB2A,
        "This is not a cargo operation from my container-vessel experience",
        "Before a fine ore or concentrate loading I confirm with the Chief Officer "
        "that the cargo declaration and the TML certificates are aboard, and this is "
        "my routine",
        intended_reason="F-5 reverted: an ungrounded bulk-carrier routine "
                        "reclaimed as the candidate's own experience"),
     "f5_no_personal_fine_ore_routine"),

    (replace_spec(
        "C2-restore-the-wrong-cargo-tonnage", QB2A,
        "<strong>71,200 tonnes</strong>", "<strong>72,100 tonnes</strong>",
        intended_reason="the transposed cargo figure put back -- the one "
                        "no source supports"),
     "q31_removed_cargo_tonnage_72_100"),

    (replace_spec(
        "C3-narrow-the-distance-hedge-again", QB2A,
        "<strong>230 to 290 nautical miles</strong>",
        "<strong>230 to 240 nautical miles</strong>",
        intended_reason="the hedge put back on the WRONG SIDE of the real "
                        "disagreement -- the defect class that also produced "
                        "the National Shipping Board date error"),
     "q31_removed_distance_range_230_to_240"),

    (replace_spec(
        "C4-delete-the-source-confidence-block", QB2A,
        "Source confidence &mdash; read this before you quote a number",
        "Further reading",
        intended_reason="the block this card alone lacked, removed again"),
     "q31_source_confidence_block_exists"),

    (replace_spec(
        "C5-convert-hypothesis-into-a-finding", QB2A,
        "it is a hypothesis", "it is now established",
        intended_reason="the judgement the whole card is built to teach -- "
                        "never convict on an open casualty"),
     "q31_body_refuses_to_convert_hypothesis_into_finding"),

    (replace_spec(
        "C6-deregister-the-casualty-source", REG,
        '"SRC-CASUALTY-OCEANWINNER-2026"', '"SRC-CASUALTY-OCEANWINNER-2026-DRAFT"',
        intended_reason="the governance ruling defeated: a recent named casualty "
                        "published with no registered supporting source"),
     "q31_named_casualty_source_registered"),

    (replace_spec(
        "C7-claim-a-source-that-was-never-read", QB2A,
        "<strong>Currentness.</strong> Verified",
        "The flag State's casualty report was read in full, chapter 4. "
        "<strong>Currentness.</strong> Verified",
        intended_reason="the specific dishonesty the brief forbade -- claiming a "
                        "source was opened when it was not, and asserting a "
                        "chapter structure for a document that does not exist"),
     "q31_scb_makes_no_read_claim_for_an_unread_source"),

    # ---------------- FAMILY D : IACS custody ------------------------------
    (replace_spec(
        "D1-corrupt-the-z20-registry-hash", REG,
        "6bfdc313a9c483f9094714003f90ced565b9e678d7611199ec4077ba94f790ed",
        "6bfdc313a9c483f9094714003f90ced565b9e678d7611199ec4077ba94f790de",
        intended_reason="the registry hash no longer matches the held bytes -- "
                        "custody claimed but not real",
        count=2),
     "iacs_REV2_hash_matches_registry"),

    (replace_spec(
        "D2-strip-z18-revision-metadata", REG,
        '"revision": "Rev.9"', '"revision": null',
        intended_reason="revision metadata lost, so 'which revision was this "
                        "verified against?' becomes unanswerable -- exactly the "
                        "gap that let a Rev.8 citation read as current"),
     "iacs_REV9_revision_metadata_present"),

    (replace_spec(
        "D3-mis-title-the-z7-row", REG,
        '"title": "IACS Unified Requirement Z7 - Hull Classification Surveys"',
        '"title": "IACS Unified Requirement Z7 - Enhanced Survey Programme for '
        'Bulk Carriers and Oil Tankers"',
        intended_reason="the exact confusion CORR-URZ7-20260901 was raised to "
                        "fix, reintroduced at the registry row rather than in a "
                        "card -- and still live in QB4_E, which this pass was "
                        "scoped out of and has reported instead"),
     "iacs_CORR1_title_correct"),

    (replace_spec(
        "D4-break-a-z20-paragraph-claim", QB1F,
        "The chief engineer shall be the responsible person on board in charge of the PMS.",
        "The chief engineer may delegate responsibility for the PMS.",
        intended_reason="a sub-paragraph-level Z20 claim silently changed to "
                        "something the held instrument does not say. This is the "
                        "check that makes 'verified against the source' mean "
                        "anything at all."),
     "z20_every_cited_paragraph_is_still_in_the_card"),

    (replace_spec(
        "D5-delete-the-custody-record", CUSTODY,
        '"kind": "SOURCE_CUSTODY_REPAIR"', '"kind": "NOTE"',
        intended_reason="the custody record downgraded to a note, so the "
                        "acquisition has no governed record"),
     "iacs_custody_record_is_not_a_correction_manifest"),
]

# NOTE on the expected-check names above.  Five of them were RETARGETED after
# the first run, and the reason is worth keeping.  A2, A3, B2, B4 and C5 all
# reported CAUGHT-BY-THE-WRONG-CHECK, which is how this harness says "your
# mutation was caught, but not by the guard you claimed".  In every case the
# originally named check was VACUOUS: it asked whether a phrase appeared
# ANYWHERE in the card, and the mutations removed it from ONE layer while three
# others still carried it.  Those five checks were tightened to assert BINDING
# rather than presence, and the mutations now name the tightened checks.  The
# escapes were real holes and they were found here, not in review.


def run_validator():
    proc = subprocess.run([sys.executable, str(REPO / VALIDATOR)],
                          cwd=REPO, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main() -> int:
    specs = [s for s, _ in SPECS]
    preflight_or_die(specs, root=REPO)

    snapshot = {}
    for rel in {s.target for s in specs}:
        snapshot[rel] = (REPO / rel).read_bytes()

    code, out = run_validator()
    control = validator_failing(out)
    state = require_control_baseline(control, VALIDATOR, REPO)
    if not state.runnable:
        print("mutations=0 escapes=0 -- CONTROL REFUSED, suite did not run")
        return 2
    baseline_details = validator_fail_details(out)

    results, escapes = [], 0
    try:
        for spec, expected in SPECS:
            path = REPO / spec.target
            original = snapshot[spec.target]
            text = original.decode("utf-8")
            mutated = spec.apply(text)
            if mutated == text:
                # Cannot happen after preflight_or_die -- but a suite that
                # trusts preflight and never re-checks at run time is one
                # refactor away from exercising nothing.
                print("FAIL      %-38s spec applied no bytes at run time"
                      % spec.mutation_id)
                escapes += 1
                continue
            path.write_bytes(mutated.encode("utf-8").replace(b"\r\n", b"\n"))
            try:
                _, mout = run_validator()
                now = validator_failing(mout)
                if expected is None:
                    new = sorted(frozenset(now) - frozenset(control))
                    verdict, detail = ("reported",
                                       "no owning check; new failures=%s" % (new or "none"))
                else:
                    verdict, detail = mutation_verdict(
                        expected, now, control,
                        validator_fail_details(mout), baseline_details)
                    if verdict == "escape":
                        escapes += 1
            finally:
                path.write_bytes(original)
            results.append((spec.mutation_id, verdict, detail))
            print("%-9s %-38s %s" % (verdict.upper(), spec.mutation_id, detail))
            print("          why: %s" % spec.intended_reason)
    finally:
        for rel, data in snapshot.items():
            (REPO / rel).write_bytes(data)
        after, _ = {rel: (REPO / rel).read_bytes() for rel in snapshot}, None
        bad = [rel for rel in snapshot if after[rel] != snapshot[rel]]
        print("\nrestore: %d file(s), byte-exact=%s"
              % (len(snapshot), "yes" if not bad else "NO -- %s" % bad))

    code2, out2 = run_validator()
    print("post-suite control: %s"
          % ("clean" if validator_failing(out2) == control else "DRIFTED"))
    counted = [r for r in results if r[1] != "reported"]
    print("\nGPT Tranche 3C mutations=%d escapes=%d"
          % (len(counted), escapes))
    return 1 if escapes else 0


if __name__ == "__main__":
    sys.exit(main())
