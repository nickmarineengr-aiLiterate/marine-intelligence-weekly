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
import tempfile
import time

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from oral_bytes import read_text, write_text                    # noqa: E402
from oral_custody import (Custodian, CustodyError, discard,     # noqa: E402
                          recover, stale_runs)
from oral_manifest import authorisation_manifest_paths          # noqa: E402
from oral_mutation import emit_results                          # noqa: E402
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

# Where the per-mutation evidence lands.  A suite that runs for over two hours
# and leaves only "2 escapes" on a terminal has produced a number, not a
# result: the 8 September release run could not name which two of thirteen
# mutations escaped, and the answer had to be re-derived by re-running it.
# This file is written before the process exits and survives it.
RESULTS_PATH = HERE / "mutate_corrections_results.json"

# What KIND of check caught a mutation.  A digest pin fires on any byte change
# to a card it pins and is blind to what the change means; a semantic check
# reads the proposition.  A mutation "caught" only by a pin has not been shown
# to be understood -- the pin would have fired on a typo just the same -- so
# the two are recorded apart rather than totalled together.
DIGEST_PIN_CHECKS = frozenset({
    "pre_existing_cards_unchanged",
    "only_authorised_cards_changed",
    "live_matches_authorised_post_state",
    "pre_edit_digests_match_baseline",
    "governing_commits_produced_post_state",
})


def _rel(item) -> str:
    """A target as a repo-relative posix path, whichever shape it arrived in."""
    path = pathlib.Path(item)
    try:
        return path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return path.as_posix()


def classify_checks(failing):
    """Split a failing-check set into digest pins and semantic checks."""
    pins = sorted(c for c in failing if c in DIGEST_PIN_CHECKS)
    semantic = sorted(c for c in failing if c not in DIGEST_PIN_CHECKS)
    return pins, semantic


def restore_ok(cust, files) -> bool:
    """Is every file this mutation touched byte-identical to its capture?

    Asked per mutation rather than only at suite scope.  The suite-scope
    assertion says the tree came back; it cannot say WHICH mutation failed to
    put its file back, and by the time it runs the next mutation has already
    captured the damaged bytes as its own original.
    """
    for item in files:
        path = pathlib.Path(item)
        was = cust.original(path)
        now = path.read_bytes() if path.is_file() else None
        if was != now:
            return False
    return True


def persist(results_path, evidence, scope, control=None) -> None:
    """Write the per-mutation record where it outlives the process.

    Outside the repository by default: this suite's closing assertion is that
    `git status` is byte-for-byte what it was, and a results file dropped into
    a tracked directory would break that assertion by existing.
    """
    payload = {
        "suite": "corrections",
        "scope": list(scope),
        "control": control or {},
        "mutations": [evidence[k] for k in sorted(evidence)],
    }
    results_path.parent.mkdir(parents=True, exist_ok=True)
    results_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + chr(10),
                            encoding="utf-8")
    print("per-mutation evidence: %s" % results_path)


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


def other_owners(file: str, anchor: str) -> list:
    """Every OTHER authorisation record that also declares this card."""
    names = []
    for path in authorisation_manifest_paths(HERE):
        if path.name == MANIFEST.name:
            continue
        for card in json.loads(read_text(path)).get("cards", []):
            if card.get("file") == file and card.get("anchor") == anchor:
                names.append(path.name)
                break
    return names


def _raw_digests(rel: str) -> dict:
    """Card digests read the way batch B reads them.

    ``newline=""``, not the module's universal-newline reader: on a CRLF page
    the two disagree, and a selector that compared a translated digest against
    an untranslated pin would be answering a different question from the guard
    it is choosing a target for.
    """
    text = (REPO / rel).read_text(encoding="utf-8", newline="")
    return card_digests(text)


def pick_sole_owned_card() -> dict:
    """A card THIS record declares that NO other authorisation record does.

    Removing cover only proves something when the cover removed is the only
    cover there was.  Mutation G used to hardcode QB5_A#q4; on 7 September
    `CORR-PASS2-HUMAN-ELEMENT-20260907` also declared that card, and from then
    on dropping it from this record removed nothing.  The guard stayed green --
    correctly, because the card was still authorised -- and the suite recorded
    an anonymous escape for a mutation that had quietly stopped asserting
    anything.

    Selecting at runtime is the discipline `pick_unowned_batch_b_card` already
    applies, for exactly this reason.  When no sole-owned card is left this
    RAISES, so the next occurrence arrives as a named failure rather than an
    escape nobody can attribute.
    """
    co_owned = {}
    for card in json.loads(read_text(MANIFEST)).get("cards", []):
        others = other_owners(card["file"], card["anchor"])
        if not others:
            return card
        co_owned["%s#%s" % (card["file"], card["anchor"])] = others
    raise AssertionError(
        "every card this record declares is also declared by another "
        "authorisation record, so dropping one of this record's declarations "
        "removes no cover and mutation G would assert nothing: %s" % co_owned)


