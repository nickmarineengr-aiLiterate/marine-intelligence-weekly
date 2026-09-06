"""Derive a ranked review pool for the MEO Class 1 Oral question bank.

The governing rule is CORRECTED != REVIEWED. A card may carry several correction
manifests and still never have been read end to end, so correction evidence
RANKS a card - it never clears one. Only an explicit entry in
review_pool_accepts.json removes a card from the pool, and a card with no entry
STAYS IN.

Prose review reports (GPT_REVIEW_*.md) are evidence for ranking and reviewer
hints only. They carry ZERO exclusion authority: Tranche 1's "Accepted cards -
untouched" means no propagation reached them, which is acceptance of non-impact
within one tranche's scope, not a whole-card review clearance. Reading it as the
latter would drop cards that were never reviewed - the false green these gates
exist to prevent.

AN ACCEPTANCE COVERS BYTES, NOT A CARD NAME. Schema/1 of the adjudication file
recorded only a card identity and a citation, and the loader read only that -
so an entry could name the exact digest it had been taken over and the
generator would still exclude the card long after those bytes were rewritten.
The record looked byte-pinned; nothing read the pin. Schema/2 makes
`canonical_card_digest` mandatory and load-bearing: when the live card's
canonical digest differs from the accepted one, the acceptance no longer covers
what is on the page and the card is REOPENED.

REOPENED IS NOT A DEFECT CLAIM. A moved digest says "the prior whole-card
acceptance no longer covers the current bytes", never "this card is wrong". The
card goes back into the queue at its evidence-derived rank; nothing about it is
marked incorrect.

`repo_head_reviewed` is PROVENANCE, not the validity test. Every unrelated
commit on main moves HEAD, and treating that as invalidation would reopen the
whole file every day for reasons no reviewer could act on. The digest is what
decides; the head is what lets an auditor find the tree that was read.

REVIEW PRIORITY IS NOT DEFECT SEVERITY. The queue bands are R1..R4 under the
field `review_priority`. R1 means "read this card first"; it never means "this
card is wrong". They were spelled P1..P4, colliding with the P0/P1/P2/P3 content
severity MIW uses everywhere else - and a card reopened purely because its bytes
moved, with no defect established at all, was emitted as `"P1"`.

This module is the library. tools/oral/build_review_pool.py is the CLI.
"""
from __future__ import annotations

import pathlib as _pathlib
import sys as _sys

_sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))

#: THE canonical card digest, imported - never reimplemented. This is the same
#: function object the oral correction records are validated with, so a pool
#: exclusion and a correction pin can never come to disagree about what a card
#: hashes to. `validate_correction_igfchain` reaches it by the same import.
from validate_batch_h_series import card_digests as canonical_card_digests  # noqa: E402
from oral_bytes import read_text                                            # noqa: E402

QB_ROOT = "meoclass1"


class PoolError(Exception):
    """A refusal. Raised whenever evidence is malformed, ambiguous or
    unresolvable - never downgraded to a warning, because a review pool that
    silently drops a card is worse than one that refuses to build."""


def _clean(value):
    return value.strip() if isinstance(value, str) else value


def card_identity(card, where="<card>"):
    """Return the canonical ``(path, anchor)`` identity for a manifest card.

    Batch manifests carry a bare ``file``; correction manifests carry both
    ``file`` and a repo-relative ``path``. Both spellings must collapse to the
    single identity ``("meoclass1/QB4_H.html", "q2")`` or one card enters the
    pool twice.
    """
    if not isinstance(card, dict):
        raise PoolError("%s: card entry is %s, not an object"
                        % (where, type(card).__name__))

    anchor = _clean(card.get("anchor"))
    if not anchor:
        raise PoolError("%s: card entry has no usable 'anchor'" % where)

    path = _clean(card.get("path"))
    if not path:
        name = _clean(card.get("file"))
        if not name:
            raise PoolError("%s: card entry has neither 'path' nor 'file'" % where)
        path = "%s/%s" % (QB_ROOT, name)

    path = path.replace("\\", "/").lstrip("./")
    return (path, anchor)


# --- the adjudication file -------------------------------------------------

ACCEPTS_SCHEMA = "miw-oral-review-pool-accepts/2"

#: Schemas this loader will not coerce. Schema/1 could not express the digest an
#: acceptance was taken over, so a /1 entry cannot be checked against the live
#: card and cannot be an enforceable whole-card clearance. Silently reading one
#: as /2 - defaulting the digest, or skipping the check when it is absent - is
#: precisely the false green this file exists to prevent, so /1 is refused by
#: name with an instruction rather than accepted with a warning.
RETIRED_ACCEPTS_SCHEMAS = {
    "miw-oral-review-pool-accepts/1":
        "schema/1 entries carry no canonical_card_digest, so they cannot be "
        "checked against the live card and are not enforceable whole-card "
        "accepts. Re-adjudicate each entry and rewrite it as %s." % ACCEPTS_SCHEMA,
}

