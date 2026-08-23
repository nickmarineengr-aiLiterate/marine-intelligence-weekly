#!/usr/bin/env python3
"""
Content validator for CORR-CSM-BOILER-SURVEY-20260823.

WHY THIS EXISTS AND WHY THE DIGEST PIN IS NOT ENOUGH
----------------------------------------------------
`validate_corrections.py` answers "is this card still exactly the bytes that
were authorised?". That is necessary, and a different question from "is what
was authorised actually right?".

QB1_G#q40 listed "main boilers" among the Vital Auxiliary Systems assessed
under Continuous Machinery Survey, in an answer that also states every CSM
item is examined at least once in five years. A boiler is not on that clock.
IACS UR Z18 keeps the two apart in two sections with two intervals: §1.3
Continuous Surveys, item interval not to exceed five years; §2 Survey of Steam
Boilers, at least two internal examinations per five-year period with no two
more than 36 months apart, plus the §2.2 annual external survey. So the defect
was not a loose word - it stretched a 36-month internal examination interval
to five years.

A digest pin would have been perfectly happy with that text. It pins whatever
it is given. The substance is therefore asserted here, one named check per
proposition a future edit could quietly lose:

    the boiler is not presented as a CSM item
    the separate Boiler Survey is named
    the 36-month interval is stated
    boiler auxiliaries are still credited to the CMS list
    the removed PR 1C citation has not crept back
    UR Z18 is cited with the sections actually relied on
    the question text and anchor are untouched

Each check is named so `mutate_correction_csmboiler.py` can require that its
mutation trips THAT check, not merely the digest pin that fires on any edit.

NEGATIVE CHECKS RUN ON UNESCAPED TEXT
-------------------------------------
A guard spelled `h&m` is blind to `h&amp;m`. Every banned-phrase search below
runs against `html.unescape()` of the card, never the raw markup.

WHY "boiler" IS NOT BANNED OUTRIGHT
-----------------------------------
The corrected card says "boiler" more often than the defective one did: it now
names the boiler auxiliaries that ARE in the CMS list and states what the
Boiler Survey requires. A flat ban would fail on the sentences carrying the
fix. What is banned is the boiler appearing as a *listed CSM machinery item*,
which is a specific shape, checked as such.

    PYTHONIOENCODING=utf-8 python tools/oral/validate_correction_csmboiler.py
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

CORRECTION_ID = "CORR-CSM-BOILER-SURVEY-20260823"
MANIFEST = HERE / "correction_corr_csm_boiler_survey_20260823_manifest.json"
PAGE = "meoclass1/QB1_G.html"
FILE = "QB1_G.html"
ANCHOR = "q40"
Q_TEXT = "CSM (Condition Survey Method) survey"

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


# The exact defective shapes. Each is a way of putting the boiler back into
# the CSM machinery list, or of restoring the citation that did not support
# the claim it was attached to.
BANNED = [
    ("boiler_not_a_listed_csm_item", r"\bmain boilers\b"),
    ("boiler_not_a_listed_csm_item",
     r"Vital Auxiliary Systems\s*\([^)]*\bboilers\b[^)]*\)"),
    ("pr1c_citation_not_restored",   r"PR\s*1C"),
    ("pr1c_citation_not_restored",   r"continuous class verification"),
]

# The boiler may be named as a CSM item nowhere; but it must be named as a
# NON-item somewhere, and the auxiliaries must survive.
REQUIRED = [
    ("separate_boiler_survey_named",
     r"separate\b[^.]{0,40}\bBoiler Survey\b|\bBoiler Survey\b[^.]{0,60}\bnot\b"),
    ("boiler_excluded_from_csm_stated",
     r"\bnot\b[^.]{0,30}\bCSM items\b|\bNot the boiler itself\b"),
    ("boiler_survey_two_internals",
     r"\btwo internal examinations\b|\bminimum of two internal\b"),
    ("boiler_auxiliaries_still_in_list",
     r"forced-?draught fans|boiler burning pumps|feed water pumps"),
    ("urz18_cited", r"\bUR\s*Z18\b"),
    ("urz18_sections_cited", r"1\.3[^.]{0,80}Continuous Surveys"),
    ("csm_five_year_item_interval_kept", r"\bfive years\b|\b5 years\b|\b5-year\b"),
]


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
                if c.get("file") == FILE and c.get("anchor") == ANCHOR]
    report("card_declared_in_record", len(declared) == 1,
           "%d matching card record(s)" % len(declared))

    # The primary authority must be named, not implied. A correction whose
    # record does not say which instrument decided it cannot be re-checked by
    # anyone later, which is the whole reason the record is kept.
    # Asserted against the structured authority block, not the free prose.
    # Reading the prose alone lets the block be emptied while the narrative
    # still name-drops the instruments -- mutation G proved it. The block is
    # what a later reader re-checks the correction against, so the block is
    # what must carry the clauses.
    auth = record.get("authority", [])
    auth_json = json.dumps(auth, ensure_ascii=False)
    report("primary_authority_recorded",
           bool(auth) and "UR Z18" in auth_json and "36 months" in auth_json
           and "ClassNK" in auth_json,
           "entries=%d URZ18=%s 36mo=%s ClassNK=%s"
           % (len(auth), "UR Z18" in auth_json, "36 months" in auth_json,
              "ClassNK" in auth_json))

    report("authority_entries_cite_clauses",
           bool(auth) and all(a.get("clauses") for a in auth),
           "%d/%d entries carry clauses"
           % (sum(1 for a in auth if a.get("clauses")), len(auth)))

    report("candidate_verdict_recorded",
           record.get("candidate_verdict") in {"CORRECT", "PARTLY_CORRECT", "INCORRECT"},
           str(record.get("candidate_verdict")))

    # A correction that silently claimed a supersession chain it never built,
    # or skipped one it needed, is the failure this field exists to prevent.
    inv = record.get("invariants", {})
    report("supersession_position_stated",
           "supersession_required" in inv and bool(inv.get("supersession_rationale")),
           "required=%s" % inv.get("supersession_required"))

    # Every occurrence the scope sweep found must carry a disposition. A
    # propagation list that names files without saying what was decided about
    # them is a list of loose ends, not a scope record -- and the schema only
    # admits this field because this check reads it.
    prop = record.get("propagation", [])
    report("propagation_dispositioned",
           bool(prop) and all(p.get("classification") and p.get("action")
                              for p in prop),
           "%d entry/entries" % len(prop))

    # ---- the live card ---------------------------------------------------
    page = read_text(REPO / PAGE)
    text = card_text(page, ANCHOR)

    if declared:
        live = card_digests(page)[ANCHOR]
        report("card_digest_matches_manifest",
               live == declared[0].get("post_edit_digest"),
               "live=%s" % live[:16])

    report("question_text_unchanged", Q_TEXT in htmllib.unescape(page),
           "stem present")
    report("anchor_unchanged", '<div class="q-card" id="%s"' % ANCHOR in page,
           ANCHOR)

    # ---- the substance ---------------------------------------------------
    for name, pattern in BANNED:
        hits = re.findall(pattern, text, re.I)
        report(name, not hits, "%d hit(s): %s" % (len(hits), str(hits[:2])[:90]))

    for name, pattern in REQUIRED:
        m = re.search(pattern, text, re.I)
        report(name, bool(m), "MISSING" if m is None else "")

    # The 36-month figure has to be attached to the boiler survey. This card
    # separately says "maximum 36 months allowed between overhauling an item
    # and presenting it to the class surveyor", which is the CE credit window
    # and a completely different rule. A bare search for "36 months" is
    # therefore satisfied by text that says nothing about boilers at all --
    # mutation D proved it, by deleting the boiler interval and still passing.
    near = [m for m in re.finditer(r"\b36\s*months?\b", text, re.I)
            if re.search(r"internal examination|boiler",
                         text[max(0, m.start() - 200):m.start()], re.I)]
    report("boiler_survey_36_month_interval", bool(near),
           "MISSING in boiler context" if not near else "")

    # The correction must not have quietly deleted the auxiliaries it moved
    # the boiler's place to, nor the rest of the verified machinery list.
    for item in ("air compressors", "steering gear pumps",
                 "emergency fire pumps", "heat exchangers"):
        report("machinery_list_intact:%s" % item.split()[0],
               item.lower() in text.lower(), item)

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    if FAILS:
        print("failing: " + ", ".join(sorted(set(FAILS))))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
