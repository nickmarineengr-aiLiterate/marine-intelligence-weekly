#!/usr/bin/env python3
"""
Gate for CORR-IGF-CHAIN-20260905 -- the IGF six-amendment closure claim.

WHAT WENT WRONG, AND WHY A COUNT IS THE WEAKEST PART OF A CLOSURE CLAIM
------------------------------------------------------------------------
QB7_D#q15 said "the five IGF amendments in force or adopted were each opened
and read" and then listed five, omitting MSC.458(101).  The chain has six.

The failure has a shape worth naming.  q14's footer -- same page, same
instrument set -- says "All five IGF amendments" and then lists SIX of them,
because its five counts the five then IN FORCE and MSC.567(109) is added with
"plus".  q15 inherited the COUNT WORD from a sentence where it was defensible
into a sentence scoped "in force OR ADOPTED", where it is not, and dropped a
resolution to make the list agree with the number.  **The number was wrong
first and the list was edited to match it.**

That is why this gate checks the ENUMERATION and the COUNT SEPARATELY, and why
it checks both cards.  A gate that only asserted "the footer says six" would
pass on a footer that says six and lists five.

AND WHY THE HELD CORPUS IS CHECKED, NOT JUST THE PROSE
--------------------------------------------------------
The previous version of this footer was corrected once already -- from four to
five -- and was still wrong.  A card that NAMES six resolutions it does not
hold is no more reproducible than one that names five.  `held_*` therefore
walks the true-source manifest and asserts every one of the six is present with
a digest that resolves against the bytes on disk, and `registered_*` asserts
each has a registry row.  The prose claim and the custody must agree, or the
claim is decoration.

MSC.391(95) IS NOT ONE OF THE SIX
-----------------------------------
It is the resolution that ADOPTS the Code.  Counting it gives seven, which is
the error in the opposite direction and the one a reader correcting "five" in
a hurry is most likely to make.  `base_not_counted_as_amendment` guards it, and
both corrected footers say so in terms.
"""

from __future__ import annotations

import hashlib
import html as htmllib
import json
import os
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_bytes import read_text                              # noqa: E402
from validate_batch_h_series import (                         # noqa: E402
    card_digests, _balanced_end)

CORRECTION_ID = "CORR-IGF-CHAIN-20260905"
MANIFEST = HERE / "correction_corr_igf_chain_20260905_manifest.json"
PAGE = "meoclass1/QB7_D.html"
REGISTRY = REPO / "docs/sources/MIW_SOURCE_REGISTRY.json"
INDEX = REPO / "meoclass1/qb_content_index.json"

TS_ROOT = pathlib.Path(r"F:\RulesApp-Local-Input")
TS_MANIFEST = TS_ROOT / "true-source/03-imo-instruments/IGF-Code/manifest.json"

# The six amendments, in adoption order. MSC.391(95) is NOT among them.
AMENDMENTS = ["MSC.422(98)", "MSC.458(101)", "MSC.475(102)",
              "MSC.524(106)", "MSC.551(108)", "MSC.567(109)"]
BASE = "MSC.391(95)"

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-48s %s" % ("PASS" if ok else "FAIL", check, detail))


