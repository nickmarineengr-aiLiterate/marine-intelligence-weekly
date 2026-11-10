#!/usr/bin/env python3
"""Content gate for CORR-LP617-SIMON-P8-20261030 - follow-up B of trap 141.

The proposition is CORR-LP617-SEWAGE-SLUDGE-20261028's, carried to the oral
notes: sewage sludge is NO LONGER on the 1996 Protocol's Annex 1 list
(Resolution LP.6(17), adopted 7 October 2022, in force 15 January 2023); no new
dumping permits; an existing permit runs to expiry, not later than 31 May 2027.

Shaped after validate_correction_lp617_qb9a.py and importing the same helpers
from validate_correction_lp617.py. Differences a notes page forces:

  * The unit is a `note-card`, not a `q-card`, and its provenance stamp is a
    `note-version` span inside `note-footer`; teaching checks strip that footer
    and the stamp is checked on its own.
  * The Annex 1 list is a semicolon list under a heading, so the "permitted"
    subject is read from the heading, as validate_correction_lp617's
    dumping_sentences() already does.
  * ISOLATION: only N3 may differ from the baseline; the other seven cards
    are compared to git byte-for-byte, because the whole-file governed pin
    cannot tell which card moved.
  * The derived ORAL_NOTES_UNITS.jsonl is deliberately NOT asserted: the
    record leaves it as a frozen snapshot (see the record's note).
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
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


REL = "meoclass1/oralnotes/simon-notes-p8.html"
PAGE = REPO / REL
TWIN = REPO / "SQ" / "simon-notes-p8.html"
CARD = "n3"
BASELINE = "cfa289e"
MANIFEST = HERE / "correction_corr_lp617_simon_p8_20261030_manifest.json"
CORR_ID = "CORR-LP617-SIMON-P8-20261030"
PARENT = "CORR-LP617-SEWAGE-SLUDGE-20261028"
GOV = HERE / "qb_content_index_governed.json"
IDX = QB / "qb_content_index.json"
TRAPS = QB / "known_traps.md"
REGISTRY = REPO / "docs" / "sources" / "MIW_SOURCE_REGISTRY.json"
CORR_DATE = "2026-10-30"
SHIPPED_WRONG = "Dredged material; sewage sludge; fish waste"
CARD_RE = re.compile(r'<div class="note-card" id="(n\d+)"')


def note_card(page: str, anchor: str) -> str | None:
    at = page.find('<div class="note-card" id="%s"' % anchor)
    if at < 0:
        return None
    depth, pos = 0, at
    tok = re.compile(r"<div\b|</div>")
    while True:
        m = tok.search(page, pos)
        if not m:
            return None
        depth += -1 if m.group(0) == "</div>" else 1
        pos = m.end()
        if depth == 0:
            return page[at:pos]


def strip_note_footer(markup: str) -> str:
    at = markup.find('<div class="note-footer"')
    return markup[:at] if at >= 0 else markup


def stamp(markup: str) -> str:
    at = markup.find('<span class="note-version"')
    return LP.flatten(markup[at:]) if at >= 0 else ""


def git_show(ref: str, rel: str) -> str | None:
    out = subprocess.run(["git", "show", "%s:%s" % (ref, rel)], cwd=str(REPO),
                         capture_output=True, check=False)
    return out.stdout.decode("utf-8") if out.returncode == 0 else None


def main() -> int:
    page = read_text(PAGE)
    card = note_card(page, CARD)
    report("target_card_present", card is not None, "simon-notes-p8#%s" % CARD)
    if card is None:
        return finish()
    report("no_sq_twin_exists", not TWIN.exists(),
           "a twin would need its own identity check")

    teach = LP.flatten(strip_note_footer(card))
    n = len(LP.SLUDGE.findall(teach))
    report("non_vacuous_sludge", n >= 3, "%d mention(s)" % n)

    # 1. Sewage sludge is never taught as permitted on the card.
    bad = [s for s in LP.dumping_sentences(teach) if LP.sludge_still_permitted(s)]
    bad += LP.sludge_still_permitted(teach)
    report("no_sludge_taught_as_permitted", not bad, "found=%r" % (bad[:2] or None))
    report("shipped_wrong_phrase_absent", SHIPPED_WRONG not in teach)

    # 2. The section that shipped the defect carries the correction itself.
    sec = LP.section(teach, "Permitted Reverse List \\(Annex 1\\)", r"1996 Protocol Amendments")
    if not sec:
        sec = LP.section(teach, "Permitted Reverse List (Annex 1)", r"1996 Protocol Amendments")
    report("annex1_section_present", len(sec.split()) > 20, "%d words" % len(sec.split()))
    listed = sec.split("Sewage sludge is no longer")[0]
    report("annex1_list_excludes_sludge",
           "Dredged material" in listed and not LP.SLUDGE.search(listed),
           "list=%r" % listed[:90])
    report("annex1_section_states_removal",
           re.search(r"Sewage sludge is no longer on the list", sec) is not None
           and "LP.6(17)" in sec and "7 October 2022" in sec
           and LP.EIF_OK.search(sec) is not None,
           "LP.6(17), adoption 7 October 2022 and 15 January 2023 required")
    report("no_new_permits_and_cutoff",
           re.search(r"No new permits may be issued", sec) is not None
           and re.search(r"expiry date, but not later than 31 May 2027", sec) is not None)

    reg = LP.section(teach, "Regulatory References", r"Simon Sir")
    report("reg_box_has_lp617_row",
           re.search(r"Resolution LP\.6\(17\) Adopted 7 Oct 2022, in force 15 Jan 2023", reg)
           is not None and LP.CUTOFF_OK.search(reg) is not None)

    # 3. Closed-world dates over the card (entry into force; permit cut-off).
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
    # in the Simon tip escaped the section-only first version (independent
    # review F1, 30 Oct 2026). N3 carries no legitimate "global" wording.
    wide = [m.group(0) for m in LP.WORLDWIDE.finditer(teach)]
    report("not_taught_as_worldwide_ban", not wide, "found=%r" % (wide[:1] or None))
    widened = [s.strip()[:90] for s in LP.sentences(teach) if LP.SCOPE_1972.search(s)
               and not re.search(r"\bnot\b|\bonly\b", s)]
    report("scope_not_extended_to_1972_parties", not widened,
           "found=%r" % (widened[:1] or None))

    # 5. The stamp records the correction.
    f = stamp(card)
    report("stamp_records_correction",
           "N3 · v1.1" in f and "corrected 30 Oct 2026" in f and "LP.6(17)" in f
           and re.search(r"removed|deleted", f) is not None, "%r" % f[:80])

    # 6. Isolation: every other card on the page is byte-identical to baseline.
    base = git_show(BASELINE, REL)
    if base is None:
        report("other_cards_unchanged", False, "baseline %s unreadable" % BASELINE)
    else:
        ids = CARD_RE.findall(base)
        moved = [a for a in ids if a != CARD and note_card(base, a) != note_card(page, a)]
        report("other_cards_unchanged", len(ids) >= 8 and not moved and CARD_RE.findall(page) == ids,
               "%d card(s); moved=%s" % (len(ids), moved or "none"))

    # 7. Changelog: governed note states the correction; derived index agrees.
    gov = json.loads(read_text(GOV))
    notes = [e for e in gov.get("recently_updated", []) if e.get("date") == CORR_DATE
             and e.get("files") == ["oralnotes/simon-notes-p8.html"]]
    note = notes[0]["note"] if notes else ""
    report("governed_note_present", len(notes) == 1, "%d note(s)" % len(notes))
    report("governed_note_states_removal",
           re.search(r"sewage sludge", note, re.I) is not None
           and re.search(r"removed|no longer|deleted", note) is not None
           and "LP.6(17)" in note and "15 January 2023" in note and "31 May 2027" in note)
    idx = json.loads(read_text(IDX))
    report("generated_index_matches_governed_changelog",
           [e.get("note") for e in gov.get("recently_updated", [])]
           == [e.get("note") for e in idx.get("recently_updated", [])])

    # 8. Trap 141: follow-up B still logged as it was, and its closure recorded.
    traps = read_text(TRAPS)
    at = traps.find("### 141. Sewage sludge")
    entry = traps[at:] if at >= 0 else ""
    nxt = re.search(r"\n### \d+\.", entry[5:])
    entry = entry[:nxt.start() + 5] if nxt else entry
    report("trap_141_still_logs_followup_b",
           "- **B.** `oralnotes/simon-notes-p8.html`" in entry,
           "the open-item record is not rewritten")
    report("trap_141_closes_followup_b",
           re.search(r"\*\*Closure of follow-up B[^*]*\*\*[^\n]*\n?[^\n]*" + re.escape(CORR_ID),
                     entry) is not None)

    # 9. The record: identity, governed-artefact form, parent, expected text.
    if not MANIFEST.is_file():
        report("record_present", False, "correction record absent")
        return finish()
    rec = json.loads(read_text(MANIFEST))
    report("record_identity", rec.get("correction_id") == CORR_ID
           and rec.get("kind") == "POST_RELEASE_CORRECTION" and rec.get("cards") == [])
    text = rec.get("authority", "") + " " + rec.get("rationale", "")
    report("record_states_the_proposition",
           all(x in text for x in ("7 October 2022", "15 January 2023", "31 May 2027"))
           and re.search(r"Delete sub-paragraph 1\.2", text) is not None)
    report("record_cites_trap_141", 141 in (rec.get("known_traps_entries") or []),
           "known_traps_entries=%s" % rec.get("known_traps_entries"))
    ga = rec.get("governed_artefacts") or []
    report("record_governs_the_page_as_propagation",
           len(ga) == 1 and ga[0].get("path") == REL and ga[0].get("artefact_type") == "NOTES_PAGE"
           and ga[0].get("classification") == "ARTEFACT_PROPAGATION"
           and ga[0].get("governing_correction") == PARENT,
           "governed_artefacts=%d" % len(ga))
    report("record_expected_text_is_live",
           len(ga) == 1 and bool(ga[0].get("expected_text_after"))
           and ga[0]["expected_text_after"] in page)

    # 10. Both sources the proposition rests on name this card.
    rows = {s.get("source_id"): s for s in json.loads(read_text(REGISTRY)).get("sources", [])}
    want = ("SRC-IMO-LP6-17", "SRC-IMO-STATUS-TREATIES-VOL2-2026-09-30")
    report("sources_registered_for_the_card",
           all(w in rows and REL + "#n3" in rows[w].get("used_by", []) for w in want),
           "missing=%r" % ([w for w in want if w not in rows] or None))

    return finish()


def finish() -> int:
    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    for f in FAILS:
        print("  FAIL " + f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
