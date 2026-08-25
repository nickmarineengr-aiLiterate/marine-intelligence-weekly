#!/usr/bin/env python3
"""Mutation suite for batch G4 - the discharge of G3's held August ask.

WHAT THIS SUITE ADDS OVER G3's
------------------------------
G3's suite attacked the FREEZE contract, because G3 was the first batch to
carry one.  G4 is the first batch to carry a `discharges_hold`, so this suite
attacks that::

    delete discharges_hold          -> a discharge must be declared, not implied
    point it at a hold that is not  -> a discharge must name a REAL hold
    close the hold in G3's record   -> the holding record must be left intact
    unfreeze the discharged ask     -> production must not outrun the freeze

plus the standing claims every fresh-intake batch makes::

    flip the adjudication back      -> action_kind is DERIVED, not asserted
    retarget the enrichment         -> it must edit the card the record named
    corrupt a post-edit digest      -> the manifest must describe what shipped
    corrupt a pre-edit digest       -> the baseline claim must be true too
    publish with no review record   -> review must be required
    fail the review and ship anyway -> a PASS verdict must be required
    declare a non-zero examiner delta -> attribution must stay earned
    name a new examiner in the card -> the derived index must not be bypassed
    leak production vocabulary      -> the candidate surface must stay clean
    create a FINAL workbook         -> the freeze gate must hold while open

WHERE AN UNSUPPORTED EXAMINER RELATIONSHIP ACTUALLY COMES FROM
--------------------------------------------------------------
The shared contract's `new_cards_name_no_examiner` skips enrichments -- and
correctly, because an existing card may legitimately already name an examiner
from its own history, as QB2_F#q3 does for the PFOS limb.  That makes the guard
pass VACUOUSLY for a batch whose only action is an enrichment, so this suite
has to prove the property somewhere else.

The FIRST attempt was wrong, and its escape is worth keeping.  Mutation L
originally added the name "Senthil" to the enriched card's CE Oral Tip and
expected the derived examiner index to go red.  It did not, and neither did
`validate_card_examiner_divergence.py`.  The reason is a genuine safety
property rather than a missing guard: ce_tip-tier relationships are published
from `STRONG_CE_TIP_REVIEW_DECISIONS.json` through `review_approved_ce_tip()`,
not by scanning card prose, so **card markup cannot inject a relationship into
the index at all**.  Writing a name into a paid card is a content defect, and
it is a real one, but it is not the route by which the examiner universe grows.

So L now attacks the route that exists: it flips a HELD CE-tip review decision
to APPROVED, which is exactly how an unearned relationship would enter, and
requires the examiner index generator to refuse it.  An escape that disproves
a mutation's premise is worth more than a catch that confirms a wrong one.

RESTORATION IS FROM A BYTE SNAPSHOT, IN EVERY PATH
--------------------------------------------------
Never from git: `git checkout <ref> -- <file>` destroys uncommitted work.  A
previous session killed a mutation suite on a timeout and left a wrong content
mutation live on a paid page, so the suite re-probes after the run and reports
residue explicitly.

  PYTHONIOENCODING=utf-8 python tools/oral/mutate_batch_g4.py
"""

from __future__ import annotations

import json
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_bytes import read_text, write_text, enable_utf8_stdio   # noqa: E402

enable_utf8_stdio()

AUDIT = REPO / "meoclass1" / "oral-intelligence" / "examiner-audit"
MANIFEST = HERE / "batch_g4_manifest.json"
HOLDER = HERE / "batch_g3_manifest.json"
ADJ = AUDIT / "AUGUST2026_INTAKE_ADJUDICATIONS.json"
REVIEW = AUDIT / "AUGUST2026_BATCH_G4_REVIEW.json"
FREEZE = AUDIT / "AUGUST2026_BATCH_G3_FREEZE.json"
CARD_FILE = REPO / "meoclass1" / "QB2_F.html"
CE_TIP_REVIEW = AUDIT / "STRONG_CE_TIP_REVIEW_DECISIONS.json"
WORKBOOKS = REPO / "docs" / "MIW-master-Question-bank"
SHARE = WORKBOOKS / "MIW_August2026_QuestionBank_INTERIM.xlsx"
FAKE_FINAL = WORKBOOKS / "MIW_August2026_QuestionBank_FINAL.xlsx"

PROBES = {
    "g4": "validate_batch_g4.py",
    "intake": "validate_oral_intake.py",
    "examiner": None,          # build_examiner_index.py --check
}


def run_probe(key: str) -> tuple[int, set]:
    if key == "examiner":
        out = subprocess.run(
            [sys.executable, str(HERE / "build_examiner_index.py"), "--check"],
            cwd=str(REPO), capture_output=True, check=False)
        text = (out.stdout + out.stderr).decode("utf-8", "replace")
        failing = set()
        if "EXAMINER INDEX CHECK: PASS" not in text:
            failing.add("examiner_index_is_current")
        return out.returncode, failing
    out = subprocess.run([sys.executable, str(HERE / PROBES[key])],
                         cwd=str(REPO), capture_output=True, check=False)
    text = (out.stdout + out.stderr).decode("utf-8", "replace")
    failing = set(re.findall(r"^FAIL\s+(\S+)", text, re.M))
    for payload in re.findall(r"violations=\[([^\]]*)\]", text):
        failing.update(re.findall(r"'([^']+)'", payload))
    return out.returncode, failing


