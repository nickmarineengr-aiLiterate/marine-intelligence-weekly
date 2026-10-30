#!/usr/bin/env python3
"""Content gate for CORR-LP617-QB9A-Q7-20261030 - follow-up A of trap 141.

The proposition is CORR-LP617-SEWAGE-SLUDGE-20261028's, carried to QB9_A Q7:
sewage sludge is NO LONGER on the 1996 Protocol's Annex 1 list (Resolution
LP.6(17), adopted 7 October 2022, in force 15 January 2023); no new dumping
permits; an existing permit runs to expiry, not later than 31 May 2027.

Shaped after validate_correction_lp617.py, whose extraction helpers it imports
rather than copies, so the two gates cannot drift into reading a card
differently:

  * PROPOSITION-SCOPED, never a banned string. The corrected card names sewage
    sludge to say it was removed, so every sentence naming it must carry the
    removal (SKILL.md 8.2a rule 2).
  * SITE-SCOPED on the limb that shipped the defect - the London Convention
    paragraph's reverse-list example - and on the reg-box row.
  * CLOSED-WORLD on the dates across the whole card.
  * Never a worldwide ban, read over the whole card; the FAL and OPRC limbs'
    three "global" phrases are set aside by exact match (GLOBAL_OK). Never
    extended to 1972 Convention Parties, read over the whole card.
  * NO SQ twin exists for QB9_A; the gate asserts that rather than assuming it.
  * OWNERSHIP: the record continues the T4a pin on q7 through `supersedes`;
    the gate checks the claim names that pin exactly. validate_corrections
    owns the digests themselves.
  * The corpus re-infection scan stays in validate_correction_lp617.py, whose
    KNOWN_OPEN still tolerates the rest of QB9_A: other cards are guarded only
    by their digest pins (independent review F4; a governed follow-up).
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio, read_text  # noqa: E402
import validate_correction_lp617 as LP  # noqa: E402

enable_utf8_stdio()

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-56s %s" % ("PASS" if ok else "FAIL", check, detail))


PAGE = QB / "QB9_A.html"
TWIN = REPO / "SQ" / "QB9_A.html"
CARD = "q7"
MANIFEST = HERE / "correction_corr_lp617_qb9a_q7_20261030_manifest.json"
CORR_ID = "CORR-LP617-QB9A-Q7-20261030"
GOV = HERE / "qb_content_index_governed.json"
IDX = QB / "qb_content_index.json"
TRAPS = QB / "known_traps.md"
REGISTRY = REPO / "docs" / "sources" / "MIW_SOURCE_REGISTRY.json"
CORR_DATE = "2026-10-30"
SHIPPED_WRONG = "such as dredged material, sewage sludge, or organic waste of natural origin"
#: The only "global" wording the card may carry: the FAL and OPRC limbs.
GLOBAL_OK = re.compile(r"global shipping efficiency|provides a global framework|"
                       r"National & Global Framework")
T4A = ("correction_corr_t4a_artefact_hygiene_20260906_manifest.json",
       "T4A-ARTEFACT-HYGIENE-20260906-13",
       "d4dfe75437dba664078a783779942415e8107c8f3a2987ddef8520fc62a4afdc")


def main() -> int:
    page = read_text(PAGE)
    card = LP.card_html(page, CARD)
    report("target_card_present", card is not None, "QB9_A#%s" % CARD)
    if card is None:
        return finish()
    report("no_sq_twin_exists", not TWIN.exists(),
           "a twin would need its own identity check")

    teach = LP.flatten(LP.strip_footers(card))
    n = len(LP.SLUDGE.findall(teach))
    report("non_vacuous_sludge", n >= 3, "%d mention(s)" % n)

    # 1. Sewage sludge is never taught as permitted, anywhere on the card.
    bad = LP.sludge_still_permitted(teach)
    report("no_sludge_taught_as_permitted", not bad, "found=%r" % (bad[:2] or None))
    report("shipped_wrong_phrase_absent", SHIPPED_WRONG not in teach)

    # 2. The limb that shipped the defect carries the correction itself.
    london = LP.section(teach, "3. London Convention and London Protocol", r"4\. OPRC")
    report("london_limb_present", len(london.split()) > 60, "%d words" % len(london.split()))
    example = LP.section(london, "explicitly permitted substances (", r"\)")
    report("reverse_list_example_excludes_sludge",
           bool(example) and not LP.SLUDGE.search(example), "example=%r" % example[:90])
    report("reverse_list_states_removal",
           re.search(r"Sewage sludge is no longer on that list", london) is not None
           and "LP.6(17)" in london and "7 October 2022" in london
           and LP.EIF_OK.search(london) is not None,
           "LP.6(17), adoption 7 October 2022 and 15 January 2023 required")
    report("no_new_permits_and_cutoff",
           re.search(r"No new permits may be issued", london) is not None
           and re.search(r"expiry date, but not later than 31 May 2027", london) is not None)

    reg = LP.section(teach, "Regulatory References", r"CE Oral Tip")
    report("reg_box_has_lp617_row",
           re.search(r"Resolution LP\.6\(17\) Adopted 7 Oct 2022, in force 15 Jan 2023", reg)
           is not None and LP.CUTOFF_OK.search(reg) is not None)

    # 3. Closed-world dates over the whole card.
    eif_bad = [m.group(1) for m in LP.CLAIM_DATE.finditer(teach)
               if not LP.EIF_OK.fullmatch(re.sub(r"\s+", " ", m.group(1)))]
    eif_bad += [m.group(1) for m in LP.CLAIM_DATE_REV.finditer(teach)
                if not LP.EIF_OK.fullmatch(re.sub(r"\s+", " ", m.group(1)))
                and not LP.ADOPTED_BEFORE.search(teach[max(0, m.start() - 20):m.start()])]
    report("every_entry_into_force_is_15_jan_2023", not eif_bad,
           "other=%r" % (eif_bad[:2] or None))
    cut_bad = [m.group(0) for s in LP.sentences(teach) if LP.PERMIT.search(s)
               for m in LP.ANY_DATE.finditer(s)
               if not LP.CUTOFF_OK.fullmatch(m.group(0))
               and (LP.ENDING.search(s) or not LP.EVENT_BEFORE.search(s[:m.start()]))]
    report("every_permit_cutoff_is_31_may_2027", not cut_bad,
           "other=%r" % (cut_bad[:2] or None))

    # 4. Never widened into a worldwide ban, over the whole card: a ban sentence
    # in the CE Oral Tip escaped the London-limb-only first version (independent
    # review F1, 30 Oct 2026). The card's FAL and OPRC limbs legitimately say
    # "global"; exactly those three phrases are set aside, nothing wider.
    wide = [m.group(0) for m in LP.WORLDWIDE.finditer(GLOBAL_OK.sub(" ", teach))]
    report("not_taught_as_worldwide_ban", not wide, "found=%r" % (wide[:1] or None))
    widened = [s.strip()[:90] for s in LP.sentences(teach) if LP.SCOPE_1972.search(s)
               and not re.search(r"\bnot\b|\bonly\b", s)]
    report("scope_not_extended_to_1972_parties", not widened,
           "found=%r" % (widened[:1] or None))

    # 5. The stamp records the correction (read on its own).
    f = LP.footer(card)
    report("stamp_records_correction",
           "Q7 · v1.2" in f and "corrected 30 Oct 2026" in f and "LP.6(17)" in f,
           "%r" % f[:80])

    # 6. Changelog: governed note states the correction; derived index agrees.
    gov = json.loads(read_text(GOV))
    notes = [e for e in gov.get("recently_updated", []) if e.get("date") == CORR_DATE
             and "QB9_A" in e.get("note", "") and "LP.6(17)" in e.get("note", "")]
    note = notes[0]["note"] if notes else ""
    report("governed_note_present", len(notes) == 1, "%d note(s)" % len(notes))
    report("governed_note_states_removal",
           re.search(r"sewage sludge", note, re.I) is not None
           and re.search(r"removed|no longer|deleted", note) is not None
           and "15 January 2023" in note and "31 May 2027" in note
           and notes[0].get("files") == ["QB9_A.html"] if notes else False)
    idx = json.loads(read_text(IDX))
    report("generated_index_matches_governed_changelog",
           [e.get("note") for e in gov.get("recently_updated", [])]
           == [e.get("note") for e in idx.get("recently_updated", [])])

    # 7. Trap 141: follow-up A still logged as it was, and its closure recorded.
    traps = read_text(TRAPS)
    at = traps.find("### 141. Sewage sludge")
    entry = traps[at:] if at >= 0 else ""
    nxt = re.search(r"\n### \d+\.", entry[5:])
    entry = entry[:nxt.start() + 5] if nxt else entry
    report("trap_141_still_logs_followup_a",
           "- **A.** `QB9_A` Q7" in entry, "the open-item record is not rewritten")
    report("trap_141_closes_followup_a",
           re.search(r"\*\*Closure of follow-up A[^*]*\*\*[^\n]*\n?[^\n]*" + re.escape(CORR_ID),
                     entry) is not None)

    # 8. The record: identity, proposition, trap link, ownership chain.
    if not MANIFEST.is_file():
        report("record_present", False, "correction record absent")
        return finish()
    rec = json.loads(read_text(MANIFEST))
    report("record_identity", rec.get("correction_id") == CORR_ID
           and rec.get("kind") == "POST_RELEASE_CORRECTION")
    text = rec.get("authority", "") + " " + rec.get("rationale", "")
    report("record_states_the_proposition",
           all(x in text for x in ("7 October 2022", "15 January 2023", "31 May 2027"))
           and re.search(r"Delete sub-paragraph 1\.2", text) is not None)
    report("record_cites_trap_141", 141 in (rec.get("known_traps_entries") or []),
           "known_traps_entries=%s" % rec.get("known_traps_entries"))
    cards = [c for c in rec.get("cards", []) if c.get("anchor") == CARD
             and c.get("path") == "meoclass1/QB9_A.html"]
    sup = cards[0].get("supersedes", {}) if len(cards) == 1 else {}
    report("record_continues_the_t4a_pin",
           len(cards) == 1 and cards[0].get("digest_pinned_by_earlier_manifest") is True
           and (sup.get("manifest"), sup.get("action_id"), sup.get("post_edit_digest")) == T4A
           and cards[0].get("pre_edit_digest") == T4A[2],
           "supersedes %s/%s" % (sup.get("manifest", "-")[:30], sup.get("action_id", "-")))
    report("record_declares_only_q7", len(rec.get("cards", [])) == 1)

    # 9. Both sources the proposition rests on name this card.
    rows = {s.get("source_id"): s for s in json.loads(read_text(REGISTRY)).get("sources", [])}
    want = ("SRC-IMO-LP6-17", "SRC-IMO-STATUS-TREATIES-VOL2-2026-09-30")
    report("sources_registered_for_the_card",
           all(w in rows and "meoclass1/QB9_A.html#q7" in rows[w].get("used_by", [])
               for w in want),
           "missing=%r" % ([w for w in want if w not in rows] or None))

    return finish()


def finish() -> int:
    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    for f in FAILS:
        print("  FAIL " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
