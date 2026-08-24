"""Controls for the committed Oral release runner and its gate registry.

  PYTHONIOENCODING=utf-8 python tools/oral/test_oral_release_runner.py

Exit 0 when every control holds. No network, no product files touched, and the
39-gate suite is NOT executed -- orchestration is proved with fixtures and a
stubbed process layer, which is the point of separating the runner from the
domain checks it calls.
"""
from __future__ import annotations

import io
import re
import json
import pathlib
import sys
from pathlib import Path
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import oral_bytes as B                 # noqa: E402
import oral_release_gates as REG       # noqa: E402
import run_oral_release as R           # noqa: E402

FAILURES = []
CHECKS = [0]


def check(name, ok, detail=""):
    CHECKS[0] += 1
    if not ok:
        FAILURES.append("%s -- %s" % (name, detail))
        print("FAIL %-56s %s" % (name, detail))
    else:
        print("ok   %-56s %s" % (name, detail))


class Args:
    """Stand-in for argparse output."""

    def __init__(self, **kw):
        self.plan = self.full = self.read_only = self.determinism = False
        self.keep_going = self.no_audit_baseline = False
        self.gate = self.category = self.log_dir = None
        self.__dict__.update(kw)


# ===========================================================================
# A / K. GATE IDENTITY
# ===========================================================================
print("\n--- A/K. gate identity ---")

ids = [g["id"] for g in REG.ALL_GATES]
check("A. every gate id is unique", len(ids) == len(set(ids)),
      "%d gates, %d distinct" % (len(ids), len(set(ids))))
check("K. duplicate gate ids would be detectable",
      len(ids) == len(set(ids)) and all(ids),
      "no empty or repeated ids")
check("historical gate count is exactly 39", len(REG.historical_39()) == 39,
      "%d" % len(REG.historical_39()))

# --- the two flags must stay separate ------------------------------------
# Selection used to key off `historical_39`, which conflated "was in E6's
# suite" with "runs today". Under that reading every gate added after E6 --
# starting with the correction gates -- would silently never run.
check("determinism is the only held-back phase",
      [g["id"] for g in REG.ALL_GATES if g["separate_phase"]] == ["determinism"],
      str([g["id"] for g in REG.ALL_GATES if g["separate_phase"]]))

_correction = [g for g in REG.ALL_GATES if g["category"] == REG.CAT_CORRECTION]
check("the correction gates are registered",
      sorted(g["id"] for g in _correction)
      == ["correction_lsavent_mutate", "corrections_mutate",
          "validate_correction_lsavent", "validate_corrections"],
      str(sorted(g["id"] for g in _correction)))
check("correction gates are post-E6, so not part of the historical 39",
      all(g["historical_39"] is False for g in _correction))
check("correction gates are NOT held back from a default run",
      all(g["separate_phase"] is False for g in _correction),
      "a release must never ship an unverified correction")
check("the correction mutator depends on its validator",
      REG.by_id("corrections_mutate")["depends_on"] == ["validate_corrections"],
      "a mutation suite against a failing validator proves nothing")

# The runner must stay ignorant of any PARTICULAR correction. Both correction
# tools iterate correction_*_manifest.json on disk; naming one here would mean
# the delegation model had been bypassed.
_runner_src = (Path(REG.__file__).parent / "run_oral_release.py").read_text(
    encoding="utf-8")
# The worktree/baseline mechanism now lives in oral_mutation, shared by the
# runner's gate baselines and by every mutation harness's control precondition.
# Both sources are read here so "one implementation" is asserted, not assumed.
_mut_src = (Path(REG.__file__).parent / "oral_mutation.py").read_text(
    encoding="utf-8")
_shared_src = _runner_src + chr(10) + _mut_src
check("the runner names no specific correction",
      "FAIR_TREATMENT" not in _runner_src and "fair_treatment" not in _runner_src,
      "correction knowledge lives in the records, not the orchestrator")
check("determinism is registered OUTSIDE the historical 39",
      REG.DETERMINISM_GATE["historical_39"] is False
      and REG.DETERMINISM_GATE in REG.ALL_GATES,
      "%d gates total, 39 historical" % len(REG.ALL_GATES))

