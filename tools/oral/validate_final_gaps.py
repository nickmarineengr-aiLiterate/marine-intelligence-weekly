"""Validate FINAL_REMAINING_ORAL_PRODUCTION_DECISIONS.json.

Every check fails closed. A check that cannot obtain its evidence reports
`unavailable` and fails; it never passes by absence. The load-bearing checks are
the ones that stop the headline count from being inflated:

  * an ambiguous family must never be counted as a new card
  * a completed P0 family must never be re-proposed as new work
  * a new card must not have an enrichment target sitting in front of it
  * a Notes-complete family must not be called NEW without a stated reason
  * the headline numbers must equal the dataset they claim to summarise

Exit 0 = all pass, 1 = at least one failure.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402
import oral_text as T  # noqa: E402
import adjudicate_final_gaps as A  # noqa: E402

DATA = L.OUT / "FINAL_REMAINING_ORAL_PRODUCTION_DECISIONS.json"
NEW = "NEW_CANONICAL_QA"
ENRICH = "ENRICH_EXISTING_QB"
NOTES = "NOTES_TO_QB_PROMOTION"
MERGE = "MERGE_WITH_EXISTING_FAMILY"
AMBIG = "HUMAN_REVIEW_REQUIRED"
COVERED = "ALREADY_COVERED"
FOLLOWUP = "FOLLOWUP_ONLY"
HIGH = "READY_HIGH_CONFIDENCE"

ANCHOR = re.compile(r"^QB[\w]*#q\d+$")
QBFILE = re.compile(r"^QB[\w]*$")

ASK_FORM = re.compile(
    r"\?|\b(what|why|how|when|where|which|who|whose|explain|describe|state|"
    r"define|compare|differen\w*|list|outline|discuss)\b", re.I)


def _is_formed_ask(text):
    """True when the prompt is phrased as a question or an instruction.

    This is what separates a short ask from a bare label. It reads the ORIGINAL
    text, not the token set: the interrogatives are all stopwords, so by the
    time a prompt has been tokenised the evidence has already been thrown away.
    """
    return bool(ASK_FORM.search(str(text or "")))


results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def main():
    if not DATA.exists():
        check("dataset present", False, "unavailable: %s not generated" % DATA.name)
        return report()
    p = json.loads(DATA.read_text(encoding="utf-8"))
    fams = p["families"]
    h = p["headline"]

    live_ids = {r["canonical_question_id"] for r in L.build_inventory()}
    live_files = {q.split("#")[0] for q in live_ids}
    check("live corpus readable", bool(live_ids),
          "unavailable: no live questions parsed" if not live_ids else
          "%d questions" % len(live_ids))

    # C1 every remaining family accounted for, exactly once
    src = json.loads((L.OUT / "FINAL_ORAL_GAP_CANDIDATES.json").read_text(encoding="utf-8"))
    expect = {g["gap_id"] for g in src["gaps"]} - set(A.P0_FAMILIES) - set(A.P0_MERGED)
    got = [f["family_id"] for f in fams]
    check("C1 every remaining family accounted for",
          set(got) == expect and len(got) == len(set(got)),
          "expected %d got %d, dupes %d" % (
              len(expect), len(got), len(got) - len(set(got))))

    # C2 exactly one primary disposition, from the governed vocabulary
    vocab = {NEW, ENRICH, NOTES, FOLLOWUP, MERGE, COVERED, "RELATIONSHIP_ONLY",
             AMBIG, "DEFER_LOW_VALUE", "NOT_A_GAP"}
    bad = [f["family_id"] for f in fams if f["decision"] not in vocab]
    check("C2 one disposition from the governed vocabulary", not bad, str(bad[:5]))

    # C3 no generic MISSING left as an instruction
    check("C3 no MISSING left as a production instruction",
          not [f for f in fams if f["decision"] == "MISSING"], "")

    # C4 no duplicate production id
    pids = [f["production_id"] for f in fams if f["decision"] == NEW]
    check("C4 no duplicate production id",
          len(pids) == len(set(pids)), "%d ids" % len(pids))

    # C5 every enrichment target resolves to a live anchor
    bad = [(f["family_id"], f["decision_target"]) for f in fams
           if f["decision"] == ENRICH
           and (not f["decision_target"] or f["decision_target"] not in live_ids)]
    check("C5 every enrichment target resolves live", not bad, str(bad[:5]))

    # C6 every ALREADY_COVERED / FOLLOWUP target resolves to a live anchor
    bad = [(f["family_id"], f["decision_target"]) for f in fams
           if f["decision"] in (COVERED, FOLLOWUP)
           and (not f["decision_target"] or f["decision_target"] not in live_ids)]
    check("C6 every covered/follow-up target resolves live", not bad, str(bad[:5]))

    # C7 every Notes source resolves to a real Notes file
    notes_dir = L.MEO / "oralnotes"
    bad = []
    for f in fams:
        if f["decision"] != NOTES:
            continue
        t = f["decision_target"] or ""
        fn = t.split("#")[0]
        if "#" not in t or not (notes_dir / fn).exists():
            bad.append((f["family_id"], t))
    check("C7 every Notes promotion source resolves", not bad, str(bad[:5]))

    # C8 every proposed new card carries source evidence
    bad = [f["family_id"] for f in fams
           if f["decision"] == NEW and not f["source_ids"]]
    check("C8 every new card carries source occurrence ids", not bad, str(bad[:5]))

    # C9 every source occurrence id exists in the 788 disposition
    known = set()
    with (L.OUT / "FINAL_788_PRODUCTION_DISPOSITION.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            known.add(json.loads(line)["source_id"])
    bad = [(f["family_id"], s) for f in fams for s in f["source_ids"]
           if s not in known]
    check("C9 every source occurrence id is known", not bad, str(bad[:5]))

    # C10 no completed P0 family reintroduced
    bad = [f["family_id"] for f in fams
           if f["family_id"] in A.P0_FAMILIES or f["family_id"] in A.P0_MERGED]
    check("C10 no completed P0 family reintroduced", not bad, str(bad[:5]))

    # C11 an unresolved item is never counted as a definite NEW
    bad = [f["family_id"] for f in fams
           if f["decision"] == NEW and f.get("confidence") not in
           (HIGH, "REVIEW_MEDIUM_CONFIDENCE")]
    amb_new = [f["family_id"] for f in fams
               if f["decision"] == AMBIG and f.get("production_id")]
    check("C11 no ambiguous family counted as NEW", not bad and not amb_new,
          str((bad + amb_new)[:5]))

    # C12 a NEW card must not have a live enrichment home in front of it
    bad = [(f["family_id"], f["current_best_answer_question_id"],
            f["current_best_answer_coverage"]) for f in fams
           if f["decision"] == NEW and f["current_best_answer_coverage"] >= 0.75
           and "enrich" not in f["decision_reason"].lower()
           and "adjacent" not in f["decision_reason"].lower()]
    check("C12 no NEW card with an unexplained enrichment home", not bad,
          str(bad[:5]))

    # C13 a Notes-complete family is not called NEW without a stated reason
    bad = [f["family_id"] for f in fams
           if f["decision"] == NEW
           and f["notes_support"] in ("NOTES_COMPLETE_SUPPORT",
                                      "NOTES_STRONG_SUPPORT")
           and "notes" not in f["decision_reason"].lower()]
    check("C13 no Notes-complete family called NEW unjustified", not bad,
          str(bad[:5]))

    # C14 every merge target is a family in this dataset or a completed P0 one
    ids = {f["family_id"] for f in fams}
    bad = [(f["family_id"], f["decision_target"]) for f in fams
           if f["decision"] == MERGE
           and f["decision_target"] not in ids | set(A.P0_FAMILIES)]
    check("C14 every merge target resolves", not bad, str(bad[:5]))

    # C15 a merge target must not itself be a merge (no chains)
    merged = {f["family_id"] for f in fams if f["decision"] == MERGE}
    bad = [f["family_id"] for f in fams
           if f["decision"] == MERGE and f["decision_target"] in merged]
    check("C15 no merge chains", not bad, str(bad[:5]))

    # C16 recommended QB home for a new card is a live QB file
    bad = [(f["family_id"], f["recommended_qb_file"]) for f in fams
           if f["decision"] == NEW and f["recommended_qb_file"] not in live_files]
    check("C16 every new-card QB home is a live file", not bad, str(bad[:5]))

    # C17 headline counts equal the dataset
    high = [f for f in fams if f["decision"] == NEW and f["confidence"] == HIGH]
    med = [f for f in fams if f["decision"] == NEW and f["confidence"] != HIGH]
    by = Counter(f["decision"] for f in fams)
    agree = (h["ADDITIONAL_NEW_CANONICAL_QA_COUNT"] == len(high)
             and h["ADDITIONAL_NEW_MEDIUM_CONFIDENCE_NOT_COUNTED"] == len(med)
             and h["ADDITIONAL_ENRICH_EXISTING_COUNT"] == by[ENRICH]
             and h["ADDITIONAL_NOTES_TO_QB_PROMOTION_COUNT"] == by[NOTES]
             and h["FOLLOWUP_ONLY_COUNT"] == by[FOLLOWUP]
             and h["MERGE_FAMILY_COUNT"] == by[MERGE]
             and h["ALREADY_COVERED_COUNT"] == by[COVERED]
             and h["TOTAL_NEW_AFTER_APPROVED_BATCH"]
             == len(A.P0_NEW_ANCHORS) + len(high))
    check("C17 headline counts equal the dataset", agree, "")

    # C18 the P0 baseline anchors are all live
    bad = [a for a in A.P0_NEW_ANCHORS + A.P0_ENRICH_ANCHORS if a not in live_ids]
    check("C18 P0 anchors are live", not bad, str(bad))

    # C19 every high-confidence new card carries a batch
    bad = [f["family_id"] for f in high if not f["batch"]]
    check("C19 every approved new card is batched", not bad, str(bad[:5]))

    # C20 duplicate-home pairs are live and distinct
    bad = []
    for d in p["duplicate_home_debt"]:
        a, b = d["pair"]
        if a == b or a not in live_ids or b not in live_ids:
            bad.append(d["pair"])
    check("C20 duplicate-home pairs are live and distinct", not bad, str(bad))

    # C21 two new cards sharing a QB home are a duplicate risk until someone
    # says otherwise. The check does not guess: it flags every same-home pair
    # and fails unless that exact pair carries an explicit distinctness ruling.
    # An unadjudicated pair therefore blocks the count, which is the point.
    seen = {}
    flagged = []
    for f in sorted(high, key=lambda x: x["family_id"]):
        home = f["recommended_qb_file"]
        if home in seen:
            flagged.append((seen[home], f["family_id"]))
        seen[home] = f["family_id"]
    unruled = [pair for pair in flagged if pair not in A.DISTINCT_NEW_PAIRS]
    check("C21 same-home new cards adjudicated distinct", not unruled,
          "%d pairs flagged, %d unruled %s"
          % (len(flagged), len(unruled), unruled[:5]))

    # C24 the dataset must reproduce the authored adjudication table. Without
    # this, relabelling a family in the artefact is invisible: the ambiguity
    # check only fires while the row still says HUMAN_REVIEW_REQUIRED, so
    # promoting an ambiguous family to NEW erases the very evidence of it.
    import final_gap_decisions as FD
    bad = []
    for f in fams:
        gid = f["family_id"]
        if gid not in FD.DECISIONS:
            continue
        want = FD.DECISIONS[gid]
        if f["decision"] != want[0] or f["decision_target"] != want[1]:
            bad.append((gid, f["decision"], want[0]))
    check("C24 dataset reproduces the authored adjudications", not bad,
          str(bad[:5]))

    # C25 a counted new card must rest on a prompt that is actually an ask.
    # Token mass alone is the wrong test: "What is a ship broker." carries two
    # content words and is unmistakably a question, while "FTIR" and "VALEMAX"
    # carry one or two and are bare labels. So a prompt is terse only when it
    # is BOTH low-mass AND unformed - no question mark and no interrogative or
    # imperative verb. Low mass on its own is a property of English, not of
    # examiner intent.
    bad = []
    for f in fams:
        if f["decision"] != NEW or f.get("confidence") != HIGH:
            continue
        formed = any(_is_formed_ask(w) for w in f["raw_ask_variants"])
        mass = max((len(T.mtokens(w)) for w in f["raw_ask_variants"]),
                   default=0)
        if mass < 3 and not formed:
            bad.append((f["family_id"], mass))
    check("C25 no counted new card rests on a bare label", not bad,
          str(bad[:5]))

    # C22 human-review verdicts are from the governed vocabulary
    hv = {"RESOLVED_TO_EXISTING", "NEW_CANONICAL_QA", "ENRICH_EXISTING",
          "FOLLOWUP_ONLY", "MERGE", "STILL_AMBIGUOUS", "DEFER"}
    bad = [r["source_id"] for r in p["human_review"]["rows"]
           if r["verdict"] not in hv]
    check("C22 human-review verdicts governed", not bad, str(bad[:5]))

    # C23 a terse human-review prompt is never resolved
    bad = [r["source_id"] for r in p["human_review"]["rows"]
           if r["prompt_token_mass"] < 3 and r["verdict"] != "STILL_AMBIGUOUS"]
    check("C23 terse prompt never force-resolved", not bad, str(bad[:5]))

    return report()


def report():
    fails = [r for r in results if not r[1]]
    for name, ok, detail in results:
        print("%-4s %-52s %s" % ("PASS" if ok else "FAIL", name, detail))
    print("\n%d checks, %d failures" % (len(results), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
