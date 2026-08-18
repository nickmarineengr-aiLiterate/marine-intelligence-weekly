"""Phase 2A-ii - what the Notes layer would move, reported not committed.

This is an ANALYSIS. It does not recompute the 788 reconciliation, does not
touch the canonical QB, and produces no P0 list. Phase 2A-iii performs the
definitive recomputation; this report exists so the Founder can see the
expected movement before authorising it.

Writes:
    ORAL_NOTES_IMPACT.md              the targeted coverage report
    ORAL_NOTES_P0_IMPACT.json         the old 15 P0 gaps against the Notes
    ORAL_NOTES_REVERSE_CONNECTIONS.json  what Notes add to existing links

    PYTHONIOENCODING=utf-8 python tools/oral/report_notes_impact.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402
import notes_coverage as C  # noqa: E402

OUT = L.OUT

# What a gap's Notes support implies for future production. These are
# CANDIDATE dispositions for Phase 2A-iii to decide, never decisions.
D_PROMOTE = "NOTES_TO_QB_PROMOTION_CANDIDATE"
D_ENRICH = "ENRICH_EXISTING_CANDIDATE"
D_NEW = "NEW_ANSWER_CANDIDATE"
D_UNCHANGED = "NOTES_DO_NOT_CHANGE_GAP"

# Reverse-connection classes: what a Note adds to an examiner link MIW already
# holds, or would create.
R_STRONGER = "ALREADY_HAS_STRONGER_EVIDENCE"
R_ADDS = "NOTE_ADDS_SUPPORT"
R_NEW = "NOTE_CREATES_NEW_EXPLICIT_CONNECTION"
R_CONFLICT = "NOTE_CONFLICTS"
R_UNRESOLVED = "NOTE_UNRESOLVED"


def jsonl(name):
    return [json.loads(l) for l in (OUT / name).open(encoding="utf-8")]


def disposition(notes_support, canonical):
    """The future production disposition a gap's Notes support suggests.

    TOPIC support is deliberately NOT treated as material. A topic-level hit
    means the unit shares a subject area, which is how a page-level reading
    concludes that "D-2 appears in 4 Notes pages" answers a specific D-2 ask.
    It does not: the Nairobi Wreck Removal topic shares vocabulary with a
    medical-certificate ask and answers none of it. Only PARTIAL and above is
    treated as reusable material.
    """
    if notes_support == C.COMPLETE_SUPPORT:
        # MIW already holds the answer; it is simply not a canonical QB card.
        return D_PROMOTE if canonical == "MISSING" else D_ENRICH
    if notes_support in (C.STRONG_SUPPORT, C.PARTIAL_SUPPORT):
        return D_ENRICH
    return D_NEW if canonical == "MISSING" else D_UNCHANGED


def main():
    cov = {c["source_id"]: c for c in jsonl("ORAL_NOTES_COVERAGE.jsonl")}
    ev = jsonl("ORAL_NOTES_EXAMINER_EVIDENCE.jsonl")
    units = {u["note_unit_id"]: u for u in jsonl("ORAL_NOTES_UNITS.jsonl")}
    gaps = json.loads((OUT / "ORAL_GAP_CANDIDATES.json").read_text(
        encoding="utf-8"))
    recon = {r["source_id"]: r for r in jsonl("ORAL_788_RECONCILIATION.jsonl")}
    rels = jsonl("CURRENT_EXAMINER_RELATIONSHIPS.jsonl")

    rank = C.SUPPORT_RANK

    # ---- old P0 against the Notes -----------------------------------------
    p0 = [g for g in gaps if g.get("priority") == "P0"]
    p0_rows = []
    for g in sorted(p0, key=lambda g: g["gap_id"]):
        sids = sorted(g["source_ids"])
        best, best_units = C.NO_SUPPORT, []
        for sid in sids:
            c = cov.get(sid)
            if not c:
                continue
            if rank[c["notes_support"]] > rank[best]:
                best = c["notes_support"]
                best_units = c["notes_units"]
        cued = sorted({e["examiner"] for u in best_units
                       for e in ev if e["note_unit_id"] == u["note_unit_id"]})
        p0_rows.append({
            "gap_id": g["gap_id"],
            "examiners": g["examiners"],
            "source_ask": g["proposed_canonical_question"],
            "occurrences": g["occurrence_count"],
            "canonical_disposition": g["dominant_disposition"],
            "canonical_nearest": g.get("nearest_existing_question"),
            "canonical_nearest_coverage": g.get("nearest_coverage"),
            "notes_support": best,
            "notes_units": [
                {"note_unit_id": u["note_unit_id"], "file": u["file"],
                 "anchor": u["anchor"], "section_title": u["section_title"],
                 "url": u["url"], "notes_support": u["notes_support"],
                 "body_coverage": u["body_coverage"],
                 "about_coverage": u["about_coverage"]}
                for u in best_units[:3]],
            "note_examiner_evidence": cued,
            "likely_future_disposition": disposition(
                best, g["dominant_disposition"]),
        })
    # Two gaps whose best Notes evidence is the SAME section are asking around
    # the same material and are merge candidates. Recorded beside the
    # disposition, never instead of it.
    top_unit = {}
    for r in p0_rows:
        if r["notes_units"]:
            top_unit.setdefault(
                r["notes_units"][0]["note_unit_id"], []).append(r["gap_id"])
    for r in p0_rows:
        r["merge_candidates"] = sorted(
            g for u in r["notes_units"][:1]
            for g in top_unit.get(u["note_unit_id"], [])
            if g != r["gap_id"])

    L.jdump({"old_p0_count": len(p0_rows),
             "note": "CANDIDATE dispositions for Phase 2A-iii. Not a P0 list.",
             "items": p0_rows}, "ORAL_NOTES_P0_IMPACT.json")

    # ---- reverse connections ----------------------------------------------
    # What does a Note add to an examiner link the canonical layer already
    # proposes? Published nothing: this is a candidate set.
    existing = defaultdict(set)
    for r in rels:
        existing[r["question_id"]].add(r["examiner"])

    reverse = []
    for sid in sorted(cov):
        c = cov[sid]
        qid = c["canonical_question_id"]
        examiner = c["examiner"]
        if not c["notes_units_naming_this_examiner"]:
            continue
        if qid is None:
            cls = R_NEW if c["notes_support"] != C.NO_SUPPORT else R_UNRESOLVED
        elif examiner in existing.get(qid, ()):
            cls = R_STRONGER
        elif rank[c["notes_support"]] >= rank[C.PARTIAL_SUPPORT]:
            cls = R_ADDS
        else:
            cls = R_UNRESOLVED
        reverse.append({
            "source_id": sid, "examiner": examiner,
            "canonical_question_id": qid,
            "canonical_disposition": c["canonical_disposition"],
            "notes_support": c["notes_support"],
            "note_units": c["notes_units_naming_this_examiner"],
            "reverse_class": cls,
        })
    L.jdump({"note": "Candidate connections. Nothing is published in 2A-ii.",
             "classes": dict(sorted(Counter(
                 r["reverse_class"] for r in reverse).items())),
             "unique_examiner_question_pairs": len(
                 {(r["examiner"], r["canonical_question_id"])
                  for r in reverse if r["canonical_question_id"]}),
             "rows": reverse}, "ORAL_NOTES_REVERSE_CONNECTIONS.json")

    # ---- the targeted coverage report -------------------------------------
    support = Counter(c["notes_support"] for c in cov.values())
    matrix = defaultdict(Counter)
    for c in cov.values():
        matrix[c["canonical_disposition"]][c["notes_support"]] += 1

    lines = []
    w = lines.append
    w("# Phase 2A-ii - Oral Notes impact on the 788 source occurrences")
    w("")
    w("An analysis, not a baseline. The committed reconciliation is still the")
    w("Phase 2 one; Phase 2A-iii performs the definitive recomputation.")
    w("")
    w("## Notes support across all source occurrences")
    w("")
    w("| Notes support | Occurrences |")
    w("|---|---|")
    for t in reversed(C.SUPPORT_TIERS):
        w("| %s | %d |" % (t, support.get(t, 0)))
    w("| **total** | **%d** |" % sum(support.values()))
    w("")
    w("## Notes support against the canonical disposition")
    w("")
    w("The two dimensions are independent. A row that is canonically MISSING")
    w("with COMPLETE Notes support is not a gap in MIW's knowledge - it is")
    w("knowledge MIW holds outside the canonical question bank.")
    w("")
    header = ["canonical \\ notes"] + [t.replace("NOTES_", "").replace(
        "_SUPPORT", "") for t in C.SUPPORT_TIERS]
    w("| " + " | ".join(header) + " |")
    w("|" + "---|" * len(header))
    for disp in sorted(matrix):
        row = [disp] + [str(matrix[disp].get(t, 0)) for t in C.SUPPORT_TIERS]
        w("| " + " | ".join(row) + " |")
    w("")
    strong = sum(support.get(t, 0) for t in
                 (C.STRONG_SUPPORT, C.COMPLETE_SUPPORT))
    w("**%d** occurrences have strong or complete Notes support; **%d** have "
      "no Notes support at all." % (strong, support.get(C.NO_SUPPORT, 0)))
    w("")
    w("## Old P0 gaps against the Notes")
    w("")
    w("| Gap | Examiner | Ask | Canonical | Notes | Likely future disposition |")
    w("|---|---|---|---|---|---|")
    for r in p0_rows:
        w("| %s | %s | %s | %s | %s | %s |" % (
            r["gap_id"], "/".join(r["examiners"]),
            r["source_ask"][:52].replace("|", "/"),
            r["canonical_disposition"],
            r["notes_support"].replace("NOTES_", "").replace("_SUPPORT", ""),
            r["likely_future_disposition"]))
    w("")
    dcount = Counter(r["likely_future_disposition"] for r in p0_rows)
    for k, v in sorted(dcount.items()):
        w("- **%s**: %d" % (k, v))
    w("")
    w("## Reverse connection value")
    w("")
    rcount = Counter(r["reverse_class"] for r in reverse)
    w("| Class | Rows |")
    w("|---|---|")
    for k, v in sorted(rcount.items()):
        w("| %s | %d |" % (k, v))
    w("")
    w("Nothing here is published. Every row is a candidate for Phase 2A-iii.")
    w("")

    p = OUT / "ORAL_NOTES_IMPACT.md"
    p.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print("old P0 analysed: %d" % len(p0_rows))
    for k, v in sorted(dcount.items()):
        print("  %-38s %d" % (k, v))
    print("reverse connection rows: %d" % len(reverse))
    for k, v in sorted(rcount.items()):
        print("  %-38s %d" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