class Snapshot:
    def __init__(self, paths):
        self.data = {}
        for path in paths:
            p = pathlib.Path(path)
            self.data[p] = p.read_bytes() if p.is_file() else None

    def restore(self) -> list[str]:
        bad = []
        for path, blob in self.data.items():
            if blob is None:
                if path.is_file():
                    path.unlink()
                continue
            path.write_bytes(blob)
            if path.read_bytes() != blob:
                bad.append(str(path))
        return bad


def _json(p):
    return json.loads(read_text(p))


def _write(p, data):
    write_text(p, json.dumps(data, indent=1, ensure_ascii=False) + "\n")


def edit(target, mutate):
    def apply():
        data = _json(target)
        mutate(data)
        _write(target, data)
    return apply


def sub_in_card(old: str, new: str, count: int = 0):
    def apply():
        text = read_text(CARD_FILE)
        assert old in text, "mutation target absent: %r" % old[:70]
        write_text(CARD_FILE, text.replace(old, new) if count == 0
                   else text.replace(old, new, count))
    return apply


# ------------------------------------------------------------------ mutators

def m_discharge_becomes_silent(d):
    d.pop("discharges_hold", None)


def m_discharge_names_a_phantom_hold(d):
    d["discharges_hold"][0]["held_by_manifest"] = "batch_g1_manifest.json"


def m_hold_closed_in_the_holding_record(d):
    d["held_actions"][0]["status"] = "DISCHARGED"


def m_freeze_drops_the_discharged_ask(d):
    d["asks"] = [a for a in d["asks"] if a["occurrence_id"] != "AUG-0015"]


def m_flip_adjudication_back(d):
    for a in d["adjudications"]:
        if a["occurrence_id"] == "AUG-0015":
            a["classification"] = "GENUINE_NEW_QUESTION"


def m_retarget_the_enrichment(d):
    for a in d["adjudications"]:
        if a["occurrence_id"] == "AUG-0015":
            a["matched_question_id"] = "QB10_B#q1"


def m_corrupt_post_digest(d):
    d["cards"][0]["post_edit_digest"] = "0" * 64


def m_corrupt_pre_digest(d):
    d["cards"][0]["pre_edit_digest"] = "0" * 64


def m_review_fails_and_ships(d):
    d["cards"][0]["verdict"] = "FAIL_APPLICATION"


def m_publish_a_held_relationship(d):
    """Publish a relationship the CE-tip review deliberately held.

    RELA-NAIR-QB10_B-q7 was held HOLD_WEAK_ASSERTION because its tip is a
    conditional anticipation ("If Nair asks ...") rather than a record that he
    asked.  Approving it is precisely the shape of an unearned relationship:
    the wording never changes, only the decision about it does.
    """
    for row in d["decisions"]:
        if row["decision"].startswith("HOLD"):
            row["decision"] = "APPROVE_CE_TIP_RELATIONSHIP"
            row["candidate_tier"] = "ce_tip"
            return
    raise AssertionError("no held CE-tip decision to flip")


def m_nonzero_examiner_delta(d):
    d["examiner_relationship_delta"] = 1


def m_remove_review():
    REVIEW.unlink()


def m_create_final_workbook():
    shutil.copyfile(SHARE, FAKE_FINAL)


# ----------------------------------------------------------------- mutations
# (id, description, files touched, apply(), probe, the check it MUST break)

