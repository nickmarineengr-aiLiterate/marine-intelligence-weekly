#!/usr/bin/env python3
"""Derive the IMPLEMENTATION state of each follow-up action from batch manifests.

WHY THIS EXISTS
---------------
`oral_followup_register.json` hardcoded `status: AUTHORISED_NOT_STARTED` and
`batch: null` on all 35 actions, and kept saying so after F1 produced FUP-018
and FUP-033 and F1b produced FUP-006. The register therefore over-reported the
remaining workload by three actions. The `status` vocabulary already contained
`PRODUCED`; nothing ever wrote it.

WHAT THIS IS NOT
----------------
It is not a hand-editable status board and it does not decide whether work is
substantively complete. It reads what the production batches already recorded
and re-expresses it in the field the register reserved for it. Nothing here
authors content, adjudicates a target, or closes a Founder judgement.

THE BINDING RULE (why a grep is not evidence)
---------------------------------------------
A manifest closes register rows only when it *declares* the register as its
`authorisation_source`, and only through `cards[].followup_id` — never through
prose. `batch_f1_manifest.json` mentions `FUP-003`, `FUP-008`, `FUP-009`,
`FUP-013`, `FUP-017`, `FUP-025` and `FUP-034` in a note explaining which
actions sit on enriched cards. A grep-driven writer would close seven actions
that were never produced. `batch_f1b_manifest.json` likewise names FUP-018 and
FUP-033 in prose about F1.

THE ROUND-TRIP INVARIANT
------------------------
An identifier can be syntactically valid and resolve successfully while
pointing at the wrong record. So every claimed closure must round-trip:

    followup_id -> the register action -> its parent_file#parent_anchor
                -> the manifest card's own file/anchor

A mismatch is an exception, never a closure.

STATES THAT ARE NEVER DERIVED
-----------------------------
`IN_BATCH` and `WITHDRAWN` are in the register vocabulary and stay unwritten:
no committed artefact expresses either. Inventing a source for them would be
the same defect this module exists to close.

Usage:
    python tools/oral/followup_closure.py --audit     # register vs artefacts
    python tools/oral/followup_closure.py --dry-run   # proposed changes, no write
    python tools/oral/followup_closure.py --apply     # regenerate the register
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

REGISTER_REL = "tools/oral/oral_followup_register.json"
REGISTER = REPO / "tools" / "oral" / "oral_followup_register.json"
GENERATOR = "tools/oral/build_followup_register.py"

# The only status a derivation may write. AUTHORISED_NOT_STARTED is the
# generator's default; PRODUCED is the single mechanical transition.
PRODUCED = "PRODUCED"
NOT_STARTED = "AUTHORISED_NOT_STARTED"

# A manifest that holds an action must say what it left the register saying.
# F1 records this explicitly; a manifest claiming a hold changed the register
# is asserting something no batch is allowed to do.
HOLD_DECLARES = "register_status_unchanged"


class ClosureException(Exception):
    """A closure that cannot be made mechanically."""


def _read_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def sha256_of(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


# --------------------------------------------------------------------------
# discovery
# --------------------------------------------------------------------------
def discover_manifests(tools_dir=None):
    """Every batch manifest that declares the follow-up register as its authority.

    Declaration is the whole test. A manifest that merely mentions the register,
    or merely mentions an FUP id, is not an authorisation record for it.
    """
    tools_dir = Path(tools_dir) if tools_dir else HERE
    found = []
    for path in sorted(glob.glob(str(tools_dir / "batch_*_manifest.json"))):
        try:
            data = _read_json(path)
        except (ValueError, OSError):
            continue
        if data.get("authorisation_source") != REGISTER_REL:
            continue
        found.append((Path(path), data))
    # Deterministic order, and the order production actually happened in:
    # a shorter batch id is the earlier batch (F1 before F1b).
    found.sort(key=lambda pair: (len(str(pair[1].get("batch_id", ""))),
                                 str(pair[1].get("batch_id", ""))))
    return found


# --------------------------------------------------------------------------
# derivation
# --------------------------------------------------------------------------
def derive(actions, manifests):
    """Return (closure_by_id, exceptions).

    `actions` is the register's action list (or any list of dicts carrying
    followup_id / parent_file / parent_anchor). `manifests` is what
    discover_manifests returns.

    Every entry in `closure_by_id` is mechanically proven. Anything needing
    judgement lands in `exceptions` and leaves the action untouched.
    """
    by_id = {a["followup_id"]: a for a in actions}
    closure = {}
    exceptions = []

    def raise_exc(kind, followup_id, manifest, detail):
        exceptions.append({
            "kind": kind,
            "followup_id": followup_id,
            "manifest": manifest,
            "detail": detail,
            "disposition": "NEEDS_FOUNDER_REVIEW",
        })

    for path, data in manifests:
        manifest_name = path.name
        batch_id = data.get("batch_id")
        if not batch_id:
            raise_exc("MANIFEST_HAS_NO_BATCH_ID", None, manifest_name,
                      "A manifest without a batch id cannot name the batch a "
                      "register row would be closed into.")
            continue

        discharged_here = {d.get("followup_id")
                           for d in (data.get("discharges_hold") or [])}

        # ---- holds: recorded, never a status change ----------------------
        for held in (data.get("held_actions") or []):
            fid = held.get("followup_id")
            if fid not in by_id:
                raise_exc("UNKNOWN_ACTION", fid, manifest_name,
                          "Held id is not in the register.")
                continue
            declared = held.get(HOLD_DECLARES)
            if declared is not None and declared != NOT_STARTED:
                raise_exc("HOLD_CLAIMS_STATUS_CHANGE", fid, manifest_name,
                          "Manifest declares %s=%r; a hold may not move the "
                          "register." % (HOLD_DECLARES, declared))
                continue
            closure.setdefault(fid, _blank(fid))
            closure[fid]["holds"].append({
                "batch_id": batch_id,
                "manifest": manifest_name,
                "status": held.get("status"),
                "target": held.get("target"),
                "discharged_by_batch_id": None,
            })

        # ---- discharges: must be produced by the discharging batch --------
        for disc in (data.get("discharges_hold") or []):
            fid = disc.get("followup_id")
            if fid not in by_id:
                raise_exc("UNKNOWN_ACTION", fid, manifest_name,
                          "Discharged id is not in the register.")
                continue
            produced_here = any(c.get("followup_id") == fid
                                for c in (data.get("cards") or []))
            if not produced_here:
                raise_exc("DISCHARGE_WITHOUT_PRODUCTION", fid, manifest_name,
                          "Batch declares it discharges this hold but its "
                          "cards[] does not implement it. Whether the hold is "
                          "genuinely satisfied is a judgement.")
                continue
            rec = closure.setdefault(fid, _blank(fid))
            for hold in rec["holds"]:
                if hold["discharged_by_batch_id"] is None:
                    hold["discharged_by_batch_id"] = batch_id

        # ---- cards: the only closure source ------------------------------
        for index, card in enumerate(data.get("cards") or []):
            fid = card.get("followup_id")
            if fid is None:
                continue  # a non-follow-up card in a mixed manifest
            if fid not in by_id:
                raise_exc("UNKNOWN_ACTION", fid, manifest_name,
                          "Card names an action the register does not hold.")
                continue

            action = by_id[fid]
            want = (action.get("parent_file"), action.get("parent_anchor"))
            got = (card.get("file"), card.get("anchor"))
            if want != got:
                raise_exc("TARGET_ROUND_TRIP_FAILED", fid, manifest_name,
                          "Register says %s#%s; manifest card says %s#%s. The "
                          "id resolves but points at a different record."
                          % (want[0], want[1], got[0], got[1]))
                continue

            rec = closure.setdefault(fid, _blank(fid))
            if rec["status"] == PRODUCED:
                prior = rec["production_evidence"]["batch_id"]
                if fid not in discharged_here:
                    raise_exc("DOUBLE_PRODUCTION", fid, manifest_name,
                              "Already produced by batch %s and re-produced "
                              "here without a discharges_hold declaration. "
                              "Which record is the implementation is a "
                              "judgement." % prior)
                    continue
            rec["status"] = PRODUCED
            rec["batch"] = batch_id
            rec["production_evidence"] = {
                "batch_id": batch_id,
                "manifest": "tools/oral/" + manifest_name,
                "card_index": index,
                "target": "%s#%s" % got,
            }

    # An exception disqualifies the action entirely: a row with an unresolved
    # question about it is not a row a writer may close.
    flagged = {e["followup_id"] for e in exceptions if e["followup_id"]}
    for fid in flagged:
        closure.pop(fid, None)

    return closure, exceptions


def _blank(fid):
    return {
        "followup_id": fid,
        "status": NOT_STARTED,
        "batch": None,
        "production_evidence": None,
        "holds": [],
    }


def closure_for_register(actions, tools_dir=None):
    """The generator's entry point. Refuses to return a partial derivation."""
    closure, exceptions = derive(actions, discover_manifests(tools_dir))
    if exceptions:
        raise ClosureException(
            "%d follow-up closure exception(s) need Founder review; the "
            "register will not be generated with a partial derivation:\n%s"
            % (len(exceptions),
               "\n".join("  %s %s (%s): %s" % (e["kind"], e["followup_id"],
                                               e["manifest"], e["detail"])
                         for e in exceptions)))
    return closure


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------
def _register_actions():
    if not REGISTER.exists():
        raise SystemExit("register not found: %s" % REGISTER)
    return _read_json(REGISTER)["actions"]


