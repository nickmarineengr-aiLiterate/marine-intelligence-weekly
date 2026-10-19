#!/usr/bin/env python3
"""LANDING gate: no correction record may land while its Founder decision is pending.

Deliberately NOT part of the qualification run (run_oral_release.py): a candidate
must be fully qualifiable while PENDING, and the qualification gates keep
enforcing every pin through `status: AUTHORISED` exactly as before. This check is
run at the landing/GO step only, and it fails closed:

  L1  every correction record parses and its founder_authorisation is well formed
  L2  every record NOT present at the legacy commit carries founder_authorisation
  L3  no record is PENDING_FOUNDER_DECISION
  L4  no record declares an OPEN cross-product safety item
      (propagation.cross_product_safety_items[].status == "OPEN") -- a safety
      error the record found in another product stays blocking until that
      product's owner has corrected and verified it

Schema-identical to the Engineering R1 lane's landing gate (L1-L3); L4 is added
by the P0 safety lane. See oral_manifest.FOUNDER_AUTHORISATION_STATES.

  PYTHONIOENCODING=utf-8 python tools/oral/check_founder_authorisation_for_landing.py
Prints "<N> checks, <M> FAIL"; exit 0 only if landing is permitted.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import oral_manifest as M  # noqa: E402


def open_cross_product_items(manifest: dict) -> list[str]:
    prop = manifest.get("propagation")
    items = prop.get("cross_product_safety_items") if isinstance(prop, dict) else None
    return ["%s (%s)" % (i.get("item_id"), i.get("product")) for i in items or []
            if not isinstance(i, dict) or i.get("status") != "CLOSED_VERIFIED"]


def main() -> int:
    res = []
    pending, missing, malformed, cross = [], [], [], []
    for p in sorted(HERE.glob(M.CORRECTION_MANIFEST_GLOB)):
        try:
            m = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            malformed.append("%s: %s" % (p.name, e))
            continue
        for check, ok, detail in M.founder_authorisation_findings(m, M._is_legacy_record(p)):
            if not ok:
                (missing if check.endswith("present_unless_legacy") else malformed).append("%s: %s" % (p.name, detail))
        if (m.get("founder_authorisation") or {}).get("state") == "PENDING_FOUNDER_DECISION":
            pending.append(p.name)
        cross += ["%s: %s" % (p.name, i) for i in open_cross_product_items(m)]
    res.append(("L1_founder_authorisation_well_formed", not malformed, "; ".join(malformed[:5])))
    res.append(("L2_new_records_carry_founder_authorisation", not missing, "; ".join(missing[:5])))
    res.append(("L3_no_record_pending_founder_decision", not pending, "pending=%s" % pending))
    res.append(("L4_no_open_cross_product_safety_item", not cross, "open=%s" % cross))
    for n, ok, d in res:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", n, ("  -- " + d) if (d and not ok) else ""))
    f = sum(1 for _, ok, _ in res if not ok)
    print("%d checks, %d FAIL" % (len(res), f))
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
