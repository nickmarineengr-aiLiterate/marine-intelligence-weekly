#!/usr/bin/env python3
"""
Byte-level safety helpers shared by the Oral release toolchain.

Three lessons from production batches E1, E5 and E6 live here as code:

1. CONTROL BYTES.  E1 lost a regex ``\\b`` to a real 0x08 backspace byte and E5
   lost a ``\\1`` backreference to a real 0x01 SOH byte, because the source was
   authored through a shell heredoc that consumed the backslash and left the
   escape's *value*.  E6 then reproduced BOTH bytes inside the handoff paragraph
   that described them.  The class is confirmed in three forms across three
   sessions, so it is checked mechanically rather than remembered.

   Rule: author anything containing a backslash with a file writer, never
   through a shell heredoc -- and scan prose artefacts, not only executable
   ones.  A handoff is release evidence; a handoff carrying hidden control
   bytes is corrupted evidence.

2. EXPLICIT UTF-8.  Windows defaults text I/O to cp1252.  ``subprocess(text=True)``
   decoding cp1252 once manufactured 450 false diffs in an oral gate.  Every read
   and write here names its encoding.

3. LINE ENDINGS.  A working copy may hold CRLF while the git blob holds LF.  In
   E1 that mismatch manufactured 57 phantom insert opcodes and invalidated an
   additivity proof.  Digest checks that must see exact bytes keep them; text
   comparisons normalise first, and say which contract they used.
"""

from __future__ import annotations

import pathlib
from typing import Iterable, NamedTuple

# TAB, LF and CR are ordinary in source, JSON and prose.  Every other C0
# character (and DEL) is unexpected and is treated as corruption.
ALLOWED_CONTROL_BYTES = frozenset({0x09, 0x0A, 0x0D})
_C0_RANGE = frozenset(range(0x00, 0x20)) | {0x7F}
FORBIDDEN_CONTROL_BYTES = frozenset(_C0_RANGE - ALLOWED_CONTROL_BYTES)


class ControlByteHit(NamedTuple):
    """One forbidden control byte, located precisely enough to repair."""

    path: str
    offset: int
    byte: int
    line: int
    context: str

    def describe(self) -> str:
        return (
            "%s: 0x%02X at offset %d (line %d) -- %r"
            % (self.path, self.byte, self.offset, self.line, self.context)
        )


def read_text(path) -> str:
    """Read a file as UTF-8.  Never inherit the platform's cp1252 default."""
    return pathlib.Path(path).read_text(encoding="utf-8")


def write_text(path, text: str) -> None:
    """Write a file as UTF-8 with LF endings, creating parents as needed.

    ``newline=""`` stops Python translating LF to CRLF on Windows, so what the
    caller composed is what lands on disk and what git will hash.
    """
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def normalise_eol(text: str) -> str:
    """Collapse CRLF and lone CR to LF.

    This is the documented normalisation contract for *text* comparison --
    additivity proofs, diff opcodes, card-body equality.  Digest and byte-delta
    checks deliberately do NOT call this: there, exact bytes are the subject.
    """
    return text.replace("\r\n", "\n").replace("\r", "\n")


def scan_control_bytes(path) -> list[ControlByteHit]:
    """Return every forbidden control byte in one file.

    Works on raw bytes, so it is valid for Python, JSON, HTML and Markdown
    alike, and cannot be defeated by a decoding error.
    """
    p = pathlib.Path(path)
    raw = p.read_bytes()
    hits: list[ControlByteHit] = []
    for offset, byte in enumerate(raw):
        if byte not in FORBIDDEN_CONTROL_BYTES:
            continue
        line = raw.count(b"\n", 0, offset) + 1
        start = max(0, offset - 24)
        context = raw[start:offset + 24].decode("utf-8", errors="replace")
        hits.append(ControlByteHit(str(p), offset, byte, line, context))
    return hits


def scan_paths(paths: Iterable) -> list[ControlByteHit]:
    """Scan many files, skipping anything that does not exist."""
    hits: list[ControlByteHit] = []
    for path in paths:
        p = pathlib.Path(path)
        if p.is_file():
            hits.extend(scan_control_bytes(p))
    return hits


def assert_clean(paths: Iterable) -> None:
    """Raise if any file carries a forbidden control byte.

    Call this on every artefact a batch produces -- tooling, manifest AND
    handoff -- before committing.
    """
    hits = scan_paths(paths)
    if hits:
        raise AssertionError(
            "forbidden control bytes found:\n  "
            + "\n  ".join(h.describe() for h in hits)
        )


def _cli(argv: list[str]) -> int:
    import argparse

    ap = argparse.ArgumentParser(
        prog="oral_bytes",
        description="Scan files for forbidden C0 control bytes (TAB/LF/CR allowed).",
    )
    ap.add_argument("paths", nargs="+", help="files to scan")
    args = ap.parse_args(argv)

    hits = scan_paths(args.paths)
    for hit in hits:
        print(hit.describe())
    scanned = sum(1 for p in args.paths if pathlib.Path(p).is_file())
    print("scanned=%d hits=%d" % (scanned, len(hits)))
    return 1 if hits else 0


if __name__ == "__main__":
    import sys

    sys.exit(_cli(sys.argv[1:]))
