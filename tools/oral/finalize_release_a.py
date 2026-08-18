"""Turn the reviewed Release-A research set into the publication set.

RELEASE_A_CONNECTIONS.json is the Phase-2A-iii research artefact the Laptop
final review (f78e2c7) examined. It stays untouched: it is the reviewed input.
This script derives from it - deterministically, from the ledgers, never by
hand - the set the Examiner Index V2 generator is allowed to publish:

  RELEASE_A_PUBLICATION.json   every relationship that may reach a candidate
  RELEASE_A_HELD.json          every reviewed pair that may not, and why

Why a separate step rather than a patched artefact
--------------------------------------------------
The final review found `evidence_ids` empty on all 136 rows, which made two
validator checks vacuous. Tracing the cause showed something larger than a
missing lookup: `build_final_package.py` Route 1 stamped `PRIMARY_TRACKER` on
every pair whose *readiness status* was READY_VERIFIED*, and that status was
granted to page-prose CE-tip pairs on the strength of a "corroborating" 788
record computed against a *pre-recompute* reconciliation. After the 2A-iii
recompute those records point at other questions. Readiness is not
provenance. So the tier is recomputed here from the evidence records that
actually name this examiner and this question, and a pair whose evidence no
longer reaches the release floor is HELD - not kept for the sake of a count.

Evidence a pair may carry (all record ids are real, none are minted here):

  MASTER-AQ-* / JULY-*   EXAMINER_EVIDENCE_LEDGER.jsonl rows whose
                         examiner_normalized and canonical_question_id are
                         this pair and whose legacy_mapping is VERIFIED_* -
                         the same admissibility reconcile_evidence.py used.
                         PRIMARY_CANDIDATE_RECORD rows carry PRIMARY_TRACKER;
                         DERIVED_PRODUCT_SURFACE rows are recorded as
                         corroboration and never raise a tier.
  ASC-*                  FINAL_788_PRODUCTION_DISPOSITION rows of the same
                         examiner whose final target is this question at
                         EXACT_MATCH or NEAR_MATCH -> EXTERNAL_SOURCE_CONFIRMED.
                         Weaker dispositions are recorded as weak
                         corroboration and never raise a tier.
  NOTEV-*                ORAL_NOTES_EXAMINER_EVIDENCE rows reached through a
                         NOTE_CREATES_NEW_EXPLICIT_CONNECTION reverse
                         connection over an EXACT/NEAR target -> NOTE_EXPLICIT.

A pair already published in the current index is not a new relationship. It
is emitted with disposition EVIDENCE_FOR_EXISTING so the generator merges the
evidence into the existing row instead of rendering a duplicate.

Portability: repo-relative through oral_lib; no drive letters, no timestamps.
    PYTHONIOENCODING=utf-8 python tools/oral/finalize_release_a.py
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

OUT = L.OUT

# Weakest to strongest. Mirrors build_final_package.EVIDENCE_RANK for the
# tiers a Release-A pair can hold after reconstruction.
RANK = {
    "CE_TIP": 2,
    "NOTE_EXPLICIT": 3,
    "EXTERNAL_SOURCE_CONFIRMED": 4,
    "PRIMARY_TRACKER": 5,
}
RELEASE_FLOOR = 3          # NOTE_EXPLICIT and above may carry a pair
ADMISSIBLE_MAPPING = ("VERIFIED_MATCH", "VERIFIED_SAME_CORE")
STRONG_788 = ("EXACT_MATCH", "NEAR_MATCH")


def jl(name):
    p = OUT / name
    with p.open(encoding="utf-8") as fh:
        return [json.loads(x) for x in fh if x.strip()]


def js(name):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def dump(obj, name):
    (OUT / name).write_text(
        json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=False) + "\n",
        encoding="utf-8", newline="\n")


def build_evidence_index():
    """(examiner, canonical_question_id) -> evidence buckets."""
    prim = defaultdict(list)      # PRIMARY_CANDIDATE_RECORD, verified mapping
    derived = defaultdict(list)   # DERIVED_PRODUCT_SURFACE, verified mapping
    for r in jl("EXAMINER_EVIDENCE_LEDGER.jsonl"):
        qid = r.get("canonical_question_id")
        if not qid or r.get("legacy_mapping") not in ADMISSIBLE_MAPPING:
            continue
        key = (r["examiner_normalized"], qid)
        if r["evidence_class"] == "PRIMARY_CANDIDATE_RECORD":
            prim[key].append(r["evidence_id"])
        else:
            derived[key].append(r["evidence_id"])

    ext = defaultdict(list)       # EXACT / NEAR occurrences
    weak = defaultdict(list)      # PARTIAL / AMBIGUOUS / SAME_CORE occurrences
    for r in jl("FINAL_788_PRODUCTION_DISPOSITION.jsonl"):
        qid = r.get("matched_question_id")
        if not qid or r["content_disposition"] == "MISSING":
            continue
        key = (r["examiner"], qid)
        (ext if r["content_disposition"] in STRONG_788 else weak)[key].append(
            r["source_id"])

    nev_by_unit = defaultdict(list)
    for e in jl("ORAL_NOTES_EXAMINER_EVIDENCE.jsonl"):
        nev_by_unit[e["note_unit_id"]].append(e)
    note = defaultdict(list)
    for r in js("ORAL_NOTES_REVERSE_CONNECTIONS.json")["rows"]:
        if r.get("reverse_class") != "NOTE_CREATES_NEW_EXPLICIT_CONNECTION":
            continue
        if r.get("canonical_disposition") not in STRONG_788:
            continue
        key = (r["examiner"], r["canonical_question_id"])
        for u in r.get("note_units", []):
            for e in nev_by_unit.get(u, []):
                if e["examiner"] == r["examiner"]:
                    note[key].append(e["evidence_id"])

    def uniq(d):
        return {k: sorted(set(v)) for k, v in d.items()}

    return uniq(prim), uniq(derived), uniq(ext), uniq(weak), uniq(note)


def main():
    research = js("RELEASE_A_CONNECTIONS.json")
    decisions = js("RELEASE_A_REVIEW_DECISIONS.json")
    held_by_review = {h["relation_id"]: h for h in decisions["held"]}
    current = {(r["examiner"], r["question_id"]): r
               for r in jl("CURRENT_EXAMINER_RELATIONSHIPS.jsonl")}
    inv = {q["canonical_question_id"]: q for q in L.build_inventory()}
    anchors = L.all_anchors()
    prim, derived, ext, weak, note = build_evidence_index()

    published, held = [], []
    for c in research["connections"]:
        key = (c["examiner"], c["canonical_question_id"])
        p, d, e, w, n = (prim.get(key, []), derived.get(key, []),
                         ext.get(key, []), weak.get(key, []), note.get(key, []))
        tiers = []
        if p:
            tiers.append("PRIMARY_TRACKER")
        if e:
            tiers.append("EXTERNAL_SOURCE_CONFIRMED")
        if n:
            tiers.append("NOTE_EXPLICIT")
        best = max(tiers, key=RANK.get) if tiers else None
        evidence_ids = sorted(set(p) | set(e) | set(n))
        diag = {
            "relation_id": c["relation_id"],
            "examiner": c["examiner"],
            "canonical_question_id": c["canonical_question_id"],
            "research_tier": c["strongest_evidence_tier"],
            "reconstructed_tier": best,
            "primary_evidence_ids": p,
            "external_evidence_ids": e,
            "note_evidence_ids": n,
            "derived_corroboration_ids": d,
            "weak_corroboration_ids": w,
        }

        if c["relation_id"] in held_by_review:
            h = held_by_review[c["relation_id"]]
            held.append(dict(diag, decision=h["decision"], reason=h["reason"],
                             authority=decisions["review_ref"]))
            continue
        if best is None or RANK[best] < RELEASE_FLOOR:
            held.append(dict(
                diag, decision="HOLD_EVIDENCE_BELOW_FLOOR",
                reason=("after evidence reconstruction no record at or above "
                        "the release floor names this examiner and this "
                        "question; the research tier rested on a readiness "
                        "status, not on provenance"),
                authority="finalize_release_a.py"))
            continue
        q = inv.get(c["canonical_question_id"])
        if q is None or c["anchor"] not in anchors.get(c["file"], set()):
            held.append(dict(diag, decision="HOLD_TARGET_UNRESOLVED",
                             reason="target does not resolve on the live QB",
                             authority="finalize_release_a.py"))
            continue

        existing = current.get(key)
        published.append({
            "relation_id": c["relation_id"],
            "examiner": c["examiner"],
            "canonical_question_id": c["canonical_question_id"],
            "file": c["file"],
            "anchor": c["anchor"],
            "url": c["url"],
            "disposition": ("EVIDENCE_FOR_EXISTING" if existing
                            else "NEW_RELATIONSHIP"),
            "existing_relationship_id": (existing["relationship_id"]
                                         if existing else None),
            "relationship_type": c["relationship_type"],
            "strongest_evidence_tier": best,
            "research_tier": c["strongest_evidence_tier"],
            "retiered": best != c["strongest_evidence_tier"],
            "evidence_tiers": sorted(tiers, key=RANK.get),
            "evidence_ids": evidence_ids,
            "primary_evidence_ids": p,
            "external_evidence_ids": e,
            "note_evidence_ids": n,
            "source_occurrence_ids": e,
            "derived_corroboration_ids": d,
            "weak_corroboration_ids": w,
        })

    def tally(rows, key):
        out = defaultdict(int)
        for r in rows:
            out[key(r)] += 1
        return dict(sorted(out.items()))

    new_rows = [r for r in published if r["disposition"] == "NEW_RELATIONSHIP"]
    payload = {
        "note": ("Publication-ready Release A, derived from the reviewed research "
                 "set by finalize_release_a.py. Every evidence id is a real "
                 "record; every tier is recomputed from those records; a pair "
                 "already in the current index is emitted as evidence for the "
                 "existing relationship, not as a new row."),
        "research_input": "RELEASE_A_CONNECTIONS.json",
        "review_ref": decisions["review_ref"],
        "research_pairs": len(research["connections"]),
        "published_pairs": len(published),
        "new_relationships": len(new_rows),
        "evidence_for_existing": len(published) - len(new_rows),
        "held_pairs": len(held),
        "composition_published": tally(published, lambda r: r["strongest_evidence_tier"]),
        "composition_new": tally(new_rows, lambda r: r["strongest_evidence_tier"]),
        "per_examiner_new": tally(new_rows, lambda r: r["examiner"]),
        "retiered": tally([r for r in published if r["retiered"]],
                          lambda r: "%s -> %s" % (r["research_tier"],
                                                  r["strongest_evidence_tier"])),
        "held_reasons": tally(held, lambda r: r["decision"]),
        "connections": published,
    }
    dump(payload, "RELEASE_A_PUBLICATION.json")
    dump({"note": ("Reviewed Release-A pairs that may not reach a candidate, with "
                   "the evidence actually found for each. Nothing here is deleted "
                   "from research history."),
          "review_ref": decisions["review_ref"],
          "held_pairs": len(held),
          "held_reasons": tally(held, lambda r: r["decision"]),
          "held": held}, "RELEASE_A_HELD.json")

    print("research pairs      %d" % payload["research_pairs"])
    print("published           %d  (new %d, evidence-for-existing %d)" % (
        payload["published_pairs"], payload["new_relationships"],
        payload["evidence_for_existing"]))
    print("composition (new)   %s" % payload["composition_new"])
    print("per examiner (new)  %s" % payload["per_examiner_new"])
    print("retiered            %s" % payload["retiered"])
    print("held                %d  %s" % (payload["held_pairs"], payload["held_reasons"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
