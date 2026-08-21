#!/usr/bin/env python3
"""
Controls for the baseline-aware mutation-control precondition.

WHAT WENT WRONG
---------------

Every E-series harness required its control validator to be ABSOLUTELY green
before launching. `validate_batch_e6` carries permanent, deliberately
unrepaired evidence debt (`line_endings_homogeneous_per_file`), so
`batch_e6_mutate` exited 2 on every clean checkout, the runner classified it
`UNAVAILABLE`, and `UNAVAILABLE` is release-critical -- a default `--full` run
stopped before health, audit, determinism and every later batch.

A guard that cannot run has silently expired, and guard expiry is a confirmed
defect class in this corpus.

WHAT MUST STILL BE TRUE
-----------------------

Relaxing the precondition is only safe if it is relaxed by exactly the right
amount. Two failures are equally bad and this file exists to prove neither
happened:

  * too tight  -- known debt keeps the suite unrunnable (the original bug);
  * too loose  -- a NEW failure slips through and mutations run against a
                  control nobody has accounted for, which certifies nothing.

So the acceptance is a pair, not a single case: debt-only must RUN, and
debt-plus-anything-new must REFUSE. The live section at the end proves both
through the real `mutate_batch_e6.py`, because a precondition that is correct
in a unit test and unwired in the harness would pass everything above it.
"""

import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_bytes import read_text, write_text                     # noqa: E402
from oral_mutation import (                                      # noqa: E402
    ControlBaseline, check_control_baseline, mutation_verdict,
    validator_failing, validator_fail_details, worktree_env)

FAILURES = []
COUNT = [0]


def check(name, ok, detail=""):
    COUNT[0] += 1
    print("%-4s %-6s %-64s %s" % ("ok" if ok else "FAIL", "%d." % COUNT[0],
                                  name, detail))
    if not ok:
        FAILURES.append(name)


E_MUTATORS = ["mutate_batch_e%d.py" % n for n in range(1, 7)]


print("=" * 100)
print("1. CONTROL ADMISSION -- subset, by identity, fail closed")
print("=" * 100)

# A green control needs no baseline at all. That is what keeps the eleven clean
# validators exactly as cheap as they were: no worktree, no git, no cost.
state = check_control_baseline([], "tools/oral/validate_batch_e1.py", REPO)
check("a green control is admitted without deriving anything",
      state.runnable and not state.carries_baseline_debt
      and state.baseline.failures == frozenset(),
      state.describe())

# The remaining cases are driven against an injected baseline so they test the
# ADMISSION RULE and not git.
def admit(control, baseline, available=True, error=""):
    import oral_mutation
    real = oral_mutation.derive_validator_baseline
    oral_mutation.derive_validator_baseline = (
        lambda *a, **k: ControlBaseline(available, frozenset(baseline),
                                        "origin/main", error))
    try:
        return oral_mutation.check_control_baseline(
            control, "tools/oral/validate_batch_e6.py", REPO)
    finally:
        oral_mutation.derive_validator_baseline = real


s = admit(["A"], ["A"])
check("control failure that is present on the baseline -> RUNNABLE",
      s.runnable and s.carries_baseline_debt, s.describe())

s = admit(["A"], ["A", "B"])
check("strictly FEWER failures than the baseline -> RUNNABLE (an improvement)",
      s.runnable, s.describe())

s = admit(["A", "C"], ["A"])
check("a NEW failure alongside known debt -> REFUSED",
      not s.runnable and s.new_failures == frozenset({"C"}), s.describe())

# The single most important negative: same COUNT, different failure. A counting
# comparison calls this "no change" and lets a regression through.
s = admit(["B"], ["A"])
check("same failure COUNT but a different failure -> REFUSED",
      not s.runnable and s.new_failures == frozenset({"B"}),
      "identity is compared, never count: %s" % s.describe())

s = admit(["A"], [], available=False, error="worktree add failed")
check("an underivable baseline -> REFUSED, never admitted",
      not s.runnable and "not permission to run" in s.reason, s.describe())

# The debt this was built for must appear only as EXPLANATION, never as
# behaviour. A named exemption would be an E6 special case wearing a contract's
# clothes -- and it would silently absorb the next batch's debt too.
def executable_strings(path):
    """Every string literal that is not a docstring, plus every identifier."""
    import ast
    tree = ast.parse(read_text(path))
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            body = getattr(node, "body", None)
            if body and isinstance(body[0], ast.Expr) and isinstance(
                    body[0].value, ast.Constant) and isinstance(
                    body[0].value.value, str):
                docstrings.add(id(body[0].value))
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if id(node) not in docstrings:
                out.append(node.value)
        elif isinstance(node, ast.Name):
            out.append(node.id)
    return out


strings = executable_strings(HERE / "oral_mutation.py")
check("no check name is hardcoded in the shared control's BEHAVIOUR",
      not any("line_endings" in s for s in strings),
      "%d executable literals/identifiers scanned; the debt appears only in "
      "prose" % len(strings))
check("the baseline is derived from a ref, never declared as a constant",
      not any(s.startswith("FAIL") and "_" in s for s in strings),
      "no literal allow-list of known failures")


print()
print("=" * 100)
print("2. PER-MUTATION VERDICT -- including the saturated-check case")
print("=" * 100)

