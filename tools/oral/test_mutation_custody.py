#!/usr/bin/env python3
"""
Controls for mutation custody -- the interruption-safety contract.

WHY THIS SUITE EXISTS
---------------------

On 4 September 2026 an interrupted run of ``mutate_corrections.py`` left the
working tree with a HISTORICAL correction manifest deleted, a digest zeroed and
QB HTML mutated, and it was repaired by hand.  A mutation suite that needs hand
repair after Ctrl-C is not a governed runner: the repair is discretionary, and
the next person to run it may not notice there was one to make.

The claim under test is a single invariant:

    Whether the suite finishes normally, fails, raises, is interrupted or is
    terminated at the Python level, every mutation target is restored to its
    exact original bytes before control returns.

EVERY FIXTURE HERE IS DISPOSABLE
--------------------------------
Nothing in this file touches the real corpus, the real manifests or the real
repository.  Sections 1-4 build a throwaway tree under ``tempfile.mkdtemp``;
section 5 kills a REAL child process, which is why it must never be pointed at
anything but a temp tree.  ``mutate_corrections.py``'s own probes already prove
the suite works on the live corpus; what this file proves is that it PUTS IT
BACK, and that claim can be proved anywhere.

SECTION 5 IS THE HONEST ONE
---------------------------
A process killed with a non-catchable signal executes no Python: no ``finally``,
no ``atexit``, no handler.  Section 5 does exactly that to a child and asserts
the damage IS present afterwards -- because pretending otherwise would be the
lie this whole layer exists to avoid.  What it then proves is the recoverable
part: the journal was on disk before the mutation, the damage is repairable
from it, and the next run refuses to start until it has been.
"""

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from oral_custody import (Custodian, CustodyError, JOURNAL_DIRNAME,   # noqa: E402
                          discard, recover, stale_runs)

COUNT = [0]
FAILURES = []