#: Required on EVERY entry, whatever its scope. Each of these is enforced by
#: its OWN validator below, with its own message - there is no aggregate
#: "missing fields" pass, because a second check that can never fire first is
#: decoration, and this file has no room for checks that only look like checks. A narrow record needs no digest
#: to be safe - it cannot exclude anything - but one shape with no optional
#: branch is one shape that cannot be mutated into a loophole, and a reviewer
#: who records what they read is recording it for the narrow case too.
ACCEPT_REQUIRED_TEXT = ("evidence", "adjudicated_by", "date", "review_id",
                        "reopen_policy")
ACCEPT_REQUIRED = ACCEPT_REQUIRED_TEXT + ("accept_scope", "repo_head_reviewed",
                                          "canonical_card_digest",
                                          "residual_findings")

#: Everything an entry may carry. An unrecognised key is a refusal, following
#: `oral_manifest`'s UNCLASSIFIED rule: a new authorisation-looking field that
#: nothing reads is decoration that a later reader will mistake for governance.
ACCEPT_FIELDS = frozenset(ACCEPT_REQUIRED) | {"file", "path", "anchor", "note"}

_HEX = frozenset("0123456789abcdef")


def _is_digest(value):
    """The repository's sha256 convention: exactly 64 lowercase hex characters.

    Deliberately the same rule as `oral_manifest._is_digest`. Restated rather
    than imported so this stays a two-line, obviously-correct predicate; the
    DIGEST itself is imported, which is where divergence would actually cost.
    """
    return (isinstance(value, str) and len(value) == 64
            and all(c in _HEX for c in value))


def _is_commitish(value):
    """An abbreviated or full git object name. Provenance only."""
    return (isinstance(value, str) and 7 <= len(value) <= 40
            and all(c in _HEX for c in value))

#: Only WHOLE_CARD removes a card from the pool. The narrower scopes exist so a
#: reviewer can record what was actually checked WITHOUT that record quietly
#: growing into a whole-card clearance.
ACCEPT_SCOPES = {
    "WHOLE_CARD":     True,   # read end to end and accepted; excludes
    "NARROW_SCOPE":   False,  # one limb/proposition checked; ranks only
    "NO_PROPAGATION": False,  # a tranche's edits did not reach it; ranks only
}


def excludes(entry):
    """True only for a whole-card acceptance."""
    return ACCEPT_SCOPES[entry["accept_scope"]]


