#!/usr/bin/env python3
"""
Historical digest supersession -- the contract that lets a later authorised
edit descend from an earlier pinned card state without destroying it.

THE PROBLEM THIS SOLVES
-----------------------

Every enrichment and follow-up manifest pins the exact state of each card it
edited::

    "file": "QB1_A.html", "anchor": "q9",
    "pre_edit_digest":  "9aab34d4782b7d14",
    "post_edit_digest": "a1deaf3445bc1c88"

and its validator compares that ``post_edit_digest`` to the LIVE page.  That is
the strongest guard in the toolchain: it proves the shipped card is byte-for-byte
what was authorised, and it is why an unmanifested live edit cannot hide.

It also, until now, made a card permanently uneditable.  Anchor-level *ownership*
delegation (``oral_manifest.authorisation_manifest_paths``) already answers "was
this later edit authorised at all?", and exempts a card from
``only_authorised_cards_changed``.  It says nothing about the digest pin, so a
second authorised edit to an already-enriched card forces a choice between
shipping a red historical guard and rebaselining historical evidence.  Both are
forbidden.

Batch F1 hit this exactly once and held the action rather than pick either:
FUP-006 targets QB1_A#q9, which ``batch_e1_enrichment_manifest.json`` pins
through ``ENRICH-A003``.  Eight of the 35 register actions sit on enriched
cards, so it is structural.

THE CONTRACT
------------

The historical pin is never rewritten.  Instead the LATER record declares, per
card, which earlier pinned state it descends from::

    "pre_edit_digest":  "a1deaf3445bc1c88",     <-- E1's post state
    "post_edit_digest": "7c0e1b2233445566",
    "supersedes": {
        "manifest": "batch_e1_enrichment_manifest.json",
        "action_id": "ENRICH-A003",
        "post_edit_digest": "a1deaf3445bc1c88"
    }

and three facts are then provable without touching E1:

    1. the predecessor still pins what the successor says it pins
       (``supersedes.post_edit_digest`` == E1's stored pin), so a rebaselined or
       tampered historical manifest breaks the chain rather than hiding in it;
    2. the successor starts where the predecessor stopped
       (``successor.pre_edit_digest`` == predecessor's ``post_edit_digest``);
    3. the LAST state in the chain is what is live.

E1's own validator keeps asserting something real: not "my state is live" but
"my state is the ancestor of what is live".  H1 survives.  H1 -> H2 -> H3 is
provable.  An unmanifested Hx is not.

WHY THIS IS NOT THE `authorised elsewhere` MECHANISM
----------------------------------------------------

They answer different questions and both are required.

    authorisation_manifest_paths()      "is this later edit authorised?"
    this module                         "does the later authorised state
                                         validly DESCEND from my pinned state?"

Ownership delegation alone would exempt a corrected card forever.  The chain
alone would not know whether the successor was ever allowed to exist.  Neither
subsumes the other, and collapsing them would silently drop one guard.

DORMANT BY DEFAULT
------------------

When no record for a target declares ``supersedes``, resolution degrades to the
exact comparison every validator already performs -- ``pin == live`` -- and no
chain machinery runs.  That is what makes adopting this a no-op for the ten
manifests already on main.  A chain is engaged only by an explicit declaration.

DIGEST CONVENTIONS ARE NOT INTERCHANGEABLE
------------------------------------------

Three coexist in this repo, all legitimate release evidence:

    sha256(card_text_lf)[:16]       E1-E5, F1
    sha256(card_text_lf)            E6
    sha256(balanced_block_lf)       correction records (via validate_batch_b)

A chain is therefore required to stay in ONE convention -- the root's.  A
successor superseding an E1 pin records that card's digests the way E1 records
them.  Mixed widths are reported as ``DIGEST_CONVENTION_MISMATCH`` rather than
compared as strings and silently failing for the wrong reason.  Fail closed,
and say which wall you hit.

SHARED TARGETS ARE ONE STATE, NOT TWO LINKS
-------------------------------------------

E5 puts ENRICH-A036 and ENRICH-A037 on QB4_C#q6 with identical digests, and the
schema requires exactly that (``shared_target_digests_agree``).  Chain nodes are
therefore keyed by ``(manifest, pre_digest, post_digest)`` with the action ids as
MEMBERS.  Keying by action id would read two co-owners of one state as two
competing terminal states and fail a card that is entirely correct.
"""

