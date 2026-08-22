#!/usr/bin/env python3
"""
Mutation suite for Oral follow-up production batch F1b.

WHAT THIS SUITE HAS TO PROVE
----------------------------
F1b is the FIRST production use of historical digest supersession.  Everything
that made it possible is new, and every new mechanism is a new way to ship a
false green.  So this suite attacks the chain itself, not only the content::

    remove the limb                   -> the limb check must go red
    remove THIS manifest              -> E1's historical pin must go red again
    corrupt the PREDECESSOR's pin     -> a rebaselined ancestor must break it
    corrupt this batch's pre-digest   -> continuity must be required
    corrupt this batch's post-digest  -> the terminal must be the live card
    edit the live card                -> the terminal must be the live card
    corrupt the supersedes claim      -> the claim must match the ancestor
    add a second successor            -> one predecessor, one successor
    name a predecessor that is absent -> an orphan must not resolve
    strip relationship metadata       -> the edge must be required
    reword q-text / move the anchor   -> identity must be stable
    edit an unauthorised card         -> delegation must not cover it
    claim FUP-006 was produced in F1  -> history must not be laundered
    delete F1's hold record           -> nor may it be erased

THE TWO MUTATIONS THAT MATTER MOST
----------------------------------
**B** removes this manifest and requires ``validate_batch_e1.py`` to go RED.
Without it, "E1 is green" would mean nothing more than "E1 was never asked".
The whole supersession contract rests on E1 still making a real claim, and B is
what proves the claim is real.

**O** and **P** attack the HISTORY rather than the product.  F1 held FUP-006 and
said so; F1b implemented it.  If a later record could edit F1 to claim it
produced the action, or simply delete the hold, the repository would lose the
only evidence that the work was ever outstanding -- and it would lose it in a
way no digest check could describe.

EACH MUTATION MUST TRIP ITS OWN NAMED CHECK
-------------------------------------------
A validator that fails for the wrong reason is not evidence.  E6's mutation L
corrupted a field nothing read and scored "caught" because something else was
already failing.  Every mutation below names the check it must break, and
breaking a DIFFERENT check counts as an escape.

CONTROL IS BASELINE-AWARE
-------------------------
The precondition is *no NEW failures*, never *no failures* -- spelling it the
second way is what made ``batch_e6_mutate`` unrunnable and stopped a default
release at gate 28 of 46.  A green control derives no baseline at all, which
matters here for a reason beyond cost: ``validate_batch_f1b.py`` does not exist
on ``BASELINE_REF`` yet, so a precondition that always derived would report
UNAVAILABLE for this suite's very first run.
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

from oral_bytes import read_text, write_text                      # noqa: E402
from oral_mutation import (                                       # noqa: E402
    mutation_verdict, parse_summary, require_control_baseline,
    validator_fail_details)
from oral_release_gates import BASELINE_REF                       # noqa: E402
from validate_batch_f1b import CARD_OPEN, cards_of                # noqa: E402

MANIFEST = HERE / "batch_f1b_manifest.json"
MANIFEST_REL = "tools/oral/batch_f1b_manifest.json"
F1_MANIFEST = HERE / "batch_f1_manifest.json"
E1_MANIFEST = HERE / "batch_e1_enrichment_manifest.json"
REGISTER = HERE / "oral_followup_register.json"

# A transient sibling record, used only by the CHAIN_FORK mutation. It must not
# survive the run: a stray manifest widens the authorisation surface of every
# guard in the repository.
FORK_MANIFEST = HERE / "batch_zzfork_f1b_manifest.json"

PROBES = {
    "f1b": "validate_batch_f1b.py",
    # The historical owner. Its pin on QB1_A#q9 is the thing this whole batch
    # had to descend from rather than overwrite.
    "e1": "validate_batch_e1.py",
}

QB1_A = "meoclass1/QB1_A.html"

# A structural byte change that says nothing, so a card-edit mutation cannot be
# mistaken for a content change.
CARD_MARKER = "<!-- f1b-mutation-probe -->"


def run_probe(key: str) -> tuple[int, set, dict]:
    """Run one validator; return (exit code, FAILing check names, details)."""
    out = subprocess.run([sys.executable, str(HERE / PROBES[key])],
                         cwd=str(REPO), capture_output=True, check=False)
    text = (out.stdout + out.stderr).decode("utf-8", "replace")
    return (out.returncode, set(re.findall(r"^FAIL\s+(\S+)", text, re.M)),
            validator_fail_details(text))


class Snapshot:
    """Byte-exact custody of every file a mutation touches.

    Restores from what this object personally read, never from git:
    ``git checkout <ref> -- <file>`` destroys uncommitted work, which has
    already cost real edits in this repository. A file that did not exist is
    restored by being removed again.
    """

    def __init__(self, paths):
        self.data = {}
        for path in paths:
            p = pathlib.Path(path)
            self.data[p] = p.read_bytes() if p.is_file() else None

    def restore(self) -> list[str]:
        bad = []
        for path, blob in self.data.items():
            if blob is None:
                if path.is_file():
                    path.unlink()
                continue
            path.write_bytes(blob)
            if path.read_bytes() != blob:
                bad.append(str(path))
        return bad


def edit_json(path, mutate, indent=2) -> None:
    data = json.loads(read_text(path))
    mutate(data)
    write_text(path, json.dumps(data, indent=indent) + "\n")


def edit_manifest(mutate) -> None:
    edit_json(MANIFEST, mutate)


def edit_register(followup_id: str, status: str) -> None:
    data = json.loads(read_text(REGISTER))
    for action in data.get("actions", []):
        if action.get("followup_id") == followup_id:
            action["status"] = status
            write_text(REGISTER, json.dumps(data, indent=1) + "\n")
            return
    raise AssertionError("no such action in the register: %s" % followup_id)


def mark_card(rel: str, anchor: str) -> None:
    """Change one card's bytes without changing what it says structurally."""
    path = REPO / rel
    text = read_text(path)
    for m in CARD_OPEN.finditer(text):
        got = re.search(r'\bid="([^"]+)"', m.group(0))
        if got and got.group(1) == anchor:
            write_text(path, text[:m.end()] + CARD_MARKER + text[m.end():])
            return
    raise AssertionError("card not found: %s#%s" % (rel, anchor))


