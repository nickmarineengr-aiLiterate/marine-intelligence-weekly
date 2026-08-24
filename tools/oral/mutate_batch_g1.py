#!/usr/bin/env python3
"""Mutation suite for batch G1 - the August 2026 fresh-intake production.

WHAT THIS SUITE HAS TO PROVE
----------------------------
G1 introduced a second evidence lane into the Oral bank. The historical 788 was
already governed; this batch is driven by a CURRENT intake that is still open
and still receiving submissions. Every new mechanism is a new way to ship a
false green, so the suite attacks the lane boundary as hard as the content::

    delete a fresh occurrence            -> the intake must not silently shrink
    file a fresh occurrence as historical -> 788 must never absorb August
    claim a second card for one ask      -> duplicates must be impossible
    name an examiner with no evidence    -> attribution must stay earned
    rewrite raw candidate wording        -> evidence must be immutable
    author from an unadjudicated ask     -> identity must precede production
    publish without a review record      -> review must be required
    launder a follow-up into a new card  -> the chain must not be flattened
    strip a negative search              -> a gap claim must stay provable
    create a final workbook              -> the freeze gate must hold while open
    delete the prior workbook            -> history must not be overwritten
    move the historical denominator      -> 788 must be pinned
    name an examiner inside a card       -> the discipline must reach the product
    edit a neighbouring card             -> the blast radius must be bounded
    leak production vocabulary           -> the candidate must never see it

EACH MUTATION MUST TRIP ITS OWN NAMED CHECK
-------------------------------------------
A validator failing for the wrong reason is not evidence. Breaking a DIFFERENT
check than the one named counts as an escape, not as a catch.

  PYTHONIOENCODING=utf-8 python tools/oral/mutate_batch_g1.py
"""
from __future__ import annotations

import io
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio      # noqa: E402

enable_utf8_stdio()

OUT = REPO / "meoclass1" / "oral-intelligence" / "examiner-audit"
RECORDS = OUT / "AUGUST2026_INTAKE_RECORDS.jsonl"
ADJ = OUT / "AUGUST2026_INTAKE_ADJUDICATIONS.json"
REVIEW = OUT / "AUGUST2026_BATCH_G1_REVIEW.json"
HIST = OUT / "ALL_SURVEYORS_SOURCE_RECORDS.jsonl"
MANIFEST = HERE / "batch_g1_manifest.json"
QBOOK = REPO / "docs" / "MIW-master-Question-bank"
JULY = QBOOK / "MIW_July2026_QuestionBank_SHARE.xlsx"
FAKE_V27 = QBOOK / "MIW_August2026_QuestionBank_v27_FINAL.xlsx"
QB2E = REPO / "meoclass1" / "QB2_E.html"
QB9D = REPO / "meoclass1" / "QB9_D.html"

INTAKE = "validate_oral_intake.py"
G1 = "validate_batch_g1.py"
INGEST = "ingest_august_intake.py"
TXT = ("docs/MIW-master-Question-bank/New questions from August orals/"
       "24 Aug 2026 oral questions.txt")


class Snapshot:
    """Byte snapshot of the files a mutation may touch, restored by exact path.

    Never a git checkout: `git checkout <ref> -- <file>` destroys uncommitted
    edits in the working tree, and this suite runs against a dirty tree by
    definition.
    """

    def __init__(self, paths):
        self.data = {p: (p.read_bytes() if p.is_file() else None) for p in paths}

    def restore(self):
        bad = []
        for p, b in self.data.items():
            if b is None:
                if p.is_file():
                    p.unlink()
            else:
                p.write_bytes(b)
                if p.read_bytes() != b:
                    bad.append(str(p))
        return bad


