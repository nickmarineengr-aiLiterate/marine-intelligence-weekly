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
import pathlib
import re
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