# EVERY gate added after E6, named. The list is enumerated rather than counted
# so a new gate cannot appear in a release by accident: adding one means editing
# this line, which is the review point. The totals below are derived FROM this
# list rather than hardcoded, because a hardcoded total is a guard that expires
# the next time a gate is registered.
POST_E6_GATES = [
    "batch_f1_mutate",
    "batch_f1b_mutate",
    # The August 2026 fresh-intake production batch. Kept in sorted position:
    # the control compares this list to a sorted derivation from the registry.
    "batch_g1_mutate",
    "correction_lsavent_mutate",
    "corrections_mutate",
    "followup_register_mutate",
    # The study-spine hook: a new oral question cannot ship unmapped.
    "study_mapping_check",
    # ...and cannot ship mapped-but-invisible: both study surfaces must
    # regenerate. study_public_roadmap_check also re-asserts the public-safety
    # guards on the rendered PUBLIC page, so a release is the point at which a
    # leak would be caught, not a later audit.
    "study_pages_check",
    "study_public_roadmap_check",
    "study_spine_validate",
    "validate_batch_f1",
    "validate_batch_f1b",
    "validate_batch_g1",
    "validate_correction_lsavent",
    "validate_corrections",
    "validate_followup_register",
]
POST_E6_MUTATION_SUITES = ["batch_f1_mutate", "batch_f1b_mutate",
                           "batch_g1_mutate", "correction_lsavent_mutate",
                           "corrections_mutate", "followup_register_mutate"]

# E6 reported 266 mutations across 15 suites. That number is HISTORY and stays
# pinned to the historical gates; post-E6 suites are counted separately rather
# than by moving the historical figure, which would quietly erase the evidence
# it encodes.
_mut_all = [g for g in REG.ALL_GATES if g["parser"] == REG.PARSER_MUTATION]
_mut_hist = [g for g in _mut_all if g["historical_39"]]
check("15 historical mutation suites, matching E6's reported 266 mutations / 15 suites",
      len(_mut_hist) == 15, "%d historical" % len(_mut_hist))
check("post-E6 mutation suites are additive, not substitutive",
      sorted(g["id"] for g in _mut_all if not g["historical_39"])
      == POST_E6_MUTATION_SUITES,
      "%d total suites" % len(_mut_all))
check("by_id resolves and rejects", REG.by_id("validate_audit")["id"] == "validate_audit",
      "lookup works")


def raises(fn, exc=Exception):
    try:
        fn()
    except exc:
        return True
    except Exception:
        return False
    return False


check("unknown gate id raises from the registry",
      raises(lambda: REG.by_id("no_such_gate"), KeyError))


# ===========================================================================
# L. EVERY GATE'S TOOL EXISTS
# ===========================================================================
print("\n--- L. command resolution ---")

missing = []
for gate in REG.ALL_GATES:
    tool = R.gate_tool_path(gate)
    if tool is not None and not tool.exists():
        missing.append("%s -> %s" % (gate["id"], tool))
check("L. every registered gate resolves to a tool that exists", not missing,
      "; ".join(missing) or "%d gates checked" % len(REG.ALL_GATES))

check("a missing tool is rejected, not run",
      R.gate_tool_path({"command": ["python", "tools/oral/nope.py"]}) is not None
      and not (REPO / "tools/oral/nope.py").exists(),
      "gate_tool_path surfaces the path so execute() can fail it")

# C. unknown gate on the command line must be an error, not a silent empty run.
check("C. unknown gate on the command line is rejected",
      raises(lambda: R.select_gates(Args(gate=["not_a_gate"])), SystemExit))
check("a known gate selects exactly one",
      len(R.select_gates(Args(gate=["validate_audit"]))) == 1)


# ===========================================================================
# H / I. INVOCATION CONTRACTS THAT HAVE BITTEN BEFORE
# ===========================================================================
print("\n--- H/I. invocation contracts ---")

node_argv = R.resolve_command(REG.by_id("node_security_tests"))
check("H. Node receives explicit .test.mjs files, never a directory",
      all(a.endswith(".test.mjs") for a in node_argv[2:]) and len(node_argv) > 3,
      "%d explicit files" % (len(node_argv) - 2))
check("H. no argument to Node is a bare directory",
      not any(a in ("tools/security", "tools/security/") for a in node_argv),
      "directory form absent")
check("H. the glob never survives into argv",
      REG.NODE_TEST_GLOB not in node_argv, "expanded by Python, not a shell")