from __future__ import annotations

import dataclasses
import json
import pathlib
from typing import Iterable

from oral_bytes import read_text
from oral_manifest import action_id_of, authorisation_manifest_paths

SUPERSEDES_FIELD = "supersedes"

# Every field a supersession claim may carry.  An unknown key is a failure for
# the same reason UNCLASSIFIED is a failure in the manifest schema: a new
# authorisation-looking key that nothing reads is exactly the decoration this
# governance layer exists to forbid.
SUPERSEDES_FIELDS = frozenset({"manifest", "action_id", "post_edit_digest", "note"})
SUPERSEDES_REQUIRED = ("manifest", "action_id", "post_edit_digest")

# Resolution outcomes.  Only the first two are acceptable states for a card.
LIVE_TERMINAL = "LIVE_TERMINAL"          # this record is last, and it is live
SUPERSEDED_OK = "SUPERSEDED"             # this record is an ancestor of live
PIN_MISMATCH = "PIN_MISMATCH"            # no chain; pin != live (today's failure)
ORPHAN_SUCCESSOR = "ORPHAN_SUCCESSOR"    # names a predecessor that does not exist
PREDECESSOR_PIN_ALTERED = "PREDECESSOR_PIN_ALTERED"
CHAIN_BREAK = "CHAIN_BREAK"              # successor.pre != predecessor.post
CHAIN_FORK = "CHAIN_FORK"                # two successors claim one predecessor
CHAIN_CYCLE = "CHAIN_CYCLE"
AMBIGUOUS_ROOT = "AMBIGUOUS_ROOT"
AMBIGUOUS_TERMINAL = "AMBIGUOUS_TERMINAL"
TERMINAL_NOT_LIVE = "TERMINAL_NOT_LIVE"  # chain is sound but live is off-chain
WRONG_CARD = "WRONG_CARD"                # successor supersedes another card
DIGEST_CONVENTION_MISMATCH = "DIGEST_CONVENTION_MISMATCH"
MALFORMED_CLAIM = "MALFORMED_CLAIM"
NOT_IN_CHAIN = "NOT_IN_CHAIN"

OK_STATUSES = frozenset({LIVE_TERMINAL, SUPERSEDED_OK})


# ---------------------------------------------------------------- records


@dataclasses.dataclass(frozen=True)
class CardRecord:
    """One card entry from one manifest, reduced to what a chain needs."""

    manifest: str
    action_id: str
    file: str
    anchor: str
    pre_edit_digest: str | None
    post_edit_digest: str | None
    supersedes: dict | None

    @property
    def target(self) -> tuple:
        return (self.file, self.anchor)

    @property
    def state_key(self) -> tuple:
        """Co-owners of one card state collapse to one node.  See module docs."""
        return (self.manifest, self.pre_edit_digest, self.post_edit_digest)

    def describe(self) -> str:
        return "%s/%s" % (self.manifest, self.action_id)


def load_card_records(directory=None) -> list[CardRecord]:
    """Every card entry across every record that may authorise an edit.

    Reads the SAME surface as the ownership-delegation scan -- batch manifests
    and correction manifests -- because a record that can authorise an edit must
    also be able to carry that edit's descent.  Reusing
    ``authorisation_manifest_paths`` is deliberate: two definitions of "the
    authorisation surface" is how the two record families drifted apart before.
    """
    records: list[CardRecord] = []
    for path in authorisation_manifest_paths(directory):
        try:
            manifest = json.loads(read_text(path))
        except Exception:
            continue
        for card in manifest.get("cards") or []:
            aid = action_id_of(card)
            if not aid:
                continue
            records.append(CardRecord(
                manifest=path.name,
                action_id=aid,
                file=card.get("file"),
                anchor=card.get("anchor"),
                pre_edit_digest=card.get("pre_edit_digest"),
                post_edit_digest=card.get("post_edit_digest"),
                supersedes=card.get(SUPERSEDES_FIELD),
            ))
    return records


