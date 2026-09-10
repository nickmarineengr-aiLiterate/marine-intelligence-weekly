"""Controls for the follow-up register closure derivation.

Every control here exists because closing a governed register row is
authority-bearing evidence. A writer that closes the wrong row, or closes a row
on a judgement it is not entitled to make, is worse than a register that
over-reports.

  PYTHONIOENCODING=utf-8 python tools/oral/test_followup_closure.py

Exit 0 when every control holds. Repo-relative, no network, no external input,
and no mutation of any tracked file: every fixture is built in a temp dir.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import followup_closure as FC  # noqa: E402

FAILURES = []
CHECKS = [0]


def check(name, ok, detail=""):
    CHECKS[0] += 1
    if not ok:
        FAILURES.append("%s -- %s" % (name, detail))
        print("FAIL %-58s %s" % (name, detail))
    else:
        print("ok   %-58s %s" % (name, detail))


# --------------------------------------------------------------------------
# fixtures
# --------------------------------------------------------------------------
def action(fid, page, anchor):
    return {"followup_id": fid, "parent_file": page, "parent_anchor": anchor,
            "status": FC.NOT_STARTED, "batch": None}


ACTIONS = [
    action("FUP-001", "QB10_B.html", "q1"),
    action("FUP-003", "QB1_A.html", "q3"),
    action("FUP-006", "QB1_A.html", "q9"),
    action("FUP-018", "QB3_I.html", "q4"),
]


def manifest(tmp, batch_id, cards=(), held=(), discharges=(),
             authorisation_source=FC.REGISTER_REL, name=None):
    data = {"batch_id": batch_id, "authorisation_source": authorisation_source,
            "cards": list(cards)}
    if held:
        data["held_actions"] = list(held)
    if discharges:
        data["discharges_hold"] = list(discharges)
    path = Path(tmp) / (name or ("batch_%s_manifest.json" % batch_id.lower()))
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path, data


def derive_in(tmp):
    return FC.derive(ACTIONS, FC.discover_manifests(tmp))


# ===========================================================================
print("\n--- 1. a produced action closes, and closes to the right row ---")
# ===========================================================================
with tempfile.TemporaryDirectory() as tmp:
    manifest(tmp, "F1", cards=[{"followup_id": "FUP-018",
                                "file": "QB3_I.html", "anchor": "q4"}])
    closure, exc = derive_in(tmp)
    check("a card's followup_id closes that action",
          closure.get("FUP-018", {}).get("status") == FC.PRODUCED,
          "FUP-018 -> PRODUCED")
    check("the closure names the batch that implemented it",
          closure["FUP-018"]["batch"] == "F1", "batch=F1")
    check("the closure carries its own evidence pointer",
          closure["FUP-018"]["production_evidence"]["card_index"] == 0
          and closure["FUP-018"]["production_evidence"]["target"] == "QB3_I.html#q4",
          "manifest + card index + target")
    check("no exception is raised for a clean closure", exc == [], "0 exceptions")


# ===========================================================================
print("\n--- 2. a wrong-but-valid identifier is refused ---")
# ===========================================================================
with tempfile.TemporaryDirectory() as tmp:
    # FUP-018's real parent is QB3_I#q4. This manifest resolves the id fine and
    # points it at a card that belongs to another action.
    manifest(tmp, "FX", cards=[{"followup_id": "FUP-018",
                                "file": "QB1_A.html", "anchor": "q9"}])
    closure, exc = derive_in(tmp)
    check("an id that resolves to the WRONG record does not close",
          "FUP-018" not in closure, "round trip failed -> no closure")
    check("the round-trip failure is reported by name",
          len(exc) == 1 and exc[0]["kind"] == "TARGET_ROUND_TRIP_FAILED",
          exc[0]["kind"] if exc else "no exception")
    check("the round-trip failure goes to Founder review",
          exc[0]["disposition"] == "NEEDS_FOUNDER_REVIEW", "")


# ===========================================================================
print("\n--- 3. an id the register does not hold fails visibly ---")
# ===========================================================================
with tempfile.TemporaryDirectory() as tmp:
    manifest(tmp, "FZ", cards=[{"followup_id": "FUP-036",
                                "file": "QB1_A.html", "anchor": "q9"}])
    closure, exc = derive_in(tmp)
    check("an unknown action shape fails visibly",
          len(exc) == 1 and exc[0]["kind"] == "UNKNOWN_ACTION",
          "FUP-036 is not a register row")
    check("an unknown action closes nothing", closure == {}, "")


# ===========================================================================
print("\n--- 4. prose is not evidence ---")
# ===========================================================================
with tempfile.TemporaryDirectory() as tmp:
    # This is the real shape of batch_f1_manifest.json: it names FUP-003 in a
    # note about colocated actions and implements only FUP-018.
    path, _ = manifest(tmp, "F1", cards=[{"followup_id": "FUP-018",
                                          "file": "QB3_I.html", "anchor": "q4"}])
    data = json.loads(path.read_text(encoding="utf-8"))
    data["note"] = ("Eight of the 35 register actions are colocated on "
                    "enriched cards (FUP-003, 006, 008, 009, 013, 017, 025, "
                    "034), so this is a structural gap.")
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    closure, exc = derive_in(tmp)
    check("an action named only in prose is not closed",
          "FUP-003" not in closure and "FUP-006" not in closure,
          "grep would have closed both")
    check("the action the manifest actually implements is still closed",
          closure["FUP-018"]["status"] == FC.PRODUCED, "")


# ===========================================================================
print("\n--- 5. a manifest that does not declare the register is ignored ---")
# ===========================================================================
with tempfile.TemporaryDirectory() as tmp:
    manifest(tmp, "E1", cards=[{"followup_id": "FUP-018",
                                "file": "QB3_I.html", "anchor": "q4"}],
             authorisation_source="tools/oral/some_other_consolidation.json")
    closure, exc = derive_in(tmp)
    check("a manifest authorised elsewhere cannot close a register row",
          closure == {} and exc == [], "not an authorisation record for this register")


# ===========================================================================
print("\n--- 6. a hold does not close, and does not move the register ---")
# ===========================================================================
with tempfile.TemporaryDirectory() as tmp:
    manifest(tmp, "F1",
             cards=[{"followup_id": "FUP-018", "file": "QB3_I.html",
                     "anchor": "q4"}],
             held=[{"followup_id": "FUP-006", "status": "HELD_GOVERNANCE",
                    "target": "QB1_A.html#q9",
                    "register_status_unchanged": FC.NOT_STARTED}])
    closure, exc = derive_in(tmp)
    check("a held action is not closed",
          closure["FUP-006"]["status"] == FC.NOT_STARTED, "stays open")
    check("the hold is recorded rather than discarded",
          closure["FUP-006"]["holds"][0]["batch_id"] == "F1",
          "held by F1, undischarged")
    check("an undischarged hold names no discharging batch",
          closure["FUP-006"]["holds"][0]["discharged_by_batch_id"] is None, "")

with tempfile.TemporaryDirectory() as tmp:
    manifest(tmp, "F1", held=[{"followup_id": "FUP-006",
                               "status": "HELD_GOVERNANCE",
                               "register_status_unchanged": "PRODUCED"}])
    closure, exc = derive_in(tmp)
    check("a hold claiming it moved the register is refused",
          len(exc) == 1 and exc[0]["kind"] == "HOLD_CLAIMS_STATUS_CHANGE",
          "a batch may not close a row it held")


# ===========================================================================
print("\n--- 7. a supersession requires real successor evidence ---")
# ===========================================================================
with tempfile.TemporaryDirectory() as tmp:
    manifest(tmp, "F1", held=[{"followup_id": "FUP-006",
                               "status": "HELD_GOVERNANCE",
                               "register_status_unchanged": FC.NOT_STARTED}])
    manifest(tmp, "F1b", cards=[{"followup_id": "FUP-006",
                                 "file": "QB1_A.html", "anchor": "q9"}],
             discharges=[{"followup_id": "FUP-006",
                          "held_by_manifest": "batch_f1_manifest.json"}])
    closure, exc = derive_in(tmp)
    check("a discharged hold closes through the discharging batch",
          closure["FUP-006"]["status"] == FC.PRODUCED
          and closure["FUP-006"]["batch"] == "F1b", "F1 held, F1b produced")
    check("the earlier hold is preserved, not erased",
          closure["FUP-006"]["holds"][0]["batch_id"] == "F1"
          and closure["FUP-006"]["holds"][0]["discharged_by_batch_id"] == "F1b",
          "F1's record stays historically true")

with tempfile.TemporaryDirectory() as tmp:
    manifest(tmp, "F1", held=[{"followup_id": "FUP-006",
                               "status": "HELD_GOVERNANCE",
                               "register_status_unchanged": FC.NOT_STARTED}])
    manifest(tmp, "F1b", discharges=[{"followup_id": "FUP-006"}])
    closure, exc = derive_in(tmp)
    check("a discharge that implements nothing is refused",
          len(exc) == 1 and exc[0]["kind"] == "DISCHARGE_WITHOUT_PRODUCTION",
          "declaring a hold discharged is not producing the work")


# ===========================================================================
print("\n--- 8. two batches claiming the same action is a judgement ---")
# ===========================================================================
with tempfile.TemporaryDirectory() as tmp:
    manifest(tmp, "F1", cards=[{"followup_id": "FUP-018",
                                "file": "QB3_I.html", "anchor": "q4"}])
    manifest(tmp, "F2", cards=[{"followup_id": "FUP-018",
                                "file": "QB3_I.html", "anchor": "q4"}])
    closure, exc = derive_in(tmp)
    check("a doubly-produced action is refused, not silently re-pointed",
          len(exc) == 1 and exc[0]["kind"] == "DOUBLE_PRODUCTION",
          "which record is the implementation is a judgement")
    check("a refused action keeps no partial closure",
          "FUP-018" not in closure, "")


# ===========================================================================
print("\n--- 9. determinism and idempotence ---")
# ===========================================================================
with tempfile.TemporaryDirectory() as tmp:
    manifest(tmp, "F1", cards=[{"followup_id": "FUP-018",
                                "file": "QB3_I.html", "anchor": "q4"}])
    manifest(tmp, "F1b", cards=[{"followup_id": "FUP-006",
                                 "file": "QB1_A.html", "anchor": "q9"}])
    first = json.dumps(derive_in(tmp)[0], sort_keys=True)
    second = json.dumps(derive_in(tmp)[0], sort_keys=True)
    check("the same input yields the same proposed changes",
          first == second, "byte-identical derivation")

    # Feed the derived state back in as if the register already carried it.
    settled = [dict(a) for a in ACTIONS]
    closure, _ = derive_in(tmp)
    for a in settled:
        d = closure.get(a["followup_id"])
        if d:
            a["status"], a["batch"] = d["status"], d["batch"]
    again, _ = FC.derive(settled, FC.discover_manifests(tmp))
    check("closing an already-closed action changes nothing",
          json.dumps(again, sort_keys=True) == first, "idempotent")


# ===========================================================================
print("\n--- 10. an exception refuses the whole generation ---")
# ===========================================================================
with tempfile.TemporaryDirectory() as tmp:
    manifest(tmp, "FZ", cards=[{"followup_id": "FUP-036",
                                "file": "QB1_A.html", "anchor": "q9"}])
    try:
        FC.closure_for_register(ACTIONS, tmp)
        raised = False
    except FC.ClosureException:
        raised = True
    check("the generator refuses a partial derivation",
          raised, "no register is written while an exception stands")


# ===========================================================================
print("\n--- 11. the CLI writes nothing on --dry-run ---")
# ===========================================================================
before = FC.sha256_of(FC.REGISTER)
proc = subprocess.run([sys.executable, str(HERE / "followup_closure.py"),
                       "--dry-run"], cwd=str(REPO), capture_output=True,
                      text=True)
after = FC.sha256_of(FC.REGISTER)
check("--dry-run leaves the register byte-identical", before == after,
      "sha256 unchanged")
check("--dry-run exits clean when no exception stands", proc.returncode == 0,
      "exit %d" % proc.returncode)
check("--dry-run states the sha it inspected", before[:16] in proc.stdout,
      "the packet names the bytes it read")


# ===========================================================================
print("\n--- 12. the live register agrees with the live artefacts ---")
# ===========================================================================
live = json.loads(FC.REGISTER.read_text(encoding="utf-8"))
live_closure, live_exc = FC.derive(live["actions"], FC.discover_manifests())
check("no live closure exception stands", live_exc == [],
      "%d exception(s)" % len(live_exc))
drift = [a["followup_id"] for a in live["actions"]
         if (a.get("status"), a.get("batch")) != (
             live_closure.get(a["followup_id"], FC._blank(a["followup_id"]))["status"],
             live_closure.get(a["followup_id"], FC._blank(a["followup_id"]))["batch"])]
check("the committed register carries no status drift", drift == [],
      "drifted: %s" % (", ".join(drift) or "none"))
check("every PRODUCED row names a manifest that exists",
      all((REPO / a["production_evidence"]["manifest"]).exists()
          for a in live["actions"] if a.get("production_evidence")),
      "evidence pointers resolve")


# ===========================================================================
print("\n%d checks, %d FAIL" % (CHECKS[0], len(FAILURES)))
for f in FAILURES:
    print("  FAIL %s" % f)
sys.exit(1 if FAILURES else 0)
