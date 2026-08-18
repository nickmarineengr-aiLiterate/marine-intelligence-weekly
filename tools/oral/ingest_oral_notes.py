"""Phase 2A-ii - build the Oral Notes secondary layer.

Writes, all research-only, all inside the examiner-audit folder:

    ORAL_NOTES_INVENTORY.json          every page, its series and its role
    ORAL_NOTES_UNITS.jsonl             every note unit
    ORAL_NOTES_EXAMINER_EVIDENCE.jsonl every explicit examiner cue
    ORAL_NOTES_CUE_AUDIT.json          raw / bounded / suppressed cue counts
    ORAL_NOTES_COVERAGE.jsonl          Notes support for all 788 source asks

Nothing here recomputes the canonical reconciliation, changes the 681 canonical
QB questions, or writes a live product file. The 788 coverage pass is an
ANALYSIS: it reports what the Notes layer would move, and Phase 2A-iii performs
the definitive recomputation.

    PYTHONIOENCODING=utf-8 python tools/oral/ingest_oral_notes.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402
import oral_notes as N  # noqa: E402
import notes_coverage as C  # noqa: E402

OUT = L.OUT


def jsonl_dump(rows, name):
    p = OUT / name
    # newline="\n" explicitly: the default translates to CRLF on Windows, so a
    # committed artefact would differ byte-for-byte between platforms
    with p.open("w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    return p


def main():
    files = N.classify_files()
    units = N.build_units()
    alias = json.loads((OUT / "EXAMINER_ALIAS_REGISTER.json").read_text(
        encoding="utf-8"))
    alias_map = N.examiner_aliases(alias)
    cues, raw_counts = N.harvest_cues(alias_map)

    # --- inventory ---------------------------------------------------------
    by_file = Counter(u["file"] for u in units)
    for row in files:
        row["note_units"] = by_file.get(row["file"], 0)
    substantive = [r for r in files if r["role"] == N.ROLE_SUBSTANTIVE]
    inventory = {
        "notes_dir": N.NOTES_DIR.relative_to(L.REPO).as_posix(),
        "html_pages": len(files),
        "substantive_pages": len(substantive),
        "navigation_pages": sum(1 for r in files if r["role"] == N.ROLE_NAVIGATION),
        "out_of_scope_pages": sum(1 for r in files
                                  if r["role"] == N.ROLE_OUT_OF_SCOPE),
        "unclassified_pages": sum(1 for r in files
                                  if r["role"] == N.ROLE_UNCLASSIFIED),
        "total_bytes": sum(r["bytes"] for r in files),
        "substantive_bytes": sum(r["bytes"] for r in substantive),
        "pages_by_series": dict(sorted(Counter(
            r["series"] for r in substantive).items())),
        "units_total": len(units),
        "units_by_level": dict(sorted(Counter(
            u["unit_level"] for u in units).items())),
        "units_by_series": dict(sorted(Counter(
            u["series"] for u in units).items())),
        "answer_bearing_units": sum(1 for u in units if u["answer_bearing"]),
        "files": files,
    }
    L.jdump(inventory, "ORAL_NOTES_INVENTORY.json")
    jsonl_dump(sorted(units, key=lambda u: u["note_unit_id"]),
               "ORAL_NOTES_UNITS.jsonl")

    # --- examiner evidence -------------------------------------------------
    # Only the explicit dispositions become evidence records. A heading
    # mention, an incidental mention and a suppressed non-examiner name are
    # counted in the audit and excluded from the ledger.
    evidence = []
    for i, c in enumerate(sorted(
            cues, key=lambda c: (c["note_unit_id"], c["examiner"],
                                 c["char_offset"], c["cue_disposition"]))):
        if c["cue_disposition"] not in N.EXPLICIT_CUES:
            continue
        rec = dict(c)
        rec["evidence_id"] = "NOTEV-%04d" % (len(evidence) + 1)
        # Provenance, stated and never stronger than this: a Note is a Note.
        rec["evidence_tier"] = N.NOTE_EVIDENCE_TIER
        rec["source_type"] = N.NOTE_SOURCE_TYPE
        rec["source_provenance"] = c["url"]
        evidence.append(rec)
    jsonl_dump(evidence, "ORAL_NOTES_EXAMINER_EVIDENCE.jsonl")

    explicit_pairs = {(e["examiner"], e["note_unit_id"]) for e in evidence}
    audit = {
        "alias_forms": {k: v for k, v in sorted(alias_map.items())},
        "raw_name_hits": {k: raw_counts[k] for k in sorted(raw_counts)},
        "cue_occurrences": len(cues),
        "cue_dispositions": dict(sorted(Counter(
            c["cue_disposition"] for c in cues).items())),
        "cue_vehicles": dict(sorted(Counter(
            c["cue_vehicle"] for c in cues).items())),
        "non_examiner_controls": dict(sorted(Counter(
            c["non_examiner_control"] for c in cues
            if c["non_examiner_control"]).items())),
        "explicit_cue_occurrences": len(evidence),
        "unique_examiner_to_unit_relations": len(explicit_pairs),
        "explicit_by_examiner": dict(sorted(Counter(
            e["examiner"] for e in evidence).items())),
        "unique_units_by_examiner": {
            k: len({u for x, u in explicit_pairs if x == k})
            for k in sorted({x for x, _ in explicit_pairs})},
    }
    L.jdump(audit, "ORAL_NOTES_CUE_AUDIT.json")

    # --- coverage of the 788 source asks -----------------------------------
    idx = C.unit_index(units)
    idf, default = C.idf_over_units(idx)
    src = [json.loads(l) for l in
           (OUT / "ALL_SURVEYORS_SOURCE_RECORDS.jsonl").open(encoding="utf-8")]
    recon = {r["source_id"]: r for r in (
        json.loads(l) for l in
        (OUT / "ORAL_788_RECONCILIATION.jsonl").open(encoding="utf-8"))}

    unit_examiners = defaultdict(set)
    for e in evidence:
        unit_examiners[e["note_unit_id"]].add(e["examiner"])

    coverage = []
    for s in sorted(src, key=lambda s: s["source_id"]):
        toks = C.source_tokens(s)
        hits = C.best_support(toks, idx, idf, default)
        best = hits[0]["notes_support"] if hits else C.NO_SUPPORT
        r = recon.get(s["source_id"], {})
        examiner = s.get("surveyor_normalized")
        # A Notes unit that names THIS examiner is a stronger reason to look at
        # it, but it never raises the support tier: coverage is about content.
        cued = sorted({u for h in hits for u in [h["note_unit_id"]]
                       if examiner in unit_examiners.get(h["note_unit_id"], ())})
        coverage.append({
            "source_id": s["source_id"],
            "examiner": examiner,
            "source_ask": s.get("question_core_text") or s.get("raw_question_text"),
            "source_family_id": s.get("source_family_id"),
            "source_token_count": len(toks),
            # the canonical dimension, carried unchanged for comparison only
            "canonical_disposition": r.get("content_disposition"),
            "canonical_question_id": r.get("matched_question_id"),
            # the Notes dimension, computed here
            "notes_support": best,
            "notes_units": hits,
            "notes_units_naming_this_examiner": cued,
        })
    jsonl_dump(coverage, "ORAL_NOTES_COVERAGE.jsonl")

    matrix = defaultdict(Counter)
    for c in coverage:
        matrix[c["canonical_disposition"]][c["notes_support"]] += 1
    summary = {
        "source_occurrences": len(coverage),
        "notes_support": dict(sorted(Counter(
            c["notes_support"] for c in coverage).items())),
        "notes_support_by_canonical_disposition": {
            k: dict(sorted(v.items())) for k, v in sorted(matrix.items())},
        "occurrences_with_any_support": sum(
            1 for c in coverage if c["notes_support"] != C.NO_SUPPORT),
        "occurrences_with_examiner_cued_unit": sum(
            1 for c in coverage if c["notes_units_naming_this_examiner"]),
        "canonical_questions_unchanged": len(L.build_inventory()),
    }
    L.jdump(summary, "ORAL_NOTES_COVERAGE_SUMMARY.json")

    print("pages %d (substantive %d) | units %d | explicit cues %d | "
          "relations %d" % (inventory["html_pages"],
                            inventory["substantive_pages"], len(units),
                            len(evidence), len(explicit_pairs)))
    print("canonical QB questions: %d" % summary["canonical_questions_unchanged"])
    for k, v in summary["notes_support"].items():
        print("  %-24s %d" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
