"""Validate batch G1 - the August 2026 fresh-intake production batch.

G1 is the first batch whose authorisation is a CURRENT-intake adjudication
record rather than the historical 788 disposition. So the load-bearing question
is different from every earlier batch: not "did the consolidation authorise this
card?" but "does this card trace to an occurrence a named candidate actually
reported at the August 2026 sitting, adjudicated as needing one?".

Fails closed: if the adjudication record is unavailable, that is a failure and
never a skip.

  PYTHONIOENCODING=utf-8 python tools/oral/validate_batch_g1.py

Exit 0 all checks pass, 1 one or more failed.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio      # noqa: E402
import oral_lib as L                          # noqa: E402
from oral_manifest import audit_manifest      # noqa: E402

enable_utf8_stdio()

MANIFEST = HERE / "batch_g1_manifest.json"
ADJ = (REPO / "meoclass1" / "oral-intelligence" / "examiner-audit"
       / "AUGUST2026_INTAKE_ADJUDICATIONS.json")
REVIEW = (REPO / "meoclass1" / "oral-intelligence" / "examiner-audit"
          / "AUGUST2026_BATCH_G1_REVIEW.json")

# An adjudication class maps to exactly one kind of production action.
ACTION_FOR = {
    "GENUINE_NEW_QUESTION": "NEW_CARD",
    "FOLLOWUP": "ENRICH_EXISTING",
}

# The seven examiner identities the bank recognises. A G1 card must name none
# of them: the August panel is known but no batch-2 occurrence except AUG-0032
# carries a per-question attribution, and a candidate-facing card is not the
# place to record a panel-level fact.
EXAMINERS = ("Rajappan", "Senthil", "Nair", "Simon", "Paul", "John", "Srivastava")

# Production vocabulary that must never reach a candidate.
LEAK = re.compile(r"AUG-\d{4}|ASC-\d{4}|G1-\d{3}|GENUINE_NEW_QUESTION|"
                  r"PARAPHRASE_EXISTING|EXACT_EXISTING|PANEL_LEVEL_ONLY|"
                  r"INDIVIDUALLY_ATTRIBUTED|NON_QUESTION_UNRECOVERABLE|"
                  r"negative_search|occurrence_id")

CARD_OPEN = re.compile(r'<div class="q-card"[^>]*>')

results: list[tuple[str, bool, str]] = []


def check(name: str, ok, detail: str = "") -> None:
    results.append((name, bool(ok), detail))


def git_show(ref: str, rel: str):
    out = subprocess.run(["git", "show", "%s:%s" % (ref, rel)],
                         cwd=str(REPO), capture_output=True)
    return out.stdout.decode("utf-8", "replace") if out.returncode == 0 else None


def _balanced_end(text: str, start: int) -> int:
    """End index of the div opened at `start`, by balanced <div> nesting."""
    depth, i = 0, start
    tag = re.compile(r"<(/?)div\b", re.I)
    while True:
        m = tag.search(text, i)
        if not m:
            return len(text)
        depth += -1 if m.group(1) else 1
        i = m.end()
        if depth == 0:
            close = text.find(">", i)
            return (close + 1) if close >= 0 else len(text)


def card_digests(text: str) -> dict:
    """anchor -> sha256 over the card's balanced block, on LF-normalised bytes.

    LF-normalised because .gitattributes pins these pages to LF in the object
    store while the working tree may hold CRLF - QB3_G does - and a raw-byte
    digest would then report every card on a CRLF page as changed.
    """
    text = text.replace("\r\n", "\n")
    out = {}
    for m in CARD_OPEN.finditer(text):
        a = re.search(r'\bid="([^"]+)"', m.group(0))
        if a:
            out[a.group(1)] = hashlib.sha256(
                text[m.start():_balanced_end(text, m.start())].encode("utf-8")
            ).hexdigest()
    return out


def card_text(text: str, anchor: str) -> str | None:
    for m in CARD_OPEN.finditer(text):
        a = re.search(r'\bid="([^"]+)"', m.group(0))
        if a and a.group(1) == anchor:
            return text[m.start():_balanced_end(text, m.start())]
    return None


def main() -> int:
    if not MANIFEST.is_file():
        print("FAIL: %s is absent" % MANIFEST.name)
        return 1
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cards = manifest["cards"]

    # ---- 1. schema ---------------------------------------------------------
    bad = [f.check for f in audit_manifest(MANIFEST) if not f.ok]
    check("g1_manifest_schema_contract", not bad, "violations=%s" % (bad or "none"))

    # ---- 2. authorisation resolves, and fails closed -----------------------
    if not ADJ.is_file():
        check("g1_authorisation_available", False, "adjudication record unavailable")
        for n, ok, d in results:
            print("%-5s %-52s %s" % ("PASS" if ok else "FAIL", n, d))
        return 1
    check("g1_authorisation_available", True, ADJ.name)
    adj = {a["occurrence_id"]: a
           for a in json.loads(ADJ.read_text(encoding="utf-8"))["adjudications"]}

    # ---- 3. every card traces to an adjudicated occurrence -----------------
    unresolved, mismatched = [], []
    for c in cards:
        for oid in c["source_occurrence_ids"]:
            a = adj.get(oid)
            if a is None:
                unresolved.append("%s->%s" % (c["action_id"], oid))
                continue
            if a["classification"] != c["adjudication"]:
                mismatched.append("%s: manifest %s vs record %s"
                                  % (oid, c["adjudication"], a["classification"]))
            if ACTION_FOR.get(a["classification"]) != c["action_kind"]:
                mismatched.append("%s: %s must produce %s, manifest says %s"
                                  % (oid, a["classification"],
                                     ACTION_FOR.get(a["classification"]),
                                     c["action_kind"]))
    check("g1_every_card_traces_to_an_adjudicated_occurrence",
          not unresolved, "%s" % (unresolved or "none"))
    check("g1_action_kind_agrees_with_adjudication",
          not mismatched, "%s" % (mismatched or "none"))

    # ---- 4. an enrichment must target the card the record named ------------
    wrong_target = []
    for c in cards:
        if c["action_kind"] != "ENRICH_EXISTING":
            continue
        for oid in c["source_occurrence_ids"]:
            want = (adj.get(oid) or {}).get("matched_question_id")
            got = "%s#%s" % (c["file"].replace(".html", ""), c["anchor"])
            if want != got:
                wrong_target.append("%s: record says %s, batch edited %s"
                                    % (oid, want, got))
    check("g1_enrichment_targets_the_card_the_record_named",
          not wrong_target, "%s" % (wrong_target or "none"))

    # ---- 5. corpus expectations --------------------------------------------
    inv = L.build_inventory()
    n_q = len(inv)
    n_f = len({c["canonical_question_id"].split("#")[0] for c in inv})
    check("g1_corpus_is_the_expected_size",
          n_q == manifest["expected_canonical_questions"]
          and n_f == manifest["expected_question_bearing_files"],
          "questions %d (expect %d), files %d (expect %d)"
          % (n_q, manifest["expected_canonical_questions"],
             n_f, manifest["expected_question_bearing_files"]))
    ids = {c["canonical_question_id"] for c in inv}
    missing = ["%s#%s" % (c["file"].replace(".html", ""), c["anchor"])
               for c in cards
               if "%s#%s" % (c["file"].replace(".html", ""), c["anchor"]) not in ids]
    check("g1_every_declared_card_is_live", not missing, "%s" % (missing or "none"))

    # ---- 6. pre and post state, against the declared baseline --------------
    base = manifest["baseline_commit"]
    wrong_pre, wrong_post, unchanged = [], [], []
    for c in cards:
        rel = "meoclass1/" + c["file"]
        before = git_show(base, rel)
        after = (REPO / rel).read_text(encoding="utf-8")
        b = card_digests(before) if before is not None else {}
        a = card_digests(after)
        key = "%s#%s" % (c["file"], c["anchor"])
        if c["action_kind"] == "NEW_CARD" and c["anchor"] in b:
            wrong_pre.append(key + " (claims NEW_CARD but existed at baseline)")
        if c["action_kind"] == "ENRICH_EXISTING":
            if b.get(c["anchor"]) != c.get("pre_edit_digest"):
                wrong_pre.append(key + " (pre-edit digest does not match baseline)")
            if b.get(c["anchor"]) == a.get(c["anchor"]):
                unchanged.append(key)
        if a.get(c["anchor"]) != c["post_edit_digest"]:
            wrong_post.append(key)
    check("g1_pre_edit_state_is_as_declared", not wrong_pre, "%s" % (wrong_pre or "none"))
    check("g1_post_edit_state_is_live", not wrong_post, "%s" % (wrong_post or "none"))
    check("g1_every_enrichment_actually_changed_its_card",
          not unchanged, "%s" % (unchanged or "none"))

    # ---- 7. blast radius: no undeclared card moved in a touched file -------
    owned = {}
    for c in cards:
        owned.setdefault(c["file"], set()).add(c["anchor"])
    strayed = []
    for fname, anchors in owned.items():
        rel = "meoclass1/" + fname
        before = git_show(base, rel)
        if before is None:
            continue
        b, a = card_digests(before), card_digests((REPO / rel).read_text(encoding="utf-8"))
        for anchor in sorted(set(b) | set(a)):
            if anchor in anchors or b.get(anchor) == a.get(anchor):
                continue
            strayed.append("%s#%s" % (fname, anchor))
    check("g1_no_undeclared_card_moved_in_a_touched_file",
          not strayed, "%s" % (strayed or "none"))

    # ---- 8. attribution discipline reaches the card ------------------------
    # The August panel is known, but only AUG-0032 carries a per-question
    # attribution. No G1 card may name an examiner: doing so would assert an
    # attribution no candidate wrote, and would silently add relationships to
    # the derived examiner index.
    named = []
    for c in cards:
        if c["action_kind"] != "NEW_CARD":
            continue
        text = card_text((REPO / ("meoclass1/" + c["file"])).read_text(encoding="utf-8"),
                         c["anchor"]) or ""
        for who in EXAMINERS:
            if re.search(r"\b%s\b" % who, text):
                named.append("%s#%s names %s" % (c["file"], c["anchor"], who))
    check("g1_new_cards_name_no_examiner", not named, "%s" % (named or "none"))
    check("g1_examiner_relationship_delta_is_declared_zero",
          manifest.get("examiner_relationship_delta") == 0,
          "declared %s" % manifest.get("examiner_relationship_delta"))

    # ---- 9. no production vocabulary reached a candidate -------------------
    leaked = []
    for c in cards:
        text = card_text((REPO / ("meoclass1/" + c["file"])).read_text(encoding="utf-8"),
                         c["anchor"]) or ""
        m = LEAK.search(text)
        if m:
            leaked.append("%s#%s: %s" % (c["file"], c["anchor"], m.group(0)))
    check("g1_no_production_vocabulary_in_a_card", not leaked, "%s" % (leaked or "none"))

    # ---- 10. every new card is behind the paywall --------------------------
    ungated = []
    for c in cards:
        if c["action_kind"] != "NEW_CARD":
            continue
        rows = {r["anchor"]: r for r in L.parse_qb_file(REPO / ("meoclass1/" + c["file"]))}
        r = rows.get(c["anchor"])
        if not r or not r.get("gated") or not r.get("has_answer"):
            ungated.append("%s#%s" % (c["file"], c["anchor"]))
    check("g1_new_cards_are_answered_and_gated", not ungated, "%s" % (ungated or "none"))

    # ---- 11. the batch accounts for what it did NOT produce ----------------
    # Eleven occurrences are adjudicated GENUINE_NEW_QUESTION across both
    # August batches. G1 produces four. The other seven are batch-1 asks that
    # this batch deliberately did not author, and a batch that silently drops
    # authorised work is indistinguishable from one that was never authorised.
    all_new = {o for o, a in adj.items()
               if a["classification"] == "GENUINE_NEW_QUESTION"}
    produced = {o for c in cards for o in c["source_occurrence_ids"]
                if c["action_kind"] == "NEW_CARD"}
    outstanding = sorted(all_new - produced)
    check("g1_unproduced_new_asks_are_still_visible",
          len(produced) == manifest["actual_new_card_count"],
          "produced %d of %d adjudicated new asks; still outstanding: %s"
          % (len(produced), len(all_new), outstanding))

    # ---- 12. the batch was reviewed ---------------------------------------
    if not REVIEW.is_file():
        check("g1_review_record_present", False, "review record unavailable")
    else:
        rev = json.loads(REVIEW.read_text(encoding="utf-8"))
        reviewed = {r["action_id"]: r for r in rev.get("cards", [])}
        unreviewed = [c["action_id"] for c in cards
                      if reviewed.get(c["action_id"], {}).get("verdict") != "PASS"]
        check("g1_review_record_present", True, rev.get("review_id", "-"))
        check("g1_every_card_passed_review", not unreviewed,
              "without a PASS verdict: %s" % (unreviewed or "none"))
        check("g1_review_states_its_independence",
              rev.get("independence") in ("INDEPENDENT_CLEAN_CONTEXT",
                                          "SAME_CONTEXT_VERIFICATION"),
              "independence=%s" % rev.get("independence"))

    for name, ok, detail in results:
        print("%-5s %-52s %s" % ("PASS" if ok else "FAIL", name, detail))
    failed = [n for n, ok, _ in results if not ok]
    print("\n%d PASS / %d FAIL" % (len(results) - len(failed), len(failed)))
    if failed:
        print("failed: " + ", ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
