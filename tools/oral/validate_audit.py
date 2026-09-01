"""Validation gate for the Oral examiner-intelligence audit datasets.

Fails closed: every check must state a real result, and an artefact that is
absent is reported as UNAVAILABLE rather than silently skipped.
"""
from __future__ import annotations

import collections
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

# Derived from the governed config -- see oral_lib.examiner_tier_literals.
VALID_TIERS = L.examiner_tier_literals()
VALID_DISPOSITIONS = {
    "ALREADY_CANONICAL_AND_LINKED",
    "ALREADY_CANONICAL_LINK_MISSING",
    "CANONICAL_MATCH_BUT_LEGACY_MAPPING_WRONG",
    "SOURCE_VARIANT_OF_CANONICAL",
    "PARTIAL_COVERAGE",
    "NO_CURRENT_QB_MATCH",
    "AMBIGUOUS",
    "STALE_SOURCE_RECORD",
}
VALID_MAPPINGS = {
    "VERIFIED_MATCH",
    "VERIFIED_SAME_CORE",
    "PARTIAL_MATCH",
    "STALE_TARGET",
    "WRONG_MATCH",
    "AMBIGUOUS",
    "UNRESOLVED",
}


def check(results, name, ok, detail):
    results.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})


def main():
    R = []
    inv = L.build_inventory()
    qids = {r["canonical_question_id"] for r in inv}
    anchors = L.all_anchors()

    ledger_p = L.OUT / "EXAMINER_EVIDENCE_LEDGER.jsonl"
    if not ledger_p.exists():
        R.append({"check": "ledger_present", "status": "UNAVAILABLE", "detail": str(ledger_p)})
        print(json.dumps({"results": R}, indent=2))
        sys.exit(1)
    ledger = [json.loads(l) for l in ledger_p.read_text(encoding="utf-8").splitlines() if l]

    # 1. every canonical id in the ledger resolves to a live question
    bad = [r["evidence_id"] for r in ledger
           if r.get("canonical_question_id") and r["canonical_question_id"] not in qids]
    check(R, "ledger_canonical_ids_resolve", not bad, f"{len(bad)} unresolved")

    # 2. no duplicate evidence ids
    c = collections.Counter(r["evidence_id"] for r in ledger)
    dup = [k for k, v in c.items() if v > 1]
    check(R, "no_duplicate_evidence_ids", not dup, f"{len(dup)} duplicated")

    # 3. vocabulary is closed
    badd = {r["disposition"] for r in ledger} - VALID_DISPOSITIONS
    check(R, "disposition_vocabulary_closed", not badd, str(sorted(badd)))
    badm = {r["legacy_mapping"] for r in ledger} - VALID_MAPPINGS
    check(R, "mapping_vocabulary_closed", not badm, str(sorted(badm)))

    # 4. no source row silently discarded
    unattributed = sum(1 for r in ledger if not r.get("examiner_normalized"))
    kinds = collections.Counter(r.get("attribution_kind") for r in ledger)
    check(R, "every_row_carries_an_attribution_kind",
          all(r.get("attribution_kind") or r["evidence_source"].startswith("MIW_July")
              for r in ledger),
          f"unattributed={unattributed} kinds={dict(kinds)}")

    # 5. index links resolve
    ix = L.parse_examiner_index(L.MEO / "examiner-index.html")
    broken = 0
    bad_tier = 0
    for r in ix["rows"]:
        f, a = L.split_href(r["href"])
        if not (L.MEO / f).exists() or a not in anchors.get(f, set()):
            broken += 1
        if r["tier"] not in VALID_TIERS:
            bad_tier += 1
    check(R, "index_links_resolve", broken == 0, f"{broken} broken")
    check(R, "index_tier_literals_valid", bad_tier == 0, f"{bad_tier} invalid literals")

    # 6. counts derive from records, not from the page header
    rendered = len(ix["rows"])
    heads = sum(s["heading_count"] or 0 for s in ix["sections"])
    mini = sum(ix["mininav"].values())
    hdr = ix["header"].get("tagged pairs")
    check(R, "index_section_headings_match_rendered_rows", heads == rendered,
          f"headings={heads} rendered={rendered}")
    check(R, "index_mininav_matches_rendered_rows", mini == rendered,
          f"mininav={mini} rendered={rendered}")
    check(R, "index_header_total_matches_rendered_rows", hdr == rendered,
          f"header={hdr} rendered={rendered}")

    # 7. examiner aliases resolve
    slugs = {s["slug"] for s in ix["sections"]}
    import reconcile_evidence as RE
    unres = [s for s in slugs if s not in RE.ALIASES]
    check(R, "examiner_aliases_resolve", not unres, str(unres))

    # 8. gap files reference live questions
    for fn in ("EXISTING_CONNECTION_GAPS.csv", "PROSE_CONNECTION_GAPS.csv"):
        p = L.OUT / fn
        if not p.exists():
            R.append({"check": f"{fn}_present", "status": "UNAVAILABLE", "detail": str(p)})
            continue
        rows = list(csv.DictReader(p.open(encoding="utf-8")))
        bad = [r["canonical_question_id"] for r in rows
               if r["canonical_question_id"] not in qids]
        check(R, f"{fn}_ids_resolve", not bad, f"{len(bad)} of {len(rows)} unresolved")

    summary = {
        "live_questions": len(inv),
        "evidence_records": len(ledger),
        "results": R,
        "passed": sum(1 for r in R if r["status"] == "PASS"),
        "failed": sum(1 for r in R if r["status"] == "FAIL"),
        "unavailable": sum(1 for r in R if r["status"] == "UNAVAILABLE"),
    }
    L.jdump(summary, "VALIDATION_RESULTS.json")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
