#!/usr/bin/env python3
"""
Content validator for CORR-G1-010-RORO-ATTRIBUTION-20260825.

WHY THE DIGEST PIN IS NOT ENOUGH
--------------------------------
`validate_corrections.py` answers "is this card still exactly the bytes that
were authorised?".  It pins whatever it is given, and it would have been
perfectly content with the wrong text: QB2_F#q3 shipped for weeks crediting the
ro-ro, vehicle and special-category-space fire-safety requirements to
resolution MSC.532(107), and every digest gate in the repository was green the
whole time.

The defect was not a typo.  MSC.532(107) and MSC.550(108) share an
entry-into-force date of 1 January 2026 and both amend SOLAS chapter II-2, so a
tranche list puts them side by side -- but MSC.532(107)'s annex touches
II-1/2, II-1/3-13, II-2/1, II-2/10, V/2, V/19, XIV/2 and XIV/3, and reaches
neither II-2/20 nor II-2/7.  QB10_B#q1 already carried the package correctly, so
two paid cards in the bank disagreed with each other about which instrument
carries the requirement.

So the substance is asserted here, one named check per proposition a future
edit could quietly lose, and `mutate_correction_g1_010.py` requires each of its
mutations to trip THAT check rather than the digest pin that fires on any edit
at all.

    the ro-ro package is credited to MSC.550(108), never to MSC.532(107)
    the FSS Code companion MSC.555(108) is named
    both resolutions' entry into force is stated as 1 January 2026
    the existing-passenger-ship date is the first survey on or after 2028
    the PFOS threshold is attributed to MSC.1/Circ.1694, not to SOLAS
    application populations are stated, not flattened into "new ships"
    the two cards that carry this package agree with each other
    no correction or production vocabulary reached the candidate surface

THE SECOND-PASS CHECK
---------------------
`no_wrong_attribution_on_any_surface` is the one that matters most.  This repo
has repaired prose and left the summary bullet, the Numbers block, the reg-box,
an SVG label or the page meta stating the corrected-away claim.  So the negative
search runs over the WHOLE card, every block, not over the paragraph that was
edited -- and it runs on `html.unescape()` output, because a guard spelled
`h&m` is blind to `h&amp;m`.

  PYTHONIOENCODING=utf-8 python tools/oral/validate_correction_g1_010.py

Exit 0 when every check passes, 1 otherwise.
"""

from __future__ import annotations

import html as htmllib
import io
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio          # noqa: E402
from validate_batch_b import card_digests         # noqa: E402

enable_utf8_stdio()

MANIFEST = HERE / "correction_corr_g1_010_roro_attribution_20260825_manifest.json"
QB_DIR = REPO / "meoclass1"

PRIMARY = ("meoclass1/QB2_F.html", "q3")
SIBLING = ("meoclass1/QB10_B.html", "q1")

PRIMARY_Q_TEXT = "What are the latest SOLAS Chapter II amendments and their key changes?"
SIBLING_Q_TEXT = ("Give a consolidated overview of SOLAS and MARPOL amendments "
                  "entering into force from 2024 through 2028.")

_checks = 0
_failed: list[str] = []


def report(check: str, ok: bool, detail: str = "") -> None:
    global _checks
    _checks += 1
    if not ok:
        _failed.append(check)
    print("%-5s %-52s %s" % ("PASS" if ok else "FAIL", check, detail))


def page(rel: str) -> str:
    return io.open(REPO / rel, encoding="utf-8", newline="").read()


def card_html(text: str, anchor: str) -> str:
    """The balanced <div class="q-card"> block for one anchor."""
    i = text.find('id="%s"' % anchor)
    if i < 0:
        return ""
    start = text.rfind('<div class="q-card', 0, i)
    depth, j = 0, start
    for m in re.finditer(r'<div\b|</div>', text[start:]):
        depth += 1 if m.group(0) != "</div>" else -1
        if depth == 0:
            j = start + m.end()
            break
    return text[start:j]


def plain(card: str) -> str:
    """Candidate-visible text, unescaped, tags stripped, whitespace collapsed."""
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", card)))