def pick_pinned_card_and_owners():
    """A batch-B-pinned card this record declares, and EVERY record covering it.

    Batch B's pin stands down for any card some authorisation record names.
    That is right -- one authorised owner is enough -- but it means "remove
    this record" stopped being a test of the pin the moment a second record
    named the only pinned card in common.  The honest form of the claim is
    "remove EVERY record that authorises it", and that is what this selects.

    The card must also have DRIFTED from the pin, or the pin would stay green
    with no owner at all and the mutation would be vacuous a second way.
    """
    pins = json.loads(read_text(HERE / "batch_b_manifest.json")).get(
        "baseline_card_digests") or {}
    skipped = {}
    for card in json.loads(read_text(MANIFEST)).get("cards", []):
        pinned = (pins.get(card["file"]) or {}).get(card["anchor"])
        key = "%s#%s" % (card["file"], card["anchor"])
        if pinned is None:
            skipped[key] = "not pinned by batch B"
            continue
        live = _raw_digests(card["path"]).get(card["anchor"])
        if live == pinned:
            skipped[key] = "live still equals the batch-B pin"
            continue
        owners = [MANIFEST] + [HERE / n for n in
                               other_owners(card["file"], card["anchor"])]
        return card, owners
    raise AssertionError(
        "no card this record declares is both pinned by batch B and drifted "
        "from that pin, so mutation A2 cannot reach the generation-1 pin at "
        "all: %s" % skipped)


