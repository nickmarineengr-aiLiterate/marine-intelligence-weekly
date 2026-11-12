#!/usr/bin/env python3
"""Positive and negative controls for the L4 governance exception (governance_exceptions.py) and the U-2
three-record compatibility allowance (oral_manifest.FOUNDER_AUTHORISATION_LEGACY_COMPAT_RECORDS).

Part A is pure (in-memory fixtures, a fake repository). Part B reads the real repository and writes only to a
temporary directory outside it. Every control states what MUST block or pass. A crash is a FAIL.
Prints "<N> checks, <M> FAIL".
"""
from __future__ import annotations

import copy
import datetime as dt
import json
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import governance_exceptions as GX  # noqa: E402
import oral_manifest as M  # noqa: E402

REAL_NAME = "governance_exception_gx_s1_rulesapp_falls_20261112.json"
REAL = json.loads((HERE / REAL_NAME).read_text(encoding="utf-8"))
FALLS = "correction_corr_safety_lsa_falls_coldstart_20261019_manifest.json"
NOW = dt.datetime(2026, 11, 12, 12, 0, tzinfo=dt.timezone.utc)
TREE = "t" * 40
VI_OK = "# comment\nnode_modules/\nRulesApp/\n"


def item(**kw):
    d = {"item_id": "XP-RULESAPP-FALLS-01", "product": "RulesApp", "status": "OPEN",
         "path": "RulesApp/repository/index/repo-data.json"}
    d.update(kw)
    return d


def records(state="FOUNDER_AUTHORISED", skip=None):
    out = {}
    for n in REAL["release"]["correction_records"]:
        if n == skip:
            continue
        out[n] = {"correction_id": "CORR-SAFETY-LSA-FALLS-COLDSTART-20261019" if n == FALLS else n,
                  "founder_authorisation": {"state": state}}
    return out


_DEFAULT = object()


class Facts:
    def __init__(self, added=_DEFAULT, anc=True, anc_candidate=True, clean=True, vi=VI_OK, tree=TREE):
        self._added = list(REAL["release"]["correction_records"]) if added is _DEFAULT else added
        self._anc, self._anc_c, self._clean, self._vi, self._tree = anc, anc_candidate, clean, vi, tree

    def is_ancestor(self, c):
        return self._anc_c if c == REAL["release"]["candidate_commit"] else self._anc

    def added_records(self, base):
        return self._added

    def clean(self):
        return self._clean

    def head_tree(self):
        return self._tree

    def vercelignore(self):
        return self._vi


def evidence(**kw):
    dc = REAL["deployment_condition"]
    ev = {"exception_id": REAL["exception_id"], "tree": TREE, "origin": dc["live_origin"],
          "checked_at_utc": "2026-11-12T11:00:00Z",
          "probes": [{"path": p, "status": 404, "redirect_followed": False} for p in dc["live_probe_paths"]]}
    ev.update(kw)
    return ev


def exc_files(e=None):
    raw = json.dumps(REAL if e is None else e, indent=1).encode("utf-8")
    eid = (REAL if e is None else e).get("exception_id")
    return {GX.exception_filename(eid) if isinstance(eid, str) else "governance_exception_x.json": raw}, \
        {eid: GX.sha256_bytes(raw)}


def run(open_items=None, recs=None, facts=None, ev="default", e=None, files=None, known=None, now=NOW):
    f, k = exc_files(e)
    files = f if files is None else files
    known = k if known is None else known
    open_items = [(FALLS, item())] if open_items is None else open_items
    ok, blocks, info = GX.evaluate_l4(records() if recs is None else recs, open_items, files, facts or Facts(),
                                      evidence() if ev == "default" else ev, now, known)
    return ok, " | ".join(blocks)


def mod(path, value):
    e = copy.deepcopy(REAL)
    cur = e
    for k in path[:-1]:
        cur = cur[k]
    cur[path[-1]] = value
    return e


def blocks_with(fragment, **kw):
    ok, why = run(**kw)
    return (not ok) and fragment in why


