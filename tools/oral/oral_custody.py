#!/usr/bin/env python3
"""
Durable byte-custody for mutation suites.

WHY THIS MODULE EXISTS
----------------------

A mutation suite deliberately damages the working tree and then repairs it.
That is the only way to prove a guard catches what it claims to catch: you have
to break the thing and watch the guard go red.  The repair is therefore not
housekeeping -- it is half the contract, and it has to hold under every exit
path the suite can take.

``mutate_corrections.py`` did not hold.  Its preflight loop restored inside
``except Exception`` and again after the happy path, but not in a ``finally``,
so ``KeyboardInterrupt`` and ``SystemExit`` -- which are ``BaseException``, not
``Exception`` -- walked straight past it.  Its probe phase spawns a validator
subprocess that runs for tens of seconds, and a Ctrl-C landing in that window
killed the parent before restore.  On 4 September 2026 that left a HISTORICAL
correction manifest deleted, a digest zeroed and QB HTML mutated, and the
worktree was repaired by hand.  A governed mutation runner that needs manual
repair after an interruption is not governed.

THE INVARIANT
-------------

    Whether the suite finishes normally, fails, raises, is interrupted or is
    terminated at the Python level, every mutation target is restored to its
    exact original bytes before control returns -- and the restoration is
    VERIFIED by reading the file back, never assumed.

Three layers, each covering what the one above cannot:

    1. ``guard()``            ``try/finally`` around one mutation.  Covers
                              return, exception, KeyboardInterrupt, SystemExit.
    2. signal + atexit        Covers SIGINT/SIGTERM arriving while a probe
                              subprocess is running, and interpreter shutdown
                              on a path that skipped the finally.
    3. the on-disk journal    Covers what no in-process handler can: SIGKILL,
                              a power loss, a console window closed with the
                              X button.  Original bytes are on disk BEFORE the
                              mutation is applied, so the NEXT run can restore
                              them.

WHAT IS NOT SOLVED, AND IS NOT PRETENDED TO BE
----------------------------------------------

A process killed with a non-catchable signal (``SIGKILL``, Windows
``TerminateProcess``, which is what Task Manager's "End task" and a closed
console window issue) executes no Python at all.  No ``finally``, no
``atexit``, no handler.  Layer 3 is the honest answer to that case: it does not
prevent the damage, it makes the damage RECOVERABLE and, crucially, makes the
next run REFUSE TO START until it has been recovered.  Silently mutating on top
of an unrecovered journal is how a hand-repair becomes a wrong commit.

The journal directory ignores itself (it writes its own ``.gitignore``
containing ``*``), so custody state can never be committed and the repo's
``.gitignore`` needs no edit.
"""

from __future__ import annotations

import atexit
import hashlib
import json
import os
import pathlib
import shutil
import signal
import time

JOURNAL_DIRNAME = ".mutation-journal"
MANIFEST_NAME = "journal.json"
BLOB_DIRNAME = "blobs"


class CustodyError(RuntimeError):
    """Restoration could not be verified.

    Deliberately its own type.  A suite must be able to distinguish "the guard
    I was testing behaved unexpectedly" (a finding) from "I could not put the
    repository back" (a hard stop), and an untyped RuntimeError makes those two
    look the same to an ``except``.
    """


def _sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def _read(path: pathlib.Path):
    """Original bytes, or None for 'this file did not exist'.

    None is a real state, not an error state: mutation A1 DELETES a correction
    manifest, so 'absent' is something custody has to be able to restore TO as
    well as restore FROM.
    """
    return path.read_bytes() if path.is_file() else None


# ------------------------------------------------------------------ journal


def _journal_root(root) -> pathlib.Path:
    return pathlib.Path(root) / JOURNAL_DIRNAME


def stale_runs(root) -> list:
    """Every journal directory left behind by a run that did not close.

    A closed run deletes its own directory, so anything still here is either a
    run in progress or the residue of a kill.  The caller decides which.
    """
    jroot = _journal_root(root)
    if not jroot.is_dir():
        return []
    return sorted(p for p in jroot.iterdir()
                  if p.is_dir() and (p / MANIFEST_NAME).is_file())


