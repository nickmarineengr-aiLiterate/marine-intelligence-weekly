"""Mutation harness for the Oral examiner intelligence gates.

A validator that passes everything proves nothing. Each mutation below breaks
one thing the reconciliation depends on; the gate that owns it must fail. A
mutation that escapes is a hole in the gate, not a curiosity.

  PYTHONIOENCODING=utf-8 python tools/oral/mutate_phase2.py

Data mutations perturb a committed artefact, run the validator, and restore the
artefact from an in-memory snapshot. Code mutations patch a throwaway copy of
tools/oral and run the committed controls against it, so what is proved is that
the controls in this repository catch the regression.

Portability: repo-relative throughout; the scratch copy goes to the platform
temp directory obtained at run time, never a hardcoded path.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402

OUT = L.OUT
TOOLS = Path(__file__).resolve().parent
ENV_NOTE = "PYTHONIOENCODING=utf-8"


# --------------------------------------------------------------------------
# data mutations - the validator must fail
# --------------------------------------------------------------------------
def _snapshot(names):
    return {n: (OUT / n).read_bytes() for n in names if (OUT / n).exists()}


def _restore(snap):
    for n, b in snap.items():
        (OUT / n).write_bytes(b)


def _jsonl(name):
    return [json.loads(l) for l in (OUT / name).open(encoding="utf-8")]


def _write_jsonl(name, rows):
    with (OUT / name).open("w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def _json(name):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def _write_json(name, obj):
    (OUT / name).write_text(
        json.dumps(obj, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8", newline="\n")


REL = "CURRENT_EXAMINER_RELATIONSHIPS.jsonl"
EV = "EXAMINER_EVIDENCE_LEDGER_V2.jsonl"
SRC = "ALL_SURVEYORS_SOURCE_RECORDS.jsonl"
RECON = "ORAL_788_RECONCILIATION.jsonl"
RESULTS = "PHASE2_VALIDATION_RESULTS.json"
NUNITS = "ORAL_NOTES_UNITS.jsonl"
NEV = "ORAL_NOTES_EXAMINER_EVIDENCE.jsonl"
NCOV = "ORAL_NOTES_COVERAGE.jsonl"
FIN = "FINAL_788_PRODUCTION_DISPOSITION.jsonl"
RELA = "RELEASE_A_CONNECTIONS.json"
P0B = "FINAL_P0_PRODUCTION_BATCH.json"


# Phase 2A-iii final package. These break the datasets a production session
# and the index generator will actually read, which is where a defect stops
# being a reporting error and becomes a wrong answer in front of a candidate.
def m_final_source_dropped():
    """A source occurrence vanishes from the final dataset."""
    rows = _jsonl(FIN)
    _write_jsonl(FIN, rows[1:])


def m_final_two_dispositions():
    """One occurrence carries two content dispositions."""
    rows = _jsonl(FIN)
    dup = dict(rows[0])
    dup["content_disposition"] = ("MISSING"
                                  if rows[0]["content_disposition"] != "MISSING"
                                  else "EXACT_MATCH")
    rows.append(dup)
    _write_jsonl(FIN, rows)


def m_release_inferred_only():
    """Release A admits a pair carried only by a topic inference."""
    o = _json(RELA)
    o["connections"][0]["strongest_evidence_tier"] = "TOPIC_INFERRED"
    o["connections"][0]["evidence_tiers"] = ["TOPIC_INFERRED"]
    _write_json(RELA, o)


def m_release_same_core_only():
    """An external Release-A pair whose only source row is SAME_CORE.

    The pair keeps a healthy-looking tier and a resolving target; the only
    thing wrong with it is that nothing behind it is an EXACT or NEAR row.
    """
    fin = {r["source_id"]: r for r in _jsonl(FIN)}
    same_core = sorted(sid for sid, r in fin.items()
                       if r["content_disposition"] == "SAME_CORE_ASK")
    o = _json(RELA)
    for c in o["connections"]:
        if c["strongest_evidence_tier"] == "EXTERNAL_SOURCE_CONFIRMED":
            c["source_occurrence_ids"] = [same_core[0]]
            break
    _write_json(RELA, o)


def m_release_broken_anchor():
    """A Release-A target anchor that does not exist on its page."""
    o = _json(RELA)
    c = o["connections"][0]
    c["anchor"] = "q99999"
    c["canonical_question_id"] = c["canonical_question_id"].rsplit("#", 1)[0] \
        + "#q99999"
    _write_json(RELA, o)


def m_p0_duplicate_family():
    """Two P0 items claiming the same production family."""
    o = _json(P0B)
    dup = dict(o["items"][0])
    dup["production_id"] = dup["production_id"] + "-DUP"
    o["items"].append(dup)
    o["p0_count"] = len(o["items"])
    _write_json(P0B, o)


def m_promotion_relabelled_new_answer():
    """A MISSING ask over complete Notes relabelled as a new answer.

    The GIRDING fixture is the deterministic case: MIW holds a dedicated Notes
    section for it, so calling it research-from-zero would send a production
    session to write material it already has.
    """
    rows = _jsonl(FIN)
    for r in rows:
        if (r["content_disposition"] == "MISSING"
                and r["notes_support"] in ("NOTES_COMPLETE_SUPPORT",
                                           "NOTES_STRONG_SUPPORT")):
            r["production_action"] = "NEW_ANSWER_REQUIRED"
            break
    _write_jsonl(FIN, rows)


def m_wrong_anchor():
    rows = _jsonl(REL)
    rows[0]["target_anchor"] = "q99999"
    rows[0]["question_id"] = rows[0]["question_id"].rsplit("#", 1)[0] + "#q99999"
    _write_jsonl(REL, rows)


def m_duplicate_relation():
    rows = _jsonl(REL)
    rows.append(dict(rows[0]))
    _write_jsonl(REL, rows)


def m_orphan_evidence():
    rows = _jsonl(EV)
    rows[0]["relationship_id"] = "REL-DOES-NOT-EXIST"
    _write_jsonl(EV, rows)


def m_unknown_examiner():
    rows = _jsonl(REL)
    rows[0]["examiner"] = "Captain Nemo"
    _write_jsonl(REL, rows)


def m_derived_promoted_to_primary():
    """M5 - the Laptop escape. A CURRENT_INDEX_RECOVERY record, which the
    ledger itself annotates 'Not independent evidence', relabelled as the
    primary tracker."""
    rows = _jsonl(EV)
    for r in rows:
        if r.get("source_type") == "CURRENT_INDEX_RECOVERY":
            r["evidence_tier"] = "PRIMARY_TRACKER"
            break
    _write_jsonl(EV, rows)


def m_july_sibling_promoted():
    rows = _jsonl(EV)
    rows[0]["source_type"] = "JULY_DERIVED_SIBLING"
    rows[0]["evidence_tier"] = "PRIMARY_TRACKER"
    _write_jsonl(EV, rows)


def m_topic_inferred_promoted():
    rows = _jsonl(EV)
    rows[0]["source_type"] = "TOPIC_INFERRED"
    rows[0]["evidence_tier"] = "PRIMARY_TRACKER"
    _write_jsonl(EV, rows)


def m_ce_tip_promoted():
    rows = _jsonl(EV)
    rows[0]["source_type"] = "CE_TIP"
    rows[0]["evidence_tier"] = "PRIMARY_TRACKER"
    _write_jsonl(EV, rows)


def m_note_explicit_promoted():
    """M13 - prepares the gate for Phase 2A-ii: an explicit examiner cue found
    in an Oral Note is real evidence, but it is not the tracker."""
    rows = _jsonl(EV)
    rows[0]["source_type"] = "NOTE_EXPLICIT"
    rows[0]["evidence_tier"] = "PRIMARY_TRACKER"
    _write_jsonl(EV, rows)


def m_dropped_source():
    rows = _jsonl(SRC)
    _write_jsonl(SRC, rows[:-1])


def m_two_dispositions():
    rows = _jsonl(RECON)
    rows.append(dict(rows[0]))
    _write_jsonl(RECON, rows)


def m_missing_disposition():
    rows = _jsonl(RECON)
    _write_jsonl(RECON, rows[:-1])


def m_invalid_tier():
    rows = _jsonl(RECON)
    rows[0]["evidence_tier"] = "TOTALLY_CONFIRMED"
    _write_jsonl(RECON, rows)



def m_note_evidence_promoted():
    """M15 - an explicit examiner cue found in an Oral Note relabelled as the
    primary tracker. A Note is a Note: it is real evidence of what a note says,
    and it is never the tracker."""
    rows = _jsonl(NEV)
    rows[0]["evidence_tier"] = "PRIMARY_TRACKER"
    _write_jsonl(NEV, rows)


def m_note_unit_missing_file():
    """M17 - a note unit that points at a page or an anchor which does not
    exist. An unresolvable citation is worse than no citation."""
    rows = _jsonl(NUNITS)
    rows[0]["file"] = "simon-notes-p99.html"
    _write_jsonl(NUNITS, rows)


def m_note_unit_missing_anchor():
    """M17b - the file exists but the section the parser claims does not."""
    rows = _jsonl(NUNITS)
    for r in rows:
        if r.get("anchor_authored"):
            r["anchor"] = "does-not-exist-9999"
            break
    _write_jsonl(NUNITS, rows)


def m_note_unit_as_canonical_question():
    """M18 - a note unit injected into the canonical namespace. The Notes are a
    secondary layer; they may never create a canonical QB question id."""
    rows = _jsonl(NUNITS)
    recon = _jsonl(RECON)
    victim = next(r["matched_question_id"] for r in recon
                  if r.get("matched_question_id"))
    rows[0]["note_unit_id"] = victim
    _write_jsonl(NUNITS, rows)


def m_note_support_without_unit():
    """M14b - a Notes support claim with nothing under it. The data-side twin
    of M14: support asserted with no section to trace it to."""
    rows = _jsonl(NCOV)
    for r in rows:
        if r["notes_support"] != "NO_NOTES_SUPPORT":
            r["notes_units"] = []
            break
    _write_jsonl(NCOV, rows)


def m_note_support_uses_canonical_word():
    """M14c - Notes support relabelled with a canonical disposition, collapsing
    the two dimensions the phase exists to keep apart."""
    rows = _jsonl(NCOV)
    rows[0]["notes_support"] = "EXACT_MATCH"
    _write_jsonl(NCOV, rows)


DATA_MUTATIONS = [
    ("M1  wrong question anchor", [REL], m_wrong_anchor),
    ("M2  duplicate relationship", [REL], m_duplicate_relation),
    ("M3  orphan evidence record", [EV], m_orphan_evidence),
    ("M4  unknown examiner alias", [REL], m_unknown_examiner),
    ("M5  derived index record -> PRIMARY_TRACKER", [EV],
     m_derived_promoted_to_primary),
    ("M6  source occurrence silently dropped", [SRC], m_dropped_source),
    ("M7  two dispositions for one occurrence", [RECON], m_two_dispositions),
    ("M8  missing disposition", [RECON], m_missing_disposition),
    ("M9  invalid evidence tier", [RECON], m_invalid_tier),
    ("M5a JULY_DERIVED_SIBLING -> PRIMARY_TRACKER", [EV], m_july_sibling_promoted),
    ("M5b TOPIC_INFERRED -> PRIMARY_TRACKER", [EV], m_topic_inferred_promoted),
    ("M5c CE_TIP -> PRIMARY_TRACKER", [EV], m_ce_tip_promoted),
    ("M13 NOTE_EXPLICIT -> PRIMARY_TRACKER", [EV], m_note_explicit_promoted),
    ("M15 note cue -> PRIMARY_TRACKER", [NEV], m_note_evidence_promoted),
    ("M17 note unit points at a missing page", [NUNITS],
     m_note_unit_missing_file),
    ("M17b note unit points at a missing section", [NUNITS],
     m_note_unit_missing_anchor),
    ("M18 note unit injected as a canonical question", [NUNITS],
     m_note_unit_as_canonical_question),
    ("M14b Notes support with no supporting unit", [NCOV],
     m_note_support_without_unit),
    ("M14c Notes support relabelled as a canonical disposition", [NCOV],
     m_note_support_uses_canonical_word),
    ("M20 final dataset drops a source occurrence", [FIN],
     m_final_source_dropped),
    ("M21 final dataset gives one occurrence two dispositions", [FIN],
     m_final_two_dispositions),
    ("M22 Release A admits an inferred-only pair", [RELA],
     m_release_inferred_only),
    ("M23 Release A admits a SAME_CORE-only external pair", [RELA],
     m_release_same_core_only),
    ("M24 Release A target anchor broken", [RELA], m_release_broken_anchor),
    ("M25 duplicate P0 production family", [P0B], m_p0_duplicate_family),
    ("M26 Notes promotion relabelled as a new answer", [FIN],
     m_promotion_relabelled_new_answer),
]


def run_validator(cwd=None):
    p = subprocess.run([sys.executable, str(TOOLS / "validate_phase2.py")],
                       capture_output=True, text=True, cwd=cwd or str(L.REPO))
    return p.returncode, (p.stdout or "") + (p.stderr or "")


# --------------------------------------------------------------------------
# code mutations - the controls must fail
# --------------------------------------------------------------------------
def c_remove_same_core_floor(files):
    """M10 - strip the SAME_CORE admission floor back to 'always admit', the
    Phase 2 behaviour."""
    p = files / "reconcile_788.py"
    s = p.read_text(encoding="utf-8")
    s = s.replace('''    if conflict:
        return False, "contradictory technical designator"''',
                  "    return True, \"\"\n    if conflict:\n"
                  "        return False, \"contradictory technical designator\"")
    p.write_text(s, encoding="utf-8", newline="\n")


def c_collapse_me_gi_me_ga(files):
    """M11 - restore the tokeniser that required a digit, so letter-suffix
    designators die and ME-GI and ME-GA both reduce to nothing."""
    p = files / "oral_text.py"
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"^def designators\(s\):",
               "def designators(s):\n    return set()", s, count=1,
               flags=re.M)
    p.write_text(s, encoding="utf-8", newline="\n")


def c_reenable_speculative_repair(files):
    """M12 - put the nearest-corpus-token repairer back: any token of five or
    more characters is 'corrected' towards the QB vocabulary."""
    p = files / "oral_text.py"
    s = p.read_text(encoding="utf-8")
    s = s.replace('''def repair(tok):
    """Return (token, note). A token is repaired only when it is a curated,
    verified source misspelling AND is not load-bearing."""
    if is_load_bearing(tok):
        return tok, None''',
                  '''_SPECULATIVE = {"attended": "unattended", "convinced": "convicted",
                "provident": "provide", "and92": "and9",
                "stcw5": "stcw15", "iii16": "iii6"}


def repair(tok):
    """Return (token, note)."""
    if tok in _SPECULATIVE:
        return _SPECULATIVE[tok], "%s->%s" % (tok, _SPECULATIVE[tok])''')
    p.write_text(s, encoding="utf-8", newline="\n")



def c_drop_notes_coverage(files):
    """M14 - delete the Notes coverage layer. The load-bearing Notes fixtures
    (GIRDING above all) must break immediately: if they do not, the layer is
    not actually carrying the result it claims to carry."""
    p = files / "notes_coverage.py"
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"^def best_support\(src_toks, idx, idf, default, limit=5\):",
               "def best_support(src_toks, idx, idf, default, limit=5):\n"
               "    return []", s, count=1, flags=re.M)
    p.write_text(s, encoding="utf-8", newline="\n")


def c_disable_non_examiner_controls(files):
    """M16 - turn off the non-examiner name controls, so John the legal
    example, John the author and John the ship all become John the examiner."""
    p = files / "oral_notes.py"
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"^def _non_examiner\(text, start, end, name\):",
               "def _non_examiner(text, start, end, name):\n    return None",
               s, count=1, flags=re.M)
    p.write_text(s, encoding="utf-8", newline="\n")


def c_page_level_notes_matching(files):
    """M14d - score the whole PAGE instead of the section. This is the failure
    mode the section-level model exists to prevent: a 116 KB page mentions
    everything, so every ask put to it finds support."""
    p = files / "oral_notes.py"
    s = p.read_text(encoding="utf-8")
    s = s.replace('                    "text": u.get("body", ""),',
                  '                    "text": page_text('
                  '(NOTES_DIR / fname).read_text('
                  'encoding="utf-8", errors="replace")),')
    p.write_text(s, encoding="utf-8", newline="\n")


def c_family_head_cancels_conflict(files):
    """M19 - restore the defective conflict cancellation: re-admit the bare
    family head as though it were a member. In mixed-case prose "ME-GI" emits
    `dsg:me` beside `dsg:me-gi`, so both sides regain the pseudo-value "me",
    it intersects, and the real GI/GA disagreement cancels. The full-sentence
    controls must fail; the bare-designator ones will not notice, which is
    precisely why the sentence controls exist."""
    p = files / "oral_text.py"
    s = p.read_text(encoding="utf-8")
    s = s.replace("            if val == key:\n"
                  "                continue          "
                  "# the family named, no member named\n", "")
    p.write_text(s, encoding="utf-8", newline="\n")


CODE_MUTATIONS = [
    ("M10 remove the SAME_CORE admission floor", c_remove_same_core_floor),
    ("M19 a shared family head cancels a specific conflict",
     c_family_head_cancels_conflict),
    ("M11 collapse ME-GI / ME-GA tokenisation", c_collapse_me_gi_me_ga),
    ("M12 re-enable speculative spell repair", c_reenable_speculative_repair),
    ("M14 drop the Notes coverage layer", c_drop_notes_coverage),
    ("M14d match Notes at page level, not section level",
     c_page_level_notes_matching),
    ("M16 disable the non-examiner name controls",
     c_disable_non_examiner_controls),
]


def run_controls(tools_dir):
    # The scratch copy holds mutated CODE and must read the repository's real
    # DATA, so the controls fail on the regression rather than on a missing
    # file. ORAL_REPO_ROOT states the root explicitly; nothing is hardcoded.
    env = dict(os.environ, ORAL_REPO_ROOT=str(L.REPO), PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, str(tools_dir / "test_oral_controls.py")],
                       capture_output=True, text=True, env=env)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


# --------------------------------------------------------------------------
def main():
    rows = []

    for name, touched, apply in DATA_MUTATIONS:
        snap = _snapshot(list(touched) + [RESULTS])
        try:
            apply()
            code, out = run_validator()
        finally:
            _restore(snap)
        caught = code != 0
        detail = "exit %d" % code
        m = re.search(r"(\d+) PASS / (\d+) FAIL", out)
        if m:
            detail = "%s PASS / %s FAIL" % (m.group(1), m.group(2))
        elif code != 0:
            detail = "validator exited %d (fails closed)" % code
        rows.append((name, caught, detail))

    scratch = Path(tempfile.mkdtemp(prefix="oral-mutate-"))
    try:
        for name, apply in CODE_MUTATIONS:
            work = scratch / re.sub(r"\W+", "_", name)
            shutil.copytree(TOOLS, work,
                            ignore=shutil.ignore_patterns("__pycache__"))
            apply(work)
            code, out = run_controls(work)
            m = re.search(r"(\d+) controls / (\d+) failures", out)
            detail = ("%s controls / %s failures" % (m.group(1), m.group(2))
                      if m else "exit %d" % code)
            rows.append((name, code != 0, detail))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    escapes = [n for n, caught, _ in rows if not caught]
    for name, caught, detail in rows:
        print("%-8s %-46s %s" % ("caught" if caught else "ESCAPED",
                                 name, detail))
    print("\n%d mutations / %d escapes" % (len(rows), len(escapes)))

    # the harness must leave the tree exactly as it found it
    code, _ = run_validator()
    print("post-run validator exit %d" % code)
    return 1 if (escapes or code != 0) else 0


if __name__ == "__main__":
    sys.exit(main())
