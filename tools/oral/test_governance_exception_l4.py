#!/usr/bin/env python3
"""Positive and negative controls for the L4 governance exception (governance_exceptions.py) and the U-2
three-record compatibility allowance (oral_manifest.FOUNDER_AUTHORISATION_LEGACY_COMPAT_RECORDS).

Part A  pure: in-memory fixtures and a fake HEAD.
Part B  hermetic real git: a throwaway repository in a temporary directory OUTSIDE this repository, one positive
        case and every bypass found by the independent review R6 (F1-F6), each run through RepoFacts.
Part C  the real repository, read-only.
Every control states what MUST block or pass. A crash is a FAIL. Prints "<N> checks, <M> FAIL".
"""
from __future__ import annotations

import copy
import datetime as dt
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import governance_exceptions as GX  # noqa: E402
import oral_manifest as M  # noqa: E402

REAL_NAME = "governance_exception_gx_s1_rulesapp_falls_20261112.json"
REAL = json.loads((HERE / REAL_NAME).read_text(encoding="utf-8"))
FALLS = REAL["cross_product_item"]["correction_manifest"]
NOW = dt.datetime(2026, 11, 12, 12, 0, tzinfo=dt.timezone.utc)
COMMIT, TREE = "c" * 40, "t" * 40
VI_OK = "# comment\nnode_modules/\nRulesApp/\n"
_D = object()


# =================================================================================================== Part A
def raw_of(e):
    return json.dumps(e, indent=1).encode("utf-8")


def known_for(e):
    return {e["exception_id"]: GX.sha256_bytes(raw_of(e))}


class Facts:
    """A fake HEAD that matches REAL's pins unless told otherwise."""

    def __init__(self, changed=_D, blobs=None, anc=True, anc_candidate=True, clean=(), vi=VI_OK, items=_D,
                 state="FOUNDER_AUTHORISED", skip_record=None, tree=TREE, commit=COMMIT):
        pin = REAL["release"]["diff_pin"]
        self._changed = {p: v["status"] for p, v in pin.items()} if changed is _D else changed
        self._blobs = {p: v["blob"] for p, v in pin.items()}
        self._blobs.update(blobs or {})
        self._anc, self._anc_c, self._clean, self._vi = anc, anc_candidate, list(clean), vi
        self._items = copy.deepcopy(REAL["cross_product_item"]["items"]) if items is _D else items
        self._state, self._skip, self._tree, self._commit = state, skip_record, tree, commit

    def head_commit(self):
        return self._commit

    def head_tree(self):
        return self._tree

    def is_ancestor(self, c):
        return self._anc_c if c == REAL["release"]["candidate_commit"] else self._anc

    def changed_paths(self, base):
        return self._changed

    def blob_at_head(self, p):
        return self._blobs.get(p)

    def show_head(self, p):
        return self._vi if p == ".vercelignore" else None

    def head_record(self, name):
        if name == self._skip or name not in REAL["release"]["correction_records"]:
            return None
        r = {"correction_id": REAL["cross_product_item"]["correction_id"] if name == FALLS else name,
             "founder_authorisation": {"state": self._state}}
        if name == FALLS:
            r["propagation"] = {"cross_product_safety_items": self._items}
        return r

    def clean_problems(self):
        return self._clean


def evidence(e=None, **kw):
    e = REAL if e is None else e
    dc = e["deployment_condition"]
    ev = {"kind": "DEPLOYMENT_EVIDENCE", "result": "NOT_DEPLOYED", "exception_id": e["exception_id"],
          "exception_sha256": GX.sha256_bytes(raw_of(e)), "commit": COMMIT, "tree": TREE, "clean": True,
          "vercelignore_excludes": True, "origin": dc["live_origin"], "checked_at_utc": "2026-11-12T11:00:00Z",
          "probes": [{"path": p, "status": 404, "redirect_followed": False} for p in dc["live_probe_paths"]]}
    ev.update(kw)
    return ev


def item(**kw):
    d = dict(REAL["cross_product_item"]["items"][0])
    d.update(kw)
    return d


def run(open_items=None, facts=None, ev=_D, e=None, files=None, known=None, now=NOW):
    e = REAL if e is None else e
    files = {GX.exception_filename(e["exception_id"]): raw_of(e)} if files is None else files
    known = known_for(e) if known is None else known
    open_items = [(FALLS, item())] if open_items is None else open_items
    ok, blocks, _ = GX.evaluate_l4(open_items, files, facts or Facts(), evidence(e) if ev is _D else ev, now, known)
    return ok, " | ".join(blocks)


