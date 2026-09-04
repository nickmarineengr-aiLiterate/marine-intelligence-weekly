#!/usr/bin/env python3
"""
Mutation suite for the post-release correction authorisation model.

WHAT THIS SUITE HAS TO PROVE
----------------------------

Adding `CORR-FAIR-TREATMENT-20260821` turned seven red batch validators green.
That is either a correct authorisation or a very effective way of switching
seven guards off, and nothing about the green output distinguishes the two.

So every mutation below attacks the delegation itself:

    remove the record        -> the historical guards must go red again
    corrupt its identity     -> the correction gate must reject it
    corrupt a target         -> delegation must not transfer
    corrupt a digest         -> the pin must reject it
    drop one declared card   -> only that card loses cover
    move a declared card     -> the pin must reject the new state
    move an UNdeclared card  -> still fails, record or no record

If any of these stays green, the model is suppressing drift rather than
authorising a correction, and the suite fails.

WHY THE PROBES ARE SPECIFIC CHECKS, NOT EXIT CODES
--------------------------------------------------
A validator that fails for the wrong reason is not evidence. Each mutation
names the check it must break, and a mutation that makes the probe fail on some
OTHER check counts as an ESCAPE, not a catch. E6's mutation L is the reason:
it corrupted a field nothing read, and the suite's coarse verdict said "caught"
because something else was failing anyway.

BATCH_B IS PROBED SEPARATELY ON PURPOSE
---------------------------------------
`pre_existing_cards_unchanged` is a generation-1 digest pin, a different code
path from generation-2's `only_authorised_cards_changed`. Mutation I edits a
batch-B-pinned card that NO record authorises and requires batch_b to still
fail, which is what shows the correction did not blanket-weaken that guard.

E6's line-ending debt is NOT touched here. Mutation J asserts it is still
failing for its own reason and is not being counted as correction success.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_bytes import read_text, write_text                    # noqa: E402
from oral_custody import (Custodian, CustodyError, discard,     # noqa: E402
                          recover, stale_runs)
from oral_manifest import authorisation_manifest_paths          # noqa: E402
from validate_batch_b import CARD_OPEN, card_digests, _balanced_end  # noqa: E402

MANIFEST = HERE / "correction_corr_fair_treatment_20260821_manifest.json"
MANIFEST_REL = "tools/oral/correction_corr_fair_treatment_20260821_manifest.json"

# Probe validators, chosen for coverage per unit of wall time:
#   batch_b   generation-1 digest pin      ~1s
#   batch_e4  generation-2 authorisation   ~19s   (an E1-E5 validator)
#   batch_e1  generation-2, the headline   ~64s   (run once)
#   batch_e6  the line-ending debt case    ~33s   (run once)
PROBES = {
    "batch_b": "validate_batch_b.py",
    "batch_e1": "validate_batch_e1.py",
    "batch_e4": "validate_batch_e4.py",
    "batch_e6": "validate_batch_e6.py",
    "corrections": "validate_corrections.py",
}

CARD_MARKER = "<!--mutation-probe-->"


# ------------------------------------------------------------------ helpers

def run_probe(key: str) -> tuple[int, set]:
    """Run one validator; return (exit code, set of FAILing check names)."""
    out = subprocess.run([sys.executable, str(HERE / PROBES[key])],
                         cwd=str(REPO), capture_output=True, check=False)
    text = (out.stdout + out.stderr).decode("utf-8", "replace")
    failing = set(re.findall(r"^FAIL\s+(\S+)", text, re.M))

    # validate_corrections rolls the whole schema audit into ONE check,
    # `manifest_schema_contract`, and names the violated sub-checks in its
    # detail as `violations=['a', 'b']`. Accepting the aggregate name alone
    # would let any schema corruption satisfy any schema mutation -- exactly
    # the coarse "something failed, call it caught" reading that let E6's
    # mutation L through. So the sub-check names are lifted out and matched
    # individually, keeping each mutation pinned to the check it must break.
    for payload in re.findall(r"violations=\[([^\]]*)\]", text):
        failing.update(re.findall(r"'([^']+)'", payload))
    return out.returncode, failing


def mutate_card(rel: str, anchor: str) -> None:
    """Change one card's bytes without changing what it says structurally."""
    path = REPO / rel
    text = read_text(path)
    for m in CARD_OPEN.finditer(text):
        got = re.search(r'\bid="([^"]+)"', m.group(0))
        if got and got.group(1) == anchor:
            write_text(path, text[:m.end()] + CARD_MARKER + text[m.end():])
            return
    raise AssertionError("card not found: %s#%s" % (rel, anchor))


