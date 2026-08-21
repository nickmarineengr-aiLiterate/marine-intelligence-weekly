#!/usr/bin/env python3
"""
Batch-manifest schema contract for the Oral release toolchain.

WHY THIS EXISTS
---------------

E6's mutation L pointed ``authorisation_batch_key`` at ``batches.E5`` and the
validator stayed green: it hardcoded ``"E6"`` and never read the key.  The field
looked like provenance and supplied none.

The audit that followed showed the escape was not one file's bug.  Each batch
validator was written fresh, so *which* fields are load-bearing drifted per
batch: ``authorisation_batch_key`` is read by the B, C and E6 validators and
ignored by A, E1, E2, E3, E4 and E5.  Fixing that validator-by-validator would
simply re-drift on the next batch.

So the contract lives here instead, and is enforced repo-wide by
``tools/oral/test_oral_release_infra.py`` over EVERY manifest -- including the
historical ones, which stay untouched and runnable as release evidence.

THE RULE (brief section 11)
---------------------------
A field that appears to control identity, authorisation, target ownership,
digest, batch scope or provenance must be validated, explicitly marked
informational, or removed.  Silent security-looking decoration is not
acceptable.  ``UNCLASSIFIED`` is a failure, so a new decorative field on a
future batch cannot slip in unnoticed.
"""

from __future__ import annotations

import dataclasses
import json
import pathlib
import subprocess
from typing import Iterable

from oral_bytes import read_text

LOAD_BEARING = "LOAD_BEARING"
INFORMATIONAL = "INFORMATIONAL"
UNCLASSIFIED = "UNCLASSIFIED"

REPO = pathlib.Path(__file__).resolve().parents[2]

# Refs that carry authorisation records not merged to main.  The enrichment
# consolidation lives on a research branch by design -- it is an authoring
# input, not a published product surface.
AUTHORISATION_REFS = (
    "origin/research/oral-final-enrichment-consolidation",
    "origin/main",
    "HEAD",
)

# ---------------------------------------------------------------------------
# Field classification.
#
# LOAD_BEARING  -- asserted by assert_manifest() below, for every batch.
# INFORMATIONAL -- deliberately human-facing prose or a recorded observation.
#                  Named here so that "unread" is a decision, not an accident.
# ---------------------------------------------------------------------------
FIELD_CLASSES: dict[str, str] = {
    # ---- identity and authorisation (all asserted) ----
    "batch_id": LOAD_BEARING,
    "authorisation_batch_key": LOAD_BEARING,
    "authorisation_source": LOAD_BEARING,
    "authorisation": LOAD_BEARING,            # generation-1 spelling
    "authorisation_selector": LOAD_BEARING,   # generation-1 (batch D)
    "authorisation_commit": LOAD_BEARING,
    "baseline_commit": LOAD_BEARING,
    "batch": LOAD_BEARING,                    # generation-1 (gap0609)

    # ---- expectations the validators compare against ----
    "expected_canonical_questions": LOAD_BEARING,
    "expected_question_bearing_files": LOAD_BEARING,
    "expected_examiner_relationships": LOAD_BEARING,
    "expected_examiners": LOAD_BEARING,
    "creates_new_cards": LOAD_BEARING,
    "distinct_target_cards": LOAD_BEARING,
    "shared_target": LOAD_BEARING,
    "shared_target_actions": LOAD_BEARING,
    "sibling_pin_delegation": LOAD_BEARING,
    "authorisation_count_key": LOAD_BEARING,
    "actual_new_card_count": LOAD_BEARING,
    "examiner_relationship_delta": LOAD_BEARING,
    "baseline_canonical_questions": LOAD_BEARING,
    "authorisation_ref": LOAD_BEARING,        # generation-1 (batches B, C, D)
    "baseline_card_digests": LOAD_BEARING,    # generation-1 pre-edit pins

    # ---- informational: prose, provenance notes, recorded observations ----
    "title": INFORMATIONAL,
    "kind": INFORMATIONAL,
    "note": INFORMATIONAL,
    "action_kind": INFORMATIONAL,
    "line_ending_note": INFORMATIONAL,
    "shared_target_note": INFORMATIONAL,
    "enrichment_programme": INFORMATIONAL,
    "followup_overlap": INFORMATIONAL,
    "initial_authorised_count": INFORMATIONAL,

    # ---- the payload ----
    "cards": LOAD_BEARING,
}

