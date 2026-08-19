"""Validate the laptop-authorised final Oral production inventory.

Every check fails CLOSED: a missing input is a failure, never a skip, and a
check that cannot run reports `unavailable` rather than passing quietly.

The seven lettered checks are the tamper controls the review was required to
implement. Two of them (F and G) had no equivalent in the adjudicated
validator, and G is the check that would have caught the GAP-0065 / GAP-0689
inconsistency before it reached an authorisation.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import production_authorization_decisions as PD  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "meoclass1" / "oral-intelligence" / "examiner-audit"
DATA = AUDIT / "FINAL_ORAL_PRODUCTION_AUTHORIZATION.json"
SRC = AUDIT / "FINAL_REMAINING_ORAL_PRODUCTION_DECISIONS.json"

QCARD = re.compile(
    r'<div[^>]*(?:class="[^"]*\bq-card\b[^"]*"[^>]*id="(q\d+)"'
    r'|id="(q\d+)"[^>]*class="[^"]*\bq-card\b[^"]*")')

FAILED = []
RAN = 0


def check(name, ok, detail=""):
    global RAN
    RAN += 1
    if not ok:
        FAILED.append(name)
    print("%-4s %-62s %s" % ("PASS" if ok else "FAIL", name, detail))


def live_anchors():
    out = set()
    for p in sorted((ROOT / "meoclass1").glob("QB*.html")):
        if "heat" in p.name.lower():
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        for m in QCARD.finditer(t):
            out.add("%s#%s" % (p.stem, m.group(1) or m.group(2)))
    return out


def main():
    if not DATA.exists():
        check("authorisation dataset present", False,
              "unavailable: %s not generated" % DATA.name)
        return finish()
    d = json.loads(DATA.read_text(encoding="utf-8"))
    src = json.loads(SRC.read_text(encoding="utf-8"))
    rows = d["families"]
    acts = d["production_actions"]
    by_id = {r["family_id"]: r for r in rows}
    live = live_anchors()

    check("live corpus readable", bool(live), "%d anchors" % len(live))
    check("baseline independently reproduced",
          d["baseline"]["independently_reproduced"]
          and d["baseline"]["live_canonical_questions"] == len(live),
          "%d == %d" % (d["baseline"]["live_canonical_questions"], len(live)))

    # ---------------- structural integrity ----------------
    check("S1 every adjudicated family carried forward",
          len(rows) == len(src["families"])
          and {r["family_id"] for r in rows}
          == {f["family_id"] for f in src["families"]},
          "%d families" % len(rows))

    dup = [k for k, v in Counter(r["family_id"] for r in rows).items() if v > 1]
    check("S2 no duplicate family row", not dup, str(dup[:5]))

    VOCAB = set(src["dispositions"]) | {"NOT_A_GAP"}
    bad = sorted(r["family_id"] for r in rows
                 if r["laptop_decision"] not in VOCAB)
    check("S3 every decision from the governed vocabulary", not bad, str(bad[:5]))

    bad = sorted(r["family_id"] for r in rows
                 if r["laptop_review_status"] not in
                 ("LAPTOP_CONFIRMED", "LAPTOP_CHANGED"))
    check("S4 every family carries a review status", not bad, str(bad[:5]))

    bad = sorted(r["family_id"] for r in rows
                 if r["laptop_review_status"] == "LAPTOP_CHANGED"
                 and r["family_id"] not in PD.OVERRIDES)
    check("S5 only recorded overrides are marked changed", not bad, str(bad[:5]))

    bad = sorted(fid for fid in PD.OVERRIDES
                 if by_id.get(fid, {}).get("laptop_decision")
                 != PD.OVERRIDES[fid][0])
    check("S6 every recorded override is applied", not bad, str(bad[:5]))

    # ---------------- lettered tamper controls ----------------
    # A. an ambiguous family may never be authorised as a new card
    amb = {r["family_id"] for r in rows
           if r["laptop_decision"] == "HUMAN_REVIEW_REQUIRED"}
    newf = {f for a in acts if a["kind"].startswith("NEW_CARD")
            for f in a["family_ids"]}
    check("A ambiguous family never authorised as NEW",
          not (amb & newf), str(sorted(amb & newf)[:5]))

    # B. production action ids must be unique
    ids = [a["production_action_id"] for a in acts]
    dup = [k for k, v in Counter(ids).items() if v > 1]
    check("B no duplicate production action id", not dup,
          "%d ids" % len(ids) if not dup else str(dup[:5]))

    # C. an approved new card must rest on source evidence
    bad = sorted(f for a in acts if a["kind"].startswith("NEW_CARD")
                 for f in a["family_ids"]
                 if not by_id[f]["source_occurrence_ids"])
    check("C every approved new card has source occurrences", not bad,
          str(bad[:5]))

    # D. a completed P0 family may never re-enter production
    p0 = set(src["baseline"]["p0_new_anchors"]) | set(
        src["baseline"]["p0_enrich_anchors"])
    p0fams = {"GAP-0002", "GAP-0016", "GAP-0034", "GAP-0042", "GAP-0043",
              "GAP-0044", "GAP-0048", "GAP-0409", "GAP-0410", "GAP-0454"}
    reentered = sorted(p0fams & {r["family_id"] for r in rows})
    check("D no completed P0 family reintroduced", not reentered,
          str(reentered))
    check("D2 P0 anchors all still live", not (p0 - live), str(sorted(p0 - live)))

    # E. every enrichment / follow-up target must resolve to a live anchor
    bad = sorted((a["production_action_id"], a["target"]) for a in acts
                 if a["kind"] in ("ENRICH_EDIT", "FOLLOWUP_INSERTION",
                                  "EXISTING_CARD_NOTES_PROMOTION")
                 and a["target"] not in live)
    check("E every existing-card target resolves live", not bad, str(bad[:5]))

    # F. a new-card Notes promotion must be inside the projected canonical count
    pc = d["projected_canonical"]
    nnotes = sum(1 for a in acts if a["kind"] == "NEW_CARD_FROM_NOTES")
    ngap = sum(1 for a in acts if a["kind"] == "NEW_CARD_FROM_GAP")
    ok = (pc["APPROVED_NEW_FROM_NOTES_PROMOTION"] == nnotes
          and pc["APPROVED_NEW_FROM_GAP"] == ngap
          and pc["FINAL_PROJECTED_CANONICAL"]
          == pc["CURRENT_CANONICAL"] + ngap + nnotes)
    check("F new-card Notes promotions inside projected count", ok,
          "%d + %d + %d = %d" % (pc["CURRENT_CANONICAL"], ngap, nnotes,
                                 pc["FINAL_PROJECTED_CANONICAL"]))

    # G. no family may be assigned to two incompatible actions, and no two
    #    families sharing a target may hold contradictory dispositions.
    seen = defaultdict(set)
    for a in acts:
        for f in a["family_ids"]:
            seen[f].add(a["kind"])
    bad = sorted(f for f, k in seen.items() if len(k) > 1)
    check("G1 no family in two incompatible actions", not bad, str(bad[:5]))

    tgt = defaultdict(set)
    for r in rows:
        if r["target"] and str(r["target"]).startswith("QB"):
            tgt[r["target"]].add(r["laptop_decision"])
    clash = sorted(t for t, s in tgt.items()
                   if "ALREADY_COVERED" in s and "NOTES_TO_QB_PROMOTION" in s)
    check("G2 no target both covered and promoted-from", not clash, str(clash))

    # ---------------- accounting ----------------
    counts = Counter(r["laptop_decision"] for r in rows)
    a_ = d["authorised"]
    agree = (a_["AUTHORISED_NEW_CANONICAL_QA"] == counts["NEW_CANONICAL_QA"]
             and a_["ENRICHMENT_SOURCE_FAMILIES"] == counts["ENRICH_EXISTING_QB"]
             and a_["FOLLOWUP_SOURCE_FAMILIES"] == counts["FOLLOWUP_ONLY"]
             and a_["DEFERRED"] == counts["DEFER_LOW_VALUE"]
             and a_["AMBIGUOUS"] == counts["HUMAN_REVIEW_REQUIRED"])
    check("N1 headline counts equal the dataset", agree, "")

    check("N2 family total conserved across the review",
          sum(counts.values()) == len(src["families"]),
          "%d == %d" % (sum(counts.values()), len(src["families"])))

    ecount = len({a["target"] for a in acts if a["kind"] == "ENRICH_EDIT"})
    check("N3 enrichment edits are deduplicated by target",
          ecount == a_["AUTHORISED_EXISTING_QB_ENRICHMENT_ACTIONS"]
          and ecount <= counts["ENRICH_EXISTING_QB"],
          "%d edits from %d families" % (ecount, counts["ENRICH_EXISTING_QB"]))

    fcount = len({a["target"] for a in acts if a["kind"] == "FOLLOWUP_INSERTION"})
    check("N4 follow-up groups are deduplicated by parent",
          fcount == a_["AUTHORISED_FOLLOWUP_INSERTION_ACTIONS"]
          and fcount <= counts["FOLLOWUP_ONLY"],
          "%d groups from %d families" % (fcount, counts["FOLLOWUP_ONLY"]))

    check("N5 every new card is batched",
          all(by_id[f]["priority"] for a in acts
              if a["kind"] == "NEW_CARD_FROM_GAP" for f in a["family_ids"]), "")

    bad = sorted(fid for fid in PD.PROMOTION_KIND
                 if by_id.get(fid, {}).get("laptop_decision")
                 != "NOTES_TO_QB_PROMOTION")
    check("N6 every classified promotion is still a promotion", not bad,
          str(bad[:5]))

    bad = sorted(r["family_id"] for r in rows
                 if r["laptop_decision"] == "NOTES_TO_QB_PROMOTION"
                 and r["family_id"] not in PD.PROMOTION_KIND)
    check("N7 every promotion is classified new-card or existing-card",
          not bad, str(bad[:5]))

    check("N8 total actions equal the sum of the kinds",
          len(acts) == d["workload"]["TOTAL_PRODUCTION_ACTIONS"]
          == ngap + nnotes + ecount + fcount
          + sum(1 for a in acts
                if a["kind"] == "EXISTING_CARD_NOTES_PROMOTION"),
          "%d" % len(acts))

    # ---------------- product safety ----------------
    check("P1 no action targets a cheatsheet",
          not [a for a in acts if a["target"] and "heat" in str(a["target"]).lower()],
          "")
    check("P2 duplicate-home debt carried forward, not counted as content",
          d["duplicate_home_debt"] == src["duplicate_home_debt"], "")

    finish()


def finish():
    print("\n%d checks, %d failures" % (RAN, len(FAILED)))
    if FAILED:
        for f in FAILED:
            print("  FAILED: %s" % f)
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