# ------------------------------------------------------------------ chain


@dataclasses.dataclass(frozen=True)
class State:
    """One pinned card state, possibly co-owned by several action ids."""

    manifest: str
    pre: str | None
    post: str | None
    action_ids: tuple
    claim: dict | None          # the supersedes claim these action ids carry

    @property
    def key(self) -> tuple:
        return (self.manifest, self.pre, self.post)

    def describe(self) -> str:
        return "%s/%s" % (self.manifest, "+".join(sorted(self.action_ids)))


@dataclasses.dataclass(frozen=True)
class Resolution:
    """The answer a validator asked for, with enough detail to act on."""

    ok: bool
    status: str
    reason: str
    chain: tuple = ()

    def describe(self) -> str:
        path = " -> ".join(self.chain) if self.chain else "-"
        return "%s: %s [%s]" % (self.status, self.reason, path)


def _same_convention(a, b) -> bool:
    """Two digests are comparable only if they are the same width.

    Not a cosmetic check.  ``sha256(text)[:16]`` and ``sha256(text)`` of the
    SAME card differ as strings, so comparing them would produce a chain break
    that reads as tampering when the real fault is that the successor recorded
    its card in another family's convention.
    """
    return (isinstance(a, str) and isinstance(b, str) and len(a) == len(b))


def _claim_problem(claim) -> str | None:
    if not isinstance(claim, dict):
        return "supersedes must be an object, got %s" % type(claim).__name__
    unknown = sorted(set(claim) - SUPERSEDES_FIELDS)
    if unknown:
        return "unknown supersedes field(s): %s" % ", ".join(unknown)
    missing = [f for f in SUPERSEDES_REQUIRED if not claim.get(f)]
    if missing:
        return "supersedes missing %s" % ", ".join(missing)
    return None


def _states_for(records: Iterable[CardRecord], target: tuple):
    """Collapse this target's card records into states, keyed as documented."""
    grouped: dict[tuple, dict] = {}
    for rec in records:
        if rec.target != target:
            continue
        slot = grouped.setdefault(rec.state_key, {"ids": [], "claims": []})
        slot["ids"].append(rec.action_id)
        if rec.supersedes is not None:
            slot["claims"].append(rec.supersedes)

    states: dict[tuple, State] = {}
    for (manifest, pre, post), slot in grouped.items():
        # Co-owners of one state must not disagree about their descent.  Two
        # different claims on one state is two different histories for one card.
        claims = slot["claims"]
        claim = claims[0] if claims else None
        if claims and any(c != claim for c in claims[1:]):
            claim = {"__conflict__": True}
        states[(manifest, pre, post)] = State(
            manifest=manifest, pre=pre, post=post,
            action_ids=tuple(slot["ids"]), claim=claim)
    return states