def run(script, *args):
    r = subprocess.run([sys.executable, str(HERE / script), *args],
                       cwd=str(REPO), capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def failing_checks(text):
    return {m.group(1) for m in re.finditer(r"^FAIL\s+(\S+)", text, re.M)}


# ------------------------------------------------------------------ mutations
def jsonl_rows(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def write_jsonl(p, rows):
    p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                 encoding="utf-8")


def m_delete_occurrence():
    rows = jsonl_rows(RECORDS)
    write_jsonl(RECORDS, [r for r in rows if r["occurrence_id"] != "AUG-0032"])


def m_fresh_into_historical():
    rows = jsonl_rows(HIST)
    rows.append({**rows[0], "source_id": "AUG-0032"})
    write_jsonl(HIST, rows)


def m_duplicate_new_ask():
    d = json.loads(ADJ.read_text(encoding="utf-8"))
    victim = next(a for a in d["adjudications"]
                  if a["classification"] == "GENUINE_NEW_QUESTION")
    twin = dict(victim)
    twin["occurrence_id"] = "AUG-0031"
    d["adjudications"] = [twin if a["occurrence_id"] == "AUG-0031" else a
                          for a in d["adjudications"]]
    ADJ.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


def m_unevidenced_examiner():
    rows = jsonl_rows(RECORDS)
    for r in rows:
        if r["occurrence_id"] == "AUG-0024":
            r["examiner_attribution"] = "INDIVIDUALLY_ATTRIBUTED"
            r["attributed_examiner"] = "Nair"
            r["attribution_marker"] = None
    write_jsonl(RECORDS, rows)


def m_rewrite_raw_wording():
    rows = jsonl_rows(RECORDS)
    for r in rows:
        if r["occurrence_id"] == "AUG-0031":
            r["raw_question_text"] = "Lifeboat and rescue boat difference (tidied up)"
    write_jsonl(RECORDS, rows)


def m_unadjudicated_source():
    d = json.loads(MANIFEST.read_text(encoding="utf-8"))
    d["cards"][0]["source_occurrence_ids"] = ["AUG-9999"]
    MANIFEST.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")


def m_remove_review():
    REVIEW.unlink()


def m_launder_followup():
    d = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for c in d["cards"]:
        if c["action_id"] == "G1-007":
            c["action_kind"] = "NEW_CARD"
    MANIFEST.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")


def m_strip_negative_search():
    d = json.loads(ADJ.read_text(encoding="utf-8"))
    for a in d["adjudications"]:
        if a["occurrence_id"] == "AUG-0026":
            a.pop("negative_search", None)
    ADJ.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


def m_create_final_workbook():
    FAKE_V27.write_bytes(b"PK\x03\x04 not a real workbook, a freeze-gate fixture")


def m_delete_prior_workbook():
    JULY.unlink()


def m_move_historical_denominator():
    rows = jsonl_rows(HIST)
    write_jsonl(HIST, rows[:-1])


def m_name_examiner_in_card():
    t = io.open(QB2E, encoding="utf-8", newline="").read()
    t = t.replace("<strong>CE Oral Tip:</strong> <p>Open with <strong>purpose</strong>",
                  "<strong>CE Oral Tip:</strong> <p>Rajappan opens with <strong>purpose</strong>", 1)
    io.open(QB2E, "w", encoding="utf-8", newline="").write(t)


def m_edit_neighbouring_card():
    """Edit a card in a file this batch touched that NO record owns.

    The original target was QB2_E#q1. That card is now owned by the
    independent-review correction record, so the blast-radius guard exempts it
    correctly and the mutation stopped proving anything - a mutation that
    cannot fail is not evidence. QB9_D#q1 is in a file batch G1 touched and is
    owned by no manifest.
    """
    t = io.open(QB9D, encoding="utf-8", newline="").read()
    m = re.search(r'(<div class="q-card"[^>]*id="q1"[\s\S]{0,4000}?<div class="q-text">)', t)
    if not m:
        return
    t = t[:m.end()] + "MUTATED " + t[m.end():]
    io.open(QB9D, "w", encoding="utf-8", newline="").write(t)


def m_leak_production_vocabulary():
    t = io.open(QB2E, encoding="utf-8", newline="").read()
    t = t.replace("Lifeboat and rescue boat &mdash; what is the difference?",
                  "Lifeboat and rescue boat &mdash; what is the difference? (AUG-0031)", 1)
    io.open(QB2E, "w", encoding="utf-8", newline="").write(t)


MUTATIONS = [
    ("A", "delete a fresh occurrence from the intake store",
     [RECORDS], m_delete_occurrence, INTAKE,
     "A2_every_intake_occurrence_adjudicated"),
    ("B", "file a fresh AUG occurrence in the historical ledger",
     [HIST], m_fresh_into_historical, INTAKE,
     "A4_no_intake_id_in_historical_ledger"),
    ("C", "claim a second new card for an ask already claimed",
     [ADJ], m_duplicate_new_ask, INTAKE,
     "A12_no_two_occurrences_claim_the_same_new_card"),
    ("D", "attribute a question to an examiner with no marker",
     [RECORDS], m_unevidenced_examiner, INTAKE,
     "A10_intake_attribution_matches_evidence"),
    ("E", "rewrite a candidate's raw wording",
     [RECORDS], m_rewrite_raw_wording, INGEST, "__ingest_drift__"),
    ("F", "author a card from an unadjudicated occurrence",
     [MANIFEST], m_unadjudicated_source, G1,
     "g1_every_card_traces_to_an_adjudicated_occurrence"),
    ("G", "publish the batch with no review record",
     [REVIEW], m_remove_review, G1, "g1_review_record_present"),
    ("H", "launder an examiner follow-up into a new card",
     [MANIFEST], m_launder_followup, G1,
     "g1_action_kind_agrees_with_adjudication"),
    ("I", "strip the negative search from a new-card claim",
     [ADJ], m_strip_negative_search, INTAKE,
     "A9_new_card_claims_carry_negative_search"),
    ("J", "create a final August workbook while intake is open",
     [FAKE_V27], m_create_final_workbook, INTAKE,
     "Z1_no_final_august_workbook_while_intake_open"),
    ("K", "delete the prior July/v26 workbook",
     [JULY], m_delete_prior_workbook, INTAKE,
     "Z2_prior_july_v26_workbooks_preserved"),
    ("L", "move the historical 788 denominator",
     [HIST], m_move_historical_denominator, INTAKE,
     "H1_historical_count_is_788"),
    ("M", "name an examiner inside a new card",
     [QB2E], m_name_examiner_in_card, G1, "g1_new_cards_name_no_examiner"),
    ("N", "edit a neighbouring card the batch never declared",
     [QB9D], m_edit_neighbouring_card, G1,
     "g1_no_undeclared_card_moved_in_a_touched_file"),
    ("O", "leak an occurrence id into candidate-facing text",
     [QB2E], m_leak_production_vocabulary, G1,
     "g1_no_production_vocabulary_in_a_card"),
]


def probe(script):
    if script == INGEST:
        rc, out = run(INGEST, "--txt", TXT, "--check")
        return rc, ({"__ingest_drift__"} if rc != 0 else set()), out
    rc, out = run(script)
    return rc, failing_checks(out), out


def main() -> int:
    if not MANIFEST.is_file():
        print("G1 manifest missing")
        return 2
    if FAKE_V27.is_file():
        print("stale freeze-gate fixture on disk: %s" % FAKE_V27.name)
        return 2

    # ---- preflight: every mutation must really change bytes ----------------
    print("--- preflight: every mutation must change bytes ---")
    no_ops = []
    for mid, desc, files, apply, _s, _c in MUTATIONS:
        snap = Snapshot(files)
        before = dict(snap.data)
        try:
            apply()
        except Exception as exc:                                   # noqa: BLE001
            print("%-3s ERROR %s: %s" % (mid, type(exc).__name__, exc))
            no_ops.append(mid)
            snap.restore()
            continue
        after = {p: (p.read_bytes() if p.is_file() else None) for p in before}
        changed = any(before[p] != after[p] for p in before)
        delta = sum(len(after[p] or b"") - len(before[p] or b"") for p in before)
        print("%-3s %-56s %-7s byte_delta=%+d"
              % (mid, desc, "applied" if changed else "NO-OP", delta))
        if not changed:
            no_ops.append(mid)
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2
    if no_ops:
        print("\npreflight FAILED - these mutations change no bytes: %s"
              % ", ".join(no_ops))
        return 1

    # ---- control: the unmutated tree must be green -------------------------
    print("\n--- control: unmutated state ---")
    baseline = {}
    for script in (INTAKE, G1, INGEST):
        rc, failing, _ = probe(script)
        print("    %-26s exit=%d failing=%s" % (script, rc, sorted(failing) or "none"))
        baseline[script] = failing
        if failing:
            print("PRE-RUN: %s is already failing; a mutation caught here would be "
                  "caught by something else. Aborting." % script)
            return 2

    # ---- the suite ---------------------------------------------------------
    print("\n--- mutations ---")
    escapes, residue = [], []
    for mid, desc, files, apply, script, expect in MUTATIONS:
        snap = Snapshot(files)
        apply()
        rc, failing, _ = probe(script)
        new = failing - baseline[script]
        caught = expect in new
        verdict = "CAUGHT" if caught else "ESCAPED"
        if not caught:
            escapes.append("%s (%s): expected %s, got %s"
                           % (mid, desc, expect, sorted(new) or "nothing"))
        print("%-3s %-56s %-8s exit=%d  %s"
              % (mid, desc, verdict, rc, expect if caught else (sorted(new) or "no failure")))
        bad = snap.restore()
        if bad:
            residue.append("%s: %s" % (mid, bad))

    # ---- post-run: the tree must be exactly as it was ----------------------
    print("\n--- post-run: the tree must be green again ---")
    for script in (INTAKE, G1, INGEST):
        rc, failing, _ = probe(script)
        print("    %-26s exit=%d failing=%s" % (script, rc, sorted(failing) or "none"))
        if failing:
            residue.append("%s still failing after restore: %s" % (script, sorted(failing)))

    print("\n%d mutations, %d escape(s), 0 no-op(s), %d residue"
          % (len(MUTATIONS), len(escapes), len(residue)))
    for e in escapes:
        print("  ESCAPE  %s" % e)
    for r in residue:
        print("  RESIDUE %s" % r)
    return 1 if (escapes or residue) else 0


if __name__ == "__main__":
    raise SystemExit(main())
