"""Adversarial mutation harness for the E4 enrichment guard.

Each mutation breaks one property validate_batch_e4.py claims to hold, runs the
validator, and requires it to FAIL for the intended reason. A mutation that is
applied but not caught is an ESCAPE. A mutation whose write changed no bytes is
a NO-OP and is reported as such rather than silently counted as a pass - a
stale anchor that no longer matches silently no-ops, which is how a mutation
harness comes to certify a guard it never actually exercised.

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
MANIFEST = TOOLS / "batch_e4_enrichment_manifest.json"
VALIDATOR = TOOLS / "validate_batch_e4.py"
QB_DIR = REPO / "meoclass1"


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


def sub_once(pattern, repl):
    def _f(text):
        new, n = re.subn(pattern, repl, text, count=1)
        return new if n else text
    return _f


def build():
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return [
        Mutation("A", "omit one authorised action from the manifest",
                 MANIFEST,
                 lambda t: json.dumps(
                     {**json.loads(t),
                      "cards": [c for c in json.loads(t)["cards"]
                                if c["action_id"] != "ENRICH-A030"]},
                     indent=2),
                 "authorised_action_set"),

        Mutation("B", "point an action at the wrong target card",
                 MANIFEST,
                 lambda t: t.replace('"anchor": "q6"', '"anchor": "q5"', 1),
                 "authorised_targets"),

        Mutation("C", "modify a neighbouring unauthorised card",
                 QB_DIR / "QB6.html",
                 sub_once(r'(<div class="q-card"[^>]*id="q7")',
                          r'\1 data-e4mut="1"'),
                 "only_authorised_cards_changed"),

        Mutation("D", "blank the added missing limb (A027 carbon content)",
                 QB_DIR / "QB6.html",
                 lambda t: t.replace("0.8744", "REDACTED"),
                 "missing_limb_supplied"),

        Mutation("E", "inject an internal action id into candidate text",
                 QB_DIR / "QB7_I.html",
                 sub_once(r"(The Missing Member)", r"\1 [ENRICH-A030]"),
                 "no_candidate_visible_metadata"),

        Mutation("F", "add a new q-card to a destination page",
                 QB_DIR / "QB6_D.html",
                 sub_once(r'(<div class="q-card"[^>]*id="q2")',
                          '<div class="q-card" id="q99">'
                          '<div class="q-text">injected</div></div>\n      \\1'),
                 "no_new_canonical_card"),

        Mutation("G", "claim a different canonical total in the manifest",
                 MANIFEST,
                 lambda t: t.replace('"expected_canonical_questions": 721',
                                     '"expected_canonical_questions": 722'),
                 "canonical_total_unchanged"),

        Mutation("H", "remove a required authority reference (A032 NTC)",
                 QB_DIR / "QB1_supplementary.html",
                 lambda t: t.replace("NOx Technical Code", "the code"),
                 "required_authority_cited"),

        Mutation("I", "alter a target card's candidate question text",
                 QB_DIR / "QB3_J.html",
                 sub_once(r"(<div class=\"q-text\">)What is carbon footprint",
                          r"\1What is the carbon budget"),
                 "q_text_and_anchors_stable"),

        Mutation("J", "claim an examiner relationship delta",
                 MANIFEST,
                 lambda t: t.replace('"expected_examiner_relationships": 960',
                                     '"expected_examiner_relationships": 961'),
                 "examiner_relationship_delta_zero"),

        Mutation("K", "declare that this batch creates new cards",
                 MANIFEST,
                 lambda t: t.replace('"creates_new_cards": false',
                                     '"creates_new_cards": true'),
                 "manifest_declares_no_new_cards"),

        Mutation("L", "revert one authorised card to its baseline",
                 QB_DIR / "QB6_D.html",
                 lambda t: re.sub(
                     r"<h4>The Drive Train Behind the Pod.*?</ul>\r?\n", "", t,
                     count=1, flags=re.S),
                 "every_authorised_card_changed"),
    ]


def main():
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
        print("  %-2s %-52s %s" % (k, d, v))

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