def _resolve_claim(claim, states, all_records, target):
    """Find the state a supersedes claim points at, or say why it cannot."""
    manifest = claim.get("manifest")
    action_id = claim.get("action_id")
    declared = claim.get("post_edit_digest")

    # Does the named action exist at all, anywhere?
    named = [r for r in all_records
             if r.manifest == manifest and r.action_id == action_id]
    if not named:
        return None, (ORPHAN_SUCCESSOR,
                      "predecessor %s/%s does not exist" % (manifest, action_id))

    # Does it describe the SAME card?  A successor that supersedes another
    # card's state would otherwise release both cards from their pins.
    off_target = [r for r in named if r.target != target]
    if off_target and not any(r.target == target for r in named):
        return None, (WRONG_CARD,
                      "predecessor %s/%s owns %s#%s, not %s#%s"
                      % (manifest, action_id, off_target[0].file,
                         off_target[0].anchor, target[0], target[1]))

    # Does the predecessor still pin what the successor says it pins?  This is
    # what makes rebaselining a historical manifest break the chain instead of
    # quietly becoming the new truth.
    on_target = [r for r in named if r.target == target]
    actual = on_target[0].post_edit_digest
    if actual != declared:
        return None, (PREDECESSOR_PIN_ALTERED,
                      "predecessor %s/%s pins %s, claim says %s"
                      % (manifest, action_id, actual, declared))

    key = (manifest, on_target[0].pre_edit_digest, actual)
    state = states.get(key)
    if state is None or action_id not in state.action_ids:
        return None, (ORPHAN_SUCCESSOR,
                      "predecessor state %s/%s not present for %s#%s"
                      % (manifest, action_id, target[0], target[1]))
    return state, None


def build_chain(target, records=None, directory=None):
    """Order every pinned state for one card into a single line of descent.

    Returns ``(ordered_states, problem)``.  ``problem`` is a
    ``(status, reason)`` pair, or None when the chain is sound.  A card with no
    supersession declaration returns ``(None, None)``: there is no chain, and the
    caller must fall back to the plain pin comparison.
    """
    records = list(records if records is not None else load_card_records(directory))
    states = _states_for(records, target)
    if not states:
        return None, None

    claimants = {k: s for k, s in states.items() if s.claim is not None}
    if not claimants:
        return None, None                 # dormant: no chain declared

    # Malformed or conflicting claims are rejected before any edge is built.
    for key, state in claimants.items():
        # Shape is checked BEFORE anything is read off the claim. A malformed
        # record must fail closed, never raise: a crash in a release guard is
        # an unavailable guard, and an unavailable guard is not a passing one.
        if isinstance(state.claim, dict) and state.claim.get("__conflict__"):
            return None, (MALFORMED_CLAIM,
                          "co-owners of %s declare different predecessors"
                          % state.describe())
        problem = _claim_problem(state.claim)
        if problem:
            return None, (MALFORMED_CLAIM, "%s: %s" % (state.describe(), problem))

    # successor state -> predecessor state
    parent: dict[tuple, tuple] = {}
    for key, state in claimants.items():
        pred, problem = _resolve_claim(state.claim, states, records, target)
        if problem:
            return None, problem
        if pred.key == key:
            return None, (CHAIN_CYCLE, "%s supersedes itself" % state.describe())
        if not _same_convention(state.pre, pred.post):
            return None, (DIGEST_CONVENTION_MISMATCH,
                          "%s pins a %s-char pre-digest, %s pins a %s-char post-digest"
                          % (state.describe(), len(state.pre or ""),
                             pred.describe(), len(pred.post or "")))
        if state.pre != pred.post:
            return None, (CHAIN_BREAK,
                          "%s starts at %s but %s ended at %s"
                          % (state.describe(), state.pre,
                             pred.describe(), pred.post))
        parent[key] = pred.key

    # Two successors claiming one predecessor is two futures for one card.
    seen_parents: dict[tuple, tuple] = {}
    for child, pred in parent.items():
        if pred in seen_parents:
            return None, (CHAIN_FORK,
                          "%s and %s both supersede %s"
                          % (states[seen_parents[pred]].describe(),
                             states[child].describe(), states[pred].describe()))
        seen_parents[pred] = child

    roots = [k for k in states if k not in parent]
    if len(roots) != 1:
        return None, (AMBIGUOUS_ROOT,
                      "%d states have no predecessor: %s"
                      % (len(roots), ", ".join(sorted(
                          states[k].describe() for k in roots))))

    terminals = [k for k in states if k not in seen_parents]
    if len(terminals) != 1:
        return None, (AMBIGUOUS_TERMINAL,
                      "%d states have no successor: %s"
                      % (len(terminals), ", ".join(sorted(
                          states[k].describe() for k in terminals))))

    # Walk root -> terminal.  Any state not reached is either a cycle or an
    # island; both mean the card has a history the chain cannot account for.
    child_of = {pred: child for pred, child in seen_parents.items()}
    order = [roots[0]]
    guard = 0
    while order[-1] in child_of:
        guard += 1
        if guard > len(states):
            return None, (CHAIN_CYCLE, "cycle detected walking %s#%s" % target)
        order.append(child_of[order[-1]])

    if len(order) != len(states):
        unreached = sorted(states[k].describe() for k in states
                           if k not in set(order))
        return None, (CHAIN_CYCLE,
                      "%d state(s) unreachable from the root: %s"
                      % (len(unreached), ", ".join(unreached)))

    return [states[k] for k in order], None


