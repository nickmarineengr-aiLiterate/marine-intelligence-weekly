#!/usr/bin/env python3
"""Narrow, data-driven governance exceptions for the landing gate's L4 (open cross-product safety items).

L4 refuses to land while any correction record declares an OPEN cross-product safety item. A governance exception
can make ONE such item non-blocking for ONE release, and only while every condition below holds. Each failure is
fail-closed and named. There is no general bypass: an open item with no exactly matching, valid exception blocks.

Everything is judged from the COMMITTED tree (HEAD), never from the working tree.

An exception is honoured only if ALL of these hold:
  X1  known: its exception_id is in KNOWN_EXCEPTIONS and the file's SHA-256 equals the pinned value
      (an unknown file, or any edit to a known one, including its scope or dates, is refused)
  X2  well formed: kind, schema_version, filename = exception_id, required fields present
  X3  in date: valid_from <= today <= expires_on (UTC)
  X4  exact match: item_id, product, correction record (filename and correction_id), declared path, status OPEN;
      AND the record at HEAD declares exactly the pinned item list (count, ids, paths, match text), so no other
      defect can hide under the same id
  X5  release scope pinned: `git diff --no-renames --name-status <production_baseline> HEAD` is EXACTLY the
      exception's diff_pin (same paths, same A/M status, and the same git blob at HEAD for every pinned path).
      Nothing else in the repository may differ from the production baseline: no other page, record, config,
      .vercelignore, vercel.json, middleware, copied RulesApp content, rename or deletion. The correction
      records added are exactly the release's nine. production_baseline and candidate_commit are ancestors of HEAD.
  X6  authorised: every release correction record AT HEAD is FOUNDER_AUTHORISED
  X7  clean: no uncommitted change, no skip-worktree / assume-unchanged index entry, no ignored *.json under
      tools/oral/ (an ignored file could shadow what the gate reads)
  X8  not deployed (tree): no deployment-surface file differs from the production baseline (implied by X5, checked
      by name for a clear reason), and HEAD's .vercelignore has the exact rule line, no negation line and no
      indented line (deploy_set.mjs's own refusals). Because X5 makes the deployment surface byte-identical to
      the production baseline, the live probes of X9 speak for the candidate's surface too.
  X9  not deployed (live): a deployment-evidence file from verify_rulesapp_not_deployed.py for THIS exception (its
      pinned SHA-256), THIS HEAD commit and tree, kind DEPLOYMENT_EVIDENCE, result NOT_DEPLOYED, clean, no older
      than evidence_max_age_hours and not in the future, every probe path present exactly once and returning
      exactly required_status with no redirect followed. It attests to production as it stands at the time of the
      probe (= the baseline deployment); it is re-run immediately before and after any push.

Every exception file present (committed or not) must itself pass X1-X3, whether or not it is used.
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
ORAL = "tools/oral/"
# Deployment surface: never allowed to differ from the production baseline under an exception.
DEPLOY_SURFACE = (".vercelignore", "vercel.json", "middleware.js", "package.json", "package-lock.json", "api/",
                  ".github/", "RulesApp/")
SELF = "SELF"  # diff_pin value for the two files that cannot pin themselves (this module and the exception file)

# Closed list. Adding or changing an exception changes this pin, which is a reviewed governance change.
KNOWN_EXCEPTIONS = {
    "GX-S1-RULESAPP-FALLS-20261112": "__PIN__",
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
    if not isinstance(eid, str) or eid not in known:
        probs.append("%s: unknown exception %r (not in KNOWN_EXCEPTIONS)" % (name, eid))
    elif sha256_bytes(raw) != known[eid]:
        probs.append("%s: exception %s does not match its pinned SHA-256 (edited or replaced)" % (name, eid))
    missing = [k for k in _REQUIRED if k not in e]
    if missing:
        probs.append("%s: missing fields %s" % (name, missing))
    if e.get("kind") != "GOVERNANCE_EXCEPTION" or e.get("schema_version") != 2:
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
    if not probs:
        try:
            _shape(e)
        except (KeyError, TypeError, ValueError) as err:
            probs.append("%s: malformed body (%s)" % (name, err))
    return (None if probs else e), probs


def _shape(e):
    """Raise on a body the evaluator cannot read safely (fail closed before any matching)."""
    rel, x, dc = e["release"], e["cross_product_item"], e["deployment_condition"]
    for k in ("release_id", "production_baseline", "candidate_commit"):
        if not isinstance(rel[k], str) or not rel[k]:
            raise ValueError("release.%s" % k)
    if not rel["correction_records"] or not isinstance(rel["diff_pin"], dict) or not rel["diff_pin"]:
        raise ValueError("release scope empty")
    for p, v in rel["diff_pin"].items():
        if not (isinstance(v, dict) and v.get("status") in ("A", "M") and isinstance(v.get("blob"), str)):
            raise ValueError("diff_pin[%s]" % p)
    if not x["items"] or len(x["items"]) != len(x["paths"]):
        raise ValueError("cross_product_item.items/paths")
    if not dc["live_probe_paths"] or not isinstance(dc["required_status"], int):
        raise ValueError("deployment_condition")


def vercelignore_problems(text: str | None, rule: str) -> list[str]:
    """Necessary conditions on HEAD's .vercelignore (the sufficient condition is X5: identical to the baseline)."""
    if text is None:
        return [".vercelignore missing at HEAD"]
    raw = text.split("\n")
    probs = []
    if rule not in [l.rstrip("\r").rstrip() for l in raw if not l.startswith("#")]:
        probs.append("rule %r is not an active line" % rule)
    if any(l.lstrip().startswith("!") for l in raw):
        probs.append("a negation (!) line exists")
    if any(l[:1] in (" ", "\t") and l.strip() for l in raw):
        probs.append("an indented line exists")
    return probs


