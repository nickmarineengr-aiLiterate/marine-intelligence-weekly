#!/usr/bin/env python3
"""
Mutation suite for Oral follow-up production batch F1.

WHAT THIS SUITE HAS TO PROVE
----------------------------
F1 is the first batch authorised by the follow-up register rather than by the
enrichment consolidation, and it ships with one of its three authorised actions
HELD.  Both of those are new shapes, and both are easy to fake:

    delete a limb                -> the limb check must go red
    corrupt a followup_id        -> the register linkage must reject it
    corrupt a target anchor      -> the register linkage must reject it
    corrupt a digest             -> the pin must reject it
    reword a q-text              -> the stability check must reject it
    edit an unauthorised card    -> delegation must not cover it
    strip relationship metadata  -> the edge must be required, not optional
    change a relationship type   -> it must match the register, not the batch
    claim a new canonical card   -> the empty exception list must hold
    corrupt a verification class -> the placeholder must not ship
    strip a currentness record   -> section 6 must be evidenced, not asserted
    touch the HELD action's card -> the hold must be enforced, not documented
    drop the HELD action's note  -> a held action must not vanish quietly
    remove F1 from the surface   -> an EARLIER guard must go red

EACH MUTATION MUST TRIP ITS OWN NAMED CHECK
-------------------------------------------
A validator that fails for the wrong reason is not evidence.  E6's mutation L
corrupted a field nothing read and was scored "caught" because something else
was already failing.  So every mutation names the check it must break, and
breaking a DIFFERENT check counts as an ESCAPE.

THE DELEGATION MUTATION IS THE IMPORTANT ONE
--------------------------------------------
F1 edits two cards that no earlier record owns.  Eleven historical guards ask
"is this card owned by some authorised record?" and answer yes only because
`batch_f1_manifest.json` is on the authorisation surface.  Mutation N removes
it and requires an earlier validator to go red.  Without that, "all guards
green" would mean nothing more than "the guards were switched off".
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
from oral_mutation import parse_summary                         # noqa: E402
from validate_batch_f1 import CARD_OPEN, cards_of               # noqa: E402

MANIFEST = HERE / "batch_f1_manifest.json"
MANIFEST_REL = "tools/oral/batch_f1_manifest.json"
REGISTER = HERE / "oral_followup_register.json"

PROBES = {
    "f1": "validate_batch_f1.py",
    # An earlier generation-2 guard whose "authorised elsewhere" scan is the
    # thing F1's presence on the surface satisfies.
    "e4": "validate_batch_e4.py",
}

# A structural byte change that says nothing, so a card-edit mutation cannot be
# mistaken for a content change.
CARD_MARKER = "<!-- f1-mutation-probe -->"


def run_probe(key: str) -> tuple[int, set]:
    """Run one validator; return (exit code, set of FAILing check names)."""
    out = subprocess.run([sys.executable, str(HERE / PROBES[key])],
                         cwd=str(REPO), capture_output=True, check=False)
    text = (out.stdout + out.stderr).decode("utf-8", "replace")
    return out.returncode, set(re.findall(r"^FAIL\s+(\S+)", text, re.M))


class Snapshot:
    """Byte-exact custody of every file a mutation touches.

    Restores from what this object personally read, never from git:
    `git checkout <ref> -- <file>` destroys uncommitted work, which has already
    cost real edits in this repository.
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


def edit_manifest(mutate) -> None:
    data = json.loads(read_text(MANIFEST))
    mutate(data)
    write_text(MANIFEST, json.dumps(data, indent=2) + "\n")


def edit_register(followup_id: str, status: str) -> None:
    data = json.loads(read_text(REGISTER))
    for action in data.get("actions", []):
        if action.get("followup_id") == followup_id:
            action["status"] = status
            write_text(REGISTER, json.dumps(data, indent=1) + "\n")
            return
    raise AssertionError("no such action in the register: %s" % followup_id)


def card_of(rel: str) -> dict:
    return cards_of(read_text(REPO / rel))


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


