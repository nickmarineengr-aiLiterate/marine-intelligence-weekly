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

TWO FLAGS, NOT ONE. `historical_39` records whether a gate was part of the suite
E6 actually ran -- it is provenance, and it is what keeps the count of 39
checkable forever. `separate_phase` records whether the runner holds a gate back
until it is asked for explicitly. Determinism is both (not historical, held
back). The correction gates are neither historical (they postdate E6) nor held
back (a release must not ship an unverified correction), which is exactly why
the two flags cannot stay conflated.

MAINTENANCE
-----------
Adding a batch adds exactly two gates: `validate_batch_<id>` and
`batch_<id>_mutate`. Nothing else in this file should need to change.

Adding a CORRECTION adds no AUTHORISATION gates at all. `validate_corrections`
and `corrections_mutate` iterate every `correction_*_manifest.json` on disk, so
a new correction record is picked up without touching this registry or the
runner. If you ever find yourself naming a specific correction *in the
delegation path*, the delegation model has been bypassed.

A correction may still add its own CONTENT gates, and CORR-LSA-LIFEBOAT-
VENTILATION-20260822 is the first that does. The two families answer different
questions and neither subsumes the other:

    validate_corrections          are these bytes the ones we authorised?
    validate_correction_<id>      is what we authorised actually right?

The generic gate pins a digest, and a digest pin is perfectly happy with wrong
text -- it pins whatever it is given. Where a correction turns on a regulatory
proposition that a later well-meaning edit could quietly drop (here: that
MSC.535(107) defines "installed on or after 1 January 2029" in two limbs, and
that the second limb reaches existing ships), that proposition needs a named
check of its own, exactly as a production batch gets `validate_batch_<id>`.
Content gates are per-correction by nature and naming one here is correct;
naming one inside the delegation path still is not.

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
CAT_CORRECTION = "correction"
CAT_AUTHORISATION = "authorisation"
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

# Files a mutating gate is expected to leave BYTE-IDENTICAL. A mutation harness
# injects corruption and puts it back; the tree it hands on is part of its
# contract, not a side effect.
#
# Six harnesses restore only on the happy path -- mutate_batch_a/b/c/d,
# mutate_ce_tip_review and mutate_qb_content_index have no `finally`. When
# `mutate_batch_a` died between injecting an editorial marker and restoring it,
# it left that marker in a real product page. Which page, and whether anything
# was left at all, depended on which page the crashing mutation had picked, and
# PYTHONHASHSEED is unpinned -- so it was luck.
#
# The runner therefore snapshots these too and puts back exactly the bytes it
# read, by exact path, the same discipline ArtefactGuard already applies. Unlike
# GENERATED_ARTEFACTS -- which mutating gates legitimately rewrite -- a
# difference here is a DEFECT and the gate that caused it fails. A harness that
# does not hand back the tree has not proved anything about the tree.
PRODUCT_GUARDED_GLOBS = (
    "meoclass1/QB*.html",
    "meoclass1/SQ/*.html",
    "tools/oral/*manifest*.json",
)

# Node 24 resolves `--test <dir>` as a MODULE to load and fails with
# "Cannot find module". E5's runner did exactly that and the gate exited 1 in
# 0.4s -- an invocation defect misread as a gate failure. Explicit files only.
# The runner expands this glob itself; it is never passed to a shell.
NODE_TEST_GLOB = "tools/security/*.test.mjs"

_ORAL = "tools/oral"


def _gate(gid, command, category, parser=PARSER_EXIT, mutates=False,
          timeout=900, always_run=True, depends_on=(), historical_39=True,
          separate_phase=False, baseline_derivable=False, note=""):
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
        "separate_phase": separate_phase,
        "baseline_derivable": baseline_derivable,
        "note": note,
    }


