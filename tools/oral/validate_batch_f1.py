#!/usr/bin/env python3
"""Release guard for Oral follow-up production batch F1.

WHAT F1 IS
----------
The first production batch derived from the committed follow-up authorisation
register (``oral_followup_register.json``) rather than from the enrichment
consolidation.  F1 was authorised as three actions -- FUP-006, FUP-018 and
FUP-033 -- of which FUP-018 and FUP-033 are IMPLEMENTED and FUP-006 is HELD.

WHY THE HOLD IS CHECKED AND NOT MERELY DOCUMENTED
-------------------------------------------------
A held action is the easiest thing in this pipeline to lose: it appears in no
``cards[]`` entry, so nothing would notice it going missing.  This validator
therefore asserts the AUTHORISED set (all three resolve in the register), the
IMPLEMENTED set (exactly the two), and that the held one is still named with a
reason.  Dropping FUP-006 silently is a failure here, not a tidy-up.

FAIL-CLOSED
-----------
If the register or the manifest is unavailable this reports ``unavailable`` and
returns non-zero.  It never skips: a guard that cannot read its authorisation
record has not passed, it has failed to run.

PERFORMANCE IS A CORRECTNESS PROPERTY
-------------------------------------
E6's first validator called ``git show`` 172 times and took 91 seconds; the
mutation suite runs a validator ~35 times, which made a 50-minute run and a
guard people skip.  The baseline corpus here is loaded with ONE ``git archive``
of ``meoclass1/`` rather than one ``git show`` per page.
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

from oral_manifest import authorisation_manifest_paths, HELD_STATUSES  # noqa: E402
from oral_supersession import resolve_authorised_card_state  # noqa: E402

MANIFEST = HERE / "batch_f1_manifest.json"
REGISTER = HERE / "oral_followup_register.json"

# The batch as AUTHORISED, and the batch as IMPLEMENTED. They differ by one
# held action and the difference is asserted, never assumed.
AUTHORISED_FUPS = {"FUP-006", "FUP-018", "FUP-033"}
IMPLEMENTED_FUPS = {"FUP-018", "FUP-033"}
HELD_FUPS = AUTHORISED_FUPS - IMPLEMENTED_FUPS

# The placeholder the register carries for every action. A producing batch must
# replace it with a real governed class; shipping the placeholder means the
# technical scoping never happened.
PLACEHOLDER_CLASS = "UNCLASSIFIED_PENDING_BATCH_SCOPING"

# Actions permitted to create a canonical card. Empty by design, and asserted
# against an explicitly empty set so "no new cards" is a decision on record
# rather than an accident of this batch's content.
NEW_CARD_EXCEPTIONS: set = set()

# Substrings that must survive in each implemented card. These are the LIMB --
# what the examiner actually asked for -- not decoration. Chosen to be specific
# enough that deleting the limb cannot leave them behind.
LIMB_TOKENS = {
    "FUP-018": ["Why Barnacles in Particular Cannot Attach",
                "cyprid",
                "hydrophobic lipid",
                "phosphoprotein",
                "bound into the hydrophilic polymer network"],
    "FUP-033": ["Marine Insurance Against Motor Insurance",
                "compulsory by statute",
                "valued policy",
                "Insured Declared Value",
                "mutual association of shipowners"],
}

# The authority each limb is required to cite. A claim whose source vanishes is
# an unsourced claim, so these are checked separately from the limb itself.
AUTHORITY_TOKENS = {
    "FUP-018": ["Nature Communications", "5:4414",
                "Science and Technology of Advanced Materials", "064706"],
    "FUP-033": ["Motor Vehicles Act, 1988", "Section 146",
                "Section 6, MIA 1906", "Section 27(3), MIA 1906",
                "Marine Insurance Act, 1963"],
}

# The directed edge must be walkable as DATA, not merely readable as prose --
# a later examiner simulator has to find it without parsing English.
CHAIN_EDGE = {
    "FUP-033": "How does marine insurance differ from car insurance?",
}

# Internal production vocabulary that must never reach a candidate.
FORBIDDEN = re.compile(
    r"\b(?:FUP-\d+|GAP-\d+|ASC-\d+|ENRICH-A\d+|followup_id|relationship_edge|"
    r"verification_scope|pre_edit_digest|post_edit_digest|"
    r"target_review_status|recurrence_class|LAPTOP_CONFIRMED)\b")

CARD_OPEN = re.compile(r'<div class="q-card"[^>]*>')
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

    Identical to the E1-E6 implementation on purpose: this batch's digests must
    be computed over exactly the same card boundaries as every historical
    guard's, or a digest would mean something different per validator.
    """
    depth = 0
    for m in re.finditer(r"<div\b[^>]*>|</div\s*>", text[start:], re.I):
        depth += -1 if m.group(0).startswith("</") else 1
        if depth == 0:
            return start + m.end()
    raise AssertionError("unbalanced q-card at %d" % start)