def load_accepts(path, known_identities):
    """Load review_pool_accepts.json, refusing anything it cannot trust.

    An absent file is a legitimate state - nothing has been adjudicated, so
    every card stays in the pool. Anything PRESENT but wrong is fatal: there is
    no fallback to prose parsing, because a half-trusted exclusion list is how
    an unreviewed card disappears from a queue a human believes is complete.
    """
    import json
    import pathlib

    path = pathlib.Path(path)
    if not path.exists():
        return {}

    raw = path.read_text(encoding="utf-8")
    try:
        doc = json.loads(raw)
    except ValueError as exc:
        raise PoolError("%s: cannot parse as JSON - %s" % (path.name, exc)) from exc

    if not isinstance(doc, dict):
        raise PoolError("%s: top level must be an object" % path.name)
    schema = doc.get("schema")
    if schema in RETIRED_ACCEPTS_SCHEMAS:
        raise PoolError("%s: schema %s is retired - %s"
                        % (path.name, schema, RETIRED_ACCEPTS_SCHEMAS[schema]))
    if schema != ACCEPTS_SCHEMA:
        raise PoolError("%s: schema is %r, expected %r"
                        % (path.name, schema, ACCEPTS_SCHEMA))

    entries = doc.get("accepts")
    if not isinstance(entries, list):
        raise PoolError("%s: 'accepts' must be a list" % path.name)

    out = {}
    for i, entry in enumerate(entries):
        where = "%s accepts[%d]" % (path.name, i)
        if not isinstance(entry, dict):
            raise PoolError("%s: entry is %s, not an object"
                            % (where, type(entry).__name__))

        unknown = sorted(set(entry) - ACCEPT_FIELDS)
        if unknown:
            raise PoolError(
                "%s: unrecognised field(s) %s - an acceptance record may carry "
                "only %s. A governance-looking key that nothing reads is how a "
                "reader comes to believe a check exists that does not."
                % (where, ", ".join(unknown), ", ".join(sorted(ACCEPT_FIELDS))))

        ident = card_identity(entry, where)

        scope = _clean(entry.get("accept_scope"))
        if scope not in ACCEPT_SCOPES:
            raise PoolError("%s: accept_scope %r is not one of %s"
                            % (where, scope, sorted(ACCEPT_SCOPES)))

        for field in ACCEPT_REQUIRED_TEXT:
            if not _clean(entry.get(field)):
                raise PoolError(
                    "%s: %r is required and must be non-empty - an acceptance "
                    "that does not say who accepted what, when, under which "
                    "review and under what reopen policy cannot be audited"
                    % (where, field))

        digest = _clean(entry.get("canonical_card_digest"))
        if not _is_digest(digest):
            raise PoolError(
                "%s: canonical_card_digest %r is not a sha256 in this "
                "repository's convention (exactly 64 lowercase hex characters). "
                "A malformed digest must never be treated as 'no digest' - that "
                "would silently restore the unchecked acceptance."
                % (where, entry.get("canonical_card_digest")))

        head = _clean(entry.get("repo_head_reviewed"))
        if not _is_commitish(head):
            raise PoolError(
                "%s: repo_head_reviewed %r is not a git object name (7-40 "
                "lowercase hex characters)" % (where, entry.get("repo_head_reviewed")))

        residuals = _residual_findings(entry.get("residual_findings"), where)

        if ident in out:
            raise PoolError("%s: duplicate adjudication for %s#%s - two entries for "
                            "one card is ambiguous, not additive"
                            % (where, ident[0], ident[1]))

        if known_identities is not None and ident not in known_identities:
            raise PoolError("%s: %s#%s is not present in the evidence corpus - an "
                            "acceptance pinned to an unstable identity would silently "
                            "stop matching" % (where, ident[0], ident[1]))

        out[ident] = {"identity": ident,
                      "accept_scope": scope,
                      "evidence": _clean(entry.get("evidence")),
                      "adjudicated_by": _clean(entry.get("adjudicated_by")),
                      "date": _clean(entry.get("date")),
                      "review_id": _clean(entry.get("review_id")),
                      "repo_head_reviewed": head,
                      "canonical_card_digest": digest,
                      "residual_findings": residuals,
                      "reopen_policy": _clean(entry.get("reopen_policy")),
                      "note": _clean(entry.get("note")) or None}
    return out


def _residual_findings(value, where):
    """Validate the SHAPE of residual_findings. Never its severity.

    Section 10 of the hardening contract is explicit that the generator does
    not adjudicate severity: P2/P3 residuals are legitimate under a whole-card
    acceptance, and whether a P1 residual may sit under one is a human ruling,
    not a string comparison in a build tool. So this refuses a residual that
    cannot be READ - not one it disagrees with.
    """
    if value is None or not isinstance(value, list):
        raise PoolError(
            "%s: residual_findings must be a list (use [] for none) - a missing "
            "list and 'no residuals' must not look the same" % where)
    out = []
    for j, item in enumerate(value):
        if not isinstance(item, dict):
            raise PoolError("%s: residual_findings[%d] is %s, not an object"
                            % (where, j, type(item).__name__))
        extra = sorted(set(item) - {"severity", "note", "id", "reference"})
        if extra:
            raise PoolError("%s: residual_findings[%d] has unrecognised field(s) %s"
                            % (where, j, ", ".join(extra)))
        for field in ("severity", "note"):
            if not _clean(item.get(field)):
                raise PoolError(
                    "%s: residual_findings[%d] needs a non-empty %r - a residual "
                    "nobody can read is not an explicit record of one"
                    % (where, j, field))
        out.append({k: _clean(v) for k, v in sorted(item.items())})
    return out


# --- evidence --------------------------------------------------------------

#: Corrections that touched a card without adjudicating its own substance. A
#: card reached ONLY by these is the sharpest form of CORRECTED != REVIEWED: it
#: looks worked-on and has never been read end to end.
NARROW_CLASSIFICATIONS = {"PROPAGATED_FACT_CORRECTION",
                          "SCOPE_PASS_CORRECTION",
                          "DEPENDENCY_CORRECTION"}
SUBSTANTIVE_CLASSIFICATIONS = {"PRIMARY_CORRECTION"}

#: Origins meaning a live defect was reported from outside the review loop.
HIGH_RISK_ORIGINS = {"candidate_feedback", "release_gate_finding",
                     "open_items_register"}

PRODUCTION_KINDS = {"CURRENT_INTAKE_PRODUCTION", "ENRICHMENT", "FOLLOWUP"}


def _manifest_id(doc, fallback):
    for key in ("correction_id", "batch_id", "batch"):
        val = _clean(doc.get(key))
        if val:
            return str(val)
    return fallback


