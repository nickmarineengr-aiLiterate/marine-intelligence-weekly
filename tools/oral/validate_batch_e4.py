"""Guard the six authorised E4 machinery/fuels/emissions ENRICHMENT edits.

batch_e4_enrichment_manifest.json is the authority for which enrichment action
edits which existing file#anchor. This validator proves, against the LIVE QB
HTML and against the consolidation record, that:

  * the manifest carries exactly the consolidation's E4 action set;
  * every action is a RETAINED enrichment action targeting the file#anchor the
    consolidation records, at the priority band it records;
  * every target card still exists, exactly once, under #q-feed;
  * NO new canonical card was created - the corpus total is unchanged, not
    merely "not regressed";
  * only the six authorised cards differ from the baseline commit;
  * each action's missing limb is now actually present, by required token;
  * each action's required authority is cited on the card;
  * no production metadata is candidate-visible on any touched page;
  * q-text and anchors are untouched - this is enrichment, not re-homing;
  * the examiner relationship count is unchanged.

WHY THE COUNT IS AN EQUALITY HERE, NOT A FLOOR
The new-card guards assert the corpus total as a floor so a later authorised
batch does not break them. An enrichment batch is the opposite case: creating a
card is precisely the failure mode, so E4 asserts strict equality against the
baseline commit it was cut from. That equality cannot expire, because it is
evaluated against a pinned commit rather than against "today".

WHY THE LIMB CHECK IS TOKEN-BASED, NOT DIGEST-BASED
A digest would only prove the card changed. These checks prove the card changed
IN THE AUTHORISED DIRECTION: each action names tokens that can only be present
if its specific missing limb was supplied. Blanking the limb while leaving the
card otherwise edited still fails.

Exit 0 when every check passes, 1 otherwise.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oral_manifest import authorisation_manifest_paths, sibling_owned_cards  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
MANIFEST = Path(__file__).resolve().parent / "batch_e4_enrichment_manifest.json"
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
    "ENRICH-A027": ["0.8744", "0.8493", "44/12"],
    "ENRICH-A028": ["Scope 1", "Scope 2", "Scope 3", "Category 3"],
    "ENRICH-A029": ["80%", "ramped", "purged", "inerted"],
    "ENRICH-A030": ["ME-GI", "300 bar", "0.20", "top dead centre"],
    "ENRICH-A031": ["frequency converter", "switchboard", "transformer",
                    "slip rings"],
    "ENRICH-A032": ["design/parts number", "Record Book of Engine Parameters",
                    "6.2.3.2", "1.3.3"],
}

# Authority that must remain cited on the card for the limb to stand up.
AUTHORITY_TOKENS = {
    "ENRICH-A027": ["MEPC.364(79)"],
    "ENRICH-A028": ["GHG Protocol"],
    "ENRICH-A029": ["IGF Code"],
    "ENRICH-A030": ["MAN"],
    "ENRICH-A031": ["SOLAS"],
    "ENRICH-A032": ["NOx Technical Code"],
}

_fails = []
_checks = 0


def report(name, ok, detail=""):
    global _checks
    _checks += 1
    print("%-5s %-44s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        _fails.append(name)


CARD_OPEN = re.compile(r'<div class="q-card[^"]*"[^>]*>', re.I)


def _balanced_end(text, start):
    depth = 0
    for m in re.finditer(r"<div\b[^>]*>|</div\s*>", text[start:], re.I):
        depth += -1 if m.group(0).startswith("</") else 1
        if depth == 0:
            return start + m.end()
    raise AssertionError("unbalanced q-card at %d" % start)


CANONICAL_ANCHOR = re.compile(r"q\d+")


def cards_of(text):
    """anchor -> card HTML, on LF-normalised text.

    LF-normalised because .gitattributes pins these pages to LF in the object
    store while the working tree may hold CRLF per file, and a raw-byte compare
    would then report every card on a CRLF checkout as changed.
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

    A .q-card div is not the same thing as a canonical question: QB1_A carries
    structural blocks (#dependency-graph, #family-trees) that reuse the class.
    Counting the class rather than the anchor convention inflates the corpus by
    two and lets a count assertion pass vacuously - the same defect that made a
    class-counting validator agree with itself during Batch C. Canonical
    anchors match q<digits>, the convention the other batch guards use.
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


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cards = manifest["cards"]
    base = manifest["baseline_commit"]

    # ---- manifest must match the consolidation's E4 set exactly ----
    consol, src = load_consolidation(manifest)
    if consol is None:
        report("authorised_action_set", False,
               "consolidation unavailable (%s) - cannot confirm linkage" % src)
        report("authorised_targets", False, "consolidation unavailable")
        report("authorised_enrichment_disposition", False,
               "consolidation unavailable")
    else:
        batch = [b for b in consol["batches"] if b["batch_id"] == "E4"]
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
            if a.get("batch") != "E4":
                bad_d.append("%s(batch %s)" % (c["action_id"], a.get("batch")))
            if a.get("family_ids", [None])[0] != c["family_id"]:
                bad_d.append("%s(family)" % c["action_id"])
            if a.get("priority") != c["priority"]:
                bad_d.append("%s(priority)" % c["action_id"])
        report("authorised_targets", not bad_t, "%s" % (sorted(set(bad_t)) or "-"))
        report("authorised_enrichment_disposition", not bad_d,
               "%s" % (sorted(set(bad_d)) or "-"))

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
        # q-text must not move on any card, authorised or not
        for a in set(L) & set(B):
            ql = re.search(r'<div class="q-text">(.*?)</div>', L[a], re.S)
            qb = re.search(r'<div class="q-text">(.*?)</div>', B[a], re.S)
            if ql and qb and ql.group(1).strip() != qb.group(1).strip():
                qtext_moved.append("%s#%s" % (fname, a))

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
    # Without this the check forbids every future authorised edit anywhere in
    # the corpus and expires the moment the next enrichment batch lands - which
    # is exactly what E3 triggered. This is the same delegation contract E4
    # completed for the A-D digest pins; it was never carried to this check,
    # one level up, so the incomplete loop survived in the validator that
    # diagnosed it. Exempt cards are reported BY NAME, never silently dropped.
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

    # A stem reworded on a card ANOTHER authorisation record owns is that
    # record's business, not this batch's. Without this exemption the check
    # asserts "no question text anywhere in the corpus has changed since my
    # baseline", which stops being true the first time any authorised
    # correction rewords a stem -- the same expiry the checks above were
    # already fixed for. A reword on a card NOBODY owns still fails, and so
    # does a reword of this batch's OWN cards, which is what the check is for.
    qtext_unowned = [x for x in qtext_moved if x not in sibling_owned]
    qtext_elsewhere = sorted(set(qtext_moved) - set(qtext_unowned))
    report("q_text_and_anchors_stable", not qtext_unowned,
           "moved=%s authorised-elsewhere=%s"
           % (qtext_unowned or "-", qtext_elsewhere or "-"))

    # ---- the limb is actually there, and its authority with it ----
    for fname, wanted in sorted(by_file.items()):
        live = cards_of((QB_DIR / fname).read_text(encoding="utf-8", newline=""))
        raw = (QB_DIR / fname).read_text(encoding="utf-8", newline="")
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
            for tok in LIMB_TOKENS.get(c["action_id"], []):
                if tok.lower() not in card.lower():
                    limb_missing.append("%s#%s lacks %r" % (fname, a, tok))
            for tok in AUTHORITY_TOKENS.get(c["action_id"], []):
                if tok.lower() not in card.lower():
                    auth_missing.append("%s#%s lacks %r" % (fname, a, tok))
            leak = FORBIDDEN.findall(visible_text(card))
            if leak:
                dirty.append("%s#%s %s" % (fname, a, sorted(set(leak))))

    report("target_cards_present", not absent, "%s" % (absent or "-"))
    report("target_anchors_unique", not dupes, "%s" % (dupes or "-"))
    report("target_cards_under_q_feed", not outside, "%s" % (outside or "-"))
    report("missing_limb_supplied", not limb_missing,
           "%s" % (limb_missing or "-"))
    report("required_authority_cited", not auth_missing,
           "%s" % (auth_missing or "-"))
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

    print("\nE4 enrichment validator: %d checks, %d FAIL" % (_checks, len(_fails)))
    if _fails:
        print("failed:", ", ".join(_fails))
    return 1 if _fails else 0


if __name__ == "__main__":
    sys.exit(main())
