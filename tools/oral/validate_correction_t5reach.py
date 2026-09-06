#!/usr/bin/env python3
"""Content gate for CORR-T5-REACH-20260906 -- correction reach.

WHAT THIS GATE HAS TO DO THAT NO PIN CAN
----------------------------------------
Three of this record's eight sites are on cheat sheets, which carry no q-card
and therefore take NO DIGEST PIN AT ALL. They are recorded in `artefacts`
without one, deliberately - a pin on an unguarded file expires on the next
unrelated edit to it. So for those three surfaces this gate is the ONLY thing
in the toolchain that can tell whether the correction is still there. If it
checked only the four pinned cards, N-2 and N-4 would be entirely unguarded
while looking recorded.

WHY EVERY CHECK IS A NEGATION-OR-QUOTATION TEST, NEVER A BANNED-PHRASE GREP
---------------------------------------------------------------------------
A correction to a superseded label QUOTES the label it rejects. Ninety-four of
the 102 corpus occurrences of "BMP5" are legitimate: the examiner's own question
wording, a TOC entry echoing it, a currentness note that names BMP5 in order to
deny it, and QB4_H#q11 which is retained ON PURPOSE as the predecessor record.
A flat "BMP5 must be absent" check would fail on the very sentences carrying the
fix, and a sweep written to satisfy it would destroy the evidence.

So each corrected surface is asserted to say the CURRENT publication in the slot
that teaches, and the KEEP surfaces are asserted to still say BMP5 - because a
future over-eager sweep removing the examiner's own wording is a real failure
mode, and only a positive check catches it. The gate binds in both directions.

WHY THE REG-CODE SLOT IS CHECKED ON ITS OWN
-------------------------------------------
known_traps entry 89 records that a wrong reg-code hid behind a right reg-desc
until the code slot was checked separately. Three of these edits are reg-box
rows, so the code and the description are asserted independently.
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

CORRECTION_ID = "CORR-T5-REACH-20260906"
MANIFEST = HERE / "correction_corr_t5_reach_20260906_manifest.json"
QB_ROOT = REPO / "meoclass1"
INDEX = REPO / "meoclass1/qb_content_index.json"
TRAPS = REPO / "meoclass1/known_traps.md"

CURRENT = "BMP Maritime Security"

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


def source_confidence(card: str) -> str:
    """The source-confidence PARAGRAPH only.

    Block-scoped because the card names BMP publications in its reg-box, its
    currentness note and its version stamp too. A card-wide check would be
    satisfied by any of them and would not be reading the footer at all - which
    is precisely the defect N-1 records.
    """
    i = card.find("Source confidence")
    if i < 0:
        return ""
    end = card.find("</p>", i)
    return flat(card[i:end + 4] if end >= 0 else card[i:])


def without_provenance(card: str) -> str:
    """The card with its version stamp and correction link removed.

    A correction stamp necessarily QUOTES the wording it removed - QB5_B#q14's
    new stamp says the body used to teach "BMP5 engineering measures". A
    card-wide negative check therefore reports the changelog as the defect,
    which is known_traps entry 89 exactly, and this gate reproduced it the
    moment provenance was added. Negative checks run on the teaching layers.
    """
    card = re.sub(r'<span class="q-version">.*?</span>', " ", card, flags=re.S)
    card = re.sub(r'<span class="correction-link">.*?</span>', " ", card,
                  flags=re.S)
    return card


def reg_rows(card: str):
    """(code, desc) for every reg-box row, with the slots kept apart."""
    return [(flat(m.group(1)).strip(), flat(m.group(2)).strip())
            for m in re.finditer(
                r'<span class="reg-code">(.*?)</span>'
                r'<span class="reg-desc">(.*?)</span>', card, re.S)]


def main() -> int:
    man = json.loads(read_text(MANIFEST))
    report("manifest_is_this_correction",
           man.get("correction_id") == CORRECTION_ID, man.get("correction_id"))
    report("status_authorised", man.get("status") == "AUTHORISED",
           man.get("status"))

    qb4h = read_text(QB_ROOT / "QB4_H.html")
    qb1f = read_text(QB_ROOT / "QB1_F.html")
    qb5b = read_text(QB_ROOT / "QB5_B.html")

    # ================= N-1 : the source-confidence footer =================
    foot = source_confidence(card_block(qb4h, "q2"))
    report("N1_footer_exists", bool(foot), "%d chars" % len(foot))
    report("N1_footer_no_longer_cites_BMP5_as_verification_authority",
           "BMP5 Section 5" not in foot and "mscio.eu" not in foot,
           "the superseded section-number citation is gone from the footer")
    report("N1_footer_cites_the_held_current_publication",
           CURRENT in foot and "1st Edition (2025)" in foot
           and "June 2026" in foot,
           "footer names BMP MS 1st Edition (2025) as updated June 2026")
    report("N1_footer_agrees_with_its_own_card_body",
           "unverifiable" in flat(card_block(qb4h, "q2")).lower()
           or "could not be verified" in flat(card_block(qb4h, "q2")),
           "the card still records WHY the old citation went")

    # ================= N-2 : the cheat-sheet circular ======================
    cs9a = read_text(QB_ROOT / "QB9_A_CheatSheet.html")
    report("N2_circular_removed_from_the_cheat_sheet",
           "MSC.1/Circ.1606" not in cs9a, "no MSC.1/Circ.1606 pill remains")
    report("N2_no_replacement_circular_was_guessed",
           len(re.findall(r'<code class="num-pill">MSC\.1/Circ\.\d+</code>',
                          cs9a)) == 0,
           "nothing was invented in its place")
    report("N2_no_empty_numbers_row_was_left_behind",
           '<div class="nums-row"></div>' not in cs9a
           and not re.search(r'Numbers &amp; Codes</div><div class="nums-row">'
                             r'\s*</div>', cs9a),
           "the row went with the pills rather than becoming an empty promise")
    report("N2_parent_card_still_records_the_removal",
           "MSC.1/Circ.1606" in read_text(QB_ROOT / "QB9_A.html"),
           "QB9_A#q9's version stamp still names what it removed - the "
           "provenance is not swept")

    # ================= N-4a : QB5_B cheat sheet ============================
    cs5b = read_text(QB_ROOT / "QB5_B_CheatSheet.html")
    q34 = re.search(r"Q34 &mdash; War Zone Crew Management|Q34 — War Zone Crew "
                    r"Management", cs5b)
    cell = ""
    if q34:
        end = cs5b.find("</div></div>", q34.end())
        cell = flat(cs5b[q34.end():end])
    report("N4a_cell_found", bool(cell), "%d chars" % len(cell))
    report("N4a_teaches_the_current_publication",
           CURRENT in cell, "Q34 names BMP Maritime Security")
    report("N4a_does_not_teach_BMP5_as_a_live_procedure",
           "BMP5 procedures" not in cell,
           "the positive-current phrasing is gone")
    report("N4a_supersession_is_stated_not_merely_renamed",
           "replaced BMP5" in cell,
           "the cell says what it replaced, so a candidate asked about BMP5 "
           "can still answer")

    # ================= N-4b : QB4_H cheat sheet, cue KEPT ==================
    cs4h = read_text(QB_ROOT / "QB4_H_cheatsheet.html")
    row11 = re.search(r"<tr><td>11</td>(.*?)</tr>", cs4h, re.S)
    row11 = row11.group(1) if row11 else ""
    report("N4b_row_found", bool(row11), "%d chars" % len(row11))
    report("N4b_examiner_cue_is_KEPT_not_rewritten",
           '"BMP5 details"' in row11,
           "the examiner's own wording survives - this is the check that "
           "catches an over-eager future sweep")
    report("N4b_answer_cell_carries_the_predecessor_status",
           "Predecessor publication" in row11 and CURRENT in row11
           and "Q13" in row11,
           "the answer cell now says what the parent card says")

    # ================= A-5 / A-6 / A-7 : card-layer reg rows ===============
    for label, text, anchor in (("A5", qb1f, "q10"), ("A6", qb4h, "q6"),
                                ("A7", qb5b, "q14")):
        rows = reg_rows(without_provenance(card_block(text, anchor)))
        codes = [c for c, _ in rows]
        # The CODE slot on its own - entry 89's lesson.
        stale_code = [c for c in codes if re.search(r"BMP\s?5\b", c)]
        report("%s_reg_code_slot_names_no_superseded_publication" % label,
               not stale_code, str(stale_code or "none"))
        report("%s_reg_code_slot_names_the_current_publication" % label,
               any(CURRENT in c for c in codes),
               "codes: %s" % [c for c in codes if "BMP" in c])
        desc = " ".join(d for c, d in rows if CURRENT in c)
        report("%s_reg_desc_states_what_it_replaced" % label,
               "BMP5" in desc,
               "the description quotes the superseded name so a candidate "
               "asked for BMP5 is not stranded")

    # A-7 also has an answer-body site
    body = flat(without_provenance(card_block(qb5b, "q14")))
    report("A7_answer_body_no_longer_teaches_BMP5_measures",
           "BMP5 engineering measures" not in body
           and "BMP Maritime Security engineering measures" in body,
           "the answer body names the current publication")

    # ================= the KEEP boundary, asserted positively =============
    # A sweep that removed the examiner's own wording would be a real defect,
    # and only a positive check catches it. These four must STILL say BMP5.
    keeps = [
        ("QB4_H.html q11 stem", card_block(qb4h, "q11")),
        ("QB9_A.html q9 stem", card_block(read_text(QB_ROOT / "QB9_A.html"), "q9")),
        ("QB9_B.html q5 stem", card_block(read_text(QB_ROOT / "QB9_B.html"), "q5")),
        ("QB4_B.html q16 stem", card_block(read_text(QB_ROOT / "QB4_B.html"), "q16")),
    ]
    for name, blk in keeps:
        stem = re.search(r'<div class="q-text">(.*?)</div>', blk, re.S)
        report("KEEP_examiner_wording_survives_%s" % name.split()[0].replace(".html", ""),
               bool(stem) and "BMP5" in stem.group(1),
               "%s still quotes the examiner" % name)
    # The BANNER at the head of the answer, specifically. The card's
    # source-confidence footer also uses the word "PREDECESSOR", so a
    # card-wide substring test survived a mutation that deleted the banner a
    # candidate actually reads - caught by mutation K.
    q11 = card_block(qb4h, "q11")
    banner = re.search(r'<div class="practice-block">(.*?)</div>', q11, re.S)
    report("KEEP_predecessor_card_is_still_a_predecessor_record",
           bool(banner) and "Predecessor publication" in banner.group(1)
           and "superseded" in banner.group(1) and "Q13" in banner.group(1),
           "QB4_H#q11 still opens with its predecessor banner")

    # ================= digests and corpus =================================
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

    # ================= governance =========================================
    report("declared_artefacts_exist",
           all((REPO / a["path"]).is_file() for a in man["artefacts"]),
           "%d artefact(s)" % len(man["artefacts"]))
    report("cheat_sheets_are_declared_as_unpinned_artefacts",
           sum(1 for a in man["artefacts"]
               if "heet" in a["path"] and "known_traps" not in a["path"]) == 3
           and all("digest" not in a for a in man["artefacts"]),
           "three revision surfaces recorded WITHOUT a digest, per the schema")
    traps = read_text(TRAPS)
    for n, needles in ((94, ("finding's card list", "94 are KEEP", "SURFACE")),
                       (95, ("no digest pin", "content gate"))):
        m = re.search(r"### %d\..*?(?=\n### |\Z)" % n, traps, re.S)
        body_t = m.group(0) if m else ""
        report("known_traps_entry_%d_carries_the_lesson" % n,
               bool(body_t) and all(x in body_t for x in needles),
               "entry %d" % n)
    report("record_states_what_was_deliberately_not_swept",
           "deliberately_not_swept" in man["propagation"]
           and "94 of the 102" in man["propagation"]["deliberately_not_swept"],
           "the KEEP boundary is in the record, not only in the code")
    overlap = man["propagation"].get(
        "cards_edited_here_but_pinned_by_a_sibling_record", "")
    report("sibling_pinned_card_is_declared",
           "QB1_F.html#q10" in overlap
           and "CORR-T5-DDCASCADE-20260906" in overlap,
           "A-5's card is pinned by the structural record; the overlap is "
           "recorded as structure, and A-5's propositions are asserted above")
    report("ambiguous_site_is_reported_not_silently_dropped",
           "ambiguous_reported_not_corrected" in man["propagation"],
           "QB4_B page-level provenance disclaimer is named")

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    if FAILS:
        print("failed: " + ", ".join(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