# SIZING A MUTATION TIMEOUT
# -------------------------
# A mutation harness re-runs its whole validator once per mutation, plus a
# control run before and a restore check after. So its wall time is very close
# to
#           (mutations + 2) x that validator's own runtime
#
# and a timeout set from a stopwatch on the day is a guess that expires. E5's
# 2400s was comfortable when it was written and is not now: its validator takes
# 103.7s and the suite has 25 mutations, so it needs ~2800s and was killed at
# exactly 2400.1s. The suite had proved nothing, and the kill landed inside a
# mutation, leaving a mutated product page behind.
#
# When adding or re-timing a pair, measure the VALIDATOR (`--gate validate_...`),
# multiply by mutations + 2, and double it. Do not tune a timeout down to what
# was observed once; the validators get slower as the authorisation surface
# grows, because every one of them scans it.
def _batch_pair(key, validator, mutator, mut_timeout, note="",
                baseline_derivable=False, historical_39=True):
    """A batch contributes exactly two gates: its validator, then its mutator.

    The mutator depends on the validator because a mutation suite proves the
    VALIDATOR catches corruption -- running it against a validator that is
    already failing proves nothing.

    ``historical_39`` defaults True because every batch that existed when the
    count of 39 was fixed is in it.  A batch registered AFTER E6 must pass
    False, or it silently inflates a number that exists to be checkable
    forever.
    """
    return [
        _gate("validate_%s" % key, ["python", "%s/%s" % (_ORAL, validator)],
              CAT_BATCH, PARSER_VALIDATOR, timeout=600, note=note,
              historical_39=historical_39,
              baseline_derivable=baseline_derivable),
        _gate("%s_mutate" % key, ["python", "%s/%s" % (_ORAL, mutator)],
              CAT_BATCH, PARSER_MUTATION, mutates=True, timeout=mut_timeout,
              historical_39=historical_39,
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

    # ---- study spine: a new oral question must reach a topic ---------------
    # The integration point tools/study/SKILL.md described as a TODO. A newly
    # authored oral question lands in qb_content_index.json, so the mapping
    # store built from it goes stale; --check fails, and the author has to map
    # the question (or route it to the review queue) before the release can
    # pass. Without this an oral question could ship ACCIDENTALLY_UNMAPPED and
    # simply never appear in any study surface.
    #
    # Neither gate touches oral product content: they read the index and write
    # only under docs/study/, so they cannot mutate a QB page.
    _gate("study_mapping_check",
          ["python", "tools/study/build_study_mappings.py", "--check"],
          CAT_INDEX, PARSER_CHECK, timeout=600, historical_39=False,
          depends_on=("content_index_check",),
          note="every canonical oral question must already carry a governed mapping"),
    _gate("study_spine_validate",
          ["python", "tools/study/validate_study_spine.py"],
          CAT_INDEX, PARSER_VALIDATOR, timeout=600, historical_39=False,
          depends_on=("study_mapping_check",),
          note="official syllabus, coverage and Topic 01 references must resolve"),

    # ---- study surfaces must regenerate from the corpus that just changed --
    # A new oral question reaches a topic (above) but would still be invisible
    # if the rendered surfaces were left stale. Both gates are --check only:
    # they compute the page and compare bytes, so a release fails rather than
    # silently shipping a roadmap that disagrees with the corpus behind it.
    #
    # The public gate additionally re-runs assert_public_safe() over the
    # rendered HTML, so a newly authored question that would drag a gated link,
    # an answer marker or an over-wide evidence claim onto the PUBLIC page
    # fails the release instead of being published.
    _gate("study_pages_check",
          ["python", "tools/study/build_topic_pages.py", "--check"],
          CAT_INDEX, PARSER_CHECK, timeout=600, historical_39=False,
          depends_on=("study_spine_validate",),
          note="gated study surfaces must match the corpus they are built from"),
    _gate("study_public_roadmap_check",
          ["python", "tools/study/build_public_study_roadmap.py", "--check"],
          CAT_INDEX, PARSER_CHECK, timeout=600, historical_39=False,
          depends_on=("study_spine_validate",),
          note="public roadmap must be current AND pass every public-safety guard"),

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
    # 25 mutations x a 103.7s validator = ~2800s needed. The old 2400s killed
    # it at 2400.1s. Sized by the rule above, with headroom.
    *_batch_pair("batch_e5", "validate_batch_e5.py", "mutate_batch_e5.py", 6000),
    # 33 mutations, and its control additionally derives a baseline from a
    # temporary worktree because of the evidence debt below.
    *_batch_pair("batch_e6", "validate_batch_e6.py", "mutate_batch_e6.py", 4800,
                 baseline_derivable=True,
                 note="carries the line_endings_homogeneous_per_file evidence "
                      "debt; its baseline is DERIVED, never declared"),

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

    # ---- post-release corrections -----------------------------------------
    # These postdate E6, so they are not part of the historical 39 -- but they
    # are NOT held back either. A correction delegates authority away from every
    # historical batch guard; the release that carries it must prove the
    # delegation is still honoured, or the guards were simply switched off.
    _gate("validate_corrections",
          ["python", "%s/validate_corrections.py" % _ORAL],
          CAT_CORRECTION, PARSER_VALIDATOR, timeout=900, historical_39=False,
          note="pins the post-correction state the batch guards now delegate"),
    _gate("corrections_mutate",
          ["python", "%s/mutate_corrections.py" % _ORAL],
          CAT_CORRECTION, PARSER_MUTATION, mutates=True, timeout=2400,
          historical_39=False, depends_on=("validate_corrections",),
          note="proves the delegation is an exemption, not a suppression"),

    # Content gates for CORR-LSA-LIFEBOAT-VENTILATION-20260822. See the
    # MAINTENANCE note: these assert the regulatory substance the digest pin
    # cannot, and are per-correction by nature.
    _gate("validate_correction_lsavent",
          ["python", "%s/validate_correction_lsavent.py" % _ORAL],
          CAT_CORRECTION, PARSER_VALIDATOR, timeout=600, historical_39=False,
          note="asserts the two-limb MSC.535(107) application rule the pin cannot"),
    _gate("correction_lsavent_mutate",
          ["python", "%s/mutate_correction_lsavent.py" % _ORAL],
          CAT_CORRECTION, PARSER_MUTATION, mutates=True, timeout=1800,
          historical_39=False, depends_on=("validate_correction_lsavent",),
          note="each mutation must trip its OWN named check, never the digest pin"),

    # ---- follow-up authorisation register ---------------------------------
    # Postdates E6, so outside the historical 39, and not held back either.
    #
    # This is NOT a product gate: the register authorises no shipped bytes and
    # a red register never means the product is unsafe. It earns a place in the
    # release because its validator reads the LIVE corpus. Every one of the 35
    # actions pins a parent card's anchor and question text, so a release that
    # moves or rewords one of those cards turns this gate red at the moment the
    # drift is introduced -- not months later when a follow-up batch tries to
    # author against a parent that no longer says what the register recorded.
    #
    # It is a standing detector for release-caused target drift, which is
    # exactly the failure the register exists to prevent.
    _gate("validate_followup_register",
          ["python", "%s/validate_followup_register.py" % _ORAL],
          CAT_AUTHORISATION, PARSER_VALIDATOR, timeout=600, historical_39=False,
          note="re-derives the register from pinned blobs and re-checks all 35 "
               "parent pins against the live corpus"),
    _gate("followup_register_mutate",
          ["python", "%s/mutate_followup_register.py" % _ORAL],
          CAT_AUTHORISATION, PARSER_MUTATION, mutates=True, timeout=1200,
          historical_39=False, depends_on=("validate_followup_register",),
          note="each mutation must trip its OWN named check, not merely the "
               "byte-currency check that fires on every edit"),

    # ---- follow-up production batches --------------------------------------
    # F1 is the first batch derived from the follow-up register rather than the
    # enrichment consolidation. It postdates E6, so historical_39 is False: the
    # count of 39 records which gates E6 actually ran and must stay checkable.
    #
    # Its pair is registered here, AFTER validate_followup_register, because a
    # follow-up batch is only meaningful if the register it was derived from is
    # itself still valid against the live corpus.
    *_batch_pair("batch_f1", "validate_batch_f1.py", "mutate_batch_f1.py", 1800,
                 historical_39=False,
                 note="follow-up batch: resolves each card's followup_id in the "
                      "register and re-checks parent, anchor, q-text and "
                      "relationship edge against it"),

    # F1b implements the one action F1 held (FUP-006) and is the FIRST
    # production use of historical digest supersession. Registered immediately
    # after F1, because its whole reason for existing is to discharge a hold F1
    # declared, and its validator asserts that F1's hold record is still there.
    *_batch_pair("batch_f1b", "validate_batch_f1b.py", "mutate_batch_f1b.py",
                 1800, historical_39=False,
                 note="follow-up batch: discharges F1's HELD_GOVERNANCE action "
                      "through a declared supersession chain, and asserts the "
                      "historical predecessor pin is preserved rather than "
                      "rebaselined"),

    # ---- current-intake production batches ---------------------------------
    # G1 is the first batch authorised by a CURRENT-intake adjudication record
    # rather than by the historical 788 disposition or the enrichment
    # consolidation. It postdates E6, so historical_39 is False.
    #
    # It is registered AFTER the follow-up register pair because G1 enriches
    # three cards that the register also pins: if a G1 edit moved a pinned
    # parent, the register gate must go red first, so the cause is reported
    # before the consequence.
    *_batch_pair("batch_g1", "validate_batch_g1.py", "mutate_batch_g1.py",
                 1800, historical_39=False,
                 note="fresh-intake batch: every card must trace to an August "
                      "occurrence a candidate actually reported, an enrichment "
                      "must target the card the adjudication named, and no card "
                      "may name an examiner the evidence does not support"),

    *_batch_pair("batch_g2", "validate_batch_g2.py", "mutate_batch_g2.py",
                 1800, historical_39=False,
                 note="second fresh-intake batch: same contract as G1, reused rather "
                      "than copied. Adds the checks S005 made necessary - a raw "
                      "carrier file must not reach a tracked or deployed surface, and "
                      "neither QB projection may drift from the governed card count"),

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
    historical_39=False, separate_phase=True,
    note="no argv parser; seeds 0/1/524287 are hardcoded in the tool. "
         "26 artefacts, 0 non-reproducible. Never probe it with --help.")

ALL_GATES = GATES + (DETERMINISM_GATE,)

# The baseline ref the health, audit and validator-baseline comparisons are
# taken against.
BASELINE_REF = "origin/main"

# DERIVED BASELINES, NEVER DECLARED ONES
# --------------------------------------
# `validate_batch_e6` fails `line_endings_homogeneous_per_file` on a clean
# checkout of the very commit it certified: its manifest pinned a
# pre-normalisation CRLF working copy while `.gitattributes` pins *.html to LF.
# The product bytes are correct; the recorded evidence is not reproducible.
#
# That failure is real and must not be reported as PASS. It is also not a
# regression, and blocking every future release on it would make the runner's
# verdict useless.
#
# So a gate may be marked `baseline_derivable`. When such a gate FAILS, the
# runner re-runs the SAME validator on a clean worktree of BASELINE_REF and
# compares the failing check names. Identical set -> PRE_EXISTING_BASELINE,
# reported as its own status with the checks named. Any difference -> FAIL.
#
# The baseline is derived, never hardcoded, for the reason `classify_audit`
# already gives: a hardcoded baseline silently absorbs the next real
# regression. A second failing check appearing in E6 tomorrow still fails.

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
