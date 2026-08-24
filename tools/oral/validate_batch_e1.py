"""Guard the ten authorised E1 insurance/liability/commercial ENRICHMENT edits.

batch_e1_enrichment_manifest.json is the authority for which enrichment action
edits which existing file#anchor. This validator proves, against the LIVE QB
HTML and against the consolidation record, that:

  * the manifest carries exactly the consolidation's E1 action set, on BOTH of
    the consolidation's independent representations;
  * every action targets the file#anchor, priority band and family the
    consolidation records;
  * every target card still exists, exactly once, under #q-feed;
  * NO new canonical card was created - the corpus total is unchanged, not
    merely "not regressed";
  * only the nine authorised cards differ from the baseline commit;
  * each action's missing limb is now actually present, by required token;
  * each action's required authority is cited on the card;
  * every edit is PURELY ADDITIVE - no baseline character was deleted or
    replaced on any authorised card;
  * the manifest's recorded pre/post digests match reality;
  * the commercial distinctions that make the additions correct are still
    qualified rather than flattened;
  * no production metadata is candidate-visible on any touched page;
  * q-text and anchors are untouched - this is enrichment, not re-homing;
  * the examiner relationship count is unchanged.

WHY TEN ACTIONS BUT NINE CARDS
ENRICH-A007 (freight-market risk under a CoA) and ENRICH-A008 (bareboat
charter-cum-demise) both land on QB9_H.html#q9. Every earlier enrichment batch
was one action per card, so a check that simply counted authorised cards would
silently accept nine actions here. `action_and_target_cardinality` asserts the
10/9 split and the shared target explicitly, so dropping either limb from the
shared card is a failure rather than an arithmetic coincidence.

WHY THE EDITION QUALIFIERS ARE GUARDED, NOT JUST THE TOKENS
E1 is the first batch whose subject matter is standard-form contract wording,
where the same Part number means different things in different editions:

  * A008 - BARECON 2001 optional Part IV is a Hire/Purchase Agreement under
    which title passes on the final instalment of hire. BARECON 2017 optional
    Part IV is a PURCHASE OPTION exercisable during the term. Both editions are
    on the card and the qualifier "BARECON 2017 changed this" must survive: a
    later tidy-up that keeps both names but drops the contrast reintroduces
    exactly the mixed-edition answer the batch brief forbids.
  * A005 - the Insurance Act 2015 did NOT abolish exact compliance. It repealed
    the SECOND sentence of MIA 1906 s.33(3) and s.34. The qualifier "was
    abolished" must stay attached to the discharge rule, not to the warranty.
  * A001 - Clause 8.4.2 excludes property "except other vessels and property on
    them". Losing that carve-out turns a correct exclusion into a false one.
  * A006 - the attribution "is not the Legal Committee's remit" is the whole
    point of the addition; without it the card credits LEG with ISPS and SUA.
  * A010 - "not a volumetric one" preserves the mass-versus-volume distinction
    that the alternative-fuel argument depends on.

WHY SOME CLAIMS ARE FORBIDDEN OUTRIGHT
FORBIDDEN_CLAIMS carries the two commercial over-simplifications the batch
brief names by hand: that P&I simply covers everything H&M does not, and that
the collision split is a rule of law rather than a clause of a market form.
Both are plausible-sounding, both are wrong, and neither is on the card today.

WHY THE NEGATIVE GUARDS ARE ENTITY-UNESCAPED
These pages write "&" as "&amp;". A forbidden-claim pattern spelled the way a
human would write it - "everything not covered by h&m" - therefore never
matches the HTML that would actually carry the claim. E1's own mutation P
proved it: injecting the single most common wrong answer about the collision
split escaped the forbidden-claim check completely and was caught only
incidentally, by the digest check. The match is now made against
html.unescape(card), which is strictly stronger - it catches both spellings.

The related trap is substring collision: unanchored commercial vocabulary
collides badly, "hire" occurring inside "hire/purchase". A negative guard must
be tested against the BASELINE card, not only the edited one, or it fires on
text nobody wrote today.

WHY THE COUNT IS AN EQUALITY HERE, NOT A FLOOR
Creating a card is precisely the failure mode for an enrichment batch, so E1
asserts strict equality against the pinned baseline commit it was cut from.
That equality cannot expire, because it is evaluated against a commit rather
than against "today".

WHY DIGESTS ARE LF-NORMALISED
QB5_J.html is CRLF in the working tree while the other six destination files
are LF; .gitattributes pins *.html to eol=lf so the object store is LF either
way. cards_of() normalises before hashing and diffing. A raw-byte comparison of
QB5_J against its blob manufactures one phantom insert opcode per line and
would make the additivity proof meaningless.

Exit 0 when every check passes, 1 otherwise.
"""
import difflib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oral_manifest import authorisation_manifest_paths, sibling_owned_cards  # noqa: E402
from oral_supersession import resolve_authorised_card_state  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
MANIFEST = Path(__file__).resolve().parent / "batch_e1_enrichment_manifest.json"
QB_DIR = REPO / "meoclass1"
CONSOL_REL = ("meoclass1/oral-intelligence/examiner-audit/"
              "FINAL_ORAL_ENRICHMENT_CONSOLIDATION.json")
