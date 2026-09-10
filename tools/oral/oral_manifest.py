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

# The two record families that can authorise an edit to a card.
#
# A batch manifest authorises the cards its production/enrichment actions own.
# A correction manifest authorises cards edited AFTER a batch shipped -- the
# candidate-feedback repair path.  Both are read by every batch validator's
# "authorised elsewhere" scan through authorisation_manifest_paths() below, so
# a legitimate post-release correction stops reading as undeclared drift.
BATCH_MANIFEST_GLOB = "batch_*_manifest.json"
CORRECTION_MANIFEST_GLOB = "correction_*_manifest.json"

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
    # Actions a batch was authorised to produce and deliberately did NOT.
    #
    # A held action leaves no cards[] entry, so nothing else in the schema can
    # see it: an authorised action that is quietly dropped and an authorised
    # action that was never authorised look identical. Recording the hold as
    # STRUCTURE rather than as prose in `note` is what makes it assertable --
    # and it is asserted below, so it cannot become decoration.
    "held_actions": LOAD_BEARING,
    # The record that froze a batch's question IDENTITIES before any answer
    # was written. Batch G3 is the first to carry one. It is LOAD_BEARING
    # rather than a note because the reuse-first decision for each ask lives
    # there and nowhere else: without it, a manifest showing eleven new cards
    # cannot be distinguished from one where the bank was never searched.
    "freeze_record": LOAD_BEARING,
    # The mirror of held_actions: a LATER batch recording that it discharged an
    # EARLIER batch's hold.
    #
    # Without it, a hold is only ever closable by rewriting the manifest that
    # declared it -- which would make the holding batch's record a mutable
    # status board and destroy the one place that says the work was owed. So
    # the hold stays where it was declared, permanently true of that batch, and
    # the discharge is recorded here, in the batch that actually did the work.
    # "Is FUP-006 still owed?" is then answerable from repository data rather
    # than by arithmetic over handoffs.
    "discharges_hold": LOAD_BEARING,
    # A LIMB-level hold, which is NOT held_actions. held_actions says "this
    # action was authorised and was NOT produced"; held_limbs says "the action
    # WAS produced, and inside it one sub-claim could not be verified". H4 was
    # the first batch to need it: the India health-declaration card ships a
    # complete answer while declining to state a commencement date nobody could
    # find in the Gazette, and the MACN currency limb ships dated developments
    # while declining to name an annual-report year the issuer's own surfaces
    # disagreed about. Recording either as a held ACTION would have been false
    # -- the card exists -- and recording neither would have let an unverified
    # limb ship silently, which is the failure this whole file exists to stop.
    "held_limbs": LOAD_BEARING,
    # A limb this batch DECLARED as held and then resolved before shipping.
    # Load-bearing because deleting a hold silently and recording its dissolution
    # are the same edit to the reader, and only one of them is honest: H4 held
    # the MACN annual-report limb, independent review found the issuer's
    # publications index settled it, and the record has to show that the hold was
    # WRONG rather than that it never existed.
    "dissolved_holds": LOAD_BEARING,
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
    # Why a LIVE expectation was refreshed. The number itself stays
    # LOAD_BEARING; this records the governed change that moved it, so a
    # refresh can never look like a quiet rebaseline.
    "expected_examiner_relationships_note": INFORMATIONAL,
    # Why a batch's post-edit digests were refreshed after publication of the
    # manifest -- e.g. an independent review that changed card content. Prose,
    # so INFORMATIONAL; the digests themselves stay LOAD_BEARING and are
    # compared against the live pages regardless of what this says.
    "review_round_note": INFORMATIONAL,
    # Why an examiner-relationship delta is what it is. The delta itself stays
    # LOAD_BEARING; this only records the reasoning.
    "examiner_relationship_delta_note": INFORMATIONAL,

    # ---- the payload ----
    "cards": LOAD_BEARING,
}

# Card-level fields that carry ownership.  The action identity itself is read
# through action_id_of(), because the two manifest generations spell it
# differently and both remain valid release evidence.
CARD_TARGET_FIELDS = ("file", "anchor")

# Why an authorised action was NOT produced. Deliberately small, and
# deliberately not overlapping the register's own dispositions: a hold says
# "authorised, still authorised, blocked" and is NOT the same claim as
# RETARGET_REQUIRED (the parent is wrong), ALREADY_COVERED (the limb is there)
# or a withdrawal (it should never have been authorised). Recording a hold as
# any of those would erase the fact that the work is still owed.
HELD_STATUSES = (
    "HELD_GOVERNANCE",   # blocked by the authorisation/guard contract itself
    "HELD_AUTHORITY",    # blocked by unresolved primary authority
    "HELD_TARGET",       # blocked by unresolved target adjudication
)

# Why a LIMB inside a produced card is unverified. Separate vocabulary from
# HELD_STATUSES on purpose: those describe why work was NOT DONE, these
# describe a bounded gap inside work that WAS done and shipped.
HELD_LIMB_STATUSES = (
    "HOLD_CURRENTNESS_UNVERIFIED",   # the fact perishes and could not be dated
    "HOLD_IDENTITY_UNRESOLVED",      # the thing named could not be pinned down
    "HOLD_SOURCE_AUTHORITY_LIMITED", # the authority exists but could not be read
)

