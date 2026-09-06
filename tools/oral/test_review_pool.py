"""Controls for the Oral QB review-pool generator.

These are load-bearing assertions, not smoke tests. Each pins a rule that, if
broken, produces a FALSE GREEN - a card silently absent from a review queue that
a reviewer trusts to be complete.

  PYTHONIOENCODING=utf-8 python tools/oral/test_review_pool.py

Exit 0 when every control holds, 1 otherwise. Portability: repo-relative, no
drive letters, no external inputs.
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import review_pool as RP        # noqa: E402

FAILURES = []
CHECKS = [0]


def ok(name, condition, detail=""):
    CHECKS[0] += 1
    if not condition:
        FAILURES.append("%s %s" % (name, ("- " + detail) if detail else ""))


def raises(name, fn, want):
    """Fail-loud control: fn must raise PoolError mentioning `want`."""
    CHECKS[0] += 1
    try:
        fn()
    except RP.PoolError as exc:
        if want.lower() not in str(exc).lower():
            FAILURES.append("%s - raised PoolError but not about %r: %s"
                            % (name, want, exc))
        return
    except Exception as exc:                      # noqa: BLE001
        FAILURES.append("%s - raised %s, not PoolError: %s"
                        % (name, type(exc).__name__, exc))
        return
    FAILURES.append("%s - did not raise; a malformed input passed silently" % name)


# --- 1. Canonical card identity -------------------------------------------
# Batch manifests carry a bare `file` ("QB7_I.html"); correction manifests carry
# both `file` and a repo-relative `path`. Joining on the raw fields makes ONE
# card enter the pool under TWO identities.

def control_identity():
    ok("identity.path_wins",
       RP.card_identity({"file": "QB4_H.html", "path": "meoclass1/QB4_H.html",
                         "anchor": "q2"}) == ("meoclass1/QB4_H.html", "q2"))
    ok("identity.bare_file_is_qualified",
       RP.card_identity({"file": "QB7_I.html", "anchor": "q10"})
       == ("meoclass1/QB7_I.html", "q10"))
    ok("identity.backslashes_normalised",
       RP.card_identity({"file": "QB4_H.html", "path": "meoclass1" + chr(92) + "QB4_H.html",
                         "anchor": "q2"}) == ("meoclass1/QB4_H.html", "q2"))
    ok("identity.two_spellings_are_one_card",
       RP.card_identity({"file": "QB4_H.html", "anchor": "q2"})
       == RP.card_identity({"file": "QB4_H.html", "path": "meoclass1/QB4_H.html",
                            "anchor": "q2"}),
       "bare-file and path spellings must collapse to one identity")

    raises("identity.missing_anchor_is_loud",
           lambda: RP.card_identity({"file": "QB4_H.html"}), "anchor")
    raises("identity.missing_file_is_loud",
           lambda: RP.card_identity({"anchor": "q2"}), "file")
    raises("identity.blank_anchor_is_loud",
           lambda: RP.card_identity({"file": "QB4_H.html", "anchor": "  "}), "anchor")


# --- 2. The adjudication file is the ONLY exclusion authority ---------------
# It is hand-maintained, so every way it can be wrong must be loud. A silently
# ignored malformed entry re-admits the false green by the back door.

KNOWN = {("meoclass1/QB4_H.html", "q2"), ("meoclass1/QB7_I.html", "q10")}


def _accepts(tmp, payload):
    f = tmp / "accepts.json"
    f.write_text(json.dumps(payload), encoding="utf-8")
    return f


ACCEPTED_DIGEST = "a" * 64          # the bytes the reviewer actually read
MOVED_DIGEST = "b" * 64             # what the card canonicalises to now


def _entry(**over):
    """A COMPLETE schema/2 acceptance record.

    Every field is present because schema/2 requires every field: an accept is
    the one artefact in this toolchain that can remove a card from a queue a
    human believes is complete, so it may not be half-filled.
    """
    base = {"file": "QB4_H.html", "anchor": "q2",
            "accept_scope": "WHOLE_CARD",
            "evidence": "GPT_REVIEW_HIGHRISK_TRANCHE1_20260904.md section 5",
            "adjudicated_by": "nixon",
            "date": "2026-09-05",
            "review_id": "TRANCHE-4-ACCEPT-001",
            "repo_head_reviewed": "cba1a9b",
            "canonical_card_digest": ACCEPTED_DIGEST,
            "residual_findings": [],
            "reopen_policy": "reopens on any candidate-facing byte change"}
    base.update(over)
    return base


def control_accepts():
    with tempfile.TemporaryDirectory() as d:
        tmp = pathlib.Path(d)

        good = RP.load_accepts(_accepts(tmp, {"schema": RP.ACCEPTS_SCHEMA,
                                              "accepts": [_entry()]}), KNOWN)
        ok("accepts.whole_card_loads",
           list(good) == [("meoclass1/QB4_H.html", "q2")])
        ok("accepts.entry_retains_evidence",
           good[("meoclass1/QB4_H.html", "q2")]["evidence"].startswith("GPT_REVIEW"))

        ok("accepts.absent_file_is_empty_not_fatal",
           RP.load_accepts(tmp / "nope.json", KNOWN) == {},
           "no adjudications yet is a legitimate state - every card stays in")

        # Narrow scope is recorded but MUST NOT carry exclusion authority.
        narrow = RP.load_accepts(
            _accepts(tmp, {"schema": RP.ACCEPTS_SCHEMA,
                           "accepts": [_entry(accept_scope="NARROW_SCOPE")]}), KNOWN)
        ok("accepts.narrow_scope_does_not_exclude",
           RP.excludes(narrow[("meoclass1/QB4_H.html", "q2")]) is False,
           "partial acceptance must never become whole-card acceptance")
        ok("accepts.whole_card_does_exclude",
           RP.excludes(good[("meoclass1/QB4_H.html", "q2")]) is True)

        raises("accepts.duplicate_identity_is_loud",
               lambda: RP.load_accepts(
                   _accepts(tmp, {"schema": RP.ACCEPTS_SCHEMA,
                                  "accepts": [_entry(), _entry(evidence="other")]}),
                   KNOWN), "duplicate")
        raises("accepts.unknown_scope_is_loud",
               lambda: RP.load_accepts(
                   _accepts(tmp, {"schema": RP.ACCEPTS_SCHEMA,
                                  "accepts": [_entry(accept_scope="LOOKS_FINE")]}),
                   KNOWN), "accept_scope")
        raises("accepts.missing_evidence_is_loud",
               lambda: RP.load_accepts(
                   _accepts(tmp, {"schema": RP.ACCEPTS_SCHEMA,
                                  "accepts": [_entry(evidence="  ")]}),
                   KNOWN), "evidence")
        raises("accepts.unstable_identity_is_loud",
               lambda: RP.load_accepts(
                   _accepts(tmp, {"schema": RP.ACCEPTS_SCHEMA,
                                  "accepts": [_entry(file="QB9_Z.html", anchor="q99")]}),
                   KNOWN), "not present")
        raises("accepts.wrong_schema_is_loud",
               lambda: RP.load_accepts(
                   _accepts(tmp, {"schema": "something-else",
                                  "accepts": [_entry()]}), KNOWN), "schema")
        raises("accepts.malformed_json_is_loud",
               lambda: RP.load_accepts(
                   _write(tmp / "bad.json", "{not json"), KNOWN), "parse")


def _write(path, text):
    path.write_text(text, encoding="utf-8")
    return path


# --- 2b. The acceptance CONTRACT (schema/2) --------------------------------
# The defect these controls close, found after Tranche 4 and before the first
# real accept was ever written:
#
#   The loader read six fields and silently discarded canonical_card_digest,
#   repo_head_reviewed, review_id, residual_findings and reopen_policy - so an
#   acceptance record could name the exact bytes it had read and the generator
#   would still exclude the card after those bytes had been rewritten. The
#   record LOOKED byte-pinned. Nothing read the pin.
#
# The rule now in code: an acceptance covers BYTES, not a card name. When the
# canonical digest of the live card differs from the digest the acceptance was
# taken over, the acceptance no longer covers what is on the page, and the card
# returns to the pool.

def _accept_record(**over):
    """The in-memory shape `load_accepts` returns, for build_pool fixtures."""
    rec = {"identity": Q2, "accept_scope": "WHOLE_CARD",
           "evidence": "tranche4 s3", "adjudicated_by": "nixon",
           "date": "2026-09-05", "review_id": "TRANCHE-4-ACCEPT-001",
           "repo_head_reviewed": "cba1a9b",
           "canonical_card_digest": ACCEPTED_DIGEST,
           "residual_findings": [], "reopen_policy": "any byte change"}
    rec.update(over)
    return rec


def _one_correction(date="2026-09-01"):
    return [("corr_a.json", _corr("CORR-A", [dict(NARROW)], date=date))]


def control_acceptance_contract():
    with tempfile.TemporaryDirectory() as d:
        tmp = pathlib.Path(d)

        # --- the contract: recognised governance fields SURVIVE the loader ---
        rec = RP.load_accepts(_accepts(tmp, {"schema": RP.ACCEPTS_SCHEMA,
                                             "accepts": [_entry()]}), KNOWN)[Q2]
        for field in ("canonical_card_digest", "repo_head_reviewed", "review_id",
                      "residual_findings", "reopen_policy"):
            ok("contract.keeps_%s" % field, field in rec,
               "schema/2 field silently discarded by the loader - the N-5 defect")
        ok("contract.digest_value_preserved",
           rec.get("canonical_card_digest") == ACCEPTED_DIGEST)

        # --- F. schema/1 is not an enforceable whole-card accept -------------
        ok("contract.schema1_refusal_says_what_to_do",
           "re-adjudicate" in RP.RETIRED_ACCEPTS_SCHEMAS[
               "miw-oral-review-pool-accepts/1"].lower(),
           "a version-mismatch message invites editing the version string - "
           "the one repair that reinstates the defect")
        raises("contract.schema1_refused",
               lambda: RP.load_accepts(
                   _accepts(tmp, {"schema": "miw-oral-review-pool-accepts/1",
                                  "accepts": [_entry()]}), KNOWN),
               "retired")

        # --- E/F. digest validation is fail-loud -----------------------------
        for label, value in (("missing", None), ("short", "abc"),
                             ("uppercase", "A" * 64), ("non_hex", "z" * 64),
                             ("not_a_string", 12345), ("empty", "")):
            entry = _entry()
            if value is None:
                del entry["canonical_card_digest"]
            else:
                entry["canonical_card_digest"] = value
            raises("contract.digest_%s_is_loud" % label,
                   lambda e=entry: RP.load_accepts(
                       _accepts(tmp, {"schema": RP.ACCEPTS_SCHEMA,
                                      "accepts": [e]}), KNOWN),
                   "canonical_card_digest")

        # --- every other required field is required --------------------------
        for field in ("evidence", "adjudicated_by", "date", "review_id",
                      "repo_head_reviewed", "reopen_policy"):
            entry = _entry()
            del entry[field]
            raises("contract.missing_%s_is_loud" % field,
                   lambda e=entry: RP.load_accepts(
                       _accepts(tmp, {"schema": RP.ACCEPTS_SCHEMA,
                                      "accepts": [e]}), KNOWN),
                   field)

        raises("contract.bad_repo_head_is_loud",
               lambda: RP.load_accepts(
                   _accepts(tmp, {"schema": RP.ACCEPTS_SCHEMA,
                                  "accepts": [_entry(repo_head_reviewed="HEAD~1")]}),
                   KNOWN), "repo_head_reviewed")

        # --- an unknown field is a refusal, not a shrug ----------------------
        raises("contract.unknown_field_is_loud",
               lambda: RP.load_accepts(
                   _accepts(tmp, {"schema": RP.ACCEPTS_SCHEMA,
                                  "accepts": [_entry(looks_official="yes")]}),
                   KNOWN), "looks_official")

        # --- 10. residual findings: shape validated, severity NOT adjudicated -
        good = RP.load_accepts(
            _accepts(tmp, {"schema": RP.ACCEPTS_SCHEMA,
                           "accepts": [_entry(residual_findings=[
                               {"severity": "P3", "note": "phrasing only"}])]}),
            KNOWN)[Q2]
        ok("contract.residual_findings_preserved",
           good.get("residual_findings") == [{"severity": "P3",
                                          "note": "phrasing only"}])
        ok("contract.residual_findings_may_be_empty",
           rec.get("residual_findings") == [])
        for label, value in (("not_a_list", {}),
                             ("not_a_list_object", {"severity": "P3"}),
                             ("item_not_object", ["P3"]),
                             ("item_missing_note", [{"severity": "P3"}]),
                             ("item_missing_severity", [{"note": "x"}])):
            raises("contract.residual_%s_is_loud" % label,
                   lambda v=value: RP.load_accepts(
                       _accepts(tmp, {"schema": RP.ACCEPTS_SCHEMA,
                                      "accepts": [_entry(residual_findings=v)]}),
                       KNOWN), "residual_findings")
        # A P1 residual is a contradiction a HUMAN must resolve, not the
        # generator: section 10 says the generator does not adjudicate severity.
        ok("contract.severity_value_not_adjudicated",
           RP.load_accepts(
               _accepts(tmp, {"schema": RP.ACCEPTS_SCHEMA,
                              "accepts": [_entry(residual_findings=[
                                  {"severity": "P1", "note": "left open"}])]}),
               KNOWN)[Q2].get("residual_findings", [{}])[0].get("severity") == "P1",
           "the generator must record severity, never rule on it")

        # --- G. a duplicate accept is ambiguous, not additive ----------------
        raises("contract.duplicate_accept_is_loud",
               lambda: RP.load_accepts(
                   _accepts(tmp, {"schema": RP.ACCEPTS_SCHEMA,
                                  "accepts": [_entry(),
                                              _entry(review_id="TRANCHE-4-ACCEPT-002")]}),
                   KNOWN), "duplicate")

    docs = _one_correction()
    live_same = {Q2: ACCEPTED_DIGEST}
    live_moved = {Q2: MOVED_DIGEST}

    # --- A. unchanged bytes: the acceptance still covers the card ------------
    pool = RP.build_pool(docs, accepts={Q2: _accept_record()},
                         live_digests=live_same)
    ok("digest.unchanged_card_is_excluded",
       Q2 not in {tuple(c["identity"]) for c in pool["cards"]})
    row = pool["excluded"][0]
    ok("digest.unchanged_status", row["review_status"] == "EXPLICITLY_ACCEPTED")
    ok("digest.unchanged_records_match",
       row["digest_state"]["digest_match"] is True)
    ok("digest.unchanged_records_both_digests",
       (row["digest_state"]["accepted_digest"],
        row["digest_state"]["current_digest"]) == (ACCEPTED_DIGEST, ACCEPTED_DIGEST))

    # --- B. changed bytes: the acceptance no longer covers the card ---------
    moved = RP.build_pool(docs, accepts={Q2: _accept_record()},
                          live_digests=live_moved)
    mby = {tuple(c["identity"]): c for c in moved["cards"]}
    ok("digest.changed_card_returns_to_pool", Q2 in mby,
       "a whole-card accept over bytes that have since moved must not exclude")
    ok("digest.changed_status", mby[Q2]["review_status"] == "REOPENED")
    ok("digest.changed_not_downgraded_to_in_pool",
       mby[Q2]["review_status"] != "IN_POOL",
       "a reopened accept must say so, not quietly look like a never-accepted card")
    ok("digest.changed_code_is_named",
       RP.CARD_DIGEST_CHANGED in mby[Q2]["reopen_codes"])
    ok("digest.changed_not_excluded",
       Q2 not in {tuple(c["identity"]) for c in moved["excluded"]})
    ok("digest.changed_counted_as_reopened",
       moved["summary"]["reopened"] == 1)
    reason = " ".join(mby[Q2]["reopen_reasons"])
    for what, needle in (("accepted_digest", ACCEPTED_DIGEST[:16]),
                         ("current_digest", MOVED_DIGEST[:16]),
                         ("review_id", "TRANCHE-4-ACCEPT-001"),
                         ("accept_date", "2026-09-05")):
        ok("digest.reason_states_%s" % what, needle in reason,
           "the reopen reason must be auditable without re-running anything")

    # --- 6. a digest change is NOT a defect finding -------------------------
    ok("digest.change_is_not_a_p1_claim",
       "P1" not in mby[Q2]["why_in_pool"]
       and not any(w in " ".join(mby[Q2]["reopen_reasons"]).lower()
                   for w in ("incorrect", "defective", "failed")),
       "changed bytes mean the accept no longer covers them - not that the "
       "card is wrong")

    # --- the accepted card no longer exists at all --------------------------
    absent = RP.build_pool(docs, accepts={Q2: _accept_record()},
                           live_digests={})
    aby = {tuple(c["identity"]): c for c in absent["cards"]}
    ok("digest.absent_card_reopens", Q2 in aby,
       "a card the corpus no longer holds cannot stay accepted")
    ok("digest.absent_card_code", RP.CARD_ABSENT in aby[Q2]["reopen_codes"])
    ok("digest.absent_card_current_digest_is_null",
       aby[Q2]["digest_state"]["current_digest"] is None)

    # --- C. unrelated repository movement does NOT reopen -------------------
    # The point of pinning bytes rather than a commit: every unrelated commit
    # on main would otherwise invalidate every acceptance in the file.
    later_head = RP.build_pool(docs,
                               accepts={Q2: _accept_record(
                                   repo_head_reviewed="0000000")},
                               live_digests=live_same)
    ok("digest.repo_head_movement_alone_does_not_reopen",
       Q2 in {tuple(c["identity"]) for c in later_head["excluded"]},
       "repo_head_reviewed is provenance; the digest is the validity test")
    ok("digest.repo_head_recorded",
       later_head["excluded"][0]["accept_records"][0]["repo_head_reviewed"]
       == "0000000")

    # --- D. later explicit risk reopens even an unchanged card --------------
    risky = RP.build_pool(
        _one_correction() + [("corr_b.json", _corr("CORR-B", [dict(NARROW)],
                                                   origin="candidate_feedback",
                                                   date="2026-09-09"))],
        accepts={Q2: _accept_record()}, live_digests=live_same)
    rby = {tuple(c["identity"]): c for c in risky["cards"]}
    ok("digest.later_evidence_still_reopens_unchanged_card", Q2 in rby,
       "digest equality must not become a way to ignore later evidence")
    ok("digest.later_evidence_code",
       RP.LATER_EVIDENCE in rby[Q2]["reopen_codes"])
    ok("digest.later_evidence_is_additional_not_replacement",
       RP.CARD_DIGEST_CHANGED not in rby[Q2]["reopen_codes"],
       "the two triggers must stay distinguishable in the record")

    # --- fail closed: a WHOLE_CARD accept with no live digests supplied -----
    raises("digest.absent_live_digests_is_loud",
           lambda: RP.build_pool(docs, accepts={Q2: _accept_record()}),
           "live card digests")
    ok("digest.no_accepts_needs_no_digests",
       RP.build_pool(docs, accepts={})["summary"]["cards_in_pool"] == 1,
       "the digest requirement must only bite where an accept could exclude")

    # A NARROW_SCOPE record never excludes, so it needs no live digest to be
    # safe - but it must still not crash the build.
    narrow = RP.build_pool(docs,
                           accepts={Q2: _accept_record(accept_scope="NARROW_SCOPE")})
    ok("digest.narrow_scope_builds_without_digests",
       Q2 in {tuple(c["identity"]) for c in narrow["cards"]})

    # --- determinism, with the new fields in the payload -------------------
    ok("digest.payload_deterministic",
       RP.canonical_json(moved)
       == RP.canonical_json(RP.build_pool(docs, accepts={Q2: _accept_record()},
                                          live_digests=live_moved)),
       "digest state must not carry anything run-varying into the payload")

    # --- J. prose hints STILL have no exclusion authority -------------------
    hinted = RP.build_pool(docs, accepts={}, prose_hints={Q2: "tranche1 s5"})
    ok("digest.prose_hint_still_cannot_exclude",
       Q2 in {tuple(c["identity"]) for c in hinted["cards"]}
       and hinted["excluded"] == [],
       "the original rule must survive the acceptance-contract change")


# --- 3. Pool rules ---------------------------------------------------------
# Fixtures, not live repo state: these pin the RULES, so they keep their meaning
# as the bank grows.

def _corr(cid, cards, origin="gpt_content_review", date="2026-09-01", **over):
    doc = {"correction_id": cid, "kind": "POST_RELEASE_CORRECTION",
           "status": "AUTHORISED", "origin": origin, "date": date, "cards": cards}
    doc.update(over)
    return doc


def _batch(bid, cards, **over):
    doc = {"batch_id": bid, "kind": "CURRENT_INTAKE_PRODUCTION", "cards": cards}
    doc.update(over)
    return doc


NARROW = {"file": "QB4_H.html", "path": "meoclass1/QB4_H.html", "anchor": "q2",
          "classification": "PROPAGATED_FACT_CORRECTION"}
PRIMARY = {"file": "QB4_H.html", "path": "meoclass1/QB4_H.html", "anchor": "q11",
           "classification": "PRIMARY_CORRECTION"}
NEWCARD = {"file": "QB7_I.html", "anchor": "q10", "action_kind": "NEW_CARD"}

Q2 = ("meoclass1/QB4_H.html", "q2")
Q11 = ("meoclass1/QB4_H.html", "q11")
Q10 = ("meoclass1/QB7_I.html", "q10")


def control_pool_rules():
    docs = [("corr_a.json", _corr("CORR-A", [NARROW, PRIMARY])),
            ("batch_h4.json", _batch("H4", [NEWCARD]))]
    ev = RP.collect_evidence(docs)

    ok("pool.evidence_keyed_by_identity", set(ev) == {Q2, Q11, Q10})

    # CORRECTED != REVIEWED, in its sharpest form.
    pool = RP.build_pool(docs, accepts={})
    by_id = {tuple(c["identity"]): c for c in pool["cards"]}
    ok("pool.corrected_card_still_in_pool", Q2 in by_id,
       "a corrected card must not be treated as reviewed")
    ok("pool.narrow_only_flagged",
       "NARROW_CORRECTION_ONLY" in by_id[Q2]["risk_signals"],
       "swept-only card never had its own substance adjudicated")
    ok("pool.primary_correction_not_narrow_only",
       "NARROW_CORRECTION_ONLY" not in by_id[Q11]["risk_signals"])
    ok("pool.narrow_only_outranks_primary",
       by_id[Q2]["risk_score"] > by_id[Q11]["risk_score"],
       "unadjudicated substance is riskier than adjudicated-and-fixed")

    # Explicit WHOLE_CARD acceptance is the only thing that removes a card.
    accepts = {Q2: _accept_record(evidence="tranche1 s5", date="2026-09-02")}
    live = {Q2: ACCEPTED_DIGEST}
    excluded = RP.build_pool(docs, accepts=accepts, live_digests=live)
    ok("pool.whole_card_accept_excludes",
       Q2 not in {tuple(c["identity"]) for c in excluded["cards"]})
    ok("pool.excluded_card_is_reported_not_vanished",
       Q2 in {tuple(c["identity"]) for c in excluded["excluded"]},
       "an excluded card must remain visible with its reason")
    ok("pool.exclusion_carries_evidence",
       excluded["excluded"][0]["evidence"] == "tranche1 s5")

    # Narrow-scope acceptance must NOT exclude.
    narrow_acc = {Q2: _accept_record(accept_scope="NO_PROPAGATION",
                                     evidence="tranche1 s5", date="2026-09-02")}
    kept = RP.build_pool(docs, accepts=narrow_acc, live_digests=live)
    ok("pool.narrow_accept_keeps_card_in_pool",
       Q2 in {tuple(c["identity"]) for c in kept["cards"]},
       "partial acceptance must never become whole-card acceptance")

    # Reopen: new evidence dated after the acceptance overrides it.
    later = docs + [("corr_b.json", _corr("CORR-B", [dict(NARROW)],
                                          origin="candidate_feedback",
                                          date="2026-09-04"))]
    reopened = RP.build_pool(later, accepts=accepts, live_digests=live)
    rby = {tuple(c["identity"]): c for c in reopened["cards"]}
    ok("pool.reopened_on_new_evidence", Q2 in rby,
       "an accepted card touched by later evidence must reopen")
    ok("pool.reopen_reason_recorded",
       any("CORR-B" in r for r in rby[Q2]["reopen_reasons"]))
    ok("pool.reopen_status", rby[Q2]["review_status"] == "REOPENED")

    # Source-custody signal.
    cust = [("corr_c.json", _corr("CORR-C", [dict(NARROW)],
                                  authority="registered as SRC-GRAINCODE-MSC23-59"))]
    cby = {tuple(c["identity"]): c
           for c in RP.build_pool(cust, accepts={})["cards"]}
    ok("pool.source_custody_signal",
       cby[Q2]["source_custody_signals"] != [],
       "SRC- registry reference must surface as a custody signal")

    # One card named by two manifests is ONE pool entry.
    dupe = [("corr_a.json", _corr("CORR-A", [dict(NARROW)])),
            ("corr_b.json", _corr("CORR-B", [{"file": "QB4_H.html", "anchor": "q2",
                                              "classification": "SCOPE_PASS_CORRECTION"}]))]
    dpool = RP.build_pool(dupe, accepts={})
    ok("pool.dedup_by_identity", len(dpool["cards"]) == 1,
       "bare-file and path spellings of one card must not both appear")
    ok("pool.dedup_merges_provenance",
       len(dpool["cards"][0]["correction_families"]) == 2,
       "dedup must merge evidence, not discard it")

    ok("pool.ranked_descending",
       [c["risk_score"] for c in pool["cards"]]
       == sorted([c["risk_score"] for c in pool["cards"]], reverse=True))
    ok("pool.every_card_has_reason",
       all(c["why_in_pool"] for c in pool["cards"]))
    ok("pool.tranche_priority_present",
       all(c["recommended_tranche_priority"] for c in pool["cards"]))


# --- 4. Determinism and JSON/Markdown consistency --------------------------
# The Markdown is RENDERED FROM the JSON, never authored beside it. If the two
# can disagree, the reviewer-facing document is not evidence of anything.

def control_determinism_and_report():
    docs = [("corr_a.json", _corr("CORR-A", [NARROW, PRIMARY])),
            ("batch_h4.json", _batch("H4", [NEWCARD]))]
    pool = RP.build_pool(docs, accepts={})

    a = RP.canonical_json(pool)
    b = RP.canonical_json(RP.build_pool(list(reversed(docs)), accepts={}))
    ok("determinism.byte_identical_across_runs", a == b,
       "manifest iteration order must not reach the canonical payload")
    ok("determinism.hash_stable", RP.content_hash(pool) == RP.content_hash(pool))

    # Key ORDER must not reach the bytes. Two payloads that differ only in the
    # order their keys were inserted must serialise identically - otherwise
    # determinism rests on dict insertion order, which is not a guarantee we
    # control once inputs vary.
    fwd = {"alpha": 1, "beta": {"x": 1, "y": 2}, "gamma": [1, 2]}
    rev = {"gamma": [1, 2], "beta": {"y": 2, "x": 1}, "alpha": 1}
    ok("determinism.key_order_does_not_reach_bytes",
       RP.canonical_json(fwd) == RP.canonical_json(rev),
       "serialisation must sort keys, not inherit insertion order")
    ok("determinism.trailing_newline", a.endswith(chr(10)))
    ok("determinism.no_timestamp_in_canonical",
       "generated_at" not in a,
       "a timestamp inside the canonical payload would break reproducibility")

    doc = RP.build_document(pool, accepts_hash="abc123", generator_commit="deadbee")
    ok("provenance.canonical_nested", doc["canonical"] == pool)
    ok("provenance.records_accepts_hash", doc["provenance"]["accepts_sha256"] == "abc123")
    ok("provenance.records_content_hash",
       doc["provenance"]["canonical_sha256"] == RP.content_hash(pool))
    ok("provenance.records_generator_commit",
       doc["provenance"]["generator_commit"] == "deadbee")

    md = RP.render_markdown(pool)
    ok("report.states_pool_count",
       ("%d" % pool["summary"]["cards_in_pool"]) in md)
    ok("report.has_required_sections",
       all(h in md for h in ("## Summary", "## Ranked review pool",
                             "## Reopened", "## Corrected only by narrow families",
                             "## Explicitly accepted", "## Unknown",
                             "## Out of scope")),
       "every section the reviewer was promised must exist")
    ok("report.lists_every_pooled_card",
       all(("%s#%s" % (c["file"], c["anchor"])) in md for c in pool["cards"]),
       "the Markdown must not silently truncate the pool")
    ok("report.gives_a_reason_per_card",
       all(c["why_in_pool"][:24] in md for c in pool["cards"]))
    ok("report.rendered_deterministically",
       md == RP.render_markdown(RP.build_pool(list(reversed(docs)), accepts={})))
    ok("report.states_the_governing_rule", "CORRECTED != REVIEWED" in md)

    # Consistency: counts in prose must equal counts in the payload.
    counts = RP.report_counts(md)
    ok("consistency.md_counts_match_json",
       counts == {"cards_in_pool": pool["summary"]["cards_in_pool"],
                  "explicitly_accepted": pool["summary"]["explicitly_accepted"],
                  "reopened": pool["summary"]["reopened"],
                  "unknown_manual_adjudication":
                      pool["summary"]["unknown_manual_adjudication"]},
       "rendered counts drifted from the payload they came from")


# --- 5. Prose hints carry zero exclusion authority --------------------------

def control_prose_hints_never_exclude():
    docs = [("corr_a.json", _corr("CORR-A", [NARROW]))]
    hints = {Q2: "TRANCHE1 section 5 'Accepted cards - untouched'"}
    pool = RP.build_pool(docs, accepts={}, prose_hints=hints)
    ids = {tuple(c["identity"]) for c in pool["cards"]}
    ok("prose.hint_does_not_exclude", Q2 in ids,
       "prose accept-sections must never remove a card from the pool")
    row = pool["cards"][0]
    ok("prose.hint_marks_manual_adjudication",
       row["review_status"] == "UNKNOWN_MANUAL_ADJUDICATION")
    ok("prose.hint_recorded_as_evidence", row["prose_hint"] == hints[Q2])
    ok("prose.hint_only_reduces_score",
       row["risk_score"] < RP.build_pool(docs, accepts={})["cards"][0]["risk_score"])


# --- 6. Prose extraction is advisory, and says so --------------------------

SAMPLE = chr(10).join([
    "# GPT High-Risk Content Review - Tranche 1",
    "",
    "## 1. Family A - Grain Code (QB2_A#q11, #q33)",
    "",
    "Body text mentioning QB2_A#q11 as edited.",
    "",
    "## 5. Accepted cards - untouched",
    "",
    "`QB3_F#q8`, `QB7_D#q13` and `QB1_K#q10` were **not** edited.",
    "",
    "## 6. Newly discovered - REPORTED, NOT FIXED",
    "",
    "QB5_C_B#q5 still carries a thin REG-BOX.",
    "",
    "## 9. K-4 - IGF amendments  *(ADJUDICATED - NO CHANGE)*",
    "",
    "QB6_A#q4 was verified and left alone.",
])


def control_prose_extraction():
    with tempfile.TemporaryDirectory() as d:
        f = pathlib.Path(d) / "GPT_REVIEW_HIGHRISK_TRANCHE1_20260904.md"
        f.write_text(SAMPLE, encoding="utf-8")
        hints = RP.extract_prose_hints([f])

        ok("prose.reads_accept_section",
           ("meoclass1/QB3_F.html", "q8") in hints)
        ok("prose.reads_all_of_accept_section",
           all(k in hints for k in [("meoclass1/QB7_D.html", "q13"),
                                    ("meoclass1/QB1_K.html", "q10")]))
        ok("prose.reads_no_change_heading",
           ("meoclass1/QB6_A.html", "q4") in hints)
        ok("prose.ignores_edited_families",
           ("meoclass1/QB2_A.html", "q11") not in hints,
           "a card the tranche EDITED is not an acceptance hint")
        ok("prose.ignores_reported_not_fixed",
           ("meoclass1/QB5_C_B.html", "q5") not in hints,
           "REPORTED, NOT FIXED is the opposite of an acceptance")
        ok("prose.hint_cites_its_source",
           "TRANCHE1" in hints[("meoclass1/QB3_F.html", "q8")])
        ok("prose.extraction_deterministic",
           hints == RP.extract_prose_hints([f]))


# --- 7. End to end, against the real repository ----------------------------
# The generator READS the bank and writes only its own git-ignored output. A
# tool that builds a review queue must never mutate the thing under review.

REPO = Path(__file__).resolve().parent.parent.parent
BUILD = REPO / "tools" / "oral" / "build_review_pool.py"
OUT = REPO / "reports" / "oral-review-pool"


def _run(*args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run([sys.executable, str(BUILD), *args], cwd=str(REPO),
                          capture_output=True, text=True, env=env, timeout=300)


def _git_status():
    out = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain"],
                         capture_output=True, text=True, timeout=60)
    return out.stdout


def control_end_to_end():
    before = _git_status()

    first = _run()
    ok("e2e.generator_exits_clean", first.returncode == 0, first.stderr[-300:])
    ok("e2e.writes_json", (OUT / "review_pool.json").exists())
    ok("e2e.writes_markdown", (OUT / "review_pool.md").exists())

    doc1 = json.loads((OUT / "review_pool.json").read_text(encoding="utf-8"))
    md1 = (OUT / "review_pool.md").read_text(encoding="utf-8")

    second = _run()
    ok("e2e.second_run_exits_clean", second.returncode == 0)
    doc2 = json.loads((OUT / "review_pool.json").read_text(encoding="utf-8"))
    md2 = (OUT / "review_pool.md").read_text(encoding="utf-8")

    ok("e2e.canonical_payload_byte_identical",
       RP.canonical_json(doc1["canonical"]) == RP.canonical_json(doc2["canonical"]),
       "a re-run on unchanged evidence must reproduce the pool exactly")
    ok("e2e.canonical_hash_stable",
       doc1["provenance"]["canonical_sha256"]
       == doc2["provenance"]["canonical_sha256"])
    ok("e2e.markdown_byte_identical", md1 == md2)

    ok("e2e.check_reports_current", _run("--check").returncode == 0,
       "--check must agree with what was just written")

    # Consistency against the REAL pool, not a fixture.
    ok("e2e.md_counts_match_json",
       RP.report_counts(md1)["cards_in_pool"]
       == doc1["canonical"]["summary"]["cards_in_pool"])

    # Identity dedup holds across the whole live corpus.
    pool = doc1["canonical"]
    idents = [tuple(c["identity"]) for c in pool["cards"]] +              [tuple(c["identity"]) for c in pool["excluded"]]
    ok("e2e.no_duplicate_identity", len(idents) == len(set(idents)),
       "one card must not appear twice under two spellings")

    # CORRECTED != REVIEWED, against live evidence.
    corrected = [c for c in pool["cards"] if c["correction_families"]]
    ok("e2e.corrected_cards_remain_in_pool", corrected != [],
       "corrected cards must still be queued for review")

    # Provenance is present, and outside the canonical payload.
    ok("e2e.provenance_outside_canonical",
       "generated_at" not in RP.canonical_json(pool))
    ok("e2e.provenance_records_accepts_hash",
       doc1["provenance"]["accepts_sha256"] is not None)

    # THE READ-ONLY PROOF.
    after = _git_status()
    ok("e2e.repository_unmutated", before == after,
       "generator changed tracked repository state: %r -> %r"
       % (before[-200:], after[-200:]))
    ok("e2e.output_is_git_ignored",
       "reports/oral-review-pool" not in after,
       "generated output must be ignored, not staged")


# --- 8. Scope, held visibly ------------------------------------------------
# The pool is the MEO Class 1 Oral question bank: meoclass1/QB*.html question
# anchors. Evidence also touches the SQ (Solved QP) series and non-question
# anchors. Those are OUT OF SCOPE - but they are reported, not dropped, because
# a silent filter is indistinguishable from a bug.

def control_scope():
    docs = [("corr_x.json", _corr("CORR-X", [
        dict(NARROW),
        {"file": "QB1_A.html", "path": "SQ/QB1_A.html", "anchor": "q3",
         "classification": "PRIMARY_CORRECTION"},
        {"file": "QB1_A.html", "path": "meoclass1/QB1_A.html",
         "anchor": "dependency-graph", "classification": "PRIMARY_CORRECTION"},
    ]))]
    pool = RP.build_pool(docs, accepts={})
    ids = {tuple(c["identity"]) for c in pool["cards"]}

    ok("scope.oral_card_included", Q2 in ids)
    ok("scope.other_series_excluded", ("SQ/QB1_A.html", "q3") not in ids,
       "the Solved-QP series is a different pool")
    ok("scope.non_question_anchor_excluded",
       ("meoclass1/QB1_A.html", "dependency-graph") not in ids)

    out = {tuple(c["identity"]): c for c in pool["scope_excluded"]}
    ok("scope.exclusions_are_reported", len(out) == 2,
       "out-of-scope evidence must stay visible, never silently filtered")
    ok("scope.exclusion_gives_reason",
       all(c["why_out_of_scope"] for c in out.values()))
    ok("scope.reason_names_the_series",
       "SQ" in out[("SQ/QB1_A.html", "q3")]["why_out_of_scope"])
    ok("scope.counted_in_summary",
       pool["summary"]["out_of_scope"] == 2)

    md = RP.render_markdown(pool)
    ok("scope.reported_in_markdown",
       all(("%s#%s" % (c["file"], c["anchor"])) in md
           for c in pool["scope_excluded"]),
       "out-of-scope rows must appear in the reviewer-facing report")


# --- 9. The digest is the CORRECTION toolchain's digest, not a second one --
# Section 3 of the hardening contract: reuse exactly the canonical card digest
# the oral correction tooling already uses. A second implementation that agreed
# today and drifted tomorrow would reopen every acceptance in the file for a
# reason no reviewer could act on.

def control_digest_reuse():
    from validate_batch_h_series import card_digests as canonical   # noqa: E402
    from oral_bytes import read_text                                # noqa: E402

    page = REPO / "meoclass1" / "QB4_H.html"
    ok("reuse.corpus_page_present", page.is_file(), str(page))
    if not page.is_file():
        return

    text = read_text(page)
    ok("reuse.same_function_object",
       RP.canonical_card_digests is canonical,
       "review_pool must call the correction toolchain's digest, not a copy")

    mine = RP.card_digests_for("meoclass1/QB4_H.html", REPO)
    theirs = {("meoclass1/QB4_H.html", a): d
              for a, d in canonical(text).items()}
    ok("reuse.identical_digests_on_a_real_page", mine == theirs,
       "the pool digest disagreed with the correction-record digest")
    ok("reuse.digests_are_repo_convention",
       all(len(d) == 64 and d == d.lower() for d in mine.values()))

    # CRLF must not move a digest: .gitattributes pins these pages to LF in the
    # object store while a working copy may hold CRLF.
    ok("reuse.crlf_insensitive",
       canonical(text.replace(chr(10), chr(13) + chr(10))) == canonical(text),
       "a CRLF checkout would otherwise reopen every acceptance at once")

    missing = RP.card_digests_for("meoclass1/QB_DOES_NOT_EXIST.html", REPO)
    ok("reuse.absent_page_is_empty_not_fatal", missing == {},
       "an accepted card on a deleted page must reopen, not crash the build")


# --- 10. --explain shows the acceptance logic ------------------------------
# An exclusion a reviewer cannot interrogate is an exclusion they have to take
# on trust, which is the posture that produced N-5 in the first place.

def control_explain_cli():
    built = _run()
    ok("explain.pool_built_for_explain", built.returncode == 0,
       built.stderr[-300:])
    if built.returncode != 0:
        return
    pool = json.loads((OUT / "review_pool.json").read_text(encoding="utf-8"))

    rows = pool["canonical"]["cards"]
    ok("explain.pool_has_a_card_to_explain", rows != [])
    if not rows:
        return
    target = "%s#%s" % (rows[0]["file"], rows[0]["anchor"])

    got = _run("--explain", target)
    ok("explain.exits_clean", got.returncode == 0, got.stderr[-300:])
    text = got.stdout
    ok("explain.names_the_card", target in text)
    ok("explain.states_review_status", rows[0]["review_status"] in text)
    ok("explain.states_the_rule", "digest_match" in text or "no acceptance" in text,
       "explain must say what the acceptance logic concluded, not just a status")

    unknown = _run("--explain", "meoclass1/QB_NOPE.html#q1")
    ok("explain.unknown_card_is_loud", unknown.returncode != 0,
       "explaining a card the pool does not hold must not print a reassuring "
       "blank")
    ok("explain.unknown_card_writes_nothing_misleading",
       "EXPLICITLY_ACCEPTED" not in unknown.stdout)


CONTROLS = [control_identity, control_accepts, control_acceptance_contract,
            control_digest_reuse, control_explain_cli, control_pool_rules,
            control_determinism_and_report,
            control_prose_hints_never_exclude,
            control_prose_extraction,
            control_end_to_end,
            control_scope]


def main():
    for c in CONTROLS:
        # A control that CRASHES must become a named failure, not a traceback.
        # A mutation suite lifts failing check names out of this script's
        # stdout; an uncaught exception prints no check name at all, so a
        # mutation that makes a control explode would read as "nothing failed"
        # - an escape produced by the harness rather than by the code.
        try:
            c()
        except BaseException as exc:                  # noqa: BLE001
            CHECKS[0] += 1
            FAILURES.append("%s.control_crashed - %s: %s"
                            % (c.__name__, type(exc).__name__, exc))
    if FAILURES:
        print("REVIEW POOL CONTROLS: FAIL (%d checks, %d failures)"
              % (CHECKS[0], len(FAILURES)))
        # `FAIL <check>` is the repo-wide probe idiom that
        # `oral_content_mutation.run_probe` lifts check names out of, so a
        # mutation suite can require that a mutation breaks the control that
        # OWNS it rather than merely turning the suite red somewhere.
        for f in FAILURES:
            print("FAIL %s" % f)
        return 1
    print("REVIEW POOL CONTROLS: PASS (%d checks)" % CHECKS[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
