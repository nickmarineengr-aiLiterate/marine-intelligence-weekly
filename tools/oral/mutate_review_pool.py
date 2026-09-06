#!/usr/bin/env python3
"""
Mutation suite for the Oral review-pool ACCEPTANCE CONTRACT.

`test_review_pool.py` reports 193 green controls. Green output is
indistinguishable from a suite that asserts nothing, and this particular suite
guards the one artefact in the toolchain that can REMOVE a card from a queue a
human believes is complete. So every proposition the contract rests on is
attacked here, and each mutation must trip the control that OWNS it.

WHY THIS SUITE EXISTS AT ALL
----------------------------
The defect it was written for (N-5) was not a wrong comparison. It was an
ABSENT one: `load_accepts` read six fields and silently discarded
`canonical_card_digest`, `repo_head_reviewed`, `review_id`, `residual_findings`
and `reopen_policy`. An acceptance record could therefore name the exact bytes
it had been taken over, and the generator would still exclude the card after
those bytes were rewritten. The record LOOKED byte-pinned; nothing read the pin.

A missing check is exactly the failure mode a mutation suite exists to find,
because a test written against an absent check passes for free. Mutations A and
C reproduce N-5 directly: C makes the loader drop the digest again, A makes the
comparison unconditional.

WHAT COUNTS AS A CATCH
----------------------
The control named in each row, and no other. Several of these mutations turn
half the suite red - a broken reopen rule shows up in five places - and
accepting "the suite went red" as evidence would prove only that something
somewhere noticed, which is what every one of these mutations already did
before the contract was hardened.

THE SUBJECT IS TOOLING SOURCE, NOT CANDIDATE CONTENT
----------------------------------------------------
Every watched path is under `tools/oral/`. This suite never touches
`meoclass1/`: the pages are the thing under review, and a harness that mutates
them to test a review queue has confused the queue with the corpus. Custody is
still byte-exact and verified by read-back, because a tooling file left mutated
is a wrong commit just as surely as a page would be.

  PYTHONIOENCODING=utf-8 python tools/oral/mutate_review_pool.py

Exit 0 when every mutation is killed, 1 on an escape, 2 if the control run is
not green to begin with.
"""

from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_content_mutation import run_suite, sub_in_file      # noqa: E402

LIB = HERE / "review_pool.py"
CLI = HERE / "build_review_pool.py"
ACCEPTS = HERE / "review_pool_accepts.json"
PROBE = "test_review_pool.py"


