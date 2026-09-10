#!/usr/bin/env python3
"""Mutation suite for CORR-REL-BJ-ATTRIBUTION and CORR-REL-BJ-FOUNDERING.

Every mutation must trip the check that OWNS its proposition, never a digest
pin. Both cards ARE pinned, so a suite that accepted a pin catch would prove
only that sha256 works while leaving every claim in the correction unguarded.

THE THREE DIRECTIONS THIS SUITE TESTS
-------------------------------------
  * REGRESSION (A, B, C, F, G) - the card goes back to naming the IMO as the
    investigator, to stating the finding as a conclusion, or to five minutes.

  * SILENT WEAKENING (D, E, H, I) - the card keeps the shape of the correction
    and loses the thing that makes it teach. Dropping "as flag State" leaves a
    correct name attached to no rule. Dropping the 10% leaves 21.3% floating,
    which is a number with nothing to compare it to. Dropping one of the two
    candidate mechanisms re-hardens the finding while still saying "most
    probable". None of these looks wrong on the page, which is exactly why a
    reader-level review passes them and a named check has to exist.

  * OVER-SWEEP (J, K, L) - a later session runs a flat banned-phrase sweep for
    "5 minutes" or for "IMO" and destroys true content: QB5_A's heavy-weather
    limb, which was TESTED and kept, or the version stamps, which quote the
    rejected wording on purpose. This is the direction nobody writes a check
    for, and it is the one that removes correct teaching rather than leaving
    stale teaching in place - the exact failure the fifth Pass-2 review found.

MUTATION M IS THE VACUITY TRAP
------------------------------
It renames the `<h5>Casualty Link</h5>` heading while leaving the button label
that also reads "Casualty Link" in place. The first version of this gate
anchored on the words rather than the markup, extracted the wrong block, and
reported the rejected wording as ABSENT from a region that never contained it.
M reproduces that state, and the non-vacuity checks must catch it - if they do
not, every negative check in the gate is decoration.
"""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import (                    # noqa: E402
    edit_json, run_suite, sub_in_file)

QB8_A = REPO / "meoclass1/QB8_A.html"
QB5_A = REPO / "meoclass1/QB5_A.html"
QB10_B = REPO / "meoclass1/QB10_B.html"
SHEET = REPO / "meoclass1/QB2_B_CheatSheet.html"
TRAPS = REPO / "meoclass1/known_traps.md"
M_ATTR = HERE / "correction_corr_rel_bj_attribution_20260908_manifest.json"
M_FOUND = HERE / "correction_corr_rel_bj_foundering_20260908_manifest.json"
M_SHEET = HERE / "correction_corr_rel_bj_cheatsheet_20260909_manifest.json"
PROBE = "validate_correction_bulkjupiter.py"
# The artefact-governance probe. Deliberately NOT validate_corrections.py:
# that gate is the authority but runs `git show` over every tracked page per
# record, so a suite that used it would take minutes per mutation and would
# stop being run. Both call the same pin function, so they cannot disagree.
PROBE_GOV = "validate_artefact_governance.py"

# The pre-edit line, kept verbatim. It is the specimen every regression
# mutation below restores, and it is the exact wording the original
# closed-world guard read straight past.
SHEET_WAS = ("<li>Casualties: <em>MV Bulk Jupiter (2015)</em> — bauxite "
             "liquefaction sinking</li>")
SHEET_NOW = ("<li>Casualties: <em>MV Bulk Jupiter (2015)</em> — bauxite; "
             "most probably liquefaction or a free-surface effect (flag State "
             "found no physical evidence of cause)</li>")

