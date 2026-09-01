#!/usr/bin/env python3
"""
Shared mutation infrastructure for the Oral release toolchain.

Two pieces of knowledge that cost real production time now live here as code
rather than as prose each session has to remember.

--------------------------------------------------------------------------
A. PREFLIGHT -- prove every mutation changes bytes BEFORE the expensive suite
--------------------------------------------------------------------------

A mutation that matches nothing writes nothing and exercises nothing.  It is
not a passing test; it is an absent test that reports like a passing one.

This happened twice.  E5's mutation C and E6's mutation H were both anchored on
patterns that read correctly in the prose they were written in and wrong in the
markup they were written into -- E6's read ``resolution <strong>MSC.550(108)</strong>``
where the card reads ``<strong>resolution MSC.550(108)</strong>``: the opening
tag sits *before* the word.  E6's suite ran for 22 minutes to discover it.

``preflight()`` applies every mutation in memory, touches no disk, and reports a
byte delta per mutation in seconds.  If any mutation is a no-op the suite must
not launch.

--------------------------------------------------------------------------
B. SUMMARY PARSING -- key=value before bare numbers, always
--------------------------------------------------------------------------

Fifteen mutation harnesses print six different summary dialects.  A loose
``(\\d+)\\s*escape`` pattern reads the **8** in ``mutations=8 escapes=0`` as the
escape count.  E5 documented that exact failure and its fix; E6 wrote the
fallback order backwards and reproduced it anyway.  A neighbouring
``fails=2 crash=False`` was separately misread as two crashes.

The ordering constraint therefore belongs in shared code.  ``parse_summary()``
reads key=value forms FIRST and, once a field has been read that way, never
falls back to the bare-number form for that field.

The six live dialects, all covered by the self-tests:

    33 mutations, 0 escape(s), 0 no-op(s), 0 crash(es)      batch_e1..e6
    12 mutations, 0 escape(s), 0 not applied, 0 crash(es)   batch_a..d
    17 mutations, 0 escapes                                 ce_tip, examiner
    mutations=8 escapes=0 no-ops=0 crashes=0                gap0609
    33 mutations / 0 escapes                                phase2
    mutations: 26 run, 0 escape(s), 0 crash(es); ...        qb_content_index
"""

from __future__ import annotations

import dataclasses
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Callable, Iterable, Sequence

from oral_bytes import read_text

# ---------------------------------------------------------------- preflight


@dataclasses.dataclass(frozen=True)
class MutationSpec:
    """One mutation, described well enough to dry-run without touching disk."""

    mutation_id: str
    target: str
    apply: Callable[[str], str]
    intended_reason: str = ""

    def __post_init__(self) -> None:
        if not self.mutation_id:
            raise ValueError("mutation_id is required")
        if not callable(self.apply):
            raise TypeError("apply must be callable")


def replace_spec(mutation_id: str, target: str, old: str, new: str,
                 intended_reason: str = "", count: int = 1) -> MutationSpec:
    """A literal search-and-replace mutation.

    ``str.replace`` on an anchor that has moved silently no-ops, which is the
    whole reason preflight exists -- so this helper exists to be preflighted,
    never to be trusted unchecked.
    """
    return MutationSpec(
        mutation_id=mutation_id,
        target=target,
        apply=lambda text: text.replace(old, new, count),
        intended_reason=intended_reason,
    )


@dataclasses.dataclass(frozen=True)
class PreflightResult:
    """The per-mutation contract required before any suite launches."""

    mutation_id: str
    target: str
    applied: bool
    pre_size: int
    post_size: int
    byte_delta: int
    error: str = ""

    def describe(self) -> str:
        if self.error:
            return "%-6s %-28s ERROR %s" % (self.mutation_id, self.target, self.error)
        state = "applied" if self.applied else "NO-OP"
        return (
            "%-6s %-28s %-8s pre=%d post=%d delta=%+d"
            % (self.mutation_id, self.target, state,
               self.pre_size, self.post_size, self.byte_delta)
        )


