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
TOPICS = QB_ROOT / "topics.html"
CURRENTNESS = HERE / "oral_currentness.py"
VISIBLE = HERE / "oral_visible.py"

GATE = "validate_correction_p1repair.py"
CONTROLS = "test_currentness_detectors.py"

FIRE = "no_incomplete_scope_firemain_claim_anywhere"
BMP = "no_surface_teaches_BMP5_as_current"
HOST = '<div class="reg-box">'


def inject(path, payload):
    return sub_in_file(path, HOST, payload + HOST, count=1)


def both(*edits):
    """One mutation made of several edits.

    Needed where a property is defended REDUNDANTLY. The noun-list rule is
    protected twice over - the left side must contain a verb AND the right side
    must open with one - so removing either alone changes nothing the control
    can see. Two independent guards is the right design; the mutation that
    proves the control falsifiable therefore has to remove both, and pretending
    a single edit did it would credit the check with a kill it never made.
    """
    def apply():
        for e in edits:
            e()
    return apply


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
     sub_in_file(CURRENTNESS,
                 "            why = _excused(sent, text, cls, stack)",
                 "            why = _excused(text, text, cls, stack)",
                 count=1),
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

    # ================= E1-E4, the terminal closure ======================
    # PRODUCT first: the exact renderings the escapes named.
    ("E1-A", "denial + live claim joined by `and`, in one sentence",
     inject(P1, "<p>BMP5 replaced BMP4 and remains the current industry "
                "standard for HRA transits.</p>"), GATE, BMP),
    ("E2-A", "the same claim spelled BMP-5",
     inject(P1, "<p>BMP-5 is current guidance for ship hardening.</p>"),
     GATE, BMP),
    ("E3-A", "modal-free label:value hydrant figure",
     inject(QB2_F, "<li>Hydrant pressure - 0.27 N/mm&sup2;</li>"), GATE, FIRE),
    ("E3-B", "modal-free figure under a Key Numbers heading",
     inject(QB2_F, "<h4>Key numbers</h4><ul><li>hydrant 2.7 bar</li></ul>"),
     GATE, FIRE),
    ("E4-A", "subject in the heading, figure in the block beneath it",
     inject(QB2_F, "<div><h4>Fire main</h4><ul><li>Minimum 0.27 MPa</li>"
                   "</ul></div>"), GATE, FIRE),
    ("G2", "a topic label the GENERATOR authors, using BMP5 as current",
     sub_in_file(TOPICS, '<ul class="q-list">',
                 '<ul class="q-list"><li><a href="topics.html#D09">BMP5 is '
                 'the current piracy guidance</a></li>', count=1),
     GATE, BMP),

    # DETECTOR second. Each new control must be falsifiable, so each is
    # attacked at the one line that carries its property. Without these the
    # controls could be narrowed back to nothing and every corpus check would
    # stay green, because the corpus is clean.
    ("E1-D", "drop subject inheritance across coordinated clauses",
     sub_in_file(CURRENTNESS, "            elif subject_group != group:",
                 "            elif True:", count=1),
     CONTROLS, "E1_MUST_CATCH_denial_then_live_claim"),
    ("E1-E", "let a coordinator split a NOUN list too (BOTH defenders)",
     # The noun-list rule is defended TWICE, and this mutation is how that was
     # discovered: removing one defender killed nothing, and reported an
     # escape the guard had not actually suffered. The two are the both-sides
     # verb test - a noun list predicates only once - and the rule that a
     # verbless fragment MERGES FORWARD rather than standing as a proposition.
     # Redundancy is good design and bad for a mutation suite: a mutation that
     # leaves the property standing credits itself with a kill it never made.
     both(
         sub_in_file(
             VISIBLE,
             "        if not (_HAS_VERB.search(left) and _HAS_VERB.search(right)):",
             "        if False:", count=1),
         sub_in_file(
             VISIBLE,
             "        if not _HAS_VERB.search(part) and "
             "part is not parts[-1]:",
             "        if False:", count=1)),
     CONTROLS, "E1_coordinator_splits_clauses_not_noun_lists"),
    ("E2-D", "revert the name to the un-hyphenated spelling only",
     sub_in_file(CURRENTNESS, r'BMP5 = re.compile(r"\bBMP[\s\-]?5\b", re.I)',
                 r'BMP5 = re.compile(r"\bBMP\s?5\b", re.I)', count=1),
     CONTROLS, "E2_hyphenated_name_is_the_same_publication"),
    ("E3-D", "require a modal again - revert label:value and numbers context",
     sub_in_file(CURRENTNESS,
                 '    return "a governed limb asserted of the fire main"',
                 "    return None", count=1),
     CONTROLS, "E3_MUST_CATCH_modal_free_governing_figure"),
    ("E4-D", "let a label reach across its container boundary",
     sub_in_file(VISIBLE,
                 "            if left > 0 and serials[:len(lparent)] == lparent:",
                 "            if left > 0:", count=1),
     CONTROLS, "E4_label_does_not_leak_across_containers"),
    ("G-D", "give generated pages a blanket exemption again",
     sub_in_file(CURRENTNESS, '    if _stem_echo(stack):',
                 '    if _stem_echo(stack) or "q-list" in cls:', count=1),
     CONTROLS, "generated_surface_status_follows_item_provenance"),
]

#: Must NOT be caught. Three ways to be innocent, each the mirror of a
#: mutation above: a sitting is anchored in time; a coordinated sentence can be
#: wholly historical; a heading in a CLOSED sibling lends no subject; and a
#: generated row that quotes an examiner is still the examiner's words.
NON_CATCH = [
    ("O", "historical BMP5 wording planted in a PAST PAPER",
     sub_in_file(PASTPAPER, '<div class="card"',
                 "<div class='qa'><p>Candidates were expected to answer as per "
                 "BMP5, the guidance current at the sitting.</p></div>"
                 '<div class="card"', count=1)),
    ("E1-B", "a wholly historical coordinated sentence",
     inject(P1, "<p>BMP5 replaced BMP4 and was itself superseded by BMP "
                "Maritime Security.</p>")),
    ("E4-B", "an unrelated heading must not lend its subject to the next block",
     inject(QB2_F, "<div><h4>Lifeboat davits</h4></div>"
                   "<div><ul><li>Minimum 0.27 MPa</li></ul></div>")),
    ("G1", "a generated row echoing a historical examiner stem",
     sub_in_file(TOPICS, '<ul class="q-list">',
                 '<ul class="q-list"><li><a href="QB9_A.html#q9">BMP5 '
                 'measures for a war risk area.</a></li>', count=1)),
]

WATCHED = [QB2_F, P1, PASTPAPER, TOPICS, CURRENTNESS, VISIBLE]


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
            print("%-5s %-60s CRASH   [%s]" % (mid, desc[:60], exc))
            snap.restore()
            continue
        _rc, failing = run_probe(probe)
        hit = want in failing
        caught += 1 if hit else 0
        if not hit:
            problems.append("%s (wanted %s in %s, got %s)"
                            % (mid, want, probe, sorted(failing) or "nothing"))
        print("%-5s %-60s %s [%s]"
              % (mid, desc[:60], "CAUGHT " if hit else "ESCAPED", want))
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2

    print()
    for mid, desc, apply in NON_CATCH:
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
        print("%-5s %-60s %s" % (mid, desc[:60],
                                 "CORRECTLY IGNORED" if ok
                                 else "WRONGLY FLAGGED %s" % sorted(failing)))

    total = len(MUTATIONS) + len(NON_CATCH)
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