def _custody_signals(doc):
    """SRC- registry references and explicit custody language, as a sorted list."""
    import json
    import re

    blob = json.dumps(doc)
    signals = set(re.findall(r"SRC-[A-Z0-9][A-Z0-9\-]{2,}", blob))
    if "custody" in blob.lower():
        signals.add("SOURCE_CUSTODY_LANGUAGE")
    return sorted(signals)


def collect_evidence(docs):
    """Fold manifests into per-identity evidence, keyed by canonical identity.

    ``docs`` is a sequence of ``(name, parsed_manifest)``. One card named by
    several manifests yields ONE entry whose evidence is merged.
    """
    evidence = {}
    for name, doc in docs:
        if not isinstance(doc, dict):
            raise PoolError("%s: manifest top level must be an object" % name)
        cards = doc.get("cards") or []
        if not isinstance(cards, list):
            raise PoolError("%s: 'cards' must be a list" % name)

        mid = _manifest_id(doc, name)
        kind = _clean(doc.get("kind")) or "UNTYPED_BATCH"
        origin = _clean(doc.get("origin"))
        date = _clean(doc.get("date"))
        custody = _custody_signals(doc)

        for i, card in enumerate(cards):
            ident = card_identity(card, "%s cards[%d]" % (name, i))
            ev = evidence.setdefault(ident, {
                "identity": ident, "manifests": [], "correction_families": [],
                "classifications": [], "action_kinds": [], "origins": [],
                "source_custody_signals": [], "topics": [], "dates": []})

            ev["manifests"].append({"manifest": name, "id": mid, "kind": kind,
                                    "origin": origin, "date": date})
            if kind == "POST_RELEASE_CORRECTION" and mid not in ev["correction_families"]:
                ev["correction_families"].append(mid)
            for field, bucket in (("classification", "classifications"),
                                  ("action_kind", "action_kinds"),
                                  ("topic", "topics")):
                val = _clean(card.get(field))
                if val and val not in ev[bucket]:
                    ev[bucket].append(val)
            if origin and origin not in ev["origins"]:
                ev["origins"].append(origin)
            if date:
                ev["dates"].append(date)
            for sig in custody:
                if sig not in ev["source_custody_signals"]:
                    ev["source_custody_signals"].append(sig)

    for ev in evidence.values():
        ev["source_custody_signals"].sort()
        ev["dates"].sort()
    return evidence


# --- scoring ---------------------------------------------------------------
# Integers, closed set, no floats: byte-identical output across runs and
# machines is a requirement, and a score a reviewer can re-derive by hand is
# auditable in a way a tuned weight is not.

SCORE_RULES = (
    ("NARROW_CORRECTION_ONLY", 40,
     "touched only by sweeps; its own substance was never adjudicated"),
    ("REOPENED_AFTER_ACCEPT", 30,
     "new evidence lands after the recorded acceptance"),
    ("HIGH_RISK_ORIGIN", 25,
     "a defect was reported from outside the review loop"),
    ("NEW_AUGUST_CARD", 20,
     "authored in the August intake and not independently reviewed since"),
    ("PRIMARY_CORRECTION", 15,
     "a fact on this card was found wrong at least once"),
    ("SOURCE_CUSTODY_SIGNAL", 15,
     "depends on a registered source whose custody is in play"),
    ("REPEATED_CORRECTION", 10,
     "corrected by more than one family"),
    ("ENRICHED_NOT_REVIEWED", 10,
     "content was added without a whole-card read"),
    ("PROSE_HINT_ONLY", -10,
     "a prose review mentions it as untouched; a hint, never a clearance"),
)
SCORE_WEIGHTS = {name: pts for name, pts, _ in SCORE_RULES}
SCORE_REASONS = {name: why for name, _, why in SCORE_RULES}

#: REVIEW priority, not defect severity. R for Review.
#:
#: These were spelled P1/P2/P3/P4, which is how MIW spells CONTENT DEFECT
#: SEVERITY - in correction manifests, tranche reports and residual findings.
#: They are different concepts, and the collision was not theoretical: a card
#: reopened only because its bytes moved after acceptance, with no content
#: defect established at all, was emitted as `"P1"` and rendered as `(P1)`. A
#: reviewer scanning that queue reads a P1 defect that nobody found.
#:
#: R1 means "read this card first". It never means "this card is wrong". The
#: thresholds and the score that feeds them are unchanged by the relabelling.
REVIEW_PRIORITY_BANDS = ((70, "R1"), (45, "R2"), (25, "R3"), (0, "R4"))