def preflight(specs: Sequence[MutationSpec],
              root: str | pathlib.Path = ".") -> list[PreflightResult]:
    """Dry-run every mutation in memory.  Never writes to disk.

    Sizes are measured in UTF-8 bytes, not characters, so the delta is the real
    on-disk delta the suite will produce.
    """
    root = pathlib.Path(root)
    results: list[PreflightResult] = []

    for spec in specs:
        path = root / spec.target
        try:
            before = read_text(path)
        except OSError as exc:
            results.append(PreflightResult(
                spec.mutation_id, spec.target, False, 0, 0, 0,
                error="target unreadable: %s" % exc))
            continue

        try:
            after = spec.apply(before)
        except Exception as exc:  # a mutation that throws is also not a test
            results.append(PreflightResult(
                spec.mutation_id, spec.target, False, 0, 0, 0,
                error="%s: %s" % (type(exc).__name__, exc)))
            continue

        pre = len(before.encode("utf-8"))
        post = len(after.encode("utf-8"))
        results.append(PreflightResult(
            mutation_id=spec.mutation_id,
            target=spec.target,
            applied=after != before,
            pre_size=pre,
            post_size=post,
            byte_delta=post - pre,
        ))

    return results


def preflight_or_die(specs: Sequence[MutationSpec],
                     root: str | pathlib.Path = ".",
                     echo: bool = True) -> list[PreflightResult]:
    """Preflight, print the contract, and raise unless every mutation applies.

    Call this as the first statement of a mutation harness's ``main()``.  It
    turns a 22-minute discovery into a two-second one.
    """
    results = preflight(specs, root=root)
    if echo:
        for result in results:
            print(result.describe())

    bad = [r for r in results if not r.applied]
    if echo:
        print("preflight: mutations=%d applied=%d no-ops=%d"
              % (len(results), len(results) - len(bad), len(bad)))
    if bad:
        raise AssertionError(
            "mutation suite must NOT launch -- %d mutation(s) change no bytes:\n  %s"
            % (len(bad), "\n  ".join(r.describe() for r in bad))
        )
    return results


# ------------------------------------------------------------ summary parse

# Field name -> the alias fragments a harness might print for it.
_FIELD_ALIASES: dict[str, str] = {
    "run": r"mutations?|run",
    "escapes": r"escapes?",
    "no_ops": r"no[-_ ]?ops?|not\s+applied|noops?",
    "crashes": r"crash(?:es)?",
    "caught": r"caught",
}

# key=value, e.g. "escapes=0" or "no-ops = 2".  Read FIRST, always.
_KV = {
    field: re.compile(r"(?:%s)\s*[=:]\s*(\d+)" % alias, re.I)
    for field, alias in _FIELD_ALIASES.items()
}

# bare number, e.g. "0 escape(s)".  Only consulted when no key=value form for
# that field appeared on the line.  ``(?<![=\d])`` stops "fails=2 crash=False"
# donating its 2 to the crash count.
_BARE = {
    field: re.compile(r"(?<![=\d])(\d+)\s*(?:%s)\b" % alias, re.I)
    for field, alias in _FIELD_ALIASES.items()
}

# "mutations: 26 run" -- the count follows the word.
_RUN_AFTER = re.compile(r"mutations?\s*[:=]?\s*(\d+)\s*run\b", re.I)


@dataclasses.dataclass(frozen=True)
class MutationSummary:
    """The normalised result contract every suite is read into."""

    run: int
    escapes: int
    caught: int
    no_ops: int
    crashes: int
    source_line: str
    dialect: str

    @property
    def green(self) -> bool:
        return (self.escapes == 0 and self.no_ops == 0
                and self.crashes == 0 and self.run > 0)

    def describe(self) -> str:
        return ("run=%d caught=%d escapes=%d no_ops=%d crashes=%d"
                % (self.run, self.caught, self.escapes, self.no_ops, self.crashes))


def _read_line(line: str) -> dict[str, int] | None:
    """Extract every field present on one line, key=value taking precedence."""
    found: dict[str, int] = {}
    dialect_kv = False

    for field, pattern in _KV.items():
        matches = pattern.findall(line)
        if matches:
            found[field] = int(matches[-1])
            dialect_kv = True

    if "run" not in found:
        after = _RUN_AFTER.search(line)
        if after:
            found["run"] = int(after.group(1))

    for field, pattern in _BARE.items():
        if field in found:
            # key=value already answered this field.  Never fall back --
            # this single line is the whole defence against reading the 8 in
            # "mutations=8 escapes=0" as an escape count.
            continue
        matches = pattern.findall(line)
        if matches:
            found[field] = int(matches[-1])

    if "run" not in found or "escapes" not in found:
        return None
    found["_kv"] = 1 if dialect_kv else 0
    return found