MUTATIONS = [
    ("A", "delete the discharge declaration - the hold closes silently",
     [MANIFEST], edit(MANIFEST, m_discharge_becomes_silent),
     "g4", "g4_discharge_declared"),

    ("B", "point the discharge at a manifest that never held this ask",
     [MANIFEST], edit(MANIFEST, m_discharge_names_a_phantom_hold),
     "g4", "g4_discharge_names_a_real_hold"),

    ("C", "close the hold by editing the record that declared it",
     [HOLDER], edit(HOLDER, m_hold_closed_in_the_holding_record),
     "g4", "g4_holding_record_left_intact"),

    ("D", "drop the discharged ask from the freeze that identified it",
     [FREEZE], edit(FREEZE, m_freeze_drops_the_discharged_ask),
     "g4", "g4_produced_ask_was_frozen_first"),

    ("E", "flip the adjudication back under a manifest that disagrees",
     [ADJ], edit(ADJ, m_flip_adjudication_back),
     "g4", "g4_action_kind_agrees_with_adjudication"),

    ("F", "retarget the enrichment to a card the record did not name",
     [ADJ], edit(ADJ, m_retarget_the_enrichment),
     "g4", "g4_enrichment_targets_the_card_the_record_named"),

    ("G", "corrupt the post-edit digest so the manifest misdescribes what shipped",
     [MANIFEST], edit(MANIFEST, m_corrupt_post_digest),
     "g4", "g4_post_edit_state_is_live"),

    ("H", "corrupt the pre-edit digest so the baseline claim is false",
     [MANIFEST], edit(MANIFEST, m_corrupt_pre_digest),
     "g4", "g4_pre_edit_state_is_as_declared"),

    ("I", "publish the batch with no review record",
     [REVIEW], m_remove_review,
     "g4", "g4_review_record_present"),

    ("J", "ship a card the independent review did not pass",
     [REVIEW], edit(REVIEW, m_review_fails_and_ships),
     "g4", "g4_every_card_passed_review"),

    ("K", "declare an examiner relationship delta this batch did not earn",
     [MANIFEST], edit(MANIFEST, m_nonzero_examiner_delta),
     "g4", "g4_examiner_relationship_delta_is_declared_zero"),

    ("L", "approve a HELD CE-tip relationship the review declined to publish",
     [CE_TIP_REVIEW], edit(CE_TIP_REVIEW, m_publish_a_held_relationship),
     "examiner", "examiner_index_is_current"),

    ("M", "leak production vocabulary onto the candidate surface",
     [CARD_FILE],
     sub_in_card('<div class="numbers-box"><h4>Key Numbers</h4>',
                 '<div class="numbers-box"><h4>Key Numbers</h4>'
                 'Source occurrence AUG-0015, GENUINE_NEW_QUESTION. '),
     "g4", "g4_no_production_vocabulary_in_a_card"),

    ("N", "create a FINAL August workbook while the intake window is open",
     [FAKE_FINAL], m_create_final_workbook,
     "intake", "Z1_no_final_august_workbook_while_intake_open"),
]


# ---------------------------------------------------------------------- main

def main() -> int:
    if not MANIFEST.is_file():
        print("G4 manifest missing")
        return 2
    if FAKE_FINAL.is_file():
        print("stale freeze-gate fixture on disk: %s" % FAKE_FINAL.name)
        return 2

    print("--- preflight: every mutation must change bytes ---")
    no_ops = []
    for mid, desc, files, apply, _p, _c in MUTATIONS:
        snap = Snapshot(files)
        before = dict(snap.data)
        try:
            apply()
        except Exception as exc:
            print("%-3s ERROR %s: %s" % (mid, type(exc).__name__, exc))
            no_ops.append(mid)
            snap.restore()
            continue
        after = {p: (p.read_bytes() if p.is_file() else None) for p in snap.data}
        changed = any(before[p] != after[p] for p in before)
        delta = sum(len(after[p] or b"") - len(before[p] or b"") for p in before)
        print("%-3s %-62s %-8s byte_delta=%+d"
              % (mid, desc, "applied" if changed else "NO-OP", delta))
        if not changed:
            no_ops.append(mid)
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2

    if no_ops:
        print("\npreflight FAILED -- these mutations change no bytes: %s"
              % ", ".join(no_ops))
        print("0 mutations, 0 escape(s), %d no-op(s), 0 crash(es)" % len(no_ops))
        return 1

    print("\n--- control: unmutated state ---")
    control_dirty = False
    for key in PROBES:
        rc, failing = run_probe(key)
        print("CTL %-10s exit=%d failing=%s" % (key, rc, sorted(failing) or "none"))
        if failing:
            control_dirty = True
    if control_dirty:
        print("CONTROL IS NOT GREEN -- every later 'catch' would be meaningless")
        return 1

    print("\n--- mutations ---")
    caught, escapes, crashes = 0, [], []
    for mid, desc, files, apply, probe, want in MUTATIONS:
        snap = Snapshot(files)
        try:
            apply()
            rc, failing = run_probe(probe)
        except Exception as exc:
            print("%-3s CRASH  %s: %s" % (mid, type(exc).__name__, exc))
            crashes.append(mid)
            snap.restore()
            continue
        hit = want in failing
        if hit:
            caught += 1
        else:
            escapes.append("%s (wanted %s, got %s)"
                           % (mid, want, sorted(failing) or "nothing"))
        print("%-3s %-62s %s  [%s]"
              % (mid, desc, "CAUGHT " if hit else "ESCAPED", want))
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2

    print("\n--- residue probe ---")
    residue = False
    for key in PROBES:
        rc, failing = run_probe(key)
        print("RES %-10s exit=%d failing=%s" % (key, rc, sorted(failing) or "none"))
        if failing:
            residue = True
    if FAKE_FINAL.is_file():
        print("RES fixture   %s STILL ON DISK" % FAKE_FINAL.name)
        residue = True

    print("\n%d caught of %d" % (caught, len(MUTATIONS)))
    print("%d mutations, %d escape(s), 0 no-op(s), %d crash(es)"
          % (len(MUTATIONS), len(escapes), len(crashes)))
    for line in escapes:
        print("  ESCAPE %s" % line)
    if residue:
        print("  RESIDUE: a probe is still red after restore")
    return 0 if (not escapes and not crashes and not residue) else 1


if __name__ == "__main__":
    raise SystemExit(main())