def risk_signals(ev, reopened, prose_hint):
    """The closed set of signals this card raises, in SCORE_RULES order."""
    cls = set(ev["classifications"])
    raised = set()

    if cls and not (cls & SUBSTANTIVE_CLASSIFICATIONS) and (cls & NARROW_CLASSIFICATIONS):
        raised.add("NARROW_CORRECTION_ONLY")
    if cls & SUBSTANTIVE_CLASSIFICATIONS:
        raised.add("PRIMARY_CORRECTION")
    if reopened:
        raised.add("REOPENED_AFTER_ACCEPT")
    if set(ev["origins"]) & HIGH_RISK_ORIGINS:
        raised.add("HIGH_RISK_ORIGIN")
    if "NEW_CARD" in ev["action_kinds"]:
        raised.add("NEW_AUGUST_CARD")
    if ev["source_custody_signals"]:
        raised.add("SOURCE_CUSTODY_SIGNAL")
    if len(ev["correction_families"]) > 1:
        raised.add("REPEATED_CORRECTION")
    if {"ENRICH_EXISTING", "EXPANSION", "CURRENCY_EXPANSION"} & set(ev["action_kinds"]):
        raised.add("ENRICHED_NOT_REVIEWED")
    if prose_hint:
        raised.add("PROSE_HINT_ONLY")

    return [name for name, _, _ in SCORE_RULES if name in raised]


def score_card(signals):
    components = [{"signal": s, "points": SCORE_WEIGHTS[s], "why": SCORE_REASONS[s]}
                  for s in signals]
    return sum(c["points"] for c in components), components


def review_priority(score):
    """The review-queue band for a risk score. Never a defect severity."""
    for floor, band in REVIEW_PRIORITY_BANDS:
        if score >= floor:
            return band
    return "R4"


# --- the pool --------------------------------------------------------------

POOL_SCHEMA = "miw-oral-review-pool/3"   # /2 digest_state+reopen_codes; /3 review_priority


#: Reopen triggers, as codes. Named constants rather than substrings so a test
#: can assert WHICH trigger fired, and so the two can never be conflated: a card
#: whose bytes moved and a card that later evidence touched are different
#: adjudications for a human, even though both go back in the queue.
CARD_DIGEST_CHANGED = "CARD_DIGEST_CHANGED_AFTER_ACCEPT"
CARD_ABSENT = "ACCEPTED_CARD_ABSENT"
LATER_EVIDENCE = "LATER_EVIDENCE_AFTER_ACCEPT"


def card_digests_for(rel_path, repo_root):
    """`{(rel_path, anchor): digest}` for one QB page, or {} if it is gone.

    An acceptance pinned to a page that no longer exists must REOPEN, not
    explode: the pool has to build in order to say so.
    """
    p = _pathlib.Path(repo_root) / rel_path
    if not p.is_file():
        return {}
    return {(rel_path, anchor): digest
            for anchor, digest in canonical_card_digests(read_text(p)).items()}


def live_digests_for(identities, repo_root):
    """Canonical digests for every identity given, one file read per page."""
    out = {}
    for rel in sorted({ident[0] for ident in identities}):
        out.update(card_digests_for(rel, repo_root))
    return {ident: out.get(ident) for ident in identities if ident in out}


def digest_state(accept, live_digests):
    """What the acceptance covered, what the card says now, and whether they agree.

    Returns None when there is no whole-card acceptance to test - the narrow
    scopes exclude nothing, so there is nothing for a digest to protect.
    """
    if not accept or not excludes(accept):
        return None
    if live_digests is None:
        raise PoolError(
            "%s#%s carries a WHOLE_CARD acceptance but no live card digests were "
            "supplied. An acceptance that is never compared against the current "
            "bytes is the defect this contract exists to close, so the pool "
            "refuses to build rather than exclude the card unchecked."
            % accept["identity"])
    current = live_digests.get(accept["identity"])
    return {"accepted_digest": accept["canonical_card_digest"],
            "current_digest": current,
            "digest_match": current == accept["canonical_card_digest"],
            "review_id": accept["review_id"],
            "accepted_on": accept["date"],
            "repo_head_reviewed": accept["repo_head_reviewed"]}


def reopen_findings(ev, accept, state):
    """`(codes, reasons)` for a whole-card acceptance that no longer holds.

    The digest trigger is ADDITIONAL to the later-evidence trigger, never a
    replacement for it: a card whose bytes are untouched can still be reopened
    by evidence dated after the acceptance, and a card nobody has filed evidence
    against can still have been rewritten.
    """
    codes, reasons = [], []
    if state and not state["digest_match"]:
        if state["current_digest"] is None:
            codes.append(CARD_ABSENT)
            reasons.append(
                "the accepted card is no longer present in the corpus; "
                "acceptance %s of %s covered digest %s"
                % (state["review_id"], state["accepted_on"],
                   state["accepted_digest"]))
        else:
            codes.append(CARD_DIGEST_CHANGED)
            reasons.append(
                "%s: the card's canonical digest has moved since it was read - "
                "accepted %s, current %s (acceptance %s of %s). The prior "
                "whole-card acceptance no longer covers the current bytes; that "
                "is a statement about coverage, not about the card."
                % (CARD_DIGEST_CHANGED, state["accepted_digest"],
                   state["current_digest"], state["review_id"],
                   state["accepted_on"]))
    later = _reopen_reasons(ev, accept)
    if later:
        codes.append(LATER_EVIDENCE)
        reasons.extend(later)
    return codes, reasons


