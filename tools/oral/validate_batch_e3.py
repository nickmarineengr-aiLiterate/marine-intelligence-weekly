"""Guard the six authorised E3 cargo/codes/safety-systems ENRICHMENT edits.

batch_e3_enrichment_manifest.json is the authority for which enrichment action
edits which existing file#anchor. This validator proves, against the LIVE QB
HTML and against the consolidation record, that:

  * the manifest carries exactly the consolidation's E3 action set;
  * every action targets the file#anchor the consolidation records, at the
    priority band and family it records;
  * every target card still exists, exactly once, under #q-feed;
  * NO new canonical card was created - the corpus total is unchanged, not
    merely "not regressed";
  * only the six authorised cards differ from the baseline commit;
  * each action's missing limb is now actually present, by required token;
  * each action's required authority is cited on the card;
  * every edit is PURELY ADDITIVE - no baseline character was deleted or
    replaced on any authorised card;
  * the manifest's recorded pre/post digests match reality;
  * the two authorisation corrections still hold;
  * no production metadata is candidate-visible on any touched page;
  * q-text and anchors are untouched - this is enrichment, not re-homing;
  * the examiner relationship count is unchanged.

WHY THE COUNT IS AN EQUALITY HERE, NOT A FLOOR
The new-card guards assert the corpus total as a floor so a later authorised
batch does not break them. An enrichment batch is the opposite case: creating a
card is precisely the failure mode, so E3 asserts strict equality against the
baseline commit it was cut from. That equality cannot expire, because it is
evaluated against a pinned commit rather than against "today".

WHY PURELY-ADDITIVE IS CHECKED AT CHARACTER LEVEL
A line-level comparison is not sufficient on these pages. Several reg-boxes are
a single very long line, so appending a reg-item to one reads as "one line
removed, one line added" - indistinguishable from a rewrite that silently
dropped a baseline reference. Character-level opcodes settle it: if the only
non-equal opcode is `insert`, nothing baseline was touched.

WHY THE CORRECTIONS ARE GUARDED BY NEGATIVE TOKEN
Two E3 limbs were written AGAINST the authorisation record rather than from it,
because primary text contradicted it (A021: SOLAS II-1/56.4 makes the gas-carrier
exclusion conditional; A026: neither AVD manufacturer supports "ceramic-like").
A future well-meaning edit that "restores" the consolidation's wording would
reintroduce a verified-wrong claim, and no positive check would catch it. These
negative tokens fail if that happens.

Exit 0 when every check passes, 1 otherwise.
"""
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oral_manifest import authorisation_manifest_paths  # noqa: E402
from oral_supersession import resolve_authorised_card_state  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
MANIFEST = Path(__file__).resolve().parent / "batch_e3_enrichment_manifest.json"
QB_DIR = REPO / "meoclass1"
CONSOL_REL = ("meoclass1/oral-intelligence/examiner-audit/"
              "FINAL_ORAL_ENRICHMENT_CONSOLIDATION.json")
CONSOL_REF = "origin/research/oral-final-enrichment-consolidation"

# Candidate-visible production vocabulary. Deliberately does NOT ban the plain
# English verb "verify": it appears in legitimate regulatory prose and in a CSS
# class name on these very pages, so banning it guarantees false positives and
# invites someone to weaken the gate to clear them.
FORBIDDEN = re.compile(
    r"ENRICH-A\d|GAP-\d{4}|\bTODO\b|\bFIXME\b|(?<![\w-])VERIFY(?![\w-])"
    r"|\bCORRECTED:|recurrence_class|laptop_review|missing_limb|batch_id"
    r"|production_action|\b[a-z_]+\.(?:json|py|xlsx)\b")

# Tokens that can only be present if the action's missing limb was supplied.
LIMB_TOKENS = {
    "ENRICH-A021": ["IGF Code", "56.2", "56.4", "1 January 2017"],
    "ENRICH-A022": ["maximum stack masses", "approved sight lines",
                    "two ship lengths", "500 m"],
    "ENRICH-A023": ["entire available length", "aftermost hatchway",
                    "one-third of the extreme breadth"],
    "ENRICH-A024": ["suitably stiffened", "one-hour standard fire test",
                    "A-0 = 0 min"],
    "ENRICH-A025": ["hanging bars", "tare", "1.8 to 2.2 N/mm", "2.2.4.11"],
    "ENRICH-A026": ["vermiculite", "mist", "not electrically conductive",
                    "platelets"],
}

# Authority that must remain cited on the card for the limb to stand up.
AUTHORITY_TOKENS = {
    "ENRICH-A021": ["MSC.391(95)", "SOLAS II-1/56"],
    "ENRICH-A022": ["MSC.1/Circ.1353/Rev.2"],
    "ENRICH-A023": ["ICLL"],
    "ENRICH-A024": ["Regulation 3.2"],
    "ENRICH-A025": ["FSS Code Ch.5"],
    "ENRICH-A026": ["MSC.1/Circ.1615"],
}

