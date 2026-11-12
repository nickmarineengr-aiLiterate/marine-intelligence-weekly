#!/usr/bin/env python3
"""Narrow, data-driven governance exceptions for the landing gate's L4 (open cross-product safety items).

L4 refuses to land while any correction record declares an OPEN cross-product safety item. A governance exception
can make ONE such item non-blocking for ONE release, and only while every condition below holds. Each failure is
fail-closed and named. There is no general bypass: an open item with no exactly matching, valid exception blocks.

An exception is honoured only if ALL of these hold:
  X1  known: its exception_id is in KNOWN_EXCEPTIONS and the file's SHA-256 equals the pinned value
      (an unknown file, or any edit to a known one, including its scope or dates, is refused)
  X2  well formed: kind, schema_version, filename = exception_id, required fields present
  X3  in date: valid_from <= today <= expires_on (UTC)
  X4  exact match: item_id, product, correction record (filename and correction_id), every declared path,
      and the item status equals required_status (OPEN)
  X5  release scope unchanged: the correction records added since production_baseline are EXACTLY the
      release's correction_records; production_baseline and candidate_commit are ancestors of HEAD
  X6  authorised: every release correction record is FOUNDER_AUTHORISED
  X7  clean tree: the working tree has no uncommitted change (the evidence binds to HEAD's tree)
  X8  not deployed (tree): .vercelignore carries the exact active rule and no negation re-includes the product
  X9  not deployed (live): a deployment-evidence file produced by verify_rulesapp_not_deployed.py for THIS
      exception and THIS tree, no older than evidence_max_age_hours and not in the future, records every probe
      path returning exactly required_status (redirects not followed)

Also, every exception file present must itself pass X1-X3, whether or not it is used ("unknown or expired
exceptions are rejected").
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
EXCEPTION_GLOB = "governance_exception_*.json"

# Closed list. Adding or changing an exception changes this pin, which is a reviewed governance change.
KNOWN_EXCEPTIONS = {
    "GX-S1-RULESAPP-FALLS-20261112": "43396f417207278a387e00c03129ec2c1cf7143ed235a1d73244c03e74b6b9d2",
}

_REQUIRED = ("exception_id", "kind", "schema_version", "gate", "decision", "authorises", "product", "release",
             "cross_product_item", "rulesapp_obligation", "deployment_condition", "valid_from", "expires_on")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def exception_filename(exception_id: str) -> str:
    return "governance_exception_%s.json" % exception_id.lower().replace("-", "_")


def check_exception_file(name: str, raw: bytes, today: _dt.date, known=None) -> tuple[dict | None, list[str]]:
    """X1-X3 for one exception file. Returns (parsed or None, problems)."""
    known = KNOWN_EXCEPTIONS if known is None else known
    probs = []
    try:
        e = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as err:
        return None, ["%s: unparseable (%s)" % (name, err)]
    if not isinstance(e, dict):
        return None, ["%s: not an object" % name]
    eid = e.get("exception_id")
    if eid not in known:
        probs.append("%s: unknown exception %r (not in KNOWN_EXCEPTIONS)" % (name, eid))
    elif sha256_bytes(raw) != known[eid]:
        probs.append("%s: exception %s does not match its pinned SHA-256 (edited or replaced)" % (name, eid))
    missing = [k for k in _REQUIRED if k not in e]
    if missing:
        probs.append("%s: missing fields %s" % (name, missing))
    if e.get("kind") != "GOVERNANCE_EXCEPTION" or e.get("schema_version") != 1:
        probs.append("%s: wrong kind/schema_version" % name)
    if isinstance(eid, str) and name != exception_filename(eid):
        probs.append("%s: filename does not match exception_id %s" % (name, eid))
    try:
        vf = _dt.date.fromisoformat(e.get("valid_from", ""))
        ex = _dt.date.fromisoformat(e.get("expires_on", ""))
        if today < vf:
            probs.append("%s: not yet valid (valid_from %s)" % (name, vf))
        if today > ex:
            probs.append("%s: expired (expires_on %s)" % (name, ex))
    except (TypeError, ValueError):
        probs.append("%s: bad valid_from/expires_on" % name)
    return (None if probs else e), probs


def vercelignore_excludes(text: str, rule: str) -> bool:
    """X8: the exact rule is an active line and no negation (!...) re-includes anything under it."""
    lines = [l.strip() for l in text.splitlines()]
    active = [l for l in lines if l and not l.startswith("#")]
    stem = rule.rstrip("/")
    if rule not in active:
        return False
    return not any(l.startswith("!") and l[1:].lstrip("/").startswith(stem) for l in active)


def evidence_problems(ev: dict | None, exc: dict, head_tree: str, now: _dt.datetime) -> list[str]:
    """X9."""
    if ev is None:
        return ["no deployment evidence supplied (--deployment-evidence)"]
    dc = exc["deployment_condition"]
    probs = []
    if ev.get("exception_id") != exc["exception_id"]:
        probs.append("evidence is for exception %r" % ev.get("exception_id"))
    if ev.get("tree") != head_tree:
        probs.append("evidence tree %s != HEAD tree %s" % (ev.get("tree"), head_tree))
    if ev.get("origin") != dc["live_origin"]:
        probs.append("evidence origin %r != %r" % (ev.get("origin"), dc["live_origin"]))
    try:
        at = _dt.datetime.fromisoformat(str(ev.get("checked_at_utc")).replace("Z", "+00:00"))
        if at.tzinfo is None:
            raise ValueError("naive timestamp")
        age_h = (now - at).total_seconds() / 3600.0
        if age_h < -0.1:
            probs.append("evidence timestamp is in the future")
        elif age_h > dc["evidence_max_age_hours"]:
            probs.append("evidence is %.1f h old (max %s h)" % (age_h, dc["evidence_max_age_hours"]))
    except (TypeError, ValueError) as err:
        probs.append("bad evidence timestamp (%s)" % err)
    got = {p.get("path"): p for p in ev.get("probes") or [] if isinstance(p, dict)}
    for path in dc["live_probe_paths"]:
        p = got.get(path)
        if p is None:
            probs.append("probe %s missing from evidence" % path)
        elif p.get("status") != dc["required_status"] or p.get("redirect_followed") is not False:
            probs.append("probe %s status %r (required %s, no redirect)" % (path, p.get("status"), dc["required_status"]))
    return probs


def item_matches(exc: dict, manifest_name: str, manifest: dict, item: dict) -> bool:
    """X4."""
    x = exc["cross_product_item"]
    return (item.get("item_id") == x["item_id"] and item.get("product") == x["product"]
            and item.get("status") == x["required_status"]
            and manifest_name == x["correction_manifest"] and manifest.get("correction_id") == x["correction_id"]
            and item.get("path") in x["paths"])


def release_problems(exc: dict, facts, records: dict) -> list[str]:
    """X5-X8 (facts: object with added_records(base), is_ancestor(c), clean(), head_tree(), vercelignore())."""
    rel = exc["release"]
    probs = []
    if not facts.is_ancestor(rel["production_baseline"]):
        probs.append("production_baseline %s is not an ancestor of HEAD" % rel["production_baseline"][:10])
    if not facts.is_ancestor(rel["candidate_commit"]):
        probs.append("candidate_commit %s is not an ancestor of HEAD" % rel["candidate_commit"][:10])
    added = facts.added_records(rel["production_baseline"])
    if added is None or sorted(added) != sorted(rel["correction_records"]):
        probs.append("release scope changed: records added since baseline %s != declared %d"
                     % (sorted(added) if added is not None else "UNKNOWN", len(rel["correction_records"])))
    for name in rel["correction_records"]:
        st = ((records.get(name) or {}).get("founder_authorisation") or {}).get("state")
        if st != "FOUNDER_AUTHORISED":
            probs.append("unauthorised correction %s (state %s)" % (name, st))
    if not facts.clean():
        probs.append("working tree not clean")
    if not vercelignore_excludes(facts.vercelignore(), exc["deployment_condition"]["vercelignore_rule"]):
        probs.append("%s is not excluded by .vercelignore (deployed product): exception does not apply"
                     % exc["cross_product_item"]["product"])
    return probs


def evaluate_l4(records: dict, open_items: list, exception_files: dict, facts, evidence, now: _dt.datetime,
                known=None) -> tuple[bool, list[str], list[str]]:
    """Pure L4. records: {manifest_name: manifest}; open_items: [(manifest_name, item_dict)];
    exception_files: {filename: raw bytes}. Returns (ok, blocking reasons, informational lines)."""
    blocks, info, valid = [], [], []
    for name, raw in sorted(exception_files.items()):
        e, probs = check_exception_file(name, raw, now.date(), known)
        blocks += probs
        if e is not None:
            valid.append(e)
    for mname, item in open_items:
        label = "%s: %s (%s)" % (mname, item.get("item_id"), item.get("product"))
        cands = [e for e in valid if item_matches(e, mname, records.get(mname) or {}, item)]
        if not cands:
            blocks.append("%s OPEN with no matching governance exception" % label)
            continue
        e = cands[0]
        probs = release_problems(e, facts, records) + evidence_problems(evidence, e, facts.head_tree(), now)
        if probs:
            blocks.append("%s: exception %s does not apply: %s" % (label, e["exception_id"], "; ".join(probs)))
        else:
            info.append("%s: non-blocking under %s (item stays OPEN)" % (label, e["exception_id"]))
    return (not blocks), blocks, info


class RepoFacts:
    """The real repository, read-only."""

    def __init__(self, repo: pathlib.Path = REPO):
        self.repo = repo

    def _git(self, *a):
        return subprocess.run(["git", *a], cwd=str(self.repo), capture_output=True, text=True, check=False)

    def is_ancestor(self, c):
        return self._git("merge-base", "--is-ancestor", c, "HEAD").returncode == 0

    def added_records(self, base):
        r = self._git("diff", "--name-only", "--diff-filter=A", base, "HEAD", "--", "tools/oral/")
        if r.returncode != 0:
            return None
        return [pathlib.Path(p).name for p in r.stdout.split()
                if pathlib.Path(p).name.startswith("correction_") and p.endswith("_manifest.json")]

    def clean(self):
        r = self._git("status", "--porcelain")
        return r.returncode == 0 and r.stdout.strip() == ""

    def head_tree(self):
        return self._git("rev-parse", "HEAD^{tree}").stdout.strip()

    def vercelignore(self):
        p = self.repo / ".vercelignore"
        return p.read_text(encoding="utf-8") if p.exists() else ""


def load_exception_files(directory: pathlib.Path = HERE) -> dict:
    return {p.name: p.read_bytes() for p in sorted(directory.glob(EXCEPTION_GLOB))}