def _reopen_reasons(ev, accept):
    """Evidence dated strictly after an acceptance reopens that acceptance.

    Dates are ISO-8601 strings throughout the manifest corpus, so a string
    compare is a date compare - and stays deterministic.
    """
    if not accept or not accept.get("date"):
        return []
    since = accept["date"]
    reasons = []
    for m in ev["manifests"]:
        if m["date"] and m["date"] > since:
            reasons.append("%s (%s, %s) is dated after the %s acceptance of %s"
                           % (m["id"], m["kind"], m["date"],
                              accept["accept_scope"], since))
    return sorted(reasons)


#: The pool is the MEO Class 1 Oral bank: meoclass1/QB*.html question anchors.
#: Evidence also touches the SQ (Solved QP) series and non-question anchors such
#: as #dependency-graph. Those belong to other pools - but they are REPORTED,
#: never silently filtered, because an invisible filter cannot be distinguished
#: from a bug.
def scope_refusal(ident):
    """Return why this identity is out of scope, or None if it belongs here."""
    import re as _re

    path, anchor = ident
    root = path.split("/")[0]
    if root != QB_ROOT:
        return ("outside the Oral bank: %s/ is a different series (this pool is "
                "%s/ only)" % (root, QB_ROOT))
    if not _re.fullmatch(r"QB[0-9A-Za-z_]*\.html", path.split("/")[-1]):
        return "not a QB card file"
    if not _re.fullmatch(r"q\d+", anchor):
        return ("anchor %r is not a question anchor" % anchor)
    return None


def build_pool(docs, accepts, prose_hints=None, live_digests=None):
    """Build the canonical, deterministic review-pool payload.

    A card leaves the pool ONLY on a WHOLE_CARD acceptance whose pinned digest
    still matches the live card AND which later evidence has not reopened.
    Everything else - corrections, sweeps, prose hints - ranks it. Excluded
    cards are reported, never dropped silently.

    `live_digests` maps identity -> the card's current canonical digest. It is
    DATA, not a file read, so the rules here stay testable without a corpus. It
    may be omitted only when nothing in `accepts` could exclude; a WHOLE_CARD
    acceptance with no live digests supplied is a refusal, not a free pass.
    """
    prose_hints = prose_hints or {}
    evidence = collect_evidence(docs)

    cards, excluded, unknown, off_scope = [], [], [], []
    for ident in sorted(evidence):
        ev = evidence[ident]

        refusal = scope_refusal(ident)
        if refusal:
            off_scope.append({"identity": list(ident), "file": ident[0],
                              "anchor": ident[1],
                              "why_out_of_scope": refusal,
                              "correction_families": ev["correction_families"],
                              "changed_manifests": ev["manifests"]})
            continue

        accept = accepts.get(ident)
        state = digest_state(accept, live_digests)
        codes, reopen = (reopen_findings(ev, accept, state)
                         if accept and excludes(accept) else ([], []))
        hint = prose_hints.get(ident)

        signals = risk_signals(ev, bool(reopen), bool(hint) and not accept)
        score, components = score_card(signals)

        row = {
            "identity": list(ident),
            "file": ident[0],
            "anchor": ident[1],
            "question": ev["topics"][0] if ev["topics"] else None,
            "changed_manifests": ev["manifests"],
            "correction_families": ev["correction_families"],
            "classifications": ev["classifications"],
            "action_kinds": ev["action_kinds"],
            "origins": ev["origins"],
            "source_custody_signals": ev["source_custody_signals"],
            "accept_records": [accept] if accept else [],
            "digest_state": state,
            "reopen_codes": codes,
            "reopen_reasons": reopen,
            "risk_signals": signals,
            "risk_score": score,
            "score_components": components,
            "review_priority": review_priority(score),
            "prose_hint": hint,
        }

        if accept and excludes(accept) and not reopen:
            row["review_status"] = "EXPLICITLY_ACCEPTED"
            row["why_out"] = ("WHOLE_CARD acceptance: %s" % accept["evidence"])
            row["evidence"] = accept["evidence"]
            excluded.append(row)
            continue

        if reopen:
            row["review_status"] = "REOPENED"
        elif accept:
            row["review_status"] = "PARTIALLY_ACCEPTED_STILL_IN_POOL"
        elif hint:
            row["review_status"] = "UNKNOWN_MANUAL_ADJUDICATION"
        else:
            row["review_status"] = "IN_POOL"

        row["why_in_pool"] = _why_in(row)
        if row["review_status"] == "UNKNOWN_MANUAL_ADJUDICATION":
            unknown.append(row)
        # NOT an elif, and deliberately unconditional: a card surfaced for
        # manual adjudication is surfaced IN ADDITION to staying in the pool.
        # A prose hint has no exclusion authority, so it may not shorten this
        # list by one row.
        cards.append(row)

    # Deterministic order: score desc, then canonical identity.
    cards.sort(key=lambda c: (-c["risk_score"], c["file"], c["anchor"]))
    excluded.sort(key=lambda c: (c["file"], c["anchor"]))
    unknown.sort(key=lambda c: (-c["risk_score"], c["file"], c["anchor"]))
    off_scope.sort(key=lambda c: (c["file"], c["anchor"]))

    return {
        "schema": POOL_SCHEMA,
        "rule": "CORRECTED != REVIEWED. Only an explicit WHOLE_CARD entry in "
                "review_pool_accepts.json removes a card. Prose reviews rank, "
                "they never clear.",
        "summary": {
            "cards_in_pool": len(cards),
            "explicitly_accepted": len(excluded),
            "reopened": sum(1 for c in cards if c["review_status"] == "REOPENED"),
            "reopened_by_digest_change": sum(
                1 for c in cards if CARD_DIGEST_CHANGED in c["reopen_codes"]),
            "reopened_by_card_absent": sum(
                1 for c in cards if CARD_ABSENT in c["reopen_codes"]),
            "unknown_manual_adjudication": len(unknown),
            "out_of_scope": len(off_scope),
            "narrow_correction_only": sum(
                1 for c in cards if "NARROW_CORRECTION_ONLY" in c["risk_signals"]),
            "by_review_priority": {band: sum(
                1 for c in cards if c["review_priority"] == band)
                for _, band in REVIEW_PRIORITY_BANDS},
        },
        "cards": cards,
        "excluded": excluded,
        "unknown": unknown,
        "scope_excluded": off_scope,
    }