det_argv = R.resolve_command(REG.DETERMINISM_GATE)
check("I. determinism is invoked bare -- no invented flags",
      det_argv[1].endswith("check_determinism.py") and len(det_argv) == 2,
      " ".join(pathlib.Path(a).name for a in det_argv))
check("I. determinism is never probed with --help",
      "--help" not in det_argv and "--help" not in str(REG.DETERMINISM_GATE["command"]),
      "the tool has no argv parser; --help would RUN it")

check("python resolves to this interpreter, not PATH",
      R.resolve_command(REG.by_id("validate_audit"))[0] == sys.executable,
      "interpreter pinned")


# ===========================================================================
# B. PLAN MODE
# ===========================================================================
print("\n--- B. plan mode ---")


def capture_plan(gates):
    buf = io.StringIO()
    R.plan(gates, out=lambda m: buf.write(str(m) + "\n"))
    return buf.getvalue()


full = R.select_gates(Args(full=True, determinism=True))
first, second = capture_plan(full), capture_plan(full)
check("B. plan mode is deterministic", first == second, "two runs identical")
check("B. plan executes nothing", "content_index_check" in first and len(first) > 500,
      "%d chars, no subprocess" % len(first))
check("B. plan shows sequence, mutation flag, parser and timeout",
      all(k in first for k in ("gate_id", "mutates", "parser", "timeout")),
      "columns present")
check("B. plan shows dependencies and conditional reasons",
      "depends_on:" in first and "note:" in first)
# The default set is the historical 39 PLUS every post-E6 gate that is not a
# held-back phase. Pinning it to a bare 39 would mean any gate added after E6
# either never runs or silently breaks this control -- and the correction gates
# are exactly such gates.
_default = R.select_gates(Args(full=False, gate=None))
_post_e6 = sorted(g["id"] for g in _default if not g["historical_39"])
check("plan of the release set is the historical 39 plus post-E6 gates",
      len(_default) == 39 + len(POST_E6_GATES)
      and sum(1 for g in _default if g["historical_39"]) == 39,
      "%d gates, %d historical, post-E6=%s"
      % (len(_default), sum(1 for g in _default if g["historical_39"]), _post_e6))
check("the post-E6 additions are the correction, authorisation and study gates",
      _post_e6 == POST_E6_GATES, str(_post_e6))
check("a default run never silently drops a post-E6 gate",
      all(not g["separate_phase"] for g in _default),
      "only held-back phases may be absent")
check("--full adds the determinism phase",
      len(full) == 39 + len(POST_E6_GATES) + 1
      and any(g["id"] == "determinism" for g in full),
      "%d gates" % len(full))
# --- derived baselines --------------------------------------------------
# E6 fails `line_endings_homogeneous_per_file` on a clean checkout of the very
# commit it certified. That is evidence debt, not a regression -- but it must
# never be reported as PASS, and it must never be hardcoded, because a
# hardcoded baseline absorbs the next real failure silently.
_derivable = [g["id"] for g in REG.ALL_GATES if g.get("baseline_derivable")]
check("only gates with known evidence debt derive a baseline",
      _derivable == ["validate_batch_e6"], str(_derivable))
check("a derived baseline is compared by check NAME, not by count",
      "baseline_failing" in _runner_src and "validator_failing" in _runner_src,
      "a swapped-out failure must not read as the same failure")
check("PRE_EXISTING_BASELINE is its own status, never PASS",
      R.BASELINE != R.PASS and R.BASELINE not in R.RELEASE_BLOCKING,
      "named in the summary, does not block, is not green")
check("an underivable baseline leaves the failure a FAIL",
      "not derived" in _runner_src,
      "a missing baseline is never an excuse to pass")
check("a derived baseline is compared by SUBSET, not equality",
      "live <= base" in _runner_src,
      "equality reports an improvement as a regression")
check("a baseline comparison records what the run FIXED",
      "baseline_fixed" in _runner_src,
      "a shrinking failure set is evidence, not noise")

# Derived worktrees and git's ownership allowlist.
# F: does not record filesystem ownership, so git refuses to operate in any
# directory absent from safe.directory. The main clone is listed; a temporary
# worktree never is. Without the exception, every git call inside a derived
# tree dies and the "baseline" describes the sandbox rather than the ref.
check("a derived worktree carries a scoped safe.directory exception",
      "GIT_CONFIG_KEY_0" in _mut_src and "safe.directory" in _mut_src,
      "otherwise git reports dubious ownership and the evidence reads as absent")
