#!/usr/bin/env python3
"""
Validate every post-release correction record against the live corpus.

WHY THIS GATE EXISTS
--------------------

The batch validators answer ONE question about a card: "does some authorised
record own it?".  That question is anchor-level by design -- a batch that
enriches QB1_A#q18 owns that card, and a later batch touching it again is
legitimate.

For a correction that answer alone is too weak.  Once
`CORR-FAIR-TREATMENT-20260821` declares QB1_A#q25, every historical guard stops
objecting to that card FOREVER, including to an edit nobody ever authorised.
Delegation would have become a permanent hole punched through eleven guards.

So the correction record also PINS the post-correction state of each card it
declares, and this gate compares those pins to the live pages.  The two halves
are deliberately different questions:

    delegation (batch validators)  "this card was legitimately edited"
    pinning    (this gate)         "and it is still exactly what was authorised"

Neither subsumes the other, and a correction is only fully authorised when both
hold.

THE WINDOW CHECK
----------------
`no_undeclared_change_in_window` re-asks the corpus-wide authorisation question
over this correction's own window -- baseline_commit to the working tree -- and
requires every card that moved in it to be owned by SOME authorisation record,
batch or correction.  That is what stops a seventh card riding along inside a
correction commit: declaring six cards does not license a change to a card the
record never names.

It is scoped by the record's own baseline rather than by a fixed commit, so it
does not expire when the next batch ships: that batch's cards are owned by that
batch's manifest, and the union is read from disk, not hardcoded.

DIALECT
-------
Prints the repo's standard batch-validator summary, "<N> checks, <M> FAIL", so
`run_oral_release.py` classifies it with the shared validator parser rather than
by exit code alone.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oral_manifest import (                                     # noqa: E402
    CORRECTION_MANIFEST_GLOB, audit_correction_manifest,
    authorisation_manifest_paths, action_id_of)
from validate_batch_b import card_digests                       # noqa: E402
from oral_supersession import resolve_authorised_card_state    # noqa: E402

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB_DIR = REPO / "meoclass1"
KNOWN_TRAPS = REPO / "meoclass1" / "known_traps.md"

_checks = 0
_failed: list[str] = []


def report(name: str, ok: bool, detail: str = "") -> None:
    global _checks
    _checks += 1
    if not ok:
        _failed.append(name)
    print("%-5s %-42s %s" % ("PASS" if ok else "FAIL", name, detail))


def git_show(ref: str, rel: str):
    """File text at a ref, or None when the path does not exist there."""
    out = subprocess.run(["git", "show", "%s:%s" % (ref, rel.replace("\\", "/"))],
                         cwd=str(REPO), capture_output=True, check=False)
    return out.stdout.decode("utf-8") if out.returncode == 0 else None


def live_text(rel: str):
    p = REPO / rel
    # newline="" so the digest sees the file's real bytes; card_digests
    # LF-normalises internally, which is what makes these pins survive a CRLF
    # working tree.
    return p.read_text(encoding="utf-8", newline="") if p.is_file() else None


def tracked_card_pages() -> list[str]:
    """Every page the window check watches: the QB corpus plus any page a
    correction record declares (which is how SQ/ copies get watched)."""
    pages = {("meoclass1/" + p.name) for p in QB_DIR.glob("QB*.html")}
    for path in HERE.glob(CORRECTION_MANIFEST_GLOB):
        for card in json.loads(path.read_text(encoding="utf-8")).get("cards", []):
            if card.get("path"):
                pages.add(str(card["path"]))
    return sorted(pages)


def owned_anchors() -> dict:
    """file -> set(anchor) owned by ANY authorisation record on disk."""
    owned: dict[str, set] = {}
    for path in authorisation_manifest_paths(HERE):
        for card in json.loads(path.read_text(encoding="utf-8")).get("cards", []):
            if card.get("file") and card.get("anchor"):
                owned.setdefault(card["file"], set()).add(card["anchor"])
    return owned


def validate(manifest_path: Path) -> None:
    name = manifest_path.name
    print("\n=== %s ===" % name)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cards = manifest.get("cards") or []

    # ---- 1. schema ---------------------------------------------------------
    schema_bad = [f.check for f in audit_correction_manifest(manifest_path)
                  if not f.ok]
    report("manifest_schema_contract", not schema_bad,
           "violations=%s" % (schema_bad or "none"))

    if manifest.get("status") == "SUPERSEDED":
        report("superseded_record_not_enforced", True,
               "status=SUPERSEDED; pins are history, not live expectations")
        return

    baseline = manifest.get("baseline_commit")
    commits = manifest.get("governing_commits") or []

    # ---- 2. the declared cards still exist ---------------------------------
    missing = []
    for card in cards:
        text = live_text(card["path"])
        if text is None or card["anchor"] not in card_digests(text):
            missing.append("%s#%s" % (card["path"], card["anchor"]))
    report("declared_cards_present_live", not missing,
           "missing=%s" % (missing or "none"))

    # ---- 3. THE PIN: live state is exactly the authorised state ------------
    drifted = []
    for card in cards:
        text = live_text(card["path"])
        if text is None:
            continue
        live = card_digests(text).get(card["anchor"])
        # A correction record is itself supersedable. Once a later authorised
        # record declares descent from this post state, the claim under test
        # becomes "my authorised state is the ancestor of what is live", which
        # still fails on any unmanifested edit. Absent such a declaration this
        # is byte-for-byte the original pin.
        res = resolve_authorised_card_state(
            manifest=manifest_path.name, action_id=action_id_of(card),
            file=card["file"], anchor=card["anchor"],
            pinned_post_digest=card["post_edit_digest"],
            live_digest=live, directory=manifest_path.parent)
        if not res.ok:
            drifted.append("%s#%s (live %s, authorised %s) %s"
                           % (card["path"], card["anchor"],
                              (live or "-")[:10], card["post_edit_digest"][:10],
                              res.describe()))
    report("live_matches_authorised_post_state", not drifted,
           "drifted=%s" % (drifted or "none"))

    # ---- 4. the record describes a transition that really happened ---------
    wrong_pre = []
    if baseline:
        for card in cards:
            text = git_show(baseline, card["path"])
            was = card_digests(text).get(card["anchor"]) if text else None
            if was != card["pre_edit_digest"]:
                wrong_pre.append("%s#%s (baseline %s, declared %s)"
                                 % (card["path"], card["anchor"],
                                    (was or "-")[:10], card["pre_edit_digest"][:10]))
    report("pre_edit_digests_match_baseline", bool(baseline) and not wrong_pre,
           "baseline=%s mismatched=%s" % (baseline or "-", wrong_pre or "none"))

    wrong_post = []
    if commits:
        last = commits[-1]
        for card in cards:
            text = git_show(last, card["path"])
            got = card_digests(text).get(card["anchor"]) if text else None
            if got != card["post_edit_digest"]:
                wrong_post.append("%s#%s" % (card["path"], card["anchor"]))
    report("governing_commits_produced_post_state", bool(commits) and not wrong_post,
           "last=%s mismatched=%s" % (commits[-1] if commits else "-",
                                      wrong_post or "none"))

    # ---- 5. nothing undeclared moved inside this record's window ----------
    owned = owned_anchors()
    undeclared = []
    if baseline:
        for rel in tracked_card_pages():
            before = git_show(baseline, rel)
            after = live_text(rel)
            if before is None or after is None:
                continue
            b, a = card_digests(before), card_digests(after)
            fname = rel.rsplit("/", 1)[-1]
            for anchor in sorted(set(b) | set(a)):
                if b.get(anchor) == a.get(anchor):
                    continue
                if anchor in owned.get(fname, set()):
                    continue
                undeclared.append("%s#%s" % (rel, anchor))
    report("no_undeclared_change_in_window", bool(baseline) and not undeclared,
           "window=%s..worktree undeclared=%s" % (baseline or "-",
                                                  undeclared or "none"))

    # ---- 6. the authorisation source actually carries the entries ---------
    entries = manifest.get("known_traps_entries") or []
    traps = KNOWN_TRAPS.read_text(encoding="utf-8") if KNOWN_TRAPS.is_file() else ""
    headings = {int(m) for m in re.findall(r"^###\s+(\d+)\.", traps, re.M)}
    absent = sorted(e for e in entries if e not in headings)
    report("known_traps_entries_exist", bool(entries) and not absent,
           "declared=%s absent=%s" % (entries or "none", absent or "none"))

    # ---- 7. declared non-card artefacts exist -----------------------------
    gone = [a.get("path") for a in (manifest.get("artefacts") or [])
            if not (REPO / str(a.get("path"))).is_file()]
    report("declared_artefacts_exist", not gone, "missing=%s" % (gone or "none"))


def tracked_correction_records() -> list[str]:
    """Correction records git knows about, whatever the working tree holds."""
    out = subprocess.run(
        ["git", "ls-files", "tools/oral/%s" % CORRECTION_MANIFEST_GLOB],
        cwd=str(REPO), capture_output=True, check=False)
    if out.returncode != 0:
        return []
    return sorted(line.rsplit("/", 1)[-1]
                  for line in out.stdout.decode("utf-8").split("\n") if line.strip())


def main() -> int:
    records = sorted(HERE.glob(CORRECTION_MANIFEST_GLOB))
    print("post-release correction records: %d" % len(records))

    # FAIL CLOSED.
    #
    # Deleting a correction record does two things at once: it revokes the
    # delegation the batch guards rely on, and -- if this gate simply iterated
    # whatever happens to be on disk -- it also silences the only gate that
    # would have noticed. Zero records would then read as zero problems.
    #
    # So the expectation comes from git, not from the directory listing. A
    # record that is tracked but absent from the working tree is a revoked
    # authorisation, and it fails here as well as in every historical guard.
    on_disk = {p.name for p in records}
    tracked = tracked_correction_records()
    vanished = sorted(set(tracked) - on_disk)
    report("tracked_correction_records_present", not vanished,
           "tracked=%d on_disk=%d vanished=%s"
           % (len(tracked), len(on_disk), vanished or "none"))

    for path in records:
        validate(path)

    print("\n%d checks, %d FAIL" % (_checks, len(_failed)))
    if _failed:
        print("failed: %s" % ", ".join(sorted(set(_failed))))
    return 1 if _failed else 0


if __name__ == "__main__":
    sys.exit(main())
