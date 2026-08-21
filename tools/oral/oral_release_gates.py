#!/usr/bin/env python3
"""
The Oral release gate registry -- the authoritative, committed record of the
full release sequence.

WHY THIS FILE EXISTS
--------------------

Batches E1 through E6 each ran a full release suite of 37-39 gates, and each
one drove it from a session-scratch script that was never committed. The gate
list itself therefore lived only in handoff prose and in conversation history.
That was the last reproducibility gap in the Oral toolchain: a new session could
read WHAT was run but had to rebuild the runner to run it.

RECONSTRUCTION -- how this list was derived from repository evidence
--------------------------------------------------------------------

`FINAL_ORAL_ENRICHMENT_BATCH_E1.md` section 17 enumerates its 37 gates by name.
Counting that list literally gives exactly 37, with the Node security tests
counted as THREE gates (`deploy_surface`, `regulatory_facts`, `link_integrity`).

`FINAL_ORAL_ENRICHMENT_BATCH_E5.md` also reports 37, but refers to a single
`node_security_tests` gate, and adds the two E5 gates. The arithmetic closes:

    E1  37
      - 2   Node collapsed from three gate records to one
      + 2   validate_batch_e5 + batch_e5_mutate
    E5  37
      + 2   validate_batch_e6 + batch_e6_mutate
    E6  39

So the E5-to-E6 increase is exactly one new batch's validator and mutator. The
39 below is E6's set, with Node as one gate.

DETERMINISM is deliberately NOT one of the 39. E1, E5 and E6 all report it in a
separate section, outside the gate count. It is registered here as a distinct
phase so the runner can drive it, and flagged `historical_39 = False` so the
historical count stays verifiable.

MAINTENANCE
-----------
Adding a batch adds exactly two gates: `validate_batch_<id>` and
`batch_<id>_mutate`. Nothing else in this file should need to change.

This module is DATA ONLY. Orchestration lives in `run_oral_release.py`.
"""

from __future__ import annotations

# --- parser kinds -----------------------------------------------------------
# How the runner decides PASS/FAIL for a gate. Exit code alone is never enough:
# validate_audit exits 0 while reporting a failed check, and a mutation harness
# prints the validator's own "FAIL:" lines as proof that a mutation was CAUGHT.
PARSER_EXIT = "exit"              # exit code is the whole story
PARSER_VALIDATOR = "validator"    # "<N> checks, <M> FAIL"
PARSER_MUTATION = "mutation"      # shared oral_mutation.parse_summary
PARSER_AUDIT = "audit"            # semantic counters vs a derived baseline
PARSER_HEALTH = "health"          # multiset finding diff, local vs ref
PARSER_CHECK = "check"            # generator --check: CURRENT or stale
PARSER_NODE = "node"              # node --test summary

# --- categories -------------------------------------------------------------
CAT_INDEX = "content-index"
CAT_UNIT = "unit-controls"
CAT_BATCH = "batch"
CAT_EXAMINER = "examiner"
CAT_CORPUS = "corpus"
CAT_SECURITY = "security"
CAT_HEALTH = "health"
CAT_DETERMINISM = "determinism"

# Files that release gates are known to rewrite. The runner snapshots these by
# byte content before any mutating gate and restores them by EXACT PATH from its
# own snapshot afterwards.
#
# It restores from a snapshot rather than from git, because
# `git checkout <ref> -- <file>` destroys uncommitted branch edits -- a trap that
# has already cost real work in this repo. The runner may only put back bytes it
# personally read.
GENERATED_ARTEFACTS = (
    "meoclass1/oral-intelligence/examiner-audit/VALIDATION_RESULTS.json",
    "meoclass1/oral-intelligence/examiner-audit/PHASE2_VALIDATION_RESULTS.json",
    "meoclass1/oral-intelligence/examiner-audit/ORAL_NOTES_IMPACT.md",
)

# Node 24 resolves `--test <dir>` as a MODULE to load and fails with
# "Cannot find module". E5's runner did exactly that and the gate exited 1 in
# 0.4s -- an invocation defect misread as a gate failure. Explicit files only.
# The runner expands this glob itself; it is never passed to a shell.
NODE_TEST_GLOB = "tools/security/*.test.mjs"

_ORAL = "tools/oral"