def flatten(raw: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", raw)))


def card_block(page_text: str, anchor: str) -> str:
    start = page_text.find('<div class="q-card" id="%s"' % anchor)
    assert start >= 0, "card not found: %s" % anchor
    return page_text[start:_balanced_end(page_text, start)]


def footer_of(card_html: str) -> str:
    """The source-confidence PARAGRAPH only -- to its closing </p>.

    Block-scoped on purpose. Both cards name IGF resolutions in their reg-box
    and their answer body too, so a CARD-wide enumeration check would be
    satisfied by mentions that are not the closure claim at all -- the
    block-scope escape class this repository keeps meeting.

    AND THE PARAGRAPH BOUND IS NOT COSMETIC.  This function first ran to the
    END OF THE CARD, which swept in the `q-version` stamp -- and that stamp
    says, correctly, "closure claim named five IGF amendments and omitted
    MSC.458(101)".  A version stamp DESCRIBES the defect it records; a
    negative check that reads it reports the changelog as the defect.  Same
    class as the quoted-rejection problem in the BMP sweep, reached from the
    other direction: there the fix was to respect quotation, here it is to
    respect the block boundary.
    """
    i = card_html.find("Source confidence")
    if i < 0:
        return ""
    end = card_html.find("</p>", i)
    return flatten(card_html[i:end + 4] if end >= 0 else card_html[i:])


MAX_ENUM_SPAN = 400

# The proposition each footer must still assert, verbatim. NOT a keyword.
CONCLUSION = {
    "q15": "none amends the Bunker Delivery Note annex",
    "q14": "Bunker Delivery Note annex were read from the IGF Code",
}


def enumeration_of(foot: str) -> str:
    """The LIST itself -- first MSC.422(98) through first MSC.567(109).

    NOT the whole footer, and the mutation suite is why. q15 legitimately
    names MSC.458(101) three times: in the list, in the changelog sentence
    recording that an earlier version omitted it, and in the sentence giving
    its amendment scope. A presence test over the whole footer therefore
    ESCAPED a mutation that dropped the resolution out of the list -- the
    changelog mention kept the check green while the enumeration went back to
    five. A closure claim is made by its LIST; the prose around it is
    commentary.

    The span is bounded at MAX_ENUM_SPAN so that a footer which lost its list
    entirely cannot pass by pairing a first mention with a distant last one.
    """
    i = foot.find("MSC.422(98)")
    j = foot.find("MSC.567(109)")
    if i < 0 or j < i or (j - i) > MAX_ENUM_SPAN:
        return ""
    return foot[i:j + len("MSC.567(109)")]


def main() -> int:
    man = json.loads(read_text(MANIFEST))
    page = read_text(REPO / PAGE)
    digests = card_digests(page)

    # ---- record ---------------------------------------------------------
    report("correction_record_authorised", man["status"] == "AUTHORISED",
           man["status"])
    report("correction_record_identity",
           man["correction_id"] == CORRECTION_ID, man["correction_id"])

    # ---- supersession chain ---------------------------------------------
    chain_ok, detail = True, []
    for card in man["cards"]:
        sup = card.get("supersedes") or {}
        pred = HERE / sup.get("manifest", "")
        if not pred.is_file():
            chain_ok = False
            detail.append("%s: predecessor manifest missing" % card["anchor"])
            continue
        pj = json.loads(read_text(pred))
        match = [c for c in pj["cards"]
                 if c["correction_action_id"] == sup.get("action_id")]
        if not match:
            chain_ok = False
            detail.append("%s: predecessor action missing" % card["anchor"])
        elif match[0]["post_edit_digest"] != card["pre_edit_digest"]:
            chain_ok = False
            detail.append("%s: pre-edit digest is not the predecessor's "
                          "post-edit digest" % card["anchor"])
    report("supersession_chain_unbroken", chain_ok,
           "; ".join(detail) or "both chains unbroken")

    # ---- live cards ------------------------------------------------------
    live_ok = all(digests.get(c["anchor"]) == c["post_edit_digest"]
                  for c in man["cards"])
    report("live_cards_match_authorised_state", live_ok,
           "q14 and q15 byte-exact" if live_ok else "digest mismatch")

    # ---- the enumeration, per card, BLOCK-scoped -------------------------
    #
    # These are the checks that carry this correction. The digest pin above
    # fires on any byte change at all and is listed in DIGEST_PINS, so it can
    # never be a mutation's catch and proves nothing about the content.
    for anchor in ("q14", "q15"):
        foot = footer_of(card_block(page, anchor))
        enum = enumeration_of(foot)
        missing = [r for r in AMENDMENTS if r not in enum]
        report("footer_names_all_six_%s" % anchor, not missing,
               "missing from the list: %s" % ", ".join(missing) if missing
               else "all six in the enumeration")
        report("footer_names_msc458_%s" % anchor, "MSC.458(101)" in enum,
               "the resolution the closure claim omitted")
        report("footer_says_six_not_five_%s" % anchor,
               re.search(r"\bsix\b", foot, re.I) is not None
               and re.search(r"\bfive\s+IGF\b", foot, re.I) is None,
               "count word agrees with the list")
        report("base_not_counted_as_amendment_%s" % anchor,
               BASE in foot and re.search(
                   r"not one of (?:the six|them)", foot, re.I) is not None,
               "MSC.391(95) named as the adopting resolution, not an amendment")
        report("bdn_conclusion_retained_%s" % anchor,
               CONCLUSION[anchor] in foot,
               "the substantive conclusion is still stated verbatim")

    # ---- the corpus behind the claim ------------------------------------
    if TS_MANIFEST.is_file():
        tsm = json.loads(TS_MANIFEST.read_text(encoding="utf-8-sig"))
        by_name = {}
        for f in tsm["files"]:
            by_name[pathlib.Path(f["path"].replace(chr(92), "/")).name] = f
        held, bad = [], []
        for r in AMENDMENTS + [BASE]:
            row = by_name.get("%s.pdf" % r)
            if not row:
                bad.append("%s not in manifest" % r)
                continue
            p = TS_ROOT / row["path"].replace(chr(92), os.sep)
            if not p.is_file():
                bad.append("%s file missing" % r)
                continue
            got = hashlib.sha256(p.read_bytes()).hexdigest().upper()
            if got != row["sha256"].upper():
                bad.append("%s digest mismatch" % r)
            else:
                held.append(r)
        report("held_all_six_amendments_plus_base",
               len(held) == 7 and not bad,
               "; ".join(bad) or "7 resolutions on disk, 7 digests resolve")
        pdfs = [f for f in tsm["files"] if f["path"].lower().endswith(".pdf")]
        report("no_duplicate_resolution_digests",
               len({f["sha256"] for f in pdfs}) == len(pdfs),
               "%d PDFs, %d distinct digests"
               % (len(pdfs), len({f["sha256"] for f in pdfs})))
        report("true_source_marked_complete",
               tsm.get("constructionStatus") == "complete",
               tsm.get("constructionStatus"))
    else:
        report("held_all_six_amendments_plus_base", False,
               "true-source manifest not reachable at %s" % TS_MANIFEST)

    # ---- the registry ----------------------------------------------------
    reg = json.loads(read_text(REGISTRY))
    ids = {s["source_id"]: s for s in reg["sources"]}
    want = {r: "SRC-IGF-MSC%s" % r[4:].replace("(", "-").replace(")", "")
            for r in AMENDMENTS}
    absent = [r for r, sid in want.items() if sid not in ids]
    report("registry_has_all_six_igf_rows", not absent,
           "missing: %s" % ", ".join(absent) if absent
           else "six SRC-IGF-* rows present")
    report("registry_rows_carry_digests",
           all(ids[sid].get("sha256") for sid in want.values()
               if sid in ids),
           "every registered row names the bytes it was read from")
    report("base_not_registered_as_an_amendment",
           "SRC-IGF-MSC391-95" not in ids,
           "the adopting resolution is not in the amendment rows")

    # ---- the lesson is recorded, not just the fix -----------------------
    #
    # `known_traps_entries` and `artefacts` are INFORMATIONAL in
    # oral_manifest's closed field table, and that table's own rule is that a
    # field is only allowed in because some correction's validator ASSERTS it.
    # These two checks are that assertion. Without them the fields would be
    # exactly the decoration the closed set exists to forbid.
    traps = read_text(REPO / "meoclass1/known_traps.md")
    declared = man.get("known_traps_entries") or []
    headings = {int(m) for m in re.findall(r"^###\s+(\d+)\.", traps, re.M)}
    report("known_traps_entry_declared_and_exists",
           bool(declared) and all(e in headings for e in declared),
           "declared=%s" % (declared or "none"))
    entry_81 = ""
    m81 = re.search(r"^### 81\..*?(?=^### |\Z)", traps, re.M | re.S)
    if m81:
        entry_81 = m81.group(0)
    report("known_traps_entry_carries_the_lesson",
           all(t in entry_81 for t in ("MSC.458(101)", "MSC.391(95)",
                                       "in force **or adopted**"))
           and "count" in entry_81.lower(),
           "entry 81 names the omitted resolution, the base, the scope and "
           "the count")
    report("declared_artefacts_exist",
           all((REPO / a["path"]).is_file()
               for a in (man.get("artefacts") or [])),
           "%d artefact(s)" % len(man.get("artefacts") or []))

    # ---- corpus ----------------------------------------------------------
    idx = json.loads(read_text(INDEX))
    report("canonical_questions_unchanged",
           idx["total_questions"]
           == man["invariants"]["canonical_questions_after"],
           str(idx["total_questions"]))
    report("question_bearing_files_unchanged",
           idx["total_files"] == man["invariants"]["question_bearing_files"],
           str(idx["total_files"]))

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    if FAILS:
        print("failed: " + ", ".join(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