def blocks_with(fragment, **kw):
    ok, why = run(**kw)
    return (not ok) and fragment in why


def mod(path, value):
    e = copy.deepcopy(REAL)
    cur = e
    for k in path[:-1]:
        cur = cur[k]
    cur[path[-1]] = value
    return e


def probes_with(i, **kw):
    return [dict(p, **kw) if j == i else p for j, p in enumerate(evidence()["probes"])]


PIN = REAL["release"]["diff_pin"]
SOME_PAGE = next(p for p in PIN if p.startswith("meoclass1/"))

CONTROLS = [
    ("P1_exact_item_valid_exception_fresh_evidence_passes", lambda: run()[0]),
    ("P2_both_declared_items_pass", lambda: run(open_items=[(FALLS, i) for i in REAL["cross_product_item"]["items"]])[0]),
    ("P3_no_open_items_passes_without_evidence", lambda: run(open_items=[], ev=None)[0]),
    # deployed product (tree)
    ("N1_vercelignore_rule_removed_blocks", lambda: blocks_with("may be deployed", facts=Facts(vi="node_modules/\n"))),
    ("N2_vercelignore_rule_commented_blocks", lambda: blocks_with("may be deployed", facts=Facts(vi="# RulesApp/\n"))),
    ("N3_any_negation_line_blocks", lambda: all(blocks_with("negation", facts=Facts(vi=VI_OK + n + "\n"))
                                                for n in ("!R*", "!**/RulesApp/", "!rulesapp/", "!*", " !RulesApp/"))),
    ("N4_indented_rule_blocks", lambda: blocks_with("may be deployed", facts=Facts(vi="node_modules/\n  RulesApp/\n"))),
    ("N5_vercelignore_missing_blocks", lambda: blocks_with("missing at HEAD", facts=Facts(vi=None))),
    ("N6_deployment_surface_change_blocks",
     lambda: all(blocks_with("deployment surface", facts=Facts(changed=dict(Facts()._changed, **{p: "M"})))
                 for p in (".vercelignore", "vercel.json", "middleware.js", "api/x.js", "RulesApp/a.json"))),
    # deployed product (live evidence)
    ("N7_live_probe_200_blocks", lambda: blocks_with("status 200", ev=evidence(probes=probes_with(2, status=200)))),
    ("N8_live_probe_redirect_blocks", lambda: blocks_with("status 302", ev=evidence(probes=probes_with(0, status=302)))),
    ("N9_probe_followed_redirect_blocks", lambda: blocks_with("no redirect", ev=evidence(probes=probes_with(0, redirect_followed=True)))),
    ("N10_probe_missing_blocks", lambda: blocks_with("missing from evidence", ev=evidence(probes=evidence()["probes"][1:]))),
    ("N11_duplicate_probe_blocks", lambda: blocks_with("duplicate probe", ev=evidence(probes=evidence()["probes"] + [dict(evidence()["probes"][0])]))),
    # evidence identity
    ("N12_missing_evidence_blocks", lambda: blocks_with("no deployment evidence", ev=None)),
    ("N13_non_object_evidence_blocks", lambda: blocks_with("not a JSON object", ev=[1, 2])),
    ("N14_stale_evidence_blocks", lambda: blocks_with("h old", ev=evidence(checked_at_utc="2026-11-10T11:00:00Z"))),
    ("N15_future_evidence_blocks", lambda: blocks_with("future", ev=evidence(checked_at_utc="2026-11-13T11:00:00Z"))),
    ("N16_naive_timestamp_blocks", lambda: blocks_with("timestamp", ev=evidence(checked_at_utc="2026-11-12T11:00:00"))),
    ("N17_evidence_other_tree_blocks", lambda: blocks_with("commit/tree", ev=evidence(tree="x" * 40))),
    ("N18_evidence_other_commit_blocks", lambda: blocks_with("commit/tree", ev=evidence(commit="d" * 40))),
    ("N19_evidence_other_exception_blocks", lambda: blocks_with("evidence is for", ev=evidence(exception_id="GX-OTHER"))),
    ("N20_evidence_wrong_exception_sha_blocks", lambda: blocks_with("exception_sha256", ev=evidence(exception_sha256="0" * 64))),
    ("N21_evidence_result_deployed_blocks", lambda: blocks_with("evidence result", ev=evidence(result="DEPLOYED_OR_UNKNOWN"))),
    ("N22_evidence_wrong_kind_blocks", lambda: blocks_with("evidence kind", ev=evidence(kind=None))),
    ("N23_evidence_not_clean_blocks", lambda: blocks_with("clean=False", ev=evidence(clean=False))),
    ("N24_evidence_vercelignore_false_blocks", lambda: blocks_with("vercelignore_excludes=False", ev=evidence(vercelignore_excludes=False))),
    ("N25_evidence_other_origin_blocks", lambda: blocks_with("origin", ev=evidence(origin="https://example.org"))),
    ("N26_empty_head_tree_blocks", lambda: blocks_with("commit/tree", facts=Facts(tree=""), ev=evidence(tree=""))),
    # unrelated or changed dependencies
    ("N27_unrelated_rulesapp_item_blocks", lambda: blocks_with("no matching governance exception", open_items=[(FALLS, item(item_id="XP-RULESAPP-RELGEAR-01"))])),
    ("N28_same_item_other_record_blocks", lambda: blocks_with("no matching", open_items=[(REAL["release"]["correction_records"][1], item())])),
    ("N29_undeclared_path_blocks", lambda: blocks_with("no matching", open_items=[(FALLS, item(path="RulesApp/other.json"))])),
    ("N30_other_product_blocks", lambda: blocks_with("no matching", open_items=[(FALLS, item(product="GHGDecarb"))])),
    ("N31_item_status_not_open_blocks", lambda: blocks_with("no matching", open_items=[(FALLS, item(status="PROPOSED_FIX"))])),
    ("N32_second_unrelated_item_blocks", lambda: blocks_with("XP-RULESAPP-RELGEAR-02", open_items=[(FALLS, item()), (FALLS, item(item_id="XP-RULESAPP-RELGEAR-02"))])),
    ("N33_extra_item_same_id_in_record_blocks (R6 F5)",
     lambda: blocks_with("differ from the pinned list",
                         facts=Facts(items=REAL["cross_product_item"]["items"] + [dict(REAL["cross_product_item"]["items"][0], proposition="other")]))),
    ("N34_item_match_text_changed_blocks", lambda: blocks_with("differ from the pinned list",
                                                              facts=Facts(items=[dict(i, match="x") for i in REAL["cross_product_item"]["items"]]))),
    ("N35_non_object_item_does_not_crash_and_blocks", lambda: blocks_with("no matching", open_items=[(FALLS, "XP")])),
    # authorisation and release scope
    ("N36_pending_release_record_blocks", lambda: blocks_with("unauthorised correction", facts=Facts(state="PENDING_FOUNDER_DECISION"))),
    ("N37_release_record_missing_blocks", lambda: blocks_with("unauthorised correction", facts=Facts(skip_record=REAL["release"]["correction_records"][0]))),
    ("N38_unpinned_path_added_blocks (R6 F3)", lambda: blocks_with("unpinned path", facts=Facts(changed=dict(Facts()._changed, **{"assets/ra/repo-data.json": "A"})))),
    ("N39_pinned_path_dropped_blocks", lambda: blocks_with("no longer differ", facts=Facts(changed={p: s for p, s in Facts()._changed.items() if p != SOME_PAGE}))),
    ("N40_pinned_content_changed_blocks", lambda: blocks_with("differs from the pinned blob", facts=Facts(blobs={SOME_PAGE: "0" * 40}))),
    ("N41_status_changed_blocks", lambda: blocks_with("status", facts=Facts(changed=dict(Facts()._changed, **{SOME_PAGE: "D"})))),
    ("N42_extra_record_added_blocks", lambda: blocks_with("correction records", facts=Facts(changed=dict(Facts()._changed, **{"tools/oral/correction_corr_rogue_20261112_manifest.json": "A"})))),
    ("N43_existing_record_edited_blocks (R6 F4)", lambda: blocks_with("correction records", facts=Facts(changed=dict(Facts()._changed, **{"tools/oral/correction_corr_annexvi_eif_20260901_manifest.json": "M"})))),
    ("N44_scope_unknown_blocks", lambda: blocks_with("scope unknown", facts=Facts(changed=None))),
    ("N45_baseline_not_ancestor_blocks", lambda: blocks_with("production_baseline", facts=Facts(anc=False))),
    ("N46_candidate_not_ancestor_blocks", lambda: blocks_with("candidate_commit", facts=Facts(anc_candidate=False))),
    ("N47_not_clean_blocks (R6 F2)", lambda: blocks_with("skip-worktree", facts=Facts(clean=["skip-worktree or assume-unchanged index entries"]))),
    # unknown, edited or expired exceptions
    ("N48_unknown_exception_blocks", lambda: blocks_with("unknown exception", known={})),
    ("N49_edited_exception_breaks_pin_blocks", lambda: blocks_with("pinned SHA-256", files={REAL_NAME: raw_of(mod(["expires_on"], "2027-12-31"))})),
    ("N50_expired_blocks", lambda: blocks_with("expired", now=dt.datetime(2026, 12, 13, 1, tzinfo=dt.timezone.utc), ev=evidence(checked_at_utc="2026-12-13T00:30:00Z"))),
    ("N51_not_yet_valid_blocks", lambda: blocks_with("not yet valid", now=dt.datetime(2026, 11, 11, 12, tzinfo=dt.timezone.utc), ev=evidence(checked_at_utc="2026-11-11T11:00:00Z"))),
    ("N52_malformed_blocks", lambda: blocks_with("missing fields", e={k: v for k, v in REAL.items() if k != "deployment_condition"},
                                          ev=evidence())),
    ("N53_empty_diff_pin_blocks", lambda: blocks_with("malformed body", e=mod(["release", "diff_pin"], {}))),
    ("N54_filename_mismatch_blocks", lambda: blocks_with("filename does not match", files={"governance_exception_other.json": raw_of(REAL)})),
    ("N55_unused_unknown_file_blocks", lambda: blocks_with("unknown exception", open_items=[], ev=None, files={"governance_exception_gx_rogue.json": b'{"exception_id": "GX-ROGUE"}'})),
    ("N56_unparseable_file_blocks", lambda: blocks_with("unparseable", files={"governance_exception_x.json": b"{"})),
    ("N57_l4_is_not_hardcoded_pass", lambda: not run(files={}, known={})[0]),
]