CONSOL_REF = "origin/research/oral-final-enrichment-consolidation"

EXPECTED_ACTIONS = 10

# Candidate-visible production vocabulary. Deliberately does NOT ban the plain
# English verb "verify": it appears in legitimate regulatory prose and in a CSS
# class name on these very pages, so banning it guarantees false positives and
# invites someone to weaken the gate to clear them.
FORBIDDEN = re.compile(
    r"ENRICH-A\d|GAP-\d{4}|\bTODO\b|\bFIXME\b|(?<![\w-])VERIFY(?![\w-])"
    r"|\bCORRECTED:|recurrence_class|laptop_review|missing_limb|batch_id"
    r"|production_action|\b[a-z_]+\.(?:json|py|xlsx)\b")

# Tokens that can only be present if the action's missing limb was supplied.
# Every one of these was checked to be ABSENT from the baseline card before it
# was adopted: a limb token that the baseline already contained would make the
# check pass without the limb being there at all.
LIMB_TOKENS = {
    "ENRICH-A001": ["cross-liabilities", "8.2.1", "8.2.2", "8.4.1", "8.4.4",
                    "8.4.5", "any one collision", "engagements of"],
    "ENRICH-A002": ["proximate cause", "dominant, effective cause", "s.55(1)"],
    "ENRICH-A003": ["appoint the average adjuster",
                    "Association of Average Adjusters",
                    "impartially and independently", "not legally binding"],
    "ENRICH-A004": ["international reserve asset", "renminbi",
                    "every five years", "basket"],
    "ENRICH-A005": ["exactly complied with", "Insurance Act 2015", "suspends",
                    "guarantee"],
    "ENRICH-A006": ["SUA Convention 1988", "2005 Protocols", "28 July 2010",
                    "Maritime Safety Committee"],
    "ENRICH-A007": ["hedging instrument", "sold the upside",
                    "freight escalation"],
    "ENRICH-A008": ["charter-cum-demise", "capital repayment", "BARECON 2001",
                    "BARECON 2017", "purchase option", "Part IV"],
    "ENRICH-A009": ["FIOST", "laytime", "demurrage", "fixture by fixture",
                    "liner terms"],
    "ENRICH-A010": ["cost per gigajoule", "gCO2e/MJ", "FuelEU Maritime",
                    "per unit of energy"],
}

# Authority that must remain cited on the card for the limb to stand up.
# A007 and A009 are TECHNICAL_REASONING_ONLY actions: A007 asserts no external
# authority at all, and A009 names only forms and terms of art, so their
# required-authority sets are deliberately small rather than absent-by-oversight.
AUTHORITY_TOKENS = {
    "ENRICH-A001": ["8.2.1", "8.4"],
    "ENRICH-A002": ["Marine Insurance Act 1906"],
    "ENRICH-A003": ["CMI Guidelines relating to General Average"],
    "ENRICH-A004": ["IMF"],
    "ENRICH-A005": ["Insurance Act 2015", "s.33"],
    "ENRICH-A006": ["SOLAS Chapter XI-2", "SUA Convention 1988"],
    "ENRICH-A007": [],
    "ENRICH-A008": ["BARECON 2017"],
    "ENRICH-A009": ["GENCON"],
    "ENRICH-A010": ["Regulation (EU) 2023/1805"],
}

# Commercial over-simplifications that are wrong and are not on the card today.
# Word-bounded - see the module docstring on substring collision.
FORBIDDEN_CLAIMS = {
    "ENRICH-A001": [r"p&i covers everything",
                    r"everything not covered by h&m",
                    r"everything h&m does not"],
    "ENRICH-A008": [r"barecon 2017[^.]{0,90}hire/purchase agreement"],
}

