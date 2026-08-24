#!/usr/bin/env python3
"""Mutation suite for batch G3 - the third August 2026 fresh-intake production.

WHAT THIS SUITE ADDS OVER G2's
------------------------------
G1 proved the intake lane and G2 added the projection surfaces. G3 introduces
two claims neither of them made, so the mutations attack those directly::

    delete the freeze record            -> a batch that claims one must have one
    drop a produced ask from the freeze -> production must not outrun the freeze
    silently drop the held ask          -> a hold must be declared, not implied
    also produce the held ask           -> held and produced are exclusive
    flip an adjudication back           -> action_kind is DERIVED, not asserted

plus the standing claims every fresh-intake batch makes::

    name an examiner in a new card      -> attribution must stay earned
    leak production vocabulary          -> the candidate surface must stay clean
    corrupt a post-edit digest          -> the manifest must describe what shipped
    publish with no review record       -> review must be required
    un-ignore the raw carrier file      -> candidate names must not be committable
    create a FINAL workbook             -> the freeze gate must hold while open

WHY THE FREEZE MUTATIONS MATTER
-------------------------------
`freeze_record` is LOAD_BEARING and, until this batch, nothing read it. A field
no validator opens is decoration, and this repository has shipped decoration
before - a half-wired digest pin, and guards that pinned a corpus total and then
passed vacuously the moment the corpus grew. B, C and D exist so that the
freeze record cannot become the next one.

RESTORATION IS IN A `finally`
-----------------------------
A previous session killed a mutation suite on a foreground timeout and left a
deliberately-wrong content mutation live on a product page. Every mutation here
restores from a byte snapshot inside a `finally`, and the suite re-probes after
the run and reports residue explicitly.

  PYTHONIOENCODING=utf-8 python tools/oral/mutate_batch_g3.py
"""
from __future__ import annotations

import io
import json
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio      # noqa: E402

enable_utf8_stdio()

OUT = REPO / "meoclass1" / "oral-intelligence" / "examiner-audit"
ADJ = OUT / "AUGUST2026_INTAKE_ADJUDICATIONS.json"
FREEZE = OUT / "AUGUST2026_BATCH_G3_FREEZE.json"
REVIEW = OUT / "AUGUST2026_BATCH_G3_REVIEW.json"
MANIFEST = HERE / "batch_g3_manifest.json"
GITIGNORE = REPO / ".gitignore"

# The card this suite mutates for content probes. QB2_C#q5 is a G3 new card, so
# a content mutation here cannot be confused with pre-existing corpus state.
CARD_FILE = REPO / "meoclass1" / "QB2_C.html"
CARD_ANCHOR = "q5"

QBOOK = REPO / "docs" / "MIW-master-Question-bank"
SHARE = QBOOK / "MIW_August2026_QuestionBank_INTERIM.xlsx"
FAKE_FINAL = QBOOK / "MIW_August2026_QuestionBank_v27_FINAL.xlsx"

INTAKE = "validate_oral_intake.py"
G3 = "validate_batch_g3.py"


class Snapshot:
    """Byte snapshot restored by exact path. Never a git checkout: this suite
    runs against a dirty tree by definition, and `git checkout -- <file>` would
    discard the very edits under test."""

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


def _json(p):
    return json.loads(p.read_text(encoding="utf-8"))