# =================================================================================================== Part B
def git(repo, *a, check=True):
    r = subprocess.run(["git", "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "-c", "core.autocrlf=false",
                        *a], cwd=str(repo), capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError("git %s: %s" % (a, r.stderr.strip()))
    return r.stdout.strip()


def write(repo, rel, text):
    p = Path(repo) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode("utf-8"))


def build_fixture():
    """B (baseline) -> C1 (content + records) -> C2 (module + exception). Returns (repo, exception, raw, known)."""
    repo = Path(tempfile.mkdtemp(prefix="gx_fixture_"))
    git(repo, "init", "-q")
    write(repo, ".vercelignore", VI_OK)
    write(repo, ".gitignore", "*.local.json\n")
    write(repo, "vercel.json", "{}\n")
    write(repo, "RulesApp/repository/index/repo-data.json", '{"falls": "wrong"}\n')
    write(repo, "meoclass1/QB1_E.html", "<p>falls wrong</p>\n")
    write(repo, "tools/oral/correction_corr_old_20260901_manifest.json", '{"correction_id": "OLD"}\n')
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "baseline")
    base = git(repo, "rev-parse", "HEAD")
    items = [{"item_id": "XP-T-01", "product": "RulesApp", "status": "OPEN", "path": "RulesApp/repository/index/repo-data.json",
              "proposition": "p", "match": "wrong"}]
    rec = {"correction_id": "CORR-T-FALLS", "founder_authorisation": {"state": "FOUNDER_AUTHORISED"},
           "propagation": {"cross_product_safety_items": items}}
    write(repo, "meoclass1/QB1_E.html", "<p>falls right</p>\n")
    write(repo, "tools/oral/correction_corr_t_falls_manifest.json", json.dumps(rec) + "\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "content")
    cand = git(repo, "rev-parse", "HEAD")
    eid = "GX-T-20261112"
    ename = GX.exception_filename(eid)
    pin = {p: {"status": s, "blob": git(repo, "rev-parse", "HEAD:%s" % p)}
           for p, s in GX.RepoFacts(repo).changed_paths(base).items()}
    pin["tools/oral/governance_exceptions.py"] = {"status": "A", "blob": GX.SELF}
    pin["tools/oral/" + ename] = {"status": "A", "blob": GX.SELF}
    e = copy.deepcopy(REAL)
    e.update(exception_id=eid)
    e["release"] = {"release_id": "T", "production_baseline": base, "candidate_commit": cand,
                    "correction_records": ["correction_corr_t_falls_manifest.json"], "diff_pin": pin}
    e["cross_product_item"] = {"item_id": "XP-T-01", "product": "RulesApp", "required_status": "OPEN",
                               "correction_id": "CORR-T-FALLS", "correction_manifest": "correction_corr_t_falls_manifest.json",
                               "paths": ["RulesApp/repository/index/repo-data.json"], "items": items}
    raw = raw_of(e)
    write(repo, "tools/oral/governance_exceptions.py", "# stand-in\n")
    (repo / "tools/oral" / ename).write_bytes(raw)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "exception")
    return repo, e, raw, {eid: GX.sha256_bytes(raw)}


