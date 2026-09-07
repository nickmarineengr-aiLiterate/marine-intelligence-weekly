#!/usr/bin/env python3
"""Mutation suite for the D01-S01 study-path corrections.

Nine mutations, one per corrected proposition, each reintroducing the DEFECT
into the live corpus and requiring a NAMED gate to go red. No digest-only
credit: a mutation that only moves bytes proves the digest pin works and
proves nothing about the teaching.

Two of these are deliberately awkward. F removes the Owner/Flag notification -
an OMISSION rather than a wrong statement, and omissions are what a negative
check cannot see. I deletes a survey-regime distinction, which is the shape of
the original defect: nothing false is written, the two regimes simply stop
being distinguished.

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
QB1_K = QB / "QB1_K.html"
QB1_H = QB / "QB1_H.html"
QP2506 = QB / "pastpapers/QP2506.html"
SKEL = REPO / "docs/study/TOPIC_01_STATUTORY_SURVEYS_AND_CLASS.md"

GATE = "validate_correction_d01s01.py"

WATCHED = [QB3_B, QB1_K, QB1_H, QP2506, SKEL]

#: (id, description, apply, required_check)
MUTATIONS = [
    ("A", "restore the 5-year HSSC framework attribution",
     sub_in_file(QB3_B,
                 "It runs on a <strong>5-year class survey cycle</strong>",
                 "It operates on a <strong>5-year HSSC cycle</strong>",
                 count=1),
     "RC01_class_system_not_said_to_operate_on_HSSC"),

    ("A2", "restore the IACS HSSC Guidelines attribution",
     sub_in_file(QB3_B,
                 '<span class="reg-code">IACS UR Z series</span>',
                 '<span class="reg-code">IACS HSSC Guidelines</span>',
                 count=1),
     "RC01_IACS_HSSC_attribution_gone_corpus_wide"),

    ("B", "restore the instrument legal-force ladder",
     sub_in_file(SKEL,
                 "1. **IMO instrument families & legal effect** — *not* a ladder.",
                 "1. **The IMO instrument hierarchy** — Convention → Protocol → Code → Resolution → Circular.",
                 count=1),
     "RC03_ladder_gone_from_the_skeleton"),

    ("C", "restore Net-Zero as adopted",
     sub_in_file(QP2506,
                 "<b>It has still not been adopted.</b>",
                 "The Net-Zero Framework was adopted at that session.",
                 count=1),
     "RC04_netzero_not_stated_as_adopted"),

    ("D", "restore 'overdue CoC automatically suspends class'",
     sub_in_file(QB1_K,
                 "the vessel's class becomes <strong>subject to a suspension procedure</strong>",
                 "class is <strong>automatically suspended</strong>",
                 count=1),
     "RC05_suspension_procedure_named"),

    ("E", "restore the blanket statutory-certificate collapse",
     sub_in_file(QB1_K,
                 "<strong>certain statutory certificates are implicitly invalidated</strong> (PR1C B.1.1&ndash;B.1.3)",
                 "it collapses the statutory certificates issued on class's behalf",
                 count=1),
     "RC05_certain_statutory_certificates_preserved"),

    ("F", "REMOVE the Owner/Flag written notification (an omission, not an error)",
     sub_in_file(QB1_K,
                 "the society must confirm it <strong>in writing to the Owner and to the Flag State</strong>, and for SOLAS ships that letter states",
                 "for SOLAS ships the society's letter states",
                 count=1),
     "RC05_owner_and_flag_notification_present"),

    ("G", "restore the universal UI interpretation claim",
     sub_in_file(QB1_H,
                 "A UI is a <strong>fallback for uniform implementation, not a binding interpretation of the convention</strong>",
                 "Once accepted UIs become the standard by which Flag States and ROs interpret the convention",
                 count=1),
     "RC06_UI_not_universal_flag_binding"),

    ("H", "restore 'PR 1C = transfer of class'",
     sub_in_file(QB1_H,
                 "PR 1C — suspension and reinstatement or withdrawal of class where surveys or conditions of class go overdue",
                 "PR 1C &mdash; transfer of class",
                 count=1),
     "RC06_PR1C_not_attributed_to_transfer_of_class"),

    ("I", "DELETE one corrected survey-regime distinction (the original defect's shape)",
     sub_in_file(QB3_B,
                 "<li><strong>Docking / Bottom Survey:</strong>",
                 "<li hidden><strong>Docking / Bottom Survey:</strong>",
                 count=1),
     "RC02_survey_list_is_complete"),
]


def main() -> int:
    title = "D01-S01 study-path corrections - mutation suite"
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
            print("%-4s %-62s CRASH   [%s]" % (mid, desc[:62], exc))
            snap.restore()
            continue
        _rc, failing = run_probe(GATE)
        hit = want in failing
        caught += 1 if hit else 0
        if not hit:
            problems.append("%s (wanted %s, got %s)"
                            % (mid, want, sorted(failing) or "nothing"))
        print("%-4s %-62s %s [%s]"
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
