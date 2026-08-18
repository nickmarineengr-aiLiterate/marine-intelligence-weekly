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


REL = "CURRENT_EXAMINER_RELATIONSHIPS.jsonl"
EV = "EXAMINER_EVIDENCE_LEDGER_V2.jsonl"
SRC = "ALL_SURVEYORS_SOURCE_RECORDS.jsonl"
RECON = "ORAL_788_RECONCILIATION.jsonl"
RESULTS = "PHASE2_VALIDATION_RESULTS.json"


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


CODE_MUTATIONS = [
    ("M10 remove the SAME_CORE admission floor", c_remove_same_core_floor),
    ("M11 collapse ME-GI / ME-GA tokenisation", c_collapse_me_gi_me_ga),
    ("M12 re-enable speculative spell repair", c_reenable_speculative_repair),
]


def run_controls(tools_dir):
    p = subprocess.run([sys.executable, str(tools_dir / "test_oral_controls.py")],
                       capture_output=True, text=True)
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
