#!/usr/bin/env python3
"""Scope control: prove "corpus-wide" means the whole corpus.

WHY THIS FILE EXISTS
--------------------
Every Pass-1 census and gate enumerated `meoclass1/*.html`. That is 128 files.
The corpus is 224. Ninety-six files - the entire `oralnotes` study series, all
of `pastpapers`, and `rulesapp` - were outside every claim of "corpus-wide", and
an independent reviewer found BMP5 taught as current in that gap, with a
timeline row dating it to 2024.

The failure had no symptom. Every count the censuses produced was internally
consistent, every gate was green, and the reports read as complete. A scope
defect is invisible from inside its own scope, so it cannot be caught by any
check that shares the enumeration under test. It needs a control that knows what
the corpus IS, independently of what the censuses look at.

WHAT IS ASSERTED
----------------
1. the enumeration is recursive, and equals an independently-computed walk;
2. a file planted in a nested directory is SEEN (the mutation this exists for);
3. a top-level-only glob CANNOT satisfy the contract - stated as a live
   comparison, so the day someone reverts the glob this test goes red rather
   than passing vacuously;
4. every consumer that claims corpus-wide scope routes through the ONE
   enumeration function rather than re-globbing locally;
5. surface classification is total - every file lands in exactly one family,
   so no file can be silently policy-less.
"""
from __future__ import annotations

import os
import pathlib
import re
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB_ROOT = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from census_known_defect_families import (            # noqa: E402
    corpus_files, surface_family, SURFACE_FAMILIES)

FAILS: list[str] = []
CHECKS = 0


def report(check: str, ok: bool, detail: str = "") -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        FAILS.append(check)
    print("%-4s %-52s %s" % ("PASS" if ok else "FAIL", check, detail))


def independent_walk():
    """os.walk, not pathlib.rglob - a second implementation on purpose."""
    out = []
    for root, _dirs, files in os.walk(QB_ROOT):
        for f in files:
            if f.lower().endswith(".html"):
                out.append(pathlib.Path(root) / f)
    return sorted(out)


def main() -> int:
    enumerated = corpus_files()
    walked = independent_walk()

    report("enumeration_matches_an_independent_walk",
           {p.resolve() for p in enumerated} == {p.resolve() for p in walked},
           "%d files, two implementations agree" % len(enumerated))

    top_only = sorted(QB_ROOT.glob("*.html"))
    report("enumeration_is_strictly_larger_than_top_level",
           len(enumerated) > len(top_only),
           "recursive %d vs top-level %d (+%d)"
           % (len(enumerated), len(top_only), len(enumerated) - len(top_only)))

    # The contract, stated as a live comparison rather than a constant: the
    # day the glob is reverted, this goes red instead of passing vacuously.
    nested = [p for p in enumerated if p.parent != QB_ROOT]
    report("top_level_glob_cannot_satisfy_the_contract",
           bool(nested) and not any(p in set(top_only) for p in nested),
           "%d nested files a top-level glob would miss" % len(nested))

    subdirs = sorted({p.parent.relative_to(QB_ROOT).as_posix()
                      for p in nested})
    report("every_known_subtree_is_enumerated",
           {"oralnotes", "pastpapers", "rulesapp"} <= set(subdirs),
           "subtrees: %s" % ", ".join(subdirs))

    # A planted file must be SEEN - proved on a SYNTHETIC tree, never by
    # writing into the product corpus. The previous version planted a probe in
    # `meoclass1/oralnotes/` and removed it in a `finally:`, which does not run
    # when a process is killed; a killed gate has left product bytes behind in
    # this repository before, and a scope control is not worth that risk.
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        (root / "a.html").write_bytes(b"<html>top</html>")
        nested = root / "deep" / "deeper"
        nested.mkdir(parents=True)
        probe = nested / "_scope_probe.html"
        probe.write_bytes(b"<html>nested</html>")
        seen = {q.resolve() for q in corpus_files(root)}
        report("a_file_planted_in_a_nested_directory_is_seen",
               probe.resolve() in seen,
               "the enumeration recurses on any root it is given")
        report("the_planted_file_is_invisible_to_a_top_level_glob",
               probe.resolve() not in {q.resolve() for q in root.glob("*.html")},
               "which is precisely the Pass-1 blind spot")
    report("scope_control_writes_nothing_into_the_product_tree",
           not any(q.name.startswith("_scope_probe") for q in enumerated),
           "the probe lives in a temporary directory, not in meoclass1/")

    # Consumers must not re-glob. One enumeration, or they drift - and the
    # drift is what hides a scope defect.
    #
    # A top-level glob is legitimate in exactly one place: a check that
    # COMPARES it against the recursive enumeration to prove the difference.
    # That use must be marked ON THE LINE, so the exemption is auditable and
    # cannot be claimed silently. An unmarked local glob is the defect.
    EXEMPT = "# scope-control: comparison only"
    LOCAL_GLOB = re.compile(r'QB_ROOT\.glob\(\s*["\']\*\.html')
    offenders = []
    for f in sorted(HERE.glob("*.py")):
        if f.name in ("test_corpus_scope.py", "census_known_defect_families.py"):
            continue
        body = f.read_text(encoding="utf-8", errors="replace")
        if not ("corpus-wide" in body.lower() or "corpus_files" in body):
            continue
        for lineno, line in enumerate(body.splitlines(), 1):
            if LOCAL_GLOB.search(line) and EXEMPT not in line:
                offenders.append("%s:%d" % (f.name, lineno))
    report("no_corpus_wide_consumer_re_globs_locally", not offenders,
           str(offenders or "none"))

    # Classification must be total, and every family must be a declared policy.
    unknown = sorted({surface_family(p) for p in enumerated}
                     - set(SURFACE_FAMILIES))
    report("surface_classification_is_total", not unknown,
           "families in use: %s" % ", ".join(
               sorted({surface_family(p) for p in enumerated})))
    report("pastpapers_are_classified_as_sitting_anchored",
           all(surface_family(p) == "pastpapers"
               for p in enumerated if "pastpapers/" in p.as_posix()),
           "historical examiner wording is policy-protected")

    print("\n%d checks, %d FAIL" % (CHECKS, len(FAILS)))
    if FAILS:
        print("failed: " + ", ".join(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