def parse_summary(text: str) -> MutationSummary:
    """Parse a mutation harness's output into the normalised contract.

    Selects the LAST line carrying BOTH a mutation count and an escape count --
    per-mutation detail lines and baseline banners carry neither, so they cannot
    be mistaken for the summary.
    """
    chosen: dict[str, int] | None = None
    chosen_line = ""

    for line in text.splitlines():
        if not line.strip():
            continue
        read = _read_line(line)
        if read is not None:
            chosen = read
            chosen_line = line.strip()

    if chosen is None:
        raise ValueError(
            "no parseable mutation summary found (need a line carrying both a "
            "mutation count and an escape count)"
        )

    run = chosen["run"]
    escapes = chosen["escapes"]
    no_ops = chosen.get("no_ops", 0)
    crashes = chosen.get("crashes", 0)
    # Most harnesses do not print "caught" -- it is derivable and must be, so
    # that a suite reporting only run/escapes still fills the contract.
    caught = chosen.get("caught", run - escapes - no_ops - crashes)

    return MutationSummary(
        run=run,
        escapes=escapes,
        caught=caught,
        no_ops=no_ops,
        crashes=crashes,
        source_line=chosen_line,
        dialect="key=value" if chosen.get("_kv") else "prose",
    )


def aggregate(summaries: Iterable[MutationSummary]) -> MutationSummary:
    """Total several suites into one contract.

    E6 aggregated fifteen suites with a single regex and reported 8 phantom
    escapes and 4 phantom crashes.  Parse each suite separately with
    ``parse_summary``, then total the structured results here.
    """
    items = list(summaries)
    return MutationSummary(
        run=sum(s.run for s in items),
        escapes=sum(s.escapes for s in items),
        caught=sum(s.caught for s in items),
        no_ops=sum(s.no_ops for s in items),
        crashes=sum(s.crashes for s in items),
        source_line="aggregate of %d suite(s)" % len(items),
        dialect="aggregate",
    )


# ------------------------------------------------- C. BASELINE-AWARE CONTROL
#
# A mutation suite proves that a VALIDATOR catches corruption.  To mean
# anything, the control state -- the tree the suite starts from -- must be one
# where the validator is not already complaining about the thing under test.
#
# Every E-series harness spelled that requirement as ABSOLUTE:
#
#     code, failed = run_validator()
#     if code != 0:
#         print("PRE-RUN validator is not green - aborting"); return 2
#
# which is the right idea and the wrong predicate.  `validate_batch_e6` fails
# `line_endings_homogeneous_per_file` on a clean checkout of the very commit it
# certified: its manifest pinned a pre-normalisation CRLF working copy while
# `.gitattributes` pins *.html to LF.  The product bytes are correct; the
# recorded evidence is not reproducible.  That debt is real, it must not be
# silenced, and it must not be repaired -- and because of it the E6 mutation
# suite could not be launched AT ALL on a clean main.  A guard that cannot run
# is a guard that has silently expired, which is a confirmed defect class here.
#
# The correct precondition is not "zero failures" but "no NEW failures":
#
#     baseline = validator's failing checks on BASELINE_REF (clean worktree)
#     control  = validator's failing checks on the current worktree
#     runnable iff control <= baseline
#
# IDENTITY, NEVER COUNT.  baseline {A} vs control {B} is the same size and is a
# regression.  baseline {A,B} vs control {A} is strictly fewer failures and is
# an improvement, which must not abort.  Comparing counts gets the first case
# wrong in the only direction that matters.
#
# DERIVED, NEVER DECLARED.  The baseline is re-derived from the ref on each
# run.  A hardcoded allow-list of "known failures" absorbs the next real
# regression the moment someone forgets to prune it -- the same reason
# `classify_audit` derives its baseline rather than storing one.
#
# COST.  Deriving a baseline needs a temporary worktree, which is not free.  So
# it is derived ONLY when the control is not already absolutely green.  For the
# eleven validators that pass cleanly the behaviour, and the cost, are exactly
# what they were before.
#
# FAIL CLOSED.  If the baseline cannot be derived -- no git, no ref, a worktree
# that will not create -- the control is NOT accepted.  An underivable baseline
# is never an excuse to run a suite against an unknown control, for the same
# reason the runner never promotes an underivable baseline to PASS.