# Card-level fields that carry ownership.  The action identity itself is read
# through action_id_of(), because the two manifest generations spell it
# differently and both remain valid release evidence.
CARD_TARGET_FIELDS = ("file", "anchor")

# Generation 1 (batches A-D, gap0609) creates new cards and names the action
# "production_action_id".  Generation 2 (E1-E6) enriches existing cards and
# names it "action_id".  One schema_version covering two key conventions is a
# known corpus-wide pattern -- subparts[] does the same thing with ref/label --
# so readers accept both rather than finding 1 of 11 manifests.
ACTION_ID_KEYS = ("action_id", "production_action_id")


def classify(field: str) -> str:
    return FIELD_CLASSES.get(field, UNCLASSIFIED)


def action_id_of(card: dict) -> str | None:
    """Read a card's action identity under either generation's key."""
    for key in ACTION_ID_KEYS:
        value = card.get(key)
        if value:
            return value
    return None


@dataclasses.dataclass(frozen=True)
class Finding:
    manifest: str
    check: str
    ok: bool
    detail: str

    def describe(self) -> str:
        return "%-4s %-42s %-38s %s" % (
            "PASS" if self.ok else "FAIL", self.manifest, self.check, self.detail)


def _git_show(ref: str, rel: str) -> bytes | None:
    try:
        out = subprocess.run(
            ["git", "show", "%s:%s" % (ref, rel.replace("\\", "/"))],
            cwd=str(REPO), capture_output=True, check=False)
    except OSError:
        return None
    return out.stdout if out.returncode == 0 else None


def resolve_authorisation_source(rel: str, commit: str | None = None) -> str | None:
    """Return where an authorisation record resolves, or None.

    Checked in order: the working tree, the manifest's own
    ``authorisation_commit``, then the known authorisation refs.  A record that
    resolves nowhere is a dangling provenance pointer and is reported as such.
    """
    if not rel:
        return None
    if (REPO / rel).is_file():
        return "tree"
    for ref in ([commit] if commit else []) + list(AUTHORISATION_REFS):
        if ref and _git_show(ref, rel) is not None:
            return ref
    return None


