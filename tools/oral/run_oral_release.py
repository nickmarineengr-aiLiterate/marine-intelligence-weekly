#!/usr/bin/env python3
"""
The committed Oral release runner.

ONE command runs the full release sequence:

    python tools/oral/run_oral_release.py --full

ONE command shows the sequence without executing it:

    python tools/oral/run_oral_release.py --plan

Batches E1-E6 each drove their 37-39 gate suite from a session-scratch script
that was never committed, so the sequence survived only in handoff prose and
conversation history. This runner and `oral_release_gates.py` close that gap.

WHAT THIS RUNNER IS NOT
-----------------------
It orchestrates existing tools. It contains no domain checks. Validators and
mutators are historical release evidence and are called, never reimplemented.
Mutation summaries are parsed by the SHARED parser in `oral_mutation.py`, so
the "mutations=8 escapes=0" precedence defect cannot be reintroduced here.

CLASSIFICATION
--------------
A process exit code is not a verdict. `validate_audit` exits 0 while reporting a
failed check, and a mutation harness prints the validator's own "FAIL:" lines as
PROOF that a mutation was caught. Each gate is classified by its declared parser:

    PASS | FAIL | PRE_EXISTING_BASELINE | UNAVAILABLE | SKIPPED

SERIAL OWNERSHIP
----------------
Gates run strictly one at a time. While a mutator or the determinism generator
owns the worktree, nothing else may observe that transient state. V1 chooses
reliability over speed.
"""

from __future__ import annotations

import argparse
import collections
import datetime
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import oral_release_gates as REG          # noqa: E402
from oral_bytes import read_text, write_text, normalise_eol   # noqa: E402
from oral_mutation import parse_summary   # noqa: E402

PASS = "PASS"
FAIL = "FAIL"
BASELINE = "PRE_EXISTING_BASELINE"
UNAVAILABLE = "UNAVAILABLE"
SKIPPED = "SKIPPED"

RELEASE_BLOCKING = (FAIL, UNAVAILABLE)


# --------------------------------------------------------------- utilities

def _now():
    return datetime.datetime.now(datetime.timezone.utc)


def resolve_command(gate):
    """Turn a registry command into an argv list that can actually be run.

    Two substitutions, both deliberate:

    * "python" becomes THIS interpreter, so the runner never depends on which
      python is first on PATH.
    * the Node test glob is expanded HERE, into explicit file paths. Node 24
      resolves `--test <dir>` as a module to load and fails with "Cannot find
      module"; E5's runner did exactly that and the gate exited 1 in 0.4s, an
      invocation defect that read as a gate failure. The glob is expanded by
      Python and never handed to a shell.
    """
    argv = []
    for part in gate["command"]:
        if part == "python":
            argv.append(sys.executable)
        elif part == REG.NODE_TEST_GLOB:
            files = sorted(p.as_posix() for p in REPO.glob(part))
            if not files:
                raise FileNotFoundError("no files match %s" % part)
            argv.extend(files)
        else:
            argv.append(part)
    return argv


def gate_tool_path(gate):
    """The script a gate runs, for existence checks.

    Returns None for gates whose target is a glob (Node) or which run no script;
    those are validated by resolve_command instead, which fails loudly when a
    glob matches nothing.
    """
    for part in gate["command"][1:]:
        if "*" in part:
            return None
        if part.endswith((".py", ".mjs")):
            return REPO / part
    return None


def run_process(argv, timeout, cwd=None, env=None):
    """Run a gate. Decoding is explicit: Windows would otherwise use cp1252,
    which has already manufactured 450 false diffs in an oral gate."""
    started = time.monotonic()
    try:
        proc = subprocess.run(
            argv, cwd=str(cwd or REPO), capture_output=True, timeout=timeout,
            env=env)
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT after %ss" % timeout, time.monotonic() - started
    out = proc.stdout.decode("utf-8", errors="replace")
    err = proc.stderr.decode("utf-8", errors="replace")
    return proc.returncode, out, err, time.monotonic() - started


# ------------------------------------------------------- artefact snapshots