def fixture_eval(repo, e, raw, known, now=NOW, ev_over=None):
    f = GX.RepoFacts(repo)
    ev = evidence(e, commit=f.head_commit(), tree=f.head_tree(), exception_sha256=known[e["exception_id"]])
    ev.update(ev_over or {})
    files = {p.name: p.read_bytes() for p in sorted((repo / "tools/oral").glob(GX.EXCEPTION_GLOB))}
    rec = f.head_record(e["cross_product_item"]["correction_manifest"]) or {}
    items = ((rec.get("propagation") or {}).get("cross_product_safety_items")) or []
    ok, blocks, _ = GX.evaluate_l4([(e["cross_product_item"]["correction_manifest"], i) for i in items],
                                   files, f, ev, now, known)
    return ok, " | ".join(blocks)


def hermetic_controls():
    out = []
    repo, e, raw, known = build_fixture()
    c2 = git(repo, "rev-parse", "HEAD")

    def attack(name, fragment, steps, ev_over=None):
        try:
            steps()
            ok, why = fixture_eval(repo, e, raw, known, ev_over=ev_over)
            out.append((name, (not ok) and fragment in why, why[:300]))
        finally:
            git(repo, "update-index", "--no-skip-worktree", ".vercelignore", check=False)
            git(repo, "update-index", "--no-assume-unchanged", "vercel.json", check=False)
            git(repo, "reset", "-q", "--hard", c2)
            git(repo, "clean", "-qfdx")

    def commit_all(msg):
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", msg)

    try:
        ok, why = fixture_eval(repo, e, raw, known)
        out.append(("B0_fixture_positive_passes_in_real_git", ok, why[:300]))
        out.append(("B1_bad_sha_is_not_ancestor", not GX.RepoFacts(repo).is_ancestor("z" * 40)
                    and not GX.RepoFacts(repo).is_ancestor("HEAD"), ""))
        for n, line in (("bang_R_star", "!R*"), ("bang_globstar", "!**/RulesApp/"), ("bang_lowercase", "!rulesapp/")):
            attack("B2_F1_vercelignore_%s_blocks" % n, "deployment surface",
                   lambda line=line: (write(repo, ".vercelignore", VI_OK + line + "\n"), commit_all("f1")))
        attack("B3_F1_indented_rule_blocks", "may be deployed",
               lambda: (write(repo, ".vercelignore", "node_modules/\n  RulesApp/\n"), commit_all("f1i")))
        attack("B4_F2_skip_worktree_hides_bad_head_blocks", "skip-worktree",
               lambda: (write(repo, ".vercelignore", "node_modules/\n"), commit_all("f2"),
                        write(repo, ".vercelignore", VI_OK),
                        git(repo, "update-index", "--skip-worktree", ".vercelignore")))
        attack("B5_F2_assume_unchanged_blocks", "skip-worktree",
               lambda: (git(repo, "update-index", "--assume-unchanged", "vercel.json"),
                        write(repo, "vercel.json", '{"rewrites": []}\n')))
        attack("B6_F3_rulesapp_content_copied_elsewhere_blocks", "unpinned path",
               lambda: (write(repo, "assets/ra/repo-data.json", '{"falls": "wrong"}\n'), commit_all("f3")))
        attack("B7_F3_vercel_json_rewrite_blocks", "deployment surface",
               lambda: (write(repo, "vercel.json", '{"rewrites": [{"source": "/x", "destination": "/RulesApp/"}]}\n'),
                        commit_all("f3r")))
        attack("B8_F4_rename_existing_record_blocks", "correction records",
               lambda: (git(repo, "mv", "tools/oral/correction_corr_old_20260901_manifest.json",
                            "tools/oral/correction_corr_rogue_20261112_manifest.json"), commit_all("f4")))
        attack("B9_F4_edit_existing_record_blocks", "correction records",
               lambda: (write(repo, "tools/oral/correction_corr_old_20260901_manifest.json", '{"correction_id": "OLD2"}\n'),
                        commit_all("f4m")))
        attack("B10_F5_extra_item_same_id_blocks", "differ from the pinned list",
               lambda: (write(repo, "tools/oral/correction_corr_t_falls_manifest.json", json.dumps(
                   {"correction_id": "CORR-T-FALLS", "founder_authorisation": {"state": "FOUNDER_AUTHORISED"},
                    "propagation": {"cross_product_safety_items": e["cross_product_item"]["items"] + [
                        dict(e["cross_product_item"]["items"][0], proposition="other")]}}) + "\n"), commit_all("f5")))
        attack("B11_untracked_file_blocks", "uncommitted or untracked",
               lambda: write(repo, "tools/oral/notes.txt", "x\n"))
        attack("B12_ignored_json_under_tools_oral_blocks", "ignored",
               lambda: write(repo, "tools/oral/shadow.local.json", "{}\n"))
        attack("B13_F6_hand_written_evidence_for_other_commit_blocks", "commit/tree", lambda: None,
               ev_over={"commit": "0" * 40})
        attack("B14_unrelated_page_change_blocks", "unpinned path",
               lambda: (write(repo, "meoclass1/QB9_Z.html", "<p>new</p>\n"), commit_all("page")))
    finally:
        shutil.rmtree(repo, ignore_errors=True)
    return out