MUTATIONS = [
    # ---- REGRESSION: who investigated -----------------------------------
    ("A", "put the investigation back on the IMO",
     sub_in_file(QB8_A,
                 "The marine safety investigation was carried out by the "
                 "<strong>Bahamas Maritime Authority</strong> as flag State",
                 "The subsequent investigation by the IMO concluded", count=1),
     "q4_does_not_attribute_the_investigation_to_the_imo"),

    ("B", "drop the express denial that the IMO investigates",
     sub_in_file(QB8_A,
                 "and the IMO does not investigate casualties; it received",
                 "and it received", count=1),
     "q4_denies_the_imo_investigated"),

    # ---- SILENT WEAKENING: a name without its rule ----------------------
    ("D", "name the right body but strip the flag-State role",
     sub_in_file(QB8_A,
                 "<strong>Bahamas Maritime Authority</strong> as flag State "
                 "&mdash; investigating a casualty is a flag-State duty under "
                 "SOLAS XI-1/6 and the Casualty Investigation Code, and",
                 "<strong>Bahamas Maritime Authority</strong> &mdash; and",
                 count=1),
     "q4_names_it_AS_flag_state"),

    # ---- REGRESSION: how strongly ---------------------------------------
    ("C", "harden the qualified finding back into a conclusion",
     sub_in_file(QB8_A,
                 "it concludes only that it is <em>most probable</em> that",
                 "it concludes that", count=1),
     "q4_states_the_finding_as_most_probable"),

    ("E", "keep 'most probable' but collapse the two mechanisms into one",
     sub_in_file(QB8_A,
                 "either liquefaction or a free-surface effect induced it",
                 "liquefaction induced it", count=1),
     "q4_carries_BOTH_candidate_mechanisms"),

    ("F", "delete the report's own no-physical-evidence qualification",
     sub_in_file(QB8_A,
                 "there is <em>no physical evidence</em> to confirm what caused "
                 "the unrecoverable list to starboard, and it",
                 "it", count=1),
     "q4_records_no_physical_evidence_of_cause"),

    # ---- SILENT WEAKENING: a number with nothing to compare it to -------
    ("H", "leave 21.3% standing but remove the declared 10% it is measured against",
     sub_in_file(QB8_A,
                 "of <strong>21.3%</strong> against the <strong>10%</strong> "
                 "declared",
                 "of <strong>21.3%</strong>", count=1),
     "q4_moisture_pair_is_a_PAIR"),

    ("I", "round the tonnage back to the wrong figure",
     sub_in_file(QB8_A, "46,400 tonnes", "46,000 tonnes", count=1),
     "q4_tonnage_is_46400"),

    ("N", "drop the crew denominator, keeping the toll",
     sub_in_file(QB8_A, "with the loss of 18 of her 19 crew",
                 "with the loss of 18 crew members", count=1),
     "q4_crew_toll_carries_its_denominator"),

    ("O", "drop the Group A BAUXITE FINES schedule the revision produced",
     sub_in_file(QB8_A,
                 " individual schedules, adding a separate Group A schedule for "
                 "BAUXITE FINES.",
                 " individual schedules for bauxite.", count=1),
     "q4_names_the_group_a_bauxite_fines_schedule"),

    # ---- REGRESSION: the number -----------------------------------------
    ("G", "put the five-minute claim back on QB5_A",
     sub_in_file(QB5_A,
                 "The vessel foundered in approximately 20 minutes in heavy "
                 "weather (NE monsoon, Beaufort 6&ndash;7) after the bauxite "
                 "cargo most probably liquefied or developed a free surface",
                 "The vessel sank within 5 minutes of bauxite cargo liquefying "
                 "in heavy weather", count=1),
     "q11_foundering_time_is_20_minutes"),

    ("P", "keep 20 minutes but re-assert the mechanism as settled",
     sub_in_file(QB5_A,
                 "after the bauxite cargo most probably liquefied or developed "
                 "a free surface",
                 "of the bauxite cargo liquefying", count=1),
     "q11_mechanism_is_not_asserted"),

    # ---- OVER-SWEEP: destroying content that was tested and kept --------
    ("J", "a flat sweep deletes the heavy-weather limb that was verified true",
     sub_in_file(QB5_A,
                 "in heavy weather (NE monsoon, Beaufort 6&ndash;7) ",
                 "", count=1),
     "q11_heavy_weather_preserved"),

    ("K", "a sweep for the rejected wording eats QB5_A's own version stamp",
     sub_in_file(QB5_A,
                 "&ldquo;sank within 5 minutes&rdquo;",
                 "an incorrect figure", count=1),
     "q11_stamp_quotes_what_it_rejected"),

    ("L", "a sweep for 'IMO' eats QB8_A's version stamp provenance",
     sub_in_file(QB8_A,
                 "marine safety investigation to the IMO and stated",
                 "marine safety investigation to the wrong body and stated",
                 count=1),
     "q4_stamp_quotes_what_it_rejected"),

    # ---- the vacuity trap ------------------------------------------------
    ("M", "rename the Casualty Link HEADING, leaving the button label that "
          "an earlier version of this gate anchored on",
     # Anchored on q11's OWN heading. The first version of this mutation said
     # `<h5>Casualty Link</h5>` alone and hit the first of many such headings in
     # QB5_A -- a different card entirely -- so it escaped by never touching the
     # card under test. A mis-aimed mutation reads exactly like a gate defect.
     sub_in_file(QB5_A,
                 "<h5>Casualty Link</h5><p>Bulk carrier Bulk Jupiter (2015)",
                 "<h5>Casualty Note</h5><p>Bulk carrier Bulk Jupiter (2015)",
                 count=1),
     "casualty_link_q11_extracted"),

    # ---- the corpus must not be allowed to disagree with itself ---------
    ("Q", "break the sibling's agreement on the moisture figure",
     # Re-aimed 2026-09-08: the earlier target string was rewritten by this
     # record's own QB10_B edit, so the mutation crashed on an absent target.
     sub_in_file(QB10_B, "<strong>21.3%</strong>", "<strong>12.3%</strong>",
                 count=1),
     "qb10b_moisture_agrees_with_q4"),

    ("R", "put the investigation back on the IMO, on the sibling page",
     # Re-aimed for the same reason as Q.
     sub_in_file(QB10_B,
                 "The <strong>Bahamas Maritime Authority</strong> investigated "
                 "her as flag State",
                 "The investigation by the IMO examined her", count=1),
     "no_other_page_attributes_the_investigation_to_the_imo"),

    # ---- the contradiction an independent verifier found ----------------
    # These four are the ones that matter. The first version of this gate had
    # no check that could see a sibling page asserting the cause as settled --
    # it asserted only the crew toll, the moisture figure and the presence of
    # "not a cargo shift", all of which agreed BEFORE the correction and so
    # could never detect a disagreement the correction created.
    # Surgical: removes ONLY the modal verb and leaves both mechanisms
    # standing, so it must trip the qualification check and nothing else. The
    # first version replaced the whole clause and tripped the mechanisms check
    # instead - a mutation that proves a different check from the one it names
    # is not evidence for the one it names.
    ("W", "state QB10_B's cause as established, keeping both mechanisms",
     sub_in_file(QB10_B,
                 "and it is <strong>most probable</strong> that either",
                 "and it is <strong>established</strong> that either", count=1),
     "cause_is_qualified_on_qb10b_site2"),

    ("X", "leave QB10_B qualified but drop the second mechanism",
     sub_in_file(QB10_B,
                 "<strong>liquefaction</strong> or a <strong>free-surface "
                 "effect</strong> induced it",
                 "<strong>liquefaction</strong> induced it", count=1),
     "cause_offers_both_mechanisms_on_qb10b_site2"),

    ("Y", "reinstate the exact sentence the verifier found, on the bullet",
     sub_in_file(QB10_B,
                 "is the standard illustration. The Bahamas Maritime Authority, "
                 "as flag State, found no physical evidence of the cause",
                 "is the standard illustration, and she was lost to bauxite "
                 "<strong>liquefaction</strong>, not a cargo shift. The flag "
                 "State found no physical evidence of the cause", count=1),
     "no_page_asserts_the_cause_as_settled"),

    # The true-and-kept limb, guarded in the other direction: a later sweep
    # removing "not a cargo shift" would delete a correct distinction.
    ("Z", "a sweep deletes the cargo-shift distinction that was kept on purpose",
     # count=1 removes the FIRST occurrence, which is the inclinometer bullet,
     # so this binds to site1. Named for the site it actually hits rather than
     # the one it was first assumed to hit.
     sub_in_file(QB10_B, " &mdash; not a cargo shift", "", count=1),
     "qb10b_site1_denies_the_cargo_shift_reading"),

    # ---- the records themselves -----------------------------------------
    ("S", "unhook the attribution record from known trap 131",
     edit_json(M_ATTR, lambda d: d.__setitem__("known_traps_entries", [128])),
     "trap_131_declared_attribution"),

    ("T", "unhook the foundering record from known trap 131",
     edit_json(M_FOUND, lambda d: d.__setitem__("known_traps_entries", [128])),
     "trap_131_declared_foundering"),

    ("U", "strip the flag-State duty out of known trap 131, leaving the anecdote",
     sub_in_file(TRAPS, "**SOLAS XI-1/6**", "the relevant SOLAS chapter",
                 count=1),
     "trap_131_names_the_flag_state_duty"),

    ("V", "withdraw the attribution record's authorisation",
     edit_json(M_ATTR, lambda d: d.__setitem__("status", "DRAFT")),
     "status_authorised_attribution"),

    # ---- the cheat sheet: the site the first gate could not see ----------
    # AA is the escape itself, reproduced. The pre-edit line said the rejected
    # proposition in words neither of the original guard's two literals
    # reached, so the corpus shipped a release in which every q-card was
    # pinned and the one page a candidate reads on the morning of the oral
    # contradicted all of them.
    ("AA", "restore the settled-cause wording to the cheat sheet",
     sub_in_file(SHEET, SHEET_NOW, SHEET_WAS, count=1),
     "cause_is_qualified_on_cheatsheet_site1"),

    ("AB", "keep 'most probably' on the cheat sheet but drop the second mechanism",
     sub_in_file(SHEET, "most probably liquefaction or a free-surface effect",
                 "most probably liquefaction", count=1),
     "cause_offers_both_mechanisms_on_cheatsheet_site1"),

    # NON-VACUITY. If a later edit removed the casualty from the cheat sheet
    # altogether, every per-site check above would pass over an empty list of
    # sites and the gate would report green on a page that teaches nothing.
    ("AC", "delete the casualty bullet entirely",
     sub_in_file(SHEET, SHEET_NOW, "", count=1),
     "cheatsheet_sites_found"),

    # OVER-SWEEP, in the cheat sheet's direction: a later sweep for the
    # rejected word takes the mechanism out of the teaching with it.
    ("AD", "a sweep for 'liquefaction' eats the TML rule the bullet sits under",
     sub_in_file(SHEET,
                 "Cannot load Group A if moisture content &gt; TML",
                 "Cannot load Group A cargo", count=1),
     "cheatsheet_teaches_the_tml_rule"),
]

