"""Guard the twelve authorised E5 STCW/MLC/crew/management ENRICHMENT edits.

batch_e5_enrichment_manifest.json is the authority for which enrichment action
edits which existing file#anchor. This validator proves, against the LIVE QB
HTML and against the consolidation record, that:

  * the manifest carries exactly the consolidation's E5 action set, on BOTH of
    the consolidation's independent representations;
  * every action targets the file#anchor, priority band and families the
    consolidation records;
  * every target card still exists, exactly once, under #q-feed;
  * NO new canonical card was created - the corpus total is unchanged, not
    merely "not regressed";
  * only the eleven authorised cards differ from the baseline commit;
  * each action's missing limb is now actually present, by required token;
  * each action's required authority is cited on the card;
  * every edit is PURELY ADDITIVE - no baseline character was deleted or
    replaced on any authorised card;
  * the manifest's recorded pre/post digests match reality;
  * the distinctions that make the additions correct are still qualified
    rather than flattened;
  * no production metadata is candidate-visible on any touched page;
  * q-text and anchors are untouched - this is enrichment, not re-homing;
  * the examiner relationship count is unchanged.

WHY TWELVE ACTIONS BUT ELEVEN CARDS
ENRICH-A036 (MLC Title 3 accommodation minima as quotable figures) and
ENRICH-A037 (the shipowner as a distinct duty-holder, and Part V of the
Merchant Shipping Act, 2025) both land on QB4_C.html#q6. E1 met this shape
first and built `action_and_target_cardinality` and `shared_target_declared`
for it. E5 needs MORE than E1 did, because E1's shared pair could be checked
by arithmetic alone: here the two limbs are on the same card AND in adjacent
prose, so a tidy-up that merges them into one section, or a manifest edit that
drops one action id while leaving the other, would keep the card looking right.

`shared_target_actions_enumerated` therefore requires the manifest to name BOTH
ids against the shared target and requires that set to equal the set actually
derived from the card list - so dropping A036 or A037 fails on the enumeration
even before the token checks run. `shared_target_limbs_independently_present`
then requires each id's own LIMB_TOKENS on the card, so the two actions cannot
collapse into one another. An action id may not be renamed into its partner
either: `authorised_action_set` is an exact set equality against the
consolidation.

WHY MLC PART A AND PART B ARE GUARDED SEPARATELY
E5 is the first batch whose subject matter is a convention with a mandatory
Part A and a non-mandatory Part B in the same Code. Standard A3.1 and Standard
A1.2 are binding; Guideline B3.1.5 and Guideline B4.3.1 are guidance. Presenting
a Guideline as mandatory, or a Standard as advisory, is the single most common
way an MLC answer goes wrong, and both directions are forbidden outright rather
than left to the positive token checks.

WHY THE CURRENTNESS QUALIFIERS ARE GUARDED, NOT JUST THE TOKENS
Three actions are CURRENT_REG_VERIFY_REQUIRED and one more turns on an
amendment date:

  * A040 - the 2022 MLC amendments are IN FORCE since 23 December 2024; the
    April 2025 Special Tripartite Committee amendments are ADOPTED and NOT yet
    in force. Collapsing adopted into in-force is the defect, so "not yet in
    force" is a required qualifier and asserting the 2025 package is in force
    is a forbidden claim.
  * A036 - Standard A3.1's dimensions are CONSTRUCTION requirements, so under
    Regulation 3.1 paragraph 2 they bind ships constructed on or after the
    Convention's entry into force for the flag State. Quoting the figures as
    though they applied to every hull afloat is wrong, so "constructed on or
    after" is a required qualifier.
  * A038 - no contribution percentage is asserted anywhere, deliberately; see
    the manifest's authorisation_correction.

WHY A036 CARRIES A LOAD LINE DISCLAIMER
The consolidation authorised "door sill/coaming heights" as MLC Title 3
accommodation minima. They are not: the string "door" does not occur anywhere
in Standard A3.1, and sill and coaming heights are Load Line Convention
weathertight-integrity requirements. That sub-limb was rejected, and the card
names the confusion instead. The disclaimer is a REQUIRED_QUALIFIER, because a
later tidy-up that deletes it leaves the reader with the consolidation's
original error and nothing to correct it.

WHY A043's THESIS IS A GUARD RATHER THAN A TOKEN
QB5_D#q3 teaches that harassment must NOT be informally mediated and that
compromise is the wrong outcome. The authorised limb is a graded ladder that
begins at counselling - which, unqualified, reads as a licence to do exactly
what the card forbids. The addition is scoped to the disciplinary response
AFTER investigation, and that scoping is guarded: both "only after" and the
sentence denying that the ladder is a way of settling the matter between the
two seafarers must survive. Without them the authorised limb degrades the
answer rather than enriching it.

WHY THE NEGATIVE GUARDS ARE ENTITY-UNESCAPED
These pages write "&" as "&amp;". E1's mutation P proved that a forbidden-claim
pattern spelled the way a person writes it can never match the HTML that would
actually carry the claim. The match is made against html.unescape(card), which
is strictly stronger. Every pattern here was also run against the BASELINE card
before being adopted, so none of them fires on text nobody wrote today.

WHY THE COUNT IS AN EQUALITY HERE, NOT A FLOOR
Creating a card is precisely the failure mode for an enrichment batch, so E5
asserts strict equality against the pinned baseline commit it was cut from.
That equality cannot expire, because it is evaluated against a commit rather
than against "today".

WHY DIGESTS ARE LF-NORMALISED
All nine E5 destination files are LF on disk and .gitattributes pins *.html to
eol=lf, so they agree today. They are normalised anyway: a future CRLF checkout
of any of these pages would otherwise manufacture one phantom insert opcode per
line and make the additivity proof meaningless.

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
MANIFEST = Path(__file__).resolve().parent / "batch_e5_enrichment_manifest.json"
QB_DIR = REPO / "meoclass1"
CONSOL_REL = ("meoclass1/oral-intelligence/examiner-audit/"
              "FINAL_ORAL_ENRICHMENT_CONSOLIDATION.json")
CONSOL_REF = "origin/research/oral-final-enrichment-consolidation"

EXPECTED_ACTIONS = 12
SHARED_TARGET = "QB4_C.html#q6"

# Candidate-visible production vocabulary. Deliberately does NOT ban the plain
# English verb "verify": it appears in legitimate regulatory prose and in a CSS
# class name on these very pages, so banning it guarantees false positives.
# "pending verification" IS banned: it is internal status language, and E5 found
# it live on QB9_H#q4 where an earlier session left it in candidate view. That
# instance is pre-existing debt outside this batch's limb, so the leak scan
# below runs on the ADDED text only - see no_candidate_visible_metadata.
FORBIDDEN = re.compile(
    r"ENRICH-A\d|GAP-\d{4}|\bTODO\b|\bFIXME\b|(?<![\w-])VERIFY(?![\w-])"
    r"|\bCORRECTED:|recurrence_class|laptop_review|missing_limb|batch_id"
    r"|production_action|pending verification|sections pending"
    r"|\b[a-z_]+\.(?:json|py|xlsx)\b")

# Tokens that can only be present if the action's missing limb was supplied.
# Every one was checked to be ABSENT from the baseline card before adoption: a
# limb token the baseline already carried would make the check pass without the
# limb being there at all.
LIMB_TOKENS = {
    "ENRICH-A033": ["III/1", "750 kW", "six months", "18 years",
                    "workshop skills training", "30 months"],
    "ENRICH-A034": ["36 months", "30 months", "Rules 35 to 37",
                    "Assistant Engineer Officer", "Engineering Management Course"],
    "ENRICH-A035": ["A-VI/1", "A-VI/3", "every five years",
                    "Regulations I/6 and I/8"],
    "ENRICH-A036": ["203 cm", "198 cm", "4.5", "5.5", "9(f)", "headroom"],
    "ENRICH-A037": ["Part V", "Titles 1 to 4", "Duty-Holder"],
    "ENRICH-A038": ["Seamen's Provident Fund", "SPFO", "Ministry of Ports"],
    "ENRICH-A039": ["Designated Grievance Redressal Officer",
                    "First Appellate Authority", "thirty working days"],
    "ENRICH-A040": ["two years", "colour vision", "six years",
                    "three months", "23 December 2024"],
    "ENRICH-A041": ["Interim Safety Management Certificate", "14.2.2",
                    "new to the Company"],
    "ENRICH-A042": ["condition-based", "predictive", "risk-based", "preventive"],
    "ENRICH-A043": ["counselling", "formal warning", "retraining", "graded"],
    "ENRICH-A044": ["Bloom", "analyse", "cognitive"],
}

# Authority that must remain cited on the card for the limb to stand up.
# A043 and A044 are TECHNICAL_REASONING_ONLY and assert no instrument, so their
# required-authority sets are deliberately empty rather than absent by oversight.
AUTHORITY_TOKENS = {
    "ENRICH-A033": ["STCW Regulation III/1", "A-III/1"],
    "ENRICH-A034": ["M.S. (STCW) Rules", "TEAP Part A"],
    "ENRICH-A035": ["STCW Regulation I/2", "A-VI/2"],
    "ENRICH-A036": ["Standard A3.1", "Regulation 3.1, paragraph 2"],
    "ENRICH-A037": ["Merchant Shipping Act, 2025", "Part V"],
    "ENRICH-A038": ["Seamen's Provident Fund Act, 1966"],
    "ENRICH-A039": ["MS Notice No. 03 of 2013"],
    "ENRICH-A040": ["STCW Regulation I/9", "MLC Standard A1.2"],
    "ENRICH-A041": ["ISM Code 14.1", "ISM Code 14.2.2"],
    "ENRICH-A042": ["ISM Section 10.3"],
    "ENRICH-A043": [],
    "ENRICH-A044": [],
}

# Over-simplifications that are wrong and are not on the card today.
# Every pattern was run against the BASELINE card before adoption.
FORBIDDEN_CLAIMS = {
    # The A3.1 dimensions are construction requirements, not universal ones.
    "ENRICH-A036": [r"appl(?:y|ies) to all ships",
                    r"regardless of (?:build|construction) date",
                    r"door sills?[^.]{0,60}under (?:standard a3\.1|mlc)"],
    # Duties in Titles 1-4 fall on the shipowner, not the flag State.
    "ENRICH-A037": [r"flag state[^.]{0,40}owes the seafarer"],
    # Adopted is not in force.
    "ENRICH-A040": [r"april 2025[^.]{0,60}(?:is|are|came|entered) in(?:to)? force",
                    r"2025 amendments[^.]{0,40}(?:are|is) now in force"],
    # The ladder is not a way of settling harassment between two crew members.
    "ENRICH-A043": [r"settle (?:it|the matter) between the two",
                    r"(?:start|begin)[^.]{0,30}with informal mediation"],
}

# MLC Part A is mandatory; Part B is guidance. Both directions are wrong and
# both are forbidden, on every MLC action in the batch.
MLC_ACTIONS = ["ENRICH-A036", "ENRICH-A037", "ENRICH-A040", "ENRICH-A043"]
PART_AB_PATTERNS = [
    r"guideline b[0-9.]*[^.]{0,70}(?:is mandatory|are mandatory|mandatory requirement)",
    r"standard a[0-9.]*[^.]{0,70}(?:is guidance|is only guidance|non-mandatory|is recommendatory)",
]

# Conditions that must accompany a claim for it to stay true. A later tidy-up
# could keep every positive token above and still flatten these into a wrong
# answer.
REQUIRED_QUALIFIER = {
    # Sea time alone does not qualify - it must be supervised watchkeeping.
    "ENRICH-A033": ["under the supervision of the chief engineer officer"],
    # The totals run from obtaining Class IV, not from first sea time.
    "ENRICH-A034": ["from obtaining Class IV"],
    # Documentary evidence is the third category, not a kind of certificate.
    "ENRICH-A035": ["other than</em> a CoC or a CoP"],
    # Construction-date limitation, and the Load Line disclaimer that replaces
    # the consolidation's rejected door-sill sub-limb.
    "ENRICH-A036": ["constructed on or after", "not MLC ones"],
    # Titles 1-4 are shipowner duties; Title 5 is the enforcement layer.
    "ENRICH-A037": ["Title 5 is the enforcement layer"],
    # Contributory social security is not grant-funded welfare.
    "ENRICH-A038": ["contributory social security"],
    # The DGRO is not the first port of call.
    "ENRICH-A039": ["only after"],
    # Adopted is not in force.
    "ENRICH-A040": ["not yet in force", "23 December 2024"],
    # ISM 14.4.5 is the triage rule.
    "ENRICH-A041": ["prior to sailing"],
    # A maintenance strategy is not the ship's to change unilaterally.
    "ENRICH-A042": ["never on the ship's own judgement"],
    # The thesis of the card. Without these the addition contradicts it.
    "ENRICH-A043": ["never a menu for settling the matter between the two seafarers",
                    "only after"],
    # Assessment must match the level of the objective.
    "ENRICH-A044": ["must match the level of the objective"],
}

VALID_STATUS = {"IMPLEMENTED", "IMPLEMENTED_REDUCED_SCOPE"}

_fails = []
_checks = 0


def report(name, ok, detail=""):
    global _checks
    _checks += 1
    print("%-5s %-46s %s" % ("PASS" if ok else "FAIL", name, detail))
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

    A .q-card div is not the same thing as a canonical question: the corpus
    carries more .q-card blocks than canonical questions. Counting the class
    rather than the anchor convention inflates the corpus and lets a count
    assertion pass vacuously.
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


def added_text(base_card, live_card):
    """The characters this batch inserted, and nothing else.

    The hygiene scan runs on this rather than the whole card because these
    pages carry pre-existing candidate-visible debt that E5 is not authorised
    to repair - notably a literal "sections pending verification" on
    QB9_H#q4. Scanning the whole card would fail the batch for text it did not
    write and cannot touch.
    """
    sm = difflib.SequenceMatcher(None, base_card, live_card, autojunk=False)
    return "".join(live_card[j1:j2] for tag, _, _, j1, j2 in sm.get_opcodes()
                   if tag in ("insert", "replace"))


def digest16(s):
    import hashlib
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cards = manifest["cards"]
    base = manifest["baseline_commit"]

    # ---- manifest must match the consolidation's E5 set exactly ----
    consol, src = load_consolidation(manifest)
    if consol is None:
        for n in ("authorised_action_set", "authorised_targets",
                  "authorised_enrichment_disposition",
                  "batch_membership_representations_agree"):
            report(n, False, "consolidation unavailable (%s)" % src)
    else:
        batch = [b for b in consol["batches"] if b["batch_id"] == "E5"]
        want = set(batch[0]["action_ids"]) if batch else set()
        got = {c["action_id"] for c in cards}
        report("authorised_action_set",
               want == got and len(got) == EXPECTED_ACTIONS,
               "manifest %d vs consolidation %d; extra=%s missing=%s [%s]"
               % (len(got), len(want), sorted(got - want) or "-",
                  sorted(want - got) or "-", src))

        # The batches[] roll-up and the per-action batch field must AGREE.
        # Checking only one of them is what let an off-by-one brief through on
        # an earlier batch.
        per_action = {a["action_id"] for a in consol["production_actions"]
                      if a.get("batch") == "E5"}
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
            if a.get("batch") != "E5":
                bad_d.append("%s(batch %s)" % (c["action_id"], a.get("batch")))
            if list(a.get("family_ids", [])) != list(c["family_ids"]):
                bad_d.append("%s(family)" % c["action_id"])
            if a.get("priority") != c["priority"]:
                bad_d.append("%s(priority)" % c["action_id"])
            if a.get("verification_scope") != c["verification_scope"]:
                bad_d.append("%s(verification_scope)" % c["action_id"])
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

    for page in sorted(p.name for p in QB_DIR.glob("QB*.html")):
        live_raw = (QB_DIR / page).read_text(encoding="utf-8", newline="")
        base_raw = git_show(base, "meoclass1/" + page)
        if base_raw is None:
            continue
        L, B = canonical_cards(live_raw), canonical_cards(base_raw)
        total_live += len(L)
        total_base += len(B)
        for a in set(L) - set(B):
            changed.append("%s#%s (CARD ADDED)" % (page, a))
        for a in set(B) - set(L):
            changed.append("%s#%s (CARD REMOVED)" % (page, a))
        for a in set(L) & set(B):
            if L[a] != B[a]:
                changed.append("%s#%s" % (page, a))
            ql = re.search(r'class="q-text"[^>]*>(.*?)</div>', L[a], re.S)
            qb = re.search(r'class="q-text"[^>]*>(.*?)</div>', B[a], re.S)
            if ql and qb and ql.group(1).strip() != qb.group(1).strip():
                qtext_moved.append("%s#%s" % (page, a))

    # A card ADDED since this batch's baseline is legitimate iff some OTHER
    # authorisation record owns it. The original form of these two checks said
    # "the corpus is exactly the size it was at my baseline, and nothing was
    # added" - true of this batch, but a claim that stops being true the first
    # time the bank grows for any reason. Batch G1 added four cards and turned
    # every E- and F-series guard red at once, none of which was a real finding.
    #
    # The claim this batch can make forever is "nothing was added that nobody
    # authorised". It is not a weakening: an addition no manifest owns still
    # fails, and so does any removal.
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
    # moment E6 lands.
    #
    # Not a weakening: the exemption is keyed on a plain "file#anchor" and the
    # CARD ADDED / CARD REMOVED entries carry a suffix, so they can never match
    # it; an edit to a card no manifest owns still fails.
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
           "unauthorised=%s authorised-elsewhere=%d card(s)"
           % (unauthorised or "-", len(exempt)))

    not_changed = sorted(authorised - set(changed))
    report("every_authorised_card_changed", not not_changed,
           "unchanged=%s" % (not_changed or "-"))

    report("q_text_and_anchors_stable", not qtext_moved,
           "moved=%s" % (qtext_moved or "-"))

    # ---- the limb is actually there, and its authority with it ----
    additive_bad, digest_bad, claim_bad, qual_bad, ab_bad = [], [], [], [], []
    for page, wanted in sorted(by_file.items()):
        raw = (QB_DIR / page).read_text(encoding="utf-8", newline="")
        live = cards_of(raw)
        base_raw = git_show(base, "meoclass1/" + page)
        based = cards_of(base_raw) if base_raw else {}
        for c in wanted:
            a = c["anchor"]
            if a not in live:
                absent.append("%s#%s" % (page, a))
                continue
            if len(re.findall(r'id="%s"' % re.escape(a), raw)) != 1:
                dupes.append("%s#%s" % (page, a))
            if raw.find('id="q-feed"') > raw.find('id="%s"' % a):
                outside.append("%s#%s" % (page, a))
            card = live[a]
            # Entity-unescaped before matching - see the module docstring.
            low = html.unescape(card).lower()
            for tok in LIMB_TOKENS.get(c["action_id"], []):
                if tok.lower() not in low:
                    limb_missing.append("%s %s#%s lacks %r"
                                        % (c["action_id"], page, a, tok))
            for tok in AUTHORITY_TOKENS.get(c["action_id"], []):
                if tok.lower() not in low:
                    auth_missing.append("%s %s#%s lacks %r"
                                        % (c["action_id"], page, a, tok))
            for pat in FORBIDDEN_CLAIMS.get(c["action_id"], []):
                if re.search(pat, low):
                    claim_bad.append("%s %s#%s reintroduced %r"
                                     % (c["action_id"], page, a, pat))
            if c["action_id"] in MLC_ACTIONS:
                for pat in PART_AB_PATTERNS:
                    if re.search(pat, low):
                        ab_bad.append("%s %s#%s: %r"
                                      % (c["action_id"], page, a, pat))
            for tok in REQUIRED_QUALIFIER.get(c["action_id"], []):
                if tok.lower() not in low:
                    qual_bad.append("%s %s#%s lost qualifier %r"
                                    % (c["action_id"], page, a, tok))

            # purely additive, at character level; hygiene on ADDED text only
            if a in based:
                bb = based[a].replace("\r\n", "\n")
                ll = card.replace("\r\n", "\n")
                sm = difflib.SequenceMatcher(None, bb, ll, autojunk=False)
                bad = [o for o in sm.get_opcodes()
                       if o[0] not in ("equal", "insert")]
                if bad:
                    additive_bad.append("%s#%s %d non-insert op(s)"
                                        % (page, a, len(bad)))
                if digest16(bb) != c.get("pre_edit_digest"):
                    digest_bad.append("%s#%s pre" % (page, a))
                # The pin is never rewritten and never relaxed. When a later
                # authorised record declares that it supersedes this state, this
                # check stops asking "is my state live?" and starts asking "is my
                # state the ancestor of what is live?" -- which is a strictly
                # stronger claim, because the whole chain must be continuous and
                # its terminal state must be the live card. With no successor
                # declared this is byte-for-byte the original comparison.
                res = resolve_authorised_card_state(
                    manifest=MANIFEST.name, action_id=c["action_id"],
                    file=page, anchor=a,
                    pinned_post_digest=c.get("post_edit_digest"),
                    live_digest=digest16(ll), directory=MANIFEST.parent)
                if not res.ok:
                    digest_bad.append("%s post %s" % ("%s#%s" % (page, a), res.describe()))
                leak = FORBIDDEN.findall(visible_text(
                    html.unescape(added_text(bb, ll))))
                if leak:
                    dirty.append("%s#%s %s" % (page, a, sorted(set(leak))))

    report("target_cards_present", not absent, "%s" % (absent or "-"))
    report("target_anchors_unique", not dupes, "%s" % (dupes or "-"))
    report("target_cards_under_q_feed", not outside, "%s" % (outside or "-"))
    report("missing_limb_supplied", not limb_missing, "%s" % (limb_missing or "-"))
    report("required_authority_cited", not auth_missing, "%s" % (auth_missing or "-"))
    report("edits_purely_additive", not additive_bad, "%s" % (additive_bad or "-"))
    report("manifest_digests_match", not digest_bad, "%s" % (digest_bad or "-"))
    report("unsubstantiated_claims_absent", not claim_bad, "%s" % (claim_bad or "-"))
    report("mlc_part_a_and_b_not_conflated", not ab_bad, "%s" % (ab_bad or "-"))
    report("required_qualifiers_kept", not qual_bad, "%s" % (qual_bad or "-"))
    report("no_candidate_visible_metadata", not dirty, "%s" % (dirty or "-"))

    # ---- timed blocks are untouched: enrichment is body-only ----
    timed_bad = []
    for page, wanted in sorted(by_file.items()):
        raw = (QB_DIR / page).read_text(encoding="utf-8", newline="")
        live = cards_of(raw)
        base_raw = git_show(base, "meoclass1/" + page)
        based = cards_of(base_raw) if base_raw else {}
        pat = re.compile(
            r'<div class="(?:practice-block|oral-box)[^"]*"[^>]*>.*?</div>', re.S)
        for c in wanted:
            a = c["anchor"]
            if a not in live or a not in based:
                continue
            lb = pat.findall(live[a].replace("\r\n", "\n"))
            bb = pat.findall(based[a].replace("\r\n", "\n"))
            if lb != bb and not c.get("timed_blocks_changed"):
                timed_bad.append("%s#%s" % (page, a))
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

    # ---- twelve actions, eleven cards: the shared target is asserted ----
    targets = ["%s#%s" % (c["file"], c["anchor"]) for c in cards]
    distinct = sorted(set(targets))
    shared = sorted({t for t in targets if targets.count(t) > 1})
    declared = manifest.get("distinct_target_cards")
    report("action_and_target_cardinality",
           len(cards) == EXPECTED_ACTIONS and len(distinct) == declared
           and shared == [SHARED_TARGET],
           "actions=%d distinct_cards=%d (manifest declares %s) shared=%s"
           % (len(cards), len(distinct), declared, shared or "-"))

    # The manifest must NAME both partners, and that naming must equal what the
    # card list actually produces. Dropping A036 or A037 therefore fails here
    # even before any token check runs.
    derived = sorted(c["action_id"] for c in cards
                     if "%s#%s" % (c["file"], c["anchor"]) == SHARED_TARGET)
    declared_actions = sorted(manifest.get("shared_target_actions") or [])
    report("shared_target_actions_enumerated",
           manifest.get("shared_target") == SHARED_TARGET
           and bool(manifest.get("shared_target_note"))
           and len(declared_actions) == 2
           and declared_actions == derived,
           "declared=%s derived=%s note=%s"
           % (declared_actions or "-", derived or "-",
              "yes" if manifest.get("shared_target_note") else "NO"))

    # Each partner's own limb must be independently present on the shared card,
    # so the two actions cannot collapse into one another.
    share_bad = []
    if len(derived) == 2:
        page, anchor = SHARED_TARGET.split("#")
        sc = cards_of((QB_DIR / page).read_text(encoding="utf-8", newline=""))
        low = html.unescape(sc.get(anchor, "")).lower()
        for aid in derived:
            missing = [t for t in LIMB_TOKENS.get(aid, []) if t.lower() not in low]
            if missing:
                share_bad.append("%s lacks %s" % (aid, missing))
    else:
        share_bad.append("shared pair not derivable (%s)" % (derived or "-"))
    report("shared_target_limbs_independently_present", not share_bad,
           "%s" % (share_bad or "both limbs present"))

    report("manifest_declares_no_new_cards",
           manifest.get("creates_new_cards") is False,
           "creates_new_cards=%s" % manifest.get("creates_new_cards"))

    print("\nE5 enrichment validator: %d checks, %d FAIL" % (_checks, len(_fails)))
    if _fails:
        print("failed:", ", ".join(_fails))
    return 1 if _fails else 0


if __name__ == "__main__":
    sys.exit(main())
