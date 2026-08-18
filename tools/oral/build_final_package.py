"""Phase 2A-iii final package — Release A, P0, movement, review residue.

Everything here is DERIVED. No count is hand-entered, no disposition is
hand-edited, and every emitted record names the source occurrence, evidence
record or note unit it rests on, so a reviewer can walk any number back to the
row that produced it.

Three separations are load-bearing and are kept apart end to end:

  canonical content match   what MIW *asks*   EXACT .. AMBIGUOUS
  Notes support             what MIW *knows*  NO_NOTES_SUPPORT .. COMPLETE
  production action         what MIW must *do*  NO_ACTION .. NEW_ANSWER_REQUIRED

MISSING + NOTES_COMPLETE_SUPPORT is not an EXACT match. It is a canonical gap
over material MIW already holds, and its production action is a promotion, not
research from zero. Collapsing those three axes into one status is the single
mistake that would put a wrong answer, or a wrong connection, in front of a
candidate six days before an oral.

  PYTHONIOENCODING=utf-8 python tools/oral/build_final_package.py

Portability: repo-relative, no drive letters, no machine-local paths, no
timestamp in any semantic artefact.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402
from oral_text import mtokens, designator_conflict  # noqa: E402

OUT = L.OUT

# ---------------------------------------------------------------- vocabularies

CANONICAL = ("EXACT_MATCH", "NEAR_MATCH", "SAME_CORE_ASK",
             "PARTIAL_COVERAGE", "MISSING", "AMBIGUOUS")

NOTES_TIERS = ("NO_NOTES_SUPPORT", "NOTES_TOPIC_SUPPORT",
               "NOTES_PARTIAL_SUPPORT", "NOTES_STRONG_SUPPORT",
               "NOTES_COMPLETE_SUPPORT")

PRODUCTION = ("NO_ACTION_ALREADY_COVERED", "CONNECT_EXISTING",
              "CONNECT_AND_ENRICH", "NOTES_TO_QB_PROMOTION",
              "NEW_ANSWER_REQUIRED", "MERGE_WITH_EXISTING_GAP",
              "HUMAN_REVIEW")

# Ranked weakest to strongest. Release A reads the strongest tier a pair holds.
EVIDENCE_RANK = {
    "TOPIC_INFERRED": 0,
    "NOTE_WEAK_MENTION": 0,
    "JULY_DERIVED_SIBLING": 1,
    "CURRENT_INDEX_RECOVERY": 1,
    "CE_TIP": 2,
    "NOTE_EXPLICIT": 3,
    "EXTERNAL_SOURCE_CONFIRMED": 4,
    "PRIMARY_TRACKER": 5,
}

# Tiers that may carry a Release-A pair on their own. Below this line a pair is
# an inference or a page declaration, and the Laptop review held both out.
RELEASE_FLOOR = 3


def jl(name):
    return [json.loads(x) for x in (OUT / name).open(encoding="utf-8") if x.strip()]


def js(name):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def dump(obj, name):
    L.jdump(obj, name)


def md(lines, name):
    (OUT / name).write_text("\n".join(lines) + "\n", encoding="utf-8",
                            newline="\n")


# ---------------------------------------------------------------- load

def load():
    d = {}
    d["rec"] = {r["source_id"]: r for r in jl("ORAL_788_RECONCILIATION.jsonl")}
    d["notes"] = {r["source_id"]: r for r in jl("ORAL_NOTES_COVERAGE.jsonl")}
    d["base"] = js("PHASE2_BASELINE_SNAPSHOT.json")["rows"]
    d["rel"] = jl("CURRENT_EXAMINER_RELATIONSHIPS.jsonl")
    d["ev"] = jl("EXAMINER_EVIDENCE_LEDGER_V2.jsonl")
    d["nev"] = jl("ORAL_NOTES_EXAMINER_EVIDENCE.jsonl")
    d["rev"] = js("ORAL_NOTES_REVERSE_CONNECTIONS.json")["rows"]
    d["ready"] = js("READY_CONNECTIONS_V2.json")
    d["gaps"] = js("ORAL_GAP_CANDIDATES.json")
    d["hrq"] = js("HUMAN_REVIEW_QUEUE.json")
    d["adj"] = {a["gap_id"]: a for a in
                js("P0_ADJUDICATIONS.json")["adjudications"]}
    d["inv"] = {q["canonical_question_id"]: q for q in L.build_inventory()}
    return d


def qtext(inv, qid):
    q = inv.get(qid)
    return (q or {}).get("question_text", "")


# ---------------------------------------------------------------- production

def production_action(canon, notes, mapping):
    """One downstream action per occurrence, derived, never overloaded.

    The canonical axis says whether MIW asks the question. The Notes axis says
    whether MIW holds the knowledge. Only both together decide what has to be
    built, and a MISSING ask over complete Notes is a promotion rather than a
    new answer precisely because the material already exists and only its
    surface is absent.
    """
    if canon == "AMBIGUOUS":
        return "HUMAN_REVIEW"
    if canon in ("EXACT_MATCH", "NEAR_MATCH", "SAME_CORE_ASK"):
        return ("NO_ACTION_ALREADY_COVERED"
                if mapping == "ALREADY_LINKED" else "CONNECT_EXISTING")
    if canon == "PARTIAL_COVERAGE":
        return "CONNECT_AND_ENRICH"
    # canon == MISSING
    if notes in ("NOTES_COMPLETE_SUPPORT", "NOTES_STRONG_SUPPORT"):
        return "NOTES_TO_QB_PROMOTION"
    return "NEW_ANSWER_REQUIRED"


# ---------------------------------------------------------------- movement

def movement_reason(old, new, rec, inv):
    """Why this row moved, from the record rather than from a narrative.

    The ladder is ordered by specificity: a demotion out of SAME_CORE is
    explained by the admission floor whatever else is also true of the row, and
    only a row no earlier rung explains is allowed to reach OTHER_EXPLAINED.
    """
    o, n = old["content_disposition"], new["content_disposition"]
    ot, nt = old.get("matched_question_id"), new.get("matched_question_id")

    if o == "SAME_CORE_ASK" and n != "SAME_CORE_ASK":
        return "SAME_CORE_FLOOR"
    if rec.get("source_spelling_repairs") is not None and o != n:
        # A row whose old coverage was manufactured by a repair the curated map
        # no longer performs. The repair list is now the curated one, so a row
        # that lost coverage and carries no repair note lost it to the removal
        # of the speculative engine.
        if n in ("MISSING", "AMBIGUOUS") and o in ("PARTIAL_COVERAGE",
                                                   "NEAR_MATCH", "EXACT_MATCH"):
            if not rec.get("source_spelling_repairs"):
                return "SPELL_REPAIR_SAFETY"
    if ot and ot != nt:
        src = mtokens(rec["raw_question_text"])
        if designator_conflict(src, mtokens(qtext(inv, ot))):
            return "DESIGNATOR_CONFLICT_FIX"
    if n == "AMBIGUOUS" and o != "AMBIGUOUS":
        return "HUMAN_ADJUDICATION"
    if ot != nt:
        return "TARGET_RESELECTION"
    return "OTHER_EXPLAINED"


def build_movement(d):
    rec, base, inv = d["rec"], d["base"], d["inv"]
    moved, retarget = [], []
    for sid in sorted(rec):
        n, o = rec[sid], base[sid]
        nt = n.get("matched_question_id")
        ot = o.get("matched_question_id")
        row = {
            "source_id": sid,
            "examiner": n["examiner"],
            "raw_question_text": n["raw_question_text"],
            "old_disposition": o["content_disposition"],
            "new_disposition": n["content_disposition"],
            "old_target": ot,
            "new_target": nt,
            "notes_support": d["notes"][sid]["notes_support"],
        }
        if o["content_disposition"] != n["content_disposition"]:
            row["reason"] = movement_reason(o, n, n, inv)
            moved.append(row)
        elif ot != nt:
            row["reason"] = "TARGET_RESELECTION"
            retarget.append(row)

    def tally(rows, key):
        t = {}
        for r in rows:
            t[r[key]] = t.get(r[key], 0) + 1
        return dict(sorted(t.items()))

    trans = {}
    for r in moved:
        k = "%s -> %s" % (r["old_disposition"], r["new_disposition"])
        trans[k] = trans.get(k, 0) + 1

    report = {
        "note": ("Movement of the 788 from the Phase-2 baseline at de6d3f2 to "
                 "the Phase-2A-iii recompute. A row that keeps its disposition "
                 "but changes target has still moved, and is counted "
                 "separately rather than reported as unchanged."),
        "baseline_commit": js("PHASE2_BASELINE_SNAPSHOT.json")["baseline_commit"],
        "source_rows": len(rec),
        "disposition_changed": len(moved),
        "target_changed_only": len(retarget),
        "unchanged": len(rec) - len(moved) - len(retarget),
        "transitions": dict(sorted(trans.items(), key=lambda kv: (-kv[1], kv[0]))),
        "reason_breakdown": tally(moved, "reason"),
        "disposition_changes": moved,
        "target_only_changes": retarget,
    }
    dump(report, "RECONCILIATION_MOVEMENT_REPORT.json")
    return report


# ---------------------------------------------------------------- release A

def build_release_a(d):
    """One record per unique examiner-question relationship we can defend.

    A pair enters only on evidence that names the examiner AND a target that
    resolves. Three admissible routes, and the exclusions are recorded with a
    reason rather than dropped silently, because "we did not publish it" and
    "we never considered it" are different claims to a reviewer.
    """
    inv, anchors = d["inv"], L.all_anchors()
    pairs = {}
    excluded = []

    def add(examiner, qid, tier, evid, why, sid=None):
        key = (examiner, qid)
        p = pairs.setdefault(key, {
            "examiner": examiner, "canonical_question_id": qid,
            "evidence_ids": [], "source_occurrence_ids": [],
            "evidence_tiers": [], "reasons": [],
        })
        if evid and evid not in p["evidence_ids"]:
            p["evidence_ids"].append(evid)
        if sid and sid not in p["source_occurrence_ids"]:
            p["source_occurrence_ids"].append(sid)
        if tier not in p["evidence_tiers"]:
            p["evidence_tiers"].append(tier)
        if why not in p["reasons"]:
            p["reasons"].append(why)

    # Route 1 - Phase-1 tracker-verified connections.
    for r in d["ready"]:
        if r["status"] not in ("READY_VERIFIED", "READY_VERIFIED_MULTI_SOURCE"):
            excluded.append({"examiner": r["examiner"],
                             "canonical_question_id": r["canonical_question_id"],
                             "route": "PHASE1_READY",
                             "reason": "EXCLUDED_%s" % r["status"]})
            continue
        add(r["examiner"], r["canonical_question_id"], "PRIMARY_TRACKER",
            None, "tracker-verified connection (%s)" % r["status"])

    # Route 2 - the external compilation, but only where the canonical target
    # is defensible. EXACT and NEAR only: SAME_CORE ran at 60% precision in the
    # Laptop's sample and is held out entirely, floor or no floor.
    for sid in sorted(d["rec"]):
        r = d["rec"][sid]
        disp, qid = r["content_disposition"], r.get("matched_question_id")
        if not qid:
            continue
        if disp in ("EXACT_MATCH", "NEAR_MATCH"):
            add(r["examiner"], qid, "EXTERNAL_SOURCE_CONFIRMED", None,
                "external surveyor compilation with a %s canonical target" % disp,
                sid)
        else:
            excluded.append({"examiner": r["examiner"],
                             "canonical_question_id": qid,
                             "source_id": sid, "route": "EXTERNAL_788",
                             "reason": "EXCLUDED_TARGET_%s" % disp})

    # Route 3 - an explicit examiner cue in an Oral Note, where the note also
    # resolves to one unambiguous canonical question.
    nev_by_unit = {}
    for e in d["nev"]:
        nev_by_unit.setdefault(e["note_unit_id"], []).append(e)
    for r in d["rev"]:
        if r.get("reverse_class") != "NOTE_CREATES_NEW_EXPLICIT_CONNECTION":
            continue
        qid = r.get("canonical_question_id")
        disp = r.get("canonical_disposition")
        if not qid or disp not in ("EXACT_MATCH", "NEAR_MATCH"):
            excluded.append({"examiner": r["examiner"],
                             "canonical_question_id": qid,
                             "source_id": r.get("source_id"),
                             "route": "NOTE_EXPLICIT",
                             "reason": "EXCLUDED_TARGET_%s" % disp})
            continue
        eids = []
        for u in r.get("note_units", []):
            for e in nev_by_unit.get(u, []):
                if e["examiner"] == r["examiner"]:
                    eids.append(e["evidence_id"])
        for e in sorted(set(eids)):
            add(r["examiner"], qid, "NOTE_EXPLICIT", e,
                "explicit examiner cue in an Oral Note over a %s target" % disp,
                r.get("source_id"))

    # Finalise: strongest tier decides, and the anchor must resolve.
    out, dropped = [], []
    for (examiner, qid), p in sorted(pairs.items()):
        best = max(p["evidence_tiers"], key=lambda t: EVIDENCE_RANK.get(t, -1))
        if EVIDENCE_RANK.get(best, -1) < RELEASE_FLOOR:
            dropped.append({"examiner": examiner, "canonical_question_id": qid,
                            "reason": "EXCLUDED_BELOW_EVIDENCE_FLOOR",
                            "strongest_tier": best})
            continue
        f, a = (qid.split("#", 1) + [""])[:2]
        fn = f if f.endswith(".html") else f + ".html"
        if a not in anchors.get(fn, set()):
            dropped.append({"examiner": examiner, "canonical_question_id": qid,
                            "reason": "EXCLUDED_TARGET_ANCHOR_UNRESOLVED"})
            continue
        out.append({
            "relation_id": "RELA-%s-%s" % (examiner.upper(),
                                           qid.replace("#", "-")),
            "examiner": examiner,
            "canonical_question_id": qid,
            "file": fn,
            "anchor": a,
            "url": "/meoclass1/%s#%s" % (fn, a),
            "candidate_safe_question_text": qtext(inv, qid),
            "relationship_type": "PRIMARY_ASK",
            "strongest_evidence_tier": best,
            "evidence_tiers": sorted(p["evidence_tiers"]),
            "evidence_ids": sorted(p["evidence_ids"]),
            "source_occurrence_ids": sorted(p["source_occurrence_ids"]),
            "why_release_ready": sorted(p["reasons"]),
        })
    excluded.extend(dropped)

    comp = {}
    for r in out:
        comp[r["strongest_evidence_tier"]] = comp.get(
            r["strongest_evidence_tier"], 0) + 1
    byex = {}
    for r in out:
        byex[r["examiner"]] = byex.get(r["examiner"], 0) + 1

    exr = {}
    for e in excluded:
        exr[e["reason"]] = exr.get(e["reason"], 0) + 1

    payload = {
        "note": ("Connection-only publication set. Every record is one unique "
                 "examiner-question relationship whose examiner provenance and "
                 "canonical target are both defensible. No answer-writing "
                 "depends on this set, and nothing here is published by this "
                 "session."),
        "unique_pairs": len(out),
        "evidence_composition": dict(sorted(comp.items())),
        "per_examiner": dict(sorted(byex.items())),
        "excluded_reasons": dict(sorted(exr.items(), key=lambda kv: (-kv[1], kv[0]))),
        "connections": out,
    }
    dump(payload, "RELEASE_A_CONNECTIONS.json")
    dump({"note": "Why each candidate pair did not reach Release A.",
          "excluded": excluded}, "RELEASE_A_EXCLUSIONS.json")
    return payload, excluded


# ---------------------------------------------------------------- gaps and P0

def build_gaps(d):
    """Recompute the gap set with the Notes in the coverage universe.

    A genuine gap is one a candidate could not close from existing QB material
    PLUS the relevant Oral Notes. That is a strictly harder test than the QB-only
    gap set, and it is the test the Laptop's review required, because its two
    NOT_A_GAP findings were both answered by a Notes page.
    """
    notes = d["notes"]
    rank = {t: i for i, t in enumerate(NOTES_TIERS)}
    out = []
    for g in d["gaps"]:
        sids = g["source_ids"]
        tiers = [notes[s]["notes_support"] for s in sids if s in notes]
        best = max(tiers, key=lambda t: rank[t]) if tiers else "NO_NOTES_SUPPORT"
        units = []
        for s in sids:
            for u in notes.get(s, {}).get("notes_units", [])[:2]:
                key = (u["file"], u["anchor"])
                if key not in [(x["file"], x["anchor"]) for x in units]:
                    units.append({"file": u["file"], "anchor": u["anchor"],
                                  "section_title": u["section_title"],
                                  "note_unit_id": u["note_unit_id"],
                                  "notes_support": u["notes_support"]})
        units = sorted(units, key=lambda u: (u["file"], u["anchor"]))[:4]

        material_notes = rank[best] >= rank["NOTES_PARTIAL_SUPPORT"]
        strong_notes = rank[best] >= rank["NOTES_STRONG_SUPPORT"]
        near = g.get("nearest_coverage") or 0.0

        if strong_notes and g["gap_kind"] == "GENUINE_GAP":
            action, kind = "P0_NOTES_TO_QB_PROMOTION", "NOTES_COVERED_GAP"
        elif g["gap_kind"] == "MATERIAL_PARTIAL" or near >= 0.40:
            action, kind = "P0_ENRICH_EXISTING_QB", "MATERIAL_PARTIAL"
        elif material_notes and near >= 0.25:
            action, kind = "P0_ENRICH_EXISTING_QB", "MATERIAL_PARTIAL"
        else:
            action, kind = "P0_NEW_ANSWER", "GENUINE_GAP"

        row = dict(g)
        row["notes_support"] = best
        row["notes_units"] = units
        row["final_gap_kind"] = kind
        row["production_action"] = action
        row["notes_changed_verdict"] = (kind != "GENUINE_GAP"
                                        and g["gap_kind"] == "GENUINE_GAP")
        out.append(row)

    out.sort(key=lambda r: r["gap_id"])
    k = {}
    for r in out:
        k[r["final_gap_kind"]] = k.get(r["final_gap_kind"], 0) + 1
    a = {}
    for r in out:
        a[r["production_action"]] = a.get(r["production_action"], 0) + 1
    payload = {
        "note": ("Gap families after the Notes are in the coverage universe. "
                 "A genuine gap is one a candidate could not close from the "
                 "existing QB answer plus the relevant Oral Notes."),
        "families": len(out),
        "final_gap_kinds": dict(sorted(k.items())),
        "production_actions": dict(sorted(a.items())),
        "verdict_changed_by_notes": sum(1 for r in out
                                        if r["notes_changed_verdict"]),
        "gaps": out,
    }
    dump(payload, "FINAL_ORAL_GAP_CANDIDATES.json")
    return payload


def build_p0(d, gaps):
    """The smallest high-value batch, ranked on stated factors only.

    P0 is not "everything missing". It is what a candidate sitting on 24 August
    still cannot answer from QB plus Notes, ranked by how many examiners ask it
    and how often. Human adjudications are read from P0_ADJUDICATIONS.json and
    applied here, so a judgement is auditable as a judgement and never arrives
    as a silently edited count.
    """
    rank = {t: i for i, t in enumerate(NOTES_TIERS)}
    adj = d["adj"]
    by_id = {g["gap_id"]: g for g in gaps["gaps"]}

    merged_away, applied = {}, []
    for gid, a in sorted(adj.items()):
        if a["decision"] == "MERGE_INTO":
            merged_away[gid] = a["merge_into"]

    cand = []
    for g in gaps["gaps"]:
        gid = g["gap_id"]
        if gid in merged_away:
            continue
        a = adj.get(gid)
        prio, action = g["priority"], g["production_action"]
        target = g.get("nearest_existing_question")
        if a:
            dec = a["decision"]
            applied.append({"gap_id": gid, "decision": dec,
                            "reason": a["reason"],
                            "evidence": a.get("evidence", [])})
            if dec in ("DEMOTE_P1", "HUMAN_REVIEW"):
                continue
            prio = "P0"
            action = dec
            target = a.get("reuse_target", target)
        if prio != "P0":
            continue
        g = dict(g)
        g["production_action"] = action
        g["reuse_target"] = target
        g["adjudicated"] = bool(a)
        # An absorbing family carries the merged family's occurrences with it.
        absorbed = [k for k, v in sorted(merged_away.items()) if v == gid]
        if absorbed:
            for k in absorbed:
                other = by_id[k]
                g["source_ids"] = sorted(set(g["source_ids"] +
                                             other["source_ids"]))
                g["source_wordings"] = (g["source_wordings"] +
                                        other["source_wordings"])
                g["examiners"] = sorted(set(g["examiners"] +
                                            other["examiners"]))
            g["examiner_count"] = len(g["examiners"])
            g["occurrence_count"] = len(g["source_ids"])
            g["absorbed_families"] = absorbed
        cand.append(g)

    def score(g):
        return (g["examiner_count"] >= 2,
                g["occurrence_count"],
                g["examiner_count"],
                rank[g["notes_support"]] >= rank["NOTES_STRONG_SUPPORT"])

    cand.sort(key=lambda g: (score(g), g["gap_id"]), reverse=True)
    p0, overflow = cand[:20], cand[20:]

    items = []
    for g in p0:
        items.append({
            "production_id": "P0-%s" % g["gap_id"].split("-")[-1],
            "gap_id": g["gap_id"],
            "absorbed_families": g.get("absorbed_families", []),
            "proposed_canonical_question": g["proposed_canonical_question"],
            "examiners": g["examiners"],
            "examiner_count": g["examiner_count"],
            "source_occurrence_ids": g["source_ids"],
            "raw_source_wordings": g["source_wordings"],
            "occurrence_count": g["occurrence_count"],
            "topics": g["topics"],
            "current_closest_qb": g.get("reuse_target"),
            "closest_existing_text": g.get("nearest_existing_text"),
            "canonical_coverage": g.get("nearest_coverage"),
            "best_answer_coverage": g.get("best_answer_coverage"),
            "notes_support": g["notes_support"],
            "recommended_miw_sources_to_reuse": g["notes_units"],
            "existing_examiner_evidence": sorted(set(g["examiners"])),
            "production_action": g["production_action"],
            "why_current_miw_would_materially_fail": g.get("priority_factors",
                                                           []),
            "adjudicated": g["adjudicated"],
            "priority_rationale": (
                "%d examiner(s), %d source occurrence(s); notes support %s; "
                "closest canonical coverage %.2f"
                % (g["examiner_count"], g["occurrence_count"],
                   g["notes_support"], g.get("nearest_coverage") or 0.0)),
        })

    by_action = {}
    for i in items:
        by_action.setdefault(i["production_action"], []).append(
            i["production_id"])
    demoted = sorted(a["gap_id"] for a in adj.values()
                     if a["decision"] in ("DEMOTE_P1", "HUMAN_REVIEW"))
    payload = {
        "note": ("The smallest defensible pre-24-August batch. Every item "
                 "carries exactly one production action; MISSING is never left "
                 "as the instruction."),
        "p0_count": len(items),
        "by_production_action": {k: sorted(v) for k, v in
                                 sorted(by_action.items())},
        "adjudications_applied": applied,
        "merged_families": dict(sorted(merged_away.items())),
        "demoted_or_referred": demoted,
        "overflow_beyond_ceiling": sorted(g["gap_id"] for g in overflow),
        "items": items,
    }
    dump(payload, "FINAL_P0_PRODUCTION_BATCH.json")
    return payload


# ---------------------------------------------------------------- residue

def build_human_review(d):
    q = d["hrq"]
    reasons = {}
    for r in q:
        reasons[r["reason"]] = reasons.get(r["reason"], 0) + 1
    rows = []
    for r in sorted(q, key=lambda x: x["source_id"]):
        row = dict(r)
        row["notes_support"] = d["notes"][r["source_id"]]["notes_support"]
        rows.append(row)
    payload = {
        "note": ("Occurrences the matcher refused to decide. A terse acronym is "
                 "not forced to a target: an unresolved row costs a review, a "
                 "wrongly resolved one costs a candidate."),
        "total": len(rows),
        "by_reason": dict(sorted(reasons.items())),
        "items": rows,
    }
    dump(payload, "FINAL_HUMAN_REVIEW_QUEUE.json")
    return payload


# What each research tier implies the published index should render. The map is
# stated rather than inferred so a tier can never quietly gain a display form.
RESEARCH_TO_DISPLAY = {
    "PRIMARY_CONFIRMED": "confirmed",
    "MULTI_SOURCE_CONFIRMED": "confirmed",
    "CE_TIP": "ce_tip",
    "INFERRED_ONLY": "inferred",
    "HEADER": "header",
}


def build_retiering(d):
    """Research-only proposed tiers. Nothing is published.

    Two distinct things are reported separately, because conflating them is how
    "197 pairs would change tier" turns into a claim nobody can check:

      a *repair*   - the published tier is not a valid literal at all, so the
                     row silently vanishes the first time a filter is used;
      a *proposal* - the tier is valid but is not what the evidence supports.

    The one rule that governs both: a tier may never outrun its own provenance.
    The published index, the July sheets, a topic inference and a weak note
    mention are each evidence of something, and none of them is the tracker.
    """
    repairs, proposals = [], []
    for r in d["rel"]:
        cur, rep = r.get("current_tier"), r.get("repaired_tier")
        best = r.get("research_best_tier")
        implied = RESEARCH_TO_DISPLAY.get(best)
        if cur != rep:
            repairs.append({
                "relationship_id": r["relationship_id"],
                "examiner": r["examiner"],
                "canonical_question_id": r["question_id"],
                "old_tier": cur,
                "new_tier": rep,
                "reason": ("published tier is not a valid literal, so the row "
                           "has no filter toggle and disappears on first use"),
                "strongest_valid_provenance": best,
            })
        if implied and implied != cur and cur == rep:
            proposals.append({
                "relationship_id": r["relationship_id"],
                "examiner": r["examiner"],
                "canonical_question_id": r["question_id"],
                "old_tier": cur,
                "new_tier": implied,
                "strongest_valid_provenance": best,
                "primary_evidence_count": r.get("primary_evidence_count", 0),
                "derived_sibling_evidence_count":
                    r.get("derived_sibling_evidence_count", 0),
                "reason": ("published tier does not match the strongest "
                           "provenance the evidence ledger holds for this pair"),
            })
    repairs.sort(key=lambda x: x["relationship_id"])
    proposals.sort(key=lambda x: x["relationship_id"])

    def trans(rows):
        t = {}
        for x in rows:
            k = "%s -> %s" % (x["old_tier"], x["new_tier"])
            t[k] = t.get(k, 0) + 1
        return dict(sorted(t.items(), key=lambda kv: (-kv[1], kv[0])))

    # A promotion to confirmed that no primary evidence supports is exactly the
    # escape mutation M5 proved was possible, so it is counted, not assumed absent.
    unsupported = [x["relationship_id"] for x in proposals
                   if x["new_tier"] == "confirmed"
                   and not x["primary_evidence_count"]]

    payload = {
        "note": ("RESEARCH ONLY - not published. CURRENT_INDEX_RECOVERY, "
                 "JULY_DERIVED_SIBLING, TOPIC_INFERRED and NOTE_WEAK_MENTION "
                 "can never become PRIMARY_TRACKER."),
        "invalid_literal_repairs": len(repairs),
        "repair_transitions": trans(repairs),
        "proposed_changes": len(proposals),
        "proposal_transitions": trans(proposals),
        "proposed_confirmed_without_primary_evidence": len(unsupported),
        "proposed_confirmed_without_primary_evidence_ids": unsupported[:20],
        "repairs": repairs,
        "proposals": proposals,
    }
    dump(payload, "FINAL_RETIERING_PROPOSAL.json")
    return payload


# ---------------------------------------------------------------- display text

EXAMINERS = ("Simon", "Nair", "Paul", "John", "Rajappan", "Srivastava",
             "Senthil")
# Two distinct leaks, and a row can carry both. A production question number
# ("Q18:") is internal ordering that contradicts the live anchor; an examiner
# name in the display text contradicts the row's own examiner heading when the
# index renders that question under a different examiner.
QNUM = re.compile(r"^\s*Q\d+\s*[:.\-—]\s*")
NAME = re.compile("(?<![A-Za-z])(" + "|".join(EXAMINERS) + ")(?![A-Za-z])")


def build_display_text(d):
    """Candidate-facing text carrying internal production vocabulary.

    A row reading "Q12: Simon - SWOT analysis" under a Nair heading contradicts
    its own examiner. Reported as candidates only; no live file is edited here.
    """
    rows = []
    for qid, q in sorted(d["inv"].items()):
        text = q.get("question_text", "")
        qnum = QNUM.match(text)
        name = NAME.search(text)
        if not (qnum or name):
            continue
        problems = []
        if qnum:
            problems.append("opens with an internal production question number")
        if name:
            problems.append("names an examiner in candidate-facing text")
        clean = QNUM.sub("", text).strip()
        if name:
            clean = NAME.sub("", clean)
            clean = re.sub(r"^\s*[—-]\s*", "", clean).strip()
        clean = re.sub(r"\s{2,}", " ", clean).strip()
        clean = clean.strip("—- ")
        f, a = (qid.split("#", 1) + [""])[:2]
        # A stray markdown fence or an "Examiner context:" preamble is not
        # a question that lost its metadata; it is production notes that
        # reached the candidate surface whole. Stripping the name leaves
        # prose that still is not an ask, so these are marked for authoring
        # rather than handed a replacement a generator might apply.
        stray = ("**" in text or "Examiner context" in text)
        if stray:
            problems.append("carries unrendered production markup or an "
                            "internal examiner-context preamble")
        rows.append({
            "canonical_question_id": qid,
            "file": f if f.endswith(".html") else f + ".html",
            "anchor": a,
            "current_text": text,
            "problem": "; ".join(problems),
            "examiner_metadata_to_separate": name.group(1) if name else None,
            "proposed_candidate_text": None if stray else (clean or text),
            "requires_human_rewrite": stray,
        })
    files = {}
    for r in rows:
        files[r["file"]] = files.get(r["file"], 0) + 1
    payload = {
        "note": ("Correction candidates only. No live QB file is modified by "
                 "this session. The examiner-index V2 generator must reject "
                 "any display text of these shapes at build time rather than "
                 "render it verbatim."),
        "count": len(rows),
        "by_file": dict(sorted(files.items())),
        "carrying_examiner_name": sum(1 for r in rows
                                      if r["examiner_metadata_to_separate"]),
        "requiring_human_rewrite": sum(1 for r in rows if r["requires_human_rewrite"]),
        "rows": rows,
    }
    dump(payload, "DISPLAY_TEXT_CORRECTION_CANDIDATES.json")
    return payload



# ---------------------------------------------------------------- final 788

def build_final_788(d):
    rows = []
    for sid in sorted(d["rec"]):
        r, n = d["rec"][sid], d["notes"][sid]
        act = production_action(r["content_disposition"], n["notes_support"],
                                r["examiner_mapping_status"])
        rows.append({
            "source_id": sid,
            "examiner": r["examiner"],
            "source_family_id": r["source_family_id"],
            "raw_question_text": r["raw_question_text"],
            "content_disposition": r["content_disposition"],
            "matched_question_id": r.get("matched_question_id"),
            "examiner_mapping_status": r["examiner_mapping_status"],
            "notes_support": n["notes_support"],
            "notes_unit_count": len(n.get("notes_units", [])),
            "production_action": act,
        })
    p = OUT / "FINAL_788_PRODUCTION_DISPOSITION.jsonl"
    with p.open("w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    return rows


def main():
    d = load()
    final = build_final_788(d)
    mv = build_movement(d)
    rel, exc = build_release_a(d)
    gaps = build_gaps(d)
    p0 = build_p0(d, gaps)
    hrq = build_human_review(d)
    rt = build_retiering(d)
    dt = build_display_text(d)

    def tally(rows, key):
        t = {}
        for r in rows:
            t[r[key]] = t.get(r[key], 0) + 1
        return dict(sorted(t.items()))

    print("final 788 rows              %d" % len(final))
    print("  content dispositions      %s" % tally(final, "content_disposition"))
    print("  notes support             %s" % tally(final, "notes_support"))
    print("  production actions        %s" % tally(final, "production_action"))
    print("movement changed/retarget   %d / %d"
          % (mv["disposition_changed"], mv["target_changed_only"]))
    print("  reasons                   %s" % mv["reason_breakdown"])
    print("release A unique pairs      %d" % rel["unique_pairs"])
    print("  evidence composition      %s" % rel["evidence_composition"])
    print("  per examiner              %s" % rel["per_examiner"])
    print("gap families                %d %s"
          % (gaps["families"], gaps["final_gap_kinds"]))
    print("  actions                   %s" % gaps["production_actions"])
    print("  verdict changed by notes  %d" % gaps["verdict_changed_by_notes"])
    print("P0 items                    %d %s"
          % (p0["p0_count"], p0["by_production_action"]))
    print("human review                %d %s" % (hrq["total"], hrq["by_reason"]))
    print("retiering proposals         %d" % rt["proposed_changes"])
    print("display-text candidates     %d" % dt["count"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