# Generation 1 (batches A-D, gap0609) creates new cards and names the action
# "production_action_id".  Generation 2 (E1-E6) enriches existing cards and
# names it "action_id".  One schema_version covering two key conventions is a
# known corpus-wide pattern -- subparts[] does the same thing with ref/label --
# so readers accept both rather than finding 1 of 11 manifests.
ACTION_ID_KEYS = ("action_id", "production_action_id", "correction_action_id")


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


# ---------------------------------------------------------------------------
# POST-RELEASE CORRECTION RECORDS
#
# WHY A SECOND RECORD FAMILY EXISTS
# ---------------------------------
# A batch manifest answers "which cards did this production run create or
# enrich?".  It cannot answer "which cards were repaired after that run
# shipped?", because a batch closes the moment it publishes and its digests are
# release evidence that must not be rebaselined.
#
# Candidate feedback arrives after publication by definition.  When the
# fair-treatment repair landed as two ordinary commits, seven of eleven batch
# validators went red -- correctly.  Every one of them asks the same question,
# "is this card owned by some authorised record?", and the answer was no,
# because no record existed that COULD own a post-release edit.
#
# So corrections get their own record family rather than being back-dated into
# a batch they never belonged to.  Delegation is shared: batch and correction
# manifests are unioned by authorisation_manifest_paths(), which every batch
# validator's sibling scan reads.  Ownership is anchor-level, matching the
# existing contract exactly.
#
# Anchor-level ownership ALONE would exempt a corrected card forever, so the
# post-correction state is additionally pinned per card and checked against the
# live pages by tools/oral/validate_corrections.py.  Delegation says "this card
# was legitimately edited"; the pin says "and it is still exactly what was
# authorised".  Neither check subsumes the other.
# ---------------------------------------------------------------------------

CORRECTION_KIND = "POST_RELEASE_CORRECTION"

# Why a declared card changed.  A correction event may legitimately carry more
# than one semantic correction -- the scope pass that follows a candidate report
# is how sibling defects get found -- but each card must say which it was, so
# "it shipped in the same commit" never stands in for "it is the same fix".
CORRECTION_CLASSES = (
    "PRIMARY_CORRECTION",          # the card the candidate actually reported
    "DEPENDENCY_CORRECTION",       # changed because the primary card changed
    "PROPAGATED_FACT_CORRECTION",  # same fact, wrong in another card too
    "SCOPE_PASS_CORRECTION",       # independent defect found by the same sweep
    "TEASER_SYNC",                 # free surface realigned to a correct gated copy
    "INDEX_METADATA",              # derived index / metadata only
)

CORRECTION_STATUSES = ("AUTHORISED", "SUPERSEDED")

CORRECTION_FIELD_CLASSES: dict[str, str] = {
    # ---- identity and authorisation (all asserted) ----
    "correction_id": LOAD_BEARING,
    "kind": LOAD_BEARING,
    "status": LOAD_BEARING,
    "origin": LOAD_BEARING,
    "governing_commits": LOAD_BEARING,
    "baseline_commit": LOAD_BEARING,
    "authorisation_source": LOAD_BEARING,
    "cards": LOAD_BEARING,
    # Candidate-facing pages this correction edited that carry no q-card, and
    # so cannot be expressed in cards[] at all. See GOVERNED_ARTEFACT_FIELDS
    # below for why this is a second collection rather than a digest bolted
    # onto the INFORMATIONAL `artefacts` list.
    "governed_artefacts": LOAD_BEARING,

    # ---- informational ----
    "title": INFORMATIONAL,
    "date": INFORMATIONAL,
    "rationale": INFORMATIONAL,
    "note": INFORMATIONAL,
    "known_traps_entries": INFORMATIONAL,
    "content_index_effect": INFORMATIONAL,
    # Files this correction touched that carry no q-card and that no release
    # guard pins.  Recorded so the event's scope is complete; deliberately
    # carrying NO digest, because a pin nothing reads is exactly the decoration
    # this schema exists to forbid, and a pin on an unguarded file would expire
    # on the next unrelated edit to it.
    "artefacts": INFORMATIONAL,

    # ---- candidate-reported corrections ----
    # Added for CORR-CSM-BOILER-SURVEY-20260823. Each of these is asserted by
    # that correction's own content validator, which is the only reason they
    # are allowed in: this table is a closed set so that a record cannot grow
    # decorative fields nothing reads, and a field no validator touches is
    # exactly that decoration. `known_traps_entries` is the precedent -- it is
    # INFORMATIONAL here and still asserted by validate_corrections.py.
    #   candidate_claim    what was reported, in the reporter's own words
    #   candidate_verdict  CORRECT / PARTLY_CORRECT / INCORRECT
    #   authority          the rule text that decided it, with clause numbers
    #   propagation        every other occurrence found, and its disposition
    #   invariants         what the correction asserts it did NOT change
    "candidate_claim": INFORMATIONAL,
    "candidate_verdict": INFORMATIONAL,
    "authority": INFORMATIONAL,
    "propagation": INFORMATIONAL,
    "invariants": INFORMATIONAL,
    # Added for CORR-G1-010-RORO-ATTRIBUTION-20260825, on the same terms as the
    # candidate-reported block above: it is allowed in because that correction's
    # own content validator ASSERTS it. A correction to published regulatory
    # content is only authorised once an independent reader who never saw the
    # producing reasoning has passed it, and that fact has to live in the record
    # rather than in a commit message, because the commit message is not
    # something any gate can read. Recording the pass COUNT and each pass's
    # verdict matters as much as the final verdict: G1-010's second pass caught
    # a material defect the first round of fixes had introduced, so a record
    # showing only "reviewed: PASS" would hide the reason the second pass is
    # mandatory rather than optional.
    "review": INFORMATIONAL,
    # Added for CORR-P1REPAIR-20260906, on the same terms as every field above:
    # it is allowed in ONLY because that correction's own content gate asserts
    # it (`record_does_not_rewrite_pass1_history`). A repair layer has to say
    # which earlier CLAIMS it falsifies, separately from which digests it
    # supersedes - `supersedes` answers "does my state descend from yours?",
    # and this answers "and what did you assert that was not true?". Without
    # somewhere to record that, the only way to correct a false claim in a
    # shipped record would be to edit the record, which destroys the evidence
    # of how the escape happened.
    "supersedes_summary": INFORMATIONAL,
    # Added for CORR-ITC51-20260908, on the same terms as every field above: it
    # is allowed in ONLY because that correction's own content gate asserts it
    # (`record_states_candidate_introduced_status`). A defect that this
    # unreleased candidate INTRODUCED and a defect it merely INHERITED are the
    # same text on disk and completely different release decisions - the first
    # cannot ship, the second is pre-existing debt that shipping does not make
    # worse. Nothing in the schema could express that difference, so the
    # question was being answered in prose in a report nobody's gate reads.
    "candidate_introduced": INFORMATIONAL,
}

