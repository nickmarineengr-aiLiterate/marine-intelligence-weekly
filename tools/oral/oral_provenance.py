"""Evidence provenance model for the Oral examiner intelligence.

Strong evidence cannot be established by changing a label. An evidence record
carries both what it claims (`evidence_tier`) and where it came from
(`source_type`, `source_id`). The tier is only as strong as the provenance
underneath it, so the two are validated against each other rather than the tier
being trusted on its own.

This closes the Laptop's mutation M5: relabelling a CURRENT_INDEX_RECOVERY
record as PRIMARY_TRACKER passed a 35-check validator, because nothing in it
ever looked at the axis re-tiering depends on.

Portability: no paths, no I/O. Import-only.
"""
from __future__ import annotations

# Evidence tiers the ledger may carry.
#
# NOTE_EXPLICIT is provisioned here for Phase 2A-ii, which will harvest explicit
# examiner cues from meoclass1/oralnotes/ ("Simon Sir typically asks ..."). It
# is defined now so the compatibility matrix already refuses to promote it. No
# Oral Note is read in Phase 2A-i.
EVIDENCE_TIERS = {
    "PRIMARY_TRACKER",
    "EXTERNAL_SURVEYOR_COMPILATION",
    "EXPLICIT_QCARD",
    "CE_TIP",
    "HEADER_METADATA",
    "CURRENT_INDEX_RECOVERY",
    "JULY_DERIVED_SIBLING",
    "TOPIC_INFERRED",
    "NOTE_EXPLICIT",
}

# What a record's provenance must be for the tier it claims. A tier admits only
# the source types listed against it; anything else is a promotion the evidence
# does not support.
#
# The rule that matters: PRIMARY_TRACKER admits ONLY provenance that actually
# points at the primary tracker structure. A derived surface (the published
# index, a July sheet), an inference (topic), a page assertion (CE tip) and an
# examiner cue in a Note are all real evidence of something - none of them is
# the tracker.
TIER_SOURCE_COMPATIBILITY = {
    "PRIMARY_TRACKER": {"PRIMARY_TRACKER", "MASTER_TRACKER"},
    "EXTERNAL_SURVEYOR_COMPILATION": {"EXTERNAL_SURVEYOR_COMPILATION",
                                      "ALL_SURVEYORS_COMPILATION"},
    "EXPLICIT_QCARD": {"EXPLICIT_QCARD", "QB_CARD_PROSE"},
    "CE_TIP": {"CE_TIP", "PAGE_PROSE_CE_TIP", "QB_CARD_PROSE"},
    "HEADER_METADATA": {"HEADER_METADATA", "QB_PAGE_HEADER"},
    "CURRENT_INDEX_RECOVERY": {"CURRENT_INDEX_RECOVERY"},
    "JULY_DERIVED_SIBLING": {"JULY_DERIVED_SIBLING", "JULY_EXAMINER_SHEET"},
    "TOPIC_INFERRED": {"TOPIC_INFERRED", "TOPIC_INFERENCE"},
    "NOTE_EXPLICIT": {"NOTE_EXPLICIT", "ORAL_NOTE_PAGE"},
}

# A tier that asserts the primary tracker must also point at it. The published
# index and the July sheets are derived products of the very relationships they
# would be used to confirm, so a record sourced from them can never carry a
# primary tier however it is labelled.
PRIMARY_TIERS = {"PRIMARY_TRACKER"}
DERIVED_SOURCE_TYPES = {"CURRENT_INDEX_RECOVERY", "JULY_DERIVED_SIBLING",
                        "JULY_EXAMINER_SHEET", "TOPIC_INFERRED",
                        "TOPIC_INFERENCE", "CE_TIP", "PAGE_PROSE_CE_TIP",
                        "NOTE_EXPLICIT", "ORAL_NOTE_PAGE"}


def incompatible(record):
    """Return a reason string when a record's tier outruns its provenance,
    or None when the record is self-consistent."""
    tier = record.get("evidence_tier")
    source = record.get("source_type")
    if tier not in EVIDENCE_TIERS:
        return "unknown evidence tier %r" % (tier,)
    if source is None:
        return "evidence tier %s carries no source_type to justify it" % tier
    if tier in PRIMARY_TIERS and source in DERIVED_SOURCE_TYPES:
        return "%s claimed on derived provenance %s" % (tier, source)
    allowed = TIER_SOURCE_COMPATIBILITY.get(tier)
    if allowed is not None and source not in allowed:
        return "evidence tier %s is not supported by source_type %s" % (tier, source)
    return None


def violations(records):
    """Every record whose claimed tier its provenance does not support,
    in a stable order."""
    out = []
    for r in sorted(records, key=lambda r: str(r.get("evidence_id", ""))):
        why = incompatible(r)
        if why:
            out.append((r.get("evidence_id"), why))
    return out
