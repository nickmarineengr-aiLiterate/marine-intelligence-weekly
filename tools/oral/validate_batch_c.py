"""Guard the five laptop-authorised P2 new canonical Q&A cards.

batch_c_manifest.json is the authority for which family id lives at which
file#anchor. This validator proves, against the LIVE QB HTML rather than any
derived artefact, that:

  * every authorised card exists, exactly once, at its recorded home;
  * the manifest's family set is exactly the authorisation record's P2 batch,
    and every one of those families is still NEW_CANONICAL_QA at the exact
    laptop_review_status the manifest records for it;
  * no sixth, unauthorised Batch-C card has appeared in a Batch-C destination;
  * each new card's anchor is unique on its page and sits under #q-feed;
  * each new card carries a clean candidate-facing question and a real answer;
  * each new card actually cites the primary authority its topic requires;
  * no production metadata is candidate-visible anywhere on those pages;
  * no pre-existing card on a Batch-C page has drifted;
  * the derived content index carries all five and has not regressed.

WHY THE DISPOSITION CHECK IS PER-CARD, NOT A BLANKET EQUALITY
Four of the five families carry laptop_review_status LAPTOP_CONFIRMED. GAP-0516
carries LAPTOP_CHANGED, because the laptop review PROMOTED it from a held
medium-confidence row into an authorised HIGH/P2 new card - that field records
that the row was ALTERED, not that it was refused. Batch B's validator asserted
LAPTOP_CONFIRMED for all ten of its families, which would reject GAP-0516 here.
Rather than relax that to "any status", the manifest records the expected status
for each family and this validator asserts an exact match. That is strictly
TIGHTER than a blanket equality: it pins five specific dispositions, so a silent
change to any one of them - in either direction - fails the build.

The corpus total is asserted as a FLOOR, never an equality, and the sixth-card
guard unions every sibling batch_*_manifest.json, so this guard does not expire
when a later authorised batch lands. Batch A's guard had to be repaired for
exactly that reason.

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
from validate_batch_b import card_digests  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
MANIFEST = Path(__file__).resolve().parent / "batch_c_manifest.json"
QB_DIR = REPO / "meoclass1"
CONTENT_INDEX = QB_DIR / "qb_content_index.json"
AUTH_REL = ("meoclass1/oral-intelligence/examiner-audit/"
            "FINAL_ORAL_PRODUCTION_AUTHORIZATION.json")

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

    # ---- the manifest must match the authorisation record exactly ----
    auth, src = load_authorisation(manifest)
    if auth is None:
        report("authorised_family_set", False,
               "authorisation record unavailable (%s) - cannot confirm linkage" % src)
        report("authorised_dispositions", False, "authorisation record unavailable")
        report("no_relationship_action", False, "authorisation record unavailable")
    else:
        key = manifest["authorisation_batch_key"].split(".")[-1]
        want = set(auth["batches"][key])
        got = {c["family_id"] for c in cards}
        report("authorised_family_set", want == got,
               "manifest %d vs authorisation %d; extra=%s missing=%s [%s]"
               % (len(got), len(want), sorted(got - want) or "-",
                  sorted(want - got) or "-", src))

        fams = {f["family_id"]: f for f in auth["families"]}
        bad = []
        for c in cards:
            f = fams.get(c["family_id"])
            if f is None:
                bad.append(c["family_id"] + "(absent)")
                continue
            if (f.get("adjudicated_decision") != "NEW_CANONICAL_QA"
                    or f.get("laptop_decision") != "NEW_CANONICAL_QA"
                    or f.get("priority") != "P2"
                    or f.get("confidence") != "HIGH"):
                bad.append(c["family_id"])
            # exact, per-family disposition - see module docstring
            if f.get("laptop_review_status") != c.get("laptop_review_status"):
                bad.append("%s(status %s != %s)" % (
                    c["family_id"], f.get("laptop_review_status"),
                    c.get("laptop_review_status")))
            if f.get("production_action_id") != c["production_action_id"]:
                bad.append(c["family_id"] + "(action)")
        report("authorised_dispositions", not bad, "%s" % (sorted(set(bad)) or "-"))

        # a relationship delta is authorised for none of these families
        rel = [a for a in auth.get("production_actions", [])
               if a.get("production_action_id") in {c["production_action_id"] for c in cards}
               and a.get("kind") != "NEW_CARD_FROM_GAP"]
        report("no_relationship_action",
               not rel and manifest.get("examiner_relationship_delta") == 0,
               "%s" % (rel or "manifest delta %s"
                       % manifest.get("examiner_relationship_delta")))

    # ---- live pages ----
    missing, dupes, sixth, parentage, structural = [], [], [], [], []
    empty, dirty_q, dirty_body, thin_auth = [], [], [], []

    for fname, wanted in sorted(by_file.items()):
        path = QB_DIR / fname
        if not path.exists():
            missing += ["%s (page missing)" % fname]
            continue
        p = Page()
        p.feed(path.read_text(encoding="utf-8", newline=""))

        anchors = [q for q, _, _ in p.cards if re.fullmatch(r"q\d+", q or "")]
        for c in wanted:
            if c["anchor"] not in anchors:
                missing.append("%s#%s" % (fname, c["anchor"]))
        dupes += ["%s#%s" % (fname, a) for a in set(anchors) if anchors.count(a) > 1]

        structural += ["%s: %s" % (fname, s) for s in p.structure]
        for qid, in_feed, anc in p.cards:
            if not in_feed:
                parentage.append("%s#%s outside #q-feed (%s)" % (fname, qid, anc))

        # a sixth, unauthorised new card in a Batch-C destination
        expected_here = {c["anchor"] for c in wanted}
        allowed_here = expected_here | authorised_elsewhere.get(fname, set())
        baseline_max = min(int(a[1:]) for a in expected_here)
        sixth += ["%s#%s" % (fname, q) for q in anchors
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
            # the card must actually cite the authority its topic rests on
            answer = norm(t["a"])
            for tok in c.get("authority_tokens", []):
                if norm(tok) not in answer:
                    thin_auth.append("%s#%s lacks %r" % (fname, c["anchor"], tok))

        page_text = " ".join("".join(p.body).split())
        for rx, why in FORBIDDEN:
            m = rx.search(page_text)
            if m:
                dirty_body.append("%s %s: %r" % (fname, why, m.group(0)))

    report("cards_present", not missing, "missing %s" % (missing or "-"))
    report("anchors_unique", not dupes, "%s" % (dupes or "-"))
    report("no_sixth_card", not sixth, "unauthorised new cards %s" % (sixth or "-"))
    report("dom_structure", not structural, "%s" % (structural[:5] or "-"))
    report("q_feed_parentage", not parentage, "%s" % (parentage[:5] or "-"))
    report("answer_non_empty", not empty, "%s" % (empty or "-"))
    report("question_text_clean", not dirty_q, "%s" % (dirty_q or "-"))
    report("authority_cited", not thin_auth, "%s" % (thin_auth or "-"))
    report("no_production_metadata", not dirty_body, "%s" % (dirty_body[:5] or "-"))

    misplaced = [c["family_id"] for c in cards if not (QB_DIR / c["file"]).exists()]
    report("homes_match_manifest", not misplaced, "%s" % (misplaced or "-"))

    # ---- appending Batch C must not have disturbed any neighbouring card ----
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
           "content index %s vs Batch-C milestone %s"
           % (total, manifest["expected_canonical_questions"]))

    indexed = []
    for c in cards:
        entry = idx.get("files", {}).get(c["file"], {})
        got = {q.get("anchor") for q in entry.get("questions", [])}
        if c["anchor"] not in got:
            indexed.append("%s#%s" % (c["file"], c["anchor"]))
    report("indexed", not indexed, "not in content index %s" % (indexed or "-"))

    print("\n%d PASS / %d FAIL" % (_checks - len(_fails), len(_fails)))
    return 1 if _fails else 0


if __name__ == "__main__":
    sys.exit(main())