CORRECTION_CARD_FIELDS = ("file", "path", "anchor",
                          "pre_edit_digest", "post_edit_digest",
                          "classification")

# ---------------------------------------------------------------------------
# GOVERNED NON-CARD ARTEFACTS
#
# WHY A THIRD COLLECTION, AND NOT A CARD OR AN `artefacts` ENTRY
# -------------------------------------------------------------
# CORR-REL-BJ-ATTRIBUTION and CORR-REL-BJ-FOUNDERING removed a settled cause
# for the loss of `Bulk Jupiter` from three q-cards.  `QB2_B_CheatSheet.html`
# stated the same rejected proposition and was not corrected with them, because
# nothing in this schema could own it:
#
#   cards[]      requires `anchor`, and every downstream reader -- the batch
#                guards' sibling scan, `card_digests`, the supersession
#                resolver -- is keyed on "file#anchor".  A cheat sheet has no
#                balanced card block, so a synthetic anchor would not merely be
#                cosmetic: it would enter the ownership map and start exempting
#                a name that does not exist from eleven historical guards.
#
#   artefacts[]  is INFORMATIONAL and deliberately carries NO digest, for the
#                reason stated on the field above -- a pin nothing reads is the
#                decoration this schema exists to forbid.  It records tooling
#                that shipped with a correction.  It is not, and must not
#                become, a claim about candidate-facing content.
#
# So the artefact form is its own collection with its own required fields, and
# its pins are read by tools/oral/validate_corrections.py against the live
# page.  A card record and an artefact record are different shapes answering
# different questions, and `governed_artefact_is_not_a_card` below asserts that
# neither can be spelled as the other.
#
# THE PIN IS WHOLE-FILE.  There is no anchor to scope it to, so any later edit
# to a governed artefact -- including one that has nothing to do with this
# correction -- fails this record until a new record declares it.  That is
# stricter than card-level pinning, not weaker, and it is the correct default
# for a page a candidate reads on the morning of the oral.
# ---------------------------------------------------------------------------

# Why a governed artefact changed.  ARTEFACT_PROPAGATION is deliberately the
# only member: an artefact-level record exists to carry an ALREADY-ADJUDICATED
# proposition onto a surface the parent correction missed.  A first-instance
# factual finding belongs in a card record with its own authority block, and
# widening this tuple is how that distinction would quietly be lost.
GOVERNED_ARTEFACT_CLASSES = ("ARTEFACT_PROPAGATION",)

# The surface families that exist in this corpus and carry no q-card.
GOVERNED_ARTEFACT_TYPES = ("CHEAT_SHEET", "NOTES_PAGE", "INDEX_PAGE", "HUB_PAGE")

GOVERNED_ARTEFACT_FIELDS = ("correction_action_id", "path", "artefact_type",
                            "classification", "proposition",
                            "proposition_markers", "expected_text_after",
                            "pre_edit_digest", "post_edit_digest",
                            "governing_correction", "propagation_reason")


def artefact_digest(text: str) -> str:
    """sha256 of a whole non-card file, LF-normalised.

    Same normalisation as `card_digests`, and for the same reason: the pages
    are LF in the object store while the working tree may hold CRLF, so a
    digest over raw bytes would drift on checkout rather than on an edit.
    """
    import hashlib

    return hashlib.sha256(
        text.replace("\r\n", "\n").encode("utf-8")).hexdigest()