# Claims that primary/OEM verification DISPROVED. Reintroducing one is a
# regression even though it would restore the authorisation record's wording.
FORBIDDEN_CLAIMS = {
    # "reckon" appears zero times in the whole Load Line Convention.
    "ENRICH-A023": ["reckoning"],
    # Neither AVD manufacturer describes the residue as ceramic.
    "ENRICH-A026": ["ceramic"],
}

# Conditions that must accompany a claim for it to stay true.
REQUIRED_QUALIFIER = {
    # 56.4 disapplies Part G only on conditions; stating the exclusion without
    # the condition is the over-absolute reading the consolidation carried.
    "ENRICH-A021": ["storage and distribution"],
}

VALID_STATUS = {"IMPLEMENTED", "IMPLEMENTED_REDUCED_SCOPE"}

_fails = []
_checks = 0


def report(name, ok, detail=""):
    global _checks
    _checks += 1
    print("%-5s %-44s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        _fails.append(name)


CARD_OPEN = re.compile(r'<div class="q-card[^"]*"[^>]*>', re.I)
CANONICAL_ANCHOR = re.compile(r"q\d+")


def _balanced_end(text, start):
    depth = 0
    for m in re.finditer(r"<div\b[^>]*>|</div\s*>", text[start:], re.I):
        depth += -1 if m.group(0).startswith("</") else 1
        if depth == 0:
            return start + m.end()
    raise AssertionError("unbalanced q-card at %d" % start)


def cards_of(text):
    """anchor -> card HTML, on LF-normalised text.

    LF-normalised because .gitattributes pins these pages to LF in the object
    store while the working tree may hold CRLF per file - and it genuinely
    differs per file here: QB2_H is LF while QB2_A, QB2_B, QB2_G and QB8_G are
    CRLF. A raw-byte compare would report every card on a CRLF checkout as
    changed.
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
    carries 723 .q-card blocks against 721 canonical questions, because some
    pages reuse the class for structural blocks. Counting the class rather than
    the anchor convention inflates the corpus by two and lets a count assertion
    pass vacuously.
    """
    return {a: c for a, c in cards_of(text).items()
            if CANONICAL_ANCHOR.fullmatch(a)}


def git_show(ref, rel):
    r = subprocess.run(["git", "show", "%s:%s" % (ref, rel)],
                       cwd=REPO, capture_output=True)
    if r.returncode != 0 or not r.stdout:
        return None
    return r.stdout.decode("utf-8", "replace")


def load_consolidation(manifest):
    p = REPO / CONSOL_REL
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8")), "tree"
    raw = git_show(manifest.get("authorisation_commit") or CONSOL_REF, CONSOL_REL)
    if raw is None:
        raw = git_show(CONSOL_REF, CONSOL_REL)
    if raw is None:
        return None, "unavailable"
    return json.loads(raw), "git"


def visible_text(card):
    return re.sub(r"<[^>]+>", " ", card)


def digest16(s):
    import hashlib
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cards = manifest["cards"]
    base = manifest["baseline_commit"]

    # ---- manifest must match the consolidation's E3 set exactly ----
    consol, src = load_consolidation(manifest)
    if consol is None:
        report("authorised_action_set", False,
               "consolidation unavailable (%s) - cannot confirm linkage" % src)
        report("authorised_targets", False, "consolidation unavailable")
        report("authorised_enrichment_disposition", False,
               "consolidation unavailable")
    else:
        batch = [b for b in consol["batches"] if b["batch_id"] == "E3"]
        want = set(batch[0]["action_ids"]) if batch else set()
        got = {c["action_id"] for c in cards}
        report("authorised_action_set", want == got and len(got) == 6,
               "manifest %d vs consolidation %d; extra=%s missing=%s [%s]"
               % (len(got), len(want), sorted(got - want) or "-",
                  sorted(want - got) or "-", src))

        pa = {a["action_id"]: a for a in consol["production_actions"]}
        bad_t, bad_d = [], []
        for c in cards:
            a = pa.get(c["action_id"])
            if a is None:
                bad_t.append(c["action_id"] + "(absent)")
                continue
            if a.get("target") != "%s#%s" % (c["file"].replace(".html", ""),
                                             c["anchor"]):
                bad_t.append("%s(target %s != %s#%s)" % (
                    c["action_id"], a.get("target"),
                    c["file"].replace(".html", ""), c["anchor"]))
            if a.get("batch") != "E3":
                bad_d.append("%s(batch %s)" % (c["action_id"], a.get("batch")))
            if a.get("family_ids", [None])[0] != c["family_id"]:
                bad_d.append("%s(family)" % c["action_id"])
            if a.get("priority") != c["priority"]:
                bad_d.append("%s(priority)" % c["action_id"])
        report("authorised_targets", not bad_t, "%s" % (sorted(set(bad_t)) or "-"))
        report("authorised_enrichment_disposition", not bad_d,
               "%s" % (sorted(set(bad_d)) or "-"))

    bad_status = [c["action_id"] for c in cards
                  if c.get("status") not in VALID_STATUS]
    report("action_status_declared", not bad_status, "%s" % (bad_status or "-"))

    # ---- enrichment creates no cards: strict equality vs the baseline ----
    changed, absent, dupes, outside = [], [], [], []
    limb_missing, auth_missing, dirty, qtext_moved = [], [], [], []
    total_base = total_live = 0
    by_file = {}
    for c in cards:
        by_file.setdefault(c["file"], []).append(c)

    all_pages = sorted(p.name for p in QB_DIR.glob("QB*.html"))
    for fname in all_pages:
        live_raw = (QB_DIR / fname).read_text(encoding="utf-8", newline="")
        base_raw = git_show(base, "meoclass1/" + fname)
        if base_raw is None:
            continue
        L, B = canonical_cards(live_raw), canonical_cards(base_raw)
        total_live += len(L)
        total_base += len(B)
        for a in set(L) - set(B):
            changed.append("%s#%s (CARD ADDED)" % (fname, a))
        for a in set(B) - set(L):
            changed.append("%s#%s (CARD REMOVED)" % (fname, a))
        for a in set(L) & set(B):
            if L[a] != B[a]:
                changed.append("%s#%s" % (fname, a))
            ql = re.search(r'<div class="q-text">(.*?)</div>', L[a], re.S)
            qb = re.search(r'<div class="q-text">(.*?)</div>', B[a], re.S)
            if ql and qb and ql.group(1).strip() != qb.group(1).strip():
                qtext_moved.append("%s#%s" % (fname, a))

    report("canonical_total_unchanged", total_live == total_base
           and total_live == manifest["expected_canonical_questions"],
           "baseline %d -> live %d (manifest expects %d)"
           % (total_base, total_live, manifest["expected_canonical_questions"]))

    report("no_new_canonical_card",
           not [x for x in changed if "CARD ADDED" in x or "CARD REMOVED" in x],
           "%s" % ([x for x in changed if "CARD" in x] or "-"))

    # A card that a SIBLING batch manifest authorises is legitimate here too.
    # Built in from the start rather than left to expire: without it this check
    # forbids every future authorised edit anywhere in the corpus and fails the
    # moment E2, E5 or E6 lands - the same guard-expiry defect E3 had to repair
    # in validate_batch_e4.py. Exempt cards are reported BY NAME.
    #
    # Not a weakening: the exemption is keyed on a plain "file#anchor" and the
    # CARD ADDED / CARD REMOVED entries carry a suffix, so they can never match
    # it; an edit to a card no manifest owns still fails (mutation C).
    authorised_elsewhere = set()
    for sib in authorisation_manifest_paths(MANIFEST.parent):
        if sib == MANIFEST:
            continue
        for sc in json.loads(sib.read_text(encoding="utf-8")).get("cards", []):
            authorised_elsewhere.add("%s#%s" % (sc["file"], sc["anchor"]))

    authorised = {"%s#%s" % (c["file"], c["anchor"]) for c in cards}
    unauthorised = sorted(set(changed) - authorised - authorised_elsewhere)
    exempt = sorted((set(changed) - authorised) & authorised_elsewhere)
    report("only_authorised_cards_changed", not unauthorised,
           "unauthorised=%s authorised-elsewhere=%s"
           % (unauthorised or "-", exempt or "-"))

    not_changed = sorted(authorised - set(changed))
    report("every_authorised_card_changed", not not_changed,
           "unchanged=%s" % (not_changed or "-"))

    report("q_text_and_anchors_stable", not qtext_moved,
           "moved=%s" % (qtext_moved or "-"))

    # ---- the limb is actually there, and its authority with it ----
    additive_bad, digest_bad, claim_bad, qual_bad = [], [], [], []
    for fname, wanted in sorted(by_file.items()):
        raw = (QB_DIR / fname).read_text(encoding="utf-8", newline="")
        live = cards_of(raw)
        base_raw = git_show(base, "meoclass1/" + fname)
        based = cards_of(base_raw) if base_raw else {}
        for c in wanted:
            a = c["anchor"]
            if a not in live:
                absent.append("%s#%s" % (fname, a))
                continue
            if len(re.findall(r'id="%s"' % re.escape(a), raw)) != 1:
                dupes.append("%s#%s" % (fname, a))
            if raw.find('id="q-feed"') > raw.find('id="%s"' % a):
                outside.append("%s#%s" % (fname, a))
            card = live[a]
            low = card.lower()
            for tok in LIMB_TOKENS.get(c["action_id"], []):
                if tok.lower() not in low:
                    limb_missing.append("%s#%s lacks %r" % (fname, a, tok))
            for tok in AUTHORITY_TOKENS.get(c["action_id"], []):
                if tok.lower() not in low:
                    auth_missing.append("%s#%s lacks %r" % (fname, a, tok))
            for tok in FORBIDDEN_CLAIMS.get(c["action_id"], []):
                if tok.lower() in low:
                    claim_bad.append("%s#%s reintroduced %r" % (fname, a, tok))
            for tok in REQUIRED_QUALIFIER.get(c["action_id"], []):
                if tok.lower() not in low:
                    qual_bad.append("%s#%s lost qualifier %r" % (fname, a, tok))
            leak = FORBIDDEN.findall(visible_text(card))
            if leak:
                dirty.append("%s#%s %s" % (fname, a, sorted(set(leak))))

            # purely additive, at character level
            if a in based:
                bb = based[a].replace("\r\n", "\n")
                ll = card.replace("\r\n", "\n")
                sm = difflib.SequenceMatcher(None, bb, ll, autojunk=False)
                bad = [o for o in sm.get_opcodes()
                       if o[0] not in ("equal", "insert")]
                if bad:
                    additive_bad.append("%s#%s %d non-insert op(s)"
                                        % (fname, a, len(bad)))
                if digest16(bb) != c.get("pre_edit_digest"):
                    digest_bad.append("%s#%s pre" % (fname, a))
                # The pin is never rewritten and never relaxed. When a later
                # authorised record declares that it supersedes this state, this
                # check stops asking "is my state live?" and starts asking "is my
                # state the ancestor of what is live?" -- which is a strictly
                # stronger claim, because the whole chain must be continuous and
                # its terminal state must be the live card. With no successor
                # declared this is byte-for-byte the original comparison.
                res = resolve_authorised_card_state(
                    manifest=MANIFEST.name, action_id=c["action_id"],
                    file=fname, anchor=a,
                    pinned_post_digest=c.get("post_edit_digest"),
                    live_digest=digest16(ll), directory=MANIFEST.parent)
                if not res.ok:
                    digest_bad.append("%s post %s" % ("%s#%s" % (fname, a), res.describe()))

    report("target_cards_present", not absent, "%s" % (absent or "-"))
    report("target_anchors_unique", not dupes, "%s" % (dupes or "-"))
    report("target_cards_under_q_feed", not outside, "%s" % (outside or "-"))
    report("missing_limb_supplied", not limb_missing,
           "%s" % (limb_missing or "-"))
    report("required_authority_cited", not auth_missing,
           "%s" % (auth_missing or "-"))
    report("edits_purely_additive", not additive_bad,
           "%s" % (additive_bad or "-"))
    report("manifest_digests_match", not digest_bad, "%s" % (digest_bad or "-"))
    report("disproved_claims_absent", not claim_bad, "%s" % (claim_bad or "-"))
    report("conditional_qualifiers_kept", not qual_bad, "%s" % (qual_bad or "-"))
    report("no_candidate_visible_metadata", not dirty, "%s" % (dirty or "-"))

    # ---- no relationship delta is authorised for an enrichment batch ----
    r = subprocess.run([sys.executable, "tools/oral/build_examiner_index.py",
                        "--check"], cwd=REPO, capture_output=True)
    out = r.stdout.decode("utf-8", "replace")
    m = re.search(r"relationships (\d+)\s+examiners (\d+)", out)
    got_rel = int(m.group(1)) if m else -1
    got_ex = int(m.group(2)) if m else -1
    report("examiner_relationship_delta_zero",
           r.returncode == 0
           and got_rel == manifest["expected_examiner_relationships"]
           and got_ex == manifest["expected_examiners"],
           "relationships %s (expect %s), examiners %s (expect %s), gate exit %d"
           % (got_rel, manifest["expected_examiner_relationships"],
              got_ex, manifest["expected_examiners"], r.returncode))

    report("manifest_declares_no_new_cards",
           manifest.get("creates_new_cards") is False,
           "creates_new_cards=%s" % manifest.get("creates_new_cards"))

    print("\nE3 enrichment validator: %d checks, %d FAIL" % (_checks, len(_fails)))
    if _fails:
        print("failed:", ", ".join(_fails))
    return 1 if _fails else 0


if __name__ == "__main__":
    sys.exit(main())
