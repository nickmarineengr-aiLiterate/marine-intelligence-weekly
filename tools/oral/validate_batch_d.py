"""Guard the nine laptop-authorised NOTES_TO_QB_PROMOTION new canonical cards.

batch_d_manifest.json is the authority for which family id lives at which
file#anchor, and which Oral Notes section each promotion was built from. This
validator proves, against the LIVE QB HTML rather than any derived artefact,
that:

  * every authorised promotion exists, exactly once, at its recorded home;
  * the manifest's family set is exactly the authorisation record's set of
    families whose laptop_decision is NOTES_TO_QB_PROMOTION, and the count
    agrees with the authorisation's own authorised total;
  * no unauthorised tenth promotion has appeared in a Batch-D destination;
  * each promotion carries exactly one final disposition - one family, one
    production action, one file#anchor, with no duplicates in any of the three;
  * each new card's anchor is unique on its page and sits under #q-feed;
  * each new card carries a clean candidate-facing question and a real answer;
  * each new card cites the current primary authority its topic rests on;
  * the Oral Notes source section each promotion was built from still resolves;
  * no production metadata - including any Notes source path - is
    candidate-visible anywhere on those pages;
  * no pre-existing card on a Batch-D page has drifted;
  * the derived content index carries all nine and has not regressed;
  * actual_new_card_count reconciles with the live corpus delta.

WHY THE FAMILY SET IS SELECTED BY laptop_decision, NOT BY A BATCH ARRAY
The authorisation record carries batches.P1-A, P1-B and P2 for the gap-based
new cards, but no array at all for the notes promotions. The nine are therefore
selected by laptop_decision == NOTES_TO_QB_PROMOTION. That is the authorisation
field. laptop_review_status is an AUDIT field - it records whether the row was
altered, not whether it is approved - and Batch C was caught by exactly that
distinction. Here the trap runs the other way: GAP-0065 is adjudicated
NOTES_TO_QB_PROMOTION but the laptop review DOWNGRADED it to ALREADY_COVERED,
which is why the adjudicated total is 10 while the authorised total is 9. This
validator asserts both halves - that all nine authorised families are present,
and that GAP-0065 specifically is absent - so a silent re-inclusion fails.

The corpus total is asserted as a FLOOR, never an equality, and the extra-card
guard unions every sibling batch_*_manifest.json, so this guard will not expire
when a later authorised batch lands.

The authorisation record lives on the laptop review branch, not on main, so the
family-set check reads it through git when it is not present in the tree, and
degrades to a recorded FAIL rather than a false PASS when it cannot be read.

Exit 0 when every check passes, 1 otherwise.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oral_manifest import authorisation_manifest_paths  # noqa: E402
from validate_batch_a import Page, FORBIDDEN, QTEXT_FORBIDDEN  # noqa: E402
from validate_batch_b import card_digests, CARD_OPEN, _balanced_end  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
MANIFEST = Path(__file__).resolve().parent / "batch_d_manifest.json"
QB_DIR = REPO / "meoclass1"
CONTENT_INDEX = QB_DIR / "qb_content_index.json"
AUTH_REL = ("meoclass1/oral-intelligence/examiner-audit/"
            "FINAL_ORAL_PRODUCTION_AUTHORIZATION.json")

# Adjudicated as a notes promotion, but downgraded by the laptop review.
DOWNGRADED = "GAP-0065"

_fails = []
_checks = 0


def report(name, ok, detail=""):
    global _checks
    _checks += 1
    print("%-5s %-46s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        _fails.append(name)


def norm(s):
    """Compare on words only, so punctuation and spacing never decide a check."""
    return " ".join(re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).split())


def load_authorisation(manifest):
    """Read the authorisation record from the tree, else from its review ref."""
    p = REPO / AUTH_REL
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8")), "tree"
    ref = manifest.get("authorisation_ref")
    if not ref:
        return None, "no ref"
    r = subprocess.run(["git", "show", "%s:%s" % (ref, AUTH_REL)],
                       cwd=REPO, capture_output=True)
    if r.returncode != 0 or not r.stdout:
        return None, "unavailable"
    return json.loads(r.stdout.decode("utf-8")), "git:" + ref


def full_card(text, anchor):
    """The card's whole balanced block, so the reg-box counts as cited text."""
    for m in CARD_OPEN.finditer(text):
        a = re.search(r'\bid="([^"]+)"', m.group(0))
        if a and a.group(1) == anchor:
            return text[m.start():_balanced_end(text, m.start())]
    return ""


