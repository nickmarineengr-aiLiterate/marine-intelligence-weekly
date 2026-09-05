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

This module is the library. tools/oral/build_review_pool.py is the CLI.
"""
from __future__ import annotations

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

ACCEPTS_SCHEMA = "miw-oral-review-pool-accepts/1"

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
    if doc.get("schema") != ACCEPTS_SCHEMA:
        raise PoolError("%s: schema is %r, expected %r"
                        % (path.name, doc.get("schema"), ACCEPTS_SCHEMA))

    entries = doc.get("accepts")
    if not isinstance(entries, list):
        raise PoolError("%s: 'accepts' must be a list" % path.name)

    out = {}
    for i, entry in enumerate(entries):
        where = "%s accepts[%d]" % (path.name, i)
        if not isinstance(entry, dict):
            raise PoolError("%s: entry is %s, not an object"
                            % (where, type(entry).__name__))

        ident = card_identity(entry, where)

        scope = _clean(entry.get("accept_scope"))
        if scope not in ACCEPT_SCOPES:
            raise PoolError("%s: accept_scope %r is not one of %s"
                            % (where, scope, sorted(ACCEPT_SCOPES)))

        if not _clean(entry.get("evidence")):
            raise PoolError("%s: 'evidence' is required - an acceptance without a "
                            "citation cannot be audited" % where)

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
                      "adjudicated_by": _clean(entry.get("adjudicated_by")) or None,
                      "date": _clean(entry.get("date")) or None}
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

PRIORITY_BANDS = ((70, "P1"), (45, "P2"), (25, "P3"), (0, "P4"))


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


def tranche_priority(score):
    for floor, band in PRIORITY_BANDS:
        if score >= floor:
            return band
    return "P4"


# --- the pool --------------------------------------------------------------

POOL_SCHEMA = "miw-oral-review-pool/1"


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


def build_pool(docs, accepts, prose_hints=None):
    """Build the canonical, deterministic review-pool payload.

    A card leaves the pool ONLY on a WHOLE_CARD acceptance that later evidence
    has not reopened. Everything else - corrections, sweeps, prose hints - ranks
    it. Excluded cards are reported, never dropped silently.
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
        reopen = _reopen_reasons(ev, accept) if accept and excludes(accept) else []
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
            "reopen_reasons": reopen,
            "risk_signals": signals,
            "risk_score": score,
            "score_components": components,
            "recommended_tranche_priority": tranche_priority(score),
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
            "unknown_manual_adjudication": len(unknown),
            "out_of_scope": len(off_scope),
            "narrow_correction_only": sum(
                1 for c in cards if "NARROW_CORRECTION_ONLY" in c["risk_signals"]),
            "by_priority": {band: sum(
                1 for c in cards if c["recommended_tranche_priority"] == band)
                for _, band in PRIORITY_BANDS},
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
               c["recommended_tranche_priority"], c["why_in_pool"]))


def render_markdown(pool):
    s = pool["summary"]
    out = ["# Oral QB review pool", "",
           "> %s" % pool["rule"], "",
           "Derived artefact. Regenerate it; do not edit it.", "",
           "## Summary", ""]
    for key, label in COUNT_LABELS:
        out.append("- %s: %d" % (label, s[key]))
    out.append("- Corrected only by narrow families: %d" % s["narrow_correction_only"])
    out.append("")
    out.append("| Priority | Cards |")
    out.append("| --- | --- |")
    for _, band in PRIORITY_BANDS:
        out.append("| %s | %d |" % (band, s["by_priority"][band]))

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
            out.append("- `%s#%s` — out: %s" % (c["file"], c["anchor"], c["why_out"]))

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