def pick_unauthorised_card() -> tuple[str, str]:
    """A canonical card that NO authorisation record owns.

    Chosen at runtime rather than hardcoded: a hardcoded anchor silently stops
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
                         "mutation H would be vacuous")


QB3_I = "meoclass1/QB3_I.html"
QB9_C = "meoclass1/QB9_C.html"
QB1_A = "meoclass1/QB1_A.html"          # the HELD action's parent


def build_mutations():
    """(id, description, files touched, apply, probe, required check)."""
    unauth_rel, unauth_anchor = pick_unauthorised_card()

    return [
        ("A", "remove the FUP-018 limb from QB3_I#q4",
         [REPO / QB3_I],
         lambda: strip_from_card(
             QB3_I, "<h4>Why Barnacles in Particular Cannot Attach</h4>"),
         "f1", "missing_limb_supplied"),

        ("B", "remove the FUP-033 limb from QB9_C#q5",
         [REPO / QB9_C],
         lambda: strip_from_card(
             QB9_C, "<h4>Marine Insurance Against Motor Insurance</h4>"),
         "f1", "missing_limb_supplied"),

        ("C", "edit the HELD action's parent card QB1_A#q9",
         [REPO / QB1_A],
         lambda: mark_card(QB1_A, "q9"),
         "f1", "held_action_target_untouched"),

        ("D", "corrupt a followup_id in the manifest",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][0].update(
             {"followup_id": "FUP-999", "action_id": "FUP-999"})),
         "f1", "implemented_set_is_exactly_the_two_produced"),

        ("E", "corrupt a target anchor in the manifest",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][1].update({"anchor": "q4"})),
         "f1", "parent_target_matches_register"),

        ("F", "falsify a recorded post-edit digest",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][0].update(
             {"post_edit_digest": "0000000000000000"})),
         "f1", "manifest_digests_match"),

        ("G", "reword a target card's question text",
         [REPO / QB9_C],
         lambda: reword_qtext(QB9_C, "q5"),
         "f1", "q_text_and_anchors_stable"),

        ("H", "edit a card no authorisation record owns",
         [REPO / unauth_rel],
         lambda: mark_card(unauth_rel, unauth_anchor),
         "f1", "only_authorised_cards_changed"),

        ("I", "strip the relationship edge from the manifest",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][0].pop("relationship_edge")),
         "f1", "relationship_edge_carried_unchanged"),

        ("J", "change a relationship type away from the register's",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][0].update(
             {"relationship_type": "CROSS_QUESTION"})),
         "f1", "relationship_type_matches_register"),

        ("K", "declare that the batch creates a new canonical card",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d.update({"creates_new_cards": True})),
         "f1", "no_action_creates_a_new_card"),

        ("L", "ship the register's placeholder verification class",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][1].update(
             {"verification_scope": "UNCLASSIFIED_PENDING_BATCH_SCOPING"})),
         "f1", "verification_class_governed_and_not_placeholder"),

        ("M", "strip a card's currentness record",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][1].pop("currentness")),
         "f1", "currentness_decision_recorded"),

        ("O", "drop the HELD action's structured declaration entirely",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d.pop("held_actions")),
         "f1", "held_action_is_declared_as_structure"),

        ("T", "restate the hold as a rejection instead",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["held_actions"][0].update(
             {"status": "REJECTED"})),
         "f1", "held_action_blocker_is_actionable"),

        ("U", "record the held work as no longer owed",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["held_actions"][0].update(
             {"work_still_owed": False})),
         "f1", "held_action_blocker_is_actionable"),

        ("V", "strip the hold's empirical proof",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["held_actions"][0].update(
             {"empirical_proof": ""})),
         "f1", "held_action_blocker_is_actionable"),

        ("W", "point the hold at the wrong target card",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["held_actions"][0].update(
             {"target": "QB9_C.html#q5"})),
         "f1", "held_action_blocker_is_actionable"),

        # The register is the authorisation record, not a status board. Editing
        # it to say FUP-006 was produced would make the hold disappear from the
        # only place a future session looks for outstanding work.
        ("X", "edit the register to disguise the hold as produced",
         [REGISTER],
         lambda: edit_register("FUP-006", "PRODUCED"),
         "f1", "register_status_of_held_action_untouched"),

        ("P", "strip a card's authority record",
         [MANIFEST],
         lambda: edit_manifest(lambda d: d["cards"][0].update({"authority": []})),
         "f1", "authority_recorded"),

        ("Q", "remove the examiner-chain edge from the live card",
         [REPO / QB9_C],
         lambda: strip_from_card(
             QB9_C, " &rarr; How does marine insurance differ from car insurance?"),
         "f1", "relationship_edge_present_in_card"),

        ("R", "leak internal production vocabulary to the candidate",
         [REPO / QB3_I],
         lambda: inject_into_card(
             QB3_I, "<h4>Why Barnacles in Particular Cannot Attach</h4>",
             "<p>FUP-018 GAP-0126 target_review_status</p>"),
         "f1", "no_candidate_visible_metadata"),

        ("S", "make the edit non-additive by deleting baseline text",
         [REPO / QB9_C],
         lambda: strip_from_card(
             QB9_C, "<h4>6. Proximate Cause</h4>"),
         "f1", "edits_purely_additive"),
    ]


def build_delegation_mutation():
    """Mutation N, run against an EARLIER guard rather than F1's own."""
    return ("N", "remove F1 from the authorisation surface",
            [MANIFEST],
            lambda: MANIFEST.unlink(),
            "e4", "only_authorised_cards_changed")