def evidence_problems(ev, exc: dict, facts, now: _dt.datetime, known=None) -> list[str]:
    """X9."""
    known = KNOWN_EXCEPTIONS if known is None else known
    if ev is None:
        return ["no deployment evidence supplied (--deployment-evidence)"]
    if not isinstance(ev, dict):
        return ["deployment evidence is not a JSON object"]
    dc = exc["deployment_condition"]
    probs = []
    if ev.get("kind") != "DEPLOYMENT_EVIDENCE":
        probs.append("evidence kind %r" % ev.get("kind"))
    if ev.get("result") != "NOT_DEPLOYED":
        probs.append("evidence result %r" % ev.get("result"))
    if ev.get("exception_id") != exc["exception_id"]:
        probs.append("evidence is for exception %r" % ev.get("exception_id"))
    if ev.get("exception_sha256") != known.get(exc["exception_id"]):
        probs.append("evidence exception_sha256 does not match the pinned exception")
    if ev.get("commit") != facts.head_commit() or ev.get("tree") != facts.head_tree() or not facts.head_tree():
        probs.append("evidence commit/tree %s/%s != HEAD %s/%s" % (ev.get("commit"), ev.get("tree"),
                                                                   facts.head_commit(), facts.head_tree()))
    if ev.get("clean") is not True or ev.get("vercelignore_excludes") is not True:
        probs.append("evidence records clean=%r vercelignore_excludes=%r" % (ev.get("clean"), ev.get("vercelignore_excludes")))
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
    probes = [p for p in (ev.get("probes") if isinstance(ev.get("probes"), list) else []) if isinstance(p, dict)]
    paths = [p.get("path") for p in probes]
    if len(paths) != len(set(paths)):
        probs.append("duplicate probe paths in evidence")
    got = {p.get("path"): p for p in probes}
    for path in dc["live_probe_paths"]:
        p = got.get(path)
        if p is None:
            probs.append("probe %s missing from evidence" % path)
        elif p.get("status") != dc["required_status"] or p.get("redirect_followed") is not False:
            probs.append("probe %s status %r (required %s, no redirect)" % (path, p.get("status"), dc["required_status"]))
    return probs


def item_matches(exc: dict, manifest_name: str, manifest: dict, item: dict) -> bool:
    """X4 (first half): the open item is one of the exception's own."""
    x = exc["cross_product_item"]
    return (isinstance(item, dict) and item.get("item_id") == x["item_id"] and item.get("product") == x["product"]
            and item.get("status") == x["required_status"]
            and manifest_name == x["correction_manifest"] and manifest.get("correction_id") == x["correction_id"]
            and item.get("path") in x["paths"])


