#!/usr/bin/env python3
"""Mutation suite for CORR-P1REPAIR-20260906 and the gates it hardened.

This suite is different in shape from its siblings: the defects it guards live
in FOUR gates, so each mutation names the probe that must catch it. A single
-probe runner would have had to leave the struct, reach and scope controls
untested, which is how the hardening would rot.

EVERY MUTATION HERE CORRESPONDS TO A CHECK THAT USED TO PASS WHILE ASSERTING
NOTHING. That is the point. The Pass-1 suites were green and their gates were
wrong, so a green suite proves nothing unless each mutation reaches a state the
old check could not distinguish:

  A/B/C  the escaped figure in three capitalisations. B and C are the ones that
         matter: the Pass-1 check was written against the lower-case spelling
         and the Pass-1 mutation reinserted the lower-case spelling, so the
         guard looked proved while the corpus carried "4.0 Bar".
  D      the recursive glob reverted to top-level. This is the scope defect
         itself, replayed.
  E      a newly-corrected oralnotes site reverted - proving the recursive gate
         actually reads the 96 files Pass 1 could not see.
  F      a repaired dd-block body altered while its class and label stay
         identical - invisible to the Pass-1 check, which compared only
         (class, label).
  G      derived_bytes faked in the manifest - the Pass-1 check read the
         record's own number and asked only whether it exceeded 50,000.
  H      the N1 footer check fed nothing but version-stamp text.
  I      single-limb 0.27 restored on the cheat sheet.
  J      the literal-True pseudo-check restored - it must be REJECTED as a
         suite error, not counted as a passing control.

Digest-only catches do not count and the runner refuses them. Serial only.
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
    Snapshot, edit_json, run_probe, sub_in_file)

MANIFEST = HERE / "correction_corr_p1repair_20260906_manifest.json"
STRUCT_MANIFEST = HERE / "correction_corr_t5_ddcascade_20260906_manifest.json"
QB2_H = QB_ROOT / "QB2_H.html"
QB1_G = QB_ROOT / "QB1_G.html"
QB4_H = QB_ROOT / "QB4_H.html"
CS2B = QB_ROOT / "QB2_B_CheatSheet.html"
P10 = QB_ROOT / "oralnotes/miw-notes-mgmt-p10.html"
CENSUS = HERE / "census_known_defect_families.py"
STRUCT_GATE = HERE / "validate_correction_t5struct.py"
REACH_GATE = HERE / "validate_correction_t5reach.py"
HYD_GATE = HERE / "validate_correction_t5hydrant.py"

P1REPAIR = "validate_correction_p1repair.py"
STRUCT = "validate_correction_t5struct.py"
REACH = "validate_correction_t5reach.py"
SCOPE = "test_corpus_scope.py"

#: The corrected Key Numbers entry, and the three spellings of the escape.
KEY_NUM_NOW = ('<li><strong>0.27 / 0.25 N/mm&sup2;:</strong> SOLAS '
               'II-2/10.2.1.6 minimum pressure at the hydrants')


def reinsert(spelling):
    """Put the false figure back, in one capitalisation."""
    return sub_in_file(
        QB2_H, KEY_NUM_NOW,
        '<li>%s: Minimum operational pressure required at the furthest deck '
        'hydrant.</li>%s' % (spelling, KEY_NUM_NOW), count=1)


def revert_glob():
    return sub_in_file(CENSUS, 'return sorted(QB_ROOT.rglob("*.html"))',
                       'return sorted(QB_ROOT.glob("*.html"))', count=1)


def alter_a_repaired_body():
    """Change a dd-block body, leaving its class and label untouched."""
    # Spliced BY OFFSET, not by string replacement.
    #
    # The first version passed the body text to a replace(). That text also
    # occurs earlier in the page outside any dd-block, so the mutation edited
    # the wrong copy: the dd-block was untouched, the body check correctly saw
    # no change, and the mutation reported ESCAPED while never having reached
    # the surface under test. A mutation that edits the wrong occurrence
    # exercises nothing - the same trap as the JSON-LD copy of a q-text stem.
    from analyse_ddcascade import DD_BLOCK

    def apply():
        text = QB1_G.read_text(encoding="utf-8")
        m = next(x for x in DD_BLOCK.finditer(text) if len(x.group(3)) > 60)
        s, e = m.start(3), m.end(3)
        assert "CONTENT SILENTLY REPLACED" not in text
        QB1_G.write_bytes((text[:s] + "CONTENT SILENTLY REPLACED" + text[e:])
                          .encode("utf-8").replace(b"\r\n", b"\n"))
    return apply


def fake_bytes(d):
    d["invariants"]["duplicated_bytes_removed"] = 99999


def stamp_only_footer():
    """Make the N1 check's evidence exist ONLY in the version stamp.

    The Pass-1 check read the whole card for the word "unverifiable", which
    lives only in the q-version stamp - so it was satisfied by provenance and
    tested nothing. The hardened check reads the teaching layers, so removing
    the footer's current-publication citation must now fail.
    """
    return sub_in_file(
        QB4_H,
        'the held <strong>BMP Maritime Security, 1st Edition (2025) as updated '
        'June 2026</strong> (safe muster point vs. citadel)',
        'the applicable industry guidance', count=1)


#: (id, description, apply, probe, required_check)
MUTATIONS = [
    ("A", "reinsert the escaped figure as '4.0 bar'",
     reinsert("4.0 bar"), P1REPAIR,
     "P0A_no_bar_figure_survives_as_a_hydrant_minimum"),
    ("B", "reinsert it as '4.0 Bar' - the spelling that ESCAPED Pass 1",
     reinsert("4.0 Bar"), P1REPAIR,
     "P0A_no_bar_figure_survives_as_a_hydrant_minimum"),
    ("C", "reinsert it as '4.0 BAR'",
     reinsert("4.0 BAR"), P1REPAIR,
     "P0A_no_bar_figure_survives_as_a_hydrant_minimum"),

    ("D", "revert the corpus enumeration to a top-level glob",
     revert_glob(), SCOPE,
     "enumeration_is_strictly_larger_than_top_level"),
    ("D2", "the same revert, seen by the repair gate's own scope check",
     revert_glob(), P1REPAIR, "gate_reads_the_recursive_corpus"),

    ("E", "revert the false 2024 BMP5 date in oralnotes",
     sub_in_file(P10,
                 '<span class="t-year">2025</span>  BMP Maritime Security '
                 'replaces',
                 '<span class="t-year">2024</span>  BMP5 supersedes BMP4 — '
                 'replaces', count=1),
     P1REPAIR, "oralnotes_false_2024_date_is_gone"),
    ("E2", "restore a BMP5 reg-code slot in a file Pass 1 could not see",
     sub_in_file(P10,
                 '<span class="reg-code">BMP Maritime Security</span>'
                 '<span class="reg-desc">Industry ship-hardening',
                 '<span class="reg-code">BMP5</span>'
                 '<span class="reg-desc">Industry ship-hardening', count=1),
     P1REPAIR, "no_reg_code_slot_names_BMP5_as_current"),

    ("F", "alter a repaired dd-block body, class and label unchanged",
     alter_a_repaired_body(), STRUCT,
     "every_typed_block_survived_the_repair"),

    ("G", "fake the duplicated-byte count in the struct manifest",
     edit_json(STRUCT_MANIFEST, fake_bytes), STRUCT,
     "declared_duplicated_bytes_matches_baseline"),

    ("H", "leave only version-stamp text to satisfy the N1 footer check",
     stamp_only_footer(), REACH, "N1_footer_agrees_with_its_own_card_body"),

    ("I", "restore single-limb 0.27 on the cheat sheet",
     sub_in_file(CS2B,
                 '<li>Min hydrant pressure, two pumps running: <strong>0.27 '
                 'N/mm²</strong> at 6,000 GT and upwards, <strong>0.25 '
                 'N/mm²</strong> below (SOLAS II-2/10.2.1.6, cargo '
                 'ships)</li>',
                 '<li>Min hydrant pressure maintained: <strong>0.27 '
                 'N/mm²</strong></li>', count=1),
     P1REPAIR, "no_single_limb_hydrant_figure_anywhere"),
]

WATCHED = [QB2_H, QB1_G, QB4_H, CS2B, P10, CENSUS, MANIFEST, STRUCT_MANIFEST]


def literal_true_restored() -> bool:
    """J - a structural check on the gates themselves, not on the corpus."""
    for gate in (STRUCT_GATE, REACH_GATE, HYD_GATE,
                 HERE / "validate_correction_p1repair.py"):
        body = gate.read_text(encoding="utf-8")
        if re.search(r"report\(\s*[\"'][a-z_]+[\"']\s*,\s*True\s*,", body):
            return True
    return False


def main() -> int:
    title = "CORR-P1REPAIR-20260906 + hardened Pass-1 gates"
    print(title)
    print("=" * len(title))

    probes = sorted({m[3] for m in MUTATIONS})
    controls = {}
    for probe in probes:
        code, failing = run_probe(probe)
        controls[probe] = failing
        if failing:
            print("control NOT green: %s -> %s" % (probe, sorted(failing)))
            return 2
        print("control green: %-42s exit %d" % (probe, code))
    print()

    caught, escapes, crashes = 0, [], []
    for mid, desc, apply, probe, want in MUTATIONS:
        snap = Snapshot(WATCHED)
        try:
            apply()
        except Exception as exc:                       # noqa: BLE001
            crashes.append("%s: %s" % (mid, exc))
            print("%-3s %-58s CRASH   [%s]" % (mid, desc, exc))
            snap.restore()
            continue
        _rc, failing = run_probe(probe)
        # A digest-only kill does not count. The named substantive check must
        # be the thing that fires.
        hit = want in failing
        if hit:
            caught += 1
        else:
            escapes.append("%s (wanted %s in %s, got %s)"
                           % (mid, want, probe, sorted(failing) or "nothing"))
        print("%-3s %-58s %s [%s]"
              % (mid, desc, "CAUGHT " if hit else "ESCAPED", want))
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2

    # ---- J : the pseudo-check must stay gone ---------------------------
    print()
    if literal_true_restored():
        print("J   literal-True pseudo-check is present in a gate      FAIL")
        escapes.append("J (a report(..., True, ...) check exists)")
    else:
        caught += 1
        print("J   no gate contains a report(..., True, ...) pseudo-check "
              "CAUGHT  [structural]")

    total = len(MUTATIONS) + 1
    print("\n%d caught of %d" % (caught, total))
    print("%d mutations, %d escape(s), %d crash(es)"
          % (total, len(escapes), len(crashes)))
    for e in escapes:
        print("  ESCAPE " + e)
    for c in crashes:
        print("  CRASH  " + c)
    return 1 if (escapes or crashes) else 0


if __name__ == "__main__":
    raise SystemExit(main())
