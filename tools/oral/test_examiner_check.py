"""Freshness gate tests for build_examiner_index.py --check.

--check must CHECK: build every governed artefact in memory, compare bytes
with disk, run the semantic validator, and write nothing. These tests prove
each clause with a real mutation, run through the tool as a subprocess, and
require the failure to be the NAMED freshness/validation failure - non-zero
exit, an "EXAMINER INDEX CHECK: FAIL" line, a STALE/MISSING OUTPUT line where
freshness is the point, and no traceback. Every artefact is restored
byte-for-byte afterwards; a mutation that survives restoration is itself a
test failure, so this can never re-baseline anything.

  A  pristine tree                                   -> PASS, exit 0
  B  stale full index (hand-edited section count)    -> FAIL, STALE meoclass1/examiner-index.html
  C  stale snapshot (one total altered)              -> FAIL, STALE EXAMINER_INDEX_SNAPSHOT.json
  D  stale SQ teaser (one stat altered)              -> FAIL, STALE SQ/examiner-index.html
  E  stale SQ home card (one generated count)        -> FAIL, STALE SQ/index.html
  F  missing generated artefact                      -> FAIL, MISSING OUTPUT
  G  generator input changed, nothing regenerated    -> FAIL, every dependent artefact STALE
  H  --check writes nothing: hashes + git status identical around every run
  I  normal generation on a current tree             -> zero byte change (write path == check path)
  J  staging residue beside a generated artefact     -> FAIL, EXTRA OUTPUT

    PYTHONIOENCODING=utf-8 python tools/oral/test_examiner_check.py
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oral_lib as L  # noqa: E402
import build_examiner_index as G  # noqa: E402

TOOLS = Path(__file__).resolve().parent
GEN = TOOLS / "build_examiner_index.py"
OUTPUTS = list(G.GENERATED_OUTPUTS)
SNAP, INDEX, SQ, SQ_HOME = OUTPUTS
DECISIONS = G.OUT / G.REVIEW_NAME
RESIDUE = SQ.parent / (SQ.name + ".test.staging")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONHASHSEED="0")


def run_check():
    r = subprocess.run([sys.executable, str(GEN), "--check"], capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=ENV, cwd=str(L.REPO))
    out = r.stdout + r.stderr
    return r.returncode, out, ("Traceback" in out)


def run_build():
    r = subprocess.run([sys.executable, str(GEN)], capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=ENV, cwd=str(L.REPO))
    return r.returncode, r.stdout + r.stderr


def git_status():
    return subprocess.run(["git", "status", "--short", "--untracked-files=all"],
                          cwd=str(L.REPO), capture_output=True, text=True).stdout


def hashes(paths):
    return {p: (hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None) for p in paths}


class Guard:
    """Snapshot bytes of every artefact a test may touch; restore on exit."""
    def __init__(self, *paths):
        self.saved = {p: (p.read_bytes() if p.exists() else None) for p in paths}

    def __enter__(self):
        return self

    def __exit__(self, *a):
        for p, b in self.saved.items():
            if b is None:
                if p.exists():
                    p.unlink()
            else:
                p.write_bytes(b)


def replace_once(path, old, new):
    b = path.read_bytes()
    if b.count(old) != 1:
        raise RuntimeError("%s: expected exactly one %r, found %d" % (path.name, old, b.count(old)))
    path.write_bytes(b.replace(old, new))


# ---------------------------------------------------------------- mutations

def m_B():
    snap = json.loads(SNAP.read_text(encoding="utf-8"))
    sec = snap["sections"][1]
    n = sec["count"]
    replace_once(INDEX, ('<span class="ex-count">%d questions</span>' % n).encode(),
                 ('<span class="ex-count">%d questions</span>' % (n + 1)).encode())
    return [INDEX]


def m_C():
    snap = json.loads(SNAP.read_text(encoding="utf-8"))
    n = snap["totals"]["relationships"]
    replace_once(SNAP, ('"relationships": %d' % n).encode(), ('"relationships": %d' % (n + 1)).encode())
    return [SNAP]


def m_D():
    snap = json.loads(SNAP.read_text(encoding="utf-8"))
    n = snap["totals"]["relationships"]
    replace_once(SQ, ('<div class="stat-num">%d</div><div class="stat-label">Questions Tagged</div>' % n).encode(),
                 ('<div class="stat-num">%d</div><div class="stat-label">Questions Tagged</div>' % (n - 1)).encode())
    return [SQ]


def m_E():
    snap = json.loads(SNAP.read_text(encoding="utf-8"))
    secs = {s["slug"]: s for s in snap["sections"]}
    promo = secs[G.CONFIG["sq"]["promo_examiner"]]
    replace_once(SQ_HOME, ("%s Sir's %d " % (promo["name"], promo["count"])).encode(),
                 ("%s Sir's %d " % (promo["name"], promo["count"] + 1)).encode())
    return [SQ_HOME]


def m_F():
    SQ.unlink()
    return [SQ]


def m_G():
    """The real workflow mistake: a governed INPUT changes (one CE-tip review
    approval is withdrawn to a hold) and nobody regenerates. Every artefact
    that depends on the decision must be stale."""
    dec = json.loads(DECISIONS.read_text(encoding="utf-8"))
    # a promo-examiner (Simon) approval: its count reaches the SQ home card
    # too, so all four artefacts must go stale, not three
    snap = json.loads(SNAP.read_text(encoding="utf-8"))
    promo_name = next(s["name"] for s in snap["sections"]
                      if s["slug"] == G.CONFIG["sq"]["promo_examiner"])
    d = next(x for x in dec["decisions"] if x["decision"] == "APPROVE_CE_TIP_RELATIONSHIP"
             and x["examiner"] == promo_name)
    d["decision"] = "HOLD_WEAK_ASSERTION"
    d.pop("candidate_tier", None)
    DECISIONS.write_bytes(json.dumps(dec, ensure_ascii=False, indent=1).encode("utf-8"))
    return [SNAP, INDEX, SQ, SQ_HOME]


def m_J():
    RESIDUE.write_bytes(b"half-written")
    return [RESIDUE]


MUTATIONS = [
    ("B", "stale full index: section count hand-edited", m_B, "STALE OUTPUT"),
    ("C", "stale snapshot: total altered", m_C, "STALE OUTPUT"),
    ("D", "stale SQ teaser: stat altered", m_D, "STALE OUTPUT"),
    ("E", "stale SQ home card: promo count altered", m_E, "STALE OUTPUT"),
    ("F", "missing generated artefact (SQ teaser deleted)", m_F, "MISSING OUTPUT"),
    ("G", "input changed (review approval -> hold), not regenerated", m_G, "STALE OUTPUT"),
    ("J", "staging residue beside the SQ teaser", m_J, "EXTRA OUTPUT"),
]


def main():
    failures = 0
    watched = OUTPUTS + [DECISIONS, RESIDUE]
    h0, s0 = hashes(watched), git_status()

    # A pristine
    rc, out, crashed = run_check()
    ok = rc == 0 and "EXAMINER INDEX CHECK: PASS" in out and not crashed
    print("A  pristine tree                                     exit=%d  %s" % (rc, "PASS" if ok else "FAIL"))
    if not ok:
        failures += 1
        print(out[-1500:])
        print("baseline not green; the mutation tests below prove nothing")
        return 2

    # H (part 1): the pristine check wrote nothing
    if hashes(watched) != h0 or git_status() != s0:
        print("H  --check on pristine tree changed the tree                 FAIL")
        failures += 1

    for code, label, mut, marker in MUTATIONS:
        with Guard(*watched):
            expected_stale = mut()
            rc, out, crashed = run_check()
            named = "EXAMINER INDEX CHECK: FAIL" in out
            listed = all(("%s: %s" % (marker, G.rel(p))) in out for p in expected_stale)
            no_write = hashes(watched) == {p: (hashlib.sha256(p.read_bytes()).hexdigest()
                                              if p.exists() else None) for p in watched}
            ok = rc != 0 and named and listed and not crashed and no_write
            print("%s  %-52s exit=%d named=%s listed=%s crash=%s  %s" % (
                code, label, rc, named, listed, crashed, "CAUGHT" if ok else "ESCAPE"))
            if not ok:
                failures += 1
                print(out[-1200:])
        # restoration proven
        if hashes(watched) != h0:
            print("   restoration failed after %s" % code)
            failures += 1

    # H (part 2): after every mutation run, tree identical to start
    h_ok = hashes(watched) == h0 and git_status() == s0
    print("H  --check never wrote: hashes+git status identical      %s" % ("PASS" if h_ok else "FAIL"))
    if not h_ok:
        failures += 1
        print(git_status())

    # I normal generation on a current tree is a byte no-op
    rc, out = run_build()
    i_ok = rc == 0 and hashes(watched) == h0 and git_status() == s0
    print("I  normal generation on current tree = zero byte change  exit=%d  %s" % (rc, "PASS" if i_ok else "FAIL"))
    if not i_ok:
        failures += 1
        print(out[-800:])
        print(git_status())

    # no staging residue anywhere the generator writes
    residue = [p for d in {o.parent for o in OUTPUTS} for p in d.glob("*.staging")]
    if residue:
        print("staging residue: %s" % residue)
        failures += 1

    print("\n%d tests, %d failures" % (len(MUTATIONS) + 3, failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