def _canon_item(i):
    return {k: i.get(k) for k in ("item_id", "product", "status", "path", "proposition", "match")} \
        if isinstance(i, dict) else {"_not_object": repr(i)}


def release_problems(exc: dict, facts) -> list[str]:
    """X4 (second half) and X5-X8, all from HEAD."""
    rel, x = exc["release"], exc["cross_product_item"]
    probs = []
    for c, label in ((rel["production_baseline"], "production_baseline"), (rel["candidate_commit"], "candidate_commit")):
        if not facts.is_ancestor(c):
            probs.append("%s %s is not an ancestor of HEAD" % (label, c[:10]))
    # X5: the whole diff against the production baseline is exactly the pinned one
    changed = facts.changed_paths(rel["production_baseline"])
    pin = rel["diff_pin"]
    if changed is None:
        probs.append("release scope unknown: cannot diff against the production baseline")
        changed = {}
    extra = sorted(set(changed) - set(pin))
    lost = sorted(set(pin) - set(changed))
    if extra:
        probs.append("release scope changed: unpinned path(s) differ from the baseline %s" % extra[:8])
    if lost:
        probs.append("release scope changed: pinned path(s) no longer differ %s" % lost[:8])
    for path in sorted(set(pin) & set(changed)):
        want = pin[path]
        if changed[path] != want["status"]:
            probs.append("release scope changed: %s status %s != pinned %s" % (path, changed[path], want["status"]))
        if want["blob"] != SELF and facts.blob_at_head(path) != want["blob"]:
            probs.append("release scope changed: %s content differs from the pinned blob" % path)
    self_entries = sorted(p for p, v in pin.items() if v["blob"] == SELF)
    if self_entries != sorted([ORAL + "governance_exceptions.py", ORAL + exception_filename(exc["exception_id"])]):
        probs.append("diff_pin SELF entries %s are not exactly this module and this exception" % self_entries)
    added = sorted(pathlib.PurePosixPath(p).name for p, s in changed.items()
                   if s == "A" and p.startswith(ORAL + "correction_") and p.endswith("_manifest.json"))
    touched = sorted(pathlib.PurePosixPath(p).name for p in changed
                     if p.startswith(ORAL + "correction_") and p.endswith("_manifest.json"))
    if added != sorted(rel["correction_records"]) or touched != added:
        probs.append("release scope changed: correction records added %s / touched %s != declared nine"
                     % (added, touched))
    # X4 second half: the record at HEAD declares exactly the pinned items
    rec = facts.head_record(x["correction_manifest"])
    items = (((rec or {}).get("propagation") or {}).get("cross_product_safety_items")
             if isinstance((rec or {}).get("propagation"), dict) else None)
    if not isinstance(items, list) or [_canon_item(i) for i in items] != [_canon_item(i) for i in x["items"]]:
        probs.append("cross-product items in %s at HEAD differ from the pinned list" % x["correction_manifest"])
    # X6
    for name in rel["correction_records"]:
        st = (((facts.head_record(name) or {}).get("founder_authorisation")) or {}).get("state")
        if st != "FOUNDER_AUTHORISED":
            probs.append("unauthorised correction %s (state at HEAD %s)" % (name, st))
    # X7
    probs += ["not clean: %s" % p for p in facts.clean_problems()]
    # X8
    surface = sorted(p for p in changed if p.startswith(DEPLOY_SURFACE) or p in DEPLOY_SURFACE)
    if surface:
        probs.append("deployment surface differs from the baseline %s: exception does not apply" % surface)
    vp = vercelignore_problems(facts.show_head(".vercelignore"), exc["deployment_condition"]["vercelignore_rule"])
    if vp:
        probs.append("%s may be deployed (.vercelignore: %s): exception does not apply"
                     % (x["product"], "; ".join(vp)))
    return probs


