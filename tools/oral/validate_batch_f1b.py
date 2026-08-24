#!/usr/bin/env python3
"""Release guard for Oral follow-up production batch F1b.

WHAT F1b IS
-----------
A single-action batch: it implements ``FUP-006`` and nothing else.

F1 authorised three actions, produced FUP-018 and FUP-033, and HELD FUP-006 as
``HELD_GOVERNANCE``.  The blocker was structural rather than editorial: FUP-006
targets ``QB1_A#q9``, which ``batch_e1_enrichment_manifest.json`` pins through
``ENRICH-A003``, and a digest pin had no delegation path in any batch validator.
Producing it meant shipping a red historical guard or rebaselining E1.  Both are
forbidden, so F1 held it and said so.

WHY THIS VALIDATOR IS DIFFERENT FROM F1'S
-----------------------------------------
F1b is the **first production use of historical digest supersession**
(``tools/oral/oral_supersession.py``).  Its card declares that its pre-edit state
IS E1's pinned post-edit state::

    "pre_edit_digest":  "a1deaf3445bc1c88",     <- E1's post state
    "post_edit_digest": "46defd301a1f56a3",
    "supersedes": { "manifest": "batch_e1_enrichment_manifest.json",
                    "action_id": "ENRICH-A003",
                    "post_edit_digest": "a1deaf3445bc1c88" }

so this file has to assert things F1's never had to:

  * the historical predecessor is still intact and still pins what F1b says it
    pins -- checked HERE and not only inside the resolver, because a validator
    that trusts the resolver to police its own inputs proves nothing about the
    record it is certifying;
  * the chain is continuous, has one root and one terminal, and the terminal is
    the live card;
  * F1's hold record is still historically TRUE -- F1 held FUP-006, and no
    later batch may launder that by editing F1's manifest;
  * F1b, not F1, is what records the implementation.

The last two are the reason a `discharges_hold` record exists at all.  A hold
closed by rewriting the manifest that declared it would leave nothing saying the
work was ever owed.

FAIL-CLOSED
-----------
If the register, the manifest, the predecessor record or the baseline is
unavailable this reports ``unavailable`` and returns non-zero.  A guard that
cannot read its authorisation record has not passed; it has failed to run.
"""

from __future__ import annotations

import difflib
import hashlib
import html
import io
import json
import pathlib
import re
import subprocess
import sys
import tarfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB_DIR = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_manifest import authorisation_manifest_paths, sibling_owned_cards, HELD_STATUSES  # noqa: E402
from oral_supersession import (  # noqa: E402
    SUPERSEDES_REQUIRED, build_chain, load_card_records,
    resolve_authorised_card_state,
)

MANIFEST = HERE / "batch_f1b_manifest.json"
REGISTER = HERE / "oral_followup_register.json"

# The batch, as authorised and as implemented. F1b holds nothing back, so unlike
# F1 these two sets are equal -- and that is asserted rather than assumed.
AUTHORISED_FUPS = {"FUP-006"}
IMPLEMENTED_FUPS = {"FUP-006"}

# The batch that HELD this action. F1b discharges that hold; F1's own record of
# it must survive untouched.
HOLDING_MANIFEST = "batch_f1_manifest.json"

# The record F1b descends from. Named here as well as in the manifest so a
# manifest that quietly re-pointed its own supersession claim at some other,
# more convenient predecessor fails against an independent expectation.
PREDECESSOR_MANIFEST = "batch_e1_enrichment_manifest.json"
PREDECESSOR_ACTION = "ENRICH-A003"

PLACEHOLDER_CLASS = "UNCLASSIFIED_PENDING_BATCH_SCOPING"

# Actions permitted to create a canonical card. Empty by design and asserted
# against an explicitly empty set, so "no new cards" is a decision on record.
NEW_CARD_EXCEPTIONS: set = set()

# The LIMB -- what the examiner actually asked for. Specific enough that
# deleting the worked application cannot leave them behind, and deliberately
# NOT satisfiable by the pre-existing Casualty Anchor, which already says
# "Ever Given" and "GA security". A token this card carried BEFORE the edit
# would make this check vacuous, so every one below was verified absent from
# the pre-edit card.
LIMB_TOKENS = {
    "FUP-006": ["Worked Application",
                "the grounding is not the general average act",
                "Rule VI(a)",
                "Rule VI(d)",
                "Richards Hogg Lindley",
                "Shoei Kisen Kaisha"],
}