def main() -> int:
    if not MANIFEST.is_file():
        print("F1 manifest missing: %s" % MANIFEST_REL)
        return 2

    mutations = build_mutations()
    delegation = build_delegation_mutation()
    every = mutations + [delegation]

    # ---- preflight: every mutation must really change something ------------
    #
    # oral_mutation.preflight_or_die() dry-runs TEXT mutations in memory. Most
    # of this suite rewrites or deletes a JSON record instead, which that helper
    # cannot model, so the same contract is enforced directly: apply, compare
    # bytes, restore. Same guarantee -- no mutation reaches the expensive probe
    # phase without proving it changes bytes. E5's mutation C and E6's mutation
    # H each matched nothing, wrote nothing and exercised nothing; E6 spent 22
    # minutes discovering it.
    print("--- preflight: every mutation must change bytes ---")
    no_ops = []
    for mid, desc, files, apply, _probe, _check in every:
        snap = Snapshot(files)
        before = dict(snap.data)
        try:
            apply()
        except Exception as exc:
            print("%-3s ERROR %s: %s" % (mid, type(exc).__name__, exc))
            no_ops.append(mid)
            snap.restore()
            continue
        after = {p: (p.read_bytes() if p.is_file() else None) for p in snap.data}
        changed = any(before[p] != after[p] for p in before)
        delta = sum((len(after[p] or b"") - len(before[p] or b"")) for p in before)
        print("%-3s %-54s %-7s byte_delta=%+d"
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

    # ---- control: unmutated, both probes must be green ---------------------
    print("\n--- control: unmutated state ---")
    control_bad = []
    for key in ("f1", "e4"):
        rc, failing = run_probe(key)
        print("    %-4s exit=%d failing=%s" % (key, rc, sorted(failing) or "none"))
        if failing:
            control_bad.append(key)
    escapes, crashes = [], []
    if control_bad:
        print("    CONTROL IS NOT GREEN (%s) -- every later 'catch' is meaningless"
              % ", ".join(control_bad))
        escapes.append("CONTROL")

    # ---- the suite ---------------------------------------------------------
    print("\n--- mutations ---")
    caught = 0
    for mid, desc, files, apply, probe, want in every:
        snap = Snapshot(files)
        try:
            apply()
            rc, failing = run_probe(probe)
        except Exception as exc:
            print("%-3s %-54s CRASH %s" % (mid, desc, exc))
            crashes.append(mid)
            snap.restore()
            continue
        finally:
            restore_failed = snap.restore()
        if restore_failed:
            print("    RESTORE FAILED: %s" % restore_failed)
            return 2

        # The NAMED check must be the one that broke. Failing for some other
        # reason is not evidence that this mutation was detected.
        if want in failing:
            caught += 1
            print("%-3s %-54s CAUGHT   %s/%s" % (mid, desc, probe, want))
        else:
            escapes.append(mid)
            print("%-3s %-54s ESCAPED  %s wanted=%s got=%s"
                  % (mid, desc, probe, want, sorted(failing) or "none"))

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