def recover(run_dir) -> tuple:
    """Restore one journal directory's files to their recorded original bytes.

    Returns ``(restored, failed)``.  Verification is a read-back compare, the
    same as the live path -- a recovery that reports success without reading
    the file back is exactly the kind of unverified claim this layer exists to
    stop.
    """
    run_dir = pathlib.Path(run_dir)
    entries = json.loads((run_dir / MANIFEST_NAME).read_text(encoding="utf-8"))
    restored, failed = [], []
    for entry in entries["files"]:
        path = pathlib.Path(entry["path"])
        if entry["blob"] is None:
            try:
                if path.is_file():
                    path.unlink()
                restored.append(str(path))
            except OSError as exc:
                failed.append("%s: %s" % (path, exc))
            continue
        blob_path = run_dir / BLOB_DIRNAME / entry["blob"]
        try:
            blob = blob_path.read_bytes()
        except OSError as exc:
            failed.append("%s: journal blob unreadable: %s" % (path, exc))
            continue
        if _sha256(blob) != entry["sha256"]:
            failed.append("%s: journal blob is itself corrupt" % path)
            continue
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(blob)
        except OSError as exc:
            failed.append("%s: %s" % (path, exc))
            continue
        if path.read_bytes() != blob:
            failed.append("%s: wrote but read back different bytes" % path)
            continue
        restored.append(str(path))
    return restored, failed


def discard(run_dir) -> None:
    shutil.rmtree(pathlib.Path(run_dir), ignore_errors=True)


# --------------------------------------------------------------- custodian