class ArtefactGuard:
    """Snapshot and restore the files that release gates rewrite.

    Restoration is from the runner's OWN in-memory snapshot, by exact path.
    It never runs `git checkout -- .`, `git restore .`, or any blanket reset --
    and it never restores from git at all, because `git checkout <ref> -- <file>`
    destroys uncommitted branch edits, a trap that has already cost real work in
    this repository. The runner may only put back bytes it personally read.
    """

    def __init__(self, paths=REG.GENERATED_ARTEFACTS):
        self.paths = [REPO / p for p in paths]
        self.snapshot = {}

    def capture(self):
        self.snapshot = {}
        for path in self.paths:
            if path.is_file():
                self.snapshot[path] = path.read_bytes()
        return self

    def dirtied(self):
        return [p for p, blob in self.snapshot.items()
                if p.is_file() and p.read_bytes() != blob]

    def restore(self):
        """Put back exactly what was captured. Returns the paths restored."""
        restored = []
        for path, blob in self.snapshot.items():
            if path.is_file() and path.read_bytes() != blob:
                path.write_bytes(blob)
                restored.append(path)
        return restored

    def verify(self):
        """True when every captured file matches its snapshot again."""
        return not self.dirtied()


# ------------------------------------------------------------- classifiers

# Five validator summary dialects ship in this repo:
#
#   31 checks, 1 FAIL                      batch validators, content_index
#   59 checks, 0 failed                    gap0609
#   315 controls / 0 failures              oral_controls, qb_question_text
#   10 tests, 0 failures                   test_examiner_check
#   107 PASS / 0 FAIL                      examiner_index, ce_tip, phase2
#
# The leading number is NOT the same quantity across them: in the last dialect
# it is the number of PASSES, not the total. What is stable is that the SECOND
# number is always the failure count, so only that is trusted for the verdict.
# `\w+\s+` absorbs a qualifier between the count and the noun --
# test_notes_controls prints "106 notes controls / 0 failures".
_VALIDATOR_SUMMARY = re.compile(
    r"(\d+)\s+(?:\w+\s+)?(checks?|controls?|tests?|PASS)\b\s*[,/]\s*(\d+)\s*"
    r"(FAIL\w*|fail\w*)", re.I)


def classify_validator(out, err, rc):
    text = out + "\n" + err
    matches = _VALIDATOR_SUMMARY.findall(text)
    if not matches:
        # No recognised summary: fall back to the exit code and SAY so, rather
        # than reporting a bare PASS that looks semantically checked.
        return (PASS if rc == 0 else FAIL), {
            "summary": "no recognised validator summary line", "exit": rc}
    lead, lead_kind, fails, _fail_kind = matches[-1]
    detail = {"failures": int(fails), "exit": rc,
              ("passes" if lead_kind.upper() == "PASS" else "checks"): int(lead)}
    # WHICH checks failed, not just how many. A baseline comparison on counts
    # alone would call a swapped-out failure "the same failure".
    failing = validator_failing(text)
    if failing:
        detail["failing"] = sorted(failing)
    return (PASS if int(fails) == 0 and rc == 0 else FAIL), detail


def validator_failing(text):
    """The check names a batch-dialect validator reported as FAIL."""
    return set(re.findall(r"^FAIL\s+(\S+)", text, re.M))


def classify_mutation(out, err, rc):
    """Delegate entirely to the shared parser.

    Nothing in this function may pattern-match escapes itself. A mutation log is
    full of the validator's own FAIL output -- that is the evidence a mutation
    was CAUGHT -- so only the harness's summary line carries the verdict.
    """
    try:
        summary = parse_summary(out + "\n" + err)
    except ValueError as exc:
        return UNAVAILABLE, {"error": str(exc), "exit": rc}
    detail = {
        "run": summary.run, "caught": summary.caught,
        "escapes": summary.escapes, "no_ops": summary.no_ops,
        "crashes": summary.crashes, "dialect": summary.dialect, "exit": rc,
    }
    ok = (summary.escapes == 0 and summary.no_ops == 0
          and summary.crashes == 0 and summary.run > 0)
    return (PASS if ok else FAIL), detail