check("the ownership exception is scoped to the worktree, never '*'",
      'GIT_CONFIG_VALUE_0"] = str(work)' in _mut_src,
      "one path, not a blanket allowlist")
# There must be exactly ONE definition of the mechanism. A runner and a mutation
# harness that each derived "the baseline" their own way could disagree about
# what the baseline IS, which is the ambiguity a derived baseline removes.
check("worktree_env is defined once, in the shared module",
      _mut_src.count("def worktree_env(") == 1
      and "def worktree_env(" not in _runner_src,
      "the runner imports it rather than keeping a second copy")
check("validator_failing is defined once, in the shared module",
      _mut_src.count("def validator_failing(") == 1
      and "def validator_failing(" not in _runner_src,
      "one definition of which checks are failing")
check("every derived worktree run passes the exception to the CHILD process",
      _shared_src.count("env=worktree_env(work)") == 2
      and "worktree_env" in _runner_src,
      "the audit derivation in the runner and the validator derivation in "
      "oral_mutation each pass it")

check("--read-only excludes every mutating gate",
      not any(g["mutates_worktree"] for g in R.select_gates(Args(read_only=True))),
      "%d read-only gates" % len(R.select_gates(Args(read_only=True))))
check("--category narrows the set",
      {g["category"] for g in R.select_gates(Args(category=["health"]))} == {"health"})


# ===========================================================================
# D / E. MUTATION RESULTS GO THROUGH THE SHARED PARSER
# ===========================================================================
print("\n--- D/E. mutation classification ---")

# The exact dialect that produced 8 phantom escapes in E6's first aggregation.
status, detail = R.classify_mutation("mutations=8 escapes=0 no-ops=0 crashes=0", "", 0)
check("D. gap0609 key=value dialect parses through the shared parser",
      status == R.PASS and detail["run"] == 8, json.dumps(detail, sort_keys=True))
check("D. THE regression: 8 is never read as the escape count",
      detail["escapes"] == 0, "escapes=%d" % detail["escapes"])

# A mutation log is FULL of the validator's FAIL output -- that is the evidence
# a mutation was caught. It must not be read as a gate failure.
CAUGHT_LOG = """BASELINE GREEN
A   corrupt the limb        exit=1 fails=2 crash=False  caught
FAIL  limb_sentence_present  the limb is absent
FAIL  digest_matches         digest drift
25 mutations, 0 escape(s), 0 no-op(s), 0 crash(es)
"""
status, detail = R.classify_mutation(CAUGHT_LOG, "", 0)
check("D. 'FAIL:' lines in a mutator log are caught-evidence, not failures",
      status == R.PASS and detail["caught"] == 25, json.dumps(detail, sort_keys=True))
check("D. neighbouring 'fails=2 crash=False' donates no crash",
      detail["crashes"] == 0, "crashes=%d" % detail["crashes"])

for label, line, field in (
        ("escape", "10 mutations, 1 escape(s), 0 no-op(s), 0 crash(es)", "escapes"),
        ("no-op", "10 mutations, 0 escape(s), 2 no-op(s), 0 crash(es)", "no_ops"),
        ("crash", "10 mutations, 0 escape(s), 0 no-op(s), 3 crash(es)", "crashes")):
    st, dt = R.classify_mutation(line, "", 0)
    check("E. a %s fails the gate" % label, st == R.FAIL and dt[field] > 0,
          "%s=%s" % (field, dt[field]))

st, dt = R.classify_mutation("nothing parseable here", "", 0)
check("E. an unparseable summary is UNAVAILABLE, never a silent pass",
      st == R.UNAVAILABLE, str(dt)[:80])

st, _ = R.classify_mutation("25 mutations, 0 escape(s), 0 no-op(s), 0 crash(es)", "", 1)
check("E. a clean summary with a non-zero exit still records the summary",
      st == R.PASS, "summary is the verdict for mutation gates")


# ===========================================================================
# F. AUDIT CANNOT HIDE BEHIND EXIT 0
# ===========================================================================
print("\n--- F. audit semantics ---")

CURRENT = json.dumps({"passed": 12, "failed": 1, "unavailable": 0,
                      "results": [{"id": "index_tier_literals_valid", "ok": False},
                                  {"id": "other", "ok": True}]})
