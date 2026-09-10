#!/usr/bin/env python3
"""Compress a release run into one approval packet.

WHY THIS EXISTS
---------------
`run_oral_release.py` runs 85 gates and writes its evidence to a temp directory
by default. Approving a release therefore meant reading a transcript that does
not durably exist. This turns that run into a bounded, deterministic packet:
what candidate is being approved, what it would change, what the gates said,
what is still open, how to undo it, and exactly which act approval permits.

WHAT IT DOES NOT DO
-------------------
It does not run gates, push, deploy, publish, or re-implement any check. It
reads the runner's own JSON record and the repository state, and it never
touches product bytes. A packet is a *summary of evidence*, not a substitute
for it: every gate it counts is named, and the run log it was built from is
cited by path.

THE ONE RULE THAT MATTERS
-------------------------
A packet is APPROVABLE only when no gate failed, the run was not interrupted,
no mutation escaped, and the run's candidate is the candidate on disk now.
Anything else is BLOCKED, and a blocked packet carries no approval line at all
-- there is nothing to sign. Passing gates authorise nothing on their own; the
packet exists so a person makes the decision faster, not so the machine makes
it instead.

CANDIDATE BINDING
-----------------
A packet names the exact commit and the exact tree hash it describes. Change
either and the packet is a different packet: an approval cannot drift onto a
candidate nobody qualified. The tree hash is what catches the dangerous case,
because a dirty worktree keeps the same commit.

Usage:
    python tools/oral/build_release_packet.py --run <oral_release_*.json>
    python tools/oral/build_release_packet.py --run <json> --out packet.md
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

PASS = "PASS"
FAIL = "FAIL"
BASELINE = "PRE_EXISTING_BASELINE"
UNAVAILABLE = "UNAVAILABLE"
SKIPPED = "SKIPPED"

APPROVABLE = "APPROVABLE"
BLOCKED = "BLOCKED"

# The single act an approval on this packet permits. Naming it in the packet
# is the point: "approve the release" is not an act, "push main to origin,
# which deploys the candidate-facing bank" is.
APPROVED_ACT = ("push the named commit to origin/main, which deploys the "
                "candidate-facing question bank")


def git(*args, cwd=REPO):
    proc = subprocess.run(["git"] + list(args), cwd=str(cwd),
                          capture_output=True, text=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def candidate_identity(cwd=REPO):
    """The exact thing a packet describes: a commit AND the tree on disk.

    A dirty worktree keeps its commit, so a commit alone cannot identify what
    was qualified. `write-tree` hashes the index; the dirty flag reports
    anything the index has not been told about.
    """
    dirty = git("status", "--porcelain", cwd=cwd)
    return {
        "commit": git("rev-parse", "HEAD", cwd=cwd),
        "commit_short": git("rev-parse", "--short", "HEAD", cwd=cwd),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD", cwd=cwd),
        "tree": git("write-tree", cwd=cwd),
        "worktree_clean": dirty == "",
        "uncommitted_paths": sorted(
            line[3:] for line in (dirty or "").splitlines()) if dirty else [],
    }


def changed_surface(base_ref, cwd=REPO):
    """What the candidate would change relative to what is published."""
    raw = git("diff", "--numstat", "%s...HEAD" % base_ref, cwd=cwd)
    if raw is None:
        return None
    rows = []
    for line in raw.splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            rows.append({"added": parts[0], "removed": parts[1],
                         "path": parts[2]})
    return rows


def read_run(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def assess(run, candidate, base_ref=None, run_path=None):
    """Build the packet. Deterministic in its inputs, and only its inputs."""
    records = run.get("records") or []
    counts = Counter(r["status"] for r in records)

    failures = [r["gate"] for r in records if r["status"] == FAIL]
    baselines = [r["gate"] for r in records if r["status"] == BASELINE]
    unavailable = [r["gate"] for r in records if r["status"] == UNAVAILABLE]
    skipped = [r["gate"] for r in records if r["status"] == SKIPPED]

    planned = run.get("gates_planned") or []
    not_executed = [g for g in planned
                    if g not in {r["gate"] for r in records}]

    mutation_rows = [r for r in records if (r.get("detail") or {}).get("run")
                     is not None]
    escapes, no_ops, crashes, mutations = 0, 0, 0, 0
    escaped_ids = []
    for r in mutation_rows:
        det = r["detail"]
        mutations += det.get("run") or 0
        escapes += det.get("escapes") or 0
        no_ops += det.get("no_ops") or 0
        crashes += det.get("crashes") or 0
        for gid in det.get("escaped_ids") or []:
            escaped_ids.append("%s:%s" % (r["gate"], gid))

    unrestored = [r["gate"] for r in records
                  if r.get("mutates") and r.get("restore_verified") is False]

    blockers = []
    if run.get("interrupted"):
        blockers.append("the run was interrupted and did not reach every gate")
    if failures:
        blockers.append("%d gate(s) FAILED: %s"
                        % (len(failures), ", ".join(failures)))
    if escapes:
        blockers.append("%d mutation(s) escaped: %s"
                        % (escapes, ", ".join(escaped_ids)))
    if crashes:
        blockers.append("%d mutation(s) crashed" % crashes)
    if unrestored:
        blockers.append("worktree restore unverified after: %s"
                        % ", ".join(unrestored))
    if not_executed:
        blockers.append("%d planned gate(s) never executed: %s"
                        % (len(not_executed), ", ".join(not_executed)))
    if not records:
        blockers.append("the run recorded no gates at all")
    # An uncommitted worktree is not a release candidate. The packet names a
    # commit to push, and a dirty tree means that commit is NOT what the gates
    # qualified: the qualified bytes are the ones on disk, and pushing would
    # publish something else. Found by building a packet against a real run.
    if not candidate.get("worktree_clean"):
        blockers.append(
            "the worktree carries %d uncommitted path(s), so the commit named "
            "here is not what the gates qualified"
            % len(candidate.get("uncommitted_paths") or []))
    if run.get("exit") not in (0, None):
        blockers.append("the runner exited %s" % run.get("exit"))

    # A packet describes ONE candidate. If the run recorded which tree it ran
    # against and the tree on disk has moved, the evidence is about something
    # else -- which is the exact failure a packet is supposed to prevent.
    run_candidate = run.get("candidate") or {}
    if run_candidate.get("tree") and run_candidate["tree"] != candidate["tree"]:
        blockers.append("the qualified tree %s is not the tree on disk %s"
                        % (run_candidate["tree"][:12], candidate["tree"][:12]))

    verdict = BLOCKED if blockers else APPROVABLE

    packet = {
        "record_class": "release_approval_packet",
        "verdict": verdict,
        "candidate": candidate,
        "run": {
            "started": run.get("started"),
            "record": str(run_path) if run_path else None,
            "exit": run.get("exit"),
            "interrupted": bool(run.get("interrupted")),
        },
        "gates": {
            "planned": len(planned),
            "executed": len(records),
            "pass": counts.get(PASS, 0),
            "fail": counts.get(FAIL, 0),
            "pre_existing_baseline": counts.get(BASELINE, 0),
            "unavailable": counts.get(UNAVAILABLE, 0),
            "skipped": counts.get(SKIPPED, 0),
            "failed_gates": failures,
            "baseline_gates": baselines,
            "unavailable_gates": unavailable,
            "skipped_gates": skipped,
            "not_executed": not_executed,
        },
        "mutations": {
            "suites": len(mutation_rows),
            "mutations": mutations,
            "escapes": escapes,
            "escaped_ids": escaped_ids,
            "no_ops": no_ops,
            "crashes": crashes,
        },
        "exceptions": {
            # A warning state is an exception the approver must see, not a
            # rounding error. It never disappears into a pass count.
            "pre_existing_baseline": baselines,
            "unavailable": unavailable,
            "skipped": skipped,
            "no_ops": no_ops,
        },
        "blockers": blockers,
        "blast_radius": None,
        "rollback": None,
        "approval": None,
    }

    if base_ref:
        surface = changed_surface(base_ref)
        if surface is not None:
            packet["blast_radius"] = {
                "compared_against": base_ref,
                "files_changed": len(surface),
                "files": surface[:200],
                "truncated": len(surface) > 200,
                # A commit-to-commit diff is blind to uncommitted work. Saying
                # "0 files differ" over a dirty tree is the most misleading
                # line a packet could carry, so it is named here explicitly.
                "uncommitted_paths_not_in_this_diff":
                    candidate.get("uncommitted_paths") or [],
            }

    packet["rollback"] = {
        "published_state": base_ref,
        "method": ("nothing is published until the approved act is performed; "
                   "before that, reverting is a local matter. After the push, "
                   "roll back by pushing a revert of %s."
                   % (candidate["commit_short"] or "the candidate")),
    }

    if verdict == APPROVABLE:
        packet["approval"] = {
            "permits_exactly": APPROVED_ACT,
            "scope": ("only the commit %s / tree %s named above. This approval "
                      "does not carry to any later commit."
                      % (candidate["commit_short"], (candidate["tree"] or "")[:12])),
            "does_not_permit": [
                "any further content change",
                "any workbook or Excel distribution",
                "any other repository or pipeline",
            ],
        }

    return packet


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------
def render(packet):
    c = packet["candidate"]
    g = packet["gates"]
    m = packet["mutations"]
    out = []
    add = out.append

    add("# Release approval packet - %s" % packet["verdict"])
    add("")
    add("| | |")
    add("|---|---|")
    add("| candidate commit | `%s` (%s) |" % (c["commit_short"], c["branch"]))
    add("| candidate tree | `%s` |" % (c["tree"] or "-"))
    add("| worktree | %s |" % ("clean" if c["worktree_clean"]
                               else "%d uncommitted path(s)"
                                    % len(c["uncommitted_paths"])))
    add("| run started | %s |" % (packet["run"]["started"] or "-"))
    add("| run record | `%s` |" % (packet["run"]["record"] or "-"))
    add("")
    add("## Gates")
    add("")
    add("| result | count |")
    add("|---|---|")
    add("| planned | %d |" % g["planned"])
    add("| executed | %d |" % g["executed"])
    add("| PASS | %d |" % g["pass"])
    add("| FAIL | %d |" % g["fail"])
    add("| pre-existing baseline | %d |" % g["pre_existing_baseline"])
    add("| unavailable | %d |" % g["unavailable"])
    add("| skipped | %d |" % g["skipped"])
    add("")
    add("Mutations: %d suites, %d mutations, %d escapes, %d no-ops, %d crashes."
        % (m["suites"], m["mutations"], m["escapes"], m["no_ops"],
           m["crashes"]))
    add("")

    add("## Exceptions the approver must see")
    add("")
    exc = packet["exceptions"]
    any_exc = False
    for label, key in (("FAILED", None), ("pre-existing baseline",
                                          "pre_existing_baseline"),
                       ("unavailable", "unavailable"), ("skipped", "skipped")):
        names = g["failed_gates"] if key is None else exc[key]
        if names:
            any_exc = True
            add("- **%s** (%d): %s" % (label, len(names), ", ".join(names)))
    if m["escaped_ids"]:
        any_exc = True
        add("- **escaped mutations**: %s" % ", ".join(m["escaped_ids"]))
    if exc["no_ops"]:
        any_exc = True
        add("- **no-op mutations**: %d — a mutation that changed nothing "
            "proved nothing." % exc["no_ops"])
    if not any_exc:
        add("None. Every planned gate executed and passed.")
    add("")

    br = packet["blast_radius"]
    add("## Blast radius")
    add("")
    if br:
        add("%d file(s) differ from `%s`."
            % (br["files_changed"], br["compared_against"]))
        if br["uncommitted_paths_not_in_this_diff"]:
            add("")
            add("**This diff is between commits and does not include %d "
                "uncommitted path(s).**"
                % len(br["uncommitted_paths_not_in_this_diff"]))
        add("")
        if br["files"]:
            add("| +/- | path |")
            add("|---|---|")
            for row in br["files"][:40]:
                add("| +%s/-%s | `%s` |" % (row["added"], row["removed"],
                                            row["path"]))
            if br["files_changed"] > 40:
                add("| … | %d more |" % (br["files_changed"] - 40))
    else:
        add("Not computed — no published baseline reference was given.")
    add("")

    add("## Rollback")
    add("")
    add(packet["rollback"]["method"])
    add("")

    add("## Decision")
    add("")
    if packet["verdict"] == BLOCKED:
        add("**BLOCKED - there is nothing to approve.**")
        add("")
        for b in packet["blockers"]:
            add("- %s" % b)
        add("")
        add("Fix the blocker and re-run the release. A blocked packet carries "
            "no approval line by design.")
    else:
        a = packet["approval"]
        add("Approving this packet permits **exactly one act**:")
        add("")
        add("> %s" % a["permits_exactly"])
        add("")
        add("Scope: %s" % a["scope"])
        add("")
        add("It does not permit:")
        for item in a["does_not_permit"]:
            add("- %s" % item)
        add("")
        add("Nothing is pushed, deployed or published by this packet, by the "
            "runner, or by any gate passing. The act above is performed by a "
            "person after approval.")
    add("")
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Compress a release run into one approval packet.")
    ap.add_argument("--run", required=True,
                    help="the runner's oral_release_*.json record")
    ap.add_argument("--base-ref", default=None,
                    help="published reference for the blast radius, "
                         "e.g. origin/main")
    ap.add_argument("--out", default=None,
                    help="write the markdown packet here (default: stdout)")
    ap.add_argument("--json-out", default=None,
                    help="also write the packet as JSON")
    args = ap.parse_args(argv)

    run_path = Path(args.run)
    if not run_path.exists():
        print("no such run record: %s" % run_path, file=sys.stderr)
        return 2

    packet = assess(read_run(run_path), candidate_identity(),
                    base_ref=args.base_ref, run_path=run_path)
    text = render(packet)

    if args.out:
        Path(args.out).write_text(text, encoding="utf-8", newline="")
    else:
        sys.stdout.write(text)
    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps(packet, indent=2, sort_keys=True) + "\n",
            encoding="utf-8", newline="")

    # Exit code is the verdict, so a wrapper cannot mistake a blocked packet
    # for an approvable one.
    return 0 if packet["verdict"] == APPROVABLE else 1


if __name__ == "__main__":
    sys.exit(main())