# The artefact-governance mutations. These run against PROBE_GOV, because the
# propositions they attack live in the RECORD rather than on the page.
#
# Three of them are answered by a digest or a pin, which the card suite refuses
# as a catch. The rule is not inverted here, it is being applied: for a q-card
# the pin is incidental to the content check that owns the proposition, so
# accepting it proves only that sha256 works. For the artefact form the pin IS
# the mechanism under test -- it is the thing that did not exist when the cheat
# sheet shipped a rejected proposition -- so a mutation that the pin does not
# catch is a mechanism that does not work.
GOVERNANCE_MUTATIONS = [
    ("GA", "remove the cheat sheet from artefact governance",
     edit_json(M_SHEET, lambda d: d.__setitem__("governed_artefacts", [])),
     "governed_artefacts_non_empty"),

    ("GB", "corrupt the artefact's post-edit digest",
     edit_json(M_SHEET, lambda d: d["governed_artefacts"][0].__setitem__(
         "post_edit_digest", "0" * 64)),
     "live_matches_authorised_artefact_state"),

    ("GC", "point the record at a parent correction that does not exist",
     edit_json(M_SHEET, lambda d: d["governed_artefacts"][0].__setitem__(
         "governing_correction", "CORR-DOES-NOT-EXIST-20260909")),
     "governed_artefact_parent_exists"),

    # LINEAGE, the other half. GC breaks the pointer; this keeps a real parent
    # and claims it says something it does not. A propagation record that may
    # assert any proposition it likes about a parent nobody re-reads is a
    # first-instance finding wearing a propagation label.
    ("GD", "keep the real parent but claim it states a proposition it does not",
     edit_json(M_SHEET, lambda d: d["governed_artefacts"][0].__setitem__(
         "proposition_markers", ["dynamic separation was the proven cause"])),
     "governed_artefact_parent_states_the_proposition"),

    ("GE", "spell the artefact as a q-card by giving it an anchor",
     edit_json(M_SHEET, lambda d: d["governed_artefacts"][0].__setitem__(
         "anchor", "q1")),
     "governed_artefact_is_not_a_card"),

    ("GF", "declare a correction that changed nothing",
     edit_json(M_SHEET, lambda d: d["governed_artefacts"][0].__setitem__(
         "post_edit_digest", d["governed_artefacts"][0]["pre_edit_digest"])),
     "governed_artefact_digests_differ"),

    ("GG", "pin the right bytes but declare the wrong text as the outcome",
     edit_json(M_SHEET, lambda d: d["governed_artefacts"][0].__setitem__(
         "expected_text_after", "<li>Casualties: none recorded</li>")),
     "artefact_carries_expected_proposition_text"),

    ("GH", "point the governed artefact at a file that does not exist",
     edit_json(M_SHEET, lambda d: d["governed_artefacts"][0].__setitem__(
         "path", "meoclass1/QB2_B_CheatSheet_NOPE.html")),
     "governed_artefact_path_exists"),

    # Re-aimed. This mutation first named `artefact_only_record_claims_no_primary`
    # and escaped to `artefact_paths_are_not_card_pages`, which showed the check
    # it named could not fail -- adding a card to make `primary` non-empty stops
    # the record being artefact-only, so the branch it lived in was never the
    # one reached. That check is gone; this now names the guard that really owns
    # the proposition. A page governed as BOTH an artefact and a q-card page is
    # pinned twice by two mechanisms with different rules, each right about half
    # of it, and a synthetic anchor on a page with no card block is exactly the
    # fake-anchor outcome the artefact form exists to avoid.
    ("GI", "claim the cheat sheet as a q-card page as well as an artefact",
     edit_json(M_SHEET, lambda d: d.__setitem__("cards", [{
         "correction_action_id": "FAKE-01", "file": "QB2_B_CheatSheet.html",
         "path": "meoclass1/QB2_B_CheatSheet.html", "anchor": "q1",
         "classification": "PRIMARY_CORRECTION",
         "pre_edit_digest": "a" * 64, "post_edit_digest": "b" * 64}])),
     "artefact_paths_are_not_card_pages"),
]


def main() -> int:
    content = run_suite("CORR-REL-BJ-* (Bulk Jupiter)", PROBE, MUTATIONS,
                        [QB8_A, QB5_A, QB10_B, SHEET, TRAPS, M_ATTR, M_FOUND])
    print()
    governance = run_suite(
        "CORR-REL-BJ-CHEATSHEET-20260909 (artefact governance)",
        PROBE_GOV, GOVERNANCE_MUTATIONS, [SHEET, M_SHEET])
    return content or governance


if __name__ == "__main__":
    raise SystemExit(main())