BASE_SAME = json.loads(CURRENT)
BASE_CLEAN = {"passed": 13, "failed": 0, "unavailable": 0, "results": []}

st, dt = R.classify_audit(CURRENT, "", 0, baseline=None)
check("F. exit 0 with failed=1 is NOT a pass", st == R.FAIL,
      "status=%s failed=%s" % (st, dt["failed"]))

st, dt = R.classify_audit(CURRENT, "", 0, baseline=BASE_SAME)
check("F. identical failure on a clean baseline is PRE_EXISTING_BASELINE",
      st == R.BASELINE, "failing=%s" % dt["failing"])

st, _ = R.classify_audit(CURRENT, "", 0, baseline=BASE_CLEAN)
check("F. a failure absent from the baseline is FAIL_CURRENT", st == R.FAIL,
      "new regression is not absorbed")

NEW_ID = json.dumps({"passed": 11, "failed": 1, "unavailable": 0,
                     "results": [{"id": "something_else", "ok": False}]})
st, _ = R.classify_audit(NEW_ID, "", 0, baseline=BASE_SAME)
check("F. same failure COUNT but different identity is FAIL, not baseline",
      st == R.FAIL, "identity is compared, not just the count")

st, _ = R.classify_audit(json.dumps({"passed": 1, "failed": 0, "unavailable": 2}),
                         "", 0, baseline=BASE_SAME)
check("F. unavailable checks are UNAVAILABLE, never PASS", st == R.UNAVAILABLE)
st, _ = R.classify_audit("no json at all", "", 0)
check("F. an unparseable audit summary is UNAVAILABLE", st == R.UNAVAILABLE)

st, dt = R.classify_validator("31 checks, 1 FAIL", "", 0)
check("a validator reporting FAIL with exit 0 is still FAIL",
      st == R.FAIL and dt["failures"] == 1, json.dumps(dt, sort_keys=True))

# All five validator dialects that actually ship, so no gate silently degrades
# to an exit-code verdict.
for label, line, fails in (
        ("batch  '31 checks, 1 FAIL'", "E6 validator: 31 checks, 1 FAIL", 1),
        ("gap0609 '59 checks, 0 failed'", "validator: 59 checks, 0 failed", 0),
        ("controls '315 controls / 0 failures'", "\n315 controls / 0 failures", 0),
        ("tests   '10 tests, 0 failures'", "\n10 tests, 0 failures", 0),
        ("phase2  '107 PASS / 0 FAIL'", "\n107 PASS / 0 FAIL", 0)):
    st, dt = R.classify_validator(line, "", 0)
    check("validator dialect parses: %s" % label,
          dt.get("failures") == fails and st == (R.PASS if not fails else R.FAIL),
          json.dumps(dt, sort_keys=True))

st, dt = R.classify_validator("\n107 PASS / 3 FAIL", "", 0)
check("in the PASS/FAIL dialect the leading number is passes, not a total",
      dt.get("passes") == 107 and dt["failures"] == 3 and st == R.FAIL,
      json.dumps(dt, sort_keys=True))

st, dt = R.classify_validator("all done", "", 0)
check("an unrecognised summary says so rather than claiming a checked PASS",
      "no recognised validator summary" in dt.get("summary", ""), str(dt))


# ===========================================================================
# G. HEALTH USES THE LOCAL WORKING TREE FOR THE CANDIDATE SIDE
# ===========================================================================
print("\n--- G. health source ---")

health = REG.by_id("qb_health_check")
cmd = " ".join(health["command"])
check("G. candidate side is --source local", "--source local" in cmd, cmd)
check("G. candidate side never reads remote main",
      "--source remote" not in cmd and "remote" not in cmd, cmd)
check("G. candidate side does not email", "--no-email" in cmd, cmd)
check("G. baseline ref is a clean ref, not remote-main-vs-itself",
      REG.BASELINE_REF == "origin/main", REG.BASELINE_REF)

# Multiset semantics, and transport normalisation before comparison.
BASE_REPORT = "finding A\nfinding B\nfinding B\n"
CAND_REPORT = "finding A\nfinding B\nfinding B\nfinding C\n"
base, cand = R.health_findings(BASE_REPORT), R.health_findings(CAND_REPORT)
check("G. findings compare as a multiset", base["finding B"] == 2, "duplicates kept")
check("G. a new finding is detected", sum((cand - base).values()) == 1,
      "NEW=%d" % sum((cand - base).values()))
