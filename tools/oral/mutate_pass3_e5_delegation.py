#!/usr/bin/env python3
"""
GPT REVIEW PASS 3 -- adversarial audit of the ``edits_purely_additive``
delegation added to ``validate_batch_e5`` in Pass 2B.

WHAT WAS CHANGED
----------------

    OLD   any card of E5's whose LIVE bytes differ from its baseline by
          anything other than an insertion fails ``edits_purely_additive``.

    NEW   the same, EXCEPT where the card is owned by some OTHER
          authorisation record, in which case the difference is attributed to
          that record and reported as ``authorised-elsewhere``.

The stated justification is that a correction REPLACES text by definition, so
compared against LIVE the old form silently asserted "no correction has ever
edited one of my cards" -- a claim that expires the first time one does.

THAT JUSTIFICATION IS ALSO EXACTLY WHAT A BACKDOOR WOULD SAY.  The danger is
that the exemption stops being per-card and becomes "anything later is
allowed", at which point E5's strongest guard is off and its output still says
PASS.  So every mutation below attacks the exemption itself:

    edit an E5 card NOBODY owns          -> E5 must still fail
    delete content from an E5 card       -> E5 must still fail
    edit the owned card arbitrarily      -> the PIN gate must catch it
    plant a manifest naming another card -> the exemption must not transfer
    corrupt the owner's pre-digest       -> the pin gate must reject it
    corrupt the owner's post-digest      -> the pin gate must reject it
    remove the owner record              -> the exemption must evaporate

WHY TWO PROBES AND NOT ONE
--------------------------
The exemption is one half of a two-half contract: E5 stops policing a card
another record owns, and ``validate_corrections`` pins that card's exact
authorised state.  A mutation that E5 is DESIGNED to ignore is therefore not
an escape -- but it is only not an escape if the pin gate catches it, so this
suite requires the catch and names which gate made it.  A mutation that
neither gate catches is a real hole and is reported as an ESCAPE.

CUSTODY
-------
Every mutation runs inside ``oral_custody.Custodian``, so an interruption at
any point restores the tree, and a hard kill leaves a journal the next run
refuses to walk past.  See ``oral_custody`` for the layer boundaries.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
QB = REPO / "meoclass1"
sys.path.insert(0, str(HERE))

from oral_bytes import read_text, write_text                        # noqa: E402
from oral_custody import Custodian, CustodyError                    # noqa: E402
from oral_manifest import sibling_owned_cards                       # noqa: E402
from validate_batch_b import CARD_OPEN, _balanced_end               # noqa: E402

E5 = HERE / "batch_e5_enrichment_manifest.json"
FAKE = HERE / "correction_corr_pass3fakegrant_20260904_manifest.json"

PROBES = {"e5": "validate_batch_e5.py", "corrections": "validate_corrections.py"}


def run_probe(key):
    out = subprocess.run([sys.executable, str(HERE / PROBES[key])],
                         cwd=str(REPO), capture_output=True, check=False)
    text = (out.stdout + out.stderr).decode("utf-8", "replace")
    failing = set(re.findall(r"^FAIL\s+(\S+)", text, re.M))
    for payload in re.findall(r"violations=\[([^\]]*)\]", text):
        failing.update(re.findall(r"'([^']+)'", payload))
    return out.returncode, failing, text


# ---------------------------------------------------------------- card surgery

def card_span(text, anchor):
    for m in CARD_OPEN.finditer(text):
        got = re.search(r'\bid="([^"]+)"', m.group(0))
        if got and got.group(1) == anchor:
            return m.start(), _balanced_end(text, m.start())
    raise AssertionError("card not found: %s" % anchor)


def delete_a_word(rel, anchor):
    """Remove one word from inside a card.

    A DELETION, deliberately: ``edits_purely_additive`` accepts ``equal`` and
    ``insert`` opcodes, so only a delete or replace can prove the check is
    still live.  An insertion would pass on a correct implementation and on a
    disabled one alike.
    """
    path = REPO / rel
    text = read_text(path)
    s, e = card_span(text, anchor)
    block = text[s:e]
    hit = block.find(" the ")
    if hit < 0:
        raise AssertionError("no deletable word in %s#%s" % (rel, anchor))
    write_text(path, text[:s] + block[:hit] + " " + block[hit + 5:] + text[e:])


def append_marker(rel, anchor):
    """A purely ADDITIVE edit -- the shape the exemption is supposed to cover."""
    path = REPO / rel
    text = read_text(path)
    s, e = card_span(text, anchor)
    marker = "<!--pass3-additive-->"
    write_text(path, text[:e - 6] + marker + text[e - 6:])


def edit_manifest(path, mutate):
    data = json.loads(read_text(path))
    mutate(data)
    write_text(path, json.dumps(data, indent=2) + "\n")


# --------------------------------------------------------------- target choice

def pick_targets():
    """An E5 card NOBODY else owns, and the E5 card the correction DOES own.

    Chosen at runtime.  A hardcoded anchor silently stops testing anything the
    day a future record authorises that card -- the same trap
    ``mutate_corrections.pick_unowned_batch_b_card`` was written to avoid.
    """
    cards = json.loads(read_text(E5))["cards"]
    owned = sibling_owned_cards(E5)
    unowned = [c for c in cards if "%s#%s" % (c["file"], c["anchor"]) not in owned]
    shared = [c for c in cards if "%s#%s" % (c["file"], c["anchor"]) in owned]
    if not unowned:
        raise AssertionError("every E5 card is owned elsewhere; the negative "
                             "mutations would be vacuous")
    if not shared:
        raise AssertionError("no E5 card is owned elsewhere; the exemption is "
                             "never exercised and this audit proves nothing")
    return unowned[0], shared[0]


FAKE_RECORD = {
    "correction_id": "CORR-PASS3FAKEGRANT-20260904",
    "title": "PASS 3 CONTROL -- a manifest nobody authorised",
    "date": "2026-09-04",
    "kind": "POST_RELEASE_CORRECTION",
    "status": "AUTHORISED",
    "baseline_commit": "HEAD",
    "cards": [],
}


def main() -> int:
    from oral_custody import stale_runs
    if stale_runs(REPO):
        print("REFUSING TO RUN -- unrecovered mutation journal present; run "
              "`python tools/oral/mutate_corrections.py --recover` first")
        return 2

    unowned, shared = pick_targets()
    u_rel = "meoclass1/" + unowned["file"]
    s_rel = "meoclass1/" + shared["file"]
    u_id = "%s#%s" % (unowned["file"], unowned["anchor"])
    s_id = "%s#%s" % (shared["file"], shared["anchor"])
    print("E5 card owned by NOBODY else : %s" % u_id)
    print("E5 card owned by a correction: %s" % s_id)

    owner = None
    for path in sorted(HERE.glob("correction_*_manifest.json")):
        rec = json.loads(read_text(path))
        if any("%s#%s" % (c.get("file"), c.get("anchor")) == s_id
               for c in rec.get("cards", [])):
            owner = path
            break
    if owner is None:
        print("no correction record owns %s -- audit would be vacuous" % s_id)
        return 2
    print("owner record                 : %s\n" % owner.name)

    dirt_before = subprocess.run(["git", "status", "--porcelain"], cwd=str(REPO),
                                 capture_output=True).stdout

    # (id, description, files, apply, must_fail[, must_stay_green])
    #
    # TWO LIMBS, BECAUSE THE CONTRACT HAS TWO HALVES. A mutation that E5 is
    # DESIGNED to ignore is not an escape -- but it is only not an escape if
    # the PIN gate catches it, and the claim is only meaningful if E5 really
    # did stay quiet. Asserting both is what distinguishes "the delegation is
    # correctly narrow" from "the delegation switched a guard off and something
    # else happened to fail". must_stay_green is optional; most mutations have
    # nothing to say about it.
    mutations = [
        ("D2", "delete a word from an E5 card NOBODY else owns",
         [REPO / u_rel], lambda: delete_a_word(u_rel, unowned["anchor"]),
         [("e5", "edits_purely_additive")]),

        # An INSERTION is exactly what `edits_purely_additive` exists to
        # permit, so that check must stay green -- and the card's digest pin
        # must catch the edit anyway. The first run of this suite expected E5
        # to be entirely silent here and was WRONG: additive-ness is not a
        # licence, and `manifest_digests_match` still binding on an
        # unauthorised insertion is the proof that the Pass 2B change did not
        # weaken the pin.
        ("D2b", "purely ADDITIVE edit to that same unowned card",
         [REPO / u_rel], lambda: append_marker(u_rel, unowned["anchor"]),
         [("e5", "manifest_digests_match")], [("e5", "edits_purely_additive")]),

        ("D3", "plant a fake manifest naming the unowned card, then damage it",
         [FAKE, REPO / u_rel],
         lambda: (write_text(FAKE, json.dumps(
             dict(FAKE_RECORD, cards=[{"correction_action_id": "FAKE-01",
                                       "file": unowned["file"],
                                       "path": u_rel,
                                       "anchor": unowned["anchor"]}]),
             indent=2) + "\n"),
             delete_a_word(u_rel, unowned["anchor"])),
         [("corrections", "ANY")], [("e5", "edits_purely_additive")]),

        ("D4", "plant a fake manifest naming a DIFFERENT card, damage the unowned one",
         [FAKE, REPO / u_rel],
         lambda: (write_text(FAKE, json.dumps(
             dict(FAKE_RECORD, cards=[{"correction_action_id": "FAKE-02",
                                       "file": shared["file"],
                                       "path": s_rel,
                                       "anchor": shared["anchor"]}]),
             indent=2) + "\n"),
             delete_a_word(u_rel, unowned["anchor"])),
         [("e5", "edits_purely_additive")]),

        ("D5", "damage the card the correction DOES own",
         [REPO / s_rel], lambda: delete_a_word(s_rel, shared["anchor"]),
         [("corrections", "live_matches_authorised_post_state")]),

        ("D6", "corrupt the owner's pre-edit digest",
         [owner],
         lambda: edit_manifest(owner, lambda d: [
             c.__setitem__("pre_edit_digest", "0" * 64)
             for c in d["cards"]
             if "%s#%s" % (c["file"], c["anchor"]) == s_id]),
         [("corrections", "pre_edit_digests_match_baseline")]),

        ("D7", "corrupt the owner's post-edit digest",
         [owner],
         lambda: edit_manifest(owner, lambda d: [
             c.__setitem__("post_edit_digest", "0" * 64)
             for c in d["cards"]
             if "%s#%s" % (c["file"], c["anchor"]) == s_id]),
         [("corrections", "live_matches_authorised_post_state")]),

        ("D8", "point the owner's card entry at a different anchor",
         [owner],
         lambda: edit_manifest(owner, lambda d: [
             c.__setitem__("anchor", "q999")
             for c in d["cards"]
             if "%s#%s" % (c["file"], c["anchor"]) == s_id]),
         [("e5", "manifest_digests_match")]),
    ]

    cust = Custodian(REPO, name="pass3-e5")
    escapes, crashes, caught = [], [], 0
    try:
        # ---- preflight ----------------------------------------------------
        print("--- preflight: every mutation must change bytes ---")
        no_ops = []
        for mid, desc, files, apply, *_ in mutations:
            with cust.guard(files):
                try:
                    apply()
                except Exception as exc:
                    print("%-4s ERROR %s: %s" % (mid, type(exc).__name__, exc))
                    no_ops.append(mid)
                    continue
                changed = any(
                    cust.original(p) != (pathlib.Path(p).read_bytes()
                                         if pathlib.Path(p).is_file() else None)
                    for p in files)
                print("%-4s %-62s %s" % (mid, desc,
                                         "applied" if changed else "NO-OP"))
                if not changed:
                    no_ops.append(mid)
        if no_ops:
            print("\npreflight FAILED -- no-ops: %s" % ", ".join(no_ops))
            return 1

        # ---- control ------------------------------------------------------
        print("\n--- control: unmutated, and the exemption must be EXERCISED ---")
        control = {}
        for key in ("e5", "corrections"):
            rc, failing, text = run_probe(key)
            control[key] = failing
            print("CTL  %-12s exit=%d failing=%s"
                  % (key, rc, sorted(failing) or "none"))
            if key == "e5":
                m = re.search(r"edits_purely_additive.*?authorised-elsewhere=(\S.*)",
                              text)
                detail = m.group(1).strip() if m else "-"
                print("CTL  edits_purely_additive authorised-elsewhere=%s" % detail)
                # NON-VACUITY.  If nothing is exempted, the changed line is
                # never taken and this whole audit tests dead code.
                if detail in ("-", "['-']", ""):
                    print("CTL  THE EXEMPTION IS NEVER EXERCISED -- audit vacuous")
                    escapes.append("CTL-vacuous")
        if control["e5"] or control["corrections"]:
            print("CTL  CONTROL IS NOT GREEN -- every later catch is meaningless")
            escapes.append("CTL")

        # ---- mutations ----------------------------------------------------
        print("\n--- mutations ---")
        for entry in mutations:
            mid, desc, files, apply, wants = entry[:5]
            green = entry[5] if len(entry) > 5 else []
            probes = sorted({p for p, _ in wants} | {p for p, _ in green})
            with cust.guard(files):
                try:
                    apply()
                    results = {p: run_probe(p)[1] for p in probes}
                except Exception as exc:
                    print("%-4s %-62s CRASH %s" % (mid, desc, exc))
                    crashes.append(mid)
                    continue

            problems, notes = [], []
            for probe, want in wants:
                new = results[probe] - control.get(probe, set())
                if want == "ANY":
                    if new:
                        notes.append("%s caught on %s" % (probe, sorted(new)))
                    else:
                        problems.append("%s caught NOTHING" % probe)
                elif want in new:
                    notes.append("%s/%s" % (probe, want))
                else:
                    problems.append("%s wanted=%s got=%s"
                                    % (probe, want, sorted(new) or "none"))
            for probe, must_stay in green:
                new = results[probe] - control.get(probe, set())
                if must_stay in new:
                    problems.append("%s/%s went red and must not have"
                                    % (probe, must_stay))
                else:
                    notes.append("%s/%s stayed green" % (probe, must_stay))

            if problems:
                escapes.append(mid)
                print("%-4s %-62s %-9s %s" % (mid, desc, "ESCAPED",
                                              "; ".join(problems)))
            else:
                caught += 1
                print("%-4s %-62s %-9s %s" % (mid, desc, "CAUGHT",
                                              "; ".join(notes)))

        print("\n%d mutations, %d escape(s), %d crash(es)"
              % (len(mutations), len(escapes), len(crashes)))
        if escapes:
            print("escaped: %s" % ", ".join(escapes))

        # ---- closing integrity --------------------------------------------
        print("\n--- closing integrity ---")
        drift = cust.verify_pristine()
        dirt_after = subprocess.run(["git", "status", "--porcelain"],
                                    cwd=str(REPO), capture_output=True).stdout
        print("custody drift: %s" % (drift or "none"))
        print("git status restored: %s" % (dirt_after == dirt_before))
        if drift or dirt_after != dirt_before:
            print("HARD FAIL -- the working tree was NOT restored.")
            return 2
        return 1 if (escapes or crashes) else 0
    finally:
        leftover = cust.restore_all()
        if leftover:
            print("SUITE-LEVEL RESTORE FAILED: %s" % leftover)
        cust.close()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CustodyError as exc:
        print("\nHARD FAIL -- custody: %s" % exc)
        sys.exit(2)
