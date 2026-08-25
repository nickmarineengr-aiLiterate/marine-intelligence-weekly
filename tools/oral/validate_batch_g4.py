"""Validate batch G4 - the fourth August 2026 fresh-intake production batch.

G4 is one action: AUG-0015, the ro-ro amendments ask, enriched into QB2_F#q3.
It makes the same claims as G1, G2 and G3 and is checked by the same contract,
so this file supplies the batch's paths and reuses that contract rather than
copying it.  A fourth drifting copy is how ten batch validators each grew their
own version of the sibling glob and then disagreed about it.

WHY THIS BATCH EXISTS SEPARATELY FROM G3
----------------------------------------
G3 froze thirteen asks and produced twelve.  AUG-0015 was declared
HELD_GOVERNANCE in `batch_g3_manifest.json` because its only sensible home,
QB2_F#q3, credited the ro-ro fire-safety package to the wrong resolution:
enriching that card would have produced one card stating two different
resolutions for one requirement.

The hold is discharged here rather than by editing G3's record, through the
`discharges_hold` contract.  G3's manifest still declares AUG-0015 as
HELD_GOVERNANCE and is not rewritten, because a manifest that can be edited to
close its own holds is a status board, not evidence - and "was that work ever
owed?" then stops being answerable from repository data.

WHY THIS FILE ADDS CHECKS INSTEAD OF ONLY DELEGATING
----------------------------------------------------
`discharges_hold` is LOAD_BEARING in the manifest schema, and the SHARED batch
contract does not read it - only `validate_batch_f1.py` does, and it reads it
for F1's own hold.  A LOAD_BEARING field that no validator opens is decoration,
and this repository has shipped decoration before: a half-wired digest pin, and
guards that pinned a corpus total and then passed vacuously the moment the
corpus grew.  So the four discharge propositions are asserted here, by name, so
`mutate_batch_g4.py` can require each mutation to trip the check that owns it.

The extra checks print in the shared batch dialect and are followed by a
COMBINED summary, which is the line the release runner reads: it takes the last
recognised summary in the output, so a failure here can never be hidden behind
the delegated pass.

NO FREEZE RECORD IS DECLARED
----------------------------
Deliberately.  `freeze_record` is checked conditionally, and its contract is
two-sided: every produced ask must be frozen, AND every frozen ask must be
produced or held.  AUG-0015 does appear in the G3 freeze, but pointing G4 at
that record would make G4 answerable for the twelve asks G3 produced, which G4
neither produced nor held.  A guard that a correct batch cannot satisfy is not
a guard.  The freeze provenance for this ask is asserted below instead, against
G3's record, where the claim is actually true.

  PYTHONIOENCODING=utf-8 python tools/oral/validate_batch_g4.py

Exit 0 all checks pass, 1 one or more failed.
"""
from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))

from oral_bytes import enable_utf8_stdio      # noqa: E402
import validate_batch_g1 as G                # noqa: E402

# Reach the shared UTF-8 stdio contract directly rather than inheriting it as
# a side effect of importing validate_batch_g1. The infra control scans this
# file's SOURCE, and a contract satisfied only at runtime by somebody else's
# import is exactly the kind of thing that stops being true after a refactor.
enable_utf8_stdio()

MANIFEST = HERE / "batch_g4_manifest.json"
HOLDER = HERE / "batch_g3_manifest.json"
AUDIT = REPO / "meoclass1" / "oral-intelligence" / "examiner-audit"
REVIEW = AUDIT / "AUGUST2026_BATCH_G4_REVIEW.json"
FREEZE = AUDIT / "AUGUST2026_BATCH_G3_FREEZE.json"

HELD_ASK = "AUG-0015"


