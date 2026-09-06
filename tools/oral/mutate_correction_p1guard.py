#!/usr/bin/env python3
"""Mutation suite for the hardened detectors (P1GUARD-20260906).

Two kinds of mutation, because a guard has two ways to fail.

PRODUCT MUTATIONS reintroduce the defect into the live corpus in renderings that
defeated earlier implementations - a `<td>`, a `<dd>`, `&nbsp;`, a split tag,
`psi`, a range, and BMP5 taught as current in plain prose. Each must be caught
by the named corpus check in the repair gate.

DETECTOR MUTATIONS attack the guard itself. These are the ones the previous five
rounds needed and did not have: if a future edit narrows `oral_currentness` or
`oral_visible` back towards spelling-matching, the adversarial control set must
go red. Without them the module could silently regress to a phrase list and
every corpus check would stay green, because the corpus is clean.

The second kind is why this suite exists. A guard that is only tested against
today's corpus is tested against the one input on which it cannot fail.

Serial. No digest-only credit - each mutation names the substantive control.
"""
from __future__ import annotations

import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB_ROOT = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_content_mutation import (                    # noqa: E402
    Snapshot, run_probe, sub_in_file)

QB2_F = QB_ROOT / "QB2_F.html"
P1 = QB_ROOT / "oralnotes/miw-notes-mgmt-p1.html"
PASTPAPER = QB_ROOT / "pastpapers/QP2301.html"
CURRENTNESS = HERE / "oral_currentness.py"
VISIBLE = HERE / "oral_visible.py"

GATE = "validate_correction_p1repair.py"
CONTROLS = "test_currentness_detectors.py"

FIRE = "no_incomplete_scope_firemain_claim_anywhere"
BMP = "no_surface_teaches_BMP5_as_current"
HOST = '<div class="reg-box">'


def inject(path, payload):
    return sub_in_file(path, HOST, payload + HOST, count=1)


#: (id, description, apply, probe, required_check)
MUTATIONS = [
    # ---- product: the claim in renderings that beat earlier guards -------
    ("A", "single-limb claim in a <dd> - a tag no allowlist ever had",
     inject(QB2_F, "<dl><dt>Fire main</dt><dd>Minimum required hydrant "
                   "pressure 0.27 MPa</dd></dl>"), GATE, FIRE),
    ("B", "the same claim with &nbsp; between figure and unit",
     inject(QB2_F, "<p>Minimum required hydrant pressure 0.27&nbsp;MPa</p>"),
     GATE, FIRE),
    ("C", "the figure split across tags",
     inject(QB2_F, "<p>Minimum required hydrant pressure "
                   "<strong>0.27</strong> MPa</p>"), GATE, FIRE),
    ("D", "the claim in psi",
     inject(QB2_F, "<p>Minimum required hydrant pressure 39.16 psi</p>"),
     GATE, FIRE),
    ("E", "the claim as a range in a <figcaption>",
     inject(QB2_F, "<figure><figcaption>Minimum required hydrant pressure "
                   "0.27-0.35 MPa</figcaption></figure>"), GATE, FIRE),
    ("F", "BMP5 taught as current in plain prose",
     inject(P1, "<p>BMP5 is the current industry guidance for HRA transits."
                "</p>"), GATE, BMP),
    ("G", "BMP5 as a live code in a bare <td>",
     inject(P1, "<table><tr><td>BMP5</td><td>Ship hardening for HRA transits"
                "</td></tr></table>"), GATE, BMP),
    ("H", "a denial clause followed by a live claim in one sentence",
     inject(P1, "<p>BMP5 replaced BMP4, but BMP5 is what we apply today.</p>"),
     GATE, BMP),

    # ---- detector: narrow the guard back towards spelling-matching -------
    ("I", "make the pressure matcher require a figure adjacent to its unit "
          "(revert the range fix)",
     # Targets `_figures`, the one line that binds a unit to every figure in a
     # group. Earlier attempts rewrote the PRESSURE pattern instead, and both
     # failed silently: the substitution either missed a target split across
     # source lines, or produced a regex that still matched the range's LAST
     # figure and so changed nothing the checks could see. A mutation must
     # destroy the property, not merely edit near it.
     sub_in_file(CURRENTNESS, "    return re.findall(_NUM, group)",
                 "    return re.findall(_NUM, group)[-1:]", count=1),
     # Owned by the range-binding control, not by the aggregate MUST-CATCH
     # list: that check is the one whose PROPERTY this mutation destroys, and
     # crediting a mutation to the check that actually names its property is
     # the whole point of refusing digest-only kills.
     CONTROLS, "range_binds_its_unit_to_every_figure"),
    ("J", "drop the legacy units from the conversion table",
     sub_in_file(CURRENTNESS, '"kg/cm2": 0.0980665,', '', count=1),
     CONTROLS, "pressure_MUST_CATCH_all_renderings"),
    ("K", "restore element-wide denial suppression",
     sub_in_file(CURRENTNESS, "            why = _excused(sent, text, cls)",
                 "            why = _excused(text, text, cls)", count=1),
     CONTROLS, "bmp5_MUST_CATCH_live_claims"),
    ("L", "make the BMP5 detector default-INNOCENT again",
     sub_in_file(CURRENTNESS, "            if why is None:",
                 "            if why is not None:", count=1),
     CONTROLS, "bmp5_MUST_CATCH_live_claims"),
    ("M", "make the currentness exemption subject-BLIND",
     sub_in_file(CURRENTNESS,
                 "        if CURRENTNESS_MARK.search(body) and BMP5.search(body) \\\n"
                 "                and SUCCESSOR.search(body):",
                 "        if CURRENTNESS_MARK.search(body):", count=1),
     CONTROLS, "currentness_exemption_is_subject_specific"),
    ("N", "treat every tag as inline, so segments stop at nothing",
     sub_in_file(VISIBLE, 'INLINE = frozenset("""',
                 'INLINE = frozenset("""\ndiv p li td th dd dt figcaption\n',
                 count=1),
     CONTROLS, "bmp5_MUST_CATCH_live_claims"),
]