def strip_from_card(rel: str, needle: str) -> None:
    path = REPO / rel
    text = read_text(path)
    if needle not in text:
        raise AssertionError("needle absent from %s: %r" % (rel, needle))
    write_text(path, text.replace(needle, "", 1))


def inject_into_card(rel: str, anchor_text: str, payload: str) -> None:
    path = REPO / rel
    text = read_text(path)
    if anchor_text not in text:
        raise AssertionError("anchor absent from %s: %r" % (rel, anchor_text))
    write_text(path, text.replace(anchor_text, anchor_text + payload, 1))


def reword_qtext(rel: str, anchor: str) -> None:
    path = REPO / rel
    text = read_text(path)
    card = cards_of(text)[anchor]
    m = re.search(r'(class="q-text"[^>]*>)(.*?)(</div>)', card, re.S)
    if not m:
        raise AssertionError("no q-text in %s#%s" % (rel, anchor))
    new_card = card[:m.start(2)] + m.group(2) + " (reworded)" + card[m.end(2):]
    write_text(path, text.replace(card, new_card, 1))


def write_fork() -> None:
    """A second successor claiming the SAME predecessor as this batch."""
    card = json.loads(read_text(MANIFEST))["cards"][0]
    write_text(FORK_MANIFEST, json.dumps({
        "batch_id": "ZZFORK",
        "note": "TRANSIENT mutation fixture. Never release evidence.",
        "cards": [{
            "action_id": "FUP-006-FORK",
            "file": card["file"], "anchor": card["anchor"],
            "pre_edit_digest": card["pre_edit_digest"],
            "post_edit_digest": "1" * len(card["post_edit_digest"]),
            "supersedes": dict(card["supersedes"]),
        }],
    }, indent=1) + "\n")