def _drift_rows(actions, closure):
    rows = []
    for a in actions:
        fid = a["followup_id"]
        derived = closure.get(fid, _blank(fid))
        register_state = (a.get("status"), a.get("batch"))
        actual_state = (derived["status"], derived["batch"])
        evidence = "-"
        if derived["production_evidence"]:
            evidence = "%s cards[%d]" % (
                derived["production_evidence"]["manifest"],
                derived["production_evidence"]["card_index"])
        elif derived["holds"]:
            evidence = "held by %s" % ", ".join(
                h["batch_id"] for h in derived["holds"])
        rows.append({
            "followup_id": fid,
            "register_state": "%s / %s" % (register_state[0], register_state[1]),
            "actual_state": "%s / %s" % (actual_state[0], actual_state[1]),
            "evidence": evidence,
            "drift": register_state != actual_state,
            "proposed": ("set status=%s batch=%s" % actual_state
                         if register_state != actual_state else "-"),
        })
    return rows


def _print_table(rows, only_drift=False):
    shown = [r for r in rows if r["drift"]] if only_drift else rows
    if not shown:
        print("  (none)")
        return
    head = "%-9s %-34s %-24s %s" % ("ACTION", "REGISTER_STATE",
                                    "ACTUAL_STATE", "EVIDENCE")
    print(head)
    print("-" * max(len(head), 96))
    for r in shown:
        print("%-9s %-34s %-24s %s%s" % (
            r["followup_id"], r["register_state"], r["actual_state"],
            r["evidence"], "   <-- DRIFT" if r["drift"] else ""))


