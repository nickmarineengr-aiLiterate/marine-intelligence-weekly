"""PRIV-1 public-repository check: September 2026 raw intake records stay out.

The public half of a two-part boundary. It needs NO private evidence, so it can
run anywhere the public repository is checked out -- GitHub Actions included --
and it proves only what a public checkout can prove:

  PUB1  no tracked path is named like one of the four raw September records;
  PUB2  no raw record sits on disk at the old public examiner-audit path;
  PUB3  the private owner area those records belong in is git-ignored;
  PUB4  the public provenance record has exactly the approved shape, and its
        four pins are the validator's pins;
  PUB5  its approval identity is the authority the production queue recorded;
  PUB6  its original intake dates are present and are not the effective month.

It does NOT verify the private records themselves: their presence, their bytes,
the fingerprints or S0-S14. That is validate_oral_intake.py's work, on a machine
that holds the genuine evidence. This script says so on every run and never
reports a September qualification.

  python tools/oral/check_september_privacy_public.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402
from oral_bytes import enable_utf8_stdio  # noqa: E402
import ingest_august_intake as I  # noqa: E402
import validate_oral_intake as V  # noqa: E402

enable_utf8_stdio()
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def git(*a):
    r = subprocess.run(["git", *a], cwd=str(L.REPO), capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def main():
    rc, listing = git("ls-files")
    named = [p for p in listing.splitlines()
             if p.rsplit("/", 1)[-1] in V.SEPTEMBER_PRIVATE_PINS]
    check("PUB1_no_raw_september_record_tracked", rc == 0 and not named,
          "git ls-files failed" if rc else "tracked: %s" % (named or "none"))

    on_disk = sorted(n for n in V.SEPTEMBER_PRIVATE_PINS if (V.OUT / n).exists())
    check("PUB2_no_raw_september_record_at_the_public_path", not on_disk,
          "present: %s" % (on_disk or "none"))

    priv = I.profile("2026-09")["records"].parent
    not_ignored = []
    for n in V.SEPTEMBER_PRIVATE_PINS:
        rel = (priv / n).relative_to(L.REPO).as_posix()
        if git("check-ignore", "-q", "--no-index", rel)[0] != 0:
            not_ignored.append(rel)
    check("PUB3_private_owner_area_is_git_ignored", not not_ignored,
          "not ignored: %s" % (not_ignored or "none"))

    try:
        prov = json.loads(V.PUBLIC_PROVENANCE.read_text(encoding="utf-8"))
        fa = json.loads(V.SEPTEMBER_QUEUE.read_text(encoding="utf-8"))["batches"]["H7"]
    except (OSError, ValueError, KeyError) as e:
        for n in ("PUB4_public_provenance_shape_and_pins",
                  "PUB5_approval_identity_matches_the_queue",
                  "PUB6_original_intake_dates_present"):
            check(n, False, f"{type(e).__name__}: {e}")
    else:
        files = (prov.get("private_originals") or {}).get("files") or {}
        bad = [n for n, h in V.SEPTEMBER_PRIVATE_PINS.items()
               if (files.get(n) or {}).get("sha256") != h]
        shape = set(prov) == V.PROVENANCE_KEYS \
            and prov.get("record_class") == "PUBLIC_MINIMISED_PROVENANCE"
        check("PUB4_public_provenance_shape_and_pins", shape and not bad,
              "shape %s; pin mismatch: %s" % ("ok" if shape else "WRONG", bad or "none"))

        ai = prov.get("approval_identity") or {}
        auth = fa.get("founder_authorisation") or {}
        diff = [f for f in V.APPROVAL_FIELDS if ai.get(f) != auth.get(f)]
        if ai.get("batch") != "H7" or fa.get("status") != "FOUNDER_AUTHORISED":
            diff.append("batch/status")
        check("PUB5_approval_identity_matches_the_queue", not diff,
              "disagrees on: %s" % (diff or "none"))

        d = prov.get("dates") or {}
        oid = d.get("original_intake_dates")
        ok = (isinstance(oid, list) and oid
              and all(isinstance(x, str) and x.startswith("2026-09-") for x in oid)
              and d.get("effective_correction_month") == "2026-10")
        check("PUB6_original_intake_dates_present", ok, "original %s, effective %s"
              % (oid, d.get("effective_correction_month")))

    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name:<56}  {detail}")
    failed = sum(1 for _, ok, _ in results if not ok)
    print(f"\n{len(results) - failed} PASS / {failed} FAIL")
    print("SCOPE: PUBLIC STRUCTURE ONLY. Private September evidence NOT verified "
          "(S0-S14, SP3, SP4, SP6, SP8 need the genuine records; run "
          "validate_oral_intake.py in an authorised private environment).")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