class Custodian:
    """Byte-exact, journalled custody of every file a suite mutates.

    Restores from bytes THIS OBJECT read, never from git.  ``git checkout <ref>
    -- <file>`` destroys uncommitted work, which has already cost real edits in
    this repository, so it is not an available repair.
    """

    def __init__(self, root, name="mutation", install_handlers=True):
        self.root = pathlib.Path(root).resolve()
        self.run_dir = (_journal_root(self.root)
                        / ("%s-%s-%d" % (name,
                                         time.strftime("%Y%m%dT%H%M%S"),
                                         os.getpid())))
        self._entries = {}          # resolved path -> {"blob", "sha256", "file"}
        self._order = []
        self._closed = False
        self._journal_started = False
        self._install = install_handlers
        self._prev_handlers = {}
        self._atexit_registered = False

    # -------------------------------------------------------- journal I/O

    def _start_journal(self) -> None:
        if self._journal_started:
            return
        jroot = _journal_root(self.root)
        jroot.mkdir(parents=True, exist_ok=True)
        # The journal ignores itself.  Custody state is never a repo change.
        gitignore = jroot / ".gitignore"
        if not gitignore.is_file():
            gitignore.write_text("*\n", encoding="utf-8")
        (self.run_dir / BLOB_DIRNAME).mkdir(parents=True, exist_ok=True)
        self._journal_started = True

    def _write_journal(self) -> None:
        """Rewrite the journal manifest atomically.

        Atomic because the whole point of the journal is that it survives a
        kill: a manifest half-written at the moment of death is worse than no
        manifest, since recovery would restore some files and silently skip
        others.  Write-then-replace makes the reader see either the old
        complete manifest or the new complete one.
        """
        payload = {"root": str(self.root), "files": [
            {"path": str(p),
             "blob": self._entries[p]["file"],
             "sha256": self._entries[p]["sha256"]}
            for p in self._order]}
        tmp = self.run_dir / (MANIFEST_NAME + ".tmp")
        tmp.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
        os.replace(str(tmp), str(self.run_dir / MANIFEST_NAME))

    # ----------------------------------------------------------- handlers

    def _install_handlers(self) -> None:
        if not self._install or self._prev_handlers:
            return
        for signame in ("SIGINT", "SIGTERM", "SIGBREAK"):
            sig = getattr(signal, signame, None)
            if sig is None:
                continue
            try:
                self._prev_handlers[sig] = signal.signal(sig, self._on_signal)
            except (ValueError, OSError):
                # Not the main thread, or the platform refuses the handler.
                # Layers 1 and 3 still apply; losing layer 2 is not fatal.
                pass
        if not self._atexit_registered:
            atexit.register(self._on_exit)
            self._atexit_registered = True

    def _on_signal(self, signum, frame):
        print("\n[custody] signal %s -- restoring %d file(s) before exit"
              % (signum, len(self._entries)))
        bad = self.restore_all()
        if bad:
            print("[custody] RESTORE FAILED: %s" % bad)
            os._exit(2)
        self.close()
        os._exit(130)

    def _on_exit(self):
        # Belt and braces for an exit path that skipped every finally.  Silent
        # when there is nothing to do, loud when there was.
        if self._closed or not self._entries:
            return
        bad = self.restore_all()
        print("[custody] atexit restored %d file(s)%s"
              % (len(self._entries), "; FAILED: %s" % bad if bad else ""))
        self.close()

    # ------------------------------------------------------------ capture

    def capture(self, paths) -> None:
        """Record the ORIGINAL bytes of each path, and journal them to disk.

        Idempotent per path: the first capture wins.  A path captured twice
        must still restore to the state it had before the FIRST mutation, not
        to whatever an intermediate mutation left.
        """
        fresh = []
        for raw in paths:
            path = pathlib.Path(raw).resolve()
            if path in self._entries:
                continue
            blob = _read(path)
            fresh.append((path, blob))
        if not fresh:
            return
        self._start_journal()
        for path, blob in fresh:
            if blob is None:
                self._entries[path] = {"blob": None, "sha256": None, "file": None}
            else:
                name = "%04d.bin" % len(self._order)
                (self.run_dir / BLOB_DIRNAME / name).write_bytes(blob)
                self._entries[path] = {"blob": blob, "sha256": _sha256(blob),
                                       "file": name}
            self._order.append(path)
        # Journal is complete on disk BEFORE the caller is allowed to mutate.
        self._write_journal()
        self._install_handlers()

    # ------------------------------------------------------------ restore

    def _restore_one(self, path) -> str | None:
        entry = self._entries[path]
        blob = entry["blob"]
        try:
            if blob is None:
                if path.is_file():
                    path.unlink()
                return None
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(blob)
        except OSError as exc:
            return "%s: %s" % (path, exc)
        # Verified, not assumed.
        if _read(path) != blob:
            return "%s: wrote but read back different bytes" % path
        return None

    def original(self, path):
        """The bytes captured for this path (None = it did not exist).

        Exposed because a preflight has to answer "did this mutation actually
        change anything?", and the only trustworthy 'before' is the one custody
        already holds -- re-reading the file to get a 'before' would read the
        MUTATED bytes if the caller got the order wrong.
        """
        return self._entries[pathlib.Path(path).resolve()]["blob"]

    def restore(self, paths) -> list:
        bad = []
        for raw in paths:
            path = pathlib.Path(raw).resolve()
            if path not in self._entries:
                bad.append("%s: never captured" % path)
                continue
            problem = self._restore_one(path)
            if problem:
                bad.append(problem)
        return bad

    def restore_all(self) -> list:
        return [p for p in (self._restore_one(path) for path in self._order) if p]

    def verify_pristine(self) -> list:
        """Every captured path is byte-identical to what it was at capture.

        The suite's closing assertion.  Restoring each mutation as it goes and
        never checking the aggregate is how a suite reports success on a tree
        it has quietly left dirty.
        """
        drift = []
        for path in self._order:
            want = self._entries[path]["blob"]
            got = _read(path)
            if got != want:
                drift.append("%s: %s" % (
                    path,
                    "should not exist but does" if want is None else
                    "missing" if got is None else
                    "%d byte(s) now, %d at capture" % (len(got), len(want))))
        return drift

    # -------------------------------------------------------------- guard

    class _Guard:
        def __init__(self, custodian, paths):
            self.custodian = custodian
            self.paths = list(paths)

        def __enter__(self):
            self.custodian.capture(self.paths)
            return self

        def __exit__(self, exc_type, exc, tb):
            # Runs for return, exception, KeyboardInterrupt and SystemExit
            # alike -- the three that walked past the old except-Exception.
            bad = self.custodian.restore(self.paths)
            if bad:
                raise CustodyError("restore verification failed: %s" % bad)
            return False        # never swallow the original exception

    def guard(self, paths):
        """Mutate inside this and the files come back, whatever happens."""
        return self._Guard(self, paths)

    # -------------------------------------------------------------- close

    def close(self) -> None:
        """Drop the journal.  Only legitimate once the tree is pristine."""
        if self._closed:
            return
        self._closed = True
        for sig, prev in self._prev_handlers.items():
            try:
                signal.signal(sig, prev)
            except (ValueError, OSError):
                pass
        self._prev_handlers.clear()
        if self._journal_started:
            discard(self.run_dir)