def resolve_authorised_card_state(*, manifest, action_id, file, anchor,
                                  pinned_post_digest, live_digest,
                                  records=None, directory=None) -> Resolution:
    """Is this record's pinned post-state still honoured by the live page?

    Two acceptable answers:

    * no authorised successor exists, and the pin IS the live card
      (``LIVE_TERMINAL`` -- exactly today's contract, unchanged); or
    * an authorised successor chain exists, this record is an ancestor in it,
      every link is continuous, and the chain's terminal state is the live card
      (``SUPERSEDED``).

    Everything else fails, including a live card that matches no state in the
    chain -- an unmanifested Hx.  Callers fold the reason into their existing
    digest check rather than adding a new one, so a validator's check COUNT is
    unchanged and its meaning is strictly stronger.
    """
    target = (file, anchor)
    records = list(records if records is not None else load_card_records(directory))
    chain, problem = build_chain(target, records=records)

    if problem is not None:
        return Resolution(False, problem[0], problem[1])

    if chain is None:
        # Dormant path: no supersession declared for this card anywhere.
        if pinned_post_digest == live_digest:
            return Resolution(True, LIVE_TERMINAL, "pin is live")
        return Resolution(False, PIN_MISMATCH,
                          "pinned %s but live is %s"
                          % (pinned_post_digest, live_digest))

    mine = [s for s in chain
            if s.manifest == manifest and action_id in s.action_ids]
    if not mine:
        return Resolution(False, NOT_IN_CHAIN,
                          "%s/%s is not a state in the chain for %s#%s"
                          % (manifest, action_id, file, anchor),
                          tuple(s.describe() for s in chain))
    state = mine[0]
    path = tuple(s.describe() for s in chain)

    if state.post != pinned_post_digest:
        # The caller passed a pin that is not the one the chain was built from.
        return Resolution(False, PREDECESSOR_PIN_ALTERED,
                          "record pins %s but the chain holds %s"
                          % (pinned_post_digest, state.post), path)

    terminal = chain[-1]
    if not _same_convention(terminal.post, live_digest):
        return Resolution(False, DIGEST_CONVENTION_MISMATCH,
                          "terminal %s pins a %s-char digest, live digest is %s chars"
                          % (terminal.describe(), len(terminal.post or ""),
                             len(live_digest or "")), path)
    if terminal.post != live_digest:
        return Resolution(False, TERMINAL_NOT_LIVE,
                          "chain ends at %s (%s) but live is %s"
                          % (terminal.describe(), terminal.post, live_digest), path)

    if terminal is state:
        return Resolution(True, LIVE_TERMINAL,
                          "pin is live; %d state(s) in chain" % len(chain), path)
    return Resolution(True, SUPERSEDED_OK,
                      "superseded by %s, which is live" % terminal.describe(), path)


# ------------------------------------------------- superseded-state recovery