def _why_in(row):
    if row["review_status"] == "REOPENED":
        return ("reopened - %s" % row["reopen_reasons"][0])
    if row["review_status"] == "PARTIALLY_ACCEPTED_STILL_IN_POOL":
        return ("acceptance on record is %s, which is not a whole-card clearance"
                % row["accept_records"][0]["accept_scope"])
    if row["review_status"] == "UNKNOWN_MANUAL_ADJUDICATION":
        return ("a prose review mentions this card as untouched, but no "
                "adjudication entry exists - needs manual adjudication")
    if not row["risk_signals"]:
        return "no whole-card acceptance is on record"
    return "; ".join(SCORE_REASONS[s] for s in row["risk_signals"]
                     if SCORE_WEIGHTS[s] > 0) or "no whole-card acceptance is on record"


# --- serialisation and provenance ------------------------------------------

GENERATOR = "tools/oral/build_review_pool.py"
GENERATOR_VERSION = "1"


def canonical_json(payload):
    """The deterministic payload: sorted keys, fixed separators, UTF-8, newline.

    Nothing time-varying may enter this string - it is the thing whose bytes
    must match on a re-run.
    """
    import json
    return json.dumps(payload, sort_keys=True, ensure_ascii=False,
                      indent=1, separators=(",", ": ")) + "\n"


def content_hash(payload):
    import hashlib
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def build_document(pool, accepts_hash=None, generator_commit=None,
                   generated_at=None):
    """Wrap the canonical payload with provenance held strictly OUTSIDE it.

    A reader can re-derive `canonical` byte for byte; `provenance` is the
    non-canonical envelope, so an optional timestamp cannot break that.
    """
    prov = {"generator": GENERATOR,
            "generator_version": GENERATOR_VERSION,
            "generator_commit": generator_commit,
            "accepts_sha256": accepts_hash,
            "canonical_sha256": content_hash(pool)}
    if generated_at:
        prov["generated_at"] = generated_at
    return {"provenance": prov, "canonical": pool}


# --- the reviewer-facing report --------------------------------------------
# Rendered FROM the canonical payload. There is no second source of truth here,
# which is why report_counts() can be asserted against the payload it came from.

COUNT_LABELS = (("cards_in_pool", "Cards in pool"),
                ("explicitly_accepted", "Explicitly accepted (excluded)"),
                ("reopened", "Reopened"),
                ("unknown_manual_adjudication", "Unknown / manual adjudication"))


def _card_line(c):
    return ("- `%s#%s` — **%d** (%s) — %s"
            % (c["file"], c["anchor"], c["risk_score"],
               c["review_priority"], c["why_in_pool"]))