def validator_failing(text: str) -> set:
    """The check names a batch-dialect validator reported as FAIL.

    One definition, used by the runner's gate classification and by every
    mutation harness's control check, so "which checks are failing" cannot come
    to mean two different things in the two places that compare it.

    SIX dialects, not five. `validate_study_spine.py` INDENTS its failures and
    suffixes the check name with a colon::

          FAIL R-ACCOUNT-ORAL: mapped 699 + unresolved 39 != corpus 759

    An anchored `^FAIL` matched none of them, so that gate had no derivable
    baseline: it could only ever be classified FAIL, and a default --full run
    stopped at gate 5 of 66 with sixty-one guards unrun. "A guard that cannot
    run has silently expired" is a confirmed defect class here, and sixty-one
    of them is the largest instance of it this repository has had.

    Leading whitespace is now allowed and one trailing colon is stripped.
    Deliberately NOT widened to `FAIL:` with no space -- a mutator log's own
    `FAIL:` evidence lines must keep failing to match, because they are
    caught-evidence, not failures.
    """
    return {name.rstrip(":")
            for name in re.findall(r"^[ \t]*FAIL\s+(\S+)", text, re.M)}


def worktree_env(work) -> dict:
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


@dataclasses.dataclass(frozen=True)
class ControlBaseline:
    """What a validator fails on the baseline ref, and whether that is known."""

    available: bool
    failures: frozenset
    ref: str
    error: str = ""

    def describe(self) -> str:
        if not self.available:
            return "baseline UNAVAILABLE (%s): %s" % (self.ref, self.error)
        return "baseline(%s) failures=%s" % (
            self.ref, sorted(self.failures) or "none")


def derive_validator_baseline(validator_rel, repo, ref="origin/main",
                              timeout=1800) -> ControlBaseline:
    """Run one validator on a clean detached worktree of ``ref``.

    A temporary worktree, never a checkout of the real tree: the caller's
    working copy holds the state under test and must not be moved out from
    under it.  The worktree is removed in ``finally`` whether or not the
    validator succeeded.
    """
    repo = pathlib.Path(repo)
    rel = pathlib.Path(validator_rel).as_posix()
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="oral-control-baseline-"))
    work = tmp / "tree"
    try:
        made = subprocess.run(
            ["git", "worktree", "add", "--detach", str(work), ref],
            cwd=str(repo), capture_output=True)
        if made.returncode != 0:
            return ControlBaseline(
                False, frozenset(), ref,
                made.stderr.decode("utf-8", "replace").strip()[:200])
        proc = subprocess.run(
            [sys.executable, rel], cwd=str(work), capture_output=True,
            timeout=timeout, env=worktree_env(work))
        text = (proc.stdout.decode("utf-8", "replace")
                + "\n" + proc.stderr.decode("utf-8", "replace"))
        return ControlBaseline(True, frozenset(validator_failing(text)), ref)
    except (OSError, subprocess.SubprocessError) as exc:
        return ControlBaseline(False, frozenset(), ref,
                               "%s: %s" % (type(exc).__name__, exc))
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(work)],
                       cwd=str(repo), capture_output=True)
        shutil.rmtree(tmp, ignore_errors=True)


@dataclasses.dataclass(frozen=True)
class ControlState:
    """The verdict on whether a mutation suite may launch."""

    runnable: bool
    control_failures: frozenset
    baseline: ControlBaseline
    new_failures: frozenset
    reason: str

    @property
    def carries_baseline_debt(self) -> bool:
        return bool(self.control_failures)

    def describe(self) -> str:
        if self.runnable and not self.control_failures:
            return "control GREEN (no failing checks)"
        if self.runnable:
            return ("control CARRIES BASELINE DEBT only: %s -- %s"
                    % (sorted(self.control_failures), self.baseline.describe()))
        return "control REFUSED: %s" % self.reason


