#!/usr/bin/env python3
"""
Content validator for CORR-MSACT-SEA-20260902  (QB9_H#q10).

WHY THIS EXISTS AND WHY THE DIGEST PIN IS NOT ENOUGH
----------------------------------------------------
No manifest pinned QB9_H#q10 at all, so this card had NO digest guard when it
shipped five candidate-visible editorial placeholders to paying candidates:

    "[cite the 2025 Act at Part level; the 1958 sections must not be quoted
     as current]"                          -- an instruction to the AUTHOR
    "[2025 Act - Part-level, sections pending verification]"   x4

The placeholders existed because a real hold existed: SRC-MSACT-2025 recorded
that section numbers beyond s.4 were not established until the 30 September
2025 corrigenda was in hand. The correction did not soften the wording -- it
RETRIEVED the corrigenda (three typographical fixes, no renumbering) and read
Part V of the Act directly.

Two propositions therefore have to hold, and they pull in opposite directions,
which is exactly why both are asserted:

  * no author-facing placeholder may EVER reappear in this card; and
  * the sections that replaced them must be the ones actually verified --
    s.63, s.64, s.83(1), s.94(1) -- with no invented neighbours and no 1958
    numbering carried across.

A future edit that "tidied" the section list by adding a plausible-looking
section number would be exactly the failure this guard exists to catch, so the
section set is asserted as a CLOSED set, not merely as a presence check.

NEGATIVE CHECKS RUN ON UNESCAPED TEXT
-------------------------------------
`&lsqb;cite` must be as visible as `[cite`, so every search runs against
`html.unescape()` of the page.
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

CORRECTION_ID = "CORR-MSACT-SEA-20260902"
MANIFEST = HERE / "correction_corr_msact_sea_20260902_manifest.json"
PAGE = "meoclass1/QB9_H.html"
ANCHOR = "q10"

# The ONLY MS Act 2025 sections established from the held Gazette text and
# cleared by the retrieved corrigenda. Anything outside this set on this card
# is an invented citation.
VERIFIED_SECTIONS = {"63", "64", "83", "94"}

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


# Author-facing scaffolding. Unlike the grain and ISM guards these ARE banned
# outright: there is no legitimate way for a production card to instruct its
# own author, so no quoting exemption is required or wanted.
PLACEHOLDERS = [
    ("no_cite_placeholder",        r"\[cite\b"),
    ("no_pending_verification",    r"pending verification"),
    ("no_bracketed_editorial",     r"\[[^\]\[<>]{4,140}\]"),
    ("no_todo_markers",            r"\bTODO\b|\bFIXME\b|\bTBD\b"),
]


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
    raw_card = card_block(page_text, ANCHOR)
    card = flatten(raw_card)

    entry = next((c for c in record["cards"] if c["anchor"] == ANCHOR), None)
    report("card_declared_in_record", entry is not None, ANCHOR)
    if entry:
        res = resolve_authorised_card_state(
            manifest=MANIFEST.name, action_id=entry["correction_action_id"],
            file=entry["file"], anchor=ANCHOR,
            pinned_post_digest=entry["post_edit_digest"],
            live_digest=card_digests(page_text).get(ANCHOR))
        report("card_digest_matches_manifest", bool(getattr(res, "ok", False)),
               "%s" % getattr(res, "status", res))

    # ---- no placeholder may EVER return to a paid card -------------------
    for name, pattern in PLACEHOLDERS:
        hit = re.search(pattern, card, re.I)
        report(name, hit is None,
               "clean" if not hit else "card carries: %r" % hit.group(0)[:70])

    # ---- the verified sections are present -------------------------------
    report("s63_agreement_with_seafarers",
           bool(re.search(r"s\.?\s*63", card, re.I))
           and bool(re.search(r"seafarers?[’']? employment agreement",
                              card, re.I)),
           "s.63 SEA obligation stated")
    report("s63_copy_to_shipping_master",
           bool(re.search(r"shipping master", card, re.I))
           and bool(re.search(r"copy", card, re.I)),
           "copy to the shipping master stated")
    report("s63_3_examine_and_seek_advice",
           bool(re.search(r"examine and seek advice", card, re.I)),
           "s.63(3) pre-signature right stated")
    report("s64_monthly_account",
           bool(re.search(r"s\.?\s*64", card, re.I))
           and bool(re.search(r"monthly account", card, re.I)),
           "s.64 wages / monthly account stated")
    report("s83_disputes_to_shipping_master",
           bool(re.search(r"s\.?\s*83\(1\)", card, re.I)),
           "s.83(1) dispute route stated")

    # ---- and NOTHING outside the verified set is cited -------------------
    cited = set(re.findall(r"\bs\.\s*(\d{1,3})", card, re.I))
    invented = sorted(cited - VERIFIED_SECTIONS)
    report("no_unverified_ms_act_sections", not invented,
           "cited=%s invented=%s" % (sorted(cited), invented or "none"))

    # ---- the 1958 Act must never be cited as CURRENT ---------------------
    stale = [m.group(0) for m in re.finditer(r"1958", card)]
    negated = bool(re.search(r"[Dd]o not carry 1958 numbering across", card))
    report("no_1958_numbering_as_current",
           (not stale) or negated,
           "1958 mentions=%d, warning present=%s" % (len(stale), negated))

    # ---- the MLC core answer the correction had to preserve --------------
    report("mlc_a2_1_core_preserved",
           bool(re.search(r"Std\s*A2\.1", card))
           and bool(re.search(r"copy.{0,60}onboard|onboard.{0,40}copy",
                              card, re.I)),
           "SEA under MLC Std A2.1 with the onboard copy intact")
    report("mlc_a2_2_wage_accounts_preserved",
           bool(re.search(r"Std\s*A2\.2", card)), "A2.2 wage accounts intact")
    report("mlc_a2_1_3_neutral_discharge_preserved",
           bool(re.search(r"A2\.1\.3", card)), "neutral discharge record intact")
    report("classical_articles_layer_preserved",
           bool(re.search(r"Articles of Agreement|ship[’']s articles",
                          card, re.I)),
           "the classical instrument is still taught")

    print("\n%d checks, %d FAIL%s"
          % (CHECKS, len(FAILS),
             " (%s)" % ", ".join(sorted(set(FAILS))) if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
