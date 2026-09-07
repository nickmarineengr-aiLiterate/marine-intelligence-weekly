#!/usr/bin/env python3
"""One-screen status probe for the Pass-2 terminal-closure run.

Exists so a periodic status report costs one cheap command instead of
re-deriving the state each time. It is READ-ONLY: it never writes to the
repository, never runs a validator or a mutator, and is therefore safe to call
while a mutation suite is live -- which is the one thing this batch has already
got wrong twice.

Reports, in order: which long job is running, how long it has been running,
whether the working tree is clean, and the last recorded result of each gate.
"""
from __future__ import annotations

import datetime as _dt
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
SCRATCH = pathlib.Path(
    r"C:\Users\User\AppData\Local\Temp\claude\F--RulesApp"
    r"\9a9ff755-957f-4796-8f2e-27a6586b6e9f\scratchpad")

#: (label, file, regex that lifts the headline out of a finished log)
JOBS = [
    ("mutation suite", "mut_tc.txt",
     r"(\d+ mutations, \d+ escape\(s\), \d+ no-op\(s\), \d+ crash\(es\))"),
    ("corpus validator", "vc_tc.txt", r"(\d+ checks, \d+ FAIL)"),
]


def _age(p: pathlib.Path) -> str:
    d = _dt.datetime.now() - _dt.datetime.fromtimestamp(p.stat().st_mtime)
    return "%dm%02ds ago" % (d.seconds // 60, d.seconds % 60)


def main() -> int:
    print("PASS-2 TERMINAL CLOSURE -- status at %s"
          % _dt.datetime.now().strftime("%H:%M:%S"))
    print("=" * 52)

    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                          cwd=REPO, capture_output=True).stdout.decode().strip()
    dirty = subprocess.run(["git", "status", "--porcelain"],
                           cwd=REPO, capture_output=True).stdout.decode().splitlines()
    dirty = [d for d in dirty if d.strip()]
    print("HEAD %s   working tree: %s"
          % (head, "clean" if not dirty else "%d file(s) modified" % len(dirty)))
    for d in dirty[:6]:
        print("   " + d.strip())

    print()
    for label, name, pat in JOBS:
        f = SCRATCH / name
        if not f.is_file():
            print("%-18s NOT STARTED" % label)
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        m = re.search(pat, text)
        if m:
            print("%-18s FINISHED  %s   (%s)" % (label, m.group(1), _age(f)))
            for line in text.splitlines():
                if line.startswith(("  ESCAPE", "  CRASH", "  NO-OP", "FAIL")):
                    print("      " + line.strip()[:100])
        else:
            tail = [l for l in text.splitlines() if l.strip()][-1:] or ["(no output yet)"]
            print("%-18s RUNNING   last: %s   (%s)"
                  % (label, tail[0][:60], _age(f)))

    print()
    print("REMINDER: no git add / commit / validator / digest sweep while the")
    print("mutation suite is RUNNING. Serial only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