def edit_manifest(mutate) -> None:
    data = json.loads(read_text(MANIFEST))
    mutate(data)
    write_text(MANIFEST, json.dumps(data, indent=2) + "\n")


def owned_anchors() -> dict:
    owned = {}
    for path in authorisation_manifest_paths(HERE):
        for card in json.loads(read_text(path)).get("cards", []):
            if card.get("file") and card.get("anchor"):
                owned.setdefault(card["file"], set()).add(card["anchor"])
    return owned


def pick_unowned_batch_b_card() -> tuple[str, str]:
    """A card batch B pins that NO authorisation record owns.

    Chosen at runtime rather than hardcoded: a hardcoded anchor silently stops
    testing anything the day some future record authorises that very card.
    """
    pins = json.loads(read_text(HERE / "batch_b_manifest.json")).get(
        "baseline_card_digests") or {}
    owned = owned_anchors()
    for fname in sorted(pins):
        for anchor in sorted(pins[fname]):
            if anchor not in owned.get(fname, set()):
                return "meoclass1/" + fname, anchor
    raise AssertionError("every batch-B pinned card is authorised somewhere; "
                         "mutation I would be vacuous")


# ----------------------------------------------------------------- mutations
# Each entry: (id, description, files it touches, apply(), probe, required check)

def build_mutations():
    unowned_file, unowned_anchor = pick_unowned_batch_b_card()
    print("mutation I target (batch-B pinned, unauthorised): %s#%s"
          % (unowned_file, unowned_anchor))

    Q25 = ("meoclass1/QB1_A.html", "q25")

    def drop_record():
        MANIFEST.unlink()

    return [
        ("A1", "remove the correction record entirely",
         [MANIFEST], drop_record, "batch_e1", "only_authorised_cards_changed"),

        ("A2", "remove the correction record entirely",
         [MANIFEST], drop_record, "batch_b", "pre_existing_cards_unchanged"),

        ("A3", "remove the correction record entirely",
         [MANIFEST], drop_record, "corrections",
         "tracked_correction_records_present"),

        ("B", "corrupt the correction id",
         [MANIFEST],
         lambda: edit_manifest(
             lambda d: d.__setitem__("correction_id", "CORR-SOMETHING-ELSE")),
         "corrections", "correction_id_matches_filename"),

        ("C1", "corrupt a declared card's anchor",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][0].__setitem__("anchor", "q999")),
         "corrections", "declared_cards_present_live"),

        ("C2", "point a declared card at the wrong page",
         [MANIFEST],
         lambda: edit_manifest(_retarget_q25_file),
         "batch_e1", "only_authorised_cards_changed"),

        ("D1", "corrupt a declared post-edit digest",
         [MANIFEST],
         lambda: edit_manifest(
             lambda d: d["cards"][0].__setitem__("post_edit_digest", "0" * 64)),
         "corrections", "live_matches_authorised_post_state"),

        ("D2", "corrupt a declared pre-edit digest",
         [MANIFEST],
         lambda: edit_manifest(
             lambda d: d["cards"][0].__setitem__("pre_edit_digest", "0" * 64)),
         "corrections", "pre_edit_digests_match_baseline"),

        ("E", "change a card the record never declares",
         [REPO / unowned_file],
         lambda: mutate_card(unowned_file, unowned_anchor),
         "corrections", "no_undeclared_change_in_window"),

        ("F", "move a declared card beyond its authorised final state",
         [REPO / Q25[0]],
         lambda: mutate_card(*Q25),
         "corrections", "live_matches_authorised_post_state"),

        ("G", "remove ONE declared card from the record",
         [MANIFEST],
         lambda: edit_manifest(_drop_qb5a_q4),
         "batch_b", "pre_existing_cards_unchanged"),

        ("I", "change a batch-B pinned card that no record authorises",
         [REPO / unowned_file],
         lambda: mutate_card(unowned_file, unowned_anchor),
         "batch_b", "pre_existing_cards_unchanged"),
    ]