def render_markdown(pool):
    s = pool["summary"]
    out = ["# Oral QB review pool", "",
           "> %s" % pool["rule"], "",
           "Derived artefact. Regenerate it; do not edit it.", "",
           "## Summary", ""]
    for key, label in COUNT_LABELS:
        out.append("- %s: %d" % (label, s[key]))
    out.append("- Corrected only by narrow families: %d" % s["narrow_correction_only"])
    out.append("- Reopened because the card's bytes moved after acceptance: %d"
               % s["reopened_by_digest_change"])
    out.append("")
    out.append("| Review priority | Cards |")
    out.append("| --- | --- |")
    for _, band in REVIEW_PRIORITY_BANDS:
        out.append("| %s | %d |" % (band, s["by_review_priority"][band]))
    out.append("")
    out.append("R1..R4 is REVIEW priority - the order to read these cards in. "
               "It is **not a content-defect severity**: R1 says \"read this "
               "first\", never \"this card is wrong\". MIW's P0/P1/P2/P3 scale "
               "means something else entirely and is not used here.")

    def section(title, rows, empty):
        out.extend(["", "## %s" % title, ""])
        if not rows:
            out.append("_%s_" % empty)
            return
        out.extend(_card_line(c) for c in rows)

    section("Ranked review pool", pool["cards"], "Nothing in the pool.")
    section("Reopened",
            [c for c in pool["cards"] if c["review_status"] == "REOPENED"],
            "No acceptance has been reopened.")
    section("Corrected only by narrow families",
            [c for c in pool["cards"]
             if "NARROW_CORRECTION_ONLY" in c["risk_signals"]],
            "None.")
    section("Unknown / manual adjudication", pool["unknown"],
            "None awaiting adjudication.")

    out.extend(["", "## Explicitly accepted", ""])
    if not pool["excluded"]:
        out.append("_No card has a WHOLE_CARD acceptance on record._")
    else:
        for c in pool["excluded"]:
            st = c["digest_state"] or {}
            out.append("- `%s#%s` — out: %s" % (c["file"], c["anchor"], c["why_out"]))
            out.append("  - review `%s` on `%s`; accepted digest `%s`, current "
                       "`%s`, digest_match **%s**"
                       % (st.get("review_id"), st.get("repo_head_reviewed"),
                          st.get("accepted_digest"), st.get("current_digest"),
                          st.get("digest_match")))

    out.extend(["", "## Out of scope (reported, not reviewed here)", ""])
    if not pool["scope_excluded"]:
        out.append("_All evidence fell inside the Oral bank._")
    else:
        for c in pool["scope_excluded"]:
            out.append("- `%s#%s` — %s"
                       % (c["file"], c["anchor"], c["why_out_of_scope"]))
    out.append("")
    return "\n".join(out)


def report_counts(md):
    """Read the counts back OUT of the rendered report.

    This exists so a test can prove the prose and the payload agree, rather
    than assuming a renderer that was correct when it was written still is.
    """
    import re

    found = {}
    for key, label in COUNT_LABELS:
        m = re.search(r"^- %s: (\d+)$" % re.escape(label), md, re.M)
        if m:
            found[key] = int(m.group(1))
    return found


# --- prose hints (ADVISORY ONLY) -------------------------------------------
# These carry no exclusion authority whatsoever. They exist so a reviewer can
# see WHICH cards a prose review called untouched and decide, by hand, whether
# that amounts to a whole-card acceptance. Nothing here writes to the
# adjudication file, and nothing here is promoted automatically.

_ACCEPTISH = ("accepted card", "no change", "untouched", "verified - no change")
_NOT_ACCEPTISH = ("not fixed", "reported", "held back", "newly discovered")


def _hint_sections(text):
    """Yield (heading, body) for headings that read as an acceptance."""
    import re

    parts = re.split(r"^(#{2,4} .*)$", text, flags=re.M)
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        low = heading.lower()
        if any(bad in low for bad in _NOT_ACCEPTISH):
            continue
        body = parts[i + 1] if i + 1 < len(parts) else ""
        if any(good in low for good in _ACCEPTISH):
            yield heading, heading + "\n" + body


def extract_prose_hints(paths):
    """Map identity -> a citation string, for cards a prose review calls untouched."""
    import pathlib
    import re

    hints = {}
    for path in sorted(pathlib.Path(p) for p in paths):
        text = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
        for heading, chunk in _hint_sections(text):
            for name, anchor in re.findall(r"\b(QB[0-9A-Za-z_]*?)#(q\d+)\b", chunk):
                ident = ("%s/%s.html" % (QB_ROOT, name), anchor)
                hints.setdefault(ident, "%s :: %s" % (path.name, heading))
    return hints