def _last_json_object(text):
    """Pull the trailing JSON object out of a tool's stdout."""
    depth, start = 0, None
    best = None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                best = text[start:i + 1]
    if best is None:
        return None
    try:
        return json.loads(best)
    except ValueError:
        return None


def classify_audit(out, err, rc, baseline=None):
    """validate_audit exits 0 while reporting a failed check.

    A current failure that is identical to the clean-baseline failure is
    PRE_EXISTING_BASELINE, not PASS and not FAIL. The baseline is DERIVED by
    running the same tool on a clean worktree -- never hardcoded, because a
    hardcoded baseline silently absorbs the next real regression.
    """
    summary = _last_json_object(out)
    if summary is None:
        return UNAVAILABLE, {"error": "no JSON summary", "exit": rc}

    detail = {
        "passed": summary.get("passed"),
        "failed": summary.get("failed"),
        "unavailable": summary.get("unavailable"),
        "failing": sorted(_failing_ids(summary)),
        "exit": rc,
    }
    if detail["unavailable"]:
        return UNAVAILABLE, detail
    if not detail["failed"]:
        return PASS, detail
    if baseline is None:
        detail["baseline"] = "not derived"
        return FAIL, detail

    detail["baseline_failing"] = sorted(_failing_ids(baseline))
    detail["baseline_failed"] = baseline.get("failed")
    if (detail["failing"] == detail["baseline_failing"]
            and detail["failed"] == baseline.get("failed")):
        return BASELINE, detail
    return FAIL, detail


def _failing_ids(summary):
    """Identity of each failing check, not merely how many failed."""
    ids = []
    for row in (summary.get("results") or summary.get("checks") or []):
        if isinstance(row, dict) and row.get("ok") is False:
            ids.append(row.get("id") or row.get("check") or "?")
    if not ids and summary.get("failing"):
        ids = list(summary["failing"])
    return ids


_CHECK_STALE = re.compile(r"\b(stale|regenerat|would\s+change|drift)", re.I)


def classify_check(out, err, rc):
    detail = {"exit": rc}
    if rc != 0:
        return FAIL, detail
    if _CHECK_STALE.search(out + err) and "no regeneration" not in (out + err).lower():
        detail["note"] = "generator reports drift"
        return FAIL, detail
    return PASS, detail


_NODE = re.compile(r"^#\s*(pass|fail|tests)\s+(\d+)", re.I | re.M)


def classify_node(out, err, rc):
    counts = {k.lower(): int(v) for k, v in _NODE.findall(out + "\n" + err)}
    detail = {"exit": rc, **counts}
    if not counts:
        return (PASS if rc == 0 else FAIL), detail
    return (PASS if counts.get("fail", 1) == 0 else FAIL), detail


# ------------------------------------------------------------------- health

# PROVENANCE IS NOT A FINDING.
#
# Every line here describes WHERE the report was taken from, not what it found.
# The runner deliberately runs the two sides with different `--source` flags, so
# each of these lines differs by construction on every single run -- and one of
# them, `Loading source: ...`, was missed. It leaked into the finding multiset
# and produced a permanent `NEW=1 GONE=1`, which made this gate impossible to
# pass on ANY tree, clean or otherwise. It is not a regression detector if it is
# always red.
#
# Guarded for non-vacuity in test_oral_release_infra.py section 6: provenance
# must be stripped AND a genuine finding difference must still be reported.
_HEALTH_NOISE = re.compile(
    r"^(=+|HEALTH CHECK SOURCE|Loading source|source_type|source|commit"
    r"|files|eol|findings)\b"
    r"|MIW QB \+ Notes Health Check|^\s*$")


def health_findings(text):
    """Reduce a health report to a comparable multiset of finding lines.

    Compared as a MULTISET, not a diff: emission order is not stable
    (PYTHONHASHSEED is unpinned), so a line-order diff manufactures a false
    regression. The transport is normalised first -- E5's runner wrote captured
    output through a newline-translating stream, turning each CRLF into CRCRLF,
    and read its own 481 extra blank lines as new findings.
    """
    lines = []
    for raw in normalise_eol(text).split("\n"):
        line = raw.rstrip()
        if not line or _HEALTH_NOISE.match(line):
            continue
        # strip a leading timestamp if a report ever carries one per line
        lines.append(re.sub(r"^\d{2}:\d{2}(:\d{2})?\s+", "", line))
    return collections.Counter(lines)