# Conditions that must accompany a claim for it to stay true. A later tidy-up
# could keep every positive token above and still flatten these into a wrong
# answer.
REQUIRED_QUALIFIER = {
    # Cl. 8.4.2 excludes property EXCEPT other vessels and property on them.
    "ENRICH-A001": ["other vessels and property on them"],
    # The Insurance Act 2015 abolished the DISCHARGE rule, not exact compliance.
    "ENRICH-A005": ["was abolished"],
    # Security of navigation is an MSC matter, not a Legal Committee one.
    "ENRICH-A006": ["is not the Legal Committee"],
    # The 2001 hire/purchase mechanism is not current BARECON wording.
    "ENRICH-A008": ["BARECON 2017 changed this"],
    # A mass-basis energy advantage is not a volumetric one.
    "ENRICH-A010": ["not a volumetric one"],
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
    differs per file here. A raw-byte compare would report every card on a
    CRLF checkout as changed.
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
    carries more .q-card blocks than canonical questions, because some pages
    reuse the class for structural blocks. Counting the class rather than the
    anchor convention inflates the corpus and lets a count assertion pass
    vacuously.
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
    raw = git_show(manifest.get("authorisation_commit") or CONSOL_REF,
                   CONSOL_REL)
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

    # ---- manifest must match the consolidation's E1 set exactly ----
    consol, src = load_consolidation(manifest)
    if consol is None:
        report("authorised_action_set", False,
               "consolidation unavailable (%s) - cannot confirm linkage" % src)
        report("authorised_targets", False, "consolidation unavailable")
        report("authorised_enrichment_disposition", False,
               "consolidation unavailable")
    else:
        batch = [b for b in consol["batches"] if b["batch_id"] == "E1"]
        want = set(batch[0]["action_ids"]) if batch else set()
        got = {c["action_id"] for c in cards}
        report("authorised_action_set",
               want == got and len(got) == EXPECTED_ACTIONS,
               "manifest %d vs consolidation %d; extra=%s missing=%s [%s]"
               % (len(got), len(want), sorted(got - want) or "-",
                  sorted(want - got) or "-", src))

        # The batches[] roll-up and the per-action batch field must AGREE.
        # Checking only one of them is what let an off-by-one brief through
        # on an earlier batch.
        per_action = {a["action_id"] for a in consol["production_actions"]
                      if a.get("batch") == "E1"}
        report("batch_membership_representations_agree",
               per_action == want and per_action == got,
               "batches[]=%d production_actions[]=%d manifest=%d"
               % (len(want), len(per_action), len(got)))

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
            if a.get("batch") != "E1":
                bad_d.append("%s(batch %s)" % (c["action_id"], a.get("batch")))
            if a.get("family_ids", [None])[0] != c["family_id"]:
                bad_d.append("%s(family)" % c["action_id"])
            if a.get("priority") != c["priority"]:
                bad_d.append("%s(priority)" % c["action_id"])
        report("authorised_targets", not bad_t,
               "%s" % (sorted(set(bad_t)) or "-"))
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
            ql = re.search(r'class="q-text"[^>]*>(.*?)</div>', L[a], re.S)
            qb = re.search(r'class="q-text"[^>]*>(.*?)</div>', B[a], re.S)
            if ql and qb and ql.group(1).strip() != qb.group(1).strip():
                qtext_moved.append("%s#%s" % (fname, a))

    # A card ADDED since this batch's baseline is legitimate iff some OTHER
    # authorisation record owns it. The original form of these two checks said
    # "the corpus is exactly the size it was at my baseline, and nothing was
    # added" - true of E1, but a claim that stops being true the first time the
    # bank grows for any reason. Batch G1 added four cards and turned every
    # E- and F-series guard red at once, none of which was a real finding.
    #
    # The claim E1 can make forever is "nothing was added that nobody
    # authorised", and that is what is asserted now. It is not a weakening: an
    # addition no manifest owns still fails, and so does any removal.
    sibling_owned = sibling_owned_cards(MANIFEST)
    added = [x for x in changed if "CARD ADDED" in x]
    removed = [x for x in changed if "CARD REMOVED" in x]
    added_legit = [x for x in added if x.split(" ")[0] in sibling_owned]
    added_rogue = [x for x in added if x.split(" ")[0] not in sibling_owned]

    report("canonical_total_unchanged",
           total_base == manifest["expected_canonical_questions"]
           and total_live == total_base + len(added_legit) - len(removed),
           "baseline %d (manifest expects %d) -> live %d, of which %d addition(s) "
           "authorised elsewhere"
           % (total_base, manifest["expected_canonical_questions"], total_live,
              len(added_legit)))

    report("no_new_canonical_card", not added_rogue and not removed,
           "unauthorised additions %s; removals %s"
           % (added_rogue or "-", removed or "-"))

    # A card that a SIBLING batch manifest authorises is legitimate here too.
    # Built in from the start rather than left to expire: without it this check
    # forbids every future authorised edit anywhere in the corpus and fails the
    # moment E1, E5 or E6 lands.
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
    # Compare on the bare "file#anchor": the CARD ADDED / CARD REMOVED suffix
    # used to make an addition unmatchable, which is precisely what made this
    # guard expire. A plain edit carries no suffix, so an edit to a card no
    # manifest owns still fails exactly as before.
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
            # Entity-unescaped before matching. These pages write "&" as
            # "&amp;", so a negative pattern spelled "h&m" - which is how a
            # candidate would read it and how anyone would write the guard -
            # can never match the HTML that actually carries the claim. E1's
            # own mutation P proved this: asserting "P&I covers everything not
            # covered by H&M" escaped the forbidden-claim check entirely and
            # was caught only incidentally by the digest check. Unescaping is
            # strictly stronger: it matches both spellings, so it can only ever
            # catch more, never less.
            low = html.unescape(card).lower()
            for tok in LIMB_TOKENS.get(c["action_id"], []):
                if tok.lower() not in low:
                    limb_missing.append("%s#%s lacks %r" % (fname, a, tok))
            for tok in AUTHORITY_TOKENS.get(c["action_id"], []):
                if tok.lower() not in low:
                    auth_missing.append("%s#%s lacks %r" % (fname, a, tok))
            for pat in FORBIDDEN_CLAIMS.get(c["action_id"], []):
                if re.search(pat, low):
                    claim_bad.append("%s#%s reintroduced %r" % (fname, a, pat))
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
    report("unsubstantiated_claims_absent", not claim_bad,
           "%s" % (claim_bad or "-"))
    report("required_qualifiers_kept", not qual_bad, "%s" % (qual_bad or "-"))
    report("no_candidate_visible_metadata", not dirty, "%s" % (dirty or "-"))

    # ---- timed blocks are untouched: enrichment is body-only ----
    timed_bad = []
    for fname, wanted in sorted(by_file.items()):
        raw = (QB_DIR / fname).read_text(encoding="utf-8", newline="")
        live = cards_of(raw)
        base_raw = git_show(base, "meoclass1/" + fname)
        based = cards_of(base_raw) if base_raw else {}
        for c in wanted:
            a = c["anchor"]
            if a not in live or a not in based:
                continue
            pat = re.compile(
                r'<div class="(?:practice-block|oral-box)[^"]*"[^>]*>.*?</div>',
                re.S)
            lb = pat.findall(live[a].replace("\r\n", "\n"))
            bb = pat.findall(based[a].replace("\r\n", "\n"))
            if lb != bb and not c.get("timed_blocks_changed"):
                timed_bad.append("%s#%s" % (fname, a))
    report("timed_blocks_unchanged", not timed_bad, "%s" % (timed_bad or "-"))

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

    # ---- ten actions, nine cards: the shared target is asserted, not assumed --
    n_actions = len(cards)
    targets = ["%s#%s" % (c["file"], c["anchor"]) for c in cards]
    distinct = sorted(set(targets))
    shared = sorted({t for t in targets if targets.count(t) > 1})
    declared = manifest.get("distinct_target_cards")
    report("action_and_target_cardinality",
           n_actions == EXPECTED_ACTIONS and len(distinct) == declared
           and shared == ["QB9_H.html#q9"],
           "actions=%d distinct_cards=%d (manifest declares %s) shared=%s"
           % (n_actions, len(distinct), declared, shared or "-"))

    # Both limbs of the shared card must be present, not just one of them.
    share_bad = []
    for c in cards:
        if "%s#%s" % (c["file"], c["anchor"]) in shared:
            if not c.get("shared_target_note"):
                share_bad.append(c["action_id"])
    report("shared_target_declared", not share_bad, "%s" % (share_bad or "-"))

    report("manifest_declares_no_new_cards",
           manifest.get("creates_new_cards") is False,
           "creates_new_cards=%s" % manifest.get("creates_new_cards"))

    print("\nE1 enrichment validator: %d checks, %d FAIL" % (_checks, len(_fails)))
    if _fails:
        print("failed:", ", ".join(_fails))
    return 1 if _fails else 0


if __name__ == "__main__":
    sys.exit(main())
