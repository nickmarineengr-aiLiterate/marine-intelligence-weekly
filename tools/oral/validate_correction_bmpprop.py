#!/usr/bin/env python3
"""
Gate for CORR-BMP-EDITION-PROP-20260905 -- the BMP Maritime Security edition
label propagated to the five cards outside QB4_H#q13.

WHAT THIS GATE IS FOR, AND WHY IT IS NOT A KEYWORD BAN
------------------------------------------------------
The corrected corpus legitimately CONTAINS the rejected wording, because it
teaches against it: q13's Common CE Failures entry says in terms that calling
BMP MS "the 2026 edition" is a failure, and known_traps entry 80 quotes the
same label in order to reject it.  A flat grep for "2026 edition" therefore
fires on the fix.  `unquoted()` below asks the only question that matters --
does any candidate-facing page ASSERT it, outside a quotation span -- which is
the E1/T2C lesson arriving for its third instance.

THE NEGATIVE SWEEP IS SCOPED, AND EACH EXCLUSION IS NAMED
----------------------------------------------------------
`meoclass1/oral-intelligence/examiner-audit/` is excluded, and not as a
convenience.  Those records are DATED EVIDENCE of what the corpus said when
they were written; one of them is the very review that reported this defect,
and `validate_oral_intake` asserts their raw wording never drifts.  Correcting
them would destroy the audit trail that proves the defect existed.

THE POSITIVE CHECKS MATTER MORE THAN THE NEGATIVE ONE
------------------------------------------------------
A sweep that only deletes a wrong label passes just as happily on a card that
now says nothing at all about the edition.  `note_carries_publisher_label_*`,
`regbox_carries_publisher_label_*` and `source_confidence_label_*` therefore
assert the CORRECT label is present in the BLOCK that carried the wrong one,
and `technique_retained_*` asserts the BMP5 content the cards exist to teach
was not collateral damage -- over-correction being the failure a "did it land?"
check cannot see.

Those per-block checks exist because the mutation suite REFUSED to run without
them.  The first draft of this gate offered `live_cards_match_authorised_state`
as the catch for six content mutations, and that check is a DIGEST PIN listed
in `oral_content_mutation.DIGEST_PINS`: it fires on any byte change at all, so
accepting it would have proved only that sha256 works.  The suite is what
found that this gate could not tell a corrected block from a changed one.

AND THE PRIMARY IS PINNED SHUT
-------------------------------
`q13_untouched` pins QB4_H#q13 to the digest CORR-GPT-T2C-CURRENCY-20260905
left it at.  This record is a propagation; if it has moved the primary's bytes
it has stopped being one, and the two records would then both claim the same
card.
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

from oral_bytes import read_text                              # noqa: E402
from validate_batch_h_series import (                         # noqa: E402
    card_digests, _balanced_end)

CORRECTION_ID = "CORR-BMP-EDITION-PROP-20260905"
MANIFEST = HERE / "correction_corr_bmp_edition_prop_20260905_manifest.json"
PREDECESSOR = HERE / "correction_corr_bmp_ms_currency_20260831_manifest.json"
T2C = HERE / "correction_corr_gpt_t2c_currency_20260905_manifest.json"
TRAPS = REPO / "meoclass1/known_traps.md"
INDEX = REPO / "meoclass1/qb_content_index.json"

# The label the publishers use, and the label they do not.
RIGHT = r"1st\s*Ed(?:ition|\.)?\s*\(?2025\)?"
WRONG = r"(?:the\s+)?2026\s+edition|current\s+edition\s+2026|" \
        r"current\s+edition\s+is\s+2026|BMP\s*MS\s*edition\s+is\s+2026|" \
        r"\(2026\s*ed\.?\)|second\s+edition\s+followed"

# Audit records are dated evidence of what the corpus SAID. Never swept.
EXCLUDED_DIRS = ("meoclass1/oral-intelligence/",)

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-46s %s" % ("PASS" if ok else "FAIL", check, detail))


def flatten(raw: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", raw)))


MAX_QUOTE_SPAN = 200


def _quoted_spans(text: str) -> list[tuple]:
    """(start, end) of every paired quotation span, curly OR straight.

    CURLY ALONE IS NOT ENOUGH, AND THIS GATE PROVED IT ON ITS FIRST RUN.
    The helper this was copied from serves HTML pages, which carry curly
    quotes.  `known_traps.md` is Markdown and rejects the wrong label as
    **"the 2026 edition"** -- straight quotes -- so the first run reported the
    trap entry that TEACHES AGAINST the defect as an instance of it.  Same
    shape as the E1 lesson: a guard spelled for one form of a mark is blind to
    the other.

    Straight quotes are ambiguous (one character opens and closes), so they are
    paired sequentially and a pair wider than MAX_QUOTE_SPAN is discarded
    rather than trusted -- a mis-pair would otherwise grant a silent amnesty to
    everything between two unrelated quotation marks.
    """
    spans, open_at = [], None
    for i, ch in enumerate(text):
        if ch == "“":
            open_at = i
        elif ch == "”" and open_at is not None:
            spans.append((open_at, i))
            open_at = None
    for mark in ('"', "`"):
        open_at = None
        for i, ch in enumerate(text):
            if ch != mark:
                continue
            if open_at is None:
                open_at = i
            else:
                if i - open_at <= MAX_QUOTE_SPAN:
                    spans.append((open_at, i))
                open_at = None
    return spans


BMP_WINDOW_BEFORE = 260
BMP_WINDOW_AFTER = 140


def _about_bmp(text: str, m: re.Match) -> bool:
    """Is this hit talking about BMP Maritime Security at all?

    THE PATTERN IS NOT SELF-SCOPING AND THAT IS A REAL DEFECT, NOT A NUISANCE.
    'the 2026 edition' is a phrase the corpus uses legitimately about other
    publications -- the HSSC Survey Guidelines in the past-paper analyses, for
    one.  A sweep that fires on those teaches the next reader that its red
    output is noise, and a gate nobody believes is a gate nobody reads.
    """
    lo = max(0, m.start() - BMP_WINDOW_BEFORE)
    return "bmp" in text[lo:m.end() + BMP_WINDOW_AFTER].lower()


def unquoted(text: str, pattern: str) -> list[str]:
    """Mentions the text ASSERTS rather than directly quotes.

    Quoting is a SPAN relation, not character adjacency. Markdown bold-quote
    spans (**"..."**) are covered too, because known_traps rejects the label in
    that form.
    """
    spans = _quoted_spans(text)
    bad = []
    for m in re.finditer(pattern, text, re.I):
        if any(a < m.start() and m.end() <= b for a, b in spans):
            continue
        if not _about_bmp(text, m):
            continue
        bad.append("..." + text[max(0, m.start() - 80):m.end()].strip())
    return bad


def card_block(page_text: str, anchor: str) -> str:
    """The card's own bytes, by BALANCED <div> nesting -- never by slicing to
    the next q-card, which runs to EOF for the last card on a page."""
    start = page_text.find('<div class="q-card" id="%s"' % anchor)
    assert start >= 0, "card not found: %s" % anchor
    return page_text[start:_balanced_end(page_text, start)]


def block_after(markup: str, needle: str, span: int) -> str:
    """Flattened text of the region that STARTS at `needle`.

    Scoped deliberately: a proposition that lives in one block must be checked
    in that block. Checking it card-wide lets a correct sibling block stand in
    for a wrong one, which is how three checks escaped in the tranche-2A suite
    and four more in 2C."""
    i = markup.find(needle)
    return flatten(markup[i:i + span]) if i >= 0 else ""


def candidate_pages() -> list[pathlib.Path]:
    """Every candidate-facing page and study document under meoclass1/,
    minus the dated audit records."""
    out = []
    for p in sorted((REPO / "meoclass1").rglob("*")):
        if p.suffix.lower() not in (".html", ".md") or not p.is_file():
            continue
        rel = p.relative_to(REPO).as_posix()
        if any(rel.startswith(d) for d in EXCLUDED_DIRS):
            continue
        out.append(p)
    return out


def main() -> int:
    man = json.loads(read_text(MANIFEST))
    pred = json.loads(read_text(PREDECESSOR))
    t2c = json.loads(read_text(T2C))

    # ---- record ---------------------------------------------------------
    report("correction_record_authorised", man["status"] == "AUTHORISED",
           man["status"])
    report("correction_record_identity",
           man["correction_id"] == CORRECTION_ID, man["correction_id"])
    report("predecessor_record_still_authorised",
           pred["status"] == "AUTHORISED",
           "the 31 Aug family this one descends from")

    # ---- supersession chain --------------------------------------------
    pred_post = {c["correction_action_id"]: c["post_edit_digest"]
                 for c in pred["cards"]}
    chain_ok, chain_detail = True, []
    for card in man["cards"]:
        sup = card.get("supersedes") or {}
        aid = sup.get("action_id")
        if aid not in pred_post:
            chain_ok = False
            chain_detail.append("%s: no predecessor action" % card["anchor"])
        elif pred_post[aid] != card["pre_edit_digest"]:
            chain_ok = False
            chain_detail.append("%s: pre-edit digest is not the predecessor's "
                                "post-edit digest" % card["anchor"])
    report("supersession_chain_unbroken", chain_ok,
           "; ".join(chain_detail) or
           "every pre-edit digest is its predecessor's post-edit digest")

    # ---- live cards match the authorised state --------------------------
    pages = {}
    live_ok, live_detail = True, []
    for card in man["cards"]:
        rel = card["path"]
        if rel not in pages:
            pages[rel] = card_digests(read_text(REPO / rel))
        got = pages[rel].get(card["anchor"])
        if got != card["post_edit_digest"]:
            live_ok = False
            live_detail.append("%s#%s" % (card["file"], card["anchor"]))
    report("live_cards_match_authorised_state", live_ok,
           ", ".join(live_detail) or "5 of 5 cards byte-exact")

    # ---- the primary is NOT this record's card --------------------------
    qb4h = card_digests(read_text(REPO / "meoclass1/QB4_H.html"))
    pinned = man["invariants"]["q13_untouched_digest"]
    t2c_q13 = next(c["post_edit_digest"] for c in t2c["cards"]
                   if c["anchor"] == "q13")
    report("q13_untouched", qb4h.get("q13") == pinned == t2c_q13,
           "propagation must not move the primary's bytes")

    # ---- the negative sweep --------------------------------------------
    offenders = []
    for p in candidate_pages():
        text = flatten(read_text(p))
        for hit in unquoted(text, WRONG):
            offenders.append("%s :: %s" % (p.relative_to(REPO).as_posix(),
                                           hit[-110:]))
    report("no_candidate_surface_asserts_a_2026_edition", not offenders,
           offenders[0] if offenders else
           "%d pages swept, 0 unquoted assertions" % len(candidate_pages()))

    # ---- the positive checks, per site, BLOCK-scoped ---------------------
    #
    # These are the checks the mutation suite must trip, and they are the
    # reason this gate is not vacuous. `live_cards_match_authorised_state` is
    # a DIGEST PIN: it fires on any byte change at all and therefore proves
    # only that sha256 works. It cannot stand as the evidence that the right
    # words are in the right blocks -- oral_content_mutation.DIGEST_PINS
    # enforces exactly that, and refused this suite until these existed.
    #
    # Each check is scoped to the BLOCK that carries its proposition, never to
    # the card and never to the page. A card-wide search for "1st Edition
    # (2025)" would pass on a card whose currentness note still said 2026, on
    # the strength of a correct reg-box thirty lines below -- the block-scope
    # escape class this repository has now hit four times.
    for card in man["cards"]:
        qid = ("%s_%s" % (card["file"].replace(".html", ""), card["anchor"])
               ).lower()
        page = read_text(REPO / card["path"])
        block = card_block(page, card["anchor"])
        flat = flatten(block)

        for surface in card["surfaces_corrected"]:
            if surface == "currentness note":
                note = block_after(block, "Currentness note", 700)
                report("note_carries_publisher_label_%s" % qid,
                       bool(re.search(RIGHT, note, re.I)),
                       "the note itself, not the card, says 1st Edition (2025)")
                report("note_drops_the_2026_edition_%s" % qid,
                       not re.search(r"current edition is 2026", note, re.I),
                       "and no longer says the current edition is 2026")
            elif surface == "reg-box":
                rb = block_after(block, "BMP Maritime Security", 320)
                report("regbox_carries_publisher_label_%s" % qid,
                       bool(re.search(RIGHT, rb, re.I)),
                       "the reg-box entry carries the label")
                report("regbox_drops_current_edition_2026_%s" % qid,
                       "current edition 2026" not in rb.lower(),
                       "")
            elif surface == "source-confidence":
                sc = block_after(block, "Source confidence", 1400)
                report("source_confidence_label_%s" % qid,
                       bool(re.search(RIGHT, sc, re.I))
                       and "no second edition" in sc.lower(),
                       "footer states the label AND that there is no second "
                       "edition")
            elif surface == "q-version":
                ver = block_after(block, 'class="q-version"', 400)
                report("version_stamped_%s" % qid,
                       "5 Sep 2026" in ver,
                       "the stamp records this correction")

        report("technique_retained_%s" % qid, "BMP5" in flat,
               "BMP5 technique content not collateral damage")

    # ---- q13's substance is untouched -----------------------------------
    h_text = flatten(read_text(REPO / "meoclass1/QB4_H.html"))
    for needle, name in (
            ("INTERTANKO", "six_publishers"),
            ("Activists", "activist_boarding_content"),
            ("global", "global_not_region_locked")):
        report("q13_substance_%s" % name, needle.lower() in h_text.lower())

    # ---- known_traps ----------------------------------------------------
    traps = read_text(TRAPS)
    report("trap_54_no_longer_asserts_a_second_edition",
           not unquoted(traps, r"second\s+edition\s+followed"),
           "entry 54 stated the defect it exists to teach against")
    report("trap_54_carries_the_publisher_label",
           bool(re.search(RIGHT, traps, re.I)))
    report("trap_80_records_the_sweep",
           CORRECTION_ID in traps and "REPORTED, not swept" in traps,
           "the report survives AND names the record that closed it")

    # ---- the record's INFORMATIONAL fields are asserted, not decorative --
    #
    # oral_manifest's field table is a closed set whose stated rule is that a
    # field is allowed in only because some correction's validator asserts it.
    # These are that assertion for this record.
    declared = man.get("known_traps_entries") or []
    headings = {int(m) for m in re.findall(r"^###\s+(\d+)\.", traps, re.M)}
    report("known_traps_entries_declared_and_exist",
           declared == [54, 80] and all(e in headings for e in declared),
           "declared=%s" % (declared or "none"))
    report("declared_artefacts_exist",
           bool(man.get("artefacts"))
           and all((REPO / a["path"]).is_file() for a in man["artefacts"]),
           "%d artefact(s)" % len(man.get("artefacts") or []))
    report("exactly_one_primary_correction",
           [c["anchor"] for c in man["cards"]
            if c["classification"] == "PRIMARY_CORRECTION"] == ["q11"],
           "q11 is the primary, as it was for the 31 August family")

    # ---- derived surfaces did not move ----------------------------------
    idx = json.loads(read_text(INDEX))
    report("canonical_questions_unchanged",
           idx["total_questions"] == man["invariants"]
           ["canonical_questions_after"], str(idx["total_questions"]))
    report("question_bearing_files_unchanged",
           idx["total_files"] == man["invariants"]["question_bearing_files"],
           str(idx["total_files"]))

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    if FAILS:
        print("failed: " + ", ".join(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
