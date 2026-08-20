"""Mutation harness for the enrichment consolidation guards.

Each mutation is applied to a COPY of the audit inputs in a scratch tree, the
validator is run against that tree, and the mutation is then restored. A
mutation that leaves the bytes unchanged is reported as NOT APPLIED and counted
as a failure of the harness, not as a caught defect: a guard "validated" by a
no-op mutation has been validated by nothing.

  PYTHONIOENCODING=utf-8 python tools/oral/mutate_enrichment_consolidation.py
"""
from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import oral_lib as L  # noqa: E402

AUDIT = L.MEO / "oral-intelligence" / "examiner-audit"
ADJ_NAME = "FINAL_ORAL_ENRICHMENT_ADJUDICATION.json"
CONS_NAME = "FINAL_ORAL_ENRICHMENT_CONSOLIDATION.json"


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(obj, path):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False, sort_keys=False)
        f.write("\n")


# Each mutation takes (adjudication, consolidation) and mutates in place.
def m_delete_family(adj, cons):
    """A. delete one family decision"""
    victim = adj["family_decisions"].pop(3)
    return f"removed {victim['family_id']}"


def m_duplicate_family(adj, cons):
    """B. duplicate one family"""
    adj["family_decisions"].append(copy.deepcopy(adj["family_decisions"][0]))
    return f"duplicated {adj['family_decisions'][0]['family_id']}"


def m_missing_target(adj, cons):
    """C. retained enrichment pointing at a target that does not exist"""
    a = cons["production_actions"][0]
    a["target"] = "QB99_Z#q999"
    return f"{a['action_id']} target -> QB99_Z#q999"


def m_blank_limb(adj, cons):
    """D. retained enrichment with a blank missing limb"""
    for d in adj["family_decisions"]:
        if d["disposition"] == "ENRICH":
            d["missing_limb"] = "   "
            return f"blanked limb on {d['family_id']}"
    raise AssertionError("no ENRICH family")


def m_covered_no_evidence(adj, cons):
    """E. ALREADY_COVERED without an evidence target"""
    for d in adj["family_decisions"]:
        if d["disposition"] == "ALREADY_COVERED_EXISTING_CARD":
            d.pop("evidence_target")
            return f"stripped evidence target from {d['family_id']}"
    raise AssertionError("no ALREADY_COVERED family")


def m_action_no_family(adj, cons):
    """F. production action with zero families"""
    a = cons["production_actions"][1]
    a["family_ids"] = []
    return f"{a['action_id']} family_ids -> []"


def m_family_two_actions(adj, cons):
    """G. one family assigned to two incompatible actions"""
    fid = cons["production_actions"][0]["family_ids"][0]
    cons["production_actions"][1]["family_ids"].append(fid)
    return f"{fid} added to {cons['production_actions'][1]['action_id']}"


def m_count_disagrees(adj, cons):
    """H. summary count disagrees with the records"""
    cons["counts"]["UNIQUE_ENRICHMENT_EDIT_ACTIONS"] += 7
    return "UNIQUE_ENRICHMENT_EDIT_ACTIONS inflated by 7"


def m_retarget_no_reason(adj, cons):
    """I. retarget without old/new reason"""
    for d in adj["family_decisions"]:
        if d["disposition"] == "RETARGET_EXISTING_QB":
            d["why_old_wrong"] = ""
            return f"cleared why_old_wrong on {d['family_id']}"
    raise AssertionError("no RETARGET family")


def m_followup_no_parent(adj, cons):
    """J. follow-up conversion without a parent"""
    for d in adj["family_decisions"]:
        if d["disposition"] == "CONVERTED_TO_FOLLOWUP":
            d.pop("parent")
            return f"stripped parent from {d['family_id']}"
    raise AssertionError("no CONVERTED_TO_FOLLOWUP family")


def m_qtext_drift(adj, cons):
    """K. recorded target q-text no longer matches live HTML"""
    a = cons["production_actions"][2]
    a["target_q_text"] = a["target_q_text"] + " (drifted)"
    return f"{a['action_id']} q-text drifted"


def m_batch_drops_family(adj, cons):
    """L. a batch silently drops a retained family"""
    for b in cons["batches"]:
        if b["source_family_ids"]:
            gone = b["source_family_ids"].pop()
            return f"{b['batch_id']} dropped {gone}"
    raise AssertionError("no batch")


MUTATIONS = [m_delete_family, m_duplicate_family, m_missing_target, m_blank_limb,
             m_covered_no_evidence, m_action_no_family, m_family_two_actions,
             m_count_disagrees, m_retarget_no_reason, m_followup_no_parent,
             m_qtext_drift, m_batch_drops_family]


def main():
    root = Path(tempfile.mkdtemp(prefix="enrich-mut-"))
    try:
        # A scratch repo root holding only what the validator reads.
        shutil.copytree(HERE, root / "tools" / "oral")
        (root / "meoclass1" / "oral-intelligence" / "examiner-audit").mkdir(parents=True)
        shutil.copy(L.MEO / "qb_content_index.json", root / "meoclass1")
        for n in os.listdir(AUDIT):
            if n.startswith("FINAL_ORAL_ENRICHMENT") or n == "FINAL_ORAL_PRODUCTION_AUTHORIZATION.json":
                shutil.copy(AUDIT / n, root / "meoclass1" / "oral-intelligence" / "examiner-audit" / n)

        sa = root / "meoclass1" / "oral-intelligence" / "examiner-audit" / ADJ_NAME
        sc = root / "meoclass1" / "oral-intelligence" / "examiner-audit" / CONS_NAME
        base_a, base_c = sa.read_bytes(), sc.read_bytes()

        env = dict(os.environ, ORAL_REPO_ROOT=str(root), PYTHONIOENCODING="utf-8")
        val = str(root / "tools" / "oral" / "validate_enrichment_consolidation.py")

        r = subprocess.run([sys.executable, val], env=env, capture_output=True, text=False)
        if r.returncode != 0:
            print("BASELINE FAILED - the harness itself is broken")
            print(r.stdout.decode("utf-8", "replace"))
            return 1
        print("baseline: clean tree validates\n")

        escapes = noops = crashes = 0
        for fn in MUTATIONS:
            label = (fn.__doc__ or fn.__name__).strip()
            adj = json.loads(sa.read_text(encoding="utf-8"))
            cons = json.loads(sc.read_text(encoding="utf-8"))
            try:
                what = fn(adj, cons)
            except Exception as e:  # a mutation that cannot be built is a harness bug
                print(f"CRASH   {label}: {e}")
                crashes += 1
                continue
            dump(adj, sa)
            dump(cons, sc)
            applied = sa.read_bytes() != base_a or sc.read_bytes() != base_c
            if not applied:
                print(f"NOT APPLIED  {label} ({what}) - byte-identical, proves nothing")
                noops += 1
            else:
                r = subprocess.run([sys.executable, val], env=env, capture_output=True, text=False)
                if r.returncode == 0:
                    print(f"ESCAPE  {label} ({what})")
                    escapes += 1
                else:
                    first = r.stdout.decode("utf-8", "replace").splitlines()[0]
                    print(f"caught  {label} -> {first}")
            sa.write_bytes(base_a)
            sc.write_bytes(base_c)
            if sa.read_bytes() != base_a or sc.read_bytes() != base_c:
                print(f"RESTORE FAILED after {label}")
                return 1

        print(f"\n{len(MUTATIONS)} mutations | {escapes} escapes | {noops} no-ops | {crashes} crashes")
        return 1 if (escapes or noops or crashes) else 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