def pick_unauthorised_card() -> tuple[str, str]:
    """A canonical card that NO authorisation record owns.

    Chosen at run time rather than hardcoded: a hardcoded anchor silently stops
    testing anything the day some future record authorises that very card.
    """
    from oral_manifest import authorisation_manifest_paths
    owned = set()
    for path in authorisation_manifest_paths(HERE):
        for card in json.loads(read_text(path)).get("cards", []):
            owned.add("%s#%s" % (card.get("file"), card.get("anchor")))
    for page in sorted((REPO / "meoclass1").glob("QB*.html")):
        for anchor in sorted(cards_of(read_text(page))):
            if not re.fullmatch(r"q\d+", anchor):
                continue
            if "%s#%s" % (page.name, anchor) not in owned:
                return "meoclass1/" + page.name, anchor
    raise AssertionError("every canonical card is authorised somewhere; "
                         "the unauthorised-card mutation would be vacuous")


def build_mutations():
    """(id, description, files touched, apply, probe, required check)."""
    unauth_rel, unauth_anchor = pick_unauthorised_card()

    return [
        # ---- the product ---------------------------------------------------
        ("A", "remove the FUP-006 limb from QB1_A#q9",
         [REPO / QB1_A],
         lambda: strip_from_card(
             QB1_A, "<h4>Worked Application — Ever Given, Suez Canal (2021)</h4>"),
         "f1b", "missing_limb_supplied"),

        # ---- the chain -----------------------------------------------------
        # THE delegation mutation: without this manifest the historical pin has
        # no successor to descend to, and E1 must go red exactly as it did
        # before the contract existed.
        ("B", "remove F1b from the authorisation surface",
         [MANIFEST],
         lambda: MANIFEST.unlink(),
         "e1", "manifest_digests_match"),

        ("C", "rebaseline the PREDECESSOR's stored pin",
         [E1_MANIFEST],
         lambda: edit_json(E1_MANIFEST, lambda d: [
             c.update({"post_edit_digest": "0" * 16})
             for c in d["cards"] if c.get("action_id") == "ENRICH-A003"], indent=1),
         "f1b", "historical_predecessor_pin_preserved"),

        ("D", "corrupt this batch's pre-edit digest (break continuity)",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][0].update(
             {"pre_edit_digest": "0" * 16})),
         "f1b", "historical_predecessor_pin_preserved"),

        ("E", "corrupt this batch's post-edit digest",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][0].update(
             {"post_edit_digest": "0" * 16})),
         "f1b", "manifest_digests_match"),

        ("F", "edit the live card past the terminal state",
         [REPO / QB1_A],
         lambda: mark_card(QB1_A, "q9"),
         "f1b", "manifest_digests_match"),

        ("G", "make the supersedes claim disagree with the ancestor's pin",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][0]["supersedes"].update(
             {"post_edit_digest": "0" * 16})),
         "f1b", "historical_predecessor_pin_preserved"),

        ("H", "add a second successor claiming the same predecessor",
         [FORK_MANIFEST],
         write_fork,
         "f1b", "supersession_chain_is_continuous_and_terminal_here"),

        ("I", "name a predecessor that does not exist",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][0]["supersedes"].update(
             {"action_id": "ENRICH-A999"})),
         "f1b", "supersession_claim_well_formed"),

        # ---- relationship and identity -------------------------------------
        ("J", "strip the relationship edge from the manifest",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][0].pop("relationship_edge")),
         "f1b", "relationship_edge_carried_unchanged"),

        ("K", "change the relationship type away from the register's",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][0].update(
             {"relationship_type": "CROSS_QUESTION"})),
         "f1b", "relationship_type_matches_register"),

        ("L", "reword the target card's question text",
         [REPO / QB1_A],
         lambda: reword_qtext(QB1_A, "q9"),
         "f1b", "q_text_and_anchors_stable"),

        ("M", "move the target anchor in the manifest",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][0].update({"anchor": "q8"})),
         "f1b", "parent_target_matches_register"),

        ("N", "edit a card no authorisation record owns",
         [REPO / unauth_rel],
         lambda: mark_card(unauth_rel, unauth_anchor),
         "f1b", "only_authorised_cards_changed"),

        # ---- the history ---------------------------------------------------
        # F1 HELD this action. Laundering that -- by claiming F1 produced it, or
        # by deleting the hold -- destroys the only record that the work was
        # ever outstanding, and no digest check would notice.
        ("O", "claim FUP-006 was produced in the historical F1 batch",
         [F1_MANIFEST],
         lambda: edit_json(F1_MANIFEST, lambda d: d["cards"].append(
             {"action_id": "FUP-006", "followup_id": "FUP-006",
              "file": "QB1_A.html", "anchor": "q9", "status": "IMPLEMENTED"})),
         "f1b", "f1_does_not_claim_to_have_produced_it"),

        ("P", "delete the HELD record from the historical F1 batch",
         [F1_MANIFEST],
         lambda: edit_json(F1_MANIFEST, lambda d: d.update({"held_actions": []})),
         "f1b", "f1_still_records_the_hold_historically"),

        ("Q", "record the held work as no longer owed",
         [F1_MANIFEST],
         lambda: edit_json(F1_MANIFEST, lambda d: d["held_actions"][0].update(
             {"work_still_owed": False})),
         "f1b", "f1_still_records_the_hold_historically"),

        ("R", "drop this batch's discharge record",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d.pop("discharges_hold")),
         "f1b", "f1b_records_the_discharge"),

        # The register is the AUTHORISATION record, not a status board. Editing
        # it to say the action was produced creates a second, competing source
        # of truth for what is done.
        ("S", "edit the register to mark the action produced",
         [REGISTER],
         lambda: edit_register("FUP-006", "PRODUCED"),
         "f1b", "register_status_of_the_action_untouched"),

        # ---- content integrity ---------------------------------------------
        ("T", "remove the examiner follow-up edge from the live card",
         [REPO / QB1_A],
         lambda: strip_from_card(
             QB1_A, " now apply it to the Ever Given aground in the Suez"),
         "f1b", "relationship_edge_present_in_card"),

        ("U", "reintroduce an unsupported settlement figure",
         [REPO / QB1_A],
         lambda: inject_into_card(
             QB1_A, "<h4>Worked Application — Ever Given, Suez Canal (2021)</h4>",
             "<p>The owners settled for $550 million.</p>"),
         "f1b", "no_unsupported_claim_reintroduced"),

        ("V", "duplicate the pre-existing casualty anchor",
         [REPO / QB1_A],
         lambda: inject_into_card(
             QB1_A, "<h4>Worked Application — Ever Given, Suez Canal (2021)</h4>",
             '<div class="casualty-box"><strong class="cas-label">Casualty Anchor'
             "</strong>duplicate</div>"),
         "f1b", "casualty_anchor_not_duplicated"),

        ("W", "make the edit non-additive by deleting baseline text",
         [REPO / QB1_A],
         lambda: strip_from_card(QB1_A, "<h4>Classic Examples</h4>"),
         "f1b", "edits_purely_additive"),

        ("X", "leak internal production vocabulary to the candidate",
         [REPO / QB1_A],
         lambda: inject_into_card(
             QB1_A, "<h4>Worked Application — Ever Given, Suez Canal (2021)</h4>",
             "<p>FUP-006 GAP-0620 target_review_status</p>"),
         "f1b", "no_candidate_visible_metadata"),

        # ---- scoping records -----------------------------------------------
        ("Y", "ship the register's placeholder verification class",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][0].update(
             {"verification_scope": "UNCLASSIFIED_PENDING_BATCH_SCOPING"})),
         "f1b", "verification_class_governed_and_not_placeholder"),

        ("Z", "strip the currentness decision",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][0].update({"currentness": {}})),
         "f1b", "currentness_decision_recorded"),
    ]


