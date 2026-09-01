"""Mutation controls for validate_oral_intake.py.

Every mutation must be caught by its OWN named gate. A mutation caught only
because some other check went red has not proved its guard, so each spec
records `expect_gate` and the harness compares the actual failing gate set.

The real repository is never mutated. The tree is copied once into a scratch
directory and ORAL_REPO_ROOT points the validator at the copy, so a killed run
cannot leave mutated bytes on disk.

  python tools/oral/mutate_oral_intake.py
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Reach the shared UTF-8 stdio contract in THIS file's source. Inheriting it
# as a side effect of somebody else's import is a contract satisfied only at
# runtime, and it stops being true the moment that import moves -- which is
# why test_oral_release_infra scans sources rather than processes.
from oral_bytes import enable_utf8_stdio  # noqa: E402

enable_utf8_stdio()
REL_AUDIT = Path("meoclass1/oral-intelligence/examiner-audit")

SRC = REL_AUDIT / "ALL_SURVEYORS_SOURCE_RECORDS.jsonl"
REC = REL_AUDIT / "ORAL_788_RECONCILIATION.jsonl"
FIN = REL_AUDIT / "FINAL_788_PRODUCTION_DISPOSITION.jsonl"
INT = REL_AUDIT / "AUGUST2026_INTAKE_RECORDS.jsonl"
ADJ = REL_AUDIT / "AUGUST2026_INTAKE_ADJUDICATIONS.json"
REG = Path("tools/oral/oral_followup_register.json")
QBK = Path("docs/MIW-master-Question-bank")


# ----------------------------------------------------------------- mutators
def rd(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def wr(p, rows):
    p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                 encoding="utf-8")


def m_delete_historical(root):
    p = root / SRC
    rows = rd(p)
    rows.pop(400)
    wr(p, rows)


def m_double_account(root):
    p = root / REC
    rows = rd(p)
    rows[7] = dict(rows[6])          # same source_id twice
    wr(p, rows)


def m_target_nonexistent_card(root):
    p = root / REC
    rows = rd(p)
    rows[0]["matched_question_id"] = "QB99_Z#q999"
    wr(p, rows)


def m_alter_raw_wording(root):
    p = root / REC
    rows = rd(p)
    rows[3]["raw_question_text"] = rows[3]["raw_question_text"] + " (tidied up)"
    wr(p, rows)


def m_unsupported_surveyor(root):
    p = root / REC
    rows = rd(p)
    rows[11]["examiner"] = "Rajappan"      # a CURRENT examiner, never historical
    wr(p, rows)


def m_followup_marked_implemented(root):
    p = root / REG
    d = json.loads(p.read_text(encoding="utf-8"))
    d["actions"][4]["status"] = "IMPLEMENTED"
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


def m_followup_renumbered(root):
    p = root / REG
    d = json.loads(p.read_text(encoding="utf-8"))
    d["actions"][9]["followup_id"] = "FUP-999"
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


def m_fresh_into_historical(root):
    """The headline defect: an August row appended to the historical ledger."""
    p = root / SRC
    rows = rd(p)
    rows.append({**rows[0], "source_id": "AUG-0001",
                 "raw_question_text": "primary and secondary means of venting"})
    wr(p, rows)


def m_paraphrase_as_new_without_evidence(root):
    p = root / ADJ
    d = json.loads(p.read_text(encoding="utf-8"))
    for a in d["adjudications"]:
        if a["occurrence_id"] == "AUG-0012":
            a["classification"] = "GENUINE_NEW_QUESTION"
            a["matched_question_id"] = None
            a["evidence"] = "looks new to me"
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


def m_delete_fresh_occurrence(root):
    p = root / INT
    rows = rd(p)
    rows.pop(5)
    wr(p, rows)


def m_invent_surveyor_attribution(root):
    p = root / INT
    rows = rd(p)
    rows[2]["examiner_attribution"] = "Rajappan"
    wr(p, rows)


def m_intake_raw_wording_altered(root):
    """Raw wording must be immutable in the intake lane too."""
    p = root / ADJ
    d = json.loads(p.read_text(encoding="utf-8"))
    d["adjudications"].append({
        "occurrence_id": "AUG-9999",
        "classification": "EXACT_EXISTING",
        "matched_question_id": "QB5_A#q2",
        "evidence": "phantom row with no preserved occurrence",
    })
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


def m_intake_target_nonexistent(root):
    p = root / ADJ
    d = json.loads(p.read_text(encoding="utf-8"))
    d["adjudications"][1]["matched_question_id"] = "QB42_X#q7"
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


def m_final_workbook_while_open(root):
    (root / QBK / "MIW_August2026_QuestionBank_FINAL.xlsx").write_bytes(b"PK\x03\x04stub")


def m_overwrite_july_workbook(root):
    (root / QBK / "MIW_July2026_QuestionBank_SHARE.xlsx").unlink()


SPECS = [
    ("MUT-01_delete_one_historical_occurrence", m_delete_historical,
     {"H1_historical_count_is_788", "H4_reconciliation_accounts_every_occurrence_once"}),
    ("MUT-02_account_one_occurrence_twice", m_double_account,
     {"H4_reconciliation_accounts_every_occurrence_once"}),
    ("MUT-03_assign_occurrence_to_nonexistent_card", m_target_nonexistent_card,
     {"H7_historical_card_targets_resolve"}),
    ("MUT-04_alter_historical_raw_wording", m_alter_raw_wording,
     {"H5_reconciliation_raw_wording_immutable"}),
    ("MUT-05_unsupported_surveyor_assignment", m_unsupported_surveyor,
     {"H8_historical_attribution_supported"}),
    ("MUT-06_unresolved_followup_marked_implemented", m_followup_marked_implemented,
     {"F3_no_followup_claims_implemented_without_a_batch_manifest"}),
    ("MUT-07_followup_renumbered", m_followup_renumbered,
     {"F1_followup_ids_stable_and_dense"}),
    ("MUT-08_fresh_occurrence_into_historical_denominator", m_fresh_into_historical,
     {"H1_historical_count_is_788", "A4_no_intake_id_in_historical_ledger",
      "A6_historical_denominator_unchanged_by_intake"}),
    ("MUT-09_paraphrase_marked_new_without_adjudication",
     m_paraphrase_as_new_without_evidence,
     {"A9_new_card_claims_carry_negative_search"}),
    ("MUT-10_delete_one_fresh_occurrence", m_delete_fresh_occurrence,
     {"A2_every_intake_occurrence_adjudicated"}),
    ("MUT-11_invent_surveyor_attribution", m_invent_surveyor_attribution,
     {"A10_intake_attribution_is_panel_level"}),
    ("MUT-12_adjudication_without_preserved_occurrence", m_intake_raw_wording_altered,
     {"A2_every_intake_occurrence_adjudicated", "A11_intake_raw_wording_present"}),
    ("MUT-13_intake_target_nonexistent_card", m_intake_target_nonexistent,
     {"A8_intake_card_targets_resolve"}),
    ("MUT-14_final_workbook_while_intake_open", m_final_workbook_while_open,
     {"Z1_no_final_august_workbook_while_intake_open"}),
    ("MUT-15_overwrite_prior_july_workbook", m_overwrite_july_workbook,
     {"Z2_prior_july_v26_workbooks_preserved"}),
]


def run_validator(root):
    env = dict(os.environ, ORAL_REPO_ROOT=str(root), PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, str(root / "tools/oral/validate_oral_intake.py")],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    failed = {ln.split()[1] for ln in r.stdout.splitlines() if ln.startswith("FAIL")}
    return r.returncode, failed


def main():
    scratch = Path(tempfile.mkdtemp(prefix="oral_intake_mut_"))
    base = scratch / "base"
    try:
        print(f"staging a copy of the tree in {scratch} ...")
        for rel in ("meoclass1", "tools/oral", "docs/MIW-master-Question-bank"):
            s = REPO / rel
            d = base / rel
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(s, d, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

        rc, failed = run_validator(base)
        if rc != 0:
            print(f"PRECONDITION FAILED: clean copy is not green -> {sorted(failed)}")
            return 1
        print("precondition: clean copy is green\n")

        caught = escaped = 0
        for name, fn, expect in SPECS:
            work = scratch / "work"
            if work.exists():
                shutil.rmtree(work)
            shutil.copytree(base, work)
            fn(work)
            rc, failed = run_validator(work)
            hit = expect & failed
            if rc != 0 and hit:
                caught += 1
                extra = failed - expect
                note = f" (+collateral {sorted(extra)})" if extra else ""
                print(f"CAUGHT   {name}  by {sorted(hit)}{note}")
            elif rc != 0:
                escaped += 1
                print(f"MISFIRED {name}  expected {sorted(expect)}, got {sorted(failed)}")
            else:
                escaped += 1
                print(f"ESCAPED  {name}  validator stayed green")
            shutil.rmtree(work)

        print(f"\nmutations={len(SPECS)} caught={caught} escaped={escaped}")

        rc, failed = run_validator(base)
        print(f"residue check: base still green = {rc == 0}")
        rc2, _ = subprocess.run(
            [sys.executable, str(REPO / "tools/oral/validate_oral_intake.py")],
            capture_output=True, text=True,
            env=dict(os.environ, PYTHONIOENCODING="utf-8")).returncode, None
        print(f"residue check: REAL repo still green = {rc2 == 0}")
        return 0 if escaped == 0 and rc == 0 and rc2 == 0 else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