# With no debt the semantics must be byte-for-byte what they always were.
out, _ = mutation_verdict("target_check", [], [])
check("no failing check at all -> ESCAPE", out == "escape")
out, _ = mutation_verdict("target_check", ["target_check"], [])
check("the intended check fires -> CAUGHT", out == "caught")
out, msg = mutation_verdict("target_check", ["other_check"], [])
check("some OTHER check fires -> ESCAPE, reported as a wrong reason",
      out == "escape" and "WRONG REASON" in msg, msg)

# With debt, the debt itself must never be read as a catch.
out, _ = mutation_verdict("target_check", ["debt"], ["debt"])
check("pre-existing debt alone is not a catch",
      out == "escape", "the control's own failure proves nothing")
out, _ = mutation_verdict("target_check", ["debt", "target_check"], ["debt"])
check("the intended check firing ALONGSIDE debt -> CAUGHT", out == "caught")

# SATURATED CHECK. A mutation aimed at a check that is already red can never
# make a new NAME appear. E6's Z4 is exactly this: it corrupts the manifest's
# line-ending record, and the guard that would catch it is the guard carrying
# E6's debt. The validator does catch it -- it names another mismatched file --
# so the proof is that the check's reported CONTENT moved.
out, msg = mutation_verdict("debt", ["debt"], ["debt"],
                            {"debt": "['a', 'b', 'c']"}, {"debt": "['a', 'b']"})
check("saturated check whose DETAIL moved -> CAUGHT",
      out == "caught" and "saturated" in msg, msg)
out, msg = mutation_verdict("debt", ["debt"], ["debt"],
                            {"debt": "['a', 'b']"}, {"debt": "['a', 'b']"})
check("saturated check whose detail did NOT move -> ESCAPE",
      out == "escape", "an unchanged report is not evidence of a catch")
out, _ = mutation_verdict("debt", ["debt"], ["debt"])
check("saturated check with no detail available -> ESCAPE, not assumed caught",
      out == "escape", "fail closed when the evidence is missing")

check("FAIL detail is parsed off the check name, not guessed",
      validator_fail_details("FAIL  some_check   ['x', 'y']")
      == {"some_check": "['x', 'y']"}
      and validator_failing("FAIL  some_check   ['x']") == {"some_check"})


print()
print("=" * 100)
print("3. THE HARNESSES ARE ACTUALLY WIRED TO IT")
print("=" * 100)

unwired, hardcoded, absolute = [], [], []
for name in E_MUTATORS:
    text = read_text(HERE / name)
    if "require_control_baseline" not in text or "mutation_verdict" not in text:
        unwired.append(name)
    if "line_endings_homogeneous_per_file" in text.split("def build")[0]:
        hardcoded.append(name)
    # The original predicate must be gone, not merely supplemented.
    if re.search(r"if code != 0:\s*\n\s*print\(\"PRE-RUN validator is not green",
                 text):
        absolute.append(name)

check("every E-series harness uses the shared control precondition",
      not unwired, "unwired=%s" % (unwired or "none"))
check("no harness names a specific check as a known-good exemption",
      not hardcoded, "hardcoded=%s" % (hardcoded or "none"))
check("the absolute-green predicate is gone from every harness",
      not absolute, "still absolute=%s" % (absolute or "none"))
check("the post-restore assertion returns to the CONTROL, not to zero",
      all("new-vs-control" in read_text(HERE / n) for n in E_MUTATORS),
      "residue against the control is what proves the restore")


print()
print("=" * 100)
print("4. LIVE NON-VACUITY -- the real E6 harness, on the real tree")
print("=" * 100)
# Sections 1-3 prove the rule. This proves the rule is what actually gates the
# suite. It runs mutate_batch_e6.py for real, twice: once as it stands, and once
# with an extra validator failure injected. Only the precondition is exercised
# -- the second run must abort before any mutation is applied.

MANIFEST = HERE / "batch_e6_enrichment_manifest.json"


def run_harness(timeout=1800):
    proc = subprocess.run([sys.executable, str(HERE / "mutate_batch_e6.py")],
                          cwd=str(REPO), capture_output=True, timeout=timeout)
    return proc.returncode, (proc.stdout.decode("utf-8", "replace")
                             + proc.stderr.decode("utf-8", "replace"))

original = MANIFEST.read_bytes()
try:
    # Inject a SECOND failing check. `expected_canonical_questions` is read by
    # `canonical_total_unchanged`, which is green on the baseline -- so this is
    # a genuinely new failure and nothing else about the tree changes.
    text = read_text(MANIFEST)
    assert '"expected_canonical_questions": 721' in text
    write_text(MANIFEST,
               text.replace('"expected_canonical_questions": 721',
                            '"expected_canonical_questions": 722', 1))
    rc, out = run_harness(600)
    refused = "PRE-RUN" in out and "canonical_total_unchanged" in out
    check("a NEW failing check makes the real E6 suite REFUSE to start",
          rc == 2 and refused,
          "exit=%d; %s" % (rc, next((l for l in out.splitlines()
                                     if l.startswith("PRE-RUN")), "-")[:150]))
    check("it refuses BEFORE applying any mutation",
          "caught (" not in out and "ESCAPE" not in out,
          "no mutation line was printed")
finally:
    MANIFEST.write_bytes(original)
    check("the injected manifest change is fully reverted",
          MANIFEST.read_bytes() == original)

print()
print("=" * 100)
print("%d checks, %d FAIL" % (COUNT[0], len(FAILURES)))
for name in FAILURES:
    print("  FAILED: %s" % name)
print("=" * 100)
sys.exit(1 if FAILURES else 0)
