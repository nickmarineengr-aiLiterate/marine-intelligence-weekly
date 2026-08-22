#!/usr/bin/env python3
"""
Content validator for CORR-LSA-LIFEBOAT-VENTILATION-20260822.

WHY THIS EXISTS AND WHY THE DIGEST PIN IS NOT ENOUGH
----------------------------------------------------
`validate_corrections.py` answers "is this card still exactly the bytes that
were authorised?". That is a necessary check, and a completely different
question from "is what was authorised actually right?".

The defect this record corrects was not a typo. QB2_F#q6 reduced the
MSC.535(107) expression *installed on or after 1 January 2029* to a
newbuilding contract / keel-laying test and concluded "new-build application
only, not retrofit". The resolution defines that expression itself, in two
limbs, and the second one reaches existing ships by the equipment's delivery
date. Keeping only limb (a) did not blur the rule, it inverted it for the
whole in-service fleet.

A digest pin would have been perfectly happy with the wrong text. It pins
whatever it is given. So the substance is asserted here, as named checks, one
per proposition a future edit could quietly lose:

    the application year is 2029, not the entry-into-force year 2026
    both limbs of the definition are stated
    no "new-build only" claim survives anywhere on the card
    no keel-laying application test survives
    entry into force and application are stated as different things
    the verified technical capsule is still present

Each check is named so `mutate_correction_lsavent.py` can require that its
mutation trips THAT check, and not merely the digest pin that fires on any
edit at all.

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
from validate_batch_b import card_digests              # noqa: E402

CORRECTION_ID = "CORR-LSA-LIFEBOAT-VENTILATION-20260822"
MANIFEST = HERE / "correction_corr_lsa_lifeboat_ventilation_20260822_manifest.json"
PAGE = "meoclass1/QB2_F.html"
ANCHOR = "q6"
Q_TEXT = "What are the ventilation requirements for a totally enclosed lifeboat?"

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-42s %s" % ("PASS" if ok else "FAIL", check, detail))


def card_text(page_text: str, anchor: str) -> str:
    """The one card, unescaped, tags stripped to plain prose."""
    start = page_text.find('<div class="q-card" id="%s"' % anchor)
    assert start >= 0, "card not found: %s" % anchor
    nxt = page_text.find('<div class="q-card"', start + 10)
    raw = page_text[start:nxt if nxt > 0 else len(page_text)]
    flat = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", htmllib.unescape(flat))


# Formulations that must not reappear, in any form. Each is the actual
# wording the card carried before the correction.
#
# Note what is NOT banned outright: the bare phrase "new-build only". The
# corrected card says it repeatedly -- "it is not new-build only", "do not
# answer 'new-builds only'" -- because a correction that teaches the reader
# which formulation is wrong has to quote the wrong formulation. This is the
# same reason the trap register marks this entry GREP: SKIP. A flat ban would
# fail on the very sentences that carry the fix, so the assertion is instead
# that every occurrence is NEGATED (see `newbuild_only_always_negated`).
BANNED = [
    ("newbuild_only_claim",         r"new-?build application only"),
    ("newbuild_only_claim",         r"next-generation newbuild"),
    ("keel_laid_application_test",  r"contracted\s*/\s*keel-?laid"),
    ("keel_laid_application_test",  r"keel laid, if no contract"),
    ("keel_laid_application_test",  r"keel-?laid on or after"),
    ("application_in_2026",         r"installed on or after 1 January 2026"),
    ("application_in_2026",         r"installed on/after 1 Jan 2026"),
]

# A "new-build only" mention is acceptable in exactly two shapes: it is
# quoted, i.e. cited as the formulation being rejected; or a denial / past-
# defect marker precedes it in the same passage. Anything else is the card
# asserting the wrong rule again.
#
# The lookback is deliberately generous (240 chars). The tightest real case is
#   Reducing "installed on or after 1 January 2029" to "keel laid after 2029"
#   or "new-builds only"
# where the denial sits behind two full quoted phrases. A short window would
# have reported that sentence -- the one doing the teaching -- as the defect.
NEGATORS = re.compile(
    r"(?:\bnot\b|\bnever\b|\bno longer\b|\bdo not\b|\bdon't\b|\brather than\b|"
    r"\bwrong\b|\breduc(?:e|ed|es|ing)\b|\bpreviously\b|\bdescrib(?:e|ed)\b|"
    r"\bcalled\b|\bstop\b|\binstead of\b)", re.I)

_QUOTES = '"“”‘’\''


def newbuild_only_mentions(text: str) -> tuple[list[str], list[str]]:
    """Split every 'new-build only' mention into (acceptable, asserted)."""
    ok, asserted = [], []
    for m in re.finditer(r"new-?builds? only", text, re.I):
        before = text[max(0, m.start() - 240):m.start()]
        after = text[m.end():m.end() + 8]
        quoted = (before[-1:] in _QUOTES and after[:1] in _QUOTES)
        if quoted or NEGATORS.search(before) or after.lstrip().startswith(", no"):
            ok.append(m.group(0))
        else:
            asserted.append(before[-52:].strip() + " >>" + m.group(0))
    return ok, asserted


def main() -> int:
    print("correction content validator: %s" % CORRECTION_ID)

    # ---- the record ------------------------------------------------------
    if not MANIFEST.is_file():
        report("correction_record_present", False, "missing %s" % MANIFEST.name)
        print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
        return 1
    record = json.loads(read_text(MANIFEST))
    report("correction_record_present", True, MANIFEST.name)

    report("correction_record_authorised",
           record.get("status") == "AUTHORISED"
           and record.get("correction_id") == CORRECTION_ID,
           "status=%s id=%s" % (record.get("status"), record.get("correction_id")))

    declared = [c for c in record.get("cards", [])
                if c.get("file") == "QB2_F.html" and c.get("anchor") == ANCHOR]
    report("card_declared_in_record", len(declared) == 1,
           "%d matching card record(s)" % len(declared))

    # The primary authority must be named, not implied. A correction whose
    # record does not say which instrument decided it cannot be re-checked by
    # anyone later, which is the whole reason the record is kept.
    prose = " ".join(str(record.get(k, "")) for k in ("rationale", "note", "title"))
    report("primary_authority_recorded",
           "MSC.535(107)" in prose and "8 June 2023" in prose,
           "MSC.535(107)=%s adoption=%s"
           % ("MSC.535(107)" in prose, "8 June 2023" in prose))

    # ---- the live card ---------------------------------------------------
    page = read_text(REPO / PAGE)
    text = card_text(page, ANCHOR)

    if declared:
        live = card_digests(page)[ANCHOR]
        report("card_digest_matches_manifest",
               live == declared[0].get("post_edit_digest"),
               "live=%s" % live[:16])

    report("question_text_unchanged", Q_TEXT in htmllib.unescape(page),
           "canonical q-text present")

    ids = re.findall(r'<div class="q-card" id="([^"]+)"', page)
    report("card_order_unchanged", ids == ["q1", "q2", "q3", "q4", "q5", "q6"],
           "ids=%s" % ids)

    # ---- the substance ---------------------------------------------------
    report("application_year_is_2029",
           "installed on or after 1 January 2029" in text and "1 Jan 2029" in text,
           "the resolution's own expression is present")

    # Limb (a): contract placed, or absent a contract CONSTRUCTED. The
    # resolution does not say "keel laid" and the card must not either.
    limb_a = ("building contract is placed" in text
              and re.search(r"absence of a contract\b[^.]{0,40}?\bconstructed\b",
                            text) is not None)
    report("definition_limb_a_present", bool(limb_a),
           "contract-placed + constructed wording")

    # Limb (b) is the limb that was missing, and losing it is what inverted
    # the rule for existing ships.
    limb_b = ("contractual delivery date for the equipment" in text
              and "actual delivery date of the equipment to the ship" in text
              and "All other ships" in text)
    report("definition_limb_b_present", bool(limb_b),
           "equipment contractual + actual delivery date, for all other ships")

    report("existing_ships_reached",
           "not a new-build-only requirement" in text
           and re.search(r"in-service|existing ship", text) is not None,
           "card states limb (b) reaches existing tonnage")

    report("no_retrofit_obligation_stated",
           "retrofit of lifeboats already installed" in text,
           "the true, narrower claim is stated")

    # Entry into force and application must be visibly different things.
    report("force_and_application_distinguished",
           "1 January 2026" in text and "1 January 2029" in text
           and "Entry into force is not the application date" in text,
           "both dates + explicit separation sentence")

    report("adoption_date_present", "8 June 2023" in text, "adopted 8 June 2023")

    # ---- verified technical capsule still intact -------------------------
    capsule = {
        "5 m3/h rate": r"5 m(?:³|3)/h per person",
        "24 hours": r"24 hours",
        "para 4.6.6": r"4\.6\.6",
        "para 4.6.7": r"4\.6\.7",
        "fuel 4.4.6.8": r"4\.4\.6\.8",
        "MSC.81(70)": r"MSC\.81\(70\)",
        "MSC.559(108)": r"MSC\.559\(108\)",
        "MSC.402(96)": r"MSC\.402\(96\)",
    }
    missing = [k for k, rx in capsule.items() if not re.search(rx, text)]
    report("technical_capsule_intact", not missing, "missing=%s" % (missing or "none"))

    # ---- banned formulations --------------------------------------------
    hits: dict[str, list[str]] = {}
    for check, rx in BANNED:
        for m in re.finditer(rx, text, re.I):
            hits.setdefault(check, []).append(m.group(0))
    for check in sorted({c for c, _ in BANNED}):
        report("no_" + check, check not in hits,
               "hits=%s" % (hits.get(check) or "none"))

    negated, asserted = newbuild_only_mentions(text)
    report("newbuild_only_always_negated", not asserted,
           "%d negated, asserted=%s" % (len(negated), asserted or "none"))

    # ---- historical ownership -------------------------------------------
    #
    # This card is pinned by NO production batch, so this correction needs no
    # supersession chain. That is a fact about today's manifests, not a
    # permanent property of the corpus: if it ever stops being true, the
    # correction must grow a chain rather than silently overwrite a batch's
    # release evidence. So it is asserted, never assumed.
    pinning = [path.name for path in sorted(HERE.glob("batch_*_manifest.json"))
               if "QB2_F" in read_text(path)]
    report("no_batch_pins_this_card", not pinning,
           "pinning=%s -- none, so no supersession chain is required"
           % (pinning or "none"))

    # ---- derived surfaces -----------------------------------------------
    index = json.loads(read_text(REPO / "meoclass1/qb_content_index.json"))
    report("canonical_totals_unchanged",
           index.get("total_questions") == 721 and index.get("total_files") == 86,
           "questions=%s files=%s"
           % (index.get("total_questions"), index.get("total_files")))

    entry = index["files"]["QB2_F.html"]
    corr_blob = " ".join(entry.get("corrections_applied") or [])
    # The original QB2_F build row described the card's own content and ended
    # "application date 1 Jan 2029 (new-build only)". That clause is a claim
    # about the live card, not a historical note, so it had to go with the
    # card. The row may still discuss the wrong formulation -- but only in the
    # negated sense the card itself uses.
    _, stale = newbuild_only_mentions(corr_blob)
    report("content_index_records_correction",
           "two limbs" in corr_blob
           and "(new-build only)" not in corr_blob and not stale,
           "governed row describes the corrected rule; stale claims=%s"
           % (stale or "none"))

    print("\n%d checks, %d FAIL%s"
          % (CHECKS, len(FAILS), " (%s)" % ", ".join(FAILS) if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