CONTROLS = [
    # ---- positive ---------------------------------------------------------------------------------
    ("P1_exact_item_valid_exception_fresh_evidence_passes", lambda: run()[0]),
    ("P2_both_declared_paths_pass",
     lambda: run(open_items=[(FALLS, item()), (FALLS, item(path="RulesApp/repository/index/search-index.json"))])[0]),
    ("P3_no_open_items_passes_without_evidence", lambda: run(open_items=[], ev=None)[0]),
    # ---- deployed product -------------------------------------------------------------------------
    ("N1_vercelignore_rule_removed_blocks", lambda: blocks_with("deployed product", facts=Facts(vi="node_modules/\n"))),
    ("N2_vercelignore_rule_commented_blocks", lambda: blocks_with("deployed product", facts=Facts(vi="# RulesApp/\n"))),
    ("N3_vercelignore_negation_reincludes_blocks",
     lambda: blocks_with("deployed product", facts=Facts(vi="RulesApp/\n!RulesApp/repository/index/\n"))),
    ("N4_live_probe_200_blocks",
     lambda: blocks_with("status 200", ev=evidence(probes=[dict(p, status=200) if i == 2 else p for i, p in
                                                          enumerate(evidence()["probes"])]))),
    ("N5_live_probe_redirect_blocks",
     lambda: blocks_with("status 302", ev=evidence(probes=[dict(p, status=302) if i == 0 else p for i, p in
                                                          enumerate(evidence()["probes"])]))),
    ("N6_probe_followed_redirect_blocks",
     lambda: blocks_with("no redirect", ev=evidence(probes=[dict(p, redirect_followed=True) if i == 0 else p
                                                           for i, p in enumerate(evidence()["probes"])]))),
    ("N7_probe_missing_from_evidence_blocks",
     lambda: blocks_with("missing from evidence", ev=evidence(probes=evidence()["probes"][1:]))),
    # ---- evidence ---------------------------------------------------------------------------------
    ("N8_missing_evidence_blocks", lambda: blocks_with("no deployment evidence", ev=None)),
    ("N9_stale_evidence_blocks", lambda: blocks_with("h old", ev=evidence(checked_at_utc="2026-11-10T11:00:00Z"))),
    ("N10_future_evidence_blocks", lambda: blocks_with("future", ev=evidence(checked_at_utc="2026-11-13T11:00:00Z"))),
    ("N11_evidence_for_other_tree_blocks", lambda: blocks_with("evidence tree", ev=evidence(tree="x" * 40))),
    ("N12_evidence_for_other_exception_blocks", lambda: blocks_with("evidence is for", ev=evidence(exception_id="GX-OTHER"))),
    ("N13_evidence_for_other_origin_blocks", lambda: blocks_with("origin", ev=evidence(origin="https://example.org"))),
    ("N14_unparseable_evidence_blocks", lambda: (not run(ev={"_unreadable": "x"})[0])),
    # ---- unrelated or changed dependencies --------------------------------------------------------
    ("N15_unrelated_rulesapp_item_blocks", lambda: blocks_with("no matching governance exception",
                                                               open_items=[(FALLS, item(item_id="XP-RULESAPP-RELGEAR-01"))])),
    ("N16_same_item_in_other_record_blocks",
     lambda: blocks_with("no matching governance exception",
                         open_items=[("correction_corr_safety_eebd_entry_20261019_manifest.json", item())])),
    ("N17_undeclared_path_blocks", lambda: blocks_with("no matching governance exception",
                                                       open_items=[(FALLS, item(path="RulesApp/other.json"))])),
    ("N18_other_product_blocks", lambda: blocks_with("no matching governance exception",
                                                     open_items=[(FALLS, item(product="GHGDecarb"))])),
    ("N19_item_status_not_open_blocks", lambda: blocks_with("no matching governance exception",
                                                            open_items=[(FALLS, item(status="PROPOSED_FIX"))])),
    ("N20_second_open_item_alongside_valid_one_blocks",
     lambda: blocks_with("XP-RULESAPP-RELGEAR-02",
                         open_items=[(FALLS, item()), (FALLS, item(item_id="XP-RULESAPP-RELGEAR-02"))])),
    # ---- unauthorised corrections and release scope -----------------------------------------------
    ("N21_pending_release_record_blocks", lambda: blocks_with("unauthorised correction", recs=records("PENDING_FOUNDER_DECISION"))),
    ("N22_release_record_missing_blocks",
     lambda: blocks_with("unauthorised correction", recs=records(skip="correction_corr_safety_eebd_entry_20261019_manifest.json"))),
    ("N23_extra_record_added_blocks",
     lambda: blocks_with("release scope changed",
                         facts=Facts(added=list(REAL["release"]["correction_records"]) + ["correction_corr_new_manifest.json"]))),
    ("N24_record_removed_from_scope_blocks",
     lambda: blocks_with("release scope changed", facts=Facts(added=list(REAL["release"]["correction_records"])[1:]))),
    ("N25_scope_unknown_blocks", lambda: blocks_with("release scope changed", facts=Facts(added=None))),
    ("N26_baseline_not_ancestor_blocks", lambda: blocks_with("production_baseline", facts=Facts(anc=False))),
    ("N27_candidate_not_ancestor_blocks", lambda: blocks_with("candidate_commit", facts=Facts(anc_candidate=False))),
    ("N28_dirty_tree_blocks", lambda: blocks_with("not clean", facts=Facts(clean=False))),
    # ---- unknown, edited or expired exceptions ----------------------------------------------------
    ("N29_unknown_exception_id_blocks", lambda: blocks_with("unknown exception", known={})),
    ("N30_edited_exception_breaks_pin_blocks",
     lambda: blocks_with("pinned SHA-256", files=exc_files(mod(["release", "correction_records"],
                                                               REAL["release"]["correction_records"][:8]))[0])),
    ("N31_widened_paths_edit_breaks_pin_blocks",
     lambda: blocks_with("pinned SHA-256", files=exc_files(mod(["cross_product_item", "paths"], ["RulesApp/"]))[0])),
    ("N32_expired_exception_blocks", lambda: blocks_with("expired", now=dt.datetime(2026, 12, 13, 1, tzinfo=dt.timezone.utc),
                                                         ev=evidence(checked_at_utc="2026-12-13T00:30:00Z"))),
    ("N33_not_yet_valid_blocks", lambda: blocks_with("not yet valid", now=dt.datetime(2026, 11, 11, 12, tzinfo=dt.timezone.utc),
                                                     ev=evidence(checked_at_utc="2026-11-11T11:00:00Z"))),
    ("N34_malformed_exception_blocks",
     lambda: blocks_with("missing fields", e={k: v for k, v in REAL.items() if k != "deployment_condition"})),
    ("N35_filename_mismatch_blocks",
     lambda: blocks_with("filename does not match", files={"governance_exception_other.json": exc_files()[0][REAL_NAME]})),
    ("N36_unused_but_unknown_exception_file_still_blocks",
     lambda: blocks_with("unknown exception", open_items=[], ev=None,
                         files={"governance_exception_gx_rogue.json": b'{"exception_id": "GX-ROGUE"}'}, known=exc_files()[1])),
    ("N37_unparseable_exception_file_blocks", lambda: blocks_with("unparseable", files={"governance_exception_x.json": b"{"})),
    ("N38_l4_is_not_hardcoded_pass",
     lambda: not run(open_items=[(FALLS, item())], files={}, known={})[0]),
]