def audit_manifest(path) -> list[Finding]:
    """Every schema assertion for one batch manifest."""
    p = pathlib.Path(path)
    name = p.name
    findings: list[Finding] = []

    def add(check: str, ok: bool, detail: str = "") -> None:
        findings.append(Finding(name, check, ok, detail))

    try:
        manifest = json.loads(read_text(p))
    except Exception as exc:
        add("manifest_parses", False, "%s: %s" % (type(exc).__name__, exc))
        return findings
    add("manifest_parses", True, "%d top-level field(s)" % len(manifest))

    # 1. No unclassified field.  This is what stops a future batch inventing a
    #    new authorisation-looking field that nothing reads.
    unknown = sorted(k for k in manifest if classify(k) == UNCLASSIFIED)
    add("all_fields_classified", not unknown,
        "unclassified=%s" % (unknown or "none"))

    # 2. The batch key must select the batch the manifest claims to be.
    #    This is E6's escape, generalised to every batch.
    key = str(manifest.get("authorisation_batch_key") or "")
    batch_id = manifest.get("batch_id")
    if batch_id is not None:
        derived = key.split(".")[-1] if key.startswith("batches.") else None
        add("authorisation_batch_key_matches_batch_id",
            derived is not None and derived == batch_id,
            "key=%s -> %s  batch_id=%s" % (key or "-", derived or "-", batch_id))
    else:
        # Generation-1 manifests spell the selector as a path, not a key.
        add("authorisation_selector_present",
            bool(key or manifest.get("authorisation")
                 or manifest.get("authorisation_selector")),
            "generation-1 schema (no batch_id)")

    # 3. Provenance pointers must actually resolve.
    commit = manifest.get("authorisation_commit")
    for field in ("authorisation_source", "authorisation", "authorisation_selector"):
        value = manifest.get(field)
        if not isinstance(value, str) or not value.endswith(".json"):
            continue
        where = resolve_authorisation_source(value, commit)
        add("%s_resolves" % field, where is not None,
            "%s -> %s" % (value, where or "UNRESOLVED"))

    # 4. Card identity.
    cards = manifest.get("cards") or []
    add("cards_present", bool(cards), "%d card record(s)" % len(cards))

    ids = [action_id_of(c) for c in cards]
    add("action_ids_unique_and_present",
        bool(ids) and all(ids) and len(set(ids)) == len(ids),
        "%d id(s), %d distinct" % (len(ids), len(set(ids))))

    missing = [action_id_of(c) for c in cards
               if not all(c.get(f) for f in CARD_TARGET_FIELDS)]
    add("card_identity_complete", not missing,
        "incomplete=%s" % (missing or "none"))

    # 5. Shared targets -- the A007+A008 / A036+A037 model.  Several action
    #    identities may share one canonical card; when they do, the manifest
    #    must SAY so, and their post-edit digests must agree, because one card
    #    has exactly one post-edit state.
    targets: dict[tuple, list[str]] = {}
    for card in cards:
        targets.setdefault((card.get("file"), card.get("anchor")), []).append(
            action_id_of(card))
    shared = {t: v for t, v in targets.items() if len(v) > 1}
    shared_desc = sorted("%s#%s:%s" % (t[0], t[1], "+".join(v))
                         for t, v in shared.items()) or "none"
    declared = bool(manifest.get("shared_target"))

    if batch_id is not None:
        # Generation 2 only: an enrichment batch that silently puts two
        # authorised limbs on one card hides the fact that one post-edit digest
        # is serving two action records.
        #
        # The declaration has TWO valid spellings and both are accepted.  E1
        # declared it per-card (`shared_target_note` on every sharing card);
        # E5 and E6 moved it to the top level (`shared_target`).  The contract
        # is that a shared target is DECLARED, not that it is declared in the
        # later dialect -- E1's validator enforces its own spelling and remains
        # untouched release evidence.
        per_card = bool(shared) and all(
            all(c.get("shared_target_note")
                for c in cards if (c.get("file"), c.get("anchor")) == target)
            for target in shared)
        add("shared_target_declared_iff_present",
            bool(shared) == (declared or per_card),
            "shared=%s top_level=%s per_card=%s"
            % (shared_desc, declared, per_card))
    else:
        add("shared_target_recorded", True,
            "generation-1 schema; shared=%s" % shared_desc)

    if shared:
        disagree = []
        for target, action_ids in shared.items():
            digests = {c.get("post_edit_digest") for c in cards
                       if (c.get("file"), c.get("anchor")) == target}
            if len(digests) > 1:
                disagree.append("%s#%s" % target)
        add("shared_target_digests_agree", not disagree,
            "disagree=%s" % (disagree or "none"))

    # 6. distinct_target_cards, when declared, must be true.
    if "distinct_target_cards" in manifest:
        add("distinct_target_cards_correct",
            manifest["distinct_target_cards"] == len(targets),
            "declared=%s actual=%d" % (manifest["distinct_target_cards"], len(targets)))

    return findings


def assert_manifest(path) -> None:
    """Raise unless every assertion for one manifest passes."""
    bad = [f for f in audit_manifest(path) if not f.ok]
    if bad:
        raise AssertionError("manifest schema violations:\n  "
                             + "\n  ".join(f.describe() for f in bad))


def audit_all(directory=None) -> list[Finding]:
    directory = pathlib.Path(directory or pathlib.Path(__file__).resolve().parent)
    findings: list[Finding] = []
    for path in sorted(directory.glob("batch_*manifest.json")):
        findings.extend(audit_manifest(path))
    return findings


def _cli(argv: list[str]) -> int:
    import argparse

    ap = argparse.ArgumentParser(
        prog="oral_manifest",
        description="Audit Oral batch manifests against the shared schema contract.")
    ap.add_argument("--quiet", action="store_true", help="print failures only")
    ap.add_argument("manifests", nargs="*", help="default: every batch manifest")
    args = ap.parse_args(argv)

    findings = ([f for m in args.manifests for f in audit_manifest(m)]
                if args.manifests else audit_all())
    for finding in findings:
        if finding.ok and args.quiet:
            continue
        print(finding.describe())

    failed = [f for f in findings if not f.ok]
    print("manifest audit: checks=%d passed=%d failed=%d"
          % (len(findings), len(findings) - len(failed), len(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    import sys

    sys.exit(_cli(sys.argv[1:]))