_HEX64 = frozenset("0123456789abcdef")


def classify_correction(field: str) -> str:
    return CORRECTION_FIELD_CLASSES.get(field, UNCLASSIFIED)


def is_correction_manifest(path) -> bool:
    return pathlib.Path(path).name.startswith("correction_")


def sibling_owned_cards(manifest_path, directory=None) -> set:
    """Every "file#anchor" that some OTHER authorisation record owns.

    Batch guards ask two different questions of a card that moved: "did I
    authorise it?" and, failing that, "did anyone?".  The second question is
    what stops a guard expiring the moment a later batch legitimately touches
    a file this one also touched.

    E1 built that exemption for EDITED cards but deliberately excluded ADDED
    ones, on the assumption that no later batch would add a card to a file an
    enrichment batch had touched.  Batch G1 added four, and every E- and F-
    series guard went red at once - not because anything was wrong, but because
    "no card was added since my baseline" is a claim that stops being true the
    first time the bank grows.  The claim a batch can actually make forever is
    "no card was added since my baseline that nobody authorised", and this
    helper is what lets each guard say that instead.
    """
    owned = set()
    for path in authorisation_manifest_paths(directory or pathlib.Path(manifest_path).parent,
                                             exclude=manifest_path):
        try:
            record = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for card in record.get("cards", []):
            if card.get("file") and card.get("anchor"):
                owned.add("%s#%s" % (card["file"], card["anchor"]))
    return owned


def authorisation_manifest_paths(directory=None, exclude=None) -> tuple:
    """Every record that may authorise an edit to a card: batch and correction.

    This is the single definition of the "authorised elsewhere" surface.  It
    exists as one function because ten batch validators each grew their own
    copy of the sibling glob, and widening that surface in ten places is how
    the two families drift apart again."""
    directory = pathlib.Path(directory or pathlib.Path(__file__).resolve().parent)
    exclude = pathlib.Path(exclude).resolve() if exclude else None
    paths = []
    for pattern in (BATCH_MANIFEST_GLOB, CORRECTION_MANIFEST_GLOB):
        for path in directory.glob(pattern):
            if exclude is not None and path.resolve() == exclude:
                continue
            paths.append(path)
    return tuple(sorted(paths))


def _commit_exists(sha: str) -> bool:
    try:
        out = subprocess.run(["git", "cat-file", "-t", sha],
                             cwd=str(REPO), capture_output=True, check=False)
    except OSError:
        return False
    return out.returncode == 0 and out.stdout.strip() == b"commit"


def _is_digest(value) -> bool:
    return (isinstance(value, str) and len(value) == 64
            and all(c in _HEX64 for c in value))