# The authority each limb must cite. A claim whose source vanishes is an
# unsourced claim, so this is checked separately from the limb itself.
AUTHORITY_TOKENS = {
    "FUP-006": ["demurrage, loss of market",
                "Rule C",
                "Rule D",
                "23 March 2021",
                "29 March 2021"],
}

# The directed follow-up edge must be visible on the card, not only walkable in
# the manifest -- the examiner relationship is the product, not just metadata.
CHAIN_EDGE = {
    "FUP-006": "now apply it to the Ever Given aground in the Suez",
}

# Claims the batch deliberately did NOT make, because the evidence does not
# support them. Re-introducing one later is a content regression that no digest
# check would describe, so they are named.
FORBIDDEN_CLAIMS = {
    "FUP-006": [r"\$\s*\d",                      # any settlement / claim figure
                r"\bsettled\s+for\b",
                r"\b(?:1|2|3|4|5)\s+April\s+2021\b"],   # unsettled declaration date
}

# Internal production vocabulary that must never reach a candidate.
FORBIDDEN = re.compile(
    r"\b(?:FUP-\d+|GAP-\d+|ASC-\d+|ENRICH-A\d+|followup_id|relationship_edge|"
    r"verification_scope|pre_edit_digest|post_edit_digest|supersedes|"
    r"discharges_hold|target_review_status|recurrence_class|LAPTOP_CONFIRMED)\b")

CARD_OPEN = re.compile(r'<div class="q-card[^"]*"[^>]*>', re.I)
CANONICAL_ANCHOR = re.compile(r"q\d+")

_checks = 0
_failed = []


def report(name, ok, detail=""):
    global _checks
    _checks += 1
    if not ok:
        _failed.append(name)
    print("%-4s %-46s %s" % ("PASS" if ok else "FAIL", name, detail))


def unavailable(reason):
    print("unavailable: %s" % reason)
    print("\n0 checks, 1 FAIL")
    return 2


