"""Validate the GAP-0609 bounded exception review.

GAP-0609 was the one family the final enrichment consolidation could not
dispose of: its authorised enrichment target did not own the topic, so it was
parked as NEW_CARD_REVIEW_REQUIRED. This validator asserts that the exception
review closed it, and that whichever way it closed is actually true of the
live corpus.

Governing principle: the live QB HTML is the truth. Every claim in the review
record is checked against a fresh derivation, never against another record.

  PYTHONIOENCODING=utf-8 python tools/oral/validate_gap0609_exception.py [--review PATH]

Exit 0 all checks pass, 1 one or more failed.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import sys
import pathlib

# Windows encodes a child process's stdout with the locale codec, so printing a
# single non-cp1252 character -- U+26A0, which this toolchain reports and
# deliberately injects -- kills the process. When that happens between applying
# a mutation and restoring it, a mutated product page is left on disk. This tool
# reaches no other shared module, so the contract is imported explicitly.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from oral_bytes import enable_utf8_stdio      # noqa: E402

enable_utf8_stdio()


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REVIEW = os.path.join(ROOT, "meoclass1", "oral-intelligence", "examiner-audit",
                      "GAP0609_EXCEPTION_REVIEW.json")
INDEX = os.path.join(ROOT, "meoclass1", "qb_content_index.json")

TERMINAL = {"NEW_CANONICAL_QA", "ENRICH_EXISTING_QB", "FOLLOWUP_ONLY",
            "ALREADY_COVERED", "RETARGET_EXISTING_QB", "HOLD_AMBIGUOUS"}
EXISTING = {"ENRICH_EXISTING_QB", "FOLLOWUP_ONLY", "ALREADY_COVERED",
            "RETARGET_EXISTING_QB"}

# Production vocabulary that must never reach a candidate-facing q-card.
PRODUCTION_MARKERS = [
    r"GAP-\d{4}", r"ENR-\d{3}", r"ASF-\d{4}", r"ASC-\d{4}",
    r"NEW_CARD_REVIEW_REQUIRED", r"laptop_decision", r"laptop_review_status",
    r"recurrence_class", r"production_action", r"\bCORRECTED:",
]


def q_cards(html):
    """Balanced div extraction of every .q-card, keyed by anchor."""
    out = {}
    tag = re.compile(r"<(/?)div\b[^>]*>")
    for m in re.finditer(r'<div[^>]*class="[^"]*\bq-card\b[^"]*"[^>]*>', html):
        i, depth = m.end(), 1
        while depth > 0:
            t = tag.search(html, i)
            if not t:
                break
            depth += -1 if t.group(1) else 1
            i = t.end()
        raw = html[m.start():i]
        a = re.search(r'id="(q[\w]*)"', raw)
        if a:
            out.setdefault(a.group(1), []).append(raw)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--review", default=REVIEW)
    ap.add_argument("--index", default=INDEX)
    args = ap.parse_args()

    fails, checks = [], 0

    def ck(cond, msg):
        nonlocal checks
        checks += 1
        if not cond:
            fails.append(msg)

    if not os.path.exists(args.review):
        print("FAIL  no exception review record at %s" % args.review)
        return 1
    rv = json.load(io.open(args.review, encoding="utf-8"))
    idx = json.load(io.open(args.index, encoding="utf-8"))

    # ---- 1. the family is accounted for exactly once, and is resolved -------
    blob = json.dumps(rv)
    ck(blob.count('"family_id": "GAP-0609"') == 1,
       "GAP-0609 must appear exactly once as a family_id in the review record")
    disp = rv.get("final_disposition")
    ck(disp in TERMINAL, "final_disposition %r is not a terminal disposition" % disp)
    ck(disp != "NEW_CARD_REVIEW_REQUIRED",
       "final_disposition is still NEW_CARD_REVIEW_REQUIRED - the family is unresolved")

    # ---- 2. reasoning must be present and non-trivial ----------------------
    lrt = rv.get("last_resort_test") or {}
    for k in ("A_materially_answered_by_one_card", "B_absorbable_as_bounded_enrichment",
              "C_followup_only", "D_notes_support_existing_card_promotion",
              "E_ask_too_broad_or_ambiguous"):
        ck(str(lrt.get(k, "")).strip() != "", "last_resort_test.%s is blank" % k)
    ck(len(str(rv.get("target_selection_reason", "")).strip()) >= 40,
       "target_selection_reason is blank or too short to be a reason")
    ck(len(str((rv.get("independent_verification") or {})
               .get("authorised_target_check", {}).get("detail", "")).strip()) >= 40,
       "independent verification of the authorised target is blank")

    # ---- 3. baseline arithmetic -------------------------------------------
    bl = rv.get("baseline") or {}
    before, after = bl.get("canonical_questions_before"), bl.get("canonical_questions_after")
    live_total = sum(len(r.get("questions", [])) for r in idx["files"].values())
    ck(live_total == after,
       "recorded canonical_questions_after %r != live derivation %d" % (after, live_total))
    expect = (before or 0) + (1 if disp == "NEW_CANONICAL_QA" else 0)
    ck(after == expect,
       "canonical count %r is wrong for disposition %s - expected %d" % (after, disp, expect))

    # ---- 4. no duplicate anchors anywhere ---------------------------------
    anchors = [f + "#" + q["anchor"] for f, r in idx["files"].items()
               for q in r.get("questions", [])]
    ck(len(anchors) == len(set(anchors)), "duplicate file#anchor in the canonical index")

    tgt = rv.get("target") or ""
    if disp == "NEW_CANONICAL_QA":
        nc = rv.get("new_card") or {}
        ck(nc.get("file_anchor") == tgt, "new_card.file_anchor does not match target")
        fname, _, anc = tgt.partition("#")
        ck(bool(fname) and bool(anc), "target %r is not a file#anchor" % tgt)

        # ---- 5. the card must actually exist and resolve ------------------
        path = os.path.join(ROOT, "meoclass1", fname)
        ck(os.path.exists(path), "destination file %s does not exist" % fname)
        if os.path.exists(path):
            html = io.open(path, encoding="utf-8").read()
            cards = q_cards(html)
            ck(anc in cards, "anchor #%s does not resolve to a q-card in %s" % (anc, fname))
            ck(len(cards.get(anc, [])) == 1,
               "anchor #%s is duplicated in %s" % (anc, fname))
            if cards.get(anc):
                raw = cards[anc][0]
                qt = re.search(r'class="q-text"[^>]*>(.*?)</div>', raw, re.S)
                ck(qt is not None and re.sub(r"<[^>]+>", "", qt.group(1)).strip() != "",
                   "new card q-text is empty")
                ans = re.search(r'class="answer-body"[^>]*>(.*)', raw, re.S)
                ck(ans is not None and len(re.sub(r"<[^>]+>", "", ans.group(1)).strip()) > 400,
                   "new card answer body is empty or too thin to be an answer")
                # ---- 6. no production metadata in candidate text ---------
                for pat in PRODUCTION_MARKERS:
                    m = re.search(pat, raw)
                    ck(m is None, "production marker %r leaked into the live card" % (
                        m.group(0) if m else pat))

        # ---- 7. the index must know about it -----------------------------
        rec = idx["files"].get(fname, {})
        ck(any(q["anchor"] == anc for q in rec.get("questions", [])),
           "%s is not present in the canonical index" % tgt)

        # ---- 8. authority must be recorded -------------------------------
        auth = rv.get("authority_scope") or []
        ck(len(auth) >= 3, "authority_scope must record at least three instruments")
        ck(all(str(a.get("instrument", "")).strip() and str(a.get("basis", "")).strip()
               for a in auth), "an authority_scope entry has no instrument or no basis")

        # ---- 8b. pre-existing cards in the destination must be untouched --
        ped = rv.get("pre_existing_card_digests") or {}
        digests = ped.get("digests") or {}
        ck(bool(digests), "no pre-existing card digest baseline recorded for the destination")
        if digests:
            dpath = os.path.join(ROOT, ped.get("file", ""))
            ck(os.path.exists(dpath), "digest baseline names a file that does not exist")
            if os.path.exists(dpath):
                live = q_cards(io.open(dpath, encoding="utf-8").read())
                for a, want in digests.items():
                    raws = live.get(a) or []
                    ck(len(raws) == 1,
                       "pre-existing card #%s is missing or duplicated" % a)
                    if len(raws) == 1:
                        got = hashlib.sha256(
                            raws[0].replace("\r\n", "\n").encode("utf-8")).hexdigest()
                        ck(got == want,
                           "pre-existing card #%s was altered by this change" % a)

    elif disp in EXISTING:
        # ---- 9. an existing-target decision must resolve ------------------
        ck(bool(tgt), "an existing-card disposition must name a target")
        fname, _, anc = tgt.partition("#")
        rec = idx["files"].get(fname)
        ck(rec is not None, "target file %s is not in the canonical index" % fname)
        if rec is not None:
            ck(any(q["anchor"] == anc for q in rec.get("questions", [])),
               "target %s does not resolve to a canonical question" % tgt)
        ck(len(str(rv.get("coverage_reason", rv.get("target_selection_reason", ""))).strip()) >= 40,
           "an existing-card disposition must record a coverage or enrichment reason")
        ck(after == before,
           "canonical count moved on a non-new disposition")

    print("GAP-0609 exception validator: %d checks, %d failed" % (checks, len(fails)))
    for f in fails:
        print("  FAIL  " + f)
    if not fails:
        print("  disposition=%s target=%s canonical=%d" % (disp, tgt, live_total))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