def _write(p, d):
    p.write_bytes((json.dumps(d, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))


def _card_span(text, anchor):
    """(start, end) of the balanced q-card block for `anchor`."""
    open_re = re.compile(r'<div\b[^>]*\bclass="[^"]*\bq-card\b[^"]*"[^>]*>', re.I)
    for m in open_re.finditer(text):
        a = re.search(r'\bid="([^"]+)"', m.group(0))
        if not a or a.group(1) != anchor:
            continue
        depth = 0
        for t in re.finditer(r"<div\b[^>]*>|</div\s*>", text[m.start():], re.I):
            depth += -1 if t.group(0).startswith("</") else 1
            if depth == 0:
                return m.start(), m.start() + t.end()
    raise AssertionError("anchor %s not found" % anchor)


def _edit_card(insert):
    raw = CARD_FILE.read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in raw else "\n"
    t = raw.replace("\r\n", "\n")
    s, _e = _card_span(t, CARD_ANCHOR)
    marker = '<div class="answer-body">'
    at = t.index(marker, s) + len(marker)
    t = t[:at] + insert + t[at:]
    CARD_FILE.write_bytes((t.replace("\n", eol) if eol == "\r\n" else t).encode("utf-8"))


# ------------------------------------------------------------------ mutations
def m_delete_freeze_record():
    FREEZE.unlink()


def m_freeze_drops_a_produced_ask():
    d = _json(FREEZE)
    d["asks"] = [a for a in d["asks"] if a["occurrence_id"] != "AUG-0022"]
    _write(FREEZE, d)


def m_hold_becomes_silent():
    """Delete the held_actions declaration. AUG-0015 is then frozen, unproduced
    and undeclared - indistinguishable from work that was quietly dropped."""
    d = _json(MANIFEST)
    d.pop("held_actions", None)
    _write(MANIFEST, d)


def m_held_ask_also_produced():
    d = _json(MANIFEST)
    d["held_actions"][0]["followup_id"] = d["cards"][0]["action_id"]
    _write(MANIFEST, d)


def m_flip_adjudication_back():
    """Return AUG-0003 to GENUINE_NEW_QUESTION while the manifest says FOLLOWUP.
    action_kind is derived from the adjudication, never asserted by the batch."""
    d = _json(ADJ)
    for a in d["adjudications"]:
        if a["occurrence_id"] == "AUG-0003":
            a["classification"] = "GENUINE_NEW_QUESTION"
    _write(ADJ, d)


def m_corrupt_post_edit_digest():
    d = _json(MANIFEST)
    d["cards"][0]["post_edit_digest"] = "0" * 64
    _write(MANIFEST, d)


def m_remove_review():
    REVIEW.unlink()


def m_name_an_examiner():
    _edit_card("<p>Senthil asks this one every sitting.</p>")


def m_leak_production_vocabulary():
    _edit_card("<p>Source occurrence AUG-0022, GENUINE_NEW_QUESTION.</p>")


def m_unignore_raw_carrier():
    t = io.open(GITIGNORE, encoding="utf-8", newline="").read()
    io.open(GITIGNORE, "w", encoding="utf-8", newline="").write(
        t.replace("docs/MIW-master-Question-bank/**/*.txt",
                  "# docs/MIW-master-Question-bank/**/*.txt", 1))


def m_create_final_workbook():
    shutil.copyfile(SHARE, FAKE_FINAL)


MUTATIONS = [
    ("A", "delete the freeze record the manifest declares", [FREEZE],
     m_delete_freeze_record, (G3,), "g3_freeze_record_resolves"),
    ("B", "drop a PRODUCED ask from the freeze record", [FREEZE],
     m_freeze_drops_a_produced_ask, (G3,), "g3_every_produced_ask_was_frozen_first"),
    ("C", "silently drop the held ask instead of declaring it", [MANIFEST],
     m_hold_becomes_silent, (G3,), "g3_every_frozen_ask_is_produced_or_held"),
    ("D", "declare an action both held and produced", [MANIFEST],
     m_held_ask_also_produced, (G3,), "g3_manifest_schema_contract"),
    ("E", "flip an adjudication back under a manifest that disagrees", [ADJ],
     m_flip_adjudication_back, (G3,), "g3_action_kind_agrees_with_adjudication"),
    ("F", "corrupt a post-edit digest so the manifest misdescribes what shipped",
     [MANIFEST], m_corrupt_post_edit_digest, (G3,), "g3_post_edit_state_is_live"),
    ("G", "publish the batch with no review record", [REVIEW], m_remove_review,
     (G3,), "g3_review_record_present"),
    ("H", "name an examiner in a new card", [CARD_FILE], m_name_an_examiner,
     (G3,), "g3_new_cards_name_no_examiner"),
    ("I", "leak production vocabulary onto a candidate surface", [CARD_FILE],
     m_leak_production_vocabulary, (G3,), "g3_no_production_vocabulary_in_a_card"),
    ("J", "un-ignore the raw candidate carrier file", [GITIGNORE],
     m_unignore_raw_carrier, (INTAKE,), "P1_raw_carrier_files_are_git_ignored"),
    ("K", "create a FINAL August workbook while the intake window is open",
     [FAKE_FINAL], m_create_final_workbook, (INTAKE,),
     "Z1_no_final_august_workbook_while_intake_open"),
]

ALL_PROBES = (INTAKE, G3)


def probe(kind):
    rc, out = run(kind)
    return rc, failing_checks(out)


def main() -> int:
    if not MANIFEST.is_file():
        print("G3 manifest missing")
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
            after = {p: (p.read_bytes() if p.is_file() else None) for p in before}
            changed = any(before[p] != after[p] for p in before)
            delta = sum(len(after[p] or b"") - len(before[p] or b"") for p in before)
            print("%-3s %-58s %-7s byte_delta=%+d"
                  % (mid, desc, "applied" if changed else "NO-OP", delta))
            if not changed:
                no_ops.append(mid)
        except Exception as exc:                                   # noqa: BLE001
            print("%-3s ERROR %s: %s" % (mid, type(exc).__name__, exc))
            no_ops.append(mid)
        finally:
            bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2
    if no_ops:
        print("\npreflight FAILED - no bytes changed: %s" % ", ".join(no_ops))
        return 1

    print("\n--- control: unmutated state ---")
    baseline = {}
    for k in ALL_PROBES:
        rc, failing = probe(k)
        print("    %-26s exit=%d failing=%s" % (k, rc, sorted(failing) or "none"))
        baseline[k] = failing
        if failing:
            print("PRE-RUN: %s already failing; a mutation caught here proves nothing." % k)
            return 2

    print("\n--- mutations ---")
    escapes, residue = [], []
    for mid, desc, files, apply, probes, expect in MUTATIONS:
        snap = Snapshot(files)
        try:
            apply()
            new, rc = set(), 0
            for k in probes:
                rc, failing = probe(k)
                new |= (failing - baseline[k])
            caught = expect in new
            if not caught:
                escapes.append("%s (%s): expected %s, got %s"
                               % (mid, desc, expect, sorted(new) or "nothing"))
            print("%-3s %-58s %-8s exit=%d  %s"
                  % (mid, desc, "CAUGHT" if caught else "ESCAPED", rc,
                     expect if caught else (sorted(new) or "no failure")))
        finally:
            bad = snap.restore()
        if bad:
            residue.append("%s: %s" % (mid, bad))

    print("\n--- post-run: the tree must be green again ---")
    for k in ALL_PROBES:
        rc, failing = probe(k)
        print("    %-26s exit=%d failing=%s" % (k, rc, sorted(failing) or "none"))
        if failing:
            residue.append("%s still failing after restore: %s" % (k, sorted(failing)))

    print("\n%d mutations, %d escape(s), 0 no-op(s), %d residue"
          % (len(MUTATIONS), len(escapes), len(residue)))
    for e in escapes:
        print("  ESCAPE  %s" % e)
    for r in residue:
        print("  RESIDUE %s" % r)
    return 1 if (escapes or residue) else 0


if __name__ == "__main__":
    raise SystemExit(main())