def cmd_audit():
    actions = _register_actions()
    closure, exceptions = derive(actions, discover_manifests())
    rows = _drift_rows(actions, closure)
    print("Follow-up register audit -- %s" % REGISTER_REL)
    print("sha256: %s\n" % sha256_of(REGISTER))
    manifests = discover_manifests()
    print("Authorising manifests (declare authorisation_source = the register):")
    for path, data in manifests:
        print("  %-6s %-28s cards=%d held=%d discharges=%d" % (
            data.get("batch_id"), path.name, len(data.get("cards") or []),
            len(data.get("held_actions") or []),
            len(data.get("discharges_hold") or [])))
    print()
    _print_table(rows)
    produced = sum(1 for r in rows if r["actual_state"].startswith(PRODUCED))
    drifted = sum(1 for r in rows if r["drift"])
    held = sum(1 for f, c in closure.items() if c["holds"])
    print("\ntotal actions          %d" % len(rows))
    print("artefact-proven done   %d" % produced)
    print("still open             %d" % (len(rows) - produced))
    print("carried a hold         %d" % held)
    print("register drift rows    %d" % drifted)
    print("Founder review needed  %d" % len(exceptions))
    for e in exceptions:
        print("  %s %s (%s): %s" % (e["kind"], e["followup_id"],
                                    e["manifest"], e["detail"]))
    return 1 if exceptions else 0


def cmd_dry_run():
    actions = _register_actions()
    closure, exceptions = derive(actions, discover_manifests())
    rows = _drift_rows(actions, closure)
    drifted = [r for r in rows if r["drift"]]
    print("DRY RUN -- no file is written.")
    print("register: %s" % REGISTER_REL)
    print("sha256 before: %s" % sha256_of(REGISTER))
    print("\nproposed mechanical updates: %d\n" % len(drifted))
    _print_table(rows, only_drift=True)
    if drifted:
        print("\nevidence per proposed update:")
        for r in drifted:
            print("  %s  %s  ->  %s" % (r["followup_id"], r["proposed"],
                                        r["evidence"]))
    print("\nexceptions requiring Founder review: %d" % len(exceptions))
    for e in exceptions:
        print("  %s %s (%s): %s" % (e["kind"], e["followup_id"],
                                    e["manifest"], e["detail"]))
    if exceptions:
        print("\nREFUSED: --apply will not run while an exception stands.")
        return 1
    print("\nApply with: python %s --apply" % Path(__file__).name)
    return 0


def cmd_apply():
    actions = _register_actions()
    closure, exceptions = derive(actions, discover_manifests())
    if exceptions:
        print("REFUSED: %d exception(s) need Founder review. Run --dry-run."
              % len(exceptions))
        return 1
    before = sha256_of(REGISTER)
    rows = _drift_rows(actions, closure)
    drifted = [r for r in rows if r["drift"]]
    if not drifted:
        print("Register already matches the artefacts. Nothing to apply.")
        return 0
    # The register has exactly one author. Applying means re-running it, never
    # editing the JSON in place -- an in-place edit would turn the generator's
    # own byte-currency check red at the next validation.
    proc = subprocess.run([sys.executable, str(REPO / GENERATOR)],
                          cwd=str(REPO), capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    if proc.returncode != 0:
        return proc.returncode
    after = sha256_of(REGISTER)
    print("\nsha256 before: %s\nsha256 after:  %s" % (before, after))
    print("rows updated:  %d" % len(drifted))
    for r in drifted:
        print("  %s  %s" % (r["followup_id"], r["proposed"]))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Audit and mechanically close the follow-up register "
                    "against committed batch manifests.")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--audit", action="store_true",
                      help="report register state against artefact state")
    mode.add_argument("--dry-run", action="store_true",
                      help="report exactly what would change; write nothing")
    mode.add_argument("--apply", action="store_true",
                      help="regenerate the register through its generator")
    args = ap.parse_args(argv)
    if args.apply:
        return cmd_apply()
    if args.dry_run:
        return cmd_dry_run()
    return cmd_audit()


if __name__ == "__main__":
    sys.exit(main())