def run_health(gate, log):
    """Candidate = LOCAL working tree. Baseline = a clean ref.

    The runner must never compare remote main against itself. That comparison
    was reported as pre-merge evidence in several handoffs while being
    structurally incapable of seeing the change under test.
    """
    cand_argv = resolve_command(gate)
    rc_c, out_c, err_c, secs_c = run_process(cand_argv, gate["timeout"])

    base_gate = dict(gate)
    base_gate["command"] = ["python", "meoclass1/qb_health_check.py",
                            "--source", "ref", "--ref", REG.BASELINE_REF,
                            "--no-email"]
    rc_b, out_b, err_b, secs_b = run_process(
        resolve_command(base_gate), gate["timeout"])

    if rc_c != 0 or rc_b != 0:
        return UNAVAILABLE, {"candidate_exit": rc_c, "baseline_exit": rc_b,
                             "error": (err_c or err_b)[:400]}, out_c + out_b, \
            secs_c + secs_b

    cand, base = health_findings(out_c), health_findings(out_b)
    new = cand - base
    gone = base - cand
    detail = {
        "candidate_source": "local (working tree)",
        "baseline_source": "ref %s" % REG.BASELINE_REF,
        "candidate_findings": sum(cand.values()),
        "baseline_findings": sum(base.values()),
        "new": sum(new.values()),
        "gone": sum(gone.values()),
        "new_sample": [l[:120] for l in list(new)[:5]],
        "gone_sample": [l[:120] for l in list(gone)[:5]],
    }
    status = PASS if not new else FAIL
    log("      candidate(local)=%d  baseline(%s)=%d  NEW=%d  GONE=%d"
        % (detail["candidate_findings"], REG.BASELINE_REF,
           detail["baseline_findings"], detail["new"], detail["gone"]))
    return status, detail, out_c + out_b, secs_c + secs_b


def worktree_env(work):
    """Environment for a process running inside a DERIVED worktree.

    `F:` here is a filesystem that does not record ownership, so git refuses to
    operate in any directory that is not on the `safe.directory` allowlist. The
    main clone is on it; a freshly created temporary worktree never is.

    The symptom is silent and expensive: every git call inside the derived tree
    dies with "detected dubious ownership", so a validator that reads its
    evidence through `git show` reports that evidence as *unavailable* -- and a
    baseline derived from it describes the sandbox, not the baseline commit.
    `validate_batch_e6` derived exactly one failing check that way,
    `consolidation_available`, which is not how it fails on a real checkout.

    The exception is scoped to this one worktree path, never `*`, and injected
    through the environment so the CHILD validator's own git calls see it too.
    """
    env = dict(os.environ)
    env["GIT_CONFIG_COUNT"] = "1"
    env["GIT_CONFIG_KEY_0"] = "safe.directory"
    env["GIT_CONFIG_VALUE_0"] = str(work).replace("\\", "/")
    return env


def derive_audit_baseline(log):
    """Run validate_audit on a clean detached worktree of the baseline ref.

    Uses a temporary worktree so the real tree is never checked out from under
    the runner. Returns the parsed summary, or None if it cannot be derived.
    """
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="oral-audit-baseline-"))
    work = tmp / "tree"
    try:
        made = subprocess.run(
            ["git", "worktree", "add", "--detach", str(work), REG.BASELINE_REF],
            cwd=str(REPO), capture_output=True)
        if made.returncode != 0:
            log("      baseline worktree unavailable: %s"
                % made.stderr.decode("utf-8", "replace").strip()[:160])
            return None
        rc, out, _err, _secs = run_process(
            [sys.executable, "tools/oral/validate_audit.py"], 600, cwd=work,
            env=worktree_env(work))
        return _last_json_object(out)
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(work)],
                       cwd=str(REPO), capture_output=True)
        shutil.rmtree(tmp, ignore_errors=True)


