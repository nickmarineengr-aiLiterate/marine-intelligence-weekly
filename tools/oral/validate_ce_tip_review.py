"""Release gate for the strong CE-tip held-relationship review.

STRONG_CE_TIP_REVIEW_DECISIONS.json adjudicates the ten Release-A pairs that
finalize_release_a.py held at HOLD_EVIDENCE_BELOW_FLOOR and whose page-prose
strength was STRONG_CE_TIP_ASSERTION. This gate proves, from files on disk:

  * the decision set is exactly that held set - every one accounted for, one
    decision each, no eleventh relation, no historically review-held pair;
  * every decision names a live target whose anchor exists and whose current
    question text is the text that was reviewed;
  * every decision uses a governed outcome; the candidate tier is the one its
    outcome permits (a CE-tip-only row can never be Confirmed); held and
    rejected rows carry no tier;
  * every approved row carries evidence ids, each of which resolves to a real
    record that names THIS examiner and THIS question: PROSE ids to a CE-tip
    prose row on the card, ASC ids to a 788 occurrence whose governed target
    is this question, MASTER/JULY ids to a ledger row mapped to this question,
    NOTEV ids to a Notes evidence row reverse-connected to this pair;
  * every corroboration id resolves and names this examiner;
  * the reviewed CE-tip wording is still on the live card, so a card edited to
    topic-only prose cannot keep its approval silently;
  * the snapshot's CE_TIP_REVIEW rows are exactly the approved decisions, no
    approved pair renders twice, and no held row renders through this route.

Exit 0 only when every check passes. Failures are named, never thrown.

    PYTHONIOENCODING=utf-8 python tools/oral/validate_ce_tip_review.py [--json]
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L                       # noqa: E402
import build_examiner_index as G           # noqa: E402
import verify_tiers as V                   # noqa: E402

RESULTS = []
OUT = L.OUT
APPROVE = set(G.REVIEW_OUTCOME_TIER)
HOLD = set(G.REVIEW_HOLD_OUTCOMES)
STRONG = "STRONG_CE_TIP_ASSERTION"


def check(name, ok, detail=""):
    RESULTS.append({"check": name, "status": "PASS" if ok else "FAIL",
                    "detail": "" if ok else str(detail)})


def js(name):
    p = OUT / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def jl(name):
    p = OUT / name
    if not p.exists():
        return None
    with p.open(encoding="utf-8") as fh:
        return [json.loads(x) for x in fh if x.strip()]


def card_text_cache():
    cache = {}

    def get(qid):
        f, a = qid.split("#")
        if f not in cache:
            p = L.MEO / (f + ".html")
            cache[f] = V.card_blocks(p)[0] if p.exists() else {}
        blk = cache[f].get(a)
        return L.strip_tags(blk) if blk else ""
    return get


def main(argv):
    dec = js(G.REVIEW_NAME)
    if dec is None:
        check("review decisions artefact present", False, G.REVIEW_NAME + " missing")
        return finish(argv)
    rows = dec.get("decisions", [])
    ids = [d["relation_id"] for d in rows]

    # ------------------------------------------------- 1. the held set itself
    held = js("RELEASE_A_HELD.json") or {"held": []}
    ready = js("READY_CONNECTIONS_V2.json") or []
    strength = {(r["examiner"], r["canonical_question_id"]): r["phase1_strength"]
                for r in ready}
    expected = sorted(h["relation_id"] for h in held["held"]
                      if h["decision"] == "HOLD_EVIDENCE_BELOW_FLOOR"
                      and strength.get((h["examiner"], h["canonical_question_id"])) == STRONG)
    check("held STRONG_CE_TIP set is derivable and non-empty", bool(expected))
    check("every held STRONG_CE_TIP pair has exactly one decision",
          sorted(ids) == expected and len(ids) == len(set(ids)),
          "missing=%s extra=%s dup=%s" % (
              sorted(set(expected) - set(ids)), sorted(set(ids) - set(expected)),
              [k for k, v in Counter(ids).items() if v > 1]))
    check("decision count equals its own record", dec.get("reviewed") == len(rows))
    check("outcome tally equals its own records",
          dec.get("decisions_by_outcome") == dict(sorted(
              Counter(d["decision"] for d in rows).items())))
    review_held = {h["relation_id"] for h in
                   (js("RELEASE_A_REVIEW_DECISIONS.json") or {"held": []})["held"]}
    check("no historically review-held Release-A pair is in this review",
          not (review_held & set(ids)), str(sorted(review_held & set(ids))))

    # ---------------------------------------------- 2. targets and outcomes
    inv = {q["canonical_question_id"]: q for q in L.build_inventory()}
    anchors = L.all_anchors()
    reg = js("EXAMINER_ALIAS_REGISTER.json") or {"examiners": []}
    examiners = {e["canonical_name"] for e in reg["examiners"]}
    bad_ex = [d["relation_id"] for d in rows if d["examiner"] not in examiners]
    check("every decision names a registered examiner", not bad_ex, str(bad_ex))
    bad_t = []
    for d in rows:
        q = inv.get(d["canonical_question_id"])
        t = d.get("reviewed_target") or {}
        if (q is None or q["file"] != t.get("file") or q["anchor"] != t.get("anchor")
                or q["anchor"] not in anchors.get(q["file"], set())):
            bad_t.append(d["relation_id"])
    check("every reviewed target resolves to a live question anchor", not bad_t, str(bad_t))
    bad_q = [d["relation_id"] for d in rows
             if d["canonical_question_id"] in inv
             and L.norm(inv[d["canonical_question_id"]]["question_text"])
             != L.norm(d.get("reviewed_question_text", ""))]
    check("every reviewed question text is the live question text", not bad_q, str(bad_q))
    bad_o = [d["relation_id"] for d in rows if d["decision"] not in APPROVE | HOLD]
    check("every decision uses a governed outcome", not bad_o, str(bad_o))
    bad_tier = [d["relation_id"] for d in rows
                if (d["decision"] in APPROVE and d.get("candidate_tier")
                    != G.REVIEW_OUTCOME_TIER[d["decision"]])
                or (d["decision"] in HOLD and d.get("candidate_tier"))]
    check("candidate tier is exactly what the outcome permits (held rows carry none)",
          not bad_tier, str(bad_tier))
    types = {"PRIMARY_ASK", "CROSS_QUESTION", "FOLLOW_UP", "EXPECTED_DETAIL",
             "TOPIC_INFERENCE_ONLY"}
    bad_rt = [d["relation_id"] for d in rows if d.get("relationship_type") not in types]
    check("every decision carries a governed relationship type", not bad_rt, str(bad_rt))
    classes = {"CE_EXPLICIT_PRIMARY_ASK", "CE_EXPLICIT_FOLLOWUP",
               "CE_EXPLICIT_EXPECTED_DETAIL", "CE_STRONG_BUT_NONEXPLICIT",
               "CE_TOPIC_ASSOCIATION", "CE_INCIDENTAL_MENTION", "CE_UNSAFE"}
    bad_c = [d["relation_id"] for d in rows if d.get("ce_provenance_class") not in classes]
    check("every decision carries a CE provenance class", not bad_c, str(bad_c))
    bad_r = [d["relation_id"] for d in rows if not (d.get("reason") or "").strip()]
    check("every decision states a reason", not bad_r, str(bad_r))

    # -------------------------------------------- 3. evidence resolution
    prose = {}
    pp = OUT / "PROSE_EXAMINER_EVIDENCE.csv"
    if pp.exists():
        with pp.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                prose[(r["examiner"], r["canonical_question_id"])] = r
    led = {e["evidence_id"]: e for e in (jl("EXAMINER_EVIDENCE_LEDGER.jsonl") or [])}
    fin = {r["source_id"]: r for r in (jl("FINAL_788_PRODUCTION_DISPOSITION.jsonl") or [])}
    nev = {e["evidence_id"]: e for e in (jl("ORAL_NOTES_EXAMINER_EVIDENCE.jsonl") or [])}
    rev_pairs = set()
    for r in (js("ORAL_NOTES_REVERSE_CONNECTIONS.json") or {"rows": []})["rows"]:
        for u in r.get("note_units", []):
            rev_pairs.add((r["examiner"], r.get("canonical_question_id"), u))

    def resolves_for(ex, qid, eid, need_target):
        """(resolves, names examiner, names this target)"""
        m = re.fullmatch(r"PROSE:([^:]+):(.+)", eid)
        if m:
            r = prose.get((m.group(1), m.group(2)))
            return (r is not None, bool(r) and m.group(1) == ex and r["in_ce_tip_block"] == "True",
                    bool(r) and m.group(2) == qid)
        if eid in led:
            r = led[eid]
            return (True, r.get("examiner_normalized") == ex,
                    r.get("canonical_question_id") == qid)
        if eid in fin:
            r = fin[eid]
            return (True, r.get("examiner") == ex, r.get("matched_question_id") == qid)
        if eid in nev:
            r = nev[eid]
            return (True, r.get("examiner") == ex, (ex, qid, r["note_unit_id"]) in rev_pairs)
        return (False, False, False)

    empty = [d["relation_id"] for d in rows if d["decision"] in APPROVE and not d.get("evidence_ids")]
    check("every approved decision carries evidence ids", not empty, str(empty))
    unsorted = [d["relation_id"] for d in rows
                if d.get("evidence_ids") != sorted(set(d.get("evidence_ids") or []))]
    check("evidence ids are unique and stably ordered", not unsorted, str(unsorted))
    no_prose = [d["relation_id"] for d in rows if d["decision"] in APPROVE
                and not any(e.startswith("PROSE:") for e in d["evidence_ids"])]
    check("every approved CE-tip decision cites the card's own CE-tip prose row",
          not no_prose, str(no_prose))
    unresolved, misattr, offtarget = [], [], []
    for d in rows:
        ex, qid = d["examiner"], d["canonical_question_id"]
        for eid in d.get("evidence_ids") or []:
            ok, ex_ok, t_ok = resolves_for(ex, qid, eid, True)
            if not ok:
                unresolved.append((d["relation_id"], eid))
            elif not ex_ok:
                misattr.append((d["relation_id"], eid))
            elif not t_ok:
                offtarget.append((d["relation_id"], eid))
        for eid in d.get("corroboration_ids") or []:
            ok, ex_ok, _ = resolves_for(ex, qid, eid, False)
            if not ok:
                unresolved.append((d["relation_id"], eid))
            elif not ex_ok:
                misattr.append((d["relation_id"], eid))
    check("every evidence and corroboration id resolves to a record", not unresolved, str(unresolved))
    check("every evidence and corroboration record names its own examiner", not misattr, str(misattr))
    check("every evidence id's governed target is this question", not offtarget, str(offtarget))

    # a Confirmed / Reported outcome needs governed-admissible evidence, not prose
    bad_conf = []
    for d in rows:
        if d["decision"] == "APPROVE_CONFIRMED_RELATIONSHIP":
            if not any(e in led and led[e]["evidence_class"] == "PRIMARY_CANDIDATE_RECORD"
                       and led[e].get("legacy_mapping") in ("VERIFIED_MATCH", "VERIFIED_SAME_CORE")
                       for e in d["evidence_ids"]):
                bad_conf.append(d["relation_id"])
        if d["decision"] == "APPROVE_REPORTED_RELATIONSHIP":
            if not any(e in fin and fin[e]["content_disposition"] in ("EXACT_MATCH", "NEAR_MATCH")
                       for e in d["evidence_ids"]):
                bad_conf.append(d["relation_id"])
    check("Confirmed/Reported outcomes rest on governed-admissible primary/external evidence",
          not bad_conf, str(bad_conf))

    # ------------------------------------------ 4. wording pinned on the card
    get = card_text_cache()
    gone = []
    for d in rows:
        w = d.get("reviewed_ce_tip_wording") or ""
        if not w.strip() or L.norm(w) not in L.norm(get(d["canonical_question_id"])):
            gone.append(d["relation_id"])
    check("every reviewed CE-tip wording is still on the live card", not gone, str(gone))
    # and it must name the examiner: an excerpt that no longer carries the name
    # is topic prose, whatever the decision says
    named = []
    for d in rows:
        w = d.get("reviewed_ce_tip_wording") or ""
        rx = V.NAME_RE.get(d["examiner"])
        if d["decision"] in APPROVE and not (rx and rx.search(w)):
            named.append(d["relation_id"])
    check("every approved wording excerpt names its examiner", not named, str(named))

    # ---------------------------------------- 5. the snapshot / rendered index
    snap = js(G.SNAPSHOT_NAME)
    if snap is None:
        check("examiner index snapshot present", False)
        return finish(argv)
    approved = {(d["examiner"], d["canonical_question_id"]): d for d in rows
                if d["decision"] in APPROVE}
    heldk = {(d["examiner"], d["canonical_question_id"]) for d in rows
             if d["decision"] in HOLD}
    via = {(r["examiner"], r["canonical_question_id"]): r for r in snap["rows"]
           if "CE_TIP_REVIEW" in r["sources"]}
    check("snapshot CE_TIP_REVIEW rows are exactly the approved decisions",
          set(via) == set(approved),
          "extra=%s missing=%s" % (sorted(set(via) - set(approved)),
                                   sorted(set(approved) - set(via))))
    bad = [k for k, r in via.items() if r["tier"] != approved.get(k, {}).get("candidate_tier")
           and k in approved]
    check("every CE_TIP_REVIEW row renders at its decided candidate tier", not bad, str(bad))
    refs_bad = [k for k, r in via.items()
                if k in approved and approved[k]["relation_id"] not in r["refs"]]
    check("every CE_TIP_REVIEW row carries its relation id", not refs_bad, str(refs_bad))
    leaked = [k for k in heldk
              if any("CE_TIP_REVIEW" in r["sources"] for r in snap["rows"]
                     if (r["examiner"], r["canonical_question_id"]) == k)]
    check("no held or rejected review row renders through the review route",
          not leaked, str(leaked))
    keys = [(r["examiner"], r["canonical_question_id"]) for r in snap["rows"]]
    dup = [k for k, v in Counter(keys).items() if v > 1 and k in approved]
    check("no approved review pair renders twice", not dup, str(dup))
    try:
        fresh = G.resolve_snapshot()
        check("snapshot equals a fresh resolve including the review route",
              fresh == snap)
    except G.BuildFailure as e:
        check("canonical data resolves with the review route", False, str(e))
    return finish(argv)


def finish(argv):
    fails = [r for r in RESULTS if r["status"] == "FAIL"]
    if "--json" in argv:
        print(json.dumps({"results": RESULTS, "pass": len(RESULTS) - len(fails),
                          "fail": len(fails)}, indent=2, ensure_ascii=False))
    else:
        for r in RESULTS:
            print("%s  %s%s" % (r["status"], r["check"],
                                ("  -- " + r["detail"]) if r["detail"] else ""))
        print("%d PASS / %d FAIL" % (len(RESULTS) - len(fails), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
