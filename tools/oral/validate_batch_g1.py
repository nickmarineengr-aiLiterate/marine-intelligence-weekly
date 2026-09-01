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
from oral_manifest import (audit_manifest, authorisation_manifest_paths,
                           sibling_owned_cards)  # noqa: E402
from oral_supersession import resolve_authorised_card_state  # noqa: E402

enable_utf8_stdio()

# Parameterised so a later fresh-intake batch reuses this contract instead of
# copying 300 lines. Defaults are G1, so running this file bare is unchanged.
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


def main(manifest_path=None, review_path=None, label="g1") -> int:
    global MANIFEST, REVIEW
    if manifest_path:
        MANIFEST = pathlib.Path(manifest_path)
    if review_path:
        REVIEW = pathlib.Path(review_path)
    results.clear()
    if not MANIFEST.is_file():
        print("FAIL: %s is absent" % MANIFEST.name)
        return 1
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cards = manifest["cards"]

    # ---- 1. schema ---------------------------------------------------------
    bad = [f.check for f in audit_manifest(MANIFEST) if not f.ok]
    check("%s_manifest_schema_contract" % label, not bad, "violations=%s" % (bad or "none"))

    # ---- 2. authorisation resolves, and fails closed -----------------------
    if not ADJ.is_file():
        check("%s_authorisation_available" % label, False, "adjudication record unavailable")
        for n, ok, d in results:
            print("%-5s %-52s %s" % ("PASS" if ok else "FAIL", n, d))
        return 1
    check("%s_authorisation_available" % label, True, ADJ.name)
    adj = {a["occurrence_id"]: a
           for a in json.loads(ADJ.read_text(encoding="utf-8"))["adjudications"]}

    # ---- 2b. the freeze record, where a batch declares one -----------------
    #
    # G3 is the first batch to freeze every question IDENTITY before writing any
    # answer. The field is LOAD_BEARING, so it is read here rather than trusted:
    # a field no validator opens is decoration, and a manifest showing eleven new
    # cards would otherwise be indistinguishable from one where the bank was
    # never searched. Conditional, so batches without a freeze record are
    # unaffected; fail-closed for any batch that claims one.
    frozen_path = manifest.get("freeze_record")
    if frozen_path:
        fp = REPO / frozen_path
        check("%s_freeze_record_resolves" % label, fp.is_file(), str(frozen_path))
        if fp.is_file():
            frozen = json.loads(fp.read_text(encoding="utf-8"))
            ids = {a.get("occurrence_id") for a in frozen.get("asks", [])}
            produced = {oid for c in cards for oid in c["source_occurrence_ids"]}
            unfrozen = sorted(produced - ids)
            check("%s_every_produced_ask_was_frozen_first" % label, not unfrozen,
                  "produced but never frozen: %s" % (unfrozen or "none"))
            # A frozen ask must be produced OR declared held. Silence is the
            # failure mode: an authorised ask that is quietly dropped and one
            # that was never authorised look identical from cards[] alone.
            held = {h for a in (manifest.get("held_actions") or [])
                    for h in (a.get("source_occurrence_ids") or [])}
            dropped = sorted(ids - produced - held)
            check("%s_every_frozen_ask_is_produced_or_held" % label, not dropped,
                  "frozen but neither produced nor held: %s" % (dropped or "none"))

    # ---- 3. every card traces to an adjudicated occurrence -----------------
    unresolved, mismatched = [], []
    # A card may cite occurrences that CORROBORATE it without driving what kind
    # of action it is - a second candidate reporting the same ask, or a second
    # limb merged into one card. Those are supporting_occurrence_ids and are
    # checked for existence only; source_occurrence_ids alone fixes action_kind.
    for c in cards:
        for oid in c.get("supporting_occurrence_ids", []) or []:
            if oid not in adj:
                unresolved.append("%s->%s (supporting)" % (c["action_id"], oid))
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
    check("%s_every_card_traces_to_an_adjudicated_occurrence" % label,
          not unresolved, "%s" % (unresolved or "none"))
    check("%s_action_kind_agrees_with_adjudication" % label,
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
    check("%s_enrichment_targets_the_card_the_record_named" % label,
          not wrong_target, "%s" % (wrong_target or "none"))

    # ---- 5. corpus expectations --------------------------------------------
    intake_p = ADJ.parent / "AUGUST2026_INTAKE_RECORDS.jsonl"
    by_occurrence = {}
    if intake_p.is_file():
        for line in intake_p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                o = json.loads(line)
                by_occurrence[o["occurrence_id"]] = o

    inv = L.build_inventory()
    n_q = len(inv)
    n_f = len({c["canonical_question_id"].split("#")[0] for c in inv})
    # NOT "the corpus is still exactly the size I left it". That is the expiring
    # guard which turned nine E- and F-series validators red the moment batch G1
    # added a card, and it would have expired here the moment G2 added two. What
    # stays true forever is that the corpus never shrank below what this batch
    # produced, and that the file count is unchanged. Whether a LATER card is
    # authorised is that batch's guard to answer, not this one's - and the cards
    # this batch owns are pinned individually by digest below.
    check("%s_corpus_is_the_expected_size" % label,
          n_q >= manifest["expected_canonical_questions"]
          and n_f == manifest["expected_question_bearing_files"],
          "questions %d (this batch left %d, +%d authorised since), files %d (expect %d)"
          % (n_q, manifest["expected_canonical_questions"],
             n_q - manifest["expected_canonical_questions"],
             n_f, manifest["expected_question_bearing_files"]))
    ids = {c["canonical_question_id"] for c in inv}
    missing = ["%s#%s" % (c["file"].replace(".html", ""), c["anchor"])
               for c in cards
               if "%s#%s" % (c["file"].replace(".html", ""), c["anchor"]) not in ids]
    check("%s_every_declared_card_is_live" % label, not missing, "%s" % (missing or "none"))

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
        live_digest = a.get(c["anchor"])
        if live_digest != c["post_edit_digest"]:
            # A card corrected AFTER this batch shipped is not tampering with
            # this batch: it is a later authorised state descending from this
            # pin. The batch record stays exactly as published - rebaselining a
            # shipped digest would destroy the evidence it exists to carry - and
            # the descent is proved through the shared supersession contract.
            res = resolve_authorised_card_state(
                manifest=MANIFEST.name, action_id=c["action_id"],
                file=c["file"], anchor=c["anchor"],
                pinned_post_digest=c["post_edit_digest"], live_digest=live_digest,
                directory=HERE)
            if not res.ok:
                wrong_post.append("%s (%s)" % (key, res.describe()))
    check("%s_pre_edit_state_is_as_declared" % label, not wrong_pre, "%s" % (wrong_pre or "none"))
    check("%s_post_edit_state_is_live" % label, not wrong_post, "%s" % (wrong_post or "none"))
    check("%s_every_enrichment_actually_changed_its_card" % label,
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
        # A card another authorisation record owns is legitimate here too - a
        # post-release correction may reach a card this batch never declared,
        # and without this the blast-radius guard forbids every future
        # authorised edit anywhere in a file this batch happened to touch.
        elsewhere = sibling_owned_cards(MANIFEST)
        for anchor in sorted(set(b) | set(a)):
            if anchor in anchors or b.get(anchor) == a.get(anchor):
                continue
            if "%s#%s" % (fname, anchor) in elsewhere:
                continue
            strayed.append("%s#%s" % (fname, anchor))
    check("%s_no_undeclared_card_moved_in_a_touched_file" % label,
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
        # A card may name an examiner ONLY where an occurrence behind it is
        # individually attributed to that examiner in the intake store.
        supported = set()
        for oid in (list(c["source_occurrence_ids"])
                    + list(c.get("supporting_occurrence_ids", []) or [])):
            o = by_occurrence.get(oid) or {}
            if (o.get("examiner_attribution") == "INDIVIDUALLY_ATTRIBUTED"
                    and o.get("attributed_examiner")):
                supported.add(o["attributed_examiner"])
        text = card_text((REPO / ("meoclass1/" + c["file"])).read_text(encoding="utf-8"),
                         c["anchor"]) or ""
        for who in EXAMINERS:
            if re.search(r"\b%s\b" % who, text) and who not in supported:
                named.append("%s#%s names %s with no individual attribution behind it"
                             % (c["file"], c["anchor"], who))
    check("%s_new_cards_name_no_examiner" % label, not named, "%s" % (named or "none"))
    check("%s_examiner_relationship_delta_is_declared_zero" % label,
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
    check("%s_no_production_vocabulary_in_a_card" % label, not leaked, "%s" % (leaked or "none"))

    # ---- 10. every new card is behind the paywall --------------------------
    ungated = []
    for c in cards:
        if c["action_kind"] != "NEW_CARD":
            continue
        rows = {r["anchor"]: r for r in L.parse_qb_file(REPO / ("meoclass1/" + c["file"]))}
        r = rows.get(c["anchor"])
        if not r or not r.get("gated") or not r.get("has_answer"):
            ungated.append("%s#%s" % (c["file"], c["anchor"]))
    check("%s_new_cards_are_answered_and_gated" % label, not ungated, "%s" % (ungated or "none"))

    # ---- 11. the batch accounts for what it did NOT produce ----------------
    # Eleven occurrences are adjudicated GENUINE_NEW_QUESTION across both
    # August batches. G1 produces four. The other seven are batch-1 asks that
    # this batch deliberately did not author, and a batch that silently drops
    # authorised work is indistinguishable from one that was never authorised.
    all_new = {o for o, a in adj.items()
               if a["classification"] == "GENUINE_NEW_QUESTION"}
    # Read EVERY authorisation record, not only this batch's. The question the
    # line answers is "which reported new asks still have no card anywhere?",
    # and answering it from one manifest would list a later batch's work as
    # outstanding forever.
    # Through the SHARED authorisation surface, never a private glob. Ten batch
    # validators each grew their own copy of that glob, and widening it in ten
    # places is how the batch and correction record families drifted apart.
    # The surface is strictly wider than the old glob -- it includes correction
    # records -- and that is correct rather than merely harmless: the loop
    # counts NEW_CARD actions, so a correction that ever created one would now
    # be seen, where before it would have read as outstanding work forever.
    produced = set()
    for mp in authorisation_manifest_paths(HERE):
        try:
            rec = json.loads(mp.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for c in rec.get("cards", []):
            if c.get("action_kind") != "NEW_CARD":
                continue
            produced.update(list(c.get("source_occurrence_ids") or [])
                            + list(c.get("supporting_occurrence_ids") or []))
    outstanding = sorted(all_new - produced)
    check("%s_unproduced_new_asks_are_still_visible" % label,
          len([c for c in cards if c["action_kind"] == "NEW_CARD"])
          == manifest["actual_new_card_count"],
          "this batch created %d card(s); %d of %d adjudicated new asks now have "
          "a card somewhere; still outstanding: %s"
          % (len([c for c in cards if c["action_kind"] == "NEW_CARD"]),
             len(all_new & produced), len(all_new), outstanding))

    # ---- 12. the batch was reviewed ---------------------------------------
    if not REVIEW.is_file():
        check("%s_review_record_present" % label, False, "review record unavailable")
    else:
        rev = json.loads(REVIEW.read_text(encoding="utf-8"))
        reviewed = {r["action_id"]: r for r in rev.get("cards", [])}
        unreviewed = [c["action_id"] for c in cards
                      if reviewed.get(c["action_id"], {}).get("verdict") != "PASS"]
        check("%s_review_record_present" % label, True, rev.get("review_id", "-"))
        check("%s_every_card_passed_review" % label, not unreviewed,
              "without a PASS verdict: %s" % (unreviewed or "none"))
        check("%s_review_states_its_independence" % label,
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