def discharge_checks() -> list[tuple[str, bool, str]]:
    """The four propositions that make this batch a DISCHARGE, not a new ask."""
    out = []

    def check(name, ok, detail=""):
        out.append(("g4_" + name, bool(ok), detail))

    if not MANIFEST.is_file():
        check("discharge_declared", False, "manifest absent")
        return out
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    discharges = manifest.get("discharges_hold") or []

    # 1. The discharge is DECLARED, and names the ask and the record that held
    #    it. Without this the batch is indistinguishable from a batch that
    #    happened to produce an ask nobody remembers was owed.
    mine = [d for d in discharges
            if HELD_ASK in (d.get("source_occurrence_ids") or [])]
    check("discharge_declared", len(mine) == 1,
          "discharges_hold entries for %s: %d" % (HELD_ASK, len(mine)))
    entry = mine[0] if mine else {}

    # 2. The record it names really does hold that ask, with that status. A
    #    discharge pointing at a hold that was never declared is a claim about
    #    history that history does not support.
    held_ok, held_detail = False, "holder record unavailable"
    if HOLDER.is_file():
        holder = json.loads(HOLDER.read_text(encoding="utf-8"))
        held = [h for h in (holder.get("held_actions") or [])
                if HELD_ASK in (h.get("source_occurrence_ids") or [])]
        held_ok = (entry.get("held_by_manifest") == HOLDER.name
                   and len(held) == 1
                   and held[0].get("status") == entry.get("held_status"))
        held_detail = ("%s declares %d hold(s) for %s; status=%s, discharge says %s"
                       % (HOLDER.name, len(held), HELD_ASK,
                          held[0].get("status") if held else "-",
                          entry.get("held_status")))
    check("discharge_names_a_real_hold", held_ok, held_detail)

    # 3. The holding record is LEFT INTACT. This is the whole point of the
    #    contract: a hold closable by editing the manifest that declared it
    #    makes that manifest a mutable status board, and destroys the only
    #    place that says the work was owed.
    intact = False
    if HOLDER.is_file():
        holder = json.loads(HOLDER.read_text(encoding="utf-8"))
        held = [h for h in (holder.get("held_actions") or [])
                if HELD_ASK in (h.get("source_occurrence_ids") or [])]
        intact = bool(held) and held[0].get("status") in G_HELD_STATUSES
    check("holding_record_left_intact", intact,
          "%s still declares %s as held" % (HOLDER.name, HELD_ASK))

    # 4. The ask was frozen before it was ever answered - asserted against G3's
    #    freeze record directly, because this batch declares no freeze_record
    #    of its own and an unasserted provenance note is decoration.
    frozen = False
    frozen_detail = "freeze record unavailable"
    if FREEZE.is_file():
        freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
        rows = [a for a in (freeze.get("asks") or [])
                if a.get("occurrence_id") == HELD_ASK]
        frozen = len(rows) == 1
        frozen_detail = ("%s appears %d time(s) in %s"
                         % (HELD_ASK, len(rows), FREEZE.name))
    check("produced_ask_was_frozen_first", frozen, frozen_detail)

    return out


G_HELD_STATUSES = ("HELD_GOVERNANCE", "HELD_AUTHORITY", "HELD_TARGET")


def main() -> int:
    rc = G.main(manifest_path=MANIFEST, review_path=REVIEW, label="g4")
    delegated = list(G.results)

    extra = discharge_checks()
    print("\n--- batch G4: the discharge contract ---")
    for name, ok, detail in extra:
        print("%-5s %-52s %s" % ("PASS" if ok else "FAIL", name, detail))

    combined = delegated + extra
    failed = [n for n, ok, _ in combined if not ok]
    # The runner reads the LAST recognised summary, so this line - not the
    # delegated one above it - is what classifies the gate.
    print("\n%d PASS / %d FAIL" % (len(combined) - len(failed), len(failed)))
    if failed:
        print("failed: " + ", ".join(failed))
    return 1 if (failed or rc not in (0, 1)) else 0


if __name__ == "__main__":
    raise SystemExit(main())
