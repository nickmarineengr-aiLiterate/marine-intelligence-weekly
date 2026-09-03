#!/usr/bin/env python3
"""
Content validator for CORR-ISM-SPARES-20260902  (QB5_I#q8).

WHY THIS EXISTS AND WHY THE DIGEST PIN IS NOT ENOUGH
----------------------------------------------------
`validate_corrections.py` answers "is this card still exactly the bytes that
were authorised?". H6's pin on this card was green for a week while the card
carried the defect this record corrects, because a pin is perfectly happy with
wrong text -- it pins whatever it is given.

The defect was a regulatory overstatement, in two directions at once:

  * ISM 10.3 was said to DRIVE / DERIVE the critical-spares list, and to stand
    behind a minimum stock and a reorder point. It does none of those things.
    It requires the Company to IDENTIFY equipment whose sudden operational
    failure may result in hazardous situations, and requires the SMS to provide
    specific measures promoting the reliability of that equipment, those
    measures to include the regular testing of stand-by arrangements.
  * An unobtainable critical spare was said to BE a non-conformity under
    ISM 9. Whether it is one is answered by ISM 1.1.9 -- objective evidence of
    the non-fulfilment of a SPECIFIED requirement -- not by the fact that
    procurement failed.

And a mis-citation travelled with it: 10.3's second and third limbs were filed
under 10.4 throughout, while 10.4's actual content (integration of the 10.2
inspections and the 10.3 measures into the ship's operational maintenance
routine) appeared nowhere on the card.

Each proposition a future well-meaning edit could quietly lose is asserted
below as a NAMED check, so `mutate_correction_ismspares.py` can require that
its mutation trips THAT check and never merely the digest pin, which fires on
any byte change at all.

NEGATIVE CHECKS RUN ON UNESCAPED TEXT
-------------------------------------
A guard spelled `h&m` is blind to `h&amp;m`. Every banned-phrase search below
runs against `html.unescape()` of the page, never the raw markup.
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

CORRECTION_ID = "CORR-ISM-SPARES-20260902"
MANIFEST = HERE / "correction_corr_ism_spares_20260902_manifest.json"
PAGE = "meoclass1/QB5_I.html"
ANCHOR = "q8"

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


# --------------------------------------------------------------- banned forms
#
# These are the ACTUAL wordings the card carried before the correction. None of
# them is quoted by the corrected card -- it teaches the right hierarchy rather
# than naming the wrong one -- so unlike the LSA-ventilation guard these can be
# banned outright rather than required to be negated. If a future edit ever
# does want to quote one in order to reject it, this guard must be upgraded to
# the negation-aware form, not deleted.
BANNED_CARD = [
    ("no_derivation_claim",   r"critical-equipment list under ISM 10\.3 drives"),
    ("no_derivation_claim",   r"critical-spares list is derived from"),
    ("no_derivation_claim",   r"derived from the critical-equipment list"),
    ("no_derivation_claim",   r"ISM 10\.3[^.]{0,40}\bdrives\b"),
    ("no_automatic_ism9",     r"I raise it as a non-conformity under ISM 9"),
    ("no_automatic_ism9",     r"that goes on the record under ISM 9"),
    ("no_automatic_ism9",     r"Refused critical spare\s*(?:→|->)\s*ISM 9 non-conformity"),
    ("ism_10_4_not_reliability",
     r"10\.4 requires measures to promote reliability"),
    ("ism_10_4_not_reliability", r"ISM 10\.4 also brings in what must be"),
    ("ism_10_4_not_reliability", r"10\.4\s*adds stand-by arrangements"),
    ("no_spares_list_source_claim",
     r"the source of the critical-spares list"),
    ("no_spares_list_source_claim",
     r"the origin of the critical-spares list"),
]

# The page-level cheat sheet carries no q-card and is pinned by no guard, which
# is exactly how it kept the corrected-away wording for a week after the body
# was fixed (known_traps entry 51: after any repair, search the whole FILE).
BANNED_PAGE = BANNED_CARD


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
    page = flatten(page_text)

    # ---- the digest the record pins, resolved through the chain -----------
    entry = next((c for c in record["cards"] if c["anchor"] == ANCHOR), None)
    report("card_declared_in_record", entry is not None, ANCHOR)
    if entry:
        live = card_digests(page_text).get(ANCHOR)
        res = resolve_authorised_card_state(
            manifest=MANIFEST.name, action_id=entry["correction_action_id"],
            file=entry["file"], anchor=ANCHOR,
            pinned_post_digest=entry["post_edit_digest"], live_digest=live)
        report("card_digest_matches_manifest", bool(getattr(res, "ok", False)),
               "%s" % getattr(res, "status", res))
        report("supersedes_h6_pin",
               (entry.get("supersedes") or {}).get("manifest")
               == "batch_h6_manifest.json",
               "predecessor=%s"
               % (entry.get("supersedes") or {}).get("manifest"))

    # ---- ISM 10.3: all three limbs, on the card --------------------------
    report("ism_10_3_identification_limb",
           bool(re.search(r"identify (?:the )?equipment[^.]{0,120}"
                          r"sudden (?:operational )?failure", card, re.I)),
           "10.3 first limb present")
    report("ism_10_3_reliability_limb",
           bool(re.search(r"promoting (?:its |their |the )?reliability", card, re.I)),
           "10.3 second limb present")
    report("ism_10_3_standby_testing_limb",
           bool(re.search(r"regular testing of stand-?by arrangements", card, re.I)),
           "10.3 third limb present")

    # ---- ISM 10.4 says what 10.4 actually says ---------------------------
    #
    # Asserted in BOTH surfaces, deliberately not as an OR. A correction that
    # fixes the prose and leaves the reg-box stale is a documented escape shape
    # in this repository (see mutate_correction_g1_010's second-pass mutation),
    # and the reg-box is the surface a candidate scans under pressure. An OR
    # here would let either half rot while the check stayed green.
    report("ism_10_4_is_integration",
           bool(re.search(r"10\.4[^.]{0,160}operational maintenance routine",
                          card, re.I)),
           "10.4 = integration, in the body")
    regbox = re.search(r'ISM Code 10\.4</span><span class="reg-desc">([^<]*)',
                       raw_card)
    report("ism_10_4_regbox_is_integration",
           bool(regbox) and "integration" in regbox.group(1).lower()
           and "reliability" not in regbox.group(1).lower().split("10.3")[0],
           "reg-box row=%r" % (regbox.group(1)[:70] if regbox else None))

    # ---- the hierarchy the card must teach -------------------------------
    report("spares_list_is_informed_not_derived",
           bool(re.search(r"informed by", card, re.I))
           and bool(re.search(r"SMS and PMS|safety-management system", card, re.I)),
           "10.3 identifies -> SMS/PMS translates -> CE manages")
    report("stock_arithmetic_not_prescribed_by_code",
           bool(re.search(r"prescribed by the ISM Code", card, re.I)),
           "reorder point stated as management technique, not Code requirement")

    # ---- ISM 9 is conditional, never automatic ---------------------------
    report("ism9_conditional_on_sms_definition",
           bool(re.search(r"(?:meets|met)[^.]{0,80}definition of a non-conformity",
                          card, re.I)),
           "ISM 9 gated on the SMS's own definition")

    # ---- the retained SOLAS figure ---------------------------------------
    # Presence is not enough. The card states this ceiling in three places --
    # body, reg-box and the Numbers deep-dive -- and the real-world defect is
    # one of them being updated while the others go stale. So every ceiling
    # figure the card states must agree, and they must all be 60.
    ceilings = set(re.findall(r"(?:not more than|maximum(?: of)?)\s*(\d+)",
                              card, re.I))
    report("solas_ii2_10_3_3_intact",
           bool(re.search(r"100% of the first ten", card, re.I))
           and bool(re.search(r"50% of the remainder", card, re.I))
           and ceilings == {"60"},
           "100/50 present, ceilings stated=%s" % (sorted(ceilings) or "none"))

    # ---- the leadership limb the correction had to preserve ---------------
    report("leadership_limb_preserved",
           bool(re.search(r"I own the standard", card, re.I))
           and bool(re.search(r"verify by sampling", card, re.I)),
           "delegation + accountability intact")

    # ---- nothing banned survives, on the card OR on the page --------------
    for name, pattern in BANNED_CARD:
        hit = re.search(pattern, card, re.I)
        report(name, hit is None,
               "clean" if not hit else "card still says: %r" % hit.group(0)[:60])
    for name, pattern in BANNED_PAGE:
        hit = re.search(pattern, page, re.I)
        report(name + "_page_wide", hit is None,
               "clean (cheat sheet included)" if not hit
               else "page still says: %r" % hit.group(0)[:60])

    print("\n%d checks, %d FAIL%s"
          % (CHECKS, len(FAILS),
             " (%s)" % ", ".join(sorted(set(FAILS))) if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