def derive_validator_baseline(gate, log):
    """Re-run one validator on a clean worktree of the baseline ref.

    Returns the set of check names failing there, or None when the baseline
    cannot be derived (in which case the live failure stays a FAIL -- an
    underivable baseline is never an excuse to pass).

    Same worktree discipline as derive_audit_baseline: the real tree is never
    checked out from under the runner.
    """
    script = gate_tool_path(gate)
    if script is None:
        return None
    rel = script.relative_to(REPO).as_posix()

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="oral-gate-baseline-"))
    work = tmp / "tree"
    try:
        made = subprocess.run(
            ["git", "worktree", "add", "--detach", str(work), REG.BASELINE_REF],
            cwd=str(REPO), capture_output=True)
        if made.returncode != 0:
            log("      baseline worktree unavailable: %s"
                % made.stderr.decode("utf-8", "replace").strip()[:160])
            return None
        _rc, out, err, _secs = run_process(
            [sys.executable, rel], gate["timeout"], cwd=work,
            env=worktree_env(work))
        return validator_failing(out + "\n" + err)
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(work)],
                       cwd=str(REPO), capture_output=True)
        shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------- the runner

CLASSIFIERS = {
    REG.PARSER_VALIDATOR: classify_validator,
    REG.PARSER_MUTATION: classify_mutation,
    REG.PARSER_CHECK: classify_check,
    REG.PARSER_NODE: classify_node,
}


def select_gates(args):
    gates = list(REG.ALL_GATES)
    # Held-back phases (determinism) run only when asked for. Selection keys off
    # `separate_phase`, NOT off `historical_39`: the latter is provenance -- it
    # records what E6's suite contained -- and using it to decide what runs today
    # would silently exclude every gate added after E6, including the correction
    # gates that keep post-release delegation honest.
    if not args.determinism:
        gates = [g for g in gates if not g["separate_phase"]]
    if args.gate:
        wanted = set(args.gate)
        unknown = wanted - set(REG.gate_ids())
        if unknown:
            raise SystemExit("unknown gate(s): %s" % ", ".join(sorted(unknown)))
        gates = [g for g in REG.ALL_GATES if g["id"] in wanted]
    if args.category:
        gates = [g for g in gates if g["category"] in set(args.category)]
    if args.read_only:
        gates = [g for g in gates if not g["mutates_worktree"]]
    return gates


def plan(gates, out=print):
    out("%-4s %-26s %-14s %-7s %-10s %-7s %s"
        % ("#", "gate_id", "category", "mutates", "parser", "timeout", "command"))
    out("-" * 118)
    for i, gate in enumerate(gates, 1):
        try:
            argv = resolve_command(gate)
            shown = " ".join(
                ["python" if a == sys.executable else pathlib.Path(a).name
                 if a.endswith((".py", ".mjs")) else a for a in argv])
            if gate["parser"] == REG.PARSER_NODE:
                shown = "node --test <%d explicit .test.mjs files>" % (len(argv) - 2)
        except FileNotFoundError as exc:
            shown = "UNRESOLVED: %s" % exc
        out("%-4d %-26s %-14s %-7s %-10s %-7s %s"
            % (i, gate["id"], gate["category"],
               "YES" if gate["mutates_worktree"] else "no",
               gate["parser"], gate["timeout"], shown))
        if gate["depends_on"]:
            out("     depends_on: %s" % ", ".join(gate["depends_on"]))
        if gate["note"]:
            out("     note: %s" % gate["note"])
    out("-" * 118)
    out("%d gate(s); %d mutate the worktree; %d of the historical 39"
        % (len(gates), sum(1 for g in gates if g["mutates_worktree"]),
           sum(1 for g in gates if g["historical_39"])))


