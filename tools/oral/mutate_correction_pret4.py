#!/usr/bin/env python3
"""Mutation proof for the pre-Tranche-4 cleanup content gates.

WHAT THIS PROVES, AND WHAT IT DOES NOT
--------------------------------------
`validate_correction_pret4.py` asserts a set of regulatory propositions.  A
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

THE MUTATIONS THIS SUITE CARES MOST ABOUT
-----------------------------------------
Three of them are not "type the old error again".  They are the failure modes
this specific pass created the opportunity for:

* **A1 / A2 equalise QB6.html in the WRONG DIRECTION** - they make q1 agree with
  q2's old wording rather than the other way round.  That is the realistic
  regression after a pass whose whole purpose was to make two cards in one file
  agree, and a gate that only watches q2 would sleep through it.
* **B4 substitutes a guessed Z10 sub-number.**  The brief forbade this and the
  prohibition turned out to be load-bearing: UR Z7 sec.1.1.3's own "respectively"
  ordering contradicts the common secondary assumption about which sub-number is
  tankers.  A correction that invents precision is a NEW defect wearing the
  corrected one's clothes, and source proof does not rescue it.
* **A6 / B7 damage a card that was already right.**  The scoped occurrences in
  QB3_J, QB1_K and QB7_A are the ones a pattern-only sweep would have eaten.
  These mutations prove the gates notice collateral damage, not just the defect.

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
VALIDATOR = "tools/oral/validate_correction_pret4.py"

QB6 = "meoclass1/QB6.html"
SHEET = "meoclass1/QB6_cheatsheet.html"
QB4E = "meoclass1/QB4_E.html"
NOTES = "meoclass1/oralnotes/simon-notes-p3.html"
QB3J = "meoclass1/QB3_J.html"
QB1I = "meoclass1/QB1_I.html"
MAN_CII = "tools/oral/correction_corr_pre_t4_cii_20260905_manifest.json"
MAN_Z7 = "tools/oral/correction_corr_pre_t4_z7esp_20260905_manifest.json"
REG = "docs/sources/MIW_SOURCE_REGISTRY.json"

# (spec, the check that MUST go red)
SPECS = [
    # ============ FAMILY A : CII capacity propagation closure ==============
    (replace_spec(
        "A1-equalise-qb6-the-wrong-way-15s", QB6,
        "measured in <strong>gCO₂ per capacity-nautical-mile</strong>",
        "measured in <strong>gCO₂/DWT·nm</strong>",
        intended_reason="the regression this pass invited: instead of q2 being "
                        "raised to q1, q1 is dragged down to q2's old wording. "
                        "A gate that watched only the corrected card would "
                        "sleep through the file being equalised backwards"),
     "cii_q1_still_teaches_capacity_not_universal_dwt"),

    (replace_spec(
        "A2-drop-q1-gt-limb", QB6,
        "gross tonnage (GT) for cruise passenger ships",
        "gross tonnage for certain ship types",
        intended_reason="the ship-type distinction blurred away in q1, which "
                        "is how a universal quietly returns without the literal "
                        "wrong string ever being typed"),
     "cii_q1_still_carries_the_ship_type_split"),

    (replace_spec(
        "A3-revert-q2-contrast-row", QB6,
        "<li><strong>CII</strong> — gCO₂ per capacity·nm (capacity is ship-type "
        "specific: <strong>DWT</strong> for the cargo categories, "
        "<strong>GT</strong> for the ro-ro, vehicle-carrier and cruise passenger "
        "categories)",
        "<li><strong>CII</strong> — gCO₂/DWT·nm",
        intended_reason="the exact defect this record corrected, put back at the "
                        "site where the unit IS the whole content of the row"),
     "cii_q2_no_universal_form_1"),

    (replace_spec(
        "A4-strip-q2-ship-type-scope-without-typing-dwt-nm", QB6,
        "capacity is ship-type specific",
        "capacity is the relevant tonnage",
        intended_reason="the scope removed while the corrected UNIT survives -- "
                        "a card that says 'capacity·nm' and never says what "
                        "capacity is has not actually taught the correction"),
     "cii_q2_carries_the_ship_type_distinction"),

    (replace_spec(
        "A5-pad-the-q2-15s-layer", QB6,
        "Unlike CII which measures operational efficiency per voyage",
        "Unlike CII, measured in gCO₂/DWT·nm, which measures operational "
        "efficiency per voyage",
        intended_reason="the brief required the short layers to stay concise. "
                        "This is the tempting wrong fix: pushing the correction "
                        "into a 15-second answer that never stated a unit"),
     "cii_q2_15s_layer_still_states_no_cii_unit"),

    (replace_spec(
        "A6-eat-a-correctly-scoped-card", QB3J,
        "in gCO&#8322;/DWT·nm for my ship type",
        "in gCO&#8322;/DWT·nm",
        intended_reason="COLLATERAL DAMAGE, not the defect. QB3_J was already "
                        "correct BECAUSE of its scope clause; a pattern-only "
                        "sweep would have left the unit and eaten the clause. "
                        "The gates must notice a card being broken, not only a "
                        "card failing to be fixed"),
     "cii_scoped_occurrences_kept_qb3j"),

    (replace_spec(
        "A7-revert-the-cheatsheet-formula", SHEET,
        "Attained CII (gCO₂ per capacity·nm)", "Attained CII (gCO₂/DWT·nm)",
        intended_reason="the revision layer reverting while the cards stay "
                        "correct -- the split this pass existed to close, "
                        "reopened from the side a candidate actually revises from"),
     "cii_cheatsheet_formula_uses_capacity"),

    (replace_spec(
        "A8-revert-the-nair-reflex-tip", SHEET,
        "Always say gCO₂ per capacity·nm", "Always say gCO₂/DWT·nm",
        intended_reason="the single worst site on the page: it drills the unit "
                        "as a reflex, for the examiner the card names by name"),
     "cii_cheatsheet_examiner_tip_drills_capacity_first"),

    (replace_spec(
        "A9-delete-the-capacity-replacement-rows", SHEET,
        '<div class="kv"><span class="k">Capacity C</span>',
        '<div class="kv"><span class="k">Capacity note</span>',
        intended_reason="the replacement fact removed while the wrong one stays "
                        "removed -- leaving a cheat sheet with a capacity unit "
                        "and no capacity term. Deleting an error is not the "
                        "same as teaching the correction"),
     "cii_cheatsheet_states_what_capacity_is"),

    (replace_spec(
        "A10-sweep-the-eedi-reference-line", SHEET,
        "Ref Line = a × DWT<sup>−c</sup>",
        "Ref Line = a × capacity<sup>−c</sup>",
        intended_reason="over-correction: the EEDI reference line is genuinely "
                        "DWT-based. This is the false positive a bounded sweep "
                        "is bounded to avoid"),
     "cii_eedi_reference_line_preserved"),

    (replace_spec(
        "A11-hide-the-predecessor-undercount", MAN_CII,
        "carried the literal gCO2/DWT.nm at FIVE sites",
        "carried the literal gCO2/DWT.nm at several sites",
        intended_reason="the deferral list's own miscount quietly absorbed "
                        "instead of recorded. A deferral list is the instruction "
                        "the next pass works from, and one that undercounts is "
                        "how a residual survives a cleanup that believes it is "
                        "complete"),
     "cii_manifest_records_the_predecessor_undercount"),

    # ============ FAMILY B : UR Z7 is not ESP ==============================
    (replace_spec(
        "B1-restore-z7-as-esp-in-the-numbers-box", QB4E,
        "2011 ESP Code (IMO res. A.1049(27)), mandatory under SOLAS Reg XI-1/2: "
        "the Enhanced Survey Programme for bulk carriers and oil tankers.",
        "IACS UR Z7: ESP for Bulk Carriers and Tankers.",
        intended_reason="the exact false teaching the brief named, put back in "
                        "the Numbers/Regs box a candidate memorises from"),
     "z7_q9_no_longer_calls_z7_esp"),

    (replace_spec(
        "B2-restore-z7-as-esp-as-the-worked-example", QB4E,
        "like UR Z7 for hull classification surveys, and the UR Z10 series for "
        "the enhanced hull surveys of bulk carriers and oil tankers",
        "like UR Z7 for the Enhanced Survey Programme",
        intended_reason="worse than a stray citation: q12 teaches the CONCEPT "
                        "of a Unified Requirement through this example, so the "
                        "error is the part the candidate retains"),
     "z7_q12_no_longer_calls_z7_esp"),

    (replace_spec(
        "B3-delete-z7s-true-subject", QB4E,
        "<strong>UR Z7 is &ldquo;Hull Classification Surveys&rdquo;</strong>, "
        "applicable to all self-propelled vessels — it is the baseline hull "
        "survey requirement, not ESP.",
        "UR Z7 is a separate requirement.",
        intended_reason="the replacement fact removed while the error stays "
                        "removed. A candidate who has memorised 'Z7 = ESP' "
                        "needs to be told what Z7 IS, not merely what it is not"),
     "z7_q9_states_what_z7_actually_is"),

    (replace_spec(
        "B4-invent-a-z10-sub-number", QB4E,
        "The corresponding class requirements are the IACS UR <strong>Z10</strong> series.",
        "The corresponding class requirement is IACS UR <strong>Z10.1</strong> "
        "for bulk carriers and <strong>Z10.2</strong> for oil tankers.",
        intended_reason="THE TRAP THE BRIEF EXPRESSLY FORBADE. Read strictly, "
                        "UR Z7 sec.1.1.3's 'respectively' maps tankers to Z10.1 "
                        "and bulk carriers to Z10.2 -- the OPPOSITE of this "
                        "plausible substitution. Nothing held resolves it, so a "
                        "sub-number here is invented precision: a new defect "
                        "wearing the corrected one's clothes"),
     "z7_q9_asserts_no_guessed_z10_sub_number"),

    (replace_spec(
        "B5-swap-statutory-authority-back-to-a-ur", QB4E,
        "mandatory under SOLAS Reg XI-1/2 and the 2011 ESP Code",
        "mandatory under the IACS Unified Requirements",
        intended_reason="the category error underneath the whole finding: ESP "
                        "is binding because SOLAS makes the ESP Code mandatory, "
                        "not because a class society published a UR. A UR binds "
                        "member societies' rules; it does not bind a flag State"),
     "z7_q9_cites_the_statutory_esp_authority"),

    (replace_spec(
        "B6-restore-z7-1-as-esp-in-the-notes", NOTES,
        "mandatory under SOLAS Reg XI-1/2 and the 2011 ESP Code "
        "(IMO res. A.1049(27)), with the corresponding class requirements in "
        "the IACS UR Z10 series. (UR Z7 is Hull Classification Surveys; UR Z7.1 "
        "is the water level detector requirement for single-hold cargo ships — "
        "neither is ESP.)",
        "mandatory under IACS UR Z7.1.",
        intended_reason="the same defect under a DIFFERENT sub-number, which is "
                        "exactly why it survived every earlier pass that "
                        "searched for the literal string 'Z7'. Found by the "
                        "sweep, not by the brief"),
     "z7_notes_no_longer_calls_z7_1_esp"),

    (replace_spec(
        "B7-damage-the-alignment-target", QB1I,
        "aligns closely with IACS UR Z10", "aligns closely with IACS UR Z7",
        intended_reason="COLLATERAL DAMAGE. QB1_I#q1 is the already-correct card "
                        "these corrections were written TO. Breaking it would "
                        "leave the corpus internally consistent and uniformly "
                        "wrong -- the worst possible outcome of a propagation "
                        "pass, and the one no per-card check would catch"),
     "z7_esp_alignment_target_intact"),

    (replace_spec(
        "B8-mis-title-the-z7-registry-row", REG,
        '"title": "IACS Unified Requirement Z7 - Hull Classification Surveys"',
        '"title": "IACS Unified Requirement Z7 - Enhanced Survey Programme"',
        intended_reason="the defect reintroduced at the CUSTODY layer rather "
                        "than in a card. The registry was right while the "
                        "corpus was wrong; if the registry is corrupted too, "
                        "nothing is left to re-derive the truth from"),
     "z7_registry_title_is_hull_classification_surveys"),

    (replace_spec(
        "B9-break-the-z7-custody-hash", REG,
        "6b1e62488d85f230d970e0beed7b13cab76afc6812a1112ae2fd29788282ea84",
        "6b1e62488d85f230d970e0beed7b13cab76afc6812a1112ae2fd29788282ea48",
        intended_reason="the registry hash no longer matches the held bytes -- "
                        "custody claimed but not real, so the sec.1.1.3 evidence "
                        "this whole family rests on becomes unverifiable"),
     "z7_registry_sha_matches_disk"),

    (replace_spec(
        "B10-bury-the-unresolved-sub-number", MAN_Z7,
        "is UNRESOLVED and is referred to GPT",
        "is a matter of numbering convention",
        intended_reason="the open question silently closed. The ambiguity is "
                        "real and becomes live the moment a card needs "
                        "sub-number precision; a record that hides it hands the "
                        "next pass a false all-clear"),
     "z7_manifest_records_the_unresolved_sub_number"),

    # ============ FAMILY C : the restraint gates ===========================
    (replace_spec(
        "C1-move-the-hub-date", "meoclass1/index.html",
        "2 Sep 2026", "5 Sep 2026",
        intended_reason="the brief forbade a hub-date change. A restraint gate "
                        "that cannot detect the forbidden act is decoration",
        count=-1),
     "restraint_hub_date_unchanged"),
]


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
                print("FAIL      %-42s spec applied no bytes at run time"
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
                                       "no owning check; new failures=%s"
                                       % (new or "none"))
                else:
                    verdict, detail = mutation_verdict(
                        expected, now, control,
                        validator_fail_details(mout), baseline_details)
                    if verdict == "escape":
                        escapes += 1
            finally:
                path.write_bytes(original)
            results.append((spec.mutation_id, verdict, detail))
            print("%-9s %-42s %s" % (verdict.upper(), spec.mutation_id, detail))
            print("          why: %s" % spec.intended_reason)
    finally:
        for rel, data in snapshot.items():
            (REPO / rel).write_bytes(data)
        after = {rel: (REPO / rel).read_bytes() for rel in snapshot}
        bad = [rel for rel in snapshot if after[rel] != snapshot[rel]]
        print("\nrestore: %d file(s), byte-exact=%s"
              % (len(snapshot), "yes" if not bad else "NO -- %s" % bad))

    _code2, out2 = run_validator()
    print("post-suite control: %s"
          % ("clean" if validator_failing(out2) == control else "DRIFTED"))
    counted = [r for r in results if r[1] != "reported"]
    print("\nPre-Tranche-4 cleanup mutations=%d escapes=%d"
          % (len(counted), escapes))
    return 1 if escapes else 0


if __name__ == "__main__":
    sys.exit(main())
