#!/usr/bin/env python3
"""Content gate for CORR-T5-HYDRANT-20260906 -- SOLAS II-2/10.2.1.6.

THE PROPOSITION THIS GATE EXISTS TO KEEP ALIVE
----------------------------------------------
For CARGO ships, with the two required pumps delivering simultaneously, the
minimum pressure at the hydrants is 0.27 N/mm2 at 6,000 GT and upwards and
0.25 N/mm2 below 6,000 GT.

That is a TWO-LIMB rule, and the second limb is what a later well-meaning edit
drops first - it looks like a qualification and reads as noise. It is not: a
card carrying only 0.27 is not vague about small ships, it is WRONG about them.
Exactly the MSC.535(107) lifeboat-ventilation shape, where keeping only the
newbuilding limb inverted the rule for the whole in-service fleet. So every one
of the three sites is asserted to carry BOTH limbs, the threshold, and the
provision - element-scoped, so an adjacent bullet cannot supply the keyword.

WHY THE OLD FIGURES ARE CHECKED PER ELEMENT AND NOT PER CARD
------------------------------------------------------------
"4 to 6 Bar" and "4.0 bar" must be gone from the elements that TAUGHT them.
They are not banned from the cards: a version stamp legitimately records what
was removed, and known_traps entry 89 is the record of three Tranche 4A gates
going red on their own audit trail. Provenance sits outside the sweep.

WHY QB9_B IS CHECKED THOUGH THIS RECORD DOES NOT EDIT IT
--------------------------------------------------------
QB9_B#q5 is the corrected sibling that made the 4.0 bar site a CONTRADICTION
rather than merely an unsourced number - which is what promoted it out of a
1,034-hit census. If QB9_B ever stopped carrying the governing figures, the
justification recorded for editing QB2_H would have quietly evaporated. A gate
that asserts a correction's REASON, not only its result, is the one that
notices.
"""
from __future__ import annotations

import html as htmllib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_bytes import read_text                                  # noqa: E402
from validate_batch_h_series import card_digests, _balanced_end   # noqa: E402
from oral_supersession import resolve_authorised_card_state       # noqa: E402

CORRECTION_ID = "CORR-T5-HYDRANT-20260906"
MANIFEST = HERE / "correction_corr_t5_hydrant_20260906_manifest.json"
QB_ROOT = REPO / "meoclass1"
INDEX = REPO / "meoclass1/qb_content_index.json"
TRAPS = REPO / "meoclass1/known_traps.md"

PROVISION = "II-2/10.2.1.6"
THRESHOLD = "6,000 GT"

#: A limb is checked WITH ITS SCOPE, never as a bare figure. Two of the three
#: elements are headed "0.27 / 0.25 N/mm2:", so a check for the bare number is
#: satisfied by the HEADING even after the substantive limb has been deleted -
#: mutations D and E escaped their own checks on exactly that and were "caught"
#: only by the digest pin, which is the false green a content gate exists to
#: prevent. The figure without its tonnage scope is not the proposition.
UPPER = "0.27 N/mm² at 6,000 GT and upwards"
LOWER = "0.25 N/mm² below"

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-56s %s" % ("PASS" if ok else "FAIL", check, detail))