def audit_correction_manifest(path) -> list[Finding]:
    """Every schema assertion for one post-release correction manifest."""
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

    unknown = sorted(k for k in manifest if classify_correction(k) == UNCLASSIFIED)
    add("all_fields_classified", not unknown,
        "unclassified=%s" % (unknown or "none"))

    add("kind_is_correction", manifest.get("kind") == CORRECTION_KIND,
        "kind=%s" % manifest.get("kind"))

    cid = manifest.get("correction_id") or ""
    add("correction_id_present", bool(cid), "correction_id=%s" % (cid or "-"))

    # The filename must carry the identity.  A record whose id and filename
    # disagree is two records as far as any human reader is concerned, and the
    # sibling scan finds records by NAME.
    slug = cid.lower().replace("-", "_")
    expected = "correction_%s_manifest.json" % slug
    add("correction_id_matches_filename", bool(cid) and name == expected,
        "%s vs expected %s" % (name, expected if cid else "correction_<id>_manifest.json"))

    add("status_known", manifest.get("status") in CORRECTION_STATUSES,
        "status=%s" % manifest.get("status"))
    add("origin_present", bool(manifest.get("origin")),
        "origin=%s" % manifest.get("origin"))

    commits = manifest.get("governing_commits") or []
    add("governing_commits_present", bool(commits), "%d commit(s)" % len(commits))
    dangling = [c for c in commits if not _commit_exists(c)]
    add("governing_commits_resolve", not dangling,
        "dangling=%s" % (dangling or "none"))

    base = manifest.get("baseline_commit")
    add("baseline_commit_resolves", bool(base) and _commit_exists(base),
        "baseline_commit=%s" % (base or "-"))

    src = manifest.get("authorisation_source")
    if isinstance(src, str) and src.endswith((".md", ".json")):
        where = resolve_authorisation_source(src)
        add("authorisation_source_resolves", where is not None,
            "%s -> %s" % (src, where or "UNRESOLVED"))
    else:
        add("authorisation_source_present", bool(src),
            "authorisation_source=%s" % (src or "-"))

    cards = manifest.get("cards") or []
    artefacts = manifest.get("governed_artefacts")

    # An artefact-only record has an empty cards[] by construction, so
    # `cards_present` cannot simply be relaxed: doing that globally would let a
    # CARD correction ship declaring nothing at all. The relaxation is
    # conditional on the record actually declaring governed artefacts, and the
    # historical records -- none of which carry the key -- keep the original
    # check under the original name, unchanged, as release evidence.
    if artefacts is None:
        add("cards_present", bool(cards), "%d card record(s)" % len(cards))
    else:
        add("card_or_artefact_target_present", bool(cards) or bool(artefacts),
            "%d card record(s), %d governed artefact(s)"
            % (len(cards), len(artefacts)))

    ids = [action_id_of(c) for c in cards]
    add("action_ids_unique_and_present",
        (all(ids) and len(set(ids)) == len(ids)) if artefacts
        else (bool(ids) and all(ids) and len(set(ids)) == len(ids)),
        "%d id(s), %d distinct" % (len(ids), len(set(ids))))

    incomplete = [action_id_of(c) or "?" for c in cards
                  if not all(c.get(f) for f in CORRECTION_CARD_FIELDS)]
    add("card_identity_complete", not incomplete,
        "incomplete=%s" % (incomplete or "none"))

    # `file` is the bare page name the batch validators key their
    # authorised-elsewhere map on; `path` is repo-relative and is what the
    # correction validator opens.  They must describe the same page.
    mismatched = ["%s: %s vs %s" % (action_id_of(c), c.get("path"), c.get("file"))
                  for c in cards
                  if c.get("path") and c.get("file")
                  and str(c["path"]).rsplit("/", 1)[-1] != c["file"]]
    add("card_path_matches_file", not mismatched,
        "mismatched=%s" % (mismatched or "none"))

    bad_digest = [action_id_of(c) or "?" for c in cards
                  if not (_is_digest(c.get("pre_edit_digest"))
                          and _is_digest(c.get("post_edit_digest")))]
    add("card_digests_well_formed", not bad_digest,
        "malformed=%s" % (bad_digest or "none"))

    # A correction that does not change the card is not a correction.
    inert = [action_id_of(c) or "?" for c in cards
             if c.get("pre_edit_digest") == c.get("post_edit_digest")]
    add("card_digests_differ", not inert, "inert=%s" % (inert or "none"))

    bad_class = ["%s=%s" % (action_id_of(c), c.get("classification"))
                 for c in cards
                 if c.get("classification") not in CORRECTION_CLASSES]
    add("card_classifications_known", not bad_class,
        "unknown=%s" % (bad_class or "none"))

    # Exactly one card is the reported defect.  Zero means the record has lost
    # its origin; more than one means two events were merged into one record.
    #
    # An artefact-only propagation record is the one shape where zero is
    # correct: the reported defect lives in the PARENT record, which is named
    # per artefact and asserted to exist by
    # `governed_artefact_parent_exists` and
    # `governed_artefact_parent_states_the_proposition`. Those two are where
    # the origin requirement is actually enforced for this shape.
    #
    # An earlier cut of this branch emitted
    # `artefact_only_record_claims_no_primary` here instead. Mutation GI showed
    # it could not fail: with `cards` empty `primary` is empty by
    # construction, and adding a card to make it non-empty routes the record to
    # the other branch. A check that cannot go red is the decoration this
    # module exists to forbid, so it is not emitted rather than left standing
    # as a reassuring PASS. A MIXED record -- cards AND artefacts -- still
    # takes the card assertion below, unchanged.
    primary = [action_id_of(c) for c in cards
               if c.get("classification") == "PRIMARY_CORRECTION"]
    if not (artefacts and not cards):
        add("exactly_one_primary_correction", len(primary) == 1,
            "primary=%s" % (primary or "none"))

    # Two copies of one card (gated + free) must agree on their post state.
    targets: dict[tuple, set] = {}
    for card in cards:
        targets.setdefault((card.get("file"), card.get("anchor")), set()).add(
            card.get("post_edit_digest"))
    disagree = sorted("%s#%s" % t for t, d in targets.items() if len(d) > 1)
    add("mirrored_cards_agree", not disagree, "disagree=%s" % (disagree or "none"))

    # 5d. GOVERNED NON-CARD ARTEFACTS.
    #
    # Every assertion here is the artefact-form equivalent of one the card form
    # already makes, plus the two only the artefact form needs: that it cannot
    # be spelled as a card, and that it names a parent whose proposition it is
    # actually carrying.
    if artefacts is not None:
        # (A) A record that declares the key and then declares nothing is a
        #     governance no-op that would otherwise pass every other check.
        add("governed_artefacts_non_empty", bool(artefacts),
            "%d artefact(s)" % len(artefacts))

        malformed = [str(a.get("correction_action_id") or "?") for a in artefacts
                     if not (isinstance(a, dict)
                             and all(a.get(f) for f in GOVERNED_ARTEFACT_FIELDS))]
        add("governed_artefact_identity_complete", not malformed,
            "incomplete=%s" % (malformed or "none"))

        aids = [a.get("correction_action_id") for a in artefacts
                if isinstance(a, dict)]
        card_ids = {action_id_of(c) for c in cards}
        add("governed_artefact_ids_unique_and_present",
            bool(aids) and all(aids) and len(set(aids)) == len(aids)
            and not (set(aids) & card_ids),
            "%d id(s), %d distinct, collides_with_cards=%s"
            % (len(aids), len(set(aids)), sorted(set(aids) & card_ids) or "none"))

        bad_type = ["%s=%s" % (a.get("correction_action_id"), a.get("artefact_type"))
                    for a in artefacts
                    if a.get("artefact_type") not in GOVERNED_ARTEFACT_TYPES]
        add("governed_artefact_type_governed", not bad_type,
            "unknown=%s" % (bad_type or "none"))

        bad_class = ["%s=%s" % (a.get("correction_action_id"), a.get("classification"))
                     for a in artefacts
                     if a.get("classification") not in GOVERNED_ARTEFACT_CLASSES]
        add("governed_artefact_classification_governed", not bad_class,
            "unknown=%s" % (bad_class or "none"))

        # (F) An artefact record must not impersonate a q-card one. `anchor`
        #     and `file` are the two keys every ownership reader in this
        #     toolchain looks for, so carrying either would put a page with no
        #     card block into the anchor-ownership map -- exactly the
        #     fake-anchor outcome this design exists to avoid.
        impersonating = [str(a.get("correction_action_id") or "?") for a in artefacts
                         if isinstance(a, dict) and ("anchor" in a or "file" in a)]
        add("governed_artefact_is_not_a_card", not impersonating,
            "carrying_card_keys=%s" % (impersonating or "none"))

        # (C) Well-formed and distinct. A propagation that changed no bytes is
        #     not a propagation.
        bad_digest = [str(a.get("correction_action_id") or "?") for a in artefacts
                      if not (_is_digest(a.get("pre_edit_digest"))
                              and _is_digest(a.get("post_edit_digest")))]
        add("governed_artefact_digests_well_formed", not bad_digest,
            "malformed=%s" % (bad_digest or "none"))

        inert = [str(a.get("correction_action_id") or "?") for a in artefacts
                 if a.get("pre_edit_digest") == a.get("post_edit_digest")]
        add("governed_artefact_digests_differ", not inert,
            "inert=%s" % (inert or "none"))

        # (B) The path must resolve to a real file in this repository.
        gone = [str(a.get("path")) for a in artefacts
                if not (REPO / str(a.get("path") or "")).is_file()]
        add("governed_artefact_path_exists", not gone,
            "missing=%s" % (gone or "none"))

        # (D) and (E). The parent must exist as a correction record on disk,
        #     must not be this record, and must itself carry the proposition
        #     being propagated -- otherwise "propagation" is a word a record
        #     could assert about a finding no earlier record ever made, which
        #     is a first-instance correction wearing a propagation label.
        unbacked, disagreeing = [], []
        for a in artefacts:
            parent_id = str(a.get("governing_correction") or "")
            aid = str(a.get("correction_action_id") or "?")
            parent_path = p.parent / ("correction_%s_manifest.json"
                                      % parent_id.lower().replace("-", "_"))
            if not parent_id or parent_id == cid or not parent_path.is_file():
                unbacked.append("%s -> %s" % (aid, parent_id or "-"))
                continue
            parent_text = read_text(parent_path)
            absent = [m for m in (a.get("proposition_markers") or [])
                      if m not in parent_text]
            if absent:
                disagreeing.append("%s: parent lacks %s" % (aid, absent))
        add("governed_artefact_parent_exists", not unbacked,
            "unbacked=%s" % (unbacked or "none"))
        add("governed_artefact_parent_states_the_proposition", not disagreeing,
            "disagreeing=%s" % (disagreeing or "none"))

    return findings


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

    # 5b. Held actions -- authorised, deliberately not produced.
    #
    # The failure mode this catches is a batch quietly narrowing its own scope.
    # A held action has no cards[] entry, so without a structured record there
    # is nothing to compare a later audit against, and "we were never asked to
    # do it" becomes indistinguishable from "we decided not to and said so".
    #
    # A hold must therefore name itself, say WHY in a governed status, and
    # carry a blocker a reader can act on. It must also NOT appear in cards[],
    # because an action cannot be both held and produced.
    held = manifest.get("held_actions")
    if held is not None:
        produced = {action_id_of(c) for c in cards}
        bad_shape = [h.get("followup_id") or "?" for h in held
                     if not (isinstance(h, dict) and h.get("followup_id")
                             and h.get("target") and h.get("blocker"))]
        add("held_actions_well_formed", not bad_shape,
            "malformed=%s" % (bad_shape or "none"))

        bad_status = ["%s=%s" % (h.get("followup_id"), h.get("status"))
                      for h in held if h.get("status") not in HELD_STATUSES]
        add("held_action_status_governed", not bad_status,
            "unknown=%s" % (bad_status or "none"))

        both = sorted(h.get("followup_id") for h in held
                      if h.get("followup_id") in produced)
        add("held_actions_are_not_also_produced", not both,
            "both=%s" % (both or "none"))

    # 5b-ii. Limb-level holds. The asymmetry with held_actions is the whole
    # point and is asserted, not assumed: a held ACTION must NOT appear in
    # cards[], whereas a held LIMB MUST name an action that cards[] actually
    # produced. Without that second assertion held_limbs would be a way to
    # declare a hold on work that was never done -- the softer-sounding word
    # doing the job the governed vocabulary refuses to do.
    held_limbs = manifest.get("held_limbs")
    if held_limbs is not None:
        produced_ids = {action_id_of(c) for c in cards}
        bad_shape = [h.get("held_limb_id") or "?" for h in held_limbs
                     if not (isinstance(h, dict) and h.get("held_limb_id")
                             and h.get("target") and h.get("exact_unknown")
                             and h.get("evidence_needed"))]
        add("held_limbs_well_formed", not bad_shape,
            "malformed=%s" % (bad_shape or "none"))

        bad_status = ["%s=%s" % (h.get("held_limb_id"), h.get("status"))
                      for h in held_limbs
                      if h.get("status") not in HELD_LIMB_STATUSES]
        add("held_limb_status_governed", not bad_status,
            "unknown=%s" % (bad_status or "none"))

        orphan = sorted(h.get("held_limb_id") for h in held_limbs
                        if h.get("action_id") not in produced_ids)
        add("held_limbs_belong_to_a_produced_action", not orphan,
            "orphan=%s" % (orphan or "none"))

        # An independent review demonstrated three escapes in the first cut of
        # this mechanism, and all three had the same shape: a field the record
        # asserts and no code contradicts. They are closed here.
        #
        # (a) TARGET CORRESPONDENCE. `target` was checked for presence only, so
        #     a hold could name action H4-003 and point at a card that action
        #     never touched -- which reads as a disclosure while describing the
        #     wrong page.
        by_id = {action_id_of(c): c for c in cards}
        mismatched = []
        for h in held_limbs:
            card = by_id.get(h.get("action_id"))
            if not card:
                continue                      # already reported as an orphan
            want = "%s#%s" % (card.get("file"), card.get("anchor"))
            if (h.get("target") or "").strip() != want:
                mismatched.append("%s->%s(want %s)"
                                  % (h.get("held_limb_id"), h.get("target"), want))
        add("held_limb_target_matches_its_action", not mismatched,
            "mismatched=%s" % (mismatched or "none"))

        # (b) THE OWED FLAG. `held_actions` has a dedicated mutation for exactly
        #     this laundering -- "mark the work no longer owed" -- and the limb
        #     form inherited none. A limb whose work is not owed is not held; it
        #     is resolved, and the record should say so by removing the entry,
        #     not by flipping a boolean inside one.
        not_owed = sorted(h.get("held_limb_id") for h in held_limbs
                          if h.get("work_still_owed") is not True)
        add("held_limb_work_is_still_owed", not not_owed,
            "not_owed=%s" % (not_owed or "none"))

        # (c) INTERNAL AGREEMENT. `held_limbs_belong_to_a_produced_action` has
        #     already established that a card exists, so a record claiming
        #     otherwise contradicts a check that passed in the same run.
        contra = sorted(h.get("held_limb_id") for h in held_limbs
                        if h.get("candidate_facing_card_produced") is not True)
        add("held_limb_agrees_a_card_was_produced", not contra,
            "contradicting=%s" % (contra or "none"))

    # 5b-iii. A dissolved hold is the opposite of a held one, so a record may
    # not claim both about the same limb, and it must say why the hold fell.
    dissolved = manifest.get("dissolved_holds")
    if dissolved is not None:
        still_held = {h.get("held_limb_id") for h in (manifest.get("held_limbs") or [])}
        both = sorted(x.get("held_limb_id") for x in dissolved
                      if x.get("held_limb_id") in still_held)
        add("dissolved_holds_are_not_still_held", not both, "both=%s" % (both or "none"))
        bad = [x.get("held_limb_id") or "?" for x in dissolved
               if not (isinstance(x, dict) and x.get("held_limb_id")
                       and x.get("outcome") and x.get("why"))]
        add("dissolved_holds_well_formed", not bad, "malformed=%s" % (bad or "none"))

    # 5c. Discharged holds -- the mirror of 5b, and asserted for the same
    # reason. A batch may not claim to have closed an earlier batch's hold
    # unless it (a) names a holding record that really declares that hold and
    # (b) actually produced the action. Without (b) "discharged" would be a
    # word a manifest could simply assert, and the outstanding work would
    # vanish from the repository while nothing had been written.
    discharged = manifest.get("discharges_hold")
    if discharged is not None:
        produced = {action_id_of(c) for c in cards}
        bad_shape = [d.get("followup_id") or "?" for d in discharged
                     if not (isinstance(d, dict) and d.get("followup_id")
                             and d.get("held_by_manifest")
                             and d.get("discharged_by"))]
        add("discharged_holds_well_formed", not bad_shape,
            "malformed=%s" % (bad_shape or "none"))

        not_produced = sorted(d.get("followup_id") for d in discharged
                              if d.get("followup_id") not in produced)
        add("discharged_holds_are_actually_produced", not not_produced,
            "claimed_but_absent_from_cards=%s" % (not_produced or "none"))

        # The holding record must exist AND still declare the hold. A discharge
        # that points at a manifest which never held the action -- or whose hold
        # has since been deleted -- is an unverifiable claim, and deleting the
        # hold is precisely how the history would be laundered.
        unbacked = []
        for d in discharged:
            fid = d.get("followup_id")
            holder = p.parent / str(d.get("held_by_manifest") or "")
            if not holder.is_file():
                unbacked.append("%s: %s absent" % (fid, d.get("held_by_manifest")))
                continue
            try:
                held_there = json.loads(read_text(holder)).get("held_actions") or []
            except Exception as exc:
                unbacked.append("%s: %s unreadable (%s)"
                                % (fid, d.get("held_by_manifest"), exc))
                continue
            if not any(h.get("followup_id") == fid for h in held_there):
                unbacked.append("%s: %s declares no such hold"
                                % (fid, d.get("held_by_manifest")))
        add("discharged_holds_name_a_real_hold", not unbacked,
            "unbacked=%s" % (unbacked or "none"))

    # 6. distinct_target_cards, when declared, must be true.
    if "distinct_target_cards" in manifest:
        add("distinct_target_cards_correct",
            manifest["distinct_target_cards"] == len(targets),
            "declared=%s actual=%d" % (manifest["distinct_target_cards"], len(targets)))

    return findings



