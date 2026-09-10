#!/usr/bin/env python3
"""Governance gate for non-card artefacts declared by correction records.

WHY THIS GATE EXISTS
--------------------

`validate_corrections.py` answers the same questions for governed artefacts
that it answers for q-cards, and it is the authority. But it answers them for
EVERY correction record on disk, and its window check runs `git show` over
every tracked card page per record -- minutes, not seconds.

A mutation suite has to run its probe once per mutation. A probe that takes
minutes is a probe nobody runs, and a governance mechanism whose mutations are
never exercised is the "negative guard that has never been shown to fire" this
toolchain has now been caught by twice.

So this is the narrow, fast probe over the artefact form only. It shares its
pins with the corpus gate by construction -- both call
`oral_manifest.audit_governed_artefacts_live`, which is the single place those
questions are asked -- so the two cannot drift into disagreeing.

WHAT IT ADDS ON TOP OF THE SHARED PINS
--------------------------------------
One check that is only answerable across records: a governed artefact path may
not also be claimed as a q-card page. The schema forbids an artefact ENTRY from
carrying `anchor` or `file`, which stops one record impersonating the other
shape. It cannot see two records disagreeing about what a page IS, and a page
owned as both would be pinned twice by two mechanisms with different rules.

FAIL CLOSED
-----------
Zero governed artefacts is a failure, not a clean run. The whole reason
`QB2_B_CheatSheet.html` shipped a rejected proposition is that nothing owned it,
and "nothing owns it" must never again read as "nothing to check".

DIALECT
-------
Prints the repo's standard "<N> checks, <M> FAIL" summary so
`run_oral_release.py` classifies it with the shared validator parser.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_manifest import (                                     # noqa: E402
    CORRECTION_MANIFEST_GLOB, audit_correction_manifest,
    audit_governed_artefacts_live, authorisation_manifest_paths)

_checks = 0
_failed: list[str] = []


def report(name: str, ok: bool, detail: str = "") -> None:
    global _checks
    _checks += 1
    if not ok:
        _failed.append(name)
    print("%-5s %-48s %s" % ("PASS" if ok else "FAIL", name, detail))


def records_declaring_artefacts() -> list[Path]:
    """Records that CARRY the key, not records whose list is non-empty.

    Found by mutation GA. Selecting on truthiness meant emptying
    `governed_artefacts` removed the record from this gate's iteration
    altogether, so the one check that exists to reject an empty declaration --
    `governed_artefacts_non_empty` -- was never reached. Withdrawing a page
    from governance silenced the gate that would have objected, which is the
    same shape as the fail-closed problem `validate_corrections.py` documents
    for deleted records.
    """
    out = []
    for path in sorted(HERE.glob(CORRECTION_MANIFEST_GLOB)):
        if "governed_artefacts" in json.loads(path.read_text(encoding="utf-8")):
            out.append(path)
    return out


def card_pages() -> set:
    """Every repo-relative page some record owns as a q-card page."""
    pages = set()
    for path in authorisation_manifest_paths(HERE):
        for card in json.loads(path.read_text(encoding="utf-8")).get("cards", []):
            if card.get("path"):
                pages.add(str(card["path"]).replace("\\", "/"))
    return pages


def main() -> int:
    records = records_declaring_artefacts()
    print("correction records declaring governed artefacts: %d" % len(records))

    report("governed_artefact_records_exist", bool(records),
           "%d record(s); zero is a failure, not a clean run" % len(records))

    owned_as_card = card_pages()
    for path in records:
        print("\n=== %s ===" % path.name)
        manifest = json.loads(path.read_text(encoding="utf-8"))

        # Reported one check per assertion rather than as a single aggregate.
        # A mutation suite must bind each mutation to the check that OWNS its
        # proposition, and an aggregate `manifest_schema_contract` would let
        # every governance mutation claim the same catch -- which proves that
        # something went red, not that the right thing did.
        for finding in audit_correction_manifest(path):
            report(finding.check, finding.ok, finding.detail)

        for finding in audit_governed_artefacts_live(path, REPO):
            report(finding.check, finding.ok, finding.detail)

        # A page cannot be governed as both an artefact and a q-card page:
        # two mechanisms with different pinning rules would each believe they
        # owned it, and each would be right about half of it.
        clash = sorted(str(a.get("path")).replace("\\", "/")
                       for a in (manifest.get("governed_artefacts") or [])
                       if str(a.get("path")).replace("\\", "/") in owned_as_card)
        report("artefact_paths_are_not_card_pages", not clash,
               "claimed_as_both=%s" % (clash or "none"))

    print("\n%d checks, %d FAIL" % (_checks, len(_failed)))
    if _failed:
        print("failed: %s" % ", ".join(sorted(set(_failed))))
    return 1 if _failed else 0


if __name__ == "__main__":
    sys.exit(main())
