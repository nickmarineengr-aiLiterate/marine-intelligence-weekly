"""Adversarial mutation harness for the E2 enrichment guard.

Each mutation breaks one property validate_batch_e2.py claims to hold, runs the
validator, and requires it to FAIL for the intended reason. A mutation that is
applied but not caught is an ESCAPE. A mutation whose write changed no bytes is
a NO-OP and is reported as such rather than silently counted as a pass - a
stale anchor that no longer matches silently no-ops, which is how a mutation
harness comes to certify a guard it never actually exercised.

Beyond the standard set, E2 carries five mutations the earlier batches had no
reason to run:

  N    reintroduce one of the four deformation terms that primary verification
       could NOT substantiate. All four appear in the authorisation record and
       none appears in IACS Rec. No. 84, so "restoring" the consolidation's
       wording is a regression that no positive-token check can see.
  O/P  flatten a distinction while leaving every positive token intact - the
       automatic-versus-procedure suspension distinction (A011), and the denial
       that any universal allowable-deformation percentage exists (A013).
  Q    falsify a recorded digest, so the manifest stops describing reality.
  R    edit a timed block on an authorised card. Enrichment is body-only; a
       15/60-second block that drifts is out of scope even on a card the batch
       legitimately owns.

Mutation C deliberately targets a card that NO manifest owns, which is what
proves the sibling-manifest delegation in validate_batch_e2.py is an exemption
rather than a hole: an unowned card must still fail.

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
MANIFEST = TOOLS / "batch_e2_enrichment_manifest.json"
VALIDATOR = TOOLS / "validate_batch_e2.py"
QB_DIR = REPO / "meoclass1"

# A card owned by no batch manifest at all. Asserted at run time rather than
# trusted, because "unowned" is the whole point of mutation C.
UNOWNED = ("QB1_H.html", "q1")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run_validator():
    r = subprocess.run([sys.executable, str(VALIDATOR)],
                       cwd=REPO, capture_output=True)
    out = r.stdout.decode("utf-8", "replace")
    failed = [l.split()[1] for l in out.splitlines() if l.startswith("FAIL ")]
    return r.returncode, failed


class Mutation:
    def __init__(self, key, desc, path, fn, expect):
        self.key, self.desc, self.path, self.fn, self.expect = (
            key, desc, path, fn, expect)


def sub_once(pattern, repl, flags=0):
    def _f(text):
        new, n = re.subn(pattern, repl, text, count=1, flags=flags)
        return new if n else text
    return _f


def assert_unowned():
    owned = set()
    for sib in sorted(TOOLS.glob("batch_*_manifest.json")):
        for c in json.loads(sib.read_text(encoding="utf-8")).get("cards", []):
            owned.add((c["file"], c["anchor"]))
    return UNOWNED not in owned


def build():
    return [
        Mutation("A", "omit one authorised action from the manifest",
                 MANIFEST,
                 lambda t: json.dumps(
                     {**json.loads(t),
                      "cards": [c for c in json.loads(t)["cards"]
                                if c["action_id"] != "ENRICH-A017"]},
                     indent=2, ensure_ascii=False),
                 "authorised_action_set"),

        Mutation("B", "point an action at the wrong target card",
                 MANIFEST,
                 lambda t: t.replace('"anchor": "q15"', '"anchor": "q14"', 1),
                 "authorised_targets"),

        Mutation("C", "modify a neighbouring card no manifest owns",
                 QB_DIR / UNOWNED[0],
                 sub_once(r'(<div class="q-card"[^>]*id="%s")' % UNOWNED[1],
                          r'\1 data-e2mut="1"'),
                 "only_authorised_cards_changed"),

        Mutation("D", "blank an added missing limb (A012 repair definition)",
                 QB_DIR / "QB1_E.html",
                 lambda t: t.replace("disassembly", "dismantling"),
                 "missing_limb_supplied"),

        Mutation("E", "inject an internal action id into candidate text",
                 QB_DIR / "QB1_F.html",
                 sub_once(r"(Class Status Ladder)", r"\1 [ENRICH-A011]"),
                 "no_candidate_visible_metadata"),

        Mutation("F", "add a new q-card to a destination page",
                 QB_DIR / "QB1_H.html",
                 sub_once(r'(<div class="q-card"[^>]*id="q5")',
                          '<div class="q-card" id="q99">'
                          '<div class="q-text">injected</div></div>\\1'),
                 "no_new_canonical_card"),

        Mutation("G", "claim a different canonical total in the manifest",
                 MANIFEST,
                 lambda t: t.replace('"expected_canonical_questions": 721',
                                     '"expected_canonical_questions": 722'),
                 "canonical_total_unchanged"),

        Mutation("H", "remove a required class authority (A013 IACS Rec. 84)",
                 QB_DIR / "QB1_F.html",
                 lambda t: t.replace("Recommendation No. 84", "guidance"),
                 "required_authority_cited"),

        Mutation("I", "alter a target card's candidate question text",
                 QB_DIR / "QB1_H.html",
                 sub_once(r'(class="q-text"[^>]*>)Explain the IMO Goal-Based',
                          r"\1Explain the IMO2 Goal-Based"),
                 "q_text_and_anchors_stable"),

        Mutation("J", "claim an examiner relationship delta",
                 MANIFEST,
                 lambda t: t.replace('"expected_examiner_relationships": 960',
                                     '"expected_examiner_relationships": 961'),
                 "examiner_relationship_delta_zero"),

        Mutation("K", "delete baseline text from an authorised card (A011)",
                 QB_DIR / "QB1_F.html",
                 lambda t: t.replace("<strong>Memoranda:</strong> ", "", 1),
                 "edits_purely_additive"),

        Mutation("L", "revert one authorised card to its baseline (A020)",
                 QB_DIR / "QB1_supplementary.html",
                 sub_once(r"\r?\n *<p><strong>Why it sat where it did\."
                          r".*?limit line\.</p>", "", flags=re.S),
                 "every_authorised_card_changed"),

        Mutation("M", "declare that this batch creates new cards",
                 MANIFEST,
                 lambda t: t.replace('"creates_new_cards": false',
                                     '"creates_new_cards": true'),
                 "manifest_declares_no_new_cards"),

        Mutation("N", "reintroduce an unsubstantiated deformation term (A013)",
                 QB_DIR / "QB1_F.html",
                 lambda t: t.replace(
                     "local means a single panel or stiffener",
                     "local means a single panel or stiffener, also called "
                     "dishing", 1),
                 "unsubstantiated_claims_absent"),

        Mutation("O", "flatten the automatic/procedure distinction (A011)",
                 QB_DIR / "QB1_F.html",
                 lambda t: t.replace("subject to a suspension procedure",
                                     "automatically suspended", 1),
                 "required_qualifiers_kept"),

        Mutation("P", "assert a universal allowable-deformation rule (A013)",
                 QB_DIR / "QB1_F.html",
                 lambda t: t.replace("no single universal percentage",
                                     "a standard permitted percentage", 1),
                 "required_qualifiers_kept"),

        Mutation("Q", "falsify a recorded post-edit digest in the manifest",
                 MANIFEST,
                 lambda t: t.replace('"post_edit_digest": "1658b73523719291"',
                                     '"post_edit_digest": "0000000000000000"'),
                 "manifest_digests_match"),

        Mutation("R", "edit a timed block on an authorised card (A014)",
                 QB_DIR / "QB3_A.html",
                 lambda t: t.replace("compiling findings into the ESP file",
                                     "compiling findings into the ESP folder",
                                     1),
                 "timed_blocks_unchanged"),
    ]


def main():
    if not assert_unowned():
        print("PRE-RUN %s#%s is owned by a manifest - mutation C would not "
              "test what it claims. Pick another card." % UNOWNED)
        return 2

    before = {}
    for p in sorted(set([MANIFEST] + list(QB_DIR.glob("QB*.html")))):
        before[p] = p.read_bytes()

    code, failed = run_validator()
    if code != 0:
        print("PRE-RUN validator is not green (%s) - aborting" % failed)
        return 2

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
            code, failed = run_validator()
            if code == 0:
                escapes += 1
                verdict = "*** ESCAPE (validator stayed green) ***"
            elif mut.expect in failed:
                verdict = "caught (%s)" % mut.expect
            else:
                escapes += 1
                verdict = "*** WRONG REASON: %s ***" % (failed or "-")
            results.append((mut.key, mut.desc, verdict))
        except Exception as e:                                  # noqa: BLE001
            crashes += 1
            results.append((mut.key, mut.desc, "*** CRASH: %s ***" % e))
        finally:
            mut.path.write_bytes(orig)

    for k, d, v in results:
        print("  %-2s %-56s %s" % (k, d, v))

    intact = all(p.read_bytes() == b for p, b in before.items())
    code, failed = run_validator()
    print("\nrestored: validator exit=%d fails=%s; tree byte-identical: %s"
          % (code, failed or "-", intact))
    print("%d mutations, %d escape(s), %d no-op(s), %d crash(es)"
          % (len(results), escapes, noops, crashes))
    ok = escapes == 0 and noops == 0 and crashes == 0 and intact and code == 0
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