def evaluate_l4(open_items: list, exception_files: dict, facts, evidence, now: _dt.datetime,
                known=None, working_records=None) -> tuple[bool, list[str], list[str]]:
    """Pure L4. open_items: [(manifest_name, item_dict)] as read by the gate; exception_files: {filename: raw};
    facts: RepoFacts-like (HEAD-based). Returns (ok, blocking reasons, informational lines)."""
    blocks, info, valid = [], [], []
    for name, raw in sorted(exception_files.items()):
        e, probs = check_exception_file(name, raw, now.date(), known)
        blocks += probs
        if e is not None:
            valid.append(e)
    for mname, item in open_items:
        label = "%s: %s (%s)" % (mname, (item or {}).get("item_id") if isinstance(item, dict) else item,
                                 (item or {}).get("product") if isinstance(item, dict) else "?")
        rec = facts.head_record(mname) or {}
        cands = [e for e in valid if item_matches(e, mname, rec, item)]
        if not cands:
            blocks.append("%s OPEN with no matching governance exception" % label)
            continue
        e = cands[0]
        probs = release_problems(e, facts) + evidence_problems(evidence, e, facts, now, known)
        if probs:
            blocks.append("%s: exception %s does not apply: %s" % (label, e["exception_id"], "; ".join(probs)))
        else:
            info.append("%s: non-blocking under %s (item stays OPEN)" % (label, e["exception_id"]))
    return (not blocks), blocks, info


class RepoFacts:
    """The real repository, read-only, judged at HEAD."""

    def __init__(self, repo: pathlib.Path = REPO):
        self.repo = pathlib.Path(repo)

    def _git(self, *a, text=True):
        return subprocess.run(["git", *a], cwd=str(self.repo), capture_output=True, text=text, check=False)

    def head_commit(self):
        r = self._git("rev-parse", "--verify", "-q", "HEAD^{commit}")
        return r.stdout.strip() if r.returncode == 0 else ""

    def head_tree(self):
        r = self._git("rev-parse", "--verify", "-q", "HEAD^{tree}")
        return r.stdout.strip() if r.returncode == 0 else ""

    def is_ancestor(self, c):
        if not isinstance(c, str) or len(c) != 40:
            return False
        return self._git("merge-base", "--is-ancestor", c, "HEAD").returncode == 0

    def changed_paths(self, base):
        """{path: status} for every path differing from base, renames and copies split (A/M/D only)."""
        r = self._git("-c", "core.quotepath=off", "diff", "--no-renames", "--no-ext-diff", "--name-status", "-z",
                      base, "HEAD")
        if r.returncode != 0:
            return None
        parts = r.stdout.split("\0")
        out = {}
        for i in range(0, len(parts) - 1, 2):
            if parts[i]:
                out[parts[i + 1]] = parts[i][0]
        return out

    def blob_at_head(self, path):
        r = self._git("rev-parse", "--verify", "-q", "HEAD:%s" % path)
        return r.stdout.strip() if r.returncode == 0 else None

    def show_head(self, path):
        r = subprocess.run(["git", "show", "HEAD:%s" % path], cwd=str(self.repo), capture_output=True, check=False)
        return r.stdout.decode("utf-8") if r.returncode == 0 else None

    def head_record(self, name):
        t = self.show_head(ORAL + name)
        try:
            return json.loads(t) if t is not None else None
        except ValueError:
            return None

    def clean_problems(self):
        probs = []
        st = self._git("status", "--porcelain", "--untracked-files=all")
        if st.returncode != 0 or st.stdout.strip():
            probs.append("uncommitted or untracked changes")
        flags = self._git("ls-files", "-v")
        if flags.returncode != 0 or any(l[:1].islower() or l[:2] == "S " for l in flags.stdout.splitlines()):
            probs.append("skip-worktree or assume-unchanged index entries")
        ig = self._git("status", "--porcelain", "--ignored", "--untracked-files=all", "--", ORAL)
        if ig.returncode != 0 or any(l.startswith("!! ") and l.endswith(".json") for l in ig.stdout.splitlines()):
            probs.append("ignored *.json under %s" % ORAL)
        return probs

    def vercelignore(self):
        return self.show_head(".vercelignore") or ""


def load_exception_files(directory: pathlib.Path = HERE) -> dict:
    return {p.name: p.read_bytes() for p in sorted(directory.glob(EXCEPTION_GLOB))}