check("G. identical reports yield zero new and zero gone",
      not (cand - cand) and not (base - base))
check("G. CRLF transport does not manufacture findings",
      R.health_findings(BASE_REPORT.replace("\n", "\r\n")) == base,
      "normalised before comparison")
check("G. the source banner is excluded from the comparison",
      R.health_findings("source_type : local\ncommit : abc\nfindings    : 3\n"
                        + BASE_REPORT) == base,
      "banner is metadata, not a finding")


# ===========================================================================
# J. SERIAL OWNERSHIP + FAILURE PROPAGATION (stubbed process layer)
# ===========================================================================
print("\n--- J. serial ownership and failure propagation ---")

check("J. every mutation-parser gate is marked as mutating the worktree",
      all(g["mutates_worktree"] for g in REG.ALL_GATES
          if g["parser"] == REG.PARSER_MUTATION),
      "15/15 mutators serial")
check("J. validate_audit is marked mutating (it rewrites VALIDATION_RESULTS)",
      REG.by_id("validate_audit")["mutates_worktree"] is True)
check("J. determinism is marked mutating", REG.DETERMINISM_GATE["mutates_worktree"])
check("J. read-only gates are not marked mutating",
      not REG.by_id("node_security_tests")["mutates_worktree"]
      and not REG.by_id("content_index_check")["mutates_worktree"])

concurrent = {"max": 0, "now": 0}
order = []


def stub_process(argv, timeout, cwd=None):
    concurrent["now"] += 1
    concurrent["max"] = max(concurrent["max"], concurrent["now"])
    name = pathlib.Path(argv[-1]).name
    order.append(name)
    concurrent["now"] -= 1
    if "validate_batch_a" in name:
        return 1, "5 checks, 2 FAIL", "", 0.1
    return 0, "10 mutations, 0 escape(s), 0 no-op(s), 0 crash(es)\n8 checks, 0 FAIL", "", 0.1


real_process = R.run_process
R.run_process = stub_process
try:
    gates = [REG.by_id(g) for g in ("validate_batch_a", "batch_a_mutate",
                                    "validate_batch_b")]
    records = R.execute(gates, Args(gate=None), lambda m: None)
    check("J. never more than one gate runs at a time", concurrent["max"] == 1,
          "max concurrent = %d" % concurrent["max"])
    check("19. a release-critical failure stops the run immediately",
          len(records) == 1 and records[0]["status"] == R.FAIL,
          "%d record(s): %s" % (len(records), [r["status"] for r in records]))

    records = R.execute(gates, Args(gate=None, keep_going=True), lambda m: None)
    check("--keep-going continues past a failure", len(records) == 3,
          "%d records" % len(records))
    check("a gate whose dependency failed is SKIPPED, not silently passed",
          records[1]["status"] == R.SKIPPED,
          "batch_a_mutate=%s" % records[1]["status"])
    check("an independent later gate still runs", records[2]["status"] == R.PASS)
finally:
    R.run_process = real_process


# ===========================================================================
# 14. GENERATED-ARTEFACT SNAPSHOT AND RESTORE
# ===========================================================================
print("\n--- 14. restore safety ---")

with tempfile.TemporaryDirectory() as tmp:
    root = pathlib.Path(tmp)
    target = root / "gen.json"
    B.write_text(target, '{"live_questions": 721}\n')

    guard = R.ArtefactGuard(paths=[]).capture()
    guard.paths = [target]
    guard.capture()

    check("snapshot captures existing artefacts", target in guard.snapshot)
    check("an untouched artefact reports no drift", guard.verify(), "clean")

    target.write_text('{"live_questions": 688}\n', encoding="utf-8")
    check("drift is detected after a gate rewrites the artefact",
          [p.name for p in guard.dirtied()] == ["gen.json"], "detected")

    restored = guard.restore()
    check("restore returns the exact paths it put back",
          [p.name for p in restored] == ["gen.json"], "exact-path restore")
    check("restored bytes are the snapshotted bytes",
          B.read_text(target) == '{"live_questions": 721}\n', "byte-identical")
    check("restore is verified afterwards", guard.verify(), "verified")

    missing_file = root / "absent.json"
    guard2 = R.ArtefactGuard(paths=[])
    guard2.paths = [missing_file]
    guard2.capture()
    check("a non-existent artefact is skipped, not created",
          not guard2.snapshot and not missing_file.exists(), "skipped")