# Sentences that credit the ro-ro / vehicle-space package to MSC.532(107).
# Every one of these is a real way the defect could come back, and each is
# checked against text where MSC.532(107) is NOT being explicitly negated.
RORO_TERMS = ("ro-ro", "vehicle space", "special category", "video monitoring",
              "weather deck", "cargo control room")


# Block boundaries.  NOT sentence boundaries: a heading carries no terminal
# punctuation, and a reg-box row is two spans, so a sentence splitter merges
# both into whatever follows -- and if what follows is one of the card's
# legitimate "it is NOT MSC.532(107)" lines, the negation exemption swallows
# the defect.  The mutation suite proved exactly that: mutations B and D
# escaped a sentence-scoped guard.
_BLOCK_END = re.compile(r"</(?:li|p|h4|h5|div|span|em|strong)>")


def blocks(card: str) -> list[str]:
    """The card's leaf content units, as candidate-visible text."""
    return [plain(frag) for frag in _BLOCK_END.split(card) if frag.strip()]


def wrong_attribution_windows(card: str) -> list[str]:
    """Blocks that credit MSC.532(107) with a reg. 20 / reg. 7 requirement.

    SCOPED TO A CONTENT BLOCK.  Two earlier scopings were wrong and the
    mutation suite found both:

      * +/- 260 characters reported nine findings on a CORRECT card, because a
        card whose whole purpose is to CONTRAST the two packages necessarily
        puts them near each other.  A guard a correct card cannot satisfy is
        noise, and noise gets deleted along with the real check.
      * A sentence let mutations B (an <h4> heading) and D (a reg-box row)
        escape, because neither ends in terminal punctuation, so both merged
        into a following block carrying a negation marker.

    A block is the right unit because a block is one claim.  The property is:
    no single claim may attribute a ro-ro, vehicle-space, special category,
    video monitoring, weather-deck or cargo-control-room requirement to
    MSC.532(107).

    A correction that TEACHES the trap must still be able to name the wrong
    resolution, so a block carrying a negation marker is not a finding.
    Without that exemption the card could never say "it is not MSC.532(107)",
    which is the single most useful line on it.
    """
    negations = ("not msc.532", "wrongly", "rather than msc.532",
                 "instead of msc.532", "two ways to lose", "attributing",
                 "quoting msc.532", "never msc.532", "a different package")
    out = []
    for block in blocks(card):
        low = block.lower()
        if "msc.532(107)" not in low:
            continue
        if not any(t in low for t in RORO_TERMS):
            continue
        if any(n in low for n in negations):
            continue
        # A block that names MSC.550(108) alongside is enumerating the 2026
        # TRANCHE, not attributing a requirement -- QB10_B#q1's 60-Second block
        # lists all six resolutions of that tranche in one breath and is
        # correct.  The defect this guard exists for always looks the other
        # way round: MSC.532(107) offered as the ro-ro instrument with the real
        # one absent, which is exactly what the wrong reg-box row and the wrong
        # heading in the mutation suite do.
        if "msc.550(108)" in low:
            continue
        out.append(" ".join(block.split())[:200])
    return out


# Every dated in-force claim the card makes.  Asserting that "1 January 2026"
# appears SOMEWHERE is unfalsifiable on a card that says it eight times: the
# mutation that moved entry into force to 2027 escaped, because one surviving
# "1 Jan 2026" kept the check green.  What is actually assertable is that every
# in-force date on the card is one of the two real ones.
_IN_FORCE = re.compile(
    r"(?:in force|eff\.|effective)[^.]{0,40}?(\d{1,2}\s+(?:Jan|January)\s+(\d{4}))",
    re.I)


def in_force_years(text: str) -> set:
    return {m.group(2) for m in _IN_FORCE.finditer(text)}


