"""Mutation harness for the E6 enrichment guard.

Every mutation must actually change bytes before its "caught" result means
anything. E5 shipped a first run in which mutation C was anchored on a
'</div>' at end of file while the target file ends with '</html>': the pattern
never matched, the write changed nothing, and the mutation exercised nothing.
The harness reported NO-OP (not applied) exactly as designed, and the lesson is
that a reviewer must read that line. This harness keeps that contract:

    a mutation that does not alter its target certifies nothing, and its
    caught result must not be accepted.

So NO-OPs are counted separately and a run with any no-op is NOT green, even
if every other mutation was caught.

Mutation C edits a card no manifest owns anywhere. "Unowned" is asserted at run
time against every batch_*_manifest.json rather than trusted, because if the
card were in fact owned, C would prove the opposite of what it claims. Its edit
is anchored INSIDE the card on the q-card opening div, not on a file-terminal
pattern.

Read the SUMMARY line, not the body. Expected-caught mutations legitimately
print FAIL lines from the validator they are provoking; grepping raw FAIL
strings misreads a working harness as a broken one. Classification must key on
the "N mutations, N escape(s), N no-op(s), N crash(es)" summary.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
MANIFEST = TOOLS / "batch_e6_enrichment_manifest.json"
VALIDATOR = TOOLS / "validate_batch_e6.py"

sys.path.insert(0, str(TOOLS))
from oral_mutation import (              # noqa: E402
    require_control_baseline, mutation_verdict, validator_fail_details)
from oral_release_gates import BASELINE_REF   # noqa: E402
QB_DIR = REPO / "meoclass1"

# A card owned by no batch manifest at all. Asserted at run time.
UNOWNED = ("QB10_A.html", "q1")

BASELINE = "1b6c6c0"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run_validator():
    r = subprocess.run([sys.executable, str(VALIDATOR)],
                       cwd=str(REPO), capture_output=True)
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


def assert_unowned():
    owned = set()
    for sib in sorted(TOOLS.glob("batch_*_manifest.json")):
        for c in json.loads(sib.read_text(encoding="utf-8")).get("cards", []):
            owned.add((c["file"], c["anchor"]))
    return UNOWNED not in owned


# Injected into an LF file so the injection itself cannot introduce mixed
# line endings and be caught for the wrong reason.
NEW_CARD = (
    '<div class="q-card" id="q97" data-tags="imo">\n'
    '  <div class="q-header"><div class="q-num-badge">97</div>'
    '<div class="q-text-wrap"><div class="q-text">Injected.</div></div></div>\n'
    '  <div class="q-answer"><div class="answer-body"><p>Injected.</p></div></div>\n'
    '</div>\n')


def build():
    return [
        # ---- manifest identity ----
        Mutation("A", "omit one authorised action from the manifest",
                 MANIFEST, edit_manifest(lambda d: _drop(d, "ENRICH-A050")),
                 "authorised_action_set"),
        Mutation("B", "retarget an action to the wrong anchor",
                 MANIFEST,
                 edit_manifest(lambda d: _card(d, "ENRICH-A047")
                               .__setitem__("anchor", "q17")),
                 "authorised_targets"),
        # First run: this ESCAPED. The validator hardcoded "E6" and never read
        # authorisation_batch_key, so pointing it at another batch changed
        # nothing. The validator now selects the batch THROUGH the key, which
        # is what makes the field provenance rather than decoration.
        Mutation("L", "corrupt manifest/consolidation batch identity",
                 MANIFEST,
                 edit_manifest(lambda d: d.__setitem__("authorisation_batch_key",
                                                       "batches.E5")),
                 "authorisation_batch_key_matches_batch_id"),
        Mutation("L2", "flip an action's disposition to an invalid status",
                 MANIFEST,
                 edit_manifest(lambda d: _card(d, "ENRICH-A048")
                               .__setitem__("status", "DEFERRED")),
                 "authorised_enrichment_disposition"),
        Mutation("V", "falsify a recorded post-edit digest",
                 MANIFEST,
                 edit_manifest(lambda d: _card(d, "ENRICH-A045")
                               .__setitem__("post_edit_digest", "0" * 64)),
                 "manifest_digests_match"),
        Mutation("G", "misstate the canonical corpus total",
                 MANIFEST,
                 edit_manifest(lambda d: d.__setitem__(
                     "expected_canonical_questions", 722)),
                 "canonical_total_unchanged"),
        Mutation("J", "claim an examiner relationship delta",
                 MANIFEST,
                 edit_manifest(lambda d: d.__setitem__(
                     "expected_examiner_relationships", 961)),
                 "examiner_index_expectation_stable"),
        Mutation("W", "declare a timed-block change on an authorised card",
                 MANIFEST,
                 edit_manifest(lambda d: _card(d, "ENRICH-A047")
                               .__setitem__("timed_blocks_changed", True)),
                 "timed_blocks_unchanged"),
        Mutation("X", "declare E6 as creating a new card",
                 MANIFEST,
                 edit_manifest(lambda d: d.__setitem__("creates_new_cards", True)),
                 "manifest_declares_no_new_cards"),
        Mutation("Y", "collapse two E6 actions onto one shared target",
                 MANIFEST,
                 edit_manifest(lambda d: _card(d, "ENRICH-A049").update(
                     {"file": "QB6_F.html", "anchor": "q4"})),
                 "authorised_targets"),
        Mutation("Z", "silently drop the follow-up overlap declaration",
                 MANIFEST,
                 edit_manifest(lambda d: _card(d, "ENRICH-A046")
                               .__setitem__("followup_overlap", None)),
                 "followup_overlap_explicit"),
        Mutation("Z2", "claim GAP-0481 is consumed by the enrichment",
                 MANIFEST,
                 edit_manifest(lambda d: _card(d, "ENRICH-A046")["followup_overlap"]
                               .__setitem__("consumed", True)),
                 "followup_overlap_explicit"),
        Mutation("Z3", "drop the currentness record from a CURRENT_REG action",
                 MANIFEST,
                 edit_manifest(lambda d: _card(d, "ENRICH-A048")
                               .__setitem__("currentness", None)),
                 "currentness_recorded_for_current_reg"),
        Mutation("Z4", "misrecord a destination file's line endings",
                 MANIFEST,
                 edit_manifest(lambda d: _card(d, "ENRICH-A045")
                               .__setitem__("file_line_endings", "LF")),
                 "line_endings_homogeneous_per_file"),

        # ---- product mutations ----
        Mutation("C", "alter a neighbouring card no manifest owns",
                 QB_DIR / UNOWNED[0],
                 sub_once(r'(<div class="q-card"[^>]*id="%s"[^>]*>)' % UNOWNED[1],
                          r"\1<!-- e6-mutation-c -->"),
                 "only_authorised_cards_changed"),
        Mutation("D", "blank one supplied limb (A050 ITU identity)",
                 QB_DIR / "QB6_F.html",
                 sub_once(r"International Telecommunication Union", "ITU"),
                 "missing_limb_supplied"),
        Mutation("D2", "blank A047's completed declaration count",
                 QB_DIR / "QB1_A.html",
                 sub_once(r"<strong>thirteen, \(a\) to \(m\)</strong>", "several"),
                 "missing_limb_supplied"),
        Mutation("E", "inject an internal action id into candidate prose",
                 QB_DIR / "QB3_J.html",
                 sub_once(r"(The Indian Statutory Frame)", r"\1 [ENRICH-A048]"),
                 "no_candidate_visible_metadata"),
        Mutation("E2", "expose internal pending-verification status in new prose",
                 QB_DIR / "QB9_B.html",
                 sub_once(r"(Strategic Layer vs Tactical Layer)",
                          r"\1 (pending verification)"),
                 "no_candidate_visible_metadata"),
        Mutation("F", "add a canonical q-card",
                 QB_DIR / "QB6_F.html",
                 sub_once(r'(\n\s*<div class="q-card" id="q4")',
                          NEW_CARD + r"\1"),
                 "canonical_total_unchanged"),
        # First run: this was a NO-OP. The pattern read
        # "resolution <strong>MSC.550(108)</strong>" while the card reads
        # "<strong>resolution MSC.550(108)</strong>" - the tag opens BEFORE the
        # word. It matched nothing, wrote nothing, and certified nothing. The
        # harness reported NO-OP rather than counting it as a pass, which is
        # the entire reason that distinction exists.
        Mutation("H", "strip a required primary authority (A047 MSC.550(108))",
                 QB_DIR / "QB1_A.html",
                 sub_once(r"<strong>resolution MSC\.550\(108\)</strong>",
                          "a recent resolution"),
                 "required_authority_cited"),
        Mutation("H2", "strip A050's Radio Regulations appendix authority",
                 QB_DIR / "QB6_F.html",
                 sub_once(r"<strong>Appendix 42</strong>", "the relevant appendix"),
                 "required_authority_cited"),
        Mutation("I", "alter the q-text of an authorised card",
                 QB_DIR / "QB3_J.html",
                 sub_once(r'(<div class="q-text">)What is NOS-DCP\?',
                          r"\1What is the NOSDCP?"),
                 "q_text_and_anchors_stable"),
        Mutation("I2", "re-anchor an authorised card",
                 QB_DIR / "QB6_F.html",
                 sub_once(r'(<div class="q-card"[^>]*)id="q4"', r'\1id="q41"'),
                 "targets_resolve"),
        # K RETARGETED, 2026-08-26. It used to delete from QB9_G#q3, which
        # CORR-DEFN-TREATY-20260825 has since SUPERSEDED. On a superseded card
        # `edits_purely_additive` compares E6's baseline against the state E6
        # itself produced -- recovered from git, so a working-tree deletion
        # cannot move it -- and K began reporting WRONG REASON, caught by
        # `manifest_digests_match` instead. That is a real escape by this
        # suite's own rule: a mutation caught only because a digest moved has
        # not proved its own guard.
        #
        # The card was always an arbitrary choice; the mutation exists to prove
        # that deleting BASELINE text trips ADDITIVITY. So it now deletes from
        # an UNSUPERSEDED authorised card, which tests exactly what it always
        # tested. "Onboard Integration" carries no LIMB, AUTHORITY or
        # QUALIFIER token of A050, so additivity is the only substantive check
        # it can trip -- the same property that made the FAL heading a good
        # target before.
        Mutation("K", "delete baseline text from an authorised card",
                 QB_DIR / "QB6_F.html",
                 sub_once(r"<h4>Onboard Integration</h4>", ""),
                 "edits_purely_additive"),
        # K2 is K's other half, and the reason this is a repair rather than a
        # retreat. Retargeting K alone would leave "the superseded card is
        # still guarded against live deletion" as an ASSERTION. K2 makes it a
        # RESULT: it performs the very deletion K used to perform, on the very
        # card K used to perform it on, and requires the check that coverage
        # MOVED to. If a future change ever breaks the chain check, K2 goes red
        # instead of the gap being discovered by accident years later.
        Mutation("K2", "delete live text from a SUPERSEDED authorised card",
                 QB_DIR / "QB9_G.html",
                 sub_once(r"<h4>FAL Committee</h4>", ""),
                 "manifest_digests_match"),
        Mutation("M", "staledate the in-force container-loss regime",
                 QB_DIR / "QB1_A.html",
                 sub_once(r"Since <strong>1 January 2026</strong>, amendments "
                          r"adopted by <strong>resolution MSC\.550\(108\)</strong> "
                          r"have required",
                          "MSC.550(108) is not yet in force, but will require"),
                 "required_qualifiers_kept"),
        Mutation("N", "convert the adopted-not-operating IMSAS framework "
                      "into today's regime",
                 QB_DIR / "QB4_I.html",
                 sub_once(r"adopted but does not begin to operate until the "
                          r"second cycle opens",
                          "already in force and the second cycle is under way"),
                 "required_qualifiers_kept"),
        Mutation("N2", "assert IMSAS audits are performed by IMO staff",
                 QB_DIR / "QB4_I.html",
                 sub_once(r"the auditors are <strong>not IMO staff</strong>",
                          "the audits are conducted by IMO staff"),
                 "required_qualifiers_kept"),
        Mutation("O", "name a FAL form as the container-loss vehicle",
                 QB_DIR / "QB1_A.html",
                 sub_once(r"<strong>No FAL declaration carries a container-loss "
                          r"report\.</strong>",
                          "FAL Form 8 carries the container loss report."),
                 "required_qualifiers_kept"),
        Mutation("P", "import 1958-Act section numbering into the 2025 Act",
                 QB_DIR / "QB3_J.html",
                 sub_once(r"<strong>sections 133 to 143</strong>",
                          "<strong>section 356A</strong>"),
                 "missing_limb_supplied"),
        # P removes the limb token as well, so it could be caught by either
        # guard. P2 injects the 1958-Act numbering while LEAVING the correct
        # section block in place, so only the forbidden-claim guard can catch
        # it - which is what proves that guard fires on the real card rather
        # than being carried by the limb check.
        Mutation("P2", "add 1958-Act numbering alongside the correct block",
                 QB_DIR / "QB3_J.html",
                 sub_once(r"(<strong>sections 133 to 143</strong>)",
                          r"\1 (formerly section 356A)"),
                 "unsubstantiated_claims_absent"),
        Mutation("Q", "drop A048's no-threshold qualifier",
                 QB_DIR / "QB3_J.html",
                 sub_once(r"the duty bites on a discharge <strong>of any "
                          r"quantity</strong>",
                          "the duty bites on a significant discharge"),
                 "required_qualifiers_kept"),
        Mutation("R", "flatten A046's code-binding thesis",
                 QB_DIR / "QB9_G.html",
                 sub_once(r"<strong>no binding force of its own</strong>",
                          "full binding force"),
                 "missing_limb_supplied"),
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
            after = mut.path.read_bytes()
            if after == orig:
                noops += 1
                results.append((mut.key, mut.desc, "NO-OP (not applied)", 0))
                continue
            delta = len(after) - len(orig)
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
            results.append((mut.key, mut.desc, verdict, delta))
        except Exception as e:                                  # noqa: BLE001
            crashes += 1
            results.append((mut.key, mut.desc, "*** CRASH: %s ***" % e, 0))
        finally:
            mut.path.write_bytes(orig)
            if sha(mut.path.read_bytes()) != sha(orig):
                print("  !! restore failed for %s" % mut.key)

    for k, d, v, delta in results:
        print("  %-3s %-58s %+6d B  %s" % (k, d, delta, v))

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
