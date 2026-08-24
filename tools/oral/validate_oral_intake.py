"""Gates over BOTH oral evidence denominators.

Historical  : the 788 All-Surveyors raw occurrences (ASC-*)
Current     : the August 2026 candidate intake (AUG-*)

The two are deliberately separate counts. The gate that matters most here is
denominator isolation: an AUG-* row that leaks into the historical ledger, or
an ASC-* row that leaks into the intake, must fail loudly. A merged count of
811 would look like progress and destroy the historical baseline.

Fails closed: a missing evidence file is a failure, never a skip.

  python tools/oral/validate_oral_intake.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

OUT = L.OUT
HIST_EXPECTED = 788
ASC_RE = re.compile(r"^ASC-\d{4}$")
AUG_RE = re.compile(r"^AUG-\d{4}$")

CLASSES = {
    "EXACT_EXISTING", "PARAPHRASE_EXISTING", "FOLLOWUP",
    "GENUINE_NEW_QUESTION", "AMBIGUOUS", "NON_QUESTION_UNRECOVERABLE",
}
NEEDS_TARGET = {"EXACT_EXISTING", "PARAPHRASE_EXISTING", "FOLLOWUP"}
NEEDS_NO_TARGET = {"GENUINE_NEW_QUESTION", "NON_QUESTION_UNRECOVERABLE"}

results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def jsonl(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def main():
    # ---------------- historical ----------------
    src = jsonl(OUT / "ALL_SURVEYORS_SOURCE_RECORDS.jsonl")
    rec = jsonl(OUT / "ORAL_788_RECONCILIATION.jsonl")
    fin = jsonl(OUT / "FINAL_788_PRODUCTION_DISPOSITION.jsonl")

    sid = [r["source_id"] for r in src]
    check("H1_historical_count_is_788", len(src) == HIST_EXPECTED, f"{len(src)}")
    check("H2_historical_ids_unique", len(set(sid)) == len(sid),
          f"{len(sid) - len(set(sid))} duplicates")
    check("H3_historical_ids_wellformed", all(ASC_RE.match(i) for i in sid))

    for label, rows in (("reconciliation", rec), ("disposition", fin)):
        ids = [r["source_id"] for r in rows]
        check(f"H4_{label}_accounts_every_occurrence_once",
              len(ids) == len(set(ids)) == len(set(sid)) and set(ids) == set(sid),
              f"n={len(ids)} unique={len(set(ids))}")

    # A row whose source_id is absent from the source store counts as drift, not
    # a crash: an exception here would exit non-zero without naming a gate, and
    # a guard that fails by crashing cannot say what it caught.
    raw = {r["source_id"]: r["raw_question_text"] for r in src}
    for label, rows in (("reconciliation", rec), ("disposition", fin)):
        drift = [r["source_id"] for r in rows
                 if r["raw_question_text"] != raw.get(r["source_id"])]
        check(f"H5_{label}_raw_wording_immutable", not drift, f"{len(drift)} drifted")

    # every occurrence carries exactly one terminal disposition on each axis
    for field, rows in (("content_disposition", rec), ("production_action", fin)):
        c = Counter(r.get(field) for r in rows)
        check(f"H6_{field}_total_is_788", sum(c.values()) == HIST_EXPECTED
              and None not in c, dict(c))

    # every matched target resolves to a live card
    inv = {c["canonical_question_id"] for c in L.build_inventory()}
    bad = sorted({r["matched_question_id"] for r in rec
                  if r.get("matched_question_id")} - inv)
    check("H7_historical_card_targets_resolve", not bad, f"unresolved: {bad[:5]}")

    # attribution: every examiner is one of the four the document declares
    declared = {"John", "Simon", "Nair", "Paul"}
    bad = sorted({r.get("examiner") for r in rec} - declared)
    check("H8_historical_attribution_supported", not bad, f"{bad}")

    # ---------------- follow-up register ----------------
    reg = json.loads((L.REPO / "tools" / "oral" / "oral_followup_register.json")
                     .read_text(encoding="utf-8"))
    acts = reg["actions"]
    check("F1_followup_ids_stable_and_dense",
          [a["followup_id"] for a in acts]
          == [f"FUP-{i:03d}" for i in range(1, len(acts) + 1)])
    check("F2_followup_targets_resolve",
          all(a.get("target_structural_check") == "TARGET_RESOLVES" for a in acts))
    check("F3_no_followup_claims_implemented_without_a_batch_manifest",
          all(a["status"] == "AUTHORISED_NOT_STARTED" for a in acts),
          "register records authorisation; manifests record implementation")

    # ---------------- current intake ----------------
    intake = jsonl(OUT / "AUGUST2026_INTAKE_RECORDS.jsonl")
    adj = json.loads((OUT / "AUGUST2026_INTAKE_ADJUDICATIONS.json")
                     .read_text(encoding="utf-8"))["adjudications"]

    aid = [o["occurrence_id"] for o in intake]
    check("A1_intake_ids_unique_and_wellformed",
          len(set(aid)) == len(aid) and all(AUG_RE.match(i) for i in aid))
    check("A2_every_intake_occurrence_adjudicated",
          {a["occurrence_id"] for a in adj} == set(aid),
          f"intake={len(aid)} adjudicated={len(adj)}")
    check("A3_intake_classifications_governed",
          all(a["classification"] in CLASSES for a in adj))

    # THE isolation gate, both directions
    check("A4_no_intake_id_in_historical_ledger",
          not (set(aid) & set(sid)) and not any(AUG_RE.match(i) for i in sid))
    check("A5_no_historical_id_in_intake",
          not any(ASC_RE.match(i) for i in aid))
    check("A6_historical_denominator_unchanged_by_intake",
          len(src) == HIST_EXPECTED,
          f"historical must stay {HIST_EXPECTED}, never {len(src) + len(aid)}")

    # a classification must agree with whether it names a card
    wrong = [a["occurrence_id"] for a in adj
             if (a["classification"] in NEEDS_TARGET) != bool(a.get("matched_question_id"))
             and a["classification"] in NEEDS_TARGET | NEEDS_NO_TARGET]
    check("A7_classification_and_target_agree", not wrong, f"{wrong}")

    bad = sorted({a["matched_question_id"] for a in adj
                  if a.get("matched_question_id")} - inv)
    check("A8_intake_card_targets_resolve", not bad, f"unresolved: {bad[:5]}")

    # every new-card claim must carry the negative search that justifies it
    thin = [a["occurrence_id"] for a in adj
            if a["classification"] == "GENUINE_NEW_QUESTION"
            and "0 hits" not in a.get("evidence", "")]
    check("A9_new_card_claims_carry_negative_search", not thin, f"{thin}")

    # attribution must never be pinned to one examiner on panel-level evidence
    check("A10_intake_attribution_is_panel_level",
          all(o.get("examiner_attribution") == "PANEL_LEVEL_ONLY" for o in intake))

    # raw wording immutability across the intake layer
    byid = {o["occurrence_id"]: o["raw_question_text"] for o in intake}
    check("A11_intake_raw_wording_present",
          all(byid.get(a["occurrence_id"]) is not None for a in adj))

    # ---------------- freeze ----------------
    qb = L.REPO / "docs" / "MIW-master-Question-bank"
    final = sorted(qb.glob("*August*FINAL*.xlsx")) + sorted(qb.glob("*v27*.xlsx"))
    final = [p for p in final if "WORKING" not in p.name]
    check("Z1_no_final_august_workbook_while_intake_open", not final,
          f"found {[p.name for p in final]}")
    july = qb / "MIW_July2026_QuestionBank_SHARE.xlsx"
    v26 = qb / "MEO_QB_master_v26.xlsx"
    check("Z2_prior_july_v26_workbooks_preserved",
          july.exists() and v26.exists())

    # ---------------- report ----------------
    width = max(len(n) for n, _, _ in results)
    for n, ok, d in results:
        print(f"{'PASS' if ok else 'FAIL'}  {n:<{width}}  {d}")
    npass = sum(1 for _, ok, _ in results if ok)
    nfail = len(results) - npass
    print(f"\n{npass} PASS / {nfail} FAIL")
    return 1 if nfail else 0


if __name__ == "__main__":
    raise SystemExit(main())
