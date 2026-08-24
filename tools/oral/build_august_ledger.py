"""Build the ONE aggregate ledger for the current August 2026 oral intake.

Batch 1 left a per-batch report and a per-batch adjudication file, which answers
"what happened in that batch" and cannot answer "where does the August intake
stand". This ledger is that second question, and it is DERIVED - from the intake
store, the adjudication record and the production manifests - so it can never
drift from them the way a hand-maintained status board would.

It deliberately keeps the two denominators apart. The historical 788 is quoted
here only as a constant to be checked, never summed with the August figures.

  PYTHONIOENCODING=utf-8 python tools/oral/build_august_ledger.py [--check]

Exit 0 written / current, 1 stale (with --check), 2 an input was unavailable.
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio      # noqa: E402

enable_utf8_stdio()

OUT = REPO / "meoclass1" / "oral-intelligence" / "examiner-audit"
RECORDS = OUT / "AUGUST2026_INTAKE_RECORDS.jsonl"
REPORT = OUT / "AUGUST2026_INTAKE_REPORT.json"
ADJ = OUT / "AUGUST2026_INTAKE_ADJUDICATIONS.json"
HIST = OUT / "ALL_SURVEYORS_SOURCE_RECORDS.jsonl"
LEDGER = OUT / "AUGUST2026_MASTER_INTAKE_LEDGER.json"

HISTORICAL_EXPECTED = 788

# Which submissions belong to which arrival batch. Batch 1 governed S001-S002;
# S003, S004 and then S005 each arrived appended to the same carrier file later
# the same day - a new submission is a BIGGER FILE, never a new file. A submission missing from this map is a FAILURE, not an "UNKNOWN"
# bucket: S004 was silently bucketed as UNKNOWN on its first build, which is
# exactly how a new submission gets counted in the total while disappearing
# from the per-batch view that a reader actually looks at.
BATCH_OF = {"AUG2026-S001": "AUGUST_BATCH_1",
            "AUG2026-S002": "AUGUST_BATCH_1",
            "AUG2026-S003": "AUGUST_BATCH_2",
            "AUG2026-S004": "AUGUST_BATCH_3",
            "AUG2026-S005": "AUGUST_BATCH_4"}

MATCHED = {"EXACT_EXISTING", "PARAPHRASE_EXISTING"}


def jsonl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def build():
    for p in (RECORDS, REPORT, ADJ, HIST):
        if not p.is_file():
            print("UNAVAILABLE: %s" % p.name)
            return None
    intake = jsonl(RECORDS)
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    adj = {a["occurrence_id"]: a
           for a in json.loads(ADJ.read_text(encoding="utf-8"))["adjudications"]}
    hist = jsonl(HIST)

    manifests = {}
    for mp in sorted(HERE.glob("batch_*_manifest.json")):
        m = json.loads(mp.read_text(encoding="utf-8"))
        for c in m.get("cards", []):
            for oid in c.get("source_occurrence_ids", []) or []:
                if oid.startswith("AUG-"):
                    manifests[oid] = {
                        "batch_id": m.get("batch_id") or m.get("batch"),
                        "action_id": c.get("action_id"),
                        "card": "%s#%s" % (c["file"].replace(".html", ""), c["anchor"]),
                        "action_kind": c.get("action_kind"),
                    }

    by_class = collections.Counter(a["classification"] for a in adj.values())
    unmapped = sorted({o["submission_id"] for o in intake
                       if o["submission_id"] not in BATCH_OF})
    if unmapped:
        print("UNMAPPED SUBMISSION(S): %s - add them to BATCH_OF in %s"
              % (", ".join(unmapped), __file__))
        return None
    by_batch = collections.Counter(BATCH_OF[o["submission_id"]] for o in intake)

    # A "unique ask" is one distinct examinable question the August intake
    # produced, counted once however many occurrences carry it: a new ask, or an
    # existing card an occurrence resolved to.
    asks = {}
    for oid, a in adj.items():
        cls = a["classification"]
        if cls == "NON_QUESTION_UNRECOVERABLE":
            continue
        key = a.get("matched_question_id") or ("NEW::" + (a.get("ask") or oid))
        e = asks.setdefault(key, {"key": key, "occurrences": [], "classes": set(),
                                  "submissions": set()})
        e["occurrences"].append(oid)
        e["classes"].add(cls)
        e["submissions"].add(next((o["submission_id"] for o in intake
                                   if o["occurrence_id"] == oid), "?"))

    multi = sorted(k for k, v in asks.items() if len(v["submissions"]) > 1)
    new_asks = sorted(k for k, v in asks.items()
                      if "GENUINE_NEW_QUESTION" in v["classes"])
    published = sorted(o for o in adj if o in manifests)
    unresolved = sorted(o for o, a in adj.items() if a["classification"] == "AMBIGUOUS")

    ledger = {
        "record_class": "CURRENT_INTAKE_MASTER_LEDGER",
        "generated_by": "tools/oral/build_august_ledger.py",
        "note": (
            "The single aggregate view of the CURRENT August 2026 oral intake. Derived from the "
            "intake store, the adjudication record and the batch manifests - never hand-edited. "
            "The historical 788 appears here only as a constant that is checked, and is never "
            "added to any August figure."),
        "intake_window": "OPEN_EXPECTING_MORE_INPUT",
        "intake_window_note": (
            "The Founder has stated that further surveyor and candidate material is expected. The "
            "window stays open, and the final August workbook stays blocked, until that is "
            "explicitly closed. Processing today's batch is not a reason to close it."),
        "historical_denominator": {
            "raw_occurrences": len(hist),
            "expected": HISTORICAL_EXPECTED,
            "unchanged": len(hist) == HISTORICAL_EXPECTED,
            "note": "Separate lane. August evidence never enters this count.",
        },
        "august": {
            "submissions": report["submissions"],
            "raw_occurrences": len(intake),
            "question_bearing_occurrences": report["question_bearing_occurrences"],
            "non_question_occurrences": report["non_question_occurrences"],
            "examiners_represented": report["examiners_represented"],
            "examiner_roles": report["examiner_roles"],
            "raw_occurrences_by_batch": dict(sorted(by_batch.items())),
            "individually_attributed_occurrences":
                report.get("individually_attributed_occurrences", []),
            "panel_level_occurrences": report.get("panel_level_occurrences"),
        },
        "adjudication": {
            "total": len(adj),
            "by_classification": dict(sorted(by_class.items())),
            "matched_existing": sum(v for k, v in by_class.items() if k in MATCHED),
            "followups": by_class.get("FOLLOWUP", 0),
            "genuine_new": by_class.get("GENUINE_NEW_QUESTION", 0),
            "ambiguous": by_class.get("AMBIGUOUS", 0),
            "non_question": by_class.get("NON_QUESTION_UNRECOVERABLE", 0),
        },
        "asks": {
            "unique_asks": len(asks),
            "unique_new_asks": len(new_asks),
            "asks_reported_by_more_than_one_candidate": multi,
            "cross_candidate_duplicate_count": len(multi),
        },
        "production": {
            "occurrences_with_a_produced_card": published,
            "produced_count": len(published),
            "outstanding_new_asks": sorted(
                o for o, a in adj.items()
                if a["classification"] == "GENUINE_NEW_QUESTION" and o not in manifests),
            "by_occurrence": {o: manifests[o] for o in published},
        },
        "unresolved": {
            "ambiguous_occurrences": unresolved,
            "note": "An ambiguous occurrence is held, never guessed into a card.",
        },
    }
    return ledger


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    ledger = build()
    if ledger is None:
        return 2
    text = json.dumps(ledger, indent=2, ensure_ascii=False) + "\n"
    if a.check:
        if not LEDGER.is_file():
            print("STALE: ledger absent")
            return 1
        if LEDGER.read_text(encoding="utf-8") != text:
            print("STALE: ledger on disk differs from a fresh derivation")
            return 1
        print("OK: August master ledger is current")
        return 0
    LEDGER.write_text(text, encoding="utf-8")
    print("wrote %s" % LEDGER.name)
    print("  submissions %d, raw occurrences %d (%s)"
          % (ledger["august"]["submissions"], ledger["august"]["raw_occurrences"],
             ledger["august"]["raw_occurrences_by_batch"]))
    print("  adjudication %s" % ledger["adjudication"]["by_classification"])
    print("  unique asks %d, of which new %d; produced %d"
          % (ledger["asks"]["unique_asks"], ledger["asks"]["unique_new_asks"],
             ledger["production"]["produced_count"]))
    print("  historical unchanged: %s (%d)"
          % (ledger["historical_denominator"]["unchanged"],
             ledger["historical_denominator"]["raw_occurrences"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
