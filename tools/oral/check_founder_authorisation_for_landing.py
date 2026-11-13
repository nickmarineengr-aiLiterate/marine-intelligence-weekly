#!/usr/bin/env python3
"""LANDING gate: no correction record may land while its Founder decision is pending.

Deliberately NOT part of the qualification run (run_oral_release.py): a candidate
must be fully qualifiable while PENDING, and the qualification gates keep
enforcing every pin through `status: AUTHORISED` exactly as before. This check is
run at the landing/GO step only, and it fails closed:

  L0  the committed state is what is judged: no replace refs, grafts, alternates, shallow history, gitlinks or
      redirected git dir; a clean tree with no untracked, ignored or index-flagged files; python -B. Every check
      below reads the records and exception files from HEAD, never from the working tree.
  L1  every correction record parses and its founder_authorisation is well formed
  L2  every record NOT present at the legacy commit carries founder_authorisation
  L3  no record is PENDING_FOUNDER_DECISION
  L4  no record declares an OPEN cross-product safety item
      (propagation.cross_product_safety_items[].status == "OPEN") -- a safety
      error the record found in another product stays blocking until that
      product's owner has corrected and verified it -- UNLESS one exactly matching, SHA-pinned governance
      exception applies (governance_exceptions.py, X1-X9, judged at HEAD): known and SHA-pinned, in date, same
      item/record/path with the record's item list pinned, the WHOLE diff from the production baseline pinned path by
      path and blob by blob (so no deployment-surface or other change can ride along), every release record
      authorised at HEAD, a clean tree with no hidden index flags, and fresh live non-deployment evidence for this
      exact commit and tree. The item itself stays OPEN.

Schema-identical to the Engineering R1 lane's landing gate (L1-L3); L4 is added
by the P0 safety lane. See oral_manifest.FOUNDER_AUTHORISATION_STATES.

  python -B -X utf8 tools/oral/check_founder_authorisation_for_landing.py [--deployment-evidence FILE]
  For a landing decision run it through the out-of-repository launcher (fresh clone, code blobs checked against
  values recorded outside the repository), never from a working checkout.
Prints "<N> checks, <M> FAIL"; exit 0 only if landing is permitted.
"""
from __future__ import annotations

import datetime as _dt
import fnmatch
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import oral_manifest as M  # noqa: E402
import governance_exceptions as GX  # noqa: E402


def open_cross_product_items(manifest: dict) -> list[str]:
    prop = manifest.get("propagation")
    items = prop.get("cross_product_safety_items") if isinstance(prop, dict) else None
    return ["%s (%s)" % (i.get("item_id"), i.get("product")) for i in items or []
            if not isinstance(i, dict) or i.get("status") != "CLOSED_VERIFIED"]


def open_cross_product_entries(manifest: dict) -> list[dict]:
    prop = manifest.get("propagation")
    items = prop.get("cross_product_safety_items") if isinstance(prop, dict) else None
    return [i if isinstance(i, dict) else {"item_id": repr(i)} for i in items or []
            if not isinstance(i, dict) or i.get("status") != "CLOSED_VERIFIED"]


def _legacy_at_head(facts, name: str) -> bool:
    """oral_manifest._is_legacy_record, judged on the committed blob instead of the working file."""
    path = GX.ORAL + name
    return facts.exists_at(M.FOUNDER_AUTHORISATION_LEGACY_COMMIT, path) or \
        M.legacy_compat_allows(name, facts.blob_at_head(path))


def main(argv=None, facts=None, known=None, now=None, dont_write_bytecode=None) -> int:
    """Every input is read from HEAD (independent review R7, B1). L0 is unconditional."""
    argv = sys.argv[1:] if argv is None else argv
    facts = GX.RepoFacts() if facts is None else facts
    now = _dt.datetime.now(_dt.timezone.utc) if now is None else now
    dwb = sys.flags.dont_write_bytecode if dont_write_bytecode is None else dont_write_bytecode
    evidence = None
    if "--deployment-evidence" in argv:
        ev_path = Path(argv[argv.index("--deployment-evidence") + 1])
        try:
            evidence = json.loads(ev_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            evidence = {"_unreadable": str(e)}
    res = []
    l0 = facts.integrity_problems() + facts.clean_problems() + GX.bytecode_problems(dwb)
    res.append(("L0_committed_state_is_what_is_judged", not l0, "; ".join(l0)))
    pending, missing, malformed, open_items = [], [], [], []
    names = facts.list_head(GX.ORAL)
    if names is None:
        malformed.append("cannot list %s at HEAD" % GX.ORAL)
        names = []
    for p in sorted(names):
        name = Path(p).name
        if not fnmatch.fnmatch(name, M.CORRECTION_MANIFEST_GLOB):
            continue
        try:
            m = json.loads(facts.show_head(p) or "")
        except ValueError as e:
            malformed.append("%s: %s" % (name, e))
            continue
        if not isinstance(m, dict):
            malformed.append("%s: not an object" % name)
            continue
        for check, ok, detail in M.founder_authorisation_findings(m, _legacy_at_head(facts, name)):
            if not ok:
                (missing if check.endswith("present_unless_legacy") else malformed).append("%s: %s" % (name, detail))
        if (m.get("founder_authorisation") or {}).get("state") == "PENDING_FOUNDER_DECISION":
            pending.append(name)
        open_items += [(name, i) for i in open_cross_product_entries(m)]
    exc_files = GX.load_exception_files_at_head(facts)
    if exc_files is None:
        l4_ok, l4_blocks, l4_info = False, ["cannot list exception files at HEAD"], []
    else:
        l4_ok, l4_blocks, l4_info = GX.evaluate_l4(open_items, exc_files, facts, evidence, now, known)
    res.append(("L1_founder_authorisation_well_formed", not malformed, "; ".join(malformed[:5])))
    res.append(("L2_new_records_carry_founder_authorisation", not missing, "; ".join(missing[:5])))
    res.append(("L3_no_record_pending_founder_decision", not pending, "pending=%s" % pending))
    res.append(("L4_no_open_cross_product_safety_item", l4_ok, "; ".join(l4_blocks)))
    for n, ok, d in res:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", n, ("  -- " + d) if (d and not ok) else ""))
    for line in l4_info:
        print("INFO  L4 %s" % line)
    f = sum(1 for _, ok, _ in res if not ok)
    print("%d checks, %d FAIL" % (len(res), f))
    return 1 if f else 0

if __name__ == "__main__":
    sys.exit(main())