# =================================================================================================== Part C
def real_repo_controls():
    out = []
    files = GX.load_exception_files(HERE)
    out.append(("R1_exactly_one_exception_file_in_repo", sorted(files) == [REAL_NAME]))
    e, probs = GX.check_exception_file(REAL_NAME, files.get(REAL_NAME, b""), dt.date(2026, 11, 12))
    out.append(("R2_repo_exception_matches_pin_and_is_well_formed_on_2026_11_12", e is not None and not probs))
    out.append(("R3_repo_exception_is_known_and_unique", list(GX.KNOWN_EXCEPTIONS) == [REAL["exception_id"]]))
    fallsrec = json.loads((HERE / FALLS).read_text(encoding="utf-8"))
    xp = fallsrec["propagation"]["cross_product_safety_items"]
    out.append(("R4_rulesapp_item_still_OPEN_and_equal_to_pinned_items",
                len(xp) == 2 and all(i["status"] == "OPEN" for i in xp)
                and [GX._canon_item(i) for i in xp] == [GX._canon_item(i) for i in REAL["cross_product_item"]["items"]]))
    out.append(("R5_head_vercelignore_passes_necessary_conditions",
                GX.vercelignore_problems(GX.RepoFacts().show_head(".vercelignore"), "RulesApp/") == []))
    out.append(("R5b_diff_pin_has_no_deployment_surface_path",
                not [p for p in REAL["release"]["diff_pin"] if p.startswith(GX.DEPLOY_SURFACE) or p in GX.DEPLOY_SURFACE]))
    exempt = sorted(p.name for p in HERE.glob("correction_*_manifest.json")
                    if p.name in M.FOUNDER_AUTHORISATION_LEGACY_COMPAT_RECORDS and M._is_legacy_record(p))
    out.append(("R6_exactly_three_lp617_records_exempt_via_allowance", exempt == sorted(M.FOUNDER_AUTHORISATION_LEGACY_COMPAT_RECORDS)))
    safety = list(HERE.glob("correction_corr_safety_*_manifest.json"))
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
    return [(n, ok, "") for n, ok in out]


def main() -> int:
    fails, n = 0, 0
    rows = []
    for name, fn in CONTROLS:
        try:
            rows.append((name, bool(fn()), ""))
        except Exception as e:  # a crash is a FAIL, never a skip
            rows.append(("%s (crash: %r)" % (name, e), False, ""))
    for part in (hermetic_controls, real_repo_controls):
        try:
            rows += part()
        except Exception as e:
            rows.append(("%s crash (%r)" % (part.__name__, e), False, ""))
    for name, ok, why in rows:
        n += 1
        fails += 0 if ok else 1
        print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  -- " + why) if (why and not ok) else ""))
    print("%d checks, %d FAIL" % (n, fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