def cards_of(text):
    """anchor -> card HTML, on LF-normalised text.

    LF-normalised because .gitattributes pins these pages to LF in the object
    store while the working tree may hold CRLF per file -- and it genuinely
    differs per file here (QB3_I.html is CRLF on disk, QB9_C.html is LF). A
    raw-byte compare would report every card on a CRLF checkout as changed.
    """
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

    A .q-card div is not the same thing as a canonical question: the corpus
    carries more .q-card blocks (723) than canonical questions (721), because
    some pages reuse the class for structural blocks. Counting the class rather
    than the anchor convention inflates the corpus and lets a count assertion
    pass vacuously.
    """
    return {a: c for a, c in cards_of(text).items()
            if CANONICAL_ANCHOR.fullmatch(a)}


def visible_text(card):
    return re.sub(r"<[^>]+>", " ", card)


def qtext_of(card):
    m = re.search(r'class="q-text"[^>]*>(.*?)</div>', card, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else None


def load_baseline(ref):
    """Every meoclass1/*.html at ``ref``, via ONE git archive. See module head."""
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
            base = name.rsplit("/", 1)[-1]
            if "/" in name[len("meoclass1/"):]:
                continue          # subdirectories (oralnotes, pastpapers)
            fh = tar.extractfile(member)
            if fh is not None:
                pages[base] = fh.read().decode("utf-8", "replace")
    return pages, None


def main():
    if not MANIFEST.exists():
        return unavailable("manifest %s is absent" % MANIFEST.name)
    if not REGISTER.exists():
        return unavailable("register %s is absent" % REGISTER.name)
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        register = json.loads(REGISTER.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return unavailable("authorisation record unreadable: %s" % exc)

    cards = manifest.get("cards") or []
    base_ref = manifest.get("baseline_commit")
    reg_actions = {a.get("followup_id"): a for a in register.get("actions") or []}

    # ---- 1. the authorised set, the implemented set, and the held one ------
    missing_auth = sorted(f for f in AUTHORISED_FUPS if f not in reg_actions)
    report("authorised_fup_set_resolves_in_register", not missing_auth,
           "authorised=%s unresolved=%s"
           % (sorted(AUTHORISED_FUPS), missing_auth or "none"))

    declared = [c.get("followup_id") for c in cards]
    report("implemented_set_is_exactly_the_two_produced",
           sorted(declared) == sorted(IMPLEMENTED_FUPS),
           "declared=%s expected=%s" % (sorted(declared), sorted(IMPLEMENTED_FUPS)))

    report("action_id_and_followup_id_agree",
           all(c.get("action_id") == c.get("followup_id") for c in cards),
           "; ".join("%s/%s" % (c.get("action_id"), c.get("followup_id"))
                     for c in cards))

    # A held action leaves no cards[] trace, so nothing else in the pipeline
    # would notice it disappearing. It must stay declared as STRUCTURE -- an
    # id, a governed status, the target, and a blocker a reader can act on.
    # Prose in `note` would not be assertable, and "we were never asked to do
    # it" must never become indistinguishable from "we held it and said so".
    held = manifest.get("held_actions") or []
    held_ids = sorted(h.get("followup_id") for h in held)
    report("held_action_is_declared_as_structure",
           held_ids == sorted(HELD_FUPS),
           "declared=%s expected=%s" % (held_ids, sorted(HELD_FUPS)))

    bad_hold = []
    for h in held:
        if h.get("status") not in HELD_STATUSES:
            bad_hold.append("%s status=%s" % (h.get("followup_id"), h.get("status")))
        rec = reg_actions.get(h.get("followup_id")) or {}
        want = "%s#%s" % (rec.get("parent_file"), rec.get("parent_anchor"))
        if h.get("target") != want:
            bad_hold.append("%s target=%s != register %s"
                            % (h.get("followup_id"), h.get("target"), want))
        for field in ("blocker", "blocking_manifest", "blocking_validator",
                      "blocking_check", "empirical_proof", "resolution_owner"):
            if not h.get(field):
                bad_hold.append("%s lacks %s" % (h.get("followup_id"), field))
        # A hold means the work is still owed. A hold that quietly says
        # otherwise is a withdrawal wearing a hold's name.
        if h.get("work_still_owed") is not True:
            bad_hold.append("%s does not record the work as still owed"
                            % h.get("followup_id"))
    report("held_action_blocker_is_actionable", not bad_hold,
           "%s" % (bad_hold or "-"))

    # The register must NOT have been edited to disguise the hold: the held
    # action stays AUTHORISED_NOT_STARTED there, and the batch carries the
    # status. Two competing status sources is the failure being prevented.
    reg_status = [(h.get("followup_id"),
                   (reg_actions.get(h.get("followup_id")) or {}).get("status"))
                  for h in held]
    report("register_status_of_held_action_untouched",
           all(s == "AUTHORISED_NOT_STARTED" for _, s in reg_status),
           "%s" % (reg_status or "-"))

    report("held_action_is_not_silently_implemented",
           not (set(declared) & HELD_FUPS),
           "declared=%s held=%s" % (sorted(declared), sorted(HELD_FUPS)))

    # ---- 2. every card matches its register record, field by field --------
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

    # ---- 3. the live corpus against the baseline --------------------------
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

    report("canonical_total_unchanged",
           total_live == total_base
           and total_live == manifest.get("expected_canonical_questions"),
           "baseline %d -> live %d (manifest expects %s)"
           % (total_base, total_live, manifest.get("expected_canonical_questions")))

    report("no_new_canonical_card",
           not [x for x in changed if "CARD " in x],
           "%s" % ([x for x in changed if "CARD " in x] or "-"))

    report("q_text_and_anchors_stable", not qtext_moved,
           "moved=%s" % (qtext_moved or "-"))

    # A card a SIBLING record authorises is legitimate here too. Built in from
    # the start rather than left to expire. The CARD ADDED / CARD REMOVED
    # entries carry a suffix, so they can never match a plain "file#anchor".
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
    unauthorised = sorted(set(changed) - authorised - authorised_elsewhere)
    exempt = sorted((set(changed) - authorised) & authorised_elsewhere)
    report("only_authorised_cards_changed", not unauthorised,
           "unauthorised=%s authorised-elsewhere=%s"
           % (unauthorised or "-", exempt or "-"))

    not_changed = sorted(authorised - set(changed))
    report("every_authorised_card_changed", not not_changed,
           "unchanged=%s" % (not_changed or "-"))

    # FUP-006's target must be untouched while the action is held. Editing it
    # anyway is the specific accident this hold exists to prevent.
    held_target = "QB1_A.html#q9"
    report("held_action_target_untouched",
           held_target not in set(changed),
           "%s changed=%s" % (held_target, held_target in set(changed)))

    # ---- 4. the limb is actually there, additively, with its authority ----
    absent, dupes, digest_bad, add_bad = [], [], [], []
    limb_missing, auth_missing, dirty, edge_missing, timed_bad = [], [], [], [], []
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
        # so a guard spelled "Ahmed & Gong" could never match the HTML that
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
        leak = FORBIDDEN.findall(visible_text(card))
        if leak:
            dirty.append("%s#%s %s" % (fname, a, sorted(set(leak))))

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
            # The pin is never rewritten and never relaxed. When a later
            # authorised record declares that it supersedes this state, this
            # check stops asking "is my state live?" and starts asking "is my
            # state the ancestor of what is live?" -- a strictly stronger claim,
            # because the whole chain must be continuous and its terminal state
            # must be the live card. With no successor declared this is
            # byte-for-byte the original comparison.
            res = resolve_authorised_card_state(
                manifest=MANIFEST.name, action_id=c["action_id"],
                file=fname, anchor=a,
                pinned_post_digest=c.get("post_edit_digest"),
                live_digest=digest16(ll), directory=MANIFEST.parent)
            if not res.ok:
                digest_bad.append("%s#%s post %s" % (fname, a, res.describe()))
            # A follow-up limb is body-only. The timed answers are the
            # candidate's recall spine and a batch that moves them has changed
            # the canonical answer, not added a limb.
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
    report("edits_purely_additive", not add_bad, "%s" % (add_bad or "-"))
    report("manifest_digests_match", not digest_bad, "%s" % (digest_bad or "-"))
    report("timed_blocks_untouched", not timed_bad,
           "%s" % (timed_bad or "-") + (" declared=%s" % manifest.get("cards")[0]
                                        .get("timed_blocks_changed")))
    report("no_candidate_visible_metadata", not dirty, "%s" % (dirty or "-"))

    # ---- 5. product invariants -------------------------------------------
    qb_files = sorted(p.name for p in QB_DIR.glob("QB*.html")
                      if canonical_cards(p.read_text(encoding="utf-8",
                                                     newline="")))
    report("question_bearing_file_count",
           len(qb_files) == manifest.get("expected_question_bearing_files"),
           "%d files (manifest expects %s)"
           % (len(qb_files), manifest.get("expected_question_bearing_files")))

    # The content index keys identity on file + anchor and carries q-text.
    # F1 moved neither, so the index must still describe the corpus WITHOUT
    # regeneration. This is the cheap invariant only -- that the derived
    # manifest still counts the corpus it indexes. Whether regenerating is a
    # true no-op is the separate `content_index_check` gate's job, and
    # duplicating it here would just make this validator slow.
    idx = REPO / "meoclass1" / "qb_content_index.json"
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

    # The index carries each card's question text. F1 changed no q-text, so
    # every indexed q-text for a target card must still match the live card --
    # a targeted check that the two edited pages did not desynchronise the
    # index even though the totals are unchanged.
    idx_bad = []
    for c in cards:
        entry = (index.get("files") or {}).get(c.get("file")) or {}
        rows = [q for q in entry.get("questions", [])
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