def notes_anchor_resolves(ref):
    """'meoclass1/oralnotes/x.html#sec' -> the file exists and carries id=sec."""
    if "#" not in ref:
        return False
    rel, anchor = ref.split("#", 1)
    p = REPO / rel
    if not p.exists():
        return False
    return ('id="%s"' % anchor) in p.read_text(encoding="utf-8")


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cards = manifest["cards"]

    # Sibling batches may share these destination files; anything they
    # authorise is legitimate here too. Keeps this guard from expiring.
    authorised_elsewhere = {}
    for sib in authorisation_manifest_paths(MANIFEST.parent):
        if sib == MANIFEST:
            continue
        for c in json.loads(sib.read_text(encoding="utf-8")).get("cards", []):
            authorised_elsewhere.setdefault(c["file"], set()).add(c["anchor"])

    by_file = {}
    for c in cards:
        by_file.setdefault(c["file"], []).append(c)

    # ---- one final disposition each ----
    fam = [c["family_id"] for c in cards]
    act = [c["production_action_id"] for c in cards]
    homes = ["%s#%s" % (c["file"], c["anchor"]) for c in cards]
    dup = ([f for f in set(fam) if fam.count(f) > 1]
           + [a for a in set(act) if act.count(a) > 1]
           + [h for h in set(homes) if homes.count(h) > 1])
    report("one_disposition_each", not dup, "duplicates %s" % (dup or "-"))

    # ---- the manifest must match the authorisation record exactly ----
    auth, src = load_authorisation(manifest)
    if auth is None:
        for n in ("authorised_family_set", "authorised_count",
                  "authorised_dispositions", "no_tenth_promotion",
                  "no_relationship_action"):
            report(n, False, "authorisation record unavailable (%s)" % src)
    else:
        want = {f["family_id"] for f in auth["families"]
                if f.get("laptop_decision") == "NOTES_TO_QB_PROMOTION"}
        got = set(fam)
        report("authorised_family_set", want == got,
               "manifest %d vs authorisation %d; extra=%s missing=%s [%s]"
               % (len(got), len(want), sorted(got - want) or "-",
                  sorted(want - got) or "-", src))

        declared = auth.get("authorised", {}).get(
            "AUTHORISED_NEW_CARD_NOTES_PROMOTIONS")
        report("authorised_count",
               declared == len(cards) == manifest["initial_authorised_count"],
               "authorisation %s, manifest cards %d, initial_authorised_count %s"
               % (declared, len(cards), manifest["initial_authorised_count"]))

        fams = {f["family_id"]: f for f in auth["families"]}
        bad = []
        for c in cards:
            f = fams.get(c["family_id"])
            if f is None:
                bad.append(c["family_id"] + "(absent)")
                continue
            if f.get("laptop_decision") != "NOTES_TO_QB_PROMOTION":
                bad.append("%s(laptop %s)" % (c["family_id"],
                                              f.get("laptop_decision")))
            if f.get("adjudicated_decision") != "NOTES_TO_QB_PROMOTION":
                bad.append("%s(adjudicated %s)" % (c["family_id"],
                                                   f.get("adjudicated_decision")))
            if f.get("production_action_id") != c["production_action_id"]:
                bad.append(c["family_id"] + "(action)")
        report("authorised_dispositions", not bad, "%s" % (sorted(set(bad)) or "-"))

        # the family the laptop review DOWNGRADED must never reappear here
        d = fams.get(DOWNGRADED, {})
        report("no_tenth_promotion",
               DOWNGRADED not in got
               and d.get("laptop_decision") == "ALREADY_COVERED",
               "%s in manifest=%s, laptop_decision=%s"
               % (DOWNGRADED, DOWNGRADED in got, d.get("laptop_decision")))

        # every action for these families must be the notes-promotion kind
        ids = set(act)
        rel = [a for a in auth.get("production_actions", [])
               if a.get("production_action_id") in ids
               and a.get("kind") != manifest["action_kind"]]
        report("no_relationship_action",
               not rel and manifest.get("examiner_relationship_delta") == 0,
               "%s" % (rel or "manifest delta %s"
                       % manifest.get("examiner_relationship_delta")))

    # ---- the Oral Notes sources must still resolve ----
    unresolved = []
    for c in cards:
        for key in ("notes_source", "notes_source_secondary"):
            ref = c.get(key)
            if ref and not notes_anchor_resolves(ref):
                unresolved.append("%s %s=%s" % (c["family_id"], key, ref))
    report("notes_source_resolves", not unresolved, "%s" % (unresolved or "-"))

    # ---- live pages ----
    missing, dupes, extra, parentage, structural = [], [], [], [], []
    empty, dirty_q, dirty_body, thin_auth, leaked = [], [], [], [], []

    for fname, wanted in sorted(by_file.items()):
        path = QB_DIR / fname
        if not path.exists():
            missing += ["%s (page missing)" % fname]
            continue
        raw = path.read_text(encoding="utf-8", newline="")
        p = Page()
        p.feed(raw)

        anchors = [q for q, _, _ in p.cards if re.fullmatch(r"q\d+", q or "")]
        for c in wanted:
            if c["anchor"] not in anchors:
                missing.append("%s#%s" % (fname, c["anchor"]))
        dupes += ["%s#%s" % (fname, a) for a in set(anchors) if anchors.count(a) > 1]

        structural += ["%s: %s" % (fname, s) for s in p.structure]
        for qid, in_feed, anc in p.cards:
            if not in_feed:
                parentage.append("%s#%s outside #q-feed (%s)" % (fname, qid, anc))

        # a tenth, unauthorised new card in a Batch-D destination
        expected_here = {c["anchor"] for c in wanted}
        allowed_here = expected_here | authorised_elsewhere.get(fname, set())
        baseline_max = min(int(a[1:]) for a in expected_here)
        extra += ["%s#%s" % (fname, q) for q in anchors
                  if int(q[1:]) > baseline_max and q not in allowed_here]

        for c in wanted:
            t = p.text.get(c["anchor"])
            if not t:
                continue
            if len(norm(t["q"])) < 20:
                empty.append("%s#%s question text" % (fname, c["anchor"]))
            if len(t["a"]) < 800:
                empty.append("%s#%s answer body (%d chars)"
                             % (fname, c["anchor"], len(t["a"])))
            for rx, why in QTEXT_FORBIDDEN:
                if rx.search(t["q"]):
                    dirty_q.append("%s#%s %s" % (fname, c["anchor"], why))
            # the whole card, so an instrument cited only in the reg-box counts
            whole = norm(full_card(raw, c["anchor"]))
            for tok in c.get("authority_tokens", []):
                if norm(tok) not in whole:
                    thin_auth.append("%s#%s lacks %r" % (fname, c["anchor"], tok))

        page_text = " ".join("".join(p.body).split())
        for rx, why in FORBIDDEN:
            m = rx.search(page_text)
            if m:
                dirty_body.append("%s %s: %r" % (fname, why, m.group(0)))
        # a Notes source path must never reach the candidate
        for c in wanted:
            for key in ("notes_source", "notes_source_secondary"):
                ref = c.get(key)
                if not ref:
                    continue
                leaf = ref.split("/")[-1].split("#")[0]
                if leaf and leaf in page_text:
                    leaked.append("%s exposes %s" % (fname, leaf))

    report("cards_present", not missing, "missing %s" % (missing or "-"))
    report("anchors_unique", not dupes, "%s" % (dupes or "-"))
    report("no_tenth_card", not extra, "unauthorised new cards %s" % (extra or "-"))
    report("dom_structure", not structural, "%s" % (structural[:5] or "-"))
    report("q_feed_parentage", not parentage, "%s" % (parentage[:5] or "-"))
    report("answer_non_empty", not empty, "%s" % (empty or "-"))
    report("question_text_clean", not dirty_q, "%s" % (dirty_q or "-"))
    report("authority_cited", not thin_auth, "%s" % (thin_auth or "-"))
    report("no_production_metadata", not dirty_body, "%s" % (dirty_body[:5] or "-"))
    report("no_notes_path_leak", not leaked, "%s" % (sorted(set(leaked)) or "-"))

    misplaced = [c["family_id"] for c in cards if not (QB_DIR / c["file"]).exists()]
    report("homes_match_manifest", not misplaced, "%s" % (misplaced or "-"))

    # ---- appending Batch D must not have disturbed any neighbouring card ----
    pinned = manifest.get("baseline_card_digests") or {}
    drifted, unpinned, exempt = [], [], []
    for fname in sorted(by_file):
        live = card_digests((QB_DIR / fname).read_text(encoding="utf-8", newline=""))
        want = pinned.get(fname)
        if want is None:
            unpinned.append(fname)
            continue
        for anchor, dig in want.items():
            # A later batch that authorises this very card is legitimate here too --
            # the same rule already applied to allowed_here above. Without this the
            # pin forbids every future authorised edit and expires on the next batch.
            if anchor in authorised_elsewhere.get(fname, set()):
                exempt.append("%s#%s" % (fname, anchor))
                continue
            if live.get(anchor) != dig:
                drifted.append("%s#%s" % (fname, anchor))
    report("pre_existing_cards_unchanged", not drifted and not unpinned,
           "drifted=%s unpinned=%s authorised-elsewhere=%s"
           % (drifted or "-", unpinned or "-", exempt or "-"))

    # ---- derived index agrees with the live pages ----
    idx = json.loads(CONTENT_INDEX.read_text(encoding="utf-8"))
    total = idx.get("total_questions")
    report("canonical_total_not_regressed",
           isinstance(total, int) and total >= manifest["expected_canonical_questions"],
           "content index %s vs Batch-D milestone %s"
           % (total, manifest["expected_canonical_questions"]))

    indexed = []
    for c in cards:
        entry = idx.get("files", {}).get(c["file"], {})
        got = {q.get("anchor") for q in entry.get("questions", [])}
        if c["anchor"] not in got:
            indexed.append("%s#%s" % (c["file"], c["anchor"]))
    report("indexed", not indexed, "not in content index %s" % (indexed or "-"))

    # ---- the published count must reconcile with what was actually built ----
    n = manifest["actual_new_card_count"]
    base = manifest["baseline_canonical_questions"]
    # The corpus keeps growing after this batch, so pinning the live total to
    # baseline + n expires the moment the next authorised card lands. What
    # Batch D can legitimately assert is that its own nine are still all there
    # - the same reasoning already applied to canonical_total_not_regressed.
    report("count_reconciles",
           n == len(cards)
           and base + n == manifest["expected_canonical_questions"]
           and isinstance(total, int) and total - base >= n,
           "actual %s, cards %d, baseline %s, expected %s, live %s"
           % (n, len(cards), base, manifest["expected_canonical_questions"], total))

    print("\n%d PASS / %d FAIL" % (_checks - len(_fails), len(_fails)))
    return 1 if _fails else 0


if __name__ == "__main__":
    sys.exit(main())