def check(name, ok, detail=""):
    COUNT[0] += 1
    print("%-6s %-68s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAILURES.append(name)


def section(title):
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


class Tree:
    """A disposable repository-shaped directory."""

    def __init__(self):
        self.root = pathlib.Path(tempfile.mkdtemp(prefix="custody-"))
        self.kept = self.root / "kept.html"
        self.doomed = self.root / "doomed.json"
        self.kept.write_bytes(b"<div class=\"q-card\" id=\"q1\">original</div>\r\n")
        self.doomed.write_bytes(b'{"correction_id": "CORR-FIXTURE"}\n')
        self.before = {p: p.read_bytes() for p in (self.kept, self.doomed)}

    def intact(self):
        return all(p.is_file() and p.read_bytes() == blob
                   for p, blob in self.before.items())

    def close(self):
        shutil.rmtree(self.root, ignore_errors=True)


# =============================================================================
section("1. THE FOUR EXIT PATHS -- return, probe FAIL, probe raise, mutator raise")
# =============================================================================

# 1. normal mutation -> restored
t = Tree()
cust = Custodian(t.root, install_handlers=False)
with cust.guard([t.kept]):
    t.kept.write_bytes(b"MUTATED")
check("1  normal mutation is restored", t.intact(),
      "kept.html back to %d bytes" % len(t.before[t.kept]))

# 2. probe FAIL (the ordinary case: the mutation worked, the guard went red)
with cust.guard([t.kept]):
    t.kept.write_bytes(b"MUTATED")
    probe_rc = 1                       # a red probe is a RESULT, not an error
check("2  a FAILING probe still restores", t.intact() and probe_rc == 1,
      "probe rc=%d" % probe_rc)

# 3. probe exception -> restored, and the exception is NOT swallowed
raised = None
try:
    with cust.guard([t.kept]):
        t.kept.write_bytes(b"MUTATED")
        raise RuntimeError("probe subprocess blew up")
except RuntimeError as exc:
    raised = str(exc)
check("3  a raising probe restores AND propagates",
      t.intact() and raised == "probe subprocess blew up", "raised=%r" % raised)

# 4. mutator exception -> restored (the mutator may have half-applied)
raised = None
try:
    with cust.guard([t.kept, t.doomed]):
        t.kept.write_bytes(b"HALF")
        raise AssertionError("card not found")
except AssertionError as exc:
    raised = str(exc)
check("4  a raising MUTATOR restores every file it had already touched",
      t.intact() and raised == "card not found", "raised=%r" % raised)

# 5. KeyboardInterrupt / SystemExit -- BaseException, the actual incident path
for exc_type in (KeyboardInterrupt, SystemExit):
    caught = False
    try:
        with cust.guard([t.kept, t.doomed]):
            t.kept.write_bytes(b"MUTATED")
            t.doomed.unlink()
            raise exc_type()
    except BaseException:
        caught = True
    check("5  %s restores (BaseException, not Exception)" % exc_type.__name__,
          t.intact() and caught, "both files back")

# =============================================================================
section("2. EVERY SHAPE OF DAMAGE THE REAL SUITE INFLICTS")
# =============================================================================

# 6. transient file created -> removed
transient = t.root / "correction_corr_fixture_manifest.json"
with cust.guard([transient]):
    transient.write_text('{"kind": "POST_RELEASE_CORRECTION"}\n', encoding="utf-8")
    existed_during = transient.is_file()
check("6  a transient file created under custody is removed",
      existed_during and not transient.is_file(), "created then unlinked")

# 7. existing file DELETED -> restored (mutation A1's shape)
with cust.guard([t.doomed]):
    t.doomed.unlink()
    gone_during = not t.doomed.is_file()
check("7  a DELETED manifest is restored", gone_during and t.intact(),
      "doomed.json back, %d bytes" % len(t.before[t.doomed]))

# 8. existing file modified -> byte-identical, including line endings
crlf_before = t.before[t.kept]
with cust.guard([t.kept]):
    t.kept.write_bytes(crlf_before.replace(b"\r\n", b"\n") + b"extra")
check("8  a modified file is restored BYTE-identically (CRLF preserved)",
      t.kept.read_bytes() == crlf_before and b"\r\n" in t.kept.read_bytes(),
      "sha-stable, CRLF intact")

# 9. restoration failure -> explicit HARD FAIL, never a silent pass
#    Simulated by making the target unrestorable: custody captured a FILE, and
#    a directory now stands in its place, so write_bytes cannot succeed.
blocked = t.root / "blocked.txt"
blocked.write_bytes(b"original")
hard_fail = None
try:
    with cust.guard([blocked]):
        blocked.unlink()
        blocked.mkdir()
except CustodyError as exc:
    hard_fail = str(exc)
check("9  an unrestorable file raises CustodyError (hard fail, typed)",
      hard_fail is not None and "restore verification failed" in (hard_fail or ""),
      (hard_fail or "-")[:60])
blocked.rmdir()

# 10. the closing tree-integrity assertion.
#     Check 9 deliberately left one file unrestorable, so the FIRST thing
#     verify_pristine must do is still be reporting it -- a hard fail that
#     stops being visible the moment the next check runs would be worse than
#     no hard fail at all.
drift = cust.verify_pristine()
check("10 verify_pristine still reports the file check 9 could not restore",
      [d for d in drift if "blocked.txt" in d], "drift=%d file(s)" % len(drift))
blocked.write_bytes(b"original")
check("10 verify_pristine is clean once that file is repaired by hand",
      cust.verify_pristine() == [], "no drift")
t.kept.write_bytes(b"edited outside any guard")
drift = cust.verify_pristine()
check("10 verify_pristine DETECTS an out-of-guard edit", len(drift) == 1,
      drift[0].split(": ")[-1] if drift else "-")
t.kept.write_bytes(crlf_before)
check("10 verify_pristine is clean again once repaired",
      cust.verify_pristine() == [], "no drift")

# non-vacuity: the checks above would notice if guard() did nothing at all
t.kept.write_bytes(b"unguarded damage")
check("10 (control) an unguarded mutation is NOT restored",
      not t.intact(), "the guard is what restores, not the tempdir")
t.kept.write_bytes(crlf_before)

cust.close()
check("   close() removes the journal directory",
      not stale_runs(t.root), "no stale runs")
t.close()

# =============================================================================
section("3. THE JOURNAL IS ON DISK BEFORE THE MUTATION IS APPLIED")
# =============================================================================

t = Tree()
cust = Custodian(t.root, install_handlers=False)
cust.capture([t.kept])
runs = stale_runs(t.root)
check("11 capture() writes a journal BEFORE the caller may mutate",
      len(runs) == 1, runs[0].name if runs else "-")
journal_blob = (runs[0] / "blobs" / "0000.bin").read_bytes() if runs else b""
check("11 the journal holds the ORIGINAL bytes",
      journal_blob == t.before[t.kept], "%d bytes" % len(journal_blob))
t.kept.write_bytes(b"DAMAGED")
restored, failed = recover(runs[0])
check("11 recover() repairs from the journal alone",
      t.intact() and not failed, "restored %d, failed %s" % (len(restored), failed))
discard(runs[0])
cust.close()
t.close()

# =============================================================================
section("4. A CORRUPT JOURNAL IS NOT A REPAIR")
# =============================================================================

t = Tree()
cust = Custodian(t.root, install_handlers=False)
cust.capture([t.kept])
run_dir = stale_runs(t.root)[0]
(run_dir / "blobs" / "0000.bin").write_bytes(b"not what was captured")
t.kept.write_bytes(b"DAMAGED")
restored, failed = recover(run_dir)
check("12 a tampered journal blob is REFUSED, not written",
      not restored and len(failed) == 1 and "corrupt" in failed[0],
      failed[0].split(": ")[-1] if failed else "-")
check("12 the damaged file is left damaged rather than silently 'repaired'",
      t.kept.read_bytes() == b"DAMAGED", "unchanged by the failed recovery")
discard(run_dir)
cust.close()
t.close()

# =============================================================================
section("5. THE UNAVOIDABLE CASE -- a real hard kill of a real child process")
# =============================================================================

# This is the one thing no in-process handler can cover, and the only honest
# way to test it is to actually do it.  The child runs against a DISPOSABLE
# tree, never the repository.
t = Tree()
child = """
import pathlib, sys, time
sys.path.insert(0, %r)
from oral_custody import Custodian
root = pathlib.Path(%r)
cust = Custodian(root, install_handlers=False)
target = root / "kept.html"
with cust.guard([target]):
    target.write_bytes(b"KILLED MID-MUTATION")
    print("mutated", flush=True)
    time.sleep(60)
""" % (str(HERE), str(t.root))

script = t.root / "_child.py"
script.write_text(child, encoding="utf-8")
proc = subprocess.Popen([sys.executable, str(script)],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
line = proc.stdout.readline().decode("utf-8", "replace").strip()
check("13 the child applied its mutation", line == "mutated", "child said %r" % line)
proc.kill()                       # TerminateProcess / SIGKILL: no Python runs
proc.wait(timeout=30)
time.sleep(0.2)

check("13 a hard kill leaves the damage -- as documented, NOT solved in-process",
      t.kept.read_bytes() == b"KILLED MID-MUTATION",
      "no finally, no atexit, no handler ran")

runs = stale_runs(t.root)
check("13 but the journal survives the kill", len(runs) == 1,
      runs[0].name if runs else "-")
restored, failed = recover(runs[0])
check("13 and the tree is fully recoverable from it",
      t.intact() and not failed, "restored %s" % [pathlib.Path(r).name for r in restored])
discard(runs[0])
check("13 recovery clears the stale journal", not stale_runs(t.root), "none left")
t.close()

# =============================================================================
section("6. THE LIVE RUNNER REFUSES TO START ON AN UNRECOVERED JOURNAL")
# =============================================================================

import mutate_corrections as MC                                    # noqa: E402

check("14 the real suite has no unrecovered journal right now",
      MC.refuse_on_stale_journal() is None, "clean")

# Plant one in the REAL repo root -- a journal directory only, no mutation, no
# file touched -- and prove the runner fails closed rather than mutating on top
# of it.  Removed immediately afterwards, and the section asserts it is gone.
planted = Custodian(MC.REPO, name="pass3-refusal-control", install_handlers=False)
sentinel = MC.REPO / JOURNAL_DIRNAME / "sentinel-never-mutated.txt"
planted.capture([sentinel])        # a file that does not exist: nothing to damage
rc = MC.refuse_on_stale_journal()
check("14 with a journal present, the runner REFUSES (exit 2)", rc == 2, "rc=%s" % rc)
discard(planted.run_dir)
planted.close()
check("14 the control journal is gone again",
      MC.refuse_on_stale_journal() is None, "clean")
check("14 the sentinel was never created", not sentinel.is_file(), "absent")

jroot = MC.REPO / JOURNAL_DIRNAME
if jroot.is_dir():
    leftover = [p.name for p in jroot.iterdir() if p.name != ".gitignore"]
    check("14 nothing left in the repo journal but its self-ignore",
          not leftover, "contents=%s" % (leftover or "['.gitignore']"))
    check("14 the journal directory ignores itself",
          (jroot / ".gitignore").read_text(encoding="utf-8").strip() == "*",
          "gitignore='*'")

print()
print("=" * 100)
print("%d checks, %d FAIL" % (COUNT[0], len(FAILURES)))
if FAILURES:
    for name in FAILURES:
        print("  FAILED: %s" % name)
print("=" * 100)
sys.exit(1 if FAILURES else 0)