def audit_governed_artefacts_live(path, repo=None) -> list[Finding]:
    """Pin every governed non-card artefact one correction record declares.

    Sections 2-4 of ``validate_corrections.py`` pin q-cards: they exist, they
    are still what was authorised, and the record describes a transition that
    really happened.  A cheat sheet has no card block, so ``card_digests``
    cannot see it and none of those three checks reaches it.  This asks the
    identical three questions over a whole-file digest, plus a fourth the card
    form gets for free: that the file moved to the RIGHT text, not merely to
    some text the record then pinned.

    Deliberately NOT routed through the supersession resolver -- that resolver
    is keyed on "file#anchor", and feeding it a page with no anchor is exactly
    the impersonation ``governed_artefact_is_not_a_card`` forbids.  A later edit
    to a governed artefact must be declared by a new record, which is the right
    default for a page a candidate reads on the morning of the oral.

    Lives here rather than in the corpus gate so that the gate and the fast
    standalone probe cannot drift into asking different questions -- the drift
    this module was written to stop.
    """
    p = pathlib.Path(path)
    repo = pathlib.Path(repo or REPO)
    findings: list[Finding] = []

    def add(check: str, ok: bool, detail: str = "") -> None:
        findings.append(Finding(p.name, check, ok, detail))

    manifest = json.loads(read_text(p))
    governed = manifest.get("governed_artefacts") or []
    if not governed:
        return findings
    if manifest.get("status") == "SUPERSEDED":
        add("superseded_artefacts_not_enforced", True,
            "status=SUPERSEDED; pins are history, not live expectations")
        return findings

    baseline = manifest.get("baseline_commit")
    commits = manifest.get("governing_commits") or []

    def live(rel):
        f = repo / str(rel)
        return f.read_text(encoding="utf-8", newline="") if f.is_file() else None

    missing = [a["path"] for a in governed if live(a["path"]) is None]
    add("governed_artefacts_present_live", not missing,
        "missing=%s" % (missing or "none"))

    drifted, absent = [], []
    for a in governed:
        text = live(a["path"])
        if text is None:
            continue
        got = artefact_digest(text)
        if got != a["post_edit_digest"]:
            drifted.append("%s (live %s, authorised %s)"
                           % (a["path"], got[:10], a["post_edit_digest"][:10]))
        if a["expected_text_after"] not in text:
            absent.append("%s/%s" % (a["path"], a["correction_action_id"]))
    add("live_matches_authorised_artefact_state", not drifted,
        "drifted=%s" % (drifted or "none"))
    add("artefact_carries_expected_proposition_text", not absent,
        "absent=%s" % (absent or "none"))

    wrong_pre = []
    if baseline:
        for a in governed:
            blob = _git_show(baseline, str(a["path"]))
            was = artefact_digest(blob.decode("utf-8")) if blob is not None else None
            if was != a["pre_edit_digest"]:
                wrong_pre.append("%s (baseline %s, declared %s)"
                                 % (a["path"], (was or "-")[:10],
                                    a["pre_edit_digest"][:10]))
    add("artefact_pre_edit_digests_match_baseline",
        bool(baseline) and not wrong_pre,
        "baseline=%s mismatched=%s" % (baseline or "-", wrong_pre or "none"))

    wrong_post = []
    if commits:
        for a in governed:
            blob = _git_show(commits[-1], str(a["path"]))
            got = artefact_digest(blob.decode("utf-8")) if blob is not None else None
            if got != a["post_edit_digest"]:
                wrong_post.append(str(a["path"]))
    add("governing_commits_produced_artefact_state",
        bool(commits) and not wrong_post,
        "last=%s mismatched=%s" % (commits[-1] if commits else "-",
                                   wrong_post or "none"))
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
    for path in sorted(directory.glob(CORRECTION_MANIFEST_GLOB)):
        findings.extend(audit_correction_manifest(path))
    return findings


def _cli(argv: list[str]) -> int:
    import argparse

    ap = argparse.ArgumentParser(
        prog="oral_manifest",
        description="Audit Oral batch manifests against the shared schema contract.")
    ap.add_argument("--quiet", action="store_true", help="print failures only")
    ap.add_argument("manifests", nargs="*", help="default: every batch manifest")
    args = ap.parse_args(argv)

    def audit_one(m):
        return (audit_correction_manifest(m) if is_correction_manifest(m)
                else audit_manifest(m))

    findings = ([f for m in args.manifests for f in audit_one(m)]
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