MUTATIONS = [
    # ---- the digest comparison itself -----------------------------------
    ("A", "disable the digest comparison (always report a match)",
     sub_in_file(LIB,
                 '"digest_match": current == accept["canonical_card_digest"],',
                 '"digest_match": True,'),
     "digest.changed_card_returns_to_pool"),

    ("B", "invert the digest comparison",
     sub_in_file(LIB,
                 '"digest_match": current == accept["canonical_card_digest"],',
                 '"digest_match": current != accept["canonical_card_digest"],'),
     "digest.unchanged_card_is_excluded"),

    ("C", "make the loader discard canonical_card_digest again -- N-5 exactly",
     sub_in_file(LIB, '"canonical_card_digest": digest,\n', ""),
     "contract.keeps_canonical_card_digest"),

    ("D", "treat a changed digest as still accepted (exclude regardless of "
          "reopen findings)",
     sub_in_file(LIB,
                 "if accept and excludes(accept) and not reopen:",
                 "if accept and excludes(accept):"),
     "digest.changed_card_returns_to_pool"),

    ("E", "downgrade a reopened card to IN_POOL, so the queue no longer says "
          "an acceptance was overtaken",
     sub_in_file(LIB, 'row["review_status"] = "REOPENED"',
                 'row["review_status"] = "IN_POOL"'),
     "digest.changed_status"),

    ("F", "treat an accepted card that has vanished from the corpus as still "
          "matching",
     sub_in_file(LIB, 'current = live_digests.get(accept["identity"])',
                 'current = live_digests.get(accept["identity"], '
                 'accept["canonical_card_digest"])'),
     "digest.absent_card_reopens"),

    # ---- reopen triggers must stay ADDITIVE ------------------------------
    ("G", "disable the explicit-risk reopen, leaving the digest as the only "
          "trigger",
     sub_in_file(LIB, "    if not accept or not accept.get(\"date\"):\n"
                      "        return []",
                 "    if True:\n        return []"),
     "digest.later_evidence_still_reopens_unchanged_card"),

    ("H", "reopen on repository-head movement, so every unrelated commit "
          "invalidates every acceptance",
     sub_in_file(LIB, 'if state and not state["digest_match"]:',
                 'if state and (not state["digest_match"]'
                 ' or state["repo_head_reviewed"] != "cba1a9b"):'),
     "digest.repo_head_movement_alone_does_not_reopen"),

    # ---- fail-loud validation --------------------------------------------
    ("I", "accept a malformed canonical_card_digest",
     sub_in_file(LIB, "        if not _is_digest(digest):",
                 "        if False:"),
     "contract.digest_short_is_loud"),

    ("J", "accept a repo_head_reviewed that is not a git object name",
     sub_in_file(LIB, "        if not _is_commitish(head):", "        if False:"),
     "contract.bad_repo_head_is_loud"),

    ("K", "silently coerce a retired schema/1 file instead of refusing it",
     sub_in_file(LIB, "    if schema in RETIRED_ACCEPTS_SCHEMAS:",
                 "    if False:"),
     "contract.schema1_refused"),

    ("L", "let an unrecognised governance-looking field through",
     sub_in_file(LIB, "        unknown = sorted(set(entry) - ACCEPT_FIELDS)",
                 "        unknown = []"),
     "contract.unknown_field_is_loud"),

    ("M", "stop validating residual_findings, so an unreadable residual counts "
          "as an explicitly recorded one",
     sub_in_file(LIB, "    if value is None or not isinstance(value, list):",
                 "    if False:"),
     "contract.residual_not_a_list_is_loud"),

    ("N", "exclude on a WHOLE_CARD accept even when no live digests were "
          "supplied -- an unchecked exclusion instead of a refusal",
     sub_in_file(LIB, "    if live_digests is None:\n        raise PoolError(",
                 "    if False:\n        raise PoolError("),
     "digest.absent_live_digests_is_loud"),

    # ---- the two rules that predate this contract and must survive it ----
    ("O", "give a prose hint exclusion authority by dropping the hinted card "
          "out of the pool list",
     sub_in_file(LIB, "            unknown.append(row)" + chr(10),
                 "            unknown.append(row)" + chr(10)
                 + "            continue" + chr(10)),
     "digest.prose_hint_still_cannot_exclude"),

    ("P", "reimplement the card digest locally instead of reusing the "
          "correction toolchain's",
     sub_in_file(LIB,
                 "from validate_batch_h_series import card_digests as "
                 "canonical_card_digests  # noqa: E402",
                 "canonical_card_digests = lambda text: {}  # noqa: E731"),
     "reuse.same_function_object"),

    # ---- the identity guards that predate the contract -------------------
    ("Q", "allow two active accepts for one card, so 'which one governs' has "
          "no answer",
     sub_in_file(LIB, "        if ident in out:", "        if False:"),
     "contract.duplicate_accept_is_loud"),

    ("R", "allow an accept pinned to an identity no evidence names, which would "
          "silently stop matching the day the spelling moved",
     sub_in_file(LIB, "        if known_identities is not None and ident not in "
                      "known_identities:",
                 "        if False:"),
     "accepts.unstable_identity_is_loud"),

    # ---- review priority is not defect severity --------------------------
    # A relabelling is the easiest kind of change to get silently wrong: the
    # old label can come back, the new label can be translated back at the
    # render boundary, or the ranking can move while attention is on the names.
    ("S", "restore the old P-series queue labels, which read as MIW defect "
          "severities",
     sub_in_file(LIB, '((70, "R1"), (45, "R2"), (25, "R3"), (0, "R4"))',
                 '((70, "P1"), (45, "P2"), (25, "P3"), (0, "P4"))'),
     "band.vocabulary_is_r_series"),

    ("T", "render R-bands back as P-bands in the reviewer-facing report, so "
          "the payload is clean and the document a human reads is not",
     sub_in_file(LIB,
                 'out.append("| %s | %d |" % (band, '
                 's["by_review_priority"][band]))',
                 'out.append("| %s | %d |" % (band.replace("R", "P"), '
                 's["by_review_priority"][band]))'),
     "band.markdown_table_is_r"),

    ("U", "move the ranking order while relabelling",
     sub_in_file(LIB,
                 'cards.sort(key=lambda c: (-c["risk_score"], c["file"], '
                 'c["anchor"]))',
                 'cards.sort(key=lambda c: (c["risk_score"], c["file"], '
                 'c["anchor"]))'),
     "band.ranking_unchanged_by_rename"),

    ("V", "shift a band threshold under cover of the rename",
     sub_in_file(LIB, '((70, "R1"), (45, "R2")', '((60, "R1"), (45, "R2")'),
     "band.boundary_69_is_R2"),

    ("W", "re-alias the retired field name alongside the new one, so a reader "
          "can keep reading the old meaning",
     sub_in_file(LIB, '"review_priority": review_priority(score),',
                 '"review_priority": review_priority(score),' + chr(10)
                 + '            "recommended_tranche_priority": '
                   'review_priority(score),'),
     "band.old_field_removed"),

    ("X", "drop the legend that tells the reader R is not a defect severity",
     sub_in_file(LIB, "**not a content-defect severity**", "**a priority**"),
     "band.markdown_says_r_is_not_severity"),
]

WATCHED = [LIB, CLI, ACCEPTS]

if __name__ == "__main__":
    raise SystemExit(run_suite(
        "mutation suite: Oral review-pool acceptance contract + priority semantics",
        PROBE, MUTATIONS, WATCHED))
