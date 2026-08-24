"""Adversarial mutation harness for the E3 enrichment guard.

Each mutation breaks one property validate_batch_e3.py claims to hold, runs the
validator, and requires it to FAIL for the intended reason. A mutation that is
applied but not caught is an ESCAPE. A mutation whose write changed no bytes is
a NO-OP and is reported as such rather than silently counted as a pass - a
stale anchor that no longer matches silently no-ops, which is how a mutation
harness comes to certify a guard it never actually exercised.

Beyond the standard set, E3 carries four mutations the earlier batches had no
reason to run:

  M/N  reintroduce a claim primary verification DISPROVED, and strip the
       condition that keeps a claim true. Both would "restore" the wording of
       the authorisation record, which is exactly why a positive-token check
       cannot catch them.
  O    make an authorised edit non-additive by deleting baseline text. An
       enrichment that quietly drops an existing reference while adding a new
       one still looks like a correctly-changed card to every other check.
  P    falsify a recorded digest, so the manifest stops describing reality.

Every mutation is applied to a real file and restored byte-exactly afterwards,
and the run ends by asserting the tree is byte-identical to how it started.

Exit 0 only when every mutation was applied, caught, and restored.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
MANIFEST = TOOLS / "batch_e3_enrichment_manifest.json"
VALIDATOR = TOOLS / "validate_batch_e3.py"

sys.path.insert(0, str(TOOLS))
from oral_mutation import (              # noqa: E402
    require_control_baseline, mutation_verdict, validator_fail_details)
from oral_release_gates import BASELINE_REF   # noqa: E402
QB_DIR = REPO / "meoclass1"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run_validator():
    r = subprocess.run([sys.executable, str(VALIDATOR)],
                       cwd=REPO, capture_output=True)
    out = r.stdout.decode("utf-8", "replace")
    failed = [l.split()[1] for l in out.splitlines() if l.startswith("FAIL ")]
    # The DETAIL is returned as well as the name. A mutation aimed at a check
    # that is already failing on the control can never make a new NAME appear,
    # so its only available proof is that the check's reported content moved.
    return r.returncode, failed, validator_fail_details(out)


class Mutation:
    def __init__(self, key, desc, path, fn, expect):
        self.key, self.desc, self.path, self.fn, self.expect = (
            key, desc, path, fn, expect)


def sub_once(pattern, repl, flags=0):
    def _f(text):
        new, n = re.subn(pattern, repl, text, count=1, flags=flags)
        return new if n else text
    return _f


def build():
    return [
        Mutation("A", "omit one authorised action from the manifest",
                 MANIFEST,
                 lambda t: json.dumps(
                     {**json.loads(t),
                      "cards": [c for c in json.loads(t)["cards"]
                                if c["action_id"] != "ENRICH-A024"]},
                     indent=2),
                 "authorised_action_set"),

        Mutation("B", "point an action at the wrong target card",
                 MANIFEST,
                 lambda t: t.replace('"anchor": "q4"', '"anchor": "q3"', 1),
                 "authorised_targets"),

        Mutation("C", "modify a neighbouring unauthorised card",
                 QB_DIR / "QB2_I.html",
                 sub_once(r'(<div class="q-card"[^>]*id="q5")',
                          r'\1 data-e3mut="1"'),
                 "only_authorised_cards_changed"),

        Mutation("D", "blank the added missing limb (A025 weighing method)",
                 QB_DIR / "QB2_I.html",
                 lambda t: t.replace("hanging bars", "some means"),
                 "missing_limb_supplied"),

        Mutation("E", "inject an internal action id into candidate text",
                 QB_DIR / "QB2_G.html",
                 sub_once(r"(Load Line stow criteria)", r"\1 [ENRICH-A023]"),
                 "no_candidate_visible_metadata"),

        Mutation("F", "add a new q-card to a destination page",
                 QB_DIR / "QB2_G.html",
                 sub_once(r'(<div class="q-card"[^>]*id="q2")',
                          '<div class="q-card" id="q99">'
                          '<div class="q-text">injected</div></div>\\1'),
                 "no_new_canonical_card"),

        Mutation("G", "claim a different canonical total in the manifest",
                 MANIFEST,
                 lambda t: t.replace('"expected_canonical_questions": 721',
                                     '"expected_canonical_questions": 722'),
                 "canonical_total_unchanged"),

        Mutation("H", "remove a required authority reference (A022 CSM circ.)",
                 QB_DIR / "QB2_B.html",
                 lambda t: t.replace("MSC.1/Circ.1353/Rev.2", "the guidelines"),
                 "required_authority_cited"),

        Mutation("I", "alter a target card's candidate question text",
                 QB_DIR / "QB8_G.html",
                 sub_once(r'(<div class="q-text">)IGC Code', r"\1IMDG Code"),
                 "q_text_and_anchors_stable"),

        Mutation("J", "claim an examiner relationship delta",
                 MANIFEST,
                 lambda t: t.replace('"expected_examiner_relationships": 958',
                                     '"expected_examiner_relationships": 959'),
                 "examiner_relationship_delta_zero"),

        Mutation("K", "declare that this batch creates new cards",
                 MANIFEST,
                 lambda t: t.replace('"creates_new_cards": false',
                                     '"creates_new_cards": true'),
                 "manifest_declares_no_new_cards"),

        Mutation("L", "revert one authorised card to its baseline (A026)",
                 QB_DIR / "QB2_A.html",
                 sub_once(r"\r?\n<h4>AVD .*?once there is access\.</p>", "",
                          flags=re.S),
                 "every_authorised_card_changed"),

        Mutation("M", "reintroduce the disproved 'ceramic' descriptor (A026)",
                 QB_DIR / "QB2_A.html",
                 sub_once(r"(The mineral itself is inert)",
                          r"The dried residue is ceramic-like. \1"),
                 "disproved_claims_absent"),

        Mutation("N", "strip the condition from the 56.4 exclusion (A021)",
                 QB_DIR / "QB8_G.html",
                 lambda t: t.replace(
                     "the fuel storage and distribution system design and "
                     "arrangements comply", "the arrangements comply"),
                 "conditional_qualifiers_kept"),

        Mutation("O", "delete baseline text from an authorised card (A023)",
                 QB_DIR / "QB2_G.html",
                 lambda t: t.replace("<strong>Fire risk:</strong> ", "", 1),
                 "edits_purely_additive"),

        Mutation("P", "falsify a recorded post-edit digest in the manifest",
                 MANIFEST,
                 lambda t: t.replace('"post_edit_digest": "dda365fb7bcef84e"',
                                     '"post_edit_digest": "0000000000000000"'),
                 "manifest_digests_match"),
    ]


def main():
    before = {}
    for p in sorted(set([MANIFEST] + list(QB_DIR.glob("QB*.html")))):
        before[p] = p.read_bytes()

    # CONTROL STATE, NOT ABSOLUTE GREEN.
    #
    # A mutation suite proves the validator catches corruption, so the control
    # must carry no failure the mutations did not cause. That is NOT the same as
    # carrying no failure at all. `validate_batch_e6` fails
    # `line_endings_homogeneous_per_file` on a clean checkout of the very commit
    # it certified -- non-reproducible historical evidence that must not be
    # repaired, rebaselined or silenced. Demanding absolute green made that
    # suite unlaunchable, and a guard that cannot run has silently expired.
    #
    # The baseline is DERIVED from the ref on every run, never declared, and is
    # derived at all only when the control is not already green. Identity is
    # compared, never count: a same-sized but different failure is a regression,
    # and strictly fewer failures is an improvement.
    code, failed, control_details = run_validator()
    control = require_control_baseline(failed, VALIDATOR.relative_to(REPO),
                                       REPO, ref=BASELINE_REF)
    if not control.runnable:
        print("PRE-RUN %s - aborting" % control.reason)
        return 2
    baseline = control.control_failures

    escapes = noops = crashes = 0
    results = []
    for mut in build():
        orig = mut.path.read_bytes()
        try:
            text = orig.decode("utf-8")
            mut.path.write_bytes(mut.fn(text).encode("utf-8"))
            applied = mut.path.read_bytes() != orig
            if not applied:
                noops += 1
                results.append((mut.key, mut.desc, "NO-OP (not applied)"))
                continue
            code, failed, details = run_validator()
            # `code == 0` cannot be the escape test once the control carries a
            # pre-existing failure: the validator then never exits 0 and every
            # mutation would read as caught. The question is whether a NEW
            # failing check appeared, and whether it is the intended one. With
            # an empty baseline this is exactly the original semantics.
            outcome, verdict = mutation_verdict(
                mut.expect, failed, baseline, details, control_details)
            if outcome == "escape":
                escapes += 1
            results.append((mut.key, mut.desc, verdict))
        except Exception as e:                                  # noqa: BLE001
            crashes += 1
            results.append((mut.key, mut.desc, "*** CRASH: %s ***" % e))
        finally:
            mut.path.write_bytes(orig)

    for k, d, v in results:
        print("  %-2s %-54s %s" % (k, d, v))

    intact = all(p.read_bytes() == b for p, b in before.items())
    code, failed, _details = run_validator()
    # The restored tree must return to the CONTROL state, not to absolute green.
    # Anything the restore failed to put back shows up here as a failing check
    # the control did not have.
    residue = sorted(set(failed) - set(baseline))
    print("\nrestored: validator exit=%d fails=%s; control baseline=%s; "
          "new-vs-control=%s; tree byte-identical: %s"
          % (code, failed or "-", sorted(baseline) or "-", residue or "-", intact))
    print("%d mutations, %d escape(s), %d no-op(s), %d crash(es)"
          % (len(results), escapes, noops, crashes))
    ok = (escapes == 0 and noops == 0 and crashes == 0 and intact
          and not residue)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