check("the registry names the artefacts gates are known to rewrite",
      len(REG.GENERATED_ARTEFACTS) == 3
      and all((REPO / p).exists() for p in REG.GENERATED_ARTEFACTS),
      ", ".join(pathlib.Path(p).name for p in REG.GENERATED_ARTEFACTS))

runner_src = B.read_text(HERE / "run_oral_release.py")

# Check what the runner EXECUTES, not what it says. The module documents the
# blanket-restore commands in order to state that it never issues them, so a
# raw substring scan would flag its own safety note.
git_calls = re.findall(r'\[\s*"git"\s*,([^\]]*)\]', runner_src)
ALLOWED_GIT = ("worktree", "add", "remove", "--detach", "--force")
bad_calls = []
for call in git_calls:
    words = re.findall(r'"([^"]+)"', call)
    if any(w not in ALLOWED_GIT for w in words):
        bad_calls.append(" ".join(words))
check("the runner's only git invocations are worktree add/remove",
      not bad_calls, "; ".join(bad_calls) or "%d git call(s)" % len(git_calls))
check("the runner issues no blanket restore",
      not any(re.search(r'"git"[^\]]*"(checkout|restore|reset|clean)"', c)
              for c in git_calls),
      "no checkout/restore/reset/clean anywhere in argv")
check("restoration is from the runner's own byte snapshot",
      "path.write_bytes(blob)" in runner_src and "self.snapshot" in runner_src,
      "never restores from git")


# ===========================================================================
# N. LOGGING CONTRACT
# ===========================================================================
print("\n--- N. logging ---")

with tempfile.TemporaryDirectory() as tmp:
    log_path = pathlib.Path(tmp) / "run.log"
    B.write_text(log_path, "line one\nline two\n")
    raw = log_path.read_bytes()
    check("N. logs are written LF-only -- no CRLF doubling",
          b"\r" not in raw, "%d bytes, no CR" % len(raw))
    check("N. log content round-trips", B.read_text(log_path) == "line one\nline two\n")

check("N. the runner writes logs through the explicit-newline helper",
      "write_text(log_path" in runner_src and "write_text(json_path" in runner_src,
      "no newline-translating stream")
check("21. logs default outside the repository",
      "mkdtemp" in runner_src and "never the repo" in runner_src,
      "scratch dir by default")
check("21. the run record is machine-readable",
      '"records": records' in runner_src and "json.dumps" in runner_src)


# ===========================================================================
# 20. INTERRUPTION SAFETY
# ===========================================================================
print("\n--- 20. interruption ---")

check("20. KeyboardInterrupt is caught and does not continue into later gates",
      "except KeyboardInterrupt" in runner_src
      and "did NOT continue into later" in runner_src)
check("20. an interrupted run exits 130", "code = 130" in runner_src)
check("20. the runner leaves a recovery message rather than pretending to repair",
      "verify with `git status`" in runner_src)


# ===========================================================================
# M. CONTROL BYTES / ENCODING
# ===========================================================================
print("\n--- M. byte safety ---")

OWN = [HERE / "run_oral_release.py", HERE / "oral_release_gates.py",
       HERE / "test_oral_release_runner.py", HERE / "SKILL.md"]
hits = B.scan_paths(OWN)
check("M. runner, registry, tests and skill are control-byte clean", hits == [],
      "; ".join(h.describe() for h in hits) or "%d files scanned" % len(OWN))
check("M. no Windows backslash path leaks into a gate command",
      not any("\\" in part for g in REG.ALL_GATES for part in g["command"]),
      "all repo-relative POSIX paths")
check("18. historical guards are not silently skipped",
      all(g["always_run"] for g in REG.historical_39()),
      "all 39 always_run")
check("18. the runtime optimisation is recorded as a proposal only",
      "Not implemented" in REG.PROPOSED_OPTIMISATIONS
      and "RISK" in REG.PROPOSED_OPTIMISATIONS,
      "documented, not applied")


