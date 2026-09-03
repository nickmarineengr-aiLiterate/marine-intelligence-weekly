#!/usr/bin/env python3
"""
Content validator for CORR-GRAIN-TERMINOLOGY-20260902  (QB2_A#q11 and #q33).

WHY THIS EXISTS AND WHY THE DIGEST PIN IS NOT ENOUGH
----------------------------------------------------
Two pins already covered these cards -- CORR-GRAIN-MSC552-20260831 on #q11 and
batch_h2_manifest.json/H2-002 on #q33 -- and both were green while both cards
asserted a legal consequence the International Grain Code does not contain:

    "The DoA is invalid unless accompanied by an approved Grain Stability
     Booklet"

The Code attaches no invalidity to the document. It states a different
relationship, and uses different words for the thing:

    A 3.1  the document of authorization "shall be accepted as evidence that
           the ship is capable of complying with the requirements of these
           regulations"
    A 3.2  "The document shall accompany or be incorporated into the grain
           loading manual"
    A 3.5  a ship without the document "shall not load grain until the master
           demonstrates ... that ... the ship complies"
    A 6.1  the information is provided "in printed booklet form"

So four terms do four different jobs: `grain loading manual` is the Code's own
term for the document, `printed booklet form` is the required FORMAT of the
information, `grain loading booklet` is acceptable examiner shorthand, and the
`Document of Authorization` is separate authorisation evidence.

Naming the CONSEQUENCE is what a candidate repeats to a panel, so it is the
part that must match the instrument. Each proposition is a named check, so
`mutate_correction_grainterm.py` can require its mutation to trip THAT check
rather than the digest pin, which fires on any byte change at all.

NEGATIVE CHECKS RUN ON UNESCAPED TEXT
-------------------------------------
`&ldquo;invalid&rdquo;` must be as visible to this guard as `"invalid"`, so
every search below runs against `html.unescape()` of the page.

WHY "invalid" IS NOT BANNED OUTRIGHT
------------------------------------
The corrected #q11 says, in terms, *The Code does not make the DoA "invalid" on
its own terms*, and #q33 says *the Code does not declare the Document of
Authorisation "invalid" without the booklet*. A correction that teaches which
formulation is wrong has to quote the wrong formulation -- the same reason the
LSA-ventilation entry is `GREP: SKIP` in the trap register. So the assertion is
that every mention is NEGATED or QUOTED, never that the word is absent.
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

from oral_bytes import read_text                       # noqa: E402
from validate_batch_h_series import (                  # noqa: E402
    card_digests, _balanced_end)
from oral_supersession import resolve_authorised_card_state   # noqa: E402

CORRECTION_ID = "CORR-GRAIN-TERMINOLOGY-20260902"
MANIFEST = HERE / "correction_corr_grain_terminology_20260902_manifest.json"
PAGE = "meoclass1/QB2_A.html"
ANCHORS = ("q11", "q33")

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


def card_block(page_text: str, anchor: str) -> str:
    """The card's own bytes, by BALANCED <div> nesting.

    Slicing to the next `<div class="q-card"` is wrong for the LAST card on a
    page: there is no next one, so the slice runs to EOF and swallows the page
    cheat sheet. That silently turns every "card-scoped" check into a
    page-scoped one and makes the separate page-wide checks duplicates -- which
    is exactly what happened here on QB5_I#q8, the last card in its file.
    `_balanced_end` is the canonical extractor the H-series validators use.
    """
    start = page_text.find('<div class="q-card" id="%s"' % anchor)
    assert start >= 0, "card not found: %s" % anchor
    return page_text[start:_balanced_end(page_text, start)]


NEGATORS = re.compile(
    r"(?:\bnot\b|\bnever\b|\bno\b|\bdoes not\b|\bdo not\b|\bwithout\b|"
    r"\brather than\b|\bwrong\b|\bprecisely\b|\bon its own terms\b)", re.I)

_QUOTES = '"“”‘’\''


# QB2_A is a 40-card page and legitimately says "invalid" about other things
# entirely -- an ICOF that lapses at its anniversary, a nozzle modification
# that invalidates approval. Only DoA-context invalidity is this correction's
# business, so the scan is scoped to mentions whose preceding window names the
# Document of Authorisation. A guard that flagged every "invalid" on the page
# would be reporting other cards' correct prose as this correction's defect.
_DOA_CONTEXT = re.compile(
    r"(?:document of authoris|document of authoriz|\bDoA\b)", re.I)


def invalidity_mentions(text: str) -> tuple[list[str], list[str]]:
    """Split every DoA-context invalidity mention into (acceptable, asserted)."""
    ok, asserted = [], []
    for m in re.finditer(r"invalid", text, re.I):
        if not _DOA_CONTEXT.search(text[max(0, m.start() - 200):m.start()]):
            continue
        before = text[max(0, m.start() - 200):m.start()]
        after = text[m.end():m.end() + 6]
        quoted = (before[-1:] in _QUOTES and after[:1] in _QUOTES)
        if quoted or NEGATORS.search(before):
            ok.append(m.group(0))
        else:
            asserted.append(before[-60:].strip() + " >>" + m.group(0))
    return ok, asserted


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
    digests = card_digests(page_text)
    cards = {a: flatten(card_block(page_text, a)) for a in ANCHORS}
    page = flatten(page_text)

    # ---- both pins, resolved through their chains ------------------------
    for anchor in ANCHORS:
        entry = next((c for c in record["cards"] if c["anchor"] == anchor), None)
        report("card_declared_in_record_%s" % anchor, entry is not None, anchor)
        if not entry:
            continue
        res = resolve_authorised_card_state(
            manifest=MANIFEST.name, action_id=entry["correction_action_id"],
            file=entry["file"], anchor=anchor,
            pinned_post_digest=entry["post_edit_digest"],
            live_digest=digests.get(anchor))
        report("card_digest_matches_manifest_%s" % anchor,
               bool(getattr(res, "ok", False)), "%s" % getattr(res, "status", res))
        report("supersedes_declared_%s" % anchor,
               bool(entry.get("supersedes")),
               "predecessor=%s" % (entry.get("supersedes") or {}).get("manifest"))

    q11, q33 = cards["q11"], cards["q33"]

    # ---- the Code's own wording, on the primary card ---------------------
    report("a3_2_accompany_or_incorporated",
           bool(re.search(r"accompany or be incorporated into the grain loading "
                          r"manual", q11, re.I)),
           "A 3.2 relationship stated verbatim")
    report("a3_2_cited_by_number",
           bool(re.search(r"\bA\s*3\.2\b", q11)), "A 3.2 cited")
    report("a6_1_printed_booklet_form",
           bool(re.search(r"printed booklet form", q11, re.I))
           and bool(re.search(r"\bA\s*6\.1\b", q11)),
           "A 6.1 format requirement stated and cited")
    report("a3_1_evidence_of_capability",
           bool(re.search(r"accepted as evidence that the ship is capable",
                          q11, re.I)),
           "A 3.1 evidential effect stated")
    report("a3_5_no_document_route",
           bool(re.search(r"shall not load grain until the master demonstrates",
                          q11, re.I))
           and bool(re.search(r"\bA\s*3\.5\b", q11)),
           "A 3.5 mechanism stated and cited")

    # ---- the four terms are separated, not conflated ---------------------
    report("formal_term_is_grain_loading_manual",
           bool(re.search(r"grain loading manual", q11, re.I))
           and bool(re.search(r"Code[’']s own term", q11, re.I)),
           "manual named as the Code's own term")
    report("shorthand_marked_as_shorthand",
           bool(re.search(r"grain loading booklet", q11, re.I)),
           "booklet shorthand acknowledged, not substituted")

    # ---- the retained MSC.552(108) content --------------------------------
    report("msc552_three_configurations_retained",
           bool(re.search(r"three compartment configurations", q11, re.I))
           and bool(re.search(r"MSC\.552\(108\)", q11)),
           "1 Jan 2026 third configuration intact")
    report("msc552_guidance_not_resolution_on_q33",
           bool(re.search(r"class-society and P&I practical guidance", q33, re.I))
           and bool(re.search(r"not.{0,20}in the text of MSC\.552\(108\)",
                              q33, re.I)),
           "q33 still separates guidance from the resolution text")

    # ---- the removed proposition, page-wide ------------------------------
    report("grain_stability_booklet_term_gone",
           not re.search(r"Grain Stability Booklet", page, re.I),
           "obsolete term absent corpus-page-wide")

    for anchor, text in (("q11", q11), ("q33", q33), ("page", page)):
        _, asserted = invalidity_mentions(text)
        report("doa_invalidity_never_asserted_%s" % anchor, not asserted,
               "clean" if not asserted else "asserted=%s" % asserted[:2])

    print("\n%d checks, %d FAIL%s"
          % (CHECKS, len(FAILS),
             " (%s)" % ", ".join(sorted(set(FAILS))) if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