def real_repo_controls():
    out = []
    files = GX.load_exception_files(HERE)
    out.append(("R1_exactly_one_exception_file_in_repo", sorted(files) == [REAL_NAME]))
    e, probs = GX.check_exception_file(REAL_NAME, files.get(REAL_NAME, b""), dt.date(2026, 11, 12))
    out.append(("R2_repo_exception_matches_pin_and_is_well_formed_on_2026_11_12", e is not None and not probs))
    out.append(("R3_repo_exception_is_known_and_unique", list(GX.KNOWN_EXCEPTIONS) == [REAL["exception_id"]]))
    fallsrec = json.loads((HERE / FALLS).read_text(encoding="utf-8"))
    xp = fallsrec["propagation"]["cross_product_safety_items"]
    out.append(("R4_rulesapp_item_still_OPEN_in_record", len(xp) == 2 and all(i["status"] == "OPEN" for i in xp)))
    out.append(("R5_repo_vercelignore_excludes_rulesapp", GX.vercelignore_excludes(GX.RepoFacts().vercelignore(), "RulesApp/")))
    # U-2 on the real files
    exempt = sorted(p.name for p in HERE.glob("correction_*_manifest.json")
                    if p.name in M.FOUNDER_AUTHORISATION_LEGACY_COMPAT_RECORDS and M._is_legacy_record(p))
    out.append(("R6_exactly_three_lp617_records_exempt_via_allowance",
                exempt == sorted(M.FOUNDER_AUTHORISATION_LEGACY_COMPAT_RECORDS)))
    safety = [p for p in HERE.glob("correction_corr_safety_*_manifest.json")]
    out.append(("R7_all_nine_safety_records_require_founder_authorisation",
                len(safety) == 9 and not any(M._is_legacy_record(p) for p in safety)))
    tmp = Path(tempfile.mkdtemp(prefix="gx_u2_"))
    try:
        name = "correction_corr_lp617_sewage_sludge_20261028_manifest.json"
        edited = tmp / name
        shutil.copyfile(HERE / name, edited)
        edited.write_bytes(edited.read_bytes() + b" ")
        out.append(("R8_edited_copy_of_allowlisted_record_is_not_exempt", not M._is_legacy_record(edited)))
        renamed = tmp / "correction_corr_lp617_sewage_sludge_20261201_manifest.json"
        shutil.copyfile(HERE / name, renamed)
        out.append(("R9_renamed_copy_of_allowlisted_record_is_not_exempt", not M._is_legacy_record(renamed)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return out


def main() -> int:
    fails, n = 0, 0
    for name, fn in CONTROLS:
        n += 1
        try:
            ok = bool(fn())
        except Exception as e:  # a crash is a FAIL, never a skip
            ok, name = False, "%s (crash: %r)" % (name, e)
        fails += 0 if ok else 1
        print("%s  %s" % ("PASS" if ok else "FAIL", name))
    try:
        rr = real_repo_controls()
    except Exception as e:
        rr = [("R_crash (%r)" % e, False)]
    for name, ok in rr:
        n += 1
        fails += 0 if ok else 1
        print("%s  %s" % ("PASS" if ok else "FAIL", name))
    print("%d checks, %d FAIL" % (n, fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
