"""Adversarial mutation harness for the E5 enrichment guard.

Each mutation breaks one property validate_batch_e5.py claims to hold, runs the
validator, and requires it to FAIL for the intended reason. A mutation that is
applied but not caught is an ESCAPE. A mutation whose write changed no bytes is
a NO-OP and is reported as such rather than silently counted as a pass - a
stale anchor that no longer matches silently no-ops, which is how a mutation
harness comes to certify a guard it never actually exercised.

READING THIS HARNESS'S OUTPUT
A caught mutation prints the validator's own FAIL line. Those FAIL strings are
CAUGHT-MUTATION EVIDENCE, not gate failures - grepping this log for "FAIL"
inverts its meaning. Classify from the final summary line only: mutations,
escapes, no-ops, crashes.

Beyond the standard set, E5 carries the mutations its subject matter needs.

  M/N/O  the shared-target trio. ENRICH-A036 and ENRICH-A037 both land on
         QB4_C.html#q6, so the card looks correct with only one of them
         accounted for. M drops A036 and leaves A037; N drops A037 and leaves
         A036; O collapses the two identities into a single action id. All
         three keep the page byte-identical and keep the arithmetic plausible,
         which is exactly why they need dedicated coverage rather than a count.

  P/Q    the MLC Part A / Part B pair, in both directions. P makes a mandatory
         Standard read as guidance; Q makes a Guideline read as mandatory.
         Neither removes a positive token, so only a dedicated negative guard
         can see them.

  R/U    currentness. R staledates the entry-into-force of the 2022 amendments;
         U asserts that the April 2025 amendments are in force when they are
         adopted and not yet in force. Collapsing adopted into in-force is the
         defect the batch brief names.

  S      deletes the Load Line disclaimer on A036. The consolidation asked for
         door sill and coaming heights as MLC accommodation minima; they are
         not in Standard A3.1 at all. The card carries the correction instead,
         and losing it leaves the reader with the original error.

  T      flattens A043's thesis. The card teaches that harassment is not to be
         informally mediated; the authorised ladder begins at counselling. Drop
         the sentence that scopes the ladder to the disciplinary response and
         the addition silently contradicts the card it was added to.

  Y      asserts the accommodation dimensions bind every ship afloat, dropping
         the Regulation 3.1(2) construction-date limitation.

Mutation C deliberately targets a card that NO manifest owns, which is what
proves the sibling-manifest delegation in validate_batch_e5.py is an exemption
for authorised cards rather than a hole. The harness asserts that card is
genuinely unowned at run time instead of trusting it.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
MANIFEST = TOOLS / "batch_e5_enrichment_manifest.json"
VALIDATOR = TOOLS / "validate_batch_e5.py"

sys.path.insert(0, str(TOOLS))
from oral_mutation import (              # noqa: E402
    require_control_baseline, mutation_verdict, validator_fail_details)
from oral_release_gates import BASELINE_REF   # noqa: E402
QB_DIR = REPO / "meoclass1"

# A card owned by no batch manifest at all. Asserted at run time rather than
# trusted, because "unowned" is the whole point of mutation C.
UNOWNED = ("QB1_H.html", "q1")

BASELINE = "e47c7e6"


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


def edit_manifest(fn):
    def _f(text):
        d = json.loads(text)
        fn(d)
        return json.dumps(d, indent=1, ensure_ascii=False)
    return _f


def _drop(d, aid):
    d["cards"] = [c for c in d["cards"] if c["action_id"] != aid]


def _card(d, aid):
    return [c for c in d["cards"] if c["action_id"] == aid][0]


def baseline_of(page):
    r = subprocess.run(["git", "show", "%s:meoclass1/%s" % (BASELINE, page)],
                       cwd=REPO, capture_output=True)
    return r.stdout.decode("utf-8")


def assert_unowned():
    owned = set()
    for sib in sorted(TOOLS.glob("batch_*_manifest.json")):
        for c in json.loads(sib.read_text(encoding="utf-8")).get("cards", []):
            owned.add((c["file"], c["anchor"]))
    return UNOWNED not in owned


NEW_CARD = (
    '<div class="q-card" id="q98" data-tags="stcw">\n'
    '  <div class="q-header"><div class="q-num-badge">98</div>'
    '<div class="q-text-wrap"><div class="q-text">Injected.</div></div></div>\n'
    '  <div class="q-answer"><div class="answer-body"><p>Injected.</p></div></div>\n'
    '</div>\n')


def build():
    return [
        Mutation("A", "omit one authorised action from the manifest",
                 MANIFEST, edit_manifest(lambda d: _drop(d, "ENRICH-A044")),
                 "authorised_action_set"),
        Mutation("B", "retarget an action to the wrong anchor",
                 MANIFEST,
                 edit_manifest(lambda d: _card(d, "ENRICH-A033")
                               .__setitem__("anchor", "q21")),
                 "authorised_targets"),
        Mutation("C", "alter a neighbouring card no manifest owns",
                 QB_DIR / UNOWNED[0],
                 # Anchored INSIDE the unowned card, not at end-of-file: the
                 # page ends with </html>, so an end-of-file </div> anchor
                 # silently no-ops and this mutation certifies nothing.
                 sub_once(r'(<div class="q-card" id="q1" data-tags="iacs ism">)',
                          r'\1<!--injected-->'),
                 "only_authorised_cards_changed"),
        Mutation("D", "blank one supplied limb (A042 taxonomy)",
                 QB_DIR / "QB4_B.html",
                 sub_once(r"<strong>Condition-based:</strong>",
                          "<strong>Reactive:</strong>"),
                 "missing_limb_supplied"),
        Mutation("E", "inject an internal action id into candidate prose",
                 QB_DIR / "QB4_B.html",
                 sub_once(r"Naming the Types of Maintenance",
                          "Naming the Types of Maintenance ENRICH-A042"),
                 "no_candidate_visible_metadata"),
        Mutation("F", "add a canonical q-card",
                 QB_DIR / "QB5_C_A.html",
                 sub_once(r'(<div class="q-card" id="q7")', NEW_CARD + r"\1"),
                 "canonical_total_unchanged"),
        Mutation("G", "misstate the canonical corpus total",
                 MANIFEST,
                 edit_manifest(lambda d: d.__setitem__(
                     "expected_canonical_questions", 720)),
                 "canonical_total_unchanged"),
        Mutation("H", "strip a required STCW authority (A033)",
                 QB_DIR / "QB4_A.html",
                 sub_once(r"<strong>STCW Regulation III/1</strong>",
                          "<strong>The entry regulation</strong>"),
                 "required_authority_cited"),
        Mutation("I", "alter the q-text of an authorised card",
                 QB_DIR / "QB4_A.html",
                 sub_once(r"(<div class=\"q-text\">)Moving from Second Engineer",
                          r"\1Moving from Third Engineer"),
                 "q_text_and_anchors_stable"),
        Mutation("J", "claim an examiner relationship delta",
                 MANIFEST,
                 edit_manifest(lambda d: d.__setitem__(
                     "expected_examiner_relationships", 961)),
                 "examiner_relationship_delta_zero"),
        Mutation("K", "delete baseline text from an authorised card",
                 QB_DIR / "QB4_C.html",
                 sub_once(r"<li><strong>Title 5: Compliance and enforcement:</strong>"
                          r"[^<]*</li>", ""),
                 "edits_purely_additive"),
        Mutation("L", "break manifest/consolidation disposition identity",
                 MANIFEST,
                 edit_manifest(lambda d: _card(d, "ENRICH-A040")
                               .__setitem__("verification_scope",
                                            "TECHNICAL_REASONING_ONLY")),
                 "authorised_enrichment_disposition"),
        Mutation("M", "drop A036 but leave A037 on the shared card",
                 MANIFEST, edit_manifest(lambda d: _drop(d, "ENRICH-A036")),
                 "shared_target_actions_enumerated"),
        Mutation("N", "drop A037 but leave A036 on the shared card",
                 MANIFEST, edit_manifest(lambda d: _drop(d, "ENRICH-A037")),
                 "shared_target_actions_enumerated"),
        Mutation("O", "collapse A036 and A037 into one action id",
                 MANIFEST,
                 edit_manifest(lambda d: _card(d, "ENRICH-A037")
                               .__setitem__("action_id", "ENRICH-A036")),
                 "shared_target_actions_enumerated"),
        Mutation("P", "make a mandatory MLC Standard read as guidance",
                 QB_DIR / "QB4_C.html",
                 sub_once(r"<strong>Standard A3\.1</strong> states them:",
                          "<strong>Standard A3.1</strong> is only guidance, "
                          "but states them:"),
                 "mlc_part_a_and_b_not_conflated"),
        Mutation("Q", "make MLC Part B guidance read as mandatory",
                 QB_DIR / "QB4_C.html",
                 sub_once(r"(<h4>Title 3 Accommodation)",
                          r"<p>Guideline B3.1.5 is mandatory.</p>\1"),
                 "mlc_part_a_and_b_not_conflated"),
        Mutation("R", "staledate the 2022 amendments' entry into force",
                 QB_DIR / "QB4_H.html",
                 sub_once(r"23 December 2024", "23 December 2014"),
                 "required_qualifiers_kept"),
        Mutation("S", "delete the Load Line disclaimer on A036",
                 QB_DIR / "QB4_C.html",
                 sub_once(r"not MLC ones", "not relevant here"),
                 "required_qualifiers_kept"),
        Mutation("T", "flatten A043's not-a-mediation thesis",
                 QB_DIR / "QB5_D.html",
                 sub_once(r"never a menu for settling the matter between the "
                          r"two seafarers", "a practical way forward"),
                 "required_qualifiers_kept"),
        Mutation("U", "assert the April 2025 amendments are in force",
                 QB_DIR / "QB4_H.html",
                 sub_once(r"April 2025 are adopted but not yet in force",
                          "April 2025 are in force"),
                 "unsubstantiated_claims_absent"),
        Mutation("V", "falsify a recorded post-edit digest",
                 MANIFEST,
                 edit_manifest(lambda d: _card(d, "ENRICH-A039")
                               .__setitem__("post_edit_digest", "0" * 16)),
                 "manifest_digests_match"),
        Mutation("W", "edit a timed block on an authorised card",
                 QB_DIR / "QB4_A.html",
                 sub_once(r"Answer in <strong>four layers, not a list</strong>",
                          "Answer in <strong>five layers</strong>"),
                 "timed_blocks_unchanged"),
        Mutation("X", "revert one authorised card to baseline",
                 QB_DIR / "QB5_C_A.html",
                 lambda t: baseline_of("QB5_C_A.html"),
                 "every_authorised_card_changed"),
        Mutation("Y", "claim the A3.1 dimensions bind every ship afloat",
                 QB_DIR / "QB4_C.html",
                 sub_once(r"constructed on or after the date the Convention "
                          r"entered into force for the flag State",
                          "apply to all ships"),
                 "unsubstantiated_claims_absent"),
    ]


def main():
    if not assert_unowned():
        print("PRE-RUN %s#%s is owned by a manifest - mutation C would not "
              "test what it claims. Pick another card." % UNOWNED)
        return 2

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
            if mut.path.read_bytes() == orig:
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
        print("  %-2s %-56s %s" % (k, d, v))

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
