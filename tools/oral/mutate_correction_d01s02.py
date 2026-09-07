#!/usr/bin/env python3
"""Mutation suite for the three D01-S02 corrections.

Mutation A is the one that matters. The previous record's gate asserted the
absence of the STRING "IACS HSSC"; A reintroduces the class-cycle-is-HSSC
PROPOSITION using completely different words - the publication name spelled
out, no "IACS", no "cycle" adjacency - and requires the gate to catch it.
Under the previous gate it would have passed.

J is its twin from the other direction: it reverts ONE memorisation layer and
leaves the corrected REG-BOX in place, which is the exact state the two cards
were found in. A card-wide "is the phrase present somewhere" check cannot see
it, and that is why every layer is guarded by name.

Serial. Byte-exact restoration, verified after every mutation.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_content_mutation import (                    # noqa: E402
    Snapshot, run_probe, sub_in_file)

QB3_B = QB / "QB3_B.html"
SUPP = QB / "QB1_supplementary.html"
QB1_F = QB / "QB1_F.html"
QB1_G = QB / "QB1_G.html"
QB1_I = QB / "QB1_I.html"

GATE = "validate_correction_d01s02.py"
WATCHED = [QB3_B, SUPP, QB1_F, QB1_G, QB1_I]

MUTATIONS = [
    ("A", "class=HSSC in DIFFERENT WORDS - no 'IACS', name spelled out",
     # The point of the whole record. The previous gate looked for the string
     # "IACS HSSC"; none of these words is that string.
     sub_in_file(QB3_B,
                 "and follows the <strong>class survey cycle</strong> set by Class Rules",
                 "and follows the <strong>Harmonized System of Survey and Certification cycle</strong> set by Class Rules",
                 count=1),
     "no_conflation_in_any_card_this_record_touched"),

    ("B", "restore the statutory-cycle reset claim",
     sub_in_file(QB3_B,
                 "it <strong>resets the 5-year class survey cycle</strong>",
                 "it <strong>resets the 5-year HSSC clock</strong>",
                 count=1),
     "no_conflation_in_any_card_this_record_touched"),

    ("C", "restore A.1104(29) as the ESP instrument",
     sub_in_file(QB3_B,
                 '<span class="reg-code">IMO Res A.1049(27)</span>',
                 '<span class="reg-code">IMO Res A.1104(29)</span>',
                 count=1),
     "B_ESP_instrument_is_A1049"),

    ("D", "restore generic chemical-tanker ESP scope",
     sub_in_file(QB3_B,
                 "It applies to <strong>bulk carriers</strong> (Annex A) and <strong>oil tankers</strong> (Annex B) of <strong>500 GT and above</strong>.",
                 "It applies to bulk carriers, oil tankers and chemical tankers.",
                 count=1),
     "B_chemical_tankers_out_of_statutory_ESP_scope"),

    ("E", "restore the false ESP age threshold",
     sub_in_file(QB3_B,
                 "for bulk carriers and oil tankers of <strong>500 gross tonnage and above</strong>",
                 "for all bulk carriers and oil tankers aged 5 years and older",
                 count=1),
     "B_no_age_threshold_for_applicability"),

    ("F", "put the PMS machinery list back under the CMS heading",
     sub_in_file(SUPP,
                 "<p><strong>(B) Under an approved PMS (UR Z20) only &mdash; NOT available under CMS:</strong>",
                 "<p><strong>Also delegated to the Chief Engineer under CMS:</strong>",
                 count=1),
     "C_CMS_and_PMS_lists_are_separated"),

    ("G", "restore the crankshaft candidate-credit statement",
     sub_in_file(SUPP,
                 "carrying out the maintenance yourself is not the same as being able to credit the survey item",
                 "if your engineers carried out the overhaul you may credit the survey item",
                 count=1),
     "C_maintenance_is_not_credit"),

    ("H", "remove the multiple-engine qualification",
     sub_in_file(SUPP,
                 "main engine crankshafts and bearings &mdash; <em>multiple engine installations only</em></strong>",
                 "main engine crankshafts and bearings</strong>",
                 count=1),
     "C_multiple_engine_qualifier_restored"),

    ("I", "swap the Z18 / Z20 attribution",
     sub_in_file(SUPP,
                 "<p><strong>(A) Under CMS (UR Z18)",
                 "<p><strong>(A) Under CMS (UR Z20)",
                 count=1),
     "C_UR_attributions_unchanged_and_correct"),

    ("J", "revert ONE memorisation layer, leaving the REG-BOX corrected",
     # The state both cards were actually found in. A card-wide phrase check
     # is blind to it; the layer-scoped controls are not.
     sub_in_file(QB3_B,
                 "<h4>Post-Renewal Class Cycle Matrix</h4>",
                 "<h4>Post-Renewal HSSC Matrix</h4>",
                 count=1),
     "no_conflation_in_any_card_this_record_touched"),

    ("K", "reintroduce the IACS attribution of HSSC in a sibling card",
     sub_in_file(QB1_I,
                 "<strong>2011 ESP Code &mdash; Enhanced Programme of Inspections "
                 "(IMO res. A.1049(27))</strong> and the separate <strong>statutory HSSC "
                 "Survey Guidelines (IMO res. A.1207(34))</strong>:",
                 "<strong>IACS Extended Survey Programme (ESP)</strong> / "
                 "<strong>HSSC Guidelines</strong>:",
                 count=1),
     "corpus_wide_no_IACS_HSSC_and_no_HSSC_reset_claim"),

    ("L", "restore the tier-6 blog as the source for a hard survey number",
     sub_in_file(QB3_B,
                 '<span class="reg-code">IACS UR Z10.2</span>',
                 '<span class="reg-code">HSSC Annual Survey Checklist</span>',
                 count=1),
     "A_closeup_restricted_to_single_side_skin_bulk_carriers"),
]


def main() -> int:
    title = "D01-S02 study-path corrections - mutation suite"
    print(title)
    print("=" * len(title))

    code, failing = run_probe(GATE)
    if failing:
        print("control NOT green: %s -> %s" % (GATE, sorted(failing)))
        return 2
    print("control green: %-44s exit %d\n" % (GATE, code))

    caught, problems, crashes = 0, [], []
    for mid, desc, apply, want in MUTATIONS:
        snap = Snapshot(WATCHED)
        try:
            apply()
        except Exception as exc:                        # noqa: BLE001
            crashes.append("%s: %s" % (mid, exc))
            print("%-3s %-62s CRASH   [%s]" % (mid, desc[:62], exc))
            snap.restore()
            continue
        _rc, failing = run_probe(GATE)
        hit = want in failing
        caught += 1 if hit else 0
        if not hit:
            problems.append("%s (wanted %s, got %s)"
                            % (mid, want, sorted(failing) or "nothing"))
        print("%-3s %-62s %s [%s]"
              % (mid, desc[:62], "CAUGHT " if hit else "ESCAPED", want))
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2

    print("\n%d of %d behaved as required" % (caught, len(MUTATIONS)))
    print("%d mutations, %d failure(s), %d crash(es)"
          % (len(MUTATIONS), len(problems), len(crashes)))
    for p in problems:
        print("  PROBLEM " + p)
    for c in crashes:
        print("  CRASH   " + c)
    return 1 if (problems or crashes) else 0


if __name__ == "__main__":
    raise SystemExit(main())