def digest16(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def _balanced_end(text, start):
    """End index of the q-card div opened at ``start``, by depth counting.

    Identical to the E1-F1 implementation on purpose: F1b's digests must be
    computed over exactly the same card boundaries as the record it supersedes,
    or the chain would compare two different notions of "the card".
    """
    depth = 0
    for m in re.finditer(r"<div\b[^>]*>|</div\s*>", text[start:], re.I):
        depth += -1 if m.group(0).startswith("</") else 1
        if depth == 0:
            return start + m.end()
    raise AssertionError("unbalanced q-card at %d" % start)


def cards_of(text):
    """anchor -> card HTML, on LF-normalised text."""
    text = text.replace("\r\n", "\n")
    out = {}
    for m in CARD_OPEN.finditer(text):
        end = _balanced_end(text, m.start())
        a = re.search(r'\bid="([^"]+)"', m.group(0))
        if a:
            out[a.group(1)] = text[m.start():end]
    return out


def canonical_cards(text):
    """Only the q-cards that are canonical QUESTIONS.

    The corpus carries more .q-card divs (723) than canonical questions (721),
    so counting the class rather than the anchor convention inflates the corpus
    and lets a total assertion pass vacuously.
    """
    return {a: c for a, c in cards_of(text).items()
            if CANONICAL_ANCHOR.fullmatch(a)}


def visible_text(card):
    return re.sub(r"<[^>]+>", " ", card)


def qtext_of(card):
    m = re.search(r'class="q-text"[^>]*>(.*?)</div>', card, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else None


def load_baseline(ref):
    """Every meoclass1/*.html at ``ref``, via ONE git archive.

    Performance is a correctness property: E6's first validator ran `git show`
    172 times and took 91 seconds, which made its mutation suite a 50-minute
    run and therefore a guard people skip.
    """
    try:
        out = subprocess.run(["git", "archive", "--format=tar", ref, "meoclass1"],
                             cwd=str(REPO), capture_output=True, check=False)
    except OSError as exc:
        return None, "git archive failed: %s" % exc
    if out.returncode != 0 or not out.stdout:
        return None, "git archive %s returned %d" % (ref, out.returncode)
    pages = {}
    with tarfile.open(fileobj=io.BytesIO(out.stdout)) as tar:
        for member in tar.getmembers():
            name = member.name.replace("\\", "/")
            if not member.isfile() or not name.endswith(".html"):
                continue
            if "/" in name[len("meoclass1/"):]:
                continue          # subdirectories (oralnotes, pastpapers)
            fh = tar.extractfile(member)
            if fh is not None:
                pages[name.rsplit("/", 1)[-1]] = fh.read().decode("utf-8", "replace")
    return pages, None


def main():
    if not MANIFEST.exists():
        return unavailable("manifest %s is absent" % MANIFEST.name)
    if not REGISTER.exists():
        return unavailable("register %s is absent" % REGISTER.name)
    holding_path = HERE / HOLDING_MANIFEST
    if not holding_path.exists():
        return unavailable("holding record %s is absent" % HOLDING_MANIFEST)
    predecessor_path = HERE / PREDECESSOR_MANIFEST
    if not predecessor_path.exists():
        return unavailable("predecessor record %s is absent" % PREDECESSOR_MANIFEST)
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        register = json.loads(REGISTER.read_text(encoding="utf-8"))
        holding = json.loads(holding_path.read_text(encoding="utf-8"))
        predecessor = json.loads(predecessor_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return unavailable("authorisation record unreadable: %s" % exc)

    cards = manifest.get("cards") or []
    base_ref = manifest.get("baseline_commit")
    reg_actions = {a.get("followup_id"): a for a in register.get("actions") or []}

    # ---- 1. the authorised set and the implemented set --------------------
    missing_auth = sorted(f for f in AUTHORISED_FUPS if f not in reg_actions)
    report("authorised_fup_set_resolves_in_register", not missing_auth,
           "authorised=%s unresolved=%s"
           % (sorted(AUTHORISED_FUPS), missing_auth or "none"))

    declared = [c.get("followup_id") for c in cards]
    report("implemented_set_is_exactly_fup_006",
           sorted(declared) == sorted(IMPLEMENTED_FUPS),
           "declared=%s expected=%s" % (sorted(declared), sorted(IMPLEMENTED_FUPS)))

    report("action_id_and_followup_id_agree",
           all(c.get("action_id") == c.get("followup_id") for c in cards),
           "; ".join("%s/%s" % (c.get("action_id"), c.get("followup_id"))
                     for c in cards))

    # F1b holds nothing. Asserting the ABSENCE keeps "this batch shipped
    # everything it was authorised to" a decision on record rather than a
    # silent property of the file.
    report("f1b_holds_nothing_back",
           not (manifest.get("held_actions") or []),
           "held=%s" % (manifest.get("held_actions") or "none"))

    # ---- 2. the F1 hold, and its discharge --------------------------------
    # F1 must STILL say it held FUP-006. A later batch that edited F1's record
    # to claim the action was produced there would erase the only evidence the
    # work was ever outstanding -- and would make this batch's own reason for
    # existing unreadable.
    f1_held = {h.get("followup_id"): h for h in holding.get("held_actions") or []}
    hold = f1_held.get("FUP-006")
    report("f1_still_records_the_hold_historically",
           hold is not None
           and hold.get("status") in HELD_STATUSES
           and hold.get("work_still_owed") is True
           and hold.get("target") == "QB1_A.html#q9",
           "f1 held=%s status=%s owed=%s target=%s"
           % (hold is not None, (hold or {}).get("status"),
              (hold or {}).get("work_still_owed"), (hold or {}).get("target")))

    # F1 must not ALSO claim to have produced it.
    report("f1_does_not_claim_to_have_produced_it",
           "FUP-006" not in {c.get("followup_id") or c.get("action_id")
                             for c in holding.get("cards") or []},
           "f1 cards=%s" % sorted(str(c.get("followup_id"))
                                  for c in holding.get("cards") or []))

    # ...and F1b must be where the implementation IS recorded.
    dis = {d.get("followup_id"): d for d in manifest.get("discharges_hold") or []}
    entry = dis.get("FUP-006")
    report("f1b_records_the_discharge",
           entry is not None
           and entry.get("held_by_manifest") == HOLDING_MANIFEST
           and bool(entry.get("discharged_by")),
           "discharged=%s by=%s" % (sorted(dis), (entry or {}).get("held_by_manifest")))

    # The register is an AUTHORISATION record, not a status board. Turning it
    # into one would mean two competing sources of truth for what is done.
    report("register_status_of_the_action_untouched",
           (reg_actions.get("FUP-006") or {}).get("status") == "AUTHORISED_NOT_STARTED",
           "register status=%s" % (reg_actions.get("FUP-006") or {}).get("status"))

    # ---- 3. the card matches its register record, field by field ----------
    tgt_bad, rel_bad, edge_bad, cls_bad, cur_bad, auth_bad, newcard_bad = (
        [], [], [], [], [], [], [])
    for c in cards:
        fid = c.get("followup_id")
        rec = reg_actions.get(fid)
        if rec is None:
            tgt_bad.append("%s not in register" % fid)
            continue
        if (c.get("file") != rec.get("parent_file")
                or c.get("anchor") != rec.get("parent_anchor")):
            tgt_bad.append("%s target %s#%s != register %s#%s"
                           % (fid, c.get("file"), c.get("anchor"),
                              rec.get("parent_file"), rec.get("parent_anchor")))
        if c.get("relationship_type") != rec.get("relationship_type"):
            rel_bad.append("%s %s != %s" % (fid, c.get("relationship_type"),
                                            rec.get("relationship_type")))
        if c.get("relationship_edge") != rec.get("relationship_edge"):
            edge_bad.append(fid)
        vs = c.get("verification_scope")
        if (vs not in (register.get("vocabularies", {}).get("verification_class") or [])
                or vs == PLACEHOLDER_CLASS):
            cls_bad.append("%s=%s" % (fid, vs))
        cur = c.get("currentness") or {}
        if ("required_by_register" not in cur or "batch_decision" not in cur
                or not cur.get("basis")
                or cur.get("required_by_register") != rec.get("currentness_required")):
            cur_bad.append(fid)
        if not (c.get("authority") and isinstance(c["authority"], list)):
            auth_bad.append(fid)
        if rec.get("creates_new_card") and fid not in NEW_CARD_EXCEPTIONS:
            newcard_bad.append(fid)

    report("parent_target_matches_register", not tgt_bad, "%s" % (tgt_bad or "-"))
    report("relationship_type_matches_register", not rel_bad, "%s" % (rel_bad or "-"))
    report("relationship_edge_carried_unchanged", not edge_bad,
           "%s" % (edge_bad or "-"))
    report("verification_class_governed_and_not_placeholder", not cls_bad,
           "%s" % (cls_bad or "-"))
    report("currentness_decision_recorded", not cur_bad, "%s" % (cur_bad or "-"))
    report("authority_recorded", not auth_bad, "%s" % (auth_bad or "-"))
    report("no_action_creates_a_new_card",
           not newcard_bad and manifest.get("creates_new_cards") is False,
           "declared=%s bad=%s"
           % (manifest.get("creates_new_cards"), newcard_bad or "-"))

    # ---- 4. the supersession claim ----------------------------------------
    # Checked against the predecessor record DIRECTLY, not only through the
    # resolver. The resolver answers "is the chain sound?"; these answer "is
    # this manifest's claim about history the claim we authorised?", and a
    # manifest that re-pointed itself at a softer predecessor would satisfy the
    # first while failing the second.
    claim_bad, pred_bad = [], []
    pred_cards = {c.get("action_id"): c for c in predecessor.get("cards") or []}
    for c in cards:
        claim = c.get("supersedes")
        if not isinstance(claim, dict):
            claim_bad.append("%s declares no supersession claim" % c.get("action_id"))
            continue
        for field in SUPERSEDES_REQUIRED:
            if not claim.get(field):
                claim_bad.append("%s claim lacks %s" % (c.get("action_id"), field))
        if claim.get("manifest") != PREDECESSOR_MANIFEST:
            claim_bad.append("%s supersedes %s, expected %s"
                             % (c.get("action_id"), claim.get("manifest"),
                                PREDECESSOR_MANIFEST))
        if claim.get("action_id") != PREDECESSOR_ACTION:
            claim_bad.append("%s supersedes %s, expected %s"
                             % (c.get("action_id"), claim.get("action_id"),
                                PREDECESSOR_ACTION))
        # The predecessor must still exist, still own this card, and still pin
        # what the claim says. A rebaselined historical manifest breaks the
        # chain here instead of quietly becoming the new truth.
        pred = pred_cards.get(PREDECESSOR_ACTION)
        if pred is None:
            pred_bad.append("%s/%s absent" % (PREDECESSOR_MANIFEST, PREDECESSOR_ACTION))
        else:
            if (pred.get("file"), pred.get("anchor")) != (c.get("file"), c.get("anchor")):
                pred_bad.append("predecessor owns %s#%s, successor owns %s#%s"
                                % (pred.get("file"), pred.get("anchor"),
                                   c.get("file"), c.get("anchor")))
            if pred.get("post_edit_digest") != claim.get("post_edit_digest"):
                pred_bad.append("predecessor pins %s, claim says %s"
                                % (pred.get("post_edit_digest"),
                                   claim.get("post_edit_digest")))
            if pred.get("post_edit_digest") != c.get("pre_edit_digest"):
                pred_bad.append("chain break: predecessor ends at %s, successor "
                                "starts at %s" % (pred.get("post_edit_digest"),
                                                  c.get("pre_edit_digest")))
            if len(str(pred.get("post_edit_digest") or "")) != len(
                    str(c.get("post_edit_digest") or "")):
                pred_bad.append("digest convention mismatch: predecessor %d chars, "
                                "successor %d chars"
                                % (len(str(pred.get("post_edit_digest") or "")),
                                   len(str(c.get("post_edit_digest") or ""))))

    report("supersession_claim_well_formed", not claim_bad, "%s" % (claim_bad or "-"))
    report("historical_predecessor_pin_preserved", not pred_bad,
           "%s" % (pred_bad or "-"))

    # The chain as the shared resolver builds it: one root, one terminal, no
    # fork, no cycle, and this batch's record is the terminal one.
    records = load_card_records(MANIFEST.parent)
    chain_bad = []
    for c in cards:
        chain, problem = build_chain((c.get("file"), c.get("anchor")),
                                     records=records)
        if problem is not None:
            chain_bad.append("%s#%s %s: %s"
                             % (c.get("file"), c.get("anchor"), problem[0], problem[1]))
            continue
        if chain is None:
            chain_bad.append("%s#%s declares a claim but builds no chain"
                             % (c.get("file"), c.get("anchor")))
            continue
        if chain[0].manifest != PREDECESSOR_MANIFEST:
            chain_bad.append("root is %s, expected %s"
                             % (chain[0].manifest, PREDECESSOR_MANIFEST))
        if chain[-1].manifest != MANIFEST.name:
            chain_bad.append("terminal is %s, expected this batch"
                             % chain[-1].describe())
    report("supersession_chain_is_continuous_and_terminal_here", not chain_bad,
           "%s" % (chain_bad or "-"))

    # ---- 5. the live corpus against the baseline --------------------------
    pages, err = load_baseline(base_ref)
    if pages is None:
        return unavailable("baseline %s: %s" % (base_ref, err))

    changed, qtext_moved = [], []
    total_live = total_base = 0
    for p in sorted(QB_DIR.glob("QB*.html")):
        live_raw = p.read_text(encoding="utf-8", newline="")
        base_raw = pages.get(p.name)
        if base_raw is None:
            continue
        L, B = canonical_cards(live_raw), canonical_cards(base_raw)
        total_live += len(L)
        total_base += len(B)
        for a in set(L) - set(B):
            changed.append("%s#%s (CARD ADDED)" % (p.name, a))
        for a in set(B) - set(L):
            changed.append("%s#%s (CARD REMOVED)" % (p.name, a))
        for a in set(L) & set(B):
            if L[a] != B[a]:
                changed.append("%s#%s" % (p.name, a))
            if qtext_of(L[a]) != qtext_of(B[a]):
                qtext_moved.append("%s#%s" % (p.name, a))

    # A card ADDED since this batch's baseline is legitimate iff some OTHER
    # authorisation record owns it. "Nothing was added since my baseline" stops
    # being true the first time the bank grows for any reason - batch G1 added
    # four cards and turned every E- and F-series guard red at once, none of
    # which was a real finding. The claim this batch can make forever is
    # "nothing was added that nobody authorised".
    sibling_owned = sibling_owned_cards(MANIFEST)
    added = [x for x in changed if "CARD ADDED" in x]
    removed = [x for x in changed if "CARD REMOVED" in x]
    added_legit = [x for x in added if x.split(" ")[0] in sibling_owned]
    added_rogue = [x for x in added if x.split(" ")[0] not in sibling_owned]

    report("canonical_total_unchanged",
           total_base == manifest.get("expected_canonical_questions")
           and total_live == total_base + len(added_legit) - len(removed),
           "baseline %d (manifest expects %s) -> live %d, of which %d addition(s) "
           "authorised elsewhere"
           % (total_base, manifest.get("expected_canonical_questions"), total_live,
              len(added_legit)))

    report("no_new_canonical_card", not added_rogue and not removed,
           "unauthorised additions %s; removals %s"
           % (added_rogue or "-", removed or "-"))

    # A stem reworded on a card ANOTHER authorisation record owns is that
    # record's business, not this batch's. Without this exemption the check
    # asserts "no question text anywhere in the corpus has changed since my
    # baseline", which stops being true the first time any authorised
    # correction rewords a stem -- the same expiry the checks above were
    # already fixed for. A reword on a card NOBODY owns still fails, and so
    # does a reword of this batch's OWN cards, which is what the check is for.
    # THIS BATCH'S OWN CARDS ARE NEVER EXEMPT. QB1_A#q9 is f1b's target and is
    # also owned by batch E1, so a bare `not in sibling_owned` test exempted the
    # very card this check exists to protect - and rewording it was then caught
    # only by manifest_digests_match, which is a different guard answering a
    # different question.
    own_cards = {"%s#%s" % (c.get("file"), c.get("anchor"))
                 for c in (manifest.get("cards") or [])
                 if c.get("file") and c.get("anchor")}
    qtext_unowned = [x for x in qtext_moved
                     if x in own_cards or x not in sibling_owned]
    qtext_elsewhere = sorted(set(qtext_moved) - set(qtext_unowned))
    report("q_text_and_anchors_stable", not qtext_unowned,
           "moved=%s authorised-elsewhere=%s"
           % (qtext_unowned or "-", qtext_elsewhere or "-"))

    authorised_elsewhere = set()
    for sib in authorisation_manifest_paths(MANIFEST.parent):
        if sib == MANIFEST:
            continue
        try:
            sibling = json.loads(sib.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return unavailable("sibling record unreadable: %s" % sib.name)
        for sc in sibling.get("cards", []):
            authorised_elsewhere.add("%s#%s" % (sc.get("file"), sc.get("anchor")))

    authorised = {"%s#%s" % (c.get("file"), c.get("anchor")) for c in cards}
    # Bare "file#anchor": the CARD ADDED / CARD REMOVED suffix used to make a
    # sibling-authorised addition unmatchable, which is what made this guard
    # expire when batch G1 added four cards. A plain edit carries no suffix, so
    # an edit to a card no manifest owns still fails exactly as before.
    unauthorised = sorted(x for x in changed
                          if x.split(" ")[0] not in authorised
                          and x.split(" ")[0] not in authorised_elsewhere)
    exempt = sorted(x for x in changed
                    if x.split(" ")[0] not in authorised
                    and x.split(" ")[0] in authorised_elsewhere)
    report("only_authorised_cards_changed", not unauthorised,
           "unauthorised=%s authorised-elsewhere=%s"
           % (unauthorised or "-", exempt or "-"))

    not_changed = sorted(authorised - set(changed))
    report("every_authorised_card_changed", not not_changed,
           "unchanged=%s" % (not_changed or "-"))

    # F1b is a one-card batch, and this is the tightest statement of ITS blast
    # radius. Subject corrected 22 August 2026 (SKILL 7.5b: change the subject,
    # never stand the check down, never special-case the change that exposed
    # it).
    #
    # As written it compared the raw changed set to F1b's authorised set, with
    # no subtraction of `authorised_elsewhere` -- the very set the check two
    # lines above computes and exempts. So it did not assert "F1b moved one
    # card". It asserted "nothing anywhere has moved since F1b", which is a
    # claim F1b has no standing to make and which expires on the first
    # authorised change that follows it, whatever that change is. The
    # post-release correction CORR-LSA-LIFEBOAT-VENTILATION-20260822 was simply
    # the first one to arrive; any later batch or correction would have tripped
    # it identically. Guard expiry, the same defect class F1b itself hit twice.
    #
    # The subject is now two propositions, both genuinely F1b's own:
    #   - F1b authorises exactly one card, so a later edit cannot quietly widen
    #     a batch documented as one-card;
    #   - the cards that moved, once cards another record authorises are set
    #     aside, are exactly the cards F1b authorised.
    # The first is not implied by any neighbouring check, which is what keeps
    # this one from collapsing into `only_authorised_cards_changed`.
    # Subtract only what ANOTHER record authorises and F1b does not. A plain
    # `changed - authorised_elsewhere` is wrong here and silently empties the
    # set: F1b's own target QB1_A#q9 is declared by F1's manifest too, as the
    # HELD_GOVERNANCE action F1b exists to discharge. Removing it would leave
    # this check asserting nothing at all -- passing hardest exactly when the
    # batch did nothing.
    # Bare "file#anchor" for the same reason as above: a card ADDED by a later
    # authorised batch carries a suffix and would otherwise never be subtracted,
    # making this check fail on every future addition.
    _elsewhere_only = authorised_elsewhere - authorised
    f1b_blast = sorted(x for x in changed if x.split(" ")[0] not in _elsewhere_only)
    report("exactly_one_card_changed_since_baseline",
           len(authorised) == 1 and f1b_blast == sorted(authorised),
           "f1b-authorised=%d changed(excluding authorised-elsewhere)=%s"
           % (len(authorised), f1b_blast or "-"))

    # ---- 6. the limb is there, additively, with its authority -------------
    absent, dupes, digest_bad, add_bad = [], [], [], []
    limb_missing, auth_missing, dirty, edge_missing, timed_bad = [], [], [], [], []
    overclaim, anchor_dupe = [], []
    for c in cards:
        fid, fname, a = c.get("followup_id"), c.get("file"), c.get("anchor")
        raw = (QB_DIR / fname).read_text(encoding="utf-8", newline="")
        live = cards_of(raw)
        based = cards_of(pages.get(fname, ""))
        if a not in live:
            absent.append("%s#%s" % (fname, a))
            continue
        if len(re.findall(r'id="%s"' % re.escape(a), raw)) != 1:
            dupes.append("%s#%s" % (fname, a))
        card = live[a]
        # Entity-unescaped before matching: these pages write "&" as "&amp;",
        # so a guard spelled with a bare "&" could never match the HTML that
        # actually carries the claim. E1's mutation P proved that escape.
        low = html.unescape(card)
        for tok in LIMB_TOKENS.get(fid, []):
            if tok not in low:
                limb_missing.append("%s#%s lacks %r" % (fname, a, tok))
        for tok in AUTHORITY_TOKENS.get(fid, []):
            if tok not in low:
                auth_missing.append("%s#%s lacks %r" % (fname, a, tok))
        if fid in CHAIN_EDGE and CHAIN_EDGE[fid] not in low:
            edge_missing.append("%s#%s lacks the chain edge" % (fname, a))
        for pat in FORBIDDEN_CLAIMS.get(fid, []):
            if re.search(pat, low):
                overclaim.append("%s#%s asserts %r" % (fname, a, pat))
        leak = FORBIDDEN.findall(visible_text(card))
        if leak:
            dirty.append("%s#%s %s" % (fname, a, sorted(set(leak))))

        # The pre-existing Casualty Anchor must survive intact and must NOT be
        # duplicated by the new limb: the register's own instruction was a
        # worked application, not a second casualty mention.
        if low.count("Casualty Anchor") != 1:
            anchor_dupe.append("%s#%s has %d casualty anchors"
                               % (fname, a, low.count("Casualty Anchor")))

        if a in based:
            bb = based[a].replace("\r\n", "\n")
            ll = card.replace("\r\n", "\n")
            sm = difflib.SequenceMatcher(None, bb, ll, autojunk=False)
            bad = [o for o in sm.get_opcodes()
                   if o[0] not in ("equal", "insert")]
            if bad:
                add_bad.append("%s#%s %d non-insert op(s)" % (fname, a, len(bad)))
            if digest16(bb) != c.get("pre_edit_digest"):
                digest_bad.append("%s#%s pre" % (fname, a))
            res = resolve_authorised_card_state(
                manifest=MANIFEST.name, action_id=c["action_id"],
                file=fname, anchor=a,
                pinned_post_digest=c.get("post_edit_digest"),
                live_digest=digest16(ll), directory=MANIFEST.parent)
            if not res.ok:
                digest_bad.append("%s#%s post %s" % (fname, a, res.describe()))
            # A follow-up limb is body-only. The timed answers are the
            # candidate's recall spine; a batch that moves them has changed the
            # canonical answer rather than added a limb.
            for cls in ("oral-15", "oral-60", "practice-block"):
                pat = r'<div class="[^"]*%s[^"]*">(.*?)</div>' % cls
                if re.findall(pat, bb, re.S) != re.findall(pat, ll, re.S):
                    timed_bad.append("%s#%s %s" % (fname, a, cls))

    report("target_cards_present", not absent, "%s" % (absent or "-"))
    report("target_anchors_unique", not dupes, "%s" % (dupes or "-"))
    report("missing_limb_supplied", not limb_missing, "%s" % (limb_missing or "-"))
    report("required_authority_cited", not auth_missing, "%s" % (auth_missing or "-"))
    report("relationship_edge_present_in_card", not edge_missing,
           "%s" % (edge_missing or "-"))
    report("no_unsupported_claim_reintroduced", not overclaim,
           "%s" % (overclaim or "-"))
    report("casualty_anchor_not_duplicated", not anchor_dupe,
           "%s" % (anchor_dupe or "-"))
    report("edits_purely_additive", not add_bad, "%s" % (add_bad or "-"))
    report("manifest_digests_match", not digest_bad, "%s" % (digest_bad or "-"))
    report("timed_blocks_untouched", not timed_bad,
           "%s" % (timed_bad or "-") + (" declared=%s" % cards[0]
                                        .get("timed_blocks_changed")))
    report("no_candidate_visible_metadata", not dirty, "%s" % (dirty or "-"))

    # ---- 7. product invariants -------------------------------------------
    qb_files = sorted(p.name for p in QB_DIR.glob("QB*.html")
                      if canonical_cards(p.read_text(encoding="utf-8",
                                                     newline="")))
    report("question_bearing_file_count",
           len(qb_files) == manifest.get("expected_question_bearing_files"),
           "%d files (manifest expects %s)"
           % (len(qb_files), manifest.get("expected_question_bearing_files")))

    idx = QB_DIR / "qb_content_index.json"
    if not idx.exists():
        return unavailable("derived content index %s is absent" % idx.name)
    try:
        index = json.loads(idx.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return unavailable("content index unreadable: %s" % exc)
    report("content_index_still_describes_the_corpus",
           index.get("total_questions") == total_live
           and index.get("total_files") == len(qb_files),
           "index=%s/%s live=%d/%d"
           % (index.get("total_questions"), index.get("total_files"),
              total_live, len(qb_files)))

    idx_bad = []
    for c in cards:
        entry_f = (index.get("files") or {}).get(c.get("file")) or {}
        rows = [q for q in entry_f.get("questions", [])
                if q.get("anchor") == c.get("anchor")]
        if len(rows) != 1:
            idx_bad.append("%s#%s indexed %d time(s)"
                           % (c.get("file"), c.get("anchor"), len(rows)))
            continue
        live_q = qtext_of(cards_of(
            (QB_DIR / c["file"]).read_text(encoding="utf-8", newline=""))[c["anchor"]])
        indexed = re.sub(r"\s+", " ", str(rows[0].get("q_text") or "")).strip()
        if indexed and html.unescape(indexed) != html.unescape(live_q or ""):
            idx_bad.append("%s#%s q-text desynchronised" % (c["file"], c["anchor"]))
    report("content_index_qtext_still_matches_targets", not idx_bad,
           "%s" % (idx_bad or "-"))

    print("\n%d checks, %d FAIL" % (_checks, len(_failed)))
    if _failed:
        print("failed: %s" % ", ".join(sorted(set(_failed))))
    return 1 if _failed else 0


if __name__ == "__main__":
    sys.exit(main())