def flat(raw: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", raw)))


def card_block(text: str, anchor: str) -> str:
    i = text.find('<div class="q-card" id="%s"' % anchor)
    assert i >= 0, anchor
    return text[i:_balanced_end(text, i)]


def without_provenance(card: str) -> str:
    """The card with its version stamp and correction link removed.

    A version stamp DESCRIBES the defect it records. Three Tranche 4A gates
    went red on their own audit trail before this was made a rule
    (known_traps 89), so the negative checks below run on the teaching layers
    only.
    """
    card = re.sub(r'<span class="q-version">.*?</span>', " ", card, flags=re.S)
    card = re.sub(r'<span class="correction-link">.*?</span>', " ", card,
                  flags=re.S)
    return card


def owning_element(card: str, needle: str) -> str:
    """The <li>, <p> or <div> that actually carries `needle`.

    Element-scoped, not a character window: known_traps entry 89 records
    guards written as "needle within N chars of keyword" passing mutations
    because an adjacent bullet supplied the keyword.
    """
    i = card.find(needle)
    if i < 0:
        return ""
    best = ""
    for tag in ("li", "p", "div"):
        starts = [m.start() for m in re.finditer(r"<%s[ >]" % tag, card[:i])]
        if not starts:
            continue
        s = starts[-1]
        e = card.find("</%s>" % tag, i)
        if e < 0:
            continue
        block = card[s:e]
        if not best or len(block) < len(best):
            best = block
    return flat(best)


SITES = [
    ("N-3", "QB2_A.html", "q8", "0.27 / 0.25 N/mm", "4 to 6 Bar"),
    ("E-3", "QB2_B.html", "q18", "0.27 / 0.25 N/mm", None),
    ("E-2", "QB2_H.html", "q2", "SOLAS II-2/10.2.1.6", "4.0 bar"),
]


def main() -> int:
    man = json.loads(read_text(MANIFEST))
    report("manifest_is_this_correction",
           man.get("correction_id") == CORRECTION_ID, man.get("correction_id"))
    report("status_authorised", man.get("status") == "AUTHORISED",
           man.get("status"))

    for label, fname, anchor, marker, removed in SITES:
        card = card_block(read_text(QB_ROOT / fname), anchor)
        teaching = without_provenance(card)
        elem = owning_element(teaching, marker)

        report("%s_corrected_element_found" % label, bool(elem),
               "%s#%s, %d chars" % (fname, anchor, len(elem)))
        report("%s_element_cites_the_governing_provision" % label,
               PROVISION in elem, "SOLAS %s" % PROVISION)
        report("%s_element_carries_the_UPPER_limb" % label,
               UPPER in elem, "0.27 N/mm2 at 6,000 GT and upwards")
        report("%s_element_carries_the_LOWER_limb" % label,
               LOWER in elem,
               "0.25 N/mm2 below - the limb a later edit drops first, "
               "checked WITH its scope so the heading cannot satisfy it")
        report("%s_element_carries_the_GT_threshold" % label,
               THRESHOLD in elem, "6,000 GT")
        report("%s_element_scopes_the_figures_to_cargo_ships" % label,
               "cargo ship" in elem.lower(),
               "the passenger limbs are not silently implied")
        report("%s_element_states_the_two_pumps_condition" % label,
               "two required pumps" in elem or "two pumps" in elem,
               "the figure is meaningless without the pump condition")
        if removed:
            report("%s_false_figure_gone_from_the_teaching_layers" % label,
                   removed not in flat(teaching),
                   "'%s' no longer taught" % removed)

    # N-3 additionally has to say that a bigger number is not a SOLAS minimum,
    # because the number it replaced was defended as a monitor-throw figure.
    q8 = flat(without_provenance(card_block(read_text(QB_ROOT / "QB2_A.html"),
                                            "q8")))
    report("N3_says_a_monitor_throw_figure_is_not_a_SOLAS_minimum",
           "not a SOLAS minimum" in q8,
           "the card names the confusion that produced the defect")

    # E-3's card must say the single-limb form is WRONG, not merely incomplete.
    q18 = flat(without_provenance(card_block(read_text(QB_ROOT / "QB2_B.html"),
                                             "q18")))
    report("E3_says_the_single_limb_form_is_wrong_below_the_threshold",
           "wrong for a ship under 6,000 GT" in q18,
           "a two-limb rule stated with one limb is wrong, not vague")

    # ---- the REASON for E-2, not only its result ------------------------
    q5 = flat(card_block(read_text(QB_ROOT / "QB9_B.html"), "q5"))
    report("sibling_card_still_carries_the_governing_figures",
           UPPER in q5 and LOWER in q5 and THRESHOLD in q5,
           "QB9_B#q5 - the corrected card the 4.0 bar site contradicted")

    # ---- provenance is preserved, not swept -----------------------------
    report("version_stamps_may_still_quote_what_was_removed",
           True, "negative checks run on the teaching layers only, per "
                 "known_traps 89 - this is stated, not asserted")

    # ---- digests and corpus ---------------------------------------------
    inv = man["invariants"]
    bad = []
    for c in man["cards"]:
        d = card_digests(read_text(QB_ROOT / c["file"]))
        res = resolve_authorised_card_state(
            manifest=MANIFEST.name, action_id=c["correction_action_id"],
            file=c["file"], anchor=c["anchor"],
            pinned_post_digest=c["post_edit_digest"],
            live_digest=d.get(c["anchor"]))
        if not res.ok:
            bad.append("%s#%s:%s" % (c["file"], c["anchor"], res.status))
    report("every_pinned_state_is_live_or_a_proven_ancestor", not bad,
           "%d card(s), problems: %s" % (len(man["cards"]), bad or "none"))

    idx = json.loads(read_text(INDEX))
    report("canonical_questions_unchanged",
           idx["total_questions"] == inv["canonical_questions_after"],
           str(idx["total_questions"]))
    report("question_bearing_files_unchanged",
           idx["total_files"] == inv["question_bearing_files"],
           str(idx["total_files"]))

    # ---- governance ------------------------------------------------------
    report("declared_artefacts_exist",
           all((REPO / a["path"]).is_file() for a in man["artefacts"]),
           "%d artefact(s)" % len(man["artefacts"]))
    m = re.search(r"### 93\..*?(?=\n### |\Z)", read_text(TRAPS), re.S)
    body = m.group(0) if m else ""
    report("known_traps_entry_93_carries_the_lesson",
           bool(body) and all(x in body for x in
                              ("0.27", "0.25", "6,000 GT",
                               "Internal contradiction", "MSC.535(107)")),
           "entry 93")
    report("passenger_limbs_are_explicitly_out_of_scope",
           "passenger-ship limbs are deliberately NOT introduced"
           in man["authority"],
           "the record says what it chose not to add")
    report("unresolved_hose_test_contradiction_is_deferred_not_guessed",
           "deferred_to_k_items" in man["propagation"]
           and "QB2_B#q16" in man["propagation"]["deferred_to_k_items"],
           "the 1 bar / 2 bar hose-test conflict is raised, not resolved")

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    if FAILS:
        print("failed: " + ", ".join(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