def _gate(gid, command, category, parser=PARSER_EXIT, mutates=False,
          timeout=900, always_run=True, depends_on=(), historical_39=True,
          note=""):
    return {
        "id": gid,
        "command": list(command),
        "category": category,
        "parser": parser,
        "mutates_worktree": mutates,
        "timeout": timeout,
        "always_run": always_run,
        "depends_on": list(depends_on),
        "historical_39": historical_39,
        "note": note,
    }


def _batch_pair(key, validator, mutator, mut_timeout, note=""):
    """A batch contributes exactly two gates: its validator, then its mutator.

    The mutator depends on the validator because a mutation suite proves the
    VALIDATOR catches corruption -- running it against a validator that is
    already failing proves nothing.
    """
    return [
        _gate("validate_%s" % key, ["python", "%s/%s" % (_ORAL, validator)],
              CAT_BATCH, PARSER_VALIDATOR, timeout=600, note=note),
        _gate("%s_mutate" % key, ["python", "%s/%s" % (_ORAL, mutator)],
              CAT_BATCH, PARSER_MUTATION, mutates=True, timeout=mut_timeout,
              depends_on=("validate_%s" % key,)),
    ]


GATES = (
    # ---- content index: is the manifest current, valid, and guarded? -------
    _gate("content_index_check",
          ["python", "%s/build_qb_content_index.py" % _ORAL, "--check"],
          CAT_INDEX, PARSER_CHECK, timeout=300,
          note="regeneration must be a no-op: 86 files / 721 questions"),
    _gate("content_index_validate",
          ["python", "%s/validate_qb_content_index.py" % _ORAL],
          CAT_INDEX, PARSER_VALIDATOR, timeout=300,
          depends_on=("content_index_check",)),
    _gate("content_index_mutate",
          ["python", "%s/mutate_qb_content_index.py" % _ORAL],
          CAT_INDEX, PARSER_MUTATION, mutates=True, timeout=1800,
          depends_on=("content_index_validate",)),

    # ---- corpus-wide unit controls ----------------------------------------
    _gate("qb_question_text", ["python", "%s/test_qb_question_text.py" % _ORAL],
          CAT_UNIT, PARSER_VALIDATOR, timeout=600),
    _gate("oral_controls", ["python", "%s/test_oral_controls.py" % _ORAL],
          CAT_UNIT, PARSER_VALIDATOR, timeout=600),
    _gate("notes_controls", ["python", "%s/test_notes_controls.py" % _ORAL],
          CAT_UNIT, PARSER_VALIDATOR, timeout=600),

    # ---- historical batches, oldest first ---------------------------------
    # Every historical guard runs on every release. A guard that stops running
    # is a guard that silently expires, and guard-expiry is a confirmed defect
    # class in this corpus. See PROPOSED_OPTIMISATIONS below.
    *_batch_pair("batch_a", "validate_batch_a.py", "mutate_batch_a.py", 900),
    *_batch_pair("batch_b", "validate_batch_b.py", "mutate_batch_b.py", 900),
    *_batch_pair("batch_c", "validate_batch_c.py", "mutate_batch_c.py", 900),
    *_batch_pair("batch_d", "validate_batch_d.py", "mutate_batch_d.py", 1200),
    *_batch_pair("gap0609", "validate_gap0609_exception.py",
                 "mutate_gap0609_exception.py", 900,
                 note="prints the key=value summary dialect"),
    *_batch_pair("batch_e1", "validate_batch_e1.py", "mutate_batch_e1.py", 2400),
    *_batch_pair("batch_e2", "validate_batch_e2.py", "mutate_batch_e2.py", 1800),
    *_batch_pair("batch_e3", "validate_batch_e3.py", "mutate_batch_e3.py", 1800),
    *_batch_pair("batch_e4", "validate_batch_e4.py", "mutate_batch_e4.py", 1200),
    *_batch_pair("batch_e5", "validate_batch_e5.py", "mutate_batch_e5.py", 2400),
    *_batch_pair("batch_e6", "validate_batch_e6.py", "mutate_batch_e6.py", 2400),

    # ---- examiner index ----------------------------------------------------
    _gate("examiner_check",
          ["python", "%s/build_examiner_index.py" % _ORAL, "--check"],
          CAT_EXAMINER, PARSER_CHECK, timeout=600,
          note="960 relationships / 7 examiners, zero delta"),
    _gate("validate_examiner_index",
          ["python", "%s/validate_examiner_index.py" % _ORAL],
          CAT_EXAMINER, PARSER_VALIDATOR, timeout=600,
          depends_on=("examiner_check",)),
    _gate("examiner_mutate", ["python", "%s/mutate_examiner_index.py" % _ORAL],
          CAT_EXAMINER, PARSER_MUTATION, mutates=True, timeout=1800,
          depends_on=("validate_examiner_index",)),
    _gate("test_examiner_check", ["python", "%s/test_examiner_check.py" % _ORAL],
          CAT_EXAMINER, PARSER_VALIDATOR, timeout=600,
          note="E1 called this the 37th gate: a superset of the 36 required"),

    # ---- CE Tip review -----------------------------------------------------
    _gate("validate_ce_tip_review",
          ["python", "%s/validate_ce_tip_review.py" % _ORAL],
          CAT_EXAMINER, PARSER_VALIDATOR, timeout=600),
    _gate("ce_tip_mutate", ["python", "%s/mutate_ce_tip_review.py" % _ORAL],
          CAT_EXAMINER, PARSER_MUTATION, mutates=True, timeout=1800,
          depends_on=("validate_ce_tip_review",)),

    # ---- phase 2 reconciliation -------------------------------------------
    _gate("validate_phase2", ["python", "%s/validate_phase2.py" % _ORAL],
          CAT_CORPUS, PARSER_VALIDATOR, timeout=900),
    _gate("phase2_mutate", ["python", "%s/mutate_phase2.py" % _ORAL],
          CAT_CORPUS, PARSER_MUTATION, mutates=True, timeout=3000,
          depends_on=("validate_phase2",)),

    # ---- audit: exits 0 while reporting a failed check ---------------------
    _gate("validate_audit", ["python", "%s/validate_audit.py" % _ORAL],
          CAT_CORPUS, PARSER_AUDIT, mutates=True, timeout=600,
          note="rewrites VALIDATION_RESULTS.json; classify semantically"),

    # ---- security / deploy surface ----------------------------------------
    _gate("node_security_tests", ["node", "--test", NODE_TEST_GLOB],
          CAT_SECURITY, PARSER_NODE, timeout=900,
          note="glob expanded by the runner; NEVER pass a directory to Node 24"),

    # ---- health: candidate LOCAL vs clean ref ------------------------------
    _gate("qb_health_check",
          ["python", "meoclass1/qb_health_check.py", "--source", "local",
           "--no-email"],
          CAT_HEALTH, PARSER_HEALTH, timeout=1800,
          note="baseline side is run by the runner as --source ref"),
)

