#!/usr/bin/env python3
"""
Content validator for CORR-CIC-STEM-20260903  (QB8_C#q4).

WHY THIS EXISTS AND WHY THE DIGEST PIN IS NOT ENOUGH
----------------------------------------------------
QB8_C#q4 asked the candidate to explain CIC and expanded it in the QUESTION
STEM as "Consolidated Inspection Campaign". No such campaign exists. The port
State control term is the CONCENTRATED Inspection Campaign, and the Paris MoU
and Tokyo MOU define it themselves in their joint press release of 3 August
2026:

    "The Member Authorities of the Tokyo MOU and Paris MoU will undertake a
     Concentrated Inspection Campaign (CIC) on Cargo Securing of Cargo Units
     and Cargo Transport Units. This CIC will be conducted from 1 September to
     30 November 2026."

The card's own ANSWER BODY was already correct -- its second heading reads
"CIC Type 2: PSC Concentrated Inspection Campaign (Tokyo MOU / Paris MOU)".
So the page contradicted itself, and the wrong half was the half a candidate
reads first and the half every generated surface copies.

No pin could have caught it: the card had never been declared by any batch or
correction manifest, and even had it been, a pin answers "are these the bytes
we authorised?" and never "is what we authorised correct?" (SKILL.md 8.2a).

THE CHECK NOTHING IN THE SUITE HAD
----------------------------------
`stem_and_body_agree` is the general control this correction contributes: the
expansion the stem gives for CIC must be the expansion the body teaches. A
card that disagrees with itself is a defect class no digest, no count and no
byte scan can see, and it survived a clean full-suite qualification.

A STEM IS NOT DECORATION -- SO THE DERIVED SURFACES ARE CHECKED TOO
------------------------------------------------------------------
known_traps entry 50 established it and this is its second instance: the
q-card `.q-text` div is parsed by `oral_lib.parse_qb_file` and copied into the
content index, the hub search records, the generated examiner index, the topic
pages and the study mapping store. `derived_*` below assert the corrected term
SURVIVES REGENERATION on each of them, because a fix that regresses the moment
someone re-runs a generator is not a fix.

NEGATIVE CHECKS RUN ON UNESCAPED TEXT, AND ARE SCOPED
-----------------------------------------------------
Every search runs against `html.unescape()` of the page: a guard spelled for
plain text is blind to the entity form, which is the E1 lesson.

The negative sweep is deliberately NOT a flat repository grep. The correction's
own candidate-facing changelog note quotes the rejected expansion once in order
to reject it -- SKILL.md 8.2a rule 2, the same reason the trap entry is
`GREP: SKIP` -- so the changelog carriers are named exemptions here rather than
being allowed to fail the guard that protects them. The audit records under
`oral-intelligence/examiner-audit/` are excluded for a different and stronger
reason: they are DATED EVIDENCE of what the corpus said when they were written,
`validate_oral_intake` asserts their raw wording never drifts, and one of them
is the very adjudication that reported this defect.
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
from oral_supersession import resolve_authorised_card_state   # noqa: E402

CORRECTION_ID = "CORR-CIC-STEM-20260903"
MANIFEST = HERE / "correction_corr_cic_stem_20260903_manifest.json"
PAGE = "meoclass1/QB8_C.html"
ANCHOR = "q4"
QID = "QB8_C#q4"

RIGHT = "Concentrated Inspection Campaign"
WRONG = "Consolidated Inspection Campaign"

# Carriers that legitimately quote the rejected expansion, and why.
CHANGELOG_CARRIERS = {
    "tools/oral/qb_content_index_governed.json":
        "the governed source of the candidate-facing correction log",
    "meoclass1/qb_content_index.json":
        "the generated copy of that same log",
}

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-44s %s" % ("PASS" if ok else "FAIL", check, detail))


def flatten(raw: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", raw)))


def card_block(page_text: str, anchor: str) -> str:
    """The card's own bytes, by BALANCED <div> nesting -- never by slicing to
    the next q-card, which runs to EOF for the last card on a page and turns a
    card-scoped check into a page-scoped one."""
    start = page_text.find('<div class="q-card" id="%s"' % anchor)
    assert start >= 0, "card not found: %s" % anchor
    return page_text[start:_balanced_end(page_text, start)]


def stem_of(card_html: str) -> str:
    """The candidate-facing question stem: the q-text div, unescaped."""
    m = re.search(r'<div class="q-text">(.*?)</div>', card_html, re.S)
    return flatten(m.group(1)) if m else ""


def body_of(card_html: str) -> str:
    """The answer region only -- everything after the q-header block."""
    i = card_html.find('<div class="q-answer">')
    return flatten(card_html[i:]) if i >= 0 else ""


def cic_expansions(text: str) -> set:
    """Every '<Word> Inspection Campaign' expansion present in the text."""
    return {m.group(1).lower()
            for m in re.finditer(r"\b(\w+)\s+Inspection Campaign\b", text, re.I)}


def read_json(rel: str):
    return json.loads(read_text(REPO / rel))


def main() -> int:
    print("correction content validator: %s" % CORRECTION_ID)

    if not MANIFEST.is_file():
        report("correction_record_present", False, "missing %s" % MANIFEST.name)
        print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
        return 1
    record = json.loads(read_text(MANIFEST))
    report("correction_record_present", True, MANIFEST.name)
    report("correction_record_authorised",
           record.get("status") == "AUTHORISED"
           and record.get("correction_id") == CORRECTION_ID,
           "status=%s" % record.get("status"))

    page_text = read_text(REPO / PAGE)
    card = card_block(page_text, ANCHOR)
    stem = stem_of(card)
    body = body_of(card)
    page = flatten(page_text)

    entry = next((c for c in record.get("cards", [])
                  if c["anchor"] == ANCHOR), None)
    report("card_declared_in_record", entry is not None, ANCHOR)
    if entry:
        res = resolve_authorised_card_state(
            manifest=MANIFEST.name, action_id=entry["correction_action_id"],
            file=entry["file"], anchor=ANCHOR,
            pinned_post_digest=entry["post_edit_digest"],
            live_digest=card_digests(page_text).get(ANCHOR))
        report("card_digest_matches_manifest",
               bool(getattr(res, "ok", False)),
               "%s" % getattr(res, "status", res))

    # ---- 1. the stem itself ----------------------------------------------
    report("stem_uses_concentrated", RIGHT.lower() in stem.lower(),
           "stem=%r" % stem[:70])
    report("stem_never_says_consolidated", WRONG.lower() not in stem.lower(),
           "rejected expansion absent from the stem")

    # ---- 2. the body still teaches the PSC campaign correctly ------------
    report("body_teaches_psc_concentrated",
           bool(re.search(r"PSC\s+Concentrated Inspection Campaign", body, re.I)),
           "Type 2 heading intact")
    report("body_never_says_consolidated", WRONG.lower() not in body.lower(),
           "rejected expansion absent from the answer")

    # ---- 3. THE GENERAL CONTROL: the card must agree with itself ---------
    in_stem, in_body = cic_expansions(stem), cic_expansions(body)
    report("stem_and_body_agree", bool(in_stem) and in_stem <= in_body,
           "stem=%s body=%s" % (sorted(in_stem), sorted(in_body)))

    # ---- 4. the facts re-verified against the 3 Aug 2026 press release ---
    report("body_window_retained",
           bool(re.search(r"1\s+September", body, re.I))
           and bool(re.search(r"30\s+November", body, re.I)),
           "1 September to 30 November window intact")
    report("body_both_senses_retained",
           bool(re.search(r"Cargo Integrity Check", body, re.I))
           and bool(re.search(r"Tokyo MOU", body, re.I))
           and bool(re.search(r"Paris MOU", body, re.I)),
           "industry sense and PSC sense both present")
    report("body_questionnaire_mechanism_retained",
           bool(re.search(r"questionnaire", body, re.I)),
           "pre-published questionnaire mechanism intact")

    # ---- 5. no candidate-facing page anywhere carries the wrong term -----
    offenders = []
    for d in ("meoclass1", "SQ", "solvedQP"):
        root = REPO / d
        if not root.is_dir():
            continue
        for p in sorted(root.rglob("*.html")):
            if WRONG.lower() in flatten(read_text(p)).lower():
                offenders.append(str(p.relative_to(REPO)).replace("\\", "/"))
    report("no_candidate_page_says_consolidated", not offenders,
           "offenders=%s" % (offenders or "none"))

    # ---- 6. the corrected term SURVIVES REGENERATION on every derived
    #         surface that copies the stem (known_traps entry 50) ----------
    idx = read_json("meoclass1/qb_content_index.json")
    idx_q = next((q for q in idx["files"]["QB8_C.html"]["questions"]
                  if q["anchor"] == ANCHOR), None)
    report("derived_content_index",
           bool(idx_q) and RIGHT in idx_q["text"] and WRONG not in idx_q["text"],
           "qb_content_index.json text")

    hub = read_text(REPO / "meoclass1/index.html")
    hub_rec = re.search(
        r'\{"q": "([^"]*?)", "file": "QB8_C\.html", "qb": "[^"]*", '
        r'"anchor": "q4"\}', hub)
    report("derived_hub_search_records",
           bool(hub_rec) and RIGHT in hub_rec.group(1)
           and WRONG not in hub_rec.group(1),
           "index.html Q_INDEX record")

    ex = flatten(read_text(REPO / "meoclass1/examiner-index.html"))
    report("derived_examiner_index",
           RIGHT.lower() in ex.lower() and WRONG.lower() not in ex.lower(),
           "examiner-index.html display text")

    topics = flatten(read_text(REPO / "meoclass1/topics.html"))
    report("derived_topic_pages",
           RIGHT.lower() in topics.lower() and WRONG.lower() not in topics.lower(),
           "topics.html question list")

    maps = read_json("docs/study/study_mappings.json")["mappings"].get(QID)
    report("derived_study_mappings",
           bool(maps) and RIGHT in maps["text"] and WRONG not in maps["text"],
           "study_mappings.json store text")

    # ---- 7. the quoting exemptions are REAL, not a blanket amnesty -------
    #      Each named carrier must actually be a changelog carrier that
    #      quotes the term inside a correction note. If one stops quoting it
    #      the exemption is stale and should be removed, not left standing.
    stale = []
    for rel in CHANGELOG_CARRIERS:
        blob = read_text(REPO / rel)
        notes = " ".join(
            e.get("note", "") for e in json.loads(blob).get("recently_updated", []))
        if WRONG not in notes:
            stale.append(rel)
    report("changelog_quoting_exemptions_are_live", not stale,
           "stale=%s" % (stale or "none"))

    print("\n%d checks, %d FAIL%s"
          % (CHECKS, len(FAILS),
             " (%s)" % ", ".join(sorted(set(FAILS))) if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
