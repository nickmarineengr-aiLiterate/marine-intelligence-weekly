"""Controls for the October 2026 intake profile (H8 / Founder FD-3, FD-4).

FD-3 registers October 2026 as its own intake and identity space and keeps the
late-September reports in the September space. FD-4 makes the curated
line-disposition record authoritative for October and forbids re-deriving it
with the shared parser. These controls pin exactly that, and pin that the two
existing profiles are untouched by the registration.

  PYTHONIOENCODING=utf-8 python tools/oral/test_intake_profile_october.py

Exit 0 when every control holds. No network, no private evidence required.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
import ingest_august_intake as I  # noqa: E402

FAIL = []


def check(name, ok, detail=""):
    print(("ok   " if ok else "FAIL ") + "%-56s %s" % (name, detail))
    if not ok:
        FAIL.append(name)


oct_ = I.profile("2026-10")
check("O1_october_profile_registered", oct_["label"] == "October")
check("O2_october_identity_space", oct_["occurrence_prefix"] == "OCT-" and oct_["submission_prefix"] == "OCT2026-S")
check("O3_october_denominator_isolated",
      len({p["denominator_class"] for p in I.INTAKE_PROFILES.values()}) == len(I.INTAKE_PROFILES))
prefixes = [p["occurrence_prefix"] for p in I.INTAKE_PROFILES.values()]
check("O4_identity_prefixes_disjoint", len(set(prefixes)) == len(prefixes), str(prefixes))
check("O5_october_curated_authoritative", oct_.get("curated_records_authoritative") is True)

rel = [str(oct_[k].relative_to(REPO)).replace("\\", "/") for k in ("records", "report", "carriers", "adjudications")]
ign = subprocess.run(["git", "-C", str(REPO), "check-ignore", "--no-index", *rel], capture_output=True, text=True)
check("O6_october_private_paths_git_ignored", ign.stdout.split() and len(ign.stdout.splitlines()) == 4,
      "%d of 4 ignored" % len(ign.stdout.splitlines()))
tracked = subprocess.run(["git", "-C", str(REPO), "ls-files", "--", *rel], capture_output=True, text=True).stdout.strip()
check("O7_october_private_paths_untracked", tracked == "", tracked or "none tracked")

# The registration must not have moved the existing months.
sep, aug = I.profile("2026-09"), I.profile("2026-08")
check("O8_september_profile_unchanged",
      sep["occurrence_prefix"] == "SEP-" and sep["submission_prefix"] == "SEP2026-S"
      and sep["denominator_class"] == "CURRENT_SEPTEMBER_INTAKE" and sep["result_bare"] is True
      and "curated_records_authoritative" not in sep
      and sep["records"].name == "SEPTEMBER2026_INTAKE_RECORDS.jsonl")
check("O9_august_profile_unchanged",
      aug["occurrence_prefix"] == "AUG-" and aug["result_bare"] is False
      and "curated_records_authoritative" not in aug and I.DEFAULT_MONTH == "2026-08")

# FD-4: the ingest CLI refuses to re-derive October, and writes nothing.
before = {p: (p.stat().st_mtime_ns if p.exists() else None) for p in (oct_["records"], oct_["report"])}
r = subprocess.run([sys.executable, str(HERE / "ingest_august_intake.py"), "--month", "2026-10"],
                   capture_output=True, text=True, encoding="utf-8")
after = {p: (p.stat().st_mtime_ns if p.exists() else None) for p in before}
check("O10_ingest_refuses_curated_october", r.returncode == 2 and "REFUSED" in r.stdout, "exit=%s" % r.returncode)
check("O11_refusal_writes_nothing", before == after)

print("october intake profile controls: %d FAIL" % len(FAIL))
sys.exit(1 if FAIL else 0)