def execute(gates, args, log):
    guard = ArtefactGuard().capture()
    records = []
    audit_baseline = None
    owner = None          # the gate currently owning the worktree

    for i, gate in enumerate(gates, 1):
        gid = gate["id"]
        if owner is not None:
            raise RuntimeError(
                "serial ownership violated: %s still owns the worktree" % owner)

        tool = gate_tool_path(gate)
        if tool is not None and not tool.exists():
            records.append({"gate": gid, "status": UNAVAILABLE,
                            "detail": {"error": "missing tool: %s" % tool},
                            "seconds": 0.0})
            log("[%02d/%02d] %-26s %s (missing tool)" % (i, len(gates), gid, UNAVAILABLE))
            if not args.keep_going:
                break
            continue

        done = {r["gate"] for r in records if r["status"] in (PASS, BASELINE)}
        missing_dep = [d for d in gate["depends_on"] if d not in done]
        if missing_dep and not args.gate:
            records.append({"gate": gid, "status": SKIPPED,
                            "detail": {"unmet": missing_dep}, "seconds": 0.0})
            log("[%02d/%02d] %-26s SKIPPED (unmet: %s)"
                % (i, len(gates), gid, ", ".join(missing_dep)))
            continue

        log("[%02d/%02d] %-26s starting..." % (i, len(gates), gid))
        if gate["mutates_worktree"]:
            owner = gid

        started = _now()
        try:
            if gate["parser"] == REG.PARSER_HEALTH:
                status, detail, out, secs = run_health(gate, log)
            else:
                argv = resolve_command(gate)
                rc, out, err, secs = run_process(argv, gate["timeout"])
                if gate["parser"] == REG.PARSER_AUDIT:
                    if audit_baseline is None and not args.no_audit_baseline:
                        log("      deriving audit baseline from %s ..." % REG.BASELINE_REF)
                        audit_baseline = derive_audit_baseline(log)
                    status, detail = classify_audit(out, err, rc, audit_baseline)
                else:
                    fn = CLASSIFIERS.get(gate["parser"])
                    if fn is None:
                        status = PASS if rc == 0 else FAIL
                        detail = {"exit": rc}
                    else:
                        status, detail = fn(out, err, rc)
                    # A gate carrying known, non-reproducible historical
                    # evidence is compared against a DERIVED baseline before
                    # its failure is called a regression. Nothing is ever
                    # promoted to PASS: the status is its own, and the checks
                    # are named in the log.
                    if (status == FAIL and gate.get("baseline_derivable")
                            and not args.no_audit_baseline):
                        live = set(detail.get("failing") or [])
                        log("      deriving %s baseline from %s ..."
                            % (gid, REG.BASELINE_REF))
                        base = derive_validator_baseline(gate, log)
                        if base is None:
                            detail["baseline"] = "not derived"
                        else:
                            detail["baseline_failing"] = sorted(base)
                            # SUBSET, not equality. The question a release asks
                            # is "is anything failing here that was not already
                            # failing on the baseline?". Equality answers a
                            # different question and gets it wrong in the one
                            # direction that matters least: it reports an
                            # IMPROVEMENT as a regression. When this correction
                            # is on origin/main, live={line_endings} while the
                            # pre-correction baseline failed that AND
                            # only_authorised_cards_changed -- strictly fewer
                            # failures, every one of them pre-existing.
                            if live and live <= base:
                                status = BASELINE
                                detail["baseline_fixed"] = sorted(base - live)
        finally:
            owner = None
            restored = guard.restore() if gate["mutates_worktree"] else []

        record = {
            "gate": gid, "status": status, "detail": detail,
            "seconds": round(secs, 1), "mutates": gate["mutates_worktree"],
            "started": started.isoformat(),
            "restored": [p.relative_to(REPO).as_posix() for p in restored],
            "restore_verified": guard.verify(),
        }
        records.append(record)

        log("[%02d/%02d] %-26s %-22s %6.1fs %s"
            % (i, len(gates), gid, status, secs,
               json.dumps(detail, sort_keys=True)[:110]))
        if restored:
            log("      restored by exact path: %s" % ", ".join(record["restored"]))
        if not record["restore_verified"]:
            log("      WARNING: generated artefacts still differ after restore")

        if status in RELEASE_BLOCKING and not args.keep_going:
            log("\nRELEASE-CRITICAL FAILURE at %s -- stopping." % gid)
            break

    return records