def main() -> int:
    if not MANIFEST.is_file():
        report("correction_record_present", False, "missing %s" % MANIFEST.name)
        print("\n%d checks, %d FAIL" % (_checks, len(_failed)))
        return 1
    rec = json.loads(MANIFEST.read_text(encoding="utf-8"))
    report("correction_record_present", True, MANIFEST.name)
    report("correction_record_authorised", rec.get("status") == "AUTHORISED",
           "status=%s" % rec.get("status"))

    declared = {(c["path"], c["anchor"]): c for c in rec.get("cards", [])}
    report("both_cards_declared_in_record",
           PRIMARY in declared and SIBLING in declared,
           "declared=%s" % sorted("%s#%s" % k for k in declared))

    primary = card_html(page(PRIMARY[0]), PRIMARY[1])
    sibling = card_html(page(SIBLING[0]), SIBLING[1])
    report("both_cards_live", bool(primary) and bool(sibling),
           "primary=%d bytes, sibling=%d bytes" % (len(primary), len(sibling)))

    ptxt, stxt = plain(primary), plain(sibling)
    both = ptxt + " ‖ " + stxt

    # ---- identity is untouched: a correction rewrites an answer, not a question
    report("primary_question_text_unchanged", PRIMARY_Q_TEXT in ptxt, PRIMARY_Q_TEXT[:60])
    report("sibling_question_text_unchanged", SIBLING_Q_TEXT in stxt, SIBLING_Q_TEXT[:60])

    ids = list(card_digests(page(PRIMARY[0])))
    report("primary_card_order_unchanged", ids == ["q1", "q2", "q3", "q4", "q5", "q6"],
           str(ids))

    # ---- digests match what the record authorised -------------------------
    drift = []
    for rel, anchor in (PRIMARY, SIBLING):
        live = card_digests(page(rel)).get(anchor)
        want = declared.get((rel, anchor), {}).get("post_edit_digest")
        if live != want:
            drift.append("%s#%s live=%s pinned=%s" % (rel, anchor, live, want))
    report("live_state_matches_the_record", not drift, "drift=%s" % (drift or "none"))

    # ---- THE CORRECTION ITSELF --------------------------------------------
    report("roro_package_credited_to_msc550", "MSC.550(108)" in ptxt,
           "MSC.550(108) named on the primary card")
    report("fss_companion_named", "MSC.555(108)" in ptxt,
           "MSC.555(108) named on the primary card")
    report("reg_20_named", "II-2/20" in ptxt, "SOLAS II-2/20 cited")

    bad = wrong_attribution_windows(primary) + wrong_attribution_windows(sibling)
    report("no_wrong_attribution_on_any_surface", not bad,
           "windows=%d%s" % (len(bad), (": " + bad[0]) if bad else ""))

    # MSC.532(107) must still be present and correctly scoped: deleting it
    # would trade one wrong card for another, because the PFOS limb IS its work.
    report("msc532_retained_for_its_own_package",
           "MSC.532(107)" in ptxt and "II-2/10.11" in ptxt,
           "PFOS limb still credited to MSC.532(107)")
    report("msc532_lifting_appliance_limb_present", "II-1/3-13" in ptxt,
           "II-1/3-13 cited")

    # ---- dates: in force, and the separate future application date --------
    years = in_force_years(ptxt)
    report("entry_into_force_stated",
           ("1 January 2026" in ptxt or "1 Jan 2026" in ptxt)
           and years and years <= {"2026", "2028"},
           "in-force years on the card: %s (2026 for the tranche, 2028 for the "
           "adopted MSC.549(108) limb)" % (sorted(years) or "none"))
    report("existing_ship_application_date_stated",
           "first survey on or after 1 January 2028" in ptxt,
           "existing passenger ships, first survey on or after 1 January 2028")
    report("force_and_application_not_conflated",
           ("1 Jan 2026" in ptxt or "1 January 2026" in ptxt)
           and "2028" in ptxt,
           "both dates present and distinct")
    report("adoption_dates_distinguish_the_packages",
           "8 Jun 2023" in ptxt and "23 May 2024" in ptxt,
           "MSC.532(107) 8 Jun 2023 / MSC.550(108) 23 May 2024")

    # ---- the PFOS threshold is a unified interpretation, not treaty text ---
    # CO-LOCATION, not mere presence.  The mutation that deleted the sentence
    # sourcing the threshold escaped a presence check, because MSC.1/Circ.1694
    # still appeared in the reg-box and the trap block.  Every block that
    # STATES the threshold must also name where it comes from.
    # Proximity, not block: `<strong>10 mg/kg</strong>` is its own leaf, so a
    # block test separates the figure from the source in text that is correct.
    # Attribution is the opposite case to the guard above -- there, nearness
    # was meaningless because the card deliberately contrasts two resolutions;
    # here, nearness IS the property, because a threshold and its source have
    # to be readable together or the candidate quotes the number bare.
    orphaned = []
    for m in re.finditer(r"10 mg/kg", ptxt):
        lo, hi = max(0, m.start() - 500), min(len(ptxt), m.end() + 500)
        if "MSC.1/Circ.1694" not in ptxt[lo:hi]:
            orphaned.append(" ".join(ptxt[lo:hi].split())[:160])
    report("pfos_threshold_attributed_to_the_circular",
           "MSC.1/Circ.1694" in ptxt and "10 mg/kg" in ptxt and not orphaned,
           "blocks stating 10 mg/kg without its source: %d%s"
           % (len(orphaned), (": " + orphaned[0][:110]) if orphaned else ""))
    report("pfos_threshold_not_claimed_as_solas",
           not re.search(r"MSC\.532\(107\)[^.]{0,120}(above|exceeding)\s+10\s*mg/kg",
                         ptxt),
           "no 'MSC.532(107) prohibits above 10 mg/kg' construction")

    # ---- application populations are stated, not flattened ----------------
    for term, label in (("passenger ship", "population_passenger_ships_named"),
                        ("cargo ship", "population_cargo_ships_named")):
        report(label, term in ptxt.lower(), term)
    report("cargo_ship_limb_distinguished", "20.4.1.5" in ptxt,
           "the cargo-ship detection limb is cited separately")
    report("video_replay_both_periods_stated",
           "seven days" in ptxt and "24 hours" in ptxt,
           "7 days new / 24 hours existing")

    # ---- the two cards must agree ----------------------------------------
    disagree = []
    for anchor_text, name in ((ptxt, "QB2_F#q3"), (stxt, "QB10_B#q1")):
        if "MSC.550(108)" not in anchor_text:
            disagree.append(name)
    report("both_cards_credit_the_same_resolution", not disagree,
           "silent=%s" % (disagree or "none"))
    report("sibling_video_replay_is_not_understated",
           "seven days" in stxt or "7 days" in stxt,
           "the sibling states the new-ship replay period too")

    # ---- the review block is asserted, not decoration ---------------------
    rev = rec.get("review") or {}
    report("review_states_its_independence",
           rev.get("independence") == "INDEPENDENT_CLEAN_CONTEXT",
           "independence=%s" % rev.get("independence"))
    report("review_ran_a_second_pass", (rev.get("passes") or 0) >= 2,
           "passes=%s" % rev.get("passes"))
    report("review_records_every_pass_verdict",
           bool(rev.get("pass_1_verdict")) and bool(rev.get("pass_2_verdict")),
           "pass_1=%s pass_2=%s"
           % (rev.get("pass_1_verdict"), rev.get("pass_2_verdict")))
    report("review_final_pass_is_publishable",
           rev.get("pass_2_verdict") in ("PASS", "PASS_WITH_FIX"),
           "final=%s" % rev.get("pass_2_verdict"))

    # ---- nothing internal leaked ------------------------------------------
    leaked = [w for w in ("CORR-G1-010", "OPEN-G1-", "AUG-0015", "pre_edit_digest",
                          "post_edit_digest", "manifest", "validator",
                          "PRIMARY_CORRECTION", "ENRICH_EXISTING")
              if w.lower() in both.lower()]
    report("no_internal_vocabulary_on_the_candidate_surface", not leaked,
           "leaked=%s" % (leaked or "none"))

    print("\n%d checks, %d FAIL" % (_checks, len(_failed)))
    if _failed:
        print("failed: " + ", ".join(_failed))
    return 1 if _failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