def check_control_baseline(control_failures, validator_rel, repo,
                           ref="origin/main", timeout=1800) -> ControlState:
    """May a mutation suite launch from this control state?

    ``control_failures`` is the set of check names the validator failed on the
    CURRENT worktree.  The baseline is derived only when that set is non-empty,
    so a green control costs nothing and behaves exactly as it always has.
    """
    control = frozenset(control_failures)
    if not control:
        return ControlState(True, control,
                            ControlBaseline(True, frozenset(), ref),
                            frozenset(), "control is green")

    baseline = derive_validator_baseline(validator_rel, repo, ref, timeout)
    if not baseline.available:
        return ControlState(
            False, control, baseline, control,
            "control fails %s and the baseline could not be derived from %s "
            "(%s) -- an underivable baseline is not permission to run"
            % (sorted(control), ref, baseline.error))

    new = control - baseline.failures
    if new:
        return ControlState(
            False, control, baseline, frozenset(new),
            "control introduces %d failure(s) absent from the baseline: %s"
            % (len(new), sorted(new)))

    return ControlState(
        True, control, baseline, frozenset(),
        "control failures %s are all present on the baseline"
        % sorted(control))


def require_control_baseline(control_failures, validator_rel, repo,
                             ref="origin/main", timeout=1800,
                             echo=True) -> ControlState:
    """``check_control_baseline`` plus the printed contract a reviewer reads.

    Call this in place of a bare ``if code != 0: return 2`` precondition.  The
    caller still decides the exit code, because a refused control is exit 2
    (UNAVAILABLE, the suite never ran) and not exit 1 (the suite ran and found
    something).
    """
    state = check_control_baseline(control_failures, validator_rel, repo,
                                   ref=ref, timeout=timeout)
    if echo:
        if state.control_failures and state.baseline.available:
            print("CONTROL  %s" % state.baseline.describe())
        print("CONTROL  %s" % state.describe())
    return state


def validator_fail_details(text) -> dict:
    """check name -> the detail text it reported, for FAIL lines only.

    A failing check says WHICH items failed, not merely that something did.
    That detail is the only signal available when a mutation targets a check
    that is ALREADY failing -- see ``mutation_verdict``.
    """
    details = {}
    for line in text.splitlines():
        if not line.startswith("FAIL"):
            continue
        parts = line.split(None, 2)
        if len(parts) >= 2:
            details[parts[1]] = parts[2].strip() if len(parts) > 2 else ""
    return details


def mutation_verdict(expected_check, failures_now, baseline_failures,
                     details_now=None, details_baseline=None):
    """Classify one applied mutation against a possibly-indebted baseline.

    ``code == 0`` cannot be the escape test once a control legitimately carries
    a pre-existing failure, because the validator then never exits 0 and every
    mutation would read as caught.  The first question is therefore whether a
    NEW failing check appeared, and whether it is the intended one.  With an
    empty baseline that is exactly the original semantics.

    CHECK SATURATION -- why the detail is also read
    -----------------------------------------------
    A name-set comparison is blind to any mutation aimed at a check that is
    ALREADY red.  E6's mutation Z4 misrecords a destination file's line endings
    and is meant to be caught by ``line_endings_homogeneous_per_file`` -- the
    very check carrying E6's evidence debt.  The validator DOES catch it, and
    says so by naming a third mismatched file; the check name alone cannot move,
    because it was already failing.

    Reading the name only would report that as an escape and let a real,
    demonstrated catch be recorded as a hole in the guard.  Reading it as caught
    without evidence would be worse.  So the detail is compared: the mutation is
    caught when the intended check's REPORTED CONTENT changed, and an escape
    when the validator's output did not move at all.

    This was invisible for as long as the suite could not launch -- the
    line-ending debt was hiding a second defect behind the first.
    """
    new = frozenset(failures_now) - frozenset(baseline_failures)
    if expected_check in new:
        return "caught", "caught (%s)" % expected_check

    # Saturated check: already failing on the control, so it cannot appear as a
    # NEW name. It is a catch only if what it reports actually changed.
    if expected_check in frozenset(baseline_failures) and details_now is not None:
        was = (details_baseline or {}).get(expected_check)
        now = details_now.get(expected_check)
        if was is not None and now is not None and was != now:
            return "caught", ("caught (%s, saturated check: detail moved)"
                              % expected_check)

    if not new:
        return "escape", "*** ESCAPE (no new failing check, no detail change) ***"
    return "escape", "*** WRONG REASON: %s ***" % sorted(new)