def summarise(records, gates, log):
    counts = collections.Counter(r["status"] for r in records)
    log("\n" + "=" * 70)
    log("ORAL RELEASE SUMMARY")
    log("=" * 70)
    for status in (PASS, BASELINE, FAIL, UNAVAILABLE, SKIPPED):
        if counts.get(status):
            log("  %-22s %d" % (status, counts[status]))
    log("  %-22s %d of %d planned" % ("executed", len(records), len(gates)))
    log("  %-22s %.1fs" % ("wall time", sum(r["seconds"] for r in records)))

    muts = [r for r in records if r["detail"].get("run") is not None]
    if muts:
        log("  %-22s %d suites, %d mutations, %d escapes, %d no-ops, %d crashes"
            % ("mutations", len(muts),
               sum(r["detail"]["run"] for r in muts),
               sum(r["detail"]["escapes"] for r in muts),
               sum(r["detail"]["no_ops"] for r in muts),
               sum(r["detail"]["crashes"] for r in muts)))

    blocking = [r["gate"] for r in records if r["status"] in RELEASE_BLOCKING]
    log("  %-22s %s" % ("release", "BLOCKED by " + ", ".join(blocking)
                        if blocking else "all gates green"))
    return 1 if blocking else 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="run_oral_release",
        description="Run the committed Oral release gate sequence.")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--plan", action="store_true",
                      help="print the exact gate sequence without executing it")
    mode.add_argument("--full", action="store_true",
                      help="run the full release sequence (39 gates + determinism)")
    ap.add_argument("--gate", action="append",
                    help="run only this gate id (repeatable)")
    ap.add_argument("--category", action="append",
                    help="run only this category (repeatable)")
    ap.add_argument("--read-only", action="store_true",
                    help="only gates that do not mutate the worktree")
    ap.add_argument("--determinism", action="store_true",
                    help="include the determinism phase (implied by --full)")
    ap.add_argument("--keep-going", action="store_true",
                    help="continue past a release-critical failure")
    ap.add_argument("--no-audit-baseline", action="store_true",
                    help="skip deriving the clean audit baseline (audit then "
                         "cannot report PRE_EXISTING_BASELINE)")
    ap.add_argument("--log-dir", default=None,
                    help="where to write logs (default: a temp dir, never the repo)")
    args = ap.parse_args(argv)

    if args.full:
        args.determinism = True
    gates = select_gates(args)

    if args.plan or not (args.full or args.gate or args.category or args.read_only):
        plan(gates)
        return 0

    log_dir = pathlib.Path(args.log_dir) if args.log_dir else pathlib.Path(
        tempfile.mkdtemp(prefix="oral-release-"))
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = _now().strftime("%Y%m%dT%H%M%SZ")
    log_path = log_dir / ("oral_release_%s.log" % stamp)
    json_path = log_dir / ("oral_release_%s.json" % stamp)
    buffer = []

    def log(message):
        print(message)
        buffer.append(str(message))

    log("Oral release runner -- %d gate(s), started %s" % (len(gates), stamp))
    log("Logs: %s" % log_dir)

    interrupted = False
    records = []
    try:
        records = execute(gates, args, log)
    except KeyboardInterrupt:
        interrupted = True
        log("\nINTERRUPTED. The runner stopped and did NOT continue into later "
            "gates.\nIf the interrupt landed inside a mutating gate, that gate's "
            "harness owns its own restore; verify with `git status` before "
            "re-running.\nThe runner restores only artefacts it snapshotted "
            "itself, by exact path.")

    code = summarise(records, gates, log)
    if interrupted:
        code = 130

    # Explicit newline contract. E5's logger wrote captured output through a
    # newline-translating stream, turning each CRLF into CRCRLF and doubling
    # the line count -- which a baseline comparison then read as 481 new
    # findings. newline="" plus explicit LF means the log says what it saw.
    write_text(log_path, "\n".join(buffer) + "\n")
    write_text(json_path, json.dumps({
        "started": stamp,
        "gates_planned": [g["id"] for g in gates],
        "interrupted": interrupted,
        "records": records,
        "exit": code,
    }, indent=2, sort_keys=True) + "\n")
    print("\nlog:  %s\njson: %s" % (log_path, json_path))
    return code


if __name__ == "__main__":
    sys.exit(main())
