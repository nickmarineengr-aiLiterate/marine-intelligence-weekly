#!/usr/bin/env python3
"""Content gate for CORR-REL-BJ-ATTRIBUTION-20260908 and
CORR-REL-BJ-FOUNDERING-20260908 -- the two Bulk Jupiter cards.

WHAT THIS GATE HAS TO DO THAT NO PIN CAN
----------------------------------------
Both records are single-card corrections whose post states ARE pinned, so a
digest pin already proves the bytes have not moved. What it cannot see is
whether the bytes say the right thing, and this defect class is entirely about
what the sentence asserts:

  * WHO investigated. "The IMO" and "the Bahamas Maritime Authority as flag
    State" are the same length, the same shape and equally plausible to a reader
    who does not know that investigation is a flag-State duty.
  * HOW STRONGLY the report found it. "concluded" and "most probable" differ by
    one word and by the whole difference between a finding and a hypothesis.
  * A NUMBER. "5 minutes" and "20 minutes" are one character apart.

None of those is visible to sha256, and none is a spelling. So every check below
asserts the PROPOSITION -- the claim the candidate would carry into an oral --
rather than banning a string.

WHY EVERY NEGATIVE CHECK STRIPS THE VERSION FOOTER FIRST
--------------------------------------------------------
Both corrected footers QUOTE the wording they removed: QB5_A#q11's stamp says
the card used to read "sank within 5 minutes", and QB8_A#q4's names the IMO in
order to deny it. A card-wide "the rejected wording must be absent" check
therefore reports the changelog as the defect -- known_traps entry 89, which
this gate reproduced the first time it was run. Negative checks run on the
teaching layers only; the footer gets its own POSITIVE checks instead, because a
stamp that loses its own provenance is a separate failure.

WHY THE CORPUS-AGREEMENT CHECKS ARE HERE AND NOT IN A SWEEP
-----------------------------------------------------------
Five pages teach this casualty. A correction that fixes one of them and leaves
the corpus disagreeing with itself is the failure shape this repository has hit
repeatedly, and a digest pin on the corrected card is structurally blind to it.
So the four UNTOUCHED sites are asserted positively: they must still teach the
loss correctly, which also catches a future over-eager sweep deleting them.
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

QB_ROOT = REPO / "meoclass1"
TRAPS = REPO / "meoclass1/known_traps.md"
MANIFESTS = {
    "CORR-REL-BJ-ATTRIBUTION-20260908":
        HERE / "correction_corr_rel_bj_attribution_20260908_manifest.json",
    "CORR-REL-BJ-FOUNDERING-20260908":
        HERE / "correction_corr_rel_bj_foundering_20260908_manifest.json",
}

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-58s %s" % ("PASS" if ok else "FAIL", check, detail))


def flat(raw: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", raw)))


def card_block(text: str, anchor: str) -> str:
    i = text.find('<div class="q-card" id="%s"' % anchor)
    assert i >= 0, anchor
    return text[i:_balanced_end(text, i)]


def without_provenance(card: str) -> str:
    """The card with its version stamp and correction link removed."""
    card = re.sub(r'<span class="q-version">.*?</span>', " ", card, flags=re.S)
    card = re.sub(r'<span class="correction-link">.*?</span>', " ", card,
                  flags=re.S)
    return card


def stamp(card: str) -> str:
    m = re.search(r'<span class="q-version">(.*?)</span>', card, re.S)
    return flat(m.group(1)) if m else ""


def casualty_link(card: str) -> str:
    """The Casualty Link block only.

    Block-scoped on purpose. Both cards name Bulk Jupiter in more than one
    layer once the version stamps are counted, and a card-wide check would be
    satisfied by the footer -- which is to say it would not be reading the
    teaching at all.

    Anchored on the HEADING MARKUP, not on the words. QB5_A#q11 opens its deep
    dive with a button reading "Trap Qs / Examiner Chain / CE Failures /
    Casualty Link", so a text search finds the label 5,491 bytes before the
    section. The first version of this gate did exactly that, extracted the CE
    Relevance prose instead, and reported six false FAILs -- and, worse, one
    false PASS: the "five minutes is gone" negative check went green because
    the text it searched was the wrong block. A negative check over an empty or
    wrong region is not a check, which is why `main` asserts non-vacuity below
    before trusting any of these.
    """
    body = without_provenance(card)
    m = re.search(r"<h5>\s*Casualty Link\s*</h5>", body)
    if m is None:
        return ""
    i = m.end()
    nxt = [j for j in (body.find("<h5>", i), body.find("</details>", i)) if j > 0]
    return flat(body[i:min(nxt)] if nxt else body[i:])


def main() -> int:
    # ---------- 0. the records themselves --------------------------------
    for cid, path in MANIFESTS.items():
        man = json.loads(read_text(path))
        report("manifest_%s_present" % cid.split("-")[3].lower(),
               man.get("correction_id") == cid, man.get("correction_id"))
        report("status_authorised_%s" % cid.split("-")[3].lower(),
               man.get("status") == "AUTHORISED", man.get("status"))
        report("trap_131_declared_%s" % cid.split("-")[3].lower(),
               131 in (man.get("known_traps_entries") or []),
               str(man.get("known_traps_entries")))

    traps = read_text(TRAPS)
    report("trap_131_exists", bool(re.search(r"^### 131\.", traps, re.M)),
           "known_traps.md")
    report("trap_131_names_the_flag_state_duty",
           bool(re.search(r"### 131\..{0,4000}?SOLAS XI-1/6", traps, re.S)),
           "the duty, not just the casualty")

    qb8a = read_text(QB_ROOT / "QB8_A.html")
    qb5a = read_text(QB_ROOT / "QB5_A.html")
    q4 = card_block(qb8a, "q4")
    q11 = card_block(qb5a, "q11")
    cl4, cl11 = casualty_link(q4), casualty_link(q11)

    # ---------- 0b. NON-VACUITY ------------------------------------------
    # Every negative check below runs over cl4/cl11. If either extraction is
    # empty or has landed on the wrong block, those checks go green while
    # reading nothing -- which is how the first run of this gate reported the
    # rejected wording as absent from a region that never contained it. The
    # extraction is therefore asserted before it is trusted.
    report("casualty_link_q4_extracted", len(cl4) > 400 and "Bulk Jupiter" in cl4,
           "%d chars" % len(cl4))
    report("casualty_link_q11_extracted",
           len(cl11) > 400 and "Bulk Jupiter" in cl11, "%d chars" % len(cl11))
    report("casualty_link_is_not_the_ce_relevance_block",
           "CE Relevance" not in cl4 and "CE Relevance" not in cl11,
           "the block a text-anchored extractor lands on instead")

    # ---------- 1. QB8_A#q4 : WHO investigated ---------------------------
    report("q4_names_the_bahamas_maritime_authority",
           "Bahamas Maritime Authority" in cl4,
           "the flag State that actually investigated")
    report("q4_names_it_AS_flag_state",
           bool(re.search(r"Bahamas Maritime Authority.{0,40}flag State", cl4)),
           "naming the body without the role teaches a name, not a rule")
    report("q4_denies_the_imo_investigated",
           bool(re.search(r"IMO does not investigate", cl4)),
           "stated positively so a reader cannot infer the opposite")
    report("q4_does_not_attribute_the_investigation_to_the_imo",
           not re.search(r"investigation by the IMO|IMO (investigated|concluded)",
                         cl4),
           "the defect itself, checked on the teaching layer only")

    # ---------- 2. QB8_A#q4 : HOW STRONGLY -------------------------------
    report("q4_records_no_physical_evidence_of_cause",
           "no physical evidence" in cl4, "the report's own section 5.1")
    report("q4_states_the_finding_as_most_probable",
           "most probable" in cl4, "not 'concluded'")
    report("q4_carries_BOTH_candidate_mechanisms",
           bool(re.search(r"liquefaction or a free-surface effect", cl4)),
           "the report offers two; a card offering one has hardened it")

    # ---------- 3. QB8_A#q4 : the particulars ----------------------------
    report("q4_date_is_2_january_2015", "2 January 2015" in cl4, "")
    report("q4_tonnage_is_46400", "46,400 tonnes" in cl4, "was 46,000")
    report("q4_crew_toll_carries_its_denominator",
           "18 of her 19 crew" in cl4, "'18 lost' alone is not the fact")
    report("q4_foundering_time_present",
           "approximately 20 minutes" in cl4, "")
    report("q4_moisture_pair_is_a_PAIR",
           bool(re.search(r"21\.3%.{0,60}10%", cl4)),
           "21.3% alone teaches nothing -- it is the gap against the declared 10%")

    # ---------- 4. QB8_A#q4 : what the correction must NOT have lost -----
    report("q4_group_c_framing_preserved",
           "Group C" in cl4, "why the schedule was the defect")
    report("q4_imsbc_schedule_revision_preserved",
           "IMSBC Code individual schedules" in cl4, "")
    report("q4_names_the_group_a_bauxite_fines_schedule",
           "BAUXITE FINES" in cl4, "the schedule the revision actually produced")

    # ---------- 5. QB5_A#q11 : the number and the mechanism --------------
    report("q11_foundering_time_is_20_minutes",
           "approximately 20 minutes" in cl11, "the BMA report's figure")
    report("q11_five_minute_claim_gone_from_teaching",
           "sank within 5 minutes" not in cl11,
           "checked on the teaching layer; the stamp quotes it on purpose")
    report("q11_mechanism_is_not_asserted",
           bool(re.search(r"most probably liquefied or developed a free surface",
                          cl11)),
           "the report concludes only that it is most probable, and either of two")

    # ---------- 6. QB5_A#q11 : what was tested and KEPT ------------------
    # The heavy-weather limb was checked against the report's own heavy-weather
    # section and is correct. It is asserted POSITIVELY because the real risk to
    # it is a later sweep deleting a true statement that sat beside a false one.
    report("q11_heavy_weather_preserved", "heavy weather" in cl11,
           "true, tested, and kept -- not removed on suspicion")
    report("q11_heavy_weather_conditions_named",
           "Beaufort 6" in cl11, "NE monsoon, Beaufort 6-7")
    report("q11_tml_teaching_preserved",
           "Transportable Moisture Limit" in cl11, "")
    report("q11_risk_assessment_teaching_preserved",
           "Likelihood" in cl11 and "Consequence" in cl11,
           "the card's actual subject")
    report("q11_crew_toll_preserved", "18 of 19 crew lost" in cl11, "")

    # ---------- 7. the version stamps ------------------------------------
    s4, s11 = stamp(q4), stamp(q11)
    report("q4_stamp_bumped_to_v1_1", "v1.1" in s4, s4[:40])
    report("q4_stamp_names_its_correction",
           "CORR-REL-BJ" in s4 or "CORR-REL-BULKJUPITER" in s4, "")
    report("q4_stamp_quotes_what_it_rejected",
           "IMO" in s4, "a stamp that hides the old claim is not provenance")
    report("q11_stamp_bumped_to_v1_1", "v1.1" in s11, s11[:40])
    report("q11_stamp_names_its_correction",
           "CORR-REL-BJ" in s11 or "CORR-REL-BULKJUPITER" in s11, "")
    report("q11_stamp_quotes_what_it_rejected",
           "5 minutes" in s11, "")

    # ---------- 8. the corpus must not disagree with itself --------------
    # Four further pages teach this casualty and none was edited. They are
    # asserted positively, because "the corrected card is right" and "the corpus
    # agrees" are different claims and only the first has a pin.
    qb10b = read_text(QB_ROOT / "QB10_B.html")
    qb8h = read_text(QB_ROOT / "QB8_H.html")
    sheet = read_text(QB_ROOT / "QB2_B_CheatSheet.html")
    report("qb10b_still_teaches_18_of_19",
           "18 of 19 crew lost" in qb10b, "untouched sibling")
    report("qb10b_moisture_agrees_with_q4",
           "21.3%" in qb10b, "the figure QB8_A now carries came from here")
    report("qb10b_still_denies_the_cargo_shift_reading",
           "not a cargo shift" in flat(qb10b), "")
    report("qb8h_still_names_the_casualty", "Bulk Jupiter 2015" in qb8h, "")
    report("cheatsheet_still_names_the_casualty",
           "Bulk Jupiter" in sheet, "")
    report("no_other_page_attributes_the_investigation_to_the_imo",
           not any(re.search(r"investigation by the IMO",
                             read_text(p))
                   for p in sorted(QB_ROOT.rglob("*.html"))),
           "closed-world: the class, not the one page it was found on")

    # ---------- 9. the pins still resolve --------------------------------
    for cid, path in MANIFESTS.items():
        man = json.loads(read_text(path))
        for card in man["cards"]:
            live = card_digests(read_text(REPO / card["path"])).get(card["anchor"])
            res = resolve_authorised_card_state(
                manifest=path.name, action_id=card["correction_action_id"],
                file=card["file"], anchor=card["anchor"],
                pinned_post_digest=card["post_edit_digest"],
                live_digest=live, directory=HERE)
            report("pin_resolves_%s_%s" % (card["file"].split(".")[0].lower(),
                                           card["anchor"]),
                   res.ok, res.describe())

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    for f in FAILS:
        print("  FAIL %s" % f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
