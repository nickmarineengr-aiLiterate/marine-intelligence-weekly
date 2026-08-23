"""The card/ledger examiner divergence gate.

The invariant
-------------
Every QB question card that renders a non-empty examiner attribution must
satisfy exactly one of:

  A. a published relationship exists for that (question, examiner) pair, or
  B. the pair is explicitly governed in CARD_EXAMINER_RECONCILIATION.json as
     held, conflicted or unsupported, with a recorded reason.

Anything else is silent divergence: a candidate reads an examiner name off a
card that the examiner intelligence does not know about.

The invariant is one-directional on purpose. A published relationship need not
render inline -- most do not, and requiring it would force an editorial change
onto every card in the corpus. Only the card-to-evidence direction is gated.

What "published" means
----------------------
Not CURRENT_EXAMINER_RELATIONSHIPS.jsonl. That file is one of four inputs
build_examiner_index.py upserts into the published universe, alongside card
data-examiner attributes, RELEASE_A_PUBLICATION.json and the CE-tip review
decisions. Fourteen of the twenty-one attributions this gate covers are
published through Release A and have no ledger row at all. Gating on the
ledger alone would report them as divergent and invite duplicate rows, so the
gate reads EXAMINER_INDEX_SNAPSHOT.json -- the resolved snapshot both
candidate pages are rendered from, which build_examiner_index.py --check
proves is byte-current.

Failures this gate is built to catch
------------------------------------
  * a card renders an attribution with no published relationship and no hold;
  * a card renders one examiner while the published relationship names another;
  * a pair carries more than one published row, inflating examiner counts;
  * a card names someone the alias register does not know;
  * a relationship is removed while the card that displays it stays.

    PYTHONIOENCODING=utf-8 python tools/oral/validate_card_examiner_divergence.py

Exit 0 clean, 1 on any divergence.
"""
from __future__ import annotations

import collections
import json
import re
import sys

import oral_lib as L

OUT = L.OUT
RECORD = "CARD_EXAMINER_RECONCILIATION.json"
SNAPSHOT = "EXAMINER_INDEX_SNAPSHOT.json"

# The one in-card construct that asserts an examiner identity. Trap-question
# speaker labels, CE-tip prose and meta descriptions are deliberately not this.
CARD_TAG = re.compile(r'examiner-tag[^>]*>\s*Examiner:\s*([^<]*)<')
ANCHOR = re.compile(r'id="(q\d+)"')

# Decisions that are a governed answer to "why is this not a relationship?"
GOVERNED_ABSENCE = {"HOLD_PROVENANCE", "CONFLICT_REQUIRES_REVIEW",
                    "DISPLAY_LINE_UNSUPPORTED"}
REASON_FIELDS = ("hold_reason", "conflict", "unsupported_reason", "why_not_removed")

FAILS = []
CHECKS = [0]


def check(label, ok, detail=""):
    CHECKS[0] += 1
    print("%-4s %s %s" % ("PASS" if ok else "FAIL", label, detail if not ok else ""))
    if not ok:
        FAILS.append(label)


def card_attributions():
    """(question_id, file, anchor, raw string) for every rendered examiner-tag."""
    out = []
    for p in L.qb_files():
        src = p.read_text(encoding="utf-8", errors="replace")
        for m in CARD_TAG.finditer(src):
            ids = ANCHOR.findall(src[:m.start()])
            out.append((p.stem + "#" + (ids[-1] if ids else "?"),
                        p.name, ids[-1] if ids else "?", m.group(1).strip()))
    return out


def main():
    snap = json.loads((OUT / SNAPSHOT).read_text(encoding="utf-8"))
    record = json.loads((OUT / RECORD).read_text(encoding="utf-8"))
    alias = json.loads((OUT / "EXAMINER_ALIAS_REGISTER.json").read_text(encoding="utf-8"))

    forms = {}
    for e in alias["examiners"]:
        for f in e["observed_forms"] + [e["canonical_name"]]:
            forms[f.strip().lower()] = e["canonical_name"]
    non_examiner = {n["raw"].strip().lower() for n in alias["non_examiner_attributions"]}

    published = collections.defaultdict(list)
    for r in snap["rows"]:
        published[(r["canonical_question_id"], r["examiner"])].append(r)
    by_question = collections.defaultdict(set)
    for qid, ex in published:
        by_question[qid].add(ex)

    governed = {}
    for d in record["decisions"]:
        if d.get("question_id") and d.get("decision") in GOVERNED_ABSENCE:
            governed[(d["question_id"], d.get("raw_examiner_string", "").strip())] = d

    cards = card_attributions()
    print("card/ledger examiner divergence gate")
    print("  %d rendered in-card attributions, %d published relationships"
          % (len(cards), len(snap["rows"])))

    # --- the display line must actually say something -----------------------
    empty = [q for q, _f, _a, raw in cards if not raw]
    check("no card renders an empty examiner attribution", not empty, str(empty[:5]))

    # --- identity: every raw string must resolve ----------------------------
    unknown = [(q, raw) for q, _f, _a, raw in cards
               if raw and raw.lower() not in forms and raw.lower() not in non_examiner]
    check("every in-card examiner string resolves in the alias register",
          not unknown, str(unknown[:5]))

    # --- the anchor the attribution hangs on must be real -------------------
    anchors = L.all_anchors()
    stray = [q for q, f, a, _r in cards if a not in anchors.get(f, set())]
    check("every in-card attribution sits on a real question anchor",
          not stray, str(stray[:5]))

    # --- A or B --------------------------------------------------------------
    divergent, mismatched, ungoverned = [], [], []
    for qid, _f, _a, raw in cards:
        if not raw:
            continue
        canon = forms.get(raw.lower())
        if canon is None:
            continue                      # a non-attribution, or already failed above
        if (qid, canon) in published:
            continue                      # A
        d = governed.get((qid, raw))
        if d is None:
            divergent.append((qid, raw))  # neither A nor B
            continue
        if not any(d.get(f) for f in REASON_FIELDS):
            ungoverned.append((qid, raw))
        # A card held for one examiner while the published evidence names a
        # different one is a contradiction the hold does not excuse.
        others = by_question.get(qid, set())
        if others and canon not in others:
            mismatched.append((qid, raw, sorted(others)))

    check("every in-card attribution is published or explicitly governed",
          not divergent, str(divergent[:5]))
    check("every governed absence records a reason", not ungoverned, str(ungoverned[:5]))
    check("no card names an examiner the published evidence contradicts",
          not mismatched, str(mismatched[:5]))

    # --- duplicate inflation -------------------------------------------------
    dup = [k for k, v in published.items() if len(v) > 1]
    check("no published pair carries duplicate relationship rows", not dup, str(dup[:5]))

    # --- the record must stay in step with the pages ------------------------
    live = {(q, raw) for q, _f, _a, raw in cards}
    stale = [(d["question_id"], d.get("raw_examiner_string"))
             for d in record["decisions"] if d.get("question_id")
             and (d["question_id"], d.get("raw_examiner_string", "").strip()) not in live]
    check("every adjudicated attribution is still rendered on its card",
          not stale, str(stale[:5]))

    counted = sum(1 for d in record["decisions"] if d.get("question_id"))
    check("the record adjudicates every rendered attribution",
          counted == len([c for c in cards if c[3]]),
          "record %d, rendered %d" % (counted, len([c for c in cards if c[3]])))

    print()
    print("%d PASS / %d FAIL" % (CHECKS[0] - len(FAILS), len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