def _retarget_q25_file(d):
    for card in d["cards"]:
        if card["anchor"] == "q25":
            card["file"] = "QB9_Z.html"
            card["path"] = "meoclass1/QB9_Z.html"


def _drop_qb5a_q4(d):
    d["cards"] = [c for c in d["cards"] if c["anchor"] != "q4"]


# ------------------------------------------------------- tree custody / recovery

def tree_dirt() -> str:
    """`git status --porcelain`, as bytes-faithful text.

    Used as the closing integrity assertion.  Restoring each mutation as it
    goes and never checking the aggregate is exactly how the 4 September
    incident reported a tidy summary over a tree that still had a manifest
    deleted in it.
    """
    out = subprocess.run(["git", "status", "--porcelain"], cwd=str(REPO),
                         capture_output=True, check=False)
    return out.stdout.decode("utf-8", "replace").strip()


def refuse_on_stale_journal() -> int | None:
    """A journal left behind means a previous run was killed mid-mutation.

    Running again on top of it is how a recoverable interruption turns into a
    committed corruption: the new run would capture the DAMAGED bytes as its
    own 'original' and faithfully restore the damage.  So this fails closed and
    names the recovery command.
    """
    stale = stale_runs(REPO)
    if not stale:
        return None
    print("REFUSING TO RUN -- %d unrecovered mutation journal(s) present." % len(stale))
    for run_dir in stale:
        entries = json.loads((run_dir / "journal.json").read_text(encoding="utf-8"))
        print("  %s  (%d file(s) under custody)"
              % (run_dir.name, len(entries["files"])))
        for entry in entries["files"]:
            print("      %s" % entry["path"])
    print("\nA previous run was terminated before it could restore these files.")
    print("Recover with:  python tools/oral/mutate_corrections.py --recover")
    return 2


def recover_main() -> int:
    stale = stale_runs(REPO)
    if not stale:
        print("no unrecovered mutation journals; nothing to do")
        return 0
    failures = []
    for run_dir in stale:
        restored, failed = recover(run_dir)
        print("%s: restored %d file(s)%s"
              % (run_dir.name, len(restored),
                 "; FAILED %s" % failed if failed else ""))
        for path in restored:
            print("    %s" % path)
        if failed:
            failures.extend(failed)
        else:
            discard(run_dir)
    if failures:
        print("\nRECOVERY INCOMPLETE: %s" % failures)
        return 2
    print("\ngit status after recovery:\n%s" % (tree_dirt() or "(clean)"))
    return 0


# ---------------------------------------------------------------------- main

def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--recover" in argv:
        return recover_main()

    if not MANIFEST.is_file():
        print("correction record missing: %s" % MANIFEST_REL)
        return 2

    refused = refuse_on_stale_journal()
    if refused is not None:
        return refused

    dirt_before = tree_dirt()
    cust = Custodian(REPO, name="corrections")
    try:
        return _run(cust, dirt_before)
    finally:
        # Layer 1 at suite scope.  Every per-mutation guard has already
        # restored, so this is normally a no-op -- but a raise between guards
        # (build_mutations, a probe helper, an assertion) has no guard of its
        # own, and this is what covers it.
        leftover = cust.restore_all()
        if leftover:
            print("SUITE-LEVEL RESTORE FAILED: %s" % leftover)
        cust.close()