def pick_co_owned_card():
    """A card this record declares that ANOTHER record also declares.

    The control case for the repair above: it must KEEP its cover.
    """
    for card in json.loads(read_text(MANIFEST)).get("cards", []):
        others = other_owners(card["file"], card["anchor"])
        if others:
            return card, others
    return None, []


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

    sole = pick_sole_owned_card()
    print("mutation G target (declared here and NOWHERE else): %s#%s"
          % (sole["file"], sole["anchor"]))

    pinned_card, pinned_owners = pick_pinned_card_and_owners()
    print("mutation A2 target (batch-B pinned, drifted): %s#%s -- authorised by %s"
          % (pinned_card["file"], pinned_card["anchor"],
             ", ".join(p.name for p in pinned_owners)))

    def drop_every_owner():
        for path in pinned_owners:
            path.unlink()

    Q25 = ("meoclass1/QB1_A.html", "q25")

    def drop_record():
        MANIFEST.unlink()

    return [
        ("A1", "remove the correction record entirely",
         [MANIFEST], drop_record, "batch_e1", "only_authorised_cards_changed"),

        # A2 asked whether batch B's generation-1 pin comes back when this
        # record is removed.  It does not, and it should not: since 7 September
        # a second record also authorises QB5_A#q4, the only pinned card the
        # two have in common, so one owner remains and the pin correctly stands
        # down.  Removing only this record left batch B reporting NO failing
        # check at all -- the mutation changed bytes and asserted nothing.
        #
        # The claim, stated truthfully, is about cover rather than about this
        # one file: with NO record authorising the card, the historical pin
        # must go red again.  The owner set is resolved at runtime, so the
        # mutation cannot expire the next time a record is added.  Mutation K
        # is the other half -- remove only ONE of the owners and cover holds.
        ("A2", "remove EVERY record authorising a batch-B pinned card",
         list(pinned_owners), drop_every_owner,
         "batch_b", "pre_existing_cards_unchanged"),

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

        # G's claim -- "drop one declared card and ONLY that card loses cover"
        # -- was hardcoded onto QB5_A#q4 and expired the day a second record
        # declared it.  The card is now chosen at runtime for sole ownership,
        # and the probe is a guard that can actually see the loss: the chosen
        # card moved inside batch E1's window, so once this record stops
        # declaring it, nothing authorises it.
        ("G", "remove ONE declared card from the record",
         [MANIFEST],
         lambda: edit_manifest(_drop_card(sole["file"], sole["anchor"])),
         "batch_e1", "only_authorised_cards_changed"),

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


def _drop_card(file: str, anchor: str):
    """Drop exactly one declared card, matched on file AND anchor.

    On both, because two cards in this record share the anchor
    `dependency-graph` and differ only by path: dropping "the one with that
    anchor" would silently drop two, and a two-card mutation is not the
    one-card claim under test.
    """
    def mutate(d):
        d["cards"] = [c for c in d["cards"]
                      if not (c["file"] == file and c["anchor"] == anchor)]
    return mutate


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

    # `--only A1,F` runs a named subset.  The control phase, the preflight
    # byte-change contract, the probe commands and the catch rule are all
    # unchanged -- only the mutation list is narrowed -- so a subset result
    # means exactly what the same mutation means in the full run.  It exists
    # because proving one repaired guard should not cost the 2.3 hours the
    # whole suite costs, not to provide a cheaper way to claim the gate green:
    # a subset run reports its own scope and is never a substitute for §8.
    only = None
    results_path = None
    for i, arg in enumerate(argv):
        if arg == "--only" and i + 1 < len(argv):
            only = {x.strip() for x in argv[i + 1].split(",") if x.strip()}
        elif arg.startswith("--only="):
            only = {x.strip() for x in arg.split("=", 1)[1].split(",") if x.strip()}
        elif arg == "--results" and i + 1 < len(argv):
            results_path = pathlib.Path(argv[i + 1])
        elif arg.startswith("--results="):
            results_path = pathlib.Path(arg.split("=", 1)[1])
    if results_path is None:
        results_path = pathlib.Path(tempfile.gettempdir()) / (
            "miw-mutate-corrections-%s.json"
            % time.strftime("%Y%m%dT%H%M%S", time.gmtime()))

    if not MANIFEST.is_file():
        print("correction record missing: %s" % MANIFEST_REL)
        return 2

    refused = refuse_on_stale_journal()
    if refused is not None:
        return refused

    dirt_before = tree_dirt()
    cust = Custodian(REPO, name="corrections")
    try:
        return _run(cust, dirt_before, only, results_path)
    finally:
        # Layer 1 at suite scope.  Every per-mutation guard has already
        # restored, so this is normally a no-op -- but a raise between guards
        # (build_mutations, a probe helper, an assertion) has no guard of its
        # own, and this is what covers it.
        leftover = cust.restore_all()
        if leftover:
            print("SUITE-LEVEL RESTORE FAILED: %s" % leftover)
        cust.close()


def _run(cust, dirt_before, only=None, results_path=None) -> int:
    mutations = build_mutations()
    if only:
        known = {m[0] for m in mutations}
        unknown = sorted(only - known)
        if unknown:
            print("unknown mutation id(s): %s" % ", ".join(unknown))
            return 2
        mutations = [m for m in mutations if m[0] in only]
        print("--only: running %s, and J always"
              % (", ".join(m[0] for m in mutations) or "(none)"))

    # ---- preflight: every mutation must really change something ------------
    #
    # oral_mutation.preflight_or_die() dry-runs TEXT mutations in memory. Half
    # of this suite deletes or rewrites a JSON record instead, which that helper
    # cannot model, so the same contract is enforced directly: apply, compare
    # bytes, restore. Same guarantee -- no mutation reaches the expensive probe
    # phase without proving it changes bytes -- reached the only way it can be
    # reached for this suite's shapes.
    print("\n--- preflight: every mutation must change bytes ---")
    evidence = {}
    for mid, desc, files, _apply, probe, check in mutations:
        evidence[mid] = {
            "id": mid,
            "description": desc,
            "probe": probe,
            "expected_check": check,
            "expected_check_kind": ("digest-pin" if check in DIGEST_PIN_CHECKS
                                    else "semantic"),
            "targets": [_rel(f) for f in files],
            "bytes_changed": None,
            "verdict": None,
            "failing_checks": [],
            "digest_pins_failing": [],
            "semantic_checks_failing": [],
            "caught_by_expected_check": None,
            "caught_only_by_digest_pin": None,
            "restore_verified": None,
            "seconds": None,
        }

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
            evidence[mid]["bytes_changed"] = bool(changed)
            if not changed:
                no_ops.append(mid)
                evidence[mid]["verdict"] = "no-op"

    if no_ops:
        print("\npreflight FAILED -- these mutations change no bytes: %s"
              % ", ".join(no_ops))
        persist(results_path, evidence, [m[0] for m in mutations])
        emit_results("corrections", no_ops=no_ops, run=len(no_ops))
        return 1

    # ---- control: unmutated, the probes must be green ----------------------
    print("\n--- control (mutation H): unmutated state ---")
    control = {}
    control_record = {}
    for key in ("corrections", "batch_b", "batch_e4"):
        started = time.time()
        rc, failing = run_probe(key)
        control[key] = failing
        control_record[key] = {
            "exit": rc,
            "failing_checks": sorted(failing),
            "seconds": round(time.time() - started, 1),
        }
        print("H   %-12s exit=%d failing=%s" % (key, rc, sorted(failing) or "none"))

    escapes = []
    crashes = []
    if control["corrections"] or control["batch_b"] or control["batch_e4"]:
        print("H   CONTROL IS NOT GREEN -- every later 'catch' is meaningless")
        escapes.append("H")

    # ---- the suite ---------------------------------------------------------
    print("\n--- mutations ---")
    caught = 0
    caught_ids = []
    for mid, desc, files, apply, probe, want in mutations:
        # The probe is a subprocess that runs for tens of seconds; that window
        # is where an interrupt actually lands.  The guard's __exit__ covers it
        # for a catchable signal, and the on-disk journal covers it for a kill.
        record = evidence[mid]
        started = time.time()
        crashed = False
        failing = set()
        with cust.guard(files):
            try:
                apply()
                rc, failing = run_probe(probe)
                record["probe_exit"] = rc
            except Exception as exc:
                print("%-3s %-52s CRASH %s" % (mid, desc, exc))
                crashes.append(mid)
                record["verdict"] = "crash"
                record["error"] = "%s: %s" % (type(exc).__name__, exc)
                crashed = True

        # Recorded AFTER the guard has exited, so it describes the restore that
        # actually happened rather than the intention to restore.
        record["seconds"] = round(time.time() - started, 1)
        record["restore_verified"] = restore_ok(cust, files)
        if crashed:
            continue

        pins, semantic = classify_checks(failing)
        record["failing_checks"] = sorted(failing)
        record["digest_pins_failing"] = pins
        record["semantic_checks_failing"] = semantic
        record["caught_by_expected_check"] = want in failing
        # "Something went red" is not the same as "the proposition was
        # checked".  A mutation whose only red is a byte pin was detected by a
        # guard that cannot tell a corrupted claim from a stray space.
        record["caught_only_by_digest_pin"] = bool(
            failing and want not in failing and not semantic)

        # The named check must be the one that broke. Failing for another
        # reason is not evidence that this mutation was detected.
        if want in failing:
            caught += 1
            caught_ids.append(mid)
            record["verdict"] = "caught"
            print("%-3s %-52s CAUGHT   %s/%s" % (mid, desc, probe, want))
        else:
            escapes.append(mid)
            record["verdict"] = "escaped"
            print("%-3s %-52s ESCAPED  %s wanted=%s got=%s"
                  % (mid, desc, probe, want, sorted(failing) or "none"))

    # ---- mutation J: E6's line-ending debt is not laundered ---------------
    print("\n--- mutation J: E6 debt must stay classified as its own failure ---")
    j_started = time.time()
    rc, failing = run_probe("batch_e6")
    evidence["J"] = {
        "id": "J",
        "description": "E6's line-ending debt must stay its own failure",
        "probe": "batch_e6",
        "expected_check": "(none: E6 must fail for a NON-correction reason)",
        "expected_check_kind": "semantic",
        "targets": [],
        "bytes_changed": False,
        "verdict": None,
        "failing_checks": sorted(failing),
        "digest_pins_failing": classify_checks(failing)[0],
        "semantic_checks_failing": classify_checks(failing)[1],
        "caught_by_expected_check": None,
        "caught_only_by_digest_pin": None,
        "restore_verified": True,
        "probe_exit": rc,
        "seconds": None,
    }
    correction_checks = {"only_authorised_cards_changed"}
    still_correction = sorted(failing & correction_checks)
    other = sorted(failing - correction_checks)
    print("J   batch_e6 exit=%d correction-caused=%s other=%s"
          % (rc, still_correction or "none", other or "none"))
    evidence["J"]["seconds"] = round(time.time() - j_started, 1)
    if still_correction:
        print("J   E6 STILL fails for a correction-authorisation reason")
        escapes.append("J")
        evidence["J"]["verdict"] = "escaped"
        evidence["J"]["caught_by_expected_check"] = False
    elif not other:
        print("J   batch_e6 is fully green; the line-ending debt is NOT present, "
              "so this mutation proves nothing and must not be reported as a pass")
        escapes.append("J")
        evidence["J"]["verdict"] = "escaped"
        evidence["J"]["caught_by_expected_check"] = False
    else:
        caught += 1
        caught_ids.append("J")
        evidence["J"]["verdict"] = "caught"
        evidence["J"]["caught_by_expected_check"] = True
        print("J   E6's remaining failure is its own: %s" % ", ".join(other))

    # ---- mutation K: a legitimately co-authorised card KEEPS its cover ----
    #
    # The negative half of A2, and the reason the A2 repair is a correction
    # rather than a weakening.  A2 removes EVERY record authorising a pinned
    # card and requires the pin to go red.  K removes ONE of them and requires
    # the pin to stay GREEN, because the remaining record still authorises the
    # card and still pins its live state.
    #
    # Without K, the obvious way to "fix" A2 would have been to make batch B
    # reject any card whose every declaring record is not intact -- which would
    # reject legitimate delegated corrections. K is what makes that
    # impossible to ship unnoticed.
    print("")
    print("--- mutation K: a co-authorised card keeps its cover ---")
    co_card, co_owners = pick_co_owned_card()
    if co_card is None:
        print("K   no card in this record is declared anywhere else, so the "
              "delegation control asserts nothing and must not pass")
        escapes.append("K")
        evidence["K"] = {
            "id": "K", "verdict": "escaped",
            "description": "co-authorised card keeps its cover",
            "probe": "batch_b", "targets": [],
            "expected_check": "pre_existing_cards_unchanged (must NOT fail)",
            "expected_check_kind": "digest-pin",
            "bytes_changed": False, "failing_checks": [],
            "digest_pins_failing": [], "semantic_checks_failing": [],
            "caught_by_expected_check": None,
            "caught_only_by_digest_pin": None,
            "restore_verified": True, "seconds": 0.0,
            "note": "VACUOUS: no co-authorised card exists"}
    else:
        k_started = time.time()
        k_files = [MANIFEST]
        with cust.guard(k_files):
            edit_manifest(_drop_card(co_card["file"], co_card["anchor"]))
            k_rc, k_failing = run_probe("batch_b")
        k_pins, k_semantic = classify_checks(k_failing)
        held = "pre_existing_cards_unchanged" not in k_failing
        evidence["K"] = {
            "id": "K",
            "description": "drop a card ANOTHER record also declares: cover holds",
            "probe": "batch_b",
            "expected_check": "pre_existing_cards_unchanged (must NOT fail)",
            "expected_check_kind": "digest-pin",
            "targets": [_rel(MANIFEST)],
            "co_owners": co_owners,
            "card": "%s#%s" % (co_card["file"], co_card["anchor"]),
            "bytes_changed": True,
            "failing_checks": sorted(k_failing),
            "digest_pins_failing": k_pins,
            "semantic_checks_failing": k_semantic,
            "caught_by_expected_check": held,
            "caught_only_by_digest_pin": False,
            "restore_verified": restore_ok(cust, k_files),
            "probe_exit": k_rc,
            "seconds": round(time.time() - k_started, 1),
            "verdict": "caught" if held else "escaped",
        }
        print("K   %s#%s is also declared by %s"
              % (co_card["file"], co_card["anchor"], ", ".join(co_owners)))
        if held:
            caught += 1
            caught_ids.append("K")
            print("K   cover HELD -- one remaining owner is enough, exactly as "
                  "the model intends (batch_b failing=%s)"
                  % (sorted(k_failing) or "none"))
        else:
            escapes.append("K")
            print("K   batch_b REJECTED a legitimately co-authorised card -- "
                  "the exemption has been broken, not hardened")

    total = len(mutations) + 2
    persist(results_path, evidence,
            [m[0] for m in mutations] + ["J", "K"], control_record)
    print("")
    emit_results("corrections", caught=caught_ids, escaped=escapes,
                 crashes=crashes, run=total)

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