def main() -> int:
    if not MANIFEST.is_file():
        print("F1b manifest missing: %s" % MANIFEST_REL)
        return 2
    if FORK_MANIFEST.is_file():
        print("stale fork fixture on disk: %s" % FORK_MANIFEST.name)
        return 2

    every = build_mutations()

    # ---- preflight: every mutation must really change something ------------
    #
    # oral_mutation.preflight_or_die() dry-runs TEXT mutations in memory. Most
    # of this suite rewrites, creates or deletes a JSON record instead, which
    # that helper cannot model, so the same contract is enforced directly:
    # apply, compare bytes, restore. Same guarantee -- no mutation reaches the
    # expensive probe phase without proving it changes bytes. E5's mutation C
    # and E6's mutation H each matched nothing, wrote nothing and exercised
    # nothing; E6 spent 22 minutes discovering it.
    print("--- preflight: every mutation must change bytes ---")
    no_ops = []
    for mid, desc, files, apply, _probe, _check in every:
        snap = Snapshot(files)
        before = dict(snap.data)
        try:
            apply()
        except Exception as exc:                                   # noqa: BLE001
            print("%-3s ERROR %s: %s" % (mid, type(exc).__name__, exc))
            no_ops.append(mid)
            snap.restore()
            continue
        after = {p: (p.read_bytes() if p.is_file() else None) for p in snap.data}
        changed = any(before[p] != after[p] for p in before)
        delta = sum((len(after[p] or b"") - len(before[p] or b"")) for p in before)
        print("%-3s %-56s %-7s byte_delta=%+d"
              % (mid, desc, "applied" if changed else "NO-OP", delta))
        if not changed:
            no_ops.append(mid)
        bad = snap.restore()
        if bad:
            print("    RESTORE FAILED: %s" % bad)
            return 2

    if no_ops:
        print("\npreflight FAILED -- these mutations change no bytes: %s"
              % ", ".join(no_ops))
        print("0 mutations, 0 escape(s), %d no-op(s), 0 crash(es)" % len(no_ops))
        return 1

    # ---- control: baseline-aware, per section 7.4a -------------------------
    print("\n--- control: unmutated state ---")
    baselines, control_details = {}, {}
    for key, script in PROBES.items():
        rc, failing, details = run_probe(key)
        print("    %-4s exit=%d failing=%s" % (key, rc, sorted(failing) or "none"))
        state = require_control_baseline(
            failing, pathlib.Path("tools/oral") / script, REPO, ref=BASELINE_REF)
        if not state.runnable:
            print("PRE-RUN %s - aborting" % state.reason)
            return 2
        baselines[key] = state.control_failures
        control_details[key] = details

    # ---- the suite ---------------------------------------------------------
    print("\n--- mutations ---")
    escapes, crashes = [], []
    caught = 0
    for mid, desc, files, apply, probe, want in every:
        snap = Snapshot(files)
        try:
            apply()
            rc, failing, details = run_probe(probe)
        except Exception as exc:                                   # noqa: BLE001
            print("%-3s %-56s CRASH %s" % (mid, desc, exc))
            crashes.append(mid)
            snap.restore()
            continue
        finally:
            restore_failed = snap.restore()
        if restore_failed:
            print("    RESTORE FAILED: %s" % restore_failed)
            return 2

        # `code == 0` stops working as the escape test the moment a control
        # legitimately carries a failure, so the question asked is whether a NEW
        # failing check appeared and whether it is the intended one. With an
        # empty baseline this is byte-for-byte the original semantics.
        outcome, verdict = mutation_verdict(
            want, failing, baselines[probe], details, control_details[probe])
        if outcome == "escape":
            escapes.append(mid)
            print("%-3s %-56s ESCAPED  %s %s" % (mid, desc, probe, verdict))
        else:
            caught += 1
            print("%-3s %-56s CAUGHT   %s/%s" % (mid, desc, probe, want))

    if FORK_MANIFEST.is_file():
        print("FORK FIXTURE SURVIVED THE RUN: %s" % FORK_MANIFEST.name)
        return 2

    summary = ("\n%d mutations, %d escape(s), 0 no-op(s), %d crash(es)"
               % (len(every), len(escapes), len(crashes)))
    print(summary)
    if escapes:
        print("escaped: %s" % ", ".join(escapes))
    if crashes:
        print("crashed: %s" % ", ".join(crashes))

    # This suite's verdict reaches the release runner as TEXT. Fifteen harnesses
    # print six dialects, and a loose reader once took the 8 in "mutations=8
    # escapes=0" for the escape count. So the summary line is parsed back with
    # the SHARED parser and required to agree with what this run actually saw --
    # a harness whose own verdict is misread is worse than no harness.
    parsed = parse_summary(summary)
    agrees = (parsed.run == len(every) and parsed.escapes == len(escapes)
              and parsed.crashes == len(crashes) and parsed.no_ops == 0)
    print("summary_is_parseable_by_the_shared_parser: %s (%s)"
          % ("yes" if agrees else "NO", parsed))
    if not agrees:
        return 1

    return 1 if (escapes or crashes) else 0


if __name__ == "__main__":
    sys.exit(main())