def _run(cust, dirt_before) -> int:
    mutations = build_mutations()

    # ---- preflight: every mutation must really change something ------------
    #
    # oral_mutation.preflight_or_die() dry-runs TEXT mutations in memory. Half
    # of this suite deletes or rewrites a JSON record instead, which that helper
    # cannot model, so the same contract is enforced directly: apply, compare
    # bytes, restore. Same guarantee -- no mutation reaches the expensive probe
    # phase without proving it changes bytes -- reached the only way it can be
    # reached for this suite's shapes.
    print("\n--- preflight: every mutation must change bytes ---")
    no_ops = []
    for mid, desc, files, apply, _probe, _check in mutations:
        # try/finally, not try/except: KeyboardInterrupt and SystemExit are
        # BaseException, so the old `except Exception` let both walk past the
        # restore with the mutation still applied.  This is the incident.
        with cust.guard(files):
            try:
                apply()
            except Exception as exc:
                print("%-3s ERROR %s: %s" % (mid, type(exc).__name__, exc))
                no_ops.append(mid)
                continue
            changed = any(
                cust.original(p) != (pathlib.Path(p).read_bytes()
                                     if pathlib.Path(p).is_file() else None)
                for p in files)
            print("%-3s %-52s %s" % (mid, desc, "applied" if changed else "NO-OP"))
            if not changed:
                no_ops.append(mid)

    if no_ops:
        print("\npreflight FAILED -- these mutations change no bytes: %s"
              % ", ".join(no_ops))
        print("0 mutations, 0 escape(s), %d no-op(s), 0 crash(es)" % len(no_ops))
        return 1

    # ---- control: unmutated, the probes must be green ----------------------
    print("\n--- control (mutation H): unmutated state ---")
    control = {}
    for key in ("corrections", "batch_b", "batch_e4"):
        rc, failing = run_probe(key)
        control[key] = failing
        print("H   %-12s exit=%d failing=%s" % (key, rc, sorted(failing) or "none"))

    escapes = []
    crashes = []
    if control["corrections"] or control["batch_b"] or control["batch_e4"]:
        print("H   CONTROL IS NOT GREEN -- every later 'catch' is meaningless")
        escapes.append("H")

    # ---- the suite ---------------------------------------------------------
    print("\n--- mutations ---")
    caught = 0
    for mid, desc, files, apply, probe, want in mutations:
        # The probe is a subprocess that runs for tens of seconds; that window
        # is where an interrupt actually lands.  The guard's __exit__ covers it
        # for a catchable signal, and the on-disk journal covers it for a kill.
        with cust.guard(files):
            try:
                apply()
                rc, failing = run_probe(probe)
            except Exception as exc:
                print("%-3s %-52s CRASH %s" % (mid, desc, exc))
                crashes.append(mid)
                continue

        # The named check must be the one that broke. Failing for another
        # reason is not evidence that this mutation was detected.
        if want in failing:
            caught += 1
            print("%-3s %-52s CAUGHT   %s/%s" % (mid, desc, probe, want))
        else:
            escapes.append(mid)
            print("%-3s %-52s ESCAPED  %s wanted=%s got=%s"
                  % (mid, desc, probe, want, sorted(failing) or "none"))

    # ---- mutation J: E6's line-ending debt is not laundered ---------------
    print("\n--- mutation J: E6 debt must stay classified as its own failure ---")
    rc, failing = run_probe("batch_e6")
    correction_checks = {"only_authorised_cards_changed"}
    still_correction = sorted(failing & correction_checks)
    other = sorted(failing - correction_checks)
    print("J   batch_e6 exit=%d correction-caused=%s other=%s"
          % (rc, still_correction or "none", other or "none"))
    if still_correction:
        print("J   E6 STILL fails for a correction-authorisation reason")
        escapes.append("J")
    elif not other:
        print("J   batch_e6 is fully green; the line-ending debt is NOT present, "
              "so this mutation proves nothing and must not be reported as a pass")
        escapes.append("J")
    else:
        caught += 1
        print("J   E6's remaining failure is its own: %s" % ", ".join(other))

    total = len(mutations) + 1
    print("\n%d mutations, %d escape(s), 0 no-op(s), %d crash(es)"
          % (total, len(escapes), len(crashes)))
    if escapes:
        print("escaped: %s" % ", ".join(escapes))

    # ---- closing integrity assertion --------------------------------------
    #
    # Two independent proofs, because they can fail apart: custody proves every
    # file it touched is byte-identical to capture, and `git status` proves the
    # suite did not leave something custody never knew about.  A HARD FAIL here
    # outranks the mutation verdict -- a suite that cannot put the repository
    # back has not passed, whatever it caught.
    print("\n--- closing integrity ---")
    drift = cust.verify_pristine()
    print("custody: %d file(s) under custody, drift=%s"
          % (len(cust._order), drift or "none"))
    dirt_after = tree_dirt()
    print("git status: %s" % (dirt_after or "(clean)"))
    if drift or dirt_after != dirt_before:
        print("HARD FAIL -- the working tree was NOT restored.")
        if dirt_after != dirt_before:
            print("  before: %s\n  after:  %s"
                  % (dirt_before or "(clean)", dirt_after or "(clean)"))
        return 2

    return 1 if (escapes or crashes) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CustodyError as exc:
        # Never let this surface as a traceback among other tracebacks.
        print("\nHARD FAIL -- custody: %s" % exc)
        sys.exit(2)