#: Must NOT be caught: sitting-anchored examiner wording is correct as written.
NON_CATCH = (
    "O", "historical BMP5 wording planted in a PAST PAPER - must NOT be caught",
    sub_in_file(PASTPAPER, '<div class="card"',
                "<div class='qa'><p>Candidates were expected to answer as per "
                "BMP5, the guidance current at the sitting.</p></div>"
                '<div class="card"', count=1))

WATCHED = [QB2_F, P1, PASTPAPER, CURRENTNESS, VISIBLE]


def main() -> int:
    title = "P1GUARD-20260906 - hardened detectors"
    print(title)
    print("=" * len(title))

    for probe in (GATE, CONTROLS):
        code, failing = run_probe(probe)
        if failing:
            print("control NOT green: %s -> %s" % (probe, sorted(failing)))
            return 2
        print("control green: %-42s exit %d" % (probe, code))
    print()

    caught, problems, crashes = 0, [], []
    for mid, desc, apply, probe, want in MUTATIONS:
        snap = Snapshot(WATCHED)
        try:
            apply()
        except Exception as exc:                        # noqa: BLE001
            crashes.append("%s: %s" % (mid, exc))
            print("%-3s %-62s CRASH   [%s]" % (mid, desc[:62], exc))
            snap.restore()
            continue
        _rc, failing = run_probe(probe)
        hit = want in failing
        caught += 1 if hit else 0
        if not hit:
            problems.append("%s (wanted %s in %s, got %s)"
                            % (mid, want, probe, sorted(failing) or "nothing"))
        print("%-3s %-62s %s [%s]"
              % (mid, desc[:62], "CAUGHT " if hit else "ESCAPED", want))
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2

    mid, desc, apply = NON_CATCH
    snap = Snapshot(WATCHED)
    try:
        apply()
        _rc, failing = run_probe(GATE)
    finally:
        bad = snap.restore()
    if bad:
        print("    RESTORE FAILED: %s" % bad)
        return 2
    ok = not failing
    caught += 1 if ok else 0
    if not ok:
        problems.append("%s (wrongly flagged: %s)" % (mid, sorted(failing)))
    print("\n%-3s %-62s %s" % (mid, desc[:62],
                               "CORRECTLY IGNORED" if ok
                               else "WRONGLY FLAGGED %s" % sorted(failing)))

    total = len(MUTATIONS) + 1
    print("\n%d of %d behaved as required" % (caught, total))
    print("%d mutations, %d failure(s), %d crash(es)"
          % (total, len(problems), len(crashes)))
    for p in problems:
        print("  PROBLEM " + p)
    for c in crashes:
        print("  CRASH   " + c)
    return 1 if (problems or crashes) else 0


if __name__ == "__main__":
    raise SystemExit(main())
