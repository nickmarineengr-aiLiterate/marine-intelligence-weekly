"""Controls for the release approval packet.

A packet exists so a person decides faster, never so the machine decides
instead. Every control here guards one of the two ways that could go wrong: a
packet that hides a failure, or a packet whose approval drifts onto a candidate
nobody qualified.

  PYTHONIOENCODING=utf-8 python tools/oral/test_release_packet.py

Exit 0 when every control holds. No network, no release run, no mutation of any
tracked file: every input is a fixture built in memory.
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

import build_release_packet as P  # noqa: E402

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
CANDIDATE = {"commit": "a" * 40, "commit_short": "aaaaaaa", "branch": "main",
             "tree": "b" * 40, "worktree_clean": True, "uncommitted_paths": []}


def gate(gid, status=P.PASS, detail=None, mutates=False, restored=True):
    return {"gate": gid, "status": status, "detail": detail or {},
            "mutates": mutates, "restore_verified": restored,
            "seconds": 1.0, "restored": [], "product_restored": [],
            "started": "2026-09-10T00:00:00"}


FULL_SUITE = P.full_suite_gate_ids() or []


def run(records=None, **kw):
    """A fixture run. By default it plans the whole suite, because a partial
    run is itself a blocker and would otherwise mask every other control."""
    records = records if records is not None else [gate(g) for g in FULL_SUITE]
    base = {"started": "20260910T000000Z",
            "gates_planned": [r["gate"] for r in records],
            "records": records, "interrupted": False, "exit": 0,
            "candidate": {"tree": CANDIDATE["tree"]}}
    base.update(kw)
    return base


# ===========================================================================
print("\n--- 1. a clean run is approvable, and says what approval permits ---")
# ===========================================================================
pkt = P.assess(run(), CANDIDATE)
check("the full suite is read from the registry, never remembered",
      len(FULL_SUITE) > 50, "%d gates" % len(FULL_SUITE))
check("a clean run produces an APPROVABLE packet",
      pkt["verdict"] == P.APPROVABLE, pkt["verdict"])
check("the packet carries no blockers", pkt["blockers"] == [], "")
check("the packet names exactly one act",
      pkt["approval"]["permits_exactly"] == P.APPROVED_ACT,
      pkt["approval"]["permits_exactly"])
check("the act named is a push, not an abstract 'release'",
      "push" in pkt["approval"]["permits_exactly"], "")
_text = P.render(pkt)
check("the rendered packet states the act in full", P.APPROVED_ACT in _text, "")


# ===========================================================================
print("\n--- 2. a failed gate can never produce an approvable packet ---")
# ===========================================================================
pkt = P.assess(run([gate(FULL_SUITE[0]), gate("g2", P.FAIL)]), CANDIDATE)
check("one FAIL blocks the packet", pkt["verdict"] == P.BLOCKED, pkt["verdict"])
check("a blocked packet carries no approval line at all",
      pkt["approval"] is None, "nothing to sign")
check("the failing gate is named, not counted",
      pkt["gates"]["failed_gates"] == ["g2"], str(pkt["gates"]["failed_gates"]))
_text = P.render(pkt)
check("the rendered packet says BLOCKED first",
      _text.startswith("# Release approval packet - BLOCKED"),
      _text.splitlines()[0])
check("a blocked packet never renders an approval sentence",
      P.APPROVED_ACT not in _text, "")


# ===========================================================================
print("\n--- 3. every other way a run can be unsound also blocks ---")
# ===========================================================================
cases = [
    ("interrupted run", run(interrupted=True)),
    ("non-zero runner exit", run(exit=1)),
    ("planned gate never executed",
     dict(run(), gates_planned=FULL_SUITE + ["g_extra"])),
    ("escaped mutation",
     run([gate(g) for g in FULL_SUITE[:-1]]
         + [gate(FULL_SUITE[-1], detail={"run": 10, "escapes": 1, "no_ops": 0,
                                         "crashes": 0, "escaped_ids": ["K"]},
                 mutates=True)])),
    ("crashed mutation",
     run([gate(g) for g in FULL_SUITE[:-1]]
         + [gate(FULL_SUITE[-1], detail={"run": 10, "escapes": 0, "no_ops": 0,
                                         "crashes": 2}, mutates=True)])),
    ("unverified restore",
     run([gate(g) for g in FULL_SUITE[:-1]]
         + [gate(FULL_SUITE[-1], detail={"run": 4, "escapes": 0, "no_ops": 0,
                                         "crashes": 0}, mutates=True,
                 restored=False)])),
    ("no gates at all", run([])),
    ("dirty worktree", run()),
    # Six green gates out of eighty-six is a check, not a qualification.
    ("partial run", run([gate(FULL_SUITE[0]), gate(FULL_SUITE[1])])),
]
for label, fixture in cases:
    subject = (dict(CANDIDATE, worktree_clean=False,
                    uncommitted_paths=["tools/oral/x.py"])
               if label == "dirty worktree" else CANDIDATE)
    p = P.assess(fixture, subject)
    check("blocked: %s" % label, p["verdict"] == P.BLOCKED,
          "; ".join(p["blockers"])[:80])


# ===========================================================================
print("\n--- 4. an approval cannot drift onto another candidate ---")
# ===========================================================================
moved = dict(CANDIDATE, tree="c" * 40)
pkt = P.assess(run(), moved)
check("a tree that moved since the run blocks the packet",
      pkt["verdict"] == P.BLOCKED,
      "; ".join(pkt["blockers"])[:90])

pkt_a = P.assess(run(), CANDIDATE)
pkt_b = P.assess(run(), dict(CANDIDATE, commit="d" * 40, commit_short="ddddddd"))
check("the packet identifies the exact candidate",
      pkt_a["candidate"]["commit"] != pkt_b["candidate"]["commit"], "")
check("the packet changes when the candidate changes",
      json.dumps(pkt_a, sort_keys=True) != json.dumps(pkt_b, sort_keys=True),
      "a packet is about one candidate")
check("the approval scope names the commit and the tree",
      pkt_a["candidate"]["commit_short"] in pkt_a["approval"]["scope"]
      and pkt_a["candidate"]["tree"][:12] in pkt_a["approval"]["scope"], "")
check("the approval refuses to carry forward",
      "does not carry" in pkt_a["approval"]["scope"], "")


# ===========================================================================
print("\n--- 5. warnings are surfaced, never absorbed into a pass count ---")
# ===========================================================================
_rest = [gate(g) for g in FULL_SUITE[4:]]
pkt = P.assess(run([gate(FULL_SUITE[0]),
                    gate(FULL_SUITE[1], P.BASELINE),
                    gate(FULL_SUITE[2], P.UNAVAILABLE),
                    gate(FULL_SUITE[3], P.SKIPPED)] + _rest[:-1]
                   + [gate(_rest[-1]["gate"],
                           detail={"run": 6, "escapes": 0, "no_ops": 2,
                                   "crashes": 0}, mutates=True)]),
                CANDIDATE)
check("a baseline state does not count as a pass",
      pkt["gates"]["pass"] == len(FULL_SUITE) - 3
      and pkt["gates"]["pre_existing_baseline"] == 1,
      "pass=%d baseline=%d" % (pkt["gates"]["pass"],
                               pkt["gates"]["pre_existing_baseline"]))
check("unavailable and skipped gates are listed by name",
      pkt["exceptions"]["unavailable"] == [FULL_SUITE[2]]
      and pkt["exceptions"]["skipped"] == [FULL_SUITE[3]], "")
check("a no-op mutation is reported as an exception",
      pkt["exceptions"]["no_ops"] == 2, "a mutation that changed nothing "
      "proved nothing")
_text = P.render(pkt)
for token in ("pre-existing baseline", "unavailable", "skipped", "no-op"):
    check("the rendered packet surfaces %r" % token, token in _text, "")


# ===========================================================================
print("\n--- 6. nothing here pushes, deploys or publishes ---")
# ===========================================================================
_src = (HERE / "build_release_packet.py").read_text(encoding="utf-8")
_calls = [line for line in _src.splitlines()
          if 'git(' in line and any(w in line for w in
                                    ('"push"', '"deploy"', '"remote"'))]
check("the packet builder issues no push or deploy", _calls == [], str(_calls))
check("the packet says the act is performed by a person",
      "performed by a person after approval" in P.render(P.assess(run(),
                                                                  CANDIDATE)),
      "")
_runner = (HERE / "run_oral_release.py").read_text(encoding="utf-8")
check("the release runner still has no push path",
      'subprocess.run(["git", "push"' not in _runner
      and '"push"' not in _runner, "gates passing cannot publish")


# ===========================================================================
print("\n--- 7. determinism ---")
# ===========================================================================
a = P.assess(run(), CANDIDATE)
b = P.assess(run(), CANDIDATE)
check("identical release evidence yields an identical packet",
      json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), "")
check("identical evidence yields identical markdown",
      P.render(a) == P.render(b), "")


# ===========================================================================
print("\n--- 8. the CLI verdict is the exit code ---")
# ===========================================================================
with tempfile.TemporaryDirectory() as tmp:
    good = Path(tmp) / "good.json"
    good.write_text(json.dumps(run(candidate={})), encoding="utf-8")
    bad = Path(tmp) / "bad.json"
    bad.write_text(json.dumps(run([gate("g1", P.FAIL)], candidate={})),
                   encoding="utf-8")
    out = Path(tmp) / "packet.md"
    rc_good = subprocess.run(
        [sys.executable, str(HERE / "build_release_packet.py"),
         "--run", str(good), "--out", str(out)],
        cwd=str(REPO), capture_output=True, text=True).returncode
    rc_bad = subprocess.run(
        [sys.executable, str(HERE / "build_release_packet.py"),
         "--run", str(bad)], cwd=str(REPO), capture_output=True,
        text=True).returncode
    # The CLI reads the REAL repository for its candidate, so whether the good
    # fixture is approvable depends on whether this worktree is clean. The
    # control is therefore that the exit code IS the verdict -- not that a
    # particular verdict comes out of a particular checkout.
    expected_good = P.assess(json.loads(good.read_text(encoding="utf-8")),
                             P.candidate_identity())["verdict"]
    check("the exit code is the verdict",
          (rc_good == 0) == (expected_good == P.APPROVABLE),
          "verdict=%s exit=%d" % (expected_good, rc_good))
    check("a blocked packet exits non-zero", rc_bad != 0, "exit %d" % rc_bad)
    check("--out writes the packet", out.exists() and out.stat().st_size > 0,
          "%d bytes" % (out.stat().st_size if out.exists() else 0))
    check("a missing run record is refused, not guessed",
          subprocess.run([sys.executable,
                          str(HERE / "build_release_packet.py"),
                          "--run", str(Path(tmp) / "nope.json")],
                         cwd=str(REPO), capture_output=True).returncode == 2,
          "")


# ===========================================================================
print("\n%d checks, %d FAIL" % (CHECKS[0], len(FAILURES)))
for f in FAILURES:
    print("  FAIL %s" % f)
sys.exit(1 if FAILURES else 0)