def successor_claim_for(*, manifest, action_id, file, anchor,
                        records=None, directory=None) -> dict | None:
    """The immediate successor that supersedes this record's state, or None.

    WHY A CALLER NEEDS THIS, AND WHY ``resolve_authorised_card_state`` IS NOT
    ENOUGH
    ------------------------------------------------------------------------
    ``resolve_authorised_card_state`` answers the DIGEST question: is my pinned
    state still the live card, or the ancestor of it?  It was folded into every
    generation-2 validator's digest check, so no validator gained a check.

    But a batch validator also asserts things about WHAT ITS OWN EDIT DID --
    E6 asserts its enrichment was purely additive and left the 15s/60s blocks
    byte-identical.  Those implementations read the LIVE card as a stand-in for
    "the state I produced".  That stand-in is correct only while the record's
    state IS live.  The moment a later authorised record supersedes it, the
    live card is somebody else's state and the assertion silently changes
    meaning -- it starts testing the successor's edit and reports it as the
    predecessor's regression.  That is guard expiry in the "starts failing"
    direction (SKILL section 7.5b), caused by a legitimate change.

    The rule there is: make the check change SUBJECT, do not stand it down.
    So a superseded record compares against the state IT produced, which the
    successor's own ``baseline_commit`` names -- the successor's pre-edit tree
    IS the predecessor's post-edit tree, by the chain-continuity requirement
    that ``pre_edit_digest == predecessor's post_edit_digest``.

    Returns a dict with ``manifest``, ``action_id`` and ``baseline_commit`` of
    the successor.  The caller recovers the text at that commit and MUST verify
    it digests to its own pinned ``post_edit_digest`` before using it -- this
    function deliberately does not touch git, so the module stays free of
    subprocess and Windows path handling, and so a caller cannot be handed
    bytes it never checked.
    """
    records = load_card_records(directory) if records is None else records
    for r in records:
        claim = r.supersedes
        if not isinstance(claim, dict):
            continue
        if (r.file, r.anchor) != (file, anchor):
            continue
        if claim.get("manifest") != manifest or claim.get("action_id") != action_id:
            continue
        base = _manifest_baseline_commit(r.manifest, directory)
        return {"manifest": r.manifest, "action_id": r.action_id,
                "baseline_commit": base}
    return None


def _manifest_baseline_commit(name, directory=None):
    for path in authorisation_manifest_paths(directory):
        if path.name != name:
            continue
        try:
            return json.loads(read_text(path)).get("baseline_commit")
        except Exception:
            return None
    return None


# ------------------------------------------------------------------ audit


def audit_supersession_chains(directory=None) -> list:
    """Every declared chain in the repository, with its verdict.

    Reports one row per target that declares a supersession.  Targets with no
    declaration are silent: they are not chains, and listing them would bury the
    handful that are.
    """
    records = load_card_records(directory)
    targets = sorted({r.target for r in records if r.supersedes is not None})
    rows = []
    for target in targets:
        chain, problem = build_chain(target, records=records)
        if problem is not None:
            rows.append((target, False, "%s: %s" % problem, ()))
            continue
        rows.append((target, True, "%d state(s)" % len(chain),
                     tuple(s.describe() for s in chain)))
    return rows


def _cli(argv):
    import argparse

    ap = argparse.ArgumentParser(
        prog="oral_supersession",
        description="Report every declared historical digest supersession chain.")
    ap.add_argument("--directory", default=None,
                    help="manifest directory (default: this tool's own)")
    args = ap.parse_args(argv)

    rows = audit_supersession_chains(args.directory)
    if not rows:
        print("no supersession chain declared; every pinned card is terminal")
        return 0
    bad = 0
    for (file, anchor), ok, detail, path in rows:
        bad += 0 if ok else 1
        print("%-4s %s#%-6s %-28s %s"
              % ("PASS" if ok else "FAIL", file, anchor, detail,
                 " -> ".join(path) if path else "-"))
    print("supersession chains: %d, %d FAIL" % (len(rows), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    import sys

    sys.exit(_cli(sys.argv[1:]))