# Determinism is a separate phase, outside the historical 39.
DETERMINISM_GATE = _gate(
    "determinism", ["python", "%s/check_determinism.py" % _ORAL],
    CAT_DETERMINISM, PARSER_EXIT, mutates=True, timeout=3600,
    historical_39=False,
    note="no argv parser; seeds 0/1/524287 are hardcoded in the tool. "
         "26 artefacts, 0 non-reproducible. Never probe it with --help.")

ALL_GATES = GATES + (DETERMINISM_GATE,)

# The baseline ref the health and audit comparisons are taken against.
BASELINE_REF = "origin/main"

# Recorded, NOT applied. Runtime is not a reason to stop running a guard.
PROPOSED_OPTIMISATIONS = """
Not implemented. Recorded for a future decision, with the risk stated.

1. Historical batch mutators (batch_a..batch_e6, 12 suites, ~200 mutations)
   dominate wall time. A follow-up batch cannot change a historical batch's
   cards, so in principle only that batch's own pair plus the corpus-wide gates
   need re-run.
   RISK: guard expiry is a confirmed defect class here -- guards pinning a
   corpus total or a digest set have passed vacuously at least four times. A
   historical mutator is exactly what detects that. Do not adopt this without a
   separate mechanism proving each skipped guard is still non-vacuous.

2. Read-only gates could run concurrently.
   RISK: several observe repo state. Serial is V1's contract.
"""


def gate_ids():
    return tuple(g["id"] for g in ALL_GATES)


def by_id(gate_id):
    for gate in ALL_GATES:
        if gate["id"] == gate_id:
            return gate
    raise KeyError("unknown gate: %r" % gate_id)


def historical_39():
    return tuple(g for g in ALL_GATES if g["historical_39"])