# ===========================================================================
# 19. A MUTATING GATE MUST HAND BACK THE TREE
# ===========================================================================
# mutate_batch_a died between injecting an editorial marker and restoring it and
# left that marker in a real product page. Six harnesses restore only on the
# happy path, so the runner guards the bytes itself -- the same discipline
# ArtefactGuard already applies to the generated artefacts, but a STRICTER
# class: a mutating gate legitimately rewrites those, and must leave these
# byte-identical.

check("the registry declares the product surface a mutating gate must not move",
      bool(REG.PRODUCT_GUARDED_GLOBS)
      and any("QB" in g for g in REG.PRODUCT_GUARDED_GLOBS),
      str(REG.PRODUCT_GUARDED_GLOBS))

_guard = R.ArtefactGuard().capture()
check("the guard actually snapshots product bytes, not an empty set",
      len(_guard.product_snapshot) > 80,
      "%d file(s) snapshotted" % len(_guard.product_snapshot))
check("the two classes are kept apart",
      not (set(_guard.snapshot) & set(_guard.product_snapshot)),
      "a generated artefact is restored quietly; a product page is a defect")

# Non-vacuity, both directions: an untouched tree must report nothing, and a
# changed byte must be seen AND put back exactly.
check("an untouched tree reports no product drift", not _guard.product_dirtied())

_victim = sorted(_guard.product_snapshot)[0]
_original = _victim.read_bytes()
try:
    _victim.write_bytes(_original + b"<!-- probe -->")
    check("a changed product byte is detected",
          _guard.product_dirtied() == [_victim], _victim.name)
    _moved = _guard.restore_product()
    check("it is put back from the runner's OWN snapshot, by exact path",
          _moved == [_victim] and _victim.read_bytes() == _original,
          "never `git checkout -- .`, which destroys uncommitted work")
finally:
    _victim.write_bytes(_original)
check("the probe left nothing behind", _victim.read_bytes() == _original)

check("a gate that leaves product bytes dirty is FAILED, not merely tidied",
      "product_left_dirty" in _runner_src
      and "status = FAIL" in _runner_src.split("product_left_dirty")[1][:400],
      "the harness gets fixed, not the symptom")

check("every child process is given an explicit UTF-8 stdout",
      'setdefault("PYTHONIOENCODING", "utf-8")' in _runner_src,
      "covers the non-Python gates the runner drives too")


# ===========================================================================
# 20. A KILLED GATE IS NOT A FAILED CHECK
# ===========================================================================
# batch_e5_mutate was killed at exactly 2400.1s and reported "no parseable
# mutation summary" -- true, and completely misleading. It reads as a broken
# harness when the harness was simply not given enough time, and it hides that
# the kill landed INSIDE a mutation and left a product page dirty.

_status, _detail = R.classify_mutation("", "TIMEOUT after 2400s", 124)
check("a timed-out mutation suite is reported as a TIMEOUT",
      _status == R.UNAVAILABLE and _detail.get("timeout") is True
      and "TIMEOUT" in _detail["error"],
      _detail["error"][:80])
check("a genuinely unparseable summary still says so",
      R.classify_mutation("nothing useful here", "", 1)[1].get("timeout") is None,
      "the two diagnoses stay distinct")
check("a healthy suite is unaffected by the timeout branch",
      R.classify_mutation("12 mutations, 0 escape(s), 0 no-op(s), 0 crash(es)",
                          "", 0)[0] == R.PASS)

# A timeout is a resource bound, and one tuned to a stopwatch expires: every
# validator gets slower as the authorisation surface grows, because every one of
# them scans it. The registry must carry the ARITHMETIC, not just a number.
_reg_src = (Path(REG.__file__)).read_text(encoding="utf-8")
check("the registry records how to size a mutation timeout",
      "mutations + 2" in _reg_src and "SIZING A MUTATION TIMEOUT" in _reg_src,
      "(mutations + 2) x the validator's own runtime")
check("the two suites that needed resizing carry their arithmetic",
      REG.by_id("batch_e5_mutate")["timeout"] >= 5000
      and REG.by_id("batch_e6_mutate")["timeout"] >= 4000,
      "e5=%ds e6=%ds" % (REG.by_id("batch_e5_mutate")["timeout"],
                         REG.by_id("batch_e6_mutate")["timeout"]))


# ===========================================================================
print("\n%d checks, %d FAIL" % (CHECKS[0], len(FAILURES)))
for f in FAILURES:
    print("  FAIL %s" % f)
sys.exit(1 if FAILURES else 0)
